import { useState } from "react";

// ═══════════════════════════════════════════════════════════════
// DATOS VERIFICADOS - Investigación Ramos Matemáticos UAI
// Fuentes:
//   - Mallas curriculares: PDFs oficiales UAI (uai.cdn7pm.net)
//   - Contenidos de cursos: uclases.cl (plataforma de clases UAI)
//     · Álgebra: uclases.cl/cursos/detalle/78/795
//     · Cálculo Diferencial: uclases.cl/cursos/detalle/655
//     · Cálculo Integral: uclases.cl/cursos/detalle/656/795
//     · Álgebra Lineal: uclases.cl/cursos/detalle/73/795
//     · Cálculo Multivariables: uclases.cl/cursos/detalle/188/795
//     · Ecuaciones Diferenciales: uclases.cl/cursos/detalle/1/795
//     · Mat. Avanzadas I: uclases.cl/cursos/detalle/651/806
//     · Mat. Avanzadas II: uclases.cl/cursos/detalle/1275/794
//   - Syllabus Álgebra Lineal: syllabi.uai.cl
// Fecha de investigación: Abril 2026
// ═══════════════════════════════════════════════════════════════

// ── CATÁLOGO COMPLETO SE REMONTA (cursos generales base) ─────
const seRemontaCursos = [
  // ─── CURSOS GENERALES (base para splitting) ───
  { id: "precalculo-cero", nombre: "Precálculo desde Cero", tipo: "general", modulos: 68, precio: 40000, color: "#8B5CF6",
    contenidos: ["Conjuntos y números", "Álgebra de expresiones", "Ecuaciones e inecuaciones", "Funciones", "Trigonometría", "Geometría analítica"] },
  { id: "nivelacion-ing", nombre: "Nivelación Ingeniería", tipo: "general", modulos: 43, precio: 20000, color: "#7C3AED" },
  { id: "algebra-lineal-gen", nombre: "Álgebra Lineal", tipo: "general", modulos: 52, precio: 40000, color: "#6366F1",
    contenidos: ["Espacio", "Sistemas de Ecuaciones", "Álgebra de Matrices", "Determinantes", "Espacios y Subespacios Vectoriales", "Valores y Vectores Propios", "Ortogonalidad", "Matrices Simétricas"] },
  { id: "calculo-1var-gen", nombre: "Cálculo en una Variable", tipo: "general", modulos: 85, precio: 40000, color: "#3B82F6",
    contenidos: ["Límites y continuidad", "Derivadas", "Aplicaciones de la derivada", "Integrales", "Técnicas de integración", "Aplicaciones de la integral"] },
  { id: "calculo-dif-gen", nombre: "Cálculo Diferencial", tipo: "general", modulos: null, precio: 25000, color: "#0EA5E9" },
  { id: "calculo-int-gen", nombre: "Cálculo Integral", tipo: "general", modulos: null, precio: 25000, color: "#06B6D4" },
  { id: "calculo-vvar-gen", nombre: "Cálculo en Varias Variables", tipo: "general", modulos: 41, precio: 40000, color: "#14B8A6",
    contenidos: ["Funciones de varias variables", "Derivadas parciales y gradiente", "Máximos y mínimos", "Multiplicadores de Lagrange", "Integrales dobles y triples", "Coordenadas curvilíneas"] },
  { id: "calculo-vec-gen", nombre: "Cálculo Vectorial", tipo: "general", modulos: 31, precio: 40000, color: "#10B981" },
  { id: "ec-dif-gen", nombre: "Ecuaciones Diferenciales", tipo: "general", modulos: 42, precio: 40000, color: "#EAB308",
    contenidos: ["EDO primer orden", "EDO segundo orden", "Transformada de Laplace", "Sistemas de ED", "Aplicaciones"] },
];

