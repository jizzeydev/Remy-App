"""
Seed del Capítulo 3 — Aplicaciones de las Derivadas (curso Cálculo Diferencial).
7 lecciones que cubren todo el contenido de las guías oficiales:
  3.1 Razones relacionadas
  3.2 Aproximaciones lineales y diferenciales
  3.3 Máximos y mínimos
  3.4 Teorema del Valor Medio
  3.5 Forma de la gráfica
  3.6 Graficar curvas
  3.7 Optimización

Idempotente: borra y re-inserta el capítulo y sus 7 lecciones.
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


def now():
    return datetime.now(timezone.utc).isoformat()


# ============ helpers para ejercicios y figuras ============
STYLE = (
    "Estilo: diagrama educativo limpio, fondo blanco, lineas claras, etiquetas "
    "en espanol, notacion matematica renderizada con buena tipografia. Acentos "
    "de color suaves (teal #06b6d4 y ambar #f59e0b). Sin sombras dramaticas, "
    "sin texturas. Apto para libro universitario."
)


def ej(titulo, enunciado, pistas, solucion):
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def fig(prompt):
    return b("figura", image_url="", caption_md="", prompt_image_md=prompt)


# =====================================================================
# LECCIÓN 3.1 — Razones relacionadas
# =====================================================================
def lesson_3_1():
    blocks = [
        b("texto", body_md=(
            "En muchos problemas de la vida real, **dos o más cantidades cambian con el tiempo y están relacionadas por una ecuación**. "
            "Si conocemos la velocidad de cambio de una de ellas, podemos calcular la de las otras. "
            "Esta clase de problemas se llama **razones relacionadas**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Identificar cuándo un problema es de razones relacionadas.\n"
            "- Plantear una **ecuación de relación** entre las cantidades involucradas.\n"
            "- Derivar implícitamente respecto al **tiempo $t$**.\n"
            "- Sustituir los valores numéricos al final, no al principio."
        )),

        b("intuicion",
          titulo="La estrategia de 5 pasos",
          body_md=(
              "Casi todo problema de razones relacionadas se resuelve igual:\n\n"
              "1. **Dibujar un esquema** y nombrar las variables (todas funciones de $t$).\n"
              "2. **Anotar lo que se sabe y lo que se busca** (las razones de cambio: derivadas respecto a $t$).\n"
              "3. **Escribir la ecuación que relaciona** las variables (geometría, trigonometría, etc.).\n"
              "4. **Derivar implícitamente respecto a $t$** la ecuación.\n"
              "5. **Sustituir** los valores conocidos en el instante específico y despejar lo desconocido.\n\n"
              "**Regla de oro:** sustituir los valores numéricos **al final**, después de derivar — nunca antes."
          )),

        b("ejemplo_resuelto",
          titulo="Globo que se infla",
          problema_md="Un globo esférico se infla a $\\dfrac{dV}{dt} = 100 \\text{ cm}^3/\\text{s}$. ¿Qué tan rápido aumenta el radio cuando $r = 25$ cm?",
          pasos=[
              {"accion_md": "**Esquema y variables.** Sea $r(t)$ el radio y $V(t)$ el volumen, ambos funciones del tiempo.\n\n**Datos:** $\\dfrac{dV}{dt} = 100$. **Buscamos:** $\\dfrac{dr}{dt}$ cuando $r = 25$.",
               "justificacion_md": "Identificamos qué cambia y qué buscamos antes de plantear la ecuación.",
               "es_resultado": False},
              {"accion_md": "**Ecuación de relación:** $V = \\dfrac{4}{3}\\pi r^3$.",
               "justificacion_md": "Es la fórmula del volumen de una esfera.",
               "es_resultado": False},
              {"accion_md": "**Derivamos respecto a $t$** (ambos lados):\n\n$$\\dfrac{dV}{dt} = 4\\pi r^2 \\cdot \\dfrac{dr}{dt}$$",
               "justificacion_md": "Por la regla de la cadena: $r$ es función de $t$, así $(r^3)' = 3r^2 \\cdot r'(t)$.",
               "es_resultado": False},
              {"accion_md": "**Sustituimos** $\\dfrac{dV}{dt} = 100$ y $r = 25$:\n\n$$100 = 4\\pi (25)^2 \\cdot \\dfrac{dr}{dt} = 2500\\pi \\cdot \\dfrac{dr}{dt}$$",
               "justificacion_md": "Recién ahora pasamos los valores numéricos.",
               "es_resultado": False},
              {"accion_md": "**Despejamos:** $\\dfrac{dr}{dt} = \\dfrac{100}{2500\\pi} = \\dfrac{1}{25\\pi} \\approx 0.0127 \\text{ cm/s}$.",
               "justificacion_md": "El radio crece muy lentamente cuando el globo ya es grande, lo que tiene sentido geométrico: a más superficie, menos cambia el radio para el mismo volumen agregado.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Escalera que resbala",
          problema_md="Una escalera de $5$ m está apoyada contra una pared. La base se aleja de la pared a $\\dfrac{dx}{dt} = 1 \\text{ m/s}$. ¿A qué velocidad cae la parte superior cuando la base está a $3$ m de la pared?",
          pasos=[
              {"accion_md": "**Variables:** $x(t)$ = distancia de la base a la pared, $y(t)$ = altura de la parte superior. La escalera tiene largo fijo $5$.\n\n**Datos:** $\\dfrac{dx}{dt} = 1$. **Buscamos:** $\\dfrac{dy}{dt}$ cuando $x = 3$.",
               "justificacion_md": "Identificación de variables.",
               "es_resultado": False},
              {"accion_md": "**Ecuación de relación** (Pitágoras): $x^2 + y^2 = 25$.",
               "justificacion_md": "La escalera, la pared y el suelo forman un triángulo rectángulo.",
               "es_resultado": False},
              {"accion_md": "**Derivamos respecto a $t$:**\n\n$$2x \\cdot \\dfrac{dx}{dt} + 2y \\cdot \\dfrac{dy}{dt} = 0 \\implies \\dfrac{dy}{dt} = -\\dfrac{x}{y} \\cdot \\dfrac{dx}{dt}$$",
               "justificacion_md": "La derivada de la constante $25$ es $0$. Despejamos $dy/dt$.",
               "es_resultado": False},
              {"accion_md": "**Cuando $x = 3$:** $y = \\sqrt{25 - 9} = 4$. Sustituimos:\n\n$$\\dfrac{dy}{dt} = -\\dfrac{3}{4} \\cdot 1 = -0.75 \\text{ m/s}$$",
               "justificacion_md": "El signo negativo indica que $y$ **decrece** — la parte superior baja, como esperábamos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Tanque cónico llenándose con agua",
          problema_md="Un tanque cónico (vértice abajo) tiene altura $H = 10$ m y radio superior $R = 4$ m. Se vierte agua a $2 \\text{ m}^3/\\text{min}$. ¿A qué velocidad sube el nivel del agua cuando $h = 5$ m?",
          pasos=[
              {"accion_md": "**Variables:** $h(t)$ = altura del agua, $r(t)$ = radio de la superficie del agua, $V(t)$ = volumen.\n\n**Datos:** $\\dfrac{dV}{dt} = 2$. **Buscamos:** $\\dfrac{dh}{dt}$ cuando $h = 5$.",
               "justificacion_md": "Las tres cambian con el tiempo, pero $r$ y $h$ están vinculadas por la geometría del cono.",
               "es_resultado": False},
              {"accion_md": "**Relación entre $r$ y $h$** (triángulos semejantes): $\\dfrac{r}{h} = \\dfrac{R}{H} = \\dfrac{4}{10} = \\dfrac{2}{5}$, así $r = \\dfrac{2h}{5}$.",
               "justificacion_md": "Eliminamos $r$ en favor de $h$: el problema queda en una sola variable espacial.",
               "es_resultado": False},
              {"accion_md": "**Ecuación de relación:**\n\n$$V = \\dfrac{1}{3}\\pi r^2 h = \\dfrac{1}{3}\\pi \\left(\\dfrac{2h}{5}\\right)^2 h = \\dfrac{4\\pi}{75} h^3$$",
               "justificacion_md": "Sustituimos $r$ por su expresión en función de $h$ antes de derivar — esto evita cargar con $dr/dt$.",
               "es_resultado": False},
              {"accion_md": "**Derivamos respecto a $t$:**\n\n$$\\dfrac{dV}{dt} = \\dfrac{12\\pi}{75} h^2 \\cdot \\dfrac{dh}{dt} = \\dfrac{4\\pi}{25} h^2 \\cdot \\dfrac{dh}{dt}$$",
               "justificacion_md": "Cadena en $h^3$: $3h^2 \\cdot h'(t)$.",
               "es_resultado": False},
              {"accion_md": "**Sustituimos** $h = 5$ y $\\dfrac{dV}{dt} = 2$:\n\n$$2 = \\dfrac{4\\pi}{25} \\cdot 25 \\cdot \\dfrac{dh}{dt} = 4\\pi \\cdot \\dfrac{dh}{dt} \\implies \\dfrac{dh}{dt} = \\dfrac{1}{2\\pi} \\approx 0.159 \\text{ m/min}$$",
               "justificacion_md": "**Lección clave:** simplificar la ecuación a una variable antes de derivar evita tener $dr/dt$ en la respuesta.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el método:",
          preguntas=[
              {
                  "enunciado_md": "En razones relacionadas, ¿cuándo se sustituyen los valores numéricos?",
                  "opciones_md": [
                      "Antes de derivar, para simplificar.",
                      "Después de derivar, en la ecuación final.",
                      "Cuando convenga.",
                      "Solo si la pregunta lo pide explícitamente.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Si se sustituyen antes, las variables se vuelven constantes y al derivar dan $0$. "
                      "**Sustituir antes de derivar es el error más común** del tema."
                  ),
              },
              {
                  "enunciado_md": "Si el área de un círculo crece a $5 \\text{ cm}^2/\\text{s}$, ¿a qué tasa crece el radio cuando $r = 10$?",
                  "opciones_md": [
                      "$\\dfrac{1}{4\\pi}$ cm/s",
                      "$\\dfrac{1}{2\\pi}$ cm/s",
                      "$\\dfrac{5}{2\\pi}$ cm/s",
                      "$5\\pi$ cm/s",
                  ],
                  "correcta": "A",
                  "explicacion_md": (
                      "$A = \\pi r^2 \\implies \\dfrac{dA}{dt} = 2\\pi r \\dfrac{dr}{dt}$. Sustituyendo $\\dfrac{dA}{dt} = 5$, $r = 10$: "
                      "$5 = 20\\pi \\dfrac{dr}{dt} \\implies \\dfrac{dr}{dt} = \\dfrac{1}{4\\pi}$ cm/s."
                  ),
              },
          ]),

        fig(
            "Diagrama de problema clasico de razones relacionadas: una escalera apoyada en una pared "
            "vertical. Pared vertical (linea negra), suelo horizontal (linea negra), escalera diagonal "
            "en teal #06b6d4 con etiqueta 'L = 5 m'. Se marca x = distancia base al pie de la pared "
            "(con flecha indicando que crece, en ambar #f59e0b) y y = altura del extremo superior "
            "(flecha indicando que decrece, en ambar). Pequenas flechas dx/dt y dy/dt junto a cada "
            "cantidad. Triangulo rectangulo formado, con el angulo recto destacado. Fondo blanco. "
            + STYLE
        ),
        ej(
            "Escalera deslizándose contra la pared",
            "Una escalera de $5$ m está apoyada contra una pared vertical. La base de la escalera se aleja de la pared a $0{,}3$ m/s. ¿A qué velocidad **desciende** el extremo superior cuando la base está a $3$ m de la pared?",
            [
                "Sea $x$ la distancia de la base a la pared y $y$ la altura del extremo superior. Plantea la ecuación que los relaciona usando Pitágoras.",
                "Deriva implícitamente respecto al tiempo y despeja $dy/dt$.",
            ],
            "**Modelo.** Por Pitágoras, $x^2 + y^2 = 5^2 = 25$.\n\n**Datos cuando $x = 3$:** $y = \\sqrt{25 - 9} = 4$ m. Y $\\dfrac{dx}{dt} = 0{,}3$ m/s.\n\n**Derivar respecto a $t$:** $2x \\dfrac{dx}{dt} + 2y \\dfrac{dy}{dt} = 0$.\n\n**Despejar:** $\\dfrac{dy}{dt} = -\\dfrac{x}{y} \\cdot \\dfrac{dx}{dt} = -\\dfrac{3}{4} \\cdot 0{,}3 = -0{,}225$ m/s.\n\n**Interpretación:** el extremo superior **desciende** a $0{,}225$ m/s (el signo negativo indica disminución de altura).",
        ),
        ej(
            "Globo esférico inflándose",
            "Un globo esférico se infla y su volumen aumenta a razón de $100$ cm³/s. ¿A qué velocidad crece el **radio** cuando el radio mide $5$ cm?",
            [
                "El volumen de la esfera es $V = \\dfrac{4}{3}\\pi r^3$. Deriva respecto a $t$.",
                "Despeja $dr/dt$ y sustituye los valores en el instante dado.",
            ],
            "**Modelo.** $V = \\dfrac{4}{3}\\pi r^3$.\n\n**Datos:** $\\dfrac{dV}{dt} = 100$ cm³/s, $r = 5$ cm.\n\n**Derivar:** $\\dfrac{dV}{dt} = 4\\pi r^2 \\dfrac{dr}{dt}$.\n\n**Despejar:** $\\dfrac{dr}{dt} = \\dfrac{1}{4\\pi r^2} \\cdot \\dfrac{dV}{dt} = \\dfrac{100}{4\\pi(25)} = \\dfrac{1}{\\pi} \\approx 0{,}318$ cm/s.\n\n**Interpretación:** el radio crece aproximadamente a $0{,}318$ cm por segundo en ese instante.",
        ),

        b("errores_comunes",
          items_md=[
              "**Sustituir valores numéricos antes de derivar.** Convierte variables en constantes y la derivada se anula incorrectamente.",
              "**Olvidar la cadena al derivar respecto a $t$.** $(r^2)' = 2r \\cdot r'(t)$, no $2r$.",
              "**No expresar todo en función de la variable de interés** cuando hay vínculos geométricos (como en el cono): tener $r$ y $h$ separadamente complica la derivada.",
              "**Confundir el signo:** una variable que decrece tiene **derivada negativa**. Si el problema dice \"se aleja\", el signo es positivo; si dice \"se acerca\", negativo.",
              "**No interpretar las unidades** del resultado. La velocidad de una longitud está en m/s, de un volumen en m³/s, etc.",
          ]),

        b("resumen",
          puntos_md=[
              "**Estructura:** dos o más cantidades cambiantes en el tiempo, relacionadas por una ecuación.",
              "**Procedimiento (5 pasos):** dibujo y variables → datos y meta → ecuación de relación → derivar respecto a $t$ → sustituir y despejar.",
              "**Sustituir valores numéricos al final, no al principio.**",
              "**Vínculos geométricos** (triángulos semejantes, Pitágoras) suelen permitir eliminar variables y simplificar.",
              "**Próxima lección:** aproximaciones lineales y diferenciales — usar la derivada para estimar valores cercanos.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-3-1-razones",
        "title": "Razones relacionadas",
        "description": "Variables que cambian con el tiempo y están vinculadas por una ecuación. Estrategia de 5 pasos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# LECCIÓN 3.2 — Aproximaciones lineales y diferenciales
# =====================================================================
def lesson_3_2():
    blocks = [
        b("texto", body_md=(
            "Calcular $\\sqrt{4.05}$ con un lápiz no es trivial. Pero $\\sqrt{4} = 2$, y la función está \"cerca\" allí. "
            "La idea de la **aproximación lineal** es usar la **recta tangente** en un punto conocido para estimar valores cercanos. "
            "Es un caso particular del polinomio de Taylor de orden $1$ y un puente conceptual hacia los **diferenciales**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Construir la **linealización** $L(x) = f(a) + f'(a)(x - a)$ y usarla para aproximar.\n"
            "- Distinguir entre **incremento** $\\Delta y$ y **diferencial** $dy$.\n"
            "- Estimar errores relativos y absolutos en mediciones."
        )),

        b("intuicion",
          titulo="La recta tangente \"copia\" la función cerca del punto",
          body_md=(
              "Cerca de un punto $a$, la gráfica de $f$ y la **recta tangente** en $(a, f(a))$ son casi indistinguibles. "
              "Si nos alejamos, la recta y la curva se separan — pero para distancias pequeñas, la recta es una excelente aproximación.\n\n"
              "Eso es lo que captura la fórmula:\n\n"
              "$$f(x) \\approx f(a) + f'(a)(x - a) \\quad \\text{para } x \\text{ cerca de } a$$"
          )),

        b("definicion",
          titulo="Linealización",
          body_md=(
              "La **linealización** de $f$ en $a$ es la función:\n\n"
              "$$L(x) = f(a) + f'(a)(x - a)$$\n\n"
              "Es exactamente la recta tangente en $(a, f(a))$, vista como función de $x$. Para $x$ cerca de $a$, $f(x) \\approx L(x)$."
          )),

        b("ejemplo_resuelto",
          titulo="Aproximar $\\sqrt{4.05}$",
          problema_md="Estimar $\\sqrt{4.05}$ usando la linealización de $f(x) = \\sqrt{x}$ en $a = 4$.",
          pasos=[
              {"accion_md": "**Calculamos $f(a)$ y $f'(a)$:** $f(4) = 2$, $f'(x) = \\dfrac{1}{2\\sqrt{x}}$, $f'(4) = \\dfrac{1}{4}$.",
               "justificacion_md": "Necesitamos el valor y la pendiente en $a$.",
               "es_resultado": False},
              {"accion_md": "**Linealización:** $L(x) = 2 + \\dfrac{1}{4}(x - 4)$.",
               "justificacion_md": "Recta tangente en $(4, 2)$.",
               "es_resultado": False},
              {"accion_md": "**Evaluamos en $x = 4.05$:** $L(4.05) = 2 + \\dfrac{1}{4}(0.05) = 2.0125$.",
               "justificacion_md": "Aproximación.",
               "es_resultado": False},
              {"accion_md": "$\\sqrt{4.05} \\approx 2.0125$. (Valor real: $2.01246\\ldots$)",
               "justificacion_md": "**Error de menos de $0.0001$**. Para qué tan poco trabajo, es excelente.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Aproximar $(1.02)^{10}$",
          problema_md="Estimar $(1.02)^{10}$ con linealización en $a = 1$.",
          pasos=[
              {"accion_md": "$f(x) = x^{10}$, $f'(x) = 10 x^9$. $f(1) = 1$, $f'(1) = 10$.",
               "justificacion_md": "Punto base $a = 1$ y derivada allí.",
               "es_resultado": False},
              {"accion_md": "$L(x) = 1 + 10(x - 1)$. Evaluamos en $1.02$: $L(1.02) = 1 + 10(0.02) = 1.2$.",
               "justificacion_md": "Linealización aplicada.",
               "es_resultado": False},
              {"accion_md": "$(1.02)^{10} \\approx 1.2$. (Valor real: $1.21899\\ldots$)",
               "justificacion_md": "El error es mayor (~$0.02$) porque $0.02$ ya no es \"infinitesimal\". Aún así, da un orden de magnitud útil.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Diferenciales",
          body_md=(
              "Si $y = f(x)$ y $\\Delta x$ es un cambio en $x$:\n\n"
              "- **Incremento real** de $y$: $\\Delta y = f(x + \\Delta x) - f(x)$.\n"
              "- **Diferencial** de $y$: $dy = f'(x) \\, dx$, donde $dx = \\Delta x$.\n\n"
              "Para $\\Delta x$ pequeño, $\\Delta y \\approx dy$. Es la misma idea que la linealización, escrita en notación diferencial."
          )),

        b("ejemplo_resuelto",
          titulo="Estimación de error",
          problema_md="Se mide el radio de una esfera como $r = 10$ cm con un error máximo de $\\pm 0.1$ cm. Estimar el error máximo en el volumen calculado.",
          pasos=[
              {"accion_md": "$V(r) = \\dfrac{4}{3}\\pi r^3$. **Diferencial:** $dV = 4\\pi r^2 \\, dr$.",
               "justificacion_md": "$\\dfrac{dV}{dr} = 4\\pi r^2$.",
               "es_resultado": False},
              {"accion_md": "Con $r = 10$ y $|dr| \\leq 0.1$:\n\n$$|dV| \\leq 4\\pi (10)^2 (0.1) = 40\\pi \\approx 125.7 \\text{ cm}^3$$",
               "justificacion_md": "El error absoluto en $V$ está acotado por $40\\pi$.",
               "es_resultado": False},
              {"accion_md": "**Error relativo:**\n\n$$\\dfrac{dV}{V} = \\dfrac{4\\pi r^2 \\, dr}{(4/3)\\pi r^3} = 3 \\dfrac{dr}{r}$$\n\nCon $\\dfrac{dr}{r} = \\dfrac{0.1}{10} = 1\\%$, el error relativo en $V$ es $\\approx 3\\%$.",
               "justificacion_md": "**Lección general:** el error relativo se **multiplica por la potencia** de la variable. En el cubo, errores en $r$ se triplican en $V$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo:",
          preguntas=[
              {
                  "enunciado_md": "La linealización de $f(x) = \\cos x$ en $a = 0$ es:",
                  "opciones_md": ["$L(x) = x$", "$L(x) = 1$", "$L(x) = 1 - x$", "$L(x) = 1 - \\dfrac{x^2}{2}$"],
                  "correcta": "B",
                  "explicacion_md": (
                      "$f(0) = 1$, $f'(x) = -\\sin x$, $f'(0) = 0$. Así $L(x) = 1 + 0(x - 0) = 1$. **Cerca de $0$, $\\cos x \\approx 1$**, una aproximación pobre porque la pendiente es cero — para mejorar habría que ir al polinomio de Taylor de orden $2$: $1 - x^2/2$."
                  ),
              },
              {
                  "enunciado_md": "Si $f(x) = x^3$ y $\\Delta x = 0.01$ en $x = 2$, $dy \\approx ?$",
                  "opciones_md": ["$0.06$", "$0.12$", "$0.5$", "$2$"],
                  "correcta": "B",
                  "explicacion_md": (
                      "$dy = f'(x) \\, dx = 3x^2 \\, dx = 3(4)(0.01) = 0.12$."
                  ),
              },
          ]),

        fig(
            "Grafica que ilustra la aproximacion lineal: una curva no lineal y = f(x) en teal #06b6d4 "
            "(forma similar a y = sqrt(x)). Marcado el punto de tangencia (a, f(a)) y trazada la recta "
            "tangente (linealizacion L(x)) en color ambar #f59e0b. A la derecha del punto, marca un "
            "x cercano y muestra dos segmentos verticales: dy (incremento de la tangente) y delta y "
            "(incremento real). Etiquetas claras para dx, dy, delta y. Anotacion: 'L(x) = f(a) + f'(a)(x-a)'. "
            "Fondo blanco, ejes con flechas. " + STYLE
        ),
        ej(
            "Aproximación lineal de una raíz",
            "Usa la linealización de $f(x) = \\sqrt{x}$ en $a = 25$ para estimar $\\sqrt{26}$. Compara con el valor real con calculadora.",
            [
                "Calcula $f(25)$, $f'(x) = 1/(2\\sqrt{x})$ y $f'(25)$.",
                "Aplica $L(x) = f(a) + f'(a)(x - a)$ con $x = 26$, $a = 25$.",
            ],
            "**Paso 1 — Datos en $a = 25$.** $f(25) = 5$, $f'(x) = \\dfrac{1}{2\\sqrt{x}}$, $f'(25) = \\dfrac{1}{10}$.\n\n**Paso 2 — Linealización.**\n\n$$L(x) = 5 + \\dfrac{1}{10}(x - 25).$$\n\n**Paso 3 — Estimar $\\sqrt{26}$.**\n\n$$\\sqrt{26} \\approx L(26) = 5 + \\dfrac{1}{10}(1) = 5{,}1.$$\n\n**Comparación:** valor real $\\sqrt{26} \\approx 5{,}09902$. Error absoluto $\\approx 0{,}001$ ($0{,}02\\%$).",
        ),
        ej(
            "Estimación de error con diferenciales",
            "Se mide el radio de una esfera y resulta $r = 10$ cm con un error máximo de $0{,}1$ cm. Estima el **error máximo absoluto** y el **error relativo** al calcular el volumen.",
            [
                "Volumen $V = \\dfrac{4}{3}\\pi r^3$. Calcula $dV = V'(r)\\, dr$.",
                "Error relativo $= |dV / V|$.",
            ],
            "**Paso 1 — Diferencial.** $V = \\tfrac{4}{3}\\pi r^3$, así $dV = 4\\pi r^2\\, dr$.\n\n**Paso 2 — Sustituir.** Con $r = 10$ y $dr = 0{,}1$: $dV = 4\\pi (100)(0{,}1) = 40\\pi \\approx 125{,}66$ cm³.\n\n**Paso 3 — Volumen nominal.** $V = \\tfrac{4}{3}\\pi (1000) \\approx 4188{,}79$ cm³.\n\n**Paso 4 — Error relativo.**\n\n$$\\left|\\dfrac{dV}{V}\\right| = \\dfrac{40\\pi}{(4/3)\\pi(1000)} = \\dfrac{40 \\cdot 3}{4000} = 0{,}03 = 3\\%.$$\n\n**Resumen:** error absoluto $\\approx 125{,}7$ cm³; error relativo $3\\%$. Observa que un error de $1\\%$ en el radio se amplifica a $3\\%$ en el volumen (factor $3$ que viene del exponente cúbico).",
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\Delta y$ con $dy$.** $\\Delta y$ es el incremento exacto, $dy$ es la aproximación lineal. Para $\\Delta x$ pequeño coinciden, para grande no.",
              "**Aplicar la linealización lejos del punto base.** Cuanto más se aleje $x$ de $a$, peor es la aproximación.",
              "**No verificar que $f$ sea derivable** en $a$. La linealización exige $f'(a)$ definida.",
              "**Olvidar el signo en la estimación de error.** El error relativo y absoluto siempre se reportan como valor absoluto.",
              "**Confundir error relativo ($dy/y$) con error absoluto ($dy$).** El relativo es porcentual, el absoluto va en las unidades de la variable.",
          ]),

        b("resumen",
          puntos_md=[
              "**Linealización:** $L(x) = f(a) + f'(a)(x - a)$. Es la recta tangente como función.",
              "**Aproximación:** $f(x) \\approx L(x)$ para $x$ cerca de $a$.",
              "**Diferencial:** $dy = f'(x) \\, dx$. Aproxima $\\Delta y$ para $\\Delta x$ pequeño.",
              "**Estimación de error:** los diferenciales propagan errores absolutos y relativos en mediciones.",
              "**Lección siguiente:** localización de máximos y mínimos — la aplicación más clásica de derivadas.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-3-2-aproximaciones",
        "title": "Aproximaciones lineales y diferenciales",
        "description": "Linealización con la recta tangente, diferenciales y estimación de errores.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 2,
    }


# =====================================================================
# LECCIÓN 3.3 — Máximos y mínimos
# =====================================================================
def lesson_3_3():
    blocks = [
        b("texto", body_md=(
            "Los **valores extremos** (máximos y mínimos) de una función responden a preguntas como: "
            "¿cuál es la mayor área que puede tener un rectángulo con cierto perímetro? ¿cuál es el menor costo de producir $x$ unidades?\n\n"
            "Esta lección presenta el aparato teórico — definiciones, teoremas y técnicas para localizarlos. La aplicación práctica viene en la lección de optimización.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Distinguir **máximos/mínimos absolutos** de **locales**.\n"
            "- Identificar **puntos críticos** ($f' = 0$ o $f'$ no existe).\n"
            "- Aplicar el **teorema del valor extremo** y el **método del intervalo cerrado**."
        )),

        b("definicion",
          titulo="Máximos y mínimos",
          body_md=(
              "Sea $f$ definida en un conjunto $D$.\n\n"
              "**Máximo absoluto** en $c$: $f(c) \\geq f(x)$ para todo $x \\in D$.\n\n"
              "**Mínimo absoluto** en $c$: $f(c) \\leq f(x)$ para todo $x \\in D$.\n\n"
              "**Máximo local** en $c$: $f(c) \\geq f(x)$ para todo $x$ en algún intervalo abierto que contenga a $c$.\n\n"
              "**Mínimo local** en $c$: $f(c) \\leq f(x)$ para todo $x$ en algún intervalo abierto que contenga a $c$."
          )),

        b("teorema",
          nombre="Teorema del valor extremo",
          enunciado_md=(
              "Si $f$ es **continua en un intervalo cerrado** $[a, b]$, entonces $f$ alcanza un **máximo absoluto** y un **mínimo absoluto** en $[a, b]$."
          ),
          demostracion_md=(
              "La demostración rigurosa usa la propiedad de Bolzano-Weierstrass y queda fuera de un curso introductorio. Lo importante es retener las **dos hipótesis**: continuidad y dominio cerrado y acotado. Si falta una, el teorema puede fallar.\n\n"
              "**Contraejemplos:**\n\n"
              "- $f(x) = x$ en $(0, 1)$ (no cerrado): no tiene máximo ni mínimo absoluto.\n"
              "- $f(x) = 1/x$ en $(0, 1]$ (no acotado por discontinuidad): no tiene máximo absoluto."
          )),

        b("definicion",
          titulo="Punto crítico",
          body_md=(
              "$c$ es **punto crítico** de $f$ si $c$ está en el dominio de $f$ y se cumple alguna de:\n\n"
              "1. $f'(c) = 0$, o\n"
              "2. $f'(c)$ no existe.\n\n"
              "Los puntos críticos son los **únicos candidatos a extremos locales** en el interior del dominio."
          )),

        b("teorema",
          nombre="Teorema de Fermat",
          enunciado_md=(
              "Si $f$ tiene un **extremo local** en $c$ y $f'(c)$ existe, entonces $f'(c) = 0$."
          ),
          demostracion_md=(
              "Si $c$ es máximo local, entonces para $h$ pequeño, $f(c+h) - f(c) \\leq 0$.\n\n"
              "- Si $h > 0$: $\\dfrac{f(c+h) - f(c)}{h} \\leq 0$, así $\\lim_{h \\to 0^+} \\leq 0$.\n"
              "- Si $h < 0$: $\\dfrac{f(c+h) - f(c)}{h} \\geq 0$, así $\\lim_{h \\to 0^-} \\geq 0$.\n\n"
              "Como ambos laterales coinciden con $f'(c)$, debe ser $f'(c) = 0$. Análogo para mínimo."
          )),

        b("intuicion",
          titulo="Recíproca de Fermat: ¡falsa!",
          body_md=(
              "$f'(c) = 0$ **no garantiza** un extremo. Ejemplo clásico: $f(x) = x^3$ en $c = 0$. La derivada es $0$ pero la función sigue creciendo (no hay extremo, hay **inflexión**).\n\n"
              "Por eso, encontrar puntos críticos solo da **candidatos**: hay que clasificarlos con un test posterior (criterio de la primera o segunda derivada, en la lección de forma de la gráfica)."
          )),

        b("definicion",
          titulo="Método del intervalo cerrado",
          body_md=(
              "Para encontrar el **máximo y mínimo absolutos** de $f$ continua en $[a, b]$:\n\n"
              "1. Encontrar todos los **puntos críticos** en $(a, b)$.\n"
              "2. Evaluar $f$ en esos puntos críticos y en los **extremos del intervalo** $a$ y $b$.\n"
              "3. El **mayor** valor es el máximo absoluto; el **menor**, el mínimo absoluto.\n\n"
              "Funciona porque el TVE garantiza la existencia, y los extremos siempre son puntos críticos o bordes del intervalo."
          )),

        b("ejemplo_resuelto",
          titulo="Extremos absolutos de $f(x) = x^3 - 3x^2 + 1$ en $[-1, 4]$",
          problema_md="Encontrar el máximo y mínimo absolutos.",
          pasos=[
              {"accion_md": "**Puntos críticos:** $f'(x) = 3x^2 - 6x = 3x(x - 2)$. Se anula en $x = 0$ y $x = 2$. Ambos están en $(-1, 4)$.",
               "justificacion_md": "Resolvemos $f'(x) = 0$. La derivada existe en todo el intervalo, así no hay puntos críticos del segundo tipo.",
               "es_resultado": False},
              {"accion_md": "**Evaluamos en los críticos y en los bordes:**\n\n- $f(-1) = -1 - 3 + 1 = -3$\n- $f(0) = 1$\n- $f(2) = 8 - 12 + 1 = -3$\n- $f(4) = 64 - 48 + 1 = 17$",
               "justificacion_md": "Son los $4$ candidatos.",
               "es_resultado": False},
              {"accion_md": "**Máximo absoluto:** $f(4) = 17$. **Mínimo absoluto:** $f(-1) = f(2) = -3$ (alcanzado en dos lugares).",
               "justificacion_md": "El método localiza el máximo y mínimo absolutos sin tener que clasificar como locales primero.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Punto crítico donde $f'$ no existe",
          problema_md="Encontrar puntos críticos de $f(x) = x^{2/3}$ en $[-1, 1]$ y los extremos absolutos.",
          pasos=[
              {"accion_md": "$f'(x) = \\dfrac{2}{3} x^{-1/3} = \\dfrac{2}{3 \\sqrt[3]{x}}$. **No está definida en $x = 0$**, pero $f(0) = 0$ sí. Por tanto $x = 0$ es **punto crítico** (segundo tipo).",
               "justificacion_md": "$f'(x)$ nunca se anula, pero falla en $x = 0$.",
               "es_resultado": False},
              {"accion_md": "**Evaluamos:** $f(-1) = 1$, $f(0) = 0$, $f(1) = 1$.",
               "justificacion_md": "Tres candidatos: dos bordes y el punto crítico.",
               "es_resultado": False},
              {"accion_md": "**Mínimo absoluto:** $f(0) = 0$. **Máximo absoluto:** $f(\\pm 1) = 1$.",
               "justificacion_md": "El mínimo está en una **esquina** (la gráfica de $x^{2/3}$ tiene una cúspide en el origen). Los bordes empatan en el máximo.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál es la diferencia entre punto crítico y extremo?",
                  "opciones_md": [
                      "Son sinónimos.",
                      "Un extremo siempre es punto crítico, pero no todo crítico es extremo.",
                      "Un crítico siempre es extremo, pero no al revés.",
                      "No tienen relación.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "**Fermat** dice: si hay extremo local con derivada existente, entonces $f' = 0$ allí — todo extremo es crítico. Pero la **recíproca falla** ($x^3$ en $0$ es crítico sin ser extremo). Los críticos son **candidatos**, no garantías."
                  ),
              },
              {
                  "enunciado_md": "Para $f(x) = 2x - x^2$ en $[0, 3]$, el máximo absoluto vale:",
                  "opciones_md": ["$0$", "$1$", "$-3$", "$2$"],
                  "correcta": "B",
                  "explicacion_md": (
                      "$f'(x) = 2 - 2x = 0 \\implies x = 1$. Evaluamos: $f(0) = 0$, $f(1) = 1$, $f(3) = -3$. Máximo: $1$."
                  ),
              },
          ]),

        fig(
            "Grafica de una funcion en un intervalo cerrado [a, b] que ilustra los tipos de extremos. "
            "Curva continua en teal #06b6d4. Marcar con puntos en ambar #f59e0b: un maximo local interior "
            "(con tangente horizontal), un minimo local interior, el maximo absoluto en el borde derecho "
            "x=b, y el minimo absoluto en un punto critico interior. Etiquetas: 'maximo local', 'minimo "
            "local', 'maximo absoluto', 'minimo absoluto'. Lineas tangentes horizontales en los puntos "
            "interiores. Ejes con flechas, fondo blanco. " + STYLE
        ),
        ej(
            "Extremos absolutos en un intervalo cerrado",
            "Encuentra los valores **máximo y mínimo absolutos** de $f(x) = x^3 - 3x + 1$ en $[-2, 2]$.",
            [
                "Encuentra los puntos críticos resolviendo $f'(x) = 0$.",
                "Evalúa $f$ en cada punto crítico interior y en los extremos del intervalo. Compara.",
            ],
            "**Paso 1 — Puntos críticos.** $f'(x) = 3x^2 - 3 = 3(x-1)(x+1) = 0 \\Rightarrow x = -1,\\ x = 1$.\n\nAmbos están en $(-2, 2)$.\n\n**Paso 2 — Evaluar.**\n\n| $x$ | $f(x)$ |\n|---|---|\n| $-2$ | $-8 + 6 + 1 = -1$ |\n| $-1$ | $-1 + 3 + 1 = 3$ |\n| $1$ | $1 - 3 + 1 = -1$ |\n| $2$ | $8 - 6 + 1 = 3$ |\n\n**Paso 3 — Conclusión.** Máximo absoluto: $3$, alcanzado en $x = -1$ y $x = 2$. Mínimo absoluto: $-1$, alcanzado en $x = -2$ y $x = 1$.",
        ),
        ej(
            "Crítico no derivable",
            "Encuentra todos los puntos críticos y los extremos absolutos de $f(x) = |x^2 - 4|$ en $[-3, 3]$.",
            [
                "Reescribe $f$ por tramos abriendo el valor absoluto donde $x^2 - 4$ cambia de signo.",
                "Hay dos tipos de puntos críticos: donde $f' = 0$ y donde $f$ no es derivable.",
            ],
            "**Paso 1 — Función por tramos.** $x^2 - 4 \\geq 0 \\iff |x| \\geq 2$. Así $f(x) = \\begin{cases} x^2 - 4 & |x| \\geq 2 \\\\ 4 - x^2 & |x| < 2 \\end{cases}$.\n\n**Paso 2 — Derivada por tramos.** $f'(x) = 2x$ si $|x| > 2$, $f'(x) = -2x$ si $|x| < 2$. En $x = \\pm 2$ las pendientes laterales no coinciden — **no derivable**.\n\n**Paso 3 — Puntos críticos.**\n- $f'(x) = 0$: en interior $|x| < 2$, $-2x = 0 \\Rightarrow x = 0$. En interior $|x| > 2$ no hay (en $(-3, -2)$ y $(2, 3)$, $2x = 0$ da $x = 0$ que no pertenece).\n- No derivables: $x = -2,\\ x = 2$.\n\n**Paso 4 — Evaluar en críticos y bordes.** $f(-3) = 5$, $f(-2) = 0$, $f(0) = 4$, $f(2) = 0$, $f(3) = 5$.\n\n**Conclusión:** máximo absoluto $5$ en $x = \\pm 3$; mínimo absoluto $0$ en $x = \\pm 2$.",
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar el método del intervalo cerrado en intervalos abiertos.** El TVE no garantiza extremos en abiertos.",
              "**Olvidar los puntos críticos donde $f'$ no existe.** No solo $f' = 0$ los produce; también la no-derivabilidad.",
              "**Asumir que $f'(c) = 0 \\Rightarrow$ extremo.** La recíproca de Fermat es falsa: $x^3$ en $0$ es el contraejemplo canónico.",
              "**No evaluar en los bordes** del intervalo. El máximo absoluto puede estar en $a$ o $b$, no necesariamente en un crítico interior.",
              "**Aplicar el TVE sin verificar continuidad.** Si $f$ tiene una asíntota o un salto, el teorema no aplica.",
          ]),

        b("resumen",
          puntos_md=[
              "**Extremos absolutos:** mayor/menor valor en todo el dominio. **Locales:** mayor/menor en un entorno.",
              "**Teorema del valor extremo:** $f$ continua en $[a, b]$ alcanza máximo y mínimo absolutos.",
              "**Punto crítico:** $f'(c) = 0$ o $f'(c)$ no existe. Son los únicos candidatos interiores a extremos locales.",
              "**Fermat:** extremo local + derivable $\\Rightarrow$ punto crítico (recíproca falsa).",
              "**Método del intervalo cerrado:** evaluar en críticos + bordes y comparar.",
              "**Próxima lección:** Teorema del Valor Medio — la herramienta teórica que conecta derivada con comportamiento global.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-3-3-extremos",
        "title": "Máximos y mínimos",
        "description": "Extremos absolutos y locales, puntos críticos, Teorema del Valor Extremo y método del intervalo cerrado.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 3,
    }


# =====================================================================
# LECCIÓN 3.4 — Teorema del Valor Medio
# =====================================================================
def lesson_3_4():
    blocks = [
        b("texto", body_md=(
            "El **Teorema del Valor Medio (TVM)** es uno de los resultados más importantes del cálculo: "
            "conecta la **derivada en un punto** con el **comportamiento global** de la función en un intervalo. "
            "De él se derivan muchos resultados: que $f' = 0$ implica $f$ constante, que $f' = g'$ implica $f = g + C$, y muchos otros que se usarán a lo largo de toda la carrera.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Enunciar y aplicar el **teorema de Rolle** y el **TVM**.\n"
            "- Comprender la **interpretación geométrica** y de **velocidad media**.\n"
            "- Aplicar las consecuencias: caracterización de funciones constantes y de antiderivadas únicas (salvo constante)."
        )),

        b("teorema",
          nombre="Teorema de Rolle",
          enunciado_md=(
              "Si $f$ es:\n\n"
              "1. Continua en $[a, b]$,\n"
              "2. Derivable en $(a, b)$,\n"
              "3. $f(a) = f(b)$,\n\n"
              "entonces existe $c \\in (a, b)$ tal que $f'(c) = 0$."
          ),
          demostracion_md=(
              "Por el TVE, $f$ alcanza un máximo $M$ y un mínimo $m$ en $[a, b]$.\n\n"
              "**Caso 1:** $M = m$. Entonces $f$ es constante, $f' = 0$ en todo $(a, b)$.\n\n"
              "**Caso 2:** $M > m$. Como $f(a) = f(b)$, al menos uno de los extremos absolutos no se alcanza en $a$ ni en $b$, sino en algún $c \\in (a, b)$. Por Fermat, $f'(c) = 0$."
          )),

        b("intuicion",
          titulo="Geometría de Rolle",
          body_md=(
              "Si una curva derivable empieza y termina a la misma altura, entonces **en algún punto intermedio la pendiente es horizontal**. "
              "Es geométricamente obvio: si subes, en algún momento tienes que bajar — y entre subir y bajar hay un instante de pendiente cero."
          )),

        b("teorema",
          nombre="Teorema del Valor Medio",
          enunciado_md=(
              "Si $f$ es:\n\n"
              "1. Continua en $[a, b]$,\n"
              "2. Derivable en $(a, b)$,\n\n"
              "entonces existe $c \\in (a, b)$ tal que:\n\n"
              "$$f'(c) = \\dfrac{f(b) - f(a)}{b - a}$$"
          ),
          demostracion_md=(
              "Definimos $h(x) = f(x) - L(x)$, donde $L(x)$ es la recta secante:\n\n"
              "$$L(x) = f(a) + \\dfrac{f(b) - f(a)}{b - a}(x - a)$$\n\n"
              "Entonces $h(a) = 0$ y $h(b) = 0$. Por **Rolle** aplicado a $h$, existe $c \\in (a, b)$ con $h'(c) = 0$. Pero $h'(x) = f'(x) - \\dfrac{f(b)-f(a)}{b-a}$, así $f'(c) = \\dfrac{f(b) - f(a)}{b - a}$."
          )),

        b("intuicion",
          titulo="Interpretación: velocidad instantánea = velocidad media",
          body_md=(
              "Si $f(t)$ es la posición de un auto y $a < b$ son dos instantes:\n\n"
              "- $\\dfrac{f(b) - f(a)}{b - a}$ es la **velocidad media** entre $a$ y $b$.\n"
              "- $f'(c)$ es la **velocidad instantánea** en $c$.\n\n"
              "El TVM dice: **en algún instante intermedio, el velocímetro marcó exactamente la velocidad promedio del trayecto.**\n\n"
              "Si manejaste $100$ km en $1$ hora (promedio $100$ km/h), aunque el velocímetro fluctuó, **en algún momento marcó exactamente $100$**."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicar el TVM a $f(x) = x^3$ en $[0, 2]$",
          problema_md="Encontrar el $c$ del TVM.",
          pasos=[
              {"accion_md": "**Verificamos las hipótesis:** $f$ es polinomial, así continua y derivable en todo $\\mathbb{R}$.",
               "justificacion_md": "Las dos hipótesis se cumplen.",
               "es_resultado": False},
              {"accion_md": "**Pendiente de la secante:**\n\n$$\\dfrac{f(2) - f(0)}{2 - 0} = \\dfrac{8 - 0}{2} = 4$$",
               "justificacion_md": "Es lo que debe igualar $f'(c)$.",
               "es_resultado": False},
              {"accion_md": "**Buscamos $c$:** $f'(x) = 3x^2 = 4 \\implies x^2 = \\dfrac{4}{3} \\implies x = \\pm \\dfrac{2}{\\sqrt{3}}$.\n\nDe estos, **$c = \\dfrac{2}{\\sqrt{3}} \\approx 1.155$** está en $(0, 2)$.",
               "justificacion_md": "El TVM garantiza la existencia; aquí lo encontramos explícitamente.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Consecuencia 1: $f' = 0 \\Rightarrow f$ constante",
          enunciado_md=(
              "Si $f$ es derivable en un intervalo $I$ y $f'(x) = 0$ para todo $x \\in I$, entonces $f$ es **constante** en $I$."
          ),
          demostracion_md=(
              "Sean $a < b$ en $I$. Por TVM existe $c \\in (a, b)$ con $f'(c) = (f(b)-f(a))/(b-a)$. Pero $f'(c) = 0$, así $f(b) = f(a)$. Como esto vale para todo par, $f$ es constante."
          )),

        b("teorema",
          nombre="Consecuencia 2: $f' = g' \\Rightarrow f = g + C$",
          enunciado_md=(
              "Si $f$ y $g$ son derivables en $I$ y $f'(x) = g'(x)$ para todo $x \\in I$, entonces existe una constante $C$ tal que $f(x) = g(x) + C$."
          ),
          demostracion_md=(
              "Sea $h = f - g$. Entonces $h' = f' - g' = 0$, así $h$ es constante por la consecuencia 1. Llamando $C$ a esa constante: $f - g = C$."
          )),

        b("intuicion",
          titulo="Por qué la consecuencia 2 es importante",
          body_md=(
              "**Establece la unicidad de la antiderivada salvo una constante.** Si encontramos una función $F$ con $F' = f$, entonces **todas** las antiderivadas son $F + C$.\n\n"
              "Ese resultado es la base del cálculo integral: cuando se calcula $\\int f(x) \\, dx$, la respuesta siempre lleva $+ C$ — y la consecuencia 2 del TVM justifica por qué."
          )),

        b("verificacion",
          intro_md="Verifica las hipótesis:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál NO es hipótesis del TVM?",
                  "opciones_md": [
                      "$f$ continua en $[a, b]$",
                      "$f$ derivable en $(a, b)$",
                      "$f(a) = f(b)$",
                      "$a < b$",
                  ],
                  "correcta": "C",
                  "explicacion_md": (
                      "$f(a) = f(b)$ es la hipótesis adicional de **Rolle**, no del TVM. El TVM no exige eso."
                  ),
              },
              {
                  "enunciado_md": "Si $f'(x) = 0$ para todo $x \\in (1, 5)$ y $f$ es continua en $[1, 5]$, entonces $f$ en $[1, 5]$ es:",
                  "opciones_md": ["Lineal", "Constante", "Polinomial de grado 2", "No se puede determinar"],
                  "correcta": "B",
                  "explicacion_md": (
                      "Por la consecuencia 1 del TVM, $f' = 0$ en un intervalo implica $f$ constante."
                  ),
              },
          ]),

        fig(
            "Diagrama del Teorema del Valor Medio: una curva continua y derivable en un intervalo [a,b] "
            "dibujada en teal #06b6d4. Marcar los puntos extremos A=(a, f(a)) y B=(b, f(b)) y trazar la "
            "secante A-B con linea punteada. Marcar un punto interior (c, f(c)) y trazar la tangente a "
            "la curva en ese punto en color ambar #f59e0b. La tangente debe ser visiblemente paralela a "
            "la secante. Anotacion: 'f'(c) = (f(b)-f(a))/(b-a)'. Ejes con flechas, fondo blanco. " + STYLE
        ),
        ej(
            "Aplicar el TVM y encontrar el $c$ explícito",
            "Verifica que $f(x) = x^2 - 3x + 2$ satisface las hipótesis del TVM en $[1, 4]$ y encuentra explícitamente el valor de $c \\in (1, 4)$ que el teorema garantiza.",
            [
                "$f$ es polinomio: continua y derivable en todo $\\mathbb{R}$, así satisface las hipótesis.",
                "Calcula la pendiente de la secante $(f(4) - f(1))/(4 - 1)$ y resuelve $f'(c) =$ ese valor.",
            ],
            "**Paso 1 — Hipótesis.** $f$ es polinomio: continua en $[1, 4]$ y derivable en $(1, 4)$. ✓\n\n**Paso 2 — Pendiente de la secante.** $f(1) = 0$, $f(4) = 6$. Pendiente $= \\dfrac{6 - 0}{4 - 1} = 2$.\n\n**Paso 3 — Resolver $f'(c) = 2$.** $f'(x) = 2x - 3$, así $2c - 3 = 2 \\Rightarrow c = \\dfrac{5}{2}$.\n\n**Verificación:** $\\dfrac{5}{2} \\in (1, 4)$. ✓\n\n**Conclusión:** el TVM garantiza la existencia de $c = 5/2$ donde la tangente es paralela a la secante.",
        ),
        ej(
            "Acotar variación con el TVM",
            "Sea $f$ una función derivable en $\\mathbb{R}$ tal que $|f'(x)| \\leq 5$ para todo $x$, y $f(2) = 1$. Demuestra que $|f(7) - 1| \\leq 25$ y describe en general qué dice el TVM sobre el crecimiento de $f$.",
            [
                "Aplica el TVM en el intervalo $[2, 7]$.",
                "Toma valor absoluto y usa la cota $|f'| \\leq 5$.",
            ],
            "**Paso 1 — Aplicar el TVM en $[2, 7]$.** Existe $c \\in (2, 7)$ tal que\n\n$$\\dfrac{f(7) - f(2)}{7 - 2} = f'(c) \\;\\Longleftrightarrow\\; f(7) - f(2) = 5\\, f'(c).$$\n\n**Paso 2 — Acotar.** $|f(7) - f(2)| = 5\\,|f'(c)| \\leq 5 \\cdot 5 = 25$.\n\nComo $f(2) = 1$, esto da $|f(7) - 1| \\leq 25$, es decir $f(7) \\in [-24, 26]$.\n\n**Interpretación general:** si $|f'| \\leq M$ en un intervalo, entonces $|f(b) - f(a)| \\leq M\\,|b - a|$ — la función es **Lipschitz** con constante $M$. Es una herramienta clásica para acotar variación a partir de cotas en la derivada.",
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Rolle o TVM sin verificar continuidad o derivabilidad.** Si fallan, el teorema no garantiza nada.",
              "**Confundir Rolle con TVM.** Rolle es el caso particular cuando $f(a) = f(b)$.",
              "**Pensar que el $c$ es único.** Puede haber varios; el teorema solo garantiza al menos uno.",
              "**Aplicar el TVM en intervalos abiertos.** La continuidad debe ser en el cerrado, la derivabilidad en el abierto. La parte cerrada es importante.",
              "**Concluir $f$ constante a partir de $f' = 0$ en un punto.** La hipótesis es $f' = 0$ en **todo** un intervalo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Rolle:** $f$ continua en $[a, b]$, derivable en $(a, b)$, $f(a) = f(b)$ $\\Rightarrow$ existe $c$ con $f'(c) = 0$.",
              "**TVM:** $f$ continua en $[a, b]$, derivable en $(a, b)$ $\\Rightarrow$ existe $c$ con $f'(c) = \\dfrac{f(b)-f(a)}{b-a}$.",
              "**Interpretación:** la velocidad instantánea iguala la velocidad media en algún momento.",
              "**Consecuencia 1:** $f' = 0$ en un intervalo $\\Rightarrow f$ constante.",
              "**Consecuencia 2:** $f' = g'$ en un intervalo $\\Rightarrow f = g + C$ (unicidad de la antiderivada salvo constante).",
              "**Próxima lección:** estudiar la **forma** de la gráfica usando $f'$ y $f''$.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-3-4-tvm",
        "title": "Teorema del Valor Medio",
        "description": "Rolle, TVM y sus consecuencias: caracterización de funciones constantes y unicidad de la antiderivada.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 4,
    }


# =====================================================================
# LECCIÓN 3.5 — Forma de la gráfica
# =====================================================================
def lesson_3_5():
    blocks = [
        b("texto", body_md=(
            "Conociendo $f'$ y $f''$, podemos describir con bastante precisión el **comportamiento gráfico** de una función: "
            "dónde **crece o decrece**, dónde tiene **máximos o mínimos locales**, dónde es **cóncava** hacia arriba o hacia abajo, y dónde **cambia de concavidad**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar el **criterio de monotonía**: $f'$ y signo.\n"
            "- Aplicar los **criterios de la primera y segunda derivada** para clasificar críticos.\n"
            "- Determinar **concavidad** y **puntos de inflexión** con $f''$."
        )),

        b("teorema",
          nombre="Criterio de monotonía",
          enunciado_md=(
              "Sea $f$ derivable en un intervalo $I$.\n\n"
              "- Si $f'(x) > 0$ para todo $x \\in I$, entonces $f$ es **estrictamente creciente** en $I$.\n"
              "- Si $f'(x) < 0$ para todo $x \\in I$, entonces $f$ es **estrictamente decreciente** en $I$."
          ),
          demostracion_md=(
              "Sean $a < b$ en $I$. Por TVM, existe $c \\in (a, b)$ con $f(b) - f(a) = f'(c)(b - a)$. Si $f' > 0$, el lado derecho es positivo, así $f(b) > f(a)$. Análogo si $f' < 0$."
          )),

        b("definicion",
          titulo="Criterio de la primera derivada (test de extremos)",
          body_md=(
              "Sea $c$ un punto crítico de $f$, y supongamos que $f$ es continua en $c$ y derivable cerca de $c$ (excepto quizá en $c$).\n\n"
              "- Si $f'$ cambia de **positiva a negativa** en $c$ $\\Rightarrow$ **máximo local** en $c$.\n"
              "- Si $f'$ cambia de **negativa a positiva** en $c$ $\\Rightarrow$ **mínimo local** en $c$.\n"
              "- Si $f'$ **no cambia de signo** en $c$ $\\Rightarrow$ **no hay extremo** (puede ser inflexión).\n\n"
              "**Idea:** si la función pasa de subir a bajar, $c$ es un \"techo\" local. De bajar a subir, un \"piso\" local."
          )),

        b("ejemplo_resuelto",
          titulo="Análisis de $f(x) = x^3 - 3x$",
          problema_md="Determinar intervalos de crecimiento/decrecimiento y clasificar los puntos críticos.",
          pasos=[
              {"accion_md": "**Puntos críticos:** $f'(x) = 3x^2 - 3 = 3(x-1)(x+1) = 0 \\implies x = \\pm 1$.",
               "justificacion_md": "Resolvemos $f'(x) = 0$.",
               "es_resultado": False},
              {"accion_md": "**Signo de $f'$ en cada intervalo:**\n\n- $x < -1$: $f'(-2) = 12 - 3 = 9 > 0$. Creciente.\n- $-1 < x < 1$: $f'(0) = -3 < 0$. Decreciente.\n- $x > 1$: $f'(2) = 12 - 3 = 9 > 0$. Creciente.",
               "justificacion_md": "Probamos un valor representativo en cada intervalo determinado por los críticos.",
               "es_resultado": False},
              {"accion_md": "**Clasificación por primera derivada:**\n\n- En $x = -1$: $f'$ pasa de $+$ a $-$ $\\Rightarrow$ **máximo local**. $f(-1) = -1 + 3 = 2$.\n- En $x = 1$: $f'$ pasa de $-$ a $+$ $\\Rightarrow$ **mínimo local**. $f(1) = 1 - 3 = -2$.",
               "justificacion_md": "El cambio de signo dicta el tipo de extremo.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Concavidad",
          body_md=(
              "Sea $f$ derivable en un intervalo $I$.\n\n"
              "- $f$ es **cóncava hacia arriba** (convexa) en $I$ si $f''(x) > 0$ en todo $I$. La gráfica se curva como una sonrisa $\\smile$.\n"
              "- $f$ es **cóncava hacia abajo** en $I$ si $f''(x) < 0$ en todo $I$. La gráfica se curva como una mueca $\\frown$.\n\n"
              "**Punto de inflexión:** un punto donde $f$ es continua y la concavidad **cambia**."
          )),

        b("intuicion",
          titulo="Concavidad y velocidad de cambio",
          body_md=(
              "$f''$ es la derivada de $f'$, así mide cómo cambia la **pendiente**:\n\n"
              "- $f'' > 0$: la pendiente está **aumentando** — la función se acelera hacia arriba.\n"
              "- $f'' < 0$: la pendiente está **disminuyendo** — la función se desacelera o curva hacia abajo.\n\n"
              "Es por eso que $f''$ describe la concavidad: dice si la curva está \"abriéndose\" o \"cerrándose\"."
          )),

        b("definicion",
          titulo="Criterio de la segunda derivada",
          body_md=(
              "Sea $c$ un punto crítico con $f'(c) = 0$ y $f''(c)$ existe.\n\n"
              "- Si $f''(c) > 0 \\Rightarrow$ **mínimo local** en $c$.\n"
              "- Si $f''(c) < 0 \\Rightarrow$ **máximo local** en $c$.\n"
              "- Si $f''(c) = 0$: **el criterio no decide** (puede ser máximo, mínimo o inflexión).\n\n"
              "Útil cuando calcular $f''$ es fácil. Si falla, hay que recurrir al criterio de la primera derivada."
          )),

        b("ejemplo_resuelto",
          titulo="Concavidad e inflexión de $f(x) = x^4 - 4x^3$",
          problema_md="Determinar intervalos de concavidad y puntos de inflexión.",
          pasos=[
              {"accion_md": "$f'(x) = 4x^3 - 12x^2 = 4x^2(x - 3)$. **Críticos:** $x = 0$ (raíz doble) y $x = 3$.",
               "justificacion_md": "Calculamos también esto para ver la relación con la concavidad.",
               "es_resultado": False},
              {"accion_md": "$f''(x) = 12x^2 - 24x = 12x(x - 2)$. **Se anula en $x = 0$ y $x = 2$.**",
               "justificacion_md": "Posibles puntos de inflexión.",
               "es_resultado": False},
              {"accion_md": "**Signo de $f''$:**\n\n- $x < 0$: $f''(-1) = 12 + 24 = 36 > 0$. Cóncava arriba.\n- $0 < x < 2$: $f''(1) = 12 - 24 = -12 < 0$. Cóncava abajo.\n- $x > 2$: $f''(3) = 108 - 72 = 36 > 0$. Cóncava arriba.",
               "justificacion_md": "Probamos un valor en cada intervalo.",
               "es_resultado": False},
              {"accion_md": "**Inflexiones:** la concavidad cambia en $x = 0$ ($+$ a $-$) y en $x = 2$ ($-$ a $+$). $f(0) = 0$, $f(2) = 16 - 32 = -16$. Inflexiones en $(0, 0)$ y $(2, -16)$.",
               "justificacion_md": "$f''$ pasando por $0$ con cambio de signo confirma la inflexión.",
               "es_resultado": False},
              {"accion_md": "**Clasificar críticos por segunda derivada:**\n\n- $x = 0$: $f''(0) = 0$, no decide. (Por primera derivada se ve que $f'$ no cambia signo en $0$ — es inflexión, no extremo.)\n- $x = 3$: $f''(3) = 36 > 0$, **mínimo local**. $f(3) = 81 - 108 = -27$.",
               "justificacion_md": "Ejemplo donde el criterio de segunda derivada falla en uno y funciona en otro.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los criterios:",
          preguntas=[
              {
                  "enunciado_md": "Si $f'(c) = 0$ y $f''(c) > 0$, entonces en $c$ hay:",
                  "opciones_md": ["Máximo local", "Mínimo local", "Punto de inflexión", "Asíntota"],
                  "correcta": "B",
                  "explicacion_md": (
                      "Criterio de la segunda derivada: $f' = 0$ y $f'' > 0 \\Rightarrow$ mínimo local (la función está cóncava arriba en un crítico — un \"piso\")."
                  ),
              },
              {
                  "enunciado_md": "$f''(x) = 0$ en $c$ garantiza:",
                  "opciones_md": [
                      "Que $c$ es punto de inflexión",
                      "Que la concavidad cambia en $c$",
                      "Que $c$ es **candidato** a punto de inflexión, hay que verificar el cambio de signo de $f''$",
                      "Nada útil",
                  ],
                  "correcta": "C",
                  "explicacion_md": (
                      "$f''(c) = 0$ es necesaria pero no suficiente. Hay que confirmar que $f''$ **cambia de signo** en $c$ para que sea inflexión real (ej.: $f(x) = x^4$ tiene $f''(0) = 0$ pero no inflexión)."
                  ),
              },
          ]),

        fig(
            "Tabla-resumen visual con cuatro combinaciones de signos de f' y f'' representadas con mini-"
            "graficos. Cuadricula 2x2 con tarjetas: (1) f'>0, f''>0: 'creciente y concava arriba' con "
            "mini-curva en teal #06b6d4 tipo y=e^x. (2) f'>0, f''<0: 'creciente y concava abajo' con "
            "mini-curva tipo y=ln(x) en ambar #f59e0b. (3) f'<0, f''<0: 'decreciente y concava abajo' "
            "tipo y=-x^2 en ambar. (4) f'<0, f''>0: 'decreciente y concava arriba' tipo y=1/x en teal. "
            "Cada celda con su mini-grafico y la conclusion. Fondo blanco. " + STYLE
        ),
        ej(
            "Análisis completo de monotonía y concavidad",
            "Para $f(x) = x^3 - 6x^2 + 9x + 1$, determina los intervalos de crecimiento, decrecimiento, concavidad y los extremos locales y puntos de inflexión.",
            [
                "Calcula $f'(x)$, factoriza y construye una tabla de signos.",
                "Repite con $f''(x)$ para concavidad y puntos de inflexión.",
            ],
            "**Paso 1 — Primera derivada.** $f'(x) = 3x^2 - 12x + 9 = 3(x-1)(x-3)$.\n\nCríticos: $x = 1$ y $x = 3$.\n\n**Tabla de signos de $f'$:**\n\n| Intervalo | $(-\\infty, 1)$ | $(1, 3)$ | $(3, +\\infty)$ |\n|---|---|---|---|\n| $f'$ | $+$ | $-$ | $+$ |\n| $f$ | crece | decrece | crece |\n\n→ **Máximo local** en $x = 1$, $f(1) = 5$. **Mínimo local** en $x = 3$, $f(3) = 1$.\n\n**Paso 2 — Segunda derivada.** $f''(x) = 6x - 12 = 6(x - 2)$. Cero en $x = 2$.\n\n**Tabla de signos de $f''$:**\n\n| Intervalo | $(-\\infty, 2)$ | $(2, +\\infty)$ |\n|---|---|---|\n| $f''$ | $-$ | $+$ |\n| concavidad | abajo | arriba |\n\n→ **Punto de inflexión** en $x = 2$, $f(2) = 3$.",
        ),
        ej(
            "Aplicar el criterio de la segunda derivada",
            "Determina si los puntos críticos de $f(x) = x^4 - 4x^3$ son máximos, mínimos o ninguno usando el criterio de la segunda derivada cuando sea posible. Si no aplica, usa el de la primera.",
            [
                "Calcula $f'$ y resuelve $f' = 0$.",
                "Evalúa $f''$ en cada crítico: $f''(c) > 0 \\Rightarrow$ mínimo, $f''(c) < 0 \\Rightarrow$ máximo, $f''(c) = 0 \\Rightarrow$ no decide.",
            ],
            "**Paso 1 — Primera derivada.** $f'(x) = 4x^3 - 12x^2 = 4x^2(x - 3) = 0 \\Rightarrow x = 0$ o $x = 3$.\n\n**Paso 2 — Segunda derivada.** $f''(x) = 12x^2 - 24x = 12x(x - 2)$.\n\n- $f''(3) = 12(3)(1) = 36 > 0 \\Rightarrow$ **mínimo local** en $x = 3$, $f(3) = -27$.\n- $f''(0) = 0 \\Rightarrow$ el criterio **no decide** en $x = 0$.\n\n**Paso 3 — Usar criterio de la primera en $x = 0$.** Cerca de $0$: para $x < 0$, $f'(x) = 4x^2(x-3) > 0$ porque $x^2 > 0$ y $x-3 < 0$... espera: $4x^2 > 0$, $(x-3) < 0$, así $f' < 0$. Para $0 < x < 3$, $f'$ sigue $< 0$. **No hay cambio de signo** en $0$ → **ni máximo ni mínimo** (es solo un punto crítico, con tangente horizontal pero sin extremo).",
        ),

        b("errores_comunes",
          items_md=[
              "**Concluir extremo desde $f'(c) = 0$ sin verificar el cambio de signo.** Recordar: $x^3$ tiene $f'(0) = 0$ pero no extremo.",
              "**Confundir concavidad arriba/abajo.** $f'' > 0$ es cóncava **hacia arriba** (sonrisa). Es la convención estándar.",
              "**Pensar que $f''(c) = 0$ implica inflexión.** Ejemplo: $f(x) = x^4$ tiene $f''(0) = 0$ pero la concavidad no cambia (siempre arriba).",
              "**Aplicar el criterio de la segunda derivada cuando $f''(c) = 0$.** En ese caso no decide; hay que ir a la primera.",
              "**Olvidar que la primera derivada determina monotonía y la segunda determina concavidad** — son dos análisis distintos.",
          ]),

        b("resumen",
          puntos_md=[
              "**Monotonía:** $f' > 0 \\Rightarrow$ creciente; $f' < 0 \\Rightarrow$ decreciente.",
              "**Primera derivada (test de extremos):** $f'$ cambia de $+$ a $-$ $\\Rightarrow$ máximo; de $-$ a $+$ $\\Rightarrow$ mínimo; sin cambio $\\Rightarrow$ no extremo.",
              "**Concavidad:** $f'' > 0$ cóncava arriba; $f'' < 0$ cóncava abajo.",
              "**Inflexión:** punto donde la concavidad cambia (requiere $f''$ pasar por $0$ y cambiar signo).",
              "**Segunda derivada:** $f' = 0$ y $f'' > 0 \\Rightarrow$ mínimo; $f' = 0$ y $f'' < 0 \\Rightarrow$ máximo; $f'' = 0$ no decide.",
              "**Próxima lección:** combinar todo en un procedimiento sistemático para **graficar funciones**.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-3-5-forma",
        "title": "Forma de la gráfica",
        "description": "Análisis con $f'$ (monotonía y extremos) y $f''$ (concavidad e inflexión).",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# LECCIÓN 3.6 — Graficar curvas
# =====================================================================
def lesson_3_6():
    blocks = [
        b("texto", body_md=(
            "Esta lección sintetiza todo lo del capítulo de Límites y de Forma de la gráfica en un **procedimiento sistemático para esbozar funciones**. "
            "No hay teoría nueva: son las herramientas conocidas, aplicadas en el orden correcto.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar la **lista completa de chequeos** (dominio, intersecciones, simetría, asíntotas, $f'$, $f''$).\n"
            "- Esbozar la gráfica con todos los elementos clave correctamente posicionados.\n"
            "- Resolver un caso integrador completo."
        )),

        b("definicion",
          titulo="Procedimiento de 7 pasos",
          body_md=(
              "Para graficar $y = f(x)$:\n\n"
              "**1. Dominio.** Identificar restricciones (denominadores, raíces, $\\ln$).\n\n"
              "**2. Intersecciones.** Con el eje $y$ (evaluar $f(0)$); con el eje $x$ (resolver $f(x) = 0$).\n\n"
              "**3. Simetría.** ¿Par ($f(-x) = f(x)$)? ¿Impar ($f(-x) = -f(x)$)? ¿Periódica?\n\n"
              "**4. Asíntotas.** Verticales (donde el denominador se anula y el numerador no), horizontales ($\\lim_{x \\to \\pm\\infty}$), oblicuas (si el grado del numerador supera al del denominador en uno).\n\n"
              "**5. Análisis de $f'$.** Críticos, intervalos de monotonía, extremos locales.\n\n"
              "**6. Análisis de $f''$.** Concavidad, puntos de inflexión.\n\n"
              "**7. Esbozo.** Ubicar los puntos relevantes y conectar respetando monotonía y concavidad."
          )),

        b("ejemplo_resuelto",
          titulo="Caso integrador: $f(x) = \\dfrac{x^2}{x^2 - 1}$",
          problema_md="Realizar el análisis completo y esbozar la gráfica.",
          pasos=[
              {"accion_md": "**1. Dominio.** $x^2 - 1 = 0 \\implies x = \\pm 1$. Dominio: $\\mathbb{R} \\setminus \\{-1, 1\\}$.",
               "justificacion_md": "El denominador no puede ser $0$.",
               "es_resultado": False},
              {"accion_md": "**2. Intersecciones.** $f(0) = 0$. Intersección con $y$: $(0, 0)$. $f(x) = 0 \\implies x^2 = 0 \\implies x = 0$. Intersección con $x$: $(0, 0)$.",
               "justificacion_md": "Solo el origen.",
               "es_resultado": False},
              {"accion_md": "**3. Simetría.** $f(-x) = \\dfrac{x^2}{x^2 - 1} = f(x)$. **Función par** — simétrica respecto al eje $y$.",
               "justificacion_md": "Solo necesitaremos analizar $x \\geq 0$ y reflejar.",
               "es_resultado": False},
              {"accion_md": "**4. Asíntotas.**\n\n- **Verticales:** en $x = \\pm 1$. Por la izquierda de $1$: $f \\to -\\infty$ (denominador $\\to 0^-$, numerador positivo). Por la derecha: $f \\to +\\infty$. Análogo en $-1$.\n- **Horizontal:** $\\lim_{x \\to \\pm\\infty} \\dfrac{x^2}{x^2-1} = 1$. Asíntota $y = 1$.\n- **Oblicua:** no aplica (los grados son iguales, hay horizontal).",
               "justificacion_md": "Las verticales requieren analizar laterales para los signos.",
               "es_resultado": False},
              {"accion_md": "**5. Análisis de $f'$.** Por la regla del cociente:\n\n$$f'(x) = \\dfrac{2x(x^2-1) - x^2(2x)}{(x^2-1)^2} = \\dfrac{-2x}{(x^2-1)^2}$$\n\n**Crítico:** $x = 0$. **Signo:** $f'(x) > 0$ para $x < 0$ y $f'(x) < 0$ para $x > 0$ (ignorando los puntos donde no está definida).\n\n**Clasificación:** $f$ pasa de creciente a decreciente en $0$ $\\Rightarrow$ **máximo local** $f(0) = 0$.",
               "justificacion_md": "$(x^2 - 1)^2 > 0$ siempre, así el signo lo da $-2x$.",
               "es_resultado": False},
              {"accion_md": "**6. Análisis de $f''$.** Calculando (regla del cociente nuevamente):\n\n$$f''(x) = \\dfrac{6x^2 + 2}{(x^2-1)^3}$$\n\n$6x^2 + 2 > 0$ siempre. El signo de $f''$ es el de $(x^2 - 1)^3$, que es positivo si $|x| > 1$ y negativo si $|x| < 1$.\n\n**Concavidad:**\n\n- $|x| > 1$: $f'' > 0$, cóncava arriba.\n- $|x| < 1$: $f'' < 0$, cóncava abajo.\n\n**Inflexiones:** en $x = \\pm 1$ no — esos puntos no están en el dominio. **No hay inflexiones.**",
               "justificacion_md": "El cambio de concavidad ocurre en las asíntotas, donde $f$ no está definida.",
               "es_resultado": False},
              {"accion_md": "**7. Esbozo.** En $x \\geq 0$:\n\n- Pasa por $(0, 0)$ con tangente horizontal (máximo local).\n- Decrece desde $(0, 0)$ hasta $-\\infty$ al acercarse a $x = 1$ por la izquierda (cóncava abajo).\n- Salta al $+\\infty$ por la derecha de $x = 1$ y decrece hacia la asíntota horizontal $y = 1$ (cóncava arriba).\n\nLa parte $x \\leq 0$ se obtiene reflejando respecto al eje $y$.",
               "justificacion_md": "Reuniendo todo el análisis se obtiene un esbozo cualitativo preciso.",
               "es_resultado": True},
          ]),

        b("grafico_desmos",
          desmos_url="",
          expresiones=[
              "f(x) = x^2/(x^2-1)",
              "y = 1",
              "x = 1",
              "x = -1",
              "(0, 0)",
          ],
          guia_md=(
              "Compara la gráfica de $f$ con las asíntotas $x = \\pm 1$, $y = 1$ y el máximo local en $(0, 0)$. "
              "La rama central, entre las dos verticales, es cóncava hacia abajo y tiene su \"techo\" en el origen. "
              "Las dos ramas exteriores son cóncavas arriba y se acercan a $y = 1$."
          ),
          altura=420),

        b("verificacion",
          intro_md="Verifica el procedimiento:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál de los siguientes pasos NO afecta dónde colocar la gráfica?",
                  "opciones_md": [
                      "Determinar las asíntotas",
                      "Calcular las intersecciones",
                      "Localizar máximos y mínimos",
                      "Calcular la longitud de arco",
                  ],
                  "correcta": "D",
                  "explicacion_md": (
                      "La longitud de arco no aparece en este procedimiento (es un cálculo integral, no de gráfico). Los demás son pasos esenciales."
                  ),
              },
              {
                  "enunciado_md": "Para $f(x) = \\dfrac{1}{x^2 + 1}$, ¿qué tipo de simetría tiene?",
                  "opciones_md": ["Par", "Impar", "Ninguna", "Periódica"],
                  "correcta": "A",
                  "explicacion_md": (
                      "$f(-x) = \\dfrac{1}{(-x)^2 + 1} = \\dfrac{1}{x^2 + 1} = f(x)$. Función **par**."
                  ),
              },
          ]),

        ej(
            "Graficar una racional con asíntotas",
            "Realiza el análisis completo de la función $f(x) = \\dfrac{x^2}{x - 1}$ (dominio, simetría, intersecciones, asíntotas, monotonía, extremos, concavidad) y describe la forma del gráfico.",
            [
                "Comienza por el dominio y las asíntotas verticales/horizontales/oblicuas.",
                "Calcula $f'(x)$ y $f''(x)$ con la regla del cociente.",
            ],
            "**Dominio:** $\\mathbb{R} \\setminus \\{1\\}$.\n\n**Intersecciones:** $f(0) = 0 \\Rightarrow$ pasa por $(0,0)$.\n\n**Asíntotas:** vertical $x = 1$ (denominador cero, numerador no). División larga: $\\dfrac{x^2}{x-1} = x + 1 + \\dfrac{1}{x-1}$ → asíntota oblicua $y = x + 1$.\n\n**Primera derivada:** $f'(x) = \\dfrac{2x(x-1) - x^2}{(x-1)^2} = \\dfrac{x^2 - 2x}{(x-1)^2} = \\dfrac{x(x-2)}{(x-1)^2}$.\n\nCríticos: $x = 0$ y $x = 2$. Signos: $+$ en $(-\\infty, 0)$, $-$ en $(0, 1)$, $-$ en $(1, 2)$, $+$ en $(2, +\\infty)$.\n\n→ **Máximo local** en $x = 0$, $f(0) = 0$. **Mínimo local** en $x = 2$, $f(2) = 4$.\n\n**Segunda derivada:** $f''(x) = \\dfrac{2}{(x-1)^3}$. Signo: negativo si $x < 1$, positivo si $x > 1$. **Concava abajo** en $(-\\infty, 1)$, **arriba** en $(1, +\\infty)$. No hay puntos de inflexión (en $x = 1$ no está definida).\n\n**Forma del gráfico:** dos ramas separadas por $x = 1$. La rama izquierda sube, alcanza máximo en $(0,0)$, baja hasta $-\\infty$ al acercarse a $x = 1^-$. La rama derecha viene de $+\\infty$ al acercarse a $1^+$, baja hasta el mínimo $(2, 4)$ y luego sube hacia la oblicua $y = x + 1$.",
        ),
        ej(
            "Graficar una función exponencial",
            "Analiza y describe la gráfica de $f(x) = x e^{-x}$ (intersecciones, monotonía, extremos, concavidad, asíntotas y comportamiento en el infinito).",
            [
                "Calcula $f'(x)$ usando la regla del producto y observa el signo.",
                "Para $\\lim_{x \\to +\\infty} x e^{-x}$, usa que $e^{-x}$ vence a $x$ (o L'Hôpital).",
            ],
            "**Dominio:** $\\mathbb{R}$.\n\n**Intersecciones:** $f(0) = 0 \\Rightarrow (0, 0)$.\n\n**Comportamiento en infinito:**\n- $\\lim_{x \\to +\\infty} x e^{-x} = 0$ (exponencial vence a polinomio) → **asíntota horizontal $y = 0$ por la derecha**.\n- $\\lim_{x \\to -\\infty} x e^{-x} = -\\infty$ (ambos factores empujan hacia $-\\infty$).\n\n**Primera derivada:** $f'(x) = e^{-x} - x e^{-x} = e^{-x}(1 - x)$. Cero en $x = 1$.\n\n- $f'(x) > 0$ si $x < 1$, $f'(x) < 0$ si $x > 1$. → **Máximo local en $x = 1$**, $f(1) = 1/e \\approx 0{,}368$.\n\n**Segunda derivada:** $f''(x) = -e^{-x}(1 - x) + e^{-x}(-1) = e^{-x}(x - 2)$. Cero en $x = 2$.\n\n- $f'' < 0$ si $x < 2$, $f'' > 0$ si $x > 2$. → **Punto de inflexión** en $x = 2$, $f(2) = 2/e^2 \\approx 0{,}271$.\n\n**Forma:** crece desde $-\\infty$ pasando por el origen, alcanza un máximo en $(1, 1/e)$, decrece y se aproxima asintóticamente a $0^+$ por la derecha; cambia concavidad en $(2, 2/e^2)$.",
        ),

        b("errores_comunes",
          items_md=[
              "**Saltarse el análisis del dominio.** Dejar fuera valores donde la función no existe lleva a interpretar mal asíntotas.",
              "**Olvidar las asíntotas oblicuas** cuando los grados difieren en exactamente uno.",
              "**No verificar el cambio de signo** en candidatos a inflexión.",
              "**Asumir simetría sin verificar.** $f(-x)$ debe ser exactamente $f(x)$ (par) o $-f(x)$ (impar). Otro tipo no hay simetría útil.",
              "**Confundir intersección con asíntota.** Las intersecciones son puntos donde la gráfica corta los ejes; las asíntotas son rectas a las que la gráfica se aproxima.",
          ]),

        b("resumen",
          puntos_md=[
              "**7 pasos:** dominio → intersecciones → simetría → asíntotas → $f'$ (monotonía y extremos) → $f''$ (concavidad e inflexión) → esbozo.",
              "**Simetría par:** $f(-x) = f(x)$, gráfica simétrica al eje $y$.",
              "**Simetría impar:** $f(-x) = -f(x)$, gráfica simétrica al origen.",
              "**Las asíntotas** se ubican antes que el análisis de $f'$ y $f''$ porque acotan el comportamiento global.",
              "**Próxima lección:** optimización — usar todo este aparato para resolver problemas de máximos y mínimos en contextos aplicados.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-3-6-graficar",
        "title": "Graficar curvas",
        "description": "Procedimiento sistemático: dominio, intersecciones, simetría, asíntotas, $f'$, $f''$ y esbozo.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 6,
    }


# =====================================================================
# LECCIÓN 3.7 — Optimización
# =====================================================================
def lesson_3_7():
    blocks = [
        b("texto", body_md=(
            "**Optimizar** significa encontrar el valor extremo (máximo o mínimo) de una cantidad sujeta a ciertas restricciones. "
            "Es la aplicación más práctica del cálculo: minimizar costos, maximizar áreas, encontrar la dosis óptima de un medicamento, etc.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Identificar la **función a optimizar** y las **restricciones**.\n"
            "- Reducir a **una sola variable** usando las restricciones.\n"
            "- Aplicar las herramientas del capítulo (puntos críticos + criterios) para encontrar el extremo y **clasificarlo**.\n"
            "- Verificar las **unidades** y la **factibilidad** de la solución."
        )),

        b("definicion",
          titulo="Procedimiento general de optimización",
          body_md=(
              "**1. Leer y entender el problema.** ¿Qué se quiere maximizar/minimizar? ¿Qué restricciones hay?\n\n"
              "**2. Asignar variables.** Dibujar si ayuda; nombrar cada cantidad relevante.\n\n"
              "**3. Función objetivo.** Escribir la cantidad a optimizar en términos de las variables.\n\n"
              "**4. Restricción.** Usarla para reducir la función objetivo a **una sola variable**.\n\n"
              "**5. Determinar el dominio físicamente válido.**\n\n"
              "**6. Encontrar puntos críticos** y comparar con los **bordes del dominio**.\n\n"
              "**7. Clasificar el extremo** (primera o segunda derivada) y verificar que es del tipo deseado.\n\n"
              "**8. Responder en las unidades originales** del problema."
          )),

        b("ejemplo_resuelto",
          titulo="Cerco rectangular con perímetro fijo",
          problema_md="Se tiene $100$ m de cerco para encerrar un terreno rectangular. ¿Qué dimensiones maximizan el área?",
          pasos=[
              {"accion_md": "**Variables:** $x, y$ los lados. **Restricción:** perímetro $2x + 2y = 100$, así $y = 50 - x$.\n\n**Función objetivo:** $A(x) = xy = x(50 - x) = 50x - x^2$.\n\n**Dominio:** $x \\in (0, 50)$ (lados positivos).",
               "justificacion_md": "Reducimos a una sola variable y acotamos el dominio físicamente.",
               "es_resultado": False},
              {"accion_md": "**Puntos críticos:** $A'(x) = 50 - 2x = 0 \\implies x = 25$.",
               "justificacion_md": "Único crítico interior.",
               "es_resultado": False},
              {"accion_md": "**Clasificamos** con segunda derivada: $A''(x) = -2 < 0 \\Rightarrow$ **máximo**. $A(25) = 25 \\cdot 25 = 625 \\text{ m}^2$.",
               "justificacion_md": "Concavidad hacia abajo confirma el máximo.",
               "es_resultado": False},
              {"accion_md": "**Dimensiones óptimas:** $25 \\times 25$ m. **El terreno óptimo es un cuadrado** con área $625 \\text{ m}^2$.",
               "justificacion_md": "**Resultado clásico:** entre rectángulos con perímetro fijo, el cuadrado maximiza el área. Este principio también aparece en cilindros (esfera ↔ relación volumen/superficie óptima).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caja sin tapa con volumen fijo",
          problema_md="Se quiere construir una caja de base cuadrada y sin tapa con volumen $V = 32 \\text{ m}^3$. ¿Qué dimensiones minimizan el material?",
          pasos=[
              {"accion_md": "**Variables:** $x$ lado de la base, $h$ altura. **Restricción:** $V = x^2 h = 32 \\implies h = \\dfrac{32}{x^2}$.\n\n**Función objetivo (superficie sin tapa):** $S = x^2 + 4xh = x^2 + 4x \\cdot \\dfrac{32}{x^2} = x^2 + \\dfrac{128}{x}$.\n\n**Dominio:** $x \\in (0, \\infty)$.",
               "justificacion_md": "Base $x^2$ + cuatro caras laterales $4 \\cdot xh$. Al sustituir $h$, queda función de una sola variable.",
               "es_resultado": False},
              {"accion_md": "**Puntos críticos:** $S'(x) = 2x - \\dfrac{128}{x^2} = 0 \\implies 2x^3 = 128 \\implies x = 4$.",
               "justificacion_md": "Despejamos $x$ resolviendo $2x^3 = 128$.",
               "es_resultado": False},
              {"accion_md": "**Clasificamos:** $S''(x) = 2 + \\dfrac{256}{x^3}$, evaluado en $x = 4$: $S''(4) = 2 + 4 = 6 > 0 \\Rightarrow$ **mínimo**.",
               "justificacion_md": "El criterio de la segunda derivada confirma el mínimo.",
               "es_resultado": False},
              {"accion_md": "**Dimensiones óptimas:** $x = 4$ m, $h = \\dfrac{32}{16} = 2$ m. **Material mínimo:** $S = 16 + 32 = 48 \\text{ m}^2$.",
               "justificacion_md": "**Observación:** la altura es la mitad del lado de la base — un patrón típico para cajas sin tapa.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Lata cilíndrica con volumen fijo",
          problema_md="Se quiere fabricar una lata cilíndrica con volumen $V = 1$ litro $= 1000 \\text{ cm}^3$. ¿Qué dimensiones minimizan el material?",
          pasos=[
              {"accion_md": "**Variables:** $r$ radio, $h$ altura. **Restricción:** $V = \\pi r^2 h = 1000 \\implies h = \\dfrac{1000}{\\pi r^2}$.\n\n**Función objetivo (superficie total):** $S = 2\\pi r^2 + 2\\pi r h = 2\\pi r^2 + \\dfrac{2000}{r}$.",
               "justificacion_md": "Dos tapas circulares + cara lateral.",
               "es_resultado": False},
              {"accion_md": "**Puntos críticos:** $S'(r) = 4\\pi r - \\dfrac{2000}{r^2} = 0 \\implies r^3 = \\dfrac{500}{\\pi} \\implies r = \\sqrt[3]{500/\\pi}$.",
               "justificacion_md": "Despejamos $r$.",
               "es_resultado": False},
              {"accion_md": "$r \\approx 5.42$ cm. Calculamos $h = \\dfrac{1000}{\\pi r^2} \\approx 10.84$ cm. **Observa:** $h = 2r$.",
               "justificacion_md": "**Resultado clásico:** la lata óptima tiene **altura igual al diámetro**. En la práctica, las latas reales no respetan esto (usan otras restricciones), pero matemáticamente es la forma de menor superficie.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el procedimiento:",
          preguntas=[
              {
                  "enunciado_md": "En un problema de optimización, ¿para qué se usa la restricción?",
                  "opciones_md": [
                      "Para limitar el dominio.",
                      "Para reducir la función objetivo a una sola variable.",
                      "Para clasificar los puntos críticos.",
                      "Para verificar las unidades.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "La restricción enlaza las variables; al despejar una en función de la otra y sustituir, la función objetivo queda de una sola variable, manejable con cálculo de una variable."
                  ),
              },
              {
                  "enunciado_md": "Si $S(x)$ es la superficie y $S'(x_0) = 0$, ¿cuándo $x_0$ minimiza $S$?",
                  "opciones_md": [
                      "Siempre, mientras $S'$ se anule.",
                      "Cuando $S''(x_0) > 0$ (o $S'$ pasa de $-$ a $+$).",
                      "Cuando $S'(x_0) > 0$.",
                      "Nunca.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "$S'(x_0) = 0$ es necesario pero no suficiente. La condición de mínimo se completa con $S''(x_0) > 0$ (criterio de la segunda derivada) o cambio de signo de $S'$ de $-$ a $+$ (criterio de la primera)."
                  ),
              },
          ]),

        fig(
            "Diagrama de problema clasico de optimizacion: una caja abierta (sin tapa) construida a "
            "partir de una lamina rectangular de carton de dimensiones 30 cm por 40 cm. En cada esquina "
            "se recorta un cuadrado de lado x (esquinas marcadas en ambar #f59e0b) y luego se doblan los "
            "lados hacia arriba para formar la caja. Mostrar la lamina plana arriba con cortes y el "
            "resultado tridimensional abajo (caja en perspectiva, aristas teal #06b6d4). Etiquetas: '40', "
            "'30', 'x', 'altura = x', 'base = (40-2x)(30-2x)'. Fondo blanco. " + STYLE
        ),
        ej(
            "Caja de volumen máximo a partir de una lámina",
            "De una lámina rectangular de cartón de $30 \\times 40$ cm se construye una caja **abierta** recortando cuadrados de lado $x$ en las esquinas y plegando los lados. Encuentra el valor de $x$ que **maximiza el volumen** y calcula ese volumen máximo.",
            [
                "Expresa $V(x) = x(30 - 2x)(40 - 2x)$ y determina el dominio físico.",
                "Resuelve $V'(x) = 0$ y verifica con la segunda derivada.",
            ],
            "**Modelo.** $V(x) = x(30 - 2x)(40 - 2x)$. Dominio físico: $x \\in (0, 15)$ (para que las dos dimensiones bases sean positivas).\n\n**Expandir:** $V(x) = x(1200 - 140x + 4x^2) = 4x^3 - 140x^2 + 1200x$.\n\n**Derivar:** $V'(x) = 12x^2 - 280x + 1200$.\n\n**Resolver $V'(x) = 0$:**\n\n$$x = \\dfrac{280 \\pm \\sqrt{280^2 - 4(12)(1200)}}{24} = \\dfrac{280 \\pm \\sqrt{78400 - 57600}}{24} = \\dfrac{280 \\pm \\sqrt{20800}}{24}.$$\n\n$\\sqrt{20800} \\approx 144{,}22$. Soluciones: $x_1 \\approx \\dfrac{280 - 144{,}22}{24} \\approx 5{,}66$ y $x_2 \\approx \\dfrac{280 + 144{,}22}{24} \\approx 17{,}68$.\n\n**Solo $x_1 \\approx 5{,}66$ está en el dominio.**\n\n**Segunda derivada:** $V''(x) = 24x - 280$. En $x_1 \\approx 5{,}66$: $V''(5{,}66) \\approx 135{,}8 - 280 < 0$ → **máximo**. ✓\n\n**Volumen máximo:** $V(5{,}66) \\approx 5{,}66 \\cdot (30 - 11{,}32)(40 - 11{,}32) \\approx 5{,}66 \\cdot 18{,}68 \\cdot 28{,}68 \\approx 3032$ cm³.",
        ),
        ej(
            "Cilindro de volumen fijo y superficie mínima",
            "Una empresa fabrica latas cilíndricas con tapa con un volumen fijo de $V = 1000$ cm³. Encuentra las dimensiones (radio $r$ y altura $h$) que **minimizan la superficie total** de hojalata utilizada.",
            [
                "Función objetivo: $S(r, h) = 2\\pi r^2 + 2\\pi r h$. Restricción: $\\pi r^2 h = 1000$.",
                "Despeja $h$ de la restricción y sustituye en $S$ para reducir a una variable.",
            ],
            "**Paso 1 — Reducir a una variable.** De $\\pi r^2 h = 1000$ obtenemos $h = \\dfrac{1000}{\\pi r^2}$.\n\nSustituyendo en $S$:\n\n$$S(r) = 2\\pi r^2 + 2\\pi r \\cdot \\dfrac{1000}{\\pi r^2} = 2\\pi r^2 + \\dfrac{2000}{r}, \\quad r > 0.$$\n\n**Paso 2 — Derivar.** $S'(r) = 4\\pi r - \\dfrac{2000}{r^2}$.\n\n**Paso 3 — Punto crítico.** $S'(r) = 0 \\Leftrightarrow 4\\pi r = \\dfrac{2000}{r^2} \\Leftrightarrow r^3 = \\dfrac{500}{\\pi}$.\n\n$$r = \\sqrt[3]{\\dfrac{500}{\\pi}} \\approx 5{,}42 \\text{ cm}.$$\n\n**Paso 4 — Confirmar mínimo.** $S''(r) = 4\\pi + \\dfrac{4000}{r^3} > 0$ siempre → mínimo. ✓\n\n**Paso 5 — Altura óptima.** $h = \\dfrac{1000}{\\pi r^2} \\approx \\dfrac{1000}{\\pi (29{,}4)} \\approx 10{,}84$ cm.\n\n**Observación clave:** $h = 2r$ — la lata óptima tiene **altura igual al diámetro**. Es el resultado clásico de minimización de superficie con volumen fijo.",
        ),

        b("errores_comunes",
          items_md=[
              "**No reducir a una variable.** Si la función objetivo queda en dos variables sin usar la restricción, no se puede aplicar el cálculo de una variable.",
              "**Olvidar verificar el dominio físico.** Soluciones matemáticas con dimensiones negativas no son válidas.",
              "**Confundir máximo con mínimo.** Siempre clasificar el extremo encontrado y comprobar que es el tipo pedido.",
              "**No considerar los bordes del dominio** cuando son finitos (por ejemplo, una pieza de lámina con tamaño máximo).",
              "**Reportar la respuesta en la variable intermedia** en vez de en lo que pide el problema. Si piden \"dimensiones\", hay que dar dos números (largo, ancho), no solo uno.",
          ]),

        b("resumen",
          puntos_md=[
              "**Optimizar = encontrar máx/mín de una cantidad bajo restricciones.**",
              "**Procedimiento:** entender → variables → función objetivo → reducir con restricción → dominio → críticos → clasificar → responder con unidades.",
              "**Resultados clásicos:** rectángulo con perímetro fijo $\\rightarrow$ cuadrado; cilindro con volumen fijo $\\rightarrow$ altura igual al diámetro; caja sin tapa con volumen fijo $\\rightarrow$ altura = mitad del lado base.",
              "**Verificar siempre** que el extremo encontrado es del tipo correcto y que está en el dominio físico.",
              "**Cierre del capítulo:** todas las herramientas (TVM, monotonía, concavidad, extremos) confluyen aquí. Es la culminación del Cálculo Diferencial.",
          ]),
    ]
    return {
        "id": "lec-aplicaciones-3-7-optimizacion",
        "title": "Optimización",
        "description": "Maximizar y minimizar cantidades en problemas aplicados. Procedimiento general y casos clásicos.",
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
    course_id = "calculo-diferencial"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Course {course_id} not found.")

    chapter_id = "ch-aplicaciones-derivadas"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Aplicaciones de las Derivadas",
        "description": "Razones relacionadas, aproximaciones, extremos, TVM, forma de la gráfica, graficar curvas y optimización.",
        "order": 3,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_3_1, lesson_3_2, lesson_3_3, lesson_3_4,
        lesson_3_5, lesson_3_6, lesson_3_7,
    ]
    total_blocks = 0
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
        print(f"  ✓ {data['title']} ({len(data['blocks'])} bloques, ~{data['duration_minutes']} min)")

    print()
    print(f"✅ Total: 7 lecciones, {total_blocks} bloques. Capítulo 3 listo.")
    print()
    print("Lecciones disponibles en:")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
