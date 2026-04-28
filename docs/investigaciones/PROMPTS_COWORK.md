# Prompt one-shot para Claude Cowork

Un único prompt que abarca todo el workflow de investigación de una universidad. Pegalo en una nueva conversación de Claude Cowork con la **extensión Claude in Chrome** activa, completando la sección "Datos de la universidad" de arriba.

Antes de pegarlo:

- Reemplazá los placeholders `{{...}}` en la sección **Datos de la universidad**.
- Si no conocés el dominio o la URL del listado de carreras, déjalos vacíos: Cowork los buscará al inicio.
- Tené abierto el archivo `docs/investigaciones/<sigla>.md` (copiá la [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) y renombrala) para ir pegando el output a medida que avanza.

---

## Prompt master

````
# Investigación de mallas curriculares — {{NOMBRE_UNIVERSIDAD}}

## Datos de la universidad
- **Nombre completo:** {{NOMBRE_UNIVERSIDAD}}
- **Sigla:** {{SIGLA}}
- **Dominio oficial sugerido:** {{DOMINIO_OFICIAL_O_VACIO}} (ej. `uchile.cl`, `uc.cl`, `usach.cl`)
- **URL del listado de carreras (si la conocés):** {{URL_LISTADO_CARRERAS_O_VACIO}}
- **Fuentes oficiales habituales para verificar / cruzar datos:**
  - Sitio raíz: `{{DOMINIO_OFICIAL_O_VACIO}}`
  - Portal de admisión / pregrado: típicamente `admision.<dominio>`, `pregrado.<dominio>`,
    `carreras.<dominio>` o sub-página dentro del sitio raíz.
  - Catálogo unificado de programas (algunas universidades tienen uno en `programas.<dominio>`
    o `catalogo.<dominio>`).
  - Mifuturo del Mineduc para datos cruzados de matrícula y empleabilidad: `mifuturo.cl`.
  - DEMRE para referencias de admisión: `demre.cl`.

## Contexto

Esto es para **Remy**, una webapp educativa para universitarios chilenos. El objetivo es construir
un mapa real de qué se enseña en la universidad chilena (TODAS las áreas: matemáticas, derecho,
medicina, comercial, psicología, arquitectura, etc.) para decidir qué cursos producir.

**Catálogo actual de Remy** (todo cubre solo área `MAT`):
- precalculo (8 caps)
- calculo-diferencial (3 caps), calculo-integral (3), calculo-multivariable (7), calculo-vectorial (3)
- algebra-lineal (8 caps)
- ecuaciones-diferenciales (4 caps)

Cualquier ramo fuera de matemáticas universitarias es un **gap esperable y deseado** de detectar.

## Herramientas

Tenés activa la **extensión Claude in Chrome** y permiso para operar la pestaña que abro al inicio.
Usala para navegar, leer DOM, seguir links, descargar PDFs. Si quedás atascado en un captcha,
modal de cookies o login, decime explícitamente y yo lo resuelvo manualmente para devolverte el
control.

## Reglas inviolables durante toda la investigación

1. **SOLO fuentes oficiales** del dominio `{{DOMINIO_OFICIAL_O_VACIO}}`, sus subdominios institucionales,
   `mifuturo.cl` y `demre.cl`. Nada de blogs, foros, Reddit, sitios de marketing externos
   (`carrerasunab.cl` ≠ `unab.cl`).
2. **Cada dato trazable** a una URL específica que reportes en la sección final "Fuentes consultadas".
3. **Anotar año del plan** de estudios cuando aparezca; si no aparece, marcalo con ⚠️.
4. **Si encontrás contradicciones** entre dos fuentes oficiales, mostrame ambas y explicá la diferencia.
5. **Para PDFs descargados**, anotá nombre del archivo y URL original.
6. **Español neutral** (sin voseo).
7. **NO filtres carreras por contenido** — TODAS las de pregrado se inventarían.
8. **Si una carrera no tiene malla pública**, marcala con ⚠️ y explicá por qué.

