"""
Mejoras al Capítulo 1 — Límites y Continuidad (curso Cálculo Diferencial).

Para cada lección:
- Agrega bloques `ejercicio` (problemas para resolver con pistas + solución)
- Agrega bloques `figura` con `prompt_image_md` listo para ChatGPT Images
- Agrega bloques `grafico_desmos` donde aporta
- Agrega bloque "Fórmulas clave" (definicion) donde aplique
- Agrega `pista_md` en preguntas de `verificacion` existentes

Idempotente: cada bloque nuevo lleva `_mej: True`. Al re-correr, se borran los previos
con esa marca y se reinsertan los actuales. Las preguntas de verificación reciben
sus `pista_md` por sobreescritura. NO se tocan los demás bloques (definiciones,
teoremas, ejemplos, etc.) — quedan intactos.

Si has editado pistas a mano desde admin, este seed las reemplazará por las nuestras.
"""
import asyncio
import os
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')


# ============ helpers ============
def b(type_, **fields):
    return {"id": str(uuid.uuid4()), "type": type_, "_mej": True, **fields}


def fig(prompt):
    """Figura con image_url vacío y prompt para ChatGPT Images."""
    return b("figura", image_url="", caption_md="", prompt_image_md=prompt)


def desmos(expressions, guide, height=400, url=""):
    return b("grafico_desmos", desmos_url=url, expresiones=expressions,
             guia_md=guide, altura=height)


def ej(titulo, enunciado, pistas, solucion):
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def formulas(titulo, body):
    """Bloque definicion usado como tabla de fórmulas clave."""
    return b("definicion", titulo=titulo, body_md=body)


# ============ Mejoras por lección ============
# Cada entrada: lesson_id -> {"new_blocks": [...], "verif_pistas": {idx: pista}}

# Estilo común para prompts de imágenes
STYLE = (
    "Estilo: diagrama educativo limpio, fondo blanco, líneas claras, etiquetas "
    "en español, notación matemática renderizada con buena tipografía. Acentos "
    "de color suaves (teal #06b6d4 y ámbar #f59e0b). Sin sombras dramáticas, "
    "sin texturas. Apto para libro universitario."
)


# -------------------- 1.1 Introducción intuitiva --------------------
LECCION_1_1 = {
    "new_blocks": [
        ej(
            titulo="Conjeturar un límite por tabla",
            enunciado=(
                "Conjetura el valor de $\\lim_{x \\to 0} \\dfrac{\\sin(3x)}{x}$ "
                "construyendo una tabla con $x = \\pm 0.1, \\pm 0.01, \\pm 0.001$."
            ),
            pistas=[
                "Calcula $\\sin(3x)/x$ para cada valor de $x$ usando una calculadora en **modo radianes**.",
                "Observa qué pasa con los valores tanto desde la izquierda como desde la derecha de $0$.",
            ],
            solucion=(
                "**Tabla:**\n\n"
                "| $x$ | $\\sin(3x)/x$ |\n|---|---|\n"
                "| $-0.1$ | $2.9552$ |\n"
                "| $-0.01$ | $2.9996$ |\n"
                "| $-0.001$ | $3.0000$ |\n"
                "| $0.001$ | $3.0000$ |\n"
                "| $0.01$ | $2.9996$ |\n"
                "| $0.1$ | $2.9552$ |\n\n"
                "Los valores tienden a $3$ desde ambos lados. **Conjetura:** "
                "$\\lim_{x \\to 0} \\dfrac{\\sin(3x)}{x} = 3$. (Más adelante lo confirmaremos "
                "algebraicamente: $\\dfrac{\\sin(3x)}{x} = 3 \\cdot \\dfrac{\\sin(3x)}{3x}$, "
                "y el segundo factor tiende a $1$.)"
            ),
        ),
        ej(
            titulo="Límites laterales de una función por tramos",
            enunciado=(
                "Sea $f(x) = \\begin{cases} x + 2 & x < 1 \\\\ x^2 & x \\geq 1 \\end{cases}$. "
                "Calcula $\\lim_{x \\to 1^-} f(x)$, $\\lim_{x \\to 1^+} f(x)$ y decide si "
                "$\\lim_{x \\to 1} f(x)$ existe."
            ),
            pistas=[
                "Para el lateral izquierdo, usa la fórmula del primer tramo.",
                "El bilateral existe sólo si los dos laterales coinciden.",
            ],
            solucion=(
                "**Lateral izquierdo** ($x < 1$): $\\lim_{x \\to 1^-}(x + 2) = 1 + 2 = 3$.\n\n"
                "**Lateral derecho** ($x \\geq 1$): $\\lim_{x \\to 1^+} x^2 = 1$.\n\n"
                "Como $3 \\neq 1$, el bilateral **no existe**. La función tiene un salto en $x = 1$."
            ),
        ),
    ],
    "verif_pistas": {
        0: "Recuerda: el límite habla del comportamiento *cerca de* $a$, no del valor en $a$.",
    },
}


