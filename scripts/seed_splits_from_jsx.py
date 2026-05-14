"""Seed de splits universitarios desde los .jsx de investigación.

Parsea los 12 archivos `docs/splits-data/*.jsx` (vía un wrapper Node para
evaluar los literales JS) y crea en Remy:
  - universidades (idempotente: backfill de tier si falta)
  - cursos universitarios con match_level "alto" o "medio"
  - axes (los items del array `contenidos` de cada ramo)
  - chapter links a los cursos base correspondientes (resolviendo aliases)

**Create-only / safe-for-prod**:
  - Si el slug del curso ya existe en la DB (id o alt_slugs), SKIP completo.
    No se tocan campos, chapters ni axes. El admin manda en lo ya curado.
  - Cursos base generales nunca se escriben — sólo se leen sus chapter IDs.
  - Universidades existentes: sólo backfill de `tier` cuando está vacío.

Ramos con matchLevel "bajo" / "ninguno" / desconocido: skip silencioso (no se
crean en Remy hasta que tengamos material base que los cubra).

Slugs huérfanos (ej. calc-dif-udd-civil del udd.jsx): se filtran del match[]
antes de resolver aliases. Como esos slugs nunca vienen solos, los ramos
quedan con base genérica correcta.

Usage:
    backend/venv/Scripts/python.exe scripts/seed_splits_from_jsx.py
    # contra Atlas:
    MONGO_URL="$ATLAS_URL" DB_NAME=remy_database \\
        backend/venv/Scripts/python.exe scripts/seed_splits_from_jsx.py

Variables de entorno:
    MONGO_URL, DB_NAME (vienen de backend/.env). Si se pasa MONGO_URL distinto,
    apunta a la DB target (típicamente Atlas para prod).
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
import unicodedata
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

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
JSX_DIR = REPO_ROOT / "docs" / "splits-data"
NODE_PARSER = REPO_ROOT / "scripts" / "parse_splits_jsx.js"

load_dotenv(BACKEND_DIR / ".env")
sys.path.insert(0, str(BACKEND_DIR))
from services.base_slug_aliases import BASE_SLUG_ALIASES, resolve_base_slugs  # noqa: E402


# ============================================================
# Metadata de universidades (sigla → nombre completo + tier)
# El parser deduce sigla del nombre del archivo; aquí mapeamos al resto.
# ============================================================
UNIVERSITIES_META: dict[str, dict] = {
    "uai":    {"short_name": "UAI",   "name": "Universidad Adolfo Ibáñez",                       "tier": 1},
    "uandes": {"short_name": "UANDES","name": "Universidad de los Andes",                        "tier": 1},
    "uch":    {"short_name": "UCH",   "name": "Universidad de Chile",                            "tier": 1},
    "udd":    {"short_name": "UDD",   "name": "Universidad del Desarrollo",                      "tier": 2},
    "utfsm":  {"short_name": "UTFSM", "name": "Universidad Técnica Federico Santa María",        "tier": 2},
    "pucv":   {"short_name": "PUCV",  "name": "Pontificia Universidad Católica de Valparaíso",   "tier": 3},
    "udec":   {"short_name": "UDEC",  "name": "Universidad de Concepción",                       "tier": 3},
    "udp":    {"short_name": "UDP",   "name": "Universidad Diego Portales",                      "tier": 3},
    "usach":  {"short_name": "USACH", "name": "Universidad de Santiago",                         "tier": 3},
    "unab":   {"short_name": "UNAB",  "name": "Universidad Andrés Bello",                        "tier": 4},
    "uss":    {"short_name": "USS",   "name": "Universidad San Sebastián",                       "tier": 4},
    "umay":   {"short_name": "UMAY",  "name": "Universidad Mayor",                               "tier": 4},
}


# ============================================================
# Utilidades
# ============================================================
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(text: str) -> str:
    """Convierte un texto en slug estable (sin acentos, lowercase, guiones)."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_jsx(path: Path) -> dict:
    """Llama al parser Node y devuelve el dict {sigla, base_courses, carreras}."""
    proc = subprocess.run(
        ["node", str(NODE_PARSER), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"parser Node falló en {path.name}: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


# ============================================================
# DB helpers
# ============================================================
async def upsert_university(db, sigla: str, meta: dict) -> tuple[str, bool]:
    """Crea la universidad si no existe. Si existe, sólo backfill de tier
    cuando está vacío. No toca logo, nombre, is_active."""
    short = meta["short_name"]
    existing = await db.library_universities.find_one({"short_name": short}, {"_id": 0})
    if existing:
        if existing.get("tier") is None:
            await db.library_universities.update_one(
                {"id": existing["id"]}, {"$set": {"tier": meta["tier"]}}
            )
        return existing["id"], False
    doc = {
        "id": str(uuid.uuid4()),
        "name": meta["name"],
        "short_name": short,
        "tier": meta["tier"],
        "is_active": True,
        "created_at": now_iso(),
    }
    await db.library_universities.insert_one(doc)
    return doc["id"], True


async def find_existing_course(db, slug: str) -> dict | None:
    """Busca por id o por alt_slugs (cualquiera de los slugs alternativos
    registrados por el seed previo cuenta como existente)."""
    return await db.courses.find_one(
        {"$or": [{"id": slug}, {"alt_slugs": slug}]},
        {"_id": 0, "id": 1, "title": 1, "alt_slugs": 1},
    )


async def get_base_chapter_ids(db, base_course_id: str) -> list[str]:
    """Chapters template (sin template_chapter_id) del curso base, en orden."""
    rows = await db.chapters.find(
        {"course_id": base_course_id},
        {"_id": 0, "id": 1, "order": 1, "template_chapter_id": 1},
    ).sort("order", 1).to_list(200)
    return [r["id"] for r in rows if not r.get("template_chapter_id")]


async def link_chapters_to_course(db, course_id: str, template_chapter_ids: list[str]) -> int:
    """Crea chapters linkeados (template_chapter_id) en el curso destino.
    Idempotente: skipea si ya existe link al mismo template."""
    if not template_chapter_ids:
        return 0
    last = await db.chapters.find_one(
        {"course_id": course_id}, {"order": 1}, sort=[("order", -1)]
    )
    next_order = (last.get("order", 0) if last else 0) + 1
    created = 0
    for tch_id in template_chapter_ids:
        already = await db.chapters.find_one(
            {"course_id": course_id, "template_chapter_id": tch_id}, {"_id": 0, "id": 1}
        )
        if already:
            continue
        template = await db.chapters.find_one({"id": tch_id}, {"_id": 0})
        if not template:
            continue
        await db.chapters.insert_one({
            "id": str(uuid.uuid4()),
            "course_id": course_id,
            "title": template.get("title", ""),
            "description": template.get("description", ""),
            "order": next_order,
            "template_chapter_id": tch_id,
            "excluded_lesson_ids": [],
            "excluded_question_ids": [],
            "created_at": now_iso(),
        })
        created += 1
        next_order += 1
    return created


async def insert_course_axes(db, course_id: str, axes: list[str]):
    """Inserta los ejes textuales. Sólo se llama cuando el curso es nuevo."""
    if not axes:
        return
    await db.course_axes.delete_many({"course_id": course_id})  # safety
    docs = [
        {
            "id": str(uuid.uuid4()),
            "course_id": course_id,
            "order": i + 1,
            "text": ax,
            "created_at": now_iso(),
        }
        for i, ax in enumerate(axes)
    ]
    await db.course_axes.insert_many(docs)


# ============================================================
# Lógica principal
# ============================================================
def build_course_slug(sigla: str, carrera_id: str, ramo_nombre: str) -> str:
    """Slug canónico del curso universitario: {sigla}-{carrera_id}-{slug(ramo)}.
    Sigla en minúscula, carrera_id ya viene en kebab-case del .jsx, ramo se
    slugifica."""
    return f"{sigla.lower()}-{carrera_id}-{slugify(ramo_nombre)}"


def filter_known_bases(match_slugs: list[str], known_bases_in_db: set[str]) -> tuple[list[str], list[str]]:
    """Resuelve los match[] del .jsx via aliases, separa los slugs conocidos
    (existen en Remy como cursos base) vs huérfanos (no existen y no son
    aliases). Devuelve (resolved_known, dropped_orphans)."""
    resolved = resolve_base_slugs(match_slugs)
    known = [s for s in resolved if s in known_bases_in_db]
    orphans = [s for s in resolved if s not in known_bases_in_db]
    return known, orphans


async def process_ramo(
    db,
    sigla: str,
    carrera: dict,
    ramo: dict,
    university_id: str,
    known_bases: set[str],
    stats: dict,
):
    """Procesa un ramo del .jsx. Devuelve True si se creó algo, False si skip."""
    match_level = (ramo.get("matchLevel") or "").lower()
    if match_level not in ("alto", "medio"):
        stats["skipped_match_level"] += 1
        return False

    nombre = ramo.get("nombre")
    if not nombre:
        stats["skipped_no_name"] += 1
        return False

    carrera_id = carrera.get("id")
    if not carrera_id:
        stats["skipped_no_carrera_id"] += 1
        return False

    slug = build_course_slug(sigla, carrera_id, nombre)

    # ¿Ya existe en DB? (por id o por alt_slugs del seed previo)
    existing = await find_existing_course(db, slug)
    if existing:
        # Backfill conservador: si el curso existe pero su id no es exactamente
        # el slug que generamos (caso fusionado donde el slug nuevo está en
        # alt_slugs), no hacemos nada. Si es exactamente el mismo id, tampoco.
        stats["skipped_existing"] += 1
        return False

    # Resolver match[] → bases reales
    match_raw = ramo.get("match") or []
    known_bases_for_ramo, dropped = filter_known_bases(match_raw, known_bases)

    if not known_bases_for_ramo:
        # Ningún slug del match[] resolvió a un curso base existente.
        # Pasa el ramo silencioso — no creamos cursos huérfanos.
        stats["skipped_no_base"] += 1
        stats["skipped_no_base_examples"].append({
            "slug": slug, "match": match_raw, "dropped": dropped,
        })
        return False

    contenidos = ramo.get("contenidos") or []
    semestre = ramo.get("semestre")
    prereqs_text = ramo.get("prereqs")
    fuente = ramo.get("fuenteContenido") or ramo.get("nota")
    split_desde = ramo.get("splitDesde")

    coverage = "complete" if match_level == "alto" else "partial"

    carrera_nombre = (carrera.get("nombre") or "").strip()
    if carrera_nombre:
        title = f"{nombre} ({sigla} — {carrera_nombre})"
    else:
        title = f"{nombre} ({sigla})"

    course_doc = {
        "id": slug,
        "title": title,
        "description": nombre,
        "category": "Matemáticas",
        "level": "Universitario",
        "modules_count": 0,
        "university_id": university_id,
        "rating": 4.8,
        "summary": split_desde or nombre,
        # Campos del modelo extendido (ya en server.py desde commit previo)
        "code": ramo.get("codigo"),
        "semester": semestre if isinstance(semestre, int) else None,
        # prereqs como texto libre va a notes; el array prereq_course_ids
        # queda vacío porque el .jsx no entrega IDs de otros cursos derivados,
        # sólo nombres.
        "prereq_course_ids": [],
        "base_course_ids": known_bases_for_ramo,
        "match_level": match_level,
        "source": "split",
        "coverage_status": coverage,
        "notes": _compose_notes(prereqs_text, fuente, split_desde, dropped),
        "alt_slugs": [],
        "visible_to_students": True,
        "created_at": now_iso(),
    }
    await db.courses.insert_one(course_doc)

    # Linkear chapters de cada base
    linked = 0
    for base in known_bases_for_ramo:
        chapter_ids = await get_base_chapter_ids(db, base)
        linked += await link_chapters_to_course(db, slug, chapter_ids)

    # Axes
    await insert_course_axes(db, slug, contenidos)

    stats["created"] += 1
    stats["created_by_level"][match_level] += 1
    stats["linked_chapters"] += linked
    stats["axes"] += len(contenidos)
    return True


def _compose_notes(prereqs_text, fuente, split_desde, dropped) -> str | None:
    parts = []
    if prereqs_text:
        parts.append(f"Prereqs en la malla: {prereqs_text}")
    if fuente:
        parts.append(f"Fuente: {fuente}")
    if split_desde:
        parts.append(f"Split: {split_desde}")
    if dropped:
        parts.append(f"Slugs match[] descartados (no son cursos base en Remy): {', '.join(dropped)}")
    return " · ".join(parts) if parts else None


async def main():
    target = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]
    print(f"→ Target: {target[:50]}{'...' if len(target)>50 else ''}")
    print(f"→ DB:     {db_name}")

    client = AsyncIOMotorClient(target)
    db = client[db_name]

    # Identificar los cursos base que SÍ existen en Remy (para filtrar match[]).
    bases_known = set()
    async for c in db.courses.find(
        {"$or": [{"university_id": None}, {"university_id": {"$exists": False}}]},
        {"_id": 0, "id": 1},
    ):
        bases_known.add(c["id"])
    print(f"→ Cursos base conocidos en DB: {sorted(bases_known)}")

    # Universidades
    print("\n== Universidades ==")
    sigla_to_uid: dict[str, str] = {}
    for key in sorted(UNIVERSITIES_META.keys()):
        meta = UNIVERSITIES_META[key]
        uid, created = await upsert_university(db, key, meta)
        marker = "+" if created else "="
        sigla_to_uid[meta["short_name"]] = uid
        print(f"  {marker} {meta['short_name']:7s} tier={meta['tier']} → {uid}")

    # Iterar .jsx
    files = sorted(p for p in JSX_DIR.glob("*.jsx") if not p.name.startswith("_"))
    print(f"\n== Archivos .jsx ({len(files)}) ==")

    total_stats = {
        "created": 0,
        "created_by_level": {"alto": 0, "medio": 0},
        "skipped_match_level": 0,
        "skipped_no_name": 0,
        "skipped_no_carrera_id": 0,
        "skipped_existing": 0,
        "skipped_no_base": 0,
        "skipped_no_base_examples": [],
        "linked_chapters": 0,
        "axes": 0,
    }
    by_uni: dict[str, dict] = {}

    for fp in files:
        key = fp.stem
        if key not in UNIVERSITIES_META:
            print(f"  ! {fp.name}: sin metadata en UNIVERSITIES_META, skip")
            continue
        meta = UNIVERSITIES_META[key]
        sigla = meta["short_name"]
        uid = sigla_to_uid[sigla]
        print(f"\n— {fp.name} ({sigla})")
        try:
            parsed = parse_jsx(fp)
        except Exception as e:
            print(f"  ✗ ERROR parseando: {e}")
            continue

        carreras = parsed.get("carreras") or []
        local_stats = {
            "created": 0, "alto": 0, "medio": 0,
            "skipped_existing": 0, "skipped_no_base": 0, "skipped_level": 0,
            "linked": 0, "axes": 0,
        }
        for carrera in carreras:
            for ramo in carrera.get("ramos") or []:
                # Stats locales precisas:
                pre_created = total_stats["created"]
                pre_no_base = total_stats["skipped_no_base"]
                pre_existing = total_stats["skipped_existing"]
                pre_level = total_stats["skipped_match_level"]
                pre_linked = total_stats["linked_chapters"]
                pre_axes = total_stats["axes"]
                await process_ramo(db, sigla, carrera, ramo, uid, bases_known, total_stats)
                if total_stats["created"] > pre_created:
                    local_stats["created"] += 1
                    lvl = (ramo.get("matchLevel") or "").lower()
                    if lvl in local_stats:
                        local_stats[lvl] += 1
                    local_stats["linked"] += total_stats["linked_chapters"] - pre_linked
                    local_stats["axes"] += total_stats["axes"] - pre_axes
                elif total_stats["skipped_existing"] > pre_existing:
                    local_stats["skipped_existing"] += 1
                elif total_stats["skipped_no_base"] > pre_no_base:
                    local_stats["skipped_no_base"] += 1
                elif total_stats["skipped_match_level"] > pre_level:
                    local_stats["skipped_level"] += 1
        by_uni[sigla] = local_stats
        print(
            f"  created={local_stats['created']:3d} (alto={local_stats['alto']:3d} medio={local_stats['medio']:3d})  "
            f"skipped: existing={local_stats['skipped_existing']:3d} sin_base={local_stats['skipped_no_base']:3d} "
            f"low_level={local_stats['skipped_level']:3d}  +{local_stats['linked']} ch  {local_stats['axes']} ejes"
        )

    # Reporte global
    print("\n== Resumen global ==")
    print(f"  Cursos creados:               {total_stats['created']}")
    print(f"    match=alto:                 {total_stats['created_by_level']['alto']}")
    print(f"    match=medio:                {total_stats['created_by_level']['medio']}")
    print(f"  Skipped por curso existente:  {total_stats['skipped_existing']}")
    print(f"  Skipped por sin base:         {total_stats['skipped_no_base']}")
    print(f"  Skipped por match bajo/none:  {total_stats['skipped_match_level']}")
    print(f"  Skipped por datos faltantes:  {total_stats['skipped_no_name'] + total_stats['skipped_no_carrera_id']}")
    print(f"  Chapter links creados:        {total_stats['linked_chapters']}")
    print(f"  Ejes insertados:              {total_stats['axes']}")

    if total_stats["skipped_no_base"]:
        print("\n  Primeros 5 ramos descartados por no tener base reconocida:")
        for ex in total_stats["skipped_no_base_examples"][:5]:
            print(f"    - {ex['slug']!s}  match={ex['match']}  dropped={ex['dropped']}")

    # Estado DB final
    courses_total = await db.courses.count_documents({})
    courses_uni = await db.courses.count_documents({"university_id": {"$ne": None}})
    courses_gen = await db.courses.count_documents(
        {"$or": [{"university_id": None}, {"university_id": {"$exists": False}}]}
    )
    axes_total = await db.course_axes.count_documents({})
    unis_total = await db.library_universities.count_documents({})
    print(f"\n  DB estado:  courses_total={courses_total} (uni={courses_uni}, gen={courses_gen}) "
          f"unis={unis_total} axes={axes_total}")

    client.close()
    print("\nOK: seed completado.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