## Taxonomía de áreas (cada ramo se etiqueta con una)

| Código | Área | Ejemplos |
|---|---|---|
| MAT | Matemáticas | Cálculo, álgebra, EDOs, estadística, probabilidad |
| FIS | Física | Mecánica, electromagnetismo, termodinámica |
| QUI | Química | Química general, orgánica, fisicoquímica |
| BIO | Biología | Biología celular, genética, ecología |
| ECO | Economía y finanzas | Microeconomía, macro, finanzas, mercados |
| ADM | Administración y gestión | Estrategia, marketing, RRHH, operaciones |
| CTB | Contabilidad y auditoría | Contabilidad financiera, costos, tributaria |
| JUR | Derecho | Civil, penal, comercial, laboral, constitucional |
| MED | Medicina y salud | Anatomía, fisiología, patología, farmacología |
| PSI | Psicología | General, clínica, social, evolutiva |
| SOC | Ciencias sociales | Sociología, antropología, ciencia política |
| EDU | Educación y pedagogía | Didáctica, currículum, psicopedagogía |
| HUM | Humanidades | Historia, filosofía, literatura, ética, teología |
| COM | Comunicaciones | Periodismo, publicidad, RRPP, audiovisual |
| ART | Arte y diseño | Diseño gráfico, industrial, arquitectura, música |
| INF | Computación e informática | Programación, BD, redes, IA, ciberseguridad |
| ING | Ingeniería aplicada | Procesos, materiales, hidráulica, estructuras |
| IDI | Idiomas | Inglés técnico, segundo idioma |
| MET | Metodología e investigación | Metodología, tesis, seminario |
| OFG | Formación general / electivos | OFG, electivos transversales |
| PRA | Prácticas y trabajo aplicado | Práctica profesional, internado, taller integrador |

Si un ramo cubre dos áreas, usá `+` (ej. `MAT+ECO` para econometría). Si nada encaja, usá `OTRO`
y justificá brevemente.

## Áreas macro de carreras

Para clasificar carreras (no ramos): Ingeniería y Tecnología / Ciencias Económicas y Administración
/ Ciencias de la Salud / Ciencias Sociales / Derecho / Humanidades y Educación / Arte y
Comunicaciones / Ciencias Básicas.

## Lo que tenés que hacer (en orden, todo en esta misma conversación)

### Fase 1 — Setup y datos institucionales

1.1. Confirmá que la extensión Chrome está activa y podés navegar.
1.2. Identificá:
   - Nombre oficial completo, sigla, sitio oficial.
   - Sedes (lista de ciudades).
   - URL del portal de admisión / pregrado.
   - URL del listado completo de carreras (si la del placeholder no sirve, buscala vos).
   - Lista de **facultades, escuelas o institutos** que dictan pregrado, con su URL si existe,
     clasificadas por área macro.

### Fase 2 — Inventario completo de carreras

Listá TODAS las carreras de pregrado de la universidad, sin filtrar por contenido.

Por cada carrera registrá: Nombre · Sede · Facultad · Área macro · Plan (año) · Duración ·
Grado · URL de la malla.

Reglas:
- Si una carrera tiene varias sedes con mallas distintas, **filas separadas**.
- Si tiene varios grados (licenciatura + profesional), **una fila por cada uno**.
- Si no encontrás malla pública, marcala con ⚠️.

Al final de esta fase, decime cuántas carreras totales hay y la distribución por área macro.

### Fase 3 — Priorización

Marcá cada carrera con prioridad:

- 🔴 **ALTA** — extraer detalle COMPLETO. Aplica a:
  * Carreras de alta matrícula nacional (medicina, derecho, ing. comercial, ing. civil
    industrial, psicología, enfermería, kinesiología, pedagogía básica).
  * Plan común de Ingeniería / Bachillerato.
  * **Al menos UNA carrera por cada área macro** (para tener cobertura panorámica temprana).

