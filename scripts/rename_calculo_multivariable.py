"""
Estandariza la carpeta docs/cursos/generales/calculo-multivariable/:
- Borra todos los archivos .mp4 (videos).
- Renombra PDFs:
  * Dentro de Clases/...: '*_Apuntes.pdf' -> 'Apuntes.pdf', otros -> 'Clase.pdf'.
  * Dentro de Ejercicios/...: '*_Solucionario.pdf' o '*_Apuntes.pdf' o '*_Soluciones.pdf' -> 'Soluciones.pdf', otros -> 'Enunciados.pdf'.
- Renombra carpetas de lección/ejercicio: 'NN. Tema' (padding 0, sentence-case en español).
- Renombra carpetas de capítulo: 'NN. Título' (padding 0).

Maneja Unicode NFC/NFD (problema típico de OneDrive en Windows).

Uso:
  python scripts/rename_calculo_multivariable.py             # dry-run
  python scripts/rename_calculo_multivariable.py --apply     # aplica cambios
"""
import os
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = REPO_ROOT / "docs" / "cursos" / "generales" / "calculo-multivariable"


# ============================================================
# Mapeos de carpetas
# ============================================================

# Lecciones (dentro de Clases/) — mapeo old_relative_path -> new_relative_path
# (relativos a BASE; usan los nombres ORIGINALES de los capítulos)
LESSON_DIR_RENAMES = {
    # Capítulo 1
    "1. Series y Sucesiones/Clases/0. Integrales Impropias": "1. Series y Sucesiones/Clases/00. Integrales impropias",
    "1. Series y Sucesiones/Clases/1. Sucesiones": "1. Series y Sucesiones/Clases/01. Sucesiones",
    "1. Series y Sucesiones/Clases/2. Series": "1. Series y Sucesiones/Clases/02. Series",
    "1. Series y Sucesiones/Clases/3. Pruebas de Series": "1. Series y Sucesiones/Clases/03. Pruebas de series",
    "1. Series y Sucesiones/Clases/4. Series Alternantes": "1. Series y Sucesiones/Clases/04. Series alternantes",
    "1. Series y Sucesiones/Clases/5. Criterios de Convergencia": "1. Series y Sucesiones/Clases/05. Criterios de convergencia",
    "1. Series y Sucesiones/Clases/6. Series de Potencias": "1. Series y Sucesiones/Clases/06. Series de potencias",
    "1. Series y Sucesiones/Clases/7. Representación de Funciones": "1. Series y Sucesiones/Clases/07. Representación de funciones",
    "1. Series y Sucesiones/Clases/8. Series de Taylor y Maclaurin": "1. Series y Sucesiones/Clases/08. Series de Taylor y Maclaurin",
    "1. Series y Sucesiones/Clases/9. Aplicaciones de Taylor (Pendiente)": "1. Series y Sucesiones/Clases/09. Aplicaciones de Taylor (pendiente)",

    # Capítulo 2
    "2. Espacio/Clases/1. Vectores": "2. Espacio/Clases/01. Vectores",
    "2. Espacio/Clases/2. Producto Punto": "2. Espacio/Clases/02. Producto punto",
    "2. Espacio/Clases/3. Producto Cruz": "2. Espacio/Clases/03. Producto cruz",
    "2. Espacio/Clases/4. Rectas y Planos": "2. Espacio/Clases/04. Rectas y planos",
    "2. Espacio/Clases/5. Superficies Cuádricas": "2. Espacio/Clases/05. Superficies cuádricas",

    # Capítulo 3
    "3. Funciones de Varias Variables/Clases/1. Dominio y Rango": "3. Funciones de Varias Variables/Clases/01. Dominio y rango",
    "3. Funciones de Varias Variables/Clases/2. Límites y Continuidad": "3. Funciones de Varias Variables/Clases/02. Límites y continuidad",

    # Capítulo 4
    "4. Derivadas Parciales/Clases/1. Derivadas Parciales": "4. Derivadas Parciales/Clases/01. Derivadas parciales",
    "4. Derivadas Parciales/Clases/2. Derivadas de Orden Superior": "4. Derivadas Parciales/Clases/02. Derivadas de orden superior",
    "4. Derivadas Parciales/Clases/3. Diferenciabilidad": "4. Derivadas Parciales/Clases/03. Diferenciabilidad",
    "4. Derivadas Parciales/Clases/4. Regla de la Cadena": "4. Derivadas Parciales/Clases/04. Regla de la cadena",

    # Capítulo 5
    "5. Aplicaciones de las Derivadas Parciales/Clases/1. Planos Tangentes y Aproximaciones Lineales": "5. Aplicaciones de las Derivadas Parciales/Clases/01. Planos tangentes y aproximaciones lineales",
    "5. Aplicaciones de las Derivadas Parciales/Clases/2. Derivadas Direccionales": "5. Aplicaciones de las Derivadas Parciales/Clases/02. Derivadas direccionales",
    "5. Aplicaciones de las Derivadas Parciales/Clases/3. Valores Máximos y Mínimos": "5. Aplicaciones de las Derivadas Parciales/Clases/03. Valores máximos y mínimos",
    "5. Aplicaciones de las Derivadas Parciales/Clases/4. Multiplicadores de Lagrange": "5. Aplicaciones de las Derivadas Parciales/Clases/04. Multiplicadores de Lagrange",

    # Capítulo 6
    "6. Integrales Múltiples/Clases/1. Integrales Dobles": "6. Integrales Múltiples/Clases/01. Integrales dobles",
    "6. Integrales Múltiples/Clases/2. Regiones Generales": "6. Integrales Múltiples/Clases/02. Regiones generales",
    "6. Integrales Múltiples/Clases/3. Coordenadas Polares": "6. Integrales Múltiples/Clases/03. Coordenadas polares",
    "6. Integrales Múltiples/Clases/4. Integrales Triples": "6. Integrales Múltiples/Clases/04. Integrales triples",
    "6. Integrales Múltiples/Clases/5. Coordenadas Cilíndricas": "6. Integrales Múltiples/Clases/05. Coordenadas cilíndricas",
    "6. Integrales Múltiples/Clases/6. Coordenadas Esféricas": "6. Integrales Múltiples/Clases/06. Coordenadas esféricas",
    "6. Integrales Múltiples/Clases/7. Cambio de Variables": "6. Integrales Múltiples/Clases/07. Cambio de variables",

    # Capítulo 7
    "7. Aplicaciones de Integrales Múltiples/Clases/1. Centros de Masa": "7. Aplicaciones de Integrales Múltiples/Clases/01. Centros de masa",
    "7. Aplicaciones de Integrales Múltiples/Clases/2. Momentos de Inercia": "7. Aplicaciones de Integrales Múltiples/Clases/02. Momentos de inercia",
    "7. Aplicaciones de Integrales Múltiples/Clases/3. Área de una Superficie": "7. Aplicaciones de Integrales Múltiples/Clases/03. Área de una superficie",
}

