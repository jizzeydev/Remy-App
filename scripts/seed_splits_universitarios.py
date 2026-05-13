"""Seed de splits universitarios de Remy.

Carga las 5 universidades (UAI, UANDES, UCH, UDD, UTFSM) y todos sus ramos
matemáticos del documento docs/splits-remy.md como `courses` con
`university_id`, reutilizando los cursos base de Remy via chapter linking.

**Create-only / safe-for-prod**:
  - Cursos: si el `id` ya existe en la DB, se SKIPEA por completo (no se
    tocan campos, ni chapters linkeados, ni axes). El admin manda en lo ya
    creado.
  - Universidades: si ya existen, sólo se añade `tier` cuando está vacío.
    Logo, nombre, is_active y demás campos no se tocan.
  - Cursos base generales (precalculo, calculo-diferencial, etc.) NUNCA se
    escriben — sólo se leen para conocer sus chapter IDs y hacer link.

Idempotente: re-ejecutar no duplica ni pisa lo curado por el admin.
Las universidades pendientes (USACH, UdeC, PUCV, UDP, UNAB, USS, UMayor)
NO se cargan acá — el schema queda listo y se agregarán cuando Cowork
entregue su investigación.

Convención de slugs: los IDs del doc son el identificador estable que cruza
con el dashboard de splits (apps/ops/data/splits en se-remonta-ops). Cuando
varios slugs apuntan al mismo programa (ej. mismo ramo dictado en plan común
e Ing. CS), se crea UN curso con `alt_slugs` listando los demás.

Uso:
    cd backend && ./venv/Scripts/python.exe ../scripts/seed_splits_universitarios.py

Variables de entorno:
    MONGO_URL, DB_NAME (vienen de backend/.env).
"""
from __future__ import annotations

import asyncio
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Windows consoles default to cp1252 and choke on unicode arrows.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
load_dotenv(BACKEND_DIR / ".env")


# ============================================================
# Universidades
# ============================================================
UNIVERSITIES = [
    {"short_name": "UAI", "name": "Universidad Adolfo Ibáñez", "tier": 1},
    {"short_name": "UANDES", "name": "Universidad de los Andes", "tier": 1},
    {"short_name": "UCH", "name": "Universidad de Chile", "tier": 1},
    {"short_name": "UDD", "name": "Universidad del Desarrollo", "tier": 2},
    {"short_name": "UTFSM", "name": "Universidad Técnica Federico Santa María", "tier": 2},
]


# ============================================================
# Ramos
# ============================================================
# Cada entry:
#   id: slug canónico (estable, cruza con dashboard de splits)
#   uni: short_name de la universidad
#   title: nombre visible
#   semester: 1..N (None para ramos sin sem asignado)
#   code: código oficial (opcional, ej "MA1102")
#   base: list[str] de slugs de cursos base de Remy (precalculo,
#         calculo-diferencial, calculo-integral, algebra-lineal,
#         calculo-multivariable, calculo-vectorial, ecuaciones-diferenciales)
#   prereqs: list[str] de IDs canónicos de otros ramos universitarios
#   match: "alto" | "medio"
#   axes: list[str] (texto literal del array `contenidos` del doc, en orden)
#   alt_slugs: list[str] de otros slugs del doc que apuntan al mismo programa
#              (convalidación o "mismo programa que X")
#   notes: texto libre — incluye motivaciones del split y advertencias del doc
#
# Reglas:
#   - "alto" -> coverage_status="complete"
#   - "medio" -> coverage_status="partial" (admin curará chapters / ejes después)
#   - match_level "bajo" / "ninguno" / "no aplica" -> NO se cargan acá
#   - `nivelacion-ing` queda fuera (decisión 2026-05-13: dejar curso afuera)
#   - `calculo-1var-gen` -> [calculo-diferencial, calculo-integral]

