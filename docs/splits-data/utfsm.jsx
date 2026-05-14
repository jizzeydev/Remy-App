import { useState } from "react";

// ═══════════════════════════════════════════════════════════════
// DATOS VERIFICADOS - Investigación Ramos Matemáticos UTFSM
// Fuentes:
//   - Programas oficiales Depto. Matemática USM:
//     · MATE10 Álgebra y Geometría: matematica.usm.cl/wp-content/uploads/2018/05/MATE10-Algebra-y-Geometria.pdf
//     · MATE20 Álgebra Lineal: matematica.usm.cl/wp-content/uploads/2018/05/MATE20-Algebra-Lineal.pdf
//   - Código MAT070 (Intro al Cálculo): studocu.com/cl/course/utfsm/introduccion-al-calculo/5439287
//   - Malla Ing. Civil nueva: usm.cl/admision/carreras/ (screenshot usuario, abril 2026)
//   - Plan Común Ing. Civil: usm.cl/admision/carreras/san-joaquin/ingenieria-civil-plan-comun/
//   - Programa antiguo MAT021 (referencia de contenidos): matematica.usm.cl (aprobado 2013)
//   - Cursos transversales DMAT: matematica.usm.cl/docencia/cursos-transversales/
// Fecha de investigación: Abril 2026
// ═══════════════════════════════════════════════════════════════

