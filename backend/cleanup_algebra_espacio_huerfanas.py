"""
Limpia las preguntas huerfanas del curso algebra-lineal capitulo Espacio.

Una pregunta es "huerfana" cuando se importo via CSV pero no se asocio a
ninguna leccion (porque las lecciones aun no existian en la BD).

Esto pasa cuando:
- source = "csv_import"
- course_id = "algebra-lineal"
- lesson_id IS NULL (o vacio)

Las pasa a la papelera para no perderlas definitivamente.

Uso:
    cd backend
    python cleanup_algebra_espacio_huerfanas.py            # dry run (solo lista)
    python cleanup_algebra_espacio_huerfanas.py --apply    # ejecuta el borrado
"""
import asyncio
import os
import sys
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('.env')

COURSE_ID = "algebra-lineal"


async def main(apply: bool):
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    query = {
        "course_id": COURSE_ID,
        "source": "csv_import",
        "$or": [
            {"lesson_id": None},
            {"lesson_id": ""},
            {"lesson_id": {"$exists": False}},
        ],
    }

    huerfanas = await db.questions.find(query, {"_id": 0}).to_list(10000)
    print(f"Preguntas huerfanas encontradas en course='{COURSE_ID}': {len(huerfanas)}")

    if not huerfanas:
        print("Nada que limpiar.")
        return

    print("\nMuestra (primeras 5):")
    for q in huerfanas[:5]:
        text = (q.get('question_text') or '')[:90].replace('\n', ' ')
        print(f"  - id={q['id'][:8]}  chapter_id={q.get('chapter_id')}  text={text!r}")

    if not apply:
        print("\nDRY RUN: no se borro nada. Vuelve a ejecutar con --apply para borrar.")
        return

    # Mover a papelera (igual que el endpoint delete)
    moved = 0
    for q in huerfanas:
        title = (q.get("question_text") or "")[:80] or "(sin enunciado)"
        trash_doc = {
            "type": "question",
            "id": q["id"],
            "title": title,
            "payload": q,
            "deleted_by": "cleanup_script",
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