RAMOS: list[dict] = [
    # ============================================================
    # UAI — Tier 1
    # ============================================================
    {
        "id": "uai-plan-comun-algebra",
        "uni": "UAI",
        "title": "Álgebra (Plan Común UAI)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Lógica y conjuntos (proposiciones, álgebra de conjuntos, cuantificadores)",
            "Números reales (axiomas, demostraciones, inducción)",
            "Números naturales (sucesiones, progresiones, sumatorias, productoria, combinatoria, binomio de Newton)",
            "Trigonometría (funciones, identidades, ecuaciones trigonométricas)",
            "Geometría analítica (vectores, producto punto/cruz, rectas, planos, distancias en el espacio)",
            "Números complejos (operaciones, forma polar, raíces)",
            "Polinomios (división sintética, raíces, teorema del resto, fracciones parciales)",
        ],
        "alt_slugs": [
            "uai-computer-science-algebra",
            "uai-bachillerato-ic-algebra",
            "uai-arq-ici-algebra",
        ],
        "notes": "Dictado en Plan Común Ing. Civil, Computer Science, Bachillerato Ing. Civil y Doble Título Arq+ICI.",
    },
    {
        "id": "uai-plan-comun-calculo-diferencial",
        "uni": "UAI",
        "title": "Cálculo Diferencial (Plan Común UAI)",
        "semester": 1,
        "base": ["calculo-diferencial"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Números reales e inecuaciones",
            "Funciones: dominio, recorrido, transformaciones, inyectivas, inversas, polinomiales, exponenciales, logarítmicas",
            "Límites (finitos, al infinito, continuidad, TVI)",
            "Derivadas: definición, reglas, derivadas implícitas",
            "Aplicaciones: razón de cambio, máx/mín, TVM, L'Hôpital, graficación",
        ],
        "alt_slugs": [
            "uai-computer-science-calculo-diferencial",
            "uai-bachillerato-ic-calculo-diferencial",
        ],
        "notes": "Dictado en Plan Común Ing. Civil, Computer Science y Bachillerato Ing. Civil.",
    },
    {
        "id": "uai-plan-comun-calculo-integral",
        "uni": "UAI",
        "title": "Cálculo Integral (Plan Común UAI)",
        "semester": 2,
        "base": ["calculo-integral"],
        "prereqs": ["uai-plan-comun-calculo-diferencial"],
        "match": "alto",
        "axes": [
            "Antiderivadas, integral indefinida, TFC, sustitución, partes, fracciones parciales, sustitución trigonométrica",
            "Aplicaciones: área entre curvas, volúmenes (discos, cascarones), curvas parametrizadas, polares",
            "Integrales impropias (tipo I y II, comparación)",
            "Sucesiones y series (criterios, series de potencias, radio/intervalo, Taylor)",
        ],
        "alt_slugs": ["uai-computer-science-calculo-integral"],
        "notes": "Dictado en Plan Común Ing. Civil y Computer Science.",
    },
    {
        "id": "uai-plan-comun-algebra-lineal",
        "uni": "UAI",
        "title": "Álgebra Lineal (Plan Común UAI)",
        "semester": 2,
        "base": ["algebra-lineal"],
        "prereqs": ["uai-plan-comun-algebra"],
        "match": "alto",
        "axes": [
            "Matrices y sistemas (Gauss-Jordan, homogéneos, por bloques, inversa, elementales)",
            "Determinantes",
            "Espacios y subespacios vectoriales (combinación e independencia lineal, bases, dimensión, coordenadas, cambio de base, subespacios fundamentales)",
            "Transformaciones lineales (kernel, imagen, inyec/sobre, matriz asociada)",
            "Diagonalización (valores/vectores propios, cadenas de Markov)",
            "Análisis vectorial (Gram-Schmidt, complemento/proyección ortogonal, mínimos cuadrados)",
        ],
        "alt_slugs": [
            "uai-computer-science-algebra-lineal",
            "uai-arq-ici-algebra-lineal",
        ],
        "notes": "Match directo y completo con `algebra-lineal-gen`.",
    },
    {
        "id": "uai-plan-comun-calculo-multivariables",
        "uni": "UAI",
        "title": "Cálculo Multivariables (Plan Común UAI)",
        "semester": 3,
        "base": ["calculo-multivariable", "calculo-vectorial"],
        "prereqs": ["uai-plan-comun-calculo-integral", "uai-plan-comun-algebra-lineal"],
        "match": "alto",
        "axes": [
            "Funciones de varias variables (superficies cuadráticas, límites, continuidad, derivadas parciales, diferenciabilidad)",
            "Plano tangente, aproximaciones lineales, regla de la cadena, derivación implícita",
            "Derivadas direccionales, máx/mín, Lagrange",
            "Integrales dobles (cambio de región, polares, masa y centro de masa)",
            "Integrales triples (cilíndricas, esféricas, cambios de variable)",
            "Cálculo vectorial (integrales de línea, Green, rotacional, divergencia, integrales de superficie, Stokes, teorema de la divergencia)",
        ],
    },
    {
        "id": "uai-plan-comun-ecuaciones-diferenciales",
        "uni": "UAI",
        "title": "Ecuaciones Diferenciales (Plan Común UAI)",
        "semester": 4,
        "base": ["ecuaciones-diferenciales"],
        "prereqs": ["uai-plan-comun-calculo-multivariables"],
        "match": "alto",
        "axes": [
            "EDO 1er orden (separable, lineal, exacta, factor integrante, homogénea, Bernoulli, Ricatti, reducible)",
            "Modelos con ED 1er orden",
            "ED orden superior (coeficientes constantes, Cauchy-Euler, coef. indeterminados, variación de parámetros, masa-resorte)",
            "Sistemas de ED",
            "Transformada de Laplace (propiedades, traslación, escalón, convolución, Delta de Dirac)",
            "Soluciones por series (puntos ordinarios, singulares regulares, Bessel)",
            "Serie de Fourier",
        ],
        "alt_slugs": ["uai-arq-ici-ecuaciones-diferenciales"],
        "notes": "Curso UAI más extenso: series Fourier + Bessel — material complementario.",
    },
    {
        "id": "uai-icom-matematicas-avanzadas-i",
        "uni": "UAI",
        "title": "Matemáticas Avanzadas I (Ing. Comercial UAI)",
        "semester": 1,
        "base": ["precalculo", "algebra-lineal"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Lógica y conjuntos. Números naturales y reales (inducción, sucesiones, progresiones, sumatorias)",
            "Axiomas de orden, demostraciones, inecuaciones (con valor absoluto), axioma del supremo",
            "Funciones (dominio, imagen, composición, inversas, log/exp, gráficos, modelación)",
            "Matrices y sistemas (Gauss-Jordan, homogéneos, por bloques, inversa, elementales)",
            "Determinantes",
            "Espacios vectoriales, subespacios, combinación y dependencia lineal",
        ],
        "alt_slugs": [
            "uai-icom-admin-matematicas-avanzadas-i",
            "uai-icom-economia-matematicas-avanzadas-i",
            "uai-bachillerato-icom-matematicas-avanzadas-i",
        ],
        "notes": "Programa compartido entre Lic. Admin Empresas, Lic. Economía y Bachillerato Ing. Comercial.",
    },
    {
        "id": "uai-icom-matematicas-avanzadas-ii",
        "uni": "UAI",
        "title": "Matemáticas Avanzadas II (Ing. Comercial UAI)",
        "semester": 2,
        "base": ["calculo-diferencial", "calculo-integral"],
        "prereqs": ["uai-icom-matematicas-avanzadas-i"],
        "match": "alto",
        "axes": [
            "Sistemas de ecuaciones lineales (repaso)",
            "Límites (normales, trigonométricos, al infinito, laterales, continuidad, teoremas)",
            "Derivadas (definición, reglas, recta tangente, análisis marginal, derivación implícita)",
            "Aplicaciones de derivadas (extremos, crecimiento, optimización, L'Hôpital)",
            "Integrales (sustitución, partes, Riemann, TFC)",
            "Aplicaciones integrales (área entre curvas, excedentes, impropias, criterios de convergencia)",
            "Funciones de probabilidad",
        ],
        "alt_slugs": [
            "uai-icom-admin-matematicas-avanzadas-ii",
            "uai-icom-economia-matematicas-avanzadas-ii",
        ],
        "notes": "Dictado en Admin y Economía. No incluye multivariable — verificado.",
    },
    {
        "id": "uai-negocios-tech-algebra-lineal-y-optimizacion",
        "uni": "UAI",
        "title": "Álgebra Lineal y Optimización (Ing. en Negocios y Tecnología UAI)",
        "semester": 1,
        "base": ["algebra-lineal"],
        "prereqs": [],
        "match": "medio",
        "axes": [
            "Matrices y sistemas lineales",
            "Espacios vectoriales básicos",
            "Introducción a optimización lineal",
            "Aplicaciones a negocios",
        ],
        "notes": "Componente de optimización es específica — material complementario pendiente.",
    },
    {
        "id": "uai-bachillerato-ic-introduccion-al-algebra",
        "uni": "UAI",
        "title": "Introducción al Álgebra (Bachillerato Ing. Civil UAI)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Razonamiento lógico-matemático",
            "Conjuntos y números",
            "Ecuaciones e inecuaciones básicas",
            "Funciones elementales",
        ],
    },
    {
        "id": "uai-bachillerato-ic-introduccion-al-calculo",
        "uni": "UAI",
        "title": "Introducción al Cálculo (Bachillerato Ing. Civil UAI)",
        "semester": 1,
        "base": ["precalculo", "calculo-diferencial"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Funciones y sus gráficas",
            "Concepto intuitivo de límite",
            "Introducción a la derivada",
            "Pendiente y razón de cambio",
        ],
    },
    {
        "id": "uai-bachillerato-icom-introduccion-al-calculo",
        "uni": "UAI",
        "title": "Introducción al Cálculo (Bachillerato Ing. Comercial UAI)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [],
        "notes": "Versión introductoria — el doc no detalla ejes específicos.",
    },
    {
        "id": "uai-bachillerato-icom-introduccion-al-algebra",
        "uni": "UAI",
        "title": "Introducción al Álgebra (Bachillerato Ing. Comercial UAI)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [],
        "notes": "Versión introductoria — el doc no detalla ejes específicos.",
    },

    # ============================================================
    # UANDES — Tier 1
    # ============================================================
    {
        "id": "uandes-plan-comun-ing-algebra-e-introduccion-al-calculo",
        "uni": "UANDES",
        "title": "Álgebra e Introducción al Cálculo (Plan Común Ing. UANDES)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Conjuntos y números reales (axiomas, desigualdades, valor absoluto)",
            "Polinomios (operaciones, división sintética, raíces)",
            "Funciones reales de variable real (lineal, cuadrática, potencia, exp, log)",
            "Trigonometría (razones, identidades, teorema del seno y coseno)",
            "Números complejos (binomial, polar)",
            "Introducción a límites y continuidad",
        ],
    },
    {
        "id": "uandes-plan-comun-ing-calculo-i",
        "uni": "UANDES",
        "title": "Cálculo I (Plan Común Ing. UANDES)",
        "semester": 2,
        "base": ["calculo-diferencial"],
        "prereqs": ["uandes-plan-comun-ing-algebra-e-introduccion-al-calculo"],
        "match": "alto",
        "axes": [
            "Límites (definición formal, propiedades, laterales, al infinito)",
            "Continuidad",
            "Derivadas (definición, reglas, cadena)",
            "Derivación implícita y logarítmica",
            "Aplicaciones (máx/mín, concavidad, L'Hôpital)",
            "Análisis y graficación",
            "Introducción a la integral",
        ],
    },
    {
        "id": "uandes-plan-comun-ing-algebra-lineal",
        "uni": "UANDES",
        "title": "Álgebra Lineal (Plan Común Ing. UANDES)",
        "semester": 2,
        "base": ["algebra-lineal"],
        "prereqs": ["uandes-plan-comun-ing-algebra-e-introduccion-al-calculo"],
        "match": "alto",
        "axes": [
            "Matrices y sistemas (Gauss, Gauss-Jordan)",
            "Determinantes",
            "Espacios vectoriales (subespacio, independencia, base, dimensión)",
            "Transformaciones lineales (núcleo, imagen)",
            "Producto interior, Gram-Schmidt",
            "Valores y vectores propios, diagonalización",
        ],
    },
    {
        "id": "uandes-plan-comun-ing-calculo-ii",
        "uni": "UANDES",
        "title": "Cálculo II (Plan Común Ing. UANDES)",
        "semester": 3,
        "base": ["calculo-diferencial", "calculo-integral", "calculo-multivariable"],
        "prereqs": ["uandes-plan-comun-ing-calculo-i"],
        "match": "alto",
        "axes": [
            "Antiderivadas e integral indefinida",
            "Técnicas de integración (sustitución, partes, fracciones parciales, trigonométricas)",
            "Integral definida y TFC",
            "Aplicaciones (áreas, volúmenes, longitud de arco)",
            "Integrales impropias",
            "Funciones de varias variables, introducción a derivadas parciales",
            "Integrales dobles y triples",
        ],
        "notes": "Curso mezcla 1 y varias variables.",
    },
    {
        "id": "uandes-plan-comun-ing-ecuaciones-diferenciales",
        "uni": "UANDES",
        "title": "Ecuaciones Diferenciales (Plan Común Ing. UANDES)",
        "semester": 3,
        "base": ["ecuaciones-diferenciales"],
        "prereqs": ["uandes-plan-comun-ing-calculo-i"],
        "match": "alto",
        "axes": [
            "EDO 1er orden (separables, lineales, exactas, Bernoulli)",
            "EDO 2do orden (coef. constantes, variación de parámetros)",
            "Laplace (definición, propiedades, inversión)",
            "Sistemas de ED",
            "Aplicaciones a ingeniería (circuitos, resortes, mezcla)",
        ],
    },
    # Ing. Civil Química (nueva malla 2026)
    {
        "id": "uandes-ing-civil-quimica-introduccion-al-algebra-y-geometria",
        "uni": "UANDES",
        "title": "Introducción al Álgebra y Geometría (Ing. Civil Química UANDES)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [],
        "notes": "Malla nueva 2026 — ejes detallados pendientes en el doc.",
    },
    {
        "id": "uandes-ing-civil-quimica-introduccion-al-calculo",
        "uni": "UANDES",
        "title": "Introducción al Cálculo (Ing. Civil Química UANDES)",
        "semester": 1,
        "base": ["precalculo", "calculo-diferencial"],
        "prereqs": [],
        "match": "alto",
        "axes": [],
        "notes": "Malla nueva 2026.",
    },
    {
        "id": "uandes-ing-civil-quimica-calculo-i",
        "uni": "UANDES",
        "title": "Cálculo I (Ing. Civil Química UANDES)",
        "semester": 2,
        "base": ["calculo-diferencial", "calculo-integral"],
        "prereqs": ["uandes-ing-civil-quimica-introduccion-al-calculo"],
        "match": "alto",
        "axes": [],
        "notes": "Derivadas + integrales + técnicas + aplicaciones. Malla nueva 2026.",
    },
    {
        "id": "uandes-ing-civil-quimica-algebra-lineal",
        "uni": "UANDES",
        "title": "Álgebra Lineal (Ing. Civil Química UANDES)",
        "semester": 2,
        "base": ["algebra-lineal"],
        "prereqs": ["uandes-ing-civil-quimica-introduccion-al-algebra-y-geometria"],
        "match": "alto",
        "axes": [],
        "notes": "Malla nueva 2026.",
    },
    {
        "id": "uandes-ing-civil-quimica-calculo-ii",
        "uni": "UANDES",
        "title": "Cálculo II (Ing. Civil Química UANDES)",
        "semester": 3,
        "base": ["calculo-multivariable", "calculo-vectorial"],
        "prereqs": ["uandes-ing-civil-quimica-calculo-i", "uandes-ing-civil-quimica-algebra-lineal"],
        "match": "alto",
        "axes": [],
        "notes": "Varias variables + coordenadas curvilíneas. Malla nueva 2026.",
    },
    {
        "id": "uandes-ing-civil-quimica-ecuaciones-diferenciales",
        "uni": "UANDES",
        "title": "Ecuaciones Diferenciales (Ing. Civil Química UANDES)",
        "semester": 3,
        "base": ["ecuaciones-diferenciales"],
        "prereqs": ["uandes-ing-civil-quimica-calculo-i"],
        "match": "alto",
        "axes": [],
        "notes": "Malla nueva 2026.",
    },
    {
        "id": "uandes-ing-comercial-algebra",
        "uni": "UANDES",
        "title": "Álgebra (Ing. Comercial UANDES)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Conjuntos y lógica",
            "Números reales (desigualdades, valor absoluto)",
            "Polinomios (raíces, fracciones parciales)",
            "Álgebra finita (sumatorias, progresiones, factorial, binomio)",
            "Matrices y determinantes",
            "Sistemas lineales",
        ],
    },
    {
        "id": "uandes-ing-comercial-calculo-i",
        "uni": "UANDES",
        "title": "Cálculo I (Ing. Comercial UANDES)",
        "semester": 2,
        "base": ["calculo-diferencial"],
        "prereqs": ["uandes-ing-comercial-algebra"],
        "match": "alto",
        "axes": [
            "Funciones reales",
            "Límites y continuidad",
            "Derivadas (concepto, reglas, orden superior, implícita)",
            "Aplicaciones (L'Hôpital, máx/mín, concavidad)",
            "Intro a varias variables",
        ],
    },
    {
        "id": "uandes-ing-comercial-optimizacion",
        "uni": "UANDES",
        "title": "Optimización (Ing. Comercial UANDES)",
        "semester": 3,
        "base": ["calculo-multivariable"],
        "prereqs": ["uandes-ing-comercial-calculo-i"],
        "match": "medio",
        "axes": [
            "Optimización de funciones de una y varias variables",
            "Lagrange",
            "Programación lineal (formulación, gráfica)",
            "Simplex",
            "Intro a programación entera",
        ],
        "notes": "PL/simplex específico — material complementario pendiente.",
    },
    {
        "id": "uandes-international-business-algebra-critical-thinking",
        "uni": "UANDES",
        "title": "Álgebra y Critical Thinking (International Business UANDES)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "medio",
        "axes": [],
        "notes": "Pensamiento analítico + álgebra aplicada a negocios + funciones básicas. Bilingüe.",
    },
    {
        "id": "uandes-international-business-calculo-quantitative-methods",
        "uni": "UANDES",
        "title": "Cálculo / Quantitative Methods (International Business UANDES)",
        "semester": 2,
        "base": ["calculo-diferencial"],
        "prereqs": ["uandes-international-business-algebra-critical-thinking"],
        "match": "medio",
        "axes": [],
        "notes": "Cálculo diferencial aplicado + optimización + intro varias variables. Bilingüe.",
    },
    {
        "id": "uandes-bachillerato-ing-nivelacion-matematica",
        "uni": "UANDES",
        "title": "Nivelación Matemática (Bachillerato Ing. UANDES)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [],
        "notes": "Razonamiento lógico + álgebra básica + funciones (preparación a Álgebra e Intro al Cálculo).",
    },
    {
        "id": "uandes-bachillerato-icom-nivelacion-matematica",
        "uni": "UANDES",
        "title": "Nivelación Matemática (Bachillerato Ing. Comercial UANDES)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [],
        "notes": "Preparación a Álgebra Ing. Comercial.",
    },

    # ============================================================
    # UCH — Tier 1
    # ============================================================
    # Plan Común FCFM
    {
        "id": "uch-plan-comun-fcfm-ma1001-introduccion-al-calculo",
        "uni": "UCH",
        "title": "MA1001 Introducción al Cálculo (Plan Común FCFM)",
        "code": "MA1001",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Números reales (igualdad, orden, valor absoluto, inecuaciones lineales/cuadráticas, factorización)",
            "Geometría analítica (cartesiano, rectas, circunferencias, parábolas, elipses, hipérbolas, excentricidad)",
            "Funciones de una variable (definición, dominio, paridad, crecimiento, composición, inyectividad, inversas)",
            "Trigonometría (funciones, identidades, ecuaciones)",
            "Límites (de sucesiones, de funciones, asíntotas)",
            "Derivadas (definición, reglas básicas — introducción)",
        ],
        "notes": "Introduce límites/derivadas rigurosamente al final.",
    },
    {
        "id": "uch-plan-comun-fcfm-ma1101-introduccion-al-algebra",
        "uni": "UCH",
        "title": "MA1101 Introducción al Álgebra (Plan Común FCFM)",
        "code": "MA1101",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "medio",
        "axes": [
            "Conjuntos (potencia, particiones, álgebra, cuantificadores)",
            "Funciones (definición formal, composición)",
            "Relaciones (propiedades, conjunto cociente, división entera)",
            "Relaciones de orden",
            "Axiomas de cuerpos (campos), campos ordenados",
            "Números reales (axioma del supremo, completitud)",
            "Conjuntos finitos e infinitos, cardinalidad",
            "Números complejos (operaciones, polar, raíces)",
        ],
        "notes": "Falta rigor axiomático en el base. Material complementario obligatorio sobre demostraciones, relaciones y cardinalidad.",
    },
    {
        "id": "uch-plan-comun-fcfm-ma1002-calculo-diferencial-e-integral",
        "uni": "UCH",
        "title": "MA1002 Cálculo Diferencial e Integral (Plan Común FCFM)",
        "code": "MA1002",
        "semester": 2,
        "base": ["calculo-diferencial", "calculo-integral"],
        "prereqs": ["uch-plan-comun-fcfm-ma1001-introduccion-al-calculo"],
        "match": "alto",
        "axes": [
            "Continuidad (subsucesiones, convergencia, discontinuidades, álgebra, TVI, Weierstrass, continuidad uniforme)",
            "Derivadas (diferenciabilidad formal, reglas, derivada de la inversa, teoremas del valor medio)",
            "Aplicaciones (máx/mín, análisis, L'Hôpital, Taylor orden 1)",
            "Integrales (primitivas, TFC 1° y 2°, sustitución, partes, fracciones parciales, sust. trigonométrica)",
            "Aplicaciones de la integral (áreas, volúmenes de revolución, centros de masa)",
            "Series de potencias (derivadas e integrales de funciones no elementales)",
            "Curvas en el espacio (longitud, curvatura, torsión)",
        ],
    },
    {
        "id": "uch-plan-comun-fcfm-ma1102-algebra-lineal",
        "uni": "UCH",
        "title": "MA1102 Álgebra Lineal (Plan Común FCFM)",
        "code": "MA1102",
        "semester": 2,
        "base": ["algebra-lineal"],
        "prereqs": [
            "uch-plan-comun-fcfm-ma1101-introduccion-al-algebra",
            "uch-plan-comun-fcfm-ma1001-introduccion-al-calculo",
        ],
        "match": "alto",
        "axes": [
            "Matrices y sistemas (operaciones, particulares/elementales/triangulares, escalonamiento, Gauss, inversa, factorización LU)",
            "Espacios vectoriales (subespacios, independencia, generadores, base, dimensión, suma directa)",
            "Geometría lineal en Rⁿ (vectores, rectas, planos, paramétricas/cartesianas, producto interno, norma, producto cruz, proyecciones ortogonales)",
            "Transformaciones lineales (núcleo, imagen, teorema núcleo-imagen, matriz representante, rango, cambio de base)",
            "Valores y vectores propios (determinante, polinomio característico, diagonalización)",
            "Ortogonalidad (Gram-Schmidt, matrices simétricas, formas cuadráticas, cónicas, mínimos cuadrados, Jacobiana)",
        ],
        "notes": "Match directo y completo. Factorización LU como contenido extra.",
    },
    {
        "id": "uch-plan-comun-fcfm-ma2001-calculo-en-varias-variables",
        "uni": "UCH",
        "title": "MA2001 Cálculo en Varias Variables (Plan Común FCFM)",
        "code": "MA2001",
        "semester": 3,
        "base": ["calculo-multivariable"],
        "prereqs": [
            "uch-plan-comun-fcfm-ma1002-calculo-diferencial-e-integral",
            "uch-plan-comun-fcfm-ma1102-algebra-lineal",
        ],
        "match": "alto",
        "axes": [
            "Topología en Rⁿ (distancias, normas, bolas, sucesiones, abiertos/cerrados/compactos)",
            "Funciones de varias variables (grafos, conjuntos de nivel, límites, continuidad)",
            "Cálculo diferencial en Rⁿ (direccionales, parciales, Fréchet, Jacobiana, regla de la cadena, gradiente, plano tangente)",
            "Teoremas función inversa e implícita, punto fijo",
            "Derivadas de orden superior (Schwartz, Hessiana, Taylor multivariable)",
            "Máx/mín (puntos críticos, 2do orden, convexas, Lagrange)",
            "Integral de Riemann en Rⁿ (particiones, propiedades)",
            "Fubini, cambio de variables (iteradas, polares, cilíndricas, esféricas, centros de masa, momentos de inercia)",
        ],
        "notes": "Agrega topología formal + función inversa/implícita respecto al base.",
    },
    {
        "id": "uch-plan-comun-fcfm-ma2601-ecuaciones-diferenciales-ordinarias",
        "uni": "UCH",
        "title": "MA2601 Ecuaciones Diferenciales Ordinarias (Plan Común FCFM)",
        "code": "MA2601",
        "semester": 3,
        "base": ["ecuaciones-diferenciales"],
        "prereqs": [
            "uch-plan-comun-fcfm-ma1002-calculo-diferencial-e-integral",
            "uch-plan-comun-fcfm-ma1102-algebra-lineal",
        ],
        "match": "alto",
        "axes": [
            "EDO 1er orden (campo vectorial, curva integral, separables, reducción de orden, homogéneas, lineales con factor integrante, Bernoulli, Ricatti, modelación, existencia y unicidad, Runge-Kutta)",
            "Ecuaciones lineales de orden superior (Wronskiano, orden 2 homogéneas/vibraciones mecánicas, variación de parámetros, Función de Green, condiciones de borde, series de potencias / Frobenius, orden n homogéneas/no homogéneas, Euler-Cauchy, coef. indeterminados)",
            "Transformada de Laplace (definición, fórmulas, ED lineales, convolución, Heaviside, Delta de Dirac)",
            "Sistemas lineales (existencia/unicidad, matriz fundamental, exponencial, asintótico, diagramas de fase 2×2, variación de parámetros)",
            "Sistemas autónomos no lineales (hamiltonianos, conservación de energía, péndulo no lineal, estabilidad puntos críticos, Lotka-Volterra, Lyapunov)",
        ],
        "notes": "~75% del programa cubierto. Material complementario: sistemas no lineales, Lyapunov, diagramas de fase, Runge-Kutta.",
    },
    {
        "id": "uch-plan-comun-fcfm-ma2002-calculo-avanzado-y-aplicaciones",
        "uni": "UCH",
        "title": "MA2002 Cálculo Avanzado y Aplicaciones (Plan Común FCFM)",
        "code": "MA2002",
        "semester": 4,
        "base": ["calculo-vectorial"],
        "prereqs": [
            "uch-plan-comun-fcfm-ma2601-ecuaciones-diferenciales-ordinarias",
            "uch-plan-comun-fcfm-ma2001-calculo-en-varias-variables",
        ],
        "match": "medio",
        "axes": [
            "Cálculo vectorial (campos escalares/vectoriales, gradiente, sistemas coordenados ortogonales, divergencia, rotor, Laplaciano, integrales de línea y superficie)",
            "Teoremas de integración vectorial (Gauss, Green, Stokes, conservativos, circulaciones, flujos)",
            "Variable compleja (derivada compleja, Cauchy-Riemann, series de potencias, Laurent, polos, residuos, integrales complejas)",
            "Series y Transformada de Fourier (funciones periódicas, coeficientes, convergencia, transformada, convolución, pares/impares)",
        ],
        "notes": "~40% cubierto. Variable compleja y Fourier NO están en catálogo Se Remonta — material extenso a grabar.",
    },
    # FEN — Métodos Matemáticos (fusionados)
    {
        "id": "uch-fen-metodos-matematicos-i",
        "uni": "UCH",
        "title": "Métodos Matemáticos I (FEN UCh)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Lógica y proposiciones (lógica proposicional, álgebra de proposiciones)",
            "Conjuntos (operaciones)",
            "Inecuaciones y valor absoluto",
            "Geometría analítica (casos aplicados)",
            "Funciones (definiciones, composición, inversas)",
            "Sumatorias (definiciones, inducción, fracciones parciales, combinatoria)",
            "Límites (introducción)",
            "Derivadas (definición, álgebra, funciones elementales)",
        ],
        "alt_slugs": [
            "uch-icom-fen-metodos-matematicos-i",
            "uch-iicg-fen-metodos-matematicos-i",
            "uch-contador-fen-metodos-matematicos-i",
        ],
        "notes": "Dictado en Ing. Comercial, IICG y Contador Auditor (FEN).",
    },
    {
        "id": "uch-fen-metodos-matematicos-ii",
        "uni": "UCH",
        "title": "Métodos Matemáticos II (FEN UCh)",
        "semester": 2,
        "base": ["calculo-diferencial", "algebra-lineal"],
        "prereqs": ["uch-fen-metodos-matematicos-i"],
        "match": "medio",
        "axes": [
            "Funciones multivariadas y derivadas",
            "Métodos de derivación con restricciones",
            "Álgebra lineal (matrices y operaciones)",
            "Metodologías aplicadas",
        ],
        "alt_slugs": [
            "uch-icom-fen-metodos-matematicos-ii",
            "uch-iicg-fen-metodos-matematicos-ii",
            "uch-contador-fen-metodos-matematicos-ii",
        ],
        "notes": "Curso híbrido — mezcla derivación multivariada + álgebra lineal. Dictado en Ing. Comercial, IICG y Contador Auditor.",
    },
    {
        "id": "uch-fen-metodos-matematicos-iii",
        "uni": "UCH",
        "title": "Métodos Matemáticos III (FEN UCh)",
        "semester": 3,
        "base": ["calculo-diferencial"],
        "prereqs": ["uch-fen-metodos-matematicos-ii"],
        "match": "medio",
        "axes": [
            "Derivadas y aplicaciones",
            "Optimización con y sin restricciones",
            "Programación lineal (PPL)",
            "Método simplex",
        ],
        "alt_slugs": [
            "uch-icom-fen-metodos-matematicos-iii",
            "uch-iicg-fen-metodos-matematicos-iii",
            "uch-contador-fen-metodos-matematicos-iii",
        ],
        "notes": "PPL/simplex no cubierto en el base — material complementario pendiente. Dictado en Ing. Comercial, IICG y Contador Auditor.",
    },
    {
        "id": "uch-iicg-fen-metodos-matematicos-iv",
        "uni": "UCH",
        "title": "Métodos Matemáticos IV (IICG FEN UCh)",
        "semester": 4,
        "base": ["calculo-diferencial", "calculo-integral"],
        "prereqs": ["uch-fen-metodos-matematicos-iii"],
        "match": "medio",
        "axes": [
            "Métodos cuantitativos avanzados",
            "Integrales y aplicaciones",
            "Modelos matemáticos para gestión",
        ],
        "notes": "Sólo dictado en IICG.",
    },
    # Lic. Matemática / Lic. Física / Pedagogía Mat-Fís (fusionados — comparten estructura)
    {
        "id": "uch-ciencias-calculo-i",
        "uni": "UCH",
        "title": "Cálculo I (Lic. Mat / Lic. Fís / Pedagogía Mat-Fís UCh)",
        "semester": 1,
        "base": ["precalculo", "calculo-diferencial"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Números reales",
            "Funciones",
            "Límites",
            "Continuidad",
            "Derivadas",
            "Aplicaciones",
        ],
        "alt_slugs": [
            "uch-lic-matematica-calculo-i",
            "uch-lic-fisica-calculo-i",
            "uch-pedagogia-mat-fis-calculo-i",
        ],
        "notes": "Comparten estructura entre las 3 carreras según doc.",
    },
    {
        "id": "uch-ciencias-algebra-i",
        "uni": "UCH",
        "title": "Álgebra I (Lic. Mat / Lic. Fís / Pedagogía Mat-Fís UCh)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "medio",
        "axes": [
            "Lógica",
            "Conjuntos",
            "Relaciones",
            "Funciones",
            "Números (naturales, enteros, racionales, reales, complejos)",
        ],
        "alt_slugs": [
            "uch-lic-matematica-algebra-i",
            "uch-lic-fisica-algebra-i",
            "uch-pedagogia-mat-fis-algebra-i",
        ],
        "notes": "Curso teórico — material complementario sobre demostraciones y rigor.",
    },
    {
        "id": "uch-ciencias-calculo-ii",
        "uni": "UCH",
        "title": "Cálculo II (Lic. Mat / Lic. Fís / Pedagogía Mat-Fís UCh)",
        "semester": 2,
        "base": ["calculo-integral"],
        "prereqs": ["uch-ciencias-calculo-i"],
        "match": "alto",
        "axes": [
            "Integrales",
            "Técnicas",
            "Series",
            "Aplicaciones",
        ],
        "alt_slugs": [
            "uch-lic-matematica-calculo-ii",
            "uch-lic-fisica-calculo-ii",
            "uch-pedagogia-mat-fis-calculo-ii",
        ],
    },
    {
        "id": "uch-ciencias-algebra-lineal",
        "uni": "UCH",
        "title": "Álgebra Lineal (Lic. Mat / Lic. Fís / Pedagogía Mat-Fís UCh)",
        "semester": 2,
        "base": ["algebra-lineal"],
        "prereqs": ["uch-ciencias-algebra-i"],
        "match": "alto",
        "axes": [
            "Matrices",
            "Sistemas",
            "Espacios vectoriales",
            "Transformaciones lineales",
            "Valores propios",
        ],
        "alt_slugs": [
            "uch-lic-matematica-algebra-lineal",
            "uch-lic-fisica-algebra-lineal",
            "uch-pedagogia-mat-fis-algebra-lineal",
        ],
    },
    {
        "id": "uch-ciencias-calculo-iii-varias-variables",
        "uni": "UCH",
        "title": "Cálculo III en Varias Variables (Lic. Mat / Lic. Fís UCh)",
        "semester": 3,
        "base": ["calculo-multivariable"],
        "prereqs": ["uch-ciencias-calculo-ii"],
        "match": "alto",
        "axes": [
            "Funciones de varias variables",
            "Derivadas parciales",
            "Integrales múltiples",
            "Lagrange",
        ],
        "alt_slugs": [
            "uch-lic-matematica-calculo-iii-varias-variables",
            "uch-lic-fisica-calculo-iii",
        ],
        "notes": "Pedagogía Mat-Fís no incluye este ramo según doc.",
    },
    {
        "id": "uch-ciencias-ecuaciones-diferenciales",
        "uni": "UCH",
        "title": "Ecuaciones Diferenciales (Lic. Mat / Lic. Fís UCh)",
        "semester": 4,
        "base": ["ecuaciones-diferenciales"],
        "prereqs": ["uch-ciencias-calculo-iii-varias-variables"],
        "match": "alto",
        "axes": [
            "EDO",
            "Métodos de resolución",
            "Laplace",
            "Sistemas",
        ],
        "alt_slugs": [
            "uch-lic-matematica-ecuaciones-diferenciales",
            "uch-lic-fisica-ecuaciones-diferenciales",
        ],
    },

    # ============================================================
    # UDD — Tier 2
    # ============================================================
    {
        "id": "udd-plan-comun-algebra",
        "uni": "UDD",
        "title": "Álgebra (Plan Común UDD)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Conjuntos y lógica",
            "Números reales (axiomas, desigualdades, valor absoluto)",
            "Polinomios (operaciones, división sintética, raíces)",
            "Álgebra finita (sumatorias, progresiones, factorial, binomio)",
            "Matrices y determinantes",
            "Sistemas de ecuaciones lineales (Gauss-Jordan)",
        ],
        "alt_slugs": ["udd-geologia-algebra"],
        "notes": "Mismo programa también en Geología.",
    },
    {
        "id": "udd-plan-comun-introduccion-al-calculo",
        "uni": "UDD",
        "title": "Introducción al Cálculo (Plan Común UDD)",
        "semester": 1,
        "base": ["precalculo", "calculo-diferencial"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Funciones reales",
            "Función lineal/cuadrática/potencia/exp/log",
            "Trigonométricas",
            "Límites (def, propiedades, laterales)",
            "Continuidad",
            "Introducción a derivada",
        ],
        "alt_slugs": ["udd-geologia-introduccion-al-calculo"],
        "notes": "Mismo programa también en Geología.",
    },
    {
        "id": "udd-plan-comun-geometria",
        "uni": "UDD",
        "title": "Geometría (Plan Común UDD)",
        "semester": 2,
        "base": ["precalculo"],
        "prereqs": ["udd-plan-comun-algebra"],
        "match": "medio",
        "axes": [
            "Geometría analítica plana (rectas, circunferencias, cónicas)",
            "Vectores en R² y R³",
            "Rectas y planos en el espacio",
            "Números complejos (binomial, polar, exponencial)",
            "Trigonometría avanzada",
        ],
        "alt_slugs": ["udd-geologia-geometria"],
        "notes": "Faltan complejos avanzados y vectores 3D en el base.",
    },
    {
        "id": "udd-plan-comun-calculo-diferencial",
        "uni": "UDD",
        "title": "Cálculo Diferencial (Plan Común UDD)",
        "semester": 2,
        "base": ["calculo-diferencial"],
        "prereqs": ["udd-plan-comun-introduccion-al-calculo"],
        "match": "alto",
        "axes": [
            "Derivadas (def, reglas)",
            "Implícita y logarítmica",
            "TVM, Rolle, L'Hôpital",
            "Aplicaciones (máx/mín, concavidad, inflexión)",
            "Análisis y graficación",
            "Diferenciales y aproximaciones",
        ],
        "alt_slugs": ["udd-geologia-calculo-diferencial"],
        "notes": "Existe curso UDD Cálculo Diferencial Ing. Civil con 58 mód en Se Remonta (referencia).",
    },
    {
        "id": "udd-plan-comun-algebra-lineal",
        "uni": "UDD",
        "title": "Álgebra Lineal (Plan Común UDD)",
        "semester": 3,
        "base": ["algebra-lineal"],
        "prereqs": ["udd-plan-comun-algebra"],
        "match": "alto",
        "axes": [
            "Matrices y sistemas (Gauss, Cramer)",
            "Planos y rectas (variedades lineales R², R³)",
            "Espacios vectoriales (subespacio, indep. lineal, base, dimensión)",
            "Producto interior, Gram-Schmidt",
            "Transformaciones lineales (núcleo, imagen, teorema de dimensión)",
            "Valores/vectores propios, diagonalización",
        ],
    },
    {
        "id": "udd-plan-comun-calculo-integral",
        "uni": "UDD",
        "title": "Cálculo Integral (Plan Común UDD)",
        "semester": 3,
        "base": ["calculo-integral"],
        "prereqs": ["udd-plan-comun-calculo-diferencial"],
        "match": "alto",
        "axes": [
            "Antiderivadas e integral indefinida",
            "Técnicas (sustitución, partes, fracciones parciales, trigonométricas)",
            "Integral definida y TFC",
            "Aplicaciones (áreas, volúmenes, longitud)",
            "Integrales impropias",
            "Sucesiones y series numéricas",
        ],
        "alt_slugs": ["udd-geologia-calculo-integral"],
        "notes": "Existe curso UDD Cálculo Integral Ing. Civil con 37 mód en Se Remonta (referencia).",
    },
    {
        "id": "udd-plan-comun-calculo-multivariable",
        "uni": "UDD",
        "title": "Cálculo Multivariable (Plan Común UDD)",
        "semester": 4,
        "base": ["calculo-multivariable", "calculo-vectorial"],
        "prereqs": ["udd-plan-comun-calculo-integral", "udd-plan-comun-algebra-lineal"],
        "match": "alto",
        "axes": [
            "Funciones de varias variables",
            "Derivadas parciales, gradiente, direccionales",
            "Máx/mín",
            "Lagrange",
            "Integrales dobles y triples",
            "Cambio de coordenadas (polares, cilíndricas, esféricas)",
        ],
    },
    {
        "id": "udd-plan-comun-ecuaciones-diferenciales",
        "uni": "UDD",
        "title": "Ecuaciones Diferenciales (Plan Común UDD)",
        "semester": 4,
        "base": ["ecuaciones-diferenciales"],
        "prereqs": ["udd-plan-comun-calculo-integral"],
        "match": "alto",
        "axes": [
            "EDO 1er orden (separables, lineales, exactas, Bernoulli)",
            "EDO 2do orden (coef. constantes, variación de parámetros)",
            "Laplace",
            "Sistemas",
            "Aplicaciones",
        ],
        "alt_slugs": ["udd-geologia-ecuaciones-diferenciales"],
        "notes": "Mismo programa también en Geología (S5 en lugar de S4).",
    },
    {
        "id": "udd-ing-comercial-algebra",
        "uni": "UDD",
        "title": "Álgebra (Ing. Comercial UDD)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Conjuntos (Venn, cardinalidad)",
            "Álgebra en reales (desigualdades, inecuaciones, valor absoluto)",
            "Polinomios (división sintética, raíces, fracciones parciales)",
            "Álgebra finita (sumatorias, progresiones, factorial, combinatorio, binomio)",
            "Matrices y determinantes",
            "Sistemas lineales",
        ],
        "alt_slugs": ["udd-gba-algebra", "udd-bachillerato-ic-algebra"],
        "notes": "Mismo programa también en Global Business Administration y Bachillerato Ing. Comercial.",
    },
    {
        "id": "udd-ing-comercial-calculo",
        "uni": "UDD",
        "title": "Cálculo (Ing. Comercial UDD)",
        "semester": 2,
        "base": ["calculo-diferencial", "calculo-multivariable"],
        "prereqs": ["udd-ing-comercial-algebra"],
        "match": "alto",
        "axes": [
            "Relaciones y funciones reales",
            "Límites y continuidad",
            "Derivadas (concepto, reglas, orden superior, implícita, diferenciales)",
            "Aplicaciones (L'Hôpital, máx/mín, concavidad)",
            "Funciones de varias variables (parciales, Cobb-Douglas, Hessiano, Lagrange)",
        ],
        "alt_slugs": ["udd-gba-calculo"],
        "notes": "Existe Cálculo I UDD Ing. Comercial 47 mód y Cálculo II UDD Ing. Comercial 33 mód en Se Remonta (referencia). Mismo programa también en GBA.",
    },
    {
        "id": "udd-ncd-matematica-avanzada",
        "uni": "UDD",
        "title": "Matemática Avanzada (Negocios y Ciencia de Datos UDD)",
        "semester": 1,
        "base": ["precalculo", "calculo-diferencial", "algebra-lineal"],
        "prereqs": [],
        "match": "medio",
        "axes": [
            "Álgebra y funciones para datos",
            "Cálculo aplicado",
            "Álgebra lineal básica",
        ],
        "notes": "Requiere selección de chapters específicos del base. Carrera nueva 2026.",
    },
    {
        "id": "udd-biomedicina-matematica-aplicada-i",
        "uni": "UDD",
        "title": "Matemática Aplicada I (Ing. Civil en BioMedicina UDD)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "medio",
        "axes": ["Fundamentos", "Funciones"],
        "notes": "Carrera nueva 2025.",
    },
    {
        "id": "udd-biomedicina-matematica-aplicada-ii",
        "uni": "UDD",
        "title": "Matemática Aplicada II (Ing. Civil en BioMedicina UDD)",
        "semester": 2,
        "base": ["calculo-diferencial"],
        "prereqs": ["udd-biomedicina-matematica-aplicada-i"],
        "match": "medio",
        "axes": ["Cálculo diferencial aplicado a biomedicina"],
        "notes": "Carrera nueva 2025.",
    },
    {
        "id": "udd-biomedicina-matematica-aplicada-iii",
        "uni": "UDD",
        "title": "Matemática Aplicada III (Ing. Civil en BioMedicina UDD)",
        "semester": 3,
        "base": ["calculo-diferencial", "calculo-integral", "algebra-lineal"],
        "prereqs": ["udd-biomedicina-matematica-aplicada-ii"],
        "match": "medio",
        "axes": ["Cálculo integral", "Álgebra lineal aplicada"],
        "notes": "Carrera nueva 2025.",
    },
    {
        "id": "udd-biomedicina-matematica-aplicada-iv",
        "uni": "UDD",
        "title": "Matemática Aplicada IV (Ing. Civil en BioMedicina UDD)",
        "semester": 4,
        "base": ["ecuaciones-diferenciales", "calculo-multivariable"],
        "prereqs": ["udd-biomedicina-matematica-aplicada-iii"],
        "match": "medio",
        "axes": ["Ecuaciones diferenciales", "Métodos numéricos aplicados"],
        "notes": "Carrera nueva 2025.",
    },
    {
        "id": "udd-quimica-farmacia-matematicas",
        "uni": "UDD",
        "title": "Matemáticas (Química y Farmacia UDD)",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "medio",
        "axes": [
            "Álgebra",
            "Funciones",
            "Ecuaciones",
            "Trigonometría básica",
        ],
        "notes": "Carrera nueva 2025.",
    },
    {
        "id": "udd-quimica-farmacia-calculo",
        "uni": "UDD",
        "title": "Cálculo (Química y Farmacia UDD)",
        "semester": 2,
        "base": ["calculo-diferencial"],
        "prereqs": ["udd-quimica-farmacia-matematicas"],
        "match": "medio",
        "axes": [
            "Límites",
            "Derivadas",
            "Integrales aplicadas",
        ],
        "notes": "Carrera nueva 2025.",
    },

    # ============================================================
    # UTFSM — Tier 2
    # ============================================================
    {
        "id": "utfsm-plan-comun-ing-civil-mate10-algebra-y-geometria",
        "uni": "UTFSM",
        "title": "MATE10 Álgebra y Geometría (Plan Común Ing. Civil UTFSM)",
        "code": "MATE10",
        "semester": 1,
        "base": ["precalculo"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Fundamentos del Lenguaje Matemático (lógica, conjuntos, álgebra de reales, geometría escolar)",
            "Trigonometría del triángulo (ángulos, razones, identidades, teoremas seno/coseno, modelación)",
            "Geometría Analítica (cartesiano, recta, cónicas centradas y trasladadas)",
            "Polinomios (números complejos, álgebra de polinomios, división, raíces, multiplicidad, teoremas)",
            "Inducción Matemática (principio, sumatoria, factorial, progresiones aritméticas y geométricas, binomio, combinatoria)",
        ],
        "alt_slugs": ["utfsm-ing-comercial-mate10-algebra-y-geometria"],
        "notes": "~85% cubierto. Texto guía: Zill, Dewar & Watson — Álgebra y Trigonometría (McGraw-Hill). Material complementario: inducción matemática y geometría escolar formal. Mismo programa también en Ing. Comercial.",
    },
    {
        "id": "utfsm-plan-comun-ing-civil-mat070-introduccion-al-calculo",
        "uni": "UTFSM",
        "title": "MAT070 Introducción al Cálculo (Plan Común Ing. Civil UTFSM)",
        "code": "MAT070",
        "semester": 1,
        "base": ["precalculo", "calculo-diferencial"],
        "prereqs": [],
        "match": "alto",
        "axes": [
            "Funciones reales (dominio, recorrido, paridad, composición, inyectividad, sobreyectividad, inversas)",
            "Funciones elementales (polinomiales, racionales, trigonométricas, exp, log)",
            "Límites (ε-δ, álgebra, laterales, al infinito, asíntotas)",
            "Continuidad (tipos de discontinuidad, propiedades, TVI)",
            "Derivada (definición como límite, interpretación geométrica, reglas, funciones elementales, regla de la cadena)",
            "Aplicaciones (recta tangente, máx/mín locales, crecimiento, concavidad, análisis introductorio)",
        ],
        "notes": "~80% cubierto.",
    },
    {
        "id": "utfsm-plan-comun-ing-civil-calculo-en-una-variable",
        "uni": "UTFSM",
        "title": "Cálculo en una Variable (Plan Común Ing. Civil UTFSM)",
        "semester": 2,
        "base": ["calculo-diferencial", "calculo-integral"],
        "prereqs": ["utfsm-plan-comun-ing-civil-mat070-introduccion-al-calculo"],
        "match": "alto",
        "axes": [
            "Derivadas (profundización, implícita, orden superior)",
            "Aplicaciones (TVM, L'Hôpital, análisis completo, optimización, aproximación lineal, Taylor)",
            "Integrales (Riemann, TFC 1° y 2°, primitivas)",
            "Técnicas de integración (sustitución, partes, fracciones parciales, sust. trigonométrica)",
            "Aplicaciones de la integral (áreas, volúmenes — discos, arandelas, capas; longitud, centros de masa)",
            "Integrales impropias (convergencia, comparación)",
        ],
        "notes": "~90% cubierto.",
    },
    {
        "id": "utfsm-plan-comun-ing-civil-mate20-algebra-lineal",
        "uni": "UTFSM",
        "title": "MATE20 Álgebra Lineal (Plan Común Ing. Civil UTFSM)",
        "code": "MATE20",
        "semester": 2,
        "base": ["algebra-lineal"],
        "prereqs": ["utfsm-plan-comun-ing-civil-mate10-algebra-y-geometria"],
        "match": "alto",
        "axes": [
            "Matrices y sistemas (nxm, tipos, álgebra, transpuesta, elementales, rango, escalonamiento, inversa, determinantes, adjunta, Cramer)",
            "Geometría Vectorial (vectores plano/espacio, producto punto/cruz, proyecciones, rectas y planos)",
            "Espacios Vectoriales (estructura, subespacios, espacio generado, independencia, base, dimensión, producto interior, ortogonalidad, Gram-Schmidt, bases ortonormales)",
            "Transformaciones Lineales (núcleo, imagen, matriz asociada)",
            "Valores y Vectores Propios (operadores, diagonalización, formas lineales/bilineales/cuadráticas)",
        ],
        "alt_slugs": ["utfsm-ing-comercial-mate20-algebra-lineal"],
        "notes": "~95% cubierto. Texto guía: Poole — Álgebra Lineal (Cengage, 4ª ed.). Mismo programa también en Ing. Comercial.",
    },
    {
        "id": "utfsm-plan-comun-ing-civil-calculo-en-varias-variables",
        "uni": "UTFSM",
        "title": "Cálculo en Varias Variables (Plan Común Ing. Civil UTFSM)",
        "semester": 3,
        "base": ["calculo-multivariable"],
        "prereqs": [
            "utfsm-plan-comun-ing-civil-calculo-en-una-variable",
            "utfsm-plan-comun-ing-civil-mate20-algebra-lineal",
        ],
        "match": "alto",
        "axes": [
            "Topología en Rⁿ (distancias, normas, abiertos/cerrados — nociones básicas)",
            "Funciones de varias variables (gráficas, conjuntos de nivel, límites, continuidad)",
            "Cálculo diferencial en Rⁿ (parciales, direccionales, gradiente, plano tangente, regla de la cadena)",
            "Máximos y mínimos (puntos críticos, Hessiana, Lagrange)",
            "Integrales múltiples (dobles, triples, Fubini, cambio de variables)",
            "Coordenadas curvilíneas (polares, cilíndricas, esféricas, Jacobiano, centros de masa, momentos)",
        ],
        "notes": "~85% cubierto.",
    },
    {
        "id": "utfsm-plan-comun-ing-civil-ecuaciones-diferenciales-edo-edp",
        "uni": "UTFSM",
        "title": "Ecuaciones Diferenciales (EDO + EDP) (Plan Común Ing. Civil UTFSM)",
        "semester": 3,
        "base": ["ecuaciones-diferenciales"],
        "prereqs": ["utfsm-plan-comun-ing-civil-calculo-en-una-variable"],
        "match": "alto",
        "axes": [
            "EDO 1er orden (separables, lineales, exactas, factor integrante, Bernoulli, existencia y unicidad, modelación)",
            "EDO lineales orden superior (homogéneas/no homogéneas, Wronskiano, coef. constantes, indeterminados, variación de parámetros, Euler-Cauchy)",
            "Transformada de Laplace (definición, propiedades, tabla, ED lineales, Heaviside, Delta, convolución)",
            "Sistemas de ED (lineales, matriz fundamental, métodos)",
            "Introducción a EDP (calor, onda, Laplace, separación de variables, series de Fourier — intro)",
        ],
        "notes": "EDO ~85%, total ~70% por EDP/Fourier. Material complementario: EDP clásicas + Fourier intro.",
    },
    {
        "id": "utfsm-ing-comercial-mate25-calculo-diferencial",
        "uni": "UTFSM",
        "title": "MATE25 Cálculo Diferencial (Ing. Comercial UTFSM)",
        "code": "MATE25",
        "semester": 2,
        "base": ["calculo-diferencial", "calculo-multivariable"],
        "prereqs": ["utfsm-plan-comun-ing-civil-mate10-algebra-y-geometria"],
        "match": "medio",
        "axes": [
            "Derivada (definición, reglas, funciones elementales, cadena)",
            "Aplicaciones (análisis, optimización)",
            "Funciones de varias variables (parciales, gradiente)",
            "Diferenciación multivariable (regla de la cadena)",
            "Optimización con/sin restricciones (Lagrange, aplicaciones económicas)",
        ],
        "notes": "~60% cubierto. Mezcla 1V y varias variables con enfoque económico.",
    },
    {
        "id": "utfsm-ing-comercial-mate26-calculo-integral",
        "uni": "UTFSM",
        "title": "MATE26 Cálculo Integral (Ing. Comercial UTFSM)",
        "code": "MATE26",
        "semester": 3,
        "base": ["calculo-integral", "calculo-diferencial"],
        "prereqs": ["utfsm-ing-comercial-mate25-calculo-diferencial"],
        "match": "medio",
        "axes": [
            "Integral (definida, TFC, primitivas)",
            "Aplicaciones (áreas, volúmenes, economía)",
            "EDO 1er y 2do orden (separables, lineales, coef. constantes)",
            "Integración múltiple (dobles, aplicaciones)",
        ],
        "notes": "~55% cubierto. Agrega EDO básicas e integrales dobles fuera del base.",
    },
    {
        "id": "utfsm-ing-civil-matematica-calculo-avanzado-variable-compleja",
        "uni": "UTFSM",
        "title": "Cálculo Avanzado y Variable Compleja (Ing. Civil Matemática UTFSM)",
        "semester": 4,
        "base": ["calculo-vectorial"],
        "prereqs": ["utfsm-plan-comun-ing-civil-calculo-en-varias-variables"],
        "match": "medio",
        "axes": [
            "Cálculo vectorial (campos, integrales de línea/superficie, Green, Stokes, divergencia)",
            "Series de Fourier (coeficientes, convergencia, transformada)",
            "Variable compleja (analíticas, Cauchy-Riemann, Laurent, residuos)",
        ],
        "notes": "~40% cubierto. Variable compleja + Fourier fuera de catálogo Remy.",
    },
]


