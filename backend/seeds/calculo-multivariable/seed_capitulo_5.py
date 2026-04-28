"""
Seed del curso Cálculo Multivariable — Capítulo 5: Aplicaciones de las Derivadas Parciales.
4 lecciones:
  5.1 Planos tangentes y aproximaciones lineales
  5.2 Derivadas direccionales (y gradiente)
  5.3 Valores máximos y mínimos
  5.4 Multiplicadores de Lagrange

Capítulo geométricamente rico. Incluye varias figuras.
Idempotente.
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
# 5.1 Planos tangentes y aproximaciones lineales
# =====================================================================
def lesson_5_1():
    blocks = [
        b("texto", body_md=(
            "En la lección 4.3 introdujimos el plano tangente a $z = f(x, y)$. Aquí lo profundizamos y "
            "extendemos a **superficies dadas implícitamente** $F(x, y, z) = k$, donde el gradiente $\\nabla F$ "
            "juega el papel de **vector normal**. También formalizamos la **aproximación lineal** y el "
            "**diferencial** como herramientas de cálculo y propagación de errores.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Construir el **plano tangente** a una superficie dada explícita o implícitamente.\n"
            "- Reconocer al **gradiente** como vector normal a superficies de nivel.\n"
            "- Aplicar la **aproximación lineal** $L(x, y)$ para estimar valores y errores.\n"
            "- Manejar el **diferencial total** $df = f_x \\, dx + f_y \\, dy + f_z \\, dz$."
        )),

        b("definicion",
          titulo="Plano tangente a $z = f(x, y)$ (repaso)",
          body_md=(
              "Si $f$ es **diferenciable en $(a, b)$**, el plano tangente a $z = f(x, y)$ en $(a, b, f(a,b))$ es:\n\n"
              "$$z = f(a, b) + f_x(a, b)(x - a) + f_y(a, b)(y - b)$$\n\n"
              "**Reescribiéndolo en forma estándar de plano:**\n\n"
              "$$f_x (x-a) + f_y (y-b) - (z - f(a,b)) = 0$$\n\n"
              "**Vector normal:** $\\vec{n} = \\langle f_x, f_y, -1 \\rangle$."
          )),

        b("teorema",
          nombre="Plano tangente a una superficie de nivel",
          enunciado_md=(
              "Sea $S$ la superficie $F(x, y, z) = k$ y $P_0 = (a, b, c) \\in S$. Si $F$ es diferenciable y $\\nabla F(P_0) \\neq \\vec{0}$, entonces el **plano tangente** a $S$ en $P_0$ es:\n\n"
              "$$F_x(P_0)(x - a) + F_y(P_0)(y - b) + F_z(P_0)(z - c) = 0$$\n\n"
              "Es decir, **$\\nabla F(P_0) = \\langle F_x, F_y, F_z \\rangle$ es vector normal** a la superficie en $P_0$."
          ),
          demostracion_md=(
              "Sea $\\vec{r}(t)$ una curva cualquiera contenida en $S$ con $\\vec{r}(0) = P_0$. Como $F(\\vec{r}(t)) = k$ es constante, derivando con la regla de la cadena: $\\nabla F \\cdot \\vec{r}'(0) = 0$. "
              "Es decir, $\\nabla F$ es perpendicular a **toda** tangente a curvas en $S$ — perpendicular al plano tangente, así sirve como vector normal."
          )),

        fig(
            "Gradiente como vector normal a una superficie de nivel. Vista 3D isométrica de una "
            "superficie ondulada (ej: una esfera o un elipsoide) en color teal translúcido. Un punto "
            "P₀ marcado sobre la superficie. Un vector ∇F saliendo perpendicular a la superficie en "
            "P₀, en color ámbar grueso, con etiqueta 'gradiente ∇F = vector normal'. Plano tangente "
            "en P₀ dibujado como un pequeño cuadrado translúcido tocando la superficie en el punto, "
            "con etiqueta 'plano tangente'. Fondo blanco. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Plano tangente a una esfera",
          problema_md="Hallar el plano tangente a $x^2 + y^2 + z^2 = 14$ en $P_0 = (1, 2, 3)$.",
          pasos=[
              {"accion_md": "**Definir** $F(x, y, z) = x^2 + y^2 + z^2$. Verificar: $F(1, 2, 3) = 14$. ✓",
               "justificacion_md": "$P_0$ está en la superficie.",
               "es_resultado": False},
              {"accion_md": "**Gradiente:** $\\nabla F = \\langle 2x, 2y, 2z \\rangle$. **En $P_0$:** $\\nabla F(P_0) = \\langle 2, 4, 6 \\rangle$.",
               "justificacion_md": "El gradiente es el vector normal en cada punto.",
               "es_resultado": False},
              {"accion_md": "**Plano tangente:**\n\n"
                            "$2(x - 1) + 4(y - 2) + 6(z - 3) = 0 \\implies 2x + 4y + 6z = 28 \\iff x + 2y + 3z = 14$.",
               "justificacion_md": "**Comprobación geométrica:** $\\nabla F(1, 2, 3) = (2, 4, 6)$ es paralelo a $(1, 2, 3) = P_0$. **Esto es general en esferas centradas en el origen:** la normal en $P$ apunta en la dirección de $\\overrightarrow{OP}$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Plano tangente a un elipsoide",
          problema_md="Hallar el plano tangente a $\\dfrac{x^2}{4} + y^2 + \\dfrac{z^2}{9} = 3$ en $(2, 1, 3)$.",
          pasos=[
              {"accion_md": "**$F(x, y, z) = x^2/4 + y^2 + z^2/9$**. Verificar: $F(2, 1, 3) = 1 + 1 + 1 = 3$. ✓",
               "justificacion_md": "Punto en la superficie.",
               "es_resultado": False},
              {"accion_md": "**Gradiente:** $\\nabla F = \\langle x/2, 2y, 2z/9 \\rangle$. **En $(2, 1, 3)$:** $\\nabla F = \\langle 1, 2, 2/3 \\rangle$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "**Plano:**\n\n"
                            "$1(x - 2) + 2(y - 1) + \\dfrac{2}{3}(z - 3) = 0$\n\n"
                            "Multiplicando por 3 para limpiar: $3(x - 2) + 6(y - 1) + 2(z - 3) = 0 \\implies 3x + 6y + 2z = 18$.",
               "justificacion_md": "Plano tangente en forma estándar.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Aproximación lineal (linealización)",
          body_md=(
              "La **linealización** de $f$ en $(a, b)$ es la función:\n\n"
              "$$L(x, y) = f(a, b) + f_x(a, b)(x - a) + f_y(a, b)(y - b)$$\n\n"
              "Es la función afín cuya gráfica es el plano tangente. Para $(x, y)$ cerca de $(a, b)$, $f(x, y) \\approx L(x, y)$.\n\n"
              "**Análogo en 3 variables:**\n\n"
              "$$L(x, y, z) = f(a,b,c) + f_x(x-a) + f_y(y-b) + f_z(z-c)$$"
          )),

        b("definicion",
          titulo="Diferencial total",
          body_md=(
              "El **diferencial** de $z = f(x, y)$ es:\n\n"
              "$$dz = f_x \\, dx + f_y \\, dy$$\n\n"
              "**Para 3 variables** ($w = f(x, y, z)$): $dw = f_x \\, dx + f_y \\, dy + f_z \\, dz$.\n\n"
              "Para incrementos pequeños $\\Delta x, \\Delta y, \\Delta z$:\n\n"
              "$$\\Delta w \\approx f_x \\Delta x + f_y \\Delta y + f_z \\Delta z$$\n\n"
              "**Aplicación principal:** estimación de errores propagados cuando varias variables tienen incertidumbre."
          )),

        b("ejemplo_resuelto",
          titulo="Estimación con linealización",
          problema_md=(
              "Aproximar $f(2.05, 2.97)$ donde $f(x, y) = \\sqrt{x^2 + y^2}$, usando linealización en $(2, 3)$."
          ),
          pasos=[
              {"accion_md": "**$f(2, 3) = \\sqrt{13}$**. **Parciales:** $f_x = x/\\sqrt{x^2+y^2}$, $f_y = y/\\sqrt{x^2+y^2}$.\n\n"
                            "**En $(2, 3)$:** $f_x = 2/\\sqrt{13}$, $f_y = 3/\\sqrt{13}$.",
               "justificacion_md": "Cálculo directo.",
               "es_resultado": False},
              {"accion_md": "**Linealización:**\n\n"
                            "$L(x, y) = \\sqrt{13} + \\dfrac{2}{\\sqrt{13}}(x - 2) + \\dfrac{3}{\\sqrt{13}}(y - 3)$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "**En $(2.05, 2.97)$:**\n\n"
                            "$L = \\sqrt{13} + \\dfrac{2}{\\sqrt{13}}(0.05) + \\dfrac{3}{\\sqrt{13}}(-0.03) = \\sqrt{13} + \\dfrac{0.1 - 0.09}{\\sqrt{13}} = \\sqrt{13} + \\dfrac{0.01}{\\sqrt{13}}$.\n\n"
                            "$\\sqrt{13} \\approx 3.6056$, así $L \\approx 3.6056 + 0.00277 \\approx 3.6083$.",
               "justificacion_md": "**Valor real:** $\\sqrt{2.05^2 + 2.97^2} = \\sqrt{4.2025 + 8.8209} = \\sqrt{13.0234} \\approx 3.6088$. **Error:** $\\approx 0.0005$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para una superficie $F(x,y,z) = k$, el vector normal en un punto $P_0$ es:",
                  "opciones_md": [
                      "$\\vec{r}_0$ (posición del punto)",
                      "$\\nabla F(P_0)$",
                      "$F(P_0)$",
                      "Cualquier vector tangente",
                  ],
                  "correcta": "B",
                  "pista_md": "El gradiente es perpendicular a las superficies de nivel.",
                  "explicacion_md": (
                      "$\\nabla F(P_0) = \\langle F_x, F_y, F_z \\rangle$ es perpendicular a la superficie de nivel $F = k$ en $P_0$. Es la base para construir el plano tangente."
                  ),
              },
              {
                  "enunciado_md": "$L(x, y)$ es una buena aproximación de $f(x, y)$ cerca de $(a, b)$ si:",
                  "opciones_md": [
                      "Existen las parciales en $(a, b)$.",
                      "$f$ es diferenciable en $(a, b)$.",
                      "$f$ es continua en $(a, b)$.",
                      "Siempre, sin condiciones.",
                  ],
                  "correcta": "B",
                  "pista_md": "Aproximación lineal exige más que existencia de parciales.",
                  "explicacion_md": (
                      "**Diferenciabilidad** es la condición correcta. Solo entonces $f - L = o(\\sqrt{(x-a)^2 + (y-b)^2})$ — el error es despreciable comparado con la distancia."
                  ),
              },
          ]),

        ej(
            titulo="Plano tangente con superficie implícita",
            enunciado=(
                "Halla el plano tangente a la superficie $xy^2 + yz^2 = 12$ en el punto $(2, 1, \\sqrt{10})$."
            ),
            pistas=[
                "$F(x, y, z) = xy^2 + yz^2$. Calcula $\\nabla F$.",
                "$F_x = y^2$, $F_y = 2xy + z^2$, $F_z = 2yz$.",
                "Evalúa en el punto y arma la ecuación.",
            ],
            solucion=(
                "$\\nabla F = \\langle y^2, 2xy + z^2, 2yz \\rangle$. **En $(2, 1, \\sqrt{10})$:** $\\nabla F = \\langle 1, 4 + 10, 2\\sqrt{10} \\rangle = \\langle 1, 14, 2\\sqrt{10} \\rangle$.\n\n"
                "**Plano:** $(x - 2) + 14(y - 1) + 2\\sqrt{10}(z - \\sqrt{10}) = 0$\n\n"
                "$\\implies x + 14y + 2\\sqrt{10}\\, z = 2 + 14 + 20 = 36$."
            ),
        ),

        ej(
            titulo="Propagación de error",
            enunciado=(
                "Dos resistencias en paralelo dan resistencia total $R$ con $\\dfrac{1}{R} = \\dfrac{1}{R_1} + \\dfrac{1}{R_2}$. "
                "Si $R_1 = 200 \\Omega$ y $R_2 = 300 \\Omega$ con error $\\pm 1\\%$ cada una, estima el error en $R$."
            ),
            pistas=[
                "Despeja $R = \\dfrac{R_1 R_2}{R_1 + R_2}$ y calcula $\\partial R/\\partial R_1$, $\\partial R/\\partial R_2$.",
                "Por simetría, $\\partial R/\\partial R_1 = R_2^2 / (R_1+R_2)^2$. Análogo para la otra.",
                "Aplica $|dR| \\leq |R_{R_1}| |dR_1| + |R_{R_2}| |dR_2|$.",
            ],
            solucion=(
                "$R = \\dfrac{200 \\cdot 300}{500} = 120$. **Parciales** en $(200, 300)$:\n\n"
                "$\\partial R/\\partial R_1 = \\dfrac{R_2^2}{(R_1+R_2)^2} = \\dfrac{90000}{250000} = 0.36$.\n\n"
                "$\\partial R/\\partial R_2 = \\dfrac{R_1^2}{(R_1+R_2)^2} = \\dfrac{40000}{250000} = 0.16$.\n\n"
                "**Errores:** $|dR_1| = 2 \\Omega$, $|dR_2| = 3 \\Omega$.\n\n"
                "$|dR| \\leq 0.36(2) + 0.16(3) = 0.72 + 0.48 = 1.2 \\Omega$. **Error relativo:** $1.2/120 = 1\\%$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir 'gradiente normal a la superficie' con 'gradiente tangente'.** $\\nabla F$ es **perpendicular** a la superficie de nivel.",
              "**Aplicar el plano tangente cuando $f$ no es diferenciable.** La fórmula da algo, pero no representa la geometría correctamente.",
              "**Calcular linealización con incrementos grandes.** El error crece cuadráticamente con la distancia al punto base.",
              "**Sumar errores con signo en lugar de en valor absoluto.** Para cota máxima del error: $|dR| \\leq \\sum |\\partial R/\\partial x_i| |dx_i|$.",
              "**Olvidar verificar que el punto está en la superficie** antes de calcular el plano tangente. $F(P_0) = k$ debe cumplirse.",
          ]),

        b("resumen",
          puntos_md=[
              "**Plano tangente a $z = f(x,y)$:** $z = f(a,b) + f_x(x-a) + f_y(y-b)$.",
              "**Plano tangente a $F(x,y,z) = k$:** $F_x(x-a) + F_y(y-b) + F_z(z-c) = 0$, con normal $\\nabla F$.",
              "**$\\nabla F$ es perpendicular a las superficies de nivel.**",
              "**Linealización:** $L(x, y) = f(a,b) + f_x(x-a) + f_y(y-b)$.",
              "**Diferencial total:** $dz = f_x \\, dx + f_y \\, dy$.",
              "**Aplicaciones:** estimación de valores cerca de un punto, propagación de errores en mediciones.",
              "**Próxima lección:** derivadas direccionales — derivar en cualquier dirección, no solo los ejes.",
          ]),
    ]
    return {
        "id": "lec-mvar-5-1-planos-tangentes",
        "title": "Planos tangentes y aproximaciones lineales",
        "description": "Plano tangente a superficies explícitas e implícitas, gradiente como vector normal, linealización y diferencial.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 5.2 Derivadas direccionales y gradiente
# =====================================================================
def lesson_5_2():
    blocks = [
        b("texto", body_md=(
            "Las derivadas parciales miden la tasa de cambio de $f$ en las **direcciones de los ejes**. "
            "¿Y si queremos saber cómo cambia $f$ en otra dirección — por ejemplo, $\\langle 1, 1 \\rangle / \\sqrt{2}$? "
            "Esa es la **derivada direccional**, y resulta tener una expresión elegante en términos del **gradiente**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y calcular $D_{\\vec{u}} f$ con $\\vec{u}$ unitario.\n"
            "- Reconocer al **gradiente** $\\nabla f$ como el vector que codifica todas las direccionales.\n"
            "- Aplicar las **propiedades geométricas** del gradiente: dirección de máximo crecimiento, perpendicular a curvas de nivel.\n"
            "- Manejar versiones $f(x, y, z)$."
        )),

        b("definicion",
          titulo="Derivada direccional",
          body_md=(
              "Sea $f$ función de varias variables y $\\vec{u}$ un **vector unitario** ($\\|\\vec{u}\\| = 1$). La **derivada direccional** de $f$ en $(a, b)$ en la dirección $\\vec{u}$ es:\n\n"
              "$$D_{\\vec{u}} f(a, b) = \\lim_{h \\to 0} \\dfrac{f((a, b) + h \\vec{u}) - f(a, b)}{h}$$\n\n"
              "**Casos especiales:**\n\n"
              "- $\\vec{u} = \\vec{i} = \\langle 1, 0 \\rangle$: $D_{\\vec{i}} f = f_x$.\n"
              "- $\\vec{u} = \\vec{j} = \\langle 0, 1 \\rangle$: $D_{\\vec{j}} f = f_y$.\n\n"
              "Las parciales son **casos particulares** de derivadas direccionales en las direcciones de los ejes."
          )),

        b("definicion",
          titulo="Gradiente",
          body_md=(
              "El **gradiente** de $f(x, y)$ es:\n\n"
              "$$\\nabla f = \\langle f_x, f_y \\rangle$$\n\n"
              "**Para $f(x, y, z)$:** $\\nabla f = \\langle f_x, f_y, f_z \\rangle$.\n\n"
              "Es un **vector** cuyas componentes son las parciales. Vive en el dominio de $f$ (no en su gráfica)."
          )),

        b("teorema",
          nombre="Cálculo de la derivada direccional",
          enunciado_md=(
              "Si $f$ es **diferenciable** en $(a, b)$ y $\\vec{u}$ es un vector unitario:\n\n"
              "$$D_{\\vec{u}} f(a, b) = \\nabla f(a, b) \\cdot \\vec{u}$$\n\n"
              "Es decir, **producto punto del gradiente con la dirección**.\n\n"
              "**Si $\\vec{u}$ no es unitario:** primero normalizarlo. Si dan una dirección $\\vec{v}$ no unitaria, la derivada en esa dirección es $\\nabla f \\cdot (\\vec{v}/\\|\\vec{v}\\|)$."
          ),
          demostracion_md=(
              "Sea $g(t) = f((a, b) + t\\vec{u}) = f(a + t u_1, b + t u_2)$. Entonces $D_{\\vec{u}} f(a, b) = g'(0)$.\n\n"
              "Por la regla de la cadena: $g'(t) = f_x \\cdot u_1 + f_y \\cdot u_2 = \\nabla f \\cdot \\vec{u}$. "
              "Evaluando en $t = 0$ se obtiene la fórmula."
          )),

        b("teorema",
          nombre="Propiedades geométricas del gradiente",
          enunciado_md=(
              "Sea $f$ diferenciable en $P$ con $\\nabla f(P) \\neq \\vec{0}$. Entonces:\n\n"
              "**1. Dirección de máximo crecimiento:** la dirección en la que $f$ crece **más rápido** es $\\nabla f / \\|\\nabla f\\|$. La tasa máxima es $\\|\\nabla f\\|$.\n\n"
              "**2. Dirección de máximo decrecimiento:** $-\\nabla f / \\|\\nabla f\\|$. Tasa máxima de decrecimiento: $-\\|\\nabla f\\|$.\n\n"
              "**3. Direcciones de cambio cero:** todas las perpendiculares a $\\nabla f$. En particular, **$\\nabla f$ es perpendicular a las curvas de nivel** que pasan por $P$.\n\n"
              "**4. Magnitud:** $D_{\\vec{u}} f = \\|\\nabla f\\| \\cos\\theta$ donde $\\theta$ es el ángulo entre $\\vec{u}$ y $\\nabla f$. Va de $-\\|\\nabla f\\|$ a $+\\|\\nabla f\\|$."
          ),
          demostracion_md=(
              "$D_{\\vec{u}} f = \\nabla f \\cdot \\vec{u} = \\|\\nabla f\\| \\|\\vec{u}\\| \\cos\\theta = \\|\\nabla f\\| \\cos\\theta$ (porque $\\vec{u}$ es unitario).\n\n"
              "Maximizar respecto a $\\vec{u}$: $\\cos\\theta = 1 \\iff \\vec{u}$ paralelo a $\\nabla f$, máximo $\\|\\nabla f\\|$.\n\n"
              "Minimizar: $\\cos\\theta = -1 \\iff \\vec{u}$ antiparalelo a $\\nabla f$, mínimo $-\\|\\nabla f\\|$.\n\n"
              "Cero: $\\cos\\theta = 0 \\iff \\vec{u} \\perp \\nabla f$. **Las curvas de nivel son las trayectorias donde $f$ no cambia**, así sus tangentes son perpendiculares a $\\nabla f$."
          )),

        fig(
            "Gradiente como dirección de máximo crecimiento, perpendicular a curvas de nivel. Plano "
            "2D (vista superior). Tres curvas de nivel concéntricas (líneas curvas) etiquetadas 'f "
            "= 1', 'f = 2', 'f = 3', en color azul oscuro. En un punto P sobre la curva 'f = 2', "
            "dibujar el vector ∇f saliendo perpendicular a la curva apuntando hacia 'f = 3' (la "
            "curva de mayor valor), en color ámbar grueso. Etiqueta '∇f (dirección de máximo "
            "crecimiento)'. Otro vector unitario u en otra dirección desde P, en gris, etiquetado "
            "'u'. Entre ∇f y u, marcar el ángulo θ. Etiquetas: 'P', 'curvas de nivel', '∇f', 'u', "
            "'θ'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Derivada direccional",
          problema_md=(
              "Sea $f(x, y) = x^2 y + y^3$. Calcular $D_{\\vec{u}} f(1, 2)$ en la dirección $\\vec{v} = \\langle 3, 4 \\rangle$."
          ),
          pasos=[
              {"accion_md": "**Normalizar la dirección:** $\\|\\vec{v}\\| = 5$, así $\\vec{u} = \\langle 3/5, 4/5 \\rangle$.",
               "justificacion_md": "$D_{\\vec{u}} f$ exige $\\vec{u}$ unitario.",
               "es_resultado": False},
              {"accion_md": "**Gradiente:** $\\nabla f = \\langle 2xy, x^2 + 3y^2 \\rangle$. **En $(1, 2)$:** $\\nabla f(1, 2) = \\langle 4, 13 \\rangle$.",
               "justificacion_md": "Cálculo directo de parciales.",
               "es_resultado": False},
              {"accion_md": "**Producto punto:**\n\n"
                            "$D_{\\vec{u}} f(1, 2) = \\langle 4, 13 \\rangle \\cdot \\langle 3/5, 4/5 \\rangle = \\dfrac{12 + 52}{5} = \\dfrac{64}{5} = 12.8$.",
               "justificacion_md": "Aplicación directa de la fórmula. **$f$ crece a tasa $12.8$ en la dirección de $\\vec{v}$ desde $(1, 2)$.**",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Dirección de máximo crecimiento",
          problema_md=(
              "Sea $T(x, y) = 100 - x^2 - 2y^2$ (temperatura en cada punto). En $(1, 1)$, "
              "**(a)** ¿en qué dirección la temperatura crece más rápido? **(b)** ¿Cuál es esa tasa máxima?"
          ),
          pasos=[
              {"accion_md": "**Gradiente:** $\\nabla T = \\langle -2x, -4y \\rangle$. **En $(1, 1)$:** $\\nabla T(1, 1) = \\langle -2, -4 \\rangle$.",
               "justificacion_md": "Estándar.",
               "es_resultado": False},
              {"accion_md": "**(a)** Dirección de máximo crecimiento: $\\hat{u} = \\dfrac{\\langle -2, -4 \\rangle}{\\sqrt{4+16}} = \\dfrac{1}{\\sqrt{20}}\\langle -2, -4 \\rangle = \\dfrac{1}{\\sqrt{5}}\\langle -1, -2 \\rangle$.",
               "justificacion_md": "Normalizamos $\\nabla T$.",
               "es_resultado": False},
              {"accion_md": "**(b)** Tasa máxima: $\\|\\nabla T(1, 1)\\| = \\sqrt{20} = 2\\sqrt{5} \\approx 4.47$ unidades de temperatura por unidad de longitud.",
               "justificacion_md": "**Interpretación:** la \"flecha de calor\" en $(1, 1)$ apunta en dirección $\\langle -1, -2\\rangle$ (hacia el origen, donde $T$ es máxima) — y el ritmo de calentamiento allí es $2\\sqrt{5}$.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Gradiente como mapa de senderismo",
          body_md=(
              "**Analogía topográfica:** si $f(x, y)$ es la altura del terreno:\n\n"
              "- **Curvas de nivel** = curvas de altura constante (las del mapa).\n"
              "- **$\\nabla f$ en cada punto** = flecha que apunta **cuesta arriba más empinada**, perpendicular a las curvas de nivel.\n"
              "- **$\\|\\nabla f\\|$** = pendiente de esa cuesta.\n"
              "- **$-\\nabla f$** = dirección por donde **rodaría** una pelota (cuesta abajo).\n\n"
              "**Aplicación física:** en un campo de temperatura, $-\\nabla T$ es la dirección de flujo del calor (de caliente a frío). Análogo para presión, concentración química, potencial gravitacional."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\vec{u}$ no es unitario, $D_{\\vec{u}} f = \\nabla f \\cdot \\vec{u}$ es:",
                  "opciones_md": [
                      "Igual a $D_{\\hat{u}} f$.",
                      "$\\|\\vec{u}\\|$ veces $D_{\\hat{u}} f$.",
                      "Independiente de $\\|\\vec{u}\\|$.",
                      "Vectorial, no escalar.",
                  ],
                  "correcta": "B",
                  "pista_md": "Si escalas $\\vec{u}$ por un factor $c$, el producto punto se escala por $c$.",
                  "explicacion_md": (
                      "$\\nabla f \\cdot (c\\hat{u}) = c \\nabla f \\cdot \\hat{u}$. **Por eso es esencial normalizar antes** — para que la derivada direccional refleje la tasa de cambio por unidad de distancia, independiente de la longitud del vector dirección."
                  ),
              },
              {
                  "enunciado_md": "Si $\\nabla f(P) = \\vec{0}$, ¿qué se puede decir de $D_{\\vec{u}} f(P)$?",
                  "opciones_md": [
                      "Vale $\\|\\vec{u}\\|$.",
                      "Vale $0$ para toda dirección $\\vec{u}$.",
                      "Es indefinida.",
                      "Vale $1$.",
                  ],
                  "correcta": "B",
                  "pista_md": "Producto punto con $\\vec{0}$.",
                  "explicacion_md": (
                      "$D_{\\vec{u}} f = \\nabla f \\cdot \\vec{u} = 0 \\cdot \\vec{u} = 0$ para todo $\\vec{u}$. **$P$ es un punto crítico** — la pendiente es cero en todas direcciones (candidato a extremo, lección 5.3)."
                  ),
              },
          ]),

        ej(
            titulo="Direccional en un punto específico",
            enunciado=(
                "Sea $f(x, y, z) = e^x \\sin(yz)$. Calcula $D_{\\vec{u}} f(0, \\pi/4, 1)$ donde $\\vec{u} = \\langle 1, 1, 1 \\rangle / \\sqrt{3}$."
            ),
            pistas=[
                "Calcula $\\nabla f$ y evalúalo en el punto.",
                "$f_x = e^x \\sin(yz)$, $f_y = e^x z \\cos(yz)$, $f_z = e^x y \\cos(yz)$.",
            ],
            solucion=(
                "**$\\nabla f = \\langle e^x \\sin(yz), z e^x \\cos(yz), y e^x \\cos(yz) \\rangle$.**\n\n"
                "**En $(0, \\pi/4, 1)$:** $e^0 = 1$, $\\sin(\\pi/4) = \\cos(\\pi/4) = \\sqrt{2}/2$.\n\n"
                "$\\nabla f = \\langle \\sqrt{2}/2, \\sqrt{2}/2, (\\pi/4)(\\sqrt{2}/2) \\rangle = \\dfrac{\\sqrt{2}}{2}\\langle 1, 1, \\pi/4 \\rangle$.\n\n"
                "$D_{\\vec{u}} f = \\dfrac{\\sqrt{2}}{2} \\cdot \\dfrac{1}{\\sqrt{3}}(1 + 1 + \\pi/4) = \\dfrac{\\sqrt{2}}{2\\sqrt{3}}\\left(2 + \\dfrac{\\pi}{4}\\right) = \\dfrac{\\sqrt{6}}{12}(8 + \\pi)$."
            ),
        ),

        ej(
            titulo="Tasa de cambio en una curva",
            enunciado=(
                "La temperatura en cada punto de una placa es $T(x, y) = 80 - x^2 + 2y$. Una hormiga "
                "está en $(2, 1)$ y se mueve hacia $(4, 3)$. ¿Cuál es la tasa instantánea de cambio "
                "de temperatura que siente al iniciar?"
            ),
            pistas=[
                "Dirección de movimiento: $\\vec{v} = (4, 3) - (2, 1) = (2, 2)$. Normaliza.",
                "Calcula $\\nabla T(2, 1)$.",
                "$D_{\\vec{u}} T = \\nabla T \\cdot \\vec{u}$.",
            ],
            solucion=(
                "$\\vec{v} = \\langle 2, 2 \\rangle$, $\\|\\vec{v}\\| = 2\\sqrt{2}$, $\\vec{u} = \\langle 1, 1 \\rangle/\\sqrt{2}$.\n\n"
                "$\\nabla T = \\langle -2x, 2 \\rangle$. En $(2, 1)$: $\\nabla T = \\langle -4, 2 \\rangle$.\n\n"
                "$D_{\\vec{u}} T = \\langle -4, 2 \\rangle \\cdot \\langle 1/\\sqrt{2}, 1/\\sqrt{2} \\rangle = \\dfrac{-4 + 2}{\\sqrt{2}} = -\\sqrt{2}$.\n\n"
                "**La hormiga siente que la temperatura DECRECE a tasa $\\sqrt{2}$** unidades por unidad de distancia recorrida."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**No normalizar el vector dirección.** Sin normalizar, $D_{\\vec{u}} f$ no es la tasa de cambio por unidad de distancia.",
              "**Confundir gradiente con direccional.** El gradiente es un vector; la direccional es un escalar (producto punto del gradiente con una dirección).",
              "**Pensar que $\\nabla f$ apunta hacia un máximo absoluto.** No — apunta hacia el máximo crecimiento **local**. Puede llevar a un punto crítico que sea silla, no máximo.",
              "**Olvidar que $\\nabla f$ es perpendicular a las curvas de nivel.** Es la propiedad geométrica más importante.",
              "**Aplicar la fórmula $\\nabla f \\cdot \\vec{u}$ cuando $f$ no es diferenciable.** El teorema requiere diferenciabilidad.",
          ]),

        b("resumen",
          puntos_md=[
              "**Derivada direccional:** $D_{\\vec{u}} f = \\nabla f \\cdot \\vec{u}$ (con $\\vec{u}$ unitario).",
              "**Gradiente:** $\\nabla f = \\langle f_x, f_y \\rangle$ (o tres componentes en 3D).",
              "**Máximo crecimiento:** dirección $\\nabla f$, tasa $\\|\\nabla f\\|$.",
              "**Máximo decrecimiento:** dirección $-\\nabla f$, tasa $-\\|\\nabla f\\|$.",
              "**Cambio cero:** direcciones $\\perp$ a $\\nabla f$ — tangentes a curvas de nivel.",
              "**Aplicación:** flujo de calor (sigue $-\\nabla T$), pelota rodando, optimización local.",
              "**Próxima lección:** valores máximos y mínimos — usar $\\nabla f = \\vec{0}$ para encontrar críticos.",
          ]),
    ]
    return {
        "id": "lec-mvar-5-2-direccionales",
        "title": "Derivadas direccionales",
        "description": "Derivada direccional, gradiente, dirección de máximo crecimiento y perpendicularidad a curvas de nivel.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 5.3 Valores máximos y mínimos
# =====================================================================
def lesson_5_3():
    blocks = [
        b("texto", body_md=(
            "Encontrar **máximos y mínimos** de funciones $f(x, y)$ es una de las aplicaciones más importantes "
            "de las derivadas parciales. La estrategia es paralela al caso 1D — encontrar puntos críticos "
            "y clasificarlos — pero ahora aparece una **nueva categoría**: los **puntos silla**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Identificar **puntos críticos** ($\\nabla f = \\vec{0}$).\n"
            "- Aplicar el **criterio de la segunda derivada** (test del Hessiano) para clasificarlos.\n"
            "- Reconocer **puntos silla** (mínimo en una dirección, máximo en otra).\n"
            "- Encontrar **extremos absolutos** sobre regiones cerradas y acotadas."
        )),

        b("definicion",
          titulo="Extremos locales y puntos críticos",
          body_md=(
              "$f$ tiene un **máximo local** en $(a, b)$ si $f(a, b) \\geq f(x, y)$ para todo $(x, y)$ cerca de $(a, b)$. "
              "Análogamente para **mínimo local**.\n\n"
              "**Punto crítico:** $(a, b)$ es punto crítico de $f$ si:\n\n"
              "$$\\nabla f(a, b) = \\vec{0}, \\quad \\text{es decir,} \\quad f_x(a, b) = 0 \\text{ y } f_y(a, b) = 0$$\n\n"
              "**O bien $\\nabla f$ no existe** allí.\n\n"
              "**Teorema de Fermat:** si $f$ tiene un extremo local en $(a, b)$ y existen las parciales, entonces $(a, b)$ es punto crítico."
          )),

        b("intuicion",
          titulo="Puntos silla — la novedad de varias variables",
          body_md=(
              "En 1D, un punto crítico es máximo, mínimo, o nada (un punto de inflexión horizontal). En 2D aparece un **caso nuevo**: el **punto silla**.\n\n"
              "Un **punto silla** es un punto crítico que es **máximo en una dirección y mínimo en otra**. La gráfica se parece a una silla de montar.\n\n"
              "**Ejemplo clásico:** $f(x, y) = x^2 - y^2$ en $(0, 0)$. $f_x = 2x, f_y = -2y$, ambas $0$ en el origen. Pero:\n\n"
              "- En el eje $x$ ($y = 0$): $f = x^2$, mínimo en $0$.\n"
              "- En el eje $y$ ($x = 0$): $f = -y^2$, máximo en $0$.\n\n"
              "Es la \"silla de montar\" geométrica."
          )),

        fig(
            "Tres tipos de puntos críticos en una función f(x, y), vista 3D isométrica. PANEL 1: "
            "mínimo local — superficie con forma de cuenco (paraboloide), un punto al fondo "
            "marcado, etiqueta 'mínimo local'. PANEL 2: máximo local — superficie con forma de "
            "domo invertido, un punto en la cima marcado, etiqueta 'máximo local'. PANEL 3: punto "
            "silla — superficie con forma de silla de montar (paraboloide hiperbólico z = x² - "
            "y²), un punto en el centro marcado, etiqueta 'punto silla'. Los tres en color teal "
            "translúcido. Cada panel con su nombre debajo. " + STYLE
        ),

        b("teorema",
          nombre="Criterio de la segunda derivada (Hessiano)",
          enunciado_md=(
              "Sea $(a, b)$ punto crítico de $f$ con segundas parciales continuas en un entorno. Define el **discriminante** (o **determinante del Hessiano**):\n\n"
              "$$D = D(a, b) = f_{xx}(a, b) \\cdot f_{yy}(a, b) - [f_{xy}(a, b)]^2$$\n\n"
              "Entonces:\n\n"
              "- Si $D > 0$ y $f_{xx}(a, b) > 0$: **mínimo local**.\n"
              "- Si $D > 0$ y $f_{xx}(a, b) < 0$: **máximo local**.\n"
              "- Si $D < 0$: **punto silla**.\n"
              "- Si $D = 0$: **inconcluso** — usar otro método (analizar trayectorias o orden superior).\n\n"
              "**Forma matricial:** $D$ es el determinante del **Hessiano** $H = \\begin{pmatrix} f_{xx} & f_{xy} \\\\ f_{xy} & f_{yy} \\end{pmatrix}$ en $(a, b)$."
          ),
          demostracion_md=(
              "Idea: el **polinomio de Taylor de segundo orden** alrededor de $(a, b)$ es:\n\n"
              "$f(a+h, b+k) \\approx f(a,b) + \\dfrac{1}{2}(f_{xx} h^2 + 2 f_{xy} h k + f_{yy} k^2)$\n\n"
              "(los términos de primer orden son $0$ porque $\\nabla f(a, b) = \\vec{0}$). "
              "El comportamiento depende del signo de la **forma cuadrática**, que se determina por $D$ y $f_{xx}$ (criterio de Sylvester)."
          )),

        b("ejemplo_resuelto",
          titulo="Clasificar puntos críticos",
          problema_md=(
              "Encontrar y clasificar los puntos críticos de $f(x, y) = x^3 - 3xy + y^3$."
          ),
          pasos=[
              {"accion_md": "**Plantear $\\nabla f = \\vec{0}$:**\n\n"
                            "$f_x = 3x^2 - 3y = 0 \\implies y = x^2$.\n\n"
                            "$f_y = -3x + 3y^2 = 0 \\implies x = y^2$.",
               "justificacion_md": "Sistema de dos ecuaciones.",
               "es_resultado": False},
              {"accion_md": "**Sustituir $y = x^2$** en $x = y^2$: $x = x^4 \\iff x(x^3 - 1) = 0 \\iff x = 0$ o $x = 1$.\n\n"
                            "**Críticos:** $(0, 0)$ y $(1, 1)$.",
               "justificacion_md": "Las soluciones del sistema.",
               "es_resultado": False},
              {"accion_md": "**Hessiano:** $f_{xx} = 6x$, $f_{yy} = 6y$, $f_{xy} = -3$. $D = 36xy - 9$.\n\n"
                            "**En $(0, 0)$:** $D = -9 < 0$ → **punto silla**.\n\n"
                            "**En $(1, 1)$:** $D = 36 - 9 = 27 > 0$, $f_{xx}(1, 1) = 6 > 0$ → **mínimo local**.",
               "justificacion_md": "**Lección:** un sistema cúbico puede tener múltiples críticos con clasificaciones distintas.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Función con un máximo local",
          problema_md=(
              "Encontrar y clasificar los puntos críticos de $f(x, y) = -x^2 - y^2 + 4x + 6y - 5$."
          ),
          pasos=[
              {"accion_md": "**$\\nabla f = \\vec{0}$:**\n\n"
                            "$f_x = -2x + 4 = 0 \\implies x = 2$. $f_y = -2y + 6 = 0 \\implies y = 3$.\n\n"
                            "**Único crítico:** $(2, 3)$.",
               "justificacion_md": "Sistema lineal trivial.",
               "es_resultado": False},
              {"accion_md": "**Hessiano:** $f_{xx} = -2$, $f_{yy} = -2$, $f_{xy} = 0$. $D = (-2)(-2) - 0 = 4 > 0$.\n\n"
                            "$f_{xx} = -2 < 0$ → **máximo local** en $(2, 3)$. **Valor:** $f(2, 3) = -4 - 9 + 8 + 18 - 5 = 8$.",
               "justificacion_md": "**Comprobación geométrica:** completar cuadrados: $f = -((x-2)^2 + (y-3)^2) + 8$. Es un paraboloide invertido con vértice $(2, 3, 8)$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Extremos absolutos en regiones cerradas y acotadas",
          body_md=(
              "Por el **teorema del valor extremo (en 2D)**: si $f$ es continua en una región $D$ **cerrada y acotada**, $f$ alcanza un **máximo absoluto** y un **mínimo absoluto** en $D$.\n\n"
              "**Procedimiento:**\n\n"
              "1. Encontrar los **puntos críticos** de $f$ en el interior de $D$.\n"
              "2. Encontrar los **extremos sobre la frontera** $\\partial D$ (suele requerir parametrizar el borde y reducir a un problema 1D).\n"
              "3. **Evaluar** $f$ en los candidatos del paso 1 y 2.\n"
              "4. **Comparar:** el mayor es el máximo absoluto, el menor el mínimo.\n\n"
              "Si $D$ no es cerrado y acotado, los extremos pueden no existir."
          )),

        b("ejemplo_resuelto",
          titulo="Extremos absolutos en un cuadrado",
          problema_md=(
              "Encontrar los extremos absolutos de $f(x, y) = x^2 + y^2 - 2x$ sobre el cuadrado $[0, 2] \\times [0, 2]$."
          ),
          pasos=[
              {"accion_md": "**Interior:** $f_x = 2x - 2 = 0 \\implies x = 1$. $f_y = 2y = 0 \\implies y = 0$. Crítico $(1, 0)$. **Está en la frontera, no en el interior** — lo trataremos en la frontera.",
               "justificacion_md": "El interior del cuadrado es $(0,2)\\times(0,2)$, sin incluir el borde. $(1, 0)$ está en el borde.",
               "es_resultado": False},
              {"accion_md": "**Frontera:** cuatro lados.\n\n"
                            "**Lado 1 ($y = 0, 0 \\leq x \\leq 2$):** $f = x^2 - 2x$, $f' = 2x - 2 = 0 \\implies x = 1$. Valores en $0, 1, 2$: $f(0,0) = 0, f(1, 0) = -1, f(2, 0) = 0$.\n\n"
                            "**Lado 2 ($y = 2, 0 \\leq x \\leq 2$):** $f = x^2 - 2x + 4$, $f' = 2x - 2 = 0 \\implies x = 1$. Valores: $f(0, 2) = 4, f(1, 2) = 3, f(2, 2) = 4$.\n\n"
                            "**Lado 3 ($x = 0, 0 \\leq y \\leq 2$):** $f = y^2$, mínimo en $y = 0$ ($f = 0$), máximo en $y = 2$ ($f = 4$).\n\n"
                            "**Lado 4 ($x = 2, 0 \\leq y \\leq 2$):** $f = y^2$, mínimo $0$ en $y=0$, máximo $4$ en $y=2$.",
               "justificacion_md": "En cada lado, parametrizar y reducir a 1D.",
               "es_resultado": False},
              {"accion_md": "**Comparar todos los candidatos:** $\\{0, -1, 0, 4, 3, 4, 0, 4, 0, 4\\}$.\n\n"
                            "**Mínimo absoluto:** $-1$ en $(1, 0)$.\n**Máximo absoluto:** $4$ en $(0, 2), (2, 0), (2, 2)$ — alcanzado en tres esquinas.",
               "justificacion_md": "**Lección:** revisar cada lado por separado y todas las esquinas. El máximo puede repetirse.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $D > 0$ y $f_{xx} < 0$ en un punto crítico, es:",
                  "opciones_md": [
                      "Mínimo local",
                      "Máximo local",
                      "Punto silla",
                      "Inconcluso",
                  ],
                  "correcta": "B",
                  "pista_md": "$D > 0$ → no es silla. $f_{xx} < 0$ → cóncava hacia abajo en dirección $x$.",
                  "explicacion_md": (
                      "$D > 0$ con $f_{xx} < 0$ significa que ambas direcciones principales son cóncavas hacia abajo. **Máximo local.**"
                  ),
              },
              {
                  "enunciado_md": "Si $D < 0$ en un punto crítico, es:",
                  "opciones_md": [
                      "Mínimo local",
                      "Máximo local",
                      "Punto silla",
                      "Inconcluso",
                  ],
                  "correcta": "C",
                  "pista_md": "$D < 0$ significa direcciones de signos opuestos.",
                  "explicacion_md": (
                      "$D < 0$ siempre indica **silla** — la función crece en una dirección y decrece en otra. La firma del paraboloide hiperbólico."
                  ),
              },
          ]),

        ej(
            titulo="Críticos con función polinomial",
            enunciado="Halla y clasifica los puntos críticos de $f(x, y) = x^4 + y^4 - 4xy + 1$.",
            pistas=[
                "$f_x = 4x^3 - 4y$, $f_y = 4y^3 - 4x$. Iguala a cero.",
                "Del sistema: $x^3 = y$ y $y^3 = x$. Sustituye una en la otra.",
                "Obtienes $x^9 = x \\iff x(x^8 - 1) = 0$.",
            ],
            solucion=(
                "$x^9 = x \\iff x = 0$ o $x^8 = 1 \\iff x = \\pm 1$. **Críticos:** $(0, 0), (1, 1), (-1, -1)$.\n\n"
                "**Hessiano:** $f_{xx} = 12x^2$, $f_{yy} = 12y^2$, $f_{xy} = -4$. $D = 144 x^2 y^2 - 16$.\n\n"
                "- $(0, 0)$: $D = -16 < 0$ → **punto silla**.\n"
                "- $(1, 1)$: $D = 144 - 16 = 128 > 0$, $f_{xx} = 12 > 0$ → **mínimo local**.\n"
                "- $(-1, -1)$: $D = 144 - 16 = 128 > 0$, $f_{xx} = 12 > 0$ → **mínimo local**.\n\n"
                "Función con dos mínimos simétricos y una silla en el origen. Valor mínimo: $f(\\pm 1, \\pm 1) = 1 + 1 - 4 + 1 = -1$."
            ),
        ),

        ej(
            titulo="Caja de volumen máximo",
            enunciado=(
                "Una caja rectangular sin tapa tiene volumen $32$ m³. Halla las dimensiones que minimizan el material usado."
            ),
            pistas=[
                "Variables: lados $x, y$ de la base y altura $z$. Restricción: $xyz = 32$.",
                "Material: $S = xy + 2xz + 2yz$ (base + 4 caras laterales).",
                "Despeja $z = 32/(xy)$ y sustituye en $S$. Reduce a problema en $(x, y)$.",
                "Encuentra críticos de $S(x, y) = xy + 64/y + 64/x$.",
            ],
            solucion=(
                "$S(x, y) = xy + 64/x + 64/y$. **Críticos:** $S_x = y - 64/x^2 = 0 \\implies x^2 y = 64$. $S_y = x - 64/y^2 = 0 \\implies x y^2 = 64$.\n\n"
                "Dividiendo: $x/y = 1 \\implies x = y$. Sustituyendo: $x^3 = 64 \\implies x = 4$.\n\n"
                "**Solución:** $x = y = 4$ m, $z = 32/16 = 2$ m. Material: $S = 16 + 16 + 16 = 48$ m².\n\n"
                "**Verificación con Hessiano:** $S_{xx} = 128/x^3, S_{yy} = 128/y^3, S_{xy} = 1$. En $(4, 4)$: $D = (2)(2) - 1 = 3 > 0$, $S_{xx} = 2 > 0$ → mínimo. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar comprobar puntos donde $\\nabla f$ no existe.** Pueden ser críticos.",
              "**Confundir los signos del criterio:** $D > 0$ con $f_{xx} > 0$ es mínimo, $f_{xx} < 0$ es máximo. $D < 0$ es silla, **independiente del signo de $f_{xx}$**.",
              "**Olvidar la frontera** al buscar extremos absolutos en una región cerrada.",
              "**Aplicar el test cuando $D = 0$.** Es inconcluso — necesita análisis adicional.",
              "**Pensar que todo punto crítico es extremo.** Las sillas también son críticos pero no son extremos.",
          ]),

        b("resumen",
          puntos_md=[
              "**Punto crítico:** $\\nabla f = \\vec{0}$ (o $\\nabla f$ no existe).",
              "**Test del Hessiano:** $D = f_{xx} f_{yy} - f_{xy}^2$.",
              "**Clasificación:** $D > 0, f_{xx} > 0$ → mínimo; $D > 0, f_{xx} < 0$ → máximo; $D < 0$ → silla; $D = 0$ → inconcluso.",
              "**Extremos absolutos en cerrado acotado:** críticos en interior + análisis de frontera + comparar.",
              "**Frontera:** parametrizar y reducir a problema 1D, considerar también las esquinas.",
              "**Próxima lección:** multiplicadores de Lagrange — optimización con restricción $g = k$.",
          ]),
    ]
    return {
        "id": "lec-mvar-5-3-extremos",
        "title": "Valores máximos y mínimos",
        "description": "Puntos críticos, test del Hessiano, puntos silla y extremos absolutos en regiones cerradas.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
    }


# =====================================================================
# 5.4 Multiplicadores de Lagrange
# =====================================================================
def lesson_5_4():
    blocks = [
        b("texto", body_md=(
            "¿Cómo encontrar el punto sobre una elipse más cercano al origen? ¿Cómo maximizar el volumen "
            "de una caja con superficie fija? Estos son problemas de **optimización con restricción**: "
            "no buscamos el extremo de $f$ en todo el plano, sino sobre una **curva** $g(x, y) = k$.\n\n"
            "El método de **multiplicadores de Lagrange** los resuelve elegantemente — y es uno de los "
            "resultados más bonitos del cálculo multivariable.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Comprender la **idea geométrica**: en el extremo, $\\nabla f$ y $\\nabla g$ son paralelos.\n"
            "- Aplicar el método: $\\nabla f = \\lambda \\nabla g$ junto con $g = k$.\n"
            "- Manejar el **caso de dos restricciones** $\\nabla f = \\lambda \\nabla g + \\mu \\nabla h$."
        )),

        b("intuicion",
          titulo="¿Por qué los gradientes deben ser paralelos?",
          body_md=(
              "Imagina las **curvas de nivel** $f = c$ y la curva de restricción $g = k$. Si nos movemos a lo largo de $g = k$, "
              "vamos pasando por curvas de nivel de $f$ — el valor de $f$ cambia.\n\n"
              "**El extremo se alcanza cuando** $g = k$ es **tangente** a una curva de nivel de $f$. Si las curvas se cruzaran transversalmente en un punto, podríamos seguir avanzando sobre $g$ y aumentar (o disminuir) $f$ aún más — no sería extremo.\n\n"
              "**Dos curvas tangentes en un punto** ⟺ tienen la **misma normal** allí. Como $\\nabla f$ es normal a las curvas de nivel de $f$, y $\\nabla g$ es normal a la curva $g = k$:\n\n"
              "$$\\nabla f \\text{ paralelo a } \\nabla g \\iff \\nabla f = \\lambda \\nabla g \\text{ para algún } \\lambda$$\n\n"
              "$\\lambda$ es el **multiplicador de Lagrange**."
          )),

        fig(
            "Idea geométrica de multiplicadores de Lagrange. Plano 2D. Curvas de nivel concéntricas "
            "de f, dibujadas como elipses suavemente irregulares en líneas finas color azul, "
            "etiquetadas 'f = 1', 'f = 2', 'f = 3', 'f = 4'. Una curva de restricción g(x,y) = k "
            "atravesando las curvas de nivel, dibujada en color teal grueso, etiquetada 'g(x, y) = "
            "k'. En el punto donde la curva g toca tangencialmente a una curva de nivel (digamos f "
            "= 3), marcar ese punto P como destacado. Desde P, dibujar dos vectores: ∇f en color "
            "ámbar (perpendicular a la curva de nivel) y ∇g en color verde (perpendicular a la "
            "curva de restricción). Mostrar que apuntan en la misma dirección (paralelos). "
            "Etiquetas: 'P = punto óptimo', '∇f', '∇g', '∇f = λ∇g'. " + STYLE
        ),

        b("teorema",
          nombre="Multiplicadores de Lagrange",
          enunciado_md=(
              "Para encontrar los **extremos** de $f(x, y)$ sujetos a la **restricción** $g(x, y) = k$ "
              "(con $f, g$ diferenciables y $\\nabla g \\neq \\vec{0}$), buscamos puntos $(x, y)$ tales que:\n\n"
              "$$\\nabla f(x, y) = \\lambda \\, \\nabla g(x, y)$$\n\n"
              "$$g(x, y) = k$$\n\n"
              "Es un **sistema de tres ecuaciones** con tres incógnitas $(x, y, \\lambda)$.\n\n"
              "**En componentes:**\n\n"
              "$$f_x = \\lambda g_x, \\quad f_y = \\lambda g_y, \\quad g(x, y) = k$$\n\n"
              "Las soluciones $(x, y)$ son **candidatos** a extremos. Hay que evaluar $f$ en cada uno y comparar.\n\n"
              "**En 3D ($f, g$ funciones de $x, y, z$):** análogo con cuatro ecuaciones."
          ),
          demostracion_md=(
              "Sea $\\vec{r}(t)$ una parametrización de la curva $g = k$ con $\\vec{r}(0) = P$ punto extremo. "
              "Entonces $h(t) = f(\\vec{r}(t))$ tiene un extremo en $t = 0$, así $h'(0) = 0$.\n\n"
              "Por la regla de la cadena: $h'(0) = \\nabla f(P) \\cdot \\vec{r}'(0) = 0$. **$\\nabla f(P)$ es perpendicular a la tangente $\\vec{r}'(0)$ de la curva.**\n\n"
              "Por otro lado, $g(\\vec{r}(t)) = k$ constante, así $\\nabla g(P) \\cdot \\vec{r}'(0) = 0$. **$\\nabla g(P)$ también es perpendicular a la tangente.**\n\n"
              "Dos vectores en $\\mathbb{R}^2$ ambos perpendiculares al mismo vector son **paralelos**: $\\nabla f = \\lambda \\nabla g$."
          )),

        b("ejemplo_resuelto",
          titulo="Punto más cercano al origen sobre una recta",
          problema_md=(
              "Encontrar el punto sobre la recta $x + 2y = 5$ más cercano al origen."
          ),
          pasos=[
              {"accion_md": "**Función a minimizar:** la distancia al origen $\\sqrt{x^2 + y^2}$. Para evitar la raíz, minimizamos su cuadrado: $f(x, y) = x^2 + y^2$.\n\n"
                            "**Restricción:** $g(x, y) = x + 2y = 5$.",
               "justificacion_md": "Truco estándar: minimizar el cuadrado de la distancia (mismo punto óptimo).",
               "es_resultado": False},
              {"accion_md": "**Sistema de Lagrange:**\n\n"
                            "$\\nabla f = \\langle 2x, 2y \\rangle$, $\\nabla g = \\langle 1, 2 \\rangle$.\n\n"
                            "$2x = \\lambda \\cdot 1, \\quad 2y = \\lambda \\cdot 2, \\quad x + 2y = 5$.",
               "justificacion_md": "Tres ecuaciones, tres incógnitas $(x, y, \\lambda)$.",
               "es_resultado": False},
              {"accion_md": "**De las dos primeras:** $\\lambda = 2x$ y $\\lambda = y$. Igualando: $y = 2x$.\n\n"
                            "**Sustituir en la tercera:** $x + 2(2x) = 5 \\implies 5x = 5 \\implies x = 1, y = 2$.",
               "justificacion_md": "Sistema lineal sencillo.",
               "es_resultado": False},
              {"accion_md": "**Punto óptimo:** $(1, 2)$. **Distancia mínima:** $\\sqrt{1 + 4} = \\sqrt{5}$.\n\n"
                            "**Verificación geométrica:** la perpendicular desde el origen a la recta $x + 2y = 5$ debe ser paralela al vector director normal de la recta. El vector dirección normal es $\\langle 1, 2 \\rangle$. Punto óptimo: $\\frac{5}{5}\\langle 1, 2 \\rangle = (1, 2)$. ✓",
               "justificacion_md": "**Lección:** Lagrange recupera el resultado geométrico clásico.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caja con superficie fija, volumen máximo",
          problema_md=(
              "Una caja rectangular cerrada tiene superficie total $S = 96$ cm². Encontrar las dimensiones que maximizan el volumen."
          ),
          pasos=[
              {"accion_md": "**$f(x, y, z) = xyz$** (volumen). **$g(x, y, z) = 2xy + 2xz + 2yz = 96$** (superficie).",
               "justificacion_md": "Maximizar volumen sujeto a restricción de superficie.",
               "es_resultado": False},
              {"accion_md": "**Sistema (4 ecuaciones):**\n\n"
                            "$yz = \\lambda(2y + 2z)$, $xz = \\lambda(2x + 2z)$, $xy = \\lambda(2x + 2y)$, $2xy + 2xz + 2yz = 96$.",
               "justificacion_md": "Las tres parciales y la restricción.",
               "es_resultado": False},
              {"accion_md": "**Por simetría**, intuir $x = y = z$. **Verificar:** las tres primeras ecuaciones dan $x^2 = \\lambda \\cdot 4x \\iff x = 4\\lambda$ (asumiendo $x \\neq 0$). Análogo para $y, z$.\n\n"
                            "Si $x = y = z$, **restricción:** $6x^2 = 96 \\implies x^2 = 16 \\implies x = 4$.",
               "justificacion_md": "Solución simétrica — un cubo. Hay que verificar que es máximo (no mínimo o silla).",
               "es_resultado": False},
              {"accion_md": "**Solución:** $x = y = z = 4$ cm. **Volumen máximo:** $V = 64$ cm³.\n\n"
                            "**Resultado clásico:** entre todas las cajas rectangulares con superficie fija, **el cubo maximiza el volumen**.",
               "justificacion_md": "**Patrón general:** problemas con simetría tienden a soluciones simétricas. Vale la pena explorar esa hipótesis primero.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Dos restricciones",
          body_md=(
              "Si hay **dos restricciones** $g(x, y, z) = k_1$ y $h(x, y, z) = k_2$, los extremos satisfacen:\n\n"
              "$$\\nabla f = \\lambda \\nabla g + \\mu \\nabla h$$\n\n"
              "$$g = k_1, \\quad h = k_2$$\n\n"
              "**Cinco ecuaciones, cinco incógnitas** $(x, y, z, \\lambda, \\mu)$.\n\n"
              "**Idea geométrica:** la intersección $g = k_1, h = k_2$ es típicamente una **curva en $\\mathbb{R}^3$**. En un extremo de $f$ sobre esa curva, $\\nabla f$ es perpendicular a la tangente — pero la tangente es perpendicular tanto a $\\nabla g$ como a $\\nabla h$. Por tanto $\\nabla f$ está en el plano generado por $\\nabla g$ y $\\nabla h$."
          )),

        b("ejemplo_resuelto",
          titulo="Maximizar sobre intersección de superficies",
          problema_md=(
              "Maximizar $f(x, y, z) = z$ sobre la intersección del cilindro $x^2 + y^2 = 1$ y el plano $x + y + z = 1$."
          ),
          pasos=[
              {"accion_md": "**Restricciones:** $g = x^2 + y^2 = 1$, $h = x + y + z = 1$. Gradientes: $\\nabla f = \\langle 0, 0, 1 \\rangle$, $\\nabla g = \\langle 2x, 2y, 0 \\rangle$, $\\nabla h = \\langle 1, 1, 1 \\rangle$.",
               "justificacion_md": "Estructura del sistema.",
               "es_resultado": False},
              {"accion_md": "**Sistema:** $0 = 2\\lambda x + \\mu$, $0 = 2\\lambda y + \\mu$, $1 = \\mu$, $x^2 + y^2 = 1$, $x + y + z = 1$.\n\n"
                            "De la tercera: $\\mu = 1$. **Sustituyendo:** $0 = 2\\lambda x + 1, 0 = 2\\lambda y + 1$, así $x = y$.",
               "justificacion_md": "$\\mu$ se despeja inmediatamente; la simetría $x = y$ surge naturalmente.",
               "es_resultado": False},
              {"accion_md": "**Restricción 1:** $x^2 + x^2 = 1 \\implies x = \\pm 1/\\sqrt{2}$, $y = \\pm 1/\\sqrt{2}$ (mismos signos).\n\n"
                            "**Restricción 2:** $z = 1 - x - y = 1 - 2x$.\n\n"
                            "**Dos candidatos:** $x = y = 1/\\sqrt{2}$, $z = 1 - \\sqrt{2}$ (con $f = 1 - \\sqrt{2} \\approx -0.41$).\n\n"
                            "$x = y = -1/\\sqrt{2}$, $z = 1 + \\sqrt{2}$ (con $f = 1 + \\sqrt{2} \\approx 2.41$).",
               "justificacion_md": "Dos puntos críticos de Lagrange.",
               "es_resultado": False},
              {"accion_md": "**Máximo:** $z = 1 + \\sqrt{2}$ en $(-1/\\sqrt{2}, -1/\\sqrt{2}, 1 + \\sqrt{2})$.",
               "justificacion_md": "**Lección:** Lagrange identifica candidatos; comparar valores selecciona el máximo.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Cuándo Lagrange vs sustitución directa",
          body_md=(
              "Para optimizar $f$ sobre $g = k$, hay dos estrategias:\n\n"
              "**1. Sustitución directa:** despejar una variable de $g = k$ y sustituir en $f$. Reduce el problema a uno sin restricción. **Funciona bien cuando** $g$ es algebraicamente simple (recta, círculo simple).\n\n"
              "**2. Lagrange:** plantear $\\nabla f = \\lambda \\nabla g$. **Mejor cuando** $g$ es complicada o cuando hay simetría que facilita el sistema.\n\n"
              "**En la práctica:** Lagrange es la opción universal. La sustitución requiere casos donde se pueda despejar limpiamente.\n\n"
              "**Ventaja conceptual de Lagrange:** $\\lambda$ tiene **interpretación física** — mide cuánto cambia el extremo cuando se relaja la restricción ($\\lambda = \\partial f^*/\\partial k$). En economía: precio sombra. En física: fuerzas de restricción."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "En un punto óptimo de $f$ sujeto a $g = k$, ¿qué relación cumplen $\\nabla f$ y $\\nabla g$?",
                  "opciones_md": [
                      "Son perpendiculares",
                      "Son paralelos: $\\nabla f = \\lambda \\nabla g$",
                      "$\\nabla f \\cdot \\nabla g = k$",
                      "Apuntan en direcciones opuestas siempre",
                  ],
                  "correcta": "B",
                  "pista_md": "Las curvas de nivel de $f$ y la curva $g = k$ son tangentes en el óptimo.",
                  "explicacion_md": (
                      "Tangencia → mismas normales (a un múltiplo escalar). Por eso $\\nabla f = \\lambda \\nabla g$. **$\\lambda$ puede ser positivo, negativo o cero**."
                  ),
              },
              {
                  "enunciado_md": "Si $\\nabla g = \\vec{0}$ en un punto, ¿qué sucede con el método de Lagrange?",
                  "opciones_md": [
                      "Funciona sin problema",
                      "Falla — hay que analizar ese punto por separado",
                      "Garantiza que es un extremo",
                      "$\\lambda$ es siempre $0$",
                  ],
                  "correcta": "B",
                  "pista_md": "El teorema asume $\\nabla g \\neq \\vec{0}$.",
                  "explicacion_md": (
                      "**El teorema de Lagrange requiere $\\nabla g \\neq \\vec{0}$.** Donde $\\nabla g = \\vec{0}$ (puntos singulares de la restricción), el método no aplica y hay que estudiar el punto manualmente."
                  ),
              },
          ]),

        ej(
            titulo="Rectángulo inscrito en círculo",
            enunciado=(
                "Hallar el rectángulo de área máxima con lados paralelos a los ejes inscrito en el círculo $x^2 + y^2 = 1$."
            ),
            pistas=[
                "Si una esquina del rectángulo es $(x, y)$ con $x, y > 0$, el área es $A = (2x)(2y) = 4xy$.",
                "Maximizar $f = 4xy$ sujeto a $g = x^2 + y^2 = 1$.",
                "Aplicar Lagrange: $4y = \\lambda(2x), 4x = \\lambda(2y)$.",
            ],
            solucion=(
                "$f = 4xy$, $g = x^2 + y^2 - 1$. Sistema: $4y = 2\\lambda x$, $4x = 2\\lambda y$, $x^2 + y^2 = 1$.\n\n"
                "Dividiendo las dos primeras: $y/x = x/y \\iff x^2 = y^2$. Como $x, y > 0$: $x = y$. Restricción: $2x^2 = 1 \\implies x = y = 1/\\sqrt{2}$.\n\n"
                "**Rectángulo óptimo:** un **cuadrado** de lado $2/\\sqrt{2} = \\sqrt{2}$. Área máxima: $2$.\n\n"
                "**Resultado clásico:** entre rectángulos inscritos en un círculo, el cuadrado maximiza el área."
            ),
        ),

        ej(
            titulo="Lagrange en 3D",
            enunciado=(
                "Hallar los extremos de $f(x, y, z) = x + 2y + 3z$ sobre la esfera $x^2 + y^2 + z^2 = 14$."
            ),
            pistas=[
                "$\\nabla f = \\langle 1, 2, 3 \\rangle$. $\\nabla g = \\langle 2x, 2y, 2z \\rangle$.",
                "Sistema: $1 = 2\\lambda x, 2 = 2\\lambda y, 3 = 2\\lambda z$.",
                "Despeja $x = 1/(2\\lambda), y = 1/\\lambda, z = 3/(2\\lambda)$ y sustituye.",
            ],
            solucion=(
                "Despejando: $x = 1/(2\\lambda), y = 2/(2\\lambda), z = 3/(2\\lambda)$, así $\\langle x, y, z \\rangle = \\dfrac{1}{2\\lambda}\\langle 1, 2, 3\\rangle$.\n\n"
                "Restricción: $\\dfrac{1+4+9}{4\\lambda^2} = 14 \\implies \\dfrac{14}{4\\lambda^2} = 14 \\implies \\lambda^2 = 1/4 \\implies \\lambda = \\pm 1/2$.\n\n"
                "**$\\lambda = 1/2$:** $\\langle x, y, z \\rangle = \\langle 1, 2, 3 \\rangle$. $f = 1 + 4 + 9 = 14$.\n"
                "**$\\lambda = -1/2$:** $\\langle x, y, z \\rangle = \\langle -1, -2, -3 \\rangle$. $f = -14$.\n\n"
                "**Máximo:** $14$ en $(1, 2, 3)$. **Mínimo:** $-14$ en $(-1, -2, -3)$. Estos puntos son los extremos del diámetro de la esfera en la dirección del gradiente $\\nabla f$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar la ecuación de restricción $g = k$.** Es esencial — sin ella, el sistema queda indeterminado.",
              "**Despejar $\\lambda$ y descartar casos.** Cuidado con la posibilidad $\\lambda = 0$ — puede ser parte del análisis.",
              "**No considerar puntos donde $\\nabla g = \\vec{0}$.** El método no aplica allí; pueden esconder extremos.",
              "**Asumir que el punto encontrado es máximo (o mínimo) sin comparar.** Lagrange da **candidatos** — hay que evaluar $f$ y comparar.",
              "**Sustituir la restricción al plantear $\\nabla f$.** Se debe trabajar con $f$ y $g$ originales, plantear el sistema, y resolver.",
          ]),

        b("resumen",
          puntos_md=[
              "**Lagrange:** $\\nabla f = \\lambda \\nabla g$, $g = k$ — sistema con $(x, y, \\lambda)$ (en 2D) o $(x, y, z, \\lambda)$ (en 3D).",
              "**Geometría:** en el extremo, las curvas de nivel de $f$ son **tangentes** a la restricción.",
              "**Dos restricciones:** $\\nabla f = \\lambda \\nabla g + \\mu \\nabla h$.",
              "**$\\lambda$ tiene significado:** sensibilidad del extremo respecto a la restricción.",
              "**Resultados clásicos:** cubo maximiza volumen con superficie fija, cuadrado maximiza área inscrita en círculo.",
              "**Cierre del capítulo:** ya tenemos las herramientas geométricas (gradiente, plano tangente, optimización con/sin restricción) — el siguiente capítulo introduce **integrales múltiples**.",
          ]),
    ]
    return {
        "id": "lec-mvar-5-4-lagrange",
        "title": "Multiplicadores de Lagrange",
        "description": "Optimización con restricciones $\\nabla f = \\lambda \\nabla g$, idea geométrica e interpretación de $\\lambda$.",
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
    course_id = "calculo-multivariable"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Curso {course_id} no existe.")

    chapter_id = "ch-aplicaciones-parciales"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Aplicaciones de las Derivadas Parciales",
        "description": "Plano tangente y linealización, derivadas direccionales y gradiente, máximos/mínimos y multiplicadores de Lagrange.",
        "order": 5,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_5_1, lesson_5_2, lesson_5_3, lesson_5_4]
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
    print(f"✅ Capítulo 5 — Aplicaciones Parciales listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
