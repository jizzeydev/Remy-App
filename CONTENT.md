# Contenido — workflow de autoría local + push a producción

Playbook para crear/editar cursos de Remy desde local con Claude Code y empujarlos
a producción sin tocar usuarios, pagos ni progreso. Compañero de [DEPLOY.md](DEPLOY.md)
(que cubre infra y deploy de código). Acá hablamos solo de **datos de contenido**.

---

## Modelo de datos

```
Course ──┬── Chapter ──┬── Lesson (blocks: Block[])
         │             └── Question[]   ← ligadas por chapter_id (y opcional lesson_id)
         └── Chapter (linked: template_chapter_id apunta a otro capítulo)
                └── puede excluir lesson_ids / question_ids específicos
```

Schema autoritativo: [backend/server.py:70-169](backend/server.py#L70-L169).
Tipos de bloque permitidos (deben matchear el frontend):

| Tipo               | Campos clave                                      | Cuándo usar                                       |
|--------------------|---------------------------------------------------|---------------------------------------------------|
| `texto`            | `body_md`                                         | párrafo libre — soporta Markdown + KaTeX          |
| `definicion`       | `titulo`, `body_md`                               | concepto formal destacado                         |
| `teorema`          | `enunciado_md`                                    | proposición + (opcional) demostración             |
| `intuicion`        | `body_md`                                         | lectura informal                                  |
| `ejemplo_resuelto` | `titulo`, `problema_md`, `pasos[]`                | resolución guiada paso a paso                     |
| `ejercicio`        | `titulo`, `enunciado_md`, `pistas_md`, `solucion_md` | el alumno resuelve, con pistas y solución      |
| `figura`           | `image_url`, `caption_md`, `prompt_image_md`      | imagen — el `prompt_image_md` alimenta la generación |
| `grafico_desmos`   | `expresiones[]`, `notas_md`                       | embed interactivo                                 |
| `errores_comunes`  | `items_md[]`                                      | bullets de pifias frecuentes                      |
| `resumen`          | `puntos_md[]`                                     | cierre de la lección                              |

Bloques son `Dict[str, Any]` en el modelo (validación laxa). El único campo común
obligatorio es `id` (UUID) y `type`. Mantené consistencia revisando seeds existentes.

---

## Layout en disco

```
backend/seeds/<curso-slug>/seed_capitulo_N.py     ← lecciones + bloques (Python, idempotente)
backend/seeds/_template/seed_capitulo_template.py ← punto de partida para capítulos nuevos
docs/cursos/generales/<curso-slug>/<NN. Capítulo>/
    Clases/                                       ← material de referencia (scans, apuntes)
    Ejercicios/                                   ← guías resueltas / problemarios
    Preguntas/<slug>.csv                          ← banco de preguntas multiple choice
scripts/run_seed.py                               ← wrapper para ejecutar seeds
scripts/import_questions_csv.py                   ← importar CSVs de preguntas a Mongo local
scripts/sync_content_to_atlas.py                  ← push selectivo de contenido a prod
```

Cursos existentes con seeds: `algebra-lineal`, `calculo-diferencial`, `calculo-integral`,
`calculo-multivariable`, `calculo-vectorial`, `ecuaciones-diferenciales`, `precalculo`.
Cursos universitarios (PUC) se generan vía [scripts/seed_uc_courses.py](scripts/seed_uc_courses.py)
linkeando capítulos de los generales — no se autorean directamente.

---

## Convenciones de IDs

Estables y human-readable, no UUID. Facilita debugging y reseed idempotente.

- `course_id`  → kebab-case del slug temático: `algebra-lineal`, `termodinamica`.
- `chapter_id` → `ch-<curso-corto>-<tema>`: `ch-al-espacio`, `ch-cd-derivadas`.
- `lesson_id`  → `lec-<curso-corto>-<cap>-<tema>`: `lec-al-1-3-producto-cruz`.
- `question.id` → UUID generado en runtime (no editorial).

---

## Setup mínimo (una sola vez)

```bash
# 1. venv del backend con las deps
python -m venv backend/venv
backend/venv/Scripts/pip.exe install -r backend/requirements.txt

# 2. Mongo local corriendo (mongod o Docker)
# 3. backend/.env tiene MONGO_URL y DB_NAME apuntando a la instancia local

# 4. backend + frontend levantados
cd backend && ./venv/Scripts/uvicorn.exe server:app --reload --port 8001
cd frontend && yarn start    # arranca en :3007
```

---

## Los 4 flujos

### Flujo 1 — Crear un curso nuevo desde cero

1. Copiá la plantilla a la carpeta del curso:
   ```bash
   mkdir -p backend/seeds/<curso-slug>
   cp backend/seeds/_template/seed_capitulo_template.py \
      backend/seeds/<curso-slug>/seed_capitulo_1.py
   ```

2. Editá `seed_capitulo_1.py`: completá los `TODO` (`COURSE_ID`, `COURSE_TITLE`,
   `CHAPTER_ID`, `CHAPTER_TITLE`, builders de lecciones).

3. Aplicá a Mongo local:
   ```bash
   python scripts/run_seed.py backend/seeds/<curso-slug>/seed_capitulo_1.py
   ```

4. Verificá en `http://localhost:3007/courses/<curso-slug>` y `/lesson/<lesson-id>`.

5. Repetí para cada capítulo (`seed_capitulo_2.py`, `seed_capitulo_3.py`, ...).
   Recordá actualizar `COURSE_MODULES_COUNT` en cada seed cuando agregues capítulos.

### Flujo 2 — Editar lecciones existentes

Edición directa del seed correspondiente. **No hay edición fuera de los seeds**:
si tocás un curso vía admin UI y después corrés el seed, perdés los cambios del UI.
Trabajá siempre desde los seeds.

```bash
# 1. abrir y editar el seed
$EDITOR backend/seeds/algebra-lineal/seed_capitulo_2.py

# 2. reseedear (delete + insert idempotente del capítulo)
python scripts/run_seed.py backend/seeds/algebra-lineal/seed_capitulo_2.py

# 3. revisar en localhost:3007
```

Para reseedear todo un curso de una:
```bash
python scripts/run_seed.py "backend/seeds/algebra-lineal/seed_capitulo_*.py"
```

### Flujo 3 — Reemplazar/agregar preguntas en masa

CSV en `docs/cursos/generales/<curso-slug>/<NN. Capítulo>/Preguntas/<slug>.csv`.

Formato (UTF-8, separador coma):
```
capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion
"Espacio","Vectores","fácil","¿Cuántas componentes tiene un vector en $\mathbb{R}^3$?","2","3","4","Depende","B","Por definición un vector en $\mathbb{R}^3$ tiene 3 componentes."
```

- `capitulo` y `leccion` matchean por **título exacto** (case-insensitive) contra
  los chapters/lessons ya en la DB. Si no matchea, la pregunta se inserta con
  `chapter_id = null` (queda huérfana — chequear antes de sync).
- `dificultad`: `fácil` | `medio` | `difícil` (acepta sin tildes y aliases en).
- Markdown + LaTeX con `$...$` permitidos en `enunciado`, `opcion_*`, `explicacion`.

Comandos:
```bash
# agrega al banco (no toca preguntas existentes)
python scripts/import_questions_csv.py algebra-lineal \
    "docs/cursos/generales/algebra-lineal/01. Espacio/Preguntas/espacio.csv"

# REEMPLAZA todas las preguntas de un capítulo (caso típico de mass-edit)
python scripts/import_questions_csv.py algebra-lineal \
    "docs/cursos/generales/algebra-lineal/01. Espacio/Preguntas/espacio.csv" \
    --replace-chapter ch-al-espacio

# dry-run: parsea, reporta errores, no escribe
python scripts/import_questions_csv.py algebra-lineal <csv> --dry-run
```

Validar después en `localhost:3007/quiz/<chapter_id>` o desde `/admin/preguntas`.

### Flujo 4 — Ajustes de metadata (sin tocar contenido)

Cambios chicos: título, descripción, orden, visibilidad, linked-chapters. Tres opciones:

**4a. Editar el seed y reseedear** (recomendado para cambios que querés versionar).
El seed actualiza `title`, `description`, `order`, etc. en el upsert del curso/capítulo.

**4b. Vía admin UI** (rápido, no queda en git):
- `https://remy.seremonta.store/admin/courses` o `localhost:3007/admin/courses`
- Editar campos desde el formulario.
- Si después corrés el seed, los cambios del UI se sobrescriben — **siempre
  reflejá en el seed los cambios que hagas vía UI** o trabajá solo en uno.

**4c. Linked chapters / cursos universitarios**: usar el endpoint admin
`POST /api/admin/courses/{course_id}/link-chapters` (ver
[backend/server.py:1761](backend/server.py#L1761)) o el dialog "Vincular capítulos"
en la admin UI. El patrón está documentado en [scripts/seed_uc_courses.py](scripts/seed_uc_courses.py).

**Ocultar un curso de estudiantes** (sin borrarlo):
- Toggle desde `/admin/courses` o setear `visible_to_students: false` en el doc.

---

## Verificación local antes de empujar

Checklist mínima antes de correr `sync_content_to_atlas.py --confirm`:

1. **Backend levantado**: `localhost:8001/api/courses` devuelve JSON con tu curso.
2. **Frontend levantado**: `localhost:3007/courses/<id>` carga sin errores 500/404.
3. **Lecciones renderizan**: abrir `/lesson/<id>` para cada lección modificada.
   Mirar que los bloques se vean OK (LaTeX, listas, ejemplos resueltos con pasos).
4. **Quiz funciona**: `/quiz/<chapter_id>` arranca y las preguntas se ven bien.
5. **Conteos**: `python scripts/run_seed.py` reporta el delta. Confirmá que
   coincide con lo que esperabas (ej: +1 capítulo, +4 lecciones, 0 huérfanos).

---

## Push a producción (un solo paso)

**Setup una sola vez:** agregá la URI de Atlas a `backend/.env`:

```
ATLAS_URL=mongodb+srv://remy_app:<PASS>@remy-prod.hwmj0fn.mongodb.net/?appName=remy-prod
```

(`backend/.env` está en `.gitignore`, así que el password no entra al repo.)

**De aquí en adelante el push es:**

```bash
# 1. dry-run — muestra el plan, no escribe
python scripts/sync_content_to_atlas.py

# 2. apply (un solo comando)
python scripts/sync_content_to_atlas.py --confirm
```

Si no querés persistir el URI en `.env`, podés pasarlo siempre como argumento:
`python scripts/sync_content_to_atlas.py "mongodb+srv://..." --confirm`.

Qué hace exactamente: dropea + reinserta las colecciones de **contenido**
(`courses`, `chapters`, `lessons`, `questions`, `library_universities`, `formulas`,
`pricing_config`, `app_settings`) en Atlas. Las colecciones de **usuarios**
(`users`, `subscriptions`, `payments`, `quiz_attempts`, `lesson_progress`,
`student_enrollments`, `user_achievements`, `user_sessions`, `trash`) **nunca
se tocan**. Source de verdad: [scripts/sync_content_to_atlas.py:29-51](scripts/sync_content_to_atlas.py#L29-L51).

Después del `--confirm` el script hace un smoke test contra
`https://api.remy.seremonta.store/api/courses` y avisa si los conteos divergen.
Verificá manualmente en `https://remy.seremonta.store` que el cambio se ve.

**No hace falta `git push`** para que el contenido vaya a prod — el sync va directo
a Atlas. Solo tocá `git push` si modificaste código en `backend/` o `frontend/`
(ver [DEPLOY.md](DEPLOY.md)).

---

## Rollback

Mongo Atlas M0 **no tiene backups automáticos**. La estrategia de rollback es:

1. Mantener el estado anterior en local (no corrás `run_seed.py` con cambios
   destructivos hasta no haber verificado los nuevos).
2. Si rompiste prod: revertí los seeds en git (`git checkout <commit-anterior> --
   backend/seeds/<curso>`), reseedeá local, y volvé a correr `sync_content_to_atlas.py
   --confirm`.

Plan B si el local también se ensució: usá `git log` + `git show` para reconstruir
el seed previo y reseedear. Por eso es importante que **todo cambio de contenido
viva en un seed versionado** y no solo en la admin UI.

---

## Áreas no-matemáticas

El patrón funciona igual; solo cambian dos cosas.

**Prompts de figura**: la constante `STYLE` en cada seed describe el estilo visual.
Adaptala según el área:

```python
# Matemáticas (default en _template):
STYLE = "Estilo: diagrama matemático educativo limpio, fondo blanco, líneas claras, etiquetas en español, notación matemática con buena tipografía. Acentos teal #06b6d4 y ámbar #f59e0b. Sin sombras dramáticas. Apto para libro universitario."

# Química:
STYLE = "Estilo: diagrama molecular limpio, fondo blanco, enlaces explícitos (líneas sólidas para covalentes, punteadas para puentes de H), átomos coloreados según convención CPK (C gris, O rojo, N azul, H blanco), etiquetas con tipografía sans-serif. Apto para libro universitario."

# Física:
STYLE = "Estilo: diagrama físico esquemático, fondo blanco, vectores como flechas etiquetadas (módulo + dirección), sistemas de referencia explícitos, líneas de fuerza/campo punteadas, colores: vectores azul #3b82f6, fuerzas rojo #dc2626. Apto para libro universitario."
```

**Programación**: NO uses bloques `figura` para mostrar código. Usá `texto` o
`ejemplo_resuelto` con triple-backtick:

```python
b("texto", body_md=(
    "Implementación recursiva:\n\n"
    "```python\n"
    "def factorial(n):\n"
    "    if n <= 1:\n"
    "        return 1\n"
    "    return n * factorial(n - 1)\n"
    "```\n\n"
    "Esta versión usa O(n) stack frames."
))
```

El frontend renderiza ``` como bloque de código con highlight (revisar
`frontend/src/components/Lesson*.jsx` si necesitás confirmar).

---

## Generación de imágenes

Las figuras se autorean con `image_url=""` y `prompt_image_md=<descripción>`.
La generación final es manual hoy: copiar el `prompt_image_md`, pegarlo en
ChatGPT Images (o tu generador), subir el resultado a Cloudinary, y rellenar
`image_url` con la URL final.

Auto-memory recordatorio: **no generar imágenes a mano (SVG inline o hotlinking
externo)** — siempre vía prompt + upload a Cloudinary.

Para hacerlo en bulk, listá las figuras pendientes con:
```bash
backend/venv/Scripts/python.exe -c "
import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv('backend/.env')
async def go():
    db = AsyncIOMotorClient(os.environ['MONGO_URL'])[os.environ['DB_NAME']]
    async for ls in db.lessons.find({}, {'id':1,'title':1,'blocks':1}):
        for blk in ls.get('blocks', []):
            if blk.get('type') == 'figura' and not blk.get('image_url'):
                print(f'{ls[\"id\"]}  {blk[\"id\"][:8]}  {ls[\"title\"]}')
asyncio.run(go())
"
```

---

## Gotchas (errores que ya pisamos en este flujo)

| Síntoma                                      | Causa                                                              | Fix                                                                    |
|----------------------------------------------|--------------------------------------------------------------------|------------------------------------------------------------------------|
| Cambio del seed no aparece en local          | Frontend cachea la respuesta del backend                           | Hard refresh (Ctrl+Shift+R) o reiniciar el dev server                  |
| Pregunta queda con `chapter_id = null`        | El nombre del capítulo en el CSV no matchea ningún chapter en DB   | Corregí el CSV a matchear el `title` exacto, o seedeá el capítulo primero |
| Seed corre OK pero sync a Atlas falla con SSL | IP de tu casa no autorizada en Atlas Network Access                | Atlas → Network Access → agregar tu IP, o dejar `0.0.0.0/0` (Render lo necesita igual) |
| Sync `--confirm` reporta MISMATCH            | Conexión flaky cortó un `insert_many` a la mitad                   | Volvé a correr `sync_content_to_atlas.py --confirm` — es idempotente   |
| Lección huérfana después de reseed           | Cambiaste el `id` de una lesson; el doc viejo quedó sin `chapter_id` válido | Borrá los huérfanos: `db.lessons.delete_many({chapter_id: <viejo>})`. Considerá usar `cleanup_*.py` style scripts |
| Pregunta duplicada después de re-import      | Corriste el script sin `--replace-chapter`                         | Borrá manualmente las dupes o reimportá con `--replace-chapter`        |
| Curso oculto a estudiantes después del sync  | El doc local tenía `visible_to_students: false`                    | Toggle desde `/admin/courses` o setear `true` en el seed y reseedear   |

---

## Cuándo Claude Code puede hacer esto solo (y cuándo pedir confirmación)

Bajo riesgo (Claude puede ejecutar sin pedir):
- Editar texto de bloques en seeds.
- Correr `run_seed.py` contra Mongo local.
- Correr `import_questions_csv.py --dry-run`.

Pedí confirmación antes de:
- `sync_content_to_atlas.py --confirm` (toca prod).
- `import_questions_csv.py --replace-course` o `--replace-chapter` (borrado).
- Borrar/renombrar IDs de capítulos o lecciones (puede dejar progreso de usuarios huérfano: `lesson_progress` referencia `lesson_id`).
- Cambios en `pricing_config` (hay un segundo lugar a tocar — ver [DEPLOY.md](DEPLOY.md#cambiar-precio-de-un-plan)).

---

## Referencias rápidas

| Necesito... | Mirar |
|---|---|
| Schema autoritativo de Course/Chapter/Lesson/Question | [backend/server.py:70-169](backend/server.py#L70-L169) |
| Plantilla de seed | [backend/seeds/_template/seed_capitulo_template.py](backend/seeds/_template/seed_capitulo_template.py) |
| Ejemplo completo de seed | [backend/seeds/algebra-lineal/seed_capitulo_1.py](backend/seeds/algebra-lineal/seed_capitulo_1.py) |
| Endpoint de import CSV (espejo del CLI) | [backend/server.py:1426](backend/server.py#L1426) |
| Linked chapters (cursos universitarios) | [backend/server.py:1761](backend/server.py#L1761), [scripts/seed_uc_courses.py](scripts/seed_uc_courses.py) |
| Sync local → Atlas | [scripts/sync_content_to_atlas.py](scripts/sync_content_to_atlas.py) |
| Deploy de código + infra | [DEPLOY.md](DEPLOY.md) |