# ============================================================
# Implementación
# ============================================================
def now_iso():
    return datetime.now(timezone.utc).isoformat()


async def upsert_university(db, uni_spec):
    """Create-only por seguridad en prod:
    - Si la universidad ya existe (por short_name), NO la toca, salvo añadir
      `tier` si está vacío (campo nuevo del schema). Nombre, logo, is_active,
      etc. se respetan tal cual los dejó el admin.
    - Si no existe, la crea con tier y is_active=True.
    Devuelve (id, created)."""
    short = uni_spec["short_name"]
    existing = await db.library_universities.find_one({"short_name": short}, {"_id": 0})
    if existing:
        # Sólo backfill de tier cuando falta — nunca pisamos un tier ya
        # configurado por el admin.
        if existing.get("tier") is None:
            await db.library_universities.update_one(
                {"id": existing["id"]},
                {"$set": {"tier": uni_spec["tier"]}},
            )
        return existing["id"], False
    doc = {
        "id": str(uuid.uuid4()),
        "name": uni_spec["name"],
        "short_name": short,
        "tier": uni_spec["tier"],
        "is_active": True,
        "created_at": now_iso(),
    }
    await db.library_universities.insert_one(doc)
    return doc["id"], True


async def get_base_chapter_ids(db, base_course_id: str) -> list[str]:
    """Devuelve los IDs de chapters templates (los que viven en el curso base)
    ordenados por `order`. Si el curso base no existe aún, devuelve lista vacía
    y el ramo queda sin chapters linkeados (admin podrá completar después)."""
    rows = await db.chapters.find(
        {"course_id": base_course_id, "template_chapter_id": {"$in": [None]}},
        {"_id": 0, "id": 1, "order": 1},
    ).sort("order", 1).to_list(200)
    # MongoDB query con `$in: [None]` no matchea documentos donde el campo
    # simplemente no existe. Tiramos otra query para los que no tienen el campo.
    if not rows:
        rows = await db.chapters.find(
            {"course_id": base_course_id},
            {"_id": 0, "id": 1, "order": 1, "template_chapter_id": 1},
        ).sort("order", 1).to_list(200)
        rows = [r for r in rows if not r.get("template_chapter_id")]
    return [r["id"] for r in rows]


