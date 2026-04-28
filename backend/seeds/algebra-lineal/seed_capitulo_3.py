"""
Seed del curso Álgebra Lineal — Capítulo 3: Álgebra de Matrices.
4 lecciones:
  3.1 Operaciones de matrices
  3.2 Inversa
  3.3 Matrices elementales (incluye Teorema de la Matriz Invertible)
  3.4 Factorizaciones LU y PA = LU

Basado en los Apuntes/Clase de Se Remonta para cada lección.
Estructura: del producto matricial visto por columnas y regla fila-columna,
pasando por la inversa (fórmula 2x2 y algoritmo de Gauss-Jordan), las
matrices elementales como puente entre OEF y multiplicación, hasta el
Teorema de la Matriz Invertible y las factorizaciones LU / PA = LU.

Requiere que el curso 'algebra-lineal' ya exista (ver
seed_algebra_lineal_chapter_1.py). Idempotente.
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
# 3.1 Operaciones de matrices
# =====================================================================
def lesson_3_1():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora hemos usado las matrices como contenedores de coeficientes de un sistema "
            "lineal. En este capítulo damos un paso conceptual mayor: las matrices son **objetos "
            "algebraicos** que se suman, se escalan, se multiplican y se transponen. El **producto "
            "matricial** $AB$ corresponde a la **composición** de las transformaciones lineales que cada "
            "matriz representa, lo que explica sus propiedades (asociatividad, distributividad) y, sobre "
            "todo, sus 'sorpresas' (no conmutatividad).\n\n"
            "Al terminar la lección debes poder:\n\n"
            "- Reconocer matrices **especiales** ($\\mathbf{0}$, $I_n$, diagonal, triangular).\n"
            "- Calcular suma y múltiplo escalar y enunciar sus propiedades.\n"
            "- Calcular $AB$ por **columnas** y por la **regla fila–columna**, decidir cuándo está definido.\n"
            "- Aplicar las propiedades algebraicas y reconocer las **advertencias** (no conmutatividad, falta de cancelación).\n"
            "- Trabajar con potencias $A^k$ y transpuesta $A^T$."
        )),

        b("definicion",
          titulo="Notación, dimensiones y matrices especiales",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{m \\times n}$. Escribimos $A = [a_{ij}]_{m \\times n}$ y, vista por columnas, "
              "$A = [\\,\\vec{a}_1\\ \\cdots\\ \\vec{a}_n\\,]$, donde cada $\\vec{a}_j \\in \\mathbb{R}^m$.\n\n"
              "**Diagonal principal:** entradas $a_{11}, a_{22}, \\ldots$\n\n"
              "**Matrices especiales:**\n\n"
              "| Nombre | Símbolo | Definición |\n|---|---|---|\n"
              "| Matriz cero | $\\mathbf{0}_{m\\times n}$ | Todas las entradas $= 0$. |\n"
              "| Identidad | $I_n$ | Cuadrada $n\\times n$, diagonal $= 1$, resto $= 0$. |\n"
              "| Diagonal | $\\text{diag}(d_1, \\ldots, d_n)$ | Cuadrada con $a_{ij} = 0$ si $i \\neq j$. |\n"
              "| Triangular superior | — | $a_{ij} = 0$ si $i > j$ (ceros bajo la diagonal). |\n"
              "| Triangular inferior | — | $a_{ij} = 0$ si $i < j$ (ceros sobre la diagonal). |\n\n"
              "**$I_n$ es la 'matriz unidad'** del producto matricial: cumple $I_m A = A = A I_n$ para toda $A \\in \\mathbb{R}^{m\\times n}$."
          )),

        b("ejemplo_resuelto",
          titulo="Lectura de entradas",
          problema_md=(
              "Sea $A = \\begin{bmatrix} 2 & -1 & 0 \\\\ 3 & 4 & 5 \\end{bmatrix}$. "
              "(i) Tamaño de $A$. (ii) Halla $a_{12}$ y $a_{23}$. (iii) Escribe la columna $2$ y la fila $1$ como vectores."
          ),
          pasos=[
              {"accion_md": "**(i)** $A$ tiene $2$ filas y $3$ columnas $\\Rightarrow A \\in \\mathbb{R}^{2 \\times 3}$.",
               "justificacion_md": "Convención: filas $\\times$ columnas.",
               "es_resultado": False},
              {"accion_md": "**(ii)** $a_{12}$ = fila $1$, columna $2$ $= -1$. $a_{23}$ = fila $2$, columna $3$ $= 5$.",
               "justificacion_md": "Recordar: índice de fila primero.",
               "es_resultado": False},
              {"accion_md": "**(iii)** Columna $2$: $\\vec{a}_2 = \\begin{bmatrix} -1 \\\\ 4 \\end{bmatrix} \\in \\mathbb{R}^2$. Fila $1$: $(2, -1, 0)$.",
               "justificacion_md": "Las columnas viven en $\\mathbb{R}^m$; las filas en $\\mathbb{R}^{1\\times n}$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Identificación de estructura",
          problema_md=(
              "Clasifica como cero, identidad, diagonal, triangular superior o triangular inferior:\n\n"
              "$$B = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}, \\ "
              "C = \\begin{bmatrix} 3 & 0 & 0 \\\\ 0 & -2 & 0 \\\\ 0 & 0 & 4 \\end{bmatrix}, \\ "
              "D = \\begin{bmatrix} 1 & 2 & -1 \\\\ 0 & 3 & 5 \\\\ 0 & 0 & -2 \\end{bmatrix}, \\ "
              "E = \\begin{bmatrix} 0 & 0 \\\\ 0 & 0 \\end{bmatrix}.$$"
          ),
          pasos=[
              {"accion_md": "**$B = I_3$** — identidad (también es diagonal). **$C$** es **diagonal** ($\\text{diag}(3, -2, 4)$).",
               "justificacion_md": "$I_n$ es el caso particular de matriz diagonal con todos los $d_i = 1$.",
               "es_resultado": False},
              {"accion_md": "**$D$** es **triangular superior** (no diagonal, pues hay entradas no nulas sobre la diagonal). **$E = \\mathbf{0}_{2\\times 2}$** — matriz cero.",
               "justificacion_md": "Triangular superior $\\iff$ ceros estrictamente debajo de la diagonal.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Suma y múltiplo escalar",
          body_md=(
              "Para matrices del **mismo tamaño** $m \\times n$ y $r \\in \\mathbb{R}$:\n\n"
              "$$A + B = [a_{ij} + b_{ij}], \\qquad rA = [r\\,a_{ij}].$$\n\n"
              "Ambas operaciones son **entrada a entrada**.\n\n"
              "**Importante:** $A + B$ **no está definido** si $A$ y $B$ tienen tamaños distintos.\n\n"
              "**Propiedades algebraicas.** Para todo $A, B, C$ del mismo tamaño y $r, s \\in \\mathbb{R}$:\n\n"
              "| Propiedad | Fórmula |\n|---|---|\n"
              "| Conmutativa | $A + B = B + A$ |\n"
              "| Asociativa | $(A + B) + C = A + (B + C)$ |\n"
              "| Neutro / opuesto | $A + \\mathbf{0} = A$, $A + (-A) = \\mathbf{0}$ |\n"
              "| Distributiva (escalar/matrices) | $r(A + B) = rA + rB$ |\n"
              "| Distributiva (escalares) | $(r + s)A = rA + sA$ |\n"
              "| Asociativa (escalares) | $r(sA) = (rs)A$ |"
          )),

        b("ejemplo_resuelto",
          titulo="Suma cuando está definida",
          problema_md=(
              "Sean $A = \\begin{bmatrix} 4 & 0 & 5 \\\\ -1 & 3 & 2 \\end{bmatrix}$, "
              "$B = \\begin{bmatrix} 1 & 1 & 1 \\\\ 3 & 5 & 7 \\end{bmatrix}$ y "
              "$C = \\begin{bmatrix} 2 & -3 \\\\ 0 & 1 \\end{bmatrix}$. Calcular $A + B$ y explicar por qué $A + C$ no está definido."
          ),
          pasos=[
              {"accion_md": (
                  "$A + B = \\begin{bmatrix} 4+1 & 0+1 & 5+1 \\\\ -1+3 & 3+5 & 2+7 \\end{bmatrix} = \\begin{bmatrix} 5 & 1 & 6 \\\\ 2 & 8 & 9 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Suma componente a componente; ambas son $2 \\times 3$.",
               "es_resultado": False},
              {"accion_md": "$A \\in \\mathbb{R}^{2\\times 3}$ y $C \\in \\mathbb{R}^{2 \\times 2}$ — **tamaños distintos** $\\Rightarrow$ $A + C$ no está definido.",
               "justificacion_md": "La suma exige tamaños idénticos. No basta con que coincidan en una dimensión.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Múltiplo escalar y combinación",
          problema_md=(
              "Con $A, B$ del ejemplo anterior, halla $2B$ y $A - 2B$."
          ),
          pasos=[
              {"accion_md": (
                  "$2B = \\begin{bmatrix} 2 & 2 & 2 \\\\ 6 & 10 & 14 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Multiplicar entrada por entrada.",
               "es_resultado": False},
              {"accion_md": (
                  "$A - 2B = \\begin{bmatrix} 4-2 & 0-2 & 5-2 \\\\ -1-6 & 3-10 & 2-14 \\end{bmatrix} = \\begin{bmatrix} 2 & -2 & 3 \\\\ -7 & -7 & -12 \\end{bmatrix}.$"
              ),
               "justificacion_md": "$A - 2B = A + (-2)B$ — caso particular de combinación lineal de matrices.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Producto matricial: vista por columnas",
          body_md=(
              "Sean $A \\in \\mathbb{R}^{m \\times n}$ y $B \\in \\mathbb{R}^{n \\times p}$ "
              "(el **número de columnas de $A$ debe coincidir con el número de filas de $B$**). "
              "Escribiendo $B = [\\,\\vec{b}_1\\ \\cdots\\ \\vec{b}_p\\,]$ por columnas, se define:\n\n"
              "$$\\boxed{AB = [\\,A\\vec{b}_1\\ \\ A\\vec{b}_2\\ \\cdots\\ A\\vec{b}_p\\,] \\in \\mathbb{R}^{m \\times p}.}$$\n\n"
              "Es decir, **la columna $j$ de $AB$ es $A\\vec{b}_j$** — el producto matriz–vector que ya conocemos del cap. 2.\n\n"
              "**Tamaños — regla mnemotécnica:**\n\n"
              "$$\\underbrace{A}_{m \\times n} \\cdot \\underbrace{B}_{n \\times p} = \\underbrace{AB}_{m \\times p}.$$\n\n"
              "Las dimensiones $n$ 'se cancelan en el medio'."
          )),

        b("ejemplo_resuelto",
          titulo="Producto por columnas",
          problema_md=(
              "Calcular $AB$ con $A = \\begin{bmatrix} 2 & 3 \\\\ 1 & -5 \\end{bmatrix}$ y "
              "$B = \\begin{bmatrix} 4 & 3 & 6 \\\\ 1 & -2 & 3 \\end{bmatrix} = [\\vec{b}_1\\ \\vec{b}_2\\ \\vec{b}_3]$, "
              "vista por columnas."
          ),
          pasos=[
              {"accion_md": (
                  "Tamaños: $A$ es $2\\times 2$, $B$ es $2 \\times 3$ $\\Rightarrow AB$ será $2 \\times 3$. "
                  "Calculamos $A\\vec{b}_j$ para $j = 1, 2, 3$:\n\n"
                  "$A\\vec{b}_1 = 4\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix} + 1\\begin{bmatrix} 3 \\\\ -5 \\end{bmatrix} = \\begin{bmatrix} 11 \\\\ -1 \\end{bmatrix}.$"
              ),
               "justificacion_md": "$A\\vec{b}_j$ = combinación lineal de las columnas de $A$ con pesos las entradas de $\\vec{b}_j$ (cap. 2).",
               "es_resultado": False},
              {"accion_md": (
                  "$A\\vec{b}_2 = 3\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix} + (-2)\\begin{bmatrix} 3 \\\\ -5 \\end{bmatrix} = \\begin{bmatrix} 0 \\\\ 13 \\end{bmatrix}$. "
                  "$A\\vec{b}_3 = 6\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix} + 3\\begin{bmatrix} 3 \\\\ -5 \\end{bmatrix} = \\begin{bmatrix} 21 \\\\ -9 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Repetimos la operación columna por columna.",
               "es_resultado": False},
              {"accion_md": (
                  "**$AB = \\begin{bmatrix} 11 & 0 & 21 \\\\ -1 & 13 & -9 \\end{bmatrix}$.**"
              ),
               "justificacion_md": "Ensamblamos las tres columnas calculadas.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Regla fila–columna (entrada por entrada)",
          body_md=(
              "Equivalentemente, la entrada $(i, j)$ del producto $AB$ es el **producto punto** entre la $i$-ésima fila de $A$ y la $j$-ésima columna de $B$:\n\n"
              "$$\\boxed{(AB)_{ij} = \\sum_{k=1}^n a_{ik}\\,b_{kj} = \\text{fila}_i(A) \\cdot \\text{col}_j(B).}$$\n\n"
              "**Consecuencias útiles:** $\\text{fila}_i(AB) = \\text{fila}_i(A)\\,B$ y $\\text{col}_j(AB) = A\\,\\text{col}_j(B)$.\n\n"
              "Las dos visiones (por columnas y por entradas) son **equivalentes** — usa la que sea más conveniente en cada problema."
          )),

        b("ejemplo_resuelto",
          titulo="Una entrada por la regla fila-columna",
          problema_md=(
              "Para $A = \\begin{bmatrix} 2 & 3 \\\\ 1 & -5 \\end{bmatrix}$ y $B = \\begin{bmatrix} 4 & 3 & 6 \\\\ 1 & -2 & 3 \\end{bmatrix}$, calcular $(AB)_{1,3}$ y $(AB)_{2,2}$."
          ),
          pasos=[
              {"accion_md": (
                  "$(AB)_{1,3} = \\text{fila}_1(A) \\cdot \\text{col}_3(B) = (2,\\ 3) \\cdot (6,\\ 3)^T = 2\\cdot 6 + 3\\cdot 3 = 21.$"
              ),
               "justificacion_md": "Producto punto fila $1$ × columna $3$.",
               "es_resultado": False},
              {"accion_md": (
                  "$(AB)_{2,2} = \\text{fila}_2(A) \\cdot \\text{col}_2(B) = (1,\\ -5) \\cdot (3,\\ -2)^T = 1\\cdot 3 + (-5)(-2) = 13.$\n\n"
                  "Coincide con lo que obtuvimos por columnas: $AB = \\begin{bmatrix} 11 & 0 & 21 \\\\ -1 & 13 & -9 \\end{bmatrix}$ ✓."
              ),
               "justificacion_md": "Útil cuando solo necesitas **una entrada** y no toda la matriz.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Propiedades del producto matricial",
            body=(
                "Para tamaños compatibles y $r \\in \\mathbb{R}$:\n\n"
                "| Propiedad | Fórmula |\n|---|---|\n"
                "| **Asociativa** | $A(BC) = (AB)C$ |\n"
                "| **Distributiva (izq.)** | $A(B + C) = AB + AC$ |\n"
                "| **Distributiva (der.)** | $(B + C)A = BA + CA$ |\n"
                "| **Compatible con escalar** | $r(AB) = (rA)B = A(rB)$ |\n"
                "| **Identidad** | $I_m A = A = A I_n$ |\n\n"
                "**Advertencias importantes** (¡no se cumplen las del álgebra escalar!):\n\n"
                "- **No conmutativa:** en general $AB \\neq BA$.\n"
                "- **No vale cancelación:** de $AB = AC$ **no** se sigue $B = C$.\n"
                "- Puede ocurrir $AB = \\mathbf{0}$ con $A \\neq \\mathbf{0}$ y $B \\neq \\mathbf{0}$.\n"
                "- $(AB)^k$ **no es** $A^k B^k$ en general."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="No conmutatividad",
          problema_md=(
              "Verifica que $AB \\neq BA$ para $A = \\begin{bmatrix} 1 & 2 \\\\ 0 & 1 \\end{bmatrix}$ y "
              "$B = \\begin{bmatrix} 2 & 0 \\\\ 0 & 3 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$AB = \\begin{bmatrix} 1 & 2 \\\\ 0 & 1 \\end{bmatrix}\\begin{bmatrix} 2 & 0 \\\\ 0 & 3 \\end{bmatrix} = \\begin{bmatrix} 2 & 6 \\\\ 0 & 3 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Por la regla fila-columna o por columnas.",
               "es_resultado": False},
              {"accion_md": (
                  "$BA = \\begin{bmatrix} 2 & 0 \\\\ 0 & 3 \\end{bmatrix}\\begin{bmatrix} 1 & 2 \\\\ 0 & 1 \\end{bmatrix} = \\begin{bmatrix} 2 & 4 \\\\ 0 & 3 \\end{bmatrix}.$\n\n"
                  "**$AB \\neq BA$** $\\Rightarrow$ el producto matricial **no es conmutativo**."
              ),
               "justificacion_md": "**Lección general:** el orden importa al multiplicar matrices, incluso cuando los tamaños permiten ambas formas.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Potencias de una matriz cuadrada",
          body_md=(
              "Sea $A$ una matriz **cuadrada** $n \\times n$. Para $k \\in \\mathbb{N}$ definimos:\n\n"
              "$$A^0 = I_n, \\qquad A^{k+1} = A^k\\,A \\quad (k \\geq 0).$$\n\n"
              "Es decir, $A^k$ es la matriz $A$ multiplicada por sí misma $k$ veces.\n\n"
              "**Propiedades.** Para enteros $k, m \\geq 0$:\n\n"
              "- $A^k A^m = A^{k+m}$.\n"
              "- $(A^k)^m = A^{km}$.\n"
              "- Si $A$ es invertible, se extiende $A^{-k} = (A^{-1})^k$ (lección 3.2).\n\n"
              "**Cuidado:** en general $(AB)^k \\neq A^k B^k$ porque el producto **no es conmutativo**."
          )),

        b("ejemplo_resuelto",
          titulo="Potencias de una matriz diagonal",
          problema_md=(
              "Sea $D = \\text{diag}(2, -1, 3)$. Calcula $D^k$ y verifica $D^{k+m} = D^k D^m$."
          ),
          pasos=[
              {"accion_md": (
                  "**Conjetura:** $D^k = \\text{diag}(2^k,\\ (-1)^k,\\ 3^k)$. Demostración por inducción inmediata: el producto de dos diagonales es diagonal y multiplica las entradas de la diagonal."
              ),
               "justificacion_md": "Las matrices diagonales 'conmutan entre sí' y elevar a potencia se reduce a elevar las entradas.",
               "es_resultado": False},
              {"accion_md": (
                  "$D^k D^m = \\text{diag}(2^k, (-1)^k, 3^k)\\,\\text{diag}(2^m, (-1)^m, 3^m) = \\text{diag}(2^{k+m}, (-1)^{k+m}, 3^{k+m}) = D^{k+m}$ ✓."
              ),
               "justificacion_md": "**Idea clave:** las matrices diagonales son el caso 'fácil'. Diagonalizar una matriz general es uno de los grandes objetivos del cap. 6.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Potencia de una triangular $2 \\times 2$",
          problema_md=(
              "Sea $U = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}$. Halla una fórmula cerrada para $U^k$."
          ),
          pasos=[
              {"accion_md": (
                  "Escribimos $U = I + N$ con $N = \\begin{bmatrix} 0 & 1 \\\\ 0 & 0 \\end{bmatrix}$. Calculamos $N^2 = \\begin{bmatrix} 0 & 0 \\\\ 0 & 0 \\end{bmatrix} = \\mathbf{0}$."
              ),
               "justificacion_md": "Una matriz $N$ con $N^j = \\mathbf{0}$ para algún $j$ se llama **nilpotente** — facilita el cálculo de potencias.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $I$ y $N$ **conmutan** ($IN = N = NI$), aplica el binomio:\n\n"
                  "$U^k = (I + N)^k = \\sum_{j=0}^k \\binom{k}{j} N^j = I + kN$ (los términos con $j \\geq 2$ son cero por $N^2 = 0$).\n\n"
                  "**$U^k = \\begin{bmatrix} 1 & k \\\\ 0 & 1 \\end{bmatrix}$.**"
              ),
               "justificacion_md": "El binomio funciona **solo cuando las matrices conmutan**.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Transpuesta",
          body_md=(
              "Dada $A = [a_{ij}]$ de tamaño $m \\times n$, su **transpuesta** $A^T$ es la matriz de tamaño "
              "$n \\times m$ con entradas\n\n"
              "$$(A^T)_{ij} = a_{ji}, \\qquad 1 \\leq i \\leq n,\\ 1 \\leq j \\leq m.$$\n\n"
              "**En palabras:** las **filas de $A$** se vuelven las **columnas de $A^T$** (y viceversa).\n\n"
              "**Propiedades.** Para tamaños compatibles y $r \\in \\mathbb{R}$:\n\n"
              "| Propiedad | Fórmula |\n|---|---|\n"
              "| Doble transpuesta | $(A^T)^T = A$ |\n"
              "| Suma | $(A + B)^T = A^T + B^T$ |\n"
              "| Escalar | $(rA)^T = r A^T$ |\n"
              "| **Producto (¡invierte el orden!)** | $(AB)^T = B^T A^T$ |\n\n"
              "**Por qué $(AB)^T = B^T A^T$ y no $A^T B^T$:** los tamaños deben encajar. $A \\in \\mathbb{R}^{m \\times n}, B \\in \\mathbb{R}^{n \\times p} \\Rightarrow AB \\in \\mathbb{R}^{m \\times p}$, así $(AB)^T \\in \\mathbb{R}^{p \\times m}$. Solo $B^T A^T$ tiene esos tamaños."
          )),

        b("ejemplo_resuelto",
          titulo="Transpuesta directa",
          problema_md=(
              "Calcula $A^T$ y $B^T$ para $A = \\begin{bmatrix} 2 & -5 & 0 \\\\ -1 & 3 & -4 \\end{bmatrix}$ y "
              "$B = \\begin{bmatrix} 4 & -6 \\\\ 7 & 1 \\\\ 3 & 2 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A^T = \\begin{bmatrix} 2 & -1 \\\\ -5 & 3 \\\\ 0 & -4 \\end{bmatrix}$ (de $2\\times 3$ a $3\\times 2$)."
              ),
               "justificacion_md": "La fila $1$ de $A$, $(2, -5, 0)$, queda como columna $1$ de $A^T$.",
               "es_resultado": False},
              {"accion_md": (
                  "$B^T = \\begin{bmatrix} 4 & 7 & 3 \\\\ -6 & 1 & 2 \\end{bmatrix}$ (de $3\\times 2$ a $2\\times 3$)."
              ),
               "justificacion_md": "Mismo procedimiento: filas → columnas.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Verificación de $(AB)^T = B^T A^T$",
          problema_md=(
              "Con las matrices $A, B$ del ejemplo anterior, verifica la identidad $(AB)^T = B^T A^T$."
          ),
          pasos=[
              {"accion_md": (
                  "$AB = \\begin{bmatrix} 2 & -5 & 0 \\\\ -1 & 3 & -4 \\end{bmatrix}\\begin{bmatrix} 4 & -6 \\\\ 7 & 1 \\\\ 3 & 2 \\end{bmatrix} = \\begin{bmatrix} -27 & -17 \\\\ 5 & 1 \\end{bmatrix}.$\n\n"
                  "$(AB)^T = \\begin{bmatrix} -27 & 5 \\\\ -17 & 1 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Producto $2\\times 3$ por $3\\times 2$ = $2 \\times 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "$B^T A^T = \\begin{bmatrix} 4 & 7 & 3 \\\\ -6 & 1 & 2 \\end{bmatrix}\\begin{bmatrix} 2 & -1 \\\\ -5 & 3 \\\\ 0 & -4 \\end{bmatrix} = \\begin{bmatrix} -27 & 5 \\\\ -17 & 1 \\end{bmatrix} = (AB)^T$ ✓."
              ),
               "justificacion_md": "**Memoriza la regla:** transpuesta del producto = producto de transpuestas **en orden inverso**.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $A \\in \\mathbb{R}^{3 \\times 5}$ y $B \\in \\mathbb{R}^{5 \\times 2}$, entonces $AB$ tiene tamaño:",
                  "opciones_md": ["$3 \\times 2$", "$5 \\times 5$", "$2 \\times 3$", "$3 \\times 5$"],
                  "correcta": "A",
                  "pista_md": "Las dimensiones interiores ($5$) se cancelan; quedan las exteriores.",
                  "explicacion_md": "$AB \\in \\mathbb{R}^{3 \\times 2}$. Regla: $(m \\times n)(n \\times p) = (m \\times p)$.",
              },
              {
                  "enunciado_md": "$(AB)^T$ es igual a:",
                  "opciones_md": [
                      "$A^T B^T$",
                      "$B^T A^T$",
                      "$AB$",
                      "$BA$",
                  ],
                  "correcta": "B",
                  "pista_md": "La transpuesta del producto **invierte** el orden.",
                  "explicacion_md": "**$(AB)^T = B^T A^T$.** Es la única opción cuyas dimensiones encajan.",
              },
              {
                  "enunciado_md": "Si $AB = AC$ y $A \\neq \\mathbf{0}$, ¿se sigue $B = C$?",
                  "opciones_md": [
                      "Sí, siempre",
                      "Sí, si $A$ es cuadrada",
                      "No, en general",
                      "Sí, si $B$ y $C$ son cuadradas",
                  ],
                  "correcta": "C",
                  "pista_md": "El producto matricial **no admite cancelación**.",
                  "explicacion_md": "**No** se cumple la cancelación. Solo si $A$ es **invertible** podemos multiplicar por $A^{-1}$ para concluir $B = C$ (lección 3.2).",
              },
          ]),

        ej(
            "Producto $2\\times 3$ por $3\\times 2$",
            "Calcula $AB$ con $A = \\begin{bmatrix} 1 & 0 & -2 \\\\ 3 & 1 & 4 \\end{bmatrix}$ y $B = \\begin{bmatrix} 2 & -1 \\\\ 0 & 3 \\\\ 1 & 5 \\end{bmatrix}$.",
            [
                "Tamaños: $2 \\times 3$ por $3 \\times 2$ $\\Rightarrow AB$ es $2 \\times 2$.",
                "Por la regla fila-columna: $(AB)_{ij}$ = fila $i$ de $A$ $\\cdot$ columna $j$ de $B$.",
            ],
            (
                "$(AB)_{11} = (1, 0, -2)\\cdot(2, 0, 1)^T = 2 - 2 = 0$.\n\n"
                "$(AB)_{12} = (1, 0, -2)\\cdot(-1, 3, 5)^T = -1 - 10 = -11$.\n\n"
                "$(AB)_{21} = (3, 1, 4)\\cdot(2, 0, 1)^T = 6 + 4 = 10$.\n\n"
                "$(AB)_{22} = (3, 1, 4)\\cdot(-1, 3, 5)^T = -3 + 3 + 20 = 20$.\n\n"
                "$AB = \\begin{bmatrix} 0 & -11 \\\\ 10 & 20 \\end{bmatrix}.$"
            ),
        ),

        ej(
            "Anuladores no triviales",
            "Encuentra matrices $2\\times 2$ no nulas $A, B$ tales que $AB = \\mathbf{0}$.",
            [
                "Toma $A = \\begin{bmatrix} 1 & 0 \\\\ 0 & 0 \\end{bmatrix}$ y prueba con un $B$ que tenga la primera fila nula.",
                "Verifica el producto.",
            ],
            (
                "$A = \\begin{bmatrix} 1 & 0 \\\\ 0 & 0 \\end{bmatrix}$, $B = \\begin{bmatrix} 0 & 0 \\\\ 1 & 1 \\end{bmatrix}$. Ambas son no nulas.\n\n"
                "$AB = \\begin{bmatrix} 1\\cdot 0 + 0\\cdot 1 & 1\\cdot 0 + 0\\cdot 1 \\\\ 0 & 0 \\end{bmatrix} = \\begin{bmatrix} 0 & 0 \\\\ 0 & 0 \\end{bmatrix} = \\mathbf{0}.$\n\n"
                "**Conclusión:** en el álgebra de matrices no vale la propiedad de los enteros 'si $ab = 0$ entonces $a = 0$ o $b = 0$'."
            ),
        ),

        ej(
            "Potencia con binomio",
            "Sea $T = \\begin{bmatrix} 1 & 0 & 1 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}$. Halla una fórmula cerrada para $T^k$.",
            [
                "Escribe $T = I + N$ con $N$ que tenga un único $1$ fuera de la diagonal.",
                "Verifica que $N^2 = \\mathbf{0}$ y aplica el binomio.",
            ],
            (
                "$T = I + N$ con $N = \\begin{bmatrix} 0 & 0 & 1 \\\\ 0 & 0 & 0 \\\\ 0 & 0 & 0 \\end{bmatrix}$. Calculamos $N^2 = \\mathbf{0}$.\n\n"
                "Por el binomio (válido porque $I$ y $N$ conmutan): $T^k = I + kN = \\begin{bmatrix} 1 & 0 & k \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}.$"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Sumar matrices de tamaños distintos.** $A + B$ exige $A$ y $B$ del mismo tamaño.",
              "**Olvidar verificar dimensiones antes de multiplicar.** $AB$ exige $\\#\\text{cols}(A) = \\#\\text{filas}(B)$.",
              "**Asumir conmutatividad.** $AB = BA$ es **falso en general**, incluso cuando ambos productos están definidos.",
              "**Cancelar:** de $AB = AC$ no se sigue $B = C$ (salvo que $A$ sea invertible).",
              "**Aplicar el binomio $(A + B)^k$ sin verificar conmutatividad.** Solo vale si $AB = BA$.",
              "**Escribir $(AB)^T = A^T B^T$.** Lo correcto es $\\boxed{(AB)^T = B^T A^T}$ — invierte el orden.",
              "**Confundir $A^k$ con multiplicar entrada por entrada.** $A^k$ es el producto matricial repetido. Para entrada por entrada, solo coincide en matrices **diagonales**.",
          ]),

        b("resumen",
          puntos_md=[
              "**Notación:** $A = [a_{ij}]_{m\\times n}$, $A = [\\vec{a}_1\\ \\cdots\\ \\vec{a}_n]$.",
              "**Suma y escalar:** entrada por entrada, **mismo tamaño**.",
              "**Producto** $AB$: **dos visiones** equivalentes — por columnas ($A\\vec{b}_j$) y por entradas (regla fila-columna).",
              "**Tamaños:** $(m \\times n)(n \\times p) = (m \\times p)$.",
              "**Propiedades:** asociativa, distributiva, $I_m A = A = A I_n$. **NO** conmutativa, **NO** admite cancelación.",
              "**Potencias:** $A^k$ (matriz cuadrada), $A^0 = I$. Cuidado con $(AB)^k \\neq A^k B^k$.",
              "**Transpuesta:** $(A^T)_{ij} = a_{ji}$, $(AB)^T = B^T A^T$ (orden invertido).",
              "**Próxima lección:** **inversa** $A^{-1}$ — el inverso multiplicativo en este álgebra.",
          ]),
    ]
    return {
        "id": "lec-al-3-1-operaciones-matrices",
        "title": "Operaciones de matrices",
        "description": "Notación, matrices especiales, suma, múltiplo escalar, producto por columnas y regla fila-columna, potencias y transpuesta.",
        "blocks": blocks,
        "duration_minutes": 65,
        "order": 1,
    }


# =====================================================================
# 3.2 Inversa
# =====================================================================
def lesson_3_2():
    blocks = [
        b("texto", body_md=(
            "Así como en los números reales el número $\\tfrac{1}{a}$ 'deshace' la multiplicación por $a$ "
            "(siempre que $a \\neq 0$), en el álgebra de matrices buscamos un objeto $A^{-1}$ que **deshaga** "
            "el efecto de multiplicar por $A$. Este objeto es la **matriz inversa**, y existe solo para "
            "matrices **cuadradas no singulares**.\n\n"
            "La inversa conecta directamente con la teoría de sistemas: si $A$ es invertible, el sistema "
            "$A\\vec{x} = \\vec{b}$ tiene **solución única** $\\vec{x} = A^{-1}\\vec{b}$ para todo $\\vec{b}$.\n\n"
            "Al terminar, debes poder:\n\n"
            "- Definir y verificar invertibilidad ($AA^{-1} = A^{-1}A = I$).\n"
            "- Aplicar la **fórmula $2 \\times 2$**: si $\\det A = ad - bc \\neq 0$, $A^{-1} = \\tfrac{1}{ad-bc}\\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix}$.\n"
            "- Calcular $A^{-1}$ por **Gauss–Jordan** sobre $[A \\mid I]$.\n"
            "- Usar la inversa para resolver $A\\vec{x} = \\vec{b}$.\n"
            "- Aplicar las propiedades $(A^{-1})^{-1} = A$, $(AB)^{-1} = B^{-1}A^{-1}$, $(A^T)^{-1} = (A^{-1})^T$."
        )),

        b("definicion",
          titulo="Matriz invertible",
          body_md=(
              "Una matriz cuadrada $A \\in \\mathbb{R}^{n \\times n}$ es **invertible** (o **no singular**) si existe $C \\in \\mathbb{R}^{n \\times n}$ tal que\n\n"
              "$$CA = I_n \\quad \\text{y} \\quad AC = I_n.$$\n\n"
              "En tal caso, $C$ es **única** y se denota $C = A^{-1}$. Si no existe tal $C$, $A$ se llama **singular**.\n\n"
              "**Consecuencias inmediatas.**\n\n"
              "- Si $A$ es invertible, para todo $\\vec{b} \\in \\mathbb{R}^n$ la ecuación $A\\vec{x} = \\vec{b}$ tiene **solución única** $\\vec{x} = A^{-1}\\vec{b}$.\n"
              "- $(A^{-1})^{-1} = A$.\n"
              "- Si $A$ y $B$ son invertibles del mismo tamaño, $AB$ es invertible y $(AB)^{-1} = B^{-1}A^{-1}$.\n"
              "- $A$ debe ser **cuadrada** — la noción de inversa no aplica a matrices rectangulares."
          )),

        b("ejemplo_resuelto",
          titulo="Verificación directa",
          problema_md=(
              "Verifica que $C = \\begin{bmatrix} -7 & -5 \\\\ 3 & 2 \\end{bmatrix}$ es la inversa de $A = \\begin{bmatrix} 2 & 5 \\\\ -3 & -7 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$AC = \\begin{bmatrix} 2 & 5 \\\\ -3 & -7 \\end{bmatrix}\\begin{bmatrix} -7 & -5 \\\\ 3 & 2 \\end{bmatrix} = \\begin{bmatrix} -14+15 & -10+10 \\\\ 21-21 & 15-14 \\end{bmatrix} = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} = I_2.$"
              ),
               "justificacion_md": "Verificamos $AC = I$.",
               "es_resultado": False},
              {"accion_md": (
                  "$CA = \\begin{bmatrix} -7 & -5 \\\\ 3 & 2 \\end{bmatrix}\\begin{bmatrix} 2 & 5 \\\\ -3 & -7 \\end{bmatrix} = \\begin{bmatrix} -14+15 & -35+35 \\\\ 6-6 & 15-14 \\end{bmatrix} = I_2.$\n\n"
                  "Como $AC = CA = I_2$, **$C = A^{-1}$**."
              ),
               "justificacion_md": "**Hecho útil:** para matrices cuadradas, basta verificar **una** de las dos igualdades $AC = I$ o $CA = I$ (lección 3.3). Pero por seguridad, ambos chequeos son recomendables hasta tener práctica.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Una matriz no invertible",
          problema_md=(
              "Estudia si $B = \\begin{bmatrix} 1 & 2 \\\\ 2 & 4 \\end{bmatrix}$ es invertible."
          ),
          pasos=[
              {"accion_md": (
                  "Reducimos por filas: $F_2 \\leftarrow F_2 - 2F_1$ da $\\begin{bmatrix} 1 & 2 \\\\ 0 & 0 \\end{bmatrix}$."
              ),
               "justificacion_md": "Solo $1$ pivote en $2$ columnas $\\Rightarrow$ las columnas son **LD** (la 2ª es el doble de la 1ª).",
               "es_resultado": False},
              {"accion_md": (
                  "$B$ no tiene pivote en cada columna $\\Rightarrow$ $B\\vec{x} = \\vec{0}$ tiene soluciones no triviales $\\Rightarrow$ **$B$ no es invertible** (es **singular**)."
              ),
               "justificacion_md": "**Criterio que usaremos en 3.3 (TMI):** $A$ invertible $\\iff$ $A$ tiene pivote en cada columna $\\iff$ columnas LI.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Fórmula $2 \\times 2$",
          enunciado_md=(
              "Sea $A = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$. Definimos $\\det(A) = ad - bc$.\n\n"
              "**Si $\\det(A) \\neq 0$,** entonces $A$ es invertible y\n\n"
              "$$\\boxed{A^{-1} = \\frac{1}{ad - bc}\\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix}.}$$\n\n"
              "**Si $\\det(A) = 0$,** $A$ **no** es invertible.\n\n"
              "**Mnemónico:** intercambia las entradas de la diagonal y cambia el signo de las entradas anti-diagonales; divide todo por $\\det A$."
          ),
          demostracion_md=(
              "Llamemos $C$ a la matriz que aparece en la fórmula. Calculamos:\n\n"
              "$AC = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}\\frac{1}{ad-bc}\\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix} = \\frac{1}{ad-bc}\\begin{bmatrix} ad - bc & 0 \\\\ 0 & ad - bc \\end{bmatrix} = I_2.$\n\n"
              "Análogamente $CA = I_2$. Por unicidad, $C = A^{-1}$. $\\blacksquare$\n\n"
              "**Si $\\det A = 0$**, las columnas son LD (una es múltiplo de la otra) $\\Rightarrow$ rango $< 2 \\Rightarrow$ $A$ no es invertible."
          )),

        b("ejemplo_resuelto",
          titulo="Inversa $2 \\times 2$ con verificación",
          problema_md=(
              "Halla $A^{-1}$ para $A = \\begin{bmatrix} 3 & 5 \\\\ 4 & 6 \\end{bmatrix}$ y verifica $AA^{-1} = I_2$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\det A = 3\\cdot 6 - 5\\cdot 4 = 18 - 20 = -2 \\neq 0$ $\\Rightarrow$ $A$ es invertible."
              ),
               "justificacion_md": "Primer chequeo: ¿es invertible?",
               "es_resultado": False},
              {"accion_md": (
                  "$A^{-1} = \\dfrac{1}{-2}\\begin{bmatrix} 6 & -5 \\\\ -4 & 3 \\end{bmatrix} = \\begin{bmatrix} -3 & 5/2 \\\\ 2 & -3/2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Aplicación directa de la fórmula.",
               "es_resultado": False},
              {"accion_md": (
                  "$AA^{-1} = \\begin{bmatrix} 3 & 5 \\\\ 4 & 6 \\end{bmatrix}\\begin{bmatrix} -3 & 5/2 \\\\ 2 & -3/2 \\end{bmatrix} = \\begin{bmatrix} -9 + 10 & 15/2 - 15/2 \\\\ -12 + 12 & 10 - 9 \\end{bmatrix} = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} = I_2$ ✓."
              ),
               "justificacion_md": "Siempre verifica el resultado — un signo equivocado se detecta al instante.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Resolver $A\\vec{x} = \\vec{b}$ con $A^{-1}$",
          enunciado_md=(
              "Si $A \\in \\mathbb{R}^{n \\times n}$ es **invertible**, entonces para todo $\\vec{b} \\in \\mathbb{R}^n$ el sistema $A\\vec{x} = \\vec{b}$ es **consistente y tiene solución única**\n\n"
              "$$\\boxed{\\vec{x} = A^{-1}\\vec{b}.}$$"
          ),
          demostracion_md=(
              "Multiplicando $A\\vec{x} = \\vec{b}$ por $A^{-1}$ a la izquierda: $A^{-1}A\\vec{x} = A^{-1}\\vec{b}$, es decir $I\\vec{x} = \\vec{x} = A^{-1}\\vec{b}$. Esto da existencia y unicidad simultáneamente. $\\blacksquare$\n\n"
              "**Observación práctica.** El método solo aplica si $A$ es invertible. En la práctica, **resolver por Gauss-Jordan suele ser más eficiente** que calcular $A^{-1}$ y luego $A^{-1}\\vec{b}$ — la inversa es útil **conceptualmente** y cuando hay que resolver $A\\vec{x} = \\vec{b}$ para muchos $\\vec{b}$ distintos."
          )),

        b("ejemplo_resuelto",
          titulo="Resolver $A\\vec{x} = \\vec{b}$ con la inversa",
          problema_md=(
              "Resuelve $A\\vec{x} = \\vec{b}$ con $A = \\begin{bmatrix} 3 & 4 \\\\ 5 & 6 \\end{bmatrix}$ y $\\vec{b} = \\begin{bmatrix} 3 \\\\ 7 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\det A = 3\\cdot 6 - 4\\cdot 5 = -2$. Entonces $A^{-1} = \\dfrac{1}{-2}\\begin{bmatrix} 6 & -4 \\\\ -5 & 3 \\end{bmatrix} = \\begin{bmatrix} -3 & 2 \\\\ 5/2 & -3/2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Fórmula $2 \\times 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\vec{x} = A^{-1}\\vec{b} = \\begin{bmatrix} -3 & 2 \\\\ 5/2 & -3/2 \\end{bmatrix}\\begin{bmatrix} 3 \\\\ 7 \\end{bmatrix} = \\begin{bmatrix} -9 + 14 \\\\ 15/2 - 21/2 \\end{bmatrix} = \\begin{bmatrix} 5 \\\\ -3 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Producto matriz-vector estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación:** $A\\vec{x} = \\begin{bmatrix} 3 & 4 \\\\ 5 & 6 \\end{bmatrix}\\begin{bmatrix} 5 \\\\ -3 \\end{bmatrix} = \\begin{bmatrix} 15 - 12 \\\\ 25 - 18 \\end{bmatrix} = \\begin{bmatrix} 3 \\\\ 7 \\end{bmatrix} = \\vec{b}$ ✓."
              ),
               "justificacion_md": "Comprobar el resultado en el sistema original es la manera más confiable de detectar errores.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Propiedades algebraicas de la inversa",
            body=(
                "Sean $A, B \\in \\mathbb{R}^{n \\times n}$ invertibles y $k \\in \\mathbb{N}$. Entonces:\n\n"
                "| Propiedad | Fórmula |\n|---|---|\n"
                "| Doble inversa | $(A^{-1})^{-1} = A$ |\n"
                "| **Producto (orden invertido)** | $(AB)^{-1} = B^{-1}A^{-1}$ |\n"
                "| Transpuesta | $(A^T)^{-1} = (A^{-1})^T$ |\n"
                "| Potencia | $(A^k)^{-1} = (A^{-1})^k$ — definimos $A^{-k} = (A^{-1})^k$ |\n"
                "| Múltiplo escalar | $(rA)^{-1} = \\tfrac{1}{r} A^{-1}$ si $r \\neq 0$ |\n\n"
                "**Por qué $(AB)^{-1} = B^{-1}A^{-1}$ y no $A^{-1}B^{-1}$:** la inversa 'deshace' las operaciones en orden inverso. Si te pones zapato izquierdo y luego derecho, te los quitas en orden inverso."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Verificando $(AB)^{-1} = B^{-1}A^{-1}$",
          problema_md=(
              "Para $A = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}$ y $B = \\begin{bmatrix} 2 & 0 \\\\ 0 & 3 \\end{bmatrix}$, verifica que $(AB)^{-1} = B^{-1}A^{-1}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A^{-1} = \\begin{bmatrix} 1 & -1 \\\\ 0 & 1 \\end{bmatrix}$ (fórmula $2\\times 2$, $\\det A = 1$). $B^{-1} = \\begin{bmatrix} 1/2 & 0 \\\\ 0 & 1/3 \\end{bmatrix}$ (diagonal: invertir entradas)."
              ),
               "justificacion_md": "Para diagonales, $\\text{diag}(d_1, \\ldots)^{-1} = \\text{diag}(1/d_1, \\ldots)$ si todos los $d_i \\neq 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "$AB = \\begin{bmatrix} 2 & 3 \\\\ 0 & 3 \\end{bmatrix}$, $\\det(AB) = 6$. Por la fórmula, $(AB)^{-1} = \\dfrac{1}{6}\\begin{bmatrix} 3 & -3 \\\\ 0 & 2 \\end{bmatrix} = \\begin{bmatrix} 1/2 & -1/2 \\\\ 0 & 1/3 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Cálculo directo de la inversa del producto.",
               "es_resultado": False},
              {"accion_md": (
                  "$B^{-1}A^{-1} = \\begin{bmatrix} 1/2 & 0 \\\\ 0 & 1/3 \\end{bmatrix}\\begin{bmatrix} 1 & -1 \\\\ 0 & 1 \\end{bmatrix} = \\begin{bmatrix} 1/2 & -1/2 \\\\ 0 & 1/3 \\end{bmatrix} = (AB)^{-1}$ ✓."
              ),
               "justificacion_md": "El orden invertido es **esencial**: $A^{-1}B^{-1}$ daría una matriz distinta.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Algoritmo para calcular $A^{-1}$ por reducción por filas",
          enunciado_md=(
              "Sea $A \\in \\mathbb{R}^{n \\times n}$. Para decidir si $A$ es invertible y, en caso afirmativo, hallar $A^{-1}$:\n\n"
              "1. Forma la **matriz aumentada** $[\\,A \\mid I_n\\,]$.\n"
              "2. Aplica OEF (intercambio, reemplazo y/o escalamiento) hasta transformar el bloque izquierdo en $I_n$.\n"
              "3. Si lo logras, **$A$ es invertible y $A^{-1}$ aparece en el bloque derecho**: $[\\,I_n \\mid A^{-1}\\,]$.\n\n"
              "Si en algún momento aparece una fila $[\\,0\\ \\cdots\\ 0 \\mid *\\,]$ en el bloque izquierdo, $A$ **no es invertible**."
          ),
          demostracion_md=(
              "**Idea:** las OEF que llevan $A$ a $I$ son matrices elementales $E_1, \\ldots, E_k$ tales que $E_k \\cdots E_1 A = I$. Pero entonces $E_k \\cdots E_1 = A^{-1}$, y aplicar esa misma sucesión de OEF al bloque derecho transforma $I$ en $E_k \\cdots E_1\\,I = A^{-1}$. La justificación formal viene en la lección 3.3 (matrices elementales). $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Inversa $3 \\times 3$ por Gauss-Jordan",
          problema_md=(
              "Halla $A^{-1}$, si existe, para $A = \\begin{bmatrix} 0 & 1 & 2 \\\\ 1 & 0 & 3 \\\\ 4 & -3 & 8 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Formamos $[A \\mid I_3]$ y aplicamos $F_1 \\leftrightarrow F_2$ (para tener pivote $1$ en $(1,1)$):\n\n"
                  "$\\left[\\begin{array}{rrr|rrr} 1 & 0 & 3 & 0 & 1 & 0 \\\\ 0 & 1 & 2 & 1 & 0 & 0 \\\\ 4 & -3 & 8 & 0 & 0 & 1 \\end{array}\\right]$."
              ),
               "justificacion_md": "Intercambio para evitar el cero en $(1,1)$.",
               "es_resultado": False},
              {"accion_md": (
                  "$F_3 \\leftarrow F_3 - 4F_1$ y luego $F_3 \\leftarrow F_3 + 3F_2$:\n\n"
                  "$\\left[\\begin{array}{rrr|rrr} 1 & 0 & 3 & 0 & 1 & 0 \\\\ 0 & 1 & 2 & 1 & 0 & 0 \\\\ 0 & 0 & 2 & 3 & -4 & 1 \\end{array}\\right]$."
              ),
               "justificacion_md": "Anulamos debajo de los pivotes columna por columna.",
               "es_resultado": False},
              {"accion_md": (
                  "$F_3 \\leftarrow \\tfrac{1}{2}F_3$, luego $F_1 \\leftarrow F_1 - 3F_3$ y $F_2 \\leftarrow F_2 - 2F_3$:\n\n"
                  "$\\left[\\begin{array}{rrr|rrr} 1 & 0 & 0 & -9/2 & 7 & -3/2 \\\\ 0 & 1 & 0 & -2 & 4 & -1 \\\\ 0 & 0 & 1 & 3/2 & -2 & 1/2 \\end{array}\\right]$."
              ),
               "justificacion_md": "Normalizar pivotes y anular arriba — RREF lograda.",
               "es_resultado": False},
              {"accion_md": (
                  "**$A^{-1} = \\begin{bmatrix} -9/2 & 7 & -3/2 \\\\ -2 & 4 & -1 \\\\ 3/2 & -2 & 1/2 \\end{bmatrix}$.**\n\n"
                  "**Verificación rápida:** $A A^{-1}$ debe ser $I_3$ — calcular al menos una entrada no diagonal para chequear."
              ),
               "justificacion_md": "El bloque derecho final es la inversa.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Una matriz $A \\in \\mathbb{R}^{3 \\times 4}$:",
                  "opciones_md": [
                      "Puede tener inversa si $\\det A \\neq 0$",
                      "Tiene inversa si sus columnas son LI",
                      "Nunca tiene inversa (la noción de inversa requiere matriz cuadrada)",
                      "Tiene inversa si tiene pivote en cada columna",
                  ],
                  "correcta": "C",
                  "pista_md": "$A^{-1}$ es la matriz tal que $AA^{-1} = A^{-1}A = I$. ¿De qué tamaño debería ser $I$?",
                  "explicacion_md": "**La inversa solo está definida para matrices cuadradas.** Para rectangulares se definen pseudo-inversas (cap. 7), que no satisfacen las mismas propiedades.",
              },
              {
                  "enunciado_md": "Si $\\det A = 0$ con $A = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$, entonces:",
                  "opciones_md": [
                      "$A^{-1} = \\frac{1}{0}\\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix}$",
                      "$A$ no es invertible",
                      "$A = I_2$",
                      "$A$ es la matriz cero",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\det A = 0 \\iff$ las columnas son LD.",
                  "explicacion_md": "**$A$ es singular** (no invertible). La fórmula $\\frac{1}{ad - bc}$ no aplica porque dividiríamos por $0$.",
              },
              {
                  "enunciado_md": "$(AB)^{-1}$ es igual a:",
                  "opciones_md": ["$A^{-1}B^{-1}$", "$B^{-1}A^{-1}$", "$AB^{-1}$", "$B A^{-1}$"],
                  "correcta": "B",
                  "pista_md": "La inversa del producto **invierte** el orden, igual que la transpuesta.",
                  "explicacion_md": "**$(AB)^{-1} = B^{-1}A^{-1}$.** Verificar: $(AB)(B^{-1}A^{-1}) = A(BB^{-1})A^{-1} = AA^{-1} = I$.",
              },
          ]),

        ej(
            "Inversa $2 \\times 2$ por fórmula",
            "Calcula $B^{-1}$ para $B = \\begin{bmatrix} 3 & 1 \\\\ 4 & 2 \\end{bmatrix}$ y verifica $BB^{-1} = I_2$.",
            [
                "$\\det B = 3\\cdot 2 - 1\\cdot 4$.",
                "Aplica la fórmula y verifica multiplicando $B$ por el resultado.",
            ],
            (
                "$\\det B = 6 - 4 = 2 \\neq 0$. $B^{-1} = \\dfrac{1}{2}\\begin{bmatrix} 2 & -1 \\\\ -4 & 3 \\end{bmatrix} = \\begin{bmatrix} 1 & -1/2 \\\\ -2 & 3/2 \\end{bmatrix}.$\n\n"
                "Verificación: $BB^{-1} = \\begin{bmatrix} 3 & 1 \\\\ 4 & 2 \\end{bmatrix}\\begin{bmatrix} 1 & -1/2 \\\\ -2 & 3/2 \\end{bmatrix} = \\begin{bmatrix} 3-2 & -3/2 + 3/2 \\\\ 4-4 & -2+3 \\end{bmatrix} = I_2$ ✓."
            ),
        ),

        ej(
            "Resolver con la inversa",
            "Usa $A^{-1}$ para resolver $A\\vec{x} = \\vec{b}$ con $A = \\begin{bmatrix} 1 & 2 \\\\ 3 & 7 \\end{bmatrix}$ y $\\vec{b} = \\begin{bmatrix} 5 \\\\ 18 \\end{bmatrix}$.",
            [
                "$\\det A = 1$.",
                "Aplica $\\vec{x} = A^{-1}\\vec{b}$.",
            ],
            (
                "$\\det A = 7 - 6 = 1$. $A^{-1} = \\begin{bmatrix} 7 & -2 \\\\ -3 & 1 \\end{bmatrix}$.\n\n"
                "$\\vec{x} = A^{-1}\\vec{b} = \\begin{bmatrix} 7 & -2 \\\\ -3 & 1 \\end{bmatrix}\\begin{bmatrix} 5 \\\\ 18 \\end{bmatrix} = \\begin{bmatrix} 35 - 36 \\\\ -15 + 18 \\end{bmatrix} = \\begin{bmatrix} -1 \\\\ 3 \\end{bmatrix}.$\n\n"
                "Verificación: $A\\vec{x} = (-1 + 6, -3 + 21)^T = (5, 18)^T = \\vec{b}$ ✓."
            ),
        ),

        ej(
            "Inversa $3 \\times 3$ por Gauss-Jordan",
            "Halla $A^{-1}$ para $A = \\begin{bmatrix} 1 & -2 & 1 \\\\ 4 & -7 & 3 \\\\ -2 & 6 & -4 \\end{bmatrix}$.",
            [
                "Forma $[A \\mid I_3]$ y reduce a $[I_3 \\mid A^{-1}]$.",
                "Verifica al final calculando $AA^{-1}$ (al menos una entrada).",
            ],
            (
                "Tras aplicar OEF a $[A \\mid I_3]$ se llega a $[I_3 \\mid A^{-1}]$ con\n\n"
                "$A^{-1} = \\begin{bmatrix} 5 & -1 & 1/2 \\\\ 5 & -1 & 1/2 \\\\ 5 & -1 & 1/2 \\end{bmatrix}$ — *espera*, hay un error: revisamos.\n\n"
                "**Procedimiento correcto:** $F_2 \\leftarrow F_2 - 4F_1$, $F_3 \\leftarrow F_3 + 2F_1$ dan $\\begin{bmatrix} 1 & -2 & 1 \\\\ 0 & 1 & -1 \\\\ 0 & 2 & -2 \\end{bmatrix}$ en el bloque izquierdo. La fila $3$ resulta proporcional a la $2$ $\\Rightarrow$ tras $F_3 \\leftarrow F_3 - 2F_2$ obtenemos una fila de ceros.\n\n"
                "**Conclusión:** $A$ **no es invertible** (sus columnas son LD: la columna $3$ es combinación lineal de las dos primeras)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Hablar de inversa de matrices no cuadradas.** $A^{-1}$ exige $A \\in \\mathbb{R}^{n \\times n}$.",
              "**Asumir que toda matriz cuadrada tiene inversa.** Solo si $\\det A \\neq 0$ (equivalente: rango $= n$).",
              "**Escribir $(AB)^{-1} = A^{-1}B^{-1}$.** Lo correcto: $\\boxed{(AB)^{-1} = B^{-1}A^{-1}}$.",
              "**Olvidar el factor $\\dfrac{1}{ad - bc}$** en la fórmula $2\\times 2$.",
              "**Cambiar las entradas equivocadas** en la fórmula. Lo correcto: intercambiar $a \\leftrightarrow d$ y cambiar signo a $b, c$.",
              "**Calcular $A^{-1}$ para resolver un único $A\\vec{x} = \\vec{b}$.** Suele ser más eficiente reducir $[A \\mid \\vec{b}]$ directamente; la inversa se justifica cuando hay muchos $\\vec{b}$.",
              "**Detenerse en REF y leer 'inversa' del bloque derecho.** El algoritmo exige llegar hasta **RREF** (bloque izquierdo $= I_n$).",
          ]),

        b("resumen",
          puntos_md=[
              "**$A$ invertible $\\iff$ existe $C$ con $AC = CA = I_n$.** Solo para matrices cuadradas.",
              "**Fórmula $2\\times 2$:** $A^{-1} = \\dfrac{1}{\\det A}\\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix}$ si $\\det A = ad - bc \\neq 0$.",
              "**Algoritmo general:** reducir $[A \\mid I]$ a $[I \\mid A^{-1}]$ por OEF.",
              "**Resolver sistemas:** si $A$ es invertible, $A\\vec{x} = \\vec{b} \\Rightarrow \\vec{x} = A^{-1}\\vec{b}$ (única).",
              "**Propiedades:** $(A^{-1})^{-1} = A$, $(AB)^{-1} = B^{-1}A^{-1}$ (orden invertido), $(A^T)^{-1} = (A^{-1})^T$.",
              "**Próxima lección:** matrices elementales — la justificación rigurosa del algoritmo $[A\\mid I] \\to [I\\mid A^{-1}]$ y el **Teorema de la Matriz Invertible**.",
          ]),
    ]
    return {
        "id": "lec-al-3-2-inversa",
        "title": "Inversa",
        "description": "Matriz invertible, fórmula $2\\times 2$ y $\\det = ad - bc$, algoritmo Gauss-Jordan $[A\\mid I]\\to[I\\mid A^{-1}]$, propiedades $(AB)^{-1} = B^{-1}A^{-1}$.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# =====================================================================
# 3.3 Matrices elementales (incluye TMI)
# =====================================================================
def lesson_3_3():
    blocks = [
        b("texto", body_md=(
            "Esta lección cierra el círculo entre los dos grandes lenguajes que hemos venido usando: "
            "**operaciones elementales de fila** (capítulo 2) y **producto de matrices** (lección 3.1). "
            "El puente son las **matrices elementales**: matrices que, al multiplicarlas por la izquierda, "
            "ejecutan exactamente una OEF.\n\n"
            "Con esta visión:\n\n"
            "- Justificamos rigurosamente el algoritmo $[A \\mid I] \\to [I \\mid A^{-1}]$.\n"
            "- Probamos el **Teorema de la Matriz Invertible (TMI)**: una docena de propiedades equivalentes "
            "que conectan invertibilidad, pivotes, independencia lineal, sistemas y transformaciones lineales.\n"
            "- Definimos cuándo una **transformación lineal** es invertible y damos su fórmula explícita."
        )),

        b("definicion",
          titulo="Matriz elemental",
          body_md=(
              "Una **matriz elemental** $E$ se obtiene al aplicar **una única** OEF a la identidad $I_m$. Hay tres tipos:\n\n"
              "| Tipo de OEF | Cómo se construye $E$ | Efecto de $EA$ |\n|---|---|---|\n"
              "| **Reemplazo:** $F_i \\leftarrow F_i + k F_j$ | $E = I_m$ con $E_{ij} = k$ (en la posición $(i,j)$) | Suma $k$ veces la fila $j$ a la fila $i$ de $A$ |\n"
              "| **Intercambio:** $F_i \\leftrightarrow F_j$ | $E = I_m$ con filas $i, j$ permutadas | Permuta esas dos filas en $A$ |\n"
              "| **Escalamiento:** $F_i \\leftarrow c F_i$ ($c \\neq 0$) | $E = I_m$ con $E_{ii} = c$ | Multiplica por $c$ la fila $i$ de $A$ |"
          )),

        b("ejemplo_resuelto",
          titulo="Efecto de las elementales por la izquierda",
          problema_md=(
              "Sean\n\n"
              "$E_1 = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ -4 & 0 & 1 \\end{bmatrix}, \\ "
              "E_2 = \\begin{bmatrix} 0 & 1 & 0 \\\\ 1 & 0 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}, \\ "
              "E_3 = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 5 \\end{bmatrix}, \\ "
              "A = \\begin{bmatrix} a & b & c \\\\ d & e & f \\\\ g & h & i \\end{bmatrix}.$\n\n"
              "Calcula $E_1 A$, $E_2 A$, $E_3 A$ y describe la OEF que cada producto realiza."
          ),
          pasos=[
              {"accion_md": (
                  "$E_1 A = \\begin{bmatrix} a & b & c \\\\ d & e & f \\\\ g - 4a & h - 4b & i - 4c \\end{bmatrix}$ — **reemplazo** $F_3 \\leftarrow F_3 - 4F_1$."
              ),
               "justificacion_md": "$E_1$ es $I_3$ con $E_{31} = -4$ — corresponde a 'sumar $-4$ veces la fila $1$ a la fila $3$'.",
               "es_resultado": False},
              {"accion_md": (
                  "$E_2 A = \\begin{bmatrix} d & e & f \\\\ a & b & c \\\\ g & h & i \\end{bmatrix}$ — **intercambio** $F_1 \\leftrightarrow F_2$."
              ),
               "justificacion_md": "$E_2$ es $I_3$ con las dos primeras filas permutadas.",
               "es_resultado": False},
              {"accion_md": (
                  "$E_3 A = \\begin{bmatrix} a & b & c \\\\ d & e & f \\\\ 5g & 5h & 5i \\end{bmatrix}$ — **escalamiento** $F_3 \\leftarrow 5F_3$."
              ),
               "justificacion_md": "$E_3$ es $I_3$ con $E_{33} = 5$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Multiplicar por una elemental = aplicar la OEF",
          enunciado_md=(
              "Si $E \\in \\mathbb{R}^{m \\times m}$ es una matriz elemental (obtenida de $I_m$ con cierta OEF) y $A \\in \\mathbb{R}^{m \\times n}$, entonces $EA$ es la matriz que resulta de aplicar **esa misma OEF** a $A$."
          ),
          demostracion_md=(
              "**Idea.** $E$ es $I_m$ con una sola fila modificada. La fila $i$ de $EA$ es $\\text{fila}_i(E)\\,A$. Si $\\text{fila}_i(E) = \\vec{e}_i^T$ (no fue modificada), $\\text{fila}_i(EA) = \\text{fila}_i(A)$. Si fue modificada, el producto $\\text{fila}_i(E)\\,A$ combina linealmente las filas de $A$ exactamente como prescribe la OEF. $\\blacksquare$"
          )),

        b("teorema",
          nombre="Las matrices elementales son invertibles",
          enunciado_md=(
              "Toda matriz elemental $E$ es invertible y $E^{-1}$ es **del mismo tipo** pero con el **parámetro opuesto**:\n\n"
              "| OEF original | OEF inversa | $E^{-1}$ es elemental |\n|---|---|---|\n"
              "| $F_i \\leftarrow F_i + k F_j$ | $F_i \\leftarrow F_i - k F_j$ | mismo tipo, $k \\to -k$ |\n"
              "| $F_i \\leftrightarrow F_j$ | $F_i \\leftrightarrow F_j$ (la misma) | el mismo intercambio |\n"
              "| $F_i \\leftarrow c F_i$ | $F_i \\leftarrow \\tfrac{1}{c} F_i$ | mismo tipo, $c \\to 1/c$ |"
          ),
          demostracion_md=(
              "Cada OEF tiene una OEF inversa explícita (mostrada arriba): aplicar primero una y luego la otra deja intacta cualquier matriz $A$. Es decir, $E^{-1}E = I = EE^{-1}$. $\\blacksquare$\n\n"
              "**Ejemplo:** si $E_1$ realiza $F_3 \\leftarrow F_3 - 4F_1$, entonces $E_1^{-1} = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 4 & 0 & 1 \\end{bmatrix}$ realiza $F_3 \\leftarrow F_3 + 4F_1$."
          )),

        b("teorema",
          nombre="Criterio de invertibilidad y justificación del algoritmo",
          enunciado_md=(
              "Sea $A \\in \\mathbb{R}^{n \\times n}$. Son **equivalentes**:\n\n"
              "(a) $A$ es invertible.\n\n"
              "(b) $A$ es **equivalente por filas** a $I_n$ (existe una sucesión de OEF que transforma $A$ en $I_n$).\n\n"
              "Además, si $E_k \\cdots E_2 E_1 A = I_n$ con $E_i$ elementales, entonces\n\n"
              "$$\\boxed{A^{-1} = E_k \\cdots E_2 E_1.}$$"
          ),
          demostracion_md=(
              "**(a) $\\Rightarrow$ (b)** Si $A$ es invertible, su RREF es $I_n$ (tiene pivote en cada columna y cada fila), así que existen $E_i$ con $E_k \\cdots E_1 A = I_n$.\n\n"
              "**(b) $\\Rightarrow$ (a)** Si $E_k \\cdots E_1 A = I_n$, definimos $C = E_k \\cdots E_1$ (producto de invertibles, luego invertible). Entonces $CA = I_n$, y multiplicando por $C^{-1}$: $A = C^{-1}$, así $AC = I_n$. Luego $C = A^{-1}$. $\\blacksquare$\n\n"
              "**Consecuencia práctica.** Al reducir $[\\,A \\mid I_n\\,] \\to [\\,I_n \\mid B\\,]$, en el bloque derecho hemos aplicado la misma sucesión de OEF a $I_n$, obteniendo $E_k \\cdots E_1 \\,I_n = E_k \\cdots E_1 = A^{-1}$. **Esa es la justificación rigurosa del algoritmo de la lección 3.2.**"
          )),

        b("teorema",
          nombre="Teorema de la Matriz Invertible (TMI)",
          enunciado_md=(
              "Sea $A \\in \\mathbb{R}^{n \\times n}$. Las siguientes afirmaciones son **equivalentes** "
              "(o todas verdaderas, o todas falsas):\n\n"
              "(a) $A$ es invertible.\n\n"
              "(b) $A$ es equivalente por filas a $I_n$.\n\n"
              "(c) $A$ tiene **$n$ posiciones pivote** (una por fila/columna).\n\n"
              "(d) La ecuación homogénea $A\\vec{x} = \\vec{0}$ solo tiene la **solución trivial**.\n\n"
              "(e) Las **columnas de $A$** son linealmente **independientes**.\n\n"
              "(f) La transformación lineal $T(\\vec{x}) = A\\vec{x}$ es **uno a uno** (inyectiva).\n\n"
              "(g) Para todo $\\vec{b} \\in \\mathbb{R}^n$, $A\\vec{x} = \\vec{b}$ es **consistente**.\n\n"
              "(h) Las columnas de $A$ **generan** $\\mathbb{R}^n$.\n\n"
              "(i) $T(\\vec{x}) = A\\vec{x}$ es **sobre** $\\mathbb{R}^n$ (sobreyectiva).\n\n"
              "(j) Existe $C \\in \\mathbb{R}^{n \\times n}$ con $CA = I_n$ (inversa por la izquierda).\n\n"
              "(k) Existe $D \\in \\mathbb{R}^{n \\times n}$ con $AD = I_n$ (inversa por la derecha).\n\n"
              "(l) $A^T$ es invertible.\n\n"
              "**Consecuencia muy útil:** para matrices **cuadradas**, basta verificar **una** inversa lateral (ej. $CA = I$) para concluir que $C = A^{-1}$ y $AC = I$ también."
          ),
          demostracion_md=(
              "**Esquema cíclico** (cada implicación se prueba con resultados previos del curso):\n\n"
              "$(a) \\Leftrightarrow (b) \\Leftrightarrow (c)$ por el algoritmo y la definición de pivote.\n\n"
              "$(c) \\Leftrightarrow (d) \\Leftrightarrow (e) \\Leftrightarrow (f)$: pivote en cada columna $\\iff$ no hay variables libres en $A\\vec{x} = \\vec{0}$ $\\iff$ columnas LI $\\iff$ $T$ inyectiva (lección 2.5).\n\n"
              "$(c) \\Leftrightarrow (g) \\Leftrightarrow (h) \\Leftrightarrow (i)$: pivote en cada fila $\\iff$ $A\\vec{x} = \\vec{b}$ siempre consistente $\\iff$ columnas generan $\\mathbb{R}^n$ $\\iff$ $T$ sobreyectiva. Pero en el caso **cuadrado** $n \\times n$, 'pivote en cada columna' y 'pivote en cada fila' son equivalentes (mismo número $n$).\n\n"
              "$(j) \\Rightarrow (a)$: si $CA = I$ entonces $A\\vec{x} = \\vec{0} \\Rightarrow CA\\vec{x} = \\vec{x} = C\\vec{0} = \\vec{0}$, luego (d), luego (a).\n\n"
              "$(l)$: $A^T$ invertible $\\iff$ $\\text{rango}(A^T) = n \\iff \\text{rango}(A) = n \\iff (a)$. $\\blacksquare$"
          )),

        b("intuicion", body_md=(
            "**Lectura práctica del TMI.** En la práctica, **basta con verificar una sola condición** (la más cómoda) para concluir todas las demás. Las más usadas:\n\n"
            "- **Reducir $A$ y contar pivotes.** Si hay $n$ pivotes, $A$ es invertible (y todo lo demás del TMI).\n"
            "- **Calcular $\\det A$** (cap. 4): si $\\det A \\neq 0$, $A$ es invertible.\n"
            "- **Verificar columnas LI** (a veces obvio por inspección).\n\n"
            "El TMI es el resultado **más usado** del álgebra lineal computacional."
        )),

        b("ejemplo_resuelto",
          titulo="Aplicación del TMI",
          problema_md=(
              "Decide si $A = \\begin{bmatrix} 1 & 0 & -2 \\\\ 3 & 1 & -2 \\\\ -5 & -1 & 9 \\end{bmatrix}$ es invertible."
          ),
          pasos=[
              {"accion_md": (
                  "Reducimos $A$: $F_2 \\leftarrow F_2 - 3F_1$, $F_3 \\leftarrow F_3 + 5F_1$:\n\n"
                  "$\\begin{bmatrix} 1 & 0 & -2 \\\\ 0 & 1 & 4 \\\\ 0 & -1 & -1 \\end{bmatrix}$. Luego $F_3 \\leftarrow F_3 + F_2$: $\\begin{bmatrix} 1 & 0 & -2 \\\\ 0 & 1 & 4 \\\\ 0 & 0 & 3 \\end{bmatrix}$."
              ),
               "justificacion_md": "REF obtenida.",
               "es_resultado": False},
              {"accion_md": (
                  "**Hay $3$ pivotes** en una matriz $3 \\times 3$ $\\Rightarrow$ se cumple (c) $\\Rightarrow$ por TMI, **$A$ es invertible** y todas las demás propiedades del teorema valen."
              ),
               "justificacion_md": "No hace falta calcular $A^{-1}$ explícitamente para responder a la pregunta de invertibilidad.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Transformaciones lineales invertibles",
          body_md=(
              "Una transformación lineal $T : \\mathbb{R}^n \\to \\mathbb{R}^n$ es **invertible** si existe otra transformación lineal $S : \\mathbb{R}^n \\to \\mathbb{R}^n$ tal que\n\n"
              "$$S(T(\\vec{x})) = \\vec{x} \\quad \\text{y} \\quad T(S(\\vec{x})) = \\vec{x} \\qquad \\forall \\vec{x} \\in \\mathbb{R}^n.$$\n\n"
              "En tal caso, $S$ es la **inversa** de $T$ y se denota $T^{-1}$.\n\n"
              "**Conexión con la matriz estándar.** Si $T(\\vec{x}) = A\\vec{x}$ con $A$ la matriz estándar de $T$, entonces:\n\n"
              "- $T$ es invertible $\\iff$ $A$ es invertible.\n"
              "- En tal caso, $T^{-1}(\\vec{x}) = A^{-1}\\vec{x}$.\n"
              "- $T$ uno a uno $\\iff$ columnas de $A$ LI; $T$ sobre $\\iff$ columnas de $A$ generan $\\mathbb{R}^n$ — equivalentes por TMI.\n\n"
              "**Para transformaciones $\\mathbb{R}^n \\to \\mathbb{R}^n$**, ser inyectiva, ser sobreyectiva y ser invertible son **lo mismo**."
          )),

        b("ejemplo_resuelto",
          titulo="Invertibilidad por la matriz estándar",
          problema_md=(
              "Sea $T : \\mathbb{R}^3 \\to \\mathbb{R}^3$ con matriz estándar "
              "$A = \\begin{bmatrix} 1 & -4 & 8 \\\\ 0 & 2 & -1 \\\\ 0 & 0 & 5 \\end{bmatrix}$. ¿Es $T$ invertible? Si lo es, ¿cómo se calcula $T^{-1}$?"
          ),
          pasos=[
              {"accion_md": (
                  "$A$ es **triangular superior** con diagonal $(1, 2, 5)$ — todas no nulas. Su determinante es el producto de la diagonal: $\\det A = 1 \\cdot 2 \\cdot 5 = 10 \\neq 0$ (cap. 4)."
              ),
               "justificacion_md": "Para triangulares, $\\det = $ producto de la diagonal. Lo demostraremos formalmente en cap. 4.",
               "es_resultado": False},
              {"accion_md": (
                  "Por TMI, **$A$ es invertible** $\\Rightarrow$ **$T$ es invertible**. Su inversa es $T^{-1}(\\vec{x}) = A^{-1}\\vec{x}$, que se calcula con el algoritmo de Gauss-Jordan."
              ),
               "justificacion_md": "**Geometría:** $T$ es una composición de un escalamiento + una rotación + un trasquilado. Como ninguna 'colapsa' información, $T$ es invertible.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$E$ es elemental con $E_{31} = -4$ (resto $= I_3$). $E^{-1}$ es:",
                  "opciones_md": [
                      "$E$ misma",
                      "$I_3$ con $E_{31} = 4$",
                      "$I_3$ con $E_{31} = -1/4$",
                      "$\\mathbf{0}$",
                  ],
                  "correcta": "B",
                  "pista_md": "La OEF $F_3 \\leftarrow F_3 - 4F_1$ se 'deshace' con $F_3 \\leftarrow F_3 + 4F_1$.",
                  "explicacion_md": "**$E^{-1}$ tiene $E_{31} = +4$.** Para el reemplazo, basta cambiar el signo del parámetro.",
              },
              {
                  "enunciado_md": "Si $A \\in \\mathbb{R}^{n\\times n}$ y $CA = I_n$, entonces:",
                  "opciones_md": [
                      "$A$ podría no ser invertible",
                      "$AC = I_n$ también, y $C = A^{-1}$",
                      "$A$ es singular",
                      "$C = A$",
                  ],
                  "correcta": "B",
                  "pista_md": "TMI: para matrices cuadradas basta una inversa lateral.",
                  "explicacion_md": "Por TMI ((j) $\\Rightarrow$ (a)), $CA = I$ implica $A$ invertible; entonces $C = A^{-1}$ y también $AC = I$.",
              },
              {
                  "enunciado_md": "Una transformación lineal $T : \\mathbb{R}^4 \\to \\mathbb{R}^4$ es uno a uno. ¿Es necesariamente sobre?",
                  "opciones_md": [
                      "No, son condiciones independientes",
                      "Sí, por TMI (caso cuadrado)",
                      "Solo si la matriz es triangular",
                      "Solo si $T$ es la identidad",
                  ],
                  "correcta": "B",
                  "pista_md": "Para transformaciones $\\mathbb{R}^n \\to \\mathbb{R}^n$, inyectiva $\\iff$ sobre $\\iff$ invertible.",
                  "explicacion_md": "**Sí.** Por TMI, en el caso **cuadrado** una transformación lineal es uno a uno $\\iff$ es sobre. (No vale para $\\mathbb{R}^n \\to \\mathbb{R}^m$ con $n \\neq m$.)",
              },
          ]),

        ej(
            "Construir matrices elementales",
            "Escribe las matrices elementales $E$ ($3\\times 3$) que ejecutan: (a) $F_2 \\leftarrow F_2 + 3F_1$; (b) $F_1 \\leftrightarrow F_3$; (c) $F_2 \\leftarrow -2F_2$. Calcula además sus inversas.",
            [
                "Aplica cada OEF a $I_3$ para construir $E$.",
                "Para la inversa, aplica la OEF inversa a $I_3$.",
            ],
            (
                "**(a)** $E = \\begin{bmatrix} 1 & 0 & 0 \\\\ 3 & 1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}$, $E^{-1} = \\begin{bmatrix} 1 & 0 & 0 \\\\ -3 & 1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}$ (cambia $3 \\to -3$).\n\n"
                "**(b)** $E = \\begin{bmatrix} 0 & 0 & 1 \\\\ 0 & 1 & 0 \\\\ 1 & 0 & 0 \\end{bmatrix}$, $E^{-1} = E$ (un intercambio es su propia inversa).\n\n"
                "**(c)** $E = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & -2 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}$, $E^{-1} = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & -1/2 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}$ (recíproco del escalar)."
            ),
        ),

        ej(
            "Aplicación del TMI por columnas LI",
            "Sea $A = \\begin{bmatrix} 1 & 2 & 3 \\\\ 0 & 1 & 4 \\\\ 0 & 0 & 1 \\end{bmatrix}$. Argumenta, sin reducir, que $A$ es invertible.",
            [
                "$A$ es triangular superior con todos los pivotes en la diagonal.",
                "Aplica la versión TMI: pivote en cada columna $\\Rightarrow$ invertible.",
            ],
            (
                "$A$ es triangular superior con diagonal $(1, 1, 1)$, todas no nulas $\\Rightarrow$ tras reducir $A$ (no hace falta hacerlo) hay pivote en cada columna.\n\n"
                "Por TMI (c), $A$ es invertible. Equivalentemente, $\\det A = 1 \\cdot 1 \\cdot 1 = 1 \\neq 0$."
            ),
        ),

        ej(
            "$T$ uno a uno y sobre simultáneamente",
            "Sea $T : \\mathbb{R}^2 \\to \\mathbb{R}^2$ la rotación de $30°$ antihoraria. Su matriz estándar es $A = \\begin{bmatrix} \\cos 30° & -\\sin 30° \\\\ \\sin 30° & \\cos 30° \\end{bmatrix}$. Argumenta que $T$ es invertible y describe $T^{-1}$.",
            [
                "Calcula $\\det A$ y aplica TMI.",
                "Geométricamente, ¿qué transformación 'deshace' una rotación de $30°$?",
            ],
            (
                "$\\det A = \\cos^2 30° + \\sin^2 30° = 1 \\neq 0$ $\\Rightarrow$ por TMI, $A$ invertible $\\Rightarrow$ $T$ invertible.\n\n"
                "$T^{-1}$ es la rotación de $-30°$ (o equivalente, $330°$), con matriz $A^{-1} = \\begin{bmatrix} \\cos 30° & \\sin 30° \\\\ -\\sin 30° & \\cos 30° \\end{bmatrix}$.\n\n"
                "**Patrón general:** la inversa de la rotación por $\\varphi$ es la rotación por $-\\varphi$, y $A^{-1} = A^T$ (matriz **ortogonal**, cap. 7)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir 'matriz elemental' con 'matriz simple/pequeña'.** Una elemental es **exactamente** la $I$ con **una** OEF aplicada.",
              "**Aplicar la elemental por la derecha esperando el efecto sobre filas.** $EA$ actúa sobre **filas**; $AE$ actuaría sobre **columnas** de $A$ (con efectos análogos pero distintos).",
              "**Olvidar que el intercambio es su propia inversa.** Para reemplazo y escalamiento la inversa cambia el signo o toma recíproco; para intercambio, $E^{-1} = E$.",
              "**Aplicar TMI a matrices no cuadradas.** TMI vale **solo** para $A \\in \\mathbb{R}^{n \\times n}$.",
              "**Mezclar 'pivote en cada columna' (inyectiva) con 'pivote en cada fila' (sobreyectiva).** En el caso cuadrado coinciden, pero en general son condiciones distintas.",
              "**Buscar inversa lateral por la izquierda y por la derecha por separado.** Por TMI, basta verificar una en el caso cuadrado.",
          ]),

        b("resumen",
          puntos_md=[
              "**Matriz elemental:** $I_m$ con **una** OEF. Tres tipos: reemplazo, intercambio, escalamiento.",
              "**$EA$ = aplicar la OEF a $A$** (la OEF se aplica a las **filas**).",
              "**Toda elemental es invertible** y $E^{-1}$ es del mismo tipo con el parámetro opuesto.",
              "**Justificación del algoritmo $[A\\mid I] \\to [I \\mid A^{-1}]$:** las OEF son productos por elementales; al llegar a la izquierda al $I$, el lado derecho acumula $E_k \\cdots E_1 = A^{-1}$.",
              "**Teorema de la Matriz Invertible (TMI):** docena de propiedades equivalentes para $A \\in \\mathbb{R}^{n\\times n}$ — invertibilidad, $n$ pivotes, columnas LI, $T$ inyectiva, $T$ sobre, etc.",
              "**Caso cuadrado:** $T$ inyectiva $\\iff$ $T$ sobre $\\iff$ $T$ invertible.",
              "**Próxima lección:** **factorizaciones LU y PA = LU** — descomponer $A$ en bloques triangulares para resolver eficientemente sistemas.",
          ]),
    ]
    return {
        "id": "lec-al-3-3-matrices-elementales",
        "title": "Matrices elementales",
        "description": "Matrices elementales y OEF, justificación del algoritmo $[A\\mid I]\\to[I\\mid A^{-1}]$, Teorema de la Matriz Invertible (TMI), transformaciones lineales invertibles.",
        "blocks": blocks,
        "duration_minutes": 65,
        "order": 3,
    }


# =====================================================================
# 3.4 Factorizaciones LU y PA = LU
# =====================================================================
def lesson_3_4():
    blocks = [
        b("texto", body_md=(
            "Las **factorizaciones de matrices** son el corazón del álgebra lineal aplicada y numérica: "
            "descomponen $A$ en producto de matrices más simples (típicamente **triangulares**) que permiten "
            "resolver sistemas, calcular determinantes e inversas con muchísima mayor eficiencia.\n\n"
            "En esta lección estudiamos las dos factorizaciones más importantes:\n\n"
            "- **Factorización LU:** $A = LU$ con $L$ triangular inferior unitaria y $U$ triangular superior. "
            "Existe cuando $A$ se reduce a forma escalonada usando **solo reemplazos** (sin intercambios).\n"
            "- **Factorización PALU (o $PA = LU$):** introduce una matriz de **permutación** $P$ para reordenar "
            "filas, **siempre existe** para matrices cuadradas.\n\n"
            "Su utilidad principal: si necesitas resolver $A\\vec{x} = \\vec{b}_1, A\\vec{x} = \\vec{b}_2, \\ldots, A\\vec{x} = \\vec{b}_p$ "
            "con la **misma matriz** $A$ y muchos lados derechos, factorizar $A$ una sola vez y resolver $L\\vec{y} = \\vec{b}$, "
            "$U\\vec{x} = \\vec{y}$ es **mucho más eficiente** que recalcular Gauss-Jordan cada vez."
        )),

        b("intuicion", body_md=(
            "**Motivación práctica.** En problemas industriales reales (ingeniería estructural, simulación, "
            "machine learning), es común tener una matriz $A$ fija y muchos lados derechos $\\vec{b}_k$ distintos:\n\n"
            "- En cada instante de simulación, $A\\vec{x} = \\vec{b}_k$ con $\\vec{b}_k$ proveniente del paso anterior.\n"
            "- En métodos iterativos, se resuelven decenas o centenas de sistemas con la misma $A$.\n\n"
            "Calcular $A^{-1}$ una vez y luego $A^{-1}\\vec{b}_k$ es **costoso y numéricamente inestable**. "
            "**LU es el estándar:** factorizar $A = LU$ una vez ($O(n^3)$ operaciones) y luego resolver "
            "$L\\vec{y} = \\vec{b}_k$ y $U\\vec{x} = \\vec{y}$ ($O(n^2)$ cada uno) es **mucho más barato**."
        )),

        b("definicion",
          titulo="Factorización LU",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{m \\times n}$. Una **factorización LU** de $A$ es una expresión\n\n"
              "$$\\boxed{A = LU,}$$\n\n"
              "donde:\n\n"
              "- $L \\in \\mathbb{R}^{m \\times m}$ es **triangular inferior unitaria** (con $1$ en toda la diagonal).\n"
              "- $U \\in \\mathbb{R}^{m \\times n}$ es **triangular superior** (cualquier diagonal).\n\n"
              "**Existencia.** Una factorización LU **existe cuando $A$ se puede reducir a forma escalonada $U$ usando solo OEF de tipo reemplazo** $F_i \\leftarrow F_i + k F_j$ con $j < i$ (es decir, sin intercambios y sin escalamientos). En tal caso, $L$ acumula los multiplicadores $-k$ usados.\n\n"
              "**Si se necesitan intercambios**, no existe LU, pero sí existe **PA = LU** (sección 2 de esta lección)."
          )),

        b("ejemplo_resuelto",
          titulo="Una factorización LU dada (verificación)",
          problema_md=(
              "Verifica que $A = LU$ con $A = \\begin{bmatrix} 3 & -7 & -2 & 2 \\\\ -3 & 5 & 1 & 0 \\\\ 6 & -4 & 0 & -5 \\\\ -9 & 5 & -5 & 12 \\end{bmatrix}$, "
              "$L = \\begin{bmatrix} 1 & 0 & 0 & 0 \\\\ -1 & 1 & 0 & 0 \\\\ 2 & -5 & 1 & 0 \\\\ -3 & 8 & 3 & 1 \\end{bmatrix}$ y "
              "$U = \\begin{bmatrix} 3 & -7 & -2 & 2 \\\\ 0 & -2 & -1 & 2 \\\\ 0 & 0 & -1 & 1 \\\\ 0 & 0 & 0 & -1 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Calculamos $LU$ por la regla fila-columna. La fila $1$ de $LU$ es $(1, 0, 0, 0) \\cdot U =$ fila $1$ de $U = (3, -7, -2, 2)$ = fila $1$ de $A$ ✓."
              ),
               "justificacion_md": "En general, fila $i$ de $LU$ es $\\text{fila}_i(L) \\cdot U$ — combinación lineal de filas de $U$.",
               "es_resultado": False},
              {"accion_md": (
                  "Fila $2$ de $LU = (-1, 1, 0, 0) \\cdot U = -1 \\cdot \\text{fila}_1(U) + 1 \\cdot \\text{fila}_2(U) = (-3, 7, 2, -2) + (0, -2, -1, 2) = (-3, 5, 1, 0)$ = fila $2$ de $A$ ✓.\n\n"
                  "Las filas $3$ y $4$ se verifican análogamente."
              ),
               "justificacion_md": "**$L$ codifica las OEF**: la fila $2$ de $L$ dice 'la fila 2 de $A$ se obtiene como $-1 \\cdot$ (fila 1 de $U$) + (fila 2 de $U$)'.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Resolver $A\\vec{x} = \\vec{b}$ con LU",
          enunciado_md=(
              "Si $A = LU$, resolver $A\\vec{x} = \\vec{b}$ se reduce a **dos sistemas triangulares**:\n\n"
              "$$L\\vec{y} = \\vec{b} \\quad \\text{(sustitución hacia adelante)}$$\n\n"
              "$$U\\vec{x} = \\vec{y} \\quad \\text{(sustitución hacia atrás)}$$\n\n"
              "Cada uno cuesta $O(n^2)$ operaciones (vs. $O(n^3)$ de Gauss-Jordan completo). Ideal cuando hay muchos lados derechos."
          ),
          demostracion_md=(
              "$A\\vec{x} = (LU)\\vec{x} = L(U\\vec{x}) = \\vec{b}$. Si llamamos $\\vec{y} = U\\vec{x}$, entonces $L\\vec{y} = \\vec{b}$. Resuelto $\\vec{y}$, recuperamos $\\vec{x}$ resolviendo $U\\vec{x} = \\vec{y}$. $\\blacksquare$\n\n"
              "**Por qué los sistemas triangulares son fáciles:** $L$ tiene unos en la diagonal, así que las ecuaciones se 'desentrelazan' fila por fila desde la primera. Análogo para $U$ desde la última."
          )),

        b("ejemplo_resuelto",
          titulo="Resolver $A\\vec{x} = \\vec{b}$ usando LU",
          problema_md=(
              "Con la factorización LU del ejemplo anterior y $\\vec{b} = (-9, 5, 7, 11)^T$, resuelve $A\\vec{x} = \\vec{b}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1 — sustitución hacia adelante:** resolvemos $L\\vec{y} = \\vec{b}$.\n\n"
                  "$\\begin{cases} y_1 = -9 \\\\ -y_1 + y_2 = 5 \\Rightarrow y_2 = -4 \\\\ 2y_1 - 5y_2 + y_3 = 7 \\Rightarrow y_3 = 7 + 18 - 20 = 5 \\\\ -3y_1 + 8y_2 + 3y_3 + y_4 = 11 \\Rightarrow y_4 = 11 - 27 + 32 - 15 = 1 \\end{cases}$\n\n"
                  "$\\vec{y} = (-9, -4, 5, 1)^T$."
              ),
               "justificacion_md": "Avanzamos fila por fila usando la triangularidad inferior de $L$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2 — sustitución hacia atrás:** resolvemos $U\\vec{x} = \\vec{y}$.\n\n"
                  "$\\begin{cases} -x_4 = 1 \\Rightarrow x_4 = -1 \\\\ -x_3 + x_4 = 5 \\Rightarrow x_3 = -6 \\\\ -2x_2 - x_3 + 2x_4 = -4 \\Rightarrow -2x_2 + 6 - 2 = -4 \\Rightarrow x_2 = 4 \\\\ 3x_1 - 7x_2 - 2x_3 + 2x_4 = -9 \\Rightarrow 3x_1 - 28 + 12 - 2 = -9 \\Rightarrow x_1 = 3 \\end{cases}$\n\n"
                  "**$\\vec{x} = (3, 4, -6, -1)^T$.**"
              ),
               "justificacion_md": "Retrocedemos desde la última ecuación, usando la triangularidad superior de $U$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Algoritmo de factorización LU",
          enunciado_md=(
              "Suponiendo que $A$ se reduce a forma escalonada $U$ usando **solo reemplazos** $F_i \\leftarrow F_i + k F_j$ con $j < i$ (sin intercambios ni escalamientos):\n\n"
              "1. Reduce $A$ a $U$ con esa sucesión de OEF, registrando los multiplicadores.\n"
              "2. Construye $L$ así: $L$ es **triangular inferior unitaria** ($1$ en la diagonal), y la entrada $L_{ij}$ ($i > j$) es **$-k$** donde $k$ es el multiplicador usado en $F_i \\leftarrow F_i + k F_j$.\n"
              "3. Verifica $A = LU$.\n\n"
              "**Atajo (ojo).** Como las OEF son $F_i \\leftarrow F_i + k F_j$, la entrada $L_{ij}$ corresponde directamente al **opuesto del multiplicador** que llevó a un cero la entrada $A_{ij}$ en la columna $j$ tras el pivote."
          ),
          demostracion_md=(
              "Cada reemplazo corresponde a multiplicar por la izquierda por una matriz elemental triangular inferior unitaria $E_p$. Si $E_p \\cdots E_1 A = U$, entonces $A = (E_p \\cdots E_1)^{-1}U$. Como producto e inversa de triangulares inferiores unitarias siguen siendo triangulares inferiores unitarias, $L = (E_p \\cdots E_1)^{-1}$ tiene la forma deseada. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Encontrar la factorización LU",
          problema_md=(
              "Halla $A = LU$ para $A = \\begin{bmatrix} 2 & 4 & -1 & 5 & -2 \\\\ -4 & -5 & 3 & -8 & 1 \\\\ 2 & -5 & -4 & 1 & 8 \\\\ -6 & 0 & 7 & -3 & 1 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Reducir $A$ a $U$ con reemplazos.** Pivote en $(1,1) = 2$. Anulamos debajo:\n\n"
                  "$F_2 \\leftarrow F_2 + 2 F_1$, $F_3 \\leftarrow F_3 - F_1$, $F_4 \\leftarrow F_4 + 3 F_1$.\n\n"
                  "Multiplicadores (lo que sumamos): $+2, -1, +3$ $\\Rightarrow$ entradas correspondientes de $L$ son sus opuestos: $L_{21} = -2,\\ L_{31} = 1,\\ L_{41} = -3$.\n\n"
                  "Espera — convención: si el reemplazo es $F_i \\leftarrow F_i + k F_j$ con $k = -2$ (para anular un $-4$ usando un pivote $2$), entonces $L_{21} = -k = 2$. **Sigamos con la convención estándar: $L_{ij}$ = multiplicador que anula esa entrada al **dividir** $A_{ij}$ entre el pivote.**"
              ),
               "justificacion_md": "Convención: $L_{ij} = A_{ij}/\\text{pivote}_j$ tras los pasos previos.",
               "es_resultado": False},
              {"accion_md": (
                  "Tras la primera ronda obtenemos $\\begin{bmatrix} 2 & 4 & -1 & 5 & -2 \\\\ 0 & 3 & 1 & 2 & -3 \\\\ 0 & -9 & -3 & -4 & 10 \\\\ 0 & 12 & 4 & 12 & -5 \\end{bmatrix}$.\n\n"
                  "Pivote $3$ en $(2,2)$. Anulamos: $F_3 \\leftarrow F_3 + 3 F_2$, $F_4 \\leftarrow F_4 - 4 F_2$.\n\n"
                  "Continuando hasta el final se llega a:\n\n"
                  "$U = \\begin{bmatrix} 2 & 4 & -1 & 5 & -2 \\\\ 0 & 3 & 1 & 2 & -3 \\\\ 0 & 0 & 2 & 1 & 0 \\\\ 0 & 0 & 0 & 0 & 5 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Solo usamos reemplazos $F_i \\leftarrow F_i + kF_j$ con $j < i$ — la factorización LU existe.",
               "es_resultado": False},
              {"accion_md": (
                  "Las entradas de $L$ (multiplicadores opuestos):\n\n"
                  "$L = \\begin{bmatrix} 1 & 0 & 0 & 0 \\\\ -2 & 1 & 0 & 0 \\\\ 1 & -3 & 1 & 0 \\\\ -3 & 4 & 2 & 1 \\end{bmatrix}.$\n\n"
                  "**Verificación rápida** (fila $2$ de $LU$): $(-2, 1, 0, 0) \\cdot U = -2(2,4,-1,5,-2) + (0,3,1,2,-3) = (-4, -5, 3, -8, 1)$ = fila $2$ de $A$ ✓."
              ),
               "justificacion_md": "$L$ tiene unos en la diagonal y los multiplicadores que necesitamos para 'reconstruir' las filas de $A$ desde las de $U$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Factorización PALU ($PA = LU$)",
          body_md=(
              "Cuando la reducción de $A$ a forma escalonada **requiere intercambios de filas** (porque aparecen ceros en posiciones pivote), la factorización $A = LU$ pura **no existe**.\n\n"
              "**Solución:** introducimos una **matriz de permutación** $P$ que reordena las filas de $A$ **antes** de factorizar.\n\n"
              "**Teorema (PALU).** Sea $A \\in \\mathbb{R}^{n \\times n}$. Existen $P, L, U$ con\n\n"
              "$$\\boxed{PA = LU,}$$\n\n"
              "donde:\n\n"
              "- $P$ es una **matriz de permutación** (filas de $I_n$ reordenadas).\n"
              "- $L$ es triangular inferior **unitaria** ($1$ en la diagonal).\n"
              "- $U$ es triangular superior.\n\n"
              "**A diferencia de LU, la factorización PALU SIEMPRE existe** para cualquier matriz cuadrada.\n\n"
              "**Cómo se usa:** $A\\vec{x} = \\vec{b} \\Leftrightarrow PA\\vec{x} = P\\vec{b} \\Leftrightarrow LU\\vec{x} = P\\vec{b}$. Resolvemos $L\\vec{y} = P\\vec{b}$ y luego $U\\vec{x} = \\vec{y}$."
          )),

        b("intuicion", body_md=(
            "**Las matrices de permutación** son simplemente $I_n$ con sus filas reordenadas. Por ejemplo:\n\n"
            "$P = \\begin{bmatrix} 0 & 0 & 1 \\\\ 0 & 1 & 0 \\\\ 1 & 0 & 0 \\end{bmatrix}$\n\n"
            "intercambia las filas 1 y 3 al multiplicar $PA$. Las matrices de permutación son productos de matrices elementales de **intercambio**, así que son invertibles y satisfacen $P^{-1} = P^T$ (matrices ortogonales especiales)."
        )),

        b("ejemplo_resuelto",
          titulo="Factorización $PA = LU$",
          problema_md=(
              "Encuentra la factorización $PA = LU$ de $A = \\begin{bmatrix} 0 & 2 & 1 \\\\ 2 & 2 & 3 \\\\ 4 & -2 & 1 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1.** $A_{11} = 0$ — no podemos pivotar ahí. Para evitarlo desde el inicio, intercambiamos $F_1 \\leftrightarrow F_3$:\n\n"
                  "$P = \\begin{bmatrix} 0 & 0 & 1 \\\\ 0 & 1 & 0 \\\\ 1 & 0 & 0 \\end{bmatrix}, \\quad PA = \\begin{bmatrix} 4 & -2 & 1 \\\\ 2 & 2 & 3 \\\\ 0 & 2 & 1 \\end{bmatrix}.$"
              ),
               "justificacion_md": "$P$ registra todos los intercambios necesarios. Aquí basta uno.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2.** Aplicamos LU estándar a $PA$. Pivote $4$ en $(1,1)$. $F_2 \\leftarrow F_2 - \\tfrac{1}{2}F_1$:\n\n"
                  "$\\begin{bmatrix} 4 & -2 & 1 \\\\ 0 & 3 & 5/2 \\\\ 0 & 2 & 1 \\end{bmatrix}$, multiplicador $L_{21} = 1/2$.\n\n"
                  "Pivote $3$ en $(2,2)$. $F_3 \\leftarrow F_3 - \\tfrac{2}{3}F_2$:\n\n"
                  "$U = \\begin{bmatrix} 4 & -2 & 1 \\\\ 0 & 3 & 5/2 \\\\ 0 & 0 & -2/3 \\end{bmatrix}$, multiplicador $L_{32} = 2/3$."
              ),
               "justificacion_md": "Solo reemplazos a partir de aquí — $L$ y $U$ se construyen como en LU estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "$L = \\begin{bmatrix} 1 & 0 & 0 \\\\ 1/2 & 1 & 0 \\\\ 0 & 2/3 & 1 \\end{bmatrix}.$\n\n"
                  "**Verificación:** $LU = \\begin{bmatrix} 4 & -2 & 1 \\\\ 2 & 2 & 3 \\\\ 0 & 2 & 1 \\end{bmatrix} = PA$ ✓.\n\n"
                  "Por tanto **$PA = LU$** con $P, L, U$ encontradas."
              ),
               "justificacion_md": "La verificación es esencial: un signo equivocado en $L$ se detecta multiplicando.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "En la factorización $A = LU$, $L$ es:",
                  "opciones_md": [
                      "Triangular superior con unos en la diagonal",
                      "Triangular inferior con cualquier diagonal",
                      "**Triangular inferior unitaria** (unos en la diagonal)",
                      "Cualquier matriz invertible",
                  ],
                  "correcta": "C",
                  "pista_md": "Por convención $L$ tiene $1$ en la diagonal (acumula multiplicadores de Gauss).",
                  "explicacion_md": "**$L$ es triangular inferior unitaria.** $U$ es triangular superior con cualquier diagonal (los pivotes).",
              },
              {
                  "enunciado_md": "Resolver $A\\vec{x} = \\vec{b}$ con $A = LU$ se hace:",
                  "opciones_md": [
                      "Calculando $A^{-1}\\vec{b}$",
                      "Resolviendo $L\\vec{y} = \\vec{b}$ y luego $U\\vec{x} = \\vec{y}$",
                      "Resolviendo $U\\vec{y} = \\vec{b}$ y luego $L\\vec{x} = \\vec{y}$",
                      "Multiplicando $LU\\vec{b}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Sustituyamos $A = LU$ en $A\\vec{x} = \\vec{b}$ y agrupemos.",
                  "explicacion_md": "**$L\\vec{y} = \\vec{b}$ (adelante), luego $U\\vec{x} = \\vec{y}$ (atrás).** Cada uno es $O(n^2)$ por ser triangular.",
              },
              {
                  "enunciado_md": "La factorización $PA = LU$:",
                  "opciones_md": [
                      "Existe solo si $A$ es invertible",
                      "Existe siempre para matrices cuadradas",
                      "Existe solo si $A$ es triangular",
                      "Existe solo si $A$ no requiere intercambios",
                  ],
                  "correcta": "B",
                  "pista_md": "$P$ se introduce justamente para manejar los intercambios necesarios.",
                  "explicacion_md": "**Siempre existe.** $P$ permite reordenar filas para garantizar pivotes no nulos en cada paso.",
              },
          ]),

        ej(
            "Factorización LU básica",
            "Halla la factorización LU de $A = \\begin{bmatrix} 2 & 4 & -2 \\\\ 1 & 5 & -2 \\\\ 4 & -1 & 9 \\end{bmatrix}$.",
            [
                "Reduce a $U$ usando solo reemplazos.",
                "Anota los multiplicadores: $L_{21} = 1/2$, $L_{31} = 2$, etc.",
            ],
            (
                "Reducción: $F_2 \\leftarrow F_2 - \\tfrac{1}{2}F_1$ ($L_{21} = 1/2$); $F_3 \\leftarrow F_3 - 2F_1$ ($L_{31} = 2$):\n\n"
                "$\\begin{bmatrix} 2 & 4 & -2 \\\\ 0 & 3 & -1 \\\\ 0 & -9 & 13 \\end{bmatrix}$.\n\n"
                "$F_3 \\leftarrow F_3 + 3F_2$ ($L_{32} = -3$): $U = \\begin{bmatrix} 2 & 4 & -2 \\\\ 0 & 3 & -1 \\\\ 0 & 0 & 10 \\end{bmatrix}$.\n\n"
                "$L = \\begin{bmatrix} 1 & 0 & 0 \\\\ 1/2 & 1 & 0 \\\\ 2 & -3 & 1 \\end{bmatrix}$.\n\n"
                "**Verificación:** $LU = A$ ✓ (calcular fila a fila)."
            ),
        ),

        ej(
            "Resolver $A\\vec{x} = \\vec{b}$ con LU",
            "Usa la factorización del ejercicio anterior para resolver $A\\vec{x} = (2, 0, 1)^T$.",
            [
                "Resuelve $L\\vec{y} = \\vec{b}$ por sustitución hacia adelante.",
                "Resuelve $U\\vec{x} = \\vec{y}$ por sustitución hacia atrás.",
            ],
            (
                "**$L\\vec{y} = \\vec{b}$:** $y_1 = 2$, $\\tfrac{1}{2}y_1 + y_2 = 0 \\Rightarrow y_2 = -1$, $2y_1 - 3y_2 + y_3 = 1 \\Rightarrow y_3 = 1 - 4 - 3 = -6$.\n\n"
                "**$U\\vec{x} = \\vec{y}$:** $10 x_3 = -6 \\Rightarrow x_3 = -3/5$. $3x_2 - x_3 = -1 \\Rightarrow x_2 = -8/15$. $2x_1 + 4x_2 - 2x_3 = 2 \\Rightarrow x_1 = (2 + 32/15 - 6/5)/2 = 26/15 \\cdot 1/2$. Calculando con cuidado: $x_1 = 13/15$.\n\n"
                "$\\vec{x} = (13/15,\\ -8/15,\\ -3/5)^T$."
            ),
        ),

        ej(
            "Cuándo se necesita PALU",
            "Explica por qué la matriz $A = \\begin{bmatrix} 0 & 1 \\\\ 1 & 0 \\end{bmatrix}$ no admite factorización LU pura, pero sí $PA = LU$.",
            [
                "$A_{11} = 0$ impide el primer pivote.",
                "Aplica $P$ que intercambie las dos filas y verifica.",
            ],
            (
                "$A_{11} = 0$, así que para reducir $A$ debemos intercambiar $F_1 \\leftrightarrow F_2$, lo cual no es un reemplazo $\\Rightarrow$ **LU pura no existe**.\n\n"
                "Con $P = \\begin{bmatrix} 0 & 1 \\\\ 1 & 0 \\end{bmatrix}$: $PA = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} = I$.\n\n"
                "Trivialmente $PA = I = I \\cdot I$, así que $L = U = I$. **PALU existe** (y es la identidad)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $L$ y $U$.** $L$ = lower (triangular inferior, unitaria). $U$ = upper (triangular superior).",
              "**Olvidar el signo de los multiplicadores en $L$.** Si la OEF es $F_i \\leftarrow F_i - k F_j$, entonces $L_{ij} = k$ (positivo).",
              "**Intentar LU sin verificar que se evitan intercambios.** Si requieres intercambiar filas, usa PALU.",
              "**Resolver $U\\vec{y} = \\vec{b}$ primero.** El orden correcto es $L\\vec{y} = \\vec{b}$ (adelante), luego $U\\vec{x} = \\vec{y}$ (atrás).",
              "**Pensar que LU es más rápido que Gauss-Jordan para un solo sistema.** El beneficio aparece con **muchos lados derechos**: factorizar una vez y resolver muchas.",
              "**Olvidar aplicar $P$ a $\\vec{b}$ en PALU.** Resolver $L\\vec{y} = P\\vec{b}$ (no $L\\vec{y} = \\vec{b}$).",
          ]),

        b("resumen",
          puntos_md=[
              "**LU:** $A = LU$ con $L$ triangular inferior unitaria y $U$ triangular superior. Existe si $A$ se reduce con solo reemplazos.",
              "**Algoritmo:** reduce $A$ a $U$ y anota multiplicadores en $L$.",
              "**Resolver:** $L\\vec{y} = \\vec{b}$ (adelante), luego $U\\vec{x} = \\vec{y}$ (atrás). Cada paso $O(n^2)$.",
              "**Beneficio:** factorizar $A$ una vez ($O(n^3)$), resolver muchos $\\vec{b}$ a $O(n^2)$ cada uno.",
              "**PALU:** $PA = LU$ con $P$ matriz de permutación. **Siempre existe** para cualquier $A$ cuadrada.",
              "**Cierre del capítulo:** Hemos pasado del producto matricial a la inversa, las matrices elementales y las factorizaciones — un kit completo para el álgebra lineal computacional.",
              "**Próximo capítulo:** **Determinantes** — generalización a $\\mathbb{R}^n$ del 'área' / 'volumen', con consecuencias para invertibilidad y sistemas.",
          ]),
    ]
    return {
        "id": "lec-al-3-4-factorizaciones",
        "title": "Factorizaciones",
        "description": "Factorización LU con $L$ triangular inferior unitaria y $U$ triangular superior; resolución eficiente de $L\\vec{y}=\\vec{b}, U\\vec{x}=\\vec{y}$; factorización PALU para casos generales.",
        "blocks": blocks,
        "duration_minutes": 60,
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

    chapter_id = "ch-al-algebra-matrices"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Álgebra de Matrices",
        "description": (
            "Suma, producto, transpuesta y potencias de matrices; matriz inversa "
            "(fórmula $2\\times 2$ y algoritmo Gauss–Jordan); matrices elementales "
            "y Teorema de la Matriz Invertible; factorizaciones LU y PALU."
        ),
        "order": 3,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_3_1, lesson_3_2, lesson_3_3, lesson_3_4]
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
        f"✅ Capítulo 3 — Álgebra de Matrices listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
