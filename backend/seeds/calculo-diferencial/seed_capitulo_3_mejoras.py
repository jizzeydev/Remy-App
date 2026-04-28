"""
Mejoras al Capítulo 3 — Aplicaciones de las Derivadas.

Mismo patrón que los seeds de mejoras anteriores: idempotente, no destructivo
sobre bloques originales.
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


def fig(prompt):
    return b("figura", image_url="", caption_md="", prompt_image_md=prompt)


def desmos(expressions, guide, height=400, url=""):
    return b("grafico_desmos", desmos_url=url, expresiones=expressions,
             guia_md=guide, altura=height)


def ej(titulo, enunciado, pistas, solucion):
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def formulas(titulo, body):
    return b("definicion", titulo=titulo, body_md=body)


STYLE = (
    "Estilo: diagrama educativo limpio, fondo blanco, líneas claras, etiquetas "
    "en español, notación matemática con buena tipografía. Acentos teal #06b6d4 "
    "y ámbar #f59e0b. Sin sombras dramáticas, sin texturas. Apto para libro universitario."
)


# -------------------- 3.1 Razones relacionadas --------------------
LECCION_3_1 = {
    "new_blocks": [
        fig(
            "Esquema de un tanque cónico invertido (vértice abajo). Cono con altura H y radio "
            "superior R marcados. Adentro, agua hasta una altura h con su radio en superficie r. "
            "Mostrar las relaciones por triángulos semejantes: r/h = R/H. Una flecha azul "
            "indicando que el agua entra a tasa dV/dt. Una flecha vertical en el nivel del agua "
            "indicando dh/dt (la incógnita). Etiquetas: 'H', 'R', 'h(t)', 'r(t)', 'dV/dt = entrada'. "
            + STYLE
        ),
        ej(
            titulo="Sombra que se alarga",
            enunciado=(
                "Un poste de luz tiene 5 m de altura. Una persona de 1.8 m de altura se aleja del "
                "poste a 1.5 m/s. ¿Con qué velocidad se alarga su sombra cuando está a 4 m del poste?"
            ),
            pistas=[
                "Dibuja el esquema: poste, persona, sombra. Forma dos triángulos semejantes.",
                "Sea $x$ la distancia persona-poste y $s$ la longitud de la sombra. Por semejanza: $\\dfrac{s}{1.8} = \\dfrac{x + s}{5}$.",
                "Despeja $s$ en función de $x$, luego deriva respecto a $t$.",
            ],
            solucion=(
                "**Semejanza:** $\\dfrac{s}{1.8} = \\dfrac{x + s}{5} \\implies 5s = 1.8(x + s) \\implies 3.2s = 1.8x \\implies s = \\dfrac{9}{16}x$.\n\n"
                "**Derivando respecto a $t$:** $\\dfrac{ds}{dt} = \\dfrac{9}{16} \\dfrac{dx}{dt}$.\n\n"
                "Con $\\dfrac{dx}{dt} = 1.5$ m/s: $\\dfrac{ds}{dt} = \\dfrac{9}{16} \\cdot 1.5 = 0.844$ m/s.\n\n"
                "**Observación:** la velocidad de la sombra **no depende de $x$** — siempre es la misma "
                "(esto cambia si hubiera más de una luz o el poste fuera distinto)."
            ),
        ),
        ej(
            titulo="Faro giratorio",
            enunciado=(
                "Un faro está a 1 km de la costa recta y gira a 4 revoluciones por minuto. ¿Con qué "
                "velocidad se mueve el haz de luz a lo largo de la costa cuando el haz forma un "
                "ángulo de $30°$ con la perpendicular a la costa?"
            ),
            pistas=[
                "Sea $\\theta$ el ángulo entre el haz y la perpendicular y $x$ la posición del haz en la costa.",
                "Por trigonometría: $x = \\tan\\theta$ (km).",
                "$\\dfrac{d\\theta}{dt} = 4 \\cdot 2\\pi = 8\\pi$ rad/min.",
            ],
            solucion=(
                "**Relación:** $x = \\tan\\theta$ (en km, asumiendo distancia $1$ km al faro).\n\n"
                "**Derivando:** $\\dfrac{dx}{dt} = \\sec^2\\theta \\cdot \\dfrac{d\\theta}{dt}$.\n\n"
                "**En $\\theta = 30°$:** $\\sec^2(30°) = \\dfrac{1}{\\cos^2(30°)} = \\dfrac{1}{(\\sqrt{3}/2)^2} = \\dfrac{4}{3}$.\n\n"
                "$\\dfrac{dx}{dt} = \\dfrac{4}{3} \\cdot 8\\pi = \\dfrac{32\\pi}{3} \\approx 33.5$ km/min."
            ),
        ),
    ],
    "verif_pistas": {
        0: "Si sustituyes los valores antes de derivar, las variables se vuelven constantes y derivar da $0$.",
    },
}


# -------------------- 3.2 Aproximaciones --------------------
LECCION_3_2 = {
    "new_blocks": [
        ej(
            titulo="Aproximar una raíz",
            enunciado="Estima $\\sqrt[3]{8.1}$ usando la linealización de $f(x) = \\sqrt[3]{x}$ en $a = 8$.",
            pistas=[
                "Calcula $f(8)$ y $f'(8)$. Recuerda $f'(x) = \\dfrac{1}{3} x^{-2/3}$.",
                "Linealización: $L(x) = f(a) + f'(a)(x - a)$.",
            ],
            solucion=(
                "$f(8) = 2$. $f'(x) = \\dfrac{1}{3 \\sqrt[3]{x^2}}$, así $f'(8) = \\dfrac{1}{3 \\cdot 4} = \\dfrac{1}{12}$.\n\n"
                "$L(x) = 2 + \\dfrac{1}{12}(x - 8)$. **Evaluando en $8.1$:** $L(8.1) = 2 + \\dfrac{0.1}{12} \\approx 2.00833$.\n\n"
                "Valor real: $\\sqrt[3]{8.1} \\approx 2.00829$. **Error: ~$0.00004$.** Excelente."
            ),
        ),
        ej(
            titulo="Error en una medición",
            enunciado=(
                "Se mide el lado de un cubo como $L = 10$ cm con error máximo de $\\pm 0.05$ cm. "
                "Estima el error máximo en el volumen calculado."
            ),
            pistas=[
                "$V = L^3$. Diferencial: $dV = 3L^2 \\, dL$.",
                "Sustituye $L = 10$ y $|dL| = 0.05$.",
            ],
            solucion=(
                "$dV = 3L^2 \\, dL = 3(100)(0.05) = 15 \\text{ cm}^3$.\n\n"
                "**Error relativo:** $\\dfrac{dV}{V} = \\dfrac{15}{1000} = 1.5\\%$. Equivale a $3 \\cdot \\dfrac{dL}{L} = 3 \\cdot 0.5\\% = 1.5\\%$. "
                "(El error relativo se triplica por el cubo.)"
            ),
        ),
    ],
    "verif_pistas": {
        0: "El error de la linealización crece a medida que $x$ se aleja de $a$.",
    },
}


# -------------------- 3.3 Máximos y mínimos --------------------
LECCION_3_3 = {
    "new_blocks": [
        fig(
            "Cuatro pequeñas gráficas en una grilla 2x2 ilustrando el Teorema del Valor Extremo. "
            "ARRIBA-IZQ: función continua en intervalo cerrado [a,b] con máximo y mínimo claramente "
            "marcados como puntos. ARRIBA-DER: función continua en intervalo abierto (a,b) que se "
            "acerca a un valor pero no lo alcanza (extremos no realizados). ABAJO-IZQ: función con "
            "discontinuidad en intervalo cerrado donde el TVE puede fallar. ABAJO-DER: función "
            "definida solo en (a,b] con asíntota vertical en a (no acotada, sin mínimo). Cada panel "
            "etiquetado: 'TVE aplica', 'no acotado abierto', 'discontinuidad', 'no acotado'. " + STYLE
        ),
        ej(
            titulo="Extremos en intervalo cerrado",
            enunciado="Halla los extremos absolutos de $f(x) = 2x^3 - 9x^2 + 12x$ en $[0, 3]$.",
            pistas=[
                "Calcula $f'(x)$ y resuelve $f'(x) = 0$ para hallar críticos en $(0, 3)$.",
                "Evalúa $f$ en críticos y en los bordes $x = 0$ y $x = 3$. El mayor es el máximo absoluto.",
            ],
            solucion=(
                "$f'(x) = 6x^2 - 18x + 12 = 6(x-1)(x-2)$. **Críticos:** $x = 1, x = 2$ (ambos en $(0, 3)$).\n\n"
                "**Evaluamos:** $f(0) = 0$, $f(1) = 2 - 9 + 12 = 5$, $f(2) = 16 - 36 + 24 = 4$, $f(3) = 54 - 81 + 36 = 9$.\n\n"
                "**Máximo absoluto:** $f(3) = 9$. **Mínimo absoluto:** $f(0) = 0$."
            ),
        ),
        ej(
            titulo="Crítico donde $f'$ no existe",
            enunciado="Halla los extremos absolutos de $f(x) = x^{2/3}$ en $[-8, 8]$.",
            pistas=[
                "$f'(x) = \\dfrac{2}{3} x^{-1/3}$. **No** está definida en $x = 0$ (pero $f(0)$ sí).",
                "Críticos del segundo tipo (donde $f'$ no existe) también cuentan.",
            ],
            solucion=(
                "$f'(x) = \\dfrac{2}{3\\sqrt[3]{x}}$. Nunca se anula, pero **no existe en $x = 0$** — crítico.\n\n"
                "**Evaluamos:** $f(-8) = (-8)^{2/3} = 4$, $f(0) = 0$, $f(8) = 4$.\n\n"
                "**Mínimo absoluto:** $f(0) = 0$. **Máximo absoluto:** $f(\\pm 8) = 4$ (alcanzado en ambos bordes)."
            ),
        ),
    ],
    "verif_pistas": {
        0: "Recuerda Fermat: extremo + derivable $\\Rightarrow$ $f'=0$. Pero la recíproca falla.",
    },
}


# -------------------- 3.4 TVM --------------------
LECCION_3_4 = {
    "new_blocks": [
        fig(
            "Diagrama del Teorema del Valor Medio. Eje x con marcas en a y b. Eje y. Una curva "
            "y = f(x) suave que pasa por los puntos A = (a, f(a)) y B = (b, f(b)). Una recta "
            "secante en color teal que une A y B. Una recta tangente en color ámbar en algún "
            "punto intermedio C = (c, f(c)) entre A y B, **paralela a la secante** (mismo "
            "ángulo). Etiquetas claras: 'A', 'B', 'C', 'recta secante (pendiente media)', "
            "'recta tangente (pendiente instantánea)'. Mostrar que ambas rectas tienen la "
            "misma pendiente. " + STYLE
        ),
        ej(
            titulo="Encontrar el c del TVM",
            enunciado="Verifica las hipótesis del TVM y encuentra el $c$ para $f(x) = x^2 - 2x$ en $[0, 3]$.",
            pistas=[
                "$f$ es polinomial: continua y derivable en todo $\\mathbb{R}$. Las hipótesis se cumplen.",
                "Calcula $\\dfrac{f(3) - f(0)}{3 - 0}$ y resuelve $f'(c) = $ ese valor.",
            ],
            solucion=(
                "**Pendiente de la secante:** $\\dfrac{f(3) - f(0)}{3} = \\dfrac{(9 - 6) - 0}{3} = 1$.\n\n"
                "**$f'(x) = 2x - 2$.** Resolviendo $f'(c) = 1$: $2c - 2 = 1 \\implies c = \\dfrac{3}{2}$.\n\n"
                "$c = \\dfrac{3}{2} \\in (0, 3)$. ✓"
            ),
        ),
        ej(
            titulo="Aplicación: $f' = g'$",
            enunciado=(
                "Sean $f(x) = \\arctan x + \\arctan(1/x)$ (para $x > 0$) y $g(x) = \\pi/2$. "
                "Demuestra que $f(x) = g(x)$ para todo $x > 0$."
            ),
            pistas=[
                "Por consecuencia 2 del TVM: si $f' = g'$ en un intervalo, entonces $f - g$ es constante.",
                "Calcula $f'(x)$ y muestra que vale $0$. Después evalúa $f$ en algún punto fácil (ej. $x = 1$).",
            ],
            solucion=(
                "**Derivamos $f$:** $f'(x) = \\dfrac{1}{1+x^2} + \\dfrac{1}{1 + (1/x)^2} \\cdot \\left(-\\dfrac{1}{x^2}\\right) = \\dfrac{1}{1+x^2} - \\dfrac{1}{x^2 + 1} = 0$.\n\n"
                "Por la consecuencia 1 del TVM, $f$ es constante en $(0, \\infty)$. **Evaluamos en $x = 1$:** "
                "$f(1) = \\arctan 1 + \\arctan 1 = \\dfrac{\\pi}{4} + \\dfrac{\\pi}{4} = \\dfrac{\\pi}{2}$.\n\n"
                "Así $f(x) = \\pi/2 = g(x)$ para todo $x > 0$. ∎"
            ),
        ),
    ],
    "verif_pistas": {
        0: "Rolle es el caso particular del TVM cuando $f(a) = f(b)$.",
    },
}


# -------------------- 3.5 Forma de la gráfica --------------------
LECCION_3_5 = {
    "new_blocks": [
        desmos(
            expressions=["f(x) = x^3 - 3x", "g(x) = 3x^2 - 3", "h(x) = 6x"],
            guide=(
                "Compara $f(x) = x^3 - 3x$ (azul) con su primera derivada $f'(x) = 3x^2 - 3$ (rojo) "
                "y su segunda derivada $f''(x) = 6x$ (verde). Donde $f' > 0$, $f$ crece; donde $f' < 0$, "
                "$f$ decrece. Donde $f'' > 0$, $f$ es cóncava arriba; donde $f'' < 0$, cóncava abajo. "
                "Los ceros de $f'$ corresponden a extremos locales de $f$; el cero de $f''$ ($x = 0$) "
                "es el punto de inflexión."
            ),
            height=420,
        ),
        ej(
            titulo="Análisis completo",
            enunciado=(
                "Analiza monotonía, extremos locales, concavidad y puntos de inflexión de "
                "$f(x) = x^4 - 8x^2$."
            ),
            pistas=[
                "$f'(x) = 4x^3 - 16x = 4x(x^2 - 4) = 4x(x-2)(x+2)$.",
                "$f''(x) = 12x^2 - 16$.",
                "Para clasificar críticos usa la segunda derivada en cada uno.",
            ],
            solucion=(
                "**Críticos** ($f' = 0$): $x = -2, 0, 2$.\n\n"
                "**Monotonía** (signo de $f'$):\n\n"
                "- $x < -2$: $f' = 4(-)(- )(-) = -$, decreciente.\n"
                "- $-2 < x < 0$: $f' = 4(-)(-)(+) = +$, creciente.\n"
                "- $0 < x < 2$: $f' = 4(+)(-)(+) = -$, decreciente.\n"
                "- $x > 2$: $f' = 4(+)(+)(+) = +$, creciente.\n\n"
                "**Extremos:** mínimos locales en $x = \\pm 2$ ($f(\\pm 2) = 16 - 32 = -16$); máximo local en $x = 0$ ($f(0) = 0$).\n\n"
                "**Concavidad** ($f'' = 12x^2 - 16 = 0$ en $x = \\pm 2/\\sqrt{3}$):\n\n"
                "- $|x| > 2/\\sqrt{3}$: $f'' > 0$, cóncava arriba.\n"
                "- $|x| < 2/\\sqrt{3}$: $f'' < 0$, cóncava abajo.\n\n"
                "**Inflexiones:** $x = \\pm 2/\\sqrt{3} \\approx \\pm 1.15$."
            ),
        ),
    ],
    "verif_pistas": {
        0: "Si $f'(c) = 0$ y $f''(c) > 0$, ¿qué tipo de extremo es?",
    },
}


# -------------------- 3.6 Graficar curvas --------------------
LECCION_3_6 = {
    "new_blocks": [
        ej(
            titulo="Análisis y esbozo completo",
            enunciado="Realiza el análisis completo y esboza la gráfica de $f(x) = \\dfrac{x}{x^2 + 1}$.",
            pistas=[
                "**Dominio:** $\\mathbb{R}$ (denominador siempre positivo).",
                "**Simetría:** verifica si $f(-x) = -f(x)$ (impar).",
                "**Asíntotas:** calcula $\\lim_{x \\to \\pm\\infty} f(x)$.",
                "**$f'$ y $f''$:** aplica regla del cociente con cuidado.",
            ],
            solucion=(
                "**Dominio:** $\\mathbb{R}$. **Intersecciones:** $f(0) = 0$, único punto $(0, 0)$. **Simetría:** $f(-x) = -f(x)$, **impar**.\n\n"
                "**Asíntotas:** horizontal $y = 0$ por ambos lados (grado den > grado num). Sin verticales.\n\n"
                "**$f'(x) = \\dfrac{(1)(x^2+1) - x(2x)}{(x^2+1)^2} = \\dfrac{1 - x^2}{(x^2+1)^2}$.** "
                "Críticos: $x = \\pm 1$. Signo: $f' > 0$ en $(-1, 1)$, $f' < 0$ fuera. **Máximo local en $(1, 1/2)$, mínimo local en $(-1, -1/2)$.**\n\n"
                "**$f''(x) = \\dfrac{2x(x^2 - 3)}{(x^2+1)^3}$.** Inflexiones en $x = 0$ y $x = \\pm\\sqrt{3}$. "
                "Concavidad arriba en $(-\\sqrt{3}, 0) \\cup (\\sqrt{3}, \\infty)$, abajo en el complemento.\n\n"
                "**Esbozo:** curva impar, pasa por origen, máximo en $(1, 1/2)$, mínimo en $(-1, -1/2)$, "
                "se acerca a $y = 0$ en ambos extremos del eje $x$."
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 3.7 Optimización --------------------
LECCION_3_7 = {
    "new_blocks": [
        fig(
            "Esquema de una caja sin tapa de base cuadrada. Vista en perspectiva isométrica simple. "
            "Base cuadrada con lado x marcado, altura h marcada en una arista lateral. La caja "
            "está abierta arriba (sin tapa). Una flecha indicando el volumen V = x²h. Etiquetas "
            "claras y limpias en español. " + STYLE
        ),
        ej(
            titulo="Cerca con un lado de río",
            enunciado=(
                "Un granjero tiene 200 m de cerca y quiere cercar un terreno rectangular con un río "
                "en uno de los lados (que no necesita cerca). ¿Qué dimensiones maximizan el área?"
            ),
            pistas=[
                "Sea $x$ el lado paralelo al río y $y$ los dos perpendiculares. **Restricción:** $x + 2y = 200$.",
                "Área: $A = xy$. Reduce a una variable usando la restricción.",
            ],
            solucion=(
                "De la restricción: $x = 200 - 2y$. **Área en función de $y$:** $A(y) = (200 - 2y)y = 200y - 2y^2$, con $y \\in (0, 100)$.\n\n"
                "$A'(y) = 200 - 4y = 0 \\implies y = 50$. $A''(y) = -4 < 0$ → **máximo**.\n\n"
                "**Dimensiones:** $y = 50$ m, $x = 100$ m. **Área máxima:** $5000$ m². "
                "(Notable: el lado paralelo al río es el doble que cada perpendicular.)"
            ),
        ),
        ej(
            titulo="Caja sin tapa con material fijo",
            enunciado=(
                "Se quiere construir una caja sin tapa de base cuadrada con $108$ m² de material. "
                "¿Qué dimensiones maximizan el volumen?"
            ),
            pistas=[
                "Sea $x$ el lado de la base y $h$ la altura. **Material:** $S = x^2 + 4xh = 108$.",
                "**Volumen:** $V = x^2 h$. Despeja $h$ de la restricción y sustituye.",
            ],
            solucion=(
                "De $x^2 + 4xh = 108$: $h = \\dfrac{108 - x^2}{4x}$.\n\n"
                "**Volumen:** $V(x) = x^2 \\cdot \\dfrac{108 - x^2}{4x} = \\dfrac{x(108 - x^2)}{4} = 27x - \\dfrac{x^3}{4}$.\n\n"
                "$V'(x) = 27 - \\dfrac{3x^2}{4} = 0 \\implies x^2 = 36 \\implies x = 6$ (positivo).\n\n"
                "$V''(x) = -\\dfrac{3x}{2} < 0$ → **máximo**.\n\n"
                "**Dimensiones:** $x = 6$ m, $h = \\dfrac{108 - 36}{24} = 3$ m. **Volumen máximo:** $108$ m³."
            ),
        ),
        ej(
            titulo="Punto más cercano sobre una parábola",
            enunciado="Halla el punto de la parábola $y = x^2$ más cercano al punto $(0, 1)$.",
            pistas=[
                "Distancia de $(x, x^2)$ a $(0, 1)$ al cuadrado: $D = x^2 + (x^2 - 1)^2$.",
                "Minimiza $D$ (es equivalente a minimizar la distancia y evita la raíz).",
            ],
            solucion=(
                "$D(x) = x^2 + (x^2 - 1)^2 = x^2 + x^4 - 2x^2 + 1 = x^4 - x^2 + 1$.\n\n"
                "$D'(x) = 4x^3 - 2x = 2x(2x^2 - 1) = 0 \\implies x = 0$ o $x = \\pm 1/\\sqrt{2}$.\n\n"
                "**Evaluamos** $D$ en cada crítico: $D(0) = 1$, $D(\\pm 1/\\sqrt{2}) = 1/4 - 1/2 + 1 = 3/4$.\n\n"
                "**Mínimo:** $x = \\pm 1/\\sqrt{2}$, dos puntos simétricos: $\\left(\\pm \\dfrac{1}{\\sqrt{2}}, \\dfrac{1}{2}\\right)$. "
                "Distancia mínima: $\\sqrt{3/4} = \\dfrac{\\sqrt{3}}{2}$."
            ),
        ),
    ],
    "verif_pistas": {
        0: "El truco de optimización es **siempre el mismo:** reducir a una variable usando la restricción.",
    },
}


IMPROVEMENTS = {
    "lec-aplicaciones-3-1-razones": LECCION_3_1,
    "lec-aplicaciones-3-2-aproximaciones": LECCION_3_2,
    "lec-aplicaciones-3-3-extremos": LECCION_3_3,
    "lec-aplicaciones-3-4-tvm": LECCION_3_4,
    "lec-aplicaciones-3-5-forma": LECCION_3_5,
    "lec-aplicaciones-3-6-graficar": LECCION_3_6,
    "lec-aplicaciones-3-7-optimizacion": LECCION_3_7,
}


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

        cleaned = [blk for blk in lesson.get("blocks", []) if not blk.get("_mej")]

        new_blocks = imp.get("new_blocks", [])
        ec_idx = next((i for i, blk in enumerate(cleaned) if blk.get("type") == "errores_comunes"), None)
        resumen_idx = next((i for i, blk in enumerate(cleaned) if blk.get("type") == "resumen"), len(cleaned))
        insert_at = ec_idx if ec_idx is not None else resumen_idx
        cleaned[insert_at:insert_at] = new_blocks

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
    print(f"✅ Capítulo 3 mejorado: {total_added} bloques nuevos, {total_pistas} pistas en verificaciones.")


if __name__ == "__main__":
    asyncio.run(main())
