"""Sync content collections from local MongoDB -> Atlas, preserving user data.

This is the selective sibling of `migrate_to_atlas.py`. Use it as the recurring
deploy step when you author/edit courses against local Mongo and want the new
content live on prod without touching real users, attempts, subscriptions, etc.

Usage:
    # dry-run (default): print what would happen, no writes
    python scripts/sync_content_to_atlas.py "mongodb+srv://USER:PASS@CLUSTER.mongodb.net/?..."

    # actually push (drops + reinserts the CONTENT collections in Atlas)
    python scripts/sync_content_to_atlas.py "mongodb+srv://USER:PASS@CLUSTER.mongodb.net/?..." --confirm

Reads source from MONGO_URL/DB_NAME in backend/.env.

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
    if len(sys.argv) < 2:
        print("ERROR: pass the Atlas URI as first argument.")
        print('Example: python scripts/sync_content_to_atlas.py "mongodb+srv://..." [--confirm]')
        sys.exit(1)

    atlas_uri = sys.argv[1]
    confirm = "--confirm" in sys.argv[2:]

    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")
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
    for c, n_src in plan:
        await dst[c].drop()
        if n_src == 0:
            print(f"  {c:35s} 0 docs (dropped only)")
            continue
        docs = await src[c].find({}).to_list(length=None)
        await dst[c].insert_many(docs)
        copied = await dst[c].count_documents({})
        total += copied
        flag = "OK" if copied == n_src else f"MISMATCH src={n_src} dst={copied}"
        print(f"  {c:35s} {copied:>6} docs  [{flag}]")

    print()
    print(f"DONE. {total} content docs synced. User collections untouched.")


if __name__ == "__main__":
    asyncio.run(main())