EXERCISE_DIR_RENAMES = {
    # Capítulo 1
    "1. Series y Sucesiones/Ejercicios/1E. Pruebas de Series": "1. Series y Sucesiones/Ejercicios/01. Pruebas de series",
    "1. Series y Sucesiones/Ejercicios/2E. Series Alternantes": "1. Series y Sucesiones/Ejercicios/02. Series alternantes",
    "1. Series y Sucesiones/Ejercicios/3E. Criterios de Convergencia": "1. Series y Sucesiones/Ejercicios/03. Criterios de convergencia",
    "1. Series y Sucesiones/Ejercicios/4E. Series de Potencias": "1. Series y Sucesiones/Ejercicios/04. Series de potencias",
    "1. Series y Sucesiones/Ejercicios/5E. Representación de Funciones": "1. Series y Sucesiones/Ejercicios/05. Representación de funciones",
    "1. Series y Sucesiones/Ejercicios/6E. Series de Taylor y Maclaurin": "1. Series y Sucesiones/Ejercicios/06. Series de Taylor y Maclaurin",

    # Capítulo 2
    "2. Espacio/Ejercicios/1E. Espacio": "2. Espacio/Ejercicios/01. Espacio",

    # Capítulo 3
    "3. Funciones de Varias Variables/Ejercicios/1E. Dominio y Curvas de Nivel": "3. Funciones de Varias Variables/Ejercicios/01. Dominio y curvas de nivel",
    "3. Funciones de Varias Variables/Ejercicios/2E. Límites": "3. Funciones de Varias Variables/Ejercicios/02. Límites",

    # Capítulo 4
    "4. Derivadas Parciales/Ejercicios/1E. Derivadas Parciales": "4. Derivadas Parciales/Ejercicios/01. Derivadas parciales",
    "4. Derivadas Parciales/Ejercicios/2E. Regla de la Cadena": "4. Derivadas Parciales/Ejercicios/02. Regla de la cadena",

    # Capítulo 5
    "5. Aplicaciones de las Derivadas Parciales/Ejercicios/1E. Planos Tangentes y Aproximaciones Lineales": "5. Aplicaciones de las Derivadas Parciales/Ejercicios/01. Planos tangentes y aproximaciones lineales",
    "5. Aplicaciones de las Derivadas Parciales/Ejercicios/2E. Derivadas Direccionales": "5. Aplicaciones de las Derivadas Parciales/Ejercicios/02. Derivadas direccionales",
    "5. Aplicaciones de las Derivadas Parciales/Ejercicios/3E. Valores Máximos y Mínimos": "5. Aplicaciones de las Derivadas Parciales/Ejercicios/03. Valores máximos y mínimos",
    "5. Aplicaciones de las Derivadas Parciales/Ejercicios/4E. Multiplicadores de Lagrange": "5. Aplicaciones de las Derivadas Parciales/Ejercicios/04. Multiplicadores de Lagrange",

    # Capítulo 6
    "6. Integrales Múltiples/Ejercicios/1E. Integrales Dobles": "6. Integrales Múltiples/Ejercicios/01. Integrales dobles",
    "6. Integrales Múltiples/Ejercicios/2E. Coordenadas Polares": "6. Integrales Múltiples/Ejercicios/02. Coordenadas polares",
    "6. Integrales Múltiples/Ejercicios/3E. Integrales Triples": "6. Integrales Múltiples/Ejercicios/03. Integrales triples",
    "6. Integrales Múltiples/Ejercicios/4E. Coordenadas Cilíndricas": "6. Integrales Múltiples/Ejercicios/04. Coordenadas cilíndricas",
    "6. Integrales Múltiples/Ejercicios/5E. Coordenadas Esféricas": "6. Integrales Múltiples/Ejercicios/05. Coordenadas esféricas",
    "6. Integrales Múltiples/Ejercicios/6E. Cambio de Variable": "6. Integrales Múltiples/Ejercicios/06. Cambio de variable",

    # Capítulo 7
    "7. Aplicaciones de Integrales Múltiples/Ejercicios/1E. Aplicaciones": "7. Aplicaciones de Integrales Múltiples/Ejercicios/01. Aplicaciones",
    "7. Aplicaciones de Integrales Múltiples/Ejercicios/2E. Área de Superficie": "7. Aplicaciones de Integrales Múltiples/Ejercicios/02. Área de superficie",
}

