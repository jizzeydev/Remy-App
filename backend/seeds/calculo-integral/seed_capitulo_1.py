"""
Seed del curso Cálculo Integral — Capítulo 1: Integrales.

Crea el curso (si no existe) y el capítulo "Integrales" con sus 3 lecciones:
  1.1 Definición de integral
  1.2 Integral indefinida
  1.3 Integral definida

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


def desmos(expressions, guide, height=400, url=""):
    return b("grafico_desmos", desmos_url=url, expresiones=expressions,
             guia_md=guide, altura=height)


def ej(titulo, enunciado, pistas, solucion):
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def now():
    return datetime.now(timezone.utc).isoformat()


STYLE = (
    "Estilo: diagrama educativo limpio, fondo blanco, líneas claras, etiquetas en español, "
    "notación matemática con buena tipografía. Acentos teal #06b6d4 y ámbar #f59e0b. "
    "Sin sombras dramáticas, sin texturas. Apto para libro universitario."
)


# =====================================================================
# LECCIÓN 1.1 — Definición de integral
# =====================================================================
def lesson_1_1():
    blocks = [
        b("texto", body_md=(
            "La **integral definida** responde a una pregunta geométrica antigua: "
            "¿cuál es el área de una región bajo una curva? "
            "La respuesta moderna pasa por aproximar con rectángulos cada vez más finos y tomar el límite. "
            "Esa idea — la **suma de Riemann** — es el corazón del cálculo integral.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Comprender la idea geométrica del área bajo una curva.\n"
            "- Definir la **partición** de un intervalo y la **suma de Riemann**.\n"
            "- Definir formalmente la **integral definida** como límite de sumas.\n"
            "- Reconocer las condiciones que garantizan la **integrabilidad** de una función."
        )),

        b("intuicion",
          titulo="Aproximar el área con rectángulos",
          body_md=(
              "Si $f(x) \\geq 0$ en $[a, b]$ y queremos el área entre la curva y el eje $x$, podemos:\n\n"
              "1. **Dividir** $[a, b]$ en $n$ subintervalos.\n"
              "2. **Levantar** un rectángulo en cada subintervalo, eligiendo su altura como $f(x_i^*)$ para algún punto $x_i^*$ del subintervalo.\n"
              "3. **Sumar** las áreas de los rectángulos.\n"
              "4. **Hacer $n \\to \\infty$** (rectángulos cada vez más finos).\n\n"
              "Si el límite existe y no depende de cómo elegimos los $x_i^*$, ese valor es **el área** — y lo llamaremos **integral definida** de $f$ entre $a$ y $b$."
          )),

        fig(
            "Diagrama del área bajo una curva aproximada por rectángulos. Eje x con marcas en a y b. "
            "Una curva continua y = f(x) positiva. Bajo la curva, dividir el intervalo [a,b] en 8 "
            "subintervalos iguales. En cada subintervalo, dibujar un rectángulo con altura = f en el "
            "extremo derecho del subintervalo. Los rectángulos llenan el área bajo la curva pero "
            "dejan triangulitos (algunos sobresalen, otros faltan). Etiquetas: 'a', 'b', 'f(x_i)' "
            "señalando una altura. Color teal para la curva, rectángulos en ámbar translúcido. "
            + STYLE
        ),

        b("definicion",
          titulo="Partición de un intervalo",
          body_md=(
              "Una **partición** $P$ de $[a, b]$ es un conjunto finito de puntos:\n\n"
              "$$a = x_0 < x_1 < x_2 < \\cdots < x_n = b$$\n\n"
              "Cada subintervalo es $[x_{i-1}, x_i]$ con ancho $\\Delta x_i = x_i - x_{i-1}$.\n\n"
              "La **norma** de la partición es $\\|P\\| = \\max_i \\Delta x_i$ — el ancho del subintervalo más grande.\n\n"
              "Si todos los subintervalos tienen el mismo ancho, $\\Delta x = \\dfrac{b - a}{n}$ y $x_i = a + i \\Delta x$. Esa es la partición **regular**."
          )),

        b("definicion",
          titulo="Suma de Riemann",
          body_md=(
              "Sea $f$ definida en $[a, b]$, $P$ una partición y $x_i^* \\in [x_{i-1}, x_i]$ un punto cualquiera del $i$-ésimo subintervalo. La **suma de Riemann** asociada es:\n\n"
              "$$S(P, f) = \\sum_{i=1}^{n} f(x_i^*) \\, \\Delta x_i$$\n\n"
              "Es la suma de las áreas (con signo) de los rectángulos de altura $f(x_i^*)$ y base $\\Delta x_i$.\n\n"
              "**Tres elecciones típicas de $x_i^*$:**\n\n"
              "- **Extremos izquierdos:** $x_i^* = x_{i-1}$ (suma izquierda).\n"
              "- **Extremos derechos:** $x_i^* = x_i$ (suma derecha).\n"
              "- **Puntos medios:** $x_i^* = (x_{i-1} + x_i)/2$ (suma del punto medio)."
          )),

        b("definicion",
          titulo="Integral definida",
          body_md=(
              "Si el límite\n\n"
              "$$\\lim_{\\|P\\| \\to 0} \\sum_{i=1}^{n} f(x_i^*) \\, \\Delta x_i$$\n\n"
              "existe y es el mismo sin importar la elección de los $x_i^*$, decimos que $f$ es **integrable** en $[a, b]$ y llamamos a ese valor la **integral definida** de $f$ entre $a$ y $b$:\n\n"
              "$$\\int_a^b f(x) \\, dx = \\lim_{\\|P\\| \\to 0} \\sum_{i=1}^{n} f(x_i^*) \\, \\Delta x_i$$\n\n"
              "**Notación:**\n\n"
              "- $\\int$ — símbolo de integral (S estilizada de \"suma\").\n"
              "- $a, b$ — **límites de integración** (inferior y superior).\n"
              "- $f(x)$ — el **integrando**.\n"
              "- $dx$ — diferencial; indica que $x$ es la variable de integración."
          )),

        b("teorema",
          nombre="Condición suficiente de integrabilidad",
          enunciado_md=(
              "Si $f$ es **continua en $[a, b]$**, entonces $f$ es **integrable** en $[a, b]$.\n\n"
              "Más generalmente: si $f$ es **acotada** en $[a, b]$ y tiene a lo sumo un **número finito de discontinuidades**, sigue siendo integrable."
          ),
          demostracion_md=(
              "La demostración rigurosa usa que toda función continua en un cerrado es uniformemente continua, "
              "y muestra que las sumas superiores e inferiores se aproximan al mismo valor cuando $\\|P\\| \\to 0$. "
              "Queda fuera del alcance de un curso introductorio. **Lo importante es retener:** continuidad ⇒ integrabilidad."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular $\\int_0^1 x^2 \\, dx$ por sumas de Riemann",
          problema_md="Calcular el área bajo $f(x) = x^2$ entre $0$ y $1$ usando la suma derecha con partición regular.",
          pasos=[
              {"accion_md": "**Partición regular:** $\\Delta x = \\dfrac{1}{n}$, $x_i = \\dfrac{i}{n}$ para $i = 0, 1, \\ldots, n$. Suma derecha: $x_i^* = x_i = \\dfrac{i}{n}$.",
               "justificacion_md": "Dividimos $[0, 1]$ en $n$ subintervalos iguales y elegimos el extremo derecho de cada uno como punto de muestreo.",
               "es_resultado": False},
              {"accion_md": "**Suma de Riemann:**\n\n$$S_n = \\sum_{i=1}^{n} f\\left(\\dfrac{i}{n}\\right) \\cdot \\dfrac{1}{n} = \\sum_{i=1}^{n} \\dfrac{i^2}{n^2} \\cdot \\dfrac{1}{n} = \\dfrac{1}{n^3} \\sum_{i=1}^{n} i^2$$",
               "justificacion_md": "Sustituimos $f(x_i) = x_i^2 = i^2/n^2$ y factorizamos $1/n^3$.",
               "es_resultado": False},
              {"accion_md": "**Usamos la fórmula** $\\sum_{i=1}^n i^2 = \\dfrac{n(n+1)(2n+1)}{6}$:\n\n$$S_n = \\dfrac{n(n+1)(2n+1)}{6 n^3} = \\dfrac{(n+1)(2n+1)}{6 n^2}$$",
               "justificacion_md": "Es la fórmula clásica de la suma de cuadrados. Con la simplificación queda en términos de $n$.",
               "es_resultado": False},
              {"accion_md": "**Tomamos el límite** $n \\to \\infty$:\n\n$$\\lim_{n \\to \\infty} \\dfrac{(n+1)(2n+1)}{6 n^2} = \\lim_{n \\to \\infty} \\dfrac{2n^2 + 3n + 1}{6 n^2} = \\dfrac{2}{6} = \\dfrac{1}{3}$$",
               "justificacion_md": "Cociente de polinomios al infinito con grados iguales: cociente de coeficientes principales.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^1 x^2 \\, dx = \\dfrac{1}{3}$.",
               "justificacion_md": "**Resultado clásico.** En la próxima lección veremos cómo obtenerlo en una línea con el Teorema Fundamental del Cálculo, sin pasar por sumas — pero entender la suma de Riemann es lo que da significado a la integral.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Convenciones útiles",
          body_md=(
              "Por convención y consistencia con propiedades posteriores:\n\n"
              "$$\\int_a^a f(x) \\, dx = 0$$\n\n"
              "$$\\int_a^b f(x) \\, dx = -\\int_b^a f(x) \\, dx$$\n\n"
              "La primera dice que el área sobre un punto es $0$. La segunda que invertir los límites cambia el signo — útil en cambio de variable y aditividad."
          )),

        b("intuicion",
          titulo="Integral con valores negativos",
          body_md=(
              "Si $f(x) < 0$ en parte del intervalo, los rectángulos correspondientes tienen \"altura negativa\": "
              "su contribución a la suma es **negativa**. Por eso la integral definida no es el \"área geométrica\" "
              "(que siempre es positiva), sino **área con signo**:\n\n"
              "$$\\int_a^b f(x) \\, dx = (\\text{área sobre el eje } x) - (\\text{área bajo el eje } x)$$"
          )),

        b("verificacion",
          intro_md="Verifica los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "¿Qué garantiza el teorema de integrabilidad?",
                  "opciones_md": [
                      "Toda función es integrable.",
                      "Si $f$ es continua en $[a, b]$, entonces es integrable.",
                      "Una función discontinua nunca es integrable.",
                      "La integral siempre es positiva.",
                  ],
                  "correcta": "B",
                  "pista_md": "Continuidad es **suficiente** pero no necesaria — funciones acotadas con pocas discontinuidades también son integrables.",
                  "explicacion_md": (
                      "**Continuidad ⇒ integrabilidad** es la condición suficiente clásica. La recíproca es falsa: hay funciones integrables no continuas (ej.: una función con un salto finito)."
                  ),
              },
              {
                  "enunciado_md": "Si $f(x) < 0$ en todo $[a, b]$, entonces $\\int_a^b f(x) \\, dx$ es:",
                  "opciones_md": [
                      "Positiva (es área).",
                      "Negativa.",
                      "Cero.",
                      "No existe.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Las alturas $f(x_i^*)$ son negativas, así cada término de la suma de Riemann es negativo. La integral es **área con signo**: si la curva está bajo el eje, da negativa."
                  ),
              },
          ]),

        ej(
            titulo="Suma de Riemann con extremos derechos",
            enunciado=(
                "Calcula $\\int_0^2 (x + 1) \\, dx$ usando la definición con sumas de Riemann derechas y partición regular."
            ),
            pistas=[
                "Partición: $\\Delta x = 2/n$, $x_i = 2i/n$. Suma derecha: $x_i^* = x_i$.",
                "Necesitarás $\\sum_{i=1}^n i = \\dfrac{n(n+1)}{2}$.",
                "Después de sumar y simplificar, toma el límite $n \\to \\infty$.",
            ],
            solucion=(
                "$f(x_i) = x_i + 1 = \\dfrac{2i}{n} + 1$. La suma:\n\n"
                "$$S_n = \\sum_{i=1}^{n} \\left(\\dfrac{2i}{n} + 1\\right) \\cdot \\dfrac{2}{n} = \\dfrac{2}{n} \\sum_{i=1}^n \\dfrac{2i}{n} + \\dfrac{2}{n} \\sum_{i=1}^n 1$$\n\n"
                "$$= \\dfrac{4}{n^2} \\cdot \\dfrac{n(n+1)}{2} + \\dfrac{2}{n} \\cdot n = \\dfrac{2(n+1)}{n} + 2$$\n\n"
                "**Límite:** $\\lim_{n \\to \\infty} \\left(\\dfrac{2(n+1)}{n} + 2\\right) = 2 + 2 = 4$.\n\n"
                "**Verificación geométrica:** la región bajo $y = x + 1$ entre $0$ y $2$ es un trapecio con bases $1$ y $3$, altura $2$. Área: $(1 + 3) \\cdot 2 / 2 = 4$. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir integral con área geométrica.** La integral es **área con signo**: negativa donde la curva está bajo el eje.",
              "**Olvidar el factor $\\Delta x$** en la suma. Cada rectángulo es $f(x_i^*) \\cdot \\Delta x_i$, no solo $f(x_i^*)$.",
              "**Usar la partición incorrecta.** Para suma derecha: $x_i^* = x_i = a + i \\Delta x$ ($i$ va de $1$ a $n$). Para suma izquierda: $x_i^* = x_{i-1}$ ($i$ va de $1$ a $n$, pero los puntos son $x_0$ a $x_{n-1}$).",
              "**No usar fórmulas cerradas para las sumas.** $\\sum i$, $\\sum i^2$, $\\sum i^3$ tienen fórmulas que evitan recurrencias. Memorizarlas ahorra muchísimo tiempo en la definición.",
              "**Pensar que toda función discontinua es no integrable.** Funciones acotadas con un número finito de saltos siguen siendo integrables.",
          ]),

        b("resumen",
          puntos_md=[
              "**Partición:** dividir $[a, b]$ en $n$ subintervalos.",
              "**Suma de Riemann:** $S = \\sum_{i=1}^n f(x_i^*) \\Delta x_i$, con $x_i^*$ en el $i$-ésimo subintervalo.",
              "**Integral definida:** $\\int_a^b f \\, dx = \\lim_{\\|P\\| \\to 0} S$, si el límite existe e independiente de los $x_i^*$.",
              "**Continuidad ⇒ integrabilidad** (condición suficiente, no necesaria).",
              "**Convenciones:** $\\int_a^a = 0$, $\\int_a^b = -\\int_b^a$.",
              "**Área con signo:** la integral es negativa donde $f < 0$.",
              "**Próxima lección:** integral indefinida — la antiderivada como herramienta para evitar sumas de Riemann.",
          ]),
    ]
    return {
        "id": "lec-integrales-1-1-definicion",
        "title": "Definición de integral",
        "description": "Sumas de Riemann, partición, integrabilidad y la integral definida como límite.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# LECCIÓN 1.2 — Integral indefinida
# =====================================================================
def lesson_1_2():
    blocks = [
        b("texto", body_md=(
            "Calcular toda integral por sumas de Riemann sería impracticable. "
            "Por suerte hay un atajo enorme: si encontramos una función $F$ tal que $F'(x) = f(x)$, "
            "muchas integrales se reducen a un cálculo algebraico. "
            "Esa función $F$ se llama **antiderivada** o **primitiva** de $f$, y a la familia de todas "
            "ellas se le da el nombre de **integral indefinida**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Comprender qué es una **antiderivada** y por qué hay infinitas (que difieren en una constante).\n"
            "- Manejar la **notación** $\\int f(x) \\, dx = F(x) + C$.\n"
            "- Memorizar la **tabla básica** de antiderivadas.\n"
            "- Aplicar las **propiedades de linealidad** para descomponer integrales."
        )),

        b("intuicion",
          titulo="La antiderivada como inversa de la derivada",
          body_md=(
              "Si la derivada es la operación que desciende grados ($x^3 \\to 3x^2$), la antiderivada es la que sube ($3x^2 \\to x^3$). \n\n"
              "Pero hay un detalle: la derivada de **cualquier constante** es $0$. Por eso, si $F(x) = x^3$ es una antiderivada de $3x^2$, entonces $G(x) = x^3 + 5$ también lo es: $G'(x) = 3x^2$. \n\n"
              "**Consecuencia:** las antiderivadas de una función $f$ forman una **familia de funciones** que difieren entre sí en una constante. Esa constante se llama **constante de integración**."
          )),

        b("definicion",
          titulo="Antiderivada (primitiva)",
          body_md=(
              "$F$ es una **antiderivada** (o **primitiva**) de $f$ en un intervalo $I$ si:\n\n"
              "$$F'(x) = f(x) \\quad \\text{para todo } x \\in I$$"
          )),

        b("teorema",
          nombre="Unicidad salvo constante",
          enunciado_md=(
              "Si $F$ y $G$ son ambas antiderivadas de $f$ en un intervalo $I$, entonces existe una constante $C$ tal que $G(x) = F(x) + C$ en $I$."
          ),
          demostracion_md=(
              "Sea $H = G - F$. Entonces $H'(x) = G'(x) - F'(x) = f(x) - f(x) = 0$ en todo $I$. "
              "Por la consecuencia 1 del Teorema del Valor Medio (capítulo 3 de Cálculo Diferencial), "
              "$H$ es **constante**. Llamando $C$ a esa constante: $G - F = C$, es decir, $G = F + C$."
          )),

        b("definicion",
          titulo="Integral indefinida",
          body_md=(
              "La **integral indefinida** de $f$ es la familia de todas sus antiderivadas:\n\n"
              "$$\\int f(x) \\, dx = F(x) + C$$\n\n"
              "donde $F$ es **una** antiderivada de $f$ y $C$ es la **constante de integración** (representa cualquier constante real).\n\n"
              "**Notación:**\n\n"
              "- $\\int$ — símbolo de integral.\n"
              "- $f(x)$ — el **integrando**.\n"
              "- $dx$ — diferencial; indica que $x$ es la variable.\n"
              "- $C$ — constante de integración (no se debe olvidar)."
          )),

        b("definicion",
          titulo="Tabla básica de antiderivadas",
          body_md=(
              "| $\\int f(x) \\, dx$ | Resultado |\n|---|---|\n"
              "| $\\int x^n \\, dx$ ($n \\neq -1$) | $\\dfrac{x^{n+1}}{n+1} + C$ |\n"
              "| $\\int \\dfrac{1}{x} \\, dx$ | $\\ln \\|x\\| + C$ |\n"
              "| $\\int e^x \\, dx$ | $e^x + C$ |\n"
              "| $\\int a^x \\, dx$ ($a > 0$) | $\\dfrac{a^x}{\\ln a} + C$ |\n"
              "| $\\int \\sin x \\, dx$ | $-\\cos x + C$ |\n"
              "| $\\int \\cos x \\, dx$ | $\\sin x + C$ |\n"
              "| $\\int \\sec^2 x \\, dx$ | $\\tan x + C$ |\n"
              "| $\\int \\csc^2 x \\, dx$ | $-\\cot x + C$ |\n"
              "| $\\int \\sec x \\tan x \\, dx$ | $\\sec x + C$ |\n"
              "| $\\int \\csc x \\cot x \\, dx$ | $-\\csc x + C$ |\n"
              "| $\\int \\dfrac{1}{\\sqrt{1 - x^2}} \\, dx$ | $\\arcsin x + C$ |\n"
              "| $\\int \\dfrac{1}{1 + x^2} \\, dx$ | $\\arctan x + C$ |\n"
              "| $\\int \\sinh x \\, dx$ | $\\cosh x + C$ |\n"
              "| $\\int \\cosh x \\, dx$ | $\\sinh x + C$ |\n\n"
              "Cada fila se verifica derivando el lado derecho. **Conviene memorizarla** — es el alfabeto del cálculo integral."
          )),

        b("teorema",
          nombre="Linealidad de la integral indefinida",
          enunciado_md=(
              "Si $f$ y $g$ tienen antiderivadas y $a, b$ son constantes:\n\n"
              "$$\\int [a \\, f(x) + b \\, g(x)] \\, dx = a \\int f(x) \\, dx + b \\int g(x) \\, dx$$\n\n"
              "En palabras: la integral respeta sumas y constantes multiplicativas."
          ),
          demostracion_md=(
              "Si $F' = f$ y $G' = g$, entonces $(aF + bG)' = aF' + bG' = af + bg$. "
              "Por tanto $aF + bG$ es antiderivada de $af + bg$, y la familia de antiderivadas se obtiene sumando $C$. "
              "El resultado se sigue por la unicidad salvo constante."
          )),

        b("ejemplo_resuelto",
          titulo="Polinomio simple",
          problema_md="Calcular $\\int (4x^3 - 6x^2 + 2x - 5) \\, dx$.",
          pasos=[
              {"accion_md": "**Linealidad** — separar término a término:\n\n$$\\int 4x^3 \\, dx - \\int 6x^2 \\, dx + \\int 2x \\, dx - \\int 5 \\, dx$$",
               "justificacion_md": "La integral respeta sumas/restas y constantes.",
               "es_resultado": False},
              {"accion_md": "**Aplicar la regla de la potencia** $\\int x^n \\, dx = \\dfrac{x^{n+1}}{n+1}$ a cada término:\n\n$$4 \\cdot \\dfrac{x^4}{4} - 6 \\cdot \\dfrac{x^3}{3} + 2 \\cdot \\dfrac{x^2}{2} - 5x + C$$",
               "justificacion_md": "Los coeficientes pasan adelante; las constantes se integran como $cx$.",
               "es_resultado": False},
              {"accion_md": "$$\\int (4x^3 - 6x^2 + 2x - 5) \\, dx = x^4 - 2x^3 + x^2 - 5x + C$$",
               "justificacion_md": "**Verificación:** derivando, $\\dfrac{d}{dx}(x^4 - 2x^3 + x^2 - 5x + C) = 4x^3 - 6x^2 + 2x - 5$. ✓",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Reescribir antes de integrar",
          problema_md="Calcular $\\int \\dfrac{x^2 + 3\\sqrt{x} - 1}{x} \\, dx$.",
          pasos=[
              {"accion_md": "**Reescribir** el integrando dividiendo cada término por $x$:\n\n$$\\dfrac{x^2}{x} + \\dfrac{3\\sqrt{x}}{x} - \\dfrac{1}{x} = x + 3 x^{-1/2} - \\dfrac{1}{x}$$",
               "justificacion_md": "$\\sqrt{x}/x = x^{1/2}/x = x^{-1/2}$. Reescribir como potencias permite usar la regla básica.",
               "es_resultado": False},
              {"accion_md": "**Integrar término a término:**\n\n$$\\int x \\, dx + 3 \\int x^{-1/2} \\, dx - \\int \\dfrac{1}{x} \\, dx$$\n\n$$= \\dfrac{x^2}{2} + 3 \\cdot \\dfrac{x^{1/2}}{1/2} - \\ln|x| + C$$",
               "justificacion_md": "Para $x^{-1/2}$: $\\dfrac{x^{-1/2 + 1}}{-1/2 + 1} = \\dfrac{x^{1/2}}{1/2} = 2 x^{1/2}$.",
               "es_resultado": False},
              {"accion_md": "$$= \\dfrac{x^2}{2} + 6 \\sqrt{x} - \\ln|x| + C$$",
               "justificacion_md": "**Lección general:** si el integrando tiene fracciones o raíces, **reescribir como potencias o sumar/restar términos** suele dejar todo en forma directamente integrable.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Por qué se omite $C$ a veces?",
          body_md=(
              "En la **integral definida** (próxima lección) la $C$ se cancela al evaluar entre los límites: $F(b) + C - (F(a) + C) = F(b) - F(a)$. Por eso ahí no aparece.\n\n"
              "Pero en la **integral indefinida** la $C$ es esencial: omitirla es escribir una sola antiderivada en lugar de la familia completa. **Olvidarla en un examen suele descontar puntos.**"
          )),

        b("verificacion",
          intro_md="Verifica el manejo:",
          preguntas=[
              {
                  "enunciado_md": "$\\int x^{-2} \\, dx = ?$",
                  "opciones_md": [
                      "$-\\dfrac{1}{x} + C$",
                      "$\\dfrac{1}{x} + C$",
                      "$-x^{-3} + C$",
                      "$\\ln|x| + C$",
                  ],
                  "correcta": "A",
                  "pista_md": "Aplica la regla de la potencia: $\\int x^n \\, dx = \\dfrac{x^{n+1}}{n+1}$. Con $n = -2$, ¿qué da?",
                  "explicacion_md": (
                      "$\\int x^{-2} \\, dx = \\dfrac{x^{-1}}{-1} + C = -\\dfrac{1}{x} + C$. **Atención al signo** del denominador $n+1 = -1$."
                  ),
              },
              {
                  "enunciado_md": "¿Cuál es la antiderivada de $\\dfrac{1}{x}$?",
                  "opciones_md": [
                      "$\\dfrac{x^0}{0}$ (no está definida)",
                      "$\\ln|x| + C$",
                      "$\\ln(x) + C$ (sin valor absoluto)",
                      "$x + C$",
                  ],
                  "correcta": "B",
                  "pista_md": "La regla de la potencia falla en $n = -1$. ¿Qué función tiene derivada $1/x$?",
                  "explicacion_md": (
                      "Para $n = -1$ la regla da $\\dfrac{x^0}{0}$, indefinida. La antiderivada correcta es $\\ln|x| + C$ (con valor absoluto, para incluir $x < 0$)."
                  ),
              },
          ]),

        ej(
            titulo="Mezclando reglas básicas",
            enunciado="Calcula $\\int \\left(2 \\sin x + e^x - \\dfrac{3}{1 + x^2}\\right) dx$.",
            pistas=[
                "Aplica linealidad y separa en tres integrales.",
                "Usa la tabla: $\\int \\sin x \\, dx = -\\cos x$, $\\int e^x \\, dx = e^x$, $\\int \\dfrac{1}{1+x^2} \\, dx = \\arctan x$.",
            ],
            solucion=(
                "$$\\int 2\\sin x \\, dx + \\int e^x \\, dx - 3 \\int \\dfrac{1}{1+x^2} \\, dx$$\n\n"
                "$$= -2\\cos x + e^x - 3 \\arctan x + C$$"
            ),
        ),

        ej(
            titulo="Recuperar una función desde su derivada",
            enunciado="Halla $f(x)$ sabiendo que $f'(x) = 6x^2 + 4x - 1$ y $f(1) = 5$.",
            pistas=[
                "Integra $f'$ para obtener $f$ con una constante $C$.",
                "Usa la condición $f(1) = 5$ para despejar $C$.",
            ],
            solucion=(
                "**Integramos:** $f(x) = \\int (6x^2 + 4x - 1) \\, dx = 2x^3 + 2x^2 - x + C$.\n\n"
                "**Condición:** $f(1) = 2 + 2 - 1 + C = 3 + C = 5$, así $C = 2$.\n\n"
                "**Respuesta:** $f(x) = 2x^3 + 2x^2 - x + 2$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar la constante $C$.** En la indefinida es obligatoria. La familia de antiderivadas no es una sola función, son infinitas.",
              "**Aplicar la regla de la potencia con $n = -1$.** No funciona — el denominador $n + 1$ se anula. Para $\\int 1/x$ usa $\\ln|x|$.",
              "**Olvidar el valor absoluto en $\\ln|x|$.** Sin él, la antiderivada solo está definida para $x > 0$.",
              "**Confundir $\\int a^x \\, dx$ con $a^x$.** La derivada de $a^x$ es $a^x \\ln a$, así la antiderivada de $a^x$ es $\\dfrac{a^x}{\\ln a}$. Solo cuando $a = e$ es \"la misma\".",
              "**Usar linealidad con productos:** $\\int f(x) g(x) \\, dx \\neq \\int f \\cdot \\int g$. No hay regla simple del producto en integración — hace falta integración por partes (capítulo 2).",
          ]),

        b("resumen",
          puntos_md=[
              "**Antiderivada** $F$ de $f$: $F'(x) = f(x)$.",
              "**Familia de antiderivadas:** $G = F + C$ para cualquier constante $C$ (consecuencia del TVM).",
              "**Notación:** $\\int f(x) \\, dx = F(x) + C$.",
              "**Tabla básica:** memorizarla; cubre potencias, exponenciales, trigonométricas, inversas e hiperbólicas.",
              "**Linealidad:** $\\int (af + bg) \\, dx = a \\int f + b \\int g$.",
              "**No olvidar $C$.** Salvo en la integral definida (próxima lección), donde se cancela.",
              "**Próxima lección:** integral definida y el Teorema Fundamental del Cálculo — el puente entre antiderivadas y áreas.",
          ]),
    ]
    return {
        "id": "lec-integrales-1-2-indefinida",
        "title": "Integral indefinida",
        "description": "Antiderivadas, familia de primitivas, tabla básica y propiedades de linealidad.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 2,
    }


# =====================================================================
# LECCIÓN 1.3 — Integral definida
# =====================================================================
def lesson_1_3():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora teníamos dos cosas separadas: la **integral definida** $\\int_a^b f \\, dx$ "
            "como límite de sumas de Riemann (lección 1.1), y la **integral indefinida** "
            "$\\int f \\, dx = F + C$ como antiderivada (lección 1.2). \n\n"
            "El **Teorema Fundamental del Cálculo (TFC)** — el resultado más importante del curso — "
            "**conecta ambas**: para evaluar $\\int_a^b f$ basta encontrar una antiderivada $F$ y calcular $F(b) - F(a)$.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Enunciar y aplicar el **TFC, partes 1 y 2**.\n"
            "- Evaluar integrales definidas usando la fórmula de Barrow.\n"
            "- Manejar las **propiedades** de la integral definida (linealidad, aditividad, signo).\n"
            "- Comprender la conexión entre antiderivada y área."
        )),

        b("intuicion",
          titulo="La función acumuladora",
          body_md=(
              "Sea $f$ continua en $[a, b]$ y definamos:\n\n"
              "$$A(x) = \\int_a^x f(t) \\, dt$$\n\n"
              "$A(x)$ es el **área acumulada** desde $a$ hasta $x$. Es una función nueva — depende del límite superior.\n\n"
              "**Pregunta clave:** ¿qué es $A'(x)$? Si pensamos en $A(x + h) - A(x)$, ese incremento es el área del \"trozo\" entre $x$ y $x + h$, que para $h$ pequeño es aproximadamente $f(x) \\cdot h$ (un rectángulo angosto). \n\n"
              "Dividiendo por $h$ y tomando límite: $A'(x) = f(x)$. **Eso es el TFC parte 1.**"
          )),

        b("teorema",
          nombre="TFC — Parte 1",
          enunciado_md=(
              "Si $f$ es continua en $[a, b]$ y se define\n\n"
              "$$A(x) = \\int_a^x f(t) \\, dt, \\quad x \\in [a, b]$$\n\n"
              "entonces $A$ es derivable en $(a, b)$ y\n\n"
              "$$A'(x) = f(x)$$\n\n"
              "Es decir, **toda función continua tiene antiderivada** — y una explícita es la función acumuladora."
          ),
          demostracion_md=(
              "Sea $h > 0$ pequeño. Por aditividad de la integral:\n\n"
              "$$A(x + h) - A(x) = \\int_a^{x+h} f - \\int_a^x f = \\int_x^{x+h} f$$\n\n"
              "Como $f$ es continua en $[x, x+h]$, por el teorema del valor medio para integrales existe $c \\in [x, x+h]$ con $\\int_x^{x+h} f = f(c) \\cdot h$. Entonces:\n\n"
              "$$\\dfrac{A(x+h) - A(x)}{h} = f(c)$$\n\n"
              "Cuando $h \\to 0^+$, $c \\to x$ y por continuidad de $f$, $f(c) \\to f(x)$. Análogo para $h \\to 0^-$. Por tanto $A'(x) = f(x)$."
          )),

        b("teorema",
          nombre="TFC — Parte 2 (Fórmula de Barrow)",
          enunciado_md=(
              "Si $f$ es continua en $[a, b]$ y $F$ es **cualquier antiderivada** de $f$ en $[a, b]$, entonces:\n\n"
              "$$\\int_a^b f(x) \\, dx = F(b) - F(a)$$\n\n"
              "**Notación común:** $F(b) - F(a) = \\bigl[F(x)\\bigr]_a^b$."
          ),
          demostracion_md=(
              "Por el TFC parte 1, la función $A(x) = \\int_a^x f$ es una antiderivada de $f$, "
              "con $A(a) = 0$ y $A(b) = \\int_a^b f$. Si $F$ es otra antiderivada, por unicidad salvo constante, "
              "$F(x) = A(x) + C$. Entonces $F(b) - F(a) = (A(b) + C) - (A(a) + C) = A(b) - A(a) = \\int_a^b f$. "
              "**La constante se cancela** — por eso no aparece en la integral definida."
          )),

        b("ejemplo_resuelto",
          titulo="Re-calcular $\\int_0^1 x^2 \\, dx$ con TFC",
          problema_md="En la lección 1.1 obtuvimos $\\int_0^1 x^2 \\, dx = 1/3$ con sumas de Riemann. Verificar usando el TFC.",
          pasos=[
              {"accion_md": "**Antiderivada:** $\\int x^2 \\, dx = \\dfrac{x^3}{3} + C$. Tomamos $F(x) = \\dfrac{x^3}{3}$ (sin la $C$, se cancela).",
               "justificacion_md": "Cualquier antiderivada sirve.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos Barrow:**\n\n$$\\int_0^1 x^2 \\, dx = F(1) - F(0) = \\dfrac{1}{3} - 0 = \\dfrac{1}{3}$$",
               "justificacion_md": "**Una línea** vs el cálculo de varias páginas con Riemann. Esa es la potencia del TFC.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Integral con suma y resta",
          problema_md="Calcular $\\int_1^4 (3x^2 - 2x + 1) \\, dx$.",
          pasos=[
              {"accion_md": "**Antiderivada por linealidad:** $F(x) = x^3 - x^2 + x$.",
               "justificacion_md": "Cada término por la regla de la potencia, sin $C$.",
               "es_resultado": False},
              {"accion_md": "**Evaluamos en los límites:**\n\n$F(4) = 64 - 16 + 4 = 52$. $F(1) = 1 - 1 + 1 = 1$.",
               "justificacion_md": "Sustitución directa.",
               "es_resultado": False},
              {"accion_md": "$$\\int_1^4 (3x^2 - 2x + 1) \\, dx = F(4) - F(1) = 52 - 1 = 51$$",
               "justificacion_md": "Listo. Tres pasos: antiderivada, evaluar, restar.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Propiedades de la integral definida",
          body_md=(
              "Si $f$ y $g$ son integrables en $[a, b]$ y $k \\in \\mathbb{R}$:\n\n"
              "**1. Linealidad:** $\\int_a^b [k f(x) + g(x)] \\, dx = k \\int_a^b f + \\int_a^b g$.\n\n"
              "**2. Aditividad de intervalos:** para $a < c < b$,\n\n"
              "$$\\int_a^b f \\, dx = \\int_a^c f \\, dx + \\int_c^b f \\, dx$$\n\n"
              "**3. Inversión de límites:** $\\int_a^b f = -\\int_b^a f$.\n\n"
              "**4. Comparación:** si $f(x) \\leq g(x)$ en $[a, b]$, entonces $\\int_a^b f \\leq \\int_a^b g$.\n\n"
              "**5. Acotación:** si $m \\leq f(x) \\leq M$ en $[a, b]$:\n\n"
              "$$m(b - a) \\leq \\int_a^b f \\, dx \\leq M(b - a)$$"
          )),

        b("ejemplo_resuelto",
          titulo="Aditividad: función por tramos",
          problema_md=(
              "Calcular $\\int_0^2 f(x) \\, dx$ donde $f(x) = \\begin{cases} x^2 & 0 \\leq x \\leq 1 \\\\ 2 - x & 1 < x \\leq 2 \\end{cases}$."
          ),
          pasos=[
              {"accion_md": "**Aditividad** en $c = 1$:\n\n$$\\int_0^2 f \\, dx = \\int_0^1 x^2 \\, dx + \\int_1^2 (2 - x) \\, dx$$",
               "justificacion_md": "Cuando $f$ está definida por tramos, partimos en los puntos de cambio.",
               "es_resultado": False},
              {"accion_md": "**Primer trozo:** $\\int_0^1 x^2 \\, dx = \\dfrac{x^3}{3}\\Big|_0^1 = \\dfrac{1}{3}$.\n\n**Segundo trozo:** $\\int_1^2 (2 - x) \\, dx = \\left[2x - \\dfrac{x^2}{2}\\right]_1^2 = (4 - 2) - (2 - \\tfrac{1}{2}) = 2 - \\tfrac{3}{2} = \\tfrac{1}{2}$.",
               "justificacion_md": "Cada trozo evaluado con su antiderivada y los límites correspondientes.",
               "es_resultado": False},
              {"accion_md": "**Total:** $\\int_0^2 f = \\dfrac{1}{3} + \\dfrac{1}{2} = \\dfrac{5}{6}$.",
               "justificacion_md": "Sumamos las dos contribuciones.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="TFC parte 1 con cadena",
          problema_md="Calcular $\\dfrac{d}{dx} \\int_0^{x^2} \\sin(t^3) \\, dt$.",
          pasos=[
              {"accion_md": "**Definimos** $A(u) = \\int_0^u \\sin(t^3) \\, dt$. Por TFC parte 1, $A'(u) = \\sin(u^3)$.",
               "justificacion_md": "El TFC nos da la derivada de la función acumuladora respecto al **límite superior**.",
               "es_resultado": False},
              {"accion_md": "Lo que pide es $\\dfrac{d}{dx} A(x^2)$, una composición. Por **regla de la cadena:**\n\n$$\\dfrac{d}{dx} A(x^2) = A'(x^2) \\cdot 2x = \\sin\\left((x^2)^3\\right) \\cdot 2x = 2x \\sin(x^6)$$",
               "justificacion_md": "**Patrón general:** $\\dfrac{d}{dx} \\int_a^{g(x)} f(t) \\, dt = f(g(x)) \\cdot g'(x)$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el dominio:",
          preguntas=[
              {
                  "enunciado_md": "$\\int_0^\\pi \\sin x \\, dx = ?$",
                  "opciones_md": ["$0$", "$1$", "$2$", "$\\pi$"],
                  "correcta": "C",
                  "pista_md": "Antiderivada: $\\int \\sin x \\, dx = -\\cos x$. Evalúa entre $0$ y $\\pi$.",
                  "explicacion_md": (
                      "$F(x) = -\\cos x$. $F(\\pi) - F(0) = -\\cos\\pi - (-\\cos 0) = -(-1) - (-1) = 1 + 1 = 2$."
                  ),
              },
              {
                  "enunciado_md": "Si $\\int_0^3 f = 5$ y $\\int_0^7 f = 12$, ¿cuánto vale $\\int_3^7 f$?",
                  "opciones_md": ["$7$", "$17$", "$-7$", "$60$"],
                  "correcta": "A",
                  "pista_md": "Aditividad: $\\int_0^7 f = \\int_0^3 f + \\int_3^7 f$.",
                  "explicacion_md": (
                      "Por aditividad: $12 = 5 + \\int_3^7 f \\implies \\int_3^7 f = 7$."
                  ),
              },
              {
                  "enunciado_md": "$\\dfrac{d}{dx} \\int_2^x t e^t \\, dt = ?$",
                  "opciones_md": [
                      "$x e^x$",
                      "$e^x$",
                      "$x e^x - 2 e^2$",
                      "$\\int_2^x e^t \\, dt$",
                  ],
                  "correcta": "A",
                  "pista_md": "TFC parte 1: $\\dfrac{d}{dx} \\int_a^x f(t) \\, dt = f(x)$. Sin necesidad de calcular la integral.",
                  "explicacion_md": (
                      "El TFC parte 1 dice que la derivada de la acumuladora es el integrando evaluado en $x$. **No hace falta** calcular $\\int t e^t$ — eso requeriría partes."
                  ),
              },
          ]),

        ej(
            titulo="Aplicar TFC con linealidad",
            enunciado="Calcula $\\int_1^e \\dfrac{1 + x^2 - 3x}{x} \\, dx$.",
            pistas=[
                "Reescribe el integrando: $\\dfrac{1}{x} + x - 3$.",
                "Integra cada término por separado.",
                "Recuerda $\\int 1/x \\, dx = \\ln|x|$, y $\\ln e = 1$.",
            ],
            solucion=(
                "**Reescribimos:** $\\dfrac{1 + x^2 - 3x}{x} = \\dfrac{1}{x} + x - 3$.\n\n"
                "**Antiderivada:** $F(x) = \\ln|x| + \\dfrac{x^2}{2} - 3x$.\n\n"
                "**Evaluamos:** $F(e) = 1 + \\dfrac{e^2}{2} - 3e$. $F(1) = 0 + \\dfrac{1}{2} - 3 = -\\dfrac{5}{2}$.\n\n"
                "**Resultado:** $F(e) - F(1) = 1 + \\dfrac{e^2}{2} - 3e + \\dfrac{5}{2} = \\dfrac{7}{2} + \\dfrac{e^2}{2} - 3e$."
            ),
        ),

        ej(
            titulo="TFC parte 1 con cadena (más complejo)",
            enunciado="Calcula $\\dfrac{d}{dx} \\int_{\\sin x}^{\\cos x} (1 + t^2) \\, dt$.",
            pistas=[
                "Cuando ambos límites son funciones de $x$, escribe la integral como diferencia: $\\int_a^{\\cos x} - \\int_a^{\\sin x}$.",
                "Aplica TFC parte 1 + cadena a cada una.",
            ],
            solucion=(
                "Por aditividad, eligiendo cualquier $a$:\n\n"
                "$$\\int_{\\sin x}^{\\cos x} (1 + t^2) \\, dt = \\int_a^{\\cos x} (1+t^2) \\, dt - \\int_a^{\\sin x} (1+t^2) \\, dt$$\n\n"
                "Derivando con TFC + cadena:\n\n"
                "$$(1 + \\cos^2 x)(-\\sin x) - (1 + \\sin^2 x)(\\cos x)$$\n\n"
                "$$= -\\sin x (1 + \\cos^2 x) - \\cos x (1 + \\sin^2 x)$$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar evaluar en los dos límites.** $\\int_a^b f = F(b) - F(a)$, no solo $F(b)$.",
              "**Restar al revés:** $F(a) - F(b)$ en lugar de $F(b) - F(a)$. El orden importa.",
              "**Aplicar TFC parte 1 sin verificar continuidad** del integrando. Si $f$ tiene discontinuidad en $[a, b]$, no aplica directamente.",
              "**No usar la cadena** cuando el límite superior es $g(x)$, no solo $x$. La derivada es $f(g(x)) \\cdot g'(x)$, no solo $f(g(x))$.",
              "**Confundirse con el dominio del antiderivado.** Por ejemplo, $\\int_{-1}^1 \\dfrac{1}{x} \\, dx$ **no** es $\\ln|1| - \\ln|-1| = 0$ porque $1/x$ no es integrable cerca de $0$ (es una integral impropia, capítulo 2).",
          ]),

        b("resumen",
          puntos_md=[
              "**TFC parte 1:** $A(x) = \\int_a^x f \\implies A'(x) = f(x)$ (toda continua tiene antiderivada).",
              "**TFC parte 2 (Barrow):** $\\int_a^b f = F(b) - F(a)$ donde $F$ es cualquier antiderivada.",
              "**Notación:** $F(b) - F(a) = \\bigl[F(x)\\bigr]_a^b$.",
              "**Propiedades:** linealidad, aditividad de intervalos, inversión de límites, comparación.",
              "**TFC con cadena:** $\\dfrac{d}{dx} \\int_a^{g(x)} f \\, dt = f(g(x)) g'(x)$.",
              "**Próximo capítulo:** métodos de integración — sustitución, partes, fracciones parciales — para calcular integrales que la tabla básica no resuelve directamente.",
          ]),
    ]
    return {
        "id": "lec-integrales-1-3-definida",
        "title": "Integral definida",
        "description": "Teorema Fundamental del Cálculo (partes 1 y 2), evaluación con la fórmula de Barrow y propiedades.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    course_id = "calculo-integral"

    # 1. Crear/asegurar el curso
    course_doc = {
        "id": course_id,
        "title": "Cálculo Integral",
        "description": "Sumas de Riemann, integrales definidas e indefinidas, métodos de integración (sustitución, partes, fracciones parciales) y aplicaciones (áreas, volúmenes, longitud de arco).",
        "category": "Matemáticas",
        "level": "Intermedio",
        "modules_count": 3,
        "rating": 4.8,
        "summary": "Curso completo de cálculo integral para alumnos universitarios chilenos.",
        "created_at": now(),
        "visible_to_students": True,
    }
    existing = await db.courses.find_one({"id": course_id})
    if existing:
        # Mantener visible_to_students y rating si ya están seteados
        update_fields = {k: v for k, v in course_doc.items() if k != "created_at"}
        await db.courses.update_one({"id": course_id}, {"$set": update_fields})
        print(f"✓ Curso actualizado: {course_doc['title']}")
    else:
        await db.courses.insert_one(course_doc)
        print(f"✓ Curso creado: {course_doc['title']}")

    # 2. Capítulo Integrales (idempotente: borra y re-crea)
    chapter_id = "ch-integrales"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Integrales",
        "description": "Definición de integral, sumas de Riemann, integral indefinida y definida, Teorema Fundamental del Cálculo.",
        "order": 1,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    # 3. Lecciones
    builders = [lesson_1_1, lesson_1_2, lesson_1_3]
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
    print(f"✅ Capítulo 1 — Integrales listo: {len(builders)} lecciones, {total_blocks} bloques.")
    print()
    print("Lecciones disponibles en:")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