# -------------------- 1.2 Definición formal ε-δ --------------------
LECCION_1_2 = {
    "new_blocks": [
        fig(
            "Diagrama matemático de la definición epsilon-delta de límite. Eje x horizontal y eje y vertical. "
            "Una curva continua y = f(x) con un punto destacado (a, L). En el eje y, marcar dos rectas "
            "horizontales en y = L - epsilon e y = L + epsilon, formando una banda horizontal sombreada "
            "en color teal claro. En el eje x, marcar x = a - delta y x = a + delta, formando una banda "
            "vertical sombreada en color ámbar claro. Mostrar cómo la curva, dentro de la banda vertical "
            "(excepto en x=a), queda contenida dentro de la banda horizontal. Etiquetas en español: "
            "'L', 'L-ε', 'L+ε' en el eje y; 'a', 'a-δ', 'a+δ' en el eje x. Punto (a,L) marcado con un "
            "círculo abierto. " + STYLE
        ),
        ej(
            titulo="Verificar un límite con ε-δ",
            enunciado=(
                "Demuestra que $\\lim_{x \\to 2}(3x - 1) = 5$ usando la definición $\\epsilon$-$\\delta$."
            ),
            pistas=[
                "Empieza por escribir $|f(x) - L|$ y simplificar: $|3x - 1 - 5| = |3x - 6| = 3|x - 2|$.",
                "Quieres que $3|x - 2| < \\epsilon$. Despeja $|x - 2|$.",
            ],
            solucion=(
                "Dado $\\epsilon > 0$, queremos hallar $\\delta > 0$ tal que $0 < |x - 2| < \\delta$ "
                "implique $|(3x - 1) - 5| < \\epsilon$.\n\n"
                "Manipulamos: $|(3x - 1) - 5| = |3x - 6| = 3|x - 2|$.\n\n"
                "Para que $3|x - 2| < \\epsilon$ basta tomar $|x - 2| < \\epsilon/3$.\n\n"
                "**Elegimos $\\delta = \\epsilon/3$.** Si $0 < |x - 2| < \\delta = \\epsilon/3$, entonces "
                "$|(3x - 1) - 5| = 3|x - 2| < 3 \\cdot \\epsilon/3 = \\epsilon$. ∎"
            ),
        ),
    ],
    "verif_pistas": {
        0: "$\\delta$ depende de $\\epsilon$ — no al revés. Imagina al adversario eligiendo $\\epsilon$ y tú respondiendo con un $\\delta$.",
    },
}