CHAPTER_DIR_RENAMES = {
    "1. Series y Sucesiones": "01. Series y Sucesiones",
    "2. Espacio": "02. Espacio",
    "3. Funciones de Varias Variables": "03. Funciones de Varias Variables",
    "4. Derivadas Parciales": "04. Derivadas Parciales",
    "5. Aplicaciones de las Derivadas Parciales": "05. Aplicaciones de las Derivadas Parciales",
    "6. Integrales Múltiples": "06. Integrales Múltiples",
    "7. Aplicaciones de Integrales Múltiples": "07. Aplicaciones de Integrales Múltiples",
}


# ============================================================
# Helpers
# ============================================================
def _nfd(s):
    return unicodedata.normalize("NFD", s)


def _resolve_actual_path(target_abs):
    """Encuentra el path real en disco (NFC vs NFD)."""
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
    """Decide el nombre nuevo para un PDF según su carpeta y sufijo."""
    name = path.name
    # ¿Está bajo Ejercicios/?
    is_ejercicio = any(part == "Ejercicios" for part in path.parts)

    base_no_ext = name[:-4] if name.lower().endswith(".pdf") else name

    if is_ejercicio:
        # Soluciones: sufijos posibles _Solucionario, _Soluciones, _Apuntes
        for suf in ("_Solucionario", "_Soluciones", "_Apuntes"):
            if base_no_ext.endswith(suf):
                return "Soluciones.pdf"
        return "Enunciados.pdf"
    else:
        # Bajo Clases/
        if base_no_ext.endswith("_Apuntes"):
            return "Apuntes.pdf"
        return "Clase.pdf"


# ============================================================
# Operaciones
# ============================================================
def find_videos():
    """Devuelve lista de Path de archivos .mp4 dentro de BASE."""
    return [p for p in BASE.rglob("*.mp4") if p.is_file()]


def find_pdfs():
    """Devuelve lista de Path de archivos .pdf dentro de BASE."""
    return [p for p in BASE.rglob("*.pdf") if p.is_file()]


