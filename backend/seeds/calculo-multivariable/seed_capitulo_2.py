"""
Seed del curso Cálculo Multivariable — Capítulo 2: Espacio.
5 lecciones:
  2.1 Vectores
  2.2 Producto punto
  2.3 Producto cruz
  2.4 Rectas y planos
  2.5 Superficies cuádricas

Incluye figuras 3D con prompt_image_md listos para ChatGPT Images en los temas
geométricos (vectores, ángulos, productos, planos, superficies).

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


def ej(titulo, enunciado, pistas, solucion):
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def formulas(titulo, body):
    return b("definicion", titulo=titulo, body_md=body)


def now():
    return datetime.now(timezone.utc).isoformat()


STYLE = (
    "Estilo: diagrama matemático 3D educativo limpio, fondo blanco, líneas claras, "
    "etiquetas en español, notación matemática con buena tipografía. Acentos teal "
    "#06b6d4 y ámbar #f59e0b. Vista isométrica simple. Sin sombras dramáticas, sin "
    "texturas pesadas. Apto para libro universitario."
)


# =====================================================================
# 2.1 Vectores
# =====================================================================
def lesson_2_1():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora trabajamos con números reales (escalares). Para describir el espacio físico "
            "necesitamos algo más: cantidades con **dirección y magnitud**. Esos son los **vectores**. "
            "El cálculo en 3D — y casi toda la física — se construye sobre ellos.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Comprender vectores como puntos de $\\mathbb{R}^2$ o $\\mathbb{R}^3$.\n"
            "- Sumar vectores y multiplicarlos por escalares (algebraica y geométricamente).\n"
            "- Calcular **magnitud** y **vectores unitarios**.\n"
            "- Manejar la base estándar $\\vec{i}, \\vec{j}, \\vec{k}$ y la **distancia entre puntos** en $\\mathbb{R}^3$."
        )),

        b("intuicion",
          titulo="Punto vs vector",
          body_md=(
              "**Punto** $P = (3, 4, 5)$: una **ubicación** en el espacio.\n\n"
              "**Vector** $\\vec{v} = \\langle 3, 4, 5 \\rangle$: una **dirección con magnitud**, sin posición fija. "
              "Se puede representar gráficamente como una flecha desde el origen al punto $(3, 4, 5)$, "
              "pero **el vector no \"vive\" en el origen** — la misma flecha trasladada a otro punto representa el mismo vector.\n\n"
              "Aunque las componentes coinciden, las operaciones difieren: dos puntos no se suman; dos vectores sí."
          )),

        b("definicion",
          titulo="Vectores en $\\mathbb{R}^2$ y $\\mathbb{R}^3$",
          body_md=(
              "**En $\\mathbb{R}^2$:** $\\vec{v} = \\langle a, b \\rangle$ con $a, b \\in \\mathbb{R}$.\n\n"
              "**En $\\mathbb{R}^3$:** $\\vec{v} = \\langle a, b, c \\rangle$ con $a, b, c \\in \\mathbb{R}$.\n\n"
              "**Notaciones equivalentes:** $\\vec{v}$, $\\mathbf{v}$, $\\vec{v} = a\\vec{i} + b\\vec{j} + c\\vec{k}$ (forma con la base estándar).\n\n"
              "**Vector entre dos puntos:** dado $P = (p_1, p_2, p_3)$ y $Q = (q_1, q_2, q_3)$, el vector $\\vec{PQ}$ que va de $P$ a $Q$ es:\n\n"
              "$$\\vec{PQ} = \\langle q_1 - p_1, q_2 - p_2, q_3 - p_3 \\rangle$$"
          )),

        fig(
            "Diagrama 3D de un sistema de coordenadas con ejes x, y, z. Mostrar un vector v = ⟨3, 4, "
            "5⟩ representado como una flecha desde el origen (0,0,0) hasta el punto (3, 4, 5). "
            "Etiquetas en los ejes: x, y, z. Etiqueta del vector: 'v'. Marcar las componentes "
            "proyectando el vector en cada eje: una flecha a lo largo de x hasta x=3, otra paralela "
            "al eje y desde (3,0,0) hasta (3,4,0), otra paralela al eje z desde (3,4,0) hasta "
            "(3,4,5). Estas tres componentes en color punteado (líneas auxiliares). El vector "
            "principal en color teal grueso. Vista isométrica clara. " + STYLE
        ),

        b("definicion",
          titulo="Operaciones con vectores",
          body_md=(
              "Sean $\\vec{u} = \\langle u_1, u_2, u_3 \\rangle$, $\\vec{v} = \\langle v_1, v_2, v_3 \\rangle$ y $c \\in \\mathbb{R}$:\n\n"
              "**Suma:** $\\vec{u} + \\vec{v} = \\langle u_1 + v_1, u_2 + v_2, u_3 + v_3 \\rangle$.\n\n"
              "**Producto por escalar:** $c \\, \\vec{v} = \\langle c v_1, c v_2, c v_3 \\rangle$.\n\n"
              "**Resta:** $\\vec{u} - \\vec{v} = \\vec{u} + (-1)\\vec{v}$.\n\n"
              "**Vector cero:** $\\vec{0} = \\langle 0, 0, 0 \\rangle$.\n\n"
              "**Geométricamente:** la suma se construye con la **regla del paralelogramo** (o la **regla cabeza-cola**: poner el inicio de $\\vec{v}$ en el final de $\\vec{u}$). "
              "El producto por escalar **estira o comprime** el vector; si $c < 0$, lo invierte."
          )),

        fig(
            "Suma de vectores en 2D ilustrada con la regla del paralelogramo. Plano cartesiano con "
            "origen. Dos vectores u (en color teal) y v (en color ámbar) saliendo del origen hacia "
            "puntos distintos. Construir el paralelogramo trazando líneas paralelas (en gris "
            "punteado): una paralela a v desde la punta de u, otra paralela a u desde la punta de "
            "v. La diagonal del paralelogramo desde el origen hasta el vértice opuesto, en color "
            "azul oscuro grueso, etiquetada 'u + v'. Etiquetas: 'u', 'v', 'u + v'. " + STYLE
        ),

        b("definicion",
          titulo="Magnitud (norma) y vectores unitarios",
          body_md=(
              "**Magnitud** de $\\vec{v} = \\langle a, b, c \\rangle$:\n\n"
              "$$\\|\\vec{v}\\| = \\sqrt{a^2 + b^2 + c^2}$$\n\n"
              "(En $\\mathbb{R}^2$: $\\|\\vec{v}\\| = \\sqrt{a^2 + b^2}$.) Es la longitud de la flecha — siempre $\\geq 0$ y vale $0$ solo si $\\vec{v} = \\vec{0}$.\n\n"
              "**Vector unitario:** vector con magnitud $1$. Dado $\\vec{v} \\neq \\vec{0}$, su unitario en la misma dirección es:\n\n"
              "$$\\hat{v} = \\dfrac{\\vec{v}}{\\|\\vec{v}\\|}$$\n\n"
              "**Distancia entre puntos** $P, Q$ es $\\|\\vec{PQ}\\|$:\n\n"
              "$$d(P, Q) = \\sqrt{(q_1 - p_1)^2 + (q_2 - p_2)^2 + (q_3 - p_3)^2}$$"
          )),

        formulas(
            titulo="Base estándar y propiedades",
            body=(
                "**Base estándar de $\\mathbb{R}^3$:**\n\n"
                "$$\\vec{i} = \\langle 1, 0, 0\\rangle, \\quad \\vec{j} = \\langle 0, 1, 0\\rangle, \\quad \\vec{k} = \\langle 0, 0, 1\\rangle$$\n\n"
                "Cualquier vector se descompone como $\\vec{v} = a\\vec{i} + b\\vec{j} + c\\vec{k}$.\n\n"
                "**Propiedades de las operaciones:**\n\n"
                "| Propiedad | Fórmula |\n|---|---|\n"
                "| Conmutativa (suma) | $\\vec{u} + \\vec{v} = \\vec{v} + \\vec{u}$ |\n"
                "| Asociativa (suma) | $(\\vec{u}+\\vec{v})+\\vec{w} = \\vec{u}+(\\vec{v}+\\vec{w})$ |\n"
                "| Identidad | $\\vec{v} + \\vec{0} = \\vec{v}$ |\n"
                "| Inverso aditivo | $\\vec{v} + (-\\vec{v}) = \\vec{0}$ |\n"
                "| Distributiva (escalar) | $c(\\vec{u}+\\vec{v}) = c\\vec{u} + c\\vec{v}$ |\n"
                "| Asociativa (escalar) | $(cd)\\vec{v} = c(d\\vec{v})$ |"
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Vector entre dos puntos y su magnitud",
          problema_md="Sea $P = (1, -2, 3)$ y $Q = (4, 1, -1)$. Hallar $\\vec{PQ}$, su magnitud y un vector unitario en su dirección.",
          pasos=[
              {"accion_md": "**Vector $\\vec{PQ}$:** $\\vec{PQ} = \\langle 4-1, 1-(-2), -1-3 \\rangle = \\langle 3, 3, -4 \\rangle$.",
               "justificacion_md": "Diferencia de coordenadas, en orden destino menos origen.",
               "es_resultado": False},
              {"accion_md": "**Magnitud:** $\\|\\vec{PQ}\\| = \\sqrt{3^2 + 3^2 + (-4)^2} = \\sqrt{9 + 9 + 16} = \\sqrt{34}$.",
               "justificacion_md": "Aplicación directa de la fórmula.",
               "es_resultado": False},
              {"accion_md": "**Unitario:** $\\hat{u} = \\dfrac{1}{\\sqrt{34}} \\langle 3, 3, -4 \\rangle = \\left\\langle \\dfrac{3}{\\sqrt{34}}, \\dfrac{3}{\\sqrt{34}}, \\dfrac{-4}{\\sqrt{34}} \\right\\rangle$.",
               "justificacion_md": "**Verificación:** $\\|\\hat{u}\\| = \\sqrt{(9 + 9 + 16)/34} = 1$. ✓",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica conceptos básicos:",
          preguntas=[
              {
                  "enunciado_md": "$\\|\\langle 1, 2, 2 \\rangle\\| = ?$",
                  "opciones_md": ["$5$", "$3$", "$\\sqrt{5}$", "$\\sqrt{6}$"],
                  "correcta": "B",
                  "pista_md": "$\\sqrt{1 + 4 + 4} = ?$",
                  "explicacion_md": (
                      "$\\sqrt{1^2 + 2^2 + 2^2} = \\sqrt{9} = 3$. Es el ejemplo clásico de un \"trío pitagórico\" en 3D."
                  ),
              },
              {
                  "enunciado_md": "Si $\\vec{u}$ es unitario, entonces $5\\vec{u}$ tiene magnitud:",
                  "opciones_md": ["$1$", "$5$", "$25$", "$\\sqrt{5}$"],
                  "correcta": "B",
                  "pista_md": "Multiplicar por un escalar $c$ multiplica la magnitud por $|c|$.",
                  "explicacion_md": (
                      "$\\|c \\vec{u}\\| = |c| \\cdot \\|\\vec{u}\\| = 5 \\cdot 1 = 5$. **Truco útil:** para construir un vector con magnitud específica $L$ en una dirección dada, calcula el unitario y multiplícalo por $L$."
                  ),
              },
          ]),

        ej(
            titulo="Combinación lineal",
            enunciado=(
                "Sean $\\vec{u} = \\langle 2, -1, 3 \\rangle$ y $\\vec{v} = \\langle 1, 0, 4 \\rangle$. "
                "Calcula $3\\vec{u} - 2\\vec{v}$ y su magnitud."
            ),
            pistas=[
                "$3\\vec{u} = \\langle 6, -3, 9 \\rangle$, $2\\vec{v} = \\langle 2, 0, 8 \\rangle$.",
                "Resta componente a componente.",
            ],
            solucion=(
                "$3\\vec{u} - 2\\vec{v} = \\langle 6 - 2, -3 - 0, 9 - 8 \\rangle = \\langle 4, -3, 1 \\rangle$.\n\n"
                "Magnitud: $\\sqrt{16 + 9 + 1} = \\sqrt{26}$."
            ),
        ),

        ej(
            titulo="Vector con dirección y magnitud dadas",
            enunciado=(
                "Halla un vector de magnitud $10$ en la misma dirección que $\\vec{w} = \\langle -1, 2, 2 \\rangle$."
            ),
            pistas=[
                "Calcula primero $\\hat{w} = \\vec{w}/\\|\\vec{w}\\|$.",
                "$\\|\\vec{w}\\| = \\sqrt{1 + 4 + 4} = 3$.",
                "Multiplica $\\hat{w}$ por $10$.",
            ],
            solucion=(
                "$\\|\\vec{w}\\| = 3$, así $\\hat{w} = \\langle -1/3, 2/3, 2/3 \\rangle$.\n\n"
                "Vector deseado: $10 \\hat{w} = \\langle -10/3, 20/3, 20/3 \\rangle$. **Magnitud:** $10 \\cdot \\|\\hat{w}\\| = 10$. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir punto con vector.** Tienen las mismas coordenadas pero distinto rol: punto es ubicación, vector es desplazamiento.",
              "**Restar al revés** al hacer $\\vec{PQ}$: es $Q - P$ (destino menos origen), no $P - Q$.",
              "**Olvidar la raíz** en la magnitud: $\\|\\vec{v}\\|^2 = a^2 + b^2 + c^2$, así $\\|\\vec{v}\\| = \\sqrt{a^2+b^2+c^2}$.",
              "**Pensar que un vector tiene posición.** Tu profesor puede dibujarlo en cualquier lugar; lo único fijo son sus componentes.",
              "**Sumar vectores como si fueran números** (sin componentes): $\\vec{u} + \\vec{v}$ se hace componente a componente.",
          ]),

        b("resumen",
          puntos_md=[
              "**Vector** = dirección + magnitud, sin posición fija.",
              "**Operaciones componente a componente:** suma, resta, multiplicación por escalar.",
              "**Magnitud:** $\\|\\vec{v}\\| = \\sqrt{a^2 + b^2 + c^2}$.",
              "**Unitario:** $\\hat{v} = \\vec{v}/\\|\\vec{v}\\|$.",
              "**Distancia** entre puntos $P, Q$: $\\|\\vec{PQ}\\|$.",
              "**Base estándar:** $\\vec{i}, \\vec{j}, \\vec{k}$.",
              "**Próxima lección:** producto punto, ángulos y proyecciones.",
          ]),
    ]
    return {
        "id": "lec-mvar-2-1-vectores",
        "title": "Vectores",
        "description": "Vectores en $\\mathbb{R}^2$ y $\\mathbb{R}^3$, operaciones, magnitud, unitarios y distancia entre puntos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 2.2 Producto punto
# =====================================================================
def lesson_2_2():
    blocks = [
        b("texto", body_md=(
            "El **producto punto** (o producto escalar) es la primera de las dos operaciones esenciales "
            "entre vectores. Combina dos vectores en un **número** (escalar) que captura información "
            "geométrica: ángulos, perpendicularidad y proyecciones.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular $\\vec{u} \\cdot \\vec{v}$ algebraica y geométricamente.\n"
            "- Encontrar el **ángulo** entre dos vectores.\n"
            "- Detectar **ortogonalidad** ($\\vec{u} \\cdot \\vec{v} = 0$).\n"
            "- Calcular la **proyección** de un vector sobre otro."
        )),

        b("definicion",
          titulo="Producto punto: definición algebraica",
          body_md=(
              "Sean $\\vec{u} = \\langle u_1, u_2, u_3 \\rangle$ y $\\vec{v} = \\langle v_1, v_2, v_3 \\rangle$. Su **producto punto** es:\n\n"
              "$$\\vec{u} \\cdot \\vec{v} = u_1 v_1 + u_2 v_2 + u_3 v_3$$\n\n"
              "**Resultado: un escalar** (no un vector). De ahí el nombre alternativo \"producto escalar\".\n\n"
              "**En $\\mathbb{R}^2$:** $\\vec{u} \\cdot \\vec{v} = u_1 v_1 + u_2 v_2$."
          )),

        formulas(
            titulo="Propiedades del producto punto",
            body=(
                "| Propiedad | Fórmula |\n|---|---|\n"
                "| Conmutativa | $\\vec{u} \\cdot \\vec{v} = \\vec{v} \\cdot \\vec{u}$ |\n"
                "| Distributiva | $\\vec{u} \\cdot (\\vec{v} + \\vec{w}) = \\vec{u}\\cdot\\vec{v} + \\vec{u}\\cdot\\vec{w}$ |\n"
                "| Asociativa con escalar | $(c\\vec{u}) \\cdot \\vec{v} = c(\\vec{u}\\cdot\\vec{v})$ |\n"
                "| Magnitud | $\\vec{v} \\cdot \\vec{v} = \\|\\vec{v}\\|^2$ |\n"
                "| Vector cero | $\\vec{0} \\cdot \\vec{v} = 0$ |\n\n"
                "**Atención:** **NO** es asociativo: $(\\vec{u} \\cdot \\vec{v}) \\cdot \\vec{w}$ no tiene sentido — el primer paso da un escalar, no un vector."
            ),
        ),

        b("teorema",
          nombre="Producto punto: definición geométrica",
          enunciado_md=(
              "Sea $\\theta$ el ángulo entre $\\vec{u}$ y $\\vec{v}$ (con $0 \\leq \\theta \\leq \\pi$). Entonces:\n\n"
              "$$\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\| \\, \\|\\vec{v}\\| \\cos\\theta$$\n\n"
              "**Despejando el ángulo:**\n\n"
              "$$\\cos\\theta = \\dfrac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{u}\\| \\, \\|\\vec{v}\\|}$$"
          ),
          demostracion_md=(
              "Por la ley del coseno aplicada al triángulo formado por $\\vec{u}, \\vec{v}, \\vec{u} - \\vec{v}$:\n\n"
              "$$\\|\\vec{u}-\\vec{v}\\|^2 = \\|\\vec{u}\\|^2 + \\|\\vec{v}\\|^2 - 2\\|\\vec{u}\\|\\|\\vec{v}\\|\\cos\\theta$$\n\n"
              "Expandiendo el lado izquierdo con la propiedad $\\vec{a} \\cdot \\vec{a} = \\|\\vec{a}\\|^2$:\n\n"
              "$$\\|\\vec{u}-\\vec{v}\\|^2 = (\\vec{u}-\\vec{v}) \\cdot (\\vec{u}-\\vec{v}) = \\|\\vec{u}\\|^2 - 2\\vec{u}\\cdot\\vec{v} + \\|\\vec{v}\\|^2$$\n\n"
              "Igualando: $-2\\vec{u}\\cdot\\vec{v} = -2\\|\\vec{u}\\|\\|\\vec{v}\\|\\cos\\theta$, así $\\vec{u}\\cdot\\vec{v} = \\|\\vec{u}\\|\\|\\vec{v}\\|\\cos\\theta$."
          )),

        fig(
            "Diagrama 2D del ángulo entre dos vectores. Plano cartesiano con origen. Dos vectores u "
            "(en color teal) y v (en color ámbar) saliendo desde el origen formando un ángulo θ "
            "entre ellos. Marcar el ángulo θ con un arco pequeño en el origen, etiquetado 'θ'. Los "
            "vectores etiquetados 'u' y 'v' cerca de sus puntas. Estilo limpio. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Ángulo entre dos vectores",
          problema_md="Hallar el ángulo entre $\\vec{u} = \\langle 1, 2, 3 \\rangle$ y $\\vec{v} = \\langle -1, 1, 2 \\rangle$.",
          pasos=[
              {"accion_md": "**Producto punto:** $\\vec{u} \\cdot \\vec{v} = 1(-1) + 2(1) + 3(2) = -1 + 2 + 6 = 7$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "**Magnitudes:** $\\|\\vec{u}\\| = \\sqrt{1 + 4 + 9} = \\sqrt{14}$, $\\|\\vec{v}\\| = \\sqrt{1+1+4} = \\sqrt{6}$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "**Coseno:** $\\cos\\theta = \\dfrac{7}{\\sqrt{14}\\sqrt{6}} = \\dfrac{7}{\\sqrt{84}} = \\dfrac{7}{2\\sqrt{21}}$.\n\n"
                            "**Ángulo:** $\\theta = \\arccos\\left(\\dfrac{7}{2\\sqrt{21}}\\right) \\approx \\arccos(0.764) \\approx 40.2°$.",
               "justificacion_md": "El ángulo agudo es típico cuando $\\vec{u}\\cdot\\vec{v} > 0$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Ortogonalidad",
          body_md=(
              "Dos vectores no nulos son **ortogonales** (perpendiculares) si y solo si:\n\n"
              "$$\\vec{u} \\cdot \\vec{v} = 0$$\n\n"
              "**Justificación:** $\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\|\\|\\vec{v}\\|\\cos\\theta = 0 \\iff \\cos\\theta = 0 \\iff \\theta = \\pi/2$.\n\n"
              "**Por convención:** $\\vec{0}$ se considera ortogonal a cualquier vector.\n\n"
              "**Signo del producto punto:**\n\n"
              "- $\\vec{u} \\cdot \\vec{v} > 0$: ángulo **agudo** (menos de $90°$).\n"
              "- $\\vec{u} \\cdot \\vec{v} = 0$: **perpendiculares**.\n"
              "- $\\vec{u} \\cdot \\vec{v} < 0$: ángulo **obtuso** (más de $90°$)."
          )),

        b("definicion",
          titulo="Proyección y componente",
          body_md=(
              "**Proyección (vectorial) de $\\vec{u}$ sobre $\\vec{v}$:** el vector que va de $\\vec{0}$ al \"pie de la perpendicular\" desde la punta de $\\vec{u}$ hacia la línea de $\\vec{v}$:\n\n"
              "$$\\text{proy}_{\\vec{v}}\\, \\vec{u} = \\dfrac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{v}\\|^2} \\vec{v}$$\n\n"
              "**Componente escalar (proyección escalar):** la \"longitud con signo\" de la proyección:\n\n"
              "$$\\text{comp}_{\\vec{v}}\\, \\vec{u} = \\dfrac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{v}\\|}$$\n\n"
              "Es positiva si la proyección apunta en la dirección de $\\vec{v}$, negativa si apunta opuesta."
          )),

        fig(
            "Proyección de un vector sobre otro. Plano cartesiano con dos vectores saliendo del "
            "origen: u (en color teal) yendo hacia arriba-derecha, y v (en color azul oscuro) "
            "yendo hacia la derecha. Trazar una línea perpendicular punteada (en gris) desde la "
            "punta de u que cae sobre la línea (extendida) de v, formando un triángulo rectángulo. "
            "El segmento en la línea de v desde el origen hasta el pie de la perpendicular es la "
            "proyección, dibujado con flecha gruesa en color ámbar y etiquetado 'proy_v u'. "
            "Etiquetas: 'u', 'v', 'proy_v u'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Proyección de un vector",
          problema_md="Calcular $\\text{proy}_{\\vec{v}} \\vec{u}$ con $\\vec{u} = \\langle 3, 4, 0 \\rangle$ y $\\vec{v} = \\langle 1, 0, 0 \\rangle$.",
          pasos=[
              {"accion_md": "**Producto punto:** $\\vec{u} \\cdot \\vec{v} = 3 + 0 + 0 = 3$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "**Magnitud al cuadrado:** $\\|\\vec{v}\\|^2 = 1$.",
               "justificacion_md": "$\\vec{v}$ es un vector unitario en la dirección de $\\vec{i}$.",
               "es_resultado": False},
              {"accion_md": "$$\\text{proy}_{\\vec{v}}\\, \\vec{u} = \\dfrac{3}{1} \\langle 1, 0, 0 \\rangle = \\langle 3, 0, 0 \\rangle$$",
               "justificacion_md": "**Tiene sentido geométrico:** la proyección de $\\langle 3, 4, 0 \\rangle$ sobre el eje $x$ es $\\langle 3, 0, 0 \\rangle$ (la primera componente).",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica las aplicaciones:",
          preguntas=[
              {
                  "enunciado_md": "$\\vec{u} = \\langle 1, 2 \\rangle$ y $\\vec{v} = \\langle 4, -2 \\rangle$. ¿Son ortogonales?",
                  "opciones_md": ["Sí", "No, son paralelos", "No, ángulo agudo", "No, ángulo obtuso"],
                  "correcta": "A",
                  "pista_md": "Calcula $\\vec{u} \\cdot \\vec{v}$.",
                  "explicacion_md": (
                      "$\\vec{u} \\cdot \\vec{v} = 1(4) + 2(-2) = 4 - 4 = 0$. **Sí son ortogonales.**"
                  ),
              },
              {
                  "enunciado_md": "Si $\\vec{u} \\cdot \\vec{v} = -5$ y ambos son no nulos, el ángulo entre ellos es:",
                  "opciones_md": [
                      "Agudo (menos de 90°)",
                      "Recto (90°)",
                      "Obtuso (más de 90°)",
                      "Recto siempre",
                  ],
                  "correcta": "C",
                  "pista_md": "Signo del producto punto = signo del coseno del ángulo.",
                  "explicacion_md": (
                      "$\\vec{u}\\cdot\\vec{v} < 0 \\implies \\cos\\theta < 0 \\implies 90° < \\theta < 180°$. **Obtuso.**"
                  ),
              },
          ]),

        ej(
            titulo="Verificar ortogonalidad",
            enunciado=(
                "Determina el valor de $k$ que hace ortogonales a $\\vec{u} = \\langle 2, k, 1 \\rangle$ y $\\vec{v} = \\langle 1, 3, -2 \\rangle$."
            ),
            pistas=[
                "Plantea $\\vec{u} \\cdot \\vec{v} = 0$.",
                "Despeja $k$.",
            ],
            solucion=(
                "$\\vec{u} \\cdot \\vec{v} = 2(1) + k(3) + 1(-2) = 2 + 3k - 2 = 3k$.\n\n"
                "$3k = 0 \\implies k = 0$. (Es decir, $\\vec{u} = \\langle 2, 0, 1 \\rangle$ y $\\vec{v} = \\langle 1, 3, -2 \\rangle$ son perpendiculares.)"
            ),
        ),

        ej(
            titulo="Trabajo (aplicación física)",
            enunciado=(
                "Una fuerza $\\vec{F} = \\langle 3, 1, -2 \\rangle$ N actúa sobre un objeto que se desplaza "
                "$\\vec{d} = \\langle 2, 4, 0 \\rangle$ m. Calcula el **trabajo** $W = \\vec{F} \\cdot \\vec{d}$."
            ),
            pistas=[
                "Trabajo es el producto punto cuando la fuerza es constante.",
                "$W = F_1 d_1 + F_2 d_2 + F_3 d_3$.",
            ],
            solucion=(
                "$W = 3(2) + 1(4) + (-2)(0) = 6 + 4 + 0 = 10$ J.\n\n"
                "**Interpretación:** $W = \\|\\vec{F}\\| \\|\\vec{d}\\| \\cos\\theta$ — la componente de la fuerza paralela al desplazamiento es lo que efectivamente \"empuja\"."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir producto punto con suma de productos.** El resultado es **un escalar**, no un vector.",
              "**Aplicar 'asociatividad' a tres vectores:** $(\\vec{u} \\cdot \\vec{v}) \\cdot \\vec{w}$ no tiene sentido — el primer producto da un escalar.",
              "**Olvidar elevar al cuadrado** la magnitud en la fórmula de proyección: $\\|\\vec{v}\\|^2$, no $\\|\\vec{v}\\|$.",
              "**Confundir proyección vectorial con escalar.** La vectorial es un vector; la escalar es un número (con signo).",
              "**Pensar que $\\vec{u} \\cdot \\vec{v} > 0$ implica vectores en la misma dirección.** Solo implica ángulo agudo (entre $0°$ y $90°$).",
          ]),

        b("resumen",
          puntos_md=[
              "**Algebraica:** $\\vec{u} \\cdot \\vec{v} = u_1 v_1 + u_2 v_2 + u_3 v_3$ (escalar).",
              "**Geométrica:** $\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\|\\|\\vec{v}\\|\\cos\\theta$.",
              "**Ortogonalidad:** $\\vec{u} \\cdot \\vec{v} = 0$ (vectores no nulos).",
              "**Proyección vectorial:** $\\text{proy}_{\\vec{v}}\\vec{u} = (\\vec{u}\\cdot\\vec{v}/\\|\\vec{v}\\|^2)\\vec{v}$.",
              "**Componente escalar:** $\\text{comp}_{\\vec{v}}\\vec{u} = \\vec{u}\\cdot\\vec{v}/\\|\\vec{v}\\|$.",
              "**Aplicación física:** trabajo $W = \\vec{F} \\cdot \\vec{d}$.",
              "**Próxima lección:** producto cruz — el otro producto, exclusivo de $\\mathbb{R}^3$.",
          ]),
    ]
    return {
        "id": "lec-mvar-2-2-producto-punto",
        "title": "Producto punto",
        "description": "Producto escalar entre vectores: definición algebraica y geométrica, ángulos, ortogonalidad y proyecciones.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# 2.3 Producto cruz
# =====================================================================
def lesson_2_3():
    blocks = [
        b("texto", body_md=(
            "El **producto cruz** (o producto vectorial) es la otra operación esencial entre vectores, "
            "**exclusiva de $\\mathbb{R}^3$**. A diferencia del producto punto, devuelve **otro vector** — "
            "uno perpendicular a los dos originales, con magnitud igual al área del paralelogramo que "
            "forman.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular $\\vec{u} \\times \\vec{v}$ usando la fórmula del determinante.\n"
            "- Conocer las propiedades (anticonmutatividad, distributiva).\n"
            "- Interpretar geométricamente: dirección por la **regla de la mano derecha**, magnitud como **área**.\n"
            "- Calcular **áreas** de paralelogramos/triángulos y **volúmenes** de paralelepípedos."
        )),

        b("definicion",
          titulo="Producto cruz: fórmula con determinante",
          body_md=(
              "Sean $\\vec{u} = \\langle u_1, u_2, u_3 \\rangle$ y $\\vec{v} = \\langle v_1, v_2, v_3 \\rangle$. Su **producto cruz** es:\n\n"
              "$$\\vec{u} \\times \\vec{v} = \\begin{vmatrix} \\vec{i} & \\vec{j} & \\vec{k} \\\\ u_1 & u_2 & u_3 \\\\ v_1 & v_2 & v_3 \\end{vmatrix}$$\n\n"
              "**Expandiendo por la primera fila:**\n\n"
              "$$\\vec{u} \\times \\vec{v} = (u_2 v_3 - u_3 v_2)\\vec{i} - (u_1 v_3 - u_3 v_1)\\vec{j} + (u_1 v_2 - u_2 v_1)\\vec{k}$$\n\n"
              "**Resultado: un vector** en $\\mathbb{R}^3$. **Solo definido en 3D** — en $\\mathbb{R}^2$ no hay producto cruz."
          )),

        formulas(
            titulo="Propiedades del producto cruz",
            body=(
                "| Propiedad | Fórmula |\n|---|---|\n"
                "| Anticonmutativa | $\\vec{u} \\times \\vec{v} = -(\\vec{v} \\times \\vec{u})$ |\n"
                "| Distributiva | $\\vec{u} \\times (\\vec{v}+\\vec{w}) = \\vec{u}\\times\\vec{v} + \\vec{u}\\times\\vec{w}$ |\n"
                "| Asociativa con escalar | $(c\\vec{u})\\times\\vec{v} = c(\\vec{u}\\times\\vec{v})$ |\n"
                "| Producto consigo mismo | $\\vec{v} \\times \\vec{v} = \\vec{0}$ |\n"
                "| Vector cero | $\\vec{0} \\times \\vec{v} = \\vec{0}$ |\n\n"
                "**Atención: NO** es asociativo: $(\\vec{u}\\times\\vec{v})\\times\\vec{w} \\neq \\vec{u}\\times(\\vec{v}\\times\\vec{w})$ en general.\n\n"
                "**Productos cruzados de la base:**\n\n"
                "$$\\vec{i} \\times \\vec{j} = \\vec{k}, \\quad \\vec{j} \\times \\vec{k} = \\vec{i}, \\quad \\vec{k} \\times \\vec{i} = \\vec{j}$$\n\n"
                "(Cíclico. Invertir el orden cambia el signo.)"
            ),
        ),

        b("teorema",
          nombre="Interpretación geométrica del producto cruz",
          enunciado_md=(
              "Sea $\\theta$ el ángulo entre $\\vec{u}$ y $\\vec{v}$. Entonces:\n\n"
              "**1. Magnitud:** $\\|\\vec{u} \\times \\vec{v}\\| = \\|\\vec{u}\\|\\|\\vec{v}\\|\\sin\\theta$.\n\n"
              "**2. Dirección:** $\\vec{u} \\times \\vec{v}$ es **perpendicular** tanto a $\\vec{u}$ como a $\\vec{v}$, con el sentido dado por la **regla de la mano derecha**.\n\n"
              "**Consecuencia geométrica:** $\\|\\vec{u}\\times\\vec{v}\\|$ es el **área del paralelogramo** generado por $\\vec{u}$ y $\\vec{v}$."
          ),
          demostracion_md=(
              "**Magnitud:** verificable por cuenta directa, $\\|\\vec{u}\\times\\vec{v}\\|^2 + (\\vec{u}\\cdot\\vec{v})^2 = \\|\\vec{u}\\|^2\\|\\vec{v}\\|^2$ (identidad de Lagrange). Como $\\vec{u}\\cdot\\vec{v} = \\|\\vec{u}\\|\\|\\vec{v}\\|\\cos\\theta$, queda $\\|\\vec{u}\\times\\vec{v}\\|^2 = \\|\\vec{u}\\|^2\\|\\vec{v}\\|^2(1 - \\cos^2\\theta) = \\|\\vec{u}\\|^2\\|\\vec{v}\\|^2\\sin^2\\theta$.\n\n"
              "**Perpendicularidad:** $(\\vec{u}\\times\\vec{v}) \\cdot \\vec{u} = 0$ y $(\\vec{u}\\times\\vec{v}) \\cdot \\vec{v} = 0$ por cuenta directa con el determinante (filas iguales → determinante cero)."
          )),

        fig(
            "Producto cruz e interpretación geométrica. Vista 3D isométrica de dos vectores u (en "
            "color teal) y v (en color azul oscuro) saliendo del origen, formando un paralelogramo "
            "(plano sombreado en ámbar translúcido). El área del paralelogramo etiquetada 'A = "
            "||u × v||'. Una flecha vertical adicional saliendo del origen perpendicularmente al "
            "paralelogramo, etiquetada 'u × v'. Pequeña ilustración a un lado de una mano derecha "
            "con los dedos doblándose desde u hacia v y el pulgar apuntando en la dirección de u × "
            "v, ilustrando la regla de la mano derecha. Etiquetas: 'u', 'v', 'u × v', 'A = "
            "||u × v||'. " + STYLE
        ),

        b("intuicion",
          titulo="Regla de la mano derecha",
          body_md=(
              "Para encontrar la **dirección** de $\\vec{u} \\times \\vec{v}$:\n\n"
              "1. Apunta los dedos de la mano derecha en la dirección de $\\vec{u}$.\n"
              "2. **Curva los dedos** hacia $\\vec{v}$ (por el ángulo más corto).\n"
              "3. El **pulgar** apunta en la dirección de $\\vec{u} \\times \\vec{v}$.\n\n"
              "**Consecuencia visible:** $\\vec{v} \\times \\vec{u}$ apunta al lado opuesto (anticonmutatividad).\n\n"
              "**Casos típicos:**\n\n"
              "- $\\vec{i} \\times \\vec{j} = \\vec{k}$: del eje $x$ al eje $y$ → eje $z$ positivo.\n"
              "- $\\vec{j} \\times \\vec{i} = -\\vec{k}$: del eje $y$ al eje $x$ → eje $z$ negativo."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular un producto cruz",
          problema_md="Calcular $\\vec{u} \\times \\vec{v}$ para $\\vec{u} = \\langle 1, 2, 3 \\rangle$ y $\\vec{v} = \\langle 4, 5, 6 \\rangle$.",
          pasos=[
              {"accion_md": "**Determinante:**\n\n"
                            "$$\\vec{u} \\times \\vec{v} = \\begin{vmatrix} \\vec{i} & \\vec{j} & \\vec{k} \\\\ 1 & 2 & 3 \\\\ 4 & 5 & 6 \\end{vmatrix}$$",
               "justificacion_md": "Disposición estándar: la primera fila son los versores, las otras dos los componentes.",
               "es_resultado": False},
              {"accion_md": "**Componente $\\vec{i}$:** $\\begin{vmatrix} 2 & 3 \\\\ 5 & 6 \\end{vmatrix} = 2(6) - 3(5) = -3$.\n\n"
                            "**Componente $\\vec{j}$ (con signo $-$):** $-\\begin{vmatrix} 1 & 3 \\\\ 4 & 6 \\end{vmatrix} = -(1(6) - 3(4)) = -(-6) = 6$.\n\n"
                            "**Componente $\\vec{k}$:** $\\begin{vmatrix} 1 & 2 \\\\ 4 & 5 \\end{vmatrix} = 1(5) - 2(4) = -3$.",
               "justificacion_md": "Expansión por la primera fila — atención al signo del término $\\vec{j}$ (alterna).",
               "es_resultado": False},
              {"accion_md": "$$\\vec{u} \\times \\vec{v} = \\langle -3, 6, -3 \\rangle$$\n\n"
                            "**Verificación:** $(\\vec{u}\\times\\vec{v}) \\cdot \\vec{u} = -3(1) + 6(2) + (-3)(3) = -3 + 12 - 9 = 0$. ✓ Perpendicular a $\\vec{u}$.",
               "justificacion_md": "Verificar siempre la perpendicularidad — atrapa errores de cálculo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Área de un paralelogramo",
          problema_md=(
              "Calcular el área del paralelogramo determinado por los vectores $\\vec{u} = \\langle 1, 0, 1 \\rangle$ y $\\vec{v} = \\langle 0, 1, 1 \\rangle$."
          ),
          pasos=[
              {"accion_md": "**Producto cruz:**\n\n"
                            "$\\vec{u} \\times \\vec{v} = \\langle (0)(1) - (1)(1), -[(1)(1) - (1)(0)], (1)(1) - (0)(0) \\rangle = \\langle -1, -1, 1 \\rangle$.",
               "justificacion_md": "Aplicar la fórmula con cuidado en el signo de $\\vec{j}$.",
               "es_resultado": False},
              {"accion_md": "**Magnitud:** $\\|\\langle -1, -1, 1 \\rangle\\| = \\sqrt{1+1+1} = \\sqrt{3}$.",
               "justificacion_md": "Es el área del paralelogramo.",
               "es_resultado": False},
              {"accion_md": "$$A = \\sqrt{3}$$",
               "justificacion_md": "**Para el área del triángulo** formado por estos vectores: $A_{\\triangle} = \\sqrt{3}/2$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Producto triple escalar y volumen",
          body_md=(
              "El **producto triple escalar** $\\vec{u} \\cdot (\\vec{v} \\times \\vec{w})$ es un escalar y se calcula como un determinante:\n\n"
              "$$\\vec{u} \\cdot (\\vec{v} \\times \\vec{w}) = \\begin{vmatrix} u_1 & u_2 & u_3 \\\\ v_1 & v_2 & v_3 \\\\ w_1 & w_2 & w_3 \\end{vmatrix}$$\n\n"
              "**Interpretación geométrica:** $|\\vec{u} \\cdot (\\vec{v} \\times \\vec{w})|$ es el **volumen del paralelepípedo** generado por $\\vec{u}, \\vec{v}, \\vec{w}$.\n\n"
              "**Caso especial:** si los tres vectores son **coplanares** (caen en un mismo plano), el producto triple es $0$. Es un test rápido de coplanaridad."
          )),

        b("ejemplo_resuelto",
          titulo="Volumen de un paralelepípedo",
          problema_md=(
              "Calcular el volumen del paralelepípedo formado por $\\vec{u} = \\langle 1, 0, 0 \\rangle$, $\\vec{v} = \\langle 1, 1, 0 \\rangle$ y $\\vec{w} = \\langle 1, 1, 1 \\rangle$."
          ),
          pasos=[
              {"accion_md": "**Determinante triple:**\n\n"
                            "$\\vec{u} \\cdot (\\vec{v}\\times\\vec{w}) = \\begin{vmatrix} 1 & 0 & 0 \\\\ 1 & 1 & 0 \\\\ 1 & 1 & 1 \\end{vmatrix} = 1 \\cdot (1 \\cdot 1 - 0 \\cdot 1) = 1$.",
               "justificacion_md": "Expansión por la primera fila.",
               "es_resultado": False},
              {"accion_md": "**Volumen:** $|1| = 1$.",
               "justificacion_md": "**Comprobación:** los tres vectores son los \"escalones\" sucesivos del cubo unitario, así forman un paralelepípedo de volumen $1$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\vec{i} \\times \\vec{k} = ?$",
                  "opciones_md": ["$\\vec{j}$", "$-\\vec{j}$", "$\\vec{i}$", "$\\vec{0}$"],
                  "correcta": "B",
                  "pista_md": "El ciclo positivo es $\\vec{i} \\to \\vec{j} \\to \\vec{k} \\to \\vec{i}$. $\\vec{i} \\times \\vec{k}$ va al **revés**.",
                  "explicacion_md": (
                      "$\\vec{k} \\times \\vec{i} = \\vec{j}$ (ciclo positivo). Por anticonmutatividad: $\\vec{i} \\times \\vec{k} = -(\\vec{k}\\times\\vec{i}) = -\\vec{j}$."
                  ),
              },
              {
                  "enunciado_md": "Si $\\vec{u}$ y $\\vec{v}$ son paralelos (no nulos), entonces $\\vec{u} \\times \\vec{v} = ?$",
                  "opciones_md": [
                      "$\\|\\vec{u}\\|\\|\\vec{v}\\|$",
                      "$\\vec{0}$",
                      "Un vector unitario",
                      "$\\vec{u}\\cdot\\vec{v}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Si son paralelos, $\\theta = 0$ o $\\pi$. ¿Cuánto vale $\\sin\\theta$?",
                  "explicacion_md": (
                      "$\\sin 0 = \\sin\\pi = 0$, así $\\|\\vec{u}\\times\\vec{v}\\| = \\|\\vec{u}\\|\\|\\vec{v}\\|\\sin\\theta = 0$. **El producto cruz de paralelos es $\\vec{0}$.** Es la diferencia clave con el producto punto (que da algo no nulo en este caso)."
                  ),
              },
          ]),

        ej(
            titulo="Vector perpendicular",
            enunciado=(
                "Encuentra un vector unitario perpendicular tanto a $\\vec{u} = \\langle 1, 1, 0 \\rangle$ como a $\\vec{v} = \\langle 0, 1, 1 \\rangle$."
            ),
            pistas=[
                "$\\vec{u} \\times \\vec{v}$ es perpendicular a ambos.",
                "Después normaliza dividiendo por su magnitud.",
            ],
            solucion=(
                "$\\vec{u} \\times \\vec{v} = \\langle 1\\cdot1 - 0\\cdot1, -(1\\cdot1 - 0\\cdot0), 1\\cdot1 - 1\\cdot0 \\rangle = \\langle 1, -1, 1 \\rangle$.\n\n"
                "Magnitud: $\\sqrt{3}$. Unitario: $\\dfrac{1}{\\sqrt{3}}\\langle 1, -1, 1 \\rangle$."
            ),
        ),

        ej(
            titulo="Área de un triángulo",
            enunciado=(
                "Calcula el área del triángulo con vértices $A = (1, 0, 0)$, $B = (0, 2, 0)$, $C = (0, 0, 3)$."
            ),
            pistas=[
                "Forma dos vectores desde un vértice: $\\vec{AB}$ y $\\vec{AC}$.",
                "Área del triángulo = $\\dfrac{1}{2}\\|\\vec{AB} \\times \\vec{AC}\\|$.",
            ],
            solucion=(
                "$\\vec{AB} = \\langle -1, 2, 0 \\rangle$, $\\vec{AC} = \\langle -1, 0, 3 \\rangle$.\n\n"
                "$\\vec{AB} \\times \\vec{AC} = \\langle 2\\cdot 3 - 0\\cdot 0, -((-1)\\cdot 3 - 0\\cdot(-1)), (-1)\\cdot 0 - 2\\cdot(-1) \\rangle = \\langle 6, 3, 2 \\rangle$.\n\n"
                "$\\|\\langle 6, 3, 2\\rangle\\| = \\sqrt{36+9+4} = 7$. **Área del triángulo:** $7/2$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el signo $-$** del término medio en el determinante (componente $\\vec{j}$).",
              "**Aplicar producto cruz en $\\mathbb{R}^2$.** No está definido — solo en 3D.",
              "**Confundir producto cruz con producto punto.** El primero da un vector; el segundo, un escalar.",
              "**Usar la mano izquierda** o invertir el orden — la regla es de la **mano derecha**, y $\\vec{v}\\times\\vec{u}$ apunta al lado opuesto.",
              "**Aplicar 'asociatividad'** $(\\vec{u}\\times\\vec{v})\\times\\vec{w} = \\vec{u}\\times(\\vec{v}\\times\\vec{w})$. **Falso en general** — el producto cruz no es asociativo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Producto cruz** $\\vec{u}\\times\\vec{v}$ (solo en $\\mathbb{R}^3$): vector con la fórmula del determinante.",
              "**Magnitud:** $\\|\\vec{u}\\times\\vec{v}\\| = \\|\\vec{u}\\|\\|\\vec{v}\\|\\sin\\theta$ — **área del paralelogramo**.",
              "**Dirección:** perpendicular a $\\vec{u}, \\vec{v}$, sentido por la regla de la mano derecha.",
              "**Anticonmutatividad:** $\\vec{u}\\times\\vec{v} = -(\\vec{v}\\times\\vec{u})$.",
              "**Triple escalar** $\\vec{u}\\cdot(\\vec{v}\\times\\vec{w})$: volumen del paralelepípedo (con signo).",
              "**Aplicaciones:** vector perpendicular, área, volumen, momento angular.",
              "**Próxima lección:** rectas y planos en $\\mathbb{R}^3$ — donde productos punto y cruz se usan en conjunto.",
          ]),
    ]
    return {
        "id": "lec-mvar-2-3-producto-cruz",
        "title": "Producto cruz",
        "description": "Producto vectorial en $\\mathbb{R}^3$, regla de la mano derecha, áreas y volúmenes.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 2.4 Rectas y planos
# =====================================================================
def lesson_2_4():
    blocks = [
        b("texto", body_md=(
            "En el plano $\\mathbb{R}^2$, una recta se describe con $y = mx + b$. En $\\mathbb{R}^3$ las cosas son distintas: "
            "**una sola ecuación de tres variables describe un plano**, no una recta. Para una recta hacen "
            "falta dos ecuaciones (o, mejor, una **ecuación vectorial**).\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Describir **rectas** con ecuación vectorial, paramétricas y simétricas.\n"
            "- Describir **planos** con la ecuación punto-normal y la forma estándar.\n"
            "- Calcular **distancias** punto-recta y punto-plano.\n"
            "- Resolver **intersecciones** entre rectas y planos."
        )),

        b("definicion",
          titulo="Recta en $\\mathbb{R}^3$",
          body_md=(
              "Una recta queda determinada por un **punto** $P_0 = (x_0, y_0, z_0)$ y un **vector dirección** $\\vec{v} = \\langle a, b, c \\rangle$.\n\n"
              "**Ecuación vectorial:**\n\n"
              "$$\\vec{r}(t) = \\vec{r}_0 + t \\vec{v}, \\quad t \\in \\mathbb{R}$$\n\n"
              "donde $\\vec{r}_0 = \\langle x_0, y_0, z_0 \\rangle$ es el vector posición de $P_0$.\n\n"
              "**Ecuaciones paramétricas** (componente a componente):\n\n"
              "$$x = x_0 + at, \\quad y = y_0 + bt, \\quad z = z_0 + ct$$\n\n"
              "**Ecuaciones simétricas** (despejar $t$ de cada paramétrica e igualar; requiere $a, b, c$ no nulos):\n\n"
              "$$\\dfrac{x - x_0}{a} = \\dfrac{y - y_0}{b} = \\dfrac{z - z_0}{c}$$"
          )),

        fig(
            "Recta en el espacio 3D. Ejes x, y, z. Un punto P₀ = (1, 2, 3) marcado en el espacio "
            "como un punto sólido. Un vector dirección v = ⟨2, 1, -1⟩ saliendo de P₀ en color teal. "
            "La recta extendida en ambas direcciones desde P₀ siguiendo la dirección de v, dibujada "
            "como línea continua color azul oscuro. Marcar otros dos puntos sobre la recta con "
            "etiquetas como 't = 1' y 't = -1' para mostrar la parametrización. Etiquetas: 'P₀', "
            "'v' (dirección), 'r(t) = r₀ + t·v'. Vista isométrica clara. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Recta por dos puntos",
          problema_md="Hallar la recta que pasa por $A = (1, 2, 3)$ y $B = (4, -1, 5)$.",
          pasos=[
              {"accion_md": "**Vector dirección:** $\\vec{v} = \\vec{AB} = \\langle 3, -3, 2 \\rangle$.",
               "justificacion_md": "Cualquier vector paralelo a la recta sirve como dirección.",
               "es_resultado": False},
              {"accion_md": "**Vectorial:** $\\vec{r}(t) = \\langle 1, 2, 3 \\rangle + t \\langle 3, -3, 2 \\rangle$.\n\n"
                            "**Paramétricas:** $x = 1 + 3t, \\; y = 2 - 3t, \\; z = 3 + 2t$.\n\n"
                            "**Simétricas:** $\\dfrac{x - 1}{3} = \\dfrac{y - 2}{-3} = \\dfrac{z - 3}{2}$.",
               "justificacion_md": "Tres formas equivalentes de la misma recta. **Verificación:** en $t = 0$ se obtiene $A$; en $t = 1$ se obtiene $B$. ✓",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Plano en $\\mathbb{R}^3$",
          body_md=(
              "Un plano queda determinado por un **punto** $P_0 = (x_0, y_0, z_0)$ y un **vector normal** "
              "$\\vec{n} = \\langle a, b, c \\rangle$ (perpendicular al plano).\n\n"
              "**Ecuación punto-normal:**\n\n"
              "$$\\vec{n} \\cdot (\\vec{r} - \\vec{r}_0) = 0$$\n\n"
              "Es decir, todo vector $\\vec{r} - \\vec{r}_0$ contenido en el plano debe ser perpendicular a la normal.\n\n"
              "**Forma estándar (cartesiana):** expandiendo:\n\n"
              "$$a(x - x_0) + b(y - y_0) + c(z - z_0) = 0$$\n\n"
              "$$ax + by + cz = d \\quad \\text{con } d = a x_0 + b y_0 + c z_0$$"
          )),

        fig(
            "Plano en el espacio 3D. Ejes x, y, z. Un plano inclinado representado como un "
            "paralelogramo translúcido en color teal claro. Un punto P₀ marcado sobre el plano. Un "
            "vector normal n perpendicular al plano saliendo desde P₀ en color ámbar grueso. Un "
            "punto adicional P sobre el plano y el vector r - r₀ desde P₀ hacia P, dibujado en el "
            "plano. Etiquetas: 'plano', 'P₀', 'n' (vector normal), 'r - r₀' (vector dentro del "
            "plano), 'n · (r - r₀) = 0'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Plano por tres puntos",
          problema_md="Hallar la ecuación del plano que pasa por $A = (1, 0, 0)$, $B = (0, 2, 0)$ y $C = (0, 0, 3)$.",
          pasos=[
              {"accion_md": "**Dos vectores en el plano:** $\\vec{AB} = \\langle -1, 2, 0 \\rangle$, $\\vec{AC} = \\langle -1, 0, 3 \\rangle$.",
               "justificacion_md": "Cualquier par de vectores no paralelos del plano sirven.",
               "es_resultado": False},
              {"accion_md": "**Vector normal por producto cruz:**\n\n"
                            "$\\vec{n} = \\vec{AB} \\times \\vec{AC} = \\langle 2\\cdot 3 - 0, -((-1)(3) - 0), 0 - 2(-1) \\rangle = \\langle 6, 3, 2 \\rangle$.",
               "justificacion_md": "**Truco fundamental:** el producto cruz de dos vectores del plano da la normal.",
               "es_resultado": False},
              {"accion_md": "**Ecuación** usando $A$ como punto:\n\n"
                            "$6(x - 1) + 3(y - 0) + 2(z - 0) = 0 \\implies 6x + 3y + 2z = 6$.",
               "justificacion_md": "**Verificación:** sustituir $B$: $0 + 6 + 0 = 6$ ✓; $C$: $0 + 0 + 6 = 6$ ✓.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Distancias",
          body_md=(
              "**Distancia de un punto $P$ a un plano** $ax + by + cz = d$ (con normal $\\vec{n} = \\langle a, b, c \\rangle$):\n\n"
              "$$D = \\dfrac{|a x_P + b y_P + c z_P - d|}{\\sqrt{a^2 + b^2 + c^2}} = \\dfrac{|\\vec{n} \\cdot \\vec{P_0 P}|}{\\|\\vec{n}\\|}$$\n\n"
              "donde $P_0$ es cualquier punto del plano. Equivale a la **componente** de $\\vec{P_0 P}$ en la dirección de $\\vec{n}$.\n\n"
              "**Distancia de un punto $P$ a una recta** $\\vec{r}(t) = \\vec{r}_0 + t \\vec{v}$:\n\n"
              "$$D = \\dfrac{\\|\\vec{P_0 P} \\times \\vec{v}\\|}{\\|\\vec{v}\\|}$$\n\n"
              "Sale de la fórmula del paralelogramo: el área $\\|\\vec{P_0 P}\\times\\vec{v}\\|$ dividida por la base $\\|\\vec{v}\\|$ da la altura."
          )),

        b("ejemplo_resuelto",
          titulo="Distancia punto-plano",
          problema_md="Calcular la distancia de $P = (2, 3, -1)$ al plano $2x - y + 2z = 5$.",
          pasos=[
              {"accion_md": "**Aplicación directa de la fórmula:**\n\n"
                            "$D = \\dfrac{|2(2) - 3 + 2(-1) - 5|}{\\sqrt{4 + 1 + 4}} = \\dfrac{|4 - 3 - 2 - 5|}{3} = \\dfrac{|-6|}{3} = 2$.",
               "justificacion_md": "Numerador: evaluar el lado izquierdo de la ecuación menos $d$, en valor absoluto. Denominador: norma de la normal.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Intersección recta-plano",
          body_md=(
              "Para hallar dónde una recta corta a un plano:\n\n"
              "1. Tomar las **paramétricas** de la recta: $x(t), y(t), z(t)$.\n"
              "2. Sustituir en la ecuación del plano.\n"
              "3. Resolver para $t$.\n"
              "4. Sustituir el $t$ obtenido en las paramétricas para tener el punto.\n\n"
              "**Casos especiales:**\n\n"
              "- Si al sustituir queda algo como $0 = 5$: no hay solución → la recta es **paralela al plano** y no lo toca.\n"
              "- Si queda $0 = 0$: la recta está **contenida** en el plano (todo $t$ funciona)."
          )),

        b("ejemplo_resuelto",
          titulo="Intersección recta-plano",
          problema_md="Hallar la intersección de la recta $\\vec{r}(t) = \\langle 1+2t, -t, 3+t \\rangle$ con el plano $x + y + z = 4$.",
          pasos=[
              {"accion_md": "**Sustituir** las paramétricas en la ecuación del plano:\n\n"
                            "$(1 + 2t) + (-t) + (3 + t) = 4 \\implies 4 + 2t = 4 \\implies t = 0$.",
               "justificacion_md": "Resolución algebraica para $t$.",
               "es_resultado": False},
              {"accion_md": "**Punto:** sustituir $t = 0$ en las paramétricas: $(1, 0, 3)$.",
               "justificacion_md": "**Verificación:** $1 + 0 + 3 = 4$. ✓",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El plano $2x + y - z = 0$ pasa por:",
                  "opciones_md": [
                      "$(0, 0, 1)$",
                      "$(1, 0, 0)$",
                      "$(0, 0, 0)$",
                      "$(1, 1, 1)$",
                  ],
                  "correcta": "C",
                  "pista_md": "Sustituye cada punto en la ecuación: ¿cuál cumple $2x + y - z = 0$?",
                  "explicacion_md": (
                      "$(0,0,0)$: $0 + 0 - 0 = 0$ ✓. $(1,0,0)$: $2 \\neq 0$. $(0,0,1)$: $-1 \\neq 0$. $(1,1,1)$: $2 + 1 - 1 = 2 \\neq 0$. **Solo el origen está en el plano** (que pasa por origen porque $d = 0$)."
                  ),
              },
              {
                  "enunciado_md": "Si dos planos tienen normales $\\vec{n}_1, \\vec{n}_2$ con $\\vec{n}_1 \\times \\vec{n}_2 = \\vec{0}$, los planos son:",
                  "opciones_md": [
                      "Perpendiculares",
                      "Idénticos",
                      "Paralelos (o idénticos)",
                      "No tienen relación",
                  ],
                  "correcta": "C",
                  "pista_md": "$\\vec{n}_1 \\times \\vec{n}_2 = 0$ significa que las normales son paralelas. ¿Qué implica eso para los planos?",
                  "explicacion_md": (
                      "Normales paralelas → planos paralelos (o coincidentes, si además comparten un punto). Para distinguir paralelos vs coincidentes, verificar un punto."
                  ),
              },
          ]),

        ej(
            titulo="Recta por intersección de dos planos",
            enunciado=(
                "Halla la dirección de la recta intersección de los planos $x + y + z = 1$ y $x - y + 2z = 2$."
            ),
            pistas=[
                "La recta intersección es perpendicular a las dos normales — usa el producto cruz.",
                "$\\vec{n}_1 = \\langle 1, 1, 1 \\rangle$, $\\vec{n}_2 = \\langle 1, -1, 2 \\rangle$.",
                "$\\vec{v} = \\vec{n}_1 \\times \\vec{n}_2$.",
            ],
            solucion=(
                "$\\vec{v} = \\vec{n}_1 \\times \\vec{n}_2 = \\langle 1\\cdot 2 - 1\\cdot(-1), -(1\\cdot 2 - 1\\cdot 1), 1\\cdot(-1) - 1\\cdot 1 \\rangle = \\langle 3, -1, -2 \\rangle$.\n\n"
                "**Dirección de la recta:** $\\langle 3, -1, -2 \\rangle$. Para tener la recta completa hay que encontrar también un punto en común — resolviendo el sistema con una variable libre, p. ej. $z = 0$ da $x + y = 1$ y $x - y = 2$, así $x = 3/2, y = -1/2$. Punto: $(3/2, -1/2, 0)$."
            ),
        ),

        ej(
            titulo="Distancia punto-recta",
            enunciado=(
                "Calcula la distancia del punto $P = (1, 2, 0)$ a la recta $\\vec{r}(t) = \\langle t, 0, t \\rangle$."
            ),
            pistas=[
                "Punto en la recta: $P_0 = (0, 0, 0)$ (con $t = 0$). Dirección $\\vec{v} = \\langle 1, 0, 1 \\rangle$.",
                "$\\vec{P_0 P} = \\langle 1, 2, 0 \\rangle$.",
                "$D = \\dfrac{\\|\\vec{P_0 P} \\times \\vec{v}\\|}{\\|\\vec{v}\\|}$.",
            ],
            solucion=(
                "$\\vec{P_0 P} \\times \\vec{v} = \\langle 1, 2, 0 \\rangle \\times \\langle 1, 0, 1 \\rangle = \\langle 2 - 0, -(1 - 0), 0 - 2 \\rangle = \\langle 2, -1, -2 \\rangle$.\n\n"
                "$\\|\\vec{P_0 P} \\times \\vec{v}\\| = \\sqrt{4 + 1 + 4} = 3$. $\\|\\vec{v}\\| = \\sqrt{2}$.\n\n"
                "$D = 3/\\sqrt{2} = 3\\sqrt{2}/2$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir vector dirección de recta con vector normal de plano.** Son roles distintos: la dirección **es paralela**, la normal **es perpendicular**.",
              "**Pensar que en $\\mathbb{R}^3$ una sola ecuación da una recta.** $ax + by + cz = d$ describe un plano. Una recta requiere dos ecuaciones (o una vectorial).",
              "**Olvidar el valor absoluto** en la fórmula de distancia punto-plano: el numerador es $|n \\cdot P_0 P|$, no $n \\cdot P_0 P$.",
              "**Pensar que rectas paralelas en $\\mathbb{R}^3$ siempre se cruzan.** En 3D pueden ser **alabeadas** (skew): no se cortan ni son paralelas.",
              "**Aplicar la fórmula simétrica cuando alguna componente de la dirección es $0$.** En ese caso, esa coordenada queda fija ($x = x_0$, por ejemplo) y solo se igualan las dos restantes.",
          ]),

        b("resumen",
          puntos_md=[
              "**Recta:** $\\vec{r}(t) = \\vec{r}_0 + t\\vec{v}$ (vectorial), paramétricas, simétricas.",
              "**Plano:** $\\vec{n}\\cdot(\\vec{r} - \\vec{r}_0) = 0$ (punto-normal), $ax+by+cz=d$ (estándar).",
              "**Plano por 3 puntos:** producto cruz de dos vectores en el plano da la normal.",
              "**Recta por 2 planos:** producto cruz de las dos normales da la dirección.",
              "**Distancia punto-plano:** $|ax_P + by_P + cz_P - d| / \\|\\vec{n}\\|$.",
              "**Distancia punto-recta:** $\\|\\vec{P_0 P}\\times\\vec{v}\\| / \\|\\vec{v}\\|$.",
              "**Próxima lección:** superficies cuádricas — los \"polinomios de grado 2\" en 3D.",
          ]),
    ]
    return {
        "id": "lec-mvar-2-4-rectas-planos",
        "title": "Rectas y planos",
        "description": "Rectas y planos en $\\mathbb{R}^3$: ecuaciones vectoriales, paramétricas, simétricas y estándar. Distancias e intersecciones.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 4,
    }


# =====================================================================
# 2.5 Superficies cuádricas
# =====================================================================
def lesson_2_5():
    blocks = [
        b("texto", body_md=(
            "Las **superficies cuádricas** son las superficies en $\\mathbb{R}^3$ definidas por ecuaciones de "
            "**segundo grado** en $x, y, z$. Son la generalización 3D de las cónicas (elipses, parábolas, "
            "hipérbolas) y aparecen constantemente en aplicaciones: antenas parabólicas, lentes, "
            "trayectorias de planetas, etc.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Reconocer las **seis familias** principales de cuádricas.\n"
            "- Identificar una superficie por su ecuación.\n"
            "- Usar **trazas** (cortes con planos coordenados) para visualizarlas."
        )),

        b("definicion",
          titulo="Forma general",
          body_md=(
              "Una **cuádrica** es una superficie definida por:\n\n"
              "$$Ax^2 + By^2 + Cz^2 + Dxy + Exz + Fyz + Gx + Hy + Iz + J = 0$$\n\n"
              "(con al menos uno de los seis coeficientes cuadráticos $A, B, C, D, E, F$ no nulo).\n\n"
              "**Mediante traslación y rotación**, toda cuádrica no degenerada se reduce a una de las "
              "**seis formas canónicas** (ecuaciones \"limpias\" centradas en el origen y alineadas con los ejes)."
          )),

        b("definicion",
          titulo="Trazas — cómo visualizar una cuádrica",
          body_md=(
              "Las **trazas** son las curvas obtenidas al cortar la superficie con planos paralelos a los planos coordenados:\n\n"
              "- **Traza horizontal** ($z = k$): qué se ve mirando desde arriba a altura $k$.\n"
              "- **Traza frontal** ($y = k$): vista lateral.\n"
              "- **Traza lateral** ($x = k$): vista de costado.\n\n"
              "**Estrategia para identificar una cuádrica:**\n\n"
              "1. Sustituir $z = k$ en la ecuación → curva en $xy$.\n"
              "2. Repetir con $y = k$ y $x = k$.\n"
              "3. Las trazas son cónicas (elipses, hipérbolas, parábolas, rectas, puntos).\n"
              "4. La combinación identifica la familia."
          )),

        formulas(
            titulo="Las seis cuádricas canónicas",
            body=(
                "**1. Elipsoide:**\n\n"
                "$$\\dfrac{x^2}{a^2} + \\dfrac{y^2}{b^2} + \\dfrac{z^2}{c^2} = 1$$\n\n"
                "Trazas: elipses en los tres planos. Si $a = b = c$: esfera.\n\n"
                "**2. Paraboloide elíptico** (\"cuenco\"):\n\n"
                "$$\\dfrac{z}{c} = \\dfrac{x^2}{a^2} + \\dfrac{y^2}{b^2}$$\n\n"
                "Trazas horizontales: elipses (a alturas positivas si $c > 0$). Verticales: parábolas.\n\n"
                "**3. Paraboloide hiperbólico** (\"silla de montar\"):\n\n"
                "$$\\dfrac{z}{c} = \\dfrac{x^2}{a^2} - \\dfrac{y^2}{b^2}$$\n\n"
                "Trazas horizontales: hipérbolas. Verticales: parábolas (una hacia arriba, otra hacia abajo).\n\n"
                "**4. Cono elíptico:**\n\n"
                "$$\\dfrac{x^2}{a^2} + \\dfrac{y^2}{b^2} = \\dfrac{z^2}{c^2}$$\n\n"
                "Pasa por el origen. Trazas horizontales: elipses (excepto $z = 0$ que es solo el origen). Verticales: dos rectas.\n\n"
                "**5. Hiperboloide de una hoja:**\n\n"
                "$$\\dfrac{x^2}{a^2} + \\dfrac{y^2}{b^2} - \\dfrac{z^2}{c^2} = 1$$\n\n"
                "Una sola pieza, con \"cintura\" en $z = 0$. Trazas horizontales: elipses; verticales: hipérbolas.\n\n"
                "**6. Hiperboloide de dos hojas:**\n\n"
                "$$-\\dfrac{x^2}{a^2} - \\dfrac{y^2}{b^2} + \\dfrac{z^2}{c^2} = 1$$\n\n"
                "Dos piezas separadas (en $z \\geq c$ y $z \\leq -c$). Trazas horizontales (para $|z| \\geq c$): elipses; verticales: hipérbolas."
            ),
        ),

        fig(
            "Galería de seis superficies cuádricas en una grilla 2x3, vista isométrica 3D para cada "
            "una. ARRIBA-IZQ: elipsoide (forma de huevo, con tres semiejes distintos a, b, c). "
            "ARRIBA-CENTRO: paraboloide elíptico (cuenco abriendo hacia arriba). ARRIBA-DER: "
            "paraboloide hiperbólico (silla de montar, con curvatura opuesta en cada dirección). "
            "ABAJO-IZQ: cono elíptico (dos conos unidos en el vértice, uno arriba y otro abajo). "
            "ABAJO-CENTRO: hiperboloide de una hoja (forma de torre con cintura, semejante a una "
            "torre de enfriamiento de central). ABAJO-DER: hiperboloide de dos hojas (dos cuencos "
            "separados, uno arriba y otro abajo del eje xy). Cada una con su nombre debajo. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Identificar una cuádrica",
          problema_md="Identificar y describir la superficie $4x^2 + y^2 + 4z^2 = 16$.",
          pasos=[
              {"accion_md": "**Dividir entre 16** para tener forma canónica:\n\n"
                            "$\\dfrac{x^2}{4} + \\dfrac{y^2}{16} + \\dfrac{z^2}{4} = 1$.",
               "justificacion_md": "Forma estándar de elipsoide.",
               "es_resultado": False},
              {"accion_md": "**Es un elipsoide** centrado en el origen, con semiejes $a = 2$ (en $x$), $b = 4$ (en $y$), $c = 2$ (en $z$).",
               "justificacion_md": "Como $a = c \\neq b$, es un elipsoide de revolución (alargado en la dirección $y$).",
               "es_resultado": False},
              {"accion_md": "**Trazas:**\n\n"
                            "- $z = 0$: $\\dfrac{x^2}{4} + \\dfrac{y^2}{16} = 1$ — elipse en el plano $xy$.\n"
                            "- $x = 0$: $\\dfrac{y^2}{16} + \\dfrac{z^2}{4} = 1$ — elipse en el plano $yz$.\n"
                            "- $y = 0$: $\\dfrac{x^2}{4} + \\dfrac{z^2}{4} = 1 \\implies x^2 + z^2 = 4$ — círculo de radio $2$ en el plano $xz$.",
               "justificacion_md": "Las trazas confirman la forma elipsoidal.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Distinguir paraboloide vs hiperboloide",
          problema_md="Identificar $z = x^2 - y^2$.",
          pasos=[
              {"accion_md": "**Forma:** $z/1 = x^2/1 - y^2/1$. Es la forma del **paraboloide hiperbólico** (silla de montar).",
               "justificacion_md": "Coeficientes $a = b = c = 1$.",
               "es_resultado": False},
              {"accion_md": "**Trazas:**\n\n"
                            "- $z = 0$: $x^2 - y^2 = 0 \\iff y = \\pm x$ — dos rectas (degenerada).\n"
                            "- $z = k > 0$: $x^2 - y^2 = k$ — hipérbola que se abre hacia el eje $x$.\n"
                            "- $z = k < 0$: $x^2 - y^2 = k$ — hipérbola que se abre hacia el eje $y$.\n"
                            "- $y = 0$: $z = x^2$ — parábola hacia arriba.\n"
                            "- $x = 0$: $z = -y^2$ — parábola hacia abajo.",
               "justificacion_md": "Las dos parábolas (una arriba, otra abajo) son la **firma** de la silla de montar.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Cómo distinguir las cuádricas en una mirada",
          body_md=(
              "**Pista por signos** de los términos cuadráticos (después de pasar todo a un lado):\n\n"
              "**Tres términos cuadráticos:**\n\n"
              "- Todos $+$ y constante $+$: **elipsoide**.\n"
              "- Dos $+$, uno $-$ y constante $+$: **hiperboloide de 1 hoja**.\n"
              "- Uno $+$, dos $-$ y constante $+$: **hiperboloide de 2 hojas**.\n"
              "- Tres $+$ (o tres $-$) y constante $0$: **cono** (degenera a un punto si todo es $+$).\n\n"
              "**Dos términos cuadráticos + uno lineal** (ej. $z = ...$):\n\n"
              "- Dos $+$: **paraboloide elíptico** (cuenco).\n"
              "- $+$ y $-$: **paraboloide hiperbólico** (silla)."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$x^2 + y^2 + z^2 = 25$ es:",
                  "opciones_md": ["Cono", "Esfera", "Paraboloide", "Hiperboloide"],
                  "correcta": "B",
                  "pista_md": "Los tres coeficientes son iguales y la suma es positiva — caso especial del elipsoide.",
                  "explicacion_md": (
                      "**Esfera** de radio $5$ centrada en el origen. Es el elipsoide con $a = b = c = 5$."
                  ),
              },
              {
                  "enunciado_md": "$z^2 = x^2 + y^2$ es:",
                  "opciones_md": [
                      "Cono",
                      "Cilindro",
                      "Paraboloide elíptico",
                      "Hiperboloide de 1 hoja",
                  ],
                  "correcta": "A",
                  "pista_md": "Trazas $z = k$: $x^2 + y^2 = k^2$ — círculo de radio $|k|$.",
                  "explicacion_md": (
                      "Es un **cono** (de eje $z$). En $z = 0$ es solo el origen; al subir o bajar, círculos cada vez más grandes proporcionalmente a $|z|$."
                  ),
              },
          ]),

        ej(
            titulo="Identificar y trazar",
            enunciado=(
                "Identifica la superficie $\\dfrac{x^2}{4} + \\dfrac{y^2}{9} - \\dfrac{z^2}{16} = 1$ "
                "y describe sus trazas."
            ),
            pistas=[
                "Tres términos cuadráticos: dos $+$, uno $-$, constante $+$.",
                "Aplica la pista por signos: ¿qué cuádrica es?",
            ],
            solucion=(
                "Dos $+$, uno $-$, constante $+1$ → **hiperboloide de una hoja** (eje a lo largo de $z$, donde aparece el signo $-$).\n\n"
                "**Trazas:**\n\n"
                "- $z = 0$ (cintura): $x^2/4 + y^2/9 = 1$ — elipse.\n"
                "- $z = k$: $x^2/4 + y^2/9 = 1 + k^2/16$ — elipses cada vez más grandes al alejarse de $z = 0$.\n"
                "- $x = 0$: $y^2/9 - z^2/16 = 1$ — hipérbola.\n"
                "- $y = 0$: $x^2/4 - z^2/16 = 1$ — hipérbola."
            ),
        ),

        ej(
            titulo="Identificar paraboloide",
            enunciado="Identifica la superficie $z + 1 = x^2 + y^2$.",
            pistas=[
                "Despeja $z = x^2 + y^2 - 1$. Reescribe.",
                "$z - (-1) = x^2 + y^2$ → ¿qué tipo y dónde está el vértice?",
            ],
            solucion=(
                "**Paraboloide elíptico** (de hecho de revolución, porque los coeficientes de $x^2$ y $y^2$ son iguales) con vértice en $(0, 0, -1)$, abriendo hacia arriba.\n\n"
                "Trazas $z = k$: $x^2 + y^2 = k + 1$. Vacío si $k < -1$. Punto si $k = -1$. Círculos crecientes si $k > -1$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**No reducir a forma canónica antes de identificar.** Dividir por la constante para tener $= 1$ o despejar $z$ a la izquierda.",
              "**Confundir paraboloide elíptico con hiperboloide de una hoja.** El primero tiene un término **lineal** ($z$ solo); el segundo, todos cuadráticos.",
              "**Confundir hiperboloide de 1 hoja vs 2 hojas.** **1 hoja:** dos $+$, uno $-$, constante $+$. **2 hojas:** uno $+$, dos $-$, constante $+$. La pista del signo del **único** $\\pm$ distinto.",
              "**Confundir cono con hiperboloide.** Cono: constante $= 0$. Hiperboloides: constante $\\neq 0$.",
              "**Olvidar que un elipsoide con $a = b = c$ es esfera.** Es el caso especial más común.",
          ]),

        b("resumen",
          puntos_md=[
              "**Seis familias canónicas:** elipsoide, paraboloide elíptico, paraboloide hiperbólico (silla), cono, hiperboloide de 1 hoja, hiperboloide de 2 hojas.",
              "**Pista rápida por signos** de los términos cuadráticos y la constante.",
              "**Trazas** (cortes con $x = k, y = k, z = k$) revelan la geometría — se obtienen cónicas conocidas.",
              "**Caso degenerado:** elipsoide con $a = b = c$ → esfera. Cono con dos coeficientes iguales → cono circular.",
              "**Cierre del capítulo:** vectores + planos + cuádricas = el lenguaje geométrico para todo lo que viene (funciones de varias variables, derivadas parciales, integrales múltiples).",
          ]),
    ]
    return {
        "id": "lec-mvar-2-5-cuadricas",
        "title": "Superficies cuádricas",
        "description": "Las seis familias canónicas: elipsoide, paraboloides, cono, hiperboloides. Identificación por trazas.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "calculo-multivariable"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Curso {course_id} no existe. Corre primero seed_calculo_multivariable_chapter_1.py")

    chapter_id = "ch-espacio"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Espacio",
        "description": "Vectores en $\\mathbb{R}^3$, productos punto y cruz, rectas y planos, superficies cuádricas.",
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
    print(f"✅ Capítulo 2 — Espacio listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
