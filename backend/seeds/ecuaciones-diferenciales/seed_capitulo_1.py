"""
Seed del curso Ecuaciones Diferenciales — Capítulo 1: EDO de Primer Orden.

Crea el curso 'ecuaciones-diferenciales' (si no existe) y siembra el Cap. 1
con sus 9 lecciones:
  1.1 Definiciones
  1.2 Soluciones, existencia y unicidad
  1.3 EDO separables
  1.4 EDO lineales
  1.5 Métodos de sustitución
  1.6 EDO exactas
  1.7 EDO reductibles
  1.8 Modelos de población
  1.9 Estabilidad

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
# 1.1 Definiciones
# =====================================================================
def lesson_1_1():
    blocks = [
        b("texto", body_md=(
            "Las **ecuaciones diferenciales** son la herramienta matemática más potente para describir "
            "**cómo cambian las cosas en el tiempo o en el espacio**. Aparecen prácticamente en cualquier "
            "rama de la ciencia y la ingeniería:\n\n"
            "- **Física:** mecánica de Newton, vibraciones, electromagnetismo, mecánica cuántica.\n"
            "- **Biología:** dinámica poblacional, propagación de enfermedades, neurociencia.\n"
            "- **Química:** velocidades de reacción, equilibrios.\n"
            "- **Economía y finanzas:** dinámica de precios, modelos de inversión.\n"
            "- **Ingeniería:** circuitos eléctricos, sistemas de control, fluidos.\n\n"
            "En esta lección sentamos las bases: definimos qué es una EDO, vemos los **ejemplos clásicos** que "
            "vamos a resolver durante todo el curso, y aprendemos a **clasificarlas** por orden, linealidad y otros criterios.\n\n"
            "Al terminar:\n\n"
            "- Distingues una **ecuación diferencial ordinaria (EDO)** de una en derivadas parciales (EDP).\n"
            "- Identificas el **orden** de una EDO.\n"
            "- Clasificas como **lineal/no lineal**, **autónoma/no autónoma**.\n"
            "- Reconoces los modelos clásicos (enfriamiento de Newton, crecimiento poblacional, MAS, caída con fricción)."
        )),

        b("definicion",
          titulo="Ecuación diferencial ordinaria (EDO)",
          body_md=(
              "Una **ecuación diferencial** es una ecuación que **relaciona una función desconocida con sus derivadas**.\n\n"
              "- Si la función desconocida depende de **una sola variable independiente**, se llama **ecuación diferencial ordinaria (EDO)**.\n"
              "- Si depende de **dos o más variables** y aparecen derivadas parciales, se llama **ecuación en derivadas parciales (EDP)**.\n\n"
              "**Ejemplo de EDO:** $\\dfrac{dy}{dt} + 3y = 0$ — la función $y(t)$ depende solo de $t$.\n\n"
              "**Ejemplo de EDP:** $\\dfrac{\\partial u}{\\partial t} = k\\dfrac{\\partial^2 u}{\\partial x^2}$ — la función $u(t, x)$ depende de dos variables (ecuación del calor).\n\n"
              "**En este curso trabajamos exclusivamente con EDOs.**"
          )),

        b("definicion",
          titulo="Ejemplos clásicos de modelación",
          body_md=(
              "Los siguientes modelos aparecerán recurrentemente en el curso:\n\n"
              "**Ley de enfriamiento de Newton:**\n\n"
              "$\\dfrac{dT}{dt} = -k(T - T_a)$\n\n"
              "donde $T(t)$ es la temperatura del objeto, $T_a$ la temperatura ambiente y $k > 0$ una constante de enfriamiento.\n\n"
              "**Crecimiento poblacional (exponencial):**\n\n"
              "$\\dfrac{dP}{dt} = rP$\n\n"
              "donde $P(t)$ representa la población y $r$ es la tasa de crecimiento.\n\n"
              "**Caída con fricción:**\n\n"
              "$m\\dfrac{dv}{dt} = mg - kv$\n\n"
              "donde $v(t)$ es la velocidad, $m$ la masa, $g$ la gravedad y $k$ un coeficiente de resistencia.\n\n"
              "**Movimiento armónico simple (resorte ideal):**\n\n"
              "$\\dfrac{d^2 x}{dt^2} + \\omega^2 x = 0$\n\n"
              "donde $x(t)$ es la posición de una masa unida a un resorte y $\\omega$ es la frecuencia angular.\n\n"
              "**En cada caso, una EDO describe cómo cambia una cantidad en función del tiempo** — y al resolverla obtenemos la trayectoria completa del sistema."
          )),

        formulas(
            titulo="Clasificación de las EDOs",
            body=(
                "Una EDO se clasifica según varios criterios:\n\n"
                "**1. Por el tipo de derivada (Ordinaria vs. Parcial):** ya descrito.\n\n"
                "**2. Por el orden:** el **orden** es la derivada más alta que aparece.\n\n"
                "- $\\dfrac{dy}{dx} = y$ — orden $1$.\n"
                "- $\\dfrac{d^2 x}{dt^2} + x = 0$ — orden $2$.\n\n"
                "**3. Por la linealidad:** una EDO es **lineal** si la función desconocida y sus derivadas aparecen **a la primera potencia** y **no multiplicadas entre sí** (ni dentro de funciones trascendentes como $\\sin, \\ln, e^y$).\n\n"
                "- Lineal: $\\dfrac{dy}{dt} + 2y = 0$.\n"
                "- No lineal: $\\dfrac{dy}{dt} = y^2$, o $\\dfrac{dy}{dt} = \\sin y$.\n\n"
                "**4. Por la autonomía:** una EDO es **autónoma** si **no depende explícitamente de la variable independiente**.\n\n"
                "- Autónoma: $\\dfrac{dy}{dt} = y(1 - y)$ (no hay $t$ en el lado derecho).\n"
                "- No autónoma: $\\dfrac{dy}{dt} = t + y$ (sí aparece $t$ explícito).\n\n"
                "**Las EDOs autónomas tienen propiedades cualitativas especiales** que estudiaremos en lección 9 (estabilidad)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Clasificar tres EDOs",
          problema_md=(
              "Clasifica cada una por orden, linealidad y autonomía:\n\n"
              "**(a)** $y' + 3y = e^t$\n\n"
              "**(b)** $y'' + (\\sin t)\\,y = 0$\n\n"
              "**(c)** $y' = y^2 - 1$"
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $y' + 3y = e^t$. Orden $1$, **lineal** ($y$ y $y'$ aparecen a la 1ra potencia), **no autónoma** (aparece $e^t$ explícito)."
              ),
               "justificacion_md": "El término $e^t$ del lado derecho introduce dependencia explícita de $t$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $y'' + (\\sin t)\\,y = 0$. Orden $2$, **lineal** (aunque hay $\\sin t$, multiplica a $y$ — no es función de $y$), **no autónoma** (depende de $t$)."
              ),
               "justificacion_md": "**Cuidado:** la linealidad se evalúa respecto a $y$ y sus derivadas, no respecto a $t$. $\\sin t$ es coeficiente, no función de $y$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** $y' = y^2 - 1$. Orden $1$, **no lineal** ($y^2$), **autónoma** (sin $t$ en el lado derecho)."
              ),
               "justificacion_md": "$y^2$ rompe la linealidad. Y al no haber $t$ explícito, es autónoma.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Identificar modelos clásicos",
          problema_md=(
              "Para cada EDO, identifica qué modelo físico describe:\n\n"
              "**(a)** $\\dfrac{dV}{dt} = -kV$\n\n"
              "**(b)** $\\dfrac{d^2 \\theta}{dt^2} + \\dfrac{g}{L}\\sin\\theta = 0$\n\n"
              "**(c)** $\\dfrac{dQ}{dt} = (\\text{entrada}) - kQ$"
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $V' = -kV$ con $k > 0$: **decaimiento exponencial**. Modela decaimiento radiactivo, descarga de un capacitor, decaimiento de un fármaco en sangre."
              ),
               "justificacion_md": "Tasa de cambio proporcional a la cantidad actual, con signo negativo.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $\\theta'' + \\frac{g}{L}\\sin\\theta = 0$: **péndulo simple** (no lineal por $\\sin\\theta$). Si linealizamos para ángulos pequeños $\\sin\\theta \\approx \\theta$, recuperamos el MAS $\\theta'' + \\omega^2 \\theta = 0$."
              ),
               "justificacion_md": "Reconocer la 'forma' del modelo y la aproximación clásica.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** $Q' = (\\text{entrada}) - kQ$: **mezcla** (lección 4) o **modelo compartimental** (farmacología, ecología) — un compartimento recibe entrada constante y pierde proporcionalmente a su contenido."
              ),
               "justificacion_md": "Patrón 'entrada - salida' típico de balances de materia.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El orden de la EDO $y''' + (y')^2 = \\sin t$ es:",
                  "opciones_md": ["$1$", "$2$", "$3$", "$4$"],
                  "correcta": "C",
                  "pista_md": "Mira la derivada de mayor orden.",
                  "explicacion_md": "**Orden $3$.** $y'''$ es la derivada más alta. (El cuadrado $(y')^2$ no cambia el orden; sí afecta la linealidad.)",
              },
              {
                  "enunciado_md": "¿Cuál de las siguientes es lineal?",
                  "opciones_md": [
                      "$y' = y^2$",
                      "$y' + 2y = \\cos t$",
                      "$y' = e^y$",
                      "$y\\,y' = 1$",
                  ],
                  "correcta": "B",
                  "pista_md": "Linealidad: $y$ y $y'$ a la 1ra potencia, no multiplicadas entre sí, no dentro de funciones trascendentes.",
                  "explicacion_md": "**(B):** $y' + 2y = \\cos t$ es lineal. Las otras no: $y^2$ (cuadrática), $e^y$ (trascendente en $y$), $y\\cdot y'$ (producto de $y$ con su derivada).",
              },
              {
                  "enunciado_md": "$\\dfrac{dy}{dt} = y(1 - y)$ es:",
                  "opciones_md": [
                      "Lineal y autónoma",
                      "Lineal y no autónoma",
                      "**No lineal** y autónoma",
                      "No lineal y no autónoma",
                  ],
                  "correcta": "C",
                  "pista_md": "$y(1-y) = y - y^2$ tiene un $y^2$.",
                  "explicacion_md": "**No lineal** (por el $y^2$ tras expandir) y **autónoma** (no aparece $t$ explícito). Esta es la **ecuación logística**, fundamental en dinámica poblacional.",
              },
          ]),

        ej(
            "Clasificar EDOs",
            "Para cada una, indica orden, linealidad y autonomía:\n\n"
            "(a) $\\dfrac{d^2 y}{dx^2} + 4y = \\cos x$\n\n"
            "(b) $\\dfrac{dy}{dt} = ty^3$\n\n"
            "(c) $\\dfrac{dy}{dx} = \\dfrac{y}{x}$",
            ["Orden = derivada más alta. Lineal: ¿$y$ y derivadas a la primera potencia, sin productos ni funciones trascendentes?"],
            (
                "(a) Orden $2$, **lineal**, **no autónoma** (aparece $\\cos x$).\n\n"
                "(b) Orden $1$, **no lineal** ($y^3$), **no autónoma** ($t$ explícito).\n\n"
                "(c) Orden $1$, **no lineal** (estrictamente: $y/x$ no es lineal en $y$ porque divide por $x$ — pero es lineal si la reescribes como $xy' = y$, vemos que $y$ aparece a la 1ra potencia $\\Rightarrow$ **lineal**), **no autónoma** (aparece $x$).\n\n"
                "**Nota didáctica:** $y' = y/x$ es lineal porque puede escribirse como $y' - (1/x)y = 0$, forma estándar de una lineal homogénea (lección 4)."
            ),
        ),

        ej(
            "Identificar variables y derivadas",
            "Para la EDO $L\\dfrac{di}{dt} + Ri = E(t)$ (circuito RL): identifica la variable independiente, la función desconocida y el orden.",
            ["Es un modelo eléctrico clásico."],
            (
                "Variable independiente: $t$ (tiempo).\n\n"
                "Función desconocida: $i(t)$ (corriente eléctrica).\n\n"
                "Constantes: $L$ (inductancia), $R$ (resistencia), $E(t)$ (fuente de voltaje, dato).\n\n"
                "**Orden $1$**, **lineal**, autónoma solo si $E(t) = $ constante.\n\n"
                "Esta EDO se resolverá completamente en la lección 4 (lineales)."
            ),
        ),

        ej(
            "Verificar que una función es solución",
            "Comprueba que $y(t) = e^{-2t}$ es solución de la EDO $y' + 2y = 0$.",
            ["Calcula $y'$ y sustituye en la ecuación."],
            (
                "$y(t) = e^{-2t} \\Rightarrow y'(t) = -2e^{-2t}$.\n\n"
                "Sustituyendo: $y' + 2y = -2e^{-2t} + 2e^{-2t} = 0$ ✓.\n\n"
                "Sí es solución. **Más aún**, $y(t) = Ce^{-2t}$ con cualquier constante $C$ también es solución (familia de soluciones, lección 2)."
            ),
        ),

        fig(
            "Campo de pendientes (slope field) de una EDO de orden 1 y'=f(x,y) en el plano (x,y). "
            "Grilla de flechitas grises con la pendiente dy/dx en cada punto. Sobre el campo, dos curvas integrales solución en teal #06b6d4, tangentes a las flechitas. "
            "Una curva marcada como solución particular pasa por un punto (x0,y0) destacado en ámbar #f59e0b. "
            "Etiquetas: 'EDO de orden 1', 'campo de pendientes', 'solución particular'. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir EDO con EDP.** EDO: una variable independiente. EDP: dos o más, con derivadas parciales.",
              "**Asumir que 'no lineal' significa 'imposible de resolver'.** Hay muchos métodos para no lineales (separables, sustituciones), como veremos.",
              "**Pensar que $y^n$ con $n=1$ es no lineal.** $y^1 = y$ — eso **sí** es lineal.",
              "**Olvidar que las funciones de $t$ (no de $y$) pueden ser coeficientes.** En $y'' + (\\sin t)y = 0$, $\\sin t$ no rompe linealidad; un $\\sin y$ sí.",
              "**Confundir 'autónoma' con 'lineal'.** Son criterios distintos: $y' = y^2$ es no lineal pero autónoma.",
          ]),

        b("resumen",
          puntos_md=[
              "**EDO:** ecuación que relaciona una función con sus derivadas, dependiendo de **una sola** variable independiente.",
              "**Modelos clásicos:** enfriamiento de Newton, crecimiento exponencial, caída con fricción, MAS.",
              "**Clasificación:** orden, lineal/no lineal, autónoma/no autónoma, ordinaria/parcial.",
              "**Lineal:** $y$ y derivadas a la 1ra potencia, sin productos ni funciones trascendentes de $y$.",
              "**Autónoma:** sin dependencia explícita de la variable independiente.",
              "**Próxima lección:** soluciones, problemas de valor inicial (PVI) y el teorema de existencia y unicidad.",
          ]),
    ]
    return {
        "id": "lec-ed-1-1-definiciones",
        "title": "Definiciones",
        "description": "¿Qué es una EDO?, ejemplos clásicos (enfriamiento, crecimiento, MAS, caída con fricción), clasificación por orden, linealidad, autonomía, tipo.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 1.2 Soluciones, existencia y unicidad
# =====================================================================
def lesson_1_2():
    blocks = [
        b("texto", body_md=(
            "Resolver una EDO produce típicamente una **familia de funciones**: la **solución general**, "
            "con una constante arbitraria $C$. Para seleccionar **una sola** solución necesitamos "
            "una **condición inicial** — esto es el **problema de valor inicial (PVI)**.\n\n"
            "Pero antes de buscar soluciones, conviene preguntarnos: **¿existe siempre una solución?** "
            "**¿Es única?** El **teorema de existencia y unicidad** da condiciones suficientes para "
            "garantizarlo.\n\n"
            "Adicionalmente, los **campos direccionales** y las **isoclinas** permiten **visualizar** "
            "soluciones sin necesidad de resolver analíticamente.\n\n"
            "Al terminar:\n\n"
            "- Distingues **solución general** (familia con $C$) y **solución particular** (con $C$ fijada).\n"
            "- Resuelves PVIs simples por integración directa.\n"
            "- Aplicas el **teorema de existencia y unicidad**.\n"
            "- Interpretas isoclinas y campos direccionales."
        )),

        b("definicion",
          titulo="Solución general y solución particular",
          body_md=(
              "**Solución general** de una EDO: una **familia de funciones** que la satisfacen, parametrizada por una constante arbitraria $C$ (para EDOs de orden $1$).\n\n"
              "**Solución particular:** un miembro específico de esa familia, obtenido al fijar el valor de $C$ usando una **condición inicial**.\n\n"
              "**Ejemplo.** La EDO $y' = 3x^2$ se resuelve integrando:\n\n"
              "$y = \\int 3x^2\\,dx = x^3 + C.$\n\n"
              "**Solución general:** $y(x) = x^3 + C$ — infinitas curvas.\n\n"
              "Si añadimos la **condición inicial** $y(1) = 5$: $5 = 1^3 + C \\Rightarrow C = 4$.\n\n"
              "**Solución particular:** $y(x) = x^3 + 4$ — una sola curva.\n\n"
              "**Geometría:** la solución general es una familia de curvas paralelas; la condición inicial selecciona la curva que pasa por el punto $(1, 5)$."
          )),

        b("definicion",
          titulo="Problema de valor inicial (PVI)",
          body_md=(
              "Un **problema de valor inicial (PVI)** consiste en una EDO **junto con una condición inicial**:\n\n"
              "$$\\boxed{\\dfrac{dy}{dx} = f(x, y), \\qquad y(x_0) = y_0.}$$\n\n"
              "Resolver el PVI significa encontrar la **solución particular** que pasa por el punto $(x_0, y_0)$.\n\n"
              "**Para EDOs de orden $n$**, se necesitan $n$ condiciones iniciales: $y(x_0), y'(x_0), \\ldots, y^{(n-1)}(x_0)$."
          )),

        b("ejemplo_resuelto",
          titulo="Resolver un PVI por integración directa",
          problema_md=(
              "Resolver $\\dfrac{dy}{dx} = 2x + 3, \\quad y(1) = 2$."
          ),
          pasos=[
              {"accion_md": (
                  "Como el lado derecho solo depende de $x$, integramos directamente:\n\n"
                  "$y = \\int (2x + 3)\\,dx = x^2 + 3x + C.$"
              ),
               "justificacion_md": "Esto es la **solución general** — una familia de parábolas desplazadas.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicamos la condición $y(1) = 2$: $2 = 1 + 3 + C \\Rightarrow C = -2$.\n\n"
                  "**Solución particular:** $y(x) = x^2 + 3x - 2$."
              ),
               "justificacion_md": "**Verificación:** $y(1) = 1 + 3 - 2 = 2$ ✓ y $y'(x) = 2x + 3$ ✓.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Aplicación: caída libre con velocidad inicial",
          problema_md=(
              "Una nave lunar cae libremente con velocidad de $450\\text{ m/s}$. Al activar los retropropulsores, desacelera con $a = -2.5\\text{ m/s}^2$. ¿A qué altura deben activarse para lograr un alunizaje suave ($v = 0$)?"
          ),
          pasos=[
              {"accion_md": (
                  "Modelo: $\\dfrac{dv}{dt} = -2.5$. Integrando: $v(t) = -2.5t + C_1$. Con $v(0) = 450$: $C_1 = 450 \\Rightarrow v(t) = -2.5t + 450$."
              ),
               "justificacion_md": "Aceleración constante (negativa) $\\Rightarrow$ velocidad lineal en $t$.",
               "es_resultado": False},
              {"accion_md": (
                  "Posición: $s(t) = \\int v\\,dt = -1.25 t^2 + 450 t + C_2$. Tomando $s(0) = 0$ (punto donde se activan los retropropulsores) $\\Rightarrow C_2 = 0$.\n\n"
                  "Tiempo de alunizaje: $v(t) = 0 \\Rightarrow t = 180\\text{ s}$."
              ),
               "justificacion_md": "Doble integración: aceleración → velocidad → posición.",
               "es_resultado": False},
              {"accion_md": (
                  "Distancia recorrida: $s(180) = -1.25(180)^2 + 450(180) = -40500 + 81000 = 40500\\text{ m}$.\n\n"
                  "**Los retropropulsores deben activarse a $40\\,500\\text{ m}$ de altura.**"
              ),
               "justificacion_md": "**Lección general:** integrando dos veces una aceleración obtenemos posición — la base de toda la cinemática.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Campo direccional e isoclinas",
          body_md=(
              "Para una EDO de la forma $\\dfrac{dy}{dx} = f(x, y)$, el **campo direccional** asigna a cada punto $(x, y)$ del plano un pequeño segmento con pendiente $f(x, y)$. **Las soluciones son curvas tangentes a este campo en cada punto.**\n\n"
              "Las **isoclinas** son curvas $f(x, y) = m$ donde la pendiente es constante. Sirven para esbozar el campo direccional sin calcular pendientes punto por punto.\n\n"
              "**Utilidad:** permiten **visualizar el comportamiento cualitativo** de las soluciones sin resolver la EDO. Útil para:\n\n"
              "- Identificar **soluciones de equilibrio** (puntos donde $f(x, y) = 0$).\n"
              "- Analizar la **estabilidad** (lección 9).\n"
              "- Entender comportamiento asintótico cuando una solución analítica es difícil."
          )),

        fig(
            "Campo direccional y curvas solución de la EDO dy/dx = ky para distintos valores de k. "
            "Mostrar tres paneles lado a lado: (1) k = 1 con flechas exponenciales crecientes hacia arriba; "
            "(2) k = 0 con flechas horizontales; (3) k = -1 con flechas exponenciales decrecientes. "
            "En cada panel, dibujar varias curvas solución (en color teal #06b6d4) sobre el campo direccional "
            "(flechas pequeñas en color gris claro). Eje x horizontal de -2 a 2, eje y vertical de -1.5 a 1.5. "
            + STYLE
        ),

        b("teorema",
          nombre="Teorema de existencia y unicidad (Picard-Lindelöf)",
          enunciado_md=(
              "Considera el PVI:\n\n"
              "$$\\dfrac{dy}{dx} = f(x, y), \\qquad y(x_0) = y_0.$$\n\n"
              "Si $f(x, y)$ y $\\dfrac{\\partial f}{\\partial y}$ son **continuas** en un rectángulo abierto que contiene al punto $(x_0, y_0)$, entonces:\n\n"
              "**Existe** un intervalo alrededor de $x_0$ en el cual existe una **solución única** $y(x)$ del PVI.\n\n"
              "**Lectura:** condiciones de regularidad sobre $f$ garantizan **existencia y unicidad local**."
          ),
          demostracion_md=(
              "La demostración usa el método de aproximaciones sucesivas de Picard, formando una sucesión $y_n(x)$ que converge a la solución. Detalles fuera del alcance de este curso."
          )),

        b("ejemplo_resuelto",
          titulo="Cuando falla el teorema",
          problema_md=(
              "Considera el PVI $y' = \\dfrac{1}{x}, \\quad y(0) = 0$. ¿Garantiza el teorema una solución?"
          ),
          pasos=[
              {"accion_md": (
                  "Identificamos $f(x, y) = 1/x$. Esta función **no es continua** en $x = 0$ — donde está el punto inicial."
              ),
               "justificacion_md": "Las hipótesis del teorema fallan en el punto $(0, 0)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**El teorema NO garantiza existencia.** De hecho, integrando obtenemos $y = \\ln|x| + C$, que **no está definida** en $x = 0$. **No existe solución que pase por $(0, 0)$.**"
              ),
               "justificacion_md": "**Lección:** la **continuidad de $f$** es necesaria para que tenga sentido buscar una solución que pase por $(x_0, y_0)$.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**¿Qué falla cuando hay múltiples soluciones?**\n\n"
            "Considera el PVI $y' = 3y^{2/3}, y(0) = 0$. Aquí $f(x, y) = 3y^{2/3}$ **es continua** en $(0, 0)$, pero $\\dfrac{\\partial f}{\\partial y} = 2y^{-1/3}$ **NO es continua** ahí (diverge cuando $y \\to 0$).\n\n"
            "El teorema falla, y de hecho **hay infinitas soluciones**: $y(x) \\equiv 0$, $y(x) = x^3$, y para cualquier $a \\geq 0$, la función $y(x) = (x - a)^3$ para $x \\geq a$ y $y(x) = 0$ para $x < a$ también es solución.\n\n"
            "**Conclusión:** las hipótesis del teorema **no son cosméticas** — protegen contra patologías reales como pérdida de unicidad."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La solución general de $y' = 3x^2$ es:",
                  "opciones_md": [
                      "$y = x^3$",
                      "$y = x^3 + C$",
                      "$y = 6x$",
                      "$y = e^{x^3}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Integrar $3x^2$ y agregar la constante.",
                  "explicacion_md": "**$y = x^3 + C$.** La constante $C$ es esencial — sin ella, no es la solución general.",
              },
              {
                  "enunciado_md": "El teorema de existencia y unicidad requiere que:",
                  "opciones_md": [
                      "$f$ sea polinomial",
                      "**$f$ y $\\partial f/\\partial y$ sean continuas** en un entorno del punto inicial",
                      "$y_0 > 0$",
                      "La EDO sea lineal",
                  ],
                  "correcta": "B",
                  "pista_md": "Las hipótesis son sobre la regularidad de $f$.",
                  "explicacion_md": "Continuidad de $f$ y $\\partial f/\\partial y$ — son **suficientes** para garantizar existencia y unicidad **local** (en algún intervalo).",
              },
              {
                  "enunciado_md": "Para el PVI $y' = y, y(0) = 1$, la solución es:",
                  "opciones_md": ["$y = e^x$", "$y = x + 1$", "$y = 1$", "$y = e^{-x}$"],
                  "correcta": "A",
                  "pista_md": "Solución general $y = Ce^x$, ajusta $C$ con $y(0) = 1$.",
                  "explicacion_md": "**$y = e^x$.** Solución general $Ce^x$, con $C = 1$ por la condición inicial.",
              },
          ]),

        ej(
            "PVI sencillo",
            "Resuelve el PVI $\\dfrac{dy}{dx} = \\cos x, \\quad y(0) = 5$.",
            ["Integra el lado derecho y aplica la condición inicial."],
            (
                "$y = \\int \\cos x\\,dx = \\sin x + C$.\n\n"
                "$y(0) = 0 + C = 5 \\Rightarrow C = 5$.\n\n"
                "**Solución:** $y(x) = \\sin x + 5$."
            ),
        ),

        ej(
            "PVI de cinemática",
            "Una pelota se lanza hacia arriba desde el suelo con velocidad inicial $20\\text{ m/s}$. Con $g = 10\\text{ m/s}^2$, halla la altura máxima.",
            ["Modelo: $s'' = -g$. Integra dos veces, aplica $s(0) = 0$ y $s'(0) = 20$. Altura máxima cuando $v = 0$."],
            (
                "$s'' = -10 \\Rightarrow s'(t) = -10t + C_1$. $s'(0) = 20 \\Rightarrow C_1 = 20 \\Rightarrow v(t) = -10t + 20$.\n\n"
                "$s(t) = -5t^2 + 20t + C_2$. $s(0) = 0 \\Rightarrow C_2 = 0$.\n\n"
                "Altura máxima: $v(t) = 0 \\Rightarrow t = 2$. $s(2) = -20 + 40 = 20\\text{ m}$."
            ),
        ),

        ej(
            "Aplicar existencia y unicidad",
            "¿Garantiza el teorema una solución única para el PVI $y' = \\sqrt{y}, \\quad y(0) = 1$?",
            ["Verifica continuidad de $f$ y $\\partial f/\\partial y$ en un entorno de $(0, 1)$."],
            (
                "$f(x, y) = \\sqrt{y}$. Continua en $y > 0$ ✓.\n\n"
                "$\\partial f/\\partial y = \\dfrac{1}{2\\sqrt{y}}$. Continua en $y > 0$ ✓.\n\n"
                "El punto inicial $(0, 1)$ tiene $y_0 = 1 > 0$, en una región donde ambas son continuas. **Sí garantiza solución única**.\n\n"
                "(Notar que en $(0, 0)$ fallaría — $\\partial f/\\partial y$ diverge, dando lugar a múltiples soluciones).\n\n"
                "**Resolviendo:** $\\dfrac{dy}{\\sqrt{y}} = dx \\Rightarrow 2\\sqrt{y} = x + C$. Con $y(0) = 1$: $C = 2$. Solución: $\\sqrt{y} = x/2 + 1$, es decir, $y = (x/2 + 1)^2$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar la constante $C$ al integrar.** Sin ella, no es la solución general — falta toda la familia.",
              "**Aplicar la condición inicial antes de integrar.** Primero la solución general, después la condición.",
              "**Confundir 'solución única' con 'solución global'.** El teorema garantiza existencia y unicidad **local** (en algún intervalo).",
              "**Pensar que toda EDO tiene solución elemental.** Muchas requieren métodos especiales (próximas lecciones), o solo soluciones implícitas, o aproximaciones numéricas.",
              "**Olvidar verificar las hipótesis del teorema.** Sin ellas, la unicidad puede fallar (como en $y' = 3y^{2/3}$).",
          ]),

        b("resumen",
          puntos_md=[
              "**Solución general:** familia con constante $C$.",
              "**Solución particular:** $C$ fijada por condición inicial.",
              "**PVI:** EDO + condición(es) inicial(es).",
              "**Teorema de existencia y unicidad:** continuidad de $f$ y $\\partial f/\\partial y$ $\\Rightarrow$ solución única local.",
              "**Campo direccional / isoclinas:** visualización cualitativa sin resolver analíticamente.",
              "**Próxima lección:** primer método sistemático de resolución — **EDOs separables**.",
          ]),
    ]
    return {
        "id": "lec-ed-1-2-soluciones-existencia-unicidad",
        "title": "Soluciones, existencia y unicidad",
        "description": "Solución general y particular, problema de valor inicial (PVI), teorema de existencia y unicidad, campos direccionales e isoclinas.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 1.3 EDO Separables
# =====================================================================
def lesson_1_3():
    blocks = [
        b("texto", body_md=(
            "Las **EDOs separables** son la familia más simple y, a la vez, una de las más útiles. Una EDO es "
            "**separable** si puede escribirse de forma que **todas las variables $y$ queden de un lado** y "
            "**todas las $x$ del otro**:\n\n"
            "$$\\dfrac{dy}{dx} = g(x)\\,h(y) \\Longrightarrow \\dfrac{dy}{h(y)} = g(x)\\,dx.$$\n\n"
            "Una vez separadas, **se integran ambos lados** y la EDO queda resuelta (al menos implícitamente).\n\n"
            "Las separables modelan fenómenos importantes:\n\n"
            "- **Crecimiento y decaimiento exponencial** (radioactividad, enfriamiento de Newton, interés compuesto).\n"
            "- **Datación con carbono-14** (arqueología).\n"
            "- **Ley de Torricelli** (drenaje de tanques).\n"
            "- **Dinámica poblacional simple**.\n\n"
            "Al terminar:\n\n"
            "- Identificas EDOs separables.\n"
            "- Aplicas el método de separación.\n"
            "- Resuelves PVIs con soluciones explícitas e implícitas.\n"
            "- Aplicas separables a problemas reales (decaimiento radiactivo, Torricelli)."
        )),

        b("definicion",
          titulo="EDO separable y método",
          body_md=(
              "Una EDO de primer orden es **separable** si se puede escribir como\n\n"
              "$$\\boxed{\\dfrac{dy}{dx} = g(x) \\cdot h(y).}$$\n\n"
              "**Método de separación de variables:**\n\n"
              "1. Reescribe como $\\dfrac{1}{h(y)}\\,dy = g(x)\\,dx$ (siempre que $h(y) \\neq 0$).\n"
              "2. Integra ambos lados: $\\int \\dfrac{dy}{h(y)} = \\int g(x)\\,dx$.\n"
              "3. Despeja $y$ en función de $x$ (si es posible) o deja la solución **implícitamente**.\n"
              "4. Aplica condición inicial (si la hay) para fijar la constante.\n\n"
              "**Importante:** los puntos donde $h(y) = 0$ dan **soluciones constantes** que pueden perderse en el paso 1 — verificar por separado."
          )),

        b("ejemplo_resuelto",
          titulo="PVI con solución explícita",
          problema_md=(
              "Resolver $\\dfrac{dy}{dx} = -6xy, \\quad y(0) = 7$."
          ),
          pasos=[
              {"accion_md": (
                  "Separamos: $\\dfrac{dy}{y} = -6x\\,dx$. Integramos:\n\n"
                  "$\\ln|y| = -3x^2 + C.$"
              ),
               "justificacion_md": "Reorganizar variables a lados opuestos antes de integrar.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicamos exponencial: $|y| = e^{-3x^2 + C} = Ke^{-3x^2}$ con $K = e^C > 0$. Permitiendo cualquier signo: $y = Ce^{-3x^2}$ con $C \\in \\mathbb{R}$."
              ),
               "justificacion_md": "**Truco común:** absorber el valor absoluto en la constante para permitir signos negativos.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicar $y(0) = 7$: $7 = Ce^0 = C \\Rightarrow C = 7$.\n\n"
                  "**Solución:** $y(x) = 7e^{-3x^2}$. Verificación: $y' = 7(-6x)e^{-3x^2} = -6x \\cdot 7e^{-3x^2} = -6xy$ ✓."
              ),
               "justificacion_md": "**Patrón:** $y' = ay$ con $a$ función de $x$ se resuelve por separación dando una exponencial.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="PVI con solución implícita",
          problema_md=(
              "Resolver $\\dfrac{dy}{dx} = \\dfrac{4 - 2x}{3y^2 - 5}, \\quad y(1) = 3$."
          ),
          pasos=[
              {"accion_md": (
                  "Separamos: $(3y^2 - 5)\\,dy = (4 - 2x)\\,dx$. Integramos:\n\n"
                  "$y^3 - 5y = 4x - x^2 + C.$"
              ),
               "justificacion_md": "Una vez separadas, ambos lados son integrales elementales.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicar $y(1) = 3$: $27 - 15 = 4 - 1 + C \\Rightarrow 12 = 3 + C \\Rightarrow C = 9$.\n\n"
                  "**Solución implícita:** $y^3 - 5y = 4x - x^2 + 9$."
              ),
               "justificacion_md": "**Lección:** algunas soluciones quedan **implícitas** (no se puede despejar $y$ en términos elementales) y eso está perfectamente bien.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Aplicación: crecimiento y decaimiento exponencial",
          body_md=(
              "El modelo $\\dfrac{dy}{dt} = ky$ es **el caso separable más importante**. Tiene solución\n\n"
              "$$y(t) = y_0 e^{kt},$$\n\n"
              "donde $y_0 = y(0)$ es el valor inicial.\n\n"
              "- **$k > 0$:** crecimiento exponencial (interés compuesto, población sin límites).\n"
              "- **$k < 0$:** decaimiento exponencial (radiactividad, descarga capacitor).\n\n"
              "**Vida media** $\\tau$ (decaimiento): tiempo para que la cantidad se reduzca a la mitad. Cumple $e^{k\\tau} = 1/2 \\Rightarrow \\tau = \\dfrac{\\ln 2}{|k|}$ (con $k < 0$, así $|k| > 0$)."
          )),

        b("ejemplo_resuelto",
          titulo="Datación con carbono-14",
          problema_md=(
              "Una muestra de carbono de leña en Stonehenge contiene un $63\\%$ del $^{14}\\text{C}$ original. La vida media del $^{14}\\text{C}$ es $5\\,730$ años. ¿Qué edad tiene la muestra?"
          ),
          pasos=[
              {"accion_md": (
                  "Modelo: $y(t) = y_0 e^{kt}$ con $k < 0$. Vida media de $5\\,730$ años:\n\n"
                  "$y(5\\,730) = y_0/2 \\Rightarrow e^{5730k} = 1/2 \\Rightarrow k = -\\dfrac{\\ln 2}{5730}.$"
              ),
               "justificacion_md": "Determinar la constante $k$ a partir de la vida media.",
               "es_resultado": False},
              {"accion_md": (
                  "Para la muestra: $y(t) = 0.63 y_0 \\Rightarrow e^{kt} = 0.63 \\Rightarrow t = \\dfrac{\\ln 0.63}{k}$."
              ),
               "justificacion_md": "Despejar $t$ usando logaritmo.",
               "es_resultado": False},
              {"accion_md": (
                  "$t = \\dfrac{\\ln 0.63}{-\\ln 2 / 5730} = \\dfrac{-0.4621}{-0.0001210} \\approx 3\\,820\\text{ años}$.\n\n"
                  "**La muestra tiene aproximadamente $3\\,820$ años.**"
              ),
               "justificacion_md": "**Lección:** este es el método estándar de datación arqueológica para muestras orgánicas hasta ~50,000 años.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Ley de Torricelli — drenaje de tanque",
          problema_md=(
              "Un tanque hemisférico de radio $4$ ft se llena de agua. Se hace un orificio de diámetro $1$ pulgada en el fondo. ¿Cuánto tarda en vaciarse? (Usar $g = 32\\text{ ft/s}^2$.)"
          ),
          pasos=[
              {"accion_md": (
                  "**Ley de Torricelli:** la velocidad del agua que escapa es $v = \\sqrt{2gy}$ con $y$ = altura del agua. El volumen $V$ disminuye según:\n\n"
                  "$\\dfrac{dV}{dt} = -a\\sqrt{2gy}$, con $a = $ área del orificio.\n\n"
                  "Para tanque hemisférico, área transversal a altura $y$: $A(y) = \\pi[16 - (4-y)^2] = \\pi(8y - y^2)$. Por la regla de la cadena, $\\dfrac{dV}{dt} = A(y)\\dfrac{dy}{dt}$."
              ),
               "justificacion_md": "Combinar la fórmula de Torricelli con la geometría del tanque.",
               "es_resultado": False},
              {"accion_md": (
                  "Igualando: $\\pi(8y - y^2)\\dfrac{dy}{dt} = -\\pi(1/24)^2\\sqrt{64y}$. Simplificando ($a = \\pi(1/24)^2$, factorizando):\n\n"
                  "$(8y - y^2)\\,dy = -\\dfrac{1}{72}\\,dt$ (separable)."
              ),
               "justificacion_md": "Después del álgebra, queda una EDO separable.",
               "es_resultado": False},
              {"accion_md": (
                  "Integrando ambos lados:\n\n"
                  "$\\int (8y^{1/2} - y^{3/2})\\,dy = -\\dfrac{1}{72}\\int dt$\n\n"
                  "$\\dfrac{16}{3}y^{3/2} - \\dfrac{2}{5}y^{5/2} = -\\dfrac{t}{72} + C$.\n\n"
                  "Con $y(0) = 4$: $C = \\dfrac{16}{3}\\cdot 8 - \\dfrac{2}{5}\\cdot 32 = \\dfrac{448}{15}$.\n\n"
                  "Tanque vacío: $y = 0 \\Rightarrow t = 72 \\cdot \\dfrac{448}{15} = 2\\,150$ s $\\approx 35$ min $50$ s."
              ),
               "justificacion_md": "**Aplicación clásica** de separación de variables a un problema de ingeniería.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál de las siguientes EDOs es separable?",
                  "opciones_md": [
                      "$y' = x + y$",
                      "$y' = e^{x+y} = e^x e^y$",
                      "$y' = \\sin(xy)$",
                      "$y' = x^2 + y^2$",
                  ],
                  "correcta": "B",
                  "pista_md": "Separable: $y' = g(x)h(y)$.",
                  "explicacion_md": "**$y' = e^x e^y$** es separable: $\\dfrac{dy}{e^y} = e^x\\,dx$.",
              },
              {
                  "enunciado_md": "Para resolver $y' = ky$, después de separar e integrar obtenemos:",
                  "opciones_md": [
                      "$y = kx + C$",
                      "$\\ln|y| = kt + C$",
                      "$y^2 = kt + C$",
                      "$y = k + Ct$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\int dy/y = \\ln|y|$.",
                  "explicacion_md": "**$\\ln|y| = kt + C$**, equivalente a $y = Ce^{kt}$ tras exponenciar.",
              },
              {
                  "enunciado_md": "El modelo de decaimiento radiactivo $y' = ky$ con $k < 0$:",
                  "opciones_md": [
                      "Crece exponencialmente",
                      "**Decae exponencialmente**",
                      "Oscila",
                      "Es lineal en $t$",
                  ],
                  "correcta": "B",
                  "pista_md": "$k < 0 \\Rightarrow$ exponente negativo.",
                  "explicacion_md": "**Decae exponencialmente.** $y(t) = y_0 e^{kt}$ con $k < 0$ tiende a $0$ cuando $t \\to \\infty$.",
              },
          ]),

        ej(
            "Separable básica",
            "Resuelve $\\dfrac{dy}{dx} = xy$, condición $y(0) = 2$.",
            ["Separar: $dy/y = x\\,dx$. Integrar y aplicar condición inicial."],
            (
                "$\\dfrac{dy}{y} = x\\,dx \\Rightarrow \\ln|y| = \\dfrac{x^2}{2} + C$.\n\n"
                "$y = Ke^{x^2/2}$. Con $y(0) = 2$: $K = 2$.\n\n"
                "**$y(x) = 2e^{x^2/2}$.**"
            ),
        ),

        ej(
            "Crecimiento bacteriano",
            "Una colonia de bacterias se duplica cada $3$ horas. Si inicialmente hay $1\\,000$ bacterias, ¿cuántas hay en $12$ horas?",
            ["Modelo: $y' = ky$. Hallar $k$ con la información de duplicación."],
            (
                "$y(t) = 1000 e^{kt}$. Duplicación en $3$ h: $y(3) = 2000 \\Rightarrow e^{3k} = 2 \\Rightarrow k = \\ln 2/3$.\n\n"
                "$y(12) = 1000 e^{12 \\ln 2/3} = 1000 \\cdot 2^4 = 16\\,000$ bacterias."
            ),
        ),

        ej(
            "Ley de enfriamiento de Newton",
            "Un café a $90°C$ se deja en una sala a $20°C$. Tras $5$ min está a $80°C$. ¿Qué temperatura tendrá tras $30$ min?",
            ["Modelo: $T' = -k(T - T_a)$ con $T_a = 20$. Hacer cambio $u = T - T_a$ para reducirlo a $u' = -ku$."],
            (
                "Sea $u = T - 20$. Entonces $u' = -ku$, con solución $u(t) = u_0 e^{-kt}$.\n\n"
                "$u_0 = T(0) - 20 = 70$. $u(5) = T(5) - 20 = 60 \\Rightarrow e^{-5k} = 60/70 = 6/7 \\Rightarrow k = -\\ln(6/7)/5 \\approx 0.03083$.\n\n"
                "$T(30) = 20 + 70 e^{-30k} = 20 + 70(6/7)^6 \\approx 20 + 70 \\cdot 0.3966 \\approx 47.8°C$."
            ),
        ),

        fig(
            "Diagrama de EDO separables en dos paneles. "
            "Izquierda: ecuación dy/g(y) = f(x) dx con dos signos de integral grandes a cada lado y flechas curvas ámbar #f59e0b indicando 'integrar ambos lados'. "
            "Derecha: plano (x, y) con familia de curvas solución y = F(x, C) en teal #06b6d4 para varios C; una curva destacada en ámbar #f59e0b pasa por un punto inicial (x0, y0). "
            "Etiquetas 'familia de soluciones' y 'solución particular'. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar dividir por $h(y)$ correctamente** o perder soluciones donde $h(y) = 0$.",
              "**No agregar la constante $C$ tras integrar.** Especialmente importante porque luego se ajusta con la condición inicial.",
              "**Aplicar mal el valor absoluto** al exponenciar $\\ln|y|$. La forma $y = Ce^{...}$ con $C \\in \\mathbb{R}$ absorbe el signo.",
              "**Intentar despejar $y$ siempre.** Algunas soluciones quedan implícitas — dejarlas así.",
              "**No verificar la solución** al final. Sustituir en la EDO original es el cierre más seguro.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma:** $y' = g(x)\\,h(y)$ — variables separables.",
              "**Método:** $\\dfrac{dy}{h(y)} = g(x)\\,dx$, integrar ambos lados.",
              "**Aplicación clave:** $y' = ky$ tiene solución $y = y_0 e^{kt}$.",
              "**Casos clásicos:** crecimiento/decaimiento exponencial, enfriamiento de Newton, datación radiactiva, Torricelli.",
              "**Soluciones implícitas** son válidas; no siempre se puede despejar $y$.",
              "**Próxima lección:** **EDOs lineales** — método del factor integrante.",
          ]),
    ]
    return {
        "id": "lec-ed-1-3-separables",
        "title": "EDO separables",
        "description": "Método de separación de variables, ejemplos con soluciones explícitas e implícitas, aplicaciones (decaimiento radiactivo, ley de Torricelli, enfriamiento de Newton).",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
    }


# =====================================================================
# 1.4 EDO Lineales
# =====================================================================
def lesson_1_4():
    blocks = [
        b("texto", body_md=(
            "Las **EDOs lineales de primer orden** tienen la forma\n\n"
            "$$\\dfrac{dy}{dx} + P(x)\\,y = Q(x).$$\n\n"
            "Aunque a primera vista parecen más complicadas que las separables, tienen un **método de "
            "resolución sistemático y elegante**: el **factor integrante**.\n\n"
            "Este método convierte el lado izquierdo en la **derivada de un producto**, lo que permite integrar directamente.\n\n"
            "Las EDOs lineales de primer orden modelan:\n\n"
            "- **Circuitos RC y RL** (electrónica).\n"
            "- **Disipación térmica** y mezclas.\n"
            "- **Modelos compartimentales** en biología y farmacología.\n"
            "- **Enfriamiento de Newton** generalizado (con temperatura ambiente variable).\n\n"
            "Al terminar:\n\n"
            "- Reconoces la forma estándar $y' + P(x)y = Q(x)$.\n"
            "- Aplicas el **método del factor integrante** $\\rho(x) = e^{\\int P(x)dx}$.\n"
            "- Resuelves PVIs lineales.\n"
            "- Modelas y resuelves problemas de **mezclas**."
        )),

        b("definicion",
          titulo="EDO lineal de primer orden y factor integrante",
          body_md=(
              "Una **EDO lineal de primer orden** se escribe en forma estándar como\n\n"
              "$$\\boxed{\\dfrac{dy}{dx} + P(x)\\,y = Q(x),}$$\n\n"
              "con $P(x), Q(x)$ funciones continuas en un intervalo $I$.\n\n"
              "**Método del factor integrante:**\n\n"
              "1. Calcular $\\rho(x) = e^{\\int P(x)\\,dx}$ — el **factor integrante**.\n"
              "2. Multiplicar la ecuación por $\\rho(x)$. El lado izquierdo se vuelve la **derivada de un producto**:\n"
              "   $$\\dfrac{d}{dx}\\bigl[\\rho(x)\\,y\\bigr] = \\rho(x)\\,Q(x).$$\n"
              "3. Integrar ambos lados:\n"
              "   $$\\rho(x)\\,y = \\int \\rho(x)\\,Q(x)\\,dx + C.$$\n"
              "4. Despejar $y$:\n"
              "   $$\\boxed{y(x) = \\dfrac{1}{\\rho(x)}\\left[\\int \\rho(x)\\,Q(x)\\,dx + C\\right].}$$\n\n"
              "**Por qué funciona:** la elección de $\\rho$ garantiza $\\rho'(x) = \\rho(x) P(x)$, así $\\rho y' + \\rho P y = \\rho y' + \\rho' y = (\\rho y)'$ por la regla del producto."
          )),

        b("ejemplo_resuelto",
          titulo="PVI lineal con factor integrante",
          problema_md=(
              "Resolver $\\dfrac{dy}{dx} - y = \\dfrac{11}{8}e^{-x/3}, \\quad y(0) = -1$."
          ),
          pasos=[
              {"accion_md": (
                  "Forma estándar con $P(x) = -1$, $Q(x) = \\frac{11}{8}e^{-x/3}$.\n\n"
                  "Factor integrante: $\\rho(x) = e^{\\int -1\\,dx} = e^{-x}$."
              ),
               "justificacion_md": "Identificar $P(x)$ y calcular $\\rho$.",
               "es_resultado": False},
              {"accion_md": (
                  "Multiplicar por $e^{-x}$:\n\n"
                  "$e^{-x}y' - e^{-x}y = \\dfrac{11}{8}e^{-x}e^{-x/3} = \\dfrac{11}{8}e^{-4x/3}$.\n\n"
                  "Lado izquierdo es $\\dfrac{d}{dx}(e^{-x}y)$. Integrar:\n\n"
                  "$e^{-x}y = \\int \\dfrac{11}{8}e^{-4x/3}\\,dx = \\dfrac{11}{8} \\cdot \\dfrac{-3}{4}e^{-4x/3} + C = -\\dfrac{33}{32}e^{-4x/3} + C$."
              ),
               "justificacion_md": "El truco: tras multiplicar por $\\rho$, el lado izquierdo es exactamente una derivada de producto.",
               "es_resultado": False},
              {"accion_md": (
                  "Despejar: $y = e^x\\left(-\\dfrac{33}{32}e^{-4x/3} + C\\right)$.\n\n"
                  "Aplicar $y(0) = -1$: $-1 = -\\dfrac{33}{32} + C \\Rightarrow C = -1 + \\dfrac{33}{32} = \\dfrac{1}{32}$.\n\n"
                  "**Solución:** $y(x) = e^x\\left(-\\dfrac{33}{32}e^{-4x/3} + \\dfrac{1}{32}\\right)$."
              ),
               "justificacion_md": "**Patrón:** factor integrante + integración + condición inicial. Sistemático para cualquier lineal.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Problemas de mezclas",
          body_md=(
              "Un **problema de mezclas** modela un tanque con una sustancia disuelta cuya cantidad cambia por entradas y salidas. El modelo general es\n\n"
              "$$\\dfrac{dA}{dt} = \\text{tasa de entrada} - \\text{tasa de salida},$$\n\n"
              "donde $A(t)$ es la cantidad de sustancia en el tanque.\n\n"
              "- **Tasa de entrada** = (concentración del fluido que entra) × (tasa de flujo de entrada).\n"
              "- **Tasa de salida** = (concentración en el tanque) × (tasa de flujo de salida) = $\\dfrac{A(t)}{V(t)} \\cdot r_{\\text{out}}$.\n\n"
              "**Cuidado con $V(t)$:** si las tasas de entrada y salida difieren, el volumen $V(t)$ **cambia con el tiempo**: $V(t) = V_0 + (r_{\\text{in}} - r_{\\text{out}})t$.\n\n"
              "Estos problemas se reducen a una **EDO lineal de primer orden** que se resuelve con factor integrante."
          )),

        b("ejemplo_resuelto",
          titulo="Mezcla con volumen variable",
          problema_md=(
              "Un tanque de $120$ gal contiene $90$ lb de sal en $90$ gal de agua. Entra salmuera con $2$ lb/gal a $4$ gal/min, sale mezcla a $3$ gal/min. ¿Cuánta sal hay cuando el tanque se llena?"
          ),
          pasos=[
              {"accion_md": (
                  "Volumen: $V(t) = 90 + (4 - 3)t = 90 + t$.\n\n"
                  "Tanque lleno: $V = 120 \\Rightarrow t = 30$ min.\n\n"
                  "**Modelo:** $\\dfrac{dA}{dt} = (4)(2) - \\dfrac{A}{90 + t}\\cdot 3 = 8 - \\dfrac{3A}{90 + t}$, con $A(0) = 90$."
              ),
               "justificacion_md": "Identificar entrada, salida y volumen variable.",
               "es_resultado": False},
              {"accion_md": (
                  "Forma estándar: $A' + \\dfrac{3}{90+t}A = 8$. Factor integrante:\n\n"
                  "$\\rho(t) = e^{\\int 3/(90+t)\\,dt} = e^{3\\ln(90+t)} = (90+t)^3$."
              ),
               "justificacion_md": "$P(t) = 3/(90+t)$, integral elemental.",
               "es_resultado": False},
              {"accion_md": (
                  "Multiplicar y reconocer derivada del producto:\n\n"
                  "$\\dfrac{d}{dt}\\bigl[(90+t)^3 A\\bigr] = 8(90+t)^3$.\n\n"
                  "Integrar: $(90+t)^3 A = 2(90+t)^4 + C \\Rightarrow A(t) = 2(90+t) + \\dfrac{C}{(90+t)^3}$.\n\n"
                  "$A(0) = 90$: $90 = 180 + C/90^3 \\Rightarrow C = -90 \\cdot 90^3 = -90^4$."
              ),
               "justificacion_md": "Resolución estándar tras factor integrante.",
               "es_resultado": False},
              {"accion_md": (
                  "$A(t) = 2(90+t) - \\dfrac{90^4}{(90+t)^3}$. Evaluar en $t = 30$:\n\n"
                  "$A(30) = 240 - \\dfrac{90^4}{120^3} = 240 - \\dfrac{65\\,610\\,000}{1\\,728\\,000} = 240 - 37.97 \\approx 202\\text{ lb}$."
              ),
               "justificacion_md": "**Más sal en el tanque al final** porque entra más concentrada de lo que está inicialmente. Verificar el modelo con valores límite es un buen control.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El factor integrante para $y' + 2y = e^x$ es:",
                  "opciones_md": ["$e^{2x}$", "$e^{x^2}$", "$e^x$", "$x^2$"],
                  "correcta": "A",
                  "pista_md": "$\\rho = e^{\\int P\\,dx}$ con $P = 2$.",
                  "explicacion_md": "**$\\rho = e^{2x}$.** $\\int 2\\,dx = 2x$.",
              },
              {
                  "enunciado_md": "Tras multiplicar $y' + Py = Q$ por $\\rho = e^{\\int P}$, el lado izquierdo es:",
                  "opciones_md": [
                      "$\\rho y' + \\rho^2 y$",
                      "**$(\\rho y)' = \\rho y' + \\rho' y$**",
                      "$\\rho^2 y$",
                      "$y'$",
                  ],
                  "correcta": "B",
                  "pista_md": "Regla del producto.",
                  "explicacion_md": "**$(\\rho y)'$.** Esta es la magia: el factor integrante convierte el lado izquierdo en una derivada de producto, integrable directamente.",
              },
              {
                  "enunciado_md": "En un problema de mezclas, si entrada $4$ gal/min y salida $4$ gal/min, el volumen:",
                  "opciones_md": [
                      "Crece linealmente",
                      "Decrece linealmente",
                      "**Permanece constante**",
                      "Oscila",
                  ],
                  "correcta": "C",
                  "pista_md": "Tasa neta = entrada - salida.",
                  "explicacion_md": "**Constante.** Si las tasas se igualan, no hay cambio neto de volumen — simplifica el modelo.",
              },
          ]),

        ej(
            "Lineal con $P$ constante",
            "Resuelve $y' + 3y = 6$, $y(0) = 1$.",
            ["$\\rho = e^{3x}$, multiplica e integra."],
            (
                "$\\rho = e^{3x}$. $(e^{3x}y)' = 6e^{3x}$. $e^{3x}y = 2e^{3x} + C \\Rightarrow y = 2 + Ce^{-3x}$.\n\n"
                "$y(0) = 1 \\Rightarrow 1 = 2 + C \\Rightarrow C = -1$. **$y = 2 - e^{-3x}$.**\n\n"
                "Verificación: $y' = 3e^{-3x}$, $3y = 6 - 3e^{-3x}$, suma $= 6$ ✓."
            ),
        ),

        ej(
            "Mezcla con volumen constante",
            "Un tanque de $100$ L contiene agua pura. Entra salmuera con $2$ g/L a $5$ L/min, sale mezcla a $5$ L/min. ¿Cuánta sal hay tras $20$ min?",
            ["Volumen constante. $A' = 10 - A/20$."],
            (
                "$A' + \\dfrac{1}{20}A = 10$. $\\rho = e^{t/20}$. $(e^{t/20}A)' = 10e^{t/20} \\Rightarrow A = 200 + Ce^{-t/20}$.\n\n"
                "$A(0) = 0 \\Rightarrow C = -200$. $A(t) = 200(1 - e^{-t/20})$.\n\n"
                "$A(20) = 200(1 - 1/e) \\approx 126.4$ g."
            ),
        ),

        ej(
            "Circuito RL",
            "En un circuito RL, $L\\dfrac{di}{dt} + Ri = E$ (constante). Halla $i(t)$ con $i(0) = 0$.",
            ["EDO lineal con $P = R/L$, $Q = E/L$."],
            (
                "Forma estándar: $i' + (R/L)i = E/L$. $\\rho = e^{Rt/L}$.\n\n"
                "$(e^{Rt/L}i)' = (E/L)e^{Rt/L} \\Rightarrow e^{Rt/L}i = (E/R)e^{Rt/L} + C \\Rightarrow i = E/R + Ce^{-Rt/L}$.\n\n"
                "$i(0) = 0 \\Rightarrow C = -E/R$. $i(t) = (E/R)(1 - e^{-Rt/L})$.\n\n"
                "**Interpretación:** la corriente crece exponencialmente hacia el valor estacionario $E/R$ (Ley de Ohm)."
            ),
        ),

        fig(
            "Diagrama del factor integrante para EDO lineales de primer orden. "
            "Arriba: ecuación original y' + P(x) y = Q(x). Flecha curva grande ámbar #f59e0b con la etiqueta 'multiplicar por μ(x) = e^∫P(x)dx' baja al paso siguiente. "
            "Abajo: la ecuación transformada en (μ y)' = μ Q, con el lado izquierdo resaltado en teal #06b6d4 como derivada exacta de un producto. "
            "Pequeño recuadro lateral con la fórmula del factor integrante. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**No poner la EDO en forma estándar** $y' + P(x)y = Q(x)$ antes de identificar $P$. Coeficiente de $y'$ debe ser $1$.",
              "**Olvidar la constante $C$ tras integrar** el lado derecho.",
              "**Aplicar el método a EDOs no lineales.** El método del factor integrante solo funciona si la EDO es **lineal** en $y$.",
              "**Confundir 'factor integrante' con 'integral'.** Es una función $\\rho(x)$ que multiplica la ecuación.",
              "**En problemas de mezclas, asumir volumen constante** sin verificar tasas de entrada y salida.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma estándar:** $y' + P(x)y = Q(x)$.",
              "**Factor integrante:** $\\rho(x) = e^{\\int P(x)\\,dx}$.",
              "**Tras multiplicar:** $(\\rho y)' = \\rho Q$, integrable directamente.",
              "**Solución general:** $y(x) = \\dfrac{1}{\\rho}\\left[\\int \\rho Q\\,dx + C\\right]$.",
              "**Aplicaciones:** mezclas, circuitos RC/RL, enfriamiento generalizado, modelos compartimentales.",
              "**Próxima lección:** **métodos de sustitución** — cambios de variable para reducir EDOs no lineales a separables o lineales.",
          ]),
    ]
    return {
        "id": "lec-ed-1-4-lineales",
        "title": "EDO lineales",
        "description": "Forma estándar $y' + P(x)y = Q(x)$, método del factor integrante $\\rho = e^{\\int P\\,dx}$, aplicaciones a problemas de mezclas y circuitos.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# =====================================================================
# 1.5 Métodos de Sustitución
# =====================================================================
def lesson_1_5():
    blocks = [
        b("texto", body_md=(
            "Cuando una EDO **no es separable ni lineal directamente**, frecuentemente se puede **transformar** en una "
            "que sí lo sea mediante un **cambio de variable** adecuado. Este es el espíritu de los **métodos de sustitución**.\n\n"
            "En esta lección estudiamos tres tipos clave de sustituciones:\n\n"
            "- **Argumentos lineales** (ej. $y' = (x + y + 3)^2$ — sustituimos $v = x + y + 3$).\n"
            "- **Ecuaciones homogéneas** (forma $y' = f(y/x)$ — sustituimos $v = y/x$).\n"
            "- **Ecuaciones de Bernoulli** (forma $y' + P(x)y = Q(x)y^n$ — sustituimos $v = y^{1-n}$).\n\n"
            "Al terminar:\n\n"
            "- Reconoces patrones que sugieren cada sustitución.\n"
            "- Aplicas la sustitución correcta para reducir a separable o lineal.\n"
            "- Resuelves la ecuación reducida y vuelves a la variable original."
        )),

        b("ejemplo_resuelto",
          titulo="Sustitución con argumento lineal",
          problema_md=(
              "Resolver $\\dfrac{dy}{dx} = (x + y + 3)^2$."
          ),
          pasos=[
              {"accion_md": (
                  "El lado derecho depende de la combinación lineal $x + y + 3$. Sustituimos $v = x + y + 3 \\Rightarrow y = v - x - 3$.\n\n"
                  "Derivando: $\\dfrac{dy}{dx} = \\dfrac{dv}{dx} - 1$."
              ),
               "justificacion_md": "Cuando una EDO involucra una expresión $ax + by + c$, esa combinación es la sustitución natural.",
               "es_resultado": False},
              {"accion_md": (
                  "Sustituyendo: $\\dfrac{dv}{dx} - 1 = v^2 \\Rightarrow \\dfrac{dv}{dx} = v^2 + 1$.\n\n"
                  "**Ahora es separable:** $\\dfrac{dv}{v^2 + 1} = dx$."
              ),
               "justificacion_md": "La sustitución redujo la EDO a una separable.",
               "es_resultado": False},
              {"accion_md": (
                  "Integrando: $\\arctan v = x + C \\Rightarrow v = \\tan(x + C)$.\n\n"
                  "Volviendo a $y$: $x + y + 3 = \\tan(x + C) \\Rightarrow y = \\tan(x + C) - x - 3$.\n\n"
                  "**Solución general:** $y(x) = \\tan(x + C) - x - 3$."
              ),
               "justificacion_md": "Integral elemental, luego despejar $y$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Ecuaciones homogéneas",
          body_md=(
              "Una EDO de la forma\n\n"
              "$$\\dfrac{dy}{dx} = f\\left(\\dfrac{y}{x}\\right)$$\n\n"
              "se llama **homogénea** (porque el lado derecho depende solo del cociente $y/x$, una función homogénea de grado $0$).\n\n"
              "**Sustitución:** $\\boxed{v = \\dfrac{y}{x} \\Rightarrow y = vx \\Rightarrow \\dfrac{dy}{dx} = v + x\\dfrac{dv}{dx}.}$\n\n"
              "Sustituyendo: $v + x\\dfrac{dv}{dx} = f(v) \\Rightarrow x\\dfrac{dv}{dx} = f(v) - v$, que es **separable** en $v$ y $x$:\n\n"
              "$\\dfrac{dv}{f(v) - v} = \\dfrac{dx}{x}.$\n\n"
              "**Cómo reconocer:** si los términos de la EDO tienen el mismo grado total en $x$ y $y$ (al considerar $y$ con grado 1, $x$ con grado 1), es homogénea."
          )),

        b("ejemplo_resuelto",
          titulo="EDO homogénea",
          problema_md=(
              "Resolver $2xy\\dfrac{dy}{dx} = 4x^2 + 3y^2$."
          ),
          pasos=[
              {"accion_md": (
                  "Dividir por $2xy$: $\\dfrac{dy}{dx} = \\dfrac{4x^2 + 3y^2}{2xy} = \\dfrac{2x}{y} + \\dfrac{3y}{2x} = 2\\left(\\dfrac{x}{y}\\right) + \\dfrac{3}{2}\\left(\\dfrac{y}{x}\\right).$\n\n"
                  "Es función de $y/x$ $\\Rightarrow$ homogénea."
              ),
               "justificacion_md": "El cociente $y/x$ es la única dependencia.",
               "es_resultado": False},
              {"accion_md": (
                  "Sustituir $y = vx$, $y' = v + xv'$:\n\n"
                  "$v + x\\dfrac{dv}{dx} = \\dfrac{2}{v} + \\dfrac{3v}{2} \\Rightarrow x\\dfrac{dv}{dx} = \\dfrac{2}{v} + \\dfrac{v}{2} = \\dfrac{4 + v^2}{2v}$.\n\n"
                  "Separar: $\\dfrac{2v\\,dv}{4 + v^2} = \\dfrac{dx}{x}$."
              ),
               "justificacion_md": "Tras sustituir, separamos variables en $v$ y $x$.",
               "es_resultado": False},
              {"accion_md": (
                  "Integrando: $\\ln(4 + v^2) = \\ln|x| + C \\Rightarrow 4 + v^2 = Kx$.\n\n"
                  "Volviendo a $y$ ($v = y/x$): $4 + \\dfrac{y^2}{x^2} = Kx \\Rightarrow y^2 = Kx^3 - 4x^2$.\n\n"
                  "**Solución general (implícita):** $y^2 = Kx^3 - 4x^2$."
              ),
               "justificacion_md": "**Patrón:** después de la sustitución, una integral elemental y luego sustituir de vuelta.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Ecuación de Bernoulli",
          body_md=(
              "Una EDO de la forma\n\n"
              "$$\\boxed{\\dfrac{dy}{dx} + P(x)\\,y = Q(x)\\,y^n}$$\n\n"
              "con $n \\neq 0, 1$ se llama **ecuación de Bernoulli**.\n\n"
              "**Sustitución:** $\\boxed{v = y^{1-n}.}$\n\n"
              "Esta sustitución transforma la Bernoulli en una **EDO lineal en $v$**:\n\n"
              "$\\dfrac{dv}{dx} + (1-n)P(x)\\,v = (1-n)Q(x).$\n\n"
              "**Casos especiales:**\n\n"
              "- $n = 0$: ya es lineal, no necesita sustitución.\n"
              "- $n = 1$: $y' + Py = Qy \\Rightarrow y' + (P-Q)y = 0$ — separable.\n"
              "- $n = 2, 3, 1/2$, etc.: aplicar la sustitución."
          )),

        b("ejemplo_resuelto",
          titulo="Ecuación de Bernoulli",
          problema_md=(
              "Resolver $x\\dfrac{dy}{dx} + 6y = 3xy^{4/3}$."
          ),
          pasos=[
              {"accion_md": (
                  "Forma estándar dividiendo por $x$: $\\dfrac{dy}{dx} + \\dfrac{6}{x}y = 3 y^{4/3}$. Es Bernoulli con $P = 6/x$, $Q = 3$, $n = 4/3$.\n\n"
                  "Sustitución: $v = y^{1 - 4/3} = y^{-1/3} \\Rightarrow y = v^{-3}, y' = -3v^{-4}v'$."
              ),
               "justificacion_md": "Identificar el exponente $n$ y aplicar la sustitución.",
               "es_resultado": False},
              {"accion_md": (
                  "Sustituyendo en la EDO:\n\n"
                  "$-3v^{-4}\\dfrac{dv}{dx} + \\dfrac{6}{x}v^{-3} = 3v^{-4}$.\n\n"
                  "Multiplicar por $-v^4/3$:\n\n"
                  "$\\dfrac{dv}{dx} - \\dfrac{2}{x}v = -1$. **EDO lineal en $v$.**"
              ),
               "justificacion_md": "El cambio convierte una Bernoulli en una lineal.",
               "es_resultado": False},
              {"accion_md": (
                  "Factor integrante: $\\rho = e^{\\int -2/x\\,dx} = x^{-2}$.\n\n"
                  "$(x^{-2}v)' = -x^{-2} \\Rightarrow x^{-2}v = x^{-1} + C \\Rightarrow v = x + Cx^2$.\n\n"
                  "Volver a $y$: $y^{-1/3} = x + Cx^2 \\Rightarrow y = (x + Cx^2)^{-3}$.\n\n"
                  "**Solución:** $y(x) = \\dfrac{1}{(x + Cx^2)^3}$."
              ),
               "justificacion_md": "Resolver la lineal con factor integrante y volver a la variable original.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para una EDO de Bernoulli $y' + Py = Qy^n$, la sustitución correcta es:",
                  "opciones_md": ["$v = y^n$", "$v = y/x$", "$v = y^{1-n}$", "$v = y'$"],
                  "correcta": "C",
                  "pista_md": "El exponente debe convertir la EDO en lineal.",
                  "explicacion_md": "**$v = y^{1-n}$.** Esta es la sustitución que linealiza la Bernoulli.",
              },
              {
                  "enunciado_md": "Una EDO $y' = f(y/x)$ se resuelve con la sustitución:",
                  "opciones_md": ["$v = y$", "**$v = y/x$**", "$v = xy$", "$v = y^2$"],
                  "correcta": "B",
                  "pista_md": "Si la EDO depende solo de $y/x$, esa combinación es la nueva variable natural.",
                  "explicacion_md": "**$v = y/x$.** Reduce la homogénea a separable.",
              },
              {
                  "enunciado_md": "Para $y' = (x - y)^2$, la sustitución natural es:",
                  "opciones_md": ["$v = x - y$", "$v = xy$", "$v = y/x$", "$v = y^2$"],
                  "correcta": "A",
                  "pista_md": "El argumento del cuadrado.",
                  "explicacion_md": "**$v = x - y$.** Para argumentos lineales $ax + by + c$, esa combinación es la sustitución natural.",
              },
          ]),

        ej(
            "Argumento lineal",
            "Resuelve $\\dfrac{dy}{dx} = (x + y)^2$.",
            ["Sustitución $v = x + y$."],
            (
                "$v = x + y \\Rightarrow v' = 1 + y' = 1 + v^2$.\n\n"
                "Separable: $\\dfrac{dv}{1 + v^2} = dx \\Rightarrow \\arctan v = x + C \\Rightarrow v = \\tan(x + C)$.\n\n"
                "**$y(x) = \\tan(x + C) - x$.**"
            ),
        ),

        ej(
            "Homogénea simple",
            "Resuelve $\\dfrac{dy}{dx} = \\dfrac{y}{x} + 1$.",
            ["Es de la forma $f(y/x)$: sustituir $v = y/x$."],
            (
                "$y = vx, y' = v + xv'$. Sustituyendo: $v + xv' = v + 1 \\Rightarrow xv' = 1 \\Rightarrow v' = 1/x$.\n\n"
                "Integrando: $v = \\ln|x| + C$. Volviendo: $y = x(\\ln|x| + C)$.\n\n"
                "**$y(x) = x\\ln|x| + Cx$.**"
            ),
        ),

        ej(
            "Bernoulli con $n = 2$",
            "Resuelve $\\dfrac{dy}{dx} + y = y^2$.",
            ["$n = 2$, $v = y^{-1}$."],
            (
                "$v = y^{-1} \\Rightarrow y = 1/v, y' = -v^{-2}v'$. Sustituyendo:\n\n"
                "$-v^{-2}v' + v^{-1} = v^{-2} \\Rightarrow$ multiplicar por $-v^2$: $v' - v = -1$.\n\n"
                "Lineal en $v$. $\\rho = e^{-x}$. $(e^{-x}v)' = -e^{-x} \\Rightarrow e^{-x}v = e^{-x} + C \\Rightarrow v = 1 + Ce^x$.\n\n"
                "**$y(x) = \\dfrac{1}{1 + Ce^x}$.**"
            ),
        ),

        fig(
            "Diagrama del cambio de variable v = y/x para EDOs homogéneas, en dos paneles. "
            "Izquierda: plano (x, y) con curva solución y(x) en teal #06b6d4 y rectas radiales grises desde el origen marcando la razón y/x. "
            "Flecha curva ámbar #f59e0b 'sustituir v = y/x' apunta al panel derecho. "
            "Derecha: plano (x, v) con la EDO transformada, ahora separable, y curvas solución en teal #06b6d4. "
            "Pie: 'la sustitución vuelve la EDO separable'. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**No reconocer el patrón antes de sustituir.** Tomarse tiempo para identificar la forma de la EDO.",
              "**Olvidar derivar la sustitución.** $v = y/x \\Rightarrow y' = v + xv'$, no solo $v'$.",
              "**Confundir Bernoulli con lineal.** $y' + Py = Q$ es lineal; $y' + Py = Qy^n$ con $n \\neq 0,1$ es Bernoulli.",
              "**No volver a la variable original.** El resultado final debe estar en términos de $y$, no de $v$.",
              "**Usar Bernoulli con $n=1$ esperando linealizar.** Para $n=1$, la EDO es separable directamente: $y' = (Q-P)y$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Argumentos lineales:** $v = ax + by + c$ reduce a separable.",
              "**Homogéneas:** $y' = f(y/x)$ con $v = y/x$ reduce a separable.",
              "**Bernoulli:** $y' + Py = Qy^n$ con $v = y^{1-n}$ reduce a lineal.",
              "**Estrategia:** identificar el patrón → aplicar sustitución → resolver la EDO transformada → volver a $y$.",
              "**Próxima lección:** **EDOs exactas** — método para EDOs con estructura de derivada total.",
          ]),
    ]
    return {
        "id": "lec-ed-1-5-sustitucion",
        "title": "Métodos de sustitución",
        "description": "Sustituciones para argumentos lineales, ecuaciones homogéneas ($v = y/x$) y ecuaciones de Bernoulli ($v = y^{1-n}$) que las reducen a separables o lineales.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 5,
    }


# =====================================================================
# 1.6 EDO Exactas
# =====================================================================
def lesson_1_6():
    blocks = [
        b("texto", body_md=(
            "Una **EDO exacta** es de la forma\n\n"
            "$$M(x, y)\\,dx + N(x, y)\\,dy = 0,$$\n\n"
            "donde el lado izquierdo es la **diferencial total** de una función $F(x, y)$:\n\n"
            "$$M = \\dfrac{\\partial F}{\\partial x}, \\quad N = \\dfrac{\\partial F}{\\partial y}.$$\n\n"
            "Si esto se cumple, la EDO equivale a $dF = 0$, cuya solución general es $F(x, y) = C$.\n\n"
            "**El problema se reduce a:**\n\n"
            "1. **Verificar la exactitud** con la condición $\\partial M/\\partial y = \\partial N/\\partial x$.\n"
            "2. **Encontrar $F$** integrando.\n"
            "3. **Escribir la solución** $F(x, y) = C$.\n\n"
            "Al terminar:\n\n"
            "- Reconoces EDOs exactas y verificas la condición de exactitud.\n"
            "- Construyes la función potencial $F(x, y)$ por integración parcial.\n"
            "- Escribes la solución implícita $F(x, y) = C$."
        )),

        b("definicion",
          titulo="EDO exacta y criterio",
          body_md=(
              "Una EDO de la forma\n\n"
              "$$M(x, y)\\,dx + N(x, y)\\,dy = 0$$\n\n"
              "es **exacta** si existe $F(x, y)$ tal que\n\n"
              "$$\\dfrac{\\partial F}{\\partial x} = M(x, y), \\qquad \\dfrac{\\partial F}{\\partial y} = N(x, y).$$\n\n"
              "**Criterio de exactitud (condición necesaria y suficiente, en regiones simplemente conexas):**\n\n"
              "$$\\boxed{\\dfrac{\\partial M}{\\partial y} = \\dfrac{\\partial N}{\\partial x}.}$$\n\n"
              "**Si la EDO es exacta**, su **solución general** es\n\n"
              "$$F(x, y) = C.$$\n\n"
              "**Cómo construir $F$:**\n\n"
              "1. Integra $M$ respecto a $x$: $F(x, y) = \\int M\\,dx + g(y)$.\n"
              "2. Deriva respecto a $y$ y compara con $N$: $\\dfrac{\\partial F}{\\partial y} = \\dfrac{\\partial}{\\partial y}\\int M\\,dx + g'(y) = N$, lo que despeja $g'(y)$.\n"
              "3. Integra $g'$ para obtener $g(y)$ y forma $F(x, y)$.\n"
              "4. La solución es $F(x, y) = C$."
          )),

        b("ejemplo_resuelto",
          titulo="EDO exacta sencilla",
          problema_md=(
              "Resolver $y^3\\,dx + 3xy^2\\,dy = 0$."
          ),
          pasos=[
              {"accion_md": (
                  "$M = y^3$, $N = 3xy^2$. Verificar exactitud:\n\n"
                  "$\\dfrac{\\partial M}{\\partial y} = 3y^2$, $\\dfrac{\\partial N}{\\partial x} = 3y^2$. **Iguales** → exacta."
              ),
               "justificacion_md": "Siempre verificar antes de aplicar el método.",
               "es_resultado": False},
              {"accion_md": (
                  "Integrar $M$ respecto a $x$: $F = \\int y^3\\,dx = xy^3 + g(y)$.\n\n"
                  "Derivar respecto a $y$: $\\dfrac{\\partial F}{\\partial y} = 3xy^2 + g'(y)$. Igualar a $N = 3xy^2$:\n\n"
                  "$3xy^2 + g'(y) = 3xy^2 \\Rightarrow g'(y) = 0 \\Rightarrow g(y) = $ constante."
              ),
               "justificacion_md": "$g$ se 'pierde' en la constante general.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:** $F(x, y) = xy^3 = C$."
              ),
               "justificacion_md": "Despejando $y$: $y = (C/x)^{1/3}$ (forma explícita opcional).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="EDO exacta más compleja",
          problema_md=(
              "Resolver $(6xy - y^3)\\,dx + (4y + 3x^2 - 3xy^2)\\,dy = 0$."
          ),
          pasos=[
              {"accion_md": (
                  "$M = 6xy - y^3$, $N = 4y + 3x^2 - 3xy^2$.\n\n"
                  "$\\dfrac{\\partial M}{\\partial y} = 6x - 3y^2$. $\\dfrac{\\partial N}{\\partial x} = 6x - 3y^2$. **Iguales** → exacta."
              ),
               "justificacion_md": "Verificación de exactitud.",
               "es_resultado": False},
              {"accion_md": (
                  "Integrar $M$ respecto a $x$:\n\n"
                  "$F = \\int (6xy - y^3)\\,dx = 3x^2 y - xy^3 + g(y)$.\n\n"
                  "Derivar respecto a $y$ y comparar con $N$:\n\n"
                  "$\\dfrac{\\partial F}{\\partial y} = 3x^2 - 3xy^2 + g'(y) = 4y + 3x^2 - 3xy^2 \\Rightarrow g'(y) = 4y \\Rightarrow g(y) = 2y^2$."
              ),
               "justificacion_md": "Aislar $g'(y)$ y luego integrar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:** $F(x, y) = 3x^2 y - xy^3 + 2y^2 = C$."
              ),
               "justificacion_md": "Solución implícita — no se puede despejar $y$ explícitamente sin ambigüedad.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El criterio de exactitud para $M\\,dx + N\\,dy = 0$ es:",
                  "opciones_md": [
                      "$M = N$",
                      "**$\\partial M/\\partial y = \\partial N/\\partial x$**",
                      "$\\partial M/\\partial x = \\partial N/\\partial y$",
                      "$M_x = N_y$",
                  ],
                  "correcta": "B",
                  "pista_md": "Las parciales 'cruzadas' deben coincidir.",
                  "explicacion_md": "**$\\partial M/\\partial y = \\partial N/\\partial x$.** Esta es la igualdad de las derivadas parciales mixtas de la $F$ que buscamos.",
              },
              {
                  "enunciado_md": "Si una EDO es exacta y construimos $F$ con $F(x,y) = C$, entonces $C$:",
                  "opciones_md": [
                      "Es siempre cero",
                      "Depende de la condición inicial",
                      "Es siempre 1",
                      "No existe",
                  ],
                  "correcta": "B",
                  "pista_md": "Constante de integración general.",
                  "explicacion_md": "**Depende de condición inicial.** $F(x,y) = C$ es solución general; la condición inicial fija $C$.",
              },
              {
                  "enunciado_md": "Para $(2x + y)\\,dx + (x + 2y)\\,dy = 0$, ¿es exacta?",
                  "opciones_md": ["Sí", "No", "No se puede decidir", "Solo si $x = y$"],
                  "correcta": "A",
                  "pista_md": "$\\partial(2x+y)/\\partial y = 1$, $\\partial(x+2y)/\\partial x = 1$.",
                  "explicacion_md": "**Sí.** Ambas parciales valen $1$, así que es exacta.",
              },
          ]),

        ej(
            "Verificar exactitud y resolver",
            "Resuelve $(2xy + 3)\\,dx + (x^2 - 1)\\,dy = 0$.",
            ["Verificar $\\partial M/\\partial y = \\partial N/\\partial x$, integrar $M$ respecto a $x$."],
            (
                "$M = 2xy + 3$, $N = x^2 - 1$. $M_y = 2x = N_x$ ✓ exacta.\n\n"
                "$F = \\int (2xy + 3)\\,dx = x^2 y + 3x + g(y)$. $F_y = x^2 + g'(y) = x^2 - 1 \\Rightarrow g'(y) = -1 \\Rightarrow g(y) = -y$.\n\n"
                "**$F(x, y) = x^2 y + 3x - y = C$.**"
            ),
        ),

        ej(
            "PVI exacto",
            "Resuelve $(2y - 3x^2)\\,dx + (2x - 4y^3)\\,dy = 0$, $y(0) = 1$.",
            ["Verificar exactitud, construir $F$, aplicar condición inicial."],
            (
                "$M_y = 2 = N_x$ ✓ exacta.\n\n"
                "$F = \\int (2y - 3x^2)\\,dx = 2xy - x^3 + g(y)$. $F_y = 2x + g'(y) = 2x - 4y^3 \\Rightarrow g'(y) = -4y^3 \\Rightarrow g = -y^4$.\n\n"
                "$F(x, y) = 2xy - x^3 - y^4 = C$. Condición $y(0) = 1$: $0 - 0 - 1 = C \\Rightarrow C = -1$.\n\n"
                "**Solución implícita:** $2xy - x^3 - y^4 = -1$, o $y^4 + x^3 - 2xy = 1$."
            ),
        ),

        ej(
            "EDO no exacta",
            "Verifica que $y\\,dx + 2x\\,dy = 0$ NO es exacta. (Sí se puede resolver por separación.)",
            ["Calcular las parciales cruzadas."],
            (
                "$M = y$, $N = 2x$. $M_y = 1$, $N_x = 2$. **No iguales → no exacta.**\n\n"
                "Pero es separable: $\\dfrac{dy}{y} = -\\dfrac{dx}{2x} \\Rightarrow \\ln|y| = -\\dfrac{1}{2}\\ln|x| + C \\Rightarrow y = K x^{-1/2}$, o $y\\sqrt{x} = K$.\n\n"
                "**Lección:** una EDO puede no ser exacta, pero ser separable o admitir un **factor integrante** que la haga exacta (técnica avanzada)."
            ),
        ),

        fig(
            "Diagrama de EDO exactas en el plano (x, y). Campo vectorial F = (M, N) representado por flechitas grises en una grilla, apuntando en la dirección del gradiente. "
            "Superpuestas, curvas de nivel F(x, y) = C de la función potencial en teal #06b6d4, cada una con su valor de C; las flechitas son perpendiculares a las curvas. "
            "Una curva solución particular destacada en ámbar #f59e0b. "
            "Pie: 'M dx + N dy = dF cuando ∂M/∂y = ∂N/∂x'. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar verificar exactitud.** El método de construcción de $F$ requiere que la EDO **sea** exacta.",
              "**Confundir $M$ y $N$.** $M$ es el coeficiente de $dx$, $N$ el de $dy$.",
              "**Olvidar la función $g(y)$ al integrar $M$ respecto a $x$.** Sin ella, perderías parte de $F$.",
              "**Despejar $y$ cuando la solución implícita es lo natural.** $F(x, y) = C$ es una respuesta válida.",
              "**Aplicar el método a EDOs que no son exactas** sin un factor integrante. Si falla la condición, el método no aplica directamente.",
          ]),

        b("resumen",
          puntos_md=[
              "**EDO exacta:** $M\\,dx + N\\,dy = 0$ con $\\partial M/\\partial y = \\partial N/\\partial x$.",
              "**Solución:** $F(x, y) = C$ donde $F$ es la función potencial.",
              "**Construcción:** integrar $M$ respecto a $x$, comparar derivada en $y$ con $N$ para hallar $g(y)$.",
              "**Si no es exacta:** revisa si es separable, lineal, Bernoulli, o admite factor integrante.",
              "**Próxima lección:** **EDOs reductibles** — EDOs de orden superior que se reducen a primer orden.",
          ]),
    ]
    return {
        "id": "lec-ed-1-6-exactas",
        "title": "EDO exactas",
        "description": "Condición de exactitud $\\partial M/\\partial y = \\partial N/\\partial x$, construcción de la función potencial $F(x, y)$, solución implícita $F(x, y) = C$.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 6,
    }


# =====================================================================
# 1.7 EDO Reductibles
# =====================================================================
def lesson_1_7():
    blocks = [
        b("texto", body_md=(
            "Aunque este capítulo se centra en **EDOs de primer orden**, vale la pena ver una técnica que "
            "permite **reducir EDOs de segundo orden** a primer orden mediante una sustitución adecuada. "
            "Estas son las **EDOs reductibles**.\n\n"
            "Hay dos casos clásicos:\n\n"
            "- **Falta la variable dependiente $y$:** $F(x, y', y'') = 0$ — sustituimos $p = y'$.\n"
            "- **Falta la variable independiente $x$:** $F(y, y', y'') = 0$ — sustituimos $p = y'$ pero tratando $p$ como función de $y$.\n\n"
            "Una vez reducida a primer orden, aplicamos los métodos del capítulo (separable, lineal, etc.). "
            "Después, una integración adicional recupera $y$.\n\n"
            "Al terminar:\n\n"
            "- Identificas EDOs de orden 2 reducibles.\n"
            "- Aplicas las sustituciones correctas según el caso.\n"
            "- Recuperas la solución original integrando."
        )),

        b("teorema",
          nombre="Caso 1: ausencia de la variable dependiente $y$",
          enunciado_md=(
              "Si la EDO de orden 2 tiene la forma $F(x, y', y'') = 0$ (no aparece $y$), sustituimos\n\n"
              "$$\\boxed{p = y' = \\dfrac{dy}{dx}, \\quad y'' = \\dfrac{dp}{dx}.}$$\n\n"
              "Esto reduce la EDO a una de **primer orden en $p$**: $F(x, p, p') = 0$.\n\n"
              "Una vez resuelta para $p(x)$, recuperamos $y$ por integración:\n\n"
              "$$y(x) = \\int p(x)\\,dx + C_2.$$"
          )),

        b("ejemplo_resuelto",
          titulo="Ausencia de $y$",
          problema_md=(
              "Resolver $xy'' + 2y' = 6x$."
          ),
          pasos=[
              {"accion_md": (
                  "No aparece $y$ explícitamente. Sustituir $p = y', y'' = p'$:\n\n"
                  "$xp' + 2p = 6x$.\n\n"
                  "Forma estándar: $p' + \\dfrac{2}{x}p = 6$. **Lineal en $p$.**"
              ),
               "justificacion_md": "La sustitución reduce orden y produce una lineal de primer orden.",
               "es_resultado": False},
              {"accion_md": (
                  "Factor integrante: $\\rho = e^{\\int 2/x\\,dx} = x^2$.\n\n"
                  "$(x^2 p)' = 6x^3 \\Rightarrow x^2 p = \\dfrac{3}{2}x^4 + C_1 \\Rightarrow p = \\dfrac{3}{2}x^2 + \\dfrac{C_1}{x^2}$.\n\n"
                  "Espera, recalculemos: $\\int 6x \\cdot x^2\\,dx = 6x^4/4 = 3x^4/2$? No, $6x^3$ sí. Hmm, mejor: $(x^2 p)' = x^2 \\cdot 6 = 6x^2$. Integrando: $x^2 p = 2x^3 + C_1 \\Rightarrow p = 2x + C_1/x^2$."
              ),
               "justificacion_md": "Cuidado: $\\rho \\cdot Q = x^2 \\cdot 6 = 6x^2$ (no $6x^3$).",
               "es_resultado": False},
              {"accion_md": (
                  "Recuperar $y$: $y = \\int p\\,dx = \\int (2x + C_1/x^2)\\,dx = x^2 - \\dfrac{C_1}{x} + C_2$.\n\n"
                  "**Solución general:** $y(x) = x^2 + \\dfrac{C_1'}{x} + C_2$ (renombrando $-C_1$ como $C_1'$)."
              ),
               "justificacion_md": "**Importante:** EDO de orden 2 → solución general con **dos** constantes.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Caso 2: ausencia de la variable independiente $x$",
          enunciado_md=(
              "Si la EDO de orden 2 tiene la forma $F(y, y', y'') = 0$ (no aparece $x$ explícita), sustituimos\n\n"
              "$$\\boxed{p = y', \\quad y'' = p\\dfrac{dp}{dy}.}$$\n\n"
              "Aquí tratamos a $p$ como **función de $y$** (no de $x$). La regla de la cadena da: $y'' = \\dfrac{dp}{dx} = \\dfrac{dp}{dy}\\dfrac{dy}{dx} = p\\dfrac{dp}{dy}$.\n\n"
              "Esto reduce la EDO a una de primer orden $F(y, p, p\\,dp/dy) = 0$ en términos de $p(y)$.\n\n"
              "Una vez resuelto $p$ como función de $y$, recuperamos $x$ por\n\n"
              "$$x = \\int \\dfrac{1}{p(y)}\\,dy + C_2.$$"
          )),

        b("ejemplo_resuelto",
          titulo="Ausencia de $x$",
          problema_md=(
              "Resolver $yy'' = (y')^2$."
          ),
          pasos=[
              {"accion_md": (
                  "No aparece $x$ explícito. Sustituir $p = y', y'' = p\\,dp/dy$:\n\n"
                  "$y \\cdot p\\dfrac{dp}{dy} = p^2 \\Rightarrow y\\dfrac{dp}{dy} = p$ (dividiendo por $p$, asumiendo $p \\neq 0$)."
              ),
               "justificacion_md": "La sustitución reduce a primer orden en $p$ y $y$.",
               "es_resultado": False},
              {"accion_md": (
                  "Separable: $\\dfrac{dp}{p} = \\dfrac{dy}{y} \\Rightarrow \\ln|p| = \\ln|y| + C_1 \\Rightarrow p = C_1 y$ (renombrando).\n\n"
                  "Recordando $p = y'$: $\\dfrac{dy}{dx} = C_1 y$. **Crecimiento exponencial.**"
              ),
               "justificacion_md": "Tras separar e integrar, queda otra EDO de primer orden separable.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolviendo: $y = Ae^{C_1 x}$ con $A = e^{C_2}$.\n\n"
                  "**Solución general:** $y(x) = Ae^{C_1 x}$ — dos constantes $A, C_1$ como esperado para orden 2."
              ),
               "justificacion_md": "**Lección:** la sustitución $y'' = p\\,dp/dy$ es muy útil para EDOs autónomas de orden 2.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para reducir $y'' + (y')^2 = e^x$ a primer orden, ¿qué sustitución conviene?",
                  "opciones_md": ["$p = y$", "**$p = y'$, con $y'' = dp/dx$**", "$p = y/x$", "$p = y^2$"],
                  "correcta": "B",
                  "pista_md": "Falta la variable dependiente $y$.",
                  "explicacion_md": "**$p = y'$, $y'' = dp/dx$.** El caso 'falta $y$' usa esta sustitución.",
              },
              {
                  "enunciado_md": "Para $y y'' + (y')^2 = 0$ (no aparece $x$), conviene:",
                  "opciones_md": [
                      "$p = y'$, $y'' = dp/dx$",
                      "**$p = y'$, $y'' = p\\,dp/dy$**",
                      "$p = y$",
                      "Es separable directamente",
                  ],
                  "correcta": "B",
                  "pista_md": "Falta la variable independiente $x$.",
                  "explicacion_md": "**$y'' = p\\,dp/dy$.** Tratar $p$ como función de $y$ vía regla de la cadena.",
              },
              {
                  "enunciado_md": "Una EDO de orden 2 tiene una solución general con:",
                  "opciones_md": ["$0$ constantes", "$1$ constante", "**$2$ constantes**", "$3$ constantes"],
                  "correcta": "C",
                  "pista_md": "Tantas constantes como el orden.",
                  "explicacion_md": "**$2$ constantes.** Cada integración aporta una constante. Por eso PVIs de orden 2 requieren 2 condiciones iniciales.",
              },
          ]),

        ej(
            "Falta $y$",
            "Resuelve $y'' = y'$.",
            ["Sustitución $p = y'$, $y'' = p'$."],
            (
                "$p' = p \\Rightarrow p = C_1 e^x$. $y = \\int p\\,dx = C_1 e^x + C_2$.\n\n"
                "**$y(x) = C_1 e^x + C_2$.**"
            ),
        ),

        ej(
            "Falta $x$",
            "Resuelve $y'' = (y')^2 / y$.",
            ["Caso 'falta $x$': $y'' = p\\,dp/dy$."],
            (
                "$p\\,dp/dy = p^2/y \\Rightarrow dp/dy = p/y \\Rightarrow$ separable: $dp/p = dy/y \\Rightarrow p = C_1 y$.\n\n"
                "$y' = C_1 y \\Rightarrow y = Ae^{C_1 x}$.\n\n"
                "**$y(x) = Ae^{C_1 x}$**, dos constantes."
            ),
        ),

        ej(
            "Falta $y$ con condiciones iniciales",
            "Resuelve $y'' = 2x$ con $y(0) = 1, y'(0) = 0$.",
            ["Integrar dos veces."],
            (
                "$y'' = 2x \\Rightarrow y' = x^2 + C_1$. $y'(0) = 0 \\Rightarrow C_1 = 0$.\n\n"
                "$y = x^3/3 + C_2$. $y(0) = 1 \\Rightarrow C_2 = 1$.\n\n"
                "**$y(x) = x^3/3 + 1$.**"
            ),
        ),

        fig(
            "Tres mini-paneles horizontales con los tipos de EDO reductibles. "
            "1 — Bernoulli: arriba y' + P(x)y = Q(x) y^n; flecha ámbar #f59e0b 'v = y^(1-n)' lleva abajo a una EDO lineal en v en teal #06b6d4. "
            "2 — Homogénea: EDO original y, tras v = y/x, EDO separable en v. "
            "3 — Reducción de orden: EDO de orden 2; tras p = y', EDO de orden 1 en p. "
            "Cada panel con título corto y flecha de transformación ámbar. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir las dos sustituciones.** Caso 1 (falta $y$): $y'' = dp/dx$. Caso 2 (falta $x$): $y'' = p\\,dp/dy$.",
              "**Olvidar que la solución general tiene 2 constantes** (orden 2).",
              "**Aplicar el método a EDOs donde $y$ y $x$ aparecen ambas explícitamente.** Ahí no aplica directamente — hay otros métodos en el cap. 2.",
              "**No volver a la variable original.** El resultado debe estar en términos de $y$ y $x$, no de $p$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Caso 1 (falta $y$):** $p = y', y'' = dp/dx$. Reduce a primer orden en $p(x)$.",
              "**Caso 2 (falta $x$):** $p = y', y'' = p\\,dp/dy$. Reduce a primer orden en $p(y)$.",
              "**Estrategia:** sustituir → resolver primer orden → recuperar $y$ por integración.",
              "**Solución general:** EDO de orden 2 → 2 constantes.",
              "**Próxima lección:** **modelos de población** — aplicación masiva de las técnicas vistas.",
          ]),
    ]
    return {
        "id": "lec-ed-1-7-reductibles",
        "title": "EDO reductibles",
        "description": "EDOs de orden 2 que se reducen a primer orden: caso 'falta $y$' ($p = y', y'' = dp/dx$) y caso 'falta $x$' ($y'' = p\\,dp/dy$).",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 7,
    }


# =====================================================================
# 1.8 Modelos de Población
# =====================================================================
def lesson_1_8():
    blocks = [
        b("texto", body_md=(
            "Los **modelos de población** son una de las aplicaciones más clásicas y poderosas de las EDOs "
            "de primer orden. Permiten **predecir la evolución** de poblaciones biológicas, propagación de "
            "rumores y enfermedades, dinámica de mercado y muchísimo más.\n\n"
            "Vamos a estudiar tres modelos en orden de complejidad creciente:\n\n"
            "1. **Crecimiento exponencial** $P' = rP$ (ya visto en lección 3 — sin restricciones).\n"
            "2. **Crecimiento hiperbólico** $P' = kP^2$ (sin tasa de mortalidad — explosión demográfica).\n"
            "3. **Ecuación logística** $P' = kP(M - P)$ — el modelo realista con **capacidad de carga** $M$.\n\n"
            "El modelo logístico es **fundamental** porque captura un fenómeno universal: el crecimiento "
            "se desacelera al acercarse a un límite natural impuesto por recursos, espacio o competencia.\n\n"
            "Al terminar:\n\n"
            "- Distingues los tres modelos y sus comportamientos cualitativos.\n"
            "- Resuelves la **ecuación logística** $P' = kP(M - P)$.\n"
            "- Identificas la **capacidad de carga** $M$ y predices el comportamiento asintótico.\n"
            "- Aplicas el modelo a problemas reales (epidemias, propagación de información)."
        )),

        b("definicion",
          titulo="Tres modelos clásicos",
          body_md=(
              "**Modelo 1 — crecimiento exponencial (sin restricciones):**\n\n"
              "$\\dfrac{dP}{dt} = rP \\Rightarrow P(t) = P_0 e^{rt}$.\n\n"
              "Crece (o decrece) sin límite. Apropiado para tiempos cortos o poblaciones pequeñas.\n\n"
              "**Modelo 2 — crecimiento hiperbólico:**\n\n"
              "$\\dfrac{dP}{dt} = kP^2$.\n\n"
              "Solución (separable): $P(t) = \\dfrac{P_0}{1 - kP_0 t}$. **Explota en tiempo finito** $t^* = 1/(kP_0)$. Modelo poco realista — solo para detectar crecimiento desbocado.\n\n"
              "**Modelo 3 — ecuación logística:**\n\n"
              "$\\boxed{\\dfrac{dP}{dt} = kP(M - P)}$ con $k, M > 0$.\n\n"
              "$M$ es la **capacidad de carga** o **población límite**. Es el modelo más utilizado en biología, ecología y epidemiología."
          )),

        b("teorema",
          nombre="Solución de la ecuación logística",
          enunciado_md=(
              "La solución del PVI $\\dfrac{dP}{dt} = kP(M - P), \\quad P(0) = P_0$ es\n\n"
              "$$\\boxed{P(t) = \\dfrac{M P_0}{P_0 + (M - P_0)e^{-kMt}}.}$$\n\n"
              "**Comportamiento asintótico:** $\\lim_{t\\to\\infty} P(t) = M$ (independientemente de $P_0$, siempre que $P_0 > 0$).\n\n"
              "**Forma de la curva (logística o sigmoide):**\n\n"
              "- Si $0 < P_0 < M$: $P$ crece monótonamente hacia $M$, con punto de inflexión en $P = M/2$.\n"
              "- Si $P_0 > M$: $P$ decrece monótonamente hacia $M$.\n"
              "- $P_0 = 0$ y $P_0 = M$ son **soluciones de equilibrio**: $P(t) \\equiv 0$ (inestable) y $P(t) \\equiv M$ (estable)."
          ),
          demostracion_md=(
              "Es separable: $\\dfrac{dP}{P(M-P)} = k\\,dt$. Por fracciones parciales,\n\n"
              "$\\dfrac{1}{P(M-P)} = \\dfrac{1}{M}\\left(\\dfrac{1}{P} + \\dfrac{1}{M-P}\\right)$.\n\n"
              "Integrando: $\\dfrac{1}{M}\\ln\\left|\\dfrac{P}{M-P}\\right| = kt + C_1$. Despejando $P$ y aplicando $P(0) = P_0$ se llega a la fórmula. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Predicción de población humana",
          problema_md=(
              "En 1885 cierto país tenía $50$ millones de habitantes y crecía a $750\\,000$/año. En 1940 tenía $100$ millones y crecía a $1$ millón/año. Asumiendo modelo logístico, halla la capacidad límite $M$ y la población estimada para el año $2000$."
          ),
          pasos=[
              {"accion_md": (
                  "$P' = kP(M - P)$. Con datos:\n\n"
                  "Año 1885: $P = 50, P' = 0.75 \\Rightarrow 0.75 = 50k(M - 50)$.\n\n"
                  "Año 1940: $P = 100, P' = 1.00 \\Rightarrow 1.00 = 100k(M - 100)$."
              ),
               "justificacion_md": "Dos ecuaciones, dos incógnitas $k, M$.",
               "es_resultado": False},
              {"accion_md": (
                  "Dividiendo: $\\dfrac{0.75}{1.00} = \\dfrac{50(M-50)}{100(M-100)} \\Rightarrow 0.75 = \\dfrac{M-50}{2(M-100)}$.\n\n"
                  "Despejando: $1.5(M-100) = M - 50 \\Rightarrow 1.5M - 150 = M - 50 \\Rightarrow 0.5M = 100 \\Rightarrow M = 200$ millones.\n\n"
                  "Sustituyendo: $1 = 100k(100) \\Rightarrow k = 10^{-4}$."
              ),
               "justificacion_md": "Resolver el sistema simultáneamente.",
               "es_resultado": False},
              {"accion_md": (
                  "Tomando $t = 0$ en 1940 ($P_0 = 100$), evaluamos en $t = 60$ (año 2000):\n\n"
                  "$P(60) = \\dfrac{200 \\cdot 100}{100 + (200 - 100)e^{-10^{-4} \\cdot 200 \\cdot 60}} = \\dfrac{20000}{100 + 100 e^{-1.2}} = \\dfrac{20000}{100(1 + e^{-1.2})} \\approx \\dfrac{200}{1 + 0.3012} \\approx 153.7$ millones.\n\n"
                  "**$\\approx 153.7$ millones de habitantes en 2000.**"
              ),
               "justificacion_md": "La población se acerca asintóticamente a $M = 200$ millones.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Aplicaciones del modelo logístico",
          body_md=(
              "El modelo $P' = kP(M - P)$ aparece en **muchos contextos** distintos:\n\n"
              "**1. Crecimiento poblacional con recursos limitados:** $M$ = capacidad de carga del entorno.\n\n"
              "**2. Competencia intraespecífica:** $\\delta = \\alpha P$ (mortalidad proporcional a la población) con $M = \\beta/\\alpha$.\n\n"
              "**3. Propagación de enfermedades (modelo SI simplificado):** $P$ = infectados, $M - P$ = susceptibles, contagios proporcionales a encuentros entre ambos grupos.\n\n"
              "**4. Difusión de información o rumores:** $P$ = personas que saben, $M - P$ = personas que no saben, rumores se transmiten por encuentros.\n\n"
              "**5. Adopción de tecnología:** la curva sigmoide (S-curve) que describe penetración de mercado.\n\n"
              "**Mensaje:** la ecuación logística es **omnipresente** porque captura un patrón universal: el crecimiento se acelera al inicio y desacelera al saturarse el sistema."
          )),

        b("ejemplo_resuelto",
          titulo="Propagación de un rumor",
          problema_md=(
              "En una ciudad de $100\\,000$ habitantes, $10\\,000$ saben un rumor. Una semana después, lo saben $20\\,000$. ¿Cuándo lo sabrá el $80\\%$ de la ciudad?"
          ),
          pasos=[
              {"accion_md": (
                  "Modelo logístico con $M = 100\\,000$ (mil personas), $P_0 = 10\\,000$. La solución es:\n\n"
                  "$P(t) = \\dfrac{1000}{10 + 90 e^{-100kt}}$ (en miles).\n\n"
                  "Determinar $k$ con $P(1) = 20$:\n\n"
                  "$20 = \\dfrac{1000}{10 + 90 e^{-100k}} \\Rightarrow 10 + 90 e^{-100k} = 50 \\Rightarrow e^{-100k} = 4/9 \\Rightarrow k = \\dfrac{1}{100}\\ln(9/4) \\approx 0.00811$."
              ),
               "justificacion_md": "Calibrar el modelo con los datos.",
               "es_resultado": False},
              {"accion_md": (
                  "$80\\% = 80\\,000 = 80$ (en miles). Resolver:\n\n"
                  "$80 = \\dfrac{1000}{10 + 90 e^{-100kt}} \\Rightarrow 10 + 90 e^{-100kt} = 12.5 \\Rightarrow e^{-100kt} = 1/36$.\n\n"
                  "$t = \\dfrac{\\ln 36}{100k} = \\dfrac{\\ln 36}{\\ln(9/4)} \\approx 4.42$ semanas."
              ),
               "justificacion_md": "Despejar tiempo dado el porcentaje deseado.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aproximadamente $4$ semanas y $3$ días** para que el rumor llegue al $80\\%$ de la ciudad.\n\n"
                  "**Patrón sigmoide:** lento al principio (pocos saben → pocos contagios), rápido al medio (muchos saben → muchos contagios a susceptibles), lento al final (pocos quedan por enterarse)."
              ),
               "justificacion_md": "Resultado interpretable.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "En la ecuación logística $P' = kP(M - P)$, $M$ representa:",
                  "opciones_md": [
                      "La población inicial",
                      "**La capacidad de carga** (límite asintótico)",
                      "La tasa de crecimiento",
                      "Una constante arbitraria",
                  ],
                  "correcta": "B",
                  "pista_md": "$M$ es donde la solución se estabiliza.",
                  "explicacion_md": "**Capacidad de carga.** $\\lim_{t\\to\\infty}P(t) = M$ (siempre que $P_0 > 0$).",
              },
              {
                  "enunciado_md": "El crecimiento exponencial $P' = rP$ con $r > 0$ es realista para:",
                  "opciones_md": [
                      "Tiempos largos sin importar el contexto",
                      "**Tiempos cortos o poblaciones pequeñas, sin saturación**",
                      "Poblaciones cercanas a la capacidad de carga",
                      "Cualquier modelo biológico",
                  ],
                  "correcta": "B",
                  "pista_md": "Sin restricciones, crece sin límite.",
                  "explicacion_md": "**Solo a corto plazo.** A largo plazo, los recursos se agotan y el modelo logístico se vuelve más apropiado.",
              },
              {
                  "enunciado_md": "El crecimiento hiperbólico $P' = kP^2$:",
                  "opciones_md": [
                      "Se estabiliza en $M$",
                      "Decrece a $0$",
                      "**Explota en tiempo finito**",
                      "Es lineal en $t$",
                  ],
                  "correcta": "C",
                  "pista_md": "Solución $P = P_0/(1 - kP_0 t)$ tiene singularidad.",
                  "explicacion_md": "**Explota** en $t^* = 1/(kP_0)$. Modelo no realista a largo plazo, pero útil para diagnosticar crecimiento desbocado.",
              },
          ]),

        ej(
            "Crecimiento exponencial corto plazo",
            "Una población de bacterias inicialmente de $100$ se duplica en $2$ horas. ¿Cuánto tarda en llegar a $1\\,000$?",
            ["$P = 100 e^{rt}$, hallar $r$ con duplicación, despejar $t$."],
            (
                "$P(2) = 200 \\Rightarrow e^{2r} = 2 \\Rightarrow r = \\ln 2/2$.\n\n"
                "$1000 = 100 e^{rt} \\Rightarrow e^{rt} = 10 \\Rightarrow t = \\ln 10/r = 2\\ln 10/\\ln 2 \\approx 6.64$ horas."
            ),
        ),

        ej(
            "Logística con condición inicial",
            "Resuelve $P' = 0.1 P(50 - P)$, $P(0) = 5$. ¿Cuándo se alcanza $P = 25$?",
            ["Aplicar fórmula logística con $M = 50, P_0 = 5, k = 0.1$."],
            (
                "$P(t) = \\dfrac{50 \\cdot 5}{5 + 45 e^{-0.1 \\cdot 50 \\cdot t}} = \\dfrac{250}{5 + 45 e^{-5t}}$.\n\n"
                "$P = 25 \\Rightarrow 5 + 45 e^{-5t} = 10 \\Rightarrow e^{-5t} = 1/9 \\Rightarrow t = \\ln 9/5 \\approx 0.439$.\n\n"
                "(En unidades de $t$. El $25 = M/2$ es justo el punto de inflexión de la sigmoide.)"
            ),
        ),

        ej(
            "Capacidad de carga asintótica",
            "Si $P(t)$ satisface la logística con $M = 1000$ y $P(0) = 100$, ¿qué se puede decir de $\\lim_{t\\to\\infty}P(t)$?",
            ["Comportamiento asintótico de la logística."],
            (
                "$\\lim_{t\\to\\infty}P(t) = M = 1000$, sin importar el valor exacto de $k$ (mientras $k > 0$).\n\n"
                "**Razonamiento:** $M$ es el equilibrio estable. Cualquier $P_0 > 0$ se acerca a él."
            ),
        ),

        fig(
            "Comparación de tres modelos de población en un plano (t, P). "
            "Curva 1 — exponencial puro P = P0 e^(kt) en gris, subiendo sin techo. "
            "Curva 2 — logística en teal #06b6d4 con forma de S que se aplana al acercarse a la capacidad de carga K, trazada como línea horizontal punteada en ámbar #f59e0b. "
            "Curva 3 — modelo con cosecha P' = rP(1 - P/K) - h, en teal con un punto de equilibrio destacado. "
            "Leyenda con los tres modelos. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar el modelo exponencial cuando hay claras restricciones de recursos.** A largo plazo siempre subestima por defecto.",
              "**Confundir $M$ con $P_0$.** $M$ es la capacidad límite (asíntota), $P_0$ es el valor inicial.",
              "**Olvidar verificar el signo de $M - P_0$.** Si $P_0 > M$, la solución decrece hacia $M$ (no crece).",
              "**No usar fracciones parciales** al separar variables en la logística — la integración fácil pasa por ahí.",
              "**Pensar que el modelo logístico es solo para biología.** Aplicaciones: rumores, ventas, adopción tecnológica, epidemias, etc.",
          ]),

        b("resumen",
          puntos_md=[
              "**Exponencial** $P' = rP$: sin restricciones, crece sin límite — solo realista a corto plazo.",
              "**Hiperbólico** $P' = kP^2$: explota en tiempo finito — modelo extremo.",
              "**Logístico** $P' = kP(M-P)$: el modelo más realista con capacidad de carga $M$.",
              "**Solución logística:** $P(t) = \\dfrac{MP_0}{P_0 + (M-P_0)e^{-kMt}}$.",
              "**Asintóticamente** $P(t) \\to M$ para todo $P_0 > 0$.",
              "**Aplicaciones universales:** poblaciones, epidemias, rumores, adopción tecnológica.",
              "**Próxima lección:** **estabilidad** — análisis cualitativo de soluciones de equilibrio.",
          ]),
    ]
    return {
        "id": "lec-ed-1-8-modelos-poblacion",
        "title": "Modelos de población",
        "description": "Crecimiento exponencial, hiperbólico y logístico $P' = kP(M-P)$, capacidad de carga $M$, aplicaciones (epidemias, propagación de rumores).",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 8,
    }


# =====================================================================
# 1.9 Estabilidad
# =====================================================================
def lesson_1_9():
    blocks = [
        b("texto", body_md=(
            "Cuando una EDO no se puede resolver explícitamente, **el análisis cualitativo** se vuelve indispensable. "
            "**¿Las soluciones se acercan a un valor fijo? ¿Se alejan? ¿Cómo afecta la condición inicial al comportamiento a largo plazo?**\n\n"
            "Estas preguntas se responden estudiando los **puntos de equilibrio** y su **estabilidad**.\n\n"
            "Para una EDO **autónoma** $\\dfrac{dx}{dt} = f(x)$:\n\n"
            "- Un **punto de equilibrio** es un valor $x^*$ donde $f(x^*) = 0$. La función constante $x(t) \\equiv x^*$ es solución.\n"
            "- $x^*$ es **estable** si pequeñas perturbaciones decrecen y la solución vuelve al equilibrio.\n"
            "- $x^*$ es **inestable** si pequeñas perturbaciones se amplifican.\n\n"
            "Este análisis es la base de:\n\n"
            "- **Ecología y biología:** poblaciones que se estabilizan o colapsan.\n"
            "- **Mecánica:** posiciones de equilibrio (estables vs. inestables).\n"
            "- **Economía:** equilibrios de mercado.\n"
            "- **Sistemas dinámicos en general.**\n\n"
            "Al terminar:\n\n"
            "- Identificas puntos de equilibrio resolviendo $f(x) = 0$.\n"
            "- Determinas estabilidad analizando el signo de $f$ alrededor del equilibrio.\n"
            "- Construyes un **diagrama de fase** unidimensional."
        )),

        b("definicion",
          titulo="Solución de equilibrio y estabilidad",
          body_md=(
              "Sea la EDO autónoma $\\dfrac{dx}{dt} = f(x)$.\n\n"
              "Un **punto de equilibrio** (o punto crítico) es $x^* \\in \\mathbb{R}$ con $f(x^*) = 0$. La función constante $x(t) \\equiv x^*$ es **solución de equilibrio**.\n\n"
              "**Clasificación según estabilidad:**\n\n"
              "- **Estable** (atractor): toda solución que comienza cerca de $x^*$ converge a $x^*$ cuando $t \\to \\infty$.\n"
              "- **Inestable** (repulsor): toda solución que comienza cerca pero distinta de $x^*$ se aleja.\n"
              "- **Semiestable**: atrae por un lado y repele por el otro.\n\n"
              "**Criterio del signo:** En una vecindad de $x^*$:\n\n"
              "- Si $f(x) > 0$ a la izquierda de $x^*$ y $f(x) < 0$ a la derecha → **estable** (las trayectorias 'apuntan hacia' $x^*$).\n"
              "- Si $f(x) < 0$ a la izquierda y $f(x) > 0$ a la derecha → **inestable**.\n\n"
              "**Criterio analítico (cuando $f$ es derivable):**\n\n"
              "- $f'(x^*) < 0$ → **estable**.\n"
              "- $f'(x^*) > 0$ → **inestable**.\n"
              "- $f'(x^*) = 0$: análisis adicional (criterio del signo)."
          )),

        b("ejemplo_resuelto",
          titulo="Ley de enfriamiento de Newton — equilibrio estable",
          problema_md=(
              "Analiza la estabilidad de los equilibrios de $\\dfrac{dx}{dt} = -k(x - A)$ con $k, A > 0$ (enfriamiento de Newton)."
          ),
          pasos=[
              {"accion_md": (
                  "Equilibrios: $-k(x - A) = 0 \\Rightarrow x^* = A$ (única solución).\n\n"
                  "Es decir, **la temperatura ambiente $A$ es el único equilibrio**."
              ),
               "justificacion_md": "Resolver $f(x) = 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "Análisis del signo:\n\n"
                  "- Si $x > A$: $f(x) = -k(x - A) < 0$ → $x$ decrece → se aproxima a $A$.\n"
                  "- Si $x < A$: $f(x) > 0$ → $x$ crece → se aproxima a $A$.\n\n"
                  "**$x^* = A$ es estable** (atractor)."
              ),
               "justificacion_md": "Criterio del signo: trayectorias apuntan hacia $A$ desde ambos lados.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación analítica:** $f'(x) = -k < 0$ → confirma estabilidad.\n\n"
                  "**Solución explícita** (ya vista): $x(t) = A + (x_0 - A)e^{-kt}$. $\\lim_{t\\to\\infty} x(t) = A$ ✓.\n\n"
                  "**Lectura física:** todo objeto tiende a la temperatura ambiente sin importar su temperatura inicial."
              ),
               "justificacion_md": "**Patrón general:** los modelos lineales $x' = -k(x - A)$ tienen equilibrio estable en $A$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Ecuación logística — dos equilibrios",
          problema_md=(
              "Analiza los equilibrios de la ecuación logística $\\dfrac{dx}{dt} = kx(M - x)$ con $k, M > 0$."
          ),
          pasos=[
              {"accion_md": (
                  "Equilibrios: $kx(M - x) = 0 \\Rightarrow x^* = 0$ o $x^* = M$.\n\n"
                  "**Dos equilibrios:** la población nula y la capacidad de carga."
              ),
               "justificacion_md": "Soluciones de $f(x) = 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "Signo de $f(x) = kx(M - x)$:\n\n"
                  "- $x < 0$: $f < 0$ (no físico para población, pero matemáticamente, $x$ decrece).\n"
                  "- $0 < x < M$: $f > 0$ → $x$ crece.\n"
                  "- $x > M$: $f < 0$ → $x$ decrece.\n\n"
                  "**$x^* = 0$:** signo cambia de $-$ a $+$ → **inestable** (extinción es repulsor).\n\n"
                  "**$x^* = M$:** signo cambia de $+$ a $-$ → **estable** (atractor)."
              ),
               "justificacion_md": "Análisis sistemático del signo de $f$ en cada región.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación analítica:** $f'(x) = kM - 2kx$. $f'(0) = kM > 0$ (inestable) ✓. $f'(M) = -kM < 0$ (estable) ✓.\n\n"
                  "**Diagrama de fase:**\n\n"
                  "```\n"
                  "x' < 0    x' > 0    x' < 0\n"
                  "←-------●--------●-------→\n"
                  "        0        M\n"
                  "    inestable   estable\n"
                  "```\n\n"
                  "**Conclusión:** toda población inicial $P_0 \\in (0, M] \\cup (M, \\infty)$ converge a $M$."
              ),
               "justificacion_md": "**Lección:** el diagrama de fase resume el comportamiento de **todas** las soluciones sin resolver la EDO.",
               "es_resultado": True},
          ]),

        fig(
            "Diagrama de fase de la ecuación logística dx/dt = kx(M - x). "
            "Línea horizontal con dos puntos marcados: x=0 (etiquetado 'inestable', círculo abierto) y x=M (etiquetado 'estable', círculo cerrado). "
            "Flechas en el eje: hacia la izquierda en x<0 (alejándose de 0), hacia la derecha en 0<x<M (alejándose de 0, acercándose a M), hacia la izquierda en x>M (acercándose a M). "
            "Por encima de la línea, varias curvas solución x(t) vs t en color teal #06b6d4: una que decrece desde x>M hacia M, otra que crece desde 0<x<M hacia M (sigmoide), una que diverge negativa desde x<0. "
            "Etiquetas claras para 'x=M' (asíntota horizontal) y 'x=0'. " + STYLE
        ),

        b("intuicion", body_md=(
            "**Interpretación física de la estabilidad.**\n\n"
            "Imagina una bola en un paisaje de colinas y valles, con la coordenada $x$ como su posición horizontal y $f(x)$ como la fuerza horizontal (proporcional al negativo de la pendiente del paisaje):\n\n"
            "- **Equilibrio estable** = fondo de un valle. Si empujas la bola un poco, vuelve.\n"
            "- **Equilibrio inestable** = cima de una colina. Cualquier perturbación la hace caer.\n"
            "- **Semiestable** = punto de inflexión.\n\n"
            "**En la práctica:** los equilibrios estables son los que **observas** en sistemas reales (las cimas son raras de mantener). El análisis de estabilidad predice qué configuraciones son **persistentes**."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para la EDO $x' = x^2 - 1$, los puntos de equilibrio son:",
                  "opciones_md": ["$x = 0$", "$x = \\pm 1$", "$x = 1$ solo", "No tiene"],
                  "correcta": "B",
                  "pista_md": "Resolver $x^2 - 1 = 0$.",
                  "explicacion_md": "**$x = \\pm 1$.** $x^2 = 1$ tiene dos soluciones reales.",
              },
              {
                  "enunciado_md": "Si $f'(x^*) < 0$, el equilibrio $x^*$ es:",
                  "opciones_md": ["Inestable", "**Estable**", "Semiestable", "Indeterminado"],
                  "correcta": "B",
                  "pista_md": "Criterio analítico de estabilidad.",
                  "explicacion_md": "**Estable.** $f' < 0$ significa que $f$ decrece al pasar por $x^*$, lo que es exactamente la condición para atractor.",
              },
              {
                  "enunciado_md": "Para la logística $x' = kx(M-x)$, $x = 0$ es:",
                  "opciones_md": ["Estable", "**Inestable**", "Semiestable", "No es equilibrio"],
                  "correcta": "B",
                  "pista_md": "$f'(0) = kM > 0$.",
                  "explicacion_md": "**Inestable.** Pequeñas poblaciones positivas crecen alejándose de $0$ hacia $M$.",
              },
          ]),

        ej(
            "Equilibrios y estabilidad",
            "Halla los equilibrios y clasifica su estabilidad para $x' = x^3 - x$.",
            ["Equilibrios donde $f = 0$. Signo o derivada para clasificar."],
            (
                "$x^3 - x = x(x^2 - 1) = x(x-1)(x+1) = 0 \\Rightarrow x = 0, 1, -1$.\n\n"
                "$f'(x) = 3x^2 - 1$. $f'(0) = -1 < 0$ → **estable**. $f'(1) = 2 > 0$ → **inestable**. $f'(-1) = 2 > 0$ → **inestable**.\n\n"
                "**Diagrama de fase:** ←(estable)←-1→(inestable)→0←(estable)←1→(inestable)→. Esperar: revisar signos."
            ),
        ),

        ej(
            "Aplicación: caída con resistencia",
            "Un objeto cae con $v' = g - kv^2$ ($g, k > 0$, fuerza gravitacional menos resistencia cuadrática). Halla la velocidad terminal y su estabilidad.",
            ["Velocidad terminal donde $v' = 0$."],
            (
                "$g - kv^2 = 0 \\Rightarrow v_T = \\sqrt{g/k}$ (única solución física, $v > 0$).\n\n"
                "$f'(v) = -2kv$. $f'(v_T) = -2k\\sqrt{g/k} = -2\\sqrt{gk} < 0 \\Rightarrow$ **estable**.\n\n"
                "**Interpretación:** todo objeto cayendo se acerca a $v_T$. Por eso skydivers alcanzan velocidad terminal."
            ),
        ),

        ej(
            "Bifurcación implícita",
            "Para $x' = x^2 - a$ con $a$ parámetro, ¿qué equilibrios hay según el signo de $a$? Discute estabilidad.",
            ["Casos $a > 0, a = 0, a < 0$."],
            (
                "**$a > 0$:** $x = \\pm\\sqrt{a}$. $f'(x) = 2x$. $f'(\\sqrt{a}) > 0$ inestable. $f'(-\\sqrt{a}) < 0$ estable.\n\n"
                "**$a = 0$:** único equilibrio $x = 0$ con $f'(0) = 0$. Mirar signo: $f(x) = x^2 \\geq 0$, así $x' \\geq 0$ siempre → **semiestable** (atrae por izquierda, repele por derecha).\n\n"
                "**$a < 0$:** **no hay equilibrios reales** ($x^2 - a > 0$ siempre, $x' > 0$, todo crece).\n\n"
                "**Bifurcación silla-nodo en $a = 0$:** los dos equilibrios colapsan y desaparecen al pasar $a$ por $0$. Fenómeno fundamental en sistemas dinámicos."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar que la estabilidad solo aplica a EDOs autónomas.** Si aparece $t$ explícito, el análisis es más complejo.",
              "**Aplicar el criterio $f'(x^*) < 0$ cuando $f'(x^*) = 0$.** En ese caso, hay que mirar el signo de $f$ directamente.",
              "**Confundir 'punto de equilibrio' con 'solución general'.** Los equilibrios son **soluciones constantes**.",
              "**No considerar todos los equilibrios.** Algunas EDOs tienen muchos (o infinitos).",
              "**Pensar que un equilibrio inestable nunca se alcanza.** Sí se alcanza si la condición inicial es **exactamente** $x^*$ — pero cualquier perturbación lo aleja.",
          ]),

        b("resumen",
          puntos_md=[
              "**Punto de equilibrio:** $f(x^*) = 0$. Solución constante $x \\equiv x^*$.",
              "**Estable** (atractor): perturbaciones decrecen. **Inestable** (repulsor): perturbaciones crecen.",
              "**Criterio del signo:** mirar $f$ en una vecindad de $x^*$.",
              "**Criterio analítico:** $f'(x^*) < 0$ estable, $f'(x^*) > 0$ inestable, $= 0$ requiere análisis adicional.",
              "**Diagrama de fase:** representación visual completa del comportamiento cualitativo.",
              "**Cierre del capítulo:** Hemos cubierto las técnicas centrales para EDOs de primer orden — separables, lineales, sustituciones, exactas, reductibles, modelado y análisis cualitativo.",
              "**Próximo capítulo:** **EDO de orden superior** — generalización a $y'' + ay' + by = f(x)$, vibraciones mecánicas y oscilaciones.",
          ]),
    ]
    return {
        "id": "lec-ed-1-9-estabilidad",
        "title": "Estabilidad",
        "description": "Soluciones de equilibrio en EDOs autónomas, criterios de estabilidad (signo de $f$ y $f'(x^*)$), diagramas de fase.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 9,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "ecuaciones-diferenciales"

    course_doc = {
        "id": course_id,
        "title": "Ecuaciones Diferenciales",
        "description": (
            "EDOs de primer orden, EDOs de orden superior, sistemas de ecuaciones diferenciales y "
            "transformada de Laplace. Modelación de fenómenos físicos, biológicos y económicos."
        ),
        "category": "Matemáticas",
        "level": "Avanzado",
        "modules_count": 4,
        "rating": 4.8,
        "summary": "Curso completo de ecuaciones diferenciales para alumnos universitarios chilenos.",
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

    chapter_id = "ch-ed-edo-primer-orden"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "EDO de Primer Orden",
        "description": (
            "Definiciones y clasificación; soluciones, PVI y teorema de existencia y unicidad; "
            "métodos de resolución (separables, lineales, sustituciones, exactas, reductibles); "
            "modelos de población y análisis de estabilidad."
        ),
        "order": 1,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_1_1, lesson_1_2, lesson_1_3, lesson_1_4, lesson_1_5,
                lesson_1_6, lesson_1_7, lesson_1_8, lesson_1_9]
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
        f"✅ Capítulo 1 — EDO de Primer Orden listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
