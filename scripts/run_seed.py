"""Ejecutar uno o varios seed scripts contra la base local con un solo comando.

Por qué existe: los seeds reales dependen de que el `.env` esté cargado y de que
`motor` esté en el PYTHONPATH — eso obligaba a correrlos como
`cd backend && ./venv/Scripts/python.exe seeds/<curso>/seed_capitulo_X.py`.
Este wrapper detecta el venv del backend, expande globs, y reporta un resumen
agregado del impacto en Mongo local.

Uso:
    # un solo seed
    python scripts/run_seed.py backend/seeds/algebra-lineal/seed_capitulo_1.py

    # varios (ojo con las comillas en bash para que el glob NO se expanda antes)
    python scripts/run_seed.py "backend/seeds/algebra-lineal/seed_capitulo_*.py"

    # todos los de un curso
    python scripts/run_seed.py "backend/seeds/precalculo/*.py"

    # dry-run (no escribe a Mongo, solo loggea qué haría)
    python scripts/run_seed.py --dry-run backend/seeds/algebra-lineal/seed_capitulo_1.py

Salida final: conteo agregado de cursos/capítulos/lecciones en Mongo local
después de correr todos los seeds, para que verifiques que el delta es el esperado.
"""
from __future__ import annotations

import asyncio
import glob
import os
import subprocess
import sys
from pathlib import Path

# Windows consoles default to cp1252 and choke on unicode (✓, Δ, etc.).
# Force UTF-8 for our own prints AND for the seed subprocess (via env).
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
VENV_PYTHON_CANDIDATES = [
    BACKEND_DIR / "venv" / "Scripts" / "python.exe",   # Windows
    BACKEND_DIR / "venv" / "bin" / "python",            # macOS / Linux
]


def find_python() -> Path:
    for cand in VENV_PYTHON_CANDIDATES:
        if cand.exists():
            return cand
    print("ERROR: no encontré el venv del backend. Esperaba uno de:")
    for c in VENV_PYTHON_CANDIDATES:
        print(f"  {c}")
    print()
    print("Creá el venv con:  python -m venv backend/venv && "
          "backend/venv/Scripts/pip.exe install -r backend/requirements.txt")
    sys.exit(1)


def expand_targets(args: list[str]) -> list[Path]:
    """Acepta paths absolutos/relativos y globs. Devuelve paths existentes,
    ordenados alfabéticamente para que `seed_capitulo_*` corra en orden."""
    paths: list[Path] = []
    for arg in args:
        # Resolver relativo al cwd primero, después al repo root.
        candidates = glob.glob(arg) or glob.glob(str(REPO_ROOT / arg))
        if not candidates:
            print(f"WARN: ningún archivo matchea '{arg}' — se ignora.")
            continue
        for c in candidates:
            p = Path(c).resolve()
            if not p.is_file():
                continue
            if p.suffix != ".py":
                print(f"WARN: '{p}' no es .py — se ignora.")
                continue
            paths.append(p)
    # Dedupe + sort.
    seen: set[Path] = set()
    out: list[Path] = []
    for p in sorted(paths):
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


async def collection_counts() -> dict[str, int]:
    """Snapshot de conteos en Mongo local — sirve para reportar el delta."""
    # Import perezoso porque solo este módulo necesita motor/dotenv en runtime.
    from dotenv import load_dotenv
    from motor.motor_asyncio import AsyncIOMotorClient
    load_dotenv(BACKEND_DIR / ".env")
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]
    out = {}
    for col in ("courses", "chapters", "lessons", "questions"):
        out[col] = await db[col].count_documents({})
    client.close()
    return out


def run_single(python: Path, seed_path: Path, dry_run: bool) -> int:
    """Ejecuta el seed con el python del venv. Devuelve el exit code."""
    env = os.environ.copy()
    # Asegura que el seed pueda imprimir Unicode (✓, ✅, etc.) en Windows.
    env["PYTHONIOENCODING"] = "utf-8"
    if dry_run:
        env["REMY_SEED_DRY_RUN"] = "1"
    print(f"\n— {seed_path.relative_to(REPO_ROOT)}")
    proc = subprocess.run(
        [str(python), str(seed_path)],
        cwd=str(BACKEND_DIR),
        env=env,
    )
    return proc.returncode


def maybe_install_dry_run_shim() -> None:
    """En modo --dry-run instalamos un shim que reemplaza los métodos de
    escritura de motor con no-ops que solo loggean. Lo hacemos vía un sitecustomize
    temporal que se inyecta por PYTHONSTARTUP — pero acá tomamos un atajo más
    simple: setear REMY_SEED_DRY_RUN=1 y que cada seed lo respete.

    Como los seeds existentes NO leen esa env var, en este release el --dry-run
    se limita a *avisarte* que no es honrado. Esta función deja el hook listo
    para cuando los seeds lo soporten (ver TODO en CONTENT.md)."""
    pass


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1

    dry_run = False
    if "--dry-run" in args:
        dry_run = True
        args = [a for a in args if a != "--dry-run"]

    python = find_python()
    targets = expand_targets(args)
    if not targets:
        print("ERROR: ningún seed para correr.")
        return 1

    if dry_run:
        print("⚠️  --dry-run NO está implementado todavía en los seeds existentes.")
        print("    Los seeds de matemáticas escriben a Mongo igual. Cancelá con Ctrl+C")
        print("    si no querés tocar la DB local. Continuando en 3s...")
        try:
            import time
            time.sleep(3)
        except KeyboardInterrupt:
            print("Cancelado.")
            return 130

    print(f"Python:  {python}")
    print(f"Backend: {BACKEND_DIR}")
    print(f"Seeds:   {len(targets)}")

    before = asyncio.run(collection_counts())

    failed: list[Path] = []
    for seed in targets:
        rc = run_single(python, seed, dry_run)
        if rc != 0:
            failed.append(seed)

    after = asyncio.run(collection_counts())

    print()
    print("=== Resumen Mongo local ===")
    print(f"{'colección':12s}  {'antes':>8s}  {'después':>8s}  {'Δ':>6s}")
    for col in ("courses", "chapters", "lessons", "questions"):
        delta = after[col] - before[col]
        sign = "+" if delta > 0 else ""
        print(f"{col:12s}  {before[col]:>8d}  {after[col]:>8d}  {sign}{delta:>5d}")

    if failed:
        print()
        print(f"❌ {len(failed)} seed(s) fallaron:")
        for p in failed:
            print(f"   - {p.relative_to(REPO_ROOT)}")
        return 1

    print()
    print("✅ Todos los seeds corrieron OK.")
    print("   Verificá en http://localhost:3007 antes de hacer sync a Atlas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
