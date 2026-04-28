# Workflow — Curado e importación de CSVs de preguntas

Este documento describe cómo **curar** los CSVs de preguntas que vienen de la base de datos anterior y **importarlos** al sistema actual mediante el panel de admin de Remy.

> **Por qué es necesario curar:** los CSVs originales fueron generados con los nombres de capítulos y lecciones de la versión anterior del producto. Los nombres ahora son distintos (ver lección modelo en [`README.md`](README.md)), por lo que el matching automático del importador falla y las preguntas quedan sin asignar a su lección.

---

## 1. Formato del CSV

El endpoint `/api/admin/questions/import-csv/{course_id}` espera un CSV con esta estructura **exacta** en la primera línea (header):

```csv
capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion
```

Una fila ejemplo:

```csv
Límites y Continuidad,Introducción intuitiva al límite,facil,"¿Qué representa $\lim_{x\to a} f(x) = L$?","El valor al que se aproxima $f(x)$",...,A,"Por la definición intuitiva..."
```

### Reglas por columna

| Columna | Tipo | Reglas |
|---|---|---|
| `capitulo` | string | **Debe coincidir exactamente** con el `title` del capítulo en MongoDB (case-insensitive, trim). Si no coincide, la pregunta queda **sin asignar** (se muestra en "Sin Categorizar" en el admin). |
| `leccion` | string | **Debe coincidir exactamente** con el `title` de la lección. Misma regla de matching. |
| `dificultad` | enum | Acepta: `facil`, `fácil`, `medio`, `dificil`, `difícil`, `easy`, `medium`, `hard`. Default: `medio`. |
| `enunciado` | string | Markdown + LaTeX inline con `$...$`. Comas y comillas dentro deben ir entre comillas dobles `"..."`. |
| `opcion_a` | string | Texto de la opción A (sin el prefijo "A) "). |
| `opcion_b` | string | Idem B. |
| `opcion_c` | string | Idem C. **Opcional pero recomendado** (las preguntas suelen tener 4 opciones). |
| `opcion_d` | string | Idem D. **Opcional pero recomendado**. |
| `respuesta_correcta` | enum | `A`, `B`, `C` o `D`. Mayúscula. |
| `explicacion` | string | Markdown + LaTeX. Idéntica codificación que `enunciado`. |

### Quirks importantes

- **Valor absoluto en LaTeX**: usar `\lvert x \rvert` o `|x|`. Ambos renderizan bien.
- **Decimales**: el CSV original usa `0{,}999` (con `{,}` para separar miles). KaTeX lo renderiza correctamente como `0,999`.
- **Encoding**: UTF-8. El backend prueba varios encodings como fallback (`utf-8`, `utf-8-sig`, `latin-1`, `cp1252`), pero **siempre exportar/guardar en UTF-8** para evitar caracteres rotos.
- **Saltos de línea dentro de celdas**: encerrar el campo entre comillas dobles. Mayoría de editores de CSV lo manejan correctamente.

---

## 2. Estructura de carpetas

Los CSVs viven dentro de cada capítulo del curso, en una subcarpeta `Preguntas/`:

```
docs/cursos/generales/
└── <slug-curso>/
    └── NN. <nombre del capítulo>/         ← padding 0, sentence-case en español
        ├── Clases/
        │   └── NN. <tema de la lección>/
        │       ├── Clase.pdf
        │       └── Apuntes.pdf
        ├── Ejercicios/
        │   └── NN. <tema>/
        │       ├── Enunciados.pdf
        │       └── Soluciones.pdf
        └── Preguntas/                      ← acá viven los CSVs
            ├── Preguntas.csv               ← CSV original (sin curar)
            └── Preguntas curadas.csv       ← CSV curado, listo para importar
```

Convenciones:
- **Carpetas**: `NN.` con padding 0; sentence-case en español (sólo capitalizar primera palabra y nombres propios como `L'Hôpital`).
- **Archivos PDF**: nombres cortos y predecibles (`Clase.pdf`, `Apuntes.pdf`, `Enunciados.pdf`, `Soluciones.pdf`).
- **Mantener siempre el CSV original** (`Preguntas.csv`). El curado se llama `Preguntas curadas.csv` y va al lado.

---

## 3. Workflow completo de curado

### Paso 1 — Inspeccionar el CSV original

Antes de cualquier cosa, necesitamos saber qué nombres de capítulo y lección aparecen, para mapearlos a los actuales.

