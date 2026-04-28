# Metodología — Construcción de lecciones para cursos generales

Este documento define cómo construir las lecciones de los cursos base de Remy a partir de las guías PDF que viven en cada carpeta de capítulo. Es la fuente de verdad pedagógica y editorial: cuando se cree contenido nuevo (manualmente o asistido por IA externa), debe seguirse esta guía.

---

## 1. Audiencia y nivel

Las lecciones están dirigidas a estudiantes universitarios chilenos de primer y segundo año en carreras STEM:

- **Ingeniería** (civil, industrial, comercial, informática, etc.)
- **College** (programas de bachillerato científico)
- **Comercial** (donde se cursa cálculo aplicado)
- A futuro, escalable a otras universidades hispanohablantes (Argentina, México, Colombia, Perú).

Esto implica:

- **Rigor matemático real**: definiciones formales con $\epsilon$-$\delta$ cuando corresponda, hipótesis explícitas en teoremas, demostraciones rigurosas.
- **Notación universitaria**: LaTeX completo. Nada de "x al cuadrado" en texto plano cuando se puede escribir $x^2$.
- **Sin tono escolar**: ni infantilizado, ni con emojis exagerados en la prosa, ni con ejemplos triviales tipo "Juan compra 3 manzanas".
- **Castellano neutral**: sin voseo, sin modismos rioplatenses, sin chilenismos extremos. Aprobable para un alumno de cualquier universidad hispanohablante.

---

## 2. Filosofía pedagógica

Cada lección debe responder, en orden, a tres preguntas implícitas del alumno:

1. **¿Por qué esto importa?** → bloque `intuicion` antes del formalismo.
2. **¿Qué es exactamente?** → bloques `definicion`, `teorema`, `ejemplo_resuelto`.
3. **¿Lo entendí?** → bloques `verificacion` distribuidos a lo largo (no solo al final).

Principios concretos que distinguen una lección excelente de una mediocre:

- **Intuición antes de formalismo.** Una analogía física o geométrica antes de la definición rigurosa. La definición es la respuesta; la intuición es la pregunta.
- **Justificación en cada paso de un ejemplo.** Los libros muestran la **acción matemática** (sustituir, factorizar, simplificar). Nosotros agregamos la **justificación** (por qué se hace ese paso). Esto es lo que separa la mímesis del aprendizaje real.
- **Hipótesis explícitas en teoremas.** Renderizadas como checklist visual. Los alumnos olvidan condiciones (ej. MVT requiere continuidad **y** derivabilidad). Hacerlas visibles previene el error.
- **Demostraciones colapsables.** Disponibles para quien quiera profundizar, no impuestas. La demostración construye técnica, pero no debe abrumar al alumno que solo quiere entender el resultado.
- **Múltiples representaciones.** Cada concepto debe presentarse en al menos dos formas: algebraica + geométrica, o algebraica + física. Distintos alumnos "lo cachan" por distintas vías.
- **Errores comunes nombrados explícitamente.** "El error más frecuente es confundir X con Y". Dar un nombre al error vacuna contra cometerlo.
- **Retrieval practice distribuido.** Preguntas de verificación cada 4-6 bloques, no solo al final. Un alumno que responde mientras lee retiene el doble que uno que solo lee.
- **Cierre que conecta.** El resumen debe mencionar qué viene en la próxima lección, para que el alumno construya estructura mental del curso.

---

## 3. Estructura macro de una lección

Toda lección sigue esta arquitectura general (no rígida, pero sí guía):

```
┌─ APERTURA ─────────────────────────────────────────────┐
│  texto       — bienvenida + objetivos explícitos        │
│  intuicion   — analogía o motivación inicial            │
└────────────────────────────────────────────────────────┘

┌─ DESARROLLO (un módulo por sección de la guía PDF) ────┐
│  Por cada concepto principal:                           │
│    intuicion     — qué problema resuelve                │
│    definicion    — formalización rigurosa               │
│    grafico_desmos / figura — representación visual      │
│    ejemplo_resuelto — al menos uno por concepto         │
│    verificacion  — 1-2 preguntas (cada 1-2 conceptos)   │
│                                                         │
│  Al menos un teorema importante por lección debe ir     │
│  con su demostración (colapsable).                      │
└────────────────────────────────────────────────────────┘

┌─ CIERRE ──────────────────────────────────────────────┐
│  errores_comunes — pitfalls específicos de la lección  │
│  resumen         — bullets clave + conexión a la       │
│                    siguiente lección                    │
└────────────────────────────────────────────────────────┘
```

