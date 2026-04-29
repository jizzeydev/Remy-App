# {{NOMBRE_UNIVERSIDAD}} ({{SIGLA}})

> **Cómo usar esta plantilla:** copialá renombrándola como `<sigla>.md` (ej. `uc.md`, `uchile.md`)
> y completá las secciones a medida que avanzás las 5 fases del [WORKFLOW.md](./WORKFLOW.md)
> con el prompt master de [PROMPTS_COWORK.md](./PROMPTS_COWORK.md).

**Investigado por:** {{tu nombre}}
**Fecha de consulta:** {{YYYY-MM-DD}}
**Tiempo invertido:** {{horas}}
**Estado:** 🟢 Completo / 🟡 En progreso / 🔴 Bloqueado

---

## Datos institucionales

> Completar después de la **Fase 1**.

- **Nombre oficial:** {{nombre completo}}
- **Sigla:** {{SIGLA}}
- **Sitio oficial:** [{{dominio}}]({{URL}})
- **Sedes:** {{ciudad 1, ciudad 2, ...}}
- **Portal de admisión:** [{{URL}}]({{URL}})
- **Listado de carreras:** [{{URL}}]({{URL}})
- **Catálogo de cursos / programas:** [{{URL}}]({{URL}})

### Notas de reemplazo de carreras

> Si la universidad NO dicta alguna de las 4 carreras objetivo, anotalo acá con la URL donde
> verificaste la ausencia y la decisión tomada (skip o reemplazo).

- {{ej. "UTFSM no dicta Medicina ni Derecho — verificado en [admision.usm.cl](...). Skip."}}

---

## Las 4 carreras objetivo

> Completar después de la **Fase 2**. Una sub-sección por carrera con la tabla compacta de
> su malla (sin contenidos — esos van en la sección "Programas verificados").

### Ingeniería Civil — plan común 🎯

**Facultad:** {{...}} · **Plan:** {{año}} · **Total ramos:** {{n}} · **Sede:** {{...}}
**URL malla:** [{{...}}]({{...}})

| Código | Nombre | Sem | Créditos | Pre-req | Área | URL programa |
|---|---|---|---|---|---|---|
| {{MAT1610}} | {{Cálculo I}} | 1 | 10 | — | MAT | [prog]({{...}}) |
| {{MAT1203}} | {{Álgebra Lineal}} | 1 | 10 | — | MAT | [prog]({{...}}) |
| {{IIC1103}} | {{Introducción a la Programación}} | 1 | 10 | — | INF | [prog]({{...}}) |
| ... | | | | | | |

**Ramos prioritarios para Remy (que pasarán a Fase 3):**
- {{lista de códigos}}

---

### Medicina 🎯

**Facultad:** {{...}} · **Plan:** {{año}} · **Total ramos:** {{n}} · **Sede:** {{...}}
**URL malla:** [{{...}}]({{...}})

| Código | Nombre | Sem | Créditos | Pre-req | Área | URL programa |
|---|---|---|---|---|---|---|
| {{MED101}} | {{Anatomía I}} | 1 | 10 | — | MED | [prog]({{...}}) |
| {{MED102}} | {{Bioquímica}} | 1 | 8 | — | MED+QUI | [prog]({{...}}) |
| ... | | | | | | |

**Ramos prioritarios para Remy:**
- {{lista de códigos}}

---

### Ingeniería Comercial 🎯

**Facultad:** {{...}} · **Plan:** {{año}} · **Total ramos:** {{n}} · **Sede:** {{...}}
**URL malla:** [{{...}}]({{...}})

| Código | Nombre | Sem | Créditos | Pre-req | Área | URL programa |
|---|---|---|---|---|---|---|
| {{EAE110}} | {{Microeconomía I}} | 2 | 10 | — | ECO | [prog]({{...}}) |
| {{EAE210}} | {{Macroeconomía I}} | 3 | 10 | EAE110 | ECO | [prog]({{...}}) |
| ... | | | | | | |

**Ramos prioritarios para Remy:**
- {{lista de códigos}}

---

### Derecho 🎯

**Facultad:** {{...}} · **Plan:** {{año}} · **Total ramos:** {{n}} · **Sede:** {{...}}
**URL malla:** [{{...}}]({{...}})

| Código | Nombre | Sem | Créditos | Pre-req | Área | URL programa |
|---|---|---|---|---|---|---|
| {{DER101}} | {{Introducción al Derecho}} | 1 | 10 | — | JUR | [prog]({{...}}) |
| {{DER102}} | {{Derecho Romano}} | 1 | 6 | — | JUR+HUM | [prog]({{...}}) |
| ... | | | | | | |

**Ramos prioritarios para Remy:**
- {{lista de códigos}}

---

## Programas verificados

> Completar después de la **Fase 3**. Una sub-sección por ramo prioritario, con cita textual
> de contenidos. Sin cita verbatim, el ramo no entra acá — se queda con ⚠️ en la malla.

### {{CÓDIGO1}} — {{Nombre oficial}}

- **Carrera origen:** {{Ing. Civil / Medicina / Ing. Comercial / Derecho}}
- **URL programa:** [{{...}}]({{...}})
- **Año / vigencia del programa:** {{...}}
- **Pre-requisitos:** {{...}}
- **Descripción / objetivos** (cita textual):
  > "{{cita verbatim 2–4 líneas del programa oficial}}"
- **Contenidos por unidad** (cita textual o transcripción fiel):
  - **Unidad 1:** {{...}}
  - **Unidad 2:** {{...}}
  - **Unidad 3:** {{...}}
- **Bibliografía principal:**
  - {{Autor, Título, Editorial, Año}}
  - {{...}}
