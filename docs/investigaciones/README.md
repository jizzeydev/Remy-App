# Investigaciones de mallas curriculares — Remy

Workflow para investigar **universidades chilenas** y producir, para cada una, un mapa **corto y verificado** de:

1. Las **4 carreras de mayor demanda** (Ingeniería Civil / plan común, Medicina, Ingeniería Comercial, Derecho).
2. Por carrera: malla oficial vigente.
3. Por ramo prioritario: el **programa oficial leído de la fuente** (no inferido del nombre), con contenidos por unidad y bibliografía.
4. Una propuesta de cursos Remy con **capítulos derivados de los contenidos reales**.

## Por qué este foco

Una versión anterior intentaba mapear *todas* las carreras de la universidad (ej. el primer pase de PUC quedó en 1.293 líneas). Eso era valioso como panorama, pero:

- **Inmanejable como insumo de producto.** Demasiado largo para decidir qué armar.
- **Propenso a errores.** Sin verificación del programa oficial, el modelo asignó contenidos por el nombre del ramo (ej. clasificó *MAT1620 — Cálculo II* de PUC como "cálculo integral" cuando en realidad es **cálculo multivariable**; en PUC, integral y diferencial van juntos en MAT1610 y MAT1630 es el vectorial).

Esta versión corrige ambos problemas: **menos carreras, más profundidad por ramo, todo trazable a un PDF/syllabus oficial.**

## Las 4 carreras objetivo (estándar)

Para mantener comparabilidad entre universidades, **siempre se investigan las mismas cuatro**:

| Carrera | Por qué | Notas de mapeo |
|---|---|---|
| Ingeniería Civil (plan común o equivalente) | Mayor cohorte STEM. Cubre el núcleo cuantitativo de Remy. | Si la universidad no tiene "plan común", tomar la malla de Ing. Civil Industrial o la base que comparten todas las civiles. |
| Medicina | Mayor demanda en salud. Define el catálogo MED/BIO/QUI. | Si la universidad no dicta Medicina, reemplazar por Enfermería + nota explicando. |
| Ingeniería Comercial | Mayor demanda económico-administrativa. Define ECO + ADM + CTB. | Si la universidad usa "Administración" o "Negocios", tomar la equivalente. |
| Derecho | Mayor demanda en humanidades/jurídicas. Define JUR. | Carrera estándar; sin reemplazos. |

Cualquier carrera fuera de esta lista queda explícitamente **fuera del alcance** de la investigación. Si producto necesita otra (ej. Psicología, Pedagogía Básica), se hace una investigación adicional dirigida.

## Cómo usar este workflow

Una universidad por vez, **una sola conversación de Cowork** por universidad. El flujo es:

1. Copiar [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) → `docs/investigaciones/<sigla>.md`.
2. Abrir el **prompt master** de [PROMPTS_COWORK.md](./PROMPTS_COWORK.md), reemplazar placeholders y pegarlo en una conversación nueva de **Claude Cowork** con la **extensión Claude in Chrome** activa.
3. Cowork recorre las 5 fases del prompt (setup → mallas → programas verificados → catálogo Remy → verificación). Vas pegando el output fase por fase.
4. El [WORKFLOW.md](./WORKFLOW.md) detalla pre-requisitos, buenas prácticas y errores comunes.

Tiempo estimado: **1.5 a 2.5 hrs** por universidad (antes 3–6).

## Archivos del workflow

| Archivo | Para qué sirve |
|---|---|
| [PROMPTS_COWORK.md](./PROMPTS_COWORK.md) | Prompt master one-shot + prompt de curación (para arreglar investigaciones viejas) + prompts auxiliares. |
| [WORKFLOW.md](./WORKFLOW.md) | Pre-requisitos, buenas prácticas con Cowork y Claude in Chrome, errores comunes. |
| [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) | Plantilla del informe. Copiar y renombrar a `<sigla>.md`. |

## Universidades objetivo

Orden sugerido por **tamaño de cohortes en las 4 carreras objetivo**:

**Tradicionales (CRUCh):**

