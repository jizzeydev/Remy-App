// ═══════════════════════════════════════════════════════════════
// DATOS VERIFICADOS - Investigación Ramos Universidad San Sebastián (USS)
// Fuentes:
//   - Portal Admisión USS (carreras): https://admision.uss.cl/carreras/ingenieria-civil
//   - Portal Admisión USS (carreras): https://admision.uss.cl/carreras/ingenieria-civil-industrial
//   - Portal Admisión USS (carreras): https://admision.uss.cl/carreras/ingenieria-civil-informatica
//   - Portal Admisión USS (carreras): https://admision.uss.cl/carreras/ingenieria-civil-en-minas
//   - Portal Admisión USS (carreras): https://admision.uss.cl/carreras/ingenieria-comercial
//   - Tabla complementaria Ing. Civil (DR 69/2023, Plan 2024): https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf
//   - Tabla complementaria Ing. Civil Industrial (DR 70/2023, Plan 2024): https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf
//   - Tabla complementaria Ing. Civil Informática (DR 71/2023, Plan 2024): https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf
//   - Tabla complementaria Ing. Civil en Minas (DR 72/2023, Plan 2024): https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf
//   - Folleto Ingeniería Comercial USS (acreditada 2016-2022): https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf
//   - Perfil Egreso Ing. Comercial USS: https://cdn.uss.cl/content/uploads/2022/12/07203814/PERFIL_INGENIERIA_COMERCIAL.pdf
//   - Studocu (referencia mallas): https://www.studocu.com/cl/document/universidad-san-sebastian/finanzas/malla-ingenieria-comercial-uss/50274536
//
// Notas globales:
//   - Las 4 ingenierías civiles USS (Civil, Civil Industrial, Civil Informática, Civil en Minas) comparten
//     un núcleo común de Ciencias Básicas (Cálculo, Álgebra, Física, Química, Programación) durante los
//     primeros ~4-5 semestres. Lo modelamos como carrera 'plan-comun' y cada especialidad lista sólo sus
//     ramos diferenciadores + el "Introducción a..." de la profesión.
//   - USS NO tiene Ingeniería Civil Química como carrera independiente; sí Ing. Civil en Minas (id 24).
//   - USS NO tiene un programa "Plan Común" como carrera matriculable separada; el ingreso es directo a
//     la especialidad. La modelación 'plan-comun' acá es analítica para Se Remonta (núcleo basal compartido).
//   - Los PDFs oficiales (Tabla complementaria) NO incluyen códigos de asignatura tipo MAT101/FIS210; usan
//     sólo el nombre del ramo. Por eso 'codigo' va vacío para ramos USS.
//   - Bibliografía: las Tablas complementarias USS no listan bibliografía obligatoria por ramo (sólo
//     descriptor + resultado de aprendizaje); no se reportan referencias bibliográficas por asignatura.
//
// Fecha de investigación: Abril 2026
// ═══════════════════════════════════════════════════════════════

import { useState } from "react";

// ─── CATÁLOGO BASE SE REMONTA (copiado tal cual del prompt) ───
const seRemontaCursos = [
  // ─── MATEMÁTICAS (catálogo activo) ───
  {
    id: "precalculo-cero",
    nombre: "Precálculo desde Cero",
    tipo: "general",
    area: "matemáticas",
    modulos: 68,
    precio: 40000,
    color: "#8B5CF6",
    contenidos: [
      "Conjuntos y números",
      "Álgebra de expresiones",
      "Ecuaciones e inecuaciones",
      "Funciones",
      "Trigonometría",
      "Geometría analítica",
    ],
  },
  {
    id: "nivelacion-ing",
    nombre: "Nivelación Ingeniería",
    tipo: "general",
    area: "matemáticas",
    modulos: 43,
    precio: 20000,
    color: "#7C3AED",
    contenidos: [
      "Repaso números reales",
      "Funciones elementales",
      "Trigonometría aplicada",
      "Vectores y geometría",
      "Lógica e inducción",
      "Polinomios",
    ],
  },
  {
    id: "algebra-lineal-gen",
    nombre: "Álgebra Lineal",
    tipo: "general",
    area: "matemáticas",
    modulos: 52,
    precio: 40000,
    color: "#6366F1",
    contenidos: [
      "Espacio",
      "Sistemas de Ecuaciones",
      "Álgebra de Matrices",
      "Determinantes",
      "Espacios y Subespacios Vectoriales",
      "Valores y Vectores Propios",
      "Ortogonalidad",
      "Matrices Simétricas",
    ],
  },
  {
    id: "calculo-1var-gen",
    nombre: "Cálculo en una Variable",
    tipo: "general",
    area: "matemáticas",
    modulos: 85,
    precio: 40000,
    color: "#3B82F6",
    contenidos: [
      "Límites y continuidad",
      "Derivadas",
      "Aplicaciones de la derivada",
      "Integrales",
      "Técnicas de integración",
      "Aplicaciones de la integral",
    ],
  },
  {
    id: "calculo-dif-gen",
    nombre: "Cálculo Diferencial",
    tipo: "general",
    area: "matemáticas",
    modulos: 52,
    precio: 35000,
    color: "#0EA5E9",
    contenidos: [
      "Números reales e inecuaciones",
      "Funciones (dominio, recorrido, transformaciones, polinomiales, exp, log)",
      "Límites y continuidad",
      "Derivadas y reglas de derivación",
      "Aplicaciones de la derivada (TVM, L'Hôpital, optimización, graficación)",
    ],
  },
  {
    id: "calculo-int-gen",
    nombre: "Cálculo Integral",
    tipo: "general",
    area: "matemáticas",
    modulos: 48,
    precio: 35000,
    color: "#06B6D4",
    contenidos: [
      "Antiderivadas e integral indefinida",
      "Teorema Fundamental del Cálculo",
      "Técnicas (sustitución, partes, fracciones parciales, sustitución trigonométrica)",
      "Aplicaciones (área, volúmenes, longitud de arco, parametrizadas, polares)",
      "Integrales impropias",
      "Sucesiones y series (criterios, Taylor, potencias)",
    ],
  },
  {
    id: "calculo-vvar-gen",
    nombre: "Cálculo en Varias Variables",
    tipo: "general",
    area: "matemáticas",
    modulos: 41,
    precio: 40000,
    color: "#14B8A6",
    contenidos: [
      "Funciones de varias variables",
      "Derivadas parciales y gradiente",
      "Máximos y mínimos",
      "Multiplicadores de Lagrange",
      "Integrales dobles y triples",
      "Coordenadas curvilíneas",
    ],
  },
  {
    id: "calculo-vec-gen",
    nombre: "Cálculo Vectorial",
    tipo: "general",
    area: "matemáticas",
    modulos: 31,
    precio: 40000,
    color: "#10B981",
    contenidos: [
      "Curvas paramétricas y vectoriales",
      "Integrales de línea (escalares y vectoriales)",
      "Teorema de Green",
      "Rotacional y divergencia",
      "Integrales de superficie",
      "Teorema de Stokes",
      "Teorema de la divergencia",
    ],
  },
  {
    id: "ec-dif-gen",
    nombre: "Ecuaciones Diferenciales",
    tipo: "general",
    area: "matemáticas",
    modulos: 42,
    precio: 40000,
    color: "#EAB308",
    contenidos: [
      "EDO primer orden (separable, lineal, exacta, factor integrante, homogénea, Bernoulli)",
      "EDO segundo orden (coef constantes, Cauchy-Euler, coef indeterminados, variación parámetros)",
      "Sistemas de ED",
      "Transformada de Laplace (propiedades, traslación, escalón, convolución, Dirac)",
      "Soluciones por series (Bessel, Frobenius)",
      "Aplicaciones (mecánica, circuitos, modelos)",
    ],
  },
];

