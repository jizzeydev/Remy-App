# Investigaciones de mallas curriculares — Remy

Workflow para investigar **universidades chilenas** y extraer **todos los ramos de todas las carreras de pregrado** que figuran en sus mallas curriculares oficiales.

## Por qué expandimos el alcance

Remy nació con foco en matemáticas universitarias (precálculo, cálculo, álgebra, EDOs), pero el plan es **convertirla en una plataforma para todas las carreras**: ingeniería civil, ingeniería comercial, administración de empresas, medicina, derecho, psicología, arquitectura, kinesiología, periodismo, etc.

Para que el equipo de producto pueda decidir qué cursos crear primero, necesitamos un **mapa real del territorio**: qué se enseña, en qué carreras, en qué orden, con qué profundidad.

Cada investigación produce dos cosas:

1. **Un mapa de ramos** por carrera, con codigo, nombre, semestre, créditos, contenidos.
2. **Una propuesta de catálogo Remy** — qué cursos vale la pena armar a partir de lo que se repite, agrupado por área de conocimiento (matemáticas, ciencias económicas, ciencias jurídicas, ciencias de la salud, ciencias sociales, humanidades, etc.).

## Cómo usar este workflow

La investigación es **una universidad por vez**, **una sola conversación de Cowork** por universidad. El flujo es:

1. Copiar [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) → `docs/investigaciones/<sigla>.md` (el entregable).
2. Abrir el **prompt master** de [PROMPTS_COWORK.md](./PROMPTS_COWORK.md), reemplazar los placeholders (`{{NOMBRE_UNIVERSIDAD}}`, `{{SIGLA}}`, `{{DOMINIO_OFICIAL}}`, `{{URL_LISTADO_CARRERAS}}`) y pegarlo en una conversación nueva de **Claude Cowork** con la **extensión Claude in Chrome** activa.
3. Cowork recorre las 8 fases del prompt (setup, inventario, priorización, extracción, agregación, propuesta de catálogo, mapeo, verificación). Vas pegando el output fase por fase en el `<sigla>.md`.
4. El [WORKFLOW.md](./WORKFLOW.md) detalla el contexto, las buenas prácticas y los errores comunes.

## Archivos del workflow

| Archivo | Para qué sirve |
|---|---|
| [PROMPTS_COWORK.md](./PROMPTS_COWORK.md) | **El prompt master one-shot** que cubre toda la investigación en una sesión, más prompts auxiliares para imprevistos (sitio caído, contexto a refrescar, dividir en sesiones). |
| [WORKFLOW.md](./WORKFLOW.md) | Contexto del proceso, pre-requisitos, buenas prácticas con Cowork y Claude in Chrome, errores comunes. |
| [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) | Plantilla del informe que llena cada investigación. Copiar y renombrar a `<sigla>.md`. |

## Universidades objetivo

Sugerencia de orden por **diversidad de carreras** y **volumen de estudiantes** (no por foco STEM como antes):

**Tradicionales (CRUCh) — alta diversidad de facultades:**

1. Universidad de Chile — `uchile.cl`
2. Pontificia Universidad Católica de Chile — `uc.cl`
3. Universidad de Santiago de Chile — `usach.cl`
4. Universidad de Concepción — `udec.cl`
5. Pontificia Universidad Católica de Valparaíso — `pucv.cl`
6. Universidad Austral de Chile — `uach.cl`
7. Universidad de Valparaíso — `uv.cl`
8. Universidad de la Frontera — `ufro.cl`
9. Universidad de Talca — `utalca.cl`
10. Universidad Técnica Federico Santa María — `usm.cl` (más STEM, pero igual relevante)

**Privadas grandes — gran cantidad de alumnos:**

11. Universidad Andrés Bello — `unab.cl`
12. Universidad San Sebastián — `uss.cl`
13. Universidad Mayor — `umayor.cl`
14. Universidad Autónoma de Chile — `uautonoma.cl`
15. Universidad Diego Portales — `udp.cl`
16. Universidad del Desarrollo — `udd.cl`
17. Universidad Adolfo Ibáñez — `uai.cl`
18. Universidad de los Andes — `uandes.cl`
19. Universidad Finis Terrae — `finisterrae.cl`
20. Universidad Central — `ucentral.cl`