def do_rename(old_abs, new_abs, dry_run, label=""):
    if old_abs == new_abs:
        return ("skip", "ya tiene ese nombre")
    actual_old = _resolve_actual_path(old_abs)
    if actual_old is None:
        return ("missing", f"no existe (ni NFC ni NFD)")
    case_only = (old_abs.name.lower() == new_abs.name.lower()
                 and old_abs.name != new_abs.name
                 and old_abs.parent == new_abs.parent)
    if new_abs.exists() and not case_only:
        actual_new = _resolve_actual_path(new_abs)
        if actual_new and actual_new != actual_old:
            return ("conflict", f"destino ya existe")
    if dry_run:
        return ("dry", f"{label}{old_abs.relative_to(BASE)}  →  {new_abs.relative_to(BASE)}")
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


# ============================================================
# Main
# ============================================================
def main():
    apply_mode = "--apply" in sys.argv

    if not BASE.exists():
        print(f"ERROR: no existe {BASE}")
        sys.exit(1)

    mode = "APPLY" if apply_mode else "DRY-RUN"
    print(f"Modo: {mode}")
    print(f"Base: {BASE}")

    counts = {"ok": 0, "dry": 0, "skip": 0, "missing": 0, "conflict": 0, "error": 0}

    def report(status, msg, prefix="  "):
        counts[status] = counts.get(status, 0) + 1
        sym = {"ok": "✓", "dry": " ", "skip": "·", "missing": "✗", "conflict": "!", "error": "✗"}[status]
        print(f"{prefix}{sym} {msg}")

    # -------- FASE 1: borrar videos --------
    videos = find_videos()
    print(f"\n=== FASE 1 — borrar videos ({len(videos)} .mp4) ===")
    for v in videos:
        s, m = do_delete(v, dry_run=not apply_mode)
        report(s, m)

    # -------- FASE 2: renombrar PDFs --------
    pdfs = find_pdfs()
    print(f"\n=== FASE 2 — renombrar PDFs ({len(pdfs)}) ===")
    # Detectar duplicados de destino dentro de la misma carpeta antes de aplicar
    dest_per_folder = {}
    for p in pdfs:
        new_name = classify_pdf(p)
        key = (str(p.parent), new_name)
        dest_per_folder.setdefault(key, []).append(p)

    duplicates = {k: v for k, v in dest_per_folder.items() if len(v) > 1}
    if duplicates:
        print("  ⚠ DUPLICADOS detectados (varios PDFs colisionarían en el mismo nombre destino):")
        for (folder, dest), files in duplicates.items():
            print(f"    En {Path(folder).relative_to(BASE)} → todos quieren llamarse '{dest}':")
            for f in files:
                print(f"      - {f.name}")
        print("  Resolviendo: el primero queda con el nombre, los demás con '_2', '_3', etc.")

    for p in pdfs:
        new_name = classify_pdf(p)
        target = p.parent / new_name
        # Si el target ya existe (otro PDF), agregar sufijo
        idx = 2
        actual_target = target
        while True:
            if not actual_target.exists() or actual_target == p:
                break
            stem = target.stem
            actual_target = target.parent / f"{stem}_{idx}.pdf"
            idx += 1
        s, m = do_rename(p, actual_target, dry_run=not apply_mode)
        report(s, m)

    # -------- FASE 3: renombrar carpetas de lección --------
    print(f"\n=== FASE 3 — carpetas de lección ({len(LESSON_DIR_RENAMES)}) ===")
    for old_rel, new_rel in LESSON_DIR_RENAMES.items():
        s, m = do_rename(BASE / old_rel, BASE / new_rel, dry_run=not apply_mode)
        report(s, m)

    # -------- FASE 4: renombrar carpetas de ejercicios --------
    print(f"\n=== FASE 4 — carpetas de ejercicios ({len(EXERCISE_DIR_RENAMES)}) ===")
    for old_rel, new_rel in EXERCISE_DIR_RENAMES.items():
        s, m = do_rename(BASE / old_rel, BASE / new_rel, dry_run=not apply_mode)
        report(s, m)

    # -------- FASE 5: renombrar carpetas de capítulo --------
    print(f"\n=== FASE 5 — carpetas de capítulo ({len(CHAPTER_DIR_RENAMES)}) ===")
    for old_rel, new_rel in CHAPTER_DIR_RENAMES.items():
        s, m = do_rename(BASE / old_rel, BASE / new_rel, dry_run=not apply_mode)
        report(s, m)

    print()
    print("=" * 60)
    print(f"Resumen: {counts}")
    if not apply_mode:
        print("\nPara aplicar:  python scripts/rename_calculo_multivariable.py --apply")


if __name__ == "__main__":
    main()