// ─── CARRERAS USS ─────────────────────────────────────────────
const carreras = [
  // ═══════════════════════════════════════════════════════════════
  // CARRERA 1 — PLAN COMÚN INGENIERÍA USS (núcleo basal compartido)
  // ═══════════════════════════════════════════════════════════════
  {
    id: "plan-comun",
    nombre: "Plan Común de Ingeniería Civil USS (núcleo basal)",
    facultad: "Facultad de Ingeniería",
    duracion: "Sem 1-4 compartidos (luego diverge por especialidad, 10 sem total)",
    especialidades: [
      "Ingeniería Civil",
      "Ingeniería Civil Industrial",
      "Ingeniería Civil Informática",
      "Ingeniería Civil en Minas",
    ],
    mallaUrl: "https://admision.uss.cl/descarga-malla-uss",
    nota: "USS NO matricula a un 'Plan Común' único: cada estudiante ingresa directamente a una de las 4 ingenierías civiles. Sin embargo, los DR 69-72/2023 muestran que los semestres 1-4 (núcleo de Ciencias Básicas: Cálculo, Álgebra, Física, Química, Programación) son idénticos entre las 4 carreras, lo que permite tratar este bloque como 'Plan Común' para fines de planificación de splits Se Remonta. Acreditación variable por carrera (Civil, Industrial, Informática y Comercial están acreditadas).",
    ramos: [
      // ── SEMESTRE 1 ──
      {
        nombre: "Introducción al Cálculo",
        codigo: "",
        area: "matemáticas",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Números reales (axiomas, orden, valor absoluto, inecuaciones)",
          "Funciones (dominio, recorrido, composición, inversa)",
          "Funciones exponenciales y logarítmicas",
          "Funciones trigonométricas e identidades",
          "Cónicas (circunferencia, parábola, elipse, hipérbola)",
          "Límites y continuidad (introducción)",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre ~80%: conjuntos, álgebra, funciones, trigonometría, geometría analítica. Nivelación Ingeniería (43 mód) refuerza funciones elementales y trigonometría. Falta grabar específicamente la sección de límites/continuidad (~15% del ramo USS).",
        nota: "Departamento de Ciencias Exactas, Facultad de Ingeniería. 8 SCT, 8 ECTS. 7h directas + 5h indirectas semanales. Ramo idéntico en Civil, Industrial, Informática y Minas (DR 69-72/2023).",
      },
      {
        nombre: "Álgebra",
        codigo: "",
        area: "matemáticas",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Lógica proposicional y conjuntos",
          "Álgebra básica (operaciones, factorización, fracciones algebraicas)",
          "Resolución de ecuaciones (lineales, cuadráticas, racionales, irracionales, exponenciales y logarítmicas)",
          "Polinomios (Teorema del resto, división, raíces)",
          "Sucesiones, sumatorias y progresiones (aritmética, geométrica)",
          "Combinatoria y Teorema del binomio",
          "Números complejos (formas binómica, polar y exponencial)",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero cubre álgebra de expresiones, ecuaciones, geometría. Nivelación Ingeniería (43 mód) cubre lógica e inducción, polinomios. Combinados llegan a ~80%. Falta grabar combinatoria/binomio y números complejos en forma polar/exponencial con más detalle.",
        nota: "Departamento de Ciencias Exactas. 8 SCT. Ramo idéntico en Civil, Industrial, Informática y Minas.",
      },
      {
        nombre: "Taller de Aptitudes Lógicas y Matemáticas",
        codigo: "",
        area: "matemáticas",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Aritmética básica y razonamiento numérico",
          "Álgebra escolar (refuerzo)",
          "Trigonometría (refuerzo)",
          "Geometría euclidiana",
          "Resolución de problemas con metodología guiada",
          "Componente psicopedagógico (autoeficacia, motivación, hábitos de estudio)",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "medio",
        splitDesde: "Precálculo desde Cero cubre aritmética, álgebra, trigonometría y geometría escolar. Es esencialmente un taller remedial. Falta grabar el componente psicopedagógico (autoeficacia/motivación), que no es matemático.",
        nota: "4 SCT. Departamento de Ciencias Exactas. Diseñado como nivelación remedial — público que ingresa con vacíos PSU/PAES. Idéntico en las 4 carreras civiles.",
      },
      {
        nombre: "Taller de Programación I",
        codigo: "",
        area: "programación",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Introducción a la programación (lógica, algoritmos, pseudocódigo)",
          "Lenguaje base introductorio (probablemente Python — se confirma en T. Programación II)",
          "Estructuras de control (condicionales, ciclos)",
          "Estructuras de datos básicas (listas, tuplas)",
          "Funciones y modularidad",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base en programación. Oportunidad: producir 'Programación para Ingenieros - Nivel 1 (Python)' como curso base. El stack USS apunta a Python (Taller II usa Python explícitamente).",
        nota: "5 SCT. Sello Facultad de Ingeniería USS. Idéntico en las 4 carreras civiles. Contenidos del syllabus oficial son escuetos; inferidos de la progresión hacia Taller de Programación II.",
      },

      // ── SEMESTRE 2 ──
      {
        nombre: "Cálculo Diferencial e Integral",
        codigo: "",
        area: "matemáticas",
        semestre: 2,
        prereqs: "Introducción al Cálculo",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Derivada (definición, reglas, derivada de funciones elementales, regla de la cadena)",
          "Aplicaciones de la derivada (TVM, L'Hôpital, optimización, análisis de funciones, Taylor)",
          "Integral indefinida y técnicas de integración (sustitución, partes, fracciones parciales, sust. trigonométrica)",
          "Integral definida (sumas de Riemann, Teorema Fundamental del Cálculo)",
          "Aplicaciones de la integral (área, volúmenes de revolución, longitud de arco)",
          "Integrales impropias",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen", "calculo-int-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód) cubre el ramo casi completo. Alternativa: combinar Cálculo Diferencial (52 mód) + Cálculo Integral (48 mód) = match ~95%. Falta grabar Taylor con más profundidad si USS lo exige.",
        nota: "8 SCT. Departamento de Ciencias Exactas. Es un curso 'integral' que combina cálculo diferencial e integral en un solo semestre. Idéntico en las 4 carreras civiles.",
      },
      {
        nombre: "Álgebra Lineal",
        codigo: "",
        area: "matemáticas",
        semestre: 2,
        prereqs: "Álgebra",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Matrices y operaciones (suma, producto, traspuesta, inversa)",
          "Sistemas de ecuaciones lineales (Gauss, Gauss-Jordan)",
          "Determinantes",
          "Espacios y subespacios vectoriales",
          "Independencia lineal, base, dimensión",
          "Transformaciones lineales (matriz asociada, núcleo, imagen)",
          "Valores y vectores propios (introducción)",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal Se Remonta (52 mód) cubre todo el ramo y va más profundo (incluye ortogonalidad y matrices simétricas que USS no profundiza en este curso). Match >85%.",
        nota: "7 SCT. Departamento de Ciencias Exactas. Idéntico en las 4 carreras civiles.",
      },
      {
        nombre: "Química General",
        codigo: "",
        area: "química",
        semestre: 2,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Estructura atómica y tabla periódica",
          "Enlace químico (iónico, covalente, metálico)",
          "Estequiometría y reacciones químicas",
          "Estados de la materia (gases, líquidos, sólidos)",
          "Soluciones y propiedades coligativas",
          "Equilibrio químico ácido-base",
          "Termoquímica y cinética química (introducción)",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "No hay curso base de química en el catálogo Se Remonta. Oportunidad: producir 'Química General para Ingenieros' como curso base nuevo — lo necesita cada Ing. Civil USS y también UDD/UAI/UC.",
        nota: "6 SCT. Departamento de Ciencias Biológicas y Químicas, Facultad de Medicina y Ciencia. Asignatura teórica (no laboratorio). Contenidos inferidos del estándar de Química General de Ingeniería Civil chilena (Brown/Chang).",
      },
      {
        nombre: "Taller de Programación II",
        codigo: "",
        area: "programación",
        semestre: 2,
        prereqs: "Taller de Programación I",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Programación en Python (procesamiento de datos)",
          "Análisis de datos (pandas/numpy implícitos)",
          "Publicación en sistemas globales (APIs, archivos, formatos JSON/CSV)",
          "Aprendizaje Basado en Proyectos con casuística real",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad: producir 'Programación para Ingenieros - Nivel 2 (Python orientado a datos)' como curso base. Stack confirmado: Python con énfasis en datos.",
        nota: "6 SCT. El descriptor oficial confirma 'programación basada en Python, incluyendo el análisis de resultados'. Idéntico en las 4 carreras civiles.",
      },

      // ── SEMESTRE 3 ──
      {
        nombre: "Cálculo Multivariable",
        codigo: "",
        area: "matemáticas",
        semestre: 3,
        prereqs: "Cálculo Diferencial e Integral, Álgebra Lineal",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Funciones de varias variables (dominio, recorrido, gráficos, curvas de nivel)",
          "Diferenciabilidad en R^n (derivadas parciales, gradiente, regla de la cadena)",
          "Optimización (puntos críticos, máximos/mínimos, multiplicadores de Lagrange)",
          "Integrales múltiples (dobles y triples) en coordenadas cartesianas, polares, cilíndricas y esféricas",
          "Integrales de línea (escalares y vectoriales)",
          "Integrales de superficie",
        ],
        match: ["calculo-vvar-gen", "calculo-vec-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre diferenciabilidad, optimización e integrales múltiples. Cálculo Vectorial (31 mód) cubre integrales de línea y superficie. Combinados = match >85%. Falta grabar específicamente coordenadas curvilíneas si USS profundiza.",
        nota: "6 SCT. Departamento de Ciencias Exactas. Idéntico en Civil, Industrial, Informática y Minas. El descriptor explícitamente menciona 'integrales de línea y superficie' por lo que cubre lo que típicamente se llama Cálculo III + Cálculo Vectorial juntos.",
      },
      {
        nombre: "Física",
        codigo: "",
        area: "física",
        semestre: 3,
        prereqs: "Cálculo Diferencial e Integral",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Cinemática (movimiento rectilíneo, en el plano, vectorial)",
          "Dinámica (Leyes de Newton, fuerzas, fricción)",
          "Trabajo, energía y conservación",
          "Sistemas de partículas (centro de masa, momento lineal, colisiones)",
          "Cuerpo rígido (introducción) — rotación, momento de inercia",
          "Laboratorio de mecánica",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "No hay curso base de física en el catálogo Se Remonta. Oportunidad de altísima prioridad: producir 'Física General I (Mecánica Newtoniana)' como curso base — todas las ingenierías chilenas (UC, UDD, USM, UAI, USS) lo requieren.",
        nota: "6 SCT. Departamento de Ciencias Exactas. Foco en mecánica Newtoniana con laboratorio. El descriptor especifica 'cinemática y dinámica del movimiento en partículas, sistemas de partículas y, a nivel introductorio, cuerpos rígidos'.",
      },
      {
        nombre: "Taller de Tecnologías Digitales",
        codigo: "",
        area: "programación",
        semestre: 3,
        prereqs: "Taller de Programación II",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Metodología ágil (Scrum) aplicada a proyectos tecnológicos",
          "Diseño asistido por computadora (CAD)",
          "Prototipado digital y físico",
          "Aprendizaje Basado en Proyectos para resolver desafíos tecnológicos",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo de prototipado/CAD/agile, no curricularmente fuerte en programación pura. Bajo valor para Se Remonta: probablemente NO replicar como curso base; descartar para split.",
        nota: "5 SCT. Sello Facultad de Ingeniería. Idéntico en las 4 carreras civiles. Más bien un taller de innovación que un ramo técnico.",
      },

      // ── SEMESTRE 4 ──
      {
        nombre: "Ecuaciones Diferenciales",
        codigo: "",
        area: "matemáticas",
        semestre: 4,
        prereqs: "Cálculo Diferencial e Integral, Cálculo Multivariable",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "EDO de primer orden (separable, lineal, exacta, factor integrante)",
          "EDO de segundo orden (coeficientes constantes, coeficientes indeterminados, variación de parámetros)",
          "Sistemas de ecuaciones diferenciales",
          "Transformada de Laplace (definición, propiedades, traslación, escalón, convolución)",
          "Aplicaciones (mecánica, circuitos eléctricos, modelos poblacionales)",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Ecuaciones Diferenciales Se Remonta (42 mód) cubre EDO de 1° y 2° orden, sistemas, Laplace y aplicaciones. Match >85%. El curso Se Remonta incluye además soluciones por series (Bessel, Frobenius) que USS no toca explícitamente — bonus.",
        nota: "5 SCT. Departamento de Ciencias Exactas. Idéntico en las 4 carreras civiles. El descriptor menciona explícitamente 'Transformada de Laplace'.",
      },
      {
        nombre: "Probabilidades y Estadística",
        codigo: "",
        area: "matemáticas",
        semestre: 4,
        prereqs: "Cálculo Diferencial e Integral",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Probabilidad (espacio muestral, eventos, axiomas, probabilidad condicional, Bayes)",
          "Variables aleatorias discretas y continuas",
          "Distribuciones de probabilidad clásicas (Bernoulli, Binomial, Poisson, Normal, Exponencial)",
          "Esperanza, varianza, momentos",
          "Inferencia estadística (estimación puntual y por intervalos)",
          "Pruebas de hipótesis",
          "Regresión lineal simple (introducción)",
          "Uso de software estadístico (R/Python en laboratorio)",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "No hay curso base de Probabilidades/Estadística en Se Remonta. Oportunidad de alto impacto: producir 'Probabilidades y Estadística para Ingeniería' como curso base — lo requieren TODAS las ingenierías chilenas y también Comercial.",
        nota: "6 SCT. Departamento de Ciencias Exactas. Idéntico en Civil, Industrial, Informática y Minas. Incluye laboratorio de computación.",
      },
      {
        nombre: "Electricidad y Magnetismo",
        codigo: "",
        area: "física",
        semestre: 4,
        prereqs: "Física, Cálculo Multivariable",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Electrostática (carga eléctrica, Ley de Coulomb, campo eléctrico, Ley de Gauss)",
          "Potencial eléctrico y energía potencial",
          "Capacitancia y dieléctricos",
          "Corriente eléctrica, resistencia, Ley de Ohm",
          "Circuitos de corriente continua (Kirchhoff, RC)",
          "Magnetostática (campo magnético, Ley de Biot-Savart, Ley de Ampère)",
          "Inducción electromagnética (Ley de Faraday, Ley de Lenz)",
          "Laboratorio de electromagnetismo",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "No hay curso base de física. Oportunidad: producir 'Física General II (Electricidad y Magnetismo)' — segundo curso de física estándar en ingeniería chilena.",
        nota: "6 SCT. Presente en Civil, Industrial e Informática. NO está en Civil en Minas. Incluye laboratorio.",
      },
      {
        nombre: "Taller de Sustentabilidad",
        codigo: "",
        area: "otra",
        semestre: 4,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Análisis de desempeño ambiental y energético de organizaciones",
          "Propuestas de mejora hacia la sustentabilidad",
          "Aprendizaje Basado en Proyectos con problemas reales",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo proyectual transversal, fuera del nicho STEM/negocios duros. Probable descarte para split: bajo costo/beneficio.",
        nota: "4 SCT. Sello Facultad de Ingeniería. Idéntico en las 4 carreras civiles.",
      },
    ],
  },

  // ═══════════════════════════════════════════════════════════════
  // CARRERA 2 — INGENIERÍA CIVIL (id 23, DR 69/2023)
  // ═══════════════════════════════════════════════════════════════
  {
    id: "ing-civil",
    nombre: "Ingeniería Civil",
    facultad: "Facultad de Ingeniería",
    duracion: "10 semestres + práctica industrial (sem 6) + práctica profesional (sem 8)",
    especialidades: [],
    mallaUrl: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
    nota: "Foco en obras civiles (estructuras, hormigón, hidráulica, geotecnia). Sedes: Santiago, Concepción, Valdivia, Patagonia. Comparte el núcleo basal con 'plan-comun' (sem 1-4: Cálculo, Álgebra, Física, Química, Programación). Acá listamos sólo los ramos diferenciadores de la especialidad.",
    ramos: [
      // ── SEMESTRE 1 (carrera-específico) ──
      {
        nombre: "Introducción a la Ingeniería Civil",
        codigo: "",
        area: "otra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Introducción a la profesión, áreas de desempeño y rol del ingeniero civil",
          "Tipos de obras civiles (estructuras, hidráulica, transporte, geotecnia)",
          "Ética profesional y normativa básica",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo introductorio profesional, no técnico. No replicable como curso base.",
        nota: "5 SCT. Línea curricular 'Planificación de Proyectos y Gestión de la Construcción'.",
      },
      // ── SEMESTRE 3 ──
      {
        nombre: "Ciencia de Materiales de Construcción",
        codigo: "",
        area: "otra",
        semestre: 3,
        prereqs: "Química General",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Propiedades físicas, químicas y mecánicas de materiales de construcción",
          "Hormigón (cemento, agregados, aditivos, dosificación)",
          "Acero estructural",
          "Madera, mampostería y materiales innovadores",
          "Ensayos normalizados",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad de Ing. Civil. Fuera del nicho Se Remonta.",
        nota: "6 SCT. Línea 'Evaluación Estructural y Geotécnica de Obras Civiles'.",
      },
      // ── SEMESTRE 4 ──
      {
        nombre: "Estática",
        codigo: "",
        area: "física",
        semestre: 4,
        prereqs: "Física, Cálculo Multivariable",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Equilibrio de partículas y cuerpos rígidos en 2D y 3D",
          "Diagramas de cuerpo libre",
          "Reacciones, fuerzas internas (axial, corte, momento)",
          "Vigas, armaduras y marcos",
          "Centroides y momentos de inercia",
          "Fricción",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo de mecánica racional / física aplicada. No hay curso base. Demanda compartida con todas las ingenierías civiles chilenas — alta prioridad si se produce 'Estática para Ingenieros'.",
        nota: "5 SCT. Línea 'Evaluación Estructural y Geotécnica de Obras Civiles'.",
      },
      // ── SEMESTRE 5 ──
      {
        nombre: "Mecánica de Sólidos",
        codigo: "",
        area: "física",
        semestre: 5,
        prereqs: "Estática, Ecuaciones Diferenciales",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Esfuerzos y deformaciones (axial, cortante, flexión, torsión)",
          "Diagramas de esfuerzo-deformación, Ley de Hooke",
          "Vigas (esfuerzos, deflexiones)",
          "Círculo de Mohr, esfuerzos principales",
          "Pandeo de columnas",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad de Ing. Civil estructural. Fuera del nicho Se Remonta.",
        nota: "5 SCT. Línea 'Evaluación Estructural'.",
      },
      {
        nombre: "Métodos Numéricos",
        codigo: "",
        area: "matemáticas",
        semestre: 5,
        prereqs: "Cálculo Multivariable, Ecuaciones Diferenciales, Taller de Programación II",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Errores numéricos y estabilidad",
          "Resolución numérica de ecuaciones no lineales (bisección, Newton-Raphson)",
          "Sistemas lineales (Gauss, LU, Gauss-Seidel)",
          "Interpolación y aproximación (Lagrange, splines)",
          "Diferenciación e integración numérica (Trapecio, Simpson)",
          "Resolución numérica de EDO (Euler, Runge-Kutta)",
          "Implementación en Python/MATLAB",
        ],
        match: ["calculo-1var-gen", "calculo-vvar-gen", "ec-dif-gen"],
        matchLevel: "bajo",
        splitDesde: "Cálculo en una Variable, Cálculo Varias Variables y Ecuaciones Diferenciales aportan la base teórica (límites, derivadas, EDO). Pero los algoritmos numéricos no están cubiertos. Match conceptual ~30%. Oportunidad: producir 'Métodos Numéricos con Python' como curso base.",
        nota: "5 SCT. Aplicación intensiva de programación. Línea 'Evaluación Estructural'.",
      },
      {
        nombre: "Fenómenos de Transporte",
        codigo: "",
        area: "física",
        semestre: 5,
        prereqs: "Física, Cálculo Multivariable, Ecuaciones Diferenciales",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Transferencia de momento (introducción a fluidos)",
          "Transferencia de calor (conducción, convección, radiación)",
          "Transferencia de masa (difusión, convección)",
          "Balances macroscópicos",
          "Aplicaciones en ingeniería civil/química",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo de física aplicada / ing. de procesos. Fuera del nicho.",
        nota: "5 SCT. Aparece también en Industrial y Minas (no en Informática).",
      },
      {
        nombre: "Gestión de Operaciones en la Construcción",
        codigo: "",
        area: "otra",
        semestre: 5,
        prereqs: "Introducción a la Ingeniería Civil",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Planificación y programación de obras",
          "Productividad y rendimientos",
          "Logística de obra",
          "Indicadores de gestión",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT.",
      },
      // ── SEMESTRE 6 ──
      {
        nombre: "Análisis de Estructuras",
        codigo: "",
        area: "física",
        semestre: 6,
        prereqs: "Mecánica de Sólidos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Estructuras isostáticas e hiperestáticas",
          "Métodos de análisis (Cross, rigidez, flexibilidad)",
          "Líneas de influencia",
          "Estructuras planas y espaciales",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad estructural. Fuera del nicho.",
        nota: "6 SCT.",
      },
      {
        nombre: "Mecánica de Suelos",
        codigo: "",
        area: "física",
        semestre: 6,
        prereqs: "Mecánica de Sólidos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Propiedades físicas y clasificación de suelos",
          "Esfuerzos en suelos, principio de esfuerzos efectivos",
          "Compresibilidad y consolidación",
          "Resistencia al corte",
          "Estabilidad de taludes (introducción)",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad geotécnica. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Mecánica de Fluidos",
        codigo: "",
        area: "física",
        semestre: 6,
        prereqs: "Física, Cálculo Multivariable, Ecuaciones Diferenciales",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Estática de fluidos",
          "Cinemática de fluidos",
          "Ecuaciones de conservación (masa, momento, energía)",
          "Flujo en tuberías y canales",
          "Análisis dimensional y similitud",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Curso de física aplicada de Ing. Civil/Química/Mecánica.",
        nota: "6 SCT. Línea 'Ingeniería Hidráulica y Ambiental'.",
      },
      // ── Ramos posteriores (sólo nombramos por completitud STEM) ──
      {
        nombre: "Estructuras Metálicas",
        codigo: "",
        area: "otra",
        semestre: 7,
        prereqs: "Análisis de Estructuras, Mecánica de Sólidos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: ["Diseño de estructuras de acero según norma chilena (NCh427/NCh2369)"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT. Sin syllabus detallado en Tabla complementaria USS.",
      },
      {
        nombre: "Hormigón Armado",
        codigo: "",
        area: "otra",
        semestre: 7,
        prereqs: "Análisis de Estructuras, Mecánica de Sólidos, Ciencia de Materiales de Construcción",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: ["Diseño de elementos de hormigón armado según NCh430"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "6 SCT.",
      },
      {
        nombre: "Análisis Sísmico",
        codigo: "",
        area: "otra",
        semestre: 7,
        prereqs: "Análisis de Estructuras",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: ["Dinámica estructural y diseño sísmico (NCh433)"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Hidráulica",
        codigo: "",
        area: "física",
        semestre: 7,
        prereqs: "Mecánica de Fluidos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: ["Hidráulica de canales, tuberías, obras hidráulicas"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Hidrología",
        codigo: "",
        area: "otra",
        semestre: 9,
        prereqs: "Probabilidades y Estadística, Hidráulica",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: ["Ciclo hidrológico, balance hídrico, hidrología estadística"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Formulación y Evaluación de Proyectos",
        codigo: "",
        area: "economía",
        semestre: 8,
        prereqs: "Probabilidades y Estadística, Administración de Proyectos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf",
        contenidos: [
          "Identificación y formulación de proyectos",
          "Estudio de mercado",
          "Estudio técnico",
          "Estudio económico-financiero (VAN, TIR, payback)",
          "Análisis de sensibilidad y riesgo",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "No hay curso base de evaluación financiera. Oportunidad media: producir 'Evaluación de Proyectos para Ingenieros' (curso de finanzas operativas — alto solape con Comercial/Industrial).",
        nota: "5 SCT. Comparte temario con cursos similares en Civil Industrial y Civil en Minas.",
      },
    ],
  },

  // ═══════════════════════════════════════════════════════════════
  // CARRERA 3 — INGENIERÍA CIVIL INDUSTRIAL (id 25, DR 70/2023)
  // ═══════════════════════════════════════════════════════════════
  {
    id: "ing-civil-industrial",
    nombre: "Ingeniería Civil Industrial",
    facultad: "Facultad de Ingeniería",
    duracion: "10 semestres + prácticas",
    especialidades: [],
    mallaUrl: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
    nota: "Foco en gestión de operaciones, optimización, ciencia de datos y finanzas. Comparte el núcleo basal con 'plan-comun' (sem 1-4). Listamos los ramos diferenciadores acá. La Tabla complementaria USS DR 70/2023 incluye descriptor + resultado de aprendizaje por ramo.",
    ramos: [
      {
        nombre: "Introducción a la Ingeniería Industrial",
        codigo: "",
        area: "otra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: ["Nociones básicas, objetivos y quehaceres de la Ingeniería Civil Industrial", "Áreas profesionales y casos reales", "Valores institucionales y ética profesional"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo introductorio profesional. No replicable como curso base.",
        nota: "5 SCT. Línea 'Gestión Estratégica y Organizacional'.",
      },
      {
        nombre: "Bases de Datos",
        codigo: "",
        area: "programación",
        semestre: 3,
        prereqs: "Taller de Programación II",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Modelo entidad-relación",
          "Modelo relacional y normalización",
          "SQL (consultas, DDL, DML)",
          "Sistemas de Gestión de Bases de Datos (SGBD)",
          "Manipulación de datos en entornos reales",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad: producir 'Bases de Datos con SQL' como curso base — necesario en Industrial e Informática.",
        nota: "6 SCT. Línea 'Gestión de Operaciones y Mejoramiento Continuo'. Aparece también en Civil Informática.",
      },
      {
        nombre: "Economía",
        codigo: "",
        area: "economía",
        semestre: 4,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Microeconomía (oferta, demanda, equilibrio, mercados)",
          "Macroeconomía (PIB, inflación, política monetaria/fiscal)",
          "Contexto nacional e internacional",
          "Toma de decisiones en el mundo empresarial",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base de economía. Oportunidad alta: producir 'Microeconomía + Macroeconomía Introductorias' — alto solape con Ing. Comercial USS.",
        nota: "5 SCT. Línea 'Gestión Estratégica y Organizacional'. Curso integrado micro+macro.",
      },
      {
        nombre: "Estadística Avanzada",
        codigo: "",
        area: "matemáticas",
        semestre: 5,
        prereqs: "Probabilidades y Estadística",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Inferencia estadística avanzada",
          "Análisis de varianza (ANOVA)",
          "Regresión lineal múltiple y no lineal",
          "Análisis multivariado",
          "Series de tiempo (introducción)",
          "Modelos predictivos con software estadístico",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base de estadística. Oportunidad: producir 'Estadística Avanzada para Ingeniería' después del curso de Probabilidades y Estadística.",
        nota: "5 SCT. Aparece también en Civil Informática.",
      },
      {
        nombre: "Optimización",
        codigo: "",
        area: "matemáticas",
        semestre: 5,
        prereqs: "Álgebra Lineal, Cálculo Multivariable",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Programación lineal (formulación, método simplex)",
          "Dualidad y análisis de sensibilidad",
          "Programación entera",
          "Programación no lineal (Lagrange, KKT)",
          "Modelamiento en software (AMPL/GAMS/Python con Pulp/Pyomo)",
        ],
        match: ["algebra-lineal-gen", "calculo-vvar-gen"],
        matchLevel: "bajo",
        splitDesde: "Álgebra Lineal aporta matrices/sistemas y Cálculo en Varias Variables aporta multiplicadores de Lagrange. Pero el grueso (programación lineal, simplex, dualidad) no está cubierto. Match ~25%. Oportunidad: producir 'Optimización (Investigación de Operaciones)' como curso base.",
        nota: "6 SCT. Línea 'Gestión de Operaciones y Mejoramiento Continuo'. Aparece también en Civil en Minas.",
      },
      {
        nombre: "Contabilidad y Costos",
        codigo: "",
        area: "economía",
        semestre: 5,
        prereqs: "Economía",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Posicionamiento financiero de la empresa (estado de resultados, balance, flujo de caja)",
          "Sistemas de costeo (absorción, variable, ABC)",
          "Análisis de rentabilidad",
          "Toma de decisiones empresariales",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad alta: producir 'Contabilidad y Costos para Ingenieros' — alto solape con Ing. Comercial.",
        nota: "5 SCT. Línea 'Gestión Estratégica y Organizacional'.",
      },
      {
        nombre: "Optimización Aplicada",
        codigo: "",
        area: "matemáticas",
        semestre: 6,
        prereqs: "Optimización",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Modelamiento avanzado de problemas industriales",
          "Programación entera mixta",
          "Heurísticas y metaheurísticas",
          "Productividad y eficiencia operativa",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Curso continuación de Optimización. Mismo gap.",
        nota: "5 SCT.",
      },
      {
        nombre: "Modelos Estocásticos",
        codigo: "",
        area: "matemáticas",
        semestre: 6,
        prereqs: "Probabilidades y Estadística",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Procesos estocásticos",
          "Cadenas de Markov (discretas y continuas)",
          "Procesos de Poisson",
          "Teoría de colas",
          "Aplicaciones a sistemas industriales",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad media: producir 'Modelos Estocásticos / Investigación de Operaciones II'.",
        nota: "6 SCT. Línea 'Gestión de Operaciones'.",
      },
      {
        nombre: "Gestión Estratégica",
        codigo: "",
        area: "otra",
        semestre: 6,
        prereqs: "Economía",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: ["Análisis estratégico, Porter, BSC, planificación estratégica"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo de management. Bajo valor para Se Remonta como curso técnico.",
        nota: "5 SCT.",
      },
      {
        nombre: "Taller de Simulación",
        codigo: "",
        area: "programación",
        semestre: 7,
        prereqs: "Modelos Estocásticos, Bases de Datos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: ["Simulación de eventos discretos", "Software (Arena, SimPy, Anylogic)", "Generación de números aleatorios", "Validación y experimentación"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Analítica y Ciencia de Datos",
        codigo: "",
        area: "programación",
        semestre: 7,
        prereqs: "Estadística Avanzada, Bases de Datos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: ["Análisis exploratorio de datos", "Aprendizaje supervisado y no supervisado (intro)", "Visualización de datos", "Python para ciencia de datos (pandas, scikit-learn)"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad alta de mercado: 'Ciencia de Datos para Ingenieros' es altamente demandado.",
        nota: "5 SCT.",
      },
      {
        nombre: "Marketing Analytics",
        codigo: "",
        area: "economía",
        semestre: 7,
        prereqs: "Estadística Avanzada",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: ["Datos de múltiples fuentes para decisiones de marketing", "Segmentación, targeting", "Métricas de marketing digital", "Modelos predictivos de comportamiento"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad de gestión. Fuera del nicho técnico.",
        nota: "5 SCT.",
      },
      {
        nombre: "Finanzas",
        codigo: "",
        area: "economía",
        semestre: 7,
        prereqs: "Contabilidad y Costos, Probabilidades y Estadística",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: [
          "Valor del dinero en el tiempo",
          "Evaluación de inversiones (VAN, TIR)",
          "Estructura de capital",
          "Riesgo y retorno (CAPM)",
          "Mercados financieros",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad alta: 'Finanzas para Ingenieros' — solape directo con Comercial.",
        nota: "5 SCT.",
      },
      {
        nombre: "Inteligencia de Negocios",
        codigo: "",
        area: "programación",
        semestre: 8,
        prereqs: "Bases de Datos, Analítica y Ciencia de Datos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: ["Data warehousing, ETL", "Dashboards y visualización (Power BI, Tableau)", "KPIs empresariales"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Gestión de Operaciones",
        codigo: "",
        area: "otra",
        semestre: 8,
        prereqs: "Optimización Aplicada, Modelos Estocásticos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: ["Pronósticos de demanda", "Planificación agregada y MRP", "Inventarios", "Lean Manufacturing"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "6 SCT.",
      },
      {
        nombre: "Formulación y Evaluación de Proyectos",
        codigo: "",
        area: "economía",
        semestre: 8,
        prereqs: "Finanzas, Contabilidad y Costos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf",
        contenidos: ["Formulación de proyectos", "Evaluación económico-financiera (VAN, TIR, payback)", "Análisis de sensibilidad y riesgo"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Misma oportunidad que en Civil y Comercial.",
        nota: "7 SCT.",
      },
    ],
  },

  // ═══════════════════════════════════════════════════════════════
  // CARRERA 4 — INGENIERÍA CIVIL INFORMÁTICA (id 26, DR 71/2023)
  // ═══════════════════════════════════════════════════════════════
  {
    id: "ing-civil-informatica",
    nombre: "Ingeniería Civil Informática",
    facultad: "Facultad de Ingeniería",
    duracion: "10 semestres + prácticas",
    especialidades: [],
    mallaUrl: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf",
    nota: "Foco en software, ciberseguridad, redes (Cisco), cloud, ciencia de datos. Alianza con Microsoft. Comparte el núcleo basal con 'plan-comun'. Listamos los ramos diferenciadores acá.",
    ramos: [
      {
        nombre: "Introducción a la Ingeniería Civil Informática",
        codigo: "",
        area: "otra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf",
        contenidos: ["Áreas de la informática profesional", "Roles del ingeniero informático", "Ética y normativas"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo introductorio. No replicable.",
        nota: "5 SCT (asumido). Sin syllabus detallado en Tabla complementaria.",
      },
      {
        nombre: "Paradigmas de Programación",
        codigo: "",
        area: "programación",
        semestre: 3,
        prereqs: "Taller de Programación II",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf",
        contenidos: [
          "Paradigma imperativo vs declarativo",
          "Programación orientada a objetos (clases, herencia, polimorfismo)",
          "Programación funcional (introducción)",
          "Patrones de diseño básicos",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad: producir 'POO + Paradigmas' como curso base, complementario a Programación I/II.",
        nota: "6 SCT. Línea 'Diseño, Implementación y Gestión de Soluciones Informáticas'.",
      },
      {
        nombre: "Matemática Discreta",
        codigo: "",
        area: "matemáticas",
        semestre: 4,
        prereqs: "Álgebra",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf",
        contenidos: [
          "Lógica proposicional y de predicados",
          "Conjuntos, relaciones, funciones",
          "Inducción matemática y recurrencia",
          "Combinatoria",
          "Teoría de grafos (intro)",
          "Aplicaciones a ciencias de la computación",
        ],
        match: ["nivelacion-ing"],
        matchLevel: "bajo",
        splitDesde: "Nivelación Ingeniería incluye lógica e inducción. Pero falta teoría de grafos, recurrencia avanzada, combinatoria formal. Match ~30%. Oportunidad: producir 'Matemática Discreta para Computación'.",
        nota: "5 SCT. Específico de Ing. Civil Informática.",
      },
      {
        nombre: "Estadística Avanzada",
        codigo: "",
        area: "matemáticas",
        semestre: 5,
        prereqs: "Probabilidades y Estadística",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf",
        contenidos: ["Inferencia avanzada", "ANOVA, regresión múltiple", "Análisis multivariado", "Series temporales (intro)"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Mismo gap que Industrial. Misma oportunidad.",
        nota: "5 SCT.",
      },
      {
        nombre: "Infraestructura TI",
        codigo: "",
        area: "programación",
        semestre: 5,
        prereqs: "Taller de Programación II",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf",
        contenidos: ["Hardware y servidores", "Virtualización", "Redes básicas", "Cloud computing (introducción)"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho técnico Se Remonta.",
        nota: "5 SCT.",
      },
      {
        nombre: "Sistemas Operativos",
        codigo: "",
        area: "programación",
        semestre: 6,
        prereqs: "Paradigmas de Programación, Infraestructura TI",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf",
        contenidos: ["Procesos e hilos", "Concurrencia y sincronización", "Gestión de memoria", "Sistemas de archivos", "Sistemas Linux/Windows"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad CS. Sin curso base.",
        nota: "6 SCT.",
      },
      {
        nombre: "Bases de Datos",
        codigo: "",
        area: "programación",
        semestre: 4,
        prereqs: "Taller de Programación II",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf",
        contenidos: ["Modelo relacional, SQL, normalización, SGBD"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Mismo gap que Industrial. Misma oportunidad.",
        nota: "Aparece tanto en Industrial (sem 3) como Informática (sem 4 — verificar). Mismo descriptor.",
      },
    ],
  },

  // ═══════════════════════════════════════════════════════════════
  // CARRERA 5 — INGENIERÍA CIVIL EN MINAS (id 24, DR 72/2023)
  // ═══════════════════════════════════════════════════════════════
  {
    id: "ing-civil-en-minas",
    nombre: "Ingeniería Civil en Minas",
    facultad: "Facultad de Ingeniería",
    duracion: "10 semestres + prácticas",
    especialidades: [],
    mallaUrl: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf",
    nota: "Foco en explotación, geología, perforación, tronadura. NO incluye 'Electricidad y Magnetismo' en su núcleo (a diferencia de las otras 3 ingenierías civiles). Comparte el resto del núcleo basal con 'plan-comun'.",
    ramos: [
      {
        nombre: "Introducción a la Industria Minera y sus Recursos Sostenibles",
        codigo: "",
        area: "otra",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf",
        contenidos: ["La industria minera chilena y mundial", "Recursos minerales y sostenibilidad", "Profesión del ingeniero en minas"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Ramo introductorio. No replicable.",
        nota: "5 SCT.",
      },
      {
        nombre: "Optimización",
        codigo: "",
        area: "matemáticas",
        semestre: 5,
        prereqs: "Álgebra Lineal, Cálculo Multivariable",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf",
        contenidos: ["Programación lineal, simplex, dualidad, programación entera, no lineal con Lagrange/KKT"],
        match: ["algebra-lineal-gen", "calculo-vvar-gen"],
        matchLevel: "bajo",
        splitDesde: "Mismo análisis que en Industrial. Match ~25%.",
        nota: "6 SCT. Idéntico al ramo de Industrial.",
      },
      {
        nombre: "Gestión del Riesgo y Legislación Minera",
        codigo: "",
        area: "otra",
        semestre: 5,
        prereqs: "Sin prerrequisitos disciplinares",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf",
        contenidos: ["Marco legal minero chileno", "Gestión de riesgo en operaciones mineras", "Normativa SERNAGEOMIN"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad legal. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Carguío, Transporte y Manejo de Materiales",
        codigo: "",
        area: "otra",
        semestre: 6,
        prereqs: "Introducción a la Industria Minera",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf",
        contenidos: ["Equipos mineros (palas, camiones, correas)", "Logística y planificación de carguío y transporte"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "4 SCT.",
      },
      {
        nombre: "Perforación y Tronadura",
        codigo: "",
        area: "otra",
        semestre: 7,
        prereqs: "Mecánica de Sólidos (asumido)",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf",
        contenidos: ["Perforación de rocas", "Diseño de tronaduras", "Explosivos y sus aplicaciones"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Métodos de Explotación de Yacimientos",
        codigo: "",
        area: "otra",
        semestre: 8,
        prereqs: "Perforación y Tronadura",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf",
        contenidos: ["Métodos de explotación a cielo abierto", "Métodos subterráneos", "Selección de método según tipo de yacimiento"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Fuera del nicho.",
        nota: "5 SCT.",
      },
      {
        nombre: "Formulación y Evaluación de Proyectos",
        codigo: "",
        area: "economía",
        semestre: 8,
        prereqs: "Probabilidades y Estadística",
        fuenteContenido: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf",
        contenidos: ["Formulación de proyectos mineros", "Evaluación económica (VAN, TIR)", "Análisis de sensibilidad"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Mismo ramo que en Civil/Industrial. Misma oportunidad.",
        nota: "7 SCT.",
      },
    ],
  },

  // ═══════════════════════════════════════════════════════════════
  // CARRERA 6 — INGENIERÍA COMERCIAL (id 17)
  // ═══════════════════════════════════════════════════════════════
  {
    id: "ing-comercial",
    nombre: "Ingeniería Comercial",
    facultad: "Facultad de Economía, Negocios y Gobierno",
    duracion: "10 semestres (8 sem para licenciatura)",
    especialidades: [
      "Gestión",
      "Finanzas",
      "Marketing",
      "Economía Empresarial",
      "Economía Financiera",
    ],
    mallaUrl: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
    nota: "Carrera ACREDITADA (6 años, 2016-2022 según folleto 2019; renovada acreditación posterior). Sedes: Santiago (Bellavista, Los Leones), Concepción, Valdivia, Patagonia. Folleto oficial USS 2019 — la malla pudo ajustarse desde entonces (USS anunció renovación curricular comercial); estos contenidos son la base verificada más reciente. NO comparte plan común con las ingenierías civiles.",
    ramos: [
      // ── SEMESTRE 1 ──
      {
        nombre: "Fundamentos de Economía",
        codigo: "",
        area: "economía",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Conceptos básicos de economía", "Oferta y demanda", "Mercados", "Rol del estado y de la empresa", "Indicadores macroeconómicos básicos"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base de economía. Oportunidad: 'Fundamentos de Economía' como curso base — alto solape con Industrial (Economía sem 4).",
        nota: "Sin syllabus verificado, contenidos inferidos del estándar de Ing. Comercial chilena.",
      },
      {
        nombre: "Métodos Cuantitativos",
        codigo: "",
        area: "matemáticas",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: [
          "Aritmética y razonamiento cuantitativo",
          "Funciones aplicadas a negocios (lineal, exponencial, logarítmica)",
          "Introducción al cálculo aplicado",
          "Resolución de problemas con métodos cuantitativos",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre funciones, álgebra, geometría analítica. Nivelación Ingeniería complementa. Match >75%. Es un ramo de nivelación cuantitativa para estudiantes de negocios.",
        nota: "Sin syllabus verificado. Contenidos inferidos del rol del ramo (preparación para Cálculo Aplicado en sem 3).",
      },
      {
        nombre: "Lógica para los Negocios I",
        codigo: "",
        area: "matemáticas",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Pensamiento lógico aplicado a problemas de negocio", "Argumentación y resolución estructurada", "Razonamiento deductivo e inductivo"],
        match: ["nivelacion-ing"],
        matchLevel: "bajo",
        splitDesde: "Nivelación Ingeniería incluye lógica e inducción. Match ~30%. Resto es soft-skills argumentativos. Bajo costo/beneficio para split.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Fundamentos de Gestión de Empresas",
        codigo: "",
        area: "economía",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Concepto de empresa y administración", "Funciones gerenciales (planificación, organización, dirección, control)", "Estructura organizacional"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base de management. Bajo prioridad para split — soft topic.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Herramientas Informáticas para los Negocios",
        codigo: "",
        area: "programación",
        semestre: 1,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Excel avanzado para negocios", "Procesadores de texto y presentaciones", "Herramientas digitales colaborativas"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad media: 'Excel para Negocios' es de alta demanda y bajo costo de producción.",
        nota: "Sin syllabus verificado.",
      },

      // ── SEMESTRE 2 ──
      {
        nombre: "Álgebra",
        codigo: "",
        area: "matemáticas",
        semestre: 2,
        prereqs: "Métodos Cuantitativos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: [
          "Matrices y operaciones",
          "Sistemas de ecuaciones lineales",
          "Determinantes",
          "Vectores y aplicaciones a negocios",
          "Programación lineal (introducción)",
        ],
        match: ["algebra-lineal-gen", "nivelacion-ing"],
        matchLevel: "medio",
        splitDesde: "Álgebra Lineal Se Remonta cubre matrices, sistemas, determinantes, espacios vectoriales. Nivelación cubre vectores. Falta grabar específicamente la aplicación a negocios y la introducción a programación lineal. Match ~55%.",
        nota: "Es álgebra MATRICIAL para negocios, no álgebra abstracta. Sin syllabus verificado.",
      },
      {
        nombre: "Lógica para los Negocios II",
        codigo: "",
        area: "matemáticas",
        semestre: 2,
        prereqs: "Lógica para los Negocios I",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Razonamiento cuantitativo avanzado", "Problemas estructurados de negocio"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Continuación. Mismo análisis que Lógica I.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Gestión Estratégica de Empresas",
        codigo: "",
        area: "economía",
        semestre: 2,
        prereqs: "Fundamentos de Gestión de Empresas",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Análisis FODA, Porter", "Cadena de valor", "Planificación estratégica"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Soft topic. Fuera del nicho técnico.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Fundamentos de Contabilidad",
        codigo: "",
        area: "economía",
        semestre: 2,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Ecuación contable", "Cuentas y libros", "Estados financieros básicos (balance, estado de resultados)", "IFRS introducción"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Misma oportunidad que Contabilidad y Costos en Industrial.",
        nota: "Sin syllabus verificado.",
      },

      // ── SEMESTRE 3 ──
      {
        nombre: "Microeconomía I",
        codigo: "",
        area: "economía",
        semestre: 3,
        prereqs: "Fundamentos de Economía",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: [
          "Teoría del consumidor (utilidad, restricción presupuestaria, demanda)",
          "Teoría de la firma (producción, costos, oferta)",
          "Equilibrio de mercado",
          "Estructuras de mercado (competencia perfecta, monopolio, oligopolio)",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad alta: 'Microeconomía' es uno de los splits más demandados en Comercial (toda U lo tiene).",
        nota: "Sin syllabus verificado, contenidos inferidos del estándar.",
      },
      {
        nombre: "Cálculo Aplicado a los Negocios",
        codigo: "",
        area: "matemáticas",
        semestre: 3,
        prereqs: "Métodos Cuantitativos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: [
          "Funciones de varias variables aplicadas a negocios",
          "Derivadas e integrales con interpretación económica (costo marginal, ingreso marginal, elasticidad)",
          "Optimización con multiplicadores de Lagrange (intro)",
          "Aplicaciones en economía y finanzas",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen", "calculo-int-gen", "calculo-vvar-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable + Cálculo en Varias Variables cubren la matemática base (derivadas, integrales, parciales, Lagrange). Falta grabar específicamente las aplicaciones económicas (costo marginal, elasticidad). Match ~70%, alto si se enriquece con casos.",
        nota: "Sin syllabus verificado. Es un cálculo light vs ingeniería: menos rigor, más aplicación.",
      },
      {
        nombre: "Legislación Laboral",
        codigo: "",
        area: "otra",
        semestre: 3,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Código del Trabajo", "Contratos, jornadas, remuneraciones", "Negociación colectiva"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Fuera del nicho.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Comunicación para los Negocios",
        codigo: "",
        area: "otra",
        semestre: 3,
        prereqs: "Sin prerrequisitos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Comunicación oral y escrita", "Presentaciones efectivas"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Soft skill. Fuera del nicho.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Contabilidad Gerencial",
        codigo: "",
        area: "economía",
        semestre: 3,
        prereqs: "Fundamentos de Contabilidad",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Costeo (absorción, variable, ABC)", "Presupuestos", "Toma de decisiones gerenciales"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Mismo gap que Contabilidad y Costos en Industrial.",
        nota: "Sin syllabus verificado.",
      },

      // ── SEMESTRE 4 ──
      {
        nombre: "Macroeconomía",
        codigo: "",
        area: "economía",
        semestre: 4,
        prereqs: "Microeconomía I",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: [
          "Identidades macro (PIB, oferta agregada, demanda agregada)",
          "Política monetaria y fiscal",
          "Inflación, desempleo, crecimiento",
          "Modelo IS-LM",
          "Economía abierta",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad alta: 'Macroeconomía' es del top 3 de cursos demandados en Comercial.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Estadística y Probabilidades",
        codigo: "",
        area: "matemáticas",
        semestre: 4,
        prereqs: "Métodos Cuantitativos",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: [
          "Estadística descriptiva",
          "Probabilidad básica",
          "Variables aleatorias y distribuciones",
          "Inferencia estadística (estimación, hipótesis)",
          "Aplicaciones a negocios",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Mismo gap que Probabilidades y Estadística en Civil. Oportunidad de doble retorno.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Legislación para Apertura y Cierre de Empresas",
        codigo: "",
        area: "otra",
        semestre: 4,
        prereqs: "Legislación Laboral",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Constitución de sociedades", "Trámites SII, registro civil", "Quiebra y reorganización"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Fuera del nicho.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Marketing",
        codigo: "",
        area: "economía",
        semestre: 4,
        prereqs: "Fundamentos de Gestión de Empresas",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["4 P's del marketing", "Investigación de mercado", "Comportamiento del consumidor"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Soft topic. Fuera del nicho técnico.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Finanzas",
        codigo: "",
        area: "economía",
        semestre: 4,
        prereqs: "Fundamentos de Contabilidad, Macroeconomía",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: [
          "Valor del dinero en el tiempo",
          "VAN, TIR",
          "Riesgo y retorno",
          "Estructura de capital (intro)",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Mismo gap que Finanzas en Industrial. Triple retorno: Civil, Industrial y Comercial.",
        nota: "Sin syllabus verificado.",
      },

      // ── SEMESTRE 5 ──
      {
        nombre: "Microeconomía II",
        codigo: "",
        area: "economía",
        semestre: 5,
        prereqs: "Microeconomía I",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Equilibrio general", "Externalidades y bienes públicos", "Información asimétrica", "Teoría de juegos (intro)"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Continuación de Micro I.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Estadística para la Toma de Decisiones",
        codigo: "",
        area: "matemáticas",
        semestre: 5,
        prereqs: "Estadística y Probabilidades",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Inferencia avanzada", "Regresión lineal y aplicaciones", "Análisis de datos para decisiones gerenciales"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Mismo gap.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Herramientas Informáticas Avanzadas para los Negocios",
        codigo: "",
        area: "programación",
        semestre: 5,
        prereqs: "Herramientas Informáticas para los Negocios",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Excel avanzado (modelado financiero, macros, VBA)", "Power BI y dashboards", "Análisis de datos"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Misma oportunidad que Herramientas Informáticas básicas.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Inteligencia de Mercado",
        codigo: "",
        area: "economía",
        semestre: 5,
        prereqs: "Marketing, Estadística y Probabilidades",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Investigación cuantitativa y cualitativa", "Análisis competitivo"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Soft topic.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Finanzas Gerenciales",
        codigo: "",
        area: "economía",
        semestre: 5,
        prereqs: "Finanzas",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Decisiones de inversión y financiamiento", "Capital de trabajo", "Política de dividendos"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Continuación de Finanzas. Mismo gap.",
        nota: "Sin syllabus verificado.",
      },

      // ── SEMESTRE 6 ──
      {
        nombre: "Política Macroeconómica",
        codigo: "",
        area: "economía",
        semestre: 6,
        prereqs: "Macroeconomía",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Política monetaria (Banco Central)", "Política fiscal", "Tipo de cambio y balanza de pagos"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Continuación de Macro. Mismo gap.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Econometría para la Gestión",
        codigo: "",
        area: "matemáticas",
        semestre: 6,
        prereqs: "Estadística para la Toma de Decisiones, Macroeconomía",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: [
          "Regresión lineal múltiple (MCO, supuestos, diagnóstico)",
          "Variables dummy",
          "Heterocedasticidad y autocorrelación",
          "Series de tiempo (introducción)",
          "Software (Stata, R o Python)",
        ],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Oportunidad alta: 'Econometría' es uno de los ramos más demandados de Comercial — alto retorno y alto valor percibido.",
        nota: "Sin syllabus verificado, contenidos inferidos del estándar de Econometría I chilena.",
      },
      {
        nombre: "Evaluación de Proyectos",
        codigo: "",
        area: "economía",
        semestre: 6,
        prereqs: "Finanzas, Estadística para la Toma de Decisiones",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Formulación de proyectos", "Evaluación financiera (VAN, TIR)", "Análisis de sensibilidad y escenarios", "Riesgo en proyectos"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Sin curso base. Triple retorno: Civil + Industrial + Comercial todas tienen Formulación/Evaluación de Proyectos.",
        nota: "Sin syllabus verificado.",
      },

      // ── SEMESTRE 7+ (especialidades, dejamos un panorama) ──
      {
        nombre: "Sostenibilidad Empresarial",
        codigo: "",
        area: "otra",
        semestre: 7,
        prereqs: "Sin prerrequisitos disciplinares",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["ESG", "Reportes de sostenibilidad", "Triple bottom line"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Soft topic. Fuera del nicho.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Impuesto a la Renta e IVA",
        codigo: "",
        area: "economía",
        semestre: 7,
        prereqs: "Contabilidad Gerencial",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Sistema tributario chileno", "Impuesto a la renta (1° y 2° categoría)", "IVA"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Tema legal-contable. Fuera del nicho.",
        nota: "Sin syllabus verificado.",
      },
      {
        nombre: "Mercado de Capitales",
        codigo: "",
        area: "economía",
        semestre: 9,
        prereqs: "Finanzas Gerenciales, Econometría",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Instrumentos de renta fija y variable", "Derivados", "Portafolio (Markowitz, CAPM)"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad financiera. Fuera del nicho actual; oportunidad de nicho avanzado para futuros cursos.",
        nota: "Especialidad Finanzas. Sin syllabus verificado.",
      },
      {
        nombre: "Valoración de Empresas",
        codigo: "",
        area: "economía",
        semestre: 9,
        prereqs: "Finanzas Gerenciales",
        fuenteContenido: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf",
        contenidos: ["Métodos de valoración (DCF, múltiplos, opciones reales)"],
        match: [],
        matchLevel: "ninguno",
        splitDesde: "Especialidad. Sin curso base.",
        nota: "Especialidad Finanzas. Sin syllabus verificado.",
      },
    ],
  },
];

// ─── FUENTES DOCUMENTADAS ─────────────────────────────────────
const fuentes = [
  { tipo: "Programa", nombre: "Tabla complementaria Ing. Civil USS (DR 69/2023)", url: "https://cdn.uss.cl/content/uploads/2025/12/17120027/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-1.pdf" },
  { tipo: "Programa", nombre: "Tabla complementaria Ing. Civil Industrial USS (DR 70/2023)", url: "https://cdn.uss.cl/content/uploads/2025/12/17120025/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Industrial-1.pdf" },
  { tipo: "Programa", nombre: "Tabla complementaria Ing. Civil Informática USS (DR 71/2023)", url: "https://cdn.uss.cl/content/uploads/2025/12/17120030/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-Informatica-1.pdf" },
  { tipo: "Programa", nombre: "Tabla complementaria Ing. Civil en Minas USS (DR 72/2023)", url: "https://cdn.uss.cl/content/uploads/2025/12/17120028/Tabla-complementaria-de-aspectos-curriculares-Ingenieria-Civil-en-Minas-1.pdf" },
  { tipo: "Programa", nombre: "Folleto Ingeniería Comercial USS", url: "https://resources.uss.cl/upload/2019/07/Folleto_Ingenieria-Comercial.pdf" },
  { tipo: "Programa", nombre: "Perfil Egreso Ing. Comercial USS", url: "https://cdn.uss.cl/content/uploads/2022/12/07203814/PERFIL_INGENIERIA_COMERCIAL.pdf" },
  { tipo: "Portal", nombre: "Admisión USS — Descarga Mallas", url: "https://admision.uss.cl/descarga-malla-uss" },
  { tipo: "Malla", nombre: "Admisión USS — Ing. Civil", url: "https://admision.uss.cl/carreras/ingenieria-civil" },
  { tipo: "Malla", nombre: "Admisión USS — Ing. Civil Industrial", url: "https://admision.uss.cl/carreras/ingenieria-civil-industrial" },
  { tipo: "Malla", nombre: "Admisión USS — Ing. Civil Informática", url: "https://admision.uss.cl/carreras/ingenieria-civil-informatica" },
  { tipo: "Malla", nombre: "Admisión USS — Ing. Civil en Minas", url: "https://admision.uss.cl/carreras/ingenieria-civil-en-minas" },
  { tipo: "Malla", nombre: "Admisión USS — Ing. Comercial", url: "https://admision.uss.cl/carreras/ingenieria-comercial" },
  { tipo: "Referencia", nombre: "Studocu — Malla Ing. Comercial USS", url: "https://www.studocu.com/cl/document/universidad-san-sebastian/finanzas/malla-ingenieria-comercial-uss/50274536" },
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
    <span className={"text-xs px-2 py-0.5 rounded-full border " + styles[level]}>
      {labels[level]}
    </span>
  );
};

const AreaBadge = ({ area }) => {
  const styles = {
    "matemáticas": "bg-blue-50 text-blue-700 border-blue-200",
    "física": "bg-purple-50 text-purple-700 border-purple-200",
    "química": "bg-pink-50 text-pink-700 border-pink-200",
    "programación": "bg-indigo-50 text-indigo-700 border-indigo-200",
    "economía": "bg-emerald-50 text-emerald-700 border-emerald-200",
    "otra": "bg-gray-50 text-gray-600 border-gray-200",
  };
  return (
    <span className={"text-xs px-2 py-0.5 rounded-full border " + (styles[area] || styles.otra)}>
      {area}
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
          {curso.codigo && <span className="text-xs text-gray-400 font-mono">{curso.codigo}</span>}
          <span className="text-xs text-gray-500">S{curso.semestre}</span>
          <AreaBadge area={curso.area} />
          <MatchBadge level={curso.matchLevel} />
          {curso.matchLevel === "ninguno" && curso.area !== "otra" && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-rose-100 text-rose-800 border border-rose-300">
              Curso base a producir
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
                <p className="text-sm font-semibold text-amber-800 mb-1">Análisis de splitting:</p>
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
                    {sr.nombre}{sr.modulos ? " (" + sr.modulos + " mód)" : ""}
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
  const [isOpen, setIsOpen] = useState(carrera.id === "plan-comun");

  const toggleCurso = (idx) =>
    setExpandedCursos((prev) => ({ ...prev, [idx]: !prev[idx] }));

  const totalMatch = carrera.ramos.filter((r) => r.matchLevel === "alto" || r.matchLevel === "medio").length;
  const oportunidades = carrera.ramos.filter((r) => r.matchLevel === "ninguno" && r.area !== "otra").length;

  return (
    <div className="border rounded-xl mb-4 overflow-hidden shadow-sm">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full text-left px-5 py-4 bg-white hover:bg-gray-50 flex items-center justify-between"
      >
        <div>
          <h3 className="font-bold text-lg text-gray-800">{carrera.nombre}</h3>
          <p className="text-sm text-gray-500">
            {carrera.facultad} · {carrera.duracion} · {carrera.ramos.length} ramos
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-green-700 bg-green-50 px-3 py-1 rounded-full">
            {totalMatch} matches
          </span>
          <span className="text-sm font-medium text-rose-700 bg-rose-50 px-3 py-1 rounded-full">
            {oportunidades} producir
          </span>
          <span className="text-gray-400 text-xl">{isOpen ? "▲" : "▼"}</span>
        </div>
      </button>
      {isOpen && (
        <div className="px-5 pb-4 bg-gray-50 border-t">
          {carrera.nota && (
            <div className="mt-3 mb-3 bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm text-blue-800">
              {carrera.nota}
            </div>
          )}
          {carrera.especialidades && carrera.especialidades.length > 0 && (
            <div className="mt-3 mb-3">
              <p className="text-xs text-gray-500 mb-1">Especialidades / menciones:</p>
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
              Ver malla curricular oficial
            </a>
          )}
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// MATRIZ DE SPLITTING (cursos base → ramos USS)
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
  });

  return (
    <div className="space-y-4">
      {matrix.map((sr) => (
        <div key={sr.id} className="border rounded-xl overflow-hidden bg-white shadow-sm">
          <div className="px-5 py-3 flex items-center gap-3" style={{ backgroundColor: sr.color + "15" }}>
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: sr.color }} />
            <h3 className="font-bold text-gray-800">{sr.nombre}</h3>
            {sr.modulos && <span className="text-xs text-gray-500">{sr.modulos} módulos</span>}
            {sr.precio && <span className="text-xs text-gray-500">${(sr.precio / 1000).toFixed(0)}k</span>}
            <span className="text-sm text-gray-500 ml-auto">
              {sr.matches.length} {sr.matches.length === 1 ? "coincidencia" : "coincidencias"} en USS
            </span>
          </div>
          <div className="p-4">
            {sr.matches.length === 0 ? (
              <p className="text-sm text-gray-400 italic">Sin coincidencias en USS por ahora.</p>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-500 border-b">
                    <th className="pb-2 font-medium">Carrera USS</th>
                    <th className="pb-2 font-medium">Ramo</th>
                    <th className="pb-2 font-medium">Sem</th>
                    <th className="pb-2 font-medium">Match</th>
                  </tr>
                </thead>
                <tbody>
                  {sr.matches.map((m, i) => (
                    <tr key={i} className="border-b last:border-0">
                      <td className="py-2 text-gray-700">{m.carrera}</td>
                      <td className="py-2 font-medium">{m.ramo}</td>
                      <td className="py-2 text-gray-500">S{m.semestre}</td>
                      <td className="py-2"><MatchBadge level={m.level} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// PIPELINE DE CURSOS BASE NUEVOS (ramos sin match agrupados)
// ═══════════════════════════════════════════════════════════════

const Pipeline = () => {
  const sinMatch = {};
  carreras.forEach((c) => {
    c.ramos.forEach((r) => {
      if (r.matchLevel === "ninguno" && r.area !== "otra") {
        const key = r.area + " :: " + r.nombre;
        if (!sinMatch[key]) sinMatch[key] = { area: r.area, nombre: r.nombre, apariciones: [] };
        sinMatch[key].apariciones.push({ carrera: c.nombre, semestre: r.semestre });
      }
    });
  });

  const lista = Object.values(sinMatch).sort((a, b) => b.apariciones.length - a.apariciones.length);

  return (
    <div className="space-y-3">
      <div className="bg-rose-50 border border-rose-200 rounded-lg p-4 mb-4">
        <p className="text-sm text-rose-800">
          <strong>Pipeline de producción</strong> — ramos USS sin match en el catálogo Se Remonta, agrupados por nombre y ordenados por demanda cruzada (más carreras = mayor prioridad).
        </p>
      </div>
      {lista.map((item, i) => (
        <div key={i} className="border rounded-xl bg-white shadow-sm p-4">
          <div className="flex items-center gap-3 mb-2 flex-wrap">
            <span className="font-semibold text-gray-800">{item.nombre}</span>
            <AreaBadge area={item.area} />
            <span className={"text-xs px-2 py-0.5 rounded-full " + (item.apariciones.length >= 3 ? "bg-rose-100 text-rose-700" : item.apariciones.length === 2 ? "bg-amber-100 text-amber-700" : "bg-gray-100 text-gray-600")}>
              {item.apariciones.length} {item.apariciones.length === 1 ? "carrera" : "carreras"}
            </span>
          </div>
          <div className="text-xs text-gray-500 flex flex-wrap gap-2">
            {item.apariciones.map((a, j) => (
              <span key={j} className="bg-gray-50 px-2 py-0.5 rounded border">
                {a.carrera} (S{a.semestre})
              </span>
            ))}
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
  let totalMatchBajo = 0;
  let totalSinMatchStem = 0;
  const porArea = {};
  carreras.forEach((c) => {
    totalRamos += c.ramos.length;
    c.ramos.forEach((r) => {
      if (r.matchLevel === "alto") totalMatchAlto++;
      if (r.matchLevel === "medio") totalMatchMedio++;
      if (r.matchLevel === "bajo") totalMatchBajo++;
      if (r.matchLevel === "ninguno" && r.area !== "otra") totalSinMatchStem++;
      porArea[r.area] = (porArea[r.area] || 0) + 1;
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
          <div className="text-xs text-purple-600">Ramos totales</div>
        </div>
        <div className="bg-rose-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-rose-700">{totalSinMatchStem}</div>
          <div className="text-xs text-rose-600">Sin match (oportunidad)</div>
        </div>
        <div className="bg-gray-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-gray-700">{seRemontaCursos.length}</div>
          <div className="text-xs text-gray-600">Cursos Se Remonta</div>
        </div>
      </div>
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-green-100 rounded-xl p-3 text-center border border-green-200">
          <div className="text-lg font-bold text-green-800">{totalMatchAlto}</div>
          <div className="text-xs text-green-700">Match alto</div>
        </div>
        <div className="bg-yellow-100 rounded-xl p-3 text-center border border-yellow-200">
          <div className="text-lg font-bold text-yellow-800">{totalMatchMedio}</div>
          <div className="text-xs text-yellow-700">Match medio</div>
        </div>
        <div className="bg-orange-100 rounded-xl p-3 text-center border border-orange-200">
          <div className="text-lg font-bold text-orange-800">{totalMatchBajo}</div>
          <div className="text-xs text-orange-700">Match bajo</div>
        </div>
      </div>
      <div className="bg-white rounded-xl border p-4">
        <p className="text-xs text-gray-500 mb-2 uppercase tracking-wide">Distribución por área</p>
        <div className="flex flex-wrap gap-2">
          {Object.entries(porArea).sort((a, b) => b[1] - a[1]).map(([area, n]) => (
            <span key={area} className="text-xs px-3 py-1 bg-gray-50 border rounded-full text-gray-700">
              <strong>{n}</strong> {area}
            </span>
          ))}
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
  const [areaFiltro, setAreaFiltro] = useState("todas");

  const carrerasFiltradas = carreras
    .map((c) => ({
      ...c,
      ramos: c.ramos.filter((r) => {
        const matchesFiltro =
          c.nombre.toLowerCase().includes(filtro.toLowerCase()) ||
          r.nombre.toLowerCase().includes(filtro.toLowerCase());
        const matchesArea = areaFiltro === "todas" || r.area === areaFiltro;
        return matchesFiltro && matchesArea;
      }),
    }))
    .filter((c) => c.ramos.length > 0);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-5xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-red-700 rounded-xl flex items-center justify-center text-white font-bold text-sm">
              USS
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">
                Ramos Universidad San Sebastián
              </h1>
              <p className="text-sm text-gray-500">
                Investigación para splitting con Se Remonta — USS
              </p>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-3">
            Análisis de <strong>{carreras.length} carreras</strong> USS
            (4 ingenierías civiles + Ing. Comercial + Plan Común analítico).
            Las 4 ingenierías civiles (Civil, Industrial, Informática, Minas) comparten un núcleo basal idéntico
            de Cálculo, Álgebra, Física, Química y Programación durante los semestres 1-4 (DR 69-72/2023, Plan 2024).
          </p>
          <div className="mt-3 bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-sm text-blue-800">
              <strong>Hallazgo clave:</strong> El catálogo actual Se Remonta (9 cursos de matemáticas) cubre con match alto los ramos
              de Cálculo (Introducción al Cálculo, Cálculo Diferencial e Integral, Cálculo Multivariable),
              Álgebra Lineal y Ecuaciones Diferenciales del núcleo basal de las 4 ingenierías civiles USS.
              <strong> El gap más rentable</strong> son <em>Probabilidades y Estadística</em> + <em>Estadística Avanzada</em> (presentes en las 4 civiles + Comercial = 5 carreras).
            </p>
          </div>
          <div className="mt-2 bg-amber-50 border border-amber-200 rounded-lg p-3">
            <p className="text-sm text-amber-800">
              <strong>Nicho de cursos base a producir:</strong> Física General I-II (Mecánica, E&M),
              Química General, Programación Python I-II, Bases de Datos, Microeconomía, Macroeconomía,
              Econometría, Finanzas, Optimización (IO). Ver tab <strong>Pipeline</strong> con priorización por demanda cruzada.
            </p>
          </div>
          <div className="mt-2 bg-green-50 border border-green-200 rounded-lg p-3">
            <p className="text-sm text-green-800">
              <strong>Nota sobre fuentes:</strong> Las 4 ingenierías civiles tienen "Tabla complementaria de aspectos curriculares"
              (DR 69-72/2023) descargada del CDN oficial USS — incluye descriptor + resultado de aprendizaje por ramo.
              Los PDFs USS NO incluyen códigos tipo MAT101. Ing. Comercial verificada con folleto oficial 2019;
              USS anunció renovación curricular comercial — re-verificar antes de producción de ese split.
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-4 bg-white rounded-xl p-1 shadow-sm">
          {[
            { id: "carreras", label: "Por Carrera" },
            { id: "splitting", label: "Matriz Splitting" },
            { id: "pipeline", label: "Pipeline (a producir)" },
            { id: "fuentes", label: "Fuentes" },
          ].map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={"flex-1 py-2.5 rounded-lg text-sm font-medium transition-colors " +
                (tab === t.id
                  ? "bg-red-700 text-white shadow"
                  : "text-gray-600 hover:bg-gray-100")}
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
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
              <input
                type="text"
                placeholder="Buscar carrera o ramo..."
                value={filtro}
                onChange={(e) => setFiltro(e.target.value)}
                className="md:col-span-2 px-4 py-2.5 rounded-xl border bg-white text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-red-400"
              />
              <select
                value={areaFiltro}
                onChange={(e) => setAreaFiltro(e.target.value)}
                className="px-4 py-2.5 rounded-xl border bg-white text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-red-400"
              >
                <option value="todas">Todas las áreas</option>
                <option value="matemáticas">Matemáticas</option>
                <option value="física">Física</option>
                <option value="química">Química</option>
                <option value="programación">Programación</option>
                <option value="economía">Economía</option>
                <option value="otra">Otra</option>
              </select>
            </div>
            {carrerasFiltradas.map((c) => (
              <CarreraSection key={c.id} carrera={c} />
            ))}
            {carrerasFiltradas.length === 0 && (
              <div className="bg-white rounded-xl p-8 text-center text-gray-500">
                No hay ramos que coincidan con el filtro.
              </div>
            )}
          </>
        )}

        {tab === "splitting" && <MatrizSplitting />}
        {tab === "pipeline" && <Pipeline />}

        {tab === "fuentes" && (
          <div className="bg-white rounded-xl shadow-sm p-5">
            <h3 className="font-bold text-gray-800 mb-4">Fuentes documentadas</h3>
            <p className="text-sm text-gray-600 mb-4">
              Datos extraídos de las Tablas complementarias de aspectos curriculares de USS
              (DR 69-72/2023, Plan 2024 Jornada Diurna), descargadas del CDN oficial cdn.uss.cl.
              Para Ing. Comercial se usó el folleto oficial 2019 desde resources.uss.cl, complementado
              con el perfil de egreso. Datos vigentes para Admisión 2026.
            </p>
            {["Programa", "Portal", "Malla", "Referencia"].map((tipo) => (
              <div key={tipo} className="mb-5">
                <h4 className="font-semibold text-sm text-gray-700 mb-2 uppercase tracking-wide">{tipo}s</h4>
                <div className="space-y-1">
                  {fuentes
                    .filter((f) => f.tipo === tipo)
                    .map((f, i) => (
                      <div key={i} className="flex items-center gap-2 text-sm">
                        <span className={"w-2 h-2 rounded-full " + (
                          tipo === "Programa" ? "bg-green-400"
                          : tipo === "Portal" ? "bg-purple-400"
                          : tipo === "Malla" ? "bg-blue-400"
                          : "bg-amber-400"
                        )} />
                        <span className="text-gray-700 font-medium">{f.nombre}</span>
                        <a href={f.url} target="_blank" rel="noopener" className="text-blue-500 underline text-xs truncate max-w-md">
                          {f.url.replace("https://cdn.uss.cl/", "cdn.uss/").replace("https://admision.uss.cl/", "admision.uss/").replace("https://www.studocu.com/cl/", "studocu/").replace("https://resources.uss.cl/", "resources.uss/")}
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
          Investigación Se Remonta × USS · Datos verificados abril 2026 · Fuentes oficiales USS (DR 69-72/2023) + folleto Comercial 2019
        </div>
      </div>
    </div>
  );
}

export { seRemontaCursos, carreras };