# -------------------- 1.3 Propiedades de los límites --------------------
LECCION_1_3 = {
    "new_blocks": [
        formulas(
            titulo="Fórmulas clave",
            body=(
                "Si $\\lim_{x \\to a} f(x) = L$ y $\\lim_{x \\to a} g(x) = M$:\n\n"
                "| Operación | Resultado |\n|---|---|\n"
                "| Suma/resta | $L \\pm M$ |\n"
                "| Producto | $L \\cdot M$ |\n"
                "| Cociente (si $M \\neq 0$) | $L/M$ |\n"
                "| Constante por función | $k \\cdot L$ |\n"
                "| Potencia | $L^n$ |\n"
                "| Raíz $n$-ésima (si $L \\geq 0$ o $n$ impar) | $\\sqrt[n]{L}$ |\n\n"
                "**Sustitución directa (continuidad):** si $f$ es polinomial, racional con denominador no nulo, "
                "trigonométrica, exponencial o logarítmica en su dominio, $\\lim_{x \\to a} f(x) = f(a)$."
            ),
        ),
        ej(
            titulo="Aplicar propiedades",
            enunciado="Calcula $\\lim_{x \\to 2} \\dfrac{x^3 - 4x + 1}{2x^2 + 3}$.",
            pistas=[
                "Es polinomial sobre polinomial. Verifica si el denominador es no nulo en $x = 2$.",
                "Si el denominador no se anula, sustitución directa.",
            ],
            solucion=(
                "El denominador $2(2)^2 + 3 = 11 \\neq 0$, así que la función es continua en $x = 2$.\n\n"
                "**Sustitución directa:** $\\dfrac{2^3 - 4 \\cdot 2 + 1}{2 \\cdot 4 + 3} = \\dfrac{8 - 8 + 1}{11} = \\dfrac{1}{11}$."
            ),
        ),
        ej(
            titulo="Producto de límites",
            enunciado=(
                "Sabiendo que $\\lim_{x \\to 0} \\dfrac{\\sin x}{x} = 1$, calcula "
                "$\\lim_{x \\to 0} \\dfrac{\\sin(5x)}{\\sin(2x)}$."
            ),
            pistas=[
                "Multiplica y divide por $5x$ y $2x$ adecuadamente para construir dos cocientes que tiendan a $1$.",
                "$\\dfrac{\\sin(5x)}{\\sin(2x)} = \\dfrac{\\sin(5x)}{5x} \\cdot \\dfrac{2x}{\\sin(2x)} \\cdot \\dfrac{5x}{2x}$.",
            ],
            solucion=(
                "Reescribimos:\n\n"
                "$$\\dfrac{\\sin(5x)}{\\sin(2x)} = \\underbrace{\\dfrac{\\sin(5x)}{5x}}_{\\to 1} "
                "\\cdot \\underbrace{\\dfrac{2x}{\\sin(2x)}}_{\\to 1} \\cdot \\dfrac{5}{2}$$\n\n"
                "Por la propiedad del producto de límites: $1 \\cdot 1 \\cdot \\dfrac{5}{2} = \\dfrac{5}{2}$."
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 1.4 Continuidad --------------------
LECCION_1_4 = {
    "new_blocks": [
        fig(
            "Tres gráficas pequeñas en una fila, cada una mostrando un tipo distinto de discontinuidad. "
            "PANEL 1 'Removible': curva continua con un círculo abierto (vacío) en un punto, "
            "y un círculo lleno desplazado verticalmente (o solo el agujero). PANEL 2 'De salto': "
            "función por tramos con dos pedazos a alturas distintas, con círculos rellenos en los "
            "extremos correctos según la definición. PANEL 3 'Esencial/infinita': curva que "
            "diverge a +infinito o -infinito acercándose a una asíntota vertical mostrada como "
            "línea punteada. Cada panel con su título debajo. Ejes x e y simples sin valores "
            "específicos. " + STYLE
        ),
        ej(
            titulo="Clasificar la discontinuidad",
            enunciado=(
                "Estudia la continuidad de $f(x) = \\dfrac{x^2 - 4}{x - 2}$ en $x = 2$ y, si es "
                "discontinua, clasifica el tipo de discontinuidad."
            ),
            pistas=[
                "Verifica primero el dominio: ¿está $f(2)$ definida?",
                "Calcula $\\lim_{x \\to 2} f(x)$ factorizando el numerador.",
            ],
            solucion=(
                "**Dominio:** $f(2)$ no está definida (denominador $0$). Discontinua en $x = 2$.\n\n"
                "**Cálculo del límite:** $\\dfrac{x^2 - 4}{x - 2} = \\dfrac{(x-2)(x+2)}{x-2} = x + 2$ "
                "para $x \\neq 2$. Así $\\lim_{x \\to 2} f(x) = 4$.\n\n"
                "El límite existe y es finito, pero $f(2)$ no está definida. **Discontinuidad removible** — "
                "se 'arregla' definiendo $f(2) = 4$."
            ),
        ),
        ej(
            titulo="Continuidad por tramos",
            enunciado=(
                "Halla el valor de $k$ que hace continua a "
                "$f(x) = \\begin{cases} kx + 3 & x \\leq 1 \\\\ x^2 + k & x > 1 \\end{cases}$ en $x = 1$."
            ),
            pistas=[
                "Para continuidad en $1$ se necesita: $\\lim_{x \\to 1^-} f(x) = \\lim_{x \\to 1^+} f(x) = f(1)$.",
                "Iguala las expresiones evaluadas en $1$ y despeja $k$.",
            ],
            solucion=(
                "**Lateral izquierdo y $f(1)$:** $k(1) + 3 = k + 3$.\n\n"
                "**Lateral derecho:** $1^2 + k = 1 + k$.\n\n"
                "Para continuidad: $k + 3 = 1 + k$, lo que da $3 = 1$. **¡Contradicción!**\n\n"
                "**Conclusión:** no existe ningún $k$ que haga $f$ continua en $1$. La diferencia entre "
                "las dos ramas es siempre de $2$ unidades, sin importar $k$."
            ),
        ),
    ],
    "verif_pistas": {
        0: "Tres condiciones deben cumplirse a la vez: $f(a)$ definida, límite existe, ambos coinciden.",
    },
}


# -------------------- 1.5 TVI --------------------
LECCION_1_5 = {
    "new_blocks": [
        fig(
            "Diagrama del Teorema del Valor Intermedio. Eje x horizontal con marcas en a y b. "
            "Eje y vertical con marcas en f(a) y f(b) (ambos a alturas distintas). Una curva "
            "continua de (a, f(a)) a (b, f(b)) cruzando un valor intermedio N que está entre "
            "f(a) y f(b). Marcar el punto (c, N) donde la curva cruza la altura N, con líneas "
            "punteadas horizontales en y=N y y=f(a), y=f(b), y vertical en x=c. La curva debe "
            "verse claramente continua (sin saltos). Etiquetas en español. " + STYLE
        ),
        ej(
            titulo="Localizar una raíz con el TVI",
            enunciado=(
                "Demuestra que la ecuación $x^3 - 3x + 1 = 0$ tiene al menos una raíz en $(0, 1)$."
            ),
            pistas=[
                "Define $f(x) = x^3 - 3x + 1$. Verifica que $f$ es continua en $[0, 1]$.",
                "Evalúa $f(0)$ y $f(1)$ y mira sus signos.",
            ],
            solucion=(
                "$f(x) = x^3 - 3x + 1$ es polinomial, así **continua en todo $\\mathbb{R}$** y en particular en $[0, 1]$.\n\n"
                "$f(0) = 1 > 0$ y $f(1) = 1 - 3 + 1 = -1 < 0$.\n\n"
                "Como $f$ es continua y los signos en los extremos son opuestos, por el **TVI** existe "
                "$c \\in (0, 1)$ con $f(c) = 0$. ∎\n\n"
                "**Bonus:** se puede afinar evaluando en $0.5$: $f(0.5) = 0.125 - 1.5 + 1 = -0.375 < 0$. "
                "Como $f(0) > 0$ y $f(0.5) < 0$, la raíz está en $(0, 0.5)$. Iterando se localiza con más precisión."
            ),
        ),
    ],
    "verif_pistas": {
        0: "El TVI requiere **continuidad en el cerrado**. Si falla, no se puede aplicar.",
    },
}


# -------------------- 1.6 Asíntotas --------------------
LECCION_1_6 = {
    "new_blocks": [
        ej(
            titulo="Asíntotas de una racional",
            enunciado="Halla todas las asíntotas (verticales, horizontales, oblicuas) de $f(x) = \\dfrac{x^2 + 1}{x - 1}$.",
            pistas=[
                "**Vertical:** dónde se anula el denominador (verifica que el numerador no se anule también).",
                "Compara grados de numerador y denominador: si difieren en $1$, hay oblicua, no horizontal.",
                "Para la oblicua, divide polinomios: $x^2 + 1 = (x-1)(x+1) + 2$.",
            ],
            solucion=(
                "**Vertical:** $x - 1 = 0$ en $x = 1$. Numerador en $1$ vale $2 \\neq 0$. **Asíntota vertical: $x = 1$.**\n\n"
                "**Horizontal:** grado numerador ($2$) > grado denominador ($1$), así $\\lim_{x \\to \\pm\\infty} f(x) = \\pm\\infty$. **No hay horizontal.**\n\n"
                "**Oblicua:** dividiendo polinomios, $\\dfrac{x^2+1}{x-1} = x + 1 + \\dfrac{2}{x-1}$. "
                "Como $\\dfrac{2}{x-1} \\to 0$ cuando $x \\to \\pm\\infty$, **asíntota oblicua: $y = x + 1$.**"
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 1.7 Resolver límites --------------------
LECCION_1_7 = {
    "new_blocks": [
        ej(
            titulo="Factorización clásica",
            enunciado="Calcula $\\lim_{x \\to 2} \\dfrac{x^3 - 8}{x^2 - 4}$.",
            pistas=[
                "Sustitución directa da $0/0$. Factoriza usando diferencia de cubos y diferencia de cuadrados.",
                "$x^3 - 8 = (x-2)(x^2 + 2x + 4)$ y $x^2 - 4 = (x-2)(x+2)$.",
            ],
            solucion=(
                "$$\\dfrac{x^3 - 8}{x^2 - 4} = \\dfrac{(x-2)(x^2 + 2x + 4)}{(x-2)(x+2)} = \\dfrac{x^2 + 2x + 4}{x+2}$$\n\n"
                "para $x \\neq 2$. Sustitución directa: $\\dfrac{4 + 4 + 4}{4} = \\dfrac{12}{4} = 3$."
            ),
        ),
        ej(
            titulo="Racionalización",
            enunciado="Calcula $\\lim_{x \\to 0} \\dfrac{\\sqrt{x + 4} - 2}{x}$.",
            pistas=[
                "Sustitución directa: $0/0$. Multiplica arriba y abajo por el conjugado $\\sqrt{x+4} + 2$.",
                "El numerador se simplifica: $(\\sqrt{x+4} - 2)(\\sqrt{x+4} + 2) = (x+4) - 4 = x$.",
            ],
            solucion=(
                "Multiplicamos por el conjugado:\n\n"
                "$$\\dfrac{\\sqrt{x+4} - 2}{x} \\cdot \\dfrac{\\sqrt{x+4} + 2}{\\sqrt{x+4} + 2} = \\dfrac{x}{x(\\sqrt{x+4} + 2)} = \\dfrac{1}{\\sqrt{x+4} + 2}$$\n\n"
                "Sustitución directa: $\\dfrac{1}{\\sqrt{4} + 2} = \\dfrac{1}{4}$."
            ),
        ),
        ej(
            titulo="Límite al infinito con raíces",
            enunciado="Calcula $\\lim_{x \\to +\\infty}(\\sqrt{x^2 + 4x} - x)$.",
            pistas=[
                "Es indeterminación $\\infty - \\infty$. Multiplica por el conjugado $\\sqrt{x^2+4x} + x$.",
                "Después divide numerador y denominador por $x$ (la potencia más alta), recordando $\\sqrt{x^2} = x$ para $x > 0$.",
            ],
            solucion=(
                "Multiplicando por el conjugado:\n\n"
                "$$\\dfrac{(x^2 + 4x) - x^2}{\\sqrt{x^2+4x} + x} = \\dfrac{4x}{\\sqrt{x^2+4x} + x}$$\n\n"
                "Dividiendo numerador y denominador por $x$ ($x > 0$, $\\sqrt{x^2+4x} = x\\sqrt{1 + 4/x}$):\n\n"
                "$$\\dfrac{4}{\\sqrt{1 + 4/x} + 1} \\to \\dfrac{4}{\\sqrt{1} + 1} = \\dfrac{4}{2} = 2$$"
            ),
        ),
    ],
    "verif_pistas": {
        0: "Sustitución directa daría $0/0$ — eso es indeterminación. ¿Qué técnica algebraica encaja con esa estructura?",
        1: "Es cociente de polinomios al infinito con grados iguales.",
    },
}


IMPROVEMENTS = {
    "lec-limites-1-1-introduccion-intuitiva": LECCION_1_1,
    "lec-limites-1-2-definicion-formal": LECCION_1_2,
    "lec-limites-1-3-propiedades": LECCION_1_3,
    "lec-limites-1-4-continuidad": LECCION_1_4,
    "lec-limites-1-5-tvi": LECCION_1_5,
    "lec-limites-1-6-asintotas": LECCION_1_6,
    "lec-limites-1-7-resolver": LECCION_1_7,
}


# ============ MAIN ============
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    total_added = 0
    total_pistas = 0
    for lesson_id, imp in IMPROVEMENTS.items():
        lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
        if not lesson:
            print(f"  ⚠ Lección no encontrada: {lesson_id}")
            continue

        # 1. Limpiar bloques de mejoras previos
        cleaned = [blk for blk in lesson.get("blocks", []) if not blk.get("_mej")]

        # 2. Insertar nuevos bloques antes del bloque resumen (o al final si no hay)
        new_blocks = imp.get("new_blocks", [])
        resumen_idx = next(
            (i for i, blk in enumerate(cleaned) if blk.get("type") == "resumen"),
            len(cleaned),
        )
        # Si hay errores_comunes, insertar antes de él
        ec_idx = next(
            (i for i, blk in enumerate(cleaned) if blk.get("type") == "errores_comunes"),
            None,
        )
        insert_at = ec_idx if ec_idx is not None else resumen_idx
        cleaned[insert_at:insert_at] = new_blocks

        # 3. Pistas en la primera verificación
        pistas = imp.get("verif_pistas", {})
        pistas_set = 0
        if pistas:
            for blk in cleaned:
                if blk.get("type") == "verificacion" and blk.get("preguntas"):
                    for idx, pista in pistas.items():
                        if idx < len(blk["preguntas"]):
                            blk["preguntas"][idx]["pista_md"] = pista
                            pistas_set += 1
                    break

        await db.lessons.update_one({"id": lesson_id}, {"$set": {"blocks": cleaned}})
        total_added += len(new_blocks)
        total_pistas += pistas_set
        print(f"  ✓ {lesson['title']} (+{len(new_blocks)} bloques, +{pistas_set} pistas)")

    print()
    print(f"✅ Capítulo 1 mejorado: {total_added} bloques nuevos, {total_pistas} pistas en verificaciones.")


if __name__ == "__main__":
    asyncio.run(main())
