"""
Seed del curso Cálculo Vectorial — Capítulo 1: Curvas.
7 lecciones:
  1.1 Ecuaciones paramétricas
  1.2 Coordenadas polares
  1.3 Funciones vectoriales
  1.4 Longitud de curva
  1.5 Vectores de curvas (T, N, B)
  1.6 Curvatura y torsión
  1.7 Fórmulas de Frenet-Serret

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
# 1.1 Ecuaciones paramétricas
# =====================================================================
def lesson_1_1():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora describimos curvas en el plano como **gráficas de funciones** $y = f(x)$. "
            "Pero esa descripción tiene límites: no captura curvas que se cruzan a sí mismas, ni "
            "círculos completos. Las **ecuaciones paramétricas** lo solucionan: introducen un "
            "**parámetro** $t$ (tiempo, usualmente) y describen cada coordenada como función suya.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y graficar curvas paramétricas $(x(t), y(t))$.\n"
            "- Convertir entre forma paramétrica y cartesiana **eliminando el parámetro**.\n"
            "- Calcular **rectas tangentes** a curvas paramétricas.\n"
            "- Reconocer las curvas clásicas: círculos, elipses, cicloides, espirales."
        )),

        b("definicion",
          titulo="Curva paramétrica",
          body_md=(
              "Una **curva paramétrica** en el plano es un par de funciones:\n\n"
              "$$x = x(t), \\quad y = y(t), \\quad t \\in I$$\n\n"
              "donde $I$ es un intervalo. La curva es el conjunto de puntos $\\{(x(t), y(t)) : t \\in I\\}$.\n\n"
              "**El parámetro $t$** suele interpretarse como **tiempo** — la curva es la trayectoria de una partícula que en el instante $t$ está en $(x(t), y(t))$.\n\n"
              "**Ventaja sobre $y = f(x)$:** podemos describir curvas que no son gráficas de funciones — círculos completos, curvas que se autointersecan, hélices (en 3D), etc."
          )),

        b("ejemplo_resuelto",
          titulo="Círculo paramétrico",
          problema_md="Mostrar que $x = \\cos t, y = \\sin t$ con $t \\in [0, 2\\pi]$ describe el círculo unitario.",
          pasos=[
              {"accion_md": "**Eliminar el parámetro:** $x^2 + y^2 = \\cos^2 t + \\sin^2 t = 1$.",
               "justificacion_md": "Identidad pitagórica.",
               "es_resultado": False},
              {"accion_md": "Es la ecuación cartesiana del círculo unitario. **Cuando $t$ recorre $[0, 2\\pi]$, el punto $(x, y)$ recorre el círculo completo** una vez, en sentido antihorario.",
               "justificacion_md": "**Lección clave:** $y = f(x)$ no podría describir el círculo completo (por punto $x$ hay dos $y$). Paramétricas sí.",
               "es_resultado": True},
          ]),

        fig(
            "Galería de curvas paramétricas en el plano. Cuatro ejemplos en una grilla 2x2: PANEL "
            "ARRIBA-IZQ: círculo unitario x = cos(t), y = sin(t). PANEL ARRIBA-DER: elipse x = "
            "2cos(t), y = sin(t). PANEL ABAJO-IZQ: cicloide (curva trazada por un punto en una "
            "rueda que rueda) x = t - sin(t), y = 1 - cos(t), mostrando 2-3 ciclos. PANEL "
            "ABAJO-DER: espiral logarítmica x = e^(t/5)cos(t), y = e^(t/5)sin(t). Cada curva en "
            "color teal con fondo cuadriculado claro y etiqueta de su nombre. " + STYLE
        ),

        formulas(
            titulo="Curvas paramétricas clásicas",
            body=(
                "| Curva | Parametrización |\n|---|---|\n"
                "| **Círculo** radio $R$ | $x = R\\cos t, y = R\\sin t$, $t \\in [0, 2\\pi]$ |\n"
                "| **Elipse** semiejes $a, b$ | $x = a\\cos t, y = b\\sin t$ |\n"
                "| **Recta** por $P_0$ con dirección $\\vec{v}$ | $x = x_0 + v_1 t, y = y_0 + v_2 t$ |\n"
                "| **Parábola** $y = x^2$ | $x = t, y = t^2$ |\n"
                "| **Cicloide** | $x = R(t - \\sin t), y = R(1 - \\cos t)$ |\n"
                "| **Hélice** (en 3D) | $x = R\\cos t, y = R\\sin t, z = ct$ |\n"
                "| **Espiral arquimediana** | $x = t\\cos t, y = t\\sin t$ |\n\n"
                "**Cualquier $y = f(x)$** se parametriza trivialmente como $x = t, y = f(t)$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Eliminar el parámetro",
          problema_md="Eliminar $t$ de $x = t^2, y = t + 1$ y describir la curva.",
          pasos=[
              {"accion_md": "**Despejar $t$ de la segunda ecuación:** $t = y - 1$.\n\n"
                            "**Sustituir en la primera:** $x = (y - 1)^2$.",
               "justificacion_md": "Si una de las ecuaciones es lineal en $t$, despeje y sustitución.",
               "es_resultado": False},
              {"accion_md": "**Curva:** $x = (y - 1)^2$ — parábola horizontal con vértice $(0, 1)$, abriendo hacia la derecha.",
               "justificacion_md": "**Atención al rango:** el parámetro $t$ original puede haber tenido restricciones que limitan la curva. Si $t \\in \\mathbb{R}$, $y$ recorre todo $\\mathbb{R}$ y la parábola es completa.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Tangente a una curva paramétrica",
          body_md=(
              "Si $x(t), y(t)$ son derivables y $x'(t) \\neq 0$ en un punto, la **pendiente de la recta tangente** allí es:\n\n"
              "$$\\dfrac{dy}{dx} = \\dfrac{dy/dt}{dx/dt} = \\dfrac{y'(t)}{x'(t)}$$\n\n"
              "(Sale de la regla de la cadena: $dy/dt = (dy/dx)(dx/dt)$.)\n\n"
              "**Tangentes verticales:** ocurren donde $x'(t) = 0$ y $y'(t) \\neq 0$.\n\n"
              "**Tangentes horizontales:** ocurren donde $y'(t) = 0$ y $x'(t) \\neq 0$.\n\n"
              "**Si ambos son cero:** punto singular — puede ser una cúspide (como en la cicloide) o una autointersección."
          )),

        b("ejemplo_resuelto",
          titulo="Tangente al círculo en el punto $(\\sqrt{2}/2, \\sqrt{2}/2)$",
          problema_md="Para $x = \\cos t, y = \\sin t$, hallar la tangente en $t = \\pi/4$.",
          pasos=[
              {"accion_md": "**Punto:** $x(\\pi/4) = \\sqrt{2}/2$, $y(\\pi/4) = \\sqrt{2}/2$. ✓\n\n"
                            "**Derivadas:** $x'(t) = -\\sin t$, $y'(t) = \\cos t$.\n\n"
                            "**En $t = \\pi/4$:** $x' = -\\sqrt{2}/2$, $y' = \\sqrt{2}/2$.",
               "justificacion_md": "Cálculo directo.",
               "es_resultado": False},
              {"accion_md": "**Pendiente:** $\\dfrac{dy}{dx} = \\dfrac{\\sqrt{2}/2}{-\\sqrt{2}/2} = -1$.\n\n"
                            "**Recta tangente:** $y - \\sqrt{2}/2 = -1 (x - \\sqrt{2}/2)$, o $x + y = \\sqrt{2}$.",
               "justificacion_md": "**Verificación geométrica:** la tangente al círculo en cualquier punto es perpendicular al radio. Aquí el radio tiene pendiente $1$, así la tangente tiene pendiente $-1$. ✓",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Una curva, infinitas parametrizaciones",
          body_md=(
              "La misma curva geométrica admite **infinitas parametrizaciones**. Por ejemplo, el círculo unitario:\n\n"
              "- $x = \\cos t, y = \\sin t$: una vuelta antihoraria con $t \\in [0, 2\\pi]$.\n"
              "- $x = \\cos(2t), y = \\sin(2t)$: la **misma** curva, recorrida **dos veces** con $t \\in [0, 2\\pi]$.\n"
              "- $x = \\sin t, y = \\cos t$: una vuelta **horaria**.\n\n"
              "La **velocidad** ($\\sqrt{(x')^2 + (y')^2}$) y la **dirección** dependen de la parametrización; "
              "la **traza geométrica** no.\n\n"
              "**Para algunos cálculos** (longitud de arco, integrales) la respuesta depende solo de la curva geométrica. **Para otros** (velocidad, parámetros físicos) sí depende de la parametrización."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para $x = e^t, y = e^{2t}$, eliminar el parámetro da:",
                  "opciones_md": ["$y = x^2$", "$y = e^x$", "$y = 2x$", "$x = y^2$"],
                  "correcta": "A",
                  "pista_md": "$y = (e^t)^2 = x^2$.",
                  "explicacion_md": (
                      "$y = e^{2t} = (e^t)^2 = x^2$. **Atención al rango:** $x = e^t > 0$, así la curva es la parte de $y = x^2$ con $x > 0$ — **no toda la parábola**."
                  ),
              },
              {
                  "enunciado_md": "Para curva paramétrica, $dy/dx = ?$",
                  "opciones_md": [
                      "$y'(t)$",
                      "$y'(t)/x'(t)$",
                      "$x'(t)/y'(t)$",
                      "$y'(t) \\cdot x'(t)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Regla de la cadena.",
                  "explicacion_md": (
                      "$dy/dt = (dy/dx)(dx/dt) \\implies dy/dx = (dy/dt)/(dx/dt) = y'(t)/x'(t)$."
                  ),
              },
          ]),

        ej(
            titulo="Eliminar parámetro y graficar",
            enunciado=(
                "Sea $x = 2\\cos t, y = 3\\sin t$, $t \\in [0, 2\\pi]$. Identifica la curva y halla la "
                "ecuación cartesiana."
            ),
            pistas=[
                "$\\cos t = x/2$, $\\sin t = y/3$.",
                "Aplica la identidad pitagórica.",
            ],
            solucion=(
                "$\\cos^2 t + \\sin^2 t = 1 \\implies \\dfrac{x^2}{4} + \\dfrac{y^2}{9} = 1$.\n\n"
                "**Elipse** con semiejes $a = 2$ (en $x$) y $b = 3$ (en $y$), centrada en el origen."
            ),
        ),

        ej(
            titulo="Tangente a una cicloide",
            enunciado=(
                "Para la cicloide $x = t - \\sin t, y = 1 - \\cos t$, halla $dy/dx$ en $t = \\pi/2$."
            ),
            pistas=[
                "$x'(t) = 1 - \\cos t$, $y'(t) = \\sin t$.",
                "En $t = \\pi/2$: $x'(\\pi/2) = 1$, $y'(\\pi/2) = 1$.",
            ],
            solucion=(
                "$\\dfrac{dy}{dx} = \\dfrac{\\sin(\\pi/2)}{1 - \\cos(\\pi/2)} = \\dfrac{1}{1 - 0} = 1$.\n\n"
                "**La tangente tiene pendiente $1$ en ese punto.** **Atención:** en $t = 0, 2\\pi, ...$, $x'(0) = 0$ y $y'(0) = 0$ — son **cúspides** donde la cicloide \"toca el suelo\". La pendiente de la tangente en una cúspide es **vertical** (la rueda invierte momentáneamente la dirección)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir 'curva paramétrica' con 'función'**. Una curva puede no ser gráfica de función (ej. círculo).",
              "**Olvidar el rango del parámetro.** $t \\in [0, \\pi]$ recorre solo la mitad del círculo, no el círculo completo.",
              "**Eliminar el parámetro sin verificar el rango resultante.** La curva cartesiana puede ser **un trozo** de lo esperado.",
              "**Confundir parametrización con curva.** Una curva puede parametrizarse de muchas maneras — la velocidad cambia, la curva no.",
              "**Aplicar $dy/dx = y'(t)/x'(t)$ cuando $x'(t) = 0$.** En esos puntos hay tangente vertical (o singular).",
          ]),

        b("resumen",
          puntos_md=[
              "**Curva paramétrica:** $(x(t), y(t))$ con $t$ en un intervalo.",
              "**Eliminar el parámetro:** despejar $t$ y sustituir, o usar identidades (pitagórica para trig).",
              "**Tangente:** $\\dfrac{dy}{dx} = \\dfrac{y'(t)}{x'(t)}$.",
              "**Tangentes verticales/horizontales:** cuando $x'$ o $y'$ se anulan respectivamente.",
              "**Curvas clásicas:** círculo, elipse, cicloide, espiral, hélice.",
              "**Una curva, infinitas parametrizaciones** — la velocidad depende de la parametrización; la geometría no.",
              "**Próxima lección:** coordenadas polares (revisitadas), una forma especial de parametrizar.",
          ]),
    ]
    return {
        "id": "lec-vec-1-1-parametricas",
        "title": "Ecuaciones paramétricas",
        "description": "Curvas $(x(t), y(t))$, eliminación del parámetro, rectas tangentes y curvas clásicas.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 1.2 Coordenadas polares
# =====================================================================
def lesson_1_2():
    blocks = [
        b("texto", body_md=(
            "Las **coordenadas polares** $(r, \\theta)$ ya las vimos como herramienta de integración (Cálculo "
            "Integral 6.3). Aquí las profundizamos como sistema para describir **curvas**: ecuaciones de la "
            "forma $r = f(\\theta)$ generan figuras imposibles o feas en cartesianas — cardioides, rosas, "
            "espirales — pero naturales en polares.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Convertir entre cartesianas y polares.\n"
            "- Reconocer y graficar curvas polares clásicas.\n"
            "- Calcular **tangentes** a curvas polares.\n"
            "- Calcular **áreas** y **longitudes** en polares."
        )),

        b("definicion",
          titulo="Curvas polares $r = f(\\theta)$",
          body_md=(
              "Una **curva polar** es el conjunto de puntos $(r, \\theta)$ con $r = f(\\theta)$. "
              "Equivalentemente, es la curva paramétrica:\n\n"
              "$$x(\\theta) = f(\\theta) \\cos\\theta, \\quad y(\\theta) = f(\\theta) \\sin\\theta$$\n\n"
              "**Convención:** $r$ puede ser **negativo** — el punto $(r, \\theta)$ con $r < 0$ se interpreta como $(|r|, \\theta + \\pi)$ (en la dirección opuesta).\n\n"
              "**Período:** muchas curvas polares se cierran al recorrer $\\theta$ un múltiplo de $\\pi$ o $2\\pi$. La cardioide $r = 1 + \\cos\\theta$ se cierra con $\\theta \\in [0, 2\\pi]$; la rosa $r = \\cos(2\\theta)$ con $\\theta \\in [0, \\pi]$ (cuatro pétalos)."
          )),

        formulas(
            titulo="Curvas polares clásicas",
            body=(
                "| Ecuación polar | Curva |\n|---|---|\n"
                "| $r = a$ | Círculo de radio $a$ centrado en el origen |\n"
                "| $r = 2a\\cos\\theta$ | Círculo de radio $a$ centrado en $(a, 0)$ |\n"
                "| $r = 2a\\sin\\theta$ | Círculo de radio $a$ centrado en $(0, a)$ |\n"
                "| $r = a + b\\cos\\theta$ | **Limaçon** (cardioide si $a = b$) |\n"
                "| $r = a\\cos(n\\theta)$ | **Rosa** de $n$ pétalos (si $n$ impar) o $2n$ pétalos (si $n$ par) |\n"
                "| $r = a\\theta$ | **Espiral arquimediana** |\n"
                "| $r = e^{a\\theta}$ | **Espiral logarítmica** |\n"
                "| $r^2 = a^2 \\cos(2\\theta)$ | **Lemniscata** (figura ocho) |"
            ),
        ),

        fig(
            "Galería de curvas polares clásicas. Grilla 2x2: PANEL ARRIBA-IZQ: cardioide r = 1 + "
            "cos(θ), forma de corazón. PANEL ARRIBA-DER: rosa de cuatro pétalos r = cos(2θ). "
            "PANEL ABAJO-IZQ: espiral arquimediana r = 0.3θ, varias vueltas saliendo del origen. "
            "PANEL ABAJO-DER: lemniscata (figura ocho) r² = cos(2θ). Cada una en color teal con "
            "fondo claro de cuadrícula polar (círculos concéntricos y radios). Etiquetas. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Convertir polar a cartesiana",
          problema_md="Convertir $r = 2\\cos\\theta$ a forma cartesiana.",
          pasos=[
              {"accion_md": "**Multiplicamos** por $r$: $r^2 = 2r\\cos\\theta$.\n\n"
                            "**Sustituimos** $r^2 = x^2 + y^2$ y $r\\cos\\theta = x$:\n\n"
                            "$x^2 + y^2 = 2x \\implies x^2 - 2x + y^2 = 0 \\implies (x - 1)^2 + y^2 = 1$.",
               "justificacion_md": "Multiplicar por $r$ es el truco estándar para conversión.",
               "es_resultado": False},
              {"accion_md": "**Es un círculo** de radio $1$ centrado en $(1, 0)$ — pasa por el origen.",
               "justificacion_md": "**Confirma la fórmula de la tabla:** $r = 2a\\cos\\theta$ con $a = 1$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Tangente a una curva polar",
          body_md=(
              "Para $r = f(\\theta)$ vista como paramétrica $x = r\\cos\\theta, y = r\\sin\\theta$:\n\n"
              "$$\\dfrac{dy}{dx} = \\dfrac{dy/d\\theta}{dx/d\\theta} = \\dfrac{f'(\\theta)\\sin\\theta + f(\\theta)\\cos\\theta}{f'(\\theta)\\cos\\theta - f(\\theta)\\sin\\theta}$$\n\n"
              "**En el origen** ($r = 0$ en $\\theta = \\theta_0$): la tangente tiene pendiente $\\tan\\theta_0$ — es decir, la curva pasa por el origen con dirección $\\theta_0$."
          )),

        b("teorema",
          nombre="Área en coordenadas polares",
          enunciado_md=(
              "El área de la región acotada por $r = f(\\theta)$ y los rayos $\\theta = \\alpha, \\theta = \\beta$ (con $f \\geq 0$) es:\n\n"
              "$$A = \\dfrac{1}{2} \\int_\\alpha^\\beta [f(\\theta)]^2 \\, d\\theta$$\n\n"
              "**Para área entre dos curvas polares** $r = f(\\theta)$ (exterior) y $r = g(\\theta)$ (interior):\n\n"
              "$$A = \\dfrac{1}{2} \\int_\\alpha^\\beta [f^2 - g^2] \\, d\\theta$$"
          ),
          demostracion_md=(
              "Idea: aproximar la región por **sectores circulares** infinitesimales de radio $r$ y ángulo $d\\theta$. Cada sector tiene área $\\frac{1}{2} r^2 \\, d\\theta$ (área del triángulo isósceles infinitesimal $\\to$ sector). Sumando con integral: $\\frac{1}{2} \\int r^2 \\, d\\theta$.\n\n"
              "**Comparación con cartesianas:** el factor $1/2$ en lugar de $1$ es porque cada sector tiene área $\\frac{1}{2} r \\cdot r \\, d\\theta$, no $r \\cdot r \\, d\\theta$."
          )),

        b("ejemplo_resuelto",
          titulo="Área de un pétalo",
          problema_md="Calcular el área de un pétalo de la rosa $r = \\cos(2\\theta)$.",
          pasos=[
              {"accion_md": "**Identificar el pétalo:** $r = \\cos(2\\theta) > 0$ cuando $-\\pi/4 < \\theta < \\pi/4$ (un pétalo a la derecha).",
               "justificacion_md": "El pétalo se cierra cuando $r$ vuelve a $0$.",
               "es_resultado": False},
              {"accion_md": "**Aplicar fórmula:**\n\n"
                            "$A = \\dfrac{1}{2} \\int_{-\\pi/4}^{\\pi/4} \\cos^2(2\\theta) \\, d\\theta = \\dfrac{1}{2} \\int_{-\\pi/4}^{\\pi/4} \\dfrac{1 + \\cos(4\\theta)}{2} \\, d\\theta$.",
               "justificacion_md": "Identidad de ángulo doble.",
               "es_resultado": False},
              {"accion_md": "$= \\dfrac{1}{4} \\left[\\theta + \\dfrac{\\sin(4\\theta)}{4}\\right]_{-\\pi/4}^{\\pi/4} = \\dfrac{1}{4}(\\pi/2 + 0) = \\dfrac{\\pi}{8}$.",
               "justificacion_md": "$\\sin(\\pi) = \\sin(-\\pi) = 0$. **Lección:** la rosa $\\cos(2\\theta)$ tiene 4 pétalos, área total $4 \\cdot \\pi/8 = \\pi/2$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Longitud de arco en polares",
          enunciado_md=(
              "Para $r = f(\\theta)$ con $\\theta \\in [\\alpha, \\beta]$:\n\n"
              "$$L = \\int_\\alpha^\\beta \\sqrt{r^2 + (r')^2} \\, d\\theta = \\int_\\alpha^\\beta \\sqrt{[f(\\theta)]^2 + [f'(\\theta)]^2} \\, d\\theta$$"
          ),
          demostracion_md=(
              "Como paramétrica: $x = r\\cos\\theta, y = r\\sin\\theta$. $L = \\int \\sqrt{(x')^2 + (y')^2} \\, d\\theta$.\n\n"
              "$x' = r'\\cos\\theta - r\\sin\\theta$, $y' = r'\\sin\\theta + r\\cos\\theta$.\n\n"
              "$(x')^2 + (y')^2 = (r')^2 + r^2$ (después de expandir y simplificar). De ahí la fórmula."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El área dentro del círculo polar $r = a$ es:",
                  "opciones_md": ["$\\pi a$", "$\\pi a^2$", "$\\pi a^2 / 2$", "$2\\pi a$"],
                  "correcta": "B",
                  "pista_md": "Aplica $A = \\dfrac{1}{2} \\int_0^{2\\pi} a^2 \\, d\\theta$.",
                  "explicacion_md": (
                      "$A = \\dfrac{1}{2} \\int_0^{2\\pi} a^2 \\, d\\theta = \\dfrac{1}{2} \\cdot a^2 \\cdot 2\\pi = \\pi a^2$. ✓ (Recupera la fórmula clásica.)"
                  ),
              },
              {
                  "enunciado_md": "$r = 1 + \\cos\\theta$ es una:",
                  "opciones_md": ["Espiral", "Cardioide", "Rosa", "Limaçon con loop interno"],
                  "correcta": "B",
                  "pista_md": "Es el caso $a = b$ del limaçon $r = a + b\\cos\\theta$.",
                  "explicacion_md": (
                      "**Cardioide** (corazón). El máximo $r = 2$ en $\\theta = 0$, mínimo $r = 0$ en $\\theta = \\pi$ (la curva toca el origen, formando la 'mella')."
                  ),
              },
          ]),

        ej(
            titulo="Área dentro de una cardioide",
            enunciado="Calcula el área dentro de la cardioide $r = 1 + \\cos\\theta$.",
            pistas=[
                "$\\theta$ recorre $[0, 2\\pi]$ para una cardioide completa.",
                "Necesitarás $\\int \\cos^2\\theta \\, d\\theta$ — usa $\\cos^2 = (1 + \\cos 2\\theta)/2$.",
            ],
            solucion=(
                "$A = \\dfrac{1}{2}\\int_0^{2\\pi}(1 + \\cos\\theta)^2 \\, d\\theta = \\dfrac{1}{2}\\int_0^{2\\pi}(1 + 2\\cos\\theta + \\cos^2\\theta) \\, d\\theta$.\n\n"
                "$\\int_0^{2\\pi} 1 = 2\\pi$. $\\int_0^{2\\pi} 2\\cos\\theta = 0$. $\\int_0^{2\\pi} \\cos^2\\theta = \\pi$.\n\n"
                "$A = \\dfrac{1}{2}(2\\pi + 0 + \\pi) = \\dfrac{3\\pi}{2}$."
            ),
        ),

        ej(
            titulo="Longitud de una espiral",
            enunciado="Halla la longitud de la espiral $r = e^\\theta$ entre $\\theta = 0$ y $\\theta = 2\\pi$.",
            pistas=[
                "$r = e^\\theta$, $r' = e^\\theta$. $r^2 + (r')^2 = 2 e^{2\\theta}$.",
                "$\\sqrt{2 e^{2\\theta}} = \\sqrt{2} \\, e^\\theta$.",
            ],
            solucion=(
                "$L = \\int_0^{2\\pi} \\sqrt{2} \\, e^\\theta \\, d\\theta = \\sqrt{2}(e^{2\\pi} - 1)$.\n\n"
                "Numéricamente: $\\sqrt{2}(534.49 - 1) \\approx 754.5$ — la espiral logarítmica crece rapidísimo."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $1/2$** en la fórmula de área polar. **No es** $\\int r^2 d\\theta$, es $\\dfrac{1}{2}\\int r^2 d\\theta$.",
              "**Aplicar fórmula de área cuando $r < 0$** sin reflexionar. La fórmula $\\dfrac{1}{2}\\int r^2 d\\theta$ funciona porque $r^2 \\geq 0$, pero la región puede no ser la esperada.",
              "**Confundir longitud polar con cartesiana.** En polares hay un factor $r^2$ extra dentro de la raíz que no aparece en $\\sqrt{1 + (f')^2}$ de cartesianas.",
              "**Olvidar el rango correcto de $\\theta$.** Las rosas con $n$ par tienen $2n$ pétalos en $[0, 2\\pi]$ — pero con $n$ impar tienen $n$ pétalos en $[0, \\pi]$ (no $2n$).",
              "**Convertir $r = a + b\\cos\\theta$ a cartesianas** sin reescribir primero como $r^2 = ar + br\\cos\\theta$. El truco \"multiplicar por $r$\" solo funciona si la ecuación es lineal en $r$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Curva polar:** $r = f(\\theta)$, equivale a paramétrica $x = r\\cos\\theta, y = r\\sin\\theta$.",
              "**Conversión polar → cartesiana:** multiplicar por $r$, sustituir $r^2 = x^2+y^2$, $r\\cos\\theta = x$, $r\\sin\\theta = y$.",
              "**Área:** $A = \\dfrac{1}{2}\\int_\\alpha^\\beta r^2 \\, d\\theta$ (factor $1/2$ esencial).",
              "**Longitud:** $L = \\int_\\alpha^\\beta \\sqrt{r^2 + (r')^2} \\, d\\theta$.",
              "**Curvas clásicas:** cardioide, rosa, limaçon, espiral, lemniscata.",
              "**Próxima lección:** funciones vectoriales — generalización a 3D.",
          ]),
    ]
    return {
        "id": "lec-vec-1-2-polares",
        "title": "Coordenadas polares",
        "description": "Curvas polares $r = f(\\theta)$, conversión, áreas y longitudes en polares.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 1.3 Funciones vectoriales
# =====================================================================
def lesson_1_3():
    blocks = [
        b("texto", body_md=(
            "Una **función vectorial** es una función que asigna a cada $t$ un **vector** "
            "$\\vec{r}(t) \\in \\mathbb{R}^3$. Es la versión más natural de las curvas paramétricas — "
            "encapsula $(x(t), y(t), z(t))$ en una sola entidad. Cuando $\\vec{r}(t)$ representa la "
            "posición de un objeto, su derivada es la **velocidad**, la magnitud de la velocidad es la "
            "**rapidez**, y la segunda derivada es la **aceleración**. Es el lenguaje natural de la mecánica.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir y manipular funciones vectoriales $\\vec{r}: I \\to \\mathbb{R}^3$.\n"
            "- Calcular **límites, derivadas e integrales** de funciones vectoriales.\n"
            "- Aplicar las **reglas de derivación** para productos punto y cruz.\n"
            "- Reconocer la **hélice** y otras curvas en 3D."
        )),

        b("definicion",
          titulo="Función vectorial",
          body_md=(
              "Una **función vectorial** (o **curva en $\\mathbb{R}^3$**) es:\n\n"
              "$$\\vec{r}(t) = \\langle x(t), y(t), z(t) \\rangle = x(t) \\vec{i} + y(t) \\vec{j} + z(t) \\vec{k}$$\n\n"
              "donde $x(t), y(t), z(t)$ son las **funciones componentes**.\n\n"
              "**Su gráfica** es la curva traza por la punta del vector cuando $t$ recorre el dominio. Es **una curva en el espacio 3D** (o 2D si solo hay dos componentes).\n\n"
              "**Operaciones componente a componente:** límite, derivada, integral se aplican a cada componente por separado."
          )),

        b("definicion",
          titulo="Límites, derivadas, integrales",
          body_md=(
              "**Límite:** $\\displaystyle\\lim_{t \\to a} \\vec{r}(t) = \\langle \\lim x(t), \\lim y(t), \\lim z(t) \\rangle$ (existe si los tres límites existen).\n\n"
              "**Continuidad:** $\\vec{r}$ es continua en $a$ si $\\lim_{t \\to a} \\vec{r}(t) = \\vec{r}(a)$.\n\n"
              "**Derivada:**\n\n"
              "$$\\vec{r}'(t) = \\langle x'(t), y'(t), z'(t) \\rangle$$\n\n"
              "**Integral (definida):**\n\n"
              "$$\\int_a^b \\vec{r}(t) \\, dt = \\left\\langle \\int_a^b x(t) \\, dt, \\int_a^b y(t) \\, dt, \\int_a^b z(t) \\, dt \\right\\rangle$$"
          )),

        b("intuicion",
          titulo="Velocidad, rapidez, aceleración",
          body_md=(
              "Si $\\vec{r}(t)$ es la **posición** de una partícula en el tiempo $t$:\n\n"
              "**Velocidad:** $\\vec{v}(t) = \\vec{r}'(t)$ — vector tangente a la curva, dirección del movimiento.\n\n"
              "**Rapidez:** $\\|\\vec{v}(t)\\| = \\|\\vec{r}'(t)\\|$ — magnitud escalar.\n\n"
              "**Aceleración:** $\\vec{a}(t) = \\vec{v}'(t) = \\vec{r}''(t)$.\n\n"
              "**Distancia recorrida** entre $t = a$ y $t = b$: longitud de arco $L = \\int_a^b \\|\\vec{v}(t)\\| \\, dt$ (lección 1.4).\n\n"
              "Toda la cinemática 3D se construye sobre esto."
          )),

        fig(
            "Hélice circular en 3D. Sistema de ejes x, y, z con el eje z vertical. Mostrar la curva "
            "r(t) = (cos(t), sin(t), t/3) trazada en color teal grueso, dando varias vueltas "
            "alrededor del eje z mientras sube. En un punto destacado de la curva, mostrar el "
            "vector tangente r'(t) = (-sin(t), cos(t), 1/3) en color ámbar. La 'sombra' de la "
            "hélice (proyección al plano xy) es un círculo, dibujada en gris punteado. Etiquetas: "
            "'r(t)', 'r'(t)' (tangente), ejes. Vista isométrica clara. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Hélice circular",
          problema_md="Sea $\\vec{r}(t) = \\langle \\cos t, \\sin t, t \\rangle$. Calcular $\\vec{r}'(t)$, $\\vec{r}''(t)$ y la rapidez.",
          pasos=[
              {"accion_md": "**Componente a componente:**\n\n"
                            "$\\vec{r}'(t) = \\langle -\\sin t, \\cos t, 1 \\rangle$ (velocidad).\n\n"
                            "$\\vec{r}''(t) = \\langle -\\cos t, -\\sin t, 0 \\rangle$ (aceleración).",
               "justificacion_md": "Derivadas estándar.",
               "es_resultado": False},
              {"accion_md": "**Rapidez:** $\\|\\vec{r}'(t)\\| = \\sqrt{\\sin^2 t + \\cos^2 t + 1} = \\sqrt{2}$.",
               "justificacion_md": "**Constante** — la hélice se recorre con rapidez uniforme. Como $\\vec{r}''$ es perpendicular a $\\vec{r}'$ (verifica: $\\vec{r}'' \\cdot \\vec{r}' = \\sin\\cos - \\cos\\sin + 0 = 0$), la aceleración es **puramente normal** — la partícula gira sin acelerar.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Reglas de derivación vectorial",
            body=(
                "Si $\\vec{u}, \\vec{v}$ son funciones vectoriales y $f$ escalar, todas derivables:\n\n"
                "| Operación | Derivada |\n|---|---|\n"
                "| $(\\vec{u} + \\vec{v})'$ | $\\vec{u}' + \\vec{v}'$ |\n"
                "| $(c\\vec{u})'$ | $c\\vec{u}'$ |\n"
                "| $(f\\vec{u})'$ | $f'\\vec{u} + f\\vec{u}'$ |\n"
                "| $(\\vec{u} \\cdot \\vec{v})'$ | $\\vec{u}' \\cdot \\vec{v} + \\vec{u} \\cdot \\vec{v}'$ |\n"
                "| $(\\vec{u} \\times \\vec{v})'$ | $\\vec{u}' \\times \\vec{v} + \\vec{u} \\times \\vec{v}'$ |\n"
                "| $\\vec{u}(f(t))$ | $\\vec{u}'(f(t)) \\cdot f'(t)$ (cadena) |\n\n"
                "**Atención al producto cruz:** **el orden importa** porque no es conmutativo. Mantener $\\vec{u} \\times \\vec{v}$ en ese orden, no intercambiar."
            ),
        ),

        b("teorema",
          nombre="Vector constante en magnitud → derivada perpendicular",
          enunciado_md=(
              "Si $\\|\\vec{r}(t)\\|$ es **constante**, entonces $\\vec{r}(t) \\perp \\vec{r}'(t)$ para todo $t$.\n\n"
              "**Aplicación:** la velocidad de una partícula que se mueve sobre una esfera de radio $R$ "
              "es siempre **tangente a la esfera** (perpendicular al vector posición desde el centro)."
          ),
          demostracion_md=(
              "$\\|\\vec{r}\\|^2 = \\vec{r} \\cdot \\vec{r} = $ constante. Derivando con la regla del producto: $2 \\vec{r} \\cdot \\vec{r}' = 0$, así $\\vec{r} \\perp \\vec{r}'$."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicar regla del producto cruz",
          problema_md=(
              "Si $\\vec{u}(t) = \\langle t, t^2, t^3 \\rangle$ y $\\vec{v}(t) = \\langle 1, t, t^2 \\rangle$, calcular $\\dfrac{d}{dt}[\\vec{u}(t) \\times \\vec{v}(t)]$ usando la regla del producto."
          ),
          pasos=[
              {"accion_md": "$\\vec{u}'(t) = \\langle 1, 2t, 3t^2 \\rangle$, $\\vec{v}'(t) = \\langle 0, 1, 2t \\rangle$.",
               "justificacion_md": "Derivadas componente a componente.",
               "es_resultado": False},
              {"accion_md": "**Aplicar la regla:** $(\\vec{u} \\times \\vec{v})' = \\vec{u}' \\times \\vec{v} + \\vec{u} \\times \\vec{v}'$.\n\n"
                            "**Lección:** en un examen, hacer ambos productos cruz es trabajo, pero el procedimiento es mecánico.",
               "justificacion_md": "El orden importa por la no-conmutatividad.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\vec{r}(t) = \\langle t^2, e^t, \\sin t \\rangle$, $\\vec{r}'(0) = ?$",
                  "opciones_md": [
                      "$\\langle 0, 1, 1 \\rangle$",
                      "$\\langle 0, 0, 0 \\rangle$",
                      "$\\langle 0, 1, 0 \\rangle$",
                      "$\\langle 2t, e^t, \\cos t \\rangle$",
                  ],
                  "correcta": "A",
                  "pista_md": "Deriva componente a componente y evalúa en $t = 0$.",
                  "explicacion_md": (
                      "$\\vec{r}'(t) = \\langle 2t, e^t, \\cos t \\rangle$. En $t = 0$: $\\langle 0, 1, 1 \\rangle$."
                  ),
              },
              {
                  "enunciado_md": "Si una partícula se mueve sobre una esfera, su velocidad es:",
                  "opciones_md": [
                      "Paralela al vector posición.",
                      "Perpendicular al vector posición.",
                      "Cero.",
                      "De magnitud constante.",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\|\\vec{r}\\| = R$ constante implica $\\vec{r} \\cdot \\vec{r}' = 0$.",
                  "explicacion_md": (
                      "Posición sobre la esfera = vector de magnitud constante = perpendicular a su derivada (velocidad). **La rapidez puede no ser constante**, solo la magnitud de la posición."
                  ),
              },
          ]),

        ej(
            titulo="Trayectoria circular uniforme",
            enunciado=(
                "Sea $\\vec{r}(t) = \\langle 2\\cos(3t), 2\\sin(3t), 0 \\rangle$. Calcula velocidad, rapidez y aceleración. ¿Qué tipo de movimiento describe?"
            ),
            pistas=[
                "$\\vec{r}' = \\langle -6\\sin(3t), 6\\cos(3t), 0 \\rangle$.",
                "$\\|\\vec{r}'\\|^2 = 36$.",
            ],
            solucion=(
                "$\\vec{v}(t) = \\langle -6\\sin(3t), 6\\cos(3t), 0 \\rangle$. **Rapidez** $= 6$ (constante).\n\n"
                "$\\vec{a}(t) = \\langle -18\\cos(3t), -18\\sin(3t), 0 \\rangle = -9 \\vec{r}(t)$.\n\n"
                "**Movimiento circular uniforme:** rapidez constante, aceleración centrípeta apuntando al centro $\\vec{0}$. La fórmula $\\vec{a} = -\\omega^2 \\vec{r}$ con $\\omega = 3$ rad/s confirma la cinemática estándar."
            ),
        ),

        ej(
            titulo="Integral vectorial",
            enunciado=(
                "Calcula $\\int_0^1 \\langle 2t, e^t, \\sin(\\pi t) \\rangle \\, dt$."
            ),
            pistas=[
                "Integra cada componente por separado.",
            ],
            solucion=(
                "$\\int_0^1 2t \\, dt = 1$.\n\n"
                "$\\int_0^1 e^t \\, dt = e - 1$.\n\n"
                "$\\int_0^1 \\sin(\\pi t) \\, dt = \\dfrac{2}{\\pi}$.\n\n"
                "**Resultado:** $\\langle 1, e - 1, 2/\\pi \\rangle$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir función vectorial con función escalar.** $\\vec{r}(t)$ es un vector — sus operaciones componente a componente.",
              "**Aplicar producto en lugar de suma a $(\\vec{u} \\cdot \\vec{v})'$.** La regla es $\\vec{u}' \\cdot \\vec{v} + \\vec{u} \\cdot \\vec{v}'$ — análogo a producto escalar.",
              "**Cambiar el orden en el producto cruz** después de derivar. **No es conmutativo:** $(\\vec{u} \\times \\vec{v})' = \\vec{u}' \\times \\vec{v} + \\vec{u} \\times \\vec{v}'$, no $\\vec{v} \\times \\vec{u}' + ...$",
              "**Confundir velocidad con rapidez.** Velocidad es vectorial; rapidez es su magnitud (escalar).",
              "**Olvidar el dominio.** Si una componente no está definida en cierto $t$, la función vectorial tampoco.",
          ]),

        b("resumen",
          puntos_md=[
              "**Función vectorial:** $\\vec{r}(t) = \\langle x(t), y(t), z(t) \\rangle$.",
              "**Operaciones componente a componente:** límite, derivada, integral.",
              "**Cinemática:** velocidad $\\vec{r}'$, rapidez $\\|\\vec{r}'\\|$, aceleración $\\vec{r}''$.",
              "**Reglas de derivación:** producto, escalar por vector, productos punto y cruz.",
              "**Magnitud constante ⇒ derivada perpendicular** (consecuencia de $\\vec{r} \\cdot \\vec{r} = $ const).",
              "**Curvas clásicas en 3D:** hélice, espirales, parábola en el espacio.",
              "**Próxima lección:** longitud de arco — integrar la rapidez.",
          ]),
    ]
    return {
        "id": "lec-vec-1-3-funciones-vectoriales",
        "title": "Funciones vectoriales",
        "description": "$\\vec{r}(t)$ en $\\mathbb{R}^3$, derivadas e integrales, cinemática y reglas de productos.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 1.4 Longitud de curva
# =====================================================================
def lesson_1_4():
    blocks = [
        b("texto", body_md=(
            "Calcular la **longitud de una curva** en 2D o 3D es una aplicación directa de la integral. "
            "La idea es la misma de Cálculo Integral 3.5: aproximar con segmentos rectos y tomar el límite. "
            "En forma vectorial queda especialmente compacta: $L = \\int \\|\\vec{r}'(t)\\| \\, dt$ — "
            "la integral de la rapidez.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular **longitudes** de curvas dadas como $\\vec{r}(t)$, paramétricas o polares.\n"
            "- Comprender la **invarianza bajo reparametrización** (la longitud no cambia).\n"
            "- Manejar la **función longitud de arco** $s(t)$.\n"
            "- Reparametrizar curvas **por longitud de arco**."
        )),

        b("teorema",
          nombre="Longitud de una curva vectorial",
          enunciado_md=(
              "Para una curva $\\vec{r}(t) = \\langle x(t), y(t), z(t) \\rangle$ con $t \\in [a, b]$ y $\\vec{r}'$ continua:\n\n"
              "$$L = \\int_a^b \\|\\vec{r}'(t)\\| \\, dt = \\int_a^b \\sqrt{[x'(t)]^2 + [y'(t)]^2 + [z'(t)]^2} \\, dt$$\n\n"
              "**Casos especiales:**\n\n"
              "- **2D paramétrica:** $L = \\int \\sqrt{(x')^2 + (y')^2} \\, dt$.\n"
              "- **2D cartesiana** $y = f(x)$ (con $x = t$): $L = \\int \\sqrt{1 + (f')^2} \\, dx$ (la conocida).\n"
              "- **Polar** $r = f(\\theta)$: $L = \\int \\sqrt{r^2 + (r')^2} \\, d\\theta$ (lección 1.2).\n\n"
              "**Si $\\vec{r}$ se interpreta como posición:** $L$ es la **distancia recorrida** entre $t = a$ y $t = b$."
          ),
          demostracion_md=(
              "Aproximar la curva con poligonal: dividir $[a, b]$ en $n$ subintervalos. La longitud de cada segmento es $\\|\\vec{r}(t_i) - \\vec{r}(t_{i-1})\\| \\approx \\|\\vec{r}'(t_i^*)\\| \\Delta t$ por el TVM. Sumando y tomando el límite $n \\to \\infty$ da la integral."
          )),

        b("ejemplo_resuelto",
          titulo="Longitud de un arco de hélice",
          problema_md="Calcular la longitud de la hélice $\\vec{r}(t) = \\langle \\cos t, \\sin t, t \\rangle$ entre $t = 0$ y $t = 2\\pi$.",
          pasos=[
              {"accion_md": "$\\vec{r}'(t) = \\langle -\\sin t, \\cos t, 1 \\rangle$. $\\|\\vec{r}'(t)\\| = \\sqrt{\\sin^2 + \\cos^2 + 1} = \\sqrt{2}$.",
               "justificacion_md": "Rapidez constante.",
               "es_resultado": False},
              {"accion_md": "$L = \\int_0^{2\\pi} \\sqrt{2} \\, dt = 2\\pi\\sqrt{2}$.",
               "justificacion_md": "**Verificación intuitiva:** la hélice da una vuelta completa (perímetro $2\\pi$ del círculo de radio $1$) mientras sube $2\\pi$ en $z$. Por Pitágoras: $\\sqrt{(2\\pi)^2 + (2\\pi)^2} = 2\\pi\\sqrt{2}$. ✓",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Longitud de una parábola",
          problema_md="Calcular la longitud de $y = x^2$ entre $x = 0$ y $x = 1$.",
          pasos=[
              {"accion_md": "**Parametrizar:** $\\vec{r}(t) = \\langle t, t^2 \\rangle$, $t \\in [0, 1]$. $\\vec{r}'(t) = \\langle 1, 2t \\rangle$. $\\|\\vec{r}'\\| = \\sqrt{1 + 4t^2}$.",
               "justificacion_md": "Cualquier $y = f(x)$ se parametriza con $x = t$.",
               "es_resultado": False},
              {"accion_md": "$L = \\int_0^1 \\sqrt{1 + 4t^2} \\, dt$.\n\n"
                            "**Sustitución hiperbólica** $2t = \\sinh u$ (o por tabla): $L = \\dfrac{\\sqrt{5}}{2} + \\dfrac{1}{4}\\ln(2 + \\sqrt{5})$.",
               "justificacion_md": "Aproximadamente $1.479$. **Lección:** la mayoría de longitudes no tienen forma elemental.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Invarianza bajo reparametrización",
          enunciado_md=(
              "Si $\\vec{r}_1(t)$ y $\\vec{r}_2(s)$ son **dos parametrizaciones** de la misma curva (relacionadas por $t = g(s)$ con $g$ creciente y derivable), entonces calcular $L$ con cualquiera da el **mismo resultado**.\n\n"
              "**Consecuencia:** la longitud es una propiedad **geométrica** de la curva, independiente de cómo la parametricemos."
          ),
          demostracion_md=(
              "Por cambio de variable: $L_2 = \\int \\|\\vec{r}_2'(s)\\| \\, ds = \\int \\|\\vec{r}_1'(g(s))\\| \\cdot g'(s) \\, ds = \\int \\|\\vec{r}_1'(t)\\| \\, dt = L_1$.\n\n"
              "Las parametrizaciones rápidas y lentas dan la misma longitud porque la rapidez se cancela con $dt$."
          )),

        b("definicion",
          titulo="Función longitud de arco",
          body_md=(
              "Dada $\\vec{r}(t)$ en $[a, b]$, la **función longitud de arco** desde $a$ hasta $t$ es:\n\n"
              "$$s(t) = \\int_a^t \\|\\vec{r}'(\\tau)\\| \\, d\\tau$$\n\n"
              "**Propiedades:**\n\n"
              "- $s(a) = 0, s(b) = L$.\n"
              "- $s(t)$ es **estrictamente creciente** (suponiendo $\\|\\vec{r}'\\| > 0$).\n"
              "- Por TFC: $\\dfrac{ds}{dt} = \\|\\vec{r}'(t)\\|$.\n\n"
              "**$s$ tiene una propiedad muy especial:** mide \"la posición a lo largo de la curva\" — un parámetro **intrínseco** que no depende de cómo se recorre."
          )),

        b("definicion",
          titulo="Reparametrización por longitud de arco",
          body_md=(
              "Como $s(t)$ es invertible, podemos despejar $t = t(s)$ y reescribir:\n\n"
              "$$\\vec{r}(s) = \\vec{r}(t(s))$$\n\n"
              "Ahora **el parámetro mismo es la longitud de arco**. Tiene la propiedad notable:\n\n"
              "$$\\|\\vec{r}'(s)\\| = 1 \\quad \\text{(rapidez unitaria siempre)}$$\n\n"
              "**Por qué importa:** muchas fórmulas se simplifican drásticamente con esta parametrización (curvatura, vectores T/N/B, fórmulas de Frenet-Serret en lecciones siguientes).\n\n"
              "**En la práctica:** rara vez se hace esta reparametrización explícitamente — es difícil. Pero conceptualmente es importante saber que existe."
          )),

        b("ejemplo_resuelto",
          titulo="Reparametrizar una hélice por longitud de arco",
          problema_md="Reparametrizar $\\vec{r}(t) = \\langle \\cos t, \\sin t, t \\rangle$ por longitud de arco.",
          pasos=[
              {"accion_md": "**Función longitud de arco** desde $t = 0$:\n\n"
                            "$s(t) = \\int_0^t \\sqrt{2} \\, d\\tau = t\\sqrt{2}$.",
               "justificacion_md": "Rapidez constante $\\sqrt{2}$ (visto antes).",
               "es_resultado": False},
              {"accion_md": "**Despejar $t$:** $t = s/\\sqrt{2}$.\n\n"
                            "**Reparametrización:**\n\n"
                            "$\\vec{r}(s) = \\langle \\cos(s/\\sqrt{2}), \\sin(s/\\sqrt{2}), s/\\sqrt{2} \\rangle$.",
               "justificacion_md": "Sustitución directa.",
               "es_resultado": False},
              {"accion_md": "**Verificación:** $\\vec{r}'(s) = \\dfrac{1}{\\sqrt{2}} \\langle -\\sin(s/\\sqrt{2}), \\cos(s/\\sqrt{2}), 1 \\rangle$.\n\n"
                            "$\\|\\vec{r}'(s)\\| = \\dfrac{1}{\\sqrt{2}} \\sqrt{1 + 1} = 1$. ✓",
               "justificacion_md": "**Confirmado: rapidez unitaria.** La hélice es uno de los pocos casos donde la reparametrización es elemental.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La longitud del segmento $\\vec{r}(t) = (1-t)\\vec{P} + t\\vec{Q}$ en $t \\in [0, 1]$ es:",
                  "opciones_md": [
                      "$\\|\\vec{Q}\\| - \\|\\vec{P}\\|$",
                      "$\\|\\vec{Q} - \\vec{P}\\|$",
                      "$\\|\\vec{P} + \\vec{Q}\\|$",
                      "$1$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\vec{r}'(t) = \\vec{Q} - \\vec{P}$ (constante).",
                  "explicacion_md": (
                      "$\\vec{r}'(t) = \\vec{Q} - \\vec{P}$, $\\|\\vec{r}'\\| = \\|\\vec{Q} - \\vec{P}\\|$. $L = \\int_0^1 \\|\\vec{Q} - \\vec{P}\\| dt = \\|\\vec{Q} - \\vec{P}\\|$. **Es la distancia entre $P$ y $Q$.**"
                  ),
              },
              {
                  "enunciado_md": "La parametrización por longitud de arco $\\vec{r}(s)$ tiene la propiedad:",
                  "opciones_md": [
                      "$\\|\\vec{r}(s)\\| = 1$ siempre.",
                      "$\\|\\vec{r}'(s)\\| = 1$ siempre.",
                      "$\\vec{r}(0) = \\vec{0}$.",
                      "$s$ es siempre $0$.",
                  ],
                  "correcta": "B",
                  "pista_md": "Velocidad unitaria — el parámetro mismo es la distancia recorrida.",
                  "explicacion_md": (
                      "$\\|\\vec{r}'(s)\\| = ds/ds = 1$. Por eso el parámetro de arco simplifica las fórmulas de curvatura, T/N/B, etc."
                  ),
              },
          ]),

        ej(
            titulo="Longitud de una curva 3D",
            enunciado=(
                "Calcula la longitud de $\\vec{r}(t) = \\langle t, t^2, \\dfrac{2t^3}{3} \\rangle$ entre $t = 0$ y $t = 1$."
            ),
            pistas=[
                "$\\vec{r}'(t) = \\langle 1, 2t, 2t^2 \\rangle$.",
                "$\\|\\vec{r}'\\|^2 = 1 + 4t^2 + 4t^4 = (1 + 2t^2)^2$ (cuadrado perfecto, ¡suerte!).",
                "$\\|\\vec{r}'\\| = 1 + 2t^2$.",
            ],
            solucion=(
                "$L = \\int_0^1 (1 + 2t^2) \\, dt = 1 + 2/3 = 5/3$.\n\n"
                "**Curva 'diseñada':** la elección de coeficientes hace que el integrando sea un cuadrado perfecto. En la naturaleza, las longitudes rara vez son tan amables."
            ),
        ),

        ej(
            titulo="Función longitud de arco",
            enunciado=(
                "Para $\\vec{r}(t) = \\langle 3\\cos t, 3\\sin t, 4t \\rangle$, calcula $s(t)$ desde $t = 0$."
            ),
            pistas=[
                "$\\vec{r}' = \\langle -3\\sin t, 3\\cos t, 4 \\rangle$.",
                "$\\|\\vec{r}'\\|^2 = 9 + 16 = 25$.",
            ],
            solucion=(
                "$\\|\\vec{r}'(t)\\| = 5$. $s(t) = \\int_0^t 5 \\, d\\tau = 5t$.\n\n"
                "**Reparametrización por longitud de arco:** $t = s/5$, así $\\vec{r}(s) = \\langle 3\\cos(s/5), 3\\sin(s/5), 4s/5 \\rangle$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar la raíz** en $\\|\\vec{r}'\\|$. La rapidez es la magnitud, no el cuadrado.",
              "**Calcular longitud con $\\vec{r}$ en vez de $\\vec{r}'$.** La fórmula usa la **derivada** (velocidad).",
              "**Asumir que el integrando tiene antiderivada elemental.** La mayoría no — requieren métodos numéricos.",
              "**Confundir distancia recorrida con desplazamiento.** $L = \\int \\|\\vec{r}'\\| dt$ (siempre $\\geq 0$); desplazamiento $= \\vec{r}(b) - \\vec{r}(a)$ (vector).",
              "**Pensar que $s(t) = t$ siempre.** $s = t$ solo si $\\|\\vec{r}'\\| = 1$ (parametrización por arco).",
          ]),

        b("resumen",
          puntos_md=[
              "**Longitud:** $L = \\int_a^b \\|\\vec{r}'(t)\\| \\, dt$ — integral de la rapidez.",
              "**Invariante** bajo reparametrización: propiedad geométrica de la curva.",
              "**Función longitud de arco:** $s(t) = \\int_a^t \\|\\vec{r}'\\| d\\tau$, con $ds/dt = \\|\\vec{r}'\\|$.",
              "**Reparametrización por arco:** $\\|\\vec{r}'(s)\\| = 1$ — rapidez unitaria, parámetro intrínseco.",
              "**Casos calculables:** hélice, líneas, ciertas curvas 'diseñadas'. La mayoría requiere métodos numéricos.",
              "**Próxima lección:** vectores tangente/normal/binormal — el triedro de Frenet.",
          ]),
    ]
    return {
        "id": "lec-vec-1-4-longitud",
        "title": "Longitud de curva",
        "description": "Longitud $L = \\int \\|\\vec{r}'\\| dt$, función longitud de arco y reparametrización.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# 1.5 Vectores de curvas (T, N, B)
# =====================================================================
def lesson_1_5():
    blocks = [
        b("texto", body_md=(
            "Una curva en el espacio 3D tiene una **estructura geométrica intrínseca** descrita por tres "
            "vectores ortogonales en cada punto: el **tangente** $\\vec{T}$, el **normal principal** $\\vec{N}$ "
            "y el **binormal** $\\vec{B}$. Forman un sistema de coordenadas móvil — el **triedro de Frenet** — "
            "que se desliza por la curva. Es la base para describir curvatura, torsión y la geometría "
            "diferencial de curvas.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular los vectores **$\\vec{T}, \\vec{N}, \\vec{B}$** en cada punto de una curva.\n"
            "- Reconocer los **planos osculador, normal y rectificante**.\n"
            "- Comprender el carácter **intrínseco** del triedro de Frenet."
        )),

        b("definicion",
          titulo="Vector tangente unitario $\\vec{T}$",
          body_md=(
              "Para una curva $\\vec{r}(t)$ con $\\vec{r}'(t) \\neq \\vec{0}$:\n\n"
              "$$\\vec{T}(t) = \\dfrac{\\vec{r}'(t)}{\\|\\vec{r}'(t)\\|}$$\n\n"
              "Es el **vector velocidad normalizado** — apunta en la dirección del movimiento, magnitud $1$.\n\n"
              "**Propiedad:** $\\|\\vec{T}\\| = 1$ siempre. Por la lección 1.3 (magnitud constante → derivada perpendicular), $\\vec{T} \\perp \\vec{T}'$. **Esto va a ser clave** para definir $\\vec{N}$."
          )),

        b("definicion",
          titulo="Vector normal principal $\\vec{N}$",
          body_md=(
              "$$\\vec{N}(t) = \\dfrac{\\vec{T}'(t)}{\\|\\vec{T}'(t)\\|}$$\n\n"
              "Es la **derivada del tangente, normalizada**. Como $\\vec{T}' \\perp \\vec{T}$:\n\n"
              "$$\\vec{N} \\perp \\vec{T}$$\n\n"
              "**Geometría:** $\\vec{N}$ apunta en la dirección hacia donde la curva 'se está doblando' — el lado **cóncavo**. Es la dirección de la **aceleración centrípeta** en mecánica.\n\n"
              "**Convención:** $\\vec{N}$ siempre es **unitario**. Si la curva es una recta, $\\vec{T}$ es constante y $\\vec{T}' = \\vec{0}$ — $\\vec{N}$ no está definido. Tiene sentido: una recta no se dobla, no hay 'lado cóncavo'."
          )),

        b("definicion",
          titulo="Vector binormal $\\vec{B}$",
          body_md=(
              "$$\\vec{B}(t) = \\vec{T}(t) \\times \\vec{N}(t)$$\n\n"
              "**Propiedades automáticas:**\n\n"
              "- $\\vec{B}$ es **unitario** (porque $\\vec{T}, \\vec{N}$ son unitarios y perpendiculares).\n"
              "- $\\vec{B} \\perp \\vec{T}$ y $\\vec{B} \\perp \\vec{N}$.\n\n"
              "$\\vec{T}, \\vec{N}, \\vec{B}$ forman un **sistema ortonormal positivamente orientado** (regla de la mano derecha) — un sistema de coordenadas que **se mueve con la partícula**, llamado **triedro de Frenet**.\n\n"
              "**Interpretación intuitiva:** un avión en vuelo tiene $\\vec{T}$ apuntando hacia donde va, $\\vec{N}$ hacia el centro de la curva (donde 'tira' la fuerza centrípeta), y $\\vec{B}$ perpendicular a ambos."
          )),

        fig(
            "Triedro de Frenet sobre una hélice. Vista isométrica 3D de una hélice circular trazada "
            "en color teal claro. En un punto P sobre la curva, dibujar tres vectores "
            "perpendiculares saliendo de P: el tangente T (en azul) apuntando en la dirección del "
            "movimiento (a lo largo de la hélice), el normal N (en ámbar) apuntando hacia el eje "
            "central (centro del cilindro), y el binormal B (en verde) perpendicular a ambos. "
            "Etiquetas claras: 'T (tangente)', 'N (normal)', 'B (binormal) = T × N'. Indicar que "
            "los tres son unitarios y mutuamente ortogonales. " + STYLE
        ),

        b("definicion",
          titulo="Planos asociados al triedro",
          body_md=(
              "En cada punto de la curva, los tres vectores definen tres **planos**:\n\n"
              "**Plano osculador** = $\\vec{T}$ + $\\vec{N}$ (normal $\\vec{B}$). Es el plano que mejor 'aproxima' la curva localmente — la curva 'se acuesta' sobre él.\n\n"
              "**Plano normal** = $\\vec{N}$ + $\\vec{B}$ (normal $\\vec{T}$). Perpendicular a la dirección de movimiento.\n\n"
              "**Plano rectificante** = $\\vec{T}$ + $\\vec{B}$ (normal $\\vec{N}$).\n\n"
              "**Curvas planas** (que viven en un plano fijo): el plano osculador **es** ese plano y $\\vec{B}$ es constante. La curva no 'sale' del plano — torsión cero (lección 1.6)."
          )),

        b("ejemplo_resuelto",
          titulo="Triedro de Frenet de una hélice",
          problema_md="Calcular $\\vec{T}, \\vec{N}, \\vec{B}$ para $\\vec{r}(t) = \\langle \\cos t, \\sin t, t \\rangle$.",
          pasos=[
              {"accion_md": "**$\\vec{T}$:** $\\vec{r}'(t) = \\langle -\\sin t, \\cos t, 1 \\rangle$. $\\|\\vec{r}'\\| = \\sqrt{2}$.\n\n"
                            "$\\vec{T}(t) = \\dfrac{1}{\\sqrt{2}} \\langle -\\sin t, \\cos t, 1 \\rangle$.",
               "justificacion_md": "Cálculo directo.",
               "es_resultado": False},
              {"accion_md": "**$\\vec{N}$:** $\\vec{T}'(t) = \\dfrac{1}{\\sqrt{2}} \\langle -\\cos t, -\\sin t, 0 \\rangle$. $\\|\\vec{T}'\\| = \\dfrac{1}{\\sqrt{2}}$.\n\n"
                            "$\\vec{N}(t) = \\dfrac{\\vec{T}'}{\\|\\vec{T}'\\|} = \\langle -\\cos t, -\\sin t, 0 \\rangle$.",
               "justificacion_md": "**$\\vec{N}$ apunta hacia el eje $z$** — el centro del cilindro de la hélice. Tiene sentido geométrico.",
               "es_resultado": False},
              {"accion_md": "**$\\vec{B}$:** $\\vec{T} \\times \\vec{N}$ — calcular el determinante.\n\n"
                            "Después de cálculo: $\\vec{B}(t) = \\dfrac{1}{\\sqrt{2}} \\langle \\sin t, -\\cos t, 1 \\rangle$.",
               "justificacion_md": "**Verificación:** $\\|\\vec{B}\\| = \\dfrac{1}{\\sqrt{2}}\\sqrt{1 + 1} = 1$. ✓",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Por qué este triedro es 'el correcto'?",
          body_md=(
              "Hay infinitas formas de definir un triedro asociado a una curva. ¿Por qué $\\vec{T}, \\vec{N}, \\vec{B}$ son **canónicos**?\n\n"
              "**Respuesta:** se construyen **únicamente desde la curva** (sin elegir un sistema de coordenadas externo). Son **intrínsecos**.\n\n"
              "- $\\vec{T}$ es la dirección del movimiento — la única canónica a lo largo de la curva.\n"
              "- $\\vec{N}$ es la única dirección unitaria perpendicular a $\\vec{T}$ que apunta hacia el lado donde la curva se dobla.\n"
              "- $\\vec{B}$ completa el sistema con orientación positiva.\n\n"
              "**Otras opciones** (como elegir un vector arbitrario perpendicular a $\\vec{T}$) **dependen de coordenadas externas**, y la geometría de la curva no debería depender de eso."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\vec{N}$ está definido como:",
                  "opciones_md": [
                      "$\\vec{r}'(t)/\\|\\vec{r}'(t)\\|$",
                      "$\\vec{T}'(t)/\\|\\vec{T}'(t)\\|$",
                      "$\\vec{r}''(t)/\\|\\vec{r}''(t)\\|$",
                      "$\\vec{T} \\times \\vec{r}$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\vec{N}$ es la derivada del tangente, normalizada.",
                  "explicacion_md": (
                      "$\\vec{N} = \\vec{T}'/\\|\\vec{T}'\\|$. **Atención:** **NO** es $\\vec{r}''/\\|\\vec{r}''\\|$ — eso no es necesariamente perpendicular a $\\vec{T}$."
                  ),
              },
              {
                  "enunciado_md": "Para una recta, $\\vec{N}$ es:",
                  "opciones_md": [
                      "Un vector cualquiera unitario.",
                      "Igual a $\\vec{T}$.",
                      "No está definido (la recta no se dobla).",
                      "Cero.",
                  ],
                  "correcta": "C",
                  "pista_md": "Una recta tiene $\\vec{T}$ constante, así $\\vec{T}' = \\vec{0}$ y $\\vec{N}$ requiere dividir por $0$.",
                  "explicacion_md": (
                      "**$\\vec{N}$ no está definido para rectas.** Es coherente geométricamente: una recta no tiene 'lado cóncavo'."
                  ),
              },
          ]),

        ej(
            titulo="Triedro de un círculo plano",
            enunciado=(
                "Sea $\\vec{r}(t) = \\langle 2\\cos t, 2\\sin t, 0 \\rangle$ (círculo de radio $2$ en el plano $xy$). "
                "Calcula $\\vec{T}, \\vec{N}, \\vec{B}$."
            ),
            pistas=[
                "$\\vec{r}'(t) = \\langle -2\\sin t, 2\\cos t, 0 \\rangle$. $\\|\\vec{r}'\\| = 2$.",
                "$\\vec{N}$ apunta hacia el centro (origen).",
                "$\\vec{B}$ es perpendicular al plano del círculo: $\\pm \\vec{k}$.",
            ],
            solucion=(
                "$\\vec{T}(t) = \\langle -\\sin t, \\cos t, 0 \\rangle$.\n\n"
                "$\\vec{T}'(t) = \\langle -\\cos t, -\\sin t, 0 \\rangle$. $\\|\\vec{T}'\\| = 1$.\n\n"
                "$\\vec{N}(t) = \\langle -\\cos t, -\\sin t, 0 \\rangle$. **Apunta hacia el origen** (centro del círculo). ✓\n\n"
                "$\\vec{B}(t) = \\vec{T} \\times \\vec{N} = \\langle 0, 0, 1 \\rangle = \\vec{k}$ (constante).\n\n"
                "**$\\vec{B}$ constante** confirma que la curva es plana. La torsión es cero (lección 1.6)."
            ),
        ),

        ej(
            titulo="Verificar la ortogonalidad",
            enunciado=(
                "Para la hélice del ejemplo anterior, verifica numéricamente en $t = 0$ que $\\vec{T} \\cdot \\vec{N} = 0$, $\\vec{T} \\cdot \\vec{B} = 0$ y $\\vec{N} \\cdot \\vec{B} = 0$."
            ),
            pistas=[
                "$\\vec{T}(0) = (0, 1, 1)/\\sqrt{2}$, $\\vec{N}(0) = (-1, 0, 0)$, $\\vec{B}(0) = (0, -1, 1)/\\sqrt{2}$.",
            ],
            solucion=(
                "$\\vec{T} \\cdot \\vec{N} = (0)(-1) + (1)(0) + (1)(0) = 0$. ✓\n\n"
                "$\\vec{T} \\cdot \\vec{B} = (1/2)[(0)(0) + (1)(-1) + (1)(1)] = 0$. ✓\n\n"
                "$\\vec{N} \\cdot \\vec{B} = (1/\\sqrt{2})[(-1)(0) + (0)(-1) + (0)(1)] = 0$. ✓\n\n"
                "**Triedro ortonormal confirmado.**"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\vec{T}$ con $\\vec{r}'$.** $\\vec{T}$ es la velocidad **normalizada** (magnitud 1).",
              "**Calcular $\\vec{N}$ como $\\vec{r}''/\\|\\vec{r}''\\|$.** No funciona en general — $\\vec{r}''$ no es perpendicular a $\\vec{T}$ en parametrizaciones no-arco.",
              "**Olvidar el orden $\\vec{T} \\times \\vec{N}$.** $\\vec{N} \\times \\vec{T} = -\\vec{B}$ — apunta al lado opuesto.",
              "**Aplicar a rectas.** $\\vec{T}' = \\vec{0}$ → $\\vec{N}$ no definido.",
              "**Olvidar normalizar.** Tanto $\\vec{T}$ como $\\vec{N}$ requieren dividir por su magnitud.",
          ]),

        b("resumen",
          puntos_md=[
              "**Tangente** $\\vec{T} = \\vec{r}'/\\|\\vec{r}'\\|$ — dirección del movimiento.",
              "**Normal principal** $\\vec{N} = \\vec{T}'/\\|\\vec{T}'\\|$ — perpendicular a $\\vec{T}$, hacia el lado cóncavo.",
              "**Binormal** $\\vec{B} = \\vec{T} \\times \\vec{N}$ — completa el sistema ortonormal.",
              "**Triedro de Frenet:** $\\{\\vec{T}, \\vec{N}, \\vec{B}\\}$ ortonormal positivo.",
              "**Planos:** osculador ($\\vec{T}, \\vec{N}$), normal ($\\vec{N}, \\vec{B}$), rectificante ($\\vec{T}, \\vec{B}$).",
              "**Curvas planas:** $\\vec{B}$ constante; torsión cero.",
              "**Próxima lección:** curvatura $\\kappa$ y torsión $\\tau$ — los dos invariantes que describen completamente una curva.",
          ]),
    ]
    return {
        "id": "lec-vec-1-5-vectores-curvas",
        "title": "Vectores de curvas",
        "description": "Triedro de Frenet $\\vec{T}, \\vec{N}, \\vec{B}$, planos asociados.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 5,
    }


# =====================================================================
# 1.6 Curvatura y torsión
# =====================================================================
def lesson_1_6():
    blocks = [
        b("texto", body_md=(
            "Dos curvas en 3D pueden parecer 'iguales' visualmente pero ser geométricamente distintas. "
            "**¿Qué propiedades intrínsecas distinguen una curva de otra?** Resulta que en cada punto bastan "
            "**dos números:** la **curvatura** $\\kappa$ (cuán fuerte se dobla) y la **torsión** $\\tau$ "
            "(cuánto se sale del plano). Dos curvas con las mismas $\\kappa(s)$ y $\\tau(s)$ son **congruentes** "
            "— se pueden superponer una sobre otra con un movimiento rígido.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Calcular la **curvatura** $\\kappa$ con varias fórmulas.\n"
            "- Calcular la **torsión** $\\tau$.\n"
            "- Interpretar geométricamente ambos números.\n"
            "- Reconocer los casos degenerados (recta, círculo, hélice)."
        )),

        b("definicion",
          titulo="Curvatura",
          body_md=(
              "La **curvatura** mide qué tan rápido cambia la dirección $\\vec{T}$ a medida que avanzamos por la curva.\n\n"
              "**Definición intrínseca** (con parametrización por longitud de arco $s$):\n\n"
              "$$\\kappa(s) = \\left\\|\\dfrac{d\\vec{T}}{ds}\\right\\| = \\|\\vec{T}'(s)\\|$$\n\n"
              "**Fórmula práctica** (parametrización general $\\vec{r}(t)$):\n\n"
              "$$\\kappa(t) = \\dfrac{\\|\\vec{r}'(t) \\times \\vec{r}''(t)\\|}{\\|\\vec{r}'(t)\\|^3}$$\n\n"
              "**Para curvas $y = f(x)$:**\n\n"
              "$$\\kappa(x) = \\dfrac{|f''(x)|}{(1 + [f'(x)]^2)^{3/2}}$$\n\n"
              "**$\\kappa \\geq 0$ siempre** — solo magnitud, no dirección. La dirección la lleva $\\vec{N}$."
          )),

        b("intuicion",
          titulo="Curvatura como inverso del radio del círculo osculador",
          body_md=(
              "**Interpretación geométrica:** en cada punto de la curva, se puede inscribir un **círculo osculador** que mejor aproxima la curva localmente. Su radio $R$ se llama **radio de curvatura** y cumple:\n\n"
              "$$R = \\dfrac{1}{\\kappa}$$\n\n"
              "**Casos límite:**\n\n"
              "- **Recta:** $\\kappa = 0$, $R = \\infty$ (sin curvatura, no se dobla).\n"
              "- **Círculo de radio $R$:** $\\kappa = 1/R$ (constante).\n"
              "- **Curva muy doblada:** $\\kappa$ grande, $R$ pequeño.\n\n"
              "**Lección rápida:** un círculo grande es 'casi recto' localmente; uno pequeño tiene curvatura fuerte. La fórmula $\\kappa = 1/R$ lo formaliza."
          )),

        b("ejemplo_resuelto",
          titulo="Curvatura de un círculo",
          problema_md="Verificar que $\\kappa = 1/R$ para el círculo $\\vec{r}(t) = \\langle R\\cos t, R\\sin t, 0 \\rangle$.",
          pasos=[
              {"accion_md": "$\\vec{r}'(t) = \\langle -R\\sin t, R\\cos t, 0 \\rangle$. $\\|\\vec{r}'\\| = R$.\n\n"
                            "$\\vec{r}''(t) = \\langle -R\\cos t, -R\\sin t, 0 \\rangle$.",
               "justificacion_md": "Estándar.",
               "es_resultado": False},
              {"accion_md": "**Producto cruz:**\n\n"
                            "$\\vec{r}' \\times \\vec{r}'' = \\langle 0, 0, R^2(\\sin^2 t + \\cos^2 t) \\rangle = \\langle 0, 0, R^2 \\rangle$. $\\|\\vec{r}' \\times \\vec{r}''\\| = R^2$.",
               "justificacion_md": "Para curva plana, el producto cruz es perpendicular al plano (eje $z$).",
               "es_resultado": False},
              {"accion_md": "$\\kappa = \\dfrac{R^2}{R^3} = \\dfrac{1}{R}$.",
               "justificacion_md": "**Confirmado:** curvatura inversamente proporcional al radio.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Torsión",
          body_md=(
              "La **torsión** mide qué tan rápido la curva se 'sale' del plano osculador — qué tan rápido cambia $\\vec{B}$.\n\n"
              "**Definición intrínseca:**\n\n"
              "$$\\dfrac{d\\vec{B}}{ds} = -\\tau(s) \\, \\vec{N}(s)$$\n\n"
              "(El signo negativo es convención.) **Equivalente:**\n\n"
              "$$\\tau(s) = -\\dfrac{d\\vec{B}}{ds} \\cdot \\vec{N}$$\n\n"
              "**Fórmula práctica:**\n\n"
              "$$\\tau(t) = \\dfrac{[\\vec{r}'(t) \\times \\vec{r}''(t)] \\cdot \\vec{r}'''(t)}{\\|\\vec{r}'(t) \\times \\vec{r}''(t)\\|^2}$$\n\n"
              "**$\\tau$ puede ser positivo, negativo o cero.** Signo positivo = la curva 'gira' en un sentido; negativo = en el otro (regla de la mano derecha)."
          )),

        b("teorema",
          nombre="Curvas planas tienen torsión cero",
          enunciado_md=(
              "Una curva tiene **torsión $\\tau = 0$ en todo punto** **si y solo si** está contenida en un plano.\n\n"
              "**En palabras:** las curvas planas no se 'salen' de su plano (por definición). Las que sí se salen tienen $\\tau \\neq 0$ en algún punto.\n\n"
              "**Confirmado por:** $\\tau = 0 \\implies \\vec{B}$ constante. Como $\\vec{B} \\perp \\vec{T}, \\vec{N}$ todo el tiempo, y $\\vec{B}$ no cambia, la curva queda confinada al plano de $\\vec{T}, \\vec{N}$."
          )),

        b("ejemplo_resuelto",
          titulo="Curvatura y torsión de la hélice",
          problema_md=(
              "Calcular $\\kappa$ y $\\tau$ para la hélice $\\vec{r}(t) = \\langle a\\cos t, a\\sin t, bt \\rangle$ (radio $a$, paso $b$)."
          ),
          pasos=[
              {"accion_md": "$\\vec{r}'(t) = \\langle -a\\sin t, a\\cos t, b \\rangle$. $\\|\\vec{r}'\\| = \\sqrt{a^2 + b^2}$.\n\n"
                            "$\\vec{r}'' = \\langle -a\\cos t, -a\\sin t, 0 \\rangle$. $\\vec{r}''' = \\langle a\\sin t, -a\\cos t, 0 \\rangle$.",
               "justificacion_md": "Tres derivadas — necesarias para $\\tau$.",
               "es_resultado": False},
              {"accion_md": "**Producto cruz:**\n\n"
                            "$\\vec{r}' \\times \\vec{r}'' = \\langle ab\\sin t, -ab\\cos t, a^2 \\rangle$. $\\|\\vec{r}' \\times \\vec{r}''\\| = a\\sqrt{a^2 + b^2}$.\n\n"
                            "**Curvatura:**\n\n"
                            "$\\kappa = \\dfrac{a\\sqrt{a^2+b^2}}{(a^2+b^2)^{3/2}} = \\dfrac{a}{a^2 + b^2}$.",
               "justificacion_md": "Curvatura **constante** — la hélice se curva igual en todas partes.",
               "es_resultado": False},
              {"accion_md": "**Torsión:**\n\n"
                            "$(\\vec{r}' \\times \\vec{r}'') \\cdot \\vec{r}''' = ab\\sin t \\cdot a\\sin t + (-ab\\cos t)(-a\\cos t) + a^2 \\cdot 0 = a^2 b$.\n\n"
                            "$\\tau = \\dfrac{a^2 b}{a^2(a^2+b^2)} = \\dfrac{b}{a^2+b^2}$.",
               "justificacion_md": "**Torsión también constante**, proporcional al paso $b$.",
               "es_resultado": False},
              {"accion_md": "**Casos límite:**\n\n"
                            "- $b = 0$: hélice colapsa a círculo. $\\kappa = 1/a$, $\\tau = 0$. ✓\n"
                            "- $a = 0$: hélice colapsa a recta vertical. $\\kappa = 0$, $\\tau$ indefinida (división por $0$ en el cruz). ✓",
               "justificacion_md": "**La hélice es la única curva con $\\kappa$ y $\\tau$ ambas constantes y no nulas** (resultado clásico de geometría diferencial).",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para una recta, $\\kappa = ?$",
                  "opciones_md": ["$0$", "$1$", "$\\infty$", "Indefinida"],
                  "correcta": "A",
                  "pista_md": "Una recta no se dobla. $\\vec{T}$ es constante.",
                  "explicacion_md": (
                      "$\\vec{T}$ constante → $\\vec{T}' = \\vec{0}$ → $\\kappa = \\|\\vec{T}'\\| = 0$. **Coherente:** una recta tiene radio de curvatura $\\infty$."
                  ),
              },
              {
                  "enunciado_md": "Si una curva tiene $\\tau = 0$ en todos los puntos, entonces:",
                  "opciones_md": [
                      "Es una recta.",
                      "Es un círculo.",
                      "Es plana (vive en un plano fijo).",
                      "$\\kappa$ también es $0$.",
                  ],
                  "correcta": "C",
                  "pista_md": "Torsión cero significa que la curva no sale de su plano osculador.",
                  "explicacion_md": (
                      "**Curva plana** ⟺ torsión cero. Puede ser cualquier curva plana: círculo, parábola, espiral plana, etc. **No tiene que ser recta ni círculo.**"
                  ),
              },
          ]),

        ej(
            titulo="Curvatura de una parábola",
            enunciado=(
                "Calcula la curvatura de $y = x^2$ en $x = 0$ y en $x = 1$."
            ),
            pistas=[
                "Fórmula: $\\kappa = |f''| / (1 + (f')^2)^{3/2}$.",
                "$f' = 2x$, $f'' = 2$.",
            ],
            solucion=(
                "**En $x = 0$:** $f'(0) = 0$, $\\kappa(0) = \\dfrac{2}{1} = 2$. (Curvatura máxima en el vértice.)\n\n"
                "**En $x = 1$:** $f'(1) = 2$, $\\kappa(1) = \\dfrac{2}{(1 + 4)^{3/2}} = \\dfrac{2}{5\\sqrt{5}} \\approx 0.179$.\n\n"
                "**Lección:** la curvatura **disminuye al alejarse del vértice** — la parábola se vuelve casi recta a la distancia."
            ),
        ),

        ej(
            titulo="Verificar curva plana",
            enunciado=(
                "Sea $\\vec{r}(t) = \\langle t, t^2, 2t + 1 \\rangle$. Demuestra que es una curva plana calculando $\\tau$."
            ),
            pistas=[
                "$\\vec{r}' = (1, 2t, 2), \\vec{r}'' = (0, 2, 0), \\vec{r}''' = (0, 0, 0)$.",
                "$\\tau$ involucra $\\vec{r}''' \\cdot (\\vec{r}' \\times \\vec{r}'')$. Si $\\vec{r}''' = 0$, $\\tau = 0$.",
            ],
            solucion=(
                "$\\vec{r}'''(t) = \\vec{0}$. Por tanto $(\\vec{r}' \\times \\vec{r}'') \\cdot \\vec{r}''' = 0$, y $\\tau = 0$.\n\n"
                "**Curva plana confirmada.** **Verificación:** la curva $(t, t^2, 2t+1)$ vive en el plano $z = 2x + 1$ — sustituye $x = t$ y verifica."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\kappa$ con $|\\vec{r}''|$.** $\\kappa$ involucra **norma del producto cruz**, no segunda derivada directa.",
              "**Olvidar elevar al cubo** $\\|\\vec{r}'\\|$ en el denominador. La fórmula es $\\|\\vec{r}'\\|^3$, no $\\|\\vec{r}'\\|^2$.",
              "**Asumir que $\\kappa \\geq 0$ implica que la curva 'va hacia arriba'.** $\\kappa$ es solo magnitud, no dirección.",
              "**Calcular torsión sin la tercera derivada.** $\\tau$ requiere $\\vec{r}'''$.",
              "**Confundir torsión nula con curvatura nula.** Son cosas distintas: $\\tau = 0$ es plana; $\\kappa = 0$ es recta.",
          ]),

        b("resumen",
          puntos_md=[
              "**Curvatura** $\\kappa = \\|\\vec{r}' \\times \\vec{r}''\\| / \\|\\vec{r}'\\|^3$ — cuán fuerte se dobla.",
              "**Radio de curvatura** $R = 1/\\kappa$.",
              "**Torsión** $\\tau = (\\vec{r}' \\times \\vec{r}'') \\cdot \\vec{r}''' / \\|\\vec{r}' \\times \\vec{r}''\\|^2$ — cuánto sale del plano.",
              "**Curva plana** ⟺ $\\tau = 0$ en todo punto.",
              "**Casos clásicos:** recta ($\\kappa = 0$), círculo ($\\kappa = 1/R, \\tau = 0$), hélice ($\\kappa, \\tau$ constantes no nulas).",
              "**$\\kappa$ y $\\tau$ caracterizan completamente una curva** (salvo movimientos rígidos) — teorema fundamental de las curvas.",
              "**Próxima lección:** Frenet-Serret — el sistema de ecuaciones que conecta todo.",
          ]),
    ]
    return {
        "id": "lec-vec-1-6-curvatura-torsion",
        "title": "Curvatura y torsión",
        "description": "Curvatura $\\kappa$ y torsión $\\tau$, fórmulas prácticas y casos clásicos.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


# =====================================================================
# 1.7 Frenet-Serret
# =====================================================================
def lesson_1_7():
    blocks = [
        b("texto", body_md=(
            "Las **fórmulas de Frenet-Serret** son tres ecuaciones diferenciales que describen cómo "
            "evoluciona el triedro $\\{\\vec{T}, \\vec{N}, \\vec{B}\\}$ a medida que avanzamos por la curva. "
            "Son la **culminación** de la geometría diferencial de curvas en 3D: si conoces $\\kappa(s)$ y "
            "$\\tau(s)$, las fórmulas determinan completamente la curva — el resto es resolver un sistema de EDOs.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Conocer y derivar las **tres fórmulas de Frenet-Serret**.\n"
            "- Reconocer su **forma matricial** (matriz antisimétrica).\n"
            "- Aplicarlas en casos concretos.\n"
            "- Comprender el **teorema fundamental** de las curvas."
        )),

        b("teorema",
          nombre="Fórmulas de Frenet-Serret",
          enunciado_md=(
              "Para una curva en $\\mathbb{R}^3$ parametrizada por longitud de arco $s$, con curvatura $\\kappa(s) > 0$ y torsión $\\tau(s)$:\n\n"
              "$$\\dfrac{d\\vec{T}}{ds} = \\kappa \\, \\vec{N}$$\n\n"
              "$$\\dfrac{d\\vec{N}}{ds} = -\\kappa \\, \\vec{T} + \\tau \\, \\vec{B}$$\n\n"
              "$$\\dfrac{d\\vec{B}}{ds} = -\\tau \\, \\vec{N}$$\n\n"
              "**En forma matricial:**\n\n"
              "$$\\dfrac{d}{ds} \\begin{pmatrix} \\vec{T} \\\\ \\vec{N} \\\\ \\vec{B} \\end{pmatrix} = \\begin{pmatrix} 0 & \\kappa & 0 \\\\ -\\kappa & 0 & \\tau \\\\ 0 & -\\tau & 0 \\end{pmatrix} \\begin{pmatrix} \\vec{T} \\\\ \\vec{N} \\\\ \\vec{B} \\end{pmatrix}$$\n\n"
              "La matriz es **antisimétrica** — propiedad clave."
          ),
          demostracion_md=(
              "**Primera ecuación:** $\\vec{N}(s) = \\vec{T}'(s)/\\|\\vec{T}'(s)\\|$ y $\\kappa = \\|\\vec{T}'\\|$, así $\\vec{T}'(s) = \\kappa \\vec{N}$. ✓\n\n"
              "**Tercera ecuación:** $\\vec{B} = \\vec{T} \\times \\vec{N}$. Derivando: $\\vec{B}' = \\vec{T}' \\times \\vec{N} + \\vec{T} \\times \\vec{N}'$. El primer término es $\\kappa \\vec{N} \\times \\vec{N} = 0$. Como $\\|\\vec{B}\\| = 1$, $\\vec{B}' \\perp \\vec{B}$. Y $\\vec{B}' \\perp \\vec{T}$ (de la fórmula con $\\times$). Por tanto $\\vec{B}' \\parallel \\vec{N}$, así $\\vec{B}' = c \\vec{N}$ para algún $c$. Por convención $c = -\\tau$, definiendo así la torsión.\n\n"
              "**Segunda ecuación:** $\\vec{N} = \\vec{B} \\times \\vec{T}$. Derivando con la regla del producto: $\\vec{N}' = \\vec{B}' \\times \\vec{T} + \\vec{B} \\times \\vec{T}' = (-\\tau \\vec{N}) \\times \\vec{T} + \\vec{B} \\times (\\kappa \\vec{N}) = -\\tau (\\vec{N} \\times \\vec{T}) + \\kappa (\\vec{B} \\times \\vec{N}) = -\\tau (-\\vec{B}) + \\kappa (-\\vec{T}) = \\tau \\vec{B} - \\kappa \\vec{T}$. ✓"
          )),

        b("intuicion",
          titulo="Significado de cada fórmula",
          body_md=(
              "**$\\vec{T}' = \\kappa \\vec{N}$:** la dirección del movimiento cambia hacia la dirección normal, a velocidad proporcional a la curvatura. **Más curvatura = el tangente gira más rápido.**\n\n"
              "**$\\vec{B}' = -\\tau \\vec{N}$:** el binormal cambia hacia $-\\vec{N}$ a velocidad proporcional a la torsión. **Si $\\tau > 0$:** el plano osculador 'rota' en cierto sentido al avanzar; si $\\tau < 0$, en el otro sentido. **Si $\\tau = 0$:** $\\vec{B}$ no cambia — curva plana.\n\n"
              "**$\\vec{N}' = -\\kappa \\vec{T} + \\tau \\vec{B}$:** el normal cambia tanto hacia $-\\vec{T}$ (porque $\\vec{T}$ y $\\vec{N}$ están 'rotando juntos' en el plano osculador) como hacia $\\vec{B}$ (porque el plano osculador mismo está rotando)."
          )),

        b("teorema",
          nombre="Teorema fundamental de las curvas",
          enunciado_md=(
              "Dadas dos funciones $\\kappa: I \\to (0, \\infty)$ y $\\tau: I \\to \\mathbb{R}$ continuas, "
              "**existe una curva** $\\vec{r}: I \\to \\mathbb{R}^3$ parametrizada por longitud de arco con esas $\\kappa(s)$ y $\\tau(s)$. "
              "**Esta curva es única salvo movimientos rígidos** (rotaciones y traslaciones) de $\\mathbb{R}^3$.\n\n"
              "**En palabras:** la geometría intrínseca de una curva 3D queda completamente determinada por su curvatura y torsión como funciones de la longitud de arco.\n\n"
              "**Es el análogo en cálculo vectorial del** *teorema fundamental* de geometría euclidiana: dos triángulos con los mismos lados son congruentes. Aquí: dos curvas con las mismas $\\kappa(s), \\tau(s)$ son congruentes.\n\n"
              "**Aplicación:** las fórmulas de Frenet-Serret son un sistema de EDOs que se puede integrar para reconstruir la curva."
          )),

        b("ejemplo_resuelto",
          titulo="Verificar Frenet-Serret en la hélice",
          problema_md="Para la hélice $\\vec{r}(t) = \\langle a\\cos t, a\\sin t, bt \\rangle$ con $\\kappa = a/(a^2+b^2)$, $\\tau = b/(a^2+b^2)$, verifica la primera fórmula.",
          pasos=[
              {"accion_md": "**De la lección 1.5:** $\\vec{T}(t) = \\dfrac{1}{\\sqrt{a^2+b^2}}\\langle -a\\sin t, a\\cos t, b \\rangle$.\n\n"
                            "$\\vec{N}(t) = \\langle -\\cos t, -\\sin t, 0 \\rangle$.",
               "justificacion_md": "Recordatorio.",
               "es_resultado": False},
              {"accion_md": "**$d\\vec{T}/dt$:** $\\dfrac{1}{\\sqrt{a^2+b^2}} \\langle -a\\cos t, -a\\sin t, 0 \\rangle = \\dfrac{a}{\\sqrt{a^2+b^2}} \\vec{N}$.",
               "justificacion_md": "Comparar con $\\vec{N}$.",
               "es_resultado": False},
              {"accion_md": "**Convertir a derivada respecto de $s$:** $\\dfrac{d\\vec{T}}{ds} = \\dfrac{d\\vec{T}/dt}{ds/dt} = \\dfrac{1}{\\sqrt{a^2+b^2}} \\cdot \\dfrac{a}{\\sqrt{a^2+b^2}} \\vec{N} = \\dfrac{a}{a^2+b^2} \\vec{N} = \\kappa \\vec{N}$. ✓",
               "justificacion_md": "**Frenet-Serret confirmado.** Las otras dos se verifican análogamente.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Por qué la matriz es antisimétrica",
          body_md=(
              "La matriz de Frenet-Serret es **antisimétrica** ($A^T = -A$). **No es coincidencia:** es porque $\\{\\vec{T}, \\vec{N}, \\vec{B}\\}$ es una **base ortonormal** que evoluciona en el tiempo.\n\n"
              "Hecho general: cualquier transformación que preserve la ortonormalidad (rotación 'rígida') está generada por una matriz antisimétrica. Las matrices antisimétricas son los **generadores infinitesimales de rotaciones**.\n\n"
              "**Lectura física:** el triedro de Frenet **rota como un cuerpo rígido** a medida que avanzamos por la curva. La matriz antisimétrica codifica el **vector de velocidad angular** de esa rotación. En 3D ese vector se llama **vector de Darboux**:\n\n"
              "$$\\vec{\\omega} = \\tau \\vec{T} + \\kappa \\vec{B}$$\n\n"
              "Y las fórmulas de Frenet-Serret son simplemente $\\vec{X}' = \\vec{\\omega} \\times \\vec{X}$ para $\\vec{X} = \\vec{T}, \\vec{N}, \\vec{B}$."
          )),

        b("verificacion",
          intro_md="Verifica las fórmulas:",
          preguntas=[
              {
                  "enunciado_md": "$d\\vec{T}/ds = ?$",
                  "opciones_md": [
                      "$\\kappa \\vec{T}$",
                      "$\\kappa \\vec{N}$",
                      "$\\tau \\vec{B}$",
                      "$-\\kappa \\vec{T} + \\tau \\vec{B}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Primera fórmula de Frenet-Serret.",
                  "explicacion_md": (
                      "$d\\vec{T}/ds = \\kappa \\vec{N}$. Es la definición misma del normal y la curvatura."
                  ),
              },
              {
                  "enunciado_md": "Si una curva tiene $\\kappa$ y $\\tau$ ambas constantes no nulas, ¿qué tipo de curva es?",
                  "opciones_md": [
                      "Recta",
                      "Círculo",
                      "Hélice circular",
                      "Cualquier curva",
                  ],
                  "correcta": "C",
                  "pista_md": "Es la única curva con esa propiedad (caracterización del teorema fundamental).",
                  "explicacion_md": (
                      "**$\\kappa, \\tau$ constantes no nulas** caracterizan completamente la **hélice circular**. Es la única curva con esa firma."
                  ),
              },
          ]),

        ej(
            titulo="Reconstruir una curva desde $\\kappa, \\tau$",
            enunciado=(
                "Una curva tiene $\\kappa = 1$ (constante) y $\\tau = 0$ en parametrización por arco. "
                "Identifica el tipo de curva y describe su geometría."
            ),
            pistas=[
                "$\\tau = 0 \\implies$ curva plana.",
                "$\\kappa = 1$ constante en una curva plana → ¿qué curva?",
                "Radio de curvatura $R = 1/\\kappa = 1$.",
            ],
            solucion=(
                "**Curva plana** ($\\tau = 0$) con **curvatura constante $\\kappa = 1$** = **círculo de radio $R = 1$**.\n\n"
                "Por el teorema fundamental, esta curva es única (salvo movimientos rígidos): cualquier movimiento la lleva a $\\vec{r}(s) = \\langle \\cos s, \\sin s, 0 \\rangle + \\vec{c}$ para alguna constante."
            ),
        ),

        ej(
            titulo="Vector de Darboux",
            enunciado=(
                "Para la hélice del ejemplo anterior con $a = b = 1$ ($\\kappa = \\tau = 1/2$), calcula el vector de Darboux $\\vec{\\omega} = \\tau \\vec{T} + \\kappa \\vec{B}$."
            ),
            pistas=[
                "$\\tau = \\kappa = 1/2$.",
                "Sustituye $\\vec{T}$ y $\\vec{B}$ que vimos antes.",
            ],
            solucion=(
                "$\\vec{\\omega} = \\dfrac{1}{2} \\vec{T} + \\dfrac{1}{2} \\vec{B}$. Sustituyendo (con $a = b = 1, t = $ general):\n\n"
                "$\\vec{T} = \\dfrac{1}{\\sqrt{2}}(-\\sin t, \\cos t, 1)$, $\\vec{B} = \\dfrac{1}{\\sqrt{2}}(\\sin t, -\\cos t, 1)$.\n\n"
                "$\\vec{\\omega} = \\dfrac{1}{2\\sqrt{2}}[(-\\sin t + \\sin t, \\cos t - \\cos t, 1 + 1)] = \\dfrac{1}{\\sqrt{2}}(0, 0, 1) = \\dfrac{1}{\\sqrt{2}} \\vec{k}$.\n\n"
                "**Constante en dirección $\\vec{k}$** — el triedro rota alrededor del eje $z$, lo cual tiene sentido geométrico para una hélice."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el signo $-$** en las fórmulas. $\\vec{N}' = -\\kappa \\vec{T} + \\tau \\vec{B}$, no $\\kappa \\vec{T} + \\tau \\vec{B}$.",
              "**Aplicar las fórmulas con parametrización general** sin convertir a $s$. Las fórmulas son **respecto a $s$** — para un parámetro general $t$, hay que multiplicar por $ds/dt = \\|\\vec{r}'(t)\\|$.",
              "**Confundir matriz antisimétrica con simétrica.** Antisimétrica significa $A^T = -A$, los elementos diagonales son $0$.",
              "**Pensar que $\\kappa$ y $\\tau$ deben ser constantes.** En general son funciones de $s$ — pueden variar a lo largo de la curva.",
              "**Asumir que el teorema fundamental da fórmulas explícitas.** El teorema garantiza existencia y unicidad, pero la reconstrucción explícita requiere resolver EDOs (a veces no elementales).",
          ]),

        b("resumen",
          puntos_md=[
              "**Fórmulas de Frenet-Serret** (parametrización por arco $s$):",
              "$\\vec{T}' = \\kappa \\vec{N}$",
              "$\\vec{N}' = -\\kappa \\vec{T} + \\tau \\vec{B}$",
              "$\\vec{B}' = -\\tau \\vec{N}$",
              "**Forma matricial:** matriz antisimétrica — generador de rotaciones.",
              "**Vector de Darboux:** $\\vec{\\omega} = \\tau\\vec{T} + \\kappa\\vec{B}$ — velocidad angular del triedro.",
              "**Teorema fundamental:** $\\kappa(s), \\tau(s)$ determinan la curva (salvo movimientos rígidos).",
              "**Casos clásicos identificados por $\\kappa, \\tau$:** recta ($\\kappa = 0$), círculo ($\\kappa = $ const, $\\tau = 0$), hélice ($\\kappa, \\tau$ ambos const no nulos).",
              "**Cierre del capítulo:** las curvas en 3D quedan completamente descritas por estas dos funciones escalares.",
          ]),
    ]
    return {
        "id": "lec-vec-1-7-frenet-serret",
        "title": "Frenet-Serret",
        "description": "Las tres fórmulas de Frenet-Serret, matriz antisimétrica y teorema fundamental de las curvas.",
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

    course_doc = {
        "id": course_id,
        "title": "Cálculo Vectorial",
        "description": "Curvas en el espacio, integrales de línea, integrales de superficie y los teoremas fundamentales (Green, Stokes, divergencia).",
        "category": "Matemáticas",
        "level": "Avanzado",
        "modules_count": 3,
        "rating": 4.8,
        "summary": "Curso completo de cálculo vectorial para alumnos universitarios chilenos.",
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

    chapter_id = "ch-curvas"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Curvas",
        "description": "Curvas paramétricas, polares, funciones vectoriales, longitud de arco, triedro de Frenet, curvatura, torsión.",
        "order": 1,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_1_1, lesson_1_2, lesson_1_3, lesson_1_4, lesson_1_5, lesson_1_6, lesson_1_7]
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
    print(f"✅ Capítulo 1 — Curvas listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
