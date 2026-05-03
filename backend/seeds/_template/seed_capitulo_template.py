"""
Plantilla para crear un capítulo nuevo desde cero.

CÓMO USARLA:
  1. Copiala a `backend/seeds/<curso-slug>/seed_capitulo_<N>.py`.
  2. Reemplazá los TODO marcados abajo: COURSE_*, CHAPTER_*, builders[].
  3. Para cada lección, completá `lesson_N_M()` agregando bloques con los helpers.
  4. Corré: `python scripts/run_seed.py backend/seeds/<curso-slug>/seed_capitulo_<N>.py`.
  5. Verificá en `localhost:3007/courses/<curso-slug>` y `/lesson/<lesson-id>`.
  6. Cuando esté OK, push a prod con `python scripts/sync_content_to_atlas.py "<URI>" --confirm`.

PATRÓN DE IDS (estables, no UUID — facilita debugging y idempotencia):
  - course_id  : kebab-case del slug temático ("algebra-lineal", "termodinamica")
  - chapter_id : "ch-<curso-corto>-<tema>"  ej: "ch-al-espacio", "ch-td-primera-ley"
  - lesson_id  : "lec-<curso-corto>-<cap>-<tema>"  ej: "lec-al-1-3-producto-cruz"

IDEMPOTENCIA: este script puede correr N veces sin duplicar datos.
  - Curso: upsert (update si existe, insert si no — preserva created_at).
  - Capítulo: delete + insert (atómico desde el punto de vista del lector).
  - Lecciones: delete + insert por id.
  - Preguntas: NO se manejan acá. Usá `scripts/import_questions_csv.py`.

CATEGORÍAS DE BLOQUE permitidas (matchear con frontend/src/lib/blockTypes.js):
  texto, definicion, teorema, intuicion, ejemplo_resuelto, grafico_desmos,
  figura, verificacion, errores_comunes, resumen, ejercicio.
"""
import asyncio
import os
import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')


# ============================================================================
# HELPERS — patrón estándar usado por todos los seeds existentes
# ============================================================================
def b(type_, **fields):
    """Construye un bloque con id UUID + tipo + campos arbitrarios."""
    return {"id": str(uuid.uuid4()), "type": type_, **fields}


def fig(prompt):
    """Bloque figura: image_url se llena después con el pipeline de imágenes
    (ChatGPT Images / Cloudinary). El prompt es lo que se le pasa al modelo."""
    return b("figura", image_url="", caption_md="", prompt_image_md=prompt)


def ej(titulo, enunciado, pistas, solucion):
    """Bloque ejercicio (no es ejemplo_resuelto — el alumno lo resuelve)."""
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def now():
    return datetime.now(timezone.utc).isoformat()


# Estilo común para prompts de figura matemática.
# Para áreas no-matemáticas reescribí esta constante:
#   - Química: "diagrama molecular limpio, enlaces explícitos, estructura de Lewis..."
#   - Física: "diagrama de cuerpo libre con flechas vectoriales etiquetadas..."
#   - Programación: NO uses figura; pasá el código en bloques `texto` con triple-backtick.
STYLE = (
    "Estilo: diagrama matemático educativo limpio, fondo blanco, líneas claras, "
    "etiquetas en español, notación matemática con buena tipografía. Acentos teal "
    "#06b6d4 y ámbar #f59e0b. Sin sombras dramáticas. Apto para libro universitario."
)


# ============================================================================
# TODO: cambiá estos identificadores
# ============================================================================
COURSE_ID = "TODO-curso-slug"           # ej: "termodinamica"
COURSE_TITLE = "TODO Título del curso"
COURSE_DESCRIPTION = "TODO descripción larga (soporta Markdown + KaTeX con $...$)."
COURSE_CATEGORY = "TODO categoría"      # ej: "Física", "Programación", "Matemáticas"
COURSE_LEVEL = "Avanzado"               # "Intermedio" | "Avanzado"
COURSE_MODULES_COUNT = 1                # cantidad TOTAL de capítulos del curso (no solo este)

CHAPTER_ID = "ch-TODO-tema"             # ej: "ch-td-primera-ley"
CHAPTER_TITLE = "TODO Título del capítulo"
CHAPTER_DESCRIPTION = "TODO descripción del capítulo."
CHAPTER_ORDER = 1                       # 1-indexed dentro del curso


