"""
Seed del curso Introducción al Cálculo — Capítulo 3: Funciones Reales.
7 lecciones:
  3.1 Funciones reales (definición, dominio, recorrido)
  3.2 Gráficas de funciones (criterio recta vertical, elementales, por partes)
  3.3 Transformaciones de funciones (escalamientos, traslaciones, reflexiones)
  3.4 Funciones racionales (asíntotas, método 6 pasos, hoyos)
  3.5 Funciones biyectivas (inyectiva, sobreyectiva, test recta horizontal)
  3.6 Álgebra de funciones (suma, producto, cociente, composición)
  3.7 Función inversa (existencia, algoritmo, gráfica reflejada)

ENFOQUE: introducción formal a las funciones como objetos matemáticos. Énfasis
en dominio/recorrido, criterios geométricos (recta vertical, recta horizontal),
método sistemático para racionales, y composición/inversa como operaciones
fundamentales que se usan masivamente en cálculo posterior.

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
# 3.1 Funciones reales
# =====================================================================
def lesson_3_1():
    blocks = [
        b("texto", body_md=(
            "El concepto de **función real** es uno de los pilares fundamentales del cálculo y del "
            "análisis matemático. Formaliza la noción intuitiva de **dependencia entre variables**: "
            "dado un valor de entrada, la función entrega un único valor de salida bien determinado.\n\n"
            "**Objetivos:**\n\n"
            "- Comprender la definición formal de función real y sus tres componentes: **dominio**, "
            "**codominio** y **regla de asignación**.\n"
            "- Distinguir cuándo dos funciones son iguales.\n"
            "- Determinar el **dominio natural** a partir de la expresión analítica.\n"
            "- Calcular el **recorrido** despejando la variable independiente."
        )),

        b("definicion",
          titulo="Función real",
          body_md=(
              "Sean $A$ y $B$ subconjuntos de $\\mathbb{R}$. Una **función** $f: A \\to B$ consta de "
              "**tres partes**:\n\n"
              "1. Un conjunto $A$, el **dominio** (conjunto donde la función está definida).\n"
              "2. Un conjunto $B$, el **codominio** (conjunto donde la función toma valores).\n"
              "3. Una **regla** que asocia, de modo bien determinado, a cada $x \\in A$ un **único** "
              "elemento $f(x) \\in B$.\n\n"
              "En símbolos:\n\n"
              "$$f: A \\to B \\text{ es función} \\iff (\\forall x \\in A)(\\exists! y \\in B)(y = f(x)).$$\n\n"
              "El cuantificador $\\exists!$ significa **\"existe un único\"** — captura con precisión "
              "que a cada entrada le corresponde **exactamente** un valor de salida.\n\n"
              "**Terminología:** $y = f(x)$ es la **imagen** de $x$ por $f$ (o variable dependiente). "
              "$x$ es la **variable independiente**."
          )),

        b("definicion",
          titulo="Igualdad de funciones",
          body_md=(
              "Dos funciones $f: A \\to B$ y $g: A' \\to B'$ son **iguales** si y solo si\n\n"
              "$$A = A', \\quad B = B' \\quad \\text{y} \\quad f(x) = g(x) \\text{ para todo } x \\in A.$$\n\n"
              "Es decir, dos funciones son iguales cuando tienen el **mismo dominio**, el **mismo "
              "codominio** y la **misma regla de asignación**. La sola coincidencia de la fórmula "
              "algebraica **no es suficiente**."
          )),

        b("ejemplo_resuelto",
          titulo="Funciones aparentemente iguales pero distintas",
          problema_md=(
              "Considere $f(x) = \\dfrac{(x-1)(x+2)}{x-1}$ y $g(x) = x + 2$. ¿Son iguales como funciones?"
          ),
          pasos=[
              {"accion_md": (
                  "Para $g$, la expresión $x + 2$ está definida para todo $x \\in \\mathbb{R}$, luego "
                  "$\\text{Dom}(g) = \\mathbb{R}$."
               ),
               "justificacion_md": "Polinomio sin restricciones.",
               "es_resultado": False},
              {"accion_md": (
                  "Para $f$, el denominador exige $x - 1 \\neq 0$, luego $x \\neq 1$. Por tanto:\n\n"
                  "$\\text{Dom}(f) = \\mathbb{R} \\setminus \\{1\\} \\neq \\mathbb{R} = \\text{Dom}(g).$"
               ),
               "justificacion_md": "Cociente exige denominador no nulo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión:** $f \\neq g$ como funciones, **a pesar** de que $f(x) = g(x)$ para "
                  "todo $x \\in \\text{Dom}(f)$. Los dominios difieren."
               ),
               "justificacion_md": "La regla algebraica simplificada no determina sola la función.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Dominio natural",
          body_md=(
              "Cuando una función se define dando solo la regla $y = f(x)$ sin especificar el dominio, "
              "se adopta la convención del **dominio natural** (o dominio máximo): el mayor subconjunto "
              "de $\\mathbb{R}$ donde $f(x)$ produce un valor real bien definido.\n\n"
              "$$\\text{Dom}(f) = \\{ x \\in \\mathbb{R} \\mid f(x) \\in \\mathbb{R} \\}.$$\n\n"
              "**Restricciones típicas a verificar:**\n\n"
              "- Denominador igual a cero (en cocientes).\n"
              "- Radicando negativo (en raíces de **índice par**).\n"
              "- Argumento no positivo (en logaritmos).\n"
              "- Cualquier combinación de las anteriores."
          )),

        b("ejemplo_resuelto",
          titulo="Dominio natural con varias restricciones",
          problema_md=(
              "Halle el dominio natural de $f(x) = \\sqrt{\\dfrac{2x - 3}{x^2 - 1}}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Restricciones:** el radicando debe ser $\\geq 0$ y el denominador no nulo.\n\n"
                  "$x \\in \\text{Dom}(f) \\iff \\dfrac{2x - 3}{x^2 - 1} \\geq 0 \\;\\land\\; x^2 - 1 \\neq 0.$"
               ),
               "justificacion_md": "Combinamos las dos restricciones de la expresión.",
               "es_resultado": False},
              {"accion_md": (
                  "Excluimos $x = \\pm 1$. Factorizando: $\\dfrac{2x - 3}{(x-1)(x+1)} \\geq 0$. "
                  "Ceros: $x = -1, 1, \\dfrac{3}{2}$."
               ),
               "justificacion_md": "Identificamos puntos críticos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Tabla de signos** (cap 2):\n\n"
                  "| Intervalo | $2x-3$ | $x-1$ | $x+1$ | Cociente |\n"
                  "|:---:|:---:|:---:|:---:|:---:|\n"
                  "| $(-\\infty, -1)$ | $-$ | $-$ | $-$ | $-$ |\n"
                  "| $(-1, 1)$ | $-$ | $-$ | $+$ | $+$ |\n"
                  "| $(1, 3/2)$ | $-$ | $+$ | $+$ | $-$ |\n"
                  "| $(3/2, +\\infty)$ | $+$ | $+$ | $+$ | $+$ |\n\n"
                  "El cociente es $\\geq 0$ en $(-1, 1)$ y $[3/2, +\\infty)$ (incluyendo $3/2$ del numerador, "
                  "excluyendo $\\pm 1$ del denominador)."
               ),
               "justificacion_md": "Aplicamos el método de tabla de signos del cap. 2.4.",
               "es_resultado": False},
              {"accion_md": (
                  "$$\\boxed{\\text{Dom}(f) = (-1, 1) \\cup \\left[ \\tfrac{3}{2}, +\\infty \\right).}$$"
               ),
               "justificacion_md": "Conjunto solución completo.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Recorrido (imagen)",
          body_md=(
              "El **recorrido** (o imagen, o rango) de $f: A \\to B$ es el conjunto de todos los valores "
              "que la función efectivamente alcanza:\n\n"
              "$$\\text{Rec}(f) = \\{ y \\in \\mathbb{R} \\mid \\exists x \\in \\text{Dom}(f) : f(x) = y \\}.$$\n\n"
              "**Estrategia para determinarlo:** partir de $y \\in \\text{Rec}(f)$, despejar $x$ en "
              "términos de $y$, y exigir que la solución pertenezca al dominio."
          )),

        b("ejemplo_resuelto",
          titulo="Recorrido despejando la variable",
          problema_md=(
              "Determine el recorrido de $f(x) = \\dfrac{x}{x^2 + 1}$."
          ),
          pasos=[
              {"accion_md": (
                  "Partimos de $y = \\dfrac{x}{x^2+1}$ y despejamos $x$. Multiplicando por "
                  "$x^2 + 1 > 0$:\n\n"
                  "$y(x^2 + 1) = x \\iff yx^2 - x + y = 0.$"
               ),
               "justificacion_md": "Cuadrática en $x$ (con $y$ como parámetro).",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso $y = 0$:** la ecuación se reduce a $-x = 0$, luego $x = 0 \\in \\text{Dom}(f)$. "
                  "Así $0 \\in \\text{Rec}(f)$."
               ),
               "justificacion_md": "Caso degenerado.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso $y \\neq 0$:** por la fórmula cuadrática, $x = \\dfrac{1 \\pm \\sqrt{1 - 4y^2}}{2y}$. "
                  "Para que $x \\in \\mathbb{R}$ se requiere $1 - 4y^2 \\geq 0 \\iff |y| \\leq \\dfrac{1}{2}$, "
                  "es decir $-\\dfrac{1}{2} \\leq y \\leq \\dfrac{1}{2}$."
               ),
               "justificacion_md": "Discriminante no negativo.",
               "es_resultado": False},
              {"accion_md": (
                  "Combinando ambos casos:\n\n"
                  "$$\\boxed{\\text{Rec}(f) = \\left[ -\\tfrac{1}{2}, \\tfrac{1}{2} \\right].}$$"
               ),
               "justificacion_md": "Caso $y = 0$ ya está incluido en el intervalo.",
               "es_resultado": True},
          ]),

        ej(
            "Dominio natural con raíz y cociente",
            "Halle el dominio natural de $f(x) = \\dfrac{1}{\\sqrt{4 - x^2}}$.",
            [
                "El radicando debe ser **estrictamente** positivo (raíz en denominador).",
                "Resolvé $4 - x^2 > 0$.",
            ],
            (
                "$4 - x^2 > 0 \\iff x^2 < 4 \\iff -2 < x < 2$.\n\n"
                "$$\\boxed{\\text{Dom}(f) = (-2, 2).}$$"
            ),
        ),

        fig(
            "Diagrama conceptual de una función real f: A -> B representada como una caja teal #06b6d4 "
            "etiquetada 'f' con flechas entrantes desde un conjunto A (óvalo a la izquierda con puntos "
            "etiquetados 'dominio') y salientes hacia un conjunto B (óvalo a la derecha, etiquetado "
            "'codominio'). Dentro de B, sombrear con ámbar #f59e0b la región alcanzada con etiqueta "
            "'imagen Im(f)'. Cada elemento del dominio tiene exactamente UNA flecha (resaltar regla de "
            "asignación única). Tipografía clara, fondo blanco, ejemplo f(x) = x^2 con dominio R y "
            "codominio R, imagen [0, +inf). " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica conceptos clave de funciones reales:",
          preguntas=[
              {"enunciado_md": "¿Cuál es el dominio máximo de $f(x) = \\dfrac{1}{\\sqrt{x - 2}}$?",
               "opciones_md": ["$x \\geq 2$", "$x > 2$", "$x \\geq 0$", "$x \\neq 2$"],
               "correcta": "B",
               "pista_md": "El radicando $\\geq 0$, pero como está en denominador, $> 0$.",
               "explicacion_md": "Se necesita $x - 2 > 0$ (estrictamente, pues está en el denominador). Dominio: $(2, +\\infty)$."},
              {"enunciado_md": "¿Por qué $f(x) = \\dfrac{(x-1)(x+2)}{x-1}$ y $g(x) = x + 2$ NO son la misma función?",
               "opciones_md": [
                   "Tienen distinta regla algebraica",
                   "Tienen distintos dominios: $f$ excluye $x = 1$ y $g$ no",
                   "$g$ tiene un punto extra",
                   "$f$ es discontinua",
               ],
               "correcta": "B",
               "pista_md": "Una función es regla + dominio + codominio.",
               "explicacion_md": "Aunque la simplificación da $x + 2$, el dominio de $f$ excluye $x = 1$. Funciones con distinto dominio NO son iguales."},
              {"enunciado_md": "Diferencia entre dominio e imagen de una función:",
               "opciones_md": [
                   "Son sinónimos",
                   "Dominio: valores de salida; imagen: valores de entrada",
                   "Dominio: valores de entrada; imagen: valores que efectivamente toma la función",
                   "Dominio = codominio siempre",
               ],
               "correcta": "C",
               "pista_md": "El dominio es 'desde dónde'; la imagen es 'qué se alcanza'.",
               "explicacion_md": "Dominio = entradas válidas. Imagen = $\\{f(x) : x \\in \\text{Dom}(f)\\}$, los valores efectivamente alcanzados (puede ser subconjunto estricto del codominio)."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Identificar función con fórmula:** $f(x) = \\dfrac{(x-1)(x+2)}{x-1}$ y $g(x) = x+2$ NO son iguales como funciones (dominios distintos).",
              "**Olvidar que la raíz cuadrada exige radicando $\\geq 0$:** índice par requiere subradical no negativo.",
              "**Confundir $\\geq 0$ con $> 0$:** en $\\sqrt{f(x)}$ basta $\\geq 0$, pero en $\\dfrac{1}{\\sqrt{f(x)}}$ se requiere $> 0$.",
              "**Pensar que el codominio es el recorrido:** son distintos. El recorrido $\\subseteq$ codominio, con igualdad solo si $f$ es sobreyectiva.",
              "**Reportar el recorrido sin verificar que el $x$ despejado pertenece al dominio:** la solución algebraica puede dar valores espurios.",
          ]),

        b("resumen",
          puntos_md=[
              "**Función real:** triple $(A, B, \\text{regla})$ con dominio, codominio y regla bien definida.",
              "**Igualdad:** mismo dominio, mismo codominio, misma regla.",
              "**Dominio natural:** mayor subconjunto de $\\mathbb{R}$ donde la fórmula da valor real.",
              "**Restricciones típicas:** denominador $\\neq 0$, radicando $\\geq 0$ (par), argumento $> 0$ (log).",
              "**Recorrido:** despejar $x$ en función de $y$, exigir $x \\in \\text{Dom}(f)$.",
              "**Próxima lección:** gráficas y funciones elementales.",
          ]),
    ]
    return {
        "id": "lec-ic-3-1-funciones-reales",
        "title": "Funciones reales",
        "description": "Definición formal de función real, igualdad de funciones, dominio natural y recorrido.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 3.2 Gráficas de funciones
# =====================================================================
def lesson_3_2():
    blocks = [
        b("texto", body_md=(
            "El **gráfico de una función** es la herramienta visual fundamental que codifica toda la "
            "información de cómo una función transforma sus entradas en salidas. Más que una curva, "
            "es un objeto matemático preciso definido como subconjunto del producto cartesiano.\n\n"
            "**Objetivos:**\n\n"
            "- Definir el gráfico formalmente.\n"
            "- Aplicar el **criterio de la recta vertical**.\n"
            "- Identificar dominio y recorrido desde la gráfica.\n"
            "- Conocer las **funciones elementales** (lineales, potencia, raíz, recíprocas).\n"
            "- Trazar funciones **definidas por partes** y la función valor absoluto.\n"
            "- Aplicar reflexiones."
        )),

        b("definicion",
          titulo="Gráfico de una función",
          body_md=(
              "El **gráfico** de $f: A \\to B$ es el subconjunto $G(f)$ del producto cartesiano "
              "$A \\times B$ formado por los pares $(x, f(x))$:\n\n"
              "$$G(f) = \\{ (x, y) \\in A \\times B \\mid y = f(x) \\}.$$\n\n"
              "Es una curva contenida en $\\mathbb{R}^2$. La condición $y = f(x)$ impone que a cada "
              "$x$ le corresponde **exactamente un** $y$ — consecuencia geométrica directa abajo."
          )),

        b("teorema",
          enunciado_md=(
              "**Criterio de la recta vertical.** Una curva en el plano coordenado es la gráfica de "
              "una función si y solo si **ninguna recta vertical la cruza más de una vez**.\n\n"
              "**Razón:** si una recta $x = a$ cortara la curva en dos puntos $(a, b)$ y $(a, c)$ con "
              "$b \\neq c$, el valor $a$ tendría dos imágenes — contradice la unicidad de la definición."
          )),

        fig(
            "Dos planos cartesianos lado a lado mostrando el criterio de la recta vertical. Plano "
            "izquierdo (etiquetado 'SÍ es función'): una parábola y = x² con una línea vertical "
            "punteada que la cruza en un solo punto, marcado con un círculo verde. Plano derecho "
            "(etiquetado 'NO es función'): una circunferencia x²+y²=4 con una línea vertical "
            "punteada que la cruza en DOS puntos, ambos marcados con círculos rojos. Subtítulos: "
            "'cada x tiene una sola imagen' vs 'x = 1 tiene dos imágenes: y = ±√3'. Color teal "
            "#06b6d4 para la curva válida, rojo suave para la no-función. Título: 'Criterio de la "
            "recta vertical'. " + STYLE
        ),

        b("definicion",
          titulo="Dominio y recorrido desde el gráfico",
          body_md=(
              "Una vez trazada la gráfica:\n\n"
              "- **Dominio** = proyección sobre el eje $x$ (todos los valores de $x$ con punto en la curva).\n"
              "- **Recorrido** = proyección sobre el eje $y$ (todos los valores $y$ alcanzados).\n\n"
              "Formalmente:\n\n"
              "$$\\text{Dom}(f) = \\{ x \\in \\mathbb{R} \\mid (x, y) \\in G(f) \\text{ para algún } y \\},$$\n\n"
              "$$\\text{Rec}(f) = \\{ y \\in \\mathbb{R} \\mid (x, y) \\in G(f) \\text{ para algún } x \\}.$$"
          )),

        b("ejemplo_resuelto",
          titulo="Gráfico de $f(x) = \\sqrt{4 - x^2}$",
          problema_md=(
              "Trace $f(x) = \\sqrt{4 - x^2}$ y determine dominio y recorrido."
          ),
          pasos=[
              {"accion_md": (
                  "$y = f(x) \\iff y = \\sqrt{4 - x^2} \\iff x^2 + y^2 = 4 \\;\\land\\; y \\geq 0.$\n\n"
                  "Esto es la **semicircunferencia superior** de centro $(0, 0)$ y radio $2$."
               ),
               "justificacion_md": "Elevamos al cuadrado y reconocemos la circunferencia, restringiendo "
                                   "$y \\geq 0$ por la raíz.",
               "es_resultado": False},
              {"accion_md": (
                  "**Dominio:** $4 - x^2 \\geq 0 \\iff -2 \\leq x \\leq 2$, luego "
                  "$\\text{Dom}(f) = [-2, 2]$.\n\n"
                  "**Recorrido:** $y = \\sqrt{4 - x^2}$ varía desde $0$ (en $x = \\pm 2$) hasta $2$ "
                  "(en $x = 0$). $\\boxed{\\text{Rec}(f) = [0, 2].}$"
               ),
               "justificacion_md": "Lectura directa desde la geometría.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Funciones elementales",
          body_md=(
              "Las cuatro familias más importantes a nivel introductorio:\n\n"
              "**1. Lineales/afines:** $f(x) = mx + b$. Recta. Dominio y recorrido $= \\mathbb{R}$ "
              "(si $m \\neq 0$). Si $m = 0$, función constante con recorrido $\\{b\\}$.\n\n"
              "**2. Potencia:** $f(x) = x^n$, $n \\in \\mathbb{N}$.\n"
              "- $n$ par: simétrica al eje $y$, parábola generalizada, $\\text{Rec} = [0, +\\infty)$.\n"
              "- $n$ impar: simétrica al origen, forma de \"S\", $\\text{Rec} = \\mathbb{R}$.\n\n"
              "**3. Raíz:** $f(x) = \\sqrt[n]{x}$.\n"
              "- $n$ par: $\\text{Dom} = \\text{Rec} = [0, +\\infty)$.\n"
              "- $n$ impar: $\\text{Dom} = \\text{Rec} = \\mathbb{R}$.\n\n"
              "**4. Recíprocas:** $f(x) = \\dfrac{1}{x^n}$. Excluye $x = 0$ del dominio. **Asíntotas** "
              "horizontal ($y = 0$) y vertical ($x = 0$). Caso $n$ impar: ramas en cuadrantes I y III; "
              "$n$ par: ambas en semiplano superior."
          )),

        b("definicion",
          titulo="Funciones definidas por partes",
          body_md=(
              "Una **función por partes** es aquella cuya regla cambia según el subconjunto del dominio. "
              "Sigue siendo **una sola función** — a cada $x$ le corresponde un único $f(x)$, "
              "determinado por la condición que satisface.\n\n"
              "Para graficar: trazar cada \"trozo\" en su subdominio respectivo, marcando con "
              "**punto cerrado** $\\bullet$ los extremos incluidos y **punto abierto** $\\circ$ los excluidos."
          )),

        b("ejemplo_resuelto",
          titulo="Función por partes",
          problema_md=(
              "Trace $f(x) = \\begin{cases} x^2 & \\text{si } x \\leq 1 \\\\ 2x + 1 & \\text{si } x > 1 \\end{cases}$ "
              "y determine $\\text{Rec}(f)$."
          ),
          pasos=[
              {"accion_md": (
                  "Para $x \\leq 1$: parábola $f(x) = x^2$. Extremo derecho $f(1) = 1$, **incluido** "
                  "($\\bullet$ en $(1, 1)$).\n\n"
                  "Para $x > 1$: recta $f(x) = 2x + 1$ con pendiente $2$. Extremo izquierdo $f(1) = 3$ "
                  "**no incluido** ($\\circ$ en $(1, 3)$)."
               ),
               "justificacion_md": "En $x = 1$ la función tiene un **salto**: el trozo izquierdo llega a $y = 1$ "
                                   "y el derecho parte desde $y = 3$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Recorrido:** del trozo parabólico ($x \\leq 1$) se alcanza $y \\in [0, +\\infty)$ "
                  "para el rango pleno, pero solo evaluamos en $x \\leq 1$ → $y \\in [0, 1]$ (mínimo en "
                  "$x = 0$, máximo en $x = -\\infty$ tendiendo a $\\infty$). Hmm: en $x \\leq 1$, "
                  "$x^2 \\geq 0$ alcanza todo $[0, +\\infty)$ (basta tomar $x \\leq -\\sqrt{y}$). "
                  "Del trozo lineal ($x > 1$): $y = 2x + 1 > 3$, $y \\in (3, +\\infty)$.\n\n"
                  "**Unión:** $[0, +\\infty) \\cup (3, +\\infty) = [0, +\\infty)$.\n\n"
                  "$\\boxed{\\text{Rec}(f) = [0, +\\infty).}$"
               ),
               "justificacion_md": "El trozo parabólico para $x \\leq 1$ ya cubre $[0, +\\infty)$ "
                                   "(porque $x \\to -\\infty \\Rightarrow x^2 \\to \\infty$).",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Función valor absoluto",
          body_md=(
              "$f(x) = |x|$ es uno de los ejemplos más importantes de función por partes:\n\n"
              "$$|x| = \\begin{cases} x & \\text{si } x \\geq 0, \\\\ -x & \\text{si } x < 0. \\end{cases}$$\n\n"
              "Su gráfica es una **\"V\"** con vértice en el origen. $\\text{Dom}(f) = \\mathbb{R}$, "
              "$\\text{Rec}(f) = [0, +\\infty)$."
          )),

        b("teorema",
          enunciado_md=(
              "**Reflexiones.**\n\n"
              "- **Eje $x$:** $y = -f(x)$ refleja la gráfica de $f$ respecto al eje $x$. Punto $(a, b) \\to (a, -b)$. "
              "Dominio igual; recorrido se refleja.\n"
              "- **Eje $y$:** $y = f(-x)$ refleja la gráfica respecto al eje $y$. Punto $(a, b) \\to (-a, b)$. "
              "Recorrido igual; dominio se refleja.\n"
              "- **Composición** $g(x) = -f(-x)$: rotación de $180°$ respecto al origen."
          )),

        ej(
            "Reflexión compuesta",
            "Si $f: [-3, -1] \\to [2, 4]$, halle el dominio y recorrido de $g(x) = -f(-x)$.",
            [
                "$f(-x)$: refleja en eje $y$ — dominio $[1, 3]$, recorrido $[2, 4]$.",
                "Aplicar el signo $-$: refleja en eje $x$ — dominio igual, recorrido se refleja.",
            ],
            (
                "**Paso 1 ($f(-x)$):** dominio $[1, 3]$ (negar y voltear), recorrido $[2, 4]$.\n\n"
                "**Paso 2 ($-f(-x)$):** dominio $[1, 3]$, recorrido $[-4, -2]$.\n\n"
                "$\\boxed{\\text{Dom}(g) = [1, 3], \\quad \\text{Rec}(g) = [-4, -2].}$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica tu lectura de gráficas:",
          preguntas=[
              {"enunciado_md": "¿Cuál es el criterio de la recta vertical?",
               "opciones_md": [
                   "Una curva es gráfica de función si toda recta horizontal la corta a lo más una vez",
                   "Una curva es gráfica de función si toda recta vertical la corta a lo más una vez",
                   "Una curva es gráfica de función si pasa por el origen",
                   "Una curva es gráfica de función si es continua",
               ],
               "correcta": "B",
               "pista_md": "A cada $x$ debe corresponder a lo más una $y = f(x)$.",
               "explicacion_md": "Una curva es gráfica de función si y solo si toda recta vertical la corta en a lo más un punto: garantiza unicidad de $f(x)$ por cada $x$."},
              {"enunciado_md": "¿La circunferencia $x^2 + y^2 = 4$ representa una función $y = f(x)$?",
               "opciones_md": [
                   "Sí, su dominio es $[-2, 2]$",
                   "No, falla el criterio de la recta vertical",
                   "Sí, si se restringe el codominio",
                   "Solo si se elimina el origen",
               ],
               "correcta": "B",
               "pista_md": "Para cada $x \\in (-2, 2)$ hay dos valores de $y$.",
               "explicacion_md": "Para $x = 0$, $y = 2$ y $y = -2$ pertenecen a la curva: hay dos valores de $y$ para un mismo $x$, así que NO es función."},
              {"enunciado_md": "Si una función por partes está definida con un círculo abierto en $(2, 3)$ y uno cerrado en $(2, 5)$, ¿cuánto vale $f(2)$?",
               "opciones_md": ["$3$", "$5$", "Ambos", "Indefinido"],
               "correcta": "B",
               "pista_md": "El círculo cerrado indica el valor incluido.",
               "explicacion_md": "El círculo cerrado señala el valor que toma la función; el abierto muestra el límite no incluido. $f(2) = 5$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Pensar que toda curva es el gráfico de una función:** la circunferencia completa $x^2+y^2=4$ NO lo es (falla criterio recta vertical).",
              "**Olvidar marcar puntos abiertos vs. cerrados** en funciones por partes.",
              "**Reflejar sin invertir el orden de los extremos:** $f(-x)$ con dominio $[a, b]$ tiene dominio $[-b, -a]$ (no $[-a, -b]$).",
              "**Confundir $y = -|x|$ con $y = |-x|$:** la primera refleja en eje $x$ (V invertida); la segunda es **igual** a $|x|$.",
              "**Reportar recorrido como si fuera dominio del codominio:** son lecturas distintas (eje $y$ vs. eje $x$).",
          ]),

        b("resumen",
          puntos_md=[
              "**Gráfico:** $G(f) = \\{(x, y) : y = f(x)\\}$.",
              "**Criterio recta vertical:** ninguna vertical corta más de una vez.",
              "**Dominio = proyección sobre eje $x$**, **recorrido = proyección sobre eje $y$**.",
              "**Familias elementales:** lineal, potencia, raíz, recíproca.",
              "**Por partes:** trazar trozo a trozo, atender extremos abiertos/cerrados.",
              "**Reflexiones:** $-f(x)$ en eje $x$, $f(-x)$ en eje $y$.",
              "**Próxima lección:** transformaciones generales (escalamientos + traslaciones).",
          ]),
    ]
    return {
        "id": "lec-ic-3-2-graficas-funciones",
        "title": "Gráficas de funciones",
        "description": "Definición formal de gráfico, criterio de la recta vertical, funciones elementales, definidas por partes y reflexiones.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 3.3 Transformaciones de funciones
# =====================================================================
def lesson_3_3():
    blocks = [
        b("texto", body_md=(
            "Las **transformaciones de funciones** son la herramienta clave para construir gráficas "
            "complejas a partir de una función base. Permiten pasar de $f(x)$ a $g(x) = \\pm A\\,f(\\pm \\omega(x + h)) + k$ "
            "interpretando cada parámetro geométricamente, sin necesidad de tabular punto a punto.\n\n"
            "**Objetivos:**\n\n"
            "- Comprender el efecto de cada tipo de transformación.\n"
            "- Identificar **escalamientos**, **reflexiones** y **traslaciones**.\n"
            "- Combinar transformaciones en el orden correcto.\n"
            "- Determinar dominio y recorrido a partir de la gráfica transformada."
        )),

        b("definicion",
          titulo="Escalamientos verticales",
          body_md=(
              "Para graficar $y = A f(x)$ a partir de $y = f(x)$ con $A > 0$:\n\n"
              "- Si $A > 1$: **alargamiento vertical** en factor $A$.\n"
              "- Si $0 < A < 1$: **contracción vertical** en factor $A$.\n\n"
              "En coordenadas, $(x_0, y_0) \\mapsto (x_0, A y_0)$. Los puntos sobre el eje $x$ "
              "(donde $f(x) = 0$) permanecen fijos."
          )),

        b("definicion",
          titulo="Escalamientos horizontales",
          body_md=(
              "Para graficar $y = f(\\omega x)$ a partir de $y = f(x)$ con $\\omega > 0$:\n\n"
              "- Si $\\omega > 1$: **contracción horizontal** en factor $1/\\omega$.\n"
              "- Si $0 < \\omega < 1$: **alargamiento horizontal** en factor $1/\\omega$.\n\n"
              "En coordenadas, $(x_0, y_0) \\mapsto (x_0 / \\omega,\\ y_0)$. **Inverso al valor de "
              "$\\omega$**: un $\\omega$ grande comprime; uno pequeño alarga."
          )),

        b("definicion",
          titulo="Traslaciones",
          body_md=(
              "**Vertical:** $y = f(x) + k$.\n\n"
              "- $k > 0$: gráfica sube $k$ unidades. $(x_0, y_0) \\to (x_0, y_0 + k)$.\n"
              "- $k < 0$: gráfica baja $|k|$ unidades.\n\n"
              "**Horizontal:** $y = f(x + h)$.\n\n"
              "- $h > 0$: gráfica se desplaza $h$ unidades a la **izquierda**.\n"
              "- $h < 0$: gráfica se desplaza $|h|$ unidades a la **derecha**.\n\n"
              "**Cuidado:** el signo del desplazamiento horizontal es **contraintuitivo** — un $h > 0$ "
              "mueve a la izquierda, no a la derecha. Esto se debe a que $x + h$ alcanza el valor original "
              "cuando $x$ es **menor**."
          )),

        b("teorema",
          enunciado_md=(
              "**Transformación general.** Toda transformación combinada se escribe en la forma\n\n"
              "$$g(x) = \\pm A\\, f\\bigl(\\pm \\omega(x + h)\\bigr) + k,$$\n\n"
              "con $A > 0$ y $\\omega > 0$. Se aplican en **3 fases**:\n\n"
              "1. **Reflexiones** (signos negativos): $-A$ refleja en eje $x$; $-\\omega$ refleja en eje $y$.\n"
              "2. **Escalamientos** ($A$ y $\\omega$): vertical y horizontal.\n"
              "3. **Traslaciones** ($h$ y $k$): horizontal y vertical."
          )),

        b("intuicion", body_md=(
            "**Tabla resumen del efecto de cada parámetro:**\n\n"
            "| Parámetro | Valor | Efecto |\n"
            "|:---:|:---:|:---|\n"
            "| Signo de $A$ | $-$ | Reflexión respecto eje $x$ |\n"
            "| Signo de $\\omega$ | $-$ | Reflexión respecto eje $y$ |\n"
            "| $A > 1$ | — | Alarga verticalmente |\n"
            "| $0 < A < 1$ | — | Contrae verticalmente |\n"
            "| $\\omega > 1$ | — | Contrae horizontalmente |\n"
            "| $0 < \\omega < 1$ | — | Alarga horizontalmente |\n"
            "| $h > 0$ | — | Traslada a la izquierda |\n"
            "| $h < 0$ | — | Traslada a la derecha |\n"
            "| $k > 0$ | — | Traslada hacia arriba |\n"
            "| $k < 0$ | — | Traslada hacia abajo |"
        )),

        fig(
            "Cuadrícula 2x3 mostrando seis transformaciones de la función base f(x)=x² (parábola "
            "negra punteada como referencia en cada panel). Panel 1: f(x)+2 (parábola desplazada "
            "hacia arriba, color teal #06b6d4, etiqueta 'k=2: sube'). Panel 2: f(x-3) (desplazada "
            "a la derecha, etiqueta 'h=-3: derecha'). Panel 3: 2·f(x) (alargada verticalmente, "
            "etiqueta 'A=2: alarga vert.'). Panel 4: -f(x) (reflejada respecto al eje x, color "
            "ámbar #f59e0b, etiqueta 'signo -: refleja'). Panel 5: f(2x) (contraída "
            "horizontalmente, etiqueta 'ω=2: contrae horiz.'). Panel 6: -f(x-1)+3 (combinada: "
            "refleja, mueve derecha 1, sube 3, color teal). Cada panel con ejes simples y la "
            "curva original punteada para comparar. Título: 'Las 6 transformaciones básicas'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Identificar transformaciones",
          problema_md=(
              "La gráfica de $g(x) = -\\sqrt{x + 3} + 1$ se obtiene a partir de $f(x) = \\sqrt{x}$. "
              "Identifique las transformaciones en orden y determine $\\text{Dom}(g)$ y $\\text{Rec}(g)$."
          ),
          pasos=[
              {"accion_md": (
                  "Comparando $g(x) = -\\sqrt{x+3} + 1$ con $\\pm A\\,f(\\pm\\omega(x+h)) + k$: "
                  "$A = 1$, signo $-$ delante (reflexión en $x$), $\\omega = 1$, $h = 3$, $k = 1$."
               ),
               "justificacion_md": "Identificación de parámetros.",
               "es_resultado": False},
              {"accion_md": (
                  "**Fase 1 — Reflexión en eje $x$:** $\\sqrt{x} \\to -\\sqrt{x}$. La gráfica que crecía hacia arriba ahora decrece hacia abajo.\n\n"
                  "**Fase 2 — Sin escalamiento** (A = ω = 1).\n\n"
                  "**Fase 3a — Traslación horizontal** ($h = 3 > 0$): mueve $3$ unidades a la **izquierda**. Punto inicial $(0, 0) \\to (-3, 0)$.\n\n"
                  "**Fase 3b — Traslación vertical** ($k = 1 > 0$): sube $1$ unidad. Punto inicial $(-3, 0) \\to (-3, 1)$."
               ),
               "justificacion_md": "Aplicamos las 3 fases en orden.",
               "es_resultado": False},
              {"accion_md": (
                  "**Dominio:** $x + 3 \\geq 0 \\iff x \\geq -3$, luego $\\text{Dom}(g) = [-3, +\\infty)$.\n\n"
                  "**Recorrido:** $-\\sqrt{x+3} \\leq 0$, sumar $1$ da valores $\\leq 1$. Como $\\sqrt{\\cdot}$ "
                  "alcanza todo $[0, +\\infty)$, $-\\sqrt{\\cdot}$ alcanza $(-\\infty, 0]$, y $-\\sqrt{\\cdot} + 1$ "
                  "alcanza $(-\\infty, 1]$.\n\n"
                  "$$\\boxed{\\text{Dom}(g) = [-3, +\\infty), \\quad \\text{Rec}(g) = (-\\infty, 1].}$$"
               ),
               "justificacion_md": "Análisis del dominio y recorrido transformados.",
               "es_resultado": True},
          ]),

        ej(
            "Transformación de $|x|$",
            "Identifique las transformaciones que llevan $f(x) = |x|$ a $g(x) = 2|x - 1| - 3$. "
            "Determine $\\text{Dom}(g)$, $\\text{Rec}(g)$ y el vértice.",
            [
                "Identificá $A$, $h$, $k$ comparando con $\\pm A f(\\pm \\omega(x+h)) + k$.",
                "Aplicá las 3 fases en orden.",
                "El vértice del $|x|$ original es $(0, 0)$ — seguilo a través de las transformaciones.",
            ],
            (
                "$A = 2$, $\\omega = 1$, $h = -1$, $k = -3$.\n\n"
                "**Fase 1:** sin reflexión.\n\n"
                "**Fase 2:** alargamiento vertical en factor $2$ — la \"V\" se hace más empinada.\n\n"
                "**Fase 3:** $h = -1 < 0$ traslada a la derecha 1; $k = -3$ baja 3.\n\n"
                "Vértice: $(0, 0) \\to (0, 0)$ tras escalamiento $\\to (1, 0) \\to (1, -3)$.\n\n"
                "$\\boxed{\\text{Dom}(g) = \\mathbb{R}, \\quad \\text{Rec}(g) = [-3, +\\infty), \\quad \\text{vértice} = (1, -3).}$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica las transformaciones de funciones:",
          preguntas=[
              {"enunciado_md": "Si $g(x) = f(x - 3)$, ¿cómo se transforma la gráfica de $f$?",
               "opciones_md": [
                   "Se traslada $3$ unidades a la izquierda",
                   "Se traslada $3$ unidades a la derecha",
                   "Se traslada $3$ unidades hacia abajo",
                   "Se refleja sobre el eje $y$",
               ],
               "correcta": "B",
               "pista_md": "Restar dentro del argumento traslada en sentido positivo (derecha).",
               "explicacion_md": "$f(x - h)$ traslada $h$ a la derecha. El signo es 'engañoso': $-3$ dentro = derecha por $3$."},
              {"enunciado_md": "¿Cuál es el efecto de $g(x) = f(2x)$ comparado con $f(x)$?",
               "opciones_md": [
                   "Estira horizontalmente por factor $2$",
                   "Comprime horizontalmente por factor $2$",
                   "Estira verticalmente por factor $2$",
                   "Comprime verticalmente por factor $2$",
               ],
               "correcta": "B",
               "pista_md": "Cambios horizontales con $\\omega > 1$ comprimen.",
               "explicacion_md": "$f(\\omega x)$ con $\\omega > 1$ comprime horizontalmente; con $0 < \\omega < 1$ estira. La gráfica de $f(2x)$ alcanza los mismos $y$ en la mitad del $x$."},
              {"enunciado_md": "¿Cuál es la gráfica de $g(x) = -f(x) + 2$ a partir de $f(x)$?",
               "opciones_md": [
                   "Reflejar sobre eje $x$ y trasladar $2$ hacia arriba",
                   "Reflejar sobre eje $y$ y trasladar $2$ hacia arriba",
                   "Reflejar sobre eje $x$ y trasladar $2$ hacia abajo",
                   "Solo trasladar $2$ hacia arriba",
               ],
               "correcta": "A",
               "pista_md": "$-f(x)$ refleja sobre el eje $x$; $+2$ es traslación vertical hacia arriba.",
               "explicacion_md": "$-f(x)$ refleja respecto al eje $x$ (cambia signo de $y$); luego $+2$ traslada hacia arriba."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir signo del desplazamiento horizontal:** $f(x + 3)$ traslada a la **izquierda**, no a la derecha.",
              "**Aplicar las transformaciones en orden incorrecto:** primero reflexiones, después escalamientos, después traslaciones.",
              "**Confundir efecto del coeficiente horizontal:** $f(2x)$ comprime ($\\omega > 1$), $f(x/2)$ alarga ($\\omega < 1$).",
              "**Pensar que $\\omega < 0$ es invalido:** simplemente significa reflexión en eje $y$ + escalamiento por $|\\omega|$.",
              "**Olvidar que el dominio cambia con traslaciones horizontales y reflexiones en $y$:** un dominio $[a, b]$ tras $f(x - h)$ pasa a $[a + h, b + h]$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma general:** $g(x) = \\pm A f(\\pm \\omega(x + h)) + k$.",
              "**3 fases** en orden: reflexiones → escalamientos → traslaciones.",
              "**Vertical (sin invertir):** $A f(x) + k$ — escala y traslada en eje $y$.",
              "**Horizontal (invertido):** $f(\\omega(x + h))$ — efectos opuestos al valor de los parámetros.",
              "**Reflexiones:** $-f$ en eje $x$, $f(-x)$ en eje $y$.",
              "**Próxima lección:** funciones racionales, asíntotas y método sistemático.",
          ]),
    ]
    return {
        "id": "lec-ic-3-3-transformaciones",
        "title": "Transformaciones de funciones",
        "description": "Escalamientos verticales y horizontales, reflexiones, traslaciones, y combinación en la forma general $\\pm Af(\\pm\\omega(x+h))+k$.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# 3.4 Funciones racionales
# =====================================================================
def lesson_3_4():
    blocks = [
        b("texto", body_md=(
            "Las **funciones racionales** son cocientes de polinomios. Aparecen en numerosos contextos "
            "de la física, ingeniería y economía. Su análisis requiere comprender no solo el dominio, "
            "sino el **comportamiento asintótico**: cómo se comporta la función cerca de valores "
            "críticos y cuando $x$ crece sin cota.\n\n"
            "**Objetivos:**\n\n"
            "- Definir función racional e identificar su dominio.\n"
            "- Determinar **asíntotas verticales y horizontales** aplicando el teorema de asíntotas.\n"
            "- Aplicar el **método sistemático de 6 pasos** para trazar gráficas.\n"
            "- Distinguir **asíntotas** de **hoyos** (cancelaciones)."
        )),

        b("definicion",
          titulo="Función racional",
          body_md=(
              "Una **función racional** es de la forma\n\n"
              "$$f(x) = \\frac{P(x)}{Q(x)} = \\frac{a_n x^n + \\cdots + a_0}{b_m x^m + \\cdots + b_0},$$\n\n"
              "con $P, Q$ polinomios, $a_n \\neq 0$, $b_m \\neq 0$. **$n$** es el grado del numerador y "
              "**$m$** el del denominador.\n\n"
              "**Dominio:**\n\n"
              "$$\\text{Dom}(f) = \\mathbb{R} \\setminus \\{ x \\mid Q(x) = 0 \\}.$$\n\n"
              "Para encontrar el dominio, factorizar $Q$ y excluir sus raíces."
          )),

        b("definicion",
          titulo="Asíntotas",
          body_md=(
              "**Asíntota vertical** $x = a$: $f(x) \\to \\pm\\infty$ cuando $x \\to a^+$ o $x \\to a^-$.\n\n"
              "**Asíntota horizontal** $y = b$: $\\lim_{x \\to \\pm\\infty} f(x) = b$. La gráfica se "
              "aproxima a la recta $y = b$ cuando $x$ crece o decrece sin cota."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema de asíntotas para funciones racionales** $f(x) = P(x)/Q(x)$ con $\\text{grad}(P) = n$, "
              "$\\text{grad}(Q) = m$:\n\n"
              "**1. Asíntotas verticales:** si $a$ es cero de $Q$ con $P(a) \\neq 0$, entonces $x = a$ es "
              "asíntota vertical. (Si $P(a) = Q(a) = 0$ hay un **hoyo** o cancelación, no asíntota.)\n\n"
              "**2. Asíntota horizontal:**\n\n"
              "- Si $n < m$: $y = 0$.\n"
              "- Si $n = m$: $y = \\dfrac{a_n}{b_m}$ (cociente de coeficientes líderes).\n"
              "- Si $n > m$: **no hay** asíntota horizontal (puede haber oblicua, en cursos posteriores).\n\n"
              "**Idea:** para $|x|$ grande, $f(x) \\approx \\dfrac{a_n}{b_m} x^{n-m}$."
          )),

        b("ejemplo_resuelto",
          titulo="Asíntotas de una racional cuadrática",
          problema_md=(
              "Halle las asíntotas vertical y horizontal de $r(x) = \\dfrac{3x^2 - 2x - 1}{2x^2 + 3x - 2}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Asíntota horizontal:** $n = m = 2$, coef. líderes $a_2 = 3$, $b_2 = 2$. "
                  "Por el teorema, asíntota $y = \\dfrac{3}{2}$."
               ),
               "justificacion_md": "Caso $n = m$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Asíntotas verticales:** factorizamos. Numerador: $3x^2 - 2x - 1 = (3x + 1)(x - 1)$, "
                  "ceros $-\\dfrac{1}{3}$ y $1$. Denominador: $2x^2 + 3x - 2 = (2x - 1)(x + 2)$, ceros "
                  "$\\dfrac{1}{2}$ y $-2$.\n\n"
                  "Como ningún cero del denominador coincide con uno del numerador, ambos generan "
                  "asíntotas verticales: $x = \\dfrac{1}{2}$ y $x = -2$."
               ),
               "justificacion_md": "Verificamos que no hay cancelaciones.",
               "es_resultado": False},
              {"accion_md": (
                  "$$\\boxed{\\text{Asíntotas verticales: } x = \\tfrac{1}{2},\\ x = -2; \\quad \\text{horizontal: } y = \\tfrac{3}{2}.}$$"
               ),
               "justificacion_md": "Resumen.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Método sistemático para graficar (6 pasos)",
          body_md=(
              "Para graficar $r(x) = P(x)/Q(x)$ con rigor, seguir estos seis pasos en orden:\n\n"
              "1. **Factorizar** $P$ y $Q$ completamente. Identificar ceros, asíntotas y posibles **hoyos**.\n"
              "2. **Tabla de signos** de $r(x)$ en los intervalos delimitados por todos los ceros (numerador y denominador).\n"
              "3. **Intersecciones con los ejes:** con eje $x$ son los ceros del numerador (que no se cancelen); "
              "con eje $y$ es $r(0)$ si $0 \\in \\text{Dom}(r)$.\n"
              "4. **Asíntotas verticales:** ceros del denominador no canceladoss. Determinar el comportamiento "
              "($+\\infty$ o $-\\infty$) a cada lado con valores de prueba.\n"
              "5. **Asíntota horizontal** aplicando el teorema.\n"
              "6. **Trazar la curva** usando toda la información en cada intervalo.\n\n"
              "**Hoyos vs. asíntotas:** si un factor se cancela entre numerador y denominador, ese punto es "
              "un **hoyo** (discontinuidad removible), no una asíntota."
          )),

        b("ejemplo_resuelto",
          titulo="Gráfica con asíntotas (sin hoyos)",
          problema_md=(
              "Analice $r(x) = \\dfrac{2x^2 + 7x - 4}{x^2 + x - 2}$ y exprese dominio."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1 — Factorizar:**\n"
                  "- Numerador: $2x^2 + 7x - 4 = (2x - 1)(x + 4)$.\n"
                  "- Denominador: $x^2 + x - 2 = (x - 1)(x + 2)$.\n\n"
                  "Sin factores comunes → no hay hoyos. $r(x) = \\dfrac{(2x - 1)(x + 4)}{(x - 1)(x + 2)}$."
               ),
               "justificacion_md": "Factorización por inspección.",
               "es_resultado": False},
              {"accion_md": (
                  "**Pasos 3-5 — Datos clave:**\n\n"
                  "- Intersecciones con eje $x$: ceros del numerador $x = \\dfrac{1}{2}$ y $x = -4$.\n"
                  "- Intersección con eje $y$: $r(0) = \\dfrac{-4}{-2} = 2$.\n"
                  "- Asíntotas verticales: $x = 1$ y $x = -2$.\n"
                  "- Asíntota horizontal ($n = m = 2$): $y = \\dfrac{2}{1} = 2$."
               ),
               "justificacion_md": "Aplicación directa de los pasos.",
               "es_resultado": False},
              {"accion_md": (
                  "$$\\boxed{\\text{Dom}(r) = \\mathbb{R} \\setminus \\{-2, 1\\}.}$$\n\n"
                  "**Asíntotas:** $x = -2$, $x = 1$ (verticales), $y = 2$ (horizontal). **Cortes:** "
                  "$(-4, 0)$, $\\left(\\dfrac{1}{2}, 0\\right)$, $(0, 2)$."
               ),
               "justificacion_md": "Información completa para trazar.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Función con hoyo",
          problema_md=(
              "Analice $f(x) = \\dfrac{x^2 - 4}{x - 2}$. ¿Asíntotas? ¿Hoyos?"
          ),
          pasos=[
              {"accion_md": (
                  "Factorizando: $\\dfrac{(x - 2)(x + 2)}{x - 2}$. El factor $(x - 2)$ **se cancela**.\n\n"
                  "Para $x \\neq 2$: $f(x) = x + 2$. La función se comporta como una recta, **excepto** "
                  "en $x = 2$, donde no está definida."
               ),
               "justificacion_md": "Cancelación de factor común.",
               "es_resultado": False},
              {"accion_md": (
                  "En $x = 2$ hay un **hoyo** (no asíntota). El \"valor faltante\" sería $f(2) = 4$ si "
                  "se completara por continuidad, pero formalmente $2 \\notin \\text{Dom}(f)$.\n\n"
                  "$\\text{Dom}(f) = \\mathbb{R} \\setminus \\{2\\}$. Sin asíntotas verticales (el factor problemático canceló). "
                  "Sin asíntota horizontal (es una recta de grado $1$).\n\n"
                  "$\\boxed{\\text{Hoyo en } (2, 4); \\text{ resto de la gráfica: recta } y = x + 2.}$"
               ),
               "justificacion_md": "Distinción crucial: cancelación = hoyo, no asíntota.",
               "es_resultado": True},
          ]),

        ej(
            "Identificar asíntotas",
            "Halle asíntotas verticales y horizontales de $f(x) = \\dfrac{2x + 5}{x - 3}$ y exprese dominio y recorrido.",
            [
                "Verifica si hay cancelaciones (no las hay).",
                "Asíntota vertical: cero del denominador.",
                "Para asíntota horizontal compará grados.",
                "Recorrido: lo que la gráfica NO alcanza es justo la asíntota horizontal.",
            ],
            (
                "Sin cancelaciones. Asíntota vertical $x = 3$. Grados $n = m = 1$, asíntota horizontal $y = \\dfrac{2}{1} = 2$.\n\n"
                "$\\text{Dom}(f) = \\mathbb{R} \\setminus \\{3\\}$. Como la gráfica nunca cruza la asíntota horizontal $y = 2$ "
                "(función racional lineal sobre lineal): $\\text{Rec}(f) = \\mathbb{R} \\setminus \\{2\\}$."
            ),
        ),

        fig(
            "Diagrama mostrando una función racional f(x) = (x^2 - 1) / (x - 1) graficada en sistema "
            "cartesiano. Curva visible es la recta y = x + 1 (porque (x^2 - 1)/(x - 1) = x + 1) pero "
            "con un círculo abierto en (1, 2) marcado en ámbar #f59e0b con etiqueta 'hoyo en x = 1: "
            "factor cancelable'. Al lado, segunda función g(x) = 1/(x - 2) en panel adyacente con su "
            "asíntota vertical x = 2 dibujada como línea punteada teal #06b6d4 y etiqueta 'asíntota "
            "vertical: factor NO cancelable'. Ejes claros, contraste entre 'hoyo' y 'asíntota'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica el análisis de funciones racionales:",
          preguntas=[
              {"enunciado_md": "¿Cuál es el dominio de $f(x) = \\dfrac{x + 3}{x^2 - 4}$?",
               "opciones_md": [
                   "$\\mathbb{R}$",
                   "$\\mathbb{R} \\setminus \\{2, -2\\}$",
                   "$\\mathbb{R} \\setminus \\{-3\\}$",
                   "$\\mathbb{R} \\setminus \\{4\\}$",
               ],
               "correcta": "B",
               "pista_md": "Buscá las raíces del denominador.",
               "explicacion_md": "$x^2 - 4 = 0 \\iff x = \\pm 2$. Esos valores anulan el denominador y deben excluirse."},
              {"enunciado_md": "En $f(x) = \\dfrac{(x - 1)(x + 2)}{(x - 1)(x - 3)}$, ¿qué hay en $x = 1$?",
               "opciones_md": [
                   "Asíntota vertical",
                   "Hoyo (discontinuidad evitable)",
                   "Cero de la función",
                   "Asíntota horizontal",
               ],
               "correcta": "B",
               "pista_md": "El factor $(x - 1)$ se cancela arriba y abajo.",
               "explicacion_md": "Cuando un factor cancela arriba y abajo, hay HOYO en ese $x$, no asíntota. La asíntota vertical aparece solo si el factor del denominador NO se cancela."},
              {"enunciado_md": "Para $f(x) = \\dfrac{2x^2 + 1}{x^2 - 5}$, ¿cuál es la asíntota horizontal?",
               "opciones_md": ["$y = 0$", "$y = 1$", "$y = 2$", "No tiene"],
               "correcta": "C",
               "pista_md": "Comparar grados: si son iguales, la asíntota es el cociente de coeficientes líderes.",
               "explicacion_md": "$\\text{grad}(P) = \\text{grad}(Q) = 2$, asíntota horizontal $y = a_n / b_m = 2/1 = 2$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir hoyo con asíntota:** si un factor se cancela, hay hoyo, NO asíntota.",
              "**Olvidar verificar cancelaciones antes de declarar asíntotas verticales:** factorizá primero.",
              "**Reportar asíntota oblicua sin estar en grado correcto:** solo aparecen cuando $n = m + 1$ (curso posterior).",
              "**Pensar que el grafo nunca cruza asíntota horizontal:** sí puede cruzarla a distancia finita; lo que no hace es cruzarla \"al infinito\".",
              "**Excluir ceros del numerador del dominio:** el dominio solo excluye ceros del **denominador**.",
          ]),

        b("resumen",
          puntos_md=[
              "**Función racional:** $f = P/Q$, dominio excluye ceros de $Q$.",
              "**Asíntota vertical** $x = a$: cero de $Q$ que NO se cancela con el numerador.",
              "**Asíntota horizontal:** depende de $n$ vs. $m$ — caso $n < m$ ($y = 0$), $n = m$ ($y = a_n/b_m$), $n > m$ (no hay).",
              "**Hoyo** vs. asíntota: cancelación produce hoyo; cero no cancelado del denominador produce asíntota.",
              "**Método 6 pasos:** factorizar → tabla signos → intersecciones → asíntotas verticales → horizontal → trazar.",
              "**Próxima lección:** funciones biyectivas — inyectividad y sobreyectividad.",
          ]),
    ]
    return {
        "id": "lec-ic-3-4-funciones-racionales",
        "title": "Funciones racionales",
        "description": "Definición, asíntotas verticales y horizontales (teorema), método sistemático de 6 pasos y distinción hoyo / asíntota.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# =====================================================================
# 3.5 Funciones biyectivas
# =====================================================================
def lesson_3_5():
    blocks = [
        b("texto", body_md=(
            "El estudio de las **funciones biyectivas** es uno de los pilares fundamentales del análisis "
            "de funciones reales. Comprender cuándo una función es inyectiva, sobreyectiva o ambas "
            "permite determinar si admite una **inversa bien definida**, lo cual es esencial en cálculo "
            "diferencial e integral.\n\n"
            "**Objetivos:**\n\n"
            "- Definir formalmente función **inyectiva**, **sobreyectiva** y **biyectiva**.\n"
            "- Aplicar el **test de la recta horizontal** como criterio geométrico de inyectividad.\n"
            "- Demostrar analíticamente las tres propiedades.\n"
            "- Calcular el recorrido para estudiar sobreyectividad."
        )),

        b("definicion",
          titulo="Función inyectiva",
          body_md=(
              "Sea $f: A \\to B$. $f$ es **inyectiva** (o uno-a-uno) si elementos distintos del dominio "
              "tienen imágenes distintas:\n\n"
              "$$(\\forall x_1, x_2 \\in A)\\bigl(x_1 \\neq x_2 \\Rightarrow f(x_1) \\neq f(x_2)\\bigr).$$\n\n"
              "Equivalentemente (forma **contrarrecíproca**, más útil en demostraciones):\n\n"
              "$$(\\forall x_1, x_2 \\in A)\\bigl(f(x_1) = f(x_2) \\Rightarrow x_1 = x_2\\bigr).$$\n\n"
              "Intuitivamente, $f$ no \"aplasta\" información: cada salida proviene de **a lo más una** entrada."
          )),

        b("teorema",
          enunciado_md=(
              "**Test de la recta horizontal.** $f$ es inyectiva si y solo si **toda recta horizontal "
              "corta su gráfica a lo más una vez**.\n\n"
              "Si una recta $y = c$ cortara la gráfica en dos puntos $(x_1, c)$ y $(x_2, c)$ con "
              "$x_1 \\neq x_2$, entonces $f(x_1) = f(x_2) = c$, contradiciendo inyectividad."
          )),

        fig(
            "Dos planos cartesianos lado a lado mostrando el test de la recta horizontal. Plano "
            "izquierdo (etiquetado 'Inyectiva: y = x³'): curva en S de y=x³ con tres rectas "
            "horizontales punteadas en y=-2, y=0, y=4, cada una cortando la curva en exactamente "
            "un punto (círculos verdes). Plano derecho (etiquetado 'NO inyectiva: y = x²'): "
            "parábola y=x² con una recta horizontal punteada en y=4 que corta la parábola en dos "
            "puntos (-2, 4) y (2, 4) (círculos rojos). Color teal #06b6d4 para curva inyectiva, "
            "color cálido para la no inyectiva. Subtítulos: 'cada y tiene a lo más una preimagen' "
            "vs 'y=4 tiene dos preimágenes: x=2 y x=-2'. Título: 'Test de la recta horizontal'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Demostración de inyectividad",
          problema_md=(
              "Demuestre que $f: \\mathbb{R} \\setminus \\{1\\} \\to \\mathbb{R}$, "
              "$f(x) = \\dfrac{2x + 1}{x - 1}$, es inyectiva."
          ),
          pasos=[
              {"accion_md": (
                  "Sean $x_1, x_2 \\in \\mathbb{R} \\setminus \\{1\\}$ tales que $f(x_1) = f(x_2)$:\n\n"
                  "$\\dfrac{2x_1 + 1}{x_1 - 1} = \\dfrac{2x_2 + 1}{x_2 - 1}.$"
               ),
               "justificacion_md": "Empezamos de la hipótesis de igualdad de imágenes.",
               "es_resultado": False},
              {"accion_md": (
                  "Multiplicando en cruz (denominadores no nulos):\n\n"
                  "$(2x_1 + 1)(x_2 - 1) = (2x_2 + 1)(x_1 - 1).$\n\n"
                  "Expandiendo: $2x_1 x_2 - 2x_1 + x_2 - 1 = 2x_1 x_2 - 2x_2 + x_1 - 1$."
               ),
               "justificacion_md": "Operación válida porque ambos denominadores son distintos de cero.",
               "es_resultado": False},
              {"accion_md": (
                  "Cancelando $2x_1 x_2$ y $-1$: $-2x_1 + x_2 = -2x_2 + x_1 \\iff 3x_2 = 3x_1 \\iff x_1 = x_2$.\n\n"
                  "Por tanto $f(x_1) = f(x_2) \\Rightarrow x_1 = x_2$. $\\boxed{f \\text{ es inyectiva.}}$"
               ),
               "justificacion_md": "Aplicamos la forma contrarrecíproca de la definición.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Refutar inyectividad por contraejemplo",
          problema_md=(
              "Pruebe que $f: \\mathbb{R} \\to \\mathbb{R}$, $f(x) = \\dfrac{x + 1}{x^2 + 1}$, no es inyectiva."
          ),
          pasos=[
              {"accion_md": (
                  "Calculemos valores específicos: $f(0) = \\dfrac{1}{1} = 1$ y $f(1) = \\dfrac{2}{2} = 1$."
               ),
               "justificacion_md": "Buscamos dos entradas distintas con la misma salida.",
               "es_resultado": False},
              {"accion_md": (
                  "$f(0) = f(1) = 1$ pero $0 \\neq 1$.\n\n"
                  "$\\boxed{f \\text{ no es inyectiva}}$ (contraejemplo $x_1 = 0, x_2 = 1$)."
               ),
               "justificacion_md": "**Para refutar inyectividad basta UN contraejemplo concreto.**",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Función sobreyectiva",
          body_md=(
              "$f: A \\to B$ es **sobreyectiva** si $\\text{Rec}(f) = B$, es decir, **todo elemento del "
              "codominio tiene al menos una preimagen**:\n\n"
              "$$(\\forall y \\in B)(\\exists x \\in A)(f(x) = y).$$\n\n"
              "**Estrategia para demostrar sobreyectividad:** tomar $y \\in B$ arbitrario, plantear "
              "$f(x) = y$, despejar $x$ en función de $y$, y verificar que la solución obtenida pertenece "
              "efectivamente al dominio $A$."
          )),

        b("definicion",
          titulo="Independencia de inyectividad y sobreyectividad",
          body_md=(
              "Las dos propiedades son **independientes**: una función puede ser inyectiva sin ser "
              "sobreyectiva, sobreyectiva sin ser inyectiva, ambas, o ninguna.\n\n"
              "**Cómo \"forzar\" cada propiedad:**\n\n"
              "- Para tornar inyectiva una $f$ que no lo es: **restringir el dominio** a un subconjunto adecuado.\n"
              "- Para tornar sobreyectiva una $f$: **cambiar el codominio** al recorrido. $f: A \\to \\text{Rec}(f)$ es sobreyectiva por construcción."
          )),

        b("definicion",
          titulo="Función biyectiva",
          body_md=(
              "$f$ es **biyectiva** si es **simultáneamente** inyectiva y sobreyectiva. Equivalentemente:\n\n"
              "$$(\\forall y \\in B)(\\exists! x \\in A)(f(x) = y).$$\n\n"
              "**Cada elemento del codominio tiene exactamente una preimagen.** La biyectividad combina "
              "lo mejor de ambas propiedades: la inyectividad garantiza unicidad y la sobreyectividad "
              "garantiza existencia.\n\n"
              "**Importancia:** las funciones biyectivas son **exactamente** aquellas que admiten función "
              "inversa (próxima lección)."
          )),

        b("ejemplo_resuelto",
          titulo="Probar biyectividad",
          problema_md=(
              "Pruebe que $f: (-\\infty, 1] \\to (-\\infty, 2]$, $f(x) = -x^2 + 4x - 1$, es biyectiva."
          ),
          pasos=[
              {"accion_md": (
                  "**Inyectividad.** Sean $x_1, x_2 \\leq 1$ con $f(x_1) = f(x_2)$. Operando: "
                  "$-x_1^2 + 4x_1 = -x_2^2 + 4x_2 \\iff (x_2 - x_1)(x_2 + x_1 - 4) = 0$.\n\n"
                  "Caso $x_1 = x_2$: ✓.\n"
                  "Caso $x_1 + x_2 = 4$: como ambos $\\leq 1$, $x_1 + x_2 \\leq 2 < 4$. **Imposible**."
               ),
               "justificacion_md": "Solo queda $x_1 = x_2$, luego inyectiva.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sobreyectividad.** Dado $y \\leq 2$, buscamos $x \\leq 1$ con $-x^2 + 4x - 1 = y$.\n\n"
                  "$x^2 - 4x + (1 + y) = 0 \\Rightarrow x = 2 \\pm \\sqrt{3 - y}.$\n\n"
                  "Como $y \\leq 2$, $3 - y \\geq 1 \\geq 0$, raíz definida. Tomamos $x = 2 - \\sqrt{3 - y}$ "
                  "(la otra rama da $x \\geq 2$).\n\n"
                  "Verificación de $x \\leq 1$: $2 - \\sqrt{3 - y} \\leq 1 \\iff \\sqrt{3 - y} \\geq 1 \\iff 3 - y \\geq 1 \\iff y \\leq 2$ ✓."
               ),
               "justificacion_md": "La preimagen pertenece al dominio para todo $y \\leq 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\boxed{f \\text{ es biyectiva.}}$"
               ),
               "justificacion_md": "Inyectiva + sobreyectiva = biyectiva.",
               "es_resultado": True},
          ]),

        ej(
            "Refutar biyectividad",
            "¿Es $f: \\mathbb{R} \\to \\mathbb{R}$, $f(x) = -\\sqrt{x^2 + 4}$, biyectiva?",
            [
                "Verificá inyectividad evaluando en $x = -1$ y $x = 1$.",
                "Verificá sobreyectividad calculando el recorrido.",
            ],
            (
                "**Inyectividad:** $f(-1) = -\\sqrt{5} = f(1)$, y $-1 \\neq 1$. **No es inyectiva.**\n\n"
                "**Sobreyectividad:** $x^2 + 4 \\geq 4$, luego $\\sqrt{x^2+4} \\geq 2$, así $f(x) \\leq -2$. "
                "$\\text{Rec}(f) = (-\\infty, -2]$, no $\\mathbb{R}$. **No es sobreyectiva.**\n\n"
                "$\\boxed{f \\text{ no es biyectiva.}}$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica inyectividad, sobreyectividad y biyectividad:",
          preguntas=[
              {"enunciado_md": "¿$f: \\mathbb{R} \\to \\mathbb{R}$, $f(x) = x^2$ es inyectiva?",
               "opciones_md": [
                   "Sí, porque es función",
                   "No, porque $f(2) = f(-2) = 4$",
                   "Sí, porque es continua",
                   "Solo si $x \\geq 0$",
               ],
               "correcta": "B",
               "pista_md": "Buscá dos puntos distintos con misma imagen.",
               "explicacion_md": "$f(2) = f(-2) = 4$ pero $2 \\neq -2$, así que falla la inyectividad. NOTA: si se restringe a $[0, +\\infty)$ sí es inyectiva."},
              {"enunciado_md": "¿$f: \\mathbb{R} \\to \\mathbb{R}$, $f(x) = x^3$ es sobreyectiva?",
               "opciones_md": [
                   "No, no alcanza valores negativos",
                   "Sí, todo real $y$ tiene preimagen $\\sqrt[3]{y}$",
                   "Solo en $[0, +\\infty)$",
                   "No, solo es inyectiva",
               ],
               "correcta": "B",
               "pista_md": "Toda raíz cúbica está bien definida en $\\mathbb{R}$.",
               "explicacion_md": "Para todo $y \\in \\mathbb{R}$ existe $x = \\sqrt[3]{y}$ tal que $x^3 = y$. La función $x^3$ es biyectiva en $\\mathbb{R}$."},
              {"enunciado_md": "Una función $f: A \\to B$ es biyectiva si y solo si:",
               "opciones_md": [
                   "Es inyectiva",
                   "Es sobreyectiva",
                   "Es inyectiva Y sobreyectiva",
                   "Tiene gráfica continua",
               ],
               "correcta": "C",
               "pista_md": "Biyección = uno-a-uno + cubre todo $B$.",
               "explicacion_md": "Biyectiva $\\iff$ inyectiva (uno-a-uno) AND sobreyectiva (alcanza todo el codominio). Las dos propiedades son INDEPENDIENTES."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Olvidar que la inyectividad depende del dominio:** $f(x) = x^2$ no es inyectiva en $\\mathbb{R}$, pero **sí** en $[0, +\\infty)$.",
              "**Olvidar que la sobreyectividad depende del codominio:** misma regla, distinto codominio = distinto resultado.",
              "**Confundir inyectividad con sobreyectividad:** son INDEPENDIENTES.",
              "**Para refutar inyectividad, intentar demostrar:** basta UN contraejemplo concreto $x_1 \\neq x_2$ con $f(x_1) = f(x_2)$.",
              "**Demostrar sobreyectividad sin verificar que la preimagen pertenece al dominio:** la solución algebraica puede dar valores fuera de $A$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Inyectiva:** $f(x_1) = f(x_2) \\Rightarrow x_1 = x_2$. Test recta horizontal.",
              "**Sobreyectiva:** $\\text{Rec}(f) = B$. Toda $y \\in B$ tiene preimagen.",
              "**Biyectiva:** ambas. Existe **única** preimagen para cada $y$.",
              "**Independencia:** inyectividad y sobreyectividad son propiedades independientes.",
              "**Para refutar:** un solo contraejemplo basta. **Para demostrar:** argumento general.",
              "**Próxima lección:** álgebra de funciones (suma, producto, composición).",
          ]),
    ]
    return {
        "id": "lec-ic-3-5-funciones-biyectivas",
        "title": "Funciones biyectivas",
        "description": "Definiciones formales de inyectividad, sobreyectividad y biyectividad. Test de la recta horizontal y técnicas de demostración / refutación.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 5,
    }


# =====================================================================
# 3.6 Álgebra de funciones
# =====================================================================
def lesson_3_6():
    blocks = [
        b("texto", body_md=(
            "El **álgebra de funciones** y la **composición** son herramientas esenciales del cálculo. "
            "Permiten construir nuevas funciones combinando funciones conocidas mediante operaciones "
            "aritméticas (suma, resta, producto, cociente) o por composición — aplicar una función "
            "sobre el resultado de otra. Comprender los **dominios resultantes** es fundamental para "
            "el análisis riguroso.\n\n"
            "**Objetivos:**\n\n"
            "- Definir el álgebra de funciones y calcular dominios.\n"
            "- Comprender la **función compuesta** y su dominio.\n"
            "- Aplicar a funciones definidas por tramos.\n"
            "- Conocer cómo se preservan inyectividad y sobreyectividad bajo composición."
        )),

        b("definicion",
          titulo="Operaciones aritméticas con funciones",
          body_md=(
              "Sean $f: A \\to C$ y $g: B \\to D$. Se definen:\n\n"
              "1. $(f + g)(x) = f(x) + g(x)$ con dominio $A \\cap B$.\n"
              "2. $(f - g)(x) = f(x) - g(x)$ con dominio $A \\cap B$.\n"
              "3. $(f \\cdot g)(x) = f(x) \\cdot g(x)$ con dominio $A \\cap B$.\n"
              "4. $\\left(\\dfrac{f}{g}\\right)(x) = \\dfrac{f(x)}{g(x)}$ con dominio $\\{x \\in A \\cap B \\mid g(x) \\neq 0\\}$.\n\n"
              "**Las tres primeras** tienen dominio $A \\cap B$. **El cociente** además excluye los ceros de $g$."
          )),

        b("ejemplo_resuelto",
          titulo="Cálculo del cociente con dominios",
          problema_md=(
              "Sean $f(x) = \\dfrac{x + 1}{\\sqrt{x + 2}}$ y $g(x) = \\dfrac{x^2 - 1}{x^2 - x - 6}$. "
              "Determine $\\text{Dom}\\left(\\dfrac{f}{g}\\right)$."
          ),
          pasos=[
              {"accion_md": (
                  "**Dominios individuales:**\n"
                  "- $f$: $x + 2 > 0 \\iff x > -2$. $\\text{Dom}(f) = (-2, +\\infty)$.\n"
                  "- $g$: denominador $x^2 - x - 6 = (x - 3)(x + 2) \\neq 0$. $\\text{Dom}(g) = \\mathbb{R} \\setminus \\{-2, 3\\}$."
               ),
               "justificacion_md": "Restricciones individuales.",
               "es_resultado": False},
              {"accion_md": (
                  "**Intersección** $\\text{Dom}(f) \\cap \\text{Dom}(g) = (-2, +\\infty) \\setminus \\{3\\}$ "
                  "(el $-2$ ya está excluido por $f$).\n\n"
                  "**Ceros de $g$:** $x^2 - 1 = (x - 1)(x + 1) = 0 \\iff x = \\pm 1$. Excluimos también $\\{-1, 1\\}$."
               ),
               "justificacion_md": "Para el cociente, excluimos donde $g$ se anula.",
               "es_resultado": False},
              {"accion_md": (
                  "$$\\boxed{\\text{Dom}\\left(\\dfrac{f}{g}\\right) = (-2, +\\infty) \\setminus \\{-1, 1, 3\\}.}$$"
               ),
               "justificacion_md": "Conjunto final.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Función compuesta",
          body_md=(
              "Sean $f: A \\to C$ y $g: B \\to D$. La **función compuesta** $g \\circ f$ se define por\n\n"
              "$$(g \\circ f)(x) = g(f(x)).$$\n\n"
              "Aplicar primero $f$ y luego $g$ sobre el resultado.\n\n"
              "**Dominio de la composición:**\n\n"
              "$$\\text{Dom}(g \\circ f) = \\{ x \\in \\text{Dom}(f) \\mid f(x) \\in \\text{Dom}(g) \\}.$$\n\n"
              "Es decir, $x$ pertenece al dominio de $g \\circ f$ si: (i) $x$ pertenece al dominio de $f$, **y** "
              "(ii) el valor $f(x)$ cae dentro del dominio de $g$."
          )),

        b("ejemplo_resuelto",
          titulo="Composición con dominios",
          problema_md=(
              "Sean $f: (-\\infty, 5) \\to \\mathbb{R}$, $f(x) = \\sqrt{x^2 + 4}$, y "
              "$g: [6, +\\infty) \\to \\mathbb{R}$, $g(x) = 2x + 3$. Defina $g \\circ f$."
          ),
          pasos=[
              {"accion_md": (
                  "$x \\in \\text{Dom}(g \\circ f) \\iff x < 5 \\;\\land\\; \\sqrt{x^2 + 4} \\geq 6$.\n\n"
                  "Resolvemos $\\sqrt{x^2+4} \\geq 6 \\iff x^2 + 4 \\geq 36 \\iff x^2 \\geq 32 \\iff |x| \\geq \\sqrt{32}$."
               ),
               "justificacion_md": "Condición sobre $f(x)$ para que entre al dominio de $g$.",
               "es_resultado": False},
              {"accion_md": (
                  "Intersectando con $x < 5$: como $\\sqrt{32} \\approx 5{,}66 > 5$, la rama $x \\geq \\sqrt{32}$ "
                  "es **incompatible** con $x < 5$. Solo queda $x \\leq -\\sqrt{32}$.\n\n"
                  "$\\text{Dom}(g \\circ f) = (-\\infty, -\\sqrt{32}]$."
               ),
               "justificacion_md": "Compatibilidad del rango con el dominio de $g$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Regla:** $(g \\circ f)(x) = g(f(x)) = 2\\sqrt{x^2 + 4} + 3$.\n\n"
                  "$$\\boxed{(g \\circ f): (-\\infty, -\\sqrt{32}] \\to \\mathbb{R}, \\quad (g \\circ f)(x) = 2\\sqrt{x^2 + 4} + 3.}$$"
               ),
               "justificacion_md": "Composición completa.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Composición con función por tramos",
          problema_md=(
              "Sean $g(x) = -3x + 1$ y $f(x) = \\begin{cases} x^2 + 5 & \\text{si } x < -1 \\\\ 1 - x & \\text{si } x \\geq -1 \\end{cases}$. Halle $f \\circ g$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\text{Dom}(f \\circ g) = \\{x \\in \\mathbb{R} : g(x) \\in \\text{Dom}(f) = \\mathbb{R}\\} = \\mathbb{R}$.\n\n"
                  "Para calcular la regla, evaluamos $f$ en $g(x) = -3x + 1$, **distinguiendo según el tramo** en que cae:"
               ),
               "justificacion_md": "Hay que ver si $g(x) < -1$ o $g(x) \\geq -1$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 1: $-3x + 1 < -1 \\iff x > \\dfrac{2}{3}$.** Aquí $f(g(x)) = (-3x+1)^2 + 5 = 9x^2 - 6x + 6$.\n\n"
                  "**Caso 2: $-3x + 1 \\geq -1 \\iff x \\leq \\dfrac{2}{3}$.** Aquí $f(g(x)) = 1 - (-3x + 1) = 3x$."
               ),
               "justificacion_md": "Distinguimos dos casos.",
               "es_resultado": False},
              {"accion_md": (
                  "$$\\boxed{(f \\circ g)(x) = \\begin{cases} 9x^2 - 6x + 6 & \\text{si } x > \\dfrac{2}{3} \\\\ 3x & \\text{si } x \\leq \\dfrac{2}{3} \\end{cases}}$$"
               ),
               "justificacion_md": "Resultado.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Composición preserva inyectividad y sobreyectividad.** Sean $f: A \\to C$ y $g: B \\to D$ "
              "con $g \\circ f$ bien definida.\n\n"
              "1. Si $f$ y $g$ son **inyectivas**, entonces $g \\circ f$ es inyectiva.\n"
              "2. Si $f$ y $g$ son **sobreyectivas**, entonces $g \\circ f$ es sobreyectiva.\n\n"
              "En particular, **la composición de dos biyecciones es una biyección**.\n\n"
              "**Demostración (1):** Sean $x_1, x_2$ con $g(f(x_1)) = g(f(x_2))$. Por inyectividad de $g$, "
              "$f(x_1) = f(x_2)$. Por inyectividad de $f$, $x_1 = x_2$. $\\square$"
          )),

        b("intuicion", body_md=(
            "**La composición no es conmutativa.** En general $f \\circ g \\neq g \\circ f$. Esto es "
            "**fundamental** y diferencia la composición de las operaciones aritméticas. Verifíquelo "
            "siempre con un ejemplo concreto: con $f(x) = x^2$ y $g(x) = x + 1$:\n\n"
            "$(f \\circ g)(x) = (x+1)^2 = x^2 + 2x + 1$\n\n"
            "$(g \\circ f)(x) = x^2 + 1$\n\n"
            "Distintas funciones."
        )),

        ej(
            "Composición y dominio",
            "Sean $f(x) = \\sqrt{x - 2}$ y $g(x) = x^2 + 1$. Halle $f \\circ g$ y $g \\circ f$ con sus dominios.",
            [
                "$\\text{Dom}(f) = [2, +\\infty)$, $\\text{Dom}(g) = \\mathbb{R}$.",
                "Para $f \\circ g$: $g(x) \\in \\text{Dom}(f)$, es decir $x^2 + 1 \\geq 2$.",
                "Para $g \\circ f$: $f(x) \\in \\text{Dom}(g) = \\mathbb{R}$, sin restricción extra.",
            ],
            (
                "**$f \\circ g$:** $x^2 + 1 \\geq 2 \\iff x^2 \\geq 1 \\iff |x| \\geq 1$. $\\text{Dom}(f \\circ g) = (-\\infty, -1] \\cup [1, +\\infty)$. Regla: $(f \\circ g)(x) = \\sqrt{x^2 - 1}$.\n\n"
                "**$g \\circ f$:** $\\text{Dom}(g \\circ f) = \\text{Dom}(f) = [2, +\\infty)$. Regla: $(g \\circ f)(x) = x - 2 + 1 = x - 1$."
            ),
        ),

        fig(
            "Diagrama del álgebra y composición de funciones. Lado izquierdo: dos cajas teal #06b6d4 "
            "rotuladas 'f' y 'g' con sus dominios solapados, indicando 'suma (f+g)(x) = f(x)+g(x)' y "
            "'producto (fg)(x) = f(x)g(x)' con el dominio común sombreado en ámbar #f59e0b. "
            "Lado derecho: cadena de composición g circ f mostrada como 'x -> f -> f(x) -> g -> g(f(x))' "
            "con flechas y dos cajas conectadas. Etiquetas: dominio inicial de f, condición f(x) en "
            "Dom(g), salida final. Tipografía clara, fondo blanco. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica el álgebra de funciones:",
          preguntas=[
              {"enunciado_md": "¿$f \\circ g = g \\circ f$ siempre?",
               "opciones_md": [
                   "Sí, la composición es conmutativa",
                   "No, en general $f \\circ g \\neq g \\circ f$",
                   "Sí, cuando $f$ y $g$ son polinomios",
                   "No, salvo si una es constante",
               ],
               "correcta": "B",
               "pista_md": "Probá con $f(x) = x + 1$ y $g(x) = x^2$.",
               "explicacion_md": "$f(g(x)) = x^2 + 1$, $g(f(x)) = (x + 1)^2 = x^2 + 2x + 1$. Distintas: la composición NO es conmutativa."},
              {"enunciado_md": "Si $f(x) = \\sqrt{x}$ y $g(x) = x - 4$, ¿cuál es el dominio de $f \\circ g$?",
               "opciones_md": ["$\\mathbb{R}$", "$x \\geq 0$", "$x \\geq 4$", "$x \\neq 4$"],
               "correcta": "C",
               "pista_md": "Necesitás $g(x) \\in \\text{Dom}(f) = [0, +\\infty)$.",
               "explicacion_md": "$(f \\circ g)(x) = \\sqrt{x - 4}$, exige $x - 4 \\geq 0$, es decir $x \\geq 4$. Hay que mirar el dominio del compuesto, no solo el de $g$."},
              {"enunciado_md": "Si $\\text{Dom}(f) = [0, 5]$ y $\\text{Dom}(g) = [-2, 3]$, ¿cuál es el dominio de $(f + g)$?",
               "opciones_md": [
                   "$[-2, 5]$ (unión)",
                   "$[0, 3]$ (intersección)",
                   "$[0, 5]$ (de $f$)",
                   "$\\mathbb{R}$",
               ],
               "correcta": "B",
               "pista_md": "Para sumar valores, ambas funciones tienen que estar definidas.",
               "explicacion_md": "$\\text{Dom}(f + g) = \\text{Dom}(f) \\cap \\text{Dom}(g) = [0, 3]$. La intersección es lo común."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Asumir que $f \\circ g = g \\circ f$:** la composición NO es conmutativa.",
              "**Olvidar la condición $f(x) \\in \\text{Dom}(g)$** al calcular $\\text{Dom}(g \\circ f)$.",
              "**Calcular $f \\circ g$ tomando $\\text{Dom}(g)$ entero:** hay que verificar que $g(x)$ cae en $\\text{Dom}(f)$.",
              "**Aplicar la regla de la función exterior sin distinguir tramos** cuando la función interior cae en distintos tramos de la exterior.",
              "**Olvidar excluir ceros de $g$ en el cociente $f/g$.**",
          ]),

        b("resumen",
          puntos_md=[
              "**Operaciones aritméticas:** suma, resta, producto con dominio $A \\cap B$; cociente excluye además ceros de $g$.",
              "**Composición:** $(g \\circ f)(x) = g(f(x))$. Dominio: $\\{x \\in \\text{Dom}(f) \\mid f(x) \\in \\text{Dom}(g)\\}$.",
              "**No conmutativa:** $f \\circ g \\neq g \\circ f$ en general.",
              "**Compuesta de inyectivas es inyectiva**, de sobreyectivas es sobreyectiva, de biyecciones es biyección.",
              "**Próxima lección:** función inversa.",
          ]),
    ]
    return {
        "id": "lec-ic-3-6-algebra-funciones",
        "title": "Álgebra de funciones",
        "description": "Operaciones aritméticas con funciones, función compuesta, dominios y preservación de inyectividad / sobreyectividad bajo composición.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


# =====================================================================
# 3.7 Función inversa
# =====================================================================
def lesson_3_7():
    blocks = [
        b("texto", body_md=(
            "La **función inversa** surge naturalmente cuando preguntamos: ¿es posible \"deshacer\" la "
            "acción de una función? Es decir, recuperar el valor original $x$ a partir de $f(x)$. Esta "
            "operación no siempre es posible: solo las **funciones biyectivas** admiten una inversa "
            "bien definida.\n\n"
            "**Objetivos:**\n\n"
            "- Definir formalmente función inversa y su relación con biyectividad.\n"
            "- Aplicar **propiedades de cancelación** para verificar inversas.\n"
            "- Ejecutar el **algoritmo algebraico** para hallarla.\n"
            "- Interpretar geométricamente la inversa como reflexión respecto a $y = x$."
        )),

        b("definicion",
          titulo="Función inversa",
          body_md=(
              "Sea $f: A \\to B$ una función **biyectiva**. La **función inversa** de $f$, denotada "
              "$f^{-1}: B \\to A$, se define por:\n\n"
              "$$f^{-1}(y) = x \\iff y = f(x).$$\n\n"
              "$f^{-1}$ asigna a cada $y \\in B$ el **único** $x \\in A$ tal que $f(x) = y$. La existencia "
              "y unicidad de ese $x$ están garantizadas precisamente por la **biyectividad** de $f$ — "
              "la sobreyectividad asegura existencia y la inyectividad asegura unicidad.\n\n"
              "**¡Cuidado!** $f^{-1}$ denota la **función inversa**; **no** debe confundirse con el "
              "**recíproco** $\\dfrac{1}{f(x)}$. Son objetos completamente distintos."
          )),

        b("teorema",
          enunciado_md=(
              "**Propiedades de cancelación.** Si $f: A \\to B$ es biyectiva con inversa $f^{-1}: B \\to A$, entonces:\n\n"
              "$$f^{-1}(f(x)) = x \\quad \\text{para todo } x \\in A,$$\n\n"
              "$$f(f^{-1}(y)) = y \\quad \\text{para todo } y \\in B.$$\n\n"
              "**Recíprocamente:** cualquier función $g: B \\to A$ que satisfaga ambas condiciones es la inversa de $f$.\n\n"
              "Estas propiedades dicen que $f$ y $f^{-1}$ se **cancelan** mutuamente cuando se componen "
              "en cualquier orden. Son la **herramienta fundamental** para verificar que dos funciones "
              "son inversas entre sí, sin recurrir a la definición."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar que dos funciones son inversas",
          problema_md=(
              "Demuestre que $f(x) = x^3$ y $g(x) = x^{1/3}$ son inversas entre sí."
          ),
          pasos=[
              {"accion_md": (
                  "Ambas tienen dominio y recorrido $\\mathbb{R}$. Verificamos las propiedades:\n\n"
                  "$g(f(x)) = g(x^3) = (x^3)^{1/3} = x^{3 \\cdot \\frac{1}{3}} = x$ ✓\n\n"
                  "$f(g(x)) = f(x^{1/3}) = (x^{1/3})^3 = x^{\\frac{1}{3} \\cdot 3} = x$ ✓"
               ),
               "justificacion_md": "Aplicación directa de las propiedades de cancelación.",
               "es_resultado": False},
              {"accion_md": (
                  "Por la proposición, $\\boxed{g = f^{-1}}$."
               ),
               "justificacion_md": "Las propiedades caracterizan la inversa.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Algoritmo para hallar $f^{-1}$",
          body_md=(
              "Si $f: A \\to B$ es biyectiva, su inversa se calcula mediante el siguiente algoritmo:\n\n"
              "**Paso 1.** Escribir $y = f(x)$.\n\n"
              "**Paso 2.** Despejar $x$ en términos de $y$.\n\n"
              "**Paso 3.** Intercambiar $x$ e $y$. La ecuación resultante es $y = f^{-1}(x)$.\n\n"
              "**Importante:** $\\text{Dom}(f^{-1}) = B = \\text{Rec}(f)$ y $\\text{Rec}(f^{-1}) = A = \\text{Dom}(f)$."
          )),

        b("ejemplo_resuelto",
          titulo="Inversa de una función racional",
          problema_md=(
              "Halle la inversa de $f(x) = \\dfrac{2x + 1}{x - 1}$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\text{Dom}(f) = \\mathbb{R} \\setminus \\{1\\}$. **Paso 1:** $y = \\dfrac{2x + 1}{x - 1}$."
               ),
               "justificacion_md": "Setup.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2:** Despejamos $x$.\n\n"
                  "$y(x - 1) = 2x + 1 \\iff xy - y = 2x + 1 \\iff x(y - 2) = y + 1 \\iff x = \\dfrac{y + 1}{y - 2}$ (válido si $y \\neq 2$)."
               ),
               "justificacion_md": "Algebra estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3:** Intercambiamos $x$ e $y$.\n\n"
                  "$\\boxed{f^{-1}(x) = \\dfrac{x + 1}{x - 2}, \\quad x \\neq 2.}$"
               ),
               "justificacion_md": "Notar la \"simetría\": $f$ y $f^{-1}$ tienen la misma estructura "
                                   "(función de Möbius).",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Gráfica de la función inversa.** La gráfica de $f^{-1}$ se obtiene **reflejando la "
              "gráfica de $f$ respecto a la recta $y = x$**.\n\n"
              "**Razón:** $b = f(a) \\iff a = f^{-1}(b)$. Si $(a, b) \\in G(f)$, entonces $(b, a) \\in G(f^{-1})$. "
              "El intercambio de coordenadas equivale geométricamente a reflexión respecto a $y = x$.\n\n"
              "**Consecuencia (test recta horizontal):** una función tiene inversa $\\iff$ ninguna recta "
              "horizontal corta su gráfica más de una vez (i.e., es inyectiva)."
          )),

        fig(
            "Plano cartesiano con dos curvas reflejadas en la recta diagonal y=x (línea punteada "
            "gris a 45°). Curva 1: f(x) = x³ en color teal #06b6d4, pasando por (0,0), (1,1), "
            "(2,8). Curva 2: f⁻¹(x) = ∛x en color ámbar #f59e0b, pasando por (0,0), (1,1), (8,2). "
            "Tres pares de puntos correspondientes marcados con flechas curvas que muestran la "
            "reflexión: (1,1) en y=x es punto fijo; (2,8) en f corresponde a (8,2) en f⁻¹; "
            "(-1,-1) similar. Líneas punteadas conectando cada par a través de la recta y=x. "
            "Etiquetas claras 'f', 'f⁻¹' y 'y = x'. Título: 'La inversa es reflejo respecto a y=x'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Inversa con restricción de dominio",
          problema_md=(
              "Halle la inversa de $f: [4, +\\infty) \\to [0, +\\infty)$, $f(x) = \\sqrt{x - 4}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1-2:** $y = \\sqrt{x - 4}$ con $y \\geq 0$. Elevando al cuadrado: $y^2 = x - 4 \\iff x = y^2 + 4$."
               ),
               "justificacion_md": "Despeje válido porque $y \\geq 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3:** $\\boxed{f^{-1}(x) = x^2 + 4, \\quad x \\geq 0.}$"
               ),
               "justificacion_md": "Sin la restricción $x \\geq 0$, $x^2 + 4$ no sería inyectiva.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inversa de función por tramos",
          problema_md=(
              "Halle la inversa de $f(x) = \\begin{cases} -3x^2 + 1 & \\text{si } x < 0 \\\\ 3x + 2 & \\text{si } x \\geq 0 \\end{cases}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Recorrido por tramos:**\n"
                  "- Tramo 1 ($x < 0$): $-3x^2 + 1 < 1$ (estricto). $\\text{Rec}_1 = (-\\infty, 1)$.\n"
                  "- Tramo 2 ($x \\geq 0$): $3x + 2 \\geq 2$. $\\text{Rec}_2 = [2, +\\infty)$.\n\n"
                  "Recorridos disjuntos $\\Rightarrow$ inyectiva globalmente."
               ),
               "justificacion_md": "Disjunción de los recorridos garantiza inyectividad global.",
               "es_resultado": False},
              {"accion_md": (
                  "**Inversa de tramo 1** ($y < 1$, $x < 0$): $y = -3x^2 + 1 \\Rightarrow x^2 = \\dfrac{1-y}{3} \\Rightarrow x = -\\sqrt{\\dfrac{1-y}{3}}$ (negativa).\n\n"
                  "**Inversa de tramo 2** ($y \\geq 2$, $x \\geq 0$): $y = 3x + 2 \\Rightarrow x = \\dfrac{y - 2}{3}$."
               ),
               "justificacion_md": "Inversa tramo a tramo.",
               "es_resultado": False},
              {"accion_md": (
                  "$$\\boxed{f^{-1}(x) = \\begin{cases} -\\sqrt{\\dfrac{1-x}{3}} & \\text{si } x < 1 \\\\ \\dfrac{x-2}{3} & \\text{si } x \\geq 2 \\end{cases}}$$"
               ),
               "justificacion_md": "Por tramos.",
               "es_resultado": True},
          ]),

        ej(
            "Inversa con restricción",
            "Sea $f: [0, +\\infty) \\to [4, +\\infty)$, $f(x) = x^2 + 4$. Halle $f^{-1}$.",
            [
                "Verificá que $f$ es biyectiva (inyectiva por restricción de dominio, sobreyectiva por imagen).",
                "Despejá $x$ usando que $x \\geq 0$.",
            ],
            (
                "$y = x^2 + 4 \\iff x^2 = y - 4 \\iff x = \\sqrt{y - 4}$ (positiva, pues $x \\geq 0$).\n\n"
                "Intercambiando: $\\boxed{f^{-1}(x) = \\sqrt{x - 4}, \\quad x \\geq 4.}$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica el concepto de función inversa:",
          preguntas=[
              {"enunciado_md": "¿$f^{-1}(x)$ es lo mismo que $\\dfrac{1}{f(x)}$?",
               "opciones_md": [
                   "Sí, son notaciones equivalentes",
                   "No, $f^{-1}$ es la inversa funcional, $1/f$ es el recíproco",
                   "Sí, si $f$ es lineal",
                   "Sí, si $f$ es polinomio",
               ],
               "correcta": "B",
               "pista_md": "$f^{-1}$ deshace lo que hace $f$.",
               "explicacion_md": "$f^{-1}(y)$ devuelve la $x$ tal que $f(x) = y$. $1/f(x)$ es solo el recíproco. Son objetos completamente distintos."},
              {"enunciado_md": "Si $f: \\mathbb{R} \\to [0, +\\infty)$, $f(x) = x^2$, ¿tiene inversa?",
               "opciones_md": [
                   "Sí, $f^{-1}(y) = \\sqrt{y}$",
                   "No, porque $f$ no es inyectiva en $\\mathbb{R}$",
                   "Sí, $f^{-1}(y) = -\\sqrt{y}$",
                   "Sí, en todo $\\mathbb{R}$",
               ],
               "correcta": "B",
               "pista_md": "Solo las funciones biyectivas tienen inversa.",
               "explicacion_md": "$f$ no es inyectiva ($f(2) = f(-2) = 4$), por lo que no tiene inversa global. Habría que restringir el dominio a $[0, +\\infty)$ primero."},
              {"enunciado_md": "Si $f$ es biyectiva con $\\text{Dom}(f) = [0, 4]$ y $\\text{Rec}(f) = [-1, 5]$, ¿cuál es $\\text{Dom}(f^{-1})$?",
               "opciones_md": ["$[0, 4]$", "$[-1, 5]$", "$\\mathbb{R}$", "$[0, 5]$"],
               "correcta": "B",
               "pista_md": "$\\text{Dom}(f^{-1}) = \\text{Rec}(f)$.",
               "explicacion_md": "El dominio de $f^{-1}$ son los valores que ALCANZA $f$, es decir su recorrido. $\\text{Dom}(f^{-1}) = [-1, 5]$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir $f^{-1}$ con $\\dfrac{1}{f}$:** son objetos completamente distintos.",
              "**Hallar inversa de función NO biyectiva:** primero hay que demostrar biyectividad (o restringir dominio).",
              "**Olvidar el dominio de la inversa:** $\\text{Dom}(f^{-1}) = \\text{Rec}(f)$, no $\\mathbb{R}$.",
              "**Tomar la rama incorrecta al despejar raíces:** si $x \\geq 0$ tomá la raíz positiva; si $x \\leq 0$ tomá la negativa.",
              "**Pensar que $f \\circ f^{-1} = x$ siempre:** sí, pero verificá que la composición esté bien definida (dominios compatibles).",
          ]),

        b("resumen",
          puntos_md=[
              "**Existencia de $f^{-1}$:** equivalente a la **biyectividad** de $f$.",
              "**Definición:** $f^{-1}(y) = x \\iff y = f(x)$.",
              "**Propiedades de cancelación:** $f^{-1}(f(x)) = x$ y $f(f^{-1}(y)) = y$.",
              "**Algoritmo:** escribir $y = f(x)$, despejar $x$, intercambiar variables.",
              "**Gráfica:** reflexión respecto a $y = x$.",
              "**Dominios y recorridos se intercambian:** $\\text{Dom}(f^{-1}) = \\text{Rec}(f)$.",
              "**Cierre del capítulo:** este capítulo sienta las bases para sucesiones (cap. 4) y exponenciales/logaritmos (cap. 5).",
          ]),
    ]
    return {
        "id": "lec-ic-3-7-funcion-inversa",
        "title": "Función inversa",
        "description": "Existencia y unicidad ligadas a biyectividad, propiedades de cancelación, algoritmo para hallarla y gráfica como reflexión respecto a y=x.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 7,
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

    chapter_id = "ch-ic-funciones-reales"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Funciones Reales",
        "description": (
            "Funciones reales, gráficas, transformaciones, funciones racionales, biyectividad, álgebra "
            "de funciones y función inversa."
        ),
        "order": 3,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_3_1, lesson_3_2, lesson_3_3, lesson_3_4, lesson_3_5, lesson_3_6, lesson_3_7]
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
    print(f"✅ Capítulo 3 — Funciones Reales listo: {len(builders)} lecciones, {total_blocks} bloques, "
          f"{total_figs} figuras pendientes.")
    print()
    print("URLs locales:")
    print(f"  http://localhost:3007/courses/{course_id}")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
