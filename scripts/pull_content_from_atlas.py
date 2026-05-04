"""Trae el contenido editable Atlas → Mongo local — paso previo al sync.

Por qué existe:
  `sync_content_to_atlas.py --confirm` hace DROP + reinsert sobre las
  colecciones de contenido en Atlas. Si vos edités algo desde /admin de prod
  (Desmos, image_url, body_md, una pregunta, una descripción de capítulo,
  etc.) y después corrés sync sin "chupar" antes esas ediciones a local,
  las perdés todas.

  Este script es el inverso de `sync_content_to_atlas.py`: por cada
  colección de contenido, mirror Atlas → local upsertando por `id`.

Modelo conceptual:
  - SEED = autoridad sobre QUÉ documentos existen (estructura: agregar/quitar
    cursos, capítulos, lecciones, bloques nuevos en una lección).
  - ATLAS = autoridad sobre el CONTENIDO de cada documento existente
    (texto, image_url, expresiones de Desmos, opciones de pregunta, etc.).

  Después de correr este script:
  - Docs que existen en Atlas: el local queda con la copia exacta de Atlas.
  - Docs que existen solo en local (nuevos seeds aún no sync-eados):
    se preservan tal cual — el próximo sync los empuja a Atlas.
  - Docs que existen solo en Atlas (creados desde admin sin pasar por seed):
    se mantienen — los upserteamos en local.

Uso:
    python scripts/pull_content_from_atlas.py             # dry-run, lista cambios
    python scripts/pull_content_from_atlas.py --confirm   # aplica a Mongo local

Workflow seguro de deploy de un nuevo curso/capítulo:
    1. python scripts/pull_content_from_atlas.py --confirm
    2. python scripts/run_seed.py "backend/seeds/<curso>/seed_capitulo_*.py"
    3. python scripts/audit_lesson_structure.py <curso>
    4. python scripts/sync_content_to_atlas.py            # dry-run
    5. python scripts/sync_content_to_atlas.py --confirm
"""
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


# Mantener en sync con sync_content_to_atlas.py — son las mismas colecciones
# que el sync drop-rea, así que también deben ser las que pulleamos de vuelta.
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


async def main():
    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")
    confirm = "--confirm" in sys.argv[1:]
    atlas_uri = os.environ.get("ATLAS_URL", "").strip()
    if not atlas_uri:
        print("ERROR: ATLAS_URL no definido en backend/.env")
        sys.exit(1)
    local_url = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]

    src = AsyncIOMotorClient(atlas_uri)[db_name]   # Atlas (fuente)
    dst = AsyncIOMotorClient(local_url)[db_name]   # local (destino)

    print(f"Source : Atlas / {db_name}")
    print(f"Target : {local_url} / {db_name}")
    print(f"Mode   : {'WRITE (--confirm)' if confirm else 'DRY-RUN'}")
    print()
    print(f"{'collection':<25s}  {'atlas':>6s}  {'upsert':>6s}  {'unchanged':>9s}  {'local-only':>10s}")
    print("-" * 70)

    grand = {"upserted": 0, "unchanged": 0, "local_only": 0}

    for c in CONTENT_COLLECTIONS:
        atlas_docs = await src[c].find({}).to_list(length=None)
        atlas_by_id = {}
        for d in atlas_docs:
            if "id" in d:
                atlas_by_id[d["id"]] = d
            else:
                # Documentos sin `id` (raros, ej: configuraciones por singleton).
                # Los identificamos por otro campo determinístico si lo hay.
                # Para `pricing_config` y `app_settings` usamos `config_id` o
                # similar; si no hay nada, los saltamos con una advertencia.
                key = d.get("config_id") or d.get("name")
                if key:
                    atlas_by_id[f"__nokey__{key}"] = d
                else:
                    print(f"  ⚠ {c}: doc sin `id` ni clave alternativa, saltado: {list(d.keys())[:5]}")

        # Inventario de ids en local para detectar docs local-only (newly-seeded).
        local_ids = set()
        async for d in dst[c].find({}, {"id": 1, "config_id": 1, "name": 1}):
            key = d.get("id") or (f"__nokey__{d.get('config_id') or d.get('name')}" if d.get("config_id") or d.get("name") else None)
            if key:
                local_ids.add(key)

        upserted = unchanged = 0
        for atlas_id, atlas_doc in atlas_by_id.items():
            # Mongo `_id` es inmutable y no debe sobrescribirse.
            atlas_clean = {k: v for k, v in atlas_doc.items() if k != "_id"}

            # Lookup local: si el id es __nokey__, buscamos por config_id/name.
            if atlas_id.startswith("__nokey__"):
                key_val = atlas_id[len("__nokey__"):]
                query = {"$or": [{"config_id": key_val}, {"name": key_val}]}
            else:
                query = {"id": atlas_id}

            current = await dst[c].find_one(query, {"_id": 0})
            if current == atlas_clean:
                unchanged += 1
                continue
            if confirm:
                await dst[c].replace_one(query, atlas_clean, upsert=True)
            upserted += 1

        local_only_ids = local_ids - set(atlas_by_id.keys())
        local_only = len(local_only_ids)

        print(f"{c:<25s}  {len(atlas_by_id):>6d}  {upserted:>6d}  {unchanged:>9d}  {local_only:>10d}")
        grand["upserted"] += upserted
        grand["unchanged"] += unchanged
        grand["local_only"] += local_only

    print("-" * 70)
    print(f"Total: upsert={grand['upserted']}  unchanged={grand['unchanged']}  local-only={grand['local_only']}")
    if not confirm:
        print()
        print("Dry-run. Re-ejecutá con --confirm para aplicar.")
    else:
        print()
        print("Listo. Local refleja Atlas + cualquier nuevo doc seedeado en local.")
        print("Ahora podés correr `sync_content_to_atlas.py --confirm` sin perder")
        print("ediciones de admin (Desmos, imágenes, textos, preguntas, etc).")


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    asyncio.run(main())
