# Investigaciones de Universidades

Carpeta donde viven los archivos `.jsx` con la **investigación pura** de cada universidad: mallas, ramos, contenidos, fuentes verificadas.

> Cada archivo es la fuente de verdad bruta. El dashboard `/splits` es solo una vista interactiva sobre estos datos.

---

## Archivos actuales

| Archivo | Universidad | Tier | Fecha | Carreras | Ramos | Match alto/medio | Estado |
|---------|-------------|------|-------|---------:|------:|-----------------:|--------|
| [`uai.jsx`](./uai.jsx) | UAI — Universidad Adolfo Ibáñez | 1 | Abr 2026 | 8 | 43 | ~26 | ✅ Cargada en dashboard |
| [`uandes.jsx`](./uandes.jsx) | UANDES — Universidad de los Andes | 1 | Abr 2026 | 10 | 32 | ~19 | ✅ Cargada en dashboard |
| [`uch.jsx`](./uch.jsx) | UCH — Universidad de Chile | 1 | Abr 2026 | 8 | 47 | ~32 | ✅ Cargada en dashboard |
| [`udd.jsx`](./udd.jsx) | UDD — Universidad del Desarrollo | 2 | Abr 2026 | 10 | 39 | ~26 | ✅ Cargada en dashboard |
| [`utfsm.jsx`](./utfsm.jsx) | UTFSM — Univ. Federico Santa María | 2 | Abr 2026 | 3 | 16 | ~12 | ✅ Cargada en dashboard |
| [`unab.jsx`](./unab.jsx) | UNAB — Universidad Andrés Bello | 4 | Abr 2026 | 4 | 130 | 16 | 🟡 Pendiente migrar al dashboard |
| [`uss.jsx`](./uss.jsx) | USS — Universidad San Sebastián | 4 | Abr 2026 | 6 | 92 | 10 | 🟡 Pendiente migrar al dashboard |
| [`pucv.jsx`](./pucv.jsx) | PUCV — PU Católica de Valparaíso | 3 | May 2026 | 6 | 70 | 23 | 🟡 Pendiente migrar al dashboard |
| [`udec.jsx`](./udec.jsx) | UdeC — Universidad de Concepción | 3 | May 2026 | 12 | 115 | 40 | 🟡 Pendiente migrar al dashboard |
| [`udp.jsx`](./udp.jsx) | UDP — Universidad Diego Portales | 3 | May 2026 | 5 | 71 | 13 | 🟡 Pendiente migrar al dashboard |
| [`umay.jsx`](./umay.jsx) | UMAY — Universidad Mayor | 4 | May 2026 | 6 | 174 | 13 | 🟡 Pendiente migrar al dashboard |
| [`usach.jsx`](./usach.jsx) | USACH — Universidad de Santiago | 3 | May 2026 | 10 | 298 | 28 | 🟡 Pendiente migrar al dashboard |

**Total: 12 universidades · 88 carreras · 1127 ramos investigados · ~258 con match alto/medio matemático.**

Distribución:
- 5 en dashboard: 39 carreras · 177 ramos
- 7 pendientes migrar: 49 carreras · 950 ramos (UNAB, USS, PUCV, UdeC, UDP, UMay, USACH)

Para migrar las 7 pendientes al dashboard hay que sumar sus entradas en `apps/ops/scripts/migrate-splits.mjs` (`UNIVERSITY_META`) y correr el script — ver paso 4 abajo.

---

## Pendientes prioritarias

Sólo queda **una** investigación crítica por hacer:

| Sigla | Universidad | Tier | Prioridad | Por qué |
|-------|-------------|------|-----------|---------|
| **UC** | Pontificia Universidad Católica | 1 | **Inmediata** | Mercado #1 actual. Hay 13 cursos publicados en seremonta.store pero la malla no está investigada |

Universidades de menor prioridad sin investigar (evaluar caso a caso):
- UFRO (Universidad de la Frontera, Temuco)
- UANTOF (Universidad de Antofagasta)
- ULS (Universidad de La Serena)
- UTAL (Universidad de Talca)
- UAH (Universidad Alberto Hurtado)
- Privadas regionales menores (UNIACC, UGM, etc.)

---

## Cómo crear una investigación nueva

1. **Pegale el prompt a Cowork:** abrí [`../PROMPT_COWORK.md`](../PROMPT_COWORK.md), reemplazá los placeholders, pegalo en Claude Cowork.

