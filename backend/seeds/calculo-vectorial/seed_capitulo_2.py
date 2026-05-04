"""
Seed del curso Cálculo Vectorial — Capítulo 2: Integrales de Línea.
6 lecciones:
  2.1 Campos vectoriales y escalares
  2.2 Integral de línea en campo escalar
  2.3 Integral de línea en campo vectorial
  2.4 Teorema fundamental para integrales de línea
  2.5 Teorema de Green
  2.6 Teorema vectorial de Green (operadores div, rot)

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
# 2.1 Campos vectoriales y escalares
# =====================================================================
def lesson_2_1():
    blocks = [
        b("texto", body_md=(
            "Un **campo escalar** asigna un número a cada punto del espacio (temperatura en una habitación, "
            "presión atmosférica). Un **campo vectorial** asigna un vector (velocidad del viento, fuerza "
            "gravitacional). Ambos son la base del cálculo vectorial — todo el resto del curso integra "
            "sobre estos objetos.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Distinguir y graficar **campos escalares** y **vectoriales**.\n"
            "- Reconocer ejemplos físicos clásicos.\n"
            "- Calcular el **gradiente** $\\nabla f$ (de escalar a vectorial).\n"
            "- Comprender los conceptos de **divergencia** y **rotacional** (preludio para 2.6)."
        )),

        b("definicion",
          titulo="Campo escalar y campo vectorial",
          body_md=(
              "**Campo escalar:** una función $f: D \\subset \\mathbb{R}^n \\to \\mathbb{R}$. A cada punto le asigna un **número**.\n\n"
              "**Campo vectorial:** una función $\\vec{F}: D \\subset \\mathbb{R}^n \\to \\mathbb{R}^n$. A cada punto le asigna un **vector**.\n\n"
              "**En $\\mathbb{R}^2$:** $\\vec{F}(x, y) = \\langle P(x, y), Q(x, y) \\rangle$.\n\n"
              "**En $\\mathbb{R}^3$:** $\\vec{F}(x, y, z) = \\langle P(x, y, z), Q(x, y, z), R(x, y, z) \\rangle$.\n\n"
              "Las **componentes** $P, Q, R$ son a su vez campos escalares."
          )),

        formulas(
            titulo="Ejemplos físicos típicos",
            body=(
                "**Campos escalares:**\n\n"
                "| Campo | Significado |\n|---|---|\n"
                "| $T(x, y, z)$ | Temperatura |\n"
                "| $p(x, y, z)$ | Presión |\n"
                "| $\\rho(x, y, z)$ | Densidad |\n"
                "| $\\phi$ (potencial) | Energía por unidad de masa/carga |\n\n"
                "**Campos vectoriales:**\n\n"
                "| Campo | Fórmula típica | Significado |\n|---|---|---|\n"
                "| $\\vec{v}(x, y, z, t)$ | — | Velocidad de un fluido |\n"
                "| $\\vec{F}_{grav}$ | $-\\dfrac{GMm}{\\|\\vec{r}\\|^3}\\vec{r}$ | Fuerza gravitacional |\n"
                "| $\\vec{E}$ | $\\dfrac{kQ}{\\|\\vec{r}\\|^3}\\vec{r}$ | Campo eléctrico |\n"
                "| $\\nabla T$ | — | Dirección de máximo crecimiento de la temperatura |"
            ),
        ),

        fig(
            "Cuatro campos vectoriales clásicos en el plano. Grilla 2x2. PANEL ARRIBA-IZQ: campo "
            "constante F = (1, 0), todas las flechas iguales apuntando a la derecha. PANEL "
            "ARRIBA-DER: campo radial F(x, y) = (x, y), flechas saliendo del origen. PANEL "
            "ABAJO-IZQ: campo de rotación F(x, y) = (-y, x), flechas tangentes a círculos "
            "concéntricos (movimiento antihorario). PANEL ABAJO-DER: campo gravitacional F = "
            "-(x, y)/(x²+y²)^(3/2), flechas apuntando al origen con magnitud decreciente. Cada "
            "flecha en color teal con longitud proporcional a la magnitud. Etiquetas. " + STYLE
        ),

        b("definicion",
          titulo="Operadores diferenciales — vista preliminar",
          body_md=(
              "Tres operadores fundamentales transforman entre escalares y vectoriales. Aquí los presentamos; los desarrollaremos en lecciones posteriores y en el cap. 3 de Cálculo Multivariable (donde gradiente ya se vio).\n\n"
              "**Gradiente** ($\\nabla$): escalar → vectorial.\n\n"
              "$$\\nabla f = \\langle f_x, f_y, f_z \\rangle$$\n\n"
              "**Divergencia** ($\\nabla \\cdot$): vectorial → escalar.\n\n"
              "$$\\nabla \\cdot \\vec{F} = P_x + Q_y + R_z$$\n\n"
              "Mide cuánto **'sale' el flujo** de cada punto. Positiva = fuente; negativa = sumidero.\n\n"
              "**Rotacional** ($\\nabla \\times$): vectorial → vectorial (solo en 3D).\n\n"
              "$$\\nabla \\times \\vec{F} = \\langle R_y - Q_z, P_z - R_x, Q_x - P_y \\rangle$$\n\n"
              "Mide cuánto **'gira' el campo** en cada punto. Vector cero = irrotacional."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular gradiente, divergencia y rotacional",
          problema_md=(
              "Para $f(x, y, z) = x^2 y + z$ y $\\vec{F}(x, y, z) = \\langle xz, y^2, xy \\rangle$, calcular $\\nabla f$, $\\nabla \\cdot \\vec{F}$ y $\\nabla \\times \\vec{F}$."
          ),
          pasos=[
              {"accion_md": "**Gradiente:** $\\nabla f = \\langle 2xy, x^2, 1 \\rangle$.",
               "justificacion_md": "Parciales componente a componente.",
               "es_resultado": False},
              {"accion_md": "**Divergencia:** $\\nabla \\cdot \\vec{F} = \\partial_x(xz) + \\partial_y(y^2) + \\partial_z(xy) = z + 2y + 0 = z + 2y$.",
               "justificacion_md": "Suma de las parciales 'diagonales'.",
               "es_resultado": False},
              {"accion_md": "**Rotacional** (con la regla nemotécnica del determinante):\n\n"
                            "$\\nabla \\times \\vec{F} = \\langle \\partial_y(xy) - \\partial_z(y^2), \\partial_z(xz) - \\partial_x(xy), \\partial_x(y^2) - \\partial_y(xz) \\rangle$\n\n"
                            "$= \\langle x - 0, x - y, 0 - 0 \\rangle = \\langle x, x - y, 0 \\rangle$.",
               "justificacion_md": "Cada componente sigue el patrón cíclico.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Campos conservativos",
          body_md=(
              "Un campo vectorial $\\vec{F}$ es **conservativo** si existe un campo escalar $f$ (llamado **función potencial**) tal que:\n\n"
              "$$\\vec{F} = \\nabla f$$\n\n"
              "En palabras: $\\vec{F}$ es el gradiente de algún potencial.\n\n"
              "**Por qué importan:** los campos conservativos tienen propiedades extraordinarias — independencia del camino, energía mecánica conservada, etc. Toda la lección 2.4 está dedicada a ellos.\n\n"
              "**Ejemplo físico:** la fuerza gravitacional es conservativa, con potencial $-\\dfrac{GMm}{r}$. La fuerza de fricción **no** es conservativa.\n\n"
              "**Test en $\\mathbb{R}^3$:** $\\vec{F}$ conservativo $\\implies$ $\\nabla \\times \\vec{F} = \\vec{0}$. La recíproca vale en regiones simplemente conexas."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El gradiente de un campo escalar es:",
                  "opciones_md": [
                      "Un escalar",
                      "Un campo vectorial",
                      "Un campo escalar",
                      "Una matriz",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\nabla f = \\langle f_x, f_y, f_z \\rangle$ — un vector en cada punto.",
                  "explicacion_md": (
                      "$\\nabla$ es operador escalar→vectorial. **Divergencia** es vectorial→escalar; **rotacional** es vectorial→vectorial."
                  ),
              },
              {
                  "enunciado_md": "Para que $\\vec{F}$ sea conservativo en una región simplemente conexa de $\\mathbb{R}^3$:",
                  "opciones_md": [
                      "$\\nabla \\cdot \\vec{F} = 0$",
                      "$\\nabla \\times \\vec{F} = \\vec{0}$",
                      "$\\vec{F} = \\vec{0}$",
                      "$\\vec{F}$ es constante",
                  ],
                  "correcta": "B",
                  "pista_md": "Conservativo = gradiente. El rotacional de un gradiente es cero (identidad).",
                  "explicacion_md": (
                      "$\\nabla \\times (\\nabla f) = \\vec{0}$ siempre — identidad clásica. Por eso un campo conservativo tiene rotacional cero."
                  ),
              },
          ]),

        ej(
            titulo="Identificar campo conservativo",
            enunciado=(
                "¿Es $\\vec{F}(x, y) = \\langle 2xy, x^2 + 3y^2 \\rangle$ conservativo? Si sí, halla un potencial."
            ),
            pistas=[
                "Test: $\\partial Q/\\partial x = \\partial P/\\partial y$.",
                "Si lo es, integrar $P$ respecto a $x$ y ajustar.",
            ],
            solucion=(
                "$\\partial P/\\partial y = 2x$. $\\partial Q/\\partial x = 2x$. **Iguales** → conservativo.\n\n"
                "**Potencial:** $f_x = 2xy$ → $f = x^2 y + g(y)$. $f_y = x^2 + g'(y) = x^2 + 3y^2$ → $g'(y) = 3y^2$ → $g(y) = y^3 + C$.\n\n"
                "**Resultado:** $f(x, y) = x^2 y + y^3 + C$."
            ),
        ),

        ej(
            titulo="Calcular divergencia",
            enunciado=(
                "Para el campo radial $\\vec{F}(x, y, z) = \\langle x, y, z \\rangle$, calcula $\\nabla \\cdot \\vec{F}$."
            ),
            pistas=[
                "$\\partial_x(x) + \\partial_y(y) + \\partial_z(z)$.",
            ],
            solucion=(
                "$\\nabla \\cdot \\vec{F} = 1 + 1 + 1 = 3$.\n\n"
                "**Interpretación:** divergencia constante positiva — el campo radial expande uniformemente. (En contexto de fluidos: cada punto es una 'fuente' del mismo tamaño.)"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir campo escalar con vectorial.** Escalar = número en cada punto; vectorial = vector.",
              "**Confundir gradiente con divergencia.** $\\nabla f$ y $\\nabla \\cdot \\vec{F}$ tienen notaciones similares pero son operadores diferentes (no requieren los mismos objetos).",
              "**Aplicar rotacional en 2D directamente.** El rotacional 'puro' es 3D; en 2D se usa la fórmula reducida $Q_x - P_y$ (componente $z$).",
              "**Olvidar que conservativo implica $\\nabla \\times \\vec{F} = \\vec{0}$, pero la recíproca requiere región simplemente conexa.**",
              "**Usar la regla del producto en $\\nabla \\cdot \\vec{F}$ donde no aplica.** $\\nabla \\cdot$ es suma de parciales individuales, no producto.",
          ]),

        b("resumen",
          puntos_md=[
              "**Campo escalar:** $f: \\mathbb{R}^n \\to \\mathbb{R}$. **Vectorial:** $\\vec{F}: \\mathbb{R}^n \\to \\mathbb{R}^n$.",
              "**Gradiente** $\\nabla f$ — escalar → vectorial.",
              "**Divergencia** $\\nabla \\cdot \\vec{F} = P_x + Q_y + R_z$ — vectorial → escalar.",
              "**Rotacional** $\\nabla \\times \\vec{F}$ — vectorial → vectorial (en 3D).",
              "**Conservativo:** $\\vec{F} = \\nabla f$ para algún potencial $f$.",
              "**Test:** $\\vec{F}$ conservativo $\\implies \\nabla \\times \\vec{F} = \\vec{0}$.",
              "**Próxima lección:** integral de línea en un campo escalar.",
          ]),
    ]
    return {
        "id": "lec-vec-2-1-campos",
        "title": "Campos vectoriales y escalares",
        "description": "Definición de campos, ejemplos físicos, gradiente, divergencia, rotacional y campos conservativos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 2.2 Integral de línea en campo escalar
# =====================================================================
def lesson_2_2():
    blocks = [
        b("texto", body_md=(
            "La **integral de línea de un campo escalar** generaliza la integral de una variable a "
            "**curvas en el espacio**. En lugar de integrar sobre $[a, b]$ del eje $x$, integramos sobre "
            "una curva $C$. Si $f$ representa densidad lineal, la integral da la **masa total** de un "
            "alambre con esa forma; si $f$ representa altura, da el área de una **muralla** sobre la curva.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir $\\int_C f \\, ds$ y calcularla con parametrización.\n"
            "- Comprender la **interpretación geométrica** (área de muralla).\n"
            "- Aplicar a problemas físicos: masa, centro de masa de un alambre.\n"
            "- Comprobar la **invarianza** bajo reparametrización."
        )),

        b("definicion",
          titulo="Integral de línea en campo escalar",
          body_md=(
              "Sea $C$ una curva suave parametrizada por $\\vec{r}(t)$, $t \\in [a, b]$, y $f$ un campo escalar definido sobre $C$. La **integral de línea** de $f$ sobre $C$ es:\n\n"
              "$$\\int_C f \\, ds = \\int_a^b f(\\vec{r}(t)) \\, \\|\\vec{r}'(t)\\| \\, dt$$\n\n"
              "**Notación:** $ds = \\|\\vec{r}'(t)\\| \\, dt$ es el elemento de **longitud de arco**. Es el factor que ya vimos en la longitud de curva (lección 1.4).\n\n"
              "**Caso especial $f \\equiv 1$:** $\\int_C 1 \\, ds = $ **longitud** de $C$. La integral de línea generaliza la longitud."
          )),

        b("intuicion",
          titulo="Geometría: área de muralla sobre la curva",
          body_md=(
              "Imagina la curva $C$ en el plano $xy$ y el campo $f(x, y) \\geq 0$ como **altura**. Construye una 'muralla' vertical sobre $C$ con altura $f(x, y)$ en cada punto.\n\n"
              "$$\\int_C f \\, ds = \\text{área de la muralla}$$\n\n"
              "Cada elemento $f(\\vec{r}) \\, ds$ es el área de un trozo de muralla de altura $f$ y ancho infinitesimal $ds$. Sumando con la integral, área total.\n\n"
              "**Comparación con integral 1D:** $\\int_a^b f(x) \\, dx$ es el caso particular donde $C$ es un segmento del eje $x$ — entonces $ds = dx$."
          )),

        b("ejemplo_resuelto",
          titulo="Integral sobre un círculo",
          problema_md=(
              "Calcular $\\int_C (x + y) \\, ds$ donde $C$ es el cuarto del círculo unitario $x^2 + y^2 = 1$ en el primer cuadrante."
          ),
          pasos=[
              {"accion_md": "**Parametrizar:** $\\vec{r}(t) = \\langle \\cos t, \\sin t \\rangle$, $t \\in [0, \\pi/2]$.\n\n"
                            "$\\vec{r}'(t) = \\langle -\\sin t, \\cos t \\rangle$, $\\|\\vec{r}'\\| = 1$ (rapidez unitaria — círculo unitario).",
               "justificacion_md": "Parametrización estándar.",
               "es_resultado": False},
              {"accion_md": "**Sustituir** en la fórmula:\n\n"
                            "$\\int_C (x + y) \\, ds = \\int_0^{\\pi/2} (\\cos t + \\sin t) \\cdot 1 \\, dt = [\\sin t - \\cos t]_0^{\\pi/2}$\n\n"
                            "$= (1 - 0) - (0 - 1) = 2$.",
               "justificacion_md": "Cálculo directo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Masa de un alambre helicoidal",
          problema_md=(
              "Un alambre con forma de hélice $\\vec{r}(t) = \\langle \\cos t, \\sin t, t \\rangle$ con $t \\in [0, 2\\pi]$ tiene densidad $\\rho(x, y, z) = z$. Calcular su masa."
          ),
          pasos=[
              {"accion_md": "**Masa:** $M = \\int_C \\rho \\, ds$.\n\n"
                            "$\\|\\vec{r}'\\| = \\sqrt{2}$ (constante para esta hélice).",
               "justificacion_md": "Generalización 3D del concepto de masa en una curva.",
               "es_resultado": False},
              {"accion_md": "$M = \\int_0^{2\\pi} t \\cdot \\sqrt{2} \\, dt = \\sqrt{2} \\cdot \\dfrac{(2\\pi)^2}{2} = 2\\pi^2 \\sqrt{2}$.",
               "justificacion_md": "**Numéricamente:** $\\approx 27.9$ unidades de masa.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Invarianza bajo reparametrización",
          enunciado_md=(
              "$\\int_C f \\, ds$ **no depende** de la parametrización elegida (mientras sea una parametrización suave de la misma curva $C$, en cualquier dirección).\n\n"
              "Es una propiedad **geométrica** de la curva y el campo, no del cómo se la recorre.\n\n"
              "**Atención** (preview de 2.3): la integral de línea en campo **vectorial** sí depende de la dirección — invertir el sentido cambia el signo."
          ),
          demostracion_md=(
              "Por cambio de variable, $ds$ se transforma exactamente para compensar cualquier reparametrización. Lo vimos para longitud de arco (lección 1.4); el mismo argumento aplica con $f$ adentro."
          )),

        b("definicion",
          titulo="Centro de masa de un alambre",
          body_md=(
              "Si un alambre tiene densidad $\\rho(x, y, z)$, su **centro de masa** está en:\n\n"
              "$$\\bar{x} = \\dfrac{1}{M} \\int_C x \\rho \\, ds, \\quad \\bar{y} = \\dfrac{1}{M} \\int_C y \\rho \\, ds, \\quad \\bar{z} = \\dfrac{1}{M} \\int_C z \\rho \\, ds$$\n\n"
              "donde $M = \\int_C \\rho \\, ds$ es la masa total. Es el análogo 1D del centro de masa de una lámina (Cálculo Multivariable 7.1).\n\n"
              "**Para densidad constante** $\\rho_0$: el **centroide** depende solo de la geometría de la curva."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\int_C 1 \\, ds$ es:",
                  "opciones_md": [
                      "Cero",
                      "El área bajo $C$",
                      "La longitud de $C$",
                      "El perímetro de la región",
                  ],
                  "correcta": "C",
                  "pista_md": "$ds$ es el elemento de longitud de arco.",
                  "explicacion_md": (
                      "Integrar $1 \\cdot ds$ a lo largo de $C$ da la suma de longitudes infinitesimales = longitud total."
                  ),
              },
              {
                  "enunciado_md": "Si invertimos la dirección de $C$, $\\int_C f \\, ds$:",
                  "opciones_md": [
                      "Cambia de signo",
                      "No cambia",
                      "Se vuelve cero",
                      "Se duplica",
                  ],
                  "correcta": "B",
                  "pista_md": "$ds > 0$ siempre, no depende de dirección.",
                  "explicacion_md": (
                      "**No cambia.** $ds$ es un escalar positivo. Invertir dirección no afecta. **(Lo que sí cambia es la integral vectorial $\\int F \\cdot d\\vec{r}$.)**"
                  ),
              },
          ]),

        ej(
            titulo="Integral sobre segmento",
            enunciado=(
                "Calcula $\\int_C xy \\, ds$ donde $C$ es el segmento del origen al punto $(3, 4)$."
            ),
            pistas=[
                "Parametriza con $\\vec{r}(t) = \\langle 3t, 4t \\rangle$, $t \\in [0, 1]$.",
                "$\\|\\vec{r}'\\| = \\sqrt{9 + 16} = 5$ (longitud del segmento es 5).",
                "$xy = (3t)(4t) = 12t^2$.",
            ],
            solucion=(
                "$\\int_0^1 12t^2 \\cdot 5 \\, dt = 60 \\cdot 1/3 = 20$."
            ),
        ),

        ej(
            titulo="Centro de masa de un semicírculo",
            enunciado=(
                "Un alambre semicircular $x^2 + y^2 = 1$, $y \\geq 0$, tiene densidad constante. "
                "Calcula su centroide."
            ),
            pistas=[
                "Parametriza: $\\vec{r}(t) = \\langle \\cos t, \\sin t \\rangle$, $t \\in [0, \\pi]$.",
                "Longitud (masa): $L = \\pi$.",
                "Por simetría, $\\bar{x} = 0$. Calcula $\\bar{y}$.",
            ],
            solucion=(
                "$\\bar{x} = 0$ por simetría.\n\n"
                "$\\bar{y} = \\dfrac{1}{\\pi} \\int_0^\\pi \\sin t \\cdot 1 \\, dt = \\dfrac{1}{\\pi}[-\\cos t]_0^\\pi = \\dfrac{2}{\\pi}$.\n\n"
                "**Resultado:** centroide $\\left(0, \\dfrac{2}{\\pi}\\right) \\approx (0, 0.637)$. **Compárese:** centroide del **semidisco** (lección 7.1 Cálc Mult): $(0, 4/(3\\pi)) \\approx (0, 0.424)$ — distinto, porque el alambre es solo el borde, no el área."
            ),
        ),

        fig(
            "Curva C en el plano R^2, ejes x y, dibujada en color teal #06b6d4. Sobre la curva se "
            "levanta una 'cortina' vertical cuya altura en cada punto es f(x,y), formando una "
            "superficie con sombreado teal degradado (más oscuro arriba, claro abajo). Interpretación "
            "visual: el área de la cortina equivale a ∫_C f ds. Etiquetas C, f(x,y), ds en ámbar "
            "#f59e0b. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $\\|\\vec{r}'(t)\\|$.** $ds = \\|\\vec{r}'\\| dt$, no $dt$.",
              "**Confundir $f \\, ds$ con $\\vec{F} \\cdot d\\vec{r}$.** El primero es escalar, el segundo es producto punto (lección 2.3).",
              "**Cambiar el signo al invertir la curva.** Solo aplica a integrales vectoriales.",
              "**No verificar que $f$ está definido sobre $C$.** Si $C$ pasa por una singularidad de $f$, la integral puede no existir.",
              "**Aplicar parametrización con $\\|\\vec{r}'\\|$ variable** sin reconocer que $ds$ ya incluye ese factor.",
          ]),

        b("resumen",
          puntos_md=[
              "**Integral de línea escalar:** $\\int_C f \\, ds = \\int_a^b f(\\vec{r}(t)) \\|\\vec{r}'(t)\\| \\, dt$.",
              "**$ds = \\|\\vec{r}'(t)\\| \\, dt$** — elemento de longitud de arco.",
              "**Caso $f = 1$:** longitud de $C$.",
              "**Geometría:** área de la muralla sobre $C$.",
              "**Invariante** bajo reparametrización (incluyendo inversión de dirección).",
              "**Aplicaciones:** masa, centro de masa de un alambre.",
              "**Próxima lección:** integral de línea de campos vectoriales — el trabajo realizado por una fuerza.",
          ]),
    ]
    return {
        "id": "lec-vec-2-2-linea-escalar",
        "title": "Integral de línea en campo escalar",
        "description": "$\\int_C f \\, ds$, geometría como área de muralla, masa y centro de masa de alambres.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# 2.3 Integral de línea en campo vectorial
# =====================================================================
def lesson_2_3():
    blocks = [
        b("texto", body_md=(
            "La **integral de línea de un campo vectorial** captura el **trabajo** realizado por una fuerza "
            "$\\vec{F}$ sobre una partícula que se mueve a lo largo de una curva $C$. La fórmula recoge solo "
            "la componente de la fuerza **alineada con el movimiento**, ignorando la componente perpendicular "
            "(que no hace trabajo).\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y calcular $\\int_C \\vec{F} \\cdot d\\vec{r}$.\n"
            "- Manejar las **dos notaciones**: $\\vec{F} \\cdot d\\vec{r}$ y $P \\, dx + Q \\, dy + R \\, dz$.\n"
            "- Comprender que **la dirección de la curva importa** (cambia el signo).\n"
            "- Calcular **trabajo** y **flujo** en aplicaciones físicas."
        )),

        b("definicion",
          titulo="Integral de línea en campo vectorial",
          body_md=(
              "Sea $\\vec{F}$ un campo vectorial continuo sobre una curva suave $C$ parametrizada por $\\vec{r}(t)$, $t \\in [a, b]$:\n\n"
              "$$\\int_C \\vec{F} \\cdot d\\vec{r} = \\int_a^b \\vec{F}(\\vec{r}(t)) \\cdot \\vec{r}'(t) \\, dt$$\n\n"
              "**Notación equivalente** (escribiendo $d\\vec{r} = \\langle dx, dy, dz \\rangle$):\n\n"
              "$$\\int_C \\vec{F} \\cdot d\\vec{r} = \\int_C P \\, dx + Q \\, dy + R \\, dz$$\n\n"
              "donde $\\vec{F} = \\langle P, Q, R \\rangle$.\n\n"
              "**Diferencia clave con la escalar:** **producto punto** entre $\\vec{F}$ y $\\vec{r}'$, no producto con la magnitud."
          )),

        b("intuicion",
          titulo="Trabajo: solo la componente alineada importa",
          body_md=(
              "**$\\vec{F} \\cdot \\vec{T} \\, ds$** es la fórmula desglosada. $\\vec{T} = \\vec{r}'/\\|\\vec{r}'\\|$ es el tangente unitario.\n\n"
              "El producto punto $\\vec{F} \\cdot \\vec{T}$ es la **componente de $\\vec{F}$ en la dirección del movimiento**. Si $\\vec{F} \\perp \\vec{T}$, no hace trabajo.\n\n"
              "**Ejemplo físico:** un planeta orbitando una estrella. La fuerza gravitacional es radial (perpendicular a la velocidad tangencial). El trabajo neto en una órbita circular es **cero** — por eso la energía cinética se conserva.\n\n"
              "**Físicamente:** $W = \\int_C \\vec{F} \\cdot d\\vec{r}$ generaliza $W = F \\cdot d$ del caso 1D con fuerza constante."
          )),

        b("ejemplo_resuelto",
          titulo="Trabajo de un campo a lo largo de una recta",
          problema_md=(
              "Calcular el trabajo realizado por $\\vec{F}(x, y) = \\langle x, x + y \\rangle$ sobre la partícula que va de $(0, 0)$ a $(2, 4)$ en línea recta."
          ),
          pasos=[
              {"accion_md": "**Parametrizar:** $\\vec{r}(t) = \\langle 2t, 4t \\rangle$, $t \\in [0, 1]$. $\\vec{r}'(t) = \\langle 2, 4 \\rangle$.",
               "justificacion_md": "Recta del origen a $(2, 4)$.",
               "es_resultado": False},
              {"accion_md": "**Evaluar $\\vec{F}$ en la curva:** $\\vec{F}(\\vec{r}(t)) = \\langle 2t, 2t + 4t \\rangle = \\langle 2t, 6t \\rangle$.\n\n"
                            "**Producto punto:** $\\vec{F} \\cdot \\vec{r}' = (2t)(2) + (6t)(4) = 4t + 24t = 28t$.",
               "justificacion_md": "Sustituir y aplicar producto punto.",
               "es_resultado": False},
              {"accion_md": "$W = \\int_0^1 28t \\, dt = 14$.",
               "justificacion_md": "**Lección:** la fórmula es siempre la misma — parametrizar, evaluar $\\vec{F}$ en la curva, producto punto, integrar.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Misma fuerza, distinto camino",
          problema_md=(
              "Repetir con $\\vec{F}(x, y) = \\langle x, x + y \\rangle$ pero por la trayectoria $C_2$: parábola $y = x^2$ desde $(0, 0)$ a $(2, 4)$."
          ),
          pasos=[
              {"accion_md": "**Parametrizar:** $\\vec{r}(t) = \\langle t, t^2 \\rangle$, $t \\in [0, 2]$. $\\vec{r}'(t) = \\langle 1, 2t \\rangle$.",
               "justificacion_md": "$y = x^2$ con $x = t$.",
               "es_resultado": False},
              {"accion_md": "**$\\vec{F}$ en la curva:** $\\vec{F}(\\vec{r}(t)) = \\langle t, t + t^2 \\rangle$.\n\n"
                            "**Producto punto:** $\\vec{F} \\cdot \\vec{r}' = t \\cdot 1 + (t + t^2)(2t) = t + 2t^2 + 2t^3$.",
               "justificacion_md": "Análogo al anterior.",
               "es_resultado": False},
              {"accion_md": "$W = \\int_0^2 (t + 2t^2 + 2t^3) \\, dt = 2 + \\dfrac{16}{3} + 8 = \\dfrac{46}{3} \\approx 15.33$.",
               "justificacion_md": "**Lección importante:** distinto camino, **distinto trabajo** ($14$ vs $46/3$). **El trabajo de un campo arbitrario depende del camino.** Solo los **conservativos** son independientes del camino (lección 2.4).",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Dependencia del sentido",
          enunciado_md=(
              "Si $-C$ denota la curva $C$ recorrida en sentido **contrario**:\n\n"
              "$$\\int_{-C} \\vec{F} \\cdot d\\vec{r} = -\\int_C \\vec{F} \\cdot d\\vec{r}$$\n\n"
              "**Por qué:** invertir la dirección invierte el vector tangente $\\vec{T}$, así $\\vec{F} \\cdot \\vec{T}$ cambia de signo. La integral total cambia de signo.\n\n"
              "**Comparación con escalar:** $\\int_{-C} f \\, ds = \\int_C f \\, ds$ (no cambia)."
          )),

        b("definicion",
          titulo="Notación $\\int_C P \\, dx + Q \\, dy$",
          body_md=(
              "Una notación alternativa muy común:\n\n"
              "$$\\int_C P(x, y) \\, dx + Q(x, y) \\, dy = \\int_a^b [P(x(t), y(t)) x'(t) + Q(x(t), y(t)) y'(t)] \\, dt$$\n\n"
              "**Equivalente a** $\\int_C \\vec{F} \\cdot d\\vec{r}$ con $\\vec{F} = \\langle P, Q \\rangle$.\n\n"
              "**En esta notación**, $dx$ y $dy$ se interpretan como $x'(t) dt$ y $y'(t) dt$ — los diferenciales de las coordenadas, no de cualquier variable.\n\n"
              "**Es la notación clásica** que aparece en libros antiguos de física y en el teorema de Green."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\int_C \\vec{F} \\cdot d\\vec{r}$ es:",
                  "opciones_md": [
                      "Un vector",
                      "Un escalar",
                      "Un campo vectorial",
                      "Una matriz",
                  ],
                  "correcta": "B",
                  "pista_md": "Producto punto = escalar.",
                  "explicacion_md": (
                      "**Escalar.** El producto punto $\\vec{F} \\cdot d\\vec{r}$ da un escalar; la integral suma escalares."
                  ),
              },
              {
                  "enunciado_md": "Si $\\vec{F} \\perp \\vec{r}'$ en todo $C$, $\\int_C \\vec{F} \\cdot d\\vec{r} = ?$",
                  "opciones_md": [
                      "$0$",
                      "$\\|\\vec{F}\\| \\cdot $ longitud de $C$",
                      "$\\infty$",
                      "Depende del camino",
                  ],
                  "correcta": "A",
                  "pista_md": "$\\vec{F} \\cdot \\vec{r}' = \\|\\vec{F}\\|\\|\\vec{r}'\\|\\cos(90°) = 0$.",
                  "explicacion_md": (
                      "**Cero.** La fuerza no hace trabajo cuando es perpendicular al movimiento (caso del planeta en órbita circular)."
                  ),
              },
          ]),

        ej(
            titulo="Trabajo del campo radial",
            enunciado=(
                "Calcula $\\int_C \\vec{F} \\cdot d\\vec{r}$ donde $\\vec{F} = \\langle x, y \\rangle$ y $C$ es el círculo $x^2 + y^2 = 4$ recorrido antihorariamente."
            ),
            pistas=[
                "Parametriza: $\\vec{r}(t) = \\langle 2\\cos t, 2\\sin t \\rangle$, $t \\in [0, 2\\pi]$.",
                "$\\vec{r}'(t) = \\langle -2\\sin t, 2\\cos t \\rangle$.",
                "$\\vec{F} \\cdot \\vec{r}' = ?$",
            ],
            solucion=(
                "$\\vec{F}(\\vec{r}(t)) = \\langle 2\\cos t, 2\\sin t \\rangle$.\n\n"
                "$\\vec{F} \\cdot \\vec{r}' = (2\\cos t)(-2\\sin t) + (2\\sin t)(2\\cos t) = 0$.\n\n"
                "**$W = 0$.** **Geometría:** el campo radial es perpendicular al círculo en cada punto, así no hace trabajo neto."
            ),
        ),

        ej(
            titulo="Notación $P \\, dx + Q \\, dy$",
            enunciado=(
                "Calcula $\\int_C (xy) \\, dx + (x + y) \\, dy$ donde $C$ es $\\vec{r}(t) = \\langle t, t^2 \\rangle$, $t \\in [0, 1]$."
            ),
            pistas=[
                "$x = t, y = t^2$. $dx = dt, dy = 2t \\, dt$.",
                "Sustituye y combina.",
            ],
            solucion=(
                "$xy = t \\cdot t^2 = t^3$. $x + y = t + t^2$.\n\n"
                "$\\int_0^1 [t^3 + (t + t^2)(2t)] \\, dt = \\int_0^1 (t^3 + 2t^2 + 2t^3) \\, dt = \\int_0^1 (3t^3 + 2t^2) \\, dt = 3/4 + 2/3 = 17/12$."
            ),
        ),

        fig(
            "Plano R^2 con un campo vectorial F representado por flechitas grises distribuidas en "
            "una grilla suave. Una curva C en color teal #06b6d4 atraviesa el campo. En un punto "
            "de C, mostrar el vector tangente unitario T en teal grueso, y la proyección F·T "
            "destacada en ámbar #f59e0b (segmento sobre T). Etiqueta ∫_C F·dr = trabajo en "
            "tipografía clara. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\vec{F} \\cdot d\\vec{r}$ con $\\vec{F} \\, ds$.** El primero es producto punto (escalar); el segundo no tiene sentido sin alguna interpretación adicional.",
              "**Olvidar el cambio de signo** al invertir la dirección. Es la diferencia clave con la integral escalar.",
              "**Aplicar la notación $P \\, dx + Q \\, dy$ con $dx, dy$ como diferenciales independientes.** Aquí $dx = x'(t) dt$, $dy = y'(t) dt$ — están atados a la parametrización.",
              "**Asumir que el resultado es independiente del camino.** Solo lo es para campos conservativos (próxima lección).",
              "**Calcular $\\vec{F}(\\vec{r}(t))$ olvidando que es $\\vec{F}$ evaluado en el punto de la curva, no la composición.**",
          ]),

        b("resumen",
          puntos_md=[
              "**Integral de línea vectorial:** $\\int_C \\vec{F} \\cdot d\\vec{r} = \\int_a^b \\vec{F}(\\vec{r}(t)) \\cdot \\vec{r}'(t) \\, dt$.",
              "**Notación equivalente:** $\\int_C P \\, dx + Q \\, dy + R \\, dz$.",
              "**Interpretación:** trabajo realizado por $\\vec{F}$ a lo largo de $C$.",
              "**Solo la componente tangencial** aporta — perpendicular hace trabajo cero.",
              "**Depende de la dirección:** $\\int_{-C} = -\\int_C$.",
              "**Depende del camino** en general — independencia es una propiedad especial (próxima lección).",
              "**Próxima lección:** teorema fundamental — campos conservativos y la simplificación radical que producen.",
          ]),
    ]
    return {
        "id": "lec-vec-2-3-linea-vectorial",
        "title": "Integral de línea en campo vectorial",
        "description": "$\\int_C \\vec{F} \\cdot d\\vec{r}$, trabajo, dependencia del camino y notación clásica $P \\, dx + Q \\, dy$.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 2.4 Teorema fundamental para integrales de línea
# =====================================================================
def lesson_2_4():
    blocks = [
        b("texto", body_md=(
            "El **teorema fundamental para integrales de línea** generaliza el TFC del cálculo de una "
            "variable: si $\\vec{F}$ es **conservativo** ($\\vec{F} = \\nabla f$), su integral entre dos "
            "puntos depende **solo de los extremos**, no del camino. Eso simplifica drásticamente los "
            "cálculos y conecta con conceptos físicos centrales como **conservación de la energía**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar el TFC para integrales de línea: $\\int_C \\nabla f \\cdot d\\vec{r} = f(B) - f(A)$.\n"
            "- Reconocer **independencia del camino**.\n"
            "- Identificar campos conservativos con el **test del rotacional**.\n"
            "- **Construir** la función potencial $f$ desde $\\vec{F}$."
        )),

        b("teorema",
          nombre="TFC para integrales de línea",
          enunciado_md=(
              "Sea $C$ una curva suave de $A$ a $B$ y $f$ una función escalar con gradiente continuo. Entonces:\n\n"
              "$$\\int_C \\nabla f \\cdot d\\vec{r} = f(B) - f(A)$$\n\n"
              "**Solo importan los puntos extremos** — el camino es irrelevante.\n\n"
              "**Análogo 1D:** $\\int_a^b F'(x) \\, dx = F(b) - F(a)$. Aquí $F$ se reemplaza por $f$ (potencial) y la derivada por el gradiente."
          ),
          demostracion_md=(
              "Sea $\\vec{r}(t)$ parametrización de $C$ con $\\vec{r}(a) = A, \\vec{r}(b) = B$. Por la regla de la cadena:\n\n"
              "$\\dfrac{d}{dt}[f(\\vec{r}(t))] = \\nabla f(\\vec{r}(t)) \\cdot \\vec{r}'(t)$\n\n"
              "Integrando de $a$ a $b$:\n\n"
              "$\\int_a^b \\nabla f \\cdot \\vec{r}' \\, dt = f(\\vec{r}(b)) - f(\\vec{r}(a)) = f(B) - f(A)$. ∎"
          )),

        b("teorema",
          nombre="Equivalencias para campo conservativo",
          enunciado_md=(
              "Sea $\\vec{F}$ un campo vectorial continuo en una región **abierta y conexa** $D \\subset \\mathbb{R}^n$. Las siguientes son equivalentes:\n\n"
              "**1.** $\\vec{F}$ es **conservativo** ($\\vec{F} = \\nabla f$ para algún potencial $f$).\n\n"
              "**2.** $\\int_C \\vec{F} \\cdot d\\vec{r}$ es **independiente del camino** entre dos puntos cualesquiera.\n\n"
              "**3.** $\\oint_C \\vec{F} \\cdot d\\vec{r} = 0$ para **toda curva cerrada** $C$ contenida en $D$.\n\n"
              "**Test práctico (en regiones simplemente conexas):**\n\n"
              "- En $\\mathbb{R}^2$: $\\vec{F} = \\langle P, Q \\rangle$ es conservativo $\\iff$ $\\dfrac{\\partial P}{\\partial y} = \\dfrac{\\partial Q}{\\partial x}$.\n\n"
              "- En $\\mathbb{R}^3$: $\\vec{F}$ es conservativo $\\iff$ $\\nabla \\times \\vec{F} = \\vec{0}$."
          ),
          demostracion_md=(
              "**(1) ⇒ (2):** por TFC, $\\int_C = f(B) - f(A)$ depende solo de los extremos.\n\n"
              "**(2) ⇒ (3):** una curva cerrada va de $A$ a $A$, así $\\int = f(A) - f(A) = 0$.\n\n"
              "**(3) ⇒ (1):** dado un punto base $P_0$, definir $f(P) = \\int_{P_0}^P \\vec{F} \\cdot d\\vec{r}$ (no depende del camino por (2/3)). Verificar que $\\nabla f = \\vec{F}$ por TFC y derivando."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicar el TFC",
          problema_md=(
              "Sabiendo que $\\vec{F}(x, y) = \\langle 2xy, x^2 + 2y \\rangle$ es conservativo con potencial $f(x, y) = x^2 y + y^2$, calcular $\\int_C \\vec{F} \\cdot d\\vec{r}$ donde $C$ es **cualquier** curva de $(1, 2)$ a $(3, 4)$."
          ),
          pasos=[
              {"accion_md": "**Aplicar TFC directo:**\n\n"
                            "$\\int_C \\vec{F} \\cdot d\\vec{r} = f(3, 4) - f(1, 2) = (9 \\cdot 4 + 16) - (1 \\cdot 2 + 4) = 52 - 6 = 46$.",
               "justificacion_md": "Sin importar la forma de la curva — solo los extremos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Construir la función potencial",
          problema_md="Dado $\\vec{F}(x, y) = \\langle 2xy + 3, x^2 + 4y \\rangle$, verificar que es conservativo y hallar $f$.",
          pasos=[
              {"accion_md": "**Test:** $\\partial P/\\partial y = 2x$. $\\partial Q/\\partial x = 2x$. **Iguales** → conservativo.",
               "justificacion_md": "Test en $\\mathbb{R}^2$.",
               "es_resultado": False},
              {"accion_md": "**Construir $f$ desde $f_x = P$:**\n\n"
                            "$f = \\int (2xy + 3) \\, dx = x^2 y + 3x + g(y)$.\n\n"
                            "(La 'constante' de integración es función de $y$ porque integramos respecto a $x$.)",
               "justificacion_md": "Integramos $P$ tratando $y$ como constante.",
               "es_resultado": False},
              {"accion_md": "**Determinar $g(y)$ usando $f_y = Q$:**\n\n"
                            "$f_y = x^2 + g'(y) = x^2 + 4y$ → $g'(y) = 4y$ → $g(y) = 2y^2 + C$.",
               "justificacion_md": "Comparar con $Q$ y resolver.",
               "es_resultado": False},
              {"accion_md": "**Potencial:** $f(x, y) = x^2 y + 3x + 2y^2 + C$.\n\n"
                            "(La constante $C$ es arbitraria — diferentes valores son potenciales distintos pero todos sirven.)",
               "justificacion_md": "**Verificación:** $\\nabla f = \\langle 2xy + 3, x^2 + 4y \\rangle = \\vec{F}$. ✓",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Por qué física llama a $f$ 'potencial'?",
          body_md=(
              "Si $\\vec{F}$ es una **fuerza conservativa** (gravitacional, eléctrica, elástica), su potencial $f$ se interpreta físicamente como **energía potencial** (a un signo y constante).\n\n"
              "**Conservación de la energía:** el trabajo realizado por $\\vec{F}$ sobre una partícula es $W = f(B) - f(A)$. La energía cinética cambia por $W$. La **energía total** $E_c + E_p$ se conserva (porque $W$ se traslada de potencial a cinético sin pérdidas).\n\n"
              "**Para fuerzas no conservativas** (fricción): no hay potencial, la energía se 'disipa' como calor. **Por eso la fricción es 'no conservativa' en el sentido literal de la palabra.**\n\n"
              "**Convención en física:** usualmente $\\vec{F} = -\\nabla U$ donde $U$ es la energía potencial. El signo es por convención (las fuerzas apuntan hacia menor energía potencial)."
          )),

        b("ejemplo_resuelto",
          titulo="Curva cerrada en campo conservativo",
          problema_md=(
              "Sea $\\vec{F} = \\nabla f$ con $f(x, y) = e^{xy}$. Calcular $\\oint_C \\vec{F} \\cdot d\\vec{r}$ donde $C$ es cualquier curva cerrada en $\\mathbb{R}^2$."
          ),
          pasos=[
              {"accion_md": "**Por equivalencia (3):** $\\oint_C \\vec{F} \\cdot d\\vec{r} = 0$ para toda curva cerrada en un campo conservativo.",
               "justificacion_md": "Sin necesidad de calcular $\\vec{F}$ ni parametrizar $C$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\vec{F} = \\nabla f$ y $C$ va de $(0, 0)$ a $(1, 1)$, $\\int_C \\vec{F} \\cdot d\\vec{r} = ?$",
                  "opciones_md": [
                      "$f(0, 0) - f(1, 1)$",
                      "$f(1, 1) - f(0, 0)$",
                      "$f(0, 0) + f(1, 1)$",
                      "Depende de $C$",
                  ],
                  "correcta": "B",
                  "pista_md": "TFC: extremo final menos inicial.",
                  "explicacion_md": (
                      "$f(B) - f(A) = f(1,1) - f(0,0)$. **Independiente del camino.**"
                  ),
              },
              {
                  "enunciado_md": "Para $\\vec{F} = \\langle y, x \\rangle$, ¿es conservativo en $\\mathbb{R}^2$?",
                  "opciones_md": [
                      "Sí, $f = xy$.",
                      "No, $\\partial P/\\partial y \\neq \\partial Q/\\partial x$.",
                      "Sí, $f = (x+y)^2/2$.",
                      "No se puede saber.",
                  ],
                  "correcta": "A",
                  "pista_md": "Test: $\\partial_y(y) = 1, \\partial_x(x) = 1$. Iguales.",
                  "explicacion_md": (
                      "$P = y, Q = x$. $P_y = 1 = Q_x$. **Conservativo.** Potencial: $f = xy$ (verifica $\\nabla(xy) = \\langle y, x \\rangle$ ✓)."
                  ),
              },
          ]),

        ej(
            titulo="Test e independencia del camino",
            enunciado=(
                "Verifica si $\\vec{F}(x, y) = \\langle 3x^2 y^2, 2x^3 y \\rangle$ es conservativo. "
                "Si lo es, halla el potencial y calcula $\\int_C \\vec{F} \\cdot d\\vec{r}$ entre $(0, 0)$ y $(1, 2)$."
            ),
            pistas=[
                "Test: $P_y = ?, Q_x = ?$",
                "Si conservativo, integra $P$ respecto a $x$ y ajusta.",
            ],
            solucion=(
                "$P_y = 6x^2 y$. $Q_x = 6x^2 y$. **Conservativo.**\n\n"
                "**Potencial:** $f = \\int 3x^2 y^2 \\, dx = x^3 y^2 + g(y)$. $f_y = 2x^3 y + g'(y) = 2x^3 y$ → $g'(y) = 0$ → $g = $ const.\n\n"
                "$f(x, y) = x^3 y^2$.\n\n"
                "$\\int_C \\vec{F} \\cdot d\\vec{r} = f(1, 2) - f(0, 0) = 4 - 0 = 4$."
            ),
        ),

        ej(
            titulo="No conservativo",
            enunciado=(
                "Demuestra que $\\vec{F}(x, y) = \\langle -y, x \\rangle$ NO es conservativo en $\\mathbb{R}^2$, "
                "calculando $\\oint_C \\vec{F} \\cdot d\\vec{r}$ sobre el círculo unitario."
            ),
            pistas=[
                "Si fuera conservativo, la integral cerrada sería $0$.",
                "Parametriza el círculo: $\\vec{r}(t) = (\\cos t, \\sin t)$.",
            ],
            solucion=(
                "$\\vec{F}(\\vec{r}(t)) = \\langle -\\sin t, \\cos t \\rangle$. $\\vec{r}'(t) = \\langle -\\sin t, \\cos t \\rangle$.\n\n"
                "$\\vec{F} \\cdot \\vec{r}' = \\sin^2 t + \\cos^2 t = 1$.\n\n"
                "$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\int_0^{2\\pi} 1 \\, dt = 2\\pi \\neq 0$.\n\n"
                "**Por equivalencia (3), no es conservativo.** Verifica con el test: $P_y = -1, Q_x = 1$ — no iguales. ✓"
            ),
        ),

        fig(
            "Plano R^2 con dos puntos A y B marcados. Dos caminos distintos los conectan: uno en "
            "color teal #06b6d4 (curva ondulada) y otro en color ámbar #f59e0b (curva más recta). "
            "Encima del diagrama, mensaje destacado: 'si F = ∇f, entonces ∫_C F·dr = f(B) - f(A) "
            "— independiente del camino'. Etiquetas A, B, C₁, C₂ claras. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar TFC sin verificar que $\\vec{F}$ es conservativo.** Si no lo es, el resultado depende del camino.",
              "**Olvidar la 'constante' $g(y)$** al integrar $P$ respecto a $x$. La 'constante' es función de las otras variables.",
              "**Usar el test de $P_y = Q_x$ en regiones no simplemente conexas.** El campo $\\vec{F} = \\langle -y/(x^2+y^2), x/(x^2+y^2) \\rangle$ pasa el test pero **no** es conservativo en $\\mathbb{R}^2 \\setminus \\{0\\}$.",
              "**Confundir 'cerrado' con 'orientado'.** Una curva cerrada vuelve al inicio; la orientación es otra cuestión.",
              "**Pensar que el potencial es único.** Cualquier $f + C$ también es potencial.",
          ]),

        b("resumen",
          puntos_md=[
              "**TFC para línea:** $\\int_C \\nabla f \\cdot d\\vec{r} = f(B) - f(A)$ — independiente del camino.",
              "**Equivalencias para conservativo:** existencia de potencial ⟺ independencia del camino ⟺ integrales cerradas son cero.",
              "**Test rápido:** en $\\mathbb{R}^2$ simplemente conexa, $P_y = Q_x$. En $\\mathbb{R}^3$, $\\nabla \\times \\vec{F} = \\vec{0}$.",
              "**Construir $f$:** integrar $P$ respecto a $x$, ajustar con $f_y = Q$.",
              "**Física:** $f$ es energía potencial; conservación de energía mecánica.",
              "**Próxima lección:** Teorema de Green — para integrales sobre curvas cerradas en $\\mathbb{R}^2$.",
          ]),
    ]
    return {
        "id": "lec-vec-2-4-tfc-linea",
        "title": "Teorema fundamental para integrales de línea",
        "description": "TFC: $\\int \\nabla f \\cdot d\\vec{r} = f(B) - f(A)$. Independencia del camino, campos conservativos y construcción de potenciales.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 4,
    }


# =====================================================================
# 2.5 Teorema de Green
# =====================================================================
def lesson_2_5():
    blocks = [
        b("texto", body_md=(
            "El **teorema de Green** es uno de los resultados más importantes del cálculo vectorial. "
            "Conecta una **integral de línea** sobre la frontera cerrada de una región plana con una "
            "**integral doble** sobre el interior de la región. Es la versión 2D de los teoremas de Stokes "
            "y la divergencia (capítulo 3).\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Enunciar y aplicar el teorema de Green.\n"
            "- Identificar la **orientación positiva** (antihoraria) de la frontera.\n"
            "- Usar Green para calcular **áreas** como integral de línea.\n"
            "- Reconocer las hipótesis del teorema (curva simple, cerrada, suave por tramos)."
        )),

        b("teorema",
          nombre="Teorema de Green",
          enunciado_md=(
              "Sea $D$ una región en $\\mathbb{R}^2$ con frontera $C$ que es **simple, cerrada, suave por tramos** y orientada **positivamente** (antihorariamente, dejando $D$ a la izquierda). Sean $P, Q$ con derivadas parciales continuas en $D$. Entonces:\n\n"
              "$$\\oint_C P \\, dx + Q \\, dy = \\iint_D \\left(\\dfrac{\\partial Q}{\\partial x} - \\dfrac{\\partial P}{\\partial y}\\right) dA$$\n\n"
              "**Equivalentemente, en notación vectorial** con $\\vec{F} = \\langle P, Q \\rangle$:\n\n"
              "$$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_D (\\nabla \\times \\vec{F}) \\cdot \\vec{k} \\, dA$$\n\n"
              "donde $(\\nabla \\times \\vec{F}) \\cdot \\vec{k} = Q_x - P_y$ es la **componente $z$ del rotacional**."
          ),
          demostracion_md=(
              "Idea: para regiones rectangulares, separar en dos partes — una para $\\partial P/\\partial y$ y otra para $\\partial Q/\\partial x$ — y aplicar TFC en cada variable. Las integrales sobre los lados verticales/horizontales de la región generan exactamente la integral de línea sobre la frontera.\n\n"
              "Para regiones más generales (Tipo I y II): reducir mediante particiones a casos rectangulares. La demostración completa es técnica — lo importante es la **conexión** entre línea y doble."
          )),

        fig(
            "Teorema de Green ilustrado. Plano 2D con una región D acotada por una curva cerrada C, "
            "dibujada con orientación antihoraria (flecha indicando el sentido). La región interior "
            "D sombreada en color teal claro. Una flecha curva en la frontera indicando 'C "
            "antihoraria'. A un lado de la figura, la fórmula del teorema escrita: '∮_C P dx + Q "
            "dy = ∬_D (∂Q/∂x - ∂P/∂y) dA'. Etiquetas claras: 'D' (en el interior), 'C' (en la "
            "frontera). " + STYLE
        ),

        b("definicion",
          titulo="Orientación positiva",
          body_md=(
              "Una curva cerrada $C$ que rodea una región $D$ está **positivamente orientada** si, al recorrerla, **la región $D$ queda a la izquierda**.\n\n"
              "**Para regiones simples (sin agujeros):** orientación positiva = **antihoraria**.\n\n"
              "**Para regiones con agujeros:** la frontera externa va antihorariamente; las fronteras internas (alrededor de agujeros) van horariamente.\n\n"
              "**Convención de notación:** $\\oint_C$ asume orientación positiva. $\\oint_{-C}$ es la opuesta."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicar Green",
          problema_md=(
              "Calcular $\\oint_C (y^2) \\, dx + (3xy) \\, dy$ donde $C$ es la frontera del semidisco $D = \\{(x, y) : x^2 + y^2 \\leq 1, y \\geq 0\\}$, orientado positivamente."
          ),
          pasos=[
              {"accion_md": "**Aplicar Green:** $P = y^2, Q = 3xy$.\n\n"
                            "$Q_x - P_y = 3y - 2y = y$.",
               "justificacion_md": "El integrando del lado derecho.",
               "es_resultado": False},
              {"accion_md": "$\\oint_C P \\, dx + Q \\, dy = \\iint_D y \\, dA$.\n\n"
                            "**En polares** sobre el semidisco superior:\n\n"
                            "$\\iint_D y \\, dA = \\int_0^\\pi \\int_0^1 (r\\sin\\theta) r \\, dr \\, d\\theta = \\int_0^\\pi \\sin\\theta \\, d\\theta \\cdot \\dfrac{1}{3} = \\dfrac{2}{3}$.",
               "justificacion_md": "**Lección:** Green convierte una integral de línea (que requeriría parametrizar las dos partes de la frontera — diámetro y semicírculo) en una doble que se hace en polares.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Área como integral de línea",
          enunciado_md=(
              "El área de la región $D$ es:\n\n"
              "$$A(D) = \\oint_C x \\, dy = -\\oint_C y \\, dx = \\dfrac{1}{2} \\oint_C (x \\, dy - y \\, dx)$$\n\n"
              "**Aplicación de Green** con elecciones específicas:\n\n"
              "- $P = 0, Q = x$: $Q_x - P_y = 1$, así $\\oint x \\, dy = \\iint 1 \\, dA = A$.\n"
              "- $P = -y, Q = 0$: $Q_x - P_y = 1$, así $-\\oint y \\, dx = A$.\n"
              "- Promediando: $A = \\dfrac{1}{2} \\oint (x \\, dy - y \\, dx)$.\n\n"
              "**Útil cuando** la frontera está parametrizada bien pero la región es compleja."
          )),

        b("ejemplo_resuelto",
          titulo="Área de una elipse vía Green",
          problema_md="Calcular el área de la elipse $\\dfrac{x^2}{a^2} + \\dfrac{y^2}{b^2} = 1$ usando integral de línea.",
          pasos=[
              {"accion_md": "**Parametrizar:** $\\vec{r}(t) = \\langle a\\cos t, b\\sin t \\rangle$, $t \\in [0, 2\\pi]$.\n\n"
                            "$dx = -a\\sin t \\, dt$, $dy = b\\cos t \\, dt$.",
               "justificacion_md": "Parametrización clásica.",
               "es_resultado": False},
              {"accion_md": "$A = \\dfrac{1}{2} \\oint(x \\, dy - y \\, dx) = \\dfrac{1}{2} \\int_0^{2\\pi} [a\\cos t \\cdot b\\cos t - b\\sin t \\cdot (-a\\sin t)] \\, dt$\n\n"
                            "$= \\dfrac{1}{2} \\int_0^{2\\pi} ab(\\cos^2 t + \\sin^2 t) \\, dt = \\dfrac{ab}{2} \\cdot 2\\pi = \\pi a b$.",
               "justificacion_md": "**Resultado clásico:** área de elipse $= \\pi a b$. Recuperado mediante Green con un cálculo de una línea.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Green con regiones que tienen agujeros",
          body_md=(
              "Para una región $D$ con un agujero (anillo, p. ej.), la frontera $C$ tiene **dos componentes**: la externa $C_1$ (antihoraria) y la interna $C_2$ (horaria). El teorema de Green vale:\n\n"
              "$$\\oint_{C_1} \\vec{F} \\cdot d\\vec{r} + \\oint_{C_2} \\vec{F} \\cdot d\\vec{r} = \\iint_D (Q_x - P_y) \\, dA$$\n\n"
              "**Aplicación clásica:** mostrar que $\\oint \\vec{F} \\cdot d\\vec{r}$ es la misma para todas las curvas que rodean al agujero (si $\\nabla \\times \\vec{F} = 0$ en el anillo).\n\n"
              "**Es la forma de detectar comportamiento no-conservativo** alrededor de singularidades. El campo $\\vec{F} = \\langle -y, x \\rangle/(x^2 + y^2)$ pasa el test $P_y = Q_x$ pero da $\\oint = 2\\pi$ alrededor del origen — inconsistencia con conservatividad porque el dominio tiene un agujero."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Green relaciona integral de línea con:",
                  "opciones_md": [
                      "Otra integral de línea",
                      "Integral doble sobre la región",
                      "Integral triple",
                      "Suma finita",
                  ],
                  "correcta": "B",
                  "pista_md": "Conecta 1D (línea) con 2D (área).",
                  "explicacion_md": (
                      "**Línea sobre la frontera = doble sobre el interior.** Es la versión 2D de los teoremas que conectan dimensiones distintas (Stokes, divergencia)."
                  ),
              },
              {
                  "enunciado_md": "Para usar $A = \\dfrac{1}{2}\\oint(x \\, dy - y \\, dx)$, ¿qué se requiere?",
                  "opciones_md": [
                      "Que el campo sea conservativo.",
                      "Que la curva sea cerrada y orientada positivamente.",
                      "Que la región sea convexa.",
                      "Nada especial.",
                  ],
                  "correcta": "B",
                  "pista_md": "La fórmula sale de Green con $P, Q$ específicos.",
                  "explicacion_md": (
                      "Curva cerrada simple, suave por tramos, orientada positivamente — las hipótesis estándar de Green."
                  ),
              },
          ]),

        ej(
            titulo="Green sobre triángulo",
            enunciado=(
                "Calcula $\\oint_C (xy^2) \\, dx + (x^2 y + 2x) \\, dy$ donde $C$ es la frontera del triángulo con vértices $(0, 0), (1, 0), (1, 1)$ orientado positivamente."
            ),
            pistas=[
                "$P = xy^2, Q = x^2 y + 2x$.",
                "$Q_x - P_y = (2xy + 2) - 2xy = 2$.",
                "Área del triángulo: $1/2$.",
            ],
            solucion=(
                "$Q_x - P_y = 2$. Por Green:\n\n"
                "$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_D 2 \\, dA = 2 \\cdot A(D) = 2 \\cdot 1/2 = 1$.\n\n"
                "**Sin Green** habría que parametrizar tres lados — por Green es trivial."
            ),
        ),

        ej(
            titulo="Área usando integral de línea",
            enunciado=(
                "Calcula el área dentro de la curva $\\vec{r}(t) = \\langle \\cos^3 t, \\sin^3 t \\rangle$, $t \\in [0, 2\\pi]$ (astroide)."
            ),
            pistas=[
                "$x = \\cos^3 t, y = \\sin^3 t$.",
                "$dx = -3\\cos^2 t \\sin t \\, dt$, $dy = 3\\sin^2 t \\cos t \\, dt$.",
                "$A = \\dfrac{1}{2}\\oint(x \\, dy - y \\, dx)$.",
            ],
            solucion=(
                "$x \\, dy - y \\, dx = 3\\sin^2 t \\cos^4 t \\, dt + 3\\sin^4 t \\cos^2 t \\, dt = 3\\sin^2 t \\cos^2 t (\\cos^2 + \\sin^2) \\, dt = 3 \\sin^2 t \\cos^2 t \\, dt$.\n\n"
                "$= \\dfrac{3}{4}\\sin^2(2t) \\, dt$.\n\n"
                "$A = \\dfrac{1}{2}\\int_0^{2\\pi} \\dfrac{3}{4}\\sin^2(2t) \\, dt = \\dfrac{3}{8} \\cdot \\pi = \\dfrac{3\\pi}{8}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Green con curva no cerrada.** El teorema requiere $C$ cerrada.",
              "**Confundir orientación positiva con horaria.** Es **antihoraria** (mano izquierda apunta a $D$).",
              "**Usar Green con $P, Q$ no derivables en $D$.** Las parciales deben ser continuas.",
              "**Confundir Green con TFC.** TFC: campo conservativo, dos puntos. Green: cualquier campo, curva cerrada.",
              "**Olvidar el signo $-$** en $Q_x - P_y$. Es $\\partial Q/\\partial x$ menos $\\partial P/\\partial y$, no al revés.",
          ]),

        b("resumen",
          puntos_md=[
              "**Teorema de Green:** $\\oint_C P \\, dx + Q \\, dy = \\iint_D (Q_x - P_y) \\, dA$.",
              "**Hipótesis:** $C$ simple, cerrada, suave por tramos, orientada positivamente.",
              "**Orientación positiva = antihoraria** (región a la izquierda al avanzar).",
              "**Área como integral de línea:** $A = \\dfrac{1}{2} \\oint (x \\, dy - y \\, dx)$.",
              "**Conexión:** integra de 1D a 2D — versión plana de Stokes (cap. 3).",
              "**Próxima lección:** versión vectorial de Green — formas de circulación y flujo.",
          ]),
    ]
    return {
        "id": "lec-vec-2-5-green",
        "title": "Teorema de Green",
        "description": "Conexión entre $\\oint_C P \\, dx + Q \\, dy$ y $\\iint_D (Q_x - P_y) \\, dA$. Área como integral de línea.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 5,
    }


# =====================================================================
# 2.6 Teorema vectorial de Green
# =====================================================================
def lesson_2_6():
    blocks = [
        b("texto", body_md=(
            "El teorema de Green tiene **dos formulaciones vectoriales** que profundizan su significado físico: "
            "la **forma de circulación** (que conecta con el rotacional) y la **forma del flujo** (que "
            "conecta con la divergencia). Ambas son los **prototipos 2D** de los teoremas de Stokes y la "
            "divergencia que veremos en el capítulo 3.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Conocer y aplicar la **forma de circulación**: $\\oint \\vec{F} \\cdot \\vec{T} \\, ds = \\iint \\text{rot} \\vec{F} \\cdot \\vec{k} \\, dA$.\n"
            "- Conocer y aplicar la **forma del flujo**: $\\oint \\vec{F} \\cdot \\vec{n} \\, ds = \\iint \\text{div} \\vec{F} \\, dA$.\n"
            "- Comprender la **interpretación física** de cada una.\n"
            "- Anticipar las generalizaciones a 3D (Stokes y divergencia)."
        )),

        b("teorema",
          nombre="Forma de la circulación (rotacional)",
          enunciado_md=(
              "Para una región $D \\subset \\mathbb{R}^2$ con frontera $C$ orientada positivamente:\n\n"
              "$$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\oint_C \\vec{F} \\cdot \\vec{T} \\, ds = \\iint_D (\\nabla \\times \\vec{F}) \\cdot \\vec{k} \\, dA$$\n\n"
              "**Interpretación:** la **circulación** total de $\\vec{F}$ alrededor de $C$ equivale a la **suma de las micro-rotaciones** del campo en el interior. Si el campo gira en cada punto, la curva 'siente' la suma de esas rotaciones.\n\n"
              "**Para $\\vec{F} = \\langle P, Q \\rangle$:** $(\\nabla \\times \\vec{F}) \\cdot \\vec{k} = Q_x - P_y$ — exactamente lo que aparece en Green clásico.\n\n"
              "**Es Green** reescrito en lenguaje vectorial. **Generalización 3D:** teorema de Stokes."
          )),

        b("intuicion",
          titulo="Rotacional como medida de rotación local",
          body_md=(
              "Imagina un campo de velocidad de un fluido. **Pon una pequeña paleta de molino** en cada punto:\n\n"
              "- Si el campo hace girar la paleta en sentido antihorario: rotacional positivo en ese punto.\n"
              "- Sentido horario: rotacional negativo.\n"
              "- No gira: rotacional cero.\n\n"
              "**Velocidad angular de la paleta** $= \\dfrac{1}{2} (\\nabla \\times \\vec{F}) \\cdot \\vec{k}$ (en 2D).\n\n"
              "**Forma de circulación:** la circulación total alrededor de un loop = suma de las micro-rotaciones que el fluido hace adentro. **Es como contar cuántas vueltas dio el fluido en total**."
          )),

        b("teorema",
          nombre="Forma del flujo (divergencia)",
          enunciado_md=(
              "Para una región $D \\subset \\mathbb{R}^2$ con frontera $C$ orientada positivamente y $\\vec{n}$ el vector normal exterior unitario:\n\n"
              "$$\\oint_C \\vec{F} \\cdot \\vec{n} \\, ds = \\iint_D \\nabla \\cdot \\vec{F} \\, dA = \\iint_D (P_x + Q_y) \\, dA$$\n\n"
              "**Interpretación:** el **flujo neto** de $\\vec{F}$ a través de $C$ (lo que sale menos lo que entra) equivale a la **divergencia total** del campo en el interior. **Si el campo 'crea' fluido en cada punto, el total que sale por la frontera es la suma de esa creación.**\n\n"
              "**$\\vec{n} = \\langle T_y, -T_x \\rangle$** si $\\vec{T} = \\langle T_x, T_y \\rangle$ (rotación 90° horaria del tangente). En coordenadas: si $\\vec{r}(t) = \\langle x(t), y(t) \\rangle$, $\\vec{n} \\, ds = \\langle dy, -dx \\rangle$.\n\n"
              "**Generalización 3D:** teorema de la divergencia (Gauss)."
          ),
          demostracion_md=(
              "Aplicar Green clásico con un cambio de variables: tomar $\\tilde P = -Q$, $\\tilde Q = P$. Entonces $\\tilde Q_x - \\tilde P_y = P_x + Q_y = \\nabla \\cdot \\vec{F}$.\n\n"
              "Y $\\oint \\tilde P \\, dx + \\tilde Q \\, dy = \\oint -Q \\, dx + P \\, dy = \\oint \\vec{F} \\cdot \\vec{n} \\, ds$ (con $\\vec{n} \\, ds = \\langle dy, -dx \\rangle$)."
          )),

        b("intuicion",
          titulo="Divergencia como fuente local",
          body_md=(
              "**Imagina el campo como velocidad de un fluido:**\n\n"
              "- $\\nabla \\cdot \\vec{F} > 0$: hay una **fuente** allí — el fluido aparece.\n"
              "- $\\nabla \\cdot \\vec{F} < 0$: hay un **sumidero** — el fluido desaparece.\n"
              "- $\\nabla \\cdot \\vec{F} = 0$: incompresible — entra tanto como sale.\n\n"
              "**Forma del flujo:** el flujo neto que sale por la frontera = total de fuentes y sumideros adentro. **Conservación de masa local.**\n\n"
              "**Aplicación:** ecuación de continuidad de la mecánica de fluidos: $\\dfrac{\\partial \\rho}{\\partial t} + \\nabla \\cdot (\\rho \\vec{v}) = 0$ — versión diferencial de la conservación de masa."
          )),

        b("ejemplo_resuelto",
          titulo="Forma de circulación: aplicar Stokes 2D",
          problema_md=(
              "Calcular $\\oint_C \\vec{F} \\cdot d\\vec{r}$ donde $\\vec{F} = \\langle xy, x^2 + y \\rangle$ y $C$ es el círculo $x^2 + y^2 = 4$ orientado antihorario."
          ),
          pasos=[
              {"accion_md": "**Rotacional 2D:** $(\\nabla \\times \\vec{F}) \\cdot \\vec{k} = Q_x - P_y = 2x - x = x$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "**Por Green (forma circulación):**\n\n"
                            "$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_D x \\, dA$.\n\n"
                            "**Por simetría:** el disco $D$ es simétrico respecto al eje $y$, e $x$ es **impar** en $x$. Entonces $\\iint_D x \\, dA = 0$.",
               "justificacion_md": "Argumento de simetría — más rápido que calcular en polares.",
               "es_resultado": False},
              {"accion_md": "**$\\oint_C \\vec{F} \\cdot d\\vec{r} = 0$.**",
               "justificacion_md": "**Sin parametrizar el círculo:** Green + simetría dan la respuesta en una línea.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Forma del flujo",
          problema_md=(
              "Calcular el flujo de $\\vec{F} = \\langle x, y \\rangle$ a través del círculo $x^2 + y^2 = 1$ (saliente)."
          ),
          pasos=[
              {"accion_md": "**Divergencia:** $\\nabla \\cdot \\vec{F} = 1 + 1 = 2$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "**Por Green (forma flujo):**\n\n"
                            "$\\oint_C \\vec{F} \\cdot \\vec{n} \\, ds = \\iint_D 2 \\, dA = 2 \\cdot \\pi(1)^2 = 2\\pi$.",
               "justificacion_md": "Constante por área del disco.",
               "es_resultado": False},
              {"accion_md": "**Verificación intuitiva:** el campo radial $\\vec{F} = \\langle x, y \\rangle$ apunta hacia afuera con magnitud $r$. En el círculo $r = 1$, $\\vec{F} \\cdot \\vec{n} = 1$ (alineado con la normal). $\\oint = 1 \\cdot 2\\pi = 2\\pi$. ✓",
               "justificacion_md": "**Lección:** el campo radial $\\langle x, y \\rangle$ tiene **divergencia constante 2** — es 'incompresible negativo' uniformemente.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La forma del flujo de Green generaliza a 3D como:",
                  "opciones_md": [
                      "Teorema de Stokes",
                      "Teorema de la divergencia",
                      "Teorema de Green",
                      "TFC",
                  ],
                  "correcta": "B",
                  "pista_md": "Flujo a través de superficie cerrada = divergencia interior.",
                  "explicacion_md": (
                      "**Teorema de la divergencia** (Gauss): $\\oiint_S \\vec{F} \\cdot \\vec{n} \\, dS = \\iiint_V \\nabla \\cdot \\vec{F} \\, dV$. La forma del flujo es su versión plana."
                  ),
              },
              {
                  "enunciado_md": "Si $\\nabla \\cdot \\vec{F} = 0$ en todo $D$, $\\oint_C \\vec{F} \\cdot \\vec{n} \\, ds = ?$",
                  "opciones_md": [
                      "$0$",
                      "Área de $D$",
                      "Perímetro de $C$",
                      "Depende de $\\vec{F}$",
                  ],
                  "correcta": "A",
                  "pista_md": "Forma del flujo: $\\oint = \\iint \\nabla \\cdot \\vec{F} \\, dA$.",
                  "explicacion_md": (
                      "$\\iint_D 0 \\, dA = 0$. **Campo incompresible** $\\Rightarrow$ flujo neto cero por cualquier curva cerrada."
                  ),
              },
          ]),

        ej(
            titulo="Forma de circulación con simetría",
            enunciado=(
                "Calcula $\\oint_C \\vec{F} \\cdot d\\vec{r}$ donde $\\vec{F} = \\langle 2x + y, x^2 - y^2 \\rangle$ y $C$ es el círculo $x^2 + y^2 = 9$ antihorario."
            ),
            pistas=[
                "Rotacional: $Q_x - P_y = 2x - 1$.",
                "Por Green: $\\iint_D (2x - 1) \\, dA$.",
                "Por simetría, $\\iint x \\, dA = 0$ en el disco. $\\iint (-1) \\, dA = -A$.",
            ],
            solucion=(
                "$\\iint_D (2x - 1) \\, dA = 2 \\iint x \\, dA - \\iint 1 \\, dA = 0 - 9\\pi = -9\\pi$."
            ),
        ),

        ej(
            titulo="Flujo a través de elipse",
            enunciado=(
                "Calcula el flujo de $\\vec{F} = \\langle x^3, y^3 \\rangle$ a través de la elipse $\\dfrac{x^2}{4} + \\dfrac{y^2}{9} = 1$ (saliente)."
            ),
            pistas=[
                "$\\nabla \\cdot \\vec{F} = 3x^2 + 3y^2$.",
                "Por Green flujo: $\\iint_D 3(x^2 + y^2) \\, dA$ — usar parametrización elíptica o polares modificadas.",
            ],
            solucion=(
                "$\\nabla \\cdot \\vec{F} = 3x^2 + 3y^2$.\n\n"
                "$\\iint_D 3(x^2 + y^2) \\, dA$. Cambio de variable $x = 2u, y = 3v$ (Jacobiano $= 6$):\n\n"
                "$3 \\iint_{u^2+v^2 \\leq 1} (4u^2 + 9v^2) \\cdot 6 \\, du \\, dv = 18 \\iint (4u^2 + 9v^2) \\, dA$.\n\n"
                "En polares ($u = r\\cos\\theta, v = r\\sin\\theta$): $= 18 \\int_0^{2\\pi} \\int_0^1 (4r^2\\cos^2 + 9r^2 \\sin^2) r \\, dr \\, d\\theta = 18 \\cdot \\dfrac{1}{4} \\int_0^{2\\pi}(4\\cos^2\\theta + 9\\sin^2\\theta) \\, d\\theta = \\dfrac{18}{4} \\cdot 13\\pi = \\dfrac{117\\pi}{2}$."
            ),
        ),

        fig(
            "Plano R^2 con una región plana D sombreada en teal #06b6d4 claro, encerrada por una "
            "curva C orientada anti-horario (flecha ámbar #f59e0b sobre la curva indicando el "
            "sentido). A un lado, fórmula del teorema de Green: ∮_C(P dx + Q dy) = ∬_D(∂Q/∂x - "
            "∂P/∂y) dA. Etiquetas D, C, n exterior. Equivalencia visual entre la integral de línea "
            "y la doble integral. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir 'circulación' con 'flujo'.** Circulación es $\\oint \\vec{F} \\cdot \\vec{T} \\, ds$; flujo es $\\oint \\vec{F} \\cdot \\vec{n} \\, ds$. Distintos.",
              "**Confundir rotacional con divergencia.** $\\nabla \\times \\vec{F}$ es vectorial; $\\nabla \\cdot \\vec{F}$ es escalar.",
              "**Olvidar la orientación.** Cambiar la orientación cambia el signo de la integral.",
              "**Aplicar Green vectorial sin que las hipótesis se cumplan.** Misma exigencia: $C$ cerrada, simple, etc.",
              "**Confundir $\\vec{n}$ exterior con interior.** Por convención, $\\vec{n}$ apunta **fuera** de $D$ en la forma del flujo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma circulación:** $\\oint \\vec{F} \\cdot \\vec{T} \\, ds = \\iint (\\nabla \\times \\vec{F}) \\cdot \\vec{k} \\, dA$ — circulación total = micro-rotaciones internas.",
              "**Forma flujo:** $\\oint \\vec{F} \\cdot \\vec{n} \\, ds = \\iint \\nabla \\cdot \\vec{F} \\, dA$ — flujo neto = fuentes/sumideros internos.",
              "**Rotacional ($\\text{rot}$):** mide la 'rotación local' del campo.",
              "**Divergencia ($\\text{div}$):** mide la 'expansión local' del campo.",
              "**Generalizaciones 3D:** Stokes (circulación) y divergencia (flujo) — capítulo 3.",
              "**Cierre del capítulo:** las integrales de línea en 2D están **completamente caracterizadas** por estos teoremas. El próximo capítulo extiende todo a superficies 3D.",
          ]),
    ]
    return {
        "id": "lec-vec-2-6-green-vectorial",
        "title": "Teorema vectorial de Green",
        "description": "Formas de circulación y flujo. Rotacional, divergencia y preludio a Stokes y divergencia 3D.",
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
    course_id = "calculo-vectorial"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Curso {course_id} no existe.")

    chapter_id = "ch-integrales-linea"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Integrales de Línea",
        "description": "Campos escalares y vectoriales, integrales de línea, teorema fundamental, teorema de Green.",
        "order": 2,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_2_1, lesson_2_2, lesson_2_3, lesson_2_4, lesson_2_5, lesson_2_6]
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
    print(f"✅ Capítulo 2 — Integrales de Línea listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
