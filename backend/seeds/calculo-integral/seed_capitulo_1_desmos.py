"""
Agrega bloques grafico_desmos a dos lecciones del Capítulo 1 — Integrales:
- 1.1 Definición de integral: visualizador de sumas de Riemann.
- 1.3 Integral definida: visualizador de área como integral definida.

Idempotente: los bloques nuevos llevan `_mej: True`. Re-correr borra los
previos con esa marca y reinserta. NO toca los demás bloques.
"""
import asyncio
import os
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')


def b(type_, **fields):
    return {"id": str(uuid.uuid4()), "type": type_, "_mej": True, **fields}


# ---- Bloque para 1.1: Suma de Riemann interactiva ----
DESMOS_RIEMANN = b(
    "grafico_desmos",
    desmos_url="https://www.desmos.com/calculator/6wmcijqx2q?lang=es",
    expresiones=[],
    altura=480,
    guia_md=(
        "**Visualización interactiva de sumas de Riemann.** Modifica la función $f(x)$, los "
        "límites $a$ y $b$, el número de subintervalos $n$ y el tipo de muestreo (izquierdo, "
        "derecho, punto medio).\n\n"
        "**Qué observar:**\n\n"
        "- A medida que **aumentas $n$**, los rectángulos se vuelven más finos y la suma se acerca al área real.\n"
        "- Compara las tres elecciones de $x_i^*$ (izquierdo, derecho, medio) con la misma $f$ y $n$ — todas convergen al mismo valor cuando $n \\to \\infty$, pero algunas convergen más rápido.\n"
        "- Prueba con una función que tenga partes positivas y negativas: la suma se vuelve **área con signo**."
    ),
)

# ---- Bloque para 1.3: Área como integral definida ----
DESMOS_AREA_DEFINIDA = b(
    "grafico_desmos",
    desmos_url="https://www.desmos.com/calculator/pgyyjkzcbs?lang=es",
    expresiones=[],
    altura=480,
    guia_md=(
        "**Visualización del área como integral definida.** Cambia la función $f(x)$ y los "
        "límites $a$, $b$ para ver cómo se calcula geométricamente $\\int_a^b f(x) \\, dx$.\n\n"
        "**Qué observar:**\n\n"
        "- El área sombreada bajo la curva equivale al valor de la integral, calculable vía TFC: $F(b) - F(a)$.\n"
        "- Si $f(x) < 0$ en parte del intervalo, esa zona contribuye con **signo negativo** (área con signo).\n"
        "- Probar $f(x) = \\sin x$ entre $0$ y $2\\pi$ para ver cómo las áreas positivas y negativas se cancelan exactamente."
    ),
)


# ---- Inserciones por lección ----
# Cada entrada: lesson_id -> función que recibe la lista de bloques limpia
# (sin _mej previos) y devuelve la lista nueva con el bloque inyectado en
# la posición correcta.

def insert_after(blocks, predicate, new_block):
    """Inserta new_block justo después del primer bloque que cumple predicate."""
    for i, blk in enumerate(blocks):
        if predicate(blk):
            return blocks[:i+1] + [new_block] + blocks[i+1:]
    # Si no hay match, lo deja al final (antes del resumen si lo hay)
    resumen_idx = next((i for i, blk in enumerate(blocks) if blk.get("type") == "resumen"), len(blocks))
    return blocks[:resumen_idx] + [new_block] + blocks[resumen_idx:]


INSERTIONS = {
    "lec-integrales-1-1-definicion": (
        DESMOS_RIEMANN,
        # Insertar después de la definición "Suma de Riemann"
        lambda blk: blk.get("type") == "definicion" and blk.get("titulo") == "Suma de Riemann",
    ),
    "lec-integrales-1-3-definida": (
        DESMOS_AREA_DEFINIDA,
        # Insertar después del ejemplo "Re-calcular ∫₀¹ x² dx con TFC"
        lambda blk: blk.get("type") == "ejemplo_resuelto" and "Re-calcular" in (blk.get("titulo") or ""),
    ),
}


async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    for lesson_id, (new_block, predicate) in INSERTIONS.items():
        lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
        if not lesson:
            print(f"  ⚠ Lección no encontrada: {lesson_id}")
            continue

        # Limpiar bloques _mej previos
        cleaned = [blk for blk in lesson.get("blocks", []) if not blk.get("_mej")]
        # Insertar el nuevo
        new_blocks = insert_after(cleaned, predicate, new_block)

        await db.lessons.update_one({"id": lesson_id}, {"$set": {"blocks": new_blocks}})
        # Detectar dónde quedó
        pos = next((i for i, blk in enumerate(new_blocks) if blk.get("id") == new_block["id"]), -1)
        print(f"  ✓ {lesson['title']} — Desmos insertado en posición {pos+1}/{len(new_blocks)}")

    print()
    print("✅ Listo. Recarga el navegador para ver los Desmos interactivos.")


if __name__ == "__main__":
    asyncio.run(main())