```bash
cd backend
PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe -c "
import csv
from collections import Counter
path = '../docs/cursos/generales/<curso>/<NN. capitulo>/Preguntas/Preguntas.csv'
with open(path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
combos = Counter((r['capitulo'], r['leccion']) for r in rows)
print(f'Total filas: {len(rows)}')
for combo, n in combos.most_common():
    print(f'  {combo}: {n}')
"
```

Output esperado: una lista de pares `(capítulo, lección)` con el conteo de preguntas en cada uno. Lo usás para construir los mapeos en el siguiente paso.

### Paso 2 — Confirmar los títulos actuales del sistema

Revisar el script de seed del capítulo (por ejemplo `backend/seed_chapter_1_limites.py`) o consultar la DB directamente:

```bash
cd backend
PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe -c "
import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv('.env')
async def t():
    c = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = c[os.environ['DB_NAME']]
    chs = await db.chapters.find({'course_id': 'calculo-diferencial'}, {'_id': 0, 'id': 1, 'title': 1}).to_list(50)
    for ch in chs:
        print(f'Capítulo: {ch[\"title\"]}')
        ls = await db.lessons.find({'chapter_id': ch['id']}, {'_id': 0, 'title': 1, 'order': 1}).sort('order').to_list(50)
        for l in ls:
            print(f'  - {l[\"title\"]}')
asyncio.run(t())
"
```

### Paso 3 — Construir el script de curado

Adaptar este template, completando los mapeos:

```python
# scripts/curate_<archivo>.py (o ejecutar inline)
import csv

src = '../docs/cursos/generales/<curso>/<NN. capitulo>/Preguntas/Preguntas.csv'
dst = '../docs/cursos/generales/<curso>/<NN. capitulo>/Preguntas/Preguntas curadas.csv'

# Mapeo: <nombre en CSV> → <nombre en sistema>
chapter_map = {
    'Límites': 'Límites y Continuidad',
}
lesson_map = {
    'Introducción': 'Introducción intuitiva al límite',
    'Definición épsilon-delta': 'Definición formal del límite ($\\epsilon$-$\\delta$)',
    'Propiedades de los límites': 'Propiedades de los límites',
    # ... resto de las lecciones
}

with open(src, encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

with open(dst, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        if r['capitulo'] in chapter_map:
            r['capitulo'] = chapter_map[r['capitulo']]
        if r['leccion'] in lesson_map:
            r['leccion'] = lesson_map[r['leccion']]
        writer.writerow(r)

print(f'Curado: {len(rows)} filas → {dst}')
```

> **Si una entrada del mapeo falta** (porque el CSV trae un capítulo/lección que aún no construimos), las filas correspondientes quedarán con el nombre original y el importador no las va a vincular. Aparecerán en el admin como "Sin Categorizar". Hay que decidir: o construir esa lección primero, o descartar esas filas, o asignarlas manualmente luego.

### Paso 4 — Verificar el CSV curado antes de importar

Test rápido vía Python (sin tocar la DB de producción):

```python
# scripts/verify_preguntas_curadas.py
import csv
path = '../docs/cursos/generales/<curso>/<NN. capitulo>/Preguntas/Preguntas curadas.csv'
with open(path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Sanidad: no hay filas con campos clave vacíos
assert all(r['enunciado'] for r in rows), 'Hay enunciados vacíos'
assert all(r['respuesta_correcta'] in ('A','B','C','D') for r in rows), 'Respuesta inválida'
assert all(r['opcion_a'] and r['opcion_b'] for r in rows), 'Faltan opciones A o B'
print(f'OK: {len(rows)} filas válidas')
```

### Paso 5 — Importar desde el admin

1. Entrar al admin: `http://localhost:3007/admin/login` (en local) o el dominio de producción.
2. **Banco de Preguntas** → seleccionar el curso (ej. "Cálculo Diferencial").
3. Click **Importar CSV** (botón arriba a la derecha).
4. Subir el archivo `Preguntas curadas.csv`.
5. El sistema responde con `created_count` y `errors_count`. Verificar que:
   - `created_count` coincide con el número de filas del CSV.
   - `errors_count` es `0`.
6. Si todo bien, las preguntas aparecen distribuidas por capítulo y lección. Si hay errores, el toast muestra los primeros 10.

### Paso 6 — Verificar que ninguna quedó "Sin Categorizar"

En la pantalla de gestión de preguntas del curso, scroll al final. Si aparece la sección **"Sin Categorizar (Importadas CSV)"** con preguntas adentro, significa que el matching falló para esas filas. Causas típicas:

- Un nombre de capítulo o lección en el CSV no estaba en el `chapter_map` / `lesson_map`.
- El nombre tiene un espacio extra, mayúscula distinta, o un carácter invisible.
- La lección aún no existe en el sistema (no se ha construido).

