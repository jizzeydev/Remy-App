"""
Estandariza la carpeta docs/cursos/generales/algebra-lineal/.
- Borra .mp4
- Renombra PDFs a Clase.pdf, Apuntes.pdf, Enunciados.pdf, Soluciones.pdf
- Renombra carpetas: padding 0, sentence-case en español, nombres propios mantenidos
- Corrige 'Algebra' → 'Álgebra' (con tilde) en el capítulo 3
"""
import os
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = REPO_ROOT / "docs" / "cursos" / "generales" / "algebra-lineal"


# ============================================================
# Mapeos
# ============================================================
LESSON_DIR_RENAMES = {
    # Cap 1 — Espacio
    "1. Espacio/Clases/1. Vectores": "1. Espacio/Clases/01. Vectores",
    "1. Espacio/Clases/2. Producto Punto": "1. Espacio/Clases/02. Producto punto",
    "1. Espacio/Clases/3. Producto Cruz": "1. Espacio/Clases/03. Producto cruz",
    "1. Espacio/Clases/4. Rectas y Planos": "1. Espacio/Clases/04. Rectas y planos",

    # Cap 2 — Sistemas de Ecuaciones
    "2. Sistemas de Ecuaciones/Clases/1. Matrices": "2. Sistemas de Ecuaciones/Clases/01. Matrices",
    "2. Sistemas de Ecuaciones/Clases/2. Reducción por Filas": "2. Sistemas de Ecuaciones/Clases/02. Reducción por filas",
    "2. Sistemas de Ecuaciones/Clases/3. Independencia Lineal": "2. Sistemas de Ecuaciones/Clases/03. Independencia lineal",
    "2. Sistemas de Ecuaciones/Clases/4. Conjunto Solución": "2. Sistemas de Ecuaciones/Clases/04. Conjunto solución",
    "2. Sistemas de Ecuaciones/Clases/5. Transformaciones Lineales": "2. Sistemas de Ecuaciones/Clases/05. Transformaciones lineales",

    # Cap 3 — Algebra de Matrices
    "3. Algebra de Matrices/Clases/1. Operaciones de Matrices": "3. Algebra de Matrices/Clases/01. Operaciones de matrices",
    "3. Algebra de Matrices/Clases/2. Inversa": "3. Algebra de Matrices/Clases/02. Inversa",
    "3. Algebra de Matrices/Clases/3. Matrices Elementales": "3. Algebra de Matrices/Clases/03. Matrices elementales",
    "3. Algebra de Matrices/Clases/4. Factorizaciones": "3. Algebra de Matrices/Clases/04. Factorizaciones",

    # Cap 4 — Determinantes
    "4. Determinantes/Clases/1. Determinante": "4. Determinantes/Clases/01. Determinante",
    "4. Determinantes/Clases/2. Propiedades de la Determinante": "4. Determinantes/Clases/02. Propiedades de la determinante",
    "4. Determinantes/Clases/3. Aplicaciones de la Determinante": "4. Determinantes/Clases/03. Aplicaciones de la determinante",

    # Cap 5 — Espacios y Subespacios Vectoriales
    "5. Espacios y Subespacios Vectoriales/Clases/1. Espacios Vectoriales": "5. Espacios y Subespacios Vectoriales/Clases/01. Espacios vectoriales",
    "5. Espacios y Subespacios Vectoriales/Clases/2. Espacios Notables": "5. Espacios y Subespacios Vectoriales/Clases/02. Espacios notables",
    "5. Espacios y Subespacios Vectoriales/Clases/3. Bases": "5. Espacios y Subespacios Vectoriales/Clases/03. Bases",
    "5. Espacios y Subespacios Vectoriales/Clases/4. Sistemas de Coordenadas": "5. Espacios y Subespacios Vectoriales/Clases/04. Sistemas de coordenadas",
    "5. Espacios y Subespacios Vectoriales/Clases/5. Dimensión y Rango": "5. Espacios y Subespacios Vectoriales/Clases/05. Dimensión y rango",
    "5. Espacios y Subespacios Vectoriales/Clases/6. Cambio de Coordenadas": "5. Espacios y Subespacios Vectoriales/Clases/06. Cambio de coordenadas",

    # Cap 6 — Valores y Vectores Propios
    "6. Valores y Vectores Propios/Clases/1. Ecuación Característica": "6. Valores y Vectores Propios/Clases/01. Ecuación característica",
    "6. Valores y Vectores Propios/Clases/2. Diagonalización": "6. Valores y Vectores Propios/Clases/02. Diagonalización",
    "6. Valores y Vectores Propios/Clases/3. Valores Propios y Transformaciones Lineales": "6. Valores y Vectores Propios/Clases/03. Valores propios y transformaciones lineales",
    "6. Valores y Vectores Propios/Clases/4. Valores Propios Complejos": "6. Valores y Vectores Propios/Clases/04. Valores propios complejos",

    # Cap 7 — Ortogonalidad (Gram-Schmidt = nombres propios)
    "7. Ortogonalidad/Clases/1. Subespacios Ortogonales": "7. Ortogonalidad/Clases/01. Subespacios ortogonales",
    "7. Ortogonalidad/Clases/2. Conjuntos Ortogonales": "7. Ortogonalidad/Clases/02. Conjuntos ortogonales",
    "7. Ortogonalidad/Clases/3. Proyecciones Ortogonales": "7. Ortogonalidad/Clases/03. Proyecciones ortogonales",
    "7. Ortogonalidad/Clases/4. Proceso de Gram-Schmidt": "7. Ortogonalidad/Clases/04. Proceso de Gram-Schmidt",
    "7. Ortogonalidad/Clases/5. Mínimos Cuadrados": "7. Ortogonalidad/Clases/05. Mínimos cuadrados",
    "7. Ortogonalidad/Clases/6. Modelos Lineales": "7. Ortogonalidad/Clases/06. Modelos lineales",

    # Cap 8 — Matrices Simétricas
    "8. Matrices Simétricas/Clases/1. Diagonalización Ortogonal": "8. Matrices Simétricas/Clases/01. Diagonalización ortogonal",
    "8. Matrices Simétricas/Clases/2. Formas Cuadráticas": "8. Matrices Simétricas/Clases/02. Formas cuadráticas",
    "8. Matrices Simétricas/Clases/3. Descomposición en Valores Singulares": "8. Matrices Simétricas/Clases/03. Descomposición en valores singulares",
}

