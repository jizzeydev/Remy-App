"""
Seed del Capítulo 1 — Límites y Continuidad (curso Cálculo Diferencial).
7 lecciones que cubren todo el contenido de las guías oficiales:
  1.1 Introducción intuitiva
  1.2 Definición formal (epsilon-delta)
  1.3 Propiedades de los límites
  1.4 Continuidad de funciones
  1.5 Teorema del Valor Intermedio
  1.6 Asíntotas
  1.7 Resolver límites

Idempotente: borra y re-inserta el capítulo y sus lecciones.
Preserva el capítulo de Derivadas si existe (lo reordena a order=2).
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


# =====================================================================
# LECCIÓN 1.1 — Introducción intuitiva
# =====================================================================
def lesson_1_1():
    blocks = [
        b("texto", body_md=(
            "El concepto de **límite** es la base sobre la que se construye todo el cálculo. "
            "Antes de la definición formal, en esta primera lección vamos a entenderlo de forma intuitiva: a través de tablas numéricas, gráficos y casos típicos.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Comprender qué significa $\\lim_{x \\to a} f(x) = L$ desde una perspectiva numérica y gráfica.\n"
            "- Calcular límites por aproximación (tabla de valores).\n"
            "- Distinguir **límites laterales** y reconocer cuándo el límite bilateral existe.\n"
            "- Reconocer **límites infinitos** y los **límites notables** que aparecen en todo el curso."
        )),

        b("intuicion",
          titulo="¿Qué problema resuelve el límite?",
          body_md=(
              "Considera la función $f(x) = \\dfrac{x^2 - 1}{x - 1}$. Evaluarla en $x = 1$ es imposible: el denominador se hace cero y la fracción no está definida. Sin embargo, podemos preguntar algo más sutil:\n\n"
              "> ¿A qué valor se acerca $f(x)$ cuando $x$ se acerca a $1$, sin necesariamente llegar a $1$?\n\n"
              "Esa pregunta — **el comportamiento de la función cerca de un punto, sin pasar por el punto** — es exactamente lo que captura el concepto de límite."
          )),

        b("definicion",
          titulo="Notación informal del límite",
          body_md=(
              "Cuando $f(x)$ se aproxima a un valor $L$ a medida que $x$ se aproxima a $a$ (sin necesariamente igualarlo), escribimos:\n\n"
              "$$\\lim_{x \\to a} f(x) = L$$\n\n"
              "Esta es la **notación informal**: la idea intuitiva. En la próxima lección veremos la definición rigurosa con $\\epsilon$ y $\\delta$ que precisa qué significa \"aproximarse\"."
          )),

        b("ejemplo_resuelto",
          titulo="Aproximación numérica de $\\dfrac{x^2 - 1}{x - 1}$ en $x = 1$",
          problema_md="Conjeturar el valor de $\\lim_{x \\to 1} \\dfrac{x^2 - 1}{x - 1}$ evaluando $f$ en valores cercanos a $1$.",
          pasos=[
              {"accion_md": "Construimos una tabla con valores de $x$ acercándose a $1$ por ambos lados:\n\n| $x$ | $f(x)$ |\n|---|---|\n| 0.9 | 1.9 |\n| 0.99 | 1.99 |\n| 0.999 | 1.999 |\n| 1.001 | 2.001 |\n| 1.01 | 2.01 |\n| 1.1 | 2.1 |",
               "justificacion_md": "Tomamos valores de $x$ a izquierda ($0.9, 0.99, 0.999$) y derecha ($1.001, 1.01, 1.1$) de $1$ para ver hacia dónde tiende $f(x)$ desde ambas direcciones.",
               "es_resultado": False},
              {"accion_md": "Observamos que cuando $x \\to 1$, los valores de $f(x)$ se acercan a $2$ desde ambos lados.",
               "justificacion_md": "Es la conjetura que la tabla nos sugiere. Aún no lo hemos demostrado: en lecciones siguientes lo confirmaremos algebraicamente factorizando $x^2 - 1 = (x-1)(x+1)$.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{x \\to 1} \\dfrac{x^2 - 1}{x - 1} = 2$",
               "justificacion_md": "El valor del límite existe y vale $2$, **a pesar de que $f(1)$ no está definida**. Este es uno de los puntos centrales del concepto: el límite habla del comportamiento *cerca de* $a$, no *en* $a$.",
               "es_resultado": True},
          ]),

        b("grafico_desmos",
          expresiones=[
              "f(x) = (x^2 - 1)/(x - 1) \\{x \\neq 1\\}",
              "(1, 2)",
          ],
          guia_md=(
              "Observa cómo la gráfica es **una línea recta** $y = x + 1$ con un **agujero** (círculo abierto) en el punto $(1, 2)$. "
              "Ese agujero refleja que $f(1)$ no está definida, pero la curva *se acerca* a $y = 2$ desde ambos lados — exactamente lo que la tabla numérica anticipó."
          ),
          altura=380),

        b("definicion",
          titulo="Límites laterales",
          body_md=(
              "Para distinguir el comportamiento *desde la izquierda* y *desde la derecha*, definimos los **límites laterales**:\n\n"
              "$$\\lim_{x \\to a^-} f(x) = L_1 \\quad \\text{(límite por la izquierda)}$$\n\n"
              "$$\\lim_{x \\to a^+} f(x) = L_2 \\quad \\text{(límite por la derecha)}$$\n\n"
              "El símbolo $a^-$ indica que $x$ se aproxima a $a$ con valores menores ($x < a$), y $a^+$ con valores mayores ($x > a$)."
          )),

        b("teorema",
          nombre="Existencia del límite (criterio de los laterales)",
          hipotesis=[
              "Los límites laterales $\\lim_{x \\to a^-} f(x)$ y $\\lim_{x \\to a^+} f(x)$ existen.",
          ],
          enunciado_md=(
              "$\\lim_{x \\to a} f(x)$ existe **si y solo si** los dos límites laterales coinciden:\n\n"
              "$$\\lim_{x \\to a^-} f(x) = \\lim_{x \\to a^+} f(x) = L$$\n\n"
              "En tal caso, $\\lim_{x \\to a} f(x) = L$. Si los laterales son distintos, **el límite bilateral no existe**."
          )),

        b("ejemplo_resuelto",
          titulo="Función a trozos: ¿existe el límite?",
          problema_md=(
              "Sea $f(x) = \\begin{cases} x + 1 & \\text{si } x < 2 \\\\ x^2 - 2 & \\text{si } x > 2 \\end{cases}$. "
              "Determinar si existe $\\lim_{x \\to 2} f(x)$."
          ),
          pasos=[
              {"accion_md": "Calculamos el límite por la izquierda. Para $x < 2$, $f(x) = x+1$:\n\n$$\\lim_{x \\to 2^-} f(x) = \\lim_{x \\to 2^-} (x + 1) = 2 + 1 = 3$$",
               "justificacion_md": "Por la izquierda usamos la rama válida en ese lado: $x + 1$.",
               "es_resultado": False},
              {"accion_md": "Calculamos el límite por la derecha. Para $x > 2$, $f(x) = x^2 - 2$:\n\n$$\\lim_{x \\to 2^+} f(x) = \\lim_{x \\to 2^+} (x^2 - 2) = 4 - 2 = 2$$",
               "justificacion_md": "Por la derecha usamos la otra rama: $x^2 - 2$ evaluada en valores cercanos a $2$.",
               "es_resultado": False},
              {"accion_md": "Como $\\lim_{x \\to 2^-} f(x) = 3 \\neq 2 = \\lim_{x \\to 2^+} f(x)$, **el límite bilateral no existe**.",
               "justificacion_md": "El criterio del teorema falla: los laterales no coinciden. La función tiene un *salto* en $x = 2$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Un caso $0/0$ que sí tiene límite: $\\lim_{t \\to 0} \\dfrac{\\sqrt{t^2 + 9} - 3}{t^2}$",
          problema_md="Calcular $\\lim_{t \\to 0} \\dfrac{\\sqrt{t^2 + 9} - 3}{t^2}$.",
          pasos=[
              {"accion_md": "Evaluar directamente en $t = 0$ produce $\\dfrac{\\sqrt{9} - 3}{0} = \\dfrac{0}{0}$, indeterminación.",
               "justificacion_md": "$0/0$ no significa que el límite no exista: significa que necesitamos otra técnica para resolverlo.",
               "es_resultado": False},
              {"accion_md": "Multiplicamos numerador y denominador por el **conjugado** $\\sqrt{t^2 + 9} + 3$:\n\n$$\\dfrac{(\\sqrt{t^2+9}-3)(\\sqrt{t^2+9}+3)}{t^2(\\sqrt{t^2+9}+3)} = \\dfrac{(t^2+9) - 9}{t^2(\\sqrt{t^2+9}+3)} = \\dfrac{t^2}{t^2(\\sqrt{t^2+9}+3)}$$",
               "justificacion_md": "La técnica de **racionalización** elimina la raíz del numerador usando la identidad $(a-b)(a+b) = a^2 - b^2$. Genera el factor $t^2$ que va a cancelar la indeterminación.",
               "es_resultado": False},
              {"accion_md": "Simplificamos cancelando $t^2$:\n\n$$\\dfrac{1}{\\sqrt{t^2+9}+3}$$",
               "justificacion_md": "La cancelación es válida porque trabajamos con $t \\neq 0$ (el límite no se preocupa por $t = 0$).",
               "es_resultado": False},
              {"accion_md": "Ahora la sustitución directa funciona:\n\n$$\\lim_{t \\to 0} \\dfrac{1}{\\sqrt{t^2+9}+3} = \\dfrac{1}{\\sqrt{9}+3} = \\dfrac{1}{6}$$",
               "justificacion_md": "El resultado es $\\dfrac{1}{6}$. Notemos que el límite existe perfectamente, aunque la función original no estuviera definida en $t = 0$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Antes de avanzar a límites infinitos, verifiquemos los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\lim_{x \\to 3^-} f(x) = 5$ y $\\lim_{x \\to 3^+} f(x) = 5$, ¿qué se concluye?",
                  "opciones_md": [
                      "$f(3) = 5$",
                      "$\\lim_{x \\to 3} f(x) = 5$",
                      "$f$ es continua en $3$",
                      "El límite no existe porque la función podría no estar definida en $3$",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Por el criterio de los laterales, si ambos coinciden, el límite bilateral existe y vale ese valor común. "
                      "**No** podemos concluir que $f(3) = 5$ ni que sea continua: el límite habla del comportamiento *cerca* de $3$, no *en* $3$. "
                      "La función podría no estar definida en $3$ y aun así tener límite igual a $5$."
                  ),
              },
              {
                  "enunciado_md": "¿Cuál es el valor de $\\lim_{x \\to 2} \\dfrac{x^2 - 4}{x - 2}$?",
                  "opciones_md": ["No existe (indeterminación $0/0$)", "$0$", "$4$", "$2$"],
                  "correcta": "C",
                  "explicacion_md": (
                      "Aunque la sustitución directa da $0/0$, factorizamos: $\\dfrac{x^2-4}{x-2} = \\dfrac{(x-2)(x+2)}{x-2} = x + 2$ para $x \\neq 2$. "
                      "Tomando límite: $\\lim_{x \\to 2}(x+2) = 4$. La opción A es un error frecuente: $0/0$ es indeterminación, no \"no existe\"."
                  ),
              },
          ]),

        b("definicion",
          titulo="Límites infinitos",
          body_md=(
              "A veces, cuando $x \\to a$, los valores de $f(x)$ crecen sin cota o decrecen sin cota. En esos casos escribimos:\n\n"
              "$$\\lim_{x \\to a} f(x) = +\\infty \\quad \\text{o} \\quad \\lim_{x \\to a} f(x) = -\\infty$$\n\n"
              "**Importante:** $\\infty$ no es un número real. Esta notación es una forma compacta de decir \"$f(x)$ no se acerca a ningún valor finito; en cambio, crece o decrece sin límite\". En sentido estricto, el límite **no existe** como número real, pero la notación captura información útil sobre el comportamiento."
          )),

        b("ejemplo_resuelto",
          titulo="$\\lim_{x \\to 0} \\dfrac{1}{x^2}$",
          problema_md="Analizar el comportamiento de $\\dfrac{1}{x^2}$ cuando $x \\to 0$.",
          pasos=[
              {"accion_md": "Por la **derecha**: cuando $x \\to 0^+$, $x^2 \\to 0^+$ con valores muy pequeños y positivos. Entonces $\\dfrac{1}{x^2}$ crece sin cota.",
               "justificacion_md": "Por ejemplo: $x = 0.1 \\Rightarrow 1/x^2 = 100$; $x = 0.01 \\Rightarrow 1/x^2 = 10000$.",
               "es_resultado": False},
              {"accion_md": "Por la **izquierda**: cuando $x \\to 0^-$, $x^2$ es nuevamente pequeño y **positivo** (porque $x^2 \\geq 0$ siempre). Entonces $\\dfrac{1}{x^2} \\to +\\infty$ también.",
               "justificacion_md": "El cuadrado elimina el signo: tanto $x = 0.1$ como $x = -0.1$ dan $x^2 = 0.01$.",
               "es_resultado": False},
              {"accion_md": "Como ambos laterales tienden a $+\\infty$, escribimos:\n\n$$\\lim_{x \\to 0} \\dfrac{1}{x^2} = +\\infty$$",
               "justificacion_md": "La función presenta una **asíntota vertical** en $x = 0$. La estudiaremos en detalle en la lección de asíntotas.",
               "es_resultado": True},
          ]),

        b("grafico_desmos",
          expresiones=["g(x) = 1/x^2"],
          guia_md=(
              "Observa cómo la curva crece sin cota a medida que $x$ se acerca a $0$ desde cualquier lado. "
              "La recta vertical $x = 0$ (el eje $y$) actúa como una **asíntota vertical**: la curva se le acerca infinitamente sin tocarla nunca."
          ),
          altura=380),

        b("texto", body_md=(
            "## Algunos límites que aparecen una y otra vez\n\n"
            "Hay ciertos límites que vale la pena conocer de memoria porque aparecen repetidamente en cálculo, especialmente cuando estudiemos derivadas, series y ecuaciones diferenciales. Los presentamos aquí; algunos los demostraremos en lecciones siguientes."
        )),

        b("definicion",
          titulo="Límite trigonométrico fundamental",
          body_md=(
              "$$\\lim_{x \\to 0} \\dfrac{\\sin x}{x} = 1$$\n\n"
              "Es la base de todas las derivadas trigonométricas. Su demostración formal usa el teorema del sándwich y el área del sector circular; lo veremos en la lección 1.3."
          )),

        b("definicion",
          titulo="Límite del coseno menos uno",
          body_md=(
              "$$\\lim_{x \\to 0} \\dfrac{1 - \\cos x}{x} = 0$$\n\n"
              "Aparece al derivar $\\cos x$ por definición. Se deduce del límite anterior multiplicando y dividiendo por $1 + \\cos x$."
          )),

        b("definicion",
          titulo="Límites que definen el número $e$",
          body_md=(
              "$$\\lim_{x \\to \\infty} \\left(1 + \\dfrac{1}{x}\\right)^x = e \\quad \\text{y equivalentemente} \\quad \\lim_{x \\to 0} (1 + x)^{1/x} = e$$\n\n"
              "Estas dos expresiones son **definiciones alternativas** del número $e \\approx 2{,}71828\\ldots$, base de los logaritmos naturales. Aparecen en cálculo financiero (interés continuo), probabilidades y ecuaciones diferenciales."
          )),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\lim_{x \\to a} f(x)$ con $f(a)$.** El límite habla del comportamiento *cerca* de $a$, sin preocuparse del valor *en* $a$. Una función puede no estar definida en $a$ y tener límite, o estar definida pero con un valor distinto al límite.",
              "**Pensar que $0/0$ significa \"el límite no existe\".** $0/0$ es una **indeterminación**: significa que la sustitución directa no funciona. Hay que usar otra técnica (factorización, racionalización, regla de L'Hôpital, etc.) para resolver.",
              "**Concluir que el límite vale $L$ porque la tabla \"se acerca a $L$\".** Las tablas numéricas son útiles para *conjeturar*, pero no demuestran nada. Solo la definición formal o las técnicas algebraicas demuestran un límite.",
              "**Olvidar verificar los dos laterales.** Si $\\lim_{x \\to a^-} f(x) \\neq \\lim_{x \\to a^+} f(x)$, el límite bilateral no existe — incluso si los laterales individualmente existen.",
              "**Usar $\\infty$ como un número.** $\\lim_{x \\to a} f(x) = \\infty$ es notación: significa que $f(x)$ crece sin cota. No es un valor numérico real.",
          ]),

        b("resumen",
          puntos_md=[
              "**Idea central:** $\\lim_{x \\to a} f(x) = L$ significa que $f(x)$ se aproxima a $L$ cuando $x$ se aproxima a $a$, **sin necesariamente igualar $a$**.",
              "**Existencia:** el límite bilateral existe si y solo si los límites laterales coinciden: $\\lim_{x \\to a^-} f(x) = \\lim_{x \\to a^+} f(x)$.",
              "**Indeterminaciones $0/0$:** no implican que el límite no exista. Se resuelven con factorización, racionalización u otras técnicas (lección 1.7).",
              "**Límites infinitos:** $\\lim_{x \\to a} f(x) = \\pm \\infty$ describe que $f$ crece o decrece sin cota cerca de $a$. Esto produce asíntotas verticales (lección 1.6).",
              "**Límites notables:** $\\dfrac{\\sin x}{x} \\to 1$, $\\dfrac{1-\\cos x}{x} \\to 0$ (cuando $x \\to 0$); $(1+1/x)^x \\to e$ (cuando $x \\to \\infty$).",
              "**Próxima lección:** la definición formal con $\\epsilon$ y $\\delta$ que da rigor matemático a la idea intuitiva de \"aproximarse\".",
          ]),
    ]

    return {
        "id": "lec-limites-1-1-introduccion-intuitiva",
        "title": "Introducción intuitiva al límite",
        "description": "Concepto intuitivo de límite, aproximación numérica y gráfica, límites laterales, límites infinitos y notables.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# LECCIÓN 1.2 — Definición formal (epsilon-delta)
# =====================================================================
def lesson_1_2():
    blocks = [
        b("texto", body_md=(
            "En la lección anterior trabajamos con la idea intuitiva del límite: \"$f(x)$ se acerca a $L$ cuando $x$ se acerca a $a$\". Pero las palabras \"se acerca\" son ambiguas. ¿Qué tan cerca? ¿Cuán precisamente?\n\n"
            "La **definición formal** con $\\epsilon$-$\\delta$ es la respuesta rigurosa de la matemática a esa pregunta. Es densa al principio, pero una vez entendida, es la herramienta que justifica todo el cálculo.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Comprender la definición $\\epsilon$-$\\delta$ y su lógica de juego (desafío y respuesta).\n"
            "- Aplicar la definición para demostrar límites de funciones lineales y cuadráticas.\n"
            "- Reconocer la estructura típica de una demostración $\\epsilon$-$\\delta$."
        )),

        b("intuicion",
          titulo="¿Por qué necesitamos una definición rigurosa?",
          body_md=(
              "Imagina que afirmas: \"$\\lim_{x \\to 2}(3x-1) = 5$\". Yo, escéptico, te respondo:\n\n"
              "> *\"Demuéstramelo. Quiero que $f(x)$ esté a menos de $0{,}001$ de $5$. ¿Cuán cerca de $2$ tengo que tomar a $x$ para garantizártelo?\"*\n\n"
              "Tu trabajo es darme un radio (un número $\\delta$) tal que si $x$ está a distancia menor que $\\delta$ de $2$, entonces $f(x)$ está a distancia menor que $0{,}001$ de $5$.\n\n"
              "Pero yo puedo cambiar mi exigencia: en vez de $0{,}001$, te pido $0{,}0001$. O cualquier número positivo, **arbitrariamente pequeño** — ese es $\\epsilon$. La definición formal dice: pase lo que pase con mi $\\epsilon$, vos siempre puedes encontrar el $\\delta$ que lo satisface."
          )),

        b("definicion",
          titulo="Definición formal de límite ($\\epsilon$-$\\delta$)",
          body_md=(
              "Sea $f$ una función definida en un intervalo abierto que contiene a $c$ (excepto posiblemente en $c$), y sea $L \\in \\mathbb{R}$. Decimos que el **límite de $f(x)$ cuando $x$ tiende a $c$ es $L$**, escrito\n\n"
              "$$\\lim_{x \\to c} f(x) = L,$$\n\n"
              "si para todo $\\epsilon > 0$, existe $\\delta > 0$ tal que:\n\n"
              "$$0 < |x - c| < \\delta \\implies |f(x) - L| < \\epsilon$$"
          )),

        b("intuicion",
          titulo="El \"juego\" del $\\epsilon$-$\\delta$",
          body_md=(
              "La definición se entiende mejor como un **juego de dos jugadores**:\n\n"
              "- **Adversario** (escéptico): elige cualquier $\\epsilon > 0$, por más pequeño que sea. Esto representa la *precisión exigida* en $f(x)$.\n"
              "- **Defensor** (yo): debe encontrar un $\\delta > 0$ tal que, si $x$ está a menos de $\\delta$ de $c$ (excluyendo el propio $c$), entonces $f(x)$ está a menos de $\\epsilon$ de $L$.\n\n"
              "Si el defensor **siempre** puede encontrar tal $\\delta$, sin importar el $\\epsilon$ propuesto, decimos que el límite existe y vale $L$. La condición $0 < |x-c|$ excluye $x = c$: el límite no se preocupa por el valor de $f$ en $c$."
          )),

        b("grafico_desmos",
          expresiones=[
              "f(x) = 3x - 1",
              "L = 5",
              "c = 2",
              "epsilon = 1",
              "delta = epsilon/3",
              "y = L + epsilon \\{c - delta < x < c + delta\\}",
              "y = L - epsilon \\{c - delta < x < c + delta\\}",
              "x = c + delta \\{L - epsilon < y < L + epsilon\\}",
              "x = c - delta \\{L - epsilon < y < L + epsilon\\}",
          ],
          guia_md=(
              "Mueve el slider $\\epsilon$. Ves dos bandas horizontales en $L \\pm \\epsilon$ (la **precisión exigida**). "
              "Para cada $\\epsilon$, se calcula $\\delta = \\epsilon/3$ y aparecen dos bandas verticales en $c \\pm \\delta$. "
              "Observa que la gráfica de $f$ entre $c-\\delta$ y $c+\\delta$ siempre queda **dentro** de la banda horizontal: eso es exactamente lo que la definición exige."
          ),
          altura=420),

        b("ejemplo_resuelto",
          titulo="Demostrar por definición que $\\lim_{x \\to 2}(3x - 1) = 5$",
          problema_md="Usar la definición $\\epsilon$-$\\delta$ para demostrar el límite anterior.",
          pasos=[
              {"accion_md": "**Planteamiento.** Dado un $\\epsilon > 0$ arbitrario, debemos encontrar $\\delta > 0$ tal que:\n\n$$0 < |x - 2| < \\delta \\implies |(3x-1) - 5| < \\epsilon$$",
               "justificacion_md": "Es la estructura obligatoria de toda demostración $\\epsilon$-$\\delta$: aceptamos un $\\epsilon$ genérico y construimos el $\\delta$ que lo satisface.",
               "es_resultado": False},
              {"accion_md": "**Trabajamos con $|f(x) - L|$.** Simplificamos la expresión:\n\n$$|(3x-1) - 5| = |3x - 6| = 3|x - 2|$$",
               "justificacion_md": "Buscamos relacionar $|f(x) - L|$ con $|x - c|$, porque esa es la cantidad que vamos a controlar con $\\delta$.",
               "es_resultado": False},
              {"accion_md": "**Forzamos la desigualdad.** Queremos $3|x - 2| < \\epsilon$, lo que equivale a $|x - 2| < \\dfrac{\\epsilon}{3}$.",
               "justificacion_md": "Despejando $|x-2|$ obtenemos la cota que necesitamos sobre $|x-2|$.",
               "es_resultado": False},
              {"accion_md": "**Elegimos $\\delta$.** Tomamos $\\delta = \\dfrac{\\epsilon}{3}$.",
               "justificacion_md": "Esta elección está motivada por el paso anterior: si $|x-2| < \\delta = \\epsilon/3$, automáticamente se cumple la condición.",
               "es_resultado": False},
              {"accion_md": "**Verificación.** Con $\\delta = \\epsilon/3$, si $0 < |x - 2| < \\delta$, entonces:\n\n$$|(3x-1) - 5| = 3|x - 2| < 3 \\cdot \\dfrac{\\epsilon}{3} = \\epsilon$$",
               "justificacion_md": "Verificamos que la elección funciona: para cualquier $\\epsilon$ que el adversario nos proponga, $\\delta = \\epsilon/3$ asegura la condición.",
               "es_resultado": False},
              {"accion_md": "Por la definición de límite: $\\lim_{x \\to 2}(3x - 1) = 5$.",
               "justificacion_md": "La demostración tiene una **estructura de cinco pasos** que se repetirá: plantear, simplificar $|f(x)-L|$, despejar $|x-c|$, elegir $\\delta$, verificar.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica que entiendes la lógica:",
          preguntas=[
              {
                  "enunciado_md": "En la definición $\\epsilon$-$\\delta$, la condición es \"para todo $\\epsilon > 0$ existe $\\delta > 0$\". ¿Cuál es el orden lógico correcto?",
                  "opciones_md": [
                      "Primero elegimos $\\delta$, luego comprobamos para todo $\\epsilon$.",
                      "Primero el adversario elige $\\epsilon$; en función de él, encontramos $\\delta$.",
                      "$\\epsilon$ y $\\delta$ se eligen simultáneamente.",
                      "$\\delta$ debe ser igual a $\\epsilon$.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "El orden es crítico: $\\epsilon$ se da primero (es el desafío), y $\\delta$ se construye **en función de $\\epsilon$**. "
                      "Por eso $\\delta$ típicamente queda expresado como una fórmula que depende de $\\epsilon$ (en el ejemplo, $\\delta = \\epsilon/3$). "
                      "La opción A invierte la lógica."
                  ),
              },
              {
                  "enunciado_md": "Para $f(x) = 5x$, ¿cuál sería el $\\delta$ apropiado al demostrar $\\lim_{x \\to 1} 5x = 5$?",
                  "opciones_md": ["$\\delta = \\epsilon$", "$\\delta = 5\\epsilon$", "$\\delta = \\dfrac{\\epsilon}{5}$", "$\\delta = \\sqrt{\\epsilon}$"],
                  "correcta": "C",
                  "explicacion_md": (
                      "$|5x - 5| = 5|x - 1|$. Para que esto sea menor que $\\epsilon$, necesitamos $|x-1| < \\epsilon/5$. "
                      "Por lo tanto $\\delta = \\epsilon/5$. La regla general para funciones lineales $f(x) = mx + b$ con $m \\neq 0$: $\\delta = \\epsilon/|m|$."
                  ),
              },
          ]),

        b("ejemplo_resuelto",
          titulo="Demostrar que $\\lim_{x \\to 3}(2x + 1) = 7$",
          problema_md="Aplicar la estructura de la demostración a otro límite lineal.",
          pasos=[
              {"accion_md": "Planteamiento: dado $\\epsilon > 0$, buscamos $\\delta$ tal que $0 < |x-3| < \\delta \\implies |(2x+1) - 7| < \\epsilon$.",
               "justificacion_md": "Misma estructura que el ejemplo anterior.",
               "es_resultado": False},
              {"accion_md": "Simplificación: $|(2x+1) - 7| = |2x - 6| = 2|x-3|$.",
               "justificacion_md": None,
               "es_resultado": False},
              {"accion_md": "Forzamos $2|x-3| < \\epsilon$, equivalente a $|x-3| < \\dfrac{\\epsilon}{2}$. Elegimos $\\delta = \\dfrac{\\epsilon}{2}$.",
               "justificacion_md": "Para funciones lineales $mx + b$, el patrón es $\\delta = \\epsilon/|m|$.",
               "es_resultado": False},
              {"accion_md": "Verificación: si $0 < |x-3| < \\epsilon/2$, entonces $|(2x+1)-7| = 2|x-3| < 2 \\cdot \\epsilon/2 = \\epsilon$. $\\quad \\square$",
               "justificacion_md": "Conclusión: $\\lim_{x \\to 3}(2x+1) = 7$ por definición.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caso cuadrático: $\\lim_{x \\to 1}(x^2 + 2x - 1) = 2$",
          problema_md="Demostrar el límite. Aquí necesitamos una técnica adicional: **acotar** un factor.",
          pasos=[
              {"accion_md": "Simplificamos: $|f(x) - L| = |x^2 + 2x - 1 - 2| = |x^2 + 2x - 3| = |(x-1)(x+3)|$",
               "justificacion_md": "Factorizamos para que aparezca $|x-1|$ — la cantidad que controlamos con $\\delta$.",
               "es_resultado": False},
              {"accion_md": "El problema: $|x+3|$ depende de $x$. Necesitamos **acotarlo**. Imponemos primero $|x-1| < 1$, lo que implica $0 < x < 2$, y por tanto $3 < x+3 < 5$, es decir $|x+3| < 5$.",
               "justificacion_md": "Cuando $f$ es no lineal, el factor adicional varía con $x$. La estrategia estándar es restringir $|x-c|$ a un intervalo conveniente (acá $|x-1| < 1$) para acotar ese factor por una constante.",
               "es_resultado": False},
              {"accion_md": "Con esa cota: $|(x-1)(x+3)| < 5|x-1|$.",
               "justificacion_md": "Ahora la expresión depende solo de $|x-1|$, que sí controlamos.",
               "es_resultado": False},
              {"accion_md": "Forzamos $5|x-1| < \\epsilon$, equivalente a $|x-1| < \\dfrac{\\epsilon}{5}$. **Elegimos $\\delta = \\min\\left\\{1, \\dfrac{\\epsilon}{5}\\right\\}$.**",
               "justificacion_md": "El mínimo asegura que se cumplen **ambas** restricciones: $|x-1| < 1$ (para que la cota $|x+3|<5$ sea válida) y $|x-1| < \\epsilon/5$ (para que el producto sea menor que $\\epsilon$).",
               "es_resultado": False},
              {"accion_md": "Verificación: si $0 < |x-1| < \\delta$, entonces $|x-1| < 1$ y $|x-1| < \\epsilon/5$. Por lo tanto $|f(x)-L| < 5 \\cdot \\dfrac{\\epsilon}{5} = \\epsilon$.\n\n$\\therefore \\lim_{x \\to 1}(x^2+2x-1) = 2$.",
               "justificacion_md": "Esta es la estructura general para polinomios y funciones más complejas: **acotar** los factores extra con una restricción inicial sobre $|x-c|$, y elegir $\\delta = \\min$ de las cotas resultantes.",
               "es_resultado": True},
          ]),

        b("errores_comunes",
          items_md=[
              "**Elegir $\\delta$ que dependa de $x$.** $\\delta$ debe ser un número, no una función de $x$. Solo puede depender de $\\epsilon$ y de constantes.",
              "**Confundir el orden.** $\\epsilon$ se da primero (desafío del adversario); $\\delta$ se construye después en función de $\\epsilon$. No al revés.",
              "**Olvidar la restricción $0 < |x - c|$.** El \"$0 <$\" excluye $x = c$. La definición no exige nada sobre $f(c)$ — el límite ignora el valor en el propio punto.",
              "**No tomar $\\delta = \\min\\{\\ldots\\}$ en casos no lineales.** Cuando se acota un factor con una restricción auxiliar (tipo $|x-c|<1$), el $\\delta$ final debe respetar esa restricción además de la condición principal: por eso aparece el mínimo.",
              "**Pensar que la demostración \"calcula\" $L$.** La definición $\\epsilon$-$\\delta$ **verifica** un valor de $L$ ya conjeturado. No se usa para encontrar el valor del límite, sino para confirmarlo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición formal:** $\\lim_{x \\to c} f(x) = L$ si $\\forall \\epsilon > 0,\\ \\exists \\delta > 0$ tal que $0 < |x-c| < \\delta \\implies |f(x) - L| < \\epsilon$.",
              "**Estructura del juego:** el adversario elige $\\epsilon$; el defensor responde con $\\delta$ en función de $\\epsilon$.",
              "**Patrón para funciones lineales** $f(x) = mx+b$ con $m \\neq 0$: $\\delta = \\epsilon/|m|$.",
              "**Patrón para funciones más complejas:** acotar factores extra restringiendo $|x-c|$ a un intervalo, y elegir $\\delta = \\min$ de las cotas resultantes.",
              "**Lo que la definición no hace:** no calcula el valor de $L$; solo verifica una conjetura.",
              "**Próxima lección:** las leyes algebraicas de los límites, que permiten calcular sin recurrir a $\\epsilon$-$\\delta$ en cada caso.",
          ]),
    ]

    return {
        "id": "lec-limites-1-2-definicion-formal",
        "title": "Definición formal del límite ($\\epsilon$-$\\delta$)",
        "description": "Definición rigurosa de límite. Demostraciones de límites lineales y cuadráticos por epsilon-delta.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# LECCIÓN 1.3 — Propiedades de los límites
# =====================================================================
def lesson_1_3():
    blocks = [
        b("texto", body_md=(
            "Demostrar cada límite con $\\epsilon$-$\\delta$ es agotador. Por suerte, una vez establecidos algunos límites básicos, podemos calcular límites más complejos combinándolos mediante las **leyes algebraicas**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar las leyes algebraicas de límites (suma, producto, cociente, potencia, raíz).\n"
            "- Entender la **regla de sustitución directa** y cuándo aplica.\n"
            "- Usar el **teorema del sándwich** para resolver límites donde las leyes fallan.\n"
            "- Calcular límites de **funciones compuestas**."
        )),

        b("intuicion",
          titulo="Estrategia: descomponer y reconstruir",
          body_md=(
              "La filosofía es la siguiente: si conocemos los límites de funciones simples (constantes, identidad, polinomios básicos), las leyes algebraicas nos permiten calcular el límite de cualquier combinación finita de ellas — sumas, restas, productos, cocientes, potencias y raíces — sin volver a la definición $\\epsilon$-$\\delta$ en cada caso. Es lo mismo que en aritmética: una vez que sabes sumar y multiplicar, puedes evaluar cualquier expresión sin redefinir las operaciones."
          )),

        b("definicion",
          titulo="Límite de una constante",
          body_md=(
              "Si $c \\in \\mathbb{R}$ es una constante:\n\n"
              "$$\\lim_{x \\to a} c = c$$\n\n"
              "El límite de una función constante es la propia constante. La función no \"se mueve\", entonces se aproxima a sí misma."
          )),

        b("definicion",
          titulo="Límite de la función identidad",
          body_md=(
              "Para $f(x) = x$:\n\n"
              "$$\\lim_{x \\to a} x = a$$"
          )),

        b("teorema",
          nombre="Leyes algebraicas de los límites",
          hipotesis=[
              "$\\lim_{x \\to a} f(x) = L$",
              "$\\lim_{x \\to a} g(x) = M$",
          ],
          enunciado_md=(
              "Bajo las hipótesis anteriores, valen las siguientes leyes:\n\n"
              "1. **Suma/resta:** $\\lim_{x \\to a} [f(x) \\pm g(x)] = L \\pm M$\n"
              "2. **Producto por constante:** $\\lim_{x \\to a} [k\\,f(x)] = k\\,L$\n"
              "3. **Producto:** $\\lim_{x \\to a} [f(x)\\,g(x)] = L \\cdot M$\n"
              "4. **Cociente:** $\\lim_{x \\to a} \\dfrac{f(x)}{g(x)} = \\dfrac{L}{M}$, siempre que $M \\neq 0$.\n"
              "5. **Potencia:** $\\lim_{x \\to a} [f(x)]^n = L^n$, para $n \\in \\mathbb{N}$.\n"
              "6. **Raíz:** $\\lim_{x \\to a} \\sqrt[n]{f(x)} = \\sqrt[n]{L}$, con $L \\geq 0$ cuando $n$ es par."
          ),
          demostracion_md=(
              "La demostración de cada ley se hace por $\\epsilon$-$\\delta$. Como ejemplo, demostramos la **ley de la suma**:\n\n"
              "Sea $\\epsilon > 0$. Como $\\lim_{x \\to a} f(x) = L$, existe $\\delta_1 > 0$ tal que $0 < |x-a| < \\delta_1 \\implies |f(x)-L| < \\epsilon/2$. Análogamente, existe $\\delta_2 > 0$ tal que $0 < |x-a| < \\delta_2 \\implies |g(x)-M| < \\epsilon/2$.\n\n"
              "Tomamos $\\delta = \\min\\{\\delta_1, \\delta_2\\}$. Si $0 < |x-a| < \\delta$, por la **desigualdad triangular**:\n\n"
              "$$|(f(x)+g(x)) - (L+M)| \\leq |f(x)-L| + |g(x)-M| < \\dfrac{\\epsilon}{2} + \\dfrac{\\epsilon}{2} = \\epsilon$$\n\n"
              "Las demás leyes se prueban con técnicas similares (más laboriosas para el producto y el cociente)."
          ),
          demostracion_default_open=False),

        b("ejemplo_resuelto",
          titulo="Aplicar las leyes: $\\lim_{x \\to 5}(2x^2 - 3x + 4)$",
          problema_md="Calcular $\\lim_{x \\to 5}(2x^2 - 3x + 4)$ usando las leyes algebraicas, justificando cada paso.",
          pasos=[
              {"accion_md": "Por la **ley de la suma/resta**, separamos el límite:\n\n$$\\lim_{x \\to 5}(2x^2 - 3x + 4) = \\lim_{x \\to 5} 2x^2 - \\lim_{x \\to 5} 3x + \\lim_{x \\to 5} 4$$",
               "justificacion_md": "Aplicamos repetidamente la ley 1 para descomponer en tres límites independientes.",
               "es_resultado": False},
              {"accion_md": "Por la **ley del producto por constante** y la **ley de la potencia**:\n\n$$\\lim_{x \\to 5} 2x^2 = 2 \\cdot \\left(\\lim_{x \\to 5} x\\right)^2, \\quad \\lim_{x \\to 5} 3x = 3 \\cdot \\lim_{x \\to 5} x$$",
               "justificacion_md": "Sacamos las constantes (ley 2) y reducimos las potencias al límite de la identidad (ley 5).",
               "es_resultado": False},
              {"accion_md": "Aplicamos $\\lim_{x \\to 5} x = 5$ (límite de la identidad) y $\\lim_{x \\to 5} 4 = 4$ (límite de constante):\n\n$$2 \\cdot 5^2 - 3 \\cdot 5 + 4 = 50 - 15 + 4$$",
               "justificacion_md": "Reducimos cada límite al valor numérico que corresponde.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{x \\to 5}(2x^2 - 3x + 4) = 39$",
               "justificacion_md": "**Observación clave:** el resultado es exactamente $f(5) = 2(25) - 15 + 4 = 39$. Esto no es coincidencia: vale para todas las funciones polinómicas, lo que motiva la regla de sustitución directa.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cociente: $\\lim_{x \\to -2} \\dfrac{x^3 + 2x^2 - 1}{5 - 3x}$",
          problema_md="Calcular el límite usando la ley del cociente.",
          pasos=[
              {"accion_md": "Verificamos que el denominador no se anule en $x = -2$: $5 - 3(-2) = 5 + 6 = 11 \\neq 0$. Podemos aplicar la ley del cociente.",
               "justificacion_md": "**La ley del cociente requiere $M \\neq 0$.** Si el denominador tiende a $0$, hay que usar otra técnica (factorización, racionalización, etc.).",
               "es_resultado": False},
              {"accion_md": "Calculamos numerador y denominador por separado:\n\n$$\\lim_{x \\to -2}(x^3 + 2x^2 - 1) = (-2)^3 + 2(-2)^2 - 1 = -8 + 8 - 1 = -1$$\n\n$$\\lim_{x \\to -2}(5 - 3x) = 5 - 3(-2) = 11$$",
               "justificacion_md": "Cada límite es de un polinomio, así que aplicamos las leyes de la suma, producto y constante.",
               "es_resultado": False},
              {"accion_md": "Por la ley del cociente: $\\lim_{x \\to -2} \\dfrac{x^3 + 2x^2 - 1}{5 - 3x} = \\dfrac{-1}{11} = -\\dfrac{1}{11}$",
               "justificacion_md": "Las leyes nos llevan al resultado sin necesidad de $\\epsilon$-$\\delta$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Regla de sustitución directa",
          hipotesis=[
              "$f$ es continua en $a$",
          ],
          enunciado_md=(
              "Si $f$ es continua en $a$, entonces:\n\n"
              "$$\\lim_{x \\to a} f(x) = f(a)$$\n\n"
              "Es decir, el límite se calcula simplemente evaluando $f$ en $a$. Esto incluye polinomios, funciones racionales (donde el denominador no se anula), exponenciales, logaritmos, trigonométricas y todas sus composiciones — en sus puntos de continuidad."
          )),

        b("teorema",
          nombre="Límite de funciones compuestas",
          hipotesis=[
              "$\\lim_{x \\to a} g(x) = b$",
              "$\\lim_{u \\to b} f(u) = L$",
              "$f$ es continua en $b$ (o $g(x) \\neq b$ cerca de $a$)",
          ],
          enunciado_md=(
              "Bajo estas hipótesis:\n\n"
              "$$\\lim_{x \\to a} f(g(x)) = L$$\n\n"
              "En palabras: podemos \"meter\" el límite dentro de la función externa, siempre que la externa sea continua en el valor al que tiende la interna."
          )),

        b("teorema",
          nombre="Teorema del Sándwich",
          hipotesis=[
              "$g(x) \\leq f(x) \\leq h(x)$ para todo $x$ cerca de $a$ (excepto posiblemente en $a$)",
              "$\\lim_{x \\to a} g(x) = \\lim_{x \\to a} h(x) = L$",
          ],
          enunciado_md=(
              "Bajo estas hipótesis:\n\n"
              "$$\\lim_{x \\to a} f(x) = L$$\n\n"
              "**Idea intuitiva:** si una función está \"atrapada\" entre dos funciones que tienden al mismo valor $L$, ella también tiene que tender a $L$. No tiene escapatoria."
          ),
          demostracion_md=(
              "Sea $\\epsilon > 0$. Por hipótesis, existen $\\delta_1, \\delta_2 > 0$ tales que:\n\n"
              "- $0 < |x-a| < \\delta_1 \\implies |g(x) - L| < \\epsilon$, equivalente a $L - \\epsilon < g(x) < L + \\epsilon$.\n"
              "- $0 < |x-a| < \\delta_2 \\implies |h(x) - L| < \\epsilon$, equivalente a $L - \\epsilon < h(x) < L + \\epsilon$.\n\n"
              "Tomando $\\delta = \\min\\{\\delta_1, \\delta_2\\}$ y $0 < |x-a| < \\delta$, combinamos con la desigualdad de las hipótesis:\n\n"
              "$$L - \\epsilon < g(x) \\leq f(x) \\leq h(x) < L + \\epsilon$$\n\n"
              "Esto es $|f(x) - L| < \\epsilon$, así que $\\lim_{x \\to a} f(x) = L$. $\\quad \\square$"
          ),
          demostracion_default_open=False),

        b("ejemplo_resuelto",
          titulo="Sándwich clásico: $\\lim_{x \\to 0} x^2 \\sin\\left(\\dfrac{1}{x}\\right) = 0$",
          problema_md=(
              "Demostrar que $\\lim_{x \\to 0} x^2 \\sin\\left(\\dfrac{1}{x}\\right) = 0$.\n\n"
              "**Por qué este caso es importante:** $\\sin(1/x)$ oscila salvajemente cerca de $0$ — ni converge ni tiene límite por sí sola. Las leyes algebraicas no aplican. Sin embargo, el sándwich resuelve el caso fácilmente."
          ),
          pasos=[
              {"accion_md": "**Acotamos $\\sin(1/x)$.** Para todo $x \\neq 0$:\n\n$$-1 \\leq \\sin\\left(\\dfrac{1}{x}\\right) \\leq 1$$",
               "justificacion_md": "El seno toma valores entre $-1$ y $1$, sin importar el argumento. Esta cota universal es el truco.",
               "es_resultado": False},
              {"accion_md": "**Multiplicamos por $x^2 \\geq 0$** (es no negativo, así que la dirección de la desigualdad se preserva):\n\n$$-x^2 \\leq x^2 \\sin\\left(\\dfrac{1}{x}\\right) \\leq x^2$$",
               "justificacion_md": "El detalle crítico: $x^2 \\geq 0$ siempre. Si fuera $x$ (que puede ser negativo), las desigualdades se invertirían en parte del intervalo.",
               "es_resultado": False},
              {"accion_md": "**Calculamos los límites de las cotas:**\n\n$$\\lim_{x \\to 0} (-x^2) = 0, \\quad \\lim_{x \\to 0} x^2 = 0$$",
               "justificacion_md": "Ambas son polinomios continuos en $0$, así que aplicamos sustitución directa.",
               "es_resultado": False},
              {"accion_md": "**Por el teorema del sándwich:** $\\lim_{x \\to 0} x^2 \\sin\\left(\\dfrac{1}{x}\\right) = 0$.",
               "justificacion_md": "Las dos cotas convergen al mismo valor $L = 0$, así que la función \"atrapada\" también converge a $0$. **Notable:** este es un límite imposible de calcular con las leyes algebraicas, pero el sándwich lo resuelve en tres líneas.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo de las leyes y el sándwich:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\lim_{x \\to 4} f(x) = 3$ y $\\lim_{x \\to 4} g(x) = 0$, ¿qué se puede afirmar sobre $\\lim_{x \\to 4} \\dfrac{f(x)}{g(x)}$?",
                  "opciones_md": [
                      "Vale $\\dfrac{3}{0} = \\infty$",
                      "Vale $0$",
                      "No se puede aplicar directamente la ley del cociente; hay que analizarlo aparte",
                      "Vale $3$",
                  ],
                  "correcta": "C",
                  "explicacion_md": (
                      "La ley del cociente exige que el denominador tienda a un valor **distinto de cero**. "
                      "Cuando $g \\to 0$ y $f \\to 3$, la situación es del tipo $3/0$: hay que analizar el comportamiento de $g$ cerca de $4$ (signo, laterales) para determinar si el límite es $+\\infty$, $-\\infty$ o no existe. "
                      "Tampoco es $0$: ese sería el caso $0/3$, no $3/0$."
                  ),
              },
              {
                  "enunciado_md": "Para aplicar el teorema del sándwich a una función $f$, es **necesario y suficiente** que:",
                  "opciones_md": [
                      "$f$ sea continua en el punto.",
                      "$f$ esté acotada por dos funciones cuyos límites coincidan en un mismo valor.",
                      "$f$ sea positiva.",
                      "Las funciones $g$ y $h$ sean polinomios.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Las hipótesis del teorema son: (1) $g(x) \\leq f(x) \\leq h(x)$ cerca del punto, y (2) $\\lim g = \\lim h = L$. "
                      "$f$ no necesita ser continua, ni positiva, ni $g, h$ polinomios. La opción A confunde el sándwich con la sustitución directa; las otras agregan condiciones innecesarias."
                  ),
              },
          ]),

        b("errores_comunes",
          items_md=[
              "**Aplicar la ley del cociente cuando el denominador tiende a $0$.** No es válido. Hay que analizar el caso aparte (factorización, laterales, asíntotas).",
              "**Aplicar la ley del producto en $0 \\cdot \\infty$.** Es una **indeterminación**, no $0$. Por ejemplo, $\\lim_{x \\to 0} x \\cdot \\dfrac{1}{x} = 1$, no $0$.",
              "**Olvidar la condición $L \\geq 0$ para raíces pares.** $\\sqrt[2]{-4}$ no está definido en $\\mathbb{R}$. La ley de la raíz exige que el límite del radicando sea no negativo cuando el índice es par.",
              "**Usar el sándwich con cotas que no convergen al mismo valor.** Si $\\lim g = 0$ pero $\\lim h = 1$, el sándwich no concluye nada. Las dos cotas deben ir al mismo $L$.",
              "**Multiplicar una desigualdad por una expresión que puede cambiar de signo.** En el ejemplo de $x^2 \\sin(1/x)$ usamos $x^2 \\geq 0$. Si fuera $x$, habría que partir en casos $x > 0$ y $x < 0$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Leyes básicas:** suma, producto, cociente, potencia, raíz se distribuyen sobre el límite, **bajo hipótesis** (denominador $\\neq 0$, radicando $\\geq 0$ para raíces pares).",
              "**Sustitución directa:** si $f$ es continua en $a$, $\\lim_{x \\to a} f(x) = f(a)$. Aplica a polinomios, racionales (donde el denominador no se anula), trigonométricas, exponenciales y sus composiciones.",
              "**Compuestas:** $\\lim_{x \\to a} f(g(x)) = f\\left(\\lim_{x \\to a} g(x)\\right)$ cuando $f$ es continua en el valor interno.",
              "**Sándwich:** $g(x) \\leq f(x) \\leq h(x)$ y $\\lim g = \\lim h = L$ implican $\\lim f = L$. Útil para funciones oscilantes acotadas.",
              "**Próxima lección:** continuidad — la condición que hace que la sustitución directa funcione, y el primer paso para hablar de funciones \"sin saltos\".",
          ]),
    ]

    return {
        "id": "lec-limites-1-3-propiedades",
        "title": "Propiedades de los límites",
        "description": "Leyes algebraicas, sustitución directa, teorema del sándwich y límite de funciones compuestas.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# LECCIÓN 1.4 — Continuidad
# =====================================================================
def lesson_1_4():
    blocks = [
        b("texto", body_md=(
            "Hemos hablado varias veces de \"continuidad\" intuitivamente: una función *sin saltos* que se puede dibujar sin levantar el lápiz. En esta lección formalizamos la idea, clasificamos los tipos de discontinuidad y revisamos qué funciones conocidas son continuas (y dónde).\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar la **definición rigurosa** de continuidad en un punto.\n"
            "- Distinguir y clasificar los tres tipos de discontinuidad: removible, de salto, e infinita.\n"
            "- Reconocer la continuidad de las familias de funciones más comunes (polinómicas, racionales, trigonométricas, exponenciales).\n"
            "- Determinar la continuidad de **funciones definidas por partes**."
        )),

        b("intuicion",
          titulo="¿Qué significa ser continua?",
          body_md=(
              "Intuitivamente, una función es continua en un punto $c$ si **al pasar por $c$ no hay sorpresas**: el valor de la función en $c$ coincide con lo que esperamos al acercarnos a $c$ desde cualquier lado. No hay saltos, agujeros ni infinitos.\n\n"
              "La definición formal es elegante: simplemente exige que el límite y el valor de la función coincidan."
          )),

        b("definicion",
          titulo="Continuidad en un punto",
          body_md=(
              "Sea $f$ una función definida en un intervalo abierto que contiene a $c$. Decimos que **$f$ es continua en $c$** si:\n\n"
              "$$\\lim_{x \\to c} f(x) = f(c)$$\n\n"
              "Esta única ecuación encierra **tres condiciones implícitas**:\n\n"
              "1. $f(c)$ está definida (la función existe en $c$).\n"
              "2. $\\lim_{x \\to c} f(x)$ existe (es decir, los laterales coinciden y son finitos).\n"
              "3. Ambos coinciden: $\\lim = f(c)$.\n\n"
              "Si alguna de las tres falla, $f$ es **discontinua** en $c$."
          )),

        b("definicion",
          titulo="Continuidad lateral y continuidad en intervalos",
          body_md=(
              "Análogamente a los límites laterales:\n\n"
              "- $f$ es **continua por la izquierda en $c$** si $\\lim_{x \\to c^-} f(x) = f(c)$.\n"
              "- $f$ es **continua por la derecha en $c$** si $\\lim_{x \\to c^+} f(x) = f(c)$.\n\n"
              "$f$ es continua en un **intervalo abierto** $(a, b)$ si lo es en cada punto del intervalo. Es continua en un **intervalo cerrado** $[a, b]$ si lo es en $(a, b)$, continua por la derecha en $a$, y continua por la izquierda en $b$."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar continuidad: $f(x) = x^2$ en $x = 2$",
          problema_md="Demostrar que $f(x) = x^2$ es continua en $x = 2$.",
          pasos=[
              {"accion_md": "**Condición 1:** $f(2) = 4$. La función está definida.",
               "justificacion_md": "Es un polinomio, definido en todo $\\mathbb{R}$.",
               "es_resultado": False},
              {"accion_md": "**Condición 2:** $\\lim_{x \\to 2} x^2 = 4$ (por las leyes de la lección anterior).",
               "justificacion_md": "El límite existe.",
               "es_resultado": False},
              {"accion_md": "**Condición 3:** $\\lim_{x \\to 2} x^2 = 4 = f(2)$.",
               "justificacion_md": "Las dos cantidades coinciden.",
               "es_resultado": False},
              {"accion_md": "Por la definición, $f$ es continua en $2$.",
               "justificacion_md": "El mismo argumento funciona para cualquier punto $a \\in \\mathbb{R}$, así que $f(x) = x^2$ es continua en todo $\\mathbb{R}$.",
               "es_resultado": True},
          ]),

        b("texto", body_md=(
            "## Tipos de discontinuidad\n\n"
            "Cuando alguna de las tres condiciones falla, la función es discontinua. Hay tres tipos clásicos según *qué* falla."
        )),

        b("definicion",
          titulo="Discontinuidad removible (evitable)",
          body_md=(
              "$f$ tiene una **discontinuidad removible** en $c$ si:\n\n"
              "- $\\lim_{x \\to c} f(x) = L$ existe (los laterales coinciden y son finitos), pero\n"
              "- $f(c)$ no está definida, o $f(c) \\neq L$.\n\n"
              "Se llama \"removible\" porque podemos *redefinir* $f(c) := L$ y obtener una función continua. La discontinuidad es \"un agujero\" que podemos *tapar*."
          )),

        b("ejemplo_resuelto",
          titulo="Removible: $f(x) = \\dfrac{x^2 - 1}{x - 1}$ en $x = 1$",
          problema_md="Clasificar la discontinuidad de $f(x) = \\dfrac{x^2 - 1}{x - 1}$ en $x = 1$ y proponer una redefinición continua.",
          pasos=[
              {"accion_md": "$f(1)$ no está definida (denominador cero). **Falla la condición 1.**",
               "justificacion_md": "El primer requisito de continuidad ya no se cumple.",
               "es_resultado": False},
              {"accion_md": "Sin embargo, $\\lim_{x \\to 1} \\dfrac{x^2-1}{x-1} = \\lim_{x \\to 1} \\dfrac{(x-1)(x+1)}{x-1} = \\lim_{x \\to 1}(x+1) = 2$. **El límite sí existe** y vale $2$.",
               "justificacion_md": "Factorizamos para cancelar el factor problemático y aplicamos sustitución directa al resultado.",
               "es_resultado": False},
              {"accion_md": "Como el límite existe pero $f(1)$ no está definida, la discontinuidad es **removible**. La redefinimos como una función por partes:\n\n$$\\tilde{f}(x) = \\begin{cases} \\dfrac{x^2-1}{x-1} & \\text{si } x \\neq 1 \\\\ 2 & \\text{si } x = 1 \\end{cases}$$",
               "justificacion_md": "Esta nueva función $\\tilde{f}$ es continua en todo $\\mathbb{R}$, porque ahora la condición 3 se cumple en $x = 1$. La función original tiene un \"agujero\" que rellenamos con el valor del límite.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Discontinuidad de salto",
          body_md=(
              "$f$ tiene una **discontinuidad de salto** en $c$ si:\n\n"
              "- Ambos límites laterales $\\lim_{x \\to c^-} f(x)$ y $\\lim_{x \\to c^+} f(x)$ existen y son finitos, pero\n"
              "- Son distintos.\n\n"
              "El límite bilateral no existe porque los laterales no coinciden. La función \"salta\" de un valor a otro al pasar por $c$. **No es removible:** ninguna redefinición de $f(c)$ logra continuidad."
          )),

        b("definicion",
          titulo="Discontinuidad infinita",
          body_md=(
              "$f$ tiene una **discontinuidad infinita** en $c$ si al menos uno de los límites laterales en $c$ es $\\pm\\infty$. Es decir, la función \"escapa\" al infinito al acercarse a $c$.\n\n"
              "Estas discontinuidades aparecen donde hay **asíntotas verticales** (las estudiaremos en la lección 1.6). Tampoco son removibles."
          )),

        b("figura",
          image_url="",
          caption_md="Comparación visual de los tres tipos de discontinuidad: removible (agujero), de salto (escalón) e infinita (asíntota vertical).",
          prompt_image_md=(
              "Tres gráficos pequeños lado a lado en un panel apaisado, fondo blanco, estilo libro de texto universitario, minimalista. "
              "Cada gráfico tiene ejes cartesianos en gris oscuro con flechas, sin grilla. Las funciones se dibujan en color cyan/turquesa (#06b6d4) con grosor ~3px.\n\n"
              "**Gráfico 1 (izquierda):** una curva continua con un círculo abierto (vacío) en un punto específico, mostrando un 'agujero' en la gráfica. Título debajo: 'Discontinuidad removible'.\n\n"
              "**Gráfico 2 (centro):** una función escalón que da un salto vertical en un punto: dos segmentos de recta horizontales a alturas diferentes, con un círculo lleno en el punto donde llega cada rama. Título debajo: 'Discontinuidad de salto'.\n\n"
              "**Gráfico 3 (derecha):** una función tipo 1/x cerca del eje y, mostrando una asíntota vertical (línea vertical punteada en gris) que la curva nunca toca. Título debajo: 'Discontinuidad infinita'.\n\n"
              "Cada gráfico debe ser claro, simétrico y didáctico. Sin etiquetas innecesarias en los ejes (solo flechas y opcionalmente 'x' y 'y' en cursiva)."
          )),

        b("teorema",
          nombre="Continuidad de las familias de funciones elementales",
          hipotesis=[],
          enunciado_md=(
              "Las siguientes funciones son **continuas en todos los puntos de su dominio**:\n\n"
              "- **Polinómicas:** continuas en todo $\\mathbb{R}$. Por ejemplo, $f(x) = x^3 - 2x^2 + x - 5$.\n"
              "- **Racionales** (cocientes de polinomios): continuas excepto donde el denominador se anula. Por ejemplo, $f(x) = \\dfrac{x^2 + 1}{x - 2}$ es continua en $\\mathbb{R} \\setminus \\{2\\}$.\n"
              "- **Trigonométricas:** $\\sin x$ y $\\cos x$ son continuas en todo $\\mathbb{R}$. $\\tan x$, $\\sec x$, $\\csc x$, $\\cot x$ son continuas excepto donde su denominador trigonométrico se anula (por ejemplo, $\\tan x$ es continua excepto en $x = \\pi/2 + k\\pi$).\n"
              "- **Exponenciales:** $e^x$ y, en general, $a^x$ con $a > 0$, son continuas en todo $\\mathbb{R}$.\n"
              "- **Logarítmicas:** $\\ln x$ es continua en su dominio natural $(0, +\\infty)$.\n"
              "- **Raíces:** $\\sqrt[n]{x}$ es continua en su dominio (en $[0, +\\infty)$ si $n$ es par, en $\\mathbb{R}$ si $n$ es impar).\n"
              "- **Sumas, productos, cocientes y composiciones** de las anteriores son continuas donde estén definidas."
          )),

        b("definicion",
          titulo="Funciones definidas por partes",
          body_md=(
              "Una **función definida por partes** asigna distintas expresiones según el subintervalo del dominio:\n\n"
              "$$f(x) = \\begin{cases} f_1(x) & \\text{si } x \\in I_1 \\\\ f_2(x) & \\text{si } x \\in I_2 \\\\ \\vdots \\\\ f_n(x) & \\text{si } x \\in I_n \\end{cases}$$\n\n"
              "donde $I_1, I_2, \\ldots, I_n$ son intervalos disjuntos. Para verificar continuidad en un **punto interior** de algún $I_i$, basta con que la expresión $f_i$ sea continua allí (típicamente sí). El punto **crítico** es la frontera entre dos ramas: ahí hay que verificar las tres condiciones explícitamente."
          )),

        b("ejemplo_resuelto",
          titulo="Continuidad de una función a trozos en su frontera",
          problema_md=(
              "Sea $f(x) = \\begin{cases} x^2 & \\text{si } x < 1 \\\\ 2x - 1 & \\text{si } x \\geq 1 \\end{cases}$. Verificar si $f$ es continua en $x = 1$."
          ),
          pasos=[
              {"accion_md": "**Condición 1:** $f(1)$. Como $x = 1$ pertenece a la rama $x \\geq 1$, $f(1) = 2(1) - 1 = 1$. Definida.",
               "justificacion_md": "Hay que mirar cuál de las dos definiciones aplica para $x = c$ (acá la segunda, por el $\\geq$).",
               "es_resultado": False},
              {"accion_md": "**Límite por la izquierda** (rama $x^2$ para $x < 1$): $\\lim_{x \\to 1^-} x^2 = 1$.",
               "justificacion_md": "Para acercarnos por la izquierda usamos la rama válida en ese lado.",
               "es_resultado": False},
              {"accion_md": "**Límite por la derecha** (rama $2x - 1$ para $x \\geq 1$): $\\lim_{x \\to 1^+}(2x-1) = 1$.",
               "justificacion_md": "Análogo por la derecha.",
               "es_resultado": False},
              {"accion_md": "**Los laterales coinciden:** $\\lim_{x \\to 1} f(x) = 1$. Por lo tanto la **condición 2** se cumple.",
               "justificacion_md": "Cuando ambos laterales coinciden, el límite bilateral existe y vale ese valor común.",
               "es_resultado": False},
              {"accion_md": "**Condición 3:** $\\lim_{x \\to 1} f(x) = 1 = f(1)$. Las tres condiciones se cumplen, por lo tanto $f$ es **continua en $x = 1$**.",
               "justificacion_md": "Pegado perfecto entre las dos ramas. **Receta general:** en cada frontera de una función a trozos, calcular el valor de cada rama allí; si todos coinciden, hay continuidad.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "Sea $f(x) = \\begin{cases} 1 & \\text{si } x < 0 \\\\ 3 & \\text{si } x \\geq 0 \\end{cases}$. ¿Qué tipo de discontinuidad tiene en $x = 0$?",
                  "opciones_md": ["Removible", "De salto", "Infinita", "Es continua, no hay discontinuidad"],
                  "correcta": "B",
                  "explicacion_md": (
                      "Los límites laterales existen y son finitos: $\\lim_{x \\to 0^-} f(x) = 1$ y $\\lim_{x \\to 0^+} f(x) = 3$. "
                      "Pero son distintos, así que el límite bilateral no existe — es una **discontinuidad de salto**. "
                      "No es removible (no se puede arreglar redefiniendo $f(0)$) ni infinita (no hay $\\pm \\infty$)."
                  ),
              },
              {
                  "enunciado_md": "¿En qué puntos es discontinua la función $g(x) = \\dfrac{x + 1}{x^2 - 4}$?",
                  "opciones_md": [
                      "Solo en $x = 0$",
                      "En $x = 2$ y $x = -2$",
                      "En todo $\\mathbb{R}$",
                      "En ningún punto",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Es una función racional, continua donde el denominador no se anule. $x^2 - 4 = 0 \\iff x = \\pm 2$. "
                      "En esos puntos $g$ no está definida, así que es discontinua. En todos los demás puntos de $\\mathbb{R}$ es continua (típicamente con discontinuidad infinita en $\\pm 2$, pero hay que verificarlo caso a caso)."
                  ),
              },
          ]),

        b("errores_comunes",
          items_md=[
              "**Pensar que \"continua\" significa \"definida en todo $\\mathbb{R}$\".** No: $\\sqrt{x}$ es continua en su dominio $[0, +\\infty)$, aunque no esté definida en negativos.",
              "**Confundir discontinuidad removible con \"continuamente extendible\".** La función *original* es discontinua en el punto problemático. Solo la **redefinida** (con el valor del límite) es continua.",
              "**No verificar las tres condiciones.** Algunos solo calculan el límite y olvidan comparar con $f(c)$, o asumen que $f(c)$ existe. La definición exige las tres condiciones.",
              "**Olvidar verificar la continuidad en la frontera de una función a trozos.** Aunque cada rama sea continua, en el punto donde se pegan puede no haberlo.",
              "**Decir que $\\tan x$ es discontinua en $\\pi/2$.** Más preciso: $\\tan x$ no está **definida** en $\\pi/2$; en su dominio (que excluye esos puntos) sí es continua.",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición:** $f$ es continua en $c$ si $\\lim_{x \\to c} f(x) = f(c)$. Implica tres condiciones: $f(c)$ definida, límite existe, ambos coinciden.",
              "**Tres tipos de discontinuidad:** removible (agujero, $f(c)$ se puede arreglar), de salto (laterales distintos), infinita (laterales $\\pm \\infty$).",
              "**Funciones elementales:** polinomios, $\\sin$, $\\cos$, $e^x$ son continuas en todo $\\mathbb{R}$. Racionales, $\\tan$, $\\ln$, raíces son continuas en su dominio natural.",
              "**Por partes:** dentro de cada rama suele haber continuidad; el punto crítico es la **frontera** entre ramas, donde hay que verificar las tres condiciones.",
              "**Próxima lección:** el Teorema del Valor Intermedio, una consecuencia poderosa de la continuidad que garantiza la existencia de soluciones a ecuaciones."
          ]),
    ]

    return {
        "id": "lec-limites-1-4-continuidad",
        "title": "Continuidad de funciones",
        "description": "Definición de continuidad, tipos de discontinuidad (removible, salto, infinita), continuidad de funciones elementales y por partes.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# LECCIÓN 1.5 — Teorema del Valor Intermedio
# =====================================================================
def lesson_1_5():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora la continuidad ha sido un concepto descriptivo: nos dice cómo se comporta una función. En esta lección veremos un teorema que **convierte la continuidad en una herramienta**: nos permite garantizar la existencia de soluciones a ecuaciones que no podemos resolver explícitamente.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Comprender el enunciado y las hipótesis del **Teorema del Valor Intermedio (TVI)**.\n"
            "- Aplicar el TVI para demostrar que ciertas ecuaciones tienen soluciones en intervalos específicos.\n"
            "- Reconocer cuándo el teorema **no es aplicable** y cuándo solo da existencia (no unicidad ni el valor)."
        )),

        b("intuicion",
          titulo="La idea del TVI en una frase",
          body_md=(
              "Si dibujas una curva continua que comienza por debajo de una recta horizontal $y = N$ y termina por encima (o viceversa), la curva tiene que **cruzar** la recta en algún punto. No puede saltar la recta — eso violaría la continuidad.\n\n"
              "El TVI formaliza este hecho geométrico tan obvio que parece innecesario… pero su utilidad es enorme: convierte una observación visual en una herramienta de demostración."
          )),

        b("teorema",
          nombre="Teorema del Valor Intermedio (TVI)",
          hipotesis=[
              "$f$ es continua en el intervalo cerrado $[a, b]$",
              "$N$ es un número entre $f(a)$ y $f(b)$, con $f(a) \\neq f(b)$",
          ],
          enunciado_md=(
              "Bajo las hipótesis anteriores, **existe** un número $c \\in (a, b)$ tal que:\n\n"
              "$$f(c) = N$$\n\n"
              "Es decir, una función continua que toma los valores $f(a)$ y $f(b)$ en los extremos del intervalo, también toma cualquier valor intermedio $N$ en algún punto del interior."
          ),
          demostracion_md=(
              "La demostración rigurosa requiere el **axioma de completitud** de los reales (cada conjunto acotado superiormente tiene supremo). Definimos:\n\n"
              "$$S = \\{x \\in [a, b] : f(x) \\leq N\\}$$\n\n"
              "$S$ es no vacío (contiene a $a$ si $f(a) < N$) y acotado superiormente (por $b$). Por completitud, $S$ tiene supremo $c$. Se demuestra usando continuidad que $f(c) = N$ (no puede ser ni $< N$ ni $> N$ sin contradecir que $c$ es supremo).\n\n"
              "La demostración completa pertenece a un curso de análisis real; aquí basta con aceptar el resultado y entenderlo geométricamente."
          ),
          demostracion_default_open=False),

        b("grafico_desmos",
          expresiones=[
              "f(x) = x^3 - 4x + 1",
              "a = 0",
              "b = 2",
              "N = 0",
              "y = N",
              "(a, f(a))",
              "(b, f(b))",
          ],
          guia_md=(
              "Observa la gráfica de $f(x) = x^3 - 4x + 1$ en $[0, 2]$. "
              "Tenemos $f(0) = 1 > 0$ y $f(2) = 8 - 8 + 1 = 1 > 0$. ¡Pero el TVI no se aplica para garantizar $f(c) = 0$ en este intervalo! Cambia $b$ a $1$ para ver: $f(1) = 1 - 4 + 1 = -2 < 0$. Ahora $0$ está entre $f(0) = 1$ y $f(1) = -2$, y la curva continua **debe cruzar** la recta $y = 0$ en algún $c \\in (0, 1)$. Localiza visualmente ese cruce."
          ),
          altura=400),

        b("ejemplo_resuelto",
          titulo="¿Tiene solución la ecuación $x^3 - x = 2$?",
          problema_md="Demostrar que la ecuación $x^3 - x = 2$ tiene al menos una solución real.",
          pasos=[
              {"accion_md": "Reformulamos como búsqueda de raíz: definimos $f(x) = x^3 - x$ y buscamos $c$ tal que $f(c) = 2$.",
               "justificacion_md": "El TVI se enuncia para $f(c) = N$. Identificamos $N = 2$.",
               "es_resultado": False},
              {"accion_md": "**Verificamos hipótesis 1:** $f(x) = x^3 - x$ es un polinomio, **continua en todo $\\mathbb{R}$**, y por tanto en cualquier $[a,b]$.",
               "justificacion_md": "Los polinomios son continuos en todo $\\mathbb{R}$, lección anterior.",
               "es_resultado": False},
              {"accion_md": "**Buscamos un intervalo donde $N = 2$ esté entre $f(a)$ y $f(b)$.** Probamos $a = 1$, $b = 2$:\n\n$$f(1) = 1 - 1 = 0, \\quad f(2) = 8 - 2 = 6$$",
               "justificacion_md": "Necesitamos que $f(a)$ y $f(b)$ \"encajen\" $N = 2$. Probar valores cercanos al ojo.",
               "es_resultado": False},
              {"accion_md": "**Verificamos hipótesis 2:** $0 < 2 < 6$, así que $N = 2$ está entre $f(1)$ y $f(2)$.",
               "justificacion_md": "Las dos hipótesis del TVI se cumplen.",
               "es_resultado": False},
              {"accion_md": "**Por el TVI:** existe $c \\in (1, 2)$ tal que $f(c) = 2$, es decir $c^3 - c = 2$.",
               "justificacion_md": "**Importante:** el TVI garantiza que $c$ existe, pero no nos dice cuánto vale ni si es único. Sólo asegura existencia. Para encontrar el valor numérico habría que usar métodos como bisección o Newton.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Una ecuación más exigente: $4x^3 - 6x^2 + 3x = 2$",
          problema_md="¿Tiene la ecuación $4x^3 - 6x^2 + 3x = 2$ alguna solución real?",
          pasos=[
              {"accion_md": "Definimos $g(x) = 4x^3 - 6x^2 + 3x$ y buscamos $c$ con $g(c) = 2$. Es polinómica, así que continua en $\\mathbb{R}$.",
               "justificacion_md": "Hipótesis 1 del TVI cumplida automáticamente.",
               "es_resultado": False},
              {"accion_md": "Evaluamos en algunos puntos. $g(0) = 0$, $g(1) = 4 - 6 + 3 = 1$, $g(2) = 32 - 24 + 6 = 14$.",
               "justificacion_md": "Buscamos un intervalo $[a,b]$ donde $g(a) < 2 < g(b)$.",
               "es_resultado": False},
              {"accion_md": "En $[1, 2]$: $g(1) = 1 < 2 < 14 = g(2)$. **Hipótesis del TVI cumplidas.**",
               "justificacion_md": "Continuidad y $N = 2$ entre los valores en los extremos.",
               "es_resultado": False},
              {"accion_md": "**Por el TVI:** existe $c \\in (1, 2)$ tal que $g(c) = 2$, es decir $4c^3 - 6c^2 + 3c = 2$.",
               "justificacion_md": "Resolver explícitamente la ecuación cúbica sería tedioso (fórmula de Cardano), pero el TVI nos da existencia *gratis*. **Esa es su utilidad central:** demostrar que algo existe sin tener que calcularlo.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo del teorema:",
          preguntas=[
              {
                  "enunciado_md": "Sea $f(x) = \\dfrac{1}{x}$ en $[-1, 1]$. ¿Es válido aplicar el TVI para garantizar $f(c) = 0$ con $c \\in (-1, 1)$?",
                  "opciones_md": [
                      "Sí, porque $f(-1) = -1$ y $f(1) = 1$ y $0$ está entre ambos.",
                      "No, porque $f$ no está definida en $0$ y por tanto no es continua en $[-1, 1]$.",
                      "Sí, porque $f$ es continua en cada $x \\neq 0$.",
                      "No, porque $f$ es decreciente.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "El TVI exige continuidad en **todo** el intervalo cerrado $[-1, 1]$. "
                      "$f(x) = 1/x$ no está definida en $x = 0 \\in [-1, 1]$, así que no es continua allí. La hipótesis del teorema falla. "
                      "De hecho, $f$ nunca toma el valor $0$, lo que confirma que el TVI no aplica."
                  ),
              },
              {
                  "enunciado_md": "Si $f$ es continua en $[a, b]$ y existe $c \\in (a, b)$ tal que $f(c) = N$, ¿qué se puede afirmar?",
                  "opciones_md": [
                      "$N$ debe estar entre $f(a)$ y $f(b)$.",
                      "$c$ es único.",
                      "Nada en particular: el TVI da una implicación, no su recíproca.",
                      "$f(a) = f(b)$.",
                  ],
                  "correcta": "C",
                  "explicacion_md": (
                      "El TVI dice: **hipótesis $\\Rightarrow$ existe $c$**. La pregunta plantea el recíproco: \"existe $c$ con $f(c)=N$, ¿qué pasa?\". "
                      "El recíproco no está garantizado por el teorema. $N$ podría no estar entre $f(a)$ y $f(b)$ (puede haber muchos $c$ donde $f$ toma cualquier valor en su rango), y $c$ no tiene por qué ser único."
                  ),
              },
          ]),

        b("errores_comunes",
          items_md=[
              "**Olvidar verificar la continuidad en TODO el intervalo.** El TVI exige continuidad en $[a, b]$ completo, no solo en los extremos. Una función con discontinuidad interna invalida el teorema.",
              "**Pensar que el TVI da el valor de $c$.** Solo garantiza **existencia**, no calcula. Para el valor explícito hay que usar otros métodos (bisección, Newton, fórmulas algebraicas si las hay).",
              "**Pensar que el TVI da unicidad.** Pueden existir **varios** $c$ que satisfacen $f(c) = N$. El teorema solo asegura *al menos uno*.",
              "**Aplicar el TVI sin que $N$ esté entre $f(a)$ y $f(b)$.** Si por ejemplo $f(a) = 3$ y $f(b) = 5$, el TVI no dice nada sobre si $f$ alcanza el valor $7$ — fuera del rango de los extremos, no garantiza nada.",
              "**Confundir el TVI con \"el rango de $f$ es un intervalo\".** Es una consecuencia *adicional* (cierta si $f$ es continua en un cerrado, por compacidad), pero no es lo que el TVI afirma directamente.",
          ]),

        b("resumen",
          puntos_md=[
              "**TVI:** si $f$ es continua en $[a,b]$ y $N$ está entre $f(a)$ y $f(b)$, entonces existe $c \\in (a,b)$ con $f(c) = N$.",
              "**Hipótesis crítica:** la **continuidad en todo el intervalo cerrado**. Si falla, el teorema no aplica.",
              "**Lo que da:** existencia. **Lo que no da:** valor explícito ni unicidad de $c$.",
              "**Aplicación clásica:** demostrar que una ecuación $f(x) = N$ tiene solución, evaluando $f$ en dos puntos donde tome valores con $N$ entre ellos.",
              "**Estrategia:** llevar la ecuación a la forma $f(c) = N$, verificar continuidad, encontrar $a, b$ con $N$ entre $f(a)$ y $f(b)$, concluir.",
              "**Próxima lección:** asíntotas — el comportamiento de funciones continuas (y discontinuas) en los extremos del dominio o cerca de discontinuidades infinitas."
          ]),
    ]

    return {
        "id": "lec-limites-1-5-tvi",
        "title": "Teorema del Valor Intermedio",
        "description": "Enunciado, hipótesis y aplicaciones del TVI para garantizar la existencia de soluciones a ecuaciones.",
        "blocks": blocks,
        "duration_minutes": 35,
        "order": 5,
    }


# =====================================================================
# LECCIÓN 1.6 — Asíntotas
# =====================================================================
def lesson_1_6():
    blocks = [
        b("texto", body_md=(
            "Las **asíntotas** son rectas que la gráfica de una función se aproxima sin tocar (o, en casos atípicos, las cruza pero sigue acercándose). Identificar las asíntotas de una función nos da una imagen clara de su comportamiento global, incluso sin graficar punto por punto.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Identificar **asíntotas verticales** vía límites infinitos.\n"
            "- Calcular **asíntotas horizontales** mediante límites al infinito.\n"
            "- Determinar **asíntotas oblicuas** usando las fórmulas para la pendiente y la ordenada al origen."
        )),

        b("intuicion",
          titulo="Tres tipos, tres preguntas",
          body_md=(
              "Para identificar las asíntotas de una función, basta con responder tres preguntas:\n\n"
              "1. **¿Hay puntos donde $f$ explota a $\\pm \\infty$?** $\\to$ asíntotas **verticales**.\n"
              "2. **¿A qué valor tiende $f$ cuando $x \\to \\pm \\infty$?** Si tiende a un número finito, hay asíntotas **horizontales**.\n"
              "3. **¿La función crece linealmente en el infinito?** Si lo hace pero la asíntota horizontal no funciona, podría haber asíntotas **oblicuas**.\n\n"
              "Estas tres preguntas se contestan con límites — exactamente la herramienta que llevamos toda la unidad construyendo."
          )),

        b("definicion",
          titulo="Asíntota vertical",
          body_md=(
              "La recta $x = a$ es una **asíntota vertical** de $f$ si al menos uno de los siguientes límites es infinito:\n\n"
              "$$\\lim_{x \\to a^-} f(x) = \\pm \\infty \\quad \\text{o} \\quad \\lim_{x \\to a^+} f(x) = \\pm \\infty$$\n\n"
              "Equivalente: la función \"escapa\" al infinito al acercarse a $a$. **Suele ocurrir donde el denominador de una fracción se anula** (sin que el numerador también lo haga)."
          )),

        b("ejemplo_resuelto",
          titulo="Asíntota vertical de $f(x) = \\dfrac{1}{x - 2}$",
          problema_md="Determinar las asíntotas verticales y describir el comportamiento.",
          pasos=[
              {"accion_md": "**Buscamos puntos donde el denominador se anule.** $x - 2 = 0 \\iff x = 2$. Candidata a asíntota vertical: $x = 2$.",
               "justificacion_md": "En esos puntos la función tiende a $\\pm \\infty$, salvo que el numerador también se anule (cancelación).",
               "es_resultado": False},
              {"accion_md": "**Límite por la derecha:** cuando $x \\to 2^+$, $x - 2 \\to 0^+$, así que $\\dfrac{1}{x-2} \\to +\\infty$.",
               "justificacion_md": "$1$ dividido por algo positivo muy pequeño da algo positivo muy grande.",
               "es_resultado": False},
              {"accion_md": "**Límite por la izquierda:** cuando $x \\to 2^-$, $x - 2 \\to 0^-$, así que $\\dfrac{1}{x-2} \\to -\\infty$.",
               "justificacion_md": "$1$ dividido por algo negativo muy pequeño da algo muy negativo.",
               "es_resultado": False},
              {"accion_md": "**Conclusión:** $x = 2$ es una asíntota vertical. La función \"sale\" hacia $-\\infty$ por la izquierda y hacia $+\\infty$ por la derecha.",
               "justificacion_md": "Es típico de funciones racionales con un cero simple en el denominador: la función cambia de signo al cruzar la asíntota.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Asíntota horizontal",
          body_md=(
              "La recta $y = b$ es una **asíntota horizontal** de $f$ si:\n\n"
              "$$\\lim_{x \\to +\\infty} f(x) = b \\quad \\text{o} \\quad \\lim_{x \\to -\\infty} f(x) = b$$\n\n"
              "Notar que una función puede tener **dos asíntotas horizontales distintas** (una por cada lado). Por ejemplo, $\\arctan x$ tiene $y = \\pi/2$ por la derecha y $y = -\\pi/2$ por la izquierda."
          )),

        b("ejemplo_resuelto",
          titulo="Asíntota horizontal de $f(x) = \\dfrac{2x + 1}{x + 3}$",
          problema_md="Calcular la(s) asíntota(s) horizontal(es).",
          pasos=[
              {"accion_md": "**Calculamos el límite cuando $x \\to +\\infty$.** Para resolver una indeterminación $\\infty/\\infty$, dividimos numerador y denominador por la potencia más alta de $x$ (acá $x^1$):\n\n$$\\lim_{x \\to +\\infty} \\dfrac{2x+1}{x+3} = \\lim_{x \\to +\\infty} \\dfrac{2 + \\dfrac{1}{x}}{1 + \\dfrac{3}{x}}$$",
               "justificacion_md": "La técnica estándar para fracciones polinomiales al infinito.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos sustitución directa**: como $\\dfrac{1}{x} \\to 0$ y $\\dfrac{3}{x} \\to 0$ cuando $x \\to \\infty$:\n\n$$\\lim_{x \\to +\\infty} \\dfrac{2 + 0}{1 + 0} = 2$$",
               "justificacion_md": "Los términos con $1/x$ desaparecen y queda el cociente de los coeficientes principales.",
               "es_resultado": False},
              {"accion_md": "**Análogo cuando $x \\to -\\infty$:** los términos $1/x$ siguen tendiendo a $0$, así que el límite también es $2$.",
               "justificacion_md": "Para esta función, ambos extremos del eje $x$ dan el mismo valor.",
               "es_resultado": False},
              {"accion_md": "**Conclusión:** $y = 2$ es asíntota horizontal por ambos lados.",
               "justificacion_md": "**Receta para racionales:** cuando los grados del numerador y del denominador son iguales, la asíntota horizontal es el cociente de los coeficientes principales (acá $2/1 = 2$).",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Asíntota oblicua",
          body_md=(
              "La recta $y = mx + n$ es una **asíntota oblicua** de $f$ si:\n\n"
              "$$\\lim_{x \\to \\pm\\infty} [f(x) - (mx + n)] = 0$$\n\n"
              "Es decir, la diferencia entre $f$ y la recta tiende a $0$ en el infinito: la gráfica se \"pega\" a la recta. Las asíntotas oblicuas aparecen cuando $f$ crece linealmente al infinito pero **no es horizontal** (es decir, $m \\neq 0$).\n\n"
              "**Cálculo de $m$ y $n$:**\n\n"
              "$$m = \\lim_{x \\to +\\infty} \\dfrac{f(x)}{x}, \\qquad n = \\lim_{x \\to +\\infty} [f(x) - mx]$$\n\n"
              "Análogo para $x \\to -\\infty$. Para que exista la asíntota oblicua, **ambos** límites deben ser finitos y $m \\neq 0$. Si $m = 0$, no hay oblicua: estaríamos describiendo una horizontal."
          )),

        b("ejemplo_resuelto",
          titulo="Asíntota oblicua de $f(x) = \\dfrac{x^2 + 3x + 2}{x}$",
          problema_md="Determinar las asíntotas de $f(x) = \\dfrac{x^2 + 3x + 2}{x}$.",
          pasos=[
              {"accion_md": "**Asíntotas verticales:** el denominador se anula en $x = 0$. El numerador en $0$ vale $2 \\neq 0$, así que hay asíntota vertical $x = 0$.",
               "justificacion_md": "Numerador finito sobre denominador que tiende a $0$ produce $\\pm \\infty$.",
               "es_resultado": False},
              {"accion_md": "**¿Asíntota horizontal?** El grado del numerador ($2$) es mayor que el del denominador ($1$), así que $\\lim_{x \\to \\pm \\infty} f(x) = \\pm \\infty$. **No hay asíntota horizontal.**",
               "justificacion_md": "Cuando el grado de arriba supera al de abajo, $f$ no se acerca a un valor finito en el infinito.",
               "es_resultado": False},
              {"accion_md": "**Buscamos asíntota oblicua $y = mx + n$.** Calculamos $m$:\n\n$$m = \\lim_{x \\to +\\infty} \\dfrac{f(x)}{x} = \\lim_{x \\to +\\infty} \\dfrac{x^2 + 3x + 2}{x \\cdot x} = \\lim_{x \\to +\\infty} \\dfrac{x^2 + 3x + 2}{x^2} = 1$$",
               "justificacion_md": "Dividimos por la potencia más alta como antes; los términos de menor grado se desvanecen.",
               "es_resultado": False},
              {"accion_md": "**Calculamos $n$:**\n\n$$n = \\lim_{x \\to +\\infty}[f(x) - 1 \\cdot x] = \\lim_{x \\to +\\infty}\\left[\\dfrac{x^2+3x+2}{x} - x\\right] = \\lim_{x \\to +\\infty} \\dfrac{x^2 + 3x + 2 - x^2}{x} = \\lim_{x \\to +\\infty} \\dfrac{3x + 2}{x} = 3$$",
               "justificacion_md": "Restamos $mx = x$ del cociente para extraer la \"parte lineal\". El residuo es lo que tiende a $n$.",
               "es_resultado": False},
              {"accion_md": "**Asíntota oblicua:** $y = x + 3$.\n\n**Resumen para esta función:** asíntota vertical $x = 0$; asíntota oblicua $y = x + 3$ por ambos lados.",
               "justificacion_md": "Una función racional con grado del numerador exactamente *uno mayor* que el del denominador siempre tiene asíntota oblicua. Una alternativa más rápida es **dividir polinomios**: $\\dfrac{x^2+3x+2}{x} = x + 3 + \\dfrac{2}{x}$, donde el término $2/x \\to 0$ deja la asíntota $y = x + 3$ a la vista.",
               "es_resultado": True},
          ]),

        b("grafico_desmos",
          expresiones=[
              "h(x) = (x^2 + 3x + 2)/x",
              "y = x + 3",
              "x = 0",
          ],
          guia_md=(
              "Compara la gráfica de $h(x) = \\dfrac{x^2+3x+2}{x}$ con la recta $y = x + 3$ (la asíntota oblicua) y con el eje vertical $x = 0$ (la asíntota vertical). "
              "Acércate al origen para ver la asíntota vertical, y aléjate hacia $\\pm \\infty$ para ver cómo la curva se pega a la recta $y = x + 3$."
          ),
          altura=420),

        b("verificacion",
          intro_md="Verifica el manejo de los tres tipos:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuántas asíntotas horizontales puede tener una función?",
                  "opciones_md": ["Como mucho una.", "Exactamente dos siempre.", "Como mucho dos: una para $x \\to +\\infty$ y otra para $x \\to -\\infty$.", "Infinitas."],
                  "correcta": "C",
                  "explicacion_md": (
                      "Cada lado del infinito puede dar a lo sumo un valor distinto. Por ejemplo, $\\arctan x$ tiene $y = \\pi/2$ a la derecha y $y = -\\pi/2$ a la izquierda — **dos asíntotas horizontales**. "
                      "Una función puede tener una, dos, o ninguna; nunca más."
                  ),
              },
              {
                  "enunciado_md": "Para $f(x) = \\dfrac{x^2 + 1}{x - 1}$, ¿qué asíntotas tiene?",
                  "opciones_md": [
                      "Solo asíntota horizontal $y = 1$.",
                      "Asíntota vertical $x = 1$ y asíntota oblicua.",
                      "Asíntota vertical $x = 1$ y horizontal $y = 1$.",
                      "Solo asíntota oblicua, sin verticales.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "El denominador se anula en $x = 1$ (numerador no), así que hay **asíntota vertical $x = 1$**. "
                      "El grado del numerador ($2$) es uno mayor que el del denominador ($1$), así que **no hay horizontal pero sí oblicua**. "
                      "Dividiendo polinomios: $\\dfrac{x^2+1}{x-1} = x + 1 + \\dfrac{2}{x-1}$, así la oblicua es $y = x + 1$."
                  ),
              },
          ]),

        b("errores_comunes",
          items_md=[
              "**Asumir asíntota vertical donde el denominador se anula sin verificar el numerador.** Si numerador y denominador se anulan al mismo tiempo, puede haber cancelación y solo discontinuidad removible. Ejemplo: $\\dfrac{x^2-1}{x-1} = x + 1$ para $x \\neq 1$. No hay asíntota vertical en $x = 1$, sólo un agujero.",
              "**Buscar asíntota oblicua cuando ya hay horizontal.** Si $\\lim_{x \\to \\infty} f(x)$ es finito, hay horizontal y **no** hay oblicua del mismo lado. Las dos son exclusivas.",
              "**Calcular $m$ con la fórmula $\\lim f(x)/x$ y obtener $0$, y aun así seguir buscando $n$.** Si $m = 0$, no hay oblicua — es una horizontal $y = b$ que se calcula con $b = \\lim f(x)$ directamente.",
              "**Olvidar que las asíntotas pueden ser distintas para $x \\to +\\infty$ y $x \\to -\\infty$.** Hay que calcular ambos lados; no asumir simetría.",
              "**Dividir polinomios solo para encontrar oblicuas y olvidar el residuo.** El residuo $R(x)/Q(x)$ tiende a $0$ en el infinito, lo que es exactamente lo que hace de la parte cociente una asíntota.",
          ]),

        b("resumen",
          puntos_md=[
              "**Verticales** ($x = a$): donde $\\lim_{x \\to a^{\\pm}} f(x) = \\pm \\infty$. Típicamente, donde el denominador se anula (sin cancelarse con el numerador).",
              "**Horizontales** ($y = b$): donde $\\lim_{x \\to \\pm\\infty} f(x) = b$ finito. Una función puede tener hasta dos (una por lado).",
              "**Oblicuas** ($y = mx + n$): donde $\\lim_{x \\to \\pm\\infty}[f(x) - (mx+n)] = 0$. Existen solo si **no** hay horizontal del mismo lado y $f$ crece linealmente.",
              "**Cálculo de $m, n$:** $m = \\lim f(x)/x$, $n = \\lim [f(x) - mx]$.",
              "**Atajo para racionales:** dividir polinomios. El cociente da la asíntota (oblicua si es de grado 1, horizontal si es constante); el residuo tiende a $0$.",
              "**Próxima lección:** una guía completa de técnicas para resolver límites — el caja de herramientas práctica del capítulo."
          ]),
    ]

    return {
        "id": "lec-limites-1-6-asintotas",
        "title": "Asíntotas",
        "description": "Asíntotas verticales, horizontales y oblicuas. Cómo calcularlas mediante límites.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 6,
    }


# =====================================================================
# LECCIÓN 1.7 — Resolver límites
# =====================================================================
def lesson_1_7():
    blocks = [
        b("texto", body_md=(
            "Esta es la lección práctica del capítulo: una **guía paso a paso** para resolver cualquier límite que aparezca en un control. Lo que cambia entre los problemas no es la teoría — eso ya lo cubrimos — sino qué **técnica algebraica** elegir según la indeterminación que encontremos.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar una **estrategia ordenada** ante un límite cualquiera.\n"
            "- Resolver indeterminaciones $\\frac{0}{0}$ con **factorización**, **racionalización** y **L'Hôpital** (mencionado, se desarrolla en derivadas).\n"
            "- Manejar límites con **funciones trigonométricas transformadas** mediante cambio de variable.\n"
            "- Resolver **límites al infinito** dividiendo por la potencia dominante.\n"
            "- Reconocer cuándo el **teorema del sándwich** es la herramienta correcta."
        )),

        b("intuicion",
          titulo="Hay un protocolo: si X falla, intentar Y",
          body_md=(
              "Frente a cualquier límite, sigue siempre el mismo protocolo:\n\n"
              "**Paso 1 — Sustitución directa.** Si la función es continua en el punto, evalúa.\n\n"
              "**Paso 2 — Si da $\\dfrac{c}{0}$ (con $c \\neq 0$).** No es indeterminación: probablemente hay asíntota vertical. Calcula laterales.\n\n"
              "**Paso 3 — Si da $\\dfrac{0}{0}$ o similar.** Es **indeterminación**. Aplica una técnica algebraica:\n\n"
              "- Factorización (cuando hay polinomios).\n"
              "- Racionalización (cuando hay raíces).\n"
              "- Regla de L'Hôpital (rápida en muchos casos, requiere derivadas).\n"
              "- Cambio de variable (especialmente con trigonométricas).\n\n"
              "**Paso 4 — Funciones trigonométricas transformadas.** Cambio de variable para reducir al límite fundamental.\n\n"
              "**Paso 5 — Límites al infinito.** Divide numerador y denominador por la potencia más alta.\n\n"
              "**Paso 6 — Si nada de lo anterior funciona.** Sándwich, manipulación más creativa, identidades especiales."
          )),

        b("definicion",
          titulo="Paso 1 — Sustitución directa",
          body_md=(
              "Si $f$ es continua en $a$, entonces $\\lim_{x \\to a} f(x) = f(a)$. Esto es lo primero que se intenta. **Si funciona, el problema está resuelto.**"
          )),

        b("ejemplo_resuelto",
          titulo="$\\lim_{x \\to \\pi} \\sin(x)$",
          problema_md="Resolver el límite.",
          pasos=[
              {"accion_md": "$\\sin$ es continua en todo $\\mathbb{R}$, en particular en $\\pi$. Evaluamos: $\\sin(\\pi) = 0$.",
               "justificacion_md": "Sustitución directa.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{x \\to \\pi} \\sin(x) = 0$.",
               "justificacion_md": "**No siempre el límite va a ser tan fácil.** Pero cuando lo es, ahorra tiempo intentar la sustitución antes de cualquier otra cosa.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Paso 2 — Si da $\\dfrac{c}{0}$ con $c \\neq 0$",
          body_md=(
              "**No es indeterminación.** El comportamiento es de tipo \"explota\": la función tiende a $\\pm \\infty$. Hay que calcular los **laterales** para ver de qué lado va a cada infinito.\n\n"
              "$$\\lim_{x \\to a^{\\pm}} \\dfrac{c}{(x-a)^k}$$\n\n"
              "El signo dependerá del signo de $c$, del signo del denominador en cada lado y de si la potencia $k$ es par o impar. **No confundir con $\\dfrac{0}{0}$**, que sí es indeterminación."
          )),

        b("ejemplo_resuelto",
          titulo="$\\lim_{x \\to 0} \\dfrac{1}{x^2}$",
          problema_md="Calcular el límite.",
          pasos=[
              {"accion_md": "Sustitución directa daría $\\dfrac{1}{0}$, que no es indeterminación: tiende a infinito.",
               "justificacion_md": "Numerador finito y denominador tendiendo a $0$: hay asíntota vertical.",
               "es_resultado": False},
              {"accion_md": "Para $x \\to 0^+$: $x^2 \\to 0^+$, así $\\dfrac{1}{x^2} \\to +\\infty$. Para $x \\to 0^-$: $x^2 \\to 0^+$ también (por el cuadrado), así $\\dfrac{1}{x^2} \\to +\\infty$.",
               "justificacion_md": "El cuadrado siempre es positivo, por eso ambos laterales coinciden en $+\\infty$.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{x \\to 0} \\dfrac{1}{x^2} = +\\infty$. Hay asíntota vertical en $x = 0$.",
               "justificacion_md": "Cuando ambos laterales coinciden en el mismo signo de infinito, escribimos el límite como $\\pm \\infty$. Si no coincidieran, simplemente no existe.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Paso 3a — Indeterminación $\\dfrac{0}{0}$ con factorización",
          body_md=(
              "Cuando numerador y denominador se anulan en $a$, es porque ambos tienen $(x - a)$ como factor. La técnica es **factorizarlos y cancelar** ese factor común.\n\n"
              "Útil con polinomios o expresiones algebraicas reconocibles."
          )),

        b("ejemplo_resuelto",
          titulo="Factorización: $\\lim_{x \\to 1} \\dfrac{x^3 - 1}{x^2 - 1}$",
          problema_md="Resolver la indeterminación.",
          pasos=[
              {"accion_md": "Sustituyendo: $\\dfrac{0}{0}$. Indeterminación. Factorizamos.",
               "justificacion_md": "Tanto numerador como denominador valen $0$ en $x=1$, así que ambos contienen $(x-1)$.",
               "es_resultado": False},
              {"accion_md": "$x^3 - 1 = (x-1)(x^2 + x + 1)$ (diferencia de cubos). $x^2 - 1 = (x-1)(x+1)$ (diferencia de cuadrados).",
               "justificacion_md": "Las identidades clásicas: $a^3 - b^3 = (a-b)(a^2+ab+b^2)$ y $a^2 - b^2 = (a-b)(a+b)$.",
               "es_resultado": False},
              {"accion_md": "$\\dfrac{x^3-1}{x^2-1} = \\dfrac{(x-1)(x^2+x+1)}{(x-1)(x+1)} = \\dfrac{x^2+x+1}{x+1}$ para $x \\neq 1$.",
               "justificacion_md": "Cancelamos el factor $(x-1)$ que era el problema. El límite ignora el punto $x=1$, así que la cancelación es legítima.",
               "es_resultado": False},
              {"accion_md": "Sustitución directa en la expresión simplificada: $\\lim_{x \\to 1} \\dfrac{x^2+x+1}{x+1} = \\dfrac{3}{2}$.",
               "justificacion_md": "Una vez cancelado el factor, la nueva fracción es continua en $1$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Paso 3b — Indeterminación con raíces: racionalización",
          body_md=(
              "Cuando el numerador (o denominador) tiene raíces y produce $\\dfrac{0}{0}$, multiplicamos arriba y abajo por el **conjugado** $\\sqrt{A} + \\sqrt{B}$ para usar la identidad $(a-b)(a+b) = a^2 - b^2$ y eliminar la raíz problemática."
          )),

        b("ejemplo_resuelto",
          titulo="Racionalización: $\\lim_{x \\to 0} \\dfrac{\\sqrt{1+2x} - \\sqrt{1-3x}}{x}$",
          problema_md="Resolver.",
          pasos=[
              {"accion_md": "Sustitución directa: $\\dfrac{1 - 1}{0} = \\dfrac{0}{0}$, indeterminación.",
               "justificacion_md": "El numerador tiende a $0$ por anularse las raíces, no por cancelación de un factor obvio.",
               "es_resultado": False},
              {"accion_md": "Multiplicamos arriba y abajo por el **conjugado** $\\sqrt{1+2x} + \\sqrt{1-3x}$:\n\n$$\\dfrac{(\\sqrt{1+2x}-\\sqrt{1-3x})(\\sqrt{1+2x}+\\sqrt{1-3x})}{x(\\sqrt{1+2x}+\\sqrt{1-3x})}$$",
               "justificacion_md": "El conjugado de $\\sqrt{A} - \\sqrt{B}$ es $\\sqrt{A} + \\sqrt{B}$. Su producto da $A - B$, eliminando las raíces.",
               "es_resultado": False},
              {"accion_md": "El numerador se simplifica: $(1+2x) - (1-3x) = 5x$.\n\n$$= \\dfrac{5x}{x(\\sqrt{1+2x}+\\sqrt{1-3x})}$$",
               "justificacion_md": "El factor $x$ del numerador es justo lo que necesitamos para cancelar el del denominador.",
               "es_resultado": False},
              {"accion_md": "Cancelamos $x$:\n\n$$\\lim_{x \\to 0} \\dfrac{5}{\\sqrt{1+2x}+\\sqrt{1-3x}} = \\dfrac{5}{1 + 1} = \\dfrac{5}{2}$$",
               "justificacion_md": "Una vez cancelado, sustituimos directamente.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Paso 3c — Regla de L'Hôpital (presentación)",
          body_md=(
              "Para indeterminaciones $\\dfrac{0}{0}$ o $\\dfrac{\\infty}{\\infty}$:\n\n"
              "$$\\lim_{x \\to a} \\dfrac{f(x)}{g(x)} = \\lim_{x \\to a} \\dfrac{f'(x)}{g'(x)}$$\n\n"
              "siempre que el segundo límite exista y se cumplan ciertas hipótesis técnicas. **Es una herramienta poderosa pero requiere derivadas**, que veremos en el capítulo siguiente. Aquí solo lo enunciamos para uso futuro.\n\n"
              "**No usar como atajo en problemas que se resuelven con factorización o racionalización trivial:** los profesores suelen exigir el método específico en esos casos."
          )),

        b("ejemplo_resuelto",
          titulo="L'Hôpital aplicado dos veces: $\\lim_{x \\to 0} \\dfrac{e^x - 1 - x}{x^2}$",
          problema_md="Resolver el límite.",
          pasos=[
              {"accion_md": "Sustitución directa: $\\dfrac{1 - 1 - 0}{0} = \\dfrac{0}{0}$. Aplicamos L'Hôpital (derivamos numerador y denominador):\n\n$$\\lim_{x \\to 0} \\dfrac{e^x - 1}{2x}$$",
               "justificacion_md": "Las derivadas: $(e^x - 1 - x)' = e^x - 1$ y $(x^2)' = 2x$.",
               "es_resultado": False},
              {"accion_md": "Volvemos a sustituir: $\\dfrac{e^0 - 1}{0} = \\dfrac{0}{0}$. Aplicamos L'Hôpital de nuevo:\n\n$$\\lim_{x \\to 0} \\dfrac{e^x}{2}$$",
               "justificacion_md": "L'Hôpital se puede aplicar **repetidamente** mientras la indeterminación persista.",
               "es_resultado": False},
              {"accion_md": "Sustitución directa: $\\dfrac{e^0}{2} = \\dfrac{1}{2}$.",
               "justificacion_md": "Esta vez, ya no hay indeterminación.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{x \\to 0} \\dfrac{e^x - 1 - x}{x^2} = \\dfrac{1}{2}$.",
               "justificacion_md": "L'Hôpital es muy rápido cuando aplica. Una alternativa sería usar la serie de Taylor de $e^x = 1 + x + \\dfrac{x^2}{2} + \\ldots$ y simplificar, pero requiere herramientas que también vienen después.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Paso 4 — Trigonométricas transformadas: cambio de variable",
          body_md=(
              "Cuando aparece $\\sin$, $\\cos$, $\\tan$ con argumento desplazado o escalado, hacemos un **cambio de variable** que reduzca al límite fundamental $\\dfrac{\\sin u}{u} \\to 1$ cuando $u \\to 0$.\n\n"
              "**Receta:** si el argumento problemático es $g(x)$, define $u = g(x)$. Cuando $x \\to a$, $u$ tiende a $g(a)$ — y el límite se reduce a uno conocido en la nueva variable."
          )),

        b("ejemplo_resuelto",
          titulo="Cambio de variable: $\\lim_{x \\to \\pi/2} \\dfrac{\\sin(x - \\pi/2)}{x - \\pi/2}$",
          problema_md="Resolver el límite.",
          pasos=[
              {"accion_md": "Cambio de variable: $u = x - \\pi/2$. Cuando $x \\to \\pi/2$, $u \\to 0$.",
               "justificacion_md": "El cambio convierte el argumento problemático en una variable simple que tiende a $0$.",
               "es_resultado": False},
              {"accion_md": "El límite se transforma:\n\n$$\\lim_{u \\to 0} \\dfrac{\\sin u}{u} = 1$$",
               "justificacion_md": "Es el límite trigonométrico fundamental que vimos en la lección 1.1.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{x \\to \\pi/2} \\dfrac{\\sin(x - \\pi/2)}{x - \\pi/2} = 1$.",
               "justificacion_md": "**Patrón general:** cuando aparece $\\sin(g(x))/g(x)$ y $g(x) \\to 0$, el límite vale $1$. La sustitución $u = g(x)$ es un automatismo útil.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Paso 5 — Sándwich",
          body_md=(
              "Si la función contiene un factor **acotado** ($\\sin$, $\\cos$, parte fraccionaria) que oscila pero no diverge, multiplicado por algo que tiende a $0$, el sándwich resuelve el caso:\n\n"
              "Si $|f(x)| \\leq h(x)$ y $h(x) \\to 0$, entonces $f(x) \\to 0$.\n\n"
              "Útil cuando las leyes algebraicas no aplican porque el factor oscilante no tiene límite por sí mismo."
          )),

        b("ejemplo_resuelto",
          titulo="$\\lim_{x \\to 0} x \\sin\\left(\\dfrac{1}{x}\\right)$",
          problema_md="Resolver el límite.",
          pasos=[
              {"accion_md": "$\\sin(1/x)$ oscila salvajemente cerca de $x = 0$, pero está **acotado**: $-1 \\leq \\sin(1/x) \\leq 1$.",
               "justificacion_md": "El acotamiento es lo que activa el sándwich.",
               "es_resultado": False},
              {"accion_md": "Multiplicamos por $|x|$:\n\n$$-|x| \\leq x \\sin\\left(\\dfrac{1}{x}\\right) \\leq |x|$$",
               "justificacion_md": "Tomamos valor absoluto al multiplicar para evitar problemas de signo.",
               "es_resultado": False},
              {"accion_md": "Como $\\lim_{x \\to 0} (-|x|) = 0$ y $\\lim_{x \\to 0} |x| = 0$, por el **teorema del sándwich**:\n\n$$\\lim_{x \\to 0} x \\sin\\left(\\dfrac{1}{x}\\right) = 0$$",
               "justificacion_md": "Atrapado entre dos cero, el resultado es cero. **Importante:** este límite **no se puede resolver por leyes algebraicas** porque $\\sin(1/x)$ no tiene límite. El sándwich es la herramienta correcta.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Paso 6 — Límites al infinito",
          body_md=(
              "Para $x \\to +\\infty$ (o $-\\infty$) en una fracción de polinomios u otras expresiones algebraicas: **dividir numerador y denominador por la potencia más alta de $x$** que aparezca.\n\n"
              "Las potencias inversas (tipo $1/x^k$ con $k > 0$) tienden a $0$, dejando solo los términos dominantes."
          )),

        b("ejemplo_resuelto",
          titulo="Polinomios al infinito: $\\lim_{x \\to +\\infty} \\dfrac{3x^3 + 2x^2 - 1}{2x^3 - x + 4}$",
          problema_md="Resolver el límite.",
          pasos=[
              {"accion_md": "La potencia más alta es $x^3$. Dividimos numerador y denominador por $x^3$:\n\n$$\\dfrac{3 + \\dfrac{2}{x} - \\dfrac{1}{x^3}}{2 - \\dfrac{1}{x^2} + \\dfrac{4}{x^3}}$$",
               "justificacion_md": "Esta es la maniobra estándar.",
               "es_resultado": False},
              {"accion_md": "Cuando $x \\to +\\infty$, todos los términos $1/x^k$ con $k > 0$ tienden a $0$:\n\n$$\\dfrac{3 + 0 - 0}{2 - 0 + 0} = \\dfrac{3}{2}$$",
               "justificacion_md": "Solo sobreviven los coeficientes principales.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{x \\to +\\infty} \\dfrac{3x^3+2x^2-1}{2x^3-x+4} = \\dfrac{3}{2}$.",
               "justificacion_md": "**Atajo memorizable:** cuando los grados del numerador y del denominador coinciden, el límite al infinito es el cociente de los coeficientes principales (acá $3/2$).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Diferencia de raíces al infinito: $\\lim_{x \\to +\\infty}(\\sqrt{x^2 + 5x} - x)$",
          problema_md="Resolver el límite, una indeterminación $\\infty - \\infty$.",
          pasos=[
              {"accion_md": "Sustitución directa: $\\infty - \\infty$, indeterminación. Multiplicamos y dividimos por el **conjugado** $\\sqrt{x^2+5x} + x$:\n\n$$\\dfrac{(\\sqrt{x^2+5x} - x)(\\sqrt{x^2+5x} + x)}{\\sqrt{x^2+5x} + x} = \\dfrac{(x^2+5x) - x^2}{\\sqrt{x^2+5x} + x} = \\dfrac{5x}{\\sqrt{x^2+5x} + x}$$",
               "justificacion_md": "La racionalización elimina la diferencia de raíces. Es la técnica análoga al paso 3b, pero al infinito.",
               "es_resultado": False},
              {"accion_md": "Dividimos por $x$ (la potencia más alta) numerador y denominador. **Cuidado con las raíces:** $\\sqrt{x^2 + 5x} = |x|\\sqrt{1 + 5/x}$, y para $x \\to +\\infty$, $|x| = x$, así $\\sqrt{x^2+5x}/x = \\sqrt{1 + 5/x}$.\n\n$$\\dfrac{5}{\\sqrt{1 + \\frac{5}{x}} + 1}$$",
               "justificacion_md": "El paso del valor absoluto es clave: para $x \\to -\\infty$, $|x| = -x$ y los signos se invierten — pero aquí no aplica.",
               "es_resultado": False},
              {"accion_md": "Tomando el límite cuando $x \\to +\\infty$, $5/x \\to 0$:\n\n$$\\dfrac{5}{\\sqrt{1+0}+1} = \\dfrac{5}{2}$$",
               "justificacion_md": "El resultado es finito, lo que indica que la función tiene una asíntota oblicua en el infinito.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica que sabes elegir la técnica adecuada:",
          preguntas=[
              {
                  "enunciado_md": "Para $\\lim_{x \\to 4} \\dfrac{x^2 - 16}{x - 4}$, ¿cuál es la técnica más apropiada?",
                  "opciones_md": ["Sustitución directa", "Factorización", "Racionalización", "Sándwich"],
                  "correcta": "B",
                  "explicacion_md": (
                      "Sustitución directa daría $0/0$ (indeterminación). El numerador es $x^2 - 16 = (x-4)(x+4)$, así que **factorización** cancela el factor problemático: $\\dfrac{(x-4)(x+4)}{x-4} = x+4 \\to 8$. "
                      "La racionalización aplica con raíces; el sándwich con factores acotados."
                  ),
              },
              {
                  "enunciado_md": "Para $\\lim_{x \\to +\\infty} \\dfrac{4x^2 + 1}{x^2 - 7}$, el resultado es:",
                  "opciones_md": ["$0$", "$1$", "$4$", "$+\\infty$"],
                  "correcta": "C",
                  "explicacion_md": (
                      "Mismo grado en numerador y denominador ($2$): el límite es el cociente de los coeficientes principales, $4/1 = 4$. "
                      "Equivalente: dividir por $x^2$ y tomar límite, $\\dfrac{4 + 1/x^2}{1 - 7/x^2} \\to \\dfrac{4}{1} = 4$."
                  ),
              },
          ]),

        b("errores_comunes",
          items_md=[
              "**Aplicar L'Hôpital sin verificar la indeterminación.** L'Hôpital solo aplica con $\\dfrac{0}{0}$ o $\\dfrac{\\infty}{\\infty}$. Usarlo en otros casos da resultados incorrectos.",
              "**Multiplicar por el conjugado equivocado.** El conjugado de $\\sqrt{A} - \\sqrt{B}$ es $\\sqrt{A} + \\sqrt{B}$, no $-\\sqrt{A} + \\sqrt{B}$. Verificar siempre que la multiplicación produce $A - B$.",
              "**Olvidar el valor absoluto en raíces al infinito por el lado negativo.** Para $x \\to -\\infty$, $\\sqrt{x^2} = |x| = -x$ (no $x$). Confundir esto invierte signos.",
              "**Cancelar antes de evaluar la indeterminación.** El paso 0 siempre debe ser intentar la sustitución directa: si funciona, ahorra trabajo y evita errores algebraicos.",
              "**Pensar que $\\infty - \\infty = 0$.** Es **indeterminación**: puede dar cualquier número finito, $\\pm \\infty$, o no existir. Hay que manipular algebraicamente para resolverla.",
          ]),

        b("resumen",
          puntos_md=[
              "**Protocolo:** sustitución directa → $\\dfrac{c}{0}$ con laterales → indeterminación con técnica algebraica → trigonométricas con cambio de variable → al infinito con división por potencia dominante → sándwich como último recurso.",
              "**Indeterminaciones más comunes:** $\\dfrac{0}{0}$, $\\dfrac{\\infty}{\\infty}$, $0 \\cdot \\infty$, $\\infty - \\infty$, $1^\\infty$, $0^0$, $\\infty^0$.",
              "**Factorización:** para polinomios. Identificar el factor común $(x-a)$ y cancelarlo.",
              "**Racionalización:** para raíces. Multiplicar arriba y abajo por el conjugado.",
              "**L'Hôpital:** atajo poderoso para $\\dfrac{0}{0}$ o $\\dfrac{\\infty}{\\infty}$, requiere derivadas (próximo capítulo).",
              "**Cambio de variable:** reducir trigonométricas transformadas a $\\dfrac{\\sin u}{u} \\to 1$.",
              "**Sándwich:** para factores oscilantes acotados multiplicados por algo que tiende a $0$.",
              "**Próximo capítulo:** Derivadas — donde la regla de L'Hôpital pasa a ser aplicable y aparece una nueva familia de límites a resolver (cocientes incrementales)."
          ]),
    ]

    return {
        "id": "lec-limites-1-7-resolver",
        "title": "Resolver límites: estrategia y técnicas",
        "description": "Guía paso a paso: sustitución directa, factorización, racionalización, L'Hôpital, cambio de variable, sándwich y límites al infinito.",
        "blocks": blocks,
        "duration_minutes": 60,
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

    # ---- Renombrar/reordenar el capítulo de Derivadas, si existe ----
    chapter_derivadas = await db.chapters.find_one({"id": "ch-derivadas"})
    if chapter_derivadas:
        await db.chapters.update_one(
            {"id": "ch-derivadas"},
            {"$set": {"title": "Derivadas", "order": 2}}
        )
        print("✓ Capítulo de Derivadas reordenado a order=2")

    # ---- Crear/actualizar el capítulo de Límites y Continuidad ----
    chapter_id = "ch-limites-continuidad"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Límites y Continuidad",
        "description": "Concepto de límite, definición formal, propiedades, continuidad, TVI, asíntotas y técnicas de resolución.",
        "order": 1,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    # ---- Insertar las 7 lecciones ----
    builders = [lesson_1_1, lesson_1_2, lesson_1_3, lesson_1_4, lesson_1_5, lesson_1_6, lesson_1_7]
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
    print(f"✅ Total: 7 lecciones, {total_blocks} bloques. Capítulo 1 listo.")
    print()
    print("Lecciones disponibles en:")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
