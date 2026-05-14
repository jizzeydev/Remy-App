// ═══════════════════════════════════════════════════════════════
// PLANTILLA — Investigación Ramos Matemáticos [SIGLA]
//
// Reemplazá [PLACEHOLDERS] con los datos reales y borrá esta nota.
//
// Fuentes consultadas:
//   - [URL malla oficial PDF]
//   - [URL syllabus por ramo]
//   - [URL plataforma apuntes]
// Fecha de investigación: [MES AÑO]
// ═══════════════════════════════════════════════════════════════

import { useState } from "react";

// ─── CATÁLOGO BASE — copiar TAL CUAL del prompt PROMPT_COWORK.md ───
// (no remover ni renombrar; el migrador asume estos 9 ids exactos)
const seRemontaCursos = [
  { id: "precalculo-cero",      nombre: "Precálculo desde Cero",      tipo: "general", modulos: 68,   precio: 40000, color: "#8B5CF6", contenidos: ["Conjuntos y números","Álgebra de expresiones","Ecuaciones e inecuaciones","Funciones","Trigonometría","Geometría analítica"] },
  { id: "nivelacion-ing",       nombre: "Nivelación Ingeniería",      tipo: "general", modulos: 43,   precio: 20000, color: "#7C3AED", contenidos: ["Repaso números reales","Funciones elementales","Trigonometría aplicada","Vectores y geometría","Lógica e inducción","Polinomios"] },
  { id: "algebra-lineal-gen",   nombre: "Álgebra Lineal",             tipo: "general", modulos: 52,   precio: 40000, color: "#6366F1", contenidos: ["Espacio","Sistemas de Ecuaciones","Álgebra de Matrices","Determinantes","Espacios y Subespacios Vectoriales","Valores y Vectores Propios","Ortogonalidad","Matrices Simétricas"] },
  { id: "calculo-1var-gen",     nombre: "Cálculo en una Variable",    tipo: "general", modulos: 85,   precio: 40000, color: "#3B82F6", contenidos: ["Límites y continuidad","Derivadas","Aplicaciones de la derivada","Integrales","Técnicas de integración","Aplicaciones de la integral"] },
  { id: "calculo-dif-gen",      nombre: "Cálculo Diferencial",        tipo: "general", modulos: 52,   precio: 35000, color: "#0EA5E9", contenidos: ["Números reales e inecuaciones","Funciones (dominio, recorrido, transformaciones, polinomiales, exp, log)","Límites y continuidad","Derivadas y reglas de derivación","Aplicaciones de la derivada (TVM, L'Hôpital, optimización, graficación)"] },
  { id: "calculo-int-gen",      nombre: "Cálculo Integral",           tipo: "general", modulos: 48,   precio: 35000, color: "#06B6D4", contenidos: ["Antiderivadas e integral indefinida","Teorema Fundamental del Cálculo","Técnicas (sustitución, partes, fracciones parciales, sustitución trigonométrica)","Aplicaciones (área, volúmenes, longitud de arco, parametrizadas, polares)","Integrales impropias","Sucesiones y series (criterios, Taylor, potencias)"] },
  { id: "calculo-vvar-gen",     nombre: "Cálculo en Varias Variables",tipo: "general", modulos: 41,   precio: 40000, color: "#14B8A6", contenidos: ["Funciones de varias variables","Derivadas parciales y gradiente","Máximos y mínimos","Multiplicadores de Lagrange","Integrales dobles y triples","Coordenadas curvilíneas"] },
  { id: "calculo-vec-gen",      nombre: "Cálculo Vectorial",          tipo: "general", modulos: 31,   precio: 40000, color: "#10B981", contenidos: ["Curvas paramétricas y vectoriales","Integrales de línea (escalares y vectoriales)","Teorema de Green","Rotacional y divergencia","Integrales de superficie","Teorema de Stokes","Teorema de la divergencia"] },
  { id: "ec-dif-gen",           nombre: "Ecuaciones Diferenciales",   tipo: "general", modulos: 42,   precio: 40000, color: "#EAB308", contenidos: ["EDO primer orden (separable, lineal, exacta, factor integrante, homogénea, Bernoulli)","EDO segundo orden (coef constantes, Cauchy-Euler, coef indeterminados, variación parámetros)","Sistemas de ED","Transformada de Laplace (propiedades, traslación, escalón, convolución, Dirac)","Soluciones por series (Bessel, Frobenius)","Aplicaciones (mecánica, circuitos, modelos)"] },
];

// ─── CARRERAS DE LA U ───────────────────────────────────────────
const carreras = [
  // ═══════════════════════════════════════
  // CARRERA 1 — Ingeniería Civil Plan Común (obligatorio)
  // ═══════════════════════════════════════
  {
    id: "plan-comun",
    nombre: "Ingeniería Civil Plan Común",
    facultad: "[Facultad]",
    duracion: "[X años de plan común + Y de especialización]",
    especialidades: [
      "[Esp 1]",
      "[Esp 2]",
    ],
    mallaUrl: "[URL del PDF oficial de la malla]",
    nota: "[Acreditación, observaciones]",
    ramos: [
      {
        nombre: "[Nombre exacto del ramo según malla]",
        semestre: 1,
        prereqs: "[Pre-requisitos o 'Sin prerrequisitos']",
        fuenteContenido: "[URL del syllabus o plataforma de apuntes]",
        contenidos: [
          "[Tema 1 con sub-temas]",
          "[Tema 2 con sub-temas]",
          "[...]",
        ],
        match: ["[id-curso-base-1]", "[id-curso-base-2-si-aplica]"],
        matchLevel: "alto", // alto | medio | bajo | ninguno
        splitDesde: "[Justificación: <curso base> cubre X. Falta grabar Y.]",
        nota: "[Opcional: limitaciones de la verificación, bibliografía]",
      },
      // ... más ramos en orden de semestre ...
    ],
  },

  // ═══════════════════════════════════════
  // CARRERA 2 — Ingeniería Comercial (si la U la dicta)
  // ═══════════════════════════════════════
  {
    id: "ing-comercial",
    nombre: "Ingeniería Comercial",
    facultad: "[Facultad de Economía y Negocios]",
    duracion: "[X años]",
    especialidades: [],
    mallaUrl: "[URL]",
    ramos: [
      // ramos matemáticos de Ing. Comercial
    ],
  },

  // ... más carreras opcionales (College, Civil Industrial, etc.) ...
];
