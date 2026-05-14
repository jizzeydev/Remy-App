"""Consolida cursos universitarios duplicados creados por el seed_splits_from_jsx.

Detecta clusters por (universidad, nombre_ramo_normalizado, mismas bases, mismo
semestre, mismo código si lo hay) y los fusiona dejando un slug canónico.

Política de canónico:
  1. Slug que contenga "plan-comun" gana.
  2. Si no, "lic-matematica" gana.
  3. Si no, "lic-fisica" gana.
  4. Si no, primer slug alfabético del cluster.

Operación de fusión:
  - Append `<otros_slugs>` al `alt_slugs[]` del canónico.
  - Borrar los documentos no-canónicos de `courses`.
  - Borrar los chapters linkeados de los no-canónicos (`chapters` con
    course_id = slug no-canónico).
  - Borrar los course_axes de los no-canónicos.

PUC se SKIPEA completo (los 3 grupos detectados son programas formalmente
distintos pese a compartir título: MAT1203 vs MAT1279, MAT1610 vs MAT1100,
MAT1620 vs MAT1220 son productos separados en seremonta.store).

REVIEW de casos donde el código USACH es distinto (10113 vs 10108, etc.):
SKIPEADOS — son ramos USACH formalmente distintos.

REVIEW de casos donde un subgrupo del cluster tiene bases idénticas + código
idéntico: SE FUSIONAN. El resto del cluster queda sin tocar.

Usage:
    backend/venv/Scripts/python.exe scripts/consolidate_duplicates.py [--dry-run] [--target-atlas]
"""
from __future__ import annotations

import asyncio
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
load_dotenv(BACKEND_DIR / ".env")


def slug_norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def ramo_name_from_title(title: str) -> str:
    if not title:
        return ""
    m = re.match(r"(.*?)\s*\(", title)
    return slug_norm(m.group(1) if m else title)


def pick_canonical(members: list[dict]) -> dict:
    """Elige el slug canónico según política."""
    def score(m: dict) -> tuple:
        slug = m["id"]
        is_plan_comun = 0 if "plan-comun" in slug else 1
        is_lic_mat = 0 if "lic-matematica" in slug else 1
        is_lic_fis = 0 if "lic-fisica" in slug else 1
        return (is_plan_comun, is_lic_mat, is_lic_fis, slug)
    return sorted(members, key=score)[0]


async def detect_clusters(db) -> tuple[list[list[dict]], list[list[dict]]]:
    """Devuelve (safe_clusters, skipped_clusters).

    `safe_clusters`: list of clusters that can be merged.
    `skipped_clusters`: clusters detected but NOT merged (PUC, USACH códigos
    distintos, programa formalmente distinto).
    """
    courses = await db.courses.find(
        {"university_id": {"$ne": None}},
        {"_id": 0},
    ).to_list(500)
    unis = await db.library_universities.find({}, {"_id": 0, "id": 1, "short_name": 1}).to_list(50)
    uid2sigla = {u["id"]: u["short_name"] for u in unis}

    # Sub-cluster por (sigla, nombre_ramo, bases_signature, semestre, código).
    sub_clusters: dict[tuple, list[dict]] = defaultdict(list)
    for c in courses:
        sigla = uid2sigla.get(c["university_id"], "?")
        rname = ramo_name_from_title(c.get("title", ""))
        bases_sig = ",".join(sorted(c.get("base_course_ids") or []))
        sem = c.get("semester")
        code = (c.get("code") or "").strip().upper()
        sub_clusters[(sigla, rname, bases_sig, sem, code)].append(c)

    safe: list[list[dict]] = []
    skipped: list[list[dict]] = []
    for key, members in sub_clusters.items():
        if len(members) < 2:
            continue
        # Filtrar cluster donde un canónico ya absorbe a otros vía alt_slugs.
        abs_set = set()
        for m in members:
            for a in m.get("alt_slugs") or []:
                abs_set.add(a)
        rem = [m for m in members if m["id"] not in abs_set]
        if len(rem) < 2:
            continue
        sigla = key[0]
        # SKIP PUC: programas formalmente distintos a pesar de mismo nombre/bases.
        if sigla == "PUC":
            skipped.append(rem)
            continue
        safe.append(rem)

    return safe, skipped