**IP/CFT (carreras técnicas y profesionales — segmento amplio):**

- INACAP — `inacap.cl`
- DUOC UC — `duoc.cl`
- AIEP — `aiep.cl`
- IP Chile — `ipchile.cl`

## Áreas de conocimiento (taxonomía estandarizada)

Para mantener consistencia entre investigaciones, **todo ramo se clasifica en una de estas áreas**:

| Código | Área | Ejemplos de ramos |
|---|---|---|
| `MAT` | Matemáticas | Cálculo, álgebra lineal, EDOs, estadística, probabilidad |
| `FIS` | Física | Mecánica, electromagnetismo, termodinámica |
| `QUI` | Química | Química general, orgánica, inorgánica, fisicoquímica |
| `BIO` | Biología | Biología celular, molecular, genética, ecología |
| `ECO` | Economía y finanzas | Microeconomía, macro, finanzas corporativas, mercados |
| `ADM` | Administración y gestión | Estrategia, marketing, RRHH, operaciones, gestión |
| `CTB` | Contabilidad y auditoría | Contabilidad financiera, costos, auditoría, tributaria |
| `JUR` | Derecho | Derecho civil, penal, comercial, laboral, constitucional |
| `MED` | Medicina y salud | Anatomía, fisiología, patología, farmacología, clínica |
| `PSI` | Psicología | Psicología general, clínica, social, evolutiva |
| `SOC` | Ciencias sociales | Sociología, antropología, ciencia política |
| `EDU` | Educación y pedagogía | Didáctica, curriculum, psicopedagogía |
| `HUM` | Humanidades | Historia, filosofía, literatura, teología, ética |
| `COM` | Comunicaciones | Periodismo, publicidad, RRPP, audiovisual |
| `ART` | Arte y diseño | Diseño gráfico, industrial, arquitectura, música |
| `INF` | Computación e informática | Programación, bases de datos, redes, IA, ciberseguridad |
| `ING` | Ingeniería aplicada | Procesos industriales, materiales, hidráulica, estructuras |
| `IDI` | Idiomas | Inglés técnico, segundo idioma |
| `MET` | Metodología e investigación | Metodología de investigación, tesis, seminarios |
| `OFG` | Formación general / electivos | Cursos de OFG, electivos transversales |
| `PRA` | Prácticas y trabajo aplicado | Práctica profesional, internado, taller integrador |

> **Nota:** estas categorías se pueden refinar con sub-áreas cuando aparezcan ramos muy específicos (por ejemplo dentro de `JUR` se puede sub-clasificar en `JUR.civil`, `JUR.penal`, etc.). El objetivo es agregar después por área para detectar qué cursos vale la pena producir.

## Output esperado por investigación

Cada `<sigla>.md` debe incluir:

- Datos institucionales (nombre, sigla, sitio oficial, fecha de la consulta).
- Lista de **todas las carreras de pregrado** organizadas por facultad/área.
- Por cada carrera procesada: tabla de **todos los ramos del plan de estudio** con código, nombre, semestre, créditos, pre-requisitos, link al programa, contenidos resumidos y **área de conocimiento**.
- **Resumen agregado por área**: cuántos ramos hay de cada área, en cuántas carreras aparecen, ramos más frecuentes.
- **Propuesta de catálogo Remy**: qué cursos crear/expandir, ordenados por demanda.
- **Fuentes** — URLs oficiales con fecha de consulta y, si descargaste PDFs, nombre del archivo y origen.

## Sobre la verificación de fuentes

**Solo se aceptan fuentes oficiales:**

- Dominio de la universidad (`*.<sigla>.cl`).
- Portal Mifuturo (`mifuturo.cl`) del Ministerio de Educación, para datos cruzados de empleabilidad/matrícula.
- DEMRE (`demre.cl`) cuando aplique.
- PDFs descargados directamente del sitio oficial.

**No se aceptan:**

- Foros, Reddit, blogs estudiantiles.
- Listas no datadas o sin link a la fuente.
- Mallas que no indiquen año de vigencia o cohorte.

Si una fuente parece dudosa, **se descarta** y se busca confirmación en el sitio oficial. Mejor un dato menos que un dato incorrecto.