const carreras = [
  // ═══════════════════════════════════════
  // INGENIERÍA CIVIL PLAN COMÚN
  // ═══════════════════════════════════════
  {
    id: "plan-comun",
    nombre: "Ingeniería Civil Plan Común",
    facultad: "Facultad de Ingeniería y Ciencias",
    duracion: "2 años plan común + 2 años especialización + 1 año titulación",
    especialidades: [
      "Ing. Civil Industrial",
      "Ing. Civil Informática",
      "Ing. Civil en Bioingeniería",
      "Ing. Civil (Obras Civiles)",
      "Ing. Civil en Energía",
      "Ing. Civil Mecánica",
      "Ing. Civil en Minería",
    ],
    mallaUrl: "https://uai.cdn7pm.net/documentos/malla-carrera-ingenieria-civil-industrial.pdf",
    nota: "ABET acreditada (3 especialidades)",
    ramos: [
      {
        nombre: "Álgebra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/78/795",
        contenidos: [
          "Lógica y conjuntos (proposiciones, álgebra de conjuntos, cuantificadores)",
          "Números reales (axiomas, demostraciones, inducción)",
          "Números naturales (sucesiones, progresiones, sumatorias polinómica/telescópica/geométrica, productoria, combinatoria, binomio de Newton)",
          "Trigonometría (funciones, identidades, ecuaciones trigonométricas)",
          "Geometría analítica (vectores, producto punto/cruz, rectas, planos, distancias en el espacio)",
          "Números complejos (operaciones, forma polar, raíces)",
          "Polinomios (división sintética, raíces, teorema del resto, fracciones parciales)",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre conjuntos, álgebra, funciones, trigonometría, geometría analítica. Nivelación Ingeniería (43 mód) complementa.",
      },
      {
        nombre: "Cálculo Diferencial",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/655",
        contenidos: [
          "Números reales e inecuaciones",
          "Funciones: dominio, recorrido, transformaciones, inyectivas, inversas, polinomiales, exponenciales, logarítmicas",
          "Límites (finitos, al infinito, continuidad, Teorema del Valor Intermedio)",
          "Derivadas: definición, reglas de derivación, derivadas implícitas",
          "Aplicaciones: razón de cambio, máximos y mínimos, Teorema del Valor Medio, L'Hôpital, graficación de funciones",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód) cubre toda la parte diferencial. También Cálculo Diferencial general (25k).",
      },
      {
        nombre: "Cálculo Integral",
        semestre: 2,
        prereqs: "Cálculo Diferencial",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/656/795",
        contenidos: [
          "Antiderivadas, integral indefinida, TFC, sustitución, integración por partes, fracciones parciales, sustitución trigonométrica",
          "Aplicaciones: área entre curvas, volúmenes (discos y cascarones cilíndricos), curvas parametrizadas, coordenadas polares",
          "Integrales impropias (tipo I y II, criterio de comparación)",
          "Sucesiones y series (criterios de convergencia, series de potencias, radio e intervalo, representación de funciones, series de Taylor)",
        ],
        match: ["calculo-1var-gen", "calculo-int-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód) cubre integrales y técnicas. Cálculo Integral general (25k) también aplica.",
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 2,
        prereqs: "Álgebra",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/73/795",
        contenidos: [
          "Matrices y sistemas de ecuaciones lineales (Gauss-Jordan, sistemas homogéneos, matrices por bloques, inversa y elementales)",
          "Determinantes (definición, propiedades)",
          "Espacios y subespacios vectoriales (combinación e independencia lineal, bases, dimensión, coordenadas, cambio de base, subespacios fundamentales)",
          "Transformaciones lineales (definición, kernel e imagen, inyectividad/sobreyectividad, matriz asociada)",
          "Diagonalización (vectores y valores propios, cadenas de Markov)",
          "Análisis vectorial (Gram-Schmidt, complemento ortogonal, proyección ortogonal, mínimos cuadrados)",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal general (52 mód, 8 capítulos) cubre todos los temas. Match directo y completo.",
      },
      {
        nombre: "Cálculo Multivariables",
        semestre: 3,
        prereqs: "Cálculo Integral, Álgebra Lineal",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/188/795",
        contenidos: [
          "Funciones de varias variables (superficies cuadráticas, límites, continuidad, derivadas parciales, diferenciabilidad)",
          "Plano tangente, aproximaciones lineales, regla de la cadena, derivación implícita",
          "Derivadas direccionales, máximos y mínimos, multiplicadores de Lagrange",
          "Integrales dobles (cambio de región, coordenadas polares, masa y centro de masa)",
          "Integrales triples (coordenadas cilíndricas y esféricas, cambios de variable)",
          "Cálculo vectorial (integrales de línea, Green, rotacional, divergencia, integrales de superficie, Stokes, teorema de la divergencia)",
        ],
        match: ["calculo-vvar-gen", "calculo-vec-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre derivadas parciales, Lagrange, integrales múltiples. Cálculo Vectorial (31 mód) cubre integrales de línea, Green, Stokes, divergencia.",
      },
      {
        nombre: "Probabilidad y Estadística",
        semestre: 3,
        prereqs: "Cálculo Integral",
        contenidos: [
          "Probabilidad: axiomas, condicional, Bayes",
          "Variables aleatorias discretas y continuas",
          "Distribuciones de probabilidad (Binomial, Poisson, Normal)",
          "Estimación puntual y por intervalos",
          "Pruebas de hipótesis",
        ],
        match: [],
        matchLevel: "ninguno",
        nota: "Sin fuente de contenido verificada. Contenidos inferidos del estándar de ingeniería.",
      },
      {
        nombre: "Ecuaciones Diferenciales",
        semestre: 4,
        prereqs: "Cálculo Multivariables",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/1/795",
        contenidos: [
          "EDO primer orden (separable, lineal, exacta, factor integrante, homogénea, Bernoulli, Ricatti, reducible a separable)",
          "Modelos con ED de primer orden",
          "ED orden superior (coeficientes constantes, Cauchy-Euler, coeficientes indeterminados, variación de parámetros, masa-resorte)",
          "Sistemas de ecuaciones diferenciales",
          "Transformada de Laplace (propiedades, traslación, escalón unitario, convolución, Delta de Dirac)",
          "Soluciones por series (puntos ordinarios, singulares regulares, Bessel)",
          "Serie de Fourier",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Ecuaciones Diferenciales general (42 mód) cubre EDO 1er y 2do orden, Laplace, sistemas. El curso UAI es más extenso (incluye series de Fourier y Bessel).",
      },
      {
        nombre: "Optimización",
        semestre: 5,
        prereqs: "Álgebra Lineal, Cálculo Multivariables",
        contenidos: [
          "Programación lineal",
          "Método simplex",
          "Dualidad",
          "Programación entera",
          "Optimización no lineal",
        ],
        match: [],
        matchLevel: "ninguno",
        nota: "Sin fuente de contenido verificada. Contenidos inferidos.",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA COMERCIAL - LIC. ADMIN. EMPRESAS
  // ═══════════════════════════════════════
  {
    id: "icom-admin",
    nombre: "Ingeniería Comercial (Lic. Administración de Empresas)",
    facultad: "Escuela de Negocios",
    duracion: "10 semestres (6 licenciatura + 4 magíster + título)",
    mallaUrl: "https://uai.cdn7pm.net/documentos/malla-licenciatura-administracion-de-empresas.pdf",
    ramos: [
      {
        nombre: "Matemáticas Avanzadas I",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/651/806",
        contenidos: [
          "Lógica y conjuntos (proposiciones, álgebra de conjuntos, cuantificadores)",
          "Números naturales y reales (inducción, sucesiones, progresiones, sumatorias polinómica/telescópica/geométrica)",
          "Axiomas de orden, demostraciones, inecuaciones (con valor absoluto), axioma del supremo",
          "Funciones (dominio, imagen, composición, inversas, logaritmo, exponencial, gráficos, modelación)",
          "Matrices y sistemas de ecuaciones lineales (propiedades, Gauss-Jordan, sistemas homogéneos, matrices por bloques, inversa, elementales)",
          "Determinantes (definición, propiedades)",
          "Espacios vectoriales, subespacios, combinación y dependencia lineal",
        ],
        match: ["precalculo-cero", "algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre lógica, conjuntos, funciones, álgebra. Álgebra Lineal (52 mód) cubre matrices, determinantes y espacios vectoriales.",
      },
      {
        nombre: "Matemáticas Avanzadas II",
        semestre: 2,
        prereqs: "Matemáticas Avanzadas I",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/1275/794",
        contenidos: [
          "Sistemas de ecuaciones lineales (repaso)",
          "Límites (normales, trigonométricos, al infinito, laterales, continuidad, teoremas de límites)",
          "Derivadas (definición, reglas de derivación, recta tangente, análisis marginal, derivación implícita)",
          "Aplicaciones de derivadas (extremos, crecimiento/decrecimiento, optimización, L'Hôpital)",
          "Integrales (sustitución, por partes, integrales de Riemann, TFC 1er y 2do)",
          "Aplicaciones integrales (área entre curvas, excedentes, integrales impropias, criterios de convergencia)",
          "Funciones de probabilidad",
        ],
        match: ["calculo-1var-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód) cubre completamente: límites, derivadas, integrales, técnicas, aplicaciones. NO incluye multivariable (verificado en fuente).",
      },
      {
        nombre: "Razonamiento Cuantitativo con Datos I",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Estadística descriptiva",
          "Representación gráfica de datos",
          "Medidas de tendencia central y dispersión",
          "Introducción a probabilidad",
        ],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Razonamiento Cuantitativo con Datos II",
        semestre: 2,
        prereqs: "Razonamiento Cuantitativo con Datos I",
        contenidos: [
          "Variables aleatorias y distribuciones",
          "Estimación e intervalos de confianza",
          "Pruebas de hipótesis",
          "Regresión lineal simple",
        ],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Estadísticas & Data Science",
        semestre: 3,
        prereqs: "Razonamiento Cuantitativo con Datos II",
        contenidos: [
          "Regresión múltiple",
          "Modelos estadísticos avanzados",
          "Introducción a machine learning",
          "Análisis de datos con herramientas computacionales",
        ],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Econometría",
        semestre: 5,
        prereqs: "Estadísticas & Data Science",
        contenidos: [
          "Modelos econométricos",
          "Regresión con variables instrumentales",
          "Series de tiempo",
        ],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA COMERCIAL - LIC. ECONOMÍA
  // ═══════════════════════════════════════
  {
    id: "icom-economia",
    nombre: "Ingeniería Comercial (Lic. Economía)",
    facultad: "Escuela de Negocios",
    duracion: "10 semestres (6 licenciatura + 4 magíster + título)",
    mallaUrl: "https://uai.cdn7pm.net/documentos/malla-licenciatura-economia.pdf",
    nota: "Plan común con Lic. Adm. Empresas en S1-S2",
    ramos: [
      {
        nombre: "Matemáticas Avanzadas I",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/651/806",
        contenidos: [
          "Lógica y conjuntos (proposiciones, álgebra de conjuntos, cuantificadores)",
          "Números naturales y reales (inducción, sucesiones, progresiones, sumatorias polinómica/telescópica/geométrica)",
          "Axiomas de orden, demostraciones, inecuaciones (con valor absoluto), axioma del supremo",
          "Funciones (dominio, imagen, composición, inversas, logaritmo, exponencial, gráficos, modelación)",
          "Matrices y sistemas (propiedades, Gauss-Jordan, sistemas homogéneos, matrices por bloques, inversa, elementales)",
          "Determinantes (definición, propiedades)",
          "Espacios vectoriales, subespacios, combinación y dependencia lineal",
        ],
        match: ["precalculo-cero", "algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre lógica, conjuntos, funciones, álgebra. Álgebra Lineal (52 mód) cubre matrices, determinantes y espacios vectoriales.",
        nota: "Compartido con Lic. Administración de Empresas",
      },
      {
        nombre: "Matemáticas Avanzadas II",
        semestre: 2,
        prereqs: "Matemáticas Avanzadas I",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/1275/794",
        contenidos: [
          "Sistemas de ecuaciones lineales (repaso)",
          "Límites (normales, trigonométricos, al infinito, laterales, continuidad, teoremas)",
          "Derivadas (definición, reglas, recta tangente, análisis marginal, derivación implícita)",
          "Aplicaciones (extremos, optimización, L'Hôpital)",
          "Integrales (sustitución, por partes, Riemann, TFC, área entre curvas, excedentes)",
          "Integrales impropias y criterios de convergencia",
          "Funciones de probabilidad",
        ],
        match: ["calculo-1var-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód) cubre completamente: límites, derivadas, integrales. NO incluye multivariable (verificado en fuente).",
        nota: "Compartido con Lic. Administración de Empresas",
      },
      {
        nombre: "Razonamiento Cuantitativo con Datos I",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Estadística descriptiva, representación gráfica, medidas centrales, introducción probabilidad"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Razonamiento Cuantitativo con Datos II",
        semestre: 2,
        prereqs: "Razonamiento Cuantitativo con Datos I",
        contenidos: ["Variables aleatorias, estimación, hipótesis, regresión simple"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Estadísticas & Data Science",
        semestre: 3,
        prereqs: "Razonamiento Cuantitativo con Datos II",
        contenidos: ["Regresión múltiple, modelos avanzados, ML básico"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Econometría I",
        semestre: 4,
        prereqs: "Estadísticas & Data Science",
        contenidos: ["Modelos econométricos, MCO, supuestos clásicos, multicolinealidad"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Economía Matemática",
        semestre: 4,
        prereqs: "Matemáticas Avanzadas II",
        contenidos: [
          "Optimización estática y dinámica",
          "Teoría de juegos",
          "Modelos de equilibrio",
          "Cálculo de variaciones",
        ],
        match: ["calculo-vvar-gen"],
        matchLevel: "bajo",
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre optimización con Lagrange. Contenido parcial.",
      },
      {
        nombre: "Econometría II",
        semestre: 5,
        prereqs: "Econometría I",
        contenidos: ["Series de tiempo, modelos panel, variables instrumentales avanzado"],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA EN COMPUTER SCIENCE
  // ═══════════════════════════════════════
  {
    id: "computer-science",
    nombre: "Ingeniería en Computer Science",
    facultad: "Facultad de Ingeniería y Ciencias",
    duracion: "11 semestres (8 licenciatura + titulación)",
    mallaUrl: "https://uai.cdn7pm.net/documentos/malla-ingenieria-en-computer-science.pdf",
    nota: "Nueva 2024. Menciones: Data Science o Ciberseguridad",
    ramos: [
      {
        nombre: "Álgebra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/78/795",
        contenidos: [
          "Lógica y conjuntos (proposiciones, álgebra de conjuntos, cuantificadores)",
          "Números reales (axiomas, demostraciones, inducción)",
          "Números naturales (sucesiones, progresiones, sumatorias polinómica/telescópica/geométrica, combinatoria, binomio de Newton)",
          "Trigonometría (funciones, identidades, ecuaciones trigonométricas)",
          "Geometría analítica (vectores, producto punto/cruz, rectas, planos, distancias en el espacio)",
          "Números complejos (operaciones, forma polar, raíces)",
          "Polinomios (división sintética, raíces, teorema del resto, fracciones parciales)",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) + Nivelación Ingeniería (43 mód). Mismo Álgebra que Ing. Civil.",
        nota: "Mismo programa que Álgebra de Ing. Civil Plan Común",
      },
      {
        nombre: "Cálculo Diferencial",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/655",
        contenidos: [
          "Números reales e inecuaciones",
          "Funciones: dominio, recorrido, transformaciones, inyectivas, inversas, polinomiales, exponenciales, logarítmicas",
          "Límites (finitos, al infinito, continuidad, Teorema del Valor Intermedio)",
          "Derivadas: definición, reglas de derivación, derivadas implícitas",
          "Aplicaciones: razón de cambio, máximos y mínimos, Teorema del Valor Medio, L'Hôpital, graficación",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód, parte diferencial) o Cálculo Diferencial gen.",
        nota: "Mismo programa que Cálculo Diferencial de Ing. Civil Plan Común",
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 2,
        prereqs: "Álgebra",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/73/795",
        contenidos: [
          "Matrices y sistemas de ecuaciones lineales (Gauss-Jordan, sistemas homogéneos, matrices por bloques, inversa y elementales)",
          "Determinantes (definición, propiedades)",
          "Espacios y subespacios vectoriales (combinación e independencia lineal, bases, dimensión, coordenadas, cambio de base)",
          "Transformaciones lineales (definición, kernel e imagen, inyectividad/sobreyectividad, matriz asociada)",
          "Diagonalización (vectores y valores propios, cadenas de Markov)",
          "Análisis vectorial (Gram-Schmidt, complemento ortogonal, proyección ortogonal, mínimos cuadrados)",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal general (52 mód) cubre todos los temas. Match directo.",
        nota: "Mismo programa que Álgebra Lineal de Ing. Civil Plan Común",
      },
      {
        nombre: "Cálculo Integral",
        semestre: 2,
        prereqs: "Cálculo Diferencial",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/656/795",
        contenidos: [
          "Antiderivadas, integral indefinida, TFC, sustitución, integración por partes, fracciones parciales, sustitución trigonométrica",
          "Aplicaciones: área entre curvas, volúmenes (discos y cascarones cilíndricos), curvas parametrizadas, coordenadas polares",
          "Integrales impropias (tipo I y II, criterio de comparación)",
          "Sucesiones y series (criterios de convergencia, series de potencias, radio e intervalo, Taylor)",
        ],
        match: ["calculo-1var-gen", "calculo-int-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód, parte integral) o Cálculo Integral gen.",
        nota: "Mismo programa que Cálculo Integral de Ing. Civil Plan Común",
      },
      {
        nombre: "Estadística",
        semestre: 3,
        prereqs: "Cálculo Integral",
        contenidos: [
          "Probabilidad y distribuciones",
          "Estimación e inferencia",
          "Pruebas de hipótesis",
          "Regresión",
        ],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Estructuras Discretas",
        semestre: 3,
        prereqs: "Álgebra",
        contenidos: [
          "Lógica y demostraciones",
          "Combinatoria",
          "Grafos y árboles",
          "Relaciones y funciones discretas",
        ],
        match: [],
        matchLevel: "ninguno",
        nota: "Ramo propio de CS, no tiene equivalente en catálogo Se Remonta.",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA EN NEGOCIOS Y TECNOLOGÍA
  // ═══════════════════════════════════════
  {
    id: "negocios-tech",
    nombre: "Ingeniería en Negocios y Tecnología",
    facultad: "Escuela de Negocios + Fac. Ingeniería",
    duracion: "10 semestres (6 licenciatura + magíster Business Analytics)",
    mallaUrl: "https://uai.cdn7pm.net/documentos/malla-pregrado-ingenieria-en-negocios-y-tecnologia.pdf",
    ramos: [
      {
        nombre: "Álgebra Lineal y Optimización",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Matrices y sistemas lineales",
          "Espacios vectoriales básicos",
          "Introducción a optimización lineal",
          "Aplicaciones a negocios",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "medio",
        splitDesde: "Álgebra Lineal general (52 mód) cubre la parte de álgebra. El componente de optimización es específico de este ramo.",
        nota: "Sin fuente verificada en uclases.cl. Contenidos inferidos de malla curricular.",
      },
      {
        nombre: "Razonamiento Cuantitativo con Datos I",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Estadística descriptiva, representación gráfica, medidas centrales"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Razonamiento Cuantitativo con Datos II",
        semestre: 2,
        prereqs: "Razonamiento Cuantitativo con Datos I",
        contenidos: ["Variables aleatorias, estimación, hipótesis, regresión simple"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Estadística y Data Science",
        semestre: 3,
        prereqs: "Razonamiento Cuantitativo con Datos II",
        contenidos: ["Regresión múltiple, modelos estadísticos, introducción ML"],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // BACHILLERATO DE INGENIERÍA CIVIL
  // ═══════════════════════════════════════
  {
    id: "bachillerato-ic",
    nombre: "Bachillerato de Ingeniería Civil",
    facultad: "Facultad de Ingeniería y Ciencias",
    duracion: "2 semestres (ingreso directo a Ing. Civil, convalidación S1)",
    mallaUrl: "https://uai.cdn7pm.net/documentos/malla-bachillerato-ing-civil-uai.pdf",
    ramos: [
      {
        nombre: "Introducción al Álgebra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Razonamiento lógico-matemático",
          "Conjuntos y números",
          "Ecuaciones e inecuaciones básicas",
          "Funciones elementales",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre ampliamente este ramo introductorio.",
      },
      {
        nombre: "Introducción al Cálculo",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Funciones y sus gráficas",
          "Concepto intuitivo de límite",
          "Introducción a la derivada",
          "Pendiente y razón de cambio",
        ],
        match: ["precalculo-cero", "calculo-1var-gen"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (funciones) + inicio de Cálculo en una Variable (límites, derivadas).",
      },
      {
        nombre: "Álgebra",
        semestre: 2,
        prereqs: "Introducción al Álgebra",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/78/795",
        contenidos: [
          "Mismo programa que Álgebra de Ing. Civil Plan Común",
          "Lógica, conjuntos, números reales, trigonometría, geometría analítica, números complejos, polinomios",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero + Nivelación Ingeniería.",
        nota: "Convalida con Álgebra del plan común de Ing. Civil",
      },
      {
        nombre: "Cálculo Diferencial",
        semestre: 2,
        prereqs: "Introducción al Cálculo",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/655",
        contenidos: [
          "Mismo programa que Cálculo Diferencial de Ing. Civil Plan Común",
          "Funciones, límites, derivadas, aplicaciones (máx/mín, L'Hôpital, graficación)",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód, parte diferencial) o Cálculo Diferencial gen.",
        nota: "Convalida con Cálculo Diferencial del plan común de Ing. Civil",
      },
    ],
  },

  // ═══════════════════════════════════════
  // BACHILLERATO DE INGENIERÍA COMERCIAL
  // ═══════════════════════════════════════
  {
    id: "bachillerato-icom",
    nombre: "Bachillerato de Ingeniería Comercial",
    facultad: "Escuela de Negocios",
    duracion: "2 semestres (ingreso directo a Ing. Comercial, convalidación S1)",
    mallaUrl: "https://uai.cdn7pm.net/documentos/malla-bachillerato-ing-comercial.pdf",
    ramos: [
      {
        nombre: "Introducción al Cálculo",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Funciones y gráficas básicas",
          "Concepto de límite",
          "Introducción a derivadas",
          "Modelación básica",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre funciones y álgebra básica.",
      },
      {
        nombre: "Introducción al Álgebra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Conjuntos y operaciones",
          "Ecuaciones e inecuaciones",
          "Álgebra básica",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre ampliamente este ramo.",
      },
      {
        nombre: "Matemáticas Avanzadas I",
        semestre: 2,
        prereqs: "Introducción al Cálculo, Introducción al Álgebra",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/651/806",
        contenidos: [
          "Mismo programa que Mat. Avanzadas I de Ing. Comercial",
          "Lógica, conjuntos, inducción, sucesiones, funciones, matrices, determinantes, espacios vectoriales",
        ],
        match: ["precalculo-cero", "algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero + Álgebra Lineal. Ingresa directamente al plan común de Ing. Comercial.",
        nota: "Convalida con Mat. Avanzadas I del plan común de Ing. Comercial",
      },
      {
        nombre: "Razonamiento Cuantitativo con Datos I",
        semestre: 2,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Estadística descriptiva, gráficos, medidas centrales"],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // DOBLE TÍTULO ARQUITECTURA + ING. CIVIL INDUSTRIAL
  // ═══════════════════════════════════════
  {
    id: "arq-ici",
    nombre: "Doble Título Arquitectura + Ing. Civil Industrial",
    facultad: "Fac. Arquitectura + Fac. Ingeniería",
    duracion: "13 semestres",
    mallaUrl: "https://uai.cdn7pm.net/documentos/malla-curricular-doble-titulo-arquitectura-ingenieria.pdf",
    nota: "Nuevo 2026. Inédito en Chile.",
    ramos: [
      {
        nombre: "Álgebra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/78/795",
        contenidos: [
          "Mismo programa que Álgebra de Ing. Civil Plan Común",
          "Lógica, conjuntos, números reales, trigonometría, geometría analítica, números complejos, polinomios",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero + Nivelación Ingeniería.",
        nota: "Mismo Álgebra que Ing. Civil Plan Común",
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 2,
        prereqs: "Álgebra",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/73/795",
        contenidos: [
          "Mismo programa que Álgebra Lineal de Ing. Civil Plan Común",
          "Matrices, determinantes, espacios vectoriales, transformaciones lineales, diagonalización, Gram-Schmidt",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal general (52 mód).",
        nota: "Mismo Álgebra Lineal que Ing. Civil Plan Común",
      },
      {
        nombre: "Ecuaciones Diferenciales",
        semestre: 5,
        prereqs: "Álgebra Lineal",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/1/795",
        contenidos: [
          "Mismo programa que Ecuaciones Diferenciales de Ing. Civil Plan Común",
          "EDO 1er y 2do orden, Laplace, sistemas de ED, series de Fourier",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Ecuaciones Diferenciales general (42 mód).",
        nota: "Mismo programa que Ec. Diferenciales de Ing. Civil Plan Común",
      },
    ],
  },
];

// Carreras UAI sin ramos matemáticos significativos
const sinMatematicas = [
  "Psicología",
  "Comunicación Estratégica - Periodismo",
  "Derecho",
  "Doble Grado Derecho + Ingeniería Comercial (ver Ing. Comercial)",
  "Doble Título Sociología + Ing. Comercial (ver Ing. Comercial)",
  "International Management",
  "Ingeniería en Diseño (ver vía Ing. Civil o Ing. Comercial)",
];

const fuentes = [
  { tipo: "Malla", nombre: "Ing. Civil Industrial", url: "https://uai.cdn7pm.net/documentos/malla-carrera-ingenieria-civil-industrial.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Informática", url: "https://uai.cdn7pm.net/documentos/malla-pregrado-ing-civil-informatica.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil en Bioingeniería", url: "https://uai.cdn7pm.net/documentos/malla-pregrado-ingenieria-civil-en-bioingenieria.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil (Obras Civiles)", url: "https://uai.cdn7pm.net/documentos/malla-pregrado-ingenieria-civil-obras-civiles.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil en Energía", url: "https://uai.cdn7pm.net/documentos/malla-pregrado-ingenieria-civil-en-energia.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Mecánica", url: "https://uai.cdn7pm.net/documentos/malla-pregrado-ingenieria-civil-mecanica.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil en Minería", url: "https://uai.cdn7pm.net/documentos/malla-pregrado-ingenieria-civil-en-mineria.pdf" },
  { tipo: "Malla", nombre: "Ing. Comercial (Lic. Admin.)", url: "https://uai.cdn7pm.net/documentos/malla-licenciatura-administracion-de-empresas.pdf" },
  { tipo: "Malla", nombre: "Ing. Comercial (Lic. Economía)", url: "https://uai.cdn7pm.net/documentos/malla-licenciatura-economia.pdf" },
  { tipo: "Malla", nombre: "Ing. en Computer Science", url: "https://uai.cdn7pm.net/documentos/malla-ingenieria-en-computer-science.pdf" },
  { tipo: "Malla", nombre: "Ing. en Negocios y Tecnología", url: "https://uai.cdn7pm.net/documentos/malla-pregrado-ingenieria-en-negocios-y-tecnologia.pdf" },
  { tipo: "Malla", nombre: "Bachillerato Ing. Civil", url: "https://uai.cdn7pm.net/documentos/malla-bachillerato-ing-civil-uai.pdf" },
  { tipo: "Malla", nombre: "Bachillerato Ing. Comercial", url: "https://uai.cdn7pm.net/documentos/malla-bachillerato-ing-comercial.pdf" },
  { tipo: "Malla", nombre: "Doble Título Arq. + ICI", url: "https://uai.cdn7pm.net/documentos/malla-curricular-doble-titulo-arquitectura-ingenieria.pdf" },
  { tipo: "Portal", nombre: "Mallas y Folletos UAI", url: "https://www.uai.cl/admision/mallas-curriculares-y-folletos" },
  { tipo: "Portal", nombre: "Admisión UAI", url: "https://admision.uai.cl/carreras/" },
  { tipo: "Contenido", nombre: "Álgebra — Ing. Civil (uclases.cl)", url: "https://www.uclases.cl/cursos/detalle/78/795" },
  { tipo: "Contenido", nombre: "Cálculo Diferencial — Ing. Civil (uclases.cl)", url: "https://www.uclases.cl/cursos/detalle/655" },
  { tipo: "Contenido", nombre: "Cálculo Integral — Ing. Civil (uclases.cl)", url: "https://www.uclases.cl/cursos/detalle/656/795" },
  { tipo: "Contenido", nombre: "Álgebra Lineal — Ing. Civil (uclases.cl)", url: "https://www.uclases.cl/cursos/detalle/73/795" },
  { tipo: "Contenido", nombre: "Cálculo Multivariables — Ing. Civil (uclases.cl)", url: "https://www.uclases.cl/cursos/detalle/188/795" },
  { tipo: "Contenido", nombre: "Ecuaciones Diferenciales — Ing. Civil (uclases.cl)", url: "https://www.uclases.cl/cursos/detalle/1/795" },
  { tipo: "Contenido", nombre: "Matemáticas Avanzadas I — Ing. Comercial (uclases.cl)", url: "https://www.uclases.cl/cursos/detalle/651/806" },
  { tipo: "Contenido", nombre: "Matemáticas Avanzadas II — Ing. Comercial (uclases.cl)", url: "https://www.uclases.cl/cursos/detalle/1275/794" },
  { tipo: "Contenido", nombre: "Álgebra Lineal Syllabus (syllabi.uai.cl)", url: "http://syllabi.uai.cl/students/view-unit-page/uos_id/286142/vid/290001" },
];

// ═══════════════════════════════════════════════════════════════
// COMPONENTES
// ═══════════════════════════════════════════════════════════════

const MatchBadge = ({ level }) => {
  const styles = {
    alto: "bg-green-100 text-green-800 border-green-300",
    medio: "bg-yellow-100 text-yellow-800 border-yellow-300",
    bajo: "bg-orange-100 text-orange-800 border-orange-300",
    ninguno: "bg-gray-100 text-gray-500 border-gray-300",
  };
  const labels = { alto: "Match Alto", medio: "Match Medio", bajo: "Match Bajo", ninguno: "Sin match" };
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full border ${styles[level]}`}>
      {labels[level]}
    </span>
  );
};

const CursoCard = ({ curso, expanded, onToggle }) => {
  const matchCursos = seRemontaCursos.filter((sr) => curso.match?.includes(sr.id));

  return (
    <div className="border rounded-lg mb-2 overflow-hidden shadow-sm bg-white">
      <button
        onClick={onToggle}
        className="w-full text-left px-4 py-3 flex items-center justify-between hover:bg-gray-50"
      >
        <div className="flex items-center gap-3 flex-wrap">
          <span className="font-semibold text-gray-800">{curso.nombre}</span>
          <span className="text-xs text-gray-500">S{curso.semestre}</span>
          <MatchBadge level={curso.matchLevel} />
          {curso.splitDesde && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-300">
              Oportunidad de split
            </span>
          )}
        </div>
        <span className="text-gray-400 text-lg">{expanded ? "−" : "+"}</span>
      </button>
      {expanded && (
        <div className="px-4 pb-4 border-t bg-gray-50">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
            <div>
              <p className="text-sm text-gray-600 mb-1">
                <span className="font-medium">Prerrequisitos:</span> {curso.prereqs || "—"}
              </p>
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <p className="text-sm font-medium text-gray-700">Contenidos:</p>
                {curso.fuenteContenido && (
                  <a
                    href={curso.fuenteContenido}
                    target="_blank"
                    rel="noopener"
                    className="text-xs text-green-600 underline flex items-center gap-1"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-green-500 inline-block" />
                    Fuente verificada
                  </a>
                )}
              </div>
              <ul className="text-sm text-gray-600 space-y-0.5">
                {curso.contenidos?.map((c, i) => (
                  <li key={i} className="flex gap-1">
                    <span className="text-gray-400">•</span> {typeof c === "string" ? c : c}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          {curso.splitDesde && (
            <div className="mt-3 pt-3 border-t">
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
                <p className="text-sm font-semibold text-amber-800 mb-1">Oportunidad de splitting:</p>
                <p className="text-sm text-amber-700">{curso.splitDesde}</p>
              </div>
            </div>
          )}
          {curso.nota && (
            <div className="mt-2">
              <p className="text-xs text-blue-600 italic">{curso.nota}</p>
            </div>
          )}
          {matchCursos.length > 0 && (
            <div className="mt-3 pt-3 border-t">
              <p className="text-sm font-medium text-gray-700 mb-2">Cursos Se Remonta compatibles:</p>
              <div className="flex flex-wrap gap-2">
                {matchCursos.map((sr) => (
                  <span
                    key={sr.id}
                    className="text-xs px-3 py-1 rounded-full text-white font-medium"
                    style={{ backgroundColor: sr.color }}
                  >
                    {sr.nombre}{sr.modulos ? ` (${sr.modulos} mód)` : ""}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const CarreraSection = ({ carrera }) => {
  const [expandedCursos, setExpandedCursos] = useState({});
  const [isOpen, setIsOpen] = useState(false);

  const toggleCurso = (idx) =>
    setExpandedCursos((prev) => ({ ...prev, [idx]: !prev[idx] }));

  const totalMatch = carrera.ramos.filter((r) => r.matchLevel === "alto" || r.matchLevel === "medio").length;

  return (
    <div className="border rounded-xl mb-4 overflow-hidden shadow-sm">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full text-left px-5 py-4 bg-white hover:bg-gray-50 flex items-center justify-between"
      >
        <div>
          <h3 className="font-bold text-lg text-gray-800">{carrera.nombre}</h3>
          <p className="text-sm text-gray-500">
            {carrera.facultad} · {carrera.duracion} · {carrera.ramos.length} ramos matemáticos
            {carrera.nota && <span className="ml-2 text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded">{carrera.nota}</span>}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-green-700 bg-green-50 px-3 py-1 rounded-full">
            {totalMatch} matches
          </span>
          <span className="text-gray-400 text-xl">{isOpen ? "▲" : "▼"}</span>
        </div>
      </button>
      {isOpen && (
        <div className="px-5 pb-4 bg-gray-50 border-t">
          {carrera.especialidades && (
            <div className="mt-3 mb-3">
              <p className="text-xs text-gray-500 mb-1">Especialidades que comparten este plan:</p>
              <div className="flex flex-wrap gap-1">
                {carrera.especialidades.map((e, i) => (
                  <span key={i} className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded">{e}</span>
                ))}
              </div>
            </div>
          )}
          <div className="mt-3">
            {carrera.ramos.map((curso, idx) => (
              <CursoCard
                key={idx}
                curso={curso}
                expanded={expandedCursos[idx]}
                onToggle={() => toggleCurso(idx)}
              />
            ))}
          </div>
          {carrera.mallaUrl && (
            <a href={carrera.mallaUrl} target="_blank" rel="noopener" className="text-sm text-blue-600 underline mt-2 inline-block">
              Ver malla curricular completa (PDF)
            </a>
          )}
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// MATRIZ DE SPLITTING
// ═══════════════════════════════════════════════════════════════

const MatrizSplitting = () => {
  const matrix = seRemontaCursos.map((sr) => {
    const matches = [];
    carreras.forEach((carrera) => {
      carrera.ramos.forEach((ramo) => {
        if (ramo.match?.includes(sr.id)) {
          matches.push({
            carrera: carrera.nombre,
            carreraId: carrera.id,
            ramo: ramo.nombre,
            semestre: ramo.semestre,
            level: ramo.matchLevel,
          });
        }
      });
    });
    return { ...sr, matches };
  }).filter(sr => sr.matches.length > 0);

  return (
    <div className="space-y-4">
      {matrix.map((sr) => (
        <div key={sr.id} className="border rounded-xl overflow-hidden bg-white shadow-sm">
          <div className="px-5 py-3 flex items-center gap-3" style={{ backgroundColor: sr.color + "15" }}>
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: sr.color }} />
            <h3 className="font-bold text-gray-800">{sr.nombre}</h3>
            {sr.modulos && <span className="text-xs text-gray-500">{sr.modulos} módulos</span>}
            {sr.precio && <span className="text-xs text-gray-500">${(sr.precio/1000).toFixed(0)}k</span>}
            <span className="text-sm text-gray-500">({sr.matches.length} coincidencias en UAI)</span>
          </div>
          <div className="p-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-2 font-medium">Carrera UAI</th>
                  <th className="pb-2 font-medium">Ramo</th>
                  <th className="pb-2 font-medium">Semestre</th>
                  <th className="pb-2 font-medium">Match</th>
                </tr>
              </thead>
              <tbody>
                {sr.matches.map((m, i) => (
                  <tr key={i} className="border-b last:border-0">
                    <td className="py-2 text-gray-700">{m.carrera}</td>
                    <td className="py-2 font-medium">{m.ramo}</td>
                    <td className="py-2 text-gray-500">S{m.semestre}</td>
                    <td className="py-2">
                      <MatchBadge level={m.level} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// RESUMEN ESTADÍSTICO
// ═══════════════════════════════════════════════════════════════

const Resumen = () => {
  let totalRamos = 0;
  let totalMatchAlto = 0;
  let totalMatchMedio = 0;
  let totalSplitOportunidad = 0;
  carreras.forEach((c) => {
    totalRamos += c.ramos.length;
    c.ramos.forEach((r) => {
      if (r.matchLevel === "alto") totalMatchAlto++;
      if (r.matchLevel === "medio") totalMatchMedio++;
      if (r.splitDesde) totalSplitOportunidad++;
    });
  });

  return (
    <div className="space-y-4 mb-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-blue-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-blue-700">{carreras.length}</div>
          <div className="text-xs text-blue-600">Carreras analizadas</div>
        </div>
        <div className="bg-purple-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-purple-700">{totalRamos}</div>
          <div className="text-xs text-purple-600">Ramos matemáticos</div>
        </div>
        <div className="bg-amber-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-amber-700">{totalSplitOportunidad}</div>
          <div className="text-xs text-amber-600">Oportunidades split</div>
        </div>
        <div className="bg-gray-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-gray-700">{seRemontaCursos.length}</div>
          <div className="text-xs text-gray-600">Cursos Se Remonta</div>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-green-100 rounded-xl p-3 text-center border border-green-200">
          <div className="text-lg font-bold text-green-800">{totalMatchAlto}</div>
          <div className="text-xs text-green-700">Matches altos</div>
        </div>
        <div className="bg-yellow-100 rounded-xl p-3 text-center border border-yellow-200">
          <div className="text-lg font-bold text-yellow-800">{totalMatchMedio}</div>
          <div className="text-xs text-yellow-700">Matches medios</div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// APP PRINCIPAL
// ═══════════════════════════════════════════════════════════════

export default function App() {
  const [tab, setTab] = useState("carreras");
  const [filtro, setFiltro] = useState("");

  const carrerasFiltradas = carreras.filter(
    (c) =>
      c.nombre.toLowerCase().includes(filtro.toLowerCase()) ||
      c.ramos.some((r) => r.nombre.toLowerCase().includes(filtro.toLowerCase()))
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-5xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-cyan-700 rounded-xl flex items-center justify-center text-white font-bold text-lg">
              UAI
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">
                Ramos Matemáticos UAI
              </h1>
              <p className="text-sm text-gray-500">
                Investigación para splitting con Se Remonta — Universidad Adolfo Ibáñez
              </p>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-3">
            Análisis de <strong>{carreras.length} programas</strong> de pregrado UAI con ramos matemáticos significativos.
            Las <strong>7 especialidades de Ing. Civil</strong> comparten el mismo plan común matemático (S1-S4).
            <strong> {sinMatematicas.length} carreras</strong> no tienen matemáticas dedicadas o usan las de otra carrera.
          </p>
          <div className="mt-3 bg-cyan-50 border border-cyan-200 rounded-lg p-3">
            <p className="text-sm text-cyan-800">
              <strong>Hallazgo clave:</strong> La UAI tiene un plan común de ingeniería muy estructurado con 8 ramos matemáticos
              en los primeros 5 semestres. Los cursos Se Remonta generales (Precálculo, Cálculo 1 Var, Álgebra Lineal,
              Cálculo Varias Var, Ec. Diferenciales) tienen match alto y directo con todos ellos.
              En Ing. Comercial, "Mat. Avanzadas I" combina álgebra + matrices y "Mat. Avanzadas II" cubre cálculo en una variable (NO incluye multivariable, verificado).
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-4 bg-white rounded-xl p-1 shadow-sm">
          {[
            { id: "carreras", label: "Por Carrera" },
            { id: "splitting", label: "Matriz de Splitting" },
            { id: "fuentes", label: "Fuentes" },
          ].map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`flex-1 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                tab === t.id
                  ? "bg-cyan-700 text-white shadow"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Resumen */}
        <Resumen />

        {/* Contenido por tab */}
        {tab === "carreras" && (
          <>
            <input
              type="text"
              placeholder="Buscar carrera o ramo..."
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border bg-white mb-4 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-400"
            />
            {carrerasFiltradas.map((c) => (
              <CarreraSection key={c.id} carrera={c} />
            ))}

            {/* Carreras sin matemáticas */}
            <div className="mt-6 border rounded-xl bg-white p-5 shadow-sm">
              <h3 className="font-bold text-gray-700 mb-3">
                Carreras sin ramos matemáticos propios ({sinMatematicas.length})
              </h3>
              <p className="text-sm text-gray-500 mb-3">
                Estas carreras no tienen cursos dedicados de matemáticas en su malla, o comparten
                los ramos de otra carrera listada arriba (por ejemplo, los dobles títulos).
              </p>
              <div className="flex flex-wrap gap-2">
                {sinMatematicas.map((c, i) => (
                  <span key={i} className="text-xs bg-gray-100 text-gray-600 px-3 py-1 rounded-full">
                    {c}
                  </span>
                ))}
              </div>
            </div>
          </>
        )}

        {tab === "splitting" && <MatrizSplitting />}

        {tab === "fuentes" && (
          <div className="bg-white rounded-xl shadow-sm p-5">
            <h3 className="font-bold text-gray-800 mb-4">Fuentes documentadas</h3>
            <p className="text-sm text-gray-600 mb-4">
              Todos los datos fueron extraídos de las mallas curriculares oficiales de la UAI
              (PDFs descargados del CDN oficial) y búsquedas de contenidos de asignaturas.
              Datos vigentes para admisión 2026.
            </p>
            {["Malla", "Portal", "Contenido"].map((tipo) => (
              <div key={tipo} className="mb-5">
                <h4 className="font-semibold text-sm text-gray-700 mb-2 uppercase tracking-wide">{tipo}s</h4>
                <div className="space-y-1">
                  {fuentes
                    .filter((f) => f.tipo === tipo)
                    .map((f, i) => (
                      <div key={i} className="flex items-center gap-2 text-sm">
                        <span className={`w-2 h-2 rounded-full ${tipo === "Malla" ? "bg-blue-400" : tipo === "Portal" ? "bg-purple-400" : "bg-green-400"}`} />
                        <span className="text-gray-700 font-medium">{f.nombre}</span>
                        <a href={f.url} target="_blank" rel="noopener" className="text-blue-500 underline text-xs truncate max-w-xs">
                          {f.url.replace("https://uai.cdn7pm.net/documentos/", "").replace("https://www.uai.cl/", "")}
                        </a>
                      </div>
                    ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="text-center text-xs text-gray-400 mt-8 pb-4">
          Investigación Se Remonta × UAI · Datos verificados abril 2026 · Fuentes oficiales UAI
        </div>
      </div>
    </div>
  );
}
