"""
Seed del curso Introducción al Álgebra — Capítulo 2: Números Naturales.
4 lecciones (alineadas con MAT1207 PUC):
  2.1 Inducción
  2.2 Sucesiones
  2.3 Sumas Finitas
  2.4 Teorema del Binomio

ENFOQUE: usa el lenguaje del Cap. 1 (lógica, demostración, cuantificadores) para
demostrar propiedades válidas para todos los naturales. Inducción es la herramienta
estrella; sucesiones y sumas la ponen en práctica. El Teorema del Binomio cierra
el capítulo conectando inducción con coeficientes binomiales y combinatoria.

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

CHAPTER_ID = "ch-ia-naturales"
CHAPTER_TITLE = "Números Naturales"
CHAPTER_DESCRIPTION = (
    "El Principio de Inducción Matemática y sus aplicaciones. Estudio de "
    "sucesiones (aritméticas, geométricas y generales), sumas finitas con "
    "notación sigma, fórmulas cerradas para sumas de potencias y sumas "
    "telescópicas. Cierra con el Teorema del Binomio y los coeficientes "
    "binomiales del Triángulo de Pascal."
)
CHAPTER_ORDER = 2


# ============================================================================
# 2.1 Inducción
# ============================================================================
def lesson_2_1():
    blocks = [
        b("texto", body_md=(
            "Cuando queremos demostrar que una propiedad es válida para **todos** "
            "los números naturales $1, 2, 3, \\ldots$, las reglas básicas del "
            "álgebra no son suficientes. Lo que estas reglas no captan es el hecho "
            "fundamental de que los naturales vienen en una **secuencia**: cualquier "
            "natural puede obtenerse partiendo del $1$ y sumándole $1$ las veces "
            "necesarias.\n\n"
            "La **inducción matemática** es precisamente el método que aprovecha "
            "esta estructura para demostrar enunciados sobre todos los naturales "
            "de manera rigurosa y elegante. Al terminar la lección serás capaz de:\n\n"
            "- Enunciar el **Principio de Inducción** y entender la analogía del dominó.\n"
            "- Identificar correctamente $P(n)$, el **caso base** $P(1)$ y el **paso "
            "inductivo** $P(k) \\Rightarrow P(k+1)$.\n"
            "- Demostrar **igualdades**, **desigualdades** y propiedades de "
            "**divisibilidad** por inducción.\n"
            "- Generalizar la inducción a enunciados válidos para todo $n \\ge n_0$."
        )),

        b("teorema",
          enunciado_md=(
              "**Principio de Inducción Matemática.** Sea $P(n)$ una afirmación "
              "que involucra al número natural $n$. Entonces $P(n)$ es verdadera "
              "para todo $n \\in \\mathbb{N}$ si se cumplen las dos condiciones:\n\n"
              "1. **Caso base:** $P(1)$ es verdadera.\n\n"
              "2. **Paso inductivo:** $P(k) \\Rightarrow P(k+1)$ para todo $k \\in \\mathbb{N}$.\n\n"
              "La hipótesis $P(k)$ que se asume verdadera en el paso inductivo se "
              "denomina **hipótesis inductiva**."
          )),

        b("intuicion", body_md=(
            "**La analogía del dominó.** Imaginá los naturales alineados como "
            "fichas de dominó. Si sabemos que:\n\n"
            "- la **primera ficha cae** (caso base $P(1)$), y\n"
            "- **cada ficha al caer derriba a la siguiente** (paso inductivo "
            "$P(k) \\Rightarrow P(k+1)$),\n\n"
            "entonces **todas las fichas caerán** sin excepción. Las dos "
            "condiciones son inseparables: si la primera no cae, ninguna cae; "
            "si están demasiado separadas para derribarse en cadena, la caída "
            "se detiene en algún punto."
        )),

        fig(
            "Ilustración de fichas de dominó alineadas en perspectiva ligeramente lateral, etiquetadas P(1), P(2), P(3), P(4), P(5), ... la primera (P(1)) cayendo hacia la derecha en plena animación de caída, las siguientes paradas pero claramente a punto de caer por efecto cascada. "
            "Flecha curva entre cada par de fichas con la etiqueta 'P(k) ⇒ P(k+1)'. Fondo blanco, fichas en color teal #06b6d4 con borde negro, flechas en ámbar #f59e0b. " + STYLE
        ),

        b("definicion",
          titulo="Plantilla estándar de demostración por inducción",
          body_md=(
              "Toda demostración por inducción sigue la misma estructura:\n\n"
              "**Demostración.** Utilizamos inducción sobre $n$.\n\n"
              "**Caso base:** Demostrar el enunciado $P(1)$ por cálculo directo.\n\n"
              "**Paso inductivo:** Supongamos como **hipótesis inductiva** que "
              "$P(k)$ es verdadera para algún natural $k$. Entonces deducir que "
              "$P(k+1)$ es verdadera. Esto demuestra el paso inductivo.\n\n"
              "**Conclusión:** Por lo tanto, por inducción, $P(n)$ es verdadera "
              "para todos los naturales $n$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Suma telescópica clásica",
          problema_md=(
              "Demuestre por inducción que para todo $n \\in \\mathbb{N}$:\n"
              "$$\\frac{1}{1\\cdot 2} + \\frac{1}{2\\cdot 3} + \\cdots + \\frac{1}{n(n+1)} = \\frac{n}{n+1}.$$"
          ),
          pasos=[
              {"accion_md": (
                  "Sea $P(n)$ el enunciado dado. **Caso base ($n=1$):** lado izquierdo "
                  "$= \\dfrac{1}{1\\cdot 2} = \\dfrac{1}{2}$ y lado derecho "
                  "$= \\dfrac{1}{1+1} = \\dfrac{1}{2}$. Como coinciden, $P(1)$ es verdadero."
               ),
               "justificacion_md": "Verificación directa.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso inductivo:** asumimos $P(k)$ verdadera, es decir,\n"
                  "$$\\frac{1}{1\\cdot 2} + \\cdots + \\frac{1}{k(k+1)} = \\frac{k}{k+1}.$$\n"
                  "Queremos probar $P(k+1)$. Agrupamos el lado izquierdo de $P(k+1)$:\n"
                  "$$\\underbrace{\\frac{1}{1\\cdot 2} + \\cdots + \\frac{1}{k(k+1)}}_{=\\,k/(k+1)\\;\\text{por HI}} + \\frac{1}{(k+1)(k+2)}.$$"
               ),
               "justificacion_md": "Aplicamos la hipótesis inductiva al primer bloque.",
               "es_resultado": False},
              {"accion_md": (
                  "Sumamos las fracciones (denominador común $(k+1)(k+2)$):\n"
                  "$$\\frac{k}{k+1} + \\frac{1}{(k+1)(k+2)} = \\frac{k(k+2) + 1}{(k+1)(k+2)} "
                  "= \\frac{k^2 + 2k + 1}{(k+1)(k+2)} = \\frac{(k+1)^2}{(k+1)(k+2)} = \\frac{k+1}{k+2}.$$\n"
                  "Esto es exactamente el lado derecho de $P(k+1)$. $\\blacksquare$"
               ),
               "justificacion_md": "Identificamos $(k+1)^2$ y simplificamos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Desigualdad por inducción",
          problema_md="Pruebe que $n \\le 2^n$ para todo $n \\in \\mathbb{N}$.",
          pasos=[
              {"accion_md": "**Caso base ($n=1$):** $1 \\le 2^1 = 2$. $P(1)$ verdadero.",
               "justificacion_md": "Verificación directa.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso inductivo:** asumimos $k \\le 2^k$ (hipótesis inductiva). Queremos $k+1 \\le 2^{k+1}$. Encadenamos:\n"
                  "$$k + 1 \\le 2^k + 1 \\quad (\\text{por HI})$$\n"
                  "$$\\le 2^k + k \\quad (\\text{como } k \\ge 1)$$\n"
                  "$$\\le 2^k + 2^k \\quad (\\text{por HI nuevamente})$$\n"
                  "$$= 2 \\cdot 2^k = 2^{k+1}.$$"
               ),
               "justificacion_md": "Encadenamos desigualdades elementales reusando la HI.",
               "es_resultado": False},
              {"accion_md": "Por inducción, $n \\le 2^n$ para todo $n \\in \\mathbb{N}$. $\\blacksquare$",
               "justificacion_md": "Ambas condiciones cumplidas.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Divisibilidad por inducción",
          problema_md="Demuestre que para todo $n \\in \\mathbb{N}$, el número $n^3 - n$ es divisible por $3$.",
          pasos=[
              {"accion_md": (
                  "Sea $P(n)$: \"$3 \\mid (n^3 - n)$\", es decir, existe un entero $q$ "
                  "con $n^3 - n = 3q$. **Caso base:** $1^3 - 1 = 0 = 3 \\cdot 0$, "
                  "luego $P(1)$ verdadero."
               ),
               "justificacion_md": "Cálculo directo del caso base.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso inductivo:** asumimos $k^3 - k = 3q$ para algún entero $q$. "
                  "Calculamos:\n"
                  "$$(k+1)^3 - (k+1) = k^3 + 3k^2 + 3k + 1 - k - 1 = (k^3 - k) + 3k^2 + 3k.$$"
               ),
               "justificacion_md": "Desarrollo del cubo y agrupación.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicando la hipótesis inductiva:\n"
                  "$$= 3q + 3k^2 + 3k = 3(q + k^2 + k).$$\n"
                  "Como $q + k^2 + k$ es entero, $(k+1)^3 - (k+1)$ es divisible por $3$. $\\blacksquare$"
               ),
               "justificacion_md": "Factorizamos por $3$ explícitamente.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Inducción generalizada.** Sea $n_0 \\in \\mathbb{Z}$. Si $P(n_0)$ "
              "es verdadera y $P(k) \\Rightarrow P(k+1)$ para todo $k \\ge n_0$, "
              "entonces $P(n)$ es verdadera para todo $n \\ge n_0$.\n\n"
              "Es decir, basta cambiar el caso base de $P(1)$ a $P(n_0)$ — la "
              "estructura del argumento es idéntica."
          )),

        ej(
            "Inducción generalizada: $n^2 \\le 2^n$ para $n \\ge 4$",
            ("Demuestre que para todo natural $n$ tal que $n \\ge 4$ se tiene "
             "$n^2 \\le 2^n$. Tip: el caso base es $n_0 = 4$. La afirmación falla "
             "para $n = 3$ ($9 \\not\\le 8$), por eso necesitamos arrancar en $4$."),
            ["Caso base $n=4$: $4^2 = 16$ y $2^4 = 16$. ¿Qué relación se cumple?",
             "Para el paso, partí de $(k+1)^2 = k^2 + 2k + 1$ y compará $2k+1$ con $k^2$ usando $k \\ge 4$.",
             "Cerrá usando la HI: $k^2 + k^2 = 2k^2 \\le 2 \\cdot 2^k = 2^{k+1}$."],
            ("**Caso base ($n=4$):** $4^2 = 16 \\le 16 = 2^4$. $P(4)$ verdadero.\n\n"
             "**Paso inductivo:** asumimos $k^2 \\le 2^k$ con $k \\ge 4$. Notamos que para $k \\ge 4$, "
             "$k^2 - 2k - 1 = (k-1)^2 - 2 \\ge 9 - 2 = 7 > 0$, luego $2k + 1 \\le k^2$. Entonces:\n"
             "$$(k+1)^2 = k^2 + 2k + 1 \\le k^2 + k^2 = 2k^2 \\le 2 \\cdot 2^k = 2^{k+1}.$$\n"
             "Por inducción generalizada desde $n_0 = 4$, $n^2 \\le 2^n$ para todo $n \\ge 4$. $\\blacksquare$")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "¿Cuáles son los **dos pasos** que componen una demostración por inducción matemática estándar?",
               "opciones_md": ["Caso base $P(0)$ y caso final $P(\\infty)$", "Caso base $P(n_0)$ y paso inductivo $P(k) \\Rightarrow P(k+1)$", "Verificar varios casos $P(1), P(2), P(3)$ y generalizar", "Demostrar $P(k)$ y $P(k-1)$"],
               "correcta": "B",
               "pista_md": "Pensá en el efecto dominó: la primera ficha y el efecto entre fichas consecutivas.",
               "explicacion_md": "Inducción consta de **caso base** ($P(n_0)$ verdadero) y **paso inductivo** (asumiendo $P(k)$ se demuestra $P(k+1)$). Verificar finitos casos individuales no es inducción."},
              {"enunciado_md": "En el paso inductivo de la demostración de $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$, ¿cuál es la **hipótesis inductiva**?",
               "opciones_md": ["$\\sum_{i=1}^{k+1} i = \\frac{(k+1)(k+2)}{2}$", "$\\sum_{i=1}^{k} i = \\frac{k(k+1)}{2}$", "$\\sum_{i=1}^{1} i = 1$", "$P(n)$ es verdadera para todo $n$"],
               "correcta": "B",
               "pista_md": "La hipótesis inductiva es lo que se asume, no lo que se demuestra.",
               "explicacion_md": "La hipótesis inductiva es $P(k)$: se asume que la fórmula vale para $n=k$. La opción A es la **tesis** $P(k+1)$ (lo que hay que demostrar)."},
              {"enunciado_md": "Si en una demostración por inducción **no se usa la hipótesis** $P(k)$ para probar $P(k+1)$, ¿qué significa?",
               "opciones_md": ["La inducción es inválida", "El caso base es innecesario", "Probablemente hay un error o la propiedad admite prueba directa", "La conclusión sigue siendo correcta"],
               "correcta": "C",
               "pista_md": "El núcleo de la inducción es heredar $P(k)$ a $P(k+1)$.",
               "explicacion_md": "Si nunca usás $P(k)$, el paso inductivo está demostrando $P(k+1)$ por sí solo, lo que sugiere o un error en la prueba o que la propiedad puede demostrarse directamente sin inducción."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Olvidar el caso base.** Sin él, el paso inductivo no demuestra nada (la primera ficha podría no caer).",
              "**Olvidar usar la hipótesis inductiva.** Si en el paso inductivo no aparece $P(k)$, casi seguro hay un error o la prueba se puede hacer directa.",
              "**Asumir lo que se quiere probar.** $P(k+1)$ es la **tesis** del paso inductivo, no una hipótesis.",
              "**Inducción aplicada sobre el ente equivocado.** Identificá claramente qué variable es $n$ y cuáles son constantes.",
          ]),

        b("resumen",
          puntos_md=[
              "El **Principio de Inducción** demuestra propiedades para todo $n \\in \\mathbb{N}$ con dos pasos: caso base $P(1)$ y paso inductivo $P(k) \\Rightarrow P(k+1)$.",
              "La estructura es siempre la misma: **identificar $P(n)$ → caso base → paso inductivo (usando HI) → conclusión**.",
              "Aplicaciones típicas: igualdades de sumas, desigualdades, divisibilidad.",
              "**Inducción generalizada** desde $n_0$ permite demostrar $P(n)$ para todo $n \\ge n_0$.",
              "Próxima lección: **sucesiones** y sumas parciales — el contexto natural donde aparece la inducción.",
          ]),
    ]
    return {
        "id": "lec-ia-2-1-induccion",
        "title": "Inducción Matemática",
        "description": "Principio de inducción, plantilla estándar y aplicaciones a igualdades, desigualdades y divisibilidad.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 1,
    }


# ============================================================================
# 2.2 Sucesiones
# ============================================================================
def lesson_2_2():
    blocks = [
        b("texto", body_md=(
            "Las **sucesiones** son uno de los objetos fundamentales en matemáticas: "
            "aparecen en el modelamiento de fenómenos naturales, en el cálculo de "
            "intereses compuestos, en la demografía y en innumerables aplicaciones "
            "de las ciencias.\n\n"
            "En esta lección estudiaremos:\n\n"
            "- La definición de sucesión y sus formas de descripción (verbal, "
            "explícita y recursiva).\n"
            "- **Sumas parciales** y la **notación sigma** ($\\sum$).\n"
            "- Dos familias clave: **sucesiones aritméticas** (crecimiento por "
            "adición constante) y **sucesiones geométricas** (crecimiento por "
            "multiplicación constante).\n"
            "- Fórmulas cerradas para el $n$-ésimo término y para las sumas parciales."
        )),

        b("definicion",
          titulo="Sucesión y formas de descripción",
          body_md=(
              "Una **sucesión de números reales** es una función $f: \\mathbb{N} \\to \\mathbb{R}$ "
              "que asocia a cada natural $n$ un real $f(n) = a_n$, llamado **$n$-ésimo término**. Se escribe\n"
              "$$a_1, a_2, a_3, \\ldots, a_n, \\ldots \\quad\\text{o también}\\quad \\{a_n\\}_{n \\in \\mathbb{N}}.$$\n"
              "Hay tres formas principales de describir una sucesión:\n\n"
              "- **Verbal:** «la sucesión de los cuadrados perfectos» $1, 4, 9, 16, \\ldots$\n"
              "- **Explícita:** una fórmula cerrada para $a_n$. Ejemplo: $a_n = 2n$.\n"
              "- **Recursiva:** cada término en función de los anteriores. Ejemplo: "
              "$a_1 = 2$ y $a_n = a_{n-1} + 2$ para $n \\ge 2$. Caso clásico: el "
              "**factorial** $0! = 1$, $\\;n! = n \\cdot (n-1)!$ para $n \\ge 1$."
          )),

        b("ejemplo_resuelto",
          titulo="Encontrar el término general",
          problema_md=(
              "Encuentre el $n$-ésimo término de las sucesiones:\n\n"
              "(a) $\\dfrac{1}{2}, \\dfrac{3}{4}, \\dfrac{5}{6}, \\dfrac{7}{8}, \\ldots$\n\n"
              "(b) $-2, 4, -8, 16, -32, \\ldots$"
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Numeradores: $1, 3, 5, 7, \\ldots$ son los impares, modelados como $2n - 1$. "
                  "Denominadores: $2, 4, 6, 8, \\ldots$ son los pares, modelados como $2n$. Por tanto:\n"
                  "$$a_n = \\frac{2n - 1}{2n}.$$"
               ),
               "justificacion_md": "Reconocemos los patrones de pares e impares.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Valores absolutos: $2, 4, 8, 16, 32, \\ldots = 2^1, 2^2, 2^3, \\ldots$ "
                  "Los signos alternan empezando por negativo, lo que se modela con $(-1)^n$. Entonces:\n"
                  "$$a_n = (-1)^n \\cdot 2^n = (-2)^n.$$"
               ),
               "justificacion_md": "Combinamos potencia de 2 con factor de signo alternante.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Sumas parciales y notación sigma",
          body_md=(
              "Dada una sucesión $\\{a_n\\}$, la **$n$-ésima suma parcial** es\n"
              "$$S_n = a_1 + a_2 + \\cdots + a_n.$$\n"
              "La sucesión $\\{S_n\\}$ se llama **sucesión de sumas parciales** y "
              "satisface $S_n = S_{n-1} + a_n$ para $n \\ge 2$.\n\n"
              "Para escribir sumas de manera compacta usamos la **notación sigma**:\n"
              "$$\\sum_{k=1}^{n} a_k = a_1 + a_2 + \\cdots + a_n.$$\n"
              "La letra $k$ es el **índice** o contador (es una variable muda — puede "
              "renombrarse). El índice puede comenzar en cualquier entero: "
              "$\\sum_{k=3}^{7} a_k = a_3 + a_4 + a_5 + a_6 + a_7$."
          )),

        b("definicion",
          titulo="Sucesión aritmética",
          body_md=(
              "Una **sucesión aritmética** tiene la forma\n"
              "$$a, \\; a + d, \\; a + 2d, \\; a + 3d, \\; \\ldots$$\n"
              "donde $a = a_1$ es el **primer término** y $d = a_{n+1} - a_n$ es la "
              "**diferencia común** (constante).\n\n"
              "Su **$n$-ésimo término** está dado por\n"
              "$$\\boxed{\\;a_n = a_1 + (n-1)d\\;}$$\n"
              "(verificable por inducción) y la **suma parcial** por\n"
              "$$\\boxed{\\;S_n = \\frac{n}{2}\\bigl[2a_1 + (n-1)d\\bigr] = n \\cdot \\frac{a_1 + a_n}{2}\\;}$$\n"
              "La segunda fórmula tiene una interpretación elegante: $S_n$ es $n$ veces el "
              "**promedio** del primer y el último término."
          )),

        b("ejemplo_resuelto",
          titulo="Suma de una progresión aritmética",
          problema_md="Calcule la suma $5 + 9 + 13 + \\cdots + 49$.",
          pasos=[
              {"accion_md": (
                  "Los términos forman una sucesión aritmética con $a_1 = 5$ y $d = 4$. "
                  "Determinamos la posición de $49$:\n"
                  "$$a_n = 49 \\iff 5 + (n-1) \\cdot 4 = 49 \\iff n = 12.$$"
               ),
               "justificacion_md": "Despeje del índice usando la fórmula del término general.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicamos la fórmula del promedio:\n"
                  "$$S_{12} = 12 \\cdot \\frac{5 + 49}{2} = 12 \\cdot 27 = \\boxed{324}.$$"
               ),
               "justificacion_md": "Sustitución en la segunda fórmula.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Sucesión geométrica",
          body_md=(
              "Una **sucesión geométrica** tiene la forma\n"
              "$$a, \\; ar, \\; ar^2, \\; ar^3, \\; \\ldots$$\n"
              "donde $a = a_1$ es el primer término y $r = \\dfrac{a_{n+1}}{a_n}$ es la "
              "**razón común** (constante, con $a_n \\neq 0$).\n\n"
              "Su **$n$-ésimo término** está dado por\n"
              "$$\\boxed{\\;a_n = a_1 \\cdot r^{n-1}\\;}$$\n"
              "y la **suma parcial** (cuando $r \\neq 1$) por\n"
              "$$\\boxed{\\;S_n = a_1 \\cdot \\frac{1 - r^n}{1 - r}\\;}$$\n"
              "**Cuando $r = 1$** todos los términos son iguales y $S_n = n \\cdot a_1$."
          )),

        b("intuicion", body_md=(
            "Las sucesiones aritméticas modelan el **crecimiento lineal discreto** "
            "(suma constante), mientras que las geométricas modelan el **crecimiento "
            "exponencial discreto** (multiplicación constante). Por eso aparecen "
            "naturalmente en interés simple vs. interés compuesto, en demografía "
            "lineal vs. exponencial, y en decaimiento radiactivo."
        )),

        b("ejemplo_resuelto",
          titulo="Sucesión geométrica con datos no consecutivos",
          problema_md=(
              "El tercer término de una sucesión geométrica es $\\dfrac{63}{4}$ y "
              "el sexto término es $\\dfrac{1701}{32}$. Encuentre el quinto término."
          ),
          pasos=[
              {"accion_md": (
                  "Como $a_n = a_1 r^{n-1}$, tenemos $a_3 = a_1 r^2 = \\dfrac{63}{4}$ "
                  "y $a_6 = a_1 r^5 = \\dfrac{1701}{32}$. Dividiendo la segunda por la primera:\n"
                  "$$\\frac{a_1 r^5}{a_1 r^2} = r^3 = \\frac{1701/32}{63/4} = \\frac{1701 \\cdot 4}{32 \\cdot 63} = \\frac{27}{8} \\implies r = \\frac{3}{2}.$$"
               ),
               "justificacion_md": "Cociente de las dos ecuaciones elimina $a_1$.",
               "es_resultado": False},
              {"accion_md": (
                  "Sustituyendo en $a_1 r^2 = \\frac{63}{4}$: $a_1 \\cdot \\frac{9}{4} = \\frac{63}{4} \\implies a_1 = 7$."
               ),
               "justificacion_md": "Despeje de $a_1$.",
               "es_resultado": False},
              {"accion_md": (
                  "Quinto término: $a_5 = 7 \\cdot \\left(\\dfrac{3}{2}\\right)^4 = 7 \\cdot \\dfrac{81}{16} = \\boxed{\\dfrac{567}{16}}.$"
               ),
               "justificacion_md": "Aplicación de la fórmula explícita.",
               "es_resultado": True},
          ]),

        ej(
            "Antepasados (suc. geométrica aplicada)",
            ("Una persona tiene 2 padres, 4 abuelos, 8 bisabuelos, y así "
             "sucesivamente. ¿Cuántos antepasados tiene en la generación $15$?"),
            ["El número de antepasados en cada generación forma una sucesión geométrica.",
             "$a_1 = 2$, $r = 2$. Aplicá $a_n = a_1 r^{n-1}$.",
             "Notá que $a_n = 2 \\cdot 2^{n-1} = 2^n$."],
            ("Los antepasados forman una sucesión geométrica con $a_1 = 2$ y $r = 2$. "
             "Entonces $a_n = 2 \\cdot 2^{n-1} = 2^n$. Para $n = 15$: "
             "$a_{15} = 2^{15} = \\boxed{32\\,768}$ antepasados.")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "Sea la sucesión aritmética $a_1 = 5$, $d = 3$. ¿Cuánto vale $a_{10}$?",
               "opciones_md": ["$30$", "$32$", "$33$", "$35$"],
               "correcta": "B",
               "pista_md": "Recordá $a_n = a_1 + (n-1)d$.",
               "explicacion_md": "$a_{10} = 5 + (10-1)\\cdot 3 = 5 + 27 = 32$. Cuidado con usar $a_1 + nd$ en vez de $a_1 + (n-1)d$: ese error daría $35$."},
              {"enunciado_md": "¿Cuál de las siguientes sucesiones **no es** geométrica?",
               "opciones_md": ["$2, 6, 18, 54, \\ldots$", "$1, -1, 1, -1, \\ldots$", "$3, 6, 9, 12, \\ldots$", "$1, \\tfrac{1}{2}, \\tfrac{1}{4}, \\tfrac{1}{8}, \\ldots$"],
               "correcta": "C",
               "pista_md": "En una geométrica el cociente entre términos consecutivos es constante.",
               "explicacion_md": "$3, 6, 9, 12$ es **aritmética** con $d = 3$, no geométrica: $6/3 = 2$ pero $9/6 = 1.5$. Las otras tres tienen razón constante $r = 3, -1, 1/2$ respectivamente."},
              {"enunciado_md": "Si $S_n = \\sum_{k=1}^{n} a_k$ y la sucesión es geométrica con razón $r \\neq 1$, ¿cuál es la fórmula correcta de $S_n$?",
               "opciones_md": ["$S_n = a_1 \\cdot r^n$", "$S_n = n \\cdot a_1$", "$S_n = a_1 \\dfrac{1-r^n}{1-r}$", "$S_n = \\dfrac{a_1 + a_n}{2}$"],
               "correcta": "C",
               "pista_md": "La opción D es de las aritméticas; la opción B vale solo cuando $r=1$.",
               "explicacion_md": "Para una progresión geométrica con $r \\neq 1$: $S_n = a_1 \\dfrac{1-r^n}{1-r}$. Cuando $r=1$ la fórmula se indefine y se reduce a $S_n = n a_1$. La opción D corresponde a sumas aritméticas."},
          ]),

        fig("Diagrama educativo en español que compara una sucesión aritmética y una geométrica. A la izquierda, puntos $(1,2),(2,5),(3,8),(4,11),(5,14)$ alineados sobre una recta (crecimiento lineal) en teal #06b6d4 con etiqueta «$d = 3$». A la derecha, puntos $(1,2),(2,4),(3,8),(4,16),(5,32)$ siguiendo una curva exponencial en ámbar #f59e0b con etiqueta «$r = 2$». Ejes con marcas de 1 a 5, fondo blanco. " + STYLE),

        b("errores_comunes",
          items_md=[
              "**Confundir aritmética con geométrica.** Aritmética: diferencia constante; geométrica: razón constante.",
              "**Usar $r = 1$ en la fórmula geométrica.** La fórmula $S_n = a_1 \\frac{1 - r^n}{1 - r}$ se indefine; en ese caso $S_n = n \\cdot a_1$.",
              "**Olvidar el $-1$ en el exponente.** $a_n = a_1 r^{n-1}$, no $a_1 r^n$. Pasa también con aritméticas: $a_n = a_1 + (n-1)d$.",
              "**Cambiar el índice de partida sin ajustar.** Si la sucesión arranca en $n_0 \\neq 1$, las fórmulas necesitan reindexarse.",
          ]),

        b("resumen",
          puntos_md=[
              "Una **sucesión** es una función $\\mathbb{N} \\to \\mathbb{R}$; se describe verbal, explícita o recursivamente.",
              "**Notación sigma:** $\\sum_{k=1}^n a_k$ compacta sumas finitas; $k$ es índice mudo.",
              "**Aritmética:** $a_n = a_1 + (n-1)d$, $\\;\\;S_n = n \\cdot \\frac{a_1 + a_n}{2}$.",
              "**Geométrica:** $a_n = a_1 r^{n-1}$, $\\;\\;S_n = a_1 \\cdot \\frac{1 - r^n}{1 - r}$ (si $r \\neq 1$).",
              "Próxima lección: propiedades algebraicas de las sumas finitas y técnica de **sumas telescópicas**.",
          ]),
    ]
    return {
        "id": "lec-ia-2-2-sucesiones",
        "title": "Sucesiones",
        "description": "Sucesiones de números reales, notación sigma, sucesiones aritméticas y geométricas con sus sumas parciales.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# ============================================================================
# 2.3 Sumas Finitas
# ============================================================================
def lesson_2_3():
    blocks = [
        b("texto", body_md=(
            "Las **sumas finitas** constituyen una herramienta fundamental del "
            "álgebra y el análisis matemático. La notación sigma —introducida por "
            "Euler— nos permite trabajar con sumas grandes de manera sistemática y "
            "eficiente.\n\n"
            "En esta lección profundizamos:\n\n"
            "- Las **propiedades algebraicas** de la sumatoria (linealidad, cambio de índice, partición).\n"
            "- **Fórmulas cerradas** para sumas de potencias: $\\sum k$, $\\sum k^2$, $\\sum k^3$.\n"
            "- La técnica de **sumas telescópicas** (cuando todo cancela menos los extremos).\n"
            "- La **suma geométrica** $\\sum r^k$ y su deducción algebraica."
        )),

        b("teorema",
          enunciado_md=(
              "**Propiedades de la notación sigma.** Sean $\\{a_k\\}, \\{b_k\\}$ "
              "sucesiones y $c \\in \\mathbb{R}$ constante:\n\n"
              "1. **Linealidad (suma):** $\\displaystyle\\sum_{k=1}^n a_k + \\sum_{k=1}^n b_k = \\sum_{k=1}^n (a_k + b_k)$.\n\n"
              "2. **Linealidad (constante):** $\\displaystyle\\sum_{k=1}^n c\\,a_k = c\\sum_{k=1}^n a_k$.\n\n"
              "3. **Producto de sumas:** $\\displaystyle\\Bigl(\\sum_{k=1}^n a_k\\Bigr)\\Bigl(\\sum_{\\ell=1}^m b_\\ell\\Bigr) = \\sum_{k=1}^n \\sum_{\\ell=1}^m a_k b_\\ell$.\n\n"
              "4. **Partición:** $\\displaystyle\\sum_{k=m}^n a_k = \\sum_{k=1}^n a_k - \\sum_{k=1}^{m-1} a_k$.\n\n"
              "5. **Cambio de índice (corrimiento):** $\\displaystyle\\sum_{k=m-\\ell}^{n-\\ell} a_{k+\\ell} = \\sum_{k=m}^n a_k$."
          )),

        b("teorema",
          enunciado_md=(
              "**Fórmulas cerradas para sumas de potencias.** Para todo $n \\in \\mathbb{N}$:\n\n"
              "$$\\sum_{k=1}^n 1 = n, \\qquad \\sum_{k=1}^n k = \\frac{n(n+1)}{2}.$$\n"
              "$$\\sum_{k=1}^n k^2 = \\frac{n(n+1)(2n+1)}{6}, \\qquad \\sum_{k=1}^n k^3 = \\left[\\frac{n(n+1)}{2}\\right]^2.$$\n"
              "Las cuatro se demuestran por inducción matemática. La cuarta tiene "
              "la notable identidad\n"
              "$$\\sum_{k=1}^n k^3 = \\Bigl(\\sum_{k=1}^n k\\Bigr)^2,$$\n"
              "es decir, **la suma de los cubos es el cuadrado de la suma**."
          )),

        b("ejemplo_resuelto",
          titulo="La suma de Gauss",
          problema_md=(
              "Verifique la fórmula $\\sum_{k=1}^n k = \\dfrac{n(n+1)}{2}$ para $n=4$ "
              "y luego calcule $\\displaystyle\\sum_{k=1}^{100} k$."
          ),
          pasos=[
              {"accion_md": (
                  "Para $n = 4$: la suma explícita es $1 + 2 + 3 + 4 = 10$, y la "
                  "fórmula da $\\dfrac{4 \\cdot 5}{2} = 10$. Coinciden. ✓"
               ),
               "justificacion_md": "Verificación de un caso concreto.",
               "es_resultado": False},
              {"accion_md": (
                  "Para $n = 100$: $\\displaystyle\\sum_{k=1}^{100} k = \\frac{100 \\cdot 101}{2} = \\boxed{5050}.$\n\n"
                  "*(Anécdota: este es el cálculo que, según la leyenda, hizo "
                  "Gauss a los 9 años cuando su maestro le pidió sumar los "
                  "primeros 100 naturales.)*"
               ),
               "justificacion_md": "Aplicación directa de la fórmula cerrada.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Sumas con linealidad y partición",
          problema_md=(
              "Calcule $\\displaystyle\\sum_{k=10}^{n} (2k + 1)$."
          ),
          pasos=[
              {"accion_md": (
                  "Por partición:\n"
                  "$$\\sum_{k=10}^n (2k+1) = \\sum_{k=1}^n (2k+1) - \\sum_{k=1}^9 (2k+1).$$"
               ),
               "justificacion_md": "Convertir a sumas desde $k=1$ para usar fórmulas cerradas.",
               "es_resultado": False},
              {"accion_md": (
                  "Por linealidad: $\\sum_{k=1}^n(2k+1) = 2\\sum_{k=1}^n k + \\sum_{k=1}^n 1 "
                  "= 2 \\cdot \\dfrac{n(n+1)}{2} + n = n(n+1) + n = n^2 + 2n.$\n\n"
                  "Análogamente $\\sum_{k=1}^9 (2k+1) = 2 \\cdot \\dfrac{9 \\cdot 10}{2} + 9 = 90 + 9 = 99.$"
               ),
               "justificacion_md": "Aplicamos linealidad + fórmulas cerradas.",
               "es_resultado": False},
              {"accion_md": (
                  "Restando: $\\displaystyle\\sum_{k=10}^n (2k+1) = (n^2 + 2n) - 99 = \\boxed{n^2 + 2n - 99}.$"
               ),
               "justificacion_md": "Resultado en forma cerrada.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Sumas telescópicas",
          body_md=(
              "Una **suma telescópica** es aquella en que los términos intermedios se "
              "cancelan entre sí. La propiedad básica es:\n"
              "$$\\sum_{k=1}^n (a_k - a_{k-1}) = a_n - a_0.$$\n"
              "Forma general (con $\\ell$ corrimientos):\n"
              "$$\\sum_{k=m}^n (a_k - a_{k+1}) = a_m - a_{n+1}.$$\n"
              "**Estrategia:** identificar una sucesión auxiliar $\\{a_k\\}$ tal "
              "que el término general de la suma se escriba como $a_k - a_{k-1}$ "
              "(o $a_k - a_{k+1}$). Una vez reconocida, la suma colapsa a una "
              "expresión cerrada de inmediato."
          )),

        b("ejemplo_resuelto",
          titulo="Telescópica con fracciones parciales",
          problema_md=(
              "Use la propiedad telescópica para obtener una fórmula cerrada de "
              "$\\displaystyle\\sum_{k=1}^{n} \\dfrac{1}{k(k+1)}$."
          ),
          pasos=[
              {"accion_md": (
                  "Por fracciones parciales: "
                  "$\\dfrac{1}{k(k+1)} = \\dfrac{1}{k} - \\dfrac{1}{k+1} = a_k - a_{k+1}$ "
                  "donde $a_k = \\dfrac{1}{k}$."
               ),
               "justificacion_md": "Descomposición en fracciones parciales.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicando la propiedad telescópica (forma general):\n"
                  "$$\\sum_{k=1}^n \\frac{1}{k(k+1)} = \\sum_{k=1}^n (a_k - a_{k+1}) = a_1 - a_{n+1} = 1 - \\frac{1}{n+1} = \\boxed{\\frac{n}{n+1}}.$$"
               ),
               "justificacion_md": "Colapso telescópico.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Suma geométrica.** Para $r \\neq 1$ y $n \\in \\mathbb{N} \\cup \\{0\\}$:\n"
              "$$\\sum_{k=0}^n r^k = \\frac{1 - r^{n+1}}{1 - r}, \\qquad \\sum_{k=1}^n r^k = r \\cdot \\frac{1 - r^n}{1 - r}.$$\n"
              "**Deducción:** sea $S = 1 + r + r^2 + \\cdots + r^n$. Multiplicando por $r$:\n"
              "$$rS = r + r^2 + \\cdots + r^{n+1}.$$\n"
              "Restando: $S - rS = 1 - r^{n+1}$, de donde $S(1-r) = 1 - r^{n+1}$ y se "
              "despeja $S$. Cuando $r = 1$, todos los términos valen $1$ y $S_n = n+1$."
          )),

        b("ejemplo_resuelto",
          titulo="Suma geométrica disfrazada",
          problema_md=(
              "Calcule $\\displaystyle\\sum_{k=1}^{n} \\dfrac{3^{k+1}}{4^k}$."
          ),
          pasos=[
              {"accion_md": (
                  "Reescribimos separando potencias:\n"
                  "$$\\sum_{k=1}^n \\frac{3^{k+1}}{4^k} = \\sum_{k=1}^n 3 \\cdot \\frac{3^k}{4^k} = 3 \\sum_{k=1}^n \\left(\\frac{3}{4}\\right)^k.$$"
               ),
               "justificacion_md": "Identificamos la razón $r = 3/4$.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicando la fórmula con $r = \\frac{3}{4}$:\n"
                  "$$3 \\cdot \\frac{3}{4} \\cdot \\frac{1 - (3/4)^n}{1 - 3/4} = \\frac{9}{4} \\cdot \\frac{1 - (3/4)^n}{1/4} = \\boxed{9\\Bigl(1 - \\Bigl(\\tfrac{3}{4}\\Bigr)^n\\Bigr)}.$$"
               ),
               "justificacion_md": "Sustitución directa y simplificación.",
               "es_resultado": True},
          ]),

        ej(
            "Telescópica con factoriales",
            ("Calcule $\\displaystyle\\sum_{k=0}^{n} k \\cdot k!$ usando una "
             "telescópica adecuada."),
            ["Reescribí $k \\cdot k! = [(k+1) - 1] \\cdot k! = (k+1)! - k!$.",
             "Definí $a_k = k!$ y observá que $k \\cdot k! = a_{k+1} - a_k$.",
             "Aplicá la propiedad telescópica: la suma colapsa a $a_{n+1} - a_0$."],
            ("Notamos que $k \\cdot k! = (k+1)! - k!$. Sea $a_k = k!$. Entonces:\n"
             "$$\\sum_{k=0}^n k \\cdot k! = \\sum_{k=0}^n (a_{k+1} - a_k) = a_{n+1} - a_0 = (n+1)! - 0! = \\boxed{(n+1)! - 1}.$$")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "¿Cuánto vale $\\sum_{k=1}^{100} k$?",
               "opciones_md": ["$5000$", "$5050$", "$10000$", "$10100$"],
               "correcta": "B",
               "pista_md": "Usá $\\sum_{k=1}^n k = \\frac{n(n+1)}{2}$.",
               "explicacion_md": "$\\sum_{k=1}^{100} k = \\frac{100 \\cdot 101}{2} = 5050$. Es la famosa suma de Gauss."},
              {"enunciado_md": "¿Cuál es la fórmula correcta de la suma geométrica $\\sum_{k=0}^{n} r^k$ cuando $r \\neq 1$?",
               "opciones_md": ["$\\dfrac{r^n - 1}{r - 1}$", "$\\dfrac{r^{n+1} - 1}{r - 1}$", "$\\dfrac{r^n}{r - 1}$", "$\\dfrac{1 - r^n}{r - 1}$"],
               "correcta": "B",
               "pista_md": "Cuidado con el rango: empieza en $k=0$.",
               "explicacion_md": "$\\sum_{k=0}^{n} r^k = 1 + r + r^2 + \\cdots + r^n = \\dfrac{r^{n+1} - 1}{r - 1}$. Hay $n+1$ términos, por eso aparece $r^{n+1}$. Si fuera $\\sum_{k=1}^n r^k$ habría $n$ términos y la respuesta sería A."},
              {"enunciado_md": "Aplicando la propiedad de **partición** del rango: $\\sum_{k=1}^{20} a_k = \\sum_{k=1}^{10} a_k + \\square$. ¿Qué va en el cuadrado?",
               "opciones_md": ["$\\sum_{k=10}^{20} a_k$", "$\\sum_{k=11}^{20} a_k$", "$\\sum_{k=10}^{19} a_k$", "$\\sum_{k=11}^{19} a_k$"],
               "correcta": "B",
               "pista_md": "El primer rango llega hasta $10$, así que el segundo arranca en $11$.",
               "explicacion_md": "Para no contar dos veces $a_{10}$, el segundo rango debe empezar en $k=11$ y llegar hasta $20$ inclusive. Así: $\\sum_{k=1}^{10} + \\sum_{k=11}^{20} = \\sum_{k=1}^{20}$."},
          ]),

        fig("Diagrama educativo en español que ilustra una suma telescópica: cinco rectángulos representan $a_1 - a_0$, $a_2 - a_1$, $a_3 - a_2$, $a_4 - a_3$, $a_5 - a_4$, con flechas de cancelación cruzadas que muestran cómo los términos intermedios se anulan, dejando el resultado $a_5 - a_0$. Trazos en teal #06b6d4 para los rectángulos y ámbar #f59e0b para las flechas. Etiquetas claras en español, fondo blanco. " + STYLE),

        b("errores_comunes",
          items_md=[
              "**Aplicar mal la partición.** $\\sum_{k=m}^n a_k = \\sum_{k=1}^n a_k - \\sum_{k=1}^{m-1} a_k$ (no hasta $m$).",
              "**Olvidar la condición $r \\neq 1$ en la suma geométrica.** Si $r = 1$, la fórmula se indefine.",
              "**Confundir $\\sum r^k$ desde $k=0$ vs. desde $k=1$.** Las fórmulas difieren por un factor de $r$.",
              "**Errores en sumas telescópicas:** confirmá cuál es $a_k$ y cuál es $a_{k\\pm 1}$ antes de colapsar.",
          ]),

        b("resumen",
          puntos_md=[
              "**Linealidad** y **partición** son las propiedades clave para manipular $\\sum$.",
              "Sumas de potencias $\\sum k, \\sum k^2, \\sum k^3$ tienen fórmulas cerradas (por inducción).",
              "**Telescópicas:** identificá $a_k - a_{k\\pm 1}$ y la suma colapsa.",
              "**Geométrica:** $\\sum_{k=0}^n r^k = \\dfrac{1-r^{n+1}}{1-r}$ para $r \\neq 1$.",
              "Próxima lección: el **Teorema del Binomio** y los coeficientes binomiales del Triángulo de Pascal.",
          ]),
    ]
    return {
        "id": "lec-ia-2-3-sumas-finitas",
        "title": "Sumas Finitas",
        "description": "Linealidad, fórmulas cerradas, sumas telescópicas y suma geométrica.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
    }


# ============================================================================
# 2.4 Teorema del Binomio
# ============================================================================
def lesson_2_4():
    blocks = [
        b("texto", body_md=(
            "El **Teorema del Binomio** es uno de los resultados más elegantes y "
            "útiles del álgebra elemental. Permite expandir de forma sistemática "
            "cualquier potencia $(a+b)^n$ sin necesidad de multiplicar factor a "
            "factor. Su demostración usa **inducción matemática** y revela la "
            "profunda conexión entre los **coeficientes binomiales**, el **triángulo "
            "de Pascal** y la combinatoria.\n\n"
            "Al terminar serás capaz de:\n\n"
            "- Calcular coeficientes binomiales y reconocer sus propiedades.\n"
            "- Construir el Triángulo de Pascal usando la identidad de Pascal.\n"
            "- Enunciar y aplicar el Teorema del Binomio para expansiones.\n"
            "- Encontrar coeficientes específicos en desarrollos binomiales.\n"
            "- Deducir corolarios como $\\sum \\binom{n}{k} = 2^n$."
        )),

        b("texto", body_md=(
            "**Patrones en la expansión.** Observemos las primeras potencias:\n\n"
            "$$\\begin{aligned}(a+b)^1 &= a + b\\\\(a+b)^2 &= a^2 + 2ab + b^2\\\\"
            "(a+b)^3 &= a^3 + 3a^2 b + 3ab^2 + b^3\\\\(a+b)^4 &= a^4 + 4a^3 b + 6a^2 b^2 + 4ab^3 + b^4\\\\"
            "(a+b)^5 &= a^5 + 5a^4 b + 10 a^3 b^2 + 10 a^2 b^3 + 5ab^4 + b^5\\end{aligned}$$\n\n"
            "Tres patrones emergen para $(a+b)^n$:\n\n"
            "1. Hay exactamente $n+1$ términos, empezando en $a^n$ y terminando en $b^n$.\n"
            "2. Los exponentes de $a$ disminuyen en 1 cada término; los de $b$ aumentan en 1.\n"
            "3. La suma de los exponentes de $a$ y $b$ en cada término es siempre $n$.\n\n"
            "Lo único que falta determinar son los **coeficientes**."
        )),

        b("definicion",
          titulo="Coeficiente binomial",
          body_md=(
              "Sean $n, k \\in \\mathbb{N} \\cup \\{0\\}$ con $k \\le n$. El **coeficiente binomial** $\\binom{n}{k}$ se define como\n"
              "$$\\binom{n}{k} = \\frac{n!}{k!\\,(n-k)!}$$\n"
              "donde $n! = n \\cdot (n-1) \\cdots 2 \\cdot 1$, con la convención $0! = 1$.\n\n"
              "Se lee «$n$ en $k$» o «$n$ sobre $k$», y representa el número de "
              "formas de elegir $k$ elementos de un conjunto de $n$.\n\n"
              "**Casos básicos:** $\\binom{n}{0} = \\binom{n}{n} = 1$ y $\\binom{n}{1} = \\binom{n}{n-1} = n$."
          )),

        b("teorema",
          enunciado_md=(
              "**Propiedades fundamentales.** Sean $n, k \\in \\mathbb{N} \\cup \\{0\\}$ con $k \\le n$:\n\n"
              "1. **Simetría:** $\\displaystyle\\binom{n}{k} = \\binom{n}{n-k}$.\n\n"
              "2. **Identidad de Pascal:** $\\displaystyle\\binom{n}{k} + \\binom{n}{k+1} = \\binom{n+1}{k+1}$.\n\n"
              "La simetría refleja que elegir $k$ es lo mismo que elegir los $n-k$ "
              "que se descartan. La identidad de Pascal es la base del **Triángulo "
              "de Pascal**: cada entrada (que no sea 1) es la suma de las dos que "
              "están diagonalmente sobre ella."
          )),

        fig(
            "Triángulo de Pascal con 7 filas (n=0 a n=6) renderizado en dos paneles lado a lado: "
            "panel izquierdo con notación binomial: (0 sobre 0), luego (1 sobre 0)(1 sobre 1), luego (2 sobre 0)(2 sobre 1)(2 sobre 2), etc., centrados horizontalmente. "
            "Panel derecho con valores numéricos correspondientes: 1; 1 1; 1 2 1; 1 3 3 1; 1 4 6 4 1; 1 5 10 10 5 1; 1 6 15 20 15 6 1. "
            "Flechas curvas tenues en el panel derecho indicando que cada número es la suma de los dos sobre él (identidad de Pascal). Acentos teal y ámbar. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Calcular coeficientes binomiales",
          problema_md="Calcule $\\dbinom{5}{2}$, $\\dbinom{n}{n}$ y $\\dbinom{n}{1}$.",
          pasos=[
              {"accion_md": (
                  "$\\dbinom{5}{2} = \\dfrac{5!}{2! \\cdot 3!} = \\dfrac{5 \\cdot 4}{2} = 10.$"
               ),
               "justificacion_md": "Cancelación del $3!$ y simplificación.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\dbinom{n}{n} = \\dfrac{n!}{n! \\cdot 0!} = 1.$"
               ),
               "justificacion_md": "Recordando $0! = 1$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\dbinom{n}{1} = \\dfrac{n!}{1! \\cdot (n-1)!} = \\dfrac{n \\cdot (n-1)!}{(n-1)!} = n.$"
               ),
               "justificacion_md": "Desarrollo del numerador.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Teorema del Binomio (Newton).** Sean $a, b \\in \\mathbb{R}$ y $n \\in \\mathbb{N}$. Entonces\n"
              "$$\\boxed{\\;(a+b)^n = \\sum_{k=0}^n \\binom{n}{k} a^{n-k} b^k\\;}$$\n"
              "Es decir, la expansión explícita es\n"
              "$$(a+b)^n = \\binom{n}{0}a^n + \\binom{n}{1}a^{n-1}b + \\binom{n}{2}a^{n-2}b^2 + \\cdots + \\binom{n}{n}b^n.$$\n"
              "El coeficiente del término $a^{n-k} b^k$ es exactamente $\\binom{n}{k}$ — de ahí el nombre."
          )),

        b("intuicion", body_md=(
            "**¿Por qué aparecen coeficientes binomiales?** Al desarrollar $(a+b)^n$ "
            "como producto de $n$ factores $(a+b)(a+b)\\cdots(a+b)$, cada término "
            "del resultado se obtiene eligiendo $a$ o $b$ de cada paréntesis. El "
            "número de formas de obtener exactamente $k$ veces $b$ (y $n-k$ veces "
            "$a$) es $\\binom{n}{k}$, el número de formas de elegir esos $k$ "
            "paréntesis. Esa es la justificación combinatoria del teorema."
        )),

        b("ejemplo_resuelto",
          titulo="Expansión binomial completa",
          problema_md=(
              "Escriba el desarrollo completo de $\\left(y^2 + \\dfrac{1}{y}\\right)^6$."
          ),
          pasos=[
              {"accion_md": (
                  "Aplicamos el Teorema del Binomio con $a = y^2$, $b = \\frac{1}{y}$, $n = 6$:\n"
                  "$$\\left(y^2 + \\tfrac{1}{y}\\right)^6 = \\sum_{k=0}^{6} \\binom{6}{k} (y^2)^{6-k} \\left(\\tfrac{1}{y}\\right)^k = \\sum_{k=0}^{6} \\binom{6}{k} y^{12-3k}.$$"
               ),
               "justificacion_md": "Sustitución y simplificación de exponentes.",
               "es_resultado": False},
              {"accion_md": (
                  "Expandiendo término a término con la fila $n=6$ del Triángulo de Pascal $(1, 6, 15, 20, 15, 6, 1)$:\n"
                  "$$= y^{12} + 6y^9 + 15 y^6 + 20 y^3 + 15 + 6y^{-3} + y^{-6}.$$"
               ),
               "justificacion_md": "Cálculo explícito de cada término.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Coeficiente específico",
          problema_md="Encuentre el coeficiente de $x^n$ en $(1 + x)^{2n}$.",
          pasos=[
              {"accion_md": (
                  "Por el Teorema del Binomio con $a = 1$, $b = x$, exponente $2n$:\n"
                  "$$(1+x)^{2n} = \\sum_{k=0}^{2n} \\binom{2n}{k} \\cdot 1^{2n-k} \\cdot x^k = \\sum_{k=0}^{2n} \\binom{2n}{k} x^k.$$"
               ),
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": (
                  "Buscamos $k$ tal que $x^k = x^n$, es decir, $k = n$. Por tanto el coeficiente es:\n"
                  "$$\\boxed{\\binom{2n}{n} = \\frac{(2n)!}{n! \\cdot n!}}.$$"
               ),
               "justificacion_md": "Identificamos el término con la potencia buscada.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Corolarios del Teorema del Binomio.** Para todo $n \\in \\mathbb{N}$:\n\n"
              "$$\\sum_{k=0}^n \\binom{n}{k} = 2^n, \\qquad \\sum_{k=0}^n (-1)^k \\binom{n}{k} = 0.$$\n"
              "**Demostración:** la primera se obtiene sustituyendo $a = b = 1$ en "
              "$(a+b)^n$; la segunda, sustituyendo $a = 1, b = -1$.\n\n"
              "**Interpretación combinatoria:** la suma de todos los coeficientes "
              "binomiales de orden $n$ es $2^n$ — el número total de subconjuntos "
              "de un conjunto de $n$ elementos."
          )),

        ej(
            "Coeficiente con doble suma",
            ("Determine el coeficiente que acompaña a $\\dfrac{1}{x^{31}}$ en el "
             "desarrollo de $\\displaystyle\\left(x - 1 + \\dfrac{1}{x^2}\\right)^{20}$."),
            ["Reescribí la base: $\\left(\\dfrac{x^3 - x^2 + 1}{x^2}\\right)^{20} = \\dfrac{1}{x^{40}}\\left(x^3 + (1 - x^2)\\right)^{20}.$",
             "Aplicá Binomio dos veces: primero con $a = x^3$, $b = 1 - x^2$; luego sobre $(1-x^2)^k$.",
             "Buscás los $(k, \\ell)$ enteros tales que el exponente final de $x$ sea $-31$."],
            ("Reescribiendo: $\\left(x - 1 + \\frac{1}{x^2}\\right)^{20} = \\frac{1}{x^{40}}(x^3 + (1-x^2))^{20}$. "
             "Aplicando Binomio: $= \\frac{1}{x^{40}} \\sum_{k=0}^{20} \\binom{20}{k} x^{60-3k}(1-x^2)^k$. "
             "Aplicando Binomio a $(1-x^2)^k$: $\\sum_{\\ell=0}^k \\binom{k}{\\ell}(-1)^\\ell x^{2\\ell}$. "
             "El término general queda $\\binom{20}{k}\\binom{k}{\\ell}(-1)^\\ell x^{20-3k+2\\ell}$. "
             "Para $x^{-31}$ necesitamos $20 - 3k + 2\\ell = -31$, es decir $\\ell = \\frac{3k - 51}{2}$, con $0 \\le \\ell \\le k \\le 20$. "
             "Los pares válidos son $(k=17, \\ell=0)$ y $(k=19, \\ell=3)$. Coeficiente final: "
             "$\\binom{20}{17}\\binom{17}{0}(-1)^0 + \\binom{20}{19}\\binom{19}{3}(-1)^3 = \\binom{20}{17} - 20 \\cdot \\binom{19}{3}.$")
        ),

        b("verificacion",
          intro_md="Verifica tu comprensión:",
          preguntas=[
              {"enunciado_md": "¿Cuántos términos tiene la expansión de $(a + b)^{10}$?",
               "opciones_md": ["$9$", "$10$", "$11$", "$12$"],
               "correcta": "C",
               "pista_md": "El índice $k$ va de $0$ a $n$.",
               "explicacion_md": "$(a+b)^n$ tiene $n+1$ términos porque $k$ recorre $0, 1, \\ldots, n$. Por lo tanto $(a+b)^{10}$ tiene $11$ términos."},
              {"enunciado_md": "En la expansión de $(x + 2)^5$, ¿cuál es el coeficiente del término $x^3$?",
               "opciones_md": ["$10$", "$20$", "$40$", "$80$"],
               "correcta": "C",
               "pista_md": "El término general es $\\binom{5}{k} x^{5-k} 2^k$.",
               "explicacion_md": "Para $x^3$ necesitamos $5-k=3$, es decir $k=2$. El coeficiente es $\\binom{5}{2} \\cdot 2^2 = 10 \\cdot 4 = 40$."},
              {"enunciado_md": "¿Cuál es el valor de $\\sum_{k=0}^{n} \\binom{n}{k}$?",
               "opciones_md": ["$n$", "$n!$", "$2^n$", "$2n$"],
               "correcta": "C",
               "pista_md": "Aplicá el Teorema del Binomio a $(1 + 1)^n$.",
               "explicacion_md": "Tomando $a = b = 1$ en $(a+b)^n = \\sum_k \\binom{n}{k} a^{n-k}b^k$ se obtiene $2^n = \\sum_{k=0}^n \\binom{n}{k}$. Cuenta también el total de subconjuntos de un conjunto de $n$ elementos."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Olvidar que el índice empieza en $k = 0$.** Hay $n + 1$ términos en la expansión, no $n$.",
              "**Confundir $a^{n-k} b^k$ con $a^k b^{n-k}$.** Mirá bien la convención del enunciado.",
              "**Calcular $\\binom{n}{k}$ sin simplificar el factorial.** Suele ser más rápido cancelar antes de evaluar.",
              "**Aplicar el binomio cuando hay tres términos.** $(a + b + c)^n$ requiere el **multinomial**, no el binomio directo (o aplicar el binomio dos veces como en el ejercicio).",
          ]),

        b("resumen",
          puntos_md=[
              "$\\binom{n}{k} = \\dfrac{n!}{k!(n-k)!}$ satisface **simetría** y la **identidad de Pascal**.",
              "El **Triángulo de Pascal** se construye sumando entradas diagonalmente.",
              "**Teorema del Binomio:** $(a+b)^n = \\sum_{k=0}^n \\binom{n}{k} a^{n-k} b^k$, demostrable por inducción.",
              "Corolarios: $\\sum \\binom{n}{k} = 2^n$ (subconjuntos) y $\\sum (-1)^k \\binom{n}{k} = 0$.",
              "**Cierre del capítulo:** ya dominás inducción, sucesiones, sumas y el binomio. Próximo capítulo: **trigonometría**, donde aplicaremos sumas y identidades algebraicas a las funciones $\\sin, \\cos, \\tan$.",
          ]),
    ]
    return {
        "id": "lec-ia-2-4-binomio",
        "title": "Teorema del Binomio",
        "description": "Coeficientes binomiales, Triángulo de Pascal, Teorema del Binomio y corolarios.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
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

    builders = [lesson_2_1, lesson_2_2, lesson_2_3, lesson_2_4]

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
