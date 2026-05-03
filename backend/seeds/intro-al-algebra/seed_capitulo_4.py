"""
Seed del curso Introducción al Álgebra — Capítulo 4: Polinomios.
6 lecciones (alineadas con MAT1207 PUC):
  4.1 Números complejos
  4.2 Forma polar de un número complejo
  4.3 Raíces n-ésimas
  4.4 Gráficas de polinomios
  4.5 Raíces racionales y complejas
  4.6 Teorema fundamental del álgebra

ENFOQUE: extender el álgebra de los reales al campo complejo, donde toda ecuación
polinomial admite el número exacto de raíces que indica su grado. Cierra con el
TFA, uno de los resultados más profundos de la matemática clásica.

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

CHAPTER_ID = "ch-ia-polinomios"
CHAPTER_TITLE = "Polinomios"
CHAPTER_DESCRIPTION = (
    "El cuerpo de los números complejos $\\mathbb{C}$ y el estudio profundo de "
    "los polinomios. Forma binomial y polar, Teorema de De Moivre, raíces "
    "$n$-ésimas, gráficas y multiplicidad de raíces, Teorema de las Raíces "
    "Racionales y Complejas Conjugadas, y el coronario teorema fundamental del "
    "álgebra que garantiza la existencia de raíces para todo polinomio no constante."
)
CHAPTER_ORDER = 4


# ============================================================================
# 4.1 Números complejos
# ============================================================================
def lesson_4_1():
    blocks = [
        b("texto", body_md=(
            "Los **números reales** constituyen una herramienta poderosa para modelar "
            "el mundo, pero presentan una limitación fundamental: ciertas ecuaciones "
            "algebraicas sencillas, como $x^2 + 1 = 0$, **no poseen solución en "
            "$\\mathbb{R}$**. Para superar esta restricción, los matemáticos extendieron "
            "el sistema numérico introduciendo la **unidad imaginaria** $i$, dando "
            "origen al conjunto de los **números complejos** $\\mathbb{C}$.\n\n"
            "Esta extensión no solo resuelve ecuaciones cuadráticas sin raíces "
            "reales, sino que abre un vasto campo con aplicaciones en ingeniería, "
            "física, procesamiento de señales y geometría analítica. En esta "
            "lección aprenderás:\n\n"
            "- La definición de la unidad imaginaria $i$ y de $\\mathbb{C}$.\n"
            "- Operaciones aritméticas (suma, resta, multiplicación, división).\n"
            "- El **plano de Argand** como representación geométrica.\n"
            "- **Conjugado** y **módulo** con sus propiedades.\n"
            "- Ecuaciones cuadráticas con discriminante negativo."
        )),

        b("definicion",
          titulo="Unidad imaginaria y números complejos",
          body_md=(
              "Se **define** la **unidad imaginaria** $i$ como el número cuyo cuadrado es $-1$:\n"
              "$$i^2 = -1.$$\n"
              "El **conjunto de los números complejos** es\n"
              "$$\\mathbb{C} = \\{z = a + bi \\mid a, b \\in \\mathbb{R}\\}.$$\n"
              "Para $z = a + bi$ se distinguen:\n"
              "- $\\operatorname{Re}(z) = a$ es la **parte real**.\n"
              "- $\\operatorname{Im}(z) = b$ es la **parte imaginaria** (es un número **real**: el coeficiente de $i$).\n\n"
              "**Igualdad:** $z_1 = z_2 \\iff \\operatorname{Re}(z_1) = \\operatorname{Re}(z_2) \\;\\land\\; \\operatorname{Im}(z_1) = \\operatorname{Im}(z_2).$\n\n"
              "**Potencias de $i$ (cíclicas con período 4):** $i^1 = i$, $i^2 = -1$, $i^3 = -i$, $i^4 = 1$, $i^5 = i$, ..."
          )),

        b("definicion",
          titulo="Operaciones en $\\mathbb{C}$",
          body_md=(
              "Sean $z_1 = a + bi$ y $z_2 = c + di$. Se definen:\n\n"
              "**Suma:** $(a+bi) + (c+di) = (a+c) + (b+d)i.$\n\n"
              "**Resta:** $(a+bi) - (c+di) = (a-c) + (b-d)i.$\n\n"
              "**Multiplicación:** se distribuye usando $i^2 = -1$:\n"
              "$$(a+bi)(c+di) = ac + adi + bci + bdi^2 = (ac - bd) + (ad + bc)i.$$\n\n"
              "**División:** se **amplifica** por el conjugado del denominador:\n"
              "$$\\frac{a + bi}{c + di} = \\frac{(a+bi)(c - di)}{(c+di)(c-di)} = \\frac{(ac + bd) + (bc - ad)i}{c^2 + d^2}.$$\n"
              "La clave: $(c+di)(c-di) = c^2 + d^2 \\in \\mathbb{R}$ elimina la parte imaginaria del denominador."
          )),

        b("ejemplo_resuelto",
          titulo="Multiplicación de complejos",
          problema_md=(
              "Calcule $(-1 + 2i) \\cdot \\bigl[(2 - i) + (3 - 2i)\\bigr]$."
          ),
          pasos=[
              {"accion_md": (
                  "Sumamos los complejos del corchete: $(2-i) + (3-2i) = 5 - 3i.$"
               ),
               "justificacion_md": "Suma componente a componente.",
               "es_resultado": False},
              {"accion_md": (
                  "Multiplicamos $(-1 + 2i)(5 - 3i)$ distribuyendo:\n"
                  "$$= -5 + 3i + 10i - 6i^2 = -5 + 13i - 6(-1) = -5 + 13i + 6 = \\boxed{1 + 13i}.$$"
               ),
               "justificacion_md": "Aplicación de $i^2 = -1$ y agrupación.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="División por el conjugado",
          problema_md="Exprese $\\dfrac{1}{(2-3i)(1+i)}$ en forma binomial $a + bi$.",
          pasos=[
              {"accion_md": (
                  "Calculamos primero el denominador: $(2-3i)(1+i) = 2 + 2i - 3i - 3i^2 = 2 - i + 3 = 5 - i.$"
               ),
               "justificacion_md": "Multiplicación y simplificación.",
               "es_resultado": False},
              {"accion_md": (
                  "Amplificamos $\\dfrac{1}{5-i}$ por el conjugado $5+i$:\n"
                  "$$\\frac{1}{5-i} \\cdot \\frac{5+i}{5+i} = \\frac{5+i}{25+1} = \\frac{5+i}{26} = \\boxed{\\frac{5}{26} + \\frac{1}{26}i}.$$"
               ),
               "justificacion_md": "Multiplicación por conjugado para racionalizar.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Plano de Argand, conjugado y módulo",
          body_md=(
              "El **plano de Argand** (o plano complejo) representa cada $z = a + bi$ "
              "como el punto $(a, b)$, con eje horizontal real e eje vertical imaginario.\n\n"
              "Para $z = a + bi$ se definen:\n\n"
              "**Conjugado:** $\\overline{z} = a - bi$. Geométricamente: reflexión respecto al eje real.\n\n"
              "**Módulo:** $|z| = \\sqrt{a^2 + b^2}$. Geométricamente: distancia desde el origen al punto $(a, b)$. Generaliza el valor absoluto real.\n\n"
              "**Identidad clave:** $z \\cdot \\overline{z} = (a+bi)(a-bi) = a^2 + b^2 = |z|^2$. "
              "De aquí $\\dfrac{1}{z} = \\dfrac{\\overline{z}}{|z|^2}$ para $z \\neq 0$."
          )),

        fig(
            "Plano complejo (de Argand): ejes etiquetados Re y Im (eje horizontal y vertical respectivamente). "
            "Un punto z = a + bi en el primer cuadrante con coordenadas (a, b), conectado al origen por una línea sólida en color teal (representando el módulo |z|). "
            "Líneas punteadas perpendiculares mostrando las proyecciones a sobre Re y b sobre Im. "
            "El punto conjugado z̄ = a - bi en el cuarto cuadrante reflejado respecto al eje real, conectado por línea ámbar. Etiquetas claras: |z|, z, z̄, a, b. " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Propiedades del conjugado y módulo.** Para $z, u \\in \\mathbb{C}$:\n\n"
              "1. $\\overline{\\overline{z}} = z$.\n"
              "2. $\\overline{z + u} = \\overline{z} + \\overline{u}$.\n"
              "3. $\\overline{z \\cdot u} = \\overline{z} \\cdot \\overline{u}$.\n"
              "4. $\\overline{(z/u)} = \\overline{z}/\\overline{u}$ ($u \\neq 0$).\n"
              "5. $z = 0 \\iff |z| = 0$.\n"
              "6. $z + \\overline{z} = 2\\operatorname{Re}(z)$, así $\\operatorname{Re}(z) = \\dfrac{z + \\overline{z}}{2}$.\n"
              "7. $z - \\overline{z} = 2\\operatorname{Im}(z) \\cdot i$, así $\\operatorname{Im}(z) = \\dfrac{z - \\overline{z}}{2i}$.\n"
              "8. $z \\in \\mathbb{R} \\iff z = \\overline{z}$.\n"
              "9. $z \\cdot \\overline{z} = |z|^2$.\n"
              "10. $|z \\cdot u| = |z| \\cdot |u|$."
          )),

        b("ejemplo_resuelto",
          titulo="Cuadrática con discriminante negativo",
          problema_md="Encuentre las raíces de $x^2 - 6x + 13 = 0$.",
          pasos=[
              {"accion_md": (
                  "Discriminante: $\\Delta = (-6)^2 - 4(1)(13) = 36 - 52 = -16 < 0$. "
                  "Hay raíces complejas conjugadas."
               ),
               "justificacion_md": "Cálculo del discriminante.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicando la fórmula cuadrática con $\\sqrt{-16} = 4i$:\n"
                  "$$x = \\frac{6 \\pm \\sqrt{-16}}{2} = \\frac{6 \\pm 4i}{2} = 3 \\pm 2i.$$\n"
                  "Las raíces son $\\boxed{x_1 = 3 + 2i, \\; x_2 = 3 - 2i}.$ Nótese que $x_2 = \\overline{x_1}$."
               ),
               "justificacion_md": "Aplicación de la fórmula cuadrática.",
               "es_resultado": True},
          ]),

        ej(
            "Demostración con conjugado",
            ("Pruebe que si $z + \\dfrac{1}{z}$ es un número real (con $z \\neq 0$), "
             "entonces $\\operatorname{Im}(z) = 0$ o $|z| = 1$."),
            ["Sea $z = a + bi$. Calculá $\\frac{1}{z}$ usando el conjugado.",
             "Sumá $z + \\frac{1}{z}$ y exigí que la parte imaginaria sea cero.",
             "La condición se factoriza como $b \\cdot (a^2 + b^2 - 1) = 0$."],
            ("Sea $z = a + bi$ con $z \\neq 0$. Por la identidad $\\frac{1}{z} = \\frac{\\overline{z}}{|z|^2} = \\frac{a - bi}{a^2 + b^2}$. "
             "Sumando: $z + \\frac{1}{z} = \\left(a + \\frac{a}{a^2+b^2}\\right) + \\left(b - \\frac{b}{a^2+b^2}\\right)i$. "
             "Para que sea real, su parte imaginaria es cero: $b - \\frac{b}{a^2+b^2} = 0 \\iff b\\left(1 - \\frac{1}{a^2+b^2}\\right) = 0$, "
             "es decir, $b \\cdot \\frac{a^2 + b^2 - 1}{a^2 + b^2} = 0$. "
             "Como $a^2 + b^2 > 0$, esto implica $b = 0$ o $a^2 + b^2 = 1$, es decir, $\\operatorname{Im}(z) = 0$ o $|z| = 1$. $\\square$")
        ),

        b("errores_comunes",
          items_md=[
              "**Suponer $\\sqrt{-a} = -\\sqrt{a}$.** Lo correcto: $\\sqrt{-a} = \\sqrt{a}\\,i$ para $a > 0$.",
              "**Aplicar $\\sqrt{x}\\sqrt{y} = \\sqrt{xy}$ con números negativos.** Esa propiedad **no vale** en $\\mathbb{C}$.",
              "**Confundir $\\operatorname{Im}(z)$ con $\\operatorname{Im}(z) \\cdot i$.** $\\operatorname{Im}(z) = b$ es real, no $bi$.",
              "**No racionalizar al dividir.** Sin amplificar por el conjugado, el denominador queda complejo.",
          ]),

        b("resumen",
          puntos_md=[
              "$\\mathbb{C} = \\{a + bi \\mid a, b \\in \\mathbb{R}\\}$ con $i^2 = -1$.",
              "Operaciones: suma, resta, multiplicación distribuyendo, división por **conjugado**.",
              "**Plano de Argand:** $z = a + bi \\leftrightarrow (a, b)$. **Módulo:** $|z| = \\sqrt{a^2 + b^2}$.",
              "Identidad clave: $z \\cdot \\overline{z} = |z|^2$.",
              "Toda cuadrática con $\\Delta < 0$ tiene dos raíces complejas conjugadas.",
              "Próxima lección: la **forma polar** $z = r\\,\\text{cis}(\\theta)$, ideal para multiplicar y elevar a potencias.",
          ]),
    ]
    return {
        "id": "lec-ia-4-1-complejos",
        "title": "Números Complejos",
        "description": "Unidad imaginaria, operaciones, plano de Argand, conjugado, módulo y cuadráticas con discriminante negativo.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 1,
    }


# ============================================================================
# 4.2 Forma polar
# ============================================================================
def lesson_4_2():
    blocks = [
        b("texto", body_md=(
            "La **forma polar** de un número complejo es una representación alternativa "
            "a la forma rectangular $z = a + bi$ que aprovecha la estructura geométrica "
            "del plano complejo. En lugar de describir un punto mediante sus coordenadas "
            "cartesianas, la forma polar lo describe mediante su **distancia al origen** "
            "y el **ángulo** que forma con el eje real positivo.\n\n"
            "Esta representación resulta extraordinariamente poderosa al multiplicar, "
            "dividir y elevar a potencias números complejos, pues transforma esas "
            "operaciones en sumas y multiplicaciones de números reales. Cierra con "
            "el **Teorema de De Moivre**, que da una fórmula directa para $z^n$."
        )),

        b("definicion",
          titulo="Forma polar",
          body_md=(
              "Sea $z = a + bi \\in \\mathbb{C} \\setminus \\{0\\}$. Sus coordenadas cartesianas se relacionan "
              "con su **módulo** $r = |z|$ y su **argumento** $\\theta$ (ángulo con el "
              "semieje real positivo) por:\n"
              "$$a = r\\cos(\\theta), \\qquad b = r\\sin(\\theta).$$\n"
              "La **forma polar** de $z$ es:\n"
              "$$z = r\\bigl(\\cos\\theta + i\\sin\\theta\\bigr) = r\\,\\text{cis}(\\theta),$$\n"
              "donde $\\text{cis}(\\theta) := \\cos\\theta + i\\sin\\theta$ es notación abreviada."
          )),

        b("definicion",
          titulo="Determinación del argumento por cuadrantes",
          body_md=(
              "Dado $z = a + bi \\neq 0$, $\\tan(\\theta) = b/a$, pero $\\arctan$ tiene "
              "rango $(-\\pi/2, \\pi/2)$, que solo cubre los cuadrantes I y IV. "
              "Para todos los cuadrantes:\n\n"
              "$$\\theta = \\begin{cases}\n"
              "\\arctan(b/a) & \\text{si } (a, b) \\in \\text{cuadrante I} \\\\\n"
              "\\arctan(b/a) + \\pi & \\text{si } (a, b) \\in \\text{cuadrante II o III} \\\\\n"
              "\\arctan(b/a) + 2\\pi & \\text{si } (a, b) \\in \\text{cuadrante IV} \\\\\n"
              "\\pi/2 & \\text{si } a = 0, b > 0 \\\\\n"
              "3\\pi/2 & \\text{si } a = 0, b < 0\n"
              "\\end{cases}$$\n"
              "El signo de $a$ y $b$ por separado resuelve la ambigüedad."
          )),

        b("ejemplo_resuelto",
          titulo="Conversión a forma polar",
          problema_md=(
              "Escriba en forma polar: (a) $z_1 = 1 + i$, (b) $z_2 = -1 + \\sqrt{3}\\,i$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $(1, 1)$ está en el cuadrante I. $r = \\sqrt{1^2 + 1^2} = \\sqrt{2}$. "
                  "$\\tan\\theta = 1/1 = 1$, $\\theta = \\arctan(1) = \\pi/4$.\n"
                  "$$\\boxed{z_1 = \\sqrt{2}\\,\\text{cis}\\!\\left(\\tfrac{\\pi}{4}\\right)}.$$"
               ),
               "justificacion_md": "Cuadrante I: aplicación directa.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $(-1, \\sqrt{3})$ está en el cuadrante II. $r = \\sqrt{1 + 3} = 2$. "
                  "$\\tan\\theta = \\sqrt{3}/(-1) = -\\sqrt{3}$. Por la fórmula: "
                  "$\\theta = \\arctan(-\\sqrt{3}) + \\pi = -\\pi/3 + \\pi = 2\\pi/3$.\n"
                  "$$\\boxed{z_2 = 2\\,\\text{cis}\\!\\left(\\tfrac{2\\pi}{3}\\right)}.$$"
               ),
               "justificacion_md": "Cuadrante II: corrección por $+\\pi$.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Producto y cociente en forma polar.** Si $z_1 = r_1\\,\\text{cis}(\\theta_1)$ "
              "y $z_2 = r_2\\,\\text{cis}(\\theta_2)$, entonces:\n\n"
              "$$z_1 z_2 = r_1 r_2 \\,\\text{cis}(\\theta_1 + \\theta_2),$$\n"
              "$$\\frac{z_1}{z_2} = \\frac{r_1}{r_2}\\,\\text{cis}(\\theta_1 - \\theta_2), \\quad z_2 \\neq 0.$$\n\n"
              "**En palabras:** al **multiplicar**, los módulos se multiplican y los argumentos **se suman**; "
              "al **dividir**, los módulos se dividen y los argumentos **se restan**.\n\n"
              "*Demostración:* expandir con $\\text{cis}$ y usar las identidades de adición de seno y coseno (Capítulo 3)."
          )),

        b("intuicion", body_md=(
            "**¿Por qué es tan útil?** La multiplicación en forma rectangular implica "
            "distribuir cuatro productos. En forma polar es **una multiplicación de "
            "reales y una suma de ángulos** — mucho más simple. Esta es la razón por "
            "la que la forma polar es la herramienta natural para potencias y raíces."
        )),

        b("ejemplo_resuelto",
          titulo="Producto y cociente en forma polar",
          problema_md=(
              "Sean $z_1 = 2\\,\\text{cis}\\!\\left(\\dfrac{\\pi}{4}\\right)$ y "
              "$z_2 = 5\\,\\text{cis}\\!\\left(\\dfrac{\\pi}{3}\\right)$. Calcule $z_1 z_2$ y $z_1/z_2$."
          ),
          pasos=[
              {"accion_md": (
                  "**Producto:** $z_1 z_2 = 2 \\cdot 5 \\cdot \\text{cis}\\!\\left(\\frac{\\pi}{4} + \\frac{\\pi}{3}\\right) = 10\\,\\text{cis}\\!\\left(\\frac{7\\pi}{12}\\right).$"
               ),
               "justificacion_md": "Producto de módulos, suma de argumentos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cociente:** $\\dfrac{z_1}{z_2} = \\dfrac{2}{5}\\,\\text{cis}\\!\\left(\\frac{\\pi}{4} - \\frac{\\pi}{3}\\right) = \\dfrac{2}{5}\\,\\text{cis}\\!\\left(-\\frac{\\pi}{12}\\right).$"
               ),
               "justificacion_md": "Cociente de módulos, resta de argumentos.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Teorema de De Moivre.** Para todo $n \\in \\mathbb{N}$ y todo $\\theta \\in \\mathbb{R}$:\n"
              "$$\\bigl(\\cos\\theta + i\\sin\\theta\\bigr)^n = \\cos(n\\theta) + i\\sin(n\\theta).$$\n"
              "En particular, si $z = r\\,\\text{cis}(\\theta)$:\n"
              "$$\\boxed{\\;z^n = r^n\\,\\text{cis}(n\\theta)\\;}$$\n"
              "**Demostración:** por inducción sobre $n$, usando la fórmula del producto en cada paso. "
              "Idea conceptual: elevar a la $n$ **eleva el módulo a la $n$ y multiplica el argumento por $n$**."
          )),

        b("ejemplo_resuelto",
          titulo="Potencia con De Moivre",
          problema_md="Calcule $(1 + i)^{10}$.",
          pasos=[
              {"accion_md": (
                  "Del ejemplo anterior, $1 + i = \\sqrt{2}\\,\\text{cis}(\\pi/4)$. Aplicando De Moivre:\n"
                  "$$(1+i)^{10} = (\\sqrt{2})^{10}\\,\\text{cis}\\!\\left(10 \\cdot \\frac{\\pi}{4}\\right) = 2^5\\,\\text{cis}\\!\\left(\\frac{10\\pi}{4}\\right) = 32\\,\\text{cis}\\!\\left(\\frac{5\\pi}{2}\\right).$$"
               ),
               "justificacion_md": "Aplicación de De Moivre en forma polar.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $\\text{cis}$ tiene período $2\\pi$: $\\frac{5\\pi}{2} = 2\\pi + \\frac{\\pi}{2}$, así $\\text{cis}(5\\pi/2) = \\text{cis}(\\pi/2) = i$. Por tanto:\n"
                  "$$\\boxed{(1+i)^{10} = 32i}.$$"
               ),
               "justificacion_md": "Reducción modulo $2\\pi$ y simplificación.",
               "es_resultado": True},
          ]),

        ej(
            "Demostración con De Moivre",
            ("Demuestre que si $(\\sqrt{3} + i)^{2n}$, con $n \\in \\mathbb{Z}$, es un "
             "número **real**, entonces $n$ es múltiplo de $3$."),
            ["Escribí $\\sqrt{3} + i = 2\\,\\text{cis}(\\pi/6)$.",
             "Aplicá De Moivre a la potencia $2n$: el resultado es $4^n\\,\\text{cis}(n\\pi/3)$.",
             "Para que sea real, $\\sin(n\\pi/3) = 0$, lo que ocurre si $n\\pi/3 = k\\pi$ para algún entero $k$."],
            ("$\\sqrt{3} + i = 2\\,\\text{cis}(\\pi/6)$. Por De Moivre: "
             "$(\\sqrt{3}+i)^{2n} = 2^{2n}\\,\\text{cis}(2n\\pi/6) = 4^n\\,\\text{cis}(n\\pi/3) = 4^n[\\cos(n\\pi/3) + i\\sin(n\\pi/3)]$. "
             "Para que sea real: $\\sin(n\\pi/3) = 0 \\iff n\\pi/3 = k\\pi$ para algún $k \\in \\mathbb{Z} \\iff n = 3k$. $\\square$")
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar $\\arctan(b/a)$ sin considerar el cuadrante.** Da el ángulo equivocado en cuadrantes II, III, IV.",
              "**Olvidar reducir el argumento módulo $2\\pi$.** Útil para identificar si el resultado es real, imaginario puro, etc.",
              "**Confundir $\\text{cis}(\\theta)^n = \\text{cis}(n\\theta)$ con $\\text{cis}(\\theta)^n = \\text{cis}(\\theta^n)$.** El exponente afecta al ángulo por multiplicación, no por elevación.",
              "**Aplicar De Moivre a sumas.** Solo vale para potencias de un único complejo en forma polar.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma polar:** $z = r\\,\\text{cis}(\\theta)$, con $r = |z|$ y $\\theta$ determinado por cuadrante.",
              "**Producto/cociente:** módulos se multiplican/dividen, argumentos se suman/restan.",
              "**De Moivre:** $z^n = r^n\\,\\text{cis}(n\\theta)$. Demostrable por inducción.",
              "Próxima lección: **raíces $n$-ésimas** — la operación inversa a la potencia, que da exactamente $n$ soluciones distintas en $\\mathbb{C}$.",
          ]),
    ]
    return {
        "id": "lec-ia-4-2-forma-polar",
        "title": "Forma Polar",
        "description": "Forma polar, argumento por cuadrantes, producto/cociente y Teorema de De Moivre.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# ============================================================================
# 4.3 Raíces n-ésimas
# ============================================================================
def lesson_4_3():
    blocks = [
        b("texto", body_md=(
            "Las **raíces $n$-ésimas** de números complejos constituyen una "
            "extensión natural del concepto de raíz cuadrada al plano complejo. A "
            "diferencia de los números reales, donde la ecuación $z^2 = \\omega$ "
            "puede no tener solución (cuando $\\omega < 0$), en $\\mathbb{C}$ "
            "**todo número complejo no nulo posee exactamente $n$ raíces $n$-ésimas "
            "distintas**.\n\n"
            "Este hecho, profundo y elegante, revela la **completitud algebraica** "
            "del campo complejo y tiene consecuencias directas en el estudio de "
            "polinomios y ecuaciones algebraicas. Veremos:\n\n"
            "- La definición y el problema de existencia.\n"
            "- El **teorema general** y la fórmula explícita en forma polar.\n"
            "- La **propiedad geométrica:** las raíces se distribuyen en un polígono regular.\n"
            "- Aplicaciones a ecuaciones polinomiales.\n"
            "- Las **raíces de la unidad** y sus propiedades algebraicas."
        )),

        b("definicion",
          titulo="Raíz $n$-ésima",
          body_md=(
              "Diremos que $z \\in \\mathbb{C}$ es una **raíz $n$-ésima** de $\\omega \\in \\mathbb{C}$ si y solo si\n"
              "$$z^n = \\omega \\qquad (\\text{formalmente: } z = \\sqrt[n]{\\omega}).$$\n"
              "El objetivo es determinar cuántas soluciones tiene esta ecuación y cómo calcularlas explícitamente."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema general de las raíces $n$-ésimas.** Todo complejo $\\omega = r\\,\\text{cis}(\\theta) \\neq 0$ "
              "tiene exactamente $n$ raíces $n$-ésimas distintas, dadas por:\n"
              "$$\\boxed{\\;z_k = \\sqrt[n]{r}\\,\\text{cis}\\!\\left(\\frac{\\theta + 2k\\pi}{n}\\right), \\quad k = 0, 1, \\ldots, n-1.\\;}$$\n\n"
              "**Idea de la demostración.** Sea $z = \\rho\\,\\text{cis}(\\varphi)$. Por De Moivre, $z^n = \\omega$ se convierte "
              "en $\\rho^n\\,\\text{cis}(n\\varphi) = r\\,\\text{cis}(\\theta)$. Igualando módulos y argumentos (módulo $2\\pi$):\n"
              "$$\\rho^n = r \\implies \\rho = \\sqrt[n]{r}, \\qquad n\\varphi = \\theta + 2k\\pi \\implies \\varphi = \\frac{\\theta + 2k\\pi}{n}.$$\n"
              "Los valores $k = 0, 1, \\ldots, n-1$ producen ángulos distintos en $[0, 2\\pi)$; para $k \\ge n$ los ángulos se repiten."
          )),

        b("teorema",
          enunciado_md=(
              "**Propiedad geométrica.** Todas las raíces $n$-ésimas de $\\omega = r\\,\\text{cis}(\\theta)$ tienen "
              "el **mismo módulo** $|z_k| = \\sqrt[n]{r}$ y se distribuyen **uniformemente** sobre la "
              "circunferencia de radio $\\sqrt[n]{r}$ centrada en el origen, formando un **polígono regular "
              "de $n$ lados** con vértices separados por ángulos de $\\dfrac{2\\pi}{n}$."
          )),

        fig(
            "Plano complejo con ejes Re e Im. Una circunferencia centrada en el origen de radio aproximado 2 (en color teal). Sobre la circunferencia, 6 puntos marcados como vértices de un hexágono regular, etiquetados z_0, z_1, z_2, z_3, z_4, z_5. "
            "Líneas punteadas conectando los puntos formando el hexágono. Líneas radiales del origen a cada punto. Arco pequeño entre dos vértices adyacentes etiquetado '2π/n'. "
            "Caption visual: 'Las n raíces n-ésimas forman un polígono regular en el círculo de radio ⁿ√r'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Raíces cúbicas de 1",
          problema_md="Determine las raíces cúbicas de $1$, es decir, resuelva $z^3 = 1$ en $\\mathbb{C}$.",
          pasos=[
              {"accion_md": (
                  "Reescribimos $z^3 - 1 = 0$ y factorizamos por diferencia de cubos:\n"
                  "$$z^3 - 1 = (z - 1)(z^2 + z + 1) = 0 \\iff z = 1 \\;\\lor\\; z^2 + z + 1 = 0.$$"
               ),
               "justificacion_md": "Factorización por diferencia de cubos.",
               "es_resultado": False},
              {"accion_md": (
                  "Para $z^2 + z + 1 = 0$, fórmula cuadrática:\n"
                  "$$z = \\frac{-1 \\pm \\sqrt{1 - 4}}{2} = \\frac{-1 \\pm \\sqrt{3}\\,i}{2}.$$"
               ),
               "justificacion_md": "Discriminante negativo → raíces complejas conjugadas.",
               "es_resultado": False},
              {"accion_md": (
                  "Las tres raíces cúbicas de $1$ son:\n"
                  "$$\\boxed{z_1 = 1, \\;\\; z_2 = -\\tfrac{1}{2} - \\tfrac{\\sqrt{3}}{2}\\,i, \\;\\; z_3 = -\\tfrac{1}{2} + \\tfrac{\\sqrt{3}}{2}\\,i.}$$\n"
                  "Las tres tienen módulo $1$ y están separadas por ángulos de $2\\pi/3$ sobre el círculo unitario."
               ),
               "justificacion_md": "Verificación de la propiedad geométrica.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Resolver $z^3 + 27 = 0$",
          problema_md="Encuentre todas las soluciones de $z^3 + 27 = 0$.",
          pasos=[
              {"accion_md": (
                  "$z^3 = -27$. Forma polar: $-27 = 27\\,\\text{cis}(\\pi)$ ($r = 27$, $\\theta = \\pi$). Con $n = 3$:\n"
                  "$$z_k = \\sqrt[3]{27}\\,\\text{cis}\\!\\left(\\frac{\\pi + 2k\\pi}{3}\\right) = 3\\,\\text{cis}\\!\\left(\\frac{(2k+1)\\pi}{3}\\right), \\;\\; k = 0, 1, 2.$$"
               ),
               "justificacion_md": "Fórmula del teorema general.",
               "es_resultado": False},
              {"accion_md": (
                  "**$k=0$:** $z_0 = 3\\,\\text{cis}(\\pi/3) = 3(\\frac{1}{2} + \\frac{\\sqrt{3}}{2}i) = \\frac{3}{2} + \\frac{3\\sqrt{3}}{2}i.$\n\n"
                  "**$k=1$:** $z_1 = 3\\,\\text{cis}(\\pi) = -3.$\n\n"
                  "**$k=2$:** $z_2 = 3\\,\\text{cis}(5\\pi/3) = \\frac{3}{2} - \\frac{3\\sqrt{3}}{2}i.$\n\n"
                  "Las tres soluciones son $\\boxed{-3, \\; \\frac{3}{2} \\pm \\frac{3\\sqrt{3}}{2}i}.$"
               ),
               "justificacion_md": "Evaluación de cada raíz.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Raíces de la unidad.** Las raíces $n$-ésimas de la unidad son las soluciones de $z^n = 1$. "
              "Por el teorema con $r = 1$, $\\theta = 0$:\n"
              "$$z_k = \\text{cis}\\!\\left(\\frac{2k\\pi}{n}\\right), \\quad k = 0, 1, \\ldots, n-1.$$\n"
              "Forman un **polígono regular** inscrito en el círculo unitario.\n\n"
              "**Caso cúbico ($n = 3$):** sea $\\omega = -\\frac{1}{2} + \\frac{\\sqrt{3}}{2}i$ una raíz cúbica de la unidad distinta de $1$. Entonces:\n"
              "1. $\\omega^2 = \\overline{\\omega}$.\n"
              "2. $1 + \\omega + \\omega^2 = 0$ (las tres raíces suman cero)."
          )),

        b("ejemplo_resuelto",
          titulo="Polinomio de grado 6 con factorización completa",
          problema_md=(
              "Resuelva $x^6 - 3x^5 - 4x^4 + 16x^2 - 48x - 64 = 0$ sabiendo que $-1$ "
              "y $4$ son raíces."
          ),
          pasos=[
              {"accion_md": (
                  "Como $-1$ y $4$ son raíces, $(x+1)(x-4) = x^2 - 3x - 4$ divide al polinomio. "
                  "Realizando la división polinomial: $p(x) = (x+1)(x-4)(x^4 + 16).$"
               ),
               "justificacion_md": "Factor común de raíces conocidas.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolvemos $x^4 + 16 = 0$, es decir $x^4 = -16$. Forma polar: $-16 = 16\\,\\text{cis}(\\pi)$. Con $n = 4$:\n"
                  "$$x_k = \\sqrt[4]{16}\\,\\text{cis}\\!\\left(\\frac{(2k+1)\\pi}{4}\\right) = 2\\,\\text{cis}\\!\\left(\\frac{(2k+1)\\pi}{4}\\right), \\;\\; k = 0, 1, 2, 3.$$"
               ),
               "justificacion_md": "Aplicación del teorema general.",
               "es_resultado": False},
              {"accion_md": (
                  "Evaluando: $x_0 = \\sqrt{2}+\\sqrt{2}i$, $x_1 = -\\sqrt{2}+\\sqrt{2}i$, $x_2 = -\\sqrt{2}-\\sqrt{2}i$, $x_3 = \\sqrt{2}-\\sqrt{2}i$.\n\n"
                  "**Las seis soluciones:** $\\boxed{x = -1, \\;\\; x = 4, \\;\\; x = \\pm\\sqrt{2} \\pm \\sqrt{2}i.}$"
               ),
               "justificacion_md": "Combinación de raíces conocidas y nuevas.",
               "es_resultado": True},
          ]),

        ej(
            "Suma de raíces cúbicas de la unidad",
            ("Sea $\\omega \\neq 1$ una raíz cúbica de la unidad. Demuestre que "
             "$1 + \\omega + \\omega^2 = 0$."),
            ["Como $\\omega^3 = 1$, entonces $\\omega^3 - 1 = 0$.",
             "Factorizá: $\\omega^3 - 1 = (\\omega - 1)(\\omega^2 + \\omega + 1)$.",
             "Como $\\omega \\neq 1$, $(\\omega - 1) \\neq 0$, así $\\omega^2 + \\omega + 1 = 0$."],
            ("Como $\\omega^3 = 1$ y $\\omega \\neq 1$, tenemos $\\omega^3 - 1 = 0$, lo que se factoriza como "
             "$(\\omega - 1)(\\omega^2 + \\omega + 1) = 0$. Dado que $\\omega \\neq 1$, el factor "
             "$(\\omega - 1) \\neq 0$, por lo que necesariamente $\\omega^2 + \\omega + 1 = 0$, "
             "es decir, $1 + \\omega + \\omega^2 = 0$. $\\square$")
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar que $z^n = \\omega$ tiene $n$ soluciones, no una.** En $\\mathbb{R}$ hay 0, 1 o 2; en $\\mathbb{C}$ siempre $n$.",
              "**Usar $\\sqrt[n]{r}$ ambiguo.** Tomá la raíz **real positiva** de $r > 0$.",
              "**No reducir argumentos módulo $2\\pi$.** Hace difícil comparar resultados o reconocer simetrías.",
              "**Olvidar que para $\\omega = 0$ la única solución es $z = 0$.** El teorema asume $\\omega \\neq 0$.",
          ]),

        b("resumen",
          puntos_md=[
              "Todo $\\omega \\neq 0$ tiene **exactamente $n$ raíces $n$-ésimas distintas** en $\\mathbb{C}$.",
              "**Fórmula:** $z_k = \\sqrt[n]{r}\\,\\text{cis}\\!\\left(\\dfrac{\\theta + 2k\\pi}{n}\\right)$, $k = 0, \\ldots, n-1$.",
              "**Geometría:** las raíces forman un polígono regular en el círculo de radio $\\sqrt[n]{r}$.",
              "Las **raíces cúbicas de la unidad** $\\{1, \\omega, \\omega^2\\}$ satisfacen $\\omega^2 = \\overline{\\omega}$ y $1 + \\omega + \\omega^2 = 0$.",
              "Próxima lección: **gráficas** de polinomios, donde la multiplicidad de las raíces determina la geometría local.",
          ]),
    ]
    return {
        "id": "lec-ia-4-3-raices-nesimas",
        "title": "Raíces $n$-ésimas",
        "description": "Teorema general, fórmula con cis, distribución geométrica, raíces de la unidad y aplicaciones.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
    }


# ============================================================================
# 4.4 Gráficas de polinomios
# ============================================================================
def lesson_4_4():
    blocks = [
        b("texto", body_md=(
            "Las **funciones polinomiales** son uno de los objetos más fundamentales del "
            "álgebra y el análisis. Su estudio geométrico —el análisis de sus gráficas— "
            "permite comprender de manera visual propiedades algebraicas profundas como "
            "los **ceros**, la **multiplicidad** de las raíces y el **comportamiento global** "
            "de la función.\n\n"
            "En esta lección desarrollamos las herramientas necesarias para trazar e "
            "interpretar correctamente la gráfica de un polinomio arbitrario, partiendo "
            "del comportamiento en el infinito hasta llegar al análisis local en cada raíz."
        )),

        b("teorema",
          enunciado_md=(
              "**Comportamiento final.** Sea $P(x) = a_n x^n + \\cdots + a_0$ con $a_n \\neq 0$. "
              "El comportamiento cuando $x \\to \\pm\\infty$ está determinado **únicamente** por "
              "el grado $n$ y el signo del coeficiente principal $a_n$:\n\n"
              "**Grado par:**\n"
              "- $a_n > 0$: $P(x) \\to +\\infty$ en ambos extremos (forma de **U**).\n"
              "- $a_n < 0$: $P(x) \\to -\\infty$ en ambos extremos (forma de **∩**).\n\n"
              "**Grado impar:**\n"
              "- $a_n > 0$: sube a la derecha ($+\\infty$), baja a la izquierda ($-\\infty$).\n"
              "- $a_n < 0$: baja a la derecha, sube a la izquierda.\n\n"
              "Toda gráfica polinomial es **continua** sobre $\\mathbb{R}$."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema del Factor.** Sea $P(x)$ un polinomio y $c \\in \\mathbb{R}$. Entonces:\n"
              "$$c \\text{ es cero de } P \\iff (x - c) \\text{ es factor de } P(x).$$\n"
              "Geométricamente, los **ceros** son los puntos donde la gráfica intersecta o es tangente al eje $x$."
          )),

        b("definicion",
          titulo="Multiplicidad de una raíz",
          body_md=(
              "Sea $c$ una raíz del polinomio $P(x)$. Decimos que $c$ tiene **multiplicidad** $m$ si\n"
              "$$P(x) = (x - c)^m \\cdot Q(x), \\quad m \\in \\mathbb{N}, \\;\\; Q(c) \\neq 0.$$\n"
              "**Efecto geométrico:** la multiplicidad determina cómo se comporta la gráfica en $x = c$:\n\n"
              "- **Multiplicidad par:** la gráfica es **tangente** al eje $x$ en $x = c$ sin cruzarlo (toca y rebota).\n"
              "- **Multiplicidad impar:** la gráfica **cruza** el eje $x$ en $x = c$.\n\n"
              "Este criterio es fundamental para trazar gráficas cualitativas correctas."
          )),

        b("ejemplo_resuelto",
          titulo="Gráfica completa con factorización dada",
          problema_md="Grafique el polinomio $P(x) = x^4(x - 2)^3(x + 1)^2$.",
          pasos=[
              {"accion_md": (
                  "**Paso 1: ceros y multiplicidades.** $x = 0$ con mult $4$ (par), "
                  "$x = 2$ con mult $3$ (impar), $x = -1$ con mult $2$ (par)."
               ),
               "justificacion_md": "Lectura directa de la forma factorizada.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2: comportamiento final.** Grado total $= 4 + 3 + 2 = 9$ (impar), "
                  "coeficiente principal $= 1 > 0$. Luego $P(x) \\to +\\infty$ a la derecha y $\\to -\\infty$ a la izquierda."
               ),
               "justificacion_md": "Aplicación de la proposición.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3: comportamiento en cada raíz.**\n"
                  "- $x = -1$ (mult par): toca y rebota.\n"
                  "- $x = 0$ (mult par): toca y rebota.\n"
                  "- $x = 2$ (mult impar): cruza el eje."
               ),
               "justificacion_md": "Aplicación de la regla par/impar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 4: signo en cada intervalo.** Para $x = -2$: $P(-2) = 16 \\cdot (-64) \\cdot 1 < 0$. "
                  "La gráfica viene desde $-\\infty$ por debajo del eje, toca y rebota en $x = -1$ (sigue negativa), "
                  "toca y rebota en $x = 0$ (sigue negativa), cruza en $x = 2$ y sube hacia $+\\infty$."
               ),
               "justificacion_md": "Análisis cualitativo completo.",
               "es_resultado": True},
          ]),

        fig(
            "Gráfica de un polinomio de grado 9 P(x) = x^4(x-2)^3(x+1)^2 sobre eje X de -2 a 3, eje Y de -50 a 50. "
            "Curva continua en color teal: viene desde abajo a la izquierda (-∞), toca el eje X en x = -1 con tangencia (rebota sin cruzar), continúa por debajo, toca el eje en x = 0 con tangencia (rebota), continúa por debajo, cruza el eje en x = 2 y sube rápidamente hacia +∞ a la derecha. "
            "Etiquetas claras de los ceros con sus multiplicidades. Líneas punteadas verticales tenues en las raíces. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Determinar polinomio a partir de su gráfica",
          problema_md=(
              "Determine el polinomio $Q(x)$ de grado $3$ cuyo gráfico tiene ceros en "
              "$x = -2$ y $x = 3$, y pasa por el punto $(0, 18)$. La gráfica cruza el "
              "eje en $x = -2$ y es tangente al eje en $x = 3$."
          ),
          pasos=[
              {"accion_md": (
                  "Multiplicidades a partir de la gráfica: en $x = -2$ cruza ⟹ mult impar (luego 1, dado el grado 3); "
                  "en $x = 3$ es tangente ⟹ mult par (luego 2). Total: $1 + 2 = 3$. ✓"
               ),
               "justificacion_md": "Lectura del comportamiento local.",
               "es_resultado": False},
              {"accion_md": (
                  "Forma general: $Q(x) = a(x + 2)^1 (x - 3)^2$ con $a$ a determinar."
               ),
               "justificacion_md": "Forma factorizada estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "Imponemos $Q(0) = 18$: $a \\cdot 2 \\cdot 9 = 18a = 18 \\Rightarrow a = 1$. Por lo tanto:\n"
                  "$$\\boxed{Q(x) = (x + 2)(x - 3)^2}.$$"
               ),
               "justificacion_md": "Determinación del coeficiente líder por valor en un punto.",
               "es_resultado": True},
          ]),

        ej(
            "Gráfica con factor común",
            ("Sea $P(x) = x^3 - 2x^2 - 3x$. (a) Encuentre los ceros de $P$. "
             "(b) Describa la gráfica indicando comportamiento final y comportamiento en cada raíz."),
            ["Factorizá $x$ común y luego la cuadrática $x^2 - 2x - 3$.",
             "Identificá la multiplicidad de cada raíz a partir de la factorización.",
             "Aplicá las reglas de comportamiento final (grado impar, coeficiente líder > 0)."],
            ("**(a)** $P(x) = x(x^2 - 2x - 3) = x(x - 3)(x + 1)$. Ceros: $x = 0, 3, -1$, todos con multiplicidad 1. "
             "**(b)** Grado 3 (impar), coeficiente líder 1 > 0: la gráfica baja hacia $-\\infty$ a la izquierda y sube hacia $+\\infty$ a la derecha. "
             "Como todas las multiplicidades son impares, la gráfica cruza el eje en $x = -1, 0, 3$ alternando signos.")
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir grado con número de ceros distintos.** Un grado-5 puede tener 2, 3 o 5 ceros distintos según multiplicidades.",
              "**Olvidar que mult par implica tangencia.** La gráfica no cruza, **rebota**.",
              "**Olvidar el coeficiente líder al determinar polinomios desde gráficas.** Tres ceros no determinan el polinomio: hay un grado de libertad ($a$).",
              "**Ignorar el comportamiento final.** Es la primera información que ordena la gráfica.",
          ]),

        b("resumen",
          puntos_md=[
              "**Comportamiento final:** determinado por el grado (par/impar) y signo del coeficiente líder.",
              "**Teorema del Factor:** $c$ raíz $\\iff$ $(x-c)$ factor.",
              "**Multiplicidad:** par ⟹ rebota; impar ⟹ cruza.",
              "**Procedimiento:** comportamiento final → ceros → multiplicidades → signos por intervalo → trazado.",
              "Próxima lección: **Teorema de las Raíces Racionales** y de las **Raíces Complejas Conjugadas** para encontrar ceros sin adivinar.",
          ]),
    ]
    return {
        "id": "lec-ia-4-4-graficas",
        "title": "Gráficas de Polinomios",
        "description": "Comportamiento final, ceros, multiplicidades, trazado de gráficas y determinación inversa.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 4,
    }


# ============================================================================
# 4.5 Raíces racionales y complejas
# ============================================================================
def lesson_4_5():
    blocks = [
        b("texto", body_md=(
            "El estudio de las raíces de polinomios constituye uno de los pilares "
            "fundamentales del álgebra. En esta lección abordaremos dos resultados clave:\n\n"
            "- El **Teorema de las Raíces Racionales**, que permite identificar candidatas a "
            "raíces racionales de un polinomio con coeficientes enteros mediante condiciones "
            "de divisibilidad.\n\n"
            "- El **Teorema de las Raíces Complejas Conjugadas**, que describe la estructura "
            "de las raíces complejas de polinomios con coeficientes reales.\n\n"
            "Combinados con la división polinomial, constituyen una herramienta poderosa para "
            "factorizar completamente cualquier polinomio."
        )),

        b("definicion",
          titulo="Polinomios sobre $\\mathbb{K}$",
          body_md=(
              "Sea $\\mathbb{K}$ uno de $\\mathbb{Z}, \\mathbb{Q}, \\mathbb{R}, \\mathbb{C}$. Un **polinomio** "
              "$P(x) \\in \\mathbb{K}[x]$ es de la forma $P(x) = a_n x^n + \\cdots + a_0$ con $a_k \\in \\mathbb{K}$. "
              "El **coeficiente líder** es $a_n$, el **término independiente** es $a_0$, y el **grado** es $n$ (cuando $a_n \\neq 0$).\n\n"
              "Una **raíz** (o **cero**) es $c \\in \\mathbb{K}$ con $P(c) = 0$. Vale la inclusión:\n"
              "$$\\mathbb{Z}[x] \\subset \\mathbb{Q}[x] \\subset \\mathbb{R}[x] \\subset \\mathbb{C}[x].$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema de las Raíces Racionales.** Sea $P(x) \\in \\mathbb{Z}[x]$ de la forma "
              "$P(x) = a_n x^n + \\cdots + a_0$. Si $c = \\dfrac{p}{q}$ (con $\\gcd(p, q) = 1$, $q > 0$) es una raíz racional de $P$, entonces:\n"
              "$$p \\mid a_0 \\qquad \\text{y} \\qquad q \\mid a_n.$$\n"
              "**Consecuencia práctica:** los candidatos a raíz racional son los cocientes $\\pm p/q$ con $p$ divisor de $a_0$ y $q$ divisor positivo de $a_n$. "
              "Si $P$ es **mónico** ($a_n = 1$), toda raíz racional es **entera** y divide a $a_0$."
          )),

        b("ejemplo_resuelto",
          titulo="Factorización con raíces racionales",
          problema_md="Factorice completamente $P(x) = 2x^3 + x^2 - 13x + 6$ y encuentre todos sus ceros.",
          pasos=[
              {"accion_md": (
                  "$a_0 = 6$, $a_3 = 2$. Divisores de $6$: $\\pm 1, \\pm 2, \\pm 3, \\pm 6$. Divisores positivos de $2$: $1, 2$. "
                  "Candidatos racionales: $\\pm 1, \\pm 2, \\pm 3, \\pm 6, \\pm \\tfrac{1}{2}, \\pm \\tfrac{3}{2}.$"
               ),
               "justificacion_md": "Listado por divisibilidad.",
               "es_resultado": False},
              {"accion_md": (
                  "Probamos $x = 2$: $P(2) = 16 + 4 - 26 + 6 = 0.$ ✓ Entonces $(x - 2)$ es factor. "
                  "Por división sintética: $2x^3 + x^2 - 13x + 6 = (x - 2)(2x^2 + 5x - 3).$"
               ),
               "justificacion_md": "Probar candidatos hasta hallar uno; dividir.",
               "es_resultado": False},
              {"accion_md": (
                  "Factorizamos $2x^2 + 5x - 3$ con la fórmula cuadrática: $x = \\dfrac{-5 \\pm \\sqrt{25 + 24}}{4} = \\dfrac{-5 \\pm 7}{4}$, "
                  "dando $x = \\tfrac{1}{2}$ y $x = -3$. Por tanto $2x^2 + 5x - 3 = (2x - 1)(x + 3).$"
               ),
               "justificacion_md": "Cuadrática para el factor restante.",
               "es_resultado": False},
              {"accion_md": (
                  "**Factorización completa:** $\\boxed{P(x) = (x - 2)(2x - 1)(x + 3)}$. Ceros: $x = 2, \\tfrac{1}{2}, -3.$"
               ),
               "justificacion_md": "Producto de tres factores lineales.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Teorema de las Raíces Complejas Conjugadas.** Si $P(x) \\in \\mathbb{R}[x]$ y $\\alpha \\in \\mathbb{C}$ "
              "es una raíz de $P(x)$, entonces $\\overline{\\alpha}$ también es raíz de $P(x)$.\n\n"
              "**Atención:** este teorema **solo aplica** cuando los coeficientes son **todos reales**. "
              "Si algún coeficiente es complejo no real, no vale.\n\n"
              "**Factorización vía pares conjugados.** Si $\\alpha$ y $\\overline{\\alpha}$ son raíces:\n"
              "$$(x - \\alpha)(x - \\overline{\\alpha}) = x^2 - 2\\operatorname{Re}(\\alpha)\\,x + |\\alpha|^2,$$\n"
              "que es un polinomio cuadrático **con coeficientes reales**. Así, todo polinomio en $\\mathbb{R}[x]$ se "
              "factoriza como producto de factores lineales y cuadráticos irreducibles sobre $\\mathbb{R}$."
          )),

        b("ejemplo_resuelto",
          titulo="Resolución usando una raíz compleja conocida",
          problema_md="Resuelva $x^3 - 7x^2 + 17x - 15 = 0$, sabiendo que $\\alpha = 2 + i$ es una raíz.",
          pasos=[
              {"accion_md": (
                  "$P(x) \\in \\mathbb{R}[x]$ y $\\alpha = 2 + i$ es raíz, así $\\overline{\\alpha} = 2 - i$ también lo es. "
                  "Construimos el factor cuadrático:\n"
                  "$(x - (2+i))(x - (2-i)) = x^2 - 4x + (4 + 1) = x^2 - 4x + 5.$"
               ),
               "justificacion_md": "Aplicación del Teorema de Conjugadas.",
               "es_resultado": False},
              {"accion_md": (
                  "Dividiendo $P(x)$ por $x^2 - 4x + 5$: $x^3 - 7x^2 + 17x - 15 = (x^2 - 4x + 5)(x - 3).$\n\n"
                  "**Soluciones:** $\\boxed{x_1 = 2 + i, \\;\\; x_2 = 2 - i, \\;\\; x_3 = 3.}$"
               ),
               "justificacion_md": "División polinomial e identificación del tercer factor.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cuadrática con coeficientes complejos (sin conjugadas)",
          problema_md="Resuelva $x^2 - (4 + 2i)x + (2 + 4i) = 0$.",
          pasos=[
              {"accion_md": (
                  "Como los coeficientes son **complejos**, **no aplica** el Teorema de las Conjugadas. "
                  "Aplicamos directamente la fórmula cuadrática.\n\n"
                  "Discriminante: $(4 + 2i)^2 - 4(2 + 4i) = 16 + 16i + 4i^2 - 8 - 16i = 16 - 4 - 8 = 4.$"
               ),
               "justificacion_md": "Cálculo del discriminante.",
               "es_resultado": False},
              {"accion_md": (
                  "$x = \\dfrac{(4 + 2i) \\pm 2}{2}$, dando $\\boxed{z_1 = 3 + i, \\;\\; z_2 = 1 + i}$. "
                  "Nótese que $\\overline{z_1} = 3 - i$ y $\\overline{z_2} = 1 - i$ **no** son raíces, confirmando que el teorema no aplica."
               ),
               "justificacion_md": "Verificación de la condición del teorema.",
               "es_resultado": True},
          ]),

        ej(
            "Polinomio cuártico con par conjugado",
            ("Resuelva $x^4 - 2x^3 + 6x^2 + 22x + 13 = 0$ sabiendo que $2 + 3i$ es un cero."),
            ["Por Conjugadas, $2 - 3i$ también es raíz. Construí el factor cuadrático irreducible $(x-(2+3i))(x-(2-3i))$.",
             "Dividí el polinomio entre ese factor cuadrático.",
             "El cociente debe ser otro cuadrático; resolvelo y combiná todas las raíces."],
            ("$(x - (2+3i))(x - (2-3i)) = x^2 - 4x + 13$. Dividiendo: $x^4 - 2x^3 + 6x^2 + 22x + 13 = (x^2 - 4x + 13)(x^2 + 2x + 1) = (x^2 - 4x + 13)(x + 1)^2$. "
             "Las raíces de $(x+1)^2 = 0$ son $x = -1$ con multiplicidad 2. "
             "Soluciones totales: $\\boxed{x_1 = 2 + 3i, \\; x_2 = 2 - 3i, \\; x_3 = x_4 = -1.}$")
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Conjugadas con coeficientes complejos.** Solo vale si **todos** los coeficientes son reales.",
              "**Pensar que las raíces racionales siempre existen.** Pueden no existir; el teorema solo da candidatos.",
              "**Olvidar dividir por $q$ en el criterio.** Para $a_n \\neq 1$, los candidatos no son enteros.",
              "**Hacer mal la división polinomial.** Verificá multiplicando los factores al final.",
          ]),

        b("resumen",
          puntos_md=[
              "**Raíces racionales:** $c = p/q$ raíz $\\Rightarrow p \\mid a_0$, $q \\mid a_n$.",
              "**Raíces complejas conjugadas:** sobre $\\mathbb{R}[x]$, las raíces complejas vienen en pares $\\alpha, \\overline{\\alpha}$.",
              "**Pares conjugados ⟹ factor cuadrático real:** $(x - \\alpha)(x - \\overline{\\alpha}) = x^2 - 2\\operatorname{Re}(\\alpha)x + |\\alpha|^2$.",
              "**Estrategia de factorización:** raíces racionales primero, luego conjugadas, dividiendo paso a paso.",
              "Próxima lección: el **Teorema Fundamental del Álgebra** y la factorización completa sobre $\\mathbb{C}$.",
          ]),
    ]
    return {
        "id": "lec-ia-4-5-raices-racionales",
        "title": "Raíces Racionales y Complejas",
        "description": "Teoremas de raíces racionales y de raíces complejas conjugadas, con factorización completa.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 5,
    }


# ============================================================================
# 4.6 Teorema fundamental del álgebra
# ============================================================================
def lesson_4_6():
    blocks = [
        b("texto", body_md=(
            "El **Teorema Fundamental del Álgebra** es uno de los resultados más profundos "
            "y elegantes de la matemática clásica. Establece que el cuerpo de los números "
            "complejos $\\mathbb{C}$ es **algebraicamente cerrado**: todo polinomio no constante "
            "con coeficientes complejos tiene al menos una raíz en $\\mathbb{C}$.\n\n"
            "Esta propiedad **no se cumple** en $\\mathbb{R}$: por ejemplo, $x^2 + 1$ no tiene "
            "raíces reales pero sí tiene raíces complejas ($i$ y $-i$). La importancia del "
            "teorema radica en que, junto al **Teorema de Factorización**, garantiza que "
            "cualquier polinomio de grado $n \\ge 1$ con coeficientes complejos se descompone "
            "completamente en $n$ factores lineales."
        )),

        b("teorema",
          enunciado_md=(
              "**Teorema Fundamental del Álgebra (TFA).** Para todo $P(x) \\in \\mathbb{C}[x]$ de grado "
              "$n \\ge 1$, existe $z \\in \\mathbb{C}$ tal que $P(z) = 0$.\n\n"
              "**Equivalentemente:** todo polinomio no constante con coeficientes complejos "
              "admite al menos una raíz en $\\mathbb{C}$.\n\n"
              "**Nota histórica.** Demostrado satisfactoriamente por primera vez en **1798** por "
              "**Carl Friedrich Gauss** en su tesis doctoral. Antes, d'Alembert y Euler propusieron "
              "demostraciones, pero Gauss probó que todas eran incorrectas. La prueba moderna usa "
              "herramientas más allá del alcance de este curso (análisis complejo o topología algebraica), "
              "por lo que admitimos el teorema sin demostrarlo."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema de Factorización.** Sea $P(x) \\in \\mathbb{C}[x]$ de grado $n \\ge 1$. Entonces $P(x)$ "
              "puede factorizarse como el producto de $n$ factores lineales (no necesariamente distintos):\n"
              "$$P(x) = a_n (x - z_1)(x - z_2) \\cdots (x - z_n),$$\n"
              "donde $z_1, z_2, \\ldots, z_n \\in \\mathbb{C}$ son las **$n$ raíces** del polinomio.\n\n"
              "**Demostración (esquema):** Por TFA, existe $z_1$ raíz; por el Teorema del Factor, $P(x) = (x - z_1) Q_1(x)$ "
              "con $Q_1 \\in \\mathbb{C}[x]$ de grado $n - 1$. Aplicando recurrentemente TFA + Teorema del Factor a $Q_1, Q_2, \\ldots$, "
              "se obtiene la factorización completa. $\\square$"
          )),

        b("teorema",
          enunciado_md=(
              "**Número de raíces.** Todo polinomio $P(x)$ de grado $n \\ge 1$ tiene **exactamente $n$ raíces en $\\mathbb{C}$**, "
              "siempre que cada raíz de **multiplicidad** $k$ se cuente $k$ veces.\n\n"
              "Aquí $z_0$ tiene multiplicidad $k$ si $(x - z_0)^k$ divide a $P(x)$ pero $(x - z_0)^{k+1}$ no. "
              "En la factorización completa, esto se refleja como la presencia del factor $(x - z_0)$ exactamente $k$ veces."
          )),

        b("intuicion", body_md=(
            "**¿Por qué es \"fundamental\"?** Porque resuelve de un golpe el problema de la "
            "**existencia** de raíces para todo polinomio, algo que durante siglos los matemáticos "
            "intuyeron pero no lograron probar rigurosamente. El TFA establece que la extensión "
            "de $\\mathbb{R}$ a $\\mathbb{C}$ es **definitiva**: no hace falta inventar más números "
            "para que todo polinomio tenga raíces. $\\mathbb{C}$ es la \"clausura algebraica\" de $\\mathbb{R}$."
        )),

        b("ejemplo_resuelto",
          titulo="Factorización por agrupación",
          problema_md="Sea $P(x) = x^3 - 3x^2 + x - 3$. (a) Encuentre todos los ceros. (b) Encuentre la factorización completa.",
          pasos=[
              {"accion_md": (
                  "**(a)** Factorizamos por agrupación:\n"
                  "$P(x) = x^2(x - 3) + 1 \\cdot (x - 3) = (x^2 + 1)(x - 3).$"
               ),
               "justificacion_md": "Factor común dentro de pares de términos.",
               "es_resultado": False},
              {"accion_md": (
                  "Igualando cada factor a cero: $x - 3 = 0 \\Rightarrow x = 3$; $x^2 + 1 = 0 \\Rightarrow x = \\pm i.$\n\n"
                  "**Tres ceros:** $\\boxed{z_1 = 3, \\;\\; z_2 = i, \\;\\; z_3 = -i.}$"
               ),
               "justificacion_md": "Resolución de cada factor.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Factorización completa con $a_3 = 1$:\n"
                  "$$\\boxed{P(x) = (x - 3)(x - i)(x + i)}.$$"
               ),
               "justificacion_md": "Producto de los tres factores lineales.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cinco ceros de un polinomio de grado 5",
          problema_md=(
              "Encuentre la factorización completa y los cinco ceros del polinomio "
              "$P(x) = 3x^5 + 24x^3 + 48x.$"
          ),
          pasos=[
              {"accion_md": (
                  "Factor común $3x$: $P(x) = 3x(x^4 + 8x^2 + 16).$ "
                  "El paréntesis es un trinomio cuadrado perfecto en $x^2$: "
                  "$x^4 + 8x^2 + 16 = (x^2 + 4)^2.$"
               ),
               "justificacion_md": "Reconocimiento de TCP en $x^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "Factorizamos $x^2 + 4 = (x - 2i)(x + 2i)$. **Factorización completa:**\n"
                  "$$\\boxed{P(x) = 3x(x - 2i)^2 (x + 2i)^2.}$$"
               ),
               "justificacion_md": "Diferencia de cuadrados con $i$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cinco ceros (con multiplicidad):** $z_1 = 0$ (mult 1), $z_2 = 2i$ (mult 2), $z_3 = -2i$ (mult 2). "
                  "Total: $1 + 2 + 2 = 5$ raíces, coherente con el grado del polinomio. ✓"
               ),
               "justificacion_md": "Verificación del conteo total.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Construir polinomio de ceros y valor dados",
          problema_md=(
              "Encuentre una función polinomial $P(x)$ de grado $4$ con ceros $i, -i, 2, -2$ y con $P(3) = 25$."
          ),
          pasos=[
              {"accion_md": (
                  "Por el Teorema de Factorización: $P(x) = a(x - i)(x + i)(x - 2)(x + 2)$. "
                  "Simplificando: $P(x) = a(x^2 + 1)(x^2 - 4).$"
               ),
               "justificacion_md": "Forma factorizada con coeficiente líder $a$ a determinar.",
               "es_resultado": False},
              {"accion_md": (
                  "Imponemos $P(3) = 25$: $P(3) = a(9 + 1)(9 - 4) = a \\cdot 10 \\cdot 5 = 50a = 25 \\Rightarrow a = \\tfrac{1}{2}.$"
               ),
               "justificacion_md": "Determinación de $a$ por una condición.",
               "es_resultado": False},
              {"accion_md": (
                  "$$\\boxed{P(x) = \\tfrac{1}{2}(x^2 + 1)(x^2 - 4) = \\tfrac{1}{2}(x^4 - 3x^2 - 4).}$$"
               ),
               "justificacion_md": "Forma desarrollada final.",
               "es_resultado": True},
          ]),

        ej(
            "Polinomio con cero de multiplicidad 3",
            ("Encuentre una función polinomial $Q(x)$ de grado $4$ con ceros $-2$ "
             "(multiplicidad $3$) y $0$. ¿Es única?"),
            ["La forma general es $Q(x) = a \\cdot (x - 0)^1 (x + 2)^3$ con $a$ libre.",
             "Sin condiciones adicionales, cualquier $a \\neq 0$ funciona; tomá $a = 1$.",
             "Expandí para verificar grado y ceros."],
            ("Como $-2$ tiene multiplicidad $3$ y $0$ multiplicidad $1$, y el grado total es $4$: "
             "$Q(x) = a \\cdot x \\cdot (x + 2)^3$. Sin condición adicional, podemos tomar $a = 1$:\n\n"
             "$$\\boxed{Q(x) = x(x + 2)^3 = x^4 + 6x^3 + 12x^2 + 8x.}$$\n\n"
             "**No es única:** cualquier $Q(x) = a \\cdot x(x+2)^3$ con $a \\neq 0$ es válido. La unicidad requeriría una condición extra (por ejemplo, $Q$ en algún punto).")
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir TFA con \"todo polinomio tiene raíces reales\".** El teorema afirma raíces **complejas**, no reales.",
              "**Olvidar contar multiplicidad.** Un polinomio de grado $n$ tiene exactamente $n$ raíces **contadas con multiplicidad**.",
              "**Olvidar el coeficiente líder al construir un polinomio.** Sin él, la respuesta no es única.",
              "**Aplicar TFA en $\\mathbb{R}$.** No vale: en $\\mathbb{R}$ pueden no existir raíces (ej. $x^2 + 1$).",
          ]),

        b("resumen",
          puntos_md=[
              "**TFA:** todo polinomio en $\\mathbb{C}[x]$ de grado $\\ge 1$ tiene al menos una raíz en $\\mathbb{C}$.",
              "**Teorema de Factorización:** $P(x) = a_n(x - z_1)\\cdots(x - z_n)$ con $z_k \\in \\mathbb{C}$.",
              "**Número de raíces:** exactamente $n$, contadas con multiplicidad.",
              "**Estrategia de factorización:** agrupación → criterio racional → división sintética → fórmula cuadrática para los factores irreducibles.",
              "**Cierre del capítulo:** ya dominás polinomios complejos. Próximo capítulo: **Geometría Analítica** — rectas, cónicas y rotaciones en el plano.",
          ]),
    ]
    return {
        "id": "lec-ia-4-6-tfa",
        "title": "Teorema Fundamental del Álgebra",
        "description": "TFA, Teorema de Factorización, número exacto de raíces y construcción de polinomios.",
        "blocks": blocks,
        "duration_minutes": 50,
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

    builders = [lesson_4_1, lesson_4_2, lesson_4_3, lesson_4_4, lesson_4_5, lesson_4_6]

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
