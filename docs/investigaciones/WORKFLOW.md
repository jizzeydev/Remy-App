# Workflow de investigación por universidad

Proceso para investigar **una universidad chilena** y mapear **todas las carreras de pregrado** con sus respectivas mallas, en **una sola sesión de Claude Cowork** usando el prompt master de [PROMPTS_COWORK.md](./PROMPTS_COWORK.md).

Tiempo estimado: **3 a 6 horas** por universidad según cantidad de carreras y calidad del sitio.

## Idea general

Una sola conversación de Cowork resuelve toda la investigación. El **prompt master** instruye al modelo a recorrer 8 fases dentro de la misma sesión:

1. Setup y datos institucionales
2. Inventario completo de carreras
3. Priorización (ALTA/MEDIA/BAJA)
4. Extracción de mallas
5. Agregación por área
6. Propuesta de catálogo Remy
7. Mapeo carrera → cursos Remy
8. Verificación final y fuentes

El output del modelo va llenando, fase por fase, las secciones de [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) — que copiaste antes como `<sigla>.md`.

## Pre-requisitos

Antes de empezar:

- [ ] **Claude Cowork** abierto en una pestaña dedicada (conversación nueva).
- [ ] **Extensión Claude in Chrome** instalada y autenticada (`chrome://extensions` la muestra activa).
- [ ] El navegador con permisos para que Claude opere las pestañas (clickear, leer DOM, descargar).
- [ ] Una pestaña en blanco lista para que Claude navegue.
- [ ] La taxonomía de áreas (sección "Áreas de conocimiento" en [README.md](./README.md)) — el prompt la incluye, pero tenerla a mano para verificar no está de más.
- [ ] Una copia de [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) renombrada como `<sigla>.md` (ej. `uc.md`, `uchile.md`, `usach.md`) en esta carpeta.

## Cómo correr una investigación

1. **Crear el archivo de la universidad.** Copiá `PLANTILLA_UNIVERSIDAD.md` → `docs/investigaciones/<sigla>.md` y completá el encabezado (nombre, sigla, fecha).

2. **Preparar el prompt master.** Abrí [PROMPTS_COWORK.md](./PROMPTS_COWORK.md), copiá el "Prompt master" completo y reemplazá los placeholders:

   - `{{NOMBRE_UNIVERSIDAD}}` — nombre completo (ej. "Pontificia Universidad Católica de Chile").
   - `{{SIGLA}}` — sigla institucional (ej. "UC").
   - `{{DOMINIO_OFICIAL_O_VACIO}}` — dominio raíz oficial (ej. `uc.cl`). Si no lo conocés, dejá vacío y Cowork lo busca.
   - `{{URL_LISTADO_CARRERAS_O_VACIO}}` — URL del listado completo de carreras si la conocés. Si no, dejá vacío.

3. **Iniciar la conversación.** Abrí Cowork en una conversación nueva, **activá la extensión Chrome** y pegá el prompt completo.

4. **Acompañar el proceso.** Cowork va a recorrer las 8 fases. En las largas (especialmente Fase 4 con muchas carreras) va a pausar para que confirmes con "ok, sigamos". Mientras tanto:

   - **Pegá el output de cada fase** en el `<sigla>.md` a medida que avanza, **no esperes al final**.
   - **Verificá las extracciones** importantes: muestra de URLs, año del plan, áreas asignadas.
   - **Si Cowork queda atascado** (captcha, login, sitio caído), usá uno de los **prompts auxiliares** del archivo PROMPTS para destrabarlo.

5. **Verificar y cerrar.** Al terminar la Fase 8, revisá la sección final del informe y completá lo que falte (tu nombre, tiempo invertido, observaciones).

## Sobre el uso de Claude in Chrome

La extensión permite que Claude **opere directamente en el navegador**: navega URLs, lee el contenido renderizado, sigue links, descarga PDFs. Esto es esencial porque muchas mallas están en:

- Páginas dinámicas con JavaScript que no se ven con un fetch simple.
- Tablas HTML que requieren parseo de la estructura visible.
- PDFs embebidos en visores propios de la universidad.
- Formularios que requieren navegación (seleccionar carrera → submit → ver malla).

