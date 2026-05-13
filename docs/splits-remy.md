# Splits para Remy — Catálogo de ramos universitarios

> **Propósito:** entregar a Claude Code (proyecto Remy) toda la materia mapeada por universidad/carrera/ramo, lista para construir cursos universitarios derivados de los cursos base de Remy. Misma lógica de splitting que usamos en Se Remonta para los cursos pagados: un curso base general (matemático) se adapta a cada ramo específico de cada universidad.
>
> **Alcance actual:** sólo ramos **matemáticos**. Remy hoy únicamente cubre matemáticas.
>
> **Fuente:** investigación Claude Cowork (abril 2026). Canon vivo en `apps/ops/data/splits/` del repo `se-remonta-ops`.
>
> **Última actualización:** 13 de mayo de 2026.

---

## 1. Cursos base de Remy (= cursos base matemáticos Se Remonta)

Estos son los cursos generales que ya tenemos grabados / disponibles. Cada split universitario debe reutilizarlos como núcleo.

| ID base | Nombre | Módulos | Contenidos / Ejes |
|---|---|---:|---|
| `precalculo-cero` | Precálculo desde Cero | 68 | Conjuntos y números · Álgebra de expresiones · Ecuaciones e inecuaciones · Funciones · Trigonometría · Geometría analítica |
| `nivelacion-ing` | Nivelación Ingeniería | 43 | (Complemento de Precálculo — fundamentos para ingreso a ingeniería) |
| `calculo-dif-gen` | Cálculo Diferencial | — | Límites · Derivadas · Aplicaciones de la derivada (subset de Cálculo 1var) |
| `calculo-int-gen` | Cálculo Integral | — | Integrales · Técnicas de integración · Aplicaciones (subset de Cálculo 1var) |
| `calculo-1var-gen` | Cálculo en una Variable | 85 | Límites y continuidad · Derivadas · Aplicaciones de la derivada · Integrales · Técnicas de integración · Aplicaciones de la integral |
| `algebra-lineal-gen` | Álgebra Lineal | 52 | Espacio · Sistemas de Ecuaciones · Álgebra de Matrices · Determinantes · Espacios y Subespacios Vectoriales · Valores y Vectores Propios · Ortogonalidad · Matrices Simétricas |
| `calculo-vvar-gen` | Cálculo en Varias Variables | 41 | Funciones de varias variables · Derivadas parciales y gradiente · Máximos y mínimos · Multiplicadores de Lagrange · Integrales dobles y triples · Coordenadas curvilíneas |
| `calculo-vec-gen` | Cálculo Vectorial | 31 | Campos · Integrales de línea · Green · Stokes · Divergencia · Integrales de superficie |
| `ec-dif-gen` | Ecuaciones Diferenciales | 42 | EDO primer orden · EDO segundo orden · Transformada de Laplace · Sistemas de ED · Aplicaciones |

> **Nota:** los IDs son los mismos que ya existen en el dashboard de splits (`apps/ops/data/splits/catalog/*.json`). Mantenerlos consistentes en Remy facilita el cruce.

---

## 2. Lógica de split (recordatorio)

1. **Match alto:** el curso base cubre ≥80% del ramo → split directo, sólo agregar 1–3 módulos específicos de la U (notación, código, evaluaciones tipo).
2. **Match medio:** 40–80% cubierto → seleccionar módulos del base + grabar 5–10 módulos nuevos.
3. **Match bajo / ninguno:** <40% → tratar como curso nuevo, no split.
4. **Identificador Remy:** `{universidad}-{carrera}-{ramo-slug}`. Mismo namespace que en `apps/ops/data/splits/universities/`.
5. **Ejes:** los ítems del array `contenidos` de cada ramo. **Cada eje** se mapea a uno o más módulos/lecciones de los cursos base.

---

## 3. Universidades

### 3.1 UAI — Universidad Adolfo Ibáñez (Tier 1)

Malla: 8 carreras con componente matemático. Convalida: Bachilleratos → planes comunes de Ing. Civil / Ing. Comercial.

#### Carreras

| ID | Nombre | Facultad |
|---|---|---|
| `uai-plan-comun` | Ingeniería Civil Plan Común | Fac. Ingeniería y Ciencias |
| `uai-icom-admin` | Ing. Comercial (Lic. Admin. Empresas) | Escuela de Negocios |
| `uai-icom-economia` | Ing. Comercial (Lic. Economía) | Escuela de Negocios |
| `uai-computer-science` | Ing. en Computer Science | Fac. Ingeniería y Ciencias |
| `uai-negocios-tech` | Ing. en Negocios y Tecnología | Negocios + Ingeniería |
| `uai-bachillerato-ic` | Bachillerato de Ing. Civil | Fac. Ingeniería y Ciencias |
| `uai-bachillerato-icom` | Bachillerato de Ing. Comercial | Escuela de Negocios |
| `uai-arq-ici` | Doble Título Arquitectura + Ing. Civil Industrial | Arquitectura + Ingeniería |

#### Ramos

**`uai-plan-comun-algebra` · Álgebra · S1 · sin prereqs**
Ejes:
- Lógica y conjuntos (proposiciones, álgebra de conjuntos, cuantificadores)
- Números reales (axiomas, demostraciones, inducción)
- Números naturales (sucesiones, progresiones, sumatorias polinómica/telescópica/geométrica, productoria, combinatoria, binomio de Newton)
- Trigonometría (funciones, identidades, ecuaciones trigonométricas)
- Geometría analítica (vectores, producto punto/cruz, rectas, planos, distancias en el espacio)
- Números complejos (operaciones, forma polar, raíces)
- Polinomios (división sintética, raíces, teorema del resto, fracciones parciales)

Base: `precalculo-cero` + `nivelacion-ing` · match **alto**.

**`uai-plan-comun-calculo-diferencial` · Cálculo Diferencial · S1**
Ejes:
- Números reales e inecuaciones
- Funciones: dominio, recorrido, transformaciones, inyectivas, inversas, polinomiales, exponenciales, logarítmicas
- Límites (finitos, al infinito, continuidad, TVI)
- Derivadas: definición, reglas, derivadas implícitas
- Aplicaciones: razón de cambio, máx/mín, TVM, L'Hôpital, graficación

Base: `calculo-1var-gen` o `calculo-dif-gen` · **alto**.

**`uai-plan-comun-calculo-integral` · Cálculo Integral · S2 · prereq Cálc Diferencial**
Ejes:
- Antiderivadas, integral indefinida, TFC, sustitución, partes, fracciones parciales, sustitución trigonométrica
- Aplicaciones: área entre curvas, volúmenes (discos, cascarones), curvas parametrizadas, polares
- Integrales impropias (tipo I y II, comparación)
- Sucesiones y series (criterios, series de potencias, radio/intervalo, Taylor)

Base: `calculo-1var-gen` o `calculo-int-gen` · **alto**.

