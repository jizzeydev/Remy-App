"""
Seed lesson: 1.1 — Definición y notación de la derivada.
Cubre todos los temas de la guía oficial:
  1. Definición de derivada (gráfica, algebraica, fórmula con `a`)
  2. Recta tangente y pendiente
  3. Derivada como función
  4. Esquinas y discontinuidades
  5. Derivadas de orden superior
  6. Diversas notaciones (Leibniz, Lagrange, Newton, Euler, Parcial)
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


# Inline SVG of |x| for the figura block (no external network).
# Same as before but with cleaner labels.
SVG_ABSOLUTE_VALUE = (
    "data:image/svg+xml;utf8,"
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 480 320' width='480' height='320'>"
    "<rect width='480' height='320' fill='%23ffffff'/>"
    "<line x1='30' y1='270' x2='450' y2='270' stroke='%23475569' stroke-width='1.5'/>"
    "<line x1='240' y1='30' x2='240' y2='290' stroke='%23475569' stroke-width='1.5'/>"
    "<polygon points='450,270 442,266 442,274' fill='%23475569'/>"
    "<polygon points='240,30 236,38 244,38' fill='%23475569'/>"
    "<line x1='60' y1='60' x2='240' y2='270' stroke='%2306b6d4' stroke-width='3'/>"
    "<line x1='240' y1='270' x2='420' y2='60' stroke='%2306b6d4' stroke-width='3'/>"
    "<circle cx='240' cy='270' r='5' fill='%230f172a'/>"
    "<text x='455' y='285' font-family='serif' font-style='italic' font-size='16' fill='%23475569'>x</text>"
    "<text x='250' y='28' font-family='serif' font-style='italic' font-size='16' fill='%23475569'>y</text>"
    "<text x='110' y='150' font-family='serif' font-style='italic' font-size='18' fill='%2306b6d4'>y = |x|</text>"
    "<text x='250' y='298' font-family='sans-serif' font-size='12' fill='%23dc2626'>esquina (no derivable)</text>"
    "</svg>"
)


async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "calculo-diferencial"
    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Course {course_id} not found.")

    # Reset chapters/lessons
    await db.chapters.delete_many({"course_id": course_id})
    await db.lessons.delete_many({})

    chapter_id = "ch-derivadas"
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Derivadas",
        "description": "Definición, notación, reglas de derivación y aplicaciones.",
        "order": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.chapters.insert_one(chapter)

    blocks = [
        # ============ Sección 0: Apertura ============
        b("texto", body_md=(
            "En esta lección vamos a construir el concepto de **derivada** desde su definición rigurosa hasta sus distintas notaciones. "
            "Al terminar, los objetivos son:\n\n"
            "- Calcular derivadas usando las dos fórmulas con límite (la del incremento $h$ y la de $x \\to a$).\n"
            "- Interpretar la derivada como pendiente de la recta tangente.\n"
            "- Comprender la derivada **como función**, no solo como número en un punto.\n"
            "- Reconocer cuándo una función **no es derivable** (esquinas, discontinuidades).\n"
            "- Manejar derivadas de orden superior y las cinco notaciones más usadas en la carrera."
        )),

        b("intuicion",
          titulo="¿Por qué nos importa la derivada?",
          body_md=(
              "Considera un ejemplo concreto: vas en auto y miras el velocímetro. Lo que muestra es la **velocidad instantánea** — qué tan rápido cambia la posición *en ese preciso instante*.\n\n"
              "La velocidad **promedio** entre dos instantes $t_1$ y $t_2$ se calcula con\n\n"
              "$$v_{\\text{prom}} = \\frac{x(t_2) - x(t_1)}{t_2 - t_1}$$\n\n"
              "pero el velocímetro no muestra promedios: muestra el valor en un instante puntual. La derivada es **la generalización matemática** de esa idea — la tasa de cambio cuando el intervalo se hace infinitesimalmente pequeño. La misma idea aparece en economía (tasa marginal), biología (crecimiento de poblaciones), química (velocidad de reacción) y en cualquier modelo donde algo cambie."
          )),

        # ============ Sección 1: Definición ============
        b("definicion",
          titulo="Derivada — interpretación geométrica",
          body_md=(
              "Sea $f$ una función definida en un intervalo abierto que contiene a $a$. La **derivada de $f$ en $a$**, denotada $f'(a)$, es la **pendiente de la recta tangente** a la gráfica de $f$ en el punto $(a, f(a))$.\n\n"
              "Si la curva es suficientemente \"suave\" en $a$, esa pendiente está bien definida y la derivada existe. Si la curva tiene una esquina, un salto, o una tangente vertical, la derivada **no existe** en ese punto."
          )),

        b("grafico_desmos",
          expresiones=[
              "f(x) = x^2",
              "a = 1",
              "h = 1",
              "P_1 = (a, f(a))",
              "P_2 = (a + h, f(a + h))",
              "y = ((f(a+h) - f(a))/h)(x - a) + f(a)",
          ],
          guia_md=(
              "**Mueve el slider $h$** y observa cómo cambia la **recta secante** que pasa por los dos puntos $P_1 = (a, f(a))$ y $P_2 = (a+h, f(a+h))$.\n\n"
              "Cuando $h$ se acerca a $0$, $P_2$ se acerca a $P_1$ y la secante se vuelve **tangente**. Esa pendiente límite es exactamente $f'(a)$. Prueba también con distintos valores de $a$."
          ),
          altura=420),

        b("definicion",
          titulo="Derivada — definición algebraica (con $h$)",
          body_md=(
              "Para hacer la idea anterior precisa, fijamos un punto $a$ y miramos cómo cambia $f$ cuando nos movemos un pequeño incremento $h$ desde $a$. La derivada es:\n\n"
              "$$f'(a) = \\lim_{h \\to 0} \\frac{f(a+h) - f(a)}{h}$$\n\n"
              "siempre que el límite exista. Si existe, decimos que $f$ es **derivable en $a$**. El cociente $\\dfrac{f(a+h)-f(a)}{h}$ se llama **cociente incremental** y representa la pendiente de la recta secante; al tomar $h \\to 0$, obtenemos la pendiente de la tangente."
          )),

        b("definicion",
          titulo="Fórmula equivalente (con $x \\to a$)",
          body_md=(
              "Es muy útil tener una segunda forma equivalente:\n\n"
              "$$f'(a) = \\lim_{x \\to a} \\frac{f(x) - f(a)}{x - a}$$\n\n"
              "Ambas fórmulas dan el mismo valor; conviene **elegir la que resulte más cómoda según el problema**. La primera enfatiza el incremento, la segunda enfatiza el punto al que nos acercamos."
          )),

        b("intuicion",
          titulo="¿Por qué las dos fórmulas son equivalentes?",
          body_md=(
              "Es un cambio de variable. Si en la primera fórmula definimos $x = a + h$, entonces $h = x - a$, y \"$h \\to 0$\" es lo mismo que \"$x \\to a$\". Sustituyendo:\n\n"
              "$$\\lim_{h \\to 0}\\frac{f(a+h)-f(a)}{h} = \\lim_{x \\to a}\\frac{f(x)-f(a)}{x-a}$$\n\n"
              "**Conclusión clave:** ambas fórmulas son la misma idea expresada con distinta variable de límite."
          )),

        b("ejemplo_resuelto",
          titulo="Derivada de $f(x) = x^3$ en $x = 1$",
          problema_md="Calcular $f'(1)$ por definición usando la fórmula del incremento $h$.",
          pasos=[
              {"accion_md": "Aplicamos la definición: $f'(1) = \\lim_{h\\to 0}\\dfrac{f(1+h) - f(1)}{h}$",
               "justificacion_md": "Trabajamos *por definición*, por lo que el primer paso obligatorio es plantear la fórmula. Sin atajos.",
               "es_resultado": False},
              {"accion_md": "Sustituimos $f$: $\\dfrac{(1+h)^3 - 1^3}{h} = \\dfrac{(1+h)^3 - 1}{h}$",
               "justificacion_md": None,
               "es_resultado": False},
              {"accion_md": "Expandimos $(1+h)^3 = 1 + 3h + 3h^2 + h^3$. El numerador queda $3h + 3h^2 + h^3$.",
               "justificacion_md": "Conviene expandir antes de simplificar: el $1$ se cancela y aparece factor común $h$, que es lo que necesitamos para resolver la indeterminación $0/0$.",
               "es_resultado": False},
              {"accion_md": "Factorizamos $h$ y simplificamos: $\\dfrac{h(3 + 3h + h^2)}{h} = 3 + 3h + h^2$",
               "justificacion_md": "La factorización elimina la indeterminación. Ahora podemos evaluar el límite directamente.",
               "es_resultado": False},
              {"accion_md": "$f'(1) = \\lim_{h\\to 0}(3 + 3h + h^2) = 3$",
               "justificacion_md": "La pendiente de la recta tangente a $y = x^3$ en el punto $(1, 1)$ es **3**. Veremos en lecciones siguientes que en general $\\dfrac{d}{dx}(x^n) = nx^{n-1}$ — esta es la *regla de la potencia*.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Antes de avanzar, conviene verificar el manejo de la definición:",
          preguntas=[
              {
                  "enunciado_md": "Para $f(x) = x^2$, ¿qué se obtiene al simplificar $\\dfrac{(3+h)^2 - 9}{h}$?",
                  "opciones_md": ["$h$", "$6 + h$", "$6$", "$h^2 + 6$"],
                  "correcta": "B",
                  "explicacion_md": (
                      "Expandiendo $(3+h)^2 = 9 + 6h + h^2$. El numerador queda $6h + h^2 = h(6 + h)$. "
                      "Al dividir por $h$ se obtiene $6 + h$. Tomando límite cuando $h \\to 0$ se obtiene $f'(3) = 6$. "
                      "La opción $6$ corresponde al límite final, no al valor del cociente antes de tomar el límite."
                  ),
              },
              {
                  "enunciado_md": "¿Cuál afirmación describe correctamente $f'(a)$?",
                  "opciones_md": [
                      "Es el valor de $f$ en el punto $a$.",
                      "Es la pendiente de la recta tangente a $f$ en el punto $(a, f(a))$.",
                      "Es el área bajo la curva de $f$ hasta $a$.",
                      "Es la tasa de cambio promedio de $f$ entre $0$ y $a$.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "$f'(a)$ es la pendiente de la recta tangente — la tasa de cambio **instantánea**, no promedio. "
                      "El \"valor de $f$ en $a$\" es $f(a)$ (sin el apóstrofe). "
                      "El \"área bajo la curva\" corresponde a la integral, no a la derivada — son operaciones inversas."
                  ),
              },
          ]),

        # ============ Sección 2: Recta tangente ============
        b("definicion",
          titulo="Ecuación de la recta tangente",
          body_md=(
              "Si $f$ es derivable en $a$, la **recta tangente** a la gráfica de $f$ en el punto $(a, f(a))$ tiene ecuación:\n\n"
              "$$y - f(a) = f'(a)\\,(x - a)$$\n\n"
              "Es la fórmula **punto-pendiente**: el punto de tangencia es $(a, f(a))$ y la pendiente es $f'(a)$. Equivalentemente, puede escribirse como $y = f'(a)\\,(x - a) + f(a)$."
          )),

        b("ejemplo_resuelto",
          titulo="Recta tangente a $f(x) = x^2$ en $x = 1$",
          problema_md="Encontrar la ecuación de la recta tangente a $f(x) = x^2$ en el punto $x = 1$.",
          pasos=[
              {"accion_md": "Calculamos el punto de tangencia: $f(1) = 1^2 = 1$. Punto: $(1, 1)$.",
               "justificacion_md": "Necesitamos un punto y una pendiente para determinar la recta.",
               "es_resultado": False},
              {"accion_md": "Calculamos $f'(1)$ por definición: $\\lim_{h\\to 0}\\dfrac{(1+h)^2 - 1}{h} = \\lim_{h\\to 0}(2 + h) = 2$.",
               "justificacion_md": "Mismo procedimiento que en el ejemplo anterior. Resultado: $f'(1) = 2$.",
               "es_resultado": False},
              {"accion_md": "Aplicamos punto-pendiente: $y - 1 = 2(x - 1)$",
               "justificacion_md": "Sustituimos $a = 1$, $f(a) = 1$, $f'(a) = 2$ en la fórmula.",
               "es_resultado": False},
              {"accion_md": "Despejamos: $y = 2x - 1$",
               "justificacion_md": "Forma explícita de la recta tangente. En $x = 1$ pasa por $(1,1)$ y crece con pendiente $2$.",
               "es_resultado": True},
          ]),

        b("grafico_desmos",
          expresiones=[
              "g(x) = x^2",
              "y = 2x - 1",
              "(1, 1)",
          ],
          guia_md=(
              "Verificación visual: la recta $y = 2x - 1$ toca la parábola $y = x^2$ exactamente en $(1, 1)$ y tiene la misma pendiente que la curva en ese punto. **Haz zoom** cerca del punto para observar que la recta y la parábola se confunden en una vecindad pequeña — esa es la idea de \"linealización local\"."
          ),
          altura=400),

        # ============ Sección 3: Derivada como función ============
        b("definicion",
          titulo="La derivada como función",
          body_md=(
              "Hasta ahora calculamos $f'(a)$ — un *número* asociado a un punto específico $a$. Pero si la derivada existe en cada punto $x$ del dominio (o de un subdominio), podemos pensar en una **función derivada** $f': x \\mapsto f'(x)$:\n\n"
              "$$f'(x) = \\lim_{h \\to 0}\\frac{f(x+h) - f(x)}{h}$$\n\n"
              "Es la misma fórmula, pero en lugar de fijar el punto, **dejamos $x$ libre**. El resultado es una nueva función que asigna a cada $x$ la pendiente de la tangente en ese punto."
          )),

        b("ejemplo_resuelto",
          titulo="Derivada de $f(x) = \\dfrac{1}{x}$",
          problema_md="Calcular $f'(x)$ por definición para $f(x) = \\dfrac{1}{x}$, con $x \\neq 0$.",
          pasos=[
              {"accion_md": "Cociente incremental: $\\dfrac{f(x+h) - f(x)}{h} = \\dfrac{1}{h}\\left(\\dfrac{1}{x+h} - \\dfrac{1}{x}\\right)$",
               "justificacion_md": "Aplicamos la definición. La diferencia de fracciones se simplifica al sacar denominador común.",
               "es_resultado": False},
              {"accion_md": "Operamos la diferencia: $\\dfrac{1}{x+h} - \\dfrac{1}{x} = \\dfrac{x - (x+h)}{x(x+h)} = \\dfrac{-h}{x(x+h)}$",
               "justificacion_md": "Denominador común $x(x+h)$. El numerador se cancela parcialmente y aparece $-h$ — exactamente el factor necesario para resolver la indeterminación.",
               "es_resultado": False},
              {"accion_md": "Sustituyendo: $\\dfrac{1}{h} \\cdot \\dfrac{-h}{x(x+h)} = \\dfrac{-1}{x(x+h)}$",
               "justificacion_md": "Se cancela el $h$ que estaba indeterminado.",
               "es_resultado": False},
              {"accion_md": "Tomando el límite: $f'(x) = \\lim_{h\\to 0}\\dfrac{-1}{x(x+h)} = \\dfrac{-1}{x \\cdot x} = -\\dfrac{1}{x^2}$",
               "justificacion_md": "La función derivada de $1/x$ es $-1/x^2$. Observación: el dominio sigue siendo $x \\neq 0$ — la derivada no \"arregla\" puntos donde $f$ no está definida.",
               "es_resultado": True},
          ]),

        # ============ Sección 4: Esquinas y discontinuidades ============
        b("intuicion",
          titulo="¿Cuándo NO hay derivada?",
          body_md=(
              "Una función puede ser **continua** y aun así no tener derivada en un punto. Los tres casos típicos son:\n\n"
              "- **Esquinas** (puntos angulosos): la pendiente cambia bruscamente. Las derivadas laterales existen pero son distintas.\n"
              "- **Tangentes verticales**: la \"pendiente\" sería infinita, así que el límite del cociente incremental no existe (en el sentido finito).\n"
              "- **Discontinuidades** (saltos, agujeros): si $f$ no es continua en $a$, no puede ser derivable en $a$.\n\n"
              "El recíproco es importante: **derivable $\\Rightarrow$ continua**, pero **continua $\\not\\Rightarrow$ derivable**. El ejemplo canónico es $f(x) = |x|$."
          )),

        b("figura",
          image_url=SVG_ABSOLUTE_VALUE,
          caption_md=(
              "La función $f(x) = |x|$ es **continua** en todo $\\mathbb{R}$ pero **no derivable en $x = 0$**. "
              "La gráfica forma una *esquina* donde la pendiente cambia bruscamente de $-1$ a $+1$."
          ),
          prompt_image_md=(
              "Gráfico matemático limpio y didáctico estilo libro de texto universitario que muestre la función f(x) = |x|. "
              "Ejes cartesianos en gris oscuro con flechas en los extremos positivos. La función dibujada en color cyan/turquesa "
              "(#06b6d4) con grosor visible (~3-4px), formando una V perfecta con vértice en el origen. "
              "Marcar el origen (0,0) con un círculo lleno negro. Etiquetar los ejes con 'x' (horizontal) e 'y' (vertical) en cursiva. "
              "Incluir el texto 'y = |x|' cerca de una de las ramas. Agregar una flecha pequeña apuntando al vértice con el texto "
              "'esquina (no derivable)' en color rojo. Fondo blanco, sin grilla, estilo minimalista, formato apaisado 4:3."
          )),

        b("ejemplo_resuelto",
          titulo="¿Por qué $|x|$ no es derivable en $0$?",
          problema_md="Demostrar rigurosamente que $f(x) = |x|$ no admite derivada en $x = 0$ calculando las derivadas laterales.",
          pasos=[
              {"accion_md": "Por la **derecha** ($h > 0$): $\\lim_{h \\to 0^+}\\dfrac{|0+h| - |0|}{h} = \\lim_{h \\to 0^+}\\dfrac{h}{h} = 1$",
               "justificacion_md": "Para $h > 0$, $|h| = h$, por lo que el cociente vale $1$ constantemente.",
               "es_resultado": False},
              {"accion_md": "Por la **izquierda** ($h < 0$): $\\lim_{h \\to 0^-}\\dfrac{|0+h| - |0|}{h} = \\lim_{h \\to 0^-}\\dfrac{-h}{h} = -1$",
               "justificacion_md": "Para $h < 0$, $|h| = -h$, por lo que el cociente vale $-1$ constantemente.",
               "es_resultado": False},
              {"accion_md": "Las derivadas laterales son **distintas** ($1 \\neq -1$), por lo tanto el límite bilateral $\\lim_{h\\to 0}\\dfrac{|h|}{h}$ **no existe** y $f'(0)$ no está definida.",
               "justificacion_md": "Para que un límite exista, los límites laterales deben coincidir. En este caso no lo hacen — eso es exactamente lo que ocurre en una esquina.",
               "es_resultado": True},
          ]),

        b("errores_comunes",
          items_md=[
              "**Continua no implica derivable.** $|x|$ es el contraejemplo canónico: continua en $\\mathbb{R}$, no derivable en $0$.",
              "**Derivable sí implica continua.** Si $f$ no es continua en $a$, no tiene sentido buscar $f'(a)$: no existe.",
              "**No confundir $\\dfrac{f(a) - f(a)}{a - a}$ con la derivada.** Eso es $\\dfrac{0}{0}$ — indeterminado. La derivada es el **límite**, no el valor del cociente en el punto.",
              "**$f'(x)$ y $f(x)'$ no significan lo mismo.** $f'(x)$ es la función derivada evaluada en $x$. $f(x)'$ no tiene sentido — la derivada se aplica a la función, no a un valor numérico.",
          ]),

        # ============ Sección 5: Derivadas de orden superior ============
        b("definicion",
          titulo="Derivadas de orden superior",
          body_md=(
              "Si $f'$ es a su vez derivable, podemos derivarla y obtener la **segunda derivada** $f''$, denotada también como $f^{(2)}$. En general, la **$n$-ésima derivada** $f^{(n)}$ se define recursivamente:\n\n"
              "$$f^{(n)}(x) = \\frac{d}{dx}\\left[f^{(n-1)}(x)\\right]$$\n\n"
              "con $f^{(0)} = f$ por convención. La segunda derivada describe la **curvatura** o **concavidad** de la función; las de orden superior aparecen en series de Taylor, ecuaciones diferenciales y muchas aplicaciones físicas."
          )),

        b("ejemplo_resuelto",
          titulo="Tercera derivada de $f(x) = x^3$",
          problema_md="Calcular $f'(x)$, $f''(x)$ y $f'''(x)$ para $f(x) = x^3$.",
          pasos=[
              {"accion_md": "$f'(x) = 3x^2$",
               "justificacion_md": "Aplicando la regla de la potencia (validada por definición más arriba para $a=1$): $\\dfrac{d}{dx}(x^n) = nx^{n-1}$.",
               "es_resultado": False},
              {"accion_md": "$f''(x) = \\dfrac{d}{dx}(3x^2) = 6x$",
               "justificacion_md": "Se deriva $f'$. Por linealidad se saca la constante: $3 \\cdot 2x = 6x$.",
               "es_resultado": False},
              {"accion_md": "$f'''(x) = \\dfrac{d}{dx}(6x) = 6$",
               "justificacion_md": "La derivada de una función lineal $cx$ es la constante $c$.",
               "es_resultado": False},
              {"accion_md": "$f^{(4)}(x) = 0$ y $f^{(n)}(x) = 0$ para todo $n \\geq 4$",
               "justificacion_md": "La derivada de una constante es cero. **Conclusión:** un polinomio de grado $n$ tiene derivadas no nulas hasta el orden $n$, y de orden $n+1$ en adelante son todas idénticamente cero.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Interpretación física de las derivadas sucesivas",
          body_md=(
              "Si $x(t)$ representa la **posición** de un objeto en función del tiempo, entonces:\n\n"
              "- $x'(t) = v(t)$ es la **velocidad** (tasa de cambio de la posición).\n"
              "- $x''(t) = a(t)$ es la **aceleración** (tasa de cambio de la velocidad).\n"
              "- $x'''(t)$ es el **jerk** o tirón (tasa de cambio de la aceleración) — relevante en ingeniería automotriz y montaje de cámaras.\n\n"
              "Las derivadas sucesivas no son una abstracción: cada orden mide cómo cambia el orden anterior."
          )),

        # ============ Sección 6: Notaciones ============
        b("texto", body_md=(
            "## Notaciones para la derivada\n\n"
            "Distintas comunidades matemáticas usan **distintas notaciones** para escribir la misma idea. Las cinco siguientes aparecen a lo largo de la carrera; conviene reconocerlas todas."
        )),

        b("definicion",
          titulo="Leibniz — $\\dfrac{dy}{dx}$",
          body_md=(
              "Si $y = f(x)$, escribimos\n\n"
              "$$\\frac{dy}{dx} \\quad \\text{o equivalentemente} \\quad \\frac{df}{dx}$$\n\n"
              "Para derivadas de orden superior: $\\dfrac{d^2y}{dx^2}$, $\\dfrac{d^3y}{dx^3}$, etc.\n\n"
              "**Cuándo se usa:** en cálculo introductorio, integración, regla de la cadena (donde la cancelación visual de \"diferenciales\" la hace muy intuitiva). Es la notación más informativa porque deja explícita **cuál es la variable independiente** respecto a la cual se deriva."
          )),

        b("definicion",
          titulo="Lagrange — $f'(x)$",
          body_md=(
              "La más compacta: usa apóstrofes ($'$) para indicar el orden:\n\n"
              "$$f'(x), \\quad f''(x), \\quad f'''(x), \\quad f^{(n)}(x)$$\n\n"
              "Para órdenes mayores que tres se prefiere $f^{(n)}(x)$ para evitar contar apóstrofes.\n\n"
              "**Cuándo se usa:** es la notación estándar en análisis matemático y la más común en libros de texto de cálculo de una variable."
          )),

        b("definicion",
          titulo="Newton — $\\dot{f}(t)$",
          body_md=(
              "Usa puntos sobre la función para indicar derivada **respecto al tiempo**:\n\n"
              "$$\\dot{x}(t) = \\text{velocidad}, \\quad \\ddot{x}(t) = \\text{aceleración}$$\n\n"
              "**Cuándo se usa:** en física y mecánica clásica. La convención implícita es que la variable independiente es el tiempo $t$. Aparece menos en matemática pura."
          )),

        b("definicion",
          titulo="Euler — $Df$ o $D_x f$",
          body_md=(
              "Trata la derivada como un **operador** $D$ que actúa sobre funciones:\n\n"
              "$$Df = f', \\quad D^2 f = f'', \\quad D_x f = \\frac{df}{dx}$$\n\n"
              "**Cuándo se usa:** en ecuaciones diferenciales y álgebra de operadores diferenciales. Permite escribir cosas como $(D^2 + 3D + 2)y = 0$ para representar la ecuación $y'' + 3y' + 2y = 0$."
          )),

        b("definicion",
          titulo="Derivada parcial — $\\dfrac{\\partial f}{\\partial x}$",
          body_md=(
              "Cuando $f$ depende de varias variables, $f(x, y, z, \\ldots)$, escribimos\n\n"
              "$$\\frac{\\partial f}{\\partial x}$$\n\n"
              "para indicar la derivada respecto a $x$ **manteniendo las demás variables constantes**. El símbolo $\\partial$ (\"d redondeada\") avisa al lector que estamos en contexto multivariable.\n\n"
              "**Cuándo se usa:** cálculo en varias variables, gradientes, ecuaciones en derivadas parciales (PDEs). En este curso introductorio no se usará, pero aparecerá muy pronto."
          )),

        b("verificacion",
          intro_md="Verifica que reconoces las notaciones:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál de estas expresiones representa la **segunda derivada** de $f$ respecto a $x$?",
                  "opciones_md": ["$\\dfrac{df}{dx}$", "$\\dfrac{d^2f}{dx^2}$", "$f'(x)$", "$\\dfrac{\\partial f}{\\partial x}$"],
                  "correcta": "B",
                  "explicacion_md": "$\\dfrac{d^2f}{dx^2}$ es la notación de Leibniz para la segunda derivada. La opción $f'(x)$ es Lagrange para la **primera** derivada. $\\dfrac{\\partial f}{\\partial x}$ es la primera derivada parcial (multivariable).",
              },
              {
                  "enunciado_md": "Si $\\dot{x}(t)$ representa la velocidad y $\\ddot{x}(t)$ la aceleración, esta es notación de:",
                  "opciones_md": ["Leibniz", "Lagrange", "Newton", "Euler"],
                  "correcta": "C",
                  "explicacion_md": "Los puntos encima de la función son la marca de la notación de **Newton**, usada principalmente en física para indicar derivadas respecto al tiempo.",
              },
          ]),

        # ============ Cierre ============
        b("resumen",
          puntos_md=[
              "**Definición:** $f'(a) = \\lim_{h\\to 0}\\dfrac{f(a+h)-f(a)}{h} = \\lim_{x\\to a}\\dfrac{f(x)-f(a)}{x-a}$ (las dos fórmulas son equivalentes vía cambio de variable).",
              "**Geometría:** $f'(a)$ es la pendiente de la recta tangente a la gráfica de $f$ en $(a, f(a))$. Ecuación: $y - f(a) = f'(a)(x-a)$.",
              "**Función derivada:** dejando $x$ libre, $f'(x)$ es una nueva función que asigna a cada punto su pendiente.",
              "**Cuándo no existe:** esquinas ($|x|$ en $0$), tangentes verticales, discontinuidades. Recuerda: **derivable $\\Rightarrow$ continua**, recíproco falso.",
              "**Orden superior:** $f''$, $f'''$, $f^{(n)}$ son derivadas de derivadas. Físicamente: posición → velocidad → aceleración → jerk.",
              "**Notaciones:** Leibniz $\\dfrac{dy}{dx}$, Lagrange $f'(x)$, Newton $\\dot{f}(t)$, Euler $Df$, parcial $\\dfrac{\\partial f}{\\partial x}$. Mismas ideas, distintos contextos.",
              "**Próxima lección:** reglas de derivación que evitan calcular el límite cada vez (regla de la potencia, suma, producto, cociente, cadena).",
          ]),
    ]

    lesson_id = "lesson-definicion-y-notacion"
    lesson = {
        "id": lesson_id,
        "chapter_id": chapter_id,
        "title": "Definición y notación de la derivada",
        "description": "Definición gráfica y algebraica, recta tangente, derivada como función, esquinas y discontinuidades, derivadas de orden superior, y las cinco notaciones estándar.",
        "blocks": blocks,
        "order": 1,
        "duration_minutes": 45,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.lessons.insert_one(lesson)

    # Counts per block type, for sanity check
    from collections import Counter
    counts = Counter(blk['type'] for blk in blocks)

    print(f"✅ Chapter: '{chapter['title']}'")
    print(f"✅ Lesson:  '{lesson['title']}' ({len(blocks)} blocks, ~{lesson['duration_minutes']} min)")
    print()
    print("Distribución de bloques:")
    for t, n in counts.most_common():
        print(f"  {t}: {n}")
    print()
    print(f"View at: http://localhost:3007/lesson/{lesson_id}")


if __name__ == "__main__":
    asyncio.run(main())
