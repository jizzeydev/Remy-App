"""
Seed del curso Álgebra Lineal — Capítulo 1: Espacio.
4 lecciones:
  1.1 Vectores
  1.2 Producto punto
  1.3 Producto cruz
  1.4 Rectas y planos

ENFOQUE ALGEBRAICO (no de cálculo):
- Vectores en R^n general (no solo R^3).
- Notación matricial / columna donde aplica.
- Énfasis en combinaciones lineales, subespacios, conexión con sistemas (preview de cap 2).
- Cauchy-Schwarz, triangular, proyecciones (preview de cap 7 Ortogonalidad).
- Hiperplanos como caso n-dimensional de planos.

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
# 1.1 Vectores
# =====================================================================
def lesson_1_1():
    blocks = [
        b("texto", body_md=(
            "El **álgebra lineal** estudia objetos llamados **vectores** y las operaciones que se hacen con "
            "ellos. A diferencia del cálculo (donde un vector es 'una flecha en el espacio físico 3D'), "
            "aquí trabajaremos con vectores en $\\mathbb{R}^n$ para **cualquier $n$** — incluso "
            "$\\mathbb{R}^4, \\mathbb{R}^{100}$ o más. La intuición geométrica viene de $\\mathbb{R}^2$ y "
            "$\\mathbb{R}^3$, pero la maquinaria algebraica funciona en cualquier dimensión.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir $\\mathbb{R}^n$ y manipular vectores como **n-tuplas** o **matrices columna**.\n"
            "- Operar con **suma**, **producto por escalar** y **combinaciones lineales**.\n"
            "- Calcular **norma**, **vector unitario** y **distancia** en $\\mathbb{R}^n$.\n"
            "- Reconocer el **conjunto generado** ($\\text{span}$) — preview de los subespacios."
        )),

        b("definicion",
          titulo="$\\mathbb{R}^n$ y notación columna",
          body_md=(
              "$\\mathbb{R}^n$ es el conjunto de **n-tuplas** ordenadas de números reales. Sus elementos son "
              "**vectores**, que escribimos como **columnas** (la convención estándar en álgebra lineal):\n\n"
              "$$\\vec{v} = \\begin{bmatrix} v_1 \\\\ v_2 \\\\ \\vdots \\\\ v_n \\end{bmatrix} \\in \\mathbb{R}^n$$\n\n"
              "**Notaciones equivalentes:** $(v_1, v_2, \\ldots, v_n)$, $\\langle v_1, \\ldots, v_n \\rangle$, "
              "o usando la **transpuesta**: $\\vec{v} = (v_1, \\ldots, v_n)^T$.\n\n"
              "**Por qué columna y no fila:** la convención es columna porque facilita la multiplicación de matrices por vectores: $A\\vec{v}$ tiene sentido cuando $\\vec{v}$ es columna. Lo veremos en el cap. 2."
          )),

        b("definicion",
          titulo="Operaciones básicas",
          body_md=(
              "Sean $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$ y $c \\in \\mathbb{R}$ (un **escalar**):\n\n"
              "**Suma componente a componente:**\n\n"
              "$$\\vec{u} + \\vec{v} = \\begin{bmatrix} u_1 + v_1 \\\\ \\vdots \\\\ u_n + v_n \\end{bmatrix}$$\n\n"
              "**Producto por escalar:**\n\n"
              "$$c \\vec{v} = \\begin{bmatrix} c v_1 \\\\ \\vdots \\\\ c v_n \\end{bmatrix}$$\n\n"
              "**Vector cero** $\\vec{0}$: todas las componentes $0$. **Vector opuesto**: $-\\vec{v}$.\n\n"
              "Estas dos operaciones (suma y producto por escalar) son los **axiomas básicos** de un **espacio vectorial** — concepto general que estudiaremos en el cap. 5."
          )),

        formulas(
            titulo="Propiedades de las operaciones",
            body=(
                "Para todo $\\vec{u}, \\vec{v}, \\vec{w} \\in \\mathbb{R}^n$ y $c, d \\in \\mathbb{R}$:\n\n"
                "| Propiedad | Fórmula |\n|---|---|\n"
                "| Conmutativa | $\\vec{u} + \\vec{v} = \\vec{v} + \\vec{u}$ |\n"
                "| Asociativa | $(\\vec{u} + \\vec{v}) + \\vec{w} = \\vec{u} + (\\vec{v} + \\vec{w})$ |\n"
                "| Identidad aditiva | $\\vec{v} + \\vec{0} = \\vec{v}$ |\n"
                "| Inverso aditivo | $\\vec{v} + (-\\vec{v}) = \\vec{0}$ |\n"
                "| Distributiva (escalar) | $c(\\vec{u} + \\vec{v}) = c\\vec{u} + c\\vec{v}$ |\n"
                "| Distributiva (vector) | $(c + d)\\vec{v} = c\\vec{v} + d\\vec{v}$ |\n"
                "| Asociativa (escalares) | $(cd)\\vec{v} = c(d\\vec{v})$ |\n"
                "| Identidad escalar | $1 \\cdot \\vec{v} = \\vec{v}$ |\n\n"
                "**Estas 8 propiedades son los axiomas de un espacio vectorial** (cap. 5)."
            ),
        ),

        b("definicion",
          titulo="Combinación lineal",
          body_md=(
              "Una **combinación lineal** de vectores $\\vec{v}_1, \\ldots, \\vec{v}_k \\in \\mathbb{R}^n$ "
              "con escalares $c_1, \\ldots, c_k \\in \\mathbb{R}$ es:\n\n"
              "$$c_1 \\vec{v}_1 + c_2 \\vec{v}_2 + \\cdots + c_k \\vec{v}_k$$\n\n"
              "Es **el único tipo de operación nueva** que se puede formar combinando suma y producto por escalar.\n\n"
              "**Concepto central:** prácticamente todo en álgebra lineal se reduce a combinaciones lineales — "
              "subespacios (cap. 5), independencia (cap. 2), bases (cap. 5), transformaciones lineales (cap. 2)."
          )),

        b("ejemplo_resuelto",
          titulo="Combinación lineal en $\\mathbb{R}^3$",
          problema_md=(
              "Sean $\\vec{v}_1 = \\begin{bmatrix} 1 \\\\ 0 \\\\ 2 \\end{bmatrix}$, "
              "$\\vec{v}_2 = \\begin{bmatrix} 3 \\\\ -1 \\\\ 0 \\end{bmatrix}$. "
              "Calcular $2\\vec{v}_1 - 3\\vec{v}_2$."
          ),
          pasos=[
              {"accion_md": "$2\\vec{v}_1 = \\begin{bmatrix} 2 \\\\ 0 \\\\ 4 \\end{bmatrix}$. "
                            "$3\\vec{v}_2 = \\begin{bmatrix} 9 \\\\ -3 \\\\ 0 \\end{bmatrix}$.",
               "justificacion_md": "Producto por escalar componente a componente.",
               "es_resultado": False},
              {"accion_md": "$2\\vec{v}_1 - 3\\vec{v}_2 = \\begin{bmatrix} 2 - 9 \\\\ 0 - (-3) \\\\ 4 - 0 \\end{bmatrix} = \\begin{bmatrix} -7 \\\\ 3 \\\\ 4 \\end{bmatrix}$.",
               "justificacion_md": "**Patrón general:** combinaciones lineales se calculan componente a componente.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Conjunto generado (span) — preview",
          body_md=(
              "El **conjunto de TODAS las combinaciones lineales** de un conjunto fijo $\\{\\vec{v}_1, \\ldots, \\vec{v}_k\\}$ se llama el **span** (o **conjunto generado**), denotado $\\text{Span}\\{\\vec{v}_1, \\ldots, \\vec{v}_k\\}$.\n\n"
              "**Geométricamente:**\n\n"
              "- $\\text{Span}\\{\\vec{v}\\}$ con $\\vec{v} \\neq \\vec{0}$: una **recta** por el origen.\n"
              "- $\\text{Span}\\{\\vec{u}, \\vec{v}\\}$ con $\\vec{u}, \\vec{v}$ no paralelos: un **plano** por el origen.\n"
              "- $\\text{Span}\\{\\vec{u}, \\vec{v}, \\vec{w}\\}$ con $\\vec{u}, \\vec{v}, \\vec{w}$ linealmente independientes: todo $\\mathbb{R}^3$.\n\n"
              "**El span es siempre un subespacio** — algo que estudiaremos en detalle en el cap. 5. Por ahora, basta retener: combinar linealmente unos pocos vectores genera 'una región plana' que pasa por el origen."
          )),

        fig(
            "Plano cartesiano R^2 con origen marcado. Dos vectores no colineales saliendo del origen: "
            "v1 (color teal #06b6d4) apuntando a (2, 1) y v2 (color ámbar #f59e0b) apuntando a (-1, 2). "
            "Mostrar también tres combinaciones lineales como flechas más finas y semi-transparentes: "
            "1.5*v1, -0.5*v2, y v1+v2 (con etiqueta). Retícula clara con líneas grises tenues, ejes x e y "
            "con flechas y etiquetas. A la derecha, una recta tenue gris claro pasando por el origen "
            "etiquetada 'Span{v} = recta' con un único vector v sobre ella, ilustrando el caso 1D del span. "
            "Sin perspectiva 3D — solo 2D plano. " + STYLE
        ),

        b("definicion",
          titulo="Norma (magnitud) y vector unitario",
          body_md=(
              "La **norma** (o **magnitud**) de $\\vec{v} \\in \\mathbb{R}^n$ es:\n\n"
              "$$\\|\\vec{v}\\| = \\sqrt{v_1^2 + v_2^2 + \\cdots + v_n^2}$$\n\n"
              "Es la generalización de la distancia pitagórica al espacio $n$-dimensional.\n\n"
              "**Propiedades:**\n\n"
              "- $\\|\\vec{v}\\| \\geq 0$, con igualdad solo si $\\vec{v} = \\vec{0}$.\n"
              "- $\\|c\\vec{v}\\| = |c| \\, \\|\\vec{v}\\|$ (escalar sale como valor absoluto).\n\n"
              "**Vector unitario:** $\\hat{v} = \\dfrac{\\vec{v}}{\\|\\vec{v}\\|}$ — magnitud $1$, misma dirección que $\\vec{v}$.\n\n"
              "**Distancia entre vectores:** $d(\\vec{u}, \\vec{v}) = \\|\\vec{u} - \\vec{v}\\|$. En $\\mathbb{R}^2, \\mathbb{R}^3$ recupera la distancia euclidiana."
          )),

        b("ejemplo_resuelto",
          titulo="Norma en $\\mathbb{R}^4$",
          problema_md=(
              "Calcular $\\|\\vec{v}\\|$ para $\\vec{v} = \\begin{bmatrix} 1 \\\\ 2 \\\\ -2 \\\\ 4 \\end{bmatrix}$ "
              "y construir el vector unitario en su dirección."
          ),
          pasos=[
              {"accion_md": "$\\|\\vec{v}\\| = \\sqrt{1 + 4 + 4 + 16} = \\sqrt{25} = 5$.",
               "justificacion_md": "Aplicación directa. **No importa que sea $\\mathbb{R}^4$** — la fórmula es la misma.",
               "es_resultado": False},
              {"accion_md": "$\\hat{v} = \\dfrac{1}{5}\\vec{v} = \\begin{bmatrix} 1/5 \\\\ 2/5 \\\\ -2/5 \\\\ 4/5 \\end{bmatrix}$.\n\n"
                            "**Verificación:** $\\|\\hat{v}\\|^2 = 1/25 + 4/25 + 4/25 + 16/25 = 25/25 = 1$. ✓",
               "justificacion_md": "Vector unitario por construcción.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Vectores estándar",
          body_md=(
              "Los **vectores estándar** (o **canónicos**) de $\\mathbb{R}^n$ son:\n\n"
              "$$\\vec{e}_1 = \\begin{bmatrix} 1 \\\\ 0 \\\\ \\vdots \\\\ 0 \\end{bmatrix}, \\quad "
              "\\vec{e}_2 = \\begin{bmatrix} 0 \\\\ 1 \\\\ \\vdots \\\\ 0 \\end{bmatrix}, \\quad \\ldots, \\quad "
              "\\vec{e}_n = \\begin{bmatrix} 0 \\\\ 0 \\\\ \\vdots \\\\ 1 \\end{bmatrix}$$\n\n"
              "Es decir, $\\vec{e}_i$ tiene un $1$ en la posición $i$ y ceros en las demás.\n\n"
              "**En $\\mathbb{R}^3$:** $\\vec{e}_1 = \\vec{i}, \\vec{e}_2 = \\vec{j}, \\vec{e}_3 = \\vec{k}$ — la notación de cálculo vectorial.\n\n"
              "**Hecho clave:** todo vector se descompone como $\\vec{v} = v_1 \\vec{e}_1 + \\cdots + v_n \\vec{e}_n$ — combinación lineal **única** de los $\\vec{e}_i$. Por eso se llaman **base estándar** (cap. 5)."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\|\\begin{bmatrix} 3 \\\\ -4 \\end{bmatrix}\\| = ?$",
                  "opciones_md": ["$5$", "$7$", "$1$", "$25$"],
                  "correcta": "A",
                  "pista_md": "$\\sqrt{9 + 16} = ?$",
                  "explicacion_md": (
                      "$\\sqrt{3^2 + (-4)^2} = \\sqrt{25} = 5$. Es el ejemplo clásico del trío 3-4-5."
                  ),
              },
              {
                  "enunciado_md": "Si $\\vec{u} = c_1 \\vec{v}_1 + c_2 \\vec{v}_2$, entonces $\\vec{u}$ es:",
                  "opciones_md": [
                      "Igual a $\\vec{v}_1$",
                      "Una combinación lineal de $\\vec{v}_1, \\vec{v}_2$",
                      "Ortogonal a $\\vec{v}_1$",
                      "El vector cero",
                  ],
                  "correcta": "B",
                  "pista_md": "Es la definición misma de combinación lineal.",
                  "explicacion_md": (
                      "**Combinación lineal:** suma de múltiplos escalares de los $\\vec{v}_i$. **$\\vec{u}$ pertenece al $\\text{Span}\\{\\vec{v}_1, \\vec{v}_2\\}$.**"
                  ),
              },
          ]),

        ej(
            titulo="Combinación lineal con tres vectores",
            enunciado=(
                "Sean $\\vec{v}_1 = (1, 2, 0)^T$, $\\vec{v}_2 = (0, 1, 3)^T$, $\\vec{v}_3 = (-1, 0, 1)^T$. "
                "Calcula $\\vec{u} = 2\\vec{v}_1 + 3\\vec{v}_2 - \\vec{v}_3$."
            ),
            pistas=[
                "Calcula cada producto por escalar primero.",
                "Luego suma componente a componente.",
            ],
            solucion=(
                "$2\\vec{v}_1 = (2, 4, 0)^T$. $3\\vec{v}_2 = (0, 3, 9)^T$. $-\\vec{v}_3 = (1, 0, -1)^T$.\n\n"
                "$\\vec{u} = (2 + 0 + 1, \\; 4 + 3 + 0, \\; 0 + 9 - 1)^T = (3, 7, 8)^T$."
            ),
        ),

        ej(
            titulo="Vector unitario en R^5",
            enunciado=(
                "Halla el vector unitario en la dirección de $\\vec{v} = (1, 1, 1, 1, 1)^T \\in \\mathbb{R}^5$."
            ),
            pistas=[
                "Calcula la norma primero.",
                "$\\|\\vec{v}\\|^2 = 5$.",
            ],
            solucion=(
                "$\\|\\vec{v}\\| = \\sqrt{5}$. **Unitario:** $\\hat{v} = \\dfrac{1}{\\sqrt{5}}(1, 1, 1, 1, 1)^T$.\n\n"
                "**Lección:** el vector 'todo unos' no tiene norma 1 — su norma es $\\sqrt{n}$ en $\\mathbb{R}^n$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir vector con punto.** En álgebra lineal, los vectores son objetos algebraicos en $\\mathbb{R}^n$ — no necesariamente 'flechas' en un espacio físico.",
              "**Olvidar la raíz** en la norma. $\\|\\vec{v}\\|^2 = \\sum v_i^2$, así $\\|\\vec{v}\\| = \\sqrt{\\sum v_i^2}$.",
              "**Pensar que solo importan $\\mathbb{R}^2, \\mathbb{R}^3$.** El álgebra lineal trabaja en **cualquier $n$** — la dimensión solo afecta la cantidad de componentes.",
              "**Usar notación de fila inconsistentemente.** En álgebra lineal, los vectores son **columnas** por convención (importante para multiplicación matricial).",
              "**Confundir $\\text{Span}$ con conjunto $\\{\\vec{v}_1, \\ldots, \\vec{v}_k\\}$.** El $\\text{Span}$ es un conjunto **infinito** — todas las combinaciones posibles.",
          ]),

        b("resumen",
          puntos_md=[
              "**$\\mathbb{R}^n$:** vectores como n-tuplas (columnas).",
              "**Operaciones:** suma y producto por escalar — componente a componente.",
              "**Combinación lineal:** $\\sum c_i \\vec{v}_i$ — la operación central del álgebra lineal.",
              "**Norma:** $\\|\\vec{v}\\| = \\sqrt{\\sum v_i^2}$.",
              "**Vector unitario:** $\\hat{v} = \\vec{v}/\\|\\vec{v}\\|$.",
              "**Vectores estándar:** $\\vec{e}_1, \\ldots, \\vec{e}_n$ — base canónica.",
              "**Span:** todas las combinaciones lineales (preview a subespacios).",
              "**Próxima lección:** producto punto — la operación que mide ángulos y proyecciones.",
          ]),
    ]
    return {
        "id": "lec-al-1-1-vectores",
        "title": "Vectores",
        "description": "$\\mathbb{R}^n$, operaciones, combinaciones lineales, norma, vectores estándar y $\\text{Span}$ como preview de subespacios.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 1.2 Producto punto
# =====================================================================
def lesson_1_2():
    blocks = [
        b("texto", body_md=(
            "El **producto punto** (o **producto interno**) es la primera operación que **mezcla dos vectores** "
            "para producir un escalar. Es la base para definir **norma**, **ángulos**, **ortogonalidad** y "
            "**proyecciones** — herramientas que reaparecerán en todo el curso (especialmente en cap. 7 sobre "
            "Ortogonalidad y Mínimos Cuadrados).\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y calcular $\\vec{u} \\cdot \\vec{v}$ en $\\mathbb{R}^n$.\n"
            "- Manejar la **notación matricial** $\\vec{u} \\cdot \\vec{v} = \\vec{u}^T \\vec{v}$.\n"
            "- Aplicar la **desigualdad de Cauchy-Schwarz** y la **desigualdad triangular**.\n"
            "- Calcular **ángulos**, **ortogonalidad** y **proyecciones**."
        )),

        b("definicion",
          titulo="Producto punto",
          body_md=(
              "Para $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$:\n\n"
              "$$\\vec{u} \\cdot \\vec{v} = u_1 v_1 + u_2 v_2 + \\cdots + u_n v_n = \\sum_{i=1}^{n} u_i v_i$$\n\n"
              "**Resultado: un escalar** (no un vector).\n\n"
              "**Notación matricial:** si $\\vec{u}, \\vec{v}$ son vectores columna,\n\n"
              "$$\\vec{u} \\cdot \\vec{v} = \\vec{u}^T \\vec{v}$$\n\n"
              "donde $\\vec{u}^T$ es el vector fila (transpuesta de columna). El producto matricial $\\vec{u}^T \\vec{v}$ es una matriz $1 \\times 1$ — un escalar.\n\n"
              "**Esta notación es central** en álgebra lineal y nos permitirá hacer manipulaciones matriciales más adelante."
          )),

        formulas(
            titulo="Propiedades del producto punto",
            body=(
                "Para todo $\\vec{u}, \\vec{v}, \\vec{w} \\in \\mathbb{R}^n$ y $c \\in \\mathbb{R}$:\n\n"
                "| Propiedad | Fórmula |\n|---|---|\n"
                "| **Conmutativa** (simetría) | $\\vec{u} \\cdot \\vec{v} = \\vec{v} \\cdot \\vec{u}$ |\n"
                "| **Distributiva** | $\\vec{u} \\cdot (\\vec{v} + \\vec{w}) = \\vec{u}\\cdot\\vec{v} + \\vec{u}\\cdot\\vec{w}$ |\n"
                "| **Asociativa con escalar** | $(c\\vec{u}) \\cdot \\vec{v} = c(\\vec{u}\\cdot\\vec{v})$ |\n"
                "| **Definida positiva** | $\\vec{v} \\cdot \\vec{v} \\geq 0$, con igualdad solo si $\\vec{v} = \\vec{0}$ |\n"
                "| **Conexión con norma** | $\\|\\vec{v}\\|^2 = \\vec{v} \\cdot \\vec{v}$ |\n\n"
                "**Las primeras cuatro propiedades** caracterizan a un **producto interno** (concepto general en cap. 5/7). El producto punto en $\\mathbb{R}^n$ es **el** producto interno estándar."
            ),
        ),

        b("teorema",
          nombre="Desigualdad de Cauchy-Schwarz",
          enunciado_md=(
              "Para todo $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$:\n\n"
              "$$|\\vec{u} \\cdot \\vec{v}| \\leq \\|\\vec{u}\\| \\, \\|\\vec{v}\\|$$\n\n"
              "**Igualdad** se alcanza si y solo si $\\vec{u}$ y $\\vec{v}$ son **paralelos** (uno es múltiplo escalar del otro).\n\n"
              "**Es la desigualdad más importante del álgebra lineal** — aparece constantemente."
          ),
          demostracion_md=(
              "Para todo $t \\in \\mathbb{R}$, $\\|\\vec{u} - t\\vec{v}\\|^2 \\geq 0$. Expandiendo:\n\n"
              "$\\|\\vec{u}\\|^2 - 2t (\\vec{u}\\cdot\\vec{v}) + t^2 \\|\\vec{v}\\|^2 \\geq 0$\n\n"
              "Es un polinomio cuadrático en $t$ siempre $\\geq 0$. Su **discriminante** debe ser $\\leq 0$:\n\n"
              "$4(\\vec{u}\\cdot\\vec{v})^2 - 4\\|\\vec{u}\\|^2 \\|\\vec{v}\\|^2 \\leq 0$\n\n"
              "$\\implies (\\vec{u}\\cdot\\vec{v})^2 \\leq \\|\\vec{u}\\|^2 \\|\\vec{v}\\|^2$.\n\n"
              "Tomando raíz: $|\\vec{u}\\cdot\\vec{v}| \\leq \\|\\vec{u}\\| \\|\\vec{v}\\|$. ∎"
          )),

        b("teorema",
          nombre="Desigualdad triangular",
          enunciado_md=(
              "Para todo $\\vec{u}, \\vec{v} \\in \\mathbb{R}^n$:\n\n"
              "$$\\|\\vec{u} + \\vec{v}\\| \\leq \\|\\vec{u}\\| + \\|\\vec{v}\\|$$\n\n"
              "**Geométricamente:** la longitud de un lado de un triángulo es a lo sumo la suma de los otros dos."
          ),
          demostracion_md=(
              "$\\|\\vec{u}+\\vec{v}\\|^2 = \\|\\vec{u}\\|^2 + 2\\vec{u}\\cdot\\vec{v} + \\|\\vec{v}\\|^2 \\leq \\|\\vec{u}\\|^2 + 2\\|\\vec{u}\\|\\|\\vec{v}\\| + \\|\\vec{v}\\|^2 = (\\|\\vec{u}\\| + \\|\\vec{v}\\|)^2$\n\n"
              "(usamos Cauchy-Schwarz en el medio). Tomando raíz: $\\|\\vec{u}+\\vec{v}\\| \\leq \\|\\vec{u}\\| + \\|\\vec{v}\\|$. ∎"
          )),

        b("definicion",
          titulo="Ángulo entre vectores",
          body_md=(
              "Por Cauchy-Schwarz, $\\dfrac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{u}\\| \\|\\vec{v}\\|} \\in [-1, 1]$. Definimos el **ángulo** $\\theta$ entre $\\vec{u}$ y $\\vec{v}$ (vectores no nulos) por:\n\n"
              "$$\\cos\\theta = \\dfrac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{u}\\| \\, \\|\\vec{v}\\|}, \\quad \\theta \\in [0, \\pi]$$\n\n"
              "**En $\\mathbb{R}^2, \\mathbb{R}^3$:** coincide con el ángulo geométrico clásico.\n\n"
              "**En $\\mathbb{R}^n$ general** ($n \\geq 4$): no hay 'ángulo geométrico' obvio, pero la fórmula sigue valiendo y define un concepto útil.\n\n"
              "**Signo del producto punto** $\\leftrightarrow$ **tipo de ángulo:**\n\n"
              "- $\\vec{u}\\cdot\\vec{v} > 0 \\iff$ ángulo agudo.\n"
              "- $\\vec{u}\\cdot\\vec{v} = 0 \\iff$ ortogonal.\n"
              "- $\\vec{u}\\cdot\\vec{v} < 0 \\iff$ ángulo obtuso."
          )),

        b("definicion",
          titulo="Ortogonalidad",
          body_md=(
              "$\\vec{u}, \\vec{v}$ son **ortogonales** (denotado $\\vec{u} \\perp \\vec{v}$) si:\n\n"
              "$$\\vec{u} \\cdot \\vec{v} = 0$$\n\n"
              "**Por convención:** $\\vec{0}$ es ortogonal a todo vector.\n\n"
              "**Conjuntos ortogonales:** $\\{\\vec{v}_1, \\ldots, \\vec{v}_k\\}$ es ortogonal si $\\vec{v}_i \\cdot \\vec{v}_j = 0$ para todo $i \\neq j$.\n\n"
              "**Conjuntos ortonormales:** ortogonal **y** todos unitarios. Los vectores estándar $\\vec{e}_1, \\ldots, \\vec{e}_n$ forman el conjunto ortonormal más simple."
          )),

        b("teorema",
          nombre="Teorema de Pitágoras",
          enunciado_md=(
              "Si $\\vec{u} \\perp \\vec{v}$ entonces:\n\n"
              "$$\\|\\vec{u} + \\vec{v}\\|^2 = \\|\\vec{u}\\|^2 + \\|\\vec{v}\\|^2$$\n\n"
              "**Es la generalización a $\\mathbb{R}^n$** del teorema de Pitágoras de la geometría euclidiana."
          ),
          demostracion_md=(
              "$\\|\\vec{u}+\\vec{v}\\|^2 = (\\vec{u}+\\vec{v}) \\cdot (\\vec{u}+\\vec{v}) = \\|\\vec{u}\\|^2 + 2\\vec{u}\\cdot\\vec{v} + \\|\\vec{v}\\|^2$.\n\n"
              "Si $\\vec{u} \\perp \\vec{v}$, $\\vec{u} \\cdot \\vec{v} = 0$ y queda $\\|\\vec{u}\\|^2 + \\|\\vec{v}\\|^2$. ∎"
          )),

        b("definicion",
          titulo="Proyección ortogonal",
          body_md=(
              "La **proyección ortogonal** de $\\vec{u}$ sobre $\\vec{v}$ (no nulo) es el vector:\n\n"
              "$$\\text{proy}_{\\vec{v}} \\vec{u} = \\dfrac{\\vec{u} \\cdot \\vec{v}}{\\vec{v} \\cdot \\vec{v}} \\, \\vec{v} = \\dfrac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{v}\\|^2} \\, \\vec{v}$$\n\n"
              "**Geométricamente:** la 'sombra' de $\\vec{u}$ sobre la recta generada por $\\vec{v}$.\n\n"
              "**Propiedad clave (ortogonalidad de la diferencia):**\n\n"
              "$$(\\vec{u} - \\text{proy}_{\\vec{v}} \\vec{u}) \\perp \\vec{v}$$\n\n"
              "Es decir, descomponer $\\vec{u} = \\text{proy}_{\\vec{v}} \\vec{u} + (\\vec{u} - \\text{proy}_{\\vec{v}} \\vec{u})$ separa $\\vec{u}$ en una **parte paralela a $\\vec{v}$** y una **parte ortogonal a $\\vec{v}$**.\n\n"
              "**Importancia:** este es el **bloque básico** del proceso de Gram-Schmidt (cap. 7) y de mínimos cuadrados."
          )),

        fig(
            "Proyección ortogonal de un vector. Plano 2D con origen. Dos vectores: u (en color teal) "
            "saliendo del origen hacia arriba-derecha, y v (en color azul) saliendo del origen hacia "
            "la derecha. Trazar una línea perpendicular punteada (en gris) desde la punta de u que "
            "cae sobre la línea de v, formando un triángulo rectángulo. El segmento sobre v desde "
            "el origen al pie de la perpendicular = proyección de u sobre v, en color ámbar grueso, "
            "etiquetado 'proy_v u'. La perpendicular misma etiquetada 'u - proy_v u' (componente "
            "ortogonal). Etiquetas claras: 'u', 'v', 'proy_v u', 'u - proy_v u (ortogonal a v)'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Calcular proyección y verificar ortogonalidad",
          problema_md=(
              "Sean $\\vec{u} = (3, 4, 0)^T$ y $\\vec{v} = (1, 0, 0)^T$. Calcular $\\text{proy}_{\\vec{v}} \\vec{u}$ y "
              "verificar que $\\vec{u} - \\text{proy}_{\\vec{v}}\\vec{u}$ es ortogonal a $\\vec{v}$."
          ),
          pasos=[
              {"accion_md": "**Producto punto:** $\\vec{u} \\cdot \\vec{v} = 3$. **Norma cuadrada:** $\\|\\vec{v}\\|^2 = 1$.\n\n"
                            "**Proyección:** $\\text{proy}_{\\vec{v}}\\vec{u} = \\dfrac{3}{1}(1, 0, 0)^T = (3, 0, 0)^T$.",
               "justificacion_md": "Aplicación de la fórmula.",
               "es_resultado": False},
              {"accion_md": "**Componente ortogonal:** $\\vec{u} - \\text{proy}_{\\vec{v}}\\vec{u} = (3, 4, 0)^T - (3, 0, 0)^T = (0, 4, 0)^T$.\n\n"
                            "**Verificación:** $(0, 4, 0) \\cdot (1, 0, 0) = 0$. ✓ **Ortogonal a $\\vec{v}$.**",
               "justificacion_md": "**Lección general:** descomponer $(3, 4, 0)$ en su parte 'a lo largo del eje $x$' (la proyección) y su parte 'perpendicular' (lo demás). Es una descomposición única.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\vec{u} \\cdot \\vec{v} = \\vec{u}^T \\vec{v}$ es un:",
                  "opciones_md": [
                      "Vector",
                      "Escalar",
                      "Matriz",
                      "Conjunto",
                  ],
                  "correcta": "B",
                  "pista_md": "Producto fila × columna ($1 \\times n$ por $n \\times 1$) da un $1 \\times 1$.",
                  "explicacion_md": (
                      "**Escalar.** El producto matricial $\\vec{u}^T \\vec{v}$ es una matriz $1 \\times 1$, identificada con un número."
                  ),
              },
              {
                  "enunciado_md": "Si $\\|\\vec{u}\\| = 3, \\|\\vec{v}\\| = 4$, ¿qué valores son **posibles** para $\\vec{u} \\cdot \\vec{v}$?",
                  "opciones_md": [
                      "Cualquier número real",
                      "Solo entre $-12$ y $12$",
                      "Solo positivos",
                      "Solo $0$",
                  ],
                  "correcta": "B",
                  "pista_md": "Cauchy-Schwarz: $|\\vec{u}\\cdot\\vec{v}| \\leq \\|\\vec{u}\\|\\|\\vec{v}\\|$.",
                  "explicacion_md": (
                      "Cauchy-Schwarz: $|\\vec{u}\\cdot\\vec{v}| \\leq 3 \\cdot 4 = 12$. **Rango: $[-12, 12]$.** Los extremos se alcanzan si los vectores son paralelos."
                  ),
              },
          ]),

        ej(
            titulo="Ángulo entre vectores en R^4",
            enunciado=(
                "Calcula el ángulo entre $\\vec{u} = (1, 0, 1, 0)^T$ y $\\vec{v} = (1, 1, 1, 1)^T$."
            ),
            pistas=[
                "$\\vec{u} \\cdot \\vec{v} = ?$",
                "$\\|\\vec{u}\\| = \\sqrt{2}$, $\\|\\vec{v}\\| = 2$.",
            ],
            solucion=(
                "$\\vec{u} \\cdot \\vec{v} = 1 + 0 + 1 + 0 = 2$.\n\n"
                "$\\cos\\theta = \\dfrac{2}{\\sqrt{2} \\cdot 2} = \\dfrac{1}{\\sqrt{2}}$.\n\n"
                "$\\theta = \\pi/4 = 45°$. **Ángulo en $\\mathbb{R}^4$** — sin geometría 'visual', pero matemáticamente bien definido."
            ),
        ),

        ej(
            titulo="Proyección y descomposición",
            enunciado=(
                "Descompón $\\vec{u} = (5, 1, 2)^T$ en una parte paralela a $\\vec{v} = (1, 1, 0)^T$ y una parte ortogonal a $\\vec{v}$."
            ),
            pistas=[
                "Proyección: $\\dfrac{\\vec{u}\\cdot\\vec{v}}{\\|\\vec{v}\\|^2}\\vec{v}$.",
                "$\\vec{u}\\cdot\\vec{v} = 6$, $\\|\\vec{v}\\|^2 = 2$.",
            ],
            solucion=(
                "**Proyección:** $\\text{proy}_{\\vec{v}}\\vec{u} = \\dfrac{6}{2}(1, 1, 0)^T = (3, 3, 0)^T$.\n\n"
                "**Componente ortogonal:** $\\vec{u} - \\text{proy}_{\\vec{v}}\\vec{u} = (2, -2, 2)^T$.\n\n"
                "**Verificación:** $(2, -2, 2) \\cdot (1, 1, 0) = 2 - 2 + 0 = 0$. ✓ Ortogonal."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\vec{u} \\cdot \\vec{v}$ (escalar) con $\\vec{u} \\vec{v}^T$ (matriz $n \\times n$).** El primero es producto interno; el segundo es **producto exterior** (matriz de rango 1).",
              "**Aplicar Cauchy-Schwarz al revés.** $|\\vec{u}\\cdot\\vec{v}| \\leq \\|\\vec{u}\\|\\|\\vec{v}\\|$, NO $\\geq$.",
              "**Olvidar elevar al cuadrado** en la fórmula de proyección. $\\dfrac{\\vec{u}\\cdot\\vec{v}}{\\|\\vec{v}\\|^2}\\vec{v}$ — atención al cuadrado.",
              "**Confundir $\\vec{u}\\cdot\\vec{v} > 0$ con 'misma dirección'.** Solo implica ángulo agudo, no que sean paralelos.",
              "**Pensar que la fórmula del ángulo solo vale en $\\mathbb{R}^3$.** Es válida en $\\mathbb{R}^n$ — define el ángulo abstracto entre vectores en cualquier dimensión.",
          ]),

        b("resumen",
          puntos_md=[
              "**Producto punto:** $\\vec{u} \\cdot \\vec{v} = \\sum u_i v_i = \\vec{u}^T \\vec{v}$ — escalar.",
              "**Cauchy-Schwarz:** $|\\vec{u}\\cdot\\vec{v}| \\leq \\|\\vec{u}\\|\\|\\vec{v}\\|$.",
              "**Triangular:** $\\|\\vec{u}+\\vec{v}\\| \\leq \\|\\vec{u}\\| + \\|\\vec{v}\\|$.",
              "**Ángulo:** $\\cos\\theta = (\\vec{u}\\cdot\\vec{v})/(\\|\\vec{u}\\|\\|\\vec{v}\\|)$, válido en $\\mathbb{R}^n$.",
              "**Ortogonalidad:** $\\vec{u}\\cdot\\vec{v} = 0$.",
              "**Pitágoras:** si $\\vec{u} \\perp \\vec{v}$, $\\|\\vec{u}+\\vec{v}\\|^2 = \\|\\vec{u}\\|^2 + \\|\\vec{v}\\|^2$.",
              "**Proyección:** $\\text{proy}_{\\vec{v}}\\vec{u} = \\dfrac{\\vec{u}\\cdot\\vec{v}}{\\|\\vec{v}\\|^2}\\vec{v}$ — bloque básico de Gram-Schmidt y mínimos cuadrados.",
              "**Próxima lección:** producto cruz — operación exclusiva de $\\mathbb{R}^3$ con conexión a determinantes.",
          ]),
    ]
    return {
        "id": "lec-al-1-2-producto-punto",
        "title": "Producto punto",
        "description": "Producto interno en $\\mathbb{R}^n$, Cauchy-Schwarz, ortogonalidad y proyección ortogonal.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 1.3 Producto cruz
# =====================================================================
def lesson_1_3():
    blocks = [
        b("texto", body_md=(
            "El **producto cruz** $\\vec{u} \\times \\vec{v}$ es una operación **exclusiva de $\\mathbb{R}^3$** "
            "que toma dos vectores y devuelve un **vector** ortogonal a ambos. A diferencia del producto "
            "punto (que generaliza a cualquier $\\mathbb{R}^n$), el producto cruz **no existe en $\\mathbb{R}^n$ "
            "para $n \\neq 3$ con las mismas propiedades** — es un fenómeno particular de la dimensión 3.\n\n"
            "Desde una mirada algebraica, el producto cruz es nuestro primer encuentro con el "
            "**determinante**, concepto central que estudiaremos a fondo en el cap 4. La fórmula del "
            "producto cruz es literalmente un determinante $3 \\times 3$.\n\n"
            "**Objetivos de la lección:**\n\n"
            "- Definir $\\vec{u} \\times \\vec{v}$ vía determinante simbólico.\n"
            "- Demostrar las propiedades algebraicas (anticonmutatividad, bilinealidad).\n"
            "- Establecer las propiedades geométricas (ortogonalidad, área, regla de la mano derecha).\n"
            "- Producto **triple escalar** $\\vec{u} \\cdot (\\vec{v} \\times \\vec{w})$ como volumen y como determinante."
        )),

        b("definicion",
          titulo="Producto cruz en $\\mathbb{R}^3$",
          body_md=(
              "Sean $\\vec{u} = (u_1, u_2, u_3)^T$ y $\\vec{v} = (v_1, v_2, v_3)^T$ en $\\mathbb{R}^3$. "
              "El **producto cruz** se define como:\n\n"
              "$$\\vec{u} \\times \\vec{v} = \\begin{vmatrix} \\vec{e}_1 & \\vec{e}_2 & \\vec{e}_3 \\\\ "
              "u_1 & u_2 & u_3 \\\\ v_1 & v_2 & v_3 \\end{vmatrix} = "
              "\\begin{bmatrix} u_2 v_3 - u_3 v_2 \\\\ u_3 v_1 - u_1 v_3 \\\\ u_1 v_2 - u_2 v_1 \\end{bmatrix}$$\n\n"
              "Este 'determinante' es **simbólico** — la primera fila contiene **vectores** $\\vec{e}_1, "
              "\\vec{e}_2, \\vec{e}_3$, no escalares. Pero la regla de expansión por cofactores funciona y "
              "produce el vector resultante.\n\n"
              "**Componente por componente** (mnemotecnia: ciclo $1 \\to 2 \\to 3 \\to 1$):\n\n"
              "$$(\\vec{u} \\times \\vec{v})_i = u_{i+1} v_{i+2} - u_{i+2} v_{i+1} \\pmod{3}$$\n\n"
              "**Vista preliminar:** un determinante $3\\times 3$ con entradas escalares es exactamente "
              "$\\vec{u} \\cdot (\\vec{v} \\times \\vec{w})$ — el **producto triple escalar**, que veremos al final."
          )),

        b("intuicion", body_md=(
            "**¿Por qué solo en $\\mathbb{R}^3$?** El producto cruz tiene una propiedad muy fuerte: produce un "
            "vector **ortogonal** a dos dados. En $\\mathbb{R}^3$, dado un plano (que contiene a $\\vec{u}$ y "
            "$\\vec{v}$), hay exactamente **una recta** ortogonal a él, y por tanto una dirección bien "
            "definida (con su signo). En $\\mathbb{R}^4$, el complemento ortogonal de un plano es **otro "
            "plano** (2-dimensional), no una recta — no hay una elección única. Por eso el producto cruz "
            "**no se generaliza directamente** a dimensiones distintas de 3 (existe una construcción análoga "
            "en $\\mathbb{R}^7$ usando octoniones, fuera del alcance del curso).\n\n"
            "**Lectura algebraica:** la operación $(\\vec{u}, \\vec{v}) \\mapsto \\vec{u} \\times \\vec{v}$ es una "
            "función **bilineal antisimétrica** $\\mathbb{R}^3 \\times \\mathbb{R}^3 \\to \\mathbb{R}^3$. Es un "
            "objeto único de la dimensión 3."
        )),

        b("ejemplo_resuelto",
          titulo="Cálculo directo",
          problema_md=(
              "Calcular $\\vec{u} \\times \\vec{v}$ con $\\vec{u} = (1, 2, 3)^T$ y $\\vec{v} = (4, 5, 6)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "Planteamos el determinante simbólico:\n\n"
                  "$$\\vec{u} \\times \\vec{v} = \\begin{vmatrix} \\vec{e}_1 & \\vec{e}_2 & \\vec{e}_3 \\\\ 1 & 2 & 3 \\\\ 4 & 5 & 6 \\end{vmatrix}.$$"
               ),
               "justificacion_md": "Definición del producto cruz como expansión por la primera fila.",
               "es_resultado": False},
              {"accion_md": (
                  "Calculamos componente a componente:\n\n"
                  "- **Componente 1:** $(2)(6) - (3)(5) = 12 - 15 = -3$.\n"
                  "- **Componente 2:** $-[(1)(6) - (3)(4)] = -(6 - 12) = 6$.\n"
                  "- **Componente 3:** $(1)(5) - (2)(4) = 5 - 8 = -3$."
               ),
               "justificacion_md": "Cuidado con el **signo negativo** de la componente 2 (alterna $+, -, +$ en la expansión).",
               "es_resultado": False},
              {"accion_md": (
                  "$\\vec{u} \\times \\vec{v} = (-3, 6, -3)^T$.\n\n"
                  "**Verificación de ortogonalidad:**\n\n"
                  "$\\vec{u} \\cdot (\\vec{u} \\times \\vec{v}) = (1)(-3) + (2)(6) + (3)(-3) = -3 + 12 - 9 = 0$ ✓\n\n"
                  "$\\vec{v} \\cdot (\\vec{u} \\times \\vec{v}) = (4)(-3) + (5)(6) + (6)(-3) = -12 + 30 - 18 = 0$ ✓"
               ),
               "justificacion_md": "El producto cruz **siempre** es ortogonal a sus dos factores — verificarlo es la mejor forma de pillar errores aritméticos.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Propiedades algebraicas del producto cruz.** Para todo $\\vec{u}, \\vec{v}, \\vec{w} \\in "
              "\\mathbb{R}^3$ y $c \\in \\mathbb{R}$:\n\n"
              "1. **Anticonmutativo:** $\\vec{u} \\times \\vec{v} = -(\\vec{v} \\times \\vec{u})$.\n"
              "2. **Bilineal:** $(c\\vec{u}) \\times \\vec{v} = c(\\vec{u} \\times \\vec{v}) = \\vec{u} \\times (c\\vec{v})$.\n"
              "3. **Distributivo:** $\\vec{u} \\times (\\vec{v} + \\vec{w}) = \\vec{u} \\times \\vec{v} + \\vec{u} \\times \\vec{w}$.\n"
              "4. $\\vec{u} \\times \\vec{u} = \\vec{0}$ (consecuencia de 1).\n"
              "5. $\\vec{u} \\times \\vec{0} = \\vec{0}$.\n"
              "6. **NO es asociativo:** en general $\\vec{u} \\times (\\vec{v} \\times \\vec{w}) \\neq (\\vec{u} \\times \\vec{v}) \\times \\vec{w}$."
          )),

        b("intuicion", body_md=(
            "**Cuidado con la no asociatividad.** El producto cruz **no se comporta como una multiplicación "
            "ordinaria**. La regla correcta para el doble producto es la identidad **BAC-CAB**:\n\n"
            "$$\\vec{u} \\times (\\vec{v} \\times \\vec{w}) = \\vec{v}(\\vec{u} \\cdot \\vec{w}) - \\vec{w}(\\vec{u} \\cdot \\vec{v})$$\n\n"
            "Esto subraya que el producto cruz **no define una estructura de álgebra asociativa** sobre "
            "$\\mathbb{R}^3$. Junto con propiedad 1 y 3, define lo que se llama un **álgebra de Lie**."
        )),

        b("teorema",
          enunciado_md=(
              "**Propiedades geométricas del producto cruz.**\n\n"
              "1. **Ortogonalidad:** $\\vec{u} \\times \\vec{v}$ es ortogonal tanto a $\\vec{u}$ como a $\\vec{v}$.\n"
              "2. **Magnitud:** $\\|\\vec{u} \\times \\vec{v}\\| = \\|\\vec{u}\\| \\|\\vec{v}\\| \\sin\\theta$, donde $\\theta \\in [0, \\pi]$ es el ángulo entre $\\vec{u}$ y $\\vec{v}$.\n"
              "3. **Área:** $\\|\\vec{u} \\times \\vec{v}\\|$ es el **área del paralelogramo** generado por $\\vec{u}$ y $\\vec{v}$.\n"
              "4. **Colinealidad:** $\\vec{u} \\times \\vec{v} = \\vec{0} \\iff \\vec{u}, \\vec{v}$ son **linealmente dependientes** (paralelos).\n"
              "5. **Orientación (regla de la mano derecha):** $(\\vec{u}, \\vec{v}, \\vec{u} \\times \\vec{v})$ forman una base **derecha** de $\\mathbb{R}^3$."
          )),

        fig(
            "Paralelogramo en R^3 generado por dos vectores u (rojo) y v (azul) saliendo desde el origen. "
            "Sombreado teal #06b6d4 para el área. Vector u×v perpendicular saliendo del plano del paralelogramo "
            "(color ámbar #f59e0b), apuntando hacia arriba según regla de la mano derecha. Etiqueta '||u×v|| = área' "
            "junto al paralelogramo. Sistema de coordenadas (x, y, z) en esquina inferior derecha. "
            "Estilo: diagrama matemático limpio, fondo blanco, líneas claras, perspectiva 3D suave. "
            + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Identidad de Lagrange.** Para todo $\\vec{u}, \\vec{v} \\in \\mathbb{R}^3$:\n\n"
              "$$\\|\\vec{u} \\times \\vec{v}\\|^2 + (\\vec{u} \\cdot \\vec{v})^2 = \\|\\vec{u}\\|^2 \\|\\vec{v}\\|^2$$\n\n"
              "**Lectura:** suma de cuadrados — la información del par $(\\vec{u}, \\vec{v})$ se reparte entre "
              "su componente paralela (medida por el producto punto) y su componente perpendicular (medida "
              "por el producto cruz).\n\n"
              "**Equivalente:** $\\sin^2\\theta + \\cos^2\\theta = 1$ multiplicado por $\\|\\vec{u}\\|^2 \\|\\vec{v}\\|^2$."
          )),

        b("ejemplo_resuelto",
          titulo="Área de un triángulo en $\\mathbb{R}^3$",
          problema_md=(
              "Encontrar el área del triángulo con vértices $A = (1, 0, 1)$, $B = (2, 1, 0)$, $C = (0, 1, 2)$."
          ),
          pasos=[
              {"accion_md": (
                  "Construimos dos lados del triángulo como vectores con origen en $A$:\n\n"
                  "$\\vec{AB} = B - A = (1, 1, -1)^T, \\qquad \\vec{AC} = C - A = (-1, 1, 1)^T.$"
               ),
               "justificacion_md": "Cualquier par de lados que compartan vértice generan el paralelogramo asociado.",
               "es_resultado": False},
              {"accion_md": (
                  "Producto cruz:\n\n"
                  "$$\\vec{AB} \\times \\vec{AC} = \\begin{bmatrix} (1)(1) - (-1)(1) \\\\ (-1)(-1) - (1)(1) \\\\ (1)(1) - (1)(-1) \\end{bmatrix} = \\begin{bmatrix} 2 \\\\ 0 \\\\ 2 \\end{bmatrix}.$$"
               ),
               "justificacion_md": "$\\|\\vec{AB} \\times \\vec{AC}\\|$ es el área del paralelogramo generado por los dos vectores.",
               "es_resultado": False},
              {"accion_md": (
                  "Magnitud: $\\|\\vec{AB} \\times \\vec{AC}\\| = \\sqrt{4 + 0 + 4} = 2\\sqrt{2}$.\n\n"
                  "**Área del triángulo** $= \\tfrac{1}{2}\\|\\vec{AB} \\times \\vec{AC}\\| = \\sqrt{2}$."
               ),
               "justificacion_md": "El triángulo es **la mitad** del paralelogramo (lo divide su diagonal $\\vec{BC}$).",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Producto triple escalar",
          body_md=(
              "Dados $\\vec{u}, \\vec{v}, \\vec{w} \\in \\mathbb{R}^3$, el **producto triple escalar** es:\n\n"
              "$$[\\vec{u}, \\vec{v}, \\vec{w}] := \\vec{u} \\cdot (\\vec{v} \\times \\vec{w})$$\n\n"
              "Es un **escalar** (no un vector). Tiene una expresión muy elegante como **determinante**:\n\n"
              "$$\\vec{u} \\cdot (\\vec{v} \\times \\vec{w}) = \\begin{vmatrix} u_1 & u_2 & u_3 \\\\ "
              "v_1 & v_2 & v_3 \\\\ w_1 & w_2 & w_3 \\end{vmatrix}$$\n\n"
              "**Propiedades:**\n\n"
              "1. **Volumen:** $|[\\vec{u}, \\vec{v}, \\vec{w}]|$ es el **volumen del paralelepípedo** generado por los tres vectores.\n"
              "2. **Coplanaridad:** $[\\vec{u}, \\vec{v}, \\vec{w}] = 0 \\iff \\vec{u}, \\vec{v}, \\vec{w}$ son **linealmente dependientes**.\n"
              "3. **Cíclico:** $\\vec{u}\\cdot(\\vec{v}\\times\\vec{w}) = \\vec{v}\\cdot(\\vec{w}\\times\\vec{u}) = \\vec{w}\\cdot(\\vec{u}\\times\\vec{v})$.\n"
              "4. **Antisimétrico:** intercambiar dos vectores cambia el signo (igual que el determinante).\n\n"
              "**Conexión con cap 4:** este es el **determinante** $3\\times 3$ aplicado a la matriz cuyas filas son "
              "$\\vec{u}, \\vec{v}, \\vec{w}$. El determinante mide el **factor de expansión de volumen** de una "
              "transformación lineal — concepto que generalizaremos a $\\mathbb{R}^n$."
          )),

        b("ejemplo_resuelto",
          titulo="Volumen de un paralelepípedo",
          problema_md=(
              "Calcular el volumen del paralelepípedo con aristas $\\vec{u} = (1, 0, 2)^T$, "
              "$\\vec{v} = (3, 1, 0)^T$, $\\vec{w} = (0, 2, 1)^T$."
          ),
          pasos=[
              {"accion_md": (
                  "El volumen es $|\\det M|$ con $M$ la matriz cuyas filas son los tres vectores:\n\n"
                  "$$\\det M = \\begin{vmatrix} 1 & 0 & 2 \\\\ 3 & 1 & 0 \\\\ 0 & 2 & 1 \\end{vmatrix}.$$"
               ),
               "justificacion_md": "Es el producto triple escalar $\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})$.",
               "es_resultado": False},
              {"accion_md": (
                  "Expandimos por la primera fila:\n\n"
                  "$\\det M = 1 \\cdot (1\\cdot 1 - 0\\cdot 2) - 0 + 2 \\cdot (3\\cdot 2 - 1\\cdot 0) = 1 + 12 = 13.$"
               ),
               "justificacion_md": "El término del medio se anula porque $u_2 = 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Volumen** $= |13| = 13$ unidades cúbicas.\n\n"
                  "Como $\\det M \\neq 0$, los tres vectores son **linealmente independientes** (forman una base de $\\mathbb{R}^3$)."
               ),
               "justificacion_md": "**Conexión con cap. 4 y 5:** $\\det \\neq 0 \\iff$ vectores LI $\\iff$ paralelepípedo de volumen positivo.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**El producto cruz es nuestro primer determinante.** Mira atentamente la fórmula:\n\n"
            "$$\\vec{u} \\times \\vec{v} = \\begin{vmatrix} \\vec{e}_1 & \\vec{e}_2 & \\vec{e}_3 \\\\ "
            "u_1 & u_2 & u_3 \\\\ v_1 & v_2 & v_3 \\end{vmatrix}, \\qquad "
            "\\vec{u} \\cdot (\\vec{v} \\times \\vec{w}) = \\begin{vmatrix} u_1 & u_2 & u_3 \\\\ "
            "v_1 & v_2 & v_3 \\\\ w_1 & w_2 & w_3 \\end{vmatrix}$$\n\n"
            "Los determinantes son la **forma algebraica** de medir orientación, área y volumen. En el cap 4 "
            "vamos a definirlos rigurosamente y descubriremos que son los **únicos** funcionales que cumplen "
            "tres propiedades: multilinealidad, antisimetría y normalización. Este será el primer paso para "
            "entender **invertibilidad de matrices, autovalores y orientación**."
        )),

        ej(
            "Producto cruz y verificación",
            "Sea $\\vec{u} = (2, -1, 3)^T$ y $\\vec{v} = (1, 0, -2)^T$. (a) Calcula $\\vec{u} \\times \\vec{v}$. "
            "(b) Verifica que el resultado es ortogonal a $\\vec{u}$ y a $\\vec{v}$. (c) Calcula "
            "$\\|\\vec{u} \\times \\vec{v}\\|$ y úsala para hallar $\\sin\\theta$ entre $\\vec{u}$ y $\\vec{v}$.",
            [
                "Aplica la fórmula del determinante simbólico fila por fila.",
                "Para verificar ortogonalidad, calcula $\\vec{u} \\cdot (\\vec{u} \\times \\vec{v})$ y $\\vec{v} \\cdot (\\vec{u} \\times \\vec{v})$.",
                "$\\sin\\theta = \\|\\vec{u} \\times \\vec{v}\\| / (\\|\\vec{u}\\|\\|\\vec{v}\\|)$.",
            ],
            (
                "**(a)** $\\vec{u} \\times \\vec{v} = ((-1)(-2) - (3)(0), (3)(1) - (2)(-2), (2)(0) - (-1)(1))^T = (2, 7, 1)^T$.\n\n"
                "**(b)** $\\vec{u} \\cdot (2, 7, 1)^T = 4 - 7 + 3 = 0$ ✓. $\\vec{v} \\cdot (2, 7, 1)^T = 2 + 0 - 2 = 0$ ✓.\n\n"
                "**(c)** $\\|\\vec{u} \\times \\vec{v}\\| = \\sqrt{4 + 49 + 1} = \\sqrt{54} = 3\\sqrt{6}$. "
                "$\\|\\vec{u}\\| = \\sqrt{14}$, $\\|\\vec{v}\\| = \\sqrt{5}$. Por tanto "
                "$\\sin\\theta = 3\\sqrt{6}/\\sqrt{70} = 3\\sqrt{6}/\\sqrt{70} = 3\\sqrt{60/700} \\approx 0.879$, "
                "luego $\\theta \\approx 1.072$ rad ($\\approx 61.4°$)."
            ),
        ),

        ej(
            "Coplanaridad",
            "Determina si los vectores $\\vec{u} = (1, 2, -1)^T$, $\\vec{v} = (2, 1, 1)^T$, "
            "$\\vec{w} = (4, 5, -1)^T$ son coplanares (linealmente dependientes).",
            [
                "Calcula el producto triple escalar $[\\vec{u}, \\vec{v}, \\vec{w}]$ como determinante $3\\times 3$.",
                "Si vale 0, son coplanares; en caso contrario, no.",
                "Usa expansión por cofactores en la primera fila.",
            ],
            (
                "$\\det \\begin{pmatrix} 1 & 2 & -1 \\\\ 2 & 1 & 1 \\\\ 4 & 5 & -1 \\end{pmatrix} = "
                "1(1 \\cdot (-1) - 1 \\cdot 5) - 2(2 \\cdot (-1) - 1 \\cdot 4) + (-1)(2 \\cdot 5 - 1 \\cdot 4)$\n\n"
                "$= 1(-6) - 2(-6) + (-1)(6) = -6 + 12 - 6 = 0$.\n\n"
                "**Sí son coplanares.** En efecto, $\\vec{w} = 2\\vec{u} + \\vec{v}$ — verifica componente a "
                "componente: $(2(1) + 2, 2(2) + 1, 2(-1) + 1) = (4, 5, -1)$ ✓."
            ),
        ),

        b("verificacion",
          intro_md="Antes del cierre, verifica que dominas las propiedades clave:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\vec{u} \\times \\vec{v} = \\vec{0}$ con $\\vec{u}, \\vec{v} \\neq \\vec{0}$, entonces:",
                  "opciones_md": [
                      "$\\vec{u}$ y $\\vec{v}$ son ortogonales",
                      "$\\vec{u}$ y $\\vec{v}$ son linealmente dependientes (paralelos)",
                      "$\\vec{u} = \\vec{v}$",
                      "Es imposible: el producto cruz nunca es cero",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\|\\vec{u} \\times \\vec{v}\\| = \\|\\vec{u}\\|\\|\\vec{v}\\|\\sin\\theta$. ¿Cuándo es cero?",
                  "explicacion_md": (
                      "Como $\\|\\vec{u}\\|, \\|\\vec{v}\\| > 0$, la única forma de que $\\|\\vec{u}\\times\\vec{v}\\| = 0$ "
                      "es $\\sin\\theta = 0$, es decir $\\theta = 0$ o $\\theta = \\pi$ — los vectores son **paralelos**."
                  ),
              },
              {
                  "enunciado_md": "$\\vec{u} \\times \\vec{v}$ es:",
                  "opciones_md": [
                      "Un escalar",
                      "Un vector ortogonal a $\\vec{u}$ y a $\\vec{v}$",
                      "Un vector paralelo a $\\vec{u}$",
                      "Un vector que está en el plano de $\\vec{u}$ y $\\vec{v}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Por construcción, ¿qué relación tiene con los dos factores?",
                  "explicacion_md": (
                      "El producto cruz produce un vector **ortogonal** tanto a $\\vec{u}$ como a $\\vec{v}$ "
                      "(propiedad fundamental). El producto **punto** sí es un escalar — no confundir."
                  ),
              },
              {
                  "enunciado_md": "Si $[\\vec{u}, \\vec{v}, \\vec{w}] = \\vec{u}\\cdot(\\vec{v}\\times\\vec{w}) = 0$, entonces los tres vectores:",
                  "opciones_md": [
                      "Son ortogonales entre sí",
                      "Son coplanares (linealmente dependientes)",
                      "Forman una base de $\\mathbb{R}^3$",
                      "Son todos iguales",
                  ],
                  "correcta": "B",
                  "pista_md": "El producto triple escalar mide el **volumen** del paralelepípedo.",
                  "explicacion_md": (
                      "Volumen cero significa que el paralelepípedo está aplastado: los tres vectores caben en "
                      "un mismo plano por el origen — son **linealmente dependientes**. Es el test estándar de coplanaridad."
                  ),
              },
          ]),

        b("errores_comunes",
          items_md=[
              "**Pensar que el producto cruz existe en $\\mathbb{R}^n$ general.** Solo en $\\mathbb{R}^3$ (con esta fórmula). En $\\mathbb{R}^2$ se usa una versión 'pseudo-escalar' $u_1 v_2 - u_2 v_1$, pero no es un vector.",
              "**Confundir orden:** $\\vec{u} \\times \\vec{v} \\neq \\vec{v} \\times \\vec{u}$. Difieren en signo (anticonmutativo).",
              "**Asociar el producto cruz:** NO es asociativo. $(\\vec{u} \\times \\vec{v}) \\times \\vec{w} \\neq \\vec{u} \\times (\\vec{v} \\times \\vec{w})$.",
              "**Olvidar el signo del cofactor central** al expandir el determinante simbólico (la componente $\\vec{e}_2$ tiene signo negativo).",
              "**Mezclar producto punto y cruz:** $\\vec{u} \\cdot \\vec{v}$ es escalar; $\\vec{u} \\times \\vec{v}$ es vector. No tiene sentido sumar uno al otro.",
          ]),

        b("resumen",
          puntos_md=[
              "**Producto cruz** $\\vec{u} \\times \\vec{v}$: solo en $\\mathbb{R}^3$, definido por determinante simbólico.",
              "**Anticonmutativo** y **bilineal**, **NO** asociativo.",
              "**Ortogonal** a $\\vec{u}$ y $\\vec{v}$; magnitud $= \\|\\vec{u}\\|\\|\\vec{v}\\|\\sin\\theta$ = área del paralelogramo.",
              "**Colinealidad:** $\\vec{u} \\times \\vec{v} = \\vec{0} \\iff \\vec{u}, \\vec{v}$ linealmente dependientes.",
              "**Producto triple escalar** $\\vec{u} \\cdot (\\vec{v} \\times \\vec{w})$ = determinante = volumen con signo.",
              "**Coplanaridad** $\\iff [\\vec{u}, \\vec{v}, \\vec{w}] = 0$.",
              "**Próxima lección:** rectas y planos — geometría afín en $\\mathbb{R}^n$ y conexión con sistemas lineales.",
          ]),
    ]
    return {
        "id": "lec-al-1-3-producto-cruz",
        "title": "Producto cruz",
        "description": "Producto cruz en $\\mathbb{R}^3$, identidad de Lagrange, producto triple escalar y conexión con determinantes.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# 1.4 Rectas y planos
# =====================================================================
def lesson_1_4():
    blocks = [
        b("texto", body_md=(
            "Esta lección cierra el capítulo aplicando todo lo anterior — vectores, producto punto, "
            "producto cruz — al estudio de **rectas, planos e hiperplanos**. La perspectiva algebraica "
            "es lo central: una recta o un plano son **conjuntos solución** de ciertas ecuaciones, lo que "
            "abre la puerta al cap 2 (sistemas lineales).\n\n"
            "**Dos descripciones complementarias:**\n\n"
            "- **Paramétrica** ($\\vec{r} = \\vec{p} + t\\vec{v}$): describe los puntos como **combinación lineal** desde un punto base. Útil cuando se conocen direcciones generadoras.\n"
            "- **Implícita** ($\\vec{n} \\cdot \\vec{r} = d$ o sistemas $A\\vec{r} = \\vec{b}$): describe los puntos como soluciones de **ecuaciones lineales**. Útil para verificar pertenencia y calcular intersecciones.\n\n"
            "**Objetivos:**\n\n"
            "- Escribir rectas y planos en forma paramétrica e implícita y pasar de una a otra.\n"
            "- Definir **hiperplanos** en $\\mathbb{R}^n$ general.\n"
            "- Calcular distancias punto-recta y punto-plano usando proyección ortogonal.\n"
            "- Reconocer rectas y planos como subconjuntos solución de sistemas — preview del cap 2."
        )),

        b("definicion",
          titulo="Recta paramétrica en $\\mathbb{R}^n$",
          body_md=(
              "Sean $\\vec{p} \\in \\mathbb{R}^n$ un punto y $\\vec{v} \\in \\mathbb{R}^n \\setminus \\{\\vec{0}\\}$ un vector "
              "**director**. La **recta** que pasa por $\\vec{p}$ con dirección $\\vec{v}$ es:\n\n"
              "$$L = \\{\\vec{p} + t\\vec{v} : t \\in \\mathbb{R}\\}$$\n\n"
              "**Forma vectorial paramétrica:**\n\n"
              "$$\\vec{r}(t) = \\vec{p} + t\\vec{v}$$\n\n"
              "**Forma escalar (componente a componente)** en $\\mathbb{R}^3$:\n\n"
              "$$x = p_1 + tv_1, \\quad y = p_2 + tv_2, \\quad z = p_3 + tv_3$$\n\n"
              "**Forma simétrica** (cuando todas las $v_i \\neq 0$, eliminando el parámetro):\n\n"
              "$$\\frac{x - p_1}{v_1} = \\frac{y - p_2}{v_2} = \\frac{z - p_3}{v_3}$$\n\n"
              "**Lectura algebraica:** la recta $L$ es la **traslación** del subespacio "
              "$\\text{span}(\\vec{v}) = \\{t\\vec{v} : t \\in \\mathbb{R}\\}$ por el vector $\\vec{p}$. Los "
              "subespacios pasan por el origen; las rectas afines no lo necesitan."
          )),

        b("intuicion", body_md=(
            "**Dos rectas son iguales** aunque sus parametrizaciones difieran. Por ejemplo, si "
            "$\\vec{p}' = \\vec{p} + s_0 \\vec{v}$ (otro punto sobre la misma recta) y $\\vec{v}' = c\\vec{v}$ con "
            "$c \\neq 0$ (mismo director, posiblemente reescalado), entonces $\\vec{p} + t\\vec{v}$ y "
            "$\\vec{p}' + t\\vec{v}'$ describen el mismo conjunto de puntos.\n\n"
            "Lo que importa es:\n\n"
            "- **Dirección** (una clase de equivalencia: $\\vec{v} \\sim c\\vec{v}$).\n"
            "- **Un punto cualquiera** sobre la recta.\n\n"
            "Esta no-unicidad es similar a cómo los **subespacios** se describen por bases distintas."
        )),

        b("definicion",
          titulo="Plano: forma punto-normal",
          body_md=(
              "Un **plano** en $\\mathbb{R}^3$ está determinado por un punto $\\vec{p}_0$ y un vector "
              "**normal** $\\vec{n} \\neq \\vec{0}$ (perpendicular al plano). Un punto $\\vec{r}$ está en el "
              "plano si y solo si $\\vec{r} - \\vec{p}_0$ es ortogonal a $\\vec{n}$:\n\n"
              "$$\\vec{n} \\cdot (\\vec{r} - \\vec{p}_0) = 0$$\n\n"
              "Desarrollando con $\\vec{n} = (a, b, c)^T$, $\\vec{r} = (x, y, z)^T$ y $d = \\vec{n} \\cdot \\vec{p}_0$:\n\n"
              "$$ax + by + cz = d$$\n\n"
              "Esa es la **ecuación general** del plano. Los coeficientes del lado izquierdo son **exactamente** "
              "las componentes del vector normal.\n\n"
              "**Forma paramétrica del plano** (con dos directores $\\vec{u}, \\vec{v}$ no paralelos):\n\n"
              "$$\\vec{r}(s, t) = \\vec{p}_0 + s\\vec{u} + t\\vec{v}, \\quad (s, t) \\in \\mathbb{R}^2$$\n\n"
              "Cualquier $\\vec{n}$ ortogonal a $\\vec{u}$ y $\\vec{v}$ sirve como normal — por ejemplo "
              "$\\vec{n} = \\vec{u} \\times \\vec{v}$ (de aquí la utilidad del producto cruz)."
          )),

        b("ejemplo_resuelto",
          titulo="Plano por tres puntos",
          problema_md=(
              "Encontrar la ecuación del plano que pasa por $A = (1, 0, 0)$, $B = (0, 2, 0)$, $C = (0, 0, 3)$."
          ),
          pasos=[
              {"accion_md": (
                  "Construimos dos vectores que viven en el plano (con origen en $A$):\n\n"
                  "$\\vec{AB} = B - A = (-1, 2, 0)^T, \\qquad \\vec{AC} = C - A = (-1, 0, 3)^T.$"
               ),
               "justificacion_md": "Cualquier par de vectores no paralelos del plano sirve para determinarlo.",
               "es_resultado": False},
              {"accion_md": (
                  "Vector normal vía producto cruz:\n\n"
                  "$\\vec{n} = \\vec{AB} \\times \\vec{AC} = ((2)(3) - (0)(0),\\ (0)(-1) - (-1)(3),\\ (-1)(0) - (2)(-1))^T = (6, 3, 2)^T.$"
               ),
               "justificacion_md": "$\\vec{u} \\times \\vec{v}$ es ortogonal a ambos $\\Rightarrow$ es normal al plano que contiene a $\\vec{u}, \\vec{v}$.",
               "es_resultado": False},
              {"accion_md": (
                  "Usamos el punto $A$ para hallar $d$: $d = \\vec{n} \\cdot A = 6(1) + 3(0) + 2(0) = 6$.\n\n"
                  "**Ecuación del plano:** $\\boxed{6x + 3y + 2z = 6}$.\n\n"
                  "**Verificación:** $B = (0,2,0) \\Rightarrow 0 + 6 + 0 = 6$ ✓. $C = (0,0,3) \\Rightarrow 0 + 0 + 6 = 6$ ✓."
               ),
               "justificacion_md": "Forma punto–normal: $\\vec{n}\\cdot(\\vec{r} - A) = 0 \\iff \\vec{n}\\cdot\\vec{r} = \\vec{n}\\cdot A$.",
               "es_resultado": True},
          ]),

        fig(
            "Diagrama 3D en perspectiva isométrica suave. Sistema de coordenadas (x, y, z) con flechas. "
            "Un plano semitransparente teal #06b6d4 inclinado, etiquetado 'Plano: n·r = d'. "
            "Sobre el plano, dos vectores no paralelos u y v en color gris oscuro saliendo de un punto base "
            "p0 (marcado con un punto negro etiquetado), ilustrando la forma paramétrica r = p0 + s·u + t·v. "
            "Saliendo de p0 perpendicular al plano, un vector normal n en ámbar #f59e0b con la etiqueta 'n = u × v'. "
            "También una recta L atravesando el plano: una flecha morada con vector director v_L y punto de "
            "intersección destacado. Cuadrícula tenue para dar sensación de profundidad. Sin sombras dramáticas. "
            + STYLE
        ),

        b("definicion",
          titulo="Hiperplano en $\\mathbb{R}^n$",
          body_md=(
              "Un **hiperplano** en $\\mathbb{R}^n$ es el análogo natural de 'recta en $\\mathbb{R}^2$' o 'plano "
              "en $\\mathbb{R}^3$': un subconjunto $(n-1)$-dimensional definido por **una sola ecuación lineal**:\n\n"
              "$$H = \\{\\vec{r} \\in \\mathbb{R}^n : \\vec{n} \\cdot \\vec{r} = d\\} = \\{\\vec{r} : a_1 r_1 + \\cdots + a_n r_n = d\\}$$\n\n"
              "donde $\\vec{n} = (a_1, \\ldots, a_n)^T \\neq \\vec{0}$ es el vector **normal** al hiperplano y "
              "$d \\in \\mathbb{R}$.\n\n"
              "**Casos particulares:**\n\n"
              "- $n = 2$: hiperplano = **recta** ($ax + by = d$).\n"
              "- $n = 3$: hiperplano = **plano** ($ax + by + cz = d$).\n"
              "- $n = 4$: hiperplano = volumen 3D dentro de $\\mathbb{R}^4$.\n\n"
              "**Conexión con sistemas lineales (preview cap 2):** una ecuación lineal en $n$ incógnitas "
              "**es** la ecuación de un hiperplano. Un sistema de $m$ ecuaciones es la **intersección** de $m$ "
              "hiperplanos. Resolverlo equivale a hallar esa intersección."
          )),

        b("intuicion", body_md=(
            "**Dimensión del conjunto solución.** Pensemos geométricamente:\n\n"
            "- Una ecuación lineal en $\\mathbb{R}^n$: define un hiperplano de dimensión $n-1$.\n"
            "- Dos ecuaciones independientes: la intersección típicamente baja a $n-2$ (un 'plano' de $\\mathbb{R}^4$, una recta en $\\mathbb{R}^3$).\n"
            "- $k$ ecuaciones independientes: dimensión $n - k$.\n\n"
            "Por ejemplo, en $\\mathbb{R}^3$ una **recta** se puede dar como **intersección de dos planos** — es decir, como solución del sistema:\n\n"
            "$$\\begin{cases} a_1 x + b_1 y + c_1 z = d_1 \\\\ a_2 x + b_2 y + c_2 z = d_2 \\end{cases}$$\n\n"
            "donde los normales $(a_1, b_1, c_1)$ y $(a_2, b_2, c_2)$ no son paralelos. Esta es la "
            "**descripción implícita** de una recta — complemento de la paramétrica $\\vec{p} + t\\vec{v}$.\n\n"
            "Esa dualidad **paramétrico ↔ implícito** es uno de los temas profundos del álgebra lineal "
            "(núcleo vs imagen, rango vs nulidad)."
        )),

        b("ejemplo_resuelto",
          titulo="De forma implícita a paramétrica",
          problema_md=(
              "Hallar la ecuación paramétrica de la recta dada como intersección de los planos "
              "$x + y + z = 1$ y $2x - y + z = 0$."
          ),
          pasos=[
              {"accion_md": (
                  "El **vector director** $\\vec{v}$ de la recta debe ser ortogonal a ambos normales $\\vec{n}_1 = (1, 1, 1)^T$ y $\\vec{n}_2 = (2, -1, 1)^T$. Tomamos:\n\n"
                  "$\\vec{v} = \\vec{n}_1 \\times \\vec{n}_2 = ((1)(1) - (1)(-1),\\ (1)(2) - (1)(1),\\ (1)(-1) - (1)(2))^T = (2, 1, -3)^T.$"
               ),
               "justificacion_md": "La recta vive en ambos planos, así que va en la dirección común a los dos — perpendicular a ambos normales.",
               "es_resultado": False},
              {"accion_md": (
                  "Necesitamos **un punto** de la recta. Fijamos $z = 0$ y resolvemos $\\begin{cases} x + y = 1 \\\\ 2x - y = 0 \\end{cases}$: sumando, $3x = 1$, así $x = 1/3$, $y = 2/3$.\n\n"
                  "Punto base: $\\vec{p} = (1/3,\\ 2/3,\\ 0)^T$."
               ),
               "justificacion_md": "Cualquier valor de una variable libre sirve para encontrar un punto particular.",
               "es_resultado": False},
              {"accion_md": (
                  "**Forma paramétrica:**\n\n"
                  "$$\\vec{r}(t) = \\begin{bmatrix} 1/3 \\\\ 2/3 \\\\ 0 \\end{bmatrix} + t \\begin{bmatrix} 2 \\\\ 1 \\\\ -3 \\end{bmatrix}, \\quad t \\in \\mathbb{R}.$$\n\n"
                  "**Verificación:** $\\vec{n}_1 \\cdot \\vec{v} = 2 + 1 - 3 = 0$ ✓ y $\\vec{n}_2 \\cdot \\vec{v} = 4 - 1 - 3 = 0$ ✓."
               ),
               "justificacion_md": "Construcción punto + dirección — el formato estándar de una recta en $\\mathbb{R}^n$.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Distancia de un punto a un hiperplano.** Sea $H : \\vec{n} \\cdot \\vec{r} = d$ un hiperplano "
              "en $\\mathbb{R}^n$ y $\\vec{q} \\in \\mathbb{R}^n$ un punto. Entonces:\n\n"
              "$$\\text{dist}(\\vec{q}, H) = \\frac{|\\vec{n} \\cdot \\vec{q} - d|}{\\|\\vec{n}\\|}$$\n\n"
              "**Demostración (vía proyección ortogonal):** sea $\\vec{p}_0 \\in H$ cualquiera (entonces "
              "$\\vec{n} \\cdot \\vec{p}_0 = d$). El vector $\\vec{q} - \\vec{p}_0$ apunta de $H$ a $\\vec{q}$. "
              "La distancia es la **componente normal**:\n\n"
              "$$\\text{dist}(\\vec{q}, H) = \\left| \\frac{\\vec{n} \\cdot (\\vec{q} - \\vec{p}_0)}{\\|\\vec{n}\\|} \\right| = \\frac{|\\vec{n}\\cdot\\vec{q} - \\vec{n}\\cdot\\vec{p}_0|}{\\|\\vec{n}\\|} = \\frac{|\\vec{n}\\cdot\\vec{q} - d|}{\\|\\vec{n}\\|}. \\qquad \\blacksquare$$"
          )),

        b("teorema",
          enunciado_md=(
              "**Distancia de un punto a una recta** (en $\\mathbb{R}^n$ general). Sea $L : \\vec{r} = \\vec{p} + t\\vec{v}$ "
              "una recta y $\\vec{q}$ un punto. Entonces:\n\n"
              "$$\\text{dist}(\\vec{q}, L) = \\| (\\vec{q} - \\vec{p}) - \\text{proy}_{\\vec{v}}(\\vec{q} - \\vec{p}) \\|$$\n\n"
              "que es la **componente ortogonal** de $\\vec{q} - \\vec{p}$ respecto al director.\n\n"
              "**En $\\mathbb{R}^3$**, una fórmula equivalente más rápida usa el producto cruz:\n\n"
              "$$\\text{dist}(\\vec{q}, L) = \\frac{\\|(\\vec{q} - \\vec{p}) \\times \\vec{v}\\|}{\\|\\vec{v}\\|}$$\n\n"
              "(área del paralelogramo dividido por la base $\\|\\vec{v}\\|$ = altura)."
          )),

        b("ejemplo_resuelto",
          titulo="Distancia punto-plano",
          problema_md=(
              "Calcular la distancia del punto $\\vec{q} = (1, 2, 3)$ al plano $2x - y + 2z = 5$."
          ),
          pasos=[
              {"accion_md": (
                  "Identificamos $\\vec{n} = (2, -1, 2)^T$ y $d = 5$. Calculamos $\\|\\vec{n}\\| = \\sqrt{4 + 1 + 4} = 3$."
               ),
               "justificacion_md": "El plano $ax + by + cz = d$ tiene normal $(a, b, c)^T$.",
               "es_resultado": False},
              {"accion_md": (
                  "Numerador: $|\\vec{n}\\cdot\\vec{q} - d| = |2(1) + (-1)(2) + 2(3) - 5| = |2 - 2 + 6 - 5| = 1$."
               ),
               "justificacion_md": "El **valor absoluto** asegura distancia $\\geq 0$ independientemente de qué lado del plano esté $\\vec{q}$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\text{dist}(\\vec{q}, H) = \\dfrac{|\\vec{n}\\cdot\\vec{q} - d|}{\\|\\vec{n}\\|} = \\dfrac{1}{3}$ unidades."
               ),
               "justificacion_md": "Aplicación directa de la fórmula de distancia punto-hiperplano.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Distancia punto-recta en $\\mathbb{R}^3$",
          problema_md=(
              "Hallar la distancia del punto $\\vec{q} = (3, 1, 2)$ a la recta "
              "$\\vec{r}(t) = (1, 0, 0) + t(0, 1, 1)$."
          ),
          pasos=[
              {"accion_md": (
                  "Identificamos $\\vec{p} = (1, 0, 0)^T$ y dirección $\\vec{v} = (0, 1, 1)^T$. Calculamos $\\vec{q} - \\vec{p} = (2, 1, 2)^T$."
               ),
               "justificacion_md": "$\\vec{q} - \\vec{p}$ es el vector que va de un punto base de la recta hasta $\\vec{q}$.",
               "es_resultado": False},
              {"accion_md": (
                  "Producto cruz:\n\n"
                  "$(\\vec{q}-\\vec{p}) \\times \\vec{v} = ((1)(1) - (2)(1),\\ (2)(0) - (2)(1),\\ (2)(1) - (1)(0))^T = (-1, -2, 2)^T.$\n\n"
                  "Magnitud: $\\|(\\vec{q}-\\vec{p}) \\times \\vec{v}\\| = \\sqrt{1 + 4 + 4} = 3$."
               ),
               "justificacion_md": "$\\|(\\vec{q}-\\vec{p})\\times\\vec{v}\\|$ es el **área** del paralelogramo generado.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\|\\vec{v}\\| = \\sqrt{2}$. Distancia:\n\n"
                  "$$\\text{dist}(\\vec{q}, L) = \\dfrac{\\|(\\vec{q}-\\vec{p}) \\times \\vec{v}\\|}{\\|\\vec{v}\\|} = \\dfrac{3}{\\sqrt{2}} = \\dfrac{3\\sqrt{2}}{2}.$$"
               ),
               "justificacion_md": "**Interpretación:** área del paralelogramo $\\div$ base $=$ altura, que es exactamente la distancia perpendicular del punto a la recta.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Posiciones relativas de dos rectas en $\\mathbb{R}^3$.** Dadas dos rectas $L_1$ y $L_2$ con "
            "directores $\\vec{v}_1, \\vec{v}_2$, hay cuatro casos:\n\n"
            "1. **Coincidentes:** misma recta (un director es múltiplo del otro y comparten un punto).\n"
            "2. **Paralelas (no coincidentes):** $\\vec{v}_1 \\parallel \\vec{v}_2$ pero los puntos base no se conectan.\n"
            "3. **Se cortan:** $\\vec{v}_1 \\not\\parallel \\vec{v}_2$ y existen $t_1, t_2$ con $\\vec{p}_1 + t_1\\vec{v}_1 = \\vec{p}_2 + t_2\\vec{v}_2$.\n"
            "4. **Cruzadas (skew):** no paralelas y no se cortan — solo posible en $\\mathbb{R}^3$ o más.\n\n"
            "**Test algebraico:** dos rectas en $\\mathbb{R}^3$ son **coplanares** (casos 1, 2 o 3) si y solo si "
            "$[\\vec{v}_1, \\vec{v}_2, \\vec{p}_2 - \\vec{p}_1] = 0$. Si el producto triple es no nulo, son cruzadas.\n\n"
            "**En $\\mathbb{R}^2$** no hay rectas cruzadas — siempre se cortan o son paralelas."
        )),

        ej(
            "Ecuación implícita de una recta",
            "Da una recta en $\\mathbb{R}^3$ que pasa por $\\vec{p} = (2, -1, 4)$ con dirección $\\vec{v} = (1, 0, -2)$. "
            "(a) Forma paramétrica vectorial. (b) Forma simétrica. "
            "(c) Forma implícita como intersección de dos planos.",
            [
                "Paramétrica: $\\vec{r}(t) = \\vec{p} + t\\vec{v}$.",
                "Simétrica: despeja $t$ en cada componente cuando $v_i \\neq 0$.",
                "Para implícita, busca dos vectores **ortogonales a $\\vec{v}$** y úsalos como normales de los dos planos.",
            ],
            (
                "**(a)** $\\vec{r}(t) = (2, -1, 4) + t(1, 0, -2)$.\n\n"
                "**(b)** Como $v_2 = 0$, separamos: $\\dfrac{x-2}{1} = \\dfrac{z-4}{-2}, \\quad y = -1$.\n\n"
                "**(c)** Tomamos dos normales independientes ortogonales a $\\vec{v} = (1,0,-2)$:\n\n"
                "$\\vec{n}_1 = (2, 0, 1)$ — verifica $\\vec{n}_1 \\cdot \\vec{v} = 2 + 0 - 2 = 0$ ✓. Plano: $2(2) + 0 + 1(4) = 8$, luego $2x + z = 8$.\n\n"
                "$\\vec{n}_2 = (0, 1, 0)$ — verifica $\\vec{n}_2 \\cdot \\vec{v} = 0$ ✓. Plano: $y = -1$.\n\n"
                "**Sistema:** $\\begin{cases} 2x + z = 8 \\\\ y = -1 \\end{cases}$"
            ),
        ),

        ej(
            "Intersección de plano y recta",
            "Halla el punto donde la recta $\\vec{r}(t) = (1, 1, 1) + t(2, -1, 1)$ corta al plano $x + y + z = 9$.",
            [
                "Sustituye $\\vec{r}(t)$ en la ecuación del plano.",
                "Despeja $t$ y luego evalúa $\\vec{r}(t)$ en ese valor.",
            ],
            (
                "Sustituyendo: $(1 + 2t) + (1 - t) + (1 + t) = 9 \\Rightarrow 3 + 2t = 9 \\Rightarrow t = 3$.\n\n"
                "Punto de intersección: $\\vec{r}(3) = (1, 1, 1) + 3(2, -1, 1) = (7, -2, 4)$.\n\n"
                "**Verificación:** $7 + (-2) + 4 = 9$ ✓."
            ),
        ),

        ej(
            "Distancia entre dos rectas paralelas",
            "Calcula la distancia entre las rectas paralelas $L_1: \\vec{r}(t) = (1, 0, 0) + t(1, 1, 1)$ y "
            "$L_2: \\vec{r}(s) = (0, 2, 0) + s(2, 2, 2)$.",
            [
                "Verifica primero que son paralelas (un director es múltiplo del otro).",
                "Toma un punto $\\vec{q}$ de $L_2$ y calcula su distancia a $L_1$ usando la fórmula del producto cruz.",
            ],
            (
                "$\\vec{v}_2 = 2\\vec{v}_1$, así que sí son paralelas.\n\n"
                "Tomamos $\\vec{q} = (0, 2, 0)$ y $\\vec{p} = (1, 0, 0)$, $\\vec{v} = (1, 1, 1)$.\n\n"
                "$\\vec{q} - \\vec{p} = (-1, 2, 0)$.\n\n"
                "$(\\vec{q}-\\vec{p}) \\times \\vec{v} = ((2)(1) - (0)(1), (0)(1) - (-1)(1), (-1)(1) - (2)(1))^T = (2, 1, -3)^T$.\n\n"
                "$\\|(\\vec{q}-\\vec{p}) \\times \\vec{v}\\| = \\sqrt{4 + 1 + 9} = \\sqrt{14}$.\n\n"
                "$\\|\\vec{v}\\| = \\sqrt{3}$.\n\n"
                "$\\text{dist}(L_1, L_2) = \\sqrt{14}/\\sqrt{3} = \\sqrt{42}/3$."
            ),
        ),

        b("verificacion",
          intro_md="Antes del cierre, verifica que dominas la geometría afín:",
          preguntas=[
              {
                  "enunciado_md": "El plano $2x - y + 3z = 7$ tiene como vector normal:",
                  "opciones_md": [
                      "$(2, -1, 3)^T$",
                      "$(2, 1, 3)^T$",
                      "$(7, 0, 0)^T$",
                      "$(-2, 1, -3)^T$",
                  ],
                  "correcta": "A",
                  "pista_md": "En $ax + by + cz = d$ los coeficientes son las componentes de $\\vec{n}$.",
                  "explicacion_md": (
                      "La ecuación $ax + by + cz = d$ es exactamente $\\vec{n}\\cdot\\vec{r} = d$ con $\\vec{n} = (a, b, c)^T$. "
                      "Por eso los coeficientes del lado izquierdo **son** las componentes del normal."
                  ),
              },
              {
                  "enunciado_md": "Dos rectas en $\\mathbb{R}^3$ con directores no paralelos:",
                  "opciones_md": [
                      "Siempre se cortan en un punto",
                      "Pueden cortarse o ser cruzadas (skew)",
                      "Siempre son paralelas",
                      "Siempre son coincidentes",
                  ],
                  "correcta": "B",
                  "pista_md": "En $\\mathbb{R}^2$ siempre se cortan, pero $\\mathbb{R}^3$ tiene más espacio.",
                  "explicacion_md": (
                      "En $\\mathbb{R}^3$ existen rectas **cruzadas** (skew): no paralelas y no se cortan. "
                      "El test es $[\\vec{v}_1, \\vec{v}_2, \\vec{p}_2 - \\vec{p}_1] \\neq 0 \\Rightarrow$ cruzadas. "
                      "En $\\mathbb{R}^2$ esto es imposible — solo hay paralelas o secantes."
                  ),
              },
              {
                  "enunciado_md": "¿Cuántas ecuaciones lineales se necesitan para describir una recta como intersección de hiperplanos en $\\mathbb{R}^4$?",
                  "opciones_md": ["1", "2", "3", "4"],
                  "correcta": "C",
                  "pista_md": "Cada ecuación independiente baja la dimensión en 1. Una recta tiene dimensión 1.",
                  "explicacion_md": (
                      "Cada ecuación lineal define un hiperplano (dimensión $n - 1 = 3$). $k$ ecuaciones independientes "
                      "dan dimensión $n - k$. Para llegar de $4$ a una recta (dim 1), necesitamos $4 - 1 = 3$ ecuaciones."
                  ),
              },
          ]),

        b("errores_comunes",
          items_md=[
              "**Confundir el vector normal del plano con el director de la recta.** El normal es **ortogonal**, el director es **paralelo**.",
              "**Olvidar dividir por $\\|\\vec{n}\\|$** en la fórmula de distancia punto-plano.",
              "**Pensar que dos rectas en $\\mathbb{R}^3$ no paralelas siempre se cortan.** Pueden ser **cruzadas** (no se cortan ni son paralelas).",
              "**Usar la forma simétrica cuando algún $v_i = 0$.** No se puede dividir por 0; en ese caso fija la coordenada correspondiente.",
              "**Mezclar parámetro de dos rectas distintas** al buscar intersección. Usa nombres distintos $t$ y $s$.",
              "**Decir que el plano $ax+by+cz=d$ pasa por el origen.** Solo si $d = 0$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Recta paramétrica:** $\\vec{r}(t) = \\vec{p} + t\\vec{v}$ — dirección + punto base.",
              "**Plano:** $\\vec{n}\\cdot(\\vec{r} - \\vec{p}_0) = 0$ ⟺ $ax + by + cz = d$ (forma punto-normal e implícita).",
              "**Hiperplano en $\\mathbb{R}^n$:** $\\vec{n} \\cdot \\vec{r} = d$ — una sola ecuación lineal.",
              "**Sistema lineal $\\leftrightarrow$ intersección de hiperplanos** (preview cap 2).",
              "**Distancia punto-hiperplano:** $|\\vec{n}\\cdot\\vec{q} - d|/\\|\\vec{n}\\|$.",
              "**Distancia punto-recta en $\\mathbb{R}^3$:** $\\|(\\vec{q}-\\vec{p}) \\times \\vec{v}\\|/\\|\\vec{v}\\|$.",
              "**Producto cruz** entrega normales (de pares de directores) y directores (de pares de normales) — útil para cambiar entre formas paramétrica e implícita.",
              "**Próximo capítulo:** sistemas lineales y matrices — generalización masiva de lo visto aquí.",
          ]),
    ]
    return {
        "id": "lec-al-1-4-rectas-y-planos",
        "title": "Rectas y planos",
        "description": "Rectas y planos en forma paramétrica e implícita, hiperplanos en $\\mathbb{R}^n$, distancias y conexión con sistemas lineales.",
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

    course_doc = {
        "id": course_id,
        "title": "Álgebra Lineal",
        "description": "Vectores en $\\mathbb{R}^n$, sistemas lineales, matrices, determinantes, espacios vectoriales, transformaciones lineales, ortogonalidad y autovalores.",
        "category": "Matemáticas",
        "level": "Avanzado",
        "modules_count": 8,
        "rating": 4.8,
        "summary": "Curso completo de álgebra lineal para alumnos universitarios chilenos.",
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

    chapter_id = "ch-al-espacio"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Espacio",
        "description": "Vectores en $\\mathbb{R}^n$, producto punto, producto cruz, rectas, planos e hiperplanos. Enfoque algebraico con preview de subespacios y sistemas lineales.",
        "order": 1,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_1_1, lesson_1_2, lesson_1_3, lesson_1_4]
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
    print(f"✅ Capítulo 1 — Espacio listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