# ============================================================================
# Lecciones — duplicá `lesson_template()` por cada lección que necesites
# ============================================================================
def lesson_template():
    """TODO: renombrá a `lesson_<cap>_<num>()` y completá."""
    blocks = [
        # --- TEXTO LIBRE (Markdown + KaTeX con $...$ y $$...$$) ---
        b("texto", body_md=(
            "TODO: párrafo de introducción. Soporta **negrita**, *cursiva*, listas, "
            "$inline\\ math$ y bloques $$f(x) = x^2$$.\n\n"
            "Buena práctica: terminá el bloque con un mini-objetivo de la lección."
        )),

        # --- DEFINICIÓN (resaltada visualmente en el frontend) ---
        b("definicion",
          titulo="TODO Nombre del concepto",
          body_md=(
              "TODO: enunciá la definición formal. Usá $\\LaTeX$ para notación.\n\n"
              "Cerrá con una nota intuitiva si ayuda."
          )),

        # --- TEOREMA (con o sin demostración) ---
        b("teorema",
          enunciado_md=(
              "**TODO Nombre del teorema.** Si X cumple Y, entonces Z."
          )),

        # --- INTUICIÓN (texto secundario, color suave) ---
        b("intuicion", body_md=(
            "TODO: la lectura informal del teorema/definición de arriba. "
            "Por qué tiene sentido geométrica/físicamente."
        )),

        # --- EJEMPLO RESUELTO (con pasos numerados y justificación) ---
        b("ejemplo_resuelto",
          titulo="TODO Título del ejemplo",
          problema_md="TODO Enunciado del problema concreto.",
          pasos=[
              {"accion_md": "TODO paso 1.",
               "justificacion_md": "TODO por qué este paso es válido.",
               "es_resultado": False},
              {"accion_md": "TODO paso 2.",
               "justificacion_md": "TODO.",
               "es_resultado": False},
              {"accion_md": "TODO resultado final.",
               "justificacion_md": "TODO comentario sobre el resultado.",
               "es_resultado": True},
          ]),

        # --- FIGURA (placeholder — image_url se llena después) ---
        fig(
            "TODO: prompt detallado para generar la imagen. Describí ejes, etiquetas, "
            "colores, perspectiva. " + STYLE
        ),

        # --- EJERCICIO (alumno resuelve, con pistas progresivas y solución) ---
        ej(
            "TODO Título del ejercicio",
            "TODO Enunciado.",
            ["TODO pista 1 (poco reveladora)",
             "TODO pista 2 (más reveladora)",
             "TODO pista 3 (casi la solución)"],
            "TODO Solución completa con pasos."
        ),

        # --- ERRORES COMUNES (lista de bullets en items_md) ---
        b("errores_comunes",
          items_md=[
              "TODO error frecuente 1 — explicación corta de por qué.",
              "TODO error frecuente 2.",
          ]),

        # --- RESUMEN (cierre de la lección, lista de bullets) ---
        b("resumen",
          puntos_md=[
              "TODO punto clave 1.",
              "TODO punto clave 2.",
              "TODO próxima lección: ...",
          ]),

        # --- (OPCIONAL) GRÁFICO DESMOS — embed interactivo ---
        # b("grafico_desmos",
        #   expresiones=["y = x^2", "y = 2x"],
        #   notas_md="TODO descripción de qué muestra el gráfico."),
    ]
    return {
        "id": "lec-TODO-cap-num-tema",
        "title": "TODO Título de la lección",
        "description": "TODO descripción corta (1 oración).",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 1,
    }


# ============================================================================
# MAIN — patrón idempotente. NO TOCAR salvo para agregar/quitar builders.
# ============================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    # Curso: upsert (preserva created_at en updates).
    course_doc = {
        "id": COURSE_ID,
        "title": COURSE_TITLE,
        "description": COURSE_DESCRIPTION,
        "category": COURSE_CATEGORY,
        "level": COURSE_LEVEL,
        "modules_count": COURSE_MODULES_COUNT,
        "rating": 4.8,
        "summary": COURSE_DESCRIPTION,
        "created_at": now(),
        "visible_to_students": True,
    }
    existing = await db.courses.find_one({"id": COURSE_ID})
    if existing:
        update_fields = {k: v for k, v in course_doc.items() if k != "created_at"}
        await db.courses.update_one({"id": COURSE_ID}, {"$set": update_fields})
        print(f"✓ Curso actualizado: {COURSE_TITLE}")
    else:
        await db.courses.insert_one(course_doc)
        print(f"✓ Curso creado: {COURSE_TITLE}")

    # Capítulo: delete + insert (idempotente, no acumula stale fields).
    await db.chapters.delete_one({"id": CHAPTER_ID})
    chapter = {
        "id": CHAPTER_ID,
        "course_id": COURSE_ID,
        "title": CHAPTER_TITLE,
        "description": CHAPTER_DESCRIPTION,
        "order": CHAPTER_ORDER,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {CHAPTER_TITLE}")

    # Lecciones: delete + insert por id.
    # TODO: agregá los builders de las lecciones de este capítulo, en orden.
    builders = [lesson_template]

    total_blocks = 0
    total_figs = 0
    for build in builders:
        data = build()
        await db.lessons.delete_one({"id": data["id"]})
        lesson = {
            "id": data["id"],
            "chapter_id": CHAPTER_ID,
            "title": data["title"],
            "description": data["description"],
            "blocks": data["blocks"],
            "order": data["order"],
            "duration_minutes": data["duration_minutes"],
            "created_at": now(),
        }
        await db.lessons.insert_one(lesson)
        total_blocks += len(data["blocks"])
        total_figs += sum(1 for blk in data["blocks"] if blk.get("type") == "figura")
        print(f"  ✓ {data['title']} ({len(data['blocks'])} bloques, ~{data['duration_minutes']} min)")

    print()
    print(f"✅ {CHAPTER_TITLE}: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    print("URLs locales para verificar:")
    print(f"  http://localhost:3007/courses/{COURSE_ID}")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
