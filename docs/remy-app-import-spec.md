# Remy App — Spec de importación de cursos universitarios

> **Documento para el repo de Remy App.** Define qué cursos universitarios hay que crear en Remy a partir de los splits matemáticos de Se Remonta, en qué orden y con qué esquema.
>
> **Detalle full de mallas:** ver [`splits-remy.md`](./splits-remy.md) en `se-remonta-ops` (1100+ líneas con todos los ramos por universidad). Este documento es el resumen accionable.
>
> **Fecha:** 14 de mayo de 2026.

---

## 1. Resumen ejecutivo

Remy hoy tiene cursos genéricos matemáticos. La tarea es crear **cursos universitarios derivados** que reutilicen los cursos base, siguiendo la misma lógica de splitting que Se Remonta usa para sus cursos pagados.

**Cobertura objetivo (al completar la importación):**

| Métrica | Valor |
|---|---:|
| Cursos base matemáticos | 9 |
| Universidades cubiertas | **12** |
| Carreras universitarias | ~88 |
| Ramos universitarios derivables | ~258 (con match alto/medio) |
| Splits **ya vendiéndose en seremonta.store** (prioridad 1) | 22 |

---

## 2. Cursos base (9 — crear primero)

Estos son los cursos "raíz" en Remy. Cada uno mapea 1:1 con un curso grabado por Se Remonta y sus lecciones son los módulos de ese curso.

| ID base (slug) | Nombre | Módulos |
|---|---|---:|
| `precalculo-cero` | Precálculo desde Cero | 68 |
| `nivelacion-ing` | Nivelación Ingeniería | 43 |
| `calculo-1var-gen` | Cálculo en una Variable | 85 |
| `calculo-dif-gen` | Cálculo Diferencial | 52 |
| `calculo-int-gen` | Cálculo Integral | 48 |
| `algebra-lineal-gen` | Álgebra Lineal | 52 |
| `calculo-vvar-gen` | Cálculo en Varias Variables | 41 |
| `calculo-vec-gen` | Cálculo Vectorial | 31 |
| `ec-dif-gen` | Ecuaciones Diferenciales | 42 |

→ **Total: 462 lecciones** distribuidas en 9 cursos.

---

## 3. Universidades a importar

**Las 12 universidades investigadas:**

| # | Sigla | Universidad | Tier | Carreras | Ramos | Match a/m | Estado split-remy |
|---|---|---|---|---:|---:|---:|---|
| 1 | UAI | Universidad Adolfo Ibáñez | 1 | 8 | 43 | ~26 | 🛒 5 publicados |
| 2 | UANDES | Universidad de los Andes | 1 | 10 | 32 | ~19 | — |
| 3 | UCH | Universidad de Chile | 1 | 8 | 47 | ~32 | — |
| 4 | UDD | Universidad del Desarrollo | 2 | 10 | 39 | ~26 | 🛒 4 publicados |
| 5 | UTFSM | U. Federico Santa María | 2 | 3 | 16 | ~12 | — |
| 6 | UNAB | Universidad Andrés Bello | 4 | 4 | 130 | 16 | — |
| 7 | USS | U. San Sebastián | 4 | 6 | 92 | 10 | — |
| 8 | PUCV | PU Católica de Valparaíso | 3 | 6 | 70 | 23 | — |
| 9 | UdeC | Universidad de Concepción | 3 | 12 | 115 | 40 | — |
| 10 | UDP | U. Diego Portales | 3 | 5 | 71 | 13 | — |
| 11 | UMay | Universidad Mayor | 4 | 6 | 174 | 13 | — |
| 12 | USACH | U. de Santiago | 3 | 10 | 298 | 28 | — |

**Bonus:** PUC tiene **13 cursos publicados en seremonta.store** pero la malla no se ha investigado todavía. Esos 13 son splits ya validados por el mercado.

---

## 4. Convención dual de IDs (importante)

