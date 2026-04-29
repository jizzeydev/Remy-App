# Prompts para Claude Cowork

Tres prompts:

1. **Prompt master** — para investigar una universidad nueva en una sola conversación.
2. **Prompt de curación** — para revisar y corregir una investigación ya hecha (ej. el primer pase de PUC quedó con errores en los códigos de ramos).
3. **Prompts auxiliares** — para destrabar imprevistos.

Antes de pegar cualquiera:

- Reemplazá los placeholders `{{...}}`.
- Tené abierto el archivo `docs/investigaciones/<sigla>.md` (copiá la [PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md)) para ir pegando el output a medida que avanza.
- Asegurate de que la **extensión Claude in Chrome** esté activa.

---

## 1. Prompt master (investigación nueva)

````
# Investigación de mallas curriculares — {{NOMBRE_UNIVERSIDAD}}

## Datos de la universidad

- **Nombre completo:** {{NOMBRE_UNIVERSIDAD}}
- **Sigla:** {{SIGLA}}
- **Dominio oficial sugerido:** {{DOMINIO_OFICIAL_O_VACIO}} (ej. `uchile.cl`, `uc.cl`, `usach.cl`)
- **URL del listado de carreras (si la conocés):** {{URL_LISTADO_CARRERAS_O_VACIO}}
- **Notas de reemplazo de carreras:** {{NOTAS_DE_REEMPLAZO_DE_CARRERAS}}
  (Ej.: "UTFSM no dicta Medicina ni Derecho — reemplazar por nota explicando el skip.
   UAI no dicta Medicina — reemplazar por Enfermería o nota.")

Fuentes oficiales habituales para verificar:
- Sitio raíz: `{{DOMINIO_OFICIAL_O_VACIO}}`
- Portal de admisión / pregrado: típicamente `admision.<dominio>` o `pregrado.<dominio>`.
- Catálogo de cursos / programas: típicamente `catalogo.<dominio>` o sub-página de la facultad.
- Mifuturo del Mineduc para datos cruzados de matrícula: `mifuturo.cl`.
- DEMRE para referencias de admisión: `demre.cl`.

## Contexto

Esto es para **Remy**, una webapp educativa para universitarios chilenos. El objetivo es construir
cursos. Para no inventar contenidos, necesito el **programa oficial** de cada ramo prioritario
(no solo la malla con códigos).

**Catálogo actual de Remy** (todo área `MAT`):
- precalculo (8 caps)
- calculo-diferencial (3 caps), calculo-integral (3), calculo-multivariable (7), calculo-vectorial (3)
- algebra-lineal (8 caps)
- ecuaciones-diferenciales (4 caps)

Cualquier ramo fuera de matemáticas universitarias es un **gap esperable** que tu propuesta
de catálogo Remy debe identificar.

## Carreras a investigar (exactamente 4)

Investigá SOLO estas cuatro. NO inventaríes otras carreras.

1. **Ingeniería Civil — plan común** (o equivalente: Ing. Civil Industrial, base de las civiles).
2. **Medicina**.
3. **Ingeniería Comercial** (o equivalente: Administración, Negocios).
4. **Derecho**.

Si la universidad NO dicta alguna, anotalo en la sección "Notas de reemplazo" del informe y
seguí con las que sí dicta. No la sustituyas por iniciativa propia salvo que las "Notas de
reemplazo" arriba lo indiquen.

## Herramientas

Tenés activa la **extensión Claude in Chrome** y permiso para operar la pestaña que abro al inicio.
Usala para navegar, leer DOM, seguir links, descargar PDFs. Si quedás atascado en un captcha,
modal de cookies o login, decime explícitamente y yo lo resuelvo manualmente.

## Reglas inviolables

1. **SOLO fuentes oficiales** del dominio `{{DOMINIO_OFICIAL_O_VACIO}}` y sus subdominios
   institucionales, más `mifuturo.cl` y `demre.cl`. Nada de blogs, foros, Reddit, sitios externos
   de marketing.
2. **Cada dato trazable a una URL específica** que reportes en la tabla "Fuentes consultadas".
3. **Anotar año del plan** de estudios cuando aparezca; si no aparece, marcalo con ⚠️.
4. **Para PDFs descargados**, anotá nombre del archivo y URL original.
5. **Español neutral** (sin voseo).
6. **Si una carrera no tiene malla pública**, marcala con ⚠️ y explicá por qué; no la inventes.
7. **REGLA CENTRAL — NO etiquetar contenidos por nombre del ramo.** Para cualquier ramo que
   pongas en la sección "Programas verificados", abrí su programa oficial (PDF o página del
   catálogo) y **citá texto verbatim** de los contenidos por unidad y la bibliografía. Si el
   programa no está disponible, marcá el ramo con ⚠️ y NO lo uses para proponer un curso Remy.

   *Ejemplo del error que esto previene:* en una investigación previa el modelo asignó
   "MAT1620 — Cálculo II" de PUC al curso `calculo-integral` porque "II ≈ integral". El programa
   oficial dice claramente que MAT1620 es **cálculo en varias variables**; en PUC, integral y
   diferencial van juntos en MAT1610 y MAT1630 es cálculo vectorial. Sin abrir el programa, no
   se puede mapear.

## Taxonomía de áreas (cada ramo se etiqueta con una)

| Código | Área | Ejemplos |
|---|---|---|
| MAT | Matemáticas | Cálculo, álgebra, EDOs, estadística, probabilidad |
| FIS | Física | Mecánica, electromagnetismo, termodinámica |
| QUI | Química | Química general, orgánica |
| BIO | Biología | Biología celular, genética |
| ECO | Economía y finanzas | Microeconomía, macro, finanzas |
| ADM | Administración y gestión | Estrategia, marketing, RRHH, operaciones |
| CTB | Contabilidad y auditoría | Contabilidad financiera, costos |
| JUR | Derecho | Civil, penal, comercial, constitucional |
| MED | Medicina y salud | Anatomía, fisiología, farmacología |
| INF | Computación e informática | Programación, BD, redes |
| ING | Ingeniería aplicada | Procesos, materiales, hidráulica, estructuras |
| HUM | Humanidades | Historia, filosofía, ética |
| MET | Metodología e investigación | Metodología, tesis, seminario |
| OFG | Formación general / electivos | OFG, electivos transversales |
| PRA | Prácticas y trabajo aplicado | Práctica profesional, internado |

Si un ramo cubre dos áreas, usá `+` (ej. `MAT+ECO` para econometría). Si nada encaja, `OTRO`
con justificación breve.

## Lo que tenés que hacer (5 fases, todo en esta misma conversación)

### Fase 1 — Setup y datos institucionales (5 min)

1.1. Confirmá que la extensión Chrome está activa y podés navegar.
1.2. Identificá:
   - Nombre oficial completo, sigla, sitio oficial.
   - Sedes / campus (lista corta).
   - URL del portal de admisión / pregrado.
   - URL del listado de carreras y URL del catálogo de cursos / programas.
   - Para cada una de las 4 carreras objetivo: URL exacta de la malla vigente y año del plan.

Si alguna carrera de las 4 no se dicta, anotalo y seguí.

### Fase 2 — Mallas de las 4 carreras objetivo (30–45 min)

Por cada carrera (Ing. Civil/plan común, Medicina, Ing. Comercial, Derecho), extraé TODOS los
ramos del plan en una tabla compacta:

| Código | Nombre | Sem | Créditos | Pre-req | Área | URL programa |

Reglas:
- TODOS los ramos van, incluyendo electivos obligatorios, formación general, prácticas y tesis.
- Para prácticas/tesis/talleres usá área `PRA`. Para OFG usá `OFG`.
- Estandarizá el formato de códigos.
- Si no hay programa oficial linkeable para un ramo, dejá la columna "URL programa" con ⚠️.
- En esta fase NO incluyas contenidos. Solo el código, nombre, semestre, créditos, prerequisito,
  área y URL del programa.

Al cerrar Fase 2, dame:
- Conteo total de ramos por carrera.
- Lista de los ramos que vas a llevar a la Fase 3 (los "prioritarios para Remy").

### Fase 3 — Programas verificados de los ramos prioritarios (45–75 min)

Definición de "ramo prioritario para Remy" (los que merecen abrir el programa oficial):

- **Todo ramo del área `MAT`** que aparezca en cualquiera de las 4 carreras (cálculo,
  álgebra, probabilidades, estadística, EDOs).
- **Todo ramo del área `FIS`, `QUI`, `BIO` con calidad de "intro universitaria"** (mecánica,
  electromag, química general, química orgánica intro, biología celular intro).
- **Todo ramo del área `INF`** que sea introductorio (intro a la programación, estructuras
  de datos básicas).
- **Microeconomía + Macroeconomía intro** (`ECO`), **Contabilidad financiera intro** (`CTB`),
  **Estrategia / Marketing intro** (`ADM`) — los que aparezcan en Ing. Comercial.
- **Anatomía intro, Fisiología intro, Bioquímica intro, Histología intro, Embriología,
  Farmacología intro** (`MED`) — los que aparezcan en Medicina.
- **Introducción al Derecho, Derecho Civil I, Derecho Romano, Derecho Constitucional intro,
  Derecho Penal I** (`JUR`) — los que aparezcan en Derecho.

Excluí (NO abras programa) ramos avanzados muy verticales (ej. *Patología Hepática Avanzada*,
*Derecho Procesal Tributario*), prácticas, tesis, OFG y electivos sin obligatoriedad.

Para CADA ramo prioritario, hacé esto:

1. Navegá a la URL del programa oficial (página del catálogo o PDF descargable).
2. Extraé los siguientes campos:

```
**{{CÓDIGO}} — {{Nombre oficial}}** (Carrera origen: {{...}})
- URL programa: {{...}}
- Año / vigencia del programa: {{...}} (si no aparece, ⚠️)
- Pre-requisitos: {{...}}
- Descripción / objetivos (cita textual, 2–4 líneas):
  > "{{cita verbatim}}"
- Contenidos por unidad (cita textual o transcripción fiel):
  - Unidad 1: {{...}}
  - Unidad 2: {{...}}
  - ...
- Bibliografía principal (si el programa la lista):
  - {{Autor, Título, Año}}
  - ...
- Mapeo a Remy (sugerido):
  - Curso Remy actual o propuesto: {{nombre tentativo}}
  - Encaje: {{calce total / parcial / es un curso nuevo}}
```

Reglas:
- **Las citas textuales son obligatorias.** Si no podés citar verbatim los contenidos
  (porque el programa no los publica en texto plano), marcá el ramo con ⚠️ y NO lo uses para
  proponer un curso Remy.
- Si dos carreras comparten el mismo ramo (mismo código), procesalo UNA sola vez y anotá las
  carreras de origen.
- Si un ramo cambió de código entre cohortes, usá la versión vigente y anotá la anterior.

**Control de tamaño:** procesá los ramos prioritarios de a lotes de 5–7 y pausá entre lotes
para que yo confirme con "ok, sigamos". Avisame al iniciar cada lote qué ramos vas a procesar.

### Fase 4 — Propuesta de catálogo Remy (15 min)

A partir de los programas verificados de la Fase 3, proponé qué cursos vale la pena armar en
Remy. Por cada curso propuesto:

- **Nombre tentativo** (slug en kebab-case, ej. `probabilidades-y-estadistica`).
- **Área principal** (de la taxonomía).
- **Estado en Remy:** ✅ ya existe / 🟡 existe pero falta expandir / ❌ falta crear.
- **Carreras que lo usan** (de las 4 investigadas; cantidad + lista).
- **Ramos universitarios que lo justifican** (códigos + nombres, máximo 5 ejemplos).
- **Capítulos propuestos** — derivados DIRECTAMENTE de los contenidos por unidad citados en
  Fase 3. Usá las unidades del programa oficial como base de los capítulos. NO inventes
  capítulos sin un contenido verbatim que los respalde.
- **Bibliografía base recomendada** — la del programa oficial, máximo 3 títulos.
- **Prioridad sugerida** (🔴 ALTA si lo usan ≥3 carreras de las 4 / 🟡 MEDIA si 2 / 🟢 BAJA si 1).

### Fase 5 — Mapeo carrera → cursos Remy + verificación final + fuentes (15 min)

5.1. Mapeo (tabla):

| Carrera | Cursos Remy aplicables (orden de relevancia) |

5.2. Verificación final:
- [ ] Probá una muestra de 5 URLs de programas — confirmá que siguen activas.
- [ ] Cada ramo de la Fase 3 tiene cita textual de contenidos.
- [ ] No hay áreas `OTRO` sin justificar.
- [ ] No hay propuestas de capítulos Remy sin un contenido verbatim que las respalde.

5.3. Tabla de fuentes consultadas:

| URL | Descripción | Fecha consulta | Estado |

Estados: ✅ Activa / 📄 PDF descargado / ⚠️ Inestable / ❌ Caída.

## Formato del output

Devolvé el contenido en **Markdown** estructurado en las secciones de la plantilla
[PLANTILLA_UNIVERSIDAD.md](./PLANTILLA_UNIVERSIDAD.md).

Estructura esperada del output, en este orden:

1. ## Datos institucionales
2. ## Las 4 carreras objetivo (sub-sección por carrera con su tabla de malla)
3. ## Programas verificados (sub-sección por ramo prioritario, con cita textual)
4. ## Propuesta de catálogo Remy
5. ## Mapeo carrera → cursos Remy
6. ## Verificación final
7. ## Fuentes consultadas
8. ## Observaciones (notas para futuras investigaciones)

## Cómo trabajar conmigo

- **Pausá entre fases.** Esperá mi "ok, sigamos" antes de pasar a la siguiente.
- **Si algo te bloquea**, decime explícitamente qué pasó (sitio caído, captcha, login) y proponé
  una alternativa. No avances inventando.
- **No inventes datos.** Si un campo no está disponible, déjalo vacío con ⚠️ y nota.
- **Mostrá tu progreso** al inicio de cada fase: "Fase 3 de 5 — Programas verificados, lote 2/4
  (ramos X, Y, Z)".

¿Confirmás que la extensión Chrome está activa y podés empezar con la Fase 1?
````

---

## 2. Prompt de curación (arreglar una investigación vieja)

Para una investigación que ya existe (ej. `PUC.md`) y que se hizo con la versión anterior del
workflow. Este prompt produce una **versión corregida** del archivo, recortada a las 4 carreras
objetivo y con los programas verificados al estilo Fase 3.

````
# Curación de investigación previa — {{SIGLA}}

## Contexto

Tengo el archivo `docs/investigaciones/{{SIGLA}}.md` con una investigación de mallas que se
hizo con la versión anterior del workflow. La investigación cubría TODAS las carreras de la
universidad y agregó datos sin verificar el programa oficial de cada ramo.

Necesito **curarla** y reducirla a la nueva forma:

- Solo las **4 carreras de mayor demanda**: Ingeniería Civil (plan común o equivalente),
  Medicina, Ingeniería Comercial, Derecho.
- Para los ramos prioritarios para Remy, **abrir el programa oficial y citar verbatim** los
  contenidos por unidad y la bibliografía.
- Reemplazar mapeos hechos por nombre con mapeos hechos por contenido real.

## Errores conocidos a corregir

Documento aquí los que ya detectamos. **Buscalos primero, arreglalos antes de seguir.**

1. **Cálculos de PUC mal mapeados.** En el archivo aparece:
   - `calculo-integral → MAT1620` ❌. **Corrección:** MAT1620 es *Cálculo II = Cálculo en
     varias variables (multivariable)*. En PUC, el cálculo integral va junto con el
     diferencial dentro de **MAT1610 — Cálculo I**.
   - `calculo-multivariable → MAT1630` ❌. **Corrección:** MAT1630 es *Cálculo III =
     Cálculo Vectorial*.
   - `calculo-vectorial → "parte de MAT1630 + cursos avanzados"` ❌. **Corrección:**
     calculo-vectorial mapea directamente a MAT1630.
   - El mapeo correcto en PUC es:
     * `precalculo` → preparatorio para MAT1610.
     * `calculo-diferencial` → contenido parcial de MAT1610 (la mitad diferencial).
     * `calculo-integral` → contenido parcial de MAT1610 (la mitad integral).
     * `calculo-multivariable` → MAT1620.
     * `calculo-vectorial` → MAT1630.
     * `ecuaciones-diferenciales` → MAT1640.
     * `algebra-lineal` → MAT1203 (o MAT1279 en su versión "introducción al álgebra lineal").
   - Verificá lo anterior abriendo cada programa oficial en `catalogo.uc.cl` y citando
     contenidos verbatim antes de aceptar el mapeo.

2. **Cualquier otro mapeo del archivo donde el código del ramo se asignó a un curso Remy
   sin haber abierto el programa oficial.** Tratalos como sospechosos y verificá.

## Lo que tenés que hacer

### Paso 1 — Leer el archivo actual

Abrí `docs/investigaciones/{{SIGLA}}.md` (te lo paso adjunto al final del prompt).
Inventariá:
- Qué carreras de las 4 objetivo ya están cubiertas (al menos parcialmente).
- Qué ramos del área MAT, FIS, QUI, BIO, INF, ECO, MED, JUR ya tienen alguna data extraída.
- Qué afirmaciones tienen URL trazable y cuáles no.

### Paso 2 — Acotar al alcance nuevo

Recortá mentalmente todo lo que NO sea una de las 4 carreras objetivo. Eso queda fuera de la
versión curada (lo guardamos como "anexo histórico" si querés, pero no es lo principal).

Para las 4 carreras objetivo, conservá la malla extraída (la lista de códigos + nombres +
semestres) si parece correcta. Si dudás, re-extraela del sitio oficial.

### Paso 3 — Verificar y corregir cada ramo prioritario

Para cada ramo prioritario (definición igual a Fase 3 del prompt master) que aparezca en la
malla de cualquiera de las 4 carreras:

1. Navegá al programa oficial.
2. Extraé el bloque de "programa verificado" (formato igual a Fase 3 del prompt master):

```
**{{CÓDIGO}} — {{Nombre oficial}}** (Carrera origen: {{...}})
- URL programa: {{...}}
- Año / vigencia del programa: {{...}}
- Pre-requisitos: {{...}}
- Descripción / objetivos (cita textual):
  > "{{cita verbatim}}"
- Contenidos por unidad (cita textual o transcripción fiel):
  - Unidad 1: {{...}}
  - Unidad 2: {{...}}
- Bibliografía principal:
  - {{Autor, Título, Año}}
- Mapeo a Remy (sugerido):
  - Curso Remy: {{nombre}}
  - Encaje: {{calce total / parcial / curso nuevo}}
```

3. Si el archivo previo afirmaba algo que no se sostiene contra el programa oficial,
   anotalo en una sub-sección **"Correcciones aplicadas"** dentro de Observaciones, con la
   forma:
   `- [ramo] — afirmación previa → corrección verificada → URL fuente.`

### Paso 4 — Reescribir Propuesta de catálogo Remy

Con los programas verificados, **reescribí la sección "Propuesta de catálogo Remy"** del
archivo. Para cada curso propuesto:
- Capítulos derivados de las unidades verbatim citadas en Paso 3.
- Bibliografía base de los programas verificados.
- Carreras (de las 4) que lo justifican.

Eliminá las propuestas viejas que no tengan respaldo en un programa verificado.

### Paso 5 — Reescribir Mapeo carrera → cursos Remy

Reescribí esa tabla usando solo los cursos sobrevivientes del Paso 4, con los códigos
correctos de la universidad.

### Paso 6 — Output

Devolvé el contenido **completo del archivo curado** en Markdown, listo para reemplazar al
actual. Estructura:

1. ## Datos institucionales
2. ## Las 4 carreras objetivo (sub-sección por carrera)
3. ## Programas verificados
4. ## Propuesta de catálogo Remy
5. ## Mapeo carrera → cursos Remy
6. ## Verificación final
7. ## Fuentes consultadas
8. ## Observaciones — incluí la sub-sección "Correcciones aplicadas".

Si el archivo previo tenía una sección de inventario panorámico de TODAS las carreras de la
universidad, NO la incluyas en la versión curada (queda fuera del nuevo alcance).

## Reglas inviolables

Las mismas del prompt master:
1. Solo fuentes oficiales (`*.{{DOMINIO}}` + mifuturo + DEMRE).
2. Cada dato trazable a una URL.
3. Citas verbatim obligatorias para cualquier ramo en "Programas verificados".
4. Si no se puede verificar un programa, ⚠️ y NO usarlo para proponer curso.
5. Español neutral.

## Cómo trabajar conmigo

- Empezá listándome qué carreras de las 4 ya están cubiertas en el archivo y cuáles faltan
  (re-extraer su malla).
- Procesá los ramos prioritarios en lotes de 5–7. Pausá entre lotes con "ok, sigamos".
- Mostrá las correcciones a medida que las encuentres, no solo al final.

Adjunto el archivo `{{SIGLA}}.md` actual:

[PEGAR ACÁ EL CONTENIDO COMPLETO DEL ARCHIVO]
````

---

## 3. Prompts auxiliares (usar solo si hay imprevistos)

Estos NO son parte del flujo principal. Usalos si Cowork queda atascado o necesitás ajustar algo
en medio.

### Si Cowork se atasca en un sitio

```
La extensión parece estar bloqueada en {{descripción}}. Te paso el control manualmente para que
yo resuelva {{captcha / cookies / login}}, después te devuelvo la pestaña. Esperá mi confirmación.
```

### Si hay duda sobre qué malla es la vigente

```
Encontraste dos mallas para la carrera {{X}}: {{URL1}} (cohorte {{año1}}) y {{URL2}}
(cohorte {{año2}}). Usá la más reciente que esté marcada como "vigente" o "actualizada" en
el sitio oficial. Confirmame antes de continuar.
```

### Si una carrera objetivo no se dicta en esta universidad

```
La universidad no dicta {{carrera}}. Anotalo en la sección "Notas de reemplazo" del informe
con la URL donde verificaste la ausencia, y seguí con las 3 carreras restantes. NO la
sustituyas por iniciativa propia.
```

### Si el programa oficial de un ramo no está disponible

```
El programa de {{CÓDIGO — Nombre}} no está públicamente disponible en {{URL intentada}}.
Marcalo con ⚠️ "sin programa público" en la sección "Programas verificados", anotá las URLs
donde buscaste y NO uses ese ramo para proponer un curso Remy. Seguí con el siguiente.
```

### Para refrescar contexto a mitad de conversación

```
Recordatorio del estado:
- Universidad: {{NOMBRE}} ({{SIGLA}}).
- Estamos en la Fase {{N}} del prompt master.
- Carreras procesadas: {{lista}}.
- Ramos prioritarios procesados en Fase 3: {{lista}}.
- Pendientes: {{lista}}.
- Sigamos con {{próxima acción concreta}}.
```

### Para acelerar dividiendo en sesiones distintas

Si la conversación se hace lenta (>2.5 hrs), abrí una segunda y pasá este resumen como contexto:

```
Estoy investigando {{NOMBRE_UNIVERSIDAD}} ({{SIGLA}}) con la nueva versión del workflow
(4 carreras objetivo + programas verificados). En una conversación anterior procesé:
- Datos institucionales: ✅
- Mallas de las 4 carreras: ✅ ({{detalle}})
- Programas verificados: ✅ parcial ({{lista de ramos ya hechos}})
- Pendientes: {{lista de ramos a verificar}}.

Te paso el archivo {{SIGLA}}.md con todo lo capturado. Continuá desde {{punto exacto}}
siguiendo las reglas del prompt master original (incluyendo cita verbatim de contenidos para
cada ramo en Fase 3).

[adjuntar contenido del archivo MD]
```