**`uai-plan-comun-algebra-lineal` · Álgebra Lineal · S2 · prereq Álgebra**
Ejes:
- Matrices y sistemas (Gauss-Jordan, homogéneos, por bloques, inversa, elementales)
- Determinantes
- Espacios y subespacios vectoriales (combinación e independencia lineal, bases, dimensión, coordenadas, cambio de base, subespacios fundamentales)
- Transformaciones lineales (kernel, imagen, inyec/sobre, matriz asociada)
- Diagonalización (valores/vectores propios, cadenas de Markov)
- Análisis vectorial (Gram-Schmidt, complemento/proyección ortogonal, mínimos cuadrados)

Base: `algebra-lineal-gen` · **alto** (match directo y completo).

**`uai-plan-comun-calculo-multivariables` · Cálculo Multivariables · S3 · prereqs Cálc Integral + Álgebra Lineal**
Ejes:
- Funciones de varias variables (superficies cuadráticas, límites, continuidad, derivadas parciales, diferenciabilidad)
- Plano tangente, aproximaciones lineales, regla de la cadena, derivación implícita
- Derivadas direccionales, máx/mín, Lagrange
- Integrales dobles (cambio de región, polares, masa y centro de masa)
- Integrales triples (cilíndricas, esféricas, cambios de variable)
- Cálculo vectorial (integrales de línea, Green, rotacional, divergencia, integrales de superficie, Stokes, teorema de la divergencia)

Base: `calculo-vvar-gen` + `calculo-vec-gen` · **alto**.

**`uai-plan-comun-ecuaciones-diferenciales` · Ecuaciones Diferenciales · S4 · prereq Cálc Multivariables**
Ejes:
- EDO 1er orden (separable, lineal, exacta, factor integrante, homogénea, Bernoulli, Ricatti, reducible)
- Modelos con ED 1er orden
- ED orden superior (coeficientes constantes, Cauchy-Euler, coef. indeterminados, variación de parámetros, masa-resorte)
- Sistemas de ED
- Transformada de Laplace (propiedades, traslación, escalón, convolución, Delta de Dirac)
- Soluciones por series (puntos ordinarios, singulares regulares, Bessel)
- Serie de Fourier

Base: `ec-dif-gen` · **alto** (curso UAI más extenso: series Fourier + Bessel — material complementario).

**`uai-icom-admin-matematicas-avanzadas-i` / `uai-icom-economia-matematicas-avanzadas-i` · Mat. Avanzadas I · S1**
*(programa compartido entre Admin y Economía, también convalida con Bachillerato Ing. Comercial)*

Ejes:
- Lógica y conjuntos · Números naturales y reales (inducción, sucesiones, progresiones, sumatorias)
- Axiomas de orden, demostraciones, inecuaciones (con valor absoluto), axioma del supremo
- Funciones (dominio, imagen, composición, inversas, log/exp, gráficos, modelación)
- Matrices y sistemas (Gauss-Jordan, homogéneos, por bloques, inversa, elementales)
- Determinantes
- Espacios vectoriales, subespacios, combinación y dependencia lineal

Base: `precalculo-cero` + `algebra-lineal-gen` · **alto**.

