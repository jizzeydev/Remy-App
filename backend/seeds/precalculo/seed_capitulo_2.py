"""
Seed del curso Precálculo — Capítulo 2: Funciones.

Crea el capítulo 'Funciones' bajo el curso 'precalculo' y siembra
sus 6 lecciones:

  - Definición, dominio y rango
  - Gráficas
  - Rapidez de cambio
  - Transformaciones de funciones
  - Álgebra de funciones
  - Funciones inversas

Basado en los Apuntes/Clase de Se Remonta. Idempotente.
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
# Definición, dominio y rango
# =====================================================================
def lesson_definicion_dominio_rango():
    blocks = [
        b("texto", body_md=(
            "El concepto de **función** es **el más importante** del precálculo y del cálculo. Casi todo "
            "lo que viene después — gráficas, derivadas, integrales, modelos físicos, biológicos, "
            "económicos — se construye sobre funciones.\n\n"
            "**Idea intuitiva:** una función es una **regla que asigna a cada entrada exactamente una "
            "salida**. Como una máquina: pones $x$ y sale $f(x)$.\n\n"
            "$$x \\;\\xrightarrow{\\;\\;f\\;\\;}\\; f(x).$$\n\n"
            "Ejemplos cotidianos: la función 'precio del kilo de pan' asigna a cada panadería un precio. "
            "La función 'temperatura' asigna a cada hora del día un valor. La función $f(x) = x^2$ asigna "
            "a cada número real su cuadrado.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces la **notación** $f: A \\to B$ y las palabras **dominio**, **codominio**, **rango**.\n"
            "- **Calculas el dominio** de funciones racionales, con raíces y con logaritmos.\n"
            "- Distingues **función** de relación general."
        )),

        b("definicion",
          titulo="Función",
          body_md=(
              "Una **función** $f$ de un conjunto $A$ a un conjunto $B$ es una regla que asigna **a cada "
              "elemento $x \\in A$ exactamente un elemento $f(x) \\in B$**.\n\n"
              "**Notación:**\n\n"
              "$$f : A \\to B, \\qquad x \\mapsto f(x).$$\n\n"
              "Se lee: '$f$ va de $A$ a $B$, $x$ se mapea a $f(x)$'.\n\n"
              "- $A$ es el **dominio** de $f$, denotado $\\operatorname{Dom}(f)$.\n"
              "- $B$ es el **codominio**.\n"
              "- $f(x)$ es la **imagen** (o valor) de $x$.\n"
              "- El **rango** (o **imagen** del conjunto) es $\\operatorname{Ran}(f) = \\{f(x) : x \\in A\\} \\subseteq B$.\n\n"
              "**Regla esencial:** a cada $x$ le corresponde **un único** $f(x)$. Si la 'regla' asigna dos "
              "valores distintos, no es función."
          )),

        b("definicion",
          titulo="Dominio: cómo calcularlo",
          body_md=(
              "Cuando una función se da por una **fórmula** $y = f(x)$ sin especificar el dominio, se "
              "asume el **dominio natural**: todos los reales para los que la fórmula tiene sentido.\n\n"
              "**Tres tipos de restricciones** (para el caso real):\n\n"
              "**1. División por cero — denominadores deben ser no nulos.**\n\n"
              "Para $f(x) = \\dfrac{P(x)}{Q(x)}$: anular $Q(x) = 0$ y excluir esos valores.\n\n"
              "**2. Raíz par de número negativo no existe en $\\mathbb{R}$.**\n\n"
              "Para $f(x) = \\sqrt{g(x)}$ (o cualquier raíz par): exigir $g(x) \\geq 0$.\n\n"
              "**3. Logaritmo de número no positivo no existe.**\n\n"
              "Para $f(x) = \\ln(g(x))$ o $\\log(g(x))$: exigir $g(x) > 0$ (estricto).\n\n"
              "**Procedimiento general.** Si la fórmula combina varias de estas operaciones, calcular las "
              "restricciones de **cada parte** y tomar la **intersección**. Lo que queda es el dominio."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular dominios típicos",
          problema_md=(
              "Halla el dominio de cada función:\n\n"
              "**(a)** $f(x) = 2 x^2 - 4 x + 1$, **(b)** $g(x) = \\dfrac{9}{x^2 - x}$, **(c)** $h(x) = \\sqrt{2 x - 6}$, **(d)** $k(x) = \\ln(x^2 - 5 x + 6)$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Polinomio: definido para todo real.\n\n"
                  "**$\\operatorname{Dom}(f) = \\mathbb{R}$**."
              ),
               "justificacion_md": "Sin denominadores, raíces ni logs.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Denominador $x^2 - x = x(x - 1)$. Se anula en $x = 0$ y $x = 1$.\n\n"
                  "**$\\operatorname{Dom}(g) = \\mathbb{R} \\setminus \\{0, 1\\} = (-\\infty, 0) \\cup (0, 1) \\cup (1, +\\infty)$**."
              ),
               "justificacion_md": "Excluir solo los ceros del denominador.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** Raíz cuadrada: $2 x - 6 \\geq 0 \\Rightarrow x \\geq 3$.\n\n"
                  "**$\\operatorname{Dom}(h) = [3, +\\infty)$**."
              ),
               "justificacion_md": "Raíz par exige radicando $\\geq 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(d)** Logaritmo: $x^2 - 5 x + 6 > 0$. Factorizar: $(x - 2)(x - 3) > 0$. "
                  "Tabla de signos da $x < 2$ o $x > 3$.\n\n"
                  "**$\\operatorname{Dom}(k) = (-\\infty, 2) \\cup (3, +\\infty)$**."
              ),
               "justificacion_md": "Logaritmo exige argumento **estrictamente positivo**.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Rango",
          body_md=(
              "El **rango** $\\operatorname{Ran}(f)$ es el conjunto de los valores que **efectivamente alcanza** la función al recorrer todo el dominio.\n\n"
              "**Métodos para hallarlo (depende de la función):**\n\n"
              "- **Funciones cuadráticas $f(x) = a x^2 + b x + c$:** completar cuadrados o usar el vértice. "
              "$\\operatorname{Ran}(f) = [k, +\\infty)$ si $a > 0$ y $[k, -\\infty)$... no, $(-\\infty, k]$ si $a < 0$, donde $k$ es la $y$ del vértice.\n"
              "- **Despejar $x$ en función de $y$:** identificar para qué valores de $y$ la fórmula tiene sentido.\n"
              "- **Mirar la gráfica.**\n\n"
              "**Ejemplo.** $f(x) = 2 x^2 - 4 x + 1 = 2(x - 1)^2 - 1$. Vértice en $(1, -1)$. Como $a = 2 > 0$, parábola abre hacia arriba. **Rango:** $[-1, +\\infty)$."
          )),

        b("intuicion", body_md=(
            "**Función como 'asignación'.** Pensá en la lista de alumnos de un curso. La función "
            "'edad' asigna a cada alumno un único número. La función 'apellido' asigna a cada alumno un "
            "string. Pero 'amigos' **no es función** — un alumno puede tener varios amigos.\n\n"
            "**Por qué la unicidad importa.** Si una 'regla' diera dos valores distintos para una misma "
            "entrada, todo lo que sigue (gráfica, derivada, integral) se rompe — necesitamos saber cuál "
            "valor usar. La definición de función elimina esa ambigüedad.\n\n"
            "**Dominio vs. codominio vs. rango.** El **dominio** son las entradas posibles; el **codominio** "
            "es el 'mundo' de salidas posibles (más grande); el **rango** son las salidas que **realmente "
            "se alcanzan**. Casi siempre $\\operatorname{Ran}(f) \\subsetneq B$ (estricto)."
        )),

        fig(
            "Diagrama de la 'máquina' de una función. "
            "A la izquierda, una caja con varios x's (entradas, en color teal #06b6d4) flecheando hacia una caja central etiquetada 'f' (estilo máquina industrial, en color púrpura). "
            "A la derecha, salidas f(x) (en color ámbar #f59e0b). "
            "Etiquetas: 'Dominio A' a la izquierda, 'Codominio B' a la derecha. "
            "Una de las salidas marcada como 'rango (lo que sí se alcanza)' resaltada. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El dominio natural de $f(x) = \\dfrac{1}{x - 5}$ es:",
                  "opciones_md": [
                      "$\\mathbb{R}$",
                      "**$\\mathbb{R} \\setminus \\{5\\}$**",
                      "$(5, +\\infty)$",
                      "$\\{5\\}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Excluir donde el denominador se anula.",
                  "explicacion_md": "Solo $x = 5$ vuelve cero el denominador.",
              },
              {
                  "enunciado_md": "El dominio de $f(x) = \\sqrt{x - 3}$ es:",
                  "opciones_md": [
                      "$\\mathbb{R}$",
                      "$(3, +\\infty)$",
                      "**$[3, +\\infty)$**",
                      "$\\{3\\}$",
                  ],
                  "correcta": "C",
                  "pista_md": "Raíz cuadrada exige radicando $\\geq 0$.",
                  "explicacion_md": "Incluye $x = 3$ porque $\\sqrt{0} = 0$ está bien definido.",
              },
              {
                  "enunciado_md": "El dominio de $f(x) = \\ln(x - 1)$ es:",
                  "opciones_md": [
                      "$\\mathbb{R} \\setminus \\{1\\}$",
                      "$[1, +\\infty)$",
                      "**$(1, +\\infty)$**",
                      "$\\mathbb{R}$",
                  ],
                  "correcta": "C",
                  "pista_md": "Argumento de log debe ser **estrictamente** positivo.",
                  "explicacion_md": "$\\ln(0)$ y $\\ln$ de negativos no existen en $\\mathbb{R}$.",
              },
          ]),

        ej(
            "Dominio combinado",
            "Halla el dominio de $f(x) = \\dfrac{\\sqrt{x + 4}}{x - 2}$.",
            ["Restricciones de raíz **y** de denominador."],
            (
                "Raíz: $x + 4 \\geq 0 \\Rightarrow x \\geq -4$. Denominador: $x \\neq 2$. "
                "Intersección: $\\operatorname{Dom}(f) = [-4, 2) \\cup (2, +\\infty)$."
            ),
        ),

        ej(
            "Dominio con cuadrática bajo raíz",
            "Halla el dominio de $f(x) = \\sqrt{x^2 - 9}$.",
            ["Tabla de signos de $x^2 - 9$."],
            (
                "$x^2 - 9 \\geq 0 \\Rightarrow (x - 3)(x + 3) \\geq 0$. Por tabla: $x \\leq -3$ o $x \\geq 3$. "
                "$\\operatorname{Dom}(f) = (-\\infty, -3] \\cup [3, +\\infty)$."
            ),
        ),

        ej(
            "Calcular rango",
            "Halla el rango de $f(x) = -x^2 + 4 x + 1$.",
            ["Completar cuadrados."],
            (
                "$f(x) = -(x^2 - 4 x) + 1 = -((x - 2)^2 - 4) + 1 = -(x - 2)^2 + 5$. "
                "Vértice $(2, 5)$, parábola hacia abajo. **Rango:** $(-\\infty, 5]$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir dominio con rango.** Dominio = entradas; rango = salidas.",
              "**Dejar el extremo cerrado en log.** $\\ln$ exige $> 0$ estricto, no $\\geq 0$.",
              "**Olvidar combinar restricciones cuando hay varias operaciones** (raíz **y** denominador, etc.).",
              "**Pensar que el codominio es el rango.** El codominio es el 'mundo de llegada' declarado; el rango es lo que efectivamente se alcanza.",
              "**Confundir 'definida' con 'distinta de cero'.** $f(x) = 0$ está perfectamente definida; lo que no se permite es **dividir por** cero.",
          ]),

        b("resumen",
          puntos_md=[
              "**Función:** regla que asigna a cada $x$ un único $f(x)$. Notación $f: A \\to B$.",
              "**Dominio natural:** todos los $x$ donde la fórmula tiene sentido. Restricciones: denominador $\\neq 0$, radicando par $\\geq 0$, argumento de log $> 0$.",
              "**Rango:** valores que la función efectivamente alcanza.",
              "**Próxima lección:** representación visual — gráficas de funciones.",
          ]),
    ]
    return {
        "id": "lec-prec-2-1-definicion-dominio-rango",
        "title": "Definición, dominio y rango",
        "description": "Concepto formal de función con notación f: A → B. Cálculo de dominio en presencia de denominadores, raíces y logaritmos. Rango como conjunto de valores alcanzados.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# Gráficas
# =====================================================================
def lesson_graficas():
    blocks = [
        b("texto", body_md=(
            "La **gráfica de una función** es su representación visual en el plano cartesiano. Permite "
            "**ver de un vistazo** propiedades que serían difíciles de leer de la fórmula: dónde crece, "
            "dónde decrece, dónde tiene máximos y mínimos, su simetría, sus asíntotas.\n\n"
            "**Definición.** La gráfica de $f$ es el conjunto de puntos\n\n"
            "$$\\{(x, f(x)) : x \\in \\operatorname{Dom}(f)\\}.$$\n\n"
            "Es decir: para cada $x$ del dominio, marcamos el punto $(x, f(x))$ en el plano. La unión de "
            "todos esos puntos forma la curva.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces las **gráficas básicas** que aparecen una y otra vez (lineal, cuadrática, cúbica, raíz, recíproca, valor absoluto, escalera).\n"
            "- Aplicas el **criterio de la recta vertical** para decidir si una curva es función.\n"
            "- Graficas **funciones por tramos** respetando los extremos abiertos/cerrados.\n"
            "- Lees dominio, rango, ceros y monotonía desde la gráfica."
        )),

        formulas(
            titulo="Gráficas básicas a memorizar",
            body=(
                "Saber estas formas de memoria acelera todo lo que sigue:\n\n"
                "| Función | Forma | Dominio | Rango |\n"
                "|---|---|---|---|\n"
                "| $f(x) = c$ | Recta horizontal | $\\mathbb{R}$ | $\\{c\\}$ |\n"
                "| $f(x) = m x + b$ | Recta de pendiente $m$ | $\\mathbb{R}$ | $\\mathbb{R}$ |\n"
                "| $f(x) = x^2$ | Parábola hacia arriba | $\\mathbb{R}$ | $[0, +\\infty)$ |\n"
                "| $f(x) = x^3$ | Cúbica creciente | $\\mathbb{R}$ | $\\mathbb{R}$ |\n"
                "| $f(x) = \\sqrt{x}$ | Raíz, parte superior | $[0, +\\infty)$ | $[0, +\\infty)$ |\n"
                "| $f(x) = \\sqrt[3]{x}$ | Raíz cúbica completa | $\\mathbb{R}$ | $\\mathbb{R}$ |\n"
                "| $f(x) = \\dfrac{1}{x}$ | Hipérbola con asíntotas $x = 0, y = 0$ | $\\mathbb{R} \\setminus \\{0\\}$ | $\\mathbb{R} \\setminus \\{0\\}$ |\n"
                "| $f(x) = \\dfrac{1}{x^2}$ | Hipérbola siempre positiva | $\\mathbb{R} \\setminus \\{0\\}$ | $(0, +\\infty)$ |\n"
                "| $f(x) = |x|$ | V con vértice en $(0, 0)$ | $\\mathbb{R}$ | $[0, +\\infty)$ |\n"
                "| $f(x) = \\lfloor x \\rfloor$ | Escalera (parte entera) | $\\mathbb{R}$ | $\\mathbb{Z}$ |\n\n"
                "**Truco.** Casi cualquier gráfica del precálculo se obtiene **transformando** una de estas (lección 4)."
            ),
        ),

        b("definicion",
          titulo="Criterio de la recta vertical",
          body_md=(
              "**Pregunta:** ¿una curva dibujada en el plano cartesiano es la gráfica de alguna función?\n\n"
              "**Criterio.** Una curva es la gráfica de una función **si y solo si** toda recta vertical "
              "la corta en **a lo sumo un punto**.\n\n"
              "**Razón.** Si una recta vertical $x = a$ corta la curva en dos puntos distintos $(a, y_1)$ "
              "y $(a, y_2)$, entonces a $x = a$ se le asignan dos valores — viola la unicidad.\n\n"
              "**Consecuencia.** La circunferencia $x^2 + y^2 = 1$ **no** es función ($y = \\pm \\sqrt{1 - x^2}$, "
              "dos valores). Pero $y = \\sqrt{1 - x^2}$ (semicírculo superior) **sí** lo es."
          )),

        b("ejemplo_resuelto",
          titulo="¿Es función?",
          problema_md="Indica si la ecuación define $y$ como función de $x$: **(a)** $y = x^2 + 2$, **(b)** $x^2 + y^2 = 4$, **(c)** $y^2 = x$.",
          pasos=[
              {"accion_md": (
                  "**(a)** Despejar $y$: ya está despejado. Para cada $x$ hay un único $y$. **Sí es función.**"
              ),
               "justificacion_md": "$y = x^2 + 2$ asigna $y$ unívocamente.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $y = \\pm \\sqrt{4 - x^2}$. Para cada $x \\in (-2, 2)$ hay **dos** valores. **No es función.**"
              ),
               "justificacion_md": "Es la circunferencia: una recta vertical la corta en dos puntos.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** $y = \\pm \\sqrt{x}$. Misma situación: dos valores para cada $x > 0$. **No es función.** (Pero $y = \\sqrt{x}$ por separado sí es función.)"
              ),
               "justificacion_md": "Es una parábola 'acostada' — falla el criterio.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Funciones definidas por tramos",
          body_md=(
              "Algunas funciones se definen por **distintas fórmulas** en distintos intervalos del dominio:\n\n"
              "$$f(x) = \\begin{cases} x^2 & \\text{si } x \\leq 1, \\\\ 2 x + 1 & \\text{si } x > 1. \\end{cases}$$\n\n"
              "**Para graficar:**\n\n"
              "1. **Cada tramo se grafica con su propia fórmula** sobre su intervalo.\n"
              "2. En los **extremos del intervalo**:\n"
              "  - **Punto lleno (●)** si el extremo está incluido (desigualdad no estricta $\\leq$ o $\\geq$).\n"
              "  - **Punto vacío (○)** si el extremo está excluido (desigualdad estricta $<$ o $>$).\n\n"
              "**Ejemplo.** En la función de arriba, en $x = 1$ el primer tramo da $y = 1$ (punto lleno), el segundo tramo daría $y = 3$ (punto vacío). La gráfica tiene un **salto** de $1$ a $3$.\n\n"
              "**Casos famosos:** valor absoluto $|x|$, función signo $\\operatorname{sgn}(x)$, función parte entera $\\lfloor x \\rfloor$."
          )),

        b("ejemplo_resuelto",
          titulo="Función por tramos",
          problema_md=(
              "Grafica y describe el dominio/rango de\n\n"
              "$$f(x) = \\begin{cases} -x & \\text{si } x < 0, \\\\ x^2 & \\text{si } 0 \\leq x \\leq 2, \\\\ 4 & \\text{si } x > 2. \\end{cases}$$"
          ),
          pasos=[
              {"accion_md": (
                  "**Tramo 1 ($x < 0$):** $-x$ es la recta de pendiente $-1$ por el origen, en el lado izquierdo. Punto vacío en $(0, 0)$."
              ),
               "justificacion_md": "$x < 0$ estricto.",
               "es_resultado": False},
              {"accion_md": (
                  "**Tramo 2 ($0 \\leq x \\leq 2$):** parábola $x^2$ desde $(0, 0)$ (punto lleno) hasta $(2, 4)$ (punto lleno)."
              ),
               "justificacion_md": "Ambos extremos cerrados.",
               "es_resultado": False},
              {"accion_md": (
                  "**Tramo 3 ($x > 2$):** recta horizontal $y = 4$. Punto vacío en $(2, 4)$, pero como el tramo 2 ya cubre ese punto, **no hay salto**.\n\n"
                  "**Dominio:** $\\mathbb{R}$. **Rango:** $[0, +\\infty)$ (los tramos 1 y 2 cubren $[0, +\\infty)$ y el tramo 3 agrega $\\{4\\}$ que ya está)."
              ),
               "justificacion_md": "Mirar la gráfica completa para extraer rango.",
               "es_resultado": True},
          ]),

        fig(
            "Las gráficas básicas de precálculo en una sola figura, en una grilla 3x3 o 3x4. "
            "Cada panel pequeño con ejes x/y y la gráfica correspondiente: "
            "(1) recta y=x; (2) parábola y=x²; (3) cúbica y=x³; (4) raíz y=√x; (5) raíz cúbica y=∛x; "
            "(6) hipérbola y=1/x con asíntotas; (7) y=1/x² (siempre positiva); (8) valor absoluto y=|x|; (9) escalera y=⌊x⌋. "
            "Cada panel etiquetado con su fórmula. Acentos teal #06b6d4. " + STYLE
        ),

        b("intuicion", body_md=(
            "**Por qué las gráficas son útiles.** Una fórmula te dice **qué hace** la función punto a punto. "
            "Una gráfica te muestra **el comportamiento global**: simetría, extremos, asíntotas, "
            "intersecciones con los ejes, regiones positivas/negativas. Habilidades como esbozar una "
            "gráfica rápidamente o **leer** propiedades de una gráfica son centrales en el cálculo.\n\n"
            "**Lectura de gráficas.** Desde la gráfica de $f$ podés leer:\n\n"
            "- **Dominio:** la sombra horizontal (proyección sobre el eje $x$).\n"
            "- **Rango:** la sombra vertical (proyección sobre el eje $y$).\n"
            "- **Ceros:** intersecciones con el eje $x$.\n"
            "- **Intersección con $y$:** valor $f(0)$.\n"
            "- **Crecimiento:** dónde sube, dónde baja, dónde es horizontal.\n"
            "- **Máximos y mínimos:** picos y valles."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$x^2 + y^2 = 9$ representa una circunferencia. ¿Es función de $x$?",
                  "opciones_md": [
                      "Sí, siempre",
                      "**No, una recta vertical la corta en dos puntos**",
                      "Sí, si $y > 0$",
                      "Depende del dominio",
                  ],
                  "correcta": "B",
                  "pista_md": "Aplicar criterio de la recta vertical.",
                  "explicacion_md": "Para cada $-3 < x < 3$ hay dos $y$. Falla la unicidad.",
              },
              {
                  "enunciado_md": "La gráfica de $f(x) = |x|$ es:",
                  "opciones_md": [
                      "Una recta",
                      "Una parábola",
                      "**Una 'V' con vértice en el origen**",
                      "Una hipérbola",
                  ],
                  "correcta": "C",
                  "pista_md": "$|x|$ vale $x$ para $x \\geq 0$ y $-x$ para $x < 0$.",
                  "explicacion_md": "Dos rectas que se encuentran en el origen formando una V.",
              },
              {
                  "enunciado_md": "El criterio de la recta vertical sirve para:",
                  "opciones_md": [
                      "Hallar el dominio",
                      "**Decidir si una curva es función**",
                      "Hallar el rango",
                      "Verificar continuidad",
                  ],
                  "correcta": "B",
                  "pista_md": "Lo que define a una función es la unicidad.",
                  "explicacion_md": "Una recta vertical corta máximo en un punto sii la curva es función.",
              },
          ]),

        ej(
            "Identificar gráfica básica",
            "¿Qué función básica tiene asíntotas verticales y horizontales en los ejes?",
            ["Mirar la tabla."],
            (
                "$f(x) = 1/x$ (hipérbola). Asíntota vertical $x = 0$, asíntota horizontal $y = 0$."
            ),
        ),

        ej(
            "Función por tramos",
            "Define una función por tramos que valga $-1$ si $x < 0$, $0$ si $x = 0$ y $1$ si $x > 0$. ¿Cómo se llama?",
            ["Es una función famosa."],
            (
                "$\\operatorname{sgn}(x) = \\begin{cases} -1 & x < 0 \\\\ 0 & x = 0 \\\\ 1 & x > 0 \\end{cases}$. Es la **función signo**. Tiene salto en $x = 0$."
            ),
        ),

        ej(
            "Lectura de gráfica",
            "Si la gráfica de $f$ pasa por $(0, 3), (1, 0), (2, -1), (3, 0)$ y es continua, ¿cuáles son los ceros y el valor de $f(0)$?",
            ["Ceros = donde la gráfica corta el eje $x$."],
            (
                "Ceros: $x = 1$ y $x = 3$ (donde $f = 0$). $f(0) = 3$ (intersección con eje $y$)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar marcar puntos abiertos/cerrados** en gráficas por tramos. Cambia totalmente el dominio y el rango.",
              "**Confundir 'curva continua' con 'función'.** La circunferencia es continua pero no es función.",
              "**Aplicar el criterio de la recta horizontal** (que sirve para inyectividad, lección 6) cuando lo que quiero es saber si es función.",
              "**Dibujar la raíz cuadrada incluyendo la mitad inferior.** $\\sqrt{x}$ siempre $\\geq 0$ (la raíz principal). Solo la mitad superior.",
              "**Olvidar que $1/x$ no toca los ejes.** Tiene asíntotas, no ceros.",
          ]),

        b("resumen",
          puntos_md=[
              "**Gráfica:** conjunto de puntos $(x, f(x))$ en el plano.",
              "**Criterio recta vertical:** una curva es función sii toda vertical la corta máximo en un punto.",
              "**Funciones por tramos:** distintas fórmulas en distintos intervalos. Cuidar puntos abiertos/cerrados.",
              "**Memorizar gráficas básicas:** lineal, cuadrática, cúbica, raíz, recíproca, valor absoluto, escalera.",
              "**Próxima lección:** medir cuánto cambia una función — rapidez de cambio.",
          ]),
    ]
    return {
        "id": "lec-prec-2-2-graficas",
        "title": "Gráficas",
        "description": "Representación gráfica de funciones, criterio de la recta vertical, gráficas básicas de referencia (lineal, cuadrática, cúbica, raíz, recíproca, valor absoluto), funciones definidas por tramos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# Rapidez de cambio
# =====================================================================
def lesson_rapidez_de_cambio():
    blocks = [
        b("texto", body_md=(
            "La **rapidez de cambio** de una función mide **cuánto cambia el valor de salida cuando cambia "
            "el valor de entrada**. Es la noción clave que conecta el precálculo con el cálculo "
            "diferencial: la **derivada** es la rapidez de cambio **instantánea**.\n\n"
            "Antes de llegar a la derivada, en precálculo trabajamos la **rapidez de cambio promedio**, "
            "que coincide con la **pendiente de la recta secante** entre dos puntos de la gráfica.\n\n"
            "**Aplicaciones cotidianas:**\n\n"
            "- **Velocidad** = rapidez de cambio de la posición respecto al tiempo.\n"
            "- **Aceleración** = rapidez de cambio de la velocidad.\n"
            "- **Tasa de inflación** = rapidez de cambio del nivel de precios.\n"
            "- **Crecimiento poblacional** = rapidez de cambio del número de habitantes.\n\n"
            "**Al terminar:**\n\n"
            "- Calculas la **rapidez de cambio promedio** entre dos puntos.\n"
            "- La interpretás como **pendiente de la recta secante**.\n"
            "- Aplicás el concepto a problemas con datos reales (tablas de temperatura, posición, etc.)."
        )),

        b("definicion",
          titulo="Rapidez de cambio promedio",
          body_md=(
              "Sea $f$ una función y $a, b$ dos puntos del dominio con $a \\neq b$. La **rapidez de cambio "
              "promedio** de $f$ entre $x = a$ y $x = b$ es\n\n"
              "$$\\boxed{\\,\\text{RCP} = \\dfrac{f(b) - f(a)}{b - a} = \\dfrac{\\Delta y}{\\Delta x}.\\,}$$\n\n"
              "**Interpretaciones:**\n\n"
              "- Es la **pendiente de la recta secante** entre los puntos $(a, f(a))$ y $(b, f(b))$ de la gráfica.\n"
              "- Es el **cambio promedio en $y$ por unidad de cambio en $x$** en ese intervalo.\n\n"
              "**Signo:**\n\n"
              "- $\\text{RCP} > 0$: en promedio $f$ **crece** en el intervalo.\n"
              "- $\\text{RCP} < 0$: en promedio $f$ **decrece**.\n"
              "- $\\text{RCP} = 0$: $f(a) = f(b)$ — los extremos coinciden, aunque adentro pueda hacer cualquier cosa.\n\n"
              "**Notación.** Algunos textos escriben $\\Delta f / \\Delta x$ o $f'_{[a, b]}$. El concepto es el mismo."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular RCP",
          problema_md="Para $f(x) = (x - 3)^2$, calcula la RCP entre **(a)** $x = 1$ y $x = 3$, **(b)** $x = 4$ y $x = 7$.",
          pasos=[
              {"accion_md": (
                  "**(a)** $f(1) = (1 - 3)^2 = 4$. $f(3) = 0$.\n\n"
                  "$\\text{RCP} = \\dfrac{0 - 4}{3 - 1} = \\dfrac{-4}{2} = -2$.\n\n"
                  "$f$ en promedio **decrece** $2$ unidades por unidad de $x$ en este intervalo."
              ),
               "justificacion_md": "Notar el signo negativo: la parábola viene bajando hacia el vértice.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $f(4) = 1$, $f(7) = 16$.\n\n"
                  "$\\text{RCP} = \\dfrac{16 - 1}{7 - 4} = \\dfrac{15}{3} = 5$.\n\n"
                  "Aquí la parábola viene **subiendo** después del vértice. RCP positiva y grande."
              ),
               "justificacion_md": "**Lección clave:** la RCP **depende del intervalo**. Una misma función puede tener RCP muy distintas en intervalos distintos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Aplicación a datos reales",
          problema_md=(
              "Una tabla registra la temperatura de un día (en $^\\circ$F) cada cierta hora:\n\n"
              "| Hora | 8:00 | 9:00 | 13:00 | 15:00 | 16:00 | 19:00 |\n"
              "|---|---|---|---|---|---|---|\n"
              "| Temp. | 38 | 40 | 62 | 67 | 64 | 51 |\n\n"
              "Calcula la RCP de temperatura entre 8 y 9 h, entre 13 y 15 h, y entre 16 y 19 h."
          ),
          pasos=[
              {"accion_md": (
                  "**8:00 a 9:00:** $\\dfrac{40 - 38}{9 - 8} = 2$ $^\\circ$F/h. Sube $2^\\circ$ por hora."
              ),
               "justificacion_md": "Mañana tibia, calentando.",
               "es_resultado": False},
              {"accion_md": (
                  "**13:00 a 15:00:** $\\dfrac{67 - 62}{15 - 13} = 2{,}5$ $^\\circ$F/h. Sigue subiendo, un poco más rápido."
              ),
               "justificacion_md": "Pico de temperatura del mediodía-tarde.",
               "es_resultado": False},
              {"accion_md": (
                  "**16:00 a 19:00:** $\\dfrac{51 - 64}{19 - 16} = \\dfrac{-13}{3} \\approx -4{,}3$ $^\\circ$F/h. **Negativo:** baja $4{,}3^\\circ$ por hora.\n\n"
                  "**Lección.** Mismo conjunto de datos, tres RCP muy distintas según el intervalo. La RCP describe el comportamiento **promedio**, no instantáneo."
              ),
               "justificacion_md": "Atardecer, enfriamiento rápido.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Conexión con la derivada (preview del cálculo).** La RCP entre $a$ y $b$ es la pendiente "
            "de la recta secante. Si hacemos $b \\to a$ (los puntos se acercan), la secante se vuelve "
            "**tangente** y la pendiente se vuelve la **derivada** $f'(a)$ — la **rapidez instantánea** "
            "en el punto $a$.\n\n"
            "$$f'(a) = \\lim_{b \\to a} \\dfrac{f(b) - f(a)}{b - a}.$$\n\n"
            "Eso ya es cálculo. En precálculo trabajamos la versión 'discreta' (entre dos puntos), que es "
            "el escalón conceptual previo.\n\n"
            "**Funciones lineales y RCP constante.** Para $f(x) = m x + b$, la RCP entre cualesquiera dos "
            "puntos es exactamente $m$ — la pendiente. Por eso decimos que las funciones lineales tienen "
            "**rapidez de cambio constante**. Cualquier función no lineal tiene RCP variable según el intervalo."
        )),

        fig(
            "Una parábola y = (x-3)² dibujada en color teal #06b6d4. "
            "Dos rectas secantes superpuestas en color ámbar #f59e0b: "
            "una entre los puntos (1, 4) y (3, 0) — etiquetada 'RCP = -2', con pendiente negativa; "
            "otra entre los puntos (4, 1) y (7, 16) — etiquetada 'RCP = 5', con pendiente positiva. "
            "Cada secante con sus dos puntos marcados (círculos llenos negros). "
            "Eje x de -1 a 8, eje y de 0 a 18. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para $f(x) = 3 x + 1$, la RCP entre cualesquiera dos puntos es:",
                  "opciones_md": [
                      "Depende de los puntos",
                      "**Siempre $3$**",
                      "Siempre $1$",
                      "Cero",
                  ],
                  "correcta": "B",
                  "pista_md": "Es función lineal con pendiente $3$.",
                  "explicacion_md": "RCP de una función lineal = la pendiente, constante.",
              },
              {
                  "enunciado_md": "Si la RCP de $f$ entre $a$ y $b$ es $0$, entonces:",
                  "opciones_md": [
                      "$f$ es constante",
                      "**$f(a) = f(b)$, pero $f$ puede no ser constante en el medio**",
                      "$f$ no está definida",
                      "$a = b$",
                  ],
                  "correcta": "B",
                  "pista_md": "Solo se compara los extremos.",
                  "explicacion_md": "Por ejemplo, una parábola entre dos puntos simétricos al vértice tiene RCP = 0 pero no es constante.",
              },
              {
                  "enunciado_md": "Geométricamente, la RCP entre $(a, f(a))$ y $(b, f(b))$ es:",
                  "opciones_md": [
                      "El área bajo la curva",
                      "**La pendiente de la recta secante**",
                      "La distancia entre los puntos",
                      "El valor mínimo de $f$",
                  ],
                  "correcta": "B",
                  "pista_md": "Es exactamente la fórmula de pendiente.",
                  "explicacion_md": "$\\dfrac{y_2 - y_1}{x_2 - x_1}$ = pendiente.",
              },
          ]),

        ej(
            "RCP cúbica",
            "Calcula la RCP de $f(x) = x^3$ entre $x = 1$ y $x = 3$.",
            ["Evaluar y dividir."],
            (
                "$f(1) = 1$, $f(3) = 27$. RCP $= (27 - 1)/(3 - 1) = 26/2 = 13$."
            ),
        ),

        ej(
            "Velocidad promedio",
            "Un objeto se mueve según $s(t) = 5 t^2$ (metros, segundos). ¿Cuál es su velocidad promedio entre $t = 1$ y $t = 4$?",
            ["RCP de $s$."],
            (
                "$s(1) = 5$, $s(4) = 80$. $v_\\text{prom} = (80 - 5)/(4 - 1) = 75/3 = 25$ m/s."
            ),
        ),

        ej(
            "Cuándo crece y cuándo decrece",
            "Para $f(x) = x^2 - 6 x + 5$, calcula RCP entre $x = 0$ y $x = 3$, y entre $x = 3$ y $x = 6$. ¿Qué muestra eso del comportamiento de $f$?",
            ["Calcular ambas y comparar signos."],
            (
                "$f(0) = 5, f(3) = -4, f(6) = 5$. RCP$_{[0,3]} = (-4 - 5)/3 = -3$ (decrece). RCP$_{[3,6]} = (5 - (-4))/3 = 3$ (crece). El vértice está en $x = 3$ (mínimo), y la parábola decrece antes y crece después."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\Delta y / \\Delta x$ con $\\Delta x / \\Delta y$.** El cambio de $y$ va arriba.",
              "**Olvidar que la RCP depende del intervalo.** No tiene sentido decir 'la RCP de $f(x) = x^2$', hay que especificar entre qué dos puntos.",
              "**Tomar $a = b$ en la fórmula.** Da $0/0$, indefinido. Solo en cálculo (con límite) se le da sentido a la rapidez 'instantánea'.",
              "**Confundir RCP con cambio total.** Cambio total = $f(b) - f(a)$. RCP = ese cambio dividido por $\\Delta x$.",
              "**Olvidar las unidades.** Si $x$ es horas y $y$ son metros, la RCP es metros/hora.",
          ]),

        b("resumen",
          puntos_md=[
              "**RCP** entre $a$ y $b$: $\\dfrac{f(b) - f(a)}{b - a}$ = pendiente de la recta secante.",
              "**Signo:** positivo (crece), negativo (decrece), cero (extremos coinciden).",
              "**Función lineal:** RCP constante (= pendiente).",
              "**Antesala de la derivada:** $f'(a) = \\lim_{b \\to a} \\text{RCP}$.",
              "**Próxima lección:** cómo modificar una gráfica conocida — transformaciones.",
          ]),
    ]
    return {
        "id": "lec-prec-2-3-rapidez-de-cambio",
        "title": "Rapidez de cambio",
        "description": "Rapidez de cambio promedio de una función entre dos puntos como pendiente de la recta secante. Interpretación, signo, dependencia del intervalo y aplicaciones a datos reales.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 3,
    }


# =====================================================================
# Transformaciones de funciones
# =====================================================================
def lesson_transformaciones():
    blocks = [
        b("texto", body_md=(
            "**Idea clave de esta lección.** En vez de graficar de cero cualquier función, podemos partir "
            "de unas pocas **funciones básicas** ($x^2, |x|, \\sqrt{x}, 1/x$, etc.) y obtener miles de "
            "gráficas distintas aplicándoles **transformaciones rígidas** y **estiramientos**.\n\n"
            "Las cinco transformaciones fundamentales son:\n\n"
            "1. **Traslación vertical** (sumar/restar constante a $f$).\n"
            "2. **Traslación horizontal** (sumar/restar dentro del argumento).\n"
            "3. **Estiramiento o compresión vertical** (multiplicar $f$ por una constante).\n"
            "4. **Estiramiento o compresión horizontal** (multiplicar el argumento).\n"
            "5. **Reflexión** respecto a uno de los ejes.\n\n"
            "Con estas, transformamos $y = x^2$ en $y = -2(x - 3)^2 + 5$ sin necesidad de tabla de valores.\n\n"
            "**Al terminar:**\n\n"
            "- Identificás cada transformación a partir de la fórmula.\n"
            "- Graficás funciones complejas paso a paso.\n"
            "- Reconocés **funciones pares e impares** y su simetría."
        )),

        formulas(
            titulo="Las cinco transformaciones",
            body=(
                "Sea $y = f(x)$ la función base. Aplicar:\n\n"
                "**1. Traslación vertical** $y = f(x) + k$:\n"
                "- $k > 0$: gráfica **sube** $k$ unidades.\n"
                "- $k < 0$: gráfica **baja** $|k|$ unidades.\n\n"
                "**2. Traslación horizontal** $y = f(x - h)$:\n"
                "- $h > 0$: gráfica se mueve $h$ unidades a la **derecha**.\n"
                "- $h < 0$: gráfica se mueve $|h|$ unidades a la **izquierda**.\n\n"
                "**Atención al signo.** $f(x - 3)$ se mueve a la **derecha**, no a la izquierda. La intuición correcta: $x = 3$ es donde 'antes' valía $x = 0$.\n\n"
                "**3. Estiramiento/compresión vertical** $y = a \\cdot f(x)$ con $a > 0$:\n"
                "- $a > 1$: **estira** verticalmente (alarga).\n"
                "- $0 < a < 1$: **comprime** verticalmente (achata).\n\n"
                "**4. Estiramiento/compresión horizontal** $y = f(b \\cdot x)$ con $b > 0$:\n"
                "- $b > 1$: **comprime** horizontalmente (encoge).\n"
                "- $0 < b < 1$: **estira** horizontalmente.\n\n"
                "Notar que el efecto es **al revés** que en vertical — el horizontal es contraintuitivo.\n\n"
                "**5. Reflexiones**:\n"
                "- $y = -f(x)$: refleja respecto al **eje $x$** (gráfica boca arriba).\n"
                "- $y = f(-x)$: refleja respecto al **eje $y$** (espejo izquierda-derecha).\n\n"
                "**Combinaciones.** Se aplican en cierto **orden**: primero las del argumento (horizontales), luego las externas (verticales). Una expresión típica $y = a \\cdot f(b(x - h)) + k$ combina las cinco."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Graficar por transformaciones",
          problema_md="Grafica $y = (x - 3)^2 + 5$ partiendo de $y = x^2$.",
          pasos=[
              {"accion_md": (
                  "**Función base:** $y = x^2$ (parábola con vértice en el origen)."
              ),
               "justificacion_md": "Identificar la base.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 1: $(x - 3)^2$ — traslación horizontal a la derecha 3 unidades.** Vértice se mueve a $(3, 0)$."
              ),
               "justificacion_md": "El $-3$ adentro mueve a la **derecha**.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2: $(x - 3)^2 + 5$ — traslación vertical hacia arriba 5 unidades.** Vértice final: $(3, 5)$.\n\n"
                  "**Forma final:** parábola idéntica a $y = x^2$, pero con vértice trasladado a $(3, 5)$."
              ),
               "justificacion_md": "Las traslaciones no cambian la forma, solo la posición.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Combinación con reflexión y estiramiento",
          problema_md="Grafica $y = -2 |x + 1| + 3$ partiendo de $y = |x|$.",
          pasos=[
              {"accion_md": (
                  "**Base:** $y = |x|$ (V con vértice en $(0, 0)$).\n\n"
                  "**Paso 1: $|x + 1|$ — traslación a la izquierda 1.** Vértice en $(-1, 0)$."
              ),
               "justificacion_md": "$x + 1 = x - (-1)$, así $h = -1$, mueve a la izquierda.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2: $2 |x + 1|$ — estiramiento vertical por 2.** La V se vuelve más empinada."
              ),
               "justificacion_md": "Cada $y$ se duplica.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3: $-2 |x + 1|$ — reflexión respecto al eje $x$.** La V apunta hacia abajo (vértice arriba, brazos hacia abajo). Vértice sigue en $(-1, 0)$."
              ),
               "justificacion_md": "Multiplicar por $-1$ refleja sobre $x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 4: $-2 |x + 1| + 3$ — traslación hacia arriba 3.** Vértice final: $(-1, 3)$. **Forma final:** V invertida, ancho $1/2$ (más empinada que la original), vértice arriba en $(-1, 3)$."
              ),
               "justificacion_md": "Sumar 3 mueve todo arriba.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Funciones pares e impares",
          body_md=(
              "Estos casos especiales corresponden a simetrías particulares.\n\n"
              "**Función par:** $f(-x) = f(x)$ para todo $x \\in \\operatorname{Dom}(f)$. **Simetría respecto al eje $y$**.\n\n"
              "Ejemplos: $f(x) = x^2$, $f(x) = x^4$, $f(x) = |x|$, $f(x) = \\cos x$ (verás trigonometría más adelante).\n\n"
              "**Función impar:** $f(-x) = -f(x)$ para todo $x$. **Simetría respecto al origen** (rotar $180^\\circ$ deja la gráfica igual).\n\n"
              "Ejemplos: $f(x) = x^3$, $f(x) = x^5$, $f(x) = 1/x$, $f(x) = \\sin x$.\n\n"
              "**Cómo testear.** Calcular $f(-x)$ y compararlo con $f(x)$ y con $-f(x)$:\n\n"
              "- Si $f(-x) = f(x)$: **par**.\n"
              "- Si $f(-x) = -f(x)$: **impar**.\n"
              "- Si no es ni una ni la otra: **ninguna de las dos** (la mayoría de funciones).\n\n"
              "**Importante.** Una función puede ser **ni par ni impar**. Solo $f \\equiv 0$ es par e impar simultáneamente."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar paridad",
          problema_md="¿Es $f(x) = 3 x^3 + 2 x^2 + 1$ par, impar o ninguna?",
          pasos=[
              {"accion_md": (
                  "**Calcular $f(-x)$:** $3(-x)^3 + 2(-x)^2 + 1 = -3 x^3 + 2 x^2 + 1$."
              ),
               "justificacion_md": "Reemplazar $x$ por $-x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Comparar:** $f(x) = 3 x^3 + 2 x^2 + 1$ ¿$= -3 x^3 + 2 x^2 + 1$? No (los términos cúbicos difieren).\n\n"
                  "$-f(x) = -3 x^3 - 2 x^2 - 1$ ¿$= -3 x^3 + 2 x^2 + 1$? No (los términos cuadrático y constante difieren).\n\n"
                  "**Conclusión:** **ni par ni impar.**"
              ),
               "justificacion_md": "Mezcla de potencias pares ($x^2, 1$) e impares ($x^3$) rompe ambas simetrías.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué horizontales 'al revés'.** $f(x - 3)$ se mueve a la **derecha** (no a la izquierda) porque el "
            "punto que en $f$ valía '0' (el origen) ahora corresponde a $x - 3 = 0 \\Rightarrow x = 3$. Es decir, "
            "el 'cero del argumento' se desplazó a $x = 3$, llevando toda la gráfica con él.\n\n"
            "**Estiramiento horizontal contraintuitivo.** $f(2 x)$ **comprime** porque ahora el valor que "
            "antes alcanzabas en $x = 4$ lo alcanzas en $x = 2$ (la mitad). Todo se acerca al eje $y$.\n\n"
            "**Pares vs impares.** Una función polinómica $\\sum a_n x^n$ es **par** si solo aparecen "
            "potencias **pares** de $x$ (más constante), e **impar** si solo aparecen potencias **impares**. "
            "Mezclar pares e impares rompe la simetría."
        )),

        fig(
            "Cuatro paneles 2x2 mostrando transformaciones de la parábola y = x². "
            "Panel superior izq: la parábola base y=x² en gris (referencia) y la parábola desplazada y=(x-3)² en teal #06b6d4 con vértice en (3,0). "
            "Panel superior der: parábola y=x²+5 en ámbar #f59e0b con vértice en (0,5) (traslación vertical). "
            "Panel inferior izq: parábola y=2x² (estirada) y y=(1/2)x² (achatada), ambas con vértice en origen, en colores distintos. "
            "Panel inferior der: parábola y=-x² reflejada (boca abajo). "
            "Cada panel etiquetado claramente. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$y = f(x + 4)$ desplaza la gráfica de $f$:",
                  "opciones_md": [
                      "4 unidades a la derecha",
                      "**4 unidades a la izquierda**",
                      "4 unidades hacia arriba",
                      "4 unidades hacia abajo",
                  ],
                  "correcta": "B",
                  "pista_md": "$x + 4 = x - (-4)$, así $h = -4$.",
                  "explicacion_md": "Sumar dentro del argumento mueve a la izquierda.",
              },
              {
                  "enunciado_md": "$f(x) = x^4 - 3 x^2$ es:",
                  "opciones_md": [
                      "Impar",
                      "**Par**",
                      "Ninguna",
                      "Ambas",
                  ],
                  "correcta": "B",
                  "pista_md": "Solo potencias pares.",
                  "explicacion_md": "$f(-x) = (-x)^4 - 3(-x)^2 = x^4 - 3 x^2 = f(x)$. **Par.**",
              },
              {
                  "enunciado_md": "La gráfica de $y = -f(x)$ es:",
                  "opciones_md": [
                      "Reflexión respecto al eje $y$",
                      "**Reflexión respecto al eje $x$**",
                      "Traslación hacia abajo",
                      "Inversión de $f$",
                  ],
                  "correcta": "B",
                  "pista_md": "El menos afuera invierte $y$.",
                  "explicacion_md": "Cada punto $(x, y)$ va a $(x, -y)$.",
              },
          ]),

        ej(
            "Identificar transformaciones",
            "Describe las transformaciones aplicadas a $y = \\sqrt{x}$ para obtener $y = -\\sqrt{x - 2} + 4$.",
            ["Identificar uno por uno."],
            (
                "1. $\\sqrt{x - 2}$: traslación a la derecha 2.\n"
                "2. $-\\sqrt{x - 2}$: reflexión respecto al eje $x$.\n"
                "3. $-\\sqrt{x - 2} + 4$: traslación hacia arriba 4. "
                "Resultado: gráfica de $\\sqrt{x}$ reflejada hacia abajo, con punto inicial en $(2, 4)$ en lugar de $(0, 0)$."
            ),
        ),

        ej(
            "Paridad",
            "¿Es $f(x) = x \\cdot |x|$ par, impar o ninguna?",
            ["Calcular $f(-x)$ con cuidado del valor absoluto."],
            (
                "$f(-x) = (-x) \\cdot |-x| = -x \\cdot |x| = -f(x)$. **Impar.**"
            ),
        ),

        ej(
            "Transformación combinada",
            "A $y = x^3$ le aplicamos: traslación derecha 1, estiramiento vertical por 3, traslación abajo 2. ¿Cuál es la fórmula final?",
            ["Componer en orden."],
            (
                "$y = 3(x - 1)^3 - 2$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir el sentido de traslación horizontal.** $f(x - 3)$ va a la derecha, no a la izquierda.",
              "**Confundir estiramiento vertical y horizontal.** $a f(x)$ estira en $y$; $f(b x)$ con $b > 1$ comprime en $x$.",
              "**Aplicar transformaciones en cualquier orden.** El orden importa: primero las del argumento (horizontales), luego las externas (verticales).",
              "**Suponer que toda función es par o impar.** La mayoría no lo es.",
              "**Confundir 'reflexión sobre eje $x$' con 'sobre eje $y$'.** $-f(x)$ refleja sobre $x$; $f(-x)$ refleja sobre $y$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Traslación vertical** $f(x) + k$, **horizontal** $f(x - h)$.",
              "**Estiramiento vertical** $a f(x)$ ($a > 1$ estira); **horizontal** $f(b x)$ ($b > 1$ comprime).",
              "**Reflexiones:** $-f(x)$ sobre eje $x$; $f(-x)$ sobre eje $y$.",
              "**Función par:** $f(-x) = f(x)$, simetría respecto al eje $y$. **Impar:** $f(-x) = -f(x)$, simetría respecto al origen.",
              "**Próxima lección:** combinar funciones — álgebra y composición.",
          ]),
    ]
    return {
        "id": "lec-prec-2-4-transformaciones",
        "title": "Transformaciones de funciones",
        "description": "Traslaciones verticales y horizontales, estiramientos/compresiones, reflexiones respecto a los ejes y combinaciones. Funciones pares e impares y simetría.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# Álgebra de funciones
# =====================================================================
def lesson_algebra_funciones():
    blocks = [
        b("texto", body_md=(
            "Así como sumamos, restamos, multiplicamos y dividimos números, podemos hacer las **mismas "
            "operaciones con funciones**. Y además aparece una operación nueva, exclusiva de funciones: "
            "la **composición**, que consiste en aplicar una función al resultado de otra.\n\n"
            "$$x \\;\\xrightarrow{\\;g\\;}\\; g(x) \\;\\xrightarrow{\\;f\\;}\\; f(g(x)).$$\n\n"
            "La composición es central en cálculo: la **regla de la cadena** para derivadas se basa "
            "íntegramente en cómo descomponer y recomponer funciones.\n\n"
            "**Al terminar:**\n\n"
            "- Calculas $f + g, f - g, f \\cdot g, f / g$ y sus dominios.\n"
            "- Calculas $(f \\circ g)(x) = f(g(x))$ y su dominio.\n"
            "- Reconoces que $f \\circ g \\neq g \\circ f$ en general (no es conmutativa)."
        )),

        formulas(
            titulo="Operaciones algebraicas",
            body=(
                "Sean $f$ y $g$ funciones reales. Definimos:\n\n"
                "$$\\boxed{(f + g)(x) = f(x) + g(x)},$$\n"
                "$$\\boxed{(f - g)(x) = f(x) - g(x)},$$\n"
                "$$\\boxed{(f \\cdot g)(x) = f(x) \\cdot g(x)},$$\n"
                "$$\\boxed{\\left(\\dfrac{f}{g}\\right)(x) = \\dfrac{f(x)}{g(x)}, \\quad g(x) \\neq 0}.$$\n\n"
                "**Dominios:**\n\n"
                "- Para suma, resta y producto: $\\operatorname{Dom}(f) \\cap \\operatorname{Dom}(g)$.\n"
                "- Para cociente: $\\operatorname{Dom}(f) \\cap \\operatorname{Dom}(g) \\setminus \\{x : g(x) = 0\\}$.\n\n"
                "Es decir: la función combinada está definida solo donde **ambas** funciones originales lo "
                "están y, en el caso del cociente, **además** donde $g$ no se anula."
            ),
        ),

        b("definicion",
          titulo="Composición $f \\circ g$",
          body_md=(
              "La **composición** de $f$ con $g$ es la función definida por\n\n"
              "$$\\boxed{(f \\circ g)(x) = f(g(x)).}$$\n\n"
              "**Procedimiento:** primero aplicar $g$ a $x$ (obtener $g(x)$), después aplicar $f$ al resultado.\n\n"
              "**Atención al orden.** En $f \\circ g$, **primero actúa $g$**, luego $f$ — al revés del orden de lectura.\n\n"
              "**Dominio de la composición:**\n\n"
              "$$\\operatorname{Dom}(f \\circ g) = \\{x \\in \\operatorname{Dom}(g) : g(x) \\in \\operatorname{Dom}(f)\\}.$$\n\n"
              "Es decir: $x$ tiene que estar en el dominio de $g$ **y** $g(x)$ tiene que poder ser entrada válida para $f$.\n\n"
              "**No es conmutativa.** En general $f \\circ g \\neq g \\circ f$. Calcular ambas y comparar es un buen ejercicio."
          )),

        b("ejemplo_resuelto",
          titulo="Operaciones básicas",
          problema_md="Sean $f(x) = \\sqrt{x}$ y $g(x) = \\dfrac{1}{x - 1}$. Calcula $(f + g)(x)$ y su dominio.",
          pasos=[
              {"accion_md": (
                  "**Suma:** $(f + g)(x) = \\sqrt{x} + \\dfrac{1}{x - 1}$."
              ),
               "justificacion_md": "Sumar punto a punto.",
               "es_resultado": False},
              {"accion_md": (
                  "**Dominios individuales:** $\\operatorname{Dom}(f) = [0, +\\infty)$, $\\operatorname{Dom}(g) = \\mathbb{R} \\setminus \\{1\\}$.\n\n"
                  "**Intersección:** $[0, +\\infty) \\cap (\\mathbb{R} \\setminus \\{1\\}) = [0, 1) \\cup (1, +\\infty)$."
              ),
               "justificacion_md": "Excluir $x = 1$ del dominio de $f$, que era $[0, +\\infty)$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Composición",
          problema_md="Sean $f(x) = x^3 + 2$ y $g(x) = \\sqrt[3]{x}$. Calcula $(f \\circ g)(x)$ y $(g \\circ f)(x)$.",
          pasos=[
              {"accion_md": (
                  "**$(f \\circ g)(x) = f(g(x)) = f(\\sqrt[3]{x}) = (\\sqrt[3]{x})^3 + 2 = x + 2$.**"
              ),
               "justificacion_md": "Aplicar $f$ al resultado de $g$.",
               "es_resultado": False},
              {"accion_md": (
                  "**$(g \\circ f)(x) = g(f(x)) = g(x^3 + 2) = \\sqrt[3]{x^3 + 2}$.**"
              ),
               "justificacion_md": "Distinto de $f \\circ g$. Confirma la no conmutatividad.",
               "es_resultado": False},
              {"accion_md": (
                  "**Dominios.** Ambas raíces cúbicas y polinomios están definidos en todo $\\mathbb{R}$, así que $\\operatorname{Dom}(f \\circ g) = \\operatorname{Dom}(g \\circ f) = \\mathbb{R}$."
              ),
               "justificacion_md": "Caso 'sin restricciones'.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Composición con restricciones",
          problema_md="Sean $f(x) = \\sqrt{x + 2}$ y $g(x) = \\dfrac{1}{x - 1}$. Calcula $(f \\circ g)(x)$ y su dominio.",
          pasos=[
              {"accion_md": (
                  "**$(f \\circ g)(x) = f(g(x)) = \\sqrt{g(x) + 2} = \\sqrt{\\dfrac{1}{x - 1} + 2} = \\sqrt{\\dfrac{1 + 2(x - 1)}{x - 1}} = \\sqrt{\\dfrac{2 x - 1}{x - 1}}.$**"
              ),
               "justificacion_md": "Sumar fracciones para obtener una sola expresión bajo la raíz.",
               "es_resultado": False},
              {"accion_md": (
                  "**Dominio:** dos restricciones a la vez:\n\n"
                  "1. $x \\in \\operatorname{Dom}(g)$: $x \\neq 1$.\n"
                  "2. $g(x) + 2 \\geq 0$: $\\dfrac{2 x - 1}{x - 1} \\geq 0$.\n\n"
                  "Tabla de signos para el cociente: puntos críticos $x = 1/2, 1$. El cociente $\\geq 0$ en $(-\\infty, 1/2] \\cup (1, +\\infty)$ (notar: $x = 1$ excluido)."
              ),
               "justificacion_md": "Combinar restricción de $g$ y de la composición $f$ aplicada a $g$.",
               "es_resultado": False},
              {"accion_md": "**Dominio:** $(-\\infty, 1/2] \\cup (1, +\\infty)$.",
               "justificacion_md": "El extremo $1/2$ se incluye (numerador cero permite raíz cero); $1$ siempre excluido.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Composición = 'enchufar' funciones.** Pensa en $g$ como un primer paso (preparar la entrada) "
            "y $f$ como el segundo paso. Por ejemplo: 'multiplicar por 3' (g) seguido de 'sumar 5' (f) "
            "produce $f(g(x)) = 3 x + 5$. En el orden inverso: $g(f(x)) = 3 (x + 5) = 3 x + 15$. **Distinto.**\n\n"
            "**Por qué la composición aparece en cálculo.** Casi cualquier función 'compleja' se puede "
            "ver como composición de funciones más simples. La derivada de una composición sigue una "
            "regla específica (la **regla de la cadena**): $(f \\circ g)'(x) = f'(g(x)) \\cdot g'(x)$. Sin "
            "saber descomponer en composición, la regla no se puede aplicar.\n\n"
            "**Ejemplo de descomposición.** $h(x) = (x^2 + 1)^5$ es $f \\circ g$ con $g(x) = x^2 + 1$ y "
            "$f(u) = u^5$. Esto es lo que veremos sistemáticamente en cálculo."
        )),

        fig(
            "Diagrama de la composición f ∘ g como dos cajas-máquina conectadas en serie. "
            "A la izquierda x entra (en color teal #06b6d4), pasa por la caja 'g', sale como g(x), "
            "pasa por la caja 'f', sale como f(g(x)) (en color ámbar #f59e0b). "
            "Etiqueta arriba: '(f ∘ g)(x) = f(g(x))' destacada. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$(f \\circ g)(x) = $",
                  "opciones_md": [
                      "$f(x) g(x)$",
                      "**$f(g(x))$**",
                      "$g(f(x))$",
                      "$f(x) + g(x)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Definición de composición.",
                  "explicacion_md": "$f$ aplicada al resultado de $g$.",
              },
              {
                  "enunciado_md": "Si $f(x) = x + 1$ y $g(x) = x^2$, entonces $(g \\circ f)(2) = $",
                  "opciones_md": [
                      "$3$",
                      "$5$",
                      "**$9$**",
                      "$8$",
                  ],
                  "correcta": "C",
                  "pista_md": "Primero $f(2) = 3$, después $g(3) = 9$.",
                  "explicacion_md": "$g(f(2)) = g(3) = 9$.",
              },
              {
                  "enunciado_md": "El dominio de $(f/g)(x)$ es:",
                  "opciones_md": [
                      "$\\operatorname{Dom}(f) \\cup \\operatorname{Dom}(g)$",
                      "$\\operatorname{Dom}(f) \\cap \\operatorname{Dom}(g)$",
                      "**$\\operatorname{Dom}(f) \\cap \\operatorname{Dom}(g)$ excluyendo donde $g(x) = 0$**",
                      "$\\operatorname{Dom}(f)$",
                  ],
                  "correcta": "C",
                  "pista_md": "El cociente requiere también que $g$ no se anule.",
                  "explicacion_md": "Restricción adicional sobre la intersección.",
              },
          ]),

        ej(
            "Operaciones",
            "Sean $f(x) = x^2 - 1$ y $g(x) = x + 3$. Calcula $(f - g)(x)$ y $(f \\cdot g)(2)$.",
            ["Operar punto a punto."],
            (
                "$(f - g)(x) = x^2 - 1 - (x + 3) = x^2 - x - 4$. $(f \\cdot g)(2) = f(2) \\cdot g(2) = 3 \\cdot 5 = 15$."
            ),
        ),

        ej(
            "Composición sencilla",
            "Sean $f(x) = x^2$ y $g(x) = \\sqrt{x - 3}$. Calcula $(f \\circ g)(x)$ y $(g \\circ f)(x)$ con sus dominios.",
            ["Una a la vez."],
            (
                "$(f \\circ g)(x) = (\\sqrt{x - 3})^2 = x - 3$, dominio $[3, +\\infty)$ (heredado de $g$).\n\n"
                "$(g \\circ f)(x) = \\sqrt{x^2 - 3}$, dominio donde $x^2 \\geq 3$: $(-\\infty, -\\sqrt{3}] \\cup [\\sqrt{3}, +\\infty)$."
            ),
        ),

        ej(
            "Descomponer",
            "Expresa $H(x) = \\sqrt{1 + \\sqrt{x}}$ como composición de funciones simples.",
            ["Identificar la 'capa' interna y externa."],
            (
                "Defino $g(x) = \\sqrt{x}$, $h(x) = 1 + x$, $f(x) = \\sqrt{x}$. Entonces $H = f \\circ h \\circ g$, es decir, $H(x) = f(h(g(x))) = \\sqrt{1 + \\sqrt{x}}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $(f \\cdot g)(x)$ con $(f \\circ g)(x)$.** El primero es el producto, el segundo es la composición.",
              "**Suponer que la composición es conmutativa.** $f \\circ g \\neq g \\circ f$ casi siempre.",
              "**Olvidar verificar el dominio en composiciones.** Hay dos restricciones, no una.",
              "**Equivocar el orden** en $f \\circ g$. Primero actúa $g$, no $f$.",
              "**Olvidar excluir los ceros de $g$ en $f/g$.** Aunque $f(x_0) = 0$, si $g(x_0) = 0$ no se permite.",
          ]),

        b("resumen",
          puntos_md=[
              "**Operaciones:** $f \\pm g, f \\cdot g, f/g$ punto a punto.",
              "**Dominios:** intersección de dominios; excluir ceros del denominador para cociente.",
              "**Composición:** $(f \\circ g)(x) = f(g(x))$. Primero $g$, después $f$.",
              "**Dominio de composición:** $x \\in \\operatorname{Dom}(g)$ **y** $g(x) \\in \\operatorname{Dom}(f)$.",
              "**No conmutativa:** $f \\circ g \\neq g \\circ f$ en general.",
              "**Próxima lección:** la operación 'inversa' que deshace una función — funciones inversas.",
          ]),
    ]
    return {
        "id": "lec-prec-2-5-algebra-de-funciones",
        "title": "Álgebra de funciones",
        "description": "Suma, resta, producto y cociente de funciones con sus dominios. Composición de funciones (f ∘ g)(x) = f(g(x)), no conmutatividad y dominios compuestos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# Funciones inversas
# =====================================================================
def lesson_funciones_inversas():
    blocks = [
        b("texto", body_md=(
            "Una función **invertible** es una que se puede 'deshacer'. Si $f$ asigna a $x$ el valor "
            "$y = f(x)$, su **inversa** $f^{-1}$ asigna a $y$ el valor $x$ original — recupera la entrada "
            "a partir de la salida.\n\n"
            "$$x \\;\\xrightarrow{\\;\\;f\\;\\;}\\; y \\;\\xrightarrow{\\;\\;f^{-1}\\;\\;}\\; x.$$\n\n"
            "**No todas las funciones son invertibles.** Para serlo, la función debe ser **inyectiva** "
            "(uno a uno): a entradas distintas le corresponden salidas distintas. Si dos $x$ distintos dan "
            "el mismo $y$, no hay forma de 'volver' unívocamente.\n\n"
            "**Aplicaciones típicas en cálculo y aplicaciones:**\n\n"
            "- $\\ln$ es la inversa de $e^x$ (próximo capítulo).\n"
            "- $\\arcsin$ es la inversa de $\\sin$ restringido a $[-\\pi/2, \\pi/2]$.\n"
            "- Despejar $x$ de $y = 3 x + 5$ produce la inversa $x = (y - 5)/3$.\n\n"
            "**Al terminar:**\n\n"
            "- Distinguís función **inyectiva**, **sobreyectiva** y **biyectiva**.\n"
            "- Aplicás el **criterio de la recta horizontal** para ver inyectividad.\n"
            "- Calculás $f^{-1}$ algebraicamente despejando.\n"
            "- Verificás que $f \\circ f^{-1} = f^{-1} \\circ f = \\text{identidad}$."
        )),

        b("definicion",
          titulo="Inyectividad y biyectividad",
          body_md=(
              "**Inyectiva (uno a uno).** $f$ es inyectiva si\n\n"
              "$$f(x_1) = f(x_2) \\;\\Longrightarrow\\; x_1 = x_2.$$\n\n"
              "Equivalentemente: si $x_1 \\neq x_2$, entonces $f(x_1) \\neq f(x_2)$.\n\n"
              "**Sobreyectiva.** $f : A \\to B$ es sobreyectiva si para todo $y \\in B$ existe $x \\in A$ con $f(x) = y$. "
              "Equivalentemente: $\\operatorname{Ran}(f) = B$.\n\n"
              "**Biyectiva.** Inyectiva **y** sobreyectiva. Solo las funciones biyectivas tienen inversa.\n\n"
              "**Criterio de la recta horizontal.** $f$ es **inyectiva** si y solo si toda recta horizontal "
              "corta la gráfica en **a lo sumo un punto**. Si alguna recta horizontal corta en $\\geq 2$ "
              "puntos, los puntos $x$ correspondientes tienen la misma imagen → no inyectiva.\n\n"
              "**Truco práctico.** En general, si la gráfica es estrictamente **monótona** (siempre crece o "
              "siempre decrece), es inyectiva. Las parábolas no lo son (suben y bajan)."
          )),

        b("definicion",
          titulo="Función inversa",
          body_md=(
              "Si $f: A \\to B$ es biyectiva, su **función inversa** $f^{-1}: B \\to A$ es la única función "
              "que cumple:\n\n"
              "$$f^{-1}(f(x)) = x \\quad \\text{para todo } x \\in A,$$\n"
              "$$f(f^{-1}(y)) = y \\quad \\text{para todo } y \\in B.$$\n\n"
              "Es decir, $f^{-1}$ y $f$ se 'cancelan' al componerse en cualquier orden.\n\n"
              "**Conexión dominio/rango:**\n\n"
              "$$\\operatorname{Dom}(f^{-1}) = \\operatorname{Ran}(f), \\qquad \\operatorname{Ran}(f^{-1}) = \\operatorname{Dom}(f).$$\n\n"
              "**Propiedad gráfica.** La gráfica de $f^{-1}$ es la **reflexión** de la gráfica de $f$ "
              "respecto a la recta $y = x$. Cada punto $(a, b)$ de $f$ corresponde a $(b, a)$ de $f^{-1}$.\n\n"
              "**Notación.** $f^{-1}$ **no es** $1/f$. Son cosas distintas. $f^{-1}(x) \\neq \\dfrac{1}{f(x)}$."
          )),

        formulas(
            titulo="Cómo hallar la inversa (algoritmo)",
            body=(
                "Para encontrar $f^{-1}$ de una función dada por $y = f(x)$:\n\n"
                "1. **Verificar inyectividad** (criterio de recta horizontal o argumento algebraico).\n"
                "2. **Escribir** $y = f(x)$.\n"
                "3. **Despejar $x$** en términos de $y$.\n"
                "4. **Intercambiar** las variables: $x \\leftrightarrow y$. Lo que tienes ahora es $y = f^{-1}(x)$.\n"
                "5. **(Opcional) Verificar** componiendo: $f(f^{-1}(x))$ debería dar $x$.\n\n"
                "**El paso 4 es solo notación.** Por convención escribimos las funciones con $x$ como variable independiente."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Inversa de una lineal",
          problema_md="Halla $f^{-1}$ para $f(x) = 3 - 5 x$.",
          pasos=[
              {"accion_md": (
                  "**Inyectividad.** $f$ es lineal con pendiente $\\neq 0$, así estrictamente decreciente. **Inyectiva.**"
              ),
               "justificacion_md": "Toda función lineal con $m \\neq 0$ es inyectiva.",
               "es_resultado": False},
              {"accion_md": (
                  "**Despejar $x$.** $y = 3 - 5 x \\Rightarrow 5 x = 3 - y \\Rightarrow x = \\dfrac{3 - y}{5}$.\n\n"
                  "**Intercambiar:** $f^{-1}(x) = \\dfrac{3 - x}{5}$."
              ),
               "justificacion_md": "Aritmética simple.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificar.** $f(f^{-1}(x)) = 3 - 5 \\cdot \\dfrac{3 - x}{5} = 3 - (3 - x) = x$. ✓"
              ),
               "justificacion_md": "La composición da la identidad.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inversa de una racional",
          problema_md="Halla $f^{-1}$ para $f(x) = \\dfrac{3 x}{x + 2}$.",
          pasos=[
              {"accion_md": (
                  "**Despejar $x$.** $y = \\dfrac{3 x}{x + 2} \\Rightarrow y(x + 2) = 3 x \\Rightarrow y x + 2 y = 3 x$."
              ),
               "justificacion_md": "Multiplicar para eliminar el denominador.",
               "es_resultado": False},
              {"accion_md": (
                  "**Agrupar términos con $x$:** $y x - 3 x = -2 y \\Rightarrow x (y - 3) = -2 y \\Rightarrow x = \\dfrac{-2 y}{y - 3} = \\dfrac{2 y}{3 - y}$."
              ),
               "justificacion_md": "Factor común y despeje.",
               "es_resultado": False},
              {"accion_md": (
                  "**Intercambiar:** $f^{-1}(x) = \\dfrac{2 x}{3 - x}$. **Dominio:** $x \\neq 3$."
              ),
               "justificacion_md": "Simétrica al original (que tenía $x \\neq -2$ por denominador). Coherente con $\\operatorname{Dom}(f^{-1}) = \\operatorname{Ran}(f)$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inversa con raíz",
          problema_md="Halla $f^{-1}$ para $f(x) = \\sqrt{2 x - 1}$.",
          pasos=[
              {"accion_md": (
                  "**Dominio y rango de $f$.** $\\operatorname{Dom}(f) = [1/2, +\\infty)$ (radicando $\\geq 0$), $\\operatorname{Ran}(f) = [0, +\\infty)$ (raíz cuadrada principal).\n\n"
                  "**Inyectiva** porque la raíz es estrictamente creciente."
              ),
               "justificacion_md": "Identificar dominio/rango antes de invertir.",
               "es_resultado": False},
              {"accion_md": (
                  "**Despejar $x$.** $y = \\sqrt{2 x - 1} \\Rightarrow y^2 = 2 x - 1 \\Rightarrow x = \\dfrac{y^2 + 1}{2}$."
              ),
               "justificacion_md": "Elevar al cuadrado (válido porque $y \\geq 0$).",
               "es_resultado": False},
              {"accion_md": (
                  "**Intercambiar:** $f^{-1}(x) = \\dfrac{x^2 + 1}{2}$, con dominio $[0, +\\infty)$ (porque era el rango de $f$)."
              ),
               "justificacion_md": "Notar que sin restringir el dominio, $\\dfrac{x^2 + 1}{2}$ no es inyectiva. Pero al restringir a $[0, +\\infty)$ sí lo es y coincide con la inversa.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Reflexión sobre $y = x$.** Si $f$ pasa por $(a, b)$, entonces $f^{-1}$ pasa por $(b, a)$. "
            "Y $(a, b)$ y $(b, a)$ son simétricos respecto a la diagonal $y = x$. Por eso la gráfica de "
            "$f^{-1}$ es la reflexión de $f$ sobre esa diagonal.\n\n"
            "**Restringir dominio para invertir.** $f(x) = x^2$ no es inyectiva (pasa por $(2, 4)$ y $(-2, 4)$). "
            "Pero **restringida** a $[0, +\\infty)$ sí lo es, y su inversa es $f^{-1}(x) = \\sqrt{x}$. La función "
            "$\\arcsin$ es otro ejemplo: $\\sin$ no es inyectiva, pero al restringir a $[-\\pi/2, \\pi/2]$ sí, "
            "y su inversa es $\\arcsin$.\n\n"
            "**$f^{-1}$ no es $1/f$.** $f^{-1}$ es la **inversa funcional**; $1/f$ es la **recíproca aritmética**. "
            "La notación es desafortunada, pero estándar."
        )),

        fig(
            "Gráfica de y = 2x - 1 (recta) en color teal #06b6d4 y su inversa y = (x+1)/2 en color ámbar #f59e0b. "
            "Línea diagonal y = x en gris punteado de fondo. "
            "Algunos pares de puntos correspondientes marcados: (1, 1), (2, 3) en la primera y su simétrico (3, 2) en la segunda. "
            "Eje x e y mismo rango (-2, 5). "
            "Etiqueta: 'f y f^{-1} son simétricas respecto a y = x'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$f^{-1}(x)$ se interpreta como:",
                  "opciones_md": [
                      "$1/f(x)$",
                      "**La función que 'deshace' $f$**",
                      "Derivada de $f$",
                      "Cuadrado de $f$",
                  ],
                  "correcta": "B",
                  "pista_md": "El '$-1$' es notacional, no exponente.",
                  "explicacion_md": "$f^{-1}(f(x)) = x$. Recupera la entrada original.",
              },
              {
                  "enunciado_md": "Una función con la gráfica de una parábola completa (no restringida):",
                  "opciones_md": [
                      "Es siempre invertible",
                      "**No es invertible (no es inyectiva)**",
                      "Es invertible solo si abre hacia arriba",
                      "Tiene infinitas inversas",
                  ],
                  "correcta": "B",
                  "pista_md": "Recta horizontal corta en dos puntos.",
                  "explicacion_md": "Falla el criterio. Hay que restringir el dominio para invertir.",
              },
              {
                  "enunciado_md": "Si $f$ es invertible, $\\operatorname{Dom}(f^{-1})$ es:",
                  "opciones_md": [
                      "$\\operatorname{Dom}(f)$",
                      "**$\\operatorname{Ran}(f)$**",
                      "$\\mathbb{R}$",
                      "El conjunto vacío",
                  ],
                  "correcta": "B",
                  "pista_md": "$f^{-1}$ recibe lo que $f$ produce.",
                  "explicacion_md": "Las salidas de $f$ son las entradas de $f^{-1}$.",
              },
          ]),

        ej(
            "Inversa básica",
            "Halla la inversa de $f(x) = 2 x - 7$.",
            ["Despejar y permutar."],
            (
                "$y = 2 x - 7 \\Rightarrow x = (y + 7)/2$. **$f^{-1}(x) = (x + 7)/2$.**"
            ),
        ),

        ej(
            "Inversa con cuadrática restringida",
            "Si $f(x) = x^2$ con dominio restringido a $[0, +\\infty)$, halla $f^{-1}$.",
            ["En $[0, +\\infty)$ la cuadrática es inyectiva."],
            (
                "$y = x^2$ con $x \\geq 0 \\Rightarrow x = \\sqrt{y}$. **$f^{-1}(x) = \\sqrt{x}$.** Dominio $[0, +\\infty)$."
            ),
        ),

        ej(
            "Verificación",
            "Demuestra que $f(x) = (x - 3)^3$ y $g(x) = \\sqrt[3]{x} + 3$ son inversas mutuas.",
            ["Calcular $f(g(x))$ y $g(f(x))$."],
            (
                "$f(g(x)) = (\\sqrt[3]{x} + 3 - 3)^3 = (\\sqrt[3]{x})^3 = x$. ✓\n\n"
                "$g(f(x)) = \\sqrt[3]{(x - 3)^3} + 3 = (x - 3) + 3 = x$. ✓\n\n"
                "Las dos composiciones dan identidad → inversas mutuas."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $f^{-1}$ con $1/f$.** Son notaciones similares pero conceptos distintos.",
              "**Olvidar verificar inyectividad antes de invertir.** Sin inyectividad, no hay inversa.",
              "**No actualizar dominio/rango** al hallar inversa: $\\operatorname{Dom}(f^{-1}) = \\operatorname{Ran}(f)$.",
              "**Equivocar el orden** al despejar: empezar de $y = f(x)$, despejar $x$, después intercambiar.",
              "**Aplicar inversa a funciones no biyectivas sin restringir el dominio.** $f(x) = x^2$ no es invertible en todo $\\mathbb{R}$, pero sí en $[0, +\\infty)$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Inyectiva:** $f(x_1) = f(x_2) \\Rightarrow x_1 = x_2$. Criterio de recta horizontal.",
              "**Biyectiva:** inyectiva + sobreyectiva. Solo las biyectivas tienen inversa.",
              "**Inversa $f^{-1}$:** $f^{-1}(f(x)) = x$ y $f(f^{-1}(y)) = y$. $\\operatorname{Dom}(f^{-1}) = \\operatorname{Ran}(f)$.",
              "**Cómo hallarla:** despejar $x$ de $y = f(x)$, intercambiar $x \\leftrightarrow y$.",
              "**Gráfica:** simétrica a $f$ respecto a la recta $y = x$.",
              "**Cierre del capítulo:** definición, gráficas, rapidez de cambio, transformaciones, álgebra y composición, inversas — todo el toolkit estándar de funciones.",
              "**Próximo capítulo:** funciones polinomiales y racionales — gráficas y propiedades específicas.",
          ]),
    ]
    return {
        "id": "lec-prec-2-6-funciones-inversas",
        "title": "Funciones inversas",
        "description": "Inyectividad, sobreyectividad, biyectividad, criterio de la recta horizontal. Definición y cálculo de la función inversa. Relación gráfica f vs f^{-1} (reflexión sobre y=x).",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 6,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "precalculo"

    existing_course = await db.courses.find_one({"id": course_id})
    if not existing_course:
        print(f"⚠ Curso '{course_id}' no existe. Ejecutá primero seed_precalculo_chapter_1.py.")
        return
    print(f"✓ Curso encontrado: {existing_course.get('title', course_id)}")

    chapter_id = "ch-prec-funciones"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Funciones",
        "description": (
            "Concepto de función, dominio y rango, gráficas, rapidez de cambio, transformaciones rígidas "
            "y de escala, álgebra y composición de funciones, funciones inversas."
        ),
        "order": 2,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_definicion_dominio_rango,
        lesson_graficas,
        lesson_rapidez_de_cambio,
        lesson_transformaciones,
        lesson_algebra_funciones,
        lesson_funciones_inversas,
    ]
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
    print(
        f"✅ Capítulo 2 — Funciones listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())