Solución: arreglar el mapeo, regenerar el CSV curado, borrar las preguntas mal-asignadas (o todas las del curso si es seguro), y reimportar.

---

## 4. Borrado y re-importación (idempotencia)

El importador **no detecta duplicados**: si subes el mismo CSV dos veces, vas a tener cada pregunta dos veces. Para re-importar limpiamente:

```bash
cd backend
PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe -c "
import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv('.env')
async def t():
    c = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = c[os.environ['DB_NAME']]
    # Borra TODAS las preguntas del curso, sin importar fuente
    n = await db.questions.delete_many({'course_id': 'calculo-diferencial'})
    print(f'Borradas {n.deleted_count} preguntas')
asyncio.run(t())
"
```

> ⚠️ Esto borra **todas** las preguntas del curso, incluyendo las creadas manualmente desde el admin. Si solo querés borrar las del último import CSV, agrega el filtro `'source': 'csv_import'` (ese campo lo setea automáticamente el importador). Pero en general, durante el desarrollo del banco es más simple borrar todo y reimportar.

---

## 5. Workflow recomendado para nuevos cursos / capítulos

Cuando termines de construir un capítulo y te toque cargarle preguntas:

1. **Consigue el CSV** de la base de datos vieja, vía export desde mongoview.emergent.host o donde lo tengas.
2. **Guárdalo** como `Preguntas.csv` dentro de `docs/cursos/generales/<curso>/<NN. capitulo>/Preguntas/` (sin tocar el original).
3. **Inspecciona los nombres** que usa (paso 1 del workflow).
4. **Anota los nombres del sistema actual** (paso 2).
5. **Genera `Preguntas curadas.csv`** ejecutando el script de curado con los mapeos correctos.
6. **Importa desde el admin** (paso 5).
7. **Verificá distribución** (paso 6). Si hay "Sin Categorizar", iterá hasta que todas estén bien.

Para **CSVs grandes** (cientos de preguntas), tiene sentido escribir el script de curado como un archivo Python en `backend/scripts/curate_<curso>_<capitulo>.py` y versionarlo. Para CSVs chicos (decenas), un one-liner inline alcanza.

---

## 6. Mapeos ya conocidos (referencia rápida)

### Cálculo Diferencial — Capítulo "Límites y Continuidad"

```python
chapter_map = {
    'Límites': 'Límites y Continuidad',
}
lesson_map = {
    'Introducción': 'Introducción intuitiva al límite',
    'Definición épsilon-delta': 'Definición formal del límite ($\\epsilon$-$\\delta$)',
    'Propiedades de los límites': 'Propiedades de los límites',
    'Continuidad de funciones': 'Continuidad de funciones',
    'Teorema del valor intermedio': 'Teorema del Valor Intermedio',
    'Asíntotas': 'Asíntotas',
    'Resolver límites': 'Resolver límites: estrategia y técnicas',
}
```

CSV curado de referencia: [`docs/cursos/generales/calculo-diferencial/01. Límites y Continuidad/Preguntas/Preguntas curadas.csv`](generales/calculo-diferencial/01.%20L%C3%ADmites%20y%20Continuidad/Preguntas/Preguntas%20curadas.csv) — 140 filas, 20 preguntas por lección, todas con dificultad balanceada (~30% fácil, ~40% medio, ~30% difícil).

### Otros capítulos

> _Por completar a medida que construyamos los capítulos restantes (Derivadas, Aplicaciones de las Derivadas, etc.). Agregar cada nuevo `chapter_map` / `lesson_map` aquí para futura referencia._

---

## 7. Sobre el banco de preguntas y los simulacros

Las preguntas importadas vía este flujo viven en la colección `questions` de MongoDB y se usan para **dos propósitos**:

1. **Simulacros del estudiante**: cuando un alumno hace un simulacro de un curso, Remy elige preguntas aleatorias del banco (filtradas por capítulo/lección si corresponde).
2. **Visibilidad en el admin**: el admin puede editar, eliminar o agregar preguntas manualmente desde la sección Banco de Preguntas.

**Estas preguntas son distintas de los bloques `verificacion`** dentro de las lecciones. Los `verificacion` son inline, embebidos en la lección, y sirven para retrieval practice durante el estudio. Las preguntas del banco son la herramienta de evaluación post-lección. **No mezclar:** cada herramienta tiene su propósito y carga distinta.

---

**Última actualización:** 2026-04-26
**Mantenedor:** Jesús (Se Remonta)
