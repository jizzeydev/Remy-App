# Funcionalidades

## Para el estudiante

### Biblioteca de cursos
- Lista de cursos disponibles (Cálculo I, II, Álgebra Lineal, Física, etc.).
- Cada curso tiene capítulos → lecciones.
- Lecciones con contenido en LaTeX/KaTeX, gráficos Desmos embebidos, imágenes.
- Candados visuales para usuarios sin suscripción activa.

### Simulacros
- Selección aleatoria desde el banco de preguntas del curso elegido.
- Configurable: número de preguntas (5/10/15/20).
- Quiz interactivo con navegación entre preguntas.
- Pantalla de resultados con score, soluciones paso a paso (KaTeX) e imágenes.

> Los cursos pueden estar tagueados a una universidad (`library_universities`) para filtrar la biblioteca, pero el banco de preguntas vive a nivel del **curso**, no de la universidad.

### Progreso
- Dashboard con KPIs personales: lecciones completadas, simulacros realizados, promedio, racha de estudio.
- Estadísticas por curso.

### Formulario / Buscador de fórmulas
- Catálogo de fórmulas matemáticas con búsqueda por nombre/tema.
- Filtrado por curso, ejemplos prácticos.

## Para el admin

### Gestión de contenido
- **Cursos**: CRUD con título, descripción, categoría, nivel. Pueden tagearse opcionalmente a una universidad (`library_universities`).
- **Capítulos** dentro de cada curso.
- **Lecciones** dentro de cada capítulo (Markdown + LaTeX + Desmos).
- **Preguntas**: CRUD con upload de imágenes a Cloudinary, soporte LaTeX, dificultad, tema, tags.
- **Universidades** (`library_universities`): CRUD ligero, solo nombre + sigla, para tagear cursos.

### Carga masiva
- **Importación CSV** con plantilla descargable. Formato:
  ```
  question_content,options,correct_answer,solution_content,difficulty,topic,tags
  ```
- Workflow: Jesús genera preguntas offline (con sus propias herramientas) → exporta a CSV con la plantilla → sube en el admin.

### Gestión de usuarios
- Lista paginada con búsqueda.
- Estadísticas globales.
- Otorgar acceso manual (1–12 meses), revocar, extender.

### Precios dinámicos
- Editar planes desde `/admin/pricing`.
- Hook `usePricing` propaga a landing y página de suscripción.

### Métricas
- Ingresos del período (selector: hoy / semana / mes / 3m / 6m / año).
- Suscripciones activas, nuevas, canceladas.
- Desglose por tipo (Mercado Pago vs manual).
- Gráficos de barras (últimos 30 días configurables a 7/14/30/60/90).
- Métricas de conversión: tasa, MRR, simulacros/usuario.
