"""Backfill chapters de `intro-al-algebra` a cursos universitarios cuyo syllabus
oficial incluye Lógica / Inducción / Conjuntos / Geometría analítica, pero el
seed inicial sólo linkeó chapters de `precalculo` (que NO cubre esos temas).

Ejemplo concreto que motivó este script: UDP CBM1100 "Introducción al Álgebra"
tiene un eje "Teoría de conjuntos y lógica" pero los 8 chapters linkeados son
todos de `precalculo` (Funciones, Trigonometría, Exp/Log...).

`intro-al-algebra` es el curso base de Remy modelado sobre PUC MAT1207, con
5 chapters:
  - ch-ia-lenguaje              ← Lógica proposicional + Conjuntos
  - ch-ia-naturales             ← Sumatorias + Inducción + Binomio
  - ch-ia-trigonometria         (solapa con precalculo, NO linkeamos)
  - ch-ia-polinomios            (solapa con precalculo, NO linkeamos)
  - ch-ia-geometria-analitica   ← Cónicas + Rectas + Planos (no en precalculo)

Idempotente: si un chapter ya está linkeado al curso destino, se skipea.
"""
from __future__ import annotations

import asyncio
import os
import re
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

# Cursos que claramente NO son de álgebra (falsos positivos por "conjuntos de
# nivel" en cálculo multivariable, etc.).
EXCLUDE = {
    "uch-plan-comun-fcfm-ma2001-calculo-en-varias-variables",
    "utfsm-plan-comun-ing-civil-calculo-en-varias-variables",
}

# Patrones de keyword por chapter de intro-al-algebra.
# Si el syllabus del curso (cualquier axis) matchea, se linkea el chapter.
KW_LENGUAJE = re.compile(
    r"\b(l[oó]gica|proposici|tablas?\s+de\s+verdad|cuantificad|conectores l[oó]gicos|conjuntos)\b",
    re.IGNORECASE,
)
KW_NATURALES = re.compile(
    r"\b(inducci[oó]n|sumatori|progresi|binomio|teorema del binomio|n[uú]meros naturales)\b",
    re.IGNORECASE,
)
KW_GEOM = re.compile(
    r"\b(geometr[ií]a anal[ií]tica|c[oó]nica|rectas y planos|circunferenci|par[aá]bola|elipse|hip[eé]rbola)\b",
    re.IGNORECASE,
)

# Chapter slugs de intro-al-algebra.
CH_IA = {
    "lenguaje": "ch-ia-lenguaje",
    "naturales": "ch-ia-naturales",
    "geometria": "ch-ia-geometria-analitica",
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


async def link_chapter(db, course_id: str, template_chapter_id: str) -> bool:
    """Crea un chapter linkeado si no existe. Devuelve True si creó nuevo."""
    existing = await db.chapters.find_one(
        {"course_id": course_id, "template_chapter_id": template_chapter_id},
        {"_id": 0, "id": 1},
    )
    if existing:
        return False
    template = await db.chapters.find_one({"id": template_chapter_id}, {"_id": 0})
    if not template:
        print(f"  WARNING: template chapter {template_chapter_id} no existe")
        return False
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
    return True


async def main():
    use_atlas = "--target-atlas" in sys.argv
    dry = "--dry-run" in sys.argv
    if use_atlas:
        os.environ["MONGO_URL"] = os.environ["ATLAS_URL"]
    label = "ATLAS" if use_atlas else "local"
    print(f"== Backfill intro-al-algebra coverage — target: {label} {'(DRY-RUN)' if dry else ''} ==\n")

    c = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = c[os.environ["DB_NAME"]]

    courses = await db.courses.find(
        {"university_id": {"$ne": None}},
        {"_id": 0, "id": 1, "title": 1, "base_course_ids": 1, "university_id": 1},
    ).to_list(500)

    affected = 0
    total_links_added = 0
    for course in courses:
        cid = course["id"]
        if cid in EXCLUDE:
            continue
        if "intro-al-algebra" in (course.get("base_course_ids") or []):
            continue
        axes = await db.course_axes.find({"course_id": cid}, {"_id": 0, "text": 1}).to_list(50)
        all_text = " | ".join(ax.get("text", "") for ax in axes)
        if not KW_LENGUAJE.search(all_text):
            continue

        to_link = ["lenguaje"]
        if KW_NATURALES.search(all_text):
            to_link.append("naturales")
        if KW_GEOM.search(all_text):
            to_link.append("geometria")

        # Verificar que el curso ya no tenga chapters equivalentes (linkeados
        # desde precalculo). Como precalculo NO tiene equivalente de
        # `ch-ia-lenguaje` ni `ch-ia-naturales`, no hace falta check.
        # Para `ch-ia-geometria-analitica`: precalculo no tiene tampoco.

        affected += 1
        print(f"  {cid}")
        new_links = 0
        for key in to_link:
            template_id = CH_IA[key]
            if dry:
                print(f"    [DRY] would link {template_id}")
                new_links += 1
            else:
                created = await link_chapter(db, cid, template_id)
                marker = "+" if created else "="
                print(f"    {marker} {template_id}")
                if created:
                    new_links += 1
        total_links_added += new_links

        # Actualizar base_course_ids para sumar 'intro-al-algebra'.
        if not dry and new_links > 0:
            new_bases = list(dict.fromkeys((course.get("base_course_ids") or []) + ["intro-al-algebra"]))
            await db.courses.update_one({"id": cid}, {"$set": {"base_course_ids": new_bases}})

    print()
    print(f"== Resumen ==")
    print(f"  Cursos afectados: {affected}")
    print(f"  Chapter links {'a crear' if dry else 'creados'}: {total_links_added}")
    c.close()


if __name__ == "__main__":
    asyncio.run(main())
