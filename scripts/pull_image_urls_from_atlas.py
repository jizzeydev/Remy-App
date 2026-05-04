"""Trae los `image_url` cargados en Atlas hacia Mongo local — paso previo al sync.

Por qué existe:
  `sync_content_to_atlas.py --confirm` hace DROP + reinsert de la colección
  `lessons` entera en Atlas, sobreescribiendo cualquier `image_url` que se haya
  cargado vía /admin de producción.

  Para preservarlos, este script lee Atlas y, para cada bloque type='figura'
  con `image_url` no vacío, copia ese URL al bloque correspondiente (mismo
  lesson.id + block.id) en Mongo local.

  Workflow recomendado antes de cada sync nuevo:
    1. python scripts/pull_image_urls_from_atlas.py            # dry-run
    2. python scripts/pull_image_urls_from_atlas.py --confirm  # aplica
    3. python scripts/run_seed.py <nuevo seed>                 # editás solo el nuevo
    4. python scripts/sync_content_to_atlas.py --confirm       # push completo

Uso:
    python scripts/pull_image_urls_from_atlas.py             # dry-run, lista cambios
    python scripts/pull_image_urls_from_atlas.py --confirm   # aplica a Mongo local
"""
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


async def main():
    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")
    confirm = "--confirm" in sys.argv[1:]
    atlas_uri = os.environ.get("ATLAS_URL", "").strip()
    if not atlas_uri:
        print("ERROR: ATLAS_URL no definido en backend/.env"); sys.exit(1)
    local_url = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]

    src = AsyncIOMotorClient(atlas_uri)[db_name]   # Atlas (fuente de imágenes cargadas)
    dst = AsyncIOMotorClient(local_url)[db_name]   # Mongo local (destino)

    print(f"Source : Atlas / {db_name}")
    print(f"Target : {local_url} / {db_name}")
    print(f"Mode   : {'WRITE (--confirm)' if confirm else 'DRY-RUN'}")
    print()

    # Indexar lessons locales por id para lookup rápido.
    local_lessons = {l["id"]: l async for l in dst.lessons.find({})}
    print(f"Lecciones en local: {len(local_lessons)}")

    updated = 0
    set_count = 0
    no_match_lesson = 0
    no_match_block = 0
    already_filled_local = 0

    async for atlas_lesson in src.lessons.find({}):
        lid = atlas_lesson.get("id")
        atlas_blocks = atlas_lesson.get("blocks", [])
        # URLs cargadas en Atlas para esta lección, indexadas por block.id
        atlas_urls = {
            blk.get("id"): blk.get("image_url", "")
            for blk in atlas_blocks
            if blk.get("type") == "figura" and (blk.get("image_url") or "").strip()
        }
        if not atlas_urls:
            continue

        local = local_lessons.get(lid)
        if not local:
            no_match_lesson += 1
            print(f"  - lesson {lid}: existe en Atlas con {len(atlas_urls)} imágenes pero NO en local")
            continue

        local_blocks = list(local.get("blocks", []))
        changed_in_lesson = 0
        for blk in local_blocks:
            if blk.get("type") != "figura":
                continue
            bid = blk.get("id")
            if bid not in atlas_urls:
                continue
            new_url = atlas_urls[bid]
            cur_url = (blk.get("image_url") or "").strip()
            if cur_url == new_url:
                continue
            if cur_url:
                already_filled_local += 1
                # local ya tiene una URL distinta (admin local también editó). No la pisamos.
                print(f"  ~ lesson {lid} block {bid}: local YA tiene URL distinta — preservo local")
                continue
            blk["image_url"] = new_url
            changed_in_lesson += 1
            set_count += 1

        # Bloques en Atlas con URL pero sin match en local (block.id distinto):
        for bid in atlas_urls:
            if not any(b.get("id") == bid for b in local_blocks):
                no_match_block += 1
                print(f"  - lesson {lid} block {bid}: en Atlas pero NO en local (probablemente cambió el seed)")

        if changed_in_lesson:
            updated += 1
            print(f"  + lesson {lid}: {changed_in_lesson} image_url copiadas Atlas→local")
            if confirm:
                await dst.lessons.update_one({"id": lid}, {"$set": {"blocks": local_blocks}})

    print()
    print("=== Resumen ===")
    print(f"  lecciones actualizadas       : {updated}")
    print(f"  image_url copiadas a local   : {set_count}")
    print(f"  lecciones en Atlas sin local : {no_match_lesson}")
    print(f"  bloques en Atlas sin local   : {no_match_block}")
    print(f"  conflictos (local ya tenía)  : {already_filled_local}")
    if not confirm:
        print()
        print("Dry-run. Re-ejecutá con --confirm para aplicar.")
    else:
        print()
        print("Listo. Ahora podés correr sync_content_to_atlas.py --confirm sin perder imágenes.")


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    asyncio.run(main())
