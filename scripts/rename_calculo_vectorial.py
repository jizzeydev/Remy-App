"""
Estandariza la carpeta docs/cursos/generales/calculo-vectorial/:
- Borra todos los .mp4
- Renombra PDFs a Clase.pdf, Apuntes.pdf, Enunciados.pdf, Soluciones.pdf
- Renombra carpetas de lección/ejercicio: 'NN. Tema' (padding 0, sentence-case)
- Renombra capítulos con padding 0
"""
import os
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = REPO_ROOT / "docs" / "cursos" / "generales" / "calculo-vectorial"


# ============================================================
# Mapeos
# ============================================================
LESSON_DIR_RENAMES = {
    # Capítulo 1 — Curvas
    "1. Curvas/Clases/1. Ecuaciones Paramétricas": "1. Curvas/Clases/01. Ecuaciones paramétricas",
    "1. Curvas/Clases/2. Coordenadas Polares": "1. Curvas/Clases/02. Coordenadas polares",
    "1. Curvas/Clases/3. Funciones Vectoriales": "1. Curvas/Clases/03. Funciones vectoriales",
    "1. Curvas/Clases/4. Longitud de Curva": "1. Curvas/Clases/04. Longitud de curva",
    "1. Curvas/Clases/5. Vectores de Curvas": "1. Curvas/Clases/05. Vectores de curvas",
    "1. Curvas/Clases/6. Curvatura y Torsión": "1. Curvas/Clases/06. Curvatura y torsión",
    "1. Curvas/Clases/7. Frenet-Serret": "1. Curvas/Clases/07. Frenet-Serret",

    # Capítulo 2 — Integrales de Línea (Green = nombre propio)
    "2. Integrales de Línea/Clases/1. Campos Vectoriales y Escalares": "2. Integrales de Línea/Clases/01. Campos vectoriales y escalares",
    "2. Integrales de Línea/Clases/2. Integral de Línea en Campo Escalar": "2. Integrales de Línea/Clases/02. Integral de línea en campo escalar",
    "2. Integrales de Línea/Clases/3. Integral de Línea en Campo Vectorial": "2. Integrales de Línea/Clases/03. Integral de línea en campo vectorial",
    "2. Integrales de Línea/Clases/4. Teorema Fundamental": "2. Integrales de Línea/Clases/04. Teorema fundamental",
    "2. Integrales de Línea/Clases/5. Teorema de Green": "2. Integrales de Línea/Clases/05. Teorema de Green",
    "2. Integrales de Línea/Clases/6. Teorema Vectorial de Green": "2. Integrales de Línea/Clases/06. Teorema vectorial de Green",

    # Capítulo 3 — Integrales de Superficie (Stokes = nombre propio)
    "3. Integrales de Superficie/Clases/1. Superficies Paramétricas": "3. Integrales de Superficie/Clases/01. Superficies paramétricas",
    "3. Integrales de Superficie/Clases/2. Integral de Superficie": "3. Integrales de Superficie/Clases/02. Integral de superficie",
    "3. Integrales de Superficie/Clases/3. Superficies Orientadas": "3. Integrales de Superficie/Clases/03. Superficies orientadas",
    "3. Integrales de Superficie/Clases/4. Integrales de Superficie de Campos Vectoriales": "3. Integrales de Superficie/Clases/04. Integrales de superficie de campos vectoriales",
    "3. Integrales de Superficie/Clases/5. Aplicaciones": "3. Integrales de Superficie/Clases/05. Aplicaciones",
    "3. Integrales de Superficie/Clases/6. Teorema de Stokes": "3. Integrales de Superficie/Clases/06. Teorema de Stokes",
    "3. Integrales de Superficie/Clases/7. Teorema de la Divergencia": "3. Integrales de Superficie/Clases/07. Teorema de la divergencia",
}

EXERCISE_DIR_RENAMES = {
    # Cap 1 (no tiene 'E')
    "1. Curvas/Ejercicios/1. Parametrización": "1. Curvas/Ejercicios/01. Parametrización",
    "1. Curvas/Ejercicios/2. Áreas y Longitudes": "1. Curvas/Ejercicios/02. Áreas y longitudes",
    "1. Curvas/Ejercicios/3. Curvas": "1. Curvas/Ejercicios/03. Curvas",

    # Cap 2 (con 'E')
    "2. Integrales de Línea/Ejercicios/1E. Integrales de Línea": "2. Integrales de Línea/Ejercicios/01. Integrales de línea",
    "2. Integrales de Línea/Ejercicios/2E. Teorema Fundamental": "2. Integrales de Línea/Ejercicios/02. Teorema fundamental",
    "2. Integrales de Línea/Ejercicios/3E. Teorema de Green": "2. Integrales de Línea/Ejercicios/03. Teorema de Green",
    "2. Integrales de Línea/Ejercicios/4E. Teorema Vectorial de Green": "2. Integrales de Línea/Ejercicios/04. Teorema vectorial de Green",

    # Cap 3
    "3. Integrales de Superficie/Ejercicios/1E. Superficies Paramétricas": "3. Integrales de Superficie/Ejercicios/01. Superficies paramétricas",
    "3. Integrales de Superficie/Ejercicios/2E. Integrales de Superficie": "3. Integrales de Superficie/Ejercicios/02. Integrales de superficie",
    "3. Integrales de Superficie/Ejercicios/3E. Teorema de Stokes": "3. Integrales de Superficie/Ejercicios/03. Teorema de Stokes",
    "3. Integrales de Superficie/Ejercicios/4E. Teorema de la Divergencia": "3. Integrales de Superficie/Ejercicios/04. Teorema de la divergencia",
}

