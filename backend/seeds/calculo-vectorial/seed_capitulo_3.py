"""
Seed del curso Cálculo Vectorial — Capítulo 3: Integrales de Superficie.
7 lecciones (cierre del curso):
  3.1 Superficies paramétricas
  3.2 Integral de superficie
  3.3 Superficies orientadas
  3.4 Integrales de superficie de campos vectoriales
  3.5 Aplicaciones
  3.6 Teorema de Stokes
  3.7 Teorema de la divergencia

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
# 3.1 Superficies paramétricas
# =====================================================================
def lesson_3_1():
    blocks = [
        b("texto", body_md=(
            "Igual que las **curvas paramétricas** describen objetos 1D mediante un parámetro $t$, las "
            "**superficies paramétricas** describen objetos 2D usando **dos parámetros** $u, v$. La función "
            "$\\vec{r}(u, v): D \\subset \\mathbb{R}^2 \\to \\mathbb{R}^3$ asigna a cada punto del dominio un "
            "punto en el espacio. La imagen es una superficie.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y manejar **superficies paramétricas** $\\vec{r}(u, v)$.\n"
            "- Conocer parametrizaciones clásicas: plano, esfera, cilindro, cono, gráfica $z = f(x, y)$.\n"
            "- Calcular **vectores tangentes** $\\vec{r}_u, \\vec{r}_v$ y el **vector normal** $\\vec{r}_u \\times \\vec{r}_v$.\n"
            "- Construir el **plano tangente** a una superficie paramétrica."
        )),

        b("definicion",
          titulo="Superficie paramétrica",
          body_md=(
              "Una **superficie paramétrica** es una función vectorial:\n\n"
              "$$\\vec{r}(u, v) = \\langle x(u, v), y(u, v), z(u, v) \\rangle, \\quad (u, v) \\in D \\subset \\mathbb{R}^2$$\n\n"
              "Su **traza** es la superficie $S = \\{\\vec{r}(u, v) : (u, v) \\in D\\}$ en $\\mathbb{R}^3$.\n\n"
              "**Ventaja sobre $z = f(x, y)$:** podemos describir superficies que no son gráficas de funciones de dos variables — esferas completas, toros, cilindros, superficies que se autointersecan."
          )),

        formulas(
            titulo="Parametrizaciones clásicas",
            body=(
                "| Superficie | Parametrización |\n|---|---|\n"
                "| **Gráfica** $z = f(x, y)$ | $\\vec{r}(u, v) = \\langle u, v, f(u, v) \\rangle$ |\n"
                "| **Plano** por $\\vec{r}_0$ con vectores $\\vec{a}, \\vec{b}$ | $\\vec{r}(u, v) = \\vec{r}_0 + u\\vec{a} + v\\vec{b}$ |\n"
                "| **Esfera** radio $R$ (con esféricas) | $\\vec{r}(\\theta, \\varphi) = R\\langle \\sin\\varphi\\cos\\theta, \\sin\\varphi\\sin\\theta, \\cos\\varphi \\rangle$ |\n"
                "| **Cilindro** $x^2+y^2=R^2$, altura $h$ | $\\vec{r}(\\theta, z) = \\langle R\\cos\\theta, R\\sin\\theta, z \\rangle$ |\n"
                "| **Cono** $z = \\sqrt{x^2+y^2}$ | $\\vec{r}(r, \\theta) = \\langle r\\cos\\theta, r\\sin\\theta, r \\rangle$ |\n"
                "| **Superficie de revolución** ($y = f(x)$ alrededor del eje $x$) | $\\vec{r}(x, \\theta) = \\langle x, f(x)\\cos\\theta, f(x)\\sin\\theta \\rangle$ |\n\n"
                "**Esfera y cono** son los casos donde polares/esféricas naturales se trasladan al cálculo vectorial."
            ),
        ),

        b("definicion",
          titulo="Vectores tangentes y normal",
          body_md=(
              "En cada punto $\\vec{r}(u_0, v_0)$ de la superficie hay dos **curvas naturales**:\n\n"
              "- **Curva $u$:** fijar $v = v_0$ y variar $u$. Tangente: $\\vec{r}_u = \\partial \\vec{r}/\\partial u$.\n"
              "- **Curva $v$:** fijar $u = u_0$ y variar $v$. Tangente: $\\vec{r}_v = \\partial \\vec{r}/\\partial v$.\n\n"
              "**Vector normal a la superficie:**\n\n"
              "$$\\vec{n} = \\vec{r}_u \\times \\vec{r}_v$$\n\n"
              "Perpendicular a ambos tangentes, así perpendicular al plano tangente.\n\n"
              "**Plano tangente** en $(u_0, v_0)$:\n\n"
              "$$\\vec{r}_u(u_0, v_0) \\cdot (P - \\vec{r}(u_0, v_0)) = 0$$\n\n"
              "(usando $\\vec{n}$ como vector normal)."
          )),

        fig(
            "Superficie paramétrica con vectores tangentes y normal. Vista isométrica 3D de una "
            "superficie ondulada r(u, v) en color teal claro semi-translúcido. En un punto P "
            "destacado sobre la superficie, dibujar dos vectores tangentes: r_u (en color azul) a "
            "lo largo de la curva 'u' (curva con v constante) y r_v (en color ámbar) a lo largo "
            "de la curva 'v' (curva con u constante). Su producto cruz r_u × r_v como un vector "
            "perpendicular saliendo del plano tangente, en color verde grueso, etiquetado 'n = "
            "r_u × r_v'. Las dos curvas paramétricas dibujadas en la superficie con líneas más "
            "delgadas. Etiquetas claras: 'P', 'r_u', 'r_v', 'n'. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Esfera paramétrica",
          problema_md="Para $\\vec{r}(\\theta, \\varphi) = \\langle \\sin\\varphi\\cos\\theta, \\sin\\varphi\\sin\\theta, \\cos\\varphi \\rangle$ (esfera unitaria), calcular $\\vec{r}_\\theta$, $\\vec{r}_\\varphi$ y la normal.",
          pasos=[
              {"accion_md": "**Parciales:**\n\n"
                            "$\\vec{r}_\\theta = \\langle -\\sin\\varphi\\sin\\theta, \\sin\\varphi\\cos\\theta, 0 \\rangle$.\n\n"
                            "$\\vec{r}_\\varphi = \\langle \\cos\\varphi\\cos\\theta, \\cos\\varphi\\sin\\theta, -\\sin\\varphi \\rangle$.",
               "justificacion_md": "Derivar componente a componente respecto a cada parámetro.",
               "es_resultado": False},
              {"accion_md": "**Producto cruz** (después de cálculo):\n\n"
                            "$\\vec{r}_\\theta \\times \\vec{r}_\\varphi = -\\sin\\varphi \\langle \\sin\\varphi\\cos\\theta, \\sin\\varphi\\sin\\theta, \\cos\\varphi \\rangle = -\\sin\\varphi \\cdot \\vec{r}$.",
               "justificacion_md": "**Resultado clásico:** la normal a la esfera es proporcional al vector posición $\\vec{r}$. Geométricamente: la normal al punto $P$ de la esfera apunta en la dirección de $\\overrightarrow{OP}$.",
               "es_resultado": False},
              {"accion_md": "**$\\|\\vec{r}_\\theta \\times \\vec{r}_\\varphi\\| = \\sin\\varphi$**.\n\n"
                            "(Esto será $dS$ en la lección 3.2 — anticipo.)",
               "justificacion_md": "**Atención al signo:** dependiendo del orden $\\vec{r}_\\theta \\times \\vec{r}_\\varphi$ vs $\\vec{r}_\\varphi \\times \\vec{r}_\\theta$, el normal apunta hacia adentro o hacia afuera de la esfera.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Curvas u y curvas v como una cuadrícula sobre la superficie",
          body_md=(
              "Las **curvas $u$** (con $v$ constante) y las **curvas $v$** (con $u$ constante) forman una **cuadrícula** sobre la superficie — análoga a las líneas del meridiano y el paralelo en una esfera.\n\n"
              "**En el dominio $D$:** cuadrícula rectangular en $(u, v)$.\n"
              "**En la superficie:** cuadrícula deformada (curvada) sobre $S$.\n\n"
              "**Vectores tangentes $\\vec{r}_u, \\vec{r}_v$:** dirección de cada familia de curvas.\n\n"
              "**Producto cruz:** perpendicular a ambas direcciones — a la superficie.\n\n"
              "**Magnitud del producto cruz:** área del paralelogramo determinado por $\\vec{r}_u, \\vec{r}_v$ — este será el **factor de área** $dS$ en la próxima lección."
          )),

        b("ejemplo_resuelto",
          titulo="Plano tangente a una superficie paramétrica",
          problema_md=(
              "Para $\\vec{r}(u, v) = \\langle u, v, u^2 + v^2 \\rangle$ (paraboloide), hallar el plano tangente en $(1, 1, 2)$ — es decir, $u = v = 1$."
          ),
          pasos=[
              {"accion_md": "**Parciales:** $\\vec{r}_u = \\langle 1, 0, 2u \\rangle$, $\\vec{r}_v = \\langle 0, 1, 2v \\rangle$.\n\n"
                            "**En $(u, v) = (1, 1)$:** $\\vec{r}_u = \\langle 1, 0, 2 \\rangle$, $\\vec{r}_v = \\langle 0, 1, 2 \\rangle$.",
               "justificacion_md": "Estándar.",
               "es_resultado": False},
              {"accion_md": "**Normal:** $\\vec{n} = \\vec{r}_u \\times \\vec{r}_v = \\langle -2, -2, 1 \\rangle$.",
               "justificacion_md": "Producto cruz componente a componente.",
               "es_resultado": False},
              {"accion_md": "**Plano tangente** en el punto $(1, 1, 2)$:\n\n"
                            "$-2(x - 1) - 2(y - 1) + (z - 2) = 0 \\implies -2x - 2y + z + 2 = 0 \\implies 2x + 2y - z = 2$.",
               "justificacion_md": "**Verificación con la fórmula tradicional para gráficas $z = f(x,y)$:** $z = x^2 + y^2$, $f_x = 2, f_y = 2$ en $(1,1)$. Plano tangente: $z = 2 + 2(x-1) + 2(y-1) = 2x + 2y - 2$. Equivalente: $z - 2x - 2y = -2$. ✓ (mismo plano salvo signo).",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El vector normal a una superficie paramétrica $\\vec{r}(u, v)$ es:",
                  "opciones_md": [
                      "$\\vec{r}(u, v)$",
                      "$\\vec{r}_u + \\vec{r}_v$",
                      "$\\vec{r}_u \\times \\vec{r}_v$",
                      "$\\vec{r}_u \\cdot \\vec{r}_v$",
                  ],
                  "correcta": "C",
                  "pista_md": "Producto cruz da un vector perpendicular a ambos tangentes.",
                  "explicacion_md": (
                      "$\\vec{n} = \\vec{r}_u \\times \\vec{r}_v$ es perpendicular a $\\vec{r}_u$ y $\\vec{r}_v$, así perpendicular al plano tangente."
                  ),
              },
              {
                  "enunciado_md": "Para una gráfica $z = f(x, y)$ parametrizada como $\\vec{r}(u, v) = \\langle u, v, f(u, v) \\rangle$, $\\vec{r}_u \\times \\vec{r}_v = ?$",
                  "opciones_md": [
                      "$\\langle f_u, f_v, 1 \\rangle$",
                      "$\\langle -f_u, -f_v, 1 \\rangle$",
                      "$\\langle 1, 1, f_u + f_v \\rangle$",
                      "$\\langle 0, 0, 1 \\rangle$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\vec{r}_u = \\langle 1, 0, f_u \\rangle$, $\\vec{r}_v = \\langle 0, 1, f_v \\rangle$.",
                  "explicacion_md": (
                      "Producto cruz: $\\langle (0)(f_v) - (f_u)(1), (f_u)(0) - (1)(f_v), (1)(1) - (0)(0) \\rangle = \\langle -f_u, -f_v, 1 \\rangle$."
                  ),
              },
          ]),

        ej(
            titulo="Cilindro paramétrico",
            enunciado=(
                "Para $\\vec{r}(\\theta, z) = \\langle 2\\cos\\theta, 2\\sin\\theta, z \\rangle$ (cilindro de radio 2), "
                "calcula el vector normal $\\vec{r}_\\theta \\times \\vec{r}_z$."
            ),
            pistas=[
                "$\\vec{r}_\\theta = \\langle -2\\sin\\theta, 2\\cos\\theta, 0 \\rangle$.",
                "$\\vec{r}_z = \\langle 0, 0, 1 \\rangle$.",
            ],
            solucion=(
                "$\\vec{r}_\\theta \\times \\vec{r}_z = \\langle 2\\cos\\theta, 2\\sin\\theta, 0 \\rangle$.\n\n"
                "**Magnitud:** $2$. **Apunta radialmente hacia afuera** desde el eje $z$ — confirma la geometría del cilindro."
            ),
        ),

        ej(
            titulo="Superficie de revolución",
            enunciado=(
                "Parametriza la superficie obtenida al rotar $y = e^x$ alrededor del eje $x$ y calcula $\\vec{r}_u \\times \\vec{r}_v$."
            ),
            pistas=[
                "Tabla: $\\vec{r}(x, \\theta) = \\langle x, e^x \\cos\\theta, e^x \\sin\\theta \\rangle$.",
                "$\\vec{r}_x = \\langle 1, e^x\\cos\\theta, e^x\\sin\\theta \\rangle$.",
                "$\\vec{r}_\\theta = \\langle 0, -e^x\\sin\\theta, e^x\\cos\\theta \\rangle$.",
            ],
            solucion=(
                "$\\vec{r}_x \\times \\vec{r}_\\theta = \\langle e^{2x}, -e^x\\cos\\theta, -e^x\\sin\\theta \\rangle$.\n\n"
                "Magnitud: $\\sqrt{e^{4x} + e^{2x}} = e^x\\sqrt{e^{2x} + 1}$.\n\n"
                "**Será el integrando** para calcular el área de la superficie en la próxima lección."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir parametrización con función.** Una superficie tiene infinitas parametrizaciones — la geometría es invariante.",
              "**Olvidar el dominio $D$.** La parametrización solo describe una porción de superficie según el dominio elegido.",
              "**Calcular $\\vec{r}_v \\times \\vec{r}_u$ en vez de $\\vec{r}_u \\times \\vec{r}_v$.** Apuntan a lados opuestos — orientación opuesta.",
              "**Asumir que toda superficie es gráfica $z = f(x, y)$.** Esferas completas, cilindros laterales no lo son.",
              "**Olvidar que el normal tiene magnitud variable.** $\\|\\vec{r}_u \\times \\vec{r}_v\\|$ no es 1 en general.",
          ]),

        b("resumen",
          puntos_md=[
              "**Superficie paramétrica:** $\\vec{r}(u, v): D \\to \\mathbb{R}^3$.",
              "**Curvas $u$ y curvas $v$** forman cuadrícula sobre $S$.",
              "**Tangentes:** $\\vec{r}_u, \\vec{r}_v$.",
              "**Normal:** $\\vec{n} = \\vec{r}_u \\times \\vec{r}_v$.",
              "**Magnitud del normal** $= \\|\\vec{r}_u \\times \\vec{r}_v\\|$ — factor de área (próxima lección).",
              "**Parametrizaciones clásicas:** gráfica, esfera, cilindro, cono, superficie de revolución.",
              "**Próxima lección:** integral de superficie escalar $\\iint_S f \\, dS$.",
          ]),
    ]
    return {
        "id": "lec-vec-3-1-superficies-parametricas",
        "title": "Superficies paramétricas",
        "description": "$\\vec{r}(u, v)$, vectores tangentes, vector normal $\\vec{r}_u \\times \\vec{r}_v$, plano tangente.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 3.2 Integral de superficie
# =====================================================================
def lesson_3_2():
    blocks = [
        b("texto", body_md=(
            "La **integral de superficie de un campo escalar** generaliza la integral de línea escalar a "
            "superficies en lugar de curvas. La fórmula central usa el **factor de área** "
            "$dS = \\|\\vec{r}_u \\times \\vec{r}_v\\| \\, du \\, dv$ — el análogo 2D del $ds = \\|\\vec{r}'\\| dt$ "
            "que vimos para curvas.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y calcular $\\iint_S f \\, dS$.\n"
            "- Reconocer el caso especial **$f = 1$**: área de la superficie.\n"
            "- Aplicar a **masa y centro de masa** de láminas en 3D.\n"
            "- Manejar parametrizaciones específicas (esfera, cilindro, gráfica)."
        )),

        b("definicion",
          titulo="Integral de superficie en campo escalar",
          body_md=(
              "Sea $S$ una superficie suave parametrizada por $\\vec{r}(u, v)$, $(u, v) \\in D$, y $f$ un campo escalar continuo en $S$:\n\n"
              "$$\\iint_S f \\, dS = \\iint_D f(\\vec{r}(u, v)) \\, \\|\\vec{r}_u \\times \\vec{r}_v\\| \\, du \\, dv$$\n\n"
              "**Elemento de área superficial:** $dS = \\|\\vec{r}_u \\times \\vec{r}_v\\| \\, du \\, dv$.\n\n"
              "**Caso especial $f \\equiv 1$:** $\\iint_S 1 \\, dS = \\text{Area}(S)$ — recupera el área de superficie de Cálculo Multivariable 7.3.\n\n"
              "**Para gráfica $z = f(x, y)$:** $\\|\\vec{r}_u \\times \\vec{r}_v\\| = \\sqrt{1 + f_x^2 + f_y^2}$ — la fórmula familiar."
          )),

        b("ejemplo_resuelto",
          titulo="Integral sobre la esfera",
          problema_md=(
              "Calcular $\\iint_S z \\, dS$ donde $S$ es la esfera unitaria."
          ),
          pasos=[
              {"accion_md": "**Parametrización (esféricas):** $\\vec{r}(\\theta, \\varphi) = \\langle \\sin\\varphi\\cos\\theta, \\sin\\varphi\\sin\\theta, \\cos\\varphi \\rangle$, "
                            "$\\theta \\in [0, 2\\pi], \\varphi \\in [0, \\pi]$.\n\n"
                            "**De la lección anterior:** $\\|\\vec{r}_\\theta \\times \\vec{r}_\\varphi\\| = \\sin\\varphi$.",
               "justificacion_md": "Reuso del cálculo previo.",
               "es_resultado": False},
              {"accion_md": "**$z = \\cos\\varphi$ en la parametrización.** Aplicar:\n\n"
                            "$\\iint_S z \\, dS = \\int_0^{2\\pi} \\int_0^\\pi \\cos\\varphi \\cdot \\sin\\varphi \\, d\\varphi \\, d\\theta$.",
               "justificacion_md": "Sustitución directa.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^\\pi \\cos\\varphi \\sin\\varphi \\, d\\varphi = \\dfrac{1}{2}\\int_0^\\pi \\sin(2\\varphi) \\, d\\varphi = \\dfrac{1}{2}\\left[-\\dfrac{\\cos(2\\varphi)}{2}\\right]_0^\\pi = 0$.\n\n"
                            "**Resultado: $0$.**",
               "justificacion_md": "**Por simetría:** la esfera es simétrica respecto al plano $z = 0$. La función $z$ es impar en $z$. La integral se anula. ✓",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Área de la esfera",
          problema_md="Verificar que el área de la esfera unitaria es $4\\pi$.",
          pasos=[
              {"accion_md": "$\\text{Area}(S) = \\iint_S 1 \\, dS = \\int_0^{2\\pi}\\int_0^\\pi \\sin\\varphi \\, d\\varphi \\, d\\theta$.",
               "justificacion_md": "Integrar $1$ sobre la esfera.",
               "es_resultado": False},
              {"accion_md": "$\\int_0^\\pi \\sin\\varphi \\, d\\varphi = 2$. $\\int_0^{2\\pi} 2 \\, d\\theta = 4\\pi$. ✓",
               "justificacion_md": "**Recupera la fórmula clásica $4\\pi R^2$ con $R = 1$.**",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Aplicaciones físicas",
          body_md=(
              "**Masa de una lámina** con densidad $\\rho(x, y, z)$:\n\n"
              "$$M = \\iint_S \\rho \\, dS$$\n\n"
              "**Centro de masa:**\n\n"
              "$$\\bar{x} = \\dfrac{1}{M}\\iint_S x \\rho \\, dS, \\quad \\bar{y} = \\dfrac{1}{M}\\iint_S y\\rho \\, dS, \\quad \\bar{z} = \\dfrac{1}{M}\\iint_S z\\rho \\, dS$$\n\n"
              "**Momento de inercia respecto al eje $z$:**\n\n"
              "$$I_z = \\iint_S (x^2 + y^2) \\rho \\, dS$$\n\n"
              "**Carga total** sobre una superficie con densidad superficial de carga $\\sigma$:\n\n"
              "$$Q = \\iint_S \\sigma \\, dS$$"
          )),

        b("ejemplo_resuelto",
          titulo="Centroide de un hemisferio",
          problema_md=(
              "Calcular el centroide del hemisferio superior $S = \\{x^2 + y^2 + z^2 = 1, z \\geq 0\\}$."
          ),
          pasos=[
              {"accion_md": "**Por simetría:** $\\bar{x} = \\bar{y} = 0$. Solo necesitamos $\\bar{z}$.\n\n"
                            "**Área del hemisferio:** $2\\pi$ (mitad de $4\\pi$).",
               "justificacion_md": "Simetría rotacional respecto al eje $z$.",
               "es_resultado": False},
              {"accion_md": "$\\iint_S z \\, dS = \\int_0^{2\\pi}\\int_0^{\\pi/2} \\cos\\varphi \\cdot \\sin\\varphi \\, d\\varphi \\, d\\theta$.\n\n"
                            "$\\int_0^{\\pi/2} \\cos\\varphi \\sin\\varphi \\, d\\varphi = \\dfrac{1}{2}$. Externa: $\\dfrac{1}{2} \\cdot 2\\pi = \\pi$.",
               "justificacion_md": "Hemisferio superior: $\\varphi \\in [0, \\pi/2]$.",
               "es_resultado": False},
              {"accion_md": "$\\bar{z} = \\dfrac{\\pi}{2\\pi} = \\dfrac{1}{2}$.\n\n"
                            "**Centroide:** $(0, 0, 1/2)$. **El centroide está a la mitad de la altura** del hemisferio (no en el centro de la bola, que sería más abajo).",
               "justificacion_md": "**Resultado clásico** en mecánica de cuerpos rígidos.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Independencia de la parametrización",
          body_md=(
              "Como con curvas y campos escalares, **$\\iint_S f \\, dS$ no depende de la parametrización**. "
              "Es una propiedad geométrica de $S$ y $f$.\n\n"
              "Por eso podemos elegir la parametrización que **simplifique más**:\n\n"
              "- Esferas: esféricas $(\\theta, \\varphi)$.\n"
              "- Cilindros: $(\\theta, z)$.\n"
              "- Gráficas $z = f(x, y)$: cartesianas $(x, y)$.\n\n"
              "Las distintas parametrizaciones dan el mismo resultado — solo cambia la facilidad del cálculo."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El elemento $dS$ en una superficie paramétrica es:",
                  "opciones_md": [
                      "$du \\, dv$",
                      "$\\|\\vec{r}_u\\| \\|\\vec{r}_v\\| \\, du \\, dv$",
                      "$\\|\\vec{r}_u \\times \\vec{r}_v\\| \\, du \\, dv$",
                      "$|\\vec{r}_u \\cdot \\vec{r}_v| \\, du \\, dv$",
                  ],
                  "correcta": "C",
                  "pista_md": "Magnitud del producto cruz da el área del paralelogramo tangente.",
                  "explicacion_md": (
                      "$dS = \\|\\vec{r}_u \\times \\vec{r}_v\\| \\, du \\, dv$ — área del paralelogramo en cada punto, integrada sobre $D$."
                  ),
              },
              {
                  "enunciado_md": "$\\iint_S 1 \\, dS$ es:",
                  "opciones_md": [
                      "Cero",
                      "Volumen encerrado por $S$",
                      "Área de $S$",
                      "Perímetro de la frontera de $S$",
                  ],
                  "correcta": "C",
                  "pista_md": "Análogo a $\\int_C 1 \\, ds$ para longitud.",
                  "explicacion_md": (
                      "Integrar $1$ sobre $S$ da el área. Generaliza $\\int_C 1 \\, ds = $ longitud."
                  ),
              },
          ]),

        ej(
            titulo="Integral sobre cilindro",
            enunciado=(
                "Calcula $\\iint_S z \\, dS$ donde $S$ es el cilindro lateral $x^2 + y^2 = 1$ con $0 \\leq z \\leq 2$."
            ),
            pistas=[
                "Parametrización: $\\vec{r}(\\theta, z) = \\langle \\cos\\theta, \\sin\\theta, z \\rangle$, $\\theta \\in [0, 2\\pi], z \\in [0, 2]$.",
                "$\\|\\vec{r}_\\theta \\times \\vec{r}_z\\| = 1$ (cilindro de radio 1).",
            ],
            solucion=(
                "$\\iint_S z \\, dS = \\int_0^{2\\pi}\\int_0^2 z \\cdot 1 \\, dz \\, d\\theta = 2\\pi \\cdot 2 = 4\\pi$."
            ),
        ),

        ej(
            titulo="Área de gráfica",
            enunciado=(
                "Calcula el área de la parte del paraboloide $z = x^2 + y^2$ con $0 \\leq z \\leq 1$."
            ),
            pistas=[
                "Sobre el disco $x^2 + y^2 \\leq 1$. $f_x = 2x, f_y = 2y$.",
                "$dS = \\sqrt{1 + 4x^2 + 4y^2} \\, dA$.",
                "Polares.",
            ],
            solucion=(
                "$A = \\int_0^{2\\pi}\\int_0^1 \\sqrt{1 + 4r^2} \\cdot r \\, dr \\, d\\theta$.\n\n"
                "Sustitución $u = 1 + 4r^2$, $du = 8r \\, dr$: $\\dfrac{1}{8}\\int_1^5 u^{1/2} \\, du = \\dfrac{1}{8} \\cdot \\dfrac{2}{3}(5\\sqrt{5} - 1) = \\dfrac{5\\sqrt{5} - 1}{12}$.\n\n"
                "Externa: $A = 2\\pi \\cdot \\dfrac{5\\sqrt{5} - 1}{12} = \\dfrac{\\pi(5\\sqrt{5} - 1)}{6}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $\\|\\vec{r}_u \\times \\vec{r}_v\\|$.** Sin él, no es la integral correcta.",
              "**Confundir $dS$ (área) con $d\\vec{S}$ (vector orientado).** El segundo aparece en integrales vectoriales (lección 3.4).",
              "**Aplicar fórmula de gráfica $\\sqrt{1 + f_x^2 + f_y^2}$** a superficies que no son gráficas. Para esferas, conos verticales, etc., usar parametrización adecuada.",
              "**Confundir parametrización con función definida en la superficie.** $f(\\vec{r}(u, v))$ es $f$ evaluada en el punto $\\vec{r}(u, v)$, no $f$ compuesta con $\\vec{r}$ en sentido funcional general.",
              "**Asumir que el resultado es siempre positivo.** Si $f$ cambia signo, $\\iint f \\, dS$ puede ser cero o negativo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Integral de superficie escalar:** $\\iint_S f \\, dS = \\iint_D f(\\vec{r}(u, v)) \\, \\|\\vec{r}_u \\times \\vec{r}_v\\| \\, du \\, dv$.",
              "**$dS$:** elemento de área superficial.",
              "**Caso $f = 1$:** área de $S$.",
              "**Aplicaciones:** masa, centro de masa, momento de inercia, carga eléctrica.",
              "**Independiente** de la parametrización.",
              "**Próxima lección:** orientación de superficies (preludio a integrales vectoriales).",
          ]),
    ]
    return {
        "id": "lec-vec-3-2-integral-superficie",
        "title": "Integral de superficie",
        "description": "$\\iint_S f \\, dS$ con $dS = \\|\\vec{r}_u \\times \\vec{r}_v\\| \\, du \\, dv$. Área, masa, centro de masa.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 3.3 Superficies orientadas
# =====================================================================
def lesson_3_3():
    blocks = [
        b("texto", body_md=(
            "Antes de integrar campos vectoriales sobre superficies, necesitamos definir un concepto sutil "
            "pero central: la **orientación** de una superficie. Es la elección de una **dirección normal** "
            "consistente. Para casi todas las superficies que veremos hay dos elecciones — pero existen "
            "superficies 'patológicas' (Möbius) donde **ninguna elección consistente es posible**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir **orientación** y **normal unitario**.\n"
            "- Distinguir superficies **orientables** (con dos lados) de las **no orientables** (Möbius).\n"
            "- Aplicar la convención de **normal exterior** a superficies cerradas.\n"
            "- Reconocer la **orientación inducida** en la frontera (regla de la mano derecha)."
        )),

        b("definicion",
          titulo="Superficie orientada",
          body_md=(
              "Una **superficie orientada** es una superficie $S$ con una elección de **vector normal unitario** $\\vec{n}$ que **varía continuamente** sobre $S$.\n\n"
              "Para una superficie paramétrica suave $\\vec{r}(u, v)$:\n\n"
              "$$\\vec{n} = \\dfrac{\\vec{r}_u \\times \\vec{r}_v}{\\|\\vec{r}_u \\times \\vec{r}_v\\|}$$\n\n"
              "Este es **un** vector normal — el otro es $-\\vec{n}$. Elegir cuál depende de la orientación deseada.\n\n"
              "**Para una gráfica $z = f(x, y)$:** la fórmula de la lección 3.1 da $\\langle -f_x, -f_y, 1 \\rangle$ — apunta hacia arriba (componente $z$ positiva). El opuesto $\\langle f_x, f_y, -1 \\rangle$ apunta hacia abajo."
          )),

        b("intuicion",
          titulo="Dos lados — el caso típico",
          body_md=(
              "**Casi todas las superficies de la vida cotidiana** tienen **dos lados** distinguibles:\n\n"
              "- Una hoja de papel: lado A y lado B.\n"
              "- Una esfera: dentro y fuera.\n"
              "- Un cilindro abierto: interior y exterior.\n\n"
              "**Elegir la orientación = elegir un lado.** El normal $\\vec{n}$ apunta hacia el lado elegido (saliendo perpendicular a la superficie).\n\n"
              "**Si caminas por la superficie llevando $\\vec{n}$ hacia 'arriba'**, no importa qué camino tomes: $\\vec{n}$ vuelve siempre apuntando al mismo lado. Eso es **orientabilidad**."
          )),

        fig(
            "Cinta de Möbius. Vista isométrica 3D de una cinta de Möbius (cinta retorcida pegada por "
            "los extremos invertidos), en color teal. Mostrar una hormiga estilizada caminando "
            "sobre la superficie con el vector normal n apuntando 'hacia arriba'. Indicar con una "
            "flecha curva que tras una vuelta completa, la hormiga vuelve al mismo punto pero del "
            "'otro lado' — el vector normal ha invertido su dirección. Etiquetas: 'Cinta de "
            "Möbius', 'una sola cara', 'no orientable'. " + STYLE
        ),

        b("definicion",
          titulo="Superficies no orientables — Möbius",
          body_md=(
              "Existen superficies donde **no hay manera consistente de elegir un normal**: caminando por la superficie y volviendo al mismo punto, el normal se ha **invertido**.\n\n"
              "**Ejemplo clásico: cinta de Möbius.** Tomar una cinta de papel, torcerla 180° y pegar los extremos. Tiene **una sola cara** (caminando por ella se llega al 'otro lado' sin levantar el dedo).\n\n"
              "**Otra:** botella de Klein (no se puede construir físicamente en $\\mathbb{R}^3$ sin autointersección).\n\n"
              "**Para los teoremas de Stokes y la divergencia:** **se requiere superficie orientable**. La cinta de Möbius es una curiosidad teórica — todas las superficies que aparecen en física estándar son orientables."
          )),

        b("definicion",
          titulo="Convención: normal exterior en superficies cerradas",
          body_md=(
              "Una superficie es **cerrada** si encierra un volumen finito (esfera, cubo, toro). Para superficies cerradas, hay una elección **canónica** de orientación: el **normal exterior** apunta **hacia afuera** del volumen encerrado.\n\n"
              "**Esta es la convención del teorema de la divergencia** (lección 3.7).\n\n"
              "**Para superficies abiertas con frontera** (como un hemisferio, un disco, la cinta lateral de un cilindro): no hay 'afuera' canónico — se debe elegir la orientación explícitamente."
          )),

        b("definicion",
          titulo="Orientación inducida en la frontera",
          body_md=(
              "Si $S$ es una **superficie con frontera $\\partial S$** y $S$ está orientada con normal $\\vec{n}$, entonces $\\partial S$ recibe una **orientación inducida** mediante la **regla de la mano derecha**:\n\n"
              "**Si el pulgar apunta en la dirección de $\\vec{n}$, los dedos doblados indican el sentido de recorrido de $\\partial S$.**\n\n"
              "Equivalentemente: caminando sobre $S$ a lo largo de $\\partial S$ con el normal $\\vec{n}$ apuntando 'hacia arriba' desde tu cabeza, **la superficie debe quedar a tu izquierda**.\n\n"
              "**Esta es la convención del teorema de Stokes** (lección 3.6).\n\n"
              "**Ejemplo:** si $S$ es el hemisferio superior con normal hacia arriba, $\\partial S$ es el círculo ecuatorial recorrido **antihorariamente** vista desde arriba."
          )),

        b("ejemplo_resuelto",
          titulo="Orientar una esfera y un disco",
          problema_md="Describir las dos orientaciones posibles de la esfera unitaria y del disco unitario en el plano $xy$.",
          pasos=[
              {"accion_md": "**Esfera unitaria** (cerrada):\n\n"
                            "- Orientación 'exterior' (canónica): $\\vec{n}$ apunta **hacia afuera** desde el origen. En cada punto $P$ de la esfera, $\\vec{n}(P) = P$ (el vector posición).\n"
                            "- Orientación 'interior': $\\vec{n}(P) = -P$.",
               "justificacion_md": "Las dos opciones — la canónica es la exterior por convención.",
               "es_resultado": False},
              {"accion_md": "**Disco unitario** $\\{x^2+y^2 \\leq 1, z = 0\\}$ (con frontera = círculo unitario):\n\n"
                            "- $\\vec{n} = \\vec{k}$ (apunta hacia arriba): frontera inducida es el círculo recorrido **antihorariamente**.\n"
                            "- $\\vec{n} = -\\vec{k}$ (hacia abajo): frontera inducida es **horaria**.",
               "justificacion_md": "**Aplicación de la regla de la mano derecha.** **Las dos orientaciones son válidas** — las elegimos según el problema.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La cinta de Möbius es:",
                  "opciones_md": [
                      "Cerrada y orientable",
                      "Abierta y orientable",
                      "Orientable",
                      "No orientable",
                  ],
                  "correcta": "D",
                  "pista_md": "Tiene una sola cara — el normal se invierte al recorrerla.",
                  "explicacion_md": (
                      "**No orientable.** No hay manera consistente de elegir $\\vec{n}$. Por eso los teoremas de Stokes y divergencia no aplican."
                  ),
              },
              {
                  "enunciado_md": "Para superficie cerrada (esfera, cubo, etc.), la orientación canónica es:",
                  "opciones_md": [
                      "Hacia adentro",
                      "Hacia afuera",
                      "Tangencial",
                      "Cualquiera",
                  ],
                  "correcta": "B",
                  "pista_md": "Convención del teorema de la divergencia.",
                  "explicacion_md": (
                      "**Hacia afuera** (normal exterior). Es la convención usada en el teorema de la divergencia y casi toda la física (ley de Gauss, etc.)."
                  ),
              },
          ]),

        ej(
            titulo="Orientación del cilindro lateral",
            enunciado=(
                "El cilindro $x^2 + y^2 = 1$ con $0 \\leq z \\leq 1$ tiene dos orientaciones. Describe ambas y "
                "determina cuál corresponde al normal exterior si tapamos las bases para hacerlo cerrado."
            ),
            pistas=[
                "Parametrizar: $\\vec{r}(\\theta, z) = \\langle \\cos\\theta, \\sin\\theta, z \\rangle$.",
                "$\\vec{r}_\\theta \\times \\vec{r}_z = \\langle \\cos\\theta, \\sin\\theta, 0 \\rangle$ — apunta radial hacia afuera.",
            ],
            solucion=(
                "**Opción 1:** $\\vec{n} = \\langle \\cos\\theta, \\sin\\theta, 0 \\rangle$ — radial **hacia afuera** desde el eje $z$.\n\n"
                "**Opción 2:** $\\vec{n} = \\langle -\\cos\\theta, -\\sin\\theta, 0 \\rangle$ — radial **hacia adentro**.\n\n"
                "**Si tapamos las bases:** el normal exterior del cilindro completo apunta hacia afuera del volumen — es la **Opción 1** en la cara lateral. (Las tapas tienen normales $\\pm \\vec{k}$ apuntando fuera del cilindro.)"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**No considerar las dos opciones de orientación.** Cada superficie tiene **dos** orientaciones — el problema indica cuál.",
              "**Aplicar Stokes o divergencia a superficies no orientables.** Los teoremas no valen — Möbius y Klein son contraejemplos.",
              "**Confundir orientación de $S$ con orientación de $\\partial S$.** Una induce la otra mediante la regla de la mano derecha, pero son cosas diferentes.",
              "**Usar normal interior** en superficies cerradas sin justificación. La convención es exterior; de no serlo, hay que ser explícito.",
              "**Asumir que toda superficie tiene 'arriba' y 'abajo'.** Para una esfera, lo correcto es 'fuera' y 'dentro'.",
          ]),

        b("resumen",
          puntos_md=[
              "**Orientación:** elección continua de normal unitario $\\vec{n}$.",
              "**Dos lados:** casi todas las superficies son orientables (dos elecciones).",
              "**No orientables:** Möbius, Klein — sin orientación consistente.",
              "**Superficies cerradas:** convención de normal exterior.",
              "**Frontera $\\partial S$:** orientación inducida por regla de la mano derecha.",
              "**Próxima lección:** integrales de superficie de campos vectoriales (donde la orientación importa).",
          ]),
    ]
    return {
        "id": "lec-vec-3-3-orientadas",
        "title": "Superficies orientadas",
        "description": "Orientación, vector normal unitario, superficies con dos lados vs no orientables (Möbius), regla de la mano derecha.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# 3.4 Integrales de superficie de campos vectoriales
# =====================================================================
def lesson_3_4():
    blocks = [
        b("texto", body_md=(
            "La **integral de superficie de un campo vectorial** mide el **flujo** de $\\vec{F}$ a través "
            "de $S$ — cuánto del campo 'atraviesa' la superficie por unidad de tiempo, contado en la "
            "dirección del normal $\\vec{n}$. Es la generalización 3D del flujo de Green (lección 2.6) y "
            "el ingrediente central del teorema de la divergencia.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y calcular $\\iint_S \\vec{F} \\cdot d\\vec{S}$.\n"
            "- Comprender la **interpretación física** como flujo.\n"
            "- Manejar las **dos notaciones**: $\\vec{F} \\cdot \\vec{n} \\, dS$ y $\\vec{F} \\cdot (\\vec{r}_u \\times \\vec{r}_v) \\, du \\, dv$.\n"
            "- Reconocer que **invertir la orientación cambia el signo**."
        )),

        b("definicion",
          titulo="Flujo de un campo vectorial",
          body_md=(
              "Sea $S$ una superficie orientada con normal unitario $\\vec{n}$, y $\\vec{F}$ un campo vectorial continuo. El **flujo** de $\\vec{F}$ a través de $S$ es:\n\n"
              "$$\\iint_S \\vec{F} \\cdot d\\vec{S} = \\iint_S \\vec{F} \\cdot \\vec{n} \\, dS$$\n\n"
              "**Cálculo con parametrización** $\\vec{r}(u, v)$:\n\n"
              "$$\\iint_S \\vec{F} \\cdot d\\vec{S} = \\iint_D \\vec{F}(\\vec{r}(u, v)) \\cdot (\\vec{r}_u \\times \\vec{r}_v) \\, du \\, dv$$\n\n"
              "**Notación:** $d\\vec{S} = \\vec{n} \\, dS = (\\vec{r}_u \\times \\vec{r}_v) \\, du \\, dv$ — vector con magnitud $dS$ y dirección $\\vec{n}$.\n\n"
              "**Si elegimos la orientación opuesta:** la integral cambia de signo."
          )),

        b("intuicion",
          titulo="Flujo: cuánto fluido atraviesa por unidad de tiempo",
          body_md=(
              "**Imagen física:** $\\vec{F}$ es la velocidad de un fluido. **El flujo** $\\iint_S \\vec{F} \\cdot \\vec{n} \\, dS$ es el **volumen de fluido por unidad de tiempo** que atraviesa $S$ en la dirección de $\\vec{n}$.\n\n"
              "- Si $\\vec{F}$ es paralelo a $S$ (perpendicular a $\\vec{n}$): no atraviesa, flujo $= 0$.\n"
              "- Si $\\vec{F}$ es paralelo a $\\vec{n}$: atraviesa máximo.\n"
              "- En general: solo la **componente normal** $\\vec{F} \\cdot \\vec{n}$ contribuye.\n\n"
              "**En electromagnetismo:** $\\iint_S \\vec{E} \\cdot d\\vec{S}$ es el **flujo eléctrico**. La ley de Gauss dice que es proporcional a la carga encerrada (próxima lección).\n\n"
              "**En mecánica de fluidos:** el flujo a través de la frontera de un volumen mide la tasa de cambio de masa adentro."
          )),

        b("ejemplo_resuelto",
          titulo="Flujo a través de la esfera",
          problema_md=(
              "Calcular el flujo del campo radial $\\vec{F}(x, y, z) = \\langle x, y, z \\rangle$ a través de la esfera unitaria con normal exterior."
          ),
          pasos=[
              {"accion_md": "**En la esfera:** $\\vec{n} = \\vec{r}/\\|\\vec{r}\\| = \\vec{r}$ (porque $\\|\\vec{r}\\| = 1$).\n\n"
                            "$\\vec{F} \\cdot \\vec{n} = \\vec{r} \\cdot \\vec{r} = \\|\\vec{r}\\|^2 = 1$.",
               "justificacion_md": "$\\vec{F} = \\vec{r}$ y $\\vec{n} = \\vec{r}$ — están alineados perfectamente.",
               "es_resultado": False},
              {"accion_md": "$\\iint_S \\vec{F} \\cdot \\vec{n} \\, dS = \\iint_S 1 \\, dS = \\text{Area}(S) = 4\\pi$.",
               "justificacion_md": "**Verificación con divergencia (próxima lección 3.7):** $\\nabla \\cdot \\vec{F} = 3$, así $\\iiint_V 3 \\, dV = 3 \\cdot \\dfrac{4\\pi}{3} = 4\\pi$. ✓",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Flujo a través de un plano (caso paramétrico)",
          problema_md=(
              "Calcular el flujo de $\\vec{F} = \\langle 0, 0, x^2 + y^2 \\rangle$ a través del disco $D = \\{x^2+y^2 \\leq 1\\}$ en el plano $z = 0$, con normal $\\vec{k}$."
          ),
          pasos=[
              {"accion_md": "**$\\vec{n} = \\vec{k}$**, $dS = dA$.\n\n"
                            "**$\\vec{F} \\cdot \\vec{n} = x^2 + y^2$.**",
               "justificacion_md": "Componente $z$ del campo.",
               "es_resultado": False},
              {"accion_md": "$\\iint_D (x^2 + y^2) \\, dA = \\int_0^{2\\pi}\\int_0^1 r^2 \\cdot r \\, dr \\, d\\theta = 2\\pi \\cdot 1/4 = \\pi/2$.",
               "justificacion_md": "Polares.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Notación con $dx \\, dy, dy \\, dz, dz \\, dx$",
          body_md=(
              "Existe una notación clásica equivalente. Para $\\vec{F} = \\langle P, Q, R \\rangle$ y $S$ orientada:\n\n"
              "$$\\iint_S \\vec{F} \\cdot d\\vec{S} = \\iint_S P \\, dy \\, dz + Q \\, dz \\, dx + R \\, dx \\, dy$$\n\n"
              "Cada término es la 'proyección' del flujo sobre uno de los planos coordenados.\n\n"
              "**En problemas:** elegir la parametrización adecuada y aplicar $\\vec{F} \\cdot (\\vec{r}_u \\times \\vec{r}_v)$ es generalmente más mecánico que esta notación."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\iint_S \\vec{F} \\cdot d\\vec{S}$ con la orientación opuesta es:",
                  "opciones_md": [
                      "Igual",
                      "El opuesto (cambia de signo)",
                      "Cero",
                      "Doble",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\vec{n}$ se invierte; el producto punto cambia de signo.",
                  "explicacion_md": (
                      "**Cambia de signo.** Es la diferencia clave con $\\iint f \\, dS$ (escalar), que no depende de orientación."
                  ),
              },
              {
                  "enunciado_md": "Si $\\vec{F}$ es tangente a $S$ en cada punto, el flujo es:",
                  "opciones_md": [
                      "Máximo",
                      "Cero",
                      "Igual al área",
                      "Indeterminado",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\vec{F} \\cdot \\vec{n} = 0$ si son perpendiculares.",
                  "explicacion_md": (
                      "$\\vec{F} \\perp \\vec{n}$ (tangente a $S$ ⟺ perpendicular a normal). $\\vec{F} \\cdot \\vec{n} = 0$. **Flujo cero.**"
                  ),
              },
          ]),

        ej(
            titulo="Flujo a través de un cilindro",
            enunciado=(
                "Calcula el flujo de $\\vec{F} = \\langle x, y, 0 \\rangle$ a través de la cara lateral del cilindro $x^2+y^2=1$ con $0 \\leq z \\leq 2$, normal exterior."
            ),
            pistas=[
                "Parametrización: $\\vec{r}(\\theta, z) = \\langle \\cos\\theta, \\sin\\theta, z \\rangle$, $\\vec{r}_\\theta \\times \\vec{r}_z = \\langle \\cos\\theta, \\sin\\theta, 0 \\rangle$.",
                "$\\vec{F}$ en la cara: $\\langle \\cos\\theta, \\sin\\theta, 0 \\rangle$.",
                "Producto punto: $\\cos^2 + \\sin^2 = 1$.",
            ],
            solucion=(
                "$\\vec{F} \\cdot (\\vec{r}_\\theta \\times \\vec{r}_z) = 1$.\n\n"
                "$\\iint = \\int_0^{2\\pi}\\int_0^2 1 \\, dz \\, d\\theta = 4\\pi$.\n\n"
                "**Tiene sentido geométrico:** el campo radial sale por la cara lateral con magnitud 1 (el radio), atravesando un área $2\\pi \\cdot 2 = 4\\pi$ (perímetro × altura). ✓"
            ),
        ),

        ej(
            titulo="Flujo a través de un paraboloide",
            enunciado=(
                "Calcula el flujo de $\\vec{F} = \\langle 0, 0, z \\rangle$ a través del paraboloide $z = x^2 + y^2$ con $z \\leq 1$, "
                "orientado hacia arriba (normal con componente $z$ positiva)."
            ),
            pistas=[
                "$\\vec{r}(x, y) = \\langle x, y, x^2+y^2 \\rangle$, $\\vec{r}_x = \\langle 1, 0, 2x \\rangle$, $\\vec{r}_y = \\langle 0, 1, 2y \\rangle$.",
                "$\\vec{r}_x \\times \\vec{r}_y = \\langle -2x, -2y, 1 \\rangle$ — pero queremos hacia arriba. Esta tiene componente $z = 1 > 0$. ✓",
                "$\\vec{F}$ en la superficie: $\\langle 0, 0, x^2+y^2 \\rangle$.",
            ],
            solucion=(
                "$\\vec{F} \\cdot (\\vec{r}_x \\times \\vec{r}_y) = 0 + 0 + (x^2+y^2)(1) = x^2 + y^2$.\n\n"
                "$\\iint_D (x^2 + y^2) \\, dA = \\int_0^{2\\pi}\\int_0^1 r^2 \\cdot r \\, dr \\, d\\theta = \\dfrac{\\pi}{2}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar la orientación.** Si la orientación está implícita ('normal exterior', 'hacia arriba'), hay que verificar que el cálculo respeta esa orientación.",
              "**Calcular $\\vec{F} \\cdot \\vec{r}$ en lugar de $\\vec{F} \\cdot (\\vec{r}_u \\times \\vec{r}_v)$.** Lo segundo es lo que entra en la integral.",
              "**Confundir $d\\vec{S}$ con $dS$.** El primero es vector orientado; el segundo, escalar positivo.",
              "**Calcular el flujo sin verificar el signo del producto cruz.** Si el cruz no apunta a la orientación deseada, multiplicar por $-1$.",
              "**Dejar $\\vec{F}$ sin evaluar en la superficie.** $\\vec{F}(\\vec{r}(u, v))$ — sustituir cada componente.",
          ]),

        b("resumen",
          puntos_md=[
              "**Flujo:** $\\iint_S \\vec{F} \\cdot d\\vec{S} = \\iint_S \\vec{F} \\cdot \\vec{n} \\, dS$.",
              "**Cálculo:** $\\iint_D \\vec{F}(\\vec{r}(u,v)) \\cdot (\\vec{r}_u \\times \\vec{r}_v) \\, du \\, dv$.",
              "**Interpretación física:** volumen de fluido por unidad de tiempo a través de $S$.",
              "**Orientación importa:** invertir cambia el signo.",
              "**Tangente a $S$:** flujo cero.",
              "**Próxima lección:** aplicaciones físicas y geométricas.",
          ]),
    ]
    return {
        "id": "lec-vec-3-4-flujo",
        "title": "Integrales de superficie de campos vectoriales",
        "description": "Flujo $\\iint_S \\vec{F} \\cdot d\\vec{S}$, dependencia de la orientación, interpretación física.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 4,
    }


# =====================================================================
# 3.5 Aplicaciones
# =====================================================================
def lesson_3_5():
    blocks = [
        b("texto", body_md=(
            "Las integrales de superficie tienen aplicaciones físicas profundas: **flujo de calor**, "
            "**flujo eléctrico**, **caudal de fluidos**, **carga total** sobre una superficie cargada. "
            "Esta lección aplica las herramientas de 3.2 y 3.4 a problemas concretos antes de los grandes "
            "teoremas (Stokes, divergencia).\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular **masa, centro de masa y momentos** de láminas curvas.\n"
            "- Aplicar el flujo a **caudal**, **calor** y **flujo eléctrico**.\n"
            "- Reconocer la **ley de Gauss** electrostática como caso particular del teorema de la divergencia."
        )),

        formulas(
            titulo="Aplicaciones del flujo en física",
            body=(
                "| Magnitud | Fórmula | Significado |\n|---|---|---|\n"
                "| **Caudal** | $\\Phi = \\iint_S \\vec{v} \\cdot d\\vec{S}$ | Volumen de fluido por unidad de tiempo a través de $S$ |\n"
                "| **Flujo de calor** | $Q = -k \\iint_S \\nabla T \\cdot d\\vec{S}$ | Calor transferido por conducción |\n"
                "| **Flujo eléctrico** | $\\Phi_E = \\iint_S \\vec{E} \\cdot d\\vec{S}$ | (Ley de Gauss) |\n"
                "| **Flujo magnético** | $\\Phi_B = \\iint_S \\vec{B} \\cdot d\\vec{S}$ | Aparece en ley de Faraday |\n"
                "| **Tasa de masa** | $\\iint_S \\rho \\vec{v} \\cdot d\\vec{S}$ | Masa por unidad de tiempo |\n\n"
                "**Flujo de calor:** signo $-k$ porque el calor fluye **opuesto** al gradiente de temperatura (de caliente a frío). $k$ = conductividad térmica."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Centro de masa de una semiesfera",
          problema_md=(
              "Una lámina con forma de hemisferio superior $x^2+y^2+z^2 = R^2, z \\geq 0$, tiene densidad superficial constante. Hallar su centro de masa."
          ),
          pasos=[
              {"accion_md": "**Por simetría:** $\\bar{x} = \\bar{y} = 0$. Calculamos $\\bar{z}$.\n\n"
                            "**Área del hemisferio:** $2\\pi R^2$.",
               "justificacion_md": "Simetría rotacional respecto al eje $z$.",
               "es_resultado": False},
              {"accion_md": "**$\\iint_S z \\, dS$:** parametrizar con esféricas.\n\n"
                            "$z = R\\cos\\varphi$, $dS = R^2 \\sin\\varphi \\, d\\varphi \\, d\\theta$.\n\n"
                            "$\\iint = \\int_0^{2\\pi}\\int_0^{\\pi/2} R\\cos\\varphi \\cdot R^2 \\sin\\varphi \\, d\\varphi \\, d\\theta = 2\\pi R^3 \\cdot 1/2 = \\pi R^3$.",
               "justificacion_md": "Hemisferio superior: $\\varphi \\in [0, \\pi/2]$. $\\int_0^{\\pi/2} \\sin\\varphi\\cos\\varphi \\, d\\varphi = 1/2$.",
               "es_resultado": False},
              {"accion_md": "$\\bar{z} = \\dfrac{\\pi R^3}{2\\pi R^2} = \\dfrac{R}{2}$.\n\n"
                            "**Centro de masa:** $(0, 0, R/2)$.",
               "justificacion_md": "**Compárese:** centroide del **hemisferio sólido** (cap 7.1 de Calc Mult): $\\bar{z} = 3R/8$. Distinto, porque aquí solo es la cáscara — no hay masa adentro.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Ley de Gauss (avance del cap. 3.7)",
          body_md=(
              "Una de las cuatro **ecuaciones de Maxwell** del electromagnetismo:\n\n"
              "$$\\oiint_S \\vec{E} \\cdot d\\vec{S} = \\dfrac{Q_{enc}}{\\epsilon_0}$$\n\n"
              "donde $Q_{enc}$ es la carga total encerrada por la superficie $S$ y $\\epsilon_0$ la permitividad del vacío.\n\n"
              "**Como veremos en 3.7** (teorema de la divergencia), esto equivale a:\n\n"
              "$$\\nabla \\cdot \\vec{E} = \\dfrac{\\rho}{\\epsilon_0}$$\n\n"
              "(forma diferencial). **La conexión flujo-divergencia** es el teorema de Gauss matemático aplicado a este caso físico."
          )),

        b("ejemplo_resuelto",
          titulo="Caudal a través de una sección de tubo",
          problema_md=(
              "El agua fluye con velocidad $\\vec{v}(x, y, z) = \\langle 0, 0, 4 - x^2 - y^2 \\rangle$ m/s "
              "(perfil parabólico) por un tubo cilíndrico vertical $x^2+y^2 \\leq 1$. "
              "Calcular el caudal a través del disco $z = 0$."
          ),
          pasos=[
              {"accion_md": "**Disco $D$:** $x^2+y^2 \\leq 1, z = 0$. Normal $\\vec{n} = \\vec{k}$.\n\n"
                            "**$\\vec{v} \\cdot \\vec{n} = 4 - x^2 - y^2$.**",
               "justificacion_md": "El flujo vertical es la componente $z$ de $\\vec{v}$.",
               "es_resultado": False},
              {"accion_md": "**Caudal:** $\\iint_D (4 - x^2 - y^2) \\, dA = \\int_0^{2\\pi}\\int_0^1 (4 - r^2) r \\, dr \\, d\\theta$\n\n"
                            "$= 2\\pi (2 - 1/4) = 2\\pi \\cdot 7/4 = 7\\pi/2$ m³/s.",
               "justificacion_md": "**Lección física:** el perfil parabólico (Poiseuille) da caudal típico de $\\dfrac{1}{2} v_{max} \\cdot A_{tubo}$ — la mitad del caudal si la velocidad fuera uniforme y máxima.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Flujo eléctrico de carga puntual",
          problema_md=(
              "Una carga $Q$ está en el origen. Su campo eléctrico es $\\vec{E}(\\vec{r}) = \\dfrac{kQ}{r^3}\\vec{r}$ con "
              "$r = \\|\\vec{r}\\|$. Calcular el flujo de $\\vec{E}$ a través de la esfera de radio $R$ centrada en el origen."
          ),
          pasos=[
              {"accion_md": "**En la esfera:** $\\vec{n} = \\vec{r}/R$ (exterior). $\\vec{E} \\cdot \\vec{n} = \\dfrac{kQ}{R^3} \\vec{r} \\cdot \\dfrac{\\vec{r}}{R} = \\dfrac{kQ R^2}{R^4} = \\dfrac{kQ}{R^2}$.",
               "justificacion_md": "**Constante** sobre la esfera (campo radial, intensidad uniforme a distancia $R$).",
               "es_resultado": False},
              {"accion_md": "$\\Phi_E = \\iint_S \\vec{E} \\cdot \\vec{n} \\, dS = \\dfrac{kQ}{R^2} \\cdot 4\\pi R^2 = 4\\pi k Q$.\n\n"
                            "**Como $k = 1/(4\\pi \\epsilon_0)$:** $\\Phi_E = Q/\\epsilon_0$.",
               "justificacion_md": "**Resultado clásico:** ley de Gauss recuperada. **El flujo NO depende de $R$** — es la misma para cualquier esfera centrada en la carga (y en general, para cualquier superficie que la encierre).",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Por qué el flujo es independiente de la superficie?",
          body_md=(
              "El resultado anterior — flujo igual para cualquier esfera — se generaliza: **el flujo de $\\vec{E}$ a través de cualquier superficie cerrada que encierre la carga es $Q/\\epsilon_0$**, sin depender de la forma o tamaño.\n\n"
              "**Razón geométrica intuitiva:** las 'líneas de campo' que salen de la carga van al infinito, atravesando exactamente una vez cada superficie que la encierre. El número total no depende de cuál superficie.\n\n"
              "**Rigorosamente:** lo prueba el teorema de la divergencia (lección 3.7). $\\nabla \\cdot \\vec{E} = 0$ excepto en $\\vec{0}$ (donde es una **delta**), así el flujo está concentrado en la carga.\n\n"
              "**Consecuencia útil:** para calcular $\\Phi_E$ por superficies complicadas, basta deformarla a una esfera (más simple), siempre que no se cruce la carga."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El caudal $\\iint_S \\vec{v} \\cdot d\\vec{S}$ tiene unidades de:",
                  "opciones_md": [
                      "Velocidad",
                      "Volumen",
                      "Volumen / tiempo",
                      "Distancia",
                  ],
                  "correcta": "C",
                  "pista_md": "$\\vec{v}$ en m/s, área $dS$ en m². Producto: m³/s.",
                  "explicacion_md": (
                      "**Volumen / tiempo** (m³/s, l/s, etc.). Es el **caudal volumétrico** clásico de hidráulica."
                  ),
              },
              {
                  "enunciado_md": "La ley de Gauss para el flujo eléctrico se escribe:",
                  "opciones_md": [
                      "$\\Phi_E = Q_{enc} \\cdot \\epsilon_0$",
                      "$\\Phi_E = Q_{enc} / \\epsilon_0$",
                      "$\\Phi_E = \\epsilon_0 / Q_{enc}$",
                      "$\\Phi_E = Q_{enc}^2 / \\epsilon_0$",
                  ],
                  "correcta": "B",
                  "pista_md": "Carga sobre permitividad — proporcionalidad lineal.",
                  "explicacion_md": (
                      "$\\oiint \\vec{E} \\cdot d\\vec{S} = Q_{enc}/\\epsilon_0$. **Maxwell I.** Es la base para calcular campos en simetrías (cargas puntuales, planos infinitos, etc.)."
                  ),
              },
          ]),

        ej(
            titulo="Caudal a través de superficie inclinada",
            enunciado=(
                "El campo de velocidad $\\vec{v} = \\langle 0, 0, 5 \\rangle$ m/s atraviesa una placa rectangular "
                "$0 \\leq x \\leq 2$, $0 \\leq y \\leq 3$, en el plano $z = x + y$. Halla el caudal con normal hacia arriba."
            ),
            pistas=[
                "$\\vec{r}(x, y) = \\langle x, y, x+y \\rangle$. $\\vec{r}_x \\times \\vec{r}_y = \\langle -1, -1, 1 \\rangle$ — apunta hacia arriba (componente z positiva). ✓",
                "$\\vec{v} \\cdot (\\vec{r}_x \\times \\vec{r}_y) = (0)(-1) + (0)(-1) + (5)(1) = 5$.",
            ],
            solucion=(
                "$\\iint = \\int_0^3 \\int_0^2 5 \\, dx \\, dy = 5 \\cdot 2 \\cdot 3 = 30$ m³/s.\n\n"
                "**Interpretación:** aunque la placa esté inclinada, **lo único que importa** es la componente del campo en la dirección normal — y el área proyectada al plano $xy$ ($2 \\times 3 = 6$ m²) por la velocidad ($5$ m/s). El cálculo recupera ese producto."
            ),
        ),

        ej(
            titulo="Flujo de calor",
            enunciado=(
                "La temperatura es $T(x, y, z) = x^2 + y^2 + z^2$ (grados). El flujo de calor es "
                "$\\vec{q} = -k\\nabla T$. Calcula el flujo total de calor que sale de la esfera unitaria si $k = 1$."
            ),
            pistas=[
                "$\\nabla T = \\langle 2x, 2y, 2z \\rangle = 2\\vec{r}$.",
                "$\\vec{q} = -2\\vec{r}$. En la esfera: $\\vec{q} \\cdot \\vec{n} = -2\\vec{r} \\cdot \\vec{r} = -2$.",
            ],
            solucion=(
                "$\\Phi = \\iint_S \\vec{q} \\cdot \\vec{n} \\, dS = \\iint_S (-2) \\, dS = -2 \\cdot 4\\pi = -8\\pi$.\n\n"
                "**Negativo:** indica que el calor fluye **hacia adentro** (de afuera hacia el origen). Tiene sentido porque $T$ es mínima en el origen — el calor 'cae' hacia donde es más frío."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir flujo de calor con gradiente de temperatura.** Son opuestos: $\\vec{q} = -k\\nabla T$.",
              "**Olvidar la orientación** al calcular flujo. Cambia el signo.",
              "**Aplicar ley de Gauss sin superficie cerrada.** Solo vale para $\\oiint$.",
              "**Confundir flujo a través de superficie con flujo a través de curva.** $\\iint_S \\vec{F} \\cdot d\\vec{S}$ vs $\\oint_C \\vec{F} \\cdot \\vec{n} \\, ds$ (lección 2.6) — distintos.",
              "**Calcular flujo de campo no físico** sin reflexionar sobre el significado. Cada aplicación tiene su propio campo (calor, eléctrico, etc.).",
          ]),

        b("resumen",
          puntos_md=[
              "**Aplicaciones físicas del flujo:** caudal, calor, flujo eléctrico, magnético.",
              "**Caudal:** $\\Phi = \\iint_S \\vec{v} \\cdot d\\vec{S}$ — volumen/tiempo.",
              "**Calor:** $\\vec{q} = -k\\nabla T$, signo $-$ porque fluye opuesto al gradiente.",
              "**Ley de Gauss:** $\\oiint \\vec{E} \\cdot d\\vec{S} = Q_{enc}/\\epsilon_0$.",
              "**Independencia de la superficie** para flujo eléctrico de cargas encerradas (consecuencia del teorema de divergencia).",
              "**Próxima lección:** teorema de Stokes — generalización 3D del teorema de Green.",
          ]),
    ]
    return {
        "id": "lec-vec-3-5-aplicaciones",
        "title": "Aplicaciones",
        "description": "Caudal, flujo de calor, flujo eléctrico, ley de Gauss y centros de masa de láminas curvas.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# 3.6 Teorema de Stokes
# =====================================================================
def lesson_3_6():
    blocks = [
        b("texto", body_md=(
            "El **teorema de Stokes** es la generalización 3D del teorema de Green. Conecta una **integral "
            "de línea sobre la frontera** de una superficie con una **integral de superficie del rotacional** "
            "sobre la propia superficie. Es uno de los **teoremas centrales** del cálculo vectorial — junto "
            "con el teorema de la divergencia, son la culminación del curso.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Enunciar y aplicar el **teorema de Stokes**.\n"
            "- Comprender la **orientación** consistente entre $S$ y $\\partial S$.\n"
            "- Reconocer la **invariancia respecto a la superficie** (cualquier $S$ con la misma frontera $C$ funciona).\n"
            "- Aplicar a problemas concretos."
        )),

        b("teorema",
          nombre="Teorema de Stokes",
          enunciado_md=(
              "Sea $S$ una superficie orientada, suave por tramos, con frontera $C = \\partial S$ orientada **positivamente** según la regla de la mano derecha. Sea $\\vec{F}$ un campo vectorial $C^1$ en una región que contiene $S$. Entonces:\n\n"
              "$$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{S}$$\n\n"
              "**En palabras:** la **circulación** de $\\vec{F}$ a lo largo del borde es el **flujo del rotacional** a través de la superficie.\n\n"
              "**Caso 2D:** si $S$ es una región plana en $\\mathbb{R}^2$ con normal $\\vec{k}$, $\\nabla \\times \\vec{F} \\cdot \\vec{k} = Q_x - P_y$ — recupera Green.\n\n"
              "**Stokes es Green generalizado a superficies en $\\mathbb{R}^3$.**"
          ),
          demostracion_md=(
              "**Idea:** dividir $S$ en pequeños paralelogramos. Por Green local, la circulación de $\\vec{F}$ alrededor de cada paralelogramo aproxima el flujo del rotacional sobre él. Las contribuciones de los lados internos se cancelan en pares (recorridos en sentidos opuestos por dos paralelogramos vecinos), quedando solo la circulación a lo largo de la **frontera externa $\\partial S$**. Tomando el límite $\\to$ teorema de Stokes."
          )),

        b("intuicion",
          titulo="Independencia de la superficie",
          body_md=(
              "**Consecuencia notable:** si $S_1$ y $S_2$ son **dos superficies con la misma frontera $C$** (orientada igual), entonces:\n\n"
              "$$\\iint_{S_1} (\\nabla \\times \\vec{F}) \\cdot d\\vec{S} = \\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_{S_2} (\\nabla \\times \\vec{F}) \\cdot d\\vec{S}$$\n\n"
              "**Es decir, el flujo del rotacional depende solo de la frontera, no de la superficie elegida.**\n\n"
              "**Aplicación práctica:** si tienes que calcular el flujo del rotacional sobre una superficie complicada, puedes **reemplazarla por una superficie más simple con la misma frontera** (un disco plano, por ejemplo).\n\n"
              "**Comparación con Green:** Green es un caso 2D, pero Stokes permite elegir entre infinitas superficies para una misma curva frontera."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar Stokes con un cálculo directo",
          problema_md=(
              "Sea $\\vec{F} = \\langle -y, x, z \\rangle$ y $S$ el hemisferio superior de la esfera unitaria. Calcular ambos lados del teorema de Stokes."
          ),
          pasos=[
              {"accion_md": "**Lado izquierdo (integral de línea):** $\\partial S$ es el círculo $x^2+y^2=1, z=0$. Por la regla de la mano derecha (normal hacia arriba), recorrer **antihorario**.\n\n"
                            "Parametrización: $\\vec{r}(t) = \\langle \\cos t, \\sin t, 0 \\rangle$, $t \\in [0, 2\\pi]$.\n\n"
                            "$\\vec{F}(\\vec{r}) = \\langle -\\sin t, \\cos t, 0 \\rangle$. $\\vec{r}'(t) = \\langle -\\sin t, \\cos t, 0 \\rangle$. Producto punto: $\\sin^2 t + \\cos^2 t = 1$.\n\n"
                            "$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\int_0^{2\\pi} 1 \\, dt = 2\\pi$.",
               "justificacion_md": "Cálculo directo del lado izquierdo.",
               "es_resultado": False},
              {"accion_md": "**Lado derecho (integral de superficie del rotacional):** $\\nabla \\times \\vec{F} = \\langle 0, 0, 2 \\rangle$ (calcular).\n\n"
                            "**En el hemisferio:** $\\vec{n} = \\vec{r}$ (normal exterior hacia arriba en el hemisferio = vector posición).",
               "justificacion_md": "$\\nabla \\times \\vec{F}$ constante.",
               "es_resultado": False},
              {"accion_md": "$(\\nabla \\times \\vec{F}) \\cdot \\vec{n} = 2 z$ (componente $z$ de $\\vec{r}$, multiplicada por 2).\n\n"
                            "$\\iint_S 2z \\, dS = 2 \\iint_S z \\, dS$. Por el ejemplo de la lección 3.2 (centroide del hemisferio): $\\iint z \\, dS = \\pi$.\n\n"
                            "**Resultado:** $2\\pi$. ✓\n\n"
                            "**Stokes confirmado:** $2\\pi = 2\\pi$.",
               "justificacion_md": "**Más fácil con la observación de Stokes:** podríamos haber elegido como $S$ el disco plano $D = \\{x^2+y^2 \\leq 1, z = 0\\}$ con $\\vec{n} = \\vec{k}$. Entonces $(\\nabla \\times \\vec{F}) \\cdot \\vec{k} = 2$, y $\\iint_D 2 \\, dA = 2\\pi$. ✓ **Mismo resultado, cálculo más simple.**",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Caracterización de campos conservativos en 3D",
          enunciado_md=(
              "Una consecuencia importante de Stokes: en una **región simplemente conexa** $D \\subset \\mathbb{R}^3$:\n\n"
              "$$\\vec{F} \\text{ es conservativo} \\iff \\nabla \\times \\vec{F} = \\vec{0} \\text{ en } D$$\n\n"
              "**Por qué:** si $\\nabla \\times \\vec{F} = \\vec{0}$, entonces para toda curva cerrada $C$ acotando una superficie $S$ en $D$:\n\n"
              "$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_S \\vec{0} \\cdot d\\vec{S} = 0$\n\n"
              "Por las equivalencias de la lección 2.4, $\\vec{F}$ es conservativo.\n\n"
              "**El test 'rotacional cero'** que enunciamos en 2.4 ahora tiene **demostración** vía Stokes."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicar Stokes para simplificar",
          problema_md=(
              "Calcular $\\oint_C \\vec{F} \\cdot d\\vec{r}$ donde $\\vec{F} = \\langle z^2, y^2, x \\rangle$ y $C$ es la curva intersección del cilindro $x^2 + y^2 = 1$ con el plano $z = y$, recorrida antihoraria vista desde arriba."
          ),
          pasos=[
              {"accion_md": "**$C$ es complicada de parametrizar.** Aplicar Stokes con la **superficie $S$** = trozo del plano $z = y$ que tiene a $C$ como frontera.\n\n"
                            "$S$ proyecta al disco $D: x^2 + y^2 \\leq 1$ en el plano $xy$. Parametrizar como gráfica $z = y$ sobre $D$.",
               "justificacion_md": "Truco clave: elegir la superficie más simple con la misma frontera.",
               "es_resultado": False},
              {"accion_md": "**Rotacional:** $\\nabla \\times \\vec{F}$. Componente $\\vec{i}$: $\\partial_y(x) - \\partial_z(y^2) = 0$. Componente $\\vec{j}$: $\\partial_z(z^2) - \\partial_x(x) = 2z - 1$. Componente $\\vec{k}$: $\\partial_x(y^2) - \\partial_y(z^2) = 0$.\n\n"
                            "$\\nabla \\times \\vec{F} = \\langle 0, 2z - 1, 0 \\rangle$.",
               "justificacion_md": "Calcular el rotacional con cuidado.",
               "es_resultado": False},
              {"accion_md": "**Parametrización de $S$:** $\\vec{r}(x, y) = \\langle x, y, y \\rangle$. $\\vec{r}_x \\times \\vec{r}_y = \\langle 0, -1, 1 \\rangle$.\n\n"
                            "**Verificar orientación:** componente $z = 1 > 0$ → apunta hacia arriba. ✓ (consistente con frontera antihoraria vista desde arriba).",
               "justificacion_md": "El producto cruz da automáticamente la orientación correcta para Stokes en este caso.",
               "es_resultado": False},
              {"accion_md": "**$\\nabla \\times \\vec{F}$ en $S$:** $\\langle 0, 2y - 1, 0 \\rangle$ (porque $z = y$).\n\n"
                            "**Producto punto:** $\\langle 0, 2y - 1, 0 \\rangle \\cdot \\langle 0, -1, 1 \\rangle = -(2y - 1) = 1 - 2y$.\n\n"
                            "$\\iint_D (1 - 2y) \\, dA = \\iint_D 1 \\, dA - 2\\iint_D y \\, dA = \\pi - 0 = \\pi$.\n\n"
                            "(Por simetría, $\\iint_D y \\, dA = 0$.)",
               "justificacion_md": "**Resultado:** $\\oint_C \\vec{F} \\cdot d\\vec{r} = \\pi$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Stokes relaciona:",
                  "opciones_md": [
                      "Integral de línea con integral doble en el plano",
                      "Integral de línea con integral de superficie del rotacional",
                      "Integral de superficie con integral triple",
                      "Dos integrales de línea",
                  ],
                  "correcta": "B",
                  "pista_md": "Stokes: línea sobre frontera vs superficie del rotacional.",
                  "explicacion_md": (
                      "$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{S}$. **Es Green generalizado a superficies 3D.**"
                  ),
              },
              {
                  "enunciado_md": "Si $\\nabla \\times \\vec{F} = \\vec{0}$ y $C$ es cerrada, $\\oint_C \\vec{F} \\cdot d\\vec{r} = ?$",
                  "opciones_md": [
                      "$2\\pi$",
                      "$0$",
                      "Depende de $C$",
                      "$\\infty$",
                  ],
                  "correcta": "B",
                  "pista_md": "Stokes con rotacional cero.",
                  "explicacion_md": (
                      "$\\oint = \\iint_S \\vec{0} \\cdot d\\vec{S} = 0$. **Caracterización de conservativos en 3D.**"
                  ),
              },
          ]),

        ej(
            titulo="Stokes con superficie alternativa",
            enunciado=(
                "Calcula $\\oint_C \\vec{F} \\cdot d\\vec{r}$ donde $\\vec{F} = \\langle y^2, x, z \\rangle$ y $C$ es el círculo unitario en el plano $xy$, antihorario."
            ),
            pistas=[
                "Aplica Stokes con $S$ = disco $D: x^2+y^2 \\leq 1, z = 0$.",
                "$\\nabla \\times \\vec{F} = ?$",
                "Solo necesitas la componente $z$ del rotacional, porque $\\vec{n} = \\vec{k}$.",
            ],
            solucion=(
                "$\\nabla \\times \\vec{F} = \\langle 0 - 0, 0 - 0, 1 - 2y \\rangle$.\n\n"
                "$(\\nabla \\times \\vec{F}) \\cdot \\vec{k} = 1 - 2y$.\n\n"
                "$\\iint_D (1 - 2y) \\, dA = \\pi - 0 = \\pi$. (Por simetría.)"
            ),
        ),

        ej(
            titulo="Stokes en hemisferio",
            enunciado=(
                "Calcula $\\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{S}$ donde $\\vec{F} = \\langle y, -x, z^2 \\rangle$ "
                "y $S$ es la parte del hemisferio $x^2+y^2+z^2 = 4, z \\geq 0$, con normal hacia arriba."
            ),
            pistas=[
                "Usa Stokes con la frontera $C: x^2+y^2 = 4, z = 0$, antihoraria.",
                "Parametrización del círculo: $\\vec{r}(t) = (2\\cos t, 2\\sin t, 0)$.",
                "$\\vec{F} \\cdot \\vec{r}'$.",
            ],
            solucion=(
                "$\\vec{F}(\\vec{r}(t)) = \\langle 2\\sin t, -2\\cos t, 0 \\rangle$. $\\vec{r}'(t) = \\langle -2\\sin t, 2\\cos t, 0 \\rangle$.\n\n"
                "$\\vec{F} \\cdot \\vec{r}' = -4\\sin^2 t - 4\\cos^2 t = -4$.\n\n"
                "$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\int_0^{2\\pi} (-4) \\, dt = -8\\pi$.\n\n"
                "Por Stokes: $\\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{S} = -8\\pi$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Stokes con superficie no orientable.** Möbius rompe el teorema.",
              "**Olvidar verificar orientación consistente** entre $S$ y $\\partial S$. La regla de la mano derecha es esencial.",
              "**Calcular sobre superficie complicada cuando hay una más simple con la misma frontera.** Aprovechar la independencia.",
              "**Confundir Stokes con divergencia.** Stokes: línea ↔ superficie. Divergencia: superficie ↔ volumen.",
              "**Aplicar a curvas no cerradas.** Stokes requiere $C$ cerrada (frontera de $S$).",
          ]),

        b("resumen",
          puntos_md=[
              "**Teorema de Stokes:** $\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{S}$.",
              "**Generalización 3D del teorema de Green.**",
              "**Orientación:** $S$ orientada → $\\partial S$ por regla de la mano derecha.",
              "**Independencia de la superficie:** dos superficies con la misma frontera dan el mismo flujo del rotacional.",
              "**Caracterización de conservativos en 3D:** $\\nabla \\times \\vec{F} = \\vec{0}$ en regiones simplemente conexas ⟺ conservativo.",
              "**Próxima lección:** teorema de la divergencia — el otro gran teorema 3D.",
          ]),
    ]
    return {
        "id": "lec-vec-3-6-stokes",
        "title": "Teorema de Stokes",
        "description": "$\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{S}$. Generalización 3D de Green.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 6,
    }


# =====================================================================
# 3.7 Teorema de la divergencia
# =====================================================================
def lesson_3_7():
    blocks = [
        b("texto", body_md=(
            "El **teorema de la divergencia** (o teorema de Gauss) es la generalización 3D de la **forma del "
            "flujo del teorema de Green**. Conecta una **integral de superficie cerrada** (flujo) con una "
            "**integral triple** (divergencia) sobre el volumen interior. Junto con Stokes, completa la "
            "trinidad de los grandes teoremas del cálculo vectorial — y cierra el curso.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Enunciar y aplicar el **teorema de la divergencia**.\n"
            "- Reconocer cuándo conviene usarlo vs el cálculo directo.\n"
            "- Comprender la **conexión con la conservación de masa y carga**.\n"
            "- Visualizar la **estructura unificada** de los grandes teoremas."
        )),

        b("teorema",
          nombre="Teorema de la divergencia (Gauss)",
          enunciado_md=(
              "Sea $E \\subset \\mathbb{R}^3$ una región sólida acotada con frontera $S = \\partial E$ que es una superficie cerrada, suave por tramos y orientada con **normal exterior**. Sea $\\vec{F}$ un campo vectorial $C^1$ en $E$. Entonces:\n\n"
              "$$\\oiint_S \\vec{F} \\cdot d\\vec{S} = \\iiint_E \\nabla \\cdot \\vec{F} \\, dV$$\n\n"
              "**En palabras:** el **flujo total** que sale de $E$ por la frontera = **suma total de las divergencias** en el interior.\n\n"
              "**Forma divergencia:** $\\nabla \\cdot \\vec{F} = P_x + Q_y + R_z$ con $\\vec{F} = \\langle P, Q, R \\rangle$.\n\n"
              "**Símbolo $\\oiint$:** integral sobre superficie cerrada — equivale a $\\iint$ pero enfatiza que es cerrada."
          ),
          demostracion_md=(
              "**Idea:** análoga a Green. Dividir $E$ en pequeños cubos. El flujo neto a través del cubo aproxima $\\nabla \\cdot \\vec{F}$ por el volumen del cubo. Las contribuciones de las caras internas se cancelan en pares (vecinas), quedando solo el flujo sobre la frontera $\\partial E$."
          )),

        b("intuicion",
          titulo="Conservación local: 'fuentes adentro = flujo afuera'",
          body_md=(
              "**Físicamente:** la divergencia mide qué tan 'fuente' o 'sumidero' es cada punto del campo. **El teorema dice:**\n\n"
              "$$\\text{flujo que sale} = \\text{total de fuentes adentro}$$\n\n"
              "**Ejemplo: agua en un tanque.** Si hay un grifo adentro (fuente, $\\nabla \\cdot \\vec{v} > 0$), el agua tiene que salir por la frontera. **El total que sale = el total que entra por el grifo.**\n\n"
              "**Si no hay fuentes** ($\\nabla \\cdot \\vec{F} = 0$ en todo $E$): el flujo neto a través de $\\partial E$ es **cero** — entra tanto como sale (campo incompresible).\n\n"
              "**Aplicación a Maxwell:** $\\nabla \\cdot \\vec{E} = \\rho/\\epsilon_0$ — la divergencia del campo eléctrico es la densidad de carga (las cargas son las fuentes)."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar el teorema con un cálculo directo",
          problema_md=(
              "Sea $\\vec{F} = \\langle x, y, z \\rangle$ y $E$ la bola unitaria. Verificar el teorema de la divergencia."
          ),
          pasos=[
              {"accion_md": "**Lado derecho:** $\\nabla \\cdot \\vec{F} = 1 + 1 + 1 = 3$.\n\n"
                            "$\\iiint_E 3 \\, dV = 3 \\cdot V(E) = 3 \\cdot \\dfrac{4\\pi}{3} = 4\\pi$.",
               "justificacion_md": "Volumen de bola unitaria.",
               "es_resultado": False},
              {"accion_md": "**Lado izquierdo:** ya calculado en la lección 3.4 — flujo de $\\vec{F} = \\vec{r}$ a través de la esfera unitaria $= 4\\pi$.",
               "justificacion_md": "Reuso del cálculo previo.",
               "es_resultado": False},
              {"accion_md": "**$4\\pi = 4\\pi$** — teorema verificado. ✓",
               "justificacion_md": "**Lección:** muchas veces el lado derecho (integral triple) es **mucho más simple** que el lado izquierdo (integral sobre superficie cerrada compleja).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Simplificar con divergencia",
          problema_md=(
              "Calcular el flujo de $\\vec{F} = \\langle x^3, y^3, z^3 \\rangle$ a través de la esfera unitaria con normal exterior."
          ),
          pasos=[
              {"accion_md": "**Por divergencia:** $\\nabla \\cdot \\vec{F} = 3x^2 + 3y^2 + 3z^2 = 3(x^2+y^2+z^2)$.\n\n"
                            "$\\iiint_E 3(x^2+y^2+z^2) \\, dV$.",
               "justificacion_md": "Cálculo directo del flujo sería sangriento.",
               "es_resultado": False},
              {"accion_md": "**En esféricas:** $x^2+y^2+z^2 = \\rho^2$.\n\n"
                            "$3 \\int_0^{2\\pi}\\int_0^\\pi \\int_0^1 \\rho^2 \\cdot \\rho^2 \\sin\\varphi \\, d\\rho \\, d\\varphi \\, d\\theta$\n\n"
                            "$= 3 \\cdot \\dfrac{1}{5} \\cdot 2 \\cdot 2\\pi = \\dfrac{12\\pi}{5}$.",
               "justificacion_md": "**Sin divergencia:** habría que parametrizar la esfera, calcular el producto cruz, hacer producto punto con $\\vec{F}$ — varias páginas. **Con divergencia: una integral triple en esféricas, directo.**",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Los grandes teoremas — visión unificada",
            body=(
                "Los teoremas centrales del cálculo conectan **integrales en distintas dimensiones**:\n\n"
                "| Teorema | Dimensión | Forma |\n|---|---|---|\n"
                "| **TFC** (1D) | $0 \\to 1$ | $\\int_a^b f' \\, dx = f(b) - f(a)$ |\n"
                "| **TFC para línea** | $1 \\to 1$ | $\\int_C \\nabla f \\cdot d\\vec{r} = f(B) - f(A)$ |\n"
                "| **Green** (2D) | $1 \\to 2$ | $\\oint_C P \\, dx + Q \\, dy = \\iint_D (Q_x - P_y) \\, dA$ |\n"
                "| **Stokes** (3D) | $1 \\to 2$ | $\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{S}$ |\n"
                "| **Divergencia** (3D) | $2 \\to 3$ | $\\oiint_S \\vec{F} \\cdot d\\vec{S} = \\iiint_E (\\nabla \\cdot \\vec{F}) \\, dV$ |\n\n"
                "**Patrón común:** integral de un 'gradiente generalizado' sobre una región = integral del campo original sobre la **frontera** de la región. **Es el teorema de Stokes generalizado** (formalmente: $\\int_M d\\omega = \\int_{\\partial M} \\omega$ — geometría diferencial)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Ley de Gauss aplicada",
          problema_md=(
              "Una distribución de carga uniforme tiene densidad $\\rho_0$ en una bola de radio $R$. Aplicar la ley de Gauss para calcular el campo eléctrico fuera de la bola."
          ),
          pasos=[
              {"accion_md": "**Aplicar la ley de Gauss** $\\oiint_S \\vec{E} \\cdot d\\vec{S} = Q_{enc}/\\epsilon_0$ con $S$ = esfera concéntrica de radio $r > R$.\n\n"
                            "**Carga encerrada:** $Q_{enc} = \\rho_0 \\cdot \\dfrac{4\\pi R^3}{3}$.",
               "justificacion_md": "Carga total de la bola interior.",
               "es_resultado": False},
              {"accion_md": "**Por simetría:** $\\vec{E}$ es radial y de magnitud constante en $S$. Llamar $E$ esa magnitud.\n\n"
                            "$\\oiint_S \\vec{E} \\cdot \\vec{n} \\, dS = E \\cdot 4\\pi r^2$.",
               "justificacion_md": "$\\vec{E} \\parallel \\vec{n}$ y $|E|$ constante.",
               "es_resultado": False},
              {"accion_md": "**Igualando:** $E \\cdot 4\\pi r^2 = \\rho_0 \\cdot \\dfrac{4\\pi R^3}{3 \\epsilon_0} \\implies E = \\dfrac{\\rho_0 R^3}{3 \\epsilon_0 r^2}$.\n\n"
                            "**Equivalente a una carga puntual** $Q = \\rho_0 \\cdot \\dfrac{4\\pi R^3}{3}$ en el origen. **Resultado físico clásico:** una distribución esférica de carga se comporta exteriormente como si toda la carga estuviera concentrada en el centro.",
               "justificacion_md": "**Aplicación dramática del teorema de la divergencia/Gauss** — sin él, calcular $\\vec{E}$ requeriría integrar sobre cada elemento de la bola (mucho más laborioso).",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El teorema de la divergencia conecta:",
                  "opciones_md": [
                      "Integral de línea con integral doble",
                      "Integral de superficie cerrada con integral triple",
                      "Dos integrales triples",
                      "Integral simple con doble",
                  ],
                  "correcta": "B",
                  "pista_md": "Flujo (superficie) ↔ divergencia (volumen).",
                  "explicacion_md": (
                      "$\\oiint_S \\vec{F} \\cdot d\\vec{S} = \\iiint_E \\nabla \\cdot \\vec{F} \\, dV$. **Generalización 3D de la forma flujo de Green.**"
                  ),
              },
              {
                  "enunciado_md": "Si $\\nabla \\cdot \\vec{F} = 0$ en todo el sólido $E$ encerrado por $S$, $\\oiint_S \\vec{F} \\cdot d\\vec{S} = ?$",
                  "opciones_md": [
                      "$0$",
                      "$\\text{Área}(S)$",
                      "$\\text{Volumen}(E)$",
                      "Depende de $\\vec{F}$",
                  ],
                  "correcta": "A",
                  "pista_md": "Divergencia cero ⇒ campo incompresible ⇒ flujo neto cero.",
                  "explicacion_md": (
                      "$\\iiint_E 0 \\, dV = 0$. **Sin fuentes ni sumideros adentro: lo que entra es igual a lo que sale.**"
                  ),
              },
          ]),

        ej(
            titulo="Divergencia simplifica el cálculo",
            enunciado=(
                "Calcula el flujo de $\\vec{F} = \\langle x + y^2, y + z^2, z + x^2 \\rangle$ a través de la frontera del cubo $[0, 1]^3$, normal exterior."
            ),
            pistas=[
                "Sin divergencia: 6 caras, 6 integrales dobles.",
                "Con divergencia: $\\nabla \\cdot \\vec{F} = 1 + 1 + 1 = 3$.",
                "$\\iiint 3 \\, dV = 3 \\cdot 1 = 3$.",
            ],
            solucion=(
                "$\\nabla \\cdot \\vec{F} = 3$. Volumen del cubo: $1$.\n\n"
                "$\\Phi = \\iiint_E 3 \\, dV = 3$.\n\n"
                "**Sin divergencia, este problema requeriría calcular las 6 integrales por separado y sumarlas — laborioso pero da el mismo resultado.**"
            ),
        ),

        ej(
            titulo="Volumen vía divergencia",
            enunciado=(
                "Demuestra que el volumen de un sólido $E$ es $V(E) = \\dfrac{1}{3} \\oiint_{\\partial E} \\vec{F} \\cdot d\\vec{S}$ "
                "con $\\vec{F} = \\langle x, y, z \\rangle$."
            ),
            pistas=[
                "$\\nabla \\cdot \\vec{F} = 3$.",
                "Aplicar divergencia.",
            ],
            solucion=(
                "Por divergencia: $\\oiint \\vec{F} \\cdot d\\vec{S} = \\iiint_E 3 \\, dV = 3 V(E)$.\n\n"
                "Despejando: $V(E) = \\dfrac{1}{3}\\oiint \\vec{F} \\cdot d\\vec{S}$.\n\n"
                "**Volumen como integral de superficie** — análogo 3D al área como integral de línea de Green ($A = \\frac{1}{2}\\oint \\ldots$)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar divergencia con superficie no cerrada.** El teorema requiere $\\partial E$ cerrada (sin agujeros).",
              "**Usar normal interior** sin avisar. La convención es exterior.",
              "**Confundir Stokes con divergencia.** Stokes: rotacional y curva. Divergencia: divergencia y volumen.",
              "**Aplicar el teorema cuando $\\vec{F}$ tiene singularidades dentro de $E$.** Hay que excluir un entorno y manejarlo aparte (p. ej., como en cargas puntuales).",
              "**Olvidar el orden:** $\\oiint = \\iiint$ (no al revés). Flujo a la izquierda, divergencia a la derecha.",
          ]),

        b("resumen",
          puntos_md=[
              "**Teorema de la divergencia:** $\\oiint_S \\vec{F} \\cdot d\\vec{S} = \\iiint_E \\nabla \\cdot \\vec{F} \\, dV$.",
              "**$S = \\partial E$ cerrada, normal exterior, $\\vec{F}$ suave.**",
              "**Interpretación:** flujo total = suma de fuentes/sumideros internos.",
              "**Aplicación clásica:** ley de Gauss del electromagnetismo, conservación de masa en fluidos.",
              "**Estructura unificada** de los grandes teoremas: TFC, Green, Stokes, divergencia — todos siguen el patrón 'integral sobre frontera = integral del derivado generalizado sobre el interior'.",
              "**🎉 Cierre del curso de Cálculo Vectorial 🎉:** desde curvas paramétricas hasta los teoremas que unifican el cálculo en cualquier dimensión.",
          ]),
    ]
    return {
        "id": "lec-vec-3-7-divergencia",
        "title": "Teorema de la divergencia",
        "description": "$\\oiint_S \\vec{F} \\cdot d\\vec{S} = \\iiint_E \\nabla \\cdot \\vec{F} \\, dV$. Generalización 3D del flujo de Green. Ley de Gauss.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 7,
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

    chapter_id = "ch-integrales-superficie"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Integrales de Superficie",
        "description": "Superficies paramétricas, integrales de superficie, orientación, flujo, teorema de Stokes y teorema de la divergencia.",
        "order": 3,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_3_1, lesson_3_2, lesson_3_3, lesson_3_4, lesson_3_5, lesson_3_6, lesson_3_7]
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
    print(f"✅ Capítulo 3 — Integrales de Superficie listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    print("🎉 Curso Cálculo Vectorial COMPLETO 🎉")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
