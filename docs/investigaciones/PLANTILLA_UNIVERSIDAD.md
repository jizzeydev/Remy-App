# {{NOMBRE_UNIVERSIDAD}} ({{SIGLA}})

> **Cómo usar esta plantilla:** copialá renombrándola como `<sigla>.md` (ej. `uc.md`, `uchile.md`)
> y completá las secciones a medida que avanzás los 7 pasos del [WORKFLOW.md](./WORKFLOW.md)
> con los [PROMPTS_COWORK.md](./PROMPTS_COWORK.md).

**Investigado por:** {{tu nombre}}
**Fecha de consulta:** {{YYYY-MM-DD}}
**Tiempo invertido:** {{horas}}
**Estado:** 🟢 Completo / 🟡 En progreso / 🔴 Bloqueado

---

## Datos institucionales

> Completar después del **Prompt 1**.

- **Nombre oficial:** {{nombre completo}}
- **Sigla:** {{SIGLA}}
- **Sitio oficial:** [{{dominio}}]({{URL}})
- **Sedes:** {{ciudad 1, ciudad 2, ...}}
- **Portal de admisión:** [{{URL}}]({{URL}})
- **Listado de carreras:** [{{URL}}]({{URL}})

---

## Facultades y escuelas

> Completar después del **Prompt 1**.

| Facultad / Escuela / Instituto | Área macro | URL |
|---|---|---|
| {{Facultad de Ingeniería}} | Ingeniería y Tecnología | [link]({{...}}) |
| {{Facultad de Medicina}} | Ciencias de la Salud | [link]({{...}}) |
| {{Facultad de Derecho}} | Derecho | [link]({{...}}) |
| {{Facultad de Economía y Negocios}} | Ciencias Económicas y Administración | [link]({{...}}) |
| {{Facultad de Ciencias Sociales}} | Ciencias Sociales | [link]({{...}}) |
| {{Facultad de Humanidades}} | Humanidades y Educación | [link]({{...}}) |
| {{Facultad de Arte / Arquitectura}} | Arte y Comunicaciones | [link]({{...}}) |
| {{Facultad de Ciencias}} | Ciencias Básicas | [link]({{...}}) |
| ... | | |

---

## Inventario de carreras

> Completar después del **Prompt 2** (sin prioridad) y agregar columna "Prioridad" después del **Prompt 3**.
> **Importante:** todas las carreras de pregrado, sin filtro.

| Carrera | Sede | Facultad | Área macro | Plan (año) | Duración | Grado | URL malla | Prioridad |
|---|---|---|---|---|---|---|---|---|
| {{Plan común Ingeniería}} | {{Santiago}} | {{Ingeniería}} | Ingeniería y Tecnología | {{2024}} | 12s | Lic + Prof | [link]({{...}}) | 🔴 |
| {{Medicina}} | {{Santiago}} | {{Medicina}} | Ciencias de la Salud | {{2024}} | 14s | Profesional | [link]({{...}}) | 🔴 |
| {{Derecho}} | {{Santiago}} | {{Derecho}} | Derecho | {{2024}} | 10s | Licenciatura | [link]({{...}}) | 🔴 |
| {{Ing. Comercial}} | {{Santiago}} | {{Economía}} | Cs. Económicas | {{2023}} | 10s | Profesional | [link]({{...}}) | 🔴 |
| {{Psicología}} | {{Santiago}} | {{Cs. Sociales}} | Ciencias Sociales | {{2024}} | 10s | Profesional | [link]({{...}}) | 🔴 |
| {{Enfermería}} | {{Santiago}} | {{Medicina}} | Ciencias de la Salud | {{2024}} | 10s | Profesional | [link]({{...}}) | 🟡 |
| {{Arquitectura}} | {{Santiago}} | {{Arquitectura}} | Arte y Comunicaciones | {{2023}} | 12s | Profesional | [link]({{...}}) | 🟡 |
| {{Periodismo}} | {{Santiago}} | {{Comunicación}} | Arte y Comunicaciones | {{2024}} | 8s | Profesional | [link]({{...}}) | 🟡 |
| {{Pedagogía Básica}} | {{Santiago}} | {{Educación}} | Humanidades y Educación | {{2024}} | 10s | Profesional | [link]({{...}}) | 🟡 |
| ... | | | | | | | | |

