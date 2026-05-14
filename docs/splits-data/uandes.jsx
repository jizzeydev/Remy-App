import { useState } from "react";

// ═══════════════════════════════════════════════════════════════
// DATOS VERIFICADOS - Investigación Ramos Matemáticos UANDES
// Fuentes: Mallas curriculares oficiales UANDES (PDFs) + Studocu + Admisión UANDES
// Fecha de investigación: Abril 2026
// ═══════════════════════════════════════════════════════════════

// ── CATÁLOGO COMPLETO SE REMONTA (33 cursos) ──────────────────
// Fuente: www.seremonta.store + archivos proyecto Se Remonta
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
  // ─── CURSOS UDD (existentes) ───
  { id: "calc-dif-udd-civil", nombre: "Cálculo Diferencial UDD Ing. Civil", tipo: "udd", modulos: 58, precio: null, color: "#DC2626",
    carrera: "Ing. Civil Plan Común" },
  { id: "calc-int-udd-civil", nombre: "Cálculo Integral UDD Ing. Civil", tipo: "udd", modulos: 37, precio: null, color: "#EF4444",
    carrera: "Ing. Civil Plan Común" },
  { id: "calc1-udd-icom", nombre: "Cálculo I UDD Ing. Comercial", tipo: "udd", modulos: 47, precio: null, color: "#F97316",
    carrera: "Ing. Comercial" },
  { id: "calc2-udd-icom", nombre: "Cálculo II UDD Ing. Comercial", tipo: "udd", modulos: 33, precio: null, color: "#FB923C",
    carrera: "Ing. Comercial" },
  // ─── CURSOS UC ───
  { id: "mat1000-uc", nombre: "MAT1000 Precálculo (UC)", tipo: "uc", modulos: 56, color: "#64748B" },
  { id: "mat1107-uc", nombre: "MAT1107 Intro Cálculo (UC)", tipo: "uc", modulos: 30, color: "#64748B" },
  { id: "mat1207-uc", nombre: "MAT1207 Intro Álgebra y Geo (UC)", tipo: "uc", modulos: 47, color: "#64748B" },
  { id: "mat1023-uc", nombre: "MAT1023 Cálculo I (UC)", tipo: "uc", modulos: 70, color: "#64748B" },
  { id: "mat1100-uc", nombre: "MAT1100 Cálculo I (UC)", tipo: "uc", modulos: 50, color: "#64748B" },
  { id: "mat1610-uc", nombre: "MAT1610 Cálculo I (UC)", tipo: "uc", modulos: 69, color: "#64748B" },
  { id: "mat1220-uc", nombre: "MAT1220 Cálculo II (UC)", tipo: "uc", modulos: 49, color: "#64748B" },
  { id: "mat1620-uc", nombre: "MAT1620 Cálculo II (UC)", tipo: "uc", modulos: 58, color: "#64748B" },
  { id: "mat1279-uc", nombre: "MAT1279-99 Intro Álgebra Lineal (UC)", tipo: "uc", modulos: 36, color: "#64748B" },
  { id: "mat1203-uc", nombre: "MAT1203 Álgebra Lineal (UC)", tipo: "uc", modulos: 64, color: "#64748B" },
  { id: "mat1630-uc", nombre: "MAT1630 Cálculo III (UC)", tipo: "uc", modulos: 32, color: "#64748B" },
  { id: "mat1640-uc", nombre: "MAT1640 Ec. Dif. (UC)", tipo: "uc", modulos: 43, color: "#64748B" },
  { id: "ics1113-uc", nombre: "ICS1113 Optimización (UC)", tipo: "uc", modulos: 18, color: "#64748B" },
  { id: "qim100i-uc", nombre: "QIM100I Química (UC)", tipo: "uc", modulos: 23, color: "#64748B" },
  { id: "fis1533-uc", nombre: "FIS1533 Electricidad (UC)", tipo: "uc", modulos: 5, color: "#64748B" },
  // ─── CURSOS UAI ───
  { id: "calc-dif-uai", nombre: "Cálculo Diferencial (UAI)", tipo: "uai", modulos: 56, color: "#A78BFA" },
  { id: "calc-int-uai", nombre: "Cálculo Integral (UAI)", tipo: "uai", modulos: 43, color: "#A78BFA" },
  { id: "calc1-uai", nombre: "Cálculo I (UAI)", tipo: "uai", modulos: 54, color: "#A78BFA" },
  { id: "calc2-uai", nombre: "Cálculo II (UAI)", tipo: "uai", modulos: 20, color: "#A78BFA" },
  { id: "calc3-uai", nombre: "Cálculo III (UAI)", tipo: "uai", modulos: 37, color: "#A78BFA" },
];

// ══════════════════════════════════════════════════════════════════
// CARRERAS UANDES CON RAMOS MATEMÁTICOS
// Fuentes: Mallas oficiales UANDES (PDFs descargados y verificados)
// Todas las Ing. Civiles comparten plan común en semestres 1-4
// ══════════════════════════════════════════════════════════════════

