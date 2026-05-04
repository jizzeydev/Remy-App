"""
Seed del curso Introducción al Cálculo — Capítulo 4: Sucesiones.
6 lecciones:
  4.1 Límites y convergencia (definición ε-N, propiedad arquimediana)
  4.2 Operaciones con límites (acotada × nula, álgebra de límites, cocientes de polinomios)
  4.3 Teorema del Sandwich (cotas, raíz n-ésima, r^n → 0)
  4.4 Sucesiones monótonas y acotadas (axioma de completitud, recurrencias)
  4.5 Límites relevantes (e, jerarquía de crecimiento, proposición del cociente)
  4.6 Límites infinitos (definición, álgebra, indeterminaciones)

ENFOQUE: primer encuentro riguroso con la idea de límite. Énfasis en la definición
ε-N, en técnicas algebraicas de cálculo (amplificación, racionalización, sandwich)
y en la jerarquía de crecimiento (polinomial ≪ exponencial ≪ factorial). Sienta
las bases para el cálculo diferencial.

Idempotente.
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
    "#06b6d4 y ámbar #f59e0b. Sin sombras dramáticas. Apto para libro universitario."
)


# =====================================================================
# 4.1 Límites y convergencia
# =====================================================================
def lesson_4_1():
    blocks = [
        b("texto", body_md=(
            "El estudio de los **límites de sucesiones** es uno de los pilares fundamentales del "
            "análisis matemático. Comprender cómo se comportan los términos de una sucesión cuando el "
            "índice $n$ crece indefinidamente nos permite formalizar las nociones intuitivas de "
            "**aproximación** y **tendencia**, dotándolas de rigor matemático mediante la definición "
            "**épsilon-N**.\n\n"
            "**Objetivos:**\n\n"
            "- Definición formal $\\varepsilon$-$N$ y su interpretación geométrica.\n"
            "- **Principio de Arquímedes** como herramienta para construir demostraciones.\n"
            "- Distinguir sucesiones convergentes y divergentes.\n"
            "- Demostrar **unicidad del límite** y que **toda convergente es acotada**."
        )),

        b("definicion",
          titulo="Sucesión",
          body_md=(
              "Una **sucesión** $\\{a_n\\}$ es una función cuyo dominio es $\\mathbb{N}$. Sus valores "
              "$a_1, a_2, a_3, \\ldots$ se llaman **términos**. La gráfica de una sucesión consiste "
              "en puntos aislados $(1, a_1), (2, a_2), \\ldots$\n\n"
              "**Motivación geométrica.** La sucesión $a_n = \\dfrac{n}{n+1}$ produce $\\tfrac{1}{2}, "
              "\\tfrac{2}{3}, \\tfrac{3}{4}, \\ldots$ — los términos se acercan al valor $1$ sin alcanzarlo. "
              "La distancia $|1 - a_n| = \\dfrac{1}{n+1}$ se hace arbitrariamente pequeña al crecer $n$. "
              "Esto motiva escribir $\\lim_{n\\to\\infty} a_n = 1$."
          )),

        b("definicion",
          titulo="Límite de una sucesión (definición ε-N)",
          body_md=(
              "Una sucesión $\\{a_n\\}$ tiene **límite** $L$, y se escribe $\\lim_{n\\to\\infty} a_n = L$, "
              "si para todo $\\varepsilon > 0$ existe un natural $N$ tal que\n\n"
              "$$n > N \\Rightarrow |a_n - L| < \\varepsilon.$$\n\n"
              "En símbolos:\n\n"
              "$$(\\forall \\varepsilon > 0)(\\exists N \\in \\mathbb{N})(n > N \\Rightarrow |a_n - L| < \\varepsilon).$$\n\n"
              "**Interpretación geométrica:** sin importar cuán pequeño sea $\\varepsilon$, a partir de "
              "algún índice $N$ todos los términos quedan dentro de la **franja horizontal** $(L - \\varepsilon, L + \\varepsilon)$. "
              "Un $\\varepsilon$ más pequeño generalmente requiere un $N$ más grande."
          )),

        fig(
            "Diagrama de definición ε-N: ejes coordenados con el eje horizontal etiquetado 'n' "
            "(índice) y el eje vertical 'aₙ'. Una recta horizontal punteada en y = L (color teal "
            "#06b6d4, etiqueta 'L = 1'). Una franja horizontal sombreada suavemente entre L-ε y "
            "L+ε (etiqueta 'L+ε' arriba, 'L-ε' abajo, color teal claro). Puntos azules dispersos "
            "representando los términos aₙ = n/(n+1) que se acercan a L: para n=1 (a=0.5), n=2 "
            "(0.67), n=3 (0.75), n=5 (0.83), n=10 (0.91), etc., con los puntos posteriores a un "
            "valor N marcado en el eje x todos dentro de la franja. Línea vertical punteada en "
            "n=N (color ámbar #f59e0b, etiqueta 'N'). Anotación: 'todos los términos con n > N "
            "caen dentro de la franja (L-ε, L+ε)'. Título: 'Convergencia ε-N: la franja como "
            "tolerancia'. " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Principio de Arquímedes.** $\\mathbb{N}$ no está acotado superiormente. Equivalentemente, "
              "para todo $a \\in \\mathbb{R}$ existe $n \\in \\mathbb{N}$ con $a < n$ (**propiedad "
              "arquimediana**).\n\n"
              "**Estrategia para demostraciones $\\varepsilon$-$N$:** dado $\\varepsilon > 0$, despejar "
              "la condición $|a_n - L| < \\varepsilon$ en términos de $n$, obtener una cota $n > f(\\varepsilon)$, "
              "e invocar Arquímedes para asegurar que existe $N \\in \\mathbb{N}$ con $N > f(\\varepsilon)$."
          )),

        b("ejemplo_resuelto",
          titulo="Demostración: $\\lim_{n\\to\\infty} \\dfrac{1}{n} = 0$",
          problema_md=(
              "Demuestre que $\\lim_{n\\to\\infty} \\dfrac{1}{n} = 0$ usando la definición."
          ),
          pasos=[
              {"accion_md": (
                  "Dado $\\varepsilon > 0$, por la propiedad arquimediana existe $N \\in \\mathbb{N}$ "
                  "con $\\dfrac{1}{N} < \\varepsilon$."
               ),
               "justificacion_md": "Aplicamos Arquímedes a $\\dfrac{1}{\\varepsilon}$: existe $N > \\dfrac{1}{\\varepsilon}$.",
               "es_resultado": False},
              {"accion_md": (
                  "Si $n > N$, entonces $\\dfrac{1}{n} < \\dfrac{1}{N}$. Luego:\n\n"
                  "$|a_n - L| = \\left|\\dfrac{1}{n} - 0\\right| = \\dfrac{1}{n} < \\dfrac{1}{N} < \\varepsilon.$"
               ),
               "justificacion_md": "Por monotonía de $1/n$ y la cota arquimediana.",
               "es_resultado": False},
              {"accion_md": (
                  "Por tanto $\\boxed{\\lim_{n\\to\\infty} \\dfrac{1}{n} = 0.} \\quad\\square$"
               ),
               "justificacion_md": "Aplicamos la definición ε-N.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Demostración con manipulación algebraica",
          problema_md=(
              "Demuestre que la sucesión $a_n = 1 + \\dfrac{5}{n+1}$ converge a $L = 1$."
          ),
          pasos=[
              {"accion_md": (
                  "$|a_n - 1| = \\left|\\dfrac{5}{n+1}\\right| = \\dfrac{5}{n+1}$. Imponemos "
                  "$\\dfrac{5}{n+1} < \\varepsilon$:\n\n"
                  "$\\dfrac{5}{n+1} < \\varepsilon \\iff n + 1 > \\dfrac{5}{\\varepsilon} \\iff n > \\dfrac{5}{\\varepsilon} - 1.$"
               ),
               "justificacion_md": "Despejamos $n$.",
               "es_resultado": False},
              {"accion_md": (
                  "Por la propiedad arquimediana, existe $N \\in \\mathbb{N}$ con $N > \\dfrac{5}{\\varepsilon} - 1$. "
                  "Para todo $n > N$:\n\n"
                  "$|a_n - 1| = \\dfrac{5}{n+1} < \\varepsilon$ ✓"
               ),
               "justificacion_md": "Construcción del $N$ requerido.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\boxed{\\lim_{n\\to\\infty} \\left(1 + \\dfrac{5}{n+1}\\right) = 1.} \\quad\\square$"
               ),
               "justificacion_md": "Por la definición.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Convergencia y divergencia",
          body_md=(
              "Una sucesión que posee límite se llama **convergente**. En caso contrario se llama **divergente**."
          )),

        b("teorema",
          enunciado_md=(
              "**Unicidad del límite.** Una sucesión no puede converger a dos límites diferentes.\n\n"
              "**Idea de la prueba.** Si $\\lim a_n = L$ y $L \\neq M$, eligiendo $\\varepsilon = |L-M|/2$ "
              "los intervalos $(L-\\varepsilon, L+\\varepsilon)$ y $(M-\\varepsilon, M+\\varepsilon)$ son "
              "disjuntos. La sucesión no puede estar eventualmente en ambos."
          )),

        b("definicion",
          titulo="Sucesión acotada",
          body_md=(
              "Una sucesión $\\{a_n\\}$ está **acotada** si existe $M > 0$ tal que $|a_n| \\leq M$ para "
              "todo $n \\in \\mathbb{N}$. Geométricamente, todos los términos pertenecen al intervalo $[-M, M]$.\n\n"
              "**Ejemplo:** $a_n = (-1)^n$ está acotada (basta $M = 1$). $b_n = \\dfrac{n}{n+1}$ "
              "está acotada (basta $M = 1$)."
          )),

        b("teorema",
          enunciado_md=(
              "**Toda sucesión convergente es acotada.**\n\n"
              "**Demostración.** Sea $\\lim a_n = L$. Tomando $\\varepsilon = 1$, existe $N$ tal que "
              "$|a_n| < |L| + 1$ para $n > N$. Sean $a, b$ el menor y mayor de $\\{a_1, \\ldots, a_N, L-1, L+1\\}$. "
              "Tomando $M = \\max(|a|, |b|)$ se tiene $|a_n| \\leq M$ para todo $n$. $\\quad\\square$\n\n"
              "**Observación importante.** El **recíproco es falso**: una sucesión acotada no necesariamente "
              "converge. Por ejemplo, $a_n = (-1)^n$ es acotada pero divergente."
          )),

        b("intuicion", body_md=(
            "**Criterio de divergencia (contrarrecíproco).** Si $\\{a_n\\}$ no está acotada, entonces "
            "es divergente. Es útil porque a menudo es más fácil verificar no acotación que demostrar "
            "directamente que no hay límite. Por ejemplo, $a_n = n$ no está acotada (Arquímedes), "
            "luego diverge."
        )),

        ej(
            "Demostrar convergencia con ε-N",
            "Demuestre que $\\lim_{n\\to\\infty} \\dfrac{2n+1}{n+3} = 2$.",
            [
                "Calculá $|a_n - 2|$ explícitamente.",
                "Despejá $n$ de $|a_n - 2| < \\varepsilon$.",
                "Invocá Arquímedes para construir el $N$.",
            ],
            (
                "$|a_n - 2| = \\left|\\dfrac{2n+1 - 2(n+3)}{n+3}\\right| = \\dfrac{5}{n+3}$.\n\n"
                "Imponemos $\\dfrac{5}{n+3} < \\varepsilon \\iff n > \\dfrac{5}{\\varepsilon} - 3$.\n\n"
                "Por Arquímedes existe $N > \\dfrac{5}{\\varepsilon} - 3$. Para $n > N$: $|a_n - 2| < \\varepsilon$. $\\quad\\square$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica la definición de límite y convergencia:",
          preguntas=[
              {"enunciado_md": "En la definición $\\forall \\varepsilon > 0,\\ \\exists N \\in \\mathbb{N},\\ \\forall n \\geq N: |a_n - L| < \\varepsilon$, ¿de qué depende $N$?",
               "opciones_md": [
                   "Solo de $L$",
                   "Solo de la sucesión",
                   "De $\\varepsilon$ (cuanto menor $\\varepsilon$, mayor $N$)",
                   "Es independiente de todo",
               ],
               "correcta": "C",
               "pista_md": "El orden de los cuantificadores importa.",
               "explicacion_md": "$N$ depende de $\\varepsilon$ porque cuanto más estricta la cota, más términos se necesitan para 'caer' dentro."},
              {"enunciado_md": "¿La sucesión $a_n = (-1)^n$ es convergente?",
               "opciones_md": [
                   "Sí, converge a $0$",
                   "Sí, converge a $1$",
                   "No, oscila entre $1$ y $-1$",
                   "Sí, converge a $\\pm 1$",
               ],
               "correcta": "C",
               "pista_md": "Tiene dos puntos de acumulación distintos.",
               "explicacion_md": "Es acotada (entre $-1$ y $1$) pero NO convergente: $|a_n - L| < \\varepsilon$ no puede cumplirse para ningún $L$ con $\\varepsilon < 1$."},
              {"enunciado_md": "¿Qué relación hay entre 'sucesión convergente' y 'sucesión acotada'?",
               "opciones_md": [
                   "Convergente $\\Rightarrow$ acotada, pero no al revés",
                   "Acotada $\\Rightarrow$ convergente, pero no al revés",
                   "Son equivalentes",
                   "No hay relación",
               ],
               "correcta": "A",
               "pista_md": "Pensa en $(-1)^n$: acotada pero no converge.",
               "explicacion_md": "Toda sucesión convergente es acotada (teorema). El recíproco es FALSO: $(-1)^n$ es acotada y no converge."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir el orden de cuantificadores:** la definición es $\\forall \\varepsilon (\\exists N (\\ldots))$, NO $\\exists N (\\forall \\varepsilon (\\ldots))$. El $N$ depende de $\\varepsilon$.",
              "**Pensar que $|a_n - L|$ tiene que ser $0$:** basta con que sea menor que cualquier $\\varepsilon > 0$ a partir de cierto índice.",
              "**Asumir que acotada implica convergente:** $a_n = (-1)^n$ es acotada pero diverge.",
              "**Olvidar la propiedad arquimediana:** sin ella no se puede garantizar la existencia de $N \\in \\mathbb{N}$ con $N > f(\\varepsilon)$.",
              "**Confundir convergencia con valor:** una sucesión converge a $L$ no significa que algún término sea exactamente $L$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Sucesión:** función $\\mathbb{N} \\to \\mathbb{R}$.",
              "**Límite ε-N:** $\\forall \\varepsilon > 0 \\, \\exists N \\, (n > N \\Rightarrow |a_n - L| < \\varepsilon)$.",
              "**Propiedad arquimediana:** $\\mathbb{N}$ no acotado en $\\mathbb{R}$.",
              "**Unicidad:** el límite, si existe, es único.",
              "**Convergente $\\Rightarrow$ acotada;** recíproco falso.",
              "**Criterio de divergencia:** no acotada $\\Rightarrow$ divergente.",
              "**Próxima lección:** operaciones algebraicas con límites.",
          ]),
    ]
    return {
        "id": "lec-ic-4-1-limites-convergencia",
        "title": "Límites y convergencia",
        "description": "Definición ε-N de límite, propiedad arquimediana, unicidad y relación entre convergencia y acotación.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 1,
    }


# =====================================================================
# 4.2 Operaciones con límites
# =====================================================================
def lesson_4_2():
    blocks = [
        b("texto", body_md=(
            "Calcular límites mediante la definición ε-N es laborioso. En esta lección desarrollamos "
            "**propiedades algebraicas** que permiten descomponer límites complejos en partes simples, "
            "y técnicas estándar para cocientes de polinomios y expresiones con raíces.\n\n"
            "**Objetivos:**\n\n"
            "- **Teorema del producto:** sucesión nula × acotada $\\to 0$.\n"
            "- Propiedades algebraicas: suma, producto, cociente.\n"
            "- $\\lim_{n\\to\\infty} \\dfrac{1}{n^p} = 0$ para $p > 0$.\n"
            "- Técnicas de **amplificación** y **racionalización**."
        )),

        b("teorema",
          enunciado_md=(
              "**Producto nula × acotada.** Si $\\lim a_n = 0$ y $\\{b_n\\}$ es **acotada**, entonces\n\n"
              "$$\\lim_{n\\to\\infty} a_n \\cdot b_n = 0.$$\n\n"
              "**Demostración.** Existe $c > 0$ con $|b_n| \\leq c$ para todo $n$. Dado $\\varepsilon > 0$, "
              "como $a_n \\to 0$, existe $N$ con $|a_n| < \\varepsilon/c$ para $n > N$. Entonces:\n\n"
              "$|a_n b_n| = |a_n||b_n| < \\dfrac{\\varepsilon}{c} \\cdot c = \\varepsilon. \\quad\\square$\n\n"
              "**Notable:** $\\{b_n\\}$ NO necesita converger, basta con que esté acotada."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicación: $\\lim \\dfrac{\\sin(n)}{n}$",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\dfrac{\\sin(n)}{n}$."
          ),
          pasos=[
              {"accion_md": (
                  "Escribimos $\\dfrac{\\sin(n)}{n} = \\dfrac{1}{n} \\cdot \\sin(n)$. La sucesión "
                  "$a_n = \\dfrac{1}{n} \\to 0$, y $b_n = \\sin(n)$ está acotada con $|b_n| \\leq 1$."
               ),
               "justificacion_md": "$\\sin(n)$ no converge (oscila), pero está acotada — basta para el teorema.",
               "es_resultado": False},
              {"accion_md": (
                  "Por el teorema producto nula × acotada:\n\n"
                  "$\\boxed{\\lim_{n\\to\\infty} \\dfrac{\\sin(n)}{n} = 0.}$"
               ),
               "justificacion_md": "Aplicación directa.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Álgebra de límites.** Si $\\lim a_n = L$ y $\\lim b_n = M$, entonces:\n\n"
              "- (a) $\\lim (a_n + b_n) = L + M$.\n"
              "- (b) $\\lim (a_n \\cdot b_n) = L \\cdot M$.\n"
              "- (c) $\\lim \\dfrac{a_n}{b_n} = \\dfrac{L}{M}$, siempre que $M \\neq 0$.\n\n"
              "Estas propiedades reducen el cálculo de límites a operar con los valores límite."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema fundamental de potencias.** Si $p > 0$, entonces $\\lim_{n\\to\\infty} \\dfrac{1}{n^p} = 0$.\n\n"
              "**Demostración (ε-N).** Imponemos $\\dfrac{1}{n^p} < \\varepsilon \\iff n > \\dfrac{1}{\\varepsilon^{1/p}}$. "
              "Por Arquímedes existe $N$ con la cota requerida. $\\quad\\square$"
          )),

        b("definicion",
          titulo="Técnica de amplificación para cocientes de polinomios",
          body_md=(
              "Para calcular $\\lim_{n\\to\\infty} \\dfrac{P(n)}{Q(n)}$ con $P, Q$ polinomios:\n\n"
              "**Amplificar** dividiendo numerador y denominador por $\\dfrac{1}{n^p}$, donde $p = \\text{grad}(Q)$.\n\n"
              "Tras amplificar, cada término de la forma $\\dfrac{c}{n^k}$ con $k > 0$ tiende a $0$, "
              "y queda un cociente entre los **coeficientes líder** y constantes finitas.\n\n"
              "**Resultado** (lo que ocurre):\n"
              "- Si $\\text{grad}(P) < \\text{grad}(Q)$: límite $= 0$.\n"
              "- Si $\\text{grad}(P) = \\text{grad}(Q)$: límite $= a_n / b_m$ (cociente de coef. líder).\n"
              "- Si $\\text{grad}(P) > \\text{grad}(Q)$: el cociente diverge a $\\pm\\infty$."
          )),

        b("ejemplo_resuelto",
          titulo="Cociente con misma grado",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\dfrac{n}{n+1}$."
          ),
          pasos=[
              {"accion_md": (
                  "El denominador $Q(n) = n + 1$ tiene grado $p = 1$. Amplificamos por $\\dfrac{1}{n}$:\n\n"
                  "$\\dfrac{n}{n+1} = \\dfrac{n \\cdot \\frac{1}{n}}{(n+1) \\cdot \\frac{1}{n}} = \\dfrac{1}{1 + \\frac{1}{n}}.$"
               ),
               "justificacion_md": "Dividimos num y den por $n$.",
               "es_resultado": False},
              {"accion_md": (
                  "Tomando límite: $\\dfrac{1}{1 + 0} = \\boxed{1}$."
               ),
               "justificacion_md": "$1/n \\to 0$ y aplicamos álgebra de límites.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cociente con grado mayor en denominador",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\dfrac{n^3 + 2n^2 - 4}{n^4 + 2}$."
          ),
          pasos=[
              {"accion_md": (
                  "Denominador grado $4$. Amplificamos por $\\dfrac{1}{n^4}$:\n\n"
                  "$\\dfrac{\\frac{1}{n} + \\frac{2}{n^2} - \\frac{4}{n^4}}{1 + \\frac{2}{n^4}}.$"
               ),
               "justificacion_md": "Dividimos cada término por $n^4$.",
               "es_resultado": False},
              {"accion_md": (
                  "Numerador $\\to 0 + 0 - 0 = 0$. Denominador $\\to 1 + 0 = 1$. Por álgebra de límites:\n\n"
                  "$\\boxed{\\lim_{n\\to\\infty} \\dfrac{n^3 + 2n^2 - 4}{n^4 + 2} = \\dfrac{0}{1} = 0.}$"
               ),
               "justificacion_md": "Caso $\\text{grad}(P) < \\text{grad}(Q) \\Rightarrow 0$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Racionalización (indeterminación $\\infty - \\infty$)",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\left( \\sqrt{n^2 + 1} - n \\right)$."
          ),
          pasos=[
              {"accion_md": (
                  "Es la forma $\\infty - \\infty$. Multiplicamos y dividimos por el conjugado "
                  "$\\sqrt{n^2 + 1} + n$:\n\n"
                  "$\\sqrt{n^2+1} - n = \\dfrac{(n^2+1) - n^2}{\\sqrt{n^2+1} + n} = \\dfrac{1}{\\sqrt{n^2+1} + n}.$"
               ),
               "justificacion_md": "Diferencia de cuadrados $(a - b)(a + b) = a^2 - b^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "Amplificamos por $\\dfrac{1}{n}$:\n\n"
                  "$\\dfrac{1/n}{\\sqrt{1 + 1/n^2} + 1}.$\n\n"
                  "Tomando límite: numerador $\\to 0$, denominador $\\to 1 + 1 = 2$. $\\boxed{\\lim = 0.}$"
               ),
               "justificacion_md": "Indeterminación resuelta vía conjugado.",
               "es_resultado": True},
          ]),

        ej(
            "Cociente con racionalización",
            "Calcule $\\lim_{n\\to\\infty} (\\sqrt{n+1} - \\sqrt{n})$.",
            [
                "Forma $\\infty - \\infty$. Multiplicar por el conjugado.",
                "$(\\sqrt{a} - \\sqrt{b})(\\sqrt{a} + \\sqrt{b}) = a - b$.",
                "El resultado debería simplificarse a algo del tipo $\\dfrac{1}{\\sqrt{n+1} + \\sqrt{n}}$.",
            ],
            (
                "$\\sqrt{n+1} - \\sqrt{n} = \\dfrac{(n+1) - n}{\\sqrt{n+1} + \\sqrt{n}} = \\dfrac{1}{\\sqrt{n+1} + \\sqrt{n}}$.\n\n"
                "Cuando $n \\to \\infty$, el denominador crece sin cota, por tanto: $\\boxed{\\lim = 0}$."
            ),
        ),

        fig(
            "Diagrama-resumen de las reglas de álgebra de límites de sucesiones. Cuatro paneles en "
            "cuadrícula 2x2 sobre fondo blanco. Panel 1: 'Suma' con la fórmula 'lim(a_n + b_n) = "
            "L + M' destacada en teal #06b6d4. Panel 2: 'Producto' con 'lim(a_n * b_n) = L * M'. "
            "Panel 3: 'Cociente' con 'lim(a_n / b_n) = L / M' y aviso ámbar #f59e0b 'requiere M != 0'. "
            "Panel 4: indeterminaciones, listando 'inf - inf', '0 * inf', 'inf/inf', '0/0' en cuadro "
            "ámbar 'NO aplicar reglas: indeterminadas'. Tipografía clara, jerarquía visual. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica las operaciones con límites:",
          preguntas=[
              {"enunciado_md": "Si $\\lim a_n = 3$ y $\\lim b_n = 0$, ¿qué se puede decir de $\\lim (a_n / b_n)$?",
               "opciones_md": [
                   "Es $3$",
                   "Es $0$",
                   "El álgebra de límites no aplica directamente — depende del signo y comportamiento de $b_n$",
                   "Siempre $+\\infty$",
               ],
               "correcta": "C",
               "pista_md": "El cociente requiere denominador con límite distinto de $0$.",
               "explicacion_md": "El álgebra de límites exige $\\lim b_n \\neq 0$ para el cociente. Si $b_n \\to 0$ desde arriba, podría dar $+\\infty$; desde abajo, $-\\infty$; si oscila, indefinido."},
              {"enunciado_md": "Calcula $\\lim_{n \\to \\infty} \\dfrac{3n^2 + 5}{2n^2 - n}$.",
               "opciones_md": ["$0$", "$\\tfrac{3}{2}$", "$\\infty$", "$1$"],
               "correcta": "B",
               "pista_md": "Dividí numerador y denominador por $n^2$.",
               "explicacion_md": "$\\dfrac{3 + 5/n^2}{2 - 1/n} \\to \\dfrac{3 + 0}{2 - 0} = \\dfrac{3}{2}$. Cuando los grados son iguales, el límite es el cociente de coeficientes líderes."},
              {"enunciado_md": "¿Cuál de las siguientes formas es indeterminada?",
               "opciones_md": ["$5 + \\infty$", "$\\infty - \\infty$", "$0 \\cdot 5$", "$1/\\infty$"],
               "correcta": "B",
               "pista_md": "Indeterminado = puede dar cualquier valor según las sucesiones.",
               "explicacion_md": "$\\infty - \\infty$ es indeterminado: $(n + 1) - n \\to 1$, pero $(2n) - n \\to \\infty$. Hay que reescribir antes de evaluar."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Aplicar álgebra de límites cuando uno no converge:** $\\lim (a_n + b_n) = \\lim a_n + \\lim b_n$ requiere ambos finitos.",
              "**Olvidar verificar $M \\neq 0$ en el cociente:** si $\\lim b_n = 0$ no se puede aplicar (c).",
              "**No identificar el grado del denominador para amplificar:** $1/n^p$ con $p$ correcto.",
              "**Confundir $0 \\cdot \\infty$ con $0$:** es una indeterminación, requiere análisis especial.",
              "**Olvidar el conjugado** ante $\\sqrt{\\cdots} - \\cdots$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Producto nula × acotada → 0** (no requiere convergencia de la acotada).",
              "**Álgebra de límites:** suma, producto, cociente cuando ambos convergen (denominador $\\neq 0$).",
              "**$1/n^p \\to 0$** para $p > 0$.",
              "**Cocientes de polinomios:** amplificar por $1/n^p$ con $p = \\text{grad}(Q)$.",
              "**Racionalización:** multiplicar por conjugado para $\\sqrt{\\cdot} - \\cdot$.",
              "**Próxima lección:** Teorema del Sandwich.",
          ]),
    ]
    return {
        "id": "lec-ic-4-2-operaciones-limites",
        "title": "Operaciones con límites",
        "description": "Producto nula × acotada, álgebra de límites, técnica de amplificación para cocientes de polinomios y racionalización.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 4.3 Teorema del Sandwich
# =====================================================================
def lesson_4_3():
    blocks = [
        b("texto", body_md=(
            "El **Teorema del Sandwich** es una de las herramientas más elegantes del análisis: si una "
            "sucesión queda **atrapada** entre dos sucesiones que convergen al mismo valor, ella también "
            "debe converger a ese valor. Permite resolver problemas que de otro modo serían intratables.\n\n"
            "**Objetivos:**\n\n"
            "- Enunciado y demostración del Teorema del Sandwich.\n"
            "- Identificar cotas adecuadas.\n"
            "- Demostrar límites clásicos: $\\sqrt[n]{n} \\to 1$, $r^n \\to 0$ para $|r| < 1$, $\\sqrt[n]{a} \\to 1$.\n"
            "- Combinar Sandwich con álgebra de límites y Binomio de Newton."
        )),

        b("teorema",
          enunciado_md=(
              "**Teorema del Sandwich.** Sean $(a_n), (b_n), (c_n)$ sucesiones reales. Si existe $n_0$ tal que\n\n"
              "$$a_n \\leq b_n \\leq c_n \\quad \\text{para todo } n \\geq n_0,$$\n\n"
              "y además $\\lim a_n = \\lim c_n = L$, entonces\n\n"
              "$$\\lim_{n\\to\\infty} b_n = L.$$\n\n"
              "**Demostración.** Dado $\\varepsilon > 0$, existen $N_1, N_2$ tales que $L - \\varepsilon < a_n$ "
              "para $n > N_1$ y $c_n < L + \\varepsilon$ para $n > N_2$. Tomando $N = \\max(N_1, N_2, n_0)$, "
              "para $n > N$:\n\n"
              "$L - \\varepsilon < a_n \\leq b_n \\leq c_n < L + \\varepsilon \\Rightarrow |b_n - L| < \\varepsilon. \\quad\\square$"
          )),

        b("intuicion", body_md=(
            "**Idea geométrica.** $a_n$ y $c_n$ son **cotas inferior y superior** de $b_n$. Si ambas "
            "convergen al mismo valor $L$, $b_n$ queda **aplastada** entre ellas y no tiene más opción que "
            "converger también a $L$.\n\n"
            "**Estrategia práctica:** (1) encontrar cotas $a_n \\leq b_n \\leq c_n$ simples; (2) verificar "
            "que ambas convergen al mismo $L$."
        )),

        fig(
            "Plano cartesiano con eje horizontal 'n' y eje vertical 'aₙ'. Tres sucesiones "
            "graficadas como puntos discretos: una sucesión superior cₙ (puntos color ámbar "
            "#f59e0b decreciendo desde valores altos hacia L=0); una sucesión inferior aₙ "
            "(puntos color ámbar creciendo desde valores bajos hacia L=0); una sucesión central "
            "bₙ (puntos color teal #06b6d4) ondulando entre ambas. Recta horizontal punteada "
            "en y=L=0. Una llave vertical resaltando 'b queda atrapada entre a y c → fuerza b "
            "a ir a L'. Etiquetas: 'cₙ → 0' arriba, 'bₙ atrapada' al medio, 'aₙ → 0' abajo. "
            "Anotación: aₙ ≤ bₙ ≤ cₙ con flechas. Título: 'Teorema del Sandwich: si las cotas "
            "convergen, b también'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Aplicación clásica con seno",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\dfrac{\\sin(n\\pi)}{n}$."
          ),
          pasos=[
              {"accion_md": (
                  "Como $-1 \\leq \\sin(n\\pi) \\leq 1$, dividiendo por $n > 0$:\n\n"
                  "$-\\dfrac{1}{n} \\leq \\dfrac{\\sin(n\\pi)}{n} \\leq \\dfrac{1}{n}.$"
               ),
               "justificacion_md": "Cota fundamental del seno + dividir por $n > 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\lim (-1/n) = 0$ y $\\lim (1/n) = 0$. Por Sandwich:\n\n"
                  "$\\boxed{\\lim_{n\\to\\infty} \\dfrac{\\sin(n\\pi)}{n} = 0.}$"
               ),
               "justificacion_md": "Ambas cotas convergen a $0$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Suma con cotas algebraicas",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} a_n$, donde $a_n = \\dfrac{1}{\\sqrt{n^2+1}} + \\dfrac{1}{\\sqrt{n^2+2}} + \\cdots + \\dfrac{1}{\\sqrt{n^2+n}}$."
          ),
          pasos=[
              {"accion_md": (
                  "Cota superior: reemplazamos cada $\\sqrt{n^2+k}$ por el menor $\\sqrt{n^2+1}$:\n\n"
                  "$a_n \\leq \\sum_{k=1}^{n} \\dfrac{1}{\\sqrt{n^2+1}} = \\dfrac{n}{\\sqrt{n^2+1}}.$\n\n"
                  "Cota inferior: por el mayor $\\sqrt{n^2+n}$:\n\n"
                  "$a_n \\geq \\sum_{k=1}^{n} \\dfrac{1}{\\sqrt{n^2+n}} = \\dfrac{n}{\\sqrt{n^2+n}}.$"
               ),
               "justificacion_md": "Aumentar el denominador disminuye la fracción y viceversa.",
               "es_resultado": False},
              {"accion_md": (
                  "Calculamos límites de las cotas (amplificando por $1/n$):\n\n"
                  "$\\lim \\dfrac{n}{\\sqrt{n^2+n}} = \\lim \\dfrac{1}{\\sqrt{1 + 1/n}} = 1$, $\\lim \\dfrac{n}{\\sqrt{n^2+1}} = \\lim \\dfrac{1}{\\sqrt{1 + 1/n^2}} = 1$.\n\n"
                  "Por Sandwich: $\\boxed{\\lim a_n = 1.}$"
               ),
               "justificacion_md": "Ambas cotas tienden a $1$.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Límite clásico** $\\lim_{n\\to\\infty} \\sqrt[n]{n} = 1$.\n\n"
              "**Demostración (con Sandwich + Binomio de Newton).** Sea $a_n = \\sqrt[n]{n} \\geq 1$. "
              "Elevando a $n$:\n\n"
              "$n = a_n^n = (1 + (a_n - 1))^n \\geq \\binom{n}{2}(a_n - 1)^2 = \\dfrac{n(n-1)}{2}(a_n - 1)^2$.\n\n"
              "Despejando: $(a_n - 1)^2 \\leq \\dfrac{2}{n-1}$, luego $a_n \\leq 1 + \\sqrt{\\dfrac{2}{n-1}}$.\n\n"
              "Así $1 \\leq \\sqrt[n]{n} \\leq 1 + \\sqrt{\\dfrac{2}{n-1}}$. Como $\\sqrt{2/(n-1)} \\to 0$, "
              "por Sandwich $\\lim \\sqrt[n]{n} = 1$. $\\square$"
          )),

        b("teorema",
          enunciado_md=(
              "**Límite clásico** $\\lim_{n\\to\\infty} r^n = 0$ si $|r| < 1$.\n\n"
              "**Demostración (caso $0 < r < 1$).** Escribimos $r = 1/s$ con $s > 1$, y $s = 1 + h$ con "
              "$h > 0$. Por Binomio de Newton, $(1+h)^n \\geq 1 + nh$. Luego:\n\n"
              "$0 < r^n = \\dfrac{1}{(1+h)^n} \\leq \\dfrac{1}{1 + nh} < \\dfrac{1}{nh}$.\n\n"
              "Como $\\dfrac{1}{nh} \\to 0$, por Sandwich $r^n \\to 0$. (Caso $-1 < r < 0$: usar "
              "$-|r|^n \\leq r^n \\leq |r|^n$.) $\\quad\\square$"
          )),

        b("teorema",
          enunciado_md=(
              "**Límite clásico** $\\lim_{n\\to\\infty} \\sqrt[n]{a} = 1$ para todo $a > 0$.\n\n"
              "**Caso $a \\geq 1$:** análogo a $\\sqrt[n]{n}$ pero con $a$ fijo. $a = (1 + (a_n - 1))^n \\geq 1 + n(a_n - 1)$, "
              "luego $a_n \\leq 1 + \\dfrac{a-1}{n}$, y se aplica Sandwich con $1 \\leq a_n \\leq 1 + \\dfrac{a-1}{n}$.\n\n"
              "**Caso $0 < a < 1$:** $\\sqrt[n]{a} = \\dfrac{1}{\\sqrt[n]{1/a}} \\to \\dfrac{1}{1} = 1$ por "
              "el caso anterior + álgebra de límites. $\\square$"
          )),

        b("ejemplo_resuelto",
          titulo="Sucesión geométrica fraccionaria",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\dfrac{2^n - 1}{3^n + 1}$."
          ),
          pasos=[
              {"accion_md": (
                  "Dividimos numerador y denominador por $3^n$:\n\n"
                  "$\\dfrac{2^n - 1}{3^n + 1} = \\dfrac{(2/3)^n - (1/3)^n}{1 + (1/3)^n}.$"
               ),
               "justificacion_md": "Identificamos la base mayor del denominador.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $|2/3| < 1$ y $|1/3| < 1$, ambas potencias $\\to 0$. Por álgebra de límites:\n\n"
                  "$\\boxed{\\lim = \\dfrac{0 - 0}{1 + 0} = 0.}$"
               ),
               "justificacion_md": "Aplicamos $r^n \\to 0$ con $|r| < 1$.",
               "es_resultado": True},
          ]),

        ej(
            "Aplicación del Sandwich",
            "Calcule $\\lim_{n\\to\\infty} \\dfrac{\\cos(n^2)}{n+1}$.",
            [
                "Acotá $\\cos(n^2)$ entre $-1$ y $1$.",
                "Dividí por $n+1 > 0$.",
                "Aplicá Sandwich.",
            ],
            (
                "$-1 \\leq \\cos(n^2) \\leq 1 \\Rightarrow -\\dfrac{1}{n+1} \\leq \\dfrac{\\cos(n^2)}{n+1} \\leq \\dfrac{1}{n+1}$.\n\n"
                "Ambas cotas $\\to 0$, por Sandwich $\\boxed{\\lim = 0}$."
            ),
        ),

        b("verificacion",
          intro_md="Verifica el Teorema del Sandwich:",
          preguntas=[
              {"enunciado_md": "¿Cuáles son las hipótesis del Teorema del Sandwich?",
               "opciones_md": [
                   "$a_n \\leq c_n$ y $\\lim a_n = \\lim c_n$",
                   "$a_n \\leq b_n \\leq c_n$ a partir de algún $n_0$, y $\\lim a_n = \\lim c_n = L$",
                   "$a_n \\leq b_n \\leq c_n$ para todo $n$, sin requerir límites",
                   "Solo $\\lim b_n$ existe",
               ],
               "correcta": "B",
               "pista_md": "Necesitas DOS cotas (arriba y abajo) Y que tengan el MISMO límite.",
               "explicacion_md": "El Sandwich requiere acotar $b_n$ entre dos sucesiones con el mismo límite $L$. La conclusión es $\\lim b_n = L$."},
              {"enunciado_md": "¿Cuál es $\\lim_{n \\to \\infty} \\dfrac{\\sin n}{n}$?",
               "opciones_md": ["$0$", "$1$", "Oscila", "No existe"],
               "correcta": "A",
               "pista_md": "Acotá usando $-1 \\leq \\sin n \\leq 1$ y dividí por $n$.",
               "explicacion_md": "$-\\tfrac{1}{n} \\leq \\tfrac{\\sin n}{n} \\leq \\tfrac{1}{n}$. Como ambas cotas tienden a $0$, por Sandwich $\\lim \\tfrac{\\sin n}{n} = 0$."},
              {"enunciado_md": "Si $a_n \\to 2$ y $c_n \\to 3$ con $a_n \\leq b_n \\leq c_n$, ¿qué concluye el Sandwich?",
               "opciones_md": [
                   "$b_n \\to 2.5$",
                   "$b_n \\to 2$",
                   "$b_n \\to 3$",
                   "El Sandwich NO aplica (límites distintos)",
               ],
               "correcta": "D",
               "pista_md": "El Sandwich exige límites iguales en las cotas.",
               "explicacion_md": "Si $\\lim a_n \\neq \\lim c_n$, el Sandwich no concluye nada sobre $b_n$. Solo se sabe que está entre ambos en el límite."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Cotas con límites distintos:** el Sandwich requiere $\\lim a_n = \\lim c_n$. Si difieren, no concluye.",
              "**Cotas que no son cotas:** verificar siempre $a_n \\leq b_n \\leq c_n$ para $n$ grande.",
              "**Confundir Sandwich con álgebra de límites:** Sandwich aplica cuando NO sabemos el límite por otros medios.",
              "**Olvidar el Binomio de Newton** para acotar potencias $(1+h)^n$.",
              "**Asumir que $r^n \\to 0$ siempre:** solo si $|r| < 1$. Si $r = 1$, vale $1$; si $|r| > 1$, diverge.",
          ]),

        b("resumen",
          puntos_md=[
              "**Sandwich:** $a_n \\leq b_n \\leq c_n$ + $\\lim a_n = \\lim c_n = L \\Rightarrow \\lim b_n = L$.",
              "**Cotas clásicas para seno/coseno:** $|\\sin x|, |\\cos x| \\leq 1$.",
              "**$\\sqrt[n]{n} \\to 1$, $r^n \\to 0$ ($|r| < 1$), $\\sqrt[n]{a} \\to 1$ ($a > 0$).**",
              "**Binomio de Newton** para acotar $(1+h)^n$: $\\geq 1 + nh$ y $\\geq \\binom{n}{2} h^2$.",
              "**Cocientes de exponenciales:** dividir por la base mayor.",
              "**Próxima lección:** sucesiones monótonas y acotadas.",
          ]),
    ]
    return {
        "id": "lec-ic-4-3-teorema-sandwich",
        "title": "Teorema del Sandwich",
        "description": "Enunciado, demostración y aplicaciones del Teorema del Sandwich. Límites clásicos: $\\sqrt[n]{n} \\to 1$, $r^n \\to 0$, $\\sqrt[n]{a} \\to 1$.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 4.4 Sucesiones monótonas y acotadas
# =====================================================================
def lesson_4_4():
    blocks = [
        b("texto", body_md=(
            "El **Teorema de Sucesiones Monótonas y Acotadas** es uno de los resultados más poderosos "
            "del análisis: garantiza convergencia **sin necesidad de conocer el límite de antemano**. "
            "La idea es simple: si una sucesión \"siempre crece\" pero está \"contenida\" en cierto rango, "
            "entonces necesariamente debe converger.\n\n"
            "**Objetivos:**\n\n"
            "- Definiciones de sucesión monótona (creciente/decreciente) y acotada.\n"
            "- **Axioma de Completitud** de $\\mathbb{R}$.\n"
            "- Teorema de Sucesiones Monótonas y Acotadas.\n"
            "- Aplicar a sucesiones definidas por **recurrencia** (con inducción)."
        )),

        b("definicion",
          titulo="Sucesión monótona",
          body_md=(
              "$\\{a_n\\}$ es:\n\n"
              "- **Monótona creciente** si $a_{n+1} \\geq a_n$ para todo $n$.\n"
              "- **Estrictamente creciente** si $a_{n+1} > a_n$.\n"
              "- **Monótona decreciente** si $a_{n+1} \\leq a_n$.\n"
              "- **Estrictamente decreciente** si $a_{n+1} < a_n$.\n\n"
              "**Tres métodos** para verificar monotonía:\n\n"
              "1. **Diferencia $a_{n+1} - a_n$:** signo positivo $\\Rightarrow$ creciente, negativo $\\Rightarrow$ decreciente.\n"
              "2. **Cociente $\\dfrac{a_{n+1}}{a_n}$** (con $a_n > 0$): mayor que $1 \\Rightarrow$ creciente.\n"
              "3. **Inducción matemática:** especialmente útil para recurrencias."
          )),

        b("definicion",
          titulo="Sucesión acotada",
          body_md=(
              "$\\{a_n\\}$ está:\n\n"
              "- **Acotada superiormente** si existe $M \\in \\mathbb{R}$ con $a_n \\leq M$ para todo $n$.\n"
              "- **Acotada inferiormente** si existe $m \\in \\mathbb{R}$ con $a_n \\geq m$ para todo $n$.\n"
              "- **Acotada** (sin más) si lo está superior e inferiormente, equivalente a $|a_n| \\leq M$ para algún $M > 0$."
          )),

        b("definicion",
          titulo="Axioma de Completitud",
          body_md=(
              "**Axioma de Completitud de $\\mathbb{R}$.** Si $S \\subseteq \\mathbb{R}$ es no vacío y "
              "tiene una cota superior, entonces $S$ posee una **cota superior mínima**, llamada **supremo** "
              "de $S$ y denotada $\\sup S$.\n\n"
              "Este axioma expresa el hecho fundamental de que **no hay agujeros** en la recta real, a "
              "diferencia de lo que ocurre con $\\mathbb{Q}$. Es la propiedad técnica que sustenta todo el "
              "análisis."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema de Sucesiones Monótonas y Acotadas.** Toda sucesión monótona y acotada es **convergente**.\n\n"
              "Más precisamente:\n"
              "- Una sucesión **creciente y acotada superiormente** converge a $L = \\sup\\{a_n\\}$.\n"
              "- Una sucesión **decreciente y acotada inferiormente** converge a $L = \\inf\\{a_n\\}$.\n\n"
              "**Idea de la demostración.** Si $\\{a_n\\}$ es creciente y acotada, $S = \\{a_n : n \\in \\mathbb{N}\\}$ "
              "tiene supremo $L$. Se prueba que $\\lim a_n = L$ usando la definición ε-N: dado $\\varepsilon > 0$, "
              "$L - \\varepsilon$ no es cota superior, luego existe $N$ con $a_N > L - \\varepsilon$, y por "
              "monotonía $L - \\varepsilon < a_N \\leq a_n \\leq L$ para $n \\geq N$. $\\square$\n\n"
              "**Importancia:** este teorema **garantiza** la existencia del límite **sin necesidad de calcularlo**."
          )),

        fig(
            "Plano cartesiano con eje horizontal 'n' y eje vertical 'aₙ'. Sucesión creciente "
            "(escalera) representada por puntos teal #06b6d4 que suben monotonamente desde "
            "a₁=2 a través de a₂=4, a₃=5, a₄=5.5, a₅=5.75, etc., acercándose pero sin tocar "
            "una recta horizontal punteada en y=L=6 (color ámbar #f59e0b, etiqueta "
            "'L = sup = 6'). Una segunda recta punteada en y=M=7 (cota superior arbitraria, "
            "etiqueta 'M = cota superior'). Líneas verticales conectando cada punto al "
            "siguiente para mostrar el ascenso. Anotación con flechas: 'creciente + acotada "
            "→ converge al supremo'. Título: 'Teorema de Sucesiones Monótonas y Acotadas'. " + STYLE
        ),

        b("definicion",
          titulo="Estrategia para sucesiones por recurrencia",
          body_md=(
              "Cuando la sucesión está definida por $a_1$ + relación $a_{n+1} = f(a_n)$:\n\n"
              "1. **Verificar monotonía** por inducción.\n"
              "2. **Verificar acotación** por inducción (cota superior si creciente, inferior si decreciente).\n"
              "3. **Concluir convergencia** por el teorema.\n"
              "4. **Calcular el límite** $L$ aplicando límite a ambos lados de la recurrencia: $L = f(L)$, "
              "lo que da una **ecuación de punto fijo**.\n\n"
              "**Cuidado:** si $L = f(L)$ tiene varias soluciones, descartar las incompatibles con los valores "
              "de la sucesión (e.g. soluciones negativas si $a_n > 0$)."
          )),

        b("ejemplo_resuelto",
          titulo="Recurrencia $a_{n+1} = \\tfrac{1}{2}(a_n + 6)$",
          problema_md=(
              "Sea $a_1 = 2$ y $a_{n+1} = \\tfrac{1}{2}(a_n + 6)$. Investigue convergencia y calcule el límite."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1 — Monotonía (creciente).** Caso base $n=1$: $a_2 = \\tfrac{1}{2}(2 + 6) = 4 > 2 = a_1$ ✓.\n\n"
                  "Paso inductivo: si $a_{k+1} > a_k$, entonces $a_{k+1} + 6 > a_k + 6$, luego "
                  "$a_{k+2} = \\tfrac{1}{2}(a_{k+1}+6) > \\tfrac{1}{2}(a_k+6) = a_{k+1}$. Por inducción, $a_{n+1} > a_n$ para todo $n$."
               ),
               "justificacion_md": "Inducción matemática.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2 — Cota superior $a_n < 6$.** Base: $a_1 = 2 < 6$ ✓. "
                  "Inductivo: si $a_k < 6$, entonces $a_k + 6 < 12$, luego $a_{k+1} = \\tfrac{1}{2}(a_k+6) < 6$. ✓"
               ),
               "justificacion_md": "Inducción para acotación.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3 — Convergencia.** Por el teorema, $\\{a_n\\}$ converge. Sea $L = \\lim a_n$.\n\n"
                  "**Paso 4 — Ecuación de punto fijo.** Tomando límite en $a_{n+1} = \\tfrac{1}{2}(a_n + 6)$:\n\n"
                  "$L = \\tfrac{1}{2}(L + 6) \\iff 2L = L + 6 \\iff \\boxed{L = 6.}$"
               ),
               "justificacion_md": "Una vez asegurada la convergencia, podemos resolver para $L$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Recurrencia con raíz cuadrada",
          problema_md=(
              "Sea $a_1 = \\sqrt{2}$ y $a_{n+1} = \\sqrt{2 + a_n}$. Pruebe convergencia y calcule el límite."
          ),
          pasos=[
              {"accion_md": (
                  "**Monotonía (creciente):** $a_1 \\approx 1.414$, $a_2 \\approx 1.848$, $a_2 > a_1$ ✓. "
                  "Inducción: si $a_{k+1} > a_k$, entonces $2 + a_{k+1} > 2 + a_k$, y por monotonía de la raíz, "
                  "$\\sqrt{2 + a_{k+1}} > \\sqrt{2 + a_k}$, es decir $a_{k+2} > a_{k+1}$."
               ),
               "justificacion_md": "Raíz cuadrada es estrictamente creciente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cota superior $a_n < 2$:** $a_1 = \\sqrt{2} < 2$ ✓. Si $a_k < 2$: $2 + a_k < 4 \\Rightarrow \\sqrt{2 + a_k} < 2$, luego $a_{k+1} < 2$.\n\n"
                  "Por el teorema, converge. Sea $L = \\lim a_n \\geq 0$."
               ),
               "justificacion_md": "Inducción + teorema.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cálculo del límite:** $L = \\sqrt{2 + L} \\Rightarrow L^2 = 2 + L \\Rightarrow L^2 - L - 2 = 0 \\Rightarrow (L-2)(L+1) = 0$.\n\n"
                  "$L = 2$ o $L = -1$. Como $a_n > 0$, descartamos $L = -1$. $\\boxed{\\lim a_n = 2.}$"
               ),
               "justificacion_md": "Descartamos solución incompatible.",
               "es_resultado": True},
          ]),

        ej(
            "Recurrencia simple",
            "Sea $a_1 = 1$ y $a_{n+1} = \\tfrac{a_n + 3}{2}$. Pruebe que converge y halle el límite.",
            [
                "Verificá monotonía: probá $a_{n+1} > a_n$ por inducción.",
                "Verificá cota superior $a_n < 3$ por inducción.",
                "Aplicá límite a la recurrencia.",
            ],
            (
                "**Monotonía:** $a_2 = 2 > 1 = a_1$. Si $a_{k+1} > a_k$: $a_{k+2} = \\tfrac{a_{k+1}+3}{2} > \\tfrac{a_k+3}{2} = a_{k+1}$.\n\n"
                "**Cota:** $a_1 = 1 < 3$. Si $a_k < 3$: $a_{k+1} = \\tfrac{a_k+3}{2} < \\tfrac{6}{2} = 3$.\n\n"
                "**Límite:** $L = \\tfrac{L+3}{2} \\iff 2L = L + 3 \\iff \\boxed{L = 3}$."
            ),
        ),

        b("verificacion",
          intro_md="Verifica el teorema de sucesiones monótonas y acotadas:",
          preguntas=[
              {"enunciado_md": "¿Cuáles son las hipótesis del teorema 'toda sucesión monótona y acotada converge'?",
               "opciones_md": [
                   "Solo monotonía",
                   "Solo acotación",
                   "Monotonía Y acotación (en el sentido apropiado)",
                   "Que sea positiva",
               ],
               "correcta": "C",
               "pista_md": "Una sin la otra no garantiza convergencia.",
               "explicacion_md": "Hay que tener AMBAS: monótona (creciente o decreciente) y acotada (sup. o inf., respectivamente). Cada una sola NO basta."},
              {"enunciado_md": "$a_n = n$ es monótona pero NO acotada. ¿Converge?",
               "opciones_md": [
                   "Sí, converge a $\\infty$",
                   "No, diverge a $+\\infty$",
                   "Sí, converge a $1$",
                   "No, oscila",
               ],
               "correcta": "B",
               "pista_md": "Convergencia exige límite finito.",
               "explicacion_md": "Crece sin cota, así que diverge a $+\\infty$. La monotonía sin acotación no implica convergencia (la convergencia exige límite real finito)."},
              {"enunciado_md": "Si $a_n$ es decreciente y acotada inferiormente por $0$, ¿qué se concluye?",
               "opciones_md": [
                   "$a_n \\to 0$",
                   "$a_n$ converge a algún $L \\geq 0$",
                   "$a_n$ diverge",
                   "$a_n$ es constante",
               ],
               "correcta": "B",
               "pista_md": "El teorema asegura existencia del límite, pero no su valor.",
               "explicacion_md": "El teorema garantiza convergencia a un $L \\geq 0$ (el ínfimo del recorrido), pero $L$ no necesariamente es $0$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Aplicar el teorema sin verificar ambas hipótesis:** monotonía Y acotación.",
              "**Confundir cota superior con cota inferior:** crecientes acotadas superiormente, decrecientes acotadas inferiormente.",
              "**Asumir el límite antes de demostrar convergencia:** primero garantizar que $L$ existe, luego calcularlo.",
              "**No descartar soluciones incompatibles** de la ecuación $L = f(L)$.",
              "**Pensar que toda sucesión acotada converge:** $a_n = (-1)^n$ es contraejemplo (no monótona).",
          ]),

        b("resumen",
          puntos_md=[
              "**Monótona creciente y acotada superiormente $\\Rightarrow$ converge a su supremo.**",
              "**Monótona decreciente y acotada inferiormente $\\Rightarrow$ converge a su ínfimo.**",
              "**Axioma de Completitud:** todo conjunto no vacío acotado superiormente tiene supremo.",
              "**Para recurrencias:** monotonía e acotación por inducción → teorema → ecuación $L = f(L)$.",
              "**Descartar soluciones espurias** según las propiedades de la sucesión.",
              "**Próxima lección:** límites relevantes ($e$, jerarquía de crecimiento).",
          ]),
    ]
    return {
        "id": "lec-ic-4-4-monotonas-acotadas",
        "title": "Sucesiones monótonas y acotadas",
        "description": "Definiciones, axioma de completitud, teorema de sucesiones monótonas y acotadas, y aplicación a recurrencias mediante inducción.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# =====================================================================
# 4.5 Límites relevantes
# =====================================================================
def lesson_4_5():
    blocks = [
        b("texto", body_md=(
            "En esta lección estudiamos algunos límites **especialmente importantes** que aparecerán a lo "
            "largo del cálculo. El más destacado es la convergencia de $\\left(1 + \\dfrac{1}{n}\\right)^n$, "
            "que define el número $e$, base del logaritmo natural. También veremos la **proposición del cociente** "
            "y la **jerarquía de crecimiento**: polinomios $\\ll$ exponenciales $\\ll$ factoriales.\n\n"
            "**Objetivos:**\n\n"
            "- Probar que $a_n = (1 + 1/n)^n$ es creciente y acotada.\n"
            "- Definir el número real $e$ y acotarlo entre $2$ y $3$.\n"
            "- **Proposición del cociente** para límites con potencias y factoriales.\n"
            "- Establecer la **jerarquía de crecimiento**."
        )),

        b("teorema",
          enunciado_md=(
              "**Convergencia de $(1 + 1/n)^n$.** La sucesión $a_n = \\left(1 + \\dfrac{1}{n}\\right)^n$ "
              "es **estrictamente creciente y acotada superiormente por $3$**, por tanto converge.\n\n"
              "**Idea de la prueba.** Por el binomio de Newton:\n\n"
              "$a_n = \\sum_{k=0}^{n} \\binom{n}{k} \\dfrac{1}{n^k} = 1 + 1 + \\dfrac{1}{2!}\\left(1 - \\dfrac{1}{n}\\right) + \\cdots$\n\n"
              "Cada sumando crece con $n$ y se agrega un término positivo al pasar de $n$ a $n+1$, "
              "luego $\\{a_n\\}$ es creciente.\n\n"
              "**Cota superior:** usando $k! \\geq 2^{k-1}$ (por inducción), se acota la suma por una progresión "
              "geométrica de razón $1/2$, obteniendo $a_n < 3$. Por el teorema de monótonas y acotadas, converge."
          )),

        b("definicion",
          titulo="El número $e$",
          body_md=(
              "Se define el número real $e$ como\n\n"
              "$$\\boxed{e = \\lim_{n\\to\\infty} \\left(1 + \\dfrac{1}{n}\\right)^n.}$$\n\n"
              "Por la prueba anterior, $2 \\leq e \\leq 3$. En realidad $e \\approx 2{,}71828\\ldots$ "
              "(irracional y trascendente). Es la **base del logaritmo natural** y aparece de manera "
              "fundamental en exponenciales, crecimiento, decaimiento y prácticamente todos los fenómenos "
              "modelados con cálculo."
          )),

        b("ejemplo_resuelto",
          titulo="Variación: $\\lim (1 - 1/n)^n$",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\left(1 - \\dfrac{1}{n}\\right)^n$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\left(1 - \\dfrac{1}{n}\\right)^n = \\left(\\dfrac{n-1}{n}\\right)^n = \\dfrac{1}{(n/(n-1))^n}.$"
               ),
               "justificacion_md": "Reescribimos como recíproco.",
               "es_resultado": False},
              {"accion_md": (
                  "Notamos que $\\dfrac{n}{n-1} = 1 + \\dfrac{1}{n-1}$, luego:\n\n"
                  "$\\left(\\dfrac{n}{n-1}\\right)^n = \\left(1 + \\dfrac{1}{n-1}\\right)^n = \\left(1 + \\dfrac{1}{n-1}\\right)^{n-1} \\cdot \\left(1 + \\dfrac{1}{n-1}\\right).$\n\n"
                  "El primer factor $\\to e$ (cuando $n-1 \\to \\infty$), el segundo $\\to 1$."
               ),
               "justificacion_md": "Manipulación algebraica para reconocer la forma de $e$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\boxed{\\lim_{n\\to\\infty} \\left(1 - \\dfrac{1}{n}\\right)^n = \\dfrac{1}{e} = e^{-1}.}$"
               ),
               "justificacion_md": "Tomando recíproco.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Proposición del cociente.** Sea $\\{a_n\\}$ con $a_n > 0$. Si\n\n"
              "$$\\lim_{n\\to\\infty} \\dfrac{a_{n+1}}{a_n} = L < 1,$$\n\n"
              "entonces $\\lim a_n = 0$.\n\n"
              "**Idea:** existe $r$ con $L < r < 1$ y a partir de cierto $N$, $\\dfrac{a_{n+1}}{a_n} < r$. "
              "Por iteración, $a_n$ está dominada por una progresión geométrica de razón $r < 1$, que tiende a $0$."
          )),

        b("ejemplo_resuelto",
          titulo="Exponencial domina polinomio",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\dfrac{n^p}{a^n}$ para $a > 1$ y $p \\in \\mathbb{N}$ fijo."
          ),
          pasos=[
              {"accion_md": (
                  "Sea $b_n = \\dfrac{n^p}{a^n} > 0$. Calculamos el cociente:\n\n"
                  "$\\dfrac{b_{n+1}}{b_n} = \\dfrac{(n+1)^p}{a^{n+1}} \\cdot \\dfrac{a^n}{n^p} = \\dfrac{1}{a} \\left(1 + \\dfrac{1}{n}\\right)^p.$"
               ),
               "justificacion_md": "Simplificación.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\lim \\dfrac{b_{n+1}}{b_n} = \\dfrac{1}{a} \\cdot 1 = \\dfrac{1}{a} < 1$ (porque $a > 1$). Por la proposición del cociente:\n\n"
                  "$\\boxed{\\lim_{n\\to\\infty} \\dfrac{n^p}{a^n} = 0.}$\n\n"
                  "**Toda potencia exponencial $a^n$ con $a > 1$ crece más rápido que cualquier potencia polinomial $n^p$.**"
               ),
               "justificacion_md": "Aplicamos la proposición.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Factorial domina exponencial",
          problema_md=(
              "Calcule $\\lim_{n\\to\\infty} \\dfrac{a^n}{n!}$ para $a \\in \\mathbb{R}$ fijo."
          ),
          pasos=[
              {"accion_md": (
                  "Sea $c_n = \\dfrac{|a|^n}{n!} > 0$. Calculamos:\n\n"
                  "$\\dfrac{c_{n+1}}{c_n} = \\dfrac{|a|^{n+1}}{(n+1)!} \\cdot \\dfrac{n!}{|a|^n} = \\dfrac{|a|}{n+1}.$"
               ),
               "justificacion_md": "Simplificación clave: el cociente es $|a|/(n+1)$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\lim \\dfrac{c_{n+1}}{c_n} = \\lim \\dfrac{|a|}{n+1} = 0 < 1$. Por la proposición del cociente, $c_n \\to 0$, luego:\n\n"
                  "$\\boxed{\\lim_{n\\to\\infty} \\dfrac{a^n}{n!} = 0.}$\n\n"
                  "**El factorial $n!$ crece más rápido que cualquier exponencial $a^n$.**"
               ),
               "justificacion_md": "Independiente del valor de $a$.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Jerarquía de crecimiento** (de menor a mayor velocidad):\n\n"
            "$$\\ln(n) \\;\\ll\\; n^p \\;\\ll\\; a^n \\;\\ll\\; n! \\;\\ll\\; n^n \\quad (a > 1, p > 0).$$\n\n"
            "**Significado:** si en un cociente aparece más de una de estas funciones, la que **crece más "
            "rápido gana**:\n\n"
            "- En el **denominador** → el límite es $0$.\n"
            "- En el **numerador** → el límite es $\\infty$.\n\n"
            "Esta jerarquía es uno de los hechos más útiles del análisis."
        )),

        ej(
            "Aplicar la jerarquía",
            "Calcule $\\lim_{n\\to\\infty} \\dfrac{n^{100}}{2^n}$.",
            [
                "Polinomio $n^{100}$ vs. exponencial $2^n$ con base $2 > 1$.",
                "Por la jerarquía, el exponencial gana.",
            ],
            (
                "Por la jerarquía polinomio $\\ll$ exponencial: $\\boxed{\\lim_{n\\to\\infty} \\dfrac{n^{100}}{2^n} = 0}$.\n\n"
                "Aunque el polinomio tiene grado $100$, el exponencial $2^n$ crece más rápido eventualmente."
            ),
        ),

        fig(
            "Diagrama tipo 'jerarquía de crecimientos' mostrando, en una escala vertical de izquierda a "
            "derecha, las velocidades asintóticas: log(n) (más lento, base) en gris, n^k (polinómico) "
            "en teal #06b6d4, a^n con a > 1 (exponencial) en ámbar #f59e0b, n! (factorial) en ámbar más "
            "saturado, n^n (más rápido) en rojo. Cada caja conecta a la siguiente con flecha rotulada "
            "'<<' indicando que cada función crece estrictamente más rápido. Pequeño grafico al lado "
            "comparando n^100 vs 2^n: para n grande la exponencial domina. Fondo blanco. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica los límites relevantes:",
          preguntas=[
              {"enunciado_md": "¿Cuál es $\\lim_{n \\to \\infty} \\dfrac{n^{100}}{2^n}$?",
               "opciones_md": ["$+\\infty$", "$0$", "$1$", "$100$"],
               "correcta": "B",
               "pista_md": "Las exponenciales con base $>1$ vencen a TODA potencia de $n$.",
               "explicacion_md": "Asintóticamente $2^n$ supera a cualquier $n^k$. Para $n$ pequeño $n^{100}$ es enorme, pero el exponencial finalmente domina y el cociente tiende a $0$."},
              {"enunciado_md": "¿Cuál es $\\lim_{n \\to \\infty} \\sqrt[n]{n}$?",
               "opciones_md": ["$0$", "$1$", "$\\infty$", "$e$"],
               "correcta": "B",
               "pista_md": "Es un límite clásico: la raíz $n$-ésima de $n$.",
               "explicacion_md": "$\\sqrt[n]{n} \\to 1$. Aunque $n \\to \\infty$, la raíz $n$-ésima 'aplana' el crecimiento y el límite es $1$."},
              {"enunciado_md": "Si $|a| < 1$, ¿cuál es $\\lim_{n \\to \\infty} a^n$?",
               "opciones_md": ["$1$", "$0$", "$\\infty$", "Oscila"],
               "correcta": "B",
               "pista_md": "Multiplicar repetidamente por algo con valor absoluto menor a $1$ tiende a $0$.",
               "explicacion_md": "$|a^n| = |a|^n \\to 0$ si $|a| < 1$. Por ejemplo $(1/2)^n \\to 0$, también $(-0.5)^n \\to 0$ alternando signo."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Pensar que $n^{100}$ siempre supera a $2^n$:** para $n$ pequeño sí, pero asintóticamente $2^n$ gana.",
              "**Aplicar proposición del cociente con $L > 1$:** falla. La proposición exige $L < 1$.",
              "**Olvidar tomar valor absoluto** en $a^n$ para aplicar la proposición cuando $a < 0$.",
              "**Confundir $n!$ con $n^n$:** $n^n$ crece aún más rápido. Por ejemplo, $4! = 24$ pero $4^4 = 256$.",
              "**Aplicar la jerarquía sin verificar las condiciones** ($a > 1$, $p > 0$).",
          ]),

        b("resumen",
          puntos_md=[
              "**$e = \\lim (1 + 1/n)^n$, con $2 \\leq e \\leq 3$, $e \\approx 2{,}718$.**",
              "**$\\lim (1 - 1/n)^n = 1/e$.**",
              "**Proposición del cociente:** $a_n > 0$, $\\lim a_{n+1}/a_n = L < 1 \\Rightarrow a_n \\to 0$.",
              "**Exponencial domina polinomio:** $n^p / a^n \\to 0$ ($a > 1$).",
              "**Factorial domina exponencial:** $a^n / n! \\to 0$.",
              "**Jerarquía:** $\\ln(n) \\ll n^p \\ll a^n \\ll n! \\ll n^n$.",
              "**Próxima lección:** límites infinitos.",
          ]),
    ]
    return {
        "id": "lec-ic-4-5-limites-relevantes",
        "title": "Límites relevantes",
        "description": "Definición del número $e$, proposición del cociente, jerarquía de crecimiento polinomio $\\ll$ exponencial $\\ll$ factorial.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 5,
    }


# =====================================================================
# 4.6 Límites infinitos
# =====================================================================
def lesson_4_6():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora hemos estudiado sucesiones convergentes, cuyo límite es un real finito. "
            "Sin embargo, muchas sucesiones importantes **crecen o decrecen sin cota**: los naturales, "
            "las exponenciales, los logaritmos. Para hablar con precisión de este comportamiento "
            "ilimitado, extendemos la noción de límite al caso infinito.\n\n"
            "**Objetivos:**\n\n"
            "- Definición ε-N para $\\lim a_n = \\pm \\infty$.\n"
            "- Distinguir **no acotación** de **límite infinito**.\n"
            "- **Teorema de operaciones** con límites infinitos.\n"
            "- Reconocer **formas indeterminadas**."
        )),

        b("definicion",
          titulo="Límite infinito",
          body_md=(
              "Sea $\\{a_n\\}$ una sucesión.\n\n"
              "**$\\lim_{n\\to\\infty} a_n = +\\infty$** significa que para todo $A > 0$ existe $N \\in \\mathbb{N}$ tal que\n\n"
              "$$n > N \\Rightarrow a_n > A.$$\n\n"
              "Análogamente, **$\\lim a_n = -\\infty$** si para todo $A > 0$ existe $N$ con $n > N \\Rightarrow a_n < -A$.\n\n"
              "**¡Cuidado!** $+\\infty$ y $-\\infty$ **no son números reales**. Si $\\lim a_n = \\pm\\infty$, "
              "la sucesión **NO es convergente**; se dice que **diverge a infinito**.\n\n"
              "**Observación:** $\\lim a_n = +\\infty \\iff \\lim (-a_n) = -\\infty$, así que basta estudiar "
              "el caso $+\\infty$."
          )),

        b("teorema",
          enunciado_md=(
              "**Divergencia implica no acotación.** Si $\\lim a_n = +\\infty$, entonces $\\{a_n\\}$ no está "
              "acotada superiormente.\n\n"
              "**Demostración (inmediata):** si $\\{a_n\\}$ tuviera cota superior $M$, tomando $A = M+1$ no "
              "existiría $N$ con $a_n > A$ para $n > N$, contradiciendo la definición."
          )),

        b("intuicion", body_md=(
            "**Recíproco falso.** **No acotada NO implica límite infinito.** Por ejemplo, "
            "$a_n = n + (-1)^n n$ produce $0, 2n, 0, 2n, \\ldots$ — los términos pares crecen sin cota pero "
            "los impares valen $0$. La sucesión no está acotada y, sin embargo, no diverge a $+\\infty$ "
            "(porque hay infinitos términos iguales a $0$, que no superan ningún $A > 0$ grande)."
        )),

        b("teorema",
          enunciado_md=(
              "**Sucesión creciente no acotada.** Si $\\{a_n\\}$ es **creciente** y no está acotada superiormente, "
              "entonces $\\lim a_n = +\\infty$.\n\n"
              "Esto **complementa** el teorema de convergencia monótona: una sucesión creciente o **converge** "
              "(si está acotada) o **diverge a $+\\infty$** (si no lo está)."
          )),

        b("ejemplo_resuelto",
          titulo="Sucesión de los naturales",
          problema_md=(
              "Pruebe que $\\lim_{n\\to\\infty} n = +\\infty$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\{n\\}_{n \\geq 1}$ es estrictamente creciente y no acotada superiormente (Arquímedes)."
               ),
               "justificacion_md": "Por el teorema anterior, basta verificar estas dos.",
               "es_resultado": False},
              {"accion_md": (
                  "Por el teorema, $\\boxed{\\lim_{n\\to\\infty} n = +\\infty.}$\n\n"
                  "Alternativamente: dado $A > 0$, basta tomar $N = \\lfloor A \\rfloor + 1$ y entonces "
                  "$n > N \\Rightarrow n > A$."
               ),
               "justificacion_md": "Aplicación directa.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Funciones notables que divergen",
          problema_md=(
              "Pruebe que $\\lim_{n\\to\\infty} e^n = +\\infty$, $\\lim_{n\\to\\infty} \\ln(n) = +\\infty$, y que para $x > 1$, $\\lim_{n\\to\\infty} x^n = +\\infty$."
          ),
          pasos=[
              {"accion_md": (
                  "**$e^n \\to +\\infty$:** desigualdad fundamental $e^n \\geq 1 + n \\geq n$. Dado $A > 0$, "
                  "tomamos $N = \\lfloor A \\rfloor + 1$, y para $n > N$: $e^n \\geq n > N > A$."
               ),
               "justificacion_md": "Comparación con la sucesión de los naturales.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\ln(n) \\to +\\infty$:** dado $A > 0$, $\\ln(n) > A \\iff n > e^A$. Tomamos $N = \\lfloor e^A \\rfloor + 1$. "
                  "Para $n > N$: $\\ln(n) > \\ln(e^A) = A$.\n\n"
                  "**$x^n \\to +\\infty$ para $x > 1$:** $0 < 1/x < 1$, luego $b_n = (1/x)^n \\to 0$, y por "
                  "el inciso 3 del teorema de operaciones (que veremos abajo), $1/b_n = x^n \\to +\\infty$."
               ),
               "justificacion_md": "Aplicaciones de la definición.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Operaciones con límites infinitos.**\n\n"
              "1. Si $\\lim a_n = +\\infty$ y $\\{b_n\\}$ está **acotada inferiormente**, entonces $\\lim (a_n + b_n) = +\\infty$.\n\n"
              "2. Si $\\lim a_n = +\\infty$ y existe $c > 0$ con $b_n > c$ para todo $n$, entonces $\\lim (a_n \\cdot b_n) = +\\infty$.\n\n"
              "3. Si $a_n > c > 0$, $b_n > 0$ y $\\lim b_n = 0$, entonces $\\lim \\dfrac{a_n}{b_n} = +\\infty$.\n\n"
              "4. Si $\\{a_n\\}$ está **acotada** y $\\lim b_n = +\\infty$, entonces $\\lim \\dfrac{a_n}{b_n} = 0$."
          )),

        b("ejemplo_resuelto",
          titulo="El recíproco de una sucesión nula no necesariamente diverge",
          problema_md=(
              "Si $\\lim a_n = 0$, ¿implica que $\\lim 1/a_n = +\\infty$?"
          ),
          pasos=[
              {"accion_md": (
                  "**No.** Considere $a_n = \\dfrac{(-1)^n}{n}$. Entonces $a_n \\to 0$, pero "
                  "$\\dfrac{1}{a_n} = (-1)^n \\cdot n$, que toma valores $+n$ (par) y $-n$ (impar)."
               ),
               "justificacion_md": "Contraejemplo.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\{1/a_n\\}$ no diverge a $+\\infty$ ni a $-\\infty$; **oscila sin límite**.\n\n"
                  "Para que el inciso 3 del teorema aplique, **se necesita que $a_n > 0$** (o al menos, "
                  "eventualmente del mismo signo)."
               ),
               "justificacion_md": "El teorema requiere signo controlado de $a_n$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Formas indeterminadas",
          body_md=(
              "Las siguientes expresiones son **formas indeterminadas**: requieren análisis caso a caso, "
              "no se pueden resolver directamente con los teoremas:\n\n"
              "- $+\\infty - \\infty$ (resta de divergentes)\n"
              "- $0 \\cdot \\infty$ (producto nula × divergente)\n"
              "- $\\dfrac{\\infty}{\\infty}$ (cociente de divergentes)\n"
              "- $\\dfrac{0}{0}$ (cociente de nulas)\n"
              "- $1^\\infty$, $0^0$, $\\infty^0$ (exponenciales límite)\n\n"
              "**Estrategias:** racionalización, amplificación, factorización del término dominante, "
              "comparación con jerarquía de crecimiento."
          )),

        b("ejemplo_resuelto",
          titulo="Tabla de límites infinitos elementales",
          problema_md=(
              "Resuma los límites infinitos elementales más importantes."
          ),
          pasos=[
              {"accion_md": (
                  "**Tabla:**\n\n"
                  "| Sucesión $a_n$ | Límite |\n"
                  "|:---:|:---:|\n"
                  "| $n$ | $+\\infty$ |\n"
                  "| $e^n$ | $+\\infty$ |\n"
                  "| $\\ln(n)$ | $+\\infty$ |\n"
                  "| $x^n$ con $x > 1$ | $+\\infty$ |\n"
                  "| $\\arctan(n)$ | $\\pi/2$ (finito) |\n"
                  "| $r^n$ con $|r| < 1$ | $0$ |"
               ),
               "justificacion_md": "Ejemplos canónicos para reconocer en problemas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Notable:** $\\arctan(n)$ tiene argumento que crece sin cota pero la salida está acotada por $\\pi/2$. "
                  "Una función puede recibir entradas arbitrariamente grandes y aún así converger a un valor finito."
               ),
               "justificacion_md": "Una función acotada compone con divergente y resulta acotada.",
               "es_resultado": True},
          ]),

        ej(
            "Identificar comportamiento",
            "Determine si las siguientes sucesiones convergen, divergen a $+\\infty$, o ninguna: (a) $a_n = n^2 - 100n$; (b) $b_n = \\dfrac{n^2 + 1}{n^3}$; (c) $c_n = (-1)^n n$.",
            [
                "(a) Factoriza para identificar el término dominante.",
                "(b) Divide num y den por $n^3$.",
                "(c) Mira términos pares e impares.",
            ],
            (
                "(a) $n^2 - 100n = n(n - 100) \\to +\\infty$ (ambos factores tienden a $+\\infty$).\n\n"
                "(b) $\\dfrac{n^2 + 1}{n^3} = \\dfrac{1/n + 1/n^3}{1} \\to 0$. Convergente.\n\n"
                "(c) $(-1)^n n$: pares $\\to +\\infty$, impares $\\to -\\infty$. **No tiene límite** (ni finito ni infinito)."
            ),
        ),

        fig(
            "Diagrama mostrando los tipos de divergencia y formas indeterminadas. Eje horizontal con n "
            "creciente. Tres curvas: (1) a_n = n en teal #06b6d4 ascendente, etiquetada 'a_n -> +infinito'; "
            "(2) a_n = -n en gris descendente, etiquetada 'a_n -> -infinito'; (3) a_n = (-1)^n * n "
            "oscilante con amplitud creciente en ámbar #f59e0b, etiquetada 'NO acotada y NO divergente "
            "a +inf ni -inf'. A la derecha caja con formas indeterminadas listadas: 'inf - inf', "
            "'0 * inf', 'inf/inf', '1^inf'. Texto: 'reescribir antes de evaluar'. Fondo blanco. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica el manejo de límites infinitos:",
          preguntas=[
              {"enunciado_md": "Si $a_n \\to +\\infty$ y $b_n \\to -\\infty$, ¿cuánto vale $\\lim (a_n + b_n)$?",
               "opciones_md": [
                   "$0$ (se compensan)",
                   "Es indeterminado: depende de las velocidades",
                   "$+\\infty$",
                   "$-\\infty$",
               ],
               "correcta": "B",
               "pista_md": "$\\infty - \\infty$ es una forma indeterminada.",
               "explicacion_md": "$\\infty - \\infty$ no es $0$. Por ejemplo $(n + 1) - n = 1$, pero $(2n) - n = n \\to \\infty$. Se requiere reescribir antes."},
              {"enunciado_md": "¿Toda sucesión NO acotada superiormente diverge a $+\\infty$?",
               "opciones_md": [
                   "Sí, no acotada implica divergente a $+\\infty$",
                   "No, podría oscilar como $(-1)^n n$",
                   "Sí, siempre",
                   "Solo si es positiva",
               ],
               "correcta": "B",
               "pista_md": "$(-1)^n n$ es no acotada pero NO diverge a $+\\infty$.",
               "explicacion_md": "No acotada superiormente NO implica $a_n \\to +\\infty$: $(-1)^n n$ alterna entre $+\\infty$ y $-\\infty$, no tiene límite."},
              {"enunciado_md": "Si $a_n \\to 0$ con $a_n > 0$ para todo $n$, ¿qué se concluye sobre $1/a_n$?",
               "opciones_md": [
                   "$1/a_n \\to 0$",
                   "$1/a_n \\to +\\infty$",
                   "$1/a_n \\to 1$",
                   "Indeterminado",
               ],
               "correcta": "B",
               "pista_md": "Reciproco de algo positivo y muy chico es muy grande.",
               "explicacion_md": "Si $a_n \\to 0^+$ (siempre positivo), $1/a_n \\to +\\infty$. CUIDADO: si el signo de $a_n$ alternara, el recíproco no divergiría a un solo lado."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Tratar $\\infty$ como un número:** $\\infty - \\infty$ no es $0$, es **indeterminado**.",
              "**Aplicar inciso 3 sin verificar el signo de $a_n$:** $1/a_n$ con $a_n \\to 0$ pero signo cambiante NO diverge.",
              "**Confundir no acotada con divergente a $+\\infty$:** la primera es necesaria pero no suficiente.",
              "**Olvidar que $\\arctan, \\sin, \\cos$ están acotadas:** acotadas / divergente $\\to 0$.",
              "**Resolver indeterminadas con teoremas directos:** requieren manipulación algebraica previa.",
          ]),

        b("resumen",
          puntos_md=[
              "**$\\lim a_n = +\\infty$:** $\\forall A > 0 \\, \\exists N \\, (n > N \\Rightarrow a_n > A)$.",
              "**Divergente $\\Rightarrow$ no acotada.** Recíproco falso.",
              "**Creciente no acotada $\\Rightarrow$ diverge a $+\\infty$.**",
              "**Operaciones:** suma, producto, cociente con condiciones de signo y acotación.",
              "**Acotada / divergente $\\to 0$.**",
              "**Indeterminadas:** $\\infty - \\infty$, $0 \\cdot \\infty$, $\\infty / \\infty$, $0/0$, $1^\\infty$.",
              "**Cierre del capítulo:** sucesiones es base para series, continuidad y derivadas.",
          ]),
    ]
    return {
        "id": "lec-ic-4-6-limites-infinitos",
        "title": "Límites infinitos",
        "description": "Definición de $\\lim a_n = \\pm\\infty$, distinción con no acotación, teorema de operaciones y formas indeterminadas.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "intro-calculo"

    course_doc = {
        "id": course_id,
        "title": "Introducción al Cálculo",
        "description": (
            "Polinomios, desigualdades, funciones reales, sucesiones y funciones exponencial y "
            "logarítmica. Curso puente al cálculo diferencial e integral."
        ),
        "category": "Matemáticas",
        "level": "Intermedio",
        "modules_count": 5,
        "rating": 4.8,
        "summary": "Curso introductorio de cálculo para alumnos universitarios chilenos.",
        "created_at": now(),
        "visible_to_students": True,
    }
    existing = await db.courses.find_one({"id": course_id})
    if existing:
        update_fields = {k: v for k, v in course_doc.items() if k != "created_at"}
        await db.courses.update_one({"id": course_id}, {"$set": update_fields})
        print(f"✓ Curso actualizado: {course_doc['title']}")
    else:
        await db.courses.insert_one(course_doc)
        print(f"✓ Curso creado: {course_doc['title']}")

    chapter_id = "ch-ic-sucesiones"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Sucesiones",
        "description": (
            "Definición ε-N de límite, álgebra de límites, Teorema del Sandwich, sucesiones monótonas y "
            "acotadas, número $e$, jerarquía de crecimiento y límites infinitos."
        ),
        "order": 4,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_4_1, lesson_4_2, lesson_4_3, lesson_4_4, lesson_4_5, lesson_4_6]
    total_blocks = 0
    total_figs = 0
    for build in builders:
        data = build()
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
        total_blocks += len(data["blocks"])
        total_figs += sum(1 for blk in data["blocks"] if blk.get("type") == "figura")
        print(f"  ✓ {data['title']} ({len(data['blocks'])} bloques, ~{data['duration_minutes']} min)")

    print()
    print(f"✅ Capítulo 4 — Sucesiones listo: {len(builders)} lecciones, {total_blocks} bloques, "
          f"{total_figs} figuras pendientes.")
    print()
    print("URLs locales:")
    print(f"  http://localhost:3007/courses/{course_id}")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