**Distribución por área macro:**

- Ingeniería y Tecnología: {{n}} carreras
- Ciencias Económicas y Administración: {{n}}
- Ciencias de la Salud: {{n}}
- Ciencias Sociales: {{n}}
- Derecho: {{n}}
- Humanidades y Educación: {{n}}
- Arte y Comunicaciones: {{n}}
- Ciencias Básicas: {{n}}
- **Total:** {{N}} carreras

**Notas:**

- ⚠️ {{cualquier observación sobre carreras con malla no encontrada o ambigüedades}}.

---

## Mallas extraídas

> Completar después del **Prompts 4 y 5**. Una sub-sección por carrera procesada (ALTA y MEDIA),
> y al final una sección con las BAJAS solo con lista de nombres.

### {{Plan común Ingeniería}} 🔴

**Facultad:** {{Ingeniería}} · **Plan:** {{2024}} · **Total ramos:** {{n}}
**URL malla:** [link]({{...}})

| Código | Nombre | Sem | Créditos | Pre-req | Área | Link programa | Contenidos |
|---|---|---|---|---|---|---|---|
| {{MAT1014}} | {{Cálculo I}} | 1 | 10 | — | MAT | [prog]({{...}}) | {{Límites, derivadas, integrales}} |
| {{MAT1024}} | {{Álgebra Lineal}} | 1 | 10 | — | MAT | [prog]({{...}}) | {{Vectores, matrices, autovalores}} |
| {{FIS1014}} | {{Mecánica}} | 2 | 10 | MAT1014 | FIS | [prog]({{...}}) | {{Cinemática, dinámica, energía}} |
| {{INF1014}} | {{Programación}} | 1 | 8 | — | INF | [prog]({{...}}) | {{Python, estructuras de datos básicas}} |
| ... | | | | | | | |

### {{Medicina}} 🔴

**Facultad:** {{Medicina}} · **Plan:** {{2024}} · **Total ramos:** {{n}}
**URL malla:** [link]({{...}})

| Código | Nombre | Sem | Créditos | Pre-req | Área | Link programa | Contenidos |
|---|---|---|---|---|---|---|---|
| {{MED1101}} | {{Anatomía I}} | 1 | 10 | — | MED | [prog]({{...}}) | {{Sistema musculoesquelético}} |
| {{MED1102}} | {{Histología}} | 1 | 6 | — | MED | [prog]({{...}}) | {{Tejidos epitelial, conectivo}} |
| {{MED1201}} | {{Bioquímica}} | 2 | 8 | — | MED+QUI | [prog]({{...}}) | {{Macromoléculas, metabolismo}} |
| {{MED1301}} | {{Fisiología}} | 3 | 10 | MED1101 | MED | [prog]({{...}}) | {{Sistemas de órganos}} |
| ... | | | | | | | |

### {{Derecho}} 🔴

**Facultad:** {{Derecho}} · **Plan:** {{2024}} · **Total ramos:** {{n}}
**URL malla:** [link]({{...}})

| Código | Nombre | Sem | Créditos | Pre-req | Área | Link programa | Contenidos |
|---|---|---|---|---|---|---|---|
| {{DER1101}} | {{Introducción al Derecho}} | 1 | 10 | — | JUR | [prog]({{...}}) | {{Conceptos básicos, fuentes}} |
| {{DER1102}} | {{Derecho Romano}} | 1 | 6 | — | JUR+HUM | [prog]({{...}}) | {{Origen del derecho civil}} |
| {{DER1201}} | {{Derecho Civil I}} | 2 | 10 | DER1101 | JUR | [prog]({{...}}) | {{Personas, bienes, hechos jurídicos}} |
| ... | | | | | | | |

### {{Ing. Comercial}} 🔴

| ... | | | | | | | |

### {{Psicología}} 🔴

| ... | | | | | | | |

### Más carreras ALTAS y MEDIAS aquí...

---

### Carreras de prioridad 🟢 BAJA — solo lista de ramos

#### {{Carrera}}
**Solapamiento con:** {{otra carrera ya procesada}}.
- {{Ramo 1}} (área: {{X}})
- {{Ramo 2}} (área: {{Y}})
- ...

