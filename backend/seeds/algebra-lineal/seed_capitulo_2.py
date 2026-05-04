"""
Seed del curso Álgebra Lineal — Capítulo 2: Sistemas de Ecuaciones.
5 lecciones:
  2.1 Matrices
  2.2 Reducción por filas
  2.3 Independencia lineal
  2.4 Conjunto solución
  2.5 Transformaciones lineales

Basado en los Apuntes/Clase de Se Remonta para cada lección.
Estructura algebraica clásica: del sistema lineal al lenguaje matricial,
método de Gauss–Jordan, lectura de la RREF, conexión con $\\text{Gen}\\{a_i\\}$,
$\\text{Col}(A)$, núcleo, y transformaciones lineales $T(x) = Ax$.

Requiere que el curso 'algebra-lineal' ya exista (ver
seed_algebra_lineal_chapter_1.py). Idempotente: borra y recrea el capítulo
y sus lecciones.
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
# 2.1 Matrices
# =====================================================================
def lesson_2_1():
    blocks = [
        b("texto", body_md=(
            "Un **sistema de ecuaciones lineales** es la herramienta más básica del álgebra lineal: "
            "un conjunto finito de ecuaciones de primer grado en las mismas incógnitas. En esta lección "
            "presentamos el lenguaje **matricial** que permite tratar a un sistema entero como un único "
            "objeto $A\\vec{x} = \\vec{b}$ y manipular su **matriz aumentada** $[A \\mid \\vec{b}]$.\n\n"
            "Este formalismo es central porque:\n\n"
            "- **Compacta** la notación (un símbolo $A$ reemplaza decenas de coeficientes).\n"
            "- Permite **algoritmos sistemáticos** (próxima lección: Gauss–Jordan).\n"
            "- Conecta sistemas con vectores, transformaciones y geometría.\n\n"
            "Al terminar la lección debes poder:\n\n"
            "- Escribir cualquier sistema lineal en forma $A\\vec{x} = \\vec{b}$ y como $[A \\mid \\vec{b}]$.\n"
            "- Reconocer el **tamaño** $m \\times n$ y manipular **filas, columnas e índices**.\n"
            "- Distinguir las tres clasificaciones posibles: **SCD, SCI, SI**."
        )),

        b("definicion",
          titulo="Ecuación lineal",
          body_md=(
              "Una **ecuación lineal** en las variables $x_1, \\ldots, x_n$ es una expresión de la forma\n\n"
              "$$a_1 x_1 + a_2 x_2 + \\cdots + a_n x_n = b,$$\n\n"
              "donde $a_1, \\ldots, a_n, b \\in \\mathbb{R}$ (o $\\mathbb{C}$) son constantes conocidas. "
              "Los $a_i$ se llaman **coeficientes** y $b$ es el **término independiente**.\n\n"
              "**Lo que NO es lineal:** $x_1^2$, $x_1 x_2$, $\\sin(x_1)$, $1/x_1$. En una ecuación lineal "
              "cada incógnita aparece **a la primera potencia** y multiplicada por una constante."
          )),

        b("definicion",
          titulo="Sistema lineal y forma matricial",
          body_md=(
              "Un **sistema lineal** es un conjunto finito de ecuaciones lineales en las mismas variables. "
              "Forma compacta:\n\n"
              "$$A \\vec{x} = \\vec{b}, \\qquad A \\in \\mathbb{R}^{m \\times n}, \\quad \\vec{x} \\in \\mathbb{R}^n, \\quad \\vec{b} \\in \\mathbb{R}^m.$$\n\n"
              "- $A$ es la **matriz de coeficientes** ($m$ filas $\\times$ $n$ columnas).\n"
              "- $\\vec{x}$ es el **vector de incógnitas**.\n"
              "- $\\vec{b}$ es el **vector de términos independientes**.\n\n"
              "La **matriz aumentada** del sistema es\n\n"
              "$$[A \\mid \\vec{b}] \\in \\mathbb{R}^{m \\times (n+1)},$$\n\n"
              "que añade $\\vec{b}$ como una columna extra separada por una barra. Concentra **toda la información** "
              "del sistema en un solo arreglo y será nuestro objeto de trabajo principal."
          )),

        b("ejemplo_resuelto",
          titulo="Pasar de ecuaciones a matriz aumentada",
          problema_md=(
              "Escribir en forma $A\\vec{x} = \\vec{b}$ y como matriz aumentada $[A \\mid \\vec{b}]$:\n\n"
              "$$\\begin{cases} x_1 - 2x_2 + x_3 = 0, \\\\ \\phantom{x_1 +\\,} 2x_2 - 8x_3 = 8, \\\\ -4x_1 + 5x_2 + 9x_3 = -9. \\end{cases}$$"
          ),
          pasos=[
              {"accion_md": (
                  "Identificamos coeficientes columna por columna y respetamos los **ceros** "
                  "donde una variable no aparece (en la 2ª ecuación falta $x_1$, así que su coeficiente es $0$):\n\n"
                  "$$A = \\begin{bmatrix} 1 & -2 & 1 \\\\ 0 & 2 & -8 \\\\ -4 & 5 & 9 \\end{bmatrix}, \\quad "
                  "\\vec{x} = \\begin{bmatrix} x_1 \\\\ x_2 \\\\ x_3 \\end{bmatrix}, \\quad "
                  "\\vec{b} = \\begin{bmatrix} 0 \\\\ 8 \\\\ -9 \\end{bmatrix}.$$"
              ),
               "justificacion_md": "Cada **fila** de $A$ corresponde a una ecuación; cada **columna**, a una incógnita.",
               "es_resultado": False},
              {"accion_md": (
                  "Matriz aumentada:\n\n"
                  "$$[A \\mid \\vec{b}] = \\left[ \\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\\\ 0 & 2 & -8 & 8 \\\\ -4 & 5 & 9 & -9 \\end{array} \\right] \\in \\mathbb{R}^{3 \\times 4}.$$"
              ),
               "justificacion_md": "**Tamaño:** $A \\in \\mathbb{R}^{3\\times 3}$ y $[A\\mid\\vec{b}] \\in \\mathbb{R}^{3\\times 4}$. La barra es solo visual: separa los coeficientes del término independiente.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Matriz, índices, filas y columnas",
          body_md=(
              "Una **matriz** $A$ de tamaño $m \\times n$ sobre $\\mathbb{K}$ ($\\mathbb{R}$ o $\\mathbb{C}$) "
              "es un arreglo rectangular de entradas $a_{ij} \\in \\mathbb{K}$:\n\n"
              "$$A = (a_{ij})_{m \\times n} = \\begin{bmatrix} a_{11} & a_{12} & \\cdots & a_{1n} \\\\ a_{21} & a_{22} & \\cdots & a_{2n} \\\\ \\vdots & \\vdots & \\ddots & \\vdots \\\\ a_{m1} & a_{m2} & \\cdots & a_{mn} \\end{bmatrix}$$\n\n"
              "**Convención de índices:** $i$ es el índice de **fila** ($1 \\leq i \\leq m$), $j$ el de **columna** ($1 \\leq j \\leq n$). Siempre **fila primero**.\n\n"
              "- Una **fila** es un vector $1 \\times n$.\n"
              "- Una **columna** es un vector $m \\times 1$.\n\n"
              "**Notaciones especiales:** $\\mathbf{0}_{m\\times n}$ es la **matriz cero** (todas sus entradas son $0$). "
              "$I_n$ es la **identidad** $n \\times n$: unos en la diagonal y ceros fuera."
          )),

        b("ejemplo_resuelto",
          titulo="Lectura de índices",
          problema_md=(
              "Sea $B = \\begin{bmatrix} 2 & 1 & 0 & -1 \\\\ 3 & 4 & 5 & 6 \\\\ 0 & -2 & 7 & 8 \\end{bmatrix}$. "
              "Determinar (i) tamaño; (ii) fila $2$ y columna $3$; (iii) entradas $b_{23}$ y $b_{31}$."
          ),
          pasos=[
              {"accion_md": "**(i)** $B$ tiene $3$ filas y $4$ columnas $\\Rightarrow B \\in \\mathbb{R}^{3 \\times 4}$.",
               "justificacion_md": "Contar filas y columnas.",
               "es_resultado": False},
              {"accion_md": (
                  "**(ii)** Fila $2$: $(3,\\ 4,\\ 5,\\ 6)$. Columna $3$: $(0,\\ 5,\\ 7)^T$."
              ),
               "justificacion_md": "Las filas son vectores $1\\times 4$; las columnas, vectores $3\\times 1$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(iii)** $b_{23}$: fila $2$, columna $3$ $\\Rightarrow b_{23} = 5$. "
                  "$b_{31}$: fila $3$, columna $1$ $\\Rightarrow b_{31} = 0$."
              ),
               "justificacion_md": "**Regla mnemotécnica:** $b_{ij}$ = '$b$ fila $i$ columna $j$'.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Clasificación de un sistema lineal",
          body_md=(
              "Todo sistema lineal cae en **exactamente una** de tres categorías según su conjunto solución:\n\n"
              "| Sigla | Nombre | Soluciones |\n|---|---|---|\n"
              "| **SCD** | Sistema Compatible **Determinado** | **Una única** solución |\n"
              "| **SCI** | Sistema Compatible **Indeterminado** | **Infinitas** soluciones |\n"
              "| **SI** | Sistema **Incompatible** | **Ninguna** solución |\n\n"
              "**'Compatible'** = tiene al menos una solución (existencia). **'Determinado'** = la solución es única (unicidad).\n\n"
              "**Nunca puede haber exactamente $2$ ni $17$ soluciones:** un sistema lineal tiene $0$, $1$ o $\\infty$ soluciones — propiedad estructural que justificaremos en la próxima lección."
          )),

        fig(
            "Tres pares de rectas en el plano cartesiano que ilustran las tres clasificaciones de un sistema 2x2. "
            "Panel izquierdo (SCD): dos rectas que se cortan en un único punto, etiquetado '1 sol.'. "
            "Panel central (SI): dos rectas paralelas distintas que nunca se cortan, etiquetado '0 sol.' (sin solución). "
            "Panel derecho (SCI): dos rectas coincidentes (la misma recta dibujada con doble trazo), etiquetado '∞ sol.'. "
            "Ejes x e y simples, líneas en color teal, etiquetas en español. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="SCD — solución única",
          problema_md=(
              "Resolver $\\begin{cases} x_1 - 2x_2 = -1, \\\\ -x_1 + 3x_2 = 3. \\end{cases}$"
          ),
          pasos=[
              {"accion_md": (
                  "Sumamos las dos ecuaciones: $x_2 = 2$. "
                  "Sustituyendo en la primera: $x_1 - 4 = -1 \\Rightarrow x_1 = 3$."
              ),
               "justificacion_md": "Eliminación: la suma cancela $x_1$ y deja una ecuación en $x_2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución única:** $(x_1, x_2) = (3, 2)$.\n\n"
                  "**Verificación:** $3 - 2(2) = -1$ ✓ y $-3 + 3(2) = 3$ ✓."
              ),
               "justificacion_md": "Geométricamente: las rectas $x_1 - 2x_2 = -1$ y $-x_1 + 3x_2 = 3$ se cortan en el punto $(3,2)$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="SI — sin solución",
          problema_md=(
              "Resolver $\\begin{cases} x_1 - 2x_2 = -1, \\\\ -x_1 + 2x_2 = 3. \\end{cases}$"
          ),
          pasos=[
              {"accion_md": "Sumamos: $0 = 2$. **Contradicción.**",
               "justificacion_md": "Los lados izquierdos se cancelan completamente (las filas de coeficientes son opuestas), pero los términos independientes no.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión: SI** (incompatible). No existe ningún par $(x_1, x_2)$ que satisfaga ambas ecuaciones.\n\n"
                  "**Geometría:** las dos rectas tienen la misma pendiente $1/2$ pero distintas ordenadas — son **paralelas distintas**, nunca se cortan."
              ),
               "justificacion_md": "**Patrón general:** una contradicción del tipo $0 = c$ con $c \\neq 0$ es la firma algebraica de SI.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="SCI — infinitas soluciones",
          problema_md=(
              "Resolver $\\begin{cases} x_1 - 2x_2 = -1, \\\\ -2x_1 + 4x_2 = 2. \\end{cases}$"
          ),
          pasos=[
              {"accion_md": "La segunda ecuación es exactamente $-2$ veces la primera $\\Rightarrow$ son **dependientes** (es la misma ecuación disfrazada).",
               "justificacion_md": "Multiplicar una ecuación por una constante no nula no agrega información.",
               "es_resultado": False},
              {"accion_md": (
                  "Tenemos en realidad **una sola ecuación útil**: $x_1 - 2x_2 = -1$.\n\n"
                  "Parametrizamos con $t \\in \\mathbb{R}$: tomamos $x_2 = t$ y despejamos $x_1 = 2t - 1$.\n\n"
                  "**Conjunto solución:** $\\{(2t - 1,\\ t) : t \\in \\mathbb{R}\\}$ — **infinitas** soluciones (una por cada valor de $t$)."
              ),
               "justificacion_md": "**Geometría:** las dos 'rectas' coinciden — toda la recta $x_1 - 2x_2 = -1$ es solución.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**¿Por qué solo $0$, $1$ o $\\infty$?** Cada ecuación lineal define un **hiperplano** en $\\mathbb{R}^n$ (recta en $\\mathbb{R}^2$, plano en $\\mathbb{R}^3$). El conjunto solución del sistema es la **intersección** de esos hiperplanos. La intersección de objetos lineales es siempre lineal: vacía (SI), un punto (SCD) o un objeto lineal de dimensión $\\geq 1$ (SCI, infinitos puntos). **Nunca** un puñado finito $> 1$ de puntos. Lo justificaremos formalmente en la lección 2.4."
        )),

        b("verificacion",
          intro_md="Verifica conceptos clave:",
          preguntas=[
              {
                  "enunciado_md": "Para el sistema $\\begin{cases} 2x_1 - x_2 + 4x_3 = 7 \\\\ -3x_1 + 5x_2 - 2x_3 = 0 \\end{cases}$, el tamaño de $A$ es:",
                  "opciones_md": ["$3 \\times 2$", "$2 \\times 3$", "$2 \\times 4$", "$3 \\times 3$"],
                  "correcta": "B",
                  "pista_md": "Filas $=$ ecuaciones, columnas $=$ incógnitas.",
                  "explicacion_md": "**$A \\in \\mathbb{R}^{2 \\times 3}$:** 2 ecuaciones (filas) y 3 incógnitas $x_1, x_2, x_3$ (columnas). La matriz aumentada $[A\\mid\\vec{b}]$ sería $2 \\times 4$.",
              },
              {
                  "enunciado_md": "Si en el proceso de resolución llegas a la línea $0 = 5$, el sistema es:",
                  "opciones_md": ["SCD", "SCI", "SI", "Imposible decidir"],
                  "correcta": "C",
                  "pista_md": "$0 = 5$ es una contradicción.",
                  "explicacion_md": "**SI (incompatible).** Una ecuación de la forma $0 = c$ con $c \\neq 0$ es imposible de satisfacer, así que el sistema no tiene solución.",
              },
              {
                  "enunciado_md": "Un sistema lineal puede tener exactamente:",
                  "opciones_md": [
                      "$0$, $1$ o $\\infty$ soluciones",
                      "Cualquier cantidad finita de soluciones",
                      "Solo $0$ o $1$ soluciones",
                      "Solo $1$ o $\\infty$ soluciones",
                  ],
                  "correcta": "A",
                  "pista_md": "Estructuralmente solo hay tres casos: SI, SCD, SCI.",
                  "explicacion_md": "Las únicas posibilidades son $0$ (SI), $1$ (SCD) o $\\infty$ (SCI). Es **imposible** que un sistema lineal tenga, por ejemplo, exactamente $2$ soluciones.",
              },
          ]),

        ej(
            "Escribir un sistema en forma matricial",
            "Escribe en forma matricial $A\\vec{x} = \\vec{b}$ el sistema $\\begin{cases} 2x_1 - x_2 + 4x_3 = 7, \\\\ -3x_1 + 5x_2 - 2x_3 = 0. \\end{cases}$ Indica $A$, $\\vec{x}$, $\\vec{b}$ y sus tamaños.",
            [
                "$A$ tiene una fila por cada ecuación.",
                "$A$ tiene una columna por cada incógnita.",
                "Recuerda que la matriz aumentada es $[A\\mid\\vec{b}]$ y tiene una columna más.",
            ],
            (
                "$$A = \\begin{bmatrix} 2 & -1 & 4 \\\\ -3 & 5 & -2 \\end{bmatrix} \\in \\mathbb{R}^{2 \\times 3}, \\quad "
                "\\vec{x} = \\begin{bmatrix} x_1 \\\\ x_2 \\\\ x_3 \\end{bmatrix} \\in \\mathbb{R}^{3 \\times 1}, \\quad "
                "\\vec{b} = \\begin{bmatrix} 7 \\\\ 0 \\end{bmatrix} \\in \\mathbb{R}^{2 \\times 1}.$$\n\n"
                "Matriz aumentada: $[A \\mid \\vec{b}] = \\left[\\begin{array}{rrr|r} 2 & -1 & 4 & 7 \\\\ -3 & 5 & -2 & 0 \\end{array}\\right] \\in \\mathbb{R}^{2 \\times 4}$."
            ),
        ),

        ej(
            "Clasificar tres sistemas $2 \\times 2$",
            "Para cada sistema, decide si es SCD, SCI o SI y justifica.\n\n"
            "**(a)** $\\begin{cases} x_1 + x_2 = 3 \\\\ x_1 - x_2 = 1 \\end{cases}$ "
            "**(b)** $\\begin{cases} 2x_1 + x_2 = 4 \\\\ 4x_1 + 2x_2 = 7 \\end{cases}$ "
            "**(c)** $\\begin{cases} x_1 - 3x_2 = 2 \\\\ 2x_1 - 6x_2 = 4 \\end{cases}$",
            [
                "Para (a), suma o resta para eliminar una variable.",
                "Para (b), nota que la fila de coeficientes de la 2ª es múltiplo de la 1ª, ¿y los términos independientes?",
                "Para (c), ¿la 2ª ecuación es proporcional a la 1ª, también del lado derecho?",
            ],
            (
                "**(a) SCD.** Sumando: $2x_1 = 4 \\Rightarrow x_1 = 2$, luego $x_2 = 1$. Solución única $(2, 1)$.\n\n"
                "**(b) SI.** La 2ª fila de $A$ es $2$ veces la 1ª, pero $7 \\neq 2 \\cdot 4 = 8$. Restando $2 \\times$ (1ª) a la (2ª): $0 = -1$, contradicción.\n\n"
                "**(c) SCI.** La 2ª ecuación es exactamente $2$ veces la 1ª (también del lado derecho: $4 = 2 \\cdot 2$). Una sola ecuación útil: $x_1 = 3x_2 + 2$. Conjunto solución $\\{(3t+2, t): t \\in \\mathbb{R}\\}$."
            ),
        ),

        ej(
            "De matriz aumentada a sistema",
            "Escribe el sistema asociado a la matriz aumentada $\\left[\\begin{array}{rrrr|r} 1 & 0 & 3 & -2 & 5 \\\\ 0 & 2 & -1 & 4 & 0 \\\\ -1 & 1 & 0 & 0 & 7 \\end{array}\\right]$ usando variables $x_1, x_2, x_3, x_4$. Indica los tamaños $m, n$.",
            [
                "Cada fila es una ecuación.",
                "El número de incógnitas $n$ es el número de columnas de $A$ (sin contar la última).",
            ],
            (
                "$m = 3$ ecuaciones, $n = 4$ incógnitas. $A \\in \\mathbb{R}^{3\\times 4}$, $[A\\mid\\vec{b}] \\in \\mathbb{R}^{3 \\times 5}$.\n\n"
                "Sistema:\n\n"
                "$$\\begin{cases} \\phantom{-}x_1 + \\phantom{0x_2 +}\\, 3x_3 - 2x_4 = 5, \\\\ \\phantom{-x_1 + \\,}2x_2 - \\phantom{0}x_3 + 4x_4 = 0, \\\\ -x_1 + \\phantom{0}x_2 \\phantom{ + 3x_3 + 4x_4} = 7. \\end{cases}$$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar los ceros** en columnas donde una variable no aparece. Si una ecuación es $2x_2 - 8x_3 = 8$, el coeficiente de $x_1$ es $0$, no se omite.",
              "**Invertir el orden de los índices.** $a_{ij}$ es siempre 'fila $i$, columna $j$' — fila primero.",
              "**Confundir $A$ con $[A \\mid \\vec{b}]$.** $A$ tiene $n$ columnas (las incógnitas); $[A\\mid\\vec{b}]$ tiene $n+1$ columnas.",
              "**Pensar que un sistema lineal puede tener $2$ o $3$ soluciones aisladas.** Imposible: solo $0$, $1$ o $\\infty$.",
              "**Decir 'el sistema es indeterminado' cuando hay contradicción.** Indeterminado = SCI = infinitas soluciones. Sin solución = SI = incompatible.",
              "**Mezclar variables al cambiar a forma matricial.** El orden de las columnas debe ser consistente con el orden elegido para $x_1, x_2, \\ldots$",
          ]),

        b("resumen",
          puntos_md=[
              "**Ecuación lineal:** $a_1 x_1 + \\cdots + a_n x_n = b$ — variables a la primera potencia.",
              "**Sistema:** conjunto finito de ecuaciones lineales, escrito como $A\\vec{x} = \\vec{b}$.",
              "**Matriz aumentada** $[A \\mid \\vec{b}]$: concentra toda la información del sistema.",
              "**Tamaño:** $A \\in \\mathbb{R}^{m \\times n}$ ($m$ ecuaciones, $n$ incógnitas), $[A\\mid\\vec{b}] \\in \\mathbb{R}^{m \\times (n+1)}$.",
              "**Índices:** $a_{ij}$ es fila $i$, columna $j$. **Filas** son vectores $1 \\times n$; **columnas**, $m \\times 1$.",
              "**Clasificación:** SCD (única), SCI (infinitas), SI (ninguna). Nunca un número finito $> 1$.",
              "**Próxima lección:** algoritmo sistemático (reducción por filas) para clasificar y resolver cualquier sistema.",
          ]),
    ]
    return {
        "id": "lec-al-2-1-matrices",
        "title": "Matrices",
        "description": "Sistema lineal, forma $A\\vec{x} = \\vec{b}$, matriz aumentada, índices, clasificación SCD/SCI/SI.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 2.2 Reducción por filas
# =====================================================================
def lesson_2_2():
    blocks = [
        b("texto", body_md=(
            "El **método de reducción por filas** (o **eliminación de Gauss / Gauss–Jordan**) es el "
            "algoritmo central del álgebra lineal computacional. Permite, mediante un número finito de "
            "**operaciones elementales de fila**, llevar cualquier matriz a una forma estandarizada — "
            "**escalonada** (REF) o **escalonada reducida** (RREF) — desde la cual se lee directamente:\n\n"
            "- si el sistema asociado tiene solución (existencia),\n"
            "- si la solución es única (unicidad),\n"
            "- y, cuando hay infinitas soluciones, una **parametrización** explícita.\n\n"
            "Al terminar:\n\n"
            "- Dominas las tres **OEF** y el **algoritmo de reducción** en 5 pasos.\n"
            "- Reconoces formas REF y RREF y sus pivotes.\n"
            "- Calculas el **rango** y aplicas el criterio de **Rouché–Frobenius**."
        )),

        b("definicion",
          titulo="Operaciones elementales de fila (OEF)",
          body_md=(
              "Son tres transformaciones sobre las filas de una matriz que **no alteran el conjunto solución** del sistema asociado:\n\n"
              "| Tipo | Notación | Efecto |\n|---|---|---|\n"
              "| **1. Reemplazo** | $F_i \\leftarrow F_i + k\\,F_j$ | Suma a la fila $i$ un múltiplo $k$ de la fila $j$ ($i \\neq j$). |\n"
              "| **2. Intercambio** | $F_i \\leftrightarrow F_j$ | Permuta dos filas. |\n"
              "| **3. Escalamiento** | $F_i \\leftarrow c\\,F_i$ con $c \\neq 0$ | Multiplica una fila por una constante no nula. |\n\n"
              "**Proposición.** Si dos matrices aumentadas son **equivalentes por filas** (una se obtiene de la otra mediante OEF), entonces representan sistemas con el **mismo conjunto solución**.\n\n"
              "**Por qué $c \\neq 0$:** multiplicar por $0$ borraría la información de esa ecuación."
          )),

        b("definicion",
          titulo="Forma escalonada (REF) y reducida (RREF)",
          body_md=(
              "**Entrada principal** de una fila no nula: la primera entrada (de izquierda a derecha) distinta de $0$. Su columna se llama **columna pivote**.\n\n"
              "Una matriz está en **forma escalonada (REF)** si:\n\n"
              "1. Todas las filas no nulas están **arriba** de las filas nulas.\n"
              "2. La entrada principal de cada fila está **a la derecha** de la entrada principal de la fila superior.\n"
              "3. En cada columna pivote, todas las entradas **debajo** del pivote son $0$.\n\n"
              "Está en **forma escalonada reducida (RREF)** si además:\n\n"
              "4. Cada entrada principal es $1$ (los **1 principales**).\n"
              "5. En cada columna pivote, el $1$ principal es la **única** entrada no nula (también hay ceros **arriba**).\n\n"
              "**Teorema (unicidad de la RREF).** Toda matriz es equivalente por filas a **una y solo una** matriz en RREF. Las **posiciones pivote** no dependen del camino de OEF elegido."
          )),

        b("ejemplo_resuelto",
          titulo="Clasificar matrices: REF, RREF o ninguna",
          problema_md=(
              "Para cada matriz, indica si está en REF, en RREF o en ninguna.\n\n"
              "$$M_1 = \\begin{bmatrix} 2 & -3 & 2 & 1 \\\\ 0 & 1 & -4 & 8 \\\\ 0 & 0 & 1 & 3 \\end{bmatrix}, \\quad "
              "M_2 = \\begin{bmatrix} 1 & 0 & 0 & 29 \\\\ 0 & 1 & 0 & 16 \\\\ 0 & 0 & 1 & 3 \\end{bmatrix}, \\quad "
              "M_3 = \\begin{bmatrix} 0 & 1 & 3 & 2 \\\\ 0 & 0 & 0 & 1 \\\\ 0 & 0 & 1 & 0 \\end{bmatrix}.$$"
          ),
          pasos=[
              {"accion_md": "**$M_1$:** los pivotes están en posiciones $(1,1), (2,2), (3,3)$, escalonados estrictamente. Las entradas debajo de cada pivote son $0$. Es **REF**, pero el pivote $(1,1)$ vale $2 \\neq 1$ $\\Rightarrow$ **no es RREF**.",
               "justificacion_md": "Cumple las condiciones 1–3 pero falla la 4.",
               "es_resultado": False},
              {"accion_md": "**$M_2$:** pivotes en $(1,1), (2,2), (3,3)$, todos iguales a $1$, y el resto de cada columna pivote es $0$. Cumple las 5 condiciones $\\Rightarrow$ **RREF**.",
               "justificacion_md": "Es la 'forma final' de Gauss–Jordan.",
               "es_resultado": False},
              {"accion_md": "**$M_3$:** la entrada principal de la fila $3$ está en la columna $3$, **a la izquierda** de la entrada principal de la fila $2$ (columna $4$). Viola la condición 2 $\\Rightarrow$ **no es REF**.",
               "justificacion_md": "Las entradas principales no se desplazan estrictamente a la derecha.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Algoritmo de reducción por filas",
          enunciado_md=(
              "El siguiente procedimiento lleva cualquier matriz a **REF** en pasos 1–4. Un quinto paso opcional la deja en **RREF**.\n\n"
              "1. **Columna pivote.** Elige la primera columna (desde la izquierda) que contenga alguna entrada no nula.\n"
              "2. **Seleccionar pivote.** Toma una entrada no nula como pivote; si es necesario, **intercambia filas** para moverla a la posición pivote (lo más arriba posible).\n"
              "3. **Crear ceros debajo.** Usa reemplazos $F_i \\leftarrow F_i + k\\,F_{\\text{pivote}}$ para anular todas las entradas **debajo** del pivote.\n"
              "4. **Cubrir y repetir.** Cubre la fila del pivote y aplica los pasos 1–3 a la submatriz restante. (Resultado: REF.)\n"
              "5. **(RREF, opcional)** Normaliza cada pivote a $1$ y, trabajando de **derecha a izquierda**, anula también las entradas **arriba** de cada pivote."
          ),
          demostracion_md=(
              "El paso 3 reduce el problema a una submatriz con una fila y una columna menos, así que el algoritmo termina en a lo sumo $\\min(m, n)$ iteraciones. La unicidad de la RREF (teorema previo) garantiza que las **posiciones pivote** son invariantes; pueden cambiar los valores intermedios pero no las columnas pivote."
          )),

        b("ejemplo_resuelto",
          titulo="De matriz aumentada a RREF (SCD)",
          problema_md=(
              "Resolver, vía reducción a RREF, $\\left[\\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\\\ 0 & 2 & -8 & 8 \\\\ -4 & 5 & 9 & -9 \\end{array}\\right]$."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1–3 (columna 1):** $F_3 \\leftarrow F_3 + 4F_1$ para anular el $-4$:\n\n"
                  "$\\left[\\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\\\ 0 & 2 & -8 & 8 \\\\ 0 & -3 & 13 & -9 \\end{array}\\right]$."
              ),
               "justificacion_md": "Pivote en $(1,1)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Columna 2** (submatriz inferior): $F_2 \\leftarrow \\tfrac{1}{2}F_2$ y luego $F_3 \\leftarrow F_3 + 3F_2$:\n\n"
                  "$\\left[\\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\\\ 0 & 1 & -4 & 4 \\\\ 0 & 0 & 1 & 3 \\end{array}\\right]$. **REF obtenida.**"
              ),
               "justificacion_md": "Pivotes en $(1,1), (2,2), (3,3)$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 5 (RREF):** anulamos arriba, de derecha a izquierda. $F_2 \\leftarrow F_2 + 4F_3$ y $F_1 \\leftarrow F_1 - F_3$:\n\n"
                  "$\\left[\\begin{array}{rrr|r} 1 & -2 & 0 & -3 \\\\ 0 & 1 & 0 & 16 \\\\ 0 & 0 & 1 & 3 \\end{array}\\right]$. "
                  "Luego $F_1 \\leftarrow F_1 + 2F_2$:\n\n"
                  "$\\left[\\begin{array}{rrr|r} 1 & 0 & 0 & 29 \\\\ 0 & 1 & 0 & 16 \\\\ 0 & 0 & 1 & 3 \\end{array}\\right]$."
              ),
               "justificacion_md": "RREF lograda.",
               "es_resultado": False},
              {"accion_md": (
                  "**Lectura:** $x_1 = 29,\\ x_2 = 16,\\ x_3 = 3$. **SCD.**\n\n"
                  "**Verificación:** $29 - 2(16) + 3 = 0$ ✓, $2(16) - 8(3) = 8$ ✓, $-4(29) + 5(16) + 9(3) = -9$ ✓."
              ),
               "justificacion_md": "La RREF muestra los $3$ pivotes en las $3$ columnas de $A$ $\\Rightarrow$ solución única.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Fila imposible (SI)",
          problema_md=(
              "Reducir y clasificar $\\left[\\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\\\ 2 & -4 & 2 & 1 \\\\ 1 & -2 & 1 & 0 \\end{array}\\right]$."
          ),
          pasos=[
              {"accion_md": (
                  "$F_2 \\leftarrow F_2 - 2F_1$ y $F_3 \\leftarrow F_3 - F_1$:\n\n"
                  "$\\left[\\begin{array}{rrr|r} 1 & -2 & 1 & 0 \\\\ 0 & 0 & 0 & 1 \\\\ 0 & 0 & 0 & 0 \\end{array}\\right]$."
              ),
               "justificacion_md": "Las filas $1$ y $3$ eran idénticas, por eso $F_3$ se anula.",
               "es_resultado": False},
              {"accion_md": (
                  "Aparece la fila $[\\,0\\ \\ 0\\ \\ 0 \\mid 1\\,]$ — equivale a $0 = 1$, **contradicción**.\n\n"
                  "**Conclusión: SI** (sistema incompatible)."
              ),
               "justificacion_md": "**Patrón:** una fila $[\\,0\\ \\cdots\\ 0 \\mid c\\,]$ con $c \\neq 0$ en la matriz aumentada $\\Leftrightarrow$ SI.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Dependencia entre ecuaciones (SCI)",
          problema_md=(
              "Reducir $\\left[\\begin{array}{rrr|r} 1 & -2 & 1 & -1 \\\\ 2 & -4 & 2 & -2 \\\\ -3 & 6 & -3 & 3 \\end{array}\\right]$."
          ),
          pasos=[
              {"accion_md": (
                  "$F_2 \\leftarrow F_2 - 2F_1$ y $F_3 \\leftarrow F_3 + 3F_1$:\n\n"
                  "$\\left[\\begin{array}{rrr|r} 1 & -2 & 1 & -1 \\\\ 0 & 0 & 0 & 0 \\\\ 0 & 0 & 0 & 0 \\end{array}\\right]$."
              ),
               "justificacion_md": "Las tres filas eran proporcionales (la 2ª y la 3ª eran múltiplos de la 1ª).",
               "es_resultado": False},
              {"accion_md": (
                  "Una sola ecuación efectiva: $x_1 - 2x_2 + x_3 = -1$. Hay **dos variables libres**: $x_2 = s$, $x_3 = t$ y $x_1 = 2s - t - 1$.\n\n"
                  "**Conjunto solución:** $\\{(2s - t - 1,\\ s,\\ t) : s, t \\in \\mathbb{R}\\}$. **SCI** con dos parámetros."
              ),
               "justificacion_md": "Dos columnas sin pivote $\\Rightarrow$ dos variables libres $\\Rightarrow$ infinitas soluciones.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Rango y criterio de Rouché–Frobenius",
          body_md=(
              "El **rango** de una matriz $A$, denotado $\\text{rango}(A)$, es el **número de pivotes** de su REF (equivalentemente, de su RREF). Por la unicidad de la RREF, este número está bien definido.\n\n"
              "**Teorema (Rouché–Frobenius).** Para el sistema $A\\vec{x} = \\vec{b}$ con $A \\in \\mathbb{R}^{m \\times n}$:\n\n"
              "$$\\boxed{\\text{El sistema es consistente} \\iff \\text{rango}(A) = \\text{rango}([A \\mid \\vec{b}]).}$$\n\n"
              "Si además es consistente:\n\n"
              "- $\\text{rango}(A) = n \\Rightarrow$ **solución única (SCD)**.\n"
              "- $\\text{rango}(A) < n \\Rightarrow$ **infinitas soluciones (SCI)**, con $n - \\text{rango}(A)$ **variables libres**.\n\n"
              "Si $\\text{rango}(A) < \\text{rango}([A\\mid\\vec{b}])$, hay alguna fila $[\\,0\\ \\cdots\\ 0\\mid c\\,]$ con $c \\neq 0$ y el sistema es **SI**."
          )),

        b("ejemplo_resuelto",
          titulo="Localizar columnas pivote",
          problema_md=(
              "Hallar las columnas pivote y el rango de $A = \\begin{bmatrix} 0 & -3 & -6 & 4 & 9 \\\\ -1 & -2 & -1 & 3 & 1 \\\\ -2 & -3 & 0 & 3 & -1 \\\\ 1 & 4 & 5 & -9 & -7 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": "**Intercambio** $F_1 \\leftrightarrow F_4$ para tener un pivote $1$ en $(1,1)$.",
               "justificacion_md": "Estrategia: evitar fracciones eligiendo bien el pivote.",
               "es_resultado": False},
              {"accion_md": "Eliminamos debajo del pivote de la columna $1$ con reemplazos en $F_2, F_3, F_4$. Luego pivote en columna $2$ y eliminamos debajo. La REF resultante tiene pivotes en columnas $1, 2$ y $4$ (la columna $3$ y la $5$ quedan sin pivote en su submatriz).",
               "justificacion_md": "Detalle: tras dos rondas se obtienen dos filas nulas; queda solo el pivote nuevo en la columna $4$.",
               "es_resultado": False},
              {"accion_md": "**Columnas pivote:** $\\{1, 2, 4\\}$. **Rango:** $\\text{rango}(A) = 3$.",
               "justificacion_md": "Las columnas $3$ y $5$ son **no pivote** $\\Rightarrow$ generarán variables libres en el sistema $A\\vec{x} = \\vec{b}$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál de las siguientes matrices está en RREF?",
                  "opciones_md": [
                      "$\\begin{bmatrix} 1 & 2 & 0 \\\\ 0 & 0 & 1 \\\\ 0 & 0 & 0 \\end{bmatrix}$",
                      "$\\begin{bmatrix} 2 & 0 & 1 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 0 \\end{bmatrix}$",
                      "$\\begin{bmatrix} 1 & 0 & 3 \\\\ 0 & 1 & 0 \\\\ 0 & 1 & 0 \\end{bmatrix}$",
                      "$\\begin{bmatrix} 0 & 1 & 0 \\\\ 1 & 0 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}$",
                  ],
                  "correcta": "A",
                  "pista_md": "Pivotes $= 1$, ceros arriba y abajo de cada pivote, escalonados estrictamente.",
                  "explicacion_md": "**(A) sí es RREF:** pivotes en $(1,1)$ y $(2,3)$, valen $1$, no hay pivote arriba/abajo en sus columnas. **(B)** falla porque el pivote $(1,1) = 2 \\neq 1$. **(C)** tiene dos filas con pivote en la misma columna. **(D)** no es siquiera REF.",
              },
              {
                  "enunciado_md": "Si $A \\in \\mathbb{R}^{4 \\times 6}$ y $\\text{rango}(A) = \\text{rango}([A\\mid\\vec{b}]) = 4$, el sistema $A\\vec{x} = \\vec{b}$:",
                  "opciones_md": [
                      "Es SI",
                      "Es SCD",
                      "Es SCI con $2$ variables libres",
                      "Es SCI con $4$ variables libres",
                  ],
                  "correcta": "C",
                  "pista_md": "Variables libres = $n - \\text{rango}(A)$.",
                  "explicacion_md": "Es **consistente** (rangos iguales). Como $\\text{rango}(A) = 4 < n = 6$, hay $n - \\text{rango}(A) = 2$ variables libres $\\Rightarrow$ SCI.",
              },
          ]),

        ej(
            "Reducir a REF y RREF",
            "Lleva $[A \\mid \\vec{b}] = \\left[\\begin{array}{rrr|r} 1 & 2 & -1 & 1 \\\\ 2 & 5 & -3 & 4 \\\\ 1 & 3 & -2 & 5 \\end{array}\\right]$ a REF y luego a RREF. Identifica columnas pivote y resuelve.",
            [
                "Empieza eliminando debajo del pivote $(1,1)$ con $F_2 \\leftarrow F_2 - 2F_1$ y $F_3 \\leftarrow F_3 - F_1$.",
                "Después busca el siguiente pivote en la columna $2$ de la submatriz.",
                "Para RREF, anula también arriba de cada pivote.",
            ],
            (
                "Tras $F_2 \\leftarrow F_2 - 2F_1$ y $F_3 \\leftarrow F_3 - F_1$:\n\n"
                "$\\left[\\begin{array}{rrr|r} 1 & 2 & -1 & 1 \\\\ 0 & 1 & -1 & 2 \\\\ 0 & 1 & -1 & 4 \\end{array}\\right]$.\n\n"
                "$F_3 \\leftarrow F_3 - F_2$:\n\n"
                "$\\left[\\begin{array}{rrr|r} 1 & 2 & -1 & 1 \\\\ 0 & 1 & -1 & 2 \\\\ 0 & 0 & 0 & 2 \\end{array}\\right]$.\n\n"
                "**Fila $[\\,0\\ 0\\ 0\\mid 2\\,]$:** contradicción $\\Rightarrow$ **SI** (incompatible). $\\text{rango}(A) = 2 < \\text{rango}([A\\mid\\vec{b}]) = 3$."
            ),
        ),

        ej(
            "Sistema $3 \\times 3$ con intercambio",
            "Reduce $\\left[\\begin{array}{rrr|r} 0 & 1 & -4 & 8 \\\\ 2 & -3 & 2 & 1 \\\\ 5 & -8 & 7 & 1 \\end{array}\\right]$ y clasifícalo.",
            [
                "Como $a_{11} = 0$, intercambia $F_1 \\leftrightarrow F_2$.",
                "Para eliminar el $5$ de $F_3$, conviene $F_3 \\leftarrow F_3 - \\tfrac{5}{2}F_1$.",
                "Continúa hasta REF. ¿Aparece alguna fila de la forma $[\\,0\\ 0\\ 0\\mid c\\,]$?",
            ],
            (
                "Tras intercambio $F_1 \\leftrightarrow F_2$:\n\n"
                "$\\left[\\begin{array}{rrr|r} 2 & -3 & 2 & 1 \\\\ 0 & 1 & -4 & 8 \\\\ 5 & -8 & 7 & 1 \\end{array}\\right]$. "
                "$F_3 \\leftarrow F_3 - \\tfrac{5}{2}F_1$ da $\\left[\\begin{array}{rrr|r} 2 & -3 & 2 & 1 \\\\ 0 & 1 & -4 & 8 \\\\ 0 & -\\tfrac{1}{2} & 2 & -\\tfrac{3}{2} \\end{array}\\right]$.\n\n"
                "$F_3 \\leftarrow F_3 + \\tfrac{1}{2}F_2$:\n\n"
                "$\\left[\\begin{array}{rrr|r} 2 & -3 & 2 & 1 \\\\ 0 & 1 & -4 & 8 \\\\ 0 & 0 & 0 & \\tfrac{5}{2} \\end{array}\\right]$.\n\n"
                "Última fila $\\equiv 0 = \\tfrac{5}{2}$: contradicción $\\Rightarrow$ **SI** (incompatible)."
            ),
        ),

        ej(
            "Matriz $4 \\times 5$: localizar pivotes",
            "Para $C = \\begin{bmatrix} 1 & 2 & 3 & 4 & 5 \\\\ 2 & 4 & 6 & 8 & 10 \\\\ 0 & 1 & 1 & 1 & 1 \\\\ 1 & 3 & 4 & 5 & 6 \\end{bmatrix}$, halla el rango y las columnas pivote.",
            [
                "$F_2 \\leftarrow F_2 - 2F_1$ anula totalmente la fila $2$.",
                "$F_4 \\leftarrow F_4 - F_1$ y luego $F_4 \\leftarrow F_4 - F_3$.",
            ],
            (
                "Tras OEF se llega a $\\begin{bmatrix} 1 & 2 & 3 & 4 & 5 \\\\ 0 & 1 & 1 & 1 & 1 \\\\ 0 & 0 & 0 & 0 & 0 \\\\ 0 & 0 & 0 & 0 & 0 \\end{bmatrix}$.\n\n"
                "**Columnas pivote:** $\\{1, 2\\}$. **Rango:** $2$.\n\n"
                "Las filas $3$ y $4$ originales eran combinaciones de las filas $1$ y $2$ (filas dependientes)."
            ),
        ),

        fig(
            "Diagrama horizontal con tres etapas de reducción por filas de una matriz aumentada 3x4, conectadas por flechas grandes. "
            "Etapa 1 (izquierda): matriz original con todos los coeficientes visibles. "
            "Etapa 2 (centro): forma escalonada (REF) con ceros debajo de la diagonal y los pivotes destacados como círculos rellenos en color ámbar #f59e0b. "
            "Etapa 3 (derecha): forma escalonada reducida (RREF) con pivotes anclados a 1 y ceros tanto arriba como abajo. "
            "Sobre cada flecha, anotaciones de la operación aplicada en color teal #06b6d4: 'F2 ← F2 - 2F1' y 'F3 ← F3 + F2'. "
            "Etiqueta inferior: 'REF → RREF'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Multiplicar una fila por $0$.** Está prohibido — eliminaría la información de esa ecuación.",
              "**Aplicar OEF a las columnas.** ¡No! Solo a las filas. Las operaciones de columna cambian el sistema.",
              "**Olvidar el signo del multiplicador** en $F_i \\leftarrow F_i + k F_j$. Para anular un $5$ debajo de un pivote $1$, hay que sumar $-5 F_{\\text{pivote}}$, no $+5$.",
              "**Confundir REF con RREF.** En REF basta tener ceros debajo del pivote. En RREF también arriba, y los pivotes deben valer $1$.",
              "**Detenerse al primer pivote raro.** Si aparece $\\tfrac{5}{2}$ o números feos, está bien: la RREF es única, pero el camino puede tener fracciones.",
              "**Olvidar que la columna del término independiente $\\vec{b}$ no cuenta como columna pivote para hallar variables libres.** Las variables libres se cuentan sobre las columnas de $A$.",
              "**Decir 'SI' cuando aparece una fila nula** $[\\,0\\ \\cdots\\ 0\\mid 0\\,]$. Una fila nula es una ecuación trivial $0 = 0$, **no** una contradicción.",
          ]),

        b("resumen",
          puntos_md=[
              "**Tres OEF:** reemplazo, intercambio, escalamiento — preservan el conjunto solución.",
              "**REF:** pivotes escalonados a la derecha, ceros debajo. **RREF:** además pivotes $= 1$ y ceros arriba.",
              "**Algoritmo en 5 pasos:** elegir columna pivote, mover pivote, anular debajo, repetir, normalizar (paso opcional).",
              "**Unicidad de la RREF:** las posiciones pivote son invariantes; $\\text{rango}(A) = $ número de pivotes.",
              "**Rouché–Frobenius:** consistente $\\iff \\text{rango}(A) = \\text{rango}([A\\mid\\vec{b}])$.",
              "**SCD:** $\\text{rango}(A) = n$. **SCI:** $\\text{rango}(A) < n$. **SI:** rangos distintos (fila $[\\,0\\cdots 0\\mid c\\,], c \\neq 0$).",
              "**Próxima lección:** los conceptos de $\\text{Gen}\\{a_i\\}$, columnas y la noción de **independencia lineal**.",
          ]),
    ]
    return {
        "id": "lec-al-2-2-reduccion-filas",
        "title": "Reducción por filas",
        "description": "Operaciones elementales, REF y RREF, algoritmo de Gauss–Jordan, pivotes, rango y Rouché–Frobenius.",
        "blocks": blocks,
        "duration_minutes": 65,
        "order": 2,
    }


# =====================================================================
# 2.3 Independencia lineal
# =====================================================================
def lesson_2_3():
    blocks = [
        b("texto", body_md=(
            "En esta lección unimos dos lenguajes: el de **vectores** (combinaciones lineales, conjunto generado) "
            "y el de **sistemas** (matriz $A$, ecuación $A\\vec{x} = \\vec{b}$). El puente es la observación clave de que "
            "$A\\vec{x}$ es una **combinación lineal de las columnas de $A$**.\n\n"
            "Con esto definimos el concepto central de **independencia lineal** y damos criterios prácticos para "
            "decidir si un conjunto de vectores es **LI** o **LD** mediante reducción por filas. Veremos también "
            "cuatro **atajos** ($T_1$–$T_4$) para evitar reducir cuando una respuesta rápida es posible.\n\n"
            "Estos conceptos son los cimientos del capítulo $5$ (espacios vectoriales, bases, dimensión)."
        )),

        b("definicion",
          titulo="Combinación lineal y conjunto generado (Gen)",
          body_md=(
              "Sean $\\vec{v}_1, \\ldots, \\vec{v}_p \\in \\mathbb{R}^n$ y $c_1, \\ldots, c_p \\in \\mathbb{R}$. El vector\n\n"
              "$$\\vec{y} = c_1 \\vec{v}_1 + c_2 \\vec{v}_2 + \\cdots + c_p \\vec{v}_p$$\n\n"
              "se llama **combinación lineal** de $\\vec{v}_1, \\ldots, \\vec{v}_p$ con **pesos** $c_1, \\ldots, c_p$.\n\n"
              "El **conjunto generado** (o **gen**) es el conjunto de **todas** las combinaciones lineales posibles:\n\n"
              "$$\\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\} = \\Bigl\\{ \\sum_{i=1}^{p} c_i \\vec{v}_i : c_i \\in \\mathbb{R} \\Bigr\\}.$$\n\n"
              "**Observaciones.**\n\n"
              "- $\\vec{0}$ siempre pertenece al gen (toma todos los $c_i = 0$).\n"
              "- Si $p = 1$ y $\\vec{v} \\neq \\vec{0}$, el gen es una **recta** por el origen.\n"
              "- Si $p = 2$ con $\\vec{v}_1, \\vec{v}_2$ no colineales, es un **plano** por el origen."
          )),

        b("ejemplo_resuelto",
          titulo="Resolver pesos en $\\mathbb{R}^2$",
          problema_md=(
              "Sean $\\vec{v}_1 = \\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix}$, $\\vec{v}_2 = \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}$, $\\vec{u} = \\begin{bmatrix} 3 \\\\ 2 \\end{bmatrix}$. Halla $c_1, c_2$ con $\\vec{u} = c_1 \\vec{v}_1 + c_2 \\vec{v}_2$."
          ),
          pasos=[
              {"accion_md": (
                  "La igualdad vectorial $c_1(-1, 1) + c_2(2, 1) = (3, 2)$ equivale al sistema "
                  "$\\begin{cases} -c_1 + 2c_2 = 3 \\\\ \\phantom{-}c_1 + \\phantom{2}c_2 = 2 \\end{cases}$."
              ),
               "justificacion_md": "Cada componente da una ecuación.",
               "es_resultado": False},
              {"accion_md": (
                  "Sumando: $3c_2 = 5 \\Rightarrow c_2 = \\tfrac{5}{3}$. Luego $c_1 = 2 - c_2 = \\tfrac{1}{3}$.\n\n"
                  "**Comprobación:** $\\tfrac{1}{3}(-1, 1) + \\tfrac{5}{3}(2, 1) = (3, 2)$ ✓."
              ),
               "justificacion_md": "**$\\vec{u} \\in \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\}$** y la combinación es única (las columnas son LI, como veremos).",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Ecuación vectorial y matricial",
          body_md=(
              "Sean $\\vec{a}_1, \\ldots, \\vec{a}_n \\in \\mathbb{R}^m$ y $\\vec{b} \\in \\mathbb{R}^m$. La **ecuación vectorial**\n\n"
              "$$x_1 \\vec{a}_1 + x_2 \\vec{a}_2 + \\cdots + x_n \\vec{a}_n = \\vec{b}$$\n\n"
              "tiene **el mismo conjunto solución** que el sistema matricial $A \\vec{x} = \\vec{b}$, donde\n\n"
              "$$A = \\begin{bmatrix} \\vec{a}_1 & \\vec{a}_2 & \\cdots & \\vec{a}_n \\end{bmatrix} \\in \\mathbb{R}^{m \\times n}.$$\n\n"
              "**Consecuencia clave:** $\\vec{b} \\in \\text{Gen}\\{\\vec{a}_1, \\ldots, \\vec{a}_n\\} \\iff A\\vec{x} = \\vec{b}$ es **consistente**.\n\n"
              "El conjunto $\\text{Gen}\\{\\vec{a}_1, \\ldots, \\vec{a}_n\\}$ se denota también $\\text{Col}(A)$ y se llama **espacio columna** de $A$ (lo veremos en cap. 5)."
          )),

        b("definicion",
          titulo="Producto matriz–vector $A\\vec{x}$",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{m \\times n}$ con columnas $\\vec{a}_1, \\ldots, \\vec{a}_n$ y $\\vec{x} \\in \\mathbb{R}^n$. El **producto matriz–vector** se define como\n\n"
              "$$A\\vec{x} = \\begin{bmatrix} \\vec{a}_1 & \\cdots & \\vec{a}_n \\end{bmatrix} \\begin{bmatrix} x_1 \\\\ \\vdots \\\\ x_n \\end{bmatrix} = x_1 \\vec{a}_1 + x_2 \\vec{a}_2 + \\cdots + x_n \\vec{a}_n.$$\n\n"
              "Es decir, **$A\\vec{x}$ es la combinación lineal de las columnas de $A$ con pesos dados por las entradas de $\\vec{x}$**. Esta visión 'por columnas' es la más útil conceptualmente.\n\n"
              "**Propiedades (linealidad).** Para $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$ y $c \\in \\mathbb{R}$:\n\n"
              "$$A(\\vec{u} + \\vec{v}) = A\\vec{u} + A\\vec{v}, \\qquad A(c\\vec{u}) = c(A\\vec{u}).$$"
          )),

        b("ejemplo_resuelto",
          titulo="$A\\vec{x}$ como combinación de columnas",
          problema_md=(
              "Calcula $A\\vec{x}$ para $A = \\begin{bmatrix} 1 & 2 & -1 \\\\ 0 & -5 & 3 \\end{bmatrix}$ y $\\vec{x} = \\begin{bmatrix} 4 \\\\ 3 \\\\ 7 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A\\vec{x} = 4 \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix} + 3 \\begin{bmatrix} 2 \\\\ -5 \\end{bmatrix} + 7 \\begin{bmatrix} -1 \\\\ 3 \\end{bmatrix}$."
              ),
               "justificacion_md": "Los pesos son las entradas de $\\vec{x}$; los vectores, las columnas de $A$.",
               "es_resultado": False},
              {"accion_md": (
                  "$= \\begin{bmatrix} 4 \\\\ 0 \\end{bmatrix} + \\begin{bmatrix} 6 \\\\ -15 \\end{bmatrix} + \\begin{bmatrix} -7 \\\\ 21 \\end{bmatrix} = \\begin{bmatrix} 3 \\\\ 6 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Sumamos componente a componente.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Equivalencias para $A \\in \\mathbb{R}^{m \\times n}$.** Las siguientes afirmaciones son equivalentes:\n\n"
              "1. Para **cada** $\\vec{b} \\in \\mathbb{R}^m$, $A\\vec{x} = \\vec{b}$ tiene solución.\n"
              "2. $\\text{Gen}\\{\\vec{a}_1, \\ldots, \\vec{a}_n\\} = \\mathbb{R}^m$ (las columnas generan todo $\\mathbb{R}^m$).\n"
              "3. $A$ tiene una **posición pivote en cada fila** (al menos $m$ pivotes; $\\text{rango}(A) = m$)."
          )),

        b("definicion",
          titulo="Independencia lineal (LI / LD)",
          body_md=(
              "Un conjunto indexado $\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\} \\subset \\mathbb{R}^n$ es **linealmente independiente** (LI) si la ecuación vectorial\n\n"
              "$$x_1 \\vec{v}_1 + x_2 \\vec{v}_2 + \\cdots + x_p \\vec{v}_p = \\vec{0}$$\n\n"
              "tiene **únicamente** la **solución trivial** $x_1 = \\cdots = x_p = 0$.\n\n"
              "Es **linealmente dependiente** (LD) si existen pesos $c_1, \\ldots, c_p$ **no todos cero** tales que $c_1 \\vec{v}_1 + \\cdots + c_p \\vec{v}_p = \\vec{0}$. Esa igualdad se llama **relación de dependencia**.\n\n"
              "**Idea:** un conjunto es LD si **algún vector es 'redundante'** (combinación lineal de los demás)."
          )),

        b("teorema",
          enunciado_md=(
              "**Independencia lineal de las columnas de una matriz.** Sea $A = [\\,\\vec{a}_1\\ \\cdots\\ \\vec{a}_n\\,] \\in \\mathbb{R}^{m \\times n}$. Las siguientes afirmaciones son equivalentes:\n\n"
              "1. Las columnas de $A$ son **LI**.\n"
              "2. La ecuación homogénea $A\\vec{x} = \\vec{0}$ tiene **solo** la solución trivial $\\vec{x} = \\vec{0}$.\n"
              "3. En la RREF de $A$ hay un **pivote en cada columna** ($\\text{rango}(A) = n$).\n\n"
              "**Por qué importa la condición 3:** convierte una pregunta abstracta ('¿son independientes?') en un cómputo mecánico (reducir por filas y contar pivotes)."
          )),

        b("ejemplo_resuelto",
          titulo="¿LI o LD? y relación de dependencia",
          problema_md=(
              "Sean $\\vec{v}_1 = (1, 2, 3)^T$, $\\vec{v}_2 = (4, 5, 6)^T$, $\\vec{v}_3 = (2, 1, 0)^T$. Determinar si $\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3\\}$ es LI; si es LD, dar una relación."
          ),
          pasos=[
              {"accion_md": (
                  "Formamos $A = \\begin{bmatrix} 1 & 4 & 2 \\\\ 2 & 5 & 1 \\\\ 3 & 6 & 0 \\end{bmatrix}$ y resolvemos $A\\vec{x} = \\vec{0}$ por reducción:\n\n"
                  "$\\begin{bmatrix} 1 & 4 & 2 \\\\ 2 & 5 & 1 \\\\ 3 & 6 & 0 \\end{bmatrix} \\sim \\begin{bmatrix} 1 & 4 & 2 \\\\ 0 & -3 & -3 \\\\ 0 & -6 & -6 \\end{bmatrix} \\sim \\begin{bmatrix} 1 & 4 & 2 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 0 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Solo $2$ pivotes en $3$ columnas $\\Rightarrow$ hay $1$ variable libre $\\Rightarrow$ infinitas soluciones no triviales $\\Rightarrow$ **LD**.",
               "es_resultado": False},
              {"accion_md": (
                  "Pivotes en columnas $1, 2$; $x_3$ libre. De la 2ª ecuación reducida: $x_2 = -x_3$. De la 1ª: $x_1 = -4x_2 - 2x_3 = -4(-x_3) - 2x_3 = 2x_3$. Tomando $x_3 = 1$: $\\vec{x} = (2, -1, 1)^T$.\n\n"
                  "**Relación de dependencia:** $2\\vec{v}_1 - \\vec{v}_2 + \\vec{v}_3 = \\vec{0}$, equivalente a $\\vec{v}_3 = -2\\vec{v}_1 + \\vec{v}_2$ (es decir, $\\vec{v}_3$ es 'redundante')."
              ),
               "justificacion_md": "**Lección:** la dependencia lineal se traduce en una expresión explícita de un vector como combinación de los demás.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Atajos para detectar dependencia",
          enunciado_md=(
              "Sea $S = \\{\\vec{v}_1, \\ldots, \\vec{v}_p\\} \\subset \\mathbb{R}^n$.\n\n"
              "**T1 (dos vectores):** $\\{\\vec{v}_1, \\vec{v}_2\\}$ es LD $\\iff$ uno es **múltiplo escalar** del otro.\n\n"
              "**T2 (más vectores que entradas):** si $p > n$, entonces $S$ es **LD**. (No puede haber más de $n$ vectores LI en $\\mathbb{R}^n$.)\n\n"
              "**T3 (contiene al cero):** si $\\vec{0} \\in S$, entonces $S$ es **LD**.\n\n"
              "**T4 (relación con el gen):** si $\\vec{u}, \\vec{v}$ son no nulos y no múltiplos, entonces $\\vec{w} \\in \\text{Gen}\\{\\vec{u}, \\vec{v}\\} \\iff \\{\\vec{u}, \\vec{v}, \\vec{w}\\}$ es LD."
          ),
          demostracion_md=(
              "**T1:** $c_1 \\vec{v}_1 + c_2 \\vec{v}_2 = \\vec{0}$ no trivial $\\iff \\vec{v}_1 = -\\tfrac{c_2}{c_1}\\vec{v}_2$ (suponiendo $c_1 \\neq 0$).\n\n"
              "**T2:** $A = [\\vec{v}_1\\ \\cdots\\ \\vec{v}_p] \\in \\mathbb{R}^{n \\times p}$ tiene a lo sumo $\\min(n, p) = n$ pivotes; como $p > n$, alguna columna no es pivote $\\Rightarrow$ hay variable libre $\\Rightarrow$ LD.\n\n"
              "**T3:** $1 \\cdot \\vec{0} + 0 \\cdot \\vec{v}_2 + \\cdots + 0 \\cdot \\vec{v}_p = \\vec{0}$ es relación no trivial.\n\n"
              "**T4:** si $\\vec{w} = a\\vec{u} + b\\vec{v}$, entonces $a\\vec{u} + b\\vec{v} - \\vec{w} = \\vec{0}$ es relación no trivial; recíproco análogo. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Aplicación de T2 (más vectores que entradas)",
          problema_md=(
              "Decidir si $S = \\left\\{ (1,0)^T, (0,1)^T, (1,1)^T \\right\\} \\subset \\mathbb{R}^2$ es LI."
          ),
          pasos=[
              {"accion_md": "$p = 3$ vectores en $\\mathbb{R}^2$ ($n = 2$). Como $p > n$, por **T2** el conjunto es **LD**.",
               "justificacion_md": "Sin necesidad de reducir.",
               "es_resultado": False},
              {"accion_md": (
                  "**Relación explícita:** $(1, 0) + (0, 1) - (1, 1) = (0, 0)$, es decir, $(1, 1) = (1, 0) + (0, 1)$."
              ),
               "justificacion_md": "El 'tercer vector' es siempre redundante en $\\mathbb{R}^2$ con dos vectores LI ya presentes.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "$A\\vec{x}$ donde $A \\in \\mathbb{R}^{m \\times n}$ y $\\vec{x} \\in \\mathbb{R}^n$ es:",
                  "opciones_md": [
                      "Una combinación lineal de las **filas** de $A$",
                      "Una combinación lineal de las **columnas** de $A$, con pesos $x_i$",
                      "Un escalar",
                      "Una matriz $m \\times n$",
                  ],
                  "correcta": "B",
                  "pista_md": "$A\\vec{x} = x_1 \\vec{a}_1 + \\cdots + x_n \\vec{a}_n$.",
                  "explicacion_md": "**$A\\vec{x}$ es la combinación lineal de las columnas $\\vec{a}_1, \\ldots, \\vec{a}_n$** con pesos $x_1, \\ldots, x_n$. Es un vector en $\\mathbb{R}^m$.",
              },
              {
                  "enunciado_md": "$\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3, \\vec{v}_4, \\vec{v}_5\\} \\subset \\mathbb{R}^3$ es:",
                  "opciones_md": [
                      "Siempre LI",
                      "Siempre LD",
                      "Depende de los vectores",
                      "Solo si contiene al $\\vec{0}$",
                  ],
                  "correcta": "B",
                  "pista_md": "$p = 5 > 3 = n$.",
                  "explicacion_md": "Por **T2** (más vectores que entradas), $5 > 3$ implica LD automáticamente, sin importar qué vectores específicos sean.",
              },
              {
                  "enunciado_md": "Las columnas de $A$ son LI $\\iff$ ¿qué tiene que pasar con la RREF?",
                  "opciones_md": [
                      "Hay un pivote en cada fila",
                      "Hay un pivote en cada columna",
                      "Hay $0$ pivotes",
                      "La última fila es nula",
                  ],
                  "correcta": "B",
                  "pista_md": "$A\\vec{x} = \\vec{0}$ debe tener solo la solución trivial.",
                  "explicacion_md": "**Pivote en cada columna** $\\iff$ no hay variables libres $\\iff$ $A\\vec{x} = \\vec{0}$ tiene solo $\\vec{x} = \\vec{0}$ $\\iff$ columnas LI.",
              },
          ]),

        ej(
            "Pertenencia al gen",
            "¿Pertenece $\\vec{w} = (1, 0, 2)^T$ a $\\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\}$ con $\\vec{v}_1 = (1, 1, 0)^T$ y $\\vec{v}_2 = (0, 1, 1)^T$?",
            [
                "Resuelve $a\\vec{v}_1 + b\\vec{v}_2 = \\vec{w}$ por reducción.",
                "Equivale a estudiar la consistencia de $[\\vec{v}_1\\ \\vec{v}_2 \\mid \\vec{w}]$.",
            ],
            (
                "El sistema $a(1,1,0) + b(0,1,1) = (1,0,2)$ equivale a $\\begin{cases} a = 1 \\\\ a + b = 0 \\\\ b = 2 \\end{cases}$, "
                "luego $a = 1$, $b = 2$, pero entonces $a + b = 3 \\neq 0$. **Inconsistente.**\n\n"
                "**Conclusión:** $\\vec{w} \\notin \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\}$."
            ),
        ),

        ej(
            "Consistencia para todo $\\vec{b}$",
            "Para $A = \\begin{bmatrix} 1 & 3 & 4 \\\\ -4 & 2 & -6 \\\\ -3 & -2 & -7 \\end{bmatrix}$, ¿es $A\\vec{x} = \\vec{b}$ consistente para **todo** $\\vec{b} \\in \\mathbb{R}^3$?",
            [
                "Reduce $A$ por filas (sin importar $\\vec{b}$).",
                "Aplica el teorema: hay solución para todo $\\vec{b}$ $\\iff$ pivote en cada fila.",
            ],
            (
                "Reduciendo: $A \\sim \\begin{bmatrix} 1 & 3 & 4 \\\\ 0 & 14 & 10 \\\\ 0 & 0 & 0 \\end{bmatrix}$.\n\n"
                "Solo $2$ pivotes en $3$ filas $\\Rightarrow$ falta pivote en la fila $3$ $\\Rightarrow$ las columnas **no generan** todo $\\mathbb{R}^3$ $\\Rightarrow$ existe algún $\\vec{b}$ para el cual $A\\vec{x} = \\vec{b}$ es **inconsistente**."
            ),
        ),

        ej(
            "Determinar LI/LD usando RREF",
            "Decide si las columnas de $A = \\begin{bmatrix} 0 & 1 & 4 \\\\ 1 & 2 & -1 \\\\ 5 & 8 & 0 \\end{bmatrix}$ son LI.",
            [
                "Reduce y cuenta pivotes en columnas.",
                "Conviene intercambiar $F_1 \\leftrightarrow F_2$ primero.",
            ],
            (
                "$A \\sim \\begin{bmatrix} 1 & 2 & -1 \\\\ 0 & 1 & 4 \\\\ 0 & -2 & 5 \\end{bmatrix} \\sim \\begin{bmatrix} 1 & 2 & -1 \\\\ 0 & 1 & 4 \\\\ 0 & 0 & 13 \\end{bmatrix}$.\n\n"
                "**Pivote en cada columna** ($1, 2, 3$) $\\Rightarrow$ **columnas LI**. La única solución de $A\\vec{x} = \\vec{0}$ es $\\vec{x} = \\vec{0}$."
            ),
        ),

        ej(
            "Atajo T4",
            "Sean $\\vec{u} = (3, 1, 0)^T$, $\\vec{v} = (1, 6, 0)^T$, $\\vec{w} = (10, 8, 0)^T$. Explica por qué $\\vec{w} \\in \\text{Gen}\\{\\vec{u}, \\vec{v}\\}$ y, por T4, $\\{\\vec{u}, \\vec{v}, \\vec{w}\\}$ es LD.",
            [
                "Resuelve $a\\vec{u} + b\\vec{v} = \\vec{w}$ por las dos primeras componentes.",
                "Para T4 escribe la relación de dependencia explícita.",
            ],
            (
                "Las 2 primeras coordenadas dan $\\begin{cases} 3a + b = 10 \\\\ a + 6b = 8 \\end{cases}$, con solución $a = 3$, $b = 1$. La 3ª coordenada se cumple ($0 = 0$).\n\n"
                "Luego $\\vec{w} = 3\\vec{u} + \\vec{v}$, y por **T4**, $3\\vec{u} + \\vec{v} - \\vec{w} = \\vec{0}$ es relación no trivial $\\Rightarrow \\{\\vec{u}, \\vec{v}, \\vec{w}\\}$ es **LD**."
            ),
        ),

        fig(
            "Dos paneles lado a lado en el plano cartesiano R^2 ilustrando independencia versus dependencia lineal. "
            "Panel izquierdo (LI): tres vectores en color teal #06b6d4 partiendo del origen, apuntando en direcciones claramente distintas y no colineales, con una nube de puntos de fondo sugiriendo que sus combinaciones lineales llenan todo el plano. Etiqueta: 'Linealmente independientes — generan R^2'. "
            "Panel derecho (LD): tres vectores colineales sobre una misma recta diagonal; dos en teal #06b6d4 y uno destacado en color ámbar #f59e0b marcado como 'redundante = 2v1 + v2'. Etiqueta: 'Linealmente dependientes'. "
            "Ejes simples con flechas y notación $\\vec{v}_1, \\vec{v}_2, \\vec{v}_3$. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Decir 'LD' cuando no se ha encontrado relación.** No es suficiente sospechar — hay que **probar** que existe una relación no trivial (vía reducción).",
              "**Olvidar que T2 ($p > n \\Rightarrow$ LD) es una **implicación**, no una equivalencia.** $p \\leq n$ no garantiza LI.",
              "**Confundir 'gen' con 'igual a $\\mathbb{R}^n$'.** $\\text{Gen}\\{\\vec{v}\\}$ es solo una recta — generar todo $\\mathbb{R}^n$ requiere al menos $n$ vectores LI.",
              "**Pensar que $A\\vec{x}$ es 'matriz por vector' fila por columna.** Algorítmicamente sí, pero la interpretación útil es **combinación lineal de columnas**.",
              "**No verificar que $\\vec{u}, \\vec{v}$ son no nulos y no múltiplos** antes de aplicar T4 — la equivalencia falla si lo son.",
              "**Mezclar 'consistente para todo $\\vec{b}$' (pivote en cada fila) con 'columnas LI' (pivote en cada columna).** Son condiciones distintas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Combinación lineal:** $\\sum c_i \\vec{v}_i$. **Gen:** todas las combinaciones lineales posibles.",
              "**Ecuación vectorial $\\equiv$ matricial:** $x_1\\vec{a}_1 + \\cdots + x_n\\vec{a}_n = \\vec{b} \\iff A\\vec{x} = \\vec{b}$.",
              "**$A\\vec{x}$:** combinación lineal de las **columnas** de $A$ con pesos dados por $\\vec{x}$.",
              "**LI:** $A\\vec{x} = \\vec{0}$ solo tiene la solución trivial $\\iff$ pivote en **cada columna** de $A$.",
              "**LD:** existe relación no trivial; algún vector es combinación lineal de los demás.",
              "**Atajos:** T1 (2 vectores: múltiplos $\\Rightarrow$ LD), T2 ($p > n \\Rightarrow$ LD), T3 ($\\vec{0} \\in S \\Rightarrow$ LD), T4 (pertenencia al gen $\\Leftrightarrow$ LD del conjunto extendido).",
              "**Próxima lección:** describir explícitamente el conjunto solución (parametrización, forma vectorial, núcleo).",
          ]),
    ]
    return {
        "id": "lec-al-2-3-independencia-lineal",
        "title": "Independencia lineal",
        "description": "Combinación lineal y gen, ecuación vectorial vs matricial, $A\\vec{x}$ por columnas, independencia lineal y atajos.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
    }


# =====================================================================
# 2.4 Conjunto solución
# =====================================================================
def lesson_2_4():
    blocks = [
        b("texto", body_md=(
            "Esta lección une todo lo anterior: dada la **RREF** de $[A \\mid \\vec{b}]$, queremos describir "
            "**explícitamente** el conjunto solución de $A\\vec{x} = \\vec{b}$, no solo decir 'es SCD/SCI/SI'.\n\n"
            "Veremos:\n\n"
            "- Cómo identificar **variables básicas** (asociadas a columnas pivote) y **variables libres** (columnas sin pivote).\n"
            "- Cómo escribir la solución en forma **paramétrica** y en forma **vectorial** $\\vec{x} = \\vec{x}_p + t_1 \\vec{v}^{(1)} + \\cdots + t_k \\vec{v}^{(k)}$.\n"
            "- La descomposición fundamental $\\vec{x} = \\vec{x}_p + \\mathcal{N}(A)$, donde $\\mathcal{N}(A) = \\{\\vec{x}: A\\vec{x} = \\vec{0}\\}$ es el **núcleo** de $A$.\n"
            "- El caso especial de **sistemas homogéneos** $A\\vec{x} = \\vec{0}$.\n\n"
            "Esta descomposición es la primera aparición del concepto de **subespacio** y conecta directamente con el cap. 5."
        )),

        b("definicion",
          titulo="Variables básicas y variables libres",
          body_md=(
              "Sea $[A \\mid \\vec{b}]$ y su RREF. Las columnas pivote **de $A$** (no del $\\vec{b}$) determinan:\n\n"
              "- **Variables básicas:** las $x_{j_1}, \\ldots, x_{j_r}$ asociadas a las **columnas pivote** de $A$.\n"
              "- **Variables libres:** las $x_{k_1}, \\ldots, x_{k_{n-r}}$ asociadas a las **columnas sin pivote** de $A$.\n\n"
              "El **número de variables libres** es $n - \\text{rango}(A)$.\n\n"
              "**Inconsistencia.** Si la RREF tiene una fila $[\\,0\\ \\cdots\\ 0 \\mid c\\,]$ con $c \\neq 0$, el sistema es **incompatible** y el conjunto solución es $\\emptyset$ — no se habla de variables libres."
          )),

        b("teorema",
          nombre="Existencia y unicidad",
          enunciado_md=(
              "Sea $A\\vec{x} = \\vec{b}$ con $A \\in \\mathbb{R}^{m \\times n}$.\n\n"
              "**(a) Consistencia.** El sistema es consistente $\\iff$ la última columna de $[A\\mid\\vec{b}]$ **no es columna pivote** $\\iff$ no aparece fila $[\\,0\\ \\cdots\\ 0\\mid c\\,]$ con $c \\neq 0$.\n\n"
              "**(b) Si es consistente:**\n\n"
              "- **Solución única (SCD)** $\\iff$ $A$ tiene pivote en **todas** sus $n$ columnas (no hay variables libres).\n"
              "- **Infinitas soluciones (SCI)** $\\iff$ existe al menos **una** variable libre.\n\n"
              "**Equivalencia útil:** SCD $\\iff \\text{rango}(A) = n$ y consistente."
          )),

        b("teorema",
          enunciado_md=(
              "**Procedimiento para describir el conjunto solución (caso consistente).**\n\n"
              "1. Forma $[A \\mid \\vec{b}]$ y reduce a RREF. Si aparece una fila imposible, **detente: es SI**.\n"
              "2. Asigna **parámetros** a las variables libres ($x_{k_\\ell} = t_\\ell$).\n"
              "3. Despeja cada variable básica en términos de los parámetros.\n"
              "4. Escribe la solución en forma **paramétrica** o **vectorial**:\n\n"
              "$$\\vec{x} = \\vec{x}_p + t_1 \\vec{v}^{(1)} + \\cdots + t_{n-r} \\vec{v}^{(n-r)},$$\n\n"
              "donde $\\vec{x}_p$ se obtiene poniendo todos los parámetros en $0$ y los $\\vec{v}^{(\\ell)}$ son los **vectores dirección** asociados a cada parámetro."
          )),

        b("ejemplo_resuelto",
          titulo="SCI con una variable libre",
          problema_md=(
              "Describir el conjunto solución a partir de la RREF $\\left[\\begin{array}{rrr|r} 1 & 0 & -5 & 1 \\\\ 0 & 1 & 1 & 4 \\\\ 0 & 0 & 0 & 0 \\end{array}\\right]$."
          ),
          pasos=[
              {"accion_md": (
                  "**Pivotes en columnas $1, 2$** $\\Rightarrow$ básicas $x_1, x_2$. Columna $3$ sin pivote $\\Rightarrow$ libre $x_3 = t$. La fila $0 = 0$ no aporta."
              ),
               "justificacion_md": "El sistema es consistente (no hay fila imposible).",
               "es_resultado": False},
              {"accion_md": (
                  "Lectura directa: $x_1 = 1 + 5t$, $x_2 = 4 - t$, $x_3 = t$. **Forma paramétrica:**\n\n"
                  "$\\{(1 + 5t,\\ 4 - t,\\ t) : t \\in \\mathbb{R}\\}.$"
              ),
               "justificacion_md": "Despejamos $x_1$ y $x_2$ desde la RREF.",
               "es_resultado": False},
              {"accion_md": (
                  "**Forma vectorial:**\n\n"
                  "$\\vec{x} = \\underbrace{\\begin{bmatrix} 1 \\\\ 4 \\\\ 0 \\end{bmatrix}}_{\\vec{x}_p} + t \\underbrace{\\begin{bmatrix} 5 \\\\ -1 \\\\ 1 \\end{bmatrix}}_{\\vec{v}^{(1)}}, \\quad t \\in \\mathbb{R}.$\n\n"
                  "**Geometría:** una **recta** en $\\mathbb{R}^3$ que pasa por $\\vec{x}_p = (1, 4, 0)$ con dirección $\\vec{v}^{(1)} = (5, -1, 1)$."
              ),
               "justificacion_md": "$\\vec{x}_p$: poner $t = 0$. $\\vec{v}^{(1)}$: derivar respecto al parámetro.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Dos variables libres y una ecuación fija",
          problema_md=(
              "Describir el conjunto solución de $\\left[\\begin{array}{rrrrr|r} 1 & 6 & 0 & 3 & 0 & 0 \\\\ 0 & 0 & 1 & -4 & 0 & 5 \\\\ 0 & 0 & 0 & 0 & 1 & 7 \\end{array}\\right]$."
          ),
          pasos=[
              {"accion_md": (
                  "Pivotes en columnas $\\{1, 3, 5\\}$ $\\Rightarrow$ básicas $x_1, x_3, x_5$. Libres: $x_2 = s$, $x_4 = t$.\n\n"
                  "De las filas: $x_1 = -6s - 3t$, $x_3 = 5 + 4t$, $x_5 = 7$."
              ),
               "justificacion_md": "Cada fila no nula determina una variable básica.",
               "es_resultado": False},
              {"accion_md": (
                  "**Forma vectorial:**\n\n"
                  "$\\vec{x} = \\begin{bmatrix} 0 \\\\ 0 \\\\ 5 \\\\ 0 \\\\ 7 \\end{bmatrix} + s \\begin{bmatrix} -6 \\\\ 1 \\\\ 0 \\\\ 0 \\\\ 0 \\end{bmatrix} + t \\begin{bmatrix} -3 \\\\ 0 \\\\ 4 \\\\ 1 \\\\ 0 \\end{bmatrix}, \\quad s, t \\in \\mathbb{R}.$"
              ),
               "justificacion_md": "$\\vec{x}_p$ con $s = t = 0$. Las direcciones $\\vec{v}^{(1)}, \\vec{v}^{(2)}$ son las derivadas respecto a $s$ y $t$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación rápida:** $x_5 = 7$ siempre — efectivamente las terceras componentes de $\\vec{v}^{(1)}, \\vec{v}^{(2)}$ son $0$ y la 5ª es $0$ también. ✓\n\n"
                  "**Geometría:** un **plano afín** en $\\mathbb{R}^5$ (2 parámetros)."
              ),
               "justificacion_md": "Cada parámetro adicional añade una 'dimensión' al objeto solución.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Sistema homogéneo y núcleo",
          body_md=(
              "Un sistema es **homogéneo** si tiene la forma $A\\vec{x} = \\vec{0}$. Siempre tiene al menos la **solución trivial** $\\vec{x} = \\vec{0}$.\n\n"
              "El conjunto de soluciones se denota\n\n"
              "$$\\mathcal{N}(A) = \\{\\vec{x} \\in \\mathbb{R}^n : A\\vec{x} = \\vec{0}\\}$$\n\n"
              "y se llama **núcleo** (o **espacio nulo**) de $A$.\n\n"
              "**Hecho clave.** $A\\vec{x} = \\vec{0}$ tiene una solución **no trivial** $\\iff$ el sistema tiene **al menos una variable libre** $\\iff \\text{rango}(A) < n$.\n\n"
              "**Corolario.** Si $A$ tiene **más columnas que filas** ($n > m$), $A\\vec{x} = \\vec{0}$ siempre tiene soluciones no triviales (no puede haber pivote en cada columna)."
          )),

        b("ejemplo_resuelto",
          titulo="Sistema homogéneo con solución no trivial",
          problema_md=(
              "Resolver $\\begin{cases} 3x_1 + 5x_2 - 4x_3 = 0 \\\\ -3x_1 - 2x_2 + 4x_3 = 0 \\\\ 6x_1 + x_2 - 8x_3 = 0 \\end{cases}$."
          ),
          pasos=[
              {"accion_md": (
                  "$[A\\mid\\vec{0}]$ se reduce (omitimos cómputos) a $\\left[\\begin{array}{rrr|r} 1 & 0 & -4/3 & 0 \\\\ 0 & 1 & 0 & 0 \\\\ 0 & 0 & 0 & 0 \\end{array}\\right]$."
              ),
               "justificacion_md": "Pivotes en columnas $1, 2$; libre $x_3 = t$.",
               "es_resultado": False},
              {"accion_md": (
                  "Despejamos: $x_1 = \\tfrac{4}{3} t$, $x_2 = 0$. Forma vectorial:\n\n"
                  "$\\vec{x} = t \\begin{bmatrix} 4/3 \\\\ 0 \\\\ 1 \\end{bmatrix}, \\quad t \\in \\mathbb{R}.$\n\n"
                  "**$\\mathcal{N}(A) = \\text{Gen}\\left\\{ (4/3,\\ 0,\\ 1)^T \\right\\}$** — una recta por el origen."
              ),
               "justificacion_md": "**Lección:** las soluciones de un sistema homogéneo siempre forman un **subespacio** (un objeto 'lineal' que pasa por $\\vec{0}$).",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Estructura de las soluciones de $A\\vec{x} = \\vec{b}$.** Si $A\\vec{x} = \\vec{b}$ es consistente, su conjunto solución es\n\n"
              "$$\\boxed{\\vec{x} = \\vec{x}_p + \\mathcal{N}(A)} = \\vec{x}_p + \\text{Gen}\\{\\vec{v}^{(1)}, \\ldots, \\vec{v}^{(k)}\\},$$\n\n"
              "donde $\\vec{x}_p$ es **una** solución particular y $\\{\\vec{v}^{(\\ell)}\\}$ es una base del núcleo $\\mathcal{N}(A)$. El número de parámetros es $k = n - \\text{rango}(A)$."
          ),
          demostracion_md=(
              "**($\\subseteq$)** Sea $\\vec{x}$ cualquier solución. Entonces $A(\\vec{x} - \\vec{x}_p) = A\\vec{x} - A\\vec{x}_p = \\vec{b} - \\vec{b} = \\vec{0}$, así que $\\vec{x} - \\vec{x}_p \\in \\mathcal{N}(A)$. Por tanto $\\vec{x} \\in \\vec{x}_p + \\mathcal{N}(A)$.\n\n"
              "**($\\supseteq$)** Si $\\vec{y} \\in \\mathcal{N}(A)$ entonces $A(\\vec{x}_p + \\vec{y}) = A\\vec{x}_p + A\\vec{y} = \\vec{b} + \\vec{0} = \\vec{b}$, luego $\\vec{x}_p + \\vec{y}$ es solución. $\\blacksquare$\n\n"
              "**Interpretación geométrica.** El conjunto solución de $A\\vec{x} = \\vec{b}$ es un **'núcleo trasladado'**: el núcleo $\\mathcal{N}(A)$ pasa por el origen; la solución particular $\\vec{x}_p$ lo desplaza para que pase por la solución."
          )),

        b("ejemplo_resuelto",
          titulo="Solución general $\\vec{x}_p + \\mathcal{N}(A)$",
          problema_md=(
              "Describir todas las soluciones de $A\\vec{x} = \\vec{b}$ con "
              "$A = \\begin{bmatrix} 3 & 5 & -4 \\\\ -3 & -2 & 4 \\\\ 6 & 1 & -8 \\end{bmatrix}$, $\\vec{b} = (7, -1, -4)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "Reduciendo $[A\\mid\\vec{b}]$ se obtiene $\\left[\\begin{array}{rrr|r} 1 & 0 & -4/3 & -1 \\\\ 0 & 1 & 0 & 2 \\\\ 0 & 0 & 0 & 0 \\end{array}\\right]$."
              ),
               "justificacion_md": "Sistema consistente; libre $x_3 = t$.",
               "es_resultado": False},
              {"accion_md": (
                  "$x_1 = -1 + \\tfrac{4}{3} t$, $x_2 = 2$, $x_3 = t$. Forma vectorial:\n\n"
                  "$\\vec{x} = \\underbrace{\\begin{bmatrix} -1 \\\\ 2 \\\\ 0 \\end{bmatrix}}_{\\vec{x}_p} + t \\underbrace{\\begin{bmatrix} 4/3 \\\\ 0 \\\\ 1 \\end{bmatrix}}_{\\vec{v}^{(1)}}, \\quad t \\in \\mathbb{R}.$"
              ),
               "justificacion_md": "$\\vec{v}^{(1)}$ coincide con la base de $\\mathcal{N}(A)$ del ejemplo previo, como predice el teorema.",
               "es_resultado": False},
              {"accion_md": (
                  "**Comprobación de $\\vec{x}_p$:** $A(-1, 2, 0)^T = (3(-1) + 5(2), -3(-1) - 2(2), 6(-1) + 2)^T = (7, -1, -4)^T = \\vec{b}$ ✓.\n\n"
                  "**Comprobación de $\\vec{v}^{(1)}$:** $A(4/3, 0, 1)^T = (4 - 4, -4 + 4, 8 - 8)^T = \\vec{0}$ ✓."
              ),
               "justificacion_md": "Esto confirma la descomposición $\\vec{x} = \\vec{x}_p + \\mathcal{N}(A)$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\text{rango}(A) = 3$ y $A \\in \\mathbb{R}^{4 \\times 5}$, el sistema homogéneo $A\\vec{x} = \\vec{0}$ tiene:",
                  "opciones_md": [
                      "Solo la solución trivial",
                      "Una recta de soluciones (1 parámetro)",
                      "Un plano de soluciones (2 parámetros)",
                      "Un volumen 3D de soluciones",
                  ],
                  "correcta": "C",
                  "pista_md": "Variables libres = $n - \\text{rango}(A)$.",
                  "explicacion_md": "$n - \\text{rango}(A) = 5 - 3 = 2$ variables libres $\\Rightarrow$ $2$ parámetros $\\Rightarrow$ **plano** por el origen en $\\mathbb{R}^5$.",
              },
              {
                  "enunciado_md": "Si $A$ tiene **más columnas que filas**, $A\\vec{x} = \\vec{0}$:",
                  "opciones_md": [
                      "Siempre solo tiene la solución trivial",
                      "Puede tener o no soluciones no triviales",
                      "**Siempre** tiene soluciones no triviales",
                      "Es incompatible",
                  ],
                  "correcta": "C",
                  "pista_md": "$\\text{rango}(A) \\leq m < n$ obliga a tener variables libres.",
                  "explicacion_md": "$\\text{rango}(A) \\leq m$, y como $n > m$, $\\text{rango}(A) < n$ $\\Rightarrow$ hay **al menos una** variable libre $\\Rightarrow$ **siempre** hay soluciones no triviales (un sistema homogéneo es siempre consistente).",
              },
              {
                  "enunciado_md": "El conjunto solución de $A\\vec{x} = \\vec{b}$ (consistente, con núcleo no trivial) es geométricamente:",
                  "opciones_md": [
                      "Un subespacio que contiene a $\\vec{0}$",
                      "Una traslación del núcleo $\\mathcal{N}(A)$ por $\\vec{x}_p$",
                      "Un punto aislado",
                      "El vacío",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\vec{x} = \\vec{x}_p + \\mathcal{N}(A)$.",
                  "explicacion_md": "**Es un 'subespacio afín'**: el núcleo (que pasa por el origen) trasladado por la solución particular $\\vec{x}_p$. Generalmente **no contiene a $\\vec{0}$** salvo cuando $\\vec{b} = \\vec{0}$ (caso homogéneo).",
              },
          ]),

        ej(
            "Forma vectorial con dos parámetros",
            "Describe el conjunto solución de $A\\vec{x} = \\vec{b}$ con $A = \\begin{bmatrix} 1 & 0 & 2 & -1 \\\\ 0 & 1 & -1 & 3 \\end{bmatrix}$ y $\\vec{b} = \\begin{bmatrix} 5 \\\\ -2 \\end{bmatrix}$.",
            [
                "La matriz ya está en RREF.",
                "Pivotes en columnas $1, 2$ $\\Rightarrow$ libres $x_3, x_4$.",
            ],
            (
                "$x_3 = t$, $x_4 = s$. De las filas: $x_1 = 5 - 2t + s$, $x_2 = -2 + t - 3s$.\n\n"
                "**Forma vectorial:**\n\n"
                "$\\vec{x} = \\begin{bmatrix} 5 \\\\ -2 \\\\ 0 \\\\ 0 \\end{bmatrix} + t \\begin{bmatrix} -2 \\\\ 1 \\\\ 1 \\\\ 0 \\end{bmatrix} + s \\begin{bmatrix} 1 \\\\ -3 \\\\ 0 \\\\ 1 \\end{bmatrix}, \\quad t, s \\in \\mathbb{R}.$"
            ),
        ),

        ej(
            "Sistema homogéneo $2 \\times 3$",
            "Resuelve $A\\vec{x} = \\vec{0}$ con $A = \\begin{bmatrix} 1 & 2 & 0 \\\\ 0 & 1 & 1 \\end{bmatrix}$ y describe $\\mathcal{N}(A)$.",
            [
                "Reduce a RREF.",
                "Despeja básicas en función de la libre.",
            ],
            (
                "$A \\sim \\begin{bmatrix} 1 & 0 & -2 \\\\ 0 & 1 & 1 \\end{bmatrix}$. Libre $x_3 = t$. $x_1 = 2t$, $x_2 = -t$.\n\n"
                "$\\vec{x} = t (2, -1, 1)^T$, así que $\\mathcal{N}(A) = \\text{Gen}\\{(2, -1, 1)^T\\}$ — una recta por el origen en $\\mathbb{R}^3$."
            ),
        ),

        ej(
            "Solución única",
            "Resuelve $A\\vec{x} = \\vec{b}$ con $A = \\begin{bmatrix} 2 & 1 \\\\ 1 & -1 \\end{bmatrix}$ y $\\vec{b} = \\begin{bmatrix} 1 \\\\ 3 \\end{bmatrix}$. ¿Cuál es $\\mathcal{N}(A)$?",
            [
                "$A$ es $2 \\times 2$. Verifica que sus dos columnas tienen pivote.",
                "Si $A$ tiene pivote en cada columna, $\\mathcal{N}(A) = \\{\\vec{0}\\}$.",
            ],
            (
                "Reduciendo: $A \\sim \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}$. **Pivote en cada columna** $\\Rightarrow$ no hay variables libres $\\Rightarrow$ **solución única**.\n\n"
                "Resolviendo el sistema: $x_1 - x_2 = 3$ y $2x_1 + x_2 = 1$. Sumando $2 \\times$ (1ª) a la (2ª) $\\Rightarrow$ $4x_1 - x_2 + x_2 = 7 \\Rightarrow$ ... mejor por sustitución directa: $x_1 = \\tfrac{4}{3}, x_2 = -\\tfrac{5}{3}$.\n\n"
                "$\\mathcal{N}(A) = \\{\\vec{0}\\}$: solo la solución trivial."
            ),
        ),

        fig(
            "Tres paneles en perspectiva 3D ilustrando los tipos de conjunto solución de un sistema $A\\vec{x} = \\vec{b}$ en R^3. "
            "Panel izquierdo: tres planos en tonos teal #06b6d4 que se intersectan en un único punto, destacado como un círculo grande en ámbar #f59e0b. Etiqueta inferior: 'Solución única'. "
            "Panel central: dos planos casi coincidentes y un tercero que los corta a lo largo de una recta resaltada en ámbar #f59e0b. Etiqueta: 'Infinitas (1 parámetro) — recta'. "
            "Panel derecho: tres planos coincidentes (el mismo plano dibujado con triple borde) en teal #06b6d4 con sombreado ámbar #f59e0b sobre toda la superficie. Etiqueta: 'Infinitas (2 parámetros) — plano'. "
            "Ejes $x_1, x_2, x_3$ visibles en cada panel. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir variables básicas y libres.** Las **básicas** corresponden a columnas pivote de $A$; las **libres**, a columnas sin pivote.",
              "**Considerar la columna de $\\vec{b}$ al contar variables libres.** Las variables libres se cuentan **solo** sobre las columnas de $A$.",
              "**Olvidar que un sistema homogéneo es **siempre** consistente.** $\\vec{x} = \\vec{0}$ es solución siempre. La pregunta es si hay soluciones **no triviales**.",
              "**Decir 'núcleo trivial' cuando hay soluciones no triviales.** $\\mathcal{N}(A) = \\{\\vec{0}\\}$ solo si $A$ tiene pivote en cada columna.",
              "**Escribir $\\vec{x}_p$ con valores no nulos en las componentes libres.** $\\vec{x}_p$ se obtiene tomando los parámetros $= 0$.",
              "**Decir 'el conjunto solución es un subespacio' para sistemas no homogéneos.** Solo en el caso homogéneo. Si $\\vec{b} \\neq \\vec{0}$, es un **subespacio afín** (no contiene a $\\vec{0}$ en general).",
              "**Olvidar verificar consistencia primero.** Si aparece fila $[\\,0\\ \\cdots\\ 0\\mid c\\,]$ con $c \\neq 0$, no hay solución, así que la 'descripción del conjunto' es $\\emptyset$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Variables básicas:** columnas pivote de $A$. **Variables libres:** columnas sin pivote.",
              "**Existencia:** consistente $\\iff$ no hay fila $[\\,0\\ \\cdots\\ 0\\mid c\\neq 0\\,]$ $\\iff$ rangos iguales.",
              "**Unicidad (consistente):** SCD $\\iff$ pivote en cada columna de $A$. SCI $\\iff$ alguna columna sin pivote.",
              "**Forma vectorial:** $\\vec{x} = \\vec{x}_p + t_1 \\vec{v}^{(1)} + \\cdots + t_k \\vec{v}^{(k)}$, con $k = n - \\text{rango}(A)$.",
              "**Núcleo:** $\\mathcal{N}(A) = \\{\\vec{x}: A\\vec{x} = \\vec{0}\\}$. Es el conjunto solución del sistema homogéneo asociado.",
              "**Estructura fundamental:** $\\vec{x} = \\vec{x}_p + \\mathcal{N}(A)$ — núcleo trasladado por una solución particular.",
              "**Próxima lección:** las matrices ya no como 'tablas', sino como **funciones lineales** $T(\\vec{x}) = A\\vec{x}$.",
          ]),
    ]
    return {
        "id": "lec-al-2-4-conjunto-solucion",
        "title": "Conjunto solución",
        "description": "Variables básicas y libres, lectura de la RREF, forma paramétrica y vectorial, núcleo $\\mathcal{N}(A)$ y descomposición $\\vec{x} = \\vec{x}_p + \\mathcal{N}(A)$.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# =====================================================================
# 2.5 Transformaciones lineales
# =====================================================================
def lesson_2_5():
    blocks = [
        b("texto", body_md=(
            "Cerramos el capítulo con el cambio de perspectiva más importante del álgebra lineal: pasar "
            "de ver una matriz como una **tabla de números** a verla como una **función**.\n\n"
            "Una **transformación lineal** $T : \\mathbb{R}^n \\to \\mathbb{R}^m$ es una regla que **preserva** "
            "las dos operaciones fundamentales (suma y producto por escalar). El teorema central de la "
            "lección dice: toda transformación lineal $\\mathbb{R}^n \\to \\mathbb{R}^m$ es de la forma "
            "$T(\\vec{x}) = A\\vec{x}$ para una **única matriz** $A$, llamada **matriz estándar** de $T$.\n\n"
            "Esto traduce preguntas geométricas (¿es $T$ sobreyectiva? ¿inyectiva?) a preguntas de **rango y pivotes** que ya sabemos responder. También conecta el álgebra con la geometría del plano: rotaciones, reflexiones, escalas, trasquilados y proyecciones tienen matriz estándar explícita."
        )),

        b("definicion",
          titulo="Transformación lineal",
          body_md=(
              "Una **transformación lineal** $T : \\mathbb{R}^n \\to \\mathbb{R}^m$ es una función que satisface:\n\n"
              "$$\\text{(L1)} \\quad T(\\vec{u} + \\vec{v}) = T(\\vec{u}) + T(\\vec{v}), \\qquad \\text{(L2)} \\quad T(c\\vec{u}) = c\\,T(\\vec{u}),$$\n\n"
              "para todos $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$ y $c \\in \\mathbb{R}$.\n\n"
              "**Consecuencias inmediatas.** Si $T$ es lineal:\n\n"
              "- $T(\\vec{0}) = \\vec{0}$ (toma $c = 0$ en L2).\n"
              "- $T(c\\vec{u} + d\\vec{v}) = cT(\\vec{u}) + dT(\\vec{v})$.\n"
              "- $T(c_1 \\vec{v}_1 + \\cdots + c_p \\vec{v}_p) = c_1 T(\\vec{v}_1) + \\cdots + c_p T(\\vec{v}_p)$.\n\n"
              "**Nomenclatura.** $\\mathbb{R}^n$ es el **dominio**, $\\mathbb{R}^m$ el **codominio**. La **imagen** (o rango) de $T$ es\n\n"
              "$$\\text{Im}(T) = \\{T(\\vec{x}) : \\vec{x} \\in \\mathbb{R}^n\\} \\subseteq \\mathbb{R}^m.$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Toda matriz define una transformación lineal.** Si $A \\in \\mathbb{R}^{m \\times n}$, la aplicación $T(\\vec{x}) = A\\vec{x}$ es lineal."
          ),
          demostracion_md=(
              "L1: $A(\\vec{u} + \\vec{v}) = A\\vec{u} + A\\vec{v}$ (linealidad del producto matriz–vector). L2: $A(c\\vec{u}) = c(A\\vec{u})$. Ambas se demostraron en la lección 2.3. $\\blacksquare$"
          )),

        b("teorema",
          nombre="Matriz estándar de una transformación lineal",
          enunciado_md=(
              "Sea $T : \\mathbb{R}^n \\to \\mathbb{R}^m$ una transformación lineal. Existe una **única** matriz $A \\in \\mathbb{R}^{m \\times n}$ tal que\n\n"
              "$$T(\\vec{x}) = A\\vec{x} \\qquad \\text{para todo } \\vec{x} \\in \\mathbb{R}^n.$$\n\n"
              "Más aún, las **columnas de $A$ son las imágenes de los vectores estándar** $\\vec{e}_1, \\ldots, \\vec{e}_n$:\n\n"
              "$$\\boxed{A = \\bigl[\\, T(\\vec{e}_1)\\ \\ T(\\vec{e}_2)\\ \\ \\cdots\\ \\ T(\\vec{e}_n) \\,\\bigr].}$$"
          ),
          demostracion_md=(
              "Para cualquier $\\vec{x} = x_1 \\vec{e}_1 + \\cdots + x_n \\vec{e}_n$, por linealidad,\n\n"
              "$T(\\vec{x}) = x_1 T(\\vec{e}_1) + \\cdots + x_n T(\\vec{e}_n) = [T(\\vec{e}_1)\\ \\cdots\\ T(\\vec{e}_n)]\\vec{x} = A\\vec{x}$.\n\n"
              "**Unicidad:** si $A$ y $A'$ representan a la misma $T$, entonces $A\\vec{e}_j = T(\\vec{e}_j) = A'\\vec{e}_j$ para todo $j$, así que sus columnas coinciden. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Construir la matriz estándar a partir de $T(\\vec{e}_1), T(\\vec{e}_2)$",
          problema_md=(
              "Sea $T : \\mathbb{R}^2 \\to \\mathbb{R}^3$ lineal con $T(\\vec{e}_1) = (5, -7, 2)^T$ y $T(\\vec{e}_2) = (-3, 8, 0)^T$. "
              "(i) Encontrar una fórmula para $T(\\vec{x})$. (ii) Hallar la matriz estándar $A$."
          ),
          pasos=[
              {"accion_md": (
                  "**(i)** Escribimos $\\vec{x} = x_1 \\vec{e}_1 + x_2 \\vec{e}_2$. Por linealidad:\n\n"
                  "$T(\\vec{x}) = x_1 T(\\vec{e}_1) + x_2 T(\\vec{e}_2) = x_1 \\begin{bmatrix} 5 \\\\ -7 \\\\ 2 \\end{bmatrix} + x_2 \\begin{bmatrix} -3 \\\\ 8 \\\\ 0 \\end{bmatrix} = \\begin{bmatrix} 5x_1 - 3x_2 \\\\ -7x_1 + 8x_2 \\\\ 2x_1 \\end{bmatrix}.$"
              ),
               "justificacion_md": "L1 + L2 aplicadas a la descomposición canónica de $\\vec{x}$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(ii)** Yuxtaponiendo $T(\\vec{e}_1)$ y $T(\\vec{e}_2)$ como columnas:\n\n"
                  "$A = \\begin{bmatrix} 5 & -3 \\\\ -7 & 8 \\\\ 2 & 0 \\end{bmatrix} \\in \\mathbb{R}^{3 \\times 2}, \\quad T(\\vec{x}) = A\\vec{x}.$"
              ),
               "justificacion_md": "**Tamaño:** $T : \\mathbb{R}^n \\to \\mathbb{R}^m$ $\\Rightarrow$ $A \\in \\mathbb{R}^{m \\times n}$.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Imagen de $T(\\vec{x}) = A\\vec{x}$.** Si $A = [\\,\\vec{a}_1\\ \\cdots\\ \\vec{a}_n\\,]$, entonces\n\n"
              "$$\\text{Im}(T) = \\text{Gen}\\{\\vec{a}_1, \\ldots, \\vec{a}_n\\} = \\text{Col}(A).$$\n\n"
              "Es decir, $\\vec{b} \\in \\text{Im}(T) \\iff A\\vec{x} = \\vec{b}$ es **consistente**."
          )),

        b("definicion",
          titulo="Sobreyectividad e inyectividad",
          body_md=(
              "Sea $T : \\mathbb{R}^n \\to \\mathbb{R}^m$ con matriz estándar $A$.\n\n"
              "**$T$ es sobreyectiva (sobre $\\mathbb{R}^m$)** si para todo $\\vec{b} \\in \\mathbb{R}^m$ existe $\\vec{x}$ con $T(\\vec{x}) = \\vec{b}$. **Equivalencias:**\n\n"
              "- $\\text{Im}(T) = \\mathbb{R}^m$.\n"
              "- $\\text{Gen}\\{\\vec{a}_1, \\ldots, \\vec{a}_n\\} = \\mathbb{R}^m$.\n"
              "- $A$ tiene posición pivote en **cada fila**.\n"
              "- $\\text{rango}(A) = m$.\n\n"
              "**$T$ es inyectiva (uno a uno)** si distintos $\\vec{x}$ dan distintos $T(\\vec{x})$. **Equivalencias:**\n\n"
              "- $T(\\vec{x}) = \\vec{0}$ tiene **solo** la solución trivial $\\vec{x} = \\vec{0}$ (núcleo trivial).\n"
              "- Las **columnas de $A$ son LI**.\n"
              "- $A$ tiene pivote en **cada columna** (no hay variables libres).\n"
              "- $\\text{rango}(A) = n$."
          )),

        formulas(
            titulo="Resumen visual: pivotes ↔ propiedades de $T$",
            body=(
                "| Propiedad de $T$ | Lugar de los pivotes | Rango |\n|---|---|---|\n"
                "| **Sobreyectiva** | Pivote en cada **fila** de $A$ | $\\text{rango}(A) = m$ |\n"
                "| **Inyectiva** | Pivote en cada **columna** de $A$ | $\\text{rango}(A) = n$ |\n"
                "| **Biyectiva** (solo si $m = n$) | Pivote en cada fila **y** columna | $\\text{rango}(A) = n = m$ |\n\n"
                "**Caso cuadrado ($m = n$):** sobreyectiva $\\iff$ inyectiva $\\iff$ invertible (cap. 3)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="¿Sobre? ¿Uno a uno?",
          problema_md=(
              "Sea $T : \\mathbb{R}^4 \\to \\mathbb{R}^3$ con $A = \\begin{bmatrix} 1 & -4 & 8 & 1 \\\\ 0 & 2 & -1 & 3 \\\\ 0 & 0 & 0 & 5 \\end{bmatrix}$. ¿$T$ mapea sobre $\\mathbb{R}^3$? ¿Es uno a uno?"
          ),
          pasos=[
              {"accion_md": (
                  "$A$ ya está en forma escalonada con pivotes en columnas $1, 2, 4$ (filas $1, 2, 3$).\n\n"
                  "**Pivote en cada fila** ($3$ pivotes en $3$ filas) $\\Rightarrow$ $\\text{rango}(A) = 3 = m$ $\\Rightarrow$ **$T$ es sobre $\\mathbb{R}^3$**."
              ),
               "justificacion_md": "Cumple el criterio de sobreyectividad.",
               "es_resultado": False},
              {"accion_md": (
                  "Sin embargo, hay $4$ columnas y solo $3$ pivotes (la columna $3$ no tiene pivote) $\\Rightarrow$ $1$ variable libre $\\Rightarrow$ las columnas son **LD**.\n\n"
                  "**Conclusión:** $T$ **no es uno a uno**."
              ),
               "justificacion_md": "Tiene sentido: una transformación de $\\mathbb{R}^4$ a $\\mathbb{R}^3$ pierde una dimensión, no puede ser inyectiva ($n > m$ siempre fuerza no inyectividad).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Proyección sobre el eje $x_1$",
          problema_md=(
              "Considera $P : \\mathbb{R}^2 \\to \\mathbb{R}^2$ dada por $P(\\vec{x}) = \\begin{bmatrix} 1 & 0 \\\\ 0 & 0 \\end{bmatrix} \\vec{x}$. Decide si $P$ es sobre y/o uno a uno."
          ),
          pasos=[
              {"accion_md": (
                  "$\\text{Im}(P) = \\text{Gen}\\{(1,0)^T, (0,0)^T\\} = \\text{Gen}\\{(1,0)^T\\}$ — **el eje $x_1$**, no todo $\\mathbb{R}^2$.\n\n"
                  "**$P$ no es sobre.**"
              ),
               "justificacion_md": "Solo hay un pivote en $A$, no hay pivote en la fila $2$.",
               "es_resultado": False},
              {"accion_md": (
                  "$P((0, t)^T) = (0, 0)^T$ para todo $t$ $\\Rightarrow$ infinitos vectores se mapean al $\\vec{0}$.\n\n"
                  "**$P$ no es uno a uno.**"
              ),
               "justificacion_md": "El núcleo $\\mathcal{N}(A) = \\{(0, t)^T : t \\in \\mathbb{R}\\}$ es no trivial (toda la 'línea $x_1 = 0$').",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Transformaciones geométricas en $\\mathbb{R}^2$",
          body_md=(
              "**Rotación por ángulo $\\varphi$** (antihoraria): $A = \\begin{bmatrix} \\cos\\varphi & -\\sin\\varphi \\\\ \\sin\\varphi & \\cos\\varphi \\end{bmatrix}$.\n\n"
              "**Reflexiones:**\n\n"
              "| Eje / recta | Matriz |\n|---|---|\n"
              "| Respecto del eje $x_1$ | $\\begin{bmatrix} 1 & 0 \\\\ 0 & -1 \\end{bmatrix}$ |\n"
              "| Respecto del eje $x_2$ | $\\begin{bmatrix} -1 & 0 \\\\ 0 & 1 \\end{bmatrix}$ |\n"
              "| Respecto de $x_2 = x_1$ | $\\begin{bmatrix} 0 & 1 \\\\ 1 & 0 \\end{bmatrix}$ |\n"
              "| Respecto de $x_2 = -x_1$ | $\\begin{bmatrix} 0 & -1 \\\\ -1 & 0 \\end{bmatrix}$ |\n"
              "| Respecto del origen | $-I = \\begin{bmatrix} -1 & 0 \\\\ 0 & -1 \\end{bmatrix}$ |\n\n"
              "**Escalas:** horizontal por $k$ → $\\begin{bmatrix} k & 0 \\\\ 0 & 1 \\end{bmatrix}$, vertical por $k$ → $\\begin{bmatrix} 1 & 0 \\\\ 0 & k \\end{bmatrix}$, uniforme → $kI$.\n\n"
              "**Trasquilados (shears):** horizontal $\\begin{bmatrix} 1 & k \\\\ 0 & 1 \\end{bmatrix}$, vertical $\\begin{bmatrix} 1 & 0 \\\\ k & 1 \\end{bmatrix}$.\n\n"
              "**Proyecciones:** sobre el eje $x_1$ → $\\begin{bmatrix} 1 & 0 \\\\ 0 & 0 \\end{bmatrix}$; sobre la recta gen. por $\\vec{u} \\neq \\vec{0}$ → $A = \\dfrac{\\vec{u}\\vec{u}^T}{\\|\\vec{u}\\|^2}$ (cap. 7)."
          )),

        b("ejemplo_resuelto",
          titulo="Matriz de la rotación de $90°$ antihoraria",
          problema_md=(
              "Verifica que la matriz de rotación con $\\varphi = \\pi/2$ es $A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Por el método de las imágenes de los $\\vec{e}_j$: una rotación de $90°$ antihoraria envía $\\vec{e}_1 = (1, 0)$ a $(0, 1)$ y $\\vec{e}_2 = (0, 1)$ a $(-1, 0)$.\n\n"
                  "**Matriz estándar:** $A = [T(\\vec{e}_1)\\ T(\\vec{e}_2)] = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}$."
              ),
               "justificacion_md": "Sustituyendo $\\varphi = \\pi/2$ en la fórmula general: $\\cos(\\pi/2) = 0$, $\\sin(\\pi/2) = 1$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación con un vector concreto:** $A \\begin{bmatrix} 4 \\\\ 1 \\end{bmatrix} = \\begin{bmatrix} -1 \\\\ 4 \\end{bmatrix}$. Efectivamente $(4, 1)$ rotado $90°$ antihorario da $(-1, 4)$ (intercambia coordenadas y cambia el signo de la nueva primera)."
              ),
               "justificacion_md": "$T(u) + T(v) = T(u+v)$ y $T(cu) = cT(u)$ se mantienen — es lineal.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Sea $T: \\mathbb{R}^3 \\to \\mathbb{R}^5$ lineal. ¿Puede $T$ ser sobreyectiva?",
                  "opciones_md": [
                      "Sí, siempre",
                      "Sí, dependiendo de la matriz",
                      "Nunca",
                      "Solo si $T$ es inyectiva",
                  ],
                  "correcta": "C",
                  "pista_md": "Sobreyectiva $\\iff$ pivote en cada fila ($m = 5$ pivotes), pero $A$ tiene solo $n = 3$ columnas.",
                  "explicacion_md": "$\\text{rango}(A) \\leq \\min(m, n) = 3 < 5 = m$. **Imposible** tener pivote en cada fila $\\Rightarrow$ $T$ nunca es sobre. **Regla:** $\\mathbb{R}^n \\to \\mathbb{R}^m$ con $n < m$ nunca es sobre.",
              },
              {
                  "enunciado_md": "La matriz estándar de la rotación de $180°$ es:",
                  "opciones_md": [
                      "$\\begin{bmatrix} 0 & 1 \\\\ 1 & 0 \\end{bmatrix}$",
                      "$\\begin{bmatrix} 1 & 0 \\\\ 0 & -1 \\end{bmatrix}$",
                      "$\\begin{bmatrix} -1 & 0 \\\\ 0 & -1 \\end{bmatrix}$",
                      "$\\begin{bmatrix} 0 & -1 \\\\ -1 & 0 \\end{bmatrix}$",
                  ],
                  "correcta": "C",
                  "pista_md": "$\\cos(\\pi) = -1$, $\\sin(\\pi) = 0$.",
                  "explicacion_md": "Sustituyendo $\\varphi = \\pi$ en la matriz de rotación: $\\begin{bmatrix} -1 & 0 \\\\ 0 & -1 \\end{bmatrix} = -I$. Coincide con la **inversión respecto del origen**.",
              },
              {
                  "enunciado_md": "Si las columnas de $A$ son LI y $A$ tiene tamaño $5 \\times 3$, entonces $T(\\vec{x}) = A\\vec{x}$ es:",
                  "opciones_md": [
                      "Sobreyectiva pero no inyectiva",
                      "Inyectiva pero no sobreyectiva",
                      "Ambas",
                      "Ninguna",
                  ],
                  "correcta": "B",
                  "pista_md": "Columnas LI $\\Rightarrow$ pivote en cada columna. Pero $n = 3 < m = 5$.",
                  "explicacion_md": "**Inyectiva**: pivote en cada columna ($\\text{rango}(A) = 3 = n$). **No sobre**: solo $3$ pivotes en $5$ filas; $\\text{Im}(T) = \\text{Col}(A)$ es solo un 'plano 3D' dentro de $\\mathbb{R}^5$.",
              },
          ]),

        ej(
            "Verificar linealidad",
            "Decide si $T : \\mathbb{R}^2 \\to \\mathbb{R}^2$ dada por $T(x_1, x_2) = (x_1 + x_2,\\ x_1 - x_2)$ es lineal. Si lo es, halla su matriz estándar.",
            [
                "Verifica L1 y L2 directamente, o intenta escribir $T(\\vec{x}) = A\\vec{x}$.",
                "Calcula $T(\\vec{e}_1)$ y $T(\\vec{e}_2)$.",
            ],
            (
                "Comprobamos: $T(\\vec{e}_1) = T(1, 0) = (1, 1)$, $T(\\vec{e}_2) = T(0, 1) = (1, -1)$.\n\n"
                "Conjeturando linealidad: $A = \\begin{bmatrix} 1 & 1 \\\\ 1 & -1 \\end{bmatrix}$, y $A\\vec{x} = (x_1 + x_2,\\ x_1 - x_2)^T$. ✓\n\n"
                "Como $T(\\vec{x}) = A\\vec{x}$, $T$ es **lineal** (toda transformación de la forma $A\\vec{x}$ lo es)."
            ),
        ),

        ej(
            "Imagen y base",
            "Para $T : \\mathbb{R}^2 \\to \\mathbb{R}^3$ con $A = \\begin{bmatrix} 1 & 0 \\\\ 2 & 1 \\\\ 3 & 1 \\end{bmatrix}$: (a) decide si $\\vec{b} = (1, 0, 2)^T \\in \\text{Im}(T)$; (b) halla una base de $\\text{Im}(T)$ y $\\dim \\text{Im}(T)$.",
            [
                "(a) Estudia la consistencia de $A\\vec{x} = \\vec{b}$.",
                "(b) Reduce $A$; las columnas pivote (de la matriz original) forman una base de $\\text{Im}(T)$.",
            ],
            (
                "**(a)** Reducimos $[A\\mid \\vec{b}] = \\left[\\begin{array}{rr|r} 1 & 0 & 1 \\\\ 2 & 1 & 0 \\\\ 3 & 1 & 2 \\end{array}\\right] \\sim \\left[\\begin{array}{rr|r} 1 & 0 & 1 \\\\ 0 & 1 & -2 \\\\ 0 & 0 & 1 \\end{array}\\right]$.\n\n"
                "Aparece fila $[\\,0\\ 0 \\mid 1\\,]$ $\\Rightarrow$ inconsistente $\\Rightarrow$ $\\vec{b} \\notin \\text{Im}(T)$.\n\n"
                "**(b)** $A$ tiene $2$ columnas LI (las dos pivote tras reducción). Una base de $\\text{Im}(T)$ es $\\{(1,2,3)^T,\\ (0,1,1)^T\\}$ y $\\dim \\text{Im}(T) = 2$."
            ),
        ),

        ej(
            "Composición de geométricas",
            "Sea $T_1$ la reflexión respecto del eje $x_1$ y $T_2$ la rotación de $90°$ antihoraria. Halla la matriz de $T = T_2 \\circ T_1$ (primero reflejar, luego rotar) y aplícala a $\\vec{u} = (3, -2)^T$.",
            [
                "Matriz de la composición = producto de matrices en el orden inverso de aplicación: $A_{T_2 \\circ T_1} = A_{T_2} A_{T_1}$.",
                "Veremos producto matricial formalmente en el cap. 3, pero aquí simplemente puedes calcular $T_2(T_1(\\vec{u}))$ paso a paso.",
            ],
            (
                "$T_1(\\vec{u}) = T_1(3, -2) = (3, 2)$ (cambia el signo de la 2ª componente).\n\n"
                "$T_2(3, 2) = (-2, 3)$ (rotación $90°$ antihoraria: $(x, y) \\to (-y, x)$).\n\n"
                "$T(\\vec{u}) = (-2, 3)$. La matriz $A_T$ se obtiene aplicando $T$ a $\\vec{e}_1$ y $\\vec{e}_2$: $T(\\vec{e}_1) = T_2(1, 0) = (0, 1)$ y $T(\\vec{e}_2) = T_2(0, -1) = (1, 0)$, así que $A_T = \\begin{bmatrix} 0 & 1 \\\\ 1 & 0 \\end{bmatrix}$ — ¡es la **reflexión respecto de $x_2 = x_1$**!"
            ),
        ),

        fig(
            "Dos planos cartesianos lado a lado mostrando el efecto de una transformación lineal $T : \\mathbb{R}^2 \\to \\mathbb{R}^2$ que combina rotación y estiramiento. "
            "Panel izquierdo (dominio): cuadrícula regular en color gris claro con los vectores canónicos $\\vec{e}_1$ y $\\vec{e}_2$ partiendo del origen en color ámbar #f59e0b. Etiqueta: 'Antes de T'. "
            "Panel derecho (codominio): cuadrícula transformada en color teal #06b6d4 cuyas celdas siguen siendo paralelogramos (no curvos), inclinados y estirados respecto al original. Sobre la cuadrícula transformada, las imágenes $T(\\vec{e}_1)$ y $T(\\vec{e}_2)$ destacadas en ámbar #f59e0b. Etiqueta: 'Después de T'. "
            "Una flecha curva grande conecta ambos paneles con la inscripción $T$. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Asumir linealidad sin verificar.** $T(x) = x + 1$ **no** es lineal (no manda $0$ a $0$).",
              "**Confundir dominio y codominio.** $T : \\mathbb{R}^n \\to \\mathbb{R}^m$ implica $A \\in \\mathbb{R}^{m \\times n}$ — el codominio define el número de **filas**.",
              "**Mezclar criterios de sobre y uno a uno.** Sobre = pivote en cada **fila**; uno a uno = pivote en cada **columna**.",
              "**Decir 'es uno a uno' cuando hay variables libres.** Variables libres $\\Leftrightarrow$ núcleo no trivial $\\Leftrightarrow$ no inyectiva.",
              "**Confundir $\\text{Im}(T) \\subseteq \\mathbb{R}^m$ con todo $\\mathbb{R}^m$.** En general $\\text{Im}(T)$ es solo un subconjunto (un 'subespacio columna').",
              "**Olvidar que la matriz estándar tiene $T(\\vec{e}_j)$ como columnas, no como filas.**",
              "**Pensar que rotaciones, reflexiones y proyecciones son arbitrarias.** Cada transformación geométrica clásica tiene una matriz estándar fija — vale la pena memorizar las más comunes.",
          ]),

        b("resumen",
          puntos_md=[
              "**Lineal:** $T(\\vec{u} + \\vec{v}) = T(\\vec{u}) + T(\\vec{v})$ y $T(c\\vec{u}) = cT(\\vec{u})$ — preserva combinaciones lineales.",
              "**Toda lineal $\\mathbb{R}^n \\to \\mathbb{R}^m$ es $T(\\vec{x}) = A\\vec{x}$**, con $A = [T(\\vec{e}_1)\\ \\cdots\\ T(\\vec{e}_n)] \\in \\mathbb{R}^{m \\times n}$.",
              "**Imagen:** $\\text{Im}(T) = \\text{Col}(A) = \\text{Gen}\\{\\text{columnas de } A\\}$.",
              "**Sobre $\\mathbb{R}^m$** $\\iff$ pivote en cada fila $\\iff \\text{rango}(A) = m$.",
              "**Uno a uno** $\\iff$ pivote en cada columna $\\iff$ columnas LI $\\iff \\mathcal{N}(A) = \\{\\vec{0}\\} \\iff \\text{rango}(A) = n$.",
              "**Geometría plana:** rotación, reflexiones, escalas, trasquilados y proyecciones tienen matrices explícitas en $\\mathbb{R}^{2 \\times 2}$.",
              "**Cierre del capítulo 2:** sistemas $\\to$ matrices $\\to$ vectores $\\to$ funciones lineales. Ya tenemos el lenguaje completo del álgebra lineal computacional.",
              "**Siguiente capítulo:** **Álgebra de matrices** — suma, producto, transpuesta, inversa.",
          ]),
    ]
    return {
        "id": "lec-al-2-5-transformaciones-lineales",
        "title": "Transformaciones lineales",
        "description": "Definición, matriz estándar $A = [T(\\vec{e}_j)]$, imagen, sobreyectividad e inyectividad, transformaciones geométricas en $\\mathbb{R}^2$.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 5,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "algebra-lineal"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(
            f"Curso {course_id} no existe. Corre primero seed_algebra_lineal_chapter_1.py"
        )

    chapter_id = "ch-al-sistemas-ecuaciones"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Sistemas de Ecuaciones",
        "description": (
            "Sistemas lineales y matriz aumentada, eliminación de Gauss–Jordan, rango y "
            "Rouché–Frobenius, independencia lineal, conjunto solución (paramétrico y vectorial), "
            "núcleo $\\mathcal{N}(A)$ y transformaciones lineales $T(\\vec{x}) = A\\vec{x}$."
        ),
        "order": 2,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_2_1, lesson_2_2, lesson_2_3, lesson_2_4, lesson_2_5]
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
        f"✅ Capítulo 2 — Sistemas de Ecuaciones listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
