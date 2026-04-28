"""
Borra (manda a papelera) TODAS las preguntas importadas por CSV en el
capitulo "Determinantes" del curso algebra-lineal, tengan o no leccion
asociada. Util cuando el import quedo mal y se quiere re-importar limpio.

Filtros:
- course_id = "algebra-lineal"
- chapter_id = id del capitulo cuyo titulo matchea "Determinantes"
- source = "csv_import"

Uso:
    cd backend
    python cleanup_determinantes_csv.py            # dry run (lista)
    python cleanup_determinantes_csv.py --apply    # ejecuta
"""
import asyncio
import os
import sys
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('.env')

COURSE_ID = "algebra-lineal"
CHAPTER_TITLE = "Determinantes"


async def main(apply: bool):
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    chapter = await db.chapters.find_one(
        {"course_id": COURSE_ID, "title": CHAPTER_TITLE}, {"_id": 0}
    )
    if not chapter:
        candidates = await db.chapters.find(
            {"course_id": COURSE_ID}, {"_id": 0, "id": 1, "title": 1}
        ).to_list(100)
        print(f"No encontre chapter con titulo exacto '{CHAPTER_TITLE}' en course='{COURSE_ID}'.")
        print("Chapters disponibles:")
        for c in candidates:
            print(f"  - id={c.get('id')}  title={c.get('title')!r}")
        sys.exit(1)

    chapter_id = chapter.get('id')
    print(f"Chapter encontrado: id={chapter_id}  title={chapter.get('title')!r}")

    query = {
        "course_id": COURSE_ID,
        "chapter_id": chapter_id,
        "source": "csv_import",
    }

    questions = await db.questions.find(query, {"_id": 0}).to_list(10000)
    print(f"\nPreguntas a borrar (csv_import en este chapter): {len(questions)}")

    if not questions:
        print("Nada que limpiar.")
        return

    by_lesson = {}
    for q in questions:
        lid = q.get('lesson_id') or '(sin leccion)'
        by_lesson[lid] = by_lesson.get(lid, 0) + 1
    print("\nDistribucion por lesson_id:")
    for lid, n in by_lesson.items():
        short = lid if lid == '(sin leccion)' else lid[:12]
        print(f"  - {short}: {n}")

    print("\nMuestra (primeras 5):")
    for q in questions[:5]:
        text = (q.get('question_text') or '')[:90].replace('\n', ' ')
        print(f"  - id={q['id'][:8]}  lesson_id={q.get('lesson_id')}  text={text!r}")

    if not apply:
        print("\nDRY RUN: no se borro nada. Ejecuta con --apply para mandar a papelera.")
        return

    moved = 0
    for q in questions:
        title = (q.get("question_text") or "")[:80] or "(sin enunciado)"
        trash_doc = {
            "type": "question",
            "id": q["id"],
            "title": title,
            "payload": q,
            "deleted_by": "cleanup_determinantes_csv",
            "deleted_at": datetime.now(timezone.utc).isoformat(),
            "course_id": q.get("course_id"),
            "chapter_id": q.get("chapter_id"),
            "lesson_id": q.get("lesson_id"),
        }
        await db.trash.insert_one(trash_doc)
        await db.questions.delete_one({"id": q["id"]})
        moved += 1

    print(f"\nMovidas a papelera: {moved} preguntas.")
    print("Para restaurar: usa la papelera del panel admin.")


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    asyncio.run(main(apply))