---

## Agregación por área de conocimiento

> Completar después del **Prompt 6**. Una sub-sección por cada área con 5+ ramos.
> Ordenar por cantidad de ramos descendente.

### Área: Matemáticas (MAT)

**Total ramos únicos:** {{n}}
**Carreras donde aparecen:** {{n}}

**Top 10 ramos más frecuentes:**

| # | Código | Nombre | Carreras (cantidad) | Carreras (lista breve) |
|---|---|---|---|---|
| 1 | MAT1014 | Cálculo I | {{12}} | {{Plan común, Ing. Civil Mat, Lic. Mat, Ing. Comercial}} |
| 2 | MAT1024 | Álgebra Lineal | {{10}} | {{...}} |
| ... | | | | |

**Patrón temático observado:** {{descripción del currículum común}}.

### Área: Medicina y salud (MED)

**Total ramos únicos:** {{n}}
...

### Área: Derecho (JUR)

**Total ramos únicos:** {{n}}
...

### Área: Economía y finanzas (ECO)

...

### Área: Administración y gestión (ADM)

...

### Área: ... (todas las que tengan 5+ ramos)

---

### Áreas menores (menos de 5 ramos)

- **{{IDI}}**: {{n}} ramos. {{lista breve}}.
- **{{ART}}**: {{n}} ramos.
- ...

---

## Resumen ejecutivo

> Completar después del **Prompt 7**.

**Carreras procesadas:**

- 🔴 ALTA: {{n}} carreras.
- 🟡 MEDIA: {{n}} carreras.
- 🟢 BAJA: {{n}} carreras.
- **Total inventariadas:** {{N}} carreras.

**Ramos únicos identificados (deduplicados por código):** {{n}}

**Top 5 áreas con más ramos:**

| # | Área | Ramos únicos | % del total |
|---|---|---|---|
| 1 | {{MED}} | {{n}} | {{%}} |
| 2 | {{JUR}} | {{n}} | {{%}} |
| 3 | {{MAT}} | {{n}} | {{%}} |
| 4 | {{ECO}} | {{n}} | {{%}} |
| 5 | {{...}} | | |

**Carreras con más ramos únicos (no compartidos con otras):**

| Carrera | Ramos únicos |
|---|---|
| {{Medicina}} | {{n}} |
| {{Derecho}} | {{n}} |
| {{...}} | |

---

## Propuesta de catálogo Remy

> Completar después del **Prompt 7**. Cursos a producir o expandir, ordenados por demanda.

### Curso propuesto 1: {{Anatomía Humana}}

- **Área principal:** MED
- **Estado en Remy:** ❌ Falta crear
- **Carreras que lo usan:** {{8}} ({{Medicina, Enfermería, Kinesiología, Obstetricia, Tecnología Médica, Nutrición, Fonoaudiología, Odontología}})
- **Ramos universitarios que lo justifican:**
  * {{MED1101}} — Anatomía I
  * {{ENF1101}} — Anatomía Aplicada
  * {{KIN1101}} — Anatomía del Sistema Locomotor
- **Sub-temas a cubrir:**
  * Sistema musculoesquelético
  * Sistema nervioso
  * Sistema cardiovascular
  * Sistema digestivo / respiratorio / urinario
  * Sistema endocrino
- **Prioridad sugerida:** 🔴 ALTA

### Curso propuesto 2: {{Microeconomía}}

- **Área principal:** ECO
- **Estado en Remy:** ❌ Falta crear
- **Carreras que lo usan:** {{6}} ({{Ing. Comercial, Economía, Auditoría, Ing. Civil Industrial, Administración, Contador}})
- **Ramos universitarios que lo justifican:**
  * {{ECO1101}} — Microeconomía I
  * {{ECO1102}} — Microeconomía II
  * ...
- **Sub-temas a cubrir:**
  * Comportamiento del consumidor
  * Comportamiento del productor
  * Mercados competitivos
  * Externalidades
  * Equilibrio general
- **Prioridad sugerida:** 🔴 ALTA

### Curso propuesto 3: {{Introducción al Derecho}}

- **Área principal:** JUR
- **Estado en Remy:** ❌ Falta crear
- ...

### Curso propuesto 4: {{Probabilidad y Estadística}}