- 🟡 **MEDIA** — extraer detalle COMPLETO, refiriendo a otras donde se repiten ramos.
  * Otras ingenierías, otras carreras de salud, otras económicas, ciencias sociales,
    pedagogías por mención, licenciaturas, comunicaciones, arquitectura/diseño.

- 🟢 **BAJA** — solo lista de ramos por nombre, sin código ni programa.
  * Carreras muy específicas, segundas menciones, arte/música/danza con mallas muy de oficio.

### Fase 4 — Extracción de mallas (ALTAS y MEDIAS)

Por cada carrera ALTA y MEDIA, extraé TODOS los ramos del plan en una tabla:

| Código | Nombre | Sem | Créditos | Pre-req | Área | Link programa | Contenidos |

Reglas:
- TODOS los ramos van, incluyendo electivos obligatorios, formación general, prácticas y tesis.
- Para prácticas/tesis/talleres usá área `PRA`. Para OFG usá `OFG`. Contenidos pueden quedar vacíos.
- Si abrís el programa oficial del ramo, extraé contenidos en 1-2 líneas. Si no hay programa, ⚠️.
- Si dos carreras comparten el mismo código, NO repitas la fila — agregá la segunda carrera a una
  columna adicional "Carreras" o anotalo en la fila existente.
- Estandarizá formato de códigos.

Para las BAJAS, capturá solo:
- Nombre de la carrera.
- Lista de ramos (nombres con su área entre paréntesis).
- Solapamiento con otra carrera ya procesada (si aplica).

**IMPORTANTE — control de tamaño del output:**
Si hay más de 6 carreras ALTAS o más de 10 MEDIAS, dividí el procesamiento en **lotes de 3-5
carreras** y pausá entre lotes para que yo confirme antes de seguir. Avisame al iniciar cada lote.

### Fase 5 — Agregación por área de conocimiento

Una vez extraídas todas las mallas, agregá los ramos por área. Por cada área con 5+ ramos únicos:

- Total de ramos únicos en esa área.
- Cantidad de carreras donde aparecen.
- **Top 10 ramos más frecuentes** (los que aparecen en más carreras), con código, nombre,
  cantidad de carreras y lista breve.
- **Patrón temático observado**: descripción del currículum común.
- Ejemplos representativos adicionales.

Ordená las áreas de mayor a menor cantidad de ramos.

### Fase 6 — Propuesta de catálogo Remy

A partir de la agregación anterior, proponé qué cursos vale la pena armar en Remy. Ordenalos
por demanda (cuántas carreras los necesitan).

Por cada curso propuesto:
- **Nombre tentativo**.
- **Área principal** (de la taxonomía).
- **Estado en Remy:** ✅ ya existe / 🟡 existe pero falta expandir / ❌ falta crear.
- **Carreras que lo usan** (cantidad + lista breve).
- **Ramos universitarios que lo justifican** (códigos + nombres, máximo 5 ejemplos).
- **Sub-temas a cubrir** (basado en contenidos extraídos).
- **Prioridad sugerida** (🔴/🟡/🟢 según demanda).

### Fase 7 — Mapeo carrera → cursos Remy

Tabla para producto: por cada carrera procesada (ALTA + MEDIA), qué cursos de Remy
(existentes o propuestos) le sirven directamente.

| Carrera | Cursos Remy aplicables (orden de relevancia) |

### Fase 8 — Verificación final y fuentes

- [ ] Probá una muestra de links del inventario para confirmar que siguen activos.
- [ ] Los ramos sin programa están marcados con ⚠️.
- [ ] Las áreas están bien asignadas (sin `OTRO` sin justificar).
- [ ] No hay datos sin fuente trazable.

Cerrá con la tabla **Fuentes consultadas**:

| URL | Descripción | Fecha consulta | Estado |