**Reglas de cantidad orientativas:**

- Lección típica: 25-35 bloques, 35-50 minutos de estudio (`duration_minutes`).
- Bloques `verificacion`: mínimo 2 por lección, distribuidos.
- Bloques `ejemplo_resuelto`: mínimo 1 por concepto principal.
- Bloque `errores_comunes`: al menos 1 al cierre, opcional intermedio.
- Bloque `resumen`: exactamente 1 al final.

---

## 4. Catálogo de bloques — cuándo usar cada uno

| Tipo | Úsalo para... | Evítalo cuando... | Campos clave |
|---|---|---|---|
| **`texto`** | Prosa narrativa, transiciones, objetivos | Algo merezca destacarse (usar otro tipo) | `body_md` |
| **`definicion`** | Concepto formal que el alumno debe memorizar | Sea solo una explicación informal (usar `intuicion`) | `titulo`, `body_md` |
| **`teorema`** | Resultado formal con hipótesis y/o demostración | Sea una propiedad menor (usar `definicion`) | `nombre`, `hipotesis[]`, `enunciado_md`, `demostracion_md`, `demostracion_default_open` |
| **`intuicion`** | Motivación informal antes del formalismo | El concepto no necesite analogía | `titulo`, `body_md` |
| **`ejemplo_resuelto`** | Problema desarrollado paso a paso con justificación | Sea solo un cálculo de una línea (incluir en `texto`) | `titulo`, `problema_md`, `pasos[].accion_md`, `pasos[].justificacion_md`, `pasos[].es_resultado` |
| **`grafico_desmos`** | Concepto que se entiende moviendo sliders | Una imagen estática sea suficiente (usar `figura`) | `expresiones[]`, `guia_md`, `altura` |
| **`figura`** | Imagen estática: discontinuidades, regiones de $\mathbb{R}^2$, diagramas anotados | Desmos pueda hacerlo bien | `image_url`, `caption_md`, `prompt_image_md` |
| **`verificacion`** | Mini-quiz de retención (1-3 preguntas) | Sea evaluación final (usar simulacros del banco) | `intro_md`, `preguntas[].enunciado_md`, `preguntas[].opciones_md[4]`, `preguntas[].correcta`, `preguntas[].explicacion_md` |
| **`errores_comunes`** | Listar pitfalls explícitamente | El error sea obvio del contexto | `items_md[]` |
| **`resumen`** | Cierre con bullets clave + hint a próxima lección | A mitad de lección (usar `texto`) | `puntos_md[]` |

### Decisiones rápidas

- **Definición o intuición**: si necesita ser citado/memorizado, es `definicion`. Si es solo "para pensarlo", es `intuicion`.
- **Teorema o definición**: si tiene hipótesis y enunciado tipo "si... entonces...", es `teorema`. Si es solo una construcción ("la derivada se define como..."), es `definicion`.
- **Desmos o figura**: si el alumno puede aprender moviendo algo, es `grafico_desmos`. Si hay que mostrar algo específico (esquina, círculo abierto, etiqueta sobre un punto), es `figura`.
- **Verificación inline o pregunta de simulacro**: las preguntas de `verificacion` son para retención durante la lección. Las preguntas de simulacro (banco general del curso) son para evaluación posterior. No mezclar.

---

## 5. Workflow desde un PDF

Cada capítulo del curso vive en `docs/cursos/<curso>/<capitulo>/` con uno o más PDFs base. El proceso para convertir un PDF en lección es:

### Paso 1 — Lectura y mapeo

Leer el PDF completo. Identificar:

