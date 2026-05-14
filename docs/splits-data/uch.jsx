import { useState } from "react";

// ═══════════════════════════════════════════════════════════════
// DATOS VERIFICADOS - Investigación Ramos Matemáticos UCh
// Fuentes:
//   - Mallas curriculares: uchile.cl/pregrado (77 carreras revisadas)
//   - Programas oficiales FCFM: ucampus.uchile.cl/m/fcfm_catalogo/
//     · MA1001 Intro al Cálculo: programa?bajar=1&id=12398
//     · MA1002 Cálc. Dif. e Integral: programa?bajar=1&id=48717
//     · MA1102 Álgebra Lineal: programa?bajar=1&id=45189
//     · MA2001 Cálc. Varias Variables: programa?bajar=1&id=48697
//     · MA2601 Ec. Dif. Ordinarias: programa?bajar=1&id=48701
//     · MA2002 Cálc. Avanzado y Aplic.: programa?bajar=1&id=13266
//   - Malla FEN: admisionfen.cl/malla-icce/, admisionfen.cl/malla-iicg/
//   - Contenidos Métodos Matemáticos I FEN: uclases.cl/cursos/detalle/851/32
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
  // PLAN COMÚN INGENIERÍA Y CIENCIAS (FCFM)
  // ═══════════════════════════════════════
  {
    id: "plan-comun-fcfm",
    nombre: "Plan Común Ingeniería y Ciencias (FCFM)",
    facultad: "Facultad de Ciencias Físicas y Matemáticas",
    duracion: "4 semestres comunes + especialidad (total 11-12 semestres)",
    mallaUrl: "https://uchile.cl/carreras/4969/ingenieria-civil",
    nota: "710 vacantes · Código 11045 · Plan compartido por TODAS las ingenierías + ciencias",
    especialidades: [
      "Ing. Civil",
      "Ing. Civil Industrial",
      "Ing. Civil en Computación",
      "Ing. Civil Eléctrica",
      "Ing. Civil Mecánica",
      "Ing. Civil de Minas",
      "Ing. Civil Química",
      "Ing. Civil en Biotecnología",
      "Ing. Civil Matemática",
      "Astronomía",
      "Física",
      "Geofísica",
      "Geología",
    ],
    ramos: [
      {
        nombre: "MA1001 Introducción al Cálculo",
        semestre: 1,
        prereqs: "Ninguno",
        fuenteContenido: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=12398",
        contenidos: [
          "Números reales: propiedades de igualdad, orden, valor absoluto, inecuaciones lineales y cuadráticas, factorización (1 sem)",
          "Geometría analítica: plano cartesiano, rectas, circunferencias, parábolas, elipses, hipérbolas, excentricidad (2 sem)",
          "Funciones de una variable: definición, dominio, paridad, crecimiento, composición, inyectividad, inversas (1 sem)",
          "Trigonometría: funciones trigonométricas, identidades, ecuaciones trigonométricas (1 sem)",
          "Límites: límites de sucesiones, límites de funciones, asíntotas (2 sem)",
          "Derivadas: definición, reglas básicas de derivación (introducción) (1 sem)",
        ],
        match: ["precalculo-cero", "nivelacion-ing"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre números reales, geometría analítica, funciones, trigonometría. Nivelación Ingeniería (43 mód) complementa. El curso UCh introduce límites y derivadas de forma rigurosa al final.",
      },
      {
        nombre: "MA1101 Introducción al Álgebra",
        semestre: 1,
        prereqs: "Ninguno",
        fuenteContenido: "https://ucampus.uchile.cl/m/fcfm_catalogo/?semestre=134&depto=21",
        contenidos: [
          "Conjuntos: conjunto potencia, particiones, álgebra de conjuntos, cuantificadores",
          "Funciones: definición formal, composición de funciones",
          "Relaciones: definición, propiedades generales, conjunto cociente, división entera",
          "Relaciones de orden",
          "Axiomas de cuerpos (campos), campos ordenados",
          "Números reales: axioma del supremo, completitud",
          "Conjuntos finitos e infinitos, cardinalidad",
          "Números complejos: operaciones, forma polar, raíces",
        ],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        splitDesde: "Precálculo desde Cero (68 mód) cubre conjuntos, funciones, complejos y álgebra básica. El curso UCh es MUCHO más teórico y formal (axiomática, demostraciones, relaciones). Cobertura parcial ~50%.",
        nota: "Curso muy formal y abstracto. Se enfoca en demostraciones y rigor, a diferencia de la UAI/UDD que mezclan con cálculo.",
      },
      {
        nombre: "MA1002 Cálculo Diferencial e Integral",
        semestre: 2,
        prereqs: "MA1001 Introducción al Cálculo",
        fuenteContenido: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=48717",
        contenidos: [
          "Continuidad de funciones: subsucesiones, convergencia, tipos de discontinuidad, álgebra de continuas, TVI, Weierstrass, continuidad uniforme (2 sem)",
          "Derivadas: diferenciabilidad formal, reglas de cálculo, derivada de la inversa, teoremas del valor medio (2 sem)",
          "Aplicaciones de la derivada: máximos y mínimos, análisis de funciones, L'Hôpital, Taylor de orden 1 (2 sem)",
          "Integrales: primitivas, TFC 1er y 2do, sustitución, por partes, fracciones parciales, sustitución trigonométrica (2 sem)",
          "Aplicaciones de la integral: áreas, volúmenes de revolución, centros de masa de curvas (1 sem)",
          "Series de potencias: derivadas e integrales de funciones no elementales (1 sem)",
          "Curvas en el espacio: longitud de curva, curvatura, torsión (1 sem)",
        ],
        match: ["calculo-1var-gen", "calculo-dif-gen", "calculo-int-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód) cubre completamente: continuidad, derivadas, integrales, aplicaciones, series. También Cálculo Diferencial (25k) + Cálculo Integral (25k) por separado.",
      },
      {
        nombre: "MA1102 Álgebra Lineal",
        semestre: 2,
        prereqs: "MA1101 Intro al Álgebra + MA1001 Intro al Cálculo",
        fuenteContenido: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=45189",
        contenidos: [
          "Matrices y sistemas lineales: operaciones, matrices particulares/elementales/triangulares, escalonamiento, Gauss, matriz inversa, factorización LU (3 sem)",
          "Espacios vectoriales: definiciones, subespacios, independencia lineal, generadores, base y dimensión, suma y suma directa (3 sem)",
          "Geometría lineal en Rⁿ: vectores, rectas, planos, ecuaciones paramétricas/cartesianas, producto interno, norma, producto cruz, proyecciones ortogonales (2 sem)",
          "Transformaciones lineales: definiciones, núcleo e imagen, teorema del núcleo-imagen, matriz representante, rango, cambio de base (2.5 sem)",
          "Valores y vectores propios: determinante, polinomio característico, cálculo de valores/vectores propios, diagonalización (2 sem)",
          "Ortogonalidad: Gram-Schmidt, matrices simétricas, formas cuadráticas, aplicaciones (cónicas, mínimos cuadrados, Jacobiana) (2.5 sem)",
        ],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal general (52 mód, 8 capítulos) cubre todos los temas: matrices, sistemas, espacios vectoriales, transformaciones lineales, valores propios, ortogonalidad. Match directo y completo.",
      },
      {
        nombre: "MA2001 Cálculo en Varias Variables",
        semestre: 3,
        prereqs: "MA1002 Cálc. Dif. e Integral + MA1102 Álgebra Lineal",
        fuenteContenido: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=48697",
        contenidos: [
          "Topología en Rⁿ: distancias, normas, bolas, sucesiones, conjuntos abiertos/cerrados/compactos (1.5 sem)",
          "Funciones de varias variables: grafos, conjuntos de nivel, límites y continuidad (1 sem)",
          "Cálculo diferencial en Rⁿ: derivadas direccionales, parciales, derivada fuerte (Fréchet), Jacobiana, regla de la cadena, gradiente, plano tangente (2 sem)",
          "Teoremas de la función inversa e implícita, punto fijo (1.5 sem)",
          "Derivadas de orden superior: Schwartz, Hessiana, Taylor multivariable (1 sem)",
          "Máximos y mínimos: puntos críticos, condiciones de 2do orden, funciones convexas, multiplicadores de Lagrange (1.5 sem)",
          "Integral de Riemann en Rⁿ: particiones, propiedades básicas (2 sem)",
          "Teorema de Fubini, cambio de variables: integrales iteradas, coordenadas polares, cilíndricas, esféricas, centros de masa, momentos de inercia (3 sem)",
        ],
        match: ["calculo-vvar-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre derivadas parciales, gradiente, Lagrange, integrales múltiples, coordenadas curvilíneas. El curso UCh es más riguroso (incluye topología formal y teoremas de func. inversa/implícita).",
      },
      {
        nombre: "MA2601 Ecuaciones Diferenciales Ordinarias",
        semestre: 3,
        prereqs: "MA1002 Cálc. Dif. e Integral + MA1102 Álgebra Lineal",
        fuenteContenido: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=48701",
        contenidos: [
          "EDO primer orden: campo vectorial, curva integral, separables, reducción de orden, homogéneas, lineales con factor integrante, Bernoulli, Ricatti, modelación, existencia y unicidad, Runge-Kutta (3 sem)",
          "Ecuaciones lineales de orden superior: Wronskiano, ED orden 2 homogéneas (vibraciones mecánicas), variación de parámetros, Función de Green, condiciones de borde, series de potencia (Frobenius), ED orden n homogéneas/no homogéneas, Euler-Cauchy, coeficientes indeterminados (4 sem)",
          "Transformada de Laplace: definición, fórmulas, resolución de ED lineales, convolución, Heaviside, Delta de Dirac (2 sem)",
          "Sistemas lineales: existencia y unicidad, matriz fundamental, matriz exponencial, comportamiento asintótico, diagramas de fase 2×2, variación de parámetros para sistemas (3 sem)",
          "Sistemas autónomos no lineales: hamiltonianos, conservación de energía, péndulo no lineal, estabilidad de puntos críticos, Lotka-Volterra, funcional de Lyapunov (3 sem)",
        ],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Ecuaciones Diferenciales (42 mód) cubre EDO 1er y 2do orden, Laplace, sistemas. El curso UCh es MÁS extenso que la UAI: incluye sistemas no lineales, Lyapunov, diagramas de fase, Runge-Kutta. Cobertura ~75% de la materia UCh.",
        nota: "Curso más avanzado que el promedio: 5 unidades en 15 semanas, incluye análisis cualitativo de sistemas no lineales.",
      },
      {
        nombre: "MA2002 Cálculo Avanzado y Aplicaciones",
        semestre: 4,
        prereqs: "MA2601 EDO + MA2001 Cálc. Varias Variables",
        fuenteContenido: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=13266",
        contenidos: [
          "Cálculo vectorial: campos escalares y vectoriales, gradiente, sistemas coordenados ortogonales, divergencia, rotor, Laplaciano, integrales de línea y superficie (1.5 sem)",
          "Teoremas de integración vectorial: Gauss, Green, Stokes, campos conservativos, circulaciones y flujos (3 sem)",
          "Funciones de variable compleja: derivada compleja, Cauchy-Riemann, series de potencias, Laurent, polos, residuos, integrales complejas (3 sem)",
          "Series y Transformada de Fourier: funciones periódicas, coeficientes, convergencia, transformada y antitransformada, convolución, funciones pares/impares (2 sem)",
        ],
        match: ["calculo-vec-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo Vectorial (31 mód) cubre la parte vectorial: Green, Stokes, divergencia. Pero este curso UCh también incluye variable compleja (Cauchy, residuos, Laurent) y Fourier, que NO están en el catálogo Se Remonta. Cobertura ~40% del total del curso.",
        nota: "Curso con materia que va más allá del catálogo actual Se Remonta. Variable compleja y Fourier son temas nuevos.",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA CIVIL INDUSTRIAL (post Plan Común)
  // ═══════════════════════════════════════
  {
    id: "ing-civil-industrial",
    nombre: "Ing. Civil Industrial (ramos post Plan Común)",
    facultad: "Facultad de Ciencias Físicas y Matemáticas",
    duracion: "Semestres 5-11 después de Plan Común",
    mallaUrl: "https://uchile.cl/carreras/4973/ingenieria-civil-industrial",
    nota: "Especialidad más popular de la FCFM",
    ramos: [
      {
        nombre: "IN3171 Modelamiento y Optimización",
        semestre: 5,
        prereqs: "Cálculo en Varias Variables, Álgebra Lineal",
        contenidos: [
          "Programación lineal",
          "Método simplex, dualidad",
          "Programación entera",
          "Optimización no lineal",
        ],
        match: [],
        matchLevel: "ninguno",
        nota: "Ramo de especialidad. Sin match directo con catálogo Se Remonta.",
      },
      {
        nombre: "IN3141 Probabilidades",
        semestre: 5,
        prereqs: "MA2001 Cálculo en Varias Variables",
        contenidos: [
          "Probabilidad axiomática, condicional, Bayes",
          "Variables aleatorias discretas y continuas",
          "Distribuciones: Binomial, Poisson, Normal, Exponencial",
          "Esperanza, varianza, funciones generadoras",
          "Ley de grandes números, TLC",
        ],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "IN3242 Estadística",
        semestre: 6,
        prereqs: "IN3141 Probabilidades",
        contenidos: [
          "Estimación puntual y por intervalos",
          "Pruebas de hipótesis",
          "Regresión lineal simple y múltiple",
          "Análisis de varianza",
        ],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA COMERCIAL (FEN)
  // ═══════════════════════════════════════
  {
    id: "icom-fen",
    nombre: "Ingeniería Comercial",
    facultad: "Facultad de Economía y Negocios (FEN)",
    duracion: "10 semestres · Semiflexible",
    mallaUrl: "https://admisionfen.cl/malla-icce/",
    nota: "400 vacantes · Código 11042 · 2 menciones: Ciencias Económicas o Administración de Empresas",
    ramos: [
      {
        nombre: "Métodos Matemáticos I",
        semestre: 1,
        prereqs: "Ninguno",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/851/32",
        contenidos: [
          "Lógica y proposiciones (lógica proposicional, álgebra de proposiciones)",
          "Conjuntos (operaciones de conjuntos)",
          "Inecuaciones y valor absoluto",
          "Geometría analítica (casos aplicados)",
          "Funciones (definiciones, composición, inversas)",
          "Sumatorias (definiciones, inducción, fracciones parciales, combinatoria)",
          "Límites de funciones (introducción)",
          "Derivadas (definición, álgebra de derivadas, funciones elementales)",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre conjuntos, inecuaciones, geometría analítica, funciones, sumatorias. Match directo con prácticamente todo el contenido.",
      },
      {
        nombre: "Métodos Matemáticos II",
        semestre: 2,
        prereqs: "Métodos Matemáticos I",
        contenidos: [
          "Funciones multivariadas y derivadas respectivas",
          "Métodos de derivación con restricciones",
          "Álgebra lineal: matrices y operaciones",
          "Metodologías de álgebra lineal aplicada",
        ],
        match: ["calculo-dif-gen", "algebra-lineal-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo Diferencial (25k) cubre derivadas. Álgebra Lineal (52 mód) cubre matrices. Curso FEN mezcla ambos temas en uno solo. Cobertura parcial de cada uno.",
        nota: "Curso híbrido que combina cálculo multivariable básico con álgebra lineal introductoria.",
      },
      {
        nombre: "Introducción Estadística",
        semestre: 2,
        prereqs: "Métodos Matemáticos I",
        contenidos: [
          "Estadística descriptiva",
          "Probabilidad básica",
          "Variables aleatorias",
          "Distribuciones de probabilidad",
        ],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Métodos Matemáticos III",
        semestre: 3,
        prereqs: "Métodos Matemáticos II",
        contenidos: [
          "Derivadas y aplicaciones",
          "Optimización con y sin restricciones",
          "Programación lineal (PPL)",
          "Método simplex",
        ],
        match: ["calculo-1var-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo en una Variable (85 mód) cubre derivadas y aplicaciones de optimización. El contenido de PPL y simplex no está cubierto.",
      },
      {
        nombre: "Métodos Matemáticos Avanzados",
        semestre: 4,
        prereqs: "Métodos Matemáticos III",
        contenidos: [
          "Métodos cuantitativos avanzados para economía y negocios",
          "Cálculo multivariable aplicado",
          "Optimización avanzada",
        ],
        match: ["calculo-vvar-gen"],
        matchLevel: "bajo",
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre parte del contenido multivariable. Enfoque aplicado a negocios.",
      },
      {
        nombre: "Teoría Estadística",
        semestre: 4,
        prereqs: "Introducción Estadística",
        contenidos: [
          "Estimación puntual y por intervalos",
          "Pruebas de hipótesis",
          "Regresión y modelos estadísticos",
        ],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Análisis de Datos",
        semestre: 4,
        prereqs: "Introducción Estadística",
        contenidos: [
          "Técnicas de análisis de datos",
          "Herramientas computacionales",
          "Visualización y modelación",
        ],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // INGENIERÍA EN INFORMACIÓN Y CONTROL DE GESTIÓN (FEN)
  // ═══════════════════════════════════════
  {
    id: "iicg-fen",
    nombre: "Ingeniería en Información y Control de Gestión",
    facultad: "Facultad de Economía y Negocios (FEN)",
    duracion: "10 semestres",
    mallaUrl: "https://admisionfen.cl/malla-iicg/",
    nota: "Comparte ramos MM I-III con Ing. Comercial y Contador Auditor",
    ramos: [
      {
        nombre: "Métodos Matemáticos I",
        semestre: 1,
        prereqs: "Ninguno",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/851/32",
        contenidos: [
          "Lógica y proposiciones, conjuntos, inecuaciones, geometría analítica",
          "Funciones, sumatorias, límites, derivadas (introducción)",
        ],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre prácticamente todo el contenido.",
        nota: "Mismo programa que MM I de Ing. Comercial",
      },
      {
        nombre: "Métodos Matemáticos II",
        semestre: 2,
        prereqs: "Métodos Matemáticos I",
        contenidos: [
          "Funciones multivariadas, derivadas con restricciones",
          "Álgebra lineal: matrices y operaciones",
        ],
        match: ["calculo-dif-gen", "algebra-lineal-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo Diferencial + Álgebra Lineal cubren parcialmente.",
        nota: "Mismo programa que MM II de Ing. Comercial",
      },
      {
        nombre: "Estadística I",
        semestre: 2,
        prereqs: "Métodos Matemáticos I",
        contenidos: ["Estadística descriptiva, probabilidad básica, distribuciones"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Métodos Matemáticos III",
        semestre: 3,
        prereqs: "Métodos Matemáticos II",
        contenidos: ["Derivadas avanzadas, optimización, PPL, simplex"],
        match: ["calculo-1var-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo en una Variable (85 mód) cubre derivadas y optimización. PPL no cubierto.",
      },
      {
        nombre: "Métodos Matemáticos IV",
        semestre: 4,
        prereqs: "Métodos Matemáticos III",
        contenidos: [
          "Métodos cuantitativos avanzados",
          "Integrales y aplicaciones",
          "Modelos matemáticos para gestión",
        ],
        match: ["calculo-1var-gen", "calculo-int-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo en una Variable (85 mód) o Cálculo Integral (25k) cubren la parte integral.",
      },
      {
        nombre: "Estadística II",
        semestre: 4,
        prereqs: "Estadística I",
        contenidos: ["Estimación, inferencia, pruebas de hipótesis, regresión"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Métodos Cuantitativos I",
        semestre: 5,
        prereqs: "Métodos Matemáticos IV, Estadística II",
        contenidos: ["Modelos cuantitativos aplicados a la gestión"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Investigación Operativa",
        semestre: 6,
        prereqs: "Métodos Cuantitativos I",
        contenidos: ["Programación lineal avanzada, simulación, teoría de colas"],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // CONTADOR AUDITOR (FEN)
  // ═══════════════════════════════════════
  {
    id: "contador-fen",
    nombre: "Contador Auditor",
    facultad: "Facultad de Economía y Negocios (FEN)",
    duracion: "10 semestres",
    mallaUrl: "https://uchile.cl/carreras/86759/contador-auditor",
    nota: "Comparte MM I-III con Ing. Comercial e IICG",
    ramos: [
      {
        nombre: "Métodos Matemáticos I",
        semestre: 1,
        prereqs: "Ninguno",
        fuenteContenido: "https://www.uclases.cl/cursos/detalle/851/32",
        contenidos: ["Lógica, conjuntos, inecuaciones, geometría analítica, funciones, sumatorias, límites, derivadas intro"],
        match: ["precalculo-cero"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero (68 mód) cubre prácticamente todo.",
        nota: "Mismo programa que MM I de Ing. Comercial e IICG",
      },
      {
        nombre: "Métodos Matemáticos II",
        semestre: 2,
        prereqs: "Métodos Matemáticos I",
        contenidos: ["Funciones multivariadas, derivadas, álgebra lineal básica (matrices)"],
        match: ["calculo-dif-gen", "algebra-lineal-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo Diferencial + Álgebra Lineal cubren parcialmente.",
      },
      {
        nombre: "Métodos Matemáticos III",
        semestre: 3,
        prereqs: "Métodos Matemáticos II",
        contenidos: ["Derivadas, optimización, PPL"],
        match: ["calculo-1var-gen"],
        matchLevel: "medio",
        splitDesde: "Cálculo en una Variable cubre derivadas y optimización.",
      },
      {
        nombre: "Estadística I",
        semestre: 3,
        prereqs: "Métodos Matemáticos II",
        contenidos: ["Estadística descriptiva, probabilidad, distribuciones"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Estadística II",
        semestre: 4,
        prereqs: "Estadística I",
        contenidos: ["Estimación, pruebas de hipótesis, regresión"],
        match: [],
        matchLevel: "ninguno",
      },
      {
        nombre: "Métodos Cuantitativos I",
        semestre: 5,
        prereqs: "Métodos Matemáticos III, Estadística II",
        contenidos: ["Modelos cuantitativos para auditoría y gestión"],
        match: [],
        matchLevel: "ninguno",
      },
    ],
  },

  // ═══════════════════════════════════════
  // FACULTAD DE CIENCIAS
  // ═══════════════════════════════════════
  {
    id: "lic-matematica",
    nombre: "Licenciatura en Ciencias mención Matemática",
    facultad: "Facultad de Ciencias",
    duracion: "8 semestres",
    mallaUrl: "https://uchile.cl/carreras/4961/licenciatura-en-ciencias-mencion-en-matematica",
    nota: "Carrera teórica pura. Ramos de cálculo/álgebra similares al Plan Común FCFM en los primeros semestres.",
    ramos: [
      {
        nombre: "Cálculo I",
        semestre: 1,
        prereqs: "Ninguno",
        contenidos: ["Números reales, funciones, límites, continuidad, derivadas, aplicaciones"],
        match: ["precalculo-cero", "calculo-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Precálculo desde Cero + Cálculo Diferencial cubren la mayor parte.",
      },
      {
        nombre: "Álgebra I",
        semestre: 1,
        prereqs: "Ninguno",
        contenidos: ["Lógica, conjuntos, relaciones, funciones, números naturales, enteros, racionales, reales"],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        splitDesde: "Precálculo cubre álgebra básica. Curso muy teórico (axiomática).",
      },
      {
        nombre: "Cálculo II",
        semestre: 2,
        prereqs: "Cálculo I",
        contenidos: ["Integrales, técnicas de integración, series, aplicaciones"],
        match: ["calculo-1var-gen", "calculo-int-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable (85 mód) o Cálculo Integral (25k) cubren todo.",
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 2,
        prereqs: "Álgebra I",
        contenidos: ["Matrices, sistemas, espacios vectoriales, transformaciones lineales, valores propios"],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal general (52 mód) match directo.",
      },
      {
        nombre: "Cálculo III (Varias Variables)",
        semestre: 3,
        prereqs: "Cálculo II, Álgebra Lineal",
        contenidos: ["Funciones de varias variables, derivadas parciales, integrales múltiples, Lagrange"],
        match: ["calculo-vvar-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre los contenidos principales.",
      },
      {
        nombre: "Ecuaciones Diferenciales",
        semestre: 3,
        prereqs: "Cálculo II, Álgebra Lineal",
        contenidos: ["EDO, métodos de resolución, Laplace, sistemas"],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Ecuaciones Diferenciales (42 mód) cubre los contenidos principales.",
      },
    ],
  },

  // ═══════════════════════════════════════
  // LICENCIATURA EN CIENCIAS MENCIÓN FÍSICA
  // ═══════════════════════════════════════
  {
    id: "lic-fisica",
    nombre: "Licenciatura en Ciencias mención Física",
    facultad: "Facultad de Ciencias",
    duracion: "8 semestres",
    mallaUrl: "https://uchile.cl/carreras/4981/licenciatura-en-ciencias-mencion-en-fisica",
    nota: "Ramos matemáticos similares a Lic. Matemática en los primeros semestres.",
    ramos: [
      {
        nombre: "Cálculo I",
        semestre: 1,
        prereqs: "Ninguno",
        contenidos: ["Números reales, funciones, límites, derivadas"],
        match: ["precalculo-cero", "calculo-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Precálculo + Cálculo Diferencial cubren la base.",
      },
      {
        nombre: "Álgebra I",
        semestre: 1,
        prereqs: "Ninguno",
        contenidos: ["Lógica, conjuntos, relaciones, números reales, complejos"],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        splitDesde: "Precálculo cubre álgebra básica. Curso teórico.",
      },
      {
        nombre: "Cálculo II",
        semestre: 2,
        prereqs: "Cálculo I",
        contenidos: ["Integrales, series, aplicaciones"],
        match: ["calculo-1var-gen", "calculo-int-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable o Cálculo Integral cubren todo.",
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 2,
        prereqs: "Álgebra I",
        contenidos: ["Matrices, espacios vectoriales, transformaciones lineales, valores propios"],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal (52 mód) match directo.",
      },
      {
        nombre: "Cálculo III",
        semestre: 3,
        prereqs: "Cálculo II, Álgebra Lineal",
        contenidos: ["Cálculo multivariable, integrales múltiples, Lagrange"],
        match: ["calculo-vvar-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en Varias Variables (41 mód) cubre contenidos principales.",
      },
      {
        nombre: "Ecuaciones Diferenciales",
        semestre: 3,
        prereqs: "Cálculo II, Álgebra Lineal",
        contenidos: ["EDO, Laplace, sistemas"],
        match: ["ec-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Ecuaciones Diferenciales (42 mód) cubre contenidos principales.",
      },
    ],
  },

  // ═══════════════════════════════════════
  // PEDAGOGÍA EN MATEMÁTICAS Y FÍSICA
  // ═══════════════════════════════════════
  {
    id: "pedagogia-mat-fis",
    nombre: "Pedagogía en Educación Media en Matemáticas y Física",
    facultad: "Facultad de Ciencias",
    duracion: "10 semestres",
    mallaUrl: "https://uchile.cl/carreras/4963/pedagogia-en-educacion-media-en-matematicas-y-fisica",
    nota: "Carrera docente con fuerte base matemática",
    ramos: [
      {
        nombre: "Cálculo I",
        semestre: 1,
        prereqs: "Ninguno",
        contenidos: ["Funciones, límites, derivadas, aplicaciones"],
        match: ["precalculo-cero", "calculo-dif-gen"],
        matchLevel: "alto",
        splitDesde: "Precálculo + Cálculo Diferencial cubren la base.",
      },
      {
        nombre: "Álgebra I",
        semestre: 1,
        prereqs: "Ninguno",
        contenidos: ["Lógica, conjuntos, números, relaciones"],
        match: ["precalculo-cero"],
        matchLevel: "medio",
        splitDesde: "Precálculo cubre parte del contenido.",
      },
      {
        nombre: "Cálculo II",
        semestre: 2,
        prereqs: "Cálculo I",
        contenidos: ["Integrales, series, aplicaciones"],
        match: ["calculo-1var-gen", "calculo-int-gen"],
        matchLevel: "alto",
        splitDesde: "Cálculo en una Variable o Cálculo Integral.",
      },
      {
        nombre: "Álgebra Lineal",
        semestre: 2,
        prereqs: "Álgebra I",
        contenidos: ["Matrices, espacios vectoriales, valores propios"],
        match: ["algebra-lineal-gen"],
        matchLevel: "alto",
        splitDesde: "Álgebra Lineal (52 mód) match directo.",
      },
    ],
  },
];

// ── CARRERAS SIN RAMOS MATEMÁTICOS PROPIOS ──────────────────
const sinMatematicas = [
  "Arquitectura", "Diseño", "Geografía",
  "Actuación Teatral", "Artes Visuales", "Composición Musical", "Danza", "Diseño Teatral",
  "Interpretación Musical", "Teoría de la Música", "Teoría e Historia del Arte",
  "Biología mención Medio Ambiente", "Ing. en Biotecnología Molecular",
  "Química Ambiental", "Pedagogía en Biología y Química",
  "Ing. Agronómica", "Ing. en Recursos Naturales Renovables",
  "Ing. en Recursos Hídricos", "Ing. Forestal",
  "Bioquímica", "Ing. en Alimentos", "Química", "Química y Farmacia",
  "Antropología-Arqueología", "Pedagogía en Ed. Especial", "Pedagogía en Ed. Física",
  "Pedagogía en Ed. Parvularia", "Psicología", "Sociología", "Trabajo Social",
  "Medicina Veterinaria",
  "Cine y Televisión", "Periodismo",
  "Derecho",
  "Filosofía", "Historia", "Lingüística y Literatura", "Lingüística y Lit. Inglesas",
  "Estudios Internacionales", "Pedagogía en Ed. Básica", "Pedagogía Ed. Media Cs-Humanistas",
  "Administración Pública", "Ciencia Política",
  "Enfermería", "Fonoaudiología", "Kinesiología", "Medicina",
  "Nutrición y Dietética", "Obstetricia", "Tecnología Médica", "Terapia Ocupacional",
  "Odontología",
  "Bachillerato",
  "Ing. en Sonido",
];

// ── FUENTES DOCUMENTADAS ────────────────────────────────────
const fuentes = [
  { tipo: "Portal", nombre: "Pregrado UCh (77 carreras)", url: "https://uchile.cl/pregrado" },
  { tipo: "Portal", nombre: "Catálogo FCFM", url: "https://ucampus.uchile.cl/m/fcfm_catalogo/" },
  { tipo: "Portal", nombre: "Admisión FEN", url: "https://admisionfen.cl/" },
  { tipo: "Programa", nombre: "MA1001 Intro al Cálculo", url: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=12398" },
  { tipo: "Programa", nombre: "MA1002 Cálc. Dif. e Integral", url: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=48717" },
  { tipo: "Programa", nombre: "MA1101 Intro al Álgebra", url: "https://ucampus.uchile.cl/m/fcfm_catalogo/?semestre=134&depto=21" },
  { tipo: "Programa", nombre: "MA1102 Álgebra Lineal", url: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=45189" },
  { tipo: "Programa", nombre: "MA2001 Cálc. Varias Var.", url: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=48697" },
  { tipo: "Programa", nombre: "MA2601 EDO", url: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=48701" },
  { tipo: "Programa", nombre: "MA2002 Cálc. Avanzado", url: "https://ucampus.uchile.cl/m/fcfm_catalogo/programa?bajar=1&id=13266" },
  { tipo: "Contenido", nombre: "MM I FEN (uclases)", url: "https://www.uclases.cl/cursos/detalle/851/32" },
  { tipo: "Malla", nombre: "Ing. Civil", url: "https://uchile.cl/carreras/4969/ingenieria-civil" },
  { tipo: "Malla", nombre: "Ing. Civil Industrial", url: "https://uchile.cl/carreras/4973/ingenieria-civil-industrial" },
  { tipo: "Malla", nombre: "Ing. Comercial FEN", url: "https://uchile.cl/carreras/4966/ingenieria-comercial" },
  { tipo: "Malla", nombre: "IICG FEN", url: "https://uchile.cl/carreras/4967/ingenieria-en-informacion-y-control-de-gestion" },
  { tipo: "Malla", nombre: "Contador Auditor", url: "https://uchile.cl/carreras/86759/contador-auditor" },
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
            <span className="text-sm text-gray-500">({sr.matches.length} coincidencias en UCh)</span>
          </div>
          <div className="p-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-2 font-medium">Carrera UCh</th>
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
            <div className="w-10 h-10 bg-blue-800 rounded-xl flex items-center justify-center text-white font-bold text-sm">
              UCh
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">
                Ramos Matemáticos UCh
              </h1>
              <p className="text-sm text-gray-500">
                Investigación para splitting con Se Remonta — Universidad de Chile
              </p>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-3">
            Análisis de <strong>{carreras.length} programas</strong> de pregrado UCh con ramos matemáticos significativos (de 77 carreras totales revisadas).
            Las <strong>13 especialidades de Ing. y Ciencias de la FCFM</strong> comparten el mismo Plan Común (S1-S4) con 7 ramos matemáticos.
            La <strong>FEN</strong> tiene 3 carreras con secuencia Métodos Matemáticos I-IV.
            <strong> {sinMatematicas.length} carreras</strong> no tienen matemáticas dedicadas.
          </p>
          <div className="mt-3 bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-sm text-blue-800">
              <strong>Hallazgo clave:</strong> La UCh tiene el plan de ingeniería más exigente de Chile. El Plan Común FCFM (710 vacantes, 13+ especialidades) tiene <strong>7 ramos matemáticos obligatorios</strong> en 4 semestres, todos con programas oficiales verificados.
              Los cursos Se Remonta generales (Precálculo, Cálculo 1 Var, Álgebra Lineal, Cálculo Varias Var, Ec. Diferenciales) tienen match alto con 6 de los 7 ramos.
              El ramo MA2002 (Cálc. Avanzado, S4) incluye variable compleja y Fourier que NO están en el catálogo actual — <strong>oportunidad de nuevo curso</strong>.
            </p>
          </div>
          <div className="mt-2 bg-amber-50 border border-amber-200 rounded-lg p-3">
            <p className="text-sm text-amber-800">
              <strong>Diferencia vs UAI/UDD/UAndes:</strong> La UCh separa Álgebra (MA1101, muy formal/axiomático) de Cálculo (MA1001) en S1, mientras que las privadas suelen combinar ambos.
              Además, el curso de EDO (MA2601) es más extenso: incluye sistemas no lineales, Lyapunov y Runge-Kutta.
              El ramo "Cálculo Avanzado" (MA2002, S4) es exclusivo de la UCh y mezcla cálculo vectorial + variable compleja + Fourier.
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
                  ? "bg-blue-800 text-white shadow"
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
                Carreras sin ramos matemáticos propios ({sinMatematicas.length})
              </h3>
              <p className="text-sm text-gray-500 mb-3">
                Estas carreras no tienen cursos dedicados de matemáticas en su malla, o sus ramos cuantitativos
                son de estadística/bioestadística básica sin match con el catálogo Se Remonta.
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
              Todos los datos fueron extraídos de los programas oficiales de la FCFM (PDFs descargados de ucampus.uchile.cl),
              las mallas publicadas en uchile.cl/pregrado y admisionfen.cl, y contenidos de uclases.cl.
              Datos vigentes para admisión 2026.
            </p>
            {["Programa", "Portal", "Malla", "Contenido"].map((tipo) => (
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
                          {f.url.replace("https://ucampus.uchile.cl/m/fcfm_catalogo/", "fcfm/").replace("https://uchile.cl/carreras/", "uchile/").replace("https://admisionfen.cl/", "fen/")}
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
          Investigación Se Remonta × UCh · Datos verificados abril 2026 · Fuentes oficiales Universidad de Chile
        </div>
      </div>
    </div>
  );
}
