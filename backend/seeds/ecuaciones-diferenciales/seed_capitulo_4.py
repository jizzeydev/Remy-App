"""
Seed del curso Ecuaciones Diferenciales — Capítulo 4: Transformada de Laplace.

Crea el capítulo 'Transformada de Laplace' bajo el curso 'ecuaciones-diferenciales'
y siembra sus 6 lecciones:

  - Transformada de Laplace e inversa
  - Existencia y unicidad
  - Resolución de EDOs con Laplace
  - Traslaciones y convolución
  - Multiplicación por t y funciones periódicas
  - Sistemas y ecuaciones con coeficientes variables

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
# Transformada de Laplace e inversa
# =====================================================================
def lesson_definicion_inversa():
    blocks = [
        b("texto", body_md=(
            "La **transformada de Laplace** es una **herramienta integral** que convierte un problema "
            "diferencial en un problema **algebraico** — más fácil de resolver. Su poder está en cuatro "
            "puntos:\n\n"
            "1. **Transforma derivadas en multiplicaciones por $s$**, así una EDO lineal se vuelve una "
            "ecuación algebraica para la transformada $X(s)$.\n"
            "2. **Incorpora las condiciones iniciales automáticamente** durante la transformación.\n"
            "3. **Maneja sin esfuerzo forzantes discontinuos** (escalones, pulsos, impulsos) — algo difícil "
            "con los métodos del Cap. 2.\n"
            "4. **Es la base del análisis de sistemas en ingeniería** (control, electrónica, procesamiento de señales).\n\n"
            "**Idea matemática.** Dada una función $f(t)$ definida en $[0, \\infty)$, su transformada es la "
            "**integral**\n\n"
            "$$\\mathcal{L}\\{f(t)\\}(s) = F(s) = \\int_0^{\\infty} e^{-s t}\\, f(t)\\, dt,$$\n\n"
            "una función de la **nueva variable $s$**. Para recuperar $f$ a partir de $F$ se aplica la "
            "**transformada inversa** $\\mathcal{L}^{-1}$.\n\n"
            "**Al terminar:**\n\n"
            "- Calculas la transformada por **definición** para funciones básicas.\n"
            "- Manejas la **tabla estándar** de transformadas.\n"
            "- Aplicas la **linealidad** para transformadas combinadas.\n"
            "- Inviertes una transformada usando tabla y descomposición en **fracciones parciales**."
        )),

        b("definicion",
          titulo="Transformada de Laplace",
          body_md=(
              "Sea $f : [0, \\infty) \\to \\mathbb{R}$. Su **transformada de Laplace** es la función\n\n"
              "$$\\boxed{\\,F(s) = \\mathcal{L}\\{f(t)\\}(s) = \\int_0^{\\infty} e^{-s t}\\, f(t)\\, dt,\\,}$$\n\n"
              "definida para los valores de $s$ donde la integral converge. Llamamos **abscisa de "
              "convergencia** al menor $c$ tal que $F(s)$ existe para $s > c$.\n\n"
              "**Notación.** Si $f$ se denota con minúscula, $F$ con mayúscula. Es decir, "
              "$\\mathcal{L}\\{f\\} = F$, $\\mathcal{L}\\{g\\} = G$, $\\mathcal{L}\\{x\\} = X$, etc.\n\n"
              "**Variable $s$.** Aunque en este curso $s$ es real, la teoría completa permite $s \\in \\mathbb{C}$. "
              "La parte real $\\operatorname{Re}(s)$ debe ser mayor que la abscisa de convergencia.\n\n"
              "**Linealidad.** Para constantes $a, b$:\n\n"
              "$$\\mathcal{L}\\{a f(t) + b g(t)\\} = a F(s) + b G(s).$$\n\n"
              "Esta es la propiedad fundamental que se usa en cada cálculo."
          )),

        formulas(
            titulo="Tabla básica de transformadas",
            body=(
                "Las transformadas de las funciones más comunes:\n\n"
                "| $f(t)$ | $F(s) = \\mathcal{L}\\{f\\}$ | Dominio |\n"
                "|---|---|---|\n"
                "| $1$ | $\\dfrac{1}{s}$ | $s > 0$ |\n"
                "| $t^n$ ($n$ entero $\\geq 1$) | $\\dfrac{n!}{s^{n+1}}$ | $s > 0$ |\n"
                "| $t^{\\alpha}$ ($\\alpha > -1$) | $\\dfrac{\\Gamma(\\alpha + 1)}{s^{\\alpha + 1}}$ | $s > 0$ |\n"
                "| $e^{a t}$ | $\\dfrac{1}{s - a}$ | $s > a$ |\n"
                "| $\\sin(b t)$ | $\\dfrac{b}{s^2 + b^2}$ | $s > 0$ |\n"
                "| $\\cos(b t)$ | $\\dfrac{s}{s^2 + b^2}$ | $s > 0$ |\n"
                "| $\\sinh(b t)$ | $\\dfrac{b}{s^2 - b^2}$ | $s > |b|$ |\n"
                "| $\\cosh(b t)$ | $\\dfrac{s}{s^2 - b^2}$ | $s > |b|$ |\n"
                "| $t^n e^{a t}$ | $\\dfrac{n!}{(s - a)^{n + 1}}$ | $s > a$ |\n"
                "| $e^{a t}\\sin(b t)$ | $\\dfrac{b}{(s - a)^2 + b^2}$ | $s > a$ |\n"
                "| $e^{a t}\\cos(b t)$ | $\\dfrac{s - a}{(s - a)^2 + b^2}$ | $s > a$ |\n\n"
                "**Función Gamma:** $\\Gamma(x) = \\int_0^{\\infty} e^{-t} t^{x - 1}\\, dt$. Cumple "
                "$\\Gamma(x + 1) = x \\Gamma(x)$, $\\Gamma(n + 1) = n!$ para $n \\in \\mathbb{N}$, "
                "$\\Gamma(1/2) = \\sqrt{\\pi}$. Aparece para potencias **no enteras**."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Calcular $\\mathcal{L}\\{1\\}$ por definición",
          problema_md="Calcula la transformada de la función constante $f(t) \\equiv 1$.",
          pasos=[
              {"accion_md": (
                  "**Aplicar la definición:**\n\n"
                  "$$F(s) = \\int_0^{\\infty} e^{-s t} \\cdot 1\\, dt = \\lim_{R \\to \\infty} \\int_0^R e^{-s t}\\, dt.$$"
              ),
               "justificacion_md": "Antiderivada elemental.",
               "es_resultado": False},
              {"accion_md": (
                  "**Antiderivada:** $\\int e^{-s t}\\, dt = -\\dfrac{1}{s} e^{-s t}$.\n\n"
                  "**Evaluar:** $\\left[-\\dfrac{1}{s} e^{-s t}\\right]_0^R = -\\dfrac{1}{s} e^{-s R} + \\dfrac{1}{s}$."
              ),
               "justificacion_md": "El límite cuando $R \\to \\infty$ existe solo si $s > 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Tomar el límite** $R \\to \\infty$ con $s > 0$: $e^{-s R} \\to 0$.\n\n"
                  "$$\\mathcal{L}\\{1\\} = \\dfrac{1}{s}, \\qquad s > 0.$$"
              ),
               "justificacion_md": "La abscisa de convergencia es $0$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Calcular $\\mathcal{L}\\{e^{a t}\\}$",
          problema_md="Calcula la transformada de $f(t) = e^{a t}$.",
          pasos=[
              {"accion_md": (
                  "**Definición:** $F(s) = \\int_0^{\\infty} e^{-s t} e^{a t}\\, dt = \\int_0^{\\infty} e^{-(s - a) t}\\, dt$."
              ),
               "justificacion_md": "Combinar exponenciales.",
               "es_resultado": False},
              {"accion_md": (
                  "**Mismo cálculo que $\\mathcal{L}\\{1\\}$ con $s$ reemplazado por $s - a$**, válido si $s - a > 0$ es decir $s > a$.\n\n"
                  "$$\\mathcal{L}\\{e^{a t}\\} = \\dfrac{1}{s - a}, \\qquad s > a.$$"
              ),
               "justificacion_md": "La abscisa de convergencia se desplaza con $a$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Calcular $\\mathcal{L}\\{\\cos(b t)\\}$ usando Euler",
          problema_md="Calcula la transformada de $\\cos(b t)$.",
          pasos=[
              {"accion_md": (
                  "**Fórmula de Euler:** $\\cos(b t) = \\dfrac{e^{i b t} + e^{-i b t}}{2}$.\n\n"
                  "**Por linealidad:** $\\mathcal{L}\\{\\cos(b t)\\} = \\dfrac{1}{2}\\bigl(\\mathcal{L}\\{e^{i b t}\\} + \\mathcal{L}\\{e^{-i b t}\\}\\bigr)$."
              ),
               "justificacion_md": "El ejemplo anterior se extiende a $a$ complejo formalmente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar:** $\\mathcal{L}\\{e^{i b t}\\} = \\dfrac{1}{s - i b}$, $\\mathcal{L}\\{e^{-i b t}\\} = \\dfrac{1}{s + i b}$.\n\n"
                  "**Sumar:** $\\dfrac{1}{2}\\left(\\dfrac{1}{s - i b} + \\dfrac{1}{s + i b}\\right) = \\dfrac{1}{2} \\cdot \\dfrac{2 s}{s^2 + b^2} = \\dfrac{s}{s^2 + b^2}$."
              ),
               "justificacion_md": "Suma de fracciones complejas con denominador real.",
               "es_resultado": False},
              {"accion_md": (
                  "**Resultado:** $\\mathcal{L}\\{\\cos(b t)\\} = \\dfrac{s}{s^2 + b^2}$, $s > 0$. Análogamente, $\\mathcal{L}\\{\\sin(b t)\\} = \\dfrac{b}{s^2 + b^2}$ (parte imaginaria)."
              ),
               "justificacion_md": "Resultado fundamental de la tabla.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Transformada inversa",
          body_md=(
              "La **transformada inversa** $\\mathcal{L}^{-1}\\{F(s)\\}$ recupera $f(t)$ a partir de $F(s)$:\n\n"
              "$$\\mathcal{L}\\{f\\} = F \\;\\Longleftrightarrow\\; f = \\mathcal{L}^{-1}\\{F\\}.$$\n\n"
              "**Linealidad:** $\\mathcal{L}^{-1}\\{a F(s) + b G(s)\\} = a f(t) + b g(t)$.\n\n"
              "**Estrategia práctica.** En la práctica no se calcula la inversa con la fórmula de Bromwich "
              "(integral en el plano complejo). En vez de eso:\n\n"
              "1. Si $F(s)$ está **directamente en la tabla**, leer $f$ de inmediato.\n"
              "2. Si no, **descomponer en fracciones parciales** hasta que cada sumando esté en la tabla.\n"
              "3. Aplicar linealidad para sumar las inversas.\n\n"
              "**Unicidad** (lección siguiente): bajo hipótesis estándar, $\\mathcal{L}^{-1}$ está bien "
              "definida — dos funciones distintas no pueden tener la misma transformada."
          )),

        b("ejemplo_resuelto",
          titulo="Inversa por fracciones parciales",
          problema_md="Calcula $\\mathcal{L}^{-1}\\left\\{\\dfrac{3 s + 1}{s^2 + 4}\\right\\}$.",
          pasos=[
              {"accion_md": (
                  "**Separar en partes que estén en la tabla:**\n\n"
                  "$\\dfrac{3 s + 1}{s^2 + 4} = 3 \\cdot \\dfrac{s}{s^2 + 4} + \\dfrac{1}{s^2 + 4} = 3 \\cdot \\dfrac{s}{s^2 + 4} + \\dfrac{1}{2} \\cdot \\dfrac{2}{s^2 + 4}$."
              ),
               "justificacion_md": "Reconocer las formas $\\cos(2t) \\to s/(s^2 + 4)$ y $\\sin(2t) \\to 2/(s^2 + 4)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar inversa término a término:**\n\n"
                  "$$\\mathcal{L}^{-1}\\left\\{\\dfrac{3 s + 1}{s^2 + 4}\\right\\} = 3 \\cos(2 t) + \\dfrac{1}{2}\\sin(2 t).$$"
              ),
               "justificacion_md": "Linealidad de la inversa.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inversa con denominador factorizable",
          problema_md="Calcula $\\mathcal{L}^{-1}\\left\\{\\dfrac{s + 3}{(s + 1)(s + 2)}\\right\\}$.",
          pasos=[
              {"accion_md": (
                  "**Fracciones parciales:** $\\dfrac{s + 3}{(s + 1)(s + 2)} = \\dfrac{A}{s + 1} + \\dfrac{B}{s + 2}$.\n\n"
                  "Multiplicando por $(s + 1)(s + 2)$: $s + 3 = A(s + 2) + B(s + 1)$. Tomando $s = -1$: $A = 2$. Tomando $s = -2$: $B = -1$."
              ),
               "justificacion_md": "Método de cobertura (Heaviside).",
               "es_resultado": False},
              {"accion_md": (
                  "**Inversa de cada parte:**\n\n"
                  "$$\\mathcal{L}^{-1}\\left\\{\\dfrac{2}{s + 1} - \\dfrac{1}{s + 2}\\right\\} = 2 e^{-t} - e^{-2 t}.$$"
              ),
               "justificacion_md": "$\\mathcal{L}^{-1}\\{1/(s - a)\\} = e^{a t}$.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué la transformada 'simplifica' EDOs.** El factor $e^{-s t}$ pesa la función $f(t)$ y "
            "calcula una especie de 'momento' parametrizado por $s$. Pero su utilidad real surge de la "
            "**propiedad de derivadas** (lección 3): derivar $f$ se traduce en multiplicar $F$ por $s$. Así, "
            "una EDO lineal en $f$ se vuelve una **ecuación algebraica** en $F$.\n\n"
            "**Analogía con logaritmo.** El logaritmo convierte productos en sumas: "
            "$\\log(a b) = \\log a + \\log b$. La transformada de Laplace convierte cálculo en álgebra: "
            "$\\mathcal{L}\\{f'\\} = s F$. En ambos casos, transformar el problema lo simplifica; al final, "
            "se aplica la inversa para volver al mundo original.\n\n"
            "**Variable $s$.** Conceptualmente $s$ tiene unidades de '1 / tiempo', es decir, **frecuencia**. "
            "Por eso la transformada de Laplace está íntimamente conectada con el análisis de frecuencias y "
            "con la transformada de Fourier."
        )),

        fig(
            "Diagrama del flujo de resolución de una EDO con transformada de Laplace. "
            "Tres cajas conectadas con flechas. "
            "Caja izquierda 'Problema en t: EDO + condiciones iniciales' en gris. "
            "Flecha hacia la derecha etiquetada 'Aplicar L (transformada)' lleva a "
            "Caja central 'Problema algebraico en s: ecuación para X(s)' en teal #06b6d4. "
            "Flecha hacia abajo etiquetada 'Resolver para X(s)' lleva a "
            "Caja inferior 'Aplicar L^{-1} (inversa)' lleva a "
            "Caja final 'Solución x(t)' en ámbar #f59e0b. "
            "Eje del tiempo y del 's' indicados sutilmente. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\mathcal{L}\\{t^3\\} = $",
                  "opciones_md": ["$\\dfrac{1}{s^4}$", "**$\\dfrac{6}{s^4}$**", "$\\dfrac{3}{s^4}$", "$\\dfrac{1}{s^3}$"],
                  "correcta": "B",
                  "pista_md": "$\\mathcal{L}\\{t^n\\} = n! / s^{n+1}$.",
                  "explicacion_md": "$3! = 6$, exponente $n + 1 = 4$.",
              },
              {
                  "enunciado_md": "$\\mathcal{L}\\{e^{-2 t}\\} = $",
                  "opciones_md": ["$\\dfrac{1}{s + 2}$", "$\\dfrac{1}{s - 2}$", "$\\dfrac{2}{s^2 + 4}$", "$\\dfrac{s}{s^2 - 4}$"],
                  "correcta": "A",
                  "pista_md": "$\\mathcal{L}\\{e^{a t}\\} = 1/(s - a)$ con $a = -2$.",
                  "explicacion_md": "$1 / (s - (-2)) = 1 / (s + 2)$.",
              },
              {
                  "enunciado_md": "$\\mathcal{L}^{-1}\\{6 / s^4\\} = $",
                  "opciones_md": ["$6 t^3$", "**$t^3$**", "$t^4$", "$6 t^4$"],
                  "correcta": "B",
                  "pista_md": "Inversa de $n!/s^{n + 1}$ es $t^n$.",
                  "explicacion_md": "$6 / s^4 = 3!/s^{3 + 1} \\to t^3$.",
              },
          ]),

        ej(
            "Transformada de un polinomio",
            "Calcula $\\mathcal{L}\\{3 t^2 - 4 t + 5\\}$.",
            ["Linealidad y tabla."],
            (
                "$3 \\cdot \\dfrac{2!}{s^3} - 4 \\cdot \\dfrac{1!}{s^2} + 5 \\cdot \\dfrac{1}{s} = \\dfrac{6}{s^3} - \\dfrac{4}{s^2} + \\dfrac{5}{s}$."
            ),
        ),

        ej(
            "Transformada con Gamma",
            "Calcula $\\mathcal{L}\\{t^{1/2}\\}$.",
            ["$\\Gamma(3/2) = \\sqrt{\\pi}/2$."],
            (
                "$\\mathcal{L}\\{t^{1/2}\\} = \\dfrac{\\Gamma(3/2)}{s^{3/2}} = \\dfrac{\\sqrt{\\pi}}{2 s^{3/2}}$."
            ),
        ),

        ej(
            "Inversión por descomposición",
            "Calcula $\\mathcal{L}^{-1}\\left\\{\\dfrac{2 s + 5}{s^2 + 9}\\right\\}$.",
            ["Separar en $\\cos$ y $\\sin$ con $b = 3$."],
            (
                "$\\dfrac{2 s + 5}{s^2 + 9} = 2 \\cdot \\dfrac{s}{s^2 + 9} + \\dfrac{5}{3} \\cdot \\dfrac{3}{s^2 + 9}$. "
                "Inversa: $2 \\cos(3 t) + \\dfrac{5}{3} \\sin(3 t)$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el dominio de convergencia.** Cada transformada vale solo para $s$ mayor que cierta abscisa.",
              "**Equivocar el signo en $s - a$ vs. $s + a$.** $\\mathcal{L}\\{e^{a t}\\} = 1/(s - a)$, así $\\mathcal{L}\\{e^{-t}\\} = 1/(s + 1)$.",
              "**Confundir $\\mathcal{L}\\{t^n\\} = n!/s^{n + 1}$ con $1/s^{n + 1}$.** Hay que multiplicar por el factorial.",
              "**Usar la tabla con potencias enteras cuando son fraccionarias.** Para $t^{\\alpha}$ con $\\alpha$ no entero hay que usar la fórmula con Gamma.",
              "**Olvidar la linealidad al invertir.** $\\mathcal{L}^{-1}$ es lineal — descomponer y aplicar a cada parte.",
          ]),

        b("resumen",
          puntos_md=[
              "**Transformada de Laplace:** $F(s) = \\int_0^{\\infty} e^{-s t} f(t) dt$. Lineal.",
              "**Tabla básica:** $1, t^n, e^{a t}, \\sin/\\cos, \\sinh/\\cosh, e^{a t} t^n, e^{a t}\\sin/\\cos$.",
              "**Función Gamma:** generaliza el factorial a potencias no enteras.",
              "**Transformada inversa:** se calcula con tabla + fracciones parciales + linealidad.",
              "**Próxima lección:** condiciones que garantizan que la transformada exista y la inversa sea única.",
          ]),
    ]
    return {
        "id": "lec-ed-4-1-transformada-inversa",
        "title": "Transformada de Laplace e inversa",
        "description": "Definición integral de la transformada de Laplace, linealidad, tabla básica de transformadas (potencias, exponenciales, trigonométricas), función Gamma y transformada inversa con fracciones parciales.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 1,
    }


# =====================================================================
# Existencia y unicidad
# =====================================================================
def lesson_existencia_unicidad():
    blocks = [
        b("texto", body_md=(
            "Antes de usar la transformada como herramienta sistemática, hay dos preguntas teóricas "
            "esenciales:\n\n"
            "1. **¿Para qué funciones $f(t)$ existe $\\mathcal{L}\\{f\\}$?** Es decir, ¿cuándo converge la integral?\n"
            "2. **¿Es única la transformada inversa?** Si dos funciones distintas pueden tener la misma "
            "transformada, $\\mathcal{L}^{-1}$ no está bien definida.\n\n"
            "Las respuestas son **sí, bajo hipótesis muy generales** que cubren prácticamente todas las "
            "funciones que aparecen en aplicaciones físicas.\n\n"
            "**Al terminar:**\n\n"
            "- Reconoces qué significa que $f$ sea de **orden exponencial**.\n"
            "- Aplicas el **teorema de existencia** para verificar que una transformada esté bien definida.\n"
            "- Conoces el **teorema de unicidad** que justifica el uso de $\\mathcal{L}^{-1}$.\n"
            "- Aplicas el **comportamiento en infinito** $\\lim_{s \\to \\infty} F(s) = 0$ para detectar errores."
        )),

        b("definicion",
          titulo="Funciones de orden exponencial",
          body_md=(
              "Una función $f : [0, \\infty) \\to \\mathbb{R}$ es de **orden exponencial $c$** si existen "
              "constantes $M > 0$, $T \\geq 0$ y $c \\in \\mathbb{R}$ tales que\n\n"
              "$$|f(t)| \\leq M\\, e^{c t} \\quad \\text{para todo } t \\geq T.$$\n\n"
              "Equivalentemente: $f$ no crece más rápido que algún exponencial.\n\n"
              "**Ejemplos:**\n\n"
              "- $f(t) = t^n$ es de orden exponencial **0** (orden polinomial $\\leq$ exponencial).\n"
              "- $f(t) = e^{a t}$ es de orden exponencial $a$.\n"
              "- $f(t) = \\sin(b t)$, $\\cos(b t)$ son de orden exponencial $0$ (acotados).\n"
              "- $f(t) = t^n e^{a t}$ es de orden exponencial $a$.\n\n"
              "**Contraejemplo (NO es de orden exponencial):** $f(t) = e^{t^2}$. Para todo $c$, "
              "$e^{t^2}/e^{c t} = e^{t^2 - c t} \\to \\infty$. Su transformada **no existe** para ningún $s$."
          )),

        b("definicion",
          titulo="Función continua por tramos",
          body_md=(
              "Una función $f : [0, \\infty) \\to \\mathbb{R}$ es **continua por tramos** (o seccionalmente "
              "continua) si en todo intervalo finito $[0, T]$:\n\n"
              "- Tiene a lo sumo un número **finito de discontinuidades**.\n"
              "- En cada discontinuidad, los **límites laterales existen y son finitos** (saltos finitos, no asíntotas).\n\n"
              "**Esto incluye:**\n\n"
              "- Funciones continuas (caso particular).\n"
              "- Funciones escalón (Heaviside).\n"
              "- Pulsos rectangulares.\n"
              "- Combinaciones por tramos de funciones suaves.\n\n"
              "**No incluye:** funciones con asíntotas verticales en intervalos finitos (p. ej. $1/t$ en $t = 0$)."
          )),

        b("definicion",
          titulo="Teorema de existencia",
          body_md=(
              "**Teorema (Existencia de la transformada).** Sea $f : [0, \\infty) \\to \\mathbb{R}$ tal que:\n\n"
              "1. $f$ es **continua por tramos** en cada intervalo finito $[0, T]$.\n"
              "2. $f$ es de **orden exponencial $c$**.\n\n"
              "Entonces la transformada $F(s) = \\mathcal{L}\\{f\\}(s)$ **existe** para todo $s > c$.\n\n"
              "**Demostración (idea).** $|e^{-s t} f(t)| \\leq M e^{-(s - c) t}$, y la integral $\\int_0^{\\infty} e^{-(s - c) t} dt = 1/(s - c)$ "
              "converge para $s > c$. Por comparación, la integral original también converge.\n\n"
              "**Hipótesis suficiente, no necesaria.** Hay funciones más generales con transformada (p. ej. "
              "la función delta de Dirac, que no es ni siquiera función). Pero para aplicaciones de EDOs, "
              "estas dos hipótesis cubren todo lo que importa."
          )),

        b("definicion",
          titulo="Comportamiento en infinito",
          body_md=(
              "**Proposición.** Si $f$ es continua por tramos y de orden exponencial, entonces\n\n"
              "$$\\lim_{s \\to \\infty} F(s) = 0.$$\n\n"
              "**Idea de la prueba.** $|F(s)| \\leq M / (s - c) \\to 0$ cuando $s \\to \\infty$.\n\n"
              "**Utilidad práctica:** si calculas una transformada que **no** tiende a 0 (por ejemplo, sale "
              "$F(s) = s^2$ o $F(s) = 1$), **es señal de error en el cálculo**. Toda transformada legítima "
              "se 'apaga' en infinito.\n\n"
              "**Más fuerte:** $F(s) \\to 0$ con velocidad al menos $1/s$. Por eso $F(s)$ debe ser una "
              "**función racional propia** (grado del numerador $<$ grado del denominador) cuando viene de "
              "una EDO con condiciones iniciales finitas."
          )),

        b("definicion",
          titulo="Teorema de unicidad de la inversa",
          body_md=(
              "**Teorema (Unicidad).** Si $f$ y $g$ son continuas en $[0, \\infty)$ y de orden exponencial, "
              "y $\\mathcal{L}\\{f\\} = \\mathcal{L}\\{g\\}$ en algún intervalo $(s_0, \\infty)$, entonces\n\n"
              "$$f(t) = g(t) \\quad \\text{para todo } t \\geq 0.$$\n\n"
              "**Versión más fuerte.** Si $f$ y $g$ son continuas por tramos, entonces $f = g$ excepto en "
              "los puntos de discontinuidad (un conjunto finito por intervalo).\n\n"
              "**Consecuencia operativa.** La inversa $\\mathcal{L}^{-1}\\{F\\}$ está **bien definida** "
              "(módulo discontinuidades aisladas). Si por algún método encontramos una $f$ que satisface "
              "$\\mathcal{L}\\{f\\} = F$, entonces **es** la inversa — no hay otra.\n\n"
              "**Importancia para EDOs.** Si transformamos una EDO + PVI a una ecuación algebraica, la "
              "resolvemos para $X(s)$ y la invertimos, la $x(t)$ resultante es **la única** solución del "
              "PVI. Coincide con la unicidad del teorema de E&U del Cap. 1."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar orden exponencial",
          problema_md="¿Es $f(t) = t^2 e^{3 t}$ de orden exponencial? Si sí, ¿con qué $c$?",
          pasos=[
              {"accion_md": (
                  "**Idea.** Comparar con $e^{c t}$ para $c$ ligeramente mayor que $3$. $\\dfrac{t^2 e^{3 t}}{e^{c t}} = t^2 e^{(3 - c) t}$.\n\n"
                  "Si $c > 3$, entonces $3 - c < 0$ y $t^2 e^{(3 - c) t} \\to 0$ cuando $t \\to \\infty$. Acotado para $t \\geq T$ adecuado."
              ),
               "justificacion_md": "Polinomio por exponencial decreciente tiende a 0.",
               "es_resultado": False},
              {"accion_md": (
                  "**Más útil:** podemos tomar directamente $c = 3$ (no hace falta estricto): $|t^2 e^{3 t}| / e^{3 t} = t^2$, "
                  "no acotado. Necesitamos $c > 3$ por un margen. **Cualquier $c > 3$** funciona."
              ),
               "justificacion_md": "Por convención, decimos que el orden exponencial **mínimo** es $3$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión:** $f$ es de orden exponencial $3$. Su transformada existe para $s > 3$."
              ),
               "justificacion_md": "$\\mathcal{L}\\{t^2 e^{3 t}\\} = 2 / (s - 3)^3$, válida para $s > 3$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Detectar transformada errónea",
          problema_md=(
              "Un estudiante calculó $\\mathcal{L}\\{f(t)\\} = \\dfrac{s^2 + 1}{s + 1}$. ¿Es válido?"
          ),
          pasos=[
              {"accion_md": (
                  "**Aplicar el criterio de comportamiento en infinito:** $\\lim_{s \\to \\infty} F(s) = ?$.\n\n"
                  "$\\dfrac{s^2 + 1}{s + 1} \\sim s \\to \\infty$ cuando $s \\to \\infty$."
              ),
               "justificacion_md": "Función racional impropia.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión:** **NO** puede ser una transformada de Laplace válida — debería tender a 0. Hay un error en el cálculo."
              ),
               "justificacion_md": "Toda $F(s)$ legítima de una función de orden exponencial es racional propia (o tiende a 0).",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué basta orden exponencial.** El factor $e^{-s t}$ en la integral 'amortigua' a $f$. "
            "Si $f$ no crece más rápido que $e^{c t}$, entonces $e^{-s t} f$ se controla por $e^{-(s - c) t}$ "
            "para $s > c$ — y esa exponencial decreciente garantiza convergencia.\n\n"
            "**Por qué la unicidad es no trivial.** En un instante $t_0$, $\\mathcal{L}\\{f\\}$ no usa solo "
            "$f(t_0)$ — integra todos los valores. Una pequeña diferencia entre $f$ y $g$ podría 'cancelarse' "
            "en la integral. El teorema dice que **no es así**: cualquier diferencia genera una $F$ "
            "diferente. La transformada captura toda la información de $f$.\n\n"
            "**Consecuencia: dos funciones continuas con la misma transformada son idénticas.** Esto es lo "
            "que justifica todo el método: una vez que conseguimos $X(s)$, **cualquier** función $x(t)$ "
            "que verifique $\\mathcal{L}\\{x\\} = X$ es la solución."
        )),

        fig(
            "Diagrama conceptual del teorema de existencia. "
            "A la izquierda, dos curvas en un eje (t, |f(t)|): una curva azul teal #06b6d4 (la función f) y otra curva ámbar #f59e0b discontinua (la cota M e^{ct}). "
            "La curva azul siempre por debajo de la curva ámbar para t grande. "
            "Anotación '|f(t)| ≤ M e^{ct} para t ≥ T'. "
            "Una flecha grande hacia la derecha etiquetada 'Transformada bien definida para s > c' lleva a "
            "una segunda gráfica con eje s y curva F(s) decreciente que tiende a 0 cuando s tiende a infinito. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$f(t) = e^{t^2}$ tiene transformada de Laplace para:",
                  "opciones_md": [
                      "$s > 0$",
                      "$s > 1$",
                      "**Ningún $s$**",
                      "Todo $s$",
                  ],
                  "correcta": "C",
                  "pista_md": "$e^{t^2}$ no es de orden exponencial.",
                  "explicacion_md": "Crece más rápido que cualquier $e^{c t}$, así la integral diverge para todo $s$.",
              },
              {
                  "enunciado_md": "Si $f, g$ son continuas y $\\mathcal{L}\\{f\\} = \\mathcal{L}\\{g\\}$, entonces:",
                  "opciones_md": [
                      "$f$ y $g$ pueden diferir en algunos puntos",
                      "**$f(t) = g(t)$ para todo $t \\geq 0$**",
                      "$f, g$ tienen la misma derivada",
                      "$f, g$ están acotadas igual",
                  ],
                  "correcta": "B",
                  "pista_md": "Teorema de unicidad para funciones continuas.",
                  "explicacion_md": "Sin discontinuidades, la unicidad es estricta.",
              },
              {
                  "enunciado_md": "Si $F(s) = (s + 1)/(s - 2)$, entonces:",
                  "opciones_md": [
                      "Es transformada de una función de orden exponencial 2",
                      "Su inversa existe en $s > 2$",
                      "**No puede ser transformada de una función de orden exponencial (no tiende a 0)**",
                      "Es transformada de $e^{2t}$",
                  ],
                  "correcta": "C",
                  "pista_md": "$\\lim_{s \\to \\infty} F = 1 \\neq 0$.",
                  "explicacion_md": "$F$ no tiende a 0 en infinito → no es transformada legítima.",
              },
          ]),

        ej(
            "Orden exponencial",
            "¿Qué orden exponencial mínimo tiene $f(t) = t^3 e^{-2 t} + \\cos(5 t)$?",
            ["Sumar dos partes; el orden es el máximo."],
            (
                "$t^3 e^{-2 t}$ es de orden $-2$ (en realidad acotado para $t$ grande). $\\cos(5 t)$ es de orden $0$. "
                "**Orden exponencial: $0$.** La transformada existe para $s > 0$."
            ),
        ),

        ej(
            "Detectar error",
            "Un cálculo dio $\\mathcal{L}\\{f\\} = s^3$. ¿Es plausible?",
            ["Comportamiento en infinito."],
            (
                "$s^3 \\to \\infty$ cuando $s \\to \\infty$. **No** puede ser transformada de Laplace de una función ordinaria. "
                "Hay un error de cálculo (o $f$ es una distribución como derivadas de la delta de Dirac, fuera del alcance del curso)."
            ),
        ),

        ej(
            "Unicidad aplicada",
            "Si $\\mathcal{L}\\{f\\} = \\mathcal{L}\\{2 e^{-t}\\}$ en $s > -1$, ¿quién es $f$?",
            ["Por unicidad..."],
            (
                "**$f(t) = 2 e^{-t}$.** No hay otra función continua de orden exponencial con la misma transformada."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que toda función tiene transformada de Laplace.** $e^{t^2}$ es un contraejemplo clásico.",
              "**No verificar el comportamiento $F \\to 0$ en infinito** al final del cálculo. Es el chequeo más rápido para detectar errores.",
              "**Confundir 'continua por tramos' con 'continua'.** La primera permite saltos finitos.",
              "**Pensar que la abscisa de convergencia es siempre $0$.** Para $e^{a t}$ con $a > 0$, la abscisa es $a > 0$.",
              "**Olvidar que la unicidad de la inversa puede tener excepciones en discontinuidades.** En la práctica esto no es problema: dos funciones que coinciden salvo en puntos aislados se consideran 'iguales' a efectos de la teoría.",
          ]),

        b("resumen",
          puntos_md=[
              "**Orden exponencial $c$:** $|f(t)| \\leq M e^{c t}$ para $t$ grande.",
              "**Continua por tramos:** finitas discontinuidades de salto finito.",
              "**Existencia:** estas dos hipótesis garantizan que $F(s)$ existe para $s > c$.",
              "**Comportamiento en infinito:** $F(s) \\to 0$ cuando $s \\to \\infty$. Útil para detectar errores.",
              "**Unicidad de la inversa:** dos funciones continuas con la misma transformada son iguales.",
              "**Próxima lección:** la propiedad estrella — transformada de derivadas y resolución de EDOs.",
          ]),
    ]
    return {
        "id": "lec-ed-4-2-existencia-unicidad",
        "title": "Existencia y unicidad",
        "description": "Condiciones que garantizan la existencia de la transformada de Laplace (orden exponencial, continuidad por tramos), comportamiento en infinito y unicidad de la transformada inversa.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 2,
    }


# =====================================================================
# Resolución de EDOs con Laplace
# =====================================================================
def lesson_edos_con_laplace():
    blocks = [
        b("texto", body_md=(
            "Llegamos a la **aplicación principal** de la transformada de Laplace: convertir una EDO con "
            "condiciones iniciales en una **ecuación algebraica** que se resuelve sin integrar.\n\n"
            "**El método.** Aplicar $\\mathcal{L}$ a ambos lados de la EDO. Las derivadas de $x(t)$ se "
            "vuelven multiplicaciones por $s$ con las condiciones iniciales **ya incorporadas**. Despejar "
            "$X(s)$ algebraicamente. Aplicar $\\mathcal{L}^{-1}$ para recuperar $x(t)$.\n\n"
            "$$\\boxed{\\;\\text{EDO} + \\text{PVI} \\xrightarrow{\\mathcal{L}} \\text{Álgebra en } s \\xrightarrow{\\mathcal{L}^{-1}} x(t)\\;}$$\n\n"
            "**Al terminar:**\n\n"
            "- Aplicas la fórmula $\\mathcal{L}\\{f^{(n)}\\} = s^n F(s) - s^{n - 1} f(0) - \\cdots - f^{(n - 1)}(0)$.\n"
            "- Resuelves PVIs lineales con coeficientes constantes de orden 1, 2 y superior.\n"
            "- Manejas la propiedad de **integral**: $\\mathcal{L}\\{\\int_0^t f\\} = F(s)/s$.\n"
            "- Reconoces cuándo conviene Laplace por sobre los métodos del Cap. 2."
        )),

        formulas(
            titulo="Transformada de derivadas",
            body=(
                "Para una función $f$ con la regularidad necesaria (continua, derivada continua por tramos, "
                "todas de orden exponencial), las transformadas de las derivadas son:\n\n"
                "$$\\mathcal{L}\\{f'(t)\\} = s F(s) - f(0).$$\n\n"
                "$$\\mathcal{L}\\{f''(t)\\} = s^2 F(s) - s f(0) - f'(0).$$\n\n"
                "$$\\mathcal{L}\\{f'''(t)\\} = s^3 F(s) - s^2 f(0) - s f'(0) - f''(0).$$\n\n"
                "**Fórmula general:**\n\n"
                "$$\\mathcal{L}\\{f^{(n)}(t)\\} = s^n F(s) - \\sum_{k = 0}^{n - 1} s^{n - 1 - k} f^{(k)}(0).$$\n\n"
                "**Tres puntos clave:**\n\n"
                "1. **Las condiciones iniciales aparecen explícitamente** — no hay que imponerlas al final.\n"
                "2. **Cada derivación en $t$ corresponde a multiplicación por $s$** menos términos de PVI.\n"
                "3. **El polinomio característico** $s^2 + p s + q$ aparece naturalmente al transformar la EDO."
            ),
        ),

        formulas(
            titulo="Transformada de integral",
            body=(
                "Si $f$ es continua por tramos y de orden exponencial, entonces\n\n"
                "$$\\mathcal{L}\\left\\{\\int_0^t f(\\tau)\\, d\\tau\\right\\} = \\dfrac{F(s)}{s}.$$\n\n"
                "**Interpretación dual a derivadas:** integrar en $t$ = dividir por $s$ en la transformada.\n\n"
                "**Aplicación práctica.** Inversión: $\\mathcal{L}^{-1}\\{F(s)/s\\} = \\int_0^t f(\\tau)\\, d\\tau$, "
                "que a menudo es más simple que descomponer en fracciones parciales.\n\n"
                "**Ejemplo:** $\\mathcal{L}^{-1}\\{1/(s(s^2 + 4))\\} = \\int_0^t \\sin(2 \\tau)/2\\, d\\tau = (1 - \\cos 2 t)/4$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="EDO de orden 2 con coeficientes constantes",
          problema_md="Resuelve $x'' + 3 x' + 2 x = 0$ con $x(0) = 1$, $x'(0) = 0$.",
          pasos=[
              {"accion_md": (
                  "**Aplicar $\\mathcal{L}$ a la EDO** (con $X = \\mathcal{L}\\{x\\}$):\n\n"
                  "$\\mathcal{L}\\{x''\\} = s^2 X - s \\cdot 1 - 0 = s^2 X - s$.\n\n"
                  "$\\mathcal{L}\\{x'\\} = s X - 1$.\n\n"
                  "$\\mathcal{L}\\{x\\} = X$.\n\n"
                  "Sustituyendo: $(s^2 X - s) + 3(s X - 1) + 2 X = 0$."
              ),
               "justificacion_md": "Las condiciones iniciales se inyectan al transformar las derivadas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Despejar $X$.** $X(s^2 + 3 s + 2) = s + 3$, así\n\n"
                  "$$X(s) = \\dfrac{s + 3}{s^2 + 3 s + 2} = \\dfrac{s + 3}{(s + 1)(s + 2)}.$$"
              ),
               "justificacion_md": "Notar el polinomio característico $s^2 + 3 s + 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Fracciones parciales.** $\\dfrac{s + 3}{(s + 1)(s + 2)} = \\dfrac{A}{s + 1} + \\dfrac{B}{s + 2}$. "
                  "Cobertura: $A = (-1 + 3)/(-1 + 2) = 2$, $B = (-2 + 3)/(-2 + 1) = -1$.\n\n"
                  "$X(s) = \\dfrac{2}{s + 1} - \\dfrac{1}{s + 2}$."
              ),
               "justificacion_md": "Método de cobertura (Heaviside).",
               "es_resultado": False},
              {"accion_md": (
                  "**Inversa por tabla:**\n\n"
                  "$$x(t) = 2 e^{-t} - e^{-2 t}.$$"
              ),
               "justificacion_md": "Inmediato. **Verificación:** $x(0) = 1$ ✓, $x'(0) = -2 + 2 = 0$ ✓.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="EDO no homogénea",
          problema_md="Resuelve $x'' + x = \\sin(2 t)$ con $x(0) = 0$, $x'(0) = 0$.",
          pasos=[
              {"accion_md": (
                  "**Transformar.** $s^2 X + X = \\dfrac{2}{s^2 + 4}$, es decir, $X (s^2 + 1) = \\dfrac{2}{s^2 + 4}$, así\n\n"
                  "$$X(s) = \\dfrac{2}{(s^2 + 1)(s^2 + 4)}.$$"
              ),
               "justificacion_md": "Condiciones iniciales nulas simplifican el lado izquierdo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Fracciones parciales.** $\\dfrac{2}{(s^2 + 1)(s^2 + 4)} = \\dfrac{A s + B}{s^2 + 1} + \\dfrac{C s + D}{s^2 + 4}$.\n\n"
                  "Multiplicando: $2 = (A s + B)(s^2 + 4) + (C s + D)(s^2 + 1)$. Igualando coeficientes:\n\n"
                  "$s^3$: $A + C = 0$. $s^2$: $B + D = 0$. $s^1$: $4 A + C = 0$. $s^0$: $4 B + D = 2$.\n\n"
                  "De $A + C = 0$ y $4 A + C = 0$: $3 A = 0 \\Rightarrow A = C = 0$.\n\n"
                  "De $B + D = 0$ y $4 B + D = 2$: $3 B = 2 \\Rightarrow B = 2/3$, $D = -2/3$."
              ),
               "justificacion_md": "Sistema $4 \\times 4$ que se resuelve por sustitución.",
               "es_resultado": False},
              {"accion_md": (
                  "$X(s) = \\dfrac{2/3}{s^2 + 1} - \\dfrac{2/3}{s^2 + 4} = \\dfrac{2}{3} \\cdot \\dfrac{1}{s^2 + 1} - \\dfrac{1}{3} \\cdot \\dfrac{2}{s^2 + 4}$.\n\n"
                  "**Inversa:** $x(t) = \\dfrac{2}{3} \\sin t - \\dfrac{1}{3} \\sin(2 t)$."
              ),
               "justificacion_md": "Notar que la solución particular y la complementaria salen 'mezcladas' — no hay paso separado.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="EDO de orden 1",
          problema_md="Resuelve $x' + 4 x = e^{-t}$ con $x(0) = 2$.",
          pasos=[
              {"accion_md": (
                  "**Transformar:** $s X - 2 + 4 X = \\dfrac{1}{s + 1}$, así $X (s + 4) = 2 + \\dfrac{1}{s + 1} = \\dfrac{2(s + 1) + 1}{s + 1} = \\dfrac{2 s + 3}{s + 1}$.\n\n"
                  "$X(s) = \\dfrac{2 s + 3}{(s + 1)(s + 4)}$."
              ),
               "justificacion_md": "EDO de orden 1: solo $f(0)$ aparece, no $f'(0)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Fracciones parciales:** $\\dfrac{2 s + 3}{(s + 1)(s + 4)} = \\dfrac{A}{s + 1} + \\dfrac{B}{s + 4}$. Cobertura: $A = 1/3$, $B = 5/3$.\n\n"
                  "$x(t) = \\dfrac{1}{3} e^{-t} + \\dfrac{5}{3} e^{-4 t}$."
              ),
               "justificacion_md": "Verificar: $x(0) = 1/3 + 5/3 = 2$ ✓.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Comparación con métodos del Cap. 2.** Para coeficientes constantes con forzantes 'tabla', "
            "Laplace es **equivalente** a coeficientes indeterminados — pero más mecánico. Las ventajas "
            "reales aparecen cuando:\n\n"
            "- **El forzante es discontinuo** (pulso, escalón) — Laplace lo maneja sin cambiar de estrategia. "
            "Coeficientes indeterminados requeriría resolver tramo por tramo y empalmar.\n"
            "- **El forzante incluye delta de Dirac** (impulsos) — Laplace lo trata como cualquier otro forzante. Otros métodos no lo manejan limpiamente.\n"
            "- **Hay sistemas acoplados** — Laplace los resuelve simultáneamente sin diagonalizar.\n"
            "- **La complejidad algebraica supera la complejidad analítica** — descomponer fracciones es más mecánico que adivinar formas particulares.\n\n"
            "**Limitación.** No siempre la inversa es fácil de calcular. Para $X(s)$ con denominador "
            "complicado (raíces irracionales, multiplicidades altas, irreducibles), el método puede volverse engorroso."
        )),

        fig(
            "Tabla visual de las propiedades clave para resolver EDOs con Laplace. "
            "Tres filas, cada una con dos columnas: 'Operación en t' (izquierda) y 'Operación en s' (derecha). "
            "Fila 1: 'f(t)' ↔ 'F(s)'. "
            "Fila 2: 'f'(t)' ↔ 's F(s) - f(0)'. "
            "Fila 3: 'f''(t)' ↔ 's² F(s) - s f(0) - f'(0)'. "
            "Fila 4: '∫₀ᵗ f(τ) dτ' ↔ 'F(s)/s'. "
            "Acentos teal #06b6d4 a la izquierda, ámbar #f59e0b a la derecha, flechas conectoras dobles. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\mathcal{L}\\{x'(t)\\} = $",
                  "opciones_md": [
                      "$X(s)$",
                      "$s X(s)$",
                      "**$s X(s) - x(0)$**",
                      "$X'(s)$",
                  ],
                  "correcta": "C",
                  "pista_md": "La condición inicial entra siempre.",
                  "explicacion_md": "Esa fórmula es la base del método.",
              },
              {
                  "enunciado_md": "$\\mathcal{L}\\{x''(t)\\} = $",
                  "opciones_md": [
                      "$s^2 X$",
                      "**$s^2 X - s\\, x(0) - x'(0)$**",
                      "$s^2 X - x(0) - s\\, x'(0)$",
                      "$s X - x(0)$",
                  ],
                  "correcta": "B",
                  "pista_md": "El coeficiente de $x(0)$ es la potencia más alta.",
                  "explicacion_md": "Cuidar el orden: $s$ acompaña a $x(0)$, no a $x'(0)$.",
              },
              {
                  "enunciado_md": "Aplicar $\\mathcal{L}$ a una EDO lineal con coeficientes constantes y PVI:",
                  "opciones_md": [
                      "Genera otra EDO equivalente",
                      "**Convierte el problema en una ecuación algebraica para $X(s)$**",
                      "Solo funciona si las CI son nulas",
                      "Requiere conocer la solución general previamente",
                  ],
                  "correcta": "B",
                  "pista_md": "Esa es la razón por la cual el método existe.",
                  "explicacion_md": "Las CI están incorporadas; despejar $X$ es álgebra elemental.",
              },
          ]),

        ej(
            "PVI orden 2 con sin",
            "Resuelve $x'' + 4 x = 0$ con $x(0) = 0$, $x'(0) = 3$.",
            ["$X = 3 / (s^2 + 4)$."],
            (
                "$s^2 X - 3 + 4 X = 0 \\Rightarrow X = 3/(s^2 + 4) = (3/2) \\cdot (2/(s^2 + 4))$. "
                "$x(t) = (3/2) \\sin(2 t)$."
            ),
        ),

        ej(
            "Orden 2 raíces complejas",
            "Resuelve $x'' + 6 x' + 25 x = 0$ con $x(0) = 1$, $x'(0) = 0$.",
            ["Completar cuadrados en $s^2 + 6 s + 25$."],
            (
                "$s^2 X - s + 6 (s X - 1) + 25 X = 0 \\Rightarrow X (s^2 + 6 s + 25) = s + 6 \\Rightarrow X = (s + 6)/(s^2 + 6 s + 25)$.\n\n"
                "$s^2 + 6 s + 25 = (s + 3)^2 + 16$. $X = ((s + 3) + 3)/((s + 3)^2 + 16) = (s + 3)/((s + 3)^2 + 16) + (3/4) \\cdot (4/((s + 3)^2 + 16))$.\n\n"
                "$x(t) = e^{-3 t}\\bigl(\\cos(4 t) + (3/4) \\sin(4 t)\\bigr)$."
            ),
        ),

        ej(
            "Inversión usando integral",
            "Calcula $\\mathcal{L}^{-1}\\{1/(s(s - 3))\\}$ usando la propiedad $\\mathcal{L}^{-1}\\{F/s\\} = \\int_0^t f$.",
            ["$1/(s - 3) \\to e^{3 t}$."],
            (
                "$\\mathcal{L}^{-1}\\{1/(s - 3)\\} = e^{3 t}$. Dividir por $s$ es integrar: $\\int_0^t e^{3 \\tau} d\\tau = (e^{3 t} - 1)/3$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar las condiciones iniciales** al transformar las derivadas. La fórmula $s X - x(0)$ siempre las incluye.",
              "**Confundir el coeficiente de $x(0)$ y $x'(0)$ en $\\mathcal{L}\\{x''\\}$.** Es $s x(0)$ y $x'(0)$ — el orden importa.",
              "**Resolver el problema completo a mano cuando solo se necesita $X(s)$.** Para problemas con discontinuidades, a veces basta el dominio $s$.",
              "**Equivocar la inversión por confundir factores.** Practicar fracciones parciales sistemáticamente.",
              "**Aplicar Laplace cuando la EDO no es lineal.** El método requiere linealidad.",
          ]),

        b("resumen",
          puntos_md=[
              "**Transformada de derivadas:** $\\mathcal{L}\\{f^{(n)}\\} = s^n F - \\sum_{k = 0}^{n - 1} s^{n - 1 - k} f^{(k)}(0)$.",
              "**Procedimiento:** transformar EDO + PVI → álgebra en $X(s)$ → invertir.",
              "**Las CI se incorporan automáticamente** en el paso de transformación.",
              "**Transformada de integral:** $\\mathcal{L}\\{\\int_0^t f\\} = F/s$. Útil para invertir.",
              "**Próxima lección:** propiedades operacionales para forzantes más complejos — traslaciones, escalones, convolución.",
          ]),
    ]
    return {
        "id": "lec-ed-4-3-edos-con-laplace",
        "title": "Resolución de EDOs con Laplace",
        "description": "Transformada de derivadas y aplicación al PVI: convertir una EDO lineal con condiciones iniciales en una ecuación algebraica para X(s), resolver y aplicar inversa. Transformada de la integral.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
    }


# =====================================================================
# Traslaciones y convolución
# =====================================================================
def lesson_traslaciones_convolucion():
    blocks = [
        b("texto", body_md=(
            "Esta lección reúne las **propiedades operacionales** que extienden el alcance de la "
            "transformada de Laplace más allá de las funciones de la tabla básica:\n\n"
            "1. **Traslación en el eje $s$** — multiplicar por $e^{a t}$ en $t$.\n"
            "2. **Traslación en el eje $t$** — la función escalón de Heaviside, forzantes que se 'encienden' tarde.\n"
            "3. **Convolución** — invertir productos de transformadas sin descomponer en fracciones parciales.\n\n"
            "Las tres propiedades son la clave para tratar **forzantes discontinuos**, **impulsos** y "
            "**inversiones complejas**.\n\n"
            "**Al terminar:**\n\n"
            "- Aplicas la primera traslación: $\\mathcal{L}\\{e^{a t} f(t)\\} = F(s - a)$.\n"
            "- Manejas la función escalón $u(t - a)$ y la segunda traslación: $\\mathcal{L}\\{u(t - a) f(t - a)\\} = e^{-a s} F(s)$.\n"
            "- Calculas convoluciones $(f * g)(t) = \\int_0^t f(\\tau) g(t - \\tau) d\\tau$.\n"
            "- Inviertes productos $F G$ vía $\\mathcal{L}^{-1}\\{F G\\} = f * g$."
        )),

        formulas(
            titulo="Primera traslación (eje $s$)",
            body=(
                "**Teorema.** Si $\\mathcal{L}\\{f(t)\\} = F(s)$, entonces\n\n"
                "$$\\boxed{\\,\\mathcal{L}\\{e^{a t} f(t)\\} = F(s - a).\\,}$$\n\n"
                "**Interpretación.** Multiplicar por $e^{a t}$ en $t$ = desplazar la transformada de $s$ a $s - a$.\n\n"
                "**Inversa correspondiente:**\n\n"
                "$$\\mathcal{L}^{-1}\\{F(s - a)\\} = e^{a t} f(t).$$\n\n"
                "**Demostración.** $\\mathcal{L}\\{e^{a t} f(t)\\} = \\int_0^{\\infty} e^{-s t} e^{a t} f(t) dt = \\int_0^{\\infty} e^{-(s - a) t} f(t) dt = F(s - a)$.\n\n"
                "**Aplicación clave.** Si una transformada $F$ se reconoce 'desplazada' (denominador con "
                "$(s - a)$ en vez de $s$), la inversa lleva un factor $e^{a t}$ multiplicando."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Aplicar primera traslación",
          problema_md="Calcula $\\mathcal{L}\\{t^4 e^{\\pi t}\\}$.",
          pasos=[
              {"accion_md": (
                  "**Identificar.** $f(t) = t^4$, $a = \\pi$. $F(s) = \\mathcal{L}\\{t^4\\} = 4!/s^5 = 24/s^5$."
              ),
               "justificacion_md": "Tabla básica para $t^n$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Trasladar:** $F(s - \\pi) = 24/(s - \\pi)^5$.\n\n"
                  "$$\\mathcal{L}\\{t^4 e^{\\pi t}\\} = \\dfrac{24}{(s - \\pi)^5}.$$"
              ),
               "justificacion_md": "Reemplazar $s$ por $s - a$ en toda la expresión.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inversa con denominador desplazado",
          problema_md="Calcula $\\mathcal{L}^{-1}\\left\\{\\dfrac{s + 3}{s^2 + 6 s + 25}\\right\\}$.",
          pasos=[
              {"accion_md": (
                  "**Completar cuadrados.** $s^2 + 6 s + 25 = (s + 3)^2 + 16$.\n\n"
                  "$\\dfrac{s + 3}{(s + 3)^2 + 16}$ se reconoce como $F(s - a)$ con $a = -3$ y $F(s) = s/(s^2 + 16) = \\mathcal{L}\\{\\cos 4 t\\}$."
              ),
               "justificacion_md": "Reconocer la forma trasladada.",
               "es_resultado": False},
              {"accion_md": (
                  "**Inversa:** $\\mathcal{L}^{-1}\\left\\{\\dfrac{s + 3}{(s + 3)^2 + 16}\\right\\} = e^{-3 t} \\cos(4 t)$."
              ),
               "justificacion_md": "Aparece típicamente en EDOs con raíces complejas $-3 \\pm 4 i$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Función escalón unitario",
          body_md=(
              "La **función escalón unitario** (o de Heaviside) se define por\n\n"
              "$$u(t - a) = \\begin{cases} 0 & \\text{si } t < a, \\\\ 1 & \\text{si } t \\geq a. \\end{cases}$$\n\n"
              "Modela un proceso que **se enciende en $t = a$**.\n\n"
              "**Su transformada:**\n\n"
              "$$\\mathcal{L}\\{u(t - a)\\} = \\dfrac{e^{-a s}}{s}, \\qquad a \\geq 0.$$\n\n"
              "**Pulso rectangular.** $u(t - a) - u(t - b) = 1$ en $[a, b)$ y $0$ fuera. Modela una señal "
              "encendida en $t = a$ y apagada en $t = b$.\n\n"
              "**Importancia.** El escalón permite **representar funciones por tramos en una sola fórmula**, "
              "lo que es indispensable para tratar forzantes discontinuos con Laplace."
          )),

        formulas(
            titulo="Segunda traslación (eje $t$)",
            body=(
                "**Teorema (segunda traslación).** Si $\\mathcal{L}\\{f(t)\\} = F(s)$ y $a > 0$, entonces\n\n"
                "$$\\boxed{\\,\\mathcal{L}\\{u(t - a)\\, f(t - a)\\} = e^{-a s}\\, F(s).\\,}$$\n\n"
                "**Interpretación.** Trasladar $f$ por $a$ y activarla con $u(t - a)$ = multiplicar la "
                "transformada por el factor $e^{-a s}$.\n\n"
                "**Atención.** El argumento de $f$ debe ser $t - a$ exactamente. Si tenemos $u(t - a)\\, f(t)$ "
                "(no $f(t - a)$), hay que reescribir: $u(t - a)\\, f(t) = u(t - a)\\, f((t - a) + a) = u(t - a)\\, g(t - a)$ "
                "con $g(\\tau) = f(\\tau + a)$, y entonces aplicar la fórmula con $G$ en vez de $F$.\n\n"
                "**Inversa:**\n\n"
                "$$\\mathcal{L}^{-1}\\{e^{-a s} F(s)\\} = u(t - a)\\, f(t - a).$$\n\n"
                "**Aplicación práctica.** Cuando una EDO tiene forzante con escalones, la transformada "
                "produce factores $e^{-a s}$ que la inversa convierte de nuevo en escalones desplazados."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Pulso rectangular",
          problema_md="Calcula la transformada del pulso $f(t) = u(t - 2) - u(t - 5)$.",
          pasos=[
              {"accion_md": (
                  "**Aplicar linealidad y la transformada del escalón.**\n\n"
                  "$\\mathcal{L}\\{u(t - 2)\\} = e^{-2 s}/s$, $\\mathcal{L}\\{u(t - 5)\\} = e^{-5 s}/s$.\n\n"
                  "$$\\mathcal{L}\\{f\\} = \\dfrac{e^{-2 s} - e^{-5 s}}{s}.$$"
              ),
               "justificacion_md": "El pulso es la diferencia de dos escalones.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Función trasladada con escalón",
          problema_md="Calcula $\\mathcal{L}\\{u(t - 1)\\,(t - 1)^2\\}$.",
          pasos=[
              {"accion_md": (
                  "**Aplicar la segunda traslación** con $a = 1$, $f(t) = t^2$, $F(s) = 2/s^3$.\n\n"
                  "$$\\mathcal{L}\\{u(t - 1)\\,(t - 1)^2\\} = e^{-s} \\cdot \\dfrac{2}{s^3} = \\dfrac{2 e^{-s}}{s^3}.$$"
              ),
               "justificacion_md": "El argumento $(t - 1)^2$ ya está en la forma correcta $f(t - a)$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Reescribir antes de aplicar",
          problema_md="Calcula $\\mathcal{L}\\{u(t - 2)\\, t^2\\}$.",
          pasos=[
              {"accion_md": (
                  "**Reescribir.** $t^2 = ((t - 2) + 2)^2 = (t - 2)^2 + 4(t - 2) + 4$. Así\n\n"
                  "$u(t - 2) t^2 = u(t - 2)\\bigl[(t - 2)^2 + 4 (t - 2) + 4\\bigr]$."
              ),
               "justificacion_md": "El argumento original no es $t - 2$, hay que ajustar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar transformada término por término** ($a = 2$):\n\n"
                  "$\\mathcal{L}\\{u(t - 2) (t - 2)^2\\} = e^{-2 s} \\cdot 2/s^3$.\n\n"
                  "$\\mathcal{L}\\{u(t - 2) (t - 2)\\} = e^{-2 s} \\cdot 1/s^2$.\n\n"
                  "$\\mathcal{L}\\{u(t - 2) \\cdot 1\\} = e^{-2 s}/s$.\n\n"
                  "**Sumar:** $\\mathcal{L}\\{u(t - 2) t^2\\} = e^{-2 s}\\bigl(2/s^3 + 4/s^2 + 4/s\\bigr)$."
              ),
               "justificacion_md": "Truco estándar: expandir potencias para que el argumento sea siempre $t - a$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Convolución",
          body_md=(
              "La **convolución** de dos funciones $f, g : [0, \\infty) \\to \\mathbb{R}$ es\n\n"
              "$$\\boxed{\\,(f * g)(t) = \\int_0^t f(\\tau)\\, g(t - \\tau)\\, d\\tau.\\,}$$\n\n"
              "**Propiedades:**\n\n"
              "- **Conmutativa:** $f * g = g * f$ (cambio de variable).\n"
              "- **Asociativa:** $(f * g) * h = f * (g * h)$.\n"
              "- **Distributiva:** $f * (g + h) = f * g + f * h$.\n"
              "- **Con la constante 1:** $(f * 1)(t) = \\int_0^t f(\\tau) d\\tau$ (integración).\n\n"
              "**Teorema de convolución (la propiedad estrella):**\n\n"
              "$$\\mathcal{L}\\{f * g\\} = F(s)\\, G(s).$$\n\n"
              "Equivalentemente, en su uso más común — **inversión de productos**:\n\n"
              "$$\\boxed{\\,\\mathcal{L}^{-1}\\{F(s)\\, G(s)\\} = (f * g)(t) = \\int_0^t f(\\tau)\\, g(t - \\tau)\\, d\\tau.\\,}$$\n\n"
              "**Consecuencia.** Si $X(s) = F(s)\\, G(s)$ con $F, G$ reconocibles, podemos invertir sin "
              "fracciones parciales — solo calculando la convolución."
          )),

        b("ejemplo_resuelto",
          titulo="Convolución de dos exponenciales",
          problema_md="Calcula $\\mathcal{L}^{-1}\\left\\{\\dfrac{1}{(s - 1)(s - 3)}\\right\\}$ por convolución.",
          pasos=[
              {"accion_md": (
                  "**Factorizar.** $F(s) = 1/(s - 1)$, $G(s) = 1/(s - 3)$.\n\n"
                  "$f(t) = e^t$, $g(t) = e^{3 t}$."
              ),
               "justificacion_md": "Cada factor se invierte por la tabla.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular la convolución** $(f * g)(t) = \\int_0^t e^{\\tau} e^{3(t - \\tau)} d\\tau = e^{3 t} \\int_0^t e^{-2 \\tau} d\\tau$.\n\n"
                  "$\\int_0^t e^{-2 \\tau} d\\tau = \\dfrac{1 - e^{-2 t}}{2}$.\n\n"
                  "$(f * g)(t) = e^{3 t} \\cdot \\dfrac{1 - e^{-2 t}}{2} = \\dfrac{e^{3 t} - e^t}{2}$."
              ),
               "justificacion_md": "Antiderivada elemental.",
               "es_resultado": False},
              {"accion_md": (
                  "**Resultado.** $\\mathcal{L}^{-1}\\left\\{\\dfrac{1}{(s - 1)(s - 3)}\\right\\} = \\dfrac{e^{3 t} - e^t}{2}$.\n\n"
                  "**Verificación con fracciones parciales:** $1/((s - 1)(s - 3)) = -1/(2(s - 1)) + 1/(2(s - 3)) \\to (-e^t + e^{3 t})/2$. ✓"
              ),
               "justificacion_md": "Ambos métodos dan lo mismo; convolución es alternativa cuando las fracciones parciales son tediosas.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Convolución de senos (inversión típica)",
          problema_md="Calcula $\\mathcal{L}^{-1}\\left\\{\\dfrac{1}{(s^2 + 1)^2}\\right\\}$.",
          pasos=[
              {"accion_md": (
                  "**Factorizar como producto.** $\\dfrac{1}{(s^2 + 1)^2} = \\dfrac{1}{s^2 + 1} \\cdot \\dfrac{1}{s^2 + 1}$.\n\n"
                  "$f(t) = g(t) = \\sin t$ (de la tabla, $\\mathcal{L}\\{\\sin t\\} = 1/(s^2 + 1)$)."
              ),
               "justificacion_md": "Producto de transformadas iguales.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular** $(\\sin * \\sin)(t) = \\int_0^t \\sin \\tau \\sin(t - \\tau)\\, d\\tau$.\n\n"
                  "Identidad: $\\sin A \\sin B = \\dfrac{1}{2}[\\cos(A - B) - \\cos(A + B)]$.\n\n"
                  "$\\sin \\tau \\sin(t - \\tau) = \\dfrac{1}{2}[\\cos(2 \\tau - t) - \\cos t]$."
              ),
               "justificacion_md": "Identidad trigonométrica para producto.",
               "es_resultado": False},
              {"accion_md": (
                  "**Integrar:** $\\int_0^t \\dfrac{1}{2}[\\cos(2 \\tau - t) - \\cos t]\\, d\\tau = \\dfrac{1}{2}\\left[\\dfrac{\\sin(2 \\tau - t)}{2} - \\tau \\cos t\\right]_0^t$.\n\n"
                  "$= \\dfrac{1}{2}\\left[\\dfrac{\\sin t - \\sin(-t)}{2} - t \\cos t\\right] = \\dfrac{1}{2}[\\sin t - t \\cos t]$.\n\n"
                  "**Resultado:** $\\mathcal{L}^{-1}\\{1/(s^2 + 1)^2\\} = \\dfrac{\\sin t - t \\cos t}{2}$."
              ),
               "justificacion_md": "Aparece naturalmente en problemas de **resonancia** (oscilador forzado a su frecuencia natural).",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué la convolución es 'la integral correcta'.** Físicamente, la convolución $(f * g)(t)$ "
            "modela cómo la **respuesta** $g$ del sistema acumula efectos de un **estímulo** $f$ a lo largo "
            "del tiempo. Por eso aparece en sistemas lineales invariantes en el tiempo (LTI): la salida es "
            "la convolución de la entrada con la respuesta al impulso del sistema.\n\n"
            "**Cuándo usar convolución vs. fracciones parciales.** Para inversión de productos $F\\, G$:\n\n"
            "- **Fracciones parciales:** sale fórmula explícita pero requiere álgebra; ideal cuando las "
            "raíces son simples y reales.\n"
            "- **Convolución:** sale como integral, a veces más sencilla que el álgebra; ideal cuando "
            "uno de los factores es complicado pero su inversa es conocida.\n\n"
            "**Convolución como producto en el dominio $s$.** El teorema dice que la transformada **convierte "
            "convolución en producto** — análogo a cómo el logaritmo convierte producto en suma. Ese "
            "diccionario es la base del uso de Laplace en teoría de sistemas."
        )),

        fig(
            "Diagrama que muestra una función f(t) y otra g(t) en un eje t, "
            "y la convolución (f*g)(t) producida por integración. "
            "Panel izquierdo: dos curvas f(τ) (en teal #06b6d4) y g(t-τ) (en ámbar #f59e0b, con τ como eje horizontal y t fijo). "
            "Área sombreada bajo el producto f(τ)g(t-τ) entre 0 y t. "
            "Flecha hacia la derecha etiquetada 'integrar' lleva al panel derecho. "
            "Panel derecho: la curva (f*g)(t) en color púrpura, con los valores correspondientes marcados. "
            "Anotación de la fórmula (f*g)(t) = ∫₀ᵗ f(τ) g(t-τ) dτ debajo. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\mathcal{L}\\{e^{2 t} \\cos(3 t)\\} = $",
                  "opciones_md": [
                      "$\\dfrac{s}{s^2 + 9} \\cdot e^{2 s}$",
                      "**$\\dfrac{s - 2}{(s - 2)^2 + 9}$**",
                      "$\\dfrac{s}{(s - 2)^2 + 9}$",
                      "$\\dfrac{s + 2}{s^2 + 9}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Primera traslación: $s \\to s - 2$.",
                  "explicacion_md": "$\\mathcal{L}\\{\\cos 3 t\\} = s/(s^2 + 9)$; reemplazar $s$ por $s - 2$.",
              },
              {
                  "enunciado_md": "$\\mathcal{L}\\{u(t - 3)\\} = $",
                  "opciones_md": [
                      "$\\dfrac{1}{s - 3}$",
                      "**$\\dfrac{e^{-3 s}}{s}$**",
                      "$\\dfrac{e^{3 s}}{s}$",
                      "$3/s$",
                  ],
                  "correcta": "B",
                  "pista_md": "Segunda traslación con $f \\equiv 1$ y $a = 3$.",
                  "explicacion_md": "$F(s) = 1/s$ y se multiplica por $e^{-3 s}$.",
              },
              {
                  "enunciado_md": "$\\mathcal{L}^{-1}\\{F(s) G(s)\\} = $",
                  "opciones_md": [
                      "$f(t) g(t)$",
                      "**$(f * g)(t)$**",
                      "$f(t) + g(t)$",
                      "$\\int F G ds$",
                  ],
                  "correcta": "B",
                  "pista_md": "Teorema de convolución.",
                  "explicacion_md": "Producto en $s$ ↔ convolución en $t$.",
              },
          ]),

        ej(
            "Primera traslación",
            "Calcula $\\mathcal{L}\\{e^{-2 t} \\sin(3 \\pi t)\\}$.",
            ["$F(s)$ para $\\sin(3 \\pi t)$ y trasladar."],
            (
                "$\\mathcal{L}\\{\\sin(3 \\pi t)\\} = 3 \\pi / (s^2 + 9 \\pi^2)$. Trasladar $s \\to s + 2$:\n\n"
                "$\\mathcal{L}\\{e^{-2 t} \\sin(3 \\pi t)\\} = \\dfrac{3 \\pi}{(s + 2)^2 + 9 \\pi^2}$."
            ),
        ),

        ej(
            "Segunda traslación inversa",
            "Calcula $\\mathcal{L}^{-1}\\left\\{\\dfrac{e^{-2 s}}{s - 3}\\right\\}$.",
            ["$F(s) = 1/(s - 3) \\to e^{3 t}$, $a = 2$."],
            (
                "$f(t - 2) = e^{3(t - 2)}$, así $\\mathcal{L}^{-1}\\{e^{-2 s}/(s - 3)\\} = u(t - 2)\\, e^{3(t - 2)}$."
            ),
        ),

        ej(
            "Convolución para invertir",
            "Calcula $\\mathcal{L}^{-1}\\left\\{\\dfrac{1}{s(s^2 + 4)}\\right\\}$ por convolución.",
            ["$1/s \\cdot 1/(s^2 + 4)$ → $1$ y $\\sin(2 t)/2$."],
            (
                "$f(t) = 1$, $g(t) = \\sin(2 t)/2$. $(f * g)(t) = \\int_0^t \\sin(2 \\tau)/2\\, d\\tau = (1 - \\cos 2 t)/4$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar la segunda traslación con argumento incorrecto.** $u(t - a) f(t)$ NO es lo mismo que $u(t - a) f(t - a)$.",
              "**Olvidar el factor $u(t - a)$ al invertir $e^{-a s} F(s)$.** El escalón es parte de la respuesta.",
              "**Confundir primera y segunda traslación.** Primera: $e^{a t} f(t) \\to F(s - a)$. Segunda: $u(t - a) f(t - a) \\to e^{-a s} F(s)$.",
              "**Calcular convolución con límites incorrectos.** Son siempre $0$ a $t$, no $-\\infty$ a $\\infty$.",
              "**No reconocer que el integrando $f(\\tau) g(t - \\tau)$ depende de $t$ (paramétricamente).** $t$ es fijo durante la integración en $\\tau$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Primera traslación:** $\\mathcal{L}\\{e^{a t} f(t)\\} = F(s - a)$.",
              "**Función escalón:** $u(t - a) = 1$ si $t \\geq a$, $0$ si $t < a$. $\\mathcal{L}\\{u(t - a)\\} = e^{-a s}/s$.",
              "**Segunda traslación:** $\\mathcal{L}\\{u(t - a) f(t - a)\\} = e^{-a s} F(s)$.",
              "**Convolución:** $(f * g)(t) = \\int_0^t f(\\tau) g(t - \\tau) d\\tau$. **Conmutativa, asociativa.**",
              "**Teorema de convolución:** $\\mathcal{L}\\{f * g\\} = F G$. Inversión: $\\mathcal{L}^{-1}\\{F G\\} = f * g$.",
              "**Próxima lección:** propiedades adicionales — multiplicación por $t^n$, integración de transformadas, funciones periódicas.",
          ]),
    ]
    return {
        "id": "lec-ed-4-4-traslaciones-convolucion",
        "title": "Traslaciones y convolución",
        "description": "Primera traslación (eje s, multiplicación por exponencial), segunda traslación (eje t, función escalón de Heaviside) y convolución con teorema y aplicaciones a inversión.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# =====================================================================
# Multiplicación por t y funciones periódicas
# =====================================================================
def lesson_t_y_periodicas():
    blocks = [
        b("texto", body_md=(
            "Tres propiedades adicionales completan el repertorio operacional de la transformada de "
            "Laplace:\n\n"
            "1. **Derivación de transformadas:** multiplicar por $t^n$ en $t$ ↔ derivar $n$ veces en $s$.\n"
            "2. **Integración de transformadas:** dividir por $t$ en $t$ ↔ integrar de $s$ a $\\infty$.\n"
            "3. **Funciones periódicas:** la transformada de una función periódica se calcula sobre **un solo período**.\n\n"
            "Estas propiedades son útiles para forzantes con factores $t$, para problemas con "
            "**coeficientes variables** (siguiente lección), y para señales **periódicas** (ondas cuadradas, "
            "diente de sierra, triangulares).\n\n"
            "**Al terminar:**\n\n"
            "- Aplicas $\\mathcal{L}\\{t^n f(t)\\} = (-1)^n F^{(n)}(s)$.\n"
            "- Aplicas $\\mathcal{L}\\{f(t)/t\\} = \\int_s^{\\infty} F(\\sigma)\\, d\\sigma$.\n"
            "- Calculas la transformada de una función periódica con la fórmula del 'período único'."
        )),

        formulas(
            titulo="Derivación de transformadas",
            body=(
                "**Teorema.** Si $\\mathcal{L}\\{f(t)\\} = F(s)$, entonces\n\n"
                "$$\\boxed{\\,\\mathcal{L}\\{t f(t)\\} = -F'(s).\\,}$$\n\n"
                "Más en general,\n\n"
                "$$\\mathcal{L}\\{t^n f(t)\\} = (-1)^n\\, \\dfrac{d^n F}{d s^n}(s).$$\n\n"
                "**Idea de la prueba.** Derivando bajo la integral: $F'(s) = \\int_0^{\\infty} (-t) e^{-s t} f(t) dt = -\\mathcal{L}\\{t f(t)\\}$. "
                "Iterando se obtiene la fórmula con $n$.\n\n"
                "**Interpretación.** Multiplicar por $t$ en $t$ = derivar (con signo) en $s$. **Es exactamente "
                "la propiedad opuesta** a 'derivar en $t$ = multiplicar por $s$'.\n\n"
                "**Aplicación clave.** Permite calcular transformadas de productos $t^n e^{a t}$, $t \\sin(b t)$, "
                "$t \\cos(b t)$, etc., sin volver a integrar."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Calcular $\\mathcal{L}\\{t \\sin(b t)\\}$",
          problema_md="Calcula $\\mathcal{L}\\{t \\sin(2 t)\\}$.",
          pasos=[
              {"accion_md": (
                  "**Identificar.** $f(t) = \\sin 2 t$, $F(s) = 2/(s^2 + 4)$.\n\n"
                  "**Derivar:** $F'(s) = -\\dfrac{2 \\cdot 2 s}{(s^2 + 4)^2} = -\\dfrac{4 s}{(s^2 + 4)^2}$."
              ),
               "justificacion_md": "Regla de la cadena para $1/(s^2 + 4)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar la propiedad:** $\\mathcal{L}\\{t \\sin 2 t\\} = -F'(s) = \\dfrac{4 s}{(s^2 + 4)^2}$."
              ),
               "justificacion_md": "Aparece en problemas de resonancia y vibraciones forzadas.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Multiplicación por $t^2$",
          problema_md="Calcula $\\mathcal{L}\\{t^2 e^{3 t}\\}$.",
          pasos=[
              {"accion_md": (
                  "**Vía 1 — derivación de la transformada.** $f = e^{3 t}$, $F = 1/(s - 3)$. $F'(s) = -1/(s - 3)^2$, $F''(s) = 2/(s - 3)^3$.\n\n"
                  "$\\mathcal{L}\\{t^2 e^{3 t}\\} = (-1)^2 F''(s) = 2/(s - 3)^3$."
              ),
               "justificacion_md": "Derivar dos veces respecto a $s$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Vía 2 — primera traslación + tabla.** $\\mathcal{L}\\{t^2\\} = 2/s^3$. Trasladar: $\\mathcal{L}\\{t^2 e^{3 t}\\} = 2/(s - 3)^3$. ✓"
              ),
               "justificacion_md": "Las dos vías coinciden — chequeo de consistencia.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Integración de transformadas",
            body=(
                "**Teorema.** Si $\\mathcal{L}\\{f(t)\\} = F(s)$ y $\\lim_{t \\to 0^+} f(t)/t$ existe (es finito), entonces\n\n"
                "$$\\boxed{\\,\\mathcal{L}\\left\\{\\dfrac{f(t)}{t}\\right\\} = \\int_s^{\\infty} F(\\sigma)\\, d\\sigma.\\,}$$\n\n"
                "**Interpretación.** Dividir por $t$ en $t$ = integrar de $s$ a $\\infty$ en $s$.\n\n"
                "**Ejemplo emblemático.** $f(t) = \\sin t$, $F(s) = 1/(s^2 + 1)$.\n\n"
                "$\\int_s^{\\infty} \\dfrac{1}{\\sigma^2 + 1}\\, d\\sigma = \\arctan(\\sigma)\\Big|_s^{\\infty} = \\dfrac{\\pi}{2} - \\arctan s$.\n\n"
                "Así\n\n"
                "$$\\mathcal{L}\\left\\{\\dfrac{\\sin t}{t}\\right\\} = \\dfrac{\\pi}{2} - \\arctan s = \\arctan\\dfrac{1}{s}.$$\n\n"
                "**Importante.** La condición $\\lim_{t \\to 0^+} f(t)/t < \\infty$ es necesaria. Por ejemplo, "
                "$1/t$ no satisface la condición y $\\mathcal{L}\\{1/t\\}$ no existe (la integral $\\int_0^{\\infty} e^{-s t}/t\\, dt$ diverge en $0$)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Función con $\\ln$ en la transformada",
          problema_md="Calcula $\\mathcal{L}\\left\\{\\dfrac{e^{2 t} - e^{-3 t}}{t}\\right\\}$.",
          pasos=[
              {"accion_md": (
                  "**Identificar.** $f(t) = e^{2 t} - e^{-3 t}$, $F(s) = \\dfrac{1}{s - 2} - \\dfrac{1}{s + 3}$. "
                  "Verificar el límite: $\\lim_{t \\to 0^+} (e^{2t} - e^{-3t})/t = 2 - (-3) = 5$ (por L'Hôpital). Existe finito ✓."
              ),
               "justificacion_md": "Pre-requisito para aplicar la propiedad.",
               "es_resultado": False},
              {"accion_md": (
                  "**Integrar:** $\\int_s^{\\infty} \\left(\\dfrac{1}{\\sigma - 2} - \\dfrac{1}{\\sigma + 3}\\right) d\\sigma = \\left[\\ln|\\sigma - 2| - \\ln|\\sigma + 3|\\right]_s^{\\infty}$.\n\n"
                  "Cuando $\\sigma \\to \\infty$, $\\ln|(\\sigma - 2)/(\\sigma + 3)| \\to \\ln 1 = 0$.\n\n"
                  "$= 0 - [\\ln|s - 2| - \\ln|s + 3|] = \\ln \\dfrac{s + 3}{s - 2}$."
              ),
               "justificacion_md": "Antiderivada $\\ln$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Resultado:** $\\mathcal{L}\\{(e^{2t} - e^{-3t})/t\\} = \\ln\\dfrac{s + 3}{s - 2}$."
              ),
               "justificacion_md": "Forma logarítmica típica cuando se aplica esta propiedad.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Funciones periódicas",
            body=(
                "Una función $f$ es **periódica de período $T > 0$** si $f(t + T) = f(t)$ para todo $t \\geq 0$.\n\n"
                "**Teorema.** Si $f$ es continua por tramos y periódica de período $T$, entonces\n\n"
                "$$\\boxed{\\,\\mathcal{L}\\{f(t)\\} = \\dfrac{1}{1 - e^{-s T}} \\int_0^T e^{-s t} f(t)\\, dt.\\,}$$\n\n"
                "**Idea.** Descomponer la integral $\\int_0^{\\infty}$ como suma de las integrales sobre los "
                "períodos $[0, T], [T, 2 T], \\ldots$ y usar la periodicidad. El factor $1/(1 - e^{-s T})$ "
                "es la suma geométrica $\\sum_{n = 0}^{\\infty} e^{-n s T}$.\n\n"
                "**Útil porque:** basta calcular **una integral sobre un solo período**, no la integral "
                "infinita.\n\n"
                "**Aplicaciones:** ondas cuadradas, dientes de sierra, ondas triangulares, rectificadas — "
                "todas las señales periódicas estándar de ingeniería."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Onda cuadrada",
          problema_md=(
              "Calcula la transformada de la función periódica con período $T = 2$ definida por\n\n"
              "$f(t) = 1$ si $0 \\leq t < 1$, $f(t) = 0$ si $1 \\leq t < 2$ (luego se repite)."
          ),
          pasos=[
              {"accion_md": (
                  "**Integrar sobre un período:**\n\n"
                  "$\\int_0^2 e^{-s t} f(t)\\, dt = \\int_0^1 e^{-s t}\\, dt + 0 = \\left[-\\dfrac{e^{-s t}}{s}\\right]_0^1 = \\dfrac{1 - e^{-s}}{s}$."
              ),
               "justificacion_md": "Usar la definición por tramos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar la fórmula:** $\\mathcal{L}\\{f\\} = \\dfrac{1}{1 - e^{-2 s}} \\cdot \\dfrac{1 - e^{-s}}{s}$.\n\n"
                  "**Simplificar:** $1 - e^{-2 s} = (1 - e^{-s})(1 + e^{-s})$, así\n\n"
                  "$\\mathcal{L}\\{f\\} = \\dfrac{1}{s(1 + e^{-s})}$."
              ),
               "justificacion_md": "Cancelación que aparece típicamente en ondas cuadradas.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué multiplicar por $t$ corresponde a derivar.** En $F(s) = \\int_0^{\\infty} e^{-s t} f(t) dt$, "
            "tratemos $s$ como parámetro y derivemos: $F'(s) = \\int_0^{\\infty} (-t) e^{-s t} f(t) dt = -\\mathcal{L}\\{t f\\}$. "
            "El operador 'multiplicar por $t$' es **dual** del operador 'derivar en $s$'. Es la cara "
            "complementaria de 'derivar en $t$ ↔ multiplicar por $s$'.\n\n"
            "**Por qué dividir por $t$ corresponde a integrar.** Es la inversa de la propiedad anterior — "
            "'invertir' la derivada da una integral.\n\n"
            "**Por qué la fórmula de funciones periódicas funciona.** La integral total se descompone en "
            "$T$, $2T$, $3T$, ..., y la periodicidad permite reescribir cada tramo en términos del primero, "
            "con un factor exponencial $e^{-n s T}$. La suma de la serie geométrica resultante es exactamente $1/(1 - e^{-s T})$."
        )),

        fig(
            "Onda cuadrada periódica de período T = 2 en un eje horizontal de 0 a 8. "
            "La función vale 1 en intervalos [0,1), [2,3), [4,5), [6,7) (rectángulos sólidos en color teal #06b6d4), "
            "y vale 0 en los intervalos intermedios. "
            "Líneas verticales punteadas marcando los saltos. Etiquetas 'T = 2' y 'amplitud = 1'. "
            "Debajo, la fórmula de transformada destacada: L{f} = 1/(s(1 + e^{-s})). " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\mathcal{L}\\{t \\cdot f(t)\\} = $",
                  "opciones_md": [
                      "$F(s)/s$",
                      "**$-F'(s)$**",
                      "$F'(s)$",
                      "$s F(s)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Derivar $F$ y cambiar signo.",
                  "explicacion_md": "Multiplicar por $t$ ↔ derivar y negar.",
              },
              {
                  "enunciado_md": "$\\mathcal{L}\\{\\sin t / t\\} = $",
                  "opciones_md": [
                      "$1/(s^2 + 1)$",
                      "$\\arctan s$",
                      "**$\\pi/2 - \\arctan s$**",
                      "$\\ln(s^2 + 1)$",
                  ],
                  "correcta": "C",
                  "pista_md": "Integrar $1/(\\sigma^2 + 1)$ de $s$ a $\\infty$.",
                  "explicacion_md": "Resultado emblemático que aparece en procesamiento de señales.",
              },
              {
                  "enunciado_md": "Para $f$ periódica de período $T$, la transformada se calcula:",
                  "opciones_md": [
                      "Integrando de $0$ a $\\infty$",
                      "**Integrando solo sobre un período y dividiendo por $1 - e^{-s T}$**",
                      "Multiplicando por $T$",
                      "Es siempre la misma para cualquier período",
                  ],
                  "correcta": "B",
                  "pista_md": "Fórmula del período único.",
                  "explicacion_md": "Aprovecha la periodicidad para evitar integrar infinitas veces.",
              },
          ]),

        ej(
            "Multiplicación por $t$ — coseno",
            "Calcula $\\mathcal{L}\\{t \\cos(3 t)\\}$.",
            ["$F(s) = s/(s^2 + 9)$ y derivar."],
            (
                "$F'(s) = \\dfrac{(s^2 + 9) - s \\cdot 2 s}{(s^2 + 9)^2} = \\dfrac{9 - s^2}{(s^2 + 9)^2}$.\n\n"
                "$\\mathcal{L}\\{t \\cos 3 t\\} = -F'(s) = \\dfrac{s^2 - 9}{(s^2 + 9)^2}$."
            ),
        ),

        ej(
            "Inversión usando $\\arctan$",
            "Calcula $\\mathcal{L}^{-1}\\{\\arctan(3/(s + 2))\\}$.",
            ["Derivar para encontrar la función original."],
            (
                "Si $F(s) = \\arctan(3/(s + 2))$, $F'(s) = -3/((s + 2)^2 + 9)$. Por la propiedad de derivación, $F'(s) = -\\mathcal{L}\\{t f(t)\\}$, así $\\mathcal{L}\\{t f(t)\\} = 3/((s + 2)^2 + 9) = \\mathcal{L}\\{e^{-2 t} \\sin 3 t\\}$.\n\n"
                "Por unicidad: $t f(t) = e^{-2 t} \\sin 3 t$, así $f(t) = e^{-2 t} \\sin(3 t)/t$."
            ),
        ),

        ej(
            "Transformada de onda triangular",
            "Una señal triangular tiene período $T = 2 \\pi$ y vale $|\\sin t|$ en $[0, 2\\pi)$. Calcula su transformada.",
            ["Integrar $|\\sin t|$ por tramos."],
            (
                "$\\int_0^{2 \\pi} e^{-s t} |\\sin t|\\, dt = \\int_0^{\\pi} e^{-s t} \\sin t\\, dt - \\int_{\\pi}^{2\\pi} e^{-s t} \\sin t\\, dt$ (cuidando signo).\n\n"
                "Cada integral usa $\\int e^{-s t} \\sin t\\, dt = -e^{-s t}(s \\sin t + \\cos t)/(s^2 + 1)$. Tras evaluación y simplificación:\n\n"
                "$\\mathcal{L}\\{|\\sin t|\\} = \\dfrac{1 + e^{-\\pi s}}{(s^2 + 1)(1 - e^{-2 \\pi s})} = \\dfrac{1}{(s^2 + 1)(1 - e^{-\\pi s})}$ tras simplificar."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el signo en la propiedad de derivación.** $\\mathcal{L}\\{t f\\} = -F'(s)$, **con menos**.",
              "**Aplicar 'integración de transformada' a $f/t$ cuando $f(t)/t$ no tiene límite finito en $0$.** Por ejemplo, $1/t$ no funciona.",
              "**Olvidar el factor $1/(1 - e^{-s T})$** en la fórmula de funciones periódicas.",
              "**Usar el período incorrecto** o no respetar la definición por tramos al integrar.",
              "**Confundir derivación de $F(s)$ con respecto a $s$ y derivación de $f(t)$ con respecto a $t$.** Son dos operaciones distintas en la teoría.",
          ]),

        b("resumen",
          puntos_md=[
              "**Multiplicación por $t^n$:** $\\mathcal{L}\\{t^n f\\} = (-1)^n F^{(n)}(s)$.",
              "**División por $t$:** $\\mathcal{L}\\{f/t\\} = \\int_s^{\\infty} F(\\sigma) d\\sigma$, requiere $\\lim_{t \\to 0^+} f/t$ finito.",
              "**Funciones periódicas:** $\\mathcal{L}\\{f\\} = \\dfrac{1}{1 - e^{-s T}} \\int_0^T e^{-s t} f(t) dt$.",
              "**Aplicaciones:** EDOs con coeficientes en $t$, problemas con factor $t$, señales periódicas.",
              "**Próxima lección (cierre del curso):** sistemas con Laplace y EDOs con coeficientes variables.",
          ]),
    ]
    return {
        "id": "lec-ed-4-5-derivacion-transformadas-periodicas",
        "title": "Multiplicación por t y funciones periódicas",
        "description": "Derivación de transformadas (multiplicación por t^n), integración de transformadas (división por t) y transformada de funciones periódicas con la fórmula del período único.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# Sistemas y ecuaciones con coeficientes variables
# =====================================================================
def lesson_sistemas_y_var():
    blocks = [
        b("texto", body_md=(
            "Cerramos el capítulo — y el curso — con dos aplicaciones avanzadas de la transformada de Laplace:\n\n"
            "1. **Sistemas de EDOs lineales acoplados.** Aplicar $\\mathcal{L}$ a cada ecuación y resolver el "
            "sistema algebraico resultante en $X_1(s), X_2(s), \\ldots$\n"
            "2. **Ecuaciones lineales con coeficientes variables** del tipo $t f(t)$. La propiedad de "
            "derivación en $s$ permite tratar coeficientes polinomiales que los métodos del Cap. 2 no abordan limpiamente.\n\n"
            "**Al terminar:**\n\n"
            "- Resuelves un sistema $\\mathbf{x}' = \\mathbf{A}\\mathbf{x} + \\mathbf{f}$ con condiciones iniciales aplicando $\\mathcal{L}$.\n"
            "- Tratas EDOs con coeficientes variables del tipo $t y'' + \\ldots$ usando $\\mathcal{L}\\{t y'\\} = -\\dfrac{d}{ds}(s Y - y(0))$, etc.\n"
            "- Obtienes, por ejemplo, soluciones tipo Bessel para algunas EDOs paramétricas."
        )),

        formulas(
            titulo="Sistemas con Laplace",
            body=(
                "Para un sistema lineal con coeficientes constantes\n\n"
                "$$\\mathbf{x}'(t) = \\mathbf{A}\\, \\mathbf{x}(t) + \\mathbf{f}(t), \\qquad \\mathbf{x}(0) = \\mathbf{x}_0,$$\n\n"
                "aplicar $\\mathcal{L}$ a cada componente da\n\n"
                "$$s\\, \\mathbf{X}(s) - \\mathbf{x}_0 = \\mathbf{A}\\, \\mathbf{X}(s) + \\mathbf{F}(s),$$\n\n"
                "donde $\\mathbf{X}(s) = (X_1(s), \\ldots, X_n(s))^T$ y $\\mathbf{F}(s) = \\mathcal{L}\\{\\mathbf{f}\\}$. Despejando:\n\n"
                "$$\\boxed{\\,(s \\mathbf{I} - \\mathbf{A})\\, \\mathbf{X}(s) = \\mathbf{x}_0 + \\mathbf{F}(s) \\;\\Longrightarrow\\; \\mathbf{X}(s) = (s \\mathbf{I} - \\mathbf{A})^{-1}(\\mathbf{x}_0 + \\mathbf{F}(s)).\\,}$$\n\n"
                "**Conexión con $e^{\\mathbf{A} t}$.** $(s \\mathbf{I} - \\mathbf{A})^{-1}$ es la transformada de "
                "la matriz exponencial: $\\mathcal{L}\\{e^{\\mathbf{A} t}\\} = (s \\mathbf{I} - \\mathbf{A})^{-1}$.\n\n"
                "**Procedimiento práctico:**\n\n"
                "1. Escribir cada componente como una ecuación escalar transformada.\n"
                "2. Resolver el sistema lineal en $X_1(s), \\ldots, X_n(s)$ (Cramer, eliminación o matricial).\n"
                "3. Invertir cada $X_i(s)$ por separado con tabla y fracciones parciales."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Sistema $2 \\times 2$ con Laplace",
          problema_md=(
              "Resuelve el sistema $x' = 2 x + y$, $y' = 6 x + 3 y$ con $x(0) = 1$, $y(0) = 0$ usando Laplace."
          ),
          pasos=[
              {"accion_md": (
                  "**Transformar cada ecuación:**\n\n"
                  "- $s X - 1 = 2 X + Y \\Rightarrow (s - 2) X - Y = 1$.\n"
                  "- $s Y - 0 = 6 X + 3 Y \\Rightarrow -6 X + (s - 3) Y = 0$."
              ),
               "justificacion_md": "Aplicar $\\mathcal{L}\\{x'\\} = s X - x(0)$ y $\\mathcal{L}\\{y'\\} = s Y - y(0)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sistema en $X, Y$:** \n\n"
                  "$\\begin{pmatrix} s - 2 & -1 \\\\ -6 & s - 3 \\end{pmatrix} \\begin{pmatrix} X \\\\ Y \\end{pmatrix} = \\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix}$.\n\n"
                  "Determinante: $(s - 2)(s - 3) - 6 = s^2 - 5 s = s(s - 5)$.\n\n"
                  "**Por Cramer:** $X = \\dfrac{(s - 3)}{s(s - 5)}$, $Y = \\dfrac{6}{s(s - 5)}$."
              ),
               "justificacion_md": "Sistema $2 \\times 2$ resoluble por Cramer o eliminación.",
               "es_resultado": False},
              {"accion_md": (
                  "**Fracciones parciales para $X$:** $\\dfrac{s - 3}{s(s - 5)} = \\dfrac{A}{s} + \\dfrac{B}{s - 5}$. Cobertura: $A = 3/5$, $B = 2/5$. Así $X = (3/5)/s + (2/5)/(s - 5)$.\n\n"
                  "**Para $Y$:** $\\dfrac{6}{s(s - 5)} = \\dfrac{6/(-5)}{s} + \\dfrac{6/5}{s - 5} = -\\dfrac{6/5}{s} + \\dfrac{6/5}{s - 5}$."
              ),
               "justificacion_md": "Los polos $s = 0, 5$ corresponden a los autovalores $0, 5$... ¡pero el sistema tiene $\\det \\mathbf{A} = 0$ en este caso! Veamos los autovalores: $\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = (2 - \\lambda)(3 - \\lambda) - 6 = \\lambda^2 - 5 \\lambda$, autovalores $\\lambda = 0, 5$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Inversa:**\n\n"
                  "$$x(t) = \\dfrac{3}{5} + \\dfrac{2}{5} e^{5 t}, \\qquad y(t) = -\\dfrac{6}{5} + \\dfrac{6}{5} e^{5 t}.$$"
              ),
               "justificacion_md": "Verificar: $x(0) = 3/5 + 2/5 = 1$ ✓, $y(0) = 0$ ✓.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="EDOs con coeficientes variables (tipo $t$)",
            body=(
                "Para una EDO con coeficientes lineales en $t$, la propiedad $\\mathcal{L}\\{t f(t)\\} = -F'(s)$ "
                "se aplica también a las derivadas de $y$. Las identidades clave son:\n\n"
                "$$\\mathcal{L}\\{t y(t)\\} = -Y'(s).$$\n\n"
                "$$\\mathcal{L}\\{t y'(t)\\} = -\\dfrac{d}{ds}[s Y(s) - y(0)] = -Y(s) - s Y'(s).$$\n\n"
                "$$\\mathcal{L}\\{t y''(t)\\} = -\\dfrac{d}{ds}[s^2 Y(s) - s y(0) - y'(0)] = -2 s Y(s) + y(0) - s^2 Y'(s).$$\n\n"
                "**Consecuencia.** Una EDO del tipo $t y'' + \\alpha y' + \\beta t y = 0$ se transforma en una "
                "**EDO de primer orden lineal en $Y(s)$** (no algebraica). Esa EDO en $s$ se resuelve por "
                "factor integrante; la solución se invierte para obtener $y(t)$.\n\n"
                "**Aplicaciones.** Ecuaciones de Bessel, Hermite, Laguerre — todas tienen versiones que "
                "ceden a esta técnica."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Ecuación de Bessel transformada",
          problema_md=(
              "Resuelve $t y'' + y' + t y = 0$ con $y(0) = 1$ (condición regularidad — $y'(0) = 0$ implícito)."
          ),
          pasos=[
              {"accion_md": (
                  "**Transformar.** Usando las identidades anteriores con $y(0) = 1$, $y'(0) = 0$:\n\n"
                  "- $\\mathcal{L}\\{t y''\\} = -2 s Y + 1 - s^2 Y'$.\n"
                  "- $\\mathcal{L}\\{y'\\} = s Y - 1$.\n"
                  "- $\\mathcal{L}\\{t y\\} = -Y'$.\n\n"
                  "Sumando: $(-2 s Y + 1 - s^2 Y') + (s Y - 1) + (-Y') = 0$.\n\n"
                  "Simplificando: $-Y'(s^2 + 1) - s Y = 0$, es decir, $\\dfrac{Y'}{Y} = -\\dfrac{s}{s^2 + 1}$."
              ),
               "justificacion_md": "EDO de primer orden lineal y separable en $Y(s)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Integrar:** $\\ln Y = -\\dfrac{1}{2}\\ln(s^2 + 1) + C$, así $Y(s) = \\dfrac{C}{\\sqrt{s^2 + 1}}$. "
                  "Determinar $C$ usando $\\lim_{s \\to \\infty} s Y(s) = y(0) = 1$ (teorema del valor inicial): "
                  "$\\lim s/\\sqrt{s^2 + 1} = 1$, así $C = 1$.\n\n"
                  "$$Y(s) = \\dfrac{1}{\\sqrt{s^2 + 1}}.$$"
              ),
               "justificacion_md": "Constante fijada por la condición inicial vía teorema del valor inicial.",
               "es_resultado": False},
              {"accion_md": (
                  "**Inversa.** $\\mathcal{L}^{-1}\\{1/\\sqrt{s^2 + 1}\\} = J_0(t)$, la **función de Bessel de primera especie de orden 0**.\n\n"
                  "$$y(t) = J_0(t).$$"
              ),
               "justificacion_md": "Resultado clásico (puede consultarse en tablas avanzadas). Coincide con la solución estándar de la ecuación de Bessel de orden 0.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Función delta de Dirac (mención)",
          body_md=(
              "La **delta de Dirac** $\\delta(t - a)$ es una 'función generalizada' (distribución) que modela "
              "un **impulso** instantáneo en $t = a$. Sus propiedades formales son:\n\n"
              "- $\\delta(t - a) = 0$ para $t \\neq a$.\n"
              "- $\\int_{-\\infty}^{\\infty} \\delta(t - a) dt = 1$.\n"
              "- $\\int_0^{\\infty} f(t) \\delta(t - a) dt = f(a)$ (propiedad de tamizado).\n\n"
              "**Su transformada:**\n\n"
              "$$\\mathcal{L}\\{\\delta(t - a)\\} = e^{-a s}, \\qquad \\mathcal{L}\\{\\delta(t)\\} = 1.$$\n\n"
              "**Aplicación.** Modela impulsos: golpes mecánicos, descargas eléctricas, impulsos de control. "
              "Una EDO con $\\delta$ como forzante se resuelve igual que cualquier otra: aplicar Laplace "
              "produce un término constante en $s$, y la inversa da la solución impulsiva.\n\n"
              "**Atención.** $\\delta$ no es función en sentido clásico — está fuera del marco de existencia "
              "estándar (no es de orden exponencial). Pero la maquinaria operacional de Laplace se extiende "
              "consistentemente."
          )),

        b("intuicion", body_md=(
            "**Cierre del capítulo y del curso.** Hemos recorrido cuatro grandes bloques:\n\n"
            "- **Cap. 1 — EDO de primer orden:** definiciones, métodos elementales (separables, lineales, "
            "exactas, sustituciones), modelado básico, estabilidad escalar.\n"
            "- **Cap. 2 — EDO de orden superior:** estructura del espacio de soluciones, coeficientes "
            "constantes, vibraciones mecánicas, métodos para problemas no homogéneos, Abel y reducción de orden.\n"
            "- **Cap. 3 — Sistemas:** formulación matricial, autovalores, matriz fundamental y exponencial, "
            "análisis cualitativo de equilibrios planares.\n"
            "- **Cap. 4 — Laplace:** transformada como herramienta operacional, inversión por tabla y "
            "fracciones parciales, propiedades operacionales (traslaciones, convolución, derivación), "
            "aplicaciones a sistemas y ecuaciones especiales.\n\n"
            "Estos cuatro capítulos cubren el contenido estándar de un curso universitario de Ecuaciones "
            "Diferenciales Ordinarias. **Donde sigue el viaje:** EDPs (calor, onda, Laplace), sistemas "
            "dinámicos no lineales, métodos numéricos, control, mecánica analítica."
        )),

        fig(
            "Mapa conceptual del curso completo de Ecuaciones Diferenciales. "
            "Cuatro cuadrantes en una malla 2x2: "
            "Cuadrante 1 (arriba izq): 'EDO de Primer Orden' con sub-temas (separables, lineales, exactas, modelos) en teal #06b6d4. "
            "Cuadrante 2 (arriba der): 'EDO de Orden Superior' con (homogénea, coef const, vibraciones, no homogénea) en ámbar #f59e0b. "
            "Cuadrante 3 (abajo izq): 'Sistemas de EDO' con (matricial, valores propios, matriz fundamental, estabilidad) en púrpura. "
            "Cuadrante 4 (abajo der): 'Transformada de Laplace' con (definición, EDOs, traslaciones, convolución, sistemas) en verde. "
            "Flechas sugiriendo dependencias entre cuadrantes (Cap 2 usa Cap 1, etc.). "
            "Título superior 'Ecuaciones Diferenciales — Mapa del curso'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para resolver un sistema lineal $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$ con Laplace, hay que invertir:",
                  "opciones_md": [
                      "$\\mathbf{A}$",
                      "**$s \\mathbf{I} - \\mathbf{A}$**",
                      "$\\mathbf{A} - s \\mathbf{I}$",
                      "$\\det \\mathbf{A}$",
                  ],
                  "correcta": "B",
                  "pista_md": "$(s \\mathbf{I} - \\mathbf{A}) \\mathbf{X} = \\mathbf{x}_0$.",
                  "explicacion_md": "Es la matriz característica evaluada en $s$.",
              },
              {
                  "enunciado_md": "$\\mathcal{L}\\{\\delta(t - 3)\\} = $",
                  "opciones_md": [
                      "$e^{3 s}$",
                      "**$e^{-3 s}$**",
                      "$1/s$",
                      "$\\delta(s)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Propiedad de tamizado.",
                  "explicacion_md": "$\\int_0^{\\infty} e^{-s t} \\delta(t - 3) dt = e^{-3 s}$.",
              },
              {
                  "enunciado_md": "Una EDO del tipo $t y'' + a y' + b y = 0$ con Laplace:",
                  "opciones_md": [
                      "Se vuelve algebraica en $Y(s)$",
                      "**Se vuelve EDO de primer orden en $Y(s)$**",
                      "No se puede tratar con Laplace",
                      "Se reduce a Bessel siempre",
                  ],
                  "correcta": "B",
                  "pista_md": "Multiplicación por $t$ se traduce en derivación de $Y$.",
                  "explicacion_md": "El factor $t$ introduce $Y'(s)$ en la transformada.",
              },
          ]),

        ej(
            "Sistema $2 \\times 2$",
            "Resuelve $x' = x + y$, $y' = -2 x + 4 y$ con $x(0) = 0$, $y(0) = 1$ usando Laplace.",
            ["Sistema en $X, Y$; resolver y aplicar fracciones parciales."],
            (
                "$(s - 1) X - Y = 0$, $2 X + (s - 4) Y = 1$. Resolver: determinante $(s - 1)(s - 4) + 2 = s^2 - 5 s + 6 = (s - 2)(s - 3)$.\n\n"
                "$X = \\dfrac{1}{(s - 2)(s - 3)}$, $Y = \\dfrac{s - 1}{(s - 2)(s - 3)}$.\n\n"
                "Fracciones parciales: $X = -1/(s - 2) + 1/(s - 3)$, $Y = -1/(s - 2) + 2/(s - 3)$.\n\n"
                "$x(t) = -e^{2 t} + e^{3 t}$, $y(t) = -e^{2 t} + 2 e^{3 t}$."
            ),
        ),

        ej(
            "EDO con $\\delta$",
            "Resuelve $x'' + x = \\delta(t - \\pi)$ con $x(0) = 0$, $x'(0) = 0$.",
            ["$\\mathcal{L}\\{\\delta(t - \\pi)\\} = e^{-\\pi s}$."],
            (
                "$(s^2 + 1) X = e^{-\\pi s}$, $X = e^{-\\pi s}/(s^2 + 1)$.\n\n"
                "Inversa con segunda traslación: $\\mathcal{L}^{-1}\\{1/(s^2 + 1)\\} = \\sin t$, así\n\n"
                "$x(t) = u(t - \\pi) \\sin(t - \\pi) = -u(t - \\pi) \\sin t$. "
                "Físicamente: oscilador en reposo recibe un golpe en $t = \\pi$ que lo hace oscilar a partir de ahí."
            ),
        ),

        ej(
            "EDO con coef variable simple",
            "Resuelve $t y' + y = 0$ con $y(1) = 1$ (no es PVI estándar; tomar como ejercicio formal con $y(0) \\to ?$).",
            ["$\\mathcal{L}\\{t y'\\} = -Y - s Y'$."],
            (
                "Suponiendo $y(0)$ (formalmente): $-Y - s Y' + Y = 0 \\Rightarrow s Y' = 0 \\Rightarrow Y = $ constante.\n\n"
                "**Observación.** La EDO original tiene singularidad en $t = 0$ y se resuelve directamente: $y' = -y/t$, separable, $y = C/t$. Con $y(1) = 1$: $y = 1/t$.\n\n"
                "Este ejemplo muestra que **no toda EDO con coeficientes variables se trata mejor con Laplace** — el método clásico de separables es más rápido cuando aplica."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar las condiciones iniciales** al transformar derivadas en sistemas. Cada $X_i$ tiene su propia $x_i(0)$.",
              "**Resolver el sistema en $X, Y$ ignorando que $\\det(s \\mathbf{I} - \\mathbf{A})$ debe ser no cero.** Si se anula para algún $s$, hay singularidades — los polos corresponden a autovalores.",
              "**Aplicar Laplace a EDOs no lineales.** El método requiere linealidad estricta.",
              "**Pensar que $\\delta$ es una función ordinaria** y querer evaluarla en un punto: $\\delta(3)$ no tiene sentido como número.",
              "**Confundir las identidades para $\\mathcal{L}\\{t y'\\}$ y $\\mathcal{L}\\{t y''\\}$.** Hay que derivar la transformada de la derivada con cuidado.",
          ]),

        b("resumen",
          puntos_md=[
              "**Sistemas con Laplace:** $(s \\mathbf{I} - \\mathbf{A}) \\mathbf{X}(s) = \\mathbf{x}_0 + \\mathbf{F}(s)$, resolver por Cramer o matricial.",
              "**Coeficientes variables tipo $t$:** $\\mathcal{L}\\{t y'\\} = -Y - s Y'$, $\\mathcal{L}\\{t y''\\} = -2 s Y + y(0) - s^2 Y'$.",
              "**Función delta:** $\\mathcal{L}\\{\\delta(t - a)\\} = e^{-a s}$. Modela impulsos.",
              "**Cierre del curso:** EDOs de primer orden + orden superior + sistemas + Laplace constituyen el núcleo estándar de un curso universitario de EDOs.",
              "**Próximos pasos sugeridos:** EDPs, sistemas dinámicos no lineales, métodos numéricos, teoría de control.",
          ]),
    ]
    return {
        "id": "lec-ed-4-6-sistemas-y-coef-variables",
        "title": "Sistemas y ecuaciones con coeficientes variables",
        "description": "Aplicación de la transformada de Laplace a sistemas de EDOs lineales y a EDOs con coeficientes lineales en t. Función delta de Dirac y modelado de impulsos. Cierre del curso completo.",
        "blocks": blocks,
        "duration_minutes": 60,
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

    chapter_id = "ch-ed-transformada-laplace"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Transformada de Laplace",
        "description": (
            "Transformada de Laplace e inversa, condiciones de existencia y unicidad, resolución de "
            "EDOs con condiciones iniciales, propiedades operacionales (traslaciones, convolución, "
            "derivación de transformadas, funciones periódicas) y aplicaciones a sistemas y EDOs con "
            "coeficientes variables."
        ),
        "order": 4,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_definicion_inversa,
        lesson_existencia_unicidad,
        lesson_edos_con_laplace,
        lesson_traslaciones_convolucion,
        lesson_t_y_periodicas,
        lesson_sistemas_y_var,
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
        f"✅ Capítulo 'Transformada de Laplace' listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
