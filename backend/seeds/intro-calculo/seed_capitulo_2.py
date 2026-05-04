"""
Seed del curso Introducción al Cálculo — Capítulo 2: Desigualdades.
6 lecciones:
  2.1 Axiomas de Orden
  2.2 Valor Absoluto
  2.3 Intervalos e Inecuaciones
  2.4 Inecuaciones Racionales
  2.5 Inecuaciones con Valor Absoluto
  2.6 Inecuaciones con Raíces

ENFOQUE: estructura formal (cuerpo ordenado) + métodos algorítmicos sistemáticos
para resolver inecuaciones. Énfasis en el dominio antes de operar (raíces, fracciones)
y en la regla de signos (especialmente al multiplicar/dividir por negativos).

NOTA TÉCNICA: NO usar `\\begin{array}` en LaTeX block math — el `|` dentro de
`{c|cccc}` rompe el render por interferencia de remark-gfm. Para tablas (signos,
casos de 2do grado, etc.) usar tablas markdown nativas.

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
# 2.1 Axiomas de Orden
# =====================================================================
def lesson_2_1():
    blocks = [
        b("texto", body_md=(
            "Los **axiomas de orden** son la base formal que nos permite comparar números reales y "
            "establecer cuándo uno es mayor o menor que otro. Más allá de la intuición visual de "
            "\"derecha en la recta\", esa estructura puede axiomatizarse en un puñado de reglas a "
            "partir de las cuales se deduce **toda** la teoría de desigualdades.\n\n"
            "**Objetivos:**\n\n"
            "- Comprender los **cuatro axiomas de orden** de los números reales.\n"
            "- Conocer el conjunto $\\mathbb{R}^+$ y su **cerradura** bajo suma y producto.\n"
            "- Aplicar los axiomas para **demostrar desigualdades** y teoremas elementales.\n"
            "- Practicar técnicas de demostración: por casos, por contradicción y construcción directa."
        )),

        b("definicion",
          titulo="Los cuatro axiomas de orden",
          body_md=(
              "El sistema de números reales $\\mathbb{R}$ es un **cuerpo ordenado**: satisface los "
              "siguientes axiomas, donde $a < b$ es una declaración que es verdadera o falsa.\n\n"
              "- **O1 — Tricotomía:** para todo $a, b \\in \\mathbb{R}$ se cumple **una y solo una** "
              "de las tres condiciones: $a = b$, $\\;a < b$, $\\;b < a$.\n"
              "- **O2 — Transitividad:** si $a < b$ y $b < c$, entonces $a < c$.\n"
              "- **O3 — Suma:** si $a < b$, entonces $a + c < b + c$ para todo $c \\in \\mathbb{R}$.\n"
              "- **O4 — Producto:** si $a < b$ y $c > 0$, entonces $a \\cdot c < b \\cdot c$.\n\n"
              "A partir de estos cuatro se deducen **todas** las propiedades de orden."
          )),

        b("definicion",
          titulo="$\\mathbb{R}^+$ y su cerradura",
          body_md=(
              "$\\mathbb{R}^+ = \\{ x \\in \\mathbb{R} \\mid x > 0 \\}$ es el conjunto de los **reales "
              "positivos**. Una propiedad fundamental es que es **cerrado** bajo suma y producto:\n\n"
              "**Teorema.** Si $a, b \\in \\mathbb{R}^+$, entonces $a + b \\in \\mathbb{R}^+$ y "
              "$a \\cdot b \\in \\mathbb{R}^+$.\n\n"
              "**Demostración (suma).** Como $a > 0$, por O3 sumando $b$ a ambos lados: "
              "$a + b > 0 + b = b > 0$. Por O2, $a + b > 0$, luego $a + b \\in \\mathbb{R}^+$.\n\n"
              "**Demostración (producto).** Como $a > 0$ y $b > 0$, por O4: $a \\cdot b > 0 \\cdot b = 0$, "
              "luego $a \\cdot b \\in \\mathbb{R}^+$. $\\quad\\square$"
          )),

        b("teorema",
          enunciado_md=(
              "**Equivalencia fundamental.** Para todo $a, b \\in \\mathbb{R}$:\n\n"
              "$$a < b \\iff b - a \\in \\mathbb{R}^+.$$\n\n"
              "Esta equivalencia es muy útil porque convierte un enunciado sobre desigualdades en uno "
              "sobre **positividad**, donde podemos aprovechar la cerradura de $\\mathbb{R}^+$."
          )),

        b("definicion",
          titulo="Desigualdad no estricta $\\leq$",
          body_md=(
              "A partir de la relación estricta $<$ definimos:\n\n"
              "- $a \\leq b$ significa $a < b$ **o** $a = b$.\n"
              "- $a \\geq b$ significa $a > b$ **o** $a = b$.\n"
              "- $b \\geq a$ significa lo mismo que $a \\leq b$.\n\n"
              "**Ejemplo.** $x < 4$ es verdadera si $x = 3$, pero falsa si $x = 4$. En cambio, "
              "$x \\leq 4$ es verdadera tanto para $x = 3$ como para $x = 4$."
          )),

        b("teorema",
          enunciado_md=(
              "**Cuadrados son no negativos.** Para todo $a \\in \\mathbb{R}$ se cumple $a^2 \\geq 0$, "
              "con igualdad si y solo si $a = 0$.\n\n"
              "**Demostración por casos** (usando tricotomía O1):\n\n"
              "- **Caso $a > 0$:** como $\\mathbb{R}^+$ es cerrado bajo producto, $a \\cdot a > 0$, es "
              "decir $a^2 > 0$.\n"
              "- **Caso $a = 0$:** entonces $a^2 = 0$, luego $a^2 \\geq 0$.\n"
              "- **Caso $a < 0$:** entonces $-a > 0$ y por cerradura $(-a)(-a) > 0$, es decir $a^2 > 0$.\n\n"
              "En todos los casos $a^2 \\geq 0$. $\\quad\\square$"
          )),

        b("teorema",
          enunciado_md=(
              "**Signo del opuesto e inverso.** Para todo $a \\in \\mathbb{R}$ no nulo:\n\n"
              "1. Si $a > 0$, entonces $-a < 0$.\n"
              "2. Si $a < 0$, entonces $-a > 0$.\n"
              "3. Si $a > 0$, entonces $a^{-1} > 0$.\n"
              "4. Si $a < 0$, entonces $a^{-1} < 0$.\n\n"
              "**Demostración del inciso 3 (por contradicción).** Supongamos $a > 0$ pero $a^{-1} < 0$. "
              "Como $a^2 > 0$ (teorema anterior), por O4 con $c = a^{-1} < 0$ se invierte la desigualdad:\n\n"
              "$$a^2 \\cdot a^{-1} < 0 \\cdot a^{-1} \\iff a < 0,$$\n\n"
              "lo cual contradice la hipótesis $a > 0$. $\\quad\\square$"
          )),

        b("teorema",
          enunciado_md=(
              "**Multiplicación por negativo invierte.** Si $a < b$:\n\n"
              "1. Si $c > 0$, entonces $ac < bc$ (O4 directo).\n"
              "2. Si $c < 0$, entonces $ac > bc$.\n\n"
              "**Demostración del inciso 2.** Si $c < 0$, entonces $-c > 0$. Por O4 con $-c > 0$: "
              "$a(-c) < b(-c)$, es decir $-ac < -bc$. Por O3 sumando $ac + bc$ a ambos lados: $bc < ac$.\n\n"
              "**Observación crítica.** Al multiplicar (o dividir) ambos lados de una desigualdad por "
              "un número **negativo**, el sentido **se invierte**. Tenelo siempre presente al manipular "
              "inecuaciones."
          )),

        b("ejemplo_resuelto",
          titulo="Demostración usando la equivalencia fundamental",
          problema_md=(
              "Pruebe que si $a < b$ y $c < d$, entonces $ad + bc < ac + bd$."
          ),
          pasos=[
              {"accion_md": (
                  "Si $a < b$ y $c < d$, entonces $b - a \\in \\mathbb{R}^+$ y $d - c \\in \\mathbb{R}^+$."
               ),
               "justificacion_md": "Aplicación directa de la equivalencia fundamental.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $\\mathbb{R}^+$ es cerrado por producto:\n\n"
                  "$(b - a)(d - c) \\in \\mathbb{R}^+ \\iff (b - a)(d - c) > 0.$"
               ),
               "justificacion_md": "Producto de positivos es positivo.",
               "es_resultado": False},
              {"accion_md": (
                  "Desarrollando: $bd - bc - ad + ac > 0$, es decir $ac + bd > ad + bc$.\n\n"
                  "$\\boxed{ad + bc < ac + bd.} \\quad\\square$"
               ),
               "justificacion_md": "Sumando $ad + bc$ a ambos lados (O3) y reorganizando.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="$0 < a < b \\Rightarrow a^2 < b^2$",
          problema_md=(
              "Demuestre que si $0 < a < b$, entonces $a^2 < b^2$."
          ),
          pasos=[
              {"accion_md": (
                  "Si $a < b$, entonces $b - a > 0$. Por hipótesis $a > 0$ y $b > 0$, luego $a + b > 0$ "
                  "(cerradura de $\\mathbb{R}^+$ bajo suma)."
               ),
               "justificacion_md": "Vamos a fabricar el factor $(b-a)(b+a) = b^2 - a^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $b - a > 0$ y $b + a > 0$, por cerradura del producto:\n\n"
                  "$(b - a)(b + a) > 0 \\iff b^2 - a^2 > 0 \\iff \\boxed{b^2 > a^2.} \\quad\\square$"
               ),
               "justificacion_md": "Producto de positivos. Diferencia de cuadrados.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Desigualdad de medias (AM-GM)",
          problema_md=(
              "Pruebe la **desigualdad entre la media geométrica y la media aritmética**:\n\n"
              "$$\\sqrt{ab} \\leq \\frac{a+b}{2} \\quad \\text{para todo } a, b > 0.$$"
          ),
          pasos=[
              {"accion_md": (
                  "Por contradicción: supongamos $\\frac{a+b}{2} < \\sqrt{ab}$. Como $a, b > 0$, "
                  "ambos lados son positivos. Aplicando lo demostrado antes "
                  "($0 < x < y \\Rightarrow x^2 < y^2$):\n\n"
                  "$\\left(\\frac{a+b}{2}\\right)^2 < ab \\iff \\frac{(a+b)^2}{4} < ab.$"
               ),
               "justificacion_md": "Elevar al cuadrado preserva el orden cuando ambos lados son "
                                   "positivos.",
               "es_resultado": False},
              {"accion_md": (
                  "Multiplicando por $4 > 0$: $(a+b)^2 < 4ab$. Desarrollando:\n\n"
                  "$a^2 + 2ab + b^2 < 4ab \\iff a^2 - 2ab + b^2 < 0 \\iff (a - b)^2 < 0.$"
               ),
               "justificacion_md": "Pasamos $4ab$ al otro lado y reconocemos un cuadrado perfecto.",
               "es_resultado": False},
              {"accion_md": (
                  "Esto contradice el teorema $a^2 \\geq 0$ aplicado a $(a - b)$. La hipótesis era falsa, "
                  "por tanto $\\boxed{\\sqrt{ab} \\leq \\dfrac{a+b}{2}.} \\quad\\square$"
               ),
               "justificacion_md": "Toda contradicción cierra la prueba por contradicción.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Punto medio entre $a$ y $b$",
          problema_md=(
              "Demuestre que si $a < b$, entonces $a < \\dfrac{a+b}{2} < b$."
          ),
          pasos=[
              {"accion_md": (
                  "**Lado izquierdo.** Sumando $a$ a ambos lados de $a < b$ (axioma O3):\n\n"
                  "$a + a < a + b \\iff 2a < a + b \\iff a < \\dfrac{a+b}{2}.$"
               ),
               "justificacion_md": "Dividir por $2 > 0$ no invierte la desigualdad.",
               "es_resultado": False},
              {"accion_md": (
                  "**Lado derecho.** Sumando $b$ a ambos lados de $a < b$:\n\n"
                  "$a + b < b + b \\iff a + b < 2b \\iff \\dfrac{a+b}{2} < b.$\n\n"
                  "Combinando: $\\boxed{a < \\dfrac{a+b}{2} < b.} \\quad\\square$"
               ),
               "justificacion_md": "Geométricamente, el punto medio entre $a$ y $b$ está estrictamente "
                                   "entre ambos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Producto de desigualdades positivas",
          problema_md=(
              "Demuestre que si $0 < a < b$ y $0 < c < d$, entonces $ac < bd$."
          ),
          pasos=[
              {"accion_md": (
                  "Como $a < b$ y $c > 0$, por O4 obtenemos $ac < bc$."
               ),
               "justificacion_md": "Multiplicar por $c > 0$ preserva el sentido.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $c < d$ y $b > 0$, por O4 obtenemos $bc < bd$."
               ),
               "justificacion_md": "Multiplicar por $b > 0$ preserva el sentido.",
               "es_resultado": False},
              {"accion_md": (
                  "Por transitividad (O2): $ac < bc < bd \\Rightarrow \\boxed{ac < bd.} \\quad\\square$"
               ),
               "justificacion_md": "Cadena $ac < bc$ y $bc < bd$ implica $ac < bd$.",
               "es_resultado": True},
          ]),

        ej(
            "$n^2 \\geq n$ para todo natural",
            "Demuestre que para todo $n \\in \\mathbb{N}$ se cumple $n^2 \\geq n$.",
            [
                "Separá la demostración en dos casos: $n = 1$ y $n \\geq 2$.",
                "Para $n \\geq 2$, mostrá $n - 1 \\in \\mathbb{R}^+$ y aplicá cerradura.",
                "Recordá que $n^2 - n = n(n-1)$.",
            ],
            (
                "**Caso 1: $n = 1$.** Entonces $n^2 = 1 = n$, luego $n^2 \\geq n$ ✓.\n\n"
                "**Caso 2: $n \\geq 2$.** Entonces $n - 1 \\geq 1 > 0$ y $n > 0$. Por cerradura del producto:\n\n"
                "$$(n-1) \\cdot n > 0 \\iff n^2 - n > 0 \\iff n^2 > n.$$\n\n"
                "Combinando ambos casos: $n^2 \\geq n$ para todo $n \\in \\mathbb{N}$. $\\quad\\square$"
            ),
        ),

        fig(
            "Diagrama de la recta real numérica horizontal con cero al centro, mostrando los axiomas "
            "de orden. Línea recta con marcas en -3, -2, -1, 0, 1, 2, 3. La parte derecha del 0 "
            "sombreada en teal #06b6d4 con etiqueta 'R+ (positivos): cerrado bajo suma y producto'. "
            "La parte izquierda en gris claro con etiqueta 'R- (negativos)'. "
            "Sobre la recta dos flechas curvas ámbar #f59e0b: una entre -2 y 1 marcada 'a < b' y otra "
            "ilustrando 'multiplicar por c < 0 invierte: ac > bc'. Tipografía clara, fondo blanco. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica los axiomas de orden:",
          preguntas=[
              {"enunciado_md": "Si $a < b$ y $c < 0$, ¿qué se concluye sobre $ac$ y $bc$?",
               "opciones_md": ["$ac < bc$", "$ac > bc$", "$ac = bc$", "Nada se puede concluir"],
               "correcta": "B",
               "pista_md": "Multiplicar por un negativo invierte el sentido de la desigualdad.",
               "explicacion_md": "Al multiplicar ambos lados por $c < 0$ la desigualdad se invierte: $ac > bc$."},
              {"enunciado_md": "Si $0 < a < b$, ¿cuál de las siguientes es siempre verdadera?",
               "opciones_md": ["$\\tfrac{1}{a} < \\tfrac{1}{b}$", "$\\tfrac{1}{a} > \\tfrac{1}{b}$", "$a^2 > b^2$", "$a - b > 0$"],
               "correcta": "B",
               "pista_md": "Tomar inversos en positivos invierte el orden.",
               "explicacion_md": "Como $a$ y $b$ son positivos y $a < b$, al tomar recíprocos el orden se invierte: $1/a > 1/b$."},
              {"enunciado_md": "¿Cuál de estas afirmaciones es FALSA?",
               "opciones_md": [
                   "$\\mathbb{R}^+$ es cerrado bajo suma",
                   "$\\mathbb{R}^+$ es cerrado bajo producto",
                   "$\\mathbb{R}^+$ es cerrado bajo resta",
                   "Si $a, b > 0$ entonces $a + b > 0$",
               ],
               "correcta": "C",
               "pista_md": "Pensa un contraejemplo con dos positivos cuya resta sea negativa.",
               "explicacion_md": "$3, 5 \\in \\mathbb{R}^+$ pero $3 - 5 = -2 \\notin \\mathbb{R}^+$. La resta no preserva positividad."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Olvidar invertir el sentido al multiplicar por negativo:** $a < b$ y $c < 0$ NO implica $ac < bc$ — lo correcto es $ac > bc$.",
              "**Aplicar tricotomía como si valiera $a \\leq b$ o $b \\leq a$ siempre:** la tricotomía es estricta entre **una** de las tres condiciones $a = b$, $a < b$, $b < a$.",
              "**Sumar desigualdades de sentidos opuestos:** si $a < b$ y $c > d$, no se puede concluir nada directo sobre $a + c$ vs. $b + d$.",
              "**Tomar raíz cuadrada sin justificar la positividad:** $a^2 < b^2$ implica $|a| < |b|$, no $a < b$ (los signos cuentan).",
              "**Asumir $\\mathbb{R}^+$ es cerrado bajo resta:** $5, 3 \\in \\mathbb{R}^+$ pero $3 - 5 = -2 \\notin \\mathbb{R}^+$. Solo suma y producto.",
          ]),

        b("resumen",
          puntos_md=[
              "**4 axiomas de orden:** O1 tricotomía, O2 transitividad, O3 compatibilidad con suma, O4 compatibilidad con producto positivo.",
              "**$\\mathbb{R}^+$ es cerrado** bajo suma y producto.",
              "**Equivalencia fundamental:** $a < b \\iff b - a \\in \\mathbb{R}^+$.",
              "**Cuadrados:** $a^2 \\geq 0$ siempre, con igualdad solo si $a = 0$.",
              "**Multiplicar por negativo** invierte el sentido de la desigualdad.",
              "**Desigualdad de medias:** $\\sqrt{ab} \\leq \\dfrac{a+b}{2}$ para $a, b > 0$.",
              "**Próxima lección:** valor absoluto — distancia y norma de un real.",
          ]),
    ]
    return {
        "id": "lec-ic-2-1-axiomas-orden",
        "title": "Axiomas de orden",
        "description": "Los cuatro axiomas de orden, $\\mathbb{R}^+$ y su cerradura, teoremas derivados (signos, multiplicación, AM-GM) y técnicas de demostración.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 1,
    }


# =====================================================================
# 2.2 Valor Absoluto
# =====================================================================
def lesson_2_2():
    blocks = [
        b("texto", body_md=(
            "Además de la estructura de orden, los reales tienen **estructura métrica**: podemos medir "
            "distancias entre puntos. El concepto que captura esto es la **función valor absoluto**, que "
            "asigna a cada número real su \"tamaño\" o \"magnitud\" sin importar el signo.\n\n"
            "**Objetivos:**\n\n"
            "- Definición formal de $|x|$ y su interpretación geométrica.\n"
            "- Propiedades fundamentales (incluyendo la **desigualdad triangular**).\n"
            "- Resolver **ecuaciones** con valor absoluto.\n"
            "- Comprender la **distancia** entre puntos reales como $d(x, y) = |x - y|$."
        )),

        b("definicion",
          titulo="Valor absoluto",
          body_md=(
              "Para cualquier $x \\in \\mathbb{R}$ se define\n\n"
              "$$|x| = \\begin{cases} x & \\text{si } x \\geq 0, \\\\ -x & \\text{si } x < 0. \\end{cases}$$\n\n"
              "**Forma equivalente:** $|x| = \\sqrt{x^2}$. De aquí se deduce la identidad clave\n\n"
              "$$|x|^2 = x^2 \\quad \\text{para todo } x \\in \\mathbb{R},$$\n\n"
              "que será de gran utilidad en demostraciones."
          )),

        b("intuicion", body_md=(
            "**Interpretación geométrica.** $|x|$ representa la **distancia** del punto $x$ al origen "
            "$0$ en la recta real. Por ejemplo:\n\n"
            "- $|3| = 3$ porque $3$ está a distancia $3$ del origen.\n"
            "- $|-5| = 5$ porque $-5$ está a distancia $5$ del origen.\n\n"
            "Más en general, $|x - a|$ es la distancia entre $x$ y $a$ — la noción de \"qué tan cerca\" "
            "está $x$ del punto $a$."
        )),

        fig(
            "Recta real horizontal con marcas en -5, -3, 0, 3, 5. Sobre la recta, dos arcos curvos "
            "etiquetados: uno desde 0 hasta 3 con etiqueta '|3| = 3' (arco color teal #06b6d4), otro "
            "desde -5 hasta 0 con etiqueta '|-5| = 5' (arco color ámbar #f59e0b). Debajo, una segunda "
            "recta con marcas en a=2 y x=7, y un arco entre ellos etiquetado 'd(x,a) = |x - a| = 5'. "
            "Título arriba: 'Valor absoluto = distancia al origen'. Subtítulo: 'En general, |x - a| "
            "mide la distancia entre x y a'. " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Propiedades del valor absoluto.** Para todo $x, y \\in \\mathbb{R}$ y $a \\geq 0$:\n\n"
              "- **(a)** $|x| \\geq 0$, con igualdad si y solo si $x = 0$.\n"
              "- **(b)** $-|x| \\leq x \\leq |x|$.\n"
              "- **(c)** $|xy| = |x||y|$.\n"
              "- **(d)** $|x| \\leq a \\iff -a \\leq x \\leq a$.\n"
              "- **(e)** $|x| \\geq a \\iff x \\leq -a$ o $x \\geq a$.\n"
              "- **(f)** $|x + y| \\leq |x| + |y|$ — **Desigualdad triangular**.\n"
              "- **(g)** $\\bigl||x| - |y|\\bigr| \\leq |x - y|$ — **Desigualdad triangular inversa**."
          )),

        b("ejemplo_resuelto",
          titulo="Demostración de la desigualdad triangular",
          problema_md=(
              "Pruebe que $|x + y| \\leq |x| + |y|$ para todo $x, y \\in \\mathbb{R}$."
          ),
          pasos=[
              {"accion_md": (
                  "Usamos $|x|^2 = x^2$ para evitar el análisis por casos. Calculamos:\n\n"
                  "$|x + y|^2 = (x + y)^2 = x^2 + 2xy + y^2 = |x|^2 + 2xy + |y|^2.$"
               ),
               "justificacion_md": "Al cuadrado, todo se simplifica algebraicamente.",
               "es_resultado": False},
              {"accion_md": (
                  "Por la propiedad (b), $xy \\leq |xy| = |x||y|$. Multiplicando por $2 > 0$:\n\n"
                  "$2xy \\leq 2|x||y|.$"
               ),
               "justificacion_md": "Como $xy$ podría ser negativo, lo acotamos por su valor absoluto.",
               "es_resultado": False},
              {"accion_md": (
                  "Sumando $|x|^2 + |y|^2$ a ambos lados:\n\n"
                  "$|x|^2 + 2xy + |y|^2 \\leq |x|^2 + 2|x||y| + |y|^2 = (|x| + |y|)^2.$\n\n"
                  "Es decir, $|x + y|^2 \\leq (|x| + |y|)^2$. Como ambos lados son no negativos, "
                  "extrayendo raíz preserva el orden:\n\n"
                  "$\\boxed{|x + y| \\leq |x| + |y|.} \\quad\\square$"
               ),
               "justificacion_md": "$0 \\leq A \\leq B \\Rightarrow \\sqrt{A} \\leq \\sqrt{B}$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="$|x| - |y| \\leq |x - y|$",
          problema_md=(
              "Demuestre que para todo $x, y \\in \\mathbb{R}$ se cumple $|x| - |y| \\leq |x - y|$."
          ),
          pasos=[
              {"accion_md": (
                  "Usamos el truco de **sumar y restar**: $x = (x - y) + y$. Aplicando desigualdad "
                  "triangular:\n\n"
                  "$|x| = |(x - y) + y| \\leq |x - y| + |y|.$"
               ),
               "justificacion_md": "Reescribimos $x$ y aplicamos triangular al resultado.",
               "es_resultado": False},
              {"accion_md": (
                  "Restando $|y|$ a ambos lados (axioma O3):\n\n"
                  "$\\boxed{|x| - |y| \\leq |x - y|.} \\quad\\square$"
               ),
               "justificacion_md": "Esto es la desigualdad triangular inversa (un lado).",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Distancia en $\\mathbb{R}$",
          body_md=(
              "La **distancia** entre dos números reales $x, y$ es\n\n"
              "$$d(x, y) = |x - y|.$$\n\n"
              "Esta definición dota a $\\mathbb{R}$ de una **estructura métrica**. En cálculo casi "
              "siempre escribimos $|x - y|$ directamente en lugar de $d(x, y)$.\n\n"
              "**Conexión con cálculo.** Cuando una sucesión $x_1, x_2, x_3, \\ldots$ se acerca a un "
              "punto $c$, decimos que $|x_n - c|$ se hace cada vez más pequeño. Es la idea **central** "
              "del concepto de límite."
          )),

        b("ejemplo_resuelto",
          titulo="Resolver $|x - 1| = 3$",
          problema_md=(
              "Resuelva la ecuación $|x - 1| = 3$ e interprétela geométricamente."
          ),
          pasos=[
              {"accion_md": (
                  "$|A| = a$ con $a \\geq 0$ si y solo si $A = a$ o $A = -a$. Aplicando con $A = x - 1$ "
                  "y $a = 3$:\n\n"
                  "$x - 1 = 3 \\quad \\text{o} \\quad x - 1 = -3.$"
               ),
               "justificacion_md": "Eliminamos el valor absoluto separando en dos casos.",
               "es_resultado": False},
              {"accion_md": (
                  "De la primera: $x = 4$. De la segunda: $x = -2$.\n\n"
                  "$\\boxed{\\text{Conjunto solución} = \\{-2,\\, 4\\}.}$\n\n"
                  "**Geométricamente:** $|x - 1| = 3$ pide los puntos cuya distancia al $1$ es exactamente $3$."
               ),
               "justificacion_md": "$1 + 3 = 4$ y $1 - 3 = -2$, ambos a distancia $3$ del $1$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Ecuación sin solución",
          problema_md=(
              "Resuelva $|3x - 5| + 3 = 0$."
          ),
          pasos=[
              {"accion_md": (
                  "Despejando: $|3x - 5| = -3$."
               ),
               "justificacion_md": "Restamos $3$ de ambos lados.",
               "es_resultado": False},
              {"accion_md": (
                  "Por la propiedad (a), $|3x - 5| \\geq 0$ para todo $x$. Nunca puede ser $-3$.\n\n"
                  "$\\boxed{\\text{Conjunto solución} = \\emptyset.}$"
               ),
               "justificacion_md": "**Antes de operar, comprobá la factibilidad:** valor absoluto "
                                   "negativo es imposible.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="$|x + 2| = |x - 1|$",
          problema_md=(
              "Resuelva $|x + 2| = |x - 1|$."
          ),
          pasos=[
              {"accion_md": (
                  "Como ambos lados son no negativos, podemos elevar al cuadrado preservando la igualdad:\n\n"
                  "$|x + 2|^2 = |x - 1|^2 \\iff (x + 2)^2 = (x - 1)^2.$"
               ),
               "justificacion_md": "$|A|^2 = A^2$ — el truco evita partir en casos.",
               "es_resultado": False},
              {"accion_md": (
                  "Expandiendo: $x^2 + 4x + 4 = x^2 - 2x + 1$. Simplificando $x^2$:\n\n"
                  "$4x + 4 = -2x + 1 \\iff 6x = -3 \\iff x = -\\dfrac{1}{2}.$"
               ),
               "justificacion_md": "Ecuación lineal directa.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación:** $|-\\tfrac{1}{2} + 2| = |\\tfrac{3}{2}| = \\tfrac{3}{2}$ y "
                  "$|-\\tfrac{1}{2} - 1| = |-\\tfrac{3}{2}| = \\tfrac{3}{2}$ ✓.\n\n"
                  "$\\boxed{x = -\\tfrac{1}{2}.}$ Geométricamente, es el **punto medio** entre $-2$ y $1$."
               ),
               "justificacion_md": "El punto a la misma distancia de $-2$ y $1$ es $\\frac{-2 + 1}{2}$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="$|x - a| < \\varepsilon$ — preludio del límite",
          problema_md=(
              "Demuestre que $|x - a| < \\varepsilon$ es equivalente a $a - \\varepsilon < x < a + \\varepsilon$. "
              "Interprete geométricamente."
          ),
          pasos=[
              {"accion_md": (
                  "Por la propiedad (d) con $a = \\varepsilon$:\n\n"
                  "$|x - a| < \\varepsilon \\iff -\\varepsilon < x - a < \\varepsilon.$"
               ),
               "justificacion_md": "Conversión directa.",
               "es_resultado": False},
              {"accion_md": (
                  "Sumando $a$ en toda la cadena (O3):\n\n"
                  "$\\boxed{a - \\varepsilon < x < a + \\varepsilon.}$\n\n"
                  "**Interpretación:** los $x$ cuya distancia a $a$ es menor que $\\varepsilon$ son "
                  "exactamente los del intervalo abierto $(a - \\varepsilon,\\ a + \\varepsilon)$ — una "
                  "**\"bola\" de radio $\\varepsilon$** centrada en $a$. Esto es **fundamental** para "
                  "definir límites en cálculo."
               ),
               "justificacion_md": "Concepto que reaparecerá una y otra vez.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cuándo se cumple $|x + y| = |x| + |y|$",
          problema_md=(
              "¿Bajo qué condiciones se cumple la **igualdad** en la desigualdad triangular?"
          ),
          pasos=[
              {"accion_md": (
                  "En la demostración, el paso clave fue $xy \\leq |xy| = |x||y|$. La igualdad ocurre "
                  "exactamente cuando $xy = |xy|$, es decir cuando $xy \\geq 0$."
               ),
               "justificacion_md": "$xy \\leq |xy|$ con igualdad si y solo si $xy \\geq 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "$xy \\geq 0$ ocurre exactamente cuando $x$ e $y$ tienen el **mismo signo** (ambos "
                  "$\\geq 0$, ambos $\\leq 0$, o al menos uno cero).\n\n"
                  "$\\boxed{|x + y| = |x| + |y| \\iff xy \\geq 0.}$"
               ),
               "justificacion_md": "Condición geométrica: vectores en la misma dirección.",
               "es_resultado": True},
          ]),

        ej(
            "Monotonía de $\\sqrt{\\,\\cdot\\,}$",
            "Demuestre que si $0 < a < b$, entonces $\\sqrt{a} < \\sqrt{b}$.",
            [
                "Procedé por contradicción.",
                "Si $\\sqrt{a} \\geq \\sqrt{b}$, elevá al cuadrado y usá que ambos son no negativos.",
                "Recordá que $0 < x < y \\Rightarrow x^2 < y^2$.",
            ],
            (
                "Por contradicción, supongamos $\\sqrt{a} \\geq \\sqrt{b}$. Como $\\sqrt{a}, \\sqrt{b} \\geq 0$, "
                "elevando al cuadrado preserva la desigualdad: $(\\sqrt{a})^2 \\geq (\\sqrt{b})^2$, es decir $a \\geq b$.\n\n"
                "Esto contradice la hipótesis $a < b$. Por tanto $\\sqrt{a} < \\sqrt{b}$. $\\quad\\square$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión del valor absoluto:",
          preguntas=[
              {"enunciado_md": "¿Cuál es la solución de $|2x - 3| = 5$?",
               "opciones_md": ["$x = 4$ solamente", "$x = 4$ o $x = -1$", "$x = -4$ o $x = 1$", "$x = 1$ solamente"],
               "correcta": "B",
               "pista_md": "$|f| = a$ con $a \\geq 0$ se separa en $f = a$ o $f = -a$.",
               "explicacion_md": "$2x - 3 = 5 \\Rightarrow x = 4$, o $2x - 3 = -5 \\Rightarrow x = -1$. Ambas soluciones son válidas."},
              {"enunciado_md": "¿Cuál de las siguientes es la desigualdad triangular correctamente aplicada?",
               "opciones_md": [
                   "$|x + y| = |x| + |y|$ siempre",
                   "$|x + y| \\leq |x| + |y|$",
                   "$|x + y| \\geq |x| + |y|$",
                   "$|x - y| = |x| - |y|$",
               ],
               "correcta": "B",
               "pista_md": "La desigualdad triangular es siempre $\\leq$, con igualdad solo si $x, y$ tienen el mismo signo.",
               "explicacion_md": "$|x + y| \\leq |x| + |y|$ es la desigualdad triangular. La igualdad solo se da si $x$ y $y$ tienen el mismo signo (o uno es $0$)."},
              {"enunciado_md": "¿Cuántas soluciones tiene la ecuación $|3x + 1| = -2$?",
               "opciones_md": ["Infinitas", "Dos", "Una", "Ninguna"],
               "correcta": "D",
               "pista_md": "El valor absoluto siempre es $\\geq 0$.",
               "explicacion_md": "$|f(x)| \\geq 0$ siempre, así que nunca puede igualar a un número negativo. $S = \\emptyset$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Pensar que $|-x| = -|x|$:** lo correcto es $|-x| = |x|$ (el valor absoluto siempre es no negativo).",
              "**Distribuir incorrectamente:** $|x + y| \\neq |x| + |y|$ en general — solo $\\leq$.",
              "**Olvidar elevar al cuadrado preserva el orden solo si ambos lados son $\\geq 0$:** $-3 < 2$ pero $9 > 4$.",
              "**Resolver $|f(x)| = a$ con $a < 0$ buscando soluciones:** simplemente no hay (conjunto vacío).",
              "**Confundir $|x - a|$ con $|x| - a$:** son cosas distintas. $|x - 3| \\neq |x| - 3$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición:** $|x| = x$ si $x \\geq 0$, $|x| = -x$ si $x < 0$. Equivalentemente $|x| = \\sqrt{x^2}$.",
              "**Identidad clave:** $|x|^2 = x^2$.",
              "**Propiedades:** no negatividad, $|xy| = |x||y|$, $|x| \\leq a \\iff -a \\leq x \\leq a$, $|x| \\geq a \\iff x \\leq -a$ o $x \\geq a$.",
              "**Desigualdad triangular:** $|x + y| \\leq |x| + |y|$, con igualdad si $xy \\geq 0$.",
              "**Distancia:** $d(x, y) = |x - y|$ — base métrica de $\\mathbb{R}$.",
              "**$|x - a| < \\varepsilon$:** intervalo $(a - \\varepsilon, a + \\varepsilon)$ — preludio del límite.",
              "**Próxima lección:** intervalos e inecuaciones de primer y segundo grado.",
          ]),
    ]
    return {
        "id": "lec-ic-2-2-valor-absoluto",
        "title": "Valor absoluto",
        "description": "Definición, propiedades, desigualdad triangular, distancia métrica y resolución de ecuaciones con valor absoluto.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 2.3 Intervalos e Inecuaciones
# =====================================================================
def lesson_2_3():
    blocks = [
        b("texto", body_md=(
            "Los **intervalos** y las **inecuaciones** son las herramientas básicas para describir "
            "subconjuntos de $\\mathbb{R}$ definidos por desigualdades. Son la primera materia que "
            "manejaremos con fluidez antes de tocar límites, continuidad o derivadas.\n\n"
            "**Objetivos:**\n\n"
            "- Conocer los **tipos de intervalos** (acotados y no acotados).\n"
            "- Comprender **inecuación** y **conjunto solución** como unión de intervalos disjuntos.\n"
            "- Resolver **inecuaciones de primer grado** $0 \\leq ax + b$.\n"
            "- Resolver **inecuaciones de segundo grado** $ax^2 + bx + c > 0$ usando discriminante y "
            "signo del coeficiente líder."
        )),

        b("definicion",
          titulo="Tipos de intervalo",
          body_md=(
              "Sean $a, b \\in \\mathbb{R}$ con $a \\leq b$.\n\n"
              "**Acotados:**\n\n"
              "- **Abierto:** $(a, b) = \\{ x \\in \\mathbb{R} : a < x < b \\}$.\n"
              "- **Cerrado:** $[a, b] = \\{ x \\in \\mathbb{R} : a \\leq x \\leq b \\}$.\n"
              "- **Semiabierto izq:** $(a, b] = \\{ x : a < x \\leq b \\}$.\n"
              "- **Semiabierto der:** $[a, b) = \\{ x : a \\leq x < b \\}$.\n\n"
              "**No acotados:**\n\n"
              "- $(-\\infty, a] = \\{ x : x \\leq a \\}$, $\\;(-\\infty, a) = \\{ x : x < a \\}$.\n"
              "- $[a, +\\infty) = \\{ x : a \\leq x \\}$, $\\;(a, +\\infty) = \\{ x : a < x \\}$.\n\n"
              "**Notación alternativa (Bourbaki, usada en Chile):** $(a, b)$ también se escribe $]a, b[$.\n\n"
              "**Casos degenerados:** $(a, a) = (a, a] = [a, a) = \\emptyset$; $[a, a] = \\{a\\}$. Y "
              "$\\mathbb{R} = (-\\infty, +\\infty)$."
          )),

        fig(
            "Cuatro rectas reales horizontales apiladas verticalmente, cada una mostrando un tipo de "
            "intervalo entre puntos a y b. (1) Intervalo abierto (a,b): círculos vacíos en a y b, "
            "segmento sombreado teal #06b6d4 entre ellos, etiqueta '(a, b)'. (2) Intervalo cerrado "
            "[a,b]: círculos rellenos en a y b, segmento sombreado, etiqueta '[a, b]'. (3) Semiabierto "
            "(a,b]: círculo vacío en a, lleno en b, etiqueta '(a, b]'. (4) Semiabierto [a,b): círculo "
            "lleno en a, vacío en b, etiqueta '[a, b)'. Abajo, dos rectas más con intervalos no "
            "acotados: '(-∞, a]' con flecha hacia la izquierda y círculo lleno en a; '(a, +∞)' con "
            "círculo vacío en a y flecha hacia la derecha. Título: 'Tipos de intervalos en R'. " + STYLE
        ),

        b("definicion",
          titulo="Inecuación y conjunto solución",
          body_md=(
              "Una **inecuación de una incógnita** es una desigualdad que puede ser verdadera o falsa "
              "dependiendo del valor asignado a la incógnita. **Resolverla** consiste en determinar todos "
              "los reales para los cuales la inecuación es verdadera.\n\n"
              "El **conjunto solución** $S$ es el conjunto de todas esas soluciones, expresado como "
              "**unión de intervalos disjuntos**.\n\n"
              "Como los intervalos siempre se anotan con $\\pm \\infty$ usando paréntesis (no corchetes "
              "— $\\pm\\infty$ no son números reales), un conjunto solución típico se ve así:\n\n"
              "$$S = (-\\infty, -2) \\cup (1, +\\infty).$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Resolución de inecuación de primer grado** $0 \\leq ax + b$.\n\n"
              "Despejando $-b \\leq ax$ y aplicando los axiomas de orden:\n\n"
              "- Si $a > 0$: dividir por $a$ **preserva** el sentido. El conjunto solución es "
              "$S = \\left[ -\\dfrac{b}{a},\\ +\\infty \\right).$\n"
              "- Si $a < 0$: dividir por $a$ **invierte** el sentido. El conjunto solución es "
              "$S = \\left( -\\infty,\\ -\\dfrac{b}{a} \\right].$\n\n"
              "**Lo crítico es el signo de $a$**: invertís el sentido de la desigualdad cuando dividís "
              "por un negativo."
          )),

        b("teorema",
          enunciado_md=(
              "**Resolución de inecuación de segundo grado** $ax^2 + bx + c > 0$ con $a \\neq 0$.\n\n"
              "Sea $\\Delta = b^2 - 4ac$ el **discriminante**.\n\n"
              "**Caso 1:** $\\Delta \\geq 0$. El polinomio tiene raíces reales $x_1 \\leq x_2$.\n\n"
              "- Si $a > 0$ (parábola abre hacia arriba): positivo **fuera** de las raíces: "
              "$S = (-\\infty, x_1) \\cup (x_2, +\\infty)$.\n"
              "- Si $a < 0$ (parábola abre hacia abajo): positivo **entre** las raíces: $S = (x_1, x_2)$.\n\n"
              "**Caso 2:** $\\Delta < 0$. No hay raíces reales (la parábola no corta al eje).\n\n"
              "- Si $a > 0$: parábola siempre arriba del eje. $S = \\mathbb{R}$.\n"
              "- Si $a < 0$: parábola siempre debajo del eje. $S = \\emptyset$.\n\n"
              "**Para inecuación no estricta** $ax^2 + bx + c \\geq 0$, incluí las raíces en el "
              "conjunto solución (paréntesis $\\to$ corchetes en los extremos finitos)."
          )),

        b("intuicion", body_md=(
            "**Cómo recordar los 4 casos.** Visualizá la parábola $y = ax^2 + bx + c$ y preguntate "
            "**en qué regiones se encuentra por encima del eje $x$**. La tabla resumen:\n\n"
            "| Discriminante | Coef. líder | $S$ de $ax^2+bx+c > 0$ | Descripción |\n"
            "|:---:|:---:|:---:|:---|\n"
            "| $\\Delta \\geq 0$ | $a > 0$ | $(-\\infty, x_1) \\cup (x_2, +\\infty)$ | Positivo fuera de las raíces |\n"
            "| $\\Delta \\geq 0$ | $a < 0$ | $(x_1, x_2)$ | Positivo entre las raíces |\n"
            "| $\\Delta < 0$ | $a > 0$ | $\\mathbb{R}$ | Siempre positivo |\n"
            "| $\\Delta < 0$ | $a < 0$ | $\\emptyset$ | Nunca positivo |\n\n"
            "Memorizá la imagen, no la fórmula."
        )),

        fig(
            "Cuadrícula 2x2 con cuatro mini-gráficos de parábolas y = ax^2+bx+c, cada uno mostrando un "
            "caso del análisis. Cuadrante superior izquierdo: parábola hacia arriba (a>0) con dos "
            "raíces reales x1 < x2 marcadas en el eje x; las regiones x<x1 y x>x2 sombreadas teal "
            "#06b6d4 y etiquetadas 'y > 0'. Cuadrante superior derecho: parábola hacia abajo (a<0) con "
            "raíces x1<x2; la región entre x1 y x2 sombreada teal etiquetada 'y > 0'. Cuadrante "
            "inferior izquierdo: parábola hacia arriba (a>0) sin raíces, completamente sobre el eje x, "
            "etiqueta 'Δ<0, S = R'. Cuadrante inferior derecho: parábola hacia abajo (a<0) sin raíces, "
            "completamente bajo el eje x, etiqueta 'Δ<0, S = ∅'. Encima de cada subgráfico: 'Δ≥0,a>0' "
            "etc. Título general: 'Inecuación de 2do grado: 4 casos según Δ y signo de a'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Inecuación de segundo grado clásica",
          problema_md=(
              "Resuelva la inecuación $x^2 + x > 2$."
          ),
          pasos=[
              {"accion_md": (
                  "Llevamos todo al lado izquierdo: $x^2 + x - 2 > 0$. Identificamos $a = 1$, $b = 1$, "
                  "$c = -2$."
               ),
               "justificacion_md": "Forma estándar de la inecuación cuadrática.",
               "es_resultado": False},
              {"accion_md": (
                  "Discriminante: $\\Delta = 1 - 4(1)(-2) = 1 + 8 = 9 > 0$. Hay dos raíces reales:\n\n"
                  "$x_{1,2} = \\dfrac{-1 \\pm 3}{2}, \\quad \\text{luego } x_1 = -2, \\; x_2 = 1.$"
               ),
               "justificacion_md": "Fórmula cuadrática.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $a = 1 > 0$ (Caso 1a), el polinomio es positivo **fuera** del intervalo entre "
                  "raíces:\n\n"
                  "$\\boxed{S = (-\\infty, -2) \\cup (1, +\\infty).}$"
               ),
               "justificacion_md": "Inecuación estricta: paréntesis (no incluye raíces).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Para qué valores de un parámetro",
          problema_md=(
              "¿Para qué valores de $r \\in \\mathbb{R}$ se cumple que $x^2 + 2x + r > 10$ para **todo** "
              "$x \\in \\mathbb{R}$?"
          ),
          pasos=[
              {"accion_md": (
                  "Reescribimos como $x^2 + 2x + (r - 10) > 0$ para todo $x$. Identificamos $a = 1 > 0$, "
                  "$b = 2$, $c = r - 10$."
               ),
               "justificacion_md": "Para que sea positivo **siempre** estamos en el Caso 2a "
                                   "($\\Delta < 0$, $a > 0$).",
               "es_resultado": False},
              {"accion_md": (
                  "Discriminante: $\\Delta = 4 - 4(r - 10) = 4 - 4r + 40 = 44 - 4r$. Imponemos $\\Delta < 0$:\n\n"
                  "$44 - 4r < 0 \\iff 44 < 4r \\iff r > 11.$"
               ),
               "justificacion_md": "Despeje algebraico.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\boxed{r > 11, \\text{ es decir, } r \\in (11, +\\infty).}$"
               ),
               "justificacion_md": "Para esos $r$, el cuadrático es siempre positivo.",
               "es_resultado": True},
          ]),

        ej(
            "Inecuación de segundo grado con $a < 0$",
            "Resuelva la inecuación $-x^2 + 3x + 4 \\geq 0$.",
            [
                "Identificá $a, b, c$ y calculá el discriminante.",
                "Cuando $a < 0$ y hay raíces, la solución es el intervalo **entre** las raíces.",
                "La inecuación es **no estricta** ($\\geq$), así que incluí las raíces.",
            ],
            (
                "$a = -1$, $b = 3$, $c = 4$. $\\Delta = 9 - 4(-1)(4) = 9 + 16 = 25 > 0$.\n\n"
                "Raíces: $x_{1,2} = \\dfrac{-3 \\pm 5}{-2}$, es decir $x_1 = -1$ y $x_2 = 4$ (orden creciente).\n\n"
                "Como $a < 0$ (Caso 1b), $-x^2 + 3x + 4$ es positivo **entre** las raíces. Inecuación no estricta: incluimos los extremos:\n\n"
                "$$\\boxed{S = [-1, 4].}$$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica tu manejo de intervalos e inecuaciones:",
          preguntas=[
              {"enunciado_md": "¿Cuál es el conjunto solución de $-3x + 6 \\leq 12$?",
               "opciones_md": ["$x \\leq -2$, es decir $(-\\infty, -2]$", "$x \\geq -2$, es decir $[-2, +\\infty)$", "$x \\leq 2$, es decir $(-\\infty, 2]$", "$x \\geq 2$, es decir $[2, +\\infty)$"],
               "correcta": "B",
               "pista_md": "Al dividir por $-3$ se invierte el sentido.",
               "explicacion_md": "$-3x \\leq 6 \\Rightarrow x \\geq -2$ (al dividir por $-3 < 0$ se invierte el $\\leq$ a $\\geq$)."},
              {"enunciado_md": "¿Cuál es la solución de $x^2 - 4 < 0$?",
               "opciones_md": ["$(-2, 2)$", "$[-2, 2]$", "$(-\\infty, -2) \\cup (2, +\\infty)$", "$(-\\infty, -2] \\cup [2, +\\infty)$"],
               "correcta": "A",
               "pista_md": "Factorizá $(x - 2)(x + 2)$ y analizá signos.",
               "explicacion_md": "$x^2 < 4 \\iff |x| < 2 \\iff -2 < x < 2$. Como la desigualdad es estricta, los extremos no se incluyen."},
              {"enunciado_md": "¿Por qué $(-\\infty, 5]$ se escribe con paréntesis en $-\\infty$ y corchete en $5$?",
               "opciones_md": [
                   "Porque $-\\infty$ es un número real pero excluido",
                   "Porque $-\\infty$ no es un número real, mientras que $5$ sí está incluido",
                   "Porque las convenciones de notación son arbitrarias",
                   "Porque $5$ siempre se excluye en intervalos",
               ],
               "correcta": "B",
               "pista_md": "$\\pm\\infty$ son símbolos, no reales — siempre se les pone paréntesis.",
               "explicacion_md": "$\\pm\\infty$ no pertenece a $\\mathbb{R}$, así que nunca puede 'incluirse'; $5$ está incluido por la igualdad del $\\leq$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Olvidar invertir la desigualdad al multiplicar/dividir por negativo:** $-2x < 6 \\Rightarrow x > -3$, no $x < -3$.",
              "**Incluir extremos en inecuaciones estrictas:** $x^2 < 4 \\Rightarrow S = (-2, 2)$, no $[-2, 2]$.",
              "**Confundir Caso 1a con Caso 1b:** repasá el signo del coeficiente líder antes de elegir el conjunto solución.",
              "**Reportar $\\mathbb{R}$ cuando $\\Delta < 0$ y $a < 0$:** ese caso da $\\emptyset$ (siempre negativo).",
              "**Usar $[+\\infty]$ con corchete:** $\\pm\\infty$ no son reales, siempre van con paréntesis.",
          ]),

        b("resumen",
          puntos_md=[
              "**Intervalos:** abiertos, cerrados, semiabiertos, no acotados — bloques fundamentales de subconjuntos de $\\mathbb{R}$.",
              "**Conjunto solución** se expresa como unión de intervalos disjuntos.",
              "**Primer grado:** despejar y atender el signo del coeficiente $a$ para saber si invertís.",
              "**Segundo grado:** depende del **discriminante** y del **signo de $a$** — 4 casos.",
              "**No estricta vs. estricta:** corchetes vs. paréntesis en los extremos finitos.",
              "**Próxima lección:** inecuaciones racionales — método de tabla de signos.",
          ]),
    ]
    return {
        "id": "lec-ic-2-3-intervalos-inecuaciones",
        "title": "Intervalos e inecuaciones",
        "description": "Tipos de intervalos, conjunto solución como unión de intervalos disjuntos, resolución sistemática de inecuaciones de primer y segundo grado.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# 2.4 Inecuaciones Racionales
# =====================================================================
def lesson_2_4():
    blocks = [
        b("texto", body_md=(
            "Las **inecuaciones racionales** aparecen naturalmente al estudiar el signo de cocientes "
            "de polinomios — algo que reaparece todo el tiempo en cálculo (signo de $f'(x)$ para "
            "monotonía, dominios de funciones racionales, etc.). En esta lección aprenderemos el "
            "método sistemático de la **tabla de signos**, herramienta fundamental para abordar este "
            "tipo de problemas de manera ordenada y a prueba de errores.\n\n"
            "**Objetivos:**\n\n"
            "- Comprender qué es una inecuación racional y cuándo aplica el método.\n"
            "- Identificar correctamente los **puntos críticos** del numerador y del denominador, "
            "distinguiendo cuáles son **restricciones** del dominio.\n"
            "- Aplicar el método paso a paso con factores lineales y cuadráticos.\n"
            "- Expresar el conjunto solución correctamente como unión de intervalos."
        )),

        b("definicion",
          titulo="Inecuación racional",
          body_md=(
              "Una **inecuación racional** es una desigualdad de la forma\n\n"
              "$$\\frac{P(x)}{Q(x)} \\;\\square\\; 0,$$\n\n"
              "donde $\\square$ representa uno de los signos $<, >, \\leq, \\geq$, y $P(x), Q(x)$ son "
              "polinomios con $Q(x) \\not\\equiv 0$.\n\n"
              "El **dominio natural** de la expresión $\\dfrac{P(x)}{Q(x)}$ excluye todos los $x$ para "
              "los cuales $Q(x) = 0$."
          )),

        b("definicion",
          titulo="Puntos críticos",
          body_md=(
              "Para cada factor lineal $(ax + b)$ que aparece en el numerador o denominador, su "
              "**punto crítico** es $x = -b/a$ (donde el factor se anula). Los puntos críticos son los "
              "**únicos lugares donde el signo de la expresión racional puede cambiar**.\n\n"
              "Hay que distinguir dos tipos:\n\n"
              "- **Puntos críticos del numerador:** valores donde $P(x) = 0$. La expresión vale **cero** ahí. "
              "**Pueden** pertenecer al conjunto solución si la inecuación es $\\leq$ o $\\geq$.\n"
              "- **Puntos críticos del denominador (restricciones):** valores donde $Q(x) = 0$. La "
              "expresión **no está definida** ahí. **Nunca** pertenecen al conjunto solución, "
              "independientemente del signo de la inecuación."
          )),

        b("definicion",
          titulo="Método de la tabla de signos — 5 pasos",
          body_md=(
              "**Paso 1: Llevar todo a un mismo lado.** Pasar todos los términos al lado izquierdo "
              "de modo que el lado derecho sea $0$. Combinar fracciones en un único cociente.\n\n"
              "**Paso 2: Factorizar numerador y denominador.** Lo más detallado posible (factores "
              "lineales o cuadráticos irreducibles).\n\n"
              "**Paso 3: Identificar puntos críticos.** Encontrar todos los $x$ que anulan algún factor. "
              "Ordenarlos en la recta real. Marcar cuáles son restricciones (vienen de $Q$).\n\n"
              "**Paso 4: Construir la tabla de signos.** Los puntos críticos dividen $\\mathbb{R}$ en "
              "intervalos abiertos. En cada uno, el signo de cada factor es constante. Determinar el "
              "signo de cada factor y luego del cociente.\n\n"
              "**Paso 5: Escribir el conjunto solución.** Seleccionar los intervalos donde el signo del "
              "cociente satisface la inecuación. Si es estricta ($<$ o $>$), excluir todos los puntos "
              "críticos. Si es $\\leq$ o $\\geq$, incluir los del numerador pero **siempre excluir los "
              "del denominador**."
          )),

        b("intuicion", body_md=(
            "**Regla de alternancia.** Al cruzar un punto crítico **simple**, el signo del factor "
            "correspondiente cambia. Si un factor aparece con exponente **par** (como $(x - a)^2$), "
            "su signo **no cambia** al cruzar $x = a$ — solo se anula ahí. Aprovechá esto para llenar "
            "la tabla más rápido."
        )),

        fig(
            "Diagrama de tabla de signos para la inecuación (x-1)/(x+2) ≤ 0. Recta real horizontal "
            "central con tres regiones marcadas por los puntos críticos x=-2 (círculo vacío, etiqueta "
            "'restricción') y x=1 (círculo lleno, etiqueta 'cero del numerador'). Encima de la recta, "
            "una tabla de tres columnas con: signo de (x-1) [-, -, +], signo de (x+2) [-, +, +], "
            "signo del cociente [+, -, +]. Las regiones donde el cociente ≤ 0 sombreadas teal "
            "#06b6d4: el intervalo (-2, 1] visible en la recta. Etiqueta inferior: 'S = (-2, 1]'. "
            "Color ámbar #f59e0b para resaltar la restricción x=-2 y un símbolo ⚠. Título: 'Tabla "
            "de signos: el signo solo cambia en puntos críticos'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Inecuación racional clásica",
          problema_md=(
              "Resuelva $\\dfrac{2x + 1}{x + 2} \\leq 1.$"
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1.** Pasamos todo al lado izquierdo y combinamos:\n\n"
                  "$\\dfrac{2x + 1}{x + 2} - 1 \\leq 0 \\iff \\dfrac{2x + 1 - (x + 2)}{x + 2} \\leq 0 "
                  "\\iff \\dfrac{x - 1}{x + 2} \\leq 0.$"
               ),
               "justificacion_md": "Crítico: NO multiplicar por $(x+2)$ sin saber su signo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Pasos 2-3.** Numerador $x - 1$: punto crítico $x = 1$. Denominador $x + 2$: punto "
                  "crítico $x = -2$ (restricción). Ordenados: $-2 < 1$. Tres intervalos: "
                  "$(-\\infty, -2)$, $(-2, 1)$ y $(1, +\\infty)$."
               ),
               "justificacion_md": "Identificar y ordenar todos los puntos críticos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 4.** Tabla de signos (valores de prueba: $x = -3,\\ x = 0,\\ x = 2$):\n\n"
                  "| Factor | $(-\\infty, -2)$ | $-2$ | $(-2, 1)$ | $1$ | $(1, +\\infty)$ |\n"
                  "|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                  "| $x - 1$ | $-$ | $-$ | $-$ | $0$ | $+$ |\n"
                  "| $x + 2$ | $-$ | $0$ | $+$ | $+$ | $+$ |\n"
                  "| $\\dfrac{x-1}{x+2}$ | $+$ | indef. | $-$ | $0$ | $+$ |"
               ),
               "justificacion_md": "Cociente de signos $-/-=+$, $-/+=-$, $+/+=+$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 5.** Buscamos donde el cociente es $\\leq 0$ (negativo o cero): el intervalo "
                  "$(-2, 1)$ y el punto $x = 1$. El punto $x = -2$ es restricción (excluido).\n\n"
                  "$\\boxed{S = (-2,\\ 1].}$"
               ),
               "justificacion_md": "Numerador anulado ($x = 1$) sí entra; denominador anulado nunca.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Numerador cuadrático factorizable",
          problema_md=(
              "Resuelva $\\dfrac{x^2 - 8x + 15}{x - 4} < 0.$"
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 2.** Factorizamos el numerador: dos números con producto $15$ y suma $-8$ "
                  "son $-3$ y $-5$. Luego $x^2 - 8x + 15 = (x - 3)(x - 5)$. La inecuación queda:\n\n"
                  "$\\dfrac{(x - 3)(x - 5)}{x - 4} < 0.$"
               ),
               "justificacion_md": "Factorización completa por inspección.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3.** Puntos críticos: $x = 3, 5$ (numerador) y $x = 4$ (denominador, "
                  "restricción). Ordenados: $3 < 4 < 5$."
               ),
               "justificacion_md": "Tres puntos críticos $\\Rightarrow$ cuatro intervalos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 4.** Tabla (valores de prueba: $x = 0,\\ 3{,}5,\\ 4{,}5,\\ 6$):\n\n"
                  "| Factor | $(-\\infty, 3)$ | $3$ | $(3, 4)$ | $4$ | $(4, 5)$ | $5$ | $(5, +\\infty)$ |\n"
                  "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                  "| $x - 3$ | $-$ | $0$ | $+$ | $+$ | $+$ | $+$ | $+$ |\n"
                  "| $x - 4$ | $-$ | $-$ | $-$ | $0$ | $+$ | $+$ | $+$ |\n"
                  "| $x - 5$ | $-$ | $-$ | $-$ | $-$ | $-$ | $0$ | $+$ |\n"
                  "| Cociente | $-$ | $0$ | $+$ | indef. | $-$ | $0$ | $+$ |"
               ),
               "justificacion_md": "Producto de tres signos negativos $= -$, etc.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 5.** Inecuación estricta ($< 0$): excluimos todos los puntos críticos. "
                  "Cociente negativo en $(-\\infty, 3)$ y $(4, 5)$.\n\n"
                  "$\\boxed{S = (-\\infty, 3) \\cup (4, 5).}$"
               ),
               "justificacion_md": "$x = 3$ y $x = 5$ anulan el numerador, pero la inecuación es "
                                   "estricta — quedan fuera.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Denominador siempre positivo",
          problema_md=(
              "Resuelva $\\dfrac{x^2 - 3x + 2}{x^2 + 2x + 6} < 3.$"
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1.** Pasamos todo al lado izquierdo:\n\n"
                  "$\\dfrac{x^2 - 3x + 2 - 3(x^2 + 2x + 6)}{x^2 + 2x + 6} < 0 \\iff "
                  "\\dfrac{-2x^2 - 9x - 16}{x^2 + 2x + 6} < 0.$"
               ),
               "justificacion_md": "Combinamos en una sola fracción.",
               "es_resultado": False},
              {"accion_md": (
                  "**Análisis del denominador.** $x^2 + 2x + 6$: discriminante $\\Delta = 4 - 24 = -20 < 0$. "
                  "Como el coeficiente líder es $+1 > 0$, **siempre es positivo**. No impone restricciones "
                  "y no afecta el signo de la inecuación."
               ),
               "justificacion_md": "Multiplicar por una cantidad siempre positiva preserva el sentido.",
               "es_resultado": False},
              {"accion_md": (
                  "La inecuación se reduce a $-2x^2 - 9x - 16 < 0$, equivalente a $2x^2 + 9x + 16 > 0$ "
                  "(multiplicamos por $-1$). Discriminante: $81 - 128 = -47 < 0$. Coef. líder positivo "
                  "$\\Rightarrow$ siempre positivo.\n\n"
                  "$\\boxed{S = \\mathbb{R}.}$"
               ),
               "justificacion_md": "**Atajo importante:** cuando un factor cuadrático no tiene raíces "
                                   "reales, su signo es constante (igual al del coef. líder).",
               "es_resultado": True},
          ]),

        ej(
            "Inecuación racional con numerador y denominador cuadráticos",
            "Resuelva $\\dfrac{(x - 1)(x - 2)}{(x + 1)(x + 2)} > 0.$",
            [
                "Identificá los 4 puntos críticos y ordenalos.",
                "Construí la tabla con los 4 factores como filas.",
                "Como la inecuación es estricta ($>$), excluí todos los puntos críticos.",
            ],
            (
                "Puntos críticos: $x = 1, 2$ (numerador), $x = -2, -1$ (denominador, restricciones). Ordenados: $-2 < -1 < 1 < 2$.\n\n"
                "Tabla de signos (valores de prueba: $-3, -1{,}5, 0, 1{,}5, 3$):\n\n"
                "| Factor | $(-\\infty, -2)$ | $(-2, -1)$ | $(-1, 1)$ | $(1, 2)$ | $(2, +\\infty)$ |\n"
                "|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                "| $x - 1$ | $-$ | $-$ | $-$ | $+$ | $+$ |\n"
                "| $x - 2$ | $-$ | $-$ | $-$ | $-$ | $+$ |\n"
                "| $x + 1$ | $-$ | $-$ | $+$ | $+$ | $+$ |\n"
                "| $x + 2$ | $-$ | $+$ | $+$ | $+$ | $+$ |\n"
                "| Cociente | $+$ | $-$ | $+$ | $-$ | $+$ |\n\n"
                "Inecuación estricta — excluimos puntos críticos. Cociente positivo en:\n\n"
                "$$\\boxed{S = (-\\infty, -2) \\cup (-1, 1) \\cup (2, +\\infty).}$$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica tu técnica para inecuaciones racionales:",
          preguntas=[
              {"enunciado_md": "¿Por qué NO conviene multiplicar ambos lados de $\\dfrac{x - 1}{x + 2} > 0$ por $(x + 2)$ directamente?",
               "opciones_md": [
                   "Porque desaparece el denominador y el grado cambia",
                   "Porque el signo de $(x + 2)$ depende de $x$, e invierte la desigualdad si es negativo",
                   "Porque el resultado siempre es trivial",
                   "Porque se pierden raíces complejas",
               ],
               "correcta": "B",
               "pista_md": "Multiplicar por algo de signo desconocido es inseguro en inecuaciones.",
               "explicacion_md": "Si $x + 2 < 0$ se invierte el sentido; si $x + 2 > 0$ no. Como no se sabe a priori, hay que usar tabla de signos."},
              {"enunciado_md": "¿Cuál es el conjunto solución de $\\dfrac{x - 1}{x + 2} \\leq 0$?",
               "opciones_md": ["$[-2, 1]$", "$(-2, 1]$", "$(-\\infty, -2) \\cup [1, +\\infty)$", "$[1, +\\infty)$"],
               "correcta": "B",
               "pista_md": "El cociente es $\\leq 0$ entre los puntos críticos, pero $x = -2$ está EXCLUIDO siempre.",
               "explicacion_md": "Entre $-2$ y $1$ el numerador y denominador tienen signos opuestos. $x = 1$ se incluye (numerador $0$), pero $x = -2$ NUNCA (denominador indefinido)."},
              {"enunciado_md": "El factor $(x - 3)^2$ aparece en una tabla de signos. ¿Cuál es su comportamiento?",
               "opciones_md": [
                   "Cambia de signo en $x = 3$",
                   "Es siempre $\\geq 0$ y se anula solo en $x = 3$",
                   "Es siempre negativo",
                   "Es indefinido en $x = 3$",
               ],
               "correcta": "B",
               "pista_md": "Una potencia par no cambia signo al cruzar la raíz.",
               "explicacion_md": "$(x - 3)^2 \\geq 0$ para todo real, vale $0$ solo en $x = 3$. No cambia de signo al cruzarlo."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Multiplicar ambos lados por $Q(x)$ sin conocer su signo:** error #1 en inecuaciones racionales. Si $Q(x) < 0$ se invierte el sentido. El método de tabla de signos lo evita.",
              "**Incluir el punto crítico del denominador en el conjunto solución:** **nunca**, aunque la inecuación sea $\\leq$ o $\\geq$. El cociente está indefinido ahí.",
              "**Olvidar pasar todo al mismo lado antes de factorizar:** $\\dfrac{f(x)}{g(x)} < c$ no es lo mismo que $\\dfrac{f(x) - c}{g(x)} < 0$ en general (a veces sí, según el signo de $g$).",
              "**Asumir que un factor con exponente par cambia de signo:** $(x - a)^2$ es siempre $\\geq 0$, se anula en $a$ pero no cambia de signo al cruzarlo.",
              "**No verificar si un cuadrático sin raíces reales aporta signo constante:** si $\\Delta < 0$ y $a > 0$, ese factor es siempre positivo y se puede simplificar.",
          ]),

        b("resumen",
          puntos_md=[
              "**Inecuación racional** $\\dfrac{P(x)}{Q(x)} \\square 0$: dominio excluye los ceros de $Q$.",
              "**Puntos críticos:** ceros del numerador (\"sí entran\" en $\\leq, \\geq$) y del denominador (\"nunca entran\").",
              "**Método (5 pasos):** llevar a un lado → factorizar → identificar puntos críticos → tabla de signos → escribir $S$.",
              "**Regla de alternancia:** signo cambia al cruzar punto crítico simple, no cambia con exponente par.",
              "**Cuadrático con $\\Delta < 0$:** signo constante — útil para simplificar.",
              "**Próxima lección:** inecuaciones con valor absoluto.",
          ]),
    ]
    return {
        "id": "lec-ic-2-4-inecuaciones-racionales",
        "title": "Inecuaciones racionales",
        "description": "Método de tabla de signos para resolver inecuaciones del tipo $P(x)/Q(x) \\square 0$, identificación de puntos críticos y restricciones del dominio.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# =====================================================================
# 2.5 Inecuaciones con Valor Absoluto
# =====================================================================
def lesson_2_5():
    blocks = [
        b("texto", body_md=(
            "Las **inecuaciones con valor absoluto** aparecen con frecuencia en cálculo, especialmente "
            "al trabajar con definiciones de límites, continuidad y vecindades de puntos. Comprender "
            "cómo resolverlas es una habilidad fundamental que permite describir conjuntos de "
            "$\\mathbb{R}$ de manera precisa.\n\n"
            "**Objetivos:**\n\n"
            "- Recordar las propiedades del valor absoluto relevantes para inecuaciones.\n"
            "- Aplicar las propiedades para resolver $|f(x)| \\leq a$ y $|f(x)| > a$.\n"
            "- Resolver inecuaciones con valor absoluto en **ambos miembros** mediante el método de "
            "puntos críticos e intervalos.\n"
            "- Expresar el conjunto solución en notación de intervalos."
        )),

        b("definicion",
          titulo="Las cuatro propiedades fundamentales",
          body_md=(
              "Sea $a > 0$.\n\n"
              "- **Propiedad 1** (menor o igual): $|x| \\leq a \\iff -a \\leq x \\leq a$.\n"
              "- **Propiedad 2** (estrictamente menor): $|x| < a \\iff -a < x < a$.\n"
              "- **Propiedad 3** (mayor estricta): $|x| > a \\iff x < -a$ o $x > a$.\n"
              "- **Propiedad 4** (mayor o igual): $|x| \\geq a \\iff x \\leq -a$ o $x \\geq a$.\n\n"
              "**Las propiedades 1 y 2** dan **un solo intervalo acotado** $[-a, a]$ o $(-a, a)$.\n\n"
              "**Las propiedades 3 y 4** dan **una unión de dos intervalos no acotados**.\n\n"
              "Estas cuatro propiedades permiten **eliminar los valores absolutos** y transformar la "
              "inecuación original en una o varias inecuaciones lineales más simples."
          )),

        b("ejemplo_resuelto",
          titulo="Inecuación tipo $|f(x)| \\leq a$",
          problema_md=(
              "Resuelva $|2x + 3| \\leq 6$."
          ),
          pasos=[
              {"accion_md": (
                  "Aplicando la Propiedad 1 con $a = 6$:\n\n"
                  "$|2x + 3| \\leq 6 \\iff -6 \\leq 2x + 3 \\leq 6.$"
               ),
               "justificacion_md": "Convertimos en una doble desigualdad.",
               "es_resultado": False},
              {"accion_md": (
                  "Restando $3$ en toda la cadena: $-9 \\leq 2x \\leq 3.$\n\n"
                  "Dividiendo por $2 > 0$: $-\\dfrac{9}{2} \\leq x \\leq \\dfrac{3}{2}.$\n\n"
                  "$\\boxed{S = \\left[ -\\dfrac{9}{2},\\ \\dfrac{3}{2} \\right].}$"
               ),
               "justificacion_md": "Operaciones reversibles que preservan el orden.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inecuación tipo $|f(x)| > a$",
          problema_md=(
              "Resuelva $|5x - 8| > 4$."
          ),
          pasos=[
              {"accion_md": (
                  "Aplicando la Propiedad 3 con $a = 4$:\n\n"
                  "$|5x - 8| > 4 \\iff 5x - 8 < -4 \\;\\text{o}\\; 5x - 8 > 4.$"
               ),
               "justificacion_md": "Convertimos en dos casos disjuntos.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolvemos cada caso por separado:\n\n"
                  "$5x < 4 \\;\\text{o}\\; 5x > 12 \\iff x < \\dfrac{4}{5} \\;\\text{o}\\; x > \\dfrac{12}{5}.$\n\n"
                  "$\\boxed{S = \\left( -\\infty,\\ \\dfrac{4}{5} \\right) \\cup \\left( \\dfrac{12}{5},\\ +\\infty \\right).}$"
               ),
               "justificacion_md": "Unión de los dos casos.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Método para inecuaciones con valor absoluto en ambos miembros",
          body_md=(
              "Cuando la inecuación involucra valores absolutos en **ambos lados**, como $|f(x)| < |g(x)|$ "
              "o $|f(x)| \\geq |g(x)|$, el método directo no basta. Se usa el **método de puntos "
              "críticos e intervalos**:\n\n"
              "1. **Identificar los puntos críticos:** valores de $x$ para los cuales cada expresión "
              "dentro de un valor absoluto se anula.\n"
              "2. **Ordenar los puntos críticos** y formar los intervalos en que dividen $\\mathbb{R}$.\n"
              "3. **Analizar cada intervalo:** determinar el signo de cada expresión bajo valor "
              "absoluto y reemplazar el valor absoluto por su definición. Eso elimina los $|\\cdot|$.\n"
              "4. **Resolver** la inecuación lineal resultante en cada intervalo, **intersectando** la "
              "solución con el intervalo de trabajo.\n"
              "5. **Unir** todas las soluciones parciales para obtener el conjunto solución final.\n\n"
              "**Truco alternativo (cuando ambos lados son no negativos):** elevar al cuadrado preserva "
              "el orden y elimina los valores absolutos."
          )),

        b("ejemplo_resuelto",
          titulo="Valor absoluto en ambos lados",
          problema_md=(
              "Resuelva $2|x| < |x - 1|$."
          ),
          pasos=[
              {"accion_md": (
                  "**Puntos críticos:** $x = 0$ (anula $|x|$) y $x = 1$ (anula $|x - 1|$). Ordenados: "
                  "$0 < 1$. Tres intervalos: $(-\\infty, 0]$, $(0, 1]$, $(1, +\\infty)$."
               ),
               "justificacion_md": "Donde cada expresión cambia de signo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 1: $x \\in (-\\infty, 0]$.** $x \\leq 0$ y $x - 1 < 0$, luego $|x| = -x$ y "
                  "$|x - 1| = -(x - 1)$. La desigualdad queda:\n\n"
                  "$2(-x) < -(x - 1) \\iff -2x < -x + 1 \\iff -x < 1 \\iff x > -1.$\n\n"
                  "Intersectando con $(-\\infty, 0]$: $S_1 = (-1, 0]$."
               ),
               "justificacion_md": "Reemplazamos los $|\\cdot|$ y resolvemos lineal.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 2: $x \\in (0, 1]$.** $x > 0$ y $x - 1 \\leq 0$, luego $|x| = x$ y "
                  "$|x - 1| = -(x - 1)$. La desigualdad:\n\n"
                  "$2x < -(x - 1) \\iff 2x < -x + 1 \\iff 3x < 1 \\iff x < \\dfrac{1}{3}.$\n\n"
                  "Intersectando con $(0, 1]$: $S_2 = \\left( 0,\\ \\dfrac{1}{3} \\right)$."
               ),
               "justificacion_md": "Otro caso con el signo cambiado.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 3: $x \\in (1, +\\infty)$.** Ambas expresiones positivas: $|x| = x$, $|x - 1| = x - 1$. "
                  "La desigualdad: $2x < x - 1 \\iff x < -1$, incompatible con $x > 1$. $S_3 = \\emptyset$."
               ),
               "justificacion_md": "Cuando la solución algebraica no intersecta con el intervalo, no aporta nada.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conjunto solución final** (unión):\n\n"
                  "$\\boxed{S = S_1 \\cup S_2 \\cup S_3 = (-1, 0] \\cup \\left( 0, \\dfrac{1}{3} \\right) "
                  "= \\left( -1,\\ \\dfrac{1}{3} \\right).}$"
               ),
               "justificacion_md": "Unión simplifica porque los intervalos son contiguos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inecuación $|x - 4| \\geq |2x - 1|$",
          problema_md=(
              "Resuelva $|x - 4| \\geq |2x - 1|$."
          ),
          pasos=[
              {"accion_md": (
                  "**Puntos críticos:** $x = 4$ y $x = \\dfrac{1}{2}$. Ordenados: $\\dfrac{1}{2} < 4$. "
                  "Tres intervalos: $\\left( -\\infty, \\tfrac{1}{2} \\right]$, $\\left( \\tfrac{1}{2}, 4 \\right]$, $(4, +\\infty)$."
               ),
               "justificacion_md": "Donde cada expresión bajo $|\\cdot|$ se anula.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 1: $x \\leq \\dfrac{1}{2}$.** Ambas expresiones $\\leq 0$: $|x - 4| = -(x - 4)$, "
                  "$|2x - 1| = -(2x - 1)$. La desigualdad:\n\n"
                  "$-(x - 4) \\geq -(2x - 1) \\iff -x + 4 \\geq -2x + 1 \\iff x \\geq -3.$\n\n"
                  "Intersectando con $\\left( -\\infty, \\tfrac{1}{2} \\right]$: $S_1 = \\left[ -3, \\tfrac{1}{2} \\right]$."
               ),
               "justificacion_md": "Intersección con el intervalo de trabajo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 2: $\\dfrac{1}{2} < x \\leq 4$.** $x - 4 \\leq 0$ y $2x - 1 > 0$: $|x - 4| = -(x - 4)$, "
                  "$|2x - 1| = 2x - 1$. La desigualdad:\n\n"
                  "$-(x - 4) \\geq 2x - 1 \\iff -x + 4 \\geq 2x - 1 \\iff 5 \\geq 3x \\iff x \\leq \\dfrac{5}{3}.$\n\n"
                  "Intersectando con $\\left( \\tfrac{1}{2}, 4 \\right]$: $S_2 = \\left( \\tfrac{1}{2},\\ \\tfrac{5}{3} \\right]$."
               ),
               "justificacion_md": "Caso intermedio con signos mixtos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 3: $x > 4$.** Ambas expresiones positivas: $|x - 4| = x - 4$, $|2x - 1| = 2x - 1$.\n\n"
                  "$x - 4 \\geq 2x - 1 \\iff -3 \\geq x$, incompatible con $x > 4$. $S_3 = \\emptyset$."
               ),
               "justificacion_md": "No aporta soluciones.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\boxed{S = S_1 \\cup S_2 \\cup S_3 = \\left[ -3,\\ \\tfrac{1}{2} \\right] \\cup "
                  "\\left( \\tfrac{1}{2},\\ \\tfrac{5}{3} \\right] = \\left[ -3,\\ \\tfrac{5}{3} \\right].}$"
               ),
               "justificacion_md": "Los intervalos contiguos se fusionan.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Resumen estratégico — qué método usar.**\n\n"
            "| Tipo | Forma | Método | Solución típica |\n"
            "|:---:|:---:|:---:|:---|\n"
            "| 1 | $|f(x)| \\leq a$ o $< a$ | Propiedad 1 o 2 directa | Intervalo acotado |\n"
            "| 2 | $|f(x)| \\geq a$ o $> a$ | Propiedad 3 o 4 directa | Unión de dos no acotados |\n"
            "| 3 | $|f(x)| \\square |g(x)|$ | Puntos críticos por casos | Depende |\n\n"
            "Para **Tipo 3**, una alternativa es elevar al cuadrado: $|f| < |g| \\iff f^2 < g^2$ "
            "(válido porque ambos lados son no negativos). A veces es más rápido."
        )),

        ej(
            "Inecuación tipo doble desigualdad",
            "Resuelva $1 < |x - 2| \\leq 5$.",
            [
                "Esta es la intersección de dos inecuaciones: $|x-2| > 1$ y $|x-2| \\leq 5$.",
                "Resolvé cada una por separado con las propiedades.",
                "Intersectá los conjuntos solución.",
            ],
            (
                "**Inecuación 1:** $|x - 2| > 1 \\iff x - 2 < -1$ o $x - 2 > 1 \\iff x < 1$ o $x > 3$. Es decir, $S_1 = (-\\infty, 1) \\cup (3, +\\infty)$.\n\n"
                "**Inecuación 2:** $|x - 2| \\leq 5 \\iff -5 \\leq x - 2 \\leq 5 \\iff -3 \\leq x \\leq 7$. Es decir, $S_2 = [-3, 7]$.\n\n"
                "**Intersección:**\n\n"
                "$$S = S_1 \\cap S_2 = \\big([-3, 1) \\cup (3, 7]\\big).$$\n\n"
                "$\\boxed{S = [-3, 1) \\cup (3, 7].}$"
            ),
        ),

        fig(
            "Diagrama en dos paneles que ilustra inecuaciones con valor absoluto sobre la recta real. "
            "Panel izquierdo: 'Caso |x - c| < r' — recta horizontal con un punto central c marcado en "
            "ámbar #f59e0b, y el intervalo abierto (c - r, c + r) sombreado en teal #06b6d4 con bordes "
            "punteados; etiqueta 'distancia a c menor que r'. Panel derecho: 'Caso |x - c| > r' — misma "
            "recta con dos rayos sombreados teal a la izquierda de c - r y a la derecha de c + r, "
            "punto c en ámbar; etiqueta 'distancia a c mayor que r'. Ambos paneles con marcas y números. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica las inecuaciones con valor absoluto:",
          preguntas=[
              {"enunciado_md": "¿Cuál es la solución de $|x - 4| < 3$?",
               "opciones_md": ["$x < 1$ o $x > 7$", "$1 < x < 7$", "$-3 < x < 3$", "$x < -3$ o $x > 3$"],
               "correcta": "B",
               "pista_md": "$|x - c| < r \\iff c - r < x < c + r$.",
               "explicacion_md": "Por la propiedad 1: $-3 < x - 4 < 3$, es decir $1 < x < 7$. Es un entorno de centro $4$ y radio $3$."},
              {"enunciado_md": "¿Cuál es la solución de $|2x + 1| \\geq 5$?",
               "opciones_md": [
                   "$-3 \\leq x \\leq 2$",
                   "$x \\leq -3$ o $x \\geq 2$",
                   "$-2 \\leq x \\leq 3$",
                   "$x \\leq -2$ o $x \\geq 3$",
               ],
               "correcta": "B",
               "pista_md": "$|f| \\geq a \\iff f \\leq -a$ o $f \\geq a$.",
               "explicacion_md": "$2x + 1 \\leq -5 \\Rightarrow x \\leq -3$, o $2x + 1 \\geq 5 \\Rightarrow x \\geq 2$. La solución son las dos colas."},
              {"enunciado_md": "¿Cuál es la solución de $|x + 2| < -1$?",
               "opciones_md": ["$\\mathbb{R}$", "$\\emptyset$", "$x = -2$", "$x < -3$"],
               "correcta": "B",
               "pista_md": "El valor absoluto siempre es $\\geq 0$.",
               "explicacion_md": "Como $|x + 2| \\geq 0 > -1$ para todo $x$, ningún real cumple la inecuación. $S = \\emptyset$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Aplicar la Propiedad 1 a $|f(x)| > a$:** la propiedad correcta es la 3 (o 4). $|x| > 5$ NO es $-5 < x < 5$ (es lo opuesto).",
              "**Olvidar intersectar con el intervalo de trabajo en cada caso:** $S_i$ debe estar contenido en el intervalo del caso, no es la solución algebraica cruda.",
              "**Resolver $|f(x)| < a$ con $a < 0$:** simplemente $S = \\emptyset$ (valor absoluto es siempre $\\geq 0$).",
              "**Resolver $|f(x)| > a$ con $a < 0$:** $S = \\mathbb{R}$ (siempre se cumple, asumiendo $f$ definida).",
              "**Elevar al cuadrado sin asegurar no negatividad de ambos lados:** preserva el orden solo si ambos $\\geq 0$.",
          ]),

        b("resumen",
          puntos_md=[
              "**4 propiedades fundamentales** para eliminar valores absolutos: 1-2 dan intervalo acotado, 3-4 dan unión de dos no acotados.",
              "**Inecuaciones con $|\\cdot|$ en ambos lados:** método de puntos críticos por casos.",
              "**En cada caso:** reemplazar $|\\cdot|$ según el signo, resolver lineal, **intersectar con el intervalo del caso**.",
              "**Truco alternativo:** elevar al cuadrado si ambos lados son no negativos.",
              "**Conjunto solución final:** unión de las soluciones parciales.",
              "**Próxima lección:** inecuaciones con raíces — control de dominio.",
          ]),
    ]
    return {
        "id": "lec-ic-2-5-inecuaciones-valor-absoluto",
        "title": "Inecuaciones con valor absoluto",
        "description": "Cuatro propiedades fundamentales para inecuaciones tipo $|f(x)| \\square a$, y método de puntos críticos para inecuaciones con valor absoluto en ambos miembros.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 5,
    }


# =====================================================================
# 2.6 Inecuaciones con Raíces
# =====================================================================
def lesson_2_6():
    blocks = [
        b("texto", body_md=(
            "Las **inecuaciones con raíces** son la última pieza del rompecabezas algebraico previo "
            "al cálculo. Aparecen al trabajar con expresiones que involucran raíces cuadradas u otras "
            "raíces de índice par, donde debemos tener especial cuidado con el **dominio de "
            "definición**, ya que las raíces imponen restricciones sobre los valores que puede tomar "
            "la variable.\n\n"
            "**Objetivos:**\n\n"
            "- Comprender la **definición de raíz $n$-ésima** y sus condiciones de existencia.\n"
            "- Calcular el **dominio** de expresiones con raíces para establecer restricciones.\n"
            "- Resolver inecuaciones con raíces cuadradas mediante **análisis por casos** y "
            "**elevación al cuadrado**.\n"
            "- Interpretar el **conjunto solución** como intersección del dominio con la solución "
            "algebraica."
        )),

        b("definicion",
          titulo="Raíz $n$-ésima",
          body_md=(
              "La raíz $n$-ésima de un real $a$ se define según la paridad de $n$ y el signo de $a$:\n\n"
              "- **Caso 1:** si $a > 0$ y $n \\in \\mathbb{N}$, $\\sqrt[n]{a}$ es el **único** $b > 0$ "
              "tal que $b^n = a$.\n"
              "- **Caso 2:** si $a < 0$ y $n$ es **impar**, $\\sqrt[n]{a}$ es el único $b < 0$ tal "
              "que $b^n = a$.\n"
              "- **Caso 3:** si $a = 0$, $\\sqrt[n]{0} = 0$ para todo $n$.\n\n"
              "Llamamos $n$ el **índice** de la raíz y $a$ la **cantidad subradical**. La relación "
              "fundamental es:\n\n"
              "$$\\sqrt[n]{a} = b \\iff b^n = a.$$"
          )),

        b("definicion",
          titulo="Observaciones esenciales sobre el dominio",
          body_md=(
              "Las siguientes observaciones son **esenciales** para trabajar correctamente con "
              "inecuaciones con raíces, pues determinan cuándo una expresión radical está bien definida "
              "en los reales.\n\n"
              "- **Obs. 1:** Si $a < 0$ y $n$ es **par**, entonces $\\sqrt[n]{a} \\notin \\mathbb{R}$ "
              "(es complejo). Conclusión: $a < 0$ y $n$ par $\\Rightarrow \\sqrt[n]{a} \\notin \\mathbb{R}$.\n"
              "- **Obs. 2:** Si $n$ es **par**, entonces $\\sqrt[n]{a}$ está bien definida como real "
              "si y solo si $a \\geq 0$.\n"
              "- **Obs. 3:** Si $n$ es **par** y $a \\geq 0$, entonces $\\sqrt[n]{a} \\geq 0$. Es decir, "
              "la raíz de índice par de un no negativo **siempre es no negativa**.\n\n"
              "Esta última observación es la base del método de resolución por casos: cuando un lado "
              "de la inecuación es una raíz de índice par, sabemos que es **no negativo de antemano**."
          )),

        b("definicion",
          titulo="Método general — 3 etapas",
          body_md=(
              "El procedimiento para resolver una inecuación con raíces cuadradas consta de **tres "
              "etapas** claramente diferenciadas. Seguirlas en orden es fundamental para no perder "
              "soluciones ni incluir valores espurios.\n\n"
              "**Etapa 1 — Determinar el dominio (restricción).** Toda expresión $\\sqrt{f(x)}$ exige "
              "$f(x) \\geq 0$. Si la inecuación tiene varias raíces, cada una impone su propia "
              "restricción. El **conjunto de restricciones** se intersecta para obtener el **dominio "
              "$R$**, donde la inecuación tiene sentido. Cualquier solución final debe pertenecer a $R$.\n\n"
              "**Etapa 2 — Análisis por casos según el signo.** Dado que $\\sqrt{g(x)} \\geq 0$ siempre, "
              "si la inecuación es $h(x) > \\sqrt{g(x)}$:\n\n"
              "- **Caso 1:** $h(x) \\leq 0$. La desigualdad estricta $h(x) > \\sqrt{g(x)} \\geq 0$ es "
              "imposible. Conjunto solución de este caso: vacío.\n"
              "- **Caso 2:** $h(x) > 0$. Podemos elevar al cuadrado preservando la equivalencia, "
              "obteniendo $[h(x)]^2 > g(x)$, una **inecuación polinomial** estándar.\n\n"
              "**Etapa 3 — Intersección con el dominio.** Una vez obtenidos los conjuntos $S_1$ y $S_2$ "
              "de cada caso, el conjunto solución final es\n\n"
              "$$S = R \\cap (S_1 \\cup S_2).$$"
          )),

        b("intuicion", body_md=(
            "**Por qué hay que analizar el signo antes de elevar al cuadrado.** La equivalencia\n\n"
            "$$A > B \\iff A^2 > B^2$$\n\n"
            "**solo vale cuando $A \\geq 0$ y $B \\geq 0$**. Si alguno puede ser negativo, la equivalencia "
            "se rompe (ej: $-3 < 2$ pero $9 > 4$). Por eso, antes de elevar al cuadrado, debemos "
            "**garantizar la no negatividad** de ambos lados — y eso es lo que hace el análisis por casos."
        )),

        fig(
            "Diagrama de flujo vertical en tres etapas para resolver una inecuación con raíz como "
            "h(x) > √g(x). Etapa 1 (caja teal #06b6d4): 'DOMINIO: g(x) ≥ 0. Resolver para obtener R'. "
            "Flecha hacia abajo. Etapa 2 (caja partida en dos): a la izquierda 'Caso 1: h(x) ≤ 0' con "
            "subtexto 'desigualdad imposible, S₁ = ∅' (color gris); a la derecha 'Caso 2: h(x) > 0' "
            "con subtexto 'elevar al cuadrado: [h(x)]² > g(x), resolver, obtener S₂' (color teal). "
            "Flecha hacia abajo desde ambos cuadros. Etapa 3 (caja ámbar #f59e0b): 'INTERSECTAR con "
            "dominio: S = R ∩ (S₁ ∪ S₂)'. Flechas etiquetadas. Título: 'Método general para "
            "inecuaciones con raíces — 3 etapas'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Inecuación con un lado lineal y otro radical",
          problema_md=(
              "Resuelva $2x - 1 > \\sqrt{x^2 - 3x}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Etapa 1 — Dominio.** $\\sqrt{x^2 - 3x}$ existe si $x^2 - 3x \\geq 0$. "
                  "Factorizando: $x(x - 3) \\geq 0 \\iff x \\leq 0$ o $x \\geq 3$.\n\n"
                  "$R = (-\\infty, 0] \\cup [3, +\\infty).$"
               ),
               "justificacion_md": "Tabla de signos del producto $x(x-3)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Etapa 2 — Análisis por casos.**\n\n"
                  "**Caso 1:** $x \\leq \\dfrac{1}{2}$. Entonces $2x - 1 \\leq 0$ y "
                  "$\\sqrt{x^2 - 3x} \\geq 0$, por transitividad $2x - 1 \\leq 0 \\leq \\sqrt{x^2 - 3x}$. "
                  "La desigualdad **estricta** $2x - 1 > \\sqrt{x^2 - 3x}$ es imposible. $S_1 = \\emptyset$."
               ),
               "justificacion_md": "Lado izquierdo no positivo, lado derecho no negativo: nunca puede "
                                   "ser estrictamente mayor.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 2:** $x > \\dfrac{1}{2}$. Entonces $2x - 1 > 0$ y podemos elevar al cuadrado "
                  "preservando la equivalencia:\n\n"
                  "$2x - 1 > \\sqrt{x^2 - 3x} \\iff (2x - 1)^2 > x^2 - 3x.$\n\n"
                  "Expandiendo: $4x^2 - 4x + 1 > x^2 - 3x \\iff 3x^2 - x + 1 > 0$."
               ),
               "justificacion_md": "Ambos lados positivos $\\Rightarrow$ elevar al cuadrado preserva.",
               "es_resultado": False},
              {"accion_md": (
                  "**Análisis del trinomio $3x^2 - x + 1$.** $\\Delta = 1 - 12 = -11 < 0$ y coef. "
                  "líder $3 > 0$, luego es **siempre positivo**. La condición se cumple para todo "
                  "$x \\in \\mathbb{R}$, en particular para $x > \\dfrac{1}{2}$:\n\n"
                  "$S_2 = \\left( \\dfrac{1}{2},\\ +\\infty \\right).$"
               ),
               "justificacion_md": "Cuadrático con $\\Delta < 0$ y $a > 0$ es siempre positivo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Etapa 3 — Intersección con el dominio.**\n\n"
                  "$S = R \\cap (S_1 \\cup S_2) = \\big[ (-\\infty, 0] \\cup [3, +\\infty) \\big] \\cap "
                  "\\left( \\dfrac{1}{2},\\ +\\infty \\right) = \\boxed{[3, +\\infty).}$"
               ),
               "justificacion_md": "**No te olvides de intersectar con el dominio** — sin esto la "
                                   "respuesta es incorrecta.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inecuación con dos raíces",
          problema_md=(
              "Resuelva $\\sqrt{x^2 + x - 2} - 2\\sqrt{x^2 - 1} \\geq 0$, es decir, "
              "$\\sqrt{x^2 + x - 2} \\geq 2\\sqrt{x^2 - 1}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Etapa 1 — Dominio.** Dos raíces, dos condiciones:\n\n"
                  "- (i) $x^2 + x - 2 \\geq 0$. Factorizando: $(x+2)(x-1) \\geq 0 \\iff x \\leq -2$ o $x \\geq 1$.\n"
                  "- (ii) $x^2 - 1 \\geq 0$. Factorizando: $(x+1)(x-1) \\geq 0 \\iff x \\leq -1$ o $x \\geq 1$.\n\n"
                  "Intersección: $R = (-\\infty, -2] \\cup [1, +\\infty)$."
               ),
               "justificacion_md": "Ambas condiciones deben cumplirse simultáneamente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Etapa 2.** Sobre $R$, **ambos lados son no negativos**, así que podemos elevar "
                  "al cuadrado directamente:\n\n"
                  "$x^2 + x - 2 \\geq 4(x^2 - 1) \\iff x^2 + x - 2 \\geq 4x^2 - 4.$\n\n"
                  "Reorganizando: $0 \\geq 3x^2 - x - 2 \\iff 3x^2 - x - 2 \\leq 0$."
               ),
               "justificacion_md": "No hay análisis por casos porque ambos lados son raíces (no negativos) por construcción.",
               "es_resultado": False},
              {"accion_md": (
                  "**Raíces de $3x^2 - x - 2$:** $x = \\dfrac{1 \\pm \\sqrt{1 + 24}}{6} = \\dfrac{1 \\pm 5}{6}$, "
                  "es decir $x = 1$ y $x = -\\dfrac{2}{3}$. Coef. líder $3 > 0$, así que el trinomio "
                  "es $\\leq 0$ **entre** las raíces:\n\n"
                  "$3x^2 - x - 2 \\leq 0 \\iff x \\in \\left[ -\\dfrac{2}{3},\\ 1 \\right].$"
               ),
               "justificacion_md": "Caso 1b de la lección anterior.",
               "es_resultado": False},
              {"accion_md": (
                  "**Etapa 3 — Intersección con $R$:**\n\n"
                  "$S = \\left[ -\\dfrac{2}{3},\\ 1 \\right] \\cap \\big[ (-\\infty, -2] \\cup [1, +\\infty) \\big] = \\{1\\}.$\n\n"
                  "El único valor que satisface simultáneamente el dominio y la inecuación algebraica es $x = 1$.\n\n"
                  "$\\boxed{S = \\{1\\}.}$"
               ),
               "justificacion_md": "**El dominio cambió completamente la respuesta** — sin él el "
                                   "intervalo $\\left[ -\\tfrac{2}{3}, 1 \\right]$ habría sido la "
                                   "respuesta espuria.",
               "es_resultado": True},
          ]),

        ej(
            "Dominio de una función con raíz",
            "Determine el dominio de $f(x) = \\dfrac{1}{\\sqrt{x^2 - 3x + 2}}$ y exprésalo como unión de intervalos.",
            [
                "El denominador no puede ser cero, luego $\\sqrt{x^2 - 3x + 2} \\neq 0$, es decir $x^2 - 3x + 2 > 0$ (estricto).",
                "Factorizá el trinomio.",
                "Resolvé la inecuación cuadrática estricta.",
            ],
            (
                "Necesitamos $x^2 - 3x + 2 > 0$ (estricto, porque está en el denominador).\n\n"
                "Factorizando: $x^2 - 3x + 2 = (x - 1)(x - 2)$. Raíces $1, 2$. Coef. líder $1 > 0$, así que el trinomio es positivo **fuera** del intervalo entre raíces:\n\n"
                "$$\\boxed{\\text{Dom}(f) = (-\\infty, 1) \\cup (2, +\\infty).}$$"
            ),
        ),

        b("verificacion",
          intro_md="Verifica las inecuaciones con raíces:",
          preguntas=[
              {"enunciado_md": "¿Cuál es el dominio (restricción) para resolver $\\sqrt{x - 5} \\geq 2$?",
               "opciones_md": ["$x \\geq 0$", "$x \\geq 5$", "$x \\geq 2$", "Todo $\\mathbb{R}$"],
               "correcta": "B",
               "pista_md": "Para que $\\sqrt{f(x)}$ exista (índice par), $f(x) \\geq 0$.",
               "explicacion_md": "El radicando debe ser $\\geq 0$: $x - 5 \\geq 0 \\iff x \\geq 5$. Cualquier solución debe estar en este dominio."},
              {"enunciado_md": "¿Por qué al resolver $h(x) > \\sqrt{g(x)}$ es válido elevar al cuadrado solo si $h(x) > 0$?",
               "opciones_md": [
                   "Porque la raíz tiene dominio restringido",
                   "Porque $A > B \\iff A^2 > B^2$ vale solo si ambos lados son no negativos",
                   "Porque elevar al cuadrado siempre invierte la desigualdad",
                   "Porque el cuadrado pierde información del signo",
               ],
               "correcta": "B",
               "pista_md": "Si $h(x) < 0$, ya $h(x) < \\sqrt{g(x)} \\geq 0$, así que se descarta de antemano.",
               "explicacion_md": "Elevar al cuadrado preserva el orden solo entre cantidades no negativas. Si $h(x) < 0$ no puede superar a una raíz."},
              {"enunciado_md": "¿Por qué las raíces de índice impar (como $\\sqrt[3]{x}$) NO requieren restricciones de dominio?",
               "opciones_md": [
                   "Porque son siempre positivas",
                   "Porque están definidas para todo $x \\in \\mathbb{R}$",
                   "Porque no se pueden elevar al cubo",
                   "Porque siempre dan resultado entero",
               ],
               "correcta": "B",
               "pista_md": "$\\sqrt[3]{-8} = -2$ es válido en $\\mathbb{R}$.",
               "explicacion_md": "Las raíces de índice impar admiten radicandos negativos, así que están definidas en todo $\\mathbb{R}$ y se puede elevar a la potencia impar sin perder soluciones."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Olvidar el dominio:** error #1. Resolver algebraicamente y omitir intersectar con $R$ lleva a incluir valores espurios donde la raíz no está definida.",
              "**Elevar al cuadrado sin verificar el signo:** elevar al cuadrado ambos lados de $h(x) > \\sqrt{g(x)}$ sin garantizar $h(x) > 0$ puede generar soluciones falsas — la equivalencia $A > B \\iff A^2 > B^2$ solo vale para $A, B \\geq 0$.",
              "**Confundir restricción con solución:** el dominio $R$ no es el conjunto solución; es el conjunto de valores **candidatos**. La solución final es un subconjunto de $R$.",
              "**Perder la intersección en el Caso 2:** en el Caso 2 trabajás bajo la hipótesis $h(x) > 0$. Al reportar $S_2$ hay que incluir esta condición antes de intersectar con $R$.",
              "**Aplicar el método a raíces de índice impar:** raíces de índice impar están definidas para todo real, no necesitan análisis de dominio. El método se simplifica porque puedes elevar a la $n$ directamente.",
          ]),

        b("resumen",
          puntos_md=[
              "**Raíz de índice par** existe en $\\mathbb{R}$ solo si el subradical es $\\geq 0$.",
              "**Raíz de índice par** de un no negativo es siempre no negativa.",
              "**Método (3 etapas):** dominio $R$ → análisis por casos → intersección con $R$.",
              "**Caso 1** (lado opuesto $\\leq 0$): solución vacía si la inecuación es estricta y el lado de la raíz $\\geq 0$.",
              "**Caso 2** (lado opuesto $> 0$): elevar al cuadrado preserva la equivalencia.",
              "**Conjunto solución final:** $S = R \\cap (S_1 \\cup S_2)$.",
              "**Próximo capítulo:** Funciones Reales — entrada formal al estudio de funciones.",
          ]),
    ]
    return {
        "id": "lec-ic-2-6-inecuaciones-raices",
        "title": "Inecuaciones con raíces",
        "description": "Definición de raíz $n$-ésima, control del dominio, método de tres etapas (dominio, análisis por casos, intersección) para inecuaciones radicales.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 6,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "intro-calculo"

    # Curso: upsert (preserva created_at, actualiza modules_count si cambió).
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

    chapter_id = "ch-ic-desigualdades"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Desigualdades",
        "description": (
            "Axiomas de orden, valor absoluto, intervalos, inecuaciones de primer y segundo grado, "
            "inecuaciones racionales, con valor absoluto y con raíces."
        ),
        "order": 2,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_2_1, lesson_2_2, lesson_2_3, lesson_2_4, lesson_2_5, lesson_2_6]
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
    print(f"✅ Capítulo 2 — Desigualdades listo: {len(builders)} lecciones, {total_blocks} bloques, "
          f"{total_figs} figuras pendientes.")
    print()
    print("URLs locales para verificar:")
    print(f"  http://localhost:3007/courses/{course_id}")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
