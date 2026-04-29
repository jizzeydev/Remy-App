"""
Seed UC (Pontificia Universidad Católica de Chile) courses by linking chapters
from the General courses already in the DB.

Mapping comes from reading the official PUC class-by-class planning PDFs in
docs/cursos/uc/contenidos. Each UC course is registered under the PUC
university_id and its chapters are LINKED (not copied) from General courses,
so future updates to the General course propagate automatically. When the PUC
plan covers only a subset of a General chapter's lessons, we either exclude
specific lessons up-front (excluded_lesson_ids) or leave the mapping coarse
and let Jesús fine-tune from the admin UI.

Idempotent: skips a UC course if a course with the same `id` already exists,
and the link-chapters endpoint itself silently skips already-linked chapters.

Usage:
  cd backend && ./venv/Scripts/python.exe ../scripts/seed_uc_courses.py
"""
from __future__ import annotations

import os
import sys
import requests

# Windows consoles default to cp1252 and choke on unicode arrows; force UTF-8
# on stdout/stderr so the script's progress output survives.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

API = os.environ.get("REMY_API_URL", "http://localhost:8001/api")
ADMIN_USERNAME = os.environ.get("REMY_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("REMY_ADMIN_PASSWORD", "remy2026admin")

# Hard-coded chapter ids — these are stable in the seed and won't change.
# Found via: GET /api/courses/with-stats (each course returns its chapters).
CH = {
    # Cálculo Diferencial
    "cd_derivadas":          "ch-derivadas",
    "cd_limites":            "ch-limites-continuidad",
    "cd_aplicaciones":       "ch-aplicaciones-derivadas",

    # Cálculo Integral
    "ci_integrales":         "ch-integrales",
    "ci_metodos":            "ch-metodos-integracion",
    "ci_aplicaciones":       "ch-aplicaciones-integral",

    # Cálculo Multivariable
    "cm_series":             "ch-series-sucesiones",
    "cm_funciones":          "ch-funciones-varias-variables",
    "cm_parciales":          "ch-derivadas-parciales",
    "cm_apl_parciales":      "ch-aplicaciones-parciales",
    "cm_integrales_mult":    "ch-integrales-multiples",
    "cm_apl_integrales":     "ch-aplicaciones-integrales-multiples",
    "cm_espacio":            "ch-espacio",

    # Cálculo Vectorial
    "cv_curvas":             "ch-curvas",
    "cv_int_linea":          "ch-integrales-linea",
    "cv_int_superficie":     "ch-integrales-superficie",

    # Álgebra Lineal
    "al_sistemas":           "ch-al-sistemas-ecuaciones",
    "al_espacio":            "ch-al-espacio",
    "al_matrices":           "ch-al-algebra-matrices",
    "al_determinantes":      "ch-al-determinantes",
    "al_subespacios":        "ch-al-espacios-subespacios",
    "al_valores":            "ch-al-valores-vectores-propios",
    "al_ortogonalidad":      "ch-al-ortogonalidad",
    "al_simetricas":         "ch-al-matrices-simetricas",

    # Ecuaciones Diferenciales
    "ed_primer":             "ch-ed-edo-primer-orden",
    "ed_superior":           "ch-ed-edo-orden-superior",
    "ed_sistemas":           "ch-ed-sistemas-edo",
    "ed_laplace":            "ch-ed-transformada-laplace",
}

# PUC university id resolved at runtime so the seed survives a re-import.

# Each entry: course meta + ordered list of template chapters to link.
# `excluded_lesson_ids` is left empty in the seed; admin can prune lessons
# per university course later from the UI without re-running this script.
UC_COURSES = [
    {
        "id": "puc-mat1000-precalculo",
        "title": "Precálculo (PUC MAT1000)",
        "description": "Precálculo según el programa MAT1000 de la PUC: ecuaciones de la recta, parábola, inecuaciones, funciones reales, exponenciales, logarítmicas, trigonométricas, polinomiales, sucesiones y sumas.",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            "ch-prec-fundamentos",
            "ch-prec-funciones",
            "ch-prec-polinomiales-racionales",
            "ch-prec-exp-log",
            "ch-prec-trigonometria",
            "ch-prec-trig-analitica",
            "ch-prec-sucesiones-series",
            # MAT1000 NO incluye Números Complejos → no se linkea ese chapter.
        ],
    },
    {
        "id": "puc-mat1100-calculo1-servicios",
        "title": "Cálculo I (PUC MAT1100)",
        "description": "Cálculo de una variable orientado a carreras de servicio. Límites, continuidad, derivadas, aplicaciones de la derivada, integrales, técnicas básicas de integración y aplicaciones (área y volúmenes).",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            CH["cd_limites"],
            CH["cd_derivadas"],
            CH["cd_aplicaciones"],
            CH["ci_integrales"],
            CH["ci_metodos"],
            CH["ci_aplicaciones"],
        ],
    },
    {
        "id": "puc-mat1610-calculo1",
        "title": "Cálculo I (PUC MAT1610)",
        "description": "Cálculo en una variable: límites, continuidad, derivadas, aplicaciones (optimización, L'Hôpital, asíntotas, trazado), integrales y técnicas de integración (sustitución, partes, trigonométricas, sustitución trigonométrica, fracciones parciales).",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            CH["cd_limites"],
            CH["cd_derivadas"],
            CH["cd_aplicaciones"],
            CH["ci_integrales"],
            CH["ci_metodos"],
            CH["ci_aplicaciones"],
        ],
    },
    {
        "id": "puc-mat1620-calculo2",
        "title": "Cálculo II (PUC MAT1620)",
        "description": "Cálculo de varias variables: sucesiones, series numéricas y de potencias, funciones de varias variables, vectores y planos en el espacio, límites y continuidad, derivadas parciales, regla de la cadena, derivadas direccionales, máximos y mínimos, multiplicadores de Lagrange e integrales múltiples (incluye coordenadas polares, cilíndricas y esféricas).",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            CH["cm_series"],
            CH["cm_espacio"],
            CH["cm_funciones"],
            CH["cm_parciales"],
            CH["cm_apl_parciales"],
            CH["cm_integrales_mult"],
            CH["cm_apl_integrales"],
        ],
    },
    {
        "id": "puc-mat1630-calculo3",
        "title": "Cálculo III (PUC MAT1630)",
        "description": "Cálculo vectorial: parametrización de curvas, longitud de arco, curvatura, vectores normal y binormal, formulas de Frenet-Serret, campos vectoriales, integrales de línea, teorema de Green, parametrización de superficies, integrales de superficie, teorema de Stokes y teorema de la divergencia.",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            CH["cv_curvas"],
            CH["cv_int_linea"],
            CH["cv_int_superficie"],
        ],
    },
    {
        "id": "puc-mat1640-ecuaciones-diferenciales",
        "title": "Ecuaciones Diferenciales (PUC MAT1640)",
        "description": "Ecuaciones diferenciales ordinarias: primer orden (separables, lineales, exactas, Bernoulli, modelos poblacionales), segundo orden (homogéneas y no homogéneas con coeficientes constantes, vibraciones mecánicas), sistemas lineales y no lineales (valores propios, estabilidad, linealización) y transformada de Laplace.",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            CH["ed_primer"],
            CH["ed_superior"],
            CH["ed_sistemas"],
            CH["ed_laplace"],
        ],
    },
    {
        "id": "puc-mat1203-algebra-lineal",
        "title": "Álgebra Lineal (PUC MAT1203)",
        "description": "Vectores en R^n, sistemas de ecuaciones lineales, álgebra de matrices, determinantes, espacios y subespacios vectoriales, dimensión y rango, valores y vectores propios, diagonalización, ortogonalidad y mínimos cuadrados, matrices simétricas, factorización de Cholesky y descomposición SVD.",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            CH["al_sistemas"],
            CH["al_espacio"],
            CH["al_matrices"],
            CH["al_determinantes"],
            CH["al_subespacios"],
            CH["al_valores"],
            CH["al_ortogonalidad"],
            CH["al_simetricas"],
        ],
    },
    {
        "id": "puc-mat1220-calculo2-servicios",
        "title": "Cálculo II (PUC MAT1220)",
        "description": "Cálculo de varias variables orientado a carreras de servicio: ecuaciones diferenciales de primer orden (separables, lineales, modelos poblacionales), funciones de varias variables, vectores y planos en el espacio, derivadas parciales, planos tangentes, máximos y mínimos, multiplicadores de Lagrange, integrales dobles y series numéricas y de potencias.",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            CH["ed_primer"],
            CH["cm_espacio"],
            CH["cm_funciones"],
            CH["cm_parciales"],
            CH["cm_apl_parciales"],
            CH["cm_integrales_mult"],
            CH["cm_apl_integrales"],
            CH["cm_series"],
        ],
    },
    {
        "id": "puc-mat1279-algebra-lineal-servicios",
        "title": "Álgebra Lineal (PUC MAT1279)",
        "description": "Álgebra lineal orientado a carreras de servicio: sistemas de ecuaciones lineales, transformaciones lineales, álgebra de matrices, determinantes, espacios y subespacios vectoriales, dimensión y rango, valores y vectores propios y diagonalización.",
        "category": "Matemáticas",
        "level": "Universitario",
        "chapters": [
            CH["al_sistemas"],
            CH["al_espacio"],
            CH["al_matrices"],
            CH["al_determinantes"],
            CH["al_subespacios"],
            CH["al_valores"],
            # MAT1279 NO incluye Ortogonalidad ni Matrices Simétricas.
        ],
    },
]


