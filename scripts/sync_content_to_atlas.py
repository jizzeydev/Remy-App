"""Sync content collections from local MongoDB -> Atlas, preserving user data.

This is the selective sibling of `migrate_to_atlas.py`. Use it as the recurring
deploy step when you author/edit courses against local Mongo and want the new
content live on prod without touching real users, attempts, subscriptions, etc.

Usage:
    # dry-run (default): print what would happen, no writes
    python scripts/sync_content_to_atlas.py

    # actually push (drops + reinserts the CONTENT collections in Atlas)
    python scripts/sync_content_to_atlas.py --confirm

    # override the URI on the fly (env var takes precedence; arg overrides if you want)
    python scripts/sync_content_to_atlas.py "mongodb+srv://..." --confirm

Reads source from MONGO_URL/DB_NAME and target from ATLAS_URL in backend/.env.
ATLAS_URL must be set (or the URI passed as the first arg).

Each CONTENT collection in Atlas is dropped and replaced with the local copy.
USER collections are never read or written.
"""
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


# Collections that hold authored/admin-managed content — safe to overwrite.
CONTENT_COLLECTIONS = [
    "courses",
    "chapters",
    "lessons",
    "questions",
    "library_universities",
    "formulas",
    "pricing_config",
    "app_settings",
]

# Collections that hold per-user state — must NEVER be touched by this script.
PRESERVE_COLLECTIONS = [
    "users",
    "user_sessions",
    "user_achievements",
    "student_enrollments",
    "quiz_attempts",
    "lesson_progress",
    "subscriptions",
    "payments",
    "trash",
]


async def main():
    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")

    args = sys.argv[1:]
    confirm = "--confirm" in args
    args = [a for a in args if a != "--confirm"]

    # Si pasaste un URI como argumento, ese gana. Si no, usar ATLAS_URL del env.
    if args:
        atlas_uri = args[0]
    else:
        atlas_uri = os.environ.get("ATLAS_URL", "").strip()
        if not atlas_uri:
            print("ERROR: no encontré la URI de Atlas.")
            print()
            print("Opciones:")
            print('  1. Agregá ATLAS_URL=mongodb+srv://... a backend/.env (recomendado)')
            print('  2. Pasala como argumento: python scripts/sync_content_to_atlas.py "<URI>" [--confirm]')
            sys.exit(1)

    src_url = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]

    src = AsyncIOMotorClient(src_url)[db_name]
    dst = AsyncIOMotorClient(atlas_uri)[db_name]

    print(f"Source:  {src_url} / {db_name}")
    print(f"Target:  Atlas / {db_name}")
    print(f"Mode:    {'WRITE (--confirm)' if confirm else 'DRY-RUN (no --confirm flag)'}")
    print()

    src_cols = set(await src.list_collection_names())
    dst_cols = set(await dst.list_collection_names())

    # Sanity: warn if local has a collection we don't know how to classify.
    known = set(CONTENT_COLLECTIONS) | set(PRESERVE_COLLECTIONS)
    unclassified = [c for c in src_cols if c not in known and not c.startswith("system.")]
    if unclassified:
        print("WARNING: local has collections this script doesn't classify:")
        for c in unclassified:
            n = await src[c].count_documents({})
            print(f"  - {c} ({n} docs) — NOT synced. Add to CONTENT_COLLECTIONS or PRESERVE_COLLECTIONS in this script if it should be.")
        print()

    print("=== CONTENT (will be replaced in Atlas) ===")
    plan = []
    for c in CONTENT_COLLECTIONS:
        if c not in src_cols:
            print(f"  {c:35s} (not in local — will leave Atlas untouched)")
            continue
        n_src = await src[c].count_documents({})
        n_dst = await dst[c].count_documents({}) if c in dst_cols else 0
        print(f"  {c:35s} local={n_src:>6}   atlas={n_dst:>6}  ->  atlas will become {n_src}")
        plan.append((c, n_src))

    print()
    print("=== PRESERVED (never touched) ===")
    for c in PRESERVE_COLLECTIONS:
        n_dst = await dst[c].count_documents({}) if c in dst_cols else 0
        print(f"  {c:35s} atlas={n_dst:>6}  (untouched)")

    if not confirm:
        print()
        print("Dry-run only. Re-run with --confirm to apply.")
        return

    print()
    print("=== APPLYING ===")
    total = 0
    mismatches: list[str] = []
    for c, n_src in plan:
        await dst[c].drop()
        if n_src == 0:
            print(f"  {c:35s} 0 docs (dropped only)")
            continue
        docs = await src[c].find({}).to_list(length=None)
        await dst[c].insert_many(docs)
        copied = await dst[c].count_documents({})
        total += copied
        if copied == n_src:
            flag = "OK"
        else:
            flag = f"MISMATCH src={n_src} dst={copied}"
            mismatches.append(c)
        print(f"  {c:35s} {copied:>6} docs  [{flag}]")

    print()
    print(f"DONE. {total} content docs synced. User collections untouched.")
    if mismatches:
        print(f"⚠️  Conteos no coinciden en: {', '.join(mismatches)}. "
              "Reintentá el sync o revisá la red.")

    # Smoke test contra la API pública: si responde con la cantidad esperada de
    # cursos visibles, el deploy está sirviendo lo nuevo. No fallar duro si la
    # request falla (firewall, prod en redeploy, etc.) — solo avisar.
    print()
    print("=== Smoke test API pública ===")
    try:
        import urllib.error
        import urllib.request
        req = urllib.request.Request(
            "https://api.remy.seremonta.store/api/courses",
            headers={"User-Agent": "remy-sync-script"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            import json
            payload = json.loads(resp.read().decode("utf-8"))
            n_visible = len(payload) if isinstance(payload, list) else 0
            print(f"  GET /api/courses → {resp.status}, {n_visible} cursos visibles.")
            if "courses" in [c for c, _ in plan]:
                n_local_visible = await src.courses.count_documents(
                    {"visible_to_students": {"$ne": False}}
                )
                if n_visible != n_local_visible:
                    print(f"  ⚠️  prod expone {n_visible} pero local tiene {n_local_visible} "
                          "visibles. Puede ser cache / redeploy en curso — chequeá en 1 min.")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"  No pude verificar la API ({e}). Chequeá manualmente:")
        print("    https://remy.seremonta.store")
        print("    https://api.remy.seremonta.store/api/courses")

    print()
    print("URLs:")
    print("  https://remy.seremonta.store")
    print("  https://api.remy.seremonta.store")


if __name__ == "__main__":
    asyncio.run(main())
