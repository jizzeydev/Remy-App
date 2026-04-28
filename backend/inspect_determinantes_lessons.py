"""
Read-only: lista chapters del curso algebra-lineal y las lecciones del
capitulo "Determinantes" tal como estan guardadas en la BD.

Sirve para descubrir por que el import del CSV no pudo asociar lecciones
(probablemente los titulos en la BD no coinciden con los del CSV).

Uso:
    cd backend
    python inspect_determinantes_lessons.py
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('.env')

COURSE_ID = "algebra-lineal"
CHAPTER_TITLE_HINT = "determinant"


async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    chapters = await db.chapters.find({"course_id": COURSE_ID}, {"_id": 0}).to_list(100)
    print(f"Chapters de course='{COURSE_ID}': {len(chapters)}")
    for ch in chapters:
        print(f"  - id={ch.get('id')}  title={ch.get('title')!r}")

    target_chapters = [
        ch for ch in chapters
        if CHAPTER_TITLE_HINT in (ch.get('title') or '').lower()
    ]
    if not target_chapters:
        print(f"\nNo encontre chapter con '{CHAPTER_TITLE_HINT}' en el titulo.")
        return

    for ch in target_chapters:
        print(f"\n=== Lessons del chapter '{ch.get('title')}' (id={ch.get('id')}) ===")
        lessons = await db.lessons.find(
            {"chapter_id": ch.get('id')}, {"_id": 0}
        ).to_list(100)
        for lesson in lessons:
            print(f"  - id={lesson.get('id')}  title={lesson.get('title')!r}")

        q_count = await db.questions.count_documents({"chapter_id": ch.get('id')})
        q_csv = await db.questions.count_documents({
            "chapter_id": ch.get('id'),
            "source": "csv_import",
        })
        q_orphan = await db.questions.count_documents({
            "chapter_id": ch.get('id'),
            "source": "csv_import",
            "$or": [
                {"lesson_id": None},
                {"lesson_id": ""},
                {"lesson_id": {"$exists": False}},
            ],
        })
        print(f"\n  Preguntas en este chapter: total={q_count}  csv_import={q_csv}  huerfanas={q_orphan}")


if __name__ == "__main__":
    asyncio.run(main())