def admin_login() -> str:
    r = requests.post(
        f"{API}/admin/login",
        json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def get_puc_university_id() -> str:
    r = requests.get(f"{API}/library-universities", timeout=10)
    r.raise_for_status()
    for u in r.json():
        if u.get("short_name") == "PUC":
            return u["id"]
    raise RuntimeError("PUC university not found in /library-universities")


def get_existing_course(course_id: str, headers: dict) -> dict | None:
    r = requests.get(f"{API}/admin/courses", headers=headers, timeout=10)
    r.raise_for_status()
    for c in r.json():
        if c.get("id") == course_id:
            return c
    return None


def create_course(course: dict, university_id: str, headers: dict) -> dict:
    """Create the course shell (visible_to_students=True).

    The Course model in server.py has `id` as a default-factory UUID; if we
    POST without an `id`, we get a random one. We send our own stable id so
    the seed is rerunnable.
    """
    payload = {
        "id": course["id"],
        "title": course["title"],
        "description": course["description"],
        "category": course["category"],
        "level": course["level"],
        "instructor": "Se Remonta",
        "rating": 0.0,
        "university_id": university_id,
        "visible_to_students": True,
        # `modules_count` is required by the Course model. We start at 0 and
        # let it grow naturally as chapters get linked.
        "modules_count": 0,
    }
    r = requests.post(f"{API}/admin/courses", json=payload, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()


def link_chapters(course_id: str, template_chapter_ids: list[str], headers: dict) -> dict:
    """Link the listed template chapters into the UC course.

    Uses the modern `chapters` shape so we could pass per-chapter exclusions
    later; the seed leaves them empty so the admin can prune from the UI.
    """
    payload = {
        "chapters": [
            {"template_chapter_id": ch_id, "excluded_lesson_ids": [], "excluded_question_ids": []}
            for ch_id in template_chapter_ids
        ]
    }
    r = requests.post(
        f"{API}/admin/courses/{course_id}/link-chapters",
        json=payload,
        headers=headers,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    print(f"→ Login admin @ {API}")
    token = admin_login()
    headers = {"Authorization": f"Bearer {token}"}

    puc_id = get_puc_university_id()
    print(f"→ PUC university id: {puc_id}")

    for spec in UC_COURSES:
        course_id = spec["id"]
        print(f"\n=== {course_id}  ({spec['title']}) ===")

        existing = get_existing_course(course_id, headers)
        if existing:
            print(f"  · curso ya existe (skip create)")
        else:
            try:
                created = create_course(spec, puc_id, headers)
                print(f"  · creado: {created.get('id')}")
            except requests.HTTPError as e:
                print(f"  ✗ error al crear: {e.response.status_code} {e.response.text[:200]}")
                continue

        try:
            res = link_chapters(course_id, spec["chapters"], headers)
            linked_n = len(res.get("linked_chapters") or [])
            errors = res.get("errors")
            print(f"  · linkeados {linked_n}/{len(spec['chapters'])} chapters")
            if errors:
                for e in errors:
                    print(f"    ⚠ {e}")
        except requests.HTTPError as e:
            print(f"  ✗ error al linkear: {e.response.status_code} {e.response.text[:200]}")

    print("\n✓ Seed UC completado.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