async def link_chapters_to_course(db, course_id: str, template_chapter_ids: list[str]) -> int:
    """Crea chapters linkeados al curso destino (idempotente: skipea los ya
    linkeados a ese template). Devuelve cuántos creó nuevos."""
    if not template_chapter_ids:
        return 0
    # Conseguimos el max order actual del curso destino.
    last = await db.chapters.find_one(
        {"course_id": course_id},
        {"order": 1},
        sort=[("order", -1)],
    )
    next_order = (last.get("order", 0) if last else 0) + 1

    created = 0
    for tch_id in template_chapter_ids:
        # ¿Ya está linkeado?
        already = await db.chapters.find_one(
            {"course_id": course_id, "template_chapter_id": tch_id},
            {"_id": 0, "id": 1},
        )
        if already:
            continue
        template = await db.chapters.find_one({"id": tch_id}, {"_id": 0})
        if not template:
            continue
        new_chapter = {
            "id": str(uuid.uuid4()),
            "course_id": course_id,
            "title": template.get("title", ""),
            "description": template.get("description", ""),
            "order": next_order,
            "template_chapter_id": tch_id,
            "excluded_lesson_ids": [],
            "excluded_question_ids": [],
            "created_at": now_iso(),
        }
        await db.chapters.insert_one(new_chapter)
        created += 1
        next_order += 1
    return created