Estados: ✅ Activa / 📄 PDF descargado / ⚠️ Inestable / ❌ Caída.

## Formato del output

Devolvé el contenido en **Markdown** estructurado en las secciones de la plantilla
[PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md) — listo para que yo lo pegue en
`docs/investigaciones/{{SIGLA}}.md`.

Estructura esperada de tu output, en este orden:

1. ## Datos institucionales
2. ## Facultades y escuelas
3. ## Inventario de carreras (con columna Prioridad)
4. ## Mallas extraídas (sub-secciones por carrera)
5. ## Agregación por área de conocimiento
6. ## Resumen ejecutivo
7. ## Propuesta de catálogo Remy
8. ## Mapeo carrera → cursos Remy
9. ## Verificación final
10. ## Fuentes consultadas
11. ## Observaciones (notas para futuras investigaciones)

## Cómo trabajar conmigo

- **Pausá entre fases largas.** Si una fase produce un output extenso, terminala y esperá mi
  confirmación con "ok, sigamos" antes de pasar a la siguiente.
- **Si algo te bloquea**, decime explícitamente qué pasó (sitio caído, captcha, requiere login)
  y proponé una alternativa.
- **No inventes datos.** Si un campo no está disponible, déjalo vacío con ⚠️ y nota.
- **Mostrá tu progreso** al inicio de cada fase: "Fase 4 de 8 — Extracción ALTAS, lote 1/3
  (carreras X, Y, Z)".

¿Confirmás que la extensión Chrome está activa y podés empezar con la Fase 1?
````

---

## Prompts auxiliares (usar solo si hay imprevistos)

Estos NO son parte del flujo principal. Usalos si Cowork queda atascado o necesitás ajustar algo en medio.

### Si Cowork se atasca en un sitio

```
La extensión parece estar bloqueada en {{descripción}}. Te paso el control manualmente para que
yo resuelva {{captcha / cookies / login}}, después te devuelvo la pestaña. Esperá mi confirmación.
```

### Si hay duda sobre qué malla es la vigente

```
Encontraste dos mallas para la carrera {{X}}: {{URL1}} (cohorte {{año1}}) y {{URL2}} (cohorte {{año2}}).
Usá la más reciente que esté marcada como "vigente" o "actualizada" en el sitio. Confirmame antes de continuar.
```

### Si una facultad entera tiene problemas

```
La facultad de {{X}} tiene su sitio caído / con paywall / sin información pública de mallas.
Marcá todas sus carreras con ⚠️ "sin acceso a malla" en el inventario y seguí con las otras
facultades. Reportalo en la sección "Observaciones" del informe.
```

### Para refrescar contexto a mitad de conversación

```
Recordatorio del estado:
- Universidad: {{NOMBRE}} ({{SIGLA}}).
- Estamos en la Fase {{N}} del prompt master.
- Carreras procesadas: {{lista}}.
- Áreas macro cubiertas: {{lista}}.
- Pendientes: {{lista}}.
- Sigamos con {{próxima acción concreta}}.
```

### Para acelerar dividiendo en sesiones distintas

Si la universidad es muy grande (50+ carreras) y la conversación se hace lenta, **abrí una segunda
conversación** y pasá este resumen como contexto inicial:

```
Estoy investigando {{NOMBRE_UNIVERSIDAD}} ({{SIGLA}}). En una conversación anterior procesé:
- Datos institucionales y facultades: ✅
- Inventario completo: ✅ ({{N}} carreras, {{distribución por área}})
- Priorización: ✅
- Carreras ALTAS procesadas: {{lista}}
- Carreras MEDIAS procesadas: {{lista parcial}}

Te paso el archivo {{SIGLA}}.md con todo lo capturado hasta ahora. Continuá desde {{punto exacto}}
siguiendo las mismas reglas, taxonomía y formato del prompt master original.

[adjuntar contenido del archivo MD]
```
