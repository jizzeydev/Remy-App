"""Importar preguntas desde un CSV directo a Mongo local (sin pasar por la API).

Útil para mass-edit de bancos de preguntas mientras autoreás contenido en local.
Después de correr esto, validá en `localhost:3007/quiz/<chapter_id>` y empujá a
prod con `python scripts/sync_content_to_atlas.py "<URI>" --confirm`.

Lógica de parsing replicada del endpoint admin
`POST /api/admin/questions/import-csv/{course_id}` (backend/server.py:1426).
Mantené las dos en sync si cambia el formato.

CSV format esperado (NUEVO, columnas separadas):
    capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion

  - capitulo: nombre exacto (case-insensitive) del capítulo en la DB.
  - leccion:  nombre de la lección (opcional). Si no matchea, queda sin lesson_id.
  - dificultad: fácil | medio | difícil (acepta sin tildes y aliases en inglés).
  - enunciado: pregunta. Soporta Markdown + LaTeX con $...$.
  - opcion_a..d: alternativas. Mínimo A y B; C y D opcionales.
  - respuesta_correcta: A | B | C | D.
  - explicacion: razonamiento de la respuesta (opcional).

Formato LEGACY (pipe-separated) también soportado por compatibilidad.

Uso:
    # agrega preguntas al curso (no toca las existentes)
    python scripts/import_questions_csv.py <course_id> <ruta-al-csv>

    # reemplaza TODO el banco del curso entero (raro — usar con cuidado)
    python scripts/import_questions_csv.py <course_id> <ruta-al-csv> --replace-course

    # reemplaza solo las preguntas de un capítulo (recomendado para mass-edit)
    python scripts/import_questions_csv.py <course_id> <ruta-al-csv> --replace-chapter <chapter_id>

    # dry-run: parsea el CSV y reporta qué pasaría, no escribe nada
    python scripts/import_questions_csv.py <course_id> <ruta-al-csv> --dry-run

Lee MONGO_URL y DB_NAME de backend/.env.
"""
from __future__ import annotations

import argparse
import asyncio
import csv as csv_module
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"


DIFFICULTY_MAP = {
    "fácil": "fácil", "facil": "fácil",
    "medio": "medio",
    "difícil": "difícil", "dificil": "difícil",
    "easy": "fácil", "medium": "medio", "hard": "difícil",
}


def read_csv_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    sys.exit(f"ERROR: no pude decodificar '{path}'. Guardalo como UTF-8.")