- **Secciones formales** (1, 1.1, 1.2, 2, etc.) — cada una corresponderá a un módulo de la lección.
- **Definiciones formales** del PDF — cada una será un bloque `definicion`.
- **Teoremas** — cada uno será un bloque `teorema`.
- **Ejemplos numerados** o "ejercicio resuelto" — cada uno será un bloque `ejemplo_resuelto`.
- **Figuras o gráficos** del PDF — cada uno será `grafico_desmos` (si interactivo) o `figura` (si estático).

### Paso 2 — Identificar lo que el PDF NO tiene

Los PDFs académicos típicamente carecen de:

- **Intuición previa al formalismo.** *Tarea: agregar bloque `intuicion` antes de cada `definicion` o `teorema` importante.*
- **Justificación en pasos de ejemplos.** *Tarea: para cada paso del ejemplo PDF, escribir el "por qué se hace este paso" en `justificacion_md`.*
- **Errores comunes.** *Tarea: agregar al menos un bloque `errores_comunes` por lección, basado en experiencia docente.*
- **Verificación de retención.** *Tarea: insertar bloques `verificacion` con preguntas que apunten a errores comunes y conceptos críticos.*
- **Conexiones a otros temas.** *Tarea: en el `resumen`, mencionar qué viene después.*

### Paso 3 — Estructurar la secuencia

Aplicar la estructura macro (apertura → desarrollo → cierre). Para cada módulo del desarrollo, aplicar el patrón:

```
intuicion → definicion/teorema → grafico/figura → ejemplo_resuelto → verificacion
```

No es obligatorio incluir los cinco pasos en cada módulo, pero al menos `definicion` + `ejemplo_resuelto` debe estar presente.

### Paso 4 — Escribir contenido

Reglas de redacción durante la escritura:

- **Cobertura total del PDF**: ningún concepto, definición, teorema o ejemplo del PDF debe quedar fuera. Verificable con un checklist al final.
- **Reorganización permitida**: si el orden del PDF no es óptimo pedagógicamente, se reordena.
- **Ampliación recomendada**: si el PDF muestra un solo ejemplo y conviene un segundo más complejo, se agrega.
- **Reemplazo permitido**: si el ejemplo del PDF es débil (caso trivial), se reemplaza por uno mejor del mismo nivel.

### Paso 5 — Imágenes vía ChatGPT Images

Para cada bloque `figura`:

1. Escribir el prompt detallado en `prompt_image_md`.
2. Copiar el prompt al portapapeles desde el editor del admin (botón "Copiar").
3. Pegar el prompt en ChatGPT Images, generar la imagen.
4. Descargar el PNG.
5. Subirlo desde el editor del admin (botón "Subir archivo" en el bloque `figura`). Va a Cloudinary automáticamente.
6. El prompt queda guardado para regenerar después si hace falta.

**Nunca usar URLs externas (Wikipedia, Pexels, etc.) ni SVGs hechos a mano.** Solo Cloudinary vía el flujo del editor.

### Paso 6 — Validación con checklist (sección 7)

Antes de publicar, correr el checklist completo.

---

## 6. Reglas de estilo

### 6.1 Idioma

- **Español neutral**. Sin voseo: usar tuteo (`tienes`, no `tenés`) o construcciones impersonales (`se obtiene`, `conviene observar`).
- **Sin modismos**: nada de "dale", "che", "bárbaro", "joya", "weón", "po", "fome".
- **Imperativos formales en enunciados de ejercicios**: "Calcular $f'(x)$" o "Demostrar que...", no "Calculá" ni "Mostrá".
- **Tono profesional, cercano sin ser informal**. El alumno debe sentirse respetado, no condescendido.

### 6.2 Notación matemática

- **Inline**: `$f(x) = x^2$` para fórmulas dentro del flujo del texto.
- **Bloque**: `$$\lim_{x \to a} f(x) = L$$` para fórmulas que merecen aire propio.
- **Nunca** usar `\(...\)` ni `\[...\]` — solo `$...$` y `$$...$$`.
- Comandos preferidos: `\dfrac` (no `\frac`) para fracciones inline en ejemplos resueltos. `\dfrac` da mejor lectura cuando aparecen en el medio del texto.
- Funciones estándar con backslash: `\sin`, `\cos`, `\log`, `\ln`, `\lim`, `\sup`, `\inf`, `\max`, `\min`. Evitar `sin(x)` plano.
- Conjuntos: `\mathbb{R}`, `\mathbb{N}`, `\mathbb{Z}`, `\mathbb{Q}`, `\mathbb{C}`.
- Producto cartesiano: `\times`. Implicación: `\Rightarrow`. Equivalencia: `\Leftrightarrow` o `\iff`. Pertenencia: `\in`.
- Negaciones: `\not\Rightarrow`, `\notin`.