- **Mapeo a Remy:**
  - **Curso Remy:** {{nombre tentativo, ej. `calculo-multivariable`}}
  - **Encaje:** ✅ calce total / 🟡 calce parcial / ❌ es un curso nuevo

---

### {{CÓDIGO2}} — {{Nombre oficial}}

- ...

---

### Más ramos verificados aquí...

---

## Propuesta de catálogo Remy

> Completar después de la **Fase 4**. Cursos a producir o expandir, con capítulos derivados
> directamente de los contenidos verbatim citados arriba.

### Curso propuesto 1: {{nombre-tentativo-en-kebab-case}}

- **Área principal:** {{XXX}}
- **Estado en Remy:** ❌ Falta crear / 🟡 Existe pero falta expandir / ✅ Ya existe
- **Carreras (de las 4) que lo usan:** {{n}} ({{lista corta}})
- **Ramos universitarios que lo justifican:**
  * {{CÓDIGO}} — {{Nombre}}
  * {{CÓDIGO}} — {{Nombre}}
- **Capítulos propuestos** (derivados de contenidos verbatim de Programas Verificados):
  1. {{Capítulo 1}} — basado en Unidad 1 de {{CÓDIGO}}
  2. {{Capítulo 2}} — basado en Unidad 2 de {{CÓDIGO}}
  3. ...
- **Bibliografía base recomendada:**
  - {{Autor, Título}}
- **Prioridad sugerida:** 🔴 ALTA (≥3 carreras) / 🟡 MEDIA (2 carreras) / 🟢 BAJA (1 carrera)

---

### Curso propuesto 2: {{...}}

- ...

---

### Curso propuesto N: {{...}}

---

## Mapeo carrera → cursos Remy

> Tabla útil para producto: si un alumno se registra como estudiante de {{carrera}}, qué
> cursos de Remy (existentes ✅ o propuestos ❌) le sirven directamente.

| Carrera | Cursos Remy aplicables (orden de relevancia) |
|---|---|
| Ingeniería Civil — plan común | ✅ precalculo · ✅ calculo-diferencial · ✅ calculo-integral · ✅ algebra-lineal · ✅ calculo-multivariable · ✅ calculo-vectorial · ✅ ecuaciones-diferenciales · ❌ probabilidades-y-estadistica · ❌ intro-programacion-python · ❌ fisica-mecanica |
| Medicina | ✅ precalculo · ❌ quimica-general · ❌ biologia-celular · ❌ anatomia · ❌ fisiologia · ❌ bioquimica-medica |
| Ingeniería Comercial | ✅ precalculo · ✅ calculo-diferencial · ✅ calculo-integral · ✅ algebra-lineal *(parcial)* · ❌ microeconomia · ❌ macroeconomia · ❌ contabilidad-financiera · ❌ probabilidades-y-estadistica · ❌ intro-programacion-python |
| Derecho | ❌ intro-derecho · ❌ derecho-civil-1 · ❌ derecho-romano · ❌ derecho-constitucional |

---

## Verificación final

- [ ] Las 4 mallas (o las disponibles, según notas de reemplazo) están extraídas.
- [ ] Cada ramo en "Programas verificados" tiene cita textual de contenidos.
- [ ] Cada propuesta de curso Remy tiene capítulos derivados de contenidos verbatim.
- [ ] Una muestra de 5 URLs de programas se probó y sigue activa.
- [ ] No hay áreas `OTRO` sin justificar.
- [ ] La fecha de consulta está al inicio del archivo.
- [ ] No hay datos sin fuente trazable.

---

## Fuentes consultadas

> Completar al cerrar la **Fase 5**. Toda URL usada en este informe debe estar acá.

| URL | Descripción | Fecha consulta | Estado |
|---|---|---|---|
| {{https://...}} | {{Portal admisión}} | {{2026-04-28}} | ✅ Activa |
| {{https://...}} | {{Listado de carreras}} | {{2026-04-28}} | ✅ Activa |
| {{https://...}} | {{Malla Ing. Civil}} | {{2026-04-28}} | ✅ Activa |
| {{https://...}} | {{Malla Medicina}} | {{2026-04-28}} | ✅ Activa |
| {{https://...}} | {{Malla Ing. Comercial}} | {{2026-04-28}} | ✅ Activa |
| {{https://...}} | {{Malla Derecho}} | {{2026-04-28}} | ✅ Activa |
| {{https://...}} | {{Programa MAT1610}} | {{2026-04-28}} | ✅ Activa |
| {{https://.../prog.pdf}} | {{Programa EAE110, PDF guardado}} | {{2026-04-28}} | 📄 PDF |
| ... | | | |

**Estados posibles:** ✅ Activa / 📄 PDF descargado / ⚠️ Inestable / ❌ Caída.

---

## Observaciones y notas para el siguiente investigador

> Cualquier cosa útil para futuras investigaciones de esta misma universidad o como referencia
> para otras.

- {{ej. "El catálogo de cursos en `catalogo.<dominio>` requiere clic en cada ramo para abrir el
  programa, no hay vista batch."}}
- {{ej. "Los programas de Medicina están detrás de login institucional — los descargué con
  ayuda manual."}}
- ...

### Correcciones aplicadas (solo si esto es una curación)

> Solo aplica si este archivo se generó con el "Prompt de curación" de PROMPTS_COWORK.md.
> Listar las afirmaciones del archivo previo que se reemplazaron y el motivo.

- {{ej. "[MAT1620] — antes mapeado a `calculo-integral` → corregido a `calculo-multivariable`
  según programa oficial en catalogo.uc.cl/MAT1620 (cita: 'cálculo en varias variables...')."}}
- ...