def parse_row(row: dict, row_num: int) -> tuple[dict | None, str | None]:
    """Devuelve (campos_de_pregunta, error_msg). Una de las dos es None."""
    is_new_format = "enunciado" in row or "opcion_a" in row

    if is_new_format:
        question_text = (row.get("enunciado") or "").strip()
        if not question_text:
            return None, "enunciado es requerido"

        a = (row.get("opcion_a") or "").strip()
        b = (row.get("opcion_b") or "").strip()
        c = (row.get("opcion_c") or "").strip()
        d = (row.get("opcion_d") or "").strip()
        if not a or not b:
            return None, "se necesitan al menos opciones A y B"

        options = [f"A) {a}", f"B) {b}"]
        if c:
            options.append(f"C) {c}")
        if d:
            options.append(f"D) {d}")

        correct = (row.get("respuesta_correcta") or "").strip().upper()
        explanation = (row.get("explicacion") or "").strip() or None
        capitulo = (row.get("capitulo") or "").strip().lower()
        leccion = (row.get("leccion") or "").strip().lower()
        difficulty_raw = (row.get("dificultad") or "").strip().lower() or "medio"
    else:
        question_text = (row.get("question_text") or "").strip()
        if not question_text:
            return None, "question_text es requerido"

        options_str = (row.get("options") or "").strip()
        if not options_str:
            return None, "options es requerido"
        options = [o.strip() for o in options_str.split("|") if o.strip()]
        if len(options) < 2:
            return None, "se necesitan al menos 2 opciones (separadas por |)"

        correct = (row.get("correct_answer") or "").strip().upper()
        explanation = (row.get("explanation") or "").strip() or None
        # En el formato legacy chapter_id/lesson_id vienen explícitos.
        capitulo = ""
        leccion = ""
        difficulty_raw = (row.get("difficulty") or "").strip().lower() or "medio"
        # Devolvemos también los ids legacy para que el caller los use sin lookup.
        return ({
            "_legacy_chapter_id": (row.get("chapter_id") or "").strip() or None,
            "_legacy_lesson_id": (row.get("lesson_id") or "").strip() or None,
            "question_text": question_text,
            "options": options,
            "correct_answer": correct,
            "explanation": explanation,
            "difficulty": DIFFICULTY_MAP.get(difficulty_raw, "medio"),
            "_capitulo": "",
            "_leccion": "",
        }, None)

    if not correct:
        return None, "respuesta_correcta es requerido"

    return ({
        "question_text": question_text,
        "options": options,
        "correct_answer": correct,
        "explanation": explanation,
        "difficulty": DIFFICULTY_MAP.get(difficulty_raw, "medio"),
        "_capitulo": capitulo,
        "_leccion": leccion,
    }, None)


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("course_id", help="ID del curso (ej: 'algebra-lineal')")
    parser.add_argument("csv_path", help="Ruta al archivo CSV")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--replace-course", action="store_true",
                   help="Borra TODAS las preguntas del curso antes de insertar (peligroso)")
    g.add_argument("--replace-chapter", metavar="CHAPTER_ID",
                   help="Borra todas las preguntas del capítulo indicado antes de insertar")
    parser.add_argument("--dry-run", action="store_true",
                        help="Parsea + muestra plan, no escribe nada")
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        sys.exit(f"ERROR: no existe {csv_path}")

    load_dotenv(BACKEND_DIR / ".env")
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]

    course = await db.courses.find_one({"id": args.course_id}, {"_id": 0})
    if not course:
        sys.exit(f"ERROR: curso '{args.course_id}' no existe en Mongo local.")

    # Mapas de capítulos y lecciones para resolver nombres → ids.
    chapters = await db.chapters.find({"course_id": args.course_id}, {"_id": 0}).to_list(500)
    chapter_map = {(c.get("title") or "").lower().strip(): c.get("id") for c in chapters}

    lesson_map: dict[str, str] = {}
    chapter_titles_by_id = {c.get("id"): (c.get("title") or "").lower().strip() for c in chapters}
    for ch in chapters:
        ch_lessons = await db.lessons.find({"chapter_id": ch.get("id")}, {"_id": 0}).to_list(500)
        for ls in ch_lessons:
            ls_title = (ls.get("title") or "").lower().strip()
            ch_title = (ch.get("title") or "").lower().strip()
            lesson_map[f"{ch_title}|{ls_title}"] = ls.get("id")
            lesson_map.setdefault(ls_title, ls.get("id"))  # fallback sin chapter

    if args.replace_chapter and args.replace_chapter not in chapter_titles_by_id:
        sys.exit(f"ERROR: capítulo '{args.replace_chapter}' no pertenece al curso '{args.course_id}'.")

    text = read_csv_text(csv_path)
    reader = csv_module.DictReader(text.splitlines())

    parsed: list[dict] = []
    errors: list[str] = []
    row_num = 1
    for row in reader:
        row_num += 1
        fields, err = parse_row(row, row_num)
        if err:
            errors.append(f"Fila {row_num}: {err}")
            continue

        chapter_id = fields.pop("_legacy_chapter_id", None)
        lesson_id = fields.pop("_legacy_lesson_id", None)
        capitulo = fields.pop("_capitulo", "")
        leccion = fields.pop("_leccion", "")

        if not chapter_id and capitulo:
            chapter_id = chapter_map.get(capitulo)
            if not chapter_id:
                errors.append(f"Fila {row_num}: capítulo '{capitulo}' no encontrado en el curso")
                # No abortamos; insertamos sin chapter_id pero avisamos.
        if not lesson_id and leccion:
            if capitulo:
                lesson_id = lesson_map.get(f"{capitulo}|{leccion}") or lesson_map.get(leccion)
            else:
                lesson_id = lesson_map.get(leccion)

        question = {
            "id": str(uuid.uuid4()),
            "course_id": args.course_id,
            "chapter_id": chapter_id,
            "lesson_id": lesson_id,
            "question_text": fields["question_text"],
            "question_type": "multiple_choice",
            "options": fields["options"],
            "correct_answer": fields["correct_answer"],
            "explanation": fields["explanation"],
            "difficulty": fields["difficulty"],
            "image_url": None,
            "source": "csv_import_cli",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        parsed.append(question)

    print(f"Curso:        {course.get('title')} ({args.course_id})")
    print(f"CSV:          {csv_path}")
    print(f"Filas OK:     {len(parsed)}")
    print(f"Filas error:  {len(errors)}")
    for e in errors[:10]:
        print(f"  - {e}")
    if len(errors) > 10:
        print(f"  ... ({len(errors) - 10} más)")

    if not parsed:
        print("\nNada que insertar. Saliendo.")
        return 1 if errors else 0

    # Plan de borrado.
    delete_filter: dict | None = None
    if args.replace_course:
        delete_filter = {"course_id": args.course_id}
        will_delete = await db.questions.count_documents(delete_filter)
        print(f"\n⚠️  --replace-course: se borrarán {will_delete} preguntas del curso entero.")
    elif args.replace_chapter:
        delete_filter = {"course_id": args.course_id, "chapter_id": args.replace_chapter}
        will_delete = await db.questions.count_documents(delete_filter)
        print(f"\n⚠️  --replace-chapter: se borrarán {will_delete} preguntas del capítulo "
              f"'{chapter_titles_by_id[args.replace_chapter]}'.")

    if args.dry_run:
        print("\nDry-run. No se escribió nada.")
        return 0

    if delete_filter is not None:
        res = await db.questions.delete_many(delete_filter)
        print(f"Borrados: {res.deleted_count}")

    if parsed:
        await db.questions.insert_many(parsed)
    total_after = await db.questions.count_documents({"course_id": args.course_id})
    print(f"Insertados: {len(parsed)}")
    print(f"Total ahora en el curso: {total_after}")
    print()
    print("✅ Listo. Verificá en http://localhost:3007/quiz/<chapter_id> antes de sync a Atlas.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
