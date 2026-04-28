"""
Seed del curso Álgebra Lineal — Capítulo 8: Matrices Simétricas.
3 lecciones:
  8.1 Diagonalización ortogonal (matrices simétricas, teorema espectral, A = PDP^T, descomposición espectral)
  8.2 Formas cuadráticas (Q(x) = x^T A x, ejes principales, clasificación)
  8.3 Descomposición en valores singulares (SVD: A = U Σ V^T)

Capítulo final del curso. Basado en los Apuntes/Clase de Se Remonta. Idempotente.
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
# 8.1 Diagonalización ortogonal
# =====================================================================
def lesson_8_1():
    blocks = [
        b("texto", body_md=(
            "Las **matrices simétricas** ($A^T = A$) tienen propiedades **excepcionalmente buenas**: "
            "son **siempre diagonalizables**, sus valores propios son **reales**, y los vectores propios "
            "se pueden elegir **ortonormales**. Esto las convierte en el caso 'ideal' de la diagonalización.\n\n"
            "El resultado central de esta lección es el **teorema espectral**: toda matriz simétrica $A$ se "
            "factoriza como $A = PDP^T$ con $P$ **ortogonal** ($P^{-1} = P^T$) y $D$ diagonal. Esto se llama "
            "**diagonalización ortogonal**.\n\n"
            "Las matrices simétricas aparecen en todas partes:\n\n"
            "- **Estadística:** matrices de covarianza ($\\Sigma$).\n"
            "- **Mecánica:** tensores de inercia, deformación.\n"
            "- **Optimización:** matrices Hessianas (segundas derivadas).\n"
            "- **Grafos:** matriz de adyacencia de grafos no dirigidos.\n"
            "- **Mecánica cuántica:** observables (matrices Hermíticas, generalización a complejos).\n\n"
            "Al terminar:\n\n"
            "- Conoces el **teorema espectral** y todas sus consecuencias.\n"
            "- Diagonalizas ortogonalmente una matriz simétrica.\n"
            "- Construyes la **descomposición espectral** $A = \\sum \\lambda_i \\vec{u}_i \\vec{u}_i^T$."
        )),

        b("definicion",
          titulo="Matriz simétrica y diagonalización ortogonal",
          body_md=(
              "Una matriz $A \\in \\mathbb{R}^{n \\times n}$ es **simétrica** si $A^T = A$, es decir, $a_{ij} = a_{ji}$ para todo $i, j$.\n\n"
              "$A$ es **diagonalizable ortogonalmente** si existen una matriz **ortogonal** $P$ (i.e., $P^T = P^{-1}$, columnas ortonormales) y una matriz diagonal $D$ tales que\n\n"
              "$$\\boxed{A = P D P^T = P D P^{-1}.}$$\n\n"
              "Por la relación $P^T = P^{-1}$ (al ser ortogonal), las dos formas son equivalentes.\n\n"
              "**Interpretación:** las columnas de $P$ son una **base ortonormal de vectores propios** de $A$, y la transformación $\\vec{x} \\mapsto A\\vec{x}$ se ve como **escalas independientes** en esa base ortonormal."
          )),

        b("teorema",
          enunciado_md=(
              "**Vectores propios de espacios propios distintos son ortogonales.**\n\n"
              "Si $A$ es **simétrica** y $\\vec{v}_1, \\vec{v}_2$ son vectores propios de $A$ correspondientes a valores propios distintos $\\lambda_1 \\neq \\lambda_2$, entonces $\\vec{v}_1 \\perp \\vec{v}_2$."
          ),
          demostracion_md=(
              "$\\lambda_1 \\vec{v}_1 \\cdot \\vec{v}_2 = (A\\vec{v}_1)\\cdot\\vec{v}_2 = \\vec{v}_1^T A^T \\vec{v}_2 = \\vec{v}_1^T A \\vec{v}_2 = \\vec{v}_1\\cdot(\\lambda_2 \\vec{v}_2) = \\lambda_2 \\vec{v}_1\\cdot\\vec{v}_2$.\n\n"
              "(Usamos $A^T = A$.) Por tanto $(\\lambda_1 - \\lambda_2)(\\vec{v}_1\\cdot\\vec{v}_2) = 0$. Como $\\lambda_1 \\neq \\lambda_2$, $\\vec{v}_1\\cdot\\vec{v}_2 = 0$. $\\blacksquare$"
          )),

        b("teorema",
          nombre="Teorema espectral (caracterización)",
          enunciado_md=(
              "Una matriz $A \\in \\mathbb{R}^{n \\times n}$ es **diagonalizable ortogonalmente** $\\iff A$ es **simétrica**.\n\n"
              "Más aún, si $A$ es simétrica:\n\n"
              "1. $A$ tiene **$n$ valores propios reales** (contando multiplicidades).\n"
              "2. Para cada valor propio, la **multiplicidad geométrica = multiplicidad algebraica** (no hay deficiencia geométrica).\n"
              "3. Los espacios propios correspondientes a valores propios distintos son **mutuamente ortogonales**.\n"
              "4. $A$ es **diagonalizable ortogonalmente** ($A = PDP^T$ con $P$ ortogonal y $D$ diagonal real)."
          ),
          demostracion_md=(
              "**($\\Leftarrow$)** Si $A = PDP^T$ con $P$ ortogonal y $D$ diagonal, entonces $A^T = (PDP^T)^T = PD^TP^T = PDP^T = A$ (porque $D = D^T$ por ser diagonal). Así, $A$ es simétrica.\n\n"
              "**($\\Rightarrow$)** Demostración no trivial; usa inducción y el teorema fundamental del álgebra. Detalles en cualquier texto avanzado de álgebra lineal. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Diagonalización ortogonal — valores propios distintos",
          problema_md=(
              "Diagonalizar ortogonalmente $A = \\begin{bmatrix} 6 & -2 & -1 \\\\ -2 & 6 & -1 \\\\ -1 & -1 & 5 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1: valores propios.** Polinomio característico (omitiendo cómputo): $0 = -\\lambda^3 + 17\\lambda^2 - 90\\lambda + 144 = -(\\lambda - 8)(\\lambda - 6)(\\lambda - 3)$.\n\n"
                  "**Valores propios:** $\\lambda_1 = 8$, $\\lambda_2 = 6$, $\\lambda_3 = 3$ — los tres distintos."
              ),
               "justificacion_md": "Como $A$ es simétrica con valores propios distintos, los vectores propios serán automáticamente ortogonales.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2: vectores propios.** Resolviendo $(A - \\lambda I)\\vec{x} = \\vec{0}$ para cada $\\lambda$:\n\n"
                  "$\\lambda = 8$: $\\vec{v}_1 = (-1, 1, 0)^T$.\n\n"
                  "$\\lambda = 6$: $\\vec{v}_2 = (-1, -1, 2)^T$.\n\n"
                  "$\\lambda = 3$: $\\vec{v}_3 = (1, 1, 1)^T$."
              ),
               "justificacion_md": "Verificar ortogonalidad: $\\vec{v}_1\\cdot\\vec{v}_2 = 1 - 1 + 0 = 0$ ✓, $\\vec{v}_1\\cdot\\vec{v}_3 = -1 + 1 + 0 = 0$ ✓, $\\vec{v}_2\\cdot\\vec{v}_3 = -1 - 1 + 2 = 0$ ✓.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3: normalizar para obtener base ortonormal.**\n\n"
                  "$\\vec{u}_1 = \\dfrac{1}{\\sqrt{2}}(-1, 1, 0)^T$, $\\vec{u}_2 = \\dfrac{1}{\\sqrt{6}}(-1, -1, 2)^T$, $\\vec{u}_3 = \\dfrac{1}{\\sqrt{3}}(1, 1, 1)^T$."
              ),
               "justificacion_md": "Dividir cada $\\vec{v}_i$ por su norma.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 4: construir $P$ y $D$.**\n\n"
                  "$P = \\begin{bmatrix} -1/\\sqrt{2} & -1/\\sqrt{6} & 1/\\sqrt{3} \\\\ 1/\\sqrt{2} & -1/\\sqrt{6} & 1/\\sqrt{3} \\\\ 0 & 2/\\sqrt{6} & 1/\\sqrt{3} \\end{bmatrix}, \\quad D = \\begin{bmatrix} 8 & 0 & 0 \\\\ 0 & 6 & 0 \\\\ 0 & 0 & 3 \\end{bmatrix}.$\n\n"
                  "**$A = PDP^T$** (porque $P^{-1} = P^T$ al ser $P$ ortogonal)."
              ),
               "justificacion_md": "Vectores ortonormales como columnas de $P$, valores propios en el orden correspondiente en $D$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Diagonalización ortogonal con valor propio repetido",
          problema_md=(
              "Diagonalizar ortogonalmente $A = \\begin{bmatrix} 3 & -2 & 4 \\\\ -2 & 6 & 2 \\\\ 4 & 2 & 3 \\end{bmatrix}$, cuya ecuación característica es $-(\\lambda - 7)^2(\\lambda + 2) = 0$."
          ),
          pasos=[
              {"accion_md": (
                  "**Valores propios:** $\\lambda = 7$ (mult. alg. 2), $\\lambda = -2$ (mult. alg. 1).\n\n"
                  "**Espacios propios.** $E_7$: resolviendo $(A - 7I)\\vec{x} = \\vec{0}$ se obtienen dos vectores LI: $\\vec{v}_1 = (1, 0, 1)^T$ y $\\vec{v}_2 = (-1/2, 1, 0)^T$.\n\n"
                  "$E_{-2}$: $\\vec{v}_3 = (-1, -1/2, 1)^T$."
              ),
               "justificacion_md": "Por el teorema espectral, $\\dim E_7 = 2$ (mult. alg.). $\\vec{v}_3$ es automáticamente ortogonal a $E_7$, pero $\\vec{v}_1, \\vec{v}_2$ NO son ortogonales entre sí.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar Gram-Schmidt dentro de $E_7$:**\n\n"
                  "$\\vec{z}_2 = \\vec{v}_2 - \\dfrac{\\vec{v}_2\\cdot\\vec{v}_1}{\\vec{v}_1\\cdot\\vec{v}_1}\\vec{v}_1 = (-1/2, 1, 0)^T - \\dfrac{-1/2}{2}(1, 0, 1)^T = (-1/4, 1, 1/4)^T.$\n\n"
                  "Escalando: $\\vec{z}_2' = (-1, 4, 1)^T$."
              ),
               "justificacion_md": "**Importante:** dentro de un espacio propio repetido hay que ortogonalizar manualmente; entre espacios propios distintos la ortogonalidad es automática.",
               "es_resultado": False},
              {"accion_md": (
                  "**Normalizar:**\n\n"
                  "$\\vec{u}_1 = \\dfrac{1}{\\sqrt{2}}(1, 0, 1)^T$, $\\vec{u}_2 = \\dfrac{1}{\\sqrt{18}}(-1, 4, 1)^T$, $\\vec{u}_3 = \\dfrac{1}{3}(-2, -1, 2)^T$ (normalizando $(-1, -1/2, 1)$ se obtiene $(-2/3, -1/3, 2/3)^T$).\n\n"
                  "$P = \\begin{bmatrix} 1/\\sqrt{2} & -1/\\sqrt{18} & -2/3 \\\\ 0 & 4/\\sqrt{18} & -1/3 \\\\ 1/\\sqrt{2} & 1/\\sqrt{18} & 2/3 \\end{bmatrix}, \\quad D = \\begin{bmatrix} 7 & 0 & 0 \\\\ 0 & 7 & 0 \\\\ 0 & 0 & -2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Por el teorema, $\\vec{u}_3 \\perp \\vec{u}_1, \\vec{u}_2$ — verificable.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Descomposición espectral",
          body_md=(
              "Sea $A = PDP^T$ una diagonalización ortogonal con $P = [\\vec{u}_1\\ \\cdots\\ \\vec{u}_n]$ (base ortonormal de vectores propios) y valores propios $\\lambda_1, \\ldots, \\lambda_n$ en la diagonal de $D$. Entonces:\n\n"
              "$$\\boxed{A = \\lambda_1 \\vec{u}_1 \\vec{u}_1^T + \\lambda_2 \\vec{u}_2 \\vec{u}_2^T + \\cdots + \\lambda_n \\vec{u}_n \\vec{u}_n^T.}$$\n\n"
              "Esta es la **descomposición espectral** de $A$.\n\n"
              "**Interpretación geométrica:** cada $\\vec{u}_j \\vec{u}_j^T$ es una **matriz de proyección de rango 1** sobre la recta generada por $\\vec{u}_j$. La descomposición expresa $A$ como **combinación lineal ponderada** de proyecciones sobre cada dirección propia, con pesos los valores propios.\n\n"
              "**Notación común:** $A = \\sum_{j=1}^n \\lambda_j P_j$ con $P_j = \\vec{u}_j \\vec{u}_j^T$."
          )),

        b("ejemplo_resuelto",
          titulo="Descomposición espectral $2\\times 2$",
          problema_md=(
              "Construir la descomposición espectral de $A = \\begin{bmatrix} 7 & 2 \\\\ 2 & 4 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Valores propios: $(7-\\lambda)(4-\\lambda) - 4 = \\lambda^2 - 11\\lambda + 24 = (\\lambda - 8)(\\lambda - 3) = 0 \\Rightarrow \\lambda_1 = 8, \\lambda_2 = 3$.\n\n"
                  "Vectores propios unitarios: $\\vec{u}_1 = (2/\\sqrt{5}, 1/\\sqrt{5})^T$ para $\\lambda = 8$, $\\vec{u}_2 = (-1/\\sqrt{5}, 2/\\sqrt{5})^T$ para $\\lambda = 3$."
              ),
               "justificacion_md": "Verificación: $\\vec{u}_1\\cdot\\vec{u}_2 = -2/5 + 2/5 = 0$ ✓.",
               "es_resultado": False},
              {"accion_md": (
                  "Calculamos las proyecciones de rango 1:\n\n"
                  "$\\vec{u}_1 \\vec{u}_1^T = \\dfrac{1}{5}\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}[2\\ 1] = \\dfrac{1}{5}\\begin{bmatrix} 4 & 2 \\\\ 2 & 1 \\end{bmatrix}$.\n\n"
                  "$\\vec{u}_2 \\vec{u}_2^T = \\dfrac{1}{5}\\begin{bmatrix} 1 & -2 \\\\ -2 & 4 \\end{bmatrix}$."
              ),
               "justificacion_md": "Cada $\\vec{u}_j\\vec{u}_j^T$ es una matriz simétrica $2 \\times 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Descomposición espectral:**\n\n"
                  "$A = 8\\vec{u}_1\\vec{u}_1^T + 3\\vec{u}_2\\vec{u}_2^T = \\dfrac{8}{5}\\begin{bmatrix} 4 & 2 \\\\ 2 & 1 \\end{bmatrix} + \\dfrac{3}{5}\\begin{bmatrix} 1 & -2 \\\\ -2 & 4 \\end{bmatrix}.$\n\n"
                  "Verificación: $\\dfrac{1}{5}\\begin{bmatrix} 32 + 3 & 16 - 6 \\\\ 16 - 6 & 8 + 12 \\end{bmatrix} = \\dfrac{1}{5}\\begin{bmatrix} 35 & 10 \\\\ 10 & 20 \\end{bmatrix} = \\begin{bmatrix} 7 & 2 \\\\ 2 & 4 \\end{bmatrix} = A$ ✓."
              ),
               "justificacion_md": "**Lección:** $A$ se descompone como combinación lineal de matrices de proyección, ponderadas por sus valores propios.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué el teorema espectral es tan importante.**\n\n"
            "El teorema espectral dice que **toda matriz simétrica es 'esencialmente diagonal'** — solo que vista en la base equivocada. La transformación $\\vec{x} \\mapsto A\\vec{x}$ es:\n\n"
            "1. **Cambiar de base** ($P^T \\vec{x}$).\n"
            "2. **Escalar cada coordenada** independientemente (multiplicar por $D$).\n"
            "3. **Volver a la base original** ($P$ vez el resultado).\n\n"
            "**Aplicaciones inmediatas:**\n\n"
            "- **Cálculo de potencias:** $A^k = PD^kP^T$, trivial vía la diagonal.\n"
            "- **Funciones de matrices:** $f(A) = Pf(D)P^T$ donde $f(D) = \\text{diag}(f(\\lambda_i))$. Ej: $e^A, \\sqrt{A}$ (si $A$ es semidefinida positiva).\n"
            "- **Análisis de componentes principales (PCA):** los $\\vec{u}_i$ son las **direcciones principales** de variación de los datos.\n"
            "- **Vibraciones y modos normales:** los $\\vec{u}_i$ son los modos de oscilación de un sistema mecánico."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Una matriz $A$ es diagonalizable ortogonalmente $\\iff$:",
                  "opciones_md": [
                      "$A$ es invertible",
                      "$A$ tiene valores propios distintos",
                      "$A$ es simétrica ($A^T = A$)",
                      "$A$ es triangular",
                  ],
                  "correcta": "C",
                  "pista_md": "Caracterización del teorema espectral.",
                  "explicacion_md": "**$A$ simétrica.** Esta es la equivalencia central del teorema espectral.",
              },
              {
                  "enunciado_md": "Si $A$ es simétrica con valores propios $\\lambda_1, \\lambda_2, \\lambda_3$ todos distintos, sus vectores propios:",
                  "opciones_md": [
                      "Son LD",
                      "Son LI pero no necesariamente ortogonales",
                      "Son automáticamente ortogonales",
                      "Son siempre la base estándar",
                  ],
                  "correcta": "C",
                  "pista_md": "Teorema sobre valores propios distintos en matrices simétricas.",
                  "explicacion_md": "**Automáticamente ortogonales.** Por el teorema, si $\\lambda_i \\neq \\lambda_j$ y $A$ es simétrica, $\\vec{v}_i \\perp \\vec{v}_j$. **No hace falta Gram-Schmidt** entre espacios propios distintos.",
              },
              {
                  "enunciado_md": "En la descomposición espectral $A = \\sum \\lambda_i \\vec{u}_i\\vec{u}_i^T$, cada $\\vec{u}_i\\vec{u}_i^T$ es:",
                  "opciones_md": [
                      "Una matriz $1 \\times 1$ (escalar)",
                      "Matriz de **proyección de rango 1** sobre $\\text{Gen}\\{\\vec{u}_i\\}$",
                      "La inversa de $A$",
                      "El vector $\\vec{u}_i$",
                  ],
                  "correcta": "B",
                  "pista_md": "Producto exterior de un vector unitario consigo mismo.",
                  "explicacion_md": "**Matriz de proyección de rango 1.** $P = \\vec{u}\\vec{u}^T$ es idempotente, simétrica, de rango 1, y proyecta cualquier vector sobre la dirección $\\vec{u}$.",
              },
          ]),

        ej(
            "Diagonalización ortogonal $2\\times 2$",
            "Diagonaliza ortogonalmente $A = \\begin{bmatrix} 1 & 5 \\\\ 5 & 1 \\end{bmatrix}$.",
            ["Calcula valores propios. Construye $P$ y $D$ con vectores propios normalizados."],
            (
                "$\\det(A - \\lambda I) = (1-\\lambda)^2 - 25 = (\\lambda - 6)(\\lambda + 4)$. **Valores propios:** $6, -4$.\n\n"
                "$\\lambda = 6$: $\\vec{v}_1 = (1, 1)^T$. $\\lambda = -4$: $\\vec{v}_2 = (1, -1)^T$. Ortogonales ✓.\n\n"
                "Normalizando: $\\vec{u}_1 = (1, 1)^T/\\sqrt{2}$, $\\vec{u}_2 = (1, -1)^T/\\sqrt{2}$.\n\n"
                "$P = \\dfrac{1}{\\sqrt{2}}\\begin{bmatrix} 1 & 1 \\\\ 1 & -1 \\end{bmatrix}$, $D = \\begin{bmatrix} 6 & 0 \\\\ 0 & -4 \\end{bmatrix}$. **$A = PDP^T$.**"
            ),
        ),

        ej(
            "Descomposición espectral",
            "Halla la descomposición espectral de $A = \\begin{bmatrix} 5 & 4 \\\\ 4 & 5 \\end{bmatrix}$.",
            ["Calcula valores y vectores propios unitarios."],
            (
                "Valores propios: $\\lambda_1 = 9, \\lambda_2 = 1$. Vectores propios unitarios: $\\vec{u}_1 = (1, 1)^T/\\sqrt{2}$, $\\vec{u}_2 = (1, -1)^T/\\sqrt{2}$.\n\n"
                "$\\vec{u}_1\\vec{u}_1^T = \\dfrac{1}{2}\\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix}$, $\\vec{u}_2\\vec{u}_2^T = \\dfrac{1}{2}\\begin{bmatrix} 1 & -1 \\\\ -1 & 1 \\end{bmatrix}$.\n\n"
                "$A = 9\\vec{u}_1\\vec{u}_1^T + \\vec{u}_2\\vec{u}_2^T = \\dfrac{9}{2}\\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix} + \\dfrac{1}{2}\\begin{bmatrix} 1 & -1 \\\\ -1 & 1 \\end{bmatrix} = \\begin{bmatrix} 5 & 4 \\\\ 4 & 5 \\end{bmatrix}$ ✓."
            ),
        ),

        ej(
            "Diagonalización con valor propio doble",
            "Para $A = \\begin{bmatrix} 2 & 1 & 1 \\\\ 1 & 2 & 1 \\\\ 1 & 1 & 2 \\end{bmatrix}$ (simétrica), halla los valores propios y discute la diagonalización ortogonal.",
            [
                "$A = I + J$ donde $J$ es la matriz de unos. Los valores propios de $J$ son $3$ (con vector $(1,1,1)$) y $0$ (con multiplicidad 2).",
            ],
            (
                "Valores propios de $A$: $\\lambda = 1 + 3 = 4$ (vector $(1,1,1)$) y $\\lambda = 1 + 0 = 1$ (multiplicidad 2).\n\n"
                "$E_4 = \\text{Gen}\\{(1,1,1)^T\\}$. $E_1 = $ plano ortogonal a $(1,1,1)$, base ej. $\\{(1,-1,0)^T, (1,0,-1)^T\\}$ (no ortogonales entre sí).\n\n"
                "Aplicando Gram-Schmidt en $E_1$: $\\vec{v}_2' = (1, 0, -1) - \\dfrac{1}{2}(1, -1, 0) = (1/2, 1/2, -1)$. Escalando: $(1, 1, -2)$.\n\n"
                "Normalizando todo: $\\vec{u}_1 = (1,1,1)/\\sqrt{3}$, $\\vec{u}_2 = (1,-1,0)/\\sqrt{2}$, $\\vec{u}_3 = (1,1,-2)/\\sqrt{6}$. $D = \\text{diag}(4, 1, 1)$, $A = PDP^T$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Gram-Schmidt entre espacios propios distintos.** No es necesario — son automáticamente ortogonales.",
              "**Olvidar Gram-Schmidt dentro de un espacio propio con $m_g > 1$.** Las bases iniciales no son automáticamente ortogonales — hay que ortogonalizar.",
              "**Confundir $P^{-1}$ con $P^T$ en general.** Son iguales **solo cuando $P$ es ortogonal** (columnas ortonormales). Para $P$ general, $P^{-1} \\neq P^T$.",
              "**Pensar que toda matriz diagonalizable es ortogonalmente diagonalizable.** Solo si es **simétrica**. Una matriz no simétrica diagonalizable usa $P$ no ortogonal.",
              "**Confundir 'diagonalizable' (existe $A = PDP^{-1}$) con 'diagonalizable ortogonalmente' (existe $A = PDP^T$).** La segunda es estrictamente más fuerte.",
          ]),

        b("resumen",
          puntos_md=[
              "**Matriz simétrica:** $A^T = A$.",
              "**Diagonalización ortogonal:** $A = PDP^T$ con $P$ ortogonal y $D$ diagonal real.",
              "**Teorema espectral:** $A$ diag. ortog. $\\iff A$ simétrica. Las simétricas tienen valores propios reales y multiplicidad geométrica = algebraica.",
              "**Vectores propios de espacios distintos son ortogonales** (en simétricas).",
              "**Algoritmo:** valores propios $\\to$ vectores propios $\\to$ Gram-Schmidt **dentro** de cada espacio propio repetido $\\to$ normalizar $\\to$ $P, D$.",
              "**Descomposición espectral:** $A = \\sum \\lambda_i \\vec{u}_i\\vec{u}_i^T$ — combinación de proyecciones de rango 1.",
              "**Próxima lección:** **formas cuadráticas** y la conexión geométrica de las matrices simétricas.",
          ]),
    ]
    return {
        "id": "lec-al-8-1-diagonalizacion-ortogonal",
        "title": "Diagonalización ortogonal",
        "description": "Teorema espectral $A = PDP^T$ para matrices simétricas, vectores propios automáticamente ortogonales entre espacios distintos, descomposición espectral $A = \\sum \\lambda_i \\vec{u}_i\\vec{u}_i^T$.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 1,
    }


# =====================================================================
# 8.2 Formas cuadráticas
# =====================================================================
def lesson_8_2():
    blocks = [
        b("texto", body_md=(
            "Una **forma cuadrática** es una función $Q(\\vec{x}) = \\vec{x}^T A \\vec{x}$ con $A$ simétrica. "
            "Generaliza expresiones del tipo $ax^2 + bxy + cy^2$ a $\\mathbb{R}^n$ y aparece naturalmente en:\n\n"
            "- **Geometría:** ecuaciones de cónicas y cuádricas.\n"
            "- **Optimización:** comportamiento de funciones cerca de un punto crítico (Hessiano).\n"
            "- **Estadística:** distancia de Mahalanobis, elipses de confianza.\n"
            "- **Mecánica:** energías cinética y potencial, momentos de inercia.\n"
            "- **Economía:** funciones de utilidad cuadráticas.\n\n"
            "El **teorema de los ejes principales** dice que mediante un cambio de variable ortogonal $\\vec{x} = P\\vec{y}$, "
            "toda forma cuadrática se reduce a una **suma de cuadrados** $\\sum \\lambda_i y_i^2$ — sin productos cruzados. "
            "Los $\\lambda_i$ son los valores propios de $A$, y las direcciones de los ejes son los vectores propios.\n\n"
            "Al terminar:\n\n"
            "- Construyes $A$ desde una forma cuadrática y viceversa.\n"
            "- Aplicas el cambio de variable $\\vec{x} = P\\vec{y}$ para eliminar productos cruzados.\n"
            "- **Clasificas** formas cuadráticas usando los **valores propios** (positiva definida, negativa definida, indefinida)."
        )),

        b("definicion",
          titulo="Forma cuadrática",
          body_md=(
              "Una **forma cuadrática** en $\\mathbb{R}^n$ es una función $Q : \\mathbb{R}^n \\to \\mathbb{R}$ definida por\n\n"
              "$$\\boxed{Q(\\vec{x}) = \\vec{x}^T A \\vec{x},}$$\n\n"
              "donde $A \\in \\mathbb{R}^{n \\times n}$ es una matriz **simétrica** llamada **matriz de la forma cuadrática**.\n\n"
              "**Cómo construir $A$ desde $Q$:**\n\n"
              "- Coeficientes de los términos cuadrados $x_i^2$ van en la **diagonal** $a_{ii}$.\n"
              "- Coeficientes de los términos cruzados $c\\,x_i x_j$ se **dividen en partes iguales** entre las posiciones simétricas: $a_{ij} = a_{ji} = c/2$.\n\n"
              "**Ejemplo más simple:** $Q(\\vec{x}) = \\|\\vec{x}\\|^2 = \\vec{x}^T \\vec{x}$ (matriz de la forma cuadrática es $I_n$)."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular $\\vec{x}^T A \\vec{x}$",
          problema_md=(
              "Para $\\vec{x} = (x_1, x_2)^T$, calcula $\\vec{x}^T A \\vec{x}$ con (a) $A = \\begin{bmatrix} 4 & 0 \\\\ 0 & 3 \\end{bmatrix}$ y (b) $A = \\begin{bmatrix} 3 & -2 \\\\ -2 & 7 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $\\vec{x}^T A \\vec{x} = [x_1\\ x_2]\\begin{bmatrix} 4 & 0 \\\\ 0 & 3 \\end{bmatrix}\\begin{bmatrix} x_1 \\\\ x_2 \\end{bmatrix} = 4x_1^2 + 3x_2^2.$"
              ),
               "justificacion_md": "**Sin productos cruzados** — porque $A$ es diagonal.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $\\vec{x}^T A \\vec{x} = [x_1\\ x_2]\\begin{bmatrix} 3 & -2 \\\\ -2 & 7 \\end{bmatrix}\\begin{bmatrix} x_1 \\\\ x_2 \\end{bmatrix} = 3x_1^2 - 2x_1x_2 - 2x_2x_1 + 7x_2^2 = 3x_1^2 - 4x_1x_2 + 7x_2^2.$"
              ),
               "justificacion_md": "Los términos cruzados $-4x_1x_2$ provienen de $a_{12} = a_{21} = -2$, que sumados dan el coeficiente $-4$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="De forma cuadrática a matriz",
          problema_md=(
              "Escribir $Q(\\vec{x}) = 5x_1^2 + 3x_2^2 + 2x_3^2 - x_1 x_2 + 8 x_2 x_3$ como $\\vec{x}^T A \\vec{x}$."
          ),
          pasos=[
              {"accion_md": (
                  "Diagonal de $A$: coeficientes de $x_i^2$ $\\Rightarrow a_{11} = 5, a_{22} = 3, a_{33} = 2$.\n\n"
                  "Términos cruzados se dividen en partes iguales:\n\n"
                  "- $-x_1 x_2$ $\\Rightarrow a_{12} = a_{21} = -1/2$.\n"
                  "- $8 x_2 x_3$ $\\Rightarrow a_{23} = a_{32} = 4$.\n"
                  "- No hay $x_1 x_3$ $\\Rightarrow a_{13} = a_{31} = 0$."
              ),
               "justificacion_md": "Cuidado con dividir entre $2$ los coeficientes de los productos cruzados.",
               "es_resultado": False},
              {"accion_md": (
                  "$A = \\begin{bmatrix} 5 & -1/2 & 0 \\\\ -1/2 & 3 & 4 \\\\ 0 & 4 & 2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "**$A$ es simétrica** por construcción.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Cambio de variable ortogonal",
          body_md=(
              "Sea $\\vec{x} = P\\vec{y}$ con $P$ una matriz invertible (cambio de base, lección 5.6). Sustituyendo:\n\n"
              "$$Q(\\vec{x}) = \\vec{x}^T A \\vec{x} = (P\\vec{y})^T A (P\\vec{y}) = \\vec{y}^T (P^T A P) \\vec{y}.$$\n\n"
              "La nueva matriz de la forma cuadrática es $P^T A P$.\n\n"
              "**Caso clave: $P$ ortogonal.** Si $A$ es simétrica, por el teorema espectral existe $P$ **ortogonal** tal que $P^T A P = D$ es **diagonal** (con los valores propios de $A$).\n\n"
              "El cambio de variable $\\vec{x} = P\\vec{y}$ con esa $P$ produce\n\n"
              "$$\\boxed{\\vec{x}^T A \\vec{x} = \\vec{y}^T D \\vec{y} = \\lambda_1 y_1^2 + \\lambda_2 y_2^2 + \\cdots + \\lambda_n y_n^2.}$$\n\n"
              "**Resultado:** **toda forma cuadrática se reduce a suma ponderada de cuadrados**, sin productos cruzados, eligiendo bien las coordenadas."
          )),

        b("teorema",
          nombre="Teorema de los ejes principales",
          enunciado_md=(
              "Sea $A \\in \\mathbb{R}^{n \\times n}$ simétrica. Existe un cambio de variable **ortogonal** $\\vec{x} = P\\vec{y}$ que transforma la forma cuadrática $\\vec{x}^T A \\vec{x}$ en una forma cuadrática $\\vec{y}^T D \\vec{y}$ **sin productos cruzados** (i.e., $D$ es diagonal con los valores propios de $A$).\n\n"
              "Las **columnas de $P$** se llaman **ejes principales** de la forma cuadrática $\\vec{x}^T A \\vec{x}$. El vector $\\vec{y}$ es el vector de coordenadas de $\\vec{x}$ respecto a la base ortonormal de $\\mathbb{R}^n$ formada por esos ejes principales.\n\n"
              "**Geometría:** la curva o superficie definida por $\\vec{x}^T A \\vec{x} = c$ tiene sus **ejes geométricos** alineados con los vectores propios de $A$, y los semiejes son determinados por los valores propios."
          )),

        b("ejemplo_resuelto",
          titulo="Eliminar productos cruzados",
          problema_md=(
              "Realiza un cambio de variable que transforme $Q(\\vec{x}) = x_1^2 - 8 x_1 x_2 - 5 x_2^2$ en una forma sin productos cruzados."
          ),
          pasos=[
              {"accion_md": (
                  "Matriz de la forma: $A = \\begin{bmatrix} 1 & -4 \\\\ -4 & -5 \\end{bmatrix}$.\n\n"
                  "Valores propios: $\\det(A - \\lambda I) = (1-\\lambda)(-5-\\lambda) - 16 = \\lambda^2 + 4\\lambda - 21 = (\\lambda - 3)(\\lambda + 7)$. **$\\lambda_1 = 3, \\lambda_2 = -7$.**"
              ),
               "justificacion_md": "Diagonalizar $A$.",
               "es_resultado": False},
              {"accion_md": (
                  "Vectores propios unitarios:\n\n"
                  "$\\lambda = 3$: $\\dfrac{1}{\\sqrt{5}}(2, -1)^T$. $\\lambda = -7$: $\\dfrac{1}{\\sqrt{5}}(1, 2)^T$.\n\n"
                  "$P = \\dfrac{1}{\\sqrt{5}}\\begin{bmatrix} 2 & 1 \\\\ -1 & 2 \\end{bmatrix}$, $D = \\begin{bmatrix} 3 & 0 \\\\ 0 & -7 \\end{bmatrix}$. $A = PDP^T$."
              ),
               "justificacion_md": "$P$ ortogonal porque vectores propios de simétrica con $\\lambda$ distintos son ortogonales.",
               "es_resultado": False},
              {"accion_md": (
                  "Cambio de variable $\\vec{x} = P\\vec{y}$:\n\n"
                  "$$\\boxed{Q(\\vec{x}) = \\vec{y}^T D \\vec{y} = 3 y_1^2 - 7 y_2^2.}$$\n\n"
                  "**Resultado limpio sin productos cruzados.** Geométricamente, $Q(\\vec{x}) = c$ es una hipérbola en las coordenadas $\\vec{y}$ (signos opuestos)."
              ),
               "justificacion_md": "**Lección poderosa:** elegir la base correcta convierte cualquier expresión cuadrática en una suma simple de cuadrados.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Eliminar producto cruzado en una elipse",
          problema_md=(
              "La elipse tiene ecuación $5x_1^2 - 4x_1 x_2 + 5x_2^2 = 48$. Encuentra un cambio de variable que elimine el producto cruzado y describe geométricamente."
          ),
          pasos=[
              {"accion_md": (
                  "Matriz: $A = \\begin{bmatrix} 5 & -2 \\\\ -2 & 5 \\end{bmatrix}$.\n\n"
                  "Valores propios: $(5-\\lambda)^2 - 4 = 0 \\Rightarrow \\lambda - 5 = \\pm 2 \\Rightarrow \\lambda = 3, 7$."
              ),
               "justificacion_md": "Cálculo directo del polinomio característico.",
               "es_resultado": False},
              {"accion_md": (
                  "Vectores propios unitarios: $\\vec{u}_1 = (1, 1)^T/\\sqrt{2}$ para $\\lambda = 3$, $\\vec{u}_2 = (-1, 1)^T/\\sqrt{2}$ para $\\lambda = 7$.\n\n"
                  "$P = \\dfrac{1}{\\sqrt{2}}\\begin{bmatrix} 1 & -1 \\\\ 1 & 1 \\end{bmatrix}$, **rotación de $45°$**.\n\n"
                  "Cambio $\\vec{x} = P\\vec{y}$: $\\vec{y}^T D \\vec{y} = 3 y_1^2 + 7 y_2^2 = 48$."
              ),
               "justificacion_md": "$P$ es la matriz de una rotación $45°$ — los ejes de la elipse están a $45°$ de los ejes coordenados originales.",
               "es_resultado": False},
              {"accion_md": (
                  "Dividiendo entre $48$: $\\dfrac{y_1^2}{16} + \\dfrac{y_2^2}{48/7} = 1$.\n\n"
                  "**Es una elipse en posición estándar** (en coordenadas $\\vec{y}$) con semiejes $a = 4$ (eje $y_1$, alineado con $\\vec{u}_1$) y $b = \\sqrt{48/7} = 4\\sqrt{3/7}$ (eje $y_2$, alineado con $\\vec{u}_2$)."
              ),
               "justificacion_md": "**Lección geométrica:** los **ejes principales** $\\vec{u}_1, \\vec{u}_2$ son los **ejes mayor/menor** de la elipse, y los semiejes son $\\sqrt{c/\\lambda_i}$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Clasificación de formas cuadráticas",
          body_md=(
              "Una forma cuadrática $Q(\\vec{x}) = \\vec{x}^T A \\vec{x}$ es:\n\n"
              "- **Positiva definida** si $Q(\\vec{x}) > 0$ para todo $\\vec{x} \\neq \\vec{0}$.\n"
              "- **Negativa definida** si $Q(\\vec{x}) < 0$ para todo $\\vec{x} \\neq \\vec{0}$.\n"
              "- **Positiva semidefinida** si $Q(\\vec{x}) \\geq 0$ para todo $\\vec{x}$ (con $Q$ posiblemente nulo en algunos $\\vec{x} \\neq \\vec{0}$).\n"
              "- **Negativa semidefinida** si $Q(\\vec{x}) \\leq 0$ para todo $\\vec{x}$.\n"
              "- **Indefinida** si toma tanto valores positivos como negativos.\n\n"
              "**Geometría:** $Q(\\vec{x}) = c$ representa, según el caso:\n\n"
              "- **Pos./neg. definida:** elipses (acotadas) en $\\mathbb{R}^2$, elipsoides en $\\mathbb{R}^3$.\n"
              "- **Indefinida:** hipérbolas, sillas (paraboloide hiperbólico)."
          )),

        b("teorema",
          nombre="Clasificación por valores propios",
          enunciado_md=(
              "Sea $A \\in \\mathbb{R}^{n \\times n}$ simétrica con valores propios $\\lambda_1, \\ldots, \\lambda_n$. La forma cuadrática $Q(\\vec{x}) = \\vec{x}^T A \\vec{x}$ es:\n\n"
              "**Positiva definida** $\\iff$ todos los $\\lambda_i > 0$.\n\n"
              "**Negativa definida** $\\iff$ todos los $\\lambda_i < 0$.\n\n"
              "**Positiva semidefinida** $\\iff$ todos los $\\lambda_i \\geq 0$.\n\n"
              "**Negativa semidefinida** $\\iff$ todos los $\\lambda_i \\leq 0$.\n\n"
              "**Indefinida** $\\iff$ $A$ tiene **valores propios positivos y negativos**."
          ),
          demostracion_md=(
              "Aplicar el teorema de los ejes principales: $Q(\\vec{x}) = \\sum \\lambda_i y_i^2$. Esta suma es siempre $> 0$ para $\\vec{y} \\neq \\vec{0}$ $\\iff$ todos los $\\lambda_i > 0$. Análogo para los demás casos. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Clasificación",
          problema_md=(
              "¿Es $Q(\\vec{x}) = 3x_1^2 + 2x_2^2 + x_3^2 + 4x_1 x_2 + 4 x_2 x_3$ positiva definida?"
          ),
          pasos=[
              {"accion_md": (
                  "Matriz: $A = \\begin{bmatrix} 3 & 2 & 0 \\\\ 2 & 2 & 2 \\\\ 0 & 2 & 1 \\end{bmatrix}$ (cuidado con los $4$ que se dividen en $2$ y $2$).\n\n"
                  "Polinomio característico: $\\det(A - \\lambda I)$. Calculando: $-\\lambda^3 + 6\\lambda^2 - 3\\lambda - 10 = -(\\lambda - 5)(\\lambda - 2)(\\lambda + 1)$."
              ),
               "justificacion_md": "Cómputo del determinante (puede expandir por la primera columna o tercera fila).",
               "es_resultado": False},
              {"accion_md": (
                  "**Valores propios:** $5, 2, -1$. Hay un valor propio **negativo** ($-1$) $\\Rightarrow$ $Q$ es **indefinida** (no positiva definida).\n\n"
                  "**Ejemplo concreto:** evaluando $Q$ en el vector propio para $\\lambda = -1$ se obtiene $Q < 0$, mientras que $Q(\\vec{e}_1) = 3 > 0$."
              ),
               "justificacion_md": "**Lección:** los signos individuales de los coeficientes de $Q$ **NO** determinan el carácter — hay que mirar los valores propios.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para $Q(\\vec{x}) = x_1^2 - 4x_1 x_2 + x_2^2$, la matriz $A$ es:",
                  "opciones_md": [
                      "$\\begin{bmatrix} 1 & -4 \\\\ -4 & 1 \\end{bmatrix}$",
                      "$\\begin{bmatrix} 1 & -2 \\\\ -2 & 1 \\end{bmatrix}$",
                      "$\\begin{bmatrix} 1 & 0 \\\\ -4 & 1 \\end{bmatrix}$",
                      "$\\begin{bmatrix} 1 & 4 \\\\ 4 & 1 \\end{bmatrix}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Coeficiente del cruzado se divide en mitades.",
                  "explicacion_md": "**$\\begin{bmatrix} 1 & -2 \\\\ -2 & 1 \\end{bmatrix}$.** Los $-4 x_1 x_2$ se dividen en $a_{12} = a_{21} = -2$.",
              },
              {
                  "enunciado_md": "Si los valores propios de $A$ son $\\{2, 5, 3\\}$, la forma $\\vec{x}^T A \\vec{x}$ es:",
                  "opciones_md": [
                      "Indefinida",
                      "Positiva definida",
                      "Negativa definida",
                      "Semidefinida",
                  ],
                  "correcta": "B",
                  "pista_md": "Todos los $\\lambda_i > 0$.",
                  "explicacion_md": "**Positiva definida.** Los tres valores propios son positivos $\\Rightarrow Q(\\vec{x}) > 0$ para todo $\\vec{x} \\neq \\vec{0}$.",
              },
              {
                  "enunciado_md": "Si la elipse $\\vec{x}^T A \\vec{x} = c$ tiene sus ejes alineados con los ejes coordenados estándar:",
                  "opciones_md": [
                      "$A$ es triangular",
                      "$A$ es **diagonal** (sin productos cruzados)",
                      "$A$ es la identidad",
                      "$c = 0$",
                  ],
                  "correcta": "B",
                  "pista_md": "Sin productos cruzados $\\iff$ matriz diagonal.",
                  "explicacion_md": "**$A$ diagonal.** En general, $A$ no diagonal corresponde a una elipse rotada — los ejes principales (vectores propios) están rotados respecto a los ejes coordenados.",
              },
          ]),

        ej(
            "Construir matriz de forma cuadrática",
            "Escribe $Q(\\vec{x}) = 2x_1^2 - 3x_2^2 + x_3^2 + 6x_1 x_3$ como $\\vec{x}^T A \\vec{x}$.",
            ["Coeficientes diagonales y mitades de los cruzados."],
            (
                "$A = \\begin{bmatrix} 2 & 0 & 3 \\\\ 0 & -3 & 0 \\\\ 3 & 0 & 1 \\end{bmatrix}$. (Sin término $x_1 x_2$ ni $x_2 x_3$.)"
            ),
        ),

        ej(
            "Reducir forma cuadrática a ejes principales",
            "Para $Q(\\vec{x}) = 3x_1^2 + 2x_2^2 + 3x_3^2 + 2x_1 x_3$, halla un cambio de variable que la diagonalice.",
            ["Encuentra valores y vectores propios de la matriz simétrica asociada."],
            (
                "$A = \\begin{bmatrix} 3 & 0 & 1 \\\\ 0 & 2 & 0 \\\\ 1 & 0 & 3 \\end{bmatrix}$. Valores propios: $\\lambda = 4, 2, 2$.\n\n"
                "$E_4 = \\text{Gen}\\{(1, 0, 1)/\\sqrt{2}\\}$. $E_2 = \\text{Gen}\\{(0, 1, 0), (1, 0, -1)/\\sqrt{2}\\}$ (LI y ortogonales por elección).\n\n"
                "$P = \\begin{bmatrix} 1/\\sqrt{2} & 0 & 1/\\sqrt{2} \\\\ 0 & 1 & 0 \\\\ 1/\\sqrt{2} & 0 & -1/\\sqrt{2} \\end{bmatrix}$. Cambio $\\vec{x} = P\\vec{y}$ da $Q = 4y_1^2 + 2y_2^2 + 2y_3^2$ (positiva definida)."
            ),
        ),

        ej(
            "Clasificación rápida",
            "Clasifica $Q(\\vec{x}) = -x_1^2 - 4x_2^2 + 2x_1 x_2$.",
            ["Halla la matriz y sus valores propios."],
            (
                "$A = \\begin{bmatrix} -1 & 1 \\\\ 1 & -4 \\end{bmatrix}$. $\\det(A - \\lambda I) = (-1-\\lambda)(-4-\\lambda) - 1 = \\lambda^2 + 5\\lambda + 3$.\n\n"
                "$\\lambda = (-5 \\pm \\sqrt{13})/2 \\approx -0.7, -4.3$. **Ambos negativos** $\\Rightarrow$ **negativa definida**."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar dividir entre 2** los coeficientes de productos cruzados al construir $A$.",
              "**Pensar que coeficientes positivos $\\Rightarrow$ positiva definida.** Falso — depende de los **valores propios**, no de los coeficientes individuales.",
              "**Aplicar cambio de variable no ortogonal.** Solo $P$ ortogonal preserva la geometría (longitudes y ángulos). Cambios no ortogonales distorsionan.",
              "**Confundir 'positiva definida' con 'todas las entradas positivas'.** Son condiciones distintas.",
              "**No identificar formas indefinidas como sillas (paraboloides hiperbólicos).** Una indefinida tiene 'caras' positivas y negativas en distintas direcciones.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma cuadrática:** $Q(\\vec{x}) = \\vec{x}^T A \\vec{x}$ con $A$ simétrica.",
              "**Construir $A$:** diagonales = coeficientes $x_i^2$; cruzados $c\\,x_i x_j$ se dividen $c/2$ en $a_{ij}$ y $a_{ji}$.",
              "**Cambio de variable ortogonal** $\\vec{x} = P\\vec{y}$ transforma $A \\to P^TAP$.",
              "**Teorema de ejes principales:** $A$ simétrica $\\Rightarrow$ existe $P$ ortogonal con $P^TAP = D$ diagonal $\\Rightarrow Q(\\vec{x}) = \\sum \\lambda_i y_i^2$ sin productos cruzados.",
              "**Clasificación por valores propios:** positiva def. ($\\lambda_i > 0$), negativa def. ($\\lambda_i < 0$), indefinida (signos mixtos).",
              "**Geometría:** $Q(\\vec{x}) = c$ es elipsoide (definida), hiperboloide (indefinida); ejes geométricos = ejes principales = vectores propios.",
              "**Próxima lección:** **SVD** — generalización de la diagonalización ortogonal a matrices **rectangulares**.",
          ]),
    ]
    return {
        "id": "lec-al-8-2-formas-cuadraticas",
        "title": "Formas cuadráticas",
        "description": "Forma cuadrática $Q(\\vec{x}) = \\vec{x}^T A \\vec{x}$, teorema de los ejes principales, clasificación (positiva/negativa definida, indefinida) por los valores propios.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# =====================================================================
# 8.3 Descomposición en Valores Singulares (SVD)
# =====================================================================
def lesson_8_3():
    blocks = [
        b("texto", body_md=(
            "La **descomposición en valores singulares (SVD, por sus siglas en inglés)** es probablemente "
            "**la factorización más importante de toda el álgebra lineal aplicada**. A diferencia de la "
            "diagonalización (limitada a matrices cuadradas diagonalizables), la **SVD existe para CUALQUIER "
            "matriz $A \\in \\mathbb{R}^{m\\times n}$** — incluyendo rectangulares y singulares.\n\n"
            "$$A = U \\Sigma V^T$$\n\n"
            "donde $U$ y $V$ son **ortogonales** y $\\Sigma$ es **diagonal rectangular** con los **valores singulares** "
            "$\\sigma_1 \\geq \\sigma_2 \\geq \\cdots \\geq 0$ en su diagonal.\n\n"
            "**Aplicaciones de la SVD:**\n\n"
            "- **Compresión de imágenes y datos:** quedarse con los $k$ valores singulares más grandes.\n"
            "- **Reducción de dimensionalidad (PCA):** los vectores singulares revelan las direcciones de mayor varianza.\n"
            "- **Sistemas mal condicionados:** SVD da el 'pseudoinverso' de Moore-Penrose.\n"
            "- **Recuperación de señales:** denoising, deblurring.\n"
            "- **Sistemas recomendadores:** factorización de matrices de usuario × items.\n"
            "- **Visión por computador, NLP, ML, ...** Casi cualquier algoritmo moderno usa SVD en algún nivel.\n\n"
            "Al terminar:\n\n"
            "- Defines y calculas **valores singulares** $\\sigma_i = \\sqrt{\\lambda_i(A^TA)}$.\n"
            "- Aplicas el **algoritmo SVD en 3 pasos** para construir $U, \\Sigma, V$.\n"
            "- Conoces el significado geométrico (mapear esfera unitaria a un elipsoide)."
        )),

        b("intuicion", body_md=(
            "**Motivación geométrica.** La transformación $\\vec{x} \\mapsto A\\vec{x}$ con $A \\in \\mathbb{R}^{m\\times n}$ envía la **esfera unitaria** $\\{\\vec{x} \\in \\mathbb{R}^n : \\|\\vec{x}\\| = 1\\}$ a un **elipsoide** en $\\mathbb{R}^m$. Las **longitudes de los semiejes** del elipsoide son los **valores singulares** $\\sigma_i$, y los **vectores propios de $A^TA$** indican las direcciones del dominio que se mapean a los semiejes.\n\n"
            "**Ejemplo $\\mathbb{R}^3 \\to \\mathbb{R}^2$:** una matriz $A$ de $2 \\times 3$ aplicada a la esfera $\\{\\|\\vec{x}\\| = 1\\} \\subset \\mathbb{R}^3$ produce una **elipse** en $\\mathbb{R}^2$. La SVD identifica:\n\n"
            "- $\\vec{v}_1$: dirección en $\\mathbb{R}^3$ que se mapea al **eje mayor** de la elipse.\n"
            "- $\\vec{v}_2$: dirección al **eje menor**.\n"
            "- $\\vec{v}_3$: dirección que **se mapea al cero** (núcleo, $\\sigma_3 = 0$).\n"
            "- $\\sigma_1, \\sigma_2$: **longitudes** de los semiejes."
        )),

        b("definicion",
          titulo="Valores singulares",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{m \\times n}$. La matriz $A^T A \\in \\mathbb{R}^{n \\times n}$ es **simétrica** y **semidefinida positiva** (todos sus valores propios $\\geq 0$). Sean $\\lambda_1 \\geq \\lambda_2 \\geq \\cdots \\geq \\lambda_n \\geq 0$ sus valores propios ordenados.\n\n"
              "Los **valores singulares** de $A$ son\n\n"
              "$$\\boxed{\\sigma_i = \\sqrt{\\lambda_i}, \\qquad i = 1, \\ldots, n,}$$\n\n"
              "ordenados $\\sigma_1 \\geq \\sigma_2 \\geq \\cdots \\geq \\sigma_n \\geq 0$.\n\n"
              "**Hechos clave:**\n\n"
              "- Los $\\sigma_i$ son siempre **reales y no negativos**.\n"
              "- El **número de valores singulares no nulos** ($r$) es igual al **rango de $A$**.\n"
              "- Si $\\{\\vec{v}_1, \\ldots, \\vec{v}_n\\}$ es base ortonormal de vectores propios de $A^T A$, entonces $\\|A\\vec{v}_i\\| = \\sigma_i$.\n"
              "- $\\{A\\vec{v}_1, \\ldots, A\\vec{v}_r\\}$ es base ortogonal de $\\text{Col}(A)$."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular valores singulares",
          problema_md=(
              "Halla los valores singulares de $A = \\begin{bmatrix} 4 & 11 & 14 \\\\ 8 & 7 & -2 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A^T A = \\begin{bmatrix} 4 & 8 \\\\ 11 & 7 \\\\ 14 & -2 \\end{bmatrix}\\begin{bmatrix} 4 & 11 & 14 \\\\ 8 & 7 & -2 \\end{bmatrix} = \\begin{bmatrix} 80 & 100 & 40 \\\\ 100 & 170 & 140 \\\\ 40 & 140 & 200 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Producto $3\\times 3$ — matriz simétrica.",
               "es_resultado": False},
              {"accion_md": (
                  "Valores propios de $A^TA$ (cómputo omitido): $\\lambda_1 = 360, \\lambda_2 = 90, \\lambda_3 = 0$."
              ),
               "justificacion_md": "Como $A$ es $2\\times 3$ con rango $2$, $A^TA$ es $3\\times 3$ con rango $2$ $\\Rightarrow$ uno de sus valores propios es $0$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Valores singulares:**\n\n"
                  "$\\sigma_1 = \\sqrt{360} = 6\\sqrt{10} \\approx 18.97$, $\\sigma_2 = \\sqrt{90} = 3\\sqrt{10} \\approx 9.49$, $\\sigma_3 = 0$.\n\n"
                  "**Geometría:** $A$ aplicada a la esfera unitaria de $\\mathbb{R}^3$ produce una **elipse** en $\\mathbb{R}^2$ con semiejes $6\\sqrt{10}$ y $3\\sqrt{10}$ (la dirección $\\vec{v}_3$ colapsa al origen)."
              ),
               "justificacion_md": "**Lección:** $\\sigma_i = 0 \\iff A\\vec{v}_i = \\vec{0} \\iff \\vec{v}_i \\in \\text{Nul}(A)$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Descomposición en valores singulares (SVD)",
          enunciado_md=(
              "Para toda matriz $A \\in \\mathbb{R}^{m \\times n}$, existe una factorización\n\n"
              "$$\\boxed{A = U \\Sigma V^T,}$$\n\n"
              "donde:\n\n"
              "- **$U \\in \\mathbb{R}^{m \\times m}$ es ortogonal** ($U^T U = I_m$). Sus columnas $\\vec{u}_1, \\ldots, \\vec{u}_m$ son los **vectores singulares izquierdos**.\n"
              "- **$V \\in \\mathbb{R}^{n \\times n}$ es ortogonal** ($V^T V = I_n$). Sus columnas $\\vec{v}_1, \\ldots, \\vec{v}_n$ son los **vectores singulares derechos** y forman una base ortonormal de vectores propios de $A^TA$.\n"
              "- **$\\Sigma \\in \\mathbb{R}^{m \\times n}$ es 'diagonal rectangular':** las primeras $r = \\text{rango}(A)$ entradas de la diagonal son los valores singulares no nulos $\\sigma_1 \\geq \\cdots \\geq \\sigma_r > 0$, y el resto son ceros.\n\n"
              "**SVD existe para cualquier matriz** — sin condiciones. Esto la hace la factorización más general y útil del álgebra lineal."
          ),
          demostracion_md=(
              "**Construcción explícita:**\n\n"
              "1. Diagonalizar ortogonalmente $A^TA = V D V^T$ con $V$ ortogonal y $D = \\text{diag}(\\lambda_1, \\ldots, \\lambda_n)$ ($\\lambda_i \\geq 0$ en orden decreciente).\n\n"
              "2. Definir $\\sigma_i = \\sqrt{\\lambda_i}$ y $\\Sigma$ como matriz diagonal rectangular con los $\\sigma_i$.\n\n"
              "3. Para $i$ con $\\sigma_i > 0$: definir $\\vec{u}_i = A\\vec{v}_i / \\sigma_i$. Esto da vectores ortonormales en $\\text{Col}(A)$.\n\n"
              "4. Completar $\\{\\vec{u}_1, \\ldots, \\vec{u}_r\\}$ a base ortonormal $\\{\\vec{u}_1, \\ldots, \\vec{u}_m\\}$ de $\\mathbb{R}^m$ (vía Gram-Schmidt).\n\n"
              "5. Verificar $A = U\\Sigma V^T$. $\\blacksquare$"
          )),

        b("teorema",
          nombre="Algoritmo SVD",
          enunciado_md=(
              "Para construir la SVD de $A \\in \\mathbb{R}^{m\\times n}$:\n\n"
              "**Paso 1.** Calcular $A^TA$ y diagonalizarla ortogonalmente: hallar valores propios $\\lambda_1 \\geq \\lambda_2 \\geq \\cdots \\geq \\lambda_n \\geq 0$ y base ortonormal de vectores propios $\\vec{v}_1, \\ldots, \\vec{v}_n$. **Construir $V = [\\vec{v}_1\\ \\cdots\\ \\vec{v}_n]$.**\n\n"
              "**Paso 2.** Calcular valores singulares $\\sigma_i = \\sqrt{\\lambda_i}$ y construir $\\Sigma$ diagonal rectangular $m \\times n$ con los $\\sigma_i$.\n\n"
              "**Paso 3.** Para cada $i$ con $\\sigma_i > 0$ ($i = 1, \\ldots, r$), calcular $\\vec{u}_i = \\dfrac{1}{\\sigma_i}A\\vec{v}_i$. Si $r < m$, **completar** $\\{\\vec{u}_1, \\ldots, \\vec{u}_r\\}$ a base ortonormal de $\\mathbb{R}^m$ usando Gram-Schmidt. **Construir $U = [\\vec{u}_1\\ \\cdots\\ \\vec{u}_m]$.**\n\n"
              "**Verificación final:** $A = U\\Sigma V^T$."
          )),

        b("ejemplo_resuelto",
          titulo="SVD completa de matriz $2\\times 3$",
          problema_md=(
              "Construir la SVD de $A = \\begin{bmatrix} 4 & 11 & 14 \\\\ 8 & 7 & -2 \\end{bmatrix}$ (continuación del ejemplo anterior)."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1.** Vectores propios unitarios de $A^TA$ correspondientes a $\\lambda_1 = 360, \\lambda_2 = 90, \\lambda_3 = 0$:\n\n"
                  "$\\vec{v}_1 = (1/3, 2/3, 2/3)^T$, $\\vec{v}_2 = (-2/3, -1/3, 2/3)^T$, $\\vec{v}_3 = (2/3, -2/3, 1/3)^T$.\n\n"
                  "$V = \\begin{bmatrix} 1/3 & -2/3 & 2/3 \\\\ 2/3 & -1/3 & -2/3 \\\\ 2/3 & 2/3 & 1/3 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Diagonalización ortogonal de $A^TA$ — usando técnicas del cap. 8.1.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2.** Valores singulares $\\sigma_1 = 6\\sqrt{10}, \\sigma_2 = 3\\sqrt{10}, \\sigma_3 = 0$.\n\n"
                  "$\\Sigma = \\begin{bmatrix} 6\\sqrt{10} & 0 & 0 \\\\ 0 & 3\\sqrt{10} & 0 \\end{bmatrix}.$ (Diagonal rectangular $2\\times 3$.)"
              ),
               "justificacion_md": "$\\sigma_3 = 0$ no aporta una columna efectiva de $U$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3.** $\\vec{u}_i = A\\vec{v}_i/\\sigma_i$ para $i = 1, 2$:\n\n"
                  "$A\\vec{v}_1 = (4/3 + 22/3 + 28/3, 8/3 + 14/3 - 4/3)^T = (18, 6)^T$. $\\vec{u}_1 = (18, 6)^T/(6\\sqrt{10}) = (3/\\sqrt{10}, 1/\\sqrt{10})^T.$\n\n"
                  "$A\\vec{v}_2 = (-8/3 - 11/3 + 28/3, -16/3 - 7/3 - 4/3)^T = (3, -9)^T$. $\\vec{u}_2 = (3, -9)^T/(3\\sqrt{10}) = (1/\\sqrt{10}, -3/\\sqrt{10})^T.$\n\n"
                  "Como $r = 2 = m$, **no necesitamos completar con Gram-Schmidt** — $\\{\\vec{u}_1, \\vec{u}_2\\}$ ya forma base ortonormal de $\\mathbb{R}^2$."
              ),
               "justificacion_md": "Para matrices con $r = m$, $U$ se construye directamente sin pasos adicionales.",
               "es_resultado": False},
              {"accion_md": (
                  "$U = \\begin{bmatrix} 3/\\sqrt{10} & 1/\\sqrt{10} \\\\ 1/\\sqrt{10} & -3/\\sqrt{10} \\end{bmatrix}.$\n\n"
                  "**SVD final:** $A = U\\Sigma V^T$ con $U, \\Sigma, V$ construidos."
              ),
               "justificacion_md": "**Una de las descomposiciones más útiles del álgebra lineal — válida para cualquier $A$.**",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="SVD con Gram-Schmidt para completar $U$",
          problema_md=(
              "Construir la SVD de $A = \\begin{bmatrix} 1 & -1 \\\\ -2 & 2 \\\\ 2 & -2 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$A^TA = \\begin{bmatrix} 9 & -9 \\\\ -9 & 9 \\end{bmatrix}$. Valores propios: $18$ y $0$.\n\n"
                  "Vectores propios unitarios: $\\vec{v}_1 = (1, -1)^T/\\sqrt{2}$ ($\\lambda = 18$), $\\vec{v}_2 = (1, 1)^T/\\sqrt{2}$ ($\\lambda = 0$).\n\n"
                  "$V = \\dfrac{1}{\\sqrt{2}}\\begin{bmatrix} 1 & 1 \\\\ -1 & 1 \\end{bmatrix}$."
              ),
               "justificacion_md": "Diagonalización ortogonal de $A^TA$.",
               "es_resultado": False},
              {"accion_md": (
                  "Valores singulares: $\\sigma_1 = \\sqrt{18} = 3\\sqrt{2}$, $\\sigma_2 = 0$.\n\n"
                  "$\\Sigma = \\begin{bmatrix} 3\\sqrt{2} & 0 \\\\ 0 & 0 \\\\ 0 & 0 \\end{bmatrix}$ (diagonal $3\\times 2$)."
              ),
               "justificacion_md": "$\\Sigma$ es del mismo tamaño que $A$.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\vec{u}_1 = A\\vec{v}_1/\\sigma_1$.** $A\\vec{v}_1 = \\dfrac{1}{\\sqrt{2}}A(1, -1)^T = \\dfrac{1}{\\sqrt{2}}(2, -4, 4)^T = (2/\\sqrt{2}, -4/\\sqrt{2}, 4/\\sqrt{2})^T$.\n\n"
                  "$\\vec{u}_1 = \\dfrac{1}{3\\sqrt{2}}(2/\\sqrt{2}, -4/\\sqrt{2}, 4/\\sqrt{2})^T = (1/3, -2/3, 2/3)^T.$"
              ),
               "justificacion_md": "Solo un $\\sigma_i \\neq 0$, así solo construimos un $\\vec{u}_i$ vía la fórmula.",
               "es_resultado": False},
              {"accion_md": (
                  "**Completar $U$ con Gram-Schmidt.** Necesitamos $\\vec{u}_2, \\vec{u}_3$ ortonormales y ortogonales a $\\vec{u}_1$. Una elección posible:\n\n"
                  "$\\vec{u}_2 = (2/\\sqrt{5}, 1/\\sqrt{5}, 0)^T$, $\\vec{u}_3 = (-2/\\sqrt{45}, 4/\\sqrt{45}, 5/\\sqrt{45})^T$ (verificable: ortonormal con $\\vec{u}_1$).\n\n"
                  "$U = \\begin{bmatrix} 1/3 & 2/\\sqrt{5} & -2/\\sqrt{45} \\\\ -2/3 & 1/\\sqrt{5} & 4/\\sqrt{45} \\\\ 2/3 & 0 & 5/\\sqrt{45} \\end{bmatrix}.$\n\n"
                  "**SVD: $A = U\\Sigma V^T$** completa."
              ),
               "justificacion_md": "**Lección:** cuando $r < m$, hay flexibilidad en elegir $\\vec{u}_2, \\ldots, \\vec{u}_m$ (cualquier base ortonormal del complemento de $\\text{Gen}\\{\\vec{u}_1, \\ldots, \\vec{u}_r\\}$).",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Cierre del curso: la SVD como puente entre lo algebraico y lo aplicado.**\n\n"
            "La SVD reúne casi todo el álgebra lineal del curso:\n\n"
            "- **Diagonalización** (cap. 6): generalización a matrices rectangulares.\n"
            "- **Diagonalización ortogonal** (lección 8.1): $A^TA$ es simétrica $\\Rightarrow$ se diagonaliza ortogonalmente.\n"
            "- **Bases ortonormales y Gram-Schmidt** (cap. 7): $U, V$ son construidas mediante estas técnicas.\n"
            "- **Espacios fundamentales** (caps. 5, 7): $\\text{Col}\\,A, \\text{Nul}\\,A, \\text{Fil}\\,A, \\text{Nul}\\,A^T$ se leen directamente de la SVD.\n\n"
            "**Aplicación moderna concreta — compresión de imágenes.** Una imagen $A$ de tamaño $m \\times n$ puede aproximarse por $A_k = U_k \\Sigma_k V_k^T$ usando solo los $k$ valores singulares más grandes (típicamente $k \\ll \\min(m, n)$). Esto reduce drásticamente el almacenamiento mientras preserva la información esencial.\n\n"
            "**¡Felicidades por terminar el curso de Álgebra Lineal!** 🎓 Tienes ahora el lenguaje matemático que estructura prácticamente toda la matemática aplicada moderna."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La SVD $A = U\\Sigma V^T$ existe:",
                  "opciones_md": [
                      "Solo si $A$ es cuadrada e invertible",
                      "Solo si $A$ es simétrica",
                      "Para cualquier matriz $A \\in \\mathbb{R}^{m\\times n}$",
                      "Solo si $A$ es diagonalizable",
                  ],
                  "correcta": "C",
                  "pista_md": "Esa es la generalidad de la SVD.",
                  "explicacion_md": "**Para cualquier matriz.** Esta universalidad es la propiedad central que la hace tan útil.",
              },
              {
                  "enunciado_md": "Los valores singulares de $A$ son:",
                  "opciones_md": [
                      "Los valores propios de $A$",
                      "Las raíces cuadradas de los valores propios de $A^TA$",
                      "Las normas de las columnas de $A$",
                      "Los determinantes de las submatrices",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\sigma_i = \\sqrt{\\lambda_i}$ con $\\lambda_i$ valores propios de $A^TA$.",
                  "explicacion_md": "**Raíces cuadradas de los valores propios de $A^TA$.** $A^TA$ es siempre simétrica semidefinida positiva, así sus valores propios son $\\geq 0$ y sus raíces son reales.",
              },
              {
                  "enunciado_md": "El número de valores singulares no nulos de $A$ vale:",
                  "opciones_md": [
                      "$\\dim(\\text{Nul}\\,A)$",
                      "$\\text{rango}(A)$",
                      "$\\min(m, n)$",
                      "$\\max(m, n)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Los $\\sigma_i$ no nulos cuentan los modos no triviales de $A$.",
                  "explicacion_md": "**$\\text{rango}(A)$.** Esto da una **caracterización directa del rango** desde la SVD — útil cuando el rango exacto es difícil de determinar numéricamente.",
              },
          ]),

        ej(
            "Valores singulares directos",
            "Halla los valores singulares de $A = \\begin{bmatrix} 3 & 0 \\\\ 0 & 2 \\\\ 0 & 0 \\end{bmatrix}$.",
            ["Calcula $A^TA$ y sus valores propios."],
            (
                "$A^TA = \\begin{bmatrix} 9 & 0 \\\\ 0 & 4 \\end{bmatrix}$. Valores propios: $9, 4$.\n\n"
                "**Valores singulares:** $\\sigma_1 = 3, \\sigma_2 = 2$.\n\n"
                "Para matrices con columnas ortogonales y entradas no negativas en la diagonal, los $\\sigma_i$ coinciden con esas entradas (ordenadas)."
            ),
        ),

        ej(
            "SVD pequeña",
            "Construye la SVD de $A = \\begin{bmatrix} 2 & 0 \\\\ 0 & -3 \\end{bmatrix}$.",
            ["Diagonalizar $A^TA$ y aplicar el algoritmo."],
            (
                "$A^TA = \\begin{bmatrix} 4 & 0 \\\\ 0 & 9 \\end{bmatrix}$. Valores propios: $9, 4$ (orden decreciente).\n\n"
                "Vectores propios: $\\vec{v}_1 = \\vec{e}_2 = (0, 1)^T$ ($\\lambda = 9$), $\\vec{v}_2 = \\vec{e}_1 = (1, 0)^T$ ($\\lambda = 4$).\n\n"
                "$\\sigma_1 = 3, \\sigma_2 = 2$. $V = \\begin{bmatrix} 0 & 1 \\\\ 1 & 0 \\end{bmatrix}$, $\\Sigma = \\begin{bmatrix} 3 & 0 \\\\ 0 & 2 \\end{bmatrix}$.\n\n"
                "$\\vec{u}_1 = A\\vec{v}_1/3 = (0, -3)^T/3 = (0, -1)^T$. $\\vec{u}_2 = A\\vec{v}_2/2 = (2, 0)^T/2 = (1, 0)^T$.\n\n"
                "$U = \\begin{bmatrix} 0 & 1 \\\\ -1 & 0 \\end{bmatrix}$. **$A = U\\Sigma V^T$.** (Verificable.)"
            ),
        ),

        ej(
            "Rango vía SVD",
            "Si una matriz $A$ tiene valores singulares $\\{5.2, 3.1, 0.8, 0.001, 0\\}$, ¿cuál es su rango? ¿Y si los valores singulares 'pequeños' provienen de error numérico?",
            [
                "El rango es el número de valores singulares estrictamente positivos.",
                "Para datos numéricos, se suele usar un umbral.",
            ],
            (
                "**Rango exacto:** $4$ (cuatro $\\sigma_i \\neq 0$).\n\n"
                "**Rango numérico:** si $0.001$ se considera 'casi cero' (umbral típico vs. el valor más grande), el rango efectivo es $3$. Esta es la base de la **regularización** y del análisis de componentes principales: descartar las componentes con $\\sigma_i$ pequeños."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir valores singulares con valores propios.** Solo coinciden cuando $A$ es simétrica semidefinida positiva.",
              "**Pensar que $\\Sigma$ es cuadrada.** $\\Sigma$ tiene el **mismo tamaño que $A$** ($m \\times n$).",
              "**Olvidar ordenar los valores singulares de mayor a menor.** Es convención, importante para algoritmos como PCA.",
              "**No completar $U$ cuando $r < m$.** Hace falta agregar $\\vec{u}_{r+1}, \\ldots, \\vec{u}_m$ ortonormales para que $U$ sea cuadrada y ortogonal.",
              "**Calcular SVD vía $A A^T$ en vez de $A^TA$.** Ambas funcionan, pero la convención estándar es trabajar con $A^TA$ (que da $V$ y los $\\sigma_i$).",
          ]),

        b("resumen",
          puntos_md=[
              "**SVD:** $A = U\\Sigma V^T$ — existe para **toda** matriz $A \\in \\mathbb{R}^{m\\times n}$.",
              "**$U \\in \\mathbb{R}^{m\\times m}$ ortogonal:** vectores singulares izquierdos.",
              "**$V \\in \\mathbb{R}^{n\\times n}$ ortogonal:** vectores singulares derechos (vectores propios de $A^TA$).",
              "**$\\Sigma \\in \\mathbb{R}^{m\\times n}$ diagonal rectangular:** valores singulares $\\sigma_i = \\sqrt{\\lambda_i(A^TA)}$.",
              "**Algoritmo (3 pasos):** diagonalizar $A^TA$ ($\\to V, \\Sigma$); calcular $\\vec{u}_i = A\\vec{v}_i/\\sigma_i$; completar $U$ con Gram-Schmidt si necesario.",
              "**Geometría:** $A$ mapea la esfera unitaria a un elipsoide con semiejes $\\sigma_i$.",
              "**Aplicaciones:** compresión, PCA, sistemas mal condicionados, recomendaciones, ML moderno.",
              "**Cierre del curso:** la SVD es la herramienta unificadora del álgebra lineal computacional. ¡Felicidades! 🎓",
          ]),
    ]
    return {
        "id": "lec-al-8-3-svd",
        "title": "Descomposición en valores singulares",
        "description": "SVD $A = U\\Sigma V^T$ válida para cualquier matriz, valores singulares $\\sigma_i = \\sqrt{\\lambda_i(A^TA)}$, algoritmo en 3 pasos, aplicaciones en compresión de datos, PCA y ML.",
        "blocks": blocks,
        "duration_minutes": 70,
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

    chapter_id = "ch-al-matrices-simetricas"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Matrices Simétricas",
        "description": (
            "Diagonalización ortogonal y teorema espectral $A = PDP^T$ para matrices simétricas; "
            "formas cuadráticas, ejes principales y clasificación; descomposición en valores "
            "singulares (SVD) $A = U\\Sigma V^T$ válida para cualquier matriz."
        ),
        "order": 8,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_8_1, lesson_8_2, lesson_8_3]
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
        f"✅ Capítulo 8 — Matrices Simétricas listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")
    print()
    print("🎓 ¡Curso de Álgebra Lineal completo! 8 capítulos seedeados.")


if __name__ == "__main__":
    asyncio.run(main())