async def insert_course_axes(db, course_id: str, axes: list[str]):
    """Inserta los ejes textuales del syllabus. Sólo se llama cuando el curso
    se acaba de crear, así que nunca pisa axes ya editados por el admin.
    Idempotente dentro del run: limpia primero los axes huérfanos del curso
    nuevo (no deberían existir si el curso es nuevo) y luego inserta."""
    await db.course_axes.delete_many({"course_id": course_id})
    if not axes:
        return
    docs = [
        {
            "id": str(uuid.uuid4()),
            "course_id": course_id,
            "order": i + 1,
            "text": ax,
            "created_at": now_iso(),
        }
        for i, ax in enumerate(axes)
    ]
    await db.course_axes.insert_many(docs)


async def upsert_ramo(db, ramo: dict, uni_id_by_short: dict) -> tuple[bool, int, int]:
    """Create-only: si el curso ya existe, SE SKIPEA por completo y no se le
    tocan campos, chapters ni axes. Esto protege el contenido que el admin ya
    está curando en producción (DESMOS, imágenes, ediciones de chapters/lessons,
    etc.). Sólo crea ramos cuyo slug NO existe aún.
    Devuelve (created, linked_chapters_count, axes_count)."""
    course_id = ramo["id"]
    existing = await db.courses.find_one({"id": course_id}, {"_id": 0, "id": 1})
    if existing:
        # SKIP completo. No actualizamos campos, no linkeamos chapters
        # adicionales, no tocamos axes. El admin manda en lo ya creado.
        return False, 0, 0

    uni_id = uni_id_by_short[ramo["uni"]]
    match = ramo["match"]
    assert match in ("alto", "medio"), f"match_level inválido en {course_id}: {match}"
    coverage = "complete" if match == "alto" else "partial"

    payload = {
        "id": course_id,
        "title": ramo["title"],
        "description": ramo.get("description") or ramo["title"],
        "category": "Matemáticas",
        "level": "Universitario",
        "modules_count": 0,
        "university_id": uni_id,
        "rating": 4.8,
        "summary": ramo.get("notes") or ramo["title"],
        "code": ramo.get("code"),
        "semester": ramo.get("semester"),
        "prereq_course_ids": ramo.get("prereqs", []),
        "base_course_ids": ramo.get("base", []),
        "match_level": match,
        "source": "split",
        "coverage_status": coverage,
        "notes": ramo.get("notes"),
        "alt_slugs": ramo.get("alt_slugs", []),
        "visible_to_students": True,
        "created_at": now_iso(),
    }
    await db.courses.insert_one(payload)

    # Linkear chapters base — sólo cuando el curso es nuevo. Si ya existía,
    # nunca llegamos acá (return arriba).
    linked = 0
    base_chapter_ids: list[str] = []
    for base_id in ramo.get("base", []):
        base_chapter_ids.extend(await get_base_chapter_ids(db, base_id))
    if base_chapter_ids:
        linked = await link_chapters_to_course(db, course_id, base_chapter_ids)

    # Axes (syllabus textual) — sólo cuando el curso es nuevo.
    axes = ramo.get("axes") or []
    await insert_course_axes(db, course_id, axes)

    return True, linked, len(axes)