2. **Cowork devuelve un .jsx** — guardalo como `<sigla>.jsx` (minúscula, sin acentos).

3. **Validá con el checklist** (más abajo).

4. **Agregá metadata** al migrador si es una U nueva — abrí `apps/ops/scripts/migrate-splits.mjs` y sumá la entrada en `UNIVERSITY_META`:

   ```js
   pucv: { sigla: "PUCV", nombre: "Pontificia Universidad Católica de Valparaíso", tier: 3 },
   ```

5. **Migrá al dashboard**:
   ```bash
   cd se-remonta-ops/apps/ops
   node scripts/migrate-splits.mjs
   ```

6. **Validá en el dashboard**: `http://localhost:3000/splits` → filtrá por la nueva U.

---

## Checklist de validación del .jsx que devuelve Cowork

Antes de aceptarlo:

- [ ] Tiene `const seRemontaCursos = [...]` con los 9 cursos base **exactos** del prompt (no inventados, no removidos).
- [ ] Tiene `const carreras = [...]` con al menos **Ingeniería Civil Plan Común**.
- [ ] **Cada carrera** tiene: `id`, `nombre`, `facultad`, `duracion`, `especialidades`, `mallaUrl`, `ramos`.
- [ ] **Cada ramo** tiene: `nombre`, `semestre`, `prereqs`, `fuenteContenido` (o `nota`), `contenidos[]` (≥3 items), `match[]`, `matchLevel`, `splitDesde`.
- [ ] Cada `match` apunta a un id del catálogo base (no inventado): `precalculo-cero`, `nivelacion-ing`, `algebra-lineal-gen`, `calculo-1var-gen`, `calculo-dif-gen`, `calculo-int-gen`, `calculo-vvar-gen`, `calculo-vec-gen`, `ec-dif-gen`.
- [ ] Cada `matchLevel` es uno de: `alto`, `medio`, `bajo`, `ninguno`.
- [ ] Las URLs de mallas y syllabi abren correctamente (no 404).
- [ ] No hay ramos no-matemáticos colados (Física, Química suelen escaparse).
- [ ] Los semestres son enteros 1–12 plausibles.
- [ ] No hay template literals (\`...\`), JSX, ni funciones en los datos — sólo arrays y objetos puros.
- [ ] El archivo no excede 100 KB (las 5 actuales pesan 46–60 KB).

Si algo falla, devolvele el feedback específico a Cowork y pedile el .jsx corregido. **No corrijas a mano** salvo errores triviales de sintaxis — Cowork debe entregar limpio para mantener consistencia.

---

## Plantilla esqueleto

Está en [`_template-universidad.jsx`](./_template-universidad.jsx) — copia y pega cuando Cowork no devuelva la estructura exacta y necesités darle la base.

---

## Re-ejecutar una investigación existente

Si una U cambia su malla (ocurre cada ~2 años) o querés que Cowork cubra carreras que se le quedaron afuera:

1. Re-ejecutá Cowork con el mismo prompt + URLs actualizadas.
2. Sobrescribí `<sigla>.jsx`.
3. Corré `migrate-splits.mjs`.
4. **El estado editable se preserva**: status, prioridad, URLs publicadas, notas — el migrador hace merge por id de ramo.
5. Si Cowork cambió el `nombre` de un ramo, su id (slug) también cambia → la migración crea el ramo como nuevo. En ese caso, mover el estado manualmente desde el ramo viejo al nuevo (editar JSON o re-marcar en el dashboard).

---

## Troubleshooting

| Síntoma | Causa frecuente | Fix |
|---------|-----------------|-----|
| `vm.runInNewContext` falla en migración | El .jsx tiene template strings o JSX en los datos | Cowork debe entregar solo strings con comillas dobles |
| Tabla "Cobertura por curso base" vacía para esta U | Los `match` apuntan a ids inexistentes | Validar checklist — los ids deben ser exactos |
| `match_level` inválido | Cowork inventó un nivel (`completo`, `parcial`) | Forzar a {`alto`, `medio`, `bajo`, `ninguno`} en el prompt |
| Ramos duplicados en una carrera | Mismo nombre con dos slugs distintos | Editar el .jsx para unificar |
| `migrate-splits.mjs` no encuentra el .jsx | Nombre con mayúscula o acento | Renombrar a minúscula sin acentos |

---

*Detalle del workflow completo end-to-end en [`docs/procesos/sop-investigacion-cowork.md`](../../../se-remonta-ops/docs/procesos/sop-investigacion-cowork.md).*
