"""
Seed del curso Ecuaciones Diferenciales — Capítulo 3: Sistemas de Ecuaciones Diferenciales.

Crea el capítulo 'Sistemas de Ecuaciones Diferenciales' bajo el curso 'ecuaciones-diferenciales'
y siembra sus 6 lecciones:

  - Sistemas lineales de primer orden
  - Soluciones de un sistema lineal
  - Método de valores propios
  - Matriz fundamental
  - Sistemas no homogéneos
  - Estabilidad

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
# Sistemas lineales de primer orden
# =====================================================================
def lesson_sistemas_lineales():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora trabajamos con **una sola función desconocida** $y(x)$. Pero la mayoría de los "
            "sistemas reales involucra **varias funciones acopladas** que evolucionan juntas: "
            "concentraciones de dos o más químicos en reacción, posiciones de varias masas conectadas, "
            "voltajes en distintos nodos de un circuito, poblaciones de presa y depredador, etc.\n\n"
            "Eso lleva al concepto de **sistema de ecuaciones diferenciales**. En este capítulo nos "
            "concentramos en el caso **lineal** y de **primer orden**, que se escribe muy compacto en "
            "**forma matricial**:\n\n"
            "$$\\mathbf{x}'(t) = \\mathbf{A}(t)\\, \\mathbf{x}(t) + \\mathbf{f}(t),$$\n\n"
            "donde $\\mathbf{x}(t) \\in \\mathbb{R}^n$ es el vector de funciones desconocidas, "
            "$\\mathbf{A}(t)$ una matriz $n \\times n$ y $\\mathbf{f}(t)$ un vector dado.\n\n"
            "**Ventaja clave:** toda la teoría que vimos para una EDO lineal de orden 2 (superposición, "
            "wronskiano, conjunto fundamental, $y_h + y_p$) se generaliza casi palabra por palabra al "
            "lenguaje matricial. Y además, **toda EDO lineal de orden $n$ se reduce a un sistema de orden 1** — "
            "así que esta teoría es realmente la 'forma canónica' de todo el capítulo anterior.\n\n"
            "**Al terminar:**\n\n"
            "- Reconoces la **forma matricial** $\\mathbf{x}' = \\mathbf{A}(t)\\mathbf{x} + \\mathbf{f}(t)$.\n"
            "- Distingues sistemas **homogéneos** vs. **no homogéneos**, **autónomos** vs. **no autónomos**.\n"
            "- **Reduces** una EDO de orden $n$ a un sistema $n \\times n$ de orden 1.\n"
            "- Aplicas el **teorema de existencia y unicidad** para el PVI."
        )),

        b("definicion",
          titulo="Sistema lineal de primer orden",
          body_md=(
              "Un **sistema lineal de $n$ ecuaciones** de primer orden tiene la forma\n\n"
              "$$\\begin{cases} x_1'(t) = a_{11}(t) x_1 + a_{12}(t) x_2 + \\cdots + a_{1n}(t) x_n + f_1(t), \\\\ "
              "x_2'(t) = a_{21}(t) x_1 + a_{22}(t) x_2 + \\cdots + a_{2n}(t) x_n + f_2(t), \\\\ "
              "\\;\\;\\vdots \\\\ "
              "x_n'(t) = a_{n1}(t) x_1 + a_{n2}(t) x_2 + \\cdots + a_{nn}(t) x_n + f_n(t). \\end{cases}$$\n\n"
              "**Forma matricial.** Definiendo el vector $\\mathbf{x}(t) = (x_1, \\ldots, x_n)^T$, la matriz "
              "$\\mathbf{A}(t) = (a_{ij}(t))$ y el vector $\\mathbf{f}(t) = (f_1, \\ldots, f_n)^T$:\n\n"
              "$$\\mathbf{x}'(t) = \\mathbf{A}(t)\\, \\mathbf{x}(t) + \\mathbf{f}(t).$$\n\n"
              "**Clasificación:**\n\n"
              "- **Homogéneo:** $\\mathbf{f}(t) \\equiv \\mathbf{0}$.\n"
              "- **Autónomo (o de coeficientes constantes):** $\\mathbf{A}(t) \\equiv \\mathbf{A}$ constante.\n"
              "- **No autónomo:** $\\mathbf{A}$ depende de $t$.\n\n"
              "El caso **lineal con coeficientes constantes** (autónomo) es el que tiene métodos completos y "
              "es nuestro foco principal."
          )),

        b("definicion",
          titulo="Problema de valor inicial para sistemas",
          body_md=(
              "Un **PVI** consiste en\n\n"
              "$$\\mathbf{x}'(t) = \\mathbf{A}(t)\\mathbf{x}(t) + \\mathbf{f}(t), \\qquad \\mathbf{x}(t_0) = \\mathbf{x}_0,$$\n\n"
              "donde $\\mathbf{x}_0 \\in \\mathbb{R}^n$ es la **condición inicial**: especifica los $n$ "
              "valores $x_1(t_0), x_2(t_0), \\ldots, x_n(t_0)$ simultáneamente.\n\n"
              "**Teorema (E&U para sistemas lineales).** Si $\\mathbf{A}(t)$ y $\\mathbf{f}(t)$ son "
              "**continuas** en un intervalo abierto $I$ que contiene a $t_0$, entonces el PVI tiene "
              "**una única solución** $\\mathbf{x}(t)$ definida en **todo** $I$.\n\n"
              "**Importante:** la continuidad se pide entrada por entrada de la matriz y del vector. Y a "
              "diferencia del caso no lineal, la solución se extiende a todo el intervalo de continuidad — "
              "no se queda 'atascada' en un punto interior."
          )),

        formulas(
            titulo="Reducción de una EDO de orden n a un sistema",
            body=(
                "**Idea.** Toda EDO lineal de orden $n$\n\n"
                "$$y^{(n)} + p_{n-1}(t) y^{(n-1)} + \\cdots + p_1(t) y' + p_0(t) y = g(t)$$\n\n"
                "se reescribe como un **sistema lineal de $n$ ecuaciones de primer orden** con el cambio de "
                "variable\n\n"
                "$$x_1 = y, \\quad x_2 = y', \\quad x_3 = y'', \\quad \\ldots, \\quad x_n = y^{(n-1)}.$$\n\n"
                "Entonces $x_1' = x_2$, $x_2' = x_3$, ..., $x_{n-1}' = x_n$, y la EDO original se traduce en\n\n"
                "$$x_n' = -p_0(t) x_1 - p_1(t) x_2 - \\cdots - p_{n-1}(t) x_n + g(t).$$\n\n"
                "En forma matricial $\\mathbf{x}' = \\mathbf{A}(t)\\mathbf{x} + \\mathbf{f}(t)$ con la "
                "**matriz compañera**\n\n"
                "$$\\mathbf{A}(t) = \\begin{pmatrix} 0 & 1 & 0 & \\cdots & 0 \\\\ 0 & 0 & 1 & \\cdots & 0 \\\\ \\vdots & & & \\ddots & \\vdots \\\\ 0 & 0 & 0 & \\cdots & 1 \\\\ -p_0 & -p_1 & -p_2 & \\cdots & -p_{n-1} \\end{pmatrix}, \\qquad \\mathbf{f}(t) = \\begin{pmatrix} 0 \\\\ 0 \\\\ \\vdots \\\\ 0 \\\\ g(t) \\end{pmatrix}.$$\n\n"
                "**Consecuencia teórica:** todo lo que probemos para sistemas se aplica también a EDOs "
                "escalares de orden alto. **Consecuencia práctica:** los métodos numéricos están diseñados "
                "para sistemas de orden 1 — por eso esta forma es estándar."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Reducir un oscilador a sistema",
          problema_md=(
              "Reescribe la EDO $y'' + 2 y' + 5 y = \\cos t$ como un sistema $2 \\times 2$ de primer orden."
          ),
          pasos=[
              {"accion_md": (
                  "**Cambio de variable:** $x_1 = y$, $x_2 = y'$. Entonces $x_1' = y' = x_2$ y "
                  "$x_2' = y'' = -2 y' - 5 y + \\cos t = -5 x_1 - 2 x_2 + \\cos t$."
              ),
               "justificacion_md": "Despejar $y''$ de la EDO original.",
               "es_resultado": False},
              {"accion_md": (
                  "**Forma matricial:**\n\n"
                  "$$\\mathbf{x}' = \\begin{pmatrix} 0 & 1 \\\\ -5 & -2 \\end{pmatrix} \\mathbf{x} + \\begin{pmatrix} 0 \\\\ \\cos t \\end{pmatrix}.$$\n\n"
                  "Sistema $2 \\times 2$ no autónomo (por el $\\cos t$) y no homogéneo."
              ),
               "justificacion_md": "Es la matriz compañera del polinomio característico $r^2 + 2 r + 5$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Tanques acoplados (mezcla)",
          problema_md=(
              "Dos tanques de volumen $V_1 = 100$ y $V_2 = 200$ litros están conectados. Desde el tanque 1 "
              "fluye al 2 a razón $r$ L/s y vuelve del 2 al 1 a la misma razón. Si $x_i(t)$ es la cantidad "
              "de sal en el tanque $i$, plantea el sistema."
          ),
          pasos=[
              {"accion_md": (
                  "**Tasa neta del tanque 1:** entra $r \\cdot x_2 / V_2$ kg/s y sale $r \\cdot x_1 / V_1$ kg/s.\n\n"
                  "$x_1' = r\\, x_2 / 200 - r\\, x_1 / 100$."
              ),
               "justificacion_md": "Balance de materia: lo que entra menos lo que sale.",
               "es_resultado": False},
              {"accion_md": (
                  "**Análogamente:** $x_2' = r\\, x_1 / 100 - r\\, x_2 / 200$."
              ),
               "justificacion_md": "Simétrico al primero.",
               "es_resultado": False},
              {"accion_md": (
                  "**Forma matricial** (tomando $r = 1$ para simplificar):\n\n"
                  "$$\\mathbf{x}' = \\begin{pmatrix} -1/100 & 1/200 \\\\ 1/100 & -1/200 \\end{pmatrix} \\mathbf{x}.$$\n\n"
                  "Sistema lineal **homogéneo, autónomo, $2 \\times 2$.** Lo resolveremos con valores propios."
              ),
               "justificacion_md": "**Observación:** la suma $x_1 + x_2$ se conserva (la sal no desaparece) — corresponde a un valor propio $0$ de la matriz.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**¿Por qué tanto énfasis en la forma matricial?** Tres razones:\n\n"
            "1. **Compacidad notacional:** $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$ se lee igual que $y' = a y$ "
            "del caso escalar. La intuición se transfiere directamente.\n"
            "2. **Métodos algebraicos directos:** valores propios y vectores propios de $\\mathbf{A}$ generan "
            "soluciones $\\mathbf{v}\\, e^{\\lambda t}$ — analogía perfecta con $e^{r x}$ del caso escalar.\n"
            "3. **Análisis numérico estándar:** los integradores numéricos (Runge-Kutta, etc.) están "
            "diseñados para la forma $\\mathbf{x}' = \\mathbf{F}(t, \\mathbf{x})$.\n\n"
            "**Espacio de fase.** Para sistemas autónomos, el vector $\\mathbf{x}(t) \\in \\mathbb{R}^n$ "
            "describe el **estado** del sistema. La trayectoria en $\\mathbb{R}^n$ se llama **órbita** o "
            "**trayectoria de fase**. En lección 6 visualizamos órbitas y clasificamos su comportamiento "
            "cualitativo."
        )),

        fig(
            "Esquema de tanques acoplados. Dos cilindros verticales lado a lado etiquetados 'Tanque 1 (V_1)' y 'Tanque 2 (V_2)'. "
            "Entre ellos, dos flechas curvas: una arriba que va del Tanque 1 al Tanque 2 etiquetada 'r L/s', "
            "y una abajo que va del Tanque 2 al Tanque 1 etiquetada 'r L/s'. "
            "Adentro de cada tanque, etiquetas 'x_1(t) kg de sal' y 'x_2(t) kg de sal'. "
            "Acentos teal #06b6d4 en los tanques y ámbar #f59e0b en las flechas. "
            "Abajo del esquema, el sistema EDO escrito: x_1' = r x_2/V_2 - r x_1/V_1, x_2' = r x_1/V_1 - r x_2/V_2. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El sistema $x_1' = 2 x_1 + x_2$, $x_2' = -x_1 + 3 x_2$ se escribe como $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$ con:",
                  "opciones_md": [
                      "$\\mathbf{A} = \\begin{pmatrix} 2 & -1 \\\\ 1 & 3 \\end{pmatrix}$",
                      "**$\\mathbf{A} = \\begin{pmatrix} 2 & 1 \\\\ -1 & 3 \\end{pmatrix}$**",
                      "$\\mathbf{A} = \\begin{pmatrix} 2 & 0 \\\\ 0 & 3 \\end{pmatrix}$",
                      "$\\mathbf{A} = \\begin{pmatrix} 2 & 3 \\\\ 1 & -1 \\end{pmatrix}$",
                  ],
                  "correcta": "B",
                  "pista_md": "La fila $i$ son los coeficientes de $x_1, x_2$ en la $i$-ésima ecuación.",
                  "explicacion_md": "Fila 1: $(2, 1)$ por $x_1' = 2 x_1 + 1 \\cdot x_2$. Fila 2: $(-1, 3)$.",
              },
              {
                  "enunciado_md": "La EDO $y''' = y$ equivale al sistema $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$ con $\\mathbf{A}$:",
                  "opciones_md": [
                      "$\\begin{pmatrix} 0 & 1 & 0 \\\\ 0 & 0 & 1 \\\\ 0 & 0 & 1 \\end{pmatrix}$",
                      "**$\\begin{pmatrix} 0 & 1 & 0 \\\\ 0 & 0 & 1 \\\\ 1 & 0 & 0 \\end{pmatrix}$**",
                      "$\\begin{pmatrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1 \\end{pmatrix}$",
                      "$\\begin{pmatrix} 0 & 0 & 1 \\\\ 1 & 0 & 0 \\\\ 0 & 1 & 0 \\end{pmatrix}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Matriz compañera: las dos primeras filas son corrimientos identidad y la última lleva los coeficientes.",
                  "explicacion_md": "$x_1' = x_2$, $x_2' = x_3$, $x_3' = y''' = y = x_1$.",
              },
              {
                  "enunciado_md": "Un PVI para un sistema $n \\times n$ requiere:",
                  "opciones_md": [
                      "Una condición $\\mathbf{x}(t_0) = c$",
                      "**$n$ condiciones — una por cada componente $x_i(t_0)$**",
                      "Las primeras $n - 1$ derivadas en $t_0$",
                      "Solo el orden de la matriz",
                  ],
                  "correcta": "B",
                  "pista_md": "Tantas como variables.",
                  "explicacion_md": "$\\mathbf{x}_0 \\in \\mathbb{R}^n$ tiene $n$ entradas — fija el estado inicial completo.",
              },
          ]),

        ej(
            "Reducir EDO de orden 4",
            "Lleva $y^{(4)} + 3 y'' - 2 y = \\sin t$ a un sistema de primer orden $4 \\times 4$.",
            ["$x_1 = y, x_2 = y', x_3 = y'', x_4 = y'''$."],
            (
                "$x_1' = x_2$, $x_2' = x_3$, $x_3' = x_4$, $x_4' = y^{(4)} = -3 y'' + 2 y + \\sin t = 2 x_1 - 3 x_3 + \\sin t$.\n\n"
                "$$\\mathbf{A} = \\begin{pmatrix} 0 & 1 & 0 & 0 \\\\ 0 & 0 & 1 & 0 \\\\ 0 & 0 & 0 & 1 \\\\ 2 & 0 & -3 & 0 \\end{pmatrix}, \\quad \\mathbf{f}(t) = \\begin{pmatrix} 0 \\\\ 0 \\\\ 0 \\\\ \\sin t \\end{pmatrix}.$$"
            ),
        ),

        ej(
            "Verificar solución",
            "Comprueba que $\\mathbf{x}(t) = \\begin{pmatrix} e^{2t} \\\\ e^{2t} \\end{pmatrix}$ es solución de $\\mathbf{x}' = \\begin{pmatrix} 1 & 1 \\\\ 1 & 1 \\end{pmatrix} \\mathbf{x}$.",
            ["Calcular $\\mathbf{x}'$ y $\\mathbf{A}\\mathbf{x}$ y comparar."],
            (
                "$\\mathbf{x}' = \\begin{pmatrix} 2 e^{2t} \\\\ 2 e^{2t} \\end{pmatrix}$.\n\n"
                "$\\mathbf{A}\\mathbf{x} = \\begin{pmatrix} e^{2t} + e^{2t} \\\\ e^{2t} + e^{2t} \\end{pmatrix} = \\begin{pmatrix} 2 e^{2t} \\\\ 2 e^{2t} \\end{pmatrix}$. ✓\n\n"
                "Coinciden — es solución (corresponde al valor propio $\\lambda = 2$ con vector propio $(1, 1)^T$, como veremos en la lección 3)."
            ),
        ),

        ej(
            "Modelado: depredador-presa lineal",
            "Una versión linealizada del modelo de Lotka-Volterra cerca del equilibrio es $u' = 2 v$, $v' = -3 u$. Escribe en forma matricial y clasifica.",
            ["Dos ecuaciones acopladas, sin término independiente."],
            (
                "$\\mathbf{x} = (u, v)^T$, $\\mathbf{x}' = \\begin{pmatrix} 0 & 2 \\\\ -3 & 0 \\end{pmatrix} \\mathbf{x}$.\n\n"
                "**Sistema lineal homogéneo autónomo $2 \\times 2$.** En la lección 3 mostraremos que sus soluciones son oscilatorias (valores propios imaginarios puros)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir filas y columnas al armar $\\mathbf{A}$.** La fila $i$ son los coeficientes de la ecuación de $x_i'$.",
              "**Olvidar el vector $\\mathbf{f}(t)$ no homogéneo** al pasar a forma matricial.",
              "**Pensar que un sistema requiere una sola condición inicial.** Hace falta una por cada $x_i$.",
              "**No reducir EDOs de orden alto a sistemas** antes de aplicar métodos numéricos.",
              "**Equivocar signo en la matriz compañera:** la última fila lleva $-p_0, -p_1, \\ldots$, no $p_0, p_1, \\ldots$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma matricial:** $\\mathbf{x}'(t) = \\mathbf{A}(t)\\mathbf{x}(t) + \\mathbf{f}(t)$, con $\\mathbf{x} \\in \\mathbb{R}^n$.",
              "**Clasificación:** homogéneo/no homogéneo según $\\mathbf{f}$; autónomo/no autónomo según $\\mathbf{A}$.",
              "**E&U:** continuidad de $\\mathbf{A}, \\mathbf{f}$ en $I$ garantiza solución única en todo $I$.",
              "**Reducción:** EDO escalar de orden $n$ ↔ sistema $n \\times n$ vía matriz compañera.",
              "**Próxima lección:** estructura de las soluciones — superposición y wronskiano para vectores.",
          ]),
    ]
    return {
        "id": "lec-ed-3-1-sistemas-lineales",
        "title": "Sistemas lineales de primer orden",
        "description": "Definición de sistema lineal en forma matricial, clasificación, problema de valor inicial y existencia y unicidad. Reducción de una EDO de orden n a un sistema 1×1 vía matriz compañera.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# Soluciones de un sistema lineal
# =====================================================================
def lesson_soluciones_sl():
    blocks = [
        b("texto", body_md=(
            "Antes de **encontrar** soluciones de un sistema lineal homogéneo $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$, "
            "estudiemos la **estructura** del conjunto de todas sus soluciones — exactamente como hicimos en "
            "el Cap. 2 con la EDO escalar de orden 2.\n\n"
            "**Resultado central** (vamos a probarlo en esta lección): el conjunto de soluciones de un sistema "
            "lineal homogéneo $n \\times n$ es un **espacio vectorial de dimensión $n$**. Eso significa que "
            "basta encontrar **$n$ soluciones linealmente independientes** $\\mathbf{x}_1, \\ldots, \\mathbf{x}_n$ "
            "y todas las demás se escriben como combinación lineal.\n\n"
            "**Al terminar:**\n\n"
            "- Aplicas el **principio de superposición** para sistemas.\n"
            "- Calculas el **wronskiano** de funciones vectoriales y lo usas para detectar conjuntos fundamentales.\n"
            "- Escribes la **solución general** $\\mathbf{x} = c_1 \\mathbf{x}_1 + \\cdots + c_n \\mathbf{x}_n$.\n"
            "- Resuelves PVIs imponiendo la condición $\\mathbf{x}(t_0) = \\mathbf{x}_0$ sobre la solución general."
        )),

        b("definicion",
          titulo="Principio de superposición",
          body_md=(
              "**Teorema (superposición).** Si $\\mathbf{x}_1(t), \\mathbf{x}_2(t), \\ldots, \\mathbf{x}_k(t)$ "
              "son soluciones del sistema homogéneo\n\n"
              "$$\\mathbf{x}'(t) = \\mathbf{A}(t)\\mathbf{x}(t),$$\n\n"
              "entonces toda combinación lineal\n\n"
              "$$\\mathbf{x}(t) = c_1 \\mathbf{x}_1(t) + c_2 \\mathbf{x}_2(t) + \\cdots + c_k \\mathbf{x}_k(t)$$\n\n"
              "también es solución.\n\n"
              "**Demostración (en una línea):** $\\mathbf{x}'(t) = \\sum c_i \\mathbf{x}_i'(t) = \\sum c_i \\mathbf{A} \\mathbf{x}_i(t) = \\mathbf{A} \\sum c_i \\mathbf{x}_i(t) = \\mathbf{A} \\mathbf{x}(t)$.\n\n"
              "**Igual que en el caso escalar:** este principio falla para sistemas no lineales."
          )),

        b("definicion",
          titulo="Independencia lineal de funciones vectoriales",
          body_md=(
              "Funciones vectoriales $\\mathbf{x}_1(t), \\ldots, \\mathbf{x}_n(t)$ definidas en $I$ son "
              "**linealmente dependientes** si existen constantes $c_1, \\ldots, c_n$ no todas nulas tales que\n\n"
              "$$c_1 \\mathbf{x}_1(t) + c_2 \\mathbf{x}_2(t) + \\cdots + c_n \\mathbf{x}_n(t) = \\mathbf{0} \\quad \\text{para todo } t \\in I.$$\n\n"
              "Caso contrario son **linealmente independientes**: la única forma de que la combinación sea "
              "idénticamente cero es $c_1 = c_2 = \\cdots = c_n = 0$.\n\n"
              "**Atención:** la combinación lineal vectorial $c_1 \\mathbf{x}_1 + \\cdots = \\mathbf{0}$ "
              "significa que **cada componente** se anula identicamente. Es una restricción muy fuerte."
          )),

        b("definicion",
          titulo="Wronskiano de funciones vectoriales",
          body_md=(
              "Para $n$ funciones vectoriales $\\mathbf{x}_1, \\ldots, \\mathbf{x}_n$ con valores en "
              "$\\mathbb{R}^n$, el **wronskiano** es el determinante de la matriz que las tiene como columnas:\n\n"
              "$$W(t) = \\det\\bigl[\\, \\mathbf{x}_1(t) \\;\\big|\\; \\mathbf{x}_2(t) \\;\\big|\\; \\cdots \\;\\big|\\; \\mathbf{x}_n(t) \\,\\bigr].$$\n\n"
              "**Criterio (para soluciones de la misma EDO lineal $\\mathbf{x}' = \\mathbf{A}(t)\\mathbf{x}$ "
              "con $\\mathbf{A}$ continua):**\n\n"
              "- Si $W(t_0) \\neq 0$ para algún $t_0 \\in I$, entonces son LI en todo $I$.\n"
              "- Si $W \\equiv 0$ en $I$, entonces son LD en $I$.\n\n"
              "**Identidad de Abel-Liouville:** $W(t) = W(t_0)\\, \\exp\\left(\\int_{t_0}^t \\operatorname{tr} \\mathbf{A}(s)\\, ds\\right)$. "
              "Por lo tanto $W$ **o es idénticamente cero, o no se anula nunca** en $I$ — basta evaluar en "
              "un solo punto para concluir."
          )),

        b("definicion",
          titulo="Conjunto fundamental y solución general",
          body_md=(
              "Un conjunto $\\{\\mathbf{x}_1, \\ldots, \\mathbf{x}_n\\}$ de **$n$ soluciones LI** del sistema "
              "homogéneo $\\mathbf{x}' = \\mathbf{A}(t)\\mathbf{x}$ se llama **conjunto fundamental** en $I$.\n\n"
              "**Teorema (estructura).** Si $\\{\\mathbf{x}_1, \\ldots, \\mathbf{x}_n\\}$ es fundamental, "
              "**toda** solución del sistema homogéneo se escribe **de manera única** como\n\n"
              "$$\\mathbf{x}(t) = c_1 \\mathbf{x}_1(t) + c_2 \\mathbf{x}_2(t) + \\cdots + c_n \\mathbf{x}_n(t).$$\n\n"
              "El espacio de soluciones es un **espacio vectorial de dimensión $n$** (donde $n$ es el "
              "tamaño del sistema).\n\n"
              "**Estructura del sistema no homogéneo:** si $\\mathbf{x}_p$ es **alguna** solución particular "
              "de $\\mathbf{x}' = \\mathbf{A}(t)\\mathbf{x} + \\mathbf{f}(t)$, la solución general es\n\n"
              "$$\\mathbf{x}(t) = \\underbrace{\\mathbf{x}_c(t)}_{\\text{solución general homogénea}} + \\mathbf{x}_p(t).$$"
          )),

        b("ejemplo_resuelto",
          titulo="Verificar conjunto fundamental",
          problema_md=(
              "Comprueba que $\\mathbf{x}_1 = \\begin{pmatrix} e^{3t} \\\\ 2 e^{3t} \\end{pmatrix}$ y "
              "$\\mathbf{x}_2 = \\begin{pmatrix} e^{-t} \\\\ -2 e^{-t} \\end{pmatrix}$ son soluciones LI de "
              "$\\mathbf{x}' = \\begin{pmatrix} 1 & 1 \\\\ 4 & 1 \\end{pmatrix} \\mathbf{x}$ y escribe la solución general."
          ),
          pasos=[
              {"accion_md": (
                  "**Verificar que $\\mathbf{x}_1$ es solución.** $\\mathbf{x}_1' = (3 e^{3t}, 6 e^{3t})^T$.\n\n"
                  "$\\mathbf{A}\\mathbf{x}_1 = \\begin{pmatrix} e^{3t} + 2 e^{3t} \\\\ 4 e^{3t} + 2 e^{3t} \\end{pmatrix} = \\begin{pmatrix} 3 e^{3t} \\\\ 6 e^{3t} \\end{pmatrix}$. ✓"
              ),
               "justificacion_md": "Las componentes coinciden — es solución.",
               "es_resultado": False},
              {"accion_md": (
                  "**Análogamente $\\mathbf{x}_2$ es solución** ($\\mathbf{x}_2' = -\\mathbf{x}_2$ y $\\mathbf{A}\\mathbf{x}_2 = -\\mathbf{x}_2$, verificación directa)."
              ),
               "justificacion_md": "Misma técnica.",
               "es_resultado": False},
              {"accion_md": (
                  "**Wronskiano:**\n\n"
                  "$$W(t) = \\det \\begin{pmatrix} e^{3t} & e^{-t} \\\\ 2 e^{3t} & -2 e^{-t} \\end{pmatrix} = -2 e^{2t} - 2 e^{2t} = -4 e^{2t} \\neq 0.$$"
              ),
               "justificacion_md": "Wronskiano nunca cero → conjunto fundamental.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:**\n\n"
                  "$$\\mathbf{x}(t) = c_1 \\begin{pmatrix} e^{3t} \\\\ 2 e^{3t} \\end{pmatrix} + c_2 \\begin{pmatrix} e^{-t} \\\\ -2 e^{-t} \\end{pmatrix} = \\begin{pmatrix} c_1 e^{3t} + c_2 e^{-t} \\\\ 2 c_1 e^{3t} - 2 c_2 e^{-t} \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Combinación lineal de las dos soluciones LI.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Resolver un PVI",
          problema_md=(
              "Continúa el ejemplo anterior y halla la solución del PVI con $\\mathbf{x}(0) = \\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Imponer condiciones iniciales** sobre la solución general en $t = 0$:\n\n"
                  "$$\\mathbf{x}(0) = c_1 \\begin{pmatrix} 1 \\\\ 2 \\end{pmatrix} + c_2 \\begin{pmatrix} 1 \\\\ -2 \\end{pmatrix} = \\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Sistema lineal $2 \\times 2$ en $c_1, c_2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sistema escalar:** $c_1 + c_2 = 1$, $2 c_1 - 2 c_2 = 0$. De la segunda $c_1 = c_2$, sustituyendo $2 c_1 = 1$, así $c_1 = c_2 = 1/2$."
              ),
               "justificacion_md": "Resolución directa.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución del PVI:**\n\n"
                  "$$\\mathbf{x}(t) = \\dfrac{1}{2} \\begin{pmatrix} e^{3t} + e^{-t} \\\\ 2 e^{3t} - 2 e^{-t} \\end{pmatrix} = \\begin{pmatrix} \\cosh t \\cdot e^t \\\\ \\sinh t \\cdot 2 e^t \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Por unicidad, no hay otra solución posible.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué dimensión exactamente $n$.** Por el teorema de E&U, para cada estado inicial "
            "$\\mathbf{x}_0 \\in \\mathbb{R}^n$ hay una y solo una solución. Es decir, el mapa "
            "'condición inicial → solución' es **biyectivo** entre $\\mathbb{R}^n$ y el espacio de "
            "soluciones. Como $\\mathbb{R}^n$ tiene dimensión $n$, también el espacio de soluciones.\n\n"
            "**Esto da una receta para chequear independencia lineal sin calcular wronskianos:** evalúa las "
            "$n$ soluciones en un punto $t_0$ cualquiera. Si los **vectores numéricos** "
            "$\\mathbf{x}_1(t_0), \\ldots, \\mathbf{x}_n(t_0) \\in \\mathbb{R}^n$ son LI (en el sentido "
            "lineal estándar), entonces las **funciones** son LI."
        )),

        fig(
            "Esquema visual del espacio de soluciones de un sistema lineal homogéneo de dimensión 2. "
            "A la izquierda, un eje t horizontal con dos curvas vectoriales: x_1(t) en teal #06b6d4 y x_2(t) en gris (cada una con dos componentes apiladas). "
            "Una flecha grande con texto 'combinación lineal c_1 x_1 + c_2 x_2' apunta a la derecha. "
            "A la derecha, una nueva curva vectorial en ámbar #f59e0b mostrando una combinación específica. "
            "Debajo, una caja con la fórmula 'x(t) = c_1 x_1(t) + c_2 x_2(t)' y el comentario 'dim espacio = n = 2'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El espacio de soluciones de un sistema lineal homogéneo $n \\times n$ tiene dimensión:",
                  "opciones_md": ["$1$", "$n - 1$", "**$n$**", "$n + 1$"],
                  "correcta": "C",
                  "pista_md": "Igual a la dimensión del sistema.",
                  "explicacion_md": "$n$ soluciones LI generan toda solución. La biyección con $\\mathbb{R}^n$ vía condición inicial lo demuestra.",
              },
              {
                  "enunciado_md": "Si $W(t_0) \\neq 0$ para soluciones del mismo sistema, las soluciones son:",
                  "opciones_md": [
                      "Linealmente dependientes",
                      "**Linealmente independientes en todo $I$**",
                      "LI solo en $t_0$",
                      "Ortogonales",
                  ],
                  "correcta": "B",
                  "pista_md": "Por Abel-Liouville, $W$ no se anula en ningún punto de $I$ si no es idénticamente cero.",
                  "explicacion_md": "Conclusión global a partir de un solo punto, gracias a la identidad de Abel-Liouville.",
              },
              {
                  "enunciado_md": "Para la solución general $\\mathbf{x}(t) = c_1 \\mathbf{x}_1 + c_2 \\mathbf{x}_2$, el sistema en $c_1, c_2$ que sale del PVI tiene matriz:",
                  "opciones_md": [
                      "$\\mathbf{A}(t_0)$",
                      "**$[\\mathbf{x}_1(t_0) \\mid \\mathbf{x}_2(t_0)]$**",
                      "$\\mathbf{x}_0$",
                      "La inversa de $\\mathbf{A}$",
                  ],
                  "correcta": "B",
                  "pista_md": "El sistema es $[\\mathbf{x}_1(t_0) \\mid \\mathbf{x}_2(t_0)] \\mathbf{c} = \\mathbf{x}_0$.",
                  "explicacion_md": "La matriz del sistema es la wronskiana evaluada en $t_0$ — invertible por ser conjunto fundamental.",
              },
          ]),

        ej(
            "Wronskiano para concluir LI",
            "Verifica que $\\mathbf{x}_1 = \\begin{pmatrix} \\cos t \\\\ -\\sin t \\end{pmatrix}$ y $\\mathbf{x}_2 = \\begin{pmatrix} \\sin t \\\\ \\cos t \\end{pmatrix}$ son LI.",
            ["Calcular $W$."],
            (
                "$W(t) = \\det \\begin{pmatrix} \\cos t & \\sin t \\\\ -\\sin t & \\cos t \\end{pmatrix} = \\cos^2 t + \\sin^2 t = 1 \\neq 0$. **LI en $\\mathbb{R}$.**"
            ),
        ),

        ej(
            "Resolver PVI sabiendo el conjunto fundamental",
            "Si $\\mathbf{x}_1 = \\begin{pmatrix} e^{2t} \\\\ e^{2t} \\end{pmatrix}$ y $\\mathbf{x}_2 = \\begin{pmatrix} e^{-2t} \\\\ -e^{-2t} \\end{pmatrix}$ son fundamentales, halla la solución con $\\mathbf{x}(0) = (3, 1)^T$.",
            ["$c_1 (1, 1) + c_2 (1, -1) = (3, 1)$."],
            (
                "$c_1 + c_2 = 3$, $c_1 - c_2 = 1 \\Rightarrow c_1 = 2, c_2 = 1$.\n\n"
                "$\\mathbf{x}(t) = 2 \\begin{pmatrix} e^{2t} \\\\ e^{2t} \\end{pmatrix} + \\begin{pmatrix} e^{-2t} \\\\ -e^{-2t} \\end{pmatrix} = \\begin{pmatrix} 2 e^{2t} + e^{-2t} \\\\ 2 e^{2t} - e^{-2t} \\end{pmatrix}$."
            ),
        ),

        ej(
            "Detectar dependencia lineal",
            "¿Son LI las funciones $\\mathbf{x}_1 = \\begin{pmatrix} t \\\\ 1 \\end{pmatrix}$ y $\\mathbf{x}_2 = \\begin{pmatrix} 2 t \\\\ 2 \\end{pmatrix}$?",
            ["Mirar si una es múltiplo escalar de la otra."],
            (
                "$\\mathbf{x}_2 = 2 \\mathbf{x}_1$ para todo $t$. **Linealmente dependientes** ($W \\equiv 0$). "
                "Cuidado: como funciones generales no provienen necesariamente del mismo sistema, conviene verificar directamente."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar el criterio del wronskiano a funciones que no son soluciones de un sistema lineal.** En general $W = 0$ no implica LD.",
              "**Olvidar que el wronskiano es un determinante de la matriz cuyas columnas son las soluciones.**",
              "**Confundir la matriz $\\mathbf{A}$ con la matriz de soluciones.** $\\mathbf{A}$ define el sistema; las soluciones son los vectores que lo satisfacen.",
              "**Pensar que un sistema $2 \\times 2$ tiene solución general con una sola constante.** Tiene exactamente $n$ — dos en este caso.",
              "**Imponer las condiciones iniciales sobre $\\mathbf{x}_h$ olvidando $\\mathbf{x}_p$ en el caso no homogéneo.** Las condiciones se aplican siempre sobre la solución total $\\mathbf{x} = \\mathbf{x}_c + \\mathbf{x}_p$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Superposición:** combinación lineal de soluciones del sistema homogéneo es solución.",
              "**Wronskiano:** $W(t) = \\det[\\mathbf{x}_1 \\mid \\cdots \\mid \\mathbf{x}_n]$. Para soluciones de la misma EDO lineal, $W \\not\\equiv 0$ $\\Leftrightarrow$ LI.",
              "**Conjunto fundamental:** $n$ soluciones LI; la solución general es su combinación lineal.",
              "**Sistema no homogéneo:** $\\mathbf{x} = \\mathbf{x}_c + \\mathbf{x}_p$.",
              "**Próxima lección:** método de valores propios para encontrar el conjunto fundamental cuando $\\mathbf{A}$ es constante.",
          ]),
    ]
    return {
        "id": "lec-ed-3-2-soluciones-sl",
        "title": "Soluciones de un sistema lineal",
        "description": "Estructura del espacio de soluciones de un sistema lineal: principio de superposición, dependencia lineal de funciones vectoriales, wronskiano y conjunto fundamental.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# Método de valores propios
# =====================================================================
def lesson_valores_propios():
    blocks = [
        b("texto", body_md=(
            "Llegamos al método **estrella** del capítulo: cómo encontrar el conjunto fundamental de un "
            "sistema lineal homogéneo con **coeficientes constantes**\n\n"
            "$$\\mathbf{x}'(t) = \\mathbf{A}\\mathbf{x}(t),$$\n\n"
            "donde $\\mathbf{A}$ es una matriz $n \\times n$ constante. La idea es la misma que en el caso "
            "escalar: probar **soluciones exponenciales** $\\mathbf{x} = \\mathbf{v}\\, e^{\\lambda t}$ con "
            "$\\mathbf{v}$ vector constante.\n\n"
            "Sustituyendo, $\\mathbf{x}' = \\lambda \\mathbf{v}\\, e^{\\lambda t}$ y $\\mathbf{A}\\mathbf{x} = \\mathbf{A}\\mathbf{v}\\, e^{\\lambda t}$. "
            "Para que sean iguales se necesita\n\n"
            "$$\\boxed{\\mathbf{A}\\mathbf{v} = \\lambda\\, \\mathbf{v}.}$$\n\n"
            "Es decir: **$\\lambda$ debe ser valor propio (autovalor) de $\\mathbf{A}$ y $\\mathbf{v}$ su "
            "vector propio (autovector)**. El método de valores propios traduce el problema diferencial en "
            "un problema **algebraico de álgebra lineal**.\n\n"
            "**Al terminar:**\n\n"
            "- Calculas valores y vectores propios resolviendo $\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = 0$.\n"
            "- Construyes la solución general en los **tres casos**: valores propios reales distintos, "
            "complejos conjugados y repetidos (con vectores propios generalizados)."
        )),

        b("definicion",
          titulo="Valores y vectores propios",
          body_md=(
              "Sea $\\mathbf{A}$ una matriz $n \\times n$. Un escalar $\\lambda \\in \\mathbb{C}$ es **valor "
              "propio** de $\\mathbf{A}$ si existe un vector no nulo $\\mathbf{v} \\neq \\mathbf{0}$ tal que\n\n"
              "$$\\mathbf{A}\\mathbf{v} = \\lambda\\, \\mathbf{v}.$$\n\n"
              "El vector $\\mathbf{v}$ se llama **vector propio** asociado a $\\lambda$.\n\n"
              "**Cómo calcularlos.** $(\\mathbf{A} - \\lambda \\mathbf{I})\\mathbf{v} = \\mathbf{0}$ tiene "
              "soluciones no triviales si y solo si\n\n"
              "$$\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = 0.$$\n\n"
              "Esta es la **ecuación característica** de $\\mathbf{A}$: un polinomio de grado $n$ en "
              "$\\lambda$. Sus raíces son los valores propios.\n\n"
              "**Multiplicidades.** Cada valor propio tiene dos multiplicidades:\n\n"
              "- **Algebraica $m_a$:** multiplicidad como raíz del polinomio característico.\n"
              "- **Geométrica $m_g$:** dimensión del espacio propio $\\ker(\\mathbf{A} - \\lambda \\mathbf{I})$.\n\n"
              "Siempre $1 \\leq m_g \\leq m_a$. Si $m_g < m_a$, el valor propio es **defectivo**."
          )),

        b("definicion",
          titulo="Solución básica del método",
          body_md=(
              "**Lema (solución exponencial).** Si $\\lambda$ es valor propio de $\\mathbf{A}$ con vector "
              "propio $\\mathbf{v}$, entonces\n\n"
              "$$\\mathbf{x}(t) = \\mathbf{v}\\, e^{\\lambda t}$$\n\n"
              "es solución de $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$.\n\n"
              "**Verificación:** $\\mathbf{x}'(t) = \\lambda \\mathbf{v}\\, e^{\\lambda t}$ y "
              "$\\mathbf{A}\\mathbf{x}(t) = \\mathbf{A}\\mathbf{v}\\, e^{\\lambda t} = \\lambda \\mathbf{v}\\, e^{\\lambda t}$. ✓\n\n"
              "**Estrategia general.** Si la matriz $\\mathbf{A}$ tiene $n$ vectores propios LI "
              "$\\mathbf{v}_1, \\ldots, \\mathbf{v}_n$ asociados a valores propios $\\lambda_1, \\ldots, \\lambda_n$ "
              "(no necesariamente distintos), entonces $\\{\\mathbf{v}_1 e^{\\lambda_1 t}, \\ldots, \\mathbf{v}_n e^{\\lambda_n t}\\}$ "
              "es un conjunto fundamental, y la solución general es\n\n"
              "$$\\mathbf{x}(t) = c_1 \\mathbf{v}_1 e^{\\lambda_1 t} + c_2 \\mathbf{v}_2 e^{\\lambda_2 t} + \\cdots + c_n \\mathbf{v}_n e^{\\lambda_n t}.$$"
          )),

        formulas(
            titulo="Caso 1 — Valores propios reales distintos",
            body=(
                "Si los $n$ valores propios $\\lambda_1, \\ldots, \\lambda_n$ son **reales y distintos**, sus "
                "vectores propios $\\mathbf{v}_1, \\ldots, \\mathbf{v}_n$ son automáticamente LI. La solución "
                "general es\n\n"
                "$$\\mathbf{x}(t) = c_1 \\mathbf{v}_1 e^{\\lambda_1 t} + c_2 \\mathbf{v}_2 e^{\\lambda_2 t} + \\cdots + c_n \\mathbf{v}_n e^{\\lambda_n t}.$$\n\n"
                "**Algoritmo:**\n\n"
                "1. Calcular $p(\\lambda) = \\det(\\mathbf{A} - \\lambda \\mathbf{I})$.\n"
                "2. Hallar las raíces $\\lambda_1, \\ldots, \\lambda_n$.\n"
                "3. Para cada $\\lambda_i$, resolver $(\\mathbf{A} - \\lambda_i \\mathbf{I}) \\mathbf{v} = \\mathbf{0}$ y elegir un vector propio $\\mathbf{v}_i$.\n"
                "4. Combinar linealmente las exponenciales con coeficientes $c_i$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Reales distintos, sistema $2 \\times 2$",
          problema_md=(
              "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 4 & 2 \\\\ 3 & -1 \\end{pmatrix} \\mathbf{x}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Polinomio característico:**\n\n"
                  "$\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = (4 - \\lambda)(-1 - \\lambda) - 6 = \\lambda^2 - 3 \\lambda - 10 = (\\lambda - 5)(\\lambda + 2)$.\n\n"
                  "Valores propios: $\\lambda_1 = 5$, $\\lambda_2 = -2$."
              ),
               "justificacion_md": "Reales distintos → caso 1.",
               "es_resultado": False},
              {"accion_md": (
                  "**Vector propio para $\\lambda_1 = 5$:** $(\\mathbf{A} - 5\\mathbf{I})\\mathbf{v} = \\mathbf{0}$, es decir, $\\begin{pmatrix} -1 & 2 \\\\ 3 & -6 \\end{pmatrix} \\mathbf{v} = \\mathbf{0}$. La fila 1 da $-v_1 + 2 v_2 = 0$, así $v_1 = 2 v_2$. Elegimos $\\mathbf{v}_1 = (2, 1)^T$."
              ),
               "justificacion_md": "Solo necesitamos un vector propio (cualquiera no nulo en el espacio propio).",
               "es_resultado": False},
              {"accion_md": (
                  "**Vector propio para $\\lambda_2 = -2$:** $\\begin{pmatrix} 6 & 2 \\\\ 3 & 1 \\end{pmatrix} \\mathbf{v} = \\mathbf{0}$, fila 1: $3 v_1 + v_2 = 0 \\Rightarrow v_2 = -3 v_1$. Elegimos $\\mathbf{v}_2 = (1, -3)^T$."
              ),
               "justificacion_md": "Misma técnica, otro autovalor.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:**\n\n"
                  "$$\\mathbf{x}(t) = c_1 \\begin{pmatrix} 2 \\\\ 1 \\end{pmatrix} e^{5 t} + c_2 \\begin{pmatrix} 1 \\\\ -3 \\end{pmatrix} e^{-2 t}.$$"
              ),
               "justificacion_md": "Conjunto fundamental: dos exponenciales con valores propios distintos.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Caso 2 — Valores propios complejos conjugados",
            body=(
                "Si $\\mathbf{A}$ es **real** y $\\lambda = \\alpha + i \\beta$ ($\\beta \\neq 0$) es valor "
                "propio con vector propio $\\mathbf{v} = \\mathbf{a} + i \\mathbf{b}$, entonces $\\bar\\lambda = \\alpha - i\\beta$ "
                "también es valor propio con $\\bar{\\mathbf{v}} = \\mathbf{a} - i \\mathbf{b}$.\n\n"
                "La solución compleja $\\mathbf{x}(t) = (\\mathbf{a} + i \\mathbf{b}) e^{(\\alpha + i \\beta) t}$ "
                "se descompone usando Euler:\n\n"
                "$$\\mathbf{x}(t) = e^{\\alpha t}\\bigl[(\\mathbf{a} \\cos \\beta t - \\mathbf{b} \\sin \\beta t) + i (\\mathbf{a} \\sin \\beta t + \\mathbf{b} \\cos \\beta t)\\bigr].$$\n\n"
                "**Las partes real e imaginaria son dos soluciones reales LI:**\n\n"
                "$$\\mathbf{x}_R(t) = e^{\\alpha t}(\\mathbf{a} \\cos \\beta t - \\mathbf{b} \\sin \\beta t),$$\n"
                "$$\\mathbf{x}_I(t) = e^{\\alpha t}(\\mathbf{a} \\sin \\beta t + \\mathbf{b} \\cos \\beta t).$$\n\n"
                "Cada par conjugado aporta dos soluciones reales — no contar el conjugado por separado."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Valores propios complejos",
          problema_md=(
              "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 1 & -2 \\\\ 1 & 3 \\end{pmatrix} \\mathbf{x}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Característica:** $(1 - \\lambda)(3 - \\lambda) + 2 = \\lambda^2 - 4 \\lambda + 5 = 0$.\n\n"
                  "$\\lambda = 2 \\pm i$, así $\\alpha = 2$, $\\beta = 1$."
              ),
               "justificacion_md": "$\\Delta = 16 - 20 = -4 < 0$ → complejas conjugadas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Vector propio para $\\lambda = 2 + i$:** $(\\mathbf{A} - (2 + i)\\mathbf{I}) \\mathbf{v} = \\mathbf{0}$, es decir, "
                  "$\\begin{pmatrix} -1 - i & -2 \\\\ 1 & 1 - i \\end{pmatrix} \\mathbf{v} = \\mathbf{0}$. Fila 2: $v_1 + (1 - i) v_2 = 0$, así $\\mathbf{v} = (-(1 - i), 1)^T = (-1 + i, 1)^T$.\n\n"
                  "Descomponer: $\\mathbf{v} = \\mathbf{a} + i \\mathbf{b}$ con $\\mathbf{a} = (-1, 1)^T$, $\\mathbf{b} = (1, 0)^T$."
              ),
               "justificacion_md": "Trabajar con un solo conjugado y luego separar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Soluciones reales:**\n\n"
                  "$\\mathbf{x}_R(t) = e^{2 t}\\bigl[(-1, 1)^T \\cos t - (1, 0)^T \\sin t\\bigr] = e^{2 t} \\begin{pmatrix} -\\cos t - \\sin t \\\\ \\cos t \\end{pmatrix}$.\n\n"
                  "$\\mathbf{x}_I(t) = e^{2 t}\\bigl[(-1, 1)^T \\sin t + (1, 0)^T \\cos t\\bigr] = e^{2 t} \\begin{pmatrix} -\\sin t + \\cos t \\\\ \\sin t \\end{pmatrix}$."
              ),
               "justificacion_md": "Aplicar la fórmula de descomposición.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:**\n\n"
                  "$$\\mathbf{x}(t) = c_1 \\mathbf{x}_R(t) + c_2 \\mathbf{x}_I(t).$$\n\n"
                  "Las trayectorias son **espirales** que se alejan del origen (porque $\\alpha = 2 > 0$)."
              ),
               "justificacion_md": "Combinación lineal con dos constantes reales.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Caso 3 — Valores propios repetidos",
            body=(
                "Si $\\lambda$ es valor propio con multiplicidad algebraica $m_a$:\n\n"
                "**Subcaso 3a — no defectivo** ($m_g = m_a$): $\\lambda$ tiene $m_a$ vectores propios LI "
                "$\\mathbf{v}_1, \\ldots, \\mathbf{v}_{m_a}$. Aporta $m_a$ soluciones $\\mathbf{v}_i e^{\\lambda t}$.\n\n"
                "**Subcaso 3b — defectivo** ($m_g < m_a$): hay menos vectores propios que la multiplicidad. "
                "Hay que completar con **vectores propios generalizados** que satisfacen\n\n"
                "$$(\\mathbf{A} - \\lambda \\mathbf{I})\\, \\mathbf{w}_k = \\mathbf{w}_{k-1},$$\n\n"
                "formando una **cadena** $\\mathbf{w}_1 = \\mathbf{v}$ (vector propio), $\\mathbf{w}_2, \\mathbf{w}_3, \\ldots$\n\n"
                "**Soluciones asociadas a la cadena de longitud $m$:**\n\n"
                "$$\\mathbf{x}_1(t) = \\mathbf{w}_1\\, e^{\\lambda t},$$\n"
                "$$\\mathbf{x}_2(t) = (\\mathbf{w}_1\\, t + \\mathbf{w}_2)\\, e^{\\lambda t},$$\n"
                "$$\\mathbf{x}_3(t) = \\Bigl(\\mathbf{w}_1\\, \\dfrac{t^2}{2} + \\mathbf{w}_2\\, t + \\mathbf{w}_3\\Bigr) e^{\\lambda t}, \\ldots$$\n\n"
                "**Caso típico ($2 \\times 2$ defectivo):** $\\mathbf{x}_1 = \\mathbf{v}\\, e^{\\lambda t}$, "
                "$\\mathbf{x}_2 = (\\mathbf{v}\\, t + \\mathbf{w})\\, e^{\\lambda t}$ con $(\\mathbf{A} - \\lambda \\mathbf{I})\\mathbf{w} = \\mathbf{v}$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Caso defectivo $2 \\times 2$",
          problema_md=(
              "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 3 & -1 \\\\ 1 & 1 \\end{pmatrix} \\mathbf{x}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Característica:** $(3 - \\lambda)(1 - \\lambda) + 1 = \\lambda^2 - 4 \\lambda + 4 = (\\lambda - 2)^2$.\n\n"
                  "$\\lambda = 2$ con $m_a = 2$."
              ),
               "justificacion_md": "Discriminante 0 → raíz doble.",
               "es_resultado": False},
              {"accion_md": (
                  "**Espacio propio:** $(\\mathbf{A} - 2 \\mathbf{I})\\mathbf{v} = \\begin{pmatrix} 1 & -1 \\\\ 1 & -1 \\end{pmatrix} \\mathbf{v} = \\mathbf{0}$. "
                  "Fila 1: $v_1 = v_2$. Espacio propio de dimensión 1, $\\mathbf{v} = (1, 1)^T$.\n\n"
                  "$m_g = 1 < m_a = 2$ → **defectivo**, falta una solución."
              ),
               "justificacion_md": "Detectar defectividad: $m_g$ es la dimensión del kernel.",
               "es_resultado": False},
              {"accion_md": (
                  "**Vector propio generalizado:** resolver $(\\mathbf{A} - 2 \\mathbf{I}) \\mathbf{w} = \\mathbf{v}$, es decir, "
                  "$\\begin{pmatrix} 1 & -1 \\\\ 1 & -1 \\end{pmatrix} \\mathbf{w} = \\begin{pmatrix} 1 \\\\ 1 \\end{pmatrix}$. "
                  "Fila 1: $w_1 - w_2 = 1$. Tomamos $\\mathbf{w} = (1, 0)^T$."
              ),
               "justificacion_md": "Cualquier $\\mathbf{w}$ que sirva — la solución general no depende de la elección.",
               "es_resultado": False},
              {"accion_md": (
                  "**Soluciones:**\n\n"
                  "$\\mathbf{x}_1 = \\begin{pmatrix} 1 \\\\ 1 \\end{pmatrix} e^{2 t}$, $\\mathbf{x}_2 = \\Bigl(\\begin{pmatrix} 1 \\\\ 1 \\end{pmatrix} t + \\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix}\\Bigr) e^{2 t} = \\begin{pmatrix} t + 1 \\\\ t \\end{pmatrix} e^{2 t}$.\n\n"
                  "**Solución general:** $\\mathbf{x}(t) = c_1 \\begin{pmatrix} 1 \\\\ 1 \\end{pmatrix} e^{2t} + c_2 \\begin{pmatrix} t + 1 \\\\ t \\end{pmatrix} e^{2t}$."
              ),
               "justificacion_md": "El factor $t$ aparece exactamente como en el caso escalar de raíz doble.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Conexión con el caso escalar.** En el Cap. 2 vimos que la EDO $a y'' + b y' + c y = 0$ se "
            "resuelve con $y = e^{rx}$ y la ecuación característica $a r^2 + b r + c = 0$. Acá la lógica es "
            "**idéntica**: probamos $\\mathbf{x} = \\mathbf{v}\\, e^{\\lambda t}$ y obtenemos "
            "$\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = 0$. Los tres casos (reales distintas, complejas, "
            "repetidas) son exactamente los tres casos de antes — incluso aparece el mismo factor $t$ en el "
            "caso defectivo, por la misma razón.\n\n"
            "**Por qué los autovalores controlan todo.** Las direcciones especiales $\\mathbf{v}$ "
            "(vectores propios) son aquellas en las que $\\mathbf{A}$ actúa como **multiplicación escalar**. "
            "En esas direcciones, el sistema vectorial se reduce a un sistema escalar trivial $y' = \\lambda y$ "
            "con solución $y = e^{\\lambda t}$. Diagonalizar = encontrar todas esas direcciones."
        )),

        fig(
            "Plano de fase mostrando los tres tipos de comportamiento según los valores propios. "
            "Tres paneles 1x3 cada uno con un retrato de fase. "
            "Panel izquierdo 'Reales distintos λ₁ > 0 > λ₂' — un nodo silla con flechas en ejes propios, color teal #06b6d4. "
            "Panel central 'Complejos α + iβ con α > 0' — espiral hacia afuera, color ámbar #f59e0b. "
            "Panel derecho 'Repetido defectivo λ' — nodo impropio con todas las trayectorias paralelas a un mismo eigendir, color púrpura. "
            "Cada panel con ejes x_1, x_2 y leyenda. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para que $\\mathbf{v} e^{\\lambda t}$ sea solución de $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$, $\\lambda$ debe satisfacer:",
                  "opciones_md": [
                      "$\\mathbf{A}\\mathbf{v} = \\mathbf{0}$",
                      "**$\\mathbf{A}\\mathbf{v} = \\lambda \\mathbf{v}$**",
                      "$\\det \\mathbf{A} = \\lambda$",
                      "$\\mathbf{v} \\cdot \\mathbf{A} = \\lambda$",
                  ],
                  "correcta": "B",
                  "pista_md": "Definición de valor propio.",
                  "explicacion_md": "Solo en esa dirección $\\mathbf{A}$ actúa como multiplicar por $\\lambda$.",
              },
              {
                  "enunciado_md": "Si $\\mathbf{A}$ es real con valor propio $\\lambda = 3 + 2 i$, también es valor propio:",
                  "opciones_md": [
                      "$3 - 2 i$ con vector propio igual a $\\mathbf{v}$",
                      "**$3 - 2 i$ con vector propio $\\bar{\\mathbf{v}}$**",
                      "$2 + 3 i$",
                      "Ningún otro",
                  ],
                  "correcta": "B",
                  "pista_md": "Conjugados conjugados.",
                  "explicacion_md": "Para matriz real, los autovalores complejos vienen en pares conjugados, con vectores propios conjugados.",
              },
              {
                  "enunciado_md": "Si $\\lambda$ es valor propio doble con $m_g = 1$, la segunda solución LI tiene la forma:",
                  "opciones_md": [
                      "$\\mathbf{v} e^{\\lambda t}$",
                      "**$(\\mathbf{v}\\, t + \\mathbf{w}) e^{\\lambda t}$ con $(\\mathbf{A} - \\lambda \\mathbf{I})\\mathbf{w} = \\mathbf{v}$**",
                      "$t \\mathbf{v} e^{\\lambda t}$ sin más",
                      "$\\mathbf{w} e^{\\lambda t}$ con $\\mathbf{w}$ ortogonal a $\\mathbf{v}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Vector propio generalizado.",
                  "explicacion_md": "Se necesita el término $\\mathbf{w}$ adicional para que la combinación satisfaga la EDO.",
              },
          ]),

        ej(
            "Reales distintos $3 \\times 3$",
            "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 1 & 0 & 0 \\\\ 0 & 2 & 0 \\\\ 0 & 0 & -1 \\end{pmatrix} \\mathbf{x}$.",
            ["Matriz diagonal: los valores propios son las entradas diagonales."],
            (
                "$\\lambda_1 = 1, \\lambda_2 = 2, \\lambda_3 = -1$ con $\\mathbf{v}_1 = e_1, \\mathbf{v}_2 = e_2, \\mathbf{v}_3 = e_3$.\n\n"
                "$\\mathbf{x}(t) = c_1 e_1 e^t + c_2 e_2 e^{2 t} + c_3 e_3 e^{-t}$. "
                "Cada componente evoluciona independientemente."
            ),
        ),

        ej(
            "Complejos puros (oscilador)",
            "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 0 & 1 \\\\ -1 & 0 \\end{pmatrix} \\mathbf{x}$.",
            ["$\\lambda = \\pm i$, $\\alpha = 0, \\beta = 1$."],
            (
                "Vector propio para $\\lambda = i$: $(-i, 1)$ vía $(\\mathbf{A} - i \\mathbf{I})\\mathbf{v} = 0 \\Rightarrow -i v_1 + v_2 = 0$, $\\mathbf{v} = (1, i)^T$. $\\mathbf{a} = (1, 0)^T$, $\\mathbf{b} = (0, 1)^T$.\n\n"
                "$\\mathbf{x}_R = (\\cos t, -\\sin t)^T$, $\\mathbf{x}_I = (\\sin t, \\cos t)^T$.\n\n"
                "$\\mathbf{x}(t) = c_1 (\\cos t, -\\sin t)^T + c_2 (\\sin t, \\cos t)^T$. **Trayectorias circulares (centro).**"
            ),
        ),

        ej(
            "Defectivo $3 \\times 3$",
            "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 5 & -3 & -2 \\\\ 8 & -5 & -4 \\\\ -4 & 3 & 3 \\end{pmatrix} \\mathbf{x}$, sabiendo que $\\lambda = 1$ tiene $m_a = 3, m_g = 1$ y $\\mathbf{v} = (1, 2, -1)^T$.",
            ["Cadena de longitud 3: $(\\mathbf{A} - \\mathbf{I})\\mathbf{w}_2 = \\mathbf{v}$, $(\\mathbf{A} - \\mathbf{I})\\mathbf{w}_3 = \\mathbf{w}_2$."],
            (
                "Resolviendo en cadena (cálculo) se obtiene, p. ej., $\\mathbf{w}_2 = (1, 1, 0)^T$, $\\mathbf{w}_3 = (0, 0, 0)^T$ — depende de la elección.\n\n"
                "**Solución general (forma):**\n\n"
                "$\\mathbf{x}(t) = e^t [c_1 \\mathbf{v} + c_2 (\\mathbf{v} t + \\mathbf{w}_2) + c_3 (\\mathbf{v} t^2 / 2 + \\mathbf{w}_2 t + \\mathbf{w}_3)]$. "
                "Las potencias $1, t, t^2$ aparecen naturalmente con la cadena de longitud 3."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar contar el conjugado de un valor propio complejo.** Cada par $\\lambda, \\bar\\lambda$ aporta **dos** soluciones reales, no cuatro.",
              "**Confundir multiplicidad algebraica con geométrica.** $m_a$ se cuenta del polinomio; $m_g$ es la dimensión del espacio propio.",
              "**Usar solo vectores propios cuando el caso es defectivo.** Falta el factor $t$; sin él, no se obtienen $n$ soluciones LI.",
              "**Olvidar separar parte real e imaginaria** y dejar la solución en forma compleja.",
              "**Equivocar el signo de $\\beta$ en la fórmula de soluciones complejas.** Por convención $\\beta > 0$ y se usa el vector propio del autovalor $\\alpha + i \\beta$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Idea:** $\\mathbf{x} = \\mathbf{v} e^{\\lambda t}$ es solución sii $\\mathbf{A}\\mathbf{v} = \\lambda \\mathbf{v}$.",
              "**Polinomio característico:** $\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = 0$, grado $n$, da $n$ valores propios contando multiplicidad.",
              "**Caso 1 (reales distintos):** $\\mathbf{x} = \\sum c_i \\mathbf{v}_i e^{\\lambda_i t}$.",
              "**Caso 2 (complejos $\\alpha \\pm i \\beta$):** dos soluciones reales $e^{\\alpha t}(\\mathbf{a} \\cos \\beta t \\mp \\mathbf{b} \\sin \\beta t)$ y $e^{\\alpha t}(\\mathbf{a} \\sin \\beta t \\pm \\mathbf{b} \\cos \\beta t)$.",
              "**Caso 3 (defectivo):** vector propio generalizado $(\\mathbf{A} - \\lambda \\mathbf{I})\\mathbf{w} = \\mathbf{v}$ y solución $(\\mathbf{v} t + \\mathbf{w}) e^{\\lambda t}$.",
              "**Próxima lección:** matriz fundamental y matriz exponencial $e^{\\mathbf{A} t}$.",
          ]),
    ]
    return {
        "id": "lec-ed-3-3-valores-propios",
        "title": "Método de valores propios",
        "description": "Resolución de sistemas lineales homogéneos con coeficientes constantes vía valores y vectores propios. Tres casos: reales distintos, complejos conjugados y repetidos defectivos.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
    }


# =====================================================================
# Matriz fundamental
# =====================================================================
def lesson_matriz_fundamental():
    blocks = [
        b("texto", body_md=(
            "Las $n$ soluciones LI de un sistema lineal homogéneo se pueden empaquetar en una **matriz** "
            "que las tenga como columnas. Esa matriz, llamada **matriz fundamental** $\\boldsymbol{\\Phi}(t)$, "
            "permite escribir la solución general en una forma extremadamente compacta:\n\n"
            "$$\\mathbf{x}(t) = \\boldsymbol{\\Phi}(t)\\, \\mathbf{c},$$\n\n"
            "y la solución del PVI con $\\mathbf{x}(t_0) = \\mathbf{x}_0$ como\n\n"
            "$$\\mathbf{x}(t) = \\boldsymbol{\\Phi}(t)\\, \\boldsymbol{\\Phi}(t_0)^{-1}\\, \\mathbf{x}_0.$$\n\n"
            "Cuando además normalizamos para que $\\boldsymbol{\\Phi}(0) = \\mathbf{I}$, obtenemos la "
            "**matriz exponencial** $e^{\\mathbf{A} t}$ — la generalización matricial natural de $e^{a t}$ "
            "del caso escalar.\n\n"
            "**Al terminar:**\n\n"
            "- Construyes la matriz fundamental $\\boldsymbol{\\Phi}(t)$ a partir del conjunto fundamental.\n"
            "- Resuelves PVIs con la fórmula $\\mathbf{x}(t) = \\boldsymbol{\\Phi}(t) \\boldsymbol{\\Phi}(t_0)^{-1} \\mathbf{x}_0$.\n"
            "- Defines $e^{\\mathbf{A} t}$ y conoces sus propiedades clave.\n"
            "- Calculas $e^{\\mathbf{A} t}$ vía $\\boldsymbol{\\Phi}(t) \\boldsymbol{\\Phi}(0)^{-1}$ o por diagonalización."
        )),

        b("definicion",
          titulo="Matriz fundamental",
          body_md=(
              "Sea $\\{\\mathbf{x}_1, \\ldots, \\mathbf{x}_n\\}$ un conjunto fundamental de "
              "$\\mathbf{x}' = \\mathbf{A}(t)\\mathbf{x}$. La **matriz fundamental** asociada es\n\n"
              "$$\\boldsymbol{\\Phi}(t) = \\bigl[\\, \\mathbf{x}_1(t) \\;\\big|\\; \\mathbf{x}_2(t) \\;\\big|\\; \\cdots \\;\\big|\\; \\mathbf{x}_n(t) \\,\\bigr],$$\n\n"
              "es decir, la matriz $n \\times n$ cuyas columnas son las $n$ soluciones LI.\n\n"
              "**Propiedades:**\n\n"
              "1. **Satisface la EDO matricial:** $\\boldsymbol{\\Phi}'(t) = \\mathbf{A}(t)\\, \\boldsymbol{\\Phi}(t)$.\n"
              "2. **Es invertible para todo $t$** (su determinante es el wronskiano, que no se anula).\n"
              "3. **Solución general:** $\\mathbf{x}(t) = \\boldsymbol{\\Phi}(t)\\, \\mathbf{c}$ con $\\mathbf{c} \\in \\mathbb{R}^n$.\n"
              "4. **Solución del PVI con $\\mathbf{x}(t_0) = \\mathbf{x}_0$:** $\\mathbf{x}(t) = \\boldsymbol{\\Phi}(t)\\, \\boldsymbol{\\Phi}(t_0)^{-1}\\, \\mathbf{x}_0$.\n\n"
              "**No única:** cualquier elección de conjunto fundamental da una matriz fundamental distinta. "
              "Dos matrices fundamentales se diferencian en una multiplicación a la derecha por una matriz "
              "constante invertible: $\\boldsymbol{\\Phi}_2(t) = \\boldsymbol{\\Phi}_1(t)\\, \\mathbf{C}$."
          )),

        b("definicion",
          titulo="Matriz exponencial",
          body_md=(
              "Para una matriz constante $\\mathbf{A}$ se define la **matriz exponencial**\n\n"
              "$$e^{\\mathbf{A} t} = \\sum_{k = 0}^{\\infty} \\dfrac{(\\mathbf{A} t)^k}{k!} = \\mathbf{I} + \\mathbf{A}\\, t + \\dfrac{\\mathbf{A}^2 t^2}{2!} + \\dfrac{\\mathbf{A}^3 t^3}{3!} + \\cdots$$\n\n"
              "(la serie converge absolutamente para todo $t \\in \\mathbb{R}$ y toda matriz $\\mathbf{A}$).\n\n"
              "**Propiedades fundamentales:**\n\n"
              "1. $e^{\\mathbf{A} \\cdot 0} = \\mathbf{I}$.\n"
              "2. $\\dfrac{d}{dt} e^{\\mathbf{A} t} = \\mathbf{A}\\, e^{\\mathbf{A} t} = e^{\\mathbf{A} t} \\mathbf{A}$.\n"
              "3. $(e^{\\mathbf{A} t})^{-1} = e^{-\\mathbf{A} t}$.\n"
              "4. **Si $\\mathbf{A}$ y $\\mathbf{B}$ conmutan** ($\\mathbf{A}\\mathbf{B} = \\mathbf{B}\\mathbf{A}$): $e^{(\\mathbf{A} + \\mathbf{B}) t} = e^{\\mathbf{A} t} e^{\\mathbf{B} t}$. **Si no conmutan, esto falla.**\n\n"
              "**Caracterización.** $e^{\\mathbf{A} t}$ es **la única matriz fundamental** de "
              "$\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$ que en $t = 0$ vale $\\mathbf{I}$.\n\n"
              "**Solución del PVI** $\\mathbf{x}(0) = \\mathbf{x}_0$:\n\n"
              "$$\\mathbf{x}(t) = e^{\\mathbf{A} t}\\, \\mathbf{x}_0.$$"
          )),

        formulas(
            titulo="Cómo calcular $e^{\\mathbf{A} t}$",
            body=(
                "Calcular la serie infinita es impracticable. Hay dos métodos prácticos:\n\n"
                "**Método 1 — Vía matriz fundamental.** Si $\\boldsymbol{\\Phi}(t)$ es **cualquier** matriz "
                "fundamental (por ejemplo, la que sale de valores propios):\n\n"
                "$$e^{\\mathbf{A} t} = \\boldsymbol{\\Phi}(t)\\, \\boldsymbol{\\Phi}(0)^{-1}.$$\n\n"
                "**Método 2 — Diagonalización.** Si $\\mathbf{A} = \\mathbf{P}\\, \\mathbf{D}\\, \\mathbf{P}^{-1}$ "
                "con $\\mathbf{D}$ diagonal de entradas $\\lambda_1, \\ldots, \\lambda_n$ y $\\mathbf{P}$ la "
                "matriz de vectores propios en columnas, entonces\n\n"
                "$$e^{\\mathbf{A} t} = \\mathbf{P}\\, e^{\\mathbf{D} t}\\, \\mathbf{P}^{-1}, \\qquad e^{\\mathbf{D} t} = \\operatorname{diag}(e^{\\lambda_1 t}, \\ldots, e^{\\lambda_n t}).$$\n\n"
                "**Caso defectivo.** Si $\\mathbf{A}$ no es diagonalizable, se usa la forma de Jordan o "
                "directamente el método 1 con la matriz fundamental que ya incluye los términos "
                "polinomiales-exponenciales del caso defectivo. La fórmula $e^{\\mathbf{A} t} = \\boldsymbol{\\Phi}(t) \\boldsymbol{\\Phi}(0)^{-1}$ siempre funciona."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Construir matriz fundamental",
          problema_md=(
              "Para el sistema $\\mathbf{x}' = \\begin{pmatrix} 4 & 2 \\\\ 3 & -1 \\end{pmatrix} \\mathbf{x}$ "
              "(del ejemplo de la lección anterior), construye una matriz fundamental y úsala para resolver "
              "el PVI $\\mathbf{x}(0) = (1, 0)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "**Conjunto fundamental** (de la lección anterior): $\\mathbf{x}_1 = (2, 1)^T e^{5 t}$, $\\mathbf{x}_2 = (1, -3)^T e^{-2 t}$.\n\n"
                  "**Matriz fundamental:**\n\n"
                  "$$\\boldsymbol{\\Phi}(t) = \\begin{pmatrix} 2 e^{5 t} & e^{-2 t} \\\\ e^{5 t} & -3 e^{-2 t} \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Cada columna es una solución LI.",
               "es_resultado": False},
              {"accion_md": (
                  "**Evaluar en $t = 0$:**\n\n"
                  "$$\\boldsymbol{\\Phi}(0) = \\begin{pmatrix} 2 & 1 \\\\ 1 & -3 \\end{pmatrix}, \\qquad \\det = -7.$$\n\n"
                  "$$\\boldsymbol{\\Phi}(0)^{-1} = -\\dfrac{1}{7}\\begin{pmatrix} -3 & -1 \\\\ -1 & 2 \\end{pmatrix} = \\dfrac{1}{7}\\begin{pmatrix} 3 & 1 \\\\ 1 & -2 \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Inversa $2 \\times 2$ por fórmula.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución del PVI:** $\\mathbf{x}(t) = \\boldsymbol{\\Phi}(t)\\, \\boldsymbol{\\Phi}(0)^{-1}\\, \\mathbf{x}_0$:\n\n"
                  "$\\boldsymbol{\\Phi}(0)^{-1} \\mathbf{x}_0 = \\dfrac{1}{7}\\begin{pmatrix} 3 \\\\ 1 \\end{pmatrix}$. Multiplicando por $\\boldsymbol{\\Phi}(t)$:\n\n"
                  "$$\\mathbf{x}(t) = \\dfrac{1}{7}\\begin{pmatrix} 6 e^{5 t} + e^{-2 t} \\\\ 3 e^{5 t} - 3 e^{-2 t} \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Equivalente a haber resuelto $c_1 (2, 1)^T + c_2 (1, -3)^T = (1, 0)^T$ y reemplazado.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Calcular $e^{\\mathbf{A} t}$",
          problema_md=(
              "Para la misma $\\mathbf{A} = \\begin{pmatrix} 4 & 2 \\\\ 3 & -1 \\end{pmatrix}$, calcula la matriz exponencial $e^{\\mathbf{A} t}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Aplicar la fórmula** $e^{\\mathbf{A} t} = \\boldsymbol{\\Phi}(t)\\, \\boldsymbol{\\Phi}(0)^{-1}$ con la matriz fundamental ya calculada:\n\n"
                  "$$e^{\\mathbf{A} t} = \\begin{pmatrix} 2 e^{5 t} & e^{-2 t} \\\\ e^{5 t} & -3 e^{-2 t} \\end{pmatrix} \\cdot \\dfrac{1}{7}\\begin{pmatrix} 3 & 1 \\\\ 1 & -2 \\end{pmatrix}.$$"
              ),
               "justificacion_md": "El producto da una matriz $2 \\times 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Multiplicar entrada por entrada:**\n\n"
                  "$$e^{\\mathbf{A} t} = \\dfrac{1}{7}\\begin{pmatrix} 6 e^{5 t} + e^{-2 t} & 2 e^{5 t} - 2 e^{-2 t} \\\\ 3 e^{5 t} - 3 e^{-2 t} & e^{5 t} + 6 e^{-2 t} \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Verificar: en $t = 0$ se obtiene $\\dfrac{1}{7}\\begin{pmatrix} 7 & 0 \\\\ 0 & 7 \\end{pmatrix} = \\mathbf{I}$. ✓",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución del PVI** con cualquier $\\mathbf{x}_0$: $\\mathbf{x}(t) = e^{\\mathbf{A} t} \\mathbf{x}_0$.\n\n"
                  "Por ejemplo, con $\\mathbf{x}_0 = (1, 0)^T$ recuperamos exactamente el resultado del ejemplo anterior."
              ),
               "justificacion_md": "$e^{\\mathbf{A} t}$ es la matriz fundamental 'canónica' (la que vale $\\mathbf{I}$ en $t = 0$).",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué $e^{\\mathbf{A} t}$ es la generalización correcta.** En el caso escalar $x' = a x$, la "
            "solución es $x(t) = e^{a t} x_0$. La matriz exponencial generaliza esa fórmula al caso "
            "vectorial: $\\mathbf{x}(t) = e^{\\mathbf{A} t} \\mathbf{x}_0$.\n\n"
            "**Cuando $\\mathbf{A}$ es diagonalizable.** Si $\\mathbf{A} = \\mathbf{P}\\mathbf{D}\\mathbf{P}^{-1}$, "
            "entonces $\\mathbf{A}^k = \\mathbf{P}\\mathbf{D}^k\\mathbf{P}^{-1}$. Sustituyendo en la serie y "
            "factorizando, sale $e^{\\mathbf{A} t} = \\mathbf{P} e^{\\mathbf{D} t} \\mathbf{P}^{-1}$. Es decir, "
            "**diagonalizar** convierte el problema vectorial en $n$ problemas escalares desacoplados — uno "
            "por cada autovalor.\n\n"
            "**Atención al cuidado del producto.** $e^{\\mathbf{A} + \\mathbf{B}} = e^{\\mathbf{A}} e^{\\mathbf{B}}$ "
            "**solo si $\\mathbf{A}\\mathbf{B} = \\mathbf{B}\\mathbf{A}$**. En general las matrices no conmutan, "
            "y esa es la razón profunda por la cual no se puede 'integrar' el factor matricial $\\mathbf{A}(t)$ "
            "como si fuera escalar para resolver $\\mathbf{x}' = \\mathbf{A}(t) \\mathbf{x}$ con coeficientes variables."
        )),

        fig(
            "Diagrama conmutativo de la diagonalización aplicada a la exponencial. "
            "Cuatro cajas dispuestas en cuadrado: arriba izquierda 'A', arriba derecha 'e^{At}', abajo izquierda 'D = P^{-1} A P', abajo derecha 'e^{Dt}'. "
            "Flechas: arriba 'exponencial' (de A a e^{At}), abajo 'exponencial' (de D a e^{Dt}, fácil porque D es diagonal). "
            "Flechas verticales etiquetadas 'P^{-1} (·) P' a la izquierda y 'P (·) P^{-1}' a la derecha. "
            "Acentos teal #06b6d4 en las matrices originales y ámbar #f59e0b en las exponenciales. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\boldsymbol{\\Phi}(t)$ es matriz fundamental, la solución del PVI $\\mathbf{x}(t_0) = \\mathbf{x}_0$ es:",
                  "opciones_md": [
                      "$\\mathbf{x} = \\boldsymbol{\\Phi}(t) \\mathbf{x}_0$",
                      "**$\\mathbf{x} = \\boldsymbol{\\Phi}(t) \\boldsymbol{\\Phi}(t_0)^{-1} \\mathbf{x}_0$**",
                      "$\\mathbf{x} = \\boldsymbol{\\Phi}(t_0) \\mathbf{x}_0$",
                      "$\\mathbf{x} = \\boldsymbol{\\Phi}(t)^{-1} \\mathbf{x}_0$",
                  ],
                  "correcta": "B",
                  "pista_md": "El factor $\\boldsymbol{\\Phi}(t_0)^{-1}$ ajusta para que la condición inicial se cumpla.",
                  "explicacion_md": "Es equivalente a resolver $\\boldsymbol{\\Phi}(t_0) \\mathbf{c} = \\mathbf{x}_0$ y luego computar $\\mathbf{x} = \\boldsymbol{\\Phi}(t) \\mathbf{c}$.",
              },
              {
                  "enunciado_md": "$e^{\\mathbf{A} t}$ es la matriz fundamental que en $t = 0$ vale:",
                  "opciones_md": [
                      "$\\mathbf{0}$",
                      "**$\\mathbf{I}$**",
                      "$\\mathbf{A}$",
                      "$\\mathbf{A}^{-1}$",
                  ],
                  "correcta": "B",
                  "pista_md": "$e^{\\mathbf{A} \\cdot 0} = ?$",
                  "explicacion_md": "$e^{\\mathbf{A} \\cdot 0} = \\mathbf{I}$ por la serie ($k = 0$ da $\\mathbf{I}$, los demás términos son $\\mathbf{0}$).",
              },
              {
                  "enunciado_md": "$e^{\\mathbf{A} + \\mathbf{B}} = e^{\\mathbf{A}} e^{\\mathbf{B}}$ se cumple:",
                  "opciones_md": [
                      "Siempre",
                      "Nunca",
                      "**Solo si $\\mathbf{A}\\mathbf{B} = \\mathbf{B}\\mathbf{A}$**",
                      "Si $\\mathbf{A}$ y $\\mathbf{B}$ son simétricas",
                  ],
                  "correcta": "C",
                  "pista_md": "Las matrices generalmente no conmutan.",
                  "explicacion_md": "La igualdad requiere conmutatividad. La simetría no basta — dos matrices simétricas pueden no conmutar.",
              },
          ]),

        ej(
            "Diagonalización a mano",
            "Calcula $e^{\\mathbf{A} t}$ para $\\mathbf{A} = \\begin{pmatrix} 1 & 0 \\\\ 0 & 2 \\end{pmatrix}$.",
            ["$\\mathbf{A}$ ya es diagonal."],
            (
                "$e^{\\mathbf{A} t} = \\begin{pmatrix} e^t & 0 \\\\ 0 & e^{2 t} \\end{pmatrix}$. La matriz exponencial de una diagonal es la diagonal de las exponenciales."
            ),
        ),

        ej(
            "Caso oscilatorio",
            "Sabiendo que para $\\mathbf{A} = \\begin{pmatrix} 0 & 1 \\\\ -1 & 0 \\end{pmatrix}$ las soluciones reales son $(\\cos t, -\\sin t)^T$ y $(\\sin t, \\cos t)^T$, calcula $e^{\\mathbf{A} t}$.",
            ["$\\boldsymbol{\\Phi}(0) = \\mathbf{I}$ por construcción."],
            (
                "$\\boldsymbol{\\Phi}(t) = \\begin{pmatrix} \\cos t & \\sin t \\\\ -\\sin t & \\cos t \\end{pmatrix}$. En $t = 0$: $\\mathbf{I}$. Así $e^{\\mathbf{A} t} = \\boldsymbol{\\Phi}(t)$ directamente: una **matriz de rotación**."
            ),
        ),

        ej(
            "PVI con matriz fundamental",
            "Dada $\\boldsymbol{\\Phi}(t) = \\begin{pmatrix} e^{2 t} & e^{-t} \\\\ e^{2 t} & -2 e^{-t} \\end{pmatrix}$ matriz fundamental, halla la solución con $\\mathbf{x}(0) = (3, 0)^T$.",
            ["$\\mathbf{c} = \\boldsymbol{\\Phi}(0)^{-1} \\mathbf{x}_0$."],
            (
                "$\\boldsymbol{\\Phi}(0) = \\begin{pmatrix} 1 & 1 \\\\ 1 & -2 \\end{pmatrix}$, $\\det = -3$, $\\boldsymbol{\\Phi}(0)^{-1} = \\dfrac{1}{3}\\begin{pmatrix} 2 & 1 \\\\ 1 & -1 \\end{pmatrix}$.\n\n"
                "$\\mathbf{c} = \\boldsymbol{\\Phi}(0)^{-1} (3, 0)^T = (2, 1)^T$.\n\n"
                "$\\mathbf{x}(t) = 2 (e^{2 t}, e^{2 t})^T + (e^{-t}, -2 e^{-t})^T = (2 e^{2 t} + e^{-t}, 2 e^{2 t} - 2 e^{-t})^T$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $e^{\\mathbf{A} t}$ con la exponenciación entrada por entrada de $\\mathbf{A} t$.** Son cosas distintas: $e^{\\mathbf{A} t}$ es una matriz que se calcula con la serie o con $\\boldsymbol{\\Phi}(t) \\boldsymbol{\\Phi}(0)^{-1}$.",
              "**Olvidar invertir $\\boldsymbol{\\Phi}(t_0)$** al resolver un PVI.",
              "**Aplicar $e^{\\mathbf{A} + \\mathbf{B}} = e^{\\mathbf{A}} e^{\\mathbf{B}}$ sin verificar conmutatividad.**",
              "**Pensar que la matriz fundamental es única.** Cualquier elección de conjunto fundamental da una matriz válida.",
              "**Para sistemas defectivos, usar solo $\\mathbf{P} e^{\\mathbf{D} t} \\mathbf{P}^{-1}$ — no funciona porque no hay $\\mathbf{P}$ invertible de vectores propios.** Usar el método 1 (matriz fundamental con términos polinomiales).",
          ]),

        b("resumen",
          puntos_md=[
              "**Matriz fundamental:** $\\boldsymbol{\\Phi}(t) = [\\mathbf{x}_1 \\mid \\cdots \\mid \\mathbf{x}_n]$ con $\\mathbf{x}_i$ conjunto fundamental.",
              "**Solución general:** $\\mathbf{x} = \\boldsymbol{\\Phi}(t) \\mathbf{c}$. **Solución del PVI:** $\\mathbf{x} = \\boldsymbol{\\Phi}(t) \\boldsymbol{\\Phi}(t_0)^{-1} \\mathbf{x}_0$.",
              "**Matriz exponencial:** $e^{\\mathbf{A} t} = \\sum_k (\\mathbf{A} t)^k / k!$, única matriz fundamental con $\\boldsymbol{\\Phi}(0) = \\mathbf{I}$.",
              "**Cálculo:** $e^{\\mathbf{A} t} = \\boldsymbol{\\Phi}(t) \\boldsymbol{\\Phi}(0)^{-1}$ (cualquier matriz fundamental sirve) o por diagonalización si $\\mathbf{A}$ es diagonalizable.",
              "**Próxima lección:** sistemas no homogéneos $\\mathbf{x}' = \\mathbf{A}\\mathbf{x} + \\mathbf{f}(t)$ — coeficientes indeterminados y variación de parámetros matricial.",
          ]),
    ]
    return {
        "id": "lec-ed-3-4-matriz-fundamental",
        "title": "Matriz fundamental",
        "description": "Matriz fundamental de un sistema lineal: definición, propiedades y uso para resolver PVIs. Matriz exponencial e^{At}: definición, propiedades y métodos de cálculo (vía matriz fundamental, diagonalización).",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# Sistemas no homogéneos
# =====================================================================
def lesson_no_homogeneos():
    blocks = [
        b("texto", body_md=(
            "Pasamos al caso **no homogéneo**:\n\n"
            "$$\\mathbf{x}'(t) = \\mathbf{A}(t)\\, \\mathbf{x}(t) + \\mathbf{f}(t),$$\n\n"
            "con $\\mathbf{f}(t)$ vector dado distinto del cero. Por linealidad, la solución general tiene la "
            "estructura\n\n"
            "$$\\mathbf{x}(t) = \\mathbf{x}_c(t) + \\mathbf{x}_p(t),$$\n\n"
            "donde $\\mathbf{x}_c$ es la solución general del sistema homogéneo asociado y $\\mathbf{x}_p$ "
            "**alguna** solución particular del no homogéneo.\n\n"
            "Hay dos métodos análogos a los del caso escalar:\n\n"
            "- **Coeficientes indeterminados** — adivinar la forma de $\\mathbf{x}_p$ a partir de la forma de $\\mathbf{f}$.\n"
            "- **Variación de parámetros** — método universal con la matriz fundamental.\n\n"
            "**Al terminar:**\n\n"
            "- Aplicas **coeficientes indeterminados** a sistemas con $\\mathbf{f}$ polinomial, exponencial o trigonométrico.\n"
            "- Manejas la **regla de modificación** cuando hay resonancia con autovalores.\n"
            "- Aplicas la **fórmula de variación de parámetros** $\\mathbf{x}_p = \\boldsymbol{\\Phi}(t) \\int \\boldsymbol{\\Phi}(s)^{-1} \\mathbf{f}(s)\\, ds$."
        )),

        b("definicion",
          titulo="Estructura $\\mathbf{x} = \\mathbf{x}_c + \\mathbf{x}_p$",
          body_md=(
              "**Teorema.** Sea $\\mathbf{x}_p$ una solución particular del sistema "
              "$\\mathbf{x}' = \\mathbf{A}(t) \\mathbf{x} + \\mathbf{f}(t)$ y $\\mathbf{x}_c$ la solución "
              "general del homogéneo $\\mathbf{x}' = \\mathbf{A}(t) \\mathbf{x}$. Entonces toda solución del "
              "no homogéneo se escribe como\n\n"
              "$$\\mathbf{x}(t) = \\mathbf{x}_c(t) + \\mathbf{x}_p(t).$$\n\n"
              "**Demostración.** Si $\\mathbf{x}, \\mathbf{x}_p$ son soluciones del no homogéneo, "
              "$\\mathbf{x} - \\mathbf{x}_p$ satisface el homogéneo, así $\\mathbf{x} - \\mathbf{x}_p = \\mathbf{x}_c$.\n\n"
              "**Procedimiento:**\n\n"
              "1. Resolver el sistema homogéneo (con valores propios) para obtener $\\mathbf{x}_c$.\n"
              "2. Encontrar $\\mathbf{x}_p$ por coeficientes indeterminados o variación de parámetros.\n"
              "3. Escribir $\\mathbf{x} = \\mathbf{x}_c + \\mathbf{x}_p$.\n"
              "4. Si hay PVI, aplicar la condición inicial sobre la suma."
          )),

        formulas(
            titulo="Coeficientes indeterminados (vectorial)",
            body=(
                "Para $\\mathbf{f}(t)$ con forma especial, se propone $\\mathbf{x}_p$ con la **misma forma** "
                "pero coeficientes vectoriales a determinar:\n\n"
                "**Si $\\mathbf{f}(t) = \\mathbf{b}$ (constante):** propuesta $\\mathbf{x}_p = \\mathbf{k}$ vector constante. Sustituyendo $\\mathbf{0} = \\mathbf{A} \\mathbf{k} + \\mathbf{b}$, así $\\mathbf{k} = -\\mathbf{A}^{-1} \\mathbf{b}$ (si $\\mathbf{A}$ invertible).\n\n"
                "**Si $\\mathbf{f}(t) = \\mathbf{b}\\, e^{r t}$:**\n\n"
                "- Si $r$ **no** es valor propio de $\\mathbf{A}$: $\\mathbf{x}_p = \\mathbf{k}\\, e^{r t}$, con $\\mathbf{k} = (r \\mathbf{I} - \\mathbf{A})^{-1} \\mathbf{b}$.\n"
                "- Si $r$ **es** valor propio (resonancia): multiplicar la propuesta por $t$ — y a veces más términos: $\\mathbf{x}_p = (\\mathbf{k}_1\\, t + \\mathbf{k}_0)\\, e^{r t}$.\n\n"
                "**Si $\\mathbf{f}(t) = \\mathbf{a}\\cos \\omega t + \\mathbf{b} \\sin \\omega t$:** propuesta $\\mathbf{x}_p = \\mathbf{k} \\cos \\omega t + \\mathbf{m} \\sin \\omega t$ con $2 n$ incógnitas; sale un sistema lineal $2 n \\times 2 n$.\n\n"
                "**Polinomio:** propuesta polinomial vectorial del mismo grado.\n\n"
                "**Superposición:** si $\\mathbf{f} = \\mathbf{f}_1 + \\mathbf{f}_2$, sumar $\\mathbf{x}_{p, 1} + \\mathbf{x}_{p, 2}$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Coeficientes indeterminados — exponencial sin resonancia",
          problema_md=(
              "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 1 & 1 \\\\ 0 & -1 \\end{pmatrix} \\mathbf{x} + \\begin{pmatrix} e^{2 t} \\\\ 0 \\end{pmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Sistema homogéneo.** $\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = (1 - \\lambda)(-1 - \\lambda) = 0 \\Rightarrow \\lambda = \\pm 1$.\n\n"
                  "Vectores propios: $\\mathbf{v}_1 = (1, 0)^T$ para $\\lambda = 1$, $\\mathbf{v}_2 = (1, -2)^T$ para $\\lambda = -1$.\n\n"
                  "$\\mathbf{x}_c = c_1 (1, 0)^T e^t + c_2 (1, -2)^T e^{-t}$."
              ),
               "justificacion_md": "Reales distintos, sin resonancia con $r = 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Propuesta.** $r = 2$ no es valor propio. $\\mathbf{x}_p = (k_1, k_2)^T e^{2 t}$. "
                  "Sustituyendo: $2 (k_1, k_2)^T = \\mathbf{A} (k_1, k_2)^T + (1, 0)^T$.\n\n"
                  "Es decir, $(2 k_1, 2 k_2)^T = (k_1 + k_2 + 1, -k_2)^T$. De la segunda: $3 k_2 = 0 \\Rightarrow k_2 = 0$. De la primera: $k_1 = k_1 + 0 + 1 - k_1 = ?$\n\n"
                  "Reordenando: $2 k_1 = k_1 + k_2 + 1$, $2 k_2 = -k_2$. Da $k_2 = 0$, $k_1 = k_2 + 1 = 1$.\n\n"
                  "$\\mathbf{x}_p = (1, 0)^T e^{2 t}$."
              ),
               "justificacion_md": "Sistema $2 \\times 2$ en $k_1, k_2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:**\n\n"
                  "$$\\mathbf{x}(t) = c_1 \\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix} e^t + c_2 \\begin{pmatrix} 1 \\\\ -2 \\end{pmatrix} e^{-t} + \\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix} e^{2 t}.$$"
              ),
               "justificacion_md": "Sistema completo: $\\mathbf{x}_c$ con dos constantes más $\\mathbf{x}_p$.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Variación de parámetros (vectorial)",
            body=(
                "**Idea.** Conocemos una matriz fundamental $\\boldsymbol{\\Phi}(t)$ del homogéneo. Proponemos\n\n"
                "$$\\mathbf{x}_p(t) = \\boldsymbol{\\Phi}(t)\\, \\mathbf{u}(t),$$\n\n"
                "con $\\mathbf{u}(t)$ vector de funciones a determinar. Sustituyendo en la EDO no homogénea y "
                "usando que $\\boldsymbol{\\Phi}' = \\mathbf{A} \\boldsymbol{\\Phi}$ se llega a\n\n"
                "$$\\boldsymbol{\\Phi}(t)\\, \\mathbf{u}'(t) = \\mathbf{f}(t) \\;\\Longrightarrow\\; \\mathbf{u}'(t) = \\boldsymbol{\\Phi}(t)^{-1}\\, \\mathbf{f}(t).$$\n\n"
                "Integrando y multiplicando por $\\boldsymbol{\\Phi}(t)$:\n\n"
                "$$\\boxed{\\,\\mathbf{x}_p(t) = \\boldsymbol{\\Phi}(t) \\int \\boldsymbol{\\Phi}(s)^{-1}\\, \\mathbf{f}(s)\\, ds.\\,}$$\n\n"
                "**Solución del PVI** $\\mathbf{x}(t_0) = \\mathbf{x}_0$:\n\n"
                "$$\\mathbf{x}(t) = \\boldsymbol{\\Phi}(t) \\boldsymbol{\\Phi}(t_0)^{-1} \\mathbf{x}_0 + \\boldsymbol{\\Phi}(t) \\int_{t_0}^t \\boldsymbol{\\Phi}(s)^{-1}\\, \\mathbf{f}(s)\\, ds.$$\n\n"
                "**Versión con la matriz exponencial** ($\\mathbf{A}$ constante):\n\n"
                "$$\\mathbf{x}(t) = e^{\\mathbf{A} (t - t_0)}\\, \\mathbf{x}_0 + \\int_{t_0}^t e^{\\mathbf{A} (t - s)}\\, \\mathbf{f}(s)\\, ds.$$\n\n"
                "**Funciona para cualquier $\\mathbf{f}(t)$ continua** — no solo las formas de la tabla. "
                "El precio: hay que invertir $\\boldsymbol{\\Phi}(t)$ e integrar."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Variación de parámetros",
          problema_md=(
              "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 0 & 1 \\\\ -1 & 0 \\end{pmatrix} \\mathbf{x} + \\begin{pmatrix} 1 \\\\ t \\end{pmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Sistema homogéneo.** Valores propios $\\pm i$, soluciones reales $(\\cos t, -\\sin t)^T$ y $(\\sin t, \\cos t)^T$.\n\n"
                  "Matriz fundamental: $\\boldsymbol{\\Phi}(t) = \\begin{pmatrix} \\cos t & \\sin t \\\\ -\\sin t & \\cos t \\end{pmatrix}$.\n\n"
                  "$\\det \\boldsymbol{\\Phi} = 1$, así $\\boldsymbol{\\Phi}^{-1}(t) = \\begin{pmatrix} \\cos t & -\\sin t \\\\ \\sin t & \\cos t \\end{pmatrix}$."
              ),
               "justificacion_md": "Es la matriz de rotación, invertirla es transponerla.",
               "es_resultado": False},
              {"accion_md": (
                  "**Producto $\\boldsymbol{\\Phi}^{-1}(s) \\mathbf{f}(s)$:**\n\n"
                  "$$\\begin{pmatrix} \\cos s & -\\sin s \\\\ \\sin s & \\cos s \\end{pmatrix} \\begin{pmatrix} 1 \\\\ s \\end{pmatrix} = \\begin{pmatrix} \\cos s - s \\sin s \\\\ \\sin s + s \\cos s \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Cálculo directo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Integrar componente a componente.** Notar que $\\dfrac{d}{ds}(s \\cos s) = \\cos s - s \\sin s$ y $\\dfrac{d}{ds}(s \\sin s) = \\sin s + s \\cos s$. Así\n\n"
                  "$$\\int \\begin{pmatrix} \\cos s - s \\sin s \\\\ \\sin s + s \\cos s \\end{pmatrix} ds = \\begin{pmatrix} s \\cos s \\\\ s \\sin s \\end{pmatrix}.$$"
              ),
               "justificacion_md": "Antiderivada exacta sin necesidad de integración por partes adicional.",
               "es_resultado": False},
              {"accion_md": (
                  "**Multiplicar por $\\boldsymbol{\\Phi}(t)$:**\n\n"
                  "$$\\mathbf{x}_p(t) = \\begin{pmatrix} \\cos t & \\sin t \\\\ -\\sin t & \\cos t \\end{pmatrix} \\begin{pmatrix} t \\cos t \\\\ t \\sin t \\end{pmatrix} = \\begin{pmatrix} t \\cos^2 t + t \\sin^2 t \\\\ -t \\sin t \\cos t + t \\cos t \\sin t \\end{pmatrix} = \\begin{pmatrix} t \\\\ 0 \\end{pmatrix}.$$\n\n"
                  "**Solución general:** $\\mathbf{x}(t) = c_1 (\\cos t, -\\sin t)^T + c_2 (\\sin t, \\cos t)^T + (t, 0)^T$."
              ),
               "justificacion_md": "La identidad pitagórica simplifica enormemente.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Coeficientes indeterminados vs. variación de parámetros.** Igual que en el caso escalar:\n\n"
            "- **Coeficientes indeterminados:** rápido cuando $\\mathbf{f}$ tiene forma 'estándar' (polinomial, "
            "exponencial, trigonométrica), no requiere integrar. Limitación: hay que reconocer la forma y "
            "manejar resonancia.\n"
            "- **Variación de parámetros:** general, funciona para cualquier $\\mathbf{f}$ continua, pero "
            "requiere invertir $\\boldsymbol{\\Phi}(t)$ e integrar — más caro computacionalmente.\n\n"
            "**Resonancia en sistemas.** Cuando $\\mathbf{f}(t) = \\mathbf{b}\\, e^{\\lambda t}$ y $\\lambda$ "
            "es valor propio de $\\mathbf{A}$, la propuesta $\\mathbf{k}\\, e^{\\lambda t}$ no funciona — hay "
            "que multiplicar por $t$. Es exactamente lo mismo que pasa en EDOs escalares con raíz repetida."
        )),

        fig(
            "Diagrama del flujo de variación de parámetros para sistemas. "
            "Caja superior: sistema 'x' = A x + f(t)'. "
            "Flecha hacia abajo etiquetada 'Resolver homogéneo' lleva a 'Φ(t) matriz fundamental'. "
            "Flecha hacia abajo etiquetada 'Aplicar fórmula' lleva a 'x_p = Φ(t) ∫ Φ(s)⁻¹ f(s) ds'. "
            "Caja final: 'x = Φ(t) c + x_p' en ámbar #f59e0b. "
            "Acento teal #06b6d4 en las cajas intermedias. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La estructura general de la solución de $\\mathbf{x}' = \\mathbf{A} \\mathbf{x} + \\mathbf{f}(t)$ es:",
                  "opciones_md": [
                      "$\\mathbf{x} = \\mathbf{x}_p$",
                      "$\\mathbf{x} = \\mathbf{x}_c$",
                      "**$\\mathbf{x} = \\mathbf{x}_c + \\mathbf{x}_p$**",
                      "$\\mathbf{x} = \\mathbf{x}_c \\cdot \\mathbf{x}_p$",
                  ],
                  "correcta": "C",
                  "pista_md": "Linealidad.",
                  "explicacion_md": "Suma, no producto. La parte homogénea aporta los grados de libertad para PVI.",
              },
              {
                  "enunciado_md": "La fórmula de variación de parámetros para sistemas dice $\\mathbf{x}_p = $:",
                  "opciones_md": [
                      "$\\boldsymbol{\\Phi}(t) \\mathbf{f}(t)$",
                      "**$\\boldsymbol{\\Phi}(t) \\int \\boldsymbol{\\Phi}(s)^{-1} \\mathbf{f}(s) ds$**",
                      "$\\int \\mathbf{A} \\mathbf{f}(t) dt$",
                      "$\\boldsymbol{\\Phi}(t)^{-1} \\mathbf{f}(t)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Análoga vectorial de la fórmula del caso escalar.",
                  "explicacion_md": "$\\boldsymbol{\\Phi}^{-1}$ se aplica a $\\mathbf{f}$, se integra, y luego se multiplica a la izquierda por $\\boldsymbol{\\Phi}$.",
              },
              {
                  "enunciado_md": "Si $\\mathbf{f}(t) = \\mathbf{b}\\, e^{\\lambda t}$ y $\\lambda$ es valor propio de $\\mathbf{A}$, entonces:",
                  "opciones_md": [
                      "Coeficientes indeterminados no aplica",
                      "**Hay resonancia: la propuesta debe llevar factor $t$**",
                      "El sistema no tiene solución",
                      "Se debe usar diagonalización",
                  ],
                  "correcta": "B",
                  "pista_md": "Igual que en el caso escalar.",
                  "explicacion_md": "$\\mathbf{x}_p = (\\mathbf{k}_1 t + \\mathbf{k}_0) e^{\\lambda t}$, con $\\mathbf{k}_1$ vector propio asociado a $\\lambda$.",
              },
          ]),

        ej(
            "Constante",
            "Resuelve $\\mathbf{x}' = \\begin{pmatrix} -2 & 1 \\\\ 0 & -3 \\end{pmatrix} \\mathbf{x} + \\begin{pmatrix} 1 \\\\ 6 \\end{pmatrix}$.",
            ["$\\mathbf{x}_p$ constante: resolver $\\mathbf{A} \\mathbf{k} + \\mathbf{b} = 0$."],
            (
                "$\\mathbf{x}_c$: $\\lambda_1 = -2, \\lambda_2 = -3$, $\\mathbf{v}_1 = (1, 0)^T, \\mathbf{v}_2 = (1, -1)^T$. $\\mathbf{x}_c = c_1 (1, 0)^T e^{-2t} + c_2 (1, -1)^T e^{-3t}$.\n\n"
                "$\\mathbf{x}_p$: $\\mathbf{A} \\mathbf{k} = -\\mathbf{b}$ es $\\begin{pmatrix} -2 & 1 \\\\ 0 & -3 \\end{pmatrix} \\mathbf{k} = -\\begin{pmatrix} 1 \\\\ 6 \\end{pmatrix}$. Fila 2: $-3 k_2 = -6 \\Rightarrow k_2 = 2$. Fila 1: $-2 k_1 + 2 = -1 \\Rightarrow k_1 = 3/2$.\n\n"
                "**Solución:** $\\mathbf{x} = \\mathbf{x}_c + (3/2, 2)^T$."
            ),
        ),

        ej(
            "Trigonométrico",
            "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 0 & 1 \\\\ -2 & -3 \\end{pmatrix} \\mathbf{x} + \\begin{pmatrix} 0 \\\\ \\cos t \\end{pmatrix}$.",
            ["$\\mathbf{x}_p = \\mathbf{k} \\cos t + \\mathbf{m} \\sin t$. Sistema $4 \\times 4$ en componentes."],
            (
                "Homogéneo: $\\lambda^2 + 3\\lambda + 2 = (\\lambda + 1)(\\lambda + 2) = 0 \\Rightarrow \\lambda = -1, -2$. Vectores propios: $(1, -1)^T$ y $(1, -2)^T$.\n\n"
                "Sin resonancia con $i$. Propuesta $\\mathbf{x}_p = \\mathbf{k} \\cos t + \\mathbf{m} \\sin t$. Sustituyendo y agrupando se obtiene un sistema $4 \\times 4$ en $k_1, k_2, m_1, m_2$ que se resuelve por sustitución.\n\n"
                "**Solución general:** $\\mathbf{x} = c_1 (1, -1)^T e^{-t} + c_2 (1, -2)^T e^{-2 t} + \\mathbf{x}_p$ con los valores numéricos del sistema."
            ),
        ),

        ej(
            "Variación de parámetros",
            "Resuelve $\\mathbf{x}' = \\begin{pmatrix} 1 & 0 \\\\ 0 & -1 \\end{pmatrix} \\mathbf{x} + \\begin{pmatrix} 1 \\\\ e^t \\end{pmatrix}$.",
            ["Sistema desacoplado: matriz fundamental $\\boldsymbol{\\Phi} = \\operatorname{diag}(e^t, e^{-t})$."],
            (
                "$\\boldsymbol{\\Phi} = \\operatorname{diag}(e^t, e^{-t})$, $\\boldsymbol{\\Phi}^{-1} = \\operatorname{diag}(e^{-t}, e^t)$.\n\n"
                "$\\boldsymbol{\\Phi}^{-1} \\mathbf{f} = (e^{-t}, e^t \\cdot e^t)^T = (e^{-t}, e^{2t})^T$. Integrando: $(-e^{-t}, e^{2t}/2)^T$.\n\n"
                "$\\mathbf{x}_p = \\boldsymbol{\\Phi} \\cdot \\text{(integral)} = (e^t \\cdot (-e^{-t}), e^{-t} \\cdot e^{2t}/2)^T = (-1, e^t / 2)^T$.\n\n"
                "**Solución:** $\\mathbf{x} = c_1 (1, 0)^T e^t + c_2 (0, 1)^T e^{-t} + (-1, e^t / 2)^T$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $t$ en resonancia.** Sin él, la propuesta no funciona y aparecen contradicciones.",
              "**Imponer condiciones iniciales sobre $\\mathbf{x}_c$ sin sumar $\\mathbf{x}_p(t_0)$.** Hay que aplicarlas sobre la suma.",
              "**Olvidar invertir $\\boldsymbol{\\Phi}(t)$** en la fórmula de variación de parámetros.",
              "**Confundir $\\boldsymbol{\\Phi}(s)^{-1}$ con $\\boldsymbol{\\Phi}^{-1}(s)$ — son lo mismo, pero hay que evaluar antes o después de invertir consistentemente.**",
              "**Dejar la solución sin sumar $\\mathbf{x}_c$** y reportar solo $\\mathbf{x}_p$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Estructura:** $\\mathbf{x} = \\mathbf{x}_c + \\mathbf{x}_p$.",
              "**Coeficientes indeterminados (vectorial):** propuesta con la forma de $\\mathbf{f}$ y coeficientes vectoriales. Resonancia $\\Rightarrow$ multiplicar por $t$.",
              "**Variación de parámetros (vectorial):** $\\mathbf{x}_p = \\boldsymbol{\\Phi}(t) \\int \\boldsymbol{\\Phi}(s)^{-1} \\mathbf{f}(s)\\, ds$.",
              "**Versión exponencial:** $\\mathbf{x}(t) = e^{\\mathbf{A}(t - t_0)} \\mathbf{x}_0 + \\int_{t_0}^t e^{\\mathbf{A}(t - s)} \\mathbf{f}(s) ds$.",
              "**Próxima lección:** análisis cualitativo — equilibrios y estabilidad de sistemas planares.",
          ]),
    ]
    return {
        "id": "lec-ed-3-5-no-homogeneos",
        "title": "Sistemas no homogéneos",
        "description": "Sistemas lineales no homogéneos x' = Ax + f(t): estructura x = x_c + x_p, método de coeficientes indeterminados (con resonancia) y variación de parámetros vectorial con la matriz fundamental.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 5,
    }


# =====================================================================
# Estabilidad
# =====================================================================
def lesson_estabilidad():
    blocks = [
        b("texto", body_md=(
            "Cerramos el capítulo con el análisis **cualitativo** de los sistemas autónomos\n\n"
            "$$\\mathbf{x}'(t) = \\mathbf{A}\\, \\mathbf{x}(t).$$\n\n"
            "En vez de resolver explícitamente, queremos describir **el comportamiento global** de las "
            "trayectorias en el **plano de fase** (caso $n = 2$): ¿se acercan al origen? ¿se alejan? ¿giran?\n\n"
            "El resultado central: **el comportamiento cualitativo está completamente determinado por los "
            "valores propios de $\\mathbf{A}$**. Cada combinación de signos y tipos genera un retrato de "
            "fase distinto — nodo, silla, espiral, centro, nodo impropio.\n\n"
            "**Al terminar:**\n\n"
            "- Encuentras los **puntos de equilibrio** (puntos donde $\\mathbf{x}' = \\mathbf{0}$).\n"
            "- Defines **estabilidad** y **estabilidad asintótica** del origen.\n"
            "- Clasificas el equilibrio del origen según los autovalores de $\\mathbf{A}$ en sistemas planares.\n"
            "- Dibujas el **retrato de fase** correspondiente."
        )),

        b("definicion",
          titulo="Punto de equilibrio",
          body_md=(
              "Un **punto de equilibrio** (o crítico, o estacionario) del sistema $\\mathbf{x}' = \\mathbf{F}(\\mathbf{x})$ "
              "es un $\\mathbf{x}^* \\in \\mathbb{R}^n$ tal que $\\mathbf{F}(\\mathbf{x}^*) = \\mathbf{0}$.\n\n"
              "**Para sistemas lineales** $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$, los equilibrios son las "
              "soluciones de $\\mathbf{A}\\mathbf{x}^* = \\mathbf{0}$:\n\n"
              "- Si $\\det \\mathbf{A} \\neq 0$, el **único** equilibrio es $\\mathbf{x}^* = \\mathbf{0}$.\n"
              "- Si $\\det \\mathbf{A} = 0$, hay un subespacio de equilibrios (la kernel).\n\n"
              "En el caso típico nos centramos en el **origen** y analizamos qué hacen las trayectorias en "
              "su entorno."
          )),

        b("definicion",
          titulo="Estabilidad (Lyapunov)",
          body_md=(
              "Sea $\\mathbf{x}^*$ un punto de equilibrio.\n\n"
              "**Estable:** para todo $\\varepsilon > 0$ existe $\\delta > 0$ tal que si "
              "$\\|\\mathbf{x}(0) - \\mathbf{x}^*\\| < \\delta$ entonces $\\|\\mathbf{x}(t) - \\mathbf{x}^*\\| < \\varepsilon$ "
              "para todo $t \\geq 0$.\n\n"
              "Es decir: pequeñas perturbaciones permanecen pequeñas.\n\n"
              "**Asintóticamente estable:** estable y además $\\mathbf{x}(t) \\to \\mathbf{x}^*$ cuando $t \\to \\infty$.\n\n"
              "Es decir: pequeñas perturbaciones decaen al equilibrio.\n\n"
              "**Inestable:** no estable. Hay perturbaciones arbitrariamente pequeñas cuyas trayectorias se "
              "alejan.\n\n"
              "**Criterio para sistemas lineales** $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$:\n\n"
              "- **Asintóticamente estable** sii **todos** los autovalores de $\\mathbf{A}$ tienen $\\operatorname{Re}(\\lambda) < 0$.\n"
              "- **Estable (no asintóticamente):** todos $\\operatorname{Re}(\\lambda) \\leq 0$, los con $\\operatorname{Re} = 0$ son simples (no defectivos).\n"
              "- **Inestable:** algún $\\lambda$ con $\\operatorname{Re}(\\lambda) > 0$, **o** algún $\\lambda$ con $\\operatorname{Re} = 0$ y defectivo."
          )),

        formulas(
            titulo="Clasificación en el plano (n = 2)",
            body=(
                "Para un sistema $2 \\times 2$ con $\\det \\mathbf{A} \\neq 0$, los autovalores $\\lambda_1, \\lambda_2$ determinan el tipo de origen:\n\n"
                "**Reales del mismo signo (no nulos):**\n\n"
                "- Ambos negativos → **nodo estable** (trayectorias entran al origen).\n"
                "- Ambos positivos → **nodo inestable** (trayectorias salen del origen).\n\n"
                "**Reales de signos opuestos** ($\\lambda_1 > 0 > \\lambda_2$): **silla** (inestable). Las trayectorias se acercan a lo largo del eje propio de $\\lambda_2$ y se alejan a lo largo del de $\\lambda_1$.\n\n"
                "**Reales repetidos** ($\\lambda_1 = \\lambda_2 = \\lambda$):\n\n"
                "- No defectivo (dos vectores propios LI) → **nodo propio** (estrella). Trayectorias rectas radiales.\n"
                "- Defectivo (un solo vector propio) → **nodo impropio**. Trayectorias se curvan.\n\n"
                "**Complejos conjugados $\\alpha \\pm i \\beta$, $\\beta \\neq 0$:**\n\n"
                "- $\\alpha < 0$ → **espiral estable** (atrae al origen oscilando).\n"
                "- $\\alpha > 0$ → **espiral inestable** (se aleja del origen oscilando).\n"
                "- $\\alpha = 0$ → **centro**: órbitas cerradas (elipses) alrededor del origen. **Estable pero no asintóticamente.**"
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Clasificar y dibujar — silla",
          problema_md="Clasifica el equilibrio en el origen de $\\mathbf{x}' = \\begin{pmatrix} 1 & 2 \\\\ 2 & 1 \\end{pmatrix} \\mathbf{x}$.",
          pasos=[
              {"accion_md": (
                  "**Autovalores:** $\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = (1 - \\lambda)^2 - 4 = \\lambda^2 - 2\\lambda - 3 = (\\lambda - 3)(\\lambda + 1)$.\n\n"
                  "$\\lambda_1 = 3, \\lambda_2 = -1$ — **reales de signos opuestos** → **silla**."
              ),
               "justificacion_md": "Signos opuestos siempre dan silla.",
               "es_resultado": False},
              {"accion_md": (
                  "**Vectores propios.** Para $\\lambda = 3$: $(1, 1)^T$. Para $\\lambda = -1$: $(1, -1)^T$.\n\n"
                  "**Retrato de fase:**\n\n"
                  "- A lo largo de la dirección $(1, 1)$: las trayectorias **se alejan** del origen (porque $\\lambda = 3 > 0$).\n"
                  "- A lo largo de la dirección $(1, -1)$: las trayectorias **se acercan** al origen (porque $\\lambda = -1 < 0$).\n"
                  "- Trayectorias generales son hipérbolas asintotando a las direcciones propias."
              ),
               "justificacion_md": "Receta universal para sillas.",
               "es_resultado": False},
              {"accion_md": "**Conclusión:** origen **inestable** (silla). Toda perturbación con componente no nula en la dirección $(1, 1)$ se aleja exponencialmente.",
               "justificacion_md": "Aún si la perturbación está casi exacta sobre la variedad estable, el más mínimo error la aleja.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Espiral estable",
          problema_md="Clasifica el origen de $\\mathbf{x}' = \\begin{pmatrix} -1 & -2 \\\\ 2 & -1 \\end{pmatrix} \\mathbf{x}$.",
          pasos=[
              {"accion_md": (
                  "**Autovalores:** $\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = (-1 - \\lambda)^2 + 4 = \\lambda^2 + 2\\lambda + 5 = 0$. \n\n"
                  "$\\lambda = -1 \\pm 2 i$. **Complejos conjugados con $\\alpha = -1 < 0$** → **espiral estable**."
              ),
               "justificacion_md": "Parte real negativa garantiza atracción al origen.",
               "es_resultado": False},
              {"accion_md": (
                  "**Comportamiento:** trayectorias espiralan hacia el origen. La frecuencia de giro es $\\beta = 2$ (período $\\pi$). El factor exponencial $e^{-t}$ atenúa el radio.\n\n"
                  "**Sentido del giro:** se determina mirando el flujo en un punto cualquiera, p. ej. $(1, 0)$: $\\mathbf{x}'|_{(1, 0)} = (-1, 2)$ — apunta arriba a la izquierda → **giro antihorario**."
              ),
               "justificacion_md": "Para distinguir antihorario/horario hay que evaluar el campo en algún punto.",
               "es_resultado": False},
              {"accion_md": "**Conclusión:** origen **asintóticamente estable** — espiral antihoraria atractora.",
               "justificacion_md": "Toda perturbación decae oscilando.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Centro",
          problema_md="Clasifica el origen de $\\mathbf{x}' = \\begin{pmatrix} 0 & 1 \\\\ -4 & 0 \\end{pmatrix} \\mathbf{x}$.",
          pasos=[
              {"accion_md": (
                  "**Autovalores:** $-\\lambda^2 + 4 \\cdot (-1) = \\lambda^2 + 4 = 0 \\Rightarrow \\lambda = \\pm 2 i$.\n\n"
                  "**Imaginarios puros** → **centro**."
              ),
               "justificacion_md": "$\\alpha = 0$, $\\beta = 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Comportamiento:** órbitas cerradas (elipses) alrededor del origen, recorridas con período $\\pi$.\n\n"
                  "**Estabilidad:** el origen es **estable pero NO asintóticamente** — perturbaciones permanecen acotadas pero no decaen."
              ),
               "justificacion_md": "Este es el modelo del oscilador armónico.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué los autovalores controlan todo.** En la base de vectores propios, "
            "$\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$ se desacopla en $n$ ecuaciones escalares "
            "$y_i' = \\lambda_i y_i$ con soluciones $y_i = c_i e^{\\lambda_i t}$. El signo de "
            "$\\operatorname{Re}(\\lambda_i)$ decide si la componente $i$ crece o decae. La parte imaginaria "
            "$\\beta$ aporta la oscilación. Volviendo a la base canónica las componentes se mezclan, pero el "
            "comportamiento cualitativo se preserva.\n\n"
            "**Diagrama 'traza-determinante'.** Para sistemas $2 \\times 2$, todo el comportamiento se lee del "
            "**discriminante** $D = (\\operatorname{tr} \\mathbf{A})^2 - 4 \\det \\mathbf{A}$ y de los signos "
            "de $\\operatorname{tr}\\mathbf{A}$ y $\\det\\mathbf{A}$. Hay un diagrama clásico en el plano "
            "$(\\operatorname{tr}, \\det)$ con todas las regiones: silla ($\\det < 0$), nodo (1er cuadrante "
            "con $D > 0$), espiral ($D < 0$), centro (eje vertical positivo), etc."
        )),

        fig(
            "Diagrama traza-determinante para clasificar equilibrios de sistemas lineales 2x2. "
            "Plano cartesiano con eje horizontal 'traza A' y eje vertical 'det A'. "
            "Zona det < 0: 'silla' (inestable). "
            "Zona det > 0 con D = tr² - 4 det > 0: 'nodos' (estable si tr < 0, inestable si tr > 0). "
            "Zona det > 0 con D < 0: 'espirales' (estable si tr < 0, inestable si tr > 0). "
            "Eje vertical positivo (tr = 0, det > 0): 'centros'. "
            "Curva D = 0 (parábola tr² = 4 det): nodos degenerados. "
            "Acentos teal #06b6d4 para regiones estables, ámbar #f59e0b para inestables. " + STYLE
        ),

        fig(
            "Cuadro 2x3 con seis retratos de fase típicos. "
            "(1) Nodo estable: trayectorias entrando al origen tangentes a un eje, color teal #06b6d4. "
            "(2) Nodo inestable: trayectorias saliendo del origen, color ámbar #f59e0b. "
            "(3) Silla: dos ejes propios, dos trayectorias entrando y dos saliendo, hipérbolas alrededor, color púrpura. "
            "(4) Espiral estable: trayectorias espirales hacia el origen, teal. "
            "(5) Espiral inestable: espirales saliendo del origen, ámbar. "
            "(6) Centro: órbitas elípticas cerradas alrededor del origen, gris. "
            "Cada panel con etiquetas de los autovalores correspondientes. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El origen es asintóticamente estable sii:",
                  "opciones_md": [
                      "Todos los autovalores son negativos",
                      "Algún autovalor tiene $\\operatorname{Re} < 0$",
                      "**Todos los autovalores tienen $\\operatorname{Re} < 0$**",
                      "$\\det \\mathbf{A} > 0$",
                  ],
                  "correcta": "C",
                  "pista_md": "Hay que considerar autovalores complejos también.",
                  "explicacion_md": "Cualquier autovalor con $\\operatorname{Re} \\geq 0$ destruye la atracción.",
              },
              {
                  "enunciado_md": "Si $\\lambda_1 > 0 > \\lambda_2$, el origen es:",
                  "opciones_md": [
                      "Nodo estable",
                      "**Silla (inestable)**",
                      "Centro",
                      "Espiral estable",
                  ],
                  "correcta": "B",
                  "pista_md": "Signos opuestos.",
                  "explicacion_md": "Una dirección atrae, otra repele — silla.",
              },
              {
                  "enunciado_md": "Si los autovalores son $\\pm i \\beta$ con $\\beta \\neq 0$, el origen es:",
                  "opciones_md": [
                      "Espiral estable",
                      "Espiral inestable",
                      "**Centro (estable, no asintóticamente)**",
                      "Nodo",
                  ],
                  "correcta": "C",
                  "pista_md": "$\\alpha = 0$.",
                  "explicacion_md": "Órbitas cerradas. Las trayectorias permanecen acotadas pero no decaen.",
              },
          ]),

        ej(
            "Nodo estable",
            "Clasifica el origen de $\\mathbf{x}' = \\begin{pmatrix} -3 & 0 \\\\ 0 & -2 \\end{pmatrix} \\mathbf{x}$.",
            ["Diagonal: autovalores leídos directamente."],
            (
                "$\\lambda_1 = -3, \\lambda_2 = -2$, ambos negativos y distintos → **nodo estable**. "
                "Trayectorias entran al origen, tangentes (cerca del origen) al eje propio del autovalor de menor módulo (eje $x_2$, $\\lambda = -2$)."
            ),
        ),

        ej(
            "Nodo impropio",
            "Clasifica el origen de $\\mathbf{x}' = \\begin{pmatrix} -1 & 1 \\\\ 0 & -1 \\end{pmatrix} \\mathbf{x}$.",
            ["Raíz doble; comprobar si es defectivo."],
            (
                "$\\lambda = -1$ doble. $(\\mathbf{A} + \\mathbf{I}) = \\begin{pmatrix} 0 & 1 \\\\ 0 & 0 \\end{pmatrix}$ tiene rango 1 → un solo vector propio $(1, 0)^T$. **Defectivo.**\n\n"
                "**Nodo impropio estable** (asintóticamente estable). Las trayectorias entran al origen pero no son tangentes a la dirección $(1, 0)$ excepto en el límite."
            ),
        ),

        ej(
            "Análisis de estabilidad sin calcular $\\lambda$",
            "Para qué valores de $a$ el origen de $\\mathbf{x}' = \\begin{pmatrix} a & 1 \\\\ -1 & a \\end{pmatrix} \\mathbf{x}$ es asintóticamente estable?",
            ["Calcular tr y det, o autovalores directamente."],
            (
                "Característica: $(a - \\lambda)^2 + 1 = 0 \\Rightarrow \\lambda = a \\pm i$. Parte real $a$.\n\n"
                "**Asintóticamente estable** sii $a < 0$. **Estable (centro)** si $a = 0$. **Inestable** si $a > 0$ (espiral inestable)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar la parte real cuando los autovalores son complejos.** El signo de $\\alpha$ es el que decide.",
              "**Confundir 'estable' con 'asintóticamente estable'.** Un centro es estable pero no asintóticamente.",
              "**Aplicar el criterio de signos a sistemas no autónomos o no lineales sin justificación.** El criterio es exacto solo para sistemas lineales con coeficientes constantes.",
              "**Olvidar verificar defectividad cuando hay raíz repetida.** Decide entre nodo propio y nodo impropio.",
              "**Dibujar la dirección del flujo al revés.** Hay que evaluar el campo en un punto para fijar el sentido.",
          ]),

        b("resumen",
          puntos_md=[
              "**Equilibrio:** $\\mathbf{x}^*$ con $\\mathbf{F}(\\mathbf{x}^*) = 0$.",
              "**Estabilidad asintótica del origen** (para $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$): todos los autovalores con $\\operatorname{Re} < 0$.",
              "**Plano de fase ($n = 2$):** nodo (autovalores reales del mismo signo), silla (signos opuestos), espiral (complejos con $\\alpha \\neq 0$), centro (imaginarios puros).",
              "**Diagrama traza-determinante:** mapa visual de todos los casos en términos de tr y det.",
              "**Cierre del capítulo:** cubrimos la teoría completa de sistemas lineales — formulación matricial, soluciones, valores propios, matriz fundamental, no homogéneos y análisis cualitativo.",
              "**Próximo capítulo:** **Transformada de Laplace** — herramienta integral para resolver EDOs y sistemas (especialmente con forzantes discontinuos o impulsos).",
          ]),
    ]
    return {
        "id": "lec-ed-3-6-estabilidad",
        "title": "Estabilidad",
        "description": "Análisis cualitativo de sistemas lineales autónomos: puntos de equilibrio, estabilidad de Lyapunov, clasificación del origen según los autovalores (nodo, silla, espiral, centro) y retratos de fase.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
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

    chapter_id = "ch-ed-sistemas-edo"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Sistemas de Ecuaciones Diferenciales",
        "description": (
            "Sistemas lineales de primer orden en forma matricial: existencia y unicidad, principio de "
            "superposición, wronskiano, método de valores propios, matriz fundamental y exponencial, "
            "sistemas no homogéneos y análisis cualitativo de estabilidad."
        ),
        "order": 3,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_sistemas_lineales,
        lesson_soluciones_sl,
        lesson_valores_propios,
        lesson_matriz_fundamental,
        lesson_no_homogeneos,
        lesson_estabilidad,
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
        f"✅ Capítulo 'Sistemas de Ecuaciones Diferenciales' listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