1. Universidad de Chile — `uchile.cl`
2. Pontificia Universidad Católica de Chile — `uc.cl` *(ya investigada — necesita curación, ver prompt en PROMPTS_COWORK.md)*
3. Universidad de Santiago de Chile — `usach.cl`
4. Universidad de Concepción — `udec.cl`
5. Pontificia Universidad Católica de Valparaíso — `pucv.cl`
6. Universidad Técnica Federico Santa María — `usm.cl` (no dicta Medicina ni Derecho — solo Ing. Civil + Ing. Comercial)
7. Universidad de Valparaíso — `uv.cl`
8. Universidad Austral de Chile — `uach.cl`

**Privadas grandes:**

9. Universidad Andrés Bello — `unab.cl`
10. Universidad San Sebastián — `uss.cl`
11. Universidad del Desarrollo — `udd.cl`
12. Universidad Adolfo Ibáñez — `uai.cl` (no dicta Medicina; reemplazar por nota)
13. Universidad de los Andes — `uandes.cl`
14. Universidad Diego Portales — `udp.cl`
15. Universidad Mayor — `umayor.cl`

## Áreas de conocimiento (taxonomía estandarizada)

Para mantener consistencia, **todo ramo se etiqueta con una de estas áreas**:

| Código | Área | Ejemplos de ramos |
|---|---|---|
| `MAT` | Matemáticas | Cálculo, álgebra lineal, EDOs, estadística, probabilidad |
| `FIS` | Física | Mecánica, electromagnetismo, termodinámica |
| `QUI` | Química | Química general, orgánica, inorgánica |
| `BIO` | Biología | Biología celular, molecular, genética |
| `ECO` | Economía y finanzas | Microeconomía, macro, finanzas, mercados |
| `ADM` | Administración y gestión | Estrategia, marketing, RRHH, operaciones |
| `CTB` | Contabilidad y auditoría | Contabilidad financiera, costos, tributaria |
| `JUR` | Derecho | Civil, penal, comercial, laboral, constitucional |
| `MED` | Medicina y salud | Anatomía, fisiología, patología, farmacología |
| `INF` | Computación e informática | Programación, BD, redes, IA |
| `ING` | Ingeniería aplicada | Procesos, materiales, hidráulica, estructuras |
| `HUM` | Humanidades | Historia, filosofía, ética, teología |
| `MET` | Metodología e investigación | Metodología, tesis, seminarios |
| `OFG` | Formación general / electivos | OFG, electivos transversales |
| `PRA` | Prácticas y trabajo aplicado | Práctica profesional, internado |

> Si un ramo cubre dos áreas, usar `+` (ej. `MAT+ECO` para econometría). Si nada encaja, `OTRO` con justificación breve.

## Catálogo actual de Remy

Lo que Remy tiene **hoy** (todos área `MAT`):

- precalculo (8 caps)
- calculo-diferencial (3 caps)
- calculo-integral (3 caps)
- calculo-multivariable (7 caps)
- calculo-vectorial (3 caps)
- algebra-lineal (8 caps)
- ecuaciones-diferenciales (4 caps)

Cualquier ramo fuera de matemáticas universitarias es un **gap esperable** que el workflow debe identificar para alimentar la roadmap.

## Output esperado por investigación

Cada `<sigla>.md` debe incluir, en este orden:

1. **Datos institucionales** mínimos.
2. **Las 4 carreras objetivo** — para cada una: malla oficial vigente con tabla de ramos.
3. **Programas verificados** — para los ramos prioritarios (los que mapean al catálogo Remy actual o futuro): cita textual de los contenidos, bibliografía y URL del programa oficial.
4. **Propuesta de catálogo Remy** — cursos a crear/expandir, con **capítulos derivados de los contenidos reales** extraídos en la fase anterior.
5. **Mapeo carrera → cursos Remy**.
6. **Fuentes consultadas** con URL, fecha y estado.

## Verificación de fuentes

**Solo se aceptan:**

- Dominio de la universidad (`*.<sigla>.cl`).
- Mifuturo (`mifuturo.cl`) y DEMRE (`demre.cl`) para datos cruzados.
- PDFs descargados directamente del sitio oficial.

**No se aceptan:**

- Foros, Reddit, blogs estudiantiles.
- Listas no datadas o sin link a la fuente.
- Mallas que no indiquen año de vigencia o cohorte.

**Regla central de esta versión:** ningún ramo puede etiquetarse con contenidos sin **abrir su programa oficial** y **citar texto verbatim** del documento. Si el programa no está disponible, el ramo se marca con ⚠️ y queda fuera de la propuesta de catálogo.