### 6.3 Markdown

- **Negrita** para conceptos clave, no para énfasis general.
- *Cursiva* para énfasis suave o términos técnicos al introducirlos.
- Listas con `-` (no `*`).
- Citas con `>` solo para advertencias o notas al margen.
- **Encabezados dentro de bloques `body_md`**: usar `##` para divisiones internas. Nunca `#` (el título del bloque cumple ese rol).

### 6.4 Tono editorial

- Frases cortas a medianas. Evitar oraciones encadenadas con tres "que".
- Usar voz activa cuando sea posible: "La derivada mide..." en lugar de "Es medida por la derivada...".
- Una idea por párrafo. Si un bloque `texto` o `body_md` supera las 6-7 líneas, dividirlo en dos bloques o usar otro tipo de bloque (`definicion`, `intuicion`).

---

## 7. Checklist de calidad — antes de publicar

Antes de marcar una lección como terminada, verificar punto por punto:

### Cobertura

- [ ] Todos los conceptos, definiciones y teoremas del PDF base están presentes.
- [ ] Todos los ejemplos numerados del PDF están como `ejemplo_resuelto`.
- [ ] Todas las figuras o gráficos del PDF tienen su contraparte (`grafico_desmos` o `figura`).

### Pedagogía

- [ ] Existe al menos un bloque `intuicion` en la apertura.
- [ ] Existe al menos un bloque `intuicion` antes de cada definición/teorema importante.
- [ ] Cada `ejemplo_resuelto` tiene al menos un paso con `justificacion_md` (idealmente la mayoría).
- [ ] Cada `teorema` tiene `hipotesis[]` poblado (no solo el enunciado).
- [ ] Cada `grafico_desmos` tiene `guia_md` indicando qué observar.
- [ ] Existe al menos un bloque `verificacion` antes de la mitad de la lección.
- [ ] Existe al menos un bloque `errores_comunes`.
- [ ] Existe exactamente un bloque `resumen` al final, con bullets clave + mención a la próxima lección.

### Estilo

- [ ] No hay voseo (`tenés`, `mirá`, `calculá`, etc.) ni modismos rioplatenses.
- [ ] No hay chilenismos extremos ("po", "weón", "fome", etc.).
- [ ] Toda fórmula matemática usa `$...$` o `$$...$$`. No hay `\(...\)` ni `\[...\]`.
- [ ] Funciones estándar usan backslash (`\sin`, `\lim`, etc.).

### Imágenes

- [ ] Todos los bloques `figura` tienen `image_url` apuntando a Cloudinary (no URLs externas, no SVG inline, no `data:`).
- [ ] Todos los bloques `figura` tienen `prompt_image_md` con el prompt usado para generar la imagen.
- [ ] Cada `figura` tiene `caption_md` que aporta contexto, no que describe lo obvio.

### Verificaciones

- [ ] Cada `verificacion` tiene 1-3 preguntas (no más).
- [ ] Cada pregunta tiene 4 opciones distintas y plausibles (los distractores deben ser errores comunes, no obviamente incorrectos).
- [ ] Cada pregunta tiene `explicacion_md` que explica **por qué** la respuesta correcta es correcta y, idealmente, **por qué** los distractores son trampas típicas.

### Render visual

- [ ] La lección renderiza sin errores en `/lesson/<id>` (vista del alumno).
- [ ] Las fórmulas LaTeX se ven bien (no aparecen `$` literales ni `\dfrac` sin renderizar).
- [ ] Las imágenes cargan correctamente.
- [ ] Los gráficos Desmos cargan y son interactivos.

---