CHAPTER_DIR_RENAMES = {
    "1. Curvas": "01. Curvas",
    "2. Integrales de Línea": "02. Integrales de Línea",
    "3. Integrales de Superficie": "03. Integrales de Superficie",
}


# ============================================================
# Helpers (idénticos a rename_calculo_multivariable)
# ============================================================
def _nfd(s):
    return unicodedata.normalize("NFD", s)


def _resolve_actual_path(target_abs):
    if target_abs.exists():
        return target_abs
    parent = target_abs.parent
    if not parent.exists():
        return None
    target_nfd = _nfd(target_abs.name)
    for child in parent.iterdir():
        if _nfd(child.name) == target_nfd:
            return child
    return None


def classify_pdf(path):
    name = path.name
    is_ejercicio = any(part == "Ejercicios" for part in path.parts)
    base = name[:-4] if name.lower().endswith(".pdf") else name
    if is_ejercicio:
        for suf in ("_Solucionario", "_Soluciones", "_Apuntes"):
            if base.endswith(suf):
                return "Soluciones.pdf"
        return "Enunciados.pdf"
    else:
        if base.endswith("_Apuntes"):
            return "Apuntes.pdf"
        return "Clase.pdf"


def find_videos():
    return [p for p in BASE.rglob("*.mp4") if p.is_file()]


def find_pdfs():
    return [p for p in BASE.rglob("*.pdf") if p.is_file()]


def do_rename(old_abs, new_abs, dry_run):
    if old_abs == new_abs:
        return ("skip", "ya tiene ese nombre")
    actual_old = _resolve_actual_path(old_abs)
    if actual_old is None:
        return ("missing", "no existe")
    case_only = (old_abs.name.lower() == new_abs.name.lower()
                 and old_abs.name != new_abs.name
                 and old_abs.parent == new_abs.parent)
    if new_abs.exists() and not case_only:
        actual_new = _resolve_actual_path(new_abs)
        if actual_new and actual_new != actual_old:
            return ("conflict", "destino ya existe")
    if dry_run:
        return ("dry", f"{old_abs.relative_to(BASE)}  →  {new_abs.relative_to(BASE)}")
    try:
        if case_only:
            tmp = new_abs.parent / (actual_old.name + ".__tmp__")
            os.rename(str(actual_old), str(tmp))
            os.rename(str(tmp), str(new_abs))
        else:
            os.rename(str(actual_old), str(new_abs))
    except OSError as e:
        return ("error", str(e))
    return ("ok", f"{old_abs.relative_to(BASE)}  →  {new_abs.relative_to(BASE)}")


def do_delete(path, dry_run):
    if dry_run:
        return ("dry", f"DELETE {path.relative_to(BASE)}")
    try:
        path.unlink()
    except OSError as e:
        return ("error", str(e))
    return ("ok", f"DELETED {path.relative_to(BASE)}")


def main():
    apply_mode = "--apply" in sys.argv
    if not BASE.exists():
        print(f"ERROR: no existe {BASE}")
        sys.exit(1)

    mode = "APPLY" if apply_mode else "DRY-RUN"
    print(f"Modo: {mode}\nBase: {BASE}")
    counts = {"ok": 0, "dry": 0, "skip": 0, "missing": 0, "conflict": 0, "error": 0}

    def report(status, msg):
        counts[status] = counts.get(status, 0) + 1
        sym = {"ok": "✓", "dry": " ", "skip": "·", "missing": "✗", "conflict": "!", "error": "✗"}[status]
        print(f"  {sym} {msg}")

    videos = find_videos()
    print(f"\n=== FASE 1 — borrar videos ({len(videos)} .mp4) ===")
    for v in videos:
        s, m = do_delete(v, dry_run=not apply_mode)
        report(s, m)

    pdfs = find_pdfs()
    print(f"\n=== FASE 2 — renombrar PDFs ({len(pdfs)}) ===")
    for p in pdfs:
        new_name = classify_pdf(p)
        target = p.parent / new_name
        idx = 2
        actual = target
        while actual.exists() and actual != p:
            actual = target.parent / f"{target.stem}_{idx}.pdf"
            idx += 1
        s, m = do_rename(p, actual, dry_run=not apply_mode)
        report(s, m)

    print(f"\n=== FASE 3 — carpetas de lección ({len(LESSON_DIR_RENAMES)}) ===")
    for old_rel, new_rel in LESSON_DIR_RENAMES.items():
        s, m = do_rename(BASE / old_rel, BASE / new_rel, dry_run=not apply_mode)
        report(s, m)

    print(f"\n=== FASE 4 — carpetas de ejercicios ({len(EXERCISE_DIR_RENAMES)}) ===")
    for old_rel, new_rel in EXERCISE_DIR_RENAMES.items():
        s, m = do_rename(BASE / old_rel, BASE / new_rel, dry_run=not apply_mode)
        report(s, m)

    print(f"\n=== FASE 5 — capítulos ({len(CHAPTER_DIR_RENAMES)}) ===")
    for old_rel, new_rel in CHAPTER_DIR_RENAMES.items():
        s, m = do_rename(BASE / old_rel, BASE / new_rel, dry_run=not apply_mode)
        report(s, m)

    print()
    print("=" * 60)
    print(f"Resumen: {counts}")
    if not apply_mode:
        print("\nPara aplicar:  python scripts/rename_calculo_vectorial.py --apply")


if __name__ == "__main__":
    main()