const carreras = [
  {
    id: "plan-comun-ing",
    nombre: "Ingeniería Civil Plan Común",
    facultad: "Ingeniería y Ciencias Aplicadas",
    duracion: "4 semestres comunes + especialización (11 sem total)",
    especialidades: [
      "Ing. Civil Industrial",
      "Ing. Civil en Obras Civiles",
      "Ing. Civil en Ciencias de la Computación",
      "Ing. Civil Eléctrica",
      "Ing. Civil Química (nueva 2026)",
    ],
    mallaUrl: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-Industrial-1.pdf",
    ramos: [
      {
        nombre: "Álgebra e Introducción al Cálculo",
        semestre: 1,
        codigo: "MAD1101",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Conjuntos y números reales: axiomas, desigualdades, valor absoluto",
          "Polinomios: operaciones, división sintética, raíces",
          "Funciones reales de variable real (lineal, cuadrática, potencia, exponencial, logarítmica)",
          "Trigonometría: razones, identidades, teorema del seno y coseno",
          "Números complejos (forma binomial, polar)",
          "Introducción a límites y continuidad",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Precálculo desde Cero (68 módulos) cubre conjuntos, álgebra, funciones y trigonometría. Nivelación Ingeniería complementa.",
        fuentePrograma: "https://www.studocu.com/cl/course/universidad-de-los-andes-chile/algebra-e-introduccion-al-calculo/3459983",
      },
      {
        nombre: "Cálculo I",
        semestre: 2,
        codigo: "MAD1102",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Álgebra e Introducción al Cálculo",
        contenidos: [
          "Límites: definición formal, propiedades, laterales, al infinito",
          "Continuidad de funciones",
          "Derivadas: definición, reglas de derivación, cadena",
          "Derivación implícita y logarítmica",
          "Aplicaciones de la derivada: máximos, mínimos, concavidad, L'Hôpital",
          "Análisis y graficación de funciones",
          "Introducción a la integral",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Cálculo en una Variable (85 módulos) cubre límites, derivadas y sus aplicaciones. Cálculo Diferencial general también aplica.",
        fuentePrograma: "https://www.studocu.com/cl/course/universidad-de-los-andes-chile/calculo-i/3459827",
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 2,
        codigo: "ING—",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Álgebra e Introducción al Cálculo",
        contenidos: [
          "Matrices y sistemas de ecuaciones lineales (Gauss, Gauss-Jordan)",
          "Determinantes: propiedades y cálculo",
          "Espacios vectoriales: definición, subespacio, independencia lineal, base, dimensión",
          "Transformaciones lineales: núcleo, imagen",
          "Producto interior, ortogonalización de Gram-Schmidt",
          "Valores y vectores propios, diagonalización",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Álgebra Lineal general (52 mód, 8 capítulos) cubre todos los temas: sistemas, matrices, determinantes, espacios vectoriales, valores propios, ortogonalidad.",
        fuentePrograma: "https://www.studocu.com/cl/course/universidad-de-los-andes-chile/algebra-lineal/3459988",
      },
      {
        nombre: "Cálculo II",
        semestre: 3,
        codigo: "MAD1103",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Cálculo I",
        contenidos: [
          "Antiderivadas e integral indefinida",
          "Técnicas de integración: sustitución, partes, fracciones parciales, trigonométricas",
          "Integral definida y Teorema Fundamental del Cálculo",
          "Aplicaciones: áreas, volúmenes, longitud de arco",
          "Integrales impropias",
          "Funciones de varias variables e introducción a derivadas parciales",
          "Integrales dobles y triples",
        ],
        match: ["calculo-1var-gen", "calculo-int-gen", "calculo-vvar-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Cálculo en una Variable (85 mód) cubre integración. Cálculo en Varias Variables (41 mód) cubre multivariable. Ambos necesarios para cobertura completa.",
      },
      {
        nombre: "Ecuaciones Diferenciales",
        semestre: 3,
        codigo: "ING—",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Cálculo II",
        contenidos: [
          "EDO de primer orden: separables, lineales, exactas, Bernoulli",
          "EDO de segundo orden: coeficientes constantes, variación de parámetros",
          "Transformada de Laplace: definición, propiedades, inversión",
          "Sistemas de ecuaciones diferenciales",
          "Aplicaciones a ingeniería: circuitos, resortes, mezcla",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Ecuaciones Diferenciales general (42 mód) cubre EDO 1er y 2do orden, Laplace, sistemas. Match casi directo.",
      },
      {
        nombre: "Probabilidades y Estadística",
        semestre: 4,
        codigo: "ING—",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Cálculo II",
        contenidos: [
          "Probabilidad: axiomas, condicional, Bayes",
          "Variables aleatorias discretas y continuas",
          "Distribuciones de probabilidad (Binomial, Poisson, Normal)",
          "Estimación puntual y por intervalos",
          "Pruebas de hipótesis",
          "Regresión lineal simple",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
    ],
  },
  {
    id: "ing-civil-industrial",
    nombre: "Ingeniería Civil Industrial",
    facultad: "Ingeniería y Ciencias Aplicadas",
    duracion: "11 semestres (6 años)",
    mallaUrl: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-Industrial-1.pdf",
    nota: "Comparte plan común. Ramos adicionales propios de la especialidad.",
    ramos: [
      {
        nombre: "Optimización",
        semestre: 5,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Álgebra Lineal, Cálculo II",
        contenidos: [
          "Programación lineal: formulación, método simplex",
          "Dualidad y análisis de sensibilidad",
          "Programación entera",
          "Modelos de optimización aplicados",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
        nota: "Ramo propio de Ing. Civil Industrial después del plan común.",
      },
      {
        nombre: "Métodos Estadísticos para la Gestión",
        semestre: 5,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Probabilidades y Estadística",
        contenidos: [
          "Regresión lineal múltiple",
          "Análisis de varianza (ANOVA)",
          "Diseño de experimentos",
          "Series de tiempo",
          "Control estadístico de procesos",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
      {
        nombre: "Modelos Estocásticos",
        semestre: 6,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Probabilidades y Estadística",
        contenidos: [
          "Cadenas de Markov",
          "Teoría de colas",
          "Simulación estocástica",
          "Procesos de decisión de Markov",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
      {
        nombre: "Programación Matemática",
        semestre: 6,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Optimización",
        contenidos: [
          "Programación no lineal",
          "Optimización convexa",
          "Métodos de punto interior",
          "Heurísticas y metaheurísticas",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
    ],
  },
  {
    id: "ing-civil-obras",
    nombre: "Ingeniería Civil en Obras Civiles",
    facultad: "Ingeniería y Ciencias Aplicadas",
    duracion: "11 semestres (6 años)",
    mallaUrl: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-en-Obras-Civiles.pdf",
    nota: "Comparte plan común. Ramos adicionales propios de la especialidad.",
    ramos: [
      {
        nombre: "Optimización",
        semestre: 5,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Álgebra Lineal, Cálculo II",
        contenidos: ["Programación lineal, método simplex, dualidad, programación entera"],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
      {
        nombre: "Métodos Numéricos",
        semestre: 5,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Ecuaciones Diferenciales",
        contenidos: [
          "Solución numérica de ecuaciones no lineales",
          "Interpolación y aproximación",
          "Integración numérica",
          "Solución numérica de EDO",
          "Métodos de diferencias finitas",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
    ],
  },
  {
    id: "ing-civil-computacion",
    nombre: "Ingeniería Civil en Ciencias de la Computación",
    facultad: "Ingeniería y Ciencias Aplicadas",
    duracion: "11 semestres (5 años acreditados)",
    mallaUrl: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-en-Computacio%CC%81n.pdf",
    nota: "Comparte plan común. Sin ramos matemáticos adicionales significativos post plan común.",
    ramos: [],
  },
  {
    id: "ing-civil-electrica",
    nombre: "Ingeniería Civil Eléctrica",
    facultad: "Ingeniería y Ciencias Aplicadas",
    duracion: "11 semestres (5 años acreditados)",
    mallaUrl: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-Ele%CC%81ctrica-1.pdf",
    nota: "Comparte plan común. Sin ramos matemáticos adicionales significativos post plan común.",
    ramos: [],
  },
  {
    id: "ing-civil-quimica",
    nombre: "Ingeniería Civil Química",
    facultad: "Ingeniería y Ciencias Aplicadas",
    duracion: "11 semestres",
    mallaUrl: "https://admision.uandes.cl/docs/default-source/carreras/documentos-area-ingenieria-y-administracion/ingenieria-civil-ambiental/malla-ing-civil-quimica-uandes.pdf",
    nota: "Nueva 2026. Malla propia ligeramente distinta al plan común histórico.",
    ramos: [
      {
        nombre: "Introducción al Álgebra y Geometría",
        semestre: 1,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Conjuntos y números reales",
          "Álgebra de polinomios y expresiones",
          "Geometría analítica plana",
          "Vectores en R² y R³",
          "Introducción a matrices",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Precálculo desde Cero (68 mód) cubre conjuntos, álgebra y geometría analítica.",
      },
      {
        nombre: "Introducción al Cálculo",
        semestre: 1,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Funciones reales (lineal, cuadrática, exponencial, logarítmica, trigonométricas)",
          "Límites y continuidad",
          "Introducción a la derivada",
        ],
        match: ["precalculo-cero", "calculo-1var-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Precálculo desde Cero cubre funciones y trig. Cálculo en una Variable (85 mód) cubre límites y derivadas.",
      },
      {
        nombre: "Cálculo I",
        semestre: 2,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Introducción al Cálculo",
        contenidos: [
          "Derivadas: reglas, cadena, implícita",
          "Aplicaciones de la derivada",
          "Integral indefinida y definida",
          "Técnicas de integración",
          "Aplicaciones de la integral",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen", "calculo-int-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Cálculo en una Variable (85 mód) cubre derivadas e integrales completas.",
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 2,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Introducción al Álgebra y Geometría",
        contenidos: [
          "Matrices y sistemas de ecuaciones",
          "Determinantes",
          "Espacios vectoriales",
          "Transformaciones lineales",
          "Valores y vectores propios",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Álgebra Lineal general (52 mód) cubre todos los temas.",
      },
      {
        nombre: "Cálculo II",
        semestre: 3,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Cálculo I",
        contenidos: [
          "Funciones de varias variables",
          "Derivadas parciales, gradiente",
          "Integrales dobles y triples",
          "Coordenadas curvilíneas",
        ],
        match: ["calculo-vvar-gen", "calculo-vec-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Cálculo en Varias Variables (41 mód) + Cálculo Vectorial (31 mód).",
      },
      {
        nombre: "Ecuaciones Diferenciales",
        semestre: 3,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Cálculo I, Álgebra Lineal",
        contenidos: [
          "EDO primer y segundo orden",
          "Transformada de Laplace",
          "Sistemas de ecuaciones diferenciales",
          "Aplicaciones",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Ecuaciones Diferenciales general (42 mód). Match casi directo.",
      },
      {
        nombre: "Teoría de Probabilidades",
        semestre: 3,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Cálculo I",
        contenidos: [
          "Probabilidad: axiomas, condicional, Bayes",
          "Variables aleatorias discretas y continuas",
          "Distribuciones de probabilidad",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
      {
        nombre: "Estadística Aplicada",
        semestre: 4,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Teoría de Probabilidades",
        contenidos: [
          "Estimación puntual y por intervalos",
          "Pruebas de hipótesis",
          "Regresión",
          "ANOVA",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
      {
        nombre: "Métodos Numéricos",
        semestre: 5,
        codigo: "ING—",
        creditos: 8,
        prereqs: "Ecuaciones Diferenciales",
        contenidos: [
          "Solución numérica de ecuaciones",
          "Interpolación",
          "Integración numérica",
          "Solución numérica de EDO",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
    ],
  },
  {
    id: "ing-comercial",
    nombre: "Ingeniería Comercial",
    facultad: "Ciencias Económicas y Empresariales",
    duracion: "10 semestres (5 años) + Magíster concurrente",
    mallaUrl: "https://www.uandes.cl/wp-content/uploads/2025/02/Malla-curricular-Ingenieria-Comercial-2024.pdf",
    ramos: [
      {
        nombre: "Álgebra",
        semestre: 1,
        codigo: "MAD1101",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Conjuntos y lógica",
          "Números reales: desigualdades, valor absoluto",
          "Polinomios: operaciones, raíces, fracciones parciales",
          "Álgebra finita: sumatorias, progresiones, factorial, binomio",
          "Matrices y determinantes: operaciones, inversa",
          "Sistemas de ecuaciones lineales",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Precálculo desde Cero (68 mód) cubre la mayoría del contenido.",
        fuentePrograma: "https://www.uandes.cl/wp-content/uploads/2020/11/normativa_malla_curricular_antigua.pdf",
      },
      {
        nombre: "Cálculo I",
        semestre: 2,
        codigo: "MAD1102",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Álgebra (MAD1101)",
        contenidos: [
          "Funciones reales (lineal, cuadrática, exponencial, logarítmica, trigonométricas)",
          "Límites y continuidad",
          "Derivadas: concepto, reglas, orden superior, implícita",
          "Aplicaciones de derivadas: L'Hôpital, máximos/mínimos, concavidad",
          "Introducción a funciones de varias variables",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Cálculo en una Variable (85 mód) cubre límites, derivadas y aplicaciones.",
      },
      {
        nombre: "Optimización",
        semestre: 3,
        codigo: "MAD1103",
        creditos: 8,
        horas: "Según plan semestral",
        prereqs: "Cálculo I (MAD1102)",
        contenidos: [
          "Optimización de funciones de una y varias variables",
          "Multiplicadores de Lagrange",
          "Programación lineal: formulación y solución gráfica",
          "Método simplex",
          "Introducción a programación entera",
        ],
        match: ["calculo-vvar-gen"],
        matchLevel: "medio",
        cursoUANDES: null,
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre parcialmente optimización multivariable y Lagrange.",
      },
      {
        nombre: "Estadística I",
        semestre: 3,
        codigo: "ADM1301",
        creditos: 6,
        prereqs: "Cálculo I",
        contenidos: [
          "Estadística descriptiva",
          "Probabilidad: axiomas, condicional, Bayes",
          "Variables aleatorias discretas y continuas",
          "Distribuciones de probabilidad (Binomial, Poisson, Normal)",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
      {
        nombre: "Estadística II",
        semestre: 4,
        codigo: "ADM1302",
        creditos: 7,
        prereqs: "Estadística I (ADM1301)",
        contenidos: [
          "Estimación puntual y por intervalos",
          "Pruebas de hipótesis",
          "Regresión lineal simple y múltiple",
          "ANOVA",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
      {
        nombre: "Econometría",
        semestre: 5,
        codigo: "ADM1303",
        creditos: 7,
        prereqs: "Estadística II",
        contenidos: [
          "Modelo de regresión lineal múltiple",
          "Multicolinealidad, heterocedasticidad, autocorrelación",
          "Variables instrumentales",
          "Modelos de datos panel",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
    ],
  },
  {
    id: "international-business",
    nombre: "International Business",
    facultad: "Ciencias Económicas y Empresariales",
    duracion: "8 semestres (4 años) + opción 5to año para título Ing. Comercial",
    mallaUrl: "https://admision.uandes.cl/docs/default-source/carreras/documentos-area-ingenieria-y-administracion/international-business/malla_international_business_2023.pdf",
    nota: "Programa bilingüe. ~60% cursos en inglés. Intercambio obligatorio 4to año.",
    ramos: [
      {
        nombre: "Álgebra / Critical Thinking",
        semestre: 1,
        codigo: "—",
        creditos: 8,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Pensamiento analítico y crítico",
          "Álgebra aplicada a negocios",
          "Funciones básicas",
        ],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        cursoUANDES: null,
        splitDesde: "Precálculo desde Cero, seleccionando módulos de álgebra y funciones aplicadas.",
      },
      {
        nombre: "Cálculo / Quantitative Methods",
        semestre: 2,
        codigo: "—",
        creditos: 8,
        prereqs: "Álgebra",
        contenidos: [
          "Cálculo diferencial aplicado a negocios",
          "Optimización básica",
          "Funciones de varias variables (introducción)",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "medio",
        cursoUANDES: null,
        splitDesde: "Cálculo en una Variable o Cálculo Diferencial general, nivel introductorio.",
      },
      {
        nombre: "Statistics",
        semestre: 3,
        codigo: "—",
        creditos: 6,
        prereqs: "Cálculo",
        contenidos: [
          "Descriptive statistics",
          "Probability",
          "Inference and hypothesis testing",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUANDES: null,
      },
    ],
  },
  {
    id: "bachillerato-ing",
    nombre: "Bachillerato de Ingeniería Civil",
    facultad: "Ingeniería y Ciencias Aplicadas",
    duracion: "2 semestres (ingreso a Ingenierías Civiles)",
    mallaUrl: "https://admision.uandes.cl/carreras/programas-de-bachillerato/bachillerato-de-ingenieria-civil",
    ramos: [
      {
        nombre: "Nivelación Matemática",
        semestre: 1,
        creditos: 6,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Razonamiento lógico-matemático",
          "Álgebra básica y funciones",
          "Preparación para Álgebra e Introducción al Cálculo",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Precálculo desde Cero (68 mód) + Nivelación Ingeniería (43 mód).",
      },
    ],
  },
  {
    id: "bachillerato-icom",
    nombre: "Bachillerato de Ingeniería Comercial",
    facultad: "Ciencias Económicas y Empresariales",
    duracion: "2 semestres (ingreso a Ing. Comercial)",
    mallaUrl: "https://admision.uandes.cl/carreras/programas-de-bachillerato/bachillerato-de-ingenieria-comercial",
    ramos: [
      {
        nombre: "Nivelación Matemática",
        semestre: 1,
        creditos: 6,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Razonamiento lógico-matemático",
          "Álgebra básica y funciones",
          "Preparación para Álgebra (MAD1101)",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        cursoUANDES: null,
        splitDesde: "Precálculo desde Cero (68 mód).",
      },
    ],
  },
];

// Carreras sin ramos matemáticos significativos
const sinMatematicas = [
  "Medicina",
  "Odontología",
  "Enfermería",
  "Obstetricia",
  "Psicología",
  "Derecho",
  "Periodismo y Comunicación Estratégica",
  "Educación de Párvulos",
  "Pedagogía Básica",
  "Pedagogía Básica Bilingüe",
  "Filosofía",
  "Historia",
  "Literatura",
];

const fuentes = [
  // Mallas
  { tipo: "Malla", nombre: "Ing. Civil Industrial", url: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-Industrial-1.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Industrial (2022)", url: "https://www.uandes.cl/wp-content/uploads/2018/09/malla_ingenieria_civil_industrial-_2022.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Industrial (2023)", url: "https://admision.uandes.cl/docs/default-source/carreras/documentos-area-ingenieria-y-administracion/ingenieria-civil-industrial/malla_ingenieria_civil_industrial-_2023.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil en Obras Civiles", url: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-en-Obras-Civiles.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil en Ciencias de la Computación", url: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-en-Computacio%CC%81n.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Eléctrica", url: "https://www.uandes.cl/wp-content/uploads/2018/09/Ingenieri%CC%81a-Civil-Ele%CC%81ctrica-1.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Química (nueva 2026)", url: "https://admision.uandes.cl/docs/default-source/carreras/documentos-area-ingenieria-y-administracion/ingenieria-civil-ambiental/malla-ing-civil-quimica-uandes.pdf" },
  { tipo: "Malla", nombre: "Ing. Comercial (2024)", url: "https://www.uandes.cl/wp-content/uploads/2025/02/Malla-curricular-Ingenieria-Comercial-2024.pdf" },
  { tipo: "Malla", nombre: "Ing. Comercial (antigua)", url: "https://www.uandes.cl/wp-content/uploads/2018/04/ICOM.pdf" },
  { tipo: "Malla", nombre: "International Business (2023)", url: "https://admision.uandes.cl/docs/default-source/carreras/documentos-area-ingenieria-y-administracion/international-business/malla_international_business_2023.pdf" },
  // Programas / Contenidos
  { tipo: "Programa", nombre: "Álgebra e Intro al Cálculo (Studocu)", url: "https://www.studocu.com/cl/course/universidad-de-los-andes-chile/algebra-e-introduccion-al-calculo/3459983" },
  { tipo: "Programa", nombre: "Cálculo I MAD1102 (Studocu)", url: "https://www.studocu.com/cl/course/universidad-de-los-andes-chile/calculo-i/3459827" },
  { tipo: "Programa", nombre: "Álgebra Lineal (Studocu)", url: "https://www.studocu.com/cl/course/universidad-de-los-andes-chile/algebra-lineal/3459988" },
  { tipo: "Programa", nombre: "Normativa ICOM (con malla y códigos)", url: "https://www.uandes.cl/wp-content/uploads/2020/01/NORMATIVA-VIGENTE-ICOM.pdf" },
  // Portales
  { tipo: "Portal", nombre: "Carreras UANDES - Admisión 2026", url: "https://admision.uandes.cl/carreras" },
  { tipo: "Portal", nombre: "Admisión UANDES 2026", url: "https://admision.uandes.cl/admision-2026" },
  { tipo: "Portal", nombre: "Facultad de Ingeniería y Ciencias Aplicadas", url: "https://www.uandes.cl/universidad/facultades/facultad-ingenieria/" },
  { tipo: "Portal", nombre: "Ing. Comercial - Admisión", url: "https://admision.uandes.cl/carreras/area-ingenieria-y-administracion/ingenieria-comercial" },
  { tipo: "Portal", nombre: "Ing. Civil Industrial - Admisión", url: "https://admision.uandes.cl/carreras/area-ingenieria-y-administracion/ingenieria-civil-industrial" },
  { tipo: "Portal", nombre: "Ing. Civil Química - Admisión", url: "https://admision.uandes.cl/carreras/area-ingenieria-y-administracion/ingenieria-civil-quimica" },
  { tipo: "Portal", nombre: "International Business - Admisión", url: "https://admision.uandes.cl/carreras/area-ingenieria-y-administracion/international-business" },
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
  const cursoUANDESObj = curso.cursoUANDES ? seRemontaCursos.find(sr => sr.id === curso.cursoUANDES) : null;
  const tieneUANDES = !!cursoUANDESObj;

  return (
    <div className={`border rounded-lg mb-2 overflow-hidden shadow-sm ${tieneUANDES ? "bg-green-50 border-green-300" : "bg-white"}`}>
      <button
        onClick={onToggle}
        className="w-full text-left px-4 py-3 flex items-center justify-between hover:bg-gray-50"
      >
        <div className="flex items-center gap-3 flex-wrap">
          <span className="font-semibold text-gray-800">{curso.nombre}</span>
          <span className="text-xs text-gray-500">S{curso.semestre}</span>
          {curso.creditos && (
            <span className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded">{curso.creditos} créditos</span>
          )}
          <MatchBadge level={curso.matchLevel} />
          {tieneUANDES && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-green-600 text-white font-medium">
              Curso UANDES existente
            </span>
          )}
          {!tieneUANDES && curso.splitDesde && (
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
              {curso.codigo && (
                <p className="text-sm text-gray-600 mb-1">
                  <span className="font-medium">Código:</span> {curso.codigo}
                </p>
              )}
              {curso.horas && (
                <p className="text-sm text-gray-600 mb-1">
                  <span className="font-medium">Horas:</span> {curso.horas}
                </p>
              )}
              <p className="text-sm text-gray-600 mb-1">
                <span className="font-medium">Prerrequisitos:</span> {curso.prereqs || "—"}
              </p>
              {curso.fuentePrograma && (
                <a
                  href={curso.fuentePrograma}
                  target="_blank"
                  rel="noopener"
                  className="text-xs text-blue-600 underline"
                >
                  Ver programa / materiales del curso
                </a>
              )}
            </div>
            <div>
              <p className="text-sm font-medium text-gray-700 mb-1">Contenidos:</p>
              <ul className="text-sm text-gray-600 space-y-0.5">
                {curso.contenidos?.map((c, i) => (
                  <li key={i} className="flex gap-1">
                    <span className="text-gray-400">•</span> {c}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          {tieneUANDES && (
            <div className="mt-3 pt-3 border-t">
              <div className="bg-green-100 border border-green-300 rounded-lg p-3">
                <p className="text-sm font-semibold text-green-800 mb-1">Ya existe curso UANDES en Se Remonta:</p>
                <span className="text-sm text-green-700">
                  {cursoUANDESObj.nombre} ({cursoUANDESObj.modulos} módulos)
                </span>
              </div>
            </div>
          )}
          {!tieneUANDES && curso.splitDesde && (
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
          {curso.bibliografia && (
            <div className="mt-3 pt-3 border-t">
              <p className="text-sm font-medium text-gray-700 mb-1">Bibliografía:</p>
              <ul className="text-xs text-gray-500 space-y-0.5">
                {curso.bibliografia.map((b, i) => (
                  <li key={i}>- {b}</li>
                ))}
              </ul>
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

  // Include plan comun ramos if this carrera shares plan comun
  const planComun = carreras.find(c => c.id === "plan-comun-ing");
  const sharesPlanComun = carrera.nota?.includes("Comparte plan común");
  const allRamos = sharesPlanComun && planComun
    ? [...planComun.ramos.map(r => ({ ...r, _fromPlanComun: true })), ...carrera.ramos]
    : carrera.ramos;

  const totalMatch = allRamos.filter((r) => r.matchLevel === "alto" || r.matchLevel === "medio").length;

  return (
    <div className="border rounded-xl mb-4 overflow-hidden shadow-sm">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full text-left px-5 py-4 bg-white hover:bg-gray-50 flex items-center justify-between"
      >
        <div>
          <h3 className="font-bold text-lg text-gray-800">{carrera.nombre}</h3>
          <p className="text-sm text-gray-500">
            {carrera.facultad} · {carrera.duracion} · {allRamos.length} ramos matemáticos
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
          {sharesPlanComun && (
            <div className="mt-3 mb-3 bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-xs text-blue-700">Los ramos del Plan Común de Ingeniería (S1-S4) se muestran primero, seguidos de los ramos propios de la especialidad.</p>
            </div>
          )}
          <div className="mt-3">
            {allRamos.map((curso, idx) => (
              <div key={idx}>
                {idx === 0 && sharesPlanComun && (
                  <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2 mt-2">Plan Común</p>
                )}
                {curso._fromPlanComun === undefined && sharesPlanComun && idx === planComun.ramos.length && (
                  <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2 mt-4">Ramos de Especialidad</p>
                )}
                <CursoCard
                  curso={curso}
                  expanded={expandedCursos[idx]}
                  onToggle={() => toggleCurso(idx)}
                />
              </div>
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
  const relevantes = seRemontaCursos.filter(c => c.tipo === "general");
  const matrix = relevantes.map((sr) => {
    const matches = [];
    carreras.forEach((carrera) => {
      // For carreras that share plan comun, include those ramos
      const planComun = carreras.find(c => c.id === "plan-comun-ing");
      const sharesPlanComun = carrera.nota?.includes("Comparte plan común");
      const allRamos = sharesPlanComun && planComun
        ? [...planComun.ramos, ...carrera.ramos]
        : carrera.ramos;

      allRamos.forEach((ramo) => {
        if (ramo.match?.includes(sr.id)) {
          // Avoid duplicates from plan comun
          const exists = matches.some(m => m.ramo === ramo.nombre && m.carrera === carrera.nombre);
          if (!exists) {
            matches.push({
              carrera: carrera.nombre,
              carreraId: carrera.id,
              ramo: ramo.nombre,
              semestre: ramo.semestre,
              level: ramo.matchLevel,
              tieneUANDES: !!ramo.cursoUANDES,
            });
          }
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
            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">General</span>
            <span className="text-sm text-gray-500">({sr.matches.length} coincidencias)</span>
          </div>
          <div className="p-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-2 font-medium">Carrera</th>
                  <th className="pb-2 font-medium">Ramo UANDES</th>
                  <th className="pb-2 font-medium">Semestre</th>
                  <th className="pb-2 font-medium">Estado</th>
                </tr>
              </thead>
              <tbody>
                {sr.matches.map((m, i) => (
                  <tr key={i} className="border-b last:border-0">
                    <td className="py-2 text-gray-700">{m.carrera}</td>
                    <td className="py-2 font-medium">{m.ramo}</td>
                    <td className="py-2 text-gray-500">S{m.semestre}</td>
                    <td className="py-2">
                      {m.tieneUANDES ? (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-green-600 text-white">Curso UANDES listo</span>
                      ) : (
                        <MatchBadge level={m.level} />
                      )}
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
  let totalConUANDES = 0;
  let totalSplitOportunidad = 0;

  carreras.forEach((c) => {
    const planComun = carreras.find(pc => pc.id === "plan-comun-ing");
    const sharesPlanComun = c.nota?.includes("Comparte plan común");
    const allRamos = sharesPlanComun && planComun
      ? [...planComun.ramos, ...c.ramos]
      : c.ramos;

    totalRamos += allRamos.length;
    allRamos.forEach((r) => {
      if (r.matchLevel === "alto") totalMatchAlto++;
      if (r.matchLevel === "medio") totalMatchMedio++;
      if (r.cursoUANDES) totalConUANDES++;
      if (!r.cursoUANDES && r.splitDesde) totalSplitOportunidad++;
    });
  });

  return (
    <div className="space-y-4 mb-6">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <div className="bg-blue-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-blue-700">{carreras.length}</div>
          <div className="text-xs text-blue-600">Carreras con mat.</div>
        </div>
        <div className="bg-purple-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-purple-700">{totalRamos}</div>
          <div className="text-xs text-purple-600">Ramos matemáticos</div>
        </div>
        <div className="bg-green-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-green-700">{totalConUANDES}</div>
          <div className="text-xs text-green-600">Cursos UANDES listos</div>
        </div>
        <div className="bg-amber-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-amber-700">{totalSplitOportunidad}</div>
          <div className="text-xs text-amber-600">Oportunidades split</div>
        </div>
        <div className="bg-gray-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-gray-700">{seRemontaCursos.length}</div>
          <div className="text-xs text-gray-600">Cursos totales SR</div>
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
            <div className="w-10 h-10 bg-emerald-700 rounded-xl flex items-center justify-center text-white font-bold text-lg">
              UA
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">
                Ramos Matemáticos UANDES
              </h1>
              <p className="text-sm text-gray-500">
                Investigación para splitting con Se Remonta — Universidad de los Andes
              </p>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-3">
            Análisis de <strong>todas las carreras</strong> de pregrado UANDES (27 carreras + 8 bachilleratos).
            Se identificaron <strong>{carreras.length} carreras/programas</strong> con ramos matemáticos significativos
            y <strong>{sinMatematicas.length} carreras sin matemáticas</strong>.
            Todas las Ingenierías Civiles comparten un <strong>plan común</strong> de 4 semestres con los mismos ramos matemáticos.
          </p>
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
                  ? "bg-emerald-700 text-white shadow"
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
              className="w-full px-4 py-2.5 rounded-xl border bg-white mb-4 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
            {carrerasFiltradas.map((c) => (
              <CarreraSection key={c.id} carrera={c} />
            ))}

            {/* Carreras sin matemáticas */}
            <div className="mt-6 border rounded-xl bg-white p-5 shadow-sm">
              <h3 className="font-bold text-gray-700 mb-3">
                Carreras sin ramos matemáticos significativos ({sinMatematicas.length})
              </h3>
              <p className="text-sm text-gray-500 mb-3">
                Estas carreras no tienen cursos dedicados de matemáticas en su malla, o solo incluyen
                estadística/bioestadística básica sin contenido de álgebra o cálculo.
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
              Todos los datos fueron extraídos directamente de documentos oficiales de la UANDES,
              mallas curriculares descargadas, y materiales de curso verificados.
            </p>
            {["Malla", "Programa", "Portal"].map((tipo) => (
              <div key={tipo} className="mb-5">
                <h4 className="font-semibold text-sm text-gray-700 mb-2 uppercase tracking-wide">{tipo}s</h4>
                <div className="space-y-1">
                  {fuentes
                    .filter((f) => f.tipo === tipo)
                    .map((f, i) => (
                      <div key={i} className="flex items-center gap-2 text-sm">
                        <span className={`w-2 h-2 rounded-full ${tipo === "Malla" ? "bg-blue-400" : tipo === "Programa" ? "bg-green-400" : "bg-purple-400"}`} />
                        <span className="text-gray-700 font-medium">{f.nombre}</span>
                        <a href={f.url} target="_blank" rel="noopener" className="text-blue-500 underline text-xs truncate max-w-xs">
                          {f.url.replace("https://www.uandes.cl/", "").replace("https://admision.uandes.cl/", "admision/")}
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
          Investigación Se Remonta × UANDES · Datos verificados abril 2026 · Fuentes oficiales Universidad de los Andes
        </div>
      </div>
    </div>
  );
}