// ── CATÁLOGO COMPLETO SE REMONTA (cursos generales base) ─────
const seRemontaCursos = [
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
  // PLAN COMÚN INGENIERÍA CIVIL (todas las especialidades)
  // ═══════════════════════════════════════
  {
    id: "plan-comun-ing-civil",
    nombre: "Plan Común Ingeniería Civil",
    facultad: "Vicerrectoría Académica — Campus Casa Central (Valparaíso) y San Joaquín (Santiago)",
    duracion: "4 semestres comunes + especialidad (total 11-12 semestres)",
    mallaUrl: "https://usm.cl/admision/carreras/san-joaquin/ingenieria-civil-plan-comun/",
    nota: "~4.500 alumnos STEM · QS #332 · Puntaje corte ~640 · Plan Común de 2 años antes de elegir especialidad",
    especialidades: [
      "Ing. Civil (Obras Civiles)",
      "Ing. Civil Industrial",
      "Ing. Civil Informática",
      "Ing. Civil Electrónica",
      "Ing. Civil Eléctrica",
      "Ing. Civil Mecánica",
      "Ing. Civil Química",
      "Ing. Civil Telemática",
      "Ing. Civil Metalúrgica y de Materiales",
      "Ing. Civil de Minas",
      "Ing. Civil Ambiental",
      "Ing. Civil Matemática",
      "Ing. Civil en Ciencia de Datos",
    ],
    ramos: [
      // ── SEMESTRE 1 ──
      {
        nombre: "MATE10 Álgebra y Geometría",
        semestre: 1,
        prereqs: "Ingreso a carrera con MATE10 en su malla",
        fuenteContenido: "https://matematica.usm.cl/wp-content/uploads/2018/05/MATE10-Algebra-y-Geometria.pdf",
        contenidos: [
          "Fundamentos del Lenguaje Matemático: lógica, conjuntos, álgebra de reales (potencias, raíces, productos notables, ecuaciones), geometría básica escolar (Pitágoras, Thales, Herón), áreas y volúmenes",
          "Trigonometría del triángulo: ángulos y unidades, razones trigonométricas, identidades básicas, teoremas del seno y coseno, aplicaciones a modelación",
          "Geometría Analítica: sistema cartesiano, ecuación de la recta, cónicas centradas y trasladadas (circunferencia, parábola, elipse, hipérbola)",
          "Polinomios: números complejos (formas), álgebra de polinomios, división de Euclides, división sintética, raíces, multiplicidad, teoremas del resto y del factor",
          "Inducción Matemática: principio de inducción, sumatoria y propiedades, factorial, progresiones aritméticas y geométricas, Teorema del binomio, combinatoria",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre casi todo: conjuntos, álgebra de reales, trigonometría, geometría analítica, funciones polinomiales, complejos. MATE10 agrega inducción matemática y geometría escolar formal (Pitágoras, Thales, Herón) pero el match de contenido base es ~85%.",
        nota: "Programa oficial verificado (PDF Depto. Matemática). 4 créditos UTFSM, 6 SCT, 174 hrs totales. Texto guía: Zill, Dewar & Watson — Álgebra y Trigonometría (McGraw-Hill).",
      },
      {
        nombre: "MAT070 Introducción al Cálculo",
        semestre: 1,
        prereqs: "Ingreso a carrera con MAT070 en su malla",
        fuenteContenido: "https://www.studocu.com/cl/course/universidad-tecnica-federico-santa-maria/introduccion-al-calculo/5439287",
        contenidos: [
          "Funciones reales de variable real: definición, dominio, recorrido, paridad, composición, inyectividad, sobreyectividad, funciones inversas",
          "Funciones elementales: polinomiales, racionales, trigonométricas, exponenciales, logarítmicas",
          "Límites de funciones: definición ε-δ, álgebra de límites, límites laterales, límites al infinito, asíntotas",
          "Continuidad: definición, tipos de discontinuidad, propiedades, teorema del valor intermedio",
          "Derivada: definición como límite, interpretación geométrica, reglas de derivación, derivada de funciones elementales, regla de la cadena",
          "Aplicaciones de la derivada: recta tangente, máximos y mínimos locales, crecimiento, concavidad, análisis de funciones (introducción)",
        ],
        match: ["precalculo-cero", "nivelacion-ing", "calculo-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre funciones, trigonometría y funciones elementales. Nivelación Ingeniería (43 mód) complementa. Cálculo Diferencial (25k) cubre derivadas y aplicaciones. El curso USM introduce límites formales (ε-δ) y continuidad rigurosa. Cobertura combinada ~80%.",
        nota: "Código MAT070 confirmado vía Studocu. Contenidos inferidos del antiguo MAT021 (aprobado 2013) y de la estructura de la nueva malla que separa álgebra (MATE10) de cálculo (MAT070) en S1.",
      },
      // ── SEMESTRE 2 ──
      {
        nombre: "Cálculo en una Variable",
        semestre: 2,
        prereqs: "MAT070 Introducción al Cálculo",
        contenidos: [
          "Derivadas: profundización en técnicas, derivación implícita, derivadas de orden superior",
          "Aplicaciones de la derivada: teoremas del valor medio, L'Hôpital, análisis completo de funciones, optimización, aproximación lineal, polinomios de Taylor",
          "Integrales: integral definida (sumas de Riemann), Teorema Fundamental del Cálculo (1° y 2° parte), primitivas",
          "Técnicas de integración: sustitución, integración por partes, fracciones parciales, sustitución trigonométrica",
          "Aplicaciones de la integral: áreas entre curvas, volúmenes de revolución (discos, arandelas, capas cilíndricas), longitud de arco, centros de masa",
          "Integrales impropias: convergencia, criterios de comparación",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen", "calculo-int-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód) cubre completamente: derivadas, integrales, aplicaciones, Taylor, técnicas de integración. También Cálculo Diferencial (25k) + Cálculo Integral (25k) por separado. Match directo ~90%.",
        nota: "Código exacto no confirmado. Contenidos estándar para cálculo de una variable en Ing. Civil chilena, consistentes con la progresión desde MAT070 y con el antiguo MAT022.",
      },
      {
        nombre: "MATE20 Álgebra Lineal",
        semestre: 2,
        prereqs: "MATE10 Álgebra y Geometría",
        fuenteContenido: "https://matematica.usm.cl/wp-content/uploads/2018/05/MATE20-Algebra-Lineal.pdf",
        contenidos: [
          "Matrices y Sistemas de Ecuaciones: matrices nxm, tipos, álgebra de matrices, transpuesta, matrices elementales, rango, resolución de sistemas con operaciones elementales, matriz inversa, determinantes nxn y propiedades, inversa por adjunta, regla de Cramer",
          "Geometría Vectorial: vectores en el plano y en el espacio, producto punto y cruz, proyecciones, rectas y planos en el espacio",
          "Espacios Vectoriales: estructura algebraica, operaciones y propiedades, subespacios, espacio generado, independencia y dependencia lineal, base y dimensión, producto interior, ortogonalidad, proceso de Gram-Schmidt, bases ortonormales",
          "Transformaciones Lineales: definición y ejemplos, núcleo e imagen, matriz asociada a una transformación lineal",
          "Valores y Vectores Propios: valores y vectores propios de operadores lineales y matrices, diagonalización, formas lineales, bilineales y cuadráticas",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal general (52 mód, 8 capítulos) cubre todos los temas: matrices, sistemas, espacios vectoriales, transformaciones lineales, valores propios, ortogonalidad, Gram-Schmidt. Match directo y completo ~95%. El curso USM agrega formas bilineales/cuadráticas y geometría vectorial en R³.",
        nota: "Programa oficial verificado (PDF Depto. Matemática). 3 créditos UTFSM, 5 SCT, 155 hrs totales. Texto guía: Poole — Álgebra Lineal, una introducción moderna (Cengage, 4ª ed.).",
      },
      // ── SEMESTRE 3 ──
      {
        nombre: "Cálculo en Varias Variables",
        semestre: 3,
        prereqs: "Cálculo en una Variable + MATE20 Álgebra Lineal",
        contenidos: [
          "Topología en Rⁿ: distancias, normas, conjuntos abiertos y cerrados (nociones básicas)",
          "Funciones de varias variables: gráficas, conjuntos de nivel, límites y continuidad",
          "Cálculo diferencial en Rⁿ: derivadas parciales, derivadas direccionales, gradiente, plano tangente, regla de la cadena multivariable",
          "Máximos y mínimos: puntos críticos, criterio de la segunda derivada (Hessiana), multiplicadores de Lagrange",
          "Integrales múltiples: integrales dobles y triples, teorema de Fubini, cambio de variables",
          "Coordenadas curvilíneas: polares, cilíndricas y esféricas, Jacobiano, aplicaciones (centros de masa, momentos de inercia)",
        ],
        match: ["calculo-vvar-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre: derivadas parciales, gradiente, Lagrange, integrales múltiples, coordenadas curvilíneas. Match directo ~85%. El curso USM puede incluir nociones topológicas más formales.",
        nota: "Contenidos estándar para Cálc. Varias Variables en Ing. Civil chilena, consistentes con el antiguo MAT023 y con la secuencia de la nueva malla.",
      },
      {
        nombre: "Ecuaciones Diferenciales (EDO & EDP)",
        semestre: 3,
        prereqs: "Cálculo en una Variable + MATE20 Álgebra Lineal",
        contenidos: [
          "EDO de primer orden: separables, lineales, exactas, factor integrante, Bernoulli, existencia y unicidad, aplicaciones a modelación",
          "EDO lineales de orden superior: ecuaciones homogéneas y no homogéneas, Wronskiano, coeficientes constantes, coeficientes indeterminados, variación de parámetros, ecuación de Euler-Cauchy",
          "Transformada de Laplace: definición, propiedades, tabla de transformadas, resolución de EDO, funciones escalón (Heaviside), Delta de Dirac, convolución",
          "Sistemas de ecuaciones diferenciales: sistemas lineales, matriz fundamental, métodos de resolución",
          "Introducción a EDP: ecuaciones clásicas (calor, onda, Laplace), separación de variables, series de Fourier (introducción)",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Ecuaciones Diferenciales (42 mód) cubre EDO 1er y 2do orden, Laplace, sistemas. El curso USM agrega introducción a EDP (calor, onda, Laplace) y series de Fourier que NO están en el catálogo Se Remonta. Cobertura de la parte EDO ~85%, total ~70% por las EDP.",
        nota: "El nombre oficial incluye '(EDO & EDP)', lo que indica contenido más amplio que un curso puro de EDO. Contenidos consistentes con el antiguo MAT023/MAT024 y con la malla del usuario.",
      },
      // ── SEMESTRES 4+ (ramos con menos match) ──
      {
        nombre: "Probabilidad y Estadística",
        semestre: 4,
        prereqs: "Cálculo en Varias Variables",
        contenidos: [
          "Probabilidad axiomática, condicional, Bayes",
          "Variables aleatorias discretas y continuas, distribuciones",
          "Esperanza, varianza, momentos",
          "Ley de grandes números, Teorema Central del Límite",
          "Estimación e inferencia estadística (introducción)",
        ],
        match: [],
        matchLevel: "ninguno",
        nota: "Sin match con catálogo Se Remonta. Fuera del foco de splitting.",
      },
      {
        nombre: "Análisis Numérico",
        semestre: 4,
        prereqs: "Cálculo en Varias Variables + MATE20 Álgebra Lineal",
        contenidos: [
          "Errores numéricos, aritmética de punto flotante",
          "Raíces de ecuaciones (bisección, Newton-Raphson, secante)",
          "Sistemas lineales numéricos (LU, Gauss, iterativos)",
          "Interpolación polinomial (Lagrange, Newton)",
          "Integración numérica (trapecios, Simpson)",
          "EDO numéricas (Euler, Runge-Kutta)",
        ],
        match: [],
        matchLevel: "ninguno",
        nota: "Sin match con catálogo Se Remonta. Fuera del foco de splitting.",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA COMERCIAL
  // ═══════════════════════════════════════
  {
    id: "ing-comercial",
    nombre: "Ingeniería Comercial",
    facultad: "Departamento de Industrias — Campus San Joaquín",
    duracion: "10 semestres",
    mallaUrl: "https://usm.cl/admision/carreras/",
    nota: "Usa ramos MATE transversales distintos a Ing. Civil para cálculo (MATE25/MATE26), pero comparte MATE10 y MATE20",
    ramos: [
      {
        nombre: "MATE10 Álgebra y Geometría",
        semestre: 1,
        prereqs: "Ingreso a carrera",
        fuenteContenido: "https://matematica.usm.cl/wp-content/uploads/2018/05/MATE10-Algebra-y-Geometria.pdf",
        contenidos: [
          "Mismo programa que en Plan Común Ing. Civil: fundamentos, trigonometría, geometría analítica, polinomios, inducción",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre ~85% del contenido.",
        nota: "Programa compartido con Ing. Civil.",
      },
      {
        nombre: "MATE25 Cálculo Diferencial",
        semestre: 2,
        prereqs: "MATE10 Álgebra y Geometría",
        contenidos: [
          "La Derivada: definición, reglas, derivación de funciones elementales, regla de la cadena",
          "Aplicaciones de la derivada: análisis de funciones, optimización",
          "Funciones de varias variables: derivadas parciales, gradiente",
          "Diferenciación de varias variables: regla de la cadena multivariable",
          "Optimización: con y sin restricciones (Lagrange), aplicaciones a economía",
        ],
        match: ["calculo-dif-gen", "calculo-vvar-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo Diferencial (25k) cubre derivadas. Cálculo en Varias Variables (41 mód) cubre parciales y Lagrange. Curso Comercial mezcla ambos con enfoque aplicado a economía. Cobertura parcial ~60%.",
        nota: "Curso transversal para carreras no-ingeniería civil. Enfoque aplicado a administración y economía.",
      },
      {
        nombre: "MATE20 Álgebra Lineal",
        semestre: 2,
        prereqs: "MATE10 Álgebra y Geometría",
        fuenteContenido: "https://matematica.usm.cl/wp-content/uploads/2018/05/MATE20-Algebra-Lineal.pdf",
        contenidos: [
          "Mismo programa que en Plan Común: matrices, geometría vectorial, espacios vectoriales, transformaciones lineales, valores propios",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal (52 mód) cubre todos los temas. Match directo ~95%.",
        nota: "Programa compartido con Ing. Civil.",
      },
      {
        nombre: "MATE26 Cálculo Integral",
        semestre: 3,
        prereqs: "MATE25 Cálculo Diferencial",
        contenidos: [
          "La Integral: integral definida, Teorema Fundamental del Cálculo, primitivas",
          "Aplicaciones de la integral: áreas, volúmenes, aplicaciones a economía",
          "EDO de primer y segundo orden: separables, lineales, coeficientes constantes",
          "Integración múltiple: integrales dobles, aplicaciones",
        ],
        match: ["calculo-int-gen", "calculo-1var-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo Integral (25k) cubre integrales y aplicaciones. Cálculo en una Variable (85 mód) cubre también la parte integral. El curso Comercial agrega EDO básicas e integración múltiple introductoria. Cobertura ~55%.",
        nota: "Curso transversal para carreras no-ingeniería civil. Incluye EDO básicas que en Ing. Civil se ven en un ramo separado.",
      },
      {
        nombre: "Probabilidad y Estadística",
        semestre: 3,
        prereqs: "MATE25 Cálculo Diferencial",
        contenidos: [
          "Probabilidad, variables aleatorias, distribuciones, inferencia",
        ],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA CIVIL MATEMÁTICA (ramos adicionales de especialidad)
  // ═══════════════════════════════════════
  {
    id: "ing-civil-matematica",
    nombre: "Ing. Civil Matemática (ramos post Plan Común)",
    facultad: "Departamento de Matemática — Campus Casa Central (Valparaíso)",
    duracion: "Semestres 5-11 después de Plan Común",
    mallaUrl: "https://matematica.usm.cl/pregrado/ingenieria-civil-matematica/",
    nota: "Especialidad con más ramos matemáticos avanzados. Los ramos de S1-S3 son los del Plan Común.",
    ramos: [
      {
        nombre: "Cálculo Avanzado / Variable Compleja",
        semestre: 4,
        prereqs: "Cálculo en Varias Variables + Ecuaciones Diferenciales",
        contenidos: [
          "Cálculo vectorial: campos, integrales de línea y superficie, teoremas de Green, Stokes, divergencia",
          "Series de Fourier: coeficientes, convergencia, transformada",
          "Variable compleja: funciones analíticas, Cauchy-Riemann, series de Laurent, residuos",
        ],
        match: ["calculo-vec-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo Vectorial (31 mód) cubre Green, Stokes, divergencia. Pero variable compleja y Fourier NO están en el catálogo Se Remonta. Cobertura ~40% del total.",
        nota: "Ramo de especialidad avanzada. Variable compleja y Fourier son temas no cubiertos por Se Remonta.",
      },
      {
        nombre: "Análisis Real",
        semestre: 5,
        prereqs: "Cálculo Avanzado",
        contenidos: [
          "Topología de Rⁿ, espacios métricos",
          "Sucesiones y series, convergencia",
          "Continuidad uniforme, compacidad",
          "Diferenciación en Rⁿ, teorema de la función inversa e implícita",
        ],
        match: [],
        matchLevel: "ninguno",
        nota: "Ramo teórico puro. Sin match con catálogo Se Remonta.",
      },
      {
        nombre: "Ecuaciones en Derivadas Parciales",
        semestre: 5,
        prereqs: "Ecuaciones Diferenciales + Cálculo Avanzado",
        contenidos: [
          "EDP clásicas: calor, onda, Laplace",
          "Métodos de separación de variables",
          "Series de Fourier aplicadas",
          "Funciones de Green",
          "Métodos numéricos para EDP",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "bajo",
        splitDesde: "Ecuaciones Diferenciales (42 mód) cubre solo EDO. Las EDP son tema avanzado no cubierto. Match bajo ~20%.",
      },
    ],
  },
];

// ── CARRERAS SIN RAMOS MATEMÁTICOS PROPIOS / FUERA DE FOCO ──
const sinMatematicas = [
  "Arquitectura",
  "Diseño USM",
  "Técnico Universitario en Control de Gestión",
  "Técnico Universitario en Administración de Empresas",
  "Técnico Universitario en Automatización y Control Industrial",
  "Técnico Universitario en Prevención de Riesgos",
];

// ── FUENTES DOCUMENTADAS ────────────────────────────────────
const fuentes = [
  { tipo: "Programa", nombre: "MATE10 Álgebra y Geometría", url: "https://matematica.usm.cl/wp-content/uploads/2018/05/MATE10-Algebra-y-Geometria.pdf" },
  { tipo: "Programa", nombre: "MATE20 Álgebra Lineal", url: "https://matematica.usm.cl/wp-content/uploads/2018/05/MATE20-Algebra-Lineal.pdf" },
  { tipo: "Referencia", nombre: "MAT070 Intro al Cálculo (Studocu)", url: "https://www.studocu.com/cl/course/universidad-tecnica-federico-santa-maria/introduccion-al-calculo/5439287" },
  { tipo: "Referencia", nombre: "MAT021 Matemática I (programa antiguo)", url: "https://matematica.usm.cl/wp-content/uploads/2018/05/document-7.pdf" },
  { tipo: "Portal", nombre: "Depto. Matemática — Cursos Transversales", url: "https://matematica.usm.cl/docencia/cursos-transversales/" },
  { tipo: "Portal", nombre: "Admisión USM — Carreras", url: "https://usm.cl/admision/carreras/" },
  { tipo: "Malla", nombre: "Ing. Civil Plan Común", url: "https://usm.cl/admision/carreras/san-joaquin/ingenieria-civil-plan-comun/" },
  { tipo: "Malla", nombre: "Ing. Civil Informática (PDF 2014)", url: "https://www.inf.utfsm.cl/images/documentos/nueva-malla-ici.pdf" },
  { tipo: "Malla", nombre: "Ing. Civil Matemática", url: "https://matematica.usm.cl/pregrado/ingenieria-civil-matematica/" },
  { tipo: "Referencia", nombre: "MAT060 Álg. y Geom. (Pedro Montero)", url: "https://pmontero.mat.utfsm.cl/mat060_2019_1.html" },
  { tipo: "Referencia", nombre: "Alejandría ICM — Material de Ramos", url: "https://www.alejandriaicm.com/material" },
];

// ═══════════════════════════════════════════════════════════════
// COMPONENTES UI
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
                    <span className="text-gray-400">•</span> {c}
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
              <p className="text-xs text-gray-500 mb-1">Especialidades/carreras que comparten este plan:</p>
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
              Ver malla curricular completa
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
            <span className="text-sm text-gray-500">({sr.matches.length} coincidencias en UTFSM)</span>
          </div>
          <div className="p-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-2 font-medium">Carrera UTFSM</th>
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
          <div className="text-xs text-blue-600">Programas analizados</div>
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
            <div className="w-10 h-10 bg-yellow-600 rounded-xl flex items-center justify-center text-white font-bold text-sm">
              USM
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">
                Ramos Matemáticos UTFSM
              </h1>
              <p className="text-sm text-gray-500">
                Investigación para splitting con Se Remonta — Universidad Técnica Federico Santa María
              </p>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-3">
            Análisis de <strong>{carreras.length} programas</strong> de pregrado UTFSM con ramos matemáticos significativos.
            Las <strong>13+ especialidades de Ingeniería Civil</strong> comparten un Plan Común de 4 semestres con 8 ramos matemáticos (6 con match).
            <strong> Ingeniería Comercial</strong> comparte MATE10 y MATE20 pero usa MATE25/MATE26 en vez de los cursos de cálculo de Ing. Civil.
            <strong> {sinMatematicas.length} carreras</strong> (Arquitectura, Diseño, técnicos) están fuera del foco STEM.
          </p>
          <div className="mt-3 bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-sm text-blue-800">
              <strong>Hallazgo clave:</strong> La UTFSM tiene un plan nuevo que reemplazó la secuencia antigua MAT021-MAT024 por cursos con nombres descriptivos.
              El Plan Común Ing. Civil (13+ especialidades, ~4.500 alumnos) tiene <strong>6 ramos matemáticos con match alto</strong> en los primeros 3 semestres.
              Los cursos MATE10 y MATE20 tienen programas oficiales verificados con PDFs del Depto. de Matemática.
              Los cursos Se Remonta (Precálculo, Cálc. 1 Var, Álgebra Lineal, Cálc. Varias Var, Ec. Diferenciales) tienen match directo con los 6 ramos principales.
            </p>
          </div>
          <div className="mt-2 bg-amber-50 border border-amber-200 rounded-lg p-3">
            <p className="text-sm text-amber-800">
              <strong>Diferencia vs UAI/UDD/UAndes/UCh:</strong> La UTFSM separa desde S1 Álgebra (MATE10) de Cálculo (MAT070), similar a la UCh.
              El ramo de Ecuaciones Diferenciales incluye <strong>EDP (ecuaciones en derivadas parciales)</strong>, más allá de lo que cubren la mayoría de las universidades privadas.
              MATE10 es particularmente fuerte en trigonometría y geometría analítica, con enfoque en modelación.
              La Ing. Comercial usa ramos de cálculo diferentes (MATE25/26) con enfoque económico, pero comparte álgebra (MATE10/MATE20).
            </p>
          </div>
          <div className="mt-2 bg-green-50 border border-green-200 rounded-lg p-3">
            <p className="text-sm text-green-800">
              <strong>Nota sobre fuentes:</strong> MATE10 y MATE20 tienen programas oficiales verificados (PDFs del Departamento de Matemática USM).
              MAT070 tiene código confirmado vía Studocu; sus contenidos fueron inferidos del antiguo MAT021 y la estructura de la nueva malla.
              Los ramos de S2-S3 (Cálc. una Variable, Cálc. Varias Variables, EDO&EDP) tienen contenidos estándar inferidos de la secuencia curricular y los antiguos MAT022-MAT024.
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
                  ? "bg-yellow-600 text-white shadow"
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
              className="w-full px-4 py-2.5 rounded-xl border bg-white mb-4 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-400"
            />
            {carrerasFiltradas.map((c) => (
              <CarreraSection key={c.id} carrera={c} />
            ))}

            {/* Carreras sin matemáticas */}
            <div className="mt-6 border rounded-xl bg-white p-5 shadow-sm">
              <h3 className="font-bold text-gray-700 mb-3">
                Carreras fuera de foco STEM ({sinMatematicas.length})
              </h3>
              <p className="text-sm text-gray-500 mb-3">
                Estas carreras no tienen ramos matemáticos de ingeniería o están fuera del foco de splitting
                (Arquitectura, Diseño, programas técnicos).
                La UTFSM es primariamente una universidad de ingeniería — casi todas sus carreras principales tienen matemáticas.
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
              Datos extraídos de los programas oficiales del Departamento de Matemática USM (PDFs descargados de matematica.usm.cl),
              mallas publicadas en usm.cl/admision/carreras/, y referencias de Studocu y sitios de profesores USM.
              MATE10 y MATE20 tienen programas 100% verificados. Los demás cursos tienen contenidos inferidos de la secuencia
              curricular y los programas antiguos (MAT021-MAT024). Datos vigentes para admisión 2026.
            </p>
            {["Programa", "Portal", "Malla", "Referencia"].map((tipo) => (
              <div key={tipo} className="mb-5">
                <h4 className="font-semibold text-sm text-gray-700 mb-2 uppercase tracking-wide">{tipo}s</h4>
                <div className="space-y-1">
                  {fuentes
                    .filter((f) => f.tipo === tipo)
                    .map((f, i) => (
                      <div key={i} className="flex items-center gap-2 text-sm">
                        <span className={`w-2 h-2 rounded-full ${
                          tipo === "Programa" ? "bg-green-400" : tipo === "Portal" ? "bg-purple-400" : tipo === "Malla" ? "bg-blue-400" : "bg-amber-400"
                        }`} />
                        <span className="text-gray-700 font-medium">{f.nombre}</span>
                        <a href={f.url} target="_blank" rel="noopener" className="text-blue-500 underline text-xs truncate max-w-md">
                          {f.url.replace("https://matematica.usm.cl/", "mat.usm/").replace("https://www.studocu.com/cl/", "studocu/").replace("https://usm.cl/", "usm/")}
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
          Investigación Se Remonta × UTFSM · Datos verificados abril 2026 · Fuentes oficiales USM + inferencias documentadas
        </div>
      </div>
    </div>
  );
}
