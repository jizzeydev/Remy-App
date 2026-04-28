"""Migrate local MongoDB -> MongoDB Atlas.

Usage:
    python scripts/migrate_to_atlas.py "mongodb+srv://USER:PASS@CLUSTER.mongodb.net/?retryWrites=true&w=majority"

Reads from MONGO_URL/DB_NAME in backend/.env (local source)
and writes to the Atlas URI passed as the first argument.

Safe to re-run: drops each target collection before re-inserting.
"""
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


async def main():
    if len(sys.argv) < 2:
        print("ERROR: pass the Atlas URI as first argument.")
        print('Example: python scripts/migrate_to_atlas.py "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority"')
        sys.exit(1)

    atlas_uri = sys.argv[1]

    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")
    src_url = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]

    print(f"Source:  {src_url} / {db_name}")
    print(f"Target:  Atlas / {db_name}")
    print()

    src = AsyncIOMotorClient(src_url)[db_name]
    dst = AsyncIOMotorClient(atlas_uri)[db_name]

    cols = await src.list_collection_names()
    cols = [c for c in cols if not c.startswith("system.")]

    total_docs = 0
    for c in sorted(cols):
        n = await src[c].count_documents({})
        if n == 0:
            print(f"  {c:35s} 0 docs (skipped)")
            continue

        await dst[c].drop()
        docs = await src[c].find({}).to_list(length=None)
        if docs:
            await dst[c].insert_many(docs)

        copied = await dst[c].count_documents({})
        total_docs += copied
        flag = "OK" if copied == n else f"MISMATCH src={n} dst={copied}"
        print(f"  {c:35s} {copied:6d} docs  [{flag}]")

    print()
    print(f"TOTAL: {total_docs} docs across {len(cols)} collections")
    print("Migration complete.")


if __name__ == "__main__":
    asyncio.run(main())
