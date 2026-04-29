# Workflow de investigación por universidad

Proceso para investigar **una universidad chilena** mapeando **las 4 carreras de mayor demanda** con sus mallas y los **programas oficiales** de los ramos prioritarios. Una sola sesión de Claude Cowork con el prompt master de [PROMPTS_COWORK.md](./PROMPTS_COWORK.md).

Tiempo estimado: **1.5 a 2.5 horas** por universidad.

## Idea general

Una sola conversación de Cowork resuelve toda la investigación. El prompt master instruye al modelo a recorrer 5 fases:

1. **Setup y datos institucionales** (5 min) — sigla, sitio, sedes, URL del listado de mallas.
2. **Mallas de las 4 carreras objetivo** (30–45 min) — Ing. Civil/plan común, Medicina, Ing. Comercial, Derecho. Tabla compacta por carrera (código, nombre, semestre, créditos, área).
3. **Programas verificados de los ramos prioritarios** (45–75 min) — solo los ramos que mapean al catálogo Remy actual o futuro. Para cada uno: abrir el programa oficial, **citar verbatim** los contenidos por unidad y la bibliografía.
4. **Propuesta de catálogo Remy** (15 min) — cursos a crear/expandir, con **capítulos derivados de los contenidos reales** de la Fase 3.
5. **Mapeo carrera → cursos Remy + verificación final + fuentes** (15 min).

El output va llenando, fase por fase, las secciones de [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md).

## Pre-requisitos

- [ ] **Claude Cowork** abierto en una pestaña dedicada (conversación nueva).
- [ ] **Extensión Claude in Chrome** instalada y autenticada.
- [ ] Permiso explícito a la extensión para operar la pestaña (clickear, leer DOM, descargar).
- [ ] Una pestaña en blanco lista para que Claude navegue.
- [ ] Una copia de [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) renombrada como `<sigla>.md` (ej. `uc.md`, `uchile.md`).

## Cómo correr una investigación

1. **Crear el archivo.** Copiá la plantilla → `docs/investigaciones/<sigla>.md` y completá el encabezado.
2. **Preparar el prompt master.** Abrí [PROMPTS_COWORK.md](./PROMPTS_COWORK.md), copiá el "Prompt master" y reemplazá:
   - `{{NOMBRE_UNIVERSIDAD}}` — nombre completo (ej. "Universidad de Chile").
   - `{{SIGLA}}` — sigla (ej. "UCH").
   - `{{DOMINIO_OFICIAL_O_VACIO}}` — dominio raíz (ej. `uchile.cl`).
   - `{{URL_LISTADO_CARRERAS_O_VACIO}}` — URL del listado de carreras si la conocés.
   - `{{NOTAS_DE_REEMPLAZO_DE_CARRERAS}}` — si la universidad no dicta alguna de las 4 carreras objetivo (ej. UTFSM no tiene Medicina ni Derecho), aclarar el reemplazo o el "skip" acá.
3. **Iniciar la conversación.** Abrí Cowork en conversación nueva, **activá la extensión Chrome** y pegá el prompt completo.
4. **Acompañar.** Cowork va a recorrer las 5 fases. Pegá el output de cada fase en `<sigla>.md` a medida que avanza, **no esperes al final**.
5. **Verificar Fase 3.** Es la fase crítica. Para cada programa "verificado" debe haber un link al PDF/HTML del programa oficial **y** una cita textual de los contenidos. Si Cowork resume sin citar, pedile la cita.
6. **Cerrar.** Al terminar la Fase 5, completá el encabezado (tu nombre, tiempo invertido, observaciones).

## Sobre el uso de Claude in Chrome

La extensión permite que Claude **opere directamente en el navegador**: navega URLs, lee DOM, sigue links, descarga PDFs. Esencial porque las mallas suelen estar en:

- Páginas dinámicas con JavaScript que no se ven con un fetch simple.
- Tablas HTML con estructura visible solo renderizada.
- PDFs embebidos en visores propios.
- Formularios (seleccionar carrera → submit → ver malla).

**Buenas prácticas:**

1. **Una pestaña dedicada** a la investigación, sin otras tabs interfiriendo.
2. **Permití explícitamente** a Claude operar la pestaña al inicio.
3. Si Claude se atasca (banner de cookies, modal, login), **resolvelo manualmente** y devolvele el control con el prompt auxiliar correspondiente.
4. Si la extensión no logra acceder a un PDF, **descargalo manualmente** y subilo a la conversación.
5. **Para Fase 3 (programas), exigí siempre el link al programa oficial.** Si no lo hay, el ramo se marca con ⚠️ y queda fuera de la propuesta.

## Sobre Cowork

- **Una sola conversación cubre toda la investigación** de una universidad.
- **Una conversación por universidad** — no mezcles dos.
- Si la conversación se vuelve muy larga (más de 2.5 hrs), abrí una segunda con el prompt auxiliar **"Para acelerar dividiendo en sesiones distintas"** y pasá el `<sigla>.md` parcial como contexto inicial.

## Catálogo actual de Remy (referencia para Fase 4)

Lo que Remy tiene **hoy** (todos área `MAT`):

- precalculo (8 caps)
- calculo-diferencial (3 caps), calculo-integral (3), calculo-multivariable (7), calculo-vectorial (3)
- algebra-lineal (8 caps)
- ecuaciones-diferenciales (4 caps)

**Cualquier ramo fuera de matemáticas universitarias es un gap esperable.** El objetivo del workflow es identificar qué cursos crear.

Gaps recurrentes esperables (ya validados con la primera investigación PUC):

- Probabilidad y estadística (`MAT`).
- Programación introductoria — Python (`INF`).
- Microeconomía + Macroeconomía intro (`ECO`).
- Contabilidad financiera básica (`CTB`).
- Química general universitaria (`QUI`).
- Biología celular intro (`BIO`).
- Física mecánica + electromagnetismo (`FIS`).
- Anatomía + fisiología intro (`MED`).
- Introducción al derecho + Derecho civil I (`JUR`).

## Errores comunes a evitar

- **Etiquetar contenidos por el nombre del ramo.** El error #1 documentado: "Cálculo II" puede ser cálculo integral en una universidad y multivariable en otra (en PUC, MAT1620 = multivariable, no integral; integral va dentro de MAT1610). **Siempre abrir el programa oficial y citar textualmente.**
- **Confundir mallas viejas con vigentes.** Tomar siempre la última, anotando el año de cohorte.
- **Tomar mallas de un campus por las del otro.** Si la carrera se dicta en varias sedes con planes distintos, declarar cuál se usa y por qué.
- **Asignar área `OTRO` sin justificar.** Indica que no se entendió el ramo.
- **Dejar prácticas / tesis con área vacía.** Etiquetar como `PRA` o `MET`.
- **Inventar bibliografía.** Si el programa oficial no la lista, dejar el campo vacío con ⚠️.
- **No anotar la fecha de consulta.** Las mallas cambian; sin fecha, en 6 meses no sabremos si la info sigue vigente.
- **Pegar el output solo al final.** Pegar fase por fase reduce el riesgo de perder trabajo si la conversación se cae.

## Output esperado

Al cerrar el workflow, `<sigla>.md` debe tener:

- Datos institucionales mínimos.
- Las 4 mallas objetivo con tabla compacta de ramos.
- La sección **"Programas verificados"** con cita textual de contenidos para los ramos prioritarios.
- Propuesta de catálogo Remy con capítulos derivados de esos contenidos.
- Mapeo carrera → cursos Remy.
- Tabla de fuentes con URL + fecha + estado.

Eso es el **entregable** y la base para que producto decida qué cursos producir.