**Buenas prácticas:**

1. **Una pestaña dedicada** a la investigación, sin otras tabs interfiriendo.
2. **Permití explícitamente** a Claude operar la pestaña al inicio de la sesión.
3. Si Claude se atasca en un sitio (banner de cookies, modal, login), **resolvelo manualmente** y volvé a darle el control con el prompt auxiliar correspondiente.
4. Si la extensión no logra acceder a algo (PDFs protegidos, paywall), **descargá manualmente** y subilo a la conversación.
5. Para universidades con muchas carreras, el prompt master ya divide la Fase 4 en lotes — confirmá entre lotes para evitar perder contexto.

## Sobre Cowork

Cowork mantiene contexto entre mensajes dentro de la misma conversación. Eso significa que:

- **Una sola conversación cubre toda la investigación** de una universidad.
- **Una conversación por universidad** — no mezcles dos en la misma sesión.
- Si la conversación se vuelve muy larga (50+ carreras o más de 4 horas), abrí una segunda conversación con el prompt auxiliar **"Para acelerar dividiendo en sesiones distintas"** y pasá como contexto inicial el archivo `<sigla>.md` parcial.

## Catálogo actual de Remy (referencia)

Lo que Remy tiene **hoy** son cursos de matemáticas, todos en la categoría `MAT`:

- precalculo (8 caps)
- calculo-diferencial (3 caps)
- calculo-integral (3 caps)
- calculo-multivariable (7 caps)
- calculo-vectorial (3 caps)
- algebra-lineal (8 caps)
- ecuaciones-diferenciales (4 caps)

**Cualquier ramo que no sea de matemáticas universitarias es, por definición, un gap del catálogo actual.** Esto es esperable y deseado: el objetivo del workflow es identificar qué cursos crear a continuación.

Algunos cursos que probablemente aparezcan como gaps recurrentes (ya esperables):

- Probabilidad y estadística (área `MAT`).
- Variable compleja, métodos numéricos, EDPs (área `MAT`).
- Microeconomía, macroeconomía, finanzas básicas (área `ECO`).
- Contabilidad financiera, costos (área `CTB`).
- Marketing, gestión, RRHH, estrategia (área `ADM`).
- Anatomía, fisiología, bioquímica, farmacología (área `MED`).
- Derecho civil, penal, comercial, constitucional (área `JUR`).
- Psicología general, evolutiva, social (área `PSI`).
- Programación introductoria, bases de datos, redes (área `INF`).
- Física básica universitaria (área `FIS`).
- Química general, orgánica (área `QUI`).
- Metodología de investigación (área `MET`).

## Errores comunes a evitar

- **Filtrar carreras por "tienen matemática" o no.** No aplica. **Todas las carreras se inventarían.**
- **Confundir mallas viejas con vigentes.** Las universidades suelen tener varios planes activos según cohorte. Tomá siempre la más reciente, anotando el año.
- **Tomar mallas de un campus por las del otro.** UDP Santiago no es lo mismo que UDP Concepción si ambas existen.
- **Asumir que el nombre del ramo equivale al contenido.** "Cálculo II" en una universidad puede ser cálculo integral; en otra puede ser cálculo multivariable. Siempre verificar el programa cuando esté disponible.
- **Asignar área `OTRO` sin justificar.** Eso indica que no se entendió el ramo. Investigar el programa antes de etiquetar así.
- **Dejar prácticas / tesis / talleres con área vacía.** Etiquetar como `PRA` o `MET` para mantener consistencia.
- **No anotar la fecha de consulta.** Las mallas cambian; sin fecha, en 6 meses no sabremos si la info sigue vigente.
- **Olvidarse de las carreras vespertinas o de continuidad de estudios.** Algunas universidades tienen mallas distintas para sus programas vespertinos o "advance"; mencionarlas en notas.
- **Pegar el output de Cowork solo al final.** Pegar fase por fase reduce el riesgo de perder trabajo si la conversación se cae o se vuelve inmanejable.

## Output esperado

Al cerrar el workflow, `<sigla>.md` debe tener llenas todas las secciones de la plantilla. Ese archivo es el **entregable** de la investigación y la base para que el equipo de producto decida qué cursos producir a continuación.
