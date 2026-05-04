"""
Seed del curso Introducción al Cálculo — Capítulo 1: Polinomios.
2 lecciones:
  1.1 Algoritmo de la división
  1.2 Teorema del factor y resto

ENFOQUE: introducción al álgebra polinomial como puerta de entrada al cálculo.
Énfasis en el paralelo con la división de números enteros, y conexión directa
con factorización y búsqueda de raíces (que son la base del análisis posterior
de funciones racionales y del Teorema Fundamental del Álgebra).

Crea el curso si no existe. Idempotente.
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


# =====================================================================
# 1.1 Algoritmo de la división
# =====================================================================
def lesson_1_1():
    blocks = [
        b("texto", body_md=(
            "Los **polinomios** son una de las familias de funciones más fundamentales del análisis "
            "matemático. Su estructura algebraica permite operar con ellos de manera análoga a los "
            "números enteros: suma, resta, multiplicación y —el foco de esta lección— **división**.\n\n"
            "El **Algoritmo de la División para polinomios** establece que, dados un dividendo y un "
            "divisor (ambos polinomios), siempre existen un **cociente** y un **resto** únicos, en "
            "perfecta analogía con la división entera. Este resultado es la puerta de entrada al "
            "Teorema del Resto, al Teorema del Factor y al estudio de raíces — herramientas "
            "indispensables para todo lo que viene en cálculo.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Recordar la **definición formal** de polinomio: grado, coeficiente principal y "
            "coeficiente constante.\n"
            "- Comprender las **propiedades del grado** bajo suma y producto.\n"
            "- Enunciar y aplicar el **Teorema del Algoritmo de la División**.\n"
            "- Ejecutar la **división larga** de polinomios obteniendo cociente y resto explícitamente."
        )),

        b("definicion",
          titulo="Polinomio de grado $n$",
          body_md=(
              "Un **polinomio de grado $n$** es una función de la forma\n\n"
              "$$P(x) = a_n x^n + a_{n-1} x^{n-1} + \\cdots + a_1 x + a_0,$$\n\n"
              "donde $n$ es un entero no negativo y $a_n \\neq 0$. Los números "
              "$a_0, a_1, \\ldots, a_n$ se denominan **coeficientes** del polinomio.\n\n"
              "- $a_0$ es el **coeficiente constante** (término independiente).\n"
              "- $a_n$ es el **coeficiente principal** (acompaña a la potencia mayor).\n\n"
              "**Notación $\\mathbb{K}[x]$:** denotamos por $\\mathbb{K}[x]$ al conjunto de **todos** "
              "los polinomios con coeficientes en el cuerpo $\\mathbb{K}$. En particular:\n\n"
              "- $\\mathbb{R}[x]$: polinomios con coeficientes reales.\n"
              "- $\\mathbb{Q}[x]$: polinomios con coeficientes racionales.\n\n"
              "**Observación.** La función constante $P(x) = 0$ también es un polinomio (el **polinomio "
              "cero**), pero por convención **no tiene grado asociado**."
          )),

        b("ejemplo_resuelto",
          titulo="Identificar grado y coeficientes",
          problema_md=(
              "Determine el grado, el coeficiente principal y el coeficiente constante de "
              "$P(x) = 7x^4 + x^3 - 3x^2 - 5$."
          ),
          pasos=[
              {"accion_md": (
                  "El polinomio está escrito en forma estándar (potencias decrecientes). El término "
                  "de mayor potencia es $7x^4$, por lo tanto $\\text{grad}(P) = 4$."
               ),
               "justificacion_md": "El grado es el mayor exponente con coeficiente no nulo.",
               "es_resultado": False},
              {"accion_md": (
                  "El coeficiente principal es $a_4 = 7$ (el que acompaña a $x^4$)."
               ),
               "justificacion_md": "Por definición, $a_n$ con $n = \\text{grad}(P)$.",
               "es_resultado": False},
              {"accion_md": (
                  "El coeficiente constante es $a_0 = -5$ (el término sin $x$).\n\n"
                  "**Resumen:** $\\text{grad}(P) = 4$, coef. principal $= 7$, coef. constante $= -5$."
               ),
               "justificacion_md": "El término independiente es siempre $a_0$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="¿Pertenece a $\\mathbb{Q}[x]$ o a $\\mathbb{R}[x]$?",
          problema_md=(
              "Sea $P(x) = 1 + x - x^3 + \\sqrt{2}\\, x^7$. Determine si $P \\in \\mathbb{Q}[x]$ o "
              "$P \\in \\mathbb{R}[x]$."
          ),
          pasos=[
              {"accion_md": (
                  "Para que $P \\in \\mathbb{Q}[x]$ **todos** sus coeficientes deben ser racionales. "
                  "El coeficiente de $x^7$ es $\\sqrt{2}$, que no es racional."
               ),
               "justificacion_md": "Basta un coeficiente no racional para descartar $\\mathbb{Q}[x]$.",
               "es_resultado": False},
              {"accion_md": (
                  "Por lo tanto $P \\notin \\mathbb{Q}[x]$. Sin embargo, $\\sqrt{2} \\in \\mathbb{R}$, "
                  "y todos los demás coeficientes ($1, 1, -1$) también son reales.\n\n"
                  "**Conclusión:** $P \\in \\mathbb{R}[x]$ pero $P \\notin \\mathbb{Q}[x]$."
               ),
               "justificacion_md": "$\\mathbb{Q}[x] \\subset \\mathbb{R}[x]$, pero la inclusión es estricta.",
               "es_resultado": True},
          ]),

        fig(
            "Diagrama anatómico de un polinomio. Mostrar P(x) = 7x^4 + x^3 - 3x^2 - 5 escrito grande "
            "y centrado en la imagen. Cada término con un callout (línea + etiqueta): "
            "(1) 7x^4 etiquetado como 'término líder' con flecha a 7 marcado 'coeficiente principal a_4 = 7' "
            "y flecha al exponente 4 marcado 'grado del polinomio'; "
            "(2) x^3 etiquetado 'a_3 = 1'; "
            "(3) -3x^2 etiquetado 'a_2 = -3'; "
            "(4) -5 etiquetado 'coeficiente constante a_0 = -5'. "
            "Notar a_1 = 0 (término ausente). " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Propiedades del grado.** Para todo $P, Q \\in \\mathbb{R}[x]$ no nulos:\n\n"
              "1. $\\text{grad}(P + Q) \\leq \\max\\{\\text{grad}(P),\\, \\text{grad}(Q)\\}$.\n"
              "2. $\\text{grad}(P \\cdot Q) = \\text{grad}(P) + \\text{grad}(Q)$.\n\n"
              "En (1) la **desigualdad puede ser estricta**: si los coeficientes principales de $P$ y "
              "$Q$ son opuestos, pueden cancelarse al sumar y reducir el grado del resultado.\n\n"
              "En (2) la **igualdad es estricta** porque en $\\mathbb{R}[x]$ el producto de coeficientes "
              "no nulos sigue siendo no nulo (los reales no tienen divisores de cero)."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar las propiedades del grado",
          problema_md=(
              "Sean $P(x) = 3 + x - x^2$ y $Q(x) = 5 + x^2$. Calcule $P + Q$ y $P \\cdot Q$, y "
              "verifique las propiedades del grado."
          ),
          pasos=[
              {"accion_md": (
                  "**Suma término a término:**\n\n"
                  "$$P(x) + Q(x) = (3 + x - x^2) + (5 + x^2) = 8 + x.$$\n\n"
                  "Notamos que $\\text{grad}(P) = 2$, $\\text{grad}(Q) = 2$, pero "
                  "$\\text{grad}(P+Q) = 1 < 2 = \\max\\{2, 2\\}$."
               ),
               "justificacion_md": "Los términos $-x^2$ y $+x^2$ se cancelaron, ilustrando la "
                                   "desigualdad estricta de la propiedad 1.",
               "es_resultado": False},
              {"accion_md": (
                  "**Producto distribuyendo:**\n\n"
                  "$$P(x) \\cdot Q(x) = (3 + x - x^2)(5 + x^2) = 15 + 3x^2 + 5x + x^3 - 5x^2 - x^4 "
                  "= 15 + 5x - 2x^2 + x^3 - x^4.$$"
               ),
               "justificacion_md": "Multiplicación distributiva término a término.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\text{grad}(P \\cdot Q) = 4 = 2 + 2 = \\text{grad}(P) + \\text{grad}(Q)$ ✓\n\n"
                  "Se cumple la igualdad de la propiedad 2."
               ),
               "justificacion_md": "El término líder $-x^4$ proviene del producto $(-x^2)(x^2)$ y no "
                                   "se cancela.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Despejar el grado de un factor",
          problema_md=(
              "Sean $P, Q$ y $D$ polinomios tales que $P(x) = D(x) \\cdot Q(x)$. Si "
              "$\\text{grad}(P) = 9$ y $\\text{grad}(D) = 3$, ¿cuál es el grado de $Q$?"
          ),
          pasos=[
              {"accion_md": (
                  "Por la propiedad 2:\n"
                  "$$\\text{grad}(P) = \\text{grad}(D) + \\text{grad}(Q).$$"
               ),
               "justificacion_md": "El grado de un producto es la suma de los grados.",
               "es_resultado": False},
              {"accion_md": (
                  "Despejando: $\\text{grad}(Q) = \\text{grad}(P) - \\text{grad}(D) = 9 - 3 = "
                  "\\boxed{6}.$"
               ),
               "justificacion_md": "Aritmética directa una vez aplicada la propiedad.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**El paralelo con los enteros.** La división de polinomios es **completamente análoga** "
            "a la división de números enteros. Recordá que al dividir $38$ entre $7$ obtenemos "
            "cociente $5$ y resto $3$:\n\n"
            "$$\\frac{38}{7} = 5 + \\frac{3}{7}, \\qquad \\text{es decir,} \\qquad 38 = 7 \\cdot 5 + 3,$$\n\n"
            "donde el resto $3$ satisface $0 \\leq 3 < 7$. Para polinomios tendremos un cociente $Q(x)$ "
            "y un resto $R(x)$ cuyo **grado es estrictamente menor que el del divisor** — la condición "
            "$0 \\leq 3 < 7$ se vuelve $\\text{grad}(R) < \\text{grad}(D)$."
        )),

        fig(
            "Comparación lado a lado entre división de enteros y división de polinomios. "
            "Lado izquierdo: división entera 38 ÷ 7 = 5 con resto 3, mostrada como expresión "
            "'38 = 7 · 5 + 3' con etiquetas: 38='dividendo', 7='divisor', 5='cociente', 3='resto'. "
            "Lado derecho: división polinomial 'P(x) = D(x) · Q(x) + R(x)' con las MISMAS etiquetas "
            "debajo: P(x)='dividendo', D(x)='divisor', Q(x)='cociente', R(x)='resto'. "
            "Una flecha curvada arriba conecta '0 ≤ 3 < 7' con 'grad(R) < grad(D)' enfatizando la analogía. "
            "Estilo limpio, dos columnas paralelas. " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Algoritmo de la División.** Si $P, D \\in \\mathbb{R}[x]$ con "
              "$\\text{grad}(P) \\geq \\text{grad}(D)$, entonces existen polinomios **únicos** "
              "$Q, R \\in \\mathbb{R}[x]$ tales que\n\n"
              "$$P(x) = D(x) \\cdot Q(x) + R(x),$$\n\n"
              "con $0 \\leq \\text{grad}(R) < \\text{grad}(D)$ o bien $R \\equiv 0$.\n\n"
              "Los polinomios $P(x)$ y $D(x)$ se denominan **dividendo** y **divisor**, "
              "respectivamente; $Q(x)$ es el **cociente** y $R(x)$ es el **resto** (o residuo).\n\n"
              "**Observación importante.** La condición $\\text{grad}(R) < \\text{grad}(D)$ garantiza "
              "la **unicidad** de la descomposición. Si el divisor es **lineal** ($\\text{grad}(D) = 1$), "
              "el resto es necesariamente una **constante** (o el polinomio cero)."
          )),

        b("ejemplo_resuelto",
          titulo="División por un polinomio lineal",
          problema_md=(
              "Divida $6x^2 - 26x + 12$ entre $x - 4$. Es decir, encuentre $Q(x)$ y $R(x)$ tales que\n\n"
              "$$6x^2 - 26x + 12 = (x - 4) \\cdot Q(x) + R(x).$$"
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1.** Dividimos el término líder del dividendo entre el del divisor:\n\n"
                  "$$\\frac{6x^2}{x} = 6x.$$\n\n"
                  "Este es el primer término del cociente."
               ),
               "justificacion_md": "Cada paso de la división larga elimina el término de mayor grado "
                                   "del dividendo actual.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2.** Multiplicamos $6x$ por $(x - 4)$ y restamos del dividendo:\n\n"
                  "$$6x^2 - 26x + 12 - 6x(x - 4) = 6x^2 - 26x + 12 - (6x^2 - 24x) = -2x + 12.$$"
               ),
               "justificacion_md": "El término $6x^2$ se cancela exactamente (era el objetivo).",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3.** Repetimos con el nuevo dividendo $-2x + 12$. El término líder es:\n\n"
                  "$$\\frac{-2x}{x} = -2.$$\n\n"
                  "Multiplicamos $-2 \\cdot (x - 4)$ y restamos:\n\n"
                  "$$-2x + 12 - (-2x + 8) = 4.$$"
               ),
               "justificacion_md": "Otra iteración del mismo procedimiento.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 4.** El resto es $R(x) = 4$, con $\\text{grad}(R) = 0 < 1 = \\text{grad}(D)$. "
                  "El proceso termina.\n\n"
                  "$$\\boxed{Q(x) = 6x - 2, \\quad R(x) = 4.}$$\n\n"
                  "**Verificación:** $(x-4)(6x-2) + 4 = 6x^2 - 2x - 24x + 8 + 4 = 6x^2 - 26x + 12$ ✓"
               ),
               "justificacion_md": "Siempre verificá multiplicando $D \\cdot Q + R$ — atrapa errores aritméticos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="División por un polinomio de grado mayor",
          problema_md=(
              "Sean $P(x) = 8x^4 + 6x^2 - 3x + 1$ y $D(x) = 2x^2 - x + 2$. Encuentre $Q(x)$ y $R(x)$ "
              "tales que $P(x) = D(x) \\cdot Q(x) + R(x)$."
          ),
          pasos=[
              {"accion_md": (
                  "Notamos que en $P(x)$ el término $x^3$ tiene coeficiente nulo. Conviene escribir "
                  "explícitamente $P(x) = 8x^4 + 0x^3 + 6x^2 - 3x + 1$ para llevar el proceso con cuidado."
               ),
               "justificacion_md": "Escribir términos ausentes con coeficiente $0$ evita errores de alineación.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 1.** $\\dfrac{8x^4}{2x^2} = 4x^2$. Multiplicamos y restamos:\n\n"
                  "$$8x^4 + 0x^3 + 6x^2 - 3x + 1 - 4x^2(2x^2 - x + 2) = 4x^3 - 2x^2 - 3x + 1.$$"
               ),
               "justificacion_md": "$4x^2 \\cdot (2x^2 - x + 2) = 8x^4 - 4x^3 + 8x^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2.** $\\dfrac{4x^3}{2x^2} = 2x$. Multiplicamos y restamos:\n\n"
                  "$$4x^3 - 2x^2 - 3x + 1 - 2x(2x^2 - x + 2) = -7x + 1.$$"
               ),
               "justificacion_md": "$2x \\cdot (2x^2 - x + 2) = 4x^3 - 2x^2 + 4x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3.** $\\text{grad}(-7x + 1) = 1 < 2 = \\text{grad}(D)$. El proceso termina.\n\n"
                  "$$\\boxed{Q(x) = 4x^2 + 2x, \\quad R(x) = -7x + 1.}$$\n\n"
                  "**Verificación:** $(2x^2 - x + 2)(4x^2 + 2x) + (-7x + 1) = 8x^4 + 6x^2 - 3x + 1$ ✓"
               ),
               "justificacion_md": "Siempre verificá el resultado.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Ejercicio integrador: análisis previo a la división",
          problema_md=(
              "Dados $P(x) = 3x^4 - 6x^3 + 3x^2 - x + 2$ y $D(x) = x^2 - 2x + 3$:\n\n"
              "- (a) Determine el grado del cociente $Q(x)$.\n"
              "- (b) Determine los posibles grados del resto $R(x)$.\n"
              "- (c) Calcule $Q(x)$ y $R(x)$ explícitamente."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Por la propiedad del grado del producto, si $P = D \\cdot Q + R$ con "
                  "$\\text{grad}(R) < \\text{grad}(D) = 2$, entonces el término dominante de $P$ "
                  "proviene de $D \\cdot Q$. Luego:\n\n"
                  "$$\\text{grad}(Q) = \\text{grad}(P) - \\text{grad}(D) = 4 - 2 = \\boxed{2}.$$"
               ),
               "justificacion_md": "El grado del cociente queda determinado **antes** de hacer la división.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Por el algoritmo, $\\text{grad}(R) < \\text{grad}(D) = 2$, o bien $R \\equiv 0$. "
                  "Los posibles grados son:\n\n"
                  "- $R \\equiv 0$ (sin grado).\n"
                  "- $\\text{grad}(R) = 0$ (constante no nula).\n"
                  "- $\\text{grad}(R) = 1$ (lineal)."
               ),
               "justificacion_md": "La condición de unicidad acota el grado del resto.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c) Paso 1.** $\\dfrac{3x^4}{x^2} = 3x^2$. Multiplicamos y restamos:\n\n"
                  "$$3x^4 - 6x^3 + 3x^2 - x + 2 - 3x^2(x^2 - 2x + 3) = -6x^2 - x + 2.$$"
               ),
               "justificacion_md": "$3x^2 \\cdot (x^2 - 2x + 3) = 3x^4 - 6x^3 + 9x^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2.** $\\dfrac{-6x^2}{x^2} = -6$. Multiplicamos y restamos:\n\n"
                  "$$-6x^2 - x + 2 - (-6)(x^2 - 2x + 3) = -13x + 20.$$"
               ),
               "justificacion_md": "$-6 \\cdot (x^2 - 2x + 3) = -6x^2 + 12x - 18$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3.** $\\text{grad}(-13x + 20) = 1 < 2$. El proceso concluye.\n\n"
                  "$$\\boxed{Q(x) = 3x^2 - 6, \\quad R(x) = -13x + 20.}$$\n\n"
                  "Coincide con la predicción de (a) y (b): $\\text{grad}(Q) = 2$ y $\\text{grad}(R) = 1$."
               ),
               "justificacion_md": "El análisis previo de grados sirve como sanity check del resultado final.",
               "es_resultado": True},
          ]),

        ej(
            "División larga con potencias ausentes",
            "Divida $P(x) = x^4 - 16$ entre $D(x) = x - 2$. Identifique $Q(x)$ y $R(x)$.",
            [
                "Antes de empezar, escribí $P(x)$ con todas las potencias, incluso las nulas: "
                "$x^4 + 0x^3 + 0x^2 + 0x - 16$.",
                "Aplicá el algoritmo paso a paso, dividiendo siempre el término líder actual entre $x$.",
                "Como el divisor es lineal, el resto debe ser una constante.",
            ],
            (
                "Escribimos $P(x) = x^4 + 0x^3 + 0x^2 + 0x - 16$ y aplicamos el algoritmo:\n\n"
                "- $x^4 / x = x^3$, resto parcial: $x^4 - x^3(x-2) = 2x^3 + 0x^2 + 0x - 16$.\n"
                "- $2x^3 / x = 2x^2$, resto parcial: $2x^3 - 2x^2(x-2) = 4x^2 + 0x - 16$.\n"
                "- $4x^2 / x = 4x$, resto parcial: $4x^2 - 4x(x-2) = 8x - 16$.\n"
                "- $8x / x = 8$, resto parcial: $8x - 16 - 8(x-2) = 0$.\n\n"
                "**Resultado:** $\\boxed{Q(x) = x^3 + 2x^2 + 4x + 8, \\quad R(x) = 0.}$\n\n"
                "Como $R = 0$, $(x-2)$ es **factor** de $x^4 - 16$. De hecho, $x^4 - 16 = (x-2)(x+2)(x^2+4)$ "
                "— anticipo del Teorema del Factor que veremos en la próxima lección."
            ),
        ),

        b("verificacion",
          intro_md="Verifica tu manejo del algoritmo de la división polinomial:",
          preguntas=[
              {"enunciado_md": "Al dividir $P(x) = 2x^3 + 5x - 7$ entre $D(x) = x^2 + 1$, ¿cuáles son los grados posibles del resto $R(x)$?",
               "opciones_md": [
                   "$\\text{grad}(R) = 0$ o $R \\equiv 0$ (solo constante)",
                   "$\\text{grad}(R) \\leq 1$ o $R \\equiv 0$",
                   "$\\text{grad}(R) = 2$",
                   "$\\text{grad}(R) \\leq 3$",
               ],
               "correcta": "B",
               "pista_md": "El algoritmo exige $\\text{grad}(R) < \\text{grad}(D)$.",
               "explicacion_md": "Como $\\text{grad}(D) = 2$, el resto puede ser cero, constante (grado 0) o lineal (grado 1)."},
              {"enunciado_md": "Si $P(x) = D(x) \\cdot Q(x) + R(x)$ con $\\text{grad}(P) = 7$ y $\\text{grad}(D) = 3$, ¿cuál es $\\text{grad}(Q)$?",
               "opciones_md": ["$3$", "$4$", "$7$", "$10$"],
               "correcta": "B",
               "pista_md": "El término líder de $P$ proviene de $D \\cdot Q$.",
               "explicacion_md": "$\\text{grad}(Q) = \\text{grad}(P) - \\text{grad}(D) = 7 - 3 = 4$."},
              {"enunciado_md": "Al dividir $x^4 - 1$ entre $x - 1$ usando división larga, ¿qué error es más común si saltás escribir las potencias ausentes?",
               "opciones_md": [
                   "El cociente queda con grado mayor",
                   "Los términos se desalinean y se calcula mal el resto",
                   "El resto siempre es positivo",
                   "No afecta al resultado",
               ],
               "correcta": "B",
               "pista_md": "Por eso conviene escribir $x^4 + 0x^3 + 0x^2 + 0x - 1$.",
               "explicacion_md": "Si no se escriben los $0x^3, 0x^2, 0x$, las restas se hacen contra términos equivocados y el resto sale mal."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Olvidar escribir las potencias ausentes con coeficiente $0$.** Si saltás un grado, "
              "los términos se desalinean y el resto sale mal.",
              "**Confundir el orden de la resta:** se resta $D \\cdot (\\text{término del cociente})$ "
              "del dividendo actual, no al revés.",
              "**Detener el algoritmo demasiado pronto:** seguí dividiendo mientras "
              "$\\text{grad}(\\text{resto parcial}) \\geq \\text{grad}(D)$.",
              "**Aplicar $\\text{grad}(P+Q) = \\max\\{\\text{grad}(P), \\text{grad}(Q)\\}$ como "
              "igualdad** — solo es desigualdad ($\\leq$). Pueden cancelarse términos líder.",
              "**Decir que el polinomio cero tiene grado $0$.** Por convención **no tiene grado** "
              "— grado $0$ está reservado para constantes no nulas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Polinomio de grado $n$:** $P(x) = a_n x^n + \\cdots + a_0$ con $a_n \\neq 0$. "
              "Coef. principal $a_n$, coef. constante $a_0$.",
              "**$\\mathbb{K}[x]$:** polinomios con coeficientes en el cuerpo $\\mathbb{K}$ "
              "(habitualmente $\\mathbb{R}$ o $\\mathbb{Q}$).",
              "**Grado de la suma:** $\\text{grad}(P+Q) \\leq \\max\\{\\text{grad}(P), \\text{grad}(Q)\\}$ "
              "(puede ser estricta).",
              "**Grado del producto:** $\\text{grad}(P \\cdot Q) = \\text{grad}(P) + \\text{grad}(Q)$ "
              "(igualdad estricta en $\\mathbb{R}[x]$).",
              "**Algoritmo de la División:** $P = D \\cdot Q + R$ con $\\text{grad}(R) < \\text{grad}(D)$ "
              "o $R \\equiv 0$. Existencia + unicidad.",
              "**División larga:** dividir el término líder actual entre el del divisor, multiplicar y restar — repetir.",
              "**Próxima lección:** Teorema del Resto y Teorema del Factor — atajos potentes cuando el "
              "divisor es lineal $x - c$.",
          ]),
    ]
    return {
        "id": "lec-ic-1-1-algoritmo-division",
        "title": "Algoritmo de la división",
        "description": "Definición de polinomio, propiedades del grado, y el algoritmo de la división larga con cociente y resto únicos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 1.2 Teorema del factor y resto
# =====================================================================
def lesson_1_2():
    blocks = [
        b("texto", body_md=(
            "En esta lección estudiaremos dos resultados centrales: el **Teorema del Resto** y el "
            "**Teorema del Factor**. Ambos permiten determinar el resto de una división polinomial y "
            "factorizar polinomios de manera **eficiente**, sin necesidad de ejecutar el algoritmo de "
            "la división completo en todos los casos.\n\n"
            "Sus aplicaciones son directas: resolver ecuaciones polinomiales, factorizar completamente, "
            "y analizar el comportamiento de funciones algebraicas — temas que serán recurrentes a lo "
            "largo del curso de cálculo.\n\n"
            "**Objetivos:**\n\n"
            "- Aplicar el **Teorema del Resto** para calcular el resto sin hacer la división.\n"
            "- Ejecutar la **División Sintética** como atajo para divisores lineales $x - c$.\n"
            "- Enunciar y usar el **Teorema del Factor** para factorizar polinomios.\n"
            "- Identificar **ceros** de un polinomio y relacionarlos con sus factores lineales.\n"
            "- Aplicar las **fórmulas especiales** de factorización: diferencia de cuadrados, "
            "cuadrados perfectos, diferencia y suma de cubos."
        )),

        b("intuicion", body_md=(
            "**De dónde sale el Teorema del Resto.** Cuando dividimos $P(x)$ por un divisor lineal "
            "$x - c$, el algoritmo garantiza\n\n"
            "$$P(x) = (x - c)\\, Q(x) + R,$$\n\n"
            "donde el resto $R$ es una **constante** (porque $\\text{grad}(R) < \\text{grad}(x-c) = 1$). "
            "**Evaluando en $x = c$** se obtiene inmediatamente:\n\n"
            "$$P(c) = (c - c)\\, Q(c) + R = 0 + R = R.$$\n\n"
            "Es decir: **el resto es simplemente $P(c)$**. Este es el contenido del próximo teorema."
        )),

        b("teorema",
          enunciado_md=(
              "**Teorema del Resto.** Si el polinomio $P(x)$ se divide por $x - c$, entonces el "
              "resto es exactamente $R = P(c)$.\n\n"
              "En palabras: no es necesario ejecutar el algoritmo completo; basta con **evaluar el "
              "polinomio en $x = c$** para conocer el resto."
          )),

        fig(
            "Visualización del Teorema del Factor sobre una gráfica. Dibujar la curva del polinomio "
            "P(x) = x^3 - 7x + 6 en un sistema cartesiano con ejes etiquetados. La curva debe cruzar "
            "el eje x en exactamente tres puntos: x = -3, x = 1, x = 2 (estos son los ceros). "
            "Marcar cada cruce con un punto teal y etiquetarlo: '(-3, 0): cero c = -3', "
            "'(1, 0): cero c = 1', '(2, 0): cero c = 2'. "
            "Debajo del gráfico mostrar la factorización: P(x) = (x+3)(x-1)(x-2), "
            "con cada factor lineal conectado por una flecha al cero correspondiente. "
            "Título arriba: 'Teorema del Factor: cada cero c produce un factor (x - c)'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Comparar división larga vs. Teorema del Resto",
          problema_md=(
              "Dado $P(x) = 5x^3 - 8x^2 - x + 7$:\n\n"
              "- (a) Use el algoritmo de la división para hallar el resto al dividir $P(x)$ entre $x - 2$.\n"
              "- (b) Use el Teorema del Resto para hacerlo en un solo paso."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Aplicamos el algoritmo. $5x^3 / x = 5x^2$. Restamos:\n\n"
                  "$$5x^3 - 8x^2 - 5x^2(x-2) = 2x^2 - x + 7.$$\n\n"
                  "$2x^2 / x = 2x$. Restamos: $2x^2 - x - 2x(x-2) = 3x + 7$.\n\n"
                  "$3x / x = 3$. Restamos: $3x + 7 - 3(x-2) = 13$.\n\n"
                  "**Resto $= 13$**, $Q(x) = 5x^2 + 2x + 3$. Es decir, $P(x) = (x-2)(5x^2 + 2x + 3) + 13$."
               ),
               "justificacion_md": "División larga estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Por el Teorema del Resto, $R = P(2)$:\n\n"
                  "$$P(2) = 5(2)^3 - 8(2)^2 - 2 + 7 = 40 - 32 - 2 + 7 = \\boxed{13}.$$\n\n"
                  "Mismo resultado en una sola línea."
               ),
               "justificacion_md": "Evaluar es muchísimo más rápido que dividir, sobre todo si solo "
                                   "necesitás el resto.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cuándo el Teorema del Resto brilla: exponentes grandes",
          problema_md=(
              "Calcule el resto al dividir $P(x) = 2x^{2021} - 5x^{2020} + 3x + 2$ entre $x + 1$."
          ),
          pasos=[
              {"accion_md": (
                  "Reescribimos $x + 1 = x - (-1)$, así $c = -1$. Por el Teorema del Resto:\n\n"
                  "$$R = P(-1) = 2(-1)^{2021} - 5(-1)^{2020} + 3(-1) + 2.$$"
               ),
               "justificacion_md": "Cuidado con el signo: $x + a = x - (-a)$.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $2021$ es impar y $2020$ es par: $(-1)^{2021} = -1$, $(-1)^{2020} = 1$. Entonces:\n\n"
                  "$$R = 2(-1) - 5(1) - 3 + 2 = -2 - 5 - 3 + 2 = \\boxed{-8}.$$\n\n"
                  "Hacer la división larga con un polinomio de grado $2021$ sería impracticable. El "
                  "Teorema del Resto lo resuelve en segundos."
               ),
               "justificacion_md": "El Teorema del Resto es **especialmente útil cuando los "
                                   "exponentes son enormes**.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="División sintética",
          body_md=(
              "La **división sintética** es un algoritmo abreviado para dividir $P(x)$ por un divisor "
              "**lineal** de la forma $x - c$, operando solo sobre los coeficientes.\n\n"
              "**Condición de uso:** solo se aplica con divisores $x - c$ (coeficiente líder $1$). Si "
              "el divisor fuera, por ejemplo, $2x - 3$, habría que reescribirlo como "
              "$2\\bigl(x - \\tfrac{3}{2}\\bigr)$ y ajustar el cociente al final.\n\n"
              "**Algoritmo.** Sea $P(x) = a_n x^n + a_{n-1} x^{n-1} + \\cdots + a_0$ y divisor $x - c$:\n\n"
              "1. Escribir en una fila los **coeficientes** de $P(x)$ en orden decreciente, incluyendo "
              "$0$ por cada potencia ausente: $a_n, a_{n-1}, \\ldots, a_0$.\n"
              "2. Escribir el valor $c$ a la izquierda.\n"
              "3. Bajar el primer coeficiente $a_n$ a la fila del resultado.\n"
              "4. Multiplicar ese valor por $c$ y escribirlo bajo el siguiente coeficiente.\n"
              "5. Sumar la columna y escribir el resultado en la fila del resultado.\n"
              "6. Repetir 4–5 hasta procesar todos los coeficientes.\n"
              "7. El **último número** es el **resto $R$**. Los demás son los coeficientes del "
              "**cociente $Q(x)$**, que tiene grado $n - 1$."
          )),

        fig(
            "Diagrama paso a paso de división sintética para P(x) = 5x³ - 8x² - x + 7 entre x - 2. "
            "Mostrar la tabla en formato visual: en la primera fila el divisor c = 2 a la izquierda, "
            "luego los coeficientes 5, -8, -1, 7. Segunda fila vacía a la izquierda, luego flechas curvas "
            "ámbar mostrando el flujo: (1) baja el 5, (2) 5×2=10 va arriba bajo el -8, (3) -8+10=2, "
            "(4) 2×2=4 va arriba bajo el -1, (5) -1+4=3, (6) 3×2=6 va arriba bajo el 7, (7) 7+6=13. "
            "Última fila resaltada: 5, 2, 3 | 13 con etiqueta 'cociente | resto'. "
            "Cada flecha numerada (1)-(7) indicando el orden. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="División sintética con divisor $x - 2$",
          problema_md=(
              "Use división sintética para dividir $P(x) = 5x^3 - 8x^2 - x + 7$ por $x - 2$."
          ),
          pasos=[
              {"accion_md": (
                  "Divisor $x - 2 \\Rightarrow c = 2$. Coeficientes de $P(x)$: $5, -8, -1, 7$.\n\n"
                  "Construimos la tabla:\n\n"
                  "| $c$ | $a_3$ | $a_2$ | $a_1$ | $a_0$ |\n"
                  "|:---:|:---:|:---:|:---:|:---:|\n"
                  "| $2$ | $5$ | $-8$ | $-1$ | $7$ |\n"
                  "|   |   | $10$ | $4$ | $6$ |\n"
                  "| **resultado** | $\\mathbf{5}$ | $\\mathbf{2}$ | $\\mathbf{3}$ | $\\mathbf{13}$ |"
               ),
               "justificacion_md": "Cada columna se suma; el producto $c \\cdot \\text{(suma anterior)}$ "
                                   "se escribe en la fila intermedia de la columna siguiente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso a paso:** bajamos el $5$. Luego $5 \\cdot 2 = 10$; $-8 + 10 = 2$. Luego "
                  "$2 \\cdot 2 = 4$; $-1 + 4 = 3$. Luego $3 \\cdot 2 = 6$; $7 + 6 = 13$.\n\n"
                  "Los coeficientes del cociente son $5, 2, 3$ (grado $2$) y el resto es $13$."
               ),
               "justificacion_md": "Cada paso multiplica por $c$ y suma.",
               "es_resultado": False},
              {"accion_md": (
                  "**Resultado:**\n\n"
                  "$$\\boxed{Q(x) = 5x^2 + 2x + 3, \\quad R = 13.}$$\n\n"
                  "Es decir, $P(x) = (x - 2)(5x^2 + 2x + 3) + 13$. **Mismo resultado** que la división "
                  "larga del ejemplo anterior, pero en mucho menos espacio."
               ),
               "justificacion_md": "La división sintética es solo una contabilidad eficiente del "
                                   "algoritmo largo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="División sintética con potencia ausente y divisor $x + 2$",
          problema_md=(
              "Use división sintética para dividir $P(x) = 2x^4 - 3x^3 + 5x - 1$ por $x + 2$."
          ),
          pasos=[
              {"accion_md": (
                  "Reescribimos $x + 2 = x - (-2)$, luego $c = -2$. Coeficientes de $P(x)$ "
                  "**incluyendo el $0$ por el término $x^2$ ausente**: $2, -3, 0, 5, -1$."
               ),
               "justificacion_md": "Olvidar el $0$ por la potencia ausente es el error #1 de la "
                                   "división sintética.",
               "es_resultado": False},
              {"accion_md": (
                  "Tabla de división sintética (5 columnas porque $P$ tiene grado $4$):\n\n"
                  "| $c$ | $a_4$ | $a_3$ | $a_2$ | $a_1$ | $a_0$ |\n"
                  "|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                  "| $-2$ | $2$ | $-3$ | $0$ | $5$ | $-1$ |\n"
                  "|   |   | $-4$ | $14$ | $-28$ | $46$ |\n"
                  "| **resultado** | $\\mathbf{2}$ | $\\mathbf{-7}$ | $\\mathbf{14}$ | $\\mathbf{-23}$ | $\\mathbf{45}$ |\n\n"
                  "Bajamos el $2$. Luego $2 \\cdot (-2) = -4$; $-3 + (-4) = -7$. Sigue $-7 \\cdot (-2) = 14$; "
                  "$0 + 14 = 14$. Sigue $14 \\cdot (-2) = -28$; $5 + (-28) = -23$. Sigue $-23 \\cdot (-2) = 46$; "
                  "$-1 + 46 = 45$."
               ),
               "justificacion_md": "Aritmética directa con $c = -2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Resultado:** coeficientes del cociente $2, -7, 14, -23$ (grado $3$), resto $45$.\n\n"
                  "$$\\boxed{Q(x) = 2x^3 - 7x^2 + 14x - 23, \\quad R = 45.}$$\n\n"
                  "**Verificación por Teorema del Resto:** $P(-2) = 2(16) - 3(-8) + 5(-2) - 1 = "
                  "32 + 24 - 10 - 1 = 45$ ✓"
               ),
               "justificacion_md": "Siempre verificá con $P(c)$ — si $R \\neq P(c)$, hay un error de signo o aritmética.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Cero y factor de un polinomio",
          body_md=(
              "**Cero de $P$ (o raíz):** un número $c$ tal que $P(c) = 0$. Equivalentemente, una "
              "solución de la ecuación $P(x) = 0$.\n\n"
              "**Factor de $P$:** un polinomio $D(x)$ tal que al dividir $P$ entre $D$ el resto es $0$. "
              "En ese caso $P(x) = D(x) \\cdot Q(x)$, y decimos que $D$ **divide** a $P$."
          )),

        b("teorema",
          enunciado_md=(
              "**Teorema del Factor.** $c$ es **cero** de $P$ si y solo si $x - c$ es **factor** de $P(x)$.\n\n"
              "**Idea de la demostración.** Por el Teorema del Resto, $P(x) = (x - c)\\, Q(x) + P(c)$.\n\n"
              "- **($\\Rightarrow$)** Si $P(c) = 0$, entonces $P(x) = (x - c)\\, Q(x)$, así que $(x-c)$ "
              "es factor.\n"
              "- **($\\Leftarrow$)** Si $(x - c)$ es factor, entonces $P(x) = (x-c) Q(x)$ para algún "
              "$Q$; evaluando en $x = c$ obtenemos $P(c) = 0$. $\\quad\\square$"
          )),

        b("ejemplo_resuelto",
          titulo="Factorizar usando un cero conocido",
          problema_md=(
              "Sea $P(x) = x^3 - 7x + 6$. Verifique que $P(1) = 0$ y use división sintética para "
              "factorizar $P$ completamente."
          ),
          pasos=[
              {"accion_md": (
                  "**Verificación:** $P(1) = 1 - 7 + 6 = 0$ ✓. Por el Teorema del Factor, $(x - 1)$ "
                  "es factor de $P(x)$."
               ),
               "justificacion_md": "Encontrar **un** cero ya nos da un factor lineal.",
               "es_resultado": False},
              {"accion_md": (
                  "Aplicamos división sintética con $c = 1$ y coeficientes $1, 0, -7, 6$ (incluimos $0$ "
                  "por el término $x^2$ ausente):\n\n"
                  "| $c$ | $a_3$ | $a_2$ | $a_1$ | $a_0$ |\n"
                  "|:---:|:---:|:---:|:---:|:---:|\n"
                  "| $1$ | $1$ | $0$ | $-7$ | $6$ |\n"
                  "|   |   | $1$ | $1$ | $-6$ |\n"
                  "| **resultado** | $\\mathbf{1}$ | $\\mathbf{1}$ | $\\mathbf{-6}$ | $\\mathbf{0}$ |\n\n"
                  "El resto $0$ confirma que $1$ es raíz. El cociente es $Q(x) = x^2 + x - 6$."
               ),
               "justificacion_md": "Cuando ya sabemos un cero, la sintética entrega gratis el factor restante.",
               "es_resultado": False},
              {"accion_md": (
                  "Factorizamos el trinomio $x^2 + x - 6$ buscando dos números con suma $1$ y producto "
                  "$-6$: son $3$ y $-2$. Por lo tanto $x^2 + x - 6 = (x + 3)(x - 2)$.\n\n"
                  "**Factorización completa:**\n\n"
                  "$$\\boxed{P(x) = (x - 1)(x + 3)(x - 2).}$$"
               ),
               "justificacion_md": "Trinomio factorizable directamente — los ceros son $1, -3, 2$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Polinomio de grado 3 con tres raíces conocidas",
          problema_md=(
              "Considere $P(x) = 2x^3 - x^2 - 2x + 1$.\n\n"
              "- (a) Verifique que $1, -1$ y $\\tfrac{1}{2}$ son raíces de $P$.\n"
              "- (b) Justifique por qué $P$ no puede tener más de tres raíces.\n"
              "- (c) Use el Teorema del Factor para escribir a $P$ como producto de factores lineales."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Evaluamos en cada candidato:\n\n"
                  "- $P(1) = 2 - 1 - 2 + 1 = 0$ ✓\n"
                  "- $P(-1) = -2 - 1 + 2 + 1 = 0$ ✓\n"
                  "- $P(\\tfrac{1}{2}) = 2 \\cdot \\tfrac{1}{8} - \\tfrac{1}{4} - 1 + 1 = "
                  "\\tfrac{1}{4} - \\tfrac{1}{4} = 0$ ✓"
               ),
               "justificacion_md": "Verificación numérica directa.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Un resultado fundamental del álgebra: un polinomio de grado $n$ tiene a lo "
                  "sumo $n$ raíces reales (de hecho complejas, pero acá nos basta lo real). Como "
                  "$\\text{grad}(P) = 3$, $P$ no puede tener más de tres raíces."
               ),
               "justificacion_md": "Si tuviera $4$ raíces, podríamos extraer $4$ factores lineales y "
                                   "el grado sería $\\geq 4$ — contradicción.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** Por el Teorema del Factor cada raíz $c$ aporta un factor $x - c$. Como "
                  "$\\text{grad}(P) = 3$ y ya tenemos tres raíces:\n\n"
                  "$$P(x) = a_n (x - 1)(x + 1)\\bigl(x - \\tfrac{1}{2}\\bigr),$$\n\n"
                  "donde $a_n = 2$ es el coeficiente líder. Multiplicando $2 \\cdot (x - \\tfrac{1}{2}) = 2x - 1$:\n\n"
                  "$$\\boxed{P(x) = (x - 1)(x + 1)(2x - 1).}$$"
               ),
               "justificacion_md": "**Cuidado con el coeficiente líder** — cuando tenés todas las "
                                   "raíces, el factor de escala $a_n$ es esencial.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Fórmulas especiales de factorización",
          body_md=(
              "Las siguientes identidades algebraicas son de uso frecuente y se derivan como casos "
              "particulares del Teorema del Factor.\n\n"
              "| Nombre | Fórmula |\n|---|---|\n"
              "| Diferencia de cuadrados | $x^2 - a^2 = (x - a)(x + a)$ |\n"
              "| Cuadrado perfecto (suma) | $x^2 + 2ax + a^2 = (x + a)^2$ |\n"
              "| Cuadrado perfecto (resta) | $x^2 - 2ax + a^2 = (x - a)^2$ |\n"
              "| Diferencia de cubos | $x^3 - a^3 = (x - a)(x^2 + ax + a^2)$ |\n"
              "| Suma de cubos | $x^3 + a^3 = (x + a)(x^2 - ax + a^2)$ |\n\n"
              "**Cómo se justifican.** Para diferencia de cubos, $P(a) = a^3 - a^3 = 0$, luego "
              "$x - a$ es factor; el cociente $x^2 + ax + a^2$ se obtiene por división. Para suma de "
              "cubos, $P(-a) = -a^3 + a^3 = 0$, así que $x + a$ es factor."
          )),

        b("ejemplo_resuelto",
          titulo="Diferencia de cubos como caso particular del Teorema del Factor",
          problema_md=(
              "Encuentre una factorización para $x^3 - 1$."
          ),
          pasos=[
              {"accion_md": (
                  "Sea $P(x) = x^3 - 1$. Notamos que $P(1) = 1^3 - 1 = 0$, por lo que $x - 1$ es "
                  "factor de $P(x)$ (Teorema del Factor)."
               ),
               "justificacion_md": "Probar $c = 1$ es siempre un buen primer intento.",
               "es_resultado": False},
              {"accion_md": (
                  "Por división (larga o sintética): $x^3 - 1 = (x - 1)(x^2 + x + 1)$.\n\n"
                  "El cuadrático $x^2 + x + 1$ tiene discriminante $\\Delta = 1 - 4 = -3 < 0$, así que "
                  "**no tiene raíces reales**. Sobre $\\mathbb{R}$ esa es la factorización completa.\n\n"
                  "$$\\boxed{x^3 - 1 = (x - 1)(x^2 + x + 1).}$$"
               ),
               "justificacion_md": "Es el caso particular $a = 1$ de la diferencia de cubos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Aplicación combinada de fórmulas",
          problema_md=(
              "Factorice los siguientes polinomios:\n\n"
              "- (a) $4x^2 - 25$.\n"
              "- (b) $x^6 + 8$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Reconocemos $4x^2 - 25 = (2x)^2 - 5^2$, una **diferencia de cuadrados**. "
                  "Aplicando la fórmula con $u = 2x$, $a = 5$:\n\n"
                  "$$\\boxed{4x^2 - 25 = (2x - 5)(2x + 5).}$$"
               ),
               "justificacion_md": "Detectar que un coeficiente es cuadrado perfecto disfrazado es "
                                   "el truco principal.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Reconocemos $x^6 + 8 = (x^2)^3 + 2^3$, una **suma de cubos** con $u = x^2$, "
                  "$a = 2$. Aplicamos la fórmula:\n\n"
                  "$$x^6 + 8 = (x^2 + 2)\\bigl((x^2)^2 - 2 x^2 + 4\\bigr) = (x^2 + 2)(x^4 - 2x^2 + 4).$$\n\n"
                  "El factor $x^2 + 2$ no tiene raíces reales (discriminante $-8$). El factor "
                  "$x^4 - 2x^2 + 4$ tampoco — no se descompone más sobre $\\mathbb{R}$.\n\n"
                  "$$\\boxed{x^6 + 8 = (x^2 + 2)(x^4 - 2x^2 + 4).}$$"
               ),
               "justificacion_md": "Para potencias múltiplo de $3$, intentá ver el polinomio como "
                                   "suma/diferencia de cubos.",
               "es_resultado": True},
          ]),

        ej(
            "Factorización completa con búsqueda de raíces",
            "Factorice completamente $P(x) = x^3 - 4x^2 + x + 6$. Pista: probá enteros pequeños como "
            "candidatos a raíz.",
            [
                "Probá $c \\in \\{-2, -1, 1, 2, 3\\}$ y buscá uno con $P(c) = 0$.",
                "Cuando encuentres una raíz $c$, usá división sintética para obtener el cociente cuadrático.",
                "El cuadrático resultante debería factorizarse fácilmente o usar la fórmula cuadrática.",
            ],
            (
                "**Buscar una raíz:** $P(-1) = -1 - 4 - 1 + 6 = 0$ ✓. Luego $(x+1)$ es factor.\n\n"
                "**División sintética con $c = -1$**, coeficientes $1, -4, 1, 6$:\n\n"
                "| $c$ | $a_3$ | $a_2$ | $a_1$ | $a_0$ |\n"
                "|:---:|:---:|:---:|:---:|:---:|\n"
                "| $-1$ | $1$ | $-4$ | $1$ | $6$ |\n"
                "|   |   | $-1$ | $5$ | $-6$ |\n"
                "| **resultado** | $\\mathbf{1}$ | $\\mathbf{-5}$ | $\\mathbf{6}$ | $\\mathbf{0}$ |\n\n"
                "Cociente: $x^2 - 5x + 6$. Factorizamos: dos números con suma $-5$ y producto $6$ → $-2, -3$. "
                "Luego $x^2 - 5x + 6 = (x - 2)(x - 3)$.\n\n"
                "**Factorización completa:** $\\boxed{P(x) = (x + 1)(x - 2)(x - 3).}$\n\n"
                "Las raíces son $-1, 2, 3$."
            ),
        ),

        ej(
            "Resto de un polinomio con exponente grande",
            "Calcule el resto al dividir $P(x) = x^{100} + 3x^{50} - 2$ entre $x - 1$.",
            [
                "No hagas la división larga — sería absurdo con grado $100$.",
                "Aplicá directamente el Teorema del Resto: $R = P(c)$ donde $c$ es la raíz del divisor.",
                "Recordá que $1^k = 1$ para todo $k$.",
            ],
            (
                "Por el Teorema del Resto, $R = P(1) = 1^{100} + 3 \\cdot 1^{50} - 2 = 1 + 3 - 2 = "
                "\\boxed{2}$.\n\n"
                "El Teorema del Resto convierte un cálculo aparentemente brutal en una evaluación trivial."
            ),
        ),

        b("verificacion",
          intro_md="Verifica tu dominio del Teorema del Resto y del Factor:",
          preguntas=[
              {"enunciado_md": "¿Cuál es el resto al dividir $P(x) = x^{50} - 3x + 1$ entre $x + 1$?",
               "opciones_md": ["$-1$", "$3$", "$5$", "$-3$"],
               "correcta": "C",
               "pista_md": "Aplicá el Teorema del Resto con $c = -1$ (porque $x + 1 = x - (-1)$).",
               "explicacion_md": "$P(-1) = (-1)^{50} - 3(-1) + 1 = 1 + 3 + 1 = 5$. El signo del divisor invierte $c$."},
              {"enunciado_md": "Si $P$ es un polinomio de grado $4$ con coeficiente líder $a_4 = 3$ y raíces $1, -1, 2, -2$, ¿cuál es la factorización?",
               "opciones_md": [
                   "$P(x) = (x - 1)(x + 1)(x - 2)(x + 2)$",
                   "$P(x) = 3(x - 1)(x + 1)(x - 2)(x + 2)$",
                   "$P(x) = 3(x + 1)(x - 1)(x + 2)(x - 2) + 3$",
                   "$P(x) = (x - 1)(x + 1)(x - 2)(x + 2) + 3$",
               ],
               "correcta": "B",
               "pista_md": "Cuando reconstruís desde raíces, no olvides el coeficiente líder $a_n$.",
               "explicacion_md": "$P(x) = a_n \\prod (x - c_i) = 3(x-1)(x+1)(x-2)(x+2)$. Sin el $3$ el polinomio sería mónico."},
              {"enunciado_md": "¿Cuál es la factorización correcta de $x^3 + 8$ sobre $\\mathbb{R}$?",
               "opciones_md": [
                   "$(x + 2)(x^2 + 2x + 4)$",
                   "$(x + 2)(x^2 - 2x + 4)$",
                   "$(x - 2)(x^2 + 2x + 4)$",
                   "$(x - 2)(x^2 - 2x + 4)$",
               ],
               "correcta": "B",
               "pista_md": "Suma de cubos: $x^3 + a^3 = (x + a)(x^2 - ax + a^2)$.",
               "explicacion_md": "Con $a = 2$: $(x + 2)(x^2 - 2x + 4)$. El término medio del cuadrático lleva signo opuesto al de la suma."},
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir el signo de $c$:** al dividir entre $x + a$, la raíz del divisor es $c = -a$, no $a$. "
              "$x + 3 \\Rightarrow c = -3$, $x - 3 \\Rightarrow c = 3$.",
              "**Olvidar el $0$ por la potencia ausente** en la división sintética. Si $P(x) = x^4 - 1$, "
              "los coeficientes son $1, 0, 0, 0, -1$ — no $1, -1$.",
              "**Aplicar división sintética con divisor no lineal o no mónico.** La sintética solo "
              "funciona con $x - c$ (coeficiente líder $1$).",
              "**Olvidar el coeficiente líder al reconstruir desde raíces.** Si $P$ tiene grado $n$ y "
              "raíces $c_1, \\ldots, c_n$, entonces $P(x) = a_n(x - c_1)\\cdots(x - c_n)$, no solo el producto.",
              "**Suponer que todo cuadrático se factoriza en $\\mathbb{R}$.** Si $\\Delta < 0$, no hay "
              "raíces reales y el cuadrático es irreducible sobre $\\mathbb{R}$.",
              "**Confundir suma y diferencia de cubos:** $x^3 - a^3 = (x-a)(x^2 + ax + a^2)$ (signos $+$ "
              "en el cuadrático), $x^3 + a^3 = (x+a)(x^2 - ax + a^2)$ (signo $-$ del término medio).",
          ]),

        b("resumen",
          puntos_md=[
              "**Teorema del Resto:** al dividir $P(x)$ por $x - c$, el resto es $R = P(c)$.",
              "**División sintética:** atajo para divisores lineales $x - c$ — opera solo sobre coeficientes.",
              "**Teorema del Factor:** $c$ es cero de $P \\iff (x - c)$ es factor de $P$.",
              "**Factorizar = encontrar raíces:** cada raíz $c$ aporta un factor $(x - c)$. Polinomio de grado $n$ "
              "tiene a lo sumo $n$ raíces reales.",
              "**Coeficiente líder:** al reconstruir $P$ desde sus raíces, multiplicar por $a_n$.",
              "**Fórmulas especiales:** diferencia de cuadrados, cuadrados perfectos, diferencia y suma de cubos.",
              "**Próximo capítulo:** desigualdades — orden en $\\mathbb{R}$, valor absoluto, intervalos e inecuaciones.",
          ]),
    ]
    return {
        "id": "lec-ic-1-2-factor-resto",
        "title": "Teorema del factor y resto",
        "description": "Teorema del Resto, división sintética, Teorema del Factor y fórmulas especiales de factorización.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "intro-calculo"

    course_doc = {
        "id": course_id,
        "title": "Introducción al Cálculo",
        "description": (
            "Polinomios, desigualdades, funciones reales, sucesiones y funciones exponencial y "
            "logarítmica. Curso puente al cálculo diferencial e integral."
        ),
        "category": "Matemáticas",
        "level": "Intermedio",
        "modules_count": 5,
        "rating": 4.8,
        "summary": "Curso introductorio de cálculo para alumnos universitarios chilenos.",
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

    chapter_id = "ch-ic-polinomios"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Polinomios",
        "description": (
            "Definición de polinomio, propiedades del grado, algoritmo de la división, división "
            "sintética y Teorema del Factor con fórmulas especiales de factorización."
        ),
        "order": 1,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_1_1, lesson_1_2]
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
    print(f"✅ Capítulo 1 — Polinomios listo: {len(builders)} lecciones, {total_blocks} bloques, "
          f"{total_figs} figuras pendientes.")
    print()
    print("URLs locales para verificar:")
    print(f"  http://localhost:3007/courses/{course_id}")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
