import { useState } from "react";

// ═══════════════════════════════════════════════════════════════
// DATOS VERIFICADOS - Investigación Ramos Matemáticos UDD
// Fuentes: Mallas curriculares oficiales UDD (PDFs) + Programas de asignatura
// Fecha de investigación: Abril 2026
// ═══════════════════════════════════════════════════════════════

// ── CATÁLOGO COMPLETO SE REMONTA (33 cursos) ──────────────────
// Fuente: www.seremonta.store + archivos proyecto Se Remonta
// Leyenda tipo: "general" = multi-universidad, "uc" = PUC, "uai" = UAI, "udd" = UDD
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
  // ─── CURSOS UDD (YA EXISTEN) ───
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

// Subconjunto para matching UDD: solo cursos generales + cursos UDD existentes
const cursosParaMatch = seRemontaCursos.filter(c => c.tipo === "general" || c.tipo === "udd");

const carreras = [
  {
    id: "plan-comun",
    nombre: "Ingeniería Civil Plan Común",
    facultad: "Ingeniería",
    duracion: "4 semestres comunes + especialización",
    especialidades: [
      "Ing. Civil Industrial",
      "Ing. Civil en Obras Civiles",
      "Ing. Civil en Minería",
      "Ing. Civil en Informática e Innovación Tecnológica",
      "Ing. Civil en Informática e Inteligencia Artificial",
    ],
    mallaUrl: "https://www.udd.cl/mallas/ingenieriacivilplancomun.pdf",
    ramos: [
      {
        nombre: "Álgebra",
        semestre: 1,
        codigo: "IIM—",
        creditos: 12,
        horas: "6 hrs/sem + 2 ayudantía",
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Conjuntos y lógica",
          "Números reales: axiomas, desigualdades, valor absoluto",
          "Polinomios: operaciones, división sintética, raíces",
          "Álgebra finita: sumatorias, progresiones, factorial, binomio",
          "Matrices y determinantes",
          "Sistemas de ecuaciones lineales (Gauss-Jordan)",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Precálculo desde Cero (68 módulos) cubre conjuntos, álgebra, funciones y trigonometría. Nivelación Ingeniería complementa.",
        fuentePrograma: "https://www.udd.cl/wp-content/uploads/2021/02/programa-de-algebra.pdf",
      },
      {
        nombre: "Introducción al Cálculo",
        semestre: 1,
        codigo: "IIM—",
        creditos: 12,
        horas: "6 hrs/sem + 2 ayudantía",
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Funciones reales de variable real",
          "Función lineal, cuadrática, potencia, exponencial, logarítmica",
          "Funciones trigonométricas",
          "Límites: definición, propiedades, laterales",
          "Continuidad de funciones",
          "Introducción a la derivada",
        ],
        match: ["precalculo-cero", "calculo-1var-gen"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Precálculo desde Cero cubre funciones y trigonometría. Cálculo en una Variable (85 mód) cubre límites y derivadas.",
      },
      {
        nombre: "Geometría",
        semestre: 2,
        codigo: "IIM—",
        creditos: 12,
        horas: "6 hrs/sem + 2 ayudantía",
        prereqs: "Álgebra",
        contenidos: [
          "Geometría analítica plana: rectas, circunferencias, cónicas",
          "Vectores en R² y R³",
          "Rectas y planos en el espacio",
          "Números complejos (forma binomial, polar, exponencial)",
          "Trigonometría avanzada",
        ],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        cursoUDD: null,
        splitDesde: "Precálculo desde Cero cubre geometría analítica y trigonometría. Falta contenido de números complejos y vectores 3D.",
      },
      {
        nombre: "Cálculo Diferencial",
        semestre: 2,
        codigo: "IIM—",
        creditos: 12,
        horas: "6 hrs/sem + 2 ayudantía",
        prereqs: "Introducción al Cálculo",
        contenidos: [
          "Derivadas: definición, reglas de derivación",
          "Derivación implícita y logarítmica",
          "Teoremas de valor medio, Rolle, L'Hôpital",
          "Aplicaciones: máximos, mínimos, concavidad, inflexión",
          "Análisis y graficación de funciones",
          "Diferenciales y aproximaciones",
        ],
        match: ["calc-dif-udd-civil", "calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "alto",
        cursoUDD: "calc-dif-udd-civil",
        splitDesde: null,
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 3,
        codigo: "IIM126A",
        creditos: 12,
        horas: "6 hrs/sem + 2 ayudantía (102 + 34 hrs totales)",
        prereqs: "Álgebra",
        contenidos: [
          "Matrices y sistemas de ecuaciones lineales (Gauss, Cramer)",
          "Planos y rectas en el espacio (variedades lineales en R², R³)",
          "Espacios vectoriales: definición, subespacio, independencia lineal, base, dimensión",
          "Producto interior, ortogonalización de Gramm-Schmidt",
          "Transformaciones lineales: núcleo, imagen, teorema de dimensión",
          "Valores y vectores propios, diagonalización",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Álgebra Lineal general (52 mód, 8 capítulos) cubre todos los temas: sistemas, matrices, determinantes, espacios vectoriales, valores propios, ortogonalidad.",
        fuentePrograma: "https://www.udd.cl/wp-content/uploads/2015/04/Algebra-Lineal-IIM126A.pdf",
        bibliografia: [
          "Grossman, S. – Álgebra Lineal (McGraw-Hill)",
          "Lay, D. – Álgebra Lineal y sus Aplicaciones (Pearson)",
        ],
      },
      {
        nombre: "Cálculo Integral",
        semestre: 3,
        codigo: "IIM—",
        creditos: 12,
        horas: "6 hrs/sem + 2 ayudantía",
        prereqs: "Cálculo Diferencial",
        contenidos: [
          "Antiderivadas y integral indefinida",
          "Técnicas de integración: sustitución, partes, fracciones parciales, trigonométricas",
          "Integral definida y Teorema Fundamental del Cálculo",
          "Aplicaciones: áreas, volúmenes, longitud de arco",
          "Integrales impropias",
          "Sucesiones y series numéricas",
        ],
        match: ["calc-int-udd-civil", "calculo-1var-gen", "calculo-int-gen"],
        matchLevel: "alto",
        cursoUDD: "calc-int-udd-civil",
        splitDesde: null,
      },
      {
        nombre: "Cálculo Multivariable",
        semestre: 4,
        codigo: "IIM—",
        creditos: 12,
        horas: "6 hrs/sem + 2 ayudantía",
        prereqs: "Cálculo Integral, Álgebra Lineal",
        contenidos: [
          "Funciones de varias variables, curvas y superficies de nivel",
          "Derivadas parciales, gradiente, derivada direccional",
          "Máximos y mínimos de funciones de varias variables",
          "Multiplicadores de Lagrange",
          "Integrales dobles y triples",
          "Cambio de coordenadas (polares, cilíndricas, esféricas)",
        ],
        match: ["calculo-vvar-gen", "calculo-vec-gen"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre derivadas parciales, Lagrange, integrales múltiples. Cálculo Vectorial (31 mód) complementa.",
        fuentePrograma: "https://www.udd.cl/relaciones-internacionales/files/2014/10/Calculo-Multivariable.pdf",
      },
      {
        nombre: "Ecuaciones Diferenciales",
        semestre: 4,
        codigo: "IIM—",
        creditos: 12,
        horas: "6 hrs/sem + 2 ayudantía",
        prereqs: "Cálculo Integral",
        contenidos: [
          "EDO de primer orden: separables, lineales, exactas, Bernoulli",
          "EDO de segundo orden: coeficientes constantes, variación de parámetros",
          "Transformada de Laplace",
          "Sistemas de ecuaciones diferenciales",
          "Aplicaciones a ingeniería y ciencias",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Ecuaciones Diferenciales general (42 mód) cubre EDO 1er y 2do orden, Laplace, sistemas. Match casi directo.",
        fuentePrograma: "https://www.udd.cl/wp-content/uploads/2015/11/Ecuaciones-Diferenciales.pdf",
      },
      {
        nombre: "Probabilidades y Estadística",
        semestre: 4,
        codigo: "IIM—",
        creditos: 10,
        horas: "4 hrs/sem + 2 ayudantía",
        prereqs: "Cálculo Integral",
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
        cursoUDD: null,
        fuentePrograma: "https://www.udd.cl/relaciones-internacionales/files/2014/10/Probabilidades.pdf",
      },
    ],
  },
  {
    id: "ing-comercial",
    nombre: "Ingeniería Comercial",
    facultad: "Economía y Negocios",
    duracion: "10 semestres",
    mallaUrl: "https://www.udd.cl/mallas/ingcomercial.pdf",
    ramos: [
      {
        nombre: "Álgebra",
        semestre: 1,
        codigo: "ECM113",
        creditos: 10,
        horas: "3 teóricas + 1 ayudantía/sem (102 + 34 hrs totales)",
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Conjuntos: operaciones, Venn, cardinalidad",
          "Álgebra en números reales: desigualdades, inecuaciones, valor absoluto",
          "Polinomios: operaciones, división sintética, raíces, fracciones parciales",
          "Álgebra finita: sumatorias, progresiones, factorial, combinatorio, binomio",
          "Matrices y determinantes: operaciones, inversa, propiedades",
          "Sistemas de ecuaciones lineales (Gauss-Jordan)",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Precálculo desde Cero (68 mód) cubre la mayoría del contenido de este ramo.",
        fuentePrograma: "https://www.udd.cl/wp-content/uploads/2021/02/programa-de-algebra.pdf",
        bibliografia: [
          "Kovacic, M. – Matemática: Aplicación a las ciencias Económico-Administrativas (Addison-Wesley)",
          "Zill, D. & Dewar, J. – Álgebra y trigonometría (McGraw-Hill)",
        ],
      },
      {
        nombre: "Cálculo",
        semestre: 2,
        codigo: "ECM123",
        creditos: 10,
        horas: "2 teóricas + 1 ayudantía/sem",
        prereqs: "Álgebra (ECM113)",
        contenidos: [
          "Relaciones y funciones reales (lineal, cuadrática, exponencial, logarítmica, trigonométricas)",
          "Límites y continuidad de funciones reales",
          "Derivadas: concepto, reglas, orden superior, implícita, diferenciales",
          "Aplicaciones de derivadas: L'Hôpital, máximos/mínimos, concavidad",
          "Funciones de varias variables: derivadas parciales, Cobbs-Douglas, Hessiano, Lagrange",
        ],
        match: ["calc1-udd-icom", "calc2-udd-icom", "calculo-1var-gen", "calculo-vvar-gen"],
        matchLevel: "alto",
        cursoUDD: "calc1-udd-icom",
        splitDesde: null,
        nota: "Ya existen Cálculo I UDD Ing. Comercial (47 mód) y Cálculo II UDD Ing. Comercial (33 mód).",
        fuentePrograma: "https://www.udd.cl/wp-content/uploads/2015/10/CALCULO-I.pdf",
        bibliografia: [
          "Zill, D. & Dewar, J. – Álgebra y trigonometría (McGraw-Hill)",
          "Hoffmann, L. & Bradley, G. – Cálculo para Administración, Economía y Ciencias Sociales (McGraw-Hill)",
          "Larson, R. et al. – Cálculo y Geometría Analítica (McGraw-Hill)",
        ],
      },
      {
        nombre: "Probabilidades e Inferencia",
        semestre: 3,
        codigo: "ECM—",
        creditos: 10,
        horas: "3 teóricas + 1 ayudantía/sem",
        prereqs: "Cálculo",
        contenidos: [
          "Probabilidad: axiomas, teorema de Bayes",
          "Variables aleatorias y distribuciones",
          "Estimación puntual y por intervalos",
          "Pruebas de hipótesis",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
      {
        nombre: "Métodos Estadísticos",
        semestre: 4,
        codigo: "ECM—",
        creditos: 10,
        horas: "3 teóricas + 1 ayudantía/sem",
        prereqs: "Probabilidades e Inferencia",
        contenidos: [
          "Regresión lineal simple y múltiple",
          "Análisis de varianza (ANOVA)",
          "Series de tiempo",
          "Métodos no paramétricos",
        ],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
    ],
  },
  {
    id: "geologia",
    nombre: "Geología",
    facultad: "Ingeniería",
    duracion: "12 semestres",
    mallaUrl: "https://www.udd.cl/mallas/geologia.pdf",
    ramos: [
      {
        nombre: "Álgebra",
        semestre: 1,
        creditos: 12,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Mismo programa que Ing. Civil Plan Común"],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Mismo split que Ing. Civil: Precálculo desde Cero + Nivelación Ing.",
      },
      {
        nombre: "Introducción al Cálculo",
        semestre: 1,
        creditos: 12,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Mismo programa que Ing. Civil Plan Común"],
        match: ["precalculo-cero", "calculo-1var-gen"],
        matchLevel: "alto",
        cursoUDD: null,
      },
      {
        nombre: "Geometría",
        semestre: 2,
        creditos: 12,
        prereqs: "Álgebra",
        contenidos: ["Mismo programa que Ing. Civil Plan Común"],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        cursoUDD: null,
      },
      {
        nombre: "Cálculo Diferencial",
        semestre: 2,
        creditos: 12,
        prereqs: "Introducción al Cálculo",
        contenidos: ["Mismo programa que Ing. Civil Plan Común"],
        match: ["calc-dif-udd-civil", "calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "alto",
        cursoUDD: "calc-dif-udd-civil",
        splitDesde: null,
        nota: "Comparte el curso UDD Cálculo Diferencial Ing. Civil (58 mód).",
      },
      {
        nombre: "Cálculo Integral",
        semestre: 3,
        creditos: 12,
        prereqs: "Cálculo Diferencial",
        contenidos: ["Mismo programa que Ing. Civil Plan Común"],
        match: ["calc-int-udd-civil", "calculo-1var-gen", "calculo-int-gen"],
        matchLevel: "alto",
        cursoUDD: "calc-int-udd-civil",
        splitDesde: null,
        nota: "Comparte el curso UDD Cálculo Integral Ing. Civil (37 mód).",
      },
      {
        nombre: "Probabilidades y Estadística",
        semestre: 4,
        creditos: 10,
        prereqs: "Cálculo Integral",
        contenidos: ["Mismo programa que Ing. Civil Plan Común"],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
      {
        nombre: "Ecuaciones Diferenciales",
        semestre: 5,
        creditos: 12,
        prereqs: "Cálculo Integral",
        contenidos: ["Mismo programa que Ing. Civil Plan Común"],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Ecuaciones Diferenciales general (42 mód).",
      },
    ],
  },
  {
    id: "gba",
    nombre: "Global Business Administration",
    facultad: "Economía y Negocios",
    duracion: "8 semestres",
    mallaUrl: "https://www.udd.cl/mallas/gba.pdf",
    ramos: [
      {
        nombre: "Álgebra",
        semestre: 1,
        creditos: 10,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Mismo programa que Ing. Comercial (orientado a negocios)"],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Precálculo desde Cero (68 mód).",
      },
      {
        nombre: "Cálculo",
        semestre: 2,
        creditos: 10,
        prereqs: "Álgebra",
        contenidos: ["Mismo programa que Ing. Comercial"],
        match: ["calc1-udd-icom", "calc2-udd-icom", "calculo-1var-gen"],
        matchLevel: "alto",
        cursoUDD: "calc1-udd-icom",
        nota: "Ya existen cursos UDD Ing. Comercial que aplican directamente.",
      },
      {
        nombre: "Probabilidades e Inferencia",
        semestre: 3,
        creditos: 10,
        prereqs: "Cálculo",
        contenidos: ["Probabilidad, variables aleatorias, estimación, hipótesis"],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
      {
        nombre: "Métodos Estadísticos",
        semestre: 4,
        creditos: 10,
        prereqs: "Probabilidades e Inferencia",
        contenidos: ["Regresión, ANOVA, series de tiempo"],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
    ],
  },
  {
    id: "ncd",
    nombre: "Negocios y Ciencia de Datos",
    facultad: "Economía y Negocios",
    duracion: "10 semestres",
    mallaUrl: "https://www.udd.cl/mallas/ncd.pdf",
    nota: "Nueva 2026. Doble título con Ing. Comercial.",
    ramos: [
      {
        nombre: "Matemática Avanzada",
        semestre: 1,
        creditos: 10,
        prereqs: "Sin prerrequisitos",
        contenidos: [
          "Álgebra y funciones orientadas a ciencia de datos",
          "Cálculo diferencial e integral aplicado",
          "Álgebra lineal básica (matrices, vectores)",
        ],
        match: ["precalculo-cero", "calculo-1var-gen", "algebra-lineal-gen"],
        matchLevel: "medio",
        cursoUDD: null,
        splitDesde: "Combina contenido de Precálculo + Cálculo 1 Var + Álgebra Lineal. Requiere selección de módulos específicos.",
      },
      {
        nombre: "Probabilidades e Inferencia",
        semestre: 2,
        creditos: 10,
        prereqs: "Matemática Avanzada",
        contenidos: ["Probabilidad, variables aleatorias, estimación, hipótesis"],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
      {
        nombre: "Métodos Estadísticos",
        semestre: 3,
        creditos: 10,
        prereqs: "Probabilidades e Inferencia",
        contenidos: ["Regresión, ANOVA, métodos estadísticos avanzados"],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
    ],
  },
  {
    id: "biomedicina",
    nombre: "Ingeniería Civil en BioMedicina",
    facultad: "Ingeniería",
    duracion: "12 semestres",
    mallaUrl: "https://www.udd.cl/mallas/ingbiomedicina.pdf",
    nota: "Nueva 2025",
    ramos: [
      {
        nombre: "Matemática Aplicada I",
        semestre: 1,
        creditos: 10,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Fundamentos matemáticos para biomedicina: álgebra, funciones"],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        cursoUDD: null,
        splitDesde: "Precálculo desde Cero, seleccionando módulos de álgebra y funciones.",
      },
      {
        nombre: "Matemática Aplicada II",
        semestre: 2,
        creditos: 10,
        prereqs: "Matemática Aplicada I",
        contenidos: ["Cálculo diferencial aplicado a biomedicina"],
        match: ["calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "medio",
        cursoUDD: null,
        splitDesde: "Cálculo en una Variable o Cálculo Diferencial general.",
      },
      {
        nombre: "Matemática Aplicada III",
        semestre: 3,
        creditos: 10,
        prereqs: "Matemática Aplicada II",
        contenidos: ["Cálculo integral, álgebra lineal aplicada"],
        match: ["calculo-1var-gen", "calculo-int-gen", "algebra-lineal-gen"],
        matchLevel: "medio",
        cursoUDD: null,
        splitDesde: "Cálculo Integral general + módulos de Álgebra Lineal.",
      },
      {
        nombre: "Matemática Aplicada IV",
        semestre: 4,
        creditos: 10,
        prereqs: "Matemática Aplicada III",
        contenidos: ["Ecuaciones diferenciales y métodos numéricos aplicados"],
        match: ["ec-dif-gen", "calculo-vvar-gen"],
        matchLevel: "medio",
        cursoUDD: null,
        splitDesde: "Ec. Diferenciales general (42 mód) + Cálculo Varias Variables (41 mód).",
      },
      {
        nombre: "Probabilidad y Estadística",
        semestre: 5,
        creditos: 10,
        prereqs: "Matemática Aplicada III",
        contenidos: ["Probabilidad, distribuciones, inferencia, bioestadística"],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
    ],
  },
  {
    id: "quimica-farmacia",
    nombre: "Química y Farmacia",
    facultad: "Ciencias de la Salud",
    duracion: "12 semestres",
    mallaUrl: "https://www.udd.cl/mallas/quimicayfarmacia.pdf",
    nota: "Nueva 2025",
    ramos: [
      {
        nombre: "Matemáticas",
        semestre: 1,
        creditos: 8,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Álgebra, funciones, ecuaciones, trigonometría básica"],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        cursoUDD: null,
        splitDesde: "Precálculo desde Cero, nivel introductorio.",
        fuentePrograma: "https://www.udd.cl/wp-content/uploads/2014/10/Matem%C3%A1ticas-I-1.pdf",
      },
      {
        nombre: "Cálculo",
        semestre: 2,
        creditos: 8,
        prereqs: "Matemáticas",
        contenidos: ["Límites, derivadas, integrales aplicadas a ciencias"],
        match: ["calculo-1var-gen", "calculo-dif-gen"],
        matchLevel: "medio",
        cursoUDD: null,
        splitDesde: "Cálculo en una Variable (85 mód) o Cálculo Diferencial general.",
      },
      {
        nombre: "Bioestadística",
        semestre: 4,
        creditos: 6,
        prereqs: "Cálculo",
        contenidos: ["Estadística descriptiva, probabilidad, inferencia en contexto biológico"],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
    ],
  },
  {
    id: "bachillerato-ic",
    nombre: "Bachillerato en Ingeniería Comercial",
    facultad: "Economía y Negocios",
    duracion: "2 semestres (ingreso a Ing. Comercial)",
    mallaUrl: "https://www.udd.cl/mallas/ingcomercial.pdf",
    ramos: [
      {
        nombre: "Pensamiento Matemático",
        semestre: 1,
        creditos: 8,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Razonamiento lógico-matemático, resolución de problemas"],
        match: ["precalculo-cero"],
        matchLevel: "bajo",
        cursoUDD: null,
      },
      {
        nombre: "Álgebra",
        semestre: 2,
        creditos: 10,
        prereqs: "Pensamiento Matemático",
        contenidos: ["Mismo programa que Álgebra de Ing. Comercial"],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        cursoUDD: null,
        splitDesde: "Precálculo desde Cero (68 mód).",
      },
    ],
  },
  {
    id: "arquitectura",
    nombre: "Arquitectura",
    facultad: "Arquitectura y Arte",
    duracion: "12 semestres",
    mallaUrl: "https://www.udd.cl/mallas/arquitectura.pdf",
    ramos: [
      {
        nombre: "Componentes de la Matemática",
        semestre: 1,
        creditos: 6,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Matemática aplicada a arquitectura: geometría, proporciones, cálculo básico"],
        match: ["precalculo-cero"],
        matchLevel: "bajo",
        cursoUDD: null,
      },
    ],
  },
  {
    id: "medicina",
    nombre: "Medicina",
    facultad: "Medicina CAS-UDD",
    duracion: "14 semestres",
    mallaUrl: "https://www.udd.cl/mallas/medicina.pdf",
    ramos: [
      {
        nombre: "Estadística",
        semestre: "1-2 (Anillo I)",
        creditos: 4,
        prereqs: "Sin prerrequisitos",
        contenidos: ["Estadística descriptiva, probabilidad, bioestadística básica"],
        match: [],
        matchLevel: "ninguno",
        cursoUDD: null,
      },
    ],
  },
];

// Carreras sin ramos matemáticos significativos
const sinMatematicas = [
  "Publicidad y Marketing",
  "Periodismo y Comunicación",
  "Derecho",
  "Diseño",
  "Psicología",
  "Cine y Comunicación Audiovisual",
  "Ciencia Política y Políticas Públicas",
  "Pedagogía en Educación Básica",
  "Pedagogía en Educación de Párvulos",
  "Enfermería",
  "Kinesiología",
  "Nutrición y Dietética",
  "Obstetricia",
  "Odontología",
  "Tecnología Médica",
  "Terapia Ocupacional",
];

const fuentes = [
  { tipo: "Malla", nombre: "Ing. Civil Plan Común", url: "https://www.udd.cl/mallas/ingenieriacivilplancomun.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Industrial", url: "https://www.udd.cl/mallas/civil_industrial.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Informática e Innovación", url: "https://www.udd.cl/mallas/Civil_Informatica_e_Innovacion.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Informática e IA", url: "https://www.udd.cl/mallas/ing_informatica_ia.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil en Minería", url: "https://www.udd.cl/mallas/civil_en_mineria.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil en Obras Civiles", url: "https://www.udd.cl/mallas/ingenieriacivilobrasciviles.pdf" },
  { tipo: "Malla", nombre: "Ing. Comercial", url: "https://www.udd.cl/mallas/ingcomercial.pdf" },
  { tipo: "Malla", nombre: "Geología", url: "https://www.udd.cl/mallas/geologia.pdf" },
  { tipo: "Malla", nombre: "GBA", url: "https://www.udd.cl/mallas/gba.pdf" },
  { tipo: "Malla", nombre: "Negocios y Ciencia de Datos", url: "https://www.udd.cl/mallas/ncd.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil en BioMedicina", url: "https://www.udd.cl/mallas/ingbiomedicina.pdf" },
  { tipo: "Malla", nombre: "Química y Farmacia", url: "https://www.udd.cl/mallas/quimicayfarmacia.pdf" },
  { tipo: "Malla", nombre: "Arquitectura", url: "https://www.udd.cl/mallas/arquitectura.pdf" },
  { tipo: "Malla", nombre: "Medicina", url: "https://www.udd.cl/mallas/medicina.pdf" },
  { tipo: "Malla", nombre: "Psicología", url: "https://www.udd.cl/mallas/psicologia.pdf" },
  { tipo: "Malla", nombre: "Publicidad", url: "https://www.udd.cl/mallas/publicidad.pdf" },
  { tipo: "Programa", nombre: "Álgebra (Ing. Comercial)", url: "https://www.udd.cl/wp-content/uploads/2021/02/programa-de-algebra.pdf" },
  { tipo: "Programa", nombre: "Cálculo I (Ing. Comercial)", url: "https://www.udd.cl/wp-content/uploads/2015/10/CALCULO-I.pdf" },
  { tipo: "Programa", nombre: "Álgebra Lineal (Ingeniería)", url: "https://www.udd.cl/wp-content/uploads/2015/04/Algebra-Lineal-IIM126A.pdf" },
  { tipo: "Programa", nombre: "Cálculo Multivariable (Ingeniería)", url: "https://www.udd.cl/relaciones-internacionales/files/2014/10/Calculo-Multivariable.pdf" },
  { tipo: "Programa", nombre: "Ecuaciones Diferenciales (Ingeniería)", url: "https://www.udd.cl/wp-content/uploads/2015/11/Ecuaciones-Diferenciales.pdf" },
  { tipo: "Programa", nombre: "Probabilidades (Ingeniería)", url: "https://www.udd.cl/relaciones-internacionales/files/2014/10/Probabilidades.pdf" },
  { tipo: "Programa", nombre: "Matemáticas I (Ciencias Salud)", url: "https://www.udd.cl/wp-content/uploads/2014/10/Matem%C3%A1ticas-I-1.pdf" },
  { tipo: "Portal", nombre: "Carreras UDD - Admisión 2026", url: "https://www.udd.cl/admision-pregrado/carreras/" },
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
  const cursoUDDObj = curso.cursoUDD ? seRemontaCursos.find(sr => sr.id === curso.cursoUDD) : null;
  const tieneUDD = !!cursoUDDObj;

  return (
    <div className={`border rounded-lg mb-2 overflow-hidden shadow-sm ${tieneUDD ? "bg-green-50 border-green-300" : "bg-white"}`}>
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
          {tieneUDD && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-green-600 text-white font-medium">
              Curso UDD existente
            </span>
          )}
          {!tieneUDD && curso.splitDesde && (
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
                  Ver programa oficial (PDF)
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
          {tieneUDD && (
            <div className="mt-3 pt-3 border-t">
              <div className="bg-green-100 border border-green-300 rounded-lg p-3">
                <p className="text-sm font-semibold text-green-800 mb-1">Ya existe curso UDD en Se Remonta:</p>
                <span className="text-sm text-green-700">
                  {cursoUDDObj.nombre} ({cursoUDDObj.modulos} módulos)
                </span>
              </div>
            </div>
          )}
          {!tieneUDD && curso.splitDesde && (
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
  // Solo mostrar cursos generales y UDD en la matriz
  const relevantes = seRemontaCursos.filter(c => c.tipo === "general" || c.tipo === "udd");
  const matrix = relevantes.map((sr) => {
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
            tieneUDD: ramo.cursoUDD === sr.id,
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
            {sr.tipo === "udd" && <span className="text-xs bg-green-600 text-white px-2 py-0.5 rounded-full">UDD</span>}
            {sr.tipo === "general" && <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">General</span>}
            <span className="text-sm text-gray-500">({sr.matches.length} coincidencias)</span>
          </div>
          <div className="p-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-2 font-medium">Carrera</th>
                  <th className="pb-2 font-medium">Ramo UDD</th>
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
                      {m.tieneUDD ? (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-green-600 text-white">Curso UDD listo</span>
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
// CATÁLOGO COMPLETO SE REMONTA
// ═══════════════════════════════════════════════════════════════

const CatalogoCompleto = () => {
  const tipos = [
    { id: "udd", label: "UDD (existentes)", color: "bg-green-600" },
    { id: "general", label: "Generales (base splitting)", color: "bg-blue-600" },
    { id: "uc", label: "UC", color: "bg-gray-500" },
    { id: "uai", label: "UAI", color: "bg-purple-500" },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl p-4 shadow-sm">
        <h3 className="font-bold text-gray-800 mb-1">Catálogo completo: {seRemontaCursos.length} cursos</h3>
        <p className="text-sm text-gray-500">Todos los cursos disponibles en www.seremonta.store</p>
      </div>
      {tipos.map(tipo => {
        const cursos = seRemontaCursos.filter(c => c.tipo === tipo.id);
        if (cursos.length === 0) return null;
        return (
          <div key={tipo.id} className="border rounded-xl overflow-hidden bg-white shadow-sm">
            <div className="px-5 py-3 flex items-center gap-3 border-b">
              <span className={`text-xs text-white px-2 py-0.5 rounded-full ${tipo.color}`}>{tipo.label}</span>
              <span className="text-sm text-gray-500">{cursos.length} cursos</span>
            </div>
            <div className="p-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {cursos.map(c => (
                  <div key={c.id} className="border rounded-lg p-3 bg-gray-50">
                    <div className="flex items-center gap-2 mb-1">
                      <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: c.color }} />
                      <span className="font-medium text-sm text-gray-800">{c.nombre}</span>
                    </div>
                    <div className="flex flex-wrap gap-2 text-xs text-gray-500">
                      {c.modulos && <span>{c.modulos} módulos</span>}
                      {c.precio && <span>${(c.precio/1000).toFixed(0)}k CLP</span>}
                      {c.carrera && <span className="text-green-700">({c.carrera})</span>}
                    </div>
                    {c.contenidos && (
                      <div className="mt-2 text-xs text-gray-400">
                        {c.contenidos.slice(0, 3).join(" · ")}{c.contenidos.length > 3 ? " ..." : ""}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
      })}
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
  let totalConUDD = 0;
  let totalSplitOportunidad = 0;
  carreras.forEach((c) => {
    totalRamos += c.ramos.length;
    c.ramos.forEach((r) => {
      if (r.matchLevel === "alto") totalMatchAlto++;
      if (r.matchLevel === "medio") totalMatchMedio++;
      if (r.cursoUDD) totalConUDD++;
      if (!r.cursoUDD && r.splitDesde) totalSplitOportunidad++;
    });
  });

  const cursosUDD = seRemontaCursos.filter(c => c.tipo === "udd").length;

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
          <div className="text-2xl font-bold text-green-700">{cursosUDD}</div>
          <div className="text-xs text-green-600">Cursos UDD listos</div>
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
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white font-bold text-lg">
              U
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">
                Ramos Matemáticos UDD
              </h1>
              <p className="text-sm text-gray-500">
                Investigación para splitting con Se Remonta — Universidad del Desarrollo
              </p>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-3">
            Análisis de <strong>todas las carreras</strong> de pregrado UDD (29 carreras + 5 bachilleratos + Plan Común).
            Se identificaron <strong>{carreras.length} carreras</strong> con ramos matemáticos significativos
            y <strong>{sinMatematicas.length} carreras sin matemáticas</strong> o con solo estadística/bioestadística.
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
                  ? "bg-blue-600 text-white shadow"
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
              className="w-full px-4 py-2.5 rounded-xl border bg-white mb-4 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
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
                estadística/bioestadística básica como parte de un módulo integrado (no un ramo independiente con contenido de álgebra o cálculo).
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
              Todos los datos fueron extraídos directamente de documentos oficiales de la UDD.
              Las mallas curriculares corresponden al formato UDD Futuro vigente para admisión 2026.
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
                          {f.url.replace("https://www.udd.cl/", "")}
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
          Investigación Se Remonta × UDD · Datos verificados abril 2026 · Fuentes oficiales UDD
        </div>
      </div>
    </div>
  );
}
