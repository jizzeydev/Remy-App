"""
Seed del curso Cálculo Multivariable — Capítulo 6: Integrales Múltiples.
7 lecciones:
  6.1 Integrales dobles
  6.2 Regiones generales
  6.3 Coordenadas polares
  6.4 Integrales triples
  6.5 Coordenadas cilíndricas
  6.6 Coordenadas esféricas
  6.7 Cambio de variables

Capítulo grande con varias figuras geométricas.
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


def formulas(titulo, body):
    return b("definicion", titulo=titulo, body_md=body)


def now():
    return datetime.now(timezone.utc).isoformat()


STYLE = (
    "Estilo: diagrama matemático educativo limpio, fondo blanco, líneas claras, "
    "etiquetas en español, notación matemática con buena tipografía. Acentos teal "
    "#06b6d4 y ámbar #f59e0b. Sin sombras dramáticas. Apto para libro universitario."
)


# =====================================================================
# 6.1 Integrales dobles
# =====================================================================
def lesson_6_1():
    blocks = [
        b("texto", body_md=(
            "La **integral doble** generaliza la integral de una variable a regiones del plano. "
            "Igual que en 1D la integral mide área bajo una curva, en 2D mide **volumen bajo una superficie**. "
            "La herramienta clave para calcularla es el **teorema de Fubini**, que reduce la integral doble a "
            "dos integrales iteradas (de una variable a la vez).\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir $\\iint_R f(x, y) \\, dA$ como límite de sumas de Riemann.\n"
            "- Aplicar el **teorema de Fubini** para evaluar sobre rectángulos.\n"
            "- Manejar las **propiedades**: linealidad, aditividad de regiones, comparación.\n"
            "- Reconocer la integral doble como **volumen** bajo $z = f(x, y) \\geq 0$."
        )),

        b("intuicion",
          titulo="Sumas de Riemann en 2D",
          body_md=(
              "Para definir $\\iint_R f(x, y) \\, dA$ sobre un rectángulo $R = [a, b] \\times [c, d]$:\n\n"
              "1. **Dividir** $R$ en una cuadrícula de subrectángulos $R_{ij}$ de área $\\Delta A = \\Delta x \\Delta y$.\n"
              "2. **Elegir un punto** $(x_{ij}^*, y_{ij}^*)$ en cada subrectángulo.\n"
              "3. **Suma de Riemann:** $S_{mn} = \\sum_{i, j} f(x_{ij}^*, y_{ij}^*) \\Delta A$.\n"
              "4. **Tomar el límite** cuando la malla se hace fina.\n\n"
              "Si $f \\geq 0$, cada término $f \\cdot \\Delta A$ es el **volumen** de un prisma con base $\\Delta A$ y altura $f$. "
              "El límite es el volumen total bajo la superficie $z = f(x, y)$."
          )),

        fig(
            "Suma de Riemann para una integral doble. Vista isométrica 3D de un rectángulo R en el "
            "plano xy, dividido en una cuadrícula de subrectángulos pequeños (ej: 5×5). Sobre cada "
            "subrectángulo, dibujar un prisma rectangular vertical cuya altura es f evaluado en un "
            "punto del subrectángulo, en color ámbar translúcido. La superficie z = f(x, y) "
            "ondulada por encima en color teal. Mostrar cómo la suma de los volúmenes de los "
            "prismas aproxima el volumen bajo la superficie. Etiquetas: 'R', 'z = f(x, y)', "
            "'subrectángulo R_ij', 'altura f(x*_ij, y*_ij)'. " + STYLE
        ),

        b("definicion",
          titulo="Integral doble sobre un rectángulo",
          body_md=(
              "Si el límite\n\n"
              "$$\\iint_R f(x, y) \\, dA = \\lim_{m, n \\to \\infty} \\sum_{i=1}^{m} \\sum_{j=1}^{n} f(x_{ij}^*, y_{ij}^*) \\Delta A$$\n\n"
              "existe y no depende de la elección de los puntos de muestreo, decimos que $f$ es **integrable** sobre $R$ y al límite lo llamamos **integral doble** de $f$ sobre $R$.\n\n"
              "**Notaciones equivalentes:** $\\iint_R f \\, dA$, $\\iint_R f(x, y) \\, dx \\, dy$, $\\iint_R f(x, y) \\, dy \\, dx$.\n\n"
              "**Hecho clave:** si $f$ es **continua** en $R$, entonces es integrable."
          )),

        b("teorema",
          nombre="Teorema de Fubini",
          enunciado_md=(
              "Si $f$ es continua sobre $R = [a, b] \\times [c, d]$, entonces:\n\n"
              "$$\\iint_R f(x, y) \\, dA = \\int_a^b \\int_c^d f(x, y) \\, dy \\, dx = \\int_c^d \\int_a^b f(x, y) \\, dx \\, dy$$\n\n"
              "Es decir, la integral doble se calcula como **dos integrales iteradas**, y **el orden no importa** (los dos órdenes dan el mismo valor).\n\n"
              "**Lectura interna:** $\\int_c^d f(x, y) \\, dy$ trata $x$ como constante, integra respecto a $y$ entre $c$ y $d$. El resultado es función de $x$. Después se integra respecto a $x$."
          ),
          demostracion_md=(
              "Idea: la suma de Riemann doble se puede agrupar de dos maneras. Sumando primero por filas (fijando $i$ y sumando sobre $j$) o primero por columnas. Cada agrupación corresponde a una integral iterada.\n\n"
              "El paso al límite requiere uniformidad — garantizada por la continuidad. La demostración formal usa el teorema de aproximación uniforme."
          )),

        b("ejemplo_resuelto",
          titulo="Integral doble sobre un rectángulo",
          problema_md=(
              "Calcular $\\iint_R xy^2 \\, dA$ donde $R = [0, 2] \\times [1, 3]$."
          ),
          pasos=[
              {"accion_md": "**Aplicar Fubini** (integramos primero respecto a $y$):\n\n"
                            "$\\iint_R xy^2 \\, dA = \\int_0^2 \\int_1^3 xy^2 \\, dy \\, dx$.",
               "justificacion_md": "El orden es libre. Empezamos con la $y$.",
               "es_resultado": False},
              {"accion_md": "**Integral interna:** $\\int_1^3 xy^2 \\, dy = x \\int_1^3 y^2 \\, dy = x \\cdot \\dfrac{y^3}{3}\\Big|_1^3 = x \\cdot \\dfrac{27 - 1}{3} = \\dfrac{26x}{3}$.",
               "justificacion_md": "$x$ se trata como constante. Antiderivada de $y^2$ es $y^3/3$.",
               "es_resultado": False},
              {"accion_md": "**Integral externa:** $\\int_0^2 \\dfrac{26x}{3} \\, dx = \\dfrac{26}{3} \\cdot \\dfrac{x^2}{2}\\Big|_0^2 = \\dfrac{26}{3} \\cdot 2 = \\dfrac{52}{3}$.",
               "justificacion_md": "Ahora integramos en $x$ el resultado anterior.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Cuando $f$ es producto: la integral se separa",
          body_md=(
              "**Caso especial útil:** si $f(x, y) = g(x) h(y)$ y $R = [a, b] \\times [c, d]$:\n\n"
              "$$\\iint_R g(x) h(y) \\, dA = \\left(\\int_a^b g(x) \\, dx\\right)\\left(\\int_c^d h(y) \\, dy\\right)$$\n\n"
              "**El doble integral se factoriza** en producto de dos integrales simples. Esto solo aplica cuando el integrando se separa Y la región es rectangular."
          )),

        b("ejemplo_resuelto",
          titulo="Integral separable",
          problema_md="Calcular $\\iint_R \\sin x \\cos y \\, dA$ con $R = [0, \\pi/2] \\times [0, \\pi/2]$.",
          pasos=[
              {"accion_md": "**Producto de funciones de una sola variable:**\n\n"
                            "$\\iint_R \\sin x \\cos y \\, dA = \\left(\\int_0^{\\pi/2} \\sin x \\, dx\\right) \\left(\\int_0^{\\pi/2} \\cos y \\, dy\\right)$.",
               "justificacion_md": "Aplicación directa del caso separable.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^{\\pi/2} \\sin x \\, dx = [-\\cos x]_0^{\\pi/2} = -0 + 1 = 1$. Análogo: $\\int_0^{\\pi/2} \\cos y \\, dy = 1$.\n\n"
                            "**Producto:** $1 \\cdot 1 = 1$.",
               "justificacion_md": "Cada integral simple es $1$.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Propiedades de la integral doble",
            body=(
                "**Linealidad:** $\\iint_R [c f + g] \\, dA = c \\iint_R f \\, dA + \\iint_R g \\, dA$.\n\n"
                "**Aditividad de regiones:** si $R = R_1 \\cup R_2$ con $R_1, R_2$ disjuntas (salvo borde):\n\n"
                "$$\\iint_R f \\, dA = \\iint_{R_1} f \\, dA + \\iint_{R_2} f \\, dA$$\n\n"
                "**Comparación:** si $f \\leq g$ en $R$, entonces $\\iint_R f \\leq \\iint_R g$.\n\n"
                "**Acotación:** si $m \\leq f \\leq M$ en $R$ con área $A(R)$:\n\n"
                "$$m \\cdot A(R) \\leq \\iint_R f \\, dA \\leq M \\cdot A(R)$$\n\n"
                "**Área:** $A(R) = \\iint_R 1 \\, dA$ (la integral del integrando constante $1$ da el área de la región)."
            ),
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\iint_R f(x, y) \\, dA$ se puede calcular en cualquier orden si:",
                  "opciones_md": [
                      "$f$ es positiva.",
                      "$R$ es rectangular y $f$ es continua.",
                      "Solo si $f(x, y) = g(x) h(y)$.",
                      "Siempre.",
                  ],
                  "correcta": "B",
                  "pista_md": "Fubini exige $R$ rectangular y $f$ continua (o al menos integrable).",
                  "explicacion_md": (
                      "**Fubini** garantiza igualdad de los dos órdenes para $f$ continua en un rectángulo. En regiones no rectangulares (lección 6.2) ambos órdenes existen pero las integrales internas tienen límites distintos."
                  ),
              },
              {
                  "enunciado_md": "Si $f(x, y) \\geq 0$ en $R$, $\\iint_R f \\, dA$ representa:",
                  "opciones_md": [
                      "Área de $R$",
                      "Volumen bajo $z = f(x, y)$ sobre $R$",
                      "Perímetro de $R$",
                      "Promedio de $f$ en $R$",
                  ],
                  "correcta": "B",
                  "pista_md": "Cada elemento $f \\, dA$ es altura por área de la base.",
                  "explicacion_md": (
                      "**Volumen.** Es el análogo 2D de \"área bajo la curva\" del caso 1D."
                  ),
              },
          ]),

        ej(
            titulo="Volumen bajo un paraboloide",
            enunciado=(
                "Calcula el volumen del sólido bajo $z = 4 - x^2 - y^2$ y sobre el rectángulo $[0, 1] \\times [0, 1]$."
            ),
            pistas=[
                "Verifica que $z \\geq 0$ en el rectángulo: $\\min(4 - x^2 - y^2) = 4 - 1 - 1 = 2 > 0$. ✓",
                "$V = \\iint_R (4 - x^2 - y^2) \\, dA$. Aplica Fubini.",
            ],
            solucion=(
                "$V = \\int_0^1 \\int_0^1 (4 - x^2 - y^2) \\, dy \\, dx$.\n\n"
                "**Interna:** $\\int_0^1 (4 - x^2 - y^2) \\, dy = (4 - x^2) y - \\dfrac{y^3}{3}\\Big|_0^1 = (4 - x^2) - \\dfrac{1}{3} = \\dfrac{11}{3} - x^2$.\n\n"
                "**Externa:** $\\int_0^1 \\left(\\dfrac{11}{3} - x^2\\right) dx = \\dfrac{11}{3} - \\dfrac{1}{3} = \\dfrac{10}{3}$."
            ),
        ),

        ej(
            titulo="Promedio de una función",
            enunciado=(
                "El **valor promedio** de $f$ sobre $R$ es $f_{prom} = \\dfrac{1}{A(R)} \\iint_R f \\, dA$. "
                "Calcula el promedio de $f(x, y) = x + y$ sobre $R = [0, 2] \\times [0, 3]$."
            ),
            pistas=[
                "Área: $A(R) = 6$.",
                "$\\iint_R (x + y) \\, dA$ por Fubini.",
            ],
            solucion=(
                "$\\iint_R (x + y) \\, dA = \\int_0^2 \\int_0^3 (x + y) \\, dy \\, dx = \\int_0^2 [xy + y^2/2]_0^3 \\, dx = \\int_0^2 (3x + 9/2) \\, dx = 6 + 9 = 15$.\n\n"
                "$f_{prom} = 15/6 = 5/2$. **Verificación:** $f$ es lineal, así su promedio es $f$ evaluado en el centro $(1, 3/2)$: $1 + 3/2 = 5/2$. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir integral doble con producto de integrales** cuando el integrando NO se separa: $\\iint x y \\, dA = (\\int x \\, dx)(\\int y \\, dy)$ vale, pero $\\iint (x+y) \\, dA$ NO se factoriza así.",
              "**Olvidar que el orden importa cuando hay límites variables.** En rectángulos no, pero en regiones generales sí.",
              "**Confundir $dA$ con $dx \\, dy$.** Son iguales solo en coordenadas cartesianas. En polares es $r \\, dr \\, d\\theta$.",
              "**Tratar $x$ como variable** al integrar respecto a $y$. Es **constante** en la integral interna.",
              "**Calcular el volumen sin verificar $f \\geq 0$.** Si $f$ cambia signo, $\\iint f \\, dA$ es **volumen con signo**, no el volumen geométrico.",
          ]),

        b("resumen",
          puntos_md=[
              "**Integral doble:** $\\iint_R f \\, dA$ — límite de sumas de Riemann en 2D.",
              "**Fubini:** sobre rectángulos, $\\iint = \\int\\int$ en cualquier orden (si $f$ continua).",
              "**Caso separable:** $f = g(x) h(y)$ → $\\iint = (\\int g)(\\int h)$.",
              "**Volumen:** si $f \\geq 0$, la integral es el volumen bajo $z = f(x, y)$.",
              "**Área:** $\\iint_R 1 \\, dA$ es el área de $R$.",
              "**Próxima lección:** regiones no rectangulares (Tipo I y II).",
          ]),
    ]
    return {
        "id": "lec-mvar-6-1-dobles",
        "title": "Integrales dobles",
        "description": "Integral doble sobre rectángulos: definición, teorema de Fubini, propiedades y volumen bajo una superficie.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 6.2 Regiones generales
# =====================================================================
def lesson_6_2():
    blocks = [
        b("texto", body_md=(
            "Casi nunca queremos integrar sobre un rectángulo. Lo más común son **regiones acotadas por curvas**: "
            "círculos, parábolas, intersecciones, etc. Para esas, hay dos esquemas estándar — **Tipo I** "
            "(verticalmente simple) y **Tipo II** (horizontalmente simple) — que reducen la integral doble "
            "a una integral iterada con **límites variables**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Identificar regiones de **Tipo I** y **Tipo II** y montar la integral correspondiente.\n"
            "- Elegir el orden que **simplifica** la integral.\n"
            "- **Cambiar el orden** de integración cuando uno se atasca.\n"
            "- Calcular áreas de regiones planas con $\\iint_R 1 \\, dA$."
        )),

        b("definicion",
          titulo="Regiones Tipo I y Tipo II",
          body_md=(
              "**Tipo I (verticalmente simple):**\n\n"
              "$$D = \\{(x, y) : a \\leq x \\leq b, \\; g_1(x) \\leq y \\leq g_2(x)\\}$$\n\n"
              "Para cada $x$ fijo, $y$ varía entre dos curvas $g_1(x)$ (frontera inferior) y $g_2(x)$ (frontera superior). Imagina **rebanadas verticales**.\n\n"
              "$$\\iint_D f \\, dA = \\int_a^b \\int_{g_1(x)}^{g_2(x)} f(x, y) \\, dy \\, dx$$\n\n"
              "**Tipo II (horizontalmente simple):**\n\n"
              "$$D = \\{(x, y) : c \\leq y \\leq d, \\; h_1(y) \\leq x \\leq h_2(y)\\}$$\n\n"
              "Para cada $y$ fijo, $x$ varía entre $h_1(y)$ y $h_2(y)$. **Rebanadas horizontales**.\n\n"
              "$$\\iint_D f \\, dA = \\int_c^d \\int_{h_1(y)}^{h_2(y)} f(x, y) \\, dx \\, dy$$"
          )),

        fig(
            "Comparación de regiones Tipo I y Tipo II en el plano. PANEL IZQUIERDO: una región "
            "acotada por dos curvas y = g₁(x) (inferior) y y = g₂(x) (superior) con x entre a y b. "
            "Trazar varias rebanadas verticales (líneas rectas verticales) cortando la región, "
            "cada una desde g₁(x) hasta g₂(x). Etiquetas: 'a', 'b', 'y = g₁(x)', 'y = g₂(x)', "
            "'Tipo I'. PANEL DERECHO: una región acotada por dos curvas x = h₁(y) (izquierda) y x = "
            "h₂(y) (derecha) con y entre c y d. Trazar varias rebanadas horizontales. Etiquetas: "
            "'c', 'd', 'x = h₁(y)', 'x = h₂(y)', 'Tipo II'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Tipo I — región triangular",
          problema_md=(
              "Calcular $\\iint_D xy \\, dA$ donde $D$ es el triángulo con vértices $(0, 0), (2, 0), (2, 2)$."
          ),
          pasos=[
              {"accion_md": "**Identificar la región:** $D$ es un triángulo. Como Tipo I: $0 \\leq x \\leq 2$, $0 \\leq y \\leq x$.\n\n"
                            "(La frontera inferior es $y = 0$, la superior es la recta $y = x$ que va de $(0,0)$ a $(2, 2)$.)",
               "justificacion_md": "Visualizar la región. La hipotenusa va por $y = x$.",
               "es_resultado": False},
              {"accion_md": "**Plantear:**\n\n$\\iint_D xy \\, dA = \\int_0^2 \\int_0^x xy \\, dy \\, dx$.",
               "justificacion_md": "Tipo I con límites variables en $y$.",
               "es_resultado": False},
              {"accion_md": "**Interna:** $\\int_0^x xy \\, dy = x \\cdot \\dfrac{y^2}{2}\\Big|_0^x = \\dfrac{x^3}{2}$.\n\n"
                            "**Externa:** $\\int_0^2 \\dfrac{x^3}{2} \\, dx = \\dfrac{x^4}{8}\\Big|_0^2 = 2$.",
               "justificacion_md": "Cálculo directo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Tipo II por elección práctica",
          problema_md=(
              "Calcular $\\iint_D y \\, dA$ donde $D$ es la región acotada por $x = y^2$ y $x = 2y$."
          ),
          pasos=[
              {"accion_md": "**Intersecciones:** $y^2 = 2y \\implies y(y - 2) = 0 \\implies y = 0, y = 2$. Puntos: $(0, 0)$ y $(4, 2)$.",
               "justificacion_md": "Encontrar dónde se cruzan las curvas para los límites.",
               "es_resultado": False},
              {"accion_md": "**Como Tipo II** (más natural): $0 \\leq y \\leq 2$, $y^2 \\leq x \\leq 2y$.\n\n"
                            "(Para $y$ entre 0 y 2, la parábola $x = y^2$ está a la izquierda de la recta $x = 2y$.)",
               "justificacion_md": "Las dos curvas son **funciones de $y$**, así Tipo II es natural. Como Tipo I tendríamos que partir el dominio.",
               "es_resultado": False},
              {"accion_md": "$\\iint_D y \\, dA = \\int_0^2 \\int_{y^2}^{2y} y \\, dx \\, dy = \\int_0^2 y(2y - y^2) \\, dy = \\int_0^2 (2y^2 - y^3) \\, dy$.\n\n"
                            "$= \\dfrac{2y^3}{3} - \\dfrac{y^4}{4}\\Big|_0^2 = \\dfrac{16}{3} - 4 = \\dfrac{4}{3}$.",
               "justificacion_md": "**Lección:** elegir el orden adecuado evita partir el dominio.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Cambiar el orden de integración",
          body_md=(
              "A veces la integral interna **no tiene antiderivada elemental** en el orden dado. "
              "Cambiando el orden, el integrando puede volverse manejable.\n\n"
              "**Procedimiento para cambiar de orden:**\n\n"
              "1. **Dibujar la región** $D$ a partir de los límites originales.\n"
              "2. **Re-describir** $D$ con el orden contrario (Tipo I ↔ Tipo II).\n"
              "3. **Reescribir** la integral con los nuevos límites.\n\n"
              "**Caso clásico:** $\\int_0^1 \\int_x^1 e^{-y^2} \\, dy \\, dx$ — la antiderivada de $e^{-y^2}$ no es elemental, pero al cambiar el orden el cálculo se vuelve trivial."
          )),

        b("ejemplo_resuelto",
          titulo="Cambio de orden clásico",
          problema_md=(
              "Calcular $\\int_0^1 \\int_x^1 e^{-y^2} \\, dy \\, dx$ cambiando el orden."
          ),
          pasos=[
              {"accion_md": "**Región original (Tipo I):** $0 \\leq x \\leq 1$, $x \\leq y \\leq 1$.\n\n"
                            "Es el triángulo arriba de $y = x$ dentro de $[0, 1] \\times [0, 1]$.",
               "justificacion_md": "Dibujar la región: triángulo con vértices $(0,0), (0,1), (1,1)$.",
               "es_resultado": False},
              {"accion_md": "**Re-describir como Tipo II:** $0 \\leq y \\leq 1$, $0 \\leq x \\leq y$.\n\n"
                            "(Para cada $y$ fijo, $x$ va desde $0$ hasta $y$.)",
               "justificacion_md": "La condición $x \\leq y$ se reescribe como $0 \\leq x \\leq y$ para $y$ entre $0$ y $1$.",
               "es_resultado": False},
              {"accion_md": "**Nueva integral:**\n\n$\\int_0^1 \\int_0^y e^{-y^2} \\, dx \\, dy = \\int_0^1 e^{-y^2} \\cdot y \\, dy$.\n\n"
                            "Ahora **la interna es trivial** ($e^{-y^2}$ no depende de $x$, así su integral en $x$ es $e^{-y^2} \\cdot y$).",
               "justificacion_md": "**Truco fundamental:** al cambiar el orden, el factor $y$ que sale aniquila la dificultad.",
               "es_resultado": False},
              {"accion_md": "**Sustitución** $u = y^2$, $du = 2y \\, dy$:\n\n"
                            "$\\int_0^1 y e^{-y^2} \\, dy = \\dfrac{1}{2} \\int_0^1 e^{-u} \\, du = \\dfrac{1}{2}(1 - e^{-1}) = \\dfrac{1 - 1/e}{2}$.",
               "justificacion_md": "**Lección poderosa:** lo que parecía imposible se vuelve directo solo cambiando el orden.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Área de una región como integral doble",
          body_md=(
              "El **área** de una región $D \\subset \\mathbb{R}^2$ es:\n\n"
              "$$A(D) = \\iint_D 1 \\, dA$$\n\n"
              "**Como Tipo I:** $A(D) = \\int_a^b [g_2(x) - g_1(x)] \\, dx$ (recupera la fórmula del cálculo de una variable: \"arriba menos abajo\").\n\n"
              "**Como Tipo II:** $A(D) = \\int_c^d [h_2(y) - h_1(y)] \\, dy$ (\"derecha menos izquierda\")."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para una región Tipo I $D$, la integral doble es:",
                  "opciones_md": [
                      "$\\int_c^d \\int_a^b f \\, dx \\, dy$",
                      "$\\int_a^b \\int_{g_1(x)}^{g_2(x)} f \\, dy \\, dx$",
                      "$\\int_{g_1}^{g_2} \\int_a^b f \\, dx \\, dy$",
                      "$\\int_a^b \\int_a^b f \\, dx \\, dy$",
                  ],
                  "correcta": "B",
                  "pista_md": "En Tipo I, $x$ va de constantes y $y$ de funciones de $x$.",
                  "explicacion_md": (
                      "**Tipo I:** $x$ es la variable externa con límites constantes; $y$ varía entre dos funciones de $x$. La interna se evalúa primero."
                  ),
              },
              {
                  "enunciado_md": "¿Cuándo conviene cambiar el orden de integración?",
                  "opciones_md": [
                      "Siempre.",
                      "Cuando la integral interna no tiene antiderivada elemental.",
                      "Cuando $f$ es separable.",
                      "Cuando la región es Tipo I.",
                  ],
                  "correcta": "B",
                  "pista_md": "El cambio de orden es una herramienta para volver tratable lo intratable.",
                  "explicacion_md": (
                      "Cambiar el orden expone factores que aniquilan integrales no elementales. El caso clásico $e^{-y^2}$ es el ejemplo prototipo."
                  ),
              },
          ]),

        ej(
            titulo="Tipo I sobre región acotada",
            enunciado=(
                "Calcula $\\iint_D 2x \\, dA$ donde $D$ es la región acotada por $y = x^2$ e $y = 2x$."
            ),
            pistas=[
                "Intersecciones: $x^2 = 2x \\implies x = 0, 2$.",
                "Para $0 \\leq x \\leq 2$, la recta $y = 2x$ está arriba de la parábola $y = x^2$.",
                "Tipo I: $\\int_0^2 \\int_{x^2}^{2x} 2x \\, dy \\, dx$.",
            ],
            solucion=(
                "$\\int_0^2 \\int_{x^2}^{2x} 2x \\, dy \\, dx = \\int_0^2 2x(2x - x^2) \\, dx = \\int_0^2 (4x^2 - 2x^3) \\, dx$.\n\n"
                "$= \\dfrac{4x^3}{3} - \\dfrac{x^4}{2}\\Big|_0^2 = \\dfrac{32}{3} - 8 = \\dfrac{8}{3}$."
            ),
        ),

        ej(
            titulo="Cambio de orden",
            enunciado=(
                "Cambia el orden y evalúa $\\int_0^1 \\int_{\\sqrt{x}}^{1} \\sin(y^3) \\, dy \\, dx$."
            ),
            pistas=[
                "Región: $0 \\leq x \\leq 1$, $\\sqrt{x} \\leq y \\leq 1$. Equivalente: $\\sqrt{x} \\leq y \\iff x \\leq y^2$.",
                "Como Tipo II: $0 \\leq y \\leq 1$, $0 \\leq x \\leq y^2$.",
                "Después de cambiar, queda $\\int_0^1 \\sin(y^3) \\cdot y^2 \\, dy$. Sustitución $u = y^3$.",
            ],
            solucion=(
                "**Nueva integral:** $\\int_0^1 \\int_0^{y^2} \\sin(y^3) \\, dx \\, dy = \\int_0^1 y^2 \\sin(y^3) \\, dy$.\n\n"
                "Sustitución $u = y^3$, $du = 3y^2 \\, dy$:\n\n"
                "$\\dfrac{1}{3} \\int_0^1 \\sin u \\, du = \\dfrac{1}{3}[-\\cos u]_0^1 = \\dfrac{1 - \\cos 1}{3}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Mezclar variables en los límites.** En Tipo I, los límites internos son funciones de $x$, no de $y$.",
              "**No dibujar la región** antes de plantear los límites. La geometría es esencial.",
              "**Olvidar partir el dominio** cuando una de las fronteras cambia de descripción.",
              "**Cambiar el orden sin re-describir la región.** Hay que pasar por la geometría — no basta intercambiar $dx \\, dy$ por $dy \\, dx$.",
              "**Considerar que cualquier región es Tipo I y II equivalentes.** Algunas regiones son más naturales en uno solo, o requieren partirse en pedazos.",
          ]),

        b("resumen",
          puntos_md=[
              "**Tipo I:** $a \\leq x \\leq b, g_1(x) \\leq y \\leq g_2(x)$ → $\\int_a^b \\int_{g_1}^{g_2} f \\, dy \\, dx$.",
              "**Tipo II:** $c \\leq y \\leq d, h_1(y) \\leq x \\leq h_2(y)$ → $\\int_c^d \\int_{h_1}^{h_2} f \\, dx \\, dy$.",
              "**Elegir el orden** según la geometría de la región y la dificultad del integrando.",
              "**Cambiar el orden:** dibujar región → re-describir → reescribir.",
              "**Truco poderoso:** integrales con $e^{-y^2}, \\sin(y^3)$, etc., en el orden equivocado son intratables.",
              "**Área:** $\\iint_D 1 \\, dA$.",
              "**Próxima lección:** coordenadas polares — el sistema natural para regiones circulares.",
          ]),
    ]
    return {
        "id": "lec-mvar-6-2-regiones-generales",
        "title": "Regiones generales",
        "description": "Integrales dobles sobre regiones Tipo I y Tipo II, cambio de orden y área como integral doble.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 6.3 Coordenadas polares
# =====================================================================
def lesson_6_3():
    blocks = [
        b("texto", body_md=(
            "Cuando una región tiene **simetría circular** (discos, anillos, sectores), las **coordenadas polares** "
            "$(r, \\theta)$ son mucho más naturales que las cartesianas. La integral doble se reescribe con un "
            "elemento de área distinto: $dA = r \\, dr \\, d\\theta$.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Convertir entre coordenadas cartesianas y polares.\n"
            "- Reconocer cuándo polares es ventajoso.\n"
            "- Aplicar la fórmula $dA = r \\, dr \\, d\\theta$.\n"
            "- Calcular integrales sobre discos, anillos y sectores."
        )),

        b("definicion",
          titulo="Coordenadas polares",
          body_md=(
              "Un punto del plano $(x, y) \\neq (0, 0)$ se describe en polares por:\n\n"
              "$$x = r \\cos\\theta, \\quad y = r \\sin\\theta$$\n\n"
              "donde $r > 0$ es la distancia al origen y $\\theta$ es el ángulo medido desde el eje $x$ positivo (en radianes).\n\n"
              "**Conversión inversa:**\n\n"
              "$$r = \\sqrt{x^2 + y^2}, \\quad \\theta = \\arctan(y/x) \\text{ (con cuidado del cuadrante)}$$\n\n"
              "**Identidades útiles:** $x^2 + y^2 = r^2$, $r \\, dr = x \\, dx + y \\, dy$ (diferencial de $r^2/2$)."
          )),

        b("teorema",
          nombre="Cambio a polares en integrales dobles",
          enunciado_md=(
              "Si $D$ es una región del plano descrita en polares por $\\alpha \\leq \\theta \\leq \\beta$, $h_1(\\theta) \\leq r \\leq h_2(\\theta)$, entonces:\n\n"
              "$$\\iint_D f(x, y) \\, dA = \\int_\\alpha^\\beta \\int_{h_1(\\theta)}^{h_2(\\theta)} f(r\\cos\\theta, r\\sin\\theta) \\cdot r \\, dr \\, d\\theta$$\n\n"
              "**Lo crucial: el factor $r$ extra.** $dA = r \\, dr \\, d\\theta$, no $dr \\, d\\theta$.\n\n"
              "**¿Por qué $r$?** El \"rectángulo polar\" $[r, r+dr] \\times [\\theta, \\theta+d\\theta]$ es geométricamente un trozo de anillo de radio $r$ y ancho $dr$. Su área aproximada es $r \\, d\\theta \\cdot dr$ (largo del arco $\\times$ ancho)."
          ),
          demostracion_md=(
              "Es un caso particular del teorema de cambio de variables (lección 6.7). El factor $r$ es el valor absoluto del **jacobiano** de la transformación $(r, \\theta) \\mapsto (x, y)$:\n\n"
              "$\\dfrac{\\partial(x, y)}{\\partial(r, \\theta)} = \\det \\begin{pmatrix} \\cos\\theta & -r\\sin\\theta \\\\ \\sin\\theta & r\\cos\\theta \\end{pmatrix} = r\\cos^2\\theta + r\\sin^2\\theta = r$"
          )),

        fig(
            "Elemento de área en coordenadas polares. Plano 2D con origen marcado. Mostrar un sector "
            "polar pequeño (un 'rectángulo polar') destacado, formado por dos arcos circulares "
            "concéntricos de radios r y r+dr (en color teal) y dos rayos saliendo del origen en "
            "ángulos θ y θ+dθ (en color teal). El área sombreada en color ámbar translúcido. "
            "Etiquetas: 'r', 'r + dr', 'θ', 'θ + dθ', 'dA = r dr dθ' (en el centro del sector). "
            "Una flecha curvada mostrando el ancho del arco r·dθ. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Integrar sobre un disco",
          problema_md=(
              "Calcular $\\iint_D (x^2 + y^2) \\, dA$ donde $D$ es el disco $x^2 + y^2 \\leq 4$."
          ),
          pasos=[
              {"accion_md": "**En polares:** $D = \\{(r, \\theta) : 0 \\leq r \\leq 2, 0 \\leq \\theta \\leq 2\\pi\\}$. Integrando $x^2 + y^2 = r^2$.",
               "justificacion_md": "El disco completo se cubre con $\\theta$ de $0$ a $2\\pi$ y $r$ de $0$ a $2$.",
               "es_resultado": False},
              {"accion_md": "**Aplicar:**\n\n"
                            "$\\iint_D r^2 \\, dA = \\int_0^{2\\pi} \\int_0^2 r^2 \\cdot r \\, dr \\, d\\theta = \\int_0^{2\\pi} \\int_0^2 r^3 \\, dr \\, d\\theta$.",
               "justificacion_md": "**No olvidar el factor $r$ extra de $dA$.**",
               "es_resultado": False},
              {"accion_md": "$\\int_0^2 r^3 \\, dr = 4$. $\\int_0^{2\\pi} 4 \\, d\\theta = 8\\pi$.\n\n"
                            "**Resultado:** $8\\pi$.",
               "justificacion_md": "**Comparación:** intentar lo mismo en cartesianas $\\iint_D (x^2+y^2) dA$ con $D$ disco da una integral mucho más complicada.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Anillo y sector",
          problema_md=(
              "Calcular el área del anillo $1 \\leq x^2 + y^2 \\leq 4$."
          ),
          pasos=[
              {"accion_md": "**En polares:** $1 \\leq r \\leq 2, 0 \\leq \\theta \\leq 2\\pi$. Integrar $1$.",
               "justificacion_md": "Anillo entre radios 1 y 2.",
               "es_resultado": False},
              {"accion_md": "$A = \\int_0^{2\\pi} \\int_1^2 1 \\cdot r \\, dr \\, d\\theta = \\int_0^{2\\pi} \\dfrac{3}{2} \\, d\\theta = 3\\pi$.\n\n"
                            "**Verificación:** $\\pi(2)^2 - \\pi(1)^2 = 4\\pi - \\pi = 3\\pi$. ✓",
               "justificacion_md": "Coincide con la fórmula geométrica de área de anillo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Integral de Gauss (truco famoso)",
          problema_md=(
              "Mostrar que $\\int_{-\\infty}^\\infty e^{-x^2} \\, dx = \\sqrt{\\pi}$."
          ),
          pasos=[
              {"accion_md": "**Truco:** llamemos $I$ a esa integral. Entonces:\n\n"
                            "$I^2 = \\left(\\int_{-\\infty}^\\infty e^{-x^2} dx\\right)\\left(\\int_{-\\infty}^\\infty e^{-y^2} dy\\right) = \\iint_{\\mathbb{R}^2} e^{-(x^2+y^2)} dA$.",
               "justificacion_md": "Producto de integrales unidimensionales = integral doble (caso separable).",
               "es_resultado": False},
              {"accion_md": "**Pasamos a polares:** $x^2 + y^2 = r^2$, $dA = r \\, dr \\, d\\theta$, $r \\in [0, \\infty)$, $\\theta \\in [0, 2\\pi]$.\n\n"
                            "$I^2 = \\int_0^{2\\pi} \\int_0^\\infty e^{-r^2} r \\, dr \\, d\\theta$.",
               "justificacion_md": "Polares simplifican enormemente.",
               "es_resultado": False},
              {"accion_md": "**Sustitución** $u = r^2$, $du = 2r \\, dr$: $\\int_0^\\infty e^{-r^2} r \\, dr = \\dfrac{1}{2}\\int_0^\\infty e^{-u} \\, du = \\dfrac{1}{2}$.\n\n"
                            "$I^2 = \\int_0^{2\\pi} \\dfrac{1}{2} \\, d\\theta = \\pi$. **Por tanto $I = \\sqrt{\\pi}$.**",
               "justificacion_md": "**Resultado fundamental** de probabilidad y estadística (la distribución normal). Sin polares, esta integral no se puede calcular.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Cuándo conviene polares?",
          body_md=(
              "**Polares son ideales cuando:**\n\n"
              "- La **región** tiene simetría circular (discos, anillos, sectores).\n"
              "- El **integrando** depende de $x^2 + y^2$ o $\\sqrt{x^2+y^2}$.\n"
              "- Aparecen $e^{-(x^2+y^2)}$, $1/(x^2+y^2)$, $\\sin(x^2+y^2)$, etc.\n\n"
              "**No conviene** cuando la región es rectangular o triangular sin relación con círculos. "
              "Ejemplos donde polares es contraproducente: regiones como $[0, 1] \\times [0, 1]$ se vuelven complicadas."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El elemento $dA$ en coordenadas polares es:",
                  "opciones_md": [
                      "$dr \\, d\\theta$",
                      "$r \\, dr \\, d\\theta$",
                      "$r^2 \\, dr \\, d\\theta$",
                      "$d\\theta \\, dr$",
                  ],
                  "correcta": "B",
                  "pista_md": "El factor $r$ viene del Jacobiano de la transformación.",
                  "explicacion_md": (
                      "$dA = r \\, dr \\, d\\theta$. Sin el factor $r$ las áreas estarían mal calculadas. **Es el error más común al pasar a polares.**"
                  ),
              },
              {
                  "enunciado_md": "Para integrar sobre $\\{(x, y) : x^2 + y^2 \\leq 1, y \\geq 0\\}$ (semidisco superior):",
                  "opciones_md": [
                      "$\\theta \\in [0, 2\\pi]$",
                      "$\\theta \\in [0, \\pi]$",
                      "$\\theta \\in [-\\pi/2, \\pi/2]$",
                      "$\\theta \\in [0, \\pi/2]$",
                  ],
                  "correcta": "B",
                  "pista_md": "$y \\geq 0$ corresponde al semiplano superior, ángulos de $0$ a $\\pi$.",
                  "explicacion_md": (
                      "El semiplano superior $y \\geq 0$ es donde $\\sin\\theta \\geq 0$, es decir $\\theta \\in [0, \\pi]$."
                  ),
              },
          ]),

        ej(
            titulo="Volumen sobre disco",
            enunciado=(
                "Calcula el volumen bajo $z = 4 - x^2 - y^2$ y sobre el disco $x^2 + y^2 \\leq 4$."
            ),
            pistas=[
                "Pasa a polares: integrando $4 - r^2$, región $r \\in [0, 2], \\theta \\in [0, 2\\pi]$.",
                "Recuerda multiplicar por $r$.",
            ],
            solucion=(
                "$V = \\int_0^{2\\pi} \\int_0^2 (4 - r^2) r \\, dr \\, d\\theta = \\int_0^{2\\pi} \\int_0^2 (4r - r^3) \\, dr \\, d\\theta$.\n\n"
                "Interna: $[2r^2 - r^4/4]_0^2 = 8 - 4 = 4$. Externa: $\\int_0^{2\\pi} 4 \\, d\\theta = 8\\pi$."
            ),
        ),

        ej(
            titulo="Sector polar",
            enunciado=(
                "Calcula $\\iint_D \\sin(x^2 + y^2) \\, dA$ donde $D$ es el sector $0 \\leq \\theta \\leq \\pi/4$, $0 \\leq r \\leq 1$."
            ),
            pistas=[
                "Sin polares no es elemental. Con polares, la integral se vuelve manejable.",
                "Sustitución $u = r^2$.",
            ],
            solucion=(
                "$\\int_0^{\\pi/4} \\int_0^1 \\sin(r^2) r \\, dr \\, d\\theta$.\n\n"
                "Interna: $u = r^2$, $du = 2r \\, dr$. $\\dfrac{1}{2}\\int_0^1 \\sin u \\, du = \\dfrac{1 - \\cos 1}{2}$.\n\n"
                "Externa: $\\int_0^{\\pi/4} \\dfrac{1 - \\cos 1}{2} \\, d\\theta = \\dfrac{(1 - \\cos 1)\\pi}{8}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $r$** del elemento de área. Sin él, los resultados están mal.",
              "**Confundir $\\theta$ con la pendiente.** $\\theta$ es ángulo, no $\\arctan$ de la pendiente.",
              "**Limitar $\\theta$ siempre a $[0, 2\\pi]$.** Para sectores o regiones parciales, los límites de $\\theta$ pueden ser más restrictivos.",
              "**Aplicar polares a regiones rectangulares.** Suele complicar; mantener cartesianas.",
              "**No simplificar el integrando** después de pasar a polares. $x^2 + y^2 = r^2$ es la simplificación más común.",
          ]),

        b("resumen",
          puntos_md=[
              "**Polares:** $x = r\\cos\\theta, y = r\\sin\\theta$, $r \\geq 0$, $\\theta \\in [0, 2\\pi)$.",
              "**Elemento de área:** $dA = r \\, dr \\, d\\theta$.",
              "**Conviene cuando:** región circular o integrando con $x^2 + y^2$.",
              "**Aplicación clásica:** integral de Gauss $\\int e^{-x^2} dx = \\sqrt{\\pi}$.",
              "**Próxima lección:** integrales triples sobre cajas y regiones generales.",
          ]),
    ]
    return {
        "id": "lec-mvar-6-3-polares",
        "title": "Coordenadas polares",
        "description": "Cambio a coordenadas polares en integrales dobles, $dA = r \\, dr \\, d\\theta$, integral de Gauss.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 6.4 Integrales triples
# =====================================================================
def lesson_6_4():
    blocks = [
        b("texto", body_md=(
            "Las **integrales triples** generalizan las dobles a tres variables. La idea es la misma: "
            "sumas de Riemann, Fubini iterado, propiedades. Lo nuevo: ahora integramos sobre **sólidos** "
            "(regiones de $\\mathbb{R}^3$) y el resultado representa **volúmenes 4D** o, más prácticamente, "
            "**masas, centros de masa, momentos de inercia** de cuerpos sólidos.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir $\\iiint_E f \\, dV$ y reconocer su significado.\n"
            "- Aplicar **Fubini en 3D** sobre cajas y regiones generales.\n"
            "- Manejar el **orden de integración** (seis órdenes posibles).\n"
            "- Calcular **volúmenes de sólidos** con $\\iiint_E 1 \\, dV$."
        )),

        b("definicion",
          titulo="Integral triple sobre una caja",
          body_md=(
              "Sea $B = [a_1, b_1] \\times [a_2, b_2] \\times [a_3, b_3]$ una caja rectangular. La **integral triple** de $f$ sobre $B$ es:\n\n"
              "$$\\iiint_B f(x, y, z) \\, dV = \\lim_{l, m, n \\to \\infty} \\sum_{i, j, k} f(P^*_{ijk}) \\Delta V$$\n\n"
              "donde $\\Delta V = \\Delta x \\Delta y \\Delta z$ y la suma es sobre subcajas.\n\n"
              "**Si $f$ es continua, es integrable.**\n\n"
              "**Notación:** $dV = dx \\, dy \\, dz$ (en cartesianas)."
          )),

        b("teorema",
          nombre="Fubini en 3D",
          enunciado_md=(
              "Sobre una caja $B$ con $f$ continua:\n\n"
              "$$\\iiint_B f \\, dV = \\int_{a_1}^{b_1} \\int_{a_2}^{b_2} \\int_{a_3}^{b_3} f(x, y, z) \\, dz \\, dy \\, dx$$\n\n"
              "y **cualquiera de los $6$ órdenes** $(dx \\, dy \\, dz, dx \\, dz \\, dy, \\ldots)$ da el mismo resultado.\n\n"
              "Para regiones generales, los límites internos se vuelven funciones, pero la idea de iterar tres integrales se mantiene."
          )),

        b("ejemplo_resuelto",
          titulo="Integral triple sobre una caja",
          problema_md=(
              "Calcular $\\iiint_B xyz \\, dV$ sobre $B = [0, 1] \\times [0, 2] \\times [0, 3]$."
          ),
          pasos=[
              {"accion_md": "**Caso separable:**\n\n"
                            "$\\iiint_B xyz \\, dV = \\left(\\int_0^1 x \\, dx\\right)\\left(\\int_0^2 y \\, dy\\right)\\left(\\int_0^3 z \\, dz\\right)$.",
               "justificacion_md": "El integrando es producto de funciones de cada variable.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^1 x \\, dx = 1/2$. $\\int_0^2 y \\, dy = 2$. $\\int_0^3 z \\, dz = 9/2$.\n\n"
                            "**Producto:** $(1/2)(2)(9/2) = 9/2$.",
               "justificacion_md": "Producto de tres integrales simples.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Regiones generales en 3D",
          body_md=(
              "Una región $E \\subset \\mathbb{R}^3$ se describe típicamente como un \"prisma\" entre dos superficies:\n\n"
              "**Tipo 1 (proyectado al plano $xy$):**\n\n"
              "$$E = \\{(x, y, z) : (x, y) \\in D, \\; u_1(x, y) \\leq z \\leq u_2(x, y)\\}$$\n\n"
              "donde $D$ es la \"sombra\" de $E$ en el plano $xy$, y $u_1, u_2$ son las superficies inferior y superior.\n\n"
              "$$\\iiint_E f \\, dV = \\iint_D \\left[\\int_{u_1(x,y)}^{u_2(x,y)} f \\, dz\\right] dA$$\n\n"
              "**Análogamente** se puede proyectar al plano $xz$ o $yz$ — seis configuraciones posibles."
          )),

        b("ejemplo_resuelto",
          titulo="Integral sobre un sólido",
          problema_md=(
              "Calcular $\\iiint_E z \\, dV$ donde $E$ es el sólido acotado por $z = 0$, $z = y$, $y = 1 - x^2$, $y = 0$."
          ),
          pasos=[
              {"accion_md": "**Identificar:** El sólido está sobre el plano $z = 0$, bajo el plano $z = y$, con $(x, y)$ en la región $D$ del plano $xy$ acotada por $y = 0$ y $y = 1 - x^2$ (parábola).\n\n"
                            "$D = \\{(x, y) : -1 \\leq x \\leq 1, 0 \\leq y \\leq 1 - x^2\\}$.",
               "justificacion_md": "Visualizar el sólido. La proyección a $xy$ es la región bajo la parábola.",
               "es_resultado": False},
              {"accion_md": "**Plantear:**\n\n"
                            "$\\iiint_E z \\, dV = \\int_{-1}^1 \\int_0^{1 - x^2} \\int_0^y z \\, dz \\, dy \\, dx$.",
               "justificacion_md": "Tres integrales iteradas. La interna $z$ va de $0$ a $y$.",
               "es_resultado": False},
              {"accion_md": "**Interna en $z$:** $\\int_0^y z \\, dz = y^2/2$.\n\n"
                            "**En $y$:** $\\int_0^{1-x^2} \\dfrac{y^2}{2} \\, dy = \\dfrac{(1-x^2)^3}{6}$.\n\n"
                            "**En $x$ (por simetría, integrar $0$ a $1$ y multiplicar por $2$):** $\\dfrac{2}{6}\\int_0^1 (1-x^2)^3 \\, dx$.",
               "justificacion_md": "**Notar:** $(1-x^2)^3$ es par, así $\\int_{-1}^1 = 2\\int_0^1$.",
               "es_resultado": False},
              {"accion_md": "**Última:** $\\int_0^1 (1 - x^2)^3 \\, dx = \\int_0^1 (1 - 3x^2 + 3x^4 - x^6) \\, dx = 1 - 1 + 3/5 - 1/7 = \\dfrac{16}{35}$.\n\n"
                            "$\\iiint_E z \\, dV = \\dfrac{1}{3} \\cdot \\dfrac{16}{35} = \\dfrac{16}{105}$.",
               "justificacion_md": "**Lección:** descomponer una integral triple en tres iteradas y avanzar paso por paso.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Volumen como integral triple",
          body_md=(
              "El **volumen** de un sólido $E$ es:\n\n"
              "$$V(E) = \\iiint_E 1 \\, dV$$\n\n"
              "Es decir, integrar la función constante $1$. Para regiones Tipo 1:\n\n"
              "$$V(E) = \\iint_D [u_2(x, y) - u_1(x, y)] \\, dA$$\n\n"
              "que recupera la fórmula 2D \"superficie superior menos inferior, integrada sobre la sombra\". **Es un mecanismo más general que los métodos de discos/anillos del capítulo 3 de Cálculo Integral.**"
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Sobre una caja $[0,1]^3$, $\\iiint x^2 y^2 z^2 \\, dV = ?$",
                  "opciones_md": ["$1$", "$1/27$", "$1/9$", "$1/8$"],
                  "correcta": "B",
                  "pista_md": "Caso separable: producto de tres integrales iguales.",
                  "explicacion_md": (
                      "$(\\int_0^1 x^2 \\, dx)^3 = (1/3)^3 = 1/27$."
                  ),
              },
              {
                  "enunciado_md": "El volumen de $E$ es:",
                  "opciones_md": [
                      "$\\iiint_E V \\, dV$",
                      "$\\iiint_E 1 \\, dV$",
                      "$\\iiint_E x \\, dV$",
                      "$\\iiint_{\\partial E} dA$",
                  ],
                  "correcta": "B",
                  "pista_md": "Análogo a $\\iint_D 1 \\, dA$ para área en 2D.",
                  "explicacion_md": (
                      "Volumen = integrar el integrando constante 1 sobre el sólido."
                  ),
              },
          ]),

        ej(
            titulo="Volumen de un tetraedro",
            enunciado=(
                "Calcula el volumen del tetraedro acotado por los planos $x = 0$, $y = 0$, $z = 0$ y $x + y + z = 1$."
            ),
            pistas=[
                "$E = \\{(x,y,z) : x \\geq 0, y \\geq 0, z \\geq 0, x+y+z \\leq 1\\}$.",
                "Como Tipo 1: $0 \\leq x \\leq 1$, $0 \\leq y \\leq 1 - x$, $0 \\leq z \\leq 1 - x - y$.",
            ],
            solucion=(
                "$V = \\int_0^1 \\int_0^{1-x} \\int_0^{1-x-y} 1 \\, dz \\, dy \\, dx$.\n\n"
                "Interna: $1 - x - y$. Después: $\\int_0^{1-x}(1 - x - y) \\, dy = (1-x)y - y^2/2|_0^{1-x} = \\dfrac{(1-x)^2}{2}$.\n\n"
                "Final: $\\int_0^1 \\dfrac{(1-x)^2}{2} \\, dx = \\dfrac{1}{6}$.\n\n"
                "**Resultado clásico:** volumen del simplex unitario en 3D es $1/6$. (Generaliza a $1/n!$ en $\\mathbb{R}^n$.)"
            ),
        ),

        ej(
            titulo="Triple separable",
            enunciado=(
                "Calcula $\\iiint_B (x^2 + y^2 + z^2) \\, dV$ donde $B = [0, 1]^3$."
            ),
            pistas=[
                "Por linealidad: $\\iiint x^2 \\, dV + \\iiint y^2 \\, dV + \\iiint z^2 \\, dV$.",
                "Cada uno se calcula por separable.",
                "$\\iiint x^2 \\, dV = (\\int_0^1 x^2 dx)(\\int_0^1 dy)(\\int_0^1 dz) = 1/3$.",
            ],
            solucion=(
                "Por simetría, los tres términos son iguales a $1/3$. Total: $1$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el orden de integración** en regiones generales — los límites cambian dependiendo del orden.",
              "**Confundir 'caja' con 'región general'.** En cajas todos los límites son constantes; en regiones generales, los internos son funciones.",
              "**No proyectar el sólido a un plano coordenado** antes de plantear la integral.",
              "**Usar polares en regiones que no tienen simetría circular.** Mantener cartesianas si la región es rectangular.",
              "**Olvidar el factor de Jacobiano** cuando se cambia a otras coordenadas (cilíndricas, esféricas — próximas lecciones).",
          ]),

        b("resumen",
          puntos_md=[
              "**Integral triple:** $\\iiint_E f \\, dV$ — generalización a 3D.",
              "**Fubini:** sobre cajas, las tres integrales iteradas en cualquiera de 6 órdenes dan el mismo valor.",
              "**Regiones generales:** proyectar a un plano coordenado y montar las tres integrales (la externa con límites constantes, las internas con funciones).",
              "**Volumen:** $\\iiint_E 1 \\, dV$.",
              "**Aplicaciones futuras:** masa, centro de masa, momentos (capítulo 7).",
              "**Próximas lecciones:** sistemas de coordenadas alternativos para sólidos (cilíndricas, esféricas).",
          ]),
    ]
    return {
        "id": "lec-mvar-6-4-triples",
        "title": "Integrales triples",
        "description": "Integrales triples sobre cajas y regiones generales, Fubini en 3D, volumen como integral triple.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 4,
    }


# =====================================================================
# 6.5 Coordenadas cilíndricas
# =====================================================================
def lesson_6_5():
    blocks = [
        b("texto", body_md=(
            "Igual que las coordenadas polares simplifican integrales sobre regiones circulares en el plano, "
            "las **coordenadas cilíndricas** simplifican integrales sobre sólidos con **simetría axial** "
            "(cilindros, conos, paraboloides). Son polares en el plano $xy$ + la coordenada $z$ sin cambio.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Convertir entre cartesianas y cilíndricas.\n"
            "- Aplicar la fórmula $dV = r \\, dr \\, d\\theta \\, dz$.\n"
            "- Reconocer cuándo cilíndricas es ventajoso.\n"
            "- Calcular volúmenes de sólidos con simetría axial."
        )),

        b("definicion",
          titulo="Coordenadas cilíndricas",
          body_md=(
              "Las **coordenadas cilíndricas** $(r, \\theta, z)$ se relacionan con las cartesianas por:\n\n"
              "$$x = r \\cos\\theta, \\quad y = r \\sin\\theta, \\quad z = z$$\n\n"
              "con $r \\geq 0$, $\\theta \\in [0, 2\\pi)$, $z \\in \\mathbb{R}$.\n\n"
              "**Conversión inversa:** $r = \\sqrt{x^2 + y^2}, \\theta = \\arctan(y/x)$, $z$ igual.\n\n"
              "**Geometría:** $r$ es la distancia al eje $z$, $\\theta$ es el ángulo en el plano $xy$, $z$ es la altura. "
              "Cada superficie $r = $ constante es un **cilindro** alrededor del eje $z$."
          )),

        b("teorema",
          nombre="Cambio a cilíndricas en integrales triples",
          enunciado_md=(
              "$$dV = r \\, dr \\, d\\theta \\, dz$$\n\n"
              "$$\\iiint_E f(x, y, z) \\, dV = \\iiint_{E'} f(r\\cos\\theta, r\\sin\\theta, z) \\cdot r \\, dr \\, d\\theta \\, dz$$\n\n"
              "donde $E'$ es la descripción de $E$ en coordenadas cilíndricas.\n\n"
              "**El factor $r$** es el mismo que en polares (jacobiano), porque $z$ no cambia."
          ),
          demostracion_md=(
              "Jacobiano de la transformación $(r, \\theta, z) \\to (x, y, z)$:\n\n"
              "$\\det \\begin{pmatrix} \\cos\\theta & -r\\sin\\theta & 0 \\\\ \\sin\\theta & r\\cos\\theta & 0 \\\\ 0 & 0 & 1 \\end{pmatrix} = r(\\cos^2 + \\sin^2) = r$"
          )),

        fig(
            "Coordenadas cilíndricas en 3D. Sistema de ejes x, y, z. Un punto P destacado en el "
            "espacio. Mostrar las tres coordenadas: r como distancia desde P al eje z (proyección "
            "horizontal), θ como ángulo medido en el plano xy desde el eje x positivo hasta la "
            "proyección horizontal de P, z como altura. Líneas auxiliares punteadas. Pequeño "
            "elemento de volumen 'cilíndrico' destacado: una caja con dimensiones r dθ (arco), dr "
            "(radial), dz (altura), con etiqueta 'dV = r dr dθ dz'. Etiquetas claras: 'P', 'r', "
            "'θ', 'z'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Volumen de un cono",
          problema_md=(
              "Calcular el volumen del cono $z = \\sqrt{x^2 + y^2}$ entre $z = 0$ y $z = 2$."
            ),
          pasos=[
              {"accion_md": "**En cilíndricas:** la condición $z = \\sqrt{x^2 + y^2}$ se vuelve $z = r$. El cono va desde $z = 0$ hasta $z = 2$, así $0 \\leq r \\leq 2$ y $r \\leq z \\leq 2$.\n\n"
                            "**O bien (más simple):** para $z \\in [0, 2]$, $0 \\leq r \\leq z$ (radio crece linealmente con la altura). $\\theta \\in [0, 2\\pi]$.",
               "justificacion_md": "Visualizar: el cono empieza en un punto en $z = 0$ y se ensancha al subir. Para cada altura $z$, el radio máximo es $z$.",
               "es_resultado": False},
              {"accion_md": "$V = \\int_0^{2\\pi} \\int_0^2 \\int_0^z r \\, dr \\, dz \\, d\\theta = \\int_0^{2\\pi} \\int_0^2 \\dfrac{z^2}{2} \\, dz \\, d\\theta$.",
               "justificacion_md": "Interna en $r$: $r^2/2 |_0^z = z^2/2$.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^2 z^2/2 \\, dz = 4/3$. $\\int_0^{2\\pi} 4/3 \\, d\\theta = 8\\pi/3$.\n\n"
                            "**Verificación:** $V_{cono} = \\dfrac{1}{3}\\pi r^2 h$ con $r = h = 2$: $\\dfrac{1}{3}\\pi(4)(2) = 8\\pi/3$. ✓",
               "justificacion_md": "Recupera la fórmula clásica.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Sólido entre paraboloide y plano",
          problema_md=(
              "Calcular el volumen del sólido acotado por $z = x^2 + y^2$ y $z = 4$."
          ),
          pasos=[
              {"accion_md": "**Visualizar:** paraboloide abriendo hacia arriba con vértice en el origen, cortado por el plano $z = 4$. **Intersección:** $x^2 + y^2 = 4$ — círculo de radio 2.",
               "justificacion_md": "El sólido es el 'tazón' lleno de líquido hasta $z = 4$.",
               "es_resultado": False},
              {"accion_md": "**En cilíndricas:** $0 \\leq r \\leq 2$, $0 \\leq \\theta \\leq 2\\pi$, $r^2 \\leq z \\leq 4$.\n\n"
                            "(Para cada $r$, $z$ va desde el paraboloide $r^2$ hasta el plano $4$.)",
               "justificacion_md": "Tipo 1: proyectado al disco $r \\leq 2$, con $z$ entre dos superficies.",
               "es_resultado": False},
              {"accion_md": "$V = \\int_0^{2\\pi} \\int_0^2 \\int_{r^2}^4 r \\, dz \\, dr \\, d\\theta = \\int_0^{2\\pi} \\int_0^2 r(4 - r^2) \\, dr \\, d\\theta$.\n\n"
                            "Interna en $r$: $\\int_0^2 (4r - r^3) \\, dr = 8 - 4 = 4$. Externa: $\\int_0^{2\\pi} 4 \\, d\\theta = 8\\pi$.",
               "justificacion_md": "**Lección:** cilíndricas convierten paraboloides ($z = r^2$) en problemas algebraicos triviales.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Cuándo cilíndricas?",
          body_md=(
              "**Cilíndricas son ideales cuando:**\n\n"
              "- El sólido tiene **simetría rotacional** alrededor del eje $z$ (o de algún eje, después de elegir orientación).\n"
              "- Aparecen **superficies tipo $z = f(r)$** (paraboloides, conos, esferas tronchadas).\n"
              "- El integrando depende solo de $\\sqrt{x^2+y^2}$ y $z$.\n\n"
              "**No conviene** cuando hay simetría esférica (mejor esféricas) o regiones rectangulares (mejor cartesianas)."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El elemento de volumen en cilíndricas es:",
                  "opciones_md": [
                      "$dr \\, d\\theta \\, dz$",
                      "$r \\, dr \\, d\\theta \\, dz$",
                      "$r^2 \\, dr \\, d\\theta \\, dz$",
                      "$r \\, dr \\, dz$",
                  ],
                  "correcta": "B",
                  "pista_md": "Es el mismo factor $r$ que en polares, por la coordenada $z$ no cambia.",
                  "explicacion_md": (
                      "$dV = r \\, dr \\, d\\theta \\, dz$. El $r$ extra viene de las polares para $(x, y)$; $z$ no contribuye factor."
                  ),
              },
              {
                  "enunciado_md": "Para integrar sobre el cilindro $x^2 + y^2 \\leq R^2, 0 \\leq z \\leq H$, los límites son:",
                  "opciones_md": [
                      "$r \\in [0, R], \\theta \\in [0, 2\\pi], z \\in [0, H]$",
                      "$r \\in [0, R], \\theta \\in [0, \\pi], z \\in [0, H]$",
                      "$r \\in [0, R^2], \\theta \\in [0, 2\\pi], z \\in [0, H]$",
                      "$r \\in [-R, R], \\theta \\in [0, 2\\pi], z \\in [0, H]$",
                  ],
                  "correcta": "A",
                  "pista_md": "$x^2 + y^2 \\leq R^2 \\iff r \\leq R$.",
                  "explicacion_md": (
                      "$r$ es siempre $\\geq 0$, así $r \\in [0, R]$ y $\\theta$ recorre los $2\\pi$. **Cilindro completo.**"
                  ),
              },
          ]),

        ej(
            titulo="Masa de un cilindro con densidad variable",
            enunciado=(
                "Un cilindro de radio $1$ y altura $2$ centrado en el eje $z$ tiene densidad "
                "$\\rho(x, y, z) = \\sqrt{x^2 + y^2}$. Calcula su masa."
            ),
            pistas=[
                "$M = \\iiint_E \\rho \\, dV$ con $\\rho = r$ en cilíndricas.",
                "Cilindro: $r \\in [0, 1], \\theta \\in [0, 2\\pi], z \\in [0, 2]$.",
                "$M = \\int \\int \\int r \\cdot r \\, dr \\, d\\theta \\, dz$.",
            ],
            solucion=(
                "$M = \\int_0^{2\\pi} \\int_0^2 \\int_0^1 r \\cdot r \\, dr \\, dz \\, d\\theta = \\int_0^{2\\pi} \\int_0^2 \\dfrac{1}{3} \\, dz \\, d\\theta$.\n\n"
                "$= \\dfrac{1}{3} \\cdot 2 \\cdot 2\\pi = \\dfrac{4\\pi}{3}$."
            ),
        ),

        ej(
            titulo="Sólido entre dos paraboloides",
            enunciado=(
                "Calcula el volumen del sólido acotado por $z = x^2 + y^2$ y $z = 8 - (x^2 + y^2)$."
            ),
            pistas=[
                "Intersección: $r^2 = 8 - r^2 \\implies r^2 = 4 \\implies r = 2$.",
                "$z$ va de $r^2$ (paraboloide inferior) hasta $8 - r^2$ (paraboloide invertido superior).",
            ],
            solucion=(
                "$V = \\int_0^{2\\pi} \\int_0^2 \\int_{r^2}^{8 - r^2} r \\, dz \\, dr \\, d\\theta = \\int_0^{2\\pi} \\int_0^2 r(8 - 2r^2) \\, dr \\, d\\theta$.\n\n"
                "Interna: $\\int_0^2 (8r - 2r^3) \\, dr = 16 - 8 = 8$. Externa: $16\\pi$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $r$** del elemento de volumen.",
              "**Confundir cilíndricas con esféricas.** En cilíndricas, $z$ es independiente; en esféricas, todo está parametrizado por una distancia y dos ángulos.",
              "**Aplicar cilíndricas cuando la simetría es esférica.** Las esferas se manejan mejor con esféricas.",
              "**No identificar el sólido como Tipo 1** (con $z$ como variable interna). Suele ser el orden más natural.",
              "**Olvidar que $r \\geq 0$** y permitir valores negativos.",
          ]),

        b("resumen",
          puntos_md=[
              "**Cilíndricas:** $(r, \\theta, z)$ con $x = r\\cos\\theta, y = r\\sin\\theta$.",
              "**$dV = r \\, dr \\, d\\theta \\, dz$.**",
              "**Conviene cuando:** simetría axial (cilindros, conos, paraboloides).",
              "**Aplicación natural:** convertir $x^2 + y^2$ en $r^2$ y simplificar.",
              "**Próxima lección:** coordenadas esféricas — el sistema natural para esferas.",
          ]),
    ]
    return {
        "id": "lec-mvar-6-5-cilindricas",
        "title": "Coordenadas cilíndricas",
        "description": "Sistema cilíndrico $(r, \\theta, z)$ para sólidos con simetría axial.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# 6.6 Coordenadas esféricas
# =====================================================================
def lesson_6_6():
    blocks = [
        b("texto", body_md=(
            "Las **coordenadas esféricas** $(\\rho, \\theta, \\varphi)$ son el sistema natural para sólidos con "
            "**simetría esférica**: bolas, capas esféricas, conos sobre la esfera. Son fundamentales en "
            "física (electrostática, gravitación, mecánica cuántica).\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Comprender la geometría de $(\\rho, \\theta, \\varphi)$.\n"
            "- Convertir entre cartesianas y esféricas.\n"
            "- Aplicar $dV = \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$.\n"
            "- Calcular volúmenes y masas de sólidos esféricos."
        )),

        b("definicion",
          titulo="Coordenadas esféricas",
          body_md=(
              "Las **coordenadas esféricas** $(\\rho, \\theta, \\varphi)$ se relacionan con cartesianas:\n\n"
              "$$x = \\rho \\sin\\varphi \\cos\\theta, \\quad y = \\rho \\sin\\varphi \\sin\\theta, \\quad z = \\rho \\cos\\varphi$$\n\n"
              "**Significado geométrico:**\n\n"
              "- $\\rho \\geq 0$: distancia al origen. $\\rho^2 = x^2 + y^2 + z^2$.\n"
              "- $\\theta \\in [0, 2\\pi)$: **ángulo azimutal** (mismo que en polares/cilíndricas, en el plano $xy$).\n"
              "- $\\varphi \\in [0, \\pi]$: **ángulo polar**, medido **desde el eje $z$ positivo** hasta el vector posición.\n\n"
              "**Casos límite:** $\\varphi = 0$ es el polo norte (eje $z$ positivo). $\\varphi = \\pi$ es el polo sur. $\\varphi = \\pi/2$ es el ecuador (plano $xy$)."
          )),

        b("teorema",
          nombre="Cambio a esféricas",
          enunciado_md=(
              "$$dV = \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$$\n\n"
              "$$\\iiint_E f \\, dV = \\iiint_{E'} f(\\rho, \\theta, \\varphi) \\cdot \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$$\n\n"
              "**El factor $\\rho^2 \\sin\\varphi$** es el jacobiano de la transformación. Es esencial — sin él, los volúmenes están mal calculados."
          ),
          demostracion_md=(
              "Jacobiano:\n\n"
              "$\\det \\begin{pmatrix} \\sin\\varphi\\cos\\theta & -\\rho\\sin\\varphi\\sin\\theta & \\rho\\cos\\varphi\\cos\\theta \\\\ \\sin\\varphi\\sin\\theta & \\rho\\sin\\varphi\\cos\\theta & \\rho\\cos\\varphi\\sin\\theta \\\\ \\cos\\varphi & 0 & -\\rho\\sin\\varphi \\end{pmatrix} = -\\rho^2\\sin\\varphi$\n\n"
              "El valor absoluto da $\\rho^2 \\sin\\varphi$."
          )),

        fig(
            "Coordenadas esféricas en 3D. Sistema de ejes x, y, z. Un punto P destacado en el "
            "espacio. Mostrar las tres coordenadas: ρ como distancia desde el origen hasta P "
            "(línea recta gruesa color teal), θ como ángulo azimutal en el plano xy desde el eje x "
            "positivo hasta la proyección horizontal de P, φ como ángulo polar desde el eje z "
            "positivo hasta la línea OP. La proyección de P en el plano xy y líneas auxiliares "
            "punteadas. Pequeño elemento de volumen 'esférico' destacado: una caja distorsionada "
            "con dimensiones dρ (radial), ρ dφ (meridional), ρ sin(φ) dθ (azimutal), con etiqueta "
            "'dV = ρ² sin(φ) dρ dθ dφ'. Etiquetas claras: 'P', 'ρ', 'θ', 'φ'. " + STYLE
        ),

        formulas(
            titulo="Conversiones útiles",
            body=(
                "**Cartesianas $\\to$ esféricas:**\n\n"
                "$\\rho = \\sqrt{x^2 + y^2 + z^2}$.\n\n"
                "$\\theta = \\arctan(y/x)$ (con cuidado del cuadrante; igual que en polares).\n\n"
                "$\\varphi = \\arccos(z/\\rho)$.\n\n"
                "**Esféricas $\\to$ cartesianas:** ya dadas en la definición.\n\n"
                "**Identidades clave:**\n\n"
                "$x^2 + y^2 + z^2 = \\rho^2$. $x^2 + y^2 = \\rho^2 \\sin^2\\varphi$. $z = \\rho\\cos\\varphi$.\n\n"
                "**Superficies clásicas en esféricas:**\n\n"
                "- $\\rho = R$: esfera de radio $R$.\n"
                "- $\\varphi = \\alpha$ (constante): cono con vértice en el origen.\n"
                "- $\\theta = \\beta$ (constante): semiplano que sale del eje $z$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Volumen de una bola",
          problema_md="Calcular el volumen de la bola $x^2 + y^2 + z^2 \\leq R^2$.",
          pasos=[
              {"accion_md": "**En esféricas:** $0 \\leq \\rho \\leq R$, $0 \\leq \\theta \\leq 2\\pi$, $0 \\leq \\varphi \\leq \\pi$.",
               "justificacion_md": "Bola completa cubre toda la esfera angular y todos los radios hasta $R$.",
               "es_resultado": False},
              {"accion_md": "$V = \\int_0^{2\\pi} \\int_0^\\pi \\int_0^R \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\varphi \\, d\\theta$.\n\n"
                            "**Separable:** $\\left(\\int_0^R \\rho^2 d\\rho\\right)\\left(\\int_0^\\pi \\sin\\varphi \\, d\\varphi\\right)\\left(\\int_0^{2\\pi} d\\theta\\right)$.",
               "justificacion_md": "El integrando se factoriza, así también la integral.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^R \\rho^2 d\\rho = R^3/3$. $\\int_0^\\pi \\sin\\varphi \\, d\\varphi = 2$. $\\int_0^{2\\pi} d\\theta = 2\\pi$.\n\n"
                            "$V = \\dfrac{R^3}{3} \\cdot 2 \\cdot 2\\pi = \\dfrac{4\\pi R^3}{3}$.",
               "justificacion_md": "**Recupera la fórmula clásica del volumen de la esfera.** En esféricas, una línea de cálculo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cono esférico (cucurucho)",
          problema_md=(
              "Calcular el volumen del sólido limitado por arriba por la esfera $x^2 + y^2 + z^2 = 4$ y "
              "lateralmente por el cono $z = \\sqrt{x^2 + y^2}$ (en la parte $z \\geq 0$)."
          ),
          pasos=[
              {"accion_md": "**El cono $z = \\sqrt{x^2+y^2}$:** en esféricas, $\\rho\\cos\\varphi = \\rho\\sin\\varphi \\implies \\tan\\varphi = 1 \\implies \\varphi = \\pi/4$.",
               "justificacion_md": "El cono $z = r$ corresponde a $\\varphi = \\pi/4$.",
               "es_resultado": False},
              {"accion_md": "**Sólido en esféricas:** $0 \\leq \\rho \\leq 2$, $0 \\leq \\theta \\leq 2\\pi$, $0 \\leq \\varphi \\leq \\pi/4$.",
               "justificacion_md": "Dentro de la esfera y dentro del cono (que abre $\\pi/4$ desde el eje $z$).",
               "es_resultado": False},
              {"accion_md": "$V = \\int_0^{2\\pi}\\int_0^{\\pi/4}\\int_0^2 \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\varphi \\, d\\theta$.\n\n"
                            "$= \\dfrac{8}{3}(1 - \\cos(\\pi/4))(2\\pi) = \\dfrac{16\\pi}{3}(1 - \\dfrac{\\sqrt{2}}{2}) = \\dfrac{16\\pi(2-\\sqrt{2})}{6} = \\dfrac{8\\pi(2-\\sqrt{2})}{3}$.",
               "justificacion_md": "$\\int_0^2 \\rho^2 \\, d\\rho = 8/3$. $\\int_0^{\\pi/4} \\sin\\varphi \\, d\\varphi = 1 - \\sqrt{2}/2$.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Cuándo esféricas?",
          body_md=(
              "**Esféricas son ideales cuando:**\n\n"
              "- Aparece **$x^2 + y^2 + z^2$** en el integrando o en la frontera.\n"
              "- El sólido tiene **simetría esférica** (bolas, capas esféricas).\n"
              "- Hay **conos centrados en el origen** ($\\varphi = $ constante).\n\n"
              "**No conviene** cuando la simetría es axial pero no esférica (mejor cilíndricas) o cuando la frontera es una caja (mejor cartesianas).\n\n"
              "**Convención sobre $\\varphi$:** algunos textos usan $\\varphi$ desde el plano $xy$ (latitud) y otros desde el eje $z$ (lo que usamos). **Verifica siempre la convención.**"
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El elemento de volumen en esféricas es:",
                  "opciones_md": [
                      "$d\\rho \\, d\\theta \\, d\\varphi$",
                      "$\\rho^2 \\, d\\rho \\, d\\theta \\, d\\varphi$",
                      "$\\rho^2 \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$",
                      "$\\rho \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$",
                  ],
                  "correcta": "C",
                  "pista_md": "Jacobiano de la transformación esférica: $\\rho^2 \\sin\\varphi$.",
                  "explicacion_md": (
                      "$dV = \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$. **Memorizarlo es fundamental** — sin el factor correcto los cálculos están mal."
                  ),
              },
              {
                  "enunciado_md": "Para el cono $z = \\sqrt{x^2 + y^2}$ ($z \\geq 0$), en esféricas:",
                  "opciones_md": [
                      "$\\varphi = 0$",
                      "$\\varphi = \\pi/4$",
                      "$\\varphi = \\pi/2$",
                      "$\\theta = \\pi/4$",
                  ],
                  "correcta": "B",
                  "pista_md": "El cono abre $45°$ desde el eje $z$.",
                  "explicacion_md": (
                      "$z = \\sqrt{x^2+y^2}$ significa $\\rho\\cos\\varphi = \\rho\\sin\\varphi$, así $\\tan\\varphi = 1$, $\\varphi = \\pi/4$."
                  ),
              },
          ]),

        ej(
            titulo="Masa de una bola con densidad radial",
            enunciado=(
                "Una bola de radio $R$ tiene densidad $\\rho_{masa}(P) = k \\cdot d(P, O)^2$ donde $d$ es "
                "la distancia al origen. Calcula su masa."
            ),
            pistas=[
                "$\\rho_{masa} = k \\rho^2$ (donde $\\rho$ es la coordenada esférica).",
                "$M = \\iiint k \\rho^2 \\cdot \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$.",
            ],
            solucion=(
                "$M = k \\int_0^{2\\pi}\\int_0^\\pi \\int_0^R \\rho^4 \\sin\\varphi \\, d\\rho \\, d\\varphi \\, d\\theta$.\n\n"
                "$= k \\cdot \\dfrac{R^5}{5} \\cdot 2 \\cdot 2\\pi = \\dfrac{4\\pi k R^5}{5}$."
            ),
        ),

        ej(
            titulo="Capa esférica",
            enunciado=(
                "Calcula el volumen de la capa esférica $1 \\leq x^2 + y^2 + z^2 \\leq 4$."
            ),
            pistas=[
                "$1 \\leq \\rho^2 \\leq 4 \\iff 1 \\leq \\rho \\leq 2$.",
                "Volumen = bola exterior - bola interior, o integrar directamente.",
            ],
            solucion=(
                "$V = \\int_0^{2\\pi}\\int_0^\\pi \\int_1^2 \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\varphi \\, d\\theta = \\dfrac{2^3 - 1^3}{3} \\cdot 2 \\cdot 2\\pi = \\dfrac{7}{3} \\cdot 4\\pi = \\dfrac{28\\pi}{3}$.\n\n"
                "**Verificación:** $\\dfrac{4\\pi}{3}(8 - 1) = \\dfrac{28\\pi}{3}$. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $\\rho^2 \\sin\\varphi$.** Es el error más caro — los volúmenes salen mal por un factor.",
              "**Confundir convenciones de $\\varphi$.** En este curso, $\\varphi$ es desde el eje $z$. En física (a veces), es desde el plano $xy$. Asegurarse antes de usar fórmulas externas.",
              "**Confundir cilíndricas con esféricas.** En cilíndricas, $r$ es radio horizontal; en esféricas, $\\rho$ es radio total al origen.",
              "**Aplicar esféricas a sólidos con simetría axial pero no esférica.** Cilíndricas suelen ser más naturales en esos casos.",
              "**Limitar $\\varphi$ a $[0, 2\\pi]$.** $\\varphi$ va de $0$ a $\\pi$ solamente — los $360°$ los cubre $\\theta$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Esféricas:** $(\\rho, \\theta, \\varphi)$ con $\\rho \\geq 0, \\theta \\in [0, 2\\pi), \\varphi \\in [0, \\pi]$.",
              "**Conversión:** $x = \\rho \\sin\\varphi\\cos\\theta, y = \\rho\\sin\\varphi\\sin\\theta, z = \\rho\\cos\\varphi$.",
              "**$dV = \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$.**",
              "**Conviene:** simetría esférica (bolas, capas), conos centrados, integrandos con $x^2+y^2+z^2$.",
              "**Cono $\\varphi = \\alpha$ constante** y **esfera $\\rho = R$ constante** son las superficies fundamentales.",
              "**Próxima lección:** cambio de variables general — la teoría detrás de polares, cilíndricas y esféricas.",
          ]),
    ]
    return {
        "id": "lec-mvar-6-6-esfericas",
        "title": "Coordenadas esféricas",
        "description": "Sistema esférico $(\\rho, \\theta, \\varphi)$ para sólidos con simetría esférica.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


# =====================================================================
# 6.7 Cambio de variables
# =====================================================================
def lesson_6_7():
    blocks = [
        b("texto", body_md=(
            "Las coordenadas polares, cilíndricas y esféricas son **casos particulares** de un teorema más "
            "general: el **teorema de cambio de variables** para integrales múltiples. La idea: cualquier "
            "transformación suficientemente buena se puede aplicar, **siempre que se incluya el factor "
            "jacobiano** apropiado.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir el **Jacobiano** $\\partial(x, y)/\\partial(u, v)$.\n"
            "- Aplicar la **fórmula de cambio de variables** en integrales dobles y triples.\n"
            "- Reconocer **transformaciones útiles** según la región y el integrando.\n"
            "- Verificar que polares, cilíndricas y esféricas son casos particulares."
        )),

        b("definicion",
          titulo="Jacobiano de una transformación",
          body_md=(
              "Sea $T: (u, v) \\mapsto (x, y)$ una transformación dada por $x = x(u, v)$, $y = y(u, v)$. El **Jacobiano** de $T$ es:\n\n"
              "$$\\dfrac{\\partial(x, y)}{\\partial(u, v)} = \\det \\begin{pmatrix} \\partial x/\\partial u & \\partial x/\\partial v \\\\ \\partial y/\\partial u & \\partial y/\\partial v \\end{pmatrix} = x_u y_v - x_v y_u$$\n\n"
              "**Para 3 variables** ($x, y, z$ funciones de $u, v, w$): determinante 3×3 análogo.\n\n"
              "**Geometría:** el valor absoluto del Jacobiano $|J|$ es el **factor de distorsión local de área (o volumen)** de la transformación. Un cuadrado pequeño en $(u, v)$ se transforma en un paralelogramo en $(x, y)$ con área $|J|$ veces el del original."
          )),

        b("teorema",
          nombre="Cambio de variables (caso 2D)",
          enunciado_md=(
              "Sea $T: D' \\to D$ una transformación inyectiva, $C^1$, con Jacobiano no nulo. Sea $f$ continua sobre $D$. Entonces:\n\n"
              "$$\\iint_D f(x, y) \\, dA = \\iint_{D'} f(x(u, v), y(u, v)) \\left|\\dfrac{\\partial(x, y)}{\\partial(u, v)}\\right| \\, du \\, dv$$\n\n"
              "**Análogo en 3D:**\n\n"
              "$$\\iiint_E f \\, dV = \\iiint_{E'} f \\cdot \\left|\\dfrac{\\partial(x, y, z)}{\\partial(u, v, w)}\\right| \\, du \\, dv \\, dw$$"
          ),
          demostracion_md=(
              "Idea geométrica: dividir $D$ en pequeños paralelogramos imagen de los cuadrados $du \\, dv$ en $D'$. Cada cuadrado se mapea a un paralelogramo de área $|J| \\, du \\, dv$. La suma de Riemann de $f$ sobre $D$ se reescribe en términos de $D'$ con el factor $|J|$. Tomando el límite, la integral aparece con $|J| \\, du \\, dv$."
          )),

        b("ejemplo_resuelto",
          titulo="Polares como caso particular",
          problema_md="Verificar que $dA = r \\, dr \\, d\\theta$ usando la fórmula general.",
          pasos=[
              {"accion_md": "**Transformación:** $x = r\\cos\\theta, y = r\\sin\\theta$. **Variables nuevas:** $(u, v) = (r, \\theta)$.",
               "justificacion_md": "Identificación.",
               "es_resultado": False},
              {"accion_md": "**Parciales:** $x_r = \\cos\\theta, x_\\theta = -r\\sin\\theta, y_r = \\sin\\theta, y_\\theta = r\\cos\\theta$.",
               "justificacion_md": "Cálculo directo.",
               "es_resultado": False},
              {"accion_md": "**Jacobiano:**\n\n"
                            "$J = \\det\\begin{pmatrix} \\cos\\theta & -r\\sin\\theta \\\\ \\sin\\theta & r\\cos\\theta \\end{pmatrix} = r\\cos^2\\theta + r\\sin^2\\theta = r$.\n\n"
                            "$|J| = r$ (porque $r \\geq 0$). **Confirmado:** $dA = r \\, dr \\, d\\theta$.",
               "justificacion_md": "**Polares es solo el cambio de variables aplicado a la transformación de polares.**",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Transformación lineal",
          problema_md=(
              "Sea $D$ la región acotada por $x + 2y = 1$, $x + 2y = 3$, $x - y = 0$, $x - y = 2$. "
              "Calcular $\\iint_D (x + 2y) \\, dA$ usando $u = x + 2y$, $v = x - y$."
          ),
          pasos=[
              {"accion_md": "**Definir** $u = x + 2y$, $v = x - y$. **Región nueva:** $D' = [1, 3] \\times [0, 2]$ (rectángulo).",
               "justificacion_md": "Las cuatro rectas se vuelven los lados del rectángulo en $(u, v)$.",
               "es_resultado": False},
              {"accion_md": "**Despejar $x, y$ de $u, v$:** sumando $u + 2v = 3x \\implies x = (u + 2v)/3$. Restando $u - v = 3y \\implies y = (u - v)/3$.",
               "justificacion_md": "Despeje algebraico.",
               "es_resultado": False},
              {"accion_md": "**Jacobiano:** $x_u = 1/3, x_v = 2/3, y_u = 1/3, y_v = -1/3$.\n\n"
                            "$J = (1/3)(-1/3) - (2/3)(1/3) = -1/9 - 2/9 = -1/3$. $|J| = 1/3$.",
               "justificacion_md": "Cálculo directo.",
               "es_resultado": False},
              {"accion_md": "$\\iint_D (x + 2y) \\, dA = \\iint_{D'} u \\cdot \\dfrac{1}{3} \\, du \\, dv = \\dfrac{1}{3} \\int_0^2 \\int_1^3 u \\, du \\, dv = \\dfrac{1}{3} \\cdot 4 \\cdot 2 = \\dfrac{8}{3}$.",
               "justificacion_md": "**Lección clave:** el cambio de variables convirtió un paralelogramo en un rectángulo, y un integrando feo en uno simple.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Cuándo cambiar variables?",
          body_md=(
              "**Buenas señales para cambiar variables:**\n\n"
              "1. La **región** se ve naturalmente en otras coordenadas (paralelogramos, regiones polares, esféricas).\n"
              "2. El **integrando** se simplifica con el cambio (ej: $x^2+y^2 = r^2$).\n"
              "3. **Las fronteras** se vuelven líneas paralelas a los ejes nuevos.\n\n"
              "**Estrategia general:**\n\n"
              "- Mirar las **fronteras de $D$**: si se reescriben como $u = $ const, $v = $ const, el cambio simplifica.\n"
              "- Mirar el **integrando**: si tiene combinaciones algebraicas claras (suma, diferencia, producto), pueden ser variables nuevas.\n"
              "- **Calcular el jacobiano** y verificar que no se anula.\n"
              "- **Reescribir todo** en las nuevas variables."
          )),

        formulas(
            titulo="Casos especiales conocidos",
            body=(
                "| Transformación | Jacobiano | Elemento |\n|---|---|---|\n"
                "| **Polares** $(x, y) = (r\\cos\\theta, r\\sin\\theta)$ | $r$ | $dA = r \\, dr \\, d\\theta$ |\n"
                "| **Cilíndricas** | $r$ | $dV = r \\, dr \\, d\\theta \\, dz$ |\n"
                "| **Esféricas** | $\\rho^2 \\sin\\varphi$ | $dV = \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\theta \\, d\\varphi$ |\n"
                "| **Lineal** $\\binom{x}{y} = M \\binom{u}{v}$ | $\\det M$ | $dA = |\\det M| \\, du \\, dv$ |"
            ),
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El factor que aparece al cambiar variables es:",
                  "opciones_md": [
                      "El Jacobiano",
                      "El valor absoluto del Jacobiano",
                      "El cuadrado del Jacobiano",
                      "El recíproco del Jacobiano",
                  ],
                  "correcta": "B",
                  "pista_md": "El área debe ser positiva — por eso el valor absoluto.",
                  "explicacion_md": (
                      "$|J|$ es el factor. El signo del Jacobiano refleja orientación, pero las áreas y volúmenes son positivos."
                  ),
              },
              {
                  "enunciado_md": "Si $J = 0$ en algún punto, ¿qué pasa?",
                  "opciones_md": [
                      "La fórmula sigue valiendo igual.",
                      "La transformación no es localmente inyectiva allí; el cambio de variables falla.",
                      "El integrando se vuelve infinito.",
                      "No tiene importancia.",
                  ],
                  "correcta": "B",
                  "pista_md": "Jacobiano cero → transformación colapsa localmente.",
                  "explicacion_md": (
                      "$J = 0$ implica que $T$ no preserva áreas localmente — colapsa una dimensión. La fórmula falla en esos puntos. Polares tiene $J = r = 0$ en el origen, y por eso hay que tener cuidado allí (aunque la integral suele converger igual)."
                  ),
              },
          ]),

        ej(
            titulo="Cambio lineal",
            enunciado=(
                "Calcula $\\iint_D xy \\, dA$ donde $D$ es el paralelogramo con vértices $(0, 0), (1, 1), (2, 0), (1, -1)$, "
                "usando el cambio $u = x + y, v = x - y$."
            ),
            pistas=[
                "Despejar: $x = (u+v)/2, y = (u-v)/2$. Producto: $xy = (u^2 - v^2)/4$.",
                "Jacobiano: $J = (1/2)(-1/2) - (1/2)(1/2) = -1/2$, $|J| = 1/2$.",
                "Región nueva: cuadrado $D' = [0, 2] \\times [-1, 1]$ (verifica con los vértices).",
            ],
            solucion=(
                "**Vértices transformados:** $(0,0) \\to (0,0); (1,1) \\to (2, 0); (2, 0) \\to (2, 2); (1, -1) \\to (0, 2)$.\n\n"
                "Hmm, no es rectángulo así de simple. Probemos: $D' = \\{(u,v) : 0 \\leq u \\leq 2, |v| \\leq u \\text{ y } |v| \\leq 2 - u + 2 = ?\\}$.\n\n"
                "Mejor: la solución directa con $D' = $ paralelogramo en $(u, v)$ con vértices $(0,0), (2, 0), (2, 2), (0, 2)$ — un cuadrado.\n\n"
                "$\\iint_{D'} \\dfrac{u^2 - v^2}{4} \\cdot \\dfrac{1}{2} \\, du \\, dv = \\dfrac{1}{8}\\int_0^2 \\int_0^2 (u^2 - v^2) \\, du \\, dv$.\n\n"
                "Por simetría, $\\int_0^2 (u^2 - v^2) \\, dv = (8/3 - 8/3)... $ Calcula: $\\int_0^2 \\int_0^2 u^2 du dv = (8/3)(2) = 16/3$. Igual para $v^2$. Diferencia: $0$.\n\n"
                "**Resultado: $0$.** (Por simetría: $xy$ es impar en la diagonal $y = -x$ del paralelogramo simétrico.)"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el valor absoluto.** El Jacobiano puede ser negativo, pero el factor en la integral es $|J|$.",
              "**Calcular el Jacobiano de la transformación inversa.** Asegurarse de qué transformación se está aplicando: $(u, v) \\to (x, y)$ o $(x, y) \\to (u, v)$. Sus Jacobianos son recíprocos.",
              "**No transformar la región $D$.** Hay que reescribir las fronteras en términos de las nuevas variables.",
              "**Aplicar el cambio sin que las nuevas variables simplifiquen.** Si las cuentas se complican, probablemente el cambio no era el adecuado.",
              "**Olvidar el integrando** en las nuevas variables. $f(x, y)$ debe expresarse en $(u, v)$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Jacobiano:** determinante de la matriz de parciales.",
              "**Fórmula:** $\\iint_D f \\, dA = \\iint_{D'} f \\cdot |J| \\, du \\, dv$.",
              "**Polares, cilíndricas, esféricas** son casos particulares con $|J| = r, r, \\rho^2 \\sin\\varphi$ respectivamente.",
              "**Estrategia:** elegir variables que simplifiquen la región o el integrando.",
              "**Cierre del capítulo:** integrales múltiples es una herramienta universal — con cambio de variables podemos atacar prácticamente cualquier región.",
              "**Próximo capítulo:** aplicaciones físicas (centros de masa, momentos de inercia, áreas de superficies).",
          ]),
    ]
    return {
        "id": "lec-mvar-6-7-cambio-variables",
        "title": "Cambio de variables",
        "description": "Teorema de cambio de variables, jacobiano y aplicación general.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 7,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "calculo-multivariable"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Curso {course_id} no existe.")

    chapter_id = "ch-integrales-multiples"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Integrales Múltiples",
        "description": "Integrales dobles y triples, regiones generales, coordenadas polares, cilíndricas, esféricas y cambio de variables.",
        "order": 6,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_6_1, lesson_6_2, lesson_6_3, lesson_6_4, lesson_6_5, lesson_6_6, lesson_6_7]
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
    print(f"✅ Capítulo 6 — Integrales Múltiples listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