Cada curso universitario derivado puede tener 2 slugs:

1. **Slug de investigación** (`slug`): `{universidad}-{carrera}-{ramo}`
   Ej: `uai-plan-comun-algebra-lineal`, `pucv-plan-comun-ing-civil-calculo-diferencial-e-integral`
   → identifica el ramo dentro de una malla investigada.

2. **Slug de producto** (`product_slug`): `{base}-{sigla}` o `{base}-{sigla}-{codigo}` cuando hay códigos UC
   Ej: `algebra-lineal-uc`, `calculo-dif-uai`, `calculo-i-uc-mat1100`
   → identifica un curso publicado/vendible en seremonta.store.

Cuando el split ya está vendiéndose, ambos campos van presentes. Cuando es sólo investigación, sólo va `slug` y `product_slug = null`.

---

## 5. Modelo de datos sugerido para Remy

```ts
// Tabla "universidades"
{
  id: string;            // slug ej. "uai", "pucv", "usach"
  sigla: string;         // "UAI", "PUCV", "USACH"
  nombre: string;        // "Universidad Adolfo Ibáñez"
  tier: 1 | 2 | 3 | 4;
}

// Tabla "carreras"
{
  id: string;            // "uai-plan-comun"
  universidad_id: string;
  nombre: string;        // "Ingeniería Civil Plan Común"
  facultad: string;
  duracion: string;
}

// Tabla "cursos_universitarios" (los splits derivados)
{
  id: string;            // slug = ID de investigación
  slug: string;          // mismo que id, único
  product_slug: string | null;     // ID de producto si está publicado
  published_at_seremonta_store: boolean;
  seremonta_url: string | null;
  universidad_id: string;
  carrera_id: string;
  base_course_id: string;           // FK a cursos base — primer curso base sugerido
  base_course_ids: string[];        // todos los cursos base aplicables
  nombre: string;        // "Álgebra Lineal MAT1203 — UC"
  codigo: string | null; // "MAT1203" si aplica
  semestre: number;      // 1-10
  prereqs: string;       // texto libre, ej. "MAT1100 Cálculo I"
  match_level: "alto" | "medio" | "bajo" | "ninguno";
  ejes: string[];        // array contenidos del .jsx
  source: "split" | "new"; // "split" si reutiliza curso base, "new" si requiere lecciones nuevas
  cobertura: "completa" | "parcial";  // "parcial" si match medio o material complementario pendiente
  notas: string | null;
}

// Tabla "curso_universitario_topics" (relación topics base ↔ cursos derivados)
{
  curso_universitario_id: string;
  topic_id: string | null;         // null si es eje pendiente sin topic asignado
  nombre_eje: string;              // texto del eje
  orden: number;
  cubierto: boolean;
}
```

---

## 6. Orden de importación (prioridad)

### Fase 1 — Cursos base (~1 día)
Crear los 9 cursos base con sus topics y lecciones existentes en Remy.

### Fase 2 — Splits ya publicados (22 cursos · ~2 días)
Estos ya se venden — máxima prioridad porque la demanda está validada:

**PUC (10 MAT):**
1. `precalculo-uc` (MAT1000) ← `precalculo-cero`
2. `intro-calculo-uc` (MAT1107) ← `precalculo-cero` + `nivelacion-ing`
3. `intro-algebra-geo-uc` (MAT1207) ← `precalculo-cero` + `nivelacion-ing`
4. `calculo-i-uc-mat1100` ← `calculo-dif-gen` + `calculo-int-gen` (50 mód, 5 cap)
5. `calculo-1var-uc-mat1023` ← `calculo-1var-gen`
6. `calculo-ii-uc-mat1220` ← `calculo-int-gen`
7. `algebra-lineal-uc` (MAT1203) ← `algebra-lineal-gen`
8. `intro-algebra-lineal-uc` (MAT1279-99) ← `algebra-lineal-gen` (subset)
9. `calculo-vec-uc` (MAT1630) ← `calculo-vvar-gen` + `calculo-vec-gen`
10. `ec-dif-uc` (MAT1640) ← `ec-dif-gen`

