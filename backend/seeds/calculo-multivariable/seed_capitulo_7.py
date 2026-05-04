"""
Seed del curso Cálculo Multivariable — Capítulo 7: Aplicaciones de Integrales Múltiples.
3 lecciones (cierre del curso):
  7.1 Centros de masa
  7.2 Momentos de inercia
  7.3 Área de una superficie

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
# 7.1 Centros de masa
# =====================================================================
def lesson_7_1():
    blocks = [
        b("texto", body_md=(
            "El **centro de masa** generaliza el concepto del 'punto medio ponderado' a regiones 2D y "
            "3D con densidad variable. Es la posición efectiva donde se concentraría la masa total para "
            "fines de equilibrio y traslación. Un objeto suspendido por su centro de masa **no rota** bajo "
            "su propio peso.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular **masa total** $M = \\iint \\rho \\, dA$ (o triple, en 3D).\n"
            "- Calcular **momentos** respecto a los ejes.\n"
            "- Encontrar el **centro de masa** $(\\bar{x}, \\bar{y})$ (o $(\\bar{x}, \\bar{y}, \\bar{z})$ en 3D).\n"
            "- Reconocer el **centroide** como caso de densidad constante."
        )),

        b("definicion",
          titulo="Masa y momentos de una lámina",
          body_md=(
              "Sea una **lámina** (placa delgada) que ocupa la región $D \\subset \\mathbb{R}^2$ con **densidad superficial** $\\rho(x, y)$ (masa por unidad de área).\n\n"
              "**Masa total:**\n\n"
              "$$M = \\iint_D \\rho(x, y) \\, dA$$\n\n"
              "**Momento respecto al eje $x$:** $M_x = \\iint_D y \\, \\rho \\, dA$ (\"distancia al eje $x$ por densidad\").\n\n"
              "**Momento respecto al eje $y$:** $M_y = \\iint_D x \\, \\rho \\, dA$.\n\n"
              "**Centro de masa:**\n\n"
              "$$\\bar{x} = \\dfrac{M_y}{M}, \\quad \\bar{y} = \\dfrac{M_x}{M}$$"
          )),

        b("intuicion",
          titulo="¿Por qué los momentos son la clave?",
          body_md=(
              "Imagina la lámina dividida en pequeños trozos $dA$. Cada trozo tiene masa $dm = \\rho \\, dA$ y está en la posición $(x, y)$.\n\n"
              "**Equilibrio rotacional respecto al eje $y$:** la suma de los \"torques\" $x \\, dm$ debe equivaler al torque que produciría toda la masa $M$ concentrada en $\\bar{x}$:\n\n"
              "$$\\bar{x} \\cdot M = \\iint x \\, \\rho \\, dA = M_y$$\n\n"
              "**Despejando:** $\\bar{x} = M_y / M$. Lo mismo para $\\bar{y}$.\n\n"
              "**Notación 'cruzada' (sutileza):** $M_y$ tiene $x$ adentro porque mide momento **alrededor del eje $y$** — la posición $x$ es la \"distancia\" al eje $y$. Análogo: $M_x$ tiene $y$ adentro."
          )),

        b("ejemplo_resuelto",
          titulo="Centro de masa de una lámina",
          problema_md=(
              "Una lámina ocupa el triángulo con vértices $(0, 0), (1, 0), (0, 2)$ con densidad $\\rho(x, y) = 1 + 3x + y$. Hallar su centro de masa."
          ),
          pasos=[
              {"accion_md": "**Triángulo:** $0 \\leq x \\leq 1, 0 \\leq y \\leq 2(1 - x) = 2 - 2x$. Tipo I.\n\n"
                            "**Masa:** $M = \\int_0^1 \\int_0^{2-2x} (1 + 3x + y) \\, dy \\, dx$.",
               "justificacion_md": "Plantear los límites según la geometría.",
               "es_resultado": False},
              {"accion_md": "**Interna:** $\\int_0^{2-2x}(1 + 3x + y) \\, dy = (1 + 3x)(2 - 2x) + \\dfrac{(2-2x)^2}{2}$\n\n"
                            "$= 2 + 6x - 2x - 6x^2 + 2(1 - x)^2 = 2 + 4x - 6x^2 + 2 - 4x + 2x^2 = 4 - 4x^2$.",
               "justificacion_md": "Expandir y simplificar.",
               "es_resultado": False},
              {"accion_md": "**Externa:** $M = \\int_0^1 (4 - 4x^2) \\, dx = 4 - 4/3 = 8/3$.",
               "justificacion_md": "Antiderivada simple.",
               "es_resultado": False},
              {"accion_md": "**$M_y$:** $\\int_0^1 \\int_0^{2-2x} x(1+3x+y) \\, dy \\, dx = \\int_0^1 x(4 - 4x^2) \\, dx = \\int_0^1 (4x - 4x^3) \\, dx = 2 - 1 = 1$.\n\n"
                            "**$M_x$:** $\\int_0^1 \\int_0^{2-2x} y(1+3x+y) \\, dy \\, dx$. Calculando: $= \\int_0^1 [(1+3x)\\dfrac{(2-2x)^2}{2} + \\dfrac{(2-2x)^3}{3}] \\, dx$. Después de simplificar: $11/6$.\n\n"
                            "(Los detalles algebraicos son tediosos; en la práctica se usaría software.)",
               "justificacion_md": "$M_y$ y $M_x$ requieren más álgebra, pero el procedimiento es mecánico.",
               "es_resultado": False},
              {"accion_md": "**Centro de masa:** $\\bar{x} = M_y/M = 1/(8/3) = 3/8$. $\\bar{y} = M_x/M = (11/6)/(8/3) = 11/16$.",
               "justificacion_md": "**Lección:** el procedimiento es siempre el mismo — masa, dos momentos, dividir.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Centroide (densidad constante)",
          body_md=(
              "Si la densidad es **constante** $\\rho_0$, los momentos quedan:\n\n"
              "$M = \\rho_0 A(D)$, $M_x = \\rho_0 \\iint y \\, dA$, $M_y = \\rho_0 \\iint x \\, dA$.\n\n"
              "Los $\\rho_0$ se cancelan al dividir, así el **centro de masa coincide con el 'centro geométrico' o centroide**:\n\n"
              "$$\\bar{x} = \\dfrac{1}{A(D)} \\iint_D x \\, dA, \\quad \\bar{y} = \\dfrac{1}{A(D)} \\iint_D y \\, dA$$\n\n"
              "**Es la posición promedio de los puntos de la región.**"
          )),

        b("ejemplo_resuelto",
          titulo="Centroide de un semicírculo",
          problema_md=(
              "Hallar el centroide del semicírculo $\\{(x, y) : x^2 + y^2 \\leq R^2, y \\geq 0\\}$."
          ),
          pasos=[
              {"accion_md": "**Por simetría:** $\\bar{x} = 0$ (la región es simétrica respecto al eje $y$).",
               "justificacion_md": "Cualquier $x$ tiene su par $-x$ con el mismo peso.",
               "es_resultado": False},
              {"accion_md": "**Para $\\bar{y}$:** área $A = \\pi R^2/2$. Calculamos $\\iint y \\, dA$ en polares:\n\n"
                            "$\\iint y \\, dA = \\int_0^\\pi \\int_0^R (r\\sin\\theta)(r) \\, dr \\, d\\theta = \\int_0^\\pi \\sin\\theta \\, d\\theta \\cdot \\int_0^R r^2 \\, dr = 2 \\cdot R^3/3 = 2R^3/3$.",
               "justificacion_md": "Polares: $y = r\\sin\\theta$, $dA = r \\, dr \\, d\\theta$.",
               "es_resultado": False},
              {"accion_md": "$\\bar{y} = \\dfrac{2R^3/3}{\\pi R^2/2} = \\dfrac{4R}{3\\pi}$.",
               "justificacion_md": "**Resultado clásico:** centroide del semicírculo está a $4R/(3\\pi) \\approx 0.42 R$ del diámetro. **No es $R/2$** — la masa está concentrada hacia el lado curvo, no en el medio.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Versión 3D",
          body_md=(
              "Para un sólido $E \\subset \\mathbb{R}^3$ con densidad $\\rho(x, y, z)$:\n\n"
              "$$M = \\iiint_E \\rho \\, dV$$\n\n"
              "$$M_{yz} = \\iiint_E x \\rho \\, dV, \\quad M_{xz} = \\iiint_E y \\rho \\, dV, \\quad M_{xy} = \\iiint_E z \\rho \\, dV$$\n\n"
              "(Cada momento está respecto al **plano** opuesto a la coordenada en el integrando.)\n\n"
              "**Centro de masa:**\n\n"
              "$$\\bar{x} = \\dfrac{M_{yz}}{M}, \\quad \\bar{y} = \\dfrac{M_{xz}}{M}, \\quad \\bar{z} = \\dfrac{M_{xy}}{M}$$"
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$M_y$ (momento respecto al eje $y$) tiene en su integrando:",
                  "opciones_md": [
                      "$y \\rho$",
                      "$x \\rho$",
                      "$\\rho$ solo",
                      "$xy \\rho$",
                  ],
                  "correcta": "B",
                  "pista_md": "Momento respecto a un eje involucra distancia al eje. La distancia al eje $y$ es $|x|$.",
                  "explicacion_md": (
                      "$M_y = \\iint x \\rho \\, dA$. La 'distancia con signo' al eje $y$ es $x$ — por eso aparece $x$ adentro, no $y$."
                  ),
              },
              {
                  "enunciado_md": "Si la densidad es constante, el centro de masa:",
                  "opciones_md": [
                      "Es siempre el origen.",
                      "Coincide con el centroide (centro geométrico).",
                      "Está en el borde.",
                      "Depende del valor de $\\rho_0$.",
                  ],
                  "correcta": "B",
                  "pista_md": "Densidad constante se cancela al dividir.",
                  "explicacion_md": (
                      "$\\rho_0$ aparece en numerador y denominador, así se cancela. **El centroide depende solo de la geometría.**"
                  ),
              },
          ]),

        ej(
            titulo="Centroide de un triángulo",
            enunciado="Halla el centroide del triángulo con vértices $(0, 0), (a, 0), (0, b)$.",
            pistas=[
                "Por simetría no hay reducción — calcular ambos.",
                "Área $A = ab/2$.",
                "$\\bar{x} = \\dfrac{1}{A} \\int_0^a \\int_0^{b(1 - x/a)} x \\, dy \\, dx$.",
            ],
            solucion=(
                "$\\int_0^a \\int_0^{b(1-x/a)} x \\, dy \\, dx = \\int_0^a x \\cdot b(1 - x/a) \\, dx = b \\int_0^a (x - x^2/a) \\, dx = b(a^2/2 - a^2/3) = a^2 b/6$.\n\n"
                "$\\bar{x} = (a^2 b/6)/(ab/2) = a/3$. **Análogo:** $\\bar{y} = b/3$.\n\n"
                "**Resultado clásico:** el centroide de un triángulo está en $(\\bar{x}, \\bar{y})$ = promedio de los vértices: $((0+a+0)/3, (0+0+b)/3) = (a/3, b/3)$. ✓"
            ),
        ),

        ej(
            titulo="Centro de masa con densidad $\\rho = x$",
            enunciado="Halla el centro de masa de la lámina sobre $[0, 1] \\times [0, 1]$ con densidad $\\rho(x, y) = x$.",
            pistas=[
                "$M = \\iint_R x \\, dA$ (rectángulo separable).",
                "$M_y = \\iint x^2 \\, dA$, $M_x = \\iint xy \\, dA$.",
            ],
            solucion=(
                "$M = (\\int_0^1 x \\, dx)(\\int_0^1 dy) = 1/2$.\n\n"
                "$M_y = (\\int_0^1 x^2 dx)(\\int_0^1 dy) = 1/3$. $M_x = (\\int_0^1 x dx)(\\int_0^1 y dy) = 1/2 \\cdot 1/2 = 1/4$.\n\n"
                "$\\bar{x} = (1/3)/(1/2) = 2/3$. $\\bar{y} = (1/4)/(1/2) = 1/2$.\n\n"
                "**Verificación:** la densidad crece con $x$, así el centro de masa está corrido hacia $x$ grande ($2/3 > 1/2$). En $y$, la densidad no depende, así $\\bar{y} = 1/2$ (centro)."
            ),
        ),

        fig(
            "Vista 2D superior de una lámina plana con forma irregular (silueta tipo gota o "
            "frijol) en el plano xy, sombreada en color teal #06b6d4 translúcido representando "
            "masa distribuida uniformemente. Ejes x, y marcados con escala. El punto del centro "
            "de masa (x̄, ȳ) marcado con una cruz ámbar #f59e0b grande y etiqueta '(x̄, ȳ)'. "
            "Debajo de la figura, dos fórmulas grandes en cajita: 'x̄ = (1/M)∬ x ρ dA' y "
            "'ȳ = (1/M)∬ y ρ dA', con etiqueta 'M = masa total'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $M_x$ con 'integrar $x$'.** $M_x$ tiene $y$ adentro (es momento respecto al eje $x$).",
              "**Olvidar dividir por la masa.** Los momentos no son el centro de masa — son numeradores.",
              "**Ignorar la simetría.** Si la región y la densidad son simétricas respecto a un eje, el centro de masa está en ese eje (no hace falta calcular).",
              "**Aplicar la fórmula de centroide cuando la densidad varía.** Centroide ≠ centro de masa si $\\rho$ no es constante.",
              "**Confundir 2D con 3D.** Las versiones tienen estructura paralela pero los integrandos y nombres difieren.",
          ]),

        b("resumen",
          puntos_md=[
              "**Masa:** $M = \\iint \\rho \\, dA$.",
              "**Momentos:** $M_y = \\iint x\\rho \\, dA$ (eje $y$), $M_x = \\iint y\\rho \\, dA$ (eje $x$).",
              "**Centro de masa:** $\\bar{x} = M_y/M, \\bar{y} = M_x/M$.",
              "**Centroide:** caso $\\rho$ constante — depende solo de la forma.",
              "**Simetría** simplifica enormemente.",
              "**3D:** análogo con triple integral.",
              "**Próxima lección:** momentos de inercia — cómo se distribuye la masa respecto a la rotación.",
          ]),
    ]
    return {
        "id": "lec-mvar-7-1-centros-masa",
        "title": "Centros de masa",
        "description": "Masa, momentos y centro de masa de láminas y sólidos. Centroide como caso de densidad constante.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 7.2 Momentos de inercia
# =====================================================================
def lesson_7_2():
    blocks = [
        b("texto", body_md=(
            "El **momento de inercia** mide la \"resistencia\" de un cuerpo a la rotación alrededor de un eje. "
            "Es el análogo rotacional de la masa: en traslación, la masa determina cuánto cuesta acelerar; "
            "en rotación, el momento de inercia determina cuánto cuesta cambiar la velocidad angular.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular $I_x, I_y, I_0$ para una lámina.\n"
            "- Comprender la conexión $K = \\frac{1}{2}I\\omega^2$ (energía cinética rotacional).\n"
            "- Calcular el **radio de giro**.\n"
            "- Manejar versiones 3D."
        )),

        b("definicion",
          titulo="Momentos de inercia de una lámina",
          body_md=(
              "Sea una lámina con densidad $\\rho(x, y)$ sobre la región $D$:\n\n"
              "**Momento de inercia respecto al eje $x$:**\n\n"
              "$$I_x = \\iint_D y^2 \\, \\rho \\, dA$$\n\n"
              "**Momento de inercia respecto al eje $y$:**\n\n"
              "$$I_y = \\iint_D x^2 \\, \\rho \\, dA$$\n\n"
              "**Momento polar (respecto al origen, eje perpendicular al plano):**\n\n"
              "$$I_0 = \\iint_D (x^2 + y^2) \\, \\rho \\, dA = I_x + I_y$$\n\n"
              "**Patrón:** distancia al eje **al cuadrado** por densidad. La diferencia con $M_x, M_y$ (centro de masa) es exactamente el cuadrado en lugar de la primera potencia."
          )),

        b("intuicion",
          titulo="¿Por qué la distancia al cuadrado?",
          body_md=(
              "La energía cinética de rotación de un cuerpo rígido es:\n\n"
              "$$K = \\dfrac{1}{2} I \\omega^2$$\n\n"
              "donde $\\omega$ es la velocidad angular y $I$ es el momento de inercia respecto al eje de rotación.\n\n"
              "Una partícula de masa $dm$ a distancia $d$ del eje, girando a velocidad angular $\\omega$, tiene velocidad lineal $v = d\\omega$ y energía $\\dfrac{1}{2} dm \\, v^2 = \\dfrac{1}{2} d^2 \\omega^2 \\, dm$.\n\n"
              "Sumando: $K = \\dfrac{\\omega^2}{2} \\iint d^2 \\, \\rho \\, dA = \\dfrac{1}{2} I \\omega^2$.\n\n"
              "**Por eso aparece $d^2$:** captura el efecto cuadrático de la distancia en la energía rotacional. Masa lejos del eje contribuye **mucho más** que masa cerca."
          )),

        b("ejemplo_resuelto",
          titulo="Momentos de un disco uniforme",
          problema_md=(
              "Un disco de radio $R$ con densidad constante $\\rho_0$ ocupa la región $x^2 + y^2 \\leq R^2$. Calcular $I_0$."
          ),
          pasos=[
              {"accion_md": "**Polares:** $I_0 = \\iint (x^2+y^2) \\rho_0 \\, dA = \\rho_0 \\int_0^{2\\pi} \\int_0^R r^2 \\cdot r \\, dr \\, d\\theta$.",
               "justificacion_md": "$x^2 + y^2 = r^2$. $dA = r \\, dr \\, d\\theta$.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^R r^3 \\, dr = R^4/4$. $\\int_0^{2\\pi} d\\theta = 2\\pi$.\n\n"
                            "$I_0 = \\rho_0 \\cdot 2\\pi \\cdot R^4/4 = \\dfrac{\\pi \\rho_0 R^4}{2}$.",
               "justificacion_md": "Cálculo directo.",
               "es_resultado": False},
              {"accion_md": "**En términos de la masa total** $M = \\rho_0 \\pi R^2$: $I_0 = \\dfrac{M R^2}{2}$.\n\n"
                            "**Resultado clásico:** un disco uniforme tiene $I_0 = MR^2/2$ respecto a su eje central perpendicular. Es la fórmula que aparece en libros de física.",
               "justificacion_md": "**Comparación:** un anillo (toda la masa en el borde) tiene $I_0 = MR^2$, el doble. **El disco distribuye la masa más cerca del eje, así rota más fácil.**",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Radio de giro",
          body_md=(
              "El **radio de giro** $\\bar{r}$ respecto a un eje es la distancia $\\bar{r}$ tal que, si toda la masa estuviera concentrada a esa distancia del eje, daría el mismo momento de inercia:\n\n"
              "$$I = M \\bar{r}^2 \\implies \\bar{r} = \\sqrt{\\dfrac{I}{M}}$$\n\n"
              "Análogamente para $\\bar{r}_x = \\sqrt{I_x/M}$ y $\\bar{r}_y = \\sqrt{I_y/M}$.\n\n"
              "**Interpretación:** un anillo equivalente al objeto tiene radio $\\bar{r}$. Para el disco anterior: $\\bar{r}_0 = \\sqrt{R^2/2} = R/\\sqrt{2}$ — la \"masa equivalente\" estaría a esa distancia del centro."
          )),

        b("ejemplo_resuelto",
          titulo="Momento de un rectángulo respecto a un lado",
          problema_md=(
              "Un rectángulo uniforme con base $a$ y altura $b$ tiene su esquina inferior izquierda en el origen. Calcular $I_x$ (respecto al lado inferior)."
          ),
          pasos=[
              {"accion_md": "**Densidad constante** $\\rho_0$. **$I_x = \\rho_0 \\iint y^2 \\, dA = \\rho_0 \\int_0^a \\int_0^b y^2 \\, dy \\, dx$.**",
               "justificacion_md": "El eje $x$ es el lado inferior.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^b y^2 \\, dy = b^3/3$. $\\int_0^a dx = a$. **$I_x = \\rho_0 \\cdot a \\cdot b^3/3 = M \\dfrac{b^2}{3}$** (con $M = \\rho_0 a b$).",
               "justificacion_md": "Resultado clásico para barras o rectángulos.",
               "es_resultado": False},
              {"accion_md": "**Comparación con el centro:** respecto al **eje horizontal central** (a altura $b/2$), el momento de inercia sería $M b^2 / 12$ (por el teorema de los ejes paralelos). El factor $1/3$ vs $1/12$ refleja que medimos respecto a un borde, no al centro.",
               "justificacion_md": "**Lección general:** $I$ depende del eje elegido. Mismo objeto, distinto eje, distinto $I$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Versión 3D",
          body_md=(
              "Para un sólido $E$ con densidad $\\rho(x, y, z)$:\n\n"
              "$$I_x = \\iiint_E (y^2 + z^2) \\rho \\, dV$$\n\n"
              "$$I_y = \\iiint_E (x^2 + z^2) \\rho \\, dV$$\n\n"
              "$$I_z = \\iiint_E (x^2 + y^2) \\rho \\, dV$$\n\n"
              "**Patrón:** $I_{eje}$ tiene la **suma de cuadrados** de las **dos coordenadas perpendiculares** al eje.\n\n"
              "**Tensor de inercia:** existen también $I_{xy} = \\iiint xy \\rho \\, dV$ etc., que forman el **tensor de inercia** completo. Pero los diagonales $I_x, I_y, I_z$ son los más usados."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$I_y$ (momento respecto al eje $y$) tiene como integrando:",
                  "opciones_md": [
                      "$y^2 \\rho$",
                      "$x^2 \\rho$",
                      "$x \\rho$",
                      "$xy \\rho$",
                  ],
                  "correcta": "B",
                  "pista_md": "Distancia al eje $y$ es $|x|$, al cuadrado: $x^2$.",
                  "explicacion_md": (
                      "$I_y = \\iint x^2 \\rho \\, dA$. **Distancia al cuadrado** porque la energía rotacional depende cuadráticamente de la distancia."
                  ),
              },
              {
                  "enunciado_md": "Para un mismo objeto, comparando $I$ respecto al eje central vs respecto a un borde:",
                  "opciones_md": [
                      "Son iguales.",
                      "$I_{borde} > I_{centro}$ (la masa está más lejos del eje en promedio).",
                      "$I_{centro} > I_{borde}$.",
                      "Depende del objeto.",
                  ],
                  "correcta": "B",
                  "pista_md": "Si el eje pasa más lejos del centro de masa, las distancias en promedio son mayores.",
                  "explicacion_md": (
                      "**Teorema de los ejes paralelos:** $I_{eje} = I_{cm} + Md^2$ donde $d$ es la distancia entre ejes. Como $d^2 \\geq 0$, $I_{borde} \\geq I_{cm}$ siempre."
                  ),
              },
          ]),

        ej(
            titulo="Momento de inercia con polares",
            enunciado=(
                "Calcula $I_0$ para una lámina con densidad $\\rho(x, y) = \\sqrt{x^2 + y^2}$ "
                "sobre el disco $x^2 + y^2 \\leq 1$."
            ),
            pistas=[
                "$\\rho = r$ en polares.",
                "$I_0 = \\iint r^2 \\cdot r \\cdot r \\, dr \\, d\\theta = \\iint r^4 \\, dr \\, d\\theta$.",
            ],
            solucion=(
                "$I_0 = \\int_0^{2\\pi} \\int_0^1 r^4 \\, dr \\, d\\theta = 2\\pi \\cdot 1/5 = 2\\pi/5$."
            ),
        ),

        ej(
            titulo="$I_x$ de un sector triangular",
            enunciado=(
                "Calcula $I_x$ para una lámina uniforme ($\\rho_0 = 1$) sobre el triángulo "
                "con vértices $(0, 0), (1, 0), (1, 2)$."
            ),
            pistas=[
                "Triángulo: $0 \\leq x \\leq 1, 0 \\leq y \\leq 2x$.",
                "$I_x = \\int_0^1 \\int_0^{2x} y^2 \\, dy \\, dx$.",
            ],
            solucion=(
                "$I_x = \\int_0^1 \\dfrac{(2x)^3}{3} dx = \\int_0^1 \\dfrac{8x^3}{3} dx = \\dfrac{8}{3} \\cdot \\dfrac{1}{4} = \\dfrac{2}{3}$."
            ),
        ),

        fig(
            "Tres mini-paneles lado a lado mostrando la misma lámina plana irregular en color "
            "teal #06b6d4 translúcido, con un elemento dA pequeño marcado adentro. Panel 1: "
            "eje de rotación = eje x (línea horizontal punteada ámbar #f59e0b en y = 0). "
            "Distancia r = y desde dA al eje, con flecha doble vertical. Etiqueta 'I_x = ∬ y² "
            "ρ dA'. Panel 2: eje = eje y (línea vertical punteada ámbar). Distancia r = x. "
            "'I_y = ∬ x² ρ dA'. Panel 3: eje = origen (punto ámbar en (0,0)). Distancia "
            "r = √(x²+y²). 'I_0 = ∬ (x²+y²) ρ dA = I_x + I_y'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $M_x$ ($\\int y \\rho$) con $I_x$ ($\\int y^2 \\rho$).** El primero es momento de masa (lineal); el segundo, momento de inercia (cuadrático).",
              "**Olvidar el cuadrado.** En $I$, la distancia siempre se eleva al cuadrado.",
              "**Confundir $I_x$ con $I_y$.** $I_x$ tiene $y^2$ en el integrando (distancia al eje $x$); $I_y$ tiene $x^2$.",
              "**Aplicar fórmulas para ejes centrales cuando el eje pasa por el borde.** Diferencias notables (factor 1/3 vs 1/12 para rectángulos).",
              "**Olvidar la densidad** en problemas con masa variable. $I = \\iint d^2 \\rho \\, dA$, no $\\iint d^2 \\, dA$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Momento de inercia:** $I = \\iint d^2 \\rho \\, dA$, distancia **al cuadrado**.",
              "**Casos clave:** $I_x = \\iint y^2 \\rho$, $I_y = \\iint x^2 \\rho$, $I_0 = I_x + I_y$.",
              "**Energía rotacional:** $K = \\dfrac{1}{2} I \\omega^2$.",
              "**Radio de giro:** $\\bar{r} = \\sqrt{I/M}$ — distancia equivalente del anillo concentrado.",
              "**Resultados clásicos:** disco $I_0 = MR^2/2$, anillo $I_0 = MR^2$, varilla por su centro $I = ML^2/12$.",
              "**3D:** $I_z = \\iiint (x^2+y^2)\\rho \\, dV$ (suma de cuadrados de las dos coords perpendiculares al eje).",
              "**Próxima lección:** área de una superficie — el cierre del curso.",
          ]),
    ]
    return {
        "id": "lec-mvar-7-2-momentos-inercia",
        "title": "Momentos de inercia",
        "description": "Momentos de inercia respecto a ejes, energía rotacional, radio de giro y versión 3D.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# 7.3 Área de una superficie
# =====================================================================
def lesson_7_3():
    blocks = [
        b("texto", body_md=(
            "Cerramos el curso calculando **áreas de superficies** dadas como gráficas $z = f(x, y)$. "
            "Análogo a la longitud de arco en 1D ($L = \\int \\sqrt{1 + (f')^2} \\, dx$), aquí necesitaremos "
            "$\\sqrt{1 + f_x^2 + f_y^2}$, que mide cuánto se 'estira' un trozo de plano $dA$ al "
            "deformarse hacia la superficie.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Plantear $A(S) = \\iint_D \\sqrt{1 + f_x^2 + f_y^2} \\, dA$.\n"
            "- Comprender la **derivación geométrica** (producto cruz de vectores tangentes).\n"
            "- Calcular áreas de superficies clásicas: planos, paraboloides, esferas (parciales)."
        )),

        b("teorema",
          nombre="Fórmula del área de superficie",
          enunciado_md=(
              "Sea $S$ la superficie $z = f(x, y)$ con $(x, y) \\in D$, donde $f$ es de clase $C^1$. El **área** de $S$ es:\n\n"
              "$$A(S) = \\iint_D \\sqrt{1 + f_x^2 + f_y^2} \\, dA$$\n\n"
              "**Notación equivalente:** $\\iint_D \\sqrt{1 + |\\nabla f|^2} \\, dA$.\n\n"
              "**Caso especial:** si $f$ es constante (plano horizontal), $f_x = f_y = 0$ y $A = \\iint 1 \\, dA = $ área de $D$. ✓"
          ),
          demostracion_md=(
              "Idea: parametriza la superficie por $\\vec{r}(x, y) = (x, y, f(x, y))$. Los vectores tangentes son $\\vec{r}_x = (1, 0, f_x)$ y $\\vec{r}_y = (0, 1, f_y)$. "
              "Su producto cruz $\\vec{r}_x \\times \\vec{r}_y = (-f_x, -f_y, 1)$ tiene magnitud $\\sqrt{f_x^2 + f_y^2 + 1}$.\n\n"
              "El elemento de área $dS = \\|\\vec{r}_x \\times \\vec{r}_y\\| \\, dA = \\sqrt{1 + f_x^2 + f_y^2} \\, dA$.\n\n"
              "Sumando: $A(S) = \\iint_D dS$. **Es Pitágoras 2D + producto cruz.**"
          )),

        fig(
            "Elemento de área de una superficie. Vista 3D isométrica de una superficie ondulada z = "
            "f(x, y) en color teal translúcido. Sobre el plano xy, un pequeño rectángulo dA en "
            "color ámbar. Su 'imagen' en la superficie es un paralelogramo curvado pequeño (en "
            "color ámbar más oscuro) cuya área es dS. Mostrar dos vectores tangentes r_x y r_y "
            "saliendo de un punto de la superficie, con su producto cruz indicado por una flecha "
            "perpendicular. Etiquetas: 'dA = dx dy' (en el plano), 'dS = √(1 + f_x² + f_y²) dA' "
            "(sobre la superficie), 'r_x', 'r_y'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Área de una superficie plana inclinada",
          problema_md=(
              "Calcular el área del trozo del plano $z = 2x + 3y$ que está sobre el rectángulo $[0, 1] \\times [0, 2]$."
          ),
          pasos=[
              {"accion_md": "**Parciales:** $f_x = 2, f_y = 3$. **Constantes**, así $\\sqrt{1 + 4 + 9} = \\sqrt{14}$.",
               "justificacion_md": "Plano: las parciales son constantes.",
               "es_resultado": False},
              {"accion_md": "$A(S) = \\iint_R \\sqrt{14} \\, dA = \\sqrt{14} \\cdot \\text{Area}(R) = \\sqrt{14} \\cdot 2 = 2\\sqrt{14}$.",
               "justificacion_md": "**Patrón general:** trozo de plano sobre una región $R$ tiene área $A(R) \\cdot \\sqrt{1 + f_x^2 + f_y^2}$ (factor de estiramiento constante).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Área de un paraboloide",
          problema_md=(
              "Calcular el área de la parte de $z = x^2 + y^2$ con $z \\leq 4$."
          ),
          pasos=[
              {"accion_md": "**Región:** $z \\leq 4 \\iff x^2 + y^2 \\leq 4$. Disco de radio $2$. **Parciales:** $f_x = 2x, f_y = 2y$.\n\n"
                            "$\\sqrt{1 + 4x^2 + 4y^2} = \\sqrt{1 + 4r^2}$ en polares.",
               "justificacion_md": "$x^2 + y^2 = r^2$.",
               "es_resultado": False},
              {"accion_md": "$A = \\int_0^{2\\pi} \\int_0^2 \\sqrt{1 + 4r^2} \\cdot r \\, dr \\, d\\theta = 2\\pi \\int_0^2 r\\sqrt{1+4r^2} \\, dr$.\n\n"
                            "**Sustitución** $u = 1 + 4r^2$, $du = 8r \\, dr$, $r \\, dr = du/8$. Cuando $r = 0$: $u = 1$; cuando $r = 2$: $u = 17$.",
               "justificacion_md": "Polares + sustitución.",
               "es_resultado": False},
              {"accion_md": "$2\\pi \\cdot \\dfrac{1}{8} \\int_1^{17} u^{1/2} \\, du = \\dfrac{\\pi}{4} \\cdot \\dfrac{2}{3} \\left[u^{3/2}\\right]_1^{17} = \\dfrac{\\pi}{6}(17^{3/2} - 1)$.\n\n"
                            "$= \\dfrac{\\pi(17\\sqrt{17} - 1)}{6} \\approx 36.18$.",
               "justificacion_md": "**Resultado clásico:** el factor $\\sqrt{1 + 4r^2}$ no es constante, así el área es **mayor** que el área del disco que es la base ($4\\pi \\approx 12.57$). El paraboloide se 'estira' al subir.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Hemisferio (truco al borde)",
          problema_md=(
              "Calcular el área del hemisferio superior $z = \\sqrt{R^2 - x^2 - y^2}$ con $z \\geq 0$."
          ),
          pasos=[
              {"accion_md": "**Parciales:** $f_x = -x/\\sqrt{R^2-x^2-y^2} = -x/z$. Análogo $f_y = -y/z$.\n\n"
                            "$1 + f_x^2 + f_y^2 = 1 + (x^2 + y^2)/z^2 = (z^2 + x^2 + y^2)/z^2 = R^2/z^2$.\n\n"
                            "$\\sqrt{1 + f_x^2 + f_y^2} = R/z = R/\\sqrt{R^2 - x^2 - y^2}$.",
               "justificacion_md": "**Magia:** la raíz se simplifica.",
               "es_resultado": False},
              {"accion_md": "**En polares** ($x^2 + y^2 = r^2$, $z = \\sqrt{R^2 - r^2}$, $dA = r \\, dr \\, d\\theta$):\n\n"
                            "$A = \\int_0^{2\\pi} \\int_0^R \\dfrac{R}{\\sqrt{R^2 - r^2}} r \\, dr \\, d\\theta$.",
               "justificacion_md": "Cambio a polares.",
               "es_resultado": False},
              {"accion_md": "**Sustitución** $u = R^2 - r^2$, $du = -2r \\, dr$:\n\n"
                            "$\\int_0^R \\dfrac{R r}{\\sqrt{R^2 - r^2}} dr = R \\cdot \\dfrac{-1}{2} \\int_{R^2}^0 u^{-1/2} \\, du = \\dfrac{R}{2} \\int_0^{R^2} u^{-1/2} du = \\dfrac{R}{2} \\cdot 2\\sqrt{R^2} = R^2$.\n\n"
                            "$A = 2\\pi \\cdot R^2 = 2\\pi R^2$.",
               "justificacion_md": "**¡Resultado clásico!** El hemisferio tiene área $2\\pi R^2$ — la mitad del área de la esfera $4\\pi R^2$. Otra confirmación de fórmulas geométricas conocidas vía cálculo.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Cuándo la integral es factible",
          body_md=(
              "El integrando $\\sqrt{1 + f_x^2 + f_y^2}$ rara vez tiene antiderivada elemental. **Funciona bien cuando:**\n\n"
              "- **$f$ es lineal** (factor constante).\n"
              "- **$f$ tiene simetría** que polares simplifican (paraboloide, esfera, cono).\n"
              "- **$1 + |\\nabla f|^2$ es un cuadrado perfecto** (caso de superficies 'diseñadas').\n\n"
              "**En general,** muchas áreas de superficies se calculan **numéricamente**.\n\n"
              "**Análogo al problema de longitud de arco** (lección 3.5 de Cálculo Integral): la mayoría de las longitudes y áreas requieren métodos numéricos."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El elemento de área superficial $dS$ es:",
                  "opciones_md": [
                      "$dA$",
                      "$\\sqrt{1 + f_x^2 + f_y^2} \\, dA$",
                      "$(f_x^2 + f_y^2) \\, dA$",
                      "$\\sqrt{f_x^2 + f_y^2} \\, dA$",
                  ],
                  "correcta": "B",
                  "pista_md": "Análogo a $ds = \\sqrt{1 + (f')^2} \\, dx$ del 1D pero con dos variables.",
                  "explicacion_md": (
                      "$dS = \\sqrt{1 + f_x^2 + f_y^2} \\, dA$. **El '$1$' es esencial** — sin él, el área de un plano horizontal sería cero (lo que es absurdo)."
                  ),
              },
              {
                  "enunciado_md": "Para una superficie plana $z = ax + by + c$ sobre una región $D$, el área es:",
                  "opciones_md": [
                      "$\\text{Area}(D)$",
                      "$\\sqrt{1 + a^2 + b^2} \\cdot \\text{Area}(D)$",
                      "$(a^2 + b^2) \\cdot \\text{Area}(D)$",
                      "$\\sqrt{a^2 + b^2} \\cdot \\text{Area}(D)$",
                  ],
                  "correcta": "B",
                  "pista_md": "$f_x = a, f_y = b$ son constantes.",
                  "explicacion_md": (
                      "Constantes salen del integrando: $A = \\sqrt{1 + a^2 + b^2} \\cdot \\iint dA = \\sqrt{1+a^2+b^2} \\cdot \\text{Area}(D)$. **Factor de estiramiento del plano inclinado.**"
                  ),
              },
          ]),

        ej(
            titulo="Cilindro lateral",
            enunciado=(
                "Calcula el área lateral del cilindro $z = y^2$ sobre el rectángulo $[0, 1] \\times [0, 2]$."
            ),
            pistas=[
                "$f_x = 0, f_y = 2y$. Integrando: $\\sqrt{1 + 4y^2}$.",
                "El integrando solo depende de $y$ — separable.",
                "$\\int_0^2 \\sqrt{1 + 4y^2} \\, dy$ por sustitución hiperbólica o tabla.",
            ],
            solucion=(
                "$A = \\int_0^1 \\int_0^2 \\sqrt{1 + 4y^2} \\, dy \\, dx = 1 \\cdot \\int_0^2 \\sqrt{1+4y^2} dy$.\n\n"
                "$\\int \\sqrt{1+4y^2} dy = \\dfrac{y\\sqrt{1+4y^2}}{2} + \\dfrac{1}{4}\\ln(2y + \\sqrt{1+4y^2}) + C$ (por tabla).\n\n"
                "Evaluando en $[0, 2]$: $\\sqrt{17} + \\dfrac{1}{4}\\ln(4 + \\sqrt{17}) - 0 - \\dfrac{1}{4}\\ln(1) = \\sqrt{17} + \\dfrac{\\ln(4+\\sqrt{17})}{4}$."
            ),
        ),

        ej(
            titulo="Área de una porción esférica",
            enunciado=(
                "Calcula el área del trozo del plano $z = x + y$ que cae dentro del cilindro $x^2 + y^2 \\leq 1$."
            ),
            pistas=[
                "Plano inclinado, factor constante: $\\sqrt{1 + 1 + 1} = \\sqrt{3}$.",
                "Región: disco de radio 1, área $\\pi$.",
            ],
            solucion=(
                "$A = \\sqrt{3} \\cdot \\pi = \\sqrt{3}\\pi$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el '$+1$'** dentro de la raíz. Es lo que distingue área de superficie de un trozo plano vs un trozo curvo.",
              "**Confundir el área de la superficie con el área de su proyección $D$.** En general son distintas — solo son iguales para superficies horizontales.",
              "**No usar polares cuando la simetría lo permite.** Paraboloides y esferas se vuelven mucho más manejables en polares.",
              "**Asumir antiderivada elemental.** Muchas integrales de área requieren tablas o métodos numéricos.",
              "**Confundir $|\\nabla f|^2 = f_x^2 + f_y^2$ con $|\\nabla f| = \\sqrt{f_x^2 + f_y^2}$.** En la fórmula aparece el cuadrado, no la magnitud directamente.",
          ]),

        b("resumen",
          puntos_md=[
              "**Área de superficie:** $A = \\iint_D \\sqrt{1 + f_x^2 + f_y^2} \\, dA$.",
              "**Origen geométrico:** producto cruz de vectores tangentes a la parametrización.",
              "**Plano inclinado:** $A = \\sqrt{1 + a^2 + b^2} \\cdot \\text{Area}(D)$.",
              "**Hemisferio:** $A = 2\\pi R^2$ (recupera la fórmula clásica).",
              "**Polares** simplifican casos con simetría circular.",
              "**Cierre del curso de Cálculo Multivariable:** hemos cubierto todo el aparato — series, espacio, funciones de varias variables, derivadas parciales y sus aplicaciones, integrales múltiples y sus aplicaciones. Es el último paso del cálculo en pregrado.",
          ]),
    ]
    return {
        "id": "lec-mvar-7-3-area-superficie",
        "title": "Área de una superficie",
        "description": "Cálculo del área de una superficie $z = f(x, y)$ usando $\\sqrt{1 + f_x^2 + f_y^2}$.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
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

    chapter_id = "ch-aplicaciones-integrales-multiples"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Aplicaciones de Integrales Múltiples",
        "description": "Centros de masa, momentos de inercia y áreas de superficies.",
        "order": 7,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_7_1, lesson_7_2, lesson_7_3]
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
    print(f"✅ Capítulo 7 — Aplicaciones de Integrales Múltiples listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    print("🎉 Curso Cálculo Multivariable COMPLETO 🎉")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
