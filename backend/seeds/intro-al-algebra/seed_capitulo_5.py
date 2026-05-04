"""
Seed del curso Introducción al Álgebra — Capítulo 5: Geometría Analítica.

Reescritura completa siguiendo los PDFs base en
docs/cursos/generales/intro-al-algebra/5. Geometría Analítica/.

8 lecciones:
  5.1 Rectas y Distancia
  5.2 Circunferencias
  5.3 Parábolas
  5.4 Elipses
  5.5 Hipérbolas
  5.6 Rotación de Ejes
  5.7 Rotaciones y Traslaciones
  5.8 Identificación de una Cónica

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


def paso(accion, justificacion="", resultado=False):
    return {"accion_md": accion, "justificacion_md": justificacion, "es_resultado": resultado}


def now():
    return datetime.now(timezone.utc).isoformat()


STYLE = (
    "Estilo: diagrama matemático educativo limpio, fondo blanco, líneas claras, "
    "etiquetas en español, notación matemática con buena tipografía. Acentos teal "
    "#06b6d4 y ámbar #f59e0b. Sin sombras dramáticas. Apto para libro universitario."
)


COURSE_ID = "intro-al-algebra"
COURSE_TITLE = "Introducción al Álgebra"
COURSE_DESCRIPTION = (
    "Curso fundacional que construye el lenguaje matemático universitario. "
    "Cubre lógica proposicional, teoría de conjuntos, cuantificadores, inducción, "
    "sucesiones, trigonometría, polinomios complejos y geometría analítica de las "
    "cónicas. Es la base de los cursos universitarios de Álgebra, Cálculo y "
    "Geometría que se construyen sobre estos contenidos.\n\n"
    "Inspirado en el programa **MAT1207** de la Pontificia Universidad Católica "
    "de Chile (Texto guía: *Álgebra e introducción al cálculo*, Irene Mikenberg)."
)
COURSE_CATEGORY = "Matemáticas"
COURSE_LEVEL = "Intermedio"
COURSE_MODULES_COUNT = 5

CHAPTER_ID = "ch-ia-geometria-analitica"
CHAPTER_TITLE = "Geometría Analítica"
CHAPTER_DESCRIPTION = (
    "El puente entre álgebra y geometría: rectas, distancia y la familia completa "
    "de las cónicas (circunferencia, parábola, elipse, hipérbola) descritas como "
    "lugares geométricos y mediante ecuaciones. Cierra con rotación, traslación "
    "de ejes e identificación general de cualquier ecuación de segundo grado "
    "mediante el discriminante."
)
CHAPTER_ORDER = 5


# ============================================================================
# 5.1 Rectas y Distancia
# ============================================================================
def lesson_5_1():
    blocks = [
        b("texto", body_md=(
            "Las **rectas en el plano** constituyen uno de los objetos geométricos más "
            "fundamentales del álgebra y la geometría analítica. A partir de nociones "
            "elementales como la **distancia entre dos puntos** y la **inclinación** de "
            "una recta, se construye toda una teoría que permite describir, clasificar "
            "y relacionar rectas mediante sus ecuaciones y propiedades métricas.\n\n"
            "**En esta lección estudiaremos:**\n\n"
            "- Distancia entre dos puntos.\n"
            "- Inclinación y pendiente de una recta.\n"
            "- Las distintas formas de la ecuación de la recta (punto-pendiente, dos puntos y forma general).\n"
            "- Criterios de **paralelismo** y **perpendicularidad**.\n"
            "- Ángulo entre dos rectas.\n"
            "- **Distancia de un punto a una recta**."
        )),

        b("definicion",
          titulo="Distancia entre dos puntos",
          body_md=(
              "Sean $P_1(x_1, y_1)$ y $P_2(x_2, y_2)$ dos puntos del plano. La **distancia** entre ellos es\n\n"
              "$$d(P_1, P_2) = \\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}.$$\n\n"
              "Se obtiene aplicando el **Teorema de Pitágoras** al triángulo rectángulo de catetos "
              "$|x_1 - x_2|$ y $|y_1 - y_2|$ e hipotenusa $\\overline{P_1 P_2}$. "
              "Notación alternativa: $|P_1 P_2|$."
          )),

        fig("Plano cartesiano con dos puntos P1(x1,y1) y P2(x2,y2). Segmento que los une marcado como hipotenusa, "
            "y los catetos del triángulo rectángulo dibujados con |x1-x2| y |y1-y2| etiquetados. " + STYLE),

        b("ejemplo_resuelto",
          titulo="Triángulo isósceles",
          problema_md=("Demuestra que el triángulo con vértices $A(-2, 3)$, $B(6, 1)$ y $C(-2, 5)$ es **isósceles** "
                       "(es decir, tiene al menos dos lados iguales)."),
          pasos=[
              paso("Calculamos las tres distancias entre vértices.", "Aplicamos la fórmula de distancia."),
              paso("$|AB| = \\sqrt{(6-(-2))^2 + (1-3)^2} = \\sqrt{64 + 4} = \\sqrt{68} = 2\\sqrt{17}.$"),
              paso("$|AC| = \\sqrt{(-2-(-2))^2 + (5-3)^2} = \\sqrt{0 + 4} = 2.$"),
              paso("$|BC| = \\sqrt{(6-(-2))^2 + (1-5)^2} = \\sqrt{64 + 16} = \\sqrt{80} = 4\\sqrt{5}.$"),
              paso("Comparando los tres lados al cuadrado: $|AB|^2 = 68$, $|AC|^2 = 4$, $|BC|^2 = 80$. "
                   "Para que el triángulo sea isósceles deben coincidir al menos dos de las tres distancias.",
                   "Estrategia: comprobar igualdades al cuadrado para evitar manipular raíces."),
              paso("**Procedimiento general:** calcular las tres distancias y verificar si al menos dos son iguales. "
                   "Esa verificación es lo que demuestra el carácter isósceles del triángulo.",
                   "Conclusión metodológica.", resultado=True),
          ]),

        b("definicion",
          titulo="Inclinación de una recta",
          body_md=(
              "La **inclinación** de una recta que interseca al eje $x$ es el menor ángulo $\\theta$, "
              "**mayor o igual a $0°$**, que forma la recta con la dirección positiva del eje $x$. "
              "La inclinación de una recta horizontal es $\\theta = 0$.\n\n"
              "De acuerdo con esta definición:\n\n"
              "$$0° \\le \\theta < 180°, \\quad \\text{o en radianes, } \\quad 0 \\le \\theta < \\pi.$$\n\n"
              "Una recta con $\\theta < 90°$ se inclina hacia la derecha; una con $\\theta > 90°$ "
              "se inclina hacia la izquierda. Las rectas verticales tienen $\\theta = 90°$."
          )),

        b("definicion",
          titulo="Pendiente de una recta",
          body_md=(
              "La **pendiente** de una recta es la **tangente de su inclinación**:\n\n"
              "$$m = \\tan(\\theta).$$\n\n"
              "- Recta inclinada hacia la derecha: $m > 0$ (ángulo agudo).\n"
              "- Recta inclinada hacia la izquierda: $m < 0$ (ángulo obtuso).\n"
              "- Recta horizontal: $m = 0$.\n"
              "- Las rectas **verticales no tienen pendiente** ($\\tan(90°)$ no existe)."
          )),

        b("teorema",
          enunciado_md=(
              "**Pendiente por dos puntos.** La pendiente $m$ de una recta que pasa por dos puntos "
              "$P_1(x_1, y_1)$ y $P_2(x_2, y_2)$ es\n\n"
              "$$m = \\frac{y_2 - y_1}{x_2 - x_1}, \\quad \\text{con } x_2 \\neq x_1.$$\n\n"
              "El orden de los puntos no afecta el valor de $m$, ya que cambiar el orden invierte "
              "simultáneamente el signo del numerador y del denominador."
          )),

        fig("Gráfica que ilustra inclinación: dos rectas en un plano cartesiano, una con ángulo agudo θ<90° (pendiente positiva) "
            "y otra con θ>90° (pendiente negativa). El ángulo θ se marca desde el eje x positivo hasta la recta. " + STYLE),

        b("ejemplo_resuelto",
          titulo="Verificar paralelogramo por pendientes",
          problema_md=("Dados los puntos $A(-1, -1)$, $B(5, 0)$, $C(4, 3)$ y $D(-2, 2)$, "
                       "muestra que $ABCD$ es un **paralelogramo**."),
          pasos=[
              paso("Para que $ABCD$ sea paralelogramo, los lados opuestos deben ser paralelos, "
                   "es decir, deben tener la **misma pendiente**.",
                   "Criterio de paralelismo."),
              paso("$m_{AB} = \\dfrac{0 - (-1)}{5 - (-1)} = \\dfrac{1}{6}.$"),
              paso("$m_{DC} = \\dfrac{3 - 2}{4 - (-2)} = \\dfrac{1}{6}.$"),
              paso("$m_{BC} = \\dfrac{3 - 0}{4 - 5} = \\dfrac{3}{-1} = -3.$"),
              paso("$m_{AD} = \\dfrac{2 - (-1)}{-2 - (-1)} = \\dfrac{3}{-1} = -3.$"),
              paso("Como $m_{AB} = m_{DC} = \\tfrac{1}{6}$, los lados $AB$ y $DC$ son paralelos. "
                   "Como $m_{BC} = m_{AD} = -3$, los lados $BC$ y $AD$ también son paralelos. "
                   "Por lo tanto, $\\boxed{ABCD \\text{ es un paralelogramo}}.$",
                   "Definición de paralelogramo.", resultado=True),
          ]),

        b("definicion",
          titulo="Recta como lugar geométrico",
          body_md=(
              "Se llama **recta** al lugar geométrico de los puntos $P(x, y)$ del plano tales que, "
              "para todo par de puntos $P_1$ y $P_2$ de ella, las pendientes $m_{PP_1}$, "
              "$m_{PP_2}$ y $m_{P_1 P_2}$ son iguales.\n\n"
              "Esta igualdad de pendientes se traduce en la relación\n\n"
              "$$\\frac{y - y_1}{x - x_1} = \\frac{y - y_2}{x - x_2} = \\frac{y_2 - y_1}{x_2 - x_1} = m, \\quad x_1 \\neq x_2.$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Formas de la ecuación de la recta.**\n\n"
              "**Punto-pendiente.** Recta que pasa por $P_1(x_1, y_1)$ con pendiente $m$:\n\n"
              "$$\\boxed{y - y_1 = m(x - x_1)}.$$\n\n"
              "**Por dos puntos.** Recta por $P_1(x_1, y_1)$ y $P_2(x_2, y_2)$ con $x_1 \\neq x_2$:\n\n"
              "$$\\boxed{y - y_1 = \\frac{y_2 - y_1}{x_2 - x_1}\\,(x - x_1)}.$$\n\n"
              "**Forma general.** Toda recta del plano admite una ecuación del tipo\n\n"
              "$$\\boxed{Ax + By + C = 0},$$\n\n"
              "donde $A, B, C \\in \\mathbb{R}$ con $A \\cdot B \\ne 0$ en el caso no horizontal-no vertical "
              "(la forma general también describe rectas verticales $x = c$ tomando $B = 0$, y horizontales $y = c$ tomando $A = 0$)."
          )),

        b("ejemplo_resuelto",
          titulo="Recta por un punto con pendiente conocida",
          problema_md="Encuentra la ecuación de la recta que pasa por $(1, -3)$ y tiene pendiente $m = -\\tfrac{1}{2}$.",
          pasos=[
              paso("Aplicamos la ecuación punto-pendiente con $(x_1, y_1) = (1, -3)$ y $m = -\\tfrac{1}{2}$:\n\n"
                   "$$y - (-3) = -\\tfrac{1}{2}(x - 1).$$"),
              paso("Desarrollando: $y + 3 = -\\tfrac{1}{2}x + \\tfrac{1}{2}$, así $y = -\\tfrac{1}{2}x - \\tfrac{5}{2}.$"),
              paso("**Forma general** (multiplicando por $2$): $2y = -x - 5$, es decir, $\\boxed{x + 2y + 5 = 0}.$",
                   "Pasamos a la forma estándar.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Recta por dos puntos",
          problema_md="Encuentra la ecuación de la recta que pasa por los puntos $(-1, 2)$ y $(3, -4)$.",
          pasos=[
              paso("Calculamos la pendiente: $m = \\dfrac{-4 - 2}{3 - (-1)} = \\dfrac{-6}{4} = -\\dfrac{3}{2}.$"),
              paso("Usamos punto-pendiente con $(-1, 2)$:\n\n"
                   "$$y - 2 = -\\tfrac{3}{2}(x + 1).$$"),
              paso("Despejando: $y = -\\tfrac{3}{2}x + \\tfrac{1}{2}$, y multiplicando por $2$: $2y = -3x + 1$, "
                   "es decir, $\\boxed{3x + 2y - 1 = 0}.$",
                   "Forma general.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Rectas paralelas y perpendiculares.**\n\n"
              "Sean $L_1$ y $L_2$ dos rectas no verticales con pendientes $m_1$ y $m_2$.\n\n"
              "- $L_1 \\parallel L_2 \\iff m_1 = m_2.$\n"
              "- $L_1 \\perp L_2 \\iff m_1 \\cdot m_2 = -1.$\n\n"
              "Equivalentemente, dos rectas inclinadas son perpendiculares si una pendiente es la "
              "**recíproca con signo opuesto** de la otra: $m_2 = -\\tfrac{1}{m_1}.$\n\n"
              "Para rectas verticales-horizontales, la perpendicularidad se identifica directamente "
              "(eje $x$ ⊥ eje $y$) sin usar la fórmula del producto."
          )),

        b("ejemplo_resuelto",
          titulo="Recta paralela por un punto",
          problema_md="Encuentra la ecuación de la recta que pasa por el punto $(5, 2)$ y es paralela a la recta $4x + 6y + 5 = 0.$",
          pasos=[
              paso("Despejamos $y$ en la recta dada para obtener su pendiente: "
                   "$6y = -4x - 5 \\;\\Longrightarrow\\; y = -\\tfrac{2}{3}x - \\tfrac{5}{6}.$ "
                   "Pendiente $m = -\\tfrac{2}{3}.$"),
              paso("La recta buscada tiene la misma pendiente y pasa por $(5, 2)$: "
                   "$y - 2 = -\\tfrac{2}{3}(x - 5).$"),
              paso("Desarrollando: $y = -\\tfrac{2}{3}x + \\tfrac{16}{3}.$"),
              paso("Forma general (multiplicando por $3$): $3y = -2x + 16$, es decir, "
                   "$\\boxed{2x + 3y - 16 = 0}.$", "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Triángulo rectángulo por pendientes",
          problema_md="Demuestra que los puntos $P(3, 3)$, $Q(8, 17)$ y $R(11, 5)$ son los vértices de un triángulo **rectángulo**.",
          pasos=[
              paso("Calculamos las pendientes de los tres lados:\n\n"
                   "$m_{PQ} = \\dfrac{17 - 3}{8 - 3} = \\dfrac{14}{5},$\n\n"
                   "$m_{QR} = \\dfrac{5 - 17}{11 - 8} = \\dfrac{-12}{3} = -4,$\n\n"
                   "$m_{PR} = \\dfrac{5 - 3}{11 - 3} = \\dfrac{2}{8} = \\dfrac{1}{4}.$"),
              paso("Verificamos si algún par de lados es perpendicular: "
                   "$m_{QR} \\cdot m_{PR} = (-4)\\cdot \\tfrac{1}{4} = -1.$"),
              paso("Como $m_{QR}\\cdot m_{PR} = -1$, los lados $QR$ y $PR$ son perpendiculares; "
                   "el ángulo recto se ubica en el vértice $R$. Por lo tanto, "
                   "$\\boxed{\\triangle PQR \\text{ es rectángulo}}.$",
                   "Criterio de perpendicularidad.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Recta perpendicular por el origen",
          problema_md="Encuentra la ecuación de la recta perpendicular a $4x + 6y + 5 = 0$ que pasa por el origen.",
          pasos=[
              paso("La pendiente de la recta dada es $m_1 = -\\tfrac{2}{3}.$ "
                   "La pendiente perpendicular es $m_2 = -\\dfrac{1}{m_1} = -\\dfrac{1}{-2/3} = \\dfrac{3}{2}.$"),
              paso("Ecuación punto-pendiente con $(0, 0)$ y $m = \\tfrac{3}{2}$: "
                   "$y - 0 = \\tfrac{3}{2}(x - 0) \\;\\Longrightarrow\\; y = \\tfrac{3}{2}x.$"),
              paso("**Forma general:** $\\boxed{3x - 2y = 0}.$", "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Ángulo entre dos rectas.** Si $\\phi$ es un ángulo entre dos rectas con pendientes "
              "$m_1$ y $m_2$, entonces\n\n"
              "$$\\boxed{\\tan(\\phi) = \\frac{m_2 - m_1}{1 + m_1 m_2}},$$\n\n"
              "donde $m_2$ es la pendiente del lado **terminal** y $m_1$ la del lado **inicial** "
              "(medición antihoraria desde la primera recta hacia la segunda).\n\n"
              "**Observación.** Si $1 + m_1 m_2 = 0$, es decir $m_1 m_2 = -1$, la tangente no está "
              "definida y $\\phi = 90°$: las rectas son **perpendiculares**, lo que es consistente "
              "con el criterio anterior.\n\n"
              "**Deducción.** Si las inclinaciones son $\\theta_1$ y $\\theta_2$, entonces "
              "$\\phi = \\theta_2 - \\theta_1$, y aplicando la identidad de tangente de la diferencia "
              "se llega a la fórmula con $m_i = \\tan(\\theta_i)$."
          )),

        b("definicion",
          titulo="Distancia de un punto a una recta",
          body_md=(
              "Sea $L$ una recta y $P(x_1, y_1)$ un punto que **no está** en $L$. Se define la "
              "**distancia de $P$ a $L$** como la distancia entre $P$ y el punto $Q$, donde $Q$ es "
              "la intersección de la recta que pasa por $P$ y es perpendicular a $L$. Se denota $d(P, L).$\n\n"
              "Geométricamente, $d(P, L)$ es la longitud del segmento perpendicular desde $P$ hasta $L$, "
              "y es la **distancia mínima** entre $P$ y cualquier punto de $L$."
          )),

        b("teorema",
          enunciado_md=(
              "**Fórmula de la distancia punto-recta.** Sea $P(x_1, y_1)$ un punto del plano y $L$ "
              "la recta de ecuación general $ax + by + c = 0.$ Entonces\n\n"
              "$$\\boxed{\\,d(P, L) = \\dfrac{|a x_1 + b y_1 + c|}{\\sqrt{a^2 + b^2}}\\,}.$$\n\n"
              "**Idea de la demostración.** Si la recta no es vertical ($b \\ne 0$), se escribe "
              "$y = mx + n$ con $m = -a/b$ y $n = -c/b$. Se construye la perpendicular por $P$, se "
              "calcula la intersección $Q$ resolviendo el sistema y luego $d(P, L) = d(P, Q)$. "
              "Sustituyendo $m$ y $n$ se obtiene la forma con $a, b, c$ de la ecuación general."
          )),

        fig("Diagrama de la distancia de un punto P a una recta L: la recta L con etiqueta ax+by+c=0, "
            "el punto P fuera de la recta, y un segmento perpendicular punteado desde P hasta el pie Q en L, "
            "etiquetado d(P,L). " + STYLE),

        b("ejemplo_resuelto",
          titulo="Distancia desde la intersección de dos rectas",
          problema_md=("Encuentra la distancia del punto de intersección de las rectas "
                       "$x - y - 1 = 0$ y $x - 2y + 1 = 0$ a la recta $5x + 12y - 13 = 0.$"),
          pasos=[
              paso("Resolvemos el sistema. Restando las dos primeras ecuaciones: "
                   "$(x - y - 1) - (x - 2y + 1) = 0 \\;\\Longrightarrow\\; y - 2 = 0 \\;\\Longrightarrow\\; y = 2.$"),
              paso("Sustituyendo en la primera: $x - 2 - 1 = 0 \\;\\Longrightarrow\\; x = 3.$ "
                   "Punto de intersección: $P(3, 2).$"),
              paso("Aplicamos la fórmula de distancia con $a = 5$, $b = 12$, $c = -13$:\n\n"
                   "$$d(P, L) = \\frac{|5(3) + 12(2) - 13|}{\\sqrt{25 + 144}} = \\frac{|26|}{\\sqrt{169}} = \\frac{26}{13} = \\boxed{2}.$$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Distancia entre dos rectas paralelas",
          problema_md="Encuentra la distancia entre las rectas paralelas $15x + 8y + 68 = 0$ y $15x + 8y - 51 = 0.$",
          pasos=[
              paso("**Estrategia:** elegir un punto cualquiera de una recta y calcular su distancia a la otra.",
                   "Para rectas paralelas, la distancia es la misma desde cualquier punto."),
              paso("Tomamos un punto de la primera recta haciendo $x = 0$: "
                   "$8y + 68 = 0 \\;\\Longrightarrow\\; y = -\\tfrac{17}{2}.$ "
                   "Punto: $P\\!\\left(0, -\\tfrac{17}{2}\\right).$"),
              paso("Distancia de $P$ a la segunda recta $15x + 8y - 51 = 0$:\n\n"
                   "$$d = \\frac{|15(0) + 8(-17/2) - 51|}{\\sqrt{15^2 + 8^2}} = \\frac{|-68 - 51|}{\\sqrt{289}} = \\frac{119}{17} = \\boxed{7}.$$",
                   "Resultado.", resultado=True),
              paso("**Generalización.** La distancia entre dos rectas paralelas $ax + by + c_1 = 0$ y "
                   "$ax + by + c_2 = 0$ es $d = \\dfrac{|c_1 - c_2|}{\\sqrt{a^2 + b^2}}.$",
                   "Resultado teórico útil."),
          ]),

        ej(
            "Triángulo isósceles por distancias",
            ("Demuestra que el triángulo de vértices $A(2, -1)$, $B(-2, 2)$ y $C(5, 3)$ "
             "es **isósceles** calculando los tres lados."),
            ["Aplica la fórmula $d = \\sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}.$",
             "Compara $|AB|^2$, $|AC|^2$ y $|BC|^2$.",
             "Si dos coinciden, el triángulo es isósceles."],
            ("$|AB|^2 = (2+2)^2 + (-1-2)^2 = 16 + 9 = 25$, $|AB| = 5.$ "
             "$|AC|^2 = (2-5)^2 + (-1-3)^2 = 9 + 16 = 25$, $|AC| = 5.$ "
             "$|BC|^2 = (-2-5)^2 + (2-3)^2 = 49 + 1 = 50$, $|BC| = 5\\sqrt{2}.$ "
             "Como $|AB| = |AC| = 5$, el triángulo $ABC$ es **isósceles**.")
        ),

        ej(
            "Recta paralela por un punto",
            "Encuentra la ecuación de la recta que pasa por $(2, -3)$ y es paralela a $3x - 2y + 7 = 0.$",
            ["Despeja $y$ en la recta dada para obtener su pendiente.",
             "Usa la misma pendiente y la ecuación punto-pendiente con $(2, -3).$",
             "Reordena a forma general."],
            ("Pendiente de la recta dada: $y = \\tfrac{3}{2}x + \\tfrac{7}{2}$, así $m = \\tfrac{3}{2}.$ "
             "Recta buscada: $y + 3 = \\tfrac{3}{2}(x - 2)$, es decir, $y = \\tfrac{3}{2}x - 6.$ "
             "Forma general: $\\boxed{3x - 2y - 12 = 0}.$")
        ),

        ej(
            "Recta perpendicular por dos pasos",
            ("Determina la ecuación de la recta que pasa por $(4, 1)$ y es **perpendicular** a la "
             "recta de ecuación $2x + 5y - 10 = 0.$"),
            ["Encuentra la pendiente $m_1$ de la recta dada.",
             "La perpendicular tiene pendiente $m_2 = -1/m_1.$",
             "Aplica punto-pendiente."],
            ("La recta dada: $y = -\\tfrac{2}{5}x + 2$, $m_1 = -\\tfrac{2}{5}.$ "
             "Perpendicular: $m_2 = -\\dfrac{1}{-2/5} = \\dfrac{5}{2}.$ "
             "Ecuación: $y - 1 = \\tfrac{5}{2}(x - 4)$, es decir, $y = \\tfrac{5}{2}x - 9.$ "
             "Forma general: $\\boxed{5x - 2y - 18 = 0}.$")
        ),

        ej(
            "Distancia desde el origen a una recta",
            "Calcula la distancia desde el origen a la recta $3x - 4y + 25 = 0.$",
            ["Aplica la fórmula $d = |a x_0 + b y_0 + c|/\\sqrt{a^2 + b^2}.$",
             "Con $(x_0, y_0) = (0, 0)$ el numerador queda solo $|c|.$"],
            ("$d = \\dfrac{|3(0) - 4(0) + 25|}{\\sqrt{9 + 16}} = \\dfrac{25}{5} = \\boxed{5}.$")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "¿Cuál es la pendiente de la recta que pasa por $(2, 3)$ y $(5, 9)$?",
               "opciones_md": ["$1$", "$2$", "$3$", "$\\dfrac{2}{3}$"],
               "correcta": "B",
               "pista_md": "$m = \\dfrac{y_2 - y_1}{x_2 - x_1}$.",
               "explicacion_md": "$m = \\dfrac{9 - 3}{5 - 2} = \\dfrac{6}{3} = 2$. Mantenete consistente con el orden de los puntos en numerador y denominador."},
              {"enunciado_md": "Dos rectas $L_1$ y $L_2$ con pendientes $m_1 = 2/3$ y $m_2 = -3/2$ son:",
               "opciones_md": ["Paralelas", "Perpendiculares", "Coincidentes", "Oblicuas (sin relación especial)"],
               "correcta": "B",
               "pista_md": "$m_1 \\cdot m_2 = -1$ caracteriza rectas perpendiculares.",
               "explicacion_md": "$\\dfrac{2}{3} \\cdot \\left(-\\dfrac{3}{2}\\right) = -1$, por lo tanto las rectas son perpendiculares."},
              {"enunciado_md": "¿Cuál es la distancia desde el punto $(1, 2)$ a la recta $3x + 4y - 5 = 0$?",
               "opciones_md": ["$0$", "$1$", "$\\dfrac{6}{5}$", "$5$"],
               "correcta": "C",
               "pista_md": "$d = \\dfrac{|ax_0 + by_0 + c|}{\\sqrt{a^2+b^2}}$.",
               "explicacion_md": "$d = \\dfrac{|3(1) + 4(2) - 5|}{\\sqrt{9 + 16}} = \\dfrac{|3 + 8 - 5|}{5} = \\dfrac{6}{5}$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir pendiente con inclinación.** $m = \\tan\\theta$, no $\\theta$ directamente.",
              "**Olvidar el valor absoluto en la fórmula de distancia punto-recta.** El numerador siempre es no negativo.",
              "**Aplicar $m_1 \\cdot m_2 = -1$ a rectas verticales.** Las verticales no tienen pendiente; la perpendicularidad horizontal-vertical se identifica directamente.",
              "**Confundir la forma general con la explícita.** $Ax + By + C = 0$ describe también rectas verticales (cuando $B = 0$); $y = mx + n$ no lo hace.",
              "**Usar puntos en orden inconsistente al calcular pendiente.** Si cambias el orden en el numerador, debes cambiarlo también en el denominador.",
          ]),

        b("resumen",
          puntos_md=[
              "**Distancia entre puntos:** $d = \\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}.$",
              "**Inclinación y pendiente:** $\\theta \\in [0°, 180°)$ y $m = \\tan\\theta = \\Delta y / \\Delta x.$",
              "**Ecuaciones de la recta:** punto-pendiente $y - y_1 = m(x - x_1)$, dos puntos, y forma general $Ax + By + C = 0.$",
              "**Paralelismo:** $m_1 = m_2.$ **Perpendicularidad:** $m_1 m_2 = -1.$",
              "**Ángulo entre rectas:** $\\tan\\phi = (m_2 - m_1)/(1 + m_1 m_2).$",
              "**Distancia punto-recta:** $d = |a x_0 + b y_0 + c|/\\sqrt{a^2 + b^2}.$",
              "Próxima lección: **circunferencias** como lugar geométrico.",
          ]),
    ]
    return {"id": "lec-ia-5-1-rectas", "title": "Rectas y Distancia",
            "description": "Distancia entre puntos, pendiente, ecuaciones de la recta, paralelismo, perpendicularidad, ángulo entre rectas y distancia punto-recta.",
            "blocks": blocks, "duration_minutes": 60, "order": 1}


# ============================================================================
# 5.2 Circunferencias
# ============================================================================
def lesson_5_2():
    blocks = [
        b("texto", body_md=(
            "La **circunferencia** es una de las curvas más fundamentales de la geometría plana. "
            "Su estudio permite comprender cómo describir algebraicamente un objeto geométrico "
            "mediante ecuaciones, y cómo extraer información geométrica (centro, radio, tangentes) "
            "directamente desde la expresión algebraica.\n\n"
            "**En esta lección desarrollaremos:**\n\n"
            "- La circunferencia como **lugar geométrico** y su ecuación canónica.\n"
            "- La **forma general** de la ecuación y el método de **completar cuadrados**.\n"
            "- **Rectas tangentes** desde un punto exterior y de pendiente dada.\n"
            "- **Familias de circunferencias** y el concepto de **eje radical**.\n"
            "- **Posición relativa** de dos circunferencias."
        )),

        b("definicion",
          titulo="Circunferencia y ecuación canónica",
          body_md=(
              "Una **circunferencia** es el lugar geométrico de todos los puntos del plano que están a "
              "una **misma distancia** de un punto fijo. Al punto fijo lo llamamos **centro** y a la "
              "distancia común, **radio**.\n\n"
              "Sea $C(h, k)$ el centro y $r > 0$ el radio. Si $P(x, y)$ es cualquier punto de la "
              "circunferencia, entonces $d(P, C) = r$, es decir,\n\n"
              "$$\\sqrt{(x - h)^2 + (y - k)^2} = r.$$\n\n"
              "Elevando al cuadrado obtenemos la **ecuación canónica** (o estándar):\n\n"
              "$$\\boxed{\\,(x - h)^2 + (y - k)^2 = r^2\\,}.$$\n\n"
              "Esta forma exhibe directamente las coordenadas del centro $C(h, k)$ y la longitud del radio $r.$ "
              "Cuando el centro está en el origen ($h = k = 0$), la ecuación se reduce a $x^2 + y^2 = r^2.$"
          )),

        fig("Plano cartesiano con una circunferencia de centro C(h,k) marcado y un punto P(x,y) sobre ella; "
            "segmento radial de C a P etiquetado con r. Ejes con ticks en blanco. " + STYLE),

        b("teorema",
          enunciado_md=(
              "**Forma general de la circunferencia.** Expandiendo la ecuación canónica se obtiene la forma\n\n"
              "$$\\boxed{\\,x^2 + y^2 + Dx + Ey + F = 0\\,},$$\n\n"
              "con $D, E, F \\in \\mathbb{R}$. Esta ecuación se caracteriza por tener coeficientes "
              "**iguales** en $x^2$ e $y^2$ y por **no tener** término en $xy$. Las relaciones con el centro y radio son\n\n"
              "$$D = -2h, \\qquad E = -2k, \\qquad F = h^2 + k^2 - r^2.$$\n\n"
              "**Clasificación según el discriminante.** Completando cuadrados se llega a\n\n"
              "$$\\left(x + \\tfrac{D}{2}\\right)^2 + \\left(y + \\tfrac{E}{2}\\right)^2 = \\tfrac{D^2 + E^2 - 4F}{4}.$$\n\n"
              "Definiendo $\\Delta = D^2 + E^2 - 4F$:\n\n"
              "- $\\Delta > 0$: **circunferencia** de centro $\\left(-\\tfrac{D}{2}, -\\tfrac{E}{2}\\right)$ y radio $\\tfrac{\\sqrt{\\Delta}}{2}.$\n"
              "- $\\Delta = 0$: **un punto** (circunferencia degenerada de radio cero).\n"
              "- $\\Delta < 0$: **conjunto vacío** (la suma de cuadrados no puede ser negativa)."
          )),

        b("ejemplo_resuelto",
          titulo="Circunferencia por extremos del diámetro",
          problema_md="Encuentra la ecuación de la circunferencia que tiene como extremos del diámetro los puntos $A(-4, 6)$ y $B(2, 0).$",
          pasos=[
              paso("**Centro = punto medio de $AB$:** $C = \\left(\\tfrac{-4 + 2}{2}, \\tfrac{6 + 0}{2}\\right) = (-1, 3).$",
                   "El centro biseca el diámetro."),
              paso("**Radio = mitad de la longitud del diámetro:**\n\n"
                   "$r = \\dfrac{d(A, B)}{2} = \\dfrac{\\sqrt{(-4-2)^2 + (6-0)^2}}{2} = \\dfrac{\\sqrt{72}}{2} = 3\\sqrt{2}.$"),
              paso("**Ecuación canónica:** $(x - (-1))^2 + (y - 3)^2 = (3\\sqrt 2)^2$, es decir, "
                   "$\\boxed{(x + 1)^2 + (y - 3)^2 = 18}.$",
                   "Sustituimos en la fórmula canónica.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Identificar el tipo de gráfica completando cuadrados",
          problema_md=("Determina la gráfica de las siguientes ecuaciones:\n\n"
                       "**(a)** $5x^2 + 5y^2 - 14x + 7y - 24 = 0.$\n\n"
                       "**(b)** $x^2 + y^2 + 6x - 2y + 10 = 0.$\n\n"
                       "**(c)** $x^2 + y^2 + 8x - 18y + 100 = 0.$"),
          pasos=[
              paso("**(a)** Dividimos por $5$ para igualar los coeficientes de $x^2$ e $y^2$ a $1$: "
                   "$x^2 + y^2 - \\tfrac{14}{5}x + \\tfrac{7}{5}y - \\tfrac{24}{5} = 0.$"),
              paso("Completando cuadrados: "
                   "$\\left(x - \\tfrac{7}{5}\\right)^2 + \\left(y + \\tfrac{7}{10}\\right)^2 = \\tfrac{49}{25} + \\tfrac{49}{100} + \\tfrac{24}{5} = \\tfrac{725}{100} = \\tfrac{29}{4}.$ "
                   "Como $\\Delta > 0$, es una circunferencia de centro $\\left(\\tfrac{7}{5}, -\\tfrac{7}{10}\\right)$ y radio $r = \\tfrac{\\sqrt{29}}{2}.$"),
              paso("**(b)** Completando cuadrados: $(x + 3)^2 - 9 + (y - 1)^2 - 1 + 10 = 0$, es decir, "
                   "$(x + 3)^2 + (y - 1)^2 = 0.$ Como $\\Delta = 0$, la ecuación representa el **punto** $(-3, 1).$"),
              paso("**(c)** $(x + 4)^2 - 16 + (y - 9)^2 - 81 + 100 = 0$, es decir, "
                   "$(x + 4)^2 + (y - 9)^2 = -3.$ Como $\\Delta < 0$, la ecuación representa el **conjunto vacío**.",
                   "Resumen: tres casos posibles según el signo de $\\Delta$.", resultado=True),
          ]),

        b("definicion",
          titulo="Recta tangente a una circunferencia",
          body_md=(
              "La **recta tangente** a una circunferencia $C$ en un punto $P$ de ella es la recta "
              "**perpendicular al radio** en dicho punto. Esta definición geométrica tiene una "
              "consecuencia algebraica fundamental: una recta es tangente a una circunferencia si "
              "y solo si la **distancia del centro a la recta es igual al radio**.\n\n"
              "**Casos según la posición del punto $P$ respecto a la circunferencia $C$:**\n\n"
              "- $P$ en el **interior** de $C$: no existen rectas tangentes a $C$ que pasen por $P$.\n"
              "- $P$ **sobre** $C$: hay exactamente **una** tangente que pasa por $P.$\n"
              "- $P$ en el **exterior** de $C$: hay exactamente **dos** tangentes que pasan por $P.$"
          )),

        b("teorema",
          enunciado_md=(
              "**Condición de tangencia (geométrica).** Sea $L$ una recta y $C$ una circunferencia "
              "de centro $Q(h, k)$ y radio $r.$ Entonces\n\n"
              "$$L \\text{ es tangente a } C \\iff d(Q, L) = r.$$\n\n"
              "Si $L: Ax + By + C = 0$, esto equivale a\n\n"
              "$$\\frac{|A h + B k + C|}{\\sqrt{A^2 + B^2}} = r.$$\n\n"
              "**Condición de tangencia (algebraica).** Al sustituir la ecuación de la recta en la "
              "ecuación de la circunferencia, se obtiene una ecuación cuadrática. La recta es tangente "
              "si y solo si dicha cuadrática tiene **discriminante igual a cero** (raíz doble)."
          )),

        b("ejemplo_resuelto",
          titulo="Tangentes desde un punto exterior",
          problema_md=("Encuentra las ecuaciones de las tangentes trazadas desde el punto $(1, -1)$ a la "
                       "circunferencia $x^2 + y^2 + 2x - 6y - 6 = 0.$"),
          pasos=[
              paso("Familia de rectas que pasan por $(1, -1)$ con pendiente $m$: "
                   "$y + 1 = m(x - 1)$, es decir, $y = mx - m - 1.$"),
              paso("Sustituyendo en la ecuación de la circunferencia: "
                   "$x^2 + (mx - m - 1)^2 + 2x - 6(mx - m - 1) - 6 = 0.$ "
                   "Expandiendo y agrupando: $(1 + m^2)x^2 + (2 - 2m^2 - 8m)x + (m^2 + 8m + 1) = 0.$"),
              paso("Imponemos discriminante nulo: $(2 - 2m^2 - 8m)^2 - 4(1 + m^2)(m^2 + 8m + 1) = 0.$ "
                   "Simplificando se obtiene $3m^2 - 4m = 0$, es decir, $m(3m - 4) = 0$, con soluciones "
                   "$m_1 = 0$ y $m_2 = \\tfrac{4}{3}.$"),
              paso("Las dos tangentes son\n\n"
                   "$$\\boxed{y = -1 \\quad \\text{y} \\quad y + 1 = \\tfrac{4}{3}(x - 1)}.$$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Tangentes de pendiente dada",
          problema_md="Halla las ecuaciones de las tangentes de pendiente $m = 2$ a la circunferencia $x^2 + y^2 + 2x - 6y - 6 = 0.$",
          pasos=[
              paso("Las tangentes serán de la forma $y = 2x + k.$ Sustituyendo en la ecuación de la circunferencia:\n\n"
                   "$x^2 + (2x + k)^2 + 2x - 6(2x + k) - 6 = 0,$ que simplifica a "
                   "$5x^2 + (4k - 10)x + (k^2 - 6k - 6) = 0.$"),
              paso("Imponemos discriminante igual a cero: "
                   "$(4k - 10)^2 - 4 \\cdot 5 \\cdot (k^2 - 6k - 6) = 0.$"),
              paso("Simplificando: $k^2 - 10k - 55 = 0$, así $k = 5 \\pm 4\\sqrt{5}.$"),
              paso("Las dos tangentes paralelas de pendiente $2$ son\n\n"
                   "$$\\boxed{y = 2x + 5 + 4\\sqrt{5} \\quad \\text{y} \\quad y = 2x + 5 - 4\\sqrt{5}}.$$",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Circunferencia que pasa por tres puntos no colineales.** Dados tres puntos $P, Q, R$ "
              "no colineales, existe una **única** circunferencia que pasa por los tres.\n\n"
              "**Procedimiento.** Plantear la ecuación general $x^2 + y^2 + Dx + Ey + F = 0$ y "
              "sustituir las coordenadas de los tres puntos. Esto produce un **sistema lineal** "
              "$3 \\times 3$ en las incógnitas $D, E, F$, cuya solución es única.\n\n"
              "**Familias paramétricas.** Si $C_1: x^2 + y^2 + D_1 x + E_1 y + F_1 = 0$ y "
              "$C_2: x^2 + y^2 + D_2 x + E_2 y + F_2 = 0$ son dos circunferencias que se cortan en "
              "$P$ y $Q$, entonces toda circunferencia que pase por $P$ y $Q$ está dada por\n\n"
              "$$C_\\lambda:\\; (x^2 + y^2 + D_1 x + E_1 y + F_1) + \\lambda (x^2 + y^2 + D_2 x + E_2 y + F_2) = 0,$$\n\n"
              "para algún $\\lambda \\in \\mathbb{R}, \\lambda \\ne -1.$"
          )),

        b("definicion",
          titulo="Eje radical de dos circunferencias",
          body_md=(
              "Cuando $\\lambda = -1$ en la familia paramétrica anterior, los términos cuadráticos se cancelan "
              "y se obtiene la ecuación de una **recta**:\n\n"
              "$$\\boxed{\\,(D_1 - D_2) x + (E_1 - E_2) y + (F_1 - F_2) = 0\\,}.$$\n\n"
              "Esta recta se llama **eje radical** de las circunferencias $C_1$ y $C_2.$ Geométricamente, "
              "el eje radical es la recta que pasa por los **dos puntos de intersección** $P, Q$ cuando "
              "$C_1 \\cap C_2 = \\{P, Q\\}.$\n\n"
              "**Aplicación.** Para hallar los puntos de intersección de dos circunferencias secantes, "
              "conviene primero encontrar la ecuación del eje radical (restando miembro a miembro las dos "
              "ecuaciones en su forma general) y luego buscar las soluciones comunes a la recta y a una "
              "de las circunferencias."
          )),

        b("teorema",
          enunciado_md=(
              "**Posición relativa de dos circunferencias.** Sean $C_1$ y $C_2$ circunferencias con "
              "centros $Q_1, Q_2$ y radios $r_1, r_2.$ Sea $d = d(Q_1, Q_2).$ Entonces:\n\n"
              "- $d > r_1 + r_2$: **exteriores**, no se intersecan ($C_1 \\cap C_2 = \\emptyset$).\n"
              "- $d = r_1 + r_2$: **tangencia exterior**, se tocan en un punto.\n"
              "- $|r_1 - r_2| < d < r_1 + r_2$: **secantes**, se intersecan en dos puntos.\n"
              "- $d = |r_1 - r_2|$: **tangencia interior**, se tocan en un punto.\n"
              "- $d < |r_1 - r_2|$: una está dentro de la otra y no se intersecan."
          )),

        b("ejemplo_resuelto",
          titulo="Familia de curvas y condición de tangencia",
          problema_md=("Dada la familia de curvas $x^2 + y^2 - 8x + k - 1 = 0$, establece:\n\n"
                       "**(a)** Para qué valores de $k$ la curva es una **circunferencia**.\n\n"
                       "**(b)** Para qué valor de $k$ la circunferencia pasa por $P(7, 0).$\n\n"
                       "**(c)** Para qué valor de $k$ la circunferencia es tangente a la recta $x + y - 10 = 0.$"),
          pasos=[
              paso("Completamos el cuadrado en $x$: $(x - 4)^2 - 16 + y^2 + k - 1 = 0$, es decir, "
                   "$(x - 4)^2 + y^2 = 17 - k.$ Centro: $Q(4, 0)$; radio: $r = \\sqrt{17 - k}.$"),
              paso("**(a)** Para que sea circunferencia se necesita $17 - k > 0$, es decir, $\\boxed{k < 17}.$"),
              paso("**(b)** El punto $P(7, 0)$ debe satisfacer la ecuación: $(7 - 4)^2 + 0 = 17 - k$, "
                   "$9 = 17 - k$, así $\\boxed{k = 8}.$ Como $8 < 17$, efectivamente es una circunferencia."),
              paso("**(c)** Distancia del centro $(4, 0)$ a la recta $x + y - 10 = 0$:\n\n"
                   "$d(Q, L) = \\dfrac{|4 + 0 - 10|}{\\sqrt{1 + 1}} = \\dfrac{6}{\\sqrt{2}} = 3\\sqrt{2}.$"),
              paso("Imponiendo $r = 3\\sqrt{2}$: $\\sqrt{17 - k} = 3\\sqrt{2} \\;\\Longrightarrow\\; 17 - k = 18$, "
                   "es decir, $\\boxed{k = -1}.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Eje radical y puntos de intersección",
          problema_md=("Encuentra la ecuación del eje radical de las circunferencias\n\n"
                       "$C_1: (x + 2)^2 + (y - 4)^2 = 10$ y "
                       "$C_2: \\left(x - \\tfrac{1}{2}\\right)^2 + \\left(y - \\tfrac{3}{2}\\right)^2 = \\tfrac{5}{2},$\n\n"
                       "y determina sus puntos de intersección."),
          pasos=[
              paso("Expandimos ambas a forma general.\n\n"
                   "$C_1: x^2 + y^2 + 4x - 8y + 10 = 0.$\n\n"
                   "$C_2: x^2 + y^2 - x - 3y = 0.$"),
              paso("**Eje radical = $C_1 - C_2$:** "
                   "$(4 - (-1))x + (-8 - (-3))y + (10 - 0) = 0$, es decir, "
                   "$5x - 5y + 10 = 0$, simplificando $\\boxed{x - y + 2 = 0}.$"),
              paso("Para hallar los puntos de intersección, sustituimos $x = y - 2$ en $C_2$:\n\n"
                   "$(y - 2)^2 + y^2 - (y - 2) - 3y = 0,$ que simplifica a $2y^2 - 8y + 6 = 0$, es decir, "
                   "$(y - 1)(y - 3) = 0.$"),
              paso("$y_1 = 1 \\Rightarrow x_1 = -1$ y $y_2 = 3 \\Rightarrow x_2 = 1.$ "
                   "Los puntos de intersección son $\\boxed{P(-1, 1) \\text{ y } Q(1, 3)}.$",
                   "Resultado.", resultado=True),
          ]),

        ej(
            "Ecuación canónica desde forma general",
            "Determina centro y radio de la circunferencia $x^2 + y^2 - 6x + 4y - 12 = 0.$",
            ["Agrupa términos en $x$ y en $y$ por separado.",
             "Completa el cuadrado en cada variable.",
             "El miembro derecho positivo es $r^2.$"],
            ("$(x^2 - 6x + 9) + (y^2 + 4y + 4) = 12 + 9 + 4 = 25.$ "
             "Es decir, $(x - 3)^2 + (y + 2)^2 = 25.$ "
             "Centro: $(3, -2)$. Radio: $r = 5.$")
        ),

        ej(
            "Circunferencia tangente al eje x",
            "Encuentra la ecuación de la circunferencia con centro en $(3, 4)$ que es tangente al eje $x.$",
            ["Si la circunferencia es tangente al eje $x$, el radio es la distancia del centro al eje.",
             "Esa distancia es $|y_C| = 4.$"],
            ("$r = 4$, así la ecuación es $(x - 3)^2 + (y - 4)^2 = 16.$")
        ),

        ej(
            "Recta tangente a circunferencia en un punto",
            ("Encuentra la ecuación de la recta tangente a la circunferencia $x^2 + y^2 = 25$ en "
             "el punto $(3, 4)$ de ella."),
            ["La tangente es perpendicular al radio en el punto de tangencia.",
             "Pendiente del radio: $m_r = 4/3.$ Pendiente de la tangente: $m_t = -3/4.$",
             "Aplica punto-pendiente con $(3, 4).$"],
            ("$y - 4 = -\\tfrac{3}{4}(x - 3)$, simplificando $4y - 16 = -3x + 9$, es decir, "
             "$\\boxed{3x + 4y - 25 = 0}.$")
        ),

        ej(
            "Posición relativa de circunferencias",
            ("Determina la posición relativa de las circunferencias\n\n"
             "$C_1: x^2 + y^2 = 4$ y $C_2: (x - 5)^2 + y^2 = 9.$"),
            ["Calcula $d(Q_1, Q_2)$ y compara con $r_1 + r_2$ y $|r_1 - r_2|.$"],
            ("$Q_1 = (0, 0)$, $Q_2 = (5, 0)$, $d = 5.$ "
             "$r_1 = 2$, $r_2 = 3$, $r_1 + r_2 = 5.$ "
             "Como $d = r_1 + r_2$, las circunferencias son **tangentes exteriormente**.")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "¿Cuál es el centro y el radio de la circunferencia $(x-3)^2 + (y+2)^2 = 25$?",
               "opciones_md": ["Centro $(3, -2)$, radio $5$", "Centro $(3, -2)$, radio $25$", "Centro $(-3, 2)$, radio $5$", "Centro $(3, 2)$, radio $5$"],
               "correcta": "A",
               "pista_md": "La canónica es $(x-h)^2 + (y-k)^2 = r^2$.",
               "explicacion_md": "$h = 3$, $k = -2$ (cuidado con el signo: $(y+2)^2 = (y-(-2))^2$). $r^2 = 25 \\Rightarrow r = 5$."},
              {"enunciado_md": "Para que $x^2 + y^2 + Dx + Ey + F = 0$ represente una **circunferencia real** (no un punto ni vacío), debe cumplirse:",
               "opciones_md": ["$D^2 + E^2 - 4F > 0$", "$D^2 + E^2 - 4F < 0$", "$D = E = 0$", "$F > 0$"],
               "correcta": "A",
               "pista_md": "El radio al cuadrado debe ser positivo.",
               "explicacion_md": "Completando cuadrados: $r^2 = \\dfrac{D^2 + E^2 - 4F}{4}$. Si es $0$ es un punto, si es $< 0$ no representa nada real, si es $> 0$ es una circunferencia."},
              {"enunciado_md": "Dos circunferencias con centros separados por $d$ y radios $r_1, r_2$ son **tangentes exteriores** cuando:",
               "opciones_md": ["$d < r_1 + r_2$", "$d = r_1 + r_2$", "$d = |r_1 - r_2|$", "$d > r_1 + r_2$"],
               "correcta": "B",
               "pista_md": "Tangentes exteriores se tocan en un único punto sin solaparse.",
               "explicacion_md": "Tangencia exterior: $d = r_1 + r_2$ (un único punto de contacto, círculos disjuntos por dentro). Tangencia interior: $d = |r_1 - r_2|$. Secantes: $|r_1 - r_2| < d < r_1 + r_2$."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir centro y radio al leer la canónica.** En $(x - h)^2 + (y - k)^2 = r^2$, el centro es $(h, k)$ y el radio es $r$, no $r^2.$",
              "**No igualar coeficientes antes de completar cuadrados.** Si los coeficientes de $x^2$ e $y^2$ no son $1$, primero hay que dividir.",
              "**Ignorar los casos degenerados.** Si $\\Delta = 0$, la ecuación es un punto; si $\\Delta < 0$, es el conjunto vacío.",
              "**Usar la condición de tangencia incorrectamente.** $d(\\text{centro}, L) = r$ caracteriza tangencia, no que la recta corte a la circunferencia.",
              "**Confundir el eje radical con la recta de los centros.** El eje radical es perpendicular a la recta de los centros y, en el caso secante, pasa por los puntos de intersección.",
          ]),

        b("resumen",
          puntos_md=[
              "**Ecuación canónica:** $(x - h)^2 + (y - k)^2 = r^2$, con centro $(h, k)$ y radio $r > 0.$",
              "**Forma general:** $x^2 + y^2 + Dx + Ey + F = 0$, con $\\Delta = D^2 + E^2 - 4F.$ Tres casos: circunferencia ($\\Delta > 0$), punto ($\\Delta = 0$) o vacío ($\\Delta < 0$).",
              "**Tangencia recta-circunferencia:** $|Ah + Bk + C|/\\sqrt{A^2 + B^2} = r$, o equivalentemente discriminante de la cuadrática igual a cero.",
              "**Circunferencia por tres puntos:** sistema lineal $3 \\times 3$ en $D, E, F.$",
              "**Familia y eje radical:** $C_1 + \\lambda C_2 = 0$ describe la familia; $\\lambda = -1$ produce el eje radical $(D_1 - D_2)x + (E_1 - E_2)y + (F_1 - F_2) = 0.$",
              "**Posición relativa** de dos circunferencias se determina comparando $d(Q_1, Q_2)$ con $r_1 + r_2$ y $|r_1 - r_2|.$",
              "**Idea clave:** toda la teoría se basa en interpretar ecuaciones cuadráticas como objetos geométricos, usando completar cuadrados y discriminantes para extraer información geométrica.",
              "Próxima lección: la **parábola** como lugar geométrico de puntos equidistantes a un foco y una directriz.",
          ]),
    ]
    return {"id": "lec-ia-5-2-circunferencias", "title": "Circunferencias",
            "description": "Definición geométrica, ecuación canónica y general, tangentes, familias de circunferencias y eje radical.",
            "blocks": blocks, "duration_minutes": 70, "order": 2}


# ============================================================================
# 5.3 Parábolas
# ============================================================================
def lesson_5_3():
    blocks = [
        b("texto", body_md=(
            "La **parábola** es una de las curvas cónicas fundamentales del álgebra y la geometría "
            "analítica. Su estudio conecta la geometría del plano con el álgebra de las ecuaciones "
            "de segundo grado, y tiene aplicaciones que van desde la trayectoria de proyectiles "
            "hasta el diseño de antenas parabólicas y espejos telescópicos.\n\n"
            "**En esta lección estudiaremos:**\n\n"
            "- La **definición geométrica** de la parábola a partir del **foco** y la **directriz**.\n"
            "- La **ecuación canónica** con vértice en el origen ($y^2 = 4px$ y $x^2 = 4py$).\n"
            "- Identificación de **vértice, foco, directriz y lado recto** desde la ecuación.\n"
            "- La parábola con vértice desplazado en $(h, k).$\n"
            "- Conversión de **forma general** a forma canónica mediante completación de cuadrados."
        )),

        b("definicion",
          titulo="Parábola: definición geométrica",
          body_md=(
              "Una **parábola** es el conjunto de todos los puntos del plano que **equidistan** de un "
              "punto fijo $F$, llamado **foco**, y de una recta fija $D$, llamada **directriz**.\n\n"
              "Formalmente, un punto $P(x, y)$ pertenece a la parábola si y solo si\n\n"
              "$$\\boxed{\\,d(P, F) = d(P, D)\\,},$$\n\n"
              "donde $d(P, D)$ denota la distancia del punto $P$ a la recta directriz $D.$\n\n"
              "**Elementos de la parábola.**\n\n"
              "- **Foco $F$:** punto fijo de la definición; está en el interior de la curva.\n"
              "- **Directriz $D$:** recta fija exterior a la curva, paralela al eje de simetría transversal.\n"
              "- **Vértice $V$:** punto medio entre el foco y la proyección perpendicular del foco sobre la directriz; es el punto de la parábola más cercano al foco y a la directriz.\n"
              "- **Eje de la parábola:** recta que pasa por el foco y el vértice, perpendicular a la directriz.\n"
              "- **Parámetro $p$:** distancia dirigida del vértice al foco. Si $p > 0$ la parábola se abre en la dirección positiva del eje; si $p < 0$, en la dirección negativa."
          )),

        fig("Parábola con vértice V en el origen, foco F sobre el eje X a distancia p del vértice, y recta directriz vertical D a la izquierda. "
            "Un punto P sobre la parábola se conecta con segmento al foco y otro segmento perpendicular hasta la directriz, ambos con la misma longitud. " + STYLE),

        b("teorema",
          enunciado_md=(
              "**Ecuación canónica de la parábola con vértice en el origen.**\n\n"
              "Si elegimos los ejes coordenados de modo que el eje de la parábola coincida con el eje $X$ "
              "y el vértice esté en el origen $O(0, 0)$, con $p$ = distancia dirigida del vértice al foco, "
              "entonces el foco es $F(p, 0)$ y la directriz es $x = -p.$\n\n"
              "Imponiendo $d(P, F) = d(P, D)$ con $P(x, y)$:\n\n"
              "$$\\sqrt{(x - p)^2 + y^2} = |x + p|.$$\n\n"
              "Elevando al cuadrado y simplificando se obtiene\n\n"
              "$$\\boxed{\\,y^2 = 4 p x\\,}.$$\n\n"
              "**Caso eje paralelo al eje $Y$.** Análogamente, con vértice en $(0, 0)$ y eje sobre el eje $Y$:\n\n"
              "$$\\boxed{\\,x^2 = 4 p y\\,}.$$\n\n"
              "**Resumen de propiedades.**\n\n"
              "| Ecuación | Vértice | Foco | Directriz | Apertura |\n"
              "|---|---|---|---|---|\n"
              "| $y^2 = 4px$ | $(0,0)$ | $(p, 0)$ | $x = -p$ | derecha si $p>0$, izquierda si $p<0$ |\n"
              "| $x^2 = 4py$ | $(0,0)$ | $(0, p)$ | $y = -p$ | arriba si $p>0$, abajo si $p<0$ |"
          )),

        b("definicion",
          titulo="Cuerda focal y lado recto",
          body_md=(
              "Todo segmento de recta que pasa por el **foco** y cuyos extremos son puntos de la "
              "parábola se llama **cuerda focal**. Entre todas las cuerdas focales, la que es "
              "**perpendicular al eje** de la parábola recibe el nombre especial de **lado recto** "
              "(a veces *latus rectum*).\n\n"
              "El lado recto resume en un solo número cuán **\"abierta\" o \"cerrada\"** es la parábola.\n\n"
              "**Proposición.** La longitud del lado recto de la parábola $y^2 = 4 p x$ (o $x^2 = 4py$) es\n\n"
              "$$\\boxed{\\,\\ell = |4p|\\,}.$$\n\n"
              "**Justificación.** Para $y^2 = 4px$ el lado recto pasa por $F(p, 0)$ con $x = p$; sustituyendo: "
              "$y^2 = 4p \\cdot p = 4p^2 \\Rightarrow y = \\pm 2p.$ Los extremos son $(p, 2p)$ y $(p, -2p)$, "
              "y la longitud es $|2p - (-2p)| = |4p|.$"
          )),

        b("ejemplo_resuelto",
          titulo="Parábola dada la directriz",
          problema_md="Halla la ecuación de la parábola con vértice en el origen y directriz $y - 5 = 0.$",
          pasos=[
              paso("La directriz $y = 5$ es **horizontal**, paralela al eje $X.$ El eje de la parábola es "
                   "**vertical** (paralelo al eje $Y$), y la ecuación tiene la forma $x^2 = 4py.$"),
              paso("Para la parábola $x^2 = 4py$ la directriz es $y = -p.$ Igualando con la directriz dada: "
                   "$-p = 5$, así $p = -5.$"),
              paso("Ecuación: $x^2 = 4(-5)y$, es decir, $\\boxed{x^2 = -20 y}.$ "
                   "Como $p < 0$, la parábola se abre **hacia abajo**, con foco $F(0, -5)$ y directriz $y = 5.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Parábola que pasa por un punto",
          problema_md=("Una parábola con vértice en el origen y eje sobre el eje $X$ pasa por el punto "
                       "$(-2, 4).$ Halla la ecuación, las coordenadas del foco, la directriz y la longitud del lado recto."),
          pasos=[
              paso("Forma de la ecuación: $y^2 = 4 p x.$ Sustituyendo $(-2, 4)$:\n\n"
                   "$4^2 = 4p(-2) \\;\\Longrightarrow\\; 16 = -8 p \\;\\Longrightarrow\\; p = -2.$"),
              paso("Ecuación: $\\boxed{y^2 = -8 x}.$ Como $p < 0$, la parábola se abre **hacia la izquierda**."),
              paso("**Foco:** $F(-2, 0).$ **Directriz:** $x = 2.$ **Lado recto:** $\\ell = |4p| = 8.$ "
                   "Extremos del lado recto: $(-2, 4)$ y $(-2, -4).$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Lectura de una parábola desde su ecuación",
          problema_md="Encuentra el vértice, el foco, los extremos del lado recto y la directriz de la parábola $y^2 = -8 x.$",
          pasos=[
              paso("La ecuación tiene la forma $y^2 = 4 p x$ con $4p = -8$, así $p = -2.$ Como $p < 0$, "
                   "la parábola se abre **hacia la izquierda**."),
              paso("Vértice: $V(0, 0).$ Foco: $F(-2, 0).$ Directriz: $x = 2.$"),
              paso("Sustituyendo $x = p = -2$ en la ecuación: $y^2 = -8 \\cdot (-2) = 16$, así $y = \\pm 4.$ "
                   "Extremos del lado recto: $(-2, 4)$ y $(-2, -4).$ Longitud: $\\ell = |4p| = 8.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Intersección de rectas sobre la directriz",
          problema_md=("Demuestra que las rectas $m y = m^2 x + p$ y $m y + x = -p m^2$ se cortan sobre la "
                       "directriz de la parábola $y^2 = 4 p x.$"),
          pasos=[
              paso("La directriz de $y^2 = 4 p x$ es $x = -p.$ Hay que mostrar que el punto de intersección de "
                   "las dos rectas tiene coordenada $x = -p.$"),
              paso("Despejamos $y$ en la primera: $m y = m^2 x + p \\Rightarrow y = m x + \\tfrac{p}{m}$ (con $m \\ne 0$). "
                   "Sustituimos en la segunda: $m\\!\\left(m x + \\tfrac{p}{m}\\right) + x = -p m^2$, es decir, "
                   "$m^2 x + p + x = -p m^2.$"),
              paso("Agrupando: $x(m^2 + 1) = -p m^2 - p = -p(m^2 + 1).$ Dividiendo por $(m^2 + 1) \\ne 0$: "
                   "$\\boxed{x = -p}.$ El punto de intersección pertenece a la directriz. ∎",
                   "Conclusión.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Parábola con vértice desplazado en $(h, k).$**\n\n"
              "Cuando el vértice se traslada al punto $(h, k)$, basta realizar el cambio de variables "
              "$X = x - h$, $Y = y - k$ en las ecuaciones canónicas, dando lugar a:\n\n"
              "**Caso eje paralelo al eje $X$:**\n\n"
              "$$\\boxed{\\,(y - k)^2 = 4 p (x - h)\\,}.$$\n\n"
              "Foco: $F(h + p, k).$ Directriz: $x = h - p.$ Eje de simetría: $y = k.$ "
              "Apertura derecha si $p > 0$, izquierda si $p < 0.$\n\n"
              "**Caso eje paralelo al eje $Y$:**\n\n"
              "$$\\boxed{\\,(x - h)^2 = 4 p (y - k)\\,}.$$\n\n"
              "Foco: $F(h, k + p).$ Directriz: $y = k - p.$ Eje de simetría: $x = h.$ "
              "Apertura arriba si $p > 0$, abajo si $p < 0.$\n\n"
              "En ambos casos la longitud del lado recto es $\\ell = |4p|.$"
          )),

        b("teorema",
          enunciado_md=(
              "**Forma general de la ecuación de la parábola.**\n\n"
              "Al expandir las ecuaciones canónicas desplazadas, se obtiene que toda parábola con eje "
              "paralelo a uno de los ejes coordenados puede escribirse en alguna de las **formas generales**:\n\n"
              "**Eje paralelo al eje $Y$** (variable cuadrática es $x$):\n\n"
              "$$\\boxed{\\,x^2 + D x + E y + F = 0\\,}.$$\n\n"
              "**Eje paralelo al eje $X$** (variable cuadrática es $y$):\n\n"
              "$$\\boxed{\\,y^2 + D x + E y + F = 0\\,}.$$\n\n"
              "En ambos casos la ecuación es **cuadrática en una variable y lineal en la otra**.\n\n"
              "**Procedimiento de completación de cuadrado.** Para recuperar la forma canónica, se "
              "agrupan los términos en la variable cuadrática, se completa el cuadrado y se despeja "
              "el término lineal en la otra variable. Por ejemplo, para $y^2 + Dx + Ey + F = 0$:\n\n"
              "$$\\left(y + \\tfrac{E}{2}\\right)^2 = -Dx - F + \\tfrac{E^2}{4}.$$\n\n"
              "El lado derecho luego se factoriza como $4p(x - h)$ para identificar $h$, $k = -E/2$ y $p.$"
          )),

        b("ejemplo_resuelto",
          titulo="Parábola con vértice y foco dados",
          problema_md="Encuentra la ecuación de la parábola con vértice en $(5, -2)$ y foco en $(5, -4).$",
          pasos=[
              paso("Como el vértice $V(5, -2)$ y el foco $F(5, -4)$ tienen la **misma coordenada $x$**, "
                   "el eje de la parábola es **vertical** (paralelo al eje $Y$). Forma: $(x - h)^2 = 4 p (y - k)$ "
                   "con $h = 5$, $k = -2.$"),
              paso("Parámetro $p$ = distancia dirigida del vértice al foco, medida en la dirección del eje:\n\n"
                   "$p = y_F - y_V = -4 - (-2) = -2.$ Como $p < 0$, la parábola se abre **hacia abajo**."),
              paso("Sustituyendo: $(x - 5)^2 = 4(-2)(y - (-2))$, es decir, $\\boxed{(x - 5)^2 = -8(y + 2)}.$"),
              paso("La directriz es $y = k - p = -2 - (-2) = 0$, es decir, $y = 0.$",
                   "Lectura completa de la cónica.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="De forma general a forma canónica (eje horizontal)",
          problema_md="Dibuja la gráfica de $y^2 + 8x - 6y + 25 = 0.$",
          pasos=[
              paso("El término cuadrático está en $y$, por lo que el eje de la parábola es **horizontal** "
                   "(paralelo al eje $X$). Agrupamos los términos en $y$: $y^2 - 6y = -8x - 25.$"),
              paso("Completamos el cuadrado en $y$ sumando $\\left(\\tfrac{6}{2}\\right)^2 = 9$ a ambos lados:\n\n"
                   "$y^2 - 6y + 9 = -8x - 25 + 9 \\;\\Longrightarrow\\; (y - 3)^2 = -8x - 16.$"),
              paso("Factorizando el lado derecho: $(y - 3)^2 = -8(x + 2).$ Forma canónica $(y - k)^2 = 4p(x - h)$ "
                   "con $h = -2$, $k = 3$, $4p = -8$, así $p = -2.$"),
              paso("Como $p < 0$, la parábola se abre hacia la **izquierda**. "
                   "**Vértice:** $V(-2, 3).$ **Foco:** $F(-4, 3).$ **Directriz:** $x = 0.$ **Lado recto:** $\\ell = 8.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="De forma general a forma canónica (eje vertical)",
          problema_md="Construye la gráfica de la ecuación $x^2 - 6x - 12y - 51 = 0.$",
          pasos=[
              paso("El término cuadrático está en $x$, así que el eje de la parábola es **vertical**. "
                   "Agrupamos: $x^2 - 6x = 12y + 51.$"),
              paso("Completamos cuadrado en $x$ sumando $9$: $x^2 - 6x + 9 = 12y + 60$, es decir, "
                   "$(x - 3)^2 = 12y + 60 = 12(y + 5).$"),
              paso("Forma canónica $(x - h)^2 = 4p(y - k)$ con $h = 3$, $k = -5$, $4p = 12 \\Rightarrow p = 3.$ "
                   "Como $p > 0$, la parábola se abre hacia **arriba**."),
              paso("**Vértice:** $V(3, -5).$ **Foco:** $F(3, -2).$ **Directriz:** $y = -8.$ **Lado recto:** $\\ell = 12.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Parábola por tres puntos",
          problema_md="Una parábola cuyo eje es paralelo al eje $Y$ pasa por los puntos $(1, 1)$, $(2, 2)$ y $(-1, 5).$ Encuentra su ecuación.",
          pasos=[
              paso("Como el eje es paralelo al eje $Y$, la ecuación general es $x^2 + Dx + Ey + F = 0.$ "
                   "Sustituimos los tres puntos:\n\n"
                   "$(1, 1)$: $1 + D + E + F = 0$, es decir, $D + E + F = -1.$ (I)\n\n"
                   "$(2, 2)$: $4 + 2D + 2E + F = 0$, es decir, $2D + 2E + F = -4.$ (II)\n\n"
                   "$(-1, 5)$: $1 - D + 5E + F = 0$, es decir, $-D + 5E + F = -1.$ (III)"),
              paso("Restando (I) de (II): $D + E = -3.$ (IV) Sumando (I) y (III): $6E + 2F = -2$, es decir, "
                   "$3E + F = -1.$ (V) De (I): $F = -1 - D - E.$"),
              paso("Sustituyendo en (V): $3E + (-1 - D - E) = -1 \\Rightarrow 2E - D = 0 \\Rightarrow D = 2E.$ (VI) "
                   "En (IV): $2E + E = -3 \\Rightarrow E = -1.$ Luego $D = -2$ y $F = -1 - (-2) - (-1) = 2.$"),
              paso("Ecuación: $\\boxed{x^2 - 2x - y + 2 = 0}$, o equivalentemente $(x - 1)^2 = y - 1$, "
                   "con vértice $V(1, 1)$ y $p = \\tfrac{1}{4}.$",
                   "Resultado.", resultado=True),
          ]),

        ej(
            "Parábola con foco y directriz dados",
            "Encuentra la ecuación de la parábola cuyo foco es $F(0, 3)$ y cuya directriz es $y = -3.$",
            ["El vértice está a igual distancia del foco y de la directriz: $V(0, 0).$",
             "El eje es vertical (paralelo al $Y$). $p = $ distancia dirigida $V \\to F.$"],
            ("Vértice: $(0, 0).$ $p = 3.$ Ecuación: $x^2 = 4(3) y$, es decir, $\\boxed{x^2 = 12 y}.$")
        ),

        ej(
            "Parábola y altura del proyectil",
            ("Una parábola tiene su vértice en el origen, eje sobre el eje $Y$ y pasa por el punto $(4, 2).$ "
             "Encuentra su foco y su directriz."),
            ["Forma: $x^2 = 4py.$ Sustituye $(4, 2)$ para hallar $p.$",
             "Foco $(0, p)$, directriz $y = -p.$"],
            ("$16 = 4p \\cdot 2 \\Rightarrow p = 2.$ Ecuación: $x^2 = 8y.$ "
             "Foco: $F(0, 2).$ Directriz: $y = -2.$")
        ),

        ej(
            "Completar cuadrado en parábola",
            "Identifica el vértice, foco y directriz de la parábola $y^2 - 4y - 8x + 28 = 0.$",
            ["Agrupa los términos en $y$ y completa el cuadrado.",
             "Despeja la forma $(y - k)^2 = 4p(x - h).$"],
            ("$(y - 2)^2 - 4 - 8x + 28 = 0$, así $(y - 2)^2 = 8x - 24 = 8(x - 3).$ "
             "$h = 3$, $k = 2$, $4p = 8 \\Rightarrow p = 2.$ "
             "Vértice: $V(3, 2).$ Foco: $F(5, 2).$ Directriz: $x = 1.$")
        ),

        ej(
            "Lado recto y apertura",
            "¿Cuál es el lado recto de la parábola $(x + 1)^2 = -16(y - 3)$? ¿Hacia dónde se abre?",
            ["Lee $4p$ de la forma canónica.",
             "El signo de $p$ indica la apertura."],
            ("$4p = -16 \\Rightarrow p = -4.$ Lado recto: $\\ell = |4p| = 16.$ "
             "Como $p < 0$ y el eje es vertical, la parábola se abre **hacia abajo**.")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "Para la parábola $y^2 = 12x$, ¿cuál es la distancia del vértice al foco?",
               "opciones_md": ["$3$", "$6$", "$12$", "$1.5$"],
               "correcta": "A",
               "pista_md": "Comparar con $y^2 = 4px$: $4p = 12$.",
               "explicacion_md": "$4p = 12 \\Rightarrow p = 3$. La distancia del vértice al foco es $|p| = 3$. El foco está en $(3, 0)$ y la directriz es $x = -3$."},
              {"enunciado_md": "La parábola $(x - 2)^2 = -8(y - 1)$ se abre hacia:",
               "opciones_md": ["Arriba", "Abajo", "Derecha", "Izquierda"],
               "correcta": "B",
               "pista_md": "El eje cuadrático es $x$ y el coeficiente es negativo.",
               "explicacion_md": "Como $x$ es la variable cuadrática, el eje de simetría es vertical. $4p = -8 \\Rightarrow p < 0$, por lo que se abre hacia **abajo**."},
              {"enunciado_md": "El **lado recto** de una parábola con $4p = 16$ vale:",
               "opciones_md": ["$4$", "$8$", "$16$", "$32$"],
               "correcta": "C",
               "pista_md": "El lado recto es $|4p|$.",
               "explicacion_md": "El lado recto (longitud de la cuerda focal perpendicular al eje) es $\\ell = |4p| = 16$. Mide cuán abierta es la parábola."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir $4p$ con $p.$** En $y^2 = 4px$, el coeficiente es $4p$, no $p$; el foco está a distancia $|p|$ del vértice, no $|4p|.$",
              "**Olvidar el signo de $p.$** Si $p < 0$, la parábola se abre en la dirección negativa del eje correspondiente.",
              "**Confundir la dirección del eje al leer la ecuación.** Si la variable cuadrática es $y$, el eje es horizontal (paralelo al $X$); si es $x$, el eje es vertical.",
              "**Poner directriz $y = p$ en lugar de $y = -p.$** La directriz está en el lado **opuesto** al foco respecto al vértice.",
              "**Olvidar completar el cuadrado** al pasar de forma general a canónica; sin ese paso no se identifican $h$, $k$ ni $p.$",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición geométrica:** $d(P, F) = d(P, D)$, donde $F$ es el foco y $D$ la directriz.",
              "**Canónica con vértice en el origen:** $y^2 = 4px$ (eje $X$) y $x^2 = 4py$ (eje $Y$).",
              "**Canónica con vértice en $(h, k)$:** $(y - k)^2 = 4p(x - h)$ y $(x - h)^2 = 4p(y - k).$",
              "**Foco y directriz:** se ubican a distancia $|p|$ del vértice en la dirección del eje, en lados **opuestos**.",
              "**Lado recto:** $\\ell = |4p|.$ Resume cuán abierta es la parábola.",
              "**Forma general:** $x^2 + Dx + Ey + F = 0$ o $y^2 + Dx + Ey + F = 0$, según el eje. Se reduce a canónica completando el cuadrado en la variable cuadrática.",
              "**Estrategia general** para analizar una parábola dada en forma general: identificar la variable cuadrática, agrupar, completar el cuadrado, factorizar como $4p(\\cdot)$ y leer $h, k, p.$",
              "Próxima lección: la **elipse** como suma constante de distancias a dos focos.",
          ]),
    ]
    return {"id": "lec-ia-5-3-parabolas", "title": "Parábolas",
            "description": "Definición geométrica (foco y directriz), ecuación canónica con vértice en el origen y desplazado, lado recto y forma general.",
            "blocks": blocks, "duration_minutes": 70, "order": 3}


# ============================================================================
# 5.4 Elipses
# ============================================================================
def lesson_5_4():
    blocks = [
        b("texto", body_md=(
            "La **elipse** es una de las curvas cónicas más importantes del álgebra y la geometría "
            "analítica. Aparece de manera natural en la descripción de las **órbitas planetarias**, en "
            "el diseño de recintos acústicos y en numerosas aplicaciones de ingeniería y arquitectura. "
            "Su estudio permite comprender cómo una condición geométrica sencilla — la suma constante "
            "de distancias a dos puntos fijos — da origen a una ecuación algebraica elegante y poderosa.\n\n"
            "**En esta lección estudiaremos:**\n\n"
            "- La **definición geométrica** de la elipse y sus elementos: focos, vértices, ejes mayor y menor, lados rectos y excentricidad.\n"
            "- La **ecuación canónica** con centro en el origen, en los casos de eje mayor horizontal y vertical.\n"
            "- La elipse con **centro desplazado** en $(h, k).$\n"
            "- La **ecuación general** $A x^2 + C y^2 + D x + E y + F = 0$ y la técnica de completar el cuadrado para identificar y graficar."
        )),

        b("definicion",
          titulo="Elipse: definición geométrica",
          body_md=(
              "Una **elipse** es el lugar geométrico de los puntos del plano que se mueven de manera "
              "que la **suma de sus distancias** a dos puntos fijos del plano se mantiene constante "
              "y es **mayor que la distancia** entre esos dos puntos fijos. Los puntos fijos $F_1$ y "
              "$F_2$ se llaman **focos** de la elipse.\n\n"
              "Formalmente, si $P(x, y)$ es un punto cualquiera de la elipse, entonces se cumple\n\n"
              "$$\\boxed{\\,d(P, F_1) + d(P, F_2) = 2 a\\,},$$\n\n"
              "donde $2 a$ es la constante de la suma y se exige que $2a > d(F_1, F_2).$ La cantidad "
              "$a$ recibe el nombre de **semieje mayor**."
          )),

        fig("Plano cartesiano con dos focos F1 y F2 sobre el eje X equidistantes del origen, una elipse alrededor de ellos, "
            "un punto P sobre la elipse y dos segmentos PF1 y PF2 marcados; al lado, etiqueta PF1+PF2=2a. " + STYLE),

        b("definicion",
          titulo="Elementos de la elipse",
          body_md=(
              "Una elipse posee varios elementos geométricos fundamentales. Considera una elipse con "
              "focos $F_1$ y $F_2$ y constante de suma $2a.$\n\n"
              "- **Eje focal:** recta que pasa por los dos focos.\n"
              "- **Vértices $V_1, V_2$:** intersecciones del eje focal con la elipse. El segmento $\\overline{V_1 V_2}$ se llama **eje mayor** y mide $2a.$\n"
              "- **Centro:** punto medio del segmento $\\overline{F_1 F_2}$ (también del eje mayor).\n"
              "- **Eje menor:** segmento $\\overline{B_1 B_2}$ donde $B_1, B_2$ son las intersecciones de la elipse con la recta perpendicular al eje focal por el centro. Su longitud es $2b$, donde $b^2 = a^2 - c^2$ y $c$ es la distancia del centro a cada foco.\n"
              "- **Lados rectos:** segmentos determinados por las intersecciones de la elipse con las rectas que pasan por los focos y son perpendiculares al eje focal. Cada lado recto tiene longitud $\\dfrac{2 b^2}{a}.$\n"
              "- **Excentricidad:** $e = \\dfrac{c}{a} = \\dfrac{\\sqrt{a^2 - b^2}}{a}.$ Cumple $0 < e < 1.$ Mide cuán \"achatada\" es la elipse: $e \\approx 0$ es casi circular; $e \\approx 1$ es muy alargada."
          )),

        b("teorema",
          enunciado_md=(
              "**Ecuación canónica de la elipse con centro en el origen.**\n\n"
              "**Caso 1 — Eje mayor horizontal.** La elipse de focos $F_1(c, 0)$ y $F_2(-c, 0)$ en la "
              "que $2a$ es la suma de distancias a ambos focos, es la gráfica de\n\n"
              "$$\\boxed{\\,\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1\\,}, \\qquad b^2 = a^2 - c^2.$$\n\n"
              "El eje mayor está sobre el eje $X.$ Vértices: $(\\pm a, 0).$ Extremos del eje menor: $(0, \\pm b).$\n\n"
              "**Caso 2 — Eje mayor vertical.** La elipse de focos $F_1(0, c)$ y $F_2(0, -c)$ es la gráfica de\n\n"
              "$$\\boxed{\\,\\frac{x^2}{b^2} + \\frac{y^2}{a^2} = 1\\,}, \\qquad b^2 = a^2 - c^2.$$\n\n"
              "El eje mayor está sobre el eje $Y.$ Vértices: $(0, \\pm a).$ Extremos del eje menor: $(\\pm b, 0).$\n\n"
              "**Observación clave.** En ambos casos, $a$ es siempre el **semieje mayor** y va debajo de la "
              "variable cuyo eje contiene a los focos. Si $a^2$ está bajo $x^2$, el eje mayor es horizontal; "
              "si $a^2$ está bajo $y^2$, es vertical."
          )),

        b("ejemplo_resuelto",
          titulo="Lectura completa de una elipse",
          problema_md="Construye la gráfica de la ecuación $16 x^2 + 25 y^2 = 400.$ Determina los focos, vértices, longitud de los lados rectos y los valores de $a, b$ y $c.$",
          pasos=[
              paso("Dividimos ambos lados por $400$ para obtener la forma canónica:\n\n"
                   "$\\dfrac{x^2}{25} + \\dfrac{y^2}{16} = 1.$"),
              paso("Identificamos $a^2 = 25$ y $b^2 = 16$, así $a = 5$ y $b = 4.$ "
                   "El **mayor denominador está bajo $x^2$**, así el **eje mayor es horizontal**."),
              paso("Calculamos $c$: $c = \\sqrt{a^2 - b^2} = \\sqrt{25 - 16} = \\sqrt{9} = 3.$"),
              paso("**Focos:** $F_1(3, 0)$ y $F_2(-3, 0).$ "
                   "**Vértices:** $V_1(5, 0)$ y $V_2(-5, 0).$ "
                   "**Extremos del eje menor:** $B_1(0, 4)$ y $B_2(0, -4).$ "
                   "**Longitud del lado recto:** $\\dfrac{2 b^2}{a} = \\dfrac{2 \\cdot 16}{5} = \\dfrac{32}{5}.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Elipse a partir de vértices y focos",
          problema_md="Determina la ecuación de la elipse cuyos vértices son los puntos $(4, 0)$ y $(-4, 0)$, y tiene focos en los puntos $(3, 0)$ y $(-3, 0).$",
          pasos=[
              paso("Los vértices están sobre el eje $X$, así que el eje mayor es horizontal y la ecuación tiene la forma "
                   "$\\dfrac{x^2}{a^2} + \\dfrac{y^2}{b^2} = 1.$"),
              paso("De los vértices $(\\pm 4, 0)$ obtenemos $a = 4$, $a^2 = 16.$ "
                   "De los focos $(\\pm 3, 0)$ obtenemos $c = 3.$"),
              paso("Calculamos $b^2 = a^2 - c^2 = 16 - 9 = 7.$"),
              paso("Ecuación: $\\boxed{\\dfrac{x^2}{16} + \\dfrac{y^2}{7} = 1}.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Elipse a partir de un foco y la excentricidad",
          problema_md=("Una elipse tiene centro en el origen y su eje mayor está sobre el eje $X.$ Si uno de sus "
                       "focos es $(3, 0)$ y la excentricidad es $\\tfrac{1}{2}$, determina:\n\n"
                       "**(a)** la ecuación de la elipse,\n\n**(b)** las coordenadas del otro foco,\n\n"
                       "**(c)** la longitud de los lados rectos,\n\n**(d)** la longitud de los ejes mayor y menor."),
          pasos=[
              paso("**(a)** Sabemos que $c = 3$ y $e = \\dfrac{c}{a} = \\dfrac{1}{2}$, así $\\dfrac{3}{a} = \\dfrac{1}{2} \\Rightarrow a = 6$, "
                   "$a^2 = 36.$ Calculamos $b^2 = a^2 - c^2 = 36 - 9 = 27.$\n\n"
                   "Ecuación: $\\boxed{\\dfrac{x^2}{36} + \\dfrac{y^2}{27} = 1}.$"),
              paso("**(b)** El otro foco es $F_2(-3, 0).$"),
              paso("**(c)** Lado recto: $\\dfrac{2 b^2}{a} = \\dfrac{2 \\cdot 27}{6} = 9.$"),
              paso("**(d)** Eje mayor: $2 a = 12.$ Eje menor: $2 b = 2\\sqrt{27} = 6\\sqrt{3}.$",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Ecuación de la elipse con centro desplazado en $(h, k).$**\n\n"
              "Cuando el centro no está en el origen sino en $(h, k)$, las ecuaciones canónicas se "
              "modifican trasladando los ejes:\n\n"
              "**Eje mayor horizontal:**\n\n"
              "$$\\boxed{\\,\\frac{(x - h)^2}{a^2} + \\frac{(y - k)^2}{b^2} = 1\\,}, \\qquad b^2 = a^2 - c^2.$$\n\n"
              "Focos: $(h \\pm c, k).$ Vértices: $(h \\pm a, k).$\n\n"
              "**Eje mayor vertical:**\n\n"
              "$$\\boxed{\\,\\frac{(x - h)^2}{b^2} + \\frac{(y - k)^2}{a^2} = 1\\,}, \\qquad b^2 = a^2 - c^2.$$\n\n"
              "Focos: $(h, k \\pm c).$ Vértices: $(h, k \\pm a).$\n\n"
              "Para pasar de la ecuación general a la forma canónica desplazada, se utiliza la técnica de "
              "**completar el cuadrado** en $x$ y en $y.$"
          )),

        b("teorema",
          enunciado_md=(
              "**Ecuación general de la elipse.** La ecuación general de una elipse es de la forma\n\n"
              "$$A x^2 + C y^2 + D x + E y + F = 0, \\qquad A C > 0 \\text{ y } A \\ne C,$$\n\n"
              "que puede representar una **elipse**, un **punto** (elipse degenerada) o el **conjunto vacío**, "
              "según los valores de las constantes.\n\n"
              "**Estrategia.** Para identificar y graficar la curva: agrupar los términos en $x$ y en $y$, "
              "factorizar los coeficientes cuadráticos $A$ y $C$ y **completar cuadrado** en cada variable "
              "para llevar la ecuación a la forma canónica desplazada. Si los dos cuadrados se anulan al "
              "mismo tiempo, la curva colapsa en un punto; si la suma debe ser negativa, no hay solución real."
          )),

        b("ejemplo_resuelto",
          titulo="Elipse general (caso elipse válida)",
          problema_md="Determina la gráfica de la ecuación $25 x^2 + 9 y^2 + 150 x - 36 y + 36 = 0.$",
          pasos=[
              paso("Agrupamos y completamos cuadrados:\n\n"
                   "$25(x^2 + 6x) + 9(y^2 - 4y) = -36.$"),
              paso("$25(x^2 + 6x + 9) + 9(y^2 - 4y + 4) = -36 + 25\\cdot 9 + 9\\cdot 4 = -36 + 225 + 36 = 225.$"),
              paso("$25(x + 3)^2 + 9(y - 2)^2 = 225.$ Dividiendo por $225$:\n\n"
                   "$\\dfrac{(x + 3)^2}{9} + \\dfrac{(y - 2)^2}{25} = 1.$"),
              paso("Es una elipse de **centro $(-3, 2)$**, $a^2 = 25$ (bajo $y$, así eje mayor **vertical**), "
                   "$b^2 = 9$, $a = 5$, $b = 3$, $c = \\sqrt{25 - 9} = 4.$ "
                   "**Focos:** $(-3, 2 \\pm 4)$, es decir, $(-3, 6)$ y $(-3, -2).$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Elipse degenerada (un punto)",
          problema_md="Determina la gráfica de la ecuación $x^2 + 4 y^2 - 2 x - 8 y + 5 = 0.$",
          pasos=[
              paso("Agrupamos: $(x^2 - 2x) + 4(y^2 - 2y) = -5.$"),
              paso("$(x^2 - 2x + 1) + 4(y^2 - 2y + 1) = -5 + 1 + 4 = 0$, es decir, "
                   "$(x - 1)^2 + 4(y - 1)^2 = 0.$"),
              paso("La única forma de que una suma de cuadrados sea cero es que cada término se anule: "
                   "$x = 1$ e $y = 1.$ La gráfica es **el punto $(1, 1)$** (elipse degenerada).",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Elipse desde focos y suma de distancias",
          problema_md="Encuentra la ecuación de la elipse cuyos focos son $F_1(5, 0)$ y $F_2(-5, 0)$ y tal que la suma de las distancias de los puntos de ella a los focos sea $12.$",
          pasos=[
              paso("De los datos: $c = 5$ y $2a = 12$, así $a = 6$ y $a^2 = 36.$ "
                   "Como los focos están sobre el eje $X$, la ecuación es $\\dfrac{x^2}{a^2} + \\dfrac{y^2}{b^2} = 1.$"),
              paso("$b^2 = a^2 - c^2 = 36 - 25 = 11.$"),
              paso("Ecuación: $\\boxed{\\dfrac{x^2}{36} + \\dfrac{y^2}{11} = 1}.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Lugar geométrico que resulta una elipse",
          problema_md=("Un punto $P(x, y)$ se mueve de tal forma que el producto de las pendientes de las dos rectas que "
                       "unen $P$ con los puntos fijos $A(1, -2)$ y $B(5, 6)$ es constante e igual a $-2.$ "
                       "Demuestra que dicho lugar geométrico es una elipse e indica su centro."),
          pasos=[
              paso("Pendientes: $m_1 = \\dfrac{y + 2}{x - 1}$ y $m_2 = \\dfrac{y - 6}{x - 5}.$ "
                   "La condición $m_1 \\cdot m_2 = -2$ da:\n\n"
                   "$\\dfrac{(y + 2)(y - 6)}{(x - 1)(x - 5)} = -2.$"),
              paso("Cruzando: $(y + 2)(y - 6) = -2(x - 1)(x - 5).$ Expandiendo: "
                   "$y^2 - 4y - 12 = -2(x^2 - 6x + 5) = -2x^2 + 12x - 10.$"),
              paso("Reordenando: $2x^2 + y^2 - 12x - 4y - 2 = 0.$ Completando cuadrados: "
                   "$2(x^2 - 6x + 9) + (y^2 - 4y + 4) = 2 + 18 + 4 = 24$, es decir, "
                   "$2(x - 3)^2 + (y - 2)^2 = 24.$"),
              paso("Dividiendo por $24$: $\\dfrac{(x - 3)^2}{12} + \\dfrac{(y - 2)^2}{24} = 1.$ "
                   "Es una **elipse** con $a^2 = 24$, $b^2 = 12$, eje mayor **vertical**, "
                   "y **centro $(3, 2)$**, que coincide con el punto medio de $A(1, -2)$ y $B(5, 6).$ ∎",
                   "Resultado.", resultado=True),
          ]),

        ej(
            "Lectura desde forma canónica",
            "Halla los focos, vértices y excentricidad de la elipse $\\dfrac{x^2}{49} + \\dfrac{y^2}{24} = 1.$",
            ["$a^2 = 49$, $b^2 = 24$.",
             "$c^2 = a^2 - b^2.$",
             "Eje mayor sobre el eje $X$ porque $a^2 > b^2$ está bajo $x^2.$"],
            ("$a = 7$, $b = 2\\sqrt{6}$, $c^2 = 25 \\Rightarrow c = 5.$ "
             "**Vértices:** $(\\pm 7, 0).$ **Focos:** $(\\pm 5, 0).$ "
             "**Excentricidad:** $e = c/a = 5/7.$")
        ),

        ej(
            "Elipse con centro desplazado",
            "Identifica centro, semiejes y focos de la elipse $\\dfrac{(x - 2)^2}{25} + \\dfrac{(y + 1)^2}{9} = 1.$",
            ["Centro: $(h, k) = (2, -1).$",
             "$a^2 = 25$, $b^2 = 9.$ Eje mayor horizontal.",
             "Focos: $(h \\pm c, k).$"],
            ("$a = 5$, $b = 3$, $c = 4.$ "
             "**Centro:** $(2, -1).$ **Vértices:** $(7, -1)$ y $(-3, -1).$ "
             "**Focos:** $(6, -1)$ y $(-2, -1).$")
        ),

        ej(
            "Elipse desde semiejes",
            "Encuentra la ecuación canónica de la elipse con centro en el origen, semieje mayor $4$ sobre el eje $Y$ y semieje menor $2.$",
            ["El eje mayor es vertical, así $a^2$ va bajo $y^2.$",
             "$\\dfrac{x^2}{b^2} + \\dfrac{y^2}{a^2} = 1$ con $a = 4$, $b = 2.$"],
            ("$\\dfrac{x^2}{4} + \\dfrac{y^2}{16} = 1.$")
        ),

        ej(
            "Pasar de general a canónica",
            "Lleva a forma canónica la ecuación $4x^2 + 9y^2 - 8x + 36y + 4 = 0$ y describe la elipse.",
            ["Agrupa términos en $x$ y en $y.$",
             "Factoriza los coeficientes y completa cuadrados.",
             "Divide por la constante para obtener $1.$"],
            ("$4(x^2 - 2x + 1) + 9(y^2 + 4y + 4) = -4 + 4 + 36 = 36.$ "
             "$4(x - 1)^2 + 9(y + 2)^2 = 36$, es decir, $\\dfrac{(x - 1)^2}{9} + \\dfrac{(y + 2)^2}{4} = 1.$ "
             "Centro $(1, -2)$, $a = 3$, $b = 2$, $c = \\sqrt 5.$ Eje mayor horizontal. "
             "**Focos:** $(1 \\pm \\sqrt 5, -2).$")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "Para la elipse $\\dfrac{x^2}{25} + \\dfrac{y^2}{16} = 1$, ¿cuál es la distancia entre los focos?",
               "opciones_md": ["$3$", "$6$", "$8$", "$10$"],
               "correcta": "B",
               "pista_md": "$c^2 = a^2 - b^2$, distancia entre focos $= 2c$.",
               "explicacion_md": "$a^2 = 25$, $b^2 = 16$, $c^2 = 25 - 16 = 9$, $c = 3$. La distancia entre los dos focos es $2c = 6$."},
              {"enunciado_md": "¿Cuál es la relación correcta entre $a$, $b$ y $c$ en la elipse?",
               "opciones_md": ["$c^2 = a^2 + b^2$", "$c^2 = a^2 - b^2$ con $a > b$", "$a^2 = b^2 + c^2$ con $b > a$", "$b^2 = a^2 + c^2$"],
               "correcta": "B",
               "pista_md": "En la elipse $a$ es el semieje mayor.",
               "explicacion_md": "$c^2 = a^2 - b^2$, donde $a$ es el semieje mayor y $b$ el menor. La opción A corresponde a la hipérbola."},
              {"enunciado_md": "La excentricidad de una elipse satisface:",
               "opciones_md": ["$e < 0$", "$e = 0$", "$0 \\leq e < 1$", "$e > 1$"],
               "correcta": "C",
               "pista_md": "$e = c/a$ y en la elipse $c < a$.",
               "explicacion_md": "$e = c/a$ con $0 \\leq c < a$, por lo tanto $0 \\leq e < 1$. Cuando $e = 0$ la elipse degenera en circunferencia; $e = 1$ daría parábola; $e > 1$ daría hipérbola."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir $a$ y $b.$** $a$ es siempre el semieje **mayor** y $a^2$ va bajo la variable cuyo eje contiene a los focos.",
              "**Aplicar $c^2 = a^2 + b^2$ (de la hipérbola).** En la elipse la relación es $\\boxed{c^2 = a^2 - b^2}.$",
              "**Olvidar que $0 < e < 1$ en la elipse.** Si $e \\ge 1$, ya no es una elipse.",
              "**No identificar la orientación del eje mayor.** Hay que comparar los denominadores: el mayor está bajo la variable del eje mayor.",
              "**Saltarse la división final** después de completar cuadrados; sin dividir por la constante para obtener $1$ del lado derecho, no es la forma canónica.",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición:** $d(P, F_1) + d(P, F_2) = 2a$, con $2a > d(F_1, F_2).$",
              "**Relación clave:** $c^2 = a^2 - b^2$ (equivalentemente, $a^2 = b^2 + c^2$).",
              "**Canónica con centro en el origen:** $\\tfrac{x^2}{a^2} + \\tfrac{y^2}{b^2} = 1$ (eje mayor en el eje con denominador $a^2$).",
              "**Canónica con centro en $(h, k)$:** se reemplaza $x \\to x - h$, $y \\to y - k.$",
              "**Excentricidad:** $e = c/a \\in (0, 1).$ Mide cuán alargada es la elipse.",
              "**Lados rectos:** longitud $\\dfrac{2b^2}{a}.$",
              "**Ecuación general:** $A x^2 + C y^2 + D x + E y + F = 0$ con $AC > 0$, $A \\ne C.$ Reducir a canónica completando cuadrados.",
              "Próxima lección: la **hipérbola**, donde la diferencia (no la suma) de distancias a dos focos es constante.",
          ]),
    ]
    return {"id": "lec-ia-5-4-elipses", "title": "Elipses",
            "description": "Definición como suma de distancias a dos focos, elementos (focos, vértices, ejes, lados rectos, excentricidad), ecuación canónica con centro en el origen y desplazado, y ecuación general.",
            "blocks": blocks, "duration_minutes": 70, "order": 4}


# ============================================================================
# 5.5 Hipérbolas
# ============================================================================
def lesson_5_5():
    blocks = [
        b("texto", body_md=(
            "La **hipérbola** es una de las cónicas más ricas en propiedades geométricas y algebraicas. "
            "A diferencia de la elipse, donde la suma de distancias a los focos es constante, en la "
            "hipérbola lo que permanece fijo es la **diferencia** de dichas distancias. Esta característica "
            "le otorga su forma característica de **dos ramas simétricas** que se abren en sentidos opuestos, "
            "aproximándose indefinidamente a dos rectas llamadas **asíntotas**. Las hipérbolas aparecen en "
            "física, astronomía, arquitectura y en el estudio de secciones cónicas en general.\n\n"
            "**En esta lección estudiaremos:**\n\n"
            "- La **definición geométrica** de la hipérbola y sus elementos: focos, vértices, eje focal, centro y asíntotas.\n"
            "- Las **ecuaciones canónicas** con centro en el origen, según el eje transverso sea horizontal o vertical.\n"
            "- Las **asíntotas** y la **caja central** como herramientas auxiliares para graficar.\n"
            "- La hipérbola **equilátera** y la hipérbola con centro trasladado en $(h, k).$\n"
            "- La **ecuación general** y su reducción a forma canónica."
        )),

        b("definicion",
          titulo="Hipérbola: definición geométrica",
          body_md=(
              "La **hipérbola** es el lugar geométrico de todos aquellos puntos del plano tal que la "
              "**diferencia** de sus distancias a dos puntos fijos del plano es constante y **menor** "
              "que la distancia entre dichos puntos. Los puntos fijos $F_1$ y $F_2$ se llaman **focos** "
              "de la hipérbola.\n\n"
              "Formalmente, un punto $P$ pertenece a la hipérbola si y solo si\n\n"
              "$$\\boxed{\\,|d(P, F_1) - d(P, F_2)| = 2 a\\,},$$\n\n"
              "donde $2a$ es la constante de la diferencia y $2a < d(F_1, F_2) = 2c$, es decir, $a < c.$\n\n"
              "**Comparación con la elipse.** En la elipse se exige $a > c$; en la hipérbola siempre se "
              "tiene $c > a > 0$, lo que determina la existencia de **dos ramas separadas**. El valor "
              "$b$ se define mediante la relación\n\n"
              "$$\\boxed{\\,b^2 = c^2 - a^2\\,},$$\n\n"
              "la cual garantiza $b > 0$ y juega un papel clave en la determinación de las **asíntotas**."
          )),

        fig("Plano cartesiano con dos focos F1 y F2 sobre el eje X y una hipérbola con dos ramas: una a la izquierda de F2 y otra a la derecha de F1. "
            "Marcar también los vértices V1, V2 sobre el eje X y dos asíntotas diagonales que se cruzan en el origen. " + STYLE),

        b("teorema",
          enunciado_md=(
              "**Ecuaciones canónicas de la hipérbola con centro en el origen.**\n\n"
              "**Caso 1 — Eje transverso horizontal.** La gráfica de la ecuación\n\n"
              "$$\\boxed{\\,\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1\\,}, \\qquad c^2 = a^2 + b^2,$$\n\n"
              "es una hipérbola con centro en el origen y las siguientes propiedades:\n\n"
              "- **Vértices:** $(\\pm a, 0).$\n"
              "- **Eje transverso:** horizontal, de longitud $2a.$\n"
              "- **Focos:** $(\\pm c, 0).$\n"
              "- **Asíntotas:** $y = \\pm\\, \\dfrac{b}{a}\\, x.$\n\n"
              "Las dos ramas se abren hacia la izquierda y hacia la derecha; la curva nunca cruza el eje $y.$\n\n"
              "**Caso 2 — Eje transverso vertical.** La gráfica de la ecuación\n\n"
              "$$\\boxed{\\,\\frac{y^2}{a^2} - \\frac{x^2}{b^2} = 1\\,}, \\qquad c^2 = a^2 + b^2,$$\n\n"
              "es una hipérbola con centro en el origen y propiedades:\n\n"
              "- **Vértices:** $(0, \\pm a).$\n"
              "- **Eje transverso:** vertical, de longitud $2a.$\n"
              "- **Focos:** $(0, \\pm c).$\n"
              "- **Asíntotas:** $y = \\pm\\, \\dfrac{a}{b}\\, x.$\n\n"
              "Las ramas se abren hacia arriba y hacia abajo; la curva nunca cruza el eje $x.$"
          )),

        b("definicion",
          titulo="Elementos de la hipérbola",
          body_md=(
              "Los principales elementos de una hipérbola son:\n\n"
              "1. **Eje focal:** recta que pasa por los dos focos $F_1$ y $F_2.$ Puede ser horizontal o vertical.\n"
              "2. **Centro:** punto medio del segmento $\\overline{F_1 F_2}.$ En posición estándar, coincide con el origen.\n"
              "3. **Vértices:** intersecciones del eje focal con la hipérbola, denotadas $V_1, V_2.$ La distancia del centro a cada vértice es $a$, llamada **semieje transverso**.\n"
              "4. **Eje transverso:** segmento $\\overline{V_1 V_2}$, de longitud $2a$, que coincide con el eje focal.\n"
              "5. **Eje conjugado:** segmento perpendicular al eje transverso por el centro, de longitud $2b$, donde $b^2 = c^2 - a^2.$ Este eje **no interseca** la hipérbola.\n"
              "6. **Focos:** puntos fijos $F_1$ y $F_2$ de la definición. La distancia del centro a cada foco es $c$, llamada **semidistancia focal**.\n"
              "7. **Asíntotas:** rectas a las que la hipérbola se aproxima para valores grandes de $|x|$ o $|y|$, sin llegar a intersecarlas.\n\n"
              "**Caja central.** Rectángulo formado por los puntos $(\\pm a, 0)$ y $(0, \\pm b)$ (caso horizontal). "
              "Sus diagonales prolongadas son precisamente las asíntotas de la hipérbola."
          )),

        b("teorema",
          enunciado_md=(
              "**Deducción de las asíntotas (eje horizontal).** Despejando $y$ de la canónica:\n\n"
              "$$\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1 \\;\\Longrightarrow\\; y^2 = b^2\\left(\\frac{x^2}{a^2} - 1\\right) "
              "\\;\\Longrightarrow\\; y = \\pm \\frac{b}{a}\\sqrt{x^2 - a^2}.$$\n\n"
              "Factorizando $x$ dentro de la raíz: $y = \\pm\\, \\dfrac{b}{a}\\, x \\sqrt{1 - \\tfrac{a^2}{x^2}}.$\n\n"
              "Cuando $|x| \\to \\infty$, $\\dfrac{a^2}{x^2} \\to 0$, así $\\sqrt{1 - \\tfrac{a^2}{x^2}} \\to 1.$ "
              "En consecuencia $y \\to \\pm\\dfrac{b}{a}\\, x$, que son las ecuaciones de las **asíntotas**.\n\n"
              "**Caja central como guía gráfica.** Para trazar la hipérbola con eje horizontal:\n\n"
              "1. Localizar los cuatro puntos $(a, 0), (-a, 0), (0, b), (0, -b).$\n"
              "2. Trazar el rectángulo de lados $2a$ y $2b$ que pasa por esos puntos.\n"
              "3. Prolongar las diagonales del rectángulo: son las asíntotas $y = \\pm \\tfrac{b}{a}\\, x.$\n"
              "4. Trazar las dos ramas partiendo de los vértices $(\\pm a, 0)$ y abriéndose hacia las asíntotas."
          )),

        b("definicion",
          titulo="Hipérbola equilátera",
          body_md=(
              "Cuando las asíntotas de una hipérbola son **perpendiculares entre sí**, la hipérbola se "
              "llama **equilátera**. Esto ocurre cuando las pendientes de las asíntotas son recíprocas con "
              "signo opuesto, es decir, cuando $\\dfrac{b}{a} \\cdot \\dfrac{b}{a} = 1$, lo que equivale a $b = a.$\n\n"
              "En ese caso la ecuación toma la forma simplificada\n\n"
              "$$x^2 - y^2 = a^2 \\quad \\text{(eje horizontal)} \\quad \\text{o} \\quad y^2 - x^2 = a^2 \\quad \\text{(eje vertical).}$$"
          )),

        b("ejemplo_resuelto",
          titulo="Hipérbola horizontal: lectura completa",
          problema_md="Una hipérbola tiene la ecuación $9 x^2 - 16 y^2 = 144.$ Traza la gráfica encontrando los vértices, focos y asíntotas.",
          pasos=[
              paso("Dividimos por $144$ para llevar a forma canónica:\n\n"
                   "$\\dfrac{9 x^2}{144} - \\dfrac{16 y^2}{144} = 1 \\;\\Longrightarrow\\; \\dfrac{x^2}{16} - \\dfrac{y^2}{9} = 1.$"),
              paso("$a^2 = 16$ y $b^2 = 9$, así $a = 4$ y $b = 3.$ Como el término positivo corresponde a $x^2$, "
                   "el eje transverso es **horizontal**."),
              paso("$c^2 = a^2 + b^2 = 16 + 9 = 25$, así $c = 5.$"),
              paso("**Vértices:** $(\\pm 4, 0).$ **Focos:** $(\\pm 5, 0).$ **Asíntotas:** $y = \\pm \\dfrac{3}{4} x.$ "
                   "Para graficar: caja central con vértices en $(\\pm 4, 0)$ y $(0, \\pm 3)$, prolongar las diagonales y dibujar las ramas.",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Producto de distancias a las asíntotas",
          problema_md=("Demuestra que el producto de las distancias de un punto $P$ de la hipérbola "
                       "$\\dfrac{x^2}{a^2} - \\dfrac{y^2}{b^2} = 1$ a cada una de sus asíntotas es **constante**."),
          pasos=[
              paso("Las asíntotas son $y = \\pm \\dfrac{b}{a} x$, que escribimos en forma general:\n\n"
                   "$L_1: bx - ay = 0,$ $L_2: bx + ay = 0.$"),
              paso("Sea $P(x_0, y_0)$ un punto de la hipérbola, así $\\dfrac{x_0^2}{a^2} - \\dfrac{y_0^2}{b^2} = 1.$ "
                   "Distancias a cada asíntota:\n\n"
                   "$d_1 = \\dfrac{|b x_0 - a y_0|}{\\sqrt{b^2 + a^2}} = \\dfrac{|b x_0 - a y_0|}{c}, \\quad "
                   "d_2 = \\dfrac{|b x_0 + a y_0|}{c}.$"),
              paso("Producto:\n\n"
                   "$d_1 \\cdot d_2 = \\dfrac{|b x_0 - a y_0| \\cdot |b x_0 + a y_0|}{c^2} = \\dfrac{|b^2 x_0^2 - a^2 y_0^2|}{c^2}.$"),
              paso("Como $P$ está sobre la hipérbola, $b^2 x_0^2 - a^2 y_0^2 = a^2 b^2 \\left(\\dfrac{x_0^2}{a^2} - \\dfrac{y_0^2}{b^2}\\right) = a^2 b^2.$ Luego\n\n"
                   "$d_1 \\cdot d_2 = \\dfrac{a^2 b^2}{c^2} = \\dfrac{a^2 b^2}{a^2 + b^2}.$"),
              paso("Esta expresión depende solo de $a$ y $b$, no de $P.$ Por lo tanto, el producto es **constante**. ∎",
                   "Conclusión.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Hipérbola con centro trasladado en $(h, k).$**\n\n"
              "**Eje transverso horizontal:**\n\n"
              "$$\\boxed{\\,\\frac{(x - h)^2}{a^2} - \\frac{(y - k)^2}{b^2} = 1\\,}, \\qquad b^2 = c^2 - a^2.$$\n\n"
              "Vértices: $(h \\pm a, k).$ Focos: $(h \\pm c, k).$ Asíntotas: $y - k = \\pm \\dfrac{b}{a} (x - h).$\n\n"
              "**Eje transverso vertical:**\n\n"
              "$$\\boxed{\\,\\frac{(y - k)^2}{a^2} - \\frac{(x - h)^2}{b^2} = 1\\,}, \\qquad b^2 = c^2 - a^2.$$\n\n"
              "Vértices: $(h, k \\pm a).$ Focos: $(h, k \\pm c).$ Asíntotas: $y - k = \\pm \\dfrac{a}{b}(x - h).$\n\n"
              "**Diferencia clave con la elipse.** En la hipérbola se cumple **$b^2 = c^2 - a^2$** (con $c > a$), "
              "mientras que en la elipse $b^2 = a^2 - c^2$ (con $a > c$). Este cambio de signo es uno de los "
              "puntos donde más errores se cometen."
          )),

        b("teorema",
          enunciado_md=(
              "**Ecuación general de la hipérbola.** La ecuación general de una hipérbola es\n\n"
              "$$A x^2 + C y^2 + D x + E y + F = 0, \\quad \\text{con } A C < 0,$$\n\n"
              "cuya gráfica es una hipérbola o bien dos rectas que se cortan (caso degenerado). La condición "
              "$AC < 0$ indica que los coeficientes de $x^2$ e $y^2$ tienen **signos opuestos**, lo que "
              "distingue a la hipérbola de la elipse ($AC > 0$) y de la parábola (uno de los cuadrados ausente).\n\n"
              "Para reducir la ecuación general a su forma canónica se utiliza la técnica de **completación "
              "de cuadrados** en $x$ e $y$ por separado."
          )),

        b("ejemplo_resuelto",
          titulo="Hipérbola desde vértices y focos",
          problema_md="Encuentra la ecuación cuya gráfica sea una hipérbola con vértices en $(\\pm 2, 0)$ y focos en $(\\pm 4, 0).$",
          pasos=[
              paso("Los vértices y focos están sobre el eje $X$, así que el eje transverso es **horizontal** "
                   "y el centro está en el origen."),
              paso("$a = 2$ (distancia centro-vértice), $c = 4$ (distancia centro-foco)."),
              paso("$b^2 = c^2 - a^2 = 16 - 4 = 12.$"),
              paso("Ecuación: $\\boxed{\\dfrac{x^2}{4} - \\dfrac{y^2}{12} = 1}.$ "
                   "Asíntotas: $y = \\pm \\dfrac{\\sqrt{12}}{2} x = \\pm\\sqrt{3}\\, x.$",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Hipérbola desde forma general (centro trasladado)",
          problema_md="Determina la gráfica de $5 x^2 - 4 y^2 - 20 x - 24 y - 36 = 0.$",
          pasos=[
              paso("Coeficientes de signos opuestos ($5 > 0$, $-4 < 0$), así que se trata de una hipérbola "
                   "(o caso degenerado). Reorganizamos:\n\n"
                   "$5 x^2 - 20 x - 4 y^2 - 24 y = 36.$"),
              paso("Completamos cuadrado en $x$: $5(x^2 - 4 x) = 5\\left[(x - 2)^2 - 4\\right] = 5(x - 2)^2 - 20.$"),
              paso("Completamos cuadrado en $y$: $-4(y^2 + 6 y) = -4\\left[(y + 3)^2 - 9\\right] = -4(y + 3)^2 + 36.$"),
              paso("Sustituyendo: $5(x - 2)^2 - 20 - 4(y + 3)^2 + 36 = 36$, es decir, "
                   "$5(x - 2)^2 - 4(y + 3)^2 = 20.$"),
              paso("Dividiendo por $20$: $\\dfrac{(x - 2)^2}{4} - \\dfrac{(y + 3)^2}{5} = 1.$ "
                   "Es una hipérbola con eje transverso **horizontal**, centro $(2, -3)$, $a = 2$, $b = \\sqrt 5$, "
                   "$c = \\sqrt{a^2 + b^2} = 3.$"),
              paso("**Vértices:** $(2 \\pm 2, -3)$, es decir, $(4, -3)$ y $(0, -3).$ "
                   "**Focos:** $(2 \\pm 3, -3)$, es decir, $(5, -3)$ y $(-1, -3).$ "
                   "**Asíntotas:** $y + 3 = \\pm \\dfrac{\\sqrt 5}{2}(x - 2).$",
                   "Resultado.", resultado=True),
          ]),

        ej(
            "Hipérbola con eje vertical",
            "Encuentra los vértices, focos y asíntotas de $\\dfrac{y^2}{9} - \\dfrac{x^2}{16} = 1.$",
            ["Eje transverso vertical porque $y^2$ tiene signo positivo.",
             "$a^2 = 9$, $b^2 = 16$, $c^2 = a^2 + b^2.$",
             "Asíntotas $y = \\pm (a/b) x.$"],
            ("$a = 3$, $b = 4$, $c = 5.$ "
             "Vértices: $(0, \\pm 3).$ Focos: $(0, \\pm 5).$ Asíntotas: $y = \\pm \\dfrac{3}{4} x.$")
        ),

        ej(
            "Hipérbola equilátera",
            "Encuentra la ecuación de la hipérbola equilátera con centro en el origen, eje transverso sobre el eje $X$ y que pasa por $(3, 1).$",
            ["Equilátera $\\Rightarrow b = a$, así $x^2 - y^2 = a^2.$",
             "Sustituye $(3, 1)$ para hallar $a^2.$"],
            ("$3^2 - 1^2 = a^2 \\Rightarrow a^2 = 8.$ Ecuación: $x^2 - y^2 = 8.$")
        ),

        ej(
            "Hipérbola desde forma general (centro trasladado)",
            "Lleva $9 x^2 - 4 y^2 - 36 x + 8 y - 4 = 0$ a forma canónica e identifica el centro.",
            ["Agrupa por variable y completa cuadrados.",
             "Divide por la constante para obtener $1$ del lado derecho."],
            ("$9(x - 2)^2 - 4(y - 1)^2 = 4 + 36 - 4 = 36$, es decir, "
             "$\\dfrac{(x - 2)^2}{4} - \\dfrac{(y - 1)^2}{9} = 1.$ Centro: $(2, 1).$ "
             "Eje transverso horizontal, $a = 2$, $b = 3$, $c = \\sqrt{13}.$")
        ),

        ej(
            "Distinguir cónicas por sus signos",
            "Indica qué tipo de cónica representa cada ecuación, sin completar cuadrados:\n\n"
            "(a) $4x^2 + 9y^2 - 16x + 18y - 11 = 0.$\n\n"
            "(b) $4x^2 - 9y^2 - 16x + 18y - 11 = 0.$\n\n"
            "(c) $4x^2 - 16x + 18y + 11 = 0.$",
            ["Compara los signos de $A$ y $C$ (coeficientes de $x^2$ y $y^2$).",
             "$AC > 0$: elipse. $AC < 0$: hipérbola. $A = 0$ o $C = 0$: parábola."],
            ("(a) $A = 4 > 0$, $C = 9 > 0$, $AC > 0$: **elipse**. "
             "(b) $A = 4 > 0$, $C = -9 < 0$, $AC < 0$: **hipérbola**. "
             "(c) $C = 0$ y $A \\ne 0$: **parábola**.")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "Para la hipérbola $\\dfrac{x^2}{9} - \\dfrac{y^2}{16} = 1$, ¿cuáles son las asíntotas?",
               "opciones_md": ["$y = \\pm \\dfrac{3}{4}x$", "$y = \\pm \\dfrac{4}{3}x$", "$y = \\pm \\dfrac{16}{9}x$", "$y = \\pm 5x$"],
               "correcta": "B",
               "pista_md": "Para hipérbola horizontal $\\tfrac{x^2}{a^2} - \\tfrac{y^2}{b^2} = 1$ las asíntotas son $y = \\pm \\tfrac{b}{a}x$.",
               "explicacion_md": "$a = 3$, $b = 4$, asíntotas $y = \\pm \\dfrac{b}{a}x = \\pm \\dfrac{4}{3}x$."},
              {"enunciado_md": "¿Cuál es la relación entre $a$, $b$ y $c$ en la hipérbola?",
               "opciones_md": ["$c^2 = a^2 + b^2$", "$c^2 = a^2 - b^2$", "$b^2 = a^2 + c^2$", "$a^2 = b^2 + c^2$"],
               "correcta": "A",
               "pista_md": "En la hipérbola $c$ es el mayor de los tres.",
               "explicacion_md": "Hipérbola: $c^2 = a^2 + b^2$. Es la diferencia clave con la elipse, donde $c^2 = a^2 - b^2$. La excentricidad cumple $e = c/a > 1$."},
              {"enunciado_md": "En $4x^2 - 9y^2 + \\ldots = 0$, ¿qué tipo de cónica es (no degenerada)?",
               "opciones_md": ["Elipse", "Parábola", "Hipérbola", "Circunferencia"],
               "correcta": "C",
               "pista_md": "El producto de los coeficientes de $x^2$ e $y^2$ es negativo.",
               "explicacion_md": "$AC = 4 \\cdot (-9) < 0$, por lo que es una **hipérbola**. Si $AC > 0$ sería elipse (o circunferencia si $A=C$), si uno es cero, parábola."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir $b^2 = c^2 - a^2$ (hipérbola) con $b^2 = a^2 - c^2$ (elipse).** Es la fuente de error más común al pasar de una cónica a otra.",
              "**Asumir que $a > b$ siempre.** En la hipérbola, $a$ y $b$ no tienen relación de orden fija; lo que sí se cumple es $c > a > 0.$",
              "**Determinar el eje por el tamaño de los denominadores.** En la hipérbola, el eje transverso es el que tiene **signo positivo** en la canónica, no el de mayor denominador.",
              "**Confundir las asíntotas: $b/a$ vs $a/b.$** Para la hipérbola horizontal $\\tfrac{x^2}{a^2} - \\tfrac{y^2}{b^2} = 1$, las asíntotas son $y = \\pm \\tfrac{b}{a} x.$ Para la vertical, $y = \\pm \\tfrac{a}{b} x.$",
              "**Olvidar que las asíntotas pasan por el centro.** En el caso trasladado, las asíntotas son $y - k = \\pm \\tfrac{b}{a}(x - h).$",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición:** $|d(P, F_1) - d(P, F_2)| = 2a$, con $2a < 2c.$",
              "**Relación clave:** $c^2 = a^2 + b^2$ (con $c > a$), opuesta a la elipse.",
              "**Canónica con centro en el origen:** $\\tfrac{x^2}{a^2} - \\tfrac{y^2}{b^2} = 1$ (eje horizontal) y $\\tfrac{y^2}{a^2} - \\tfrac{x^2}{b^2} = 1$ (eje vertical).",
              "**Asíntotas:** $y = \\pm \\tfrac{b}{a} x$ (horizontal) y $y = \\pm \\tfrac{a}{b} x$ (vertical).",
              "**Caja central:** rectángulo de lados $2a$ y $2b$ con vértices auxiliares en $(\\pm a, 0)$ y $(0, \\pm b)$; sus diagonales son las asíntotas.",
              "**Hipérbola equilátera:** $a = b$, asíntotas perpendiculares; ecuación simplificada $x^2 - y^2 = a^2.$",
              "**Centro trasladado:** $\\tfrac{(x-h)^2}{a^2} - \\tfrac{(y-k)^2}{b^2} = 1$, con asíntotas $y - k = \\pm \\tfrac{b}{a}(x - h).$",
              "**Ecuación general:** $A x^2 + C y^2 + D x + E y + F = 0$ con $AC < 0.$",
              "Próxima lección: **rotación de ejes** para tratar ecuaciones con término cruzado $Bxy.$",
          ]),
    ]
    return {"id": "lec-ia-5-5-hiperbolas", "title": "Hipérbolas",
            "description": "Definición como diferencia de distancias a dos focos, ecuaciones canónicas con eje transverso horizontal y vertical, asíntotas y caja central, hipérbola equilátera, hipérbola con centro trasladado y ecuación general.",
            "blocks": blocks, "duration_minutes": 70, "order": 5}


# ============================================================================
# 5.6 Rotación de Ejes
# ============================================================================
def lesson_5_6():
    blocks = [
        b("texto", body_md=(
            "La **rotación de ejes** es una herramienta fundamental del álgebra y la geometría analítica "
            "que permite simplificar la **ecuación general de segundo grado** eliminando el **término "
            "cruzado** $Bxy.$ Cuando una cónica aparece \"inclinada\" respecto a los ejes coordenados, "
            "su ecuación contiene dicho término mixto, lo que dificulta identificar su naturaleza y "
            "graficarla. Mediante una rotación apropiada del sistema de coordenadas, es posible obtener "
            "una ecuación en forma canónica que revela directamente si la curva es una elipse, una "
            "parábola o una hipérbola.\n\n"
            "**En esta lección estudiaremos:**\n\n"
            "- La **ecuación general de segundo grado** y el rol del término cruzado $Bxy$ en la identificación de cónicas.\n"
            "- La deducción y aplicación de las **fórmulas de rotación de ejes** para transformar coordenadas bajo un ángulo $\\phi.$\n"
            "- Cómo determinar el **ángulo de rotación** que elimina el término $Bxy$ y escribir la ecuación en forma canónica.\n"
            "- La identificación de la naturaleza de una cónica usando el **discriminante** $\\delta = B^2 - 4AC.$"
        )),

        b("definicion",
          titulo="Ecuación general de segundo grado",
          body_md=(
              "La **ecuación general de segundo grado**, también llamada **ecuación cuadrática**, en "
              "las variables $x$ e $y$ se escribe en la forma\n\n"
              "$$\\boxed{\\,A x^2 + B x y + C y^2 + D x + E y + F = 0\\,},$$\n\n"
              "donde $A, B, C, D, E$ y $F$ son constantes reales. Para que la ecuación sea efectivamente "
              "de segundo grado se requiere que **al menos una** de las constantes $A, B$ o $C$ sea distinta "
              "de cero. Además se supone que no todos los coeficientes que involucran a una misma variable "
              "son simultáneamente cero.\n\n"
              "El término $B x y$ se denomina **término cruzado** o **término mixto**. Cuando $B \\ne 0$, "
              "los ejes de la cónica que representa la ecuación **no son paralelos** a los ejes coordenados "
              "$x$ e $y$, sino que aparecen **rotados** respecto de ellos. Esto dificulta el análisis directo "
              "de la curva. La técnica de **rotación de ejes** busca encontrar un nuevo sistema de coordenadas "
              "$XY$ en el que dicho término desaparezca."
          )),

        b("teorema",
          enunciado_md=(
              "**Fórmulas de rotación de ejes (deducción geométrica).** Supongamos que los ejes $x$ e $y$ "
              "se giran un ángulo agudo $\\phi$ alrededor del origen, produciendo un nuevo par de ejes "
              "$X$ e $Y.$ Un punto $P$ del plano tiene coordenadas $(x, y)$ en el sistema original y "
              "coordenadas $(X, Y)$ en el sistema rotado.\n\n"
              "Si $r$ denota la distancia del punto $P$ al origen y $\\theta$ es el ángulo que forma el "
              "segmento $\\overline{OP}$ con el eje $X$ (en el sistema rotado), entonces:\n\n"
              "$$X = r \\cos(\\theta), \\qquad Y = r \\sin(\\theta),$$\n\n"
              "y respecto a los ejes originales el mismo segmento forma un ángulo $\\theta + \\phi$ con el eje $x$, así:\n\n"
              "$$x = r \\cos(\\theta + \\phi), \\qquad y = r \\sin(\\theta + \\phi).$$\n\n"
              "Aplicando la **fórmula de adición** del coseno y del seno se obtiene\n\n"
              "$$x = r\\cos(\\theta + \\phi) = X \\cos\\phi - Y \\sin\\phi,$$\n\n"
              "$$y = r\\sin(\\theta + \\phi) = X \\sin\\phi + Y \\cos\\phi.$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema de rotación de ejes.** Si el punto $P$ tiene coordenadas $(x, y)$ respecto a "
              "los ejes rectangulares $xy$ y los ejes coordenados se giran un ángulo $\\phi$ en torno al "
              "origen, siendo $(X, Y)$ las coordenadas del punto $P$ con respecto a los nuevos ejes "
              "rectangulares $XY$, entonces las **ecuaciones de rotación** del sistema original al "
              "nuevo sistema de coordenadas son\n\n"
              "$$\\boxed{\\,x = X \\cos\\phi - Y \\sin\\phi, \\qquad y = X \\sin\\phi + Y \\cos\\phi.\\,}$$\n\n"
              "Estas relaciones permiten sustituir $x$ e $y$ en la ecuación general de segundo grado para "
              "obtener su expresión en el sistema rotado $XY$, sin término cruzado, siempre que $\\phi$ "
              "sea elegido adecuadamente."
          )),

        fig("Plano cartesiano original con ejes x e y. Sobre el mismo origen, otro par de ejes X e Y rotados un ángulo phi en sentido antihorario. "
            "Un punto P en el primer cuadrante con segmento OP, y el ángulo theta marcado entre OP y el eje X rotado, y el ángulo phi marcado entre el eje x y el eje X. " + STYLE),

        b("ejemplo_resuelto",
          titulo="Demostrar que xy = 2 es una hipérbola",
          problema_md="Gira los ejes coordenados un ángulo de $45°$ para demostrar que la gráfica de la ecuación $x y = 2$ es una hipérbola.",
          pasos=[
              paso("Usamos las fórmulas de rotación con $\\phi = 45°$, recordando que "
                   "$\\cos 45° = \\sin 45° = \\dfrac{1}{\\sqrt 2}$:\n\n"
                   "$x = \\dfrac{X}{\\sqrt 2} - \\dfrac{Y}{\\sqrt 2}, \\quad y = \\dfrac{X}{\\sqrt 2} + \\dfrac{Y}{\\sqrt 2}.$"),
              paso("Sustituyendo en $xy = 2$:\n\n"
                   "$\\left(\\dfrac{X}{\\sqrt 2} - \\dfrac{Y}{\\sqrt 2}\\right) \\left(\\dfrac{X}{\\sqrt 2} + \\dfrac{Y}{\\sqrt 2}\\right) = 2.$"),
              paso("Reconociendo el producto suma por diferencia $(a - b)(a + b) = a^2 - b^2$:\n\n"
                   "$\\dfrac{X^2}{2} - \\dfrac{Y^2}{2} = 2 \\;\\Longleftrightarrow\\; \\dfrac{X^2}{4} - \\dfrac{Y^2}{4} = 1.$"),
              paso("Esta es la forma canónica de una **hipérbola equilátera** con semieje real $a = 2$ y "
                   "semieje imaginario $b = 2$, cuyos ejes coinciden con los ejes rotados $X$ e $Y.$ "
                   "Queda así demostrado que $xy = 2$ es una hipérbola, rotada $45°$ respecto a los ejes coordenados originales.",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Elección del ángulo de rotación que elimina $Bxy.$** Para eliminar el término $B x y$ "
              "en la ecuación general de cónicas\n\n"
              "$$A x^2 + B x y + C y^2 + D x + E y + F = 0,$$\n\n"
              "se debe girar los ejes el **ángulo agudo** $\\phi$ que satisface\n\n"
              "$$\\boxed{\\;\\begin{cases}\\tan(2\\phi) = \\dfrac{B}{A - C} & \\text{si } A \\ne C, \\\\[4pt]"
              "\\phi = \\dfrac{\\pi}{4} & \\text{si } A = C. \\end{cases}\\;}$$\n\n"
              "**Justificación.** Al sustituir las fórmulas de rotación en la ecuación general y agrupar "
              "los términos del mismo tipo, el coeficiente del término $XY$ en el nuevo sistema se anula "
              "si y solo si $\\phi$ satisface la relación anterior. Eligiendo $\\phi$ como **ángulo agudo** "
              "($0 < \\phi < \\pi/2$), $2\\phi \\in (0, \\pi)$ y la relación con $\\tan(2\\phi)$ tiene sentido "
              "(con la convención $\\tan(\\pi/2) = \\infty$ correspondiendo al caso $A = C$, donde "
              "$A - C = 0$ y $\\phi = \\pi/4$).\n\n"
              "**Cálculo de $\\sin\\phi$ y $\\cos\\phi$ a partir de $\\tan(2\\phi).$** Una vez determinado "
              "$\\tan(2\\phi)$, se calcula $\\cos(2\\phi)$ usando la identidad pitagórica\n\n"
              "$$\\cos^2(2\\phi) = \\dfrac{1}{1 + \\tan^2(2\\phi)},$$\n\n"
              "tomando la raíz positiva (ya que $\\phi$ es agudo y por tanto $2\\phi \\in (0, \\pi)$). "
              "Luego $\\sin\\phi$ y $\\cos\\phi$ se obtienen mediante las **identidades del ángulo medio**:\n\n"
              "$$\\sin\\phi = \\sqrt{\\dfrac{1 - \\cos(2\\phi)}{2}}, \\qquad \\cos\\phi = \\sqrt{\\dfrac{1 + \\cos(2\\phi)}{2}}.$$"
          )),

        b("ejemplo_resuelto",
          titulo="Identificar cónica con término cruzado",
          problema_md=("Usa una rotación de ejes para eliminar el término $xy$ en la ecuación\n\n"
                       "$64 x^2 + 96 xy + 36 y^2 - 15 x + 20 y - 25 = 0,$\n\n"
                       "e identifica su gráfica."),
          pasos=[
              paso("Identificamos $A = 64$, $B = 96$, $C = 36.$ Como $A \\ne C$, el ángulo de rotación satisface\n\n"
                   "$\\tan(2\\phi) = \\dfrac{B}{A - C} = \\dfrac{96}{64 - 36} = \\dfrac{96}{28} = \\dfrac{24}{7}.$"),
              paso("Calculamos $\\cos(2\\phi)$ con un triángulo rectángulo de catetos $7$ y $24$ e hipotenusa "
                   "$\\sqrt{49 + 576} = \\sqrt{625} = 25$:\n\n"
                   "$\\cos(2\\phi) = \\dfrac{7}{25}.$"),
              paso("Aplicando las identidades del ángulo medio:\n\n"
                   "$\\sin\\phi = \\sqrt{\\dfrac{1 - 7/25}{2}} = \\sqrt{\\dfrac{18/25}{2}} = \\sqrt{\\dfrac{9}{25}} = \\dfrac{3}{5}, "
                   "\\quad \\cos\\phi = \\sqrt{\\dfrac{1 + 7/25}{2}} = \\sqrt{\\dfrac{32/25}{2}} = \\dfrac{4}{5}.$"),
              paso("Las fórmulas de rotación son entonces $x = \\dfrac{4 X - 3 Y}{5}$, $y = \\dfrac{3 X + 4 Y}{5}.$"),
              paso("Al sustituir en la ecuación original (cálculos algebraicos extensos), el término $XY$ "
                   "se cancela por construcción y se obtiene una ecuación en $X$ e $Y$ sin término cruzado. "
                   "Verificación rápida con el discriminante:\n\n"
                   "$\\delta = B^2 - 4 A C = 96^2 - 4 \\cdot 64 \\cdot 36 = 9216 - 9216 = 0.$ "
                   "Como $\\delta = 0$, la cónica es una **parábola**.",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Identificación de cónicas por el discriminante.** La cantidad\n\n"
              "$$\\delta = B^2 - 4 A C$$\n\n"
              "es un **invariante** bajo rotaciones de ejes, es decir, su valor no cambia al efectuar el "
              "cambio de coordenadas. Esto permite identificar la naturaleza de la cónica directamente "
              "a partir de los coeficientes de la ecuación original, sin necesidad de efectuar la rotación.\n\n"
              "**Teorema (clasificación).** La gráfica de la ecuación general $A x^2 + B x y + C y^2 + D x + E y + F = 0$ "
              "es una cónica o una cónica degenerada. En los casos **no degenerados**, la gráfica es:\n\n"
              "1. una **elipse** (o circunferencia) si $B^2 - 4AC < 0$,\n"
              "2. una **parábola** si $B^2 - 4 A C = 0$,\n"
              "3. una **hipérbola** si $B^2 - 4 A C > 0.$\n\n"
              "El término $\\delta = B^2 - 4 A C$ recibe el nombre de **discriminante** de la ecuación. "
              "Los casos degenerados incluyen un **punto**, **dos rectas**, una **recta doble** o el "
              "**conjunto vacío**."
          )),

        b("ejemplo_resuelto",
          titulo="Identificación y reducción a forma canónica",
          problema_md=("Determina la naturaleza de la cónica que representa la ecuación dada y reduce la "
                       "ecuación a su forma canónica por transformación de coordenadas:\n\n"
                       "$$2 x^2 - 12 x y + 18 y^2 + x - 3 y - 6 = 0.$$"),
          pasos=[
              paso("Identificamos los coeficientes: $A = 2$, $B = -12$, $C = 18.$ Calculamos el discriminante:\n\n"
                   "$\\delta = B^2 - 4 A C = (-12)^2 - 4 \\cdot 2 \\cdot 18 = 144 - 144 = 0.$ "
                   "Como $\\delta = 0$, la cónica es una **parábola** (o caso degenerado)."),
              paso("Determinamos el ángulo de rotación. Como $A \\ne C$:\n\n"
                   "$\\tan(2\\phi) = \\dfrac{B}{A - C} = \\dfrac{-12}{2 - 18} = \\dfrac{-12}{-16} = \\dfrac{3}{4}.$"),
              paso("Triángulo rectángulo con catetos $3$ y $4$, hipotenusa $5$, así $\\cos(2\\phi) = \\dfrac{4}{5}.$"),
              paso("Aplicando las identidades del ángulo medio:\n\n"
                   "$\\sin\\phi = \\sqrt{\\dfrac{1 - 4/5}{2}} = \\sqrt{\\dfrac{1}{10}} = \\dfrac{1}{\\sqrt{10}}, \\quad "
                   "\\cos\\phi = \\sqrt{\\dfrac{1 + 4/5}{2}} = \\sqrt{\\dfrac{9}{10}} = \\dfrac{3}{\\sqrt{10}}.$"),
              paso("Las fórmulas de rotación son\n\n"
                   "$x = \\dfrac{3 X - Y}{\\sqrt{10}}, \\qquad y = \\dfrac{X + 3 Y}{\\sqrt{10}}.$"),
              paso("Sustituyendo y simplificando se obtiene una ecuación en $X$ e $Y$ sin término cruzado, "
                   "que corresponde a la forma canónica de una **parábola** (posiblemente degenerada). "
                   "El detalle algebraico se completa con una **traslación** posterior para llevar la ecuación "
                   "a $X'^2 = aY'$ o similar.",
                   "Resultado.", resultado=True),
          ]),

        ej(
            "Discriminante directo",
            "Identifica el tipo de cónica de las siguientes ecuaciones usando el discriminante:\n\n"
            "(a) $3x^2 + 2xy + 3y^2 - 8 = 0.$\n\n"
            "(b) $4x^2 + 4xy + y^2 - 24x + 38y - 139 = 0.$\n\n"
            "(c) $x^2 - 4xy + y^2 + 5 = 0.$",
            ["Calcula $\\delta = B^2 - 4 A C$ en cada caso.",
             "$\\delta < 0$ elipse, $\\delta = 0$ parábola, $\\delta > 0$ hipérbola."],
            ("(a) $\\delta = 4 - 36 = -32 < 0$: **elipse**. "
             "(b) $\\delta = 16 - 16 = 0$: **parábola**. "
             "(c) $\\delta = 16 - 4 = 12 > 0$: **hipérbola**.")
        ),

        ej(
            "Ángulo de rotación cuando A = C",
            "¿Qué ángulo de rotación elimina el término cruzado en $5x^2 + 6xy + 5y^2 - 4 = 0$?",
            ["Compara $A$ y $C.$",
             "Cuando $A = C$, el ángulo es $\\pi/4 = 45°.$"],
            ("$A = C = 5$, así $\\phi = 45°.$")
        ),

        ej(
            "Cálculo de sen y cos del ángulo medio",
            "Sabiendo que $\\tan(2\\phi) = \\dfrac{5}{12}$ con $\\phi$ agudo, calcula $\\sin\\phi$ y $\\cos\\phi.$",
            ["Forma triángulo rectángulo de catetos $5$ y $12.$",
             "Hipotenusa $13$ da $\\cos(2\\phi) = 12/13.$",
             "Aplica $\\sin\\phi = \\sqrt{(1 - \\cos 2\\phi)/2}$ y $\\cos\\phi = \\sqrt{(1 + \\cos 2\\phi)/2}.$"],
            ("$\\cos(2\\phi) = 12/13.$ "
             "$\\sin\\phi = \\sqrt{(1 - 12/13)/2} = \\sqrt{1/26} = 1/\\sqrt{26}.$ "
             "$\\cos\\phi = \\sqrt{(1 + 12/13)/2} = \\sqrt{25/26} = 5/\\sqrt{26}.$")
        ),

        ej(
            "Aplicar fórmulas de rotación",
            "Si $\\phi$ es tal que $\\sin\\phi = 3/5$ y $\\cos\\phi = 4/5$, escribe las fórmulas de rotación.",
            ["$x = X\\cos\\phi - Y\\sin\\phi$, $y = X\\sin\\phi + Y\\cos\\phi.$"],
            ("$x = \\dfrac{4X - 3Y}{5}$, $y = \\dfrac{3X + 4Y}{5}.$")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "Para eliminar el término cruzado $Bxy$ rotando los ejes un ángulo $\\phi$, ¿qué fórmula se usa?",
               "opciones_md": ["$\\tan\\phi = \\dfrac{B}{A - C}$", "$\\cot(2\\phi) = \\dfrac{A - C}{B}$", "$\\tan(2\\phi) = \\dfrac{A - C}{B}$", "$\\sin(2\\phi) = B$"],
               "correcta": "B",
               "pista_md": "El ángulo correcto se obtiene de $2\\phi$, no de $\\phi$ directo.",
               "explicacion_md": "$\\cot(2\\phi) = \\dfrac{A - C}{B}$ (equivalentemente $\\tan(2\\phi) = \\dfrac{B}{A - C}$). Es la condición que anula el coeficiente del término cruzado tras la rotación."},
              {"enunciado_md": "Si $A = C$ en $Ax^2 + Bxy + Cy^2 + \\ldots = 0$ con $B \\neq 0$, ¿qué ángulo de rotación elimina el término cruzado?",
               "opciones_md": ["$\\phi = 0$", "$\\phi = \\pi/6$", "$\\phi = \\pi/4$", "$\\phi = \\pi/2$"],
               "correcta": "C",
               "pista_md": "Cuando $A - C = 0$, $\\cot(2\\phi) = 0$.",
               "explicacion_md": "$A = C \\Rightarrow A - C = 0 \\Rightarrow \\cot(2\\phi) = 0 \\Rightarrow 2\\phi = \\pi/2 \\Rightarrow \\phi = \\pi/4$."},
              {"enunciado_md": "El **discriminante** de una cónica $Ax^2 + Bxy + Cy^2 + \\ldots = 0$ es $\\delta = B^2 - 4AC$. ¿Qué representa $\\delta < 0$?",
               "opciones_md": ["Hipérbola", "Parábola", "Elipse (o circunferencia)", "Recta"],
               "correcta": "C",
               "pista_md": "El discriminante es invariante bajo rotaciones.",
               "explicacion_md": "$\\delta < 0$: elipse (o circunferencia si además $A = C$ y $B = 0$). $\\delta = 0$: parábola. $\\delta > 0$: hipérbola. El discriminante es invariante por rotaciones."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\tan(2\\phi)$ con $\\tan\\phi.$** La fórmula que elimina el término cruzado relaciona $B$ y $A - C$ con $\\tan(2\\phi)$, no con $\\tan\\phi$ directamente.",
              "**Olvidar el caso $A = C.$** Cuando los coeficientes cuadráticos coinciden, $A - C = 0$ y la fórmula no aplica directamente; el ángulo es $\\phi = \\pi/4.$",
              "**Tomar el signo incorrecto al calcular $\\cos(2\\phi).$** Como $\\phi$ es ángulo agudo y $2\\phi \\in (0, \\pi)$, $\\cos(2\\phi)$ puede ser positivo o negativo, pero $\\sin\\phi$ y $\\cos\\phi$ son positivos.",
              "**Usar las fórmulas de rotación al revés.** Las fórmulas $x = X\\cos\\phi - Y\\sin\\phi$, $y = X\\sin\\phi + Y\\cos\\phi$ expresan $(x, y)$ en términos de $(X, Y).$ La transformación inversa cambia de signo el ángulo.",
              "**Evaluar el discriminante con signo equivocado.** $\\delta = B^2 - 4 A C$, no $4AC - B^2.$",
          ]),

        b("resumen",
          puntos_md=[
              "**Ecuación general de segundo grado:** $A x^2 + B x y + C y^2 + D x + E y + F = 0.$",
              "**Fórmulas de rotación:** $x = X\\cos\\phi - Y\\sin\\phi,\\, y = X\\sin\\phi + Y\\cos\\phi.$",
              "**Ángulo que elimina $Bxy$:** $\\tan(2\\phi) = B/(A - C)$ si $A \\ne C$, $\\phi = \\pi/4$ si $A = C.$",
              "**Cálculo de $\\sin\\phi, \\cos\\phi$:** primero $\\cos(2\\phi)$ por la identidad pitagórica $\\cos^2(2\\phi) = 1/(1 + \\tan^2 2\\phi)$, luego ángulo medio.",
              "**Discriminante** $\\delta = B^2 - 4AC$ es invariante bajo rotación. Clasifica la cónica: $\\delta < 0$ elipse, $\\delta = 0$ parábola, $\\delta > 0$ hipérbola.",
              "**Procedimiento general:** (1) calcular $\\delta$; (2) si $B \\ne 0$ obtener $\\phi$; (3) calcular $\\sin\\phi$, $\\cos\\phi$; (4) sustituir las fórmulas de rotación; (5) reconocer la forma canónica.",
              "Próxima lección: **rotaciones combinadas con traslaciones** para tratar cónicas no centradas en el origen.",
          ]),
    ]
    return {"id": "lec-ia-5-6-rotacion", "title": "Rotación de Ejes",
            "description": "Ecuación general de segundo grado, fórmulas de rotación de ejes, eliminación del término xy y cálculo de seno y coseno del ángulo de rotación.",
            "blocks": blocks, "duration_minutes": 60, "order": 6}


# ============================================================================
# 5.7 Rotaciones y Traslaciones
# ============================================================================
def lesson_5_7():
    blocks = [
        b("texto", body_md=(
            "La **ecuación general de segundo grado** en dos variables aparece naturalmente al estudiar "
            "las curvas cónicas: elipses, parábolas e hipérbolas. Sin embargo, cuando la ecuación contiene "
            "un término mixto $xy$, la naturaleza geométrica de la curva no es evidente de inmediato. "
            "Las técnicas de **rotación** y **traslación** de ejes coordenados permiten simplificar estas "
            "ecuaciones hasta llevarlas a una forma reconocible, revelando la cónica subyacente y sus "
            "propiedades esenciales.\n\n"
            "**En esta lección estudiaremos:**\n\n"
            "- Cómo girar los ejes coordenados para eliminar el término $xy.$\n"
            "- Cómo combinar la rotación con una **traslación** para llevar la ecuación a su forma canónica.\n"
            "- Cómo determinar el ángulo de rotación adecuado mediante $\\tan(2\\phi) = \\dfrac{B}{A - C}.$\n"
            "- La clasificación de cónicas mediante el **discriminante** $\\delta = B^2 - 4AC$, sin necesidad de realizar la transformación completa.\n"
            "- El procedimiento completo de identificación y reducción aplicado a ejemplos concretos."
        )),

        b("definicion",
          titulo="Ecuación general de segundo grado",
          body_md=(
              "La **ecuación general de segundo grado**, también llamada **ecuación cuadrática**, en las "
              "variables $x$ e $y$ se escribe en la forma\n\n"
              "$$\\boxed{\\,A x^2 + B x y + C y^2 + D x + E y + F = 0\\,},$$\n\n"
              "donde $A, B, C, D, E$ y $F$ son constantes reales.\n\n"
              "El término $B x y$ recibe el nombre de **término mixto** o **término cruzado**. Su presencia "
              "indica que los ejes de la cónica están **inclinados** respecto a los ejes cartesianos "
              "originales, lo que dificulta identificar directamente el tipo de curva. La estrategia "
              "fundamental para simplificar la ecuación consiste en **rotar los ejes coordenados** un "
              "ángulo apropiado $\\phi$ de modo que, en el nuevo sistema de ejes $XY$, el coeficiente "
              "del término $XY$ sea igual a cero.\n\n"
              "Una vez eliminado el término cruzado, los términos lineales $D'X$ y $E'Y$ que pueden quedar "
              "se eliminan a su vez mediante una **traslación** de ejes, llevando la ecuación a la forma "
              "canónica de la cónica."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema de rotación de ejes.** Si el punto $P$ tiene coordenadas $(x, y)$ respecto a "
              "los ejes rectangulares $xy$, y los ejes coordenados se giran un ángulo $\\phi$ en torno "
              "al origen, entonces las coordenadas $(X, Y)$ de $P$ en el nuevo sistema satisfacen las "
              "**ecuaciones de rotación**:\n\n"
              "$$\\boxed{\\,x = X \\cos\\phi - Y \\sin\\phi, \\qquad y = X \\sin\\phi + Y \\cos\\phi.\\,}$$\n\n"
              "**Deducción.** Si introducimos la distancia $r = OP$ y el ángulo $\\theta$ que forma "
              "$\\overline{OP}$ con el eje $X$ rotado, entonces $X = r\\cos\\theta$, $Y = r\\sin\\theta.$ "
              "Respecto a los ejes originales, el mismo segmento forma un ángulo $\\theta + \\phi$ con el "
              "eje $x$, por lo que $x = r \\cos(\\theta + \\phi)$ e $y = r\\sin(\\theta + \\phi).$ "
              "Aplicando las **fórmulas de adición** de coseno y seno se obtienen las ecuaciones de rotación."
          )),

        b("ejemplo_resuelto",
          titulo="xy = 2 vista como hipérbola rotada",
          problema_md="Gira los ejes coordenados un ángulo de $45°$ para demostrar que la gráfica de $xy = 2$ es una hipérbola.",
          pasos=[
              paso("Aplicamos las fórmulas de rotación con $\\phi = 45°$, $\\cos 45° = \\sin 45° = \\dfrac{1}{\\sqrt 2}$:\n\n"
                   "$x = \\dfrac{X}{\\sqrt 2} - \\dfrac{Y}{\\sqrt 2}, \\qquad y = \\dfrac{X}{\\sqrt 2} + \\dfrac{Y}{\\sqrt 2}.$"),
              paso("Sustituyendo en $xy = 2$:\n\n"
                   "$\\left(\\dfrac{X}{\\sqrt 2} - \\dfrac{Y}{\\sqrt 2}\\right)\\left(\\dfrac{X}{\\sqrt 2} + \\dfrac{Y}{\\sqrt 2}\\right) = 2.$"),
              paso("El producto a la izquierda es una diferencia de cuadrados: "
                   "$\\dfrac{X^2}{2} - \\dfrac{Y^2}{2} = 2$, equivalentemente $\\dfrac{X^2}{4} - \\dfrac{Y^2}{4} = 1.$"),
              paso("Esta es la ecuación canónica de una **hipérbola** equilátera de semiejes $a = b = 2$, "
                   "con eje transverso a lo largo del eje $X$ rotado $45°$ respecto al eje $x$ original. "
                   "Sus ejes de simetría son las **bisectrices** de los cuadrantes del sistema original.",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Eliminación del término $xy$: ángulo de rotación óptimo.**\n\n"
              "Para eliminar el término $B x y$ en la ecuación general de cónicas, se debe girar los "
              "ejes un **ángulo agudo** $\\phi$ que satisface:\n\n"
              "$$\\boxed{\\;\\begin{cases}\\tan(2\\phi) = \\dfrac{B}{A - C} & \\text{si } A \\ne C, \\\\[4pt]"
              "\\phi = \\dfrac{\\pi}{4} & \\text{si } A = C. \\end{cases}\\;}$$\n\n"
              "**Cálculo de $\\sin\\phi$ y $\\cos\\phi$ a partir de $\\tan(2\\phi).$** Una vez determinado "
              "$\\tan(2\\phi)$, se calcula $\\cos(2\\phi)$ usando la identidad pitagórica\n\n"
              "$$\\cos^2(2\\phi) = \\dfrac{1}{1 + \\tan^2(2\\phi)},$$\n\n"
              "tomando la raíz **positiva** (puesto que $0 < 2\\phi < \\pi$). Luego, las funciones "
              "$\\sin\\phi$ y $\\cos\\phi$ se calculan mediante las **identidades del ángulo medio**:\n\n"
              "$$\\sin\\phi = \\sqrt{\\dfrac{1 - \\cos(2\\phi)}{2}}, \\qquad \\cos\\phi = \\sqrt{\\dfrac{1 + \\cos(2\\phi)}{2}},$$\n\n"
              "tomando las raíces positivas porque $\\phi$ es un ángulo agudo."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicación: parábola rotada",
          problema_md=("Usa una rotación de ejes para eliminar el término $xy$ en la ecuación\n\n"
                       "$64 x^2 + 96 xy + 36 y^2 - 15 x + 20 y - 25 = 0,$\n\n"
                       "y describe la gráfica resultante."),
          pasos=[
              paso("Coeficientes: $A = 64$, $B = 96$, $C = 36.$ Como $A \\ne C$:\n\n"
                   "$\\tan(2\\phi) = \\dfrac{B}{A - C} = \\dfrac{96}{28} = \\dfrac{24}{7}.$"),
              paso("Triángulo rectángulo con catetos $24$ y $7$, hipotenusa $\\sqrt{576 + 49} = 25.$ "
                   "Luego $\\cos(2\\phi) = \\dfrac{7}{25}.$"),
              paso("Identidades del ángulo medio:\n\n"
                   "$\\sin\\phi = \\sqrt{\\dfrac{1 - 7/25}{2}} = \\sqrt{\\dfrac{18/25}{2}} = \\sqrt{\\dfrac{9}{25}} = \\dfrac{3}{5}, \\quad "
                   "\\cos\\phi = \\sqrt{\\dfrac{1 + 7/25}{2}} = \\sqrt{\\dfrac{16}{25}} = \\dfrac{4}{5}.$"),
              paso("Fórmulas de rotación:\n\n"
                   "$x = \\dfrac{4 X - 3 Y}{5}, \\qquad y = \\dfrac{3 X + 4 Y}{5}.$"),
              paso("Sustituyendo en la ecuación original (el término $XY$ se cancela por construcción), "
                   "se obtiene una ecuación en $X$ e $Y$ que corresponde a una **parábola** en posición "
                   "estándar respecto a los ejes $X$ e $Y.$ El discriminante confirma la clasificación: "
                   "$\\delta = B^2 - 4AC = 9216 - 9216 = 0.$",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Clasificación de cónicas por el discriminante.** Una herramienta poderosa para "
              "identificar el tipo de cónica **sin necesidad de realizar la rotación** es el "
              "**discriminante**\n\n"
              "$$\\delta = B^2 - 4 A C,$$\n\n"
              "que es **invariante** bajo rotaciones de ejes. Esto significa que conserva su valor "
              "cualquiera sea el ángulo de rotación aplicado, lo que justifica que pueda usarse "
              "directamente sobre los coeficientes originales.\n\n"
              "**Teorema (identificación de cónicas).** La gráfica de la ecuación general "
              "$A x^2 + B x y + C y^2 + D x + E y + F = 0$ es una cónica o una cónica degenerada. "
              "En los casos no degenerados, la gráfica es:\n\n"
              "1. una **elipse** (o circunferencia) si $B^2 - 4 A C < 0$,\n"
              "2. una **parábola** si $B^2 - 4 A C = 0$,\n"
              "3. una **hipérbola** si $B^2 - 4 A C > 0.$\n\n"
              "Cuando $B = 0$, el discriminante se reduce a $-4AC$, recuperando la clasificación habitual "
              "para cónicas en posición estándar."
          )),

        b("ejemplo_resuelto",
          titulo="Identificación, rotación y traslación combinadas",
          problema_md=("Determina la naturaleza de la cónica que representa la ecuación\n\n"
                       "$$2 x^2 - 12 x y + 18 y^2 + x - 3 y - 6 = 0,$$\n\n"
                       "reduce la ecuación a su forma canónica por transformación de coordenadas y traza "
                       "el lugar geométrico junto con todos los sistemas de ejes coordenados."),
          pasos=[
              paso("Identificamos $A = 2$, $B = -12$, $C = 18.$ Discriminante:\n\n"
                   "$\\delta = B^2 - 4AC = 144 - 144 = 0.$ Es una **parábola** o caso degenerado de tipo parabólico."),
              paso("Como $A \\ne C$: $\\tan(2\\phi) = \\dfrac{-12}{2 - 18} = \\dfrac{-12}{-16} = \\dfrac{3}{4}.$ "
                   "Triángulo de catetos $3, 4$ e hipotenusa $5$ da $\\cos(2\\phi) = \\dfrac{4}{5}.$"),
              paso("$\\sin\\phi = \\sqrt{\\dfrac{1 - 4/5}{2}} = \\dfrac{1}{\\sqrt{10}}, \\quad "
                   "\\cos\\phi = \\sqrt{\\dfrac{1 + 4/5}{2}} = \\dfrac{3}{\\sqrt{10}}.$"),
              paso("Fórmulas de rotación: $x = \\dfrac{3 X - Y}{\\sqrt{10}}, \\quad y = \\dfrac{X + 3 Y}{\\sqrt{10}}.$"),
              paso("Observación: $2x^2 - 12xy + 18y^2 = 2(x - 3y)^2.$ Calculamos $x - 3y$ tras la rotación:\n\n"
                   "$x - 3y = \\dfrac{3 X - Y - 3 X - 9 Y}{\\sqrt{10}} = \\dfrac{-10 Y}{\\sqrt{10}} = -\\sqrt{10}\\, Y.$ "
                   "Luego $2(x - 3y)^2 = 2 \\cdot 10 Y^2 = 20 Y^2.$"),
              paso("Para el término lineal $x - 3y$ (en el resto de la ecuación):\n\n"
                   "$x - 3y = -\\sqrt{10}\\, Y$, así sustituyendo:\n\n"
                   "$20 Y^2 + \\dfrac{1}{\\sqrt{10}}(-\\sqrt{10}\\, Y) - 6 = 0 \\;\\Longrightarrow\\; 20 Y^2 - Y - 6 = 0.$"),
              paso("Esta es una ecuación cuadrática en $Y$ que **no involucra $X$**, lo cual indica que "
                   "la gráfica son **dos rectas paralelas** al eje $X$ (caso degenerado de parábola). "
                   "Resolviendo $20Y^2 - Y - 6 = 0$ se obtienen los valores $Y$ y, en consecuencia, "
                   "la ecuación se simplifica a un par de rectas $Y = Y_1$, $Y = Y_2$ en el sistema rotado.",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Procedimiento general de identificación y reducción.** Para analizar y simplificar una "
              "ecuación cuadrática general $A x^2 + B x y + C y^2 + D x + E y + F = 0$, el procedimiento "
              "completo se organiza en las siguientes etapas:\n\n"
              "**Paso 1 — Calcular el discriminante.** Evaluar $\\delta = B^2 - 4AC$ para clasificar "
              "preliminarmente la cónica: elipse si $\\delta < 0$, parábola si $\\delta = 0$, hipérbola si $\\delta > 0.$\n\n"
              "**Paso 2 — Determinar el ángulo de rotación.** Si $B \\ne 0$, calcular $\\phi$ mediante "
              "$\\tan(2\\phi) = \\dfrac{B}{A - C}$ (con $\\phi = \\pi/4$ si $A = C$), y luego obtener "
              "$\\sin\\phi$ y $\\cos\\phi$ usando las identidades del ángulo medio.\n\n"
              "**Paso 3 — Aplicar la rotación.** Sustituir $x = X\\cos\\phi - Y\\sin\\phi$ e "
              "$y = X\\sin\\phi + Y\\cos\\phi$ en la ecuación original. El resultado es una ecuación sin "
              "término $XY$, de la forma $A' X^2 + C' Y^2 + D' X + E' Y + F' = 0.$\n\n"
              "**Paso 4 — Completar el cuadrado (traslación).** Si aún existen términos lineales $D' X$ "
              "o $E' Y$, completar cuadrados en $X$ y en $Y$ para trasladar el origen al **vértice** "
              "(si es parábola) o al **centro** (si es elipse o hipérbola). La traslación se escribe "
              "$X = X' + h$, $Y = Y' + k$, lo cual lleva la ecuación a su **forma canónica** $a {X'}^2 + b {Y'}^2 = c$ "
              "u otra forma reconocible.\n\n"
              "**Paso 5 — Identificar y graficar.** Con la forma canónica, identificar los parámetros de "
              "la cónica (semiejes, vértices, focos, directriz, etc.) y trazar la curva indicando los "
              "distintos sistemas de ejes utilizados (original, rotado, trasladado)."
          )),

        b("texto", body_md=(
            "**Fórmulas de referencia rápida.**\n\n"
            "- **Ecuación general:** $A x^2 + B x y + C y^2 + D x + E y + F = 0.$\n"
            "- **Rotación:** $x = X\\cos\\phi - Y\\sin\\phi$, $y = X\\sin\\phi + Y\\cos\\phi.$\n"
            "- **Ángulo:** $\\tan(2\\phi) = B/(A - C)$ (o $\\phi = \\pi/4$ si $A = C$).\n"
            "- **Cálculo de $\\sin\\phi, \\cos\\phi$:** $\\cos^2(2\\phi) = 1/(1 + \\tan^2 2\\phi)$ y luego identidades del ángulo medio.\n"
            "- **Discriminante:** $\\delta = B^2 - 4AC.$\n"
            "- **Traslación de ejes (centro/vértice en $(h, k)$):** $X = X' + h$, $Y = Y' + k.$"
        )),

        ej(
            "Identificar y rotar (caso A = C)",
            "Determina el ángulo de rotación que elimina el término $xy$ en la ecuación $2x^2 + 4xy + 2y^2 - 8 = 0$ y reduce a forma canónica.",
            ["Como $A = C = 2$, el ángulo de rotación es $\\pi/4.$",
             "Aplica $\\sin 45° = \\cos 45° = 1/\\sqrt 2$ en las fórmulas.",
             "Sustituye y simplifica."],
            ("$\\phi = 45°.$ Fórmulas: $x = (X - Y)/\\sqrt 2$, $y = (X + Y)/\\sqrt 2.$ "
             "Sustituyendo: $2((X-Y)/\\sqrt 2)^2 + 4((X-Y)/\\sqrt 2)((X+Y)/\\sqrt 2) + 2((X+Y)/\\sqrt 2)^2 - 8 = 0$, "
             "que simplifica a $4 X^2 - 8 = 0$, es decir, $X^2 = 2.$ Son **dos rectas paralelas** $X = \\pm\\sqrt 2$ "
             "(elipse degenerada con $B^2 - 4AC = 16 - 16 = 0$, parábola degenerada).")
        ),

        ej(
            "Naturaleza por discriminante con eje horizontal",
            "Clasifica la cónica $5 x^2 + 6 x y + 5 y^2 - 4 x + 4 y - 4 = 0$ usando el discriminante.",
            ["Calcula $\\delta = B^2 - 4AC.$",
             "$A = 5$, $B = 6$, $C = 5.$"],
            ("$\\delta = 36 - 100 = -64 < 0$: **elipse** (rotada).")
        ),

        ej(
            "Rotación cuando el término xy domina",
            "¿Qué cónica representa $xy - 4 = 0$? Justifica con el discriminante y rótala $45°$ para confirmar.",
            ["$A = C = 0$, $B = 1.$ $\\delta = 1 > 0.$",
             "Rotación $45°$: $xy = ((X-Y)/\\sqrt 2)((X+Y)/\\sqrt 2) = (X^2 - Y^2)/2.$"],
            ("$\\delta = 1 > 0$: **hipérbola**. Rotando $45°$: $\\dfrac{X^2 - Y^2}{2} = 4 \\Rightarrow X^2 - Y^2 = 8$, "
             "hipérbola equilátera con $a = b = 2\\sqrt 2.$")
        ),

        ej(
            "Identificación con traslación posterior",
            ("Para la cónica $4 x^2 + 4 x y + y^2 - 24 x + 38 y - 139 = 0$, "
             "(a) clasifícala usando el discriminante; (b) determina el ángulo de rotación que elimina $xy.$"),
            ["Calcula $\\delta = B^2 - 4AC$ y clasifica.",
             "Si $A = C$, $\\phi = 45°.$ Si no, $\\tan(2\\phi) = B/(A - C).$",
             "$A = 4$, $B = 4$, $C = 1.$"],
            ("**(a)** $\\delta = 16 - 16 = 0$: **parábola** (o degenerada). "
             "**(b)** $\\tan(2\\phi) = 4/(4 - 1) = 4/3.$ "
             "Triángulo $3, 4, 5$ da $\\cos(2\\phi) = 3/5.$ "
             "$\\sin\\phi = \\sqrt{(1 - 3/5)/2} = 1/\\sqrt 5$, $\\cos\\phi = \\sqrt{(1 + 3/5)/2} = 2/\\sqrt 5$, "
             "es decir, $\\phi = \\arctan(1/2) \\approx 26{,}57°.$")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "Si en la ecuación general $Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0$ se tiene $B = 0$, ¿qué transformación basta para llegar a la forma canónica?",
               "opciones_md": ["Solo rotación", "Solo traslación (completar cuadrados)", "Rotación seguida de traslación", "Ninguna basta"],
               "correcta": "B",
               "pista_md": "El término cruzado $Bxy$ es el que requiere rotación.",
               "explicacion_md": "Cuando $B = 0$ no hay término cruzado y los ejes ya están alineados con los de la cónica; basta una **traslación** (completar cuadrados) para centrarla en el vértice o centro."},
              {"enunciado_md": "Si la cónica está rotada **y** desplazada, ¿en qué orden se aplican las transformaciones?",
               "opciones_md": ["Primero traslación, luego rotación", "Primero rotación, luego traslación", "El orden no importa", "Solo se aplica una transformación"],
               "correcta": "B",
               "pista_md": "Primero hay que eliminar el término cruzado; luego mover el centro.",
               "explicacion_md": "La estrategia estándar es **rotar primero** para eliminar $Bxy$ y obtener una cónica con ejes paralelos a los nuevos ejes; luego **trasladar** completando cuadrados para centrarla en su vértice/centro."},
              {"enunciado_md": "El discriminante $\\delta = B^2 - 4AC$ permite clasificar una cónica **sin transformar**, pero no informa sobre:",
               "opciones_md": ["El tipo (elipse/parábola/hipérbola)", "Si la cónica es degenerada (recta, punto, vacío)", "El signo de $A$", "La presencia de $xy$"],
               "correcta": "B",
               "pista_md": "El discriminante predice el tipo pero no la degeneración.",
               "explicacion_md": "$\\delta$ identifica el tipo, pero hay que examinar la ecuación tras transformar para detectar **casos degenerados** (par de rectas, un punto o el vacío)."},
          ]),

        fig("Diagrama educativo en español que ilustra la estrategia rotación + traslación: tres paneles consecutivos. Panel 1: una cónica rotada y desplazada en el plano $XY$ original. Panel 2: tras rotación, la cónica con sus ejes paralelos a los ejes coordenados pero desplazada del origen. Panel 3: tras traslación final, la cónica en posición canónica con su centro/vértice en el origen. Flechas ámbar #f59e0b entre paneles indicando \"rotar $\\phi$\" y \"trasladar\". Cónicas en teal #06b6d4. Fondo blanco. " + STYLE),

        b("errores_comunes",
          items_md=[
              "**Aplicar rotación cuando $B = 0.$** Si no hay término cruzado, la cónica ya está en posición estándar; basta completar cuadrados (traslación) para llevarla a forma canónica.",
              "**Olvidar el paso de traslación.** Tras la rotación pueden quedar términos lineales $D' X$ o $E' Y$; eliminarlos requiere completar cuadrados.",
              "**Confundir el orden rotación/traslación.** Si la cónica tiene su centro fuera del origen y está rotada, primero se rota y después se traslada.",
              "**Tomar valores incorrectos en el ángulo medio.** Recordar que $\\sin\\phi$ y $\\cos\\phi$ son positivos por ser $\\phi$ agudo, pero $\\cos(2\\phi)$ puede ser positivo o negativo según el cuadrante de $2\\phi.$",
              "**Ignorar los casos degenerados.** El discriminante predice el **tipo** pero no descarta la degeneración (rectas, puntos, vacío). Hay que examinar la ecuación resultante tras la transformación.",
          ]),

        b("resumen",
          puntos_md=[
              "**Ecuación general:** $A x^2 + B x y + C y^2 + D x + E y + F = 0.$",
              "**Rotación de ejes** elimina el término cruzado $Bxy$ con $\\phi$ determinado por $\\tan(2\\phi) = B/(A - C).$",
              "**Traslación de ejes** elimina los términos lineales tras la rotación y centra la cónica en su vértice o centro.",
              "**Discriminante invariante:** $\\delta = B^2 - 4AC$ clasifica el tipo de cónica sin necesidad de transformar.",
              "**Procedimiento completo:** (1) discriminante; (2) ángulo de rotación; (3) sustitución; (4) traslación / completar cuadrados; (5) lectura de la forma canónica.",
              "Próxima lección: **identificación de cualquier ecuación de segundo grado** y casos degenerados.",
          ]),
    ]
    return {"id": "lec-ia-5-7-rotaciones-traslaciones", "title": "Rotaciones y Traslaciones",
            "description": "Combinación de rotación y traslación de ejes para llevar la ecuación general de segundo grado a su forma canónica reconocible.",
            "blocks": blocks, "duration_minutes": 60, "order": 7}


# ============================================================================
# 5.8 Identificación de una Cónica
# ============================================================================
def lesson_5_8():
    blocks = [
        b("texto", body_md=(
            "La **ecuación general de segundo grado** permite describir de manera unificada todas las "
            "curvas cónicas: elipses, parábolas e hipérbolas. Cuando dicha ecuación contiene un término "
            "mixto $Bxy$ con $B \\ne 0$, la cónica aparece **rotada** respecto a los ejes coordenados, "
            "lo que dificulta su identificación directa. La herramienta clave para resolver este problema "
            "es la **rotación de ejes**, que permite eliminar el término cruzado y reducir la ecuación a "
            "una forma canónica reconocible. Sin embargo, gracias a la **invarianza del discriminante** "
            "$B^2 - 4AC$, podemos identificar el tipo de cónica **sin necesidad** de realizar la rotación.\n\n"
            "**En esta lección estudiaremos:**\n\n"
            "- La forma general de la ecuación cuadrática en dos variables y sus coeficientes.\n"
            "- Cómo aplicar las **fórmulas de rotación** para eliminar el término mixto $Bxy.$\n"
            "- Cómo determinar el **ángulo de rotación** adecuado y calcular $\\sin\\phi$ y $\\cos\\phi.$\n"
            "- Cómo identificar el **tipo de cónica** mediante el discriminante $\\delta = B^2 - 4AC.$\n"
            "- Cómo reducir cualquier ecuación general de segundo grado a su **forma canónica**, incluyendo el tratamiento de casos degenerados.\n\n"
            "Esta lección **cierra el curso de Introducción al Álgebra**, integrando todo lo aprendido sobre cónicas."
        )),

        b("definicion",
          titulo="Ecuación general de segundo grado",
          body_md=(
              "La **ecuación general de segundo grado**, también llamada **ecuación cuadrática**, en "
              "las variables $x$ e $y$ se escribe como\n\n"
              "$$\\boxed{\\,A x^2 + B x y + C y^2 + D x + E y + F = 0\\,},$$\n\n"
              "donde $A, B, C, D, E$ y $F$ son constantes reales. Para que la ecuación sea efectivamente "
              "de segundo grado, al menos una de las constantes $A$, $B$ o $C$ debe ser distinta de cero.\n\n"
              "Cuando $B \\ne 0$, la ecuación contiene un **término mixto $Bxy$** que indica que la cónica "
              "está **inclinada** respecto a los ejes cartesianos originales. Para identificar y graficar "
              "la cónica en estos casos, es conveniente realizar una **rotación de ejes** que elimine "
              "dicho término."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema de rotación de ejes.** Si el punto $P$ tiene coordenadas $(x, y)$ respecto a "
              "los ejes rectangulares $xy$, y los ejes coordenados se giran un ángulo agudo $\\phi$ "
              "alrededor del origen, entonces las coordenadas $(X, Y)$ del punto $P$ en el nuevo sistema "
              "satisfacen las **ecuaciones de rotación**:\n\n"
              "$$\\boxed{\\,x = X \\cos(\\phi) - Y \\sin(\\phi), \\qquad y = X \\sin(\\phi) + Y \\cos(\\phi).\\,}$$\n\n"
              "Estas relaciones permiten expresar las variables originales $x$ e $y$ en términos de las "
              "nuevas variables $X$ e $Y$, lo que posibilita sustituirlas en cualquier ecuación dada para "
              "obtener su expresión en el sistema rotado."
          )),

        b("teorema",
          enunciado_md=(
              "**Eliminación del término mixto.** Para eliminar el término $B x y$ en la ecuación general "
              "de cónicas, se deben girar los ejes un **ángulo agudo** $\\phi$ que satisface la condición:\n\n"
              "$$\\boxed{\\;\\begin{cases}\\tan(2\\phi) = \\dfrac{B}{A - C} & \\text{si } A \\ne C, \\\\[4pt]"
              "\\phi = \\dfrac{\\pi}{4} & \\text{si } A = C. \\end{cases}\\;}$$\n\n"
              "**Cálculo de $\\sin\\phi, \\cos\\phi.$** Una vez determinado $\\tan(2\\phi)$, se calcula "
              "$\\cos(2\\phi)$ mediante\n\n"
              "$$\\cos^2(2\\phi) = \\dfrac{1}{1 + \\tan^2(2\\phi)},$$\n\n"
              "tomando la raíz positiva. Luego $\\sin\\phi$ y $\\cos\\phi$ se obtienen con las "
              "**identidades del ángulo medio**\n\n"
              "$$\\sin\\phi = \\sqrt{\\dfrac{1 - \\cos(2\\phi)}{2}}, \\qquad \\cos\\phi = \\sqrt{\\dfrac{1 + \\cos(2\\phi)}{2}}.$$"
          )),

        b("ejemplo_resuelto",
          titulo="Demostrar que xy = 2 es una hipérbola",
          problema_md="Gira los ejes coordenados un ángulo de $45°$ para demostrar que la gráfica de $xy = 2$ es una hipérbola.",
          pasos=[
              paso("Con $\\phi = 45°$ tenemos $\\cos 45° = \\sin 45° = \\dfrac{1}{\\sqrt 2}.$ Las fórmulas de rotación dan\n\n"
                   "$x = \\dfrac{X - Y}{\\sqrt 2}, \\qquad y = \\dfrac{X + Y}{\\sqrt 2}.$"),
              paso("Sustituyendo en $xy = 2$:\n\n"
                   "$\\left(\\dfrac{X - Y}{\\sqrt 2}\\right) \\left(\\dfrac{X + Y}{\\sqrt 2}\\right) = 2 "
                   "\\;\\Longleftrightarrow\\; \\dfrac{X^2 - Y^2}{2} = 2 \\;\\Longleftrightarrow\\; \\dfrac{X^2}{4} - \\dfrac{Y^2}{4} = 1.$"),
              paso("Esta es la ecuación canónica de una **hipérbola** equilátera con semiejes $a = b = 2$, "
                   "centrada en el origen del sistema $XY$, cuyos ejes están rotados $45°$ respecto a los ejes "
                   "originales. Queda demostrado que la curva $xy = 2$ es efectivamente una hipérbola.",
                   "Resultado.", resultado=True),
          ]),

        b("ejemplo_resuelto",
          titulo="Eliminación del término xy: parábola rotada",
          problema_md=("Usa una rotación de ejes para eliminar el término $xy$ en la ecuación\n\n"
                       "$64 x^2 + 96 xy + 36 y^2 - 15 x + 20 y - 25 = 0,$\n\n"
                       "identifica y traza su gráfica."),
          pasos=[
              paso("Identificamos $A = 64$, $B = 96$, $C = 36.$ Como $A \\ne C$:\n\n"
                   "$\\tan(2\\phi) = \\dfrac{B}{A - C} = \\dfrac{96}{28} = \\dfrac{24}{7}.$"),
              paso("Triángulo de catetos $24$ y $7$, hipotenusa $\\sqrt{576 + 49} = 25$, da $\\cos(2\\phi) = \\dfrac{7}{25}.$"),
              paso("Identidades del ángulo medio:\n\n"
                   "$\\sin\\phi = \\sqrt{\\dfrac{1 - 7/25}{2}} = \\sqrt{\\dfrac{18}{50}} = \\sqrt{\\dfrac{9}{25}} = \\dfrac{3}{5}, \\quad "
                   "\\cos\\phi = \\sqrt{\\dfrac{1 + 7/25}{2}} = \\sqrt{\\dfrac{32}{50}} = \\sqrt{\\dfrac{16}{25}} = \\dfrac{4}{5}.$"),
              paso("Las fórmulas de rotación son\n\n"
                   "$x = \\dfrac{4 X - 3 Y}{5}, \\qquad y = \\dfrac{3 X + 4 Y}{5}.$"),
              paso("Al sustituir en la ecuación original (el término $XY$ se cancela), se obtiene una "
                   "ecuación en $X$ e $Y$ que corresponde a una **parábola**, cuya forma canónica se "
                   "identifica completando cuadrados en el sistema rotado.",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Teorema del discriminante.** No siempre es necesario efectuar la rotación completa para "
              "identificar el tipo de cónica. Existe un criterio algebraico directo basado en los "
              "coeficientes de la ecuación general:\n\n"
              "**La gráfica de $A x^2 + B x y + C y^2 + D x + E y + F = 0$ es una cónica o una cónica "
              "degenerada. En los casos no degenerados, la naturaleza de la cónica queda determinada por "
              "el valor del discriminante** $\\delta = B^2 - 4 A C$:\n\n"
              "1. Es una **elipse** (o circunferencia) si $B^2 - 4 A C < 0.$\n"
              "2. Es una **parábola** si $B^2 - 4 A C = 0.$\n"
              "3. Es una **hipérbola** si $B^2 - 4 A C > 0.$\n\n"
              "El valor $\\delta = B^2 - 4 A C$ recibe el nombre de **discriminante** de la ecuación. Es "
              "un **invariante** bajo rotaciones de ejes: no cambia cuando se efectúa una rotación. Esto "
              "justifica que pueda usarse directamente sobre los coeficientes originales $A, B, C$ sin "
              "necesidad de realizar la rotación."
          )),

        b("ejemplo_resuelto",
          titulo="Identificación, rotación y traslación combinadas",
          problema_md=("Determina la naturaleza de la cónica que representa la ecuación\n\n"
                       "$$2 x^2 - 12 x y + 18 y^2 + x - 3 y - 6 = 0,$$\n\n"
                       "y reduce la ecuación a su forma canónica por transformación de coordenadas."),
          pasos=[
              paso("Identificamos $A = 2$, $B = -12$, $C = 18.$ Calculamos el discriminante:\n\n"
                   "$\\delta = B^2 - 4AC = 144 - 144 = 0.$ La cónica es una **parábola** (o un caso degenerado).") ,
              paso("Para reducirla a forma canónica determinamos el ángulo de rotación. Como $A \\ne C$:\n\n"
                   "$\\tan(2\\phi) = \\dfrac{-12}{2 - 18} = \\dfrac{3}{4}.$"),
              paso("Triángulo de catetos $3$ y $4$, hipotenusa $5$: $\\cos(2\\phi) = \\dfrac{4}{5}.$ "
                   "Identidades del ángulo medio: $\\sin\\phi = \\dfrac{1}{\\sqrt{10}}, \\quad \\cos\\phi = \\dfrac{3}{\\sqrt{10}}.$"),
              paso("Fórmulas de rotación: $x = \\dfrac{3 X - Y}{\\sqrt{10}}, \\quad y = \\dfrac{X + 3 Y}{\\sqrt{10}}.$"),
              paso("Observamos $2x^2 - 12xy + 18y^2 = 2(x - 3y)^2.$ Calculamos $x - 3y$ tras la rotación:\n\n"
                   "$x - 3y = \\dfrac{3 X - Y}{\\sqrt{10}} - 3 \\cdot \\dfrac{X + 3 Y}{\\sqrt{10}} = \\dfrac{-10 Y}{\\sqrt{10}} = -\\sqrt{10}\\, Y.$"),
              paso("Luego $2(x - 3y)^2 = 20 Y^2.$ El término lineal $x - 3y$ se sustituye igual: "
                   "$\\dfrac{1}{\\sqrt{10}}(x - 3y) = \\dfrac{1}{\\sqrt{10}} \\cdot (-\\sqrt{10}\\, Y) = -Y.$ "
                   "La ecuación queda\n\n"
                   "$20 Y^2 - Y - 6 = 0.$"),
              paso("Esta es una **parábola** en la variable $X$ (no aparece $X$ en términos cuadráticos pero sí "
                   "es una cuadrática en $Y$ sin lineal en $X$, o sea, dos rectas paralelas $Y = $ constante en este caso particular degenerado). "
                   "Para llevar la ecuación a forma canónica $X' = a {Y'}^2$ se aplica una **traslación** que "
                   "elimina los términos lineales restantes.",
                   "Resultado.", resultado=True),
          ]),

        b("teorema",
          enunciado_md=(
              "**Esquema general de identificación.** Para identificar y reducir una cónica dada por "
              "$A x^2 + B x y + C y^2 + D x + E y + F = 0$, el procedimiento general es:\n\n"
              "**Paso 1 — Discriminante.** Calcular $\\delta = B^2 - 4AC$ para determinar el tipo de "
              "cónica: elipse si $\\delta < 0$, parábola si $\\delta = 0$, hipérbola si $\\delta > 0.$\n\n"
              "**Paso 2 — Ángulo de rotación.** Si $B \\ne 0$, calcular el ángulo $\\phi$ usando "
              "$\\tan(2\\phi) = \\dfrac{B}{A - C}$ (o $\\phi = \\pi/4$ si $A = C$), y obtener "
              "$\\sin\\phi, \\cos\\phi$ mediante las identidades del ángulo medio.\n\n"
              "**Paso 3 — Aplicar la rotación.** Sustituir $x = X\\cos\\phi - Y\\sin\\phi$ e "
              "$y = X\\sin\\phi + Y\\cos\\phi$ en la ecuación original para obtener una expresión sin "
              "el término $XY.$\n\n"
              "**Paso 4 — Traslación y forma canónica.** Completar cuadrados en $X$ e $Y$ según corresponda "
              "y efectuar la traslación $X = X' + h$, $Y = Y' + k$ para llevar la ecuación a su forma canónica.\n\n"
              "**Paso 5 — Identificar y graficar.** Identificar los elementos geométricos de la cónica "
              "(centro, vértice, focos, semiejes, asíntotas, etc.) en el sistema canónico y trazar la "
              "curva indicando los distintos sistemas de ejes utilizados."
          )),

        b("texto", body_md=(
            "**Casos degenerados.** Los casos degenerados ocurren cuando la ecuación general no representa "
            "una curva propiamente dicha, sino:\n\n"
            "- Un **punto** (elipse degenerada).\n"
            "- Una **recta**.\n"
            "- **Dos rectas** paralelas, secantes o coincidentes.\n"
            "- El **conjunto vacío**.\n\n"
            "El discriminante identifica el **tipo** de cónica, pero no descarta la degeneración: para "
            "determinar si la curva es degenerada se requiere un análisis adicional, por ejemplo, mediante "
            "el determinante de la **matriz asociada** a la forma cuadrática extendida\n\n"
            "$$M = \\begin{pmatrix} A & B/2 & D/2 \\\\ B/2 & C & E/2 \\\\ D/2 & E/2 & F \\end{pmatrix}.$$\n\n"
            "Si $\\det(M) = 0$, la cónica es degenerada; si $\\det(M) \\ne 0$, es no degenerada."
        )),

        ej(
            "Clasificación rápida por discriminante",
            "Indica el tipo de cónica:\n\n"
            "(a) $4 x^2 - 24 x y + 11 y^2 + 56 x - 58 y + 95 = 0.$\n\n"
            "(b) $9 x^2 + 12 x y + 4 y^2 - 24 x - 16 y + 3 = 0.$\n\n"
            "(c) $5 x^2 + 6 x y + 2 y^2 - 4 x + 4 y + 1 = 0.$",
            ["Identifica $A$, $B$, $C$ y calcula $\\delta = B^2 - 4AC$ en cada caso."],
            ("(a) $\\delta = 576 - 176 = 400 > 0$: **hipérbola**. "
             "(b) $\\delta = 144 - 144 = 0$: **parábola**. "
             "(c) $\\delta = 36 - 40 = -4 < 0$: **elipse**.")
        ),

        ej(
            "Caso degenerado: dos rectas paralelas",
            "Identifica la gráfica de $4x^2 - 4xy + y^2 - 12x + 6y + 5 = 0.$",
            ["Calcula el discriminante.",
             "Si $\\delta = 0$ es parábola o caso degenerado.",
             "Trata de factorizar la parte cuadrática como cuadrado perfecto."],
            ("$\\delta = 16 - 16 = 0$: tipo parábola. La parte cuadrática es $4x^2 - 4xy + y^2 = (2x - y)^2.$ "
             "La ecuación queda $(2x - y)^2 - 12x + 6y + 5 = (2x - y)^2 - 6(2x - y) + 5 = 0.$ "
             "Sea $u = 2x - y$: $u^2 - 6u + 5 = 0 \\Rightarrow (u - 1)(u - 5) = 0$, así $u = 1$ o $u = 5.$ "
             "**Dos rectas paralelas** $2x - y = 1$ y $2x - y = 5$ (parábola degenerada).")
        ),

        ej(
            "Identificación y rotación combinada",
            ("Para la cónica $5 x^2 + 4 x y + 2 y^2 - 24 x - 12 y + 18 = 0$:\n\n"
             "(a) clasifícala por discriminante; (b) determina el ángulo de rotación que elimina $xy.$"),
            ["$\\delta = B^2 - 4AC.$",
             "$\\tan(2\\phi) = B/(A - C)$ con $A \\ne C.$"],
            ("(a) $\\delta = 16 - 40 = -24 < 0$: **elipse**. "
             "(b) $\\tan(2\\phi) = 4/(5 - 2) = 4/3.$ Triángulo $3, 4, 5$ da $\\cos(2\\phi) = 3/5.$ "
             "$\\sin\\phi = \\sqrt{(1 - 3/5)/2} = 1/\\sqrt 5$, $\\cos\\phi = \\sqrt{(1 + 3/5)/2} = 2/\\sqrt 5.$")
        ),

        ej(
            "Detección de degeneración",
            "Demuestra que $x^2 - y^2 = 0$ es una cónica degenerada y describe su gráfica.",
            ["Factoriza el lado izquierdo.",
             "Cada factor igualado a cero da una ecuación de recta."],
            ("$x^2 - y^2 = (x - y)(x + y) = 0.$ La gráfica son las **dos rectas** $y = x$ e $y = -x$ "
             "(hipérbola degenerada en su par de asíntotas).")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "Si $\\delta = B^2 - 4AC = -7$ para una cónica no degenerada, ¿qué tipo es?",
               "opciones_md": ["Hipérbola", "Parábola", "Elipse (o circunferencia)", "Recta"],
               "correcta": "C",
               "pista_md": "$\\delta < 0$ corresponde a la cónica acotada.",
               "explicacion_md": "$\\delta < 0$: **elipse** (o circunferencia si además $A = C$ y $B = 0$). $\\delta = 0$: parábola. $\\delta > 0$: hipérbola."},
              {"enunciado_md": "Para clasificar la cónica $3x^2 - 4xy + 8y^2 - 12 = 0$, ¿cuánto vale $\\delta$ y qué tipo es?",
               "opciones_md": ["$\\delta = 16 - 96 = -80$, elipse", "$\\delta = 16 - 24 = -8$, elipse", "$\\delta = 16 + 96 = 112$, hipérbola", "$\\delta = -4 \\cdot 3 \\cdot 8 = -96$, parábola"],
               "correcta": "A",
               "pista_md": "$A = 3$, $B = -4$, $C = 8$. $\\delta = B^2 - 4AC$.",
               "explicacion_md": "$\\delta = (-4)^2 - 4 \\cdot 3 \\cdot 8 = 16 - 96 = -80 < 0$, por lo tanto es una **elipse** (rotada porque $B \\neq 0$)."},
              {"enunciado_md": "Si $\\delta > 0$ pero $\\det(M) = 0$ (matriz extendida de la cónica), ¿qué tenemos?",
               "opciones_md": ["Hipérbola no degenerada", "Par de rectas secantes (hipérbola degenerada)", "Elipse degenerada (un punto)", "Parábola"],
               "correcta": "B",
               "pista_md": "$\\det(M) = 0$ siempre indica degeneración.",
               "explicacion_md": "$\\delta > 0$ marca el tipo \"hipérbola\", pero si $\\det(M) = 0$ la cónica es degenerada: una hipérbola degenera en su **par de asíntotas** (dos rectas secantes)."},
          ]),

        fig("Diagrama educativo en español que clasifica cónicas según el discriminante $\\delta = B^2 - 4AC$ con tres regiones bien diferenciadas: a la izquierda una elipse en teal #06b6d4 con etiqueta \"$\\delta < 0$\", en el centro una parábola en ámbar #f59e0b con etiqueta \"$\\delta = 0$\", a la derecha una hipérbola en teal con etiqueta \"$\\delta > 0$\". Línea numérica horizontal abajo mostrando el signo del discriminante. Tipografía clara, fondo blanco. " + STYLE),

        b("errores_comunes",
          items_md=[
              "**Confundir el signo del discriminante.** $\\delta < 0$ ⟹ elipse, $\\delta = 0$ ⟹ parábola, $\\delta > 0$ ⟹ hipérbola. Memorizar el orden inverso es un error frecuente.",
              "**Olvidar que existen casos degenerados.** El discriminante predice el **tipo** pero no descarta la degeneración (rectas, puntos, vacío).",
              "**Aplicar el discriminante a cónicas en forma canónica.** Si la ecuación ya está en forma canónica, la identificación es directa por la forma; calcular $\\delta$ es innecesario.",
              "**Confundir el discriminante de la cónica con el de una cuadrática.** $B^2 - 4AC$ se refiere a la ecuación cuadrática **en dos variables**, no al discriminante $b^2 - 4ac$ de una ecuación cuadrática unidimensional.",
              "**Saltar el paso de traslación.** Tras eliminar el término $xy$ por rotación, los términos lineales remanentes se eliminan trasladando los ejes (completando cuadrados).",
              "**Tomar la raíz negativa al calcular $\\sin\\phi$ o $\\cos\\phi.$** Como $\\phi$ es ángulo agudo, ambas funciones son positivas; el signo de $\\cos(2\\phi)$ puede ser cualquiera, pero el de $\\sin\\phi$ y $\\cos\\phi$ es positivo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Ecuación general de segundo grado:** $A x^2 + B x y + C y^2 + D x + E y + F = 0.$",
              "**Discriminante** $\\delta = B^2 - 4 A C$ clasifica el tipo:",
              "$\\delta < 0$ ⟹ **elipse** (o circunferencia).",
              "$\\delta = 0$ ⟹ **parábola**.",
              "$\\delta > 0$ ⟹ **hipérbola**.",
              "**Casos degenerados:** punto, recta, dos rectas o conjunto vacío. Se identifican factorizando o completando cuadrados.",
              "**Procedimiento de reducción:** (1) discriminante; (2) ángulo de rotación; (3) sustitución; (4) traslación; (5) lectura canónica.",
              "**Cierre del curso:** ya dominas todo el lenguaje matemático universitario fundamental — lógica, conjuntos, inducción, sucesiones, trigonometría, polinomios complejos y geometría analítica. Estás listo para Cálculo Diferencial, Álgebra Lineal y los demás cursos universitarios construidos sobre estos cimientos.",
          ]),
    ]
    return {"id": "lec-ia-5-8-identificacion", "title": "Identificación de una Cónica",
            "description": "Discriminante δ = B² - 4AC, clasificación de cónicas no degeneradas, casos degenerados y esquema general de identificación y reducción.",
            "blocks": blocks, "duration_minutes": 50, "order": 8}


# ============================================================================
# MAIN
# ============================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

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

    builders = [
        lesson_5_1, lesson_5_2, lesson_5_3, lesson_5_4,
        lesson_5_5, lesson_5_6, lesson_5_7, lesson_5_8,
    ]

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
