"""
Seed para la lección 1.0 — Integrales impropias (prerrequisito).

Se inserta en el Capítulo 1 — Series y Sucesiones del curso Cálculo Multivariable
con `order = 0`, antes de las 8 lecciones reales del capítulo. Necesaria para
entender el test de la integral en la lección 1.3 (criterio $p$ de impropias
↔ criterio $p$ de series).

Es un repaso compacto, no el desarrollo completo (ese vive en Cálculo Integral 2.7).

Idempotente: borra y re-inserta esta lección. NO toca las otras 8.
"""
import asyncio
import os
import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')


def b(type_, **fields):
    return {"id": str(uuid.uuid4()), "type": type_, **fields}


def fig(prompt):
    return b("figura", image_url="", caption_md="", prompt_image_md=prompt)


def ej(titulo, enunciado, pistas, solucion):
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def now():
    return datetime.now(timezone.utc).isoformat()


STYLE = (
    "Estilo: diagrama matemático educativo limpio, fondo blanco, líneas claras, "
    "etiquetas en español, notación matemática con buena tipografía. Acentos teal "
    "#06b6d4 y ámbar #f59e0b. Sin sombras dramáticas, sin texturas. Apto para "
    "libro universitario."
)


def lesson_1_0():
    blocks = [
        b("texto", body_md=(
            "Esta lección es un **repaso compacto** de integrales impropias del curso de Cálculo Integral. "
            "La traemos aquí porque es **prerrequisito directo** del test de la integral (lección 1.3) y "
            "del criterio $p$ para series (lección 1.2): la convergencia de $\\sum 1/n^p$ y de $\\int 1/x^p \\, dx$ están conectadas.\n\n"
            "Si quieres el desarrollo completo (con todos los ejemplos y casos), revisa la lección "
            "**2.7 de Cálculo Integral** — aquí solo cubrimos lo necesario para Series.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Reconocer los **dos tipos** de integrales impropias.\n"
            "- Calcular impropias del Tipo 1 ($\\int_a^\\infty f \\, dx$).\n"
            "- Aplicar el **criterio $p$**, que se traslada idéntico a series."
        )),

        b("definicion",
          titulo="Tipo 1 — Límites infinitos",
          body_md=(
              "Cuando un límite de integración es infinito, definimos la integral como un límite:\n\n"
              "$$\\int_a^\\infty f(x) \\, dx = \\lim_{t \\to \\infty} \\int_a^t f(x) \\, dx$$\n\n"
              "Si el límite existe y es finito, la integral **converge** a ese valor. Si no, **diverge**.\n\n"
              "**Análogamente** para $\\int_{-\\infty}^b f \\, dx$ y $\\int_{-\\infty}^\\infty f \\, dx = \\int_{-\\infty}^c f + \\int_c^\\infty f$ (ambas deben converger)."
          )),

        b("definicion",
          titulo="Tipo 2 — Integrando no acotado",
          body_md=(
              "Cuando $f$ tiene una **asíntota vertical** en algún punto del intervalo, también pasamos a un límite:\n\n"
              "**Asíntota en $b$ (extremo derecho):** $\\int_a^b f \\, dx = \\lim_{t \\to b^-} \\int_a^t f \\, dx$.\n\n"
              "**Asíntota en $a$ (extremo izquierdo):** $\\int_a^b f \\, dx = \\lim_{t \\to a^+} \\int_t^b f \\, dx$.\n\n"
              "**Asíntota en $c \\in (a, b)$:** partir en $c$ y exigir que ambas convergen."
          )),

        b("ejemplo_resuelto",
          titulo="Convergente: $\\int_1^\\infty \\dfrac{1}{x^2} \\, dx$",
          problema_md="Calcular y determinar si converge.",
          pasos=[
              {"accion_md": "**Por definición:** $\\lim_{t \\to \\infty} \\int_1^t \\dfrac{1}{x^2} \\, dx = \\lim_{t \\to \\infty} \\left[-\\dfrac{1}{x}\\right]_1^t = \\lim_{t \\to \\infty}\\left(1 - \\dfrac{1}{t}\\right) = 1$.",
               "justificacion_md": "Antiderivada $-1/x$ y límite finito.",
               "es_resultado": False},
              {"accion_md": "**Converge a $1$.**",
               "justificacion_md": "Es un caso clásico — y es el análogo continuo de $\\sum 1/n^2$ (que converge a $\\pi^2/6$, valor distinto pero convergencia equivalente).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Divergente: $\\int_1^\\infty \\dfrac{1}{x} \\, dx$",
          problema_md="Determinar si converge.",
          pasos=[
              {"accion_md": "$\\int_1^t \\dfrac{1}{x} \\, dx = \\ln t - \\ln 1 = \\ln t$.",
               "justificacion_md": "Antiderivada $\\ln|x|$.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{t \\to \\infty} \\ln t = +\\infty$. **Diverge.**",
               "justificacion_md": "**Sorpresa famosa:** $1/x$ tiende a $0$ (lentamente), pero su integral hasta infinito es infinita. Análogo: $\\sum 1/n$ (armónica) también diverge.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Criterio $p$ (clave para series)",
          enunciado_md=(
              "**Para integrales en $[1, \\infty)$:**\n\n"
              "$$\\int_1^\\infty \\dfrac{1}{x^p} \\, dx \\quad \\text{converge si } p > 1, \\text{ diverge si } p \\leq 1$$\n\n"
              "**Para integrales en $(0, 1]$:**\n\n"
              "$$\\int_0^1 \\dfrac{1}{x^p} \\, dx \\quad \\text{converge si } p < 1, \\text{ diverge si } p \\geq 1$$\n\n"
              "**Atención al \"al revés\":** en infinito $p > 1$ converge, en $0$ es $p < 1$. Las dos condiciones son **opuestas** y memorizarlas conjuntamente es lo más útil."
          ),
          demostracion_md=(
              "Para $p \\neq 1$: $\\int_1^t \\dfrac{1}{x^p} \\, dx = \\dfrac{x^{1-p}}{1-p}\\Big|_1^t = \\dfrac{t^{1-p} - 1}{1-p}$.\n\n"
              "Cuando $t \\to \\infty$: si $p > 1$, $1-p < 0$ y $t^{1-p} \\to 0$ → converge a $\\dfrac{1}{p-1}$. Si $p < 1$, $t^{1-p} \\to \\infty$ → diverge.\n\n"
              "Para $p = 1$: $\\ln t \\to \\infty$ → diverge."
          )),

        b("intuicion",
          titulo="Conexión con series — adelanto de 1.2 y 1.3",
          body_md=(
              "El **mismo** criterio $p$ vale para series: $\\sum_{n=1}^\\infty \\dfrac{1}{n^p}$ converge si $p > 1$, diverge si $p \\leq 1$.\n\n"
              "**¿Por qué?** Porque $f(x) = 1/x^p$ es continua, positiva y decreciente en $[1, \\infty)$. "
              "Por el **test de la integral** (lección 1.3), la serie y la integral comparten convergencia.\n\n"
              "Es decir, los dos criterios $p$ — el de integrales y el de series — **son el mismo teorema disfrazado**."
          )),

        b("verificacion",
          intro_md="Verifica el criterio:",
          preguntas=[
              {
                  "enunciado_md": "$\\int_1^\\infty \\dfrac{1}{x^{1.5}} \\, dx$ es:",
                  "opciones_md": ["Convergente", "Divergente", "Igual a $\\infty$", "No se puede determinar"],
                  "correcta": "A",
                  "pista_md": "$p = 1.5 > 1$ — caso convergente del criterio $p$ en $[1, \\infty)$.",
                  "explicacion_md": (
                      "$p = 1.5 > 1$ → **converge**. Su valor es $\\dfrac{1}{p-1} = \\dfrac{1}{0.5} = 2$."
                  ),
              },
              {
                  "enunciado_md": "$\\int_0^1 \\dfrac{1}{x^{0.5}} \\, dx$ es:",
                  "opciones_md": ["Convergente", "Divergente", "Igual a $\\infty$", "No se puede determinar"],
                  "correcta": "A",
                  "pista_md": "Es Tipo 2 con asíntota en $0$. En $(0, 1]$, $1/x^p$ converge si $p < 1$.",
                  "explicacion_md": (
                      "$p = 0.5 < 1$ → **converge** (criterio $p$ en $(0,1]$). Atención: opuesto al de infinito. $\\int_0^1 x^{-1/2} \\, dx = [2\\sqrt{x}]_0^1 = 2$."
                  ),
              },
          ]),

        ej(
            titulo="Aplicar el criterio",
            enunciado="Determina si $\\int_1^\\infty \\dfrac{1}{x^3} \\, dx$ converge y, en ese caso, calcula su valor.",
            pistas=[
                "$p = 3 > 1$ → criterio $p$ dice converge.",
                "Calcula $\\lim_{t \\to \\infty} \\int_1^t x^{-3} \\, dx$ explícitamente.",
            ],
            solucion=(
                "$\\int_1^t x^{-3} \\, dx = \\left[\\dfrac{x^{-2}}{-2}\\right]_1^t = -\\dfrac{1}{2t^2} + \\dfrac{1}{2}$.\n\n"
                "$\\lim_{t \\to \\infty}\\left(\\dfrac{1}{2} - \\dfrac{1}{2t^2}\\right) = \\dfrac{1}{2}$. **Converge a $1/2$.**"
            ),
        ),

        fig(
            "Dos paneles lado a lado ilustrando los dos tipos de integrales impropias. "
            "Panel izquierdo (a): la curva y = 1/x^2 en color teal #06b6d4 sobre el eje x desde "
            "x = 1 hacia la derecha. El área bajo la curva está sombreada en teal translúcido y "
            "se extiende hasta el infinito, con una flecha hacia la derecha y etiqueta "
            "'∫_1^∞ 1/x² dx = 1 (converge)'. Panel derecho (b): la curva y = 1/√x con asíntota "
            "vertical en x = 0 marcada con línea ámbar #f59e0b discontinua. El área entre x = 0 "
            "y x = 1 sombreada en teal translúcido, etiqueta '∫_0^1 1/√x dx = 2 (converge)'. "
            "Ejes con marcas claras. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir las dos formas del criterio $p$**: en $[1, \\infty)$ converge si $p > 1$; en $(0, 1]$ converge si $p < 1$. Son **opuestas**.",
              "**Aplicar Barrow ingenuamente** cuando hay asíntota interior. Ejemplo trampa: $\\int_{-1}^1 1/x^2 \\, dx$ — hay que partir en $0$ y cada trozo diverge.",
              "**Pensar que $f \\to 0 \\Rightarrow$ integral converge.** $1/x \\to 0$ y aún así $\\int_1^\\infty 1/x \\, dx$ diverge.",
              "**Olvidar verificar continuidad** del integrando antes de usar el TFC.",
          ]),

        b("resumen",
          puntos_md=[
              "**Tipo 1:** límites infinitos. Pasar a límite: $\\int_a^\\infty f = \\lim_{t \\to \\infty} \\int_a^t f$.",
              "**Tipo 2:** integrando no acotado. Reemplazar el extremo problemático por límite.",
              "**Criterio $p$ en $[1, \\infty)$:** $\\int 1/x^p$ converge $\\iff p > 1$.",
              "**Criterio $p$ en $(0, 1]$:** $\\int 1/x^p$ converge $\\iff p < 1$ (opuesto).",
              "**Conexión con series:** el mismo criterio $p$ vale para $\\sum 1/n^p$ (lección 1.3 lo formaliza con el test de la integral).",
              "**Si quieres más** (formas indeterminadas, asíntotas interiores, comparación de impropias): Cálculo Integral lección 2.7.",
          ]),
    ]
    return {
        "id": "lec-mvar-1-0-impropias",
        "title": "Integrales impropias (prerrequisito)",
        "description": "Repaso de integrales impropias y criterio $p$, prerrequisito para el test de la integral y series $p$.",
        "blocks": blocks,
        "duration_minutes": 30,
        "order": 0,
    }


async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    chapter_id = "ch-series-sucesiones"
    chapter = await db.chapters.find_one({"id": chapter_id})
    if not chapter:
        raise SystemExit(f"Capítulo {chapter_id} no existe. Corre primero seed_calculo_multivariable_chapter_1.py")

    data = lesson_1_0()
    await db.lessons.delete_one({"id": data["id"]})
    lesson = {
        "id": data["id"],
        "chapter_id": chapter_id,
        "title": data["title"],
        "description": data["description"],
        "blocks": data["blocks"],
        "order": data["order"],
        "duration_minutes": data["duration_minutes"],
        "created_at": now(),
    }
    await db.lessons.insert_one(lesson)
    print(f"✓ Lección 1.0 insertada (order=0): {data['title']} ({len(data['blocks'])} bloques, ~{data['duration_minutes']} min)")
    print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