**UAI (5):**
- `calculo-dif-uai`, `calculo-int-uai`, `calculo-i-uai`, `calculo-ii-uai` (parcial), `calculo-iii-uai`

**UDD (4):**
- `calculo-dif-udd` (parcial), `calculo-int-udd` (parcial), `calculo-i-udd`, `calculo-ii-udd`

### Fase 3 — Splits match alto sin publicar (~150 cursos · ~5 días)

Por universidad, en orden de Tier 1 → 4. Cada uno corresponde a una "vista filtrada" del curso base — sólo cambia metadata (nombre, código U, orden pedagógico). No requiere generar lecciones nuevas.

Subgrupos prioritarios dentro de Fase 3:
1. **UC** (UCH): Plan Común FCFM × 6 + FEN MM I-IV × 4 + Lic. Mat/Fís/Pedagogía × 18 = 28 cursos.
2. **PUC** (UC): MAT pendientes (MAT1610, MAT1620 cuando se publiquen) — espera investigación de malla primero.
3. **USACH**: Plan Común × 6 + Lic. Mat/Fís × 4-6 + FAE × 3 + Bachillerato × 3 = ~16 cursos.
4. **UdeC**: 12 carreras compartiendo Plan Común — ~7 splits cubren las 12 carreras.
5. **UANDES**, **UAI**, **UDD**, **UTFSM**, **PUCV**, **UDP**, **UMay**, **UNAB**, **USS**.

### Fase 4 — Splits match medio (~50 cursos · ~5 días)

Requieren material complementario. Marcar `cobertura: "parcial"` y exponer cuáles ejes faltan. No generar preguntas aún para esos ejes.

### Fase 5 — Generación de preguntas/simulacros (continuo)

Seguir el SOP de Remy (`sop-remy-preguntas.md` en se-remonta-ops). Cada eje es un objetivo de aprendizaje.

---

## 7. Operación post-importación

1. **Endpoint de listado**: `GET /api/universities` → 12 universidades.
2. **Endpoint por U**: `GET /api/universities/:sigla/courses` → todos los cursos universitarios de esa U, agrupados por carrera y semestre.
3. **Endpoint por curso derivado**: `GET /api/university-courses/:slug` → metadata + ejes + topics base heredados + cobertura.
4. **Dashboard admin**: vista por universidad mostrando #ramos cubiertos completos / parciales / pendientes. Permite priorizar generación de preguntas.

---

## 8. No tocar

- **No crear preguntas nuevas** durante la importación. La importación es sólo de estructura. Las preguntas se heredan por relación con topics del curso base.
- **No renombrar slugs** del documento. Son el identificador estable que comparte el dashboard de Se Remonta y permite cruzar progreso entre sistemas.
- **No incluir ramos no-matemáticos** (física, química, programación, economía, estadística). Quedan registrados en los `.jsx` pero **fuera del scope de Remy hoy** — Remy es 100% matemáticas en esta fase.
- **No incluir Pedagogía / Licenciaturas** con ramos avanzados (Análisis Real, Topología, Análisis Complejo) — fuera del catálogo base actual.

---

## 9. Referencias en se-remonta-ops

- Investigaciones `.jsx`: `docs/splitting/Investigaciones_Universidades/<sigla>.jsx` — fuente bruta verificada.
- Catálogo base JSON: `apps/ops/data/splits/catalog/<id>.json` — metadata cursos base.
- Mallas en dashboard: `apps/ops/data/splits/universities/<sigla>.json` — sólo 5 cargadas hoy.
- SOP completo: `docs/procesos/sop-splitting.md`.
- Doc full con todos los ramos por U: `docs/producto/splits-remy.md`.
