"""
Seed del curso Ecuaciones Diferenciales — Capítulo 2: EDO de Orden Superior.

Crea el capítulo 'EDO de Orden Superior' bajo el curso 'ecuaciones-diferenciales'
y siembra sus 9 lecciones:

  - Modelos, existencia y unicidad
  - EDO homogénea: solución general
  - Coeficientes constantes
  - EDO de orden n
  - Coeficientes constantes de orden superior
  - Vibraciones mecánicas
  - Coeficientes indeterminados
  - Variación de parámetros
  - Fórmula de Abel

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
# Modelos, existencia y unicidad
# =====================================================================
def lesson_modelos():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora estudiamos **EDOs de primer orden**: una sola derivada relacionada con la función. "
            "Pero la mayoría de los fenómenos físicos involucra **aceleración** — es decir, **derivadas de segundo "
            "orden**. La segunda ley de Newton $F = ma$ es, esencialmente, una EDO de segundo orden.\n\n"
            "**Aplicaciones típicas que requieren orden 2 o superior:**\n\n"
            "- **Vibraciones mecánicas:** sistema masa-resorte-amortiguador, $mx'' + cx' + kx = F(t)$.\n"
            "- **Circuitos RLC:** carga del condensador, $L Q'' + R Q' + Q/C = E(t)$.\n"
            "- **Péndulo simple:** $\\theta'' + (g/L)\\sin\\theta = 0$.\n"
            "- **Vigas y deformación:** ecuación de Euler-Bernoulli, $EI\\, y^{(4)} = w(x)$.\n"
            "- **Mecánica cuántica:** ecuación de Schrödinger estacionaria.\n\n"
            "En esta lección sentamos las **bases teóricas**: definimos qué es una EDO lineal de orden 2, "
            "qué significa un **problema de valor inicial (PVI)** y enunciamos el **teorema de existencia y "
            "unicidad**. En las lecciones siguientes desarrollamos los **métodos de resolución**.\n\n"
            "**Al terminar:**\n\n"
            "- Reconoces la **forma estándar** de una EDO lineal de orden 2.\n"
            "- Distingues entre **homogénea** y **no homogénea**.\n"
            "- Sabes que un PVI de orden 2 requiere **dos condiciones iniciales**.\n"
            "- Aplicas el teorema de **existencia y unicidad** para garantizar solución única."
        )),

        b("definicion",
          titulo="EDO lineal de orden 2",
          body_md=(
              "Una **ecuación diferencial lineal de orden 2** tiene la forma\n\n"
              "$$a_2(x)\\, y'' + a_1(x)\\, y' + a_0(x)\\, y = g(x),$$\n\n"
              "donde $a_2, a_1, a_0, g$ son funciones de la variable independiente $x$ (o $t$ en problemas "
              "temporales) y $a_2(x) \\neq 0$ en el intervalo de interés.\n\n"
              "Dividiendo por $a_2(x)$ obtenemos la **forma estándar** o **normalizada**:\n\n"
              "$$y'' + p(x)\\, y' + q(x)\\, y = f(x).$$\n\n"
              "**Clasificación según $f$:**\n\n"
              "- Si $f(x) \\equiv 0$, la EDO se llama **homogénea**.\n"
              "- Si $f(x) \\not\\equiv 0$, la EDO se llama **no homogénea** o **completa**.\n\n"
              "**¿Por qué 'lineal'?** Porque $y, y', y''$ aparecen a la primera potencia y no multiplicados entre sí. "
              "Una ecuación como $y'' + y\\, y' = 0$ o $y'' + \\sin y = 0$ **no** es lineal."
          )),

        b("definicion",
          titulo="Problema de valor inicial (PVI)",
          body_md=(
              "Un **problema de valor inicial** para una EDO de orden 2 consiste en resolver\n\n"
              "$$y'' + p(x)\\, y' + q(x)\\, y = f(x), \\qquad y(x_0) = y_0, \\quad y'(x_0) = y_1.$$\n\n"
              "Es decir, además de la EDO, se especifican **dos condiciones iniciales en el mismo punto** $x_0$: "
              "el **valor** de la función y el **valor de su derivada**.\n\n"
              "**¿Por qué dos?** Porque la solución general de una EDO lineal de orden 2 contiene **dos constantes "
              "arbitrarias** — y necesitamos dos ecuaciones para determinarlas.\n\n"
              "**Interpretación física (oscilador):** $y(t_0)$ es la posición inicial y $y'(t_0)$ es la velocidad "
              "inicial. Conocer ambas es necesario y suficiente para predecir toda la trayectoria futura."
          )),

        formulas(
            titulo="Modelos clásicos de orden 2",
            body=(
                "Los siguientes modelos físicos aparecerán a lo largo del capítulo:\n\n"
                "**Sistema masa-resorte-amortiguador (forzado):**\n\n"
                "$$m\\, x''(t) + c\\, x'(t) + k\\, x(t) = F(t),$$\n\n"
                "donde $m$ es la masa, $c$ el coeficiente de amortiguamiento, $k$ la constante del resorte y "
                "$F(t)$ una fuerza externa.\n\n"
                "**Circuito RLC en serie** (con fuente $E(t)$ y carga $Q(t)$ en el condensador):\n\n"
                "$$L\\, Q''(t) + R\\, Q'(t) + \\dfrac{1}{C}\\, Q(t) = E(t).$$\n\n"
                "**Péndulo simple** (no lineal, longitud $L$, gravedad $g$):\n\n"
                "$$\\theta''(t) + \\dfrac{g}{L}\\sin\\theta(t) = 0.$$\n\n"
                "Para ángulos pequeños $\\sin\\theta \\approx \\theta$ y obtenemos el **MAS lineal**: "
                "$\\theta'' + (g/L)\\theta = 0$.\n\n"
                "**Observación clave:** el sistema masa-resorte y el RLC son la **misma EDO** con distinto "
                "significado físico de las variables. Lo que aprendamos para uno se traduce inmediatamente al otro."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Clasificar EDOs de orden 2",
          problema_md=(
              "Para cada una, decide si es lineal o no lineal, homogénea o no homogénea:\n\n"
              "**(a)** $y'' + 4y' + 5y = 0$\n\n"
              "**(b)** $y'' + 4y' + 5y = \\cos(2x)$\n\n"
              "**(c)** $y'' + (\\sin x)\\, y = e^x$\n\n"
              "**(d)** $y'' + y\\, y' = 0$"
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $y'' + 4y' + 5y = 0$. Coeficientes constantes, $f = 0$. **Lineal, homogénea**."
              ),
               "justificacion_md": "Es el caso prototípico que veremos en la lección de coeficientes constantes.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $y'' + 4y' + 5y = \\cos(2x)$. Misma parte izquierda; ahora $f(x) = \\cos(2x) \\neq 0$. **Lineal, no homogénea**."
              ),
               "justificacion_md": "El término $\\cos(2x)$ rompe la homogeneidad pero conserva la linealidad.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** $y'' + (\\sin x)\\, y = e^x$. Coeficiente variable $\\sin x$. Pero $y$ y $y''$ aparecen "
                  "a la primera potencia, sin multiplicarse. **Lineal, no homogénea**."
              ),
               "justificacion_md": "**Cuidado:** la linealidad se evalúa respecto a $y$ y sus derivadas, **no** respecto a $x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(d)** $y'' + y\\, y' = 0$. Aparece el producto $y \\cdot y'$. **No lineal**."
              ),
               "justificacion_md": "Una vez que se rompe la linealidad, los métodos del capítulo no aplican directamente.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Teorema de existencia y unicidad",
          body_md=(
              "**Teorema.** Sea el PVI\n\n"
              "$$y'' + p(x)\\, y' + q(x)\\, y = f(x), \\qquad y(x_0) = y_0, \\quad y'(x_0) = y_1.$$\n\n"
              "Si $p, q, f$ son **continuas** en un intervalo abierto $I$ que contiene a $x_0$, entonces el PVI "
              "tiene **una única solución** $y(x)$ definida en **todo** $I$.\n\n"
              "**Tres consecuencias importantes:**\n\n"
              "1. **Existencia garantizada:** basta con verificar continuidad de los coeficientes.\n"
              "2. **Unicidad global:** la solución se extiende a todo el intervalo de continuidad — no se queda "
              "'atascada' como puede pasar en EDOs no lineales.\n"
              "3. **Determinismo físico:** el sistema queda completamente determinado por su estado inicial "
              "$(y(x_0), y'(x_0))$ — la trayectoria pasada y futura está fijada.\n\n"
              "**Versión sin normalizar:** si la EDO viene como $a_2(x) y'' + a_1 y' + a_0 y = g$, también hay "
              "que pedir $a_2(x) \\neq 0$ en $I$ (de lo contrario, los coeficientes normalizados $p = a_1/a_2$, "
              "$q = a_0/a_2$ pueden no estar definidos)."
          )),

        b("intuicion", body_md=(
            "**¿Por qué exactamente dos condiciones iniciales?**\n\n"
            "En física newtoniana, conocer la **posición** $x(t_0)$ y la **velocidad** $x'(t_0)$ de una "
            "partícula es **necesario y suficiente** para predecir su trayectoria — siempre que conozcamos las "
            "fuerzas. La aceleración $x''$ está determinada por las fuerzas, no es 'libre'.\n\n"
            "Matemáticamente: la EDO $x'' = F(t, x, x')/m$ permite calcular $x''$ en cualquier instante a partir "
            "de $(t, x, x')$. Integrando una vez recuperamos $x'$ (necesita 1 constante), integrando otra vez "
            "recuperamos $x$ (otra constante). **Dos integraciones, dos constantes.**\n\n"
            "**Generalización:** una EDO de orden $n$ requiere $n$ condiciones iniciales — los valores de "
            "$y, y', y'', \\ldots, y^{(n-1)}$ en un punto."
        )),

        b("ejemplo_resuelto",
          titulo="Aplicar existencia y unicidad",
          problema_md=(
              "Determina el intervalo más grande donde el PVI tiene solución única garantizada:\n\n"
              "$$(x^2 - 4)\\, y'' + x\\, y' + (\\ln x)\\, y = 0, \\qquad y(1) = 0, \\quad y'(1) = 1.$$"
          ),
          pasos=[
              {"accion_md": (
                  "**Normalizar.** Dividir por $a_2(x) = x^2 - 4$:\n\n"
                  "$$y'' + \\dfrac{x}{x^2 - 4}\\, y' + \\dfrac{\\ln x}{x^2 - 4}\\, y = 0.$$\n\n"
                  "Identificamos $p(x) = \\dfrac{x}{x^2 - 4}$, $q(x) = \\dfrac{\\ln x}{x^2 - 4}$, $f(x) = 0$."
              ),
               "justificacion_md": "El teorema requiere la forma normalizada con coeficientes continuos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Localizar discontinuidades:**\n\n"
                  "- $p$ y $q$ se indefinen en $x = \\pm 2$ (denominador $x^2 - 4$).\n"
                  "- $\\ln x$ requiere $x > 0$.\n\n"
                  "**Posibles intervalos:** $(0, 2)$ y $(2, \\infty)$."
              ),
               "justificacion_md": "Hay que excluir todos los puntos donde algún coeficiente falla en ser continuo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Elegir el intervalo que contiene $x_0 = 1$:** es $(0, 2)$.\n\n"
                  "**Conclusión:** existe una única solución del PVI definida en todo $(0, 2)$."
              ),
               "justificacion_md": "El teorema garantiza solución hasta el borde del intervalo de continuidad.",
               "es_resultado": True},
          ]),

        fig(
            "Diagrama del modelo masa-resorte-amortiguador en posición horizontal. "
            "Una masa cuadrada (etiquetada 'm') unida a un resorte helicoidal a la izquierda fijo a una pared "
            "y a un cilindro amortiguador (dashpot) etiquetado 'c'. Eje x horizontal con flecha indicando "
            "desplazamiento x(t) desde la posición de equilibrio (línea vertical punteada). "
            "Una flecha externa F(t) apunta horizontalmente sobre la masa. "
            "Etiquetas claras: 'k' sobre el resorte, 'c' sobre el amortiguador, 'F(t)' sobre la flecha externa. "
            "Acento teal #06b6d4 en el resorte, ámbar #f59e0b en la masa. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuántas condiciones iniciales requiere un PVI de orden 2?",
                  "opciones_md": ["Una", "**Dos**", "Tres", "Depende de la EDO"],
                  "correcta": "B",
                  "pista_md": "Tantas como el orden de la EDO.",
                  "explicacion_md": "**Dos.** El valor $y(x_0)$ y la derivada $y'(x_0)$ en el mismo punto.",
              },
              {
                  "enunciado_md": "$y'' + (\\cos x)\\, y' + 3y = e^x$ es:",
                  "opciones_md": [
                      "Lineal homogénea",
                      "**Lineal no homogénea**",
                      "No lineal homogénea",
                      "No lineal no homogénea",
                  ],
                  "correcta": "B",
                  "pista_md": "Mira si $y, y', y''$ aparecen a la primera potencia y si $f \\neq 0$.",
                  "explicacion_md": "**Lineal no homogénea.** $\\cos x$ es coeficiente (no función de $y$), y $e^x \\neq 0$.",
              },
              {
                  "enunciado_md": "Para garantizar existencia y unicidad en $y'' + p y' + q y = f$ se necesita que:",
                  "opciones_md": [
                      "$p, q, f$ sean polinomios",
                      "$p, q$ sean acotadas",
                      "**$p, q, f$ sean continuas en un intervalo que contenga $x_0$**",
                      "$f \\equiv 0$",
                  ],
                  "correcta": "C",
                  "pista_md": "Versión lineal del teorema de E&U.",
                  "explicacion_md": "**Continuidad de los tres coeficientes** en un intervalo abierto que contenga la condición inicial.",
              },
          ]),

        ej(
            "Clasificar y normalizar",
            "Lleva a forma estándar e indica si es lineal: $(t+1) y'' - t y' + 2 y = \\sin t$.",
            ["Dividir por $(t+1)$ cuando $t \\neq -1$."],
            (
                "$y'' - \\dfrac{t}{t+1}\\, y' + \\dfrac{2}{t+1}\\, y = \\dfrac{\\sin t}{t+1}$. "
                "**Lineal no homogénea.** Coeficientes continuos en $(-\\infty, -1)$ y en $(-1, \\infty)$."
            ),
        ),

        ej(
            "Intervalo de existencia",
            "¿En qué intervalo está garantizada la solución única del PVI "
            "$x y'' + (\\sin x) y' + y = 0$, $y(\\pi) = 1$, $y'(\\pi) = 0$?",
            ["Normalizar y mirar dónde fallan los coeficientes."],
            (
                "Normalizando: $y'' + \\dfrac{\\sin x}{x} y' + \\dfrac{1}{x} y = 0$. "
                "Falla solo en $x = 0$. Como $x_0 = \\pi > 0$, el intervalo es $(0, \\infty)$."
            ),
        ),

        ej(
            "Modelo físico",
            "Plantea la EDO de un sistema masa-resorte sin amortiguamiento ni fuerza externa, con $m = 2$ kg "
            "y $k = 8$ N/m. Indica la forma del PVI si se suelta desde $x_0 = 0{,}5$ m con velocidad inicial $0$.",
            ["$mx'' + kx = 0$."],
            (
                "EDO: $2 x'' + 8 x = 0$, equivalentemente $x'' + 4 x = 0$. "
                "PVI: $x(0) = 0{,}5$, $x'(0) = 0$. "
                "La solución (que veremos próximamente) es $x(t) = 0{,}5 \\cos(2t)$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar normalizar antes de aplicar E&U.** El coeficiente líder $a_2(x)$ debe ser no nulo.",
              "**Dar una sola condición inicial para orden 2.** Hace falta valor y derivada.",
              "**Confundir 'condiciones iniciales' con 'condiciones de frontera'.** Las primeras se especifican en el mismo punto $x_0$; las segundas en dos puntos distintos $a, b$ (es otro problema, llamado problema de contorno).",
              "**Pensar que coeficientes variables vuelven la EDO no lineal.** No: la linealidad se mide respecto a $y$ y sus derivadas, no a $x$.",
          ]),

        b("resumen",
          puntos_md=[
              "**EDO lineal de orden 2:** $y'' + p(x) y' + q(x) y = f(x)$.",
              "**Homogénea** si $f \\equiv 0$, **no homogénea** en otro caso.",
              "**PVI:** EDO + dos condiciones iniciales $y(x_0) = y_0$, $y'(x_0) = y_1$ en el **mismo** punto.",
              "**Teorema de E&U:** continuidad de $p, q, f$ en $I \\ni x_0$ $\\Rightarrow$ solución única en todo $I$.",
              "**Modelos clave:** masa-resorte-amortiguador, RLC, péndulo lineal, viga.",
              "**Próxima lección:** estructura de la solución general de una EDO homogénea (superposición y wronskiano).",
          ]),
    ]
    return {
        "id": "lec-ed-2-1-modelos-existencia-unicidad",
        "title": "Modelos, existencia y unicidad",
        "description": "EDO lineal de orden 2: forma estándar, clasificación, problema de valor inicial y teorema de existencia y unicidad. Modelos clásicos: masa-resorte, RLC, péndulo.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# EDO homogénea: solución general
# =====================================================================
def lesson_homogenea_general():
    blocks = [
        b("texto", body_md=(
            "Antes de aprender a **encontrar** soluciones de una EDO de orden 2, conviene entender la "
            "**estructura** del conjunto de todas las soluciones de la ecuación homogénea\n\n"
            "$$y'' + p(x)\\, y' + q(x)\\, y = 0.$$\n\n"
            "La buena noticia es que el conjunto de soluciones tiene una estructura **lineal** muy simple: "
            "es un **espacio vectorial de dimensión 2**. Eso significa que basta con encontrar **dos soluciones "
            "linealmente independientes** $y_1, y_2$, y todas las demás se obtienen como **combinación lineal**.\n\n"
            "**Al terminar:**\n\n"
            "- Aplicas el **principio de superposición** para construir nuevas soluciones.\n"
            "- Decides si dos soluciones son linealmente independientes usando el **wronskiano**.\n"
            "- Reconoces un **conjunto fundamental de soluciones** y escribes la **solución general**."
        )),

        b("definicion",
          titulo="Principio de superposición",
          body_md=(
              "**Teorema (superposición).** Sean $y_1(x)$ e $y_2(x)$ soluciones de la EDO homogénea\n\n"
              "$$y'' + p(x) y' + q(x) y = 0$$\n\n"
              "en un intervalo $I$. Entonces, para cualesquiera constantes $c_1, c_2 \\in \\mathbb{R}$, la "
              "**combinación lineal**\n\n"
              "$$y(x) = c_1 y_1(x) + c_2 y_2(x)$$\n\n"
              "también es solución de la EDO en $I$.\n\n"
              "**Demostración (en una línea):** sustituir y usar la linealidad de la derivada — "
              "$(c_1 y_1 + c_2 y_2)'' + p(c_1 y_1 + c_2 y_2)' + q(c_1 y_1 + c_2 y_2) = c_1(y_1'' + p y_1' + q y_1) + c_2(y_2'' + p y_2' + q y_2) = 0 + 0 = 0$.\n\n"
              "**Importante:** este principio falla para EDOs no lineales. Por ejemplo, $y_1 = 1$ e $y_2 = x$ son soluciones de $y'' = 0$, pero la suma de soluciones de $y'' = y^2$ no es solución."
          )),

        b("definicion",
          titulo="Dependencia e independencia lineal",
          body_md=(
              "Dos funciones $f, g$ definidas en un intervalo $I$ son **linealmente dependientes** en $I$ si "
              "existen constantes $c_1, c_2$ **no ambas nulas** tales que\n\n"
              "$$c_1 f(x) + c_2 g(x) = 0 \\quad \\text{para todo } x \\in I.$$\n\n"
              "Equivalentemente: una es **múltiplo escalar** de la otra ($g = \\lambda f$).\n\n"
              "Si no son linealmente dependientes, son **linealmente independientes**: la única forma de que "
              "$c_1 f + c_2 g \\equiv 0$ es $c_1 = c_2 = 0$.\n\n"
              "**Ejemplos rápidos:**\n\n"
              "- $f = e^x$, $g = 3 e^x$: dependientes ($g = 3 f$).\n"
              "- $f = \\cos x$, $g = \\sin x$: independientes (no hay $\\lambda$ tal que $\\sin x = \\lambda \\cos x$ para todo $x$).\n"
              "- $f = x$, $g = x^2$: independientes."
          )),

        b("definicion",
          titulo="Wronskiano",
          body_md=(
              "Dadas dos funciones derivables $y_1, y_2$, su **wronskiano** es el determinante\n\n"
              "$$W(y_1, y_2)(x) \\;=\\; \\begin{vmatrix} y_1(x) & y_2(x) \\\\ y_1'(x) & y_2'(x) \\end{vmatrix} \\;=\\; y_1(x)\\, y_2'(x) - y_1'(x)\\, y_2(x).$$\n\n"
              "**Criterio del wronskiano (para soluciones de una EDO lineal de orden 2 con $p, q$ continuas).** "
              "Sean $y_1, y_2$ soluciones de $y'' + p y' + q y = 0$ en $I$. Entonces:\n\n"
              "- **Si existe $x_0 \\in I$ con $W(y_1, y_2)(x_0) \\neq 0$**, entonces $y_1, y_2$ son linealmente independientes en $I$.\n"
              "- **Si $W(y_1, y_2) \\equiv 0$ en $I$**, entonces $y_1, y_2$ son linealmente dependientes en $I$.\n\n"
              "**Hecho fuerte (consecuencia de la identidad de Abel):** el wronskiano de dos soluciones de la "
              "misma EDO lineal **o es idénticamente cero**, **o no se anula nunca** en $I$. No hay punto medio. "
              "Por eso basta evaluarlo en **un solo punto** para concluir."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar independencia con el wronskiano",
          problema_md=(
              "Comprueba que $y_1 = e^{2x}$ e $y_2 = e^{-2x}$ son soluciones de $y'' - 4y = 0$ y forman un "
              "conjunto linealmente independiente."
          ),
          pasos=[
              {"accion_md": (
                  "**Verificar que son soluciones.** $y_1' = 2 e^{2x}$, $y_1'' = 4 e^{2x}$, así $y_1'' - 4 y_1 = 4 e^{2x} - 4 e^{2x} = 0$. ✓\n\n"
                  "Análogamente $y_2'' - 4 y_2 = 4 e^{-2x} - 4 e^{-2x} = 0$. ✓"
              ),
               "justificacion_md": "Antes de hablar de wronskianos hay que confirmar que ambas son soluciones.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular el wronskiano:**\n\n"
                  "$$W(y_1, y_2) = \\begin{vmatrix} e^{2x} & e^{-2x} \\\\ 2 e^{2x} & -2 e^{-2x} \\end{vmatrix} = e^{2x}(-2 e^{-2x}) - e^{-2x}(2 e^{2x}) = -2 - 2 = -4.$$\n\n"
                  "$W = -4 \\neq 0$ para todo $x$."
              ),
               "justificacion_md": "Wronskiano constante no nulo (consistente con que $p \\equiv 0$ en esta EDO).",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión.** $y_1, y_2$ son linealmente independientes en $\\mathbb{R}$. La solución general de $y'' - 4y = 0$ es\n\n"
                  "$$y(x) = c_1 e^{2x} + c_2 e^{-2x}.$$"
              ),
               "justificacion_md": "Dos soluciones LI de una EDO lineal homogénea de orden 2 generan **toda** la solución.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Conjunto fundamental y solución general",
          body_md=(
              "Un par $\\{y_1, y_2\\}$ de soluciones **linealmente independientes** de la EDO homogénea de orden 2 "
              "se llama **conjunto fundamental de soluciones** en $I$.\n\n"
              "**Teorema (solución general).** Si $\\{y_1, y_2\\}$ es un conjunto fundamental en $I$, entonces "
              "**toda** solución $y$ de $y'' + p y' + q y = 0$ en $I$ se escribe de manera única como\n\n"
              "$$y(x) = c_1 y_1(x) + c_2 y_2(x), \\qquad c_1, c_2 \\in \\mathbb{R}.$$\n\n"
              "Esta es la **solución general** de la EDO homogénea.\n\n"
              "**Importancia:** la búsqueda de soluciones se reduce a encontrar **dos soluciones cualesquiera** "
              "que sean independientes — el resto se obtiene 'gratis' por superposición. Las próximas lecciones "
              "se concentran en **cómo encontrar** ese par."
          )),

        b("intuicion", body_md=(
            "**El espacio de soluciones es un plano.**\n\n"
            "Pensa el conjunto de todas las soluciones de $y'' + p y' + q y = 0$ como un **espacio vectorial**: "
            "los vectores son funciones, la suma y el producto por escalar son los usuales. El teorema dice "
            "que ese espacio tiene **dimensión exactamente 2**. Por eso $\\{y_1, y_2\\}$ LI es una **base**.\n\n"
            "**Analogía con $\\mathbb{R}^2$:** dos vectores no paralelos generan todo el plano. Aquí, dos "
            "soluciones no proporcionales generan todas las soluciones.\n\n"
            "**Consecuencia operativa:** dos soluciones distintas del mismo PVI **deben coincidir** (unicidad). "
            "Esto se usa muchas veces como herramienta: si encuentro algo que satisface la EDO y las "
            "condiciones iniciales, **es** la solución."
        )),

        b("ejemplo_resuelto",
          titulo="Resolver un PVI con conjunto fundamental conocido",
          problema_md=(
              "Sabiendo que $y_1 = \\cos(3x)$ e $y_2 = \\sin(3x)$ forman un conjunto fundamental de "
              "$y'' + 9 y = 0$, resuelve el PVI con $y(0) = 2$, $y'(0) = -3$."
          ),
          pasos=[
              {"accion_md": (
                  "**Solución general:**\n\n"
                  "$$y(x) = c_1 \\cos(3x) + c_2 \\sin(3x).$$\n\n"
                  "$$y'(x) = -3 c_1 \\sin(3x) + 3 c_2 \\cos(3x).$$"
              ),
               "justificacion_md": "Por superposición, toda solución tiene esta forma.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar las condiciones iniciales:**\n\n"
                  "- $y(0) = c_1 \\cos 0 + c_2 \\sin 0 = c_1 = 2 \\Rightarrow c_1 = 2$.\n"
                  "- $y'(0) = 3 c_2 = -3 \\Rightarrow c_2 = -1$."
              ),
               "justificacion_md": "Sistema lineal $2 \\times 2$ en $c_1, c_2$ — siempre tiene solución única si el wronskiano en $x_0$ es no nulo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución del PVI:**\n\n"
                  "$$y(x) = 2 \\cos(3x) - \\sin(3x).$$"
              ),
               "justificacion_md": "Por unicidad (E&U), no hay otra solución posible.",
               "es_resultado": True},
          ]),

        fig(
            "Gráfico cartesiano con eje x y eje y. Tres curvas superpuestas: y1 = cos(3x) en azul teal #06b6d4 (línea sólida fina), "
            "y2 = sin(3x) en gris (línea sólida fina), y la combinación y = 2 cos(3x) - sin(3x) en ámbar #f59e0b (línea más gruesa). "
            "Rango x: -π a π. Eje y: -3 a 3. Marcas en x = 0 con un punto negro mostrando que la curva ámbar pasa por (0, 2) con pendiente -3 (anotar 'PVI'). "
            "Cuadrícula tenue. Leyenda en la esquina superior derecha. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $y_1, y_2$ son soluciones LI de una EDO lineal homogénea de orden 2, su wronskiano:",
                  "opciones_md": [
                      "Puede anularse en algunos puntos",
                      "**No se anula en ningún punto del intervalo**",
                      "Siempre vale 1",
                      "Siempre es constante",
                  ],
                  "correcta": "B",
                  "pista_md": "Hecho fuerte derivado de la identidad de Abel.",
                  "explicacion_md": "**O es idénticamente cero, o nunca se anula.** Si son LI, no es cero, así que nunca se anula.",
              },
              {
                  "enunciado_md": "El wronskiano de $y_1 = x$ e $y_2 = x^2$ es:",
                  "opciones_md": ["$0$", "$x$", "**$x^2$**", "$x^3$"],
                  "correcta": "C",
                  "pista_md": "$W = y_1 y_2' - y_1' y_2$.",
                  "explicacion_md": "$W = x \\cdot 2x - 1 \\cdot x^2 = 2x^2 - x^2 = x^2$.",
              },
              {
                  "enunciado_md": "¿Cuántas constantes arbitrarias tiene la solución general de una EDO lineal homogénea de orden 2?",
                  "opciones_md": ["Una", "**Dos**", "Tres", "Depende del intervalo"],
                  "correcta": "B",
                  "pista_md": "Dimensión del espacio de soluciones.",
                  "explicacion_md": "**Dos.** El espacio de soluciones tiene dimensión 2; necesitamos dos coeficientes para escribir la base.",
              },
          ]),

        ej(
            "Wronskiano y conclusión",
            "Comprueba que $y_1 = e^x$ e $y_2 = x e^x$ son soluciones de $y'' - 2 y' + y = 0$ y forman un conjunto fundamental.",
            ["Verificar la EDO en cada una; calcular $W$."],
            (
                "**Soluciones.** $y_1' = y_1'' = e^x$, así $y_1'' - 2 y_1' + y_1 = e^x - 2 e^x + e^x = 0$. ✓\n\n"
                "Para $y_2 = x e^x$: $y_2' = (1+x) e^x$, $y_2'' = (2+x) e^x$. Sustituyendo: $(2+x) e^x - 2(1+x) e^x + x e^x = (2 + x - 2 - 2x + x) e^x = 0$. ✓\n\n"
                "**Wronskiano.** $W = e^x \\cdot (1+x) e^x - e^x \\cdot x e^x = e^{2x}((1+x) - x) = e^{2x} \\neq 0$. **Conjunto fundamental.**"
            ),
        ),

        ej(
            "Construir solución general",
            "Sabiendo que $y_1 = x^2$, $y_2 = x^{-1}$ son soluciones independientes de $x^2 y'' - 2 y = 0$ en $(0, \\infty)$, escribe la solución general y resuelve el PVI $y(1) = 0$, $y'(1) = 3$.",
            ["$y = c_1 x^2 + c_2 / x$ y aplicar condiciones."],
            (
                "$y = c_1 x^2 + c_2 / x$, $y' = 2 c_1 x - c_2 / x^2$.\n\n"
                "$y(1) = c_1 + c_2 = 0$, $y'(1) = 2 c_1 - c_2 = 3$. Sumando: $3 c_1 = 3 \\Rightarrow c_1 = 1$, $c_2 = -1$.\n\n"
                "**Solución:** $y(x) = x^2 - 1/x$ en $(0, \\infty)$."
            ),
        ),

        ej(
            "Detectar dependencia",
            "¿Son $y_1 = \\sin x$ e $y_2 = \\cos(x - \\pi/2)$ linealmente independientes en $\\mathbb{R}$?",
            ["Reescribir $\\cos(x - \\pi/2)$."],
            (
                "$\\cos(x - \\pi/2) = \\cos x \\cos(\\pi/2) + \\sin x \\sin(\\pi/2) = \\sin x$. "
                "Es decir, $y_2 = y_1$. **Linealmente dependientes** (su wronskiano es 0)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Concluir 'LI' de un wronskiano nulo en un solo punto.** El criterio fuerte aplica solo a soluciones de la misma EDO lineal; para funciones generales un wronskiano nulo en un punto no implica nada.",
              "**Olvidar verificar que cada $y_i$ es solución antes de calcular el wronskiano.** Sin eso el criterio del wronskiano no aplica.",
              "**Pensar que la solución general 'es' una solución particular.** La solución general es una **familia** parametrizada por dos constantes; la solución particular se obtiene fijando esas constantes.",
              "**Usar superposición en una EDO no lineal.** Solo es válida en EDOs lineales homogéneas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Superposición:** combinación lineal de soluciones de la EDO homogénea es solución.",
              "**Independencia lineal:** ninguna es múltiplo escalar de la otra.",
              "**Wronskiano:** $W(y_1, y_2) = y_1 y_2' - y_1' y_2$. Para soluciones de la misma EDO lineal, $W \\not\\equiv 0$ $\\Leftrightarrow$ LI.",
              "**Conjunto fundamental:** par $\\{y_1, y_2\\}$ LI. La solución general es $y = c_1 y_1 + c_2 y_2$.",
              "**Próxima lección:** método sistemático para encontrar conjuntos fundamentales cuando los coeficientes son constantes.",
          ]),
    ]
    return {
        "id": "lec-ed-2-2-homogenea-solucion-general",
        "title": "EDO homogénea: solución general",
        "description": "Principio de superposición, independencia lineal, wronskiano, conjunto fundamental y solución general de la EDO lineal homogénea de orden 2.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# Coeficientes constantes (orden 2)
# =====================================================================
def lesson_coef_constantes():
    blocks = [
        b("texto", body_md=(
            "En la lección anterior vimos que la solución general de\n\n"
            "$$y'' + p(x) y' + q(x) y = 0$$\n\n"
            "queda determinada en cuanto encontramos **dos soluciones linealmente independientes**. Pero "
            "**¿cómo encontrarlas?** Para coeficientes generales el problema es difícil, pero hay un caso muy "
            "importante donde tenemos un **método sistemático y completo**: cuando los coeficientes son "
            "**constantes**.\n\n"
            "$$a y'' + b y' + c y = 0, \\qquad a, b, c \\in \\mathbb{R}, \\quad a \\neq 0.$$\n\n"
            "El método se basa en una sola idea: **probar soluciones de la forma $y = e^{rx}$**. Sustituyendo, "
            "obtenemos una **ecuación algebraica** para $r$ — la ecuación característica — que clasifica todo "
            "según tres casos.\n\n"
            "**Al terminar:**\n\n"
            "- Escribes la **ecuación característica** de cualquier EDO con coeficientes constantes.\n"
            "- Distingues los **tres casos** según el discriminante (raíces reales distintas, doble, complejas).\n"
            "- Escribes la **solución general** en cada caso y resuelves PVIs."
        )),

        b("definicion",
          titulo="Ecuación característica",
          body_md=(
              "**Idea.** Probamos $y = e^{rx}$ en $a y'' + b y' + c y = 0$. Como $y' = r e^{rx}$ y $y'' = r^2 e^{rx}$, sustituyendo:\n\n"
              "$$a r^2 e^{rx} + b r e^{rx} + c e^{rx} = (a r^2 + b r + c)\\, e^{rx} = 0.$$\n\n"
              "Como $e^{rx} \\neq 0$ para todo $x$, la EDO se reduce a la ecuación algebraica\n\n"
              "$$\\boxed{a r^2 + b r + c = 0}$$\n\n"
              "llamada **ecuación característica** (o ecuación auxiliar).\n\n"
              "Sus raíces $r_1, r_2$ provienen de\n\n"
              "$$r = \\dfrac{-b \\pm \\sqrt{b^2 - 4ac}}{2a},$$\n\n"
              "y el **discriminante** $\\Delta = b^2 - 4ac$ separa tres casos."
          )),

        formulas(
            titulo="Los tres casos",
            body=(
                "**Caso 1 — Raíces reales y distintas** ($\\Delta > 0$, $r_1 \\neq r_2$ reales):\n\n"
                "$$y(x) = c_1 e^{r_1 x} + c_2 e^{r_2 x}.$$\n\n"
                "Las dos exponenciales son LI (su wronskiano es $(r_2 - r_1) e^{(r_1 + r_2)x} \\neq 0$).\n\n"
                "**Caso 2 — Raíz real doble** ($\\Delta = 0$, $r_1 = r_2 = r = -b/(2a)$):\n\n"
                "$$y(x) = (c_1 + c_2 x)\\, e^{r x}.$$\n\n"
                "El factor extra $x$ asegura independencia lineal (de lo contrario tendríamos una sola exponencial).\n\n"
                "**Caso 3 — Raíces complejas conjugadas** ($\\Delta < 0$, $r = \\alpha \\pm i\\beta$ con $\\beta > 0$):\n\n"
                "$$y(x) = e^{\\alpha x}\\bigl(c_1 \\cos(\\beta x) + c_2 \\sin(\\beta x)\\bigr).$$\n\n"
                "**Origen.** $e^{(\\alpha + i\\beta)x} = e^{\\alpha x}(\\cos\\beta x + i \\sin\\beta x)$ por la fórmula de Euler. "
                "Tomando partes real e imaginaria obtenemos las dos soluciones reales LI."
            ),
        ),

        b("intuicion", body_md=(
            "**¿Por qué exponenciales?** En una EDO de coeficientes constantes, derivar **multiplica** por una "
            "constante (la constante característica $r$). La función $e^{rx}$ tiene la propiedad mágica de que "
            "$\\frac{d}{dx} e^{rx} = r e^{rx}$ — derivar es lo mismo que multiplicar. Eso convierte la ecuación "
            "diferencial en una ecuación algebraica.\n\n"
            "**Significado físico de las raíces:**\n\n"
            "- **Reales negativas:** decaimiento exponencial puro.\n"
            "- **Reales positivas:** crecimiento explosivo (sistema inestable).\n"
            "- **Complejas con $\\alpha < 0$:** oscilación amortiguada.\n"
            "- **Complejas con $\\alpha = 0$:** oscilación pura (MAS).\n"
            "- **Complejas con $\\alpha > 0$:** oscilación con amplitud creciente."
        )),

        b("ejemplo_resuelto",
          titulo="Caso 1 — Raíces reales distintas",
          problema_md="Resuelve $2 y'' - 7 y' + 3 y = 0$.",
          pasos=[
              {"accion_md": (
                  "**Ecuación característica:** $2 r^2 - 7 r + 3 = 0$.\n\n"
                  "Factorizando: $(2 r - 1)(r - 3) = 0 \\Rightarrow r_1 = 1/2$, $r_2 = 3$."
              ),
               "justificacion_md": "Discriminante $\\Delta = 49 - 24 = 25 > 0$ — dos raíces reales distintas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:**\n\n"
                  "$$y(x) = c_1 e^{x/2} + c_2 e^{3x}.$$"
              ),
               "justificacion_md": "Combinación lineal de las dos exponenciales.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caso 2 — Raíz doble (con PVI)",
          problema_md="Resuelve $y'' + 2 y' + y = 0$ con $y(0) = 5$, $y'(0) = -3$.",
          pasos=[
              {"accion_md": (
                  "**Ecuación característica:** $r^2 + 2 r + 1 = (r + 1)^2 = 0 \\Rightarrow r = -1$ (doble).\n\n"
                  "**Solución general:** $y(x) = (c_1 + c_2 x) e^{-x}$."
              ),
               "justificacion_md": "$\\Delta = 4 - 4 = 0$. Por la raíz doble, agregamos el factor $x$ a la segunda solución.",
               "es_resultado": False},
              {"accion_md": (
                  "**Derivada:**\n\n"
                  "$$y'(x) = c_2 e^{-x} - (c_1 + c_2 x) e^{-x} = (c_2 - c_1 - c_2 x) e^{-x}.$$"
              ),
               "justificacion_md": "Producto regla, cuidando el signo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar condiciones iniciales:**\n\n"
                  "- $y(0) = c_1 = 5$.\n"
                  "- $y'(0) = c_2 - c_1 = -3 \\Rightarrow c_2 = 2$.\n\n"
                  "**Solución del PVI:** $y(x) = (5 + 2 x) e^{-x}$."
              ),
               "justificacion_md": "Sistema lineal $2 \\times 2$, solución única.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caso 3 — Raíces complejas",
          problema_md="Resuelve $y'' - 2 y' + 5 y = 0$.",
          pasos=[
              {"accion_md": (
                  "**Ecuación característica:** $r^2 - 2 r + 5 = 0$.\n\n"
                  "$\\Delta = 4 - 20 = -16 < 0$. Raíces:\n\n"
                  "$$r = \\dfrac{2 \\pm \\sqrt{-16}}{2} = 1 \\pm 2 i.$$\n\n"
                  "Es decir, $\\alpha = 1$, $\\beta = 2$."
              ),
               "justificacion_md": "Identificar $\\alpha$ (parte real) y $\\beta$ (parte imaginaria positiva).",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:**\n\n"
                  "$$y(x) = e^{x}\\bigl(c_1 \\cos(2x) + c_2 \\sin(2x)\\bigr).$$"
              ),
               "justificacion_md": "Plantilla del Caso 3. La envolvente $e^{x}$ es exponencial creciente porque $\\alpha = 1 > 0$.",
               "es_resultado": True},
          ]),

        fig(
            "Tres paneles horizontales lado a lado, fondo blanco, mostrando las formas cualitativas de solución según el tipo de raíces. "
            "Panel izquierdo (Caso 1: raíces reales distintas, ejemplo y'' - 5y' + 6y = 0): dos curvas exponenciales en teal #06b6d4 (e^{2x}) y ámbar #f59e0b (e^{3x}), título 'Δ > 0'. "
            "Panel central (Caso 2: raíz doble, ejemplo y'' + 2y' + y = 0): una curva (1 + x)e^{-x} en teal mostrando el factor x*exp con un máximo y luego decaimiento, título 'Δ = 0'. "
            "Panel derecho (Caso 3: complejas, ejemplo y'' + 4y = 0): oscilación cos(2x) en teal y otra amortiguada e^{-x/2}cos(2x) en ámbar, título 'Δ < 0'. "
            "Cada panel con ejes pequeños x e y, cuadrícula tenue y nota debajo con la fórmula. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La ecuación característica de $y'' + 4 y' + 13 y = 0$ es:",
                  "opciones_md": [
                      "$r + 4 + 13 = 0$",
                      "**$r^2 + 4 r + 13 = 0$**",
                      "$r^2 + 4 = 0$",
                      "$r^2 + 13 r + 4 = 0$",
                  ],
                  "correcta": "B",
                  "pista_md": "Reemplazar $y^{(k)}$ por $r^k$ con coeficientes intactos.",
                  "explicacion_md": "**$r^2 + 4r + 13 = 0$**, con discriminante $16 - 52 = -36$ (raíces complejas).",
              },
              {
                  "enunciado_md": "La solución general de $y'' + 4 y = 0$ es:",
                  "opciones_md": [
                      "$c_1 e^{2x} + c_2 e^{-2x}$",
                      "$(c_1 + c_2 x) e^{2x}$",
                      "**$c_1 \\cos(2x) + c_2 \\sin(2x)$**",
                      "$c_1 e^{x} \\cos(2x) + c_2 e^{x} \\sin(2x)$",
                  ],
                  "correcta": "C",
                  "pista_md": "Raíces $r = \\pm 2i$, así $\\alpha = 0$, $\\beta = 2$.",
                  "explicacion_md": "Como $\\alpha = 0$, no hay factor exponencial. **MAS puro.**",
              },
              {
                  "enunciado_md": "Si la ecuación característica es $(r + 3)^2 = 0$, la solución general es:",
                  "opciones_md": [
                      "$c_1 e^{-3x} + c_2 e^{3x}$",
                      "**$(c_1 + c_2 x) e^{-3x}$**",
                      "$c_1 \\cos(3x) + c_2 \\sin(3x)$",
                      "$e^{-3x}(c_1 \\cos x + c_2 \\sin x)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Raíz doble en $r = -3$.",
                  "explicacion_md": "Caso 2: la segunda solución LI lleva un factor $x$.",
              },
          ]),

        ej(
            "Reales distintas con PVI",
            "Resuelve $y'' - y' - 6 y = 0$ con $y(0) = 1$, $y'(0) = 0$.",
            ["Factorizar $r^2 - r - 6$."],
            (
                "$r^2 - r - 6 = (r - 3)(r + 2) = 0 \\Rightarrow r = 3, -2$. "
                "$y = c_1 e^{3x} + c_2 e^{-2x}$, $y' = 3 c_1 e^{3x} - 2 c_2 e^{-2x}$.\n\n"
                "$y(0) = c_1 + c_2 = 1$, $y'(0) = 3 c_1 - 2 c_2 = 0$. Resolviendo: $c_1 = 2/5$, $c_2 = 3/5$.\n\n"
                "**Solución:** $y(x) = \\dfrac{2}{5} e^{3x} + \\dfrac{3}{5} e^{-2x}$."
            ),
        ),

        ej(
            "Raíz doble",
            "Resuelve $4 y'' + 12 y' + 9 y = 0$.",
            ["Discriminante $= 144 - 144 = 0$."],
            (
                "$4 r^2 + 12 r + 9 = (2 r + 3)^2 = 0 \\Rightarrow r = -3/2$ doble. "
                "**Solución:** $y(x) = (c_1 + c_2 x) e^{-3x/2}$."
            ),
        ),

        ej(
            "Complejas con PVI",
            "Resuelve $y'' + 6 y' + 13 y = 0$ con $y(0) = 0$, $y'(0) = 4$.",
            ["Raíces $-3 \\pm 2 i$."],
            (
                "$r^2 + 6 r + 13 = 0 \\Rightarrow r = -3 \\pm 2 i$. "
                "$y = e^{-3x}(c_1 \\cos 2x + c_2 \\sin 2x)$.\n\n"
                "$y(0) = c_1 = 0$. $y' = -3 e^{-3x}(c_1 \\cos 2x + c_2 \\sin 2x) + e^{-3x}(-2 c_1 \\sin 2x + 2 c_2 \\cos 2x)$. "
                "$y'(0) = -3 c_1 + 2 c_2 = 2 c_2 = 4 \\Rightarrow c_2 = 2$.\n\n"
                "**Solución:** $y(x) = 2 e^{-3x} \\sin(2x)$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $x$ en el caso de raíz doble.** Sin él la solución general queda con una sola constante (¡falta una!).",
              "**Tomar $\\beta = 0$ en raíces complejas.** Si las raíces son reales, no se usa la fórmula trigonométrica.",
              "**Equivocarse de signo en el discriminante.** Conviene siempre escribir $\\Delta = b^2 - 4 a c$ y mirar su signo antes de extraer raíces.",
              "**Cancelar mal $e^{rx}$ en la sustitución.** Solo se cancela porque $e^{rx} \\neq 0$ para todo $x$ — ese paso es clave para reducir a álgebra.",
              "**Olvidar normalizar coeficientes.** $a$ debe ser no nulo, pero también hay que llevar la EDO a la forma $a y'' + b y' + c y = 0$ antes de leer los coeficientes.",
          ]),

        b("resumen",
          puntos_md=[
              "**Ecuación característica:** $a r^2 + b r + c = 0$ obtenida al probar $y = e^{rx}$.",
              "**Caso 1 ($\\Delta > 0$):** $y = c_1 e^{r_1 x} + c_2 e^{r_2 x}$.",
              "**Caso 2 ($\\Delta = 0$):** $y = (c_1 + c_2 x) e^{r x}$.",
              "**Caso 3 ($\\Delta < 0$, $r = \\alpha \\pm i \\beta$):** $y = e^{\\alpha x}(c_1 \\cos\\beta x + c_2 \\sin\\beta x)$.",
              "**Próxima lección:** generalización a EDOs lineales de orden $n$ — superposición y wronskiano para más funciones.",
          ]),
    ]
    return {
        "id": "lec-ed-2-3-coeficientes-constantes",
        "title": "Coeficientes constantes",
        "description": "Ecuación característica para EDOs lineales homogéneas de orden 2 con coeficientes constantes. Tres casos según discriminante: raíces reales distintas, doble y complejas conjugadas.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# EDO de orden n
# =====================================================================
def lesson_orden_n():
    blocks = [
        b("texto", body_md=(
            "Toda la teoría que hemos visto para la EDO lineal de orden 2 se generaliza a EDOs lineales de "
            "**orden $n$**. Los enunciados son casi los mismos, solo que ahora el espacio de soluciones tiene "
            "**dimensión $n$** y el wronskiano es un determinante de tamaño $n \\times n$.\n\n"
            "**Forma general:**\n\n"
            "$$y^{(n)} + p_{n-1}(x) y^{(n-1)} + \\cdots + p_1(x) y' + p_0(x) y = f(x).$$\n\n"
            "**¿Cuándo aparecen?** Vigas (orden 4), modelos de control con varios estados acoplados, sistemas "
            "mecánicos con varios grados de libertad linealizados a una variable, ecuaciones que provienen de "
            "eliminar variables en sistemas de EDOs de primer orden.\n\n"
            "**Al terminar:**\n\n"
            "- Reconoces la **forma estándar** de orden $n$ y los datos del PVI.\n"
            "- Aplicas el **principio de superposición** y el **teorema de existencia y unicidad** en orden $n$.\n"
            "- Calculas el **wronskiano** de $n$ funciones y lo usas para detectar conjuntos fundamentales.\n"
            "- Escribes la **solución general** como combinación lineal de $n$ soluciones LI."
        )),

        b("definicion",
          titulo="EDO lineal de orden n y PVI",
          body_md=(
              "Una **EDO lineal de orden $n$** en forma estándar es\n\n"
              "$$y^{(n)} + p_{n-1}(x) y^{(n-1)} + \\cdots + p_1(x) y' + p_0(x) y = f(x).$$\n\n"
              "Es **homogénea** si $f \\equiv 0$.\n\n"
              "Un **PVI de orden $n$** consiste en la EDO más $n$ condiciones iniciales en el mismo punto $x_0$:\n\n"
              "$$y(x_0) = b_0, \\quad y'(x_0) = b_1, \\quad \\ldots, \\quad y^{(n-1)}(x_0) = b_{n-1}.$$\n\n"
              "**Teorema (E&U, orden $n$).** Si $p_0, p_1, \\ldots, p_{n-1}, f$ son continuas en un intervalo "
              "abierto $I \\ni x_0$, entonces el PVI tiene una **única** solución definida en todo $I$."
          )),

        b("definicion",
          titulo="Superposición y dependencia lineal",
          body_md=(
              "**Principio de superposición.** Si $y_1, \\ldots, y_n$ son soluciones de la ecuación homogénea\n\n"
              "$$y^{(n)} + p_{n-1} y^{(n-1)} + \\cdots + p_0 y = 0,$$\n\n"
              "entonces toda combinación lineal $y = c_1 y_1 + \\cdots + c_n y_n$ también es solución.\n\n"
              "**Independencia lineal.** Las funciones $y_1, \\ldots, y_n$ son **linealmente dependientes** en $I$ "
              "si existen constantes $c_1, \\ldots, c_n$ no todas nulas tales que\n\n"
              "$$c_1 y_1(x) + c_2 y_2(x) + \\cdots + c_n y_n(x) = 0 \\quad \\text{para todo } x \\in I.$$\n\n"
              "Caso contrario son **linealmente independientes**: la única combinación lineal idénticamente "
              "nula tiene todos los coeficientes cero."
          )),

        b("definicion",
          titulo="Wronskiano de n funciones",
          body_md=(
              "Dadas $y_1, y_2, \\ldots, y_n$ con $n - 1$ derivadas, su **wronskiano** es el determinante\n\n"
              "$$W(y_1, \\ldots, y_n)(x) = \\begin{vmatrix} y_1 & y_2 & \\cdots & y_n \\\\ y_1' & y_2' & \\cdots & y_n' \\\\ \\vdots & \\vdots & \\ddots & \\vdots \\\\ y_1^{(n-1)} & y_2^{(n-1)} & \\cdots & y_n^{(n-1)} \\end{vmatrix}.$$\n\n"
              "**Criterio (para soluciones de la misma EDO lineal homogénea con coeficientes continuos):**\n\n"
              "- Si $W(y_1, \\ldots, y_n)(x_0) \\neq 0$ para algún $x_0 \\in I$, entonces $y_1, \\ldots, y_n$ son LI en $I$.\n"
              "- Si $W \\equiv 0$ en $I$, entonces son LD.\n\n"
              "Como antes, **o $W \\equiv 0$, o $W$ no se anula nunca** en $I$ (consecuencia de Abel)."
          )),

        b("definicion",
          titulo="Conjunto fundamental y solución general",
          body_md=(
              "Un conjunto $\\{y_1, \\ldots, y_n\\}$ de **$n$ soluciones LI** de la ecuación homogénea de orden "
              "$n$ se llama **conjunto fundamental** en $I$.\n\n"
              "**Teorema (estructura de soluciones).** Si $\\{y_1, \\ldots, y_n\\}$ es fundamental, entonces "
              "**toda** solución de la EDO homogénea se escribe de manera única como\n\n"
              "$$y(x) = c_1 y_1(x) + c_2 y_2(x) + \\cdots + c_n y_n(x), \\qquad c_i \\in \\mathbb{R}.$$\n\n"
              "El espacio de soluciones es un **espacio vectorial de dimensión $n$**."
          )),

        b("intuicion", body_md=(
            "**Por qué $n$ y no más.** Una EDO lineal de orden $n$ permite despejar $y^{(n)}$ en términos de "
            "$y, y', \\ldots, y^{(n-1)}$. Eso significa que el 'estado' del sistema en cada instante son las $n$ "
            "cantidades $y, y', \\ldots, y^{(n-1)}$ — **$n$ grados de libertad**. La condición inicial fija esos "
            "$n$ valores y el resto queda determinado.\n\n"
            "**Equivalencia con sistema de orden 1.** La EDO de orden $n$ se puede reescribir como un "
            "**sistema de $n$ EDOs de primer orden** definiendo $u_1 = y$, $u_2 = y'$, ..., $u_n = y^{(n-1)}$. "
            "Esa equivalencia es la base del análisis de sistemas (próximo capítulo)."
        )),

        b("ejemplo_resuelto",
          titulo="Verificar conjunto fundamental (orden 3)",
          problema_md=(
              "Comprueba que $y_1 = 1$, $y_2 = x$, $y_3 = x^2$ son soluciones LI de $y''' = 0$ en $\\mathbb{R}$ "
              "y escribe la solución general."
          ),
          pasos=[
              {"accion_md": (
                  "**Verificar que cada una es solución.** $y_1''' = 0$, $y_2''' = 0$, $y_3''' = 0$. ✓"
              ),
               "justificacion_md": "Polinomios de grado $< 3$ tienen tercera derivada nula.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular el wronskiano:**\n\n"
                  "$$W = \\begin{vmatrix} 1 & x & x^2 \\\\ 0 & 1 & 2x \\\\ 0 & 0 & 2 \\end{vmatrix}.$$\n\n"
                  "Es triangular superior, así $W = 1 \\cdot 1 \\cdot 2 = 2 \\neq 0$ en todo $\\mathbb{R}$."
              ),
               "justificacion_md": "Determinante triangular: producto de la diagonal.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión.** $\\{1, x, x^2\\}$ es conjunto fundamental. La solución general de $y''' = 0$ es\n\n"
                  "$$y(x) = c_1 + c_2 x + c_3 x^2,$$\n\n"
                  "es decir, **todos los polinomios de grado $\\leq 2$**."
              ),
               "justificacion_md": "Era esperable: $y''' = 0$ se integra tres veces dando un polinomio de grado 2.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="PVI de orden 3",
          problema_md="Resuelve $y''' = 0$ con $y(0) = 1$, $y'(0) = 2$, $y''(0) = -4$.",
          pasos=[
              {"accion_md": (
                  "**Solución general** (del ejemplo anterior): $y = c_1 + c_2 x + c_3 x^2$.\n\n"
                  "$y' = c_2 + 2 c_3 x$, $y'' = 2 c_3$."
              ),
               "justificacion_md": "Tres derivadas listas para imponer las tres condiciones.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar condiciones iniciales:**\n\n"
                  "- $y(0) = c_1 = 1$.\n"
                  "- $y'(0) = c_2 = 2$.\n"
                  "- $y''(0) = 2 c_3 = -4 \\Rightarrow c_3 = -2$."
              ),
               "justificacion_md": "Sistema diagonal — uno a uno por cada coeficiente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución del PVI:** $y(x) = 1 + 2 x - 2 x^2$."
              ),
               "justificacion_md": "Tres condiciones iniciales fijan los tres parámetros.",
               "es_resultado": True},
          ]),

        fig(
            "Esquema visual de cómo n soluciones LI forman una base del espacio de soluciones. "
            "A la izquierda, tres curvas etiquetadas y_1, y_2, y_3 en colores distintos (teal #06b6d4, ámbar #f59e0b, gris). "
            "Una flecha grande horizontal a la derecha con etiqueta 'combinación lineal: c_1 y_1 + c_2 y_2 + c_3 y_3'. "
            "A la derecha, un par de curvas resultantes (dos ejemplos de combinaciones distintas) en color púrpura. "
            "Debajo, una caja rectangular con la fórmula y = c_1 y_1 + c_2 y_2 + c_3 y_3 y la nota 'dim = n = 3'. "
            + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El espacio de soluciones de una EDO lineal homogénea de orden $n$ tiene dimensión:",
                  "opciones_md": ["$1$", "$n - 1$", "**$n$**", "$n + 1$"],
                  "correcta": "C",
                  "pista_md": "Tantas constantes como el orden.",
                  "explicacion_md": "**$n$.** Un PVI de orden $n$ requiere $n$ condiciones iniciales y la solución general tiene $n$ constantes.",
              },
              {
                  "enunciado_md": "Para usar el criterio del wronskiano y concluir 'LI', $W$ debe ser:",
                  "opciones_md": [
                      "Constante en $I$",
                      "**No nulo en al menos un punto de $I$**",
                      "Nulo en algún punto",
                      "Positivo en todo $I$",
                  ],
                  "correcta": "B",
                  "pista_md": "Recuerda que para soluciones de la misma EDO, $W \\not\\equiv 0$ y $W \\neq 0$ en cualquier punto coinciden.",
                  "explicacion_md": "Basta evaluarlo en un solo punto cómodo y ver que no se anula.",
              },
              {
                  "enunciado_md": "El wronskiano de $\\{1, x, x^2, x^3\\}$ es:",
                  "opciones_md": ["$0$", "$x^6$", "**$12$**", "$24 x$"],
                  "correcta": "C",
                  "pista_md": "Determinante triangular superior con diagonal $1, 1, 2, 6$.",
                  "explicacion_md": "$W = 1 \\cdot 1 \\cdot 2 \\cdot 6 = 12$. Son LI en $\\mathbb{R}$.",
              },
          ]),

        ej(
            "Wronskiano de tres exponenciales",
            "Calcula el wronskiano de $y_1 = e^x$, $y_2 = e^{2x}$, $y_3 = e^{3x}$ y concluye sobre su independencia.",
            ["Sacar factor común $e^{6x}$ y reconocer determinante de Vandermonde."],
            (
                "$W = e^{6x} \\det\\begin{pmatrix} 1 & 1 & 1 \\\\ 1 & 2 & 3 \\\\ 1 & 4 & 9 \\end{pmatrix} = e^{6x} \\cdot 2 = 2 e^{6x} \\neq 0$.\n\n"
                "**LI en $\\mathbb{R}$.** (Más en general, $\\{e^{r_1 x}, \\ldots, e^{r_n x}\\}$ con $r_i$ distintas son siempre LI.)"
            ),
        ),

        ej(
            "Conjunto fundamental conocido",
            "Sabiendo que $y_1 = e^x$, $y_2 = x e^x$, $y_3 = e^{-x}$ es un conjunto fundamental de cierta EDO de orden 3, escribe la solución general y resuelve el PVI $y(0) = 0$, $y'(0) = 1$, $y''(0) = 2$.",
            ["$y = c_1 e^x + c_2 x e^x + c_3 e^{-x}$ y aplicar condiciones."],
            (
                "$y = c_1 e^x + c_2 x e^x + c_3 e^{-x}$, $y' = (c_1 + c_2) e^x + c_2 x e^x - c_3 e^{-x}$, "
                "$y'' = (c_1 + 2 c_2) e^x + c_2 x e^x + c_3 e^{-x}$.\n\n"
                "$y(0) = c_1 + c_3 = 0$, $y'(0) = c_1 + c_2 - c_3 = 1$, $y''(0) = c_1 + 2 c_2 + c_3 = 2$.\n\n"
                "De la primera: $c_3 = -c_1$. Sustituyendo: $2 c_1 + c_2 = 1$, $c_1 + 2 c_2 - c_1 = 2 \\Rightarrow c_2 = 1$, $c_1 = 0$, $c_3 = 0$.\n\n"
                "**Solución:** $y(x) = x e^x$."
            ),
        ),

        ej(
            "Detectar dependencia",
            "¿Son LI las funciones $y_1 = \\sin^2 x$, $y_2 = \\cos^2 x$, $y_3 = 1$ en $\\mathbb{R}$?",
            ["Identidad pitagórica."],
            (
                "$\\sin^2 x + \\cos^2 x = 1$, es decir, $1 \\cdot y_1 + 1 \\cdot y_2 + (-1) \\cdot y_3 = 0$ con coeficientes no todos nulos. "
                "**Linealmente dependientes.**"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar el criterio del wronskiano a funciones que no son soluciones de la misma EDO lineal.** En ese caso $W = 0$ no implica LD.",
              "**Olvidar que necesitamos $n$ soluciones LI** (ni más ni menos) para una EDO de orden $n$.",
              "**Equivocarse en el orden de derivación al armar el wronskiano.** La fila $k$-ésima son las derivadas de orden $k - 1$.",
              "**Confundir EDO de orden $n$ con sistema de $n$ EDOs.** Son objetos relacionados pero distintos: el sistema vive en $\\mathbb{R}^n$ con una sola variable independiente.",
          ]),

        b("resumen",
          puntos_md=[
              "**EDO lineal de orden $n$:** $y^{(n)} + p_{n-1} y^{(n-1)} + \\cdots + p_0 y = f$.",
              "**PVI:** EDO + valores de $y, y', \\ldots, y^{(n-1)}$ en $x_0$. E&U garantizado si los coeficientes son continuos.",
              "**Wronskiano:** determinante $n \\times n$. Para soluciones de la EDO, $W \\not\\equiv 0$ $\\Leftrightarrow$ LI.",
              "**Conjunto fundamental:** $n$ soluciones LI; la solución general es su combinación lineal.",
              "**Próxima lección:** método de coeficientes constantes generalizado a orden $n$ — multiplicidades, raíces complejas múltiples.",
          ]),
    ]
    return {
        "id": "lec-ed-2-4-orden-n",
        "title": "EDO de orden n",
        "description": "Generalización a orden n: principio de superposición, dependencia lineal, wronskiano de n funciones, conjunto fundamental y solución general.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 4,
    }


# =====================================================================
# Coeficientes constantes orden superior
# =====================================================================
def lesson_coef_const_orden_n():
    blocks = [
        b("texto", body_md=(
            "El método de la **ecuación característica** se extiende sin sorpresas a la EDO lineal homogénea de "
            "**orden $n$ con coeficientes constantes**:\n\n"
            "$$a_n y^{(n)} + a_{n-1} y^{(n-1)} + \\cdots + a_1 y' + a_0 y = 0.$$\n\n"
            "Probando $y = e^{rx}$ se obtiene la **ecuación característica de grado $n$**:\n\n"
            "$$a_n r^n + a_{n-1} r^{n-1} + \\cdots + a_1 r + a_0 = 0.$$\n\n"
            "Por el teorema fundamental del álgebra, este polinomio tiene **exactamente $n$ raíces complejas** "
            "(contadas con multiplicidad). Cada raíz contribuye soluciones según las mismas reglas del orden 2, "
            "extendidas para tratar **multiplicidades altas**.\n\n"
            "**Al terminar:**\n\n"
            "- Construyes la **ecuación característica** de cualquier EDO lineal de coeficientes constantes.\n"
            "- Manejas **raíces reales múltiples** (factor $1, x, x^2, \\ldots, x^{m-1}$).\n"
            "- Manejas **raíces complejas múltiples** (factor extra $1, x, x^2, \\ldots$).\n"
            "- Escribes la **solución general** combinando todas las contribuciones."
        )),

        b("definicion",
          titulo="Ecuación característica de grado n",
          body_md=(
              "Para $a_n y^{(n)} + \\cdots + a_1 y' + a_0 y = 0$ ($a_n \\neq 0$), la ecuación característica es\n\n"
              "$$P(r) = a_n r^n + a_{n-1} r^{n-1} + \\cdots + a_1 r + a_0 = 0.$$\n\n"
              "El polinomio $P(r)$ se factoriza sobre $\\mathbb{C}$ como\n\n"
              "$$P(r) = a_n (r - r_1)^{m_1} (r - r_2)^{m_2} \\cdots (r - r_k)^{m_k},$$\n\n"
              "donde $r_1, \\ldots, r_k$ son las raíces distintas y $m_1, \\ldots, m_k$ sus **multiplicidades** "
              "(con $m_1 + m_2 + \\cdots + m_k = n$).\n\n"
              "**Las raíces complejas vienen siempre en pares conjugados** $\\alpha \\pm i\\beta$, ambas con la misma multiplicidad."
          )),

        formulas(
            titulo="Soluciones según el tipo de raíz",
            body=(
                "**Regla general:** cada raíz aporta tantas soluciones LI como su multiplicidad, multiplicando "
                "por potencias crecientes de $x$.\n\n"
                "**Raíz real $r$ de multiplicidad $m$:** aporta\n\n"
                "$$e^{r x}, \\quad x e^{r x}, \\quad x^2 e^{r x}, \\quad \\ldots, \\quad x^{m-1} e^{r x}.$$\n\n"
                "**Par de raíces complejas conjugadas $\\alpha \\pm i\\beta$ de multiplicidad $m$:** aportan $2m$ soluciones reales\n\n"
                "$$e^{\\alpha x} \\cos(\\beta x), \\quad e^{\\alpha x} \\sin(\\beta x),$$\n"
                "$$x e^{\\alpha x} \\cos(\\beta x), \\quad x e^{\\alpha x} \\sin(\\beta x),$$\n"
                "$$\\vdots$$\n"
                "$$x^{m-1} e^{\\alpha x} \\cos(\\beta x), \\quad x^{m-1} e^{\\alpha x} \\sin(\\beta x).$$\n\n"
                "**La solución general** es la combinación lineal de todas estas $n$ soluciones, con $n$ "
                "constantes arbitrarias."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Orden 3 — raíces reales distintas",
          problema_md="Resuelve $y''' - 6 y'' + 11 y' - 6 y = 0$.",
          pasos=[
              {"accion_md": (
                  "**Ecuación característica:** $r^3 - 6 r^2 + 11 r - 6 = 0$.\n\n"
                  "Probamos divisores de 6 ($\\pm 1, \\pm 2, \\pm 3, \\pm 6$): $r = 1$ funciona.\n\n"
                  "Dividiendo: $r^3 - 6 r^2 + 11 r - 6 = (r - 1)(r^2 - 5 r + 6) = (r - 1)(r - 2)(r - 3)$."
              ),
               "justificacion_md": "Teorema de raíces racionales y factorización por división sintética.",
               "es_resultado": False},
              {"accion_md": (
                  "**Raíces:** $r = 1, 2, 3$ (todas reales distintas, multiplicidad 1).\n\n"
                  "**Solución general:** $y(x) = c_1 e^x + c_2 e^{2x} + c_3 e^{3x}$."
              ),
               "justificacion_md": "Cada raíz simple aporta una sola exponencial.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Orden 4 — raíces reales con multiplicidad",
          problema_md="Resuelve $y^{(4)} - 2 y''' + y'' = 0$.",
          pasos=[
              {"accion_md": (
                  "**Ecuación característica:** $r^4 - 2 r^3 + r^2 = r^2 (r^2 - 2 r + 1) = r^2 (r - 1)^2 = 0$.\n\n"
                  "**Raíces:** $r = 0$ con multiplicidad $2$; $r = 1$ con multiplicidad $2$."
              ),
               "justificacion_md": "Factorizar primero $r^2$ y luego completar el cuadrado.",
               "es_resultado": False},
              {"accion_md": (
                  "**Soluciones aportadas:**\n\n"
                  "- Raíz $0$ con $m = 2$: $1$ y $x$ (notar que $e^{0 \\cdot x} = 1$).\n"
                  "- Raíz $1$ con $m = 2$: $e^x$ y $x e^x$.\n\n"
                  "**Solución general:**\n\n"
                  "$$y(x) = c_1 + c_2 x + c_3 e^x + c_4 x e^x.$$"
              ),
               "justificacion_md": "Cuatro soluciones LI para una EDO de orden 4: dimensión correcta.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Orden 4 — raíces complejas con multiplicidad",
          problema_md="Resuelve $y^{(4)} + 2 y'' + y = 0$.",
          pasos=[
              {"accion_md": (
                  "**Ecuación característica:** $r^4 + 2 r^2 + 1 = (r^2 + 1)^2 = 0$.\n\n"
                  "**Raíces:** $r^2 = -1 \\Rightarrow r = \\pm i$, **cada una con multiplicidad 2**.\n\n"
                  "Es decir, $\\alpha = 0$, $\\beta = 1$, $m = 2$."
              ),
               "justificacion_md": "Polinomio bicuadrático que factoriza como cuadrado perfecto.",
               "es_resultado": False},
              {"accion_md": (
                  "**Soluciones (por la regla, $2m = 4$ soluciones):**\n\n"
                  "- $\\cos x$, $\\sin x$ (multiplicidad 1).\n"
                  "- $x \\cos x$, $x \\sin x$ (factor extra $x$ por multiplicidad 2).\n\n"
                  "**Solución general:**\n\n"
                  "$$y(x) = (c_1 + c_2 x) \\cos x + (c_3 + c_4 x) \\sin x.$$"
              ),
               "justificacion_md": "Cuatro soluciones LI = orden 4. Aparecen en problemas de **resonancia** (forzar el oscilador a su frecuencia natural).",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**¿Por qué los factores $x^k$ con multiplicidad?** Si una raíz $r$ es solo simple, $e^{rx}$ es una "
            "única solución. Pero si $r$ es doble, ¿de dónde sacamos la segunda solución LI? La técnica clásica "
            "(reducción de orden, lección de Abel) muestra que multiplicar por $x$ produce una nueva solución "
            "que es independiente de $e^{rx}$. Para multiplicidad $m$, este proceso se itera dando "
            "$e^{rx}, x e^{rx}, x^2 e^{rx}, \\ldots, x^{m-1} e^{rx}$.\n\n"
            "**Conexión física.** Las raíces complejas en orden mayor con multiplicidad aparecen en sistemas "
            "**resonantes** — vibraciones forzadas justo en la frecuencia natural. La solución crece "
            "polinomialmente (los $x^k$) en lugar de ser puramente acotada — la **resonancia destructiva**."
        )),

        fig(
            "Cuadro-mapa de las raíces de la ecuación característica vs. la forma de las soluciones. "
            "Plano complejo en el centro con ejes Re y Im. Cuatro casos marcados con círculos: "
            "(1) raíz real simple en el eje real (etiqueta 'e^{rx}'), "
            "(2) raíz real doble (círculo más grande con '2' adentro, etiqueta 'e^{rx}, x e^{rx}'), "
            "(3) par complejo conjugado simple (dos círculos arriba y abajo del eje real, etiqueta 'e^{αx} cos βx, e^{αx} sin βx'), "
            "(4) par complejo conjugado doble (dos círculos grandes con '2' adentro, etiqueta 'multiplicar por 1, x'). "
            "Acentos teal para reales y ámbar para complejas. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La solución general de $y''' - 3 y' + 2 y = 0$, sabiendo que $r = 1$ es raíz doble y $r = -2$ es raíz simple, es:",
                  "opciones_md": [
                      "$c_1 e^x + c_2 e^{-2x}$",
                      "**$(c_1 + c_2 x) e^x + c_3 e^{-2x}$**",
                      "$c_1 e^x + c_2 e^{x} + c_3 e^{-2x}$",
                      "$(c_1 + c_2 + c_3 x) e^x \\cdot e^{-2x}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Multiplicidad 2 → factor extra $x$.",
                  "explicacion_md": "Raíz doble en $1$ aporta $e^x$ y $x e^x$; raíz simple en $-2$ aporta $e^{-2x}$.",
              },
              {
                  "enunciado_md": "Si la ecuación característica es $r^2 (r - 3)^3 = 0$, la solución general tiene cuántas constantes:",
                  "opciones_md": ["$2$", "$3$", "**$5$**", "$6$"],
                  "correcta": "C",
                  "pista_md": "Sumar las multiplicidades.",
                  "explicacion_md": "Multiplicidades $2 + 3 = 5$ → EDO de orden 5 → 5 constantes.",
              },
              {
                  "enunciado_md": "Si las raíces son $\\pm 2 i$ con multiplicidad 2, la solución general es:",
                  "opciones_md": [
                      "$c_1 \\cos 2x + c_2 \\sin 2x$",
                      "**$(c_1 + c_2 x) \\cos 2x + (c_3 + c_4 x) \\sin 2x$**",
                      "$c_1 e^{2x} + c_2 e^{-2x}$",
                      "$c_1 \\cos 2x + c_2 \\sin 2x + c_3 \\cos 2x + c_4 \\sin 2x$",
                  ],
                  "correcta": "B",
                  "pista_md": "Por cada multiplicidad extra, multiplicar por $x$.",
                  "explicacion_md": "Resonancia pura: oscilación con amplitud que crece linealmente en $x$.",
              },
          ]),

        ej(
            "Orden 4 con raíces reales y complejas",
            "Resuelve $y^{(4)} - y = 0$.",
            ["Factorizar $r^4 - 1 = (r^2 - 1)(r^2 + 1)$."],
            (
                "$r^4 - 1 = (r - 1)(r + 1)(r^2 + 1) = 0 \\Rightarrow r = 1, -1, \\pm i$.\n\n"
                "**Solución general:** $y(x) = c_1 e^x + c_2 e^{-x} + c_3 \\cos x + c_4 \\sin x$."
            ),
        ),

        ej(
            "PVI orden 3 con raíz triple",
            "Resuelve $y''' - 3 y'' + 3 y' - y = 0$ con $y(0) = 1$, $y'(0) = 2$, $y''(0) = 3$.",
            ["$(r - 1)^3 = 0$."],
            (
                "$(r - 1)^3 = 0 \\Rightarrow r = 1$ triple.\n\n"
                "$y = (c_1 + c_2 x + c_3 x^2) e^x$. Calculando $y'$ y $y''$ en $0$:\n\n"
                "$y(0) = c_1 = 1$. $y'(0) = c_1 + c_2 = 2 \\Rightarrow c_2 = 1$. $y''(0) = c_1 + 2 c_2 + 2 c_3 = 3 \\Rightarrow c_3 = 0$.\n\n"
                "**Solución:** $y(x) = (1 + x) e^x$."
            ),
        ),

        ej(
            "Mezcla de tipos",
            "Escribe la solución general si la ecuación característica factoriza como $(r - 2)(r + 1)^2 (r^2 + 4)(r^2 + 9)^2 = 0$.",
            ["Cada factor aporta lo correspondiente."],
            (
                "Raíces: $r = 2$ (simple), $r = -1$ (doble), $r = \\pm 2 i$ (simple), $r = \\pm 3 i$ (doble). Total $1 + 2 + 2 + 4 = 9$ → orden 9.\n\n"
                "**Solución general:**\n\n"
                "$y = c_1 e^{2x} + (c_2 + c_3 x) e^{-x} + c_4 \\cos 2x + c_5 \\sin 2x + (c_6 + c_7 x) \\cos 3x + (c_8 + c_9 x) \\sin 3x$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $x^k$ por multiplicidad.** Sin él, faltan soluciones LI y la 'solución general' está incompleta.",
              "**Tratar las raíces complejas con multiplicidad como si fueran simples.** Cada par conjugado de multiplicidad $m$ aporta $2m$ soluciones reales, no $2$.",
              "**Confundir el grado del polinomio con el orden de la EDO.** Coinciden, pero hay que llevar la EDO a la forma estándar antes de leer.",
              "**Mezclar coeficientes complejos al volver a real.** Las raíces vienen en pares conjugados; las soluciones reales se obtienen de $\\cos$ y $\\sin$, no de $e^{i\\beta x}$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Ecuación característica:** polinomio de grado $n$ con $n$ raíces complejas contadas con multiplicidad.",
              "**Raíz real $r$ de multiplicidad $m$:** aporta $e^{rx}, x e^{rx}, \\ldots, x^{m-1} e^{rx}$.",
              "**Par complejo $\\alpha \\pm i \\beta$ de multiplicidad $m$:** aporta $x^k e^{\\alpha x} \\cos(\\beta x)$ y $x^k e^{\\alpha x} \\sin(\\beta x)$ para $k = 0, \\ldots, m-1$.",
              "**Solución general:** suma de todas las contribuciones, con $n$ constantes arbitrarias.",
              "**Próxima lección:** la aplicación estrella — vibraciones mecánicas (libre amortiguado, forzado, resonancia).",
          ]),
    ]
    return {
        "id": "lec-ed-2-5-coef-const-orden-superior",
        "title": "Coeficientes constantes de orden superior",
        "description": "Ecuación característica de grado n: raíces reales con multiplicidad, raíces complejas con multiplicidad. Construcción sistemática de la solución general.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# Vibraciones mecánicas
# =====================================================================
def lesson_vibraciones():
    blocks = [
        b("texto", body_md=(
            "El sistema **masa-resorte-amortiguador** es la aplicación canónica de la EDO lineal de orden 2. "
            "Modela desde un auto sobre una suspensión hasta un edificio durante un terremoto, pasando por "
            "circuitos eléctricos, instrumentos musicales, suspensiones de bicicleta, sismógrafos y antenas. "
            "Toda esa fenomenología se reduce a estudiar:\n\n"
            "$$m\\, x''(t) + c\\, x'(t) + k\\, x(t) = F(t).$$\n\n"
            "donde $m > 0$ es la masa, $c \\geq 0$ el coeficiente de amortiguamiento, $k > 0$ la constante del "
            "resorte y $F(t)$ una fuerza externa.\n\n"
            "**Esta lección recorre los cuatro regímenes:**\n\n"
            "1. **Vibración libre no amortiguada** ($c = 0$, $F = 0$): MAS puro.\n"
            "2. **Vibración libre amortiguada** ($c > 0$, $F = 0$): tres subcasos según $c^2 - 4 m k$.\n"
            "3. **Vibración forzada amortiguada** ($c > 0$, $F \\neq 0$): respuesta transitoria + estacionaria.\n"
            "4. **Resonancia** ($c = 0$, $F$ a la frecuencia natural): amplitud crece sin cota.\n\n"
            "**Al terminar:**\n\n"
            "- Reconoces los tres tipos de amortiguamiento (sub, crítico, sobre) y dibujas sus gráficas.\n"
            "- Identificas la **frecuencia natural** $\\omega_0 = \\sqrt{k/m}$ y la **amortiguada** $\\omega_d$.\n"
            "- Distingues respuesta **transitoria** y **estacionaria** en el régimen forzado.\n"
            "- Explicas el fenómeno de **resonancia** y por qué es destructivo."
        )),

        b("definicion",
          titulo="Modelo masa-resorte-amortiguador",
          body_md=(
              "Una masa $m$ está unida a un resorte (constante $k$) y un amortiguador (coeficiente $c$). Sea "
              "$x(t)$ el desplazamiento desde el equilibrio. Por la segunda ley de Newton:\n\n"
              "- Fuerza del resorte: $F_r = -k x$ (Hooke).\n"
              "- Fuerza del amortiguador: $F_a = -c x'$ (proporcional a la velocidad, opuesta).\n"
              "- Fuerza externa: $F(t)$.\n\n"
              "$$m x'' = -k x - c x' + F(t) \\;\\Longrightarrow\\; \\boxed{m x'' + c x' + k x = F(t)}.$$\n\n"
              "En forma normalizada (dividiendo por $m$):\n\n"
              "$$x'' + 2 \\zeta \\omega_0 x' + \\omega_0^2 x = \\dfrac{F(t)}{m},$$\n\n"
              "donde $\\omega_0 = \\sqrt{k/m}$ es la **frecuencia natural** (rad/s) y $\\zeta = \\dfrac{c}{2\\sqrt{m k}}$ es el **factor de amortiguamiento adimensional**."
          )),

        formulas(
            titulo="Vibración libre no amortiguada (MAS)",
            body=(
                "Caso $c = 0$, $F = 0$:\n\n"
                "$$m x'' + k x = 0, \\quad \\omega_0 = \\sqrt{k/m}.$$\n\n"
                "**Solución general:**\n\n"
                "$$x(t) = c_1 \\cos(\\omega_0 t) + c_2 \\sin(\\omega_0 t) = A \\cos(\\omega_0 t - \\phi),$$\n\n"
                "con $A = \\sqrt{c_1^2 + c_2^2}$ (amplitud) y $\\tan \\phi = c_2 / c_1$ (fase).\n\n"
                "**Período:** $T = 2 \\pi / \\omega_0$. **Frecuencia:** $f = \\omega_0 / (2\\pi)$.\n\n"
                "Las oscilaciones son **perfectamente periódicas** y de **amplitud constante**."
            ),
        ),

        formulas(
            titulo="Vibración libre amortiguada — tres regímenes",
            body=(
                "Caso $c > 0$, $F = 0$. Ecuación característica de $m r^2 + c r + k = 0$:\n\n"
                "$$r = \\dfrac{-c \\pm \\sqrt{c^2 - 4 m k}}{2 m}.$$\n\n"
                "El **discriminante** $\\Delta = c^2 - 4 m k$ define tres regímenes:\n\n"
                "**Sobreamortiguado** ($\\Delta > 0$, $\\zeta > 1$): dos raíces reales negativas distintas.\n"
                "$$x(t) = c_1 e^{r_1 t} + c_2 e^{r_2 t}.$$\n"
                "El sistema vuelve al equilibrio **sin oscilar**, pero lentamente.\n\n"
                "**Críticamente amortiguado** ($\\Delta = 0$, $\\zeta = 1$): raíz doble $r = -c/(2m) < 0$.\n"
                "$$x(t) = (c_1 + c_2 t) e^{-c t / (2m)}.$$\n"
                "Vuelve al equilibrio **sin oscilar y lo más rápido posible** — caso ideal para amortiguadores de auto.\n\n"
                "**Subamortiguado** ($\\Delta < 0$, $0 < \\zeta < 1$): raíces complejas $r = -\\dfrac{c}{2m} \\pm i \\omega_d$, con\n"
                "$$\\omega_d = \\dfrac{\\sqrt{4 m k - c^2}}{2 m} = \\omega_0 \\sqrt{1 - \\zeta^2}$$\n"
                "(**frecuencia amortiguada**). Solución:\n"
                "$$x(t) = e^{-c t / (2m)}\\bigl(c_1 \\cos \\omega_d t + c_2 \\sin \\omega_d t\\bigr) = A e^{-c t / (2m)} \\cos(\\omega_d t - \\phi).$$\n"
                "**Oscila** con frecuencia $\\omega_d$ pero la amplitud decrece exponencialmente."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Subamortiguado",
          problema_md="Un sistema con $m = 1$, $c = 2$, $k = 5$ se libera desde $x(0) = 1$ con $x'(0) = 0$. Halla $x(t)$.",
          pasos=[
              {"accion_md": (
                  "**EDO:** $x'' + 2 x' + 5 x = 0$. Característica: $r^2 + 2 r + 5 = 0$, $\\Delta = 4 - 20 = -16$.\n\n"
                  "$r = -1 \\pm 2 i$. Subamortiguado con $\\omega_d = 2$."
              ),
               "justificacion_md": "$\\Delta < 0$ → oscilaciones amortiguadas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:** $x(t) = e^{-t}(c_1 \\cos 2 t + c_2 \\sin 2 t)$.\n\n"
                  "$x'(t) = -e^{-t}(c_1 \\cos 2 t + c_2 \\sin 2 t) + e^{-t}(-2 c_1 \\sin 2 t + 2 c_2 \\cos 2 t)$."
              ),
               "justificacion_md": "Producto regla con cuidado en los signos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar PVI:** $x(0) = c_1 = 1$. $x'(0) = -c_1 + 2 c_2 = 0 \\Rightarrow c_2 = 1/2$.\n\n"
                  "**Solución:** $x(t) = e^{-t}\\bigl(\\cos 2t + \\tfrac{1}{2} \\sin 2t\\bigr)$."
              ),
               "justificacion_md": "Oscila con período $\\pi$ y la envolvente $e^{-t}$ atenúa la amplitud.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Críticamente amortiguado",
          problema_md="$m = 1$, $c = 2$, $k = 1$, $x(0) = 1$, $x'(0) = 0$.",
          pasos=[
              {"accion_md": (
                  "**EDO:** $x'' + 2 x' + x = 0$. Característica: $(r + 1)^2 = 0$, $r = -1$ doble.\n\n"
                  "**Solución general:** $x(t) = (c_1 + c_2 t) e^{-t}$."
              ),
               "justificacion_md": "$\\Delta = 0$ → amortiguamiento crítico.",
               "es_resultado": False},
              {"accion_md": (
                  "$x'(t) = c_2 e^{-t} - (c_1 + c_2 t) e^{-t}$.\n\n"
                  "$x(0) = c_1 = 1$. $x'(0) = c_2 - c_1 = 0 \\Rightarrow c_2 = 1$.\n\n"
                  "**Solución:** $x(t) = (1 + t) e^{-t}$."
              ),
               "justificacion_md": "Sin oscilar, vuelve al equilibrio rápido y monotónicamente.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Vibración forzada — respuesta estacionaria",
            body=(
                "Con forzamiento sinusoidal $F(t) = F_0 \\cos(\\omega t)$:\n\n"
                "$$m x'' + c x' + k x = F_0 \\cos(\\omega t).$$\n\n"
                "Por superposición, la solución se descompone en\n\n"
                "$$x(t) = \\underbrace{x_h(t)}_{\\text{transitoria}} + \\underbrace{x_p(t)}_{\\text{estacionaria}}.$$\n\n"
                "**Transitoria** $x_h$: solución de la homogénea, decae a 0 (si $c > 0$).\n\n"
                "**Estacionaria** $x_p$: solución particular de la forma\n\n"
                "$$x_p(t) = A(\\omega) \\cos(\\omega t - \\delta(\\omega)),$$\n\n"
                "donde la **amplitud de respuesta** es\n\n"
                "$$A(\\omega) = \\dfrac{F_0}{\\sqrt{(k - m \\omega^2)^2 + (c \\omega)^2}}.$$\n\n"
                "Para $t$ grande, solo subsiste $x_p$: el sistema oscila a la **frecuencia del forzante**, no a su frecuencia natural."
            ),
        ),

        formulas(
            titulo="Resonancia",
            body=(
                "**Caso sin amortiguamiento** ($c = 0$): si $\\omega = \\omega_0$, la fórmula de $A(\\omega)$ "
                "**diverge** ($k - m \\omega_0^2 = 0$). El método de coeficientes indeterminados muestra que la "
                "solución particular tiene la forma\n\n"
                "$$x_p(t) = \\dfrac{F_0}{2 m \\omega_0}\\, t \\sin(\\omega_0 t),$$\n\n"
                "con amplitud que **crece linealmente** en $t$. Esto es **resonancia pura**.\n\n"
                "**Caso con amortiguamiento ligero** ($c$ pequeño): la amplitud no diverge pero alcanza un "
                "máximo cerca de\n\n"
                "$$\\omega_{\\text{res}} = \\omega_0 \\sqrt{1 - 2 \\zeta^2}.$$\n\n"
                "**Importancia práctica:** evitar que un sistema sea forzado a su frecuencia natural — caso "
                "clásico del puente de Tacoma Narrows (1940) y de soldados que rompen el paso al cruzar puentes."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Resonancia pura",
          problema_md="Sin amortiguamiento, $m = 1$, $k = 4$, forzante $F(t) = \\cos(2 t)$, $x(0) = 0$, $x'(0) = 0$.",
          pasos=[
              {"accion_md": (
                  "**EDO:** $x'' + 4 x = \\cos 2 t$. Frecuencia natural $\\omega_0 = 2$ = frecuencia del forzante. **Resonancia.**\n\n"
                  "Homogénea: $x_h = c_1 \\cos 2 t + c_2 \\sin 2 t$."
              ),
               "justificacion_md": "Detectar resonancia comparando $\\omega$ del forzante con $\\omega_0$ natural.",
               "es_resultado": False},
              {"accion_md": (
                  "**Particular** (proponer $x_p = t (A \\cos 2 t + B \\sin 2 t)$ por la regla de modificación):\n\n"
                  "Sustituyendo y agrupando, $A = 0$, $B = 1/4$. Es decir, $x_p = \\tfrac{t}{4} \\sin 2 t$."
              ),
               "justificacion_md": "Veremos el método de coeficientes indeterminados con detalle en la próxima lección.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:** $x(t) = c_1 \\cos 2 t + c_2 \\sin 2 t + \\tfrac{t}{4} \\sin 2 t$.\n\n"
                  "PVI: $x(0) = c_1 = 0$, $x'(0) = 2 c_2 + 0 = 0 \\Rightarrow c_2 = 0$.\n\n"
                  "**Solución:** $x(t) = \\dfrac{t}{4} \\sin 2 t$. La amplitud crece linealmente sin cota."
              ),
               "justificacion_md": "Sin disipación, el forzante a la frecuencia natural inyecta energía constantemente.",
               "es_resultado": True},
          ]),

        fig(
            "Cuadro de cuatro paneles 2x2 mostrando los tipos de respuesta del oscilador. "
            "Panel superior izquierdo: 'No amortiguado (MAS)' — onda cosenoidal pura color teal #06b6d4 con amplitud constante. "
            "Panel superior derecho: 'Subamortiguado' — onda cosenoidal con envolvente exponencial decreciente, color teal con líneas punteadas grises mostrando ±A e^{-ct/(2m)}. "
            "Panel inferior izquierdo: 'Críticamente amortiguado' — curva (1+t)e^{-t} sin cruces por cero, color ámbar #f59e0b. "
            "Panel inferior derecho: 'Sobreamortiguado' — combinación de dos exponenciales decrecientes, color ámbar más claro, sin oscilación. "
            "Cada panel con eje t horizontal, eje x vertical, cuadrícula tenue. " + STYLE
        ),

        fig(
            "Gráfico de resonancia: curva creciente de amplitud x(t) = (t/4) sin(2t) en color ámbar #f59e0b, t de 0 a 20. "
            "Las envolventes ±t/4 dibujadas como líneas punteadas grises. "
            "Título: 'Resonancia pura: x'' + 4x = cos(2t)'. Ejes etiquetados t y x. "
            "Anotación 'amplitud crece linealmente' con flecha hacia la curva. " + STYLE
        ),

        b("intuicion", body_md=(
            "**Por qué el amortiguamiento crítico es óptimo.** En un amortiguador de auto querés que después "
            "de pasar un bache la suspensión vuelva al equilibrio **rápido y sin rebotes**. Sub-amortiguado "
            "rebota; sobre-amortiguado vuelve lento; **crítico** es el punto justo. Por eso los amortiguadores "
            "se diseñan cerca de $\\zeta = 1$.\n\n"
            "**Por qué la resonancia es peligrosa.** Aún con amortiguamiento real, la amplitud cerca de "
            "$\\omega_0$ puede ser muchísimo mayor que la del forzante (factor $1 / (2\\zeta)$ en el pico). En "
            "estructuras (puentes, edificios) eso puede llevar a **falla por fatiga** o colapso. Los ingenieros "
            "diseñan para que las frecuencias de carga estén **lejos** de las frecuencias naturales."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El régimen de amortiguamiento del sistema $x'' + 4 x' + 4 x = 0$ es:",
                  "opciones_md": [
                      "Subamortiguado",
                      "**Críticamente amortiguado**",
                      "Sobreamortiguado",
                      "No amortiguado",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\Delta = 16 - 16 = 0$.",
                  "explicacion_md": "Discriminante cero → raíz doble → amortiguamiento crítico.",
              },
              {
                  "enunciado_md": "La frecuencia natural de un sistema masa-resorte con $m = 4$ y $k = 16$ es:",
                  "opciones_md": ["$\\omega_0 = 1$", "**$\\omega_0 = 2$**", "$\\omega_0 = 4$", "$\\omega_0 = 8$"],
                  "correcta": "B",
                  "pista_md": "$\\omega_0 = \\sqrt{k/m}$.",
                  "explicacion_md": "$\\sqrt{16/4} = 2$ rad/s.",
              },
              {
                  "enunciado_md": "En vibración forzada con amortiguamiento, la respuesta para $t$ grande es:",
                  "opciones_md": [
                      "Solo transitoria",
                      "**Solo estacionaria**",
                      "La suma a partes iguales",
                      "Cero",
                  ],
                  "correcta": "B",
                  "pista_md": "La transitoria decae exponencialmente.",
                  "explicacion_md": "$x_h \\to 0$, así $x \\to x_p$ para $t$ grande.",
              },
          ]),

        ej(
            "Identificar régimen",
            "Un sistema tiene $m = 2$ kg, $k = 8$ N/m. ¿Qué valor de $c$ produce amortiguamiento crítico?",
            ["Crítico cuando $c^2 = 4 m k$."],
            (
                "$c^2 = 4 \\cdot 2 \\cdot 8 = 64 \\Rightarrow c = 8$ N·s/m.\n\n"
                "Si $c < 8$: subamortiguado. Si $c > 8$: sobreamortiguado."
            ),
        ),

        ej(
            "Respuesta libre subamortiguada",
            "Resuelve $x'' + 2 x' + 10 x = 0$ con $x(0) = 0$, $x'(0) = 3$.",
            ["Raíces $-1 \\pm 3 i$."],
            (
                "$x(t) = e^{-t}(c_1 \\cos 3t + c_2 \\sin 3t)$. $x(0) = c_1 = 0$. $x'(0) = -c_1 + 3 c_2 = 3 \\Rightarrow c_2 = 1$.\n\n"
                "**Solución:** $x(t) = e^{-t} \\sin(3 t)$."
            ),
        ),

        ej(
            "Frecuencia amortiguada",
            "Para el sistema $x'' + 0{,}4 x' + 100 x = 0$, calcula $\\omega_0$, $\\zeta$ y $\\omega_d$.",
            ["$\\omega_0 = \\sqrt{k}$, $\\zeta = c / (2\\omega_0)$ con $m = 1$."],
            (
                "$\\omega_0 = 10$. $\\zeta = 0{,}4 / 20 = 0{,}02$ (muy levemente amortiguado). "
                "$\\omega_d = 10\\sqrt{1 - 0{,}0004} \\approx 9{,}998$.\n\n"
                "**La frecuencia amortiguada es prácticamente igual a la natural** — casi no se nota la diferencia con un MAS puro."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir frecuencia natural $\\omega_0$ con frecuencia amortiguada $\\omega_d$.** Solo coinciden si $c = 0$.",
              "**Olvidar que la transitoria decae** y dar la solución general como respuesta a 'qué pasa para $t$ grande'.",
              "**Detectar mal la resonancia.** Hay que comparar $\\omega$ del forzante con $\\omega_0 = \\sqrt{k/m}$, no con $\\omega_d$.",
              "**Pensar que sobreamortiguado vuelve al equilibrio más rápido que el crítico.** Es al revés: el crítico es el más rápido sin oscilar.",
              "**No usar la regla de modificación en resonancia.** Sin el factor $t$ extra, la propuesta para $x_p$ no funciona.",
          ]),

        b("resumen",
          puntos_md=[
              "**Ecuación general:** $m x'' + c x' + k x = F(t)$.",
              "**Frecuencia natural:** $\\omega_0 = \\sqrt{k/m}$. **Factor de amortiguamiento:** $\\zeta = c / (2\\sqrt{m k})$.",
              "**Libre no amortiguado:** MAS, oscilación pura $x = A \\cos(\\omega_0 t - \\phi)$.",
              "**Libre amortiguado:** sub ($\\zeta < 1$, oscila amortiguada), crítico ($\\zeta = 1$, vuelve rápido sin oscilar), sobre ($\\zeta > 1$, vuelve lento sin oscilar).",
              "**Forzado:** $x = x_h$ (transitoria) $+ x_p$ (estacionaria). Para $t$ grande domina $x_p$.",
              "**Resonancia:** forzar a $\\omega = \\omega_0$ con $c = 0$ produce amplitud creciente lineal en $t$.",
              "**Próxima lección:** método sistemático para encontrar $x_p$ — coeficientes indeterminados.",
          ]),
    ]
    return {
        "id": "lec-ed-2-6-vibraciones-mecanicas",
        "title": "Vibraciones mecánicas",
        "description": "Sistema masa-resorte-amortiguador: vibración libre no amortiguada, sub/crítico/sobreamortiguada, vibración forzada, transitoria vs estacionaria, resonancia.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 6,
    }


# =====================================================================
# Coeficientes indeterminados
# =====================================================================
def lesson_coef_indeterminados():
    blocks = [
        b("texto", body_md=(
            "Hasta acá sabemos resolver la **EDO homogénea** $L[y] = 0$ con coeficientes constantes. Toca "
            "el caso **no homogéneo**:\n\n"
            "$$y'' + p\\, y' + q\\, y = f(x), \\qquad f \\not\\equiv 0.$$\n\n"
            "**Estructura de la solución general** (consecuencia de linealidad):\n\n"
            "$$y(x) = y_h(x) + y_p(x),$$\n\n"
            "donde $y_h$ es la solución general de la homogénea (con sus dos constantes) e $y_p$ es **cualquier** "
            "solución particular de la no homogénea.\n\n"
            "El método de **coeficientes indeterminados** busca $y_p$ **adivinando** su forma a partir de "
            "$f(x)$, con coeficientes a determinar. Funciona cuando $f(x)$ es una combinación de **polinomios**, "
            "**exponenciales**, **senos/cosenos** y sus productos.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces la **tabla de propuestas** según la forma de $f(x)$.\n"
            "- Aplicas la **regla de modificación** (factor $x^s$) cuando hay resonancia con $y_h$.\n"
            "- Combinas el método con superposición cuando $f$ es suma de varios términos."
        )),

        b("definicion",
          titulo="Estructura $y = y_h + y_p$",
          body_md=(
              "**Teorema.** Sea $y_p$ **alguna** solución particular de\n\n"
              "$$L[y] := y'' + p y' + q y = f(x),$$\n\n"
              "y sea $y_h = c_1 y_1 + c_2 y_2$ la solución general de la homogénea $L[y] = 0$. Entonces toda "
              "solución de la no homogénea se escribe como\n\n"
              "$$y(x) = y_h(x) + y_p(x).$$\n\n"
              "**Demostración.** Si $y$ es solución de $L[y] = f$ y $y_p$ también, entonces $L[y - y_p] = "
              "L[y] - L[y_p] = f - f = 0$, así $y - y_p = c_1 y_1 + c_2 y_2$, de donde $y = y_h + y_p$.\n\n"
              "**Procedimiento de resolución:**\n\n"
              "1. Resolver la homogénea para obtener $y_h$.\n"
              "2. Encontrar **una** solución particular $y_p$.\n"
              "3. Escribir $y = y_h + y_p$.\n"
              "4. Si hay PVI, imponer las condiciones iniciales sobre la suma."
          )),

        formulas(
            titulo="Tabla de propuestas",
            body=(
                "Para cada forma de $f(x)$ se propone $y_p$ con coeficientes a determinar:\n\n"
                "| $f(x)$ | Propuesta $y_p$ |\n"
                "|---|---|\n"
                "| $P_n(x)$ (polinomio grado $n$) | $A_n x^n + A_{n-1} x^{n-1} + \\cdots + A_0$ |\n"
                "| $e^{\\alpha x}$ | $A e^{\\alpha x}$ |\n"
                "| $\\sin(\\beta x)$ o $\\cos(\\beta x)$ | $A \\cos\\beta x + B \\sin\\beta x$ |\n"
                "| $P_n(x) e^{\\alpha x}$ | $(A_n x^n + \\cdots + A_0) e^{\\alpha x}$ |\n"
                "| $e^{\\alpha x} \\cos\\beta x$ o $e^{\\alpha x} \\sin\\beta x$ | $e^{\\alpha x}(A \\cos\\beta x + B \\sin\\beta x)$ |\n"
                "| $P_n(x) e^{\\alpha x} \\cos\\beta x$ | $e^{\\alpha x}\\bigl[(A_n x^n + \\cdots) \\cos\\beta x + (B_n x^n + \\cdots) \\sin\\beta x\\bigr]$ |\n\n"
                "**Regla de modificación (resonancia).** Si algún término de la propuesta **coincide con una "
                "solución de la homogénea**, multiplicar la propuesta entera por $x^s$, con $s$ el menor entero "
                "$\\geq 1$ tal que ningún término de $y_p$ esté en $y_h$.\n\n"
                "**Linealidad (superposición).** Si $f = f_1 + f_2$, encontrar por separado $y_{p,1}$ para $f_1$ "
                "e $y_{p,2}$ para $f_2$ y sumar."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Polinomio sin resonancia",
          problema_md="Resuelve $y'' + 3 y' + 4 y = 3 x + 2$.",
          pasos=[
              {"accion_md": (
                  "**Homogénea:** $r^2 + 3 r + 4 = 0$, $\\Delta = 9 - 16 = -7$. $r = -3/2 \\pm i \\sqrt{7}/2$.\n\n"
                  "$y_h = e^{-3 x / 2}\\bigl(c_1 \\cos(\\tfrac{\\sqrt 7}{2} x) + c_2 \\sin(\\tfrac{\\sqrt 7}{2} x)\\bigr)$."
              ),
               "justificacion_md": "Primer paso siempre: resolver la homogénea.",
               "es_resultado": False},
              {"accion_md": (
                  "**Propuesta:** $f = 3x + 2$ es polinomio de grado 1. No hay polinomios en $y_h$, así $s = 0$.\n\n"
                  "$y_p = A x + B$. $y_p' = A$, $y_p'' = 0$."
              ),
               "justificacion_md": "Sin resonancia, propuesta directa de la tabla.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sustituir:** $0 + 3 A + 4(A x + B) = 3 x + 2$, es decir, $4 A\\, x + (3 A + 4 B) = 3 x + 2$.\n\n"
                  "Igualando coeficientes: $4 A = 3 \\Rightarrow A = 3/4$. $3 A + 4 B = 2 \\Rightarrow 4 B = 2 - 9/4 = -1/4 \\Rightarrow B = -1/16$.\n\n"
                  "$y_p = \\dfrac{3}{4} x - \\dfrac{1}{16}$."
              ),
               "justificacion_md": "Sistema lineal $2 \\times 2$ en los coeficientes indeterminados.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:**\n\n"
                  "$$y(x) = e^{-3 x / 2}\\Bigl(c_1 \\cos\\tfrac{\\sqrt 7}{2} x + c_2 \\sin\\tfrac{\\sqrt 7}{2} x\\Bigr) + \\dfrac{3}{4} x - \\dfrac{1}{16}.$$"
              ),
               "justificacion_md": "Suma de homogénea (con constantes) y particular.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Exponencial sin resonancia",
          problema_md="Resuelve $y'' - 4 y = 2 e^{3 x}$.",
          pasos=[
              {"accion_md": (
                  "**Homogénea:** $r^2 - 4 = 0 \\Rightarrow r = \\pm 2$. $y_h = c_1 e^{2 x} + c_2 e^{-2 x}$."
              ),
               "justificacion_md": "Caso 1.",
               "es_resultado": False},
              {"accion_md": (
                  "**Propuesta:** $f = 2 e^{3x}$, $\\alpha = 3$. **No** está en $y_h$ (que tiene $e^{\\pm 2 x}$). $s = 0$.\n\n"
                  "$y_p = A e^{3 x}$, $y_p' = 3 A e^{3 x}$, $y_p'' = 9 A e^{3 x}$."
              ),
               "justificacion_md": "Sin resonancia.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sustituir:** $9 A e^{3x} - 4 A e^{3x} = 2 e^{3x} \\Rightarrow 5 A = 2 \\Rightarrow A = 2/5$.\n\n"
                  "**Solución general:** $y(x) = c_1 e^{2 x} + c_2 e^{-2 x} + \\dfrac{2}{5} e^{3 x}$."
              ),
               "justificacion_md": "Coeficiente único; cierre directo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Exponencial CON resonancia (regla de modificación)",
          problema_md="Resuelve $y'' - 4 y = 2 e^{2 x}$.",
          pasos=[
              {"accion_md": (
                  "**Homogénea:** $y_h = c_1 e^{2 x} + c_2 e^{-2 x}$ (igual que antes).\n\n"
                  "**Detectar resonancia:** $f = 2 e^{2 x}$ con $\\alpha = 2$. **$e^{2 x}$ está en $y_h$.** Hay que multiplicar la propuesta por $x$."
              ),
               "justificacion_md": "Si propusiéramos $y_p = A e^{2x}$ obtendríamos $0 = 2 e^{2x}$, contradicción.",
               "es_resultado": False},
              {"accion_md": (
                  "**Propuesta modificada:** $y_p = A x e^{2 x}$. \n\n"
                  "$y_p' = A(1 + 2 x) e^{2 x}$, $y_p'' = A(4 + 4 x) e^{2 x}$."
              ),
               "justificacion_md": "$s = 1$ basta, ya que $A x e^{2x}$ no está en $y_h$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sustituir:** $A(4 + 4 x) e^{2 x} - 4 A x e^{2 x} = 2 e^{2 x}$, simplificando $4 A e^{2 x} = 2 e^{2 x} \\Rightarrow A = 1/2$.\n\n"
                  "**Solución general:** $y(x) = c_1 e^{2 x} + c_2 e^{-2 x} + \\dfrac{1}{2} x e^{2 x}$."
              ),
               "justificacion_md": "Los términos $4 A x e^{2 x}$ y $-4 A x e^{2 x}$ se cancelan exactamente — el factor $x$ es indispensable.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Forzante trigonométrico",
          problema_md="Resuelve $3 y'' + y' - 2 y = 2 \\cos x$.",
          pasos=[
              {"accion_md": (
                  "**Homogénea:** $3 r^2 + r - 2 = (3 r - 2)(r + 1) = 0 \\Rightarrow r = 2/3, -1$.\n\n"
                  "$y_h = c_1 e^{2 x / 3} + c_2 e^{-x}$. **No** contiene $\\cos x$ ni $\\sin x$."
              ),
               "justificacion_md": "Sin resonancia trigonométrica.",
               "es_resultado": False},
              {"accion_md": (
                  "**Propuesta:** $y_p = A \\cos x + B \\sin x$. Sustituir derivadas:\n\n"
                  "$y_p' = -A \\sin x + B \\cos x$, $y_p'' = -A \\cos x - B \\sin x$."
              ),
               "justificacion_md": "Hay que incluir **ambos** términos $\\cos$ y $\\sin$ aunque $f$ solo tenga $\\cos$, porque $y'$ los mezcla.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sustituir y agrupar.** Coef. de $\\cos x$: $-3 A + B - 2 A = -5 A + B = 2$. Coef. de $\\sin x$: $-3 B - A - 2 B = -A - 5 B = 0$.\n\n"
                  "De la segunda: $A = -5 B$. Sustituir: $-5(-5 B) + B = 26 B = 2 \\Rightarrow B = 1/13$, $A = -5/13$.\n\n"
                  "**Solución general:** $y(x) = c_1 e^{2 x / 3} + c_2 e^{-x} - \\dfrac{5}{13} \\cos x + \\dfrac{1}{13} \\sin x$."
              ),
               "justificacion_md": "Sistema $2 \\times 2$ en $A, B$ con solución única.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Superposición de varios términos (PVI)",
          problema_md="Resuelve $y'' - 3 y' + 2 y = 3 e^{-x} - 10 \\cos 3 x$ con $y(0) = 1$, $y'(0) = 2$.",
          pasos=[
              {"accion_md": (
                  "**Homogénea:** $r^2 - 3 r + 2 = (r - 1)(r - 2) = 0 \\Rightarrow r = 1, 2$.\n\n"
                  "$y_h = c_1 e^x + c_2 e^{2 x}$."
              ),
               "justificacion_md": "Sin resonancia con $e^{-x}$ ni con $\\cos 3 x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Propuesta:** $y_p = A e^{-x} + B \\cos 3 x + C \\sin 3 x$.\n\n"
                  "$y_p' = -A e^{-x} - 3 B \\sin 3 x + 3 C \\cos 3 x$.\n\n"
                  "$y_p'' = A e^{-x} - 9 B \\cos 3 x - 9 C \\sin 3 x$."
              ),
               "justificacion_md": "Combinar las propuestas individuales para cada sumando de $f$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Igualar coeficientes** (después de sustituir):\n\n"
                  "- $e^{-x}$: $A + 3 A + 2 A = 6 A = 3 \\Rightarrow A = 1/2$.\n"
                  "- $\\cos 3x$: $-9 B - 9 C + 2 B = -7 B - 9 C = -10$.\n"
                  "- $\\sin 3x$: $-9 C + 9 B + 2 C = 9 B - 7 C = 0$.\n\n"
                  "De la última: $B = 7 C / 9$. Sustituyendo: $-7 \\cdot 7 C / 9 - 9 C = -10 \\Rightarrow -(49 + 81) C / 9 = -10 \\Rightarrow C = 90/130 = 9/13$, $B = 7/13$.\n\n"
                  "$y_p = \\tfrac{1}{2} e^{-x} + \\tfrac{7}{13} \\cos 3 x + \\tfrac{9}{13} \\sin 3 x$."
              ),
               "justificacion_md": "Tres ecuaciones, tres incógnitas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Imponer PVI** sobre $y = y_h + y_p$:\n\n"
                  "$y(0) = c_1 + c_2 + 1/2 + 7/13 = 1 \\Rightarrow c_1 + c_2 = 1 - 1/2 - 7/13 = -1/26$.\n\n"
                  "$y'(0) = c_1 + 2 c_2 - 1/2 + 27/13 = 2 \\Rightarrow c_1 + 2 c_2 = 2 + 1/2 - 27/13 = 11/26$.\n\n"
                  "Restando: $c_2 = 12/26 = 6/13$, $c_1 = -1/26 - 6/13 = -13/26 = -1/2$.\n\n"
                  "**Solución del PVI:** $y(x) = -\\tfrac{1}{2} e^x + \\tfrac{6}{13} e^{2 x} + \\tfrac{1}{2} e^{-x} + \\tfrac{7}{13} \\cos 3 x + \\tfrac{9}{13} \\sin 3 x$."
              ),
               "justificacion_md": "Las constantes $c_1, c_2$ se imponen al final, sobre la suma completa.",
               "es_resultado": True},
          ]),

        fig(
            "Esquema visual de la estructura y = y_h + y_p. "
            "Tres curvas en un mismo gráfico: y_h en gris claro punteado (oscilación amortiguada), y_p en teal #06b6d4 (oscilación regular), "
            "y la suma y = y_h + y_p en ámbar #f59e0b (línea más gruesa). "
            "Ejes x y y. Anotaciones: 'transitoria' apuntando a y_h, 'estacionaria/forzada' apuntando a y_p, 'respuesta total' apuntando a y. "
            "Para t grande, y_h tiende a 0 y y se confunde con y_p — destacar este hecho con una flecha y nota. " + STYLE
        ),

        b("intuicion", body_md=(
            "**¿Por qué adivinar funciona?** Las funciones de la tabla (polinomios, exponenciales, "
            "$\\sin, \\cos$ y sus productos) tienen la propiedad de que **al derivarlas, se quedan dentro de la "
            "misma familia**. Eso significa que $L[y_p]$ tiene la misma forma que $y_p$, y podemos forzar la "
            "igualdad término a término.\n\n"
            "**Cuándo NO usar coeficientes indeterminados:** si $f$ no es una de esas formas (por ejemplo "
            "$f = \\tan x$, $f = 1/x$, $f = \\ln x$), hay que usar **variación de parámetros** (próxima lección)."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para $y'' - y = e^x$, la propuesta correcta de $y_p$ es:",
                  "opciones_md": [
                      "$A e^x$",
                      "**$A x e^x$**",
                      "$A x^2 e^x$",
                      "$A e^x + B$",
                  ],
                  "correcta": "B",
                  "pista_md": "$y_h = c_1 e^x + c_2 e^{-x}$: hay resonancia con $e^x$.",
                  "explicacion_md": "Multiplicar por $x$ una sola vez basta: $A x e^x$ no está en $y_h$.",
              },
              {
                  "enunciado_md": "Si $f(x) = \\sin x + e^{2x}$ y la homogénea no tiene resonancia, la propuesta es:",
                  "opciones_md": [
                      "$A \\sin x + B e^{2x}$",
                      "**$A \\cos x + B \\sin x + C e^{2x}$**",
                      "$A x \\sin x + B x e^{2x}$",
                      "$A e^x \\sin x$",
                  ],
                  "correcta": "B",
                  "pista_md": "Para forzante trigonométrico hay que incluir cos y sin.",
                  "explicacion_md": "Aunque $f$ solo tenga $\\sin x$, la derivada genera $\\cos x$.",
              },
              {
                  "enunciado_md": "La estructura general de la solución de una EDO no homogénea es:",
                  "opciones_md": [
                      "$y = y_p$",
                      "$y = y_h$",
                      "**$y = y_h + y_p$**",
                      "$y = y_h \\cdot y_p$",
                  ],
                  "correcta": "C",
                  "pista_md": "Linealidad.",
                  "explicacion_md": "Suma, no producto. La parte homogénea aporta las constantes para PVI.",
              },
          ]),

        ej(
            "Polinomio con resonancia",
            "Resuelve $y'' = 2 x + 3$.",
            ["$y_h = c_1 + c_2 x$. Notar la doble resonancia con polinomios de grado $\\leq 1$."],
            (
                "$y_h = c_1 + c_2 x$. Como propuestas $A$ y $A x$ están en $y_h$, multiplicar por $x^2$: "
                "$y_p = x^2 (A + B x) = A x^2 + B x^3$. $y_p'' = 2 A + 6 B x = 2 x + 3$ "
                "$\\Rightarrow 6 B = 2$, $2 A = 3$, así $A = 3/2$, $B = 1/3$.\n\n"
                "**Solución:** $y = c_1 + c_2 x + \\dfrac{3}{2} x^2 + \\dfrac{1}{3} x^3$."
            ),
        ),

        ej(
            "Producto polinomio-exponencial",
            "Resuelve $y'' - y' = x e^{x}$.",
            ["Resonancia con $e^x$ porque $y_h = c_1 + c_2 e^x$."],
            (
                "$y_h = c_1 + c_2 e^x$. Resonancia: el término constante $c_1$ corresponde a $r = 0$ y $c_2 e^x$ a $r = 1$. Como $f = x e^x$ involucra $r = 1$ (que está en $y_h$), multiplicar la propuesta por $x$:\n\n"
                "$y_p = x (A + B x) e^x = (A x + B x^2) e^x$.\n\n"
                "Calculando $y_p', y_p''$ y sustituyendo, se llega a $A = -1$, $B = 1/2$.\n\n"
                "**Solución:** $y = c_1 + c_2 e^x + (-x + \\tfrac{1}{2} x^2) e^x$."
            ),
        ),

        ej(
            "Polinomio + trigonométrico",
            "Resuelve $y'' + y = x^2 + \\sin x$.",
            ["Resonancia trigonométrica con $\\sin x$."],
            (
                "$y_h = c_1 \\cos x + c_2 \\sin x$.\n\n"
                "Para $x^2$ (sin resonancia): $y_{p1} = A x^2 + B x + C$. Sustituyendo en $y'' + y$: $2 A + A x^2 + B x + C = x^2 \\Rightarrow A = 1, B = 0, C = -2$.\n\n"
                "Para $\\sin x$ (CON resonancia): $y_{p2} = x(D \\cos x + E \\sin x)$. Sustituyendo: $-2 D \\sin x + 2 E \\cos x = \\sin x \\Rightarrow D = -1/2, E = 0$.\n\n"
                "**Solución:** $y = c_1 \\cos x + c_2 \\sin x + x^2 - 2 - \\tfrac{1}{2} x \\cos x$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $x^s$ en resonancia.** Lleva a contradicciones del tipo $0 = $ coef. no nulo.",
              "**Proponer solo $\\sin$ o solo $\\cos$ cuando $f$ tiene uno solo.** Hay que incluir ambos.",
              "**Resolver el PVI imponiendo condiciones sobre $y_h$ en vez de sobre $y = y_h + y_p$.** Las condiciones se aplican siempre sobre la solución completa.",
              "**Multiplicar por $x^s$ con $s$ insuficiente.** Si la raíz tiene multiplicidad $m$ en la característica y $f$ resuena, hay que usar $s = m$ (puede ser 2 o más).",
              "**Aplicar el método cuando $f$ es $\\tan x$, $\\sec x$, $1/x$.** No funciona; usar variación de parámetros.",
          ]),

        b("resumen",
          puntos_md=[
              "**Estructura:** $y = y_h + y_p$.",
              "**Tabla de propuestas:** según la forma de $f$ (polinomio, exp, sen/cos, productos).",
              "**Regla de modificación:** si la propuesta resuena con $y_h$, multiplicar por $x^s$ con $s$ mínimo.",
              "**Superposición:** si $f = f_1 + f_2$, sumar propuestas independientes.",
              "**Limitación:** solo aplica a $f$ en una clase específica de funciones.",
              "**Próxima lección:** método más general — variación de parámetros — que funciona para cualquier $f$ continua.",
          ]),
    ]
    return {
        "id": "lec-ed-2-7-coeficientes-indeterminados",
        "title": "Coeficientes indeterminados",
        "description": "Método de coeficientes indeterminados para EDO no homogénea con f en clase polinomio-exponencial-trigonométrica. Tabla de propuestas y regla de modificación.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 7,
    }


# =====================================================================
# Variación de parámetros
# =====================================================================
def lesson_variacion_parametros():
    blocks = [
        b("texto", body_md=(
            "El método de **coeficientes indeterminados** funciona solo cuando $f(x)$ es una combinación de "
            "polinomios, exponenciales y senos/cosenos. ¿Qué hacer cuando $f$ es algo más exótico, como $\\tan x$, "
            "$\\sec x$, $1/x$, $e^x / x$, $\\ln x$? La respuesta es **variación de parámetros**, un método "
            "**universal** que vale para cualquier $f(x)$ continua.\n\n"
            "**Idea.** Conocemos un conjunto fundamental $\\{y_1, y_2\\}$ de la homogénea. Buscamos una "
            "solución particular de la forma\n\n"
            "$$y_p(x) = u_1(x)\\, y_1(x) + u_2(x)\\, y_2(x),$$\n\n"
            "donde **$u_1, u_2$ son ahora funciones** de $x$ (de ahí el nombre 'variación de parámetros'). "
            "Imponiendo una condición auxiliar inteligente, el sistema para $u_1', u_2'$ se desacopla y se "
            "resuelve con álgebra simple.\n\n"
            "**Al terminar:**\n\n"
            "- Comprendes la deducción del método (sistema con condición auxiliar).\n"
            "- Aplicas la **fórmula explícita** con el wronskiano.\n"
            "- Resuelves EDOs no homogéneas con $f$ general.\n"
            "- Conoces la generalización a orden $n$."
        )),

        b("definicion",
          titulo="Idea y deducción",
          body_md=(
              "Consideremos la EDO en forma estándar\n\n"
              "$$y'' + p(x) y' + q(x) y = f(x),$$\n\n"
              "y sea $\\{y_1, y_2\\}$ un conjunto fundamental de la homogénea asociada. Proponemos\n\n"
              "$$y_p = u_1 y_1 + u_2 y_2.$$\n\n"
              "Calculando $y_p'$ aparece un término $u_1' y_1 + u_2' y_2$ que complicaría todo. **Imponemos "
              "la condición auxiliar:**\n\n"
              "$$u_1' y_1 + u_2' y_2 = 0. \\qquad (\\star)$$\n\n"
              "Con $(\\star)$, $y_p' = u_1 y_1' + u_2 y_2'$ y $y_p'' = u_1' y_1' + u_1 y_1'' + u_2' y_2' + u_2 y_2''$. "
              "Sustituyendo en la EDO y usando que $y_i'' + p y_i' + q y_i = 0$:\n\n"
              "$$u_1' y_1' + u_2' y_2' = f(x). \\qquad (\\star\\star)$$\n\n"
              "Las dos condiciones $(\\star)$ y $(\\star\\star)$ forman el **sistema de variación de parámetros**:\n\n"
              "$$\\begin{cases} y_1\\, u_1' + y_2\\, u_2' = 0 \\\\ y_1'\\, u_1' + y_2'\\, u_2' = f(x) \\end{cases}$$\n\n"
              "cuya matriz de coeficientes es justamente la traspuesta de la wronskiana — y por tanto **invertible** "
              "siempre que $W(y_1, y_2) \\neq 0$, lo cual ocurre por ser conjunto fundamental."
          )),

        formulas(
            titulo="Fórmula explícita (orden 2)",
            body=(
                "Resolviendo el sistema por Cramer:\n\n"
                "$$u_1'(x) = -\\dfrac{y_2(x)\\, f(x)}{W(y_1, y_2)(x)}, \\qquad u_2'(x) = \\dfrac{y_1(x)\\, f(x)}{W(y_1, y_2)(x)}.$$\n\n"
                "Integrando (sin constantes — ya las aporta $y_h$):\n\n"
                "$$u_1(x) = -\\int \\dfrac{y_2(x)\\, f(x)}{W(y_1, y_2)(x)}\\, dx, \\qquad u_2(x) = \\int \\dfrac{y_1(x)\\, f(x)}{W(y_1, y_2)(x)}\\, dx.$$\n\n"
                "**Solución particular:**\n\n"
                "$$\\boxed{\\,y_p(x) = u_1(x)\\, y_1(x) + u_2(x)\\, y_2(x).\\,}$$\n\n"
                "**Importante:** la EDO debe estar en **forma estándar** $y'' + p y' + q y = f$ (coeficiente 1 "
                "en $y''$). De lo contrario hay que normalizar primero — el $f$ en la fórmula es el del lado "
                "derecho **después** de dividir por el coeficiente líder."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="$y'' + y = \\sec x$",
          problema_md="Resuelve $y'' + y = \\sec x$ en $-\\pi/2 < x < \\pi/2$.",
          pasos=[
              {"accion_md": (
                  "**Homogénea:** $r^2 + 1 = 0 \\Rightarrow r = \\pm i$. $y_1 = \\cos x$, $y_2 = \\sin x$.\n\n"
                  "**Wronskiano:** $W = \\cos x \\cdot \\cos x - (-\\sin x) \\sin x = \\cos^2 x + \\sin^2 x = 1$."
              ),
               "justificacion_md": "Wronskiano constante (porque $p = 0$ en la EDO).",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular $u_1', u_2'$:**\n\n"
                  "$u_1' = -\\dfrac{\\sin x \\cdot \\sec x}{1} = -\\dfrac{\\sin x}{\\cos x} = -\\tan x$.\n\n"
                  "$u_2' = \\dfrac{\\cos x \\cdot \\sec x}{1} = 1$."
              ),
               "justificacion_md": "Aplicar fórmula directa.",
               "es_resultado": False},
              {"accion_md": (
                  "**Integrar:** $u_1 = -\\int \\tan x\\, dx = \\ln|\\cos x|$. $u_2 = \\int 1\\, dx = x$."
              ),
               "justificacion_md": "Sin constantes (ya están en $y_h$).",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución particular:** $y_p = \\cos x \\ln|\\cos x| + x \\sin x$.\n\n"
                  "**Solución general:**\n\n"
                  "$$y(x) = c_1 \\cos x + c_2 \\sin x + \\cos x \\ln|\\cos x| + x \\sin x.$$"
              ),
               "justificacion_md": "Coeficientes indeterminados no podía con $\\sec x$ — variación de parámetros sí.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="$y'' + y = \\tan x$",
          problema_md="Resuelve $y'' + y = \\tan x$ en $-\\pi/2 < x < \\pi/2$.",
          pasos=[
              {"accion_md": (
                  "**Misma homogénea:** $y_1 = \\cos x$, $y_2 = \\sin x$, $W = 1$.\n\n"
                  "$u_1' = -\\sin x \\tan x = -\\dfrac{\\sin^2 x}{\\cos x} = -\\dfrac{1 - \\cos^2 x}{\\cos x} = -\\sec x + \\cos x$."
              ),
               "justificacion_md": "Reescribir $\\sin^2$ con identidad pitagórica.",
               "es_resultado": False},
              {"accion_md": (
                  "**Integrar $u_1$:** $u_1 = -\\ln|\\sec x + \\tan x| + \\sin x$."
              ),
               "justificacion_md": "Antiderivada estándar de $\\sec x$.",
               "es_resultado": False},
              {"accion_md": (
                  "$u_2' = \\cos x \\tan x = \\sin x \\Rightarrow u_2 = -\\cos x$."
              ),
               "justificacion_md": "Cálculo directo.",
               "es_resultado": False},
              {"accion_md": (
                  "**$y_p = u_1 \\cos x + u_2 \\sin x = -\\cos x \\ln|\\sec x + \\tan x| + \\sin x \\cos x - \\cos x \\sin x = -\\cos x \\ln|\\sec x + \\tan x|$.**\n\n"
                  "**Solución general:** $y = c_1 \\cos x + c_2 \\sin x - \\cos x \\ln|\\sec x + \\tan x|$."
              ),
               "justificacion_md": "Los términos $\\sin x \\cos x$ se cancelan.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Resonancia generalizada: $y'' - 2 y' + y = e^x / x$",
          problema_md="Resuelve $y'' - 2 y' + y = \\dfrac{e^x}{x}$ en $x > 0$.",
          pasos=[
              {"accion_md": (
                  "**Homogénea:** $(r - 1)^2 = 0 \\Rightarrow r = 1$ doble. $y_1 = e^x$, $y_2 = x e^x$.\n\n"
                  "**Wronskiano:** $W = e^x (e^x + x e^x) - e^x \\cdot x e^x = e^{2 x}$."
              ),
               "justificacion_md": "Coeficientes indeterminados no aplica acá: $f = e^x / x$ no es una clase válida.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular $u_1', u_2'$:**\n\n"
                  "$u_1' = -\\dfrac{x e^x \\cdot (e^x / x)}{e^{2 x}} = -1$.\n\n"
                  "$u_2' = \\dfrac{e^x \\cdot (e^x / x)}{e^{2 x}} = \\dfrac{1}{x}$."
              ),
               "justificacion_md": "Notar la simplificación de las exponenciales.",
               "es_resultado": False},
              {"accion_md": (
                  "**Integrar:** $u_1 = -x$, $u_2 = \\ln x$ (en $x > 0$).\n\n"
                  "**$y_p = -x \\cdot e^x + \\ln x \\cdot x e^x = e^x (x \\ln x - x)$.**"
              ),
               "justificacion_md": "Sale una solución particular exótica que combina exponencial y logaritmo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:** $y(x) = (c_1 + c_2 x) e^x + e^x (x \\ln x - x)$."
              ),
               "justificacion_md": "El término $-x e^x$ podría absorberse en $c_2 x e^x$ redefiniendo $c_2$, pero dejarlo explícito mejora la legibilidad.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Generalización a orden n",
            body=(
                "Para la EDO lineal de orden $n$ en forma estándar\n\n"
                "$$y^{(n)} + p_{n-1}(x) y^{(n-1)} + \\cdots + p_0(x) y = f(x),$$\n\n"
                "con $\\{y_1, \\ldots, y_n\\}$ conjunto fundamental, proponemos\n\n"
                "$$y_p = u_1 y_1 + u_2 y_2 + \\cdots + u_n y_n,$$\n\n"
                "imponemos $n - 1$ **condiciones auxiliares** (todas las derivadas mixtas hasta orden $n - 1$ "
                "son nulas) y obtenemos el sistema\n\n"
                "$$\\begin{pmatrix} y_1 & y_2 & \\cdots & y_n \\\\ y_1' & y_2' & \\cdots & y_n' \\\\ \\vdots & \\vdots & \\ddots & \\vdots \\\\ y_1^{(n-1)} & y_2^{(n-1)} & \\cdots & y_n^{(n-1)} \\end{pmatrix} \\begin{pmatrix} u_1' \\\\ u_2' \\\\ \\vdots \\\\ u_n' \\end{pmatrix} = \\begin{pmatrix} 0 \\\\ 0 \\\\ \\vdots \\\\ f(x) \\end{pmatrix}.$$\n\n"
                "La matriz es la **wronskiana** y es invertible porque $\\{y_i\\}$ es conjunto fundamental. Por "
                "Cramer,\n\n"
                "$$u_k'(x) = \\dfrac{W_k(x)}{W(y_1, \\ldots, y_n)(x)}\\, f(x),$$\n\n"
                "donde $W_k$ es el determinante que se obtiene de $W$ reemplazando la columna $k$ por "
                "$(0, 0, \\ldots, 0, 1)^T$. Integrando se obtienen $u_k$ y luego $y_p$."
            ),
        ),

        b("intuicion", body_md=(
            "**Por qué la condición auxiliar.** Tener dos funciones $u_1, u_2$ desconocidas para satisfacer una "
            "única ecuación diferencial deja un grado de libertad — podemos imponer una condición extra **a "
            "nuestra elección**. Tomar $u_1' y_1 + u_2' y_2 = 0$ logra que la fórmula final no involucre "
            "$u_1''$ ni $u_2''$ — solo $u_1', u_2'$. Es un truco de simplificación elegante.\n\n"
            "**Coeficientes indeterminados vs. variación de parámetros.** Cuando ambos aplican, "
            "**coeficientes indeterminados es más rápido** (sistema lineal pequeño, sin integrales). Cuando $f$ "
            "no entra en la tabla, **variación de parámetros es la única opción** — pero el costo son las "
            "integrales, que pueden ser difíciles."
        )),

        fig(
            "Diagrama comparativo coeficientes indeterminados vs. variación de parámetros. "
            "Dos cajas grandes lado a lado. Caja izquierda 'Coeficientes Indeterminados' en teal #06b6d4: "
            "lista de viñetas — '+ rápido', '+ no requiere integrar', '- f debe estar en la tabla', '- regla de modificación'. "
            "Caja derecha 'Variación de Parámetros' en ámbar #f59e0b: 'Funciona para cualquier f continua', "
            "'Requiere conjunto fundamental', '- integrales pueden ser difíciles'. "
            "Flecha entre ambos con texto 'usar primero el de la izquierda; si no aplica, ir al de la derecha'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Variación de parámetros propone $y_p$ de la forma:",
                  "opciones_md": [
                      "$A y_1 + B y_2$ con $A, B$ constantes",
                      "**$u_1(x) y_1(x) + u_2(x) y_2(x)$ con $u_1, u_2$ funciones**",
                      "$y_1 + y_2$",
                      "$f(x) / W(y_1, y_2)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Por eso 'variación de parámetros'.",
                  "explicacion_md": "Las constantes de la solución homogénea se 'liberan' a funciones a determinar.",
              },
              {
                  "enunciado_md": "En la fórmula de $u_1'$, el denominador es:",
                  "opciones_md": [
                      "$y_1 y_2$",
                      "$y_1 + y_2$",
                      "**$W(y_1, y_2)$**",
                      "$f(x)$",
                  ],
                  "correcta": "C",
                  "pista_md": "Determinante del sistema $2 \\times 2$.",
                  "explicacion_md": "Cramer: el denominador es el wronskiano.",
              },
              {
                  "enunciado_md": "Antes de aplicar la fórmula de variación de parámetros, hay que:",
                  "opciones_md": [
                      "Calcular el discriminante",
                      "Hallar las condiciones iniciales",
                      "**Llevar la EDO a forma estándar (coeficiente 1 en $y''$)**",
                      "Verificar que $f$ es continua en todo $\\mathbb{R}$",
                  ],
                  "correcta": "C",
                  "pista_md": "Si el coeficiente líder no es 1, $f$ no es el de la fórmula.",
                  "explicacion_md": "Normalizar dividiendo por $a_2(x)$ es paso obligatorio.",
              },
          ]),

        ej(
            "Variación con homogénea reales distintas",
            "Resuelve $y'' - y = \\dfrac{2}{1 + e^x}$.",
            ["$y_1 = e^x$, $y_2 = e^{-x}$, $W = -2$. Integrales con sustitución $u = e^x$."],
            (
                "$u_1' = -\\dfrac{e^{-x} \\cdot 2/(1 + e^x)}{-2} = \\dfrac{e^{-x}}{1 + e^x}$. "
                "Sustitución $u = e^x$: $u_1 = -\\ln(1 + e^{-x}) - x$ (tras simplificación, salvo constante).\n\n"
                "$u_2' = \\dfrac{e^x \\cdot 2/(1 + e^x)}{-2} = -\\dfrac{e^x}{1 + e^x}$, $u_2 = -\\ln(1 + e^x)$.\n\n"
                "$y_p = u_1 e^x + u_2 e^{-x}$ (combinar y simplificar).\n\n"
                "**Solución general:** $y = c_1 e^x + c_2 e^{-x} + y_p$ con $y_p$ dado por la combinación anterior."
            ),
        ),

        ej(
            "Logaritmo en el forzante",
            "Resuelve $y'' + y = \\dfrac{1}{\\sin x}$ en $0 < x < \\pi$.",
            ["$y_1 = \\cos x$, $y_2 = \\sin x$, $W = 1$. Integrales con $\\cot$ y $\\csc$."],
            (
                "$u_1' = -\\dfrac{\\sin x \\cdot 1/\\sin x}{1} = -1 \\Rightarrow u_1 = -x$.\n\n"
                "$u_2' = \\dfrac{\\cos x / \\sin x}{1} = \\cot x \\Rightarrow u_2 = \\ln|\\sin x|$.\n\n"
                "$y_p = -x \\cos x + \\sin x \\ln|\\sin x|$.\n\n"
                "**Solución general:** $y = c_1 \\cos x + c_2 \\sin x - x \\cos x + \\sin x \\ln|\\sin x|$."
            ),
        ),

        ej(
            "Variación con raíz doble",
            "Resuelve $y'' - 2 y' + y = \\dfrac{e^x}{x^2}$ en $x > 0$.",
            ["$y_1 = e^x$, $y_2 = x e^x$, $W = e^{2x}$."],
            (
                "$u_1' = -\\dfrac{x e^x \\cdot e^x / x^2}{e^{2 x}} = -\\dfrac{1}{x} \\Rightarrow u_1 = -\\ln x$.\n\n"
                "$u_2' = \\dfrac{e^x \\cdot e^x / x^2}{e^{2 x}} = \\dfrac{1}{x^2} \\Rightarrow u_2 = -\\dfrac{1}{x}$.\n\n"
                "$y_p = -e^x \\ln x - e^x = -e^x (\\ln x + 1)$.\n\n"
                "**Solución general:** $y = (c_1 + c_2 x) e^x - e^x (\\ln x + 1)$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar normalizar la EDO antes de aplicar la fórmula.** $f$ es el lado derecho **después** de dividir por el coeficiente de $y''$.",
              "**Agregar constantes al integrar $u_1, u_2$.** Esas constantes ya están en $y_h$ — incluirlas duplica.",
              "**Confundir el signo en $u_1'$.** Es $u_1' = -y_2 f / W$, con menos.",
              "**Aplicar variación de parámetros sin tener un conjunto fundamental.** Hay que resolver primero la homogénea.",
              "**Usar variación cuando coeficientes indeterminados aplica.** Es válido pero más caro — preferir el método más simple cuando funcione.",
          ]),

        b("resumen",
          puntos_md=[
              "**Idea:** $y_p = u_1 y_1 + u_2 y_2$ con $u_1, u_2$ funciones a determinar.",
              "**Sistema:** $\\begin{cases} y_1 u_1' + y_2 u_2' = 0 \\\\ y_1' u_1' + y_2' u_2' = f \\end{cases}$.",
              "**Fórmulas:** $u_1' = -y_2 f / W$, $u_2' = y_1 f / W$. Integrar y formar $y_p = u_1 y_1 + u_2 y_2$.",
              "**Universalidad:** funciona para cualquier $f$ continua, no solo polinomios/exp/sen/cos.",
              "**Generalización a orden $n$:** sistema $n \\times n$ con la wronskiana y Cramer.",
              "**Próxima lección:** identidad de Abel para el wronskiano y reducción de orden.",
          ]),
    ]
    return {
        "id": "lec-ed-2-8-variacion-de-parametros",
        "title": "Variación de parámetros",
        "description": "Método universal de variación de parámetros para resolver EDO no homogénea. Sistema 2x2 con condición auxiliar, fórmula con wronskiano y generalización a orden n.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 8,
    }


# =====================================================================
# Fórmula de Abel
# =====================================================================
def lesson_abel():
    blocks = [
        b("texto", body_md=(
            "Cerramos el capítulo con dos resultados clásicos de gran utilidad teórica y práctica:\n\n"
            "1. La **identidad de Abel**, que da una fórmula explícita para el wronskiano de dos soluciones de "
            "una EDO lineal de orden 2 — sin necesidad de conocer las soluciones.\n"
            "2. El método de **reducción de orden**, que permite encontrar una segunda solución LI a partir de "
            "una solución conocida.\n\n"
            "Ambos resultados son útiles cuando los coeficientes son **variables** y no podemos usar la "
            "ecuación característica. Aplicaciones típicas: ecuación de Legendre, Bessel, Cauchy-Euler.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces la **identidad de Abel** y la usas para calcular el wronskiano sin resolver la EDO.\n"
            "- Aplicas la fórmula de **reducción de orden** para encontrar $y_2$ a partir de $y_1$.\n"
            "- Resuelves EDOs lineales de coeficientes variables cuando una solución es 'visible'."
        )),

        b("definicion",
          titulo="Identidad de Abel",
          body_md=(
              "**Teorema (Abel).** Sea $y_1, y_2$ dos soluciones de\n\n"
              "$$y'' + p(x) y' + q(x) y = 0$$\n\n"
              "en un intervalo $I$ donde $p$ es continua. Entonces el wronskiano $W(x) = W(y_1, y_2)(x)$ "
              "satisface\n\n"
              "$$W'(x) = -p(x)\\, W(x),$$\n\n"
              "y por lo tanto\n\n"
              "$$\\boxed{\\,W(x) = W(x_0)\\, \\exp\\!\\left(-\\int_{x_0}^x p(s)\\, ds\\right).\\,}$$\n\n"
              "**Demostración (idea).** Diferenciando $W = y_1 y_2' - y_1' y_2$ y usando que cada $y_i$ "
              "satisface la EDO, los términos con $q$ se cancelan y queda $W' = -p W$. Es una EDO lineal de "
              "primer orden en $W$ — la integramos con factor integrante.\n\n"
              "**Tres consecuencias inmediatas:**\n\n"
              "1. **El wronskiano queda determinado salvo una constante** por $p(x)$ — no depende de cuánto cueste resolver la EDO.\n"
              "2. **O $W \\equiv 0$ o $W$ no se anula nunca:** la exponencial es siempre positiva, así que $W(x_0) = 0$ implica $W \\equiv 0$.\n"
              "3. Si $p \\equiv 0$, entonces $W$ es **constante**."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular el wronskiano sin resolver la EDO",
          problema_md=(
              "Sin encontrar las soluciones explícitas, halla la forma del wronskiano de dos soluciones de\n\n"
              "$$y'' + 2 x y' + (\\sin x) y = 0.$$"
          ),
          pasos=[
              {"accion_md": (
                  "**Identificar $p(x) = 2 x$.**\n\n"
                  "Por la identidad de Abel:\n\n"
                  "$$W(x) = W(0) \\exp\\!\\left(-\\int_0^x 2 s\\, ds\\right) = W(0)\\, e^{-x^2}.$$"
              ),
               "justificacion_md": "Solo necesitamos $p$ — los detalles de $q$ son irrelevantes para esto.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión.** El wronskiano de cualquier par de soluciones es de la forma $C e^{-x^2}$, con "
                  "$C$ constante (que depende del par elegido). Si $C \\neq 0$, son LI; si $C = 0$, LD."
              ),
               "justificacion_md": "Ojo: $C \\neq 0$ aquí depende del par específico.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Reducción de orden",
            body=(
                "**Problema.** Conocemos $y_1(x)$ solución de\n\n"
                "$$y'' + p(x) y' + q(x) y = 0$$\n\n"
                "y queremos encontrar una segunda solución $y_2$ LI con $y_1$.\n\n"
                "**Idea.** Probar $y_2 = v(x)\\, y_1(x)$ con $v$ a determinar. Sustituyendo en la EDO y usando "
                "que $y_1$ es solución, se llega a una EDO de primer orden en $v'$ que se resuelve por separación "
                "(o factor integrante). El resultado final es la **fórmula de reducción de orden**:\n\n"
                "$$\\boxed{\\,y_2(x) = y_1(x) \\int \\dfrac{e^{-\\int p(x)\\, dx}}{y_1(x)^2}\\, dx.\\,}$$\n\n"
                "**Conexión con Abel.** El integrando $e^{-\\int p\\, dx}/y_1^2$ es exactamente $W/y_1^2$, "
                "porque por Abel $W = C e^{-\\int p\\, dx}$ (eligiendo $C = 1$). Así $y_2/y_1 = \\int W/y_1^2 \\, dx$.\n\n"
                "**Verificación de independencia.** $W(y_1, y_2) = e^{-\\int p\\, dx} \\neq 0$, así $\\{y_1, y_2\\}$ es conjunto fundamental."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Reducción de orden — Cauchy-Euler",
          problema_md=(
              "Sabiendo que $y_1 = x$ es solución de $x^2 y'' - 2 x y' + 2 y = 0$ en $x > 0$, halla la solución general."
          ),
          pasos=[
              {"accion_md": (
                  "**Normalizar:** dividir por $x^2$ → $y'' - \\dfrac{2}{x} y' + \\dfrac{2}{x^2} y = 0$.\n\n"
                  "Identificamos $p(x) = -2/x$, $q(x) = 2/x^2$."
              ),
               "justificacion_md": "La fórmula requiere forma estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular $\\int p\\, dx = -2 \\ln x$**, así $e^{-\\int p\\, dx} = e^{2 \\ln x} = x^2$.\n\n"
                  "**Aplicar la fórmula:**\n\n"
                  "$$y_2 = x \\int \\dfrac{x^2}{x^2}\\, dx = x \\int 1\\, dx = x \\cdot x = x^2.$$"
              ),
               "justificacion_md": "Sale exactamente $y_2 = x^2$, otra solución LI con $y_1 = x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificar.** $y_2'' = 2$, así $x^2 \\cdot 2 - 2 x \\cdot 2 x + 2 \\cdot x^2 = 2 x^2 - 4 x^2 + 2 x^2 = 0$. ✓\n\n"
                  "**Solución general:** $y(x) = c_1 x + c_2 x^2$."
              ),
               "justificacion_md": "Wronskiano $W = x \\cdot 2 x - 1 \\cdot x^2 = x^2 \\neq 0$ en $x > 0$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Reducción de orden con $y_1 = e^x$",
          problema_md=(
              "Sabiendo que $y_1 = e^x$ es solución de $(x - 1) y'' - x y' + y = 0$ en $x > 1$, halla $y_2$."
          ),
          pasos=[
              {"accion_md": (
                  "**Normalizar:** $y'' - \\dfrac{x}{x - 1} y' + \\dfrac{1}{x - 1} y = 0$. $p(x) = -\\dfrac{x}{x - 1}$.\n\n"
                  "**Calcular $-\\int p\\, dx = \\int \\dfrac{x}{x - 1}\\, dx$.** Reescribir: $\\dfrac{x}{x - 1} = 1 + \\dfrac{1}{x - 1}$, así $\\int = x + \\ln(x - 1)$."
              ),
               "justificacion_md": "Truco habitual: descomponer fracción para integrar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar la fórmula:**\n\n"
                  "$$y_2 = e^x \\int \\dfrac{e^{x + \\ln(x - 1)}}{e^{2 x}}\\, dx = e^x \\int (x - 1) e^{-x}\\, dx.$$\n\n"
                  "Por partes ($u = x - 1$, $dv = e^{-x} dx$): $\\int (x - 1) e^{-x} dx = -(x - 1) e^{-x} - e^{-x} = -x e^{-x}$.\n\n"
                  "$$y_2 = e^x \\cdot (-x e^{-x}) = -x.$$"
              ),
               "justificacion_md": "Salvo signo, $y_2 = x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:** $y(x) = c_1 e^x + c_2 x$."
              ),
               "justificacion_md": "El signo absorbe en $c_2$.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué Abel es 'mágico'.** En general resolver una EDO lineal de orden 2 con coeficientes "
            "variables es difícil — no hay método universal. Pero si conocemos **una sola solución**, Abel "
            "(vía reducción de orden) nos da la **otra gratis**, sin resolver una EDO de orden 2 más.\n\n"
            "**De dónde sacar $y_1$.** A veces $y_1$ aparece por inspección (como $x$ en Cauchy-Euler, o $e^x$ "
            "en algunos casos). Otras veces se postula del tipo correcto (por ejemplo, $x^r$ en Cauchy-Euler "
            "lleva a una ecuación característica).\n\n"
            "**Ecuaciones famosas donde se usa.** Legendre, Bessel, Hermite, Laguerre, Chebyshev — todas "
            "ecuaciones especiales donde una solución se conoce (vía series) y la otra se obtiene por reducción."
        )),

        fig(
            "Diagrama conceptual de la identidad de Abel y reducción de orden. "
            "A la izquierda, una caja con la EDO 'y'' + p(x) y' + q(x) y = 0' en color teal #06b6d4. "
            "Una flecha hacia abajo etiquetada 'Abel' lleva a 'W(x) = W(x_0) e^{-∫p dx}'. "
            "A la derecha, una caja con 'y_1 conocida' y una flecha etiquetada 'reducción de orden' que lleva a 'y_2 = y_1 ∫ (e^{-∫p}/y_1^2) dx'. "
            "Una llave abajo conecta y_1 e y_2 a 'solución general y = c_1 y_1 + c_2 y_2' en ámbar #f59e0b. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La identidad de Abel dice que el wronskiano satisface:",
                  "opciones_md": [
                      "$W' = q\\, W$",
                      "**$W' = -p\\, W$**",
                      "$W' = -q\\, W$",
                      "$W = $ constante",
                  ],
                  "correcta": "B",
                  "pista_md": "Solo el coeficiente de $y'$ aparece.",
                  "explicacion_md": "$W' = -p W$, una EDO lineal de primer orden en $W$.",
              },
              {
                  "enunciado_md": "Si la EDO es $y'' + 3 y = 0$ ($p = 0$), el wronskiano de cualquier par de soluciones es:",
                  "opciones_md": [
                      "Cero",
                      "Decreciente",
                      "**Constante**",
                      "Igual a $e^{3 x}$",
                  ],
                  "correcta": "C",
                  "pista_md": "$p = 0 \\Rightarrow W' = 0$.",
                  "explicacion_md": "Wronskiano constante — coherente con que $\\cos$ y $\\sin$ tienen $W = 1$.",
              },
              {
                  "enunciado_md": "Reducción de orden requiere conocer:",
                  "opciones_md": [
                      "Solo $p(x)$",
                      "Solo $q(x)$",
                      "**Una solución $y_1$ de la EDO homogénea**",
                      "Una solución particular de la no homogénea",
                  ],
                  "correcta": "C",
                  "pista_md": "Lo dice el nombre.",
                  "explicacion_md": "Bajamos el orden de 2 a 1 gracias a una solución conocida.",
              },
          ]),

        ej(
            "Wronskiano por Abel",
            "Calcula la forma del wronskiano de soluciones de $y'' + (\\tan x) y' - y = 0$ en $-\\pi/2 < x < \\pi/2$.",
            ["$\\int \\tan x\\, dx = -\\ln|\\cos x|$."],
            (
                "$p = \\tan x$, $\\int p\\, dx = -\\ln|\\cos x|$. $W = W(0)\\, e^{\\ln|\\cos x|} = C |\\cos x|$. "
                "En $(-\\pi/2, \\pi/2)$, $\\cos x > 0$, así $W = C \\cos x$."
            ),
        ),

        ej(
            "Reducción de orden — Bessel modificada de orden 0",
            "Sabiendo que $y_1 = x$ es solución de $x^2 y'' + x y' - y = 0$ en $x > 0$, halla $y_2$.",
            ["$p = 1/x$ tras normalizar."],
            (
                "Normalizar: $y'' + \\dfrac{1}{x} y' - \\dfrac{1}{x^2} y = 0$. $p = 1/x$, $\\int p\\, dx = \\ln x$, $e^{-\\int p} = 1/x$.\n\n"
                "$y_2 = x \\int \\dfrac{1/x}{x^2}\\, dx = x \\int x^{-3}\\, dx = x \\cdot \\left(-\\dfrac{1}{2 x^2}\\right) = -\\dfrac{1}{2 x}$.\n\n"
                "Salvo constante, $y_2 = 1/x$. **Solución general:** $y = c_1 x + c_2 / x$."
            ),
        ),

        ej(
            "Reducción con $y_1$ trigonométrica",
            "Sabiendo que $y_1 = \\sin x$ es solución de $y'' + (\\cot x) y' + (\\csc^2 x) y = 0$ en $0 < x < \\pi$, halla $y_2$.",
            ["$\\int \\cot x\\, dx = \\ln|\\sin x|$."],
            (
                "$p = \\cot x$, $\\int p\\, dx = \\ln \\sin x$ (en $(0, \\pi)$). $e^{-\\int p} = 1/\\sin x$.\n\n"
                "$y_2 = \\sin x \\int \\dfrac{1/\\sin x}{\\sin^2 x}\\, dx = \\sin x \\int \\dfrac{dx}{\\sin^3 x}$.\n\n"
                "$\\int \\csc^3 x\\, dx = -\\dfrac{1}{2}(\\csc x \\cot x + \\ln|\\csc x + \\cot x|) + C$ (estándar).\n\n"
                "Multiplicando por $\\sin x$, $y_2 = -\\dfrac{1}{2}(\\cot x + \\sin x \\ln|\\csc x + \\cot x|)$ (salvo constante)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar normalizar antes de leer $p(x)$.** El $p$ que va en Abel y en reducción es el coeficiente de $y'$ en la **forma estándar**.",
              "**Equivocar el signo en $\\int p\\, dx$.** En Abel la exponencial lleva signo menos: $e^{-\\int p}$.",
              "**Pensar que reducción de orden funciona para cualquier EDO no lineal.** Es solo para lineales homogéneas.",
              "**Confundir reducción de orden con coeficientes indeterminados.** Reducción de orden es para la **homogénea** cuando ya conocemos $y_1$; coeficientes indeterminados es para la no homogénea.",
              "**No verificar que la $y_2$ obtenida es realmente independiente.** Si por casualidad sale proporcional a $y_1$, hubo un error de cálculo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Identidad de Abel:** $W(x) = W(x_0)\\, e^{-\\int_{x_0}^x p(s)\\, ds}$. El wronskiano queda determinado por $p$ y un valor inicial.",
              "**Consecuencia:** $W \\equiv 0$ o $W \\neq 0$ siempre — sin punto medio.",
              "**Reducción de orden:** $y_2 = y_1 \\int \\dfrac{e^{-\\int p\\, dx}}{y_1^2}\\, dx$ a partir de una solución conocida.",
              "**Aplicaciones:** ecuaciones especiales con coeficientes variables (Cauchy-Euler, Bessel, Legendre).",
              "**Cierre del capítulo:** cubrimos toda la teoría y los métodos para EDOs lineales de orden 2 y superior — homogéneas y no homogéneas, coeficientes constantes y variables, aplicaciones a vibraciones.",
              "**Próximo capítulo:** **sistemas de EDOs** — varias funciones desconocidas acopladas, modelos depredador-presa, circuitos con varias mallas, oscilaciones acopladas.",
          ]),
    ]
    return {
        "id": "lec-ed-2-9-formula-de-abel",
        "title": "Fórmula de Abel",
        "description": "Identidad de Abel para el wronskiano y reducción de orden: encontrar una segunda solución LI a partir de una conocida. Aplicaciones a EDOs con coeficientes variables.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 9,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "ecuaciones-diferenciales"

    existing_course = await db.courses.find_one({"id": course_id})
    if not existing_course:
        print(f"⚠ Curso '{course_id}' no existe. Ejecutá primero seed_ecuaciones_diferenciales_chapter_1.py.")
        return
    print(f"✓ Curso encontrado: {existing_course.get('title', course_id)}")

    chapter_id = "ch-ed-edo-orden-superior"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "EDO de Orden Superior",
        "description": (
            "EDOs lineales de orden 2 y superior: existencia y unicidad, principio de superposición, "
            "wronskiano, coeficientes constantes, vibraciones mecánicas, métodos de coeficientes "
            "indeterminados y variación de parámetros, identidad de Abel y reducción de orden."
        ),
        "order": 2,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_modelos,
        lesson_homogenea_general,
        lesson_coef_constantes,
        lesson_orden_n,
        lesson_coef_const_orden_n,
        lesson_vibraciones,
        lesson_coef_indeterminados,
        lesson_variacion_parametros,
        lesson_abel,
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
        f"✅ Capítulo 'EDO de Orden Superior' listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