async def apply_merge(db, cluster: list[dict], dry_run: bool) -> dict:
    """Fusiona un cluster. Devuelve dict con stats."""
    canonical = pick_canonical(cluster)
    others = [m for m in cluster if m["id"] != canonical["id"]]

    other_ids = [m["id"] for m in others]
    existing_alts = list(canonical.get("alt_slugs") or [])
    new_alts = list(dict.fromkeys(existing_alts + other_ids))  # preserve order, dedup

    stats = {
        "canonical": canonical["id"],
        "absorbed": other_ids,
        "axes_deleted": 0,
        "chapters_deleted": 0,
    }

    if dry_run:
        return stats

    # 1. Append alt_slugs al canónico.
    await db.courses.update_one(
        {"id": canonical["id"]},
        {"$set": {"alt_slugs": new_alts}},
    )

    # 2. Borrar axes de los absorbidos.
    if other_ids:
        r = await db.course_axes.delete_many({"course_id": {"$in": other_ids}})
        stats["axes_deleted"] = r.deleted_count
        # 3. Borrar chapters linkeados de los absorbidos. Los chapters tienen
        #    course_id = curso universitario absorbido y template_chapter_id que
        #    apunta al base. Como el canónico ya tiene linkeados los mismos
        #    templates, borrarlos no rompe nada.
        r = await db.chapters.delete_many({"course_id": {"$in": other_ids}})
        stats["chapters_deleted"] = r.deleted_count
        # 4. Borrar los docs de course.
        await db.courses.delete_many({"id": {"$in": other_ids}})

    return stats


async def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    target_atlas = "--target-atlas" in args

    if target_atlas:
        os.environ["MONGO_URL"] = os.environ["ATLAS_URL"]
        target_label = "ATLAS (prod)"
    else:
        target_label = f"local ({os.environ['MONGO_URL']})"

    print(f"== Consolidación de cursos duplicados ==")
    print(f"   Target: {target_label}")
    print(f"   Mode:   {'DRY RUN' if dry_run else 'APPLY'}")
    print()

    c = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = c[os.environ["DB_NAME"]]

    safe, skipped = await detect_clusters(db)
    print(f"Detectados:")
    print(f"  SAFE clusters: {len(safe)} ({sum(len(c)-1 for c in safe)} cursos a absorber)")
    print(f"  SKIP (PUC):    {len(skipped)} ({sum(len(c)-1 for c in skipped)} cursos preservados)")
    print()

    total_axes = 0
    total_chapters = 0
    total_absorbed = 0
    rows = []
    for cluster in safe:
        s = await apply_merge(db, cluster, dry_run)
        rows.append(s)
        total_axes += s["axes_deleted"]
        total_chapters += s["chapters_deleted"]
        total_absorbed += len(s["absorbed"])

    # Group rows by canonical sigla for readability
    print("== FUSIONES ==")
    for s in rows:
        n = len(s["absorbed"])
        marker = "+" if not dry_run else "?"
        print(f"  {marker} {s['canonical']:80s}  absorbe {n}  (-{s['axes_deleted']} ejes, -{s['chapters_deleted']} ch links)")
        for a in s["absorbed"]:
            print(f"      ← {a}")

    print()
    print(f"== Resumen ==")
    print(f"  Clusters fusionados: {len(safe)}")
    print(f"  Cursos absorbidos:   {total_absorbed}")
    print(f"  Axes removidos:      {total_axes}")
    print(f"  Chapter links removidos: {total_chapters}")

    if skipped:
        print()
        print(f"== SKIPPED (preservados) ==")
        for cluster in skipped:
            for m in cluster:
                print(f"  - {m['id']:50s}  {m.get('title','')[:60]}")

    # Estado post
    courses_uni = await db.courses.count_documents({"university_id": {"$ne": None}})
    axes_total = await db.course_axes.count_documents({})
    chapters_linked = await db.chapters.count_documents({"template_chapter_id": {"$ne": None}})
    print()
    print(f"  DB tras consolidación: courses_uni={courses_uni} axes={axes_total} chapters_linked={chapters_linked}")

    c.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
