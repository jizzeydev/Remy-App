"""
Seed del curso Álgebra Lineal — Capítulo 7: Ortogonalidad.
6 lecciones:
  7.1 Subespacios ortogonales (producto interno, norma, distancia, complemento ortogonal)
  7.2 Conjuntos ortogonales (bases ortogonales/ortonormales, matrices con cols ortonormales)
  7.3 Proyecciones ortogonales (descomposición y = ŷ + z, mejor aproximación, proj_W = U U^T)
  7.4 Proceso de Gram-Schmidt (algoritmo, base ortonormal, factorización QR)
  7.5 Mínimos cuadrados (ecuaciones normales A^T A x = A^T b, error, vía QR)
  7.6 Modelos lineales (regresión, X β = y, ecuaciones normales)

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
# 7.1 Subespacios ortogonales
# =====================================================================
def lesson_7_1():
    blocks = [
        b("texto", body_md=(
            "La **ortogonalidad** es uno de los conceptos más útiles del álgebra lineal. Generaliza la idea "
            "geométrica de **perpendicularidad** ($\\mathbb{R}^2, \\mathbb{R}^3$) a espacios de cualquier dimensión, "
            "vía el **producto interno**.\n\n"
            "Con el producto interno construimos:\n\n"
            "- **Norma** $\\|\\vec{v}\\|$ — la 'longitud' de un vector.\n"
            "- **Distancia** $\\text{dist}(\\vec{u}, \\vec{v}) = \\|\\vec{u} - \\vec{v}\\|$ — generaliza la distancia euclídea.\n"
            "- **Ortogonalidad** $\\vec{u} \\cdot \\vec{v} = 0$ — la condición algebraica de la perpendicularidad.\n"
            "- **Complemento ortogonal** $W^\\perp$ — el subespacio de todo lo perpendicular a $W$.\n\n"
            "Estos conceptos son la base para:\n\n"
            "- **Proyecciones ortogonales** y mínimos cuadrados (lecciones 7.3 y 7.5).\n"
            "- **Bases ortonormales** y Gram-Schmidt (lecciones 7.2 y 7.4).\n"
            "- **Análisis de Fourier** y descomposición espectral.\n\n"
            "Al terminar:\n\n"
            "- Calculas producto interno, norma, distancia y verificas ortogonalidad.\n"
            "- Defines y construyes el **complemento ortogonal** $W^\\perp$.\n"
            "- Aplicas el teorema $(\\text{Fil}\\,A)^\\perp = \\text{Nul}\\,A$ y $(\\text{Col}\\,A)^\\perp = \\text{Nul}\\,A^T$."
        )),

        b("definicion",
          titulo="Producto interno (producto punto)",
          body_md=(
              "Para $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$ vistos como matrices columna $n \\times 1$, el **producto interno** (o **producto punto**) es\n\n"
              "$$\\boxed{\\vec{u} \\cdot \\vec{v} = \\vec{u}^T \\vec{v} = u_1 v_1 + u_2 v_2 + \\cdots + u_n v_n.}$$\n\n"
              "**Propiedades.** Para $\\vec{u}, \\vec{v}, \\vec{w} \\in \\mathbb{R}^n$ y $c \\in \\mathbb{R}$:\n\n"
              "| Propiedad | Fórmula |\n|---|---|\n"
              "| **Conmutativa** | $\\vec{u} \\cdot \\vec{v} = \\vec{v} \\cdot \\vec{u}$ |\n"
              "| **Distributiva** | $(\\vec{u} + \\vec{v}) \\cdot \\vec{w} = \\vec{u}\\cdot\\vec{w} + \\vec{v}\\cdot\\vec{w}$ |\n"
              "| **Compatible con escalar** | $(c\\vec{u})\\cdot\\vec{v} = c(\\vec{u}\\cdot\\vec{v})$ |\n"
              "| **Definida positiva** | $\\vec{u}\\cdot\\vec{u} \\geq 0$, con igualdad solo si $\\vec{u} = \\vec{0}$ |\n\n"
              "Combinándolas: $(c_1\\vec{u}_1 + \\cdots + c_p\\vec{u}_p) \\cdot \\vec{w} = c_1(\\vec{u}_1\\cdot\\vec{w}) + \\cdots + c_p(\\vec{u}_p\\cdot\\vec{w})$."
          )),

        b("ejemplo_resuelto",
          titulo="Producto interno",
          problema_md=(
              "Calcula $\\vec{u}\\cdot\\vec{v}$ y $\\vec{v}\\cdot\\vec{u}$ para $\\vec{u} = (2, -5, -1)^T$ y $\\vec{v} = (3, 2, -3)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\vec{u}\\cdot\\vec{v} = (2)(3) + (-5)(2) + (-1)(-3) = 6 - 10 + 3 = -1.$"
              ),
               "justificacion_md": "Suma de productos componente a componente.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\vec{v}\\cdot\\vec{u} = (3)(2) + (2)(-5) + (-3)(-1) = 6 - 10 + 3 = -1$ ✓ (conmutativa)."
              ),
               "justificacion_md": "**Como esperábamos:** el producto interno es conmutativo.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Norma (longitud) de un vector",
          body_md=(
              "Para $\\vec{v} \\in \\mathbb{R}^n$, la **norma** (o **longitud**) es el escalar no negativo\n\n"
              "$$\\boxed{\\|\\vec{v}\\| = \\sqrt{\\vec{v}\\cdot\\vec{v}} = \\sqrt{v_1^2 + v_2^2 + \\cdots + v_n^2},}$$\n\n"
              "y se cumple $\\|\\vec{v}\\|^2 = \\vec{v}\\cdot\\vec{v}$.\n\n"
              "**En $\\mathbb{R}^2$ y $\\mathbb{R}^3$** coincide con la longitud euclídea (Pitágoras). Se generaliza a $\\mathbb{R}^n$ sin cambio.\n\n"
              "**Propiedades:** $\\|\\vec{v}\\| \\geq 0$ con igualdad solo si $\\vec{v} = \\vec{0}$, y $\\|c\\vec{v}\\| = |c|\\,\\|\\vec{v}\\|$.\n\n"
              "**Vector unitario** $\\hat{u} = \\dfrac{\\vec{v}}{\\|\\vec{v}\\|}$ (norma $1$, misma dirección que $\\vec{v}$). El proceso $\\vec{v} \\mapsto \\hat{u}$ se llama **normalización**."
          )),

        b("ejemplo_resuelto",
          titulo="Vector unitario",
          problema_md=(
              "Sea $\\vec{v} = (1, -2, 2, 0)^T$. Encuentra un vector unitario $\\vec{u}$ en la misma dirección que $\\vec{v}$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\|\\vec{v}\\|^2 = \\vec{v}\\cdot\\vec{v} = 1 + 4 + 4 + 0 = 9$, así $\\|\\vec{v}\\| = 3$."
              ),
               "justificacion_md": "Calcular la norma antes de dividir.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\vec{u} = \\dfrac{1}{\\|\\vec{v}\\|}\\vec{v} = \\dfrac{1}{3}\\begin{bmatrix} 1 \\\\ -2 \\\\ 2 \\\\ 0 \\end{bmatrix} = \\begin{bmatrix} 1/3 \\\\ -2/3 \\\\ 2/3 \\\\ 0 \\end{bmatrix}.$\n\n"
                  "**Verificación:** $\\vec{u}\\cdot\\vec{u} = 1/9 + 4/9 + 4/9 + 0 = 1$ ✓."
              ),
               "justificacion_md": "**Patrón:** dividir un vector por su norma da otro vector unitario en la misma dirección.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Distancia y ortogonalidad",
          body_md=(
              "**Distancia** entre $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$:\n\n"
              "$$\\text{dist}(\\vec{u}, \\vec{v}) = \\|\\vec{u} - \\vec{v}\\|.$$\n\n"
              "Generaliza la distancia euclídea de $\\mathbb{R}^2, \\mathbb{R}^3$.\n\n"
              "**Ortogonalidad.** Dos vectores $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$ son **ortogonales** (denotado $\\vec{u} \\perp \\vec{v}$) si\n\n"
              "$$\\boxed{\\vec{u}\\cdot\\vec{v} = 0.}$$\n\n"
              "**Casos especiales:**\n\n"
              "- $\\vec{0}$ es ortogonal a **todo** vector.\n"
              "- En $\\mathbb{R}^2, \\mathbb{R}^3$ coincide con la perpendicularidad geométrica.\n\n"
              "**Teorema de Pitágoras (general).** $\\vec{u} \\perp \\vec{v} \\iff \\|\\vec{u} + \\vec{v}\\|^2 = \\|\\vec{u}\\|^2 + \\|\\vec{v}\\|^2$."
          )),

        b("ejemplo_resuelto",
          titulo="Distancia entre vectores",
          problema_md=(
              "Halla la distancia entre $\\vec{u} = (7, 1)^T$ y $\\vec{v} = (3, 2)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\vec{u} - \\vec{v} = (4, -1)^T$.\n\n"
                  "$\\|\\vec{u} - \\vec{v}\\| = \\sqrt{16 + 1} = \\sqrt{17}.$"
              ),
               "justificacion_md": "Restamos y aplicamos norma.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Complemento ortogonal $W^\\perp$",
          body_md=(
              "Sea $W$ un subespacio de $\\mathbb{R}^n$. Un vector $\\vec{z} \\in \\mathbb{R}^n$ es **ortogonal a $W$** si $\\vec{z}\\cdot\\vec{w} = 0$ para todo $\\vec{w} \\in W$.\n\n"
              "El **complemento ortogonal** de $W$ es el conjunto de todos esos vectores:\n\n"
              "$$\\boxed{W^\\perp = \\{\\vec{z} \\in \\mathbb{R}^n : \\vec{z}\\cdot\\vec{w} = 0 \\text{ para todo } \\vec{w} \\in W\\}.}$$\n\n"
              "(Se lee 'perpendicular a $W$'.)\n\n"
              "**Hechos importantes:**\n\n"
              "1. **$W^\\perp$ es un subespacio** de $\\mathbb{R}^n$.\n"
              "2. **Basta verificar ortogonalidad con un conjunto generador:** $\\vec{z} \\in W^\\perp \\iff \\vec{z}$ es ortogonal a cada vector de un conjunto generador de $W$.\n"
              "3. **$(W^\\perp)^\\perp = W$**: el complemento del complemento es el subespacio original.\n"
              "4. **$W \\cap W^\\perp = \\{\\vec{0}\\}$**: solo el vector cero está en ambos."
          )),

        b("intuicion", body_md=(
            "**Visualización en $\\mathbb{R}^3$.** Sea $W$ un plano por el origen. Entonces $W^\\perp$ es la **recta** por el origen perpendicular al plano. Recíprocamente, si $L$ es una recta por el origen, $L^\\perp$ es el plano perpendicular.\n\n"
            "**En general:** si $\\dim W = k$, entonces $\\dim W^\\perp = n - k$ (los dos subespacios 'descomponen' $\\mathbb{R}^n$ ortogonalmente)."
        )),

        b("teorema",
          enunciado_md=(
              "**Teorema fundamental: ortogonales de espacios fila y columna.**\n\n"
              "Sea $A \\in \\mathbb{R}^{m \\times n}$. Entonces:\n\n"
              "$$\\boxed{(\\text{Fil}\\,A)^\\perp = \\text{Nul}\\,A,} \\qquad \\boxed{(\\text{Col}\\,A)^\\perp = \\text{Nul}\\,A^T.}$$\n\n"
              "**Lectura:**\n\n"
              "- $\\vec{x}$ es ortogonal a todas las filas de $A$ $\\iff$ $A\\vec{x} = \\vec{0}$ $\\iff$ $\\vec{x} \\in \\text{Nul}\\,A$.\n"
              "- Análogamente para $\\text{Col}\\,A$ usando $A^T$."
          ),
          demostracion_md=(
              "$\\vec{x} \\in (\\text{Fil}\\,A)^\\perp$ $\\iff$ $\\vec{x}$ es ortogonal a cada fila de $A$ $\\iff$ cada producto $(\\text{fila}_i(A))\\cdot\\vec{x} = 0$ $\\iff$ $A\\vec{x} = \\vec{0}$ $\\iff$ $\\vec{x} \\in \\text{Nul}\\,A$. Análogo para columnas con $A^T$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Verificar ortogonalidad",
          problema_md=(
              "Sean $\\vec{u} = (3, 1, 1)^T$ y $\\vec{w} = (-1, 2, 1)^T$. ¿Son ortogonales?"
          ),
          pasos=[
              {"accion_md": (
                  "$\\vec{u}\\cdot\\vec{w} = (3)(-1) + (1)(2) + (1)(1) = -3 + 2 + 1 = 0.$\n\n"
                  "**$\\vec{u} \\perp \\vec{w}$ ✓.**"
              ),
               "justificacion_md": "Producto punto $= 0 \\iff$ ortogonalidad.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\vec{u}, \\vec{v} \\in \\mathbb{R}^3$ son ortogonales y $\\|\\vec{u}\\| = 3, \\|\\vec{v}\\| = 4$, entonces $\\|\\vec{u} + \\vec{v}\\|$ vale:",
                  "opciones_md": ["$7$", "$\\sqrt{7}$", "$5$", "$25$"],
                  "correcta": "C",
                  "pista_md": "Pitágoras generalizado.",
                  "explicacion_md": "**$\\|\\vec{u}+\\vec{v}\\|^2 = 3^2 + 4^2 = 25 \\Rightarrow \\|\\vec{u}+\\vec{v}\\| = 5$.** Pitágoras se aplica solo cuando los vectores son ortogonales.",
              },
              {
                  "enunciado_md": "Para una matriz $A$, $(\\text{Col}\\,A)^\\perp$ es:",
                  "opciones_md": [
                      "$\\text{Nul}\\,A$",
                      "**$\\text{Nul}\\,A^T$**",
                      "$\\text{Fil}\\,A$",
                      "$\\text{Col}\\,A^T$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\text{Col}\\,A = \\text{Fil}\\,A^T$.",
                  "explicacion_md": "**$(\\text{Col}\\,A)^\\perp = \\text{Nul}\\,A^T$.** Aplicar el teorema fundamental a $A^T$.",
              },
              {
                  "enunciado_md": "Si $W \\subseteq \\mathbb{R}^5$ tiene dimensión $2$, entonces $\\dim W^\\perp$ vale:",
                  "opciones_md": ["$2$", "$3$", "$5$", "$0$"],
                  "correcta": "B",
                  "pista_md": "$\\dim W + \\dim W^\\perp = n$.",
                  "explicacion_md": "**$\\dim W^\\perp = 5 - 2 = 3$.** $\\mathbb{R}^n$ se descompone como suma directa $W \\oplus W^\\perp$.",
              },
          ]),

        ej(
            "Cálculo de norma y unitario",
            "Halla $\\|\\vec{v}\\|$ y normaliza $\\vec{v} = (2, -3, 6, 0)^T$.",
            ["Calcula $\\vec{v}\\cdot\\vec{v}$ primero."],
            (
                "$\\|\\vec{v}\\|^2 = 4 + 9 + 36 + 0 = 49 \\Rightarrow \\|\\vec{v}\\| = 7$.\n\n"
                "$\\hat{u} = \\dfrac{1}{7}(2, -3, 6, 0)^T = (2/7,\\ -3/7,\\ 6/7,\\ 0)^T$."
            ),
        ),

        ej(
            "Distancia",
            "Halla la distancia entre $\\vec{u} = (1, 2, 3)^T$ y $\\vec{v} = (4, 0, 1)^T$.",
            ["$\\|\\vec{u} - \\vec{v}\\|$."],
            (
                "$\\vec{u} - \\vec{v} = (-3, 2, 2)^T$. $\\|\\vec{u}-\\vec{v}\\| = \\sqrt{9 + 4 + 4} = \\sqrt{17}$."
            ),
        ),

        ej(
            "Complemento ortogonal de un subespacio",
            "Sea $W = \\text{Gen}\\{(1, 2, -1)^T\\} \\subseteq \\mathbb{R}^3$. Halla $W^\\perp$.",
            [
                "$W^\\perp$ son los $\\vec{x}$ con $\\vec{x}\\cdot(1,2,-1) = 0$.",
                "Es la solución de una sola ecuación: un plano.",
            ],
            (
                "$W^\\perp = \\{\\vec{x} : x_1 + 2x_2 - x_3 = 0\\}$. Variables libres $x_2, x_3$:\n\n"
                "$x_1 = -2x_2 + x_3$, $\\vec{x} = x_2(-2, 1, 0)^T + x_3(1, 0, 1)^T$.\n\n"
                "$W^\\perp = \\text{Gen}\\{(-2, 1, 0)^T, (1, 0, 1)^T\\}$. Es un **plano** por el origen, y $\\dim W^\\perp = 2 = 3 - 1$ ✓."
            ),
        ),

        fig(
            "Diagrama 3D en R^3 con ejes x, y, z. Un plano W teal #06b6d4 semitransparente pasando por el origen, "
            "con un vector u teal apoyado sobre él. Una recta W^perp en ámbar #f59e0b ortogonal al plano, también "
            "pasando por el origen, con un vector v ámbar a lo largo de ella. Pequeña marca de ángulo recto entre "
            "el plano y la recta. Etiqueta inferior: 'u·v = 0 para todo u en W, v en W^perp'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que ortogonal = paralelo.** Son opuestos: $\\vec{u}\\cdot\\vec{v} = 0 \\Rightarrow$ perpendiculares; paralelos $\\iff$ uno es múltiplo del otro.",
              "**Aplicar Pitágoras sin ortogonalidad.** $\\|\\vec{u}+\\vec{v}\\|^2 = \\|\\vec{u}\\|^2 + \\|\\vec{v}\\|^2$ **solo si** $\\vec{u}\\perp\\vec{v}$.",
              "**Confundir $(\\text{Col}\\,A)^\\perp$ con $\\text{Nul}\\,A$.** Lo correcto: $(\\text{Col}\\,A)^\\perp = \\text{Nul}\\,A^T$ (con la transpuesta).",
              "**Olvidar que $W^\\perp$ es subespacio.** Aunque se construye como conjunto de soluciones, es **siempre** subespacio (núcleo de algo).",
              "**Confundir norma con producto punto.** $\\|\\vec{v}\\| = \\sqrt{\\vec{v}\\cdot\\vec{v}}$, no $\\vec{v}\\cdot\\vec{v}$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Producto interno:** $\\vec{u}\\cdot\\vec{v} = \\vec{u}^T\\vec{v} = \\sum u_i v_i$.",
              "**Norma:** $\\|\\vec{v}\\| = \\sqrt{\\vec{v}\\cdot\\vec{v}}$. **Distancia:** $\\|\\vec{u} - \\vec{v}\\|$.",
              "**Ortogonalidad:** $\\vec{u}\\perp\\vec{v} \\iff \\vec{u}\\cdot\\vec{v} = 0$.",
              "**Pitágoras general:** $\\|\\vec{u}+\\vec{v}\\|^2 = \\|\\vec{u}\\|^2 + \\|\\vec{v}\\|^2$ si $\\vec{u}\\perp\\vec{v}$.",
              "**Complemento ortogonal:** $W^\\perp$ = subespacio de todos los vectores ortogonales a $W$.",
              "**Teorema fundamental:** $(\\text{Fil}\\,A)^\\perp = \\text{Nul}\\,A$ y $(\\text{Col}\\,A)^\\perp = \\text{Nul}\\,A^T$.",
              "**Próxima lección:** **conjuntos ortogonales** y **bases ortonormales**.",
          ]),
    ]
    return {
        "id": "lec-al-7-1-subespacios-ortogonales",
        "title": "Subespacios ortogonales",
        "description": "Producto interno, norma, distancia, ortogonalidad $\\vec{u}\\cdot\\vec{v} = 0$, complemento ortogonal $W^\\perp$, teorema $(\\text{Fil}\\,A)^\\perp = \\text{Nul}\\,A$.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 1,
    }


# =====================================================================
# 7.2 Conjuntos ortogonales
# =====================================================================
def lesson_7_2():
    blocks = [
        b("texto", body_md=(
            "Una base es buena. Una base **ortogonal** es **mucho mejor**: simplifica drásticamente "
            "los cálculos de coordenadas y proyecciones. Una base **ortonormal** (ortogonal + unitarios) "
            "es lo más cómodo posible — las matrices con columnas ortonormales **preservan longitudes y ángulos**.\n\n"
            "Estas bases son la herramienta de elección en:\n\n"
            "- **Análisis numérico:** algoritmos estables (QR, SVD).\n"
            "- **Procesamiento de señales:** Fourier, wavelets.\n"
            "- **Geometría computacional:** rotaciones, isometrías.\n\n"
            "Al terminar:\n\n"
            "- Defines y reconoces conjuntos ortogonales y ortonormales.\n"
            "- Calculas coordenadas en una **base ortogonal** con la fórmula $c_j = \\dfrac{\\vec{y}\\cdot\\vec{u}_j}{\\vec{u}_j\\cdot\\vec{u}_j}$.\n"
            "- Trabajas con la **proyección sobre una recta** $\\text{proy}_L\\,\\vec{y}$.\n"
            "- Usas matrices con **columnas ortonormales** y la propiedad $U^T U = I$."
        )),

        b("definicion",
          titulo="Conjunto ortogonal",
          body_md=(
              "Un conjunto $\\{\\vec{u}_1, \\ldots, \\vec{u}_p\\} \\subseteq \\mathbb{R}^n$ es **ortogonal** si\n\n"
              "$$\\boxed{\\vec{u}_i \\cdot \\vec{u}_j = 0 \\quad \\forall i \\neq j.}$$\n\n"
              "Es decir, los pares **distintos** son ortogonales entre sí.\n\n"
              "**Teorema clave.** Si $\\{\\vec{u}_1, \\ldots, \\vec{u}_p\\}$ es ortogonal y todos los $\\vec{u}_i \\neq \\vec{0}$, entonces es **linealmente independiente** y forma una **base** de $\\text{Gen}\\{\\vec{u}_1, \\ldots, \\vec{u}_p\\}$.\n\n"
              "**Demostración.** Si $\\sum c_i \\vec{u}_i = \\vec{0}$, tomando producto con $\\vec{u}_j$: $c_j \\vec{u}_j\\cdot\\vec{u}_j = 0 \\Rightarrow c_j = 0$ (porque $\\vec{u}_j\\cdot\\vec{u}_j = \\|\\vec{u}_j\\|^2 \\neq 0$). $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Verificar conjunto ortogonal",
          problema_md=(
              "Demuestra que $\\{\\vec{u}_1, \\vec{u}_2, \\vec{u}_3\\}$ es ortogonal con $\\vec{u}_1 = (3, 1, 1)^T$, $\\vec{u}_2 = (-1, 2, 1)^T$, $\\vec{u}_3 = (-1/2, -2, 7/2)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "Calculamos los $\\binom{3}{2} = 3$ productos punto distintos:\n\n"
                  "$\\vec{u}_1\\cdot\\vec{u}_2 = -3 + 2 + 1 = 0$. ✓\n\n"
                  "$\\vec{u}_1\\cdot\\vec{u}_3 = -3/2 - 2 + 7/2 = 0$. ✓\n\n"
                  "$\\vec{u}_2\\cdot\\vec{u}_3 = 1/2 - 4 + 7/2 = 0$. ✓"
              ),
               "justificacion_md": "Solo verificar pares distintos.",
               "es_resultado": False},
              {"accion_md": (
                  "Los tres vectores son no nulos y mutuamente ortogonales $\\Rightarrow$ **conjunto ortogonal LI** $\\Rightarrow$ **base ortogonal de $\\mathbb{R}^3$** (3 vectores LI en $\\mathbb{R}^3$)."
              ),
               "justificacion_md": "Por el teorema, ortogonalidad + no nulos $\\Rightarrow$ LI.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Coordenadas en una base ortogonal",
          enunciado_md=(
              "Sea $\\{\\vec{u}_1, \\ldots, \\vec{u}_p\\}$ una **base ortogonal** de un subespacio $W \\subseteq \\mathbb{R}^n$. Para cada $\\vec{y} \\in W$, los pesos $c_j$ en la combinación lineal $\\vec{y} = c_1 \\vec{u}_1 + \\cdots + c_p \\vec{u}_p$ están dados **explícitamente** por:\n\n"
              "$$\\boxed{c_j = \\frac{\\vec{y}\\cdot\\vec{u}_j}{\\vec{u}_j\\cdot\\vec{u}_j}, \\qquad j = 1, \\ldots, p.}$$\n\n"
              "**Sin resolver ningún sistema lineal** — la ortogonalidad permite leer cada coordenada **independientemente**."
          ),
          demostracion_md=(
              "Tomando producto interno con $\\vec{u}_j$ en ambos lados de $\\vec{y} = \\sum c_i \\vec{u}_i$:\n\n"
              "$\\vec{y}\\cdot\\vec{u}_j = \\sum c_i (\\vec{u}_i\\cdot\\vec{u}_j) = c_j (\\vec{u}_j\\cdot\\vec{u}_j)$ (todos los demás son $0$ por ortogonalidad).\n\n"
              "Despejando $c_j = (\\vec{y}\\cdot\\vec{u}_j)/(\\vec{u}_j\\cdot\\vec{u}_j)$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Coordenadas en base ortogonal",
          problema_md=(
              "Con $\\{\\vec{u}_1, \\vec{u}_2, \\vec{u}_3\\}$ del ejemplo anterior (base ortogonal de $\\mathbb{R}^3$), expresa $\\vec{y} = (6, 1, -8)^T$ como combinación lineal."
          ),
          pasos=[
              {"accion_md": (
                  "Productos:\n\n"
                  "$\\vec{y}\\cdot\\vec{u}_1 = 18 + 1 - 8 = 11$. $\\vec{u}_1\\cdot\\vec{u}_1 = 9 + 1 + 1 = 11$.\n\n"
                  "$\\vec{y}\\cdot\\vec{u}_2 = -6 + 2 - 8 = -12$. $\\vec{u}_2\\cdot\\vec{u}_2 = 1 + 4 + 1 = 6$.\n\n"
                  "$\\vec{y}\\cdot\\vec{u}_3 = -3 - 2 - 28 = -33$. $\\vec{u}_3\\cdot\\vec{u}_3 = 1/4 + 4 + 49/4 = 33/2$."
              ),
               "justificacion_md": "Calcular los productos punto necesarios.",
               "es_resultado": False},
              {"accion_md": (
                  "Coordenadas: $c_1 = 11/11 = 1$, $c_2 = -12/6 = -2$, $c_3 = -33/(33/2) = -2$.\n\n"
                  "**$\\vec{y} = \\vec{u}_1 - 2\\vec{u}_2 - 2\\vec{u}_3$.**"
              ),
               "justificacion_md": "**Sin resolver ningún sistema lineal** — solo cálculos de productos punto.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Proyección ortogonal sobre una recta",
          body_md=(
              "Dado $\\vec{u} \\neq \\vec{0}$ en $\\mathbb{R}^n$, sea $L = \\text{Gen}\\{\\vec{u}\\}$ la **recta** generada por $\\vec{u}$. Para cualquier $\\vec{y} \\in \\mathbb{R}^n$, podemos descomponer\n\n"
              "$$\\vec{y} = \\hat{\\vec{y}} + \\vec{z},$$\n\n"
              "donde $\\hat{\\vec{y}}$ es múltiplo de $\\vec{u}$ (en $L$) y $\\vec{z}$ es ortogonal a $\\vec{u}$.\n\n"
              "La **proyección ortogonal de $\\vec{y}$ sobre $L$** (o sobre $\\vec{u}$) es\n\n"
              "$$\\boxed{\\hat{\\vec{y}} = \\text{proy}_L\\,\\vec{y} = \\frac{\\vec{y}\\cdot\\vec{u}}{\\vec{u}\\cdot\\vec{u}}\\,\\vec{u}.}$$\n\n"
              "Y $\\vec{z} = \\vec{y} - \\hat{\\vec{y}}$ es la **componente de $\\vec{y}$ ortogonal a $\\vec{u}$**.\n\n"
              "**Geometría:** $\\hat{\\vec{y}}$ es el punto de $L$ más cercano a $\\vec{y}$ (la 'sombra' de $\\vec{y}$ sobre la recta)."
          )),

        b("ejemplo_resuelto",
          titulo="Proyección sobre una recta",
          problema_md=(
              "Sea $\\vec{y} = (7, 6)^T$ y $\\vec{u} = (4, 2)^T$. Halla $\\text{proy}_L\\,\\vec{y}$ donde $L = \\text{Gen}\\{\\vec{u}\\}$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\vec{y}\\cdot\\vec{u} = 28 + 12 = 40$. $\\vec{u}\\cdot\\vec{u} = 16 + 4 = 20$."
              ),
               "justificacion_md": "Productos previos.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\hat{\\vec{y}} = \\dfrac{40}{20}(4, 2)^T = 2(4, 2)^T = (8, 4)^T.$\n\n"
                  "Componente ortogonal: $\\vec{z} = \\vec{y} - \\hat{\\vec{y}} = (7-8, 6-4)^T = (-1, 2)^T.$\n\n"
                  "**Verificación:** $\\hat{\\vec{y}}\\cdot\\vec{z} = (8)(-1) + (4)(2) = 0$ ✓."
              ),
               "justificacion_md": "Descomposición $\\vec{y} = \\hat{\\vec{y}} + \\vec{z}$ con $\\hat{\\vec{y}} \\in L$ y $\\vec{z} \\perp L$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Conjunto / base ortonormal",
          body_md=(
              "Un conjunto $\\{\\vec{u}_1, \\ldots, \\vec{u}_p\\}$ es **ortonormal** si es ortogonal **y** todos sus vectores son **unitarios**:\n\n"
              "$$\\vec{u}_i\\cdot\\vec{u}_j = \\delta_{ij} = \\begin{cases} 1 & \\text{si } i = j \\\\ 0 & \\text{si } i \\neq j \\end{cases}.$$\n\n"
              "**Base ortonormal:** una base que también es conjunto ortonormal.\n\n"
              "**Ejemplos:** la base estándar $\\{\\vec{e}_1, \\ldots, \\vec{e}_n\\}$ de $\\mathbb{R}^n$. Cualquier subconjunto suyo también es ortonormal.\n\n"
              "**Convertir base ortogonal en ortonormal:** **normalizar** cada vector dividiendo por su norma — el método de Gram-Schmidt en lección 7.4."
          )),

        b("teorema",
          nombre="Matrices con columnas ortonormales",
          enunciado_md=(
              "Una matriz $U \\in \\mathbb{R}^{m \\times n}$ tiene **columnas ortonormales** si y solo si\n\n"
              "$$\\boxed{U^T U = I_n.}$$\n\n"
              "Si $U$ tiene columnas ortonormales y $\\vec{x}, \\vec{y} \\in \\mathbb{R}^n$:\n\n"
              "**(a) Preserva longitudes:** $\\|U\\vec{x}\\| = \\|\\vec{x}\\|$.\n\n"
              "**(b) Preserva productos internos:** $(U\\vec{x})\\cdot(U\\vec{y}) = \\vec{x}\\cdot\\vec{y}$.\n\n"
              "**(c) Preserva ortogonalidad:** $(U\\vec{x})\\cdot(U\\vec{y}) = 0 \\iff \\vec{x}\\cdot\\vec{y} = 0$.\n\n"
              "**Geometría:** la transformación $\\vec{x} \\mapsto U\\vec{x}$ es una **isometría** (rotación, reflexión, o combinación)."
          ),
          demostracion_md=(
              "$(U\\vec{x})\\cdot(U\\vec{y}) = (U\\vec{x})^T(U\\vec{y}) = \\vec{x}^T U^T U \\vec{y} = \\vec{x}^T I \\vec{y} = \\vec{x}\\cdot\\vec{y}$. (a) y (c) son consecuencias inmediatas. $\\blacksquare$\n\n"
              "**Caso especial $m = n$:** $U^T U = I$ y $U$ cuadrada $\\Rightarrow U^{-1} = U^T$. Estas son las **matrices ortogonales** — rotaciones y reflexiones de $\\mathbb{R}^n$."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar columnas ortonormales y preservación",
          problema_md=(
              "Sea $U = \\begin{bmatrix} 1/\\sqrt{2} & 2/3 \\\\ 1/\\sqrt{2} & -2/3 \\\\ 0 & 1/3 \\end{bmatrix}$ y $\\vec{x} = (\\sqrt{2}, 3)^T$. Verifica $U^T U = I$ y $\\|U\\vec{x}\\| = \\|\\vec{x}\\|$."
          ),
          pasos=[
              {"accion_md": (
                  "$U^T U = \\begin{bmatrix} 1/\\sqrt{2} & 1/\\sqrt{2} & 0 \\\\ 2/3 & -2/3 & 1/3 \\end{bmatrix}\\begin{bmatrix} 1/\\sqrt{2} & 2/3 \\\\ 1/\\sqrt{2} & -2/3 \\\\ 0 & 1/3 \\end{bmatrix} = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} = I_2$ ✓."
              ),
               "justificacion_md": "Las entradas son productos punto entre columnas; diagonal $= 1$ (vectores unitarios), fuera $= 0$ (ortogonales).",
               "es_resultado": False},
              {"accion_md": (
                  "$U\\vec{x} = \\begin{bmatrix} 1/\\sqrt{2}\\cdot\\sqrt{2} + 2/3\\cdot 3 \\\\ 1/\\sqrt{2}\\cdot\\sqrt{2} - 2/3\\cdot 3 \\\\ 0 + 1/3\\cdot 3 \\end{bmatrix} = \\begin{bmatrix} 3 \\\\ -1 \\\\ 1 \\end{bmatrix}.$\n\n"
                  "$\\|U\\vec{x}\\| = \\sqrt{9 + 1 + 1} = \\sqrt{11}$. $\\|\\vec{x}\\| = \\sqrt{2 + 9} = \\sqrt{11}$ ✓."
              ),
               "justificacion_md": "**Patrón:** matrices con columnas ortonormales no estiran ni comprimen vectores — son isometrías.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\{\\vec{u}_1, \\vec{u}_2\\}$ es base ortogonal de $W$ y $\\vec{y} \\in W$, entonces los pesos en $\\vec{y} = c_1\\vec{u}_1 + c_2\\vec{u}_2$ son:",
                  "opciones_md": [
                      "Solución de un sistema $2\\times 2$ general",
                      "$c_j = \\dfrac{\\vec{y}\\cdot\\vec{u}_j}{\\vec{u}_j\\cdot\\vec{u}_j}$",
                      "$c_j = \\vec{y}\\cdot\\vec{u}_j$",
                      "$c_j = \\|\\vec{u}_j\\|$",
                  ],
                  "correcta": "B",
                  "pista_md": "Fórmula explícita por ortogonalidad.",
                  "explicacion_md": "**$c_j = (\\vec{y}\\cdot\\vec{u}_j)/(\\vec{u}_j\\cdot\\vec{u}_j)$.** Si la base es además **ortonormal** ($\\vec{u}_j\\cdot\\vec{u}_j = 1$), simplifica a $c_j = \\vec{y}\\cdot\\vec{u}_j$.",
              },
              {
                  "enunciado_md": "Una matriz $U$ tiene columnas ortonormales $\\iff$:",
                  "opciones_md": ["$U U^T = I$", "$U^T U = I$", "$U = I$", "$U^{-1} = U$"],
                  "correcta": "B",
                  "pista_md": "Las entradas de $U^T U$ son productos punto entre columnas.",
                  "explicacion_md": "**$U^T U = I$.** ($U U^T = I$ solo si $U$ es además **cuadrada**, i.e., matriz ortogonal.)",
              },
              {
                  "enunciado_md": "La proyección de $\\vec{y}$ sobre $\\vec{u} \\neq \\vec{0}$ es:",
                  "opciones_md": [
                      "$\\vec{y}\\cdot\\vec{u}$",
                      "$\\dfrac{\\vec{y}\\cdot\\vec{u}}{\\vec{u}\\cdot\\vec{u}}\\vec{u}$",
                      "$\\dfrac{\\vec{u}}{\\|\\vec{u}\\|}$",
                      "$\\vec{u} - \\vec{y}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Múltiplo escalar de $\\vec{u}$ con coeficiente normalizado.",
                  "explicacion_md": "**$\\hat{\\vec{y}} = \\dfrac{\\vec{y}\\cdot\\vec{u}}{\\vec{u}\\cdot\\vec{u}}\\vec{u}$.** Es un múltiplo de $\\vec{u}$ tal que $\\vec{y} - \\hat{\\vec{y}}$ es ortogonal a $\\vec{u}$.",
              },
          ]),

        ej(
            "Coordenadas con base ortogonal",
            "Sean $\\vec{u}_1 = (1, 1, 1)^T$, $\\vec{u}_2 = (1, -2, 1)^T$, $\\vec{u}_3 = (1, 0, -1)^T$. Verifica que es base ortogonal de $\\mathbb{R}^3$ y expresa $\\vec{y} = (3, 1, 5)^T$ en esa base.",
            ["Productos punto pares.", "Aplica la fórmula $c_j = (\\vec{y}\\cdot\\vec{u}_j)/(\\vec{u}_j\\cdot\\vec{u}_j)$."],
            (
                "Productos: $\\vec{u}_1\\cdot\\vec{u}_2 = 0$, $\\vec{u}_1\\cdot\\vec{u}_3 = 0$, $\\vec{u}_2\\cdot\\vec{u}_3 = 0$ ✓ (ortogonal).\n\n"
                "$\\vec{u}_i\\cdot\\vec{u}_i$: $3, 6, 2$. $\\vec{y}\\cdot\\vec{u}_i$: $9, -2, -2$.\n\n"
                "$c_1 = 9/3 = 3$, $c_2 = -2/6 = -1/3$, $c_3 = -2/2 = -1$. **$\\vec{y} = 3\\vec{u}_1 - \\tfrac{1}{3}\\vec{u}_2 - \\vec{u}_3$.**"
            ),
        ),

        ej(
            "Proyección sobre una recta",
            "Halla la proyección de $\\vec{y} = (1, 4)^T$ sobre $\\vec{u} = (3, 1)^T$ y la componente ortogonal.",
            ["$\\hat{\\vec{y}} = ((\\vec{y}\\cdot\\vec{u})/(\\vec{u}\\cdot\\vec{u}))\\vec{u}$."],
            (
                "$\\vec{y}\\cdot\\vec{u} = 3 + 4 = 7$. $\\vec{u}\\cdot\\vec{u} = 9 + 1 = 10$.\n\n"
                "$\\hat{\\vec{y}} = (7/10)(3, 1)^T = (21/10, 7/10)^T$. $\\vec{z} = (1, 4) - (21/10, 7/10) = (-11/10, 33/10)$.\n\n"
                "Verificación: $\\hat{\\vec{y}}\\cdot\\vec{z} = -231/100 + 231/100 = 0$ ✓."
            ),
        ),

        ej(
            "Matriz ortonormal y norma",
            "Sea $U = \\begin{bmatrix} 3/5 & -4/5 \\\\ 4/5 & 3/5 \\end{bmatrix}$. Verifica que $U^T U = I$ e identifica la transformación geométrica.",
            ["Calcula $U^T U$.", "Identifica $\\cos\\theta, \\sin\\theta$."],
            (
                "$U^T U = \\begin{bmatrix} 3/5 & 4/5 \\\\ -4/5 & 3/5 \\end{bmatrix}\\begin{bmatrix} 3/5 & -4/5 \\\\ 4/5 & 3/5 \\end{bmatrix} = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} = I_2$ ✓.\n\n"
                "$U$ tiene la forma $\\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix}$ con $\\cos\\theta = 3/5, \\sin\\theta = 4/5$. Es la **rotación** por ángulo $\\theta = \\arctan(4/3) \\approx 53.13°$."
            ),
        ),

        fig(
            "Dos paneles lado a lado en R^3. Panel izquierdo: tres vectores ortogonales saliendo del origen, u1 "
            "teal #06b6d4, u2 ámbar #f59e0b y u3 púrpura, formando ángulos rectos entre sí dos a dos. Pequeñas "
            "marcas de ángulo recto entre cada par. Panel derecho: los mismos tres vectores ya unitarios (norma 1) "
            "más cortos, etiquetados con sombrero û1, û2, û3. Título: 'Ortogonal vs Ortonormal'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar verificar que los $\\vec{u}_i \\neq \\vec{0}$ para concluir LI.** Un conjunto que contiene a $\\vec{0}$ es LD aunque sea trivialmente 'ortogonal'.",
              "**Aplicar la fórmula $c_j = (\\vec{y}\\cdot\\vec{u}_j)/(\\vec{u}_j\\cdot\\vec{u}_j)$ a una base no ortogonal.** **Solo vale** para bases ortogonales — para otras hay que resolver un sistema.",
              "**Confundir $U^T U = I$ con $UU^T = I$.** Para matrices rectangulares con columnas ortonormales: $U^T U = I_n$. $UU^T = I_m$ solo si $U$ es además cuadrada.",
              "**Pensar que toda matriz con columnas unitarias es ortonormal.** Hace falta que las columnas sean **mutuamente ortogonales** además de unitarias.",
              "**Confundir 'ortogonal' (mutuamente perpendiculares) con 'ortonormal' (también unitarios).**",
          ]),

        b("resumen",
          puntos_md=[
              "**Conjunto ortogonal:** $\\vec{u}_i\\cdot\\vec{u}_j = 0$ para $i \\neq j$.",
              "**Ortogonal + no nulos $\\Rightarrow$ LI** (son base de su gen).",
              "**Coordenadas en base ortogonal:** $c_j = \\dfrac{\\vec{y}\\cdot\\vec{u}_j}{\\vec{u}_j\\cdot\\vec{u}_j}$ — fórmula explícita, sin sistema.",
              "**Proyección sobre recta:** $\\text{proy}_L\\,\\vec{y} = \\dfrac{\\vec{y}\\cdot\\vec{u}}{\\vec{u}\\cdot\\vec{u}}\\vec{u}$.",
              "**Conjunto ortonormal:** ortogonal + vectores unitarios.",
              "**Columnas ortonormales:** $U^T U = I$. La transformación $\\vec{x} \\mapsto U\\vec{x}$ preserva longitudes y ángulos.",
              "**Próxima lección:** **proyección ortogonal sobre subespacios** generales (no solo rectas).",
          ]),
    ]
    return {
        "id": "lec-al-7-2-conjuntos-ortogonales",
        "title": "Conjuntos ortogonales",
        "description": "Conjuntos y bases ortogonales/ortonormales, fórmula de coordenadas $c_j = (\\vec{y}\\cdot\\vec{u}_j)/(\\vec{u}_j\\cdot\\vec{u}_j)$, proyección sobre recta y matrices con columnas ortonormales ($U^TU = I$).",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# =====================================================================
# 7.3 Proyecciones ortogonales
# =====================================================================
def lesson_7_3():
    blocks = [
        b("texto", body_md=(
            "Generalizamos la **proyección sobre una recta** (lección 7.2) a **proyección sobre cualquier subespacio**. "
            "El resultado central es que todo vector $\\vec{y} \\in \\mathbb{R}^n$ se descompone de forma **única** "
            "como $\\vec{y} = \\hat{\\vec{y}} + \\vec{z}$, con $\\hat{\\vec{y}} \\in W$ y $\\vec{z} \\in W^\\perp$.\n\n"
            "El vector $\\hat{\\vec{y}}$ se llama la **proyección ortogonal de $\\vec{y}$ sobre $W$**, y tiene una propiedad notable: "
            "es el **punto de $W$ más cercano a $\\vec{y}$**. Esta es la base de los **mínimos cuadrados** y de muchísimas "
            "aplicaciones en estadística y machine learning.\n\n"
            "Al terminar:\n\n"
            "- Aplicas el **teorema de descomposición ortogonal** $\\vec{y} = \\hat{\\vec{y}} + \\vec{z}$.\n"
            "- Calculas $\\text{proy}_W\\,\\vec{y}$ usando una base ortogonal de $W$.\n"
            "- Aplicas el **teorema de la mejor aproximación**.\n"
            "- Usas la **fórmula matricial** $\\text{proy}_W\\,\\vec{y} = U U^T \\vec{y}$ con $U$ de columnas ortonormales."
        )),

        b("teorema",
          nombre="Teorema de descomposición ortogonal",
          enunciado_md=(
              "Sea $W$ un subespacio de $\\mathbb{R}^n$. Entonces todo $\\vec{y} \\in \\mathbb{R}^n$ se escribe de forma **única** como\n\n"
              "$$\\boxed{\\vec{y} = \\hat{\\vec{y}} + \\vec{z}, \\quad \\hat{\\vec{y}} \\in W, \\ \\vec{z} \\in W^\\perp.}$$\n\n"
              "Si $\\{\\vec{u}_1, \\ldots, \\vec{u}_p\\}$ es una **base ortogonal** de $W$, entonces\n\n"
              "$$\\hat{\\vec{y}} = \\frac{\\vec{y}\\cdot\\vec{u}_1}{\\vec{u}_1\\cdot\\vec{u}_1}\\vec{u}_1 + \\cdots + \\frac{\\vec{y}\\cdot\\vec{u}_p}{\\vec{u}_p\\cdot\\vec{u}_p}\\vec{u}_p, \\qquad \\vec{z} = \\vec{y} - \\hat{\\vec{y}}.$$\n\n"
              "$\\hat{\\vec{y}}$ se llama la **proyección ortogonal de $\\vec{y}$ sobre $W$** y se denota $\\text{proy}_W\\,\\vec{y}$.\n\n"
              "**El resultado es independiente de la base ortogonal elegida** — $\\hat{\\vec{y}}$ está determinado por $W$ y $\\vec{y}$."
          ),
          demostracion_md=(
              "**Existencia:** definir $\\hat{\\vec{y}}$ por la fórmula y $\\vec{z} = \\vec{y} - \\hat{\\vec{y}}$. Por construcción $\\hat{\\vec{y}} \\in W$. Verificar $\\vec{z} \\perp \\vec{u}_j$ para cada $j$ (cálculo directo) $\\Rightarrow \\vec{z} \\in W^\\perp$.\n\n"
              "**Unicidad:** si $\\vec{y} = \\hat{\\vec{y}} + \\vec{z} = \\hat{\\vec{y}}' + \\vec{z}'$ con ambos $\\hat{\\vec{y}}, \\hat{\\vec{y}}' \\in W$ y $\\vec{z}, \\vec{z}' \\in W^\\perp$, entonces $\\hat{\\vec{y}} - \\hat{\\vec{y}}' = \\vec{z}' - \\vec{z} \\in W \\cap W^\\perp = \\{\\vec{0}\\}$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Descomposición ortogonal",
          problema_md=(
              "Sean $\\vec{u}_1 = (2, 5, -1)^T$, $\\vec{u}_2 = (-2, 1, 1)^T$ (base ortogonal de $W = \\text{Gen}\\{\\vec{u}_1, \\vec{u}_2\\}$) y $\\vec{y} = (1, 2, 3)^T$. Descompón $\\vec{y} = \\hat{\\vec{y}} + \\vec{z}$ con $\\hat{\\vec{y}} \\in W$, $\\vec{z} \\in W^\\perp$."
          ),
          pasos=[
              {"accion_md": (
                  "Productos: $\\vec{y}\\cdot\\vec{u}_1 = 2 + 10 - 3 = 9$, $\\vec{u}_1\\cdot\\vec{u}_1 = 4 + 25 + 1 = 30$.\n\n"
                  "$\\vec{y}\\cdot\\vec{u}_2 = -2 + 2 + 3 = 3$, $\\vec{u}_2\\cdot\\vec{u}_2 = 4 + 1 + 1 = 6$."
              ),
               "justificacion_md": "Productos previos para la fórmula.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\hat{\\vec{y}} = \\dfrac{9}{30}\\vec{u}_1 + \\dfrac{3}{6}\\vec{u}_2 = \\dfrac{9}{30}(2, 5, -1) + \\dfrac{1}{2}(-2, 1, 1) = (3/5 - 1, 3/2 + 1/2, -3/10 + 1/2) = (-2/5, 2, 1/5)^T.$"
              ),
               "justificacion_md": "Suma componente a componente.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\vec{z} = \\vec{y} - \\hat{\\vec{y}} = (1, 2, 3) - (-2/5, 2, 1/5) = (7/5, 0, 14/5)^T.$\n\n"
                  "**Verificación:** $\\vec{z}\\cdot\\vec{u}_1 = 14/5 + 0 - 14/5 = 0$ ✓ y $\\vec{z}\\cdot\\vec{u}_2 = -14/5 + 0 + 14/5 = 0$ ✓."
              ),
               "justificacion_md": "$\\vec{z}$ es ortogonal a la base de $W$ $\\Rightarrow$ ortogonal a todo $W$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Mejor aproximación",
          enunciado_md=(
              "Sean $W$ un subespacio de $\\mathbb{R}^n$ y $\\vec{y} \\in \\mathbb{R}^n$. Si $\\hat{\\vec{y}} = \\text{proy}_W\\,\\vec{y}$, entonces $\\hat{\\vec{y}}$ es el **punto de $W$ más cercano a $\\vec{y}$**:\n\n"
              "$$\\boxed{\\|\\vec{y} - \\hat{\\vec{y}}\\| < \\|\\vec{y} - \\vec{v}\\| \\quad \\text{para todo } \\vec{v} \\in W, \\vec{v} \\neq \\hat{\\vec{y}}.}$$\n\n"
              "**Lectura:** la proyección ortogonal **minimiza la distancia** desde $\\vec{y}$ hasta el subespacio $W$. Es la 'mejor aproximación' de $\\vec{y}$ por elementos de $W$."
          ),
          demostracion_md=(
              "Sea $\\vec{v} \\in W$ arbitrario. Entonces $\\vec{y} - \\vec{v} = (\\vec{y} - \\hat{\\vec{y}}) + (\\hat{\\vec{y}} - \\vec{v})$. El primer sumando $\\in W^\\perp$, el segundo $\\in W$ (resta de elementos de $W$). Como son ortogonales, por Pitágoras:\n\n"
              "$\\|\\vec{y} - \\vec{v}\\|^2 = \\|\\vec{y} - \\hat{\\vec{y}}\\|^2 + \\|\\hat{\\vec{y}} - \\vec{v}\\|^2 \\geq \\|\\vec{y} - \\hat{\\vec{y}}\\|^2$.\n\n"
              "Igualdad solo si $\\hat{\\vec{y}} = \\vec{v}$. $\\blacksquare$"
          )),

        b("intuicion", body_md=(
            "**Aplicación directa: aproximación por subespacios.**\n\n"
            "Si $W$ representa un 'modelo simplificado' (ej., $W$ = funciones lineales, polinomios de grado $\\leq k$), y $\\vec{y}$ es un dato real complejo, entonces $\\hat{\\vec{y}} = \\text{proy}_W\\,\\vec{y}$ es **la mejor aproximación de $\\vec{y}$ dentro del modelo**.\n\n"
            "Esta es la idea germen de:\n\n"
            "- **Mínimos cuadrados** (lección 7.5): aproximar datos $\\vec{b}$ por elementos de $\\text{Col}\\,A$.\n"
            "- **Series de Fourier**: aproximar funciones por sumas finitas de senos y cosenos.\n"
            "- **Análisis de componentes principales (PCA)**: proyectar datos a un subespacio de baja dimensión que preserve la varianza."
        )),

        b("teorema",
          nombre="Proyección con base ortonormal",
          enunciado_md=(
              "Si $\\{\\vec{u}_1, \\ldots, \\vec{u}_p\\}$ es una **base ortonormal** de $W$ (i.e., $\\vec{u}_j\\cdot\\vec{u}_j = 1$), la fórmula simplifica:\n\n"
              "$$\\text{proy}_W\\,\\vec{y} = (\\vec{y}\\cdot\\vec{u}_1)\\vec{u}_1 + \\cdots + (\\vec{y}\\cdot\\vec{u}_p)\\vec{u}_p.$$\n\n"
              "Equivalentemente, en forma **matricial**, si $U = [\\vec{u}_1\\ \\cdots\\ \\vec{u}_p]$ tiene como columnas la base ortonormal:\n\n"
              "$$\\boxed{\\text{proy}_W\\,\\vec{y} = U U^T \\vec{y}.}$$\n\n"
              "$P = U U^T$ se llama la **matriz de proyección sobre $W$**, y satisface $P^2 = P$ (idempotente) y $P^T = P$ (simétrica)."
          ),
          demostracion_md=(
              "$U^T \\vec{y} = (\\vec{u}_1\\cdot\\vec{y}, \\ldots, \\vec{u}_p\\cdot\\vec{y})^T$. Multiplicar por $U$ a la izquierda da $\\sum (\\vec{y}\\cdot\\vec{u}_j)\\vec{u}_j$, que es la fórmula de proyección. $\\blacksquare$\n\n"
              "**Idempotencia $P^2 = P$:** proyectar un vector ya proyectado da el mismo vector. **Simetría $P^T = P$:** distintas formas equivalentes."
          )),

        b("ejemplo_resuelto",
          titulo="Proyección con matriz $UU^T$",
          problema_md=(
              "Sea $W = \\text{Gen}\\{\\vec{u}_1, \\vec{u}_2\\}$ con $\\vec{u}_1 = (1/\\sqrt{2}, 1/\\sqrt{2}, 0)^T$ y $\\vec{u}_2 = (0, 0, 1)^T$ (ortonormal). Halla $\\text{proy}_W\\,\\vec{y}$ para $\\vec{y} = (3, 5, 7)^T$ usando la fórmula matricial."
          ),
          pasos=[
              {"accion_md": (
                  "$U = \\begin{bmatrix} 1/\\sqrt{2} & 0 \\\\ 1/\\sqrt{2} & 0 \\\\ 0 & 1 \\end{bmatrix}$, $U^T \\vec{y} = \\begin{bmatrix} 3/\\sqrt{2} + 5/\\sqrt{2} \\\\ 7 \\end{bmatrix} = \\begin{bmatrix} 8/\\sqrt{2} \\\\ 7 \\end{bmatrix} = \\begin{bmatrix} 4\\sqrt{2} \\\\ 7 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Productos punto $\\vec{y}\\cdot\\vec{u}_j$.",
               "es_resultado": False},
              {"accion_md": (
                  "$U(U^T \\vec{y}) = 4\\sqrt{2}\\,\\vec{u}_1 + 7\\,\\vec{u}_2 = 4\\sqrt{2}(1/\\sqrt{2}, 1/\\sqrt{2}, 0) + 7(0, 0, 1) = (4, 4, 7)^T.$\n\n"
                  "**$\\text{proy}_W\\,\\vec{y} = (4, 4, 7)^T$.**"
              ),
               "justificacion_md": "**Geometría:** $W$ es el plano $x = y$, así $\\vec{y} = (3, 5, 7)$ se proyecta promediando las dos primeras componentes.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El teorema de la mejor aproximación dice que $\\hat{\\vec{y}} = \\text{proy}_W\\,\\vec{y}$:",
                  "opciones_md": [
                      "Es el punto de $W^\\perp$ más cercano a $\\vec{y}$",
                      "Es el punto de $W$ más cercano a $\\vec{y}$",
                      "Es el punto de $\\mathbb{R}^n$ más alejado de $\\vec{y}$",
                      "Es siempre el origen",
                  ],
                  "correcta": "B",
                  "pista_md": "Minimiza $\\|\\vec{y} - \\vec{v}\\|$ para $\\vec{v} \\in W$.",
                  "explicacion_md": "**El punto de $W$ más cercano a $\\vec{y}$.** La distancia mínima es $\\|\\vec{y} - \\hat{\\vec{y}}\\| = \\|\\vec{z}\\|$ (norma de la componente ortogonal).",
              },
              {
                  "enunciado_md": "Si $U \\in \\mathbb{R}^{n \\times p}$ tiene columnas ortonormales que generan $W$, $\\text{proy}_W\\,\\vec{y}$ vale:",
                  "opciones_md": ["$U^T U \\vec{y}$", "$U U^T \\vec{y}$", "$U \\vec{y}$", "$\\|\\vec{y}\\|\\,\\vec{u}_1$"],
                  "correcta": "B",
                  "pista_md": "Multiplicar $\\vec{y}$ primero por $U^T$ y luego por $U$.",
                  "explicacion_md": "**$\\text{proy}_W\\,\\vec{y} = UU^T\\vec{y}$.** $U^TU = I$ (Gram), pero $UU^T$ proyecta sobre $\\text{Col}\\,U = W$.",
              },
              {
                  "enunciado_md": "Si $\\vec{y} \\in W$, entonces $\\text{proy}_W\\,\\vec{y}$ vale:",
                  "opciones_md": ["$\\vec{0}$", "$\\vec{y}$", "$-\\vec{y}$", "$\\|\\vec{y}\\|$"],
                  "correcta": "B",
                  "pista_md": "Si $\\vec{y}$ ya está en $W$, no hace falta proyectar.",
                  "explicacion_md": "**$\\vec{y}$ mismo.** El punto de $W$ más cercano a $\\vec{y} \\in W$ es $\\vec{y}$. Idempotencia: proyectar lo ya proyectado no cambia.",
              },
          ]),

        ej(
            "Proyección sobre plano",
            "Sea $W = \\text{Gen}\\{\\vec{u}_1, \\vec{u}_2\\}$ con $\\vec{u}_1 = (1, 0, 1)^T$, $\\vec{u}_2 = (1, 1, -1)^T$ (ortogonal). Proyecta $\\vec{y} = (4, 8, 1)^T$ sobre $W$.",
            ["Verifica ortogonalidad y aplica la fórmula con base ortogonal."],
            (
                "$\\vec{u}_1\\cdot\\vec{u}_2 = 1 + 0 - 1 = 0$ ✓.\n\n"
                "$\\vec{y}\\cdot\\vec{u}_1 = 4 + 0 + 1 = 5$, $\\vec{u}_1\\cdot\\vec{u}_1 = 2$. $\\vec{y}\\cdot\\vec{u}_2 = 4 + 8 - 1 = 11$, $\\vec{u}_2\\cdot\\vec{u}_2 = 3$.\n\n"
                "$\\hat{\\vec{y}} = (5/2)(1, 0, 1) + (11/3)(1, 1, -1) = (5/2 + 11/3, 11/3, 5/2 - 11/3) = (37/6, 11/3, -7/6)$."
            ),
        ),

        ej(
            "Distancia desde un vector a un subespacio",
            "Para el ejercicio anterior, halla $\\text{dist}(\\vec{y}, W) = \\|\\vec{y} - \\hat{\\vec{y}}\\|$.",
            ["Calcula $\\vec{z}$ y su norma."],
            (
                "$\\vec{z} = \\vec{y} - \\hat{\\vec{y}} = (4 - 37/6, 8 - 11/3, 1 - (-7/6)) = (-13/6, 13/3, 13/6)$.\n\n"
                "$\\|\\vec{z}\\| = \\sqrt{169/36 + 169/9 + 169/36} = \\sqrt{169(1/36 + 4/36 + 1/36)} = 13\\sqrt{6/36} = 13/\\sqrt{6} \\approx 5.31$."
            ),
        ),

        ej(
            "Matriz de proyección",
            "Sea $\\vec{u} = (1, 1, 1)^T/\\sqrt{3}$ (unitario). Halla la matriz $P = \\vec{u}\\vec{u}^T$ de proyección sobre la recta generada por $\\vec{u}$. Verifica $P^2 = P$.",
            ["$P = U U^T$ con $U = [\\vec{u}]$."],
            (
                "$P = \\dfrac{1}{3}\\begin{bmatrix} 1 \\\\ 1 \\\\ 1 \\end{bmatrix}\\begin{bmatrix} 1 & 1 & 1 \\end{bmatrix} = \\dfrac{1}{3}\\begin{bmatrix} 1 & 1 & 1 \\\\ 1 & 1 & 1 \\\\ 1 & 1 & 1 \\end{bmatrix}.$\n\n"
                "$P^2 = \\dfrac{1}{9}\\begin{bmatrix} 1 & 1 & 1 \\\\ 1 & 1 & 1 \\\\ 1 & 1 & 1 \\end{bmatrix}\\begin{bmatrix} 1 & 1 & 1 \\\\ 1 & 1 & 1 \\\\ 1 & 1 & 1 \\end{bmatrix} = \\dfrac{1}{9}\\begin{bmatrix} 3 & 3 & 3 \\\\ 3 & 3 & 3 \\\\ 3 & 3 & 3 \\end{bmatrix} = P$ ✓ (idempotente)."
            ),
        ),

        fig(
            "Diagrama 3D con un plano W teal #06b6d4 semitransparente pasando por el origen. Vector v gris saliendo "
            "del origen, hacia arriba, fuera del plano. Su proyección proy_W(v) teal cae sobre el plano. Vector z "
            "ámbar #f59e0b perpendicular al plano va desde la punta de proy_W(v) hasta la punta de v. Triángulo "
            "rectángulo destacado con marca de ángulo recto. Etiqueta: 'v = proy_W(v) + z'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar la fórmula simple $(\\vec{y}\\cdot\\vec{u}_j)\\vec{u}_j$ con base no ortonormal.** Solo vale para **ortonormal** ($\\vec{u}_j\\cdot\\vec{u}_j = 1$). Para ortogonal hay que dividir por $\\vec{u}_j\\cdot\\vec{u}_j$.",
              "**Confundir $UU^T$ con $U^TU$.** $U^TU = I_p$ (cuando hay ortonormalidad), $UU^T$ es la matriz de proyección $P$ (de tamaño $n \\times n$).",
              "**Olvidar que $\\hat{\\vec{y}}$ es independiente de la base ortogonal elegida.** Distintas bases dan los mismos pesos finales.",
              "**Pensar que $P = UU^T$ es invertible.** **No lo es** si $p < n$ — proyectar es una operación 'destructiva' (pierde información sobre $W^\\perp$).",
              "**Proyectar sobre una base no-ortogonal sin ortogonalizarla primero.** El método requiere base ortogonal — si no, hay que aplicar Gram-Schmidt (lección 7.4) o resolver $A^TA\\vec{x} = A^T\\vec{y}$ (lección 7.5).",
          ]),

        b("resumen",
          puntos_md=[
              "**Descomposición ortogonal:** $\\vec{y} = \\hat{\\vec{y}} + \\vec{z}$ con $\\hat{\\vec{y}} \\in W$, $\\vec{z} \\in W^\\perp$.",
              "**Fórmula con base ortogonal:** $\\hat{\\vec{y}} = \\sum (\\vec{y}\\cdot\\vec{u}_j)/(\\vec{u}_j\\cdot\\vec{u}_j) \\vec{u}_j$.",
              "**Mejor aproximación:** $\\hat{\\vec{y}}$ es el punto de $W$ más cercano a $\\vec{y}$.",
              "**Forma matricial (base ortonormal):** $\\text{proy}_W\\,\\vec{y} = U U^T \\vec{y}$.",
              "**Matriz de proyección:** $P = UU^T$ es **idempotente** ($P^2 = P$) y **simétrica** ($P^T = P$).",
              "**Próxima lección:** **Gram-Schmidt** — construir bases ortonormales a partir de cualquier base.",
          ]),
    ]
    return {
        "id": "lec-al-7-3-proyecciones-ortogonales",
        "title": "Proyecciones ortogonales",
        "description": "Descomposición $\\vec{y} = \\hat{\\vec{y}} + \\vec{z}$ con $\\hat{\\vec{y}} \\in W$, $\\vec{z} \\in W^\\perp$, teorema de la mejor aproximación, fórmula matricial $\\text{proy}_W\\,\\vec{y} = UU^T\\vec{y}$.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 7.4 Proceso de Gram-Schmidt
# =====================================================================
def lesson_7_4():
    blocks = [
        b("texto", body_md=(
            "El **proceso de Gram-Schmidt** es un algoritmo que **convierte cualquier base** $\\{\\vec{x}_1, \\ldots, \\vec{x}_p\\}$ "
            "**en una base ortogonal** $\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$ del **mismo subespacio**. Normalizando cada $\\vec{v}_i$ "
            "se obtiene una base ortonormal.\n\n"
            "**Idea:** ir construyendo los $\\vec{v}_i$ uno por uno, restando a cada $\\vec{x}_i$ su proyección sobre el subespacio "
            "ya generado por los anteriores.\n\n"
            "Como aplicación inmediata, Gram-Schmidt produce la **factorización QR**: si $A$ tiene columnas LI, entonces $A = QR$ "
            "con $Q$ de columnas ortonormales y $R$ triangular superior. La factorización QR es la base de algoritmos numéricos "
            "estables para mínimos cuadrados, valores propios, etc.\n\n"
            "Al terminar:\n\n"
            "- Aplicas el algoritmo de Gram-Schmidt paso a paso.\n"
            "- Construyes bases ortonormales por normalización.\n"
            "- Conoces la **factorización QR** $A = QR$.\n"
            "- Sabes **completar** un conjunto LI a base ortogonal de $\\mathbb{R}^n$."
        )),

        b("teorema",
          nombre="Proceso de Gram-Schmidt",
          enunciado_md=(
              "Dada una base $\\{\\vec{x}_1, \\ldots, \\vec{x}_p\\}$ de un subespacio $W \\subseteq \\mathbb{R}^n$, definimos:\n\n"
              "$$\\vec{v}_1 = \\vec{x}_1$$\n\n"
              "$$\\vec{v}_2 = \\vec{x}_2 - \\frac{\\vec{x}_2\\cdot\\vec{v}_1}{\\vec{v}_1\\cdot\\vec{v}_1}\\vec{v}_1$$\n\n"
              "$$\\vec{v}_3 = \\vec{x}_3 - \\frac{\\vec{x}_3\\cdot\\vec{v}_1}{\\vec{v}_1\\cdot\\vec{v}_1}\\vec{v}_1 - \\frac{\\vec{x}_3\\cdot\\vec{v}_2}{\\vec{v}_2\\cdot\\vec{v}_2}\\vec{v}_2$$\n\n"
              "$$\\vdots$$\n\n"
              "$$\\boxed{\\vec{v}_k = \\vec{x}_k - \\sum_{j=1}^{k-1} \\frac{\\vec{x}_k\\cdot\\vec{v}_j}{\\vec{v}_j\\cdot\\vec{v}_j}\\vec{v}_j.}$$\n\n"
              "Entonces $\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$ es una **base ortogonal** de $W$, y\n\n"
              "$$\\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_k\\} = \\text{Gen}\\{\\vec{x}_1, \\ldots, \\vec{x}_k\\}, \\quad 1 \\leq k \\leq p.$$\n\n"
              "**Idea geométrica:** $\\vec{v}_k$ se obtiene quitándole a $\\vec{x}_k$ su componente en el subespacio ya construido $W_{k-1} = \\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_{k-1}\\}$. Lo que queda es ortogonal a $W_{k-1}$.\n\n"
              "**Para una base ortonormal:** normalizar cada $\\vec{v}_k$ a $\\vec{u}_k = \\vec{v}_k/\\|\\vec{v}_k\\|$ — usualmente conviene hacerlo al final para evitar fracciones."
          )),

        b("ejemplo_resuelto",
          titulo="Gram-Schmidt en $\\mathbb{R}^4$",
          problema_md=(
              "Aplica Gram-Schmidt a $\\vec{x}_1 = (1, 1, 1, 1)^T$, $\\vec{x}_2 = (0, 1, 1, 1)^T$, $\\vec{x}_3 = (0, 0, 1, 1)^T$ para construir una base ortogonal del subespacio $W = \\text{Gen}\\{\\vec{x}_1, \\vec{x}_2, \\vec{x}_3\\}$."
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1:** $\\vec{v}_1 = \\vec{x}_1 = (1, 1, 1, 1)^T$.\n\n"
                  "**Paso 2:** $\\vec{x}_2\\cdot\\vec{v}_1 = 0+1+1+1 = 3$. $\\vec{v}_1\\cdot\\vec{v}_1 = 4$.\n\n"
                  "$\\vec{v}_2 = \\vec{x}_2 - \\dfrac{3}{4}\\vec{v}_1 = (0,1,1,1) - (3/4, 3/4, 3/4, 3/4) = (-3/4, 1/4, 1/4, 1/4)^T.$\n\n"
                  "**Escalando** por $4$: $\\vec{v}_2' = (-3, 1, 1, 1)^T$ (el subespacio generado no cambia)."
              ),
               "justificacion_md": "Restar la proyección sobre $\\vec{v}_1$. Escalar para limpiar fracciones.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3:** $\\vec{x}_3\\cdot\\vec{v}_1 = 2$, $\\vec{x}_3\\cdot\\vec{v}_2' = 0 + 1 + 1 = 2$. $\\vec{v}_1\\cdot\\vec{v}_1 = 4$, $\\vec{v}_2'\\cdot\\vec{v}_2' = 9 + 1 + 1 + 1 = 12$.\n\n"
                  "$\\vec{v}_3 = \\vec{x}_3 - \\dfrac{2}{4}\\vec{v}_1 - \\dfrac{2}{12}\\vec{v}_2' = (0, 0, 1, 1) - (1/2, 1/2, 1/2, 1/2) - (1/6)(-3, 1, 1, 1)$\n\n"
                  "$= (0 - 1/2 + 1/2,\\ 0 - 1/2 - 1/6,\\ 1 - 1/2 - 1/6,\\ 1 - 1/2 - 1/6) = (0, -2/3, 1/3, 1/3)^T.$\n\n"
                  "Escalando por $3$: $\\vec{v}_3' = (0, -2, 1, 1)^T$."
              ),
               "justificacion_md": "Restar proyecciones sobre los dos vectores ortogonales ya construidos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Base ortogonal:** $\\{(1,1,1,1)^T, (-3, 1, 1, 1)^T, (0, -2, 1, 1)^T\\}$.\n\n"
                  "**Verificación:** $\\vec{v}_1\\cdot\\vec{v}_2' = -3 + 1 + 1 + 1 = 0$ ✓, $\\vec{v}_1\\cdot\\vec{v}_3' = 0 - 2 + 1 + 1 = 0$ ✓, $\\vec{v}_2'\\cdot\\vec{v}_3' = 0 - 2 + 1 + 1 = 0$ ✓."
              ),
               "justificacion_md": "Los $3$ vectores son mutuamente ortogonales. Span igual al original.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Base ortonormal por normalización",
          body_md=(
              "Dada la base ortogonal $\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$ producida por Gram-Schmidt, la **base ortonormal** correspondiente es\n\n"
              "$$\\vec{u}_k = \\dfrac{\\vec{v}_k}{\\|\\vec{v}_k\\|}, \\qquad k = 1, \\ldots, p.$$\n\n"
              "**Práctica recomendada:** normalizar al final, después de aplicar Gram-Schmidt y escalar cada $\\vec{v}_k$ para limpiar fracciones. Normalizar **dentro** del proceso introduce muchas raíces cuadradas innecesarias."
          )),

        b("ejemplo_resuelto",
          titulo="Normalización a base ortonormal",
          problema_md=(
              "Normaliza la base ortogonal $\\vec{v}_1 = (3, 6, 0)^T$, $\\vec{v}_2 = (0, 0, 2)^T$ del subespacio $W \\subseteq \\mathbb{R}^3$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\|\\vec{v}_1\\| = \\sqrt{9 + 36 + 0} = \\sqrt{45} = 3\\sqrt{5}$.\n\n"
                  "$\\vec{u}_1 = \\dfrac{1}{3\\sqrt{5}}(3, 6, 0)^T = (1/\\sqrt{5},\\ 2/\\sqrt{5},\\ 0)^T.$"
              ),
               "justificacion_md": "Dividir por la norma.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\|\\vec{v}_2\\| = 2$. $\\vec{u}_2 = (0, 0, 1)^T.$\n\n"
                  "**Base ortonormal:** $\\{(1/\\sqrt{5}, 2/\\sqrt{5}, 0)^T,\\ (0, 0, 1)^T\\}$."
              ),
               "justificacion_md": "Cada $\\vec{u}_k$ tiene norma $1$ y son ortogonales por construcción.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Factorización QR",
          enunciado_md=(
              "Si $A \\in \\mathbb{R}^{m \\times n}$ tiene **columnas linealmente independientes**, entonces $A$ se factoriza como\n\n"
              "$$\\boxed{A = QR,}$$\n\n"
              "donde:\n\n"
              "- $Q \\in \\mathbb{R}^{m \\times n}$ tiene **columnas ortonormales** que generan $\\text{Col}\\,A$.\n"
              "- $R \\in \\mathbb{R}^{n \\times n}$ es **triangular superior invertible** con entradas positivas en la diagonal.\n\n"
              "**Construcción:** $Q$ se obtiene aplicando Gram-Schmidt y normalización a las columnas de $A$. Una vez obtenida $Q$, $R = Q^T A$ (porque $Q^T Q = I$).\n\n"
              "**Aplicaciones:** la factorización QR es la base de:\n\n"
              "- **Mínimos cuadrados** numéricamente estables (lección 7.5).\n"
              "- **Algoritmo QR** para calcular valores propios.\n"
              "- **Resolución de sistemas** mal condicionados."
          )),

        b("ejemplo_resuelto",
          titulo="Factorización QR",
          problema_md=(
              "Encuentra una factorización QR de $A = \\begin{bmatrix} 1 & 0 & 0 \\\\ 1 & 1 & 0 \\\\ 1 & 1 & 1 \\\\ 1 & 1 & 1 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Las columnas son $\\vec{x}_1, \\vec{x}_2, \\vec{x}_3$ del ejemplo de Gram-Schmidt anterior. Ya obtuvimos la base ortogonal $\\{(1,1,1,1)^T, (-3,1,1,1)^T, (0,-2,1,1)^T\\}$ con normas $2, \\sqrt{12}, \\sqrt{6}$."
              ),
               "justificacion_md": "Reusamos el cómputo de Gram-Schmidt previo.",
               "es_resultado": False},
              {"accion_md": (
                  "Normalizamos para obtener $Q$:\n\n"
                  "$Q = \\begin{bmatrix} 1/2 & -3/\\sqrt{12} & 0 \\\\ 1/2 & 1/\\sqrt{12} & -2/\\sqrt{6} \\\\ 1/2 & 1/\\sqrt{12} & 1/\\sqrt{6} \\\\ 1/2 & 1/\\sqrt{12} & 1/\\sqrt{6} \\end{bmatrix}.$"
              ),
               "justificacion_md": "Cada columna es $\\vec{v}_k/\\|\\vec{v}_k\\|$.",
               "es_resultado": False},
              {"accion_md": (
                  "$R = Q^T A$ (calculo directo) $= \\begin{bmatrix} 2 & 3/2 & 1 \\\\ 0 & 3/\\sqrt{12} & 2/\\sqrt{12} \\\\ 0 & 0 & 2/\\sqrt{6} \\end{bmatrix}.$\n\n"
                  "**$A = QR$.** $R$ triangular superior con diagonal positiva (verificable: $\\sqrt{12}/2 \\cdot 3 = 3\\sqrt{12}/2$, etc., todas positivas)."
              ),
               "justificacion_md": "**Forma estándar de factorización QR.** Útil para resolver $A\\vec{x} = \\vec{b}$ y mínimos cuadrados.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Completar a base ortogonal de $\\mathbb{R}^n$.** Si tenemos un conjunto LI $\\{\\vec{x}_1, \\ldots, \\vec{x}_k\\}$ con $k < n$:\n\n"
            "1. Aplicar Gram-Schmidt para obtener $\\{\\vec{v}_1, \\ldots, \\vec{v}_k\\}$ ortogonal.\n"
            "2. Agregar vectores adicionales $\\vec{x}_{k+1}, \\ldots, \\vec{x}_n$ que **completen una base de $\\mathbb{R}^n$** (típicamente vectores de la base canónica que no estén en el gen).\n"
            "3. Volver a aplicar Gram-Schmidt al conjunto completo para obtener $\\{\\vec{v}_1, \\ldots, \\vec{v}_n\\}$ ortogonal de $\\mathbb{R}^n$.\n"
            "4. Normalizar si se desea base ortonormal.\n\n"
            "**Atajo:** los vectores nuevos en el paso 2 pueden tomarse como base de $W^\\perp$ (donde $W = \\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_k\\}$), y entonces ya son ortogonales al resto."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El primer vector $\\vec{v}_1$ de Gram-Schmidt aplicado a $\\{\\vec{x}_1, \\vec{x}_2, \\ldots\\}$ es:",
                  "opciones_md": [
                      "$\\vec{x}_1$ normalizado",
                      "$\\vec{x}_1$ tal cual",
                      "$\\vec{x}_2 - \\vec{x}_1$",
                      "$\\vec{0}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Inicialización del algoritmo.",
                  "explicacion_md": "**$\\vec{v}_1 = \\vec{x}_1$.** Sin modificar (la normalización es opcional al final).",
              },
              {
                  "enunciado_md": "Después de Gram-Schmidt sobre $\\{\\vec{x}_1, \\vec{x}_2, \\vec{x}_3\\}$, el span de $\\{\\vec{v}_1, \\vec{v}_2\\}$ vale:",
                  "opciones_md": [
                      "$\\text{Gen}\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3\\}$",
                      "$\\text{Gen}\\{\\vec{x}_1, \\vec{x}_2\\}$",
                      "Solo la recta $\\text{Gen}\\{\\vec{v}_1\\}$",
                      "$\\mathbb{R}^n$",
                  ],
                  "correcta": "B",
                  "pista_md": "Gram-Schmidt preserva spans parciales.",
                  "explicacion_md": "**$\\text{Gen}\\{\\vec{x}_1, \\vec{x}_2\\}$.** El proceso preserva spans intermedios — propiedad útil para QR.",
              },
              {
                  "enunciado_md": "En $A = QR$, ¿qué tamaño tiene $R$?",
                  "opciones_md": ["$m \\times m$", "$m \\times n$", "$n \\times n$", "$n \\times m$"],
                  "correcta": "C",
                  "pista_md": "$Q \\in \\mathbb{R}^{m\\times n}$ y $R$ debe encajar en el producto.",
                  "explicacion_md": "**$R \\in \\mathbb{R}^{n\\times n}$**, triangular superior invertible.",
              },
          ]),

        ej(
            "Gram-Schmidt en $\\mathbb{R}^3$",
            "Aplica Gram-Schmidt a $\\vec{x}_1 = (3, 6, 0)^T$, $\\vec{x}_2 = (1, 2, 2)^T$.",
            ["$\\vec{v}_1 = \\vec{x}_1$. $\\vec{v}_2 = \\vec{x}_2 - \\text{proy}_{\\vec{v}_1}\\vec{x}_2$."],
            (
                "$\\vec{v}_1 = (3, 6, 0)$.\n\n"
                "$\\vec{x}_2\\cdot\\vec{v}_1 = 3 + 12 + 0 = 15$, $\\vec{v}_1\\cdot\\vec{v}_1 = 45$.\n\n"
                "$\\vec{v}_2 = (1, 2, 2) - (15/45)(3, 6, 0) = (1, 2, 2) - (1, 2, 0) = (0, 0, 2)$.\n\n"
                "**Base ortogonal:** $\\{(3, 6, 0), (0, 0, 2)\\}$. Verificación: $\\vec{v}_1\\cdot\\vec{v}_2 = 0$ ✓."
            ),
        ),

        ej(
            "Normalización",
            "Convierte la base ortogonal $\\{(2, 0, 1), (-1, 0, 2), (0, 1, 0)\\}$ de $\\mathbb{R}^3$ en ortonormal.",
            ["Calcula la norma de cada vector y divide."],
            (
                "Normas: $\\sqrt{5}, \\sqrt{5}, 1$.\n\n"
                "Base ortonormal: $\\{(2/\\sqrt{5}, 0, 1/\\sqrt{5}), (-1/\\sqrt{5}, 0, 2/\\sqrt{5}), (0, 1, 0)\\}$."
            ),
        ),

        ej(
            "QR de matriz $3\\times 2$",
            "Encuentra QR de $A = \\begin{bmatrix} 1 & 1 \\\\ 1 & -1 \\\\ 1 & 4 \\end{bmatrix}$.",
            ["Aplica Gram-Schmidt a las columnas. Normaliza para $Q$. $R = Q^T A$."],
            (
                "$\\vec{x}_1 = (1, 1, 1)$, $\\vec{x}_2 = (1, -1, 4)$.\n\n"
                "$\\vec{v}_1 = \\vec{x}_1$. $\\vec{x}_2\\cdot\\vec{v}_1 = 1 - 1 + 4 = 4$, $\\vec{v}_1\\cdot\\vec{v}_1 = 3$.\n\n"
                "$\\vec{v}_2 = (1,-1,4) - (4/3)(1,1,1) = (-1/3, -7/3, 8/3)$. Escalando por $3$: $(-1, -7, 8)$.\n\n"
                "Normas: $\\|\\vec{v}_1\\| = \\sqrt{3}$, $\\|(-1,-7,8)\\| = \\sqrt{114}$.\n\n"
                "$Q = \\begin{bmatrix} 1/\\sqrt{3} & -1/\\sqrt{114} \\\\ 1/\\sqrt{3} & -7/\\sqrt{114} \\\\ 1/\\sqrt{3} & 8/\\sqrt{114} \\end{bmatrix}$, $R = Q^T A = \\begin{bmatrix} \\sqrt{3} & 4/\\sqrt{3} \\\\ 0 & \\sqrt{114}/3 \\end{bmatrix}$."
            ),
        ),

        fig(
            "Tres paneles secuenciales en R^3 mostrando Gram-Schmidt. Panel 1: vectores v1, v2, v3 grises no "
            "ortogonales y u1=v1 teal #06b6d4. Panel 2: agrega u2 = v2 - proy_{u1}(v2) ámbar #f59e0b, con la "
            "resta dibujada y u1 perpendicular a u2. Panel 3: agrega u3 púrpura ortogonal al plano de u1, u2, "
            "con marcas de ángulo recto. Flechas entre paneles. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar restar todas las proyecciones previas en cada paso.** El paso $k$ resta proyecciones sobre $\\vec{v}_1, \\ldots, \\vec{v}_{k-1}$ — todas, no solo la última.",
              "**Normalizar antes de tiempo.** Mejor escalar para limpiar fracciones durante el proceso y normalizar al final.",
              "**Confundir Gram-Schmidt con eliminación de Gauss.** Son procesos completamente distintos: Gauss simplifica matrices; Gram-Schmidt construye vectores ortogonales.",
              "**Aplicar Gram-Schmidt a un conjunto LD.** El proceso requiere que los $\\vec{x}_i$ sean **LI** — si no, algún $\\vec{v}_k$ saldrá $\\vec{0}$.",
              "**Pensar que $Q$ debe ser cuadrada.** En general $Q \\in \\mathbb{R}^{m\\times n}$ con $m \\geq n$ y solo cumple $Q^TQ = I_n$, no $QQ^T = I_m$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Gram-Schmidt:** $\\vec{v}_k = \\vec{x}_k - \\sum_{j<k} \\text{proy}_{\\vec{v}_j}\\vec{x}_k$.",
              "Produce **base ortogonal** del mismo subespacio. Spans parciales se preservan.",
              "**Normalizar al final** para obtener base ortonormal.",
              "**Factorización QR:** $A = QR$ con $Q$ de columnas ortonormales y $R$ triangular superior invertible.",
              "**$R = Q^T A$** una vez obtenida $Q$.",
              "**Completar bases:** se puede extender un conjunto LI a base ortogonal de $\\mathbb{R}^n$ aplicando Gram-Schmidt al conjunto extendido.",
              "**Próxima lección:** **mínimos cuadrados** — usar proyecciones ortogonales para resolver sistemas inconsistentes.",
          ]),
    ]
    return {
        "id": "lec-al-7-4-gram-schmidt",
        "title": "Proceso de Gram-Schmidt",
        "description": "Algoritmo $\\vec{v}_k = \\vec{x}_k - \\sum \\text{proy}_{\\vec{v}_j}\\vec{x}_k$ para construir bases ortogonales/ortonormales, factorización QR $A = QR$.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# =====================================================================
# 7.5 Mínimos cuadrados
# =====================================================================
def lesson_7_5():
    blocks = [
        b("texto", body_md=(
            "Los sistemas $A\\vec{x} = \\vec{b}$ del mundo real son frecuentemente **inconsistentes** — el vector "
            "$\\vec{b}$ no pertenece a $\\text{Col}\\,A$. En lugar de rendirnos, buscamos la **mejor aproximación**: "
            "el vector $\\hat{\\vec{x}}$ que hace $A\\hat{\\vec{x}}$ lo más cercano posible a $\\vec{b}$ en norma euclídea.\n\n"
            "Esta es la idea del **método de mínimos cuadrados**. Geométricamente, $A\\hat{\\vec{x}}$ es la proyección "
            "ortogonal de $\\vec{b}$ sobre $\\text{Col}\\,A$. Algebraicamente, $\\hat{\\vec{x}}$ se obtiene resolviendo "
            "las **ecuaciones normales** $A^TA\\hat{\\vec{x}} = A^T\\vec{b}$.\n\n"
            "Mínimos cuadrados es la herramienta central de:\n\n"
            "- **Estadística:** regresión lineal y modelos predictivos.\n"
            "- **Machine learning:** ajuste de modelos.\n"
            "- **Procesamiento de señales:** filtrado y reconstrucción.\n"
            "- **Geodesia, ingeniería, física experimental:** ajuste de mediciones.\n\n"
            "Al terminar:\n\n"
            "- Defines y resuelves el problema de mínimos cuadrados.\n"
            "- Aplicas las **ecuaciones normales** $A^TA\\hat{\\vec{x}} = A^T\\vec{b}$.\n"
            "- Calculas el **error de mínimos cuadrados** $\\|\\vec{b} - A\\hat{\\vec{x}}\\|$.\n"
            "- Conoces la solución vía **factorización QR**: $\\hat{\\vec{x}} = R^{-1}Q^T\\vec{b}$."
        )),

        b("definicion",
          titulo="Solución de mínimos cuadrados",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{m \\times n}$ y $\\vec{b} \\in \\mathbb{R}^m$. Una **solución de mínimos cuadrados** de $A\\vec{x} = \\vec{b}$ es un vector $\\hat{\\vec{x}} \\in \\mathbb{R}^n$ tal que\n\n"
              "$$\\boxed{\\|\\vec{b} - A\\hat{\\vec{x}}\\| \\leq \\|\\vec{b} - A\\vec{x}\\| \\quad \\forall \\vec{x} \\in \\mathbb{R}^n.}$$\n\n"
              "**Interpretación geométrica.** Como $A\\vec{x}$ siempre pertenece a $\\text{Col}\\,A$, buscamos que $A\\hat{\\vec{x}}$ sea el **punto de $\\text{Col}\\,A$ más cercano a $\\vec{b}$**:\n\n"
              "$$A\\hat{\\vec{x}} = \\hat{\\vec{b}} = \\text{proy}_{\\text{Col}\\,A}\\,\\vec{b}.$$\n\n"
              "Por el teorema de la mejor aproximación, este $\\hat{\\vec{b}}$ existe y es único."
          )),

        b("teorema",
          nombre="Ecuaciones normales",
          enunciado_md=(
              "$\\hat{\\vec{x}}$ es solución de mínimos cuadrados de $A\\vec{x} = \\vec{b}$ si y solo si satisface las **ecuaciones normales**:\n\n"
              "$$\\boxed{A^T A \\hat{\\vec{x}} = A^T \\vec{b}.}$$"
          ),
          demostracion_md=(
              "$A\\hat{\\vec{x}} = \\hat{\\vec{b}}$ (proyección) $\\iff \\vec{b} - A\\hat{\\vec{x}} \\in (\\text{Col}\\,A)^\\perp = \\text{Nul}\\,A^T$ (lección 7.1)\n\n"
              "$\\iff A^T(\\vec{b} - A\\hat{\\vec{x}}) = \\vec{0} \\iff A^T A\\hat{\\vec{x}} = A^T\\vec{b}$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Mínimos cuadrados con ecuaciones normales",
          problema_md=(
              "Encuentra una solución de mínimos cuadrados del sistema **inconsistente** $A\\vec{x} = \\vec{b}$ con $A = \\begin{bmatrix} 4 & 0 \\\\ 0 & 2 \\\\ 1 & 1 \\end{bmatrix}$ y $\\vec{b} = (2, 0, 11)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "Calcular $A^T A$ y $A^T \\vec{b}$:\n\n"
                  "$A^T A = \\begin{bmatrix} 4 & 0 & 1 \\\\ 0 & 2 & 1 \\end{bmatrix}\\begin{bmatrix} 4 & 0 \\\\ 0 & 2 \\\\ 1 & 1 \\end{bmatrix} = \\begin{bmatrix} 17 & 1 \\\\ 1 & 5 \\end{bmatrix}.$\n\n"
                  "$A^T \\vec{b} = \\begin{bmatrix} 4 & 0 & 1 \\\\ 0 & 2 & 1 \\end{bmatrix}\\begin{bmatrix} 2 \\\\ 0 \\\\ 11 \\end{bmatrix} = \\begin{bmatrix} 19 \\\\ 11 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Premultiplicación por $A^T$.",
               "es_resultado": False},
              {"accion_md": (
                  "Sistema de ecuaciones normales $\\begin{bmatrix} 17 & 1 \\\\ 1 & 5 \\end{bmatrix}\\hat{\\vec{x}} = \\begin{bmatrix} 19 \\\\ 11 \\end{bmatrix}$.\n\n"
                  "$(A^TA)^{-1} = \\dfrac{1}{84}\\begin{bmatrix} 5 & -1 \\\\ -1 & 17 \\end{bmatrix}$.\n\n"
                  "$\\hat{\\vec{x}} = \\dfrac{1}{84}\\begin{bmatrix} 5 & -1 \\\\ -1 & 17 \\end{bmatrix}\\begin{bmatrix} 19 \\\\ 11 \\end{bmatrix} = \\dfrac{1}{84}\\begin{bmatrix} 84 \\\\ 168 \\end{bmatrix} = \\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Sistema $2 \\times 2$, resolvemos con la inversa $2\\times 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\hat{\\vec{x}} = (1, 2)^T$.** Verificación: $A\\hat{\\vec{x}} = (4, 4, 3)^T \\neq \\vec{b} = (2, 0, 11)^T$ (sistema **inconsistente**), pero es la **mejor aproximación**."
              ),
               "justificacion_md": "Los datos NO se ajustan exactamente, pero $A\\hat{\\vec{x}}$ minimiza la distancia.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Existencia y unicidad de la solución de mínimos cuadrados.** Para $A \\in \\mathbb{R}^{m \\times n}$ y $\\vec{b} \\in \\mathbb{R}^m$:\n\n"
              "**(a)** El conjunto de soluciones de mínimos cuadrados de $A\\vec{x} = \\vec{b}$ siempre es **no vacío** (existe al menos una).\n\n"
              "**(b)** Las siguientes son **equivalentes**:\n\n"
              "- $A\\vec{x} = \\vec{b}$ tiene **solución única** de mínimos cuadrados.\n"
              "- Las columnas de $A$ son **linealmente independientes**.\n"
              "- $A^TA$ es **invertible**.\n\n"
              "**(c)** Si las columnas de $A$ son LI, la solución única es\n\n"
              "$$\\hat{\\vec{x}} = (A^TA)^{-1} A^T \\vec{b}.$$\n\n"
              "**El error de mínimos cuadrados** es $\\|\\vec{b} - A\\hat{\\vec{x}}\\|$ — la distancia entre $\\vec{b}$ y $\\text{Col}\\,A$."
          )),

        b("ejemplo_resuelto",
          titulo="Error de mínimos cuadrados",
          problema_md=(
              "Para el ejemplo anterior, calcula el error $\\|\\vec{b} - A\\hat{\\vec{x}}\\|$."
          ),
          pasos=[
              {"accion_md": (
                  "$A\\hat{\\vec{x}} = \\begin{bmatrix} 4 & 0 \\\\ 0 & 2 \\\\ 1 & 1 \\end{bmatrix}\\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix} = \\begin{bmatrix} 4 \\\\ 4 \\\\ 3 \\end{bmatrix}.$\n\n"
                  "$\\vec{b} - A\\hat{\\vec{x}} = (2-4, 0-4, 11-3)^T = (-2, -4, 8)^T.$"
              ),
               "justificacion_md": "Residuo del ajuste.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\|\\vec{b} - A\\hat{\\vec{x}}\\| = \\sqrt{4 + 16 + 64} = \\sqrt{84} \\approx 9.17.$\n\n"
                  "**Esta es la mínima distancia posible** entre $\\vec{b}$ y los vectores de la forma $A\\vec{x}$."
              ),
               "justificacion_md": "**Lección:** ningún otro $\\vec{x}$ produce un $A\\vec{x}$ más cercano a $\\vec{b}$ que $A\\hat{\\vec{x}}$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Mínimos cuadrados con columnas ortogonales",
          enunciado_md=(
              "Cuando las columnas de $A$ son **ortogonales**, las ecuaciones normales se simplifican drásticamente: $A^TA$ es **diagonal** y la proyección se calcula directamente como\n\n"
              "$$\\hat{\\vec{b}} = \\sum_{j=1}^n \\frac{\\vec{b}\\cdot\\vec{a}_j}{\\vec{a}_j\\cdot\\vec{a}_j} \\vec{a}_j.$$\n\n"
              "Los pesos en esa combinación lineal son **directamente** las componentes de $\\hat{\\vec{x}}$:\n\n"
              "$$\\hat{x}_j = \\frac{\\vec{b}\\cdot\\vec{a}_j}{\\vec{a}_j\\cdot\\vec{a}_j}.$$\n\n"
              "**No se necesita resolver el sistema de ecuaciones normales** — basta calcular productos punto."
          )),

        b("ejemplo_resuelto",
          titulo="Mínimos cuadrados con columnas ortogonales",
          problema_md=(
              "Resuelve $A\\vec{x} = \\vec{b}$ por mínimos cuadrados con $A = \\begin{bmatrix} 1 & -6 \\\\ 1 & -2 \\\\ 1 & 1 \\\\ 1 & 7 \\end{bmatrix}$ y $\\vec{b} = (-1, 2, 1, 6)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "Verificamos ortogonalidad de las columnas $\\vec{a}_1 = (1,1,1,1)^T$ y $\\vec{a}_2 = (-6,-2,1,7)^T$:\n\n"
                  "$\\vec{a}_1\\cdot\\vec{a}_2 = -6 - 2 + 1 + 7 = 0$ ✓ (ortogonales)."
              ),
               "justificacion_md": "Confirmar antes de aplicar la fórmula.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\vec{b}\\cdot\\vec{a}_1 = -1 + 2 + 1 + 6 = 8$. $\\vec{a}_1\\cdot\\vec{a}_1 = 4$. $\\hat{x}_1 = 8/4 = 2$.\n\n"
                  "$\\vec{b}\\cdot\\vec{a}_2 = 6 - 4 + 1 + 42 = 45$. $\\vec{a}_2\\cdot\\vec{a}_2 = 36 + 4 + 1 + 49 = 90$. $\\hat{x}_2 = 45/90 = 1/2$.\n\n"
                  "**$\\hat{\\vec{x}} = (2, 1/2)^T$** — sin resolver ningún sistema."
              ),
               "justificacion_md": "**Patrón:** columnas ortogonales convierten mínimos cuadrados en un cálculo trivial.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Mínimos cuadrados vía factorización QR",
          enunciado_md=(
              "Si $A = QR$ es la factorización QR de $A$ (con columnas LI), entonces la solución única de mínimos cuadrados es\n\n"
              "$$\\boxed{\\hat{\\vec{x}} = R^{-1} Q^T \\vec{b}.}$$\n\n"
              "Equivalentemente, se resuelve el sistema **triangular superior** $R\\hat{\\vec{x}} = Q^T \\vec{b}$ por sustitución hacia atrás.\n\n"
              "**Este método es numéricamente más estable** que las ecuaciones normales — $A^TA$ tiene 'condicionamiento' al cuadrado del de $A$, lo que amplifica los errores numéricos."
          ),
          demostracion_md=(
              "$A^TA\\hat{\\vec{x}} = A^T\\vec{b}$ con $A = QR$:\n\n"
              "$(QR)^T(QR)\\hat{\\vec{x}} = (QR)^T \\vec{b}$ $\\Rightarrow R^T Q^T Q R\\hat{\\vec{x}} = R^T Q^T \\vec{b}$ $\\Rightarrow R^T R \\hat{\\vec{x}} = R^T Q^T \\vec{b}$ (porque $Q^TQ = I$).\n\n"
              "Como $R^T$ es invertible, $R\\hat{\\vec{x}} = Q^T\\vec{b}$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Mínimos cuadrados con QR",
          problema_md=(
              "Resuelve por mínimos cuadrados $A\\vec{x} = \\vec{b}$ con $A = \\begin{bmatrix} 1 & 3 & 5 \\\\ 1 & 1 & 0 \\\\ 1 & 1 & 2 \\\\ 1 & 3 & 3 \\end{bmatrix}$ y $\\vec{b} = (3, 5, 7, -3)^T$, dada la factorización $A = QR$ con $Q = \\dfrac{1}{2}\\begin{bmatrix} 1 & 1 & 1 \\\\ 1 & -1 & -1 \\\\ 1 & -1 & 1 \\\\ 1 & 1 & -1 \\end{bmatrix}$ y $R = \\begin{bmatrix} 2 & 4 & 5 \\\\ 0 & 2 & 3 \\\\ 0 & 0 & 2 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "$Q^T \\vec{b} = \\dfrac{1}{2}\\begin{bmatrix} 1 & 1 & 1 & 1 \\\\ 1 & -1 & -1 & 1 \\\\ 1 & -1 & 1 & -1 \\end{bmatrix}\\begin{bmatrix} 3 \\\\ 5 \\\\ 7 \\\\ -3 \\end{bmatrix} = \\dfrac{1}{2}\\begin{bmatrix} 12 \\\\ -12 \\\\ 8 \\end{bmatrix} = \\begin{bmatrix} 6 \\\\ -6 \\\\ 4 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Multiplicación matriz-vector estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "Resolvemos $R\\hat{\\vec{x}} = Q^T\\vec{b}$ por sustitución hacia atrás:\n\n"
                  "$2\\hat{x}_3 = 4 \\Rightarrow \\hat{x}_3 = 2$.\n\n"
                  "$2\\hat{x}_2 + 3(2) = -6 \\Rightarrow \\hat{x}_2 = -6$.\n\n"
                  "$2\\hat{x}_1 + 4(-6) + 5(2) = 6 \\Rightarrow 2\\hat{x}_1 = 20 \\Rightarrow \\hat{x}_1 = 10$.\n\n"
                  "**$\\hat{\\vec{x}} = (10, -6, 2)^T$.**"
              ),
               "justificacion_md": "**Sistema triangular** — fácil de resolver por sustitución.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\hat{\\vec{x}}$ es solución de mínimos cuadrados de $A\\vec{x} = \\vec{b}$ $\\iff$:",
                  "opciones_md": [
                      "$A\\hat{\\vec{x}} = \\vec{b}$ exactamente",
                      "$A^TA\\hat{\\vec{x}} = A^T\\vec{b}$",
                      "$\\hat{\\vec{x}} = \\vec{0}$",
                      "$\\vec{b} \\in \\text{Nul}\\,A$",
                  ],
                  "correcta": "B",
                  "pista_md": "Ecuaciones normales.",
                  "explicacion_md": "**Ecuaciones normales $A^TA\\hat{\\vec{x}} = A^T\\vec{b}$.** Si $A\\vec{x} = \\vec{b}$ es consistente, las soluciones de mínimos cuadrados coinciden con las soluciones exactas.",
              },
              {
                  "enunciado_md": "La solución de mínimos cuadrados es **única** $\\iff$:",
                  "opciones_md": [
                      "$A$ es cuadrada",
                      "Las columnas de $A$ son linealmente independientes",
                      "$\\vec{b} \\in \\text{Col}\\,A$",
                      "$A^T = A^{-1}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Equivalente a $A^TA$ invertible.",
                  "explicacion_md": "**Columnas LI** $\\iff$ $A^TA$ invertible $\\iff$ solución única $\\hat{\\vec{x}} = (A^TA)^{-1}A^T\\vec{b}$.",
              },
              {
                  "enunciado_md": "Vía QR, $\\hat{\\vec{x}}$ se obtiene resolviendo:",
                  "opciones_md": [
                      "$Q\\hat{\\vec{x}} = R\\vec{b}$",
                      "$R\\hat{\\vec{x}} = Q^T\\vec{b}$",
                      "$Q^TQ\\hat{\\vec{x}} = \\vec{b}$",
                      "$R^T\\hat{\\vec{x}} = Q\\vec{b}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Sistema triangular superior.",
                  "explicacion_md": "**$R\\hat{\\vec{x}} = Q^T\\vec{b}$** — sustitución hacia atrás (R es triangular superior).",
              },
          ]),

        ej(
            "Mínimos cuadrados $2\\times 1$",
            "Halla la solución de mínimos cuadrados de $A\\vec{x} = \\vec{b}$ con $A = \\begin{bmatrix} 2 \\\\ -1 \\\\ 2 \\end{bmatrix}$ y $\\vec{b} = (1, 3, 4)^T$.",
            ["Una sola variable, una columna. $A^TA$ es escalar."],
            (
                "$A^TA = 4 + 1 + 4 = 9$. $A^T\\vec{b} = 2 - 3 + 8 = 7$. $\\hat{x} = 7/9$."
            ),
        ),

        ej(
            "Sistema sobredeterminado",
            "Halla la solución de mínimos cuadrados de $\\begin{cases} x_1 + x_2 = 2 \\\\ -x_1 + x_2 = 1 \\\\ -x_2 = 0 \\end{cases}$.",
            ["Forma $A$, $\\vec{b}$ y aplica ecuaciones normales."],
            (
                "$A = \\begin{bmatrix} 1 & 1 \\\\ -1 & 1 \\\\ 0 & -1 \\end{bmatrix}$, $\\vec{b} = (2, 1, 0)^T$. $A^TA = \\begin{bmatrix} 2 & 0 \\\\ 0 & 3 \\end{bmatrix}$, $A^T\\vec{b} = \\begin{bmatrix} 1 \\\\ 3 \\end{bmatrix}$.\n\n"
                "Sistema diagonal: $\\hat{x}_1 = 1/2$, $\\hat{x}_2 = 1$. **$\\hat{\\vec{x}} = (1/2, 1)^T$.**"
            ),
        ),

        ej(
            "Error y consistencia",
            "Para $A = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\\\ 1 & 1 \\end{bmatrix}$ y $\\vec{b} = (1, 1, 0)^T$, halla $\\hat{\\vec{x}}$ y el error.",
            ["Aplica las ecuaciones normales."],
            (
                "$A^TA = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}$, $A^T\\vec{b} = \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}$.\n\n"
                "$(A^TA)^{-1} = \\dfrac{1}{3}\\begin{bmatrix} 2 & -1 \\\\ -1 & 2 \\end{bmatrix}$. $\\hat{\\vec{x}} = \\dfrac{1}{3}(1, 1)^T$.\n\n"
                "$A\\hat{\\vec{x}} = (1/3, 1/3, 2/3)^T$, $\\vec{b} - A\\hat{\\vec{x}} = (2/3, 2/3, -2/3)^T$.\n\n"
                "Error: $\\sqrt{4/9 + 4/9 + 4/9} = \\sqrt{12}/3 = 2\\sqrt{3}/3$."
            ),
        ),

        fig(
            "Diagrama 2D con ejes x, y. Nube de puntos negros dispersos siguiendo una tendencia lineal aproximada. "
            "Recta de mejor ajuste teal #06b6d4 atravesando la nube. Desde cada punto, una línea vertical "
            "punteada ámbar #f59e0b conecta el punto con la recta, representando los residuos ε_i. Etiqueta "
            "destacada: 'minimiza Σ ε_i^2'. Título: 'Mínimos cuadrados'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que mínimos cuadrados resuelve el sistema $A\\vec{x} = \\vec{b}$ exactamente.** Solo si es **consistente**; si no, da la mejor aproximación.",
              "**Usar $(A^TA)^{-1}A^T\\vec{b}$ con $A^TA$ singular.** Si las columnas de $A$ son LD, $A^TA$ no es invertible — hay infinitas soluciones de mínimos cuadrados.",
              "**Olvidar premultiplicar por $A^T$.** Las ecuaciones normales requieren $A^TA\\vec{x} = A^T\\vec{b}$, no $A\\vec{x} = \\vec{b}$.",
              "**Confundir mínimos cuadrados con regresión lineal estadística.** Mínimos cuadrados es la **herramienta**; regresión es una **aplicación**.",
              "**Usar las ecuaciones normales con datos numéricamente delicados.** Para precisión, preferir QR (más estable).",
          ]),

        b("resumen",
          puntos_md=[
              "**Solución de mínimos cuadrados:** $\\hat{\\vec{x}}$ que minimiza $\\|\\vec{b} - A\\vec{x}\\|$.",
              "**Geométricamente:** $A\\hat{\\vec{x}} = \\text{proy}_{\\text{Col}\\,A}\\,\\vec{b}$.",
              "**Ecuaciones normales:** $A^TA\\hat{\\vec{x}} = A^T\\vec{b}$ — siempre consistente.",
              "**Solución única** $\\iff$ columnas de $A$ LI $\\iff$ $A^TA$ invertible.",
              "**Error de mínimos cuadrados:** $\\|\\vec{b} - A\\hat{\\vec{x}}\\|$ — distancia mínima de $\\vec{b}$ a $\\text{Col}\\,A$.",
              "**Vía QR:** $\\hat{\\vec{x}} = R^{-1}Q^T\\vec{b}$ — más estable numéricamente.",
              "**Caso ortogonal:** $\\hat{x}_j = (\\vec{b}\\cdot\\vec{a}_j)/(\\vec{a}_j\\cdot\\vec{a}_j)$ — sin resolver sistema.",
              "**Próxima lección:** **modelos lineales** — aplicación de mínimos cuadrados a regresión.",
          ]),
    ]
    return {
        "id": "lec-al-7-5-minimos-cuadrados",
        "title": "Mínimos cuadrados",
        "description": "Solución de mínimos cuadrados de $A\\vec{x} = \\vec{b}$, ecuaciones normales $A^TA\\hat{\\vec{x}} = A^T\\vec{b}$, error $\\|\\vec{b} - A\\hat{\\vec{x}}\\|$, solución vía QR.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 5,
    }


# =====================================================================
# 7.6 Modelos lineales
# =====================================================================
def lesson_7_6():
    blocks = [
        b("texto", body_md=(
            "Cerramos el capítulo con la aplicación más cotidiana del álgebra lineal: el **ajuste de modelos lineales** "
            "a datos experimentales. Es la base de la **regresión lineal**, omnipresente en estadística, ciencia de "
            "datos, machine learning, ciencias experimentales e ingeniería.\n\n"
            "**Idea central:** dados puntos de datos $(x_i, y_i)$, queremos encontrar la recta (o plano, o hiperplano) "
            "$y = \\beta_0 + \\beta_1 x$ que **mejor se ajuste** a los datos en el sentido de los mínimos cuadrados.\n\n"
            "Esto se traduce en un sistema sobredeterminado $X\\beta = \\vec{y}$ (típicamente inconsistente) y se resuelve "
            "por las ecuaciones normales $X^T X \\hat{\\beta} = X^T \\vec{y}$.\n\n"
            "Al terminar:\n\n"
            "- Formulas un problema de regresión como sistema $X\\beta = \\vec{y}$.\n"
            "- Construyes la **matriz de diseño** $X$ y el **vector de observaciones** $\\vec{y}$.\n"
            "- Calculas el **vector de parámetros** $\\hat{\\beta}$ vía ecuaciones normales.\n"
            "- Generalizas a regresión múltiple y modelos polinomiales."
        )),

        b("definicion",
          titulo="Modelo lineal",
          body_md=(
              "Un **modelo lineal** describe una variable dependiente $y$ como combinación lineal de variables predictoras (o features) más un término constante:\n\n"
              "$$y = \\beta_0 + \\beta_1 x_1 + \\beta_2 x_2 + \\cdots + \\beta_k x_k.$$\n\n"
              "Los $\\beta_j$ son los **parámetros** (o **coeficientes**) del modelo a determinar.\n\n"
              "**Notación matricial** para $m$ observaciones $\\{(x_{i1}, x_{i2}, \\ldots, x_{ik}, y_i)\\}_{i=1}^m$:\n\n"
              "$$\\boxed{X\\beta = \\vec{y},}$$\n\n"
              "donde:\n\n"
              "- $X \\in \\mathbb{R}^{m \\times (k+1)}$ es la **matriz de diseño** (cada fila es una observación, una columna por predictor más una columna de unos para $\\beta_0$).\n"
              "- $\\beta = (\\beta_0, \\beta_1, \\ldots, \\beta_k)^T \\in \\mathbb{R}^{k+1}$ es el **vector de parámetros**.\n"
              "- $\\vec{y} \\in \\mathbb{R}^m$ es el **vector de observaciones**.\n\n"
              "**El sistema típicamente es sobredeterminado** ($m > k+1$) e **inconsistente** (los datos reales no se ajustan exactamente). Buscamos la **solución de mínimos cuadrados**:\n\n"
              "$$\\hat{\\beta} = \\arg\\min_{\\beta} \\|\\vec{y} - X\\beta\\|.$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Solución del modelo lineal por mínimos cuadrados.** El vector de parámetros $\\hat{\\beta}$ que mejor ajusta el modelo $X\\beta = \\vec{y}$ se obtiene resolviendo las **ecuaciones normales**:\n\n"
              "$$\\boxed{X^T X \\hat{\\beta} = X^T \\vec{y}.}$$\n\n"
              "Si las columnas de $X$ son LI (caso típico cuando los predictores no son redundantes):\n\n"
              "$$\\hat{\\beta} = (X^T X)^{-1} X^T \\vec{y}.$$\n\n"
              "**Interpretación:** $X\\hat{\\beta}$ es la **mejor aproximación** lineal de los datos $\\vec{y}$ por las columnas de $X$."
          )),

        b("ejemplo_resuelto",
          titulo="Recta de regresión por 4 puntos",
          problema_md=(
              "Halla la ecuación $y = \\beta_0 + \\beta_1 x$ de la recta de mínimos cuadrados que mejor ajusta los puntos $(2, 1), (5, 2), (7, 3), (8, 3)$."
          ),
          pasos=[
              {"accion_md": (
                  "**Construir matriz de diseño y vector de observaciones.** Para una recta, $X$ tiene una columna de unos (para $\\beta_0$) y una columna con los $x_i$ (para $\\beta_1$):\n\n"
                  "$X = \\begin{bmatrix} 1 & 2 \\\\ 1 & 5 \\\\ 1 & 7 \\\\ 1 & 8 \\end{bmatrix}, \\quad \\vec{y} = \\begin{bmatrix} 1 \\\\ 2 \\\\ 3 \\\\ 3 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Cada fila representa una observación; columnas representan los términos del modelo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular $X^T X$ y $X^T \\vec{y}$:**\n\n"
                  "$X^T X = \\begin{bmatrix} 1 & 1 & 1 & 1 \\\\ 2 & 5 & 7 & 8 \\end{bmatrix}\\begin{bmatrix} 1 & 2 \\\\ 1 & 5 \\\\ 1 & 7 \\\\ 1 & 8 \\end{bmatrix} = \\begin{bmatrix} 4 & 22 \\\\ 22 & 142 \\end{bmatrix}.$\n\n"
                  "$X^T \\vec{y} = \\begin{bmatrix} 1 + 2 + 3 + 3 \\\\ 2 + 10 + 21 + 24 \\end{bmatrix} = \\begin{bmatrix} 9 \\\\ 57 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Cálculos directos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Resolver $X^T X \\hat{\\beta} = X^T \\vec{y}$:**\n\n"
                  "$\\det(X^T X) = 4 \\cdot 142 - 22^2 = 568 - 484 = 84$.\n\n"
                  "$(X^T X)^{-1} = \\dfrac{1}{84}\\begin{bmatrix} 142 & -22 \\\\ -22 & 4 \\end{bmatrix}$.\n\n"
                  "$\\hat{\\beta} = \\dfrac{1}{84}\\begin{bmatrix} 142 & -22 \\\\ -22 & 4 \\end{bmatrix}\\begin{bmatrix} 9 \\\\ 57 \\end{bmatrix} = \\dfrac{1}{84}\\begin{bmatrix} 24 \\\\ 30 \\end{bmatrix} = \\begin{bmatrix} 2/7 \\\\ 5/14 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Inversa de matriz $2\\times 2$ y multiplicación.",
               "es_resultado": False},
              {"accion_md": (
                  "**Recta de mínimos cuadrados:**\n\n"
                  "$$\\boxed{y = \\dfrac{2}{7} + \\dfrac{5}{14}x.}$$\n\n"
                  "**Verificación:** evaluando en $x = 2$: $y = 2/7 + 10/14 = 4/14 + 10/14 = 1$ — pasa cerca de $(2, 1)$ ✓. En $x = 8$: $y = 2/7 + 40/14 = 4/14 + 40/14 = 44/14 \\approx 3.14$ — cerca de $(8, 3)$ ✓."
              ),
               "justificacion_md": "**La recta no pasa exactamente por los puntos** (es imposible si no son colineales), pero minimiza la suma de cuadrados de las distancias verticales.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué 'mínimos cuadrados'.** El error que se minimiza es\n\n"
            "$\\sum_{i=1}^m (y_i - (\\beta_0 + \\beta_1 x_i))^2$ — la **suma de cuadrados** de las **distancias verticales** entre los puntos y la recta.\n\n"
            "**Por qué cuadrados** (y no valores absolutos): los cuadrados son **diferenciables**, lo que da una solución cerrada vía las ecuaciones normales. La 'regresión robusta' usa otras normas pero requiere métodos iterativos.\n\n"
            "**Importante:** los residuos $r_i = y_i - \\hat{y}_i$ contienen información sobre la **calidad del ajuste**. Si el modelo es correcto, los residuos deberían distribuirse 'aleatoriamente' (sin patrones obvios)."
        )),

        b("definicion",
          titulo="Regresión múltiple y modelos polinomiales",
          body_md=(
              "**Regresión múltiple:** $y = \\beta_0 + \\beta_1 x_1 + \\cdots + \\beta_k x_k$ con varios predictores. La matriz de diseño $X$ tiene $k+1$ columnas (una por predictor más la de unos).\n\n"
              "**Modelo polinomial:** $y = \\beta_0 + \\beta_1 x + \\beta_2 x^2 + \\cdots + \\beta_k x^k$. Aunque la **función** es no lineal en $x$, **el modelo es lineal en los parámetros $\\beta$**, así que se ajusta por las mismas ecuaciones normales. La matriz de diseño tiene columnas $1, x, x^2, \\ldots, x^k$ evaluadas en cada $x_i$.\n\n"
              "**Modelo logarítmico, exponencial, etc.:** muchos modelos no lineales se **linealizan** vía transformaciones (ej. $y = a e^{bx}$ se vuelve $\\ln y = \\ln a + bx$ — lineal en $\\ln a$ y $b$)."
          )),

        b("ejemplo_resuelto",
          titulo="Modelo polinomial cuadrático",
          problema_md=(
              "Ajusta una parábola $y = \\beta_0 + \\beta_1 x + \\beta_2 x^2$ a los puntos $(1, 1), (2, 1), (3, 2)$."
          ),
          pasos=[
              {"accion_md": (
                  "Matriz de diseño con columnas $(1, x, x^2)$:\n\n"
                  "$X = \\begin{bmatrix} 1 & 1 & 1 \\\\ 1 & 2 & 4 \\\\ 1 & 3 & 9 \\end{bmatrix}, \\quad \\vec{y} = (1, 1, 2)^T.$"
              ),
               "justificacion_md": "Cada $x_i$ se eleva a potencias $0, 1, 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "Como tenemos $3$ puntos y $3$ parámetros, $X$ es $3\\times 3$ invertible (cuadrada con det $\\neq 0$). El sistema $X\\beta = \\vec{y}$ es **consistente** y tiene solución única exacta:\n\n"
                  "$\\det X = 2 \\neq 0$, $\\hat{\\beta} = X^{-1}\\vec{y}$.\n\n"
                  "Resolviendo: $\\hat{\\beta} = (1, -\\tfrac{1}{2}, \\tfrac{1}{2})^T$, así $y = 1 - \\tfrac{x}{2} + \\tfrac{x^2}{2}$."
              ),
               "justificacion_md": "**Caso especial:** con tantos parámetros como puntos, la parábola pasa exactamente por los $3$ puntos (interpolación, no regresión).",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación:** $y(1) = 1 - 0.5 + 0.5 = 1$ ✓. $y(2) = 1 - 1 + 2 = 2$... espera, debe ser $1$. Recalculemos.\n\n"
                  "Sistema $\\beta_0 + \\beta_1 + \\beta_2 = 1$, $\\beta_0 + 2\\beta_1 + 4\\beta_2 = 1$, $\\beta_0 + 3\\beta_1 + 9\\beta_2 = 2$. Restando: $\\beta_1 + 3\\beta_2 = 0$ y $\\beta_1 + 5\\beta_2 = 1 \\Rightarrow \\beta_2 = 1/2, \\beta_1 = -3/2, \\beta_0 = 1 - (-3/2) - 1/2 = 2$.\n\n"
                  "$y = 2 - \\tfrac{3x}{2} + \\tfrac{x^2}{2}$. **Verificación:** $y(1) = 2 - 1.5 + 0.5 = 1$ ✓, $y(2) = 2 - 3 + 2 = 1$ ✓, $y(3) = 2 - 4.5 + 4.5 = 2$ ✓."
              ),
               "justificacion_md": "**Lección:** con suficientes parámetros, el ajuste es exacto. Con menos parámetros que puntos, mínimos cuadrados da el mejor ajuste aproximado.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para ajustar una recta $y = \\beta_0 + \\beta_1 x$ a $n$ puntos, la matriz de diseño $X$ tiene tamaño:",
                  "opciones_md": ["$2 \\times n$", "$n \\times 2$", "$n \\times n$", "$2 \\times 2$"],
                  "correcta": "B",
                  "pista_md": "Filas = observaciones, columnas = términos del modelo.",
                  "explicacion_md": "**$n \\times 2$.** Una fila por punto, dos columnas (una de unos para $\\beta_0$, una con los $x_i$ para $\\beta_1$).",
              },
              {
                  "enunciado_md": "Las ecuaciones normales para regresión lineal son:",
                  "opciones_md": [
                      "$X\\beta = \\vec{y}$",
                      "$X^T X \\beta = X^T \\vec{y}$",
                      "$\\beta = X^{-1}\\vec{y}$",
                      "$X X^T \\beta = \\vec{y}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Premultiplicar por $X^T$.",
                  "explicacion_md": "**$X^T X \\beta = X^T \\vec{y}$.** Premultiplicación por $X^T$ da un sistema cuadrado siempre consistente.",
              },
              {
                  "enunciado_md": "Un modelo polinomial $y = \\beta_0 + \\beta_1 x + \\beta_2 x^2$ es:",
                  "opciones_md": [
                      "No es modelo lineal (es cuadrático en $x$)",
                      "Sí es modelo lineal (lineal en los $\\beta$)",
                      "Solo si $\\beta_2 = 0$",
                      "Solo si $x \\geq 0$",
                  ],
                  "correcta": "B",
                  "pista_md": "Linealidad se refiere a los **parámetros** $\\beta$, no a los predictores.",
                  "explicacion_md": "**Es modelo lineal en los $\\beta$.** Por eso se resuelve por las mismas ecuaciones normales — la 'no linealidad' está en cómo se construye $X$ (con potencias de $x$), pero los $\\beta$ aparecen linealmente.",
              },
          ]),

        ej(
            "Recta por 3 puntos",
            "Halla la recta $y = \\beta_0 + \\beta_1 x$ por mínimos cuadrados a los puntos $(0, 1), (1, 1), (2, 4)$.",
            ["Construye $X$ y $\\vec{y}$. Aplica ecuaciones normales."],
            (
                "$X = \\begin{bmatrix} 1 & 0 \\\\ 1 & 1 \\\\ 1 & 2 \\end{bmatrix}$, $\\vec{y} = (1, 1, 4)^T$.\n\n"
                "$X^TX = \\begin{bmatrix} 3 & 3 \\\\ 3 & 5 \\end{bmatrix}$, $X^T\\vec{y} = (6, 9)^T$.\n\n"
                "$\\det = 6$. $(X^TX)^{-1} = \\dfrac{1}{6}\\begin{bmatrix} 5 & -3 \\\\ -3 & 3 \\end{bmatrix}$.\n\n"
                "$\\hat{\\beta} = \\dfrac{1}{6}(30 - 27, -18 + 27)^T = \\dfrac{1}{6}(3, 9)^T = (1/2, 3/2)^T$.\n\n"
                "**Recta:** $y = \\tfrac{1}{2} + \\tfrac{3}{2}x$."
            ),
        ),

        ej(
            "Predicción con modelo ajustado",
            "Para la recta $y = 2/7 + (5/14)x$ del ejemplo, predice el valor de $y$ en $x = 10$.",
            ["Solo evalúa la fórmula."],
            (
                "$y(10) = 2/7 + 50/14 = 4/14 + 50/14 = 54/14 = 27/7 \\approx 3.857$."
            ),
        ),

        ej(
            "Regresión múltiple simple",
            "Ajusta $y = \\beta_0 + \\beta_1 x_1 + \\beta_2 x_2$ a $(1, 0, 2), (0, 1, 1), (1, 1, 3)$ donde $(x_1, x_2, y)$ representa cada observación.",
            ["Filas $(1, x_{i1}, x_{i2})$ en $X$.", "Sistema cuadrado $3\\times 3$ — solución exacta."],
            (
                "$X = \\begin{bmatrix} 1 & 1 & 0 \\\\ 1 & 0 & 1 \\\\ 1 & 1 & 1 \\end{bmatrix}$, $\\vec{y} = (2, 1, 3)^T$.\n\n"
                "Sistema cuadrado consistente. $\\beta_0 + \\beta_1 = 2$, $\\beta_0 + \\beta_2 = 1$, $\\beta_0 + \\beta_1 + \\beta_2 = 3$.\n\n"
                "De la 1ª y 3ª: $\\beta_2 = 1$. De la 2ª: $\\beta_0 = 0$. De la 1ª: $\\beta_1 = 2$.\n\n"
                "**Modelo:** $y = 2x_1 + x_2$."
            ),
        ),

        fig(
            "Tres paneles lado a lado, cada uno con la misma nube de puntos negros sobre ejes x, y. Panel 1: "
            "ajuste lineal y = ax + b en teal #06b6d4, con etiqueta 'Lineal' debajo. Panel 2: ajuste cuadrático "
            "y = ax² + bx + c en ámbar #f59e0b, con etiqueta 'Cuadrático' debajo. Panel 3: ajuste exponencial "
            "linealizado log(y) = ax + b en púrpura, con etiqueta 'Exponencial' debajo. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar la columna de unos en $X$.** Sin ella, la recta forzosamente pasa por el origen.",
              "**Confundir 'lineal en los predictores' con 'lineal en los parámetros'.** Modelos polinomiales son lineales en los $\\beta$ aunque las features sean potencias de $x$.",
              "**Aplicar mínimos cuadrados a un sistema consistente.** Si $X\\beta = \\vec{y}$ es consistente exactamente, las ecuaciones normales dan la solución exacta — no hay aproximación.",
              "**Olvidar verificar la calidad del ajuste.** Un $\\hat{\\beta}$ óptimo no garantiza un buen modelo si los residuos muestran patrones (heterocedasticidad, no linealidad oculta, etc.).",
              "**Sobreajustar (overfitting).** Con tantos parámetros como puntos, el ajuste es perfecto pero el modelo no generaliza — base de problemas en machine learning.",
          ]),

        b("resumen",
          puntos_md=[
              "**Modelo lineal:** $y = \\beta_0 + \\beta_1 x_1 + \\cdots + \\beta_k x_k$ — lineal en los $\\beta$.",
              "**Notación matricial:** $X\\beta = \\vec{y}$ con $X$ matriz de diseño, $\\beta$ parámetros, $\\vec{y}$ observaciones.",
              "**Solución por mínimos cuadrados:** $\\hat{\\beta}$ resuelve $X^TX\\hat{\\beta} = X^T\\vec{y}$.",
              "**Si columnas de $X$ son LI:** $\\hat{\\beta} = (X^TX)^{-1}X^T\\vec{y}$.",
              "**Modelos polinomiales** son casos especiales — columnas de $X$ son potencias de $x$.",
              "**Cierre del capítulo y del curso:** la ortogonalidad y los mínimos cuadrados son la conexión entre el álgebra lineal teórica y las aplicaciones reales.",
              "**Próximo capítulo:** **Matrices simétricas** — diagonalización ortogonal y formas cuadráticas.",
          ]),
    ]
    return {
        "id": "lec-al-7-6-modelos-lineales",
        "title": "Modelos lineales",
        "description": "Regresión lineal por mínimos cuadrados, matriz de diseño $X$, ecuaciones normales $X^TX\\beta = X^T\\vec{y}$, modelos polinomiales y regresión múltiple.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
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

    chapter_id = "ch-al-ortogonalidad"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Ortogonalidad",
        "description": (
            "Producto interno y norma; complemento ortogonal; bases ortogonales y ortonormales; "
            "proyección ortogonal y mejor aproximación; proceso de Gram-Schmidt y factorización QR; "
            "mínimos cuadrados y modelos lineales."
        ),
        "order": 7,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_7_1, lesson_7_2, lesson_7_3, lesson_7_4, lesson_7_5, lesson_7_6]
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
        f"✅ Capítulo 7 — Ortogonalidad listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
