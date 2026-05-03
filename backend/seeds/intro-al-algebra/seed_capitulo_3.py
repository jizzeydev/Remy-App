"""
Seed del curso Introducción al Álgebra — Capítulo 3: Trigonometría.
6 lecciones (alineadas con MAT1207 PUC):
  3.1 Razones trigonométricas
  3.2 Funciones trigonométricas
  3.3 Identidades trigonométricas
  3.4 Funciones trigonométricas inversas
  3.5 Ecuaciones trigonométricas
  3.6 Teorema del seno y coseno

ENFOQUE: del triángulo rectángulo al círculo unitario, de las funciones a las
identidades, de las identidades a las ecuaciones, y finalmente a la resolución
de triángulos arbitrarios. Esta progresión es la base de todo lo que viene en
cálculo y geometría analítica.

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

CHAPTER_ID = "ch-ia-trigonometria"
CHAPTER_TITLE = "Trigonometría"
CHAPTER_DESCRIPTION = (
    "Trigonometría desde cero: razones en el triángulo rectángulo, funciones "
    "trigonométricas en el círculo unitario, identidades fundamentales (adición, "
    "ángulo doble, producto a suma, prostaféresis), funciones inversas (arcsen, "
    "arccos, arctan), técnica para resolver ecuaciones trigonométricas y los "
    "Teoremas del Seno y del Coseno para resolver triángulos arbitrarios."
)
CHAPTER_ORDER = 3


# ============================================================================
# 3.1 Razones trigonométricas
# ============================================================================
def lesson_3_1():
    blocks = [
        b("texto", body_md=(
            "Las **razones trigonométricas** constituyen la base del estudio de la "
            "trigonometría. Permiten relacionar los ángulos de un triángulo "
            "rectángulo con las longitudes de sus lados, lo que abre la puerta a "
            "calcular distancias, alturas y ángulos inaccesibles a partir de "
            "medidas conocidas. Sus aplicaciones cruzan ingeniería, física, "
            "topografía y astronomía.\n\n"
            "En esta lección estudiaremos:\n\n"
            "- La definición de las **seis razones trigonométricas** y por qué "
            "dependen exclusivamente del ángulo.\n"
            "- Las **identidades recíprocas, de cociente y de Pitágoras**.\n"
            "- Las **fórmulas de cofunción** (complemento).\n"
            "- Los valores exactos para los **ángulos notables** $30°$, $45°$ y $60°$.\n"
            "- Cómo **resolver triángulos rectángulos** y aplicar todo a problemas reales."
        )),

        b("definicion",
          titulo="Las seis razones trigonométricas",
          body_md=(
              "Sea $ABC$ un triángulo rectángulo en $C$, con ángulo $\\alpha$ en el "
              "vértice $A$. Denotamos: $a$ = cateto opuesto a $\\alpha$, $b$ = cateto "
              "adyacente, $c$ = hipotenusa. Las **seis razones trigonométricas** se "
              "definen como:\n\n"
              "$$\\sin(\\alpha) = \\frac{a}{c}, \\quad \\cos(\\alpha) = \\frac{b}{c}, \\quad \\tan(\\alpha) = \\frac{a}{b},$$\n"
              "$$\\csc(\\alpha) = \\frac{c}{a}, \\quad \\sec(\\alpha) = \\frac{c}{b}, \\quad \\cot(\\alpha) = \\frac{b}{a}.$$\n"
              "**Observación clave:** dos triángulos rectángulos con el mismo ángulo "
              "$\\alpha$ son **semejantes**, por lo que las razones entre sus lados "
              "son idénticas. En consecuencia, **las razones dependen solo del "
              "ángulo, no del triángulo particular**."
          )),

        fig(
            "Triángulo rectángulo ABC con el ángulo recto en C (esquina inferior derecha). El vértice A en la esquina inferior izquierda con el ángulo α marcado en teal. "
            "El vértice B en la esquina superior derecha. Los lados etiquetados: 'a' (cateto vertical opuesto a α, lado derecho), 'b' (cateto horizontal adyacente a α, lado inferior), 'c' (hipotenusa, segmento diagonal en línea punteada que va de A a B). "
            "Pequeño cuadrado en el ángulo recto. Fondo blanco, líneas negras finas, etiquetas con tipografía matemática. " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Identidades fundamentales.**\n\n"
              "1. **Recíprocas:** $\\csc \\alpha = \\dfrac{1}{\\sin \\alpha}, \\;\\;\\sec \\alpha = \\dfrac{1}{\\cos \\alpha}, \\;\\;\\cot \\alpha = \\dfrac{1}{\\tan \\alpha}.$\n\n"
              "2. **Cociente:** $\\tan \\alpha = \\dfrac{\\sin \\alpha}{\\cos \\alpha}.$\n\n"
              "3. **Pitágoras:** $\\sin^2 \\alpha + \\cos^2 \\alpha = 1$. Dividiendo por $\\cos^2 \\alpha$ y por $\\sin^2 \\alpha$ se obtienen:\n"
              "$$\\tan^2 \\alpha + 1 = \\sec^2 \\alpha, \\qquad 1 + \\cot^2 \\alpha = \\csc^2 \\alpha.$$\n\n"
              "4. **Cofunción** (los ángulos agudos suman $90°$):\n"
              "$$\\sin(90° - \\alpha) = \\cos \\alpha, \\quad \\cos(90° - \\alpha) = \\sin \\alpha, \\quad \\tan(90° - \\alpha) = \\cot \\alpha.$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Valores exactos para ángulos notables.** Usando un triángulo "
              "equilátero (lado 2) y un isósceles rectángulo (catetos 1, 1) se obtienen:\n\n"
              "| Función | $30°$ | $45°$ | $60°$ |\n|---|---|---|---|\n"
              "| $\\sin$ | $\\frac{1}{2}$ | $\\frac{\\sqrt{2}}{2}$ | $\\frac{\\sqrt{3}}{2}$ |\n"
              "| $\\cos$ | $\\frac{\\sqrt{3}}{2}$ | $\\frac{\\sqrt{2}}{2}$ | $\\frac{1}{2}$ |\n"
              "| $\\tan$ | $\\frac{\\sqrt{3}}{3}$ | $1$ | $\\sqrt{3}$ |\n\n"
              "**Mnemotecnia:** los valores de $\\sin$ son $\\sqrt{1}/2, \\sqrt{2}/2, \\sqrt{3}/2$ "
              "(en orden de ángulo creciente); los de $\\cos$ son los mismos en orden inverso "
              "—consistente con la cofunción."
          )),

        b("ejemplo_resuelto",
          titulo="Resolver un triángulo rectángulo",
          problema_md=(
              "Resuelva el triángulo $ABC$ rectángulo en $C$, donde el ángulo "
              "$\\alpha = 30°$ y la hipotenusa $c = 12$."
          ),
          pasos=[
              {"accion_md": (
                  "Como los ángulos suman $180°$ y el ángulo en $C$ es $90°$:\n"
                  "$$\\angle B = 180° - 90° - 30° = 60°.$$"
               ),
               "justificacion_md": "Suma de ángulos interiores = 180°.",
               "es_resultado": False},
              {"accion_md": (
                  "Para el cateto $a$ (opuesto a $30°$), usamos $\\sin$:\n"
                  "$$\\sin(30°) = \\frac{a}{c} \\Rightarrow \\frac{1}{2} = \\frac{a}{12} \\Rightarrow a = 6.$$"
               ),
               "justificacion_md": "Despeje a partir de la definición.",
               "es_resultado": False},
              {"accion_md": (
                  "Para el cateto $b$ (adyacente a $30°$), usamos $\\cos$:\n"
                  "$$\\cos(30°) = \\frac{b}{c} \\Rightarrow \\frac{\\sqrt{3}}{2} = \\frac{b}{12} \\Rightarrow b = 6\\sqrt{3}.$$\n"
                  "**Solución completa:** $\\alpha = 30°$, $\\angle B = 60°$, $\\angle C = 90°$, $a = 6$, $b = 6\\sqrt{3}$, $c = 12$."
               ),
               "justificacion_md": "Triángulo completamente resuelto.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Asta de bandera (ángulos de elevación)",
          problema_md=(
              "Un asta de bandera está enclavada verticalmente en lo alto de un "
              "edificio. A $12$ m de distancia horizontal del edificio, los ángulos "
              "de elevación de la punta del asta y del techo del edificio son $60°$ y "
              "$30°$ respectivamente. Hallar la longitud del asta."
          ),
          pasos=[
              {"accion_md": (
                  "Sean $h$ = altura del edificio y $\\ell$ = longitud del asta. "
                  "Para la cima del edificio ($30°$):\n"
                  "$$\\tan(30°) = \\frac{h}{12} \\Rightarrow h = 12 \\cdot \\tfrac{\\sqrt{3}}{3} = 4\\sqrt{3} \\text{ m}.$$"
               ),
               "justificacion_md": "Aplicación de la tangente al primer triángulo.",
               "es_resultado": False},
              {"accion_md": (
                  "Para la punta del asta ($60°$, altura total $h + \\ell$):\n"
                  "$$\\tan(60°) = \\frac{h + \\ell}{12} \\Rightarrow \\sqrt{3} = \\frac{4\\sqrt{3} + \\ell}{12} \\Rightarrow 12\\sqrt{3} = 4\\sqrt{3} + \\ell.$$"
               ),
               "justificacion_md": "Aplicación al segundo triángulo, sustituyendo $h$.",
               "es_resultado": False},
              {"accion_md": "Despejando $\\ell$: $\\boxed{\\ell = 8\\sqrt{3} \\approx 13{,}86 \\text{ m}}.$",
               "justificacion_md": "Resta para aislar el asta.",
               "es_resultado": True},
          ]),

        ej(
            "Cateto desconocido con tan + Pitágoras",
            ("En un triángulo $ABC$ rectángulo en $C$, $\\tan(\\alpha) = \\dfrac{3}{\\sqrt{5}}$ "
             "y la hipotenusa $c = \\sqrt{70}$. Calcule el cateto $a$."),
            ["$\\tan(\\alpha) = a/b = 3/\\sqrt{5}$ sugiere parametrizar $a = 3k$, $b = \\sqrt{5}\\,k$.",
             "Aplicá Pitágoras: $a^2 + b^2 = c^2$ y despejá $k$.",
             "Sustituí $k$ en $a = 3k$."],
            ("Como $\\tan(\\alpha) = 3/\\sqrt{5}$ podemos escribir $a = 3k$, $b = \\sqrt{5}\\,k$ "
             "para algún $k > 0$. Por Pitágoras:\n"
             "$(3k)^2 + (\\sqrt{5}\\,k)^2 = (\\sqrt{70})^2 \\iff 9k^2 + 5k^2 = 70 \\iff 14k^2 = 70 \\iff k^2 = 5$, "
             "luego $k = \\sqrt{5}$. Por tanto $a = 3\\sqrt{5}$.")
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir cateto opuesto y adyacente.** Siempre referenciado al ángulo $\\alpha$ que se está usando.",
              "**Aplicar las razones a triángulos no rectángulos.** Estas definiciones requieren el ángulo recto. Para triángulos arbitrarios, ver lección 3.6.",
              "**Olvidar la identidad de Pitágoras al despejar.** Si conocés $\\sin$, podés calcular $\\cos$ por $\\sin^2 + \\cos^2 = 1$.",
              "**Mezclar grados y radianes.** En esta lección trabajamos en grados; en la próxima introducimos radianes.",
          ]),

        b("resumen",
          puntos_md=[
              "Las **seis razones** $\\sin, \\cos, \\tan, \\csc, \\sec, \\cot$ se definen sobre el triángulo rectángulo y dependen solo del ángulo.",
              "**Identidades fundamentales:** recíprocas, cociente, Pitágoras y cofunción.",
              "**Ángulos notables** $30°, 45°, 60°$ tienen valores exactos memorizables.",
              "Próxima lección: extender las funciones trigonométricas al **círculo unitario** y al dominio $\\mathbb{R}$.",
          ]),
    ]
    return {
        "id": "lec-ia-3-1-razones",
        "title": "Razones Trigonométricas",
        "description": "Las seis razones, identidades fundamentales, valores notables y resolución de triángulos rectángulos.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 1,
    }


# ============================================================================
# 3.2 Funciones trigonométricas
# ============================================================================
def lesson_3_2():
    blocks = [
        b("texto", body_md=(
            "Las **funciones trigonométricas** constituyen una de las familias más "
            "importantes de las matemáticas. Para definirlas como funciones de "
            "**números reales**, partimos de una idea elegante: medir ángulos no en "
            "grados, sino mediante **longitudes de arco** sobre la circunferencia "
            "unitaria. Esto da origen a la medida en **radianes**.\n\n"
            "En esta lección:\n\n"
            "- Definiremos **radián** y la conversión entre grados y radianes.\n"
            "- Definiremos $\\sin$ y $\\cos$ como funciones de $\\mathbb{R} \\to \\mathbb{R}$ vía la circunferencia unitaria.\n"
            "- Estudiaremos sus propiedades: **periodicidad, paridad** e **identidad pitagórica**.\n"
            "- Analizaremos las **gráficas** y las **funciones sinusoidales generales** $a\\sin(k(x-b))$.\n"
            "- Definiremos $\\tan, \\cot, \\sec, \\csc$ y sus dominios."
        )),

        b("definicion",
          titulo="Radián y conversión",
          body_md=(
              "La **circunferencia unitaria** es $x^2 + y^2 = 1$. Dado un punto $P$ "
              "sobre ella y $A = (1, 0)$, la **medida en radianes** del ángulo "
              "$\\angle AOP$ es la **longitud del arco** $AP$.\n\n"
              "Como la circunferencia completa mide $2\\pi$, los $360°$ corresponden "
              "a $2\\pi$ radianes. La conversión es:\n"
              "$$\\frac{\\text{radianes}}{\\text{grados}} = \\frac{\\pi}{180}.$$\n"
              "Para pasar grados → radianes: multiplicar por $\\dfrac{\\pi}{180}$. "
              "Para pasar radianes → grados: multiplicar por $\\dfrac{180}{\\pi}$."
          )),

        b("definicion",
          titulo="Las funciones seno y coseno",
          body_md=(
              "Sea $t \\in \\mathbb{R}$ y $P(x, y)$ el punto sobre la circunferencia "
              "unitaria determinado por $t$ (en radianes). Definimos:\n"
              "$$\\sin(t) = y, \\qquad \\cos(t) = x.$$\n"
              "Es decir, $\\sin(t)$ y $\\cos(t)$ son las **coordenadas** del punto sobre el círculo unitario.\n\n"
              "Esta definición extiende las razones del triángulo rectángulo a "
              "**todo número real** $t$, y reproduce los valores conocidos para "
              "ángulos agudos."
          )),

        fig(
            "Circunferencia unitaria centrada en el origen O. Eje X horizontal, eje Y vertical. Punto A = (1,0) marcado en el extremo derecho. "
            "Un punto P en el primer cuadrante sobre la circunferencia, etiquetado P(cos t, sen t). Línea desde O hasta P. Arco desde A hasta P en color teal con etiqueta 't' (longitud del arco = ángulo en radianes). "
            "Líneas punteadas desde P perpendiculares a los ejes mostrando: la altura (proyección sobre Y) etiquetada 'sen(t)' y la base (proyección sobre X) etiquetada 'cos(t)'. " + STYLE
        ),

        b("texto", body_md=(
            "**Valores especiales** (de triángulos $30$-$60$-$90$, $45$-$45$-$90$ y puntos axiales):\n\n"
            "| $t$ | $0$ | $\\frac{\\pi}{6}$ | $\\frac{\\pi}{4}$ | $\\frac{\\pi}{3}$ | $\\frac{\\pi}{2}$ |\n|---|---|---|---|---|---|\n"
            "| $\\sin(t)$ | $0$ | $\\frac{1}{2}$ | $\\frac{\\sqrt{2}}{2}$ | $\\frac{\\sqrt{3}}{2}$ | $1$ |\n"
            "| $\\cos(t)$ | $1$ | $\\frac{\\sqrt{3}}{2}$ | $\\frac{\\sqrt{2}}{2}$ | $\\frac{1}{2}$ | $0$ |\n\n"
            "**Signos por cuadrante:** I (ambos +), II ($\\sin +, \\cos -$), III (ambos −), IV ($\\sin -, \\cos +$)."
        )),

        b("teorema",
          enunciado_md=(
              "**Propiedades fundamentales.** Para todo $t \\in \\mathbb{R}$ y $k \\in \\mathbb{Z}$:\n\n"
              "1. **Periodicidad:** $\\sin(t + 2\\pi k) = \\sin(t)$ y $\\cos(t + 2\\pi k) = \\cos(t)$.\n\n"
              "2. **Paridad/imparidad:** $\\cos(-t) = \\cos(t)$ (par), $\\sin(-t) = -\\sin(t)$ (impar).\n\n"
              "3. **Identidad pitagórica:** $\\sin^2(t) + \\cos^2(t) = 1$ (porque $P$ está en el círculo unitario).\n\n"
              "4. **Recorrido:** $\\sin(t), \\cos(t) \\in [-1, 1]$ para todo $t$."
          )),

        b("ejemplo_resuelto",
          titulo="Cálculo de valores usando periodicidad e imparidad",
          problema_md=(
              "Calcule: (a) $\\cos\\!\\left(\\dfrac{2\\pi}{3}\\right)$, (b) $\\sin\\!\\left(\\dfrac{19\\pi}{4}\\right)$, "
              "(c) $\\sin\\!\\left(-\\dfrac{\\pi}{6}\\right)$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $\\frac{2\\pi}{3}$ está en el segundo cuadrante (cos < 0). "
                  "Su ángulo de referencia es $\\pi - \\frac{2\\pi}{3} = \\frac{\\pi}{3}$:\n"
                  "$$\\cos\\!\\left(\\tfrac{2\\pi}{3}\\right) = -\\cos\\!\\left(\\tfrac{\\pi}{3}\\right) = -\\tfrac{1}{2}.$$"
               ),
               "justificacion_md": "Cuadrante + ángulo de referencia.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Por periodicidad: $\\frac{19\\pi}{4} = \\frac{3\\pi}{4} + 2\\pi \\cdot 2$. Luego:\n"
                  "$$\\sin\\!\\left(\\tfrac{19\\pi}{4}\\right) = \\sin\\!\\left(\\tfrac{3\\pi}{4}\\right) = \\sin\\!\\left(\\pi - \\tfrac{\\pi}{4}\\right) = \\sin\\!\\left(\\tfrac{\\pi}{4}\\right) = \\tfrac{\\sqrt{2}}{2}.$$"
               ),
               "justificacion_md": "Periodicidad y simetría suplementaria del seno.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** Por imparidad: $\\sin\\!\\left(-\\frac{\\pi}{6}\\right) = -\\sin\\!\\left(\\frac{\\pi}{6}\\right) = -\\frac{1}{2}.$"
               ),
               "justificacion_md": "Aplicación de $\\sin(-t) = -\\sin(t)$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Identidad pitagórica + cuadrante",
          problema_md="Si $\\cos(t) = \\dfrac{3}{4}$ y $t$ está en el cuarto cuadrante, encuentre $\\sin(t)$.",
          pasos=[
              {"accion_md": (
                  "Por la identidad pitagórica: $\\sin^2(t) = 1 - \\cos^2(t) = 1 - \\dfrac{9}{16} = \\dfrac{7}{16}$, "
                  "luego $\\sin(t) = \\pm \\dfrac{\\sqrt{7}}{4}$."
               ),
               "justificacion_md": "Despeje desde la identidad.",
               "es_resultado": False},
              {"accion_md": (
                  "En el cuarto cuadrante la coordenada $y$ es **negativa**, por lo tanto:\n"
                  "$$\\boxed{\\sin(t) = -\\dfrac{\\sqrt{7}}{4}}.$$"
               ),
               "justificacion_md": "El cuadrante elimina la ambigüedad de signo.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Funciones sinusoidales generales",
          body_md=(
              "Las curvas $y = a \\sin\\bigl(k(x-b)\\bigr)$ con $a \\neq 0, k > 0$ tienen:\n\n"
              "- **Amplitud:** $|a|$ (distancia del eje al máximo/mínimo).\n"
              "- **Período:** $\\dfrac{2\\pi}{k}$ (longitud de un ciclo completo).\n"
              "- **Desfase:** $b$ (desplazamiento horizontal; positivo → derecha, negativo → izquierda).\n\n"
              "Un período completo se grafica sobre $\\bigl[b,\\, b + \\frac{2\\pi}{k}\\bigr]$."
          )),

        fig(
            "Dos paneles uno encima del otro con eje X de 0 a 4π. "
            "Panel superior: gráfica de y = sen(t) en color teal, oscilando entre -1 y 1, marcando claramente que cruza por 0 en 0, π, 2π, 3π, 4π; máximos en π/2 y 5π/2; mínimos en 3π/2 y 7π/2. Líneas punteadas grises horizontales en y=1 y y=-1. Etiqueta 'Período 2π' bajo el primer ciclo. "
            "Panel inferior: gráfica de y = cos(t) en color ámbar, mismas características pero desplazada (máximo en 0 y 2π, mínimo en π y 3π, ceros en π/2, 3π/2, 5π/2, 7π/2). " + STYLE
        ),

        b("definicion",
          titulo="Las cuatro funciones restantes",
          body_md=(
              "Definimos los conjuntos de dominio:\n"
              "$$A = \\{t \\in \\mathbb{R} : \\cos(t) \\neq 0\\} = \\mathbb{R} \\setminus \\left\\{\\tfrac{(2n+1)\\pi}{2} : n \\in \\mathbb{Z}\\right\\},$$\n"
              "$$B = \\{t \\in \\mathbb{R} : \\sin(t) \\neq 0\\} = \\mathbb{R} \\setminus \\{n\\pi : n \\in \\mathbb{Z}\\}.$$\n"
              "**Tangente** y **cotangente** (cocientes):\n"
              "$$\\tan(t) = \\frac{\\sin(t)}{\\cos(t)} \\quad (t \\in A), \\qquad \\cot(t) = \\frac{\\cos(t)}{\\sin(t)} \\quad (t \\in B).$$\n"
              "**Secante** y **cosecante** (recíprocas):\n"
              "$$\\sec(t) = \\frac{1}{\\cos(t)} \\quad (t \\in A), \\qquad \\csc(t) = \\frac{1}{\\sin(t)} \\quad (t \\in B).$$"
          )),

        ej(
            "Función sinusoidal general",
            ("Encuentre la amplitud, período y desfase de "
             "$y = 3 \\sin\\!\\left(2x - \\dfrac{\\pi}{2}\\right)$ y describa cómo "
             "se grafica un período completo."),
            ["Reescribí en la forma estándar $y = a \\sin(k(x-b))$ factorizando el coeficiente de $x$ adentro.",
             "Identificá $a$, $k$ y $b$ por inspección.",
             "El período es $2\\pi/k$ y el desfase es $b$."],
            ("Reescribiendo: $y = 3 \\sin\\!\\left(2(x - \\tfrac{\\pi}{4})\\right)$. "
             "Por tanto $a = 3$, $k = 2$, $b = \\pi/4$. **Amplitud** $= 3$, "
             "**período** $= 2\\pi / 2 = \\pi$, **desfase** $= \\pi/4$. "
             "Un período se grafica en $[\\pi/4, 5\\pi/4]$, con puntos clave en "
             "$\\pi/4$ (cero), $\\pi/2$ (máximo $3$), $3\\pi/4$ (cero), $\\pi$ (mínimo $-3$), $5\\pi/4$ (cero).")
        ),

        b("errores_comunes",
          items_md=[
              "**Mezclar grados y radianes.** Las propiedades en términos de $\\pi$ requieren radianes; en grados, $2\\pi \\to 360°$.",
              "**Olvidar el cuadrante al usar Pitágoras.** $\\sin^2 + \\cos^2 = 1$ deja signo ambiguo; el cuadrante lo decide.",
              "**Confundir período de $\\sin$ con el de $\\sin(kx)$.** El período se divide por $k$.",
              "**No factorizar correctamente al hallar desfase.** $y = \\sin(2x - \\pi/2) = \\sin(2(x - \\pi/4))$, no desfase $\\pi/2$.",
          ]),

        b("resumen",
          puntos_md=[
              "El **radián** mide ángulos como longitud de arco en el círculo unitario.",
              "$\\sin(t)$ y $\\cos(t)$ son las **coordenadas** del punto en el círculo unitario.",
              "Propiedades clave: **periodicidad** ($2\\pi$), **paridad/imparidad**, **pitágoras**, recorrido $[-1, 1]$.",
              "Las funciones sinusoidales $a\\sin(k(x-b))$ tienen amplitud $|a|$, período $2\\pi/k$ y desfase $b$.",
              "Próxima lección: las **identidades trigonométricas** (adición, ángulo doble, producto a suma).",
          ]),
    ]
    return {
        "id": "lec-ia-3-2-funciones",
        "title": "Funciones Trigonométricas",
        "description": "Radianes, definición vía círculo unitario, propiedades, gráficas y funciones sinusoidales generales.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# ============================================================================
# 3.3 Identidades trigonométricas
# ============================================================================
def lesson_3_3():
    blocks = [
        b("texto", body_md=(
            "Las **identidades trigonométricas** constituyen uno de los pilares "
            "fundamentales del álgebra. A diferencia de las **ecuaciones** "
            "trigonométricas (verdaderas solo para ciertos valores), las identidades "
            "se cumplen para **todo** valor del dominio. Su dominio permite "
            "simplificar expresiones complejas, demostrar nuevas identidades y "
            "resolver problemas en cálculo y física.\n\n"
            "En esta lección estudiaremos las cuatro familias de identidades clave:\n\n"
            "- **Adición y sustracción** (suma y resta de ángulos).\n"
            "- **Ángulo doble** y **bajar potencias**.\n"
            "- **Producto a suma**.\n"
            "- **Prostaféresis** (suma a producto)."
        )),

        b("teorema",
          enunciado_md=(
              "**Fórmulas de adición y sustracción.** Para $\\alpha, \\beta \\in \\mathbb{R}$:\n\n"
              "$$\\sin(\\alpha \\pm \\beta) = \\sin\\alpha \\cos\\beta \\pm \\cos\\alpha \\sin\\beta,$$\n"
              "$$\\cos(\\alpha \\pm \\beta) = \\cos\\alpha \\cos\\beta \\mp \\sin\\alpha \\sin\\beta,$$\n"
              "$$\\tan(\\alpha \\pm \\beta) = \\frac{\\tan\\alpha \\pm \\tan\\beta}{1 \\mp \\tan\\alpha \\tan\\beta}.$$\n\n"
              "**Idea de la demostración.** La fórmula clave es $\\cos(\\alpha - \\beta) = \\cos\\alpha\\cos\\beta + \\sin\\alpha\\sin\\beta$, que se "
              "deduce comparando dos cuerdas iguales en el círculo unitario. De ella, las demás se obtienen por cofunción y paridad."
          )),

        b("ejemplo_resuelto",
          titulo="Valores exactos en ángulos no estándar",
          problema_md=(
              "Calcule (a) $\\cos\\!\\left(\\dfrac{5\\pi}{12}\\right)$ y (b) $\\cos\\!\\left(\\dfrac{\\pi}{12}\\right)$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $\\frac{5\\pi}{12} = \\frac{\\pi}{4} + \\frac{\\pi}{6}$. Por suma:\n"
                  "$$\\cos\\!\\left(\\tfrac{5\\pi}{12}\\right) = \\cos\\tfrac{\\pi}{4}\\cos\\tfrac{\\pi}{6} - \\sin\\tfrac{\\pi}{4}\\sin\\tfrac{\\pi}{6} "
                  "= \\tfrac{\\sqrt{2}}{2}\\tfrac{\\sqrt{3}}{2} - \\tfrac{\\sqrt{2}}{2}\\tfrac{1}{2} = \\boxed{\\tfrac{\\sqrt{6} - \\sqrt{2}}{4}}.$$"
               ),
               "justificacion_md": "Descomposición en ángulos notables.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $\\frac{\\pi}{12} = \\frac{\\pi}{4} - \\frac{\\pi}{6}$. Por resta:\n"
                  "$$\\cos\\!\\left(\\tfrac{\\pi}{12}\\right) = \\cos\\tfrac{\\pi}{4}\\cos\\tfrac{\\pi}{6} + \\sin\\tfrac{\\pi}{4}\\sin\\tfrac{\\pi}{6} "
                  "= \\boxed{\\tfrac{\\sqrt{6} + \\sqrt{2}}{4}}.$$"
               ),
               "justificacion_md": "Mismo método con resta.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Fórmulas de ángulo doble.** Tomando $\\beta = \\alpha$ en las de adición:\n\n"
              "$$\\sin(2\\alpha) = 2\\sin\\alpha\\cos\\alpha,$$\n"
              "$$\\cos(2\\alpha) = \\cos^2\\alpha - \\sin^2\\alpha = 1 - 2\\sin^2\\alpha = 2\\cos^2\\alpha - 1,$$\n"
              "$$\\tan(2\\alpha) = \\frac{2\\tan\\alpha}{1 - \\tan^2\\alpha}.$$\n\n"
              "Las **tres formas** de $\\cos(2\\alpha)$ son útiles según el contexto."
          )),

        b("teorema",
          enunciado_md=(
              "**Fórmulas para bajar potencias** (despejes de las de ángulo doble):\n\n"
              "$$\\sin^2\\alpha = \\frac{1 - \\cos(2\\alpha)}{2}, \\qquad \\cos^2\\alpha = \\frac{1 + \\cos(2\\alpha)}{2}, \\qquad \\tan^2\\alpha = \\frac{1 - \\cos(2\\alpha)}{1 + \\cos(2\\alpha)}.$$\n\n"
              "Son **fundamentales en cálculo integral**: convierten $\\sin^2$ y $\\cos^2$ en funciones lineales del coseno de $2\\alpha$."
          )),

        b("ejemplo_resuelto",
          titulo="$\\cos(3x)$ en términos de $\\cos(x)$",
          problema_md="Escriba $\\cos(3x)$ como un polinomio en $\\cos(x)$.",
          pasos=[
              {"accion_md": (
                  "Descomponemos $3x = 2x + x$ y aplicamos la fórmula de adición del coseno:\n"
                  "$$\\cos(3x) = \\cos(2x)\\cos(x) - \\sin(2x)\\sin(x).$$"
               ),
               "justificacion_md": "Adición del coseno.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicamos $\\cos(2x) = 2\\cos^2 x - 1$ y $\\sin(2x) = 2\\sin x \\cos x$:\n"
                  "$$= (2\\cos^2 x - 1)\\cos x - 2\\sin^2 x \\cos x = 2\\cos^3 x - \\cos x - 2\\sin^2 x \\cos x.$$"
               ),
               "justificacion_md": "Sustitución de las fórmulas de ángulo doble.",
               "es_resultado": False},
              {"accion_md": (
                  "Usando $\\sin^2 x = 1 - \\cos^2 x$:\n"
                  "$$= 2\\cos^3 x - \\cos x - 2\\cos x(1 - \\cos^2 x) = \\boxed{4\\cos^3 x - 3\\cos x}.$$"
               ),
               "justificacion_md": "Reescritura final usando solo $\\cos x$.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Fórmulas de producto a suma.** Para $u, v \\in \\mathbb{R}$:\n\n"
              "$$\\sin u \\cos v = \\tfrac{1}{2}\\bigl[\\sin(u+v) + \\sin(u-v)\\bigr],$$\n"
              "$$\\cos u \\cos v = \\tfrac{1}{2}\\bigl[\\cos(u+v) + \\cos(u-v)\\bigr],$$\n"
              "$$\\sin u \\sin v = \\tfrac{1}{2}\\bigl[\\cos(u-v) - \\cos(u+v)\\bigr].$$\n\n"
              "Útiles para integrar productos de funciones trigonométricas."
          )),

        b("teorema",
          enunciado_md=(
              "**Fórmulas de prostaféresis (suma a producto).** Para $\\alpha, \\beta \\in \\mathbb{R}$:\n\n"
              "$$\\sin\\alpha + \\sin\\beta = 2 \\sin\\!\\left(\\tfrac{\\alpha+\\beta}{2}\\right) \\cos\\!\\left(\\tfrac{\\alpha-\\beta}{2}\\right),$$\n"
              "$$\\sin\\alpha - \\sin\\beta = 2 \\cos\\!\\left(\\tfrac{\\alpha+\\beta}{2}\\right) \\sin\\!\\left(\\tfrac{\\alpha-\\beta}{2}\\right),$$\n"
              "$$\\cos\\alpha + \\cos\\beta = 2 \\cos\\!\\left(\\tfrac{\\alpha+\\beta}{2}\\right) \\cos\\!\\left(\\tfrac{\\alpha-\\beta}{2}\\right),$$\n"
              "$$\\cos\\alpha - \\cos\\beta = -2 \\sin\\!\\left(\\tfrac{\\alpha+\\beta}{2}\\right) \\sin\\!\\left(\\tfrac{\\alpha-\\beta}{2}\\right).$$\n\n"
              "Son la inversa de las de producto a suma. Útiles para **factorizar** y simplificar cocientes."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar identidad encadenada",
          problema_md=(
              "Verifique la identidad $\\dfrac{\\sin(3x)}{\\sin(x)\\cos(x)} = 4\\cos(x) - \\sec(x).$"
          ),
          pasos=[
              {"accion_md": (
                  "Por el ejemplo anterior, $\\sin(3x) = \\sin(x)\\bigl(2\\cos^2 x + (1 - 2\\sin^2 x)\\bigr) = \\sin(x)(4\\cos^2 x - 1)$ "
                  "(reduciendo con $\\sin^2 x = 1 - \\cos^2 x$)."
               ),
               "justificacion_md": "Análoga al ejercicio anterior.",
               "es_resultado": False},
              {"accion_md": (
                  "Sustituimos en la fracción y cancelamos $\\sin(x)$:\n"
                  "$$\\frac{\\sin(x)(4\\cos^2 x - 1)}{\\sin(x)\\cos(x)} = \\frac{4\\cos^2 x - 1}{\\cos x} = 4\\cos x - \\frac{1}{\\cos x} = \\boxed{4\\cos x - \\sec x}. \\quad \\square$$"
               ),
               "justificacion_md": "Descomposición de la fracción.",
               "es_resultado": True},
          ]),

        ej(
            "Demostración con cofunción y ángulo doble",
            ("Demuestre que si $2\\alpha + \\beta = \\dfrac{\\pi}{2}$ entonces "
             "$\\cos^2(\\alpha) = \\dfrac{1 + \\sin\\beta}{2}$."),
            ["Despejá $2\\alpha = \\frac{\\pi}{2} - \\beta$.",
             "Aplicá la identidad de cofunción: $\\cos\\!\\left(\\frac{\\pi}{2} - \\beta\\right) = \\sin\\beta$.",
             "Usá $\\cos(2\\alpha) = 2\\cos^2\\alpha - 1$."],
            ("Si $2\\alpha + \\beta = \\frac{\\pi}{2}$, entonces $2\\alpha = \\frac{\\pi}{2} - \\beta$. "
             "Aplicando coseno y la cofunción $\\cos\\!\\left(\\frac{\\pi}{2}-\\beta\\right) = \\sin\\beta$:\n"
             "$\\cos(2\\alpha) = \\sin\\beta \\iff 2\\cos^2\\alpha - 1 = \\sin\\beta \\iff \\cos^2\\alpha = \\frac{1+\\sin\\beta}{2}.$ $\\square$")
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir signos en sustracción.** $\\cos(\\alpha - \\beta) = \\cos\\alpha\\cos\\beta + \\sin\\alpha\\sin\\beta$ (signo $+$, no $-$).",
              "**Aplicar $\\sin(2x) = 2\\sin x$.** ¡Error! Lo correcto es $\\sin(2x) = 2\\sin x \\cos x$.",
              "**Olvidar elegir la forma correcta de $\\cos(2x)$.** Las tres son útiles: elegí la que cancele lo que aparezca.",
              "**No factorizar el ángulo doble en problemas más complejos.** $\\sin(3x) = \\sin(2x + x)$ es la entrada estándar.",
          ]),

        b("resumen",
          puntos_md=[
              "**Adición/sustracción:** la base de todas las demás identidades.",
              "**Ángulo doble:** caso particular con $\\beta = \\alpha$. Tres formas para $\\cos(2\\alpha)$.",
              "**Bajar potencias:** despejes que convierten $\\sin^2, \\cos^2$ en funciones lineales (clave en integrales).",
              "**Producto a suma / Prostaféresis:** convierten productos en sumas y viceversa.",
              "Próxima lección: **funciones inversas** $\\arcsin, \\arccos, \\arctan$.",
          ]),
    ]
    return {
        "id": "lec-ia-3-3-identidades",
        "title": "Identidades Trigonométricas",
        "description": "Adición, sustracción, ángulo doble, bajar potencias, producto a suma y prostaféresis.",
        "blocks": blocks,
        "duration_minutes": 65,
        "order": 3,
    }


# ============================================================================
# 3.4 Funciones trigonométricas inversas
# ============================================================================
def lesson_3_4():
    blocks = [
        b("texto", body_md=(
            "Las funciones trigonométricas son **periódicas** y, por tanto, **no son "
            "inyectivas** en $\\mathbb{R}$. Para definir sus inversas debemos primero "
            "**restringir el dominio** a un intervalo donde sí sean inyectivas. Las "
            "funciones así obtenidas, llamadas **funciones inversas** o **funciones "
            "arco**, permiten recuperar ángulos a partir de razones trigonométricas.\n\n"
            "En esta lección:\n\n"
            "- Definiremos $\\arcsin$, $\\arccos$ y $\\arctan$ con sus dominios y recorridos.\n"
            "- Estudiaremos las **propiedades de cancelación**.\n"
            "- Aprenderemos la técnica del **triángulo rectángulo** para evaluar composiciones.\n"
            "- Demostraremos identidades clave como $\\arcsin(x) + \\arccos(x) = \\dfrac{\\pi}{2}$."
        )),

        b("definicion",
          titulo="Las tres funciones inversas",
          body_md=(
              "**$\\arcsin$:** restringimos $\\sin$ al intervalo $\\left[-\\frac{\\pi}{2}, \\frac{\\pi}{2}\\right]$ donde es estrictamente creciente.\n"
              "$$\\arcsin: [-1, 1] \\to \\left[-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}\\right], \\quad \\arcsin(y) = x \\iff \\sin(x) = y \\;\\land\\; -\\tfrac{\\pi}{2} \\le x \\le \\tfrac{\\pi}{2}.$$\n\n"
              "**$\\arccos$:** restringimos $\\cos$ al intervalo $[0, \\pi]$ donde es estrictamente decreciente.\n"
              "$$\\arccos: [-1, 1] \\to [0, \\pi], \\quad \\arccos(y) = x \\iff \\cos(x) = y \\;\\land\\; 0 \\le x \\le \\pi.$$\n\n"
              "**$\\arctan$:** restringimos $\\tan$ al intervalo abierto $\\left(-\\frac{\\pi}{2}, \\frac{\\pi}{2}\\right)$.\n"
              "$$\\arctan: \\mathbb{R} \\to \\left(-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}\\right), \\quad \\arctan(y) = x \\iff \\tan(x) = y \\;\\land\\; -\\tfrac{\\pi}{2} < x < \\tfrac{\\pi}{2}.$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Propiedades de cancelación.**\n\n"
              "$$\\sin(\\arcsin(x)) = x \\;\\;\\text{para } x \\in [-1, 1], \\quad \\arcsin(\\sin(x)) = x \\;\\;\\text{solo si } x \\in \\left[-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}\\right].$$\n"
              "$$\\cos(\\arccos(x)) = x \\;\\;\\text{para } x \\in [-1, 1], \\quad \\arccos(\\cos(x)) = x \\;\\;\\text{solo si } x \\in [0, \\pi].$$\n"
              "$$\\tan(\\arctan(x)) = x \\;\\;\\text{para todo } x \\in \\mathbb{R}, \\quad \\arctan(\\tan(x)) = x \\;\\;\\text{solo si } x \\in \\left(-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}\\right).$$\n\n"
              "**Cuidado:** las cancelaciones de la forma $f^{-1}(f(x))$ **no valen siempre**. Si $x$ cae fuera del rango, hay que reducirlo primero al ángulo equivalente dentro del rango."
          )),

        b("ejemplo_resuelto",
          titulo="Cancelaciones del arcsen y arccos",
          problema_md=(
              "Calcule (a) $\\arcsin\\!\\left(\\sin\\!\\left(\\dfrac{2\\pi}{3}\\right)\\right)$, (b) $\\arccos\\!\\left(\\cos\\!\\left(\\dfrac{5\\pi}{3}\\right)\\right)$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Como $\\frac{2\\pi}{3} \\notin \\left[-\\frac{\\pi}{2}, \\frac{\\pi}{2}\\right]$, no se cancela directamente. "
                  "Buscamos el ángulo en el rango con el mismo seno: $\\sin\\!\\left(\\frac{2\\pi}{3}\\right) = \\sin\\!\\left(\\pi - \\frac{2\\pi}{3}\\right) = \\sin\\!\\left(\\frac{\\pi}{3}\\right) = \\frac{\\sqrt{3}}{2}$. "
                  "Como $\\frac{\\pi}{3} \\in \\left[-\\frac{\\pi}{2}, \\frac{\\pi}{2}\\right]$:\n"
                  "$$\\arcsin\\!\\left(\\sin\\!\\left(\\tfrac{2\\pi}{3}\\right)\\right) = \\boxed{\\tfrac{\\pi}{3}}.$$"
               ),
               "justificacion_md": "Reducimos al rango usando la simetría $\\sin(\\pi - x) = \\sin x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $\\frac{5\\pi}{3} \\notin [0, \\pi]$. Calculamos $\\cos\\!\\left(\\frac{5\\pi}{3}\\right) = \\cos\\!\\left(2\\pi - \\frac{\\pi}{3}\\right) = \\cos\\!\\left(\\frac{\\pi}{3}\\right) = \\frac{1}{2}$. "
                  "Como $\\frac{\\pi}{3} \\in [0, \\pi]$:\n"
                  "$$\\arccos\\!\\left(\\cos\\!\\left(\\tfrac{5\\pi}{3}\\right)\\right) = \\boxed{\\tfrac{\\pi}{3}}.$$"
               ),
               "justificacion_md": "Paridad del coseno + reducción al rango.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Técnica del triángulo rectángulo",
          body_md=(
              "Para evaluar $f(g^{-1}(x))$ donde $f, g$ son trigonométricas, se "
              "**dibuja un triángulo rectángulo** que realice la condición impuesta "
              "por la inversa. A partir de él se leen directamente todas las razones.\n\n"
              "**Procedimiento:** Para evaluar $\\cos(\\arcsin(a))$, sea $\\theta = \\arcsin(a)$. "
              "Entonces $\\sin(\\theta) = a$ con $\\theta \\in \\left[-\\frac{\\pi}{2}, \\frac{\\pi}{2}\\right]$. Se traza un triángulo "
              "rectángulo de cateto opuesto $a$, hipotenusa $1$. El cateto adyacente "
              "se obtiene por Pitágoras: $\\sqrt{1 - a^2}$. El signo lo decide el rango."
          )),

        b("ejemplo_resuelto",
          titulo="Composición con triángulo rectángulo",
          problema_md="Calcule $\\cos\\!\\left(\\arcsin\\!\\left(\\dfrac{\\sqrt{3}}{2}\\right)\\right)$.",
          pasos=[
              {"accion_md": (
                  "Sea $\\theta = \\arcsin\\!\\left(\\frac{\\sqrt{3}}{2}\\right)$, de modo que $\\sin(\\theta) = \\frac{\\sqrt{3}}{2}$ con "
                  "$\\theta \\in \\left[-\\frac{\\pi}{2}, \\frac{\\pi}{2}\\right]$. Triángulo: cateto opuesto $\\sqrt{3}$, hipotenusa $2$."
               ),
               "justificacion_md": "Construcción del triángulo a partir de la condición.",
               "es_resultado": False},
              {"accion_md": (
                  "Cateto adyacente $= \\sqrt{2^2 - (\\sqrt{3})^2} = \\sqrt{1} = 1$. Como $\\theta$ está en el rango "
                  "$\\left[-\\frac{\\pi}{2}, \\frac{\\pi}{2}\\right]$, $\\cos(\\theta) > 0$:\n"
                  "$$\\cos(\\theta) = \\frac{1}{2}.$$\n"
                  "(Coincide con $\\arcsin(\\sqrt{3}/2) = \\pi/3$ y $\\cos(\\pi/3) = 1/2$.) $\\boxed{\\frac{1}{2}}$"
               ),
               "justificacion_md": "Pitágoras + signo del rango.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Composición con ángulo doble",
          problema_md="Calcule $\\sin\\!\\left(2 \\arccos\\!\\left(\\dfrac{3}{5}\\right)\\right)$.",
          pasos=[
              {"accion_md": (
                  "Sea $\\theta = \\arccos(3/5)$, así $\\cos\\theta = 3/5$ con $\\theta \\in [0, \\pi]$. "
                  "Triángulo: cateto adyacente $3$, hipotenusa $5$, cateto opuesto $\\sqrt{25 - 9} = 4$."
               ),
               "justificacion_md": "Construcción del triángulo (3-4-5).",
               "es_resultado": False},
              {"accion_md": (
                  "Como $\\theta \\in [0, \\pi]$, $\\sin\\theta \\ge 0$, así $\\sin\\theta = 4/5$. Aplicando ángulo doble:\n"
                  "$$\\sin(2\\theta) = 2 \\sin\\theta \\cos\\theta = 2 \\cdot \\tfrac{4}{5} \\cdot \\tfrac{3}{5} = \\boxed{\\tfrac{24}{25}}.$$"
               ),
               "justificacion_md": "Sustitución en $\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Expresar $\\cos(\\arctan(x))$ en términos de $x$",
          problema_md="Exprese $\\cos(\\arctan(x))$ como función algebraica de $x$, sin trigonometría.",
          pasos=[
              {"accion_md": (
                  "Sea $y = \\arctan(x)$, $\\tan(y) = x$ con $y \\in \\left(-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}\\right)$. Por la pitagórica de la tangente:\n"
                  "$$\\tan^2 y + 1 = \\sec^2 y \\Rightarrow 1 + x^2 = \\sec^2 y \\Rightarrow \\cos^2 y = \\frac{1}{1 + x^2}.$$"
               ),
               "justificacion_md": "Identidad pitagórica para tangente y secante.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $y \\in \\left(-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}\\right)$, $\\cos y > 0$, así:\n"
                  "$$\\cos(\\arctan(x)) = \\boxed{\\frac{1}{\\sqrt{1 + x^2}}}.$$"
               ),
               "justificacion_md": "Signo decidido por el rango de $\\arctan$.",
               "es_resultado": True},
          ]),

        ej(
            "Identidad fundamental entre arcsin y arccos",
            ("Demuestre que para todo $x \\in [-1, 1]$:\n\n"
             "$$\\arcsin(x) + \\arccos(x) = \\frac{\\pi}{2}.$$"),
            ["Sea $\\alpha = \\frac{\\pi}{2} - \\arcsin(x)$. Calculá $\\cos(\\alpha)$ usando cofunción.",
             "Usá $\\cos\\!\\left(\\frac{\\pi}{2} - \\theta\\right) = \\sin(\\theta)$.",
             "Verificá que $\\alpha \\in [0, \\pi]$ para concluir $\\alpha = \\arccos(x)$."],
            ("Sea $\\alpha = \\frac{\\pi}{2} - \\arcsin(x)$. Por cofunción: "
             "$\\cos(\\alpha) = \\cos\\!\\left(\\frac{\\pi}{2} - \\arcsin(x)\\right) = \\sin(\\arcsin(x)) = x$. "
             "Como $\\arcsin(x) \\in [-\\pi/2, \\pi/2]$, $\\alpha \\in [0, \\pi]$. Por la definición de $\\arccos$, "
             "$\\alpha = \\arccos(x)$, es decir, $\\frac{\\pi}{2} - \\arcsin(x) = \\arccos(x)$, lo que da el resultado. $\\square$")
        ),

        b("errores_comunes",
          items_md=[
              "**Asumir cancelación en cualquier dirección.** $\\sin(\\arcsin x) = x$ siempre que $|x| \\le 1$, pero $\\arcsin(\\sin x) = x$ solo si $x \\in [-\\pi/2, \\pi/2]$.",
              "**Olvidar el signo en triángulos.** El rango de la inversa decide el signo de las funciones derivadas.",
              "**Confundir $\\arcsin$ con $\\sin^{-1}$ y con $\\csc$.** $\\sin^{-1}$ y $\\arcsin$ son lo mismo; $\\csc = 1/\\sin$ es distinto.",
              "**Suponer que $\\arctan$ tiene rango $[0, \\pi]$.** Tiene rango $(-\\pi/2, \\pi/2)$.",
          ]),

        b("resumen",
          puntos_md=[
              "$\\arcsin: [-1,1] \\to [-\\pi/2, \\pi/2]$, $\\arccos: [-1,1] \\to [0, \\pi]$, $\\arctan: \\mathbb{R} \\to (-\\pi/2, \\pi/2)$.",
              "**Cancelaciones:** $f(f^{-1}(x)) = x$ siempre; $f^{-1}(f(x)) = x$ solo dentro del rango restringido.",
              "**Triángulo rectángulo:** la herramienta más práctica para evaluar composiciones.",
              "**Identidad clave:** $\\arcsin(x) + \\arccos(x) = \\pi/2$.",
              "Próxima lección: **ecuaciones trigonométricas** y técnicas para resolverlas usando todo lo aprendido.",
          ]),
    ]
    return {
        "id": "lec-ia-3-4-inversas",
        "title": "Funciones Trigonométricas Inversas",
        "description": "arcsen, arccos, arctan: dominios, recorridos, cancelación y composiciones con triángulo rectángulo.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# ============================================================================
# 3.5 Ecuaciones trigonométricas
# ============================================================================
def lesson_3_5():
    blocks = [
        b("texto", body_md=(
            "Las **ecuaciones trigonométricas** son ecuaciones donde las incógnitas "
            "aparecen únicamente en los argumentos de las funciones trigonométricas. "
            "A diferencia de las ecuaciones algebraicas ordinarias, presentan una "
            "característica fundamental: debido a la **periodicidad**, si $x_0$ es "
            "una solución, entonces $x_0 + 2\\pi k$ también lo es para todo "
            "$k \\in \\mathbb{Z}$. Esto significa que toda ecuación trigonométrica "
            "con solución tiene **infinitas soluciones**.\n\n"
            "La estrategia consiste en encontrar primero las **soluciones básicas** "
            "en el intervalo $[0, 2\\pi)$, y luego describir el conjunto solución "
            "completo mediante la periodicidad."
        )),

        b("teorema",
          enunciado_md=(
              "**Soluciones de las ecuaciones elementales.**\n\n"
              "1. Para $\\sin(x) = a$ con $a \\in [-1, 1]$:\n"
              "$$S = \\{k\\pi + (-1)^k \\alpha \\mid k \\in \\mathbb{Z}\\}$$\n"
              "donde $\\alpha$ es la solución básica en el primer o cuarto cuadrante.\n\n"
              "2. Para $\\cos(x) = b$ con $b \\in [-1, 1]$:\n"
              "$$S = \\{2k\\pi \\pm \\alpha \\mid k \\in \\mathbb{Z}\\}$$\n"
              "donde $\\alpha$ es la solución básica en el primer o segundo cuadrante.\n\n"
              "3. Para $\\tan(x) = c$ con $c \\in \\mathbb{R}$:\n"
              "$$S = \\{k\\pi + \\gamma \\mid k \\in \\mathbb{Z}\\}$$\n"
              "donde $\\gamma$ es la solución básica en el primer o cuarto cuadrante. "
              "(La tangente tiene período $\\pi$, no $2\\pi$.)"
          )),

        b("intuicion", body_md=(
            "**¿Por qué estas formas?** En $[0, 2\\pi)$, el seno toma cada valor en "
            "**dos** ángulos $\\alpha$ y $\\pi - \\alpha$; el coseno también en **dos** "
            "ángulos $\\alpha$ y $-\\alpha$ (módulo $2\\pi$); la tangente toma cada "
            "valor en **dos** ángulos que difieren en $\\pi$ (por su período).\n\n"
            "La fórmula $(-1)^k \\alpha$ del seno alterna entre $\\alpha$ y $-\\alpha$ "
            "según la paridad de $k$, capturando así todas las soluciones."
        )),

        b("ejemplo_resuelto",
          titulo="Reducir con ángulo doble y factorizar",
          problema_md="Determine las soluciones de $\\sin(x) = \\sin(2x)$.",
          pasos=[
              {"accion_md": (
                  "Usando $\\sin(2x) = 2\\sin x \\cos x$, la ecuación se convierte en:\n"
                  "$$\\sin x = 2\\sin x \\cos x \\iff \\sin x (1 - 2\\cos x) = 0,$$\n"
                  "lo cual ocurre si y solo si $\\sin x = 0$ o $\\cos x = \\frac{1}{2}$."
               ),
               "justificacion_md": "Identidad de ángulo doble + factorización.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 1:** $\\sin x = 0$ tiene solución básica $\\alpha = 0$, así $S_1 = \\{k\\pi \\mid k \\in \\mathbb{Z}\\}$."
               ),
               "justificacion_md": "Aplicación directa de la fórmula del seno.",
               "es_resultado": False},
              {"accion_md": (
                  "**Caso 2:** $\\cos x = \\frac{1}{2}$ tiene solución básica $\\alpha = \\frac{\\pi}{3}$ (primer cuadrante), "
                  "así $S_2 = \\left\\{2k\\pi \\pm \\frac{\\pi}{3} \\mid k \\in \\mathbb{Z}\\right\\}$.\n\n"
                  "**Conjunto solución total:** $S = S_1 \\cup S_2$."
               ),
               "justificacion_md": "Unión de los conjuntos por cada caso del producto cero.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Ecuación cuadrática en una función trigonométrica",
          problema_md="Resuelva $2\\cos^2(\\theta) - 7\\cos(\\theta) + 3 = 0$.",
          pasos=[
              {"accion_md": (
                  "Sea $u = \\cos\\theta$. La ecuación es $2u^2 - 7u + 3 = 0$, que se factoriza como:\n"
                  "$$(2u - 1)(u - 3) = 0 \\iff u = \\tfrac{1}{2} \\;\\lor\\; u = 3.$$"
               ),
               "justificacion_md": "Tratamos como cuadrática y factorizamos.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\cos\\theta = 3$ **no tiene solución real** pues $\\cos\\theta \\in [-1, 1]$. "
                  "Solo queda $\\cos\\theta = \\frac{1}{2}$."
               ),
               "justificacion_md": "Filtramos por el recorrido del coseno.",
               "es_resultado": False},
              {"accion_md": (
                  "Solución básica: $\\alpha = \\frac{\\pi}{3}$. Por la fórmula del coseno:\n"
                  "$$\\boxed{S = \\left\\{2k\\pi \\pm \\tfrac{\\pi}{3} \\mid k \\in \\mathbb{Z}\\right\\}}.$$"
               ),
               "justificacion_md": "Aplicación directa de la fórmula.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Reducir todo a tangente",
          problema_md=(
              "Determine las soluciones de $(1 - \\tan(x))(\\sin(2x) + 1) = 1 + \\tan(x)$."
          ),
          pasos=[
              {"accion_md": (
                  "Reescribimos $\\sin(2x) + 1$ en términos de $\\tan x$ usando $\\sin(2x) = \\frac{2\\tan x}{1 + \\tan^2 x}$:\n"
                  "$$\\sin(2x) + 1 = \\frac{2\\tan x + 1 + \\tan^2 x}{1 + \\tan^2 x} = \\frac{(1 + \\tan x)^2}{1 + \\tan^2 x}.$$"
               ),
               "justificacion_md": "Manipulación con identidad universal de la tangente.",
               "es_resultado": False},
              {"accion_md": (
                  "Sustituyendo y multiplicando por $(1 + \\tan^2 x)$:\n"
                  "$$(1 - \\tan x)(1 + \\tan x)^2 = (1 + \\tan x)(1 + \\tan^2 x).$$\n"
                  "Factorizando $(1 + \\tan x)$:\n"
                  "$$(1 + \\tan x)\\bigl[(1 - \\tan x)(1 + \\tan x) - (1 + \\tan^2 x)\\bigr] = 0.$$"
               ),
               "justificacion_md": "Trasponemos y factorizamos el factor común.",
               "es_resultado": False},
              {"accion_md": (
                  "El corchete: $(1 - \\tan^2 x) - (1 + \\tan^2 x) = -2\\tan^2 x$. Luego:\n"
                  "$$(1 + \\tan x)(-2\\tan^2 x) = 0 \\iff \\tan x = -1 \\;\\lor\\; \\tan x = 0.$$\n"
                  "Soluciones: $x = k\\pi - \\frac{\\pi}{4}$ o $x = k\\pi$, $k \\in \\mathbb{Z}$.\n"
                  "$$\\boxed{S = \\{k\\pi \\mid k \\in \\mathbb{Z}\\} \\cup \\left\\{k\\pi - \\tfrac{\\pi}{4} \\mid k \\in \\mathbb{Z}\\right\\}}.$$"
               ),
               "justificacion_md": "Diferencia de cuadrados y aplicación de la fórmula de la tangente.",
               "es_resultado": True},
          ]),

        ej(
            "Ecuación con $\\cos$ del doble",
            ("Resuelva $\\cos(2x) = \\sin(x)$ encontrando todas las soluciones en $\\mathbb{R}$."),
            ["Usá $\\cos(2x) = 1 - 2\\sin^2 x$ para obtener una cuadrática en $\\sin x$.",
             "Aparecerá $2\\sin^2 x + \\sin x - 1 = 0$. Factorizá.",
             "Resolvé cada caso elemental con las fórmulas del seno."],
            ("Sustituyendo $\\cos(2x) = 1 - 2\\sin^2 x$: $1 - 2\\sin^2 x = \\sin x \\iff 2\\sin^2 x + \\sin x - 1 = 0$. "
             "Factorizando: $(2\\sin x - 1)(\\sin x + 1) = 0$, así $\\sin x = \\frac{1}{2}$ o $\\sin x = -1$.\n\n"
             "Caso 1: $\\sin x = \\frac{1}{2}$, $\\alpha = \\frac{\\pi}{6}$, $S_1 = \\left\\{k\\pi + (-1)^k \\frac{\\pi}{6} \\mid k \\in \\mathbb{Z}\\right\\}$.\n\n"
             "Caso 2: $\\sin x = -1$, $\\alpha = -\\frac{\\pi}{2}$, $S_2 = \\left\\{2k\\pi - \\frac{\\pi}{2} \\mid k \\in \\mathbb{Z}\\right\\} = \\left\\{\\frac{3\\pi}{2} + 2k\\pi \\mid k \\in \\mathbb{Z}\\right\\}$.\n\n"
             "Conjunto total: $S = S_1 \\cup S_2$.")
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar todas las soluciones por periodicidad.** Resolver solo en $[0, 2\\pi)$ y no incluir el $+2k\\pi$ es perder información.",
              "**Dividir por una función trigonométrica que puede ser cero.** Esto borra soluciones. Mejor factorizar.",
              "**Aceptar valores fuera del recorrido.** $\\cos x = 3$ no tiene solución; $\\arcsin(2)$ no existe.",
              "**Confundir período de tangente.** $\\tan$ tiene período $\\pi$, no $2\\pi$.",
          ]),

        b("resumen",
          puntos_md=[
              "Toda ecuación trigonométrica con solución tiene **infinitas soluciones** por periodicidad.",
              "**Estrategia:** identidades para simplificar → factorizar → resolver ecuaciones elementales.",
              "**Tres formas básicas:** $\\sin x = a$, $\\cos x = b$, $\\tan x = c$, cada una con su fórmula del conjunto solución.",
              "Verificá siempre que las soluciones pertenezcan al **dominio** (en particular, evitar $\\frac{\\pi}{2} + k\\pi$ para tangente).",
              "Próxima lección: **Teoremas del Seno y del Coseno** para resolver triángulos arbitrarios.",
          ]),
    ]
    return {
        "id": "lec-ia-3-5-ecuaciones",
        "title": "Ecuaciones Trigonométricas",
        "description": "Soluciones básicas, periodicidad, fórmulas para sen=a, cos=b, tan=c y técnicas de factorización.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 5,
    }


# ============================================================================
# 3.6 Teorema del seno y coseno
# ============================================================================
def lesson_3_6():
    blocks = [
        b("texto", body_md=(
            "El estudio de los **triángulos arbitrarios** —no necesariamente "
            "rectángulos— requiere herramientas que vayan más allá del Teorema de "
            "Pitágoras. El **Teorema del Seno** y el **Teorema del Coseno** son las "
            "dos relaciones fundamentales que permiten resolver cualquier triángulo "
            "conociendo información parcial sobre sus lados y ángulos.\n\n"
            "Estas herramientas tienen aplicaciones directas en **topografía**, "
            "**navegación**, **astronomía** e **ingeniería**, como veremos en los "
            "ejemplos. Cierran el capítulo de trigonometría conectando todas las "
            "lecciones anteriores."
        )),

        b("teorema",
          enunciado_md=(
              "**Área de un triángulo.** El área de un triángulo con dos lados de "
              "longitudes $a$ y $b$ y ángulo entre ellos $\\theta$ es:\n"
              "$$A = \\tfrac{1}{2}\\, ab \\sin(\\theta).$$\n\n"
              "**Demostración:** Si $\\theta$ es agudo, la altura desde el vértice opuesto al lado $a$ "
              "satisface $h = b \\sin\\theta$ (definición de seno). Por tanto $A = \\frac{1}{2}\\,ah = \\frac{1}{2}\\,ab\\sin\\theta$. "
              "Si $\\theta$ es obtuso, la altura exterior cumple $h = b\\sin(\\pi - \\theta) = b\\sin\\theta$ (cofunción de suplemento), "
              "y se llega a la misma fórmula. $\\blacksquare$"
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema del Seno.** En todo triángulo $ABC$ con lados $a, b, c$ "
              "opuestos a los ángulos $\\alpha, \\beta, \\gamma$ respectivamente:\n"
              "$$\\boxed{\\;\\frac{\\sin\\alpha}{a} = \\frac{\\sin\\beta}{b} = \\frac{\\sin\\gamma}{c}\\;}$$\n\n"
              "**Demostración:** El área del triángulo se expresa de tres maneras: "
              "$A = \\frac{1}{2} bc\\sin\\alpha = \\frac{1}{2} ac\\sin\\beta = \\frac{1}{2} ab\\sin\\gamma$. "
              "Multiplicando las tres por $\\frac{2}{abc}$ se obtiene el teorema. $\\blacksquare$"
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema del Coseno.** En todo triángulo $ABC$ se cumple:\n"
              "$$a^2 = b^2 + c^2 - 2bc\\cos\\alpha,$$\n"
              "$$b^2 = a^2 + c^2 - 2ac\\cos\\beta,$$\n"
              "$$c^2 = a^2 + b^2 - 2ab\\cos\\gamma.$$\n\n"
              "**Generaliza el Teorema de Pitágoras:** si $\\alpha = 90°$, $\\cos\\alpha = 0$ y se recupera $a^2 = b^2 + c^2$.\n\n"
              "**Demostración (forma a):** se ubica $A$ en el origen, $B = (c, 0)$, "
              "$C = (b\\cos\\alpha, b\\sin\\alpha)$. Calculando $a^2 = |BC|^2$ y "
              "aplicando $\\sin^2\\alpha + \\cos^2\\alpha = 1$ se obtiene la fórmula."
          )),

        fig(
            "Triángulo arbitrario ABC en color teal, no rectángulo, con vértices etiquetados A (esquina inferior izquierda), B (esquina inferior derecha), C (vértice superior, ligeramente desplazado hacia la izquierda). "
            "Los ángulos interiores etiquetados con letras griegas: α en A, β en B, γ en C. Los lados opuestos etiquetados con minúsculas: a en el lado BC (frente a α), b en el lado AC (frente a β), c en el lado AB (frente a γ). "
            "Líneas auxiliares punteadas mostrando la altura desde C al lado AB (altura h del Teorema del Área). " + STYLE
        ),

        b("definicion",
          titulo="Criterios de resolución de triángulos",
          body_md=(
              "Según qué información se conozca, se elige el teorema apropiado:\n\n"
              "- **ALA** (ángulo-lado-ángulo): se conocen dos ángulos y el lado "
              "comprendido. → Tercer ángulo por suma $180°$, lados restantes por **Seno**.\n"
              "- **AAL** (ángulo-ángulo-lado): dos ángulos y un lado no comprendido. → Igual.\n"
              "- **LAL** (lado-ángulo-lado): dos lados y el ángulo entre ellos. → "
              "Tercer lado por **Coseno**, luego ángulos por Seno.\n"
              "- **LLL** (lado-lado-lado): los tres lados. → Ángulos por **Coseno**."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicación: el túnel de la montaña (LAL → Coseno)",
          problema_md=(
              "Para estimar la longitud de un túnel a través de una montaña, un "
              "topógrafo mide desde un punto exterior $C$ las distancias hasta las "
              "dos bocas $A$ y $B$: $CA = 12$ m, $CB = 10$ m, y el ángulo "
              "$\\angle ACB = 60°$. Aproxime la longitud $AB$."
          ),
          pasos=[
              {"accion_md": (
                  "Datos del triángulo $ABC$: $b = CA = 12$, $a = CB = 10$, $\\gamma = 60°$, $c = AB$ (incógnita). "
                  "Aplicamos el Teorema del Coseno en su tercera forma:\n"
                  "$$c^2 = a^2 + b^2 - 2ab\\cos\\gamma.$$"
               ),
               "justificacion_md": "LAL ⟹ Teorema del Coseno.",
               "es_resultado": False},
              {"accion_md": (
                  "Sustituyendo: $c^2 = 100 + 144 - 240 \\cdot \\cos(60°) = 244 - 240 \\cdot \\tfrac{1}{2} = 124.$"
               ),
               "justificacion_md": "Cálculo directo con $\\cos 60° = 1/2$.",
               "es_resultado": False},
              {"accion_md": "$c = \\sqrt{124} = 2\\sqrt{31} \\approx \\boxed{11{,}14 \\text{ m}}.$",
               "justificacion_md": "Raíz cuadrada y simplificación.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Aplicación: satélite sobre Chile (AAL → Seno)",
          problema_md=(
              "Un satélite que gira en órbita pasa directamente sobre las estaciones "
              "de La Serena y Santiago, separadas por $550$ km. En un instante en que "
              "el satélite $S$ está entre ambas, su ángulo de elevación es de $60°$ "
              "desde La Serena ($L$) y $75°$ desde Santiago ($T$). ¿A qué distancia "
              "está el satélite de Santiago?"
          ),
          pasos=[
              {"accion_md": (
                  "Modelamos con el triángulo $LST$. Datos: $LT = 550$ km (lado entre "
                  "estaciones), $\\angle SLT = 60°$, $\\angle STL = 75°$. **Paso 1:** "
                  "$\\angle LST = 180° - 60° - 75° = 45°.$"
               ),
               "justificacion_md": "Suma de ángulos interiores.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2:** Buscamos $ST$ (opuesto al ángulo en $L$). $LT$ es opuesto al ángulo en $S$. "
                  "Por el Teorema del Seno:\n"
                  "$$\\frac{ST}{\\sin 60°} = \\frac{550}{\\sin 45°}.$$"
               ),
               "justificacion_md": "AAL ⟹ Teorema del Seno.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3:** despejando:\n"
                  "$$ST = \\frac{550 \\cdot \\sin 60°}{\\sin 45°} = \\frac{550 \\cdot \\sqrt{3}/2}{\\sqrt{2}/2} = 550\\sqrt{\\tfrac{3}{2}} = 275\\sqrt{6} \\approx \\boxed{673{,}0 \\text{ km}}.$$"
               ),
               "justificacion_md": "Algebra y aproximación numérica final.",
               "es_resultado": True},
          ]),

        ej(
            "Resolución de triángulo LLL",
            ("Un triángulo tiene lados $a = 7$, $b = 8$, $c = 9$. Encuentre el "
             "ángulo $\\gamma$ opuesto al lado $c$, expresado como $\\arccos$ de un "
             "número exacto."),
            ["Como tenemos los tres lados (LLL), aplicá el Teorema del Coseno: $c^2 = a^2 + b^2 - 2ab\\cos\\gamma$.",
             "Despejá $\\cos\\gamma$.",
             "Sustituí los valores y simplificá la fracción."],
            ("Por el Teorema del Coseno: $81 = 49 + 64 - 2 \\cdot 7 \\cdot 8 \\cos\\gamma = 113 - 112\\cos\\gamma$. "
             "Despejando: $112\\cos\\gamma = 32 \\iff \\cos\\gamma = \\frac{32}{112} = \\frac{2}{7}$. "
             "Por tanto $\\gamma = \\arccos\\!\\left(\\frac{2}{7}\\right) \\approx 73{,}4°$.")
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Pitágoras en triángulos no rectángulos.** Solo vale en rectángulos; el Coseno generaliza.",
              "**Confundir $\\sin\\alpha / a$ vs. $a / \\sin\\alpha$.** Ambas formas valen, pero hay que usar la misma a ambos lados.",
              "**Olvidar que el seno es positivo en $(0, \\pi)$.** Esto puede dar dos triángulos posibles en algunos casos AAL.",
              "**Mezclar grados y radianes en la calculadora.** Verificá el modo antes de evaluar.",
          ]),

        b("resumen",
          puntos_md=[
              "**Área:** $A = \\frac{1}{2} ab \\sin\\theta$ — generalización del «base por altura sobre 2».",
              "**Teorema del Seno:** $\\sin\\alpha / a = \\sin\\beta / b = \\sin\\gamma / c$. Útil para AAL/ALA.",
              "**Teorema del Coseno:** $a^2 = b^2 + c^2 - 2bc\\cos\\alpha$. Útil para LAL/LLL. Generaliza Pitágoras.",
              "Identificá el caso (ALA, AAL, LAL, LLL) antes de elegir el teorema.",
              "**Cierre del capítulo:** ya dominás trigonometría completa. Próximo capítulo: **polinomios complejos**, donde extenderemos el álgebra al campo $\\mathbb{C}$.",
          ]),
    ]
    return {
        "id": "lec-ia-3-6-seno-coseno",
        "title": "Teoremas del Seno y del Coseno",
        "description": "Área del triángulo, Teorema del Seno y Teorema del Coseno con criterios ALA/AAL/LAL/LLL.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


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

    builders = [lesson_3_1, lesson_3_2, lesson_3_3, lesson_3_4, lesson_3_5, lesson_3_6]

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
