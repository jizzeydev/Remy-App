"""
Seed del curso Álgebra Lineal — Capítulo 4: Determinantes.
3 lecciones:
  4.1 Determinante (definición por cofactores)
  4.2 Propiedades del determinante (OEF, multiplicatividad, transpuesta)
  4.3 Aplicaciones (Cramer, fórmula adjunta, área/volumen)

Basado en los Apuntes/Clase de Se Remonta para cada lección.
Estructura: del cálculo por cofactores al manejo eficiente vía OEF y
triangulación, hasta las aplicaciones (Cramer, $A^{-1} = \\tfrac{1}{\\det A}\\text{adj}\\,A$,
e interpretación geométrica como factor de área/volumen).

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
# 4.1 Determinante
# =====================================================================
def lesson_4_1():
    blocks = [
        b("texto", body_md=(
            "El **determinante** es un número real asociado a cada matriz **cuadrada** que "
            "condensa muchísima información sobre ella en un solo escalar. En esta lección "
            "lo definimos vía **menores y cofactores** (definición recursiva), aprendemos a "
            "calcularlo expandiendo por una fila o columna, y vemos por qué para matrices "
            "**triangulares** $\\det(A)$ es simplemente el producto de la diagonal.\n\n"
            "**¿Qué nos dice $\\det A$?**\n\n"
            "- **$\\det A \\neq 0 \\iff A$ es invertible** (TMI extendido, lección 3.3).\n"
            "- **$|\\det A|$ = factor de cambio de área/volumen** bajo $T(\\vec{x}) = A\\vec{x}$ (lección 4.3).\n"
            "- **Signo de $\\det A$:** detecta si $T$ preserva ($+$) o invierte ($-$) la orientación.\n\n"
            "Al terminar, debes poder:\n\n"
            "- Definir **menor $A_{ij}$** y **cofactor $C_{ij} = (-1)^{i+j}\\det(A_{ij})$**.\n"
            "- Calcular $\\det A$ por **expansión por cofactores** a lo largo de cualquier fila o columna.\n"
            "- Reconocer el patrón de signos $\\begin{bmatrix} + & - & + \\\\ - & + & - \\\\ + & - & + \\end{bmatrix}$.\n"
            "- Aplicar el **atajo**: si $A$ es triangular, $\\det A = \\prod_i a_{ii}$."
        )),

        b("definicion",
          titulo="Determinante de matrices $1\\times 1$ y $2\\times 2$",
          body_md=(
              "**Casos base** (definición directa):\n\n"
              "$$\\det[a] = a, \\qquad \\det \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} = ad - bc.$$\n\n"
              "El determinante $2\\times 2$ ya apareció en el cap. 3 como **discriminante de invertibilidad**: $A$ invertible $\\iff ad - bc \\neq 0$. La fórmula $A^{-1} = \\tfrac{1}{ad-bc}\\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix}$ confirma que el determinante aparece en el denominador.\n\n"
              "**Notación equivalente:** $|A|$ con barras verticales en vez de corchetes:\n\n"
              "$$\\begin{vmatrix} a & b \\\\ c & d \\end{vmatrix} = ad - bc.$$"
          )),

        b("definicion",
          titulo="Menor, cofactor y patrón de signos",
          body_md=(
              "Sea $A = [a_{ij}] \\in \\mathbb{R}^{n \\times n}$ (con $n \\geq 2$).\n\n"
              "**Menor $A_{ij}$:** la submatriz $(n-1) \\times (n-1)$ que se obtiene **eliminando la fila $i$ y la columna $j$** de $A$.\n\n"
              "**Cofactor $C_{ij}$:** el escalar\n\n"
              "$$\\boxed{C_{ij} = (-1)^{i+j} \\det(A_{ij}).}$$\n\n"
              "**Patrón de signos** $(-1)^{i+j}$, en forma de tablero:\n\n"
              "$$\\begin{bmatrix} + & - & + & - & \\cdots \\\\ - & + & - & + & \\cdots \\\\ + & - & + & - & \\cdots \\\\ \\vdots & & & & \\ddots \\end{bmatrix}.$$\n\n"
              "Empieza con $+$ en la posición $(1,1)$ y alterna en filas y columnas."
          )),

        b("teorema",
          nombre="Definición por desarrollo por cofactores (recursiva)",
          enunciado_md=(
              "Para $A \\in \\mathbb{R}^{n \\times n}$ con $n \\geq 2$, el determinante **se calcula por expansión a lo largo de cualquier fila o columna**:\n\n"
              "**Por la fila $i$:** $\\det(A) = a_{i1}C_{i1} + a_{i2}C_{i2} + \\cdots + a_{in}C_{in}.$\n\n"
              "**Por la columna $j$:** $\\det(A) = a_{1j}C_{1j} + a_{2j}C_{2j} + \\cdots + a_{nj}C_{nj}.$\n\n"
              "Las distintas elecciones de fila/columna dan **el mismo valor** (independencia del desarrollo).\n\n"
              "**Estrategia práctica:** elige la fila o columna **con más ceros** — los términos con $a_{ij} = 0$ no aportan, ahorrando trabajo."
          ),
          demostracion_md=(
              "La equivalencia entre los distintos desarrollos se prueba por inducción en $n$, mostrando que el desarrollo por la fila $1$ y por la columna $1$ producen el mismo número, y que reorganizar las sumas usando el patrón de signos preserva el valor. Demostración técnica que omitimos. $\\blacksquare$\n\n"
              "**Convención común:** la 'definición' suele dar como expansión por la primera fila:\n\n"
              "$\\det A = \\sum_{j=1}^n (-1)^{1+j} a_{1j}\\,\\det(A_{1j}).$"
          )),

        b("ejemplo_resuelto",
          titulo="Cálculo por expansión (fila $1$)",
          problema_md=(
              "Calcular $\\det A$ para $A = \\begin{bmatrix} 1 & 5 & 0 \\\\ 2 & 4 & -1 \\\\ 0 & -2 & 0 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Expandimos por la **fila $1$**: $\\det A = 1\\cdot C_{11} + 5\\cdot C_{12} + 0 \\cdot C_{13}$.\n\n"
                  "$C_{11} = (+1) \\det\\begin{bmatrix} 4 & -1 \\\\ -2 & 0 \\end{bmatrix} = 4\\cdot 0 - (-1)(-2) = -2.$\n\n"
                  "$C_{12} = (-1) \\det\\begin{bmatrix} 2 & -1 \\\\ 0 & 0 \\end{bmatrix} = -(2\\cdot 0 - (-1)\\cdot 0) = 0.$"
              ),
               "justificacion_md": "El término con $a_{13} = 0$ no se calcula — ahorro automático.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\det A = 1\\cdot(-2) + 5\\cdot 0 + 0 = -2.$"
              ),
               "justificacion_md": "Resultado directo de la expansión.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Misma matriz, expansión por la fila $3$ (más ceros)",
          problema_md=(
              "Verificar $\\det A = -2$ usando ahora la **fila $3$** de $A = \\begin{bmatrix} 1 & 5 & 0 \\\\ 2 & 4 & -1 \\\\ 0 & -2 & 0 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "La fila $3$ es $(0, -2, 0)$ — solo el término del medio aporta:\n\n"
                  "$\\det A = 0\\cdot C_{31} + (-2) \\cdot C_{32} + 0\\cdot C_{33} = -2\\,C_{32}.$"
              ),
               "justificacion_md": "**Patrón:** elegir la fila/columna con más ceros reduce el trabajo a 1 cofactor.",
               "es_resultado": False},
              {"accion_md": (
                  "$A_{32} = \\begin{bmatrix} 1 & 0 \\\\ 2 & -1 \\end{bmatrix}$ (eliminar fila $3$ y columna $2$). $\\det(A_{32}) = 1(-1) - 0\\cdot 2 = -1.$\n\n"
                  "$C_{32} = (-1)^{3+2}\\det(A_{32}) = (-1)\\cdot(-1) = 1.$"
              ),
               "justificacion_md": "El factor $(-1)^{3+2} = (-1)^5 = -1$ por el patrón de signos.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\det A = -2 \\cdot 1 = -2$ ✓ — coincide con el cálculo por la fila $1$."
              ),
               "justificacion_md": "Confirmamos la independencia del desarrollo.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Cuándo conviene expandir por cada fila/columna:**\n\n"
            "- **Por la fila/columna con más ceros.** Cada $a_{ij} = 0$ **anula su término** $\\Rightarrow$ no calculamos su cofactor.\n"
            "- **Por la primera fila** si la matriz es 'genérica' (sin patrones especiales) — convención clásica.\n"
            "- **Por una columna** si una columna es notablemente más simple que cualquier fila.\n\n"
            "Aprovechar esta libertad reduce drásticamente el cómputo manual. Las diferencias de eficiencia entre opciones pueden ser 10× o más."
        )),

        b("teorema",
          nombre="Determinante de una matriz triangular",
          enunciado_md=(
              "Si $A \\in \\mathbb{R}^{n \\times n}$ es **triangular** (superior o inferior), entonces\n\n"
              "$$\\boxed{\\det(A) = \\prod_{i=1}^n a_{ii} = a_{11}\\,a_{22}\\cdots a_{nn},}$$\n\n"
              "es decir, el determinante es el **producto de las entradas de la diagonal principal**.\n\n"
              "**Casos especiales:** $\\det(I_n) = 1$ (todos los unos en la diagonal). $\\det(\\text{diag}(d_1, \\ldots, d_n)) = d_1 \\cdots d_n$."
          ),
          demostracion_md=(
              "Por inducción en $n$. Para $n = 1$, $\\det[a_{11}] = a_{11}$. Para $n > 1$, expandimos por la **primera columna** de una triangular **superior**: solo $a_{11}$ es no nulo en esa columna, así\n\n"
              "$\\det A = a_{11}\\,C_{11} = a_{11}\\,\\det(A_{11}).$\n\n"
              "$A_{11}$ es la submatriz $(n-1)\\times (n-1)$ obtenida eliminando fila $1$ y columna $1$, **también triangular superior**. Por inducción, $\\det(A_{11}) = a_{22}\\cdots a_{nn}$, luego $\\det A = a_{11}\\cdots a_{nn}$. Para triangulares inferiores, expandimos por la primera **fila**. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Determinante de una triangular",
          problema_md=(
              "Calcular $\\det A$ con $A = \\begin{bmatrix} 3 & 7 & -2 & 5 \\\\ 0 & -1 & 4 & 0 \\\\ 0 & 0 & 2 & 8 \\\\ 0 & 0 & 0 & -4 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A$ es **triangular superior** (todos los ceros estrictamente debajo de la diagonal). La diagonal es $(3, -1, 2, -4)$."
              ),
               "justificacion_md": "Identificar la estructura **antes** de calcular ahorra todo el trabajo de expansión.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\det A = 3 \\cdot (-1) \\cdot 2 \\cdot (-4) = 24.$"
              ),
               "justificacion_md": "Producto de la diagonal, sin un solo cofactor calculado.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Expansión $4\\times 4$ aprovechando ceros",
          problema_md=(
              "Calcular $\\det A$ con $A = \\begin{bmatrix} 0 & 1 & 2 & -1 \\\\ 3 & 0 & 0 & 0 \\\\ 1 & -2 & 4 & 5 \\\\ 0 & 1 & 0 & 3 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "La **fila $2$** tiene tres ceros — elegimos esa para expandir:\n\n"
                  "$\\det A = 3\\cdot C_{21} + 0 + 0 + 0 = 3\\,C_{21}.$\n\n"
                  "$C_{21} = (-1)^{2+1}\\det(A_{21}) = -\\det(A_{21})$ donde $A_{21} = \\begin{bmatrix} 1 & 2 & -1 \\\\ -2 & 4 & 5 \\\\ 1 & 0 & 3 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Eliminamos fila $2$ y columna $1$ para formar $A_{21}$.",
               "es_resultado": False},
              {"accion_md": (
                  "Calculamos $\\det(A_{21})$ expandiendo por la **fila $3$** (que tiene un cero):\n\n"
                  "$\\det(A_{21}) = 1\\cdot \\det\\begin{bmatrix} 2 & -1 \\\\ 4 & 5 \\end{bmatrix} - 0 + 3\\cdot \\det\\begin{bmatrix} 1 & 2 \\\\ -2 & 4 \\end{bmatrix}$\n\n"
                  "$= 1(10 + 4) + 3(4 + 4) = 14 + 24 = 38.$"
              ),
               "justificacion_md": "Cofactores con sus signos $(-1)^{3+1} = +$ y $(-1)^{3+3} = +$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\det A = 3 \\cdot (-1) \\cdot 38 = -114.$"
              ),
               "justificacion_md": "**Lección:** dos niveles de expansión bien elegidos son mucho más rápidos que un cálculo 'por la fuerza' por la primera fila.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El cofactor $C_{32}$ de una matriz $4\\times 4$ tiene signo:",
                  "opciones_md": ["$+$", "$-$", "Depende de la matriz", "$0$"],
                  "correcta": "B",
                  "pista_md": "$(-1)^{i+j}$ con $i=3, j=2$.",
                  "explicacion_md": "$(-1)^{3+2} = (-1)^5 = -1$ $\\Rightarrow$ signo **$-$**. El cofactor es $C_{32} = -\\det(A_{32})$.",
              },
              {
                  "enunciado_md": "Para una matriz triangular $5\\times 5$ con diagonal $(2, -3, 1, 4, -1)$, $\\det A$ vale:",
                  "opciones_md": ["$3$", "$24$", "$-24$", "$0$"],
                  "correcta": "B",
                  "pista_md": "Producto de la diagonal — cuenta con cuidado los signos.",
                  "explicacion_md": "$\\det A = 2 \\cdot (-3) \\cdot 1 \\cdot 4 \\cdot (-1)$. Calculando paso a paso: $2 \\cdot (-3) = -6$, $-6 \\cdot 1 = -6$, $-6 \\cdot 4 = -24$, $-24 \\cdot (-1) = 24$. **Dos signos negativos se cancelan** $\\Rightarrow$ $\\det A = 24$.",
              },
              {
                  "enunciado_md": "Expandiendo por una fila con todos sus elementos cero:",
                  "opciones_md": [
                      "$\\det A = 1$",
                      "$\\det A = 0$",
                      "$\\det A$ no está definido",
                      "Hay que elegir otra fila",
                  ],
                  "correcta": "B",
                  "pista_md": "Cada término es $a_{ij}\\,C_{ij}$. Si todos los $a_{ij}$ son $0$...",
                  "explicacion_md": "**$\\det A = 0$.** Cada término del desarrollo es $0 \\cdot C_{ij} = 0$. Por extensión: si $A$ tiene una fila (o columna) **completamente nula**, su determinante es cero.",
              },
          ]),

        ej(
            "Determinante $3\\times 3$ con expansión",
            "Calcula $\\det A$ para $A = \\begin{bmatrix} 2 & 1 & 3 \\\\ 1 & -1 & 1 \\\\ 1 & 4 & -2 \\end{bmatrix}$.",
            [
                "Expande por la primera fila o por una columna con más ceros (aquí no hay ceros, pero la fila $2$ tiene entradas pequeñas).",
                "Cuida los signos del patrón.",
            ],
            (
                "Expandimos por la **fila $1$**:\n\n"
                "$\\det A = 2\\det\\begin{bmatrix} -1 & 1 \\\\ 4 & -2 \\end{bmatrix} - 1\\det\\begin{bmatrix} 1 & 1 \\\\ 1 & -2 \\end{bmatrix} + 3\\det\\begin{bmatrix} 1 & -1 \\\\ 1 & 4 \\end{bmatrix}$\n\n"
                "$= 2(2 - 4) - 1(-2 - 1) + 3(4 + 1) = 2(-2) - (-3) + 3(5) = -4 + 3 + 15 = 14$."
            ),
        ),

        ej(
            "Determinante de matriz triangular grande",
            "Calcula $\\det A$ para $A = \\begin{bmatrix} 5 & 2 & 0 & 1 & 7 \\\\ 0 & -3 & 4 & 6 & 0 \\\\ 0 & 0 & 2 & 1 & 9 \\\\ 0 & 0 & 0 & 1 & 8 \\\\ 0 & 0 & 0 & 0 & -2 \\end{bmatrix}$.",
            [
                "Identifica la estructura antes de calcular.",
                "Aplica el atajo de triangular.",
            ],
            (
                "$A$ es **triangular superior** $\\Rightarrow$ $\\det A = $ producto de la diagonal $= 5 \\cdot (-3) \\cdot 2 \\cdot 1 \\cdot (-2) = 60$."
            ),
        ),

        ej(
            "Eligiendo la mejor fila/columna",
            "Calcula $\\det A$ para $A = \\begin{bmatrix} 4 & 0 & 7 & 0 \\\\ 3 & 0 & -1 & 0 \\\\ 1 & 2 & 5 & 6 \\\\ 8 & 0 & 9 & 0 \\end{bmatrix}$.",
            [
                "Mira la columna $2$ y la columna $4$: ambas tienen tres ceros.",
                "Expande por una de ellas.",
            ],
            (
                "Expandimos por la **columna $2$**: solo el término $a_{32} = 2$ aporta.\n\n"
                "$\\det A = 2\\,C_{32} = 2\\,(-1)^{3+2}\\det(A_{32}) = -2\\det\\begin{bmatrix} 4 & 7 & 0 \\\\ 3 & -1 & 0 \\\\ 8 & 9 & 0 \\end{bmatrix} = -2 \\cdot 0 = 0$.\n\n"
                "**$\\det A = 0$** — la columna $4$ de $A$ es nula, lo que ya garantizaba este resultado."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el signo $(-1)^{i+j}$ en el cofactor.** $C_{ij}$ no es solo $\\det(A_{ij})$, lleva el signo del patrón.",
              "**Confundir menor con cofactor.** El menor es la **submatriz**; el cofactor es **un escalar** (con su signo).",
              "**Aplicar la fórmula $ad - bc$ a matrices más grandes.** Solo vale para $2\\times 2$.",
              "**Olvidar que solo aplica a matrices cuadradas.** $\\det A$ no está definido para $A$ rectangular.",
              "**No aprovechar la libertad de elegir fila/columna.** Expandir por una fila sin ceros cuando hay otra con tres ceros es ineficiente.",
              "**Confundir el atajo triangular con cualquier matriz.** Solo si **todos** los ceros están de un lado de la diagonal.",
              "**Calcular cofactores de entradas nulas.** Si $a_{ij} = 0$, no necesitas calcular $C_{ij}$ — el término se anula.",
          ]),

        b("resumen",
          puntos_md=[
              "**Determinante:** número real asociado a una matriz **cuadrada**, denotado $\\det A$ o $|A|$.",
              "**Casos base:** $\\det[a] = a$ y $\\det\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} = ad - bc$.",
              "**Menor $A_{ij}$:** submatriz $(n-1)\\times(n-1)$ al eliminar fila $i$ y columna $j$.",
              "**Cofactor:** $C_{ij} = (-1)^{i+j}\\det(A_{ij})$ — patrón alternado de signos en tablero.",
              "**Expansión por cofactores:** $\\det A = \\sum_j a_{ij}C_{ij}$ (por fila $i$) o $\\sum_i a_{ij}C_{ij}$ (por columna $j$). **Cualquier fila/columna sirve.**",
              "**Atajo triangular:** $A$ triangular $\\Rightarrow$ $\\det A = \\prod_i a_{ii}$.",
              "**Estrategia:** expandir por la fila/columna con más ceros.",
              "**Próxima lección:** propiedades del determinante (efecto de OEF, multiplicatividad).",
          ]),
    ]
    return {
        "id": "lec-al-4-1-determinante",
        "title": "Determinante",
        "description": "Definición por menores y cofactores, expansión por cualquier fila/columna, patrón de signos $(-1)^{i+j}$, fórmula para matrices triangulares.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 1,
    }


# =====================================================================
# 4.2 Propiedades del determinante
# =====================================================================
def lesson_4_2():
    blocks = [
        b("texto", body_md=(
            "Calcular un determinante por **expansión directa** se vuelve impracticable rápidamente: "
            "una matriz $5\\times 5$ requiere expandir y luego cinco $4\\times 4$, cada una con cuatro "
            "$3\\times 3$, etc. La buena noticia es que el determinante tiene **propiedades** que permiten "
            "calcularlo de manera muchísimo más eficiente.\n\n"
            "El truco esencial es **combinar reducción por filas (OEF) con la fórmula triangular**: "
            "llevamos $A$ a forma triangular superior $U$ controlando cómo cada OEF afecta al "
            "determinante, y entonces $\\det A$ se calcula como producto de la diagonal de $U$ ajustado "
            "por los factores acumulados.\n\n"
            "Al terminar, debes poder:\n\n"
            "- Aplicar las **3 reglas de OEF sobre $\\det$**: reemplazo no cambia, intercambio cambia signo, escalamiento multiplica.\n"
            "- Usar $\\det(A^T) = \\det(A)$ para mover entre filas y columnas según convenga.\n"
            "- Aplicar la **propiedad multiplicativa** $\\det(AB) = \\det(A)\\det(B)$ y sus consecuencias.\n"
            "- Combinar todo en un **algoritmo eficiente** para determinantes $n\\times n$."
        )),

        b("teorema",
          nombre="Efecto de las OEF sobre $\\det$",
          enunciado_md=(
              "Sea $A$ una matriz cuadrada y $B$ la matriz que resulta tras aplicar **una** OEF:\n\n"
              "**(a) Reemplazo:** si $B$ se obtiene de $A$ por $F_i \\leftarrow F_i + k F_j$ (con $i \\neq j$), entonces $\\det B = \\det A$ — **no cambia**.\n\n"
              "**(b) Intercambio:** si $B$ se obtiene de $A$ permutando dos filas, entonces $\\det B = -\\det A$ — **cambia el signo**.\n\n"
              "**(c) Escalamiento:** si $B$ se obtiene de $A$ multiplicando una fila por $k$ ($k \\neq 0$), entonces $\\det B = k\\,\\det A$ — **se multiplica por $k$**."
          ),
          demostracion_md=(
              "Cada OEF corresponde a multiplicar por la izquierda por una matriz **elemental** $E$. Por la propiedad multiplicativa (más adelante), $\\det B = \\det(EA) = \\det(E)\\det(A)$. Calculamos $\\det E$ para cada tipo:\n\n"
              "(a) $E$ tiene la diagonal $1$ y un $k$ fuera $\\Rightarrow$ es triangular con $\\det E = 1$.\n\n"
              "(b) $E$ es $I$ con dos filas permutadas $\\Rightarrow$ $\\det E = -1$.\n\n"
              "(c) $E$ es $I$ con una entrada de la diagonal $= k$ $\\Rightarrow$ $\\det E = k$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Triangulación con control de signos",
          problema_md=(
              "Calcular $\\det A$ para $A = \\begin{bmatrix} 1 & -4 & 2 \\\\ -2 & 8 & -9 \\\\ -1 & 7 & 0 \\end{bmatrix}$ vía OEF."
          ),
          pasos=[
              {"accion_md": (
                  "Aplicamos **reemplazos** (no alteran $\\det$): $F_2 \\leftarrow F_2 + 2 F_1$ y $F_3 \\leftarrow F_3 + F_1$:\n\n"
                  "$\\begin{bmatrix} 1 & -4 & 2 \\\\ 0 & 0 & -5 \\\\ 0 & 3 & 2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Anulamos debajo del primer pivote sin cambiar el determinante.",
               "es_resultado": False},
              {"accion_md": (
                  "El pivote $(2,2)$ es $0$ — necesitamos un **intercambio** $F_2 \\leftrightarrow F_3$ (cambia el signo):\n\n"
                  "$\\det A = -\\det\\begin{bmatrix} 1 & -4 & 2 \\\\ 0 & 3 & 2 \\\\ 0 & 0 & -5 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Llevamos un valor no nulo a la posición pivote.",
               "es_resultado": False},
              {"accion_md": (
                  "La matriz dentro es triangular superior $\\Rightarrow$ $\\det = 1\\cdot 3\\cdot (-5) = -15$.\n\n"
                  "**$\\det A = -(-15) = 15.$**"
              ),
               "justificacion_md": "**Lección clave:** combinar reemplazos (gratis) con un intercambio o dos puede triangulizar y resolver casi cualquier $\\det$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Determinante $4\\times 4$ con factor común",
          problema_md=(
              "Calcular $\\det A$ con $A = \\begin{bmatrix} 2 & -8 & 6 & 8 \\\\ 3 & -9 & 5 & 10 \\\\ -3 & 0 & 1 & -2 \\\\ 1 & -4 & 0 & 6 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Extraemos el factor $2$ de la fila $1$** (escala $\\Rightarrow$ multiplicamos $\\det$ por $1/2$ luego compensamos):\n\n"
                  "$\\det A = 2 \\cdot \\det\\begin{bmatrix} 1 & -4 & 3 & 4 \\\\ 3 & -9 & 5 & 10 \\\\ -3 & 0 & 1 & -2 \\\\ 1 & -4 & 0 & 6 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Sacar factor común de una fila multiplica el determinante por ese factor — útil cuando todas las entradas son múltiplos.",
               "es_resultado": False},
              {"accion_md": (
                  "Reemplazos $F_2 \\leftarrow F_2 - 3F_1$, $F_3 \\leftarrow F_3 + 3F_1$, $F_4 \\leftarrow F_4 - F_1$:\n\n"
                  "$\\det A = 2 \\cdot \\det\\begin{bmatrix} 1 & -4 & 3 & 4 \\\\ 0 & 3 & -4 & -2 \\\\ 0 & -12 & 10 & 10 \\\\ 0 & 0 & -3 & 2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Reemplazos no alteran $\\det$.",
               "es_resultado": False},
              {"accion_md": (
                  "$F_3 \\leftarrow F_3 + 4 F_2$, luego $F_4 \\leftarrow F_4 - \\tfrac{1}{2}F_3$:\n\n"
                  "$\\det A = 2 \\cdot \\det\\begin{bmatrix} 1 & -4 & 3 & 4 \\\\ 0 & 3 & -4 & -2 \\\\ 0 & 0 & -6 & 2 \\\\ 0 & 0 & 0 & 1 \\end{bmatrix} = 2 \\cdot (1 \\cdot 3 \\cdot (-6) \\cdot 1) = 2 \\cdot (-18) = -36.$"
              ),
               "justificacion_md": "Triangulamos completamente y aplicamos el atajo triangular.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Determinante de la transpuesta.** Para toda matriz cuadrada,\n\n"
              "$$\\boxed{\\det(A^T) = \\det(A).}$$"
          ),
          demostracion_md=(
              "Por inducción en $n$ usando el desarrollo por cofactores: al transponer, el cofactor $C_{ij}$ pasa a la posición $(j, i)$, y el patrón de signos $(-1)^{i+j}$ es **simétrico** ($i$ y $j$ juegan el mismo papel). Por tanto el desarrollo por una fila de $A$ coincide con el desarrollo por la columna correspondiente de $A^T$. $\\blacksquare$\n\n"
              "**Consecuencia muy útil:** **todas las propiedades para filas tienen análogas para columnas.** Las **OEC** (operaciones elementales de columna) afectan al determinante exactamente igual que las OEF correspondientes."
          )),

        b("definicion",
          titulo="Operaciones elementales de columna (OEC)",
          body_md=(
              "Análogo a las OEF, pero sobre columnas:\n\n"
              "- **Reemplazo:** $C_j \\leftarrow C_j + k C_i$ ($i \\neq j$) — **no cambia** $\\det$.\n"
              "- **Intercambio:** $C_i \\leftrightarrow C_j$ — **cambia el signo** de $\\det$.\n"
              "- **Escalamiento:** $C_j \\leftarrow k C_j$ — **multiplica** $\\det$ por $k$.\n\n"
              "Al multiplicar por la **derecha** por una matriz elemental, las OEC actúan sobre las columnas.\n\n"
              "**Estrategia mixta:** combinar OEF y OEC en un mismo cálculo, eligiendo siempre la operación más conveniente."
          )),

        b("ejemplo_resuelto",
          titulo="Cálculo con OEC",
          problema_md=(
              "Calcular $\\det A$ con $A = \\begin{bmatrix} 1 & 2 & -1 \\\\ 3 & 0 & 5 \\\\ 2 & 1 & 4 \\end{bmatrix}$ usando operaciones de columna."
          ),
          pasos=[
              {"accion_md": (
                  "Aplicamos $C_2 \\leftarrow C_2 - 2 C_1$ y $C_3 \\leftarrow C_3 + C_1$ (ambas reemplazos $\\Rightarrow$ no alteran $\\det$):\n\n"
                  "$\\begin{bmatrix} 1 & 0 & 0 \\\\ 3 & -6 & 8 \\\\ 2 & -3 & 6 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Anulamos debajo del 'pivote' de la fila $1$ — pero ahora trabajando por columnas.",
               "es_resultado": False},
              {"accion_md": (
                  "Expandimos por la **fila $1$**: $\\det A = 1 \\cdot \\det\\begin{bmatrix} -6 & 8 \\\\ -3 & 6 \\end{bmatrix} = -36 - (-24) = -12.$"
              ),
               "justificacion_md": "**Idea:** las OEC simplifican la primera fila, y luego una expansión $1\\times 1$ en esa fila da el resultado en un solo paso.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Propiedad multiplicativa",
          enunciado_md=(
              "Para $A, B \\in \\mathbb{R}^{n \\times n}$:\n\n"
              "$$\\boxed{\\det(AB) = \\det(A)\\,\\det(B).}$$\n\n"
              "**Consecuencias inmediatas:**\n\n"
              "- $\\det(A^k) = (\\det A)^k$ para $k \\in \\mathbb{N}$.\n"
              "- Si $A$ es invertible: $\\det(A^{-1}) = \\dfrac{1}{\\det A}$ (porque $A A^{-1} = I$ implica $\\det A \\cdot \\det A^{-1} = 1$).\n"
              "- $\\det(rA) = r^n \\det A$ para $A \\in \\mathbb{R}^{n \\times n}$ (escalar multiplicado a **todas** las entradas).\n"
              "- **¡Cuidado!** $\\det(A + B) \\neq \\det(A) + \\det(B)$ en general — la suma **no** es multiplicativa."
          ),
          demostracion_md=(
              "Si $A$ es **singular**, entonces $AB$ también lo es (las columnas de $AB$ son combinaciones lineales de columnas de $A$, no pueden generar $\\mathbb{R}^n$), así $\\det(AB) = 0 = 0 \\cdot \\det B = \\det A \\cdot \\det B$.\n\n"
              "Si $A$ es **invertible**, $A$ se factoriza como producto de elementales: $A = E_1 \\cdots E_p$. Por inducción y porque $\\det(E A) = \\det(E)\\det(A)$ para elementales (efecto de OEF), $\\det(AB) = \\det(E_1 \\cdots E_p B) = \\det(E_1)\\cdots \\det(E_p)\\det(B) = \\det(A)\\det(B)$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Verificación de la propiedad multiplicativa",
          problema_md=(
              "Verificar $\\det(AB) = \\det(A)\\det(B)$ para $A = \\begin{bmatrix} 6 & 1 \\\\ 3 & 2 \\end{bmatrix}$ y $B = \\begin{bmatrix} 4 & 3 \\\\ 1 & 2 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\det A = 12 - 3 = 9$. $\\det B = 8 - 3 = 5$. Producto esperado: $\\det(AB) = 45$."
              ),
               "justificacion_md": "Cálculos $2\\times 2$ con la fórmula $ad - bc$.",
               "es_resultado": False},
              {"accion_md": (
                  "$AB = \\begin{bmatrix} 6 & 1 \\\\ 3 & 2 \\end{bmatrix}\\begin{bmatrix} 4 & 3 \\\\ 1 & 2 \\end{bmatrix} = \\begin{bmatrix} 25 & 20 \\\\ 14 & 13 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Producto matricial estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\det(AB) = 25\\cdot 13 - 20\\cdot 14 = 325 - 280 = 45 = \\det A \\cdot \\det B$ ✓."
              ),
               "justificacion_md": "**Idea profunda:** $\\det(AB)$ mide el factor de cambio de volumen tras aplicar $B$ y luego $A$ — los factores se multiplican.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**$\\det A \\neq 0 \\iff A$ invertible** — esta equivalencia, ya enunciada en el TMI, ahora se entiende profundamente:\n\n"
            "- Si reducimos $A$ a forma triangular $U$ vía OEF, $\\det A = \\pm \\det U \\cdot (\\text{factores de escalado})$.\n"
            "- $\\det U = \\prod u_{ii}$ es no nulo $\\iff$ todos los pivotes son no nulos $\\iff$ $A$ tiene $n$ pivotes $\\iff$ $A$ invertible.\n\n"
            "**Para resolver $A\\vec{x} = \\vec{b}$:** $\\det A \\neq 0$ $\\Rightarrow$ solución única (lección 4.3 da la fórmula explícita por Cramer)."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\det A = 5$ y $B$ se obtiene de $A$ intercambiando dos filas, entonces $\\det B$ vale:",
                  "opciones_md": ["$5$", "$-5$", "$10$", "$0$"],
                  "correcta": "B",
                  "pista_md": "Intercambio de filas cambia el signo.",
                  "explicacion_md": "**$\\det B = -5$.** El intercambio de dos filas (o columnas) **siempre** invierte el signo del determinante.",
              },
              {
                  "enunciado_md": "Si $A$ es $3\\times 3$ y $\\det A = 2$, entonces $\\det(5A)$ vale:",
                  "opciones_md": ["$10$", "$25$", "$250$", "$2$"],
                  "correcta": "C",
                  "pista_md": "$\\det(rA) = r^n \\det A$ con $n = 3$.",
                  "explicacion_md": "**$\\det(5A) = 5^3 \\cdot 2 = 125 \\cdot 2 = 250$.** El escalar $5$ multiplica **cada** una de las $n = 3$ filas.",
              },
              {
                  "enunciado_md": "$\\det(AB) = \\det(BA)$ para matrices cuadradas $A, B$:",
                  "opciones_md": [
                      "Solo si $AB = BA$",
                      "Siempre",
                      "Nunca",
                      "Solo si $A, B$ son invertibles",
                  ],
                  "correcta": "B",
                  "pista_md": "Aunque $AB \\neq BA$ en general, ¿qué pasa con sus determinantes?",
                  "explicacion_md": "**Siempre.** $\\det(AB) = \\det A \\det B = \\det B \\det A = \\det(BA)$. Los **determinantes** sí conmutan, aunque los **productos** no.",
              },
          ]),

        ej(
            "Triangular y calcular",
            "Calcula $\\det A$ para $A = \\begin{bmatrix} 0 & 1 & 2 \\\\ 1 & 0 & 1 \\\\ 2 & 1 & 0 \\end{bmatrix}$ usando OEF.",
            [
                "Como $a_{11} = 0$, conviene un intercambio inicial.",
                "Recuerda controlar el signo.",
            ],
            (
                "Intercambio $F_1 \\leftrightarrow F_2$ (cambia signo):\n\n"
                "$\\det A = -\\det\\begin{bmatrix} 1 & 0 & 1 \\\\ 0 & 1 & 2 \\\\ 2 & 1 & 0 \\end{bmatrix}.$\n\n"
                "$F_3 \\leftarrow F_3 - 2F_1$ (no cambia): $-\\det\\begin{bmatrix} 1 & 0 & 1 \\\\ 0 & 1 & 2 \\\\ 0 & 1 & -2 \\end{bmatrix}$.\n\n"
                "$F_3 \\leftarrow F_3 - F_2$: $-\\det\\begin{bmatrix} 1 & 0 & 1 \\\\ 0 & 1 & 2 \\\\ 0 & 0 & -4 \\end{bmatrix} = -(1)(1)(-4) = 4$."
            ),
        ),

        ej(
            "Aplicar la propiedad multiplicativa",
            "Si $\\det A = 3$ y $\\det B = -2$, calcula: (a) $\\det(A^2 B)$; (b) $\\det(A^{-1})$; (c) $\\det(A B^T)$ asumiendo $A, B$ son $3\\times 3$.",
            [
                "(a) Multiplicatividad y $\\det A^k$.",
                "(b) $\\det(A^{-1}) = 1/\\det A$.",
                "(c) Propiedad de la transpuesta: $\\det B^T = \\det B$.",
            ],
            (
                "(a) $\\det(A^2 B) = (\\det A)^2 \\cdot \\det B = 9 \\cdot (-2) = -18$.\n\n"
                "(b) $\\det(A^{-1}) = 1/\\det A = 1/3$.\n\n"
                "(c) $\\det(A B^T) = \\det A \\cdot \\det B^T = \\det A \\cdot \\det B = 3 \\cdot (-2) = -6$."
            ),
        ),

        ej(
            "Determinante con factor común",
            "Calcula $\\det A$ para $A = \\begin{bmatrix} 4 & 8 & 12 \\\\ 1 & -1 & 2 \\\\ 0 & 3 & 5 \\end{bmatrix}$ aprovechando el factor común en la fila $1$.",
            [
                "Saca factor 4 de la fila 1.",
                "Luego triangula.",
            ],
            (
                "Factor 4 fuera de $F_1$: $\\det A = 4 \\det\\begin{bmatrix} 1 & 2 & 3 \\\\ 1 & -1 & 2 \\\\ 0 & 3 & 5 \\end{bmatrix}$.\n\n"
                "$F_2 \\leftarrow F_2 - F_1$: $4 \\det\\begin{bmatrix} 1 & 2 & 3 \\\\ 0 & -3 & -1 \\\\ 0 & 3 & 5 \\end{bmatrix}$. $F_3 \\leftarrow F_3 + F_2$: $4 \\det\\begin{bmatrix} 1 & 2 & 3 \\\\ 0 & -3 & -1 \\\\ 0 & 0 & 4 \\end{bmatrix} = 4 \\cdot 1 \\cdot (-3) \\cdot 4 = -48$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar invertir el signo al intercambiar filas.** Cada intercambio multiplica $\\det$ por $-1$.",
              "**Pensar que $\\det(A + B) = \\det A + \\det B$.** **Falso** en general — el determinante **no** es lineal.",
              "**Aplicar 'reemplazo no cambia' a escalamientos.** Solo el reemplazo $F_i \\leftarrow F_i + kF_j$ ($i \\neq j$) preserva $\\det$. Multiplicar una fila por $k$ sí lo cambia (por factor $k$).",
              "**Confundir 'sacar factor de una fila' con 'sacar factor de la matriz entera'.** Sacar factor $k$ de una sola fila multiplica $\\det$ por $k$. Para $\\det(rA)$ donde $r$ multiplica **todo**, el factor es $r^n$.",
              "**Aplicar OEC sin saber que también afectan $\\det$.** Las operaciones de columna se comportan exactamente como las de fila gracias a $\\det A^T = \\det A$.",
              "**Usar la propiedad multiplicativa con matrices no cuadradas o de tamaños incompatibles.** $\\det(AB)$ requiere $A, B$ ambas cuadradas del **mismo tamaño**.",
          ]),

        b("resumen",
          puntos_md=[
              "**OEF y $\\det$:** reemplazo no cambia, intercambio cambia signo, escalamiento por $k$ multiplica por $k$.",
              "**$\\det(A^T) = \\det(A)$** $\\Rightarrow$ las propiedades para filas se trasladan a columnas (OEC).",
              "**Algoritmo eficiente:** triangulizar con OEF (controlando signos) y aplicar $\\det = \\prod u_{ii}$.",
              "**Multiplicativa:** $\\det(AB) = \\det(A)\\det(B)$.",
              "**Consecuencias:** $\\det(A^k) = (\\det A)^k$, $\\det(A^{-1}) = 1/\\det A$, $\\det(rA) = r^n \\det A$.",
              "**Cuidado:** $\\det(A + B) \\neq \\det A + \\det B$ en general.",
              "**Próxima lección:** **aplicaciones** — Cramer, fórmula de la inversa por adjunta, e interpretación geométrica como factor de área/volumen.",
          ]),
    ]
    return {
        "id": "lec-al-4-2-propiedades-determinante",
        "title": "Propiedades del determinante",
        "description": "Efecto de OEF y OEC sobre $\\det$, $\\det(A^T) = \\det(A)$, propiedad multiplicativa $\\det(AB) = \\det A \\det B$ y método eficiente vía triangulación.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# =====================================================================
# 4.3 Aplicaciones de la determinante
# =====================================================================
def lesson_4_3():
    blocks = [
        b("texto", body_md=(
            "Cerramos el capítulo con tres aplicaciones clásicas y profundas del determinante:\n\n"
            "1. **Regla de Cramer** — fórmula explícita para la solución de $A\\vec{x} = \\vec{b}$ cuando $A$ es invertible.\n"
            "2. **Fórmula de la inversa por adjunta** — expresión cerrada $A^{-1} = \\tfrac{1}{\\det A}\\,\\text{adj}(A)$.\n"
            "3. **Interpretación geométrica** — $|\\det A|$ es el **factor de cambio de área/volumen** de la transformación $T(\\vec{x}) = A\\vec{x}$.\n\n"
            "Aunque numéricamente las dos primeras son **ineficientes** para tamaños grandes (en la práctica se usa Gauss-Jordan o factorizaciones LU/QR), son **conceptualmente esenciales**: dan fórmulas explícitas que conectan el determinante con la solución de sistemas y con la inversa, y la interpretación geométrica abre la puerta al **cambio de variable** en cálculo integral (jacobiano).\n\n"
            "Al terminar, debes poder:\n\n"
            "- Aplicar la **regla de Cramer** a sistemas $2\\times 2$ y $3\\times 3$.\n"
            "- Construir la **adjunta** $\\text{adj}(A) = C^T$ y usarla para calcular $A^{-1}$.\n"
            "- Interpretar $|\\det A|$ como factor de área/volumen y aplicarlo (ej. área de una elipse)."
        )),

        b("definicion",
          titulo="Notación $A_i(\\vec{b})$ para la regla de Cramer",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{n \\times n}$ con columnas $A = [\\,\\vec{a}_1\\ \\vec{a}_2\\ \\cdots\\ \\vec{a}_n\\,]$ y $\\vec{b} \\in \\mathbb{R}^n$.\n\n"
              "Para $i = 1, \\ldots, n$, definimos $A_i(\\vec{b})$ como la matriz que se obtiene **reemplazando la columna $i$ de $A$ por el vector $\\vec{b}$**:\n\n"
              "$$A_i(\\vec{b}) = [\\,\\vec{a}_1\\ \\cdots\\ \\vec{a}_{i-1}\\ \\vec{b}\\ \\vec{a}_{i+1}\\ \\cdots\\ \\vec{a}_n\\,].$$\n\n"
              "Es la matriz $A$ con **una sola columna sustituida**."
          )),

        b("teorema",
          nombre="Regla de Cramer",
          enunciado_md=(
              "Si $A \\in \\mathbb{R}^{n \\times n}$ es **invertible** ($\\det A \\neq 0$), entonces el sistema $A\\vec{x} = \\vec{b}$ tiene solución única $\\vec{x} = (x_1, \\ldots, x_n)^T$ dada por\n\n"
              "$$\\boxed{x_i = \\frac{\\det\\bigl(A_i(\\vec{b})\\bigr)}{\\det(A)}, \\qquad i = 1, \\ldots, n.}$$"
          ),
          demostracion_md=(
              "Escribimos $A\\vec{x} = \\vec{b}$ como $A \\cdot [\\,\\vec{e}_1\\ \\cdots\\ \\vec{x}\\ \\cdots\\ \\vec{e}_n\\,] = A_i(\\vec{b})$ (con $\\vec{x}$ en la posición $i$). Llamando $I_i(\\vec{x})$ a la matriz $I_n$ con la columna $i$ reemplazada por $\\vec{x}$:\n\n"
              "$A \\cdot I_i(\\vec{x}) = A_i(\\vec{b})$.\n\n"
              "Aplicando $\\det$ y la propiedad multiplicativa:\n\n"
              "$\\det(A) \\cdot \\det(I_i(\\vec{x})) = \\det(A_i(\\vec{b}))$.\n\n"
              "Desarrollando $\\det(I_i(\\vec{x}))$ por cofactores en la columna $i$ (que es $\\vec{x}$, y el resto de columnas son $\\vec{e}_j$ con $j \\neq i$): $\\det(I_i(\\vec{x})) = x_i$. Por tanto $x_i = \\det(A_i(\\vec{b}))/\\det(A)$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Cramer en un sistema $2\\times 2$",
          problema_md=(
              "Resolver por Cramer $\\begin{cases} 3x_1 - 2x_2 = 6 \\\\ -5x_1 + 4x_2 = 8 \\end{cases}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A = \\begin{bmatrix} 3 & -2 \\\\ -5 & 4 \\end{bmatrix}$, $\\det A = 12 - 10 = 2 \\neq 0$ $\\Rightarrow$ Cramer aplica.\n\n"
                  "$A_1(\\vec{b}) = \\begin{bmatrix} 6 & -2 \\\\ 8 & 4 \\end{bmatrix}$ (columna 1 reemplazada por $\\vec{b}$). $\\det(A_1(\\vec{b})) = 24 + 16 = 40$."
              ),
               "justificacion_md": "Verificamos invertibilidad antes de usar Cramer.",
               "es_resultado": False},
              {"accion_md": (
                  "$A_2(\\vec{b}) = \\begin{bmatrix} 3 & 6 \\\\ -5 & 8 \\end{bmatrix}$. $\\det(A_2(\\vec{b})) = 24 - (-30) = 54$.\n\n"
                  "$x_1 = 40/2 = 20$, $x_2 = 54/2 = 27$.\n\n"
                  "**$\\vec{x} = (20, 27)^T$.**"
              ),
               "justificacion_md": "Verificación: $3(20) - 2(27) = 60 - 54 = 6$ ✓ y $-5(20) + 4(27) = -100 + 108 = 8$ ✓.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**¿Cuándo conviene Cramer?**\n\n"
            "- **Sistemas $2 \\times 2$ y $3 \\times 3$ con coeficientes simples:** la fórmula es directa y produce resultados rápido.\n"
            "- **Demostraciones teóricas:** al ser una **fórmula cerrada**, permite probar resultados (ej. la fórmula de la inversa por adjunta).\n"
            "- **Análisis de sensibilidad:** muestra cómo varían las soluciones cuando cambian los coeficientes.\n\n"
            "**¿Cuándo NO conviene?**\n\n"
            "- **Sistemas grandes ($n \\geq 4$):** calcular $n + 1$ determinantes es **mucho** más costoso que Gauss-Jordan ($O(n!)$ vs $O(n^3)$).\n"
            "- **Sistemas con coeficientes numéricos generales:** numéricamente inestable.\n\n"
            "En la práctica computacional, Cramer es más una herramienta teórica que un método algorítmico."
        )),

        b("definicion",
          titulo="Matriz de cofactores y adjunta",
          body_md=(
              "Sea $A = [a_{ij}] \\in \\mathbb{R}^{n \\times n}$. Definimos:\n\n"
              "- **Matriz de cofactores** $C = [C_{ij}]$, donde $C_{ij} = (-1)^{i+j}\\det(A_{ij})$ (igual que en lección 4.1).\n"
              "- **Adjunta** (o **adjugada**) de $A$:\n\n"
              "$$\\boxed{\\text{adj}(A) = C^T.}$$\n\n"
              "Es decir, $\\text{adj}(A)$ es la **transpuesta** de la matriz de cofactores. La entrada $(i, j)$ de $\\text{adj}(A)$ es $C_{ji}$ (con índices intercambiados).\n\n"
              "**¡Cuidado con la transposición!** Es uno de los puntos donde más se equivocan los estudiantes."
          )),

        b("teorema",
          nombre="Fórmula de la inversa por adjunta",
          enunciado_md=(
              "Si $A \\in \\mathbb{R}^{n \\times n}$ es **invertible**, entonces\n\n"
              "$$\\boxed{A^{-1} = \\frac{1}{\\det A}\\,\\text{adj}(A),}$$\n\n"
              "y entrada por entrada,\n\n"
              "$$(A^{-1})_{ij} = \\frac{C_{ji}}{\\det A}.$$"
          ),
          demostracion_md=(
              "Para cada $j$, la columna $j$ de $A^{-1}$ es la solución de $A\\vec{x} = \\vec{e}_j$. Por la regla de Cramer:\n\n"
              "$(A^{-1})_{ij} = x_i = \\frac{\\det(A_i(\\vec{e}_j))}{\\det A} = \\frac{(-1)^{i+j}\\det(A_{ji})}{\\det A} = \\frac{C_{ji}}{\\det A}.$\n\n"
              "(El cofactor que aparece es $C_{ji}$ — índices intercambiados — porque al desarrollar $\\det(A_i(\\vec{e}_j))$ por la columna $i$, el único término no nulo es $1 \\cdot C_{ji}$.) Agrupando todas las columnas se obtiene $A^{-1} = \\tfrac{1}{\\det A}\\,\\text{adj}(A)$. $\\blacksquare$\n\n"
              "**Observación.** Esto recupera la fórmula $2\\times 2$: para $A = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$, los cofactores son $C_{11} = d, C_{12} = -c, C_{21} = -b, C_{22} = a$, así $C = \\begin{bmatrix} d & -c \\\\ -b & a \\end{bmatrix}$ y $\\text{adj}(A) = C^T = \\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix}$. Recuperamos exactamente $A^{-1} = \\frac{1}{ad - bc}\\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix}$."
          )),

        b("ejemplo_resuelto",
          titulo="Inversa $3\\times 3$ por adjunta",
          problema_md=(
              "Halla $A^{-1}$ usando la fórmula de la adjunta para $A = \\begin{bmatrix} 2 & 1 & 3 \\\\ 1 & -1 & 1 \\\\ 1 & 4 & -2 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Calcular $\\det A$.** Por expansión por la fila $1$:\n\n"
                  "$\\det A = 2\\det\\begin{bmatrix} -1 & 1 \\\\ 4 & -2 \\end{bmatrix} - 1\\det\\begin{bmatrix} 1 & 1 \\\\ 1 & -2 \\end{bmatrix} + 3\\det\\begin{bmatrix} 1 & -1 \\\\ 1 & 4 \\end{bmatrix}$\n\n"
                  "$= 2(2 - 4) - (-3) + 3(5) = -4 + 3 + 15 = 14.$"
              ),
               "justificacion_md": "Si saliera $0$, $A$ no sería invertible y la fórmula no aplicaría.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular los $9$ cofactores** (organizados como matriz $C$):\n\n"
                  "$C_{11} = +\\det\\begin{bmatrix} -1 & 1 \\\\ 4 & -2 \\end{bmatrix} = -2$, $C_{12} = -\\det\\begin{bmatrix} 1 & 1 \\\\ 1 & -2 \\end{bmatrix} = 3$, $C_{13} = +\\det\\begin{bmatrix} 1 & -1 \\\\ 1 & 4 \\end{bmatrix} = 5$,\n\n"
                  "$C_{21} = -\\det\\begin{bmatrix} 1 & 3 \\\\ 4 & -2 \\end{bmatrix} = 14$, $C_{22} = +\\det\\begin{bmatrix} 2 & 3 \\\\ 1 & -2 \\end{bmatrix} = -7$, $C_{23} = -\\det\\begin{bmatrix} 2 & 1 \\\\ 1 & 4 \\end{bmatrix} = -7$,\n\n"
                  "$C_{31} = +\\det\\begin{bmatrix} 1 & 3 \\\\ -1 & 1 \\end{bmatrix} = 4$, $C_{32} = -\\det\\begin{bmatrix} 2 & 3 \\\\ 1 & 1 \\end{bmatrix} = 1$, $C_{33} = +\\det\\begin{bmatrix} 2 & 1 \\\\ 1 & -1 \\end{bmatrix} = -3$.\n\n"
                  "Matriz de cofactores: $C = \\begin{bmatrix} -2 & 3 & 5 \\\\ 14 & -7 & -7 \\\\ 4 & 1 & -3 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Es **el** paso laborioso. Para tamaños $\\geq 4$ es prohibitivo a mano.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\text{adj}(A) = C^T = \\begin{bmatrix} -2 & 14 & 4 \\\\ 3 & -7 & 1 \\\\ 5 & -7 & -3 \\end{bmatrix}.$\n\n"
                  "$A^{-1} = \\dfrac{1}{14}\\begin{bmatrix} -2 & 14 & 4 \\\\ 3 & -7 & 1 \\\\ 5 & -7 & -3 \\end{bmatrix} = \\begin{bmatrix} -1/7 & 1 & 2/7 \\\\ 3/14 & -1/2 & 1/14 \\\\ 5/14 & -1/2 & -3/14 \\end{bmatrix}.$"
              ),
               "justificacion_md": "**Recordatorio: transponer** la matriz de cofactores antes de dividir por $\\det A$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Determinante como área (en $\\mathbb{R}^2$) y volumen (en $\\mathbb{R}^3$)",
          enunciado_md=(
              "**(a)** Si $A \\in \\mathbb{R}^{2 \\times 2}$, el **área del paralelogramo** generado por las columnas de $A$ es $|\\det A|$.\n\n"
              "**(b)** Si $A \\in \\mathbb{R}^{3 \\times 3}$, el **volumen del paralelepípedo** generado por las columnas de $A$ es $|\\det A|$.\n\n"
              "El **signo** de $\\det A$ codifica la **orientación**: $\\det A > 0$ preserva orientación; $\\det A < 0$ la invierte (reflexión)."
          ),
          demostracion_md=(
              "**Esquema $\\mathbb{R}^2$.** Sean $\\vec{u} = (a, c)^T$ y $\\vec{v} = (b, d)^T$ las columnas. El paralelogramo generado tiene base $\\|\\vec{u}\\|$ y altura $h = \\|\\vec{v}\\| |\\sin\\theta|$. Así, área $= \\|\\vec{u}\\|\\|\\vec{v}\\||\\sin\\theta|$. Pero $\\|\\vec{u}\\|\\|\\vec{v}\\|\\sin\\theta$ es la magnitud del producto cruz tridimensional con $\\vec{u}, \\vec{v}$ extendidos a $\\mathbb{R}^3$ (con tercera componente $0$), que es $|ad - bc| = |\\det A|$. $\\blacksquare$\n\n"
              "El caso $\\mathbb{R}^3$ recurre al **producto triple escalar** $\\vec{u} \\cdot (\\vec{v} \\times \\vec{w}) = \\det A$ (lección 1.3)."
          )),

        b("ejemplo_resuelto",
          titulo="Área del paralelogramo en $\\mathbb{R}^2$",
          problema_md=(
              "Calcular el área del paralelogramo generado por las columnas de $A = \\begin{bmatrix} 3 & 2 \\\\ 1 & 4 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Las columnas $\\vec{u} = (3, 1)^T$ y $\\vec{v} = (2, 4)^T$ forman el paralelogramo. Aplicamos:\n\n"
                  "$\\text{área} = |\\det A| = |3\\cdot 4 - 1\\cdot 2| = |12 - 2| = 10.$"
              ),
               "justificacion_md": "Sin necesidad de coordenadas — el determinante absorbe toda la geometría.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Volumen del paralelepípedo en $\\mathbb{R}^3$",
          problema_md=(
              "Calcular el volumen del paralelepípedo generado por las columnas de $A = \\begin{bmatrix} 1 & 0 & 2 \\\\ 0 & 1 & 2 \\\\ 2 & 0 & 1 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Expandimos $\\det A$ por la fila $2$ (tiene un $0$):\n\n"
                  "$\\det A = 0 - 1\\cdot \\det\\begin{bmatrix} 1 & 2 \\\\ 2 & 1 \\end{bmatrix} + 2 \\cdot \\det\\begin{bmatrix} 1 & 0 \\\\ 2 & 0 \\end{bmatrix} \\cdot 0 = -(1 - 4) + 0 = 3.$\n\n"
                  "Espera — recalculamos con cuidado. Por fila $1$: $\\det A = 1\\det\\begin{bmatrix} 1 & 2 \\\\ 0 & 1 \\end{bmatrix} - 0 + 2\\det\\begin{bmatrix} 0 & 1 \\\\ 2 & 0 \\end{bmatrix} = 1(1) + 2(-2) = -3.$"
              ),
               "justificacion_md": "Doble verificación: dos expansiones distintas deben dar el mismo número.",
               "es_resultado": False},
              {"accion_md": (
                  "**Volumen** $= |\\det A| = |-3| = 3$ unidades cúbicas."
              ),
               "justificacion_md": "El **valor absoluto** elimina el signo (la orientación) y deja el volumen geométrico.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Área/volumen bajo transformaciones lineales",
          enunciado_md=(
              "Sea $T : \\mathbb{R}^n \\to \\mathbb{R}^n$ ($n = 2$ o $3$) la transformación lineal $T(\\vec{x}) = A\\vec{x}$ y $S$ una región del dominio. Entonces:\n\n"
              "$$\\text{área}/\\text{volumen}(T(S)) = |\\det A| \\cdot \\text{área}/\\text{volumen}(S).$$\n\n"
              "Es decir, **$|\\det A|$ es el factor de escala** con que $T$ transforma áreas (en $\\mathbb{R}^2$) o volúmenes (en $\\mathbb{R}^3$)."
          ),
          demostracion_md=(
              "Para un **paralelogramo** $S$ con lados $\\vec{u}, \\vec{v}$, $T(S)$ tiene lados $A\\vec{u}, A\\vec{v}$, así su área es $|\\det[\\,A\\vec{u}\\ A\\vec{v}\\,]| = |\\det(A[\\vec{u}\\ \\vec{v}])| = |\\det A| |\\det[\\vec{u}\\ \\vec{v}]| = |\\det A| \\cdot \\text{área}(S)$.\n\n"
              "Para regiones generales, el resultado se extiende vía **integración** (cambio de variables, jacobiano = $|\\det A|$). $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Área de una elipse",
          problema_md=(
              "Sean $a, b > 0$. Halla el área de la región $E$ acotada por la elipse $\\dfrac{x_1^2}{a^2} + \\dfrac{x_2^2}{b^2} \\leq 1$."
          ),
          pasos=[
              {"accion_md": (
                  "$E$ es la imagen del **disco unitario** $D = \\{\\vec{u} : u_1^2 + u_2^2 \\leq 1\\}$ bajo la transformación lineal $T(\\vec{u}) = A\\vec{u}$ con $A = \\begin{bmatrix} a & 0 \\\\ 0 & b \\end{bmatrix}$.\n\n"
                  "Verificación: si $\\vec{x} = A\\vec{u}$, entonces $u_1 = x_1/a$, $u_2 = x_2/b$, y $u_1^2 + u_2^2 \\leq 1 \\iff x_1^2/a^2 + x_2^2/b^2 \\leq 1$ ✓."
              ),
               "justificacion_md": "**Idea clave:** una elipse es 'el disco escalado por $a$ en horizontal y $b$ en vertical'.",
               "es_resultado": False},
              {"accion_md": (
                  "Por el teorema, $\\text{área}(E) = |\\det A| \\cdot \\text{área}(D) = ab \\cdot \\pi(1)^2 = \\boxed{\\pi a b}.$"
              ),
               "justificacion_md": "**Resultado clásico** que generalmente requiere integrales — aquí cae directamente del determinante. Esta es la **idea germen del jacobiano** en cambio de variables.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "En la regla de Cramer para $A\\vec{x} = \\vec{b}$, la matriz $A_2(\\vec{b})$ se obtiene:",
                  "opciones_md": [
                      "Reemplazando la fila $2$ de $A$ por $\\vec{b}$",
                      "Reemplazando la **columna $2$** de $A$ por $\\vec{b}$",
                      "Multiplicando $A$ por $2$",
                      "Tomando la transpuesta de $A$",
                  ],
                  "correcta": "B",
                  "pista_md": "El subíndice indica la columna que se reemplaza.",
                  "explicacion_md": "**Reemplazar la columna $i$ por $\\vec{b}$** define $A_i(\\vec{b})$. Cramer da $x_i = \\det(A_i(\\vec{b}))/\\det A$.",
              },
              {
                  "enunciado_md": "La fórmula $A^{-1} = \\frac{1}{\\det A}\\text{adj}(A)$ requiere:",
                  "opciones_md": [
                      "$\\det A = 1$",
                      "$\\det A \\neq 0$",
                      "$A$ ser triangular",
                      "$A$ ser simétrica",
                  ],
                  "correcta": "B",
                  "pista_md": "Hay que dividir por $\\det A$.",
                  "explicacion_md": "**$\\det A \\neq 0$** (i.e., $A$ invertible). Si fuera $0$, dividiríamos por cero y la inversa no existe.",
              },
              {
                  "enunciado_md": "Si $T(\\vec{x}) = A\\vec{x}$ con $\\det A = -3$ y $S$ es un cuadrado de área $4$, entonces $T(S)$:",
                  "opciones_md": [
                      "Tiene área $-12$",
                      "Tiene área $12$ y conserva la orientación",
                      "**Tiene área $12$ y invierte la orientación**",
                      "No es un cuadrilátero",
                  ],
                  "correcta": "C",
                  "pista_md": "El signo de $\\det A$ codifica orientación; el módulo, el factor de área.",
                  "explicacion_md": "Área de $T(S) = |\\det A| \\cdot 4 = 3 \\cdot 4 = 12$. **Signo negativo $\\Rightarrow$ invierte orientación** (el cuadrado original con vértices en orden antihorario sale en orden horario).",
              },
          ]),

        ej(
            "Cramer en sistema $3\\times 3$",
            "Resuelve por Cramer: $\\begin{cases} x_1 + 2x_2 + x_3 = 5 \\\\ 2x_1 - x_2 + x_3 = -1 \\\\ x_1 + x_2 - x_3 = 0 \\end{cases}$.",
            [
                "Calcula $\\det A$ primero.",
                "Construye $A_1(\\vec{b}), A_2(\\vec{b}), A_3(\\vec{b})$ reemplazando la columna correspondiente.",
            ],
            (
                "$A = \\begin{bmatrix} 1 & 2 & 1 \\\\ 2 & -1 & 1 \\\\ 1 & 1 & -1 \\end{bmatrix}$, $\\det A = 1(1-1) - 2(-2-1) + 1(2+1) = 0 + 6 + 3 = 9$.\n\n"
                "$A_1(\\vec{b}) = \\begin{bmatrix} 5 & 2 & 1 \\\\ -1 & -1 & 1 \\\\ 0 & 1 & -1 \\end{bmatrix}$, $\\det = 5(1 - 1) - 2(1 - 0) + 1(-1 - 0) = -3$. $x_1 = -3/9 = -1/3$.\n\n"
                "$A_2(\\vec{b}) = \\begin{bmatrix} 1 & 5 & 1 \\\\ 2 & -1 & 1 \\\\ 1 & 0 & -1 \\end{bmatrix}$, $\\det = 1(1) - 5(-3) + 1(1) = 1 + 15 + 1 = 17$. $x_2 = 17/9$.\n\n"
                "$A_3(\\vec{b}) = \\begin{bmatrix} 1 & 2 & 5 \\\\ 2 & -1 & -1 \\\\ 1 & 1 & 0 \\end{bmatrix}$, $\\det = 1(0 + 1) - 2(0 + 1) + 5(2 + 1) = 1 - 2 + 15 = 14$. $x_3 = 14/9$.\n\n"
                "$\\vec{x} = (-1/3,\\ 17/9,\\ 14/9)^T$."
            ),
        ),

        ej(
            "Inversa $2\\times 2$ por adjunta",
            "Aplica la fórmula $A^{-1} = \\tfrac{1}{\\det A}\\text{adj}(A)$ a $A = \\begin{bmatrix} 4 & 7 \\\\ 2 & 5 \\end{bmatrix}$.",
            [
                "Calcula los $4$ cofactores y arma $C$.",
                "Transpón para obtener $\\text{adj}(A)$.",
            ],
            (
                "$\\det A = 20 - 14 = 6$.\n\n"
                "Cofactores: $C_{11} = 5$, $C_{12} = -2$, $C_{21} = -7$, $C_{22} = 4$. $C = \\begin{bmatrix} 5 & -2 \\\\ -7 & 4 \\end{bmatrix}$.\n\n"
                "$\\text{adj}(A) = C^T = \\begin{bmatrix} 5 & -7 \\\\ -2 & 4 \\end{bmatrix}$.\n\n"
                "$A^{-1} = \\dfrac{1}{6}\\begin{bmatrix} 5 & -7 \\\\ -2 & 4 \\end{bmatrix} = \\begin{bmatrix} 5/6 & -7/6 \\\\ -1/3 & 2/3 \\end{bmatrix}$.\n\n"
                "Coincide con la fórmula directa $2\\times 2$: $\\dfrac{1}{6}\\begin{bmatrix} 5 & -7 \\\\ -2 & 4 \\end{bmatrix}$ ✓."
            ),
        ),

        ej(
            "Área de un paralelogramo",
            "Halla el área del paralelogramo con vértices $(0,0)$, $(3, 1)$, $(1, 5)$ y $(4, 6)$.",
            [
                "Identifica las dos columnas de la matriz $A$ con dos lados desde el origen.",
                "Aplica $|\\det A|$.",
            ],
            (
                "Lados desde $(0,0)$: $\\vec{u} = (3, 1)^T$ y $\\vec{v} = (1, 5)^T$. (Verificamos: $\\vec{u} + \\vec{v} = (4, 6)^T$ — el cuarto vértice coincide ✓.)\n\n"
                "$A = \\begin{bmatrix} 3 & 1 \\\\ 1 & 5 \\end{bmatrix}$, $|\\det A| = |15 - 1| = 14$.\n\n"
                "**Área $= 14$.**"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Cramer cuando $\\det A = 0$.** No funciona — el sistema es SI o SCI; usa Gauss-Jordan.",
              "**Olvidar transponer la matriz de cofactores** al construir la adjunta. $\\text{adj}(A) = C^T$, no $C$.",
              "**Confundir el subíndice de $A_i(\\vec{b})$.** Es la **columna** $i$ que se reemplaza, no la fila.",
              "**Usar Cramer para sistemas grandes.** Es $O(n!)$ — extremadamente ineficiente para $n \\geq 4$.",
              "**Olvidar el valor absoluto** al usar $\\det A$ como área/volumen. El signo solo da orientación.",
              "**Pensar que $\\det(A^{-1}) = -\\det A$.** Lo correcto: $\\det(A^{-1}) = \\frac{1}{\\det A}$.",
              "**Aplicar la fórmula del área 'columnas de $A$' a otros conjuntos.** El teorema da el área del paralelogramo generado por **las columnas**, no por filas o vectores arbitrarios.",
          ]),

        b("resumen",
          puntos_md=[
              "**Regla de Cramer:** $x_i = \\det(A_i(\\vec{b}))/\\det(A)$, válida si $\\det A \\neq 0$.",
              "**Fórmula de la inversa:** $A^{-1} = \\frac{1}{\\det A}\\,\\text{adj}(A)$, donde $\\text{adj}(A) = C^T$ (matriz de cofactores transpuesta).",
              "**$|\\det A|$ = factor de área (en $\\mathbb{R}^2$) o volumen (en $\\mathbb{R}^3$)** del paralelogramo/paralelepípedo generado por las columnas de $A$.",
              "**$|\\det A|$ es el factor de escala** con que $T(\\vec{x}) = A\\vec{x}$ transforma áreas y volúmenes.",
              "**Signo de $\\det A$:** positivo preserva orientación, negativo la invierte.",
              "**Cramer y la fórmula de la inversa son ineficientes para $n \\geq 4$** — útiles **conceptualmente** y en pruebas teóricas. La práctica usa eliminación / factorizaciones.",
              "**Cierre del capítulo:** El determinante conecta álgebra (invertibilidad, sistemas) con geometría (áreas, volúmenes, orientación).",
              "**Próximo capítulo:** **Espacios y subespacios vectoriales** — el marco abstracto que generaliza $\\mathbb{R}^n$.",
          ]),
    ]
    return {
        "id": "lec-al-4-3-aplicaciones-determinante",
        "title": "Aplicaciones del determinante",
        "description": "Regla de Cramer, fórmula de la inversa por adjunta $A^{-1} = \\frac{1}{\\det A}\\text{adj}(A)$, interpretación geométrica como factor de área/volumen.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
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

    chapter_id = "ch-al-determinantes"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Determinantes",
        "description": (
            "Determinante por menores y cofactores; propiedades respecto a OEF, "
            "transpuesta y producto; aplicaciones: regla de Cramer, fórmula de la "
            "inversa por adjunta e interpretación como factor de área/volumen."
        ),
        "order": 4,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_4_1, lesson_4_2, lesson_4_3]
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
        f"✅ Capítulo 4 — Determinantes listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
