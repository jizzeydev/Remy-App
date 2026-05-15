"""Aplica los gaps detectados por los agentes de verificación de syllabi.

Input: un archivo JSON consolidado con la siguiente forma:
  {
    "fixes": [
      {
        "course_id": "udp-plan-comun-ing-civil-introduccion-al-algebra",
        "source_url": "https://eit.udp.cl/.../CBM1100.pdf",
        "chapters_to_link": ["ch-ia-lenguaje", "ch-ia-naturales"],
        "note": "Programa oficial incluye lógica + inducción"
      },
      ...
    ]
  }

Operación: para cada fix, linkear los chapters de la lista al curso (idempotente,
skipea los ya linkeados). Actualiza base_course_ids con los slugs de los cursos
base de los chapters agregados. NO toca chapters ya existentes ni axes.

Usage:
  backend/venv/Scripts/python.exe scripts/apply_syllabus_gaps.py [--target-atlas] [--dry-run] <fixes.json>
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(Path(__file__).resolve().parent.parent / "backend" / ".env")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


async def link_chapter(db, course_id: str, template_chapter_id: str) -> tuple[bool, str | None]:
    """Crea un chapter linkeado si no existe. Devuelve (created, base_course_id_of_template)."""
    existing = await db.chapters.find_one(
        {"course_id": course_id, "template_chapter_id": template_chapter_id},
        {"_id": 0, "id": 1},
    )
    template = await db.chapters.find_one({"id": template_chapter_id}, {"_id": 0})
    if not template:
        return (False, None)
    if existing:
        return (False, template.get("course_id"))
    last = await db.chapters.find_one(
        {"course_id": course_id}, {"order": 1}, sort=[("order", -1)]
    )
    next_order = (last.get("order", 0) if last else 0) + 1
    await db.chapters.insert_one({
        "id": str(uuid.uuid4()),
        "course_id": course_id,
        "title": template.get("title", ""),
        "description": template.get("description", ""),
        "order": next_order,
        "template_chapter_id": template_chapter_id,
        "excluded_lesson_ids": [],
        "excluded_question_ids": [],
        "created_at": now_iso(),
    })
    return (True, template.get("course_id"))


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_atlas = "--target-atlas" in sys.argv
    dry = "--dry-run" in sys.argv

    if not args:
        print("Usage: apply_syllabus_gaps.py [--target-atlas] [--dry-run] <fixes.json>")
        sys.exit(1)

    if use_atlas:
        os.environ["MONGO_URL"] = os.environ["ATLAS_URL"]
    print(f"== Apply syllabus gaps — target: {'ATLAS' if use_atlas else 'local'} {'(DRY-RUN)' if dry else ''} ==\n")

    with open(args[0], encoding="utf-8") as f:
        data = json.load(f)

    fixes = data.get("fixes") or []
    c = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = c[os.environ["DB_NAME"]]

    total_links_created = 0
    total_skipped_existing = 0
    total_unknown_templates = 0
    courses_touched = 0
    by_uni_summary: dict = {}

    for fix in fixes:
        cid = fix.get("course_id")
        templates = fix.get("chapters_to_link") or []
        if not cid or not templates:
            continue
        course = await db.courses.find_one({"id": cid}, {"_id": 0, "id": 1, "base_course_ids": 1, "university_id": 1})
        if not course:
            print(f"  ✗ {cid}: curso no existe en DB, skip")
            continue
        courses_touched += 1
        new_bases: set = set(course.get("base_course_ids") or [])
        created_this_course = 0
        print(f"  · {cid}")
        for tcid in templates:
            if dry:
                t = await db.chapters.find_one({"id": tcid}, {"_id": 0, "course_id": 1, "title": 1})
                if t:
                    print(f"    [DRY] would link {tcid} ({t.get('course_id')}/{t.get('title')})")
                    new_bases.add(t.get("course_id"))
                else:
                    print(f"    [DRY] UNKNOWN template {tcid}")
                    total_unknown_templates += 1
                continue
            created, base_id = await link_chapter(db, cid, tcid)
            if base_id is None:
                print(f"    ! UNKNOWN template {tcid}")
                total_unknown_templates += 1
                continue
            if created:
                print(f"    + {tcid} ({base_id})")
                total_links_created += 1
                created_this_course += 1
            else:
                total_skipped_existing += 1
            new_bases.add(base_id)
        if not dry and (created_this_course > 0 or new_bases != set(course.get("base_course_ids") or [])):
            await db.courses.update_one({"id": cid}, {"$set": {"base_course_ids": sorted(new_bases)}})

    print()
    print("== Resumen ==")
    print(f"  Cursos tocados:               {courses_touched}")
    print(f"  Chapter links creados:        {total_links_created}")
    print(f"  Skipped (ya existían):        {total_skipped_existing}")
    print(f"  Templates desconocidos:       {total_unknown_templates}")
    c.close()


if __name__ == "__main__":
    asyncio.run(main())
