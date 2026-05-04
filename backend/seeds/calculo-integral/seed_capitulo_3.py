"""
Seed del curso Cálculo Integral — Capítulo 3: Aplicaciones de la Integral.
9 lecciones:
  3.1 Áreas entre curvas
  3.2 Volúmenes — discos y anillos
  3.3 Volúmenes — cascarones cilíndricos
  3.4 Valor promedio
  3.5 Longitud de arco
  3.6 Áreas de superficies de revolución
  3.7 Aplicaciones en física
  3.8 Aplicaciones en economía
  3.9 Aplicaciones en biología

Incluye figuras (image_url vacío + prompt_image_md) para generar con ChatGPT Images
en las lecciones donde una imagen aporta (volúmenes, áreas, longitudes, etc.).

Idempotente: borra y re-inserta el capítulo y sus lecciones.
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
    "#06b6d4 y ámbar #f59e0b. Sin sombras dramáticas, sin texturas. Apto para libro "
    "universitario."
)


# =====================================================================
# 3.1 Áreas entre curvas
# =====================================================================
def lesson_3_1():
    blocks = [
        b("texto", body_md=(
            "La integral definida calcula el área bajo una curva. "
            "Una **generalización natural** es calcular el área entre **dos** curvas — "
            "el primer paso hacia las aplicaciones geométricas de la integral.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Plantear $A = \\int_a^b [f(x) - g(x)] \\, dx$ cuando $f \\geq g$ en $[a, b]$.\n"
            "- Manejar el caso de **intersecciones múltiples** partiendo el intervalo.\n"
            "- Integrar **respecto a $y$** cuando es más natural.\n"
            "- Evitar el error común de ignorar el signo (siempre **\"arriba menos abajo\"**)."
        )),

        b("intuicion",
          titulo="Restar el área de abajo del área de arriba",
          body_md=(
              "Si $f(x) \\geq g(x)$ en $[a, b]$, el área entre las curvas es la diferencia de áreas bajo cada curva:\n\n"
              "$$A = \\int_a^b f(x) \\, dx - \\int_a^b g(x) \\, dx = \\int_a^b [f(x) - g(x)] \\, dx$$\n\n"
              "**Observación importante:** la fórmula vale aun si una o ambas curvas están bajo el eje $x$ — "
              "lo que importa es cuál está **arriba** y cuál **abajo**, no su signo."
          )),

        fig(
            "Diagrama de área entre dos curvas. Ejes x e y. Dos curvas: una superior y = f(x) en color "
            "teal, una inferior y = g(x) en color azul. Ambas continuas en [a, b]. Marcas en a y b en "
            "el eje x. La región entre las curvas (entre f y g, entre las verticales x=a y x=b) "
            "sombreada en ámbar translúcido. Una flecha vertical entre las dos curvas en algún x "
            "intermedio mostrando 'f(x) - g(x)' (la altura del rectángulo infinitesimal). Etiquetas "
            "claras: 'y = f(x)', 'y = g(x)', 'a', 'b'. " + STYLE
        ),

        b("definicion",
          titulo="Fórmula del área entre curvas",
          body_md=(
              "Si $f, g$ son continuas en $[a, b]$ y $f(x) \\geq g(x)$ para todo $x \\in [a, b]$:\n\n"
              "$$A = \\int_a^b [f(x) - g(x)] \\, dx$$\n\n"
              "**Si las curvas se cruzan:** hay que partir el intervalo en los puntos de intersección "
              "y poner siempre la \"superior menos inferior\" en cada trozo.\n\n"
              "**Variante respecto a $y$:** si las funciones se expresan más fácilmente como $x = h(y)$:\n\n"
              "$$A = \\int_c^d [\\text{derecha}(y) - \\text{izquierda}(y)] \\, dy$$"
          )),

        b("ejemplo_resuelto",
          titulo="Recta y parábola",
          problema_md="Calcular el área entre $y = x$ y $y = x^2$.",
          pasos=[
              {"accion_md": "**Encontrar intersecciones:** $x = x^2 \\implies x(x - 1) = 0 \\implies x = 0, 1$.",
               "justificacion_md": "Igualar las dos funciones para hallar los límites.",
               "es_resultado": False},
              {"accion_md": "**Identificar arriba y abajo en $(0, 1)$:** en $x = 0.5$, $y = 0.5$ vs $y = 0.25$. La recta $y = x$ está **arriba**.",
               "justificacion_md": "Probamos un punto intermedio para no equivocarnos del orden.",
               "es_resultado": False},
              {"accion_md": "**Integrar:**\n\n$$A = \\int_0^1 (x - x^2) \\, dx = \\left[\\dfrac{x^2}{2} - \\dfrac{x^3}{3}\\right]_0^1 = \\dfrac{1}{2} - \\dfrac{1}{3} = \\dfrac{1}{6}$$",
               "justificacion_md": "Aplicación directa de la fórmula.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Curvas que se cruzan: partir el intervalo",
          problema_md="Calcular el área encerrada entre $y = \\sin x$ y $y = \\cos x$ en $[0, \\pi/2]$.",
          pasos=[
              {"accion_md": "**Intersecciones en $[0, \\pi/2]$:** $\\sin x = \\cos x \\iff \\tan x = 1 \\iff x = \\pi/4$.",
               "justificacion_md": "En $[0, \\pi/4]$ el coseno está arriba; en $[\\pi/4, \\pi/2]$ el seno está arriba.",
               "es_resultado": False},
              {"accion_md": "**Partimos en $\\pi/4$:**\n\n$$A = \\int_0^{\\pi/4} (\\cos x - \\sin x) \\, dx + \\int_{\\pi/4}^{\\pi/2} (\\sin x - \\cos x) \\, dx$$",
               "justificacion_md": "Cada trozo respeta \"arriba menos abajo\".",
               "es_resultado": False},
              {"accion_md": "**Calculamos cada uno:**\n\n$\\int_0^{\\pi/4}(\\cos - \\sin) = [\\sin x + \\cos x]_0^{\\pi/4} = (\\sqrt{2}/2 + \\sqrt{2}/2) - (0 + 1) = \\sqrt{2} - 1$.\n\n"
                            "$\\int_{\\pi/4}^{\\pi/2}(\\sin - \\cos) = [-\\cos x - \\sin x]_{\\pi/4}^{\\pi/2} = (0 - 1) - (-\\sqrt{2}/2 - \\sqrt{2}/2) = -1 + \\sqrt{2}$.",
               "justificacion_md": "Antiderivadas estándar evaluadas en cada trozo.",
               "es_resultado": False},
              {"accion_md": "$$A = (\\sqrt{2} - 1) + (\\sqrt{2} - 1) = 2\\sqrt{2} - 2$$",
               "justificacion_md": "**Trampa típica:** si hubiéramos calculado $\\int_0^{\\pi/2}(\\sin - \\cos)$ directo (sin partir), obtendríamos un número distinto y posiblemente con signo incorrecto. Siempre partir en intersecciones.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Integrar respecto a $y$",
          problema_md="Calcular el área encerrada entre $y^2 = x$ y $y = x - 2$.",
          pasos=[
              {"accion_md": "**Reconocer:** la primera curva es una parábola horizontal ($x = y^2$). Si integramos respecto a $x$ habría que partir en pedazos. Más natural: respecto a $y$.",
               "justificacion_md": "Cuando las funciones tienen una sola fórmula como $x(y)$, integrar en $y$ simplifica.",
               "es_resultado": False},
              {"accion_md": "**Reescribir:** $x_{izq}(y) = y^2$ (parábola) y $x_{der}(y) = y + 2$ (recta despejada).",
               "justificacion_md": "Cada función como $x$ en función de $y$.",
               "es_resultado": False},
              {"accion_md": "**Intersecciones:** $y^2 = y + 2 \\iff y^2 - y - 2 = 0 \\iff (y-2)(y+1) = 0 \\iff y = -1, 2$.",
               "justificacion_md": "Resolver la cuadrática.",
               "es_resultado": False},
              {"accion_md": "**Integrar:**\n\n$$A = \\int_{-1}^{2} [(y + 2) - y^2] \\, dy = \\left[\\dfrac{y^2}{2} + 2y - \\dfrac{y^3}{3}\\right]_{-1}^{2}$$\n\n"
                            "$= (2 + 4 - 8/3) - (1/2 - 2 + 1/3) = \\dfrac{10}{3} - (-\\dfrac{7}{6}) = \\dfrac{27}{6} = \\dfrac{9}{2}$",
               "justificacion_md": "**Lección general:** mirar la geometría primero — a veces respecto a $y$ es mucho más cómodo.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el método:",
          preguntas=[
              {
                  "enunciado_md": "Si $f(x) \\geq g(x)$ en $[a, b]$, el área entre las curvas es:",
                  "opciones_md": [
                      "$\\int_a^b [f(x) + g(x)] \\, dx$",
                      "$\\int_a^b [f(x) - g(x)] \\, dx$",
                      "$\\int_a^b |f(x) - g(x)| \\, dx$",
                      "$\\int_a^b f(x) g(x) \\, dx$",
                  ],
                  "correcta": "B",
                  "pista_md": "Si $f$ está arriba, restar $g$ da una altura positiva.",
                  "explicacion_md": (
                      "Cuando $f \\geq g$, la diferencia $f - g$ ya es no negativa, así no hace falta valor absoluto. "
                      "Si las curvas se **cruzan**, sí necesitas partir el intervalo (para evitar $|f-g|$ y mantener el signo)."
                  ),
              },
              {
                  "enunciado_md": "Si dos curvas se cruzan en $c \\in (a, b)$, ¿qué hacer?",
                  "opciones_md": [
                      "Ignorar la intersección.",
                      "Integrar $\\int_a^b |f - g| \\, dx$.",
                      "Partir en $c$ y poner 'arriba menos abajo' en cada trozo.",
                      "Dividir el resultado por 2.",
                  ],
                  "correcta": "C",
                  "pista_md": "El orden 'arriba/abajo' cambia en cada trozo.",
                  "explicacion_md": (
                      "Hay que detectar el cruce, partir el intervalo y, en cada trozo, escribir 'arriba menos abajo'. "
                      "El valor absoluto funciona pero suele ser más laborioso."
                  ),
              },
          ]),

        ej(
            titulo="Parábola y eje x",
            enunciado="Calcula el área de la región acotada por $y = 4 - x^2$ y el eje $x$.",
            pistas=[
                "Encuentra dónde la parábola corta al eje $x$: $4 - x^2 = 0 \\implies x = \\pm 2$.",
                "Entre $-2$ y $2$, la parábola está arriba del eje $x$.",
                "$A = \\int_{-2}^{2} (4 - x^2) \\, dx$.",
            ],
            solucion=(
                "**Intersecciones con el eje:** $x = \\pm 2$. La parábola está arriba en $[-2, 2]$.\n\n"
                "$$A = \\int_{-2}^{2}(4 - x^2) \\, dx = \\left[4x - \\dfrac{x^3}{3}\\right]_{-2}^{2}$$\n\n"
                "$= (8 - 8/3) - (-8 + 8/3) = 16 - 16/3 = \\dfrac{32}{3}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar partir en las intersecciones.** Si $f$ y $g$ se cruzan, integrar en todo el intervalo sin partir mezcla signos.",
              "**Confundir cuál curva está arriba.** Probar siempre con un punto intermedio antes de plantear la integral.",
              "**Pensar que el área puede ser negativa.** El área es siempre $\\geq 0$. Un resultado negativo indica que confundiste el orden.",
              "**No considerar integrar respecto a $y$** cuando la geometría lo pide (parábolas horizontales, etc.).",
              "**Olvidar resolver la ecuación de intersección antes de integrar.** Sin los puntos de cruce no se conocen los límites.",
          ]),

        b("resumen",
          puntos_md=[
              "**Fórmula:** $A = \\int_a^b [\\text{arriba} - \\text{abajo}] \\, dx$ con $a, b$ los puntos de intersección.",
              "**Cruces:** partir el intervalo y respetar el orden en cada trozo.",
              "**Respecto a $y$:** $A = \\int_c^d [\\text{derecha}(y) - \\text{izquierda}(y)] \\, dy$ — útil para parábolas horizontales.",
              "**Verificación rápida:** dibujar la región o probar un punto interior antes de plantear.",
              "**Próxima lección:** volúmenes de sólidos de revolución por discos y anillos.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-1-areas",
        "title": "Áreas entre curvas",
        "description": "Calcular el área de regiones encerradas entre dos curvas, integrando respecto a $x$ o a $y$.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 3.2 Volúmenes — discos y anillos
# =====================================================================
def lesson_3_2():
    blocks = [
        b("texto", body_md=(
            "Cuando una región plana **gira alrededor de un eje**, genera un **sólido de revolución**. "
            "Su volumen se calcula sumando volúmenes de **rodajas infinitesimales** perpendiculares al eje. "
            "Si la rodaja es un disco macizo, hablamos del **método de discos**; si es un disco con un agujero "
            "(un anillo), del **método de anillos** o **washers**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Plantear $V = \\pi \\int_a^b [f(x)]^2 \\, dx$ para el método de discos.\n"
            "- Plantear $V = \\pi \\int_a^b ([R(x)]^2 - [r(x)]^2) \\, dx$ para anillos.\n"
            "- Identificar cuándo usar cada uno."
        )),

        b("intuicion",
          titulo="Rodajas perpendiculares al eje de rotación",
          body_md=(
              "Imagina cortar el sólido en rodajas finitas perpendiculares al eje. Cada rodaja es un cilindro circular "
              "muy delgado (espesor $dx$). \n\n"
              "Si la región original era $0 \\leq y \\leq f(x)$ y se gira alrededor del eje $x$, "
              "la rodaja en la posición $x$ es un **disco** de radio $f(x)$. Su volumen infinitesimal es:\n\n"
              "$$dV = \\pi [f(x)]^2 \\, dx \\quad (\\text{área del círculo} \\times \\text{espesor})$$\n\n"
              "Sumando todas las rodajas con una integral:\n\n"
              "$$V = \\int_a^b dV = \\pi \\int_a^b [f(x)]^2 \\, dx$$"
          )),

        fig(
            "Sólido de revolución por método de discos. Una región plana acotada por y = f(x) (curva "
            "teal), el eje x y las verticales x=a, x=b. Mostrar la región inicial sombreada en ámbar. "
            "Indicar mediante una flecha curva 'gira alrededor del eje x'. A la derecha, mostrar el "
            "sólido 3D resultante (parecido a un trompo o jarrón) con un disco infinitesimal "
            "destacado: un cilindro circular delgado de radio f(x) y espesor dx. Etiquetas: 'y = f(x)', "
            "'a', 'b', 'radio = f(x)', 'dx'. Vista isométrica simple. " + STYLE
        ),

        b("definicion",
          titulo="Método de discos",
          body_md=(
              "Sea la región $0 \\leq y \\leq f(x)$ en $[a, b]$. **Volumen del sólido al girar alrededor del eje $x$:**\n\n"
              "$$V = \\pi \\int_a^b [f(x)]^2 \\, dx$$\n\n"
              "**Análogo respecto al eje $y$** (si $0 \\leq x \\leq g(y)$ en $[c, d]$):\n\n"
              "$$V = \\pi \\int_c^d [g(y)]^2 \\, dy$$"
          )),

        b("ejemplo_resuelto",
          titulo="Volumen de un cono",
          problema_md=(
              "Calcular el volumen del cono generado al girar la región bajo $y = (h/r) x$ entre $0$ y $r$ "
              "alrededor del eje $x$. (Este cono tiene radio de base $h$ y altura $r$, pero al girar la "
              "región queda con la altura coincidiendo con el eje $x$.)"
          ),
          pasos=[
              {"accion_md": "$f(x) = \\dfrac{h}{r} x$. Aplicamos la fórmula de discos:\n\n"
                            "$$V = \\pi \\int_0^r \\left(\\dfrac{h}{r} x\\right)^2 dx = \\pi \\dfrac{h^2}{r^2} \\int_0^r x^2 \\, dx$$",
               "justificacion_md": "$f$ es lineal, así $f^2$ es cuadrática.",
               "es_resultado": False},
              {"accion_md": "$$= \\pi \\dfrac{h^2}{r^2} \\cdot \\dfrac{r^3}{3} = \\dfrac{1}{3}\\pi r h^2$$\n\n"
                            "Reordenando con $r$ como radio de base y $h$ como altura del cono físico:\n\n"
                            "$$V = \\dfrac{1}{3}\\pi r^2 h$$",
               "justificacion_md": "**La fórmula clásica del cono.** Aquí la deducimos en una línea con la integral.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Método de anillos (washers)",
          body_md=(
              "Si la región está entre dos curvas $g(x) \\leq y \\leq f(x)$ y se gira alrededor del eje $x$, "
              "la rodaja es un **anillo** (disco grande menos disco chico):\n\n"
              "$$V = \\pi \\int_a^b \\big( [f(x)]^2 - [g(x)]^2 \\big) \\, dx$$\n\n"
              "**Notación habitual:** $R(x) = $ radio externo (curva más lejana al eje), "
              "$r(x) = $ radio interno (curva más cercana). Entonces:\n\n"
              "$$V = \\pi \\int_a^b \\big( R^2 - r^2 \\big) \\, dx$$\n\n"
              "**Importante:** se eleva al cuadrado **antes** de restar, no al revés. $f^2 - g^2 \\neq (f-g)^2$."
          )),

        fig(
            "Método de anillos (washers). Vista 3D isométrica de un sólido de revolución generado por "
            "una región entre dos curvas y = f(x) (externa, color teal) y y = g(x) (interna, color "
            "azul). Mostrar un anillo infinitesimal: dos cilindros concéntricos, el externo de radio "
            "f(x) y el interno de radio g(x), espesor dx. La región anular sombreada. Etiquetas: "
            "'R(x) = f(x)', 'r(x) = g(x)', 'dx'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Anillos: rotar la región entre $y = \\sqrt{x}$ y $y = x$ alrededor del eje $x$",
          problema_md="Las curvas se cruzan en $x = 0$ y $x = 1$. Calcular el volumen.",
          pasos=[
              {"accion_md": "**Identificar exterior e interior:** en $x = 0.5$, $\\sqrt{0.5} \\approx 0.71 > 0.5$. **$\\sqrt{x}$ está arriba**, así $R(x) = \\sqrt{x}$, $r(x) = x$.",
               "justificacion_md": "Probamos un punto intermedio para saber el orden.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la fórmula:**\n\n$$V = \\pi \\int_0^1 \\big[(\\sqrt{x})^2 - x^2\\big] \\, dx = \\pi \\int_0^1 (x - x^2) \\, dx$$",
               "justificacion_md": "$(\\sqrt{x})^2 = x$.",
               "es_resultado": False},
              {"accion_md": "$$= \\pi \\left[\\dfrac{x^2}{2} - \\dfrac{x^3}{3}\\right]_0^1 = \\pi \\left(\\dfrac{1}{2} - \\dfrac{1}{3}\\right) = \\dfrac{\\pi}{6}$$",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Volumen de una esfera",
          problema_md="Deducir $V = \\dfrac{4}{3}\\pi r^3$ rotando un semicírculo alrededor del eje $x$.",
          pasos=[
              {"accion_md": "**Semicírculo:** $y = \\sqrt{r^2 - x^2}$ en $[-r, r]$. Aplicamos discos:\n\n"
                            "$$V = \\pi \\int_{-r}^{r} (r^2 - x^2) \\, dx$$",
               "justificacion_md": "Elevamos al cuadrado y la raíz desaparece.",
               "es_resultado": False},
              {"accion_md": "**Por simetría** podemos integrar de $0$ a $r$ y multiplicar por $2$:\n\n"
                            "$$V = 2\\pi \\int_0^r (r^2 - x^2) \\, dx = 2\\pi \\left[r^2 x - \\dfrac{x^3}{3}\\right]_0^r = 2\\pi \\left(r^3 - \\dfrac{r^3}{3}\\right) = \\dfrac{4\\pi r^3}{3}$$",
               "justificacion_md": "**La fórmula clásica de la esfera.** Otro caso donde la integral confirma una fórmula geométrica conocida.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el método:",
          preguntas=[
              {
                  "enunciado_md": "El método de **discos** aplica cuando:",
                  "opciones_md": [
                      "La región es entre dos curvas y un eje.",
                      "La región está entre $y = 0$ y $y = f(x)$ (un solo borde curvo).",
                      "El sólido tiene un agujero.",
                      "Se gira alrededor de cualquier recta.",
                  ],
                  "correcta": "B",
                  "pista_md": "Discos = sólido macizo. Anillos = con agujero.",
                  "explicacion_md": (
                      "**Discos:** la rodaja es un círculo macizo (sin agujero). Eso pasa cuando un borde de la región es el propio eje de rotación. **Anillos:** la rodaja tiene un agujero — la región no toca el eje."
                  ),
              },
              {
                  "enunciado_md": "Para anillos: $V = \\pi \\int (R^2 - r^2) \\, dx$ — ¿qué error es típico?",
                  "opciones_md": [
                      "Olvidar el $\\pi$.",
                      "Escribir $(R - r)^2$ en lugar de $R^2 - r^2$.",
                      "Integrar respecto a $y$.",
                      "Usar discos en vez de anillos.",
                  ],
                  "correcta": "B",
                  "pista_md": "$(R-r)^2 \\neq R^2 - r^2$. Hay que **elevar al cuadrado primero**, después restar.",
                  "explicacion_md": (
                      "**$(R-r)^2 = R^2 - 2Rr + r^2$**, distinto de $R^2 - r^2$. La fórmula correcta resta los **cuadrados**: cada disco tiene área $\\pi R^2$ o $\\pi r^2$ por separado."
                  ),
              },
          ]),

        ej(
            titulo="Discos: volumen de un paraboloide",
            enunciado="Calcula el volumen generado al girar $y = x^2$ entre $0$ y $1$ alrededor del eje $x$.",
            pistas=[
                "Discos: $V = \\pi \\int_0^1 (x^2)^2 \\, dx = \\pi \\int_0^1 x^4 \\, dx$.",
                "Antiderivada: $x^5/5$.",
            ],
            solucion=(
                "$$V = \\pi \\int_0^1 x^4 \\, dx = \\pi \\left[\\dfrac{x^5}{5}\\right]_0^1 = \\dfrac{\\pi}{5}$$"
            ),
        ),

        ej(
            titulo="Anillos alrededor de $y = -1$",
            enunciado=(
                "Calcula el volumen al girar la región entre $y = x$ y $y = x^2$ (en $[0, 1]$) alrededor "
                "de la **recta $y = -1$**."
            ),
            pistas=[
                "El eje de rotación es $y = -1$. Los radios se miden **desde** ese eje, no desde $y = 0$.",
                "Radio externo: $R = (\\text{curva más lejos}) - (-1) = x + 1$ (porque $x \\geq x^2$ en $[0,1]$).",
                "Radio interno: $r = x^2 - (-1) = x^2 + 1$.",
            ],
            solucion=(
                "Eje $y = -1$. $R(x) = x - (-1) = x + 1$, $r(x) = x^2 - (-1) = x^2 + 1$.\n\n"
                "$$V = \\pi \\int_0^1 [(x+1)^2 - (x^2+1)^2] \\, dx$$\n\n"
                "$(x+1)^2 = x^2 + 2x + 1$. $(x^2+1)^2 = x^4 + 2x^2 + 1$. Resta: $x^2 + 2x - x^4 - 2x^2 = -x^4 - x^2 + 2x$.\n\n"
                "$$V = \\pi \\int_0^1 (-x^4 - x^2 + 2x) \\, dx = \\pi\\left[-\\dfrac{x^5}{5} - \\dfrac{x^3}{3} + x^2\\right]_0^1 = \\pi\\left(-\\dfrac{1}{5} - \\dfrac{1}{3} + 1\\right) = \\dfrac{7\\pi}{15}$$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar elevar al cuadrado:** la fórmula es $\\pi \\int [f(x)]^2 \\, dx$, no $\\pi \\int f(x) \\, dx$.",
              "**Confundir $(R - r)^2$ con $R^2 - r^2$.** Son cosas distintas: la correcta resta los cuadrados.",
              "**Medir radios desde el eje equivocado.** Si el eje es $y = c$ (no el eje $x$), el radio es $|f(x) - c|$, no $f(x)$.",
              "**No identificar correctamente cuál curva está más lejos del eje.** Probar un punto intermedio.",
              "**Aplicar discos cuando hace falta anillos** (la región no toca el eje).",
          ]),

        b("resumen",
          puntos_md=[
              "**Discos:** $V = \\pi \\int_a^b [f(x)]^2 \\, dx$ — sólido sin agujero.",
              "**Anillos (washers):** $V = \\pi \\int_a^b (R^2 - r^2) \\, dx$ — sólido con agujero.",
              "**Eje arbitrario $y = c$:** los radios se miden como $|f(x) - c|$.",
              "**Identificar bien:** ¿qué curva está más lejos del eje? Probar punto intermedio.",
              "**Próxima lección:** método de cascarones cilíndricos — alternativa cuando discos/anillos resulta complicado.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-2-discos-anillos",
        "title": "Volúmenes — discos y anillos",
        "description": "Volúmenes de sólidos de revolución por rodajas perpendiculares al eje. Métodos de discos y anillos.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 3.3 Volúmenes — cascarones cilíndricos
# =====================================================================
def lesson_3_3():
    blocks = [
        b("texto", body_md=(
            "El **método de cascarones cilíndricos** es una alternativa a discos/anillos: en vez de cortar "
            "el sólido en rodajas perpendiculares al eje, lo cortamos en **cilindros concéntricos** que "
            "envuelven el eje. Cada cascarón es muy fino y se desenrolla mentalmente como un rectángulo.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Plantear $V = 2\\pi \\int_a^b x \\cdot h(x) \\, dx$ para revolución alrededor del eje $y$.\n"
            "- Reconocer cuándo cascarones es más simple que discos/anillos.\n"
            "- Manejar ejes de rotación distintos del eje $y$."
        )),

        b("intuicion",
          titulo="Desenrollar un cascarón",
          body_md=(
              "Imagina un cascarón cilíndrico muy fino: un cilindro circular con radio interior $x$, "
              "espesor $dx$ y altura $h(x)$. \n\n"
              "Si lo cortas verticalmente y lo **desenrollas**, obtienes un rectángulo plano de:\n\n"
              "- **Largo** = perímetro del cilindro = $2\\pi x$.\n"
              "- **Alto** = $h(x)$.\n"
              "- **Espesor** = $dx$.\n\n"
              "Su volumen es entonces $dV = 2\\pi x \\cdot h(x) \\, dx$. Sumando todos los cascarones:\n\n"
              "$$V = 2\\pi \\int_a^b x \\cdot h(x) \\, dx$$"
          )),

        fig(
            "Método de cascarones cilíndricos. Mostrar dos paneles. PANEL 1: la región plana bajo y = "
            "f(x) entre x=a y x=b, con un rectángulo vertical infinitesimal de ancho dx en x. PANEL 2: "
            "el sólido 3D obtenido al girar alrededor del eje y. Destacar un cascarón cilíndrico (un "
            "cilindro hueco muy delgado) en posición x, con altura f(x), radio x, espesor dx. A la "
            "derecha del PANEL 2, mostrar el cascarón 'desenrollado' como un rectángulo plano de "
            "dimensiones 2πx × f(x) × dx. Etiquetas claras. " + STYLE
        ),

        b("definicion",
          titulo="Método de cascarones cilíndricos",
          body_md=(
              "Sea la región $0 \\leq y \\leq f(x)$ en $[a, b]$ con $a \\geq 0$. **Volumen al girar alrededor del eje $y$:**\n\n"
              "$$V = 2\\pi \\int_a^b x \\cdot f(x) \\, dx$$\n\n"
              "**Notación general:** $V = 2\\pi \\int (\\text{radio})(\\text{altura}) \\, dx$, donde:\n\n"
              "- **radio** = distancia al eje de rotación.\n"
              "- **altura** = $f(x) - g(x)$ si la región está entre dos curvas.\n\n"
              "**Si la región se da en función de $y$** ($0 \\leq x \\leq g(y)$) y giramos alrededor del eje $x$:\n\n"
              "$$V = 2\\pi \\int_c^d y \\cdot g(y) \\, dy$$"
          )),

        b("intuicion",
          titulo="¿Cuándo cascarones vs discos?",
          body_md=(
              "**Cascarones es ventajoso cuando:**\n\n"
              "- La función está dada como $y = f(x)$ y el eje de rotación es **vertical** (eje $y$ o $x = c$). "
              "Discos requeriría despejar $x = f^{-1}(y)$, que puede ser complicado.\n\n"
              "**Discos/anillos es ventajoso cuando:**\n\n"
              "- La función está dada como $y = f(x)$ y el eje de rotación es **horizontal** (eje $x$ o $y = c$).\n\n"
              "**Regla práctica:** cascarones usa el eje de rotación **paralelo** al eje de la variable de integración. "
              "Discos/anillos usa el eje **perpendicular**."
          )),

        b("ejemplo_resuelto",
          titulo="Caso clásico: $y = x^2$ rotando alrededor del eje $y$",
          problema_md="Región entre $y = x^2$ y el eje $x$ en $[0, 2]$. Volumen al girar alrededor del eje $y$.",
          pasos=[
              {"accion_md": "**Por cascarones:** radio $= x$, altura $= x^2$.\n\n$$V = 2\\pi \\int_0^2 x \\cdot x^2 \\, dx = 2\\pi \\int_0^2 x^3 \\, dx$$",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "$$= 2\\pi \\left[\\dfrac{x^4}{4}\\right]_0^2 = 2\\pi \\cdot 4 = 8\\pi$$",
               "justificacion_md": "Cálculo trivial. **Por discos** habría sido más laborioso: tendríamos que invertir $x = \\sqrt{y}$ e integrar respecto a $y$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cascarones con curva entre dos funciones",
          problema_md=(
              "Región entre $y = x$ y $y = x^2$ en $[0, 1]$. Volumen al girar alrededor del eje $y$."
          ),
          pasos=[
              {"accion_md": "**Identificar altura:** en $[0, 1]$, $x \\geq x^2$, así altura $= x - x^2$.",
               "justificacion_md": "Restar la curva inferior de la superior.",
               "es_resultado": False},
              {"accion_md": "**Aplicar:**\n\n$$V = 2\\pi \\int_0^1 x \\cdot (x - x^2) \\, dx = 2\\pi \\int_0^1 (x^2 - x^3) \\, dx$$",
               "justificacion_md": "Radio $= x$, altura $= x - x^2$.",
               "es_resultado": False},
              {"accion_md": "$$= 2\\pi \\left[\\dfrac{x^3}{3} - \\dfrac{x^4}{4}\\right]_0^1 = 2\\pi \\left(\\dfrac{1}{3} - \\dfrac{1}{4}\\right) = \\dfrac{\\pi}{6}$$",
               "justificacion_md": "**Verificación cruzada:** podríamos también haberlo hecho por anillos respecto a $y$ — daría el mismo $\\pi/6$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Eje de rotación distinto del eje $y$",
          problema_md="Región $0 \\leq y \\leq x^2$ en $[0, 1]$. Girar alrededor de la recta $x = -1$.",
          pasos=[
              {"accion_md": "**Eje $x = -1$:** el radio del cascarón en posición $x$ es la distancia $x - (-1) = x + 1$.",
               "justificacion_md": "Radio se mide **desde el eje de rotación**, no desde el origen.",
               "es_resultado": False},
              {"accion_md": "**Altura:** $x^2$ (la región va desde $y = 0$ hasta $y = x^2$).",
               "justificacion_md": "Sin cambios respecto del caso clásico — la altura es la misma.",
               "es_resultado": False},
              {"accion_md": "$$V = 2\\pi \\int_0^1 (x + 1)(x^2) \\, dx = 2\\pi \\int_0^1 (x^3 + x^2) \\, dx$$\n\n"
                            "$$= 2\\pi \\left[\\dfrac{x^4}{4} + \\dfrac{x^3}{3}\\right]_0^1 = 2\\pi \\left(\\dfrac{1}{4} + \\dfrac{1}{3}\\right) = \\dfrac{7\\pi}{6}$$",
               "justificacion_md": "**Patrón general:** cuando el eje cambia, solo cambia la fórmula del **radio**.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el criterio:",
          preguntas=[
              {
                  "enunciado_md": "Para girar la región bajo $y = f(x)$ alrededor del **eje $y$**, ¿cuál fórmula es más directa?",
                  "opciones_md": [
                      "Discos: $\\pi \\int [f(x)]^2 dx$.",
                      "Anillos respecto a $x$.",
                      "Cascarones: $2\\pi \\int x f(x) \\, dx$.",
                      "Cualquier método da igual de fácil.",
                  ],
                  "correcta": "C",
                  "pista_md": "Rotación alrededor del eje vertical ($y$) + función $y = f(x)$ → cascarones suele ser directo.",
                  "explicacion_md": (
                      "Cascarones evita despejar $x$ en función de $y$, que puede ser difícil o no tener forma cerrada."
                  ),
              },
              {
                  "enunciado_md": "$V = 2\\pi \\int (\\text{radio})(\\text{altura}) \\, dx$. Si el eje es $x = 5$ y la región está en $[0, 3]$, el radio es:",
                  "opciones_md": [
                      "$x$",
                      "$5$",
                      "$5 - x$",
                      "$x - 5$",
                  ],
                  "correcta": "C",
                  "pista_md": "El radio es la distancia desde la posición $x$ al eje $x = 5$, y debe ser positiva.",
                  "explicacion_md": (
                      "$x \\in [0, 3]$ y el eje está en $5$, así $x < 5$ siempre. La distancia es $5 - x > 0$."
                  ),
              },
          ]),

        ej(
            titulo="Cascarones rápido",
            enunciado="Calcula el volumen al girar $y = x^3$ entre $0$ y $1$ alrededor del eje $y$.",
            pistas=[
                "Cascarones: radio $= x$, altura $= x^3$.",
                "$V = 2\\pi \\int_0^1 x \\cdot x^3 \\, dx$.",
            ],
            solucion=(
                "$$V = 2\\pi \\int_0^1 x^4 \\, dx = 2\\pi \\left[\\dfrac{x^5}{5}\\right]_0^1 = \\dfrac{2\\pi}{5}$$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el $2\\pi$.** Es el perímetro del cascarón al desenrollarlo.",
              "**Confundir radio con $x$ siempre.** Si el eje no es el $y$, el radio es la distancia al eje (puede ser $x \\pm c$).",
              "**Usar la altura equivocada.** Si la región está entre dos curvas, la altura es la diferencia, no solo $f(x)$.",
              "**Aplicar cascarones cuando discos/anillos sería trivial** (y viceversa). Pensar antes qué método se ajusta a la geometría.",
              "**Olvidar que el método requiere $a \\geq 0$ (en su forma básica).** Si la región atraviesa el eje, hay que adaptar.",
          ]),

        b("resumen",
          puntos_md=[
              "**Cascarones cilíndricos:** $V = 2\\pi \\int (\\text{radio})(\\text{altura}) \\, dx$.",
              "**Cuándo conviene:** función dada como $y = f(x)$ + eje de rotación **vertical** (paralelo a la variable que integramos).",
              "**Eje arbitrario:** el radio se mide desde el eje de rotación.",
              "**Comparación con discos:** cascarones evita invertir la función. Discos evita el factor $x$ extra.",
              "**Próxima lección:** valor promedio de una función en un intervalo.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-3-cascarones",
        "title": "Volúmenes — cascarones cilíndricos",
        "description": "Método alternativo para volúmenes de revolución usando cilindros concéntricos al eje.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# 3.4 Valor promedio
# =====================================================================
def lesson_3_4():
    blocks = [
        b("texto", body_md=(
            "El **valor promedio** de una función en un intervalo generaliza la idea de promedio aritmético: "
            "en vez de promediar finitos valores, promediamos un continuo de valores. "
            "La integral nos lo permite calcular en una línea.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y calcular $f_{\\text{prom}} = \\dfrac{1}{b-a} \\int_a^b f(x) \\, dx$.\n"
            "- Aplicar el **teorema del valor medio para integrales**.\n"
            "- Interpretar geométricamente el promedio (rectángulo con la misma área)."
        )),

        b("intuicion",
          titulo="Del promedio discreto al continuo",
          body_md=(
              "Si tienes $n$ valores $y_1, \\ldots, y_n$, su promedio es $\\bar{y} = \\dfrac{y_1 + \\cdots + y_n}{n}$. "
              "Para una función continua $f$ en $[a, b]$, hacemos lo análogo:\n\n"
              "1. Tomar $n$ valores $f(x_1), \\ldots, f(x_n)$ con $x_i$ equiespaciados, $\\Delta x = (b-a)/n$.\n"
              "2. Promediar: $\\bar{f}_n = \\dfrac{1}{n}\\sum f(x_i) = \\dfrac{1}{b-a}\\sum f(x_i) \\Delta x$.\n"
              "3. Tomar $n \\to \\infty$: la suma de Riemann converge a $\\int_a^b f \\, dx$.\n\n"
              "Resultado:\n\n"
              "$$f_{\\text{prom}} = \\dfrac{1}{b-a} \\int_a^b f(x) \\, dx$$"
          )),

        b("definicion",
          titulo="Valor promedio",
          body_md=(
              "Sea $f$ continua en $[a, b]$. El **valor promedio** de $f$ en $[a, b]$ es:\n\n"
              "$$f_{\\text{prom}} = \\dfrac{1}{b-a} \\int_a^b f(x) \\, dx$$\n\n"
              "**Interpretación geométrica:** $f_{\\text{prom}}$ es la altura del rectángulo de base $[a, b]$ "
              "que tiene la **misma área** que la región bajo $f$:\n\n"
              "$$f_{\\text{prom}} \\cdot (b - a) = \\int_a^b f(x) \\, dx$$"
          )),

        fig(
            "Interpretación geométrica del valor promedio. Una curva continua y = f(x) sobre el "
            "intervalo [a, b] en color teal. La región bajo la curva sombreada en ámbar translúcido. "
            "Una recta horizontal y = f_prom (en azul punteado) que pasa por el medio del intervalo, "
            "tal que el rectángulo de altura f_prom y base [a, b] tiene la misma área que la región "
            "bajo la curva. Marcar las dos áreas iguales con etiquetas. Etiquetas: 'a', 'b', "
            "'y = f(x)', 'f_prom' (en la línea horizontal). " + STYLE
        ),

        b("teorema",
          nombre="Teorema del valor medio para integrales",
          enunciado_md=(
              "Si $f$ es continua en $[a, b]$, entonces existe $c \\in [a, b]$ tal que:\n\n"
              "$$f(c) = f_{\\text{prom}} = \\dfrac{1}{b-a} \\int_a^b f(x) \\, dx$$\n\n"
              "Es decir, **la función alcanza su valor promedio** en al menos un punto del intervalo."
          ),
          demostracion_md=(
              "Sea $A(x) = \\int_a^x f(t) \\, dt$. Por el TFC parte 1, $A$ es derivable y $A'(x) = f(x)$. "
              "Aplicando el TVM a $A$ en $[a, b]$, existe $c \\in (a, b)$ con\n\n"
              "$$A'(c) = \\dfrac{A(b) - A(a)}{b - a} = \\dfrac{\\int_a^b f - 0}{b-a} = f_{\\text{prom}}$$\n\n"
              "Pero $A'(c) = f(c)$, así $f(c) = f_{\\text{prom}}$."
          )),

        b("ejemplo_resuelto",
          titulo="Promedio de $f(x) = x^2$ en $[0, 3]$",
          problema_md="Calcular el valor promedio.",
          pasos=[
              {"accion_md": "$$f_{\\text{prom}} = \\dfrac{1}{3 - 0} \\int_0^3 x^2 \\, dx = \\dfrac{1}{3} \\cdot \\dfrac{27}{3} = 3$$",
               "justificacion_md": "Aplicación directa de la fórmula.",
               "es_resultado": False},
              {"accion_md": "**Por TVM-integrales:** existe $c \\in [0, 3]$ con $f(c) = c^2 = 3$, así $c = \\sqrt{3} \\approx 1.73$.",
               "justificacion_md": "El punto $c$ existe y se puede calcular explícitamente. Geométricamente: a la altura $y = 3$, la curva $y = x^2$ vale $3$ exactamente en $x = \\sqrt{3}$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Promedio de la temperatura",
          problema_md=(
              "Si la temperatura a las $t$ horas (en $[0, 24]$) es $T(t) = 20 + 5\\sin\\left(\\dfrac{\\pi t}{12}\\right)$ "
              "grados, calcular la temperatura promedio del día."
          ),
          pasos=[
              {"accion_md": "$$T_{\\text{prom}} = \\dfrac{1}{24} \\int_0^{24} \\left(20 + 5\\sin\\left(\\dfrac{\\pi t}{12}\\right)\\right) dt$$",
               "justificacion_md": "Fórmula con $a = 0$, $b = 24$.",
               "es_resultado": False},
              {"accion_md": "**Separar:** $\\int 20 \\, dt + 5 \\int \\sin\\left(\\dfrac{\\pi t}{12}\\right) dt$.\n\n"
                            "Para la segunda, sustituir $u = \\pi t / 12$: $\\int \\sin u \\cdot \\dfrac{12}{\\pi} du = -\\dfrac{12}{\\pi}\\cos u$.\n\n"
                            "Evaluar en $[0, 24]$: $\\cos(2\\pi) - \\cos(0) = 1 - 1 = 0$. **Esa integral es $0$.**",
               "justificacion_md": "Un período completo del seno tiene integral cero.",
               "es_resultado": False},
              {"accion_md": "$$T_{\\text{prom}} = \\dfrac{1}{24} \\cdot (20 \\cdot 24 + 0) = 20°$$",
               "justificacion_md": "**Lección:** el promedio del seno (puro) sobre un período es $0$. La temperatura promedio es solo la constante.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el concepto:",
          preguntas=[
              {
                  "enunciado_md": "El valor promedio de $f(x) = x$ en $[0, 4]$ es:",
                  "opciones_md": ["$1$", "$2$", "$4$", "$8$"],
                  "correcta": "B",
                  "pista_md": "$\\int_0^4 x \\, dx = 8$. Divide por $4 - 0 = 4$.",
                  "explicacion_md": (
                      "$\\dfrac{1}{4} \\int_0^4 x \\, dx = \\dfrac{1}{4} \\cdot 8 = 2$. **Geométricamente:** $f$ es lineal, su promedio es el promedio aritmético de los extremos: $(0 + 4)/2 = 2$."
                  ),
              },
              {
                  "enunciado_md": "¿Qué garantiza el TVM para integrales?",
                  "opciones_md": [
                      "Que $f_{\\text{prom}} = (f(a) + f(b))/2$.",
                      "Que existe $c \\in [a,b]$ donde $f(c) = f_{\\text{prom}}$.",
                      "Que $f$ es derivable.",
                      "Que la integral es positiva.",
                  ],
                  "correcta": "B",
                  "pista_md": "Es el análogo del TVM de derivadas, pero para integrales.",
                  "explicacion_md": (
                      "El TVM-integrales garantiza que el promedio se **realiza** efectivamente como un valor de la función — no solo es un número en abstracto."
                  ),
              },
          ]),

        ej(
            titulo="Velocidad promedio",
            enunciado=(
                "Un objeto se mueve con velocidad $v(t) = 3t^2$ m/s. ¿Cuál es su velocidad promedio "
                "entre $t = 0$ y $t = 2$ segundos?"
            ),
            pistas=[
                "$v_{\\text{prom}} = \\dfrac{1}{2-0} \\int_0^2 3t^2 \\, dt$.",
                "Antiderivada de $3t^2$: $t^3$.",
            ],
            solucion=(
                "$$v_{\\text{prom}} = \\dfrac{1}{2} \\int_0^2 3t^2 \\, dt = \\dfrac{1}{2}[t^3]_0^2 = \\dfrac{8}{2} = 4 \\text{ m/s}$$\n\n"
                "**Verificación:** la posición es $s(t) = t^3$. La distancia recorrida en $[0, 2]$ es $s(2) - s(0) = 8 - 0 = 8$ m. Promedio = $8/2 = 4$ m/s. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar dividir por $(b - a)$.** Lo que sale del integral es área; el promedio es área dividida entre el ancho.",
              "**Confundir promedio con valor medio del intervalo:** $f_{\\text{prom}} \\neq f((a+b)/2)$ en general (son iguales solo si $f$ es lineal).",
              "**Confundir velocidad promedio con rapidez promedio.** La primera puede ser negativa o cero (si vuelve al origen); la segunda no.",
              "**Aplicar el TVM-integrales sin continuidad** — es necesaria para que el $c$ exista.",
          ]),

        b("resumen",
          puntos_md=[
              "**Fórmula:** $f_{\\text{prom}} = \\dfrac{1}{b-a}\\int_a^b f \\, dx$.",
              "**Interpretación geométrica:** altura del rectángulo con la misma área que la región bajo $f$.",
              "**TVM-integrales:** existe $c \\in [a, b]$ con $f(c) = f_{\\text{prom}}$ (si $f$ es continua).",
              "**Aplicaciones:** temperatura promedio, velocidad promedio, etc.",
              "**Próxima lección:** longitud de arco — medir cuánto mide una curva.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-4-promedio",
        "title": "Valor promedio",
        "description": "Promedio continuo de una función con la integral. Teorema del valor medio para integrales.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 4,
    }


# =====================================================================
# 3.5 Longitud de arco
# =====================================================================
def lesson_3_5():
    blocks = [
        b("texto", body_md=(
            "Si conocemos $y = f(x)$ en $[a, b]$, ¿cuánto mide la **curva**? "
            "Esta es la pregunta de la **longitud de arco**: medir la distancia recorrida a lo largo de la "
            "gráfica, no el área debajo.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Plantear $L = \\int_a^b \\sqrt{1 + [f'(x)]^2} \\, dx$.\n"
            "- Comprender la idea geométrica (Pitágoras infinitesimal).\n"
            "- Aplicar la fórmula a curvas concretas, reconociendo cuándo el integrando se simplifica."
        )),

        b("intuicion",
          titulo="Pitágoras infinitesimal",
          body_md=(
              "Aproximamos la curva con segmentos rectos pequeños y sumamos sus longitudes. "
              "Cada segmento entre $(x, f(x))$ y $(x + dx, f(x + dx))$ tiene componentes:\n\n"
              "- Horizontal: $dx$.\n"
              "- Vertical: $dy = f'(x) \\, dx$ (aproximadamente).\n\n"
              "Por Pitágoras, su longitud infinitesimal es:\n\n"
              "$$ds = \\sqrt{(dx)^2 + (dy)^2} = \\sqrt{1 + \\left(\\dfrac{dy}{dx}\\right)^2} \\, dx$$\n\n"
              "Sumando todos los segmentos con una integral:\n\n"
              "$$L = \\int_a^b ds = \\int_a^b \\sqrt{1 + [f'(x)]^2} \\, dx$$"
          )),

        fig(
            "Aproximación de longitud de arco. Eje x e y. Una curva suave y = f(x) en color teal entre "
            "x = a y x = b. La curva aproximada por una poligonal de varios segmentos rectos cortos "
            "(unos 8 segmentos) en color azul. Hacer zoom en uno de los segmentos: mostrar que el "
            "segmento tiene componente horizontal dx y vertical dy, formando un triángulo rectángulo. "
            "Etiquetas: 'a', 'b', 'y = f(x)', 'dx', 'dy', 'ds = √(dx² + dy²)' en el segmento "
            "ampliado. " + STYLE
        ),

        b("definicion",
          titulo="Longitud de arco",
          body_md=(
              "Si $f$ es derivable con derivada continua en $[a, b]$, la **longitud de arco** de la curva "
              "$y = f(x)$ entre $a$ y $b$ es:\n\n"
              "$$L = \\int_a^b \\sqrt{1 + [f'(x)]^2} \\, dx$$\n\n"
              "**Versión respecto a $y$** (si la curva es $x = g(y)$ en $[c, d]$):\n\n"
              "$$L = \\int_c^d \\sqrt{1 + [g'(y)]^2} \\, dy$$\n\n"
              "**Forma paramétrica** (si $x = x(t)$, $y = y(t)$ en $[\\alpha, \\beta]$):\n\n"
              "$$L = \\int_\\alpha^\\beta \\sqrt{[x'(t)]^2 + [y'(t)]^2} \\, dt$$"
          )),

        b("intuicion",
          titulo="¿Por qué el integrando rara vez es bonito?",
          body_md=(
              "El integrando $\\sqrt{1 + [f'(x)]^2}$ tiene una raíz cuadrada que casi nunca se simplifica. "
              "Para que la integral tenga forma cerrada, $1 + [f'(x)]^2$ debe ser un **cuadrado perfecto**.\n\n"
              "**Casos típicos donde sí sale bien:** funciones diseñadas a propósito para que $1 + (f')^2 = (\\text{algo})^2$. "
              "Por ejemplo $f(x) = \\dfrac{x^2}{2} - \\dfrac{\\ln x}{4}$ produce un cuadrado perfecto.\n\n"
              "En la práctica, **muchas longitudes de arco se calculan numéricamente** porque las antiderivadas no son elementales."
          )),

        b("ejemplo_resuelto",
          titulo="Longitud de un segmento de parábola",
          problema_md="Calcular la longitud de la curva $y = \\dfrac{2}{3}(x-1)^{3/2}$ en $[1, 4]$.",
          pasos=[
              {"accion_md": "**Derivada:** $f'(x) = \\dfrac{2}{3} \\cdot \\dfrac{3}{2}(x-1)^{1/2} = (x-1)^{1/2}$.\n\n"
                            "**Cuadrado:** $[f'(x)]^2 = x - 1$.",
               "justificacion_md": "La curva está hecha para que el cuadrado dé algo simple.",
               "es_resultado": False},
              {"accion_md": "**Integrando:** $\\sqrt{1 + (x-1)} = \\sqrt{x}$.\n\n"
                            "$$L = \\int_1^4 \\sqrt{x} \\, dx = \\left[\\dfrac{2}{3} x^{3/2}\\right]_1^4 = \\dfrac{2}{3}(8 - 1) = \\dfrac{14}{3}$$",
               "justificacion_md": "$\\sqrt{1 + (x-1)} = \\sqrt{x}$ es uno de esos casos donde el cuadrado perfecto sale.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Catenaria: longitud de $y = \\cosh x$ en $[0, 1]$",
          problema_md="Calcular la longitud.",
          pasos=[
              {"accion_md": "**Derivada:** $f'(x) = \\sinh x$. Cuadrado: $\\sinh^2 x$.\n\n"
                            "**Integrando:** $\\sqrt{1 + \\sinh^2 x} = \\sqrt{\\cosh^2 x} = \\cosh x$.",
               "justificacion_md": "Identidad hiperbólica $1 + \\sinh^2 = \\cosh^2$. **La catenaria está diseñada para esto.**",
               "es_resultado": False},
              {"accion_md": "$$L = \\int_0^1 \\cosh x \\, dx = [\\sinh x]_0^1 = \\sinh 1 - 0 = \\sinh 1 \\approx 1.175$$",
               "justificacion_md": "**Resultado clásico.** Por eso las funciones hiperbólicas aparecen tanto en problemas de cables colgantes.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el concepto:",
          preguntas=[
              {
                  "enunciado_md": "$L = \\int_a^b \\sqrt{1 + [f'(x)]^2} \\, dx$. El factor $\\sqrt{1 + (f')^2}$ proviene de:",
                  "opciones_md": [
                      "Pitágoras aplicado a un segmento infinitesimal.",
                      "Producto escalar.",
                      "Identidad pitagórica trigonométrica.",
                      "Definición arbitraria.",
                  ],
                  "correcta": "A",
                  "pista_md": "Cada segmento es la hipotenusa de un triángulo con catetos $dx$ y $dy = f'(x) dx$.",
                  "explicacion_md": (
                      "$ds = \\sqrt{(dx)^2 + (dy)^2}$ es Pitágoras. Factorizando $dx$: $ds = \\sqrt{1 + (dy/dx)^2} \\, dx$."
                  ),
              },
              {
                  "enunciado_md": "Para $y = mx + b$ (lineal) en $[a, b]$, la longitud es:",
                  "opciones_md": [
                      "$b - a$",
                      "$\\sqrt{1 + m^2}(b - a)$",
                      "$m(b - a)$",
                      "$\\int (mx + b) \\, dx$",
                  ],
                  "correcta": "B",
                  "pista_md": "$f' = m$ constante. La integral es trivial.",
                  "explicacion_md": (
                      "$L = \\int_a^b \\sqrt{1 + m^2} \\, dx = \\sqrt{1 + m^2}(b - a)$. **Verificación geométrica:** Pitágoras: $\\sqrt{(\\Delta x)^2 + (\\Delta y)^2} = \\sqrt{1 + m^2} \\Delta x$. ✓"
                  ),
              },
          ]),

        ej(
            titulo="Otra curva con cuadrado perfecto",
            enunciado=(
                "Calcula la longitud de $y = \\dfrac{x^3}{3} + \\dfrac{1}{4x}$ en $[1, 2]$."
            ),
            pistas=[
                "$f'(x) = x^2 - \\dfrac{1}{4x^2}$.",
                "$1 + [f'(x)]^2 = 1 + x^4 - \\dfrac{1}{2} + \\dfrac{1}{16 x^4} = x^4 + \\dfrac{1}{2} + \\dfrac{1}{16x^4} = \\left(x^2 + \\dfrac{1}{4x^2}\\right)^2$. ¡Cuadrado perfecto!",
                "Así $\\sqrt{1 + (f')^2} = x^2 + \\dfrac{1}{4x^2}$.",
            ],
            solucion=(
                "$$L = \\int_1^2 \\left(x^2 + \\dfrac{1}{4x^2}\\right) dx = \\left[\\dfrac{x^3}{3} - \\dfrac{1}{4x}\\right]_1^2$$\n\n"
                "$= \\left(\\dfrac{8}{3} - \\dfrac{1}{8}\\right) - \\left(\\dfrac{1}{3} - \\dfrac{1}{4}\\right) = \\dfrac{64 - 3}{24} - \\dfrac{4 - 3}{12} = \\dfrac{61}{24} - \\dfrac{1}{12} = \\dfrac{59}{24}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir longitud con área.** $L \\neq \\int f \\, dx$ — la longitud lleva la raíz $\\sqrt{1 + (f')^2}$.",
              "**Olvidar el $1 +$** dentro de la raíz: el integrando es $\\sqrt{1 + (f')^2}$, no $\\sqrt{(f')^2} = |f'|$.",
              "**Asumir que la integral siempre tiene forma cerrada.** En la práctica, muchas requieren métodos numéricos.",
              "**Confundir $[f'(x)]^2$ con $(f^2)'(x)$.** El primero es la derivada al cuadrado; el segundo, la derivada del cuadrado de $f$ (igual a $2 f f'$).",
          ]),

        b("resumen",
          puntos_md=[
              "**Fórmula:** $L = \\int_a^b \\sqrt{1 + [f'(x)]^2} \\, dx$.",
              "**Origen:** Pitágoras aplicado a segmentos infinitesimales.",
              "**Versiones:** respecto a $y$ ($\\sqrt{1 + [g'(y)]^2}$) y paramétrica ($\\sqrt{[x'(t)]^2 + [y'(t)]^2}$).",
              "**El integrando rara vez es bonito** — solo en curvas \"diseñadas\" da forma cerrada.",
              "**Próxima lección:** áreas de superficies de revolución — combinar longitud de arco con rotación.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-5-arco",
        "title": "Longitud de arco",
        "description": "Medir la longitud de una curva usando $L = \\int \\sqrt{1 + (f')^2} \\, dx$.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 5,
    }


# =====================================================================
# 3.6 Áreas de superficies de revolución
# =====================================================================
def lesson_3_6():
    blocks = [
        b("texto", body_md=(
            "Cuando una curva $y = f(x)$ gira alrededor de un eje, no solo genera un sólido (volumen) "
            "sino también una **superficie**. La fórmula para el área de esa superficie combina la idea "
            "de longitud de arco con la del perímetro circular generado por la rotación.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Plantear $S = 2\\pi \\int_a^b f(x) \\sqrt{1 + [f'(x)]^2} \\, dx$ para revolución alrededor del eje $x$.\n"
            "- Comprender la deducción (perímetro × longitud infinitesimal de arco).\n"
            "- Reconocer cuándo el integrando se simplifica a forma cerrada."
        )),

        b("intuicion",
          titulo="Bandas cilíndricas infinitesimales",
          body_md=(
              "Imagina la curva $y = f(x)$ girando alrededor del eje $x$. Cada segmento infinitesimal de "
              "la curva, de longitud $ds = \\sqrt{1 + (f')^2}\\, dx$, genera una **banda cónica** (un anillo) "
              "al girar:\n\n"
              "- **Circunferencia** del anillo $= 2\\pi \\cdot (\\text{distancia al eje}) = 2\\pi f(x)$.\n"
              "- **Ancho** de la banda $= ds$.\n\n"
              "Su área infinitesimal es $dS = 2\\pi f(x) \\, ds$. Sumando:\n\n"
              "$$S = \\int_a^b 2\\pi f(x) \\sqrt{1 + [f'(x)]^2} \\, dx$$"
          )),

        fig(
            "Superficie de revolución generada por la curva y = f(x) (en color teal) al girar "
            "alrededor del eje x. Vista isométrica del sólido 3D mostrando la superficie exterior "
            "(no el volumen interior). Destacar una banda anular infinitesimal: un anillo cónico de "
            "circunferencia 2πf(x) y ancho ds, posicionado a una distancia x del origen. Etiquetas: "
            "'y = f(x)', 'eje x' (eje de rotación), 'radio = f(x)', 'ancho = ds'. " + STYLE
        ),

        b("definicion",
          titulo="Área de superficie de revolución",
          body_md=(
              "Si $f \\geq 0$ es derivable con derivada continua en $[a, b]$, el **área de la superficie** "
              "generada al girar $y = f(x)$ alrededor del eje $x$ es:\n\n"
              "$$S = 2\\pi \\int_a^b f(x) \\sqrt{1 + [f'(x)]^2} \\, dx$$\n\n"
              "**Alrededor del eje $y$** (curva $x = g(y)$ en $[c, d]$):\n\n"
              "$$S = 2\\pi \\int_c^d g(y) \\sqrt{1 + [g'(y)]^2} \\, dy$$\n\n"
              "**Forma general:** $S = 2\\pi \\int (\\text{distancia al eje}) \\, ds$, "
              "con $ds$ la longitud de arco infinitesimal."
          )),

        b("ejemplo_resuelto",
          titulo="Superficie de una esfera",
          problema_md="Deducir $S = 4\\pi r^2$ rotando $y = \\sqrt{r^2 - x^2}$ en $[-r, r]$ alrededor del eje $x$.",
          pasos=[
              {"accion_md": "**Derivada:** $f'(x) = -\\dfrac{x}{\\sqrt{r^2 - x^2}}$. **Cuadrado:** $\\dfrac{x^2}{r^2 - x^2}$.\n\n"
                            "$$1 + [f']^2 = 1 + \\dfrac{x^2}{r^2 - x^2} = \\dfrac{r^2}{r^2 - x^2}$$",
               "justificacion_md": "Suma de fracciones con denominador común.",
               "es_resultado": False},
              {"accion_md": "**Raíz:** $\\sqrt{1 + [f']^2} = \\dfrac{r}{\\sqrt{r^2 - x^2}}$.\n\n"
                            "**Integrando:**\n\n$$f(x) \\sqrt{1 + [f']^2} = \\sqrt{r^2 - x^2} \\cdot \\dfrac{r}{\\sqrt{r^2 - x^2}} = r$$",
               "justificacion_md": "**Magia:** la raíz del numerador y denominador se cancela. Queda solo $r$, una constante.",
               "es_resultado": False},
              {"accion_md": "$$S = 2\\pi \\int_{-r}^{r} r \\, dx = 2\\pi r \\cdot 2r = 4\\pi r^2$$",
               "justificacion_md": "**La fórmula clásica de la esfera.** Otra confirmación de cómo la integral convierte fórmulas geométricas en cálculos de una línea.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Superficie de un cono",
          problema_md=(
              "Calcular el área lateral del cono generado al girar $y = x$ entre $0$ y $h$ alrededor "
              "del eje $x$. (Es un cono con altura $h$ y radio de base $h$.)"
          ),
          pasos=[
              {"accion_md": "$f(x) = x$, $f'(x) = 1$, así $\\sqrt{1 + 1} = \\sqrt{2}$.\n\n"
                            "$$S = 2\\pi \\int_0^h x \\cdot \\sqrt{2} \\, dx = 2\\pi \\sqrt{2} \\cdot \\dfrac{h^2}{2} = \\pi h^2 \\sqrt{2}$$",
               "justificacion_md": "Integral trivial. **Comparación con la fórmula clásica** $S = \\pi r \\ell$ con $r = h$ (radio) y $\\ell = h\\sqrt{2}$ (generatriz): $\\pi \\cdot h \\cdot h\\sqrt{2} = \\pi h^2 \\sqrt{2}$. ✓",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El factor $2\\pi f(x)$ en la fórmula de superficie corresponde a:",
                  "opciones_md": [
                      "El área del círculo en cada $x$.",
                      "La circunferencia del anillo generado al girar.",
                      "El volumen infinitesimal.",
                      "La derivada del área.",
                  ],
                  "correcta": "B",
                  "pista_md": "Al girar el punto $(x, f(x))$ alrededor del eje $x$, traza un círculo de radio $f(x)$.",
                  "explicacion_md": (
                      "El punto $(x, f(x))$ traza una circunferencia de longitud $2\\pi f(x)$. Multiplicada por el ancho infinitesimal $ds$ da el área de la banda anular."
                  ),
              },
              {
                  "enunciado_md": "Comparado con el volumen $V = \\pi \\int [f(x)]^2 \\, dx$, la superficie tiene:",
                  "opciones_md": [
                      "Menos factores.",
                      "$2\\pi$ en vez de $\\pi$, $f(x)$ en vez de $f(x)^2$, y un factor $\\sqrt{1 + (f')^2}$.",
                      "Lo mismo.",
                      "Otra integral distinta.",
                  ],
                  "correcta": "B",
                  "pista_md": "Volumen ↔ disco macizo (área del círculo). Superficie ↔ borde del disco (circunferencia × ancho de arco).",
                  "explicacion_md": (
                      "Volumen: cada rodaja es un círculo macizo (área $\\pi f^2$). Superficie: cada banda es un anillo cónico (longitud $2\\pi f$ × ancho $ds$, donde $ds$ tiene la raíz)."
                  ),
              },
          ]),

        ej(
            titulo="Aplicar la fórmula",
            enunciado=(
                "Calcula el área de la superficie generada al girar $y = \\sqrt{x}$ en $[0, 4]$ "
                "alrededor del eje $x$."
            ),
            pistas=[
                "$f(x) = x^{1/2}$, $f'(x) = \\dfrac{1}{2\\sqrt{x}}$, $[f']^2 = \\dfrac{1}{4x}$.",
                "$1 + [f']^2 = \\dfrac{4x + 1}{4x}$. La raíz: $\\dfrac{\\sqrt{4x+1}}{2\\sqrt{x}}$.",
                "Integrando: $\\sqrt{x} \\cdot \\dfrac{\\sqrt{4x+1}}{2\\sqrt{x}} = \\dfrac{\\sqrt{4x+1}}{2}$.",
                "Sustituye $u = 4x + 1$.",
            ],
            solucion=(
                "$$S = 2\\pi \\int_0^4 \\dfrac{\\sqrt{4x+1}}{2} \\, dx = \\pi \\int_0^4 \\sqrt{4x+1} \\, dx$$\n\n"
                "Sustitución $u = 4x + 1$, $du = 4 \\, dx$, límites $u(0) = 1$, $u(4) = 17$:\n\n"
                "$$\\pi \\cdot \\dfrac{1}{4} \\int_1^{17} u^{1/2} \\, du = \\dfrac{\\pi}{4} \\cdot \\dfrac{2}{3} [u^{3/2}]_1^{17} = \\dfrac{\\pi}{6}(17^{3/2} - 1)$$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir superficie con volumen.** Volumen lleva $f^2$ y $\\pi$; superficie lleva $f$ y $2\\pi$, **además de la raíz** $\\sqrt{1 + (f')^2}$.",
              "**Olvidar el factor $\\sqrt{1 + (f')^2}$.** Sin él la fórmula da el área lateral de un cilindro, no de una superficie curva.",
              "**Confundir 'distancia al eje' con $f(x)$ siempre.** Si el eje no es el $x$, la distancia es $|f(x) - c|$.",
              "**Olvidar que $f$ debe ser no negativa** (o tomar valor absoluto): la circunferencia $2\\pi f$ requiere $f \\geq 0$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Fórmula:** $S = 2\\pi \\int (\\text{distancia al eje}) \\sqrt{1 + (f')^2} \\, dx$.",
              "**Eje $x$:** $S = 2\\pi \\int f(x) \\sqrt{1 + (f')^2} \\, dx$.",
              "**Eje $y$:** $S = 2\\pi \\int g(y) \\sqrt{1 + (g')^2} \\, dy$ (curva $x = g(y)$).",
              "**Confirmaciones clásicas:** esfera $4\\pi r^2$, cono $\\pi r \\ell$.",
              "**Próxima lección:** aplicaciones físicas — trabajo, centro de masa, presión.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-6-superficies",
        "title": "Áreas de superficies de revolución",
        "description": "Áreas de superficies generadas al girar curvas alrededor de ejes.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 6,
    }


# =====================================================================
# 3.7 Aplicaciones en física
# =====================================================================
def lesson_3_7():
    blocks = [
        b("texto", body_md=(
            "Las integrales aparecen en física cada vez que algo varía continuamente. "
            "Tres aplicaciones clásicas: el **trabajo** realizado por una fuerza variable, "
            "el **centro de masa** de un cuerpo con densidad variable y la **presión hidrostática**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Plantear $W = \\int_a^b F(x) \\, dx$ para trabajo de una fuerza variable.\n"
            "- Aplicar la ley de Hooke al estiramiento de un resorte.\n"
            "- Calcular el trabajo de bombear líquido.\n"
            "- Calcular el centro de masa de una varilla con densidad variable."
        )),

        b("definicion",
          titulo="Trabajo de una fuerza variable",
          body_md=(
              "Si una fuerza $F(x)$ (en newtons) se aplica a un objeto a lo largo del eje $x$ entre las "
              "posiciones $a$ y $b$ (en metros), el **trabajo** realizado es:\n\n"
              "$$W = \\int_a^b F(x) \\, dx \\quad (\\text{en julios})$$\n\n"
              "**Unidades:** $1 \\text{ J} = 1 \\text{ N} \\cdot \\text{m}$.\n\n"
              "**Caso especial $F$ constante:** $W = F \\cdot (b - a)$, la fórmula de física básica."
          )),

        b("ejemplo_resuelto",
          titulo="Ley de Hooke: estirar un resorte",
          problema_md=(
              "Un resorte tiene constante $k = 200$ N/m. Calcular el trabajo necesario para estirarlo "
              "$0.1$ m desde su longitud natural."
          ),
          pasos=[
              {"accion_md": "**Ley de Hooke:** $F(x) = kx$ con $x$ = elongación. Aquí $F(x) = 200x$ N.",
               "justificacion_md": "La fuerza es proporcional al estiramiento.",
               "es_resultado": False},
              {"accion_md": "$$W = \\int_0^{0.1} 200 x \\, dx = 200 \\cdot \\dfrac{x^2}{2}\\Big|_0^{0.1} = 100 \\cdot 0.01 = 1 \\text{ J}$$",
               "justificacion_md": "**Lección:** $W = \\dfrac{1}{2}kx^2$ es la \"energía potencial elástica\" almacenada — fórmula clásica del resorte.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Trabajo de bombear agua",
          problema_md=(
              "Un tanque cilíndrico de radio $2$ m y altura $5$ m está lleno de agua. ¿Cuánto trabajo "
              "se necesita para bombear toda el agua hasta el borde superior? (Densidad del agua: "
              "$\\rho = 1000$ kg/m³, $g = 9.8$ m/s².)"
          ),
          pasos=[
              {"accion_md": "**Cortar el agua en capas horizontales** de espesor $dy$ a altura $y$ medida desde el fondo.\n\n"
                            "**Volumen de la capa:** $dV = \\pi r^2 \\, dy = 4\\pi \\, dy$ m³.\n"
                            "**Masa:** $dm = \\rho \\, dV = 4000\\pi \\, dy$ kg.\n"
                            "**Peso (fuerza):** $dF = g \\, dm = 4000 \\pi g \\, dy = 39\\,200\\pi \\, dy$ N.",
               "justificacion_md": "Cada capa se trata como un disco que pesa $dF$.",
               "es_resultado": False},
              {"accion_md": "**Distancia que recorre la capa:** desde altura $y$ hasta $5$ m, es decir, $5 - y$.\n\n"
                            "**Trabajo de bombear esa capa:** $dW = (5 - y) \\, dF = 39\\,200\\pi (5 - y) \\, dy$.",
               "justificacion_md": "Trabajo = fuerza × distancia. La distancia depende de la altura inicial de la capa.",
               "es_resultado": False},
              {"accion_md": "**Integrar de $0$ a $5$:**\n\n$$W = 39\\,200\\pi \\int_0^5 (5 - y) \\, dy = 39\\,200\\pi \\cdot \\dfrac{25}{2} = 490\\,000 \\pi \\approx 1.54 \\times 10^6 \\text{ J}$$",
               "justificacion_md": "**Patrón:** trabajo de bombeo = $\\int (\\text{peso de la capa}) \\times (\\text{distancia)}$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Centro de masa de una varilla",
          body_md=(
              "Si una varilla ocupa $[a, b]$ con densidad lineal $\\rho(x)$ (masa por unidad de longitud), su:\n\n"
              "**Masa total:** $M = \\int_a^b \\rho(x) \\, dx$.\n\n"
              "**Momento respecto al origen:** $M_0 = \\int_a^b x \\rho(x) \\, dx$.\n\n"
              "**Centro de masa:**\n\n"
              "$$\\bar{x} = \\dfrac{M_0}{M} = \\dfrac{\\int_a^b x \\rho(x) \\, dx}{\\int_a^b \\rho(x) \\, dx}$$\n\n"
              "**Caso uniforme** ($\\rho$ constante): $\\bar{x} = (a + b)/2$ (centro geométrico)."
          )),

        b("ejemplo_resuelto",
          titulo="Centro de masa con densidad lineal",
          problema_md=(
              "Una varilla en $[0, 2]$ tiene densidad $\\rho(x) = 3 + x$ kg/m. Calcular su centro de masa."
          ),
          pasos=[
              {"accion_md": "**Masa total:**\n\n$$M = \\int_0^2 (3 + x) \\, dx = \\left[3x + \\dfrac{x^2}{2}\\right]_0^2 = 6 + 2 = 8 \\text{ kg}$$",
               "justificacion_md": "Antiderivada simple.",
               "es_resultado": False},
              {"accion_md": "**Momento:**\n\n$$M_0 = \\int_0^2 x(3 + x) \\, dx = \\int_0^2 (3x + x^2) \\, dx = \\dfrac{3x^2}{2} + \\dfrac{x^3}{3}\\Big|_0^2 = 6 + \\dfrac{8}{3} = \\dfrac{26}{3}$$",
               "justificacion_md": "Multiplicamos por $x$ adentro de la integral.",
               "es_resultado": False},
              {"accion_md": "**Centro de masa:**\n\n$$\\bar{x} = \\dfrac{26/3}{8} = \\dfrac{26}{24} = \\dfrac{13}{12} \\approx 1.083$$",
               "justificacion_md": "**Verificación cualitativa:** la densidad es mayor cerca de $x = 2$, así el centro de masa debe estar a la derecha del centro geométrico ($x = 1$). $1.083 > 1$. ✓",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para un resorte con constante $k$, el trabajo de estirarlo de $x = 0$ a $x = a$ es:",
                  "opciones_md": [
                      "$ka$",
                      "$\\dfrac{1}{2} k a^2$",
                      "$\\dfrac{1}{3} k a^3$",
                      "$k a^2$",
                  ],
                  "correcta": "B",
                  "pista_md": "$F(x) = kx$, así $W = \\int_0^a kx \\, dx$.",
                  "explicacion_md": (
                      "$W = \\int_0^a kx \\, dx = k \\cdot a^2/2 = \\dfrac{1}{2} k a^2$. **Es la energía potencial elástica.**"
                  ),
              },
              {
                  "enunciado_md": "Si una varilla en $[0, L]$ tiene densidad **constante** $\\rho_0$, su centro de masa es:",
                  "opciones_md": ["$0$", "$L$", "$L/2$", "$\\rho_0 L / 2$"],
                  "correcta": "C",
                  "pista_md": "Densidad uniforme → centro de masa = centro geométrico.",
                  "explicacion_md": (
                      "$\\bar{x} = \\dfrac{\\int_0^L x \\rho_0 \\, dx}{\\int_0^L \\rho_0 \\, dx} = \\dfrac{\\rho_0 L^2/2}{\\rho_0 L} = L/2$. Sin densidad variable, el centro de masa es el medio del intervalo."
                  ),
              },
          ]),

        ej(
            titulo="Trabajo con fuerza cuadrática",
            enunciado=(
                "Una fuerza variable $F(x) = x^2 + 2x$ N actúa sobre un objeto que se mueve de "
                "$x = 0$ a $x = 3$ m. Calcula el trabajo total."
            ),
            pistas=[
                "$W = \\int_0^3 (x^2 + 2x) \\, dx$.",
                "Antiderivada: $x^3/3 + x^2$.",
            ],
            solucion=(
                "$$W = \\int_0^3 (x^2 + 2x) \\, dx = \\left[\\dfrac{x^3}{3} + x^2\\right]_0^3 = 9 + 9 = 18 \\text{ J}$$"
            ),
        ),

        fig(
            "Lámina con tres paneles físicos lado a lado. Panel (a): resorte horizontal estirado con fórmula W = ∫ F(x) dx, con flecha de fuerza en teal #06b6d4 y desplazamiento marcado en ámbar #f59e0b. Panel (b): placa plana con eje x debajo y fórmula del centro de masa x̄ = (1/M) ∫ x ρ(x) dA, con un punto teal marcando x̄. Panel (c): pared vertical inundada con líquido azulado, mostrando presión hidrostática creciente con la profundidad y flechas ámbar perpendiculares a la pared."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir fuerza con trabajo.** $F$ tiene unidades N; $W$ tiene unidades $\\text{N} \\cdot \\text{m} = \\text{J}$.",
              "**No considerar la distancia variable** en problemas de bombeo. Cada capa se levanta una distancia distinta.",
              "**Olvidar la densidad** del fluido en $dF = \\rho g \\, dV$.",
              "**Centro de masa: dividir por longitud en vez de masa.** Si la densidad varía, $\\bar{x} = M_0 / M$, no $M_0 / (b - a)$.",
              "**Confundir signo** del trabajo: si la fuerza apunta opuesta al movimiento, el trabajo es negativo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Trabajo:** $W = \\int_a^b F(x) \\, dx$.",
              "**Resorte (Hooke):** $F = kx$, $W = \\dfrac{1}{2}kx^2$.",
              "**Bombeo:** $W = \\int (\\text{peso capa})(\\text{distancia})$.",
              "**Centro de masa:** $\\bar{x} = \\dfrac{\\int x \\rho \\, dx}{\\int \\rho \\, dx}$.",
              "**Densidad uniforme:** centro de masa = centro geométrico.",
              "**Próxima lección:** aplicaciones en economía — excedente del consumidor, costo total desde costo marginal.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-7-fisica",
        "title": "Aplicaciones en física",
        "description": "Trabajo de fuerzas variables, ley de Hooke, bombeo de líquidos y centro de masa.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 7,
    }


# =====================================================================
# 3.8 Aplicaciones en economía
# =====================================================================
def lesson_3_8():
    blocks = [
        b("texto", body_md=(
            "Las integrales miden cantidades acumuladas — exactamente lo que se necesita en economía cuando "
            "se conoce una **tasa marginal** y se quiere el total. Tres aplicaciones clave: "
            "**costo total desde costo marginal**, **excedente del consumidor** y **excedente del productor**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Recuperar costo (o ingreso) total desde su tasa marginal.\n"
            "- Calcular el excedente del consumidor y del productor.\n"
            "- Interpretar geométricamente cada cantidad."
        )),

        b("definicion",
          titulo="Costo total desde costo marginal",
          body_md=(
              "Si $C(q)$ es el costo de producir $q$ unidades y $MC(q) = C'(q)$ es el **costo marginal**, "
              "entonces por el TFC:\n\n"
              "$$C(q) = C(0) + \\int_0^q MC(t) \\, dt$$\n\n"
              "donde $C(0)$ es el **costo fijo**. Análogo para ingreso ($MR$ → $R$) y beneficio.\n\n"
              "**Cambio total entre $q_1$ y $q_2$:**\n\n"
              "$$C(q_2) - C(q_1) = \\int_{q_1}^{q_2} MC(t) \\, dt$$"
          )),

        b("ejemplo_resuelto",
          titulo="Costo total desde marginal",
          problema_md=(
              "Una fábrica tiene costo marginal $MC(q) = 0.02q + 5$ (en USD por unidad). El costo "
              "fijo es $C(0) = 1000$ USD. Calcular el costo total de producir $200$ unidades."
          ),
          pasos=[
              {"accion_md": "$$C(200) = 1000 + \\int_0^{200} (0.02 t + 5) \\, dt$$",
               "justificacion_md": "TFC sobre el costo marginal.",
               "es_resultado": False},
              {"accion_md": "$$\\int_0^{200}(0.02t + 5) \\, dt = \\left[0.01 t^2 + 5t\\right]_0^{200} = 400 + 1000 = 1400$$",
               "justificacion_md": "Antiderivada y evaluación.",
               "es_resultado": False},
              {"accion_md": "$C(200) = 1000 + 1400 = 2400$ USD.",
               "justificacion_md": "**Costo total** = costo fijo + costo variable acumulado.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Excedente del consumidor",
          body_md=(
              "Sea $p = D(q)$ la **función de demanda** (precio que el mercado está dispuesto a pagar para "
              "una cantidad $q$). Si el precio de equilibrio es $p^*$ y la cantidad de equilibrio es $q^*$:\n\n"
              "$$\\text{EC} = \\int_0^{q^*} D(q) \\, dq - p^* q^*$$\n\n"
              "**Interpretación:** los consumidores estarían dispuestos a pagar $\\int_0^{q^*} D \\, dq$ en total, "
              "pero solo pagan $p^* q^*$. La diferencia es su **beneficio neto agregado**."
          )),

        fig(
            "Diagrama económico de oferta y demanda. Eje x: cantidad q. Eje y: precio p. Una curva de "
            "demanda D(q) decreciente (en color azul) y una curva de oferta S(q) creciente (en color "
            "rojo). Su intersección marca el punto de equilibrio (q*, p*) destacado. Sombrear en "
            "ámbar la región entre la curva de demanda y la línea horizontal y = p* (de q=0 a q=q*) — "
            "**excedente del consumidor**. Sombrear en teal la región entre la línea y = p* y la "
            "curva de oferta (mismo intervalo) — **excedente del productor**. Etiquetas claras: "
            "'Demanda D(q)', 'Oferta S(q)', 'p*', 'q*', 'EC' (en la zona del consumidor), 'EP' (en "
            "la del productor). " + STYLE
        ),

        b("definicion",
          titulo="Excedente del productor",
          body_md=(
              "Análogo, con la **función de oferta** $p = S(q)$:\n\n"
              "$$\\text{EP} = p^* q^* - \\int_0^{q^*} S(q) \\, dq$$\n\n"
              "**Interpretación:** los productores reciben $p^* q^*$ pero estarían dispuestos a vender por "
              "$\\int_0^{q^*} S \\, dq$ (su costo agregado). La diferencia es su ganancia neta."
          )),

        b("ejemplo_resuelto",
          titulo="Excedente del consumidor con demanda lineal",
          problema_md=(
              "La demanda es $D(q) = 100 - 2q$ (USD por unidad) y el precio de equilibrio es $p^* = 40$ "
              "USD. Calcular el excedente del consumidor."
          ),
          pasos=[
              {"accion_md": "**Cantidad de equilibrio:** $D(q^*) = 40 \\implies 100 - 2q^* = 40 \\implies q^* = 30$.",
               "justificacion_md": "Despejamos $q$ a partir del precio de equilibrio.",
               "es_resultado": False},
              {"accion_md": "**Excedente del consumidor:**\n\n$$\\text{EC} = \\int_0^{30}(100 - 2q) \\, dq - 40 \\cdot 30$$\n\n"
                            "$\\int_0^{30}(100 - 2q) \\, dq = [100q - q^2]_0^{30} = 3000 - 900 = 2100$.\n\n"
                            "$\\text{EC} = 2100 - 1200 = 900$ USD.",
               "justificacion_md": "Cálculo directo. **Geométricamente:** es el área de un triángulo con base $30$ y altura $100 - 40 = 60$, así $30 \\cdot 60 / 2 = 900$. ✓",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "Si conoces $MC(q)$ y $C(0)$, ¿cómo calculas $C(q)$?",
                  "opciones_md": [
                      "$C(q) = MC(q) \\cdot q$",
                      "$C(q) = C(0) + \\int_0^q MC(t) \\, dt$",
                      "$C(q) = MC(q) - C(0)$",
                      "$C(q) = MC(q) / q$",
                  ],
                  "correcta": "B",
                  "pista_md": "$C$ es la antiderivada de $MC$, ajustada con la condición inicial.",
                  "explicacion_md": (
                      "$MC = C'$, así $C(q) = C(0) + \\int_0^q MC$. Es el TFC parte 2 con condición inicial."
                  ),
              },
              {
                  "enunciado_md": "El excedente del consumidor representa:",
                  "opciones_md": [
                      "El precio que paga.",
                      "La diferencia entre lo que estaría dispuesto a pagar y lo que efectivamente paga.",
                      "El beneficio del productor.",
                      "El costo total del bien.",
                  ],
                  "correcta": "B",
                  "pista_md": "Mide cuánto 'gana' el consumidor pagando menos de lo que estaría dispuesto.",
                  "explicacion_md": (
                      "El consumidor estaría dispuesto a pagar $\\int_0^{q^*} D \\, dq$ (área bajo la demanda). Solo paga $p^* q^*$. La diferencia (un triángulo en la oferta-demanda) es su excedente."
                  ),
              },
          ]),

        ej(
            titulo="Cambio total de costo",
            enunciado=(
                "Costo marginal $MC(q) = 0.5q + 10$. ¿Cuánto aumenta el costo total al pasar la "
                "producción de $50$ a $100$ unidades?"
            ),
            pistas=[
                "El cambio total es $\\int_{50}^{100} MC(q) \\, dq$, sin necesitar el costo fijo.",
                "Antiderivada: $0.25 q^2 + 10q$.",
            ],
            solucion=(
                "$$C(100) - C(50) = \\int_{50}^{100}(0.5q + 10) \\, dq = [0.25q^2 + 10q]_{50}^{100}$$\n\n"
                "$= (2500 + 1000) - (625 + 500) = 3500 - 1125 = 2375$ USD."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el costo fijo $C(0)$** al recuperar el costo total. Sin él se obtiene solo el costo variable.",
              "**Confundir $D$ con $S$** al calcular excedentes. Demanda decrece; oferta crece.",
              "**Restar al revés:** EC = $\\int D - p^* q^*$, EP = $p^* q^* - \\int S$. Si los inviertes, el signo sale al revés.",
              "**Aplicar EC con un precio que no es el de equilibrio.** El cálculo asume mercado en equilibrio.",
          ]),

        b("resumen",
          puntos_md=[
              "**Costo total desde marginal:** $C(q) = C(0) + \\int_0^q MC(t) \\, dt$.",
              "**Excedente del consumidor:** $\\int_0^{q^*} D - p^* q^*$ (área entre demanda y línea horizontal).",
              "**Excedente del productor:** $p^* q^* - \\int_0^{q^*} S$ (área entre línea horizontal y oferta).",
              "**Análogos** para ingreso, beneficio, ganancia, etc.",
              "**Próxima lección:** aplicaciones en biología — crecimiento poblacional, flujo sanguíneo.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-8-economia",
        "title": "Aplicaciones en economía",
        "description": "Recuperar totales desde tasas marginales, excedente del consumidor y del productor.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 8,
    }


# =====================================================================
# 3.9 Aplicaciones en biología
# =====================================================================
def lesson_3_9():
    blocks = [
        b("texto", body_md=(
            "Las integrales en biología modelan **acumulación**: cuántos individuos nacen en un período, "
            "cuánta sangre fluye por una arteria, cuánto medicamento se distribuye en el cuerpo. "
            "Esta lección reúne tres aplicaciones representativas.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular **crecimiento poblacional acumulado** desde una tasa de cambio.\n"
            "- Aplicar la **ley de Poiseuille** para flujo sanguíneo.\n"
            "- Calcular **dosis acumulada** de un medicamento."
        )),

        b("definicion",
          titulo="Crecimiento poblacional acumulado",
          body_md=(
              "Si $r(t)$ es la **tasa de crecimiento** poblacional (individuos por unidad de tiempo), "
              "el cambio acumulado entre $t_1$ y $t_2$ es:\n\n"
              "$$P(t_2) - P(t_1) = \\int_{t_1}^{t_2} r(t) \\, dt$$\n\n"
              "**Variación neta** considerando nacimientos $b(t)$ y muertes $d(t)$:\n\n"
              "$$\\Delta P = \\int_{t_1}^{t_2} [b(t) - d(t)] \\, dt$$\n\n"
              "**Caso clásico — crecimiento exponencial:** $r(t) = k P(t)$ → la solución $P(t) = P_0 e^{kt}$ "
              "se obtiene por separación de variables (lo veremos en cálculo de varias variables o ED)."
          )),

        b("ejemplo_resuelto",
          titulo="Crecimiento de bacterias",
          problema_md=(
              "Un cultivo de bacterias crece a una tasa $r(t) = 1000 e^{0.1 t}$ bacterias por hora. "
              "¿Cuántas bacterias se generaron entre $t = 0$ y $t = 5$ h?"
          ),
          pasos=[
              {"accion_md": "$$\\Delta P = \\int_0^5 1000 e^{0.1 t} \\, dt$$",
               "justificacion_md": "Integramos la tasa.",
               "es_resultado": False},
              {"accion_md": "**Antiderivada** (con sustitución $u = 0.1 t$, o directamente):\n\n"
                            "$$\\int 1000 e^{0.1t} \\, dt = \\dfrac{1000}{0.1} e^{0.1 t} = 10\\,000 \\, e^{0.1 t}$$",
               "justificacion_md": "$\\int e^{kt} dt = e^{kt}/k$.",
               "es_resultado": False},
              {"accion_md": "**Evaluamos:**\n\n$$\\Delta P = 10\\,000 [e^{0.5} - e^0] = 10\\,000 (1.6487 - 1) \\approx 6487 \\text{ bacterias}$$",
               "justificacion_md": "**Interpretación:** la tasa exponencial acumula crecimiento que no es lineal.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Ley de Poiseuille — flujo sanguíneo",
          body_md=(
              "En una arteria de radio $R$, la velocidad del flujo a una distancia $r$ del centro es:\n\n"
              "$$v(r) = \\dfrac{P}{4 \\eta L}(R^2 - r^2)$$\n\n"
              "donde $P$ es la diferencia de presión, $\\eta$ es la viscosidad de la sangre y $L$ la longitud "
              "del tramo. **El flujo total** (volumen por unidad de tiempo) se obtiene integrando la "
              "velocidad sobre la sección transversal:\n\n"
              "$$F = \\int_0^R v(r) \\cdot 2\\pi r \\, dr = \\dfrac{\\pi P R^4}{8 \\eta L}$$\n\n"
              "**Lección clave:** $F$ depende de $R^4$ — un pequeño cambio en el radio (por ejemplo, "
              "constricción del 10 %) altera el flujo dramáticamente."
          )),

        b("ejemplo_resuelto",
          titulo="Flujo total con Poiseuille",
          problema_md=(
              "Para una arteria con $R = 0.008$ cm, $L = 2$ cm, $P = 4000$ dinas/cm², "
              "$\\eta = 0.027$ poise, calcular el flujo $F$."
          ),
          pasos=[
              {"accion_md": "**Aplicar la fórmula:**\n\n$$F = \\dfrac{\\pi P R^4}{8 \\eta L}$$",
               "justificacion_md": "Resultado de integrar la velocidad sobre la sección transversal.",
               "es_resultado": False},
              {"accion_md": "**Sustituyendo:**\n\n$$F = \\dfrac{\\pi \\cdot 4000 \\cdot (0.008)^4}{8 \\cdot 0.027 \\cdot 2} = \\dfrac{\\pi \\cdot 4000 \\cdot 4.096 \\times 10^{-9}}{0.432}$$\n\n"
                            "$$\\approx \\dfrac{5.15 \\times 10^{-5}}{0.432} \\approx 1.19 \\times 10^{-4} \\text{ cm}^3/\\text{s}$$",
               "justificacion_md": "Cálculo numérico. **Sensibilidad a $R$:** si $R$ baja un 10 % a $0.0072$, el flujo cae en $(0.9)^4 \\approx 0.66$, es decir, **34 % menos** flujo.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Dosis acumulada de un medicamento",
          body_md=(
              "Si un medicamento se administra a una **tasa** $r(t)$ (mg/h), la **dosis total acumulada** "
              "en un período $[t_1, t_2]$ es:\n\n"
              "$$D = \\int_{t_1}^{t_2} r(t) \\, dt$$\n\n"
              "Si la concentración en sangre $C(t)$ decae con el tiempo (eliminación renal/hepática), "
              "típicamente $C(t) = C_0 e^{-kt}$, y la **exposición total** (área bajo la curva, AUC) es:\n\n"
              "$$\\text{AUC} = \\int_0^\\infty C(t) \\, dt = \\dfrac{C_0}{k}$$\n\n"
              "**AUC** es un parámetro fundamental en farmacocinética para evaluar la biodisponibilidad."
          )),

        b("ejemplo_resuelto",
          titulo="AUC de un medicamento",
          problema_md=(
              "La concentración plasmática de una droga es $C(t) = 5 e^{-0.2 t}$ mg/L (con $t$ en horas). "
              "Calcular la AUC total."
          ),
          pasos=[
              {"accion_md": "$$\\text{AUC} = \\int_0^\\infty 5 e^{-0.2 t} \\, dt$$",
               "justificacion_md": "Integral impropia tipo 1.",
               "es_resultado": False},
              {"accion_md": "$$= \\lim_{T \\to \\infty} \\int_0^T 5 e^{-0.2 t} \\, dt = \\lim_{T \\to \\infty} \\left[\\dfrac{5}{-0.2} e^{-0.2 t}\\right]_0^T = -25 (0 - 1) = 25 \\text{ mg} \\cdot \\text{h} / \\text{L}$$",
               "justificacion_md": "$e^{-0.2T} \\to 0$ cuando $T \\to \\infty$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si la tasa de crecimiento de una población es $r(t) = 100$ individuos/h (constante), ¿cuántos individuos se acumulan en $24$ horas?",
                  "opciones_md": ["$100$", "$1200$", "$2400$", "$\\int 100 e^t$"],
                  "correcta": "C",
                  "pista_md": "Tasa constante → simplemente $r \\cdot t$.",
                  "explicacion_md": (
                      "$\\Delta P = \\int_0^{24} 100 \\, dt = 100 \\cdot 24 = 2400$. **Trampa:** $1200$ es la mitad — sería el correcto solo si la tasa fuera $50$/h."
                  ),
              },
              {
                  "enunciado_md": "Según la ley de Poiseuille, si el radio de una arteria se reduce a la mitad, el flujo se reduce a:",
                  "opciones_md": [
                      "La mitad.",
                      "Un cuarto.",
                      "Un dieciseisavo ($1/16$).",
                      "No cambia.",
                  ],
                  "correcta": "C",
                  "pista_md": "$F \\propto R^4$. ¿Cuánto es $(1/2)^4$?",
                  "explicacion_md": (
                      "$F \\propto R^4$, así $(1/2)^4 = 1/16$. Por eso pequeñas reducciones del radio (placas de colesterol) tienen efectos enormes sobre el flujo."
                  ),
              },
          ]),

        ej(
            titulo="Población con tasa variable",
            enunciado=(
                "La tasa de natalidad en una colonia es $r(t) = 50 + 10t$ individuos por año. "
                "¿Cuántos individuos nacen entre los años $0$ y $5$?"
            ),
            pistas=[
                "$\\Delta P = \\int_0^5 (50 + 10t) \\, dt$.",
                "Antiderivada: $50t + 5t^2$.",
            ],
            solucion=(
                "$$\\Delta P = \\int_0^5 (50 + 10t) \\, dt = [50t + 5t^2]_0^5 = 250 + 125 = 375$$\n\n"
                "**$375$ individuos nuevos** en 5 años."
            ),
        ),

        fig(
            "Dos paneles con ejes cartesianos. Panel (a) titulado 'Crecimiento logístico': curva en forma de S en teal #06b6d4 que parte cerca del eje x, asciende, pasa por un punto de inflexión marcado con un círculo ámbar #f59e0b, y se aplana acercándose a una asíntota horizontal punteada ámbar etiquetada K (capacidad de carga). Eje x = tiempo, eje y = población. Panel (b) titulado 'Distribución de tamaños': curva campana simétrica en gris con área bajo la curva sombreada en teal #06b6d4 entre dos límites verticales a y b; etiqueta P(a < X < b)."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir tasa con población.** La tasa $r(t)$ tiene unidades de individuos/tiempo; la población es individuos.",
              "**Olvidar las muertes** al calcular cambio neto. Si solo integras nacimientos, sobrestimas el crecimiento.",
              "**Aplicar Poiseuille con unidades inconsistentes.** Pasar todo a un mismo sistema (CGS o SI) antes de calcular.",
              "**No reconocer AUC como integral impropia** cuando la concentración decae a cero. Hay que tomar límite a $\\infty$.",
              "**Confundir 'dosis' con 'concentración'.** Dosis es masa total administrada; concentración es masa/volumen.",
          ]),

        b("resumen",
          puntos_md=[
              "**Tasa → cantidad acumulada:** $\\Delta P = \\int_a^b r(t) \\, dt$.",
              "**Crecimiento exponencial:** $P(t) = P_0 e^{kt}$ — viene de $dP/dt = kP$ (lo formaliza ED).",
              "**Poiseuille:** $F = \\pi P R^4 / (8 \\eta L)$ — flujo proporcional a $R^4$.",
              "**AUC** (área bajo la curva): exposición total a un medicamento, integral impropia tipo 1.",
              "**Cierre del curso:** todas las técnicas (sustitución, partes, parciales, impropias) confluyen en problemas aplicados a física, economía y biología.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-int-3-9-biologia",
        "title": "Aplicaciones en biología",
        "description": "Crecimiento poblacional acumulado, ley de Poiseuille y dosis de medicamentos (AUC).",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 9,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "calculo-integral"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Course {course_id} not found. Corre primero seed_calculo_integral_chapter_1.py")

    chapter_id = "ch-aplicaciones-integral"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Aplicaciones de la Integral",
        "description": "Áreas, volúmenes (discos, anillos, cascarones), valor promedio, longitud de arco, superficies, y aplicaciones en física, economía y biología.",
        "order": 3,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_3_1, lesson_3_2, lesson_3_3, lesson_3_4, lesson_3_5,
        lesson_3_6, lesson_3_7, lesson_3_8, lesson_3_9,
    ]
    total_blocks = 0
    total_figures = 0
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
        total_figures += sum(1 for blk in data["blocks"] if blk.get("type") == "figura")
        print(f"  ✓ {data['title']} ({len(data['blocks'])} bloques, ~{data['duration_minutes']} min)")

    print()
    print(f"✅ Capítulo 3 — Aplicaciones de la Integral listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figures} figuras pendientes.")
    print()
    print("Lecciones disponibles en:")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