async def main():
    print(f"-> Conectando a {os.environ['MONGO_URL']} / DB {os.environ['DB_NAME']}")
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]

    # 1) Universidades
    print("\n== Universidades ==")
    uni_id_by_short: dict[str, str] = {}
    created_unis = 0
    for u in UNIVERSITIES:
        uid, created = await upsert_university(db, u)
        uni_id_by_short[u["short_name"]] = uid
        marker = "+" if created else "="
        print(f"  {marker} {u['short_name']:7s} tier {u['tier']}  -> {uid}")
        if created:
            created_unis += 1

    # 2) Ramos
    print(f"\n== Ramos ({len(RAMOS)} total) ==")
    by_uni: dict[str, dict] = {u["short_name"]: {"created": 0, "skipped": 0, "complete": 0, "partial": 0, "axes": 0, "linked_chapters": 0} for u in UNIVERSITIES}
    bases_missing: set[str] = set()
    duplicates_ids = set()
    seen = set()
    for r in RAMOS:
        if r["id"] in seen:
            duplicates_ids.add(r["id"])
        seen.add(r["id"])
    if duplicates_ids:
        raise RuntimeError(f"IDs duplicados en RAMOS: {duplicates_ids}")

    for ramo in RAMOS:
        # Validar bases existentes (warning, no falla).
        for base in ramo.get("base", []):
            base_doc = await db.courses.find_one({"id": base}, {"_id": 0, "id": 1})
            if not base_doc:
                bases_missing.add(base)
        created, linked, axes = await upsert_ramo(db, ramo, uni_id_by_short)
        bucket = by_uni[ramo["uni"]]
        if created:
            bucket["created"] += 1
            if ramo["match"] == "alto":
                bucket["complete"] += 1
            else:
                bucket["partial"] += 1
            bucket["axes"] += axes
            bucket["linked_chapters"] += linked
            marker = "+"
            print(f"  {marker} {ramo['id']:80s}  match={ramo['match']:5s}  +{linked} ch  {axes} ejes")
        else:
            bucket["skipped"] += 1
            marker = "."
            print(f"  {marker} {ramo['id']:80s}  ya existe, no se toca")

    # 3) Reporte final
    print("\n== Resumen (create-only) ==")
    print(f"  Universidades nuevas: {created_unis} / {len(UNIVERSITIES)} total")
    tot = {"created": 0, "skipped": 0, "complete": 0, "partial": 0, "axes": 0, "linked_chapters": 0}
    for short, b in by_uni.items():
        for k in tot:
            tot[k] += b[k]
        print(
            f"  {short:7s}  created={b['created']:3d}  skipped={b['skipped']:3d}  "
            f"complete={b['complete']:3d}  partial={b['partial']:3d}  "
            f"axes={b['axes']:4d}  linked_chapters={b['linked_chapters']:4d}"
        )
    print(
        f"  TOTAL    created={tot['created']:3d}  skipped={tot['skipped']:3d}  "
        f"complete={tot['complete']:3d}  partial={tot['partial']:3d}  "
        f"axes={tot['axes']:4d}  linked_chapters={tot['linked_chapters']:4d}"
    )

    if bases_missing:
        print()
        print("WARNING: estos cursos base no existen en la DB — ramos quedaron sin chapters linkeados:")
        for b in sorted(bases_missing):
            print(f"  - {b}")
        print(
            "Estos cursos base deberían existir tras correr los seeds de backend/seeds/<curso>/. "
            "Una vez que existan, re-correr este seed crea los links faltantes (idempotente)."
        )

    # Cobertura por endpoint admin (sanity check de lectura)
    courses_with_uni = await db.courses.count_documents({"university_id": {"$ne": None}})
    axes_total = await db.course_axes.count_documents({})
    print(f"\n  Estado actual DB: {courses_with_uni} courses con university_id; {axes_total} ejes totales en course_axes.")

    client.close()
    print("\nOK: seed completado.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
