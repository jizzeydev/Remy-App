"""
Seed del curso Álgebra Lineal — Capítulo 6: Valores y Vectores Propios.
4 lecciones:
  6.1 Ecuación característica (vectores propios, det(A − λI) = 0, multiplicidades, similitud)
  6.2 Diagonalización (A = PDP^-1, algoritmo, casos diagonalizable / no)
  6.3 Vectores propios y transformaciones lineales (B-matriz, diagonalización como cambio de base)
  6.4 Valores propios complejos (C^n, parte real/imaginaria, A = PCP^-1 con C de rotación-escala)

Basado en los Apuntes/Clase de Se Remonta para cada lección.

Requiere que el curso 'algebra-lineal' ya exista. Idempotente.
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
# 6.1 Ecuación característica
# =====================================================================
def lesson_6_1():
    blocks = [
        b("texto", body_md=(
            "Una transformación lineal $T(\\vec{x}) = A\\vec{x}$ generalmente mueve los vectores en "
            "direcciones complicadas. Pero existen vectores **especiales** sobre los cuales $A$ actúa "
            "**simplemente como una escala** — los **vectores propios**. Cada uno de estos vectores tiene "
            "asociado un **valor propio** que indica el factor de estiramiento o compresión.\n\n"
            "Encontrar los valores y vectores propios de $A$ revela la **estructura geométrica** "
            "fundamental de la transformación. Es la base de:\n\n"
            "- **Diagonalización** de matrices (próxima lección).\n"
            "- **Sistemas dinámicos lineales** y ecuaciones diferenciales.\n"
            "- **Análisis de componentes principales (PCA)** en estadística y ML.\n"
            "- **Mecánica cuántica** (los autovalores son cantidades observables).\n\n"
            "Al terminar:\n\n"
            "- Defines y verificas vectores y valores propios.\n"
            "- Calculas el **espacio propio** $E_\\lambda = \\text{Nul}(A - \\lambda I)$.\n"
            "- Resuelves la **ecuación característica** $\\det(A - \\lambda I) = 0$.\n"
            "- Distingues **multiplicidad algebraica** y **geométrica**.\n"
            "- Sabes que matrices **similares** comparten valores propios."
        )),

        b("definicion",
          titulo="Vector y valor propio",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{n \\times n}$. Un **vector propio** de $A$ es un vector **no nulo** $\\vec{v} \\in \\mathbb{R}^n$ tal que\n\n"
              "$$\\boxed{A\\vec{v} = \\lambda \\vec{v}}$$\n\n"
              "para algún escalar $\\lambda \\in \\mathbb{R}$. Ese escalar $\\lambda$ se llama el **valor propio** correspondiente a $\\vec{v}$.\n\n"
              "**Geométricamente:** $A$ no rota a $\\vec{v}$, solo lo **estira** por factor $\\lambda$ (o lo invierte si $\\lambda < 0$, lo encoge si $|\\lambda| < 1$).\n\n"
              "**Restricción importante:** $\\vec{v} \\neq \\vec{0}$ (el cero satisface $A\\vec{0} = \\lambda\\vec{0}$ trivialmente para cualquier $\\lambda$ — no aporta información).\n\n"
              "**Espacio propio asociado a $\\lambda$:**\n\n"
              "$$E_\\lambda = \\{\\vec{x} \\in \\mathbb{R}^n : A\\vec{x} = \\lambda\\vec{x}\\} = \\text{Nul}(A - \\lambda I).$$\n\n"
              "Es siempre un **subespacio** de $\\mathbb{R}^n$ (núcleo de la matriz $A - \\lambda I$). Los vectores propios asociados a $\\lambda$ son los elementos **no nulos** de $E_\\lambda$."
          )),

        b("ejemplo_resuelto",
          titulo="Verificación de vectores propios",
          problema_md=(
              "Sea $A = \\begin{bmatrix} 1 & 6 \\\\ 5 & 2 \\end{bmatrix}$. Verifica si $\\vec{u} = (6, -5)^T$ y $\\vec{v} = (3, -2)^T$ son vectores propios de $A$."
          ),
          pasos=[
              {"accion_md": (
                  "Calculamos $A\\vec{u}$:\n\n"
                  "$A\\vec{u} = \\begin{bmatrix} 1 & 6 \\\\ 5 & 2 \\end{bmatrix}\\begin{bmatrix} 6 \\\\ -5 \\end{bmatrix} = \\begin{bmatrix} 6 - 30 \\\\ 30 - 10 \\end{bmatrix} = \\begin{bmatrix} -24 \\\\ 20 \\end{bmatrix} = -4\\begin{bmatrix} 6 \\\\ -5 \\end{bmatrix} = -4\\vec{u}.$\n\n"
                  "**$\\vec{u}$ es vector propio** con valor propio $\\lambda = -4$."
              ),
               "justificacion_md": "Buscamos un escalar $\\lambda$ tal que $A\\vec{u} = \\lambda\\vec{u}$. Aquí $\\lambda = -4$.",
               "es_resultado": False},
              {"accion_md": (
                  "Calculamos $A\\vec{v}$:\n\n"
                  "$A\\vec{v} = \\begin{bmatrix} 1 & 6 \\\\ 5 & 2 \\end{bmatrix}\\begin{bmatrix} 3 \\\\ -2 \\end{bmatrix} = \\begin{bmatrix} 3 - 12 \\\\ 15 - 4 \\end{bmatrix} = \\begin{bmatrix} -9 \\\\ 11 \\end{bmatrix} \\neq \\lambda \\vec{v}$ para ningún $\\lambda$.\n\n"
                  "**$\\vec{v}$ no es vector propio** ($A\\vec{v}$ no es múltiplo de $\\vec{v}$)."
              ),
               "justificacion_md": "Hay que verificar que $A\\vec{v}$ sea **proporcional** a $\\vec{v}$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Espacio propio asociado a un $\\lambda$ dado",
          problema_md=(
              "Demuestra que $\\lambda = 7$ es valor propio de $A = \\begin{bmatrix} 1 & 6 \\\\ 5 & 2 \\end{bmatrix}$ y halla una base del espacio propio."
          ),
          pasos=[
              {"accion_md": (
                  "Resolver $A\\vec{x} = 7\\vec{x}$ equivale a $(A - 7I)\\vec{x} = \\vec{0}$ con\n\n"
                  "$A - 7I = \\begin{bmatrix} -6 & 6 \\\\ 5 & -5 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Pasar todo a un lado y factorizar $\\vec{x}$.",
               "es_resultado": False},
              {"accion_md": (
                  "Reduciendo:\n\n"
                  "$\\begin{bmatrix} -6 & 6 \\\\ 5 & -5 \\end{bmatrix} \\sim \\begin{bmatrix} 1 & -1 \\\\ 0 & 0 \\end{bmatrix}.$\n\n"
                  "Como aparece una variable libre $x_2$, hay soluciones no triviales $\\Rightarrow$ **$\\lambda = 7$ es valor propio**."
              ),
               "justificacion_md": "$\\lambda$ es valor propio $\\iff (A - \\lambda I)\\vec{x} = \\vec{0}$ tiene soluciones no triviales $\\iff A - \\lambda I$ no es invertible.",
               "es_resultado": False},
              {"accion_md": (
                  "Solución general: $\\vec{x} = x_2\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}$. **Espacio propio:** $E_7 = \\text{Gen}\\{(1, 1)^T\\}$.\n\n"
                  "Una **base de $E_7$**: $\\{(1, 1)^T\\}$."
              ),
               "justificacion_md": "Un vector propio cualquiera, como $(1, 1)^T$, basta para describir todo el espacio propio.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Espacio propio en $\\mathbb{R}^3$",
          problema_md=(
              "Sea $A = \\begin{bmatrix} 4 & -1 & 6 \\\\ 2 & 1 & 6 \\\\ 2 & -1 & 8 \\end{bmatrix}$. Sabiendo que $\\lambda = 2$ es valor propio, halla una base de $E_2$."
          ),
          pasos=[
              {"accion_md": (
                  "$A - 2I = \\begin{bmatrix} 2 & -1 & 6 \\\\ 2 & -1 & 6 \\\\ 2 & -1 & 6 \\end{bmatrix}$. Reduciendo: $\\begin{bmatrix} 2 & -1 & 6 \\\\ 0 & 0 & 0 \\\\ 0 & 0 & 0 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Las tres filas son idénticas — generan una sola ecuación.",
               "es_resultado": False},
              {"accion_md": (
                  "Una sola ecuación: $2x_1 - x_2 + 6x_3 = 0 \\Rightarrow x_2 = 2x_1 + 6x_3$. Variables libres $x_1, x_3$:\n\n"
                  "$\\vec{x} = x_1 \\begin{bmatrix} 1 \\\\ 2 \\\\ 0 \\end{bmatrix} + x_3 \\begin{bmatrix} 0 \\\\ 6 \\\\ 1 \\end{bmatrix}.$\n\n"
                  "Hmm, mejor parametrizar de manera limpia: tomemos $x_1 = 1, x_3 = 0$ y $x_1 = 0, x_3 = 1$, dando $\\vec{v}_1 = (1, 2, 0)^T$ y $\\vec{v}_2 = (0, 6, 1)^T$. Equivalentemente, ajustando para evitar el coeficiente $6$, podemos tomar $x_3 = 1, x_1 = 0$: $\\vec{v}_2 = (0, 6, 1)^T$ o reescalar."
              ),
               "justificacion_md": "Cualquier base de $E_2$ vale; los generadores naturales aparecen al despejar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Base de $E_2$:** $\\Bigl\\{(1, 2, 0)^T,\\ (-3, 0, 1)^T\\Bigr\\}$ (ajustando con $x_1 = -3, x_3 = 1$ para 'limpiar': $x_2 = 2(-3) + 6(1) = 0$ ✓).\n\n"
                  "**$\\dim E_2 = 2$** (dos vectores LI)."
              ),
               "justificacion_md": "**Patrón:** la dimensión del espacio propio es el número de variables libres en $(A - \\lambda I)\\vec{x} = \\vec{0}$ — la **multiplicidad geométrica** de $\\lambda$.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Valores propios de matrices triangulares.** Si $A$ es triangular (superior o inferior), sus valores propios son las entradas de la **diagonal principal**.\n\n"
              "**Demostración rápida:** $\\det(A - \\lambda I) = \\prod_i (a_{ii} - \\lambda)$ (determinante de triangular = producto de la diagonal). Las raíces son $\\lambda = a_{11}, a_{22}, \\ldots, a_{nn}$."
          )),

        b("teorema",
          nombre="$\\lambda = 0$ y conexión con TMI",
          enunciado_md=(
              "$0$ es un valor propio de $A$ $\\iff A\\vec{x} = \\vec{0}$ tiene solución no trivial $\\iff A$ **no es invertible**.\n\n"
              "**Equivalentemente:** $A$ es invertible $\\iff$ $0$ no es valor propio $\\iff$ todos los valores propios de $A$ son no nulos."
          )),

        b("teorema",
          enunciado_md=(
              "**Vectores propios de valores propios distintos son LI.**\n\n"
              "Si $\\vec{v}_1, \\ldots, \\vec{v}_p$ son vectores propios de $A$ correspondientes a valores propios **distintos** $\\lambda_1, \\ldots, \\lambda_p$, entonces $\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$ es **linealmente independiente**."
          ),
          demostracion_md=(
              "Por inducción en $p$. Caso $p = 1$: $\\vec{v}_1 \\neq \\vec{0}$ por definición. Para $p > 1$, supón $\\sum c_i \\vec{v}_i = \\vec{0}$. Aplicando $A$ y restando $\\lambda_p$ veces la ecuación: $\\sum_{i<p} c_i (\\lambda_i - \\lambda_p)\\vec{v}_i = \\vec{0}$. Por hipótesis inductiva los $\\vec{v}_i$ con $i < p$ son LI, así $c_i (\\lambda_i - \\lambda_p) = 0$. Como $\\lambda_i \\neq \\lambda_p$, $c_i = 0$. Sustituyendo, $c_p \\vec{v}_p = \\vec{0} \\Rightarrow c_p = 0$. $\\blacksquare$"
          )),

        b("definicion",
          titulo="Ecuación característica y polinomio característico",
          body_md=(
              "Para que $\\lambda$ sea valor propio de $A$ debe existir $\\vec{x} \\neq \\vec{0}$ con $(A - \\lambda I)\\vec{x} = \\vec{0}$. Esto significa que $A - \\lambda I$ es **singular**, equivalentemente:\n\n"
              "$$\\boxed{\\det(A - \\lambda I) = 0.}$$\n\n"
              "Esta ecuación se llama **ecuación característica** de $A$.\n\n"
              "El **polinomio característico** $p_A(\\lambda) = \\det(A - \\lambda I)$ es un polinomio en $\\lambda$ de grado **$n$** (donde $A$ es $n \\times n$).\n\n"
              "**Resumen práctico:**\n\n"
              "1. Calcular $A - \\lambda I$.\n"
              "2. Calcular $p_A(\\lambda) = \\det(A - \\lambda I)$.\n"
              "3. Resolver $p_A(\\lambda) = 0$ — las raíces son los valores propios.\n"
              "4. Para cada $\\lambda$, hallar $E_\\lambda = \\text{Nul}(A - \\lambda I)$ y una base."
          )),

        b("ejemplo_resuelto",
          titulo="Ecuación característica $2 \\times 2$",
          problema_md=(
              "Determina los valores propios de $A = \\begin{bmatrix} 2 & 3 \\\\ 3 & -6 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A - \\lambda I = \\begin{bmatrix} 2 - \\lambda & 3 \\\\ 3 & -6 - \\lambda \\end{bmatrix}$.\n\n"
                  "$\\det(A - \\lambda I) = (2 - \\lambda)(-6 - \\lambda) - 9 = -12 - 2\\lambda + 6\\lambda + \\lambda^2 - 9 = \\lambda^2 + 4\\lambda - 21.$"
              ),
               "justificacion_md": "Aplicamos $ad - bc$ y expandimos.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolvemos $\\lambda^2 + 4\\lambda - 21 = 0$. Factorizando: $(\\lambda - 3)(\\lambda + 7) = 0$.\n\n"
                  "**Valores propios:** $\\lambda = 3$ y $\\lambda = -7$."
              ),
               "justificacion_md": "Polinomio cuadrático con dos raíces reales distintas.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Polinomio característico de matriz triangular $4\\times 4$",
          problema_md=(
              "Encuentra los valores propios de $A = \\begin{bmatrix} 5 & -2 & 6 & -1 \\\\ 0 & 3 & -8 & 0 \\\\ 0 & 0 & 5 & 4 \\\\ 0 & 0 & 0 & 1 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A - \\lambda I$ es triangular superior con diagonal $(5-\\lambda, 3-\\lambda, 5-\\lambda, 1-\\lambda)$. Su determinante es el producto:\n\n"
                  "$\\det(A - \\lambda I) = (5-\\lambda)(3-\\lambda)(5-\\lambda)(1-\\lambda) = (5-\\lambda)^2(3-\\lambda)(1-\\lambda).$"
              ),
               "justificacion_md": "Para triangulares, no hace falta expandir cofactores.",
               "es_resultado": False},
              {"accion_md": (
                  "Ecuación característica: $(5-\\lambda)^2(3-\\lambda)(1-\\lambda) = 0$.\n\n"
                  "**Valores propios:** $\\lambda = 5$ (con **multiplicidad algebraica** $2$), $\\lambda = 3$, $\\lambda = 1$."
              ),
               "justificacion_md": "**Lección:** los valores propios de una triangular son las entradas de la diagonal — y se cuentan con su multiplicidad como factor del polinomio.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Multiplicidad algebraica y geométrica",
          body_md=(
              "Sea $\\lambda$ un valor propio de $A$.\n\n"
              "**Multiplicidad algebraica** $m_a(\\lambda)$: el número de veces que $\\lambda$ aparece como raíz del polinomio característico (su exponente en la factorización).\n\n"
              "**Multiplicidad geométrica** $m_g(\\lambda) = \\dim E_\\lambda$: la dimensión del espacio propio (= número de vectores propios LI asociados a $\\lambda$).\n\n"
              "**Desigualdad fundamental:** para cualquier valor propio,\n\n"
              "$$\\boxed{1 \\leq m_g(\\lambda) \\leq m_a(\\lambda).}$$\n\n"
              "**Casos especiales:**\n\n"
              "- Si $m_a(\\lambda) = 1$: forzosamente $m_g(\\lambda) = 1$.\n"
              "- Si $m_g(\\lambda) < m_a(\\lambda)$: hay una **deficiencia geométrica**, lo que impide que $A$ sea diagonalizable (próxima lección).\n"
              "- Si $m_g(\\lambda) = m_a(\\lambda)$ para **todos** los valores propios: $A$ **es diagonalizable**."
          )),

        b("ejemplo_resuelto",
          titulo="Multiplicidad algebraica desde el polinomio",
          problema_md=(
              "El polinomio característico de una matriz $6 \\times 6$ es $p(\\lambda) = \\lambda^6 - 4\\lambda^5 - 12\\lambda^4$. Halla los valores propios y sus multiplicidades algebraicas."
          ),
          pasos=[
              {"accion_md": (
                  "Factorizamos: $\\lambda^6 - 4\\lambda^5 - 12\\lambda^4 = \\lambda^4(\\lambda^2 - 4\\lambda - 12) = \\lambda^4(\\lambda - 6)(\\lambda + 2).$"
              ),
               "justificacion_md": "Sacamos factor común y resolvemos la cuadrática.",
               "es_resultado": False},
              {"accion_md": (
                  "**Valores propios:**\n\n"
                  "- $\\lambda = 0$ con multiplicidad algebraica $4$.\n"
                  "- $\\lambda = 6$ con multiplicidad algebraica $1$.\n"
                  "- $\\lambda = -2$ con multiplicidad algebraica $1$.\n\n"
                  "Total: $4 + 1 + 1 = 6$ ✓ (consistente con que el polinomio es de grado $6$)."
              ),
               "justificacion_md": "**La suma de las multiplicidades algebraicas siempre es $n$** (cuando se permiten raíces complejas).",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Matrices similares",
          body_md=(
              "Dos matrices $A, B \\in \\mathbb{R}^{n \\times n}$ son **similares** si existe una matriz invertible $P$ tal que\n\n"
              "$$P^{-1} A P = B \\quad \\Longleftrightarrow \\quad A = P B P^{-1}.$$\n\n"
              "El proceso $A \\mapsto P^{-1}AP$ se llama **transformación de similitud**.\n\n"
              "**Teorema (similaridad conserva valores propios).** Si $A$ y $B$ son similares, entonces tienen el **mismo polinomio característico** $\\Rightarrow$ los **mismos valores propios** con las mismas multiplicidades algebraicas.\n\n"
              "**Demostración:** $\\det(B - \\lambda I) = \\det(P^{-1}AP - \\lambda P^{-1}IP) = \\det(P^{-1}(A - \\lambda I)P) = \\det(P^{-1})\\det(A - \\lambda I)\\det(P) = \\det(A - \\lambda I)$. $\\blacksquare$\n\n"
              "**Advertencias importantes:**\n\n"
              "1. **Tener los mismos valores propios NO implica similitud.** Las matrices $\\begin{bmatrix} 2 & 1 \\\\ 0 & 2 \\end{bmatrix}$ y $\\begin{bmatrix} 2 & 0 \\\\ 0 & 2 \\end{bmatrix}$ tienen ambas $\\lambda = 2$ doble, pero **no son similares** (la segunda es $2I$ y solo es similar a sí misma).\n\n"
              "2. **Similaridad ≠ equivalencia por filas.** Las OEF cambian los valores propios; la similitud no."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $A\\vec{v} = \\lambda \\vec{v}$ con $\\vec{v} \\neq \\vec{0}$, entonces:",
                  "opciones_md": [
                      "$\\vec{v}$ es valor propio y $\\lambda$ vector propio",
                      "$\\vec{v}$ es vector propio y $\\lambda$ valor propio",
                      "$\\lambda = 0$ siempre",
                      "$A$ es invertible siempre",
                  ],
                  "correcta": "B",
                  "pista_md": "El **vector** es $\\vec{v}$, el **escalar** $\\lambda$ es el valor.",
                  "explicacion_md": "**$\\vec{v}$ es el vector propio, $\\lambda$ el valor propio.** $\\lambda$ puede ser cualquier número real (positivo, negativo o cero); cada caso da una geometría distinta.",
              },
              {
                  "enunciado_md": "$A$ es invertible $\\iff$:",
                  "opciones_md": [
                      "$0$ es valor propio de $A$",
                      "$0$ NO es valor propio de $A$",
                      "Todos los valores propios son positivos",
                      "$\\det A = 1$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\lambda = 0 \\iff \\det(A) = 0$.",
                  "explicacion_md": "**$0$ no es valor propio.** Equivalentemente, $\\det A \\neq 0$ (TMI extendido).",
              },
              {
                  "enunciado_md": "Si $A$ es triangular con diagonal $(3, 5, -2, 5)$, ¿cuáles son los valores propios y sus multiplicidades algebraicas?",
                  "opciones_md": [
                      "$\\lambda = 3$ (mult. 1), $\\lambda = 5$ (mult. 2), $\\lambda = -2$ (mult. 1)",
                      "$\\lambda = 11$ (mult. 4)",
                      "Solo $\\lambda = 5$",
                      "No tiene valores propios reales",
                  ],
                  "correcta": "A",
                  "pista_md": "Diagonal de triangular = valores propios; cada repetición = multiplicidad.",
                  "explicacion_md": "**$\\lambda = 3$ (1 vez), $\\lambda = 5$ (2 veces), $\\lambda = -2$ (1 vez).** Suma: $4$ ✓.",
              },
          ]),

        ej(
            "Calcular valores propios $2\\times 2$",
            "Halla los valores propios de $A = \\begin{bmatrix} 5 & -1 \\\\ 4 & 1 \\end{bmatrix}$.",
            [
                "Plantea $\\det(A - \\lambda I) = 0$.",
                "Resuelve la ecuación cuadrática.",
            ],
            (
                "$\\det\\begin{bmatrix} 5 - \\lambda & -1 \\\\ 4 & 1 - \\lambda \\end{bmatrix} = (5-\\lambda)(1-\\lambda) + 4 = \\lambda^2 - 6\\lambda + 9 = (\\lambda - 3)^2 = 0$.\n\n"
                "**$\\lambda = 3$** con multiplicidad algebraica $2$."
            ),
        ),

        ej(
            "Espacio propio explícito",
            "Para $A$ del ejercicio anterior y $\\lambda = 3$, halla una base de $E_3$.",
            [
                "Resuelve $(A - 3I)\\vec{x} = \\vec{0}$.",
            ],
            (
                "$A - 3I = \\begin{bmatrix} 2 & -1 \\\\ 4 & -2 \\end{bmatrix} \\sim \\begin{bmatrix} 2 & -1 \\\\ 0 & 0 \\end{bmatrix}$.\n\n"
                "$2x_1 - x_2 = 0 \\Rightarrow x_2 = 2x_1$. $\\vec{x} = x_1(1, 2)^T$.\n\n"
                "**Base de $E_3$:** $\\{(1, 2)^T\\}$. **$\\dim E_3 = 1 < m_a(3) = 2$** $\\Rightarrow$ **deficiencia geométrica** (la matriz no será diagonalizable)."
            ),
        ),

        ej(
            "Polinomio característico $3\\times 3$",
            "Encuentra los valores propios de $A = \\begin{bmatrix} 4 & 0 & 1 \\\\ -2 & 1 & 0 \\\\ -2 & 0 & 1 \\end{bmatrix}$.",
            [
                "Expande $\\det(A - \\lambda I)$ por una columna con ceros.",
                "Factoriza el polinomio cúbico.",
            ],
            (
                "$\\det(A - \\lambda I) = \\det\\begin{bmatrix} 4-\\lambda & 0 & 1 \\\\ -2 & 1-\\lambda & 0 \\\\ -2 & 0 & 1-\\lambda \\end{bmatrix}$. Expandiendo por la columna $2$ (un solo término no nulo):\n\n"
                "$= (1-\\lambda)\\det\\begin{bmatrix} 4-\\lambda & 1 \\\\ -2 & 1-\\lambda \\end{bmatrix} = (1-\\lambda)[(4-\\lambda)(1-\\lambda) + 2] = (1-\\lambda)(\\lambda^2 - 5\\lambda + 6) = (1-\\lambda)(\\lambda - 2)(\\lambda - 3)$.\n\n"
                "**Valores propios:** $\\lambda = 1, 2, 3$ — tres distintos."
            ),
        ),

        fig(
            "Diagrama matemático con dos paneles lado a lado. Panel izquierdo: cuadrícula 2D antes de aplicar A, "
            "con varios vectores grises desde el origen apuntando en distintas direcciones. Resaltar dos vectores "
            "especiales: v1 en teal #06b6d4 y v2 en ámbar #f59e0b. Panel derecho: la misma cuadrícula deformada "
            "por A. Los vectores grises ahora cambiaron de dirección, pero v1 y v2 siguen sobre las mismas rectas "
            "originales, solo estirados por factores λ1 y λ2. Etiquetas 'Av1 = λ1 v1' y 'Av2 = λ2 v2'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Considerar $\\vec{v} = \\vec{0}$ como vector propio.** Por definición, los vectores propios son **no nulos**.",
              "**Olvidar que $\\lambda = 0$ es un valor propio válido** (no como vector propio): significa que $A$ es singular.",
              "**Confundir multiplicidad algebraica con geométrica.** Algebraica = exponente en el polinomio; geométrica = $\\dim E_\\lambda$. Pueden ser distintas.",
              "**Pensar que matrices con los mismos valores propios son similares.** **Falso** — la similitud es una condición más fuerte.",
              "**Aplicar OEF a $A$ para 'simplificar' antes de calcular valores propios.** Las OEF **cambian** los valores propios. Para calcular el polinomio característico, no se reduce $A$.",
              "**Olvidar que el polinomio característico tiene grado $n$.** Para $A \\in \\mathbb{R}^{n\\times n}$, $p_A(\\lambda)$ tiene grado exactamente $n$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Vector propio:** $\\vec{v} \\neq \\vec{0}$ con $A\\vec{v} = \\lambda \\vec{v}$. **Valor propio:** $\\lambda$.",
              "**Espacio propio:** $E_\\lambda = \\text{Nul}(A - \\lambda I)$, subespacio de $\\mathbb{R}^n$.",
              "**Triangular:** valores propios = entradas de la diagonal.",
              "**$0$ es valor propio $\\iff A$ no invertible** (extensión TMI).",
              "**Vectores propios de $\\lambda$ distintos son LI.**",
              "**Ecuación característica:** $\\det(A - \\lambda I) = 0$. Polinomio $p_A(\\lambda)$ de grado $n$.",
              "**Multiplicidades:** algebraica $m_a(\\lambda)$ (exponente) $\\geq$ geométrica $m_g(\\lambda) = \\dim E_\\lambda \\geq 1$.",
              "**Similaridad:** $A \\sim B$ si $A = PBP^{-1}$ — preserva el polinomio característico.",
              "**Próxima lección:** **diagonalización** $A = PDP^{-1}$, posible $\\iff$ hay $n$ vectores propios LI.",
          ]),
    ]
    return {
        "id": "lec-al-6-1-ecuacion-caracteristica",
        "title": "Ecuación característica",
        "description": "Vectores y valores propios, espacio propio $E_\\lambda$, ecuación $\\det(A - \\lambda I) = 0$, multiplicidad algebraica vs geométrica, similitud y conservación del polinomio característico.",
        "blocks": blocks,
        "duration_minutes": 65,
        "order": 1,
    }


# =====================================================================
# 6.2 Diagonalización
# =====================================================================
def lesson_6_2():
    blocks = [
        b("texto", body_md=(
            "**Diagonalizar** una matriz $A$ significa encontrar una matriz invertible $P$ y una matriz "
            "**diagonal** $D$ tales que $A = PDP^{-1}$. Cuando esto es posible, $A$ se entiende como "
            "una **transformación de escalas independientes** en una base adecuada (las columnas de $P$).\n\n"
            "**¿Por qué importa diagonalizar?**\n\n"
            "- Calcular **potencias de matrices** se vuelve trivial: $A^k = PD^kP^{-1}$, y $D^k$ es elevar la diagonal entrada por entrada.\n"
            "- Resolver **sistemas dinámicos lineales** $\\vec{x}_{t+1} = A\\vec{x}_t$ — la solución general es $\\vec{x}_t = A^t \\vec{x}_0 = PD^tP^{-1}\\vec{x}_0$.\n"
            "- En **ecuaciones diferenciales** $\\dot{\\vec{x}} = A\\vec{x}$, la solución es $\\vec{x}(t) = e^{At}\\vec{x}_0$ con $e^{At} = Pe^{Dt}P^{-1}$.\n"
            "- En **mecánica cuántica**, **estadística** y **machine learning** (PCA), diagonalizar es entender los modos fundamentales del problema.\n\n"
            "Al terminar:\n\n"
            "- Conoces el **teorema de diagonalización**: $A$ diagonalizable $\\iff$ tiene $n$ vectores propios LI.\n"
            "- Aplicas el **algoritmo en 4 pasos** para diagonalizar.\n"
            "- Distingues casos diagonalizables vs no diagonalizables (deficiencia geométrica).\n"
            "- Sabes que $n$ valores propios distintos $\\Rightarrow$ siempre diagonalizable."
        )),

        b("teorema",
          nombre="Teorema de diagonalización",
          enunciado_md=(
              "Una matriz $A \\in \\mathbb{R}^{n\\times n}$ es **diagonalizable** $\\iff$ tiene **$n$ vectores propios linealmente independientes**.\n\n"
              "En tal caso,\n\n"
              "$$\\boxed{A = P D P^{-1},}$$\n\n"
              "donde:\n\n"
              "- $P = [\\,\\vec{v}_1\\ \\cdots\\ \\vec{v}_n\\,]$ tiene como columnas los vectores propios LI.\n"
              "- $D = \\text{diag}(\\lambda_1, \\ldots, \\lambda_n)$ tiene los valores propios correspondientes en la diagonal.\n\n"
              "**Importante:** el orden de las columnas de $P$ y de las entradas de $D$ debe **coincidir** — el $i$-ésimo vector propio en $P$ corresponde al $i$-ésimo valor propio en $D$."
          ),
          demostracion_md=(
              "**($\\Leftarrow$)** Si $A\\vec{v}_i = \\lambda_i \\vec{v}_i$ para $i = 1, \\ldots, n$ con $\\vec{v}_i$ LI, entonces $AP = [A\\vec{v}_1\\ \\cdots\\ A\\vec{v}_n] = [\\lambda_1 \\vec{v}_1\\ \\cdots\\ \\lambda_n \\vec{v}_n] = PD$. Como $P$ tiene columnas LI, es invertible, así $A = PDP^{-1}$.\n\n"
              "**($\\Rightarrow$)** Si $A = PDP^{-1}$, entonces $AP = PD$, lo que implica $A\\vec{v}_i = \\lambda_i \\vec{v}_i$ para cada columna $\\vec{v}_i$ de $P$. Como $P$ es invertible, sus columnas son LI. $\\blacksquare$"
          )),

        b("intuicion", body_md=(
            "**Por qué diagonalizar simplifica las potencias.** Si $A = PDP^{-1}$, entonces\n\n"
            "$A^2 = (PDP^{-1})(PDP^{-1}) = PD(P^{-1}P)DP^{-1} = PD^2P^{-1}$.\n\n"
            "Por inducción, $\\boxed{A^k = PD^kP^{-1}}$ para todo $k \\geq 1$.\n\n"
            "Y $D^k$ es trivial: si $D = \\text{diag}(\\lambda_1, \\ldots, \\lambda_n)$, entonces $D^k = \\text{diag}(\\lambda_1^k, \\ldots, \\lambda_n^k)$.\n\n"
            "**Lo que era $O(n^3)$ por iteración de Gauss se vuelve $O(n)$** una vez diagonalizado."
        )),

        b("ejemplo_resuelto",
          titulo="Potencia de matriz diagonal",
          problema_md=(
              "Si $D = \\begin{bmatrix} 5 & 0 \\\\ 0 & 3 \\end{bmatrix}$, calcula $D^2$, $D^3$ y $D^k$ en general."
          ),
          pasos=[
              {"accion_md": (
                  "$D^2 = \\begin{bmatrix} 5 & 0 \\\\ 0 & 3 \\end{bmatrix}\\begin{bmatrix} 5 & 0 \\\\ 0 & 3 \\end{bmatrix} = \\begin{bmatrix} 25 & 0 \\\\ 0 & 9 \\end{bmatrix} = \\begin{bmatrix} 5^2 & 0 \\\\ 0 & 3^2 \\end{bmatrix}$. Análogamente $D^3 = \\begin{bmatrix} 125 & 0 \\\\ 0 & 27 \\end{bmatrix}$."
              ),
               "justificacion_md": "Cada entrada diagonal se eleva independientemente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Fórmula general:** $D^k = \\begin{bmatrix} 5^k & 0 \\\\ 0 & 3^k \\end{bmatrix}$ para todo $k \\geq 1$."
              ),
               "justificacion_md": "**Patrón clave:** las potencias de matriz diagonal son triviales — esa es toda la motivación de diagonalizar.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Algoritmo de diagonalización",
          enunciado_md=(
              "Para diagonalizar una matriz $A \\in \\mathbb{R}^{n\\times n}$:\n\n"
              "**Paso 1.** Calcular los **valores propios** resolviendo $\\det(A - \\lambda I) = 0$.\n\n"
              "**Paso 2.** Para cada valor propio $\\lambda$, hallar una **base del espacio propio** $E_\\lambda = \\text{Nul}(A - \\lambda I)$.\n\n"
              "**Paso 3.** Si la unión de las bases tiene **$n$ vectores LI**, formar $P = [\\,\\vec{v}_1\\ \\cdots\\ \\vec{v}_n\\,]$. Si no llega a $n$, **$A$ no es diagonalizable**.\n\n"
              "**Paso 4.** Construir $D = \\text{diag}(\\lambda_1, \\ldots, \\lambda_n)$ con los valores propios en el **mismo orden** que los vectores propios en $P$.\n\n"
              "**Verificación:** $AP = PD$ (equivalente a $A = PDP^{-1}$)."
          )),

        b("ejemplo_resuelto",
          titulo="Diagonalización exitosa",
          problema_md=(
              "Diagonalizar $A = \\begin{bmatrix} 1 & 3 & 3 \\\\ -3 & -5 & -3 \\\\ 3 & 3 & 1 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1.** Polinomio característico: $\\det(A - \\lambda I) = -(\\lambda - 1)(\\lambda + 2)^2$. **Valores propios:** $\\lambda_1 = 1$ (mult. alg. 1) y $\\lambda_2 = -2$ (mult. alg. 2)."
              ),
               "justificacion_md": "Cómputo del polinomio (omitido por extensión).",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2.** Espacios propios:\n\n"
                  "- $E_1$: resolver $(A - I)\\vec{x} = \\vec{0}$ da base $\\vec{v}_1 = (1, -1, 1)^T$.\n"
                  "- $E_{-2}$: resolver $(A + 2I)\\vec{x} = \\vec{0}$ da base $\\{\\vec{v}_2, \\vec{v}_3\\} = \\{(-1, 1, 0)^T, (-1, 0, 1)^T\\}$.\n\n"
                  "**$\\dim E_1 = 1, \\dim E_{-2} = 2$**, total $3$ vectores."
              ),
               "justificacion_md": "$m_g(-2) = 2 = m_a(-2)$ — **no hay deficiencia geométrica**.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3.** Los $3$ vectores son LI (en general, vectores de distintos espacios propios son LI). Formamos:\n\n"
                  "$P = \\begin{bmatrix} 1 & -1 & -1 \\\\ -1 & 1 & 0 \\\\ 1 & 0 & 1 \\end{bmatrix}, \\quad D = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & -2 & 0 \\\\ 0 & 0 & -2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "El **orden importa**: $\\lambda = 1$ corresponde a la primera columna de $P$, $\\lambda = -2$ a la segunda y tercera.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación rápida:** $AP$ debe coincidir con $PD$. La columna $1$ de $AP$ es $A\\vec{v}_1 = 1 \\cdot \\vec{v}_1$ ✓; la 2ª es $-2\\vec{v}_2$ ✓; la 3ª es $-2\\vec{v}_3$ ✓.\n\n"
                  "**$A = PDP^{-1}$.** Diagonalización completa."
              ),
               "justificacion_md": "**$A$ es diagonalizable** porque encontramos los $3$ vectores propios LI necesarios.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Matriz NO diagonalizable",
          problema_md=(
              "Decide si $A = \\begin{bmatrix} 2 & 4 & 3 \\\\ -4 & -6 & -3 \\\\ 3 & 3 & 1 \\end{bmatrix}$ es diagonalizable."
          ),
          pasos=[
              {"accion_md": (
                  "Polinomio característico: $-(\\lambda - 1)(\\lambda + 2)^2$ — **mismos valores propios** que el ejemplo anterior."
              ),
               "justificacion_md": "Mismas multiplicidades algebraicas: $m_a(1) = 1, m_a(-2) = 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "Espacios propios:\n\n"
                  "- $E_1$: base $\\vec{v}_1 = (1, -1, 1)^T$ ($m_g(1) = 1$).\n"
                  "- $E_{-2}$: resolviendo $(A + 2I)\\vec{x} = \\vec{0}$ se obtiene **una sola** dirección, $\\vec{v}_2 = (-1, 1, 0)^T$ ($m_g(-2) = 1$).\n\n"
                  "**Solo $2$ vectores propios LI en total** — no llega a $3$."
              ),
               "justificacion_md": "$m_g(-2) = 1 < 2 = m_a(-2)$ $\\Rightarrow$ **deficiencia geométrica**.",
               "es_resultado": False},
              {"accion_md": (
                  "Por el teorema de diagonalización, **$A$ NO es diagonalizable**."
              ),
               "justificacion_md": "**La misma ecuación característica no garantiza diagonalizabilidad** — depende de las multiplicidades geométricas.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Condición suficiente: $n$ valores propios distintos",
          enunciado_md=(
              "Si $A \\in \\mathbb{R}^{n \\times n}$ tiene **$n$ valores propios distintos**, entonces $A$ es **diagonalizable**.\n\n"
              "**Demostración:** los $n$ vectores propios correspondientes son automáticamente LI (lección 6.1). Por el teorema, $A$ es diagonalizable. $\\blacksquare$\n\n"
              "**Importante:** es solo **suficiente**, no necesaria. Una matriz con valores propios repetidos también puede ser diagonalizable, siempre que las multiplicidades geométricas igualen a las algebraicas (como en el primer ejemplo)."
          )),

        b("ejemplo_resuelto",
          titulo="Triangular con valores propios distintos",
          problema_md=(
              "Decide si $A = \\begin{bmatrix} 5 & -8 & 1 \\\\ 0 & 0 & 7 \\\\ 0 & 0 & -2 \\end{bmatrix}$ es diagonalizable."
          ),
          pasos=[
              {"accion_md": (
                  "$A$ es triangular superior $\\Rightarrow$ valores propios = diagonal: $\\lambda = 5, 0, -2$ — **tres distintos**."
              ),
               "justificacion_md": "Atajo para triangulares.",
               "es_resultado": False},
              {"accion_md": (
                  "Por el teorema de la condición suficiente, **$A$ es diagonalizable** sin necesidad de calcular los espacios propios explícitamente."
              ),
               "justificacion_md": "**Patrón útil:** triangular con diagonal sin entradas repetidas $\\Rightarrow$ diagonalizable automático.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Caracterización completa de diagonalizabilidad",
          enunciado_md=(
              "Sea $A \\in \\mathbb{R}^{n \\times n}$ con valores propios distintos $\\lambda_1, \\ldots, \\lambda_p$ (cada uno con multiplicidad algebraica $m_a(\\lambda_k)$ y geométrica $m_g(\\lambda_k)$). Entonces:\n\n"
              "**(a)** Para cada $\\lambda_k$, $1 \\leq m_g(\\lambda_k) \\leq m_a(\\lambda_k)$.\n\n"
              "**(b)** $A$ es **diagonalizable** $\\iff$ se cumplen ambas:\n\n"
              "- (i) El polinomio característico se factoriza completamente en factores lineales (sobre $\\mathbb{R}$).\n"
              "- (ii) $m_g(\\lambda_k) = m_a(\\lambda_k)$ para **cada** $k$.\n\n"
              "**(c)** Si $A$ es diagonalizable y $\\mathcal{B}_k$ es base de $E_{\\lambda_k}$, entonces $\\mathcal{B}_1 \\cup \\cdots \\cup \\mathcal{B}_p$ es base de $\\mathbb{R}^n$ formada por vectores propios."
          )),

        b("ejemplo_resuelto",
          titulo="Diagonalización con valores repetidos pero suficientes vectores",
          problema_md=(
              "Diagonalizar $A = \\begin{bmatrix} 5 & 0 & 0 & 0 \\\\ 0 & 5 & 0 & 0 \\\\ 1 & 4 & -3 & 0 \\\\ -1 & -2 & 0 & -3 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Triangular inferior con diagonal $(5, 5, -3, -3)$ $\\Rightarrow$ valores propios $\\lambda = 5$ (mult. 2) y $\\lambda = -3$ (mult. 2)."
              ),
               "justificacion_md": "Se cumple (i): el polinomio se factoriza como $(\\lambda - 5)^2(\\lambda + 3)^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolviendo los espacios propios:\n\n"
                  "- $E_5$: base $\\{(-8, 4, 1, 0)^T, (-16, 4, 0, 1)^T\\}$ ($m_g = 2 = m_a$ ✓).\n"
                  "- $E_{-3}$: base $\\{(0, 0, 1, 0)^T, (0, 0, 0, 1)^T\\}$ ($m_g = 2 = m_a$ ✓)."
              ),
               "justificacion_md": "Las multiplicidades geométricas igualan a las algebraicas en cada $\\lambda$.",
               "es_resultado": False},
              {"accion_md": (
                  "Por el teorema, **$A$ es diagonalizable**:\n\n"
                  "$P = \\begin{bmatrix} -8 & -16 & 0 & 0 \\\\ 4 & 4 & 0 & 0 \\\\ 1 & 0 & 1 & 0 \\\\ 0 & 1 & 0 & 1 \\end{bmatrix}, \\quad D = \\text{diag}(5, 5, -3, -3).$"
              ),
               "justificacion_md": "**Lección:** valores propios repetidos no impiden diagonalización — siempre que haya suficientes vectores propios LI.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $A$ es $5\\times 5$ con $5$ valores propios distintos, entonces:",
                  "opciones_md": [
                      "$A$ es siempre diagonalizable",
                      "$A$ nunca es diagonalizable",
                      "Depende de los espacios propios",
                      "$A = I$",
                  ],
                  "correcta": "A",
                  "pista_md": "$n$ valores propios distintos $\\Rightarrow$ diagonalizable.",
                  "explicacion_md": "**Siempre diagonalizable.** Cada $\\lambda$ aporta al menos $1$ vector propio (LI con los demás), totalizando $5$ vectores propios LI.",
              },
              {
                  "enunciado_md": "Para $A = PDP^{-1}$, $A^{10}$ vale:",
                  "opciones_md": [
                      "$P D^{10} P^{-1}$",
                      "$P^{10} D^{10} P^{-10}$",
                      "$10 PDP^{-1}$",
                      "$D^{10}$",
                  ],
                  "correcta": "A",
                  "pista_md": "$A^k = PD^kP^{-1}$ por inducción.",
                  "explicacion_md": "**$A^{10} = PD^{10}P^{-1}$.** Es la **razón principal** para diagonalizar — calcular potencias se vuelve trivial.",
              },
              {
                  "enunciado_md": "Si $A$ es $3 \\times 3$ con $\\lambda = 2$ de mult. alg. $2$ y $\\dim E_2 = 1$, entonces $A$:",
                  "opciones_md": [
                      "Es diagonalizable porque $\\lambda$ es real",
                      "**No** es diagonalizable (deficiencia geométrica)",
                      "Es invertible",
                      "Tiene $3$ valores propios distintos",
                  ],
                  "correcta": "B",
                  "pista_md": "$m_g < m_a \\Rightarrow$ no diagonalizable.",
                  "explicacion_md": "**No diagonalizable.** $m_g(2) = 1 < 2 = m_a(2)$ $\\Rightarrow$ falta un vector propio para totalizar $3$ LI.",
              },
          ]),

        ej(
            "Diagonalizar matriz $2\\times 2$",
            "Diagonaliza $A = \\begin{bmatrix} 7 & 2 \\\\ -4 & 1 \\end{bmatrix}$ y úsalo para hallar $A^k$.",
            [
                "Calcula valores propios y vectores propios.",
                "Forma $P$ y $D$, calcula $P^{-1}$.",
            ],
            (
                "$\\det(A - \\lambda I) = (7-\\lambda)(1-\\lambda) + 8 = \\lambda^2 - 8\\lambda + 15 = (\\lambda - 5)(\\lambda - 3)$. **Valores propios:** $\\lambda = 5, 3$.\n\n"
                "$E_5$: $(A - 5I)\\vec{x} = \\vec{0}$ con $A - 5I = \\begin{bmatrix} 2 & 2 \\\\ -4 & -4 \\end{bmatrix} \\Rightarrow \\vec{v}_1 = (1, -1)^T$.\n\n"
                "$E_3$: $(A - 3I)\\vec{x} = \\vec{0}$ con $A - 3I = \\begin{bmatrix} 4 & 2 \\\\ -4 & -2 \\end{bmatrix} \\Rightarrow \\vec{v}_2 = (1, -2)^T$.\n\n"
                "$P = \\begin{bmatrix} 1 & 1 \\\\ -1 & -2 \\end{bmatrix}$, $D = \\begin{bmatrix} 5 & 0 \\\\ 0 & 3 \\end{bmatrix}$, $P^{-1} = \\begin{bmatrix} 2 & 1 \\\\ -1 & -1 \\end{bmatrix}$.\n\n"
                "$A^k = PD^kP^{-1} = \\begin{bmatrix} 2\\cdot 5^k - 3^k & 5^k - 3^k \\\\ -2\\cdot 5^k + 2\\cdot 3^k & -5^k + 2\\cdot 3^k \\end{bmatrix}$."
            ),
        ),

        ej(
            "Verificar no diagonalizable",
            "Demuestra que $A = \\begin{bmatrix} 3 & 1 \\\\ 0 & 3 \\end{bmatrix}$ no es diagonalizable.",
            [
                "Calcula valores propios y dim espacio propio.",
            ],
            (
                "$A$ es triangular con $\\lambda = 3$ doble ($m_a = 2$).\n\n"
                "$A - 3I = \\begin{bmatrix} 0 & 1 \\\\ 0 & 0 \\end{bmatrix} \\Rightarrow$ $x_2 = 0$, $x_1$ libre. $E_3 = \\text{Gen}\\{(1, 0)^T\\}$, $\\dim E_3 = 1$.\n\n"
                "$m_g(3) = 1 < 2 = m_a(3)$ $\\Rightarrow$ **no diagonalizable**. (Es el ejemplo canónico de un 'bloque de Jordan' $2\\times 2$.)"
            ),
        ),

        ej(
            "Aplicación: $A^{100}$",
            "Sea $A = \\begin{bmatrix} 0.5 & 0.3 \\\\ 0.5 & 0.7 \\end{bmatrix}$. Diagonaliza $A$ y calcula $\\lim_{k \\to \\infty} A^k \\vec{x}_0$ con $\\vec{x}_0 = (1, 0)^T$ (matriz estocástica simple).",
            [
                "Halla valores propios. Uno de ellos siempre es $1$ para matrices estocásticas.",
                "Lleva al límite usando $A^k = PD^kP^{-1}$.",
            ],
            (
                "$\\det(A - \\lambda I) = (0.5 - \\lambda)(0.7 - \\lambda) - 0.15 = \\lambda^2 - 1.2\\lambda + 0.2 = (\\lambda - 1)(\\lambda - 0.2)$.\n\n"
                "Vectores propios: $\\vec{v}_1 = (3, 5)^T$ para $\\lambda = 1$ y $\\vec{v}_2 = (1, -1)^T$ para $\\lambda = 0.2$.\n\n"
                "Como $0.2^k \\to 0$ y $1^k = 1$, $A^k \\vec{x}_0 \\to \\dfrac{1}{8}(3, 5)^T \\cdot 8 \\cdot c$ — el componente en la dirección $\\vec{v}_1$ persiste, el otro decae. **Distribución límite:** $(3/8,\\ 5/8)^T$."
            ),
        ),

        fig(
            "Diagrama de pipeline horizontal con tres cuadrículas 2D conectadas por flechas etiquetadas, "
            "ilustrando A = P D P^-1. Primera cuadrícula (izquierda) en base canónica con un vector ámbar "
            "#f59e0b. Flecha hacia la derecha rotulada 'P^-1: cambia a base de autovectores'. Segunda "
            "cuadrícula con ejes en teal #06b6d4 (los autovectores). Flecha 'D: estira por λ1 y λ2'. "
            "Tercera cuadrícula con el mismo vector estirado a lo largo de los ejes teal. Flecha final "
            "'P: vuelve a base canónica'. Cuarta cuadrícula con el resultado A·x. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que toda matriz es diagonalizable.** Solo si tiene $n$ vectores propios LI.",
              "**Confundir orden de columnas en $P$ con valores propios en $D$.** El $i$-ésimo vector propio en $P$ corresponde al $i$-ésimo valor propio en $D$.",
              "**Calcular $A^k$ sin diagonalizar.** Para $k$ grande, sin diagonalización es prohibitivo. Con diagonalización es trivial.",
              "**Olvidar verificar la condición $m_g = m_a$ para cada $\\lambda$.** Es el criterio clave para diagonalizabilidad.",
              "**Asumir que valores propios reales garantizan diagonalización.** Hace falta además multiplicidad geométrica completa.",
              "**Confundir 'diagonal' con 'diagonalizable'.** Una matriz triangular no diagonal puede ser diagonalizable (si tiene valores propios distintos), y una matriz $2I$ ya es diagonal pero solo es similar a sí misma.",
          ]),

        b("resumen",
          puntos_md=[
              "**$A$ diagonalizable $\\iff$ tiene $n$ vectores propios LI** $\\iff A = PDP^{-1}$.",
              "**$P$**: vectores propios como columnas. **$D$**: valores propios en la diagonal (mismo orden).",
              "**Ventaja:** $A^k = PD^kP^{-1}$, y $D^k$ es trivial.",
              "**Algoritmo (4 pasos):** valores propios $\\to$ espacios propios $\\to$ formar $P$ $\\to$ formar $D$.",
              "**$n$ valores propios distintos $\\Rightarrow$ diagonalizable** (suficiente, no necesario).",
              "**No diagonalizable $\\iff$ existe $\\lambda$ con $m_g(\\lambda) < m_a(\\lambda)$** (deficiencia geométrica).",
              "**Próxima lección:** diagonalización **interpretada como cambio de base** y matriz de TL respecto a una base.",
          ]),
    ]
    return {
        "id": "lec-al-6-2-diagonalizacion",
        "title": "Diagonalización",
        "description": "Teorema $A = PDP^{-1}$ con $P$ de vectores propios y $D$ diagonal de valores propios; algoritmo en 4 pasos; condición $n$ valores distintos; casos no diagonalizables (deficiencia geométrica).",
        "blocks": blocks,
        "duration_minutes": 65,
        "order": 2,
    }


# =====================================================================
# 6.3 Vectores propios y transformaciones lineales
# =====================================================================
def lesson_6_3():
    blocks = [
        b("texto", body_md=(
            "En esta lección unimos dos ideas: la **matriz de una transformación lineal respecto a una base** "
            "(generalización del cap. 2) y la **diagonalización** (lección 6.2). El resultado es una "
            "interpretación poderosa: **diagonalizar $A$ significa encontrar la base en la cual $T(\\vec{x}) = A\\vec{x}$ "
            "se ve como una matriz diagonal**.\n\n"
            "En esta nueva base, la transformación es 'simple': cada vector se escala por su valor propio "
            "correspondiente. La elección de base **adecuada** revela la estructura geométrica oculta de $T$.\n\n"
            "Al terminar:\n\n"
            "- Construyes la **matriz $M$ de una TL respecto a bases $\\mathcal{B}, \\mathcal{C}$** ($V \\to W$).\n"
            "- Conoces la **$\\mathcal{B}$-matriz** $[T]_{\\mathcal{B}}$ para TL $V \\to V$.\n"
            "- Interpretas la **diagonalización como un cambio de base**: $D$ es la $\\mathcal{B}$-matriz de $T$ con $\\mathcal{B}$ formada por vectores propios."
        )),

        b("definicion",
          titulo="Matriz de una TL respecto a bases",
          body_md=(
              "Sean $V$ un espacio de dimensión $n$, $W$ uno de dimensión $m$, $T : V \\to W$ una TL, "
              "$\\mathcal{B} = \\{\\vec{b}_1, \\ldots, \\vec{b}_n\\}$ base de $V$ y $\\mathcal{C}$ base de $W$.\n\n"
              "La **matriz de $T$ respecto a $\\mathcal{B}$ y $\\mathcal{C}$** es\n\n"
              "$$\\boxed{M = \\bigl[\\,[T(\\vec{b}_1)]_{\\mathcal{C}}\\ \\ [T(\\vec{b}_2)]_{\\mathcal{C}}\\ \\cdots\\ [T(\\vec{b}_n)]_{\\mathcal{C}}\\,\\bigr] \\in \\mathbb{R}^{m \\times n}.}$$\n\n"
              "Es decir, las **columnas** de $M$ son los **$\\mathcal{C}$-coordenadas de las imágenes** $T(\\vec{b}_j)$.\n\n"
              "**Propiedad clave:**\n\n"
              "$$[T(\\vec{x})]_{\\mathcal{C}} = M\\,[\\vec{x}]_{\\mathcal{B}} \\qquad \\forall \\vec{x} \\in V.$$\n\n"
              "Es la **versión matricial** de $T$ una vez fijadas las bases — todo cálculo en $V$ se reduce a multiplicar por $M$ en $\\mathbb{R}^n$."
          )),

        b("ejemplo_resuelto",
          titulo="Matriz de TL en bases dadas",
          problema_md=(
              "Sean $\\mathcal{B} = \\{\\vec{b}_1, \\vec{b}_2\\}$ base de $V$ y $\\mathcal{C} = \\{\\vec{c}_1, \\vec{c}_2, \\vec{c}_3\\}$ base de $W$. Sea $T : V \\to W$ con $T(\\vec{b}_1) = 3\\vec{c}_1 - 2\\vec{c}_2 + 5\\vec{c}_3$ y $T(\\vec{b}_2) = 4\\vec{c}_1 + 7\\vec{c}_2 - \\vec{c}_3$. Halla la matriz $M$."
          ),
          pasos=[
              {"accion_md": (
                  "Los $\\mathcal{C}$-coordenadas de las imágenes son:\n\n"
                  "$[T(\\vec{b}_1)]_{\\mathcal{C}} = (3, -2, 5)^T, \\quad [T(\\vec{b}_2)]_{\\mathcal{C}} = (4, 7, -1)^T.$"
              ),
               "justificacion_md": "Lectura directa de los coeficientes en la combinación lineal.",
               "es_resultado": False},
              {"accion_md": (
                  "Yuxtaponemos como columnas:\n\n"
                  "$M = \\begin{bmatrix} 3 & 4 \\\\ -2 & 7 \\\\ 5 & -1 \\end{bmatrix} \\in \\mathbb{R}^{3 \\times 2}.$"
              ),
               "justificacion_md": "$M \\in \\mathbb{R}^{m \\times n}$ con $m = \\dim W = 3$, $n = \\dim V = 2$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="$\\mathcal{B}$-matriz para TL $V \\to V$",
          body_md=(
              "Cuando $W = V$ y elegimos $\\mathcal{C} = \\mathcal{B}$ (la **misma** base en ambos lados), la matriz $M$ se llama **$\\mathcal{B}$-matriz para $T$** y se denota $[T]_{\\mathcal{B}}$:\n\n"
              "$$\\boxed{[T]_{\\mathcal{B}} = \\bigl[\\,[T(\\vec{b}_1)]_{\\mathcal{B}}\\ \\cdots\\ [T(\\vec{b}_n)]_{\\mathcal{B}}\\,\\bigr] \\in \\mathbb{R}^{n \\times n}.}$$\n\n"
              "Y se cumple\n\n"
              "$$[T(\\vec{x})]_{\\mathcal{B}} = [T]_{\\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}} \\qquad \\forall \\vec{x} \\in V.$$\n\n"
              "**Cambiar la base $\\mathcal{B}$ produce distintas matrices $[T]_{\\mathcal{B}}$** — todas representan a la misma transformación $T$, pero con distintas 'apariencias'."
          )),

        b("ejemplo_resuelto",
          titulo="$\\mathcal{B}$-matriz del operador derivada",
          problema_md=(
              "Sea $T : \\mathcal{P}_2 \\to \\mathcal{P}_2$ definido por $T(a_0 + a_1 t + a_2 t^2) = a_1 + 2a_2 t$ (derivada). Halla $[T]_{\\mathcal{B}}$ con $\\mathcal{B} = \\{1, t, t^2\\}$ y verifica $[T(p)]_{\\mathcal{B}} = [T]_{\\mathcal{B}}[p]_{\\mathcal{B}}$ para $p$ general."
          ),
          pasos=[
              {"accion_md": (
                  "Calculamos las imágenes de los vectores básicos:\n\n"
                  "$T(1) = 0$, $T(t) = 1$, $T(t^2) = 2t$.\n\n"
                  "$\\mathcal{B}$-coordenadas: $[T(1)]_{\\mathcal{B}} = (0, 0, 0)^T$, $[T(t)]_{\\mathcal{B}} = (1, 0, 0)^T$, $[T(t^2)]_{\\mathcal{B}} = (0, 2, 0)^T$."
              ),
               "justificacion_md": "Cada imagen se escribe como combinación lineal de la base y se leen los coeficientes.",
               "es_resultado": False},
              {"accion_md": (
                  "$[T]_{\\mathcal{B}} = \\begin{bmatrix} 0 & 1 & 0 \\\\ 0 & 0 & 2 \\\\ 0 & 0 & 0 \\end{bmatrix}.$\n\n"
                  "**Esta es la 'matriz de la derivada' en la base estándar de polinomios.**"
              ),
               "justificacion_md": "Cálculo derivativo se transforma en producto matricial — útil para implementaciones numéricas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación con $p(t) = a_0 + a_1 t + a_2 t^2$:** $[p]_{\\mathcal{B}} = (a_0, a_1, a_2)^T$.\n\n"
                  "$[T]_{\\mathcal{B}}[p]_{\\mathcal{B}} = \\begin{bmatrix} 0 & 1 & 0 \\\\ 0 & 0 & 2 \\\\ 0 & 0 & 0 \\end{bmatrix}\\begin{bmatrix} a_0 \\\\ a_1 \\\\ a_2 \\end{bmatrix} = \\begin{bmatrix} a_1 \\\\ 2a_2 \\\\ 0 \\end{bmatrix} = [a_1 + 2a_2 t]_{\\mathcal{B}} = [T(p)]_{\\mathcal{B}}$ ✓."
              ),
               "justificacion_md": "Consistencia confirmada — derivar $p$ equivale a multiplicar sus coordenadas por $[T]_{\\mathcal{B}}$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Diagonalización como cambio de base",
          enunciado_md=(
              "Sea $A = PDP^{-1}$ una diagonalización con $D$ diagonal. Si $\\mathcal{B} = \\{\\vec{v}_1, \\ldots, \\vec{v}_n\\}$ es la base de $\\mathbb{R}^n$ formada por las columnas de $P$ (los vectores propios), entonces\n\n"
              "$$\\boxed{[T]_{\\mathcal{B}} = D,}$$\n\n"
              "donde $T(\\vec{x}) = A\\vec{x}$. Es decir, la **$\\mathcal{B}$-matriz de $T$ es diagonal** (con los valores propios en la diagonal).\n\n"
              "**Lectura geométrica:** la transformación $T$, vista en la base de vectores propios, es **trivialmente** una escala independiente en cada dirección $\\vec{v}_i$ por factor $\\lambda_i$."
          ),
          demostracion_md=(
              "Como $\\vec{v}_i$ es vector propio con valor $\\lambda_i$, $T(\\vec{v}_i) = A\\vec{v}_i = \\lambda_i \\vec{v}_i$. En la base $\\mathcal{B}$:\n\n"
              "$[T(\\vec{v}_i)]_{\\mathcal{B}} = [\\lambda_i \\vec{v}_i]_{\\mathcal{B}} = \\lambda_i [\\vec{v}_i]_{\\mathcal{B}} = \\lambda_i \\vec{e}_i$.\n\n"
              "Las columnas de $[T]_{\\mathcal{B}}$ son $\\lambda_i \\vec{e}_i$, formando la matriz diagonal $D = \\text{diag}(\\lambda_1, \\ldots, \\lambda_n)$. $\\blacksquare$"
          )),

        b("intuicion", body_md=(
            "**El significado profundo de la diagonalización.** Tenemos dos formas de hacer la misma transformación:\n\n"
            "- **En la base estándar:** $\\vec{x} \\mapsto A\\vec{x}$ — multiplicación matricial general (puede ser compleja).\n"
            "- **En la base de vectores propios:** $[\\vec{x}]_{\\mathcal{B}} \\mapsto D[\\vec{x}]_{\\mathcal{B}}$ — solo escalar cada coordenada.\n\n"
            "**Las dos representaciones describen la misma TL.** La diagonal es 'la misma transformación con anteojos mejores'.\n\n"
            "**Cambio de coordenadas explícito:** si $P$ es la matriz de cambio de coordenadas $\\mathcal{B} \\to$ estándar, entonces:\n\n"
            "$\\vec{x}_{\\text{estándar}} \\xrightarrow{P^{-1}} [\\vec{x}]_{\\mathcal{B}} \\xrightarrow{D} [T(\\vec{x})]_{\\mathcal{B}} \\xrightarrow{P} T(\\vec{x})_{\\text{estándar}}$.\n\n"
            "Componiendo: $A = PDP^{-1}$ — exactamente la fórmula de diagonalización."
        )),

        b("ejemplo_resuelto",
          titulo="Encontrar base donde $T$ es diagonal",
          problema_md=(
              "Sea $T : \\mathbb{R}^2 \\to \\mathbb{R}^2$ con $T(\\vec{x}) = A\\vec{x}$ y $A = \\begin{bmatrix} 7 & 2 \\\\ -4 & 1 \\end{bmatrix}$. Encuentra una base $\\mathcal{B}$ tal que $[T]_{\\mathcal{B}}$ sea diagonal."
          ),
          pasos=[
              {"accion_md": (
                  "Diagonalizar $A$. Polinomio: $(\\lambda - 5)(\\lambda - 3) = 0$. Vectores propios: $\\vec{v}_1 = (1, -1)^T$ para $\\lambda = 5$, $\\vec{v}_2 = (1, -2)^T$ para $\\lambda = 3$."
              ),
               "justificacion_md": "Mismos cálculos que en lección 6.2.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\mathcal{B} = \\{\\vec{v}_1, \\vec{v}_2\\}$.** En esta base, $[T]_{\\mathcal{B}} = D = \\begin{bmatrix} 5 & 0 \\\\ 0 & 3 \\end{bmatrix}.$\n\n"
                  "**Geométricamente:** $T$ multiplica por $5$ en la dirección de $\\vec{v}_1$ y por $3$ en la dirección de $\\vec{v}_2$. Sin rotación, sin mezcla."
              ),
               "justificacion_md": "**Esa es la potencia de la diagonalización:** descubrir las direcciones 'naturales' de la transformación.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Las columnas de la matriz $[T]_{\\mathcal{B}}$ son:",
                  "opciones_md": [
                      "Los vectores $\\vec{b}_i$",
                      "Los $T(\\vec{b}_i)$ en coordenadas estándar",
                      "Los **$\\mathcal{B}$-coordenadas** de los $T(\\vec{b}_i)$",
                      "Los valores propios de $T$",
                  ],
                  "correcta": "C",
                  "pista_md": "La matriz traduce $[\\vec{x}]_{\\mathcal{B}} \\to [T(\\vec{x})]_{\\mathcal{B}}$.",
                  "explicacion_md": "**$[T(\\vec{b}_j)]_{\\mathcal{B}}$ como columnas.** Esto es lo que hace que $[T]_{\\mathcal{B}}\\vec{e}_j = [T(\\vec{b}_j)]_{\\mathcal{B}}$.",
              },
              {
                  "enunciado_md": "Si $A = PDP^{-1}$ y $\\mathcal{B}$ son las columnas de $P$, entonces $[T]_{\\mathcal{B}}$ vale:",
                  "opciones_md": ["$A$", "$D$", "$P$", "$P^{-1}$"],
                  "correcta": "B",
                  "pista_md": "En la base de vectores propios, la matriz se vuelve diagonal.",
                  "explicacion_md": "**$[T]_{\\mathcal{B}} = D$.** Esa es la interpretación geométrica de la diagonalización.",
              },
              {
                  "enunciado_md": "El operador derivada $T : \\mathcal{P}_n \\to \\mathcal{P}_n$ tiene $[T]_{\\mathcal{B}}$ con la base estándar:",
                  "opciones_md": [
                      "Diagonal con $0, 1, 2, \\ldots, n$",
                      "Con $1$'s sobre la diagonal y $0$'s en la diagonal",
                      "**Triangular superior** con la subdiagonal $1, 2, \\ldots, n$ y ceros en la diagonal",
                      "La identidad",
                  ],
                  "correcta": "C",
                  "pista_md": "$T(t^k) = k t^{k-1}$.",
                  "explicacion_md": "**Triangular superior estricta** con subdiagonal $1, 2, \\ldots, n$ (corresponde a la derivada de cada $t^k$). Es **nilpotente** ($[T]^{n+1} = 0$): derivar $n+1$ veces un polinomio de grado $n$ da cero.",
              },
          ]),

        ej(
            "Matriz de TL respecto a bases",
            "Sea $T : \\mathbb{R}^2 \\to \\mathbb{R}^3$ con $T(\\vec{x}) = (x_1 + x_2, 2x_1, -x_2)$. Halla $M$ respecto a las bases estándar $\\mathcal{B} = \\{\\vec{e}_1, \\vec{e}_2\\}$ y $\\mathcal{C} = \\{\\vec{e}_1, \\vec{e}_2, \\vec{e}_3\\}$.",
            [
                "Calcula $T(\\vec{e}_1)$ y $T(\\vec{e}_2)$.",
                "Las columnas de $M$ son sus $\\mathcal{C}$-coordenadas.",
            ],
            (
                "$T(\\vec{e}_1) = T(1, 0) = (1, 2, 0)$. $T(\\vec{e}_2) = T(0, 1) = (1, 0, -1)$.\n\n"
                "Como $\\mathcal{C}$ es la base estándar de $\\mathbb{R}^3$, los $\\mathcal{C}$-coordenadas son los vectores mismos.\n\n"
                "$M = \\begin{bmatrix} 1 & 1 \\\\ 2 & 0 \\\\ 0 & -1 \\end{bmatrix}$. Coincide con la matriz estándar de $T$."
            ),
        ),

        ej(
            "$\\mathcal{B}$-matriz en base no estándar",
            "Sea $T : \\mathbb{R}^2 \\to \\mathbb{R}^2$ con $T(\\vec{x}) = A\\vec{x}$ donde $A = \\begin{bmatrix} 4 & -2 \\\\ 1 & 1 \\end{bmatrix}$. Halla $[T]_{\\mathcal{B}}$ con $\\mathcal{B} = \\{(1, 1)^T, (1, 2)^T\\}$.",
            [
                "Calcula $T(\\vec{b}_1)$ y $T(\\vec{b}_2)$.",
                "Halla sus $\\mathcal{B}$-coordenadas resolviendo sistemas.",
            ],
            (
                "$T(\\vec{b}_1) = A(1,1)^T = (2, 2)^T = 2(1, 1)^T = 2\\vec{b}_1 + 0\\vec{b}_2 \\Rightarrow [T(\\vec{b}_1)]_{\\mathcal{B}} = (2, 0)^T$.\n\n"
                "$T(\\vec{b}_2) = A(1, 2)^T = (0, 3)^T$. Resolviendo $\\alpha(1,1) + \\beta(1,2) = (0, 3)$: $\\beta = 3$, $\\alpha = -3$. $[T(\\vec{b}_2)]_{\\mathcal{B}} = (-3, 3)^T$.\n\n"
                "$[T]_{\\mathcal{B}} = \\begin{bmatrix} 2 & -3 \\\\ 0 & 3 \\end{bmatrix}.$ (Triangular: $\\vec{b}_1$ es vector propio con $\\lambda = 2$.)"
            ),
        ),

        ej(
            "Operador derivada en otra base",
            "Sea $T : \\mathcal{P}_2 \\to \\mathcal{P}_2$ derivar. Halla $[T]_{\\mathcal{B}}$ con $\\mathcal{B} = \\{1, 1+t, 1+t+t^2\\}$.",
            [
                "Calcula $T(\\vec{b}_i)$ y exprésalos en base $\\mathcal{B}$.",
            ],
            (
                "$T(1) = 0$, $T(1+t) = 1$, $T(1+t+t^2) = 1 + 2t = 1 + 2((1+t) - 1) = -1 + 2(1+t)$. En base $\\mathcal{B}$:\n\n"
                "$[T(1)]_{\\mathcal{B}} = (0, 0, 0)^T$, $[T(1+t)]_{\\mathcal{B}} = (1, 0, 0)^T$, $[T(1+t+t^2)]_{\\mathcal{B}} = (-1, 2, 0)^T$.\n\n"
                "$[T]_{\\mathcal{B}} = \\begin{bmatrix} 0 & 1 & -1 \\\\ 0 & 0 & 2 \\\\ 0 & 0 & 0 \\end{bmatrix}$.\n\n"
                "Distinta apariencia que en la base estándar, pero misma transformación abstracta."
            ),
        ),

        fig(
            "Diagrama matemático con dos paneles lado a lado mostrando la misma transformación T en dos bases. "
            "Panel izquierdo: cuadrícula canónica con ejes negros, vector x deformado por una matriz 'fea' A "
            "con entradas mezcladas; arriba el rótulo '[T]_canónica = A' y la matriz 2x2 con cuatro entradas "
            "no nulas. Panel derecho: cuadrícula con ejes oblicuos teal #06b6d4 y ámbar #f59e0b (los "
            "autovectores v1, v2); el mismo vector se estira solo a lo largo de esos ejes; arriba "
            "'[T]_B = D' con la matriz diagonal diag(λ1, λ2). Mensaje inferior centrado: 'la base correcta "
            "diagonaliza T'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar pasar a $\\mathcal{C}$-coordenadas.** Las columnas de $M$ son **coordenadas**, no los vectores $T(\\vec{b}_j)$ en sí.",
              "**Confundir matrices con bases distintas.** $A$ es la matriz de $T$ en la **base estándar**; $[T]_{\\mathcal{B}}$ es en otra base. Distintas matrices, **misma transformación**.",
              "**Pensar que toda $\\mathcal{B}$-matriz es diagonal.** Solo si $\\mathcal{B}$ es base de **vectores propios** y $T$ es diagonalizable.",
              "**Olvidar que $\\dim V = \\dim W = n$ se requiere para $[T]_{\\mathcal{B}}$.** Para TL $V \\to W$ con dimensiones distintas, hay que usar $M$ con dos bases.",
          ]),

        b("resumen",
          puntos_md=[
              "**Matriz de TL:** $M = [\\,[T(\\vec{b}_j)]_{\\mathcal{C}}\\,]$ — columnas = $\\mathcal{C}$-coordenadas de imágenes.",
              "**Propiedad:** $[T(\\vec{x})]_{\\mathcal{C}} = M[\\vec{x}]_{\\mathcal{B}}$.",
              "**$\\mathcal{B}$-matriz** $[T]_{\\mathcal{B}}$ (caso $V \\to V$, $\\mathcal{C} = \\mathcal{B}$).",
              "**Diagonalización como cambio de base:** $A = PDP^{-1}$ con $\\mathcal{B}$ formada por las columnas de $P$ $\\Rightarrow [T]_{\\mathcal{B}} = D$.",
              "**Lectura geométrica:** en la base de vectores propios, $T$ es **escalar independiente** en cada dirección.",
              "**Próxima lección:** valores propios **complejos** — qué pasa cuando el polinomio característico tiene raíces no reales.",
          ]),
    ]
    return {
        "id": "lec-al-6-3-vectores-tl",
        "title": "Vectores propios y transformaciones lineales",
        "description": "Matriz de una TL $V \\to W$ respecto a bases $\\mathcal{B}, \\mathcal{C}$, $\\mathcal{B}$-matriz $[T]_{\\mathcal{B}}$ para TL $V \\to V$, diagonalización como cambio de base.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 6.4 Valores propios complejos
# =====================================================================
def lesson_6_4():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora hemos restringido valores propios a **números reales**. Pero el polinomio "
            "característico de una matriz real puede tener **raíces complejas**, y de hecho, **toda matriz "
            "$n \\times n$ tiene exactamente $n$ valores propios** (contando multiplicidades) si admitimos "
            "raíces en $\\mathbb{C}$.\n\n"
            "**Por qué nos importa:**\n\n"
            "- Sistemas dinámicos con **rotaciones** o **oscilaciones** tienen valores propios complejos.\n"
            "- En vibraciones mecánicas, circuitos eléctricos y mecánica cuántica, los valores propios "
            "complejos $\\lambda = a \\pm bi$ codifican **frecuencia** ($b$) y **amortiguamiento** ($a$).\n"
            "- Permiten diagonalizar matrices que no son diagonalizables sobre $\\mathbb{R}$.\n\n"
            "Para matrices reales $2 \\times 2$ con valores propios complejos, hay un **resultado especial**: "
            "$A = PCP^{-1}$ donde $C$ es una **matriz de rotación-escala** — la transformación es esencialmente una "
            "**rotación combinada con un escalado**.\n\n"
            "Al terminar:\n\n"
            "- Trabajas con vectores propios complejos en $\\mathbb{C}^n$.\n"
            "- Manejas **partes real e imaginaria** $\\text{Re}\\,\\vec{v}, \\text{Im}\\,\\vec{v}$.\n"
            "- Aplicas el **Teorema 9** para descomponer matrices reales $2\\times 2$ con valores propios complejos."
        )),

        b("definicion",
          titulo="Valores y vectores propios complejos",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{n\\times n}$. Si admitimos $\\mathbb{C}^n$ como dominio, la teoría de valores propios se extiende sin cambios: $\\lambda \\in \\mathbb{C}$ es un **valor propio complejo** $\\iff$ existe $\\vec{x} \\in \\mathbb{C}^n$ no nulo con\n\n"
              "$$A\\vec{x} = \\lambda \\vec{x}.$$\n\n"
              "**Hecho clave:** la ecuación característica $\\det(A - \\lambda I) = 0$ es un polinomio de grado $n$ y, por el **Teorema Fundamental del Álgebra**, tiene **exactamente $n$ raíces** en $\\mathbb{C}$ (contando multiplicidades).\n\n"
              "**Pares conjugados.** Para $A$ con entradas **reales**, los valores propios complejos vienen en **pares conjugados**: si $\\lambda = a + bi$ es valor propio con vector propio $\\vec{v}$, entonces $\\bar{\\lambda} = a - bi$ también es valor propio con vector propio $\\bar{\\vec{v}}$ (conjugado componente a componente)."
          )),

        b("ejemplo_resuelto",
          titulo="Rotación de $90°$ en $\\mathbb{R}^2$",
          problema_md=(
              "Sea $A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}$ (rotación $90°$ antihoraria). Halla sus valores y vectores propios."
          ),
          pasos=[
              {"accion_md": (
                  "Polinomio característico: $\\det(A - \\lambda I) = \\det\\begin{bmatrix} -\\lambda & -1 \\\\ 1 & -\\lambda \\end{bmatrix} = \\lambda^2 + 1 = 0$.\n\n"
                  "**Raíces complejas:** $\\lambda = i$ y $\\lambda = -i$ (par conjugado)."
              ),
               "justificacion_md": "**Geométricamente esperable:** una rotación pura no tiene direcciones invariantes en $\\mathbb{R}^2$ — los valores propios son no reales.",
               "es_resultado": False},
              {"accion_md": (
                  "**Vector propio para $\\lambda = i$:** resolver $(A - iI)\\vec{v} = \\vec{0}$ con $A - iI = \\begin{bmatrix} -i & -1 \\\\ 1 & -i \\end{bmatrix}$. Una solución: $\\vec{v}_1 = (1, -i)^T$.\n\n"
                  "**Vector propio para $\\lambda = -i$:** $\\vec{v}_2 = \\bar{\\vec{v}}_1 = (1, i)^T$."
              ),
               "justificacion_md": "Los vectores propios para valores propios conjugados son **vectores conjugados**.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación:** $A\\vec{v}_1 = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}\\begin{bmatrix} 1 \\\\ -i \\end{bmatrix} = \\begin{bmatrix} i \\\\ 1 \\end{bmatrix} = i\\begin{bmatrix} 1 \\\\ -i \\end{bmatrix} = i\\vec{v}_1$ ✓ (usando $i \\cdot (-i) = 1$)."
              ),
               "justificacion_md": "**Sin valores propios reales** $\\Rightarrow$ no hay direcciones invariantes en $\\mathbb{R}^2$. La rotación 'requiere' los complejos para diagonalizarse.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Partes real e imaginaria de un vector complejo",
          body_md=(
              "El **complejo conjugado** de $\\vec{x} \\in \\mathbb{C}^n$, denotado $\\bar{\\vec{x}}$, es el vector cuyas entradas son los conjugados de las entradas de $\\vec{x}$.\n\n"
              "Las **partes real e imaginaria** de $\\vec{x}$ son los vectores $\\text{Re}\\,\\vec{x}, \\text{Im}\\,\\vec{x} \\in \\mathbb{R}^n$ formados con las partes real e imaginaria de cada entrada:\n\n"
              "$$\\vec{x} = \\text{Re}\\,\\vec{x} + i\\,\\text{Im}\\,\\vec{x}, \\qquad \\bar{\\vec{x}} = \\text{Re}\\,\\vec{x} - i\\,\\text{Im}\\,\\vec{x}.$$\n\n"
              "**Ejemplo.** Si $\\vec{x} = \\begin{bmatrix} 3 - i \\\\ i \\\\ 2 + 5i \\end{bmatrix}$, entonces $\\text{Re}\\,\\vec{x} = (3, 0, 2)^T$ y $\\text{Im}\\,\\vec{x} = (-1, 1, 5)^T$."
          )),

        b("teorema",
          nombre="Estructura de matrices reales $2\\times 2$ con valores propios complejos",
          enunciado_md=(
              "Sea $A \\in \\mathbb{R}^{2 \\times 2}$ con valor propio complejo $\\lambda = a - bi$ (con $b \\neq 0$) y vector propio asociado $\\vec{v} \\in \\mathbb{C}^2$. Entonces\n\n"
              "$$\\boxed{A = PCP^{-1},}$$\n\n"
              "donde\n\n"
              "$$P = \\bigl[\\,\\text{Re}\\,\\vec{v}\\ \\ \\text{Im}\\,\\vec{v}\\,\\bigr], \\qquad C = \\begin{bmatrix} a & -b \\\\ b & a \\end{bmatrix}.$$\n\n"
              "**Interpretación.** $C$ es la matriz de una **rotación combinada con escala**. Específicamente, $C = r R_\\theta$ donde:\n\n"
              "- $r = \\sqrt{a^2 + b^2} = |\\lambda|$ es el factor de escala.\n"
              "- $R_\\theta$ es la rotación por ángulo $\\theta = \\arg(\\lambda)$.\n\n"
              "**Consecuencia geométrica:** **toda matriz real $2\\times 2$ con valores propios complejos es similar a una rotación-escala**. Capturó la 'esencia oscilatoria' de la transformación."
          )),

        b("ejemplo_resuelto",
          titulo="Descomposición de la rotación $90°$",
          problema_md=(
              "Aplica el teorema a $A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Del ejemplo anterior, $\\lambda = i = 0 + i$, así $a = 0, b = 1$. Vector propio para $\\lambda = -i$ (la convención del teorema): $\\vec{v} = (1, i)^T$.\n\n"
                  "$\\text{Re}\\,\\vec{v} = (1, 0)^T$, $\\text{Im}\\,\\vec{v} = (0, 1)^T$."
              ),
               "justificacion_md": "Hay convenciones distintas; aquí seguimos $\\lambda = a - bi$ y elegimos $\\vec{v}$ asociado a $\\lambda = -i$.",
               "es_resultado": False},
              {"accion_md": (
                  "$P = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} = I$, $C = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix} = A$.\n\n"
                  "$A = ICI^{-1} = C$ ✓. **La rotación de $90°$ ya está en forma canónica $C$** — no hay nada que cambiar."
              ),
               "justificacion_md": "**Caso especial:** una rotación pura ya tiene la forma de la matriz canónica $C$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Otra matriz con valores propios complejos",
          problema_md=(
              "Aplica el teorema a $A = \\begin{bmatrix} 0.5 & -0.6 \\\\ 0.75 & 1.1 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Polinomio: $(0.5-\\lambda)(1.1-\\lambda) + 0.45 = \\lambda^2 - 1.6\\lambda + 1 = 0$.\n\n"
                  "$\\lambda = \\dfrac{1.6 \\pm \\sqrt{2.56 - 4}}{2} = 0.8 \\pm 0.6i$. Tomamos $\\lambda = 0.8 - 0.6i$ ($a = 0.8, b = 0.6$)."
              ),
               "justificacion_md": "$\\Delta = 1.6^2 - 4 = -1.44 < 0$ $\\Rightarrow$ raíces complejas.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolvemos $(A - \\lambda I)\\vec{v} = \\vec{0}$ con $\\lambda = 0.8 - 0.6i$:\n\n"
                  "$A - \\lambda I = \\begin{bmatrix} -0.3 + 0.6i & -0.6 \\\\ 0.75 & 0.3 + 0.6i \\end{bmatrix}$.\n\n"
                  "Una solución: $\\vec{v} = (-2 - 4i, 5)^T$ (verificable). $\\text{Re}\\,\\vec{v} = (-2, 5)^T$, $\\text{Im}\\,\\vec{v} = (-4, 0)^T$."
              ),
               "justificacion_md": "Cualquier vector propio sirve; las cuentas son más sutiles que en el caso real.",
               "es_resultado": False},
              {"accion_md": (
                  "$P = \\begin{bmatrix} -2 & -4 \\\\ 5 & 0 \\end{bmatrix}$, $C = \\begin{bmatrix} 0.8 & -0.6 \\\\ 0.6 & 0.8 \\end{bmatrix}$.\n\n"
                  "**$|\\lambda| = \\sqrt{0.64 + 0.36} = 1$**, así $C$ es una **rotación pura** (sin escala). El ángulo es $\\theta = \\arctan(0.6/0.8) \\approx 36.87°$.\n\n"
                  "**Conclusión:** $A$ es similar a una rotación de $\\approx 37°$ — es una rotación 'disfrazada' por el cambio de base $P$."
              ),
               "justificacion_md": "**Lección poderosa:** valores propios complejos de magnitud $1$ corresponden a transformaciones que solo rotan (sin amplificar/atenuar).",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**¿Qué nos dice $|\\lambda|$ y $\\arg(\\lambda)$ sobre la dinámica de $\\vec{x}_{t+1} = A\\vec{x}_t$?**\n\n"
            "Para una matriz real $2 \\times 2$ con valor propio $\\lambda = a + bi$:\n\n"
            "- **$|\\lambda| < 1$:** las trayectorias **espiral hacia el origen** (sistema estable).\n"
            "- **$|\\lambda| = 1$:** las trayectorias son **órbitas circulares** o **elípticas** (oscilación pura).\n"
            "- **$|\\lambda| > 1$:** las trayectorias **espiral hacia el infinito** (sistema inestable).\n"
            "- **$\\arg(\\lambda)$:** ángulo de rotación por iteración.\n\n"
            "Esta es la base del **análisis de estabilidad** en sistemas lineales y el origen de la **transformada de Fourier** y los **modos normales** en vibraciones."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si una matriz real $A$ tiene valor propio $\\lambda = 2 + 3i$, entonces:",
                  "opciones_md": [
                      "$\\lambda$ es el único valor propio",
                      "$A$ no tiene vectores propios",
                      "$\\bar{\\lambda} = 2 - 3i$ también es valor propio",
                      "$A$ no es diagonalizable",
                  ],
                  "correcta": "C",
                  "pista_md": "Pares conjugados.",
                  "explicacion_md": "**$\\bar{\\lambda} = 2 - 3i$ también.** Los valores propios complejos de matrices reales vienen siempre en pares conjugados.",
              },
              {
                  "enunciado_md": "La matriz $C = \\begin{bmatrix} a & -b \\\\ b & a \\end{bmatrix}$ representa una:",
                  "opciones_md": [
                      "Reflexión",
                      "**Rotación escalada** por factor $\\sqrt{a^2 + b^2}$",
                      "Proyección",
                      "Cizalladura (shear)",
                  ],
                  "correcta": "B",
                  "pista_md": "$C = \\sqrt{a^2+b^2} \\cdot R_\\theta$.",
                  "explicacion_md": "**Rotación-escala.** $C$ rota por ángulo $\\theta = \\arctan(b/a)$ y escala por $\\sqrt{a^2 + b^2}$.",
              },
              {
                  "enunciado_md": "Si una matriz real $2\\times 2$ tiene valores propios $\\lambda = 0.9 \\pm 0.4i$, las trayectorias de $\\vec{x}_{t+1} = A\\vec{x}_t$:",
                  "opciones_md": [
                      "Espiral hacia el origen",
                      "Órbitas circulares",
                      "Espiral hacia el infinito",
                      "Convergen a un punto fijo no nulo",
                  ],
                  "correcta": "A",
                  "pista_md": "$|\\lambda| = \\sqrt{0.81 + 0.16} = \\sqrt{0.97} < 1$.",
                  "explicacion_md": "**Espiral hacia el origen.** $|\\lambda| < 1$ $\\Rightarrow$ contracción $\\Rightarrow$ sistema estable que decae.",
              },
          ]),

        ej(
            "Valores propios complejos $2\\times 2$",
            "Halla los valores propios de $A = \\begin{bmatrix} 1 & -2 \\\\ 1 & 3 \\end{bmatrix}$.",
            [
                "Calcula el discriminante.",
            ],
            (
                "$\\det(A - \\lambda I) = (1 - \\lambda)(3 - \\lambda) + 2 = \\lambda^2 - 4\\lambda + 5 = 0$.\n\n"
                "Discriminante: $16 - 20 = -4 < 0$ $\\Rightarrow$ raíces complejas.\n\n"
                "$\\lambda = \\dfrac{4 \\pm \\sqrt{-4}}{2} = 2 \\pm i$. **Valores propios:** $\\lambda = 2 + i$ y $\\lambda = 2 - i$."
            ),
        ),

        ej(
            "Descomposición $A = PCP^{-1}$",
            "Aplica el Teorema 9 a $A = \\begin{bmatrix} 1 & -2 \\\\ 1 & 3 \\end{bmatrix}$ del ejercicio anterior.",
            [
                "Calcula un vector propio para $\\lambda = 2 - i$.",
                "Identifica $a, b$ y construye $C$.",
            ],
            (
                "Para $\\lambda = 2 - i$: $A - \\lambda I = \\begin{bmatrix} -1 + i & -2 \\\\ 1 & 1 + i \\end{bmatrix}$. Una solución: $\\vec{v} = (-2, 1 - i)^T$ o equivalentemente $\\vec{v} = (1 + i, -1)^T$ (escalando).\n\n"
                "Tomemos $\\vec{v} = (-2, 1 - i)^T$. $\\text{Re}\\,\\vec{v} = (-2, 1)^T$, $\\text{Im}\\,\\vec{v} = (0, -1)^T$.\n\n"
                "$P = \\begin{bmatrix} -2 & 0 \\\\ 1 & -1 \\end{bmatrix}$, $C = \\begin{bmatrix} 2 & -1 \\\\ 1 & 2 \\end{bmatrix}$ (con $a = 2, b = 1$).\n\n"
                "$|\\lambda| = \\sqrt{5} \\Rightarrow$ amplificación con factor $\\sqrt{5}$ por iteración. **Sistema inestable** que espiral hacia el infinito."
            ),
        ),

        ej(
            "Identificar geometría",
            "Una matriz real $2 \\times 2$ tiene valores propios $\\lambda = \\sqrt{3}/2 \\pm i/2$. Describe la transformación.",
            [
                "Calcula $|\\lambda|$ y $\\arg(\\lambda)$.",
            ],
            (
                "$|\\lambda| = \\sqrt{3/4 + 1/4} = 1$. $\\arg(\\lambda) = \\arctan(\\tfrac{1/2}{\\sqrt{3}/2}) = \\arctan(\\tfrac{1}{\\sqrt{3}}) = 30°$.\n\n"
                "**$A$ es similar a una rotación pura de $30°$** (sin escala, ya que $|\\lambda| = 1$). Las iteraciones $\\vec{x}_{t+1} = A\\vec{x}_t$ describen órbitas elípticas alrededor del origen."
            ),
        ),

        fig(
            "Diagrama matemático con dos paneles. Panel izquierdo: cuadrícula 2D bajo una matriz de rotación "
            "2x2 sin autovectores reales; un punto inicial x0 y su órbita {x0, A x0, A^2 x0, ...} dibujada "
            "como espiral en teal #06b6d4 girando alrededor del origen, sin estabilizarse en ninguna "
            "dirección. Etiqueta 'sin direcciones invariantes reales'. Panel derecho: plano complejo con "
            "ejes Re e Im, y dos puntos conjugados λ = a + bi y λ = a - bi marcados como círculos ámbar "
            "#f59e0b, simétricos respecto al eje real, unidos por una línea punteada. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que matrices reales solo tienen valores propios reales.** Falso: el polinomio característico puede tener raíces complejas.",
              "**Olvidar que los valores propios complejos de matrices reales vienen en pares conjugados.**",
              "**Construir $C$ con signos equivocados.** Convención: si $\\lambda = a - bi$ es el valor propio elegido, $C = \\begin{bmatrix} a & -b \\\\ b & a \\end{bmatrix}$.",
              "**Mezclar conjugaciones.** Si $A\\vec{v} = \\lambda\\vec{v}$, entonces $A\\bar{\\vec{v}} = \\bar{\\lambda}\\bar{\\vec{v}}$ — no $\\lambda \\bar{\\vec{v}}$.",
              "**No identificar $|\\lambda|$ y $\\arg(\\lambda)$ con la dinámica.** $|\\lambda|$ controla amplitud, $\\arg(\\lambda)$ controla rotación.",
          ]),

        b("resumen",
          puntos_md=[
              "**Polinomio característico** tiene siempre $n$ raíces en $\\mathbb{C}$ (TFA).",
              "**Pares conjugados:** matrices reales tienen valores propios complejos en pares $\\lambda, \\bar{\\lambda}$ con vectores propios $\\vec{v}, \\bar{\\vec{v}}$.",
              "**Partes real e imaginaria** de un vector $\\vec{x} \\in \\mathbb{C}^n$: $\\vec{x} = \\text{Re}\\,\\vec{x} + i\\,\\text{Im}\\,\\vec{x}$.",
              "**Teorema (real $2\\times 2$):** $A = PCP^{-1}$ con $C = \\begin{bmatrix} a & -b \\\\ b & a \\end{bmatrix}$ — **rotación-escala**.",
              "**$|\\lambda|$:** factor de escala (estabilidad/inestabilidad).",
              "**$\\arg(\\lambda)$:** ángulo de rotación por iteración.",
              "**Cierre del capítulo:** los valores propios capturan la **estructura geométrica** de una transformación lineal.",
              "**Próximo capítulo:** **Ortogonalidad** — proyecciones, bases ortonormales, mínimos cuadrados.",
          ]),
    ]
    return {
        "id": "lec-al-6-4-valores-complejos",
        "title": "Valores propios complejos",
        "description": "Valores propios en $\\mathbb{C}$, vectores propios complejos y pares conjugados, partes real e imaginaria, descomposición $A = PCP^{-1}$ con $C$ matriz de rotación-escala.",
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
    course_id = "algebra-lineal"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(
            f"Curso {course_id} no existe. Corre primero seed_algebra_lineal_chapter_1.py"
        )

    chapter_id = "ch-al-valores-vectores-propios"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Valores y Vectores Propios",
        "description": (
            "Vectores propios $A\\vec{v} = \\lambda\\vec{v}$ y ecuación característica "
            "$\\det(A - \\lambda I) = 0$; diagonalización $A = PDP^{-1}$ y sus aplicaciones; "
            "diagonalización como cambio de base; valores propios complejos y descomposición rotación-escala."
        ),
        "order": 6,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_6_1, lesson_6_2, lesson_6_3, lesson_6_4]
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
        f"✅ Capítulo 6 — Valores y Vectores Propios listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