- **Área principal:** MAT
- **Estado en Remy:** 🟡 Existe pero falta expandir (no hay un curso dedicado, solo cap suelto)
- **Carreras que lo usan:** {{15+}} ({{prácticamente todas}})
- ...

### Curso propuesto N: {{...}}

...

---

## Mapeo carrera → cursos Remy

> Tabla útil para producto: si un alumno se registra como estudiante de {{carrera}}, qué cursos
> de Remy (existentes o propuestos) le sirven directamente.

| Carrera | Cursos Remy aplicables (orden de relevancia) |
|---|---|
| Plan común Ingeniería | precalculo (refuerzo), calculo-diferencial, algebra-lineal, calculo-integral, [propuesto] fisica-mecanica, [propuesto] programacion-introductoria |
| Ing. Civil Matemática | algebra-lineal, calculo-multivariable, calculo-vectorial, ecuaciones-diferenciales, [propuesto] variable-compleja, [propuesto] metodos-numericos |
| Ing. Comercial | precalculo, calculo-diferencial, algebra-lineal (parcial), [propuesto] microeconomia, [propuesto] macroeconomia, [propuesto] contabilidad-financiera, [propuesto] estadistica |
| Medicina | [propuesto] anatomia, [propuesto] fisiologia, [propuesto] bioquimica-medica, [propuesto] farmacologia, [propuesto] estadistica-medica |
| Derecho | [propuesto] intro-derecho, [propuesto] derecho-civil-1, [propuesto] derecho-romano, [propuesto] derecho-constitucional |
| Psicología | [propuesto] psicologia-general, [propuesto] estadistica-aplicada, [propuesto] psicobiologia |
| Enfermería | [propuesto] anatomia, [propuesto] fisiologia, [propuesto] farmacologia, [propuesto] estadistica-bioestadistica |
| Arquitectura | [propuesto] geometria-descriptiva, [propuesto] historia-arquitectura, [propuesto] estructuras-basicas |
| Periodismo | [propuesto] redaccion-periodistica, [propuesto] historia-de-medios, [propuesto] etica-comunicacional |
| Pedagogía Básica | [propuesto] didactica-general, [propuesto] curriculum, [propuesto] psicopedagogia |
| ... | |

---

## Verificación final

- [ ] Todos los links del inventario funcionan.
- [ ] Los ramos sin programa están marcados con ⚠️.
- [ ] Las áreas están bien asignadas (sin "OTRO" sin justificar).
- [ ] La fecha de consulta está al final.
- [ ] No hay datos sin fuente trazable.

---

## Fuentes consultadas

> Completar después del **Prompt 7**. Toda URL usada en este informe debe estar acá.

| URL | Descripción | Fecha consulta | Estado |
|---|---|---|---|
| {{https://...}} | {{Portal admisión}} | {{2026-04-27}} | ✅ Activa |
| {{https://...}} | {{Listado de facultades}} | {{2026-04-27}} | ✅ Activa |
| {{https://...}} | {{Malla Plan común Ingeniería}} | {{2026-04-27}} | ✅ Activa |
| {{https://...}} | {{Malla Medicina}} | {{2026-04-27}} | ✅ Activa |
| {{https://...}} | {{Malla Derecho}} | {{2026-04-27}} | ✅ Activa |
| {{https://...}} | {{Programa MAT1014}} | {{2026-04-27}} | ✅ Activa |
| {{https://.../malla.pdf}} | {{PDF descargado, guardado en docs/...}} | {{2026-04-27}} | 📄 PDF |
| ... | | | |

**Estados posibles:** ✅ Activa / 📄 PDF descargado / ⚠️ Inestable / ❌ Caída.

---

## Observaciones y notas para el siguiente investigador

> Cualquier cosa útil para futuras investigaciones de esta misma universidad o como referencia
> para otras.

- {{El sitio de la facultad de ingeniería tiene un buscador de programas en {{URL}} muy útil.}}
- {{Las mallas de Ciencias están en otro subdominio, no en el portal central.}}
- {{Cuidado con la cohorte 2020 que tiene plan distinto a la 2024.}}
- {{La facultad de Arte tiene mallas solo en PDF, hay que descargarlas una por una.}}
- {{...}}