## 8. Anti-patrones — qué NO hacer

- **❌ "Wall of text" en `body_md`.** Si un bloque tiene más de ~8 líneas, dividirlo. La densidad visual mata la atención.
- **❌ Definir sin motivar.** Lanzar una `definicion` sin un `intuicion` previo es académico-burocrático.
- **❌ Ejemplos sin justificación.** "Paso 1: aplicamos la regla. Paso 2: simplificamos." sin decir POR QUÉ es el atajo de los libros malos.
- **❌ Demostraciones largas no colapsadas.** Una demo de 10 líneas con `demostracion_default_open: true` enterrá el siguiente bloque visualmente.
- **❌ Verificación al final solamente.** El alumno necesita feedback durante, no después.
- **❌ Distractores tontos.** Si las opciones incorrectas son obviamente absurdas, la pregunta no enseña nada.
- **❌ Resumen genérico.** Bullets como "vimos qué es la derivada" son inútiles. Debe ser específico: "$f'(a) = \\lim_{h\\to 0}\\dfrac{f(a+h)-f(a)}{h}$, equivalente a la fórmula con $x \\to a$".
- **❌ Imágenes hechas a mano (SVG inline) o de Wikipedia.** Solo Cloudinary vía ChatGPT Images.
- **❌ Mezclar bloques `verificacion` con preguntas del simulacro.** Son herramientas distintas con propósitos distintos.
- **❌ Usar `texto` cuando hay un tipo más específico.** Si el contenido es una definición, va en `definicion`. Si es un ejemplo, en `ejemplo_resuelto`. `texto` es solo para narrativa de transición.

---

## 9. Convención de carpetas

```
docs/
└── cursos/
    ├── README.md                       ← este documento
    └── <slug-del-curso>/                ← ej. calculo-diferencial
        ├── <slug-del-capitulo>/         ← ej. derivadas
        │   ├── <Tema>.pdf               ← guía base de la lección
        │   ├── <Otro_Tema>.pdf
        │   └── notas.md                 ← (opcional) notas específicas
        ├── <otro-capitulo>/
        └── ...
```

**Convención de slugs:**

- Curso: `calculo-diferencial`, `algebra-lineal`, `ecuaciones-diferenciales`.
- Capítulo: `derivadas`, `limites`, `integracion`.
- Carpetas y archivos: kebab-case en español, sin tildes, sin espacios.

**Lo que va en cada PDF:** son las guías académicas que sirven de fuente. No se modifican; son input.

**Lo que produce el proceso:** una lección en MongoDB (visible en el admin y para los alumnos). El PDF queda como referencia.

---

## 10. Plantilla rápida para empezar una lección nueva

Cuando se inicie una lección desde cero, esta es la secuencia mínima de bloques (luego se expande según el contenido del PDF):

```
1.  texto              — bienvenida + objetivos
2.  intuicion          — motivación inicial
3.  definicion         — concepto principal #1
4.  ejemplo_resuelto   — aplicación del concepto #1
5.  verificacion       — 1-2 preguntas
6.  intuicion          — motivación del concepto #2
7.  teorema            — concepto #2 con hipótesis
8.  grafico_desmos     — visualización del concepto #2
9.  ejemplo_resuelto   — aplicación del concepto #2
10. errores_comunes    — pitfalls de la lección
11. verificacion       — 1-2 preguntas finales
12. resumen            — cierre + conexión a próxima lección
```

Esta plantilla cubre los mínimos pedagógicos. Ampliar con más bloques según contenido del PDF.

---

## 11. Referencia: lección modelo

La lección **"1.1 — Definición y notación de la derivada"** (curso Cálculo Diferencial) sirve como referencia canónica de aplicación de esta metodología. Está disponible en producción local en `/lesson/lesson-definicion-y-notacion`. Su seed vive en `backend/seed_lesson_definicion_derivada.py`.

Cuando haya dudas de implementación, comparar con esa lección.

---

**Última actualización:** 2026-04-25
**Mantenedor:** Jesús (Se Remonta)
**Aplica a:** todos los cursos generales de Remy (los cursos enfocados a universidad específica heredarán esta metodología cuando se construyan).
