"""
Seed del curso Cálculo Multivariable — Capítulo 4: Derivadas Parciales.
4 lecciones:
  4.1 Derivadas parciales
  4.2 Derivadas de orden superior
  4.3 Diferenciabilidad
  4.4 Regla de la cadena

Capítulo principalmente algebraico. Pocas figuras (3 totales).
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
# 4.1 Derivadas parciales
# =====================================================================
def lesson_4_1():
    blocks = [
        b("texto", body_md=(
            "Una función $f(x, y)$ tiene **dos direcciones independientes** de variación. La **derivada "
            "parcial** $\\partial f/\\partial x$ mide cómo cambia $f$ respecto a $x$ **manteniendo $y$ fijo**. "
            "Es el primer paso natural del cálculo en varias variables — y la base de todo lo que viene.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular derivadas parciales con la regla \"trato la otra variable como constante\".\n"
            "- Manejar las distintas notaciones ($\\partial f/\\partial x$, $f_x$, $D_x f$).\n"
            "- Comprender la **interpretación geométrica** como pendiente de una traza.\n"
            "- Extender la idea a funciones de tres o más variables."
        )),

        b("intuicion",
          titulo="Una variable a la vez",
          body_md=(
              "Si fijamos $y = b$, la función $g(x) = f(x, b)$ es una función de **una sola variable**. "
              "Su derivada $g'(x)$ es justamente $\\partial f/\\partial x$ evaluada en $(x, b)$.\n\n"
              "**Geométricamente:** la curva $z = f(x, b)$ vive en el plano $y = b$ (un \"corte vertical\" "
              "de la superficie $z = f(x, y)$). $\\partial f/\\partial x$ en $(a, b)$ es la **pendiente** "
              "de la tangente a esa curva en el punto $(a, b, f(a, b))$.\n\n"
              "Análogamente $\\partial f/\\partial y$ es la pendiente del corte $x = a$."
          )),

        b("definicion",
          titulo="Derivadas parciales",
          body_md=(
              "Sea $f(x, y)$. Las **derivadas parciales** en $(a, b)$ son:\n\n"
              "$$\\dfrac{\\partial f}{\\partial x}(a, b) = \\lim_{h \\to 0} \\dfrac{f(a + h, b) - f(a, b)}{h}$$\n\n"
              "$$\\dfrac{\\partial f}{\\partial y}(a, b) = \\lim_{h \\to 0} \\dfrac{f(a, b + h) - f(a, b)}{h}$$\n\n"
              "**Notaciones equivalentes:**\n\n"
              "- $\\dfrac{\\partial f}{\\partial x} = f_x = D_x f = \\partial_x f$\n"
              "- En cálculos: $\\dfrac{\\partial f}{\\partial x}(a, b) = f_x(a, b)$\n\n"
              "**Regla práctica:** para calcular $f_x$, **deriva respecto a $x$ tratando $y$ como constante**. Análogo para $f_y$."
          )),

        fig(
            "Interpretación geométrica de la derivada parcial. Vista 3D isométrica de una superficie "
            "z = f(x, y) ondulada en color teal translúcido. Un punto P = (a, b, f(a,b)) marcado en "
            "la superficie. Un plano vertical y = b cortando la superficie, dibujado en color "
            "ámbar translúcido. La intersección del plano con la superficie es una curva (la "
            "traza). En el punto P, dibujar la recta tangente a esa curva, en color azul oscuro "
            "grueso, con etiqueta 'pendiente = f_x(a, b)'. Etiquetas claras: ejes x, y, z; punto "
            "P; plano y = b; traza; tangente. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Cálculo directo de parciales",
          problema_md="Calcular $f_x$ y $f_y$ para $f(x, y) = x^2 y + 3xy^3 - 2y$.",
          pasos=[
              {"accion_md": "**$f_x$:** trato $y$ como constante.\n\n"
                            "$f_x = \\dfrac{\\partial}{\\partial x}(x^2 y) + \\dfrac{\\partial}{\\partial x}(3xy^3) - \\dfrac{\\partial}{\\partial x}(2y)$\n\n"
                            "$= 2xy + 3y^3 - 0 = 2xy + 3y^3$.",
               "justificacion_md": "El primer término: $y$ es coeficiente de $x^2$, derivada $2xy$. El segundo: $3y^3$ es coeficiente de $x$, derivada $3y^3$. El tercero: $-2y$ no depende de $x$, derivada $0$.",
               "es_resultado": False},
              {"accion_md": "**$f_y$:** trato $x$ como constante.\n\n"
                            "$f_y = x^2 + 9xy^2 - 2$.",
               "justificacion_md": "$x^2 y \\to x^2$ (coef de $y$). $3xy^3 \\to 9xy^2$. $-2y \\to -2$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Parciales de funciones trigonométricas",
          problema_md="Calcular $f_x$ y $f_y$ para $f(x, y) = \\sin(x^2 + y) + e^{xy}$.",
          pasos=[
              {"accion_md": "**$f_x$** (con regla de la cadena):\n\n"
                            "$\\partial_x \\sin(x^2 + y) = \\cos(x^2 + y) \\cdot 2x$.\n\n"
                            "$\\partial_x e^{xy} = e^{xy} \\cdot y$.\n\n"
                            "$f_x = 2x \\cos(x^2 + y) + y e^{xy}$.",
               "justificacion_md": "Cadena dentro de $\\sin$ y dentro de $\\exp$. Las constantes (respecto a $x$) son $y$ en ambos casos.",
               "es_resultado": False},
              {"accion_md": "**$f_y$:**\n\n"
                            "$\\partial_y \\sin(x^2 + y) = \\cos(x^2 + y) \\cdot 1$.\n\n"
                            "$\\partial_y e^{xy} = e^{xy} \\cdot x$.\n\n"
                            "$f_y = \\cos(x^2 + y) + x e^{xy}$.",
               "justificacion_md": "Lo mismo, ahora derivando respecto a $y$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Funciones de tres o más variables",
          body_md=(
              "Para $f(x, y, z)$:\n\n"
              "$$f_x = \\dfrac{\\partial f}{\\partial x}, \\quad f_y = \\dfrac{\\partial f}{\\partial y}, \\quad f_z = \\dfrac{\\partial f}{\\partial z}$$\n\n"
              "Cada una se calcula tratando **las otras dos** variables como constantes. La extensión a $n$ variables es análoga: $\\partial f / \\partial x_i$ trata todo $x_j$ con $j \\neq i$ como constante."
          )),

        b("ejemplo_resuelto",
          titulo="Tres variables",
          problema_md="Sea $f(x, y, z) = x y^2 z^3 + e^{x + y - z}$. Calcular las tres parciales.",
          pasos=[
              {"accion_md": "**$f_x$:** $y^2 z^3 + e^{x+y-z}$.",
               "justificacion_md": "Trato $y, z$ como constantes en cada término.",
               "es_resultado": False},
              {"accion_md": "**$f_y$:** $2xy z^3 + e^{x+y-z}$.",
               "justificacion_md": "$xy^2 z^3 \\to 2xy z^3$.",
               "es_resultado": False},
              {"accion_md": "**$f_z$:** $3xy^2 z^2 - e^{x+y-z}$.",
               "justificacion_md": "Atención al signo: $\\partial_z (x + y - z) = -1$, así $\\partial_z e^{x+y-z} = -e^{x+y-z}$.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Existencia y continuidad?",
          body_md=(
              "**Sorpresa importante:** que $f_x$ y $f_y$ existan en un punto **NO implica** que $f$ sea continua allí. "
              "Eso parece contradecir el caso 1D, donde derivable ⇒ continua.\n\n"
              "**Ejemplo:** $f(x, y) = \\dfrac{xy}{x^2 + y^2}$ extendida con $f(0, 0) = 0$:\n\n"
              "- $f_x(0, 0) = 0$ y $f_y(0, 0) = 0$ (los ejes dan $0$).\n"
              "- Pero $f$ no es continua en $(0, 0)$: por el camino $y = x$, el límite es $1/2 \\neq 0$.\n\n"
              "**Conclusión:** las parciales solo \"miran\" en direcciones de los ejes. Para tener un análogo robusto de \"derivable\", hay que pedir más — ese es el tema de la lección 4.3 (diferenciabilidad)."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $f(x, y) = x^3 y^2$, entonces $f_x(2, 3) = ?$",
                  "opciones_md": ["$36$", "$108$", "$54$", "$72$"],
                  "correcta": "B",
                  "pista_md": "$f_x = 3x^2 y^2$. Sustituye.",
                  "explicacion_md": (
                      "$f_x = 3x^2 y^2$. En $(2, 3)$: $3 \\cdot 4 \\cdot 9 = 108$."
                  ),
              },
              {
                  "enunciado_md": "Para calcular $f_y$, ¿qué se trata como constante?",
                  "opciones_md": [
                      "$y$",
                      "$x$",
                      "Tanto $x$ como $y$",
                      "Ninguna",
                  ],
                  "correcta": "B",
                  "pista_md": "$f_y$ mide cambio respecto a $y$. ¿Qué se mantiene fijo?",
                  "explicacion_md": (
                      "$f_y$ deriva respecto a $y$, así $x$ se trata como **constante**. Es la misma idea que las derivadas ordinarias, pero con una variable 'congelada'."
                  ),
              },
          ]),

        ej(
            titulo="Parciales con cociente",
            enunciado="Halla $f_x$ y $f_y$ para $f(x, y) = \\dfrac{x + y}{x - y}$.",
            pistas=[
                "Aplica regla del cociente para cada parcial.",
                "Para $f_x$: $u = x + y$ (con $u_x = 1$), $v = x - y$ (con $v_x = 1$).",
            ],
            solucion=(
                "$f_x = \\dfrac{(1)(x-y) - (x+y)(1)}{(x-y)^2} = \\dfrac{-2y}{(x-y)^2}$.\n\n"
                "$f_y = \\dfrac{(1)(x-y) - (x+y)(-1)}{(x-y)^2} = \\dfrac{2x}{(x-y)^2}$.\n\n"
                "**Verificación:** $f_x \\cdot x + f_y \\cdot y = \\dfrac{-2xy + 2xy}{(x-y)^2} = 0$. (Es una identidad de Euler para funciones homogéneas de grado 0 — bonus.)"
            ),
        ),

        ej(
            titulo="Parciales en un punto específico",
            enunciado=(
                "Calcula $f_x(1, -1)$ y $f_y(1, -1)$ para $f(x, y) = e^{xy} \\ln(x^2 + y^2)$."
            ),
            pistas=[
                "Es producto de dos factores. Aplica regla del producto al derivar.",
                "$\\partial_x e^{xy} = y e^{xy}$. $\\partial_x \\ln(x^2+y^2) = 2x/(x^2+y^2)$.",
                "Sustituye al final.",
            ],
            solucion=(
                "**$f_x$:** producto $u = e^{xy}$, $v = \\ln(x^2+y^2)$. $u_x = y e^{xy}$, $v_x = 2x/(x^2+y^2)$.\n\n"
                "$f_x = y e^{xy} \\ln(x^2+y^2) + e^{xy} \\cdot \\dfrac{2x}{x^2+y^2}$.\n\n"
                "**En $(1, -1)$:** $e^{xy} = e^{-1} = 1/e$. $\\ln(1 + 1) = \\ln 2$. $x^2+y^2 = 2$.\n\n"
                "$f_x(1, -1) = (-1)\\dfrac{1}{e}\\ln 2 + \\dfrac{1}{e} \\cdot \\dfrac{2}{2} = \\dfrac{1 - \\ln 2}{e}$.\n\n"
                "**Análogo $f_y$** (intercambiando roles de $x$ y $y$): $f_y(1, -1) = (1)\\dfrac{1}{e}\\ln 2 + \\dfrac{1}{e} \\cdot \\dfrac{-2}{2} = \\dfrac{\\ln 2 - 1}{e}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar tratar la otra variable como constante.** Es el error más común al inicio.",
              "**Olvidar la regla de la cadena** dentro de las parciales: $\\partial_x \\sin(x^2 + y) = \\cos(x^2+y) \\cdot 2x$, no solo $\\cos(x^2+y)$.",
              "**Pensar que existencia de parciales implica diferenciabilidad o continuidad.** **No** — hay contraejemplos.",
              "**Confundir $\\partial f/\\partial x$ con $df/dx$**. El primero es parcial; el segundo solo tiene sentido cuando $f$ depende de una sola variable.",
              "**Aplicar la regla del cociente al revés** o con signo equivocado en parciales: igual que en 1D, el orden importa.",
          ]),

        b("resumen",
          puntos_md=[
              "**Derivada parcial:** $\\partial f/\\partial x$ deriva respecto a $x$ tratando otras variables como constantes.",
              "**Notaciones:** $\\partial f/\\partial x$, $f_x$, $D_x f$.",
              "**Geometría:** pendiente de la traza en el plano vertical $y = b$ (o $x = a$).",
              "**Reglas habituales** (cadena, producto, cociente) **siguen valiendo** dentro de cada parcial.",
              "**$n$ variables:** análogo, congelar todas las demás.",
              "**Atención:** existencia de parciales **NO implica** continuidad ni diferenciabilidad.",
              "**Próxima lección:** derivadas de orden superior y el teorema de Clairaut.",
          ]),
    ]
    return {
        "id": "lec-mvar-4-1-parciales",
        "title": "Derivadas parciales",
        "description": "Definición, cálculo, notaciones y interpretación geométrica de derivadas parciales.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 4.2 Derivadas de orden superior
# =====================================================================
def lesson_4_2():
    blocks = [
        b("texto", body_md=(
            "Igual que en 1D, las derivadas parciales se pueden derivar nuevamente. Aparecen las **derivadas "
            "parciales de segundo orden**: $f_{xx}, f_{yy}, f_{xy}, f_{yx}$. Una sorpresa elegante — el "
            "**teorema de Clairaut** — dice que las dos mixtas $f_{xy}$ y $f_{yx}$ **coinciden** bajo "
            "hipótesis razonables. Eso significa que el orden de derivación no importa.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular las cuatro derivadas parciales de segundo orden.\n"
            "- Aplicar el **teorema de Clairaut** para verificar cálculos.\n"
            "- Manejar derivadas de orden $\\geq 3$.\n"
            "- Reconocer el **operador laplaciano** $\\nabla^2 f = f_{xx} + f_{yy}$."
        )),

        b("definicion",
          titulo="Derivadas parciales de segundo orden",
          body_md=(
              "Para $f(x, y)$ existen **cuatro** parciales de segundo orden:\n\n"
              "$$f_{xx} = \\dfrac{\\partial}{\\partial x}\\left(\\dfrac{\\partial f}{\\partial x}\\right) = \\dfrac{\\partial^2 f}{\\partial x^2}$$\n\n"
              "$$f_{yy} = \\dfrac{\\partial^2 f}{\\partial y^2}$$\n\n"
              "$$f_{xy} = \\dfrac{\\partial}{\\partial y}\\left(\\dfrac{\\partial f}{\\partial x}\\right) = \\dfrac{\\partial^2 f}{\\partial y \\partial x}$$\n\n"
              "$$f_{yx} = \\dfrac{\\partial}{\\partial x}\\left(\\dfrac{\\partial f}{\\partial y}\\right) = \\dfrac{\\partial^2 f}{\\partial x \\partial y}$$\n\n"
              "**Convención de notación:** $f_{xy}$ significa **primero $x$, luego $y$**. En la notación $\\partial$, el orden es **al revés** ($\\partial^2 f / \\partial y \\partial x$ = primero $x$, luego $y$). Confunde, pero es estándar."
          )),

        b("ejemplo_resuelto",
          titulo="Las cuatro segundas parciales",
          problema_md="Calcular las cuatro segundas parciales de $f(x, y) = x^3 y - x y^2$.",
          pasos=[
              {"accion_md": "**Primero las primeras:**\n\n"
                            "$f_x = 3x^2 y - y^2$.\n\n"
                            "$f_y = x^3 - 2xy$.",
               "justificacion_md": "Aplicación rutinaria.",
               "es_resultado": False},
              {"accion_md": "**Segundas:**\n\n"
                            "$f_{xx} = \\partial_x(3x^2 y - y^2) = 6xy$.\n\n"
                            "$f_{yy} = \\partial_y(x^3 - 2xy) = -2x$.\n\n"
                            "$f_{xy} = \\partial_y(3x^2 y - y^2) = 3x^2 - 2y$.\n\n"
                            "$f_{yx} = \\partial_x(x^3 - 2xy) = 3x^2 - 2y$.",
               "justificacion_md": "**Verifica que $f_{xy} = f_{yx}$.** Es Clairaut en acción.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Teorema de Clairaut (igualdad de mixtas)",
          enunciado_md=(
              "Si $f$, $f_x$, $f_y$, $f_{xy}$ y $f_{yx}$ son **todas continuas** en un entorno del punto $(a, b)$, entonces:\n\n"
              "$$f_{xy}(a, b) = f_{yx}(a, b)$$\n\n"
              "**Es decir, el orden de las derivadas parciales no importa** (con la condición técnica de continuidad).\n\n"
              "**Lectura práctica:** para casi todas las funciones que aparecen en la práctica (polinomios, racionales, exp, log, trig — todas con sus mixtas continuas), $f_{xy} = f_{yx}$ siempre."
          ),
          demostracion_md=(
              "La demostración formal usa el teorema del valor medio aplicado a la función auxiliar "
              "$\\Delta(h, k) = f(a+h, b+k) - f(a+h, b) - f(a, b+k) + f(a, b)$. "
              "Aplicando TVM dos veces se muestra que $\\Delta = h k \\, f_{xy}(c_1, c_2) = h k \\, f_{yx}(c_3, c_4)$. "
              "Por continuidad de las mixtas, al hacer $(h, k) \\to 0$ ambos coinciden."
          )),

        b("intuicion",
          titulo="Cuándo Clairaut puede fallar",
          body_md=(
              "Hay funciones \"patológicas\" donde $f_{xy}(0, 0) \\neq f_{yx}(0, 0)$. El ejemplo clásico es:\n\n"
              "$$f(x, y) = \\begin{cases} \\dfrac{xy(x^2 - y^2)}{x^2 + y^2} & (x, y) \\neq (0, 0) \\\\ 0 & (x, y) = (0, 0) \\end{cases}$$\n\n"
              "Para esta función, $f_{xy}(0, 0) = -1$ pero $f_{yx}(0, 0) = 1$. Clairaut falla porque las mixtas existen pero **no son continuas** en $(0, 0)$.\n\n"
              "**No vale la pena memorizar el contraejemplo** — solo recordar que la hipótesis de continuidad es esencial. En problemas estándar, Clairaut siempre aplica."
          )),

        b("definicion",
          titulo="Derivadas de orden superior",
          body_md=(
              "Las derivadas de tercer orden tienen **ocho** combinaciones (en principio): $f_{xxx}, f_{xxy}, f_{xyx}, f_{xyy}, f_{yxx}, f_{yxy}, f_{yyx}, f_{yyy}$.\n\n"
              "**Por Clairaut iterado:** todas las que tengan el **mismo número** de derivaciones respecto a $x$ y respecto a $y$ son iguales. Así, en realidad solo hay **cuatro** distintas:\n\n"
              "$$f_{xxx}, f_{xxy}, f_{xyy}, f_{yyy}$$\n\n"
              "**Generalización:** para orden $n$, hay $n+1$ derivadas distintas, clasificadas por cuántas veces se deriva respecto a cada variable.\n\n"
              "**Para $f(x, y, z)$:** análogo, pero con muchas más combinaciones."
          )),

        b("definicion",
          titulo="Operador laplaciano",
          body_md=(
              "El **laplaciano** de $f(x, y)$ es:\n\n"
              "$$\\nabla^2 f = \\Delta f = f_{xx} + f_{yy}$$\n\n"
              "**Para $f(x, y, z)$:** $\\nabla^2 f = f_{xx} + f_{yy} + f_{zz}$.\n\n"
              "**Funciones armónicas:** $f$ es **armónica** si $\\nabla^2 f = 0$. Son fundamentales en física (electricidad, conductividad de calor en estado estacionario, mecánica de fluidos incompresibles).\n\n"
              "**Ejemplos clásicos** de armónicas: $f(x, y) = x^2 - y^2$, $f(x, y) = e^x \\cos y$, $f(x, y) = \\ln(x^2 + y^2)$ (en su dominio)."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar que una función es armónica",
          problema_md="Mostrar que $f(x, y) = x^3 - 3xy^2$ es armónica.",
          pasos=[
              {"accion_md": "**Primeras parciales:** $f_x = 3x^2 - 3y^2$, $f_y = -6xy$.",
               "justificacion_md": "Estándar.",
               "es_resultado": False},
              {"accion_md": "**Segundas:** $f_{xx} = 6x$, $f_{yy} = -6x$.",
               "justificacion_md": "Derivar las primeras una vez más en cada variable.",
               "es_resultado": False},
              {"accion_md": "$\\nabla^2 f = f_{xx} + f_{yy} = 6x + (-6x) = 0$. **Es armónica.** ✓",
               "justificacion_md": "**Bonus:** $x^3 - 3xy^2 = \\Re(z^3)$ donde $z = x + iy$ — la parte real de toda función analítica compleja es armónica (no es coincidencia).",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $f(x, y) = x^4 + y^4$, $f_{xy} = ?$",
                  "opciones_md": ["$0$", "$4x^3$", "$12x^2 y^2$", "$4y^3$"],
                  "correcta": "A",
                  "pista_md": "$f_x = 4x^3$. Derivar respecto a $y$.",
                  "explicacion_md": (
                      "$f_x = 4x^3$ (no contiene $y$). $f_{xy} = \\partial_y(4x^3) = 0$. **Las mixtas se anulan** cuando las primeras dependen solo de una variable."
                  ),
              },
              {
                  "enunciado_md": "Por Clairaut, ¿cuántas derivadas terceras distintas tiene $f(x,y)$ típica?",
                  "opciones_md": ["$2$", "$3$", "$4$", "$8$"],
                  "correcta": "C",
                  "pista_md": "Cuántas formas hay de elegir cuántas $x$ vs $y$ con un total de $3$.",
                  "explicacion_md": (
                      "Las distintas son $f_{xxx}, f_{xxy}, f_{xyy}, f_{yyy}$ — **cuatro**. Clairaut hace iguales todas las que tengan el mismo número de derivadas respecto a $x$."
                  ),
              },
          ]),

        ej(
            titulo="Verificar Clairaut",
            enunciado=(
                "Para $f(x, y) = e^{x} \\sin y + xy^2$, calcula $f_{xy}$ y $f_{yx}$ y verifica que son iguales."
            ),
            pistas=[
                "$f_x = e^x \\sin y + y^2$, $f_y = e^x \\cos y + 2xy$.",
                "Deriva una vez más cada una en la otra variable.",
            ],
            solucion=(
                "$f_x = e^x \\sin y + y^2$. $f_{xy} = e^x \\cos y + 2y$.\n\n"
                "$f_y = e^x \\cos y + 2xy$. $f_{yx} = e^x \\cos y + 2y$.\n\n"
                "**Coinciden.** ✓ (Como manda Clairaut, porque $f$ es analítica con todas sus derivadas continuas.)"
            ),
        ),

        ej(
            titulo="Función armónica con logaritmo",
            enunciado=(
                "Verifica que $f(x, y) = \\ln(x^2 + y^2)$ es armónica para $(x, y) \\neq (0, 0)$."
            ),
            pistas=[
                "$f_x = 2x/(x^2+y^2)$, $f_y = 2y/(x^2+y^2)$.",
                "Calcula $f_{xx}$ con regla del cociente — atención al signo.",
            ],
            solucion=(
                "$f_x = \\dfrac{2x}{x^2+y^2}$. Por cociente:\n\n"
                "$f_{xx} = \\dfrac{2(x^2+y^2) - 2x \\cdot 2x}{(x^2+y^2)^2} = \\dfrac{2y^2 - 2x^2}{(x^2+y^2)^2}$.\n\n"
                "Análogo: $f_{yy} = \\dfrac{2x^2 - 2y^2}{(x^2+y^2)^2}$.\n\n"
                "$\\nabla^2 f = f_{xx} + f_{yy} = 0$. ✓ **$\\ln(x^2+y^2)$ es armónica** en su dominio."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir el orden en $\\partial^2 f / \\partial y \\partial x$**: significa primero $x$, luego $y$ (al revés del orden de lectura). Más fácil usar $f_{xy}$.",
              "**Olvidar Clairaut** y duplicar trabajo: si calculas $f_{xy}$, ya tienes $f_{yx}$ en problemas estándar.",
              "**Aplicar Clairaut sin verificar continuidad**. En contextos exóticos puede fallar.",
              "**Confundir el laplaciano con el gradiente.** Gradiente $\\nabla f = (f_x, f_y)$ es vectorial; laplaciano $\\nabla^2 f$ es escalar.",
              "**Pensar que toda función es armónica.** La mayoría no lo es — ser armónica es una restricción fuerte.",
          ]),

        b("resumen",
          puntos_md=[
              "**Cuatro segundas parciales:** $f_{xx}, f_{yy}, f_{xy}, f_{yx}$.",
              "**Clairaut:** $f_{xy} = f_{yx}$ con continuidad de las mixtas (caso típico).",
              "**Orden $n$:** $n+1$ derivadas distintas tras Clairaut iterado.",
              "**Laplaciano:** $\\nabla^2 f = f_{xx} + f_{yy}$ (sumar segundas puras).",
              "**Funciones armónicas:** $\\nabla^2 f = 0$. Aparecen en electrostática, calor estacionario, fluidos.",
              "**Próxima lección:** diferenciabilidad — qué se necesita además de existencia de parciales.",
          ]),
    ]
    return {
        "id": "lec-mvar-4-2-orden-superior",
        "title": "Derivadas de orden superior",
        "description": "Segundas parciales, teorema de Clairaut, laplaciano y funciones armónicas.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# 4.3 Diferenciabilidad
# =====================================================================
def lesson_4_3():
    blocks = [
        b("texto", body_md=(
            "En 1D, la existencia de la derivada es la única condición que importa: derivable ⇒ continua, "
            "y la derivada da la mejor aproximación lineal. **En varias variables eso falla.** "
            "Hace falta una condición más fuerte: **diferenciabilidad**, que garantiza una verdadera "
            "aproximación lineal por el plano tangente.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir **diferenciabilidad** rigurosamente con aproximación lineal.\n"
            "- Reconocer el **plano tangente** como la aproximación lineal en un punto.\n"
            "- Aplicar el **criterio de Clairaut\\* (parciales continuas):** si $f_x, f_y$ son continuas, $f$ es diferenciable.\n"
            "- Calcular el **diferencial total** $df = f_x dx + f_y dy$ y usarlo para estimación de errores.\n\n"
            "_\\*Aclaración: el teorema 'parciales continuas → diferenciable' no es el de Clairaut, pero es del mismo grupo de resultados clásicos sobre suficiencia._"
        )),

        b("intuicion",
          titulo="Por qué no basta con que existan las parciales",
          body_md=(
              "Las parciales solo \"miran\" en las direcciones de los ejes coordenados. Una función puede:\n\n"
              "- Tener $f_x$ y $f_y$ existentes en $(0, 0)$.\n"
              "- Pero comportarse muy mal en otras direcciones.\n\n"
              "**Ejemplo dramático:** $f(x, y) = \\dfrac{xy}{x^2+y^2}$ con $f(0,0) = 0$. Las parciales en $(0,0)$ existen y valen $0$ (los ejes son donde $f \\equiv 0$), pero $f$ no es siquiera **continua** allí.\n\n"
              "**Diferenciabilidad** pide que $f$ sea localmente \"plana\" — bien aproximada por su plano tangente — en **todas** las direcciones."
          )),

        b("definicion",
          titulo="Diferenciabilidad",
          body_md=(
              "$f$ es **diferenciable en $(a, b)$** si existen $f_x(a, b)$ y $f_y(a, b)$, y se cumple:\n\n"
              "$$\\lim_{(h, k) \\to (0, 0)} \\dfrac{f(a + h, b + k) - f(a, b) - f_x(a, b) \\cdot h - f_y(a, b) \\cdot k}{\\sqrt{h^2 + k^2}} = 0$$\n\n"
              "**En palabras:** el error de aproximar $f(a+h, b+k)$ por la fórmula lineal $f(a,b) + h f_x + k f_y$ "
              "tiende a $0$ **más rápido** que la distancia $\\sqrt{h^2+k^2}$.\n\n"
              "**Es decir:** $f$ se ve localmente como un plano. Ese plano es el **plano tangente** en $(a, b)$."
          )),

        b("definicion",
          titulo="Plano tangente",
          body_md=(
              "Si $f$ es diferenciable en $(a, b)$, el **plano tangente** a la superficie $z = f(x, y)$ en el punto $(a, b, f(a,b))$ es:\n\n"
              "$$z = f(a, b) + f_x(a, b)(x - a) + f_y(a, b)(y - b)$$\n\n"
              "Es el análogo bidimensional de la recta tangente $y = f(a) + f'(a)(x - a)$ en 1D.\n\n"
              "**Vector normal al plano tangente:** $\\vec{n} = \\langle f_x(a,b), f_y(a,b), -1 \\rangle$ (de la ecuación $-z + f(a,b) + f_x(x-a) + f_y(y-b) = 0$)."
          )),

        fig(
            "Plano tangente a una superficie 3D. Vista isométrica de una superficie z = f(x, y) "
            "ondulada, en color teal translúcido. Un punto P = (a, b, f(a,b)) destacado en la "
            "superficie. Un plano tangente en P, en color ámbar translúcido, que toca a la "
            "superficie suavemente en P. Una pequeña flecha perpendicular al plano tangente en P "
            "etiquetada 'normal'. Etiquetas: 'z = f(x, y)' (sobre la superficie), 'plano tangente' "
            "(sobre el plano), 'P = (a, b, f(a,b))'. " + STYLE
        ),

        b("teorema",
          nombre="Criterio suficiente de diferenciabilidad",
          enunciado_md=(
              "Si las derivadas parciales $f_x$ y $f_y$ **existen y son continuas** en un entorno de $(a, b)$, entonces $f$ es **diferenciable en $(a, b)$**.\n\n"
              "**En la práctica:** este es el test que se aplica casi siempre. Si las parciales son funciones \"comunes\" (polinomios, racionales sin denominador 0, exp, log, trig en sus dominios), $f$ es diferenciable."
          ),
          demostracion_md=(
              "Por el teorema del valor medio aplicado dos veces:\n\n"
              "$f(a+h, b+k) - f(a, b) = [f(a+h, b+k) - f(a, b+k)] + [f(a, b+k) - f(a, b)]$\n\n"
              "$= h f_x(c_1, b+k) + k f_y(a, c_2)$ por TVM.\n\n"
              "Por continuidad de las parciales, $f_x(c_1, b+k) \\to f_x(a, b)$ y análogo. La diferencia entre el incremento real y la aproximación lineal va a $0$ más rápido que $\\sqrt{h^2+k^2}$."
          )),

        b("teorema",
          nombre="Diferenciabilidad implica continuidad",
          enunciado_md=(
              "Si $f$ es diferenciable en $(a, b)$, entonces $f$ es **continua en $(a, b)$**.\n\n"
              "**Es el análogo correcto** de \"derivable ⇒ continua\" en 1D. La existencia de parciales no es suficiente para esto; **diferenciabilidad sí**."
          ),
          demostracion_md=(
              "De la definición, $f(a+h, b+k) - f(a, b) = h f_x + k f_y + \\epsilon \\sqrt{h^2+k^2}$ con $\\epsilon \\to 0$. "
              "Cuando $(h, k) \\to (0, 0)$, los tres términos del lado derecho van a $0$, así $f(a+h, b+k) \\to f(a, b)$."
          )),

        b("definicion",
          titulo="Diferencial total",
          body_md=(
              "El **diferencial** de $z = f(x, y)$ es:\n\n"
              "$$dz = df = f_x \\, dx + f_y \\, dy$$\n\n"
              "Para incrementos pequeños $\\Delta x, \\Delta y$:\n\n"
              "$$\\Delta z \\approx f_x \\, \\Delta x + f_y \\, \\Delta y$$\n\n"
              "Es la **aproximación lineal** del cambio en $f$. Útil para:\n\n"
              "- **Estimación de errores** propagados (medición de varias variables).\n"
              "- Aproximaciones rápidas de $f$ cerca de un punto.\n"
              "- **Linealización** $L(x, y) = f(a, b) + f_x(a-x) + f_y(b-y)$ que aproxima $f(x, y)$ cerca de $(a, b)$."
          )),

        b("ejemplo_resuelto",
          titulo="Plano tangente a un paraboloide",
          problema_md=(
              "Encontrar el plano tangente a $z = x^2 + y^2$ en el punto $(1, 2, 5)$."
          ),
          pasos=[
              {"accion_md": "**Parciales:** $f_x = 2x$, $f_y = 2y$. **En $(1, 2)$:** $f_x = 2$, $f_y = 4$.",
               "justificacion_md": "Continuas en todo $\\mathbb{R}^2$, así $f$ es diferenciable. Plano tangente bien definido.",
               "es_resultado": False},
              {"accion_md": "**Plano tangente:**\n\n"
                            "$z = 5 + 2(x - 1) + 4(y - 2) = 2x + 4y - 5$.",
               "justificacion_md": "Aplicación de la fórmula con $f(1, 2) = 5$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Estimación de error con diferencial",
          problema_md=(
              "El radio $r$ de un cilindro se mide en $5$ cm con error $\\pm 0.01$ cm; la altura $h$ en $10$ cm con error $\\pm 0.02$ cm. Estimar el error en el volumen $V = \\pi r^2 h$."
          ),
          pasos=[
              {"accion_md": "**Diferencial:**\n\n"
                            "$dV = V_r \\, dr + V_h \\, dh = 2\\pi r h \\, dr + \\pi r^2 \\, dh$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "**Sustituyendo** valores nominales y errores máximos:\n\n"
                            "$|dV| \\leq 2\\pi(5)(10)(0.01) + \\pi(25)(0.02) = \\pi + 0.5\\pi = 1.5\\pi \\approx 4.71$ cm³.",
               "justificacion_md": "**Error relativo:** $dV/V = 1.5\\pi / (250\\pi) = 0.006 = 0.6\\%$. **Lección:** se obtiene cota sumando los errores parciales en valor absoluto.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "Si $f$ es diferenciable en $(a, b)$, entonces:",
                  "opciones_md": [
                      "Existen $f_x$ y $f_y$, pero $f$ puede no ser continua.",
                      "$f$ es continua pero no necesariamente las parciales son continuas.",
                      "$f$ es continua y existen $f_x$ y $f_y$.",
                      "Las parciales son siempre cero.",
                  ],
                  "correcta": "C",
                  "pista_md": "Diferenciable ⇒ continua, y existencia de parciales es parte de la definición.",
                  "explicacion_md": (
                      "Diferenciable implica: parciales existen + $f$ continua + plano tangente bien definido. "
                      "**No implica que las parciales sean continuas** (aunque la implicación inversa sí: continuidad de parciales → diferenciable)."
                  ),
              },
              {
                  "enunciado_md": "Para verificar diferenciabilidad rápidamente, basta:",
                  "opciones_md": [
                      "Verificar que existen $f_x, f_y$.",
                      "Verificar que $f_x$ y $f_y$ son continuas.",
                      "Calcular el plano tangente.",
                      "Verificar que $f$ es continua.",
                  ],
                  "correcta": "B",
                  "pista_md": "Hay un criterio suficiente con continuidad de parciales.",
                  "explicacion_md": (
                      "$f_x, f_y$ continuas en un entorno → $f$ diferenciable. **Es el test estándar** — funciona para todas las funciones de fórmula común."
                  ),
              },
          ]),

        ej(
            titulo="Plano tangente",
            enunciado=(
                "Encuentra el plano tangente a $z = \\sin(xy)$ en el punto $(1, \\pi/2, 1)$."
            ),
            pistas=[
                "$f_x = y \\cos(xy)$, $f_y = x \\cos(xy)$.",
                "En $(1, \\pi/2)$: $\\cos(\\pi/2) = 0$.",
            ],
            solucion=(
                "$f_x(1, \\pi/2) = (\\pi/2) \\cdot 0 = 0$. $f_y(1, \\pi/2) = 1 \\cdot 0 = 0$.\n\n"
                "**Plano tangente:** $z = 1 + 0(x-1) + 0(y - \\pi/2) = 1$. **Plano horizontal.**\n\n"
                "**Interpretación:** el punto $(1, \\pi/2, 1)$ es un máximo de $\\sin(xy)$ (porque $\\sin(\\pi/2) = 1$), y los máximos tienen plano tangente horizontal."
            ),
        ),

        ej(
            titulo="Aproximación lineal",
            enunciado=(
                "Usando linealización de $f(x, y) = \\sqrt{x^2 + y^2}$ en $(3, 4)$, estima $f(3.05, 3.97)$."
            ),
            pistas=[
                "$f(3, 4) = 5$. Calcula las parciales en $(3, 4)$.",
                "$f_x = x/\\sqrt{x^2+y^2}$, $f_y = y/\\sqrt{x^2+y^2}$.",
                "Linealización: $L(x, y) = f(3, 4) + f_x(x-3) + f_y(y-4)$.",
            ],
            solucion=(
                "$f(3, 4) = 5$. $f_x(3, 4) = 3/5$, $f_y(3, 4) = 4/5$.\n\n"
                "$L(x, y) = 5 + 0.6(x - 3) + 0.8(y - 4)$.\n\n"
                "**En $(3.05, 3.97)$:** $L = 5 + 0.6(0.05) + 0.8(-0.03) = 5 + 0.03 - 0.024 = 5.006$.\n\n"
                "**Valor real:** $\\sqrt{3.05^2 + 3.97^2} = \\sqrt{9.3025 + 15.7609} = \\sqrt{25.0634} \\approx 5.0063$. Error $\\approx 0.0003$. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que existencia de parciales implica diferenciabilidad.** No alcanza — hace falta también continuidad de $f$ o un criterio más fuerte.",
              "**Confundir 'diferenciable' con 'tiene parciales'.** Diferenciable es la condición correcta para el plano tangente.",
              "**Olvidar que la fórmula del plano tangente** asume $f$ diferenciable en el punto. Si no lo es, el 'plano tangente' calculado con esa fórmula no representa nada geométrico.",
              "**Usar incrementos grandes con la aproximación lineal.** El diferencial es bueno solo para $\\Delta x, \\Delta y$ pequeños.",
              "**Sumar errores con signo (no en valor absoluto)** al estimar incertidumbre — los errores pueden sumarse en el peor caso, así $|dV| \\leq |V_x dx| + |V_y dy|$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Diferenciable** = aproximable por un plano tangente con error mayor en orden que la distancia.",
              "**Plano tangente:** $z = f(a,b) + f_x(a-x) + f_y(b-y)$.",
              "**Criterio suficiente:** $f_x, f_y$ continuas en un entorno → $f$ diferenciable.",
              "**Diferenciable ⇒ continua** (análogo correcto del 1D).",
              "**Diferencial total:** $df = f_x dx + f_y dy$. Aplicaciones: estimación de error, aproximación.",
              "**Próxima lección:** regla de la cadena en varias variables — composición de funciones.",
          ]),
    ]
    return {
        "id": "lec-mvar-4-3-diferenciabilidad",
        "title": "Diferenciabilidad",
        "description": "Aproximación lineal, plano tangente, criterio de continuidad de parciales y diferencial total.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 4.4 Regla de la cadena
# =====================================================================
def lesson_4_4():
    blocks = [
        b("texto", body_md=(
            "La **regla de la cadena** se generaliza a varias variables, pero ahora con varios casos posibles "
            "según cómo se compongan las funciones. La idea central sigue siendo la misma: si una función "
            "depende de otra, y esa de otra, las derivadas se **multiplican**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar el **caso 1**: $z = f(x, y)$ con $x = x(t)$, $y = y(t)$ → $dz/dt$.\n"
            "- Aplicar el **caso 2**: $z = f(x, y)$ con $x = x(s, t)$, $y = y(s, t)$ → $\\partial z/\\partial s$, $\\partial z/\\partial t$.\n"
            "- Usar el **diagrama de árbol** como herramienta sistemática.\n"
            "- Aplicar la regla a la **derivación implícita** $F(x, y) = 0$."
        )),

        b("teorema",
          nombre="Regla de la cadena — Caso 1",
          enunciado_md=(
              "Si $z = f(x, y)$ es diferenciable y $x = x(t)$, $y = y(t)$ son derivables, entonces $z$ depende de $t$ vía la composición y:\n\n"
              "$$\\dfrac{dz}{dt} = \\dfrac{\\partial f}{\\partial x} \\cdot \\dfrac{dx}{dt} + \\dfrac{\\partial f}{\\partial y} \\cdot \\dfrac{dy}{dt}$$\n\n"
              "**Idea:** $z$ tiene una sola variable independiente ($t$), pero hay dos \"rutas\" para que un cambio en $t$ afecte a $z$ (una por $x$, otra por $y$). Se **suman** las contribuciones."
          ),
          demostracion_md=(
              "Por diferenciabilidad de $f$:\n\n"
              "$\\Delta z = f_x \\Delta x + f_y \\Delta y + \\epsilon \\sqrt{(\\Delta x)^2 + (\\Delta y)^2}$\n\n"
              "donde $\\epsilon \\to 0$. Dividiendo por $\\Delta t$ y haciendo $\\Delta t \\to 0$:\n\n"
              "$\\Delta x / \\Delta t \\to dx/dt$, $\\Delta y / \\Delta t \\to dy/dt$, y el término de error desaparece más rápido. Quedan los dos términos de la fórmula."
          )),

        fig(
            "Diagrama de árbol para la regla de la cadena. Tres niveles de cajas conectadas por "
            "líneas rectas. NIVEL SUPERIOR: una caja 'z'. NIVEL MEDIO: dos cajas 'x' e 'y' "
            "conectadas a 'z' arriba con líneas etiquetadas '∂f/∂x' y '∂f/∂y' respectivamente. "
            "NIVEL INFERIOR: una sola caja 't' conectada a 'x' e 'y' con líneas etiquetadas "
            "'dx/dt' y 'dy/dt' respectivamente. Mostrar como dos rutas distintas desde 't' hasta "
            "'z'. La fórmula 'dz/dt = (∂f/∂x)(dx/dt) + (∂f/∂y)(dy/dt)' al lado del diagrama. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Caso 1: $z$ función de $t$",
          problema_md=(
              "Sea $z = x^2 y + y^2$ con $x = \\sin t$ e $y = e^t$. Calcular $dz/dt$."
          ),
          pasos=[
              {"accion_md": "**Parciales de $f$:** $f_x = 2xy$, $f_y = x^2 + 2y$.",
               "justificacion_md": "Trato cada variable por separado.",
               "es_resultado": False},
              {"accion_md": "**Derivadas ordinarias:** $dx/dt = \\cos t$, $dy/dt = e^t$.",
               "justificacion_md": "Derivadas estándar de funciones de una variable.",
               "es_resultado": False},
              {"accion_md": "$$\\dfrac{dz}{dt} = (2xy)\\cos t + (x^2 + 2y)e^t$$\n\n"
                            "Sustituyendo $x = \\sin t, y = e^t$:\n\n"
                            "$\\dfrac{dz}{dt} = 2 \\sin t \\cdot e^t \\cos t + (\\sin^2 t + 2e^t)e^t$.",
               "justificacion_md": "**Lección:** generalmente conviene sustituir al final, no al principio.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Regla de la cadena — Caso 2",
          enunciado_md=(
              "Si $z = f(x, y)$ con $x = x(s, t)$, $y = y(s, t)$:\n\n"
              "$$\\dfrac{\\partial z}{\\partial s} = \\dfrac{\\partial f}{\\partial x} \\cdot \\dfrac{\\partial x}{\\partial s} + \\dfrac{\\partial f}{\\partial y} \\cdot \\dfrac{\\partial y}{\\partial s}$$\n\n"
              "$$\\dfrac{\\partial z}{\\partial t} = \\dfrac{\\partial f}{\\partial x} \\cdot \\dfrac{\\partial x}{\\partial t} + \\dfrac{\\partial f}{\\partial y} \\cdot \\dfrac{\\partial y}{\\partial t}$$\n\n"
              "**Idea:** $z$ ahora depende de **dos** variables independientes $(s, t)$. Para cada una, hay dos rutas que pasan por $x$ y $y$. Se aplica el caso 1 \"a cada variable independiente por separado\"."
          )),

        b("ejemplo_resuelto",
          titulo="Caso 2: dos variables intermedias y dos finales",
          problema_md=(
              "Sea $z = x^2 + xy$ con $x = s + t$ y $y = st$. Calcular $\\partial z/\\partial s$ y $\\partial z/\\partial t$."
          ),
          pasos=[
              {"accion_md": "**Parciales de $f$:** $f_x = 2x + y$, $f_y = x$.",
               "justificacion_md": "Estándar.",
               "es_resultado": False},
              {"accion_md": "**Parciales de $x, y$ respecto a $s, t$:**\n\n"
                            "$\\partial x/\\partial s = 1$, $\\partial x/\\partial t = 1$.\n\n"
                            "$\\partial y/\\partial s = t$, $\\partial y/\\partial t = s$.",
               "justificacion_md": "Funciones simples de $s$ y $t$.",
               "es_resultado": False},
              {"accion_md": "**Aplicar:**\n\n"
                            "$\\partial z/\\partial s = (2x + y)(1) + (x)(t) = 2x + y + xt$.\n\n"
                            "$\\partial z/\\partial t = (2x + y)(1) + (x)(s) = 2x + y + xs$.\n\n"
                            "**Sustituyendo** $x = s+t$, $y = st$:\n\n"
                            "$\\partial z/\\partial s = 2(s+t) + st + (s+t)t = 2s + 2t + st + st + t^2 = 2s + 2t + 2st + t^2$.",
               "justificacion_md": "Análogo para $\\partial z/\\partial t$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Derivación implícita",
          body_md=(
              "Si una ecuación $F(x, y) = 0$ define implícitamente $y$ como función de $x$, podemos derivar usando la cadena:\n\n"
              "$$\\dfrac{dy}{dx} = -\\dfrac{F_x}{F_y}$$\n\n"
              "**(Asumiendo $F_y \\neq 0$.)**\n\n"
              "**Análogo en 3 variables:** si $F(x, y, z) = 0$ define $z = z(x, y)$:\n\n"
              "$$\\dfrac{\\partial z}{\\partial x} = -\\dfrac{F_x}{F_z}, \\quad \\dfrac{\\partial z}{\\partial y} = -\\dfrac{F_y}{F_z}$$\n\n"
              "**Mucho más limpia** que la derivación implícita \"a mano\" que vimos en cálculo de una variable."
          )),

        b("ejemplo_resuelto",
          titulo="Derivación implícita rápida",
          problema_md=(
              "Calcular $dy/dx$ en la curva $x^3 + y^3 - 6xy = 0$."
          ),
          pasos=[
              {"accion_md": "**Definir** $F(x, y) = x^3 + y^3 - 6xy$. Calcular parciales:\n\n"
                            "$F_x = 3x^2 - 6y$. $F_y = 3y^2 - 6x$.",
               "justificacion_md": "Tratamos la ecuación como $F(x, y) = 0$ y derivamos.",
               "es_resultado": False},
              {"accion_md": "**Aplicar la fórmula:**\n\n"
                            "$\\dfrac{dy}{dx} = -\\dfrac{F_x}{F_y} = -\\dfrac{3x^2 - 6y}{3y^2 - 6x} = \\dfrac{2y - x^2}{y^2 - 2x}$.",
               "justificacion_md": "**Comparación:** la versión clásica (derivar implícitamente término a término y despejar) habría tomado más pasos. Usar parciales es más mecánico.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $z = f(x, y)$ y $x = x(t), y = y(t)$, entonces $dz/dt$ requiere:",
                  "opciones_md": [
                      "Solo $f_x$ y $f_y$.",
                      "$f_x, f_y, dx/dt, dy/dt$ — los cuatro.",
                      "Solo $dx/dt$ y $dy/dt$.",
                      "Una sola derivada parcial.",
                  ],
                  "correcta": "B",
                  "pista_md": "Cada ruta del diagrama de árbol contribuye con el producto de derivadas a lo largo de ella.",
                  "explicacion_md": (
                      "$dz/dt = f_x \\cdot dx/dt + f_y \\cdot dy/dt$. Necesitamos las **cuatro** derivadas — dos parciales y dos ordinarias."
                  ),
              },
              {
                  "enunciado_md": "Para $F(x, y) = x^2 + y^2 - 25 = 0$ (círculo), $dy/dx = ?$",
                  "opciones_md": ["$x/y$", "$-x/y$", "$y/x$", "$-y/x$"],
                  "correcta": "B",
                  "pista_md": "$F_x = 2x$, $F_y = 2y$. Aplica la fórmula.",
                  "explicacion_md": (
                      "$dy/dx = -F_x/F_y = -2x/2y = -x/y$. **Coincide** con el resultado clásico de derivación implícita."
                  ),
              },
          ]),

        ej(
            titulo="Caso 1 con función trigonométrica",
            enunciado=(
                "Sea $w = \\sin(xy)$ con $x = t^2$ e $y = t^3$. Calcula $dw/dt$ usando la regla de la cadena."
            ),
            pistas=[
                "$w_x = y \\cos(xy)$, $w_y = x \\cos(xy)$.",
                "$dx/dt = 2t$, $dy/dt = 3t^2$.",
            ],
            solucion=(
                "$dw/dt = w_x \\cdot dx/dt + w_y \\cdot dy/dt = y \\cos(xy) \\cdot 2t + x \\cos(xy) \\cdot 3t^2$.\n\n"
                "$= \\cos(xy) (2ty + 3t^2 x)$. Sustituyendo $x = t^2, y = t^3$, $xy = t^5$:\n\n"
                "$= \\cos(t^5)(2t \\cdot t^3 + 3t^2 \\cdot t^2) = \\cos(t^5)(2t^4 + 3t^4) = 5t^4 \\cos(t^5)$.\n\n"
                "**Verificación directa:** $w(t) = \\sin(t^5)$, así $dw/dt = \\cos(t^5) \\cdot 5t^4 = 5t^4 \\cos(t^5)$. ✓"
            ),
        ),

        ej(
            titulo="Implícita en 3 variables",
            enunciado=(
                "La ecuación $x^2 z + y z^2 + xz - 3 = 0$ define $z = z(x, y)$ implícitamente. "
                "Calcula $\\partial z/\\partial x$ y $\\partial z/\\partial y$."
            ),
            pistas=[
                "$F(x, y, z) = x^2 z + y z^2 + xz - 3$.",
                "$F_x = 2xz + z$, $F_y = z^2$, $F_z = x^2 + 2yz + x$.",
                "Aplica $\\partial z / \\partial x = -F_x/F_z$.",
            ],
            solucion=(
                "$F_x = 2xz + z = z(2x + 1)$. $F_y = z^2$. $F_z = x^2 + 2yz + x$.\n\n"
                "$\\partial z/\\partial x = -\\dfrac{z(2x + 1)}{x^2 + 2yz + x}$.\n\n"
                "$\\partial z/\\partial y = -\\dfrac{z^2}{x^2 + 2yz + x}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar sumar las contribuciones** de las distintas rutas del árbol. Cada ruta contribuye con el producto de derivadas a lo largo de ella; **al final se suman**.",
              "**Confundir derivadas ordinarias y parciales** en la fórmula. Si una variable depende de una sola intermedia, es ordinaria; si depende de varias, es parcial.",
              "**Sustituir antes de derivar** cuando la sustitución vuelve la fórmula complicada. Generalmente es más limpio dejar las cosas en función de las intermedias y sustituir al final.",
              "**Olvidar el signo $-$** en la derivación implícita: $dy/dx = -F_x/F_y$, no $F_x/F_y$.",
              "**Aplicar la fórmula implícita cuando $F_y = 0$.** Allí la curva no define $y$ como función de $x$ — son los puntos donde la curva se vuelve vertical o se corta a sí misma.",
          ]),

        b("resumen",
          puntos_md=[
              "**Caso 1** ($z = f(x, y)$, $x, y$ funciones de $t$): $dz/dt = f_x \\cdot dx/dt + f_y \\cdot dy/dt$.",
              "**Caso 2** ($z = f(x, y)$, $x, y$ funciones de $s, t$): igual pero con parciales en cada variable independiente.",
              "**Diagrama de árbol:** herramienta sistemática para construir la fórmula.",
              "**Implícita:** $dy/dx = -F_x/F_y$ desde $F(x, y) = 0$.",
              "**3 variables:** $\\partial z/\\partial x = -F_x/F_z$, $\\partial z/\\partial y = -F_y/F_z$ desde $F(x, y, z) = 0$.",
              "**Próximo capítulo:** aplicaciones de las derivadas parciales — planos tangentes, derivadas direccionales, máximos y mínimos.",
          ]),
    ]
    return {
        "id": "lec-mvar-4-4-cadena",
        "title": "Regla de la cadena",
        "description": "Casos 1 y 2 de la regla de la cadena en varias variables, diagramas de árbol y derivación implícita.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 4,
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

    chapter_id = "ch-derivadas-parciales"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Derivadas Parciales",
        "description": "Derivadas parciales, orden superior, diferenciabilidad, plano tangente y regla de la cadena.",
        "order": 4,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_4_1, lesson_4_2, lesson_4_3, lesson_4_4]
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
    print(f"✅ Capítulo 4 — Derivadas Parciales listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
