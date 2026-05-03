"""
Seed del curso Introducción al Cálculo — Capítulo 5: Funciones Exponencial y Logarítmica.
3 lecciones:
  5.1 Función exponencial (definición vía límite, desigualdad fundamental, propiedades)
  5.2 Función logarítmica (logaritmo natural, propiedades algebraicas, $a^x$, $\\log_a$, aplicaciones)
  5.3 Ecuaciones exponenciales y logarítmicas (4 métodos: igualar base, cambio de variable,
      logaritmo, forma exponencial / igualar argumento)

ENFOQUE: cierre del curso. Construcción rigurosa de $e^x$ desde sucesiones, su inversa $\\ln$,
extensión a $a^x$ y $\\log_a$, y métodos sistemáticos para resolver ecuaciones. Aplicaciones a
crecimiento exponencial y decaimiento radiactivo.

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
# 5.1 Función exponencial
# =====================================================================
def lesson_5_1():
    blocks = [
        b("texto", body_md=(
            "La **función exponencial** es una de las funciones más importantes del análisis matemático "
            "y tiene aplicaciones fundamentales en biología, física, economía e ingeniería. Su construcción "
            "rigurosa parte de la noción de **límite de sucesiones** (cap. 4), conectando de manera profunda "
            "el análisis de sucesiones con el estudio de funciones reales.\n\n"
            "**Objetivos:**\n\n"
            "- Definir $e^x$ como **límite de la sucesión** $(1 + x/n)^n$.\n"
            "- Demostrar la **desigualdad fundamental** $e^x \\geq 1 + x$.\n"
            "- Establecer **positividad**, **crecimiento estricto** e **inyectividad**.\n"
            "- Identificar dominio $\\mathbb{R}$ y recorrido $(0, +\\infty)$."
        )),

        b("definicion",
          titulo="Recordatorio: el número $e$",
          body_md=(
              "El **número de Euler** $e$ se definió en cap. 4 como\n\n"
              "$$e = \\lim_{n\\to\\infty} \\left(1 + \\dfrac{1}{n}\\right)^n.$$\n\n"
              "Su construcción usó el teorema de sucesiones monótonas y acotadas: la sucesión "
              "$(1 + 1/n)^n$ es estrictamente creciente y acotada por $3$. La pregunta natural es: ¿qué "
              "ocurre si reemplazamos el $1$ por un real arbitrario $x$?"
          )),

        b("teorema",
          enunciado_md=(
              "**Convergencia de $(1 + x/n)^n$.** Para todo $x \\in \\mathbb{R}$, la sucesión\n\n"
              "$$x_n = \\left(1 + \\dfrac{x}{n}\\right)^n$$\n\n"
              "es **convergente**. Más precisamente, $\\{x_n\\}$ es creciente y acotada superiormente "
              "a partir de cierto $n > -x$.\n\n"
              "La demostración usa la **desigualdad de Bernoulli** ($(1+x)^n \\geq 1 + nx$ para $1+x > 0$) "
              "y el principio de Arquímedes. Garantiza que para cada $x \\in \\mathbb{R}$, el límite "
              "$\\lim_{n\\to\\infty} (1 + x/n)^n$ está bien definido como número real."
          )),

        b("definicion",
          titulo="Función exponencial",
          body_md=(
              "La **función exponencial** $\\exp: \\mathbb{R} \\to \\mathbb{R}$ se define por\n\n"
              "$$e^x = \\lim_{n\\to\\infty} \\left(1 + \\dfrac{x}{n}\\right)^n.$$\n\n"
              "Cuando $x = 1$, esta definición recupera $e$. La notación $e^x$ se justifica porque la "
              "función satisface **todas las propiedades algebraicas de una potencia**.\n\n"
              "**Dominio:** $\\text{Dom}(e^x) = \\mathbb{R}$. La sucesión converge para todo $x$ real, "
              "luego $e^x$ está definido para cualquier número real."
          )),

        b("teorema",
          enunciado_md=(
              "**Desigualdad fundamental.** Para todo $x \\in \\mathbb{R}$ se cumple\n\n"
              "$$\\boxed{e^x \\geq 1 + x,}$$\n\n"
              "con igualdad si y solo si $x = 0$.\n\n"
              "**Demostración.** Como la sucesión $\\{x_n\\}$ es creciente a partir de $n > -x$ y converge "
              "a $e^x$, se tiene $e^x \\geq x_n$ para todo $n$ suficientemente grande. Aplicando Bernoulli "
              "con $x/n$ (con $1 + x/n > 0$):\n\n"
              "$e^x \\geq \\left(1 + \\dfrac{x}{n}\\right)^n \\geq 1 + n \\cdot \\dfrac{x}{n} = 1 + x. \\quad\\square$"
          )),

        b("intuicion", body_md=(
            "**Interpretación geométrica.** La recta $y = 1 + x$ es **tangente** a la curva $y = e^x$ "
            "en el punto $(0, 1)$. La desigualdad fundamental dice que la curva exponencial siempre "
            "queda **arriba o sobre** su recta tangente en el origen, tocándola únicamente en $(0, 1)$. "
            "Esta propiedad refleja que la exponencial es una función **convexa**."
        )),

        fig(
            "Plano cartesiano con la curva y = e^x graficada en color teal #06b6d4 (creciente "
            "rápido, pasando por (0,1), (1, 2.72), (2, 7.39)). Una recta y = 1 + x graficada "
            "en color ámbar #f59e0b (línea recta de pendiente 1, pasando por (0,1) y (-1, 0)). "
            "Las dos curvas se tocan exactamente en el punto (0, 1) (resaltado con un círculo "
            "y etiqueta '(0, 1) único punto de contacto'). En las regiones x < 0 y x > 0, la "
            "exponencial queda claramente por encima de la recta. Sombreado suave teal entre "
            "las dos curvas para enfatizar e^x ≥ 1 + x. Anotación en x=1: 'e ≈ 2.72 vs "
            "1+1 = 2'. Asíntota y = 0 (eje x) marcada como línea punteada con etiqueta "
            "'asíntota: y = 0'. Título: 'Desigualdad fundamental: e^x ≥ 1 + x'. " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Positividad.** Para todo $x \\in \\mathbb{R}$, $e^x > 0$. La función exponencial es "
              "**estrictamente positiva** y **no tiene ceros**.\n\n"
              "**Demostración (por casos):**\n\n"
              "- **Caso $x > -1$** ($x + 1 > 0$): por la desigualdad fundamental, $e^x \\geq x + 1 > 0$.\n"
              "- **Caso $x \\leq -1$:** entonces $-x \\geq 1 > 0$. Por Arquímedes existe $n \\in \\mathbb{N}$ "
              "con $-x < n$, luego $0 < 1 + x/n$, y elevando: $0 < (1 + x/n)^n \\leq e^x$. $\\square$"
          )),

        b("teorema",
          enunciado_md=(
              "**Crecimiento estricto e inyectividad.** Para todo $x, y \\in \\mathbb{R}$:\n\n"
              "$$x < y \\Rightarrow e^x < e^y.$$\n\n"
              "En particular, la exponencial es **estrictamente creciente** y por lo tanto **inyectiva**.\n\n"
              "**Demostración.** Sean $x < y$, así $y - x > 0$. Usando $e^y = e^x \\cdot e^{y-x}$ y la "
              "desigualdad fundamental con $t = y - x > 0$:\n\n"
              "$e^y = e^x \\cdot e^{y-x} \\geq e^x (1 + y - x) > e^x,$\n\n"
              "porque $1 + y - x > 1$ y $e^x > 0$. $\\quad\\square$\n\n"
              "**Corolario:** $\\text{Rec}(e^x) = (0, +\\infty)$. La función es estrictamente creciente, "
              "positiva y no acotada superiormente."
          )),

        b("ejemplo_resuelto",
          titulo="Transformaciones de la función exponencial",
          problema_md=(
              "Determine el comportamiento de las siguientes funciones:\n\n"
              "(a) $g(x) = e^{-x}$.\n"
              "(b) $h(x) = \\dfrac{10}{1 + e^{-x}}$ (función **logística**)."
          ),
          pasos=[
              {"accion_md": (
                  "**(a) $g(x) = e^{-x}$:** se obtiene reflejando $e^x$ respecto al eje $y$. Cada punto "
                  "$(x_0, e^{x_0})$ pasa a $(-x_0, e^{x_0})$.\n\n"
                  "**Comportamiento:** estrictamente **decreciente**, $g(0) = 1$, $g(x) \\to 0$ cuando "
                  "$x \\to +\\infty$ y $g(x) \\to +\\infty$ cuando $x \\to -\\infty$. Dominio $\\mathbb{R}$, "
                  "recorrido $(0, +\\infty)$."
               ),
               "justificacion_md": "Reflexión horizontal de $e^x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b) $h(x)$ — función logística:** analizamos sus límites.\n\n"
                  "- Cuando $x \\to +\\infty$: $e^{-x} \\to 0$, luego $h(x) \\to \\dfrac{10}{1 + 0} = 10$.\n"
                  "- Cuando $x \\to -\\infty$: $e^{-x} \\to +\\infty$, luego $h(x) \\to 0$.\n"
                  "- En $x = 0$: $h(0) = \\dfrac{10}{1 + 1} = 5$.\n\n"
                  "**Asíntotas horizontales** $y = 0$ e $y = 10$. Recorrido $(0, 10)$. Estrictamente "
                  "creciente. Forma de \"S\" (sigmoide). $\\boxed{\\text{Modelo de saturación.}}$"
               ),
               "justificacion_md": "La logística es fundamental en biología, ML, economía.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Modelo de propagación de enfermedad",
          problema_md=(
              "Una enfermedad infecciosa se propaga en una ciudad de $10\\,000$ habitantes. Después de $t$ días, "
              "el número de personas infectadas es $v(t) = \\dfrac{10\\,000}{5 + 1245\\, e^{-0{,}97 t}}$. "
              "(a) ¿Cuántas personas están infectadas inicialmente? (b) Comportamiento a largo plazo."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Evaluamos en $t = 0$:\n\n"
                  "$v(0) = \\dfrac{10\\,000}{5 + 1245 \\cdot e^{0}} = \\dfrac{10\\,000}{5 + 1245} = \\dfrac{10\\,000}{1250} = \\boxed{8}$ personas."
               ),
               "justificacion_md": "$e^0 = 1$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Cuando $t \\to +\\infty$, $e^{-0{,}97 t} \\to 0$. Luego:\n\n"
                  "$\\lim_{t\\to+\\infty} v(t) = \\dfrac{10\\,000}{5 + 0} = 2\\,000.$\n\n"
                  "**Asíntota horizontal $y = 2000$:** el número máximo de infectados es $2000$, el "
                  "$20\\%$ de la población. La función crece desde $8$ y se estabiliza cerca de $2000$ "
                  "— curva **logística** clásica."
               ),
               "justificacion_md": "Modelo realista de epidemias con saturación.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Propiedades algebraicas",
          body_md=(
              "Para todo $x, y \\in \\mathbb{R}$:\n\n"
              "- $e^{x+y} = e^x \\cdot e^y$.\n"
              "- $e^{x-y} = \\dfrac{e^x}{e^y}$.\n"
              "- $e^0 = 1$.\n"
              "- $e^{-x} = \\dfrac{1}{e^x}$.\n"
              "- $(e^x)^z = e^{xz}$ para $z \\in \\mathbb{R}$.\n\n"
              "Estas propiedades **justifican** la notación $e^x$: la función se comporta exactamente "
              "como una potencia. Las demostraciones rigurosas usan la definición vía límite y propiedades "
              "del producto de límites."
          )),

        b("intuicion", body_md=(
            "**Comportamiento asintótico.**\n\n"
            "$\\lim_{x \\to +\\infty} e^x = +\\infty$: la exponencial **crece sin cota**.\n\n"
            "$\\lim_{x \\to -\\infty} e^x = 0$: el eje $x$ es **asíntota horizontal** cuando "
            "$x \\to -\\infty$.\n\n"
            "**Comparación con polinomios** (jerarquía de crecimiento del cap. 4): $e^x$ crece más "
            "rápido que cualquier polinomio. Esto es lo que hace de $e^x$ la herramienta natural para "
            "modelar **crecimiento explosivo** (epidemias en fase inicial, interés compuesto, "
            "reacciones en cadena)."
        )),

        ej(
            "Resolver desigualdad con exponencial",
            "Resuelva $e^{2x - 1} > e^{x + 3}$.",
            [
                "Aplicá inyectividad: $e^a > e^b \\iff a > b$ (válida porque $e^x$ es estrictamente creciente).",
                "Resolvé la inecuación lineal resultante.",
            ],
            (
                "Por monotonía estricta: $e^{2x-1} > e^{x+3} \\iff 2x - 1 > x + 3 \\iff x > 4$.\n\n"
                "$\\boxed{S = (4, +\\infty).}$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $e^x$ con $e \\cdot x$:** son cosas distintas. $e^x$ es exponencial, $e \\cdot x$ es lineal.",
              "**Asumir $e^x > x^e$ siempre:** depende de $x$. Iguales en algún punto, intersectan.",
              "**Calcular $e^{x+y} = e^x + e^y$:** error clásico. La regla correcta es $e^{x+y} = e^x \\cdot e^y$.",
              "**Pensar que $e^x$ tiene ceros:** $e^x > 0$ para todo $x$. Nunca vale $0$.",
              "**Olvidar que $e^x \\to 0$ cuando $x \\to -\\infty$:** asíntota horizontal por la izquierda.",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición:** $e^x = \\lim_{n\\to\\infty} (1 + x/n)^n$.",
              "**Dominio** $\\mathbb{R}$, **recorrido** $(0, +\\infty)$.",
              "**Desigualdad fundamental:** $e^x \\geq 1 + x$, igualdad si $x = 0$.",
              "**Positividad:** $e^x > 0$ siempre, no tiene ceros.",
              "**Crecimiento estricto:** $x < y \\Rightarrow e^x < e^y$. Inyectiva.",
              "**Algebraicas:** $e^{x+y} = e^x e^y$, $e^{-x} = 1/e^x$, $e^0 = 1$.",
              "**Próxima lección:** función inversa — el logaritmo natural.",
          ]),
    ]
    return {
        "id": "lec-ic-5-1-funcion-exponencial",
        "title": "Función exponencial",
        "description": "Definición rigurosa de $e^x$ vía límite, desigualdad fundamental, positividad, crecimiento estricto e inyectividad.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 1,
    }


# =====================================================================
# 5.2 Función logarítmica
# =====================================================================
def lesson_5_2():
    blocks = [
        b("texto", body_md=(
            "La **función logarítmica** surge de manera natural como la función inversa de la exponencial. "
            "Su importancia es enorme: desde el crecimiento poblacional y el decaimiento radiactivo hasta "
            "la escala de Richter y los decibelios, el logaritmo es la herramienta indispensable para "
            "modelar fenómenos que involucran crecimientos o decaimientos proporcionales.\n\n"
            "**Objetivos:**\n\n"
            "- Definir $\\ln$ como inversa de $e^x$ y propiedades fundamentales.\n"
            "- **Propiedades algebraicas:** aditividad, sustracción, homogeneidad respecto a potencias.\n"
            "- **Desigualdad fundamental** del logaritmo natural.\n"
            "- Definir $a^x$ y $\\log_a$ para base arbitraria.\n"
            "- Aplicaciones a crecimiento exponencial y decaimiento."
        )),

        b("definicion",
          titulo="Logaritmo natural",
          body_md=(
              "La función exponencial $\\exp: \\mathbb{R} \\to (0, +\\infty)$ es **biyectiva** "
              "(inyectiva por crecimiento estricto, sobreyectiva por positividad y crecimiento sin cota). "
              "Por tanto, admite una única función inversa.\n\n"
              "**Definición.** La función inversa de $e^x$ es la **función logaritmo natural**\n\n"
              "$$\\ln: (0, +\\infty) \\to \\mathbb{R},$$\n\n"
              "definida por\n\n"
              "$$y = \\ln(x) \\iff e^y = x.$$\n\n"
              "En palabras: $\\ln(x)$ es el **único** $y$ real tal que $e^y = x$. El logaritmo natural de "
              "$x$ es el **exponente al que hay que elevar $e$ para obtener $x$**."
          )),

        b("teorema",
          enunciado_md=(
              "**Propiedades fundamentales del logaritmo natural.** Como consecuencia directa de ser "
              "inversa de $e^x$:\n\n"
              "- (a) $\\exp(\\ln(x)) = x$ para todo $x > 0$.\n"
              "- (b) $\\ln(\\exp(x)) = x$ para todo $x \\in \\mathbb{R}$. En particular, $\\ln(e) = 1$ y $\\ln(1) = 0$.\n"
              "- (c) $\\ln$ es **estrictamente creciente** (inversa de creciente). Preserva desigualdades: $0 < a < b \\Rightarrow \\ln(a) < \\ln(b)$.\n"
              "- (d) **Único cero:** $\\ln(x) = 0 \\iff x = 1$.\n"
              "- (e) $\\ln(x) > 0 \\iff x > 1$ y $\\ln(x) < 0 \\iff 0 < x < 1$."
          )),

        fig(
            "Plano cartesiano con dos curvas reflejadas en la diagonal y = x (línea punteada "
            "gris a 45°). Curva 1: y = e^x en color teal #06b6d4 (creciente rápido, asíntota "
            "horizontal y = 0 en izquierda; pasa por (-1, 0.37), (0, 1), (1, 2.72)). Curva 2: "
            "y = ln(x) en color ámbar #f59e0b (creciente lento, asíntota vertical x = 0 abajo; "
            "pasa por (0.37, -1), (1, 0), (2.72, 1)). Las curvas son reflejos exactos respecto "
            "a y = x. Tres pares de puntos correspondientes resaltados con líneas punteadas: "
            "(0, 1) ↔ (1, 0), (1, e) ↔ (e, 1), (-1, 1/e) ↔ (1/e, -1). Asíntotas marcadas: "
            "x = 0 punteada (vertical, para ln) y y = 0 punteada (horizontal, para exp). "
            "Anotación: 'ln(x) = y ⇔ e^y = x'. Título: 'ln es la inversa de e^x — reflejo "
            "respecto a y = x'. " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Propiedades algebraicas del logaritmo natural.** Para todo $x, y > 0$ y $z \\in \\mathbb{R}$:\n\n"
              "1. $\\ln(xy) = \\ln(x) + \\ln(y)$ (logaritmo del producto = suma).\n"
              "2. $\\ln(x/y) = \\ln(x) - \\ln(y)$ (logaritmo del cociente = diferencia).\n"
              "3. $\\ln(x^z) = z \\ln(x)$ (potencia sale como factor).\n\n"
              "**Demostración del 1.** Sean $u = \\ln(x)$, $w = \\ln(y)$, así $e^u = x$, $e^w = y$. Entonces:\n\n"
              "$\\ln(xy) = \\ln(e^u \\cdot e^w) = \\ln(e^{u+w}) = u + w = \\ln(x) + \\ln(y). \\quad\\square$\n\n"
              "**Demostración del 3.** Sea $u = \\ln(x)$, $e^u = x$. Entonces:\n\n"
              "$\\ln(x^z) = \\ln((e^u)^z) = \\ln(e^{zu}) = zu = z \\ln(x). \\quad\\square$\n\n"
              "**Importancia histórica:** estas propiedades **transforman productos en sumas y potencias en "
              "productos**. Fue la razón por la que se inventaron los logaritmos en el siglo XVII — para "
              "simplificar cálculos aritméticos complejos."
          )),

        b("ejemplo_resuelto",
          titulo="Simplificación de logaritmos",
          problema_md=(
              "Simplifique $\\ln(8) - \\ln(2) + \\ln(5)$ usando las propiedades."
          ),
          pasos=[
              {"accion_md": (
                  "Aplicamos propiedad 2 a los dos primeros términos:\n\n"
                  "$\\ln(8) - \\ln(2) = \\ln\\left(\\dfrac{8}{2}\\right) = \\ln(4).$"
               ),
               "justificacion_md": "Logaritmo del cociente.",
               "es_resultado": False},
              {"accion_md": (
                  "Sumando el último: $\\ln(4) + \\ln(5) = \\ln(4 \\cdot 5) = \\boxed{\\ln(20).}$"
               ),
               "justificacion_md": "Logaritmo del producto.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Expansión usando propiedades",
          problema_md=(
              "Exprese $\\ln\\left(\\dfrac{x^3 \\sqrt{x+1}}{(x-2)^4}\\right)$ como suma y diferencia "
              "de logaritmos simples (para $x > 2$)."
          ),
          pasos=[
              {"accion_md": (
                  "Aplicando propiedades 1 (producto) y 2 (cociente):\n\n"
                  "$\\ln\\left(\\dfrac{x^3 \\sqrt{x+1}}{(x-2)^4}\\right) = \\ln(x^3) + \\ln(\\sqrt{x+1}) - \\ln((x-2)^4).$"
               ),
               "justificacion_md": "Descomponemos el cociente y el producto.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicando propiedad 3 (potencia, recordando $\\sqrt{u} = u^{1/2}$):\n\n"
                  "$= \\boxed{3\\ln(x) + \\dfrac{1}{2}\\ln(x+1) - 4\\ln(x-2).}$"
               ),
               "justificacion_md": "Bajamos los exponentes como factores.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Desigualdad fundamental del logaritmo natural.** Para todo $x > 0$:\n\n"
              "$$\\boxed{1 - \\dfrac{1}{x} \\leq \\ln(x) \\leq x - 1,}$$\n\n"
              "con igualdad en ambos lados si y solo si $x = 1$.\n\n"
              "**Demostración del lado derecho ($\\ln(x) \\leq x - 1$).** Sabemos que $e^z \\geq 1 + z$ "
              "(desigualdad fundamental de la exponencial). Aplicando $\\ln$ a ambos lados (válido porque "
              "$\\ln$ es creciente):\n\n"
              "$z = \\ln(e^z) \\geq \\ln(1 + z).$\n\n"
              "Cambio de variable $z = x - 1$ con $x > 0$ ($z > -1$):\n\n"
              "$x - 1 \\geq \\ln(1 + (x-1)) = \\ln(x). \\quad\\square$\n\n"
              "**Lado izquierdo:** se obtiene aplicando la cota anterior a $1/x$ y usando $\\ln(1/x) = -\\ln(x)$."
          )),

        b("intuicion", body_md=(
            "**Interpretación geométrica.** La recta $y = x - 1$ es **tangente** a $y = \\ln(x)$ en el "
            "punto $(1, 0)$. Como $\\ln$ es **cóncava**, su gráfica queda siempre **por debajo** de "
            "cualquier recta tangente. La desigualdad $\\ln(x) \\leq x - 1$ es exactamente esta cota.\n\n"
            "Análogamente, $1 - 1/x$ acota a $\\ln(x)$ por **abajo**. Las dos cotas encierran al "
            "logaritmo entre dos funciones algebraicas simples."
        )),

        b("definicion",
          titulo="Función $a^x$ y logaritmo en base $a$",
          body_md=(
              "Hasta ahora trabajamos con base $e$. Para una base arbitraria $a \\in \\mathbb{R}^+ \\setminus \\{1\\}$:\n\n"
              "$$a^x = \\exp(x \\ln a) = e^{x \\ln a}.$$\n\n"
              "Esta definición extiende potencias a exponentes reales (incluyendo irracionales como $2^{\\sqrt{2}}$).\n\n"
              "**Propiedades** (consecuencia directa de las de $\\exp$):\n\n"
              "- Dominio $\\mathbb{R}$, recorrido $(0, +\\infty)$.\n"
              "- **Estrictamente creciente** si $a > 1$ (porque $\\ln(a) > 0$).\n"
              "- **Estrictamente decreciente** si $0 < a < 1$ (porque $\\ln(a) < 0$).\n"
              "- **Inyectiva** y biyectiva sobre su recorrido.\n\n"
              "**Logaritmo en base $a$** (inversa de $a^x$):\n\n"
              "$$\\log_a(x) = \\dfrac{\\ln(x)}{\\ln(a)}.$$\n\n"
              "Esta es la **fórmula de cambio de base**: cualquier logaritmo se expresa en términos del "
              "natural. Casos especiales:\n\n"
              "- $\\log_e(x) = \\ln(x)$ (natural).\n"
              "- $\\log_{10}(x)$: **logaritmo decimal** o común. Usado en escala de Richter, pH, decibelios."
          )),

        b("ejemplo_resuelto",
          titulo="Crecimiento bacteriano",
          problema_md=(
              "Una colonia bacteriana inicia con $400$ bacterias y crece al $5\\%$ por hora. Si el número "
              "no debe superar $10\\,000$ antes de cambiar el tratamiento, ¿cuánto tiempo se dispone?"
          ),
          pasos=[
              {"accion_md": (
                  "**Modelo:** $N(t) = N_0 e^{\\lambda t}$ con $N_0 = 400$, $\\lambda = 0{,}05$. Buscamos $t$ tal que $N(t) = 10\\,000$:\n\n"
                  "$400 \\cdot e^{0{,}05 t} = 10\\,000 \\iff e^{0{,}05 t} = 25.$"
               ),
               "justificacion_md": "Ecuación de crecimiento exponencial.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicamos $\\ln$ a ambos lados (válido porque ambos son positivos):\n\n"
                  "$0{,}05 t = \\ln(25) \\iff t = \\dfrac{\\ln(25)}{0{,}05}.$\n\n"
                  "$\\ln(25) = \\ln(5^2) = 2\\ln(5) \\approx 2 \\cdot 1{,}609 = 3{,}219$. Por tanto:\n\n"
                  "$t \\approx \\dfrac{3{,}219}{0{,}05} \\approx \\boxed{64{,}38 \\text{ horas.}}$"
               ),
               "justificacion_md": "Aproximadamente 64 horas — a partir de ahí hay que cambiar tratamiento.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Decaimiento radiactivo (vida media)",
          problema_md=(
              "Una sustancia radiactiva tiene **vida media** de $10$ años. Si inicialmente hay $M_0$ gramos, "
              "halle $\\lambda$ y el tiempo para que la masa caiga al $10\\%$ del valor inicial."
          ),
          pasos=[
              {"accion_md": (
                  "**Modelo:** $M(t) = M_0 e^{\\lambda t}$ con $\\lambda < 0$. Vida media: $M(10) = M_0 / 2$.\n\n"
                  "$e^{10\\lambda} = \\dfrac{1}{2} \\iff 10\\lambda = \\ln(1/2) = -\\ln 2 \\iff \\lambda = -\\dfrac{\\ln 2}{10}.$"
               ),
               "justificacion_md": "Caracterización por vida media.",
               "es_resultado": False},
              {"accion_md": (
                  "Para $M(t) = 0{,}1 M_0$:\n\n"
                  "$e^{-(\\ln 2 / 10) t} = 0{,}1 \\iff -\\dfrac{\\ln 2}{10} t = \\ln(0{,}1) = -\\ln 10.$\n\n"
                  "Despejando: $t = \\dfrac{10 \\ln 10}{\\ln 2} \\approx \\dfrac{10 \\cdot 2{,}303}{0{,}693} \\approx \\boxed{33{,}22 \\text{ años.}}$"
               ),
               "justificacion_md": "Aproximadamente $3{,}3$ vidas medias.",
               "es_resultado": True},
          ]),

        ej(
            "Aplicar propiedades del logaritmo",
            "Pruebe la propiedad $\\ln(x) - \\ln(y) = \\ln(x/y)$ usando las propiedades 1 y 3.",
            [
                "Escribí $x/y = x \\cdot y^{-1}$.",
                "Aplicá propiedad 1 (producto) y luego propiedad 3 con exponente $-1$.",
            ],
            (
                "$\\ln(x/y) = \\ln(x \\cdot y^{-1}) \\stackrel{(1)}{=} \\ln(x) + \\ln(y^{-1}) \\stackrel{(3)}{=} \\ln(x) + (-1)\\ln(y) = \\ln(x) - \\ln(y). \\quad\\square$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Calcular $\\ln(x + y) = \\ln(x) + \\ln(y)$:** ERROR. La regla es para producto: $\\ln(xy) = \\ln(x) + \\ln(y)$.",
              "**Olvidar dominio del log:** $\\ln(x)$ exige $x > 0$. Aparece en muchas restricciones.",
              "**Confundir $\\ln(x)$ con $\\log(x)$:** este último suele ser base $10$. Notación importa.",
              "**Aplicar $\\ln$ a una desigualdad sin verificar positividad:** $\\ln$ solo está definido en positivos.",
              "**Dividir $\\ln(x)/\\ln(y)$ pensando que es $\\ln(x/y)$:** son cosas distintas. La fórmula correcta del cociente es $\\ln(x/y) = \\ln(x) - \\ln(y)$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición:** $y = \\ln(x) \\iff e^y = x$, con $x > 0$.",
              "**Valores especiales:** $\\ln(1) = 0$, $\\ln(e) = 1$.",
              "**Algebraicas:** $\\ln(xy) = \\ln(x) + \\ln(y)$, $\\ln(x/y) = \\ln(x) - \\ln(y)$, $\\ln(x^z) = z\\ln(x)$.",
              "**Desigualdad fundamental:** $1 - 1/x \\leq \\ln(x) \\leq x - 1$, igualdad solo en $x = 1$.",
              "**Función $a^x = e^{x \\ln a}$, logaritmo en base $a$:** $\\log_a(x) = \\ln(x)/\\ln(a)$.",
              "**Modelo de crecimiento:** $N(t) = N_0 e^{\\lambda t}$, despejar $t$ con $\\ln$.",
              "**Próxima lección:** ecuaciones exponenciales y logarítmicas.",
          ]),
    ]
    return {
        "id": "lec-ic-5-2-funcion-logaritmica",
        "title": "Función logarítmica",
        "description": "Definición de $\\ln$ como inversa de $e^x$, propiedades algebraicas, desigualdad fundamental, función $a^x$, logaritmo de base $a$ y aplicaciones.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# =====================================================================
# 5.3 Ecuaciones exponenciales y logarítmicas
# =====================================================================
def lesson_5_3():
    blocks = [
        b("texto", body_md=(
            "Las **ecuaciones exponenciales y logarítmicas** aparecen en múltiples contextos del cálculo "
            "y sus aplicaciones: crecimiento poblacional, interés compuesto, escalas de pH, magnitudes "
            "sísmicas. En esta lección presentamos los **cuatro métodos fundamentales** para abordarlas, "
            "con énfasis en la verificación del dominio para evitar **soluciones extrañas**.\n\n"
            "**Métodos:**\n\n"
            "- **Para exponenciales:** igualar base, cambio de variable, logaritmo.\n"
            "- **Para logarítmicas:** forma exponencial, igualar argumento.\n\n"
            "**Crítico:** verificar el dominio en ecuaciones logarítmicas — argumento $> 0$ siempre."
        )),

        fig(
            "Diagrama de árbol de decisión vertical para resolver ecuaciones exponenciales y "
            "logarítmicas. Caja superior (color teal #06b6d4): '¿Qué tipo de ecuación?'. Dos "
            "ramas: 'EXPONENCIAL: a^f(x) = b^g(x)' (rama izquierda) y 'LOGARÍTMICA: log(...) = "
            "log(...) o log(...) = c' (rama derecha). En la rama exponencial, tres sub-cajas "
            "ámbar #f59e0b: '¿Misma base posible?' → Método 1 (igualar base); '¿Múltiplos del "
            "mismo exponente?' → Método 2 (cambio de variable u = a^x); 'Ningún caso anterior' "
            "→ Método 3 (aplicar log y bajar exponente). En la rama logarítmica, dos sub-cajas: "
            "'log = constante' → Método 4 (forma exponencial: log_a(u) = c ⇔ u = a^c); 'log = "
            "log' → igualar argumentos. Caja final ROJA en la base: '⚠ VERIFICAR DOMINIO: "
            "argumento > 0' apuntando a la rama logarítmica. Título: 'Estrategia para resolver "
            "ecuaciones exponenciales y logarítmicas'. " + STYLE
        ),

        b("definicion",
          titulo="Método 1 — Igualar base",
          body_md=(
              "Se basa en la **inyectividad** de $a^x$ con $a > 0$, $a \\neq 1$:\n\n"
              "$$a^x = a^y \\iff x = y.$$\n\n"
              "**Estrategia:** reescribir ambos lados como potencias de una **misma base** $a$, igualar "
              "exponentes y resolver. Útil cuando los términos comparten una base común (e.g., $2, 4, 8, 16$ "
              "todas son potencias de $2$).\n\n"
              "**Propiedades de exponentes útiles:**\n\n"
              "- $a^{x+k} = a^k \\cdot a^x$\n"
              "- $a^{x-k} = a^x / a^k$\n"
              "- $(a^m)^n = a^{mn}$"
          )),

        b("ejemplo_resuelto",
          titulo="Igualar base con factorización",
          problema_md=(
              "Resuelva $3 \\cdot 2^{x+1} - 5 \\cdot 2^x + 2^{x-1} = 48$."
          ),
          pasos=[
              {"accion_md": (
                  "Reescribimos cada término en función de $2^x$: $2^{x+1} = 2 \\cdot 2^x$, $2^{x-1} = 2^x / 2$:\n\n"
                  "$3 \\cdot 2 \\cdot 2^x - 5 \\cdot 2^x + \\dfrac{2^x}{2} = 48 \\iff 2^x \\left(6 - 5 + \\dfrac{1}{2}\\right) = 48.$"
               ),
               "justificacion_md": "Factorizamos $2^x$.",
               "es_resultado": False},
              {"accion_md": (
                  "Simplificamos: $2^x \\cdot \\dfrac{3}{2} = 48 \\iff 2^x = 32 = 2^5$. Por inyectividad: $\\boxed{x = 5.}$"
               ),
               "justificacion_md": "Reconocemos $32 = 2^5$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Método 2 — Cambio de variable",
          body_md=(
              "Cuando la ecuación contiene la base elevada a **distintos múltiplos** del exponente, no "
              "siempre se puede igualar bases. Se sustituye $u = a^x$ con $u > 0$, transformando la ecuación "
              "exponencial en **algebraica** (frecuentemente cuadrática).\n\n"
              "**Después de resolver para $u$:**\n\n"
              "1. Descartar soluciones $u \\leq 0$ (recordar que $a^x > 0$ siempre).\n"
              "2. Para cada $u > 0$ válida, resolver $a^x = u$ con métodos 1 o 3."
          )),

        b("ejemplo_resuelto",
          titulo="Cambio de variable a cuadrática",
          problema_md=(
              "Resuelva $4^{x+1} - \\dfrac{2}{4^x} = 7$."
          ),
          pasos=[
              {"accion_md": (
                  "$4^{x+1} = 4 \\cdot 4^x$. Sea $u = 4^x > 0$:\n\n"
                  "$4u - \\dfrac{2}{u} = 7 \\iff 4u^2 - 2 = 7u \\iff 4u^2 - 7u - 2 = 0.$"
               ),
               "justificacion_md": "Multiplicamos por $u > 0$ — válido.",
               "es_resultado": False},
              {"accion_md": (
                  "Fórmula cuadrática: $u = \\dfrac{7 \\pm \\sqrt{49 + 32}}{8} = \\dfrac{7 \\pm 9}{8}$. "
                  "Soluciones: $u_1 = 2$, $u_2 = -1/4$.\n\n"
                  "Como $u > 0$, descartamos $u_2$. Queda $u_1 = 2$."
               ),
               "justificacion_md": "Descartamos solución negativa.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolvemos $4^x = 2 \\iff (2^2)^x = 2^1 \\iff 2^{2x} = 2^1 \\iff 2x = 1$. "
                  "$\\boxed{x = \\dfrac{1}{2}.}$"
               ),
               "justificacion_md": "Igualar base con $2$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Método 3 — Logaritmo",
          body_md=(
              "Cuando los términos no pueden reducirse a una misma base, se aplica el **logaritmo** "
              "(natural o decimal) a ambos lados. Se basa en la equivalencia:\n\n"
              "$$a^x = b \\iff x = \\log_a(b), \\quad a > 0,\\ a \\neq 1,\\ b > 0.$$\n\n"
              "Equivalentemente, aplicar $\\ln$ a ambos lados y usar $\\ln(a^x) = x \\ln(a)$.\n\n"
              "**Propiedades clave:**\n\n"
              "- $\\log_a(mn) = \\log_a(m) + \\log_a(n)$\n"
              "- $\\log_a(m/n) = \\log_a(m) - \\log_a(n)$\n"
              "- $\\log_a(m^r) = r \\log_a(m)$"
          )),

        b("ejemplo_resuelto",
          titulo="Aplicación del logaritmo",
          problema_md=(
              "Resuelva $2 \\cdot 3^{x+1} - 5 \\cdot 3^x + 3^{x-1} = 24$."
          ),
          pasos=[
              {"accion_md": (
                  "Reescribimos como en el método 1: $3^{x+1} = 3 \\cdot 3^x$, $3^{x-1} = 3^x / 3$. Factorizando $3^x$:\n\n"
                  "$3^x \\left(6 - 5 + \\dfrac{1}{3}\\right) = 24 \\iff 3^x \\cdot \\dfrac{4}{3} = 24 \\iff 3^x = 18.$"
               ),
               "justificacion_md": "Factorización.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $18$ no es potencia exacta de $3$ ($18 = 2 \\cdot 9 = 2 \\cdot 3^2$), aplicamos $\\log_3$:\n\n"
                  "$x = \\log_3(18) = \\log_3(2 \\cdot 3^2) = \\log_3(2) + \\log_3(3^2) = \\log_3(2) + 2.$\n\n"
                  "$\\boxed{x = 2 + \\log_3(2).}$"
               ),
               "justificacion_md": "Solución exacta en términos de logaritmo. Aproximación: $\\log_3 2 \\approx 0{,}631$, $x \\approx 2{,}631$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Método 4 — Forma exponencial (para ecuaciones logarítmicas)",
          body_md=(
              "Para resolver $\\log_a(f(x)) = c$, se convierte a la **forma exponencial** usando:\n\n"
              "$$\\log_a(x) = c \\iff x = a^c.$$\n\n"
              "Si la ecuación tiene varios logaritmos, primero se usan las propiedades para reducir a "
              "la forma $\\log_a(f(x)) = c$.\n\n"
              "**¡ATENCIÓN AL DOMINIO!** Toda ecuación logarítmica impone restricciones sobre $x$. El "
              "argumento de cualquier logaritmo debe ser **estrictamente positivo**. Es **indispensable** "
              "verificar que las soluciones obtenidas satisfagan estas condiciones; de lo contrario, deben "
              "**descartarse como soluciones extrañas**."
          )),

        b("ejemplo_resuelto",
          titulo="Forma exponencial — solución válida",
          problema_md=(
              "Resuelva $\\log_2(x + 2) - \\log_2(x - 1) = 3$."
          ),
          pasos=[
              {"accion_md": (
                  "**Dominio:** $x + 2 > 0$ y $x - 1 > 0$ ⟹ $x > 1$.\n\n"
                  "Aplicando $\\log_a(m) - \\log_a(n) = \\log_a(m/n)$:\n\n"
                  "$\\log_2\\left(\\dfrac{x+2}{x-1}\\right) = 3.$"
               ),
               "justificacion_md": "Compactamos los dos logaritmos.",
               "es_resultado": False},
              {"accion_md": (
                  "Forma exponencial:\n\n"
                  "$\\dfrac{x+2}{x-1} = 2^3 = 8 \\iff x + 2 = 8(x-1) = 8x - 8 \\iff 10 = 7x \\iff x = \\dfrac{10}{7}.$\n\n"
                  "**Verificación dominio:** $\\dfrac{10}{7} \\approx 1{,}43 > 1$ ✓. $\\boxed{x = \\dfrac{10}{7}.}$"
               ),
               "justificacion_md": "La solución pertenece al dominio.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Forma exponencial — solución extraña",
          problema_md=(
              "Resuelva $\\log_3(x - 2) - \\log_3(x - 1) = 1$."
          ),
          pasos=[
              {"accion_md": (
                  "**Dominio:** $x - 2 > 0$ y $x - 1 > 0$ ⟹ $x > 2$.\n\n"
                  "$\\log_3\\left(\\dfrac{x-2}{x-1}\\right) = 1 \\iff \\dfrac{x-2}{x-1} = 3.$"
               ),
               "justificacion_md": "Reducción a forma exponencial.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolviendo: $x - 2 = 3(x-1) = 3x - 3 \\iff 1 = 2x \\iff x = \\dfrac{1}{2}$.\n\n"
                  "**Verificación dominio:** $\\dfrac{1}{2} < 2$. **NO satisface** $x > 2$. ✗\n\n"
                  "$\\boxed{S = \\emptyset.}$ Solución **extraña** — descartada por dominio."
               ),
               "justificacion_md": "**SIEMPRE verificar dominio** en ecuaciones logarítmicas.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Método 5 — Igualar argumento (para ecuaciones logarítmicas)",
          body_md=(
              "Aprovecha la **inyectividad** de $\\log_a$:\n\n"
              "$$\\log_a(x) = \\log_a(y) \\iff x = y, \\quad x, y > 0.$$\n\n"
              "**Estrategia:** usar propiedades para llevar la ecuación a la forma $\\log_a(f(x)) = \\log_a(g(x))$ "
              "e igualar los argumentos. Aplicable cuando ambos lados son logaritmos (no constantes). "
              "Como en el método 4, siempre verificar el dominio."
          )),

        b("ejemplo_resuelto",
          titulo="Igualar argumento + descartar solución extraña",
          problema_md=(
              "Resuelva $\\ln(x + 1) - \\ln(2x - 1) = \\ln(x - 1)$."
          ),
          pasos=[
              {"accion_md": (
                  "**Dominio:** $x + 1 > 0$, $2x - 1 > 0$, $x - 1 > 0$. La condición más restrictiva: $x > 1$.\n\n"
                  "Aplicando diferencia: $\\ln\\left(\\dfrac{x+1}{2x-1}\\right) = \\ln(x - 1)$.\n\n"
                  "Igualando argumentos: $\\dfrac{x+1}{2x-1} = x - 1$."
               ),
               "justificacion_md": "Inyectividad del logaritmo.",
               "es_resultado": False},
              {"accion_md": (
                  "Multiplicamos por $2x - 1 > 0$ (válido para $x > 1$):\n\n"
                  "$x + 1 = (x-1)(2x-1) = 2x^2 - 3x + 1 \\iff 2x^2 - 4x = 0 \\iff 2x(x - 2) = 0.$\n\n"
                  "Soluciones algebraicas: $x = 0$ y $x = 2$."
               ),
               "justificacion_md": "Cuadrática.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación dominio** ($x > 1$):\n\n"
                  "- $x = 0$: NO satisface. ✗ Solución extraña, descartada.\n"
                  "- $x = 2$: SÍ satisface. ✓\n\n"
                  "**Verificación numérica:** $\\ln(3) - \\ln(3) = 0 = \\ln(1)$ ✓.\n\n"
                  "$\\boxed{S = \\{2\\}.}$"
               ),
               "justificacion_md": "Una solución extraña descartada, otra válida.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Resumen de los 5 métodos:**\n\n"
            "| Método | Cuándo aplicar | Idea clave |\n"
            "|:---:|:---|:---|\n"
            "| 1 — Igualar base | $a^{f(x)} = a^{g(x)}$ | Inyectividad de $a^x$ |\n"
            "| 2 — Cambio de variable | $a^x$ aparece en distintas potencias | $u = a^x > 0$ |\n"
            "| 3 — Logaritmo | $a^{f(x)} = b$ con bases incompatibles | Aplicar $\\log$ ambos lados |\n"
            "| 4 — Forma exponencial | $\\log_a(f(x)) = c$ | $f(x) = a^c$ |\n"
            "| 5 — Igualar argumento | $\\log_a(f(x)) = \\log_a(g(x))$ | Inyectividad de $\\log_a$ |\n\n"
            "**Para ecuaciones logarítmicas (4 y 5):** SIEMPRE verificar dominio para descartar **soluciones extrañas**."
        )),

        ej(
            "Ecuación exponencial con cambio de variable",
            "Resuelva $9^x - 4 \\cdot 3^x + 3 = 0$.",
            [
                "Notá $9^x = (3^x)^2$.",
                "Cambio $u = 3^x > 0$, obtené cuadrática.",
                "Resolvé cada $a^x = u_i$ para $u_i > 0$.",
            ],
            (
                "$9^x = (3^x)^2 = u^2$ con $u = 3^x > 0$. Ecuación: $u^2 - 4u + 3 = 0 \\iff (u-1)(u-3) = 0$. Soluciones $u = 1, u = 3$, ambas positivas.\n\n"
                "$3^x = 1 \\iff x = 0$. $3^x = 3 \\iff x = 1$.\n\n"
                "$\\boxed{S = \\{0, 1\\}.}$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar verificar dominio en ecuaciones logarítmicas:** las soluciones extrañas son la trampa más frecuente.",
              "**Aceptar $u \\leq 0$ tras cambio de variable $u = a^x$:** $a^x > 0$ siempre. Descartar negativas/nulas.",
              "**Aplicar logaritmo a ambos lados sin verificar positividad:** $\\log$ solo definido para $> 0$.",
              "**Reducir $\\log_a(f) + \\log_a(g)$ a $\\log_a(f \\cdot g)$ sin verificar que ambos $> 0$:** se pueden añadir soluciones espurias.",
              "**Pensar que toda ecuación exponencial tiene solución:** ej. $e^x = -2$ no tiene solución porque $e^x > 0$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Exponenciales** (3 métodos): igualar base, cambio de variable ($u = a^x > 0$), logaritmo.",
              "**Logarítmicas** (2 métodos): forma exponencial, igualar argumento.",
              "**$a^x = a^y \\iff x = y$** (inyectividad de $a^x$).",
              "**$\\log_a(x) = \\log_a(y) \\iff x = y$** (inyectividad del logaritmo).",
              "**$\\log_a(x) = c \\iff x = a^c$** (definición).",
              "**Verificar dominio SIEMPRE** en ecuaciones logarítmicas.",
              "**Cierre del curso:** Introducción al Cálculo te dejó listo para Cálculo Diferencial.",
          ]),
    ]
    return {
        "id": "lec-ic-5-3-ecuaciones-exp-log",
        "title": "Ecuaciones exponenciales y logarítmicas",
        "description": "Cinco métodos: igualar base, cambio de variable, logaritmo, forma exponencial e igualar argumento. Verificación de dominio y soluciones extrañas.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
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

    chapter_id = "ch-ic-exp-log"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Funciones Exponencial y Logarítmica",
        "description": (
            "Construcción rigurosa de la función exponencial $e^x$ vía sucesiones, función logaritmo "
            "natural como inversa, propiedades algebraicas, función $a^x$ y logaritmo en base $a$, y "
            "métodos para resolver ecuaciones exponenciales y logarítmicas."
        ),
        "order": 5,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_5_1, lesson_5_2, lesson_5_3]
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
    print(f"✅ Capítulo 5 — Funciones Exp y Log listo: {len(builders)} lecciones, {total_blocks} bloques, "
          f"{total_figs} figuras pendientes.")
    print()
    print("URLs locales:")
    print(f"  http://localhost:3007/courses/{course_id}")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