**`uai-icom-admin-matematicas-avanzadas-ii` / `uai-icom-economia-matematicas-avanzadas-ii` · Mat. Avanzadas II · S2 · prereq Mat. Avanzadas I**
Ejes:
- Sistemas de ecuaciones lineales (repaso)
- Límites (normales, trigonométricos, al infinito, laterales, continuidad, teoremas)
- Derivadas (definición, reglas, recta tangente, análisis marginal, derivación implícita)
- Aplicaciones de derivadas (extremos, crecimiento, optimización, L'Hôpital)
- Integrales (sustitución, partes, Riemann, TFC)
- Aplicaciones integrales (área entre curvas, excedentes, impropias, criterios de convergencia)
- Funciones de probabilidad

Base: `calculo-1var-gen` · **alto** (no incluye multivariable — verificado).

**`uai-computer-science-algebra` · Álgebra · S1** — mismo programa que Plan Común Ing. Civil. Base: `precalculo-cero` + `nivelacion-ing`.

**`uai-computer-science-calculo-diferencial` · Cálculo Diferencial · S1** — mismo programa que Plan Común. Base: `calculo-1var-gen` o `calculo-dif-gen`.

**`uai-computer-science-algebra-lineal` · Álgebra Lineal · S2** — mismo programa. Base: `algebra-lineal-gen`.

**`uai-computer-science-calculo-integral` · Cálculo Integral · S2** — mismo programa. Base: `calculo-1var-gen` o `calculo-int-gen`.

**`uai-negocios-tech-algebra-lineal-y-optimizacion` · Álgebra Lineal y Optimización · S1**
Ejes:
- Matrices y sistemas lineales
- Espacios vectoriales básicos
- Introducción a optimización lineal
- Aplicaciones a negocios

Base: `algebra-lineal-gen` · **medio** (componente de optimización es específico).

**`uai-bachillerato-ic-introduccion-al-algebra` · Intro al Álgebra · S1**
Ejes: razonamiento lógico-matemático · conjuntos y números · ecuaciones e inecuaciones básicas · funciones elementales. Base: `precalculo-cero` · **alto**.

**`uai-bachillerato-ic-introduccion-al-calculo` · Intro al Cálculo · S1**
Ejes: funciones y sus gráficas · concepto intuitivo de límite · introducción a la derivada · pendiente y razón de cambio. Base: `precalculo-cero` + `calculo-1var-gen` · **alto**.

**`uai-bachillerato-ic-algebra` · Álgebra · S2** — convalida con Álgebra Plan Común. Base: `precalculo-cero` + `nivelacion-ing`.

**`uai-bachillerato-ic-calculo-diferencial` · Cálculo Diferencial · S2** — convalida con Cálc Diferencial Plan Común. Base: `calculo-1var-gen` o `calculo-dif-gen`.

**`uai-bachillerato-icom-introduccion-al-calculo` / `-introduccion-al-algebra` · S1** — versión introductoria. Base: `precalculo-cero` · **alto**.

**`uai-bachillerato-icom-matematicas-avanzadas-i` · Mat. Avanzadas I · S2** — convalida con MM I del plan común Ing. Comercial. Base: `precalculo-cero` + `algebra-lineal-gen`.

**`uai-arq-ici-algebra` / `-algebra-lineal` / `-ecuaciones-diferenciales`** — mismos programas que Plan Común Ing. Civil. Bases: `precalculo-cero`+`nivelacion-ing` / `algebra-lineal-gen` / `ec-dif-gen` respectivamente.

---

### 3.2 UANDES — Universidad de los Andes (Tier 1)

#### Carreras

| ID | Nombre |
|---|---|
| `uandes-plan-comun-ing` | Ing. Civil Plan Común |
| `uandes-ing-civil-industrial` / `-obras` / `-computacion` / `-electrica` | Especialidades Civil |
| `uandes-ing-civil-quimica` | Ing. Civil Química (malla propia, nueva 2026) |
| `uandes-ing-comercial` | Ingeniería Comercial |
| `uandes-international-business` | International Business (bilingüe) |
| `uandes-bachillerato-ing` / `-icom` | Bachilleratos |

#### Ramos

**`uandes-plan-comun-ing-algebra-e-introduccion-al-calculo` · Álgebra e Introducción al Cálculo · S1**
Ejes:
- Conjuntos y números reales (axiomas, desigualdades, valor absoluto)
- Polinomios (operaciones, división sintética, raíces)
- Funciones reales de variable real (lineal, cuadrática, potencia, exp, log)
- Trigonometría (razones, identidades, teorema del seno y coseno)
- Números complejos (binomial, polar)
- Introducción a límites y continuidad

Base: `precalculo-cero` + `nivelacion-ing` · **alto**.

**`uandes-plan-comun-ing-calculo-i` · Cálculo I · S2**
Ejes:
- Límites (definición formal, propiedades, laterales, al infinito)
- Continuidad
- Derivadas (definición, reglas, cadena)
- Derivación implícita y logarítmica
- Aplicaciones (máx/mín, concavidad, L'Hôpital)
- Análisis y graficación
- Introducción a la integral

Base: `calculo-1var-gen` o `calculo-dif-gen` · **alto**.

**`uandes-plan-comun-ing-algebra-lineal` · Álgebra Lineal · S2**
Ejes: Matrices y sistemas (Gauss, Gauss-Jordan) · Determinantes · Espacios vectoriales (subespacio, independencia, base, dimensión) · Transformaciones lineales (núcleo, imagen) · Producto interior, Gram-Schmidt · Valores y vectores propios, diagonalización.

Base: `algebra-lineal-gen` · **alto**.

**`uandes-plan-comun-ing-calculo-ii` · Cálculo II · S3**
Ejes:
- Antiderivadas e integral indefinida
- Técnicas de integración (sustitución, partes, fracciones parciales, trigonométricas)
- Integral definida y TFC
- Aplicaciones (áreas, volúmenes, longitud de arco)
- Integrales impropias
- Funciones de varias variables, introducción a derivadas parciales
- Integrales dobles y triples

Base: `calculo-1var-gen` + `calculo-int-gen` + `calculo-vvar-gen` · **alto** (curso mezcla 1 y varias variables).

**`uandes-plan-comun-ing-ecuaciones-diferenciales` · Ecuaciones Diferenciales · S3**
Ejes: EDO 1er orden (separables, lineales, exactas, Bernoulli) · EDO 2do orden (coef. constantes, variación de parámetros) · Laplace (definición, propiedades, inversión) · Sistemas de ED · Aplicaciones a ingeniería (circuitos, resortes, mezcla).

Base: `ec-dif-gen` · **alto**.

**`uandes-ing-civil-obras-optimizacion` · Optimización · S5**
Ejes: programación lineal, simplex, dualidad, programación entera. Base: ninguno · **descartar como split**, curso nuevo.

**Ing. Civil Química (nueva malla 2026):**
- `uandes-ing-civil-quimica-introduccion-al-algebra-y-geometria` · S1 → Base: `precalculo-cero` · alto.
- `uandes-ing-civil-quimica-introduccion-al-calculo` · S1 → Base: `precalculo-cero` + `calculo-1var-gen` · alto.
- `uandes-ing-civil-quimica-calculo-i` · S2 (derivadas + integrales + técnicas + aplicaciones) → Base: `calculo-1var-gen` · alto.
- `uandes-ing-civil-quimica-algebra-lineal` · S2 → Base: `algebra-lineal-gen` · alto.
- `uandes-ing-civil-quimica-calculo-ii` · S3 (varias variables + coordenadas curvilíneas) → Base: `calculo-vvar-gen` + `calculo-vec-gen` · alto.
- `uandes-ing-civil-quimica-ecuaciones-diferenciales` · S3 → Base: `ec-dif-gen` · alto.

**`uandes-ing-comercial-algebra` · Álgebra · S1**
Ejes: Conjuntos y lógica · Números reales (desigualdades, valor absoluto) · Polinomios (raíces, fracciones parciales) · Álgebra finita (sumatorias, progresiones, factorial, binomio) · Matrices y determinantes · Sistemas lineales. Base: `precalculo-cero` · **alto**.

**`uandes-ing-comercial-calculo-i` · Cálculo I · S2**
Ejes: Funciones reales · Límites y continuidad · Derivadas (concepto, reglas, orden superior, implícita) · Aplicaciones (L'Hôpital, máx/mín, concavidad) · Intro a varias variables. Base: `calculo-1var-gen` o `calculo-dif-gen` · **alto**.

**`uandes-ing-comercial-optimizacion` · Optimización · S3**
Ejes: Optimización de funciones de una y varias variables · Lagrange · Programación lineal (formulación, gráfica) · Simplex · Intro a programación entera. Base: `calculo-vvar-gen` · **medio** (PL/simplex específico).

**`uandes-international-business-algebra-critical-thinking` · S1** — pensamiento analítico + álgebra aplicada a negocios + funciones básicas. Base: `precalculo-cero` · **medio**.

**`uandes-international-business-calculo-quantitative-methods` · S2** — cálculo diferencial aplicado + optimización + intro varias variables. Base: `calculo-1var-gen` o `calculo-dif-gen` · **medio**.

**`uandes-bachillerato-ing-nivelacion-matematica` · S1** — razonamiento lógico + álgebra básica + funciones (preparación a Álgebra e Intro al Cálculo). Base: `precalculo-cero` + `nivelacion-ing` · **alto**.

**`uandes-bachillerato-icom-nivelacion-matematica` · S1** — preparación a Álgebra Ing. Comercial. Base: `precalculo-cero` · **alto**.

---

### 3.3 UCH — Universidad de Chile (Tier 1)

Plan Común FCFM (710 vacantes, cubre todas las ingenierías civiles + ciencias) + carreras FEN + Lic. Matemática / Física + Pedagogía.

#### Carreras

| ID | Nombre |
|---|---|
| `uch-plan-comun-fcfm` | Plan Común Ingeniería y Ciencias (FCFM) |
| `uch-ing-civil-industrial` | Ing. Civil Industrial post Plan Común |
| `uch-icom-fen` | Ingeniería Comercial (FEN) |
| `uch-iicg-fen` | Ing. en Información y Control de Gestión |
| `uch-contador-fen` | Contador Auditor |
| `uch-lic-matematica` | Lic. Ciencias mención Matemática |
| `uch-lic-fisica` | Lic. Ciencias mención Física |
| `uch-pedagogia-mat-fis` | Pedagogía en Ed. Media Matemáticas y Física |

#### Ramos — Plan Común FCFM (rigurosos, más teóricos que el promedio)

**`uch-plan-comun-fcfm-ma1001-introduccion-al-calculo` · MA1001 Intro al Cálculo · S1**
Ejes:
- Números reales (igualdad, orden, valor absoluto, inecuaciones lineales/cuadráticas, factorización) — 1 sem
- Geometría analítica (cartesiano, rectas, circunferencias, parábolas, elipses, hipérbolas, excentricidad) — 2 sem
- Funciones de una variable (definición, dominio, paridad, crecimiento, composición, inyectividad, inversas) — 1 sem
- Trigonometría (funciones, identidades, ecuaciones) — 1 sem
- Límites (de sucesiones, de funciones, asíntotas) — 2 sem
- Derivadas (definición, reglas básicas — introducción) — 1 sem

Base: `precalculo-cero` + `nivelacion-ing` · **alto** (introduce límites/derivadas rigurosamente al final).

**`uch-plan-comun-fcfm-ma1101-introduccion-al-algebra` · MA1101 Intro al Álgebra · S1**
Ejes:
- Conjuntos (potencia, particiones, álgebra, cuantificadores)
- Funciones (definición formal, composición)
- Relaciones (propiedades, conjunto cociente, división entera)
- Relaciones de orden
- Axiomas de cuerpos (campos), campos ordenados
- Números reales (axioma del supremo, completitud)
- Conjuntos finitos e infinitos, cardinalidad
- Números complejos (operaciones, polar, raíces)

Base: `precalculo-cero` · **medio** (~50%, falta rigor axiomático). **Material complementario obligatorio** sobre demostraciones, relaciones y cardinalidad.

**`uch-plan-comun-fcfm-ma1002-calculo-diferencial-e-integral` · MA1002 · S2 · prereq MA1001**
Ejes:
- Continuidad (subsucesiones, convergencia, discontinuidades, álgebra, TVI, Weierstrass, continuidad uniforme) — 2 sem
- Derivadas (diferenciabilidad formal, reglas, derivada de la inversa, teoremas del valor medio) — 2 sem
- Aplicaciones (máx/mín, análisis, L'Hôpital, Taylor orden 1) — 2 sem
- Integrales (primitivas, TFC 1° y 2°, sustitución, partes, fracciones parciales, sust. trigonométrica) — 2 sem
- Aplicaciones de la integral (áreas, volúmenes de revolución, centros de masa) — 1 sem
- Series de potencias (derivadas e integrales de funciones no elementales) — 1 sem
- Curvas en el espacio (longitud, curvatura, torsión) — 1 sem

Base: `calculo-1var-gen` (+ `calculo-dif-gen`, `calculo-int-gen`) · **alto**.

**`uch-plan-comun-fcfm-ma1102-algebra-lineal` · MA1102 · S2 · prereqs MA1101 + MA1001**
Ejes:
- Matrices y sistemas (operaciones, particulares/elementales/triangulares, escalonamiento, Gauss, inversa, factorización LU) — 3 sem
- Espacios vectoriales (subespacios, independencia, generadores, base, dimensión, suma directa) — 3 sem
- Geometría lineal en Rⁿ (vectores, rectas, planos, paramétricas/cartesianas, producto interno, norma, producto cruz, proyecciones ortogonales) — 2 sem
- Transformaciones lineales (núcleo, imagen, teorema núcleo-imagen, matriz representante, rango, cambio de base) — 2.5 sem
- Valores y vectores propios (determinante, polinomio característico, diagonalización) — 2 sem
- Ortogonalidad (Gram-Schmidt, matrices simétricas, formas cuadráticas, cónicas, mínimos cuadrados, Jacobiana) — 2.5 sem

Base: `algebra-lineal-gen` · **alto** (match directo y completo, +LU factorization como extra).

**`uch-plan-comun-fcfm-ma2001-calculo-en-varias-variables` · MA2001 · S3 · prereqs MA1002 + MA1102**
Ejes:
- Topología en Rⁿ (distancias, normas, bolas, sucesiones, abiertos/cerrados/compactos) — 1.5 sem
- Funciones de varias variables (grafos, conjuntos de nivel, límites, continuidad) — 1 sem
- Cálculo diferencial en Rⁿ (direccionales, parciales, Fréchet, Jacobiana, regla de la cadena, gradiente, plano tangente) — 2 sem
- Teoremas función inversa e implícita, punto fijo — 1.5 sem
- Derivadas de orden superior (Schwartz, Hessiana, Taylor multivariable) — 1 sem
- Máx/mín (puntos críticos, 2do orden, convexas, Lagrange) — 1.5 sem
- Integral de Riemann en Rⁿ (particiones, propiedades) — 2 sem
- Fubini, cambio de variables (iteradas, polares, cilíndricas, esféricas, centros de masa, momentos de inercia) — 3 sem

Base: `calculo-vvar-gen` · **alto** (curso UCh agrega topología formal + función inversa/implícita).

**`uch-plan-comun-fcfm-ma2601-ecuaciones-diferenciales-ordinarias` · MA2601 · S3 · prereqs MA1002 + MA1102**
Ejes:
- EDO 1er orden (campo vectorial, curva integral, separables, reducción de orden, homogéneas, lineales con factor integrante, Bernoulli, Ricatti, modelación, existencia y unicidad, Runge-Kutta) — 3 sem
- Ecuaciones lineales de orden superior (Wronskiano, orden 2 homogéneas/vibraciones mecánicas, variación de parámetros, Función de Green, condiciones de borde, series de potencias / Frobenius, orden n homogéneas/no homogéneas, Euler-Cauchy, coef. indeterminados) — 4 sem
- Transformada de Laplace (definición, fórmulas, ED lineales, convolución, Heaviside, Delta de Dirac) — 2 sem
- Sistemas lineales (existencia/unicidad, matriz fundamental, exponencial, asintótico, diagramas de fase 2×2, variación de parámetros) — 3 sem
- Sistemas autónomos no lineales (hamiltonianos, conservación de energía, péndulo no lineal, estabilidad puntos críticos, Lotka-Volterra, Lyapunov) — 3 sem

Base: `ec-dif-gen` · **alto** (~75%). **Material complementario** sobre sistemas no lineales, Lyapunov, diagramas de fase, Runge-Kutta.

**`uch-plan-comun-fcfm-ma2002-calculo-avanzado-y-aplicaciones` · MA2002 · S4 · prereqs MA2601 + MA2001**
Ejes:
- Cálculo vectorial (campos escalares/vectoriales, gradiente, sistemas coordenados ortogonales, divergencia, rotor, Laplaciano, integrales de línea y superficie) — 1.5 sem
- Teoremas de integración vectorial (Gauss, Green, Stokes, conservativos, circulaciones, flujos) — 3 sem
- Variable compleja (derivada compleja, Cauchy-Riemann, series de potencias, Laurent, polos, residuos, integrales complejas) — 3 sem
- Series y Transformada de Fourier (funciones periódicas, coeficientes, convergencia, transformada, convolución, pares/impares) — 2 sem

Base: `calculo-vec-gen` · **medio** (~40%, variable compleja y Fourier NO están en catálogo Se Remonta — material extenso a grabar).

#### Ramos — FEN (Ing. Comercial, IICG, Contador Auditor — MM I a IV)

**`uch-icom-fen-metodos-matematicos-i` / `uch-iicg-fen-metodos-matematicos-i` / `uch-contador-fen-metodos-matematicos-i` · MM I · S1** (mismo programa)
Ejes: Lógica y proposiciones (lógica proposicional, álgebra de proposiciones) · Conjuntos (operaciones) · Inecuaciones y valor absoluto · Geometría analítica (casos aplicados) · Funciones (definiciones, composición, inversas) · Sumatorias (definiciones, inducción, fracciones parciales, combinatoria) · Límites (introducción) · Derivadas (definición, álgebra, funciones elementales).

Base: `precalculo-cero` · **alto** (match directo).

**`uch-icom-fen-metodos-matematicos-ii` / IICG / Contador · MM II · S2 · prereq MM I**
Ejes: Funciones multivariadas y derivadas · Métodos de derivación con restricciones · Álgebra lineal (matrices y operaciones) · Metodologías aplicadas.

Base: `calculo-dif-gen` + `algebra-lineal-gen` · **medio** (curso híbrido, mezcla ambos temas en uno).

**`uch-icom-fen-metodos-matematicos-iii` / IICG / Contador · MM III · S3 · prereq MM II**
Ejes: Derivadas y aplicaciones · Optimización con y sin restricciones · Programación lineal (PPL) · Método simplex.

Base: `calculo-1var-gen` · **medio** (PPL/simplex no cubierto).

**`uch-iicg-fen-metodos-matematicos-iv` · MM IV · S4**
Ejes: métodos cuantitativos avanzados · integrales y aplicaciones · modelos matemáticos para gestión.

Base: `calculo-1var-gen` + `calculo-int-gen` · **medio**.

#### Ramos — Lic. Matemática / Física / Pedagogía Mat-Fís

(Los tres comparten estructura. Sólo se listan los IDs y la base sugerida.)

| Ramo | Ejes | Base | Match |
|---|---|---|---|
| `uch-lic-matematica-calculo-i` / `uch-lic-fisica-calculo-i` / `uch-pedagogia-mat-fis-calculo-i` | Números reales · funciones · límites · continuidad · derivadas · aplicaciones | `precalculo-cero` + `calculo-dif-gen` | alto |
| `uch-lic-matematica-algebra-i` / `uch-lic-fisica-algebra-i` / `uch-pedagogia-mat-fis-algebra-i` | Lógica · conjuntos · relaciones · funciones · números (naturales, enteros, racionales, reales, complejos) | `precalculo-cero` | medio (teórico) |
| `uch-lic-matematica-calculo-ii` / `uch-lic-fisica-calculo-ii` / `uch-pedagogia-mat-fis-calculo-ii` | Integrales · técnicas · series · aplicaciones | `calculo-1var-gen` o `calculo-int-gen` | alto |
| `uch-lic-matematica-algebra-lineal` / `uch-lic-fisica-algebra-lineal` / `uch-pedagogia-mat-fis-algebra-lineal` | Matrices · sistemas · espacios vectoriales · transformaciones lineales · valores propios | `algebra-lineal-gen` | alto |
| `uch-lic-matematica-calculo-iii-varias-variables` / `uch-lic-fisica-calculo-iii` | Funciones de varias variables · derivadas parciales · integrales múltiples · Lagrange | `calculo-vvar-gen` | alto |
| `uch-lic-matematica-ecuaciones-diferenciales` / `uch-lic-fisica-ecuaciones-diferenciales` | EDO · métodos de resolución · Laplace · sistemas | `ec-dif-gen` | alto |

---

### 3.4 UDD — Universidad del Desarrollo (Tier 2)

#### Carreras

| ID | Nombre |
|---|---|
| `udd-plan-comun` | Ing. Civil Plan Común (4 sem comunes + especialidad) |
| `udd-ing-comercial` | Ingeniería Comercial |
| `udd-geologia` | Geología |
| `udd-gba` | Global Business Administration |
| `udd-ncd` | Negocios y Ciencia de Datos (nueva 2026, doble título con Ing. Comercial) |
| `udd-biomedicina` | Ing. Civil en BioMedicina (nueva 2025) |
| `udd-quimica-farmacia` | Química y Farmacia (nueva 2025) |
| `udd-bachillerato-ic` | Bachillerato en Ing. Comercial |
| `udd-arquitectura` | Arquitectura |
| `udd-medicina` | Medicina |

#### Ramos

**`udd-plan-comun-algebra` · Álgebra · S1**
Ejes: Conjuntos y lógica · Números reales (axiomas, desigualdades, valor absoluto) · Polinomios (operaciones, división sintética, raíces) · Álgebra finita (sumatorias, progresiones, factorial, binomio) · Matrices y determinantes · Sistemas de ecuaciones lineales (Gauss-Jordan).
Base: `precalculo-cero` + `nivelacion-ing` · **alto**.

**`udd-plan-comun-introduccion-al-calculo` · Intro al Cálculo · S1**
Ejes: Funciones reales · función lineal/cuadrática/potencia/exp/log · trigonométricas · límites (def, propiedades, laterales) · continuidad · introducción a derivada.
Base: `precalculo-cero` + `calculo-1var-gen` · **alto**.

**`udd-plan-comun-geometria` · Geometría · S2 · prereq Álgebra**
Ejes: Geometría analítica plana (rectas, circunferencias, cónicas) · Vectores en R² y R³ · Rectas y planos en el espacio · Números complejos (binomial, polar, exponencial) · Trigonometría avanzada.
Base: `precalculo-cero` · **medio** (faltan complejos avanzados y vectores 3D).

**`udd-plan-comun-calculo-diferencial` · Cálculo Diferencial · S2 · prereq Intro Cálculo**
Ejes: Derivadas (def, reglas) · implícita y logarítmica · TVM, Rolle, L'Hôpital · aplicaciones (máx/mín, concavidad, inflexión) · análisis y graficación · diferenciales y aproximaciones.
Base: `calculo-1var-gen` o `calculo-dif-gen` · **alto** (ya existe curso UDD Cálculo Diferencial Ing. Civil con 58 mód).

**`udd-plan-comun-algebra-lineal` · Álgebra Lineal · S3 · prereq Álgebra**
Ejes: Matrices y sistemas (Gauss, Cramer) · Planos y rectas (variedades lineales R², R³) · Espacios vectoriales (subespacio, indep. lineal, base, dimensión) · Producto interior, Gram-Schmidt · Transformaciones lineales (núcleo, imagen, teorema de dimensión) · Valores/vectores propios, diagonalización.
Base: `algebra-lineal-gen` · **alto**.

**`udd-plan-comun-calculo-integral` · Cálculo Integral · S3 · prereq Cálc Diferencial**
Ejes: Antiderivadas e integral indefinida · Técnicas (sustitución, partes, fracciones parciales, trigonométricas) · Integral definida y TFC · Aplicaciones (áreas, volúmenes, longitud) · Integrales impropias · Sucesiones y series numéricas.
Base: `calculo-1var-gen` o `calculo-int-gen` · **alto** (ya existe curso UDD Cálculo Integral Ing. Civil con 37 mód).

**`udd-plan-comun-calculo-multivariable` · Cálculo Multivariable · S4 · prereqs Cálc Integral + Álgebra Lineal**
Ejes: Funciones de varias variables · derivadas parciales, gradiente, direccionales · máx/mín · Lagrange · integrales dobles y triples · cambio de coordenadas (polares, cilíndricas, esféricas).
Base: `calculo-vvar-gen` + `calculo-vec-gen` · **alto**.

**`udd-plan-comun-ecuaciones-diferenciales` · Ecuaciones Diferenciales · S4 · prereq Cálc Integral**
Ejes: EDO 1er orden (separables, lineales, exactas, Bernoulli) · EDO 2do orden (coef. constantes, variación de parámetros) · Laplace · Sistemas · Aplicaciones.
Base: `ec-dif-gen` · **alto**.

**`udd-ing-comercial-algebra` · Álgebra · S1**
Ejes: Conjuntos (Venn, cardinalidad) · Álgebra en reales (desigualdades, inecuaciones, valor absoluto) · Polinomios (división sintética, raíces, fracciones parciales) · Álgebra finita (sumatorias, progresiones, factorial, combinatorio, binomio) · Matrices y determinantes · Sistemas lineales.
Base: `precalculo-cero` · **alto**.

**`udd-ing-comercial-calculo` · Cálculo · S2 · prereq Álgebra**
Ejes: Relaciones y funciones reales · límites y continuidad · derivadas (concepto, reglas, orden superior, implícita, diferenciales) · aplicaciones (L'Hôpital, máx/mín, concavidad) · funciones de varias variables (parciales, Cobb-Douglas, Hessiano, Lagrange).
Base: `calculo-1var-gen` + `calculo-vvar-gen` · **alto** (ya existen Cálculo I UDD Ing. Comercial 47 mód y Cálculo II UDD Ing. Comercial 33 mód).

**`udd-ing-comercial-probabilidades-e-inferencia` · S3** y **`udd-ing-comercial-metodos-estadisticos` · S4** — Base: ninguno (estadística fuera del catálogo Remy actual). Marcar como **no aplica**.

**Geología** (mismas mallas mat. que Plan Común Ing. Civil):
- `udd-geologia-algebra` → como Plan Común. Base: `precalculo-cero`+`nivelacion-ing`.
- `udd-geologia-introduccion-al-calculo` → idem. Base: `precalculo-cero` + `calculo-1var-gen`.
- `udd-geologia-geometria` · S2 → idem. Base: `precalculo-cero` · medio.
- `udd-geologia-calculo-diferencial` · S2 → idem. Base: `calculo-1var-gen` o `calculo-dif-gen`.
- `udd-geologia-calculo-integral` · S3 → idem. Base: `calculo-1var-gen` o `calculo-int-gen`.
- `udd-geologia-ecuaciones-diferenciales` · S5 → idem. Base: `ec-dif-gen`.
- `udd-geologia-probabilidades-y-estadistica` · S4 → **no aplica** (estadística).

**Global Business Administration** (mismo programa que Ing. Comercial):
- `udd-gba-algebra` · S1 → Base: `precalculo-cero` · alto.
- `udd-gba-calculo` · S2 → Base: `calculo-1var-gen` · alto.

**Negocios y Ciencia de Datos:**
- `udd-ncd-matematica-avanzada` · S1 → Álgebra y funciones para datos + cálculo aplicado + álgebra lineal básica. Base: `precalculo-cero` + `calculo-1var-gen` + `algebra-lineal-gen` · **medio** (requiere selección).
- `udd-ncd-probabilidades-e-inferencia` y `-metodos-estadisticos` → **no aplica** (estadística).

**Ing. Civil en BioMedicina (Matemática Aplicada I–IV):**
- I (S1) — fundamentos · funciones. Base: `precalculo-cero` · medio.
- II (S2) — cálculo diferencial aplicado a biomedicina. Base: `calculo-1var-gen` o `calculo-dif-gen` · medio.
- III (S3) — cálculo integral + álgebra lineal aplicada. Base: `calculo-1var-gen` + `calculo-int-gen` + `algebra-lineal-gen` · medio.
- IV (S4) — ED y métodos numéricos aplicados. Base: `ec-dif-gen` + `calculo-vvar-gen` · medio.

**Química y Farmacia:**
- `udd-quimica-farmacia-matematicas` · S1 → Álgebra, funciones, ecuaciones, trigonometría básica. Base: `precalculo-cero` · medio.
- `udd-quimica-farmacia-calculo` · S2 → Límites, derivadas, integrales aplicadas. Base: `calculo-1var-gen` o `calculo-dif-gen` · medio.

**Bachillerato Ing. Comercial:**
- `udd-bachillerato-ic-pensamiento-matematico` · S1 → razonamiento. Base: `precalculo-cero` · bajo.
- `udd-bachillerato-ic-algebra` · S2 → mismo que Álgebra Ing. Comercial. Base: `precalculo-cero` · alto.

**Arquitectura:**
- `udd-arquitectura-componentes-de-la-matematica` · S1 → geometría, proporciones, cálculo básico aplicado. Base: `precalculo-cero` · bajo (curso muy específico).

---

### 3.5 UTFSM — Universidad Técnica Federico Santa María (Tier 2)

#### Carreras

| ID | Nombre |
|---|---|
| `utfsm-plan-comun-ing-civil` | Plan Común Ingeniería Civil (Casa Central + San Joaquín) |
| `utfsm-ing-comercial` | Ingeniería Comercial (San Joaquín, usa MATE25/MATE26) |
| `utfsm-ing-civil-matematica` | Ing. Civil Matemática (post Plan Común — Casa Central) |

#### Ramos — Plan Común Ing. Civil

**`utfsm-plan-comun-ing-civil-mate10-algebra-y-geometria` · MATE10 · S1**
Ejes:
- Fundamentos del Lenguaje Matemático (lógica, conjuntos, álgebra de reales — potencias, raíces, productos notables, ecuaciones; geometría escolar — Pitágoras, Thales, Herón, áreas, volúmenes)
- Trigonometría del triángulo (ángulos, razones, identidades, teoremas seno/coseno, modelación)
- Geometría Analítica (cartesiano, recta, cónicas centradas y trasladadas — circunferencia, parábola, elipse, hipérbola)
- Polinomios (números complejos en formas, álgebra de polinomios, división de Euclides, sintética, raíces, multiplicidad, teoremas del resto y del factor)
- Inducción Matemática (principio, sumatoria, factorial, progresiones aritméticas y geométricas, binomio, combinatoria)

Base: `precalculo-cero` · **alto** (~85%). Material complementario: inducción matemática y geometría escolar formal. Texto guía: Zill, Dewar & Watson — Álgebra y Trigonometría (McGraw-Hill).

**`utfsm-plan-comun-ing-civil-mat070-introduccion-al-calculo` · MAT070 · S1**
Ejes:
- Funciones reales (dominio, recorrido, paridad, composición, inyectividad, sobreyectividad, inversas)
- Funciones elementales (polinomiales, racionales, trigonométricas, exp, log)
- Límites (ε-δ, álgebra, laterales, al infinito, asíntotas)
- Continuidad (tipos de discontinuidad, propiedades, TVI)
- Derivada (definición como límite, interpretación geométrica, reglas, funciones elementales, regla de la cadena)
- Aplicaciones (recta tangente, máx/mín locales, crecimiento, concavidad, análisis introductorio)

Base: `precalculo-cero` + `nivelacion-ing` + `calculo-dif-gen` · **alto** (~80%).

**`utfsm-plan-comun-ing-civil-calculo-en-una-variable` · S2 · prereq MAT070**
Ejes:
- Derivadas (profundización, implícita, orden superior)
- Aplicaciones (TVM, L'Hôpital, análisis completo, optimización, aproximación lineal, Taylor)
- Integrales (Riemann, TFC 1° y 2°, primitivas)
- Técnicas de integración (sustitución, partes, fracciones parciales, sust. trigonométrica)
- Aplicaciones de la integral (áreas, volúmenes — discos, arandelas, capas; longitud, centros de masa)
- Integrales impropias (convergencia, comparación)

Base: `calculo-1var-gen` (+ `calculo-dif-gen` + `calculo-int-gen`) · **alto** (~90%).

**`utfsm-plan-comun-ing-civil-mate20-algebra-lineal` · MATE20 · S2 · prereq MATE10**
Ejes:
- Matrices y sistemas (nxm, tipos, álgebra, transpuesta, elementales, rango, escalonamiento, inversa, determinantes nxn, adjunta, Cramer)
- Geometría Vectorial (vectores plano/espacio, producto punto/cruz, proyecciones, rectas y planos)
- Espacios Vectoriales (estructura, subespacios, espacio generado, independencia, base, dimensión, producto interior, ortogonalidad, Gram-Schmidt, bases ortonormales)
- Transformaciones Lineales (núcleo, imagen, matriz asociada)
- Valores y Vectores Propios (operadores, diagonalización, formas lineales/bilineales/cuadráticas)

Base: `algebra-lineal-gen` · **alto** (~95%). Texto guía: Poole — Álgebra Lineal (Cengage, 4ª ed.).

**`utfsm-plan-comun-ing-civil-calculo-en-varias-variables` · S3 · prereqs Cálc 1V + MATE20**
Ejes:
- Topología en Rⁿ (distancias, normas, abiertos/cerrados — nociones básicas)
- Funciones de varias variables (gráficas, conjuntos de nivel, límites, continuidad)
- Cálculo diferencial en Rⁿ (parciales, direccionales, gradiente, plano tangente, regla de la cadena)
- Máximos y mínimos (puntos críticos, Hessiana, Lagrange)
- Integrales múltiples (dobles, triples, Fubini, cambio de variables)
- Coordenadas curvilíneas (polares, cilíndricas, esféricas, Jacobiano, centros de masa, momentos)

Base: `calculo-vvar-gen` · **alto** (~85%).

**`utfsm-plan-comun-ing-civil-ecuaciones-diferenciales-edo-edp` · S3**
Ejes:
- EDO 1er orden (separables, lineales, exactas, factor integrante, Bernoulli, existencia y unicidad, modelación)
- EDO lineales orden superior (homogéneas/no homogéneas, Wronskiano, coef. constantes, indeterminados, variación de parámetros, Euler-Cauchy)
- Transformada de Laplace (definición, propiedades, tabla, ED lineales, Heaviside, Delta, convolución)
- Sistemas de ED (lineales, matriz fundamental, métodos)
- Introducción a EDP (calor, onda, Laplace, separación de variables, series de Fourier — intro)

Base: `ec-dif-gen` · **alto** (EDO ~85%, total ~70% por EDP/Fourier). **Material complementario**: EDP clásicas + Fourier intro.

#### Ramos — Ing. Comercial (transversales MATE25/MATE26)

**`utfsm-ing-comercial-mate10-algebra-y-geometria` · S1** — mismo programa que Plan Común Ing. Civil. Base: `precalculo-cero` · alto.

**`utfsm-ing-comercial-mate25-calculo-diferencial` · S2 · prereq MATE10**
Ejes: Derivada (definición, reglas, funciones elementales, cadena) · Aplicaciones (análisis, optimización) · Funciones de varias variables (parciales, gradiente) · Diferenciación multivariable (regla de la cadena) · Optimización con/sin restricciones (Lagrange, aplicaciones económicas).
Base: `calculo-dif-gen` + `calculo-vvar-gen` · **medio** (~60%, mezcla 1V y varias variables con enfoque económico).

**`utfsm-ing-comercial-mate20-algebra-lineal` · S2** — mismo programa que Plan Común. Base: `algebra-lineal-gen` · alto.

**`utfsm-ing-comercial-mate26-calculo-integral` · S3 · prereq MATE25**
Ejes: Integral (definida, TFC, primitivas) · Aplicaciones (áreas, volúmenes, economía) · EDO 1er y 2do orden (separables, lineales, coef. constantes) · Integración múltiple (dobles, aplicaciones).
Base: `calculo-int-gen` + `calculo-1var-gen` · **medio** (~55%, agrega EDO básicas e integrales dobles).

#### Ramos — Ing. Civil Matemática (especialidad avanzada)

**`utfsm-ing-civil-matematica-calculo-avanzado-variable-compleja` · S4**
Ejes: Cálculo vectorial (campos, integrales de línea/superficie, Green, Stokes, divergencia) · Series de Fourier (coeficientes, convergencia, transformada) · Variable compleja (analíticas, Cauchy-Riemann, Laurent, residuos).
Base: `calculo-vec-gen` · **medio** (~40%). Variable compleja + Fourier fuera de catálogo.

**`utfsm-ing-civil-matematica-ecuaciones-en-derivadas-parciales` · S5**
Ejes: EDP clásicas (calor, onda, Laplace) · separación de variables · Fourier aplicado · funciones de Green · métodos numéricos.
Base: `ec-dif-gen` · **bajo** (~20%). Tratar como curso nuevo.

---

## 4. Matriz cruzada: curso base Remy → universidades / ramos que lo aprovechan

> Útil para decidir orden de producción. Un curso base con más matches = más ROI por split.

### `precalculo-cero` (Precálculo desde Cero · 68 mód)

Cubre el **primer ramo de S1** de prácticamente todas las carreras (Álgebra, Intro al Cálculo, Métodos Mat. I, Mat. Avanzadas I):

- **UAI:** Álgebra (Plan Común, CS, Arq+ICI), Mat. Avanzadas I (Admin, Economía, Bach. ICom), Intro al Álgebra/Cálculo (Bachilleratos)
- **UANDES:** Álgebra e Intro al Cálculo (Plan Común), Intro al Álgebra y Geometría (Ing. Civil Química), Álgebra (Ing. Comercial), Nivelación Mat (Bachilleratos), Critical Thinking (IB)
- **UCH:** MA1001 + MA1101 (Plan Común FCFM, parcial), MM I (Ing. Comercial, IICG, Contador), Cálculo I + Álgebra I (Lic. Mat / Fís / Pedagogía)
- **UDD:** Álgebra (Plan Común, Geología, Ing. Comercial, GBA, Bach. IC), Intro al Cálculo (Plan Común, Geología), Mat. Aplicada I (BioMed), Matemáticas (Q&F), Componentes (Arq), Mat. Avanzada (NCD)
- **UTFSM:** MATE10 (Plan Común + Ing. Comercial), MAT070 (Plan Común — junto con `nivelacion-ing` y `calculo-dif-gen`)

→ **Primer curso a portar a Remy.** Mayor cobertura horizontal.

### `nivelacion-ing` (Nivelación Ingeniería · 43 mód)

Complementa a `precalculo-cero` en mallas STEM más exigentes:

- UAI: Álgebra (Plan Común, CS), Álgebra Bach. IC y Arq+ICI
- UANDES: Álgebra e Intro al Cálculo, Nivelación Mat (Bach. Ing.)
- UCH: MA1001 (Plan Común FCFM)
- UDD: Álgebra (Plan Común, Geología)
- UTFSM: MAT070 (Plan Común)

### `calculo-1var-gen` (Cálculo en una Variable · 85 mód)

Cubre tanto Cálculo Diferencial como Integral en una variable. **Curso “workhorse”** de S1–S2 STEM.

- UAI: Cálc Diferencial, Cálc Integral (Plan Común, CS, Arq+ICI), Mat Avanzadas II (Admin, Eco, Bach. ICom)
- UANDES: Cálc I + Cálc II (Plan Común Ing., Ing. Civil Química), Cálc I (Ing. Comercial), Cálc/Quant Methods (IB)
- UCH: MA1002 (Plan Común FCFM), MM III + MM IV (FEN), Cálc I+II (Lic. Mat/Fís/Ped)
- UDD: Intro Cálc, Cálc Diferencial, Cálc Integral (Plan Común, Geología); Cálculo (Ing. Comercial, GBA); Mat. Aplicada II/III (BioMed); Cálc (Q&F); Mat. Avanzada (NCD)
- UTFSM: MAT070 + Cálc en una Variable (Plan Común), MATE26 (Ing. Comercial)

→ **Segundo curso a portar.** Alta densidad de uso.

### `calculo-dif-gen` y `calculo-int-gen` (subsets de Cálc 1V)

Útiles cuando un ramo cubre **solo** la mitad (diferencial o integral). Mismos matches que `calculo-1var-gen` filtrados por mitad.

### `algebra-lineal-gen` (Álgebra Lineal · 52 mód)

Match casi 1:1 con todos los Álgebra Lineal de S2-S3 STEM.

- UAI: Álgebra Lineal (Plan Común, CS, Arq+ICI), Álg Lineal + Optimización (NTec), Mat. Avanzadas I (Admin, Eco, Bach. ICom)
- UANDES: Álgebra Lineal (Plan Común, Ing. Civil Química)
- UCH: MA1102 (Plan Común FCFM), MM II (FEN — parcial), Álg Lineal (Lic. Mat/Fís/Ped)
- UDD: Álgebra Lineal (Plan Común), Cálculo (Ing. Comercial — parcial), Mat. Aplicada III (BioMed), Mat. Avanzada (NCD)
- UTFSM: MATE20 (Plan Común + Ing. Comercial)

→ **Tercer curso a portar.** Match alto y limpio.

### `calculo-vvar-gen` + `calculo-vec-gen`

Para Cálculo Multivariables / Vectorial de S3-S4 STEM.

- UAI: Cálc Multivariables (Plan Común, Arq+ICI)
- UANDES: Cálc II (Plan Común — parcial), Cálc II (Ing. Civil Química), Optimización (Ing. Comercial)
- UCH: MA2001 + MA2002 (Plan Común FCFM), Cálc III (Lic. Mat / Lic. Fís)
- UDD: Cálc Multivariable (Plan Común), Cálculo (Ing. Comercial — parcial), Mat. Aplicada IV (BioMed)
- UTFSM: Cálc Varias Variables (Plan Común), Cálc Avanzado (ICM — parcial), MATE25 (Ing. Comercial — parcial)

### `ec-dif-gen` (Ecuaciones Diferenciales · 42 mód)

Para EDO de S3-S4 STEM. Algunas mallas (UCh, UTFSM) extienden con sistemas no lineales, EDP o Fourier — requieren material complementario.

- UAI: ED (Plan Común, Arq+ICI)
- UANDES: ED (Plan Común, Ing. Civil Química)
- UCH: MA2601 (Plan Común FCFM — ~75%, agregar sist. no lineales / Lyapunov), ED (Lic. Mat / Lic. Fís)
- UDD: ED (Plan Común, Geología), Mat. Aplicada IV (BioMed)
- UTFSM: ED EDO+EDP (Plan Común — ~70%, agregar EDP/Fourier), EDP (ICM — bajo, curso nuevo)

---

## 5. Cómo usar este documento desde Claude Code en Remy

1. **Crear un curso base** en Remy por cada ID de la sección 1 (mismo slug). Las **lecciones** de Remy se mapean uno a uno con los módulos de cada curso Se Remonta.
2. Por cada ramo de la sección 3, **crear un curso universitario derivado** con:
   - `id`: el del documento (ej. `uai-plan-comun-algebra-lineal`)
   - `universidad`, `carrera`, `semestre`, `nombre`, `codigo` (si aplica), `prereqs`
   - `ejes`: el array `contenidos`
   - `base_ids`: array con los cursos base sugeridos
   - `match_level`: alto / medio / bajo
   - Cuando el match sea **alto** y `base_ids` tenga uno solo, el curso derivado puede ser una **vista filtrada** del base sin lecciones nuevas. Sólo cambian metadata (nombre, código, marca de U) y orden pedagógico.
   - Cuando sea **medio**, generar/seleccionar las lecciones aplicables del base y crear un **set de simulacros/ejercicios específico** para la U + el código del ramo.
3. **Generación de preguntas / simulacros:** seguir el SOP `docs/procesos/sop-remy-preguntas.md`. Cada eje de cada ramo es un objetivo de aprendizaje sobre el cual generar preguntas tipo control de la U real.
4. **Prerrequisitos:** modelarlos en Remy como dependencias entre cursos derivados de la misma universidad (no entre los base — los base son universales).
5. **Estado de cobertura:** mantener una columna `cubierto_en_remy: boolean` por ramo, igual que el `status` que llevamos en `apps/ops/data/splits/universities/*.json`.

---

## 6. Próximos splits a sumar (mallas pendientes — Cowork)

Estas universidades aún no tienen ramos cargados en el catálogo (sólo a nivel de investigación general). Cuando Cowork las complete, este documento se regenera.

- **Fase 3 (Jul–Sep):** USACH, UdeC, PUCV
- **Fase 4 (Sep–Dic):** UDP, UNAB, USS, UMayor

Cada nueva U cae como sección adicional en §3 siguiendo el mismo formato.

---

*Este documento se regenera desde `apps/ops/data/splits/` (catalog + universities). Si la investigación se actualiza, ejecutar el script de exportación o regenerar manualmente esta vista.*