EXERCISE_DIR_RENAMES = {
    "1. Espacio/Ejercicios/1. Espacio": "1. Espacio/Ejercicios/01. Espacio",

    "2. Sistemas de Ecuaciones/Ejercicios/1. Pivoteo": "2. Sistemas de Ecuaciones/Ejercicios/01. Pivoteo",
    "2. Sistemas de Ecuaciones/Ejercicios/2. Resolver Sistemas": "2. Sistemas de Ecuaciones/Ejercicios/02. Resolver sistemas",
    "2. Sistemas de Ecuaciones/Ejercicios/3. Transformaciones Lineales": "2. Sistemas de Ecuaciones/Ejercicios/03. Transformaciones lineales",

    "3. Algebra de Matrices/Ejercicios/1. Inversa": "3. Algebra de Matrices/Ejercicios/01. Inversa",
    "3. Algebra de Matrices/Ejercicios/2. Factorizaciones": "3. Algebra de Matrices/Ejercicios/02. Factorizaciones",

    "4. Determinantes/Ejercicios/1. Determinantes": "4. Determinantes/Ejercicios/01. Determinantes",

    "5. Espacios y Subespacios Vectoriales/Ejercicios/1. Espacios Vectoriales": "5. Espacios y Subespacios Vectoriales/Ejercicios/01. Espacios vectoriales",
    "5. Espacios y Subespacios Vectoriales/Ejercicios/2. Coordenadas": "5. Espacios y Subespacios Vectoriales/Ejercicios/02. Coordenadas",

    "6. Valores y Vectores Propios/Ejercicios/1. Diagonalización": "6. Valores y Vectores Propios/Ejercicios/01. Diagonalización",
    "6. Valores y Vectores Propios/Ejercicios/2. Transformaciones Lineales": "6. Valores y Vectores Propios/Ejercicios/02. Transformaciones lineales",
    "6. Valores y Vectores Propios/Ejercicios/3. Valores Propios Complejos": "6. Valores y Vectores Propios/Ejercicios/03. Valores propios complejos",

    "7. Ortogonalidad/Ejercicios/1. Conjuntos Ortogonales": "7. Ortogonalidad/Ejercicios/01. Conjuntos ortogonales",
    "7. Ortogonalidad/Ejercicios/2. Mínimos Cuadrados": "7. Ortogonalidad/Ejercicios/02. Mínimos cuadrados",

    "8. Matrices Simétricas/Ejercicios/1. Diagonalización Ortogonal": "8. Matrices Simétricas/Ejercicios/01. Diagonalización ortogonal",
    "8. Matrices Simétricas/Ejercicios/2. Formas Cuadráticas": "8. Matrices Simétricas/Ejercicios/02. Formas cuadráticas",
    "8. Matrices Simétricas/Ejercicios/3. Descomposición en Valores Singulares": "8. Matrices Simétricas/Ejercicios/03. Descomposición en valores singulares",
}

# Capítulos: padding 0 + corrección 'Algebra' → 'Álgebra' (Cap 3)
CHAPTER_DIR_RENAMES = {
    "1. Espacio": "01. Espacio",
    "2. Sistemas de Ecuaciones": "02. Sistemas de Ecuaciones",
    "3. Algebra de Matrices": "03. Álgebra de Matrices",
    "4. Determinantes": "04. Determinantes",
    "5. Espacios y Subespacios Vectoriales": "05. Espacios y Subespacios Vectoriales",
    "6. Valores y Vectores Propios": "06. Valores y Vectores Propios",
    "7. Ortogonalidad": "07. Ortogonalidad",
    "8. Matrices Simétricas": "08. Matrices Simétricas",
}


# ============================================================
# Helpers (idénticos a scripts anteriores)
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
        print("\nPara aplicar:  python scripts/rename_algebra_lineal.py --apply")


if __name__ == "__main__":
    main()
