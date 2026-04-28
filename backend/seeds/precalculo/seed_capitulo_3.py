"""
Seed del curso Precálculo — Capítulo 3: Funciones Polinomiales y Racionales.

Crea el capítulo 'Funciones Polinomiales y Racionales' bajo el curso 'precalculo'
y siembra sus 4 lecciones:

  - Función cuadrática
  - Funciones polinomiales
  - División de polinomios
  - Funciones racionales

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
# Función cuadrática
# =====================================================================
def lesson_funcion_cuadratica():
    blocks = [
        b("texto", body_md=(
            "Una **función cuadrática** es una función polinomial de **grado 2**:\n\n"
            "$$f(x) = a x^2 + b x + c, \\qquad a \\neq 0.$$\n\n"
            "Su gráfica es siempre una **parábola** — la primera curva no lineal que estudiamos en "
            "detalle. Aparece por todos lados en física, ingeniería, economía:\n\n"
            "- **Trayectorias balísticas:** un proyectil sigue una parábola (sin fricción).\n"
            "- **Maximización/minimización:** áreas con perímetro fijo, beneficios, costos.\n"
            "- **Antenas y reflectores:** sus secciones transversales son parábolas (foco de luz/sonido).\n\n"
            "**Al terminar:**\n\n"
            "- Conocés la **forma estándar** y la **forma vértice** de una cuadrática.\n"
            "- Encontrás el **vértice** completando cuadrados o usando $x_v = -b/(2a)$.\n"
            "- Aplicás el **discriminante** para clasificar las raíces.\n"
            "- Graficás una parábola identificando vértice, eje, intersecciones y concavidad."
        )),

        b("definicion",
          titulo="Forma estándar y forma vértice",
          body_md=(
              "**Forma estándar:**\n\n"
              "$$f(x) = a x^2 + b x + c, \\qquad a \\neq 0.$$\n\n"
              "**Forma vértice (o canónica):**\n\n"
              "$$f(x) = a(x - h)^2 + k,$$\n\n"
              "donde $(h, k)$ es el **vértice** de la parábola y $x = h$ su **eje de simetría**.\n\n"
              "**Conexión entre ambas:**\n\n"
              "$$h = -\\dfrac{b}{2 a}, \\qquad k = f(h) = c - \\dfrac{b^2}{4 a}.$$\n\n"
              "**Cómo obtener forma vértice (completando cuadrados):**\n\n"
              "1. Factorizar el coeficiente $a$ del término $x^2$ y $x$ (no del constante): $a(x^2 + (b/a) x) + c$.\n"
              "2. Sumar y restar $(b/(2 a))^2$ adentro del paréntesis para completar el cuadrado.\n"
              "3. Reescribir como $a(x - h)^2 + k$ y simplificar.\n\n"
              "**Concavidad y vértice:**\n\n"
              "- $a > 0$: parábola **abre hacia arriba**, vértice es **mínimo**.\n"
              "- $a < 0$: parábola **abre hacia abajo**, vértice es **máximo**."
          )),

        b("ejemplo_resuelto",
          titulo="A forma vértice por completación",
          problema_md="Lleva $f(x) = x^2 - 4 x + 3$ a forma vértice y describe la parábola.",
          pasos=[
              {"accion_md": (
                  "**Completar cuadrados.** Tomar $x^2 - 4 x$. La mitad de $-4$ es $-2$, su cuadrado es $4$.\n\n"
                  "$x^2 - 4 x = (x^2 - 4 x + 4) - 4 = (x - 2)^2 - 4$.\n\n"
                  "Reincorporando el $+ 3$: $f(x) = (x - 2)^2 - 4 + 3 = (x - 2)^2 - 1$."
              ),
               "justificacion_md": "Sumar y restar el término que completa el cuadrado.",
               "es_resultado": False},
              {"accion_md": (
                  "**Lectura.** $h = 2$, $k = -1$. **Vértice:** $(2, -1)$. **Eje:** $x = 2$.\n\n"
                  "$a = 1 > 0$: abre hacia arriba, vértice es mínimo. **Rango:** $[-1, +\\infty)$.\n\n"
                  "**Ceros:** $(x - 2)^2 = 1 \\Rightarrow x - 2 = \\pm 1 \\Rightarrow x = 1, 3$."
              ),
               "justificacion_md": "Toda la información sale de la forma vértice de un vistazo.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Discriminante y ceros",
            body=(
                "Para $f(x) = a x^2 + b x + c$, los **ceros** son las soluciones de $f(x) = 0$.\n\n"
                "**Fórmula cuadrática:** $x = \\dfrac{-b \\pm \\sqrt{b^2 - 4 a c}}{2 a}$.\n\n"
                "El **discriminante** $\\Delta = b^2 - 4 a c$ clasifica los ceros:\n\n"
                "- $\\Delta > 0$: **dos ceros reales distintos** → la parábola **corta el eje $x$ dos veces**.\n"
                "- $\\Delta = 0$: **un cero real (doble)** → la parábola es **tangente al eje $x$** en el vértice.\n"
                "- $\\Delta < 0$: **dos ceros complejos** (no reales) → la parábola **no toca el eje $x$**.\n\n"
                "**Conexión con concavidad:** si $a > 0$ y $\\Delta < 0$, toda la parábola está **arriba** del eje; "
                "si $a < 0$ y $\\Delta < 0$, toda **abajo**. Esto sirve para resolver inecuaciones cuadráticas en una mirada."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Cuadrática con vértice y ceros",
          problema_md="Estudia $f(x) = -2 x^2 + 8 x - 6$: vértice, ceros, concavidad y rango.",
          pasos=[
              {"accion_md": (
                  "**Vértice por fórmula.** $x_v = -b/(2 a) = -8/(-4) = 2$. $y_v = f(2) = -2 \\cdot 4 + 16 - 6 = 2$. **Vértice:** $(2, 2)$.\n\n"
                  "$a = -2 < 0$: abre **hacia abajo**, vértice es **máximo**."
              ),
               "justificacion_md": "Más rápido que completar cuadrados cuando solo se quiere el vértice.",
               "es_resultado": False},
              {"accion_md": (
                  "**Discriminante.** $\\Delta = 64 - 4 \\cdot (-2) \\cdot (-6) = 64 - 48 = 16 > 0$. **Dos raíces reales.**\n\n"
                  "$x = \\dfrac{-8 \\pm 4}{-4}$, así $x_1 = \\dfrac{-4}{-4} = 1$, $x_2 = \\dfrac{-12}{-4} = 3$. **Ceros:** $x = 1, 3$."
              ),
               "justificacion_md": "Cuidar los signos al aplicar la fórmula con $a$ negativo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Rango.** Como abre hacia abajo y máximo es $2$: $\\operatorname{Ran}(f) = (-\\infty, 2]$.\n\n"
                  "**Forma vértice (verificación):** $f(x) = -2(x - 2)^2 + 2$."
              ),
               "justificacion_md": "Todos los datos coherentes.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué el vértice está en $x = -b/(2a)$.** Por simetría: las dos raíces son $\\dfrac{-b \\pm \\sqrt{\\Delta}}{2a}$. "
            "Su **promedio** (que es el centro entre ambas) es $\\dfrac{-b}{2 a}$. Y el centro de la parábola es justamente el vértice — el eje de simetría pasa por ahí.\n\n"
            "**Aplicación: optimización.** ¿Qué número $x$ maximiza el producto $x(20 - x)$? Eso es "
            "$f(x) = -x^2 + 20 x$, parábola hacia abajo. Vértice en $x = -20/(-2) = 10$. **Respuesta:** "
            "$x = 10, y = 100$. Ese problema corresponde a 'partir 20 en dos partes que multiplicadas den máximo' — la solución es 10 y 10.\n\n"
            "**Aplicación: tiro parabólico.** Un proyectil con altura $h(t) = -5 t^2 + v_0 t$ alcanza altura "
            "máxima en $t = v_0 / 10$ (vértice). Lo mismo para distancia, alcance, etc."
        )),

        fig(
            "Tres parábolas en un plano cartesiano para mostrar los casos del discriminante. "
            "Parábola izquierda Δ > 0 en color teal #06b6d4, abre hacia arriba con vértice abajo del eje x, cortando dos veces. "
            "Parábola central Δ = 0 en color ámbar #f59e0b, tangente al eje x con vértice en el eje. "
            "Parábola derecha Δ < 0 en color púrpura, completamente arriba del eje x sin tocarlo. "
            "Cada parábola etiquetada con su valor de Δ. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El vértice de $f(x) = 2 x^2 - 8 x + 5$ es:",
                  "opciones_md": [
                      "$(2, 5)$",
                      "$(-2, -3)$",
                      "**$(2, -3)$**",
                      "$(4, 5)$",
                  ],
                  "correcta": "C",
                  "pista_md": "$x_v = -b/(2 a) = 8/4 = 2$; calcular $f(2)$.",
                  "explicacion_md": "$f(2) = 8 - 16 + 5 = -3$. Vértice $(2, -3)$.",
              },
              {
                  "enunciado_md": "Si $a < 0$, la parábola:",
                  "opciones_md": [
                      "Abre hacia arriba, vértice es mínimo",
                      "**Abre hacia abajo, vértice es máximo**",
                      "Es una recta",
                      "No tiene vértice",
                  ],
                  "correcta": "B",
                  "pista_md": "Signo de $a$ controla la concavidad.",
                  "explicacion_md": "Hacia abajo, máximo en el vértice.",
              },
              {
                  "enunciado_md": "Si $\\Delta < 0$, la parábola:",
                  "opciones_md": [
                      "Corta el eje $x$ dos veces",
                      "Es tangente al eje $x$",
                      "**No corta el eje $x$**",
                      "Tiene infinitos ceros",
                  ],
                  "correcta": "C",
                  "pista_md": "Sin raíces reales = no toca el eje.",
                  "explicacion_md": "Las raíces son complejas; gráficamente la parábola está toda arriba o toda abajo.",
              },
          ]),

        ej(
            "Forma vértice",
            "Lleva $f(x) = 3 x^2 + 12 x + 7$ a forma vértice.",
            ["Factorizar 3 antes de completar."],
            (
                "$3(x^2 + 4 x) + 7 = 3((x + 2)^2 - 4) + 7 = 3(x + 2)^2 - 12 + 7 = 3(x + 2)^2 - 5$. Vértice $(-2, -5)$."
            ),
        ),

        ej(
            "Optimización",
            "Un agricultor quiere cercar un terreno rectangular contra un río (no necesita cerca de ese lado). Tiene 100 m de cerca. Halla las dimensiones que maximizan el área.",
            ["Área $A(x) = x(100 - 2 x)$ donde $x$ es el ancho (lados perpendiculares al río)."],
            (
                "$A(x) = -2 x^2 + 100 x$. Vértice en $x = -100/(-4) = 25$. **Dimensiones:** $25$ m × $50$ m. **Área máxima:** $1250$ m²."
            ),
        ),

        ej(
            "Tiro vertical",
            "Una pelota se lanza con $h(t) = -5 t^2 + 30 t + 2$ (metros, segundos). ¿Altura máxima y cuándo?",
            ["Vértice de la parábola."],
            (
                "$t_v = -30/(-10) = 3$ s. $h(3) = -45 + 90 + 2 = 47$ m. **Altura máxima 47 m a los 3 s.**"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar factorizar $a$ al completar cuadrados** cuando $a \\neq 1$.",
              "**Equivocar el signo de $h$** en $f(x) = a(x - h)^2 + k$. $(x + 3)^2$ corresponde a $h = -3$.",
              "**Confundir vértice con intersección con eje $y$.** El vértice está en $x = -b/(2 a)$, no en $x = 0$.",
              "**Aplicar la fórmula cuadrática con $\\Delta < 0$** sin reconocer que no hay raíces reales (en este curso).",
              "**Pensar que toda parábola tiene ceros.** Si $\\Delta < 0$ no corta el eje $x$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma estándar:** $a x^2 + b x + c$. **Forma vértice:** $a(x - h)^2 + k$.",
              "**Vértice:** $h = -b/(2 a)$, $k = f(h)$. Eje de simetría $x = h$.",
              "**Concavidad:** $a > 0$ hacia arriba (mínimo); $a < 0$ hacia abajo (máximo).",
              "**Discriminante** $\\Delta = b^2 - 4 a c$: $> 0$ dos ceros; $= 0$ uno doble; $< 0$ ninguno real.",
              "**Aplicaciones:** optimización, trayectorias parabólicas.",
              "**Próxima lección:** generalización a polinomios de cualquier grado.",
          ]),
    ]
    return {
        "id": "lec-prec-3-1-funcion-cuadratica",
        "title": "Función cuadrática",
        "description": "Función cuadrática f(x) = ax² + bx + c: forma estándar y forma vértice, completación de cuadrados, vértice y eje de simetría, discriminante, ceros y aplicaciones a optimización.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# Funciones polinomiales
# =====================================================================
def lesson_funciones_polinomiales():
    blocks = [
        b("texto", body_md=(
            "Las **funciones polinomiales** generalizan las cuadráticas a cualquier grado. Son funciones "
            "con la forma\n\n"
            "$$P(x) = a_n x^n + a_{n - 1} x^{n - 1} + \\cdots + a_1 x + a_0,$$\n\n"
            "con $a_n \\neq 0$. El número $n$ es el **grado** del polinomio.\n\n"
            "Son **continuas** (sin saltos), **suaves** (sin picos) y tienen **dominio $\\mathbb{R}$**. Su "
            "gráfica está totalmente determinada por **dos cosas**: el **end behavior** (qué hace en "
            "$\\pm \\infty$) y los **ceros** (con sus multiplicidades).\n\n"
            "**Al terminar:**\n\n"
            "- Reconocés grado, coeficiente principal, término constante.\n"
            "- Determinás el **comportamiento al infinito** según grado y coeficiente principal.\n"
            "- Calculás los **ceros** y entendés el efecto de la **multiplicidad** en la gráfica.\n"
            "- Esbozás la gráfica de un polinomio sin tabla de valores."
        )),

        b("definicion",
          titulo="Función polinomial",
          body_md=(
              "Una **función polinomial** es\n\n"
              "$$P(x) = a_n x^n + a_{n - 1} x^{n - 1} + \\cdots + a_1 x + a_0,$$\n\n"
              "con $a_n \\neq 0$ y $n \\in \\mathbb{N} \\cup \\{0\\}$. Aquí:\n\n"
              "- $n$ es el **grado** del polinomio.\n"
              "- $a_n$ es el **coeficiente principal**.\n"
              "- $a_n x^n$ es el **término principal**.\n"
              "- $a_0$ es el **término constante** (= $P(0)$, intersección con eje $y$).\n\n"
              "**Casos clásicos por grado:**\n\n"
              "- Grado 0: $P(x) = c$ (constante).\n"
              "- Grado 1: $P(x) = m x + b$ (lineal).\n"
              "- Grado 2: $a x^2 + b x + c$ (cuadrática — lección anterior).\n"
              "- Grado 3: cúbica.\n"
              "- Grado 4: cuártica, etc."
          )),

        b("definicion",
          titulo="Ceros y multiplicidad",
          body_md=(
              "Un **cero** (o raíz) de $P$ es un valor $c$ tal que $P(c) = 0$. Geométricamente, los ceros "
              "son las intersecciones de la gráfica con el eje $x$.\n\n"
              "**Multiplicidad.** Si $(x - c)^m$ divide a $P(x)$ pero $(x - c)^{m + 1}$ no, decimos que $c$ "
              "es cero de **multiplicidad $m$**.\n\n"
              "Equivalentemente, factorizando $P$ completamente en factores lineales y cuadráticos "
              "irreducibles:\n\n"
              "$$P(x) = a_n (x - c_1)^{m_1} (x - c_2)^{m_2} \\cdots (x - c_k)^{m_k} \\cdot Q(x),$$\n\n"
              "donde $Q$ es producto de cuadráticos irreducibles (raíces complejas). Los $m_i$ son las multiplicidades.\n\n"
              "**Efecto de la multiplicidad en la gráfica:**\n\n"
              "- **Multiplicidad impar** (1, 3, 5, ...): la gráfica **cruza** el eje $x$ en $c$ (cambia de signo).\n"
              "- **Multiplicidad par** (2, 4, 6, ...): la gráfica **rebota** en el eje $x$ en $c$ (no cambia de signo).\n\n"
              "**Multiplicidad alta = más 'aplastado'.** A mayor multiplicidad, la curva se 'achata' más cerca del eje en $c$."
          )),

        formulas(
            titulo="Comportamiento al infinito (end behavior)",
            body=(
                "El comportamiento de $P(x)$ cuando $x \\to \\pm \\infty$ está dominado por el **término principal** $a_n x^n$:\n\n"
                "| Grado $n$ | Coef. principal $a_n$ | $x \\to +\\infty$ | $x \\to -\\infty$ |\n"
                "|---|---|---|---|\n"
                "| Par | $> 0$ | $+\\infty$ | $+\\infty$ |\n"
                "| Par | $< 0$ | $-\\infty$ | $-\\infty$ |\n"
                "| Impar | $> 0$ | $+\\infty$ | $-\\infty$ |\n"
                "| Impar | $< 0$ | $-\\infty$ | $+\\infty$ |\n\n"
                "**Mnemotecnia visual:**\n\n"
                "- Grado **par + $a_n > 0$**: forma de **U** (sube por ambos lados).\n"
                "- Grado **par + $a_n < 0$**: forma de **U invertida** (baja por ambos lados).\n"
                "- Grado **impar + $a_n > 0$**: sube por la **derecha**, baja por la **izquierda**.\n"
                "- Grado **impar + $a_n < 0$**: baja por la derecha, sube por la izquierda.\n\n"
                "**Cantidad de extremos locales.** Un polinomio de grado $n$ tiene **a lo sumo $n - 1$ extremos locales** (máximos y mínimos relativos)."
            ),
        ),

        b("definicion",
          titulo="Teoremas clave",
          body_md=(
              "**Teorema fundamental del álgebra.** Todo polinomio de grado $n \\geq 1$ tiene **exactamente $n$ raíces complejas** (contando multiplicidades).\n\n"
              "**Consecuencia.** Sobre los **reales** un polinomio de grado $n$ tiene **a lo sumo $n$** raíces reales. Las que faltan son complejas conjugadas (siempre vienen en pares).\n\n"
              "**Teorema del valor intermedio (versión polinomios).** Si $P$ es polinomial y $P(a)$ y $P(b)$ tienen **signos opuestos**, entonces $P$ tiene al menos un cero en $(a, b)$.\n\n"
              "Este último resultado es la base de los **métodos numéricos** para encontrar raíces (bisección)."
          )),

        b("ejemplo_resuelto",
          titulo="Esbozar gráfica",
          problema_md="Esboza la gráfica de $P(x) = x^3 - 2 x^2 - 3 x = x(x - 3)(x + 1)$.",
          pasos=[
              {"accion_md": (
                  "**Ceros (ya factorizado):** $x = -1, 0, 3$. Todos de multiplicidad $1$ → la gráfica **cruza** el eje en cada uno."
              ),
               "justificacion_md": "Multiplicidades impares = cruce.",
               "es_resultado": False},
              {"accion_md": (
                  "**End behavior:** grado $3$ (impar), $a_3 = 1 > 0$. \n\n"
                  "$x \\to +\\infty$: $P \\to +\\infty$. $x \\to -\\infty$: $P \\to -\\infty$."
              ),
               "justificacion_md": "Forma típica de cúbica creciente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Análisis de signo** en intervalos definidos por los ceros:\n\n"
                  "| Intervalo | $x$ | $x - 3$ | $x + 1$ | $P$ |\n"
                  "|---|---|---|---|---|\n"
                  "| $x < -1$ | − | − | − | **−** |\n"
                  "| $-1 < x < 0$ | − | − | + | **+** |\n"
                  "| $0 < x < 3$ | + | − | + | **−** |\n"
                  "| $x > 3$ | + | + | + | **+** |"
              ),
               "justificacion_md": "Signo de $P$ en cada intervalo coincide con el del producto de factores.",
               "es_resultado": False},
              {"accion_md": (
                  "**Esbozo.** Viene de $-\\infty$ por la izquierda, sube cruzando $x = -1$, alcanza máximo local entre $-1$ y $0$, baja cruzando $0$, sigue bajando hasta mínimo local entre $0$ y $3$, sube cruzando $3$ y va a $+\\infty$.\n\n"
                  "Forma característica de cúbica con tres ceros."
              ),
               "justificacion_md": "Hay 2 extremos locales (= $n - 1 = 2$, máximo posible para cúbica).",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué el término principal domina al infinito.** Si $P(x) = 3 x^4 - 100 x^3 + \\ldots$, "
            "para $x = 10^6$: $3 x^4 = 3 \\cdot 10^{24}$ pero $-100 x^3 = -100 \\cdot 10^{18} = -10^{20}$. "
            "El primer término es **6 órdenes de magnitud** mayor. Cualquier polinomio de menor grado se "
            "vuelve insignificante para $x$ grande.\n\n"
            "**Multiplicidad geométricamente.** En $P(x) = (x - 1)^2 (x - 3)$, en $x = 1$ la gráfica **toca** "
            "el eje (rebote), en $x = 3$ lo **cruza**. El factor $(x - 1)^2$ es siempre $\\geq 0$, así "
            "$P(x)$ tiene el mismo signo que $(x - 3)$ cerca de $x = 1$. Por eso no cambia de signo.\n\n"
            "**Estrategia para esbozar.** Combinar end behavior (qué hace en los extremos) + ceros (puntos de cruce/rebote) + análisis de signo en intervalos. Eso es **suficiente** para una gráfica cualitativa."
        )),

        fig(
            "Cuatro polinomios prototípicos en cuatro paneles 2x2 mostrando todas las combinaciones de end behavior. "
            "Panel superior izq: cuártica grado par positiva, forma de W (dos U), color teal #06b6d4. "
            "Panel superior der: cuártica grado par negativa, forma de M invertida, color ámbar #f59e0b. "
            "Panel inferior izq: cúbica grado impar positiva, sube por derecha y baja por izquierda. "
            "Panel inferior der: cúbica grado impar negativa, opuesta. "
            "Cada panel etiquetado con su forma y signo del coeficiente principal. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $P(x) = -2 x^4 + x^3 - 5$, el end behavior es:",
                  "opciones_md": [
                      "$+\\infty$ por ambos lados",
                      "**$-\\infty$ por ambos lados**",
                      "$+\\infty$ derecha, $-\\infty$ izquierda",
                      "Constante",
                  ],
                  "correcta": "B",
                  "pista_md": "Grado par, $a_n < 0$.",
                  "explicacion_md": "U invertida (forma M sin extremos absolutos).",
              },
              {
                  "enunciado_md": "En $P(x) = (x - 2)^3 (x + 1)$, en $x = 2$ la gráfica:",
                  "opciones_md": [
                      "Rebota sin cruzar",
                      "**Cruza el eje (multiplicidad impar)**",
                      "Toca pero no llega a 0",
                      "Tiene asíntota",
                  ],
                  "correcta": "B",
                  "pista_md": "Multiplicidad 3 (impar) → cruce.",
                  "explicacion_md": "La gráfica cruza con un 'aplastamiento' por la potencia 3.",
              },
              {
                  "enunciado_md": "Un polinomio de grado 5 tiene como máximo:",
                  "opciones_md": [
                      "5 extremos locales",
                      "**4 extremos locales**",
                      "5 ceros complejos",
                      "Ninguno",
                  ],
                  "correcta": "B",
                  "pista_md": "$n - 1$ extremos.",
                  "explicacion_md": "5 raíces complejas (TFA) y máximo 4 extremos locales.",
              },
          ]),

        ej(
            "Ceros y multiplicidad",
            "Halla los ceros y sus multiplicidades de $P(x) = x^4 - 4 x^3 + 4 x^2$.",
            ["Factor común y trinomio cuadrado perfecto."],
            (
                "$P(x) = x^2(x^2 - 4 x + 4) = x^2 (x - 2)^2$. **Ceros:** $x = 0$ multiplicidad 2 (rebota), $x = 2$ multiplicidad 2 (rebota). Polinomio siempre $\\geq 0$."
            ),
        ),

        ej(
            "End behavior",
            "Describe el end behavior de $P(x) = -x^5 + 3 x^2 + 1$.",
            ["Mira solo el término principal."],
            (
                "Grado 5 (impar), $a_5 = -1 < 0$. $x \\to +\\infty$: $P \\to -\\infty$. $x \\to -\\infty$: $P \\to +\\infty$."
            ),
        ),

        ej(
            "Localizar un cero",
            "Demuestra que $P(x) = x^3 - x - 1$ tiene un cero en $(1, 2)$.",
            ["Teorema del valor intermedio."],
            (
                "$P(1) = -1 < 0$, $P(2) = 8 - 2 - 1 = 5 > 0$. Como $P$ es continua y cambia de signo, hay al menos un cero en $(1, 2)$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir multiplicidad con número de ceros distintos.** Un polinomio grado 5 puede tener 1 cero distinto (con multiplicidad 5).",
              "**Olvidar el signo del coeficiente principal** al determinar end behavior.",
              "**Pensar que todo polinomio cruza el eje en cada cero.** Si la multiplicidad es par, **rebota**.",
              "**Dibujar polinomios con saltos o picos.** Son siempre **continuos y suaves**.",
              "**Olvidar el TFA** y suponer que un polinomio podría no tener raíces. Siempre tiene $n$ complejas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Polinomio:** $a_n x^n + \\cdots + a_0$. Continuo y suave. Dominio $\\mathbb{R}$.",
              "**Ceros:** intersecciones con eje $x$. **Multiplicidad** controla si cruza o rebota.",
              "**End behavior:** dictado por grado y signo del coeficiente principal.",
              "**TFA:** $n$ raíces complejas contando multiplicidad. Reales $\\leq n$.",
              "**Esbozar gráfica:** ceros + multiplicidad + end behavior + signo en intervalos.",
              "**Próxima lección:** cómo dividir polinomios para encontrar ceros.",
          ]),
    ]
    return {
        "id": "lec-prec-3-2-funciones-polinomiales",
        "title": "Funciones polinomiales",
        "description": "Funciones polinomiales de grado n: ceros, multiplicidad y su efecto gráfico (cruce vs rebote), comportamiento al infinito según grado y signo del coeficiente principal, teorema fundamental del álgebra y teorema del valor intermedio.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# División de polinomios
# =====================================================================
def lesson_division_polinomios():
    blocks = [
        b("texto", body_md=(
            "Para **encontrar los ceros** de un polinomio de grado $> 2$, no hay fórmula general "
            "(como la cuadrática). La estrategia es **factorizar** — y factorizar requiere **dividir**.\n\n"
            "Esta lección presenta dos técnicas:\n\n"
            "1. **División larga de polinomios** — análoga a la división larga de números.\n"
            "2. **División sintética (regla de Ruffini)** — más rápida, válida solo cuando el divisor es de la forma $x - c$.\n\n"
            "Junto con la división, vienen dos teoremas clave: el **del residuo** y el **del factor**, que "
            "conectan división con evaluación y factorización.\n\n"
            "**Al terminar:**\n\n"
            "- Aplicás la **división larga** para dividir polinomios cualquiera.\n"
            "- Aplicás la **división sintética** cuando el divisor es $(x - c)$.\n"
            "- Usás el **teorema del residuo** para evaluar y el **teorema del factor** para detectar ceros.\n"
            "- Aplicás el **teorema de las raíces racionales** para encontrar candidatos a ceros."
        )),

        formulas(
            titulo="Algoritmo de la división",
            body=(
                "**Teorema (algoritmo de la división de polinomios).** Dados polinomios $P(x)$ (dividendo) "
                "y $D(x)$ (divisor) con $D \\neq 0$, existen **únicos** polinomios $Q(x)$ (cociente) y "
                "$R(x)$ (residuo) tales que\n\n"
                "$$\\boxed{\\,P(x) = D(x) \\cdot Q(x) + R(x),\\,}$$\n\n"
                "con $\\deg(R) < \\deg(D)$ (o $R = 0$).\n\n"
                "**Notación equivalente:**\n\n"
                "$$\\dfrac{P(x)}{D(x)} = Q(x) + \\dfrac{R(x)}{D(x)}.$$\n\n"
                "**División exacta:** si $R = 0$, entonces $D$ **divide** a $P$ (es decir, $P = D \\cdot Q$). "
                "$D$ es un **factor** de $P$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="División larga",
          problema_md="Divide $P(x) = 4 x^3 + 7 x + 9$ entre $D(x) = 2 x + 1$.",
          pasos=[
              {"accion_md": (
                  "**Preparar.** Falta el término en $x^2$ → escribir $4 x^3 + 0 x^2 + 7 x + 9$.\n\n"
                  "**Paso 1.** $4 x^3 \\div 2 x = 2 x^2$. Multiplicar: $2 x^2 \\cdot (2 x + 1) = 4 x^3 + 2 x^2$. Restar: $0 - 2 x^2 = -2 x^2$. Bajar el siguiente término: $-2 x^2 + 7 x$."
              ),
               "justificacion_md": "Como con números, dividir el término líder.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2.** $-2 x^2 \\div 2 x = -x$. Multiplicar: $-x(2 x + 1) = -2 x^2 - x$. Restar: $7 x - (-x) = 8 x$. Bajar: $8 x + 9$."
              ),
               "justificacion_md": "Repetir.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3.** $8 x \\div 2 x = 4$. Multiplicar: $4(2 x + 1) = 8 x + 4$. Restar: $9 - 4 = 5$.\n\n"
                  "Como $\\deg(5) = 0 < 1 = \\deg(D)$, **terminamos**.\n\n"
                  "**Cociente:** $Q(x) = 2 x^2 - x + 4$. **Residuo:** $R = 5$.\n\n"
                  "**Verificación.** $(2 x + 1)(2 x^2 - x + 4) + 5 = 4 x^3 - 2 x^2 + 8 x + 2 x^2 - x + 4 + 5 = 4 x^3 + 7 x + 9$ ✓."
              ),
               "justificacion_md": "Siempre verificar al final.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="División sintética (Ruffini)",
            body=(
                "**Cuando el divisor es de la forma $(x - c)$**, hay un atajo: la **división sintética**.\n\n"
                "**Procedimiento (para $P(x) \\div (x - c)$):**\n\n"
                "1. Escribir los **coeficientes** de $P$ en orden (incluyendo ceros para términos faltantes).\n"
                "2. Escribir $c$ a la izquierda.\n"
                "3. Bajar el primer coeficiente al renglón inferior.\n"
                "4. Multiplicar por $c$, escribir el resultado debajo del siguiente coeficiente, sumar.\n"
                "5. Repetir hasta agotar.\n"
                "6. Los números obtenidos son los **coeficientes del cociente** (uno menos que los del dividendo) y el **residuo** al final.\n\n"
                "**Ejemplo.** $P(x) = x^4 - x^3 + x^2 - x + 2$ entre $(x - 2)$:\n\n"
                "```\n"
                " 2 |  1   -1    1   -1    2\n"
                "   |       2    2    6   10\n"
                "   |  1    1    3    5  | 12\n"
                "```\n\n"
                "**Cociente:** $Q(x) = x^3 + x^2 + 3 x + 5$. **Residuo:** $R = 12$.\n\n"
                "**Atención.** La división sintética solo funciona para divisor $(x - c)$ — **no** para $(2 x - 3)$ ni para divisores cuadráticos."
            ),
        ),

        b("definicion",
          titulo="Teoremas del residuo y del factor",
          body_md=(
              "**Teorema del residuo.** Al dividir $P(x)$ entre $(x - c)$, el residuo es exactamente $P(c)$.\n\n"
              "$$P(x) = (x - c) Q(x) + R \\;\\Longrightarrow\\; P(c) = R.$$\n\n"
              "**Aplicación.** Para evaluar $P(c)$ rápidamente, hacer división sintética y leer el residuo.\n\n"
              "**Teorema del factor.** $(x - c)$ es **factor** de $P(x)$ si y solo si $P(c) = 0$.\n\n"
              "**Aplicación.** Si encontrás un cero $c$ (probando), podés **factorizar** $P$ como $(x - c) Q(x)$, donde $Q$ tiene un grado menos. Repetir hasta factorizar completamente.\n\n"
              "**Teorema de las raíces racionales.** Si $P(x) = a_n x^n + \\cdots + a_0$ tiene coeficientes "
              "**enteros** y una raíz racional $p/q$ (en forma irreducible), entonces $p$ divide a $a_0$ y "
              "$q$ divide a $a_n$.\n\n"
              "**Aplicación.** Listar los **candidatos** $\\pm p/q$ con $p \\mid a_0, q \\mid a_n$. Probar cada uno con el teorema del residuo (o sintética). Los que den residuo cero son raíces."
          )),

        b("ejemplo_resuelto",
          titulo="Factorizar usando raíces racionales",
          problema_md="Factoriza $P(x) = x^3 - 3 x - 2$ y halla todos sus ceros.",
          pasos=[
              {"accion_md": (
                  "**Candidatos a raíces racionales.** $a_0 = -2$, $a_n = 1$. Divisores de $-2$: $\\pm 1, \\pm 2$. Divisores de $1$: $\\pm 1$. **Candidatos:** $\\pm 1, \\pm 2$."
              ),
               "justificacion_md": "Lista corta para probar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Probar $x = 2$ por sintética:**\n\n"
                  "```\n"
                  " 2 |  1    0   -3   -2\n"
                  "   |       2    4    2\n"
                  "   |  1    2    1  |  0\n"
                  "```\n\n"
                  "Residuo $0$ → $x = 2$ es raíz. Cociente: $x^2 + 2 x + 1$."
              ),
               "justificacion_md": "El residuo cero confirma que $(x - 2)$ es factor.",
               "es_resultado": False},
              {"accion_md": (
                  "**Factorizar el cociente.** $x^2 + 2 x + 1 = (x + 1)^2$.\n\n"
                  "**Factorización completa:** $P(x) = (x - 2)(x + 1)^2$.\n\n"
                  "**Ceros:** $x = 2$ (multiplicidad 1), $x = -1$ (multiplicidad 2)."
              ),
               "justificacion_md": "Combinar ambos factores.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**División larga vs sintética.** La sintética es **mucho más rápida** y comete menos errores, "
            "pero solo aplica para $(x - c)$. La división larga es general (sirve para cualquier divisor) "
            "pero más laboriosa.\n\n"
            "**Por qué el teorema del residuo es 'milagroso'.** En vez de evaluar $P(c)$ punto a punto "
            "(con todos los exponentes), basta hacer una división sintética rápida. Para polinomios "
            "de grado alto, la sintética es **mucho más eficiente**.\n\n"
            "**Por qué el teorema de las raíces racionales es útil.** Sin él, buscar ceros sería como "
            "buscar una aguja en un pajar (todos los reales). El teorema reduce la búsqueda a una **lista "
            "finita** de candidatos. Si ninguno funciona, las raíces son irracionales o complejas — y hay que "
            "usar otros métodos (numéricos, fórmula cúbica, etc.)."
        )),

        fig(
            "Diagrama esquemático de la división sintética para P(x) = x⁴ - x³ + x² - x + 2 dividido por (x - 2). "
            "Recuadro con tres filas. Fila superior: 'c = 2 |' a la izquierda y luego coeficientes 1, -1, 1, -1, 2. "
            "Fila media: espacio en blanco bajo el primer coeficiente, luego 2, 2, 6, 10 (resultados de multiplicar por c y arrastrar). "
            "Fila inferior: 1, 1, 3, 5 | 12 (sumas, último es el residuo, separado por barra vertical). "
            "Etiqueta 'cociente x³ + x² + 3x + 5' debajo de los primeros 4 números, 'residuo 12' bajo el último. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$P(c) = $ residuo de $P(x)$ dividido entre:",
                  "opciones_md": [
                      "$x + c$",
                      "**$x - c$**",
                      "$c$",
                      "$P(x)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Teorema del residuo.",
                  "explicacion_md": "$P(x) = (x - c) Q(x) + R$, evaluar en $x = c$.",
              },
              {
                  "enunciado_md": "Si $P(3) = 0$, entonces:",
                  "opciones_md": [
                      "$P$ es de grado 3",
                      "**$(x - 3)$ es factor de $P$**",
                      "$3$ no es raíz",
                      "$P$ tiene 3 raíces",
                  ],
                  "correcta": "B",
                  "pista_md": "Teorema del factor.",
                  "explicacion_md": "$(x - c)$ es factor sii $P(c) = 0$.",
              },
              {
                  "enunciado_md": "Para $P(x) = 2 x^3 + x - 6$, los candidatos a raíces racionales son:",
                  "opciones_md": [
                      "$\\pm 1, \\pm 2, \\pm 3, \\pm 6$",
                      "**$\\pm 1, \\pm 2, \\pm 3, \\pm 6, \\pm 1/2, \\pm 3/2$**",
                      "Solo enteros que dividen $2$",
                      "$\\{0, \\pm 1\\}$",
                  ],
                  "correcta": "B",
                  "pista_md": "$p \\mid a_0 = -6$, $q \\mid a_n = 2$.",
                  "explicacion_md": "Numeradores: divisores de 6. Denominadores: divisores de 2.",
              },
          ]),

        ej(
            "División larga",
            "Divide $P(x) = 3 x^4 - 5 x^3 - 20 x - 5$ entre $D(x) = x^2 + x + 3$.",
            ["División larga, agregar $0 x^2$ si falta."],
            (
                "Tras aplicar el algoritmo se obtiene $Q(x) = 3 x^2 - 8 x - 1$ y $R(x) = 5 x - 2$. "
                "Verificación: $(x^2 + x + 3)(3 x^2 - 8 x - 1) + (5 x - 2) = 3 x^4 - 5 x^3 - 20 x - 5$ ✓."
            ),
        ),

        ej(
            "Verificar factor",
            "¿Es $(x + 2)$ factor de $P(x) = x^3 + x^2 - 4 x - 4$? Si sí, factoriza completamente.",
            ["Evaluar $P(-2)$."],
            (
                "$P(-2) = -8 + 4 + 8 - 4 = 0$. **Sí**, $(x + 2)$ es factor. División sintética con $c = -2$ da cociente $x^2 - x - 2 = (x - 2)(x + 1)$. **Factorización:** $P(x) = (x + 2)(x - 2)(x + 1)$."
            ),
        ),

        ej(
            "Raíces racionales",
            "Halla todos los ceros de $P(x) = x^3 - x^2 - 8 x + 12$.",
            ["Candidatos $\\pm 1, \\pm 2, \\pm 3, \\pm 4, \\pm 6, \\pm 12$."],
            (
                "$P(2) = 8 - 4 - 16 + 12 = 0$. Sintética con $c = 2$: cociente $x^2 + x - 6 = (x + 3)(x - 2)$. "
                "**Factorización:** $P(x) = (x - 2)^2 (x + 3)$. **Ceros:** $x = 2$ (mult. 2), $x = -3$ (mult. 1)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar incluir términos con coeficiente cero** al hacer división. $x^3 + 5 = x^3 + 0 x^2 + 0 x + 5$.",
              "**Usar división sintética con divisor que no es $(x - c)$.** Solo funciona en ese caso.",
              "**Confundir el signo de $c$ en sintética.** Si dividís entre $(x + 2)$, usás $c = -2$ (no $+2$).",
              "**Probar candidatos del teorema sin verificar si dieron residuo $0$.** No todos son raíces.",
              "**Olvidar que las raíces irracionales o complejas escapan al teorema racional.** Hay polinomios sin raíces racionales.",
          ]),

        b("resumen",
          puntos_md=[
              "**Algoritmo de división:** $P = D Q + R$ con $\\deg R < \\deg D$, únicos.",
              "**División sintética:** atajo para $(x - c)$. Más rápida que la larga.",
              "**Teorema del residuo:** $P(c) = $ residuo de $P \\div (x - c)$.",
              "**Teorema del factor:** $P(c) = 0 \\Leftrightarrow (x - c)$ es factor.",
              "**Raíces racionales:** $\\pm p/q$ con $p \\mid a_0$, $q \\mid a_n$. Lista finita de candidatos.",
              "**Próxima lección:** cocientes de polinomios — funciones racionales.",
          ]),
    ]
    return {
        "id": "lec-prec-3-3-division-polinomios",
        "title": "División de polinomios",
        "description": "División larga y división sintética (Ruffini) de polinomios. Teoremas del residuo y del factor. Teorema de las raíces racionales y factorización completa de polinomios de grado mayor que 2.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# Funciones racionales
# =====================================================================
def lesson_funciones_racionales():
    blocks = [
        b("texto", body_md=(
            "Una **función racional** es un cociente de polinomios:\n\n"
            "$$r(x) = \\dfrac{P(x)}{Q(x)}, \\qquad Q(x) \\neq 0.$$\n\n"
            "Su gráfica suele tener **asíntotas** — rectas a las que la curva se acerca sin tocarlas — "
            "y eso la hace mucho más interesante que la de un polinomio.\n\n"
            "**Tres tipos de asíntotas a estudiar:**\n\n"
            "- **Verticales** ($x = a$): donde el denominador se anula sin que el numerador lo haga.\n"
            "- **Horizontales** ($y = b$): donde la función tiende cuando $x \\to \\pm \\infty$.\n"
            "- **Oblicuas** ($y = m x + b$): cuando el grado del numerador supera al denominador en uno.\n\n"
            "**Al terminar:**\n\n"
            "- Hallás el **dominio** y los **ceros** de una función racional.\n"
            "- Identificás las **asíntotas verticales, horizontales y oblicuas**.\n"
            "- Esbozás la gráfica usando intersecciones, asíntotas y análisis de signo."
        )),

        b("definicion",
          titulo="Función racional",
          body_md=(
              "Una **función racional** es de la forma\n\n"
              "$$r(x) = \\dfrac{P(x)}{Q(x)},$$\n\n"
              "donde $P$ y $Q$ son polinomios y $Q \\neq 0$ como polinomio.\n\n"
              "**Dominio:** todos los reales **excepto** los ceros de $Q(x)$:\n\n"
              "$$\\operatorname{Dom}(r) = \\{x \\in \\mathbb{R} : Q(x) \\neq 0\\}.$$\n\n"
              "**Ceros (intersecciones con eje $x$):** ceros del numerador $P(x)$ **que no anulen también el denominador**.\n\n"
              "**Intersección con eje $y$:** $r(0) = P(0)/Q(0)$, si $Q(0) \\neq 0$.\n\n"
              "**Antes de cualquier análisis, factorizar y simplificar** numerador y denominador. Esto revela cancelaciones que producen 'agujeros' (discontinuidades evitables) en vez de asíntotas."
          )),

        b("definicion",
          titulo="Asíntota vertical",
          body_md=(
              "Una recta $x = a$ es **asíntota vertical** de $r$ si $r(x) \\to \\pm \\infty$ cuando $x \\to a$ (por izquierda, derecha o ambos lados).\n\n"
              "**Cómo encontrarlas:** después de **simplificar** $r$, los **ceros del denominador** son las asíntotas verticales.\n\n"
              "Ejemplo: $r(x) = \\dfrac{1}{x - 3}$ tiene asíntota vertical $x = 3$.\n\n"
              "**Cuidado con cancelaciones.** Si $P$ y $Q$ comparten un factor $(x - a)$ que se cancela, entonces en $x = a$ hay un **'agujero' (hueco)** en la gráfica, no una asíntota.\n\n"
              "Ejemplo: $r(x) = \\dfrac{x^2 - 4}{x - 2} = \\dfrac{(x - 2)(x + 2)}{x - 2} = x + 2$ (con $x \\neq 2$). En $x = 2$ hay un agujero, **no** asíntota."
          )),

        formulas(
            titulo="Asíntotas horizontales y oblicuas",
            body=(
                "Sea $r(x) = \\dfrac{P(x)}{Q(x)}$ con $\\deg(P) = n$ y $\\deg(Q) = m$. Las asíntotas al "
                "infinito dependen de la **comparación entre $n$ y $m$**:\n\n"
                "| Caso | Asíntota |\n"
                "|---|---|\n"
                "| $n < m$ | **Horizontal** $y = 0$ |\n"
                "| $n = m$ | **Horizontal** $y = a_n / b_m$ (cociente de coeficientes principales) |\n"
                "| $n = m + 1$ | **Oblicua** $y = m x + b$ (cociente de la división polinomial) |\n"
                "| $n > m + 1$ | **Ninguna** asíntota al infinito (la función crece más rápido que cualquier recta) |\n\n"
                "**Para hallar la asíntota oblicua** ($n = m + 1$): hacer la división polinomial $P / Q$. El "
                "cociente es una recta $m x + b$, que es la asíntota.\n\n"
                "$$r(x) = (m x + b) + \\dfrac{R(x)}{Q(x)},$$\n\n"
                "donde el segundo sumando $\\to 0$ cuando $x \\to \\pm \\infty$.\n\n"
                "**Una función racional tiene a lo sumo una asíntota horizontal o una oblicua, no ambas.**"
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Análisis completo",
          problema_md=(
              "Estudia $r(x) = \\dfrac{3 x^2 - 2 x - 1}{2 x^2 + 3 x - 2}$: dominio, ceros, asíntotas e intersecciones."
          ),
          pasos=[
              {"accion_md": (
                  "**Factorizar.** Numerador: $3 x^2 - 2 x - 1 = (3 x + 1)(x - 1)$. Denominador: $2 x^2 + 3 x - 2 = (2 x - 1)(x + 2)$.\n\n"
                  "$r(x) = \\dfrac{(3 x + 1)(x - 1)}{(2 x - 1)(x + 2)}$. **No hay cancelaciones.**"
              ),
               "justificacion_md": "Factorizar siempre primero.",
               "es_resultado": False},
              {"accion_md": (
                  "**Dominio:** $x \\neq 1/2$ y $x \\neq -2$. **$\\operatorname{Dom}(r) = \\mathbb{R} \\setminus \\{-2, 1/2\\}$**."
              ),
               "justificacion_md": "Anular denominador.",
               "es_resultado": False},
              {"accion_md": (
                  "**Ceros (eje $x$):** ceros del numerador. $3 x + 1 = 0 \\Rightarrow x = -1/3$. $x - 1 = 0 \\Rightarrow x = 1$.\n\n"
                  "**Intersección con eje $y$:** $r(0) = -1 / -2 = 1/2$. Punto $(0, 1/2)$."
              ),
               "justificacion_md": "Numerador cero, denominador no cero.",
               "es_resultado": False},
              {"accion_md": (
                  "**Asíntotas verticales:** ceros del denominador → $x = 1/2$ y $x = -2$.\n\n"
                  "**Asíntota horizontal:** mismo grado (2 = 2) → $y = a_n/b_m = 3/2$."
              ),
               "justificacion_md": "Aplicar la tabla.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Asíntota oblicua",
          problema_md="Halla las asíntotas de $r(x) = \\dfrac{x^2}{x - 2}$.",
          pasos=[
              {"accion_md": (
                  "**Asíntota vertical:** $x = 2$ (cero del denominador, no se cancela)."
              ),
               "justificacion_md": "Simple.",
               "es_resultado": False},
              {"accion_md": (
                  "**Comparar grados:** $n = 2$, $m = 1$, $n = m + 1$. **Hay asíntota oblicua.**\n\n"
                  "**División polinomial.** $x^2 \\div (x - 2)$ por sintética con $c = 2$:\n\n"
                  "```\n"
                  " 2 |  1   0   0\n"
                  "   |      2   4\n"
                  "   |  1   2  | 4\n"
                  "```\n\n"
                  "Cociente $x + 2$, residuo $4$. Así $r(x) = x + 2 + \\dfrac{4}{x - 2}$."
              ),
               "justificacion_md": "El cociente da la asíntota oblicua.",
               "es_resultado": False},
              {"accion_md": (
                  "**Asíntota oblicua:** $y = x + 2$. Cuando $x \\to \\pm \\infty$, el término $4/(x - 2) \\to 0$, así $r(x) \\to x + 2$."
              ),
               "justificacion_md": "Confirmación rigurosa.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué los grados deciden.** Cuando $x$ es muy grande, en $r(x) = P(x)/Q(x)$ los términos "
            "principales dominan: $r(x) \\approx (a_n x^n) / (b_m x^m) = (a_n / b_m) x^{n - m}$.\n\n"
            "- Si $n < m$: $x^{n - m} \\to 0$, así $r \\to 0$ (asíntota horizontal $y = 0$).\n"
            "- Si $n = m$: $x^{n - m} = 1$, así $r \\to a_n / b_m$ (constante).\n"
            "- Si $n = m + 1$: $r \\approx (a_n / b_m) x$, recta — pero más precisamente $r = m x + b + (\\text{decreciente})$.\n"
            "- Si $n > m + 1$: $r$ crece sin parecerse a ninguna recta.\n\n"
            "**Asíntotas vs. la función.** Una función **se acerca** a su asíntota pero **puede cruzarla** (las horizontales y oblicuas se pueden cruzar; las verticales no, porque la función no está definida ahí).\n\n"
            "**Estrategia para graficar.** (1) Factorizar. (2) Dominio, ceros, intersección $y$. (3) Asíntotas vert., horiz. u oblicua. (4) Análisis de signo en cada región delimitada por ceros y asíntotas verticales. (5) Esbozar acercándose a las asíntotas."
        )),

        fig(
            "Función racional r(x) = (3x² - 2x - 1)/(2x² + 3x - 2) graficada en color teal #06b6d4. "
            "Asíntotas verticales x = 1/2 y x = -2 dibujadas como líneas verticales punteadas en color ámbar #f59e0b. "
            "Asíntota horizontal y = 3/2 dibujada como línea horizontal punteada gris. "
            "La curva tiene tres ramas separadas por las asíntotas verticales, cada una acercándose a las asíntotas. "
            "Marcar los ceros x = -1/3 y x = 1 con puntos sobre el eje x. "
            "Eje x de -5 a 5, eje y de -5 a 5. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para $r(x) = \\dfrac{x + 1}{x^2 - 4}$, las asíntotas verticales son:",
                  "opciones_md": [
                      "$x = -1$",
                      "**$x = \\pm 2$**",
                      "$y = 0$",
                      "Ninguna",
                  ],
                  "correcta": "B",
                  "pista_md": "Ceros del denominador.",
                  "explicacion_md": "$x^2 - 4 = (x - 2)(x + 2) = 0$. Sin cancelaciones.",
              },
              {
                  "enunciado_md": "Si $\\deg P = 3$ y $\\deg Q = 5$, la asíntota horizontal es:",
                  "opciones_md": [
                      "No tiene",
                      "**$y = 0$**",
                      "$y = a_3 / b_5$",
                      "$y = x$",
                  ],
                  "correcta": "B",
                  "pista_md": "$n < m$.",
                  "explicacion_md": "Si el numerador es de menor grado, la función va a cero en infinito.",
              },
              {
                  "enunciado_md": "Para $r(x) = \\dfrac{(x - 3)(x + 1)}{x - 3}$ (sin simplificar), en $x = 3$ hay:",
                  "opciones_md": [
                      "Asíntota vertical",
                      "**Un agujero (no asíntota)**",
                      "Cero",
                      "Asíntota horizontal",
                  ],
                  "correcta": "B",
                  "pista_md": "El factor $(x - 3)$ se cancela.",
                  "explicacion_md": "Cancelación del numerador con denominador → agujero, no asíntota.",
              },
          ]),

        ej(
            "Asíntotas",
            "Halla las asíntotas verticales y horizontal de $s(x) = \\dfrac{6 x^2 + 1}{2 x^2 + x - 1}$.",
            ["Factorizar denominador, comparar grados."],
            (
                "Denominador: $(2 x - 1)(x + 1)$. **Verticales:** $x = 1/2, x = -1$. Mismo grado en numerador y denominador → **horizontal:** $y = 6/2 = 3$."
            ),
        ),

        ej(
            "Transformación de $1/x$",
            "Reescribe $r(x) = \\dfrac{2 x - 3}{x - 2}$ como una transformación de $y = 1/x$ y describe sus asíntotas.",
            ["División larga: $r = 2 + 1/(x - 2)$."],
            (
                "$r(x) = 2 + \\dfrac{1}{x - 2}$. Asíntota vertical $x = 2$, horizontal $y = 2$. Es la hipérbola $1/x$ trasladada 2 a la derecha y 2 hacia arriba."
            ),
        ),

        ej(
            "Asíntota oblicua",
            "Halla la asíntota oblicua y vertical de $r(x) = \\dfrac{x^2 + 5 x + 4}{x - 3}$.",
            ["División sintética con $c = 3$."],
            (
                "Sintética: cociente $x + 8$, residuo $28$. $r(x) = x + 8 + \\dfrac{28}{x - 3}$.\n\n"
                "**Asíntota vertical:** $x = 3$. **Asíntota oblicua:** $y = x + 8$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar factorizar antes** y perder cancelaciones (agujeros tratados como asíntotas).",
              "**Confundir asíntota horizontal con oblicua.** Solo hay una de las dos según los grados.",
              "**Pensar que la función nunca cruza las asíntotas.** Las horizontales y oblicuas se pueden cruzar.",
              "**Calcular asíntota horizontal con grados $n > m$ y poner $y = 0$.** Solo es $y = 0$ cuando $n < m$.",
              "**No verificar el signo de la función a ambos lados de una asíntota vertical.** Determina si va a $+\\infty$ o a $-\\infty$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Función racional:** $P(x)/Q(x)$. Dominio = $\\mathbb{R} \\setminus \\{Q = 0\\}$.",
              "**Ceros:** ceros del numerador (que no anulen denominador).",
              "**Asíntotas verticales:** ceros del denominador (después de simplificar).",
              "**Asíntotas horizontales/oblicuas:** comparar $\\deg P$ y $\\deg Q$. Tabla de la lección.",
              "**Cancelaciones:** producen agujeros, no asíntotas.",
              "**Cierre del capítulo:** dominamos polinomiales (cuadrática, grado n, división) y racionales — todas las funciones algebraicas.",
              "**Próximo capítulo:** funciones trascendentes — exponenciales y logarítmicas.",
          ]),
    ]
    return {
        "id": "lec-prec-3-4-funciones-racionales",
        "title": "Funciones racionales",
        "description": "Cocientes de polinomios r(x) = P(x)/Q(x): dominio, ceros, asíntotas verticales, horizontales y oblicuas según comparación de grados. Cancelaciones (agujeros) y esbozo de gráfica.",
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
    course_id = "precalculo"

    existing_course = await db.courses.find_one({"id": course_id})
    if not existing_course:
        print(f"⚠ Curso '{course_id}' no existe. Ejecutá primero seed_precalculo_chapter_1.py.")
        return
    print(f"✓ Curso encontrado: {existing_course.get('title', course_id)}")

    chapter_id = "ch-prec-polinomiales-racionales"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Funciones Polinomiales y Racionales",
        "description": (
            "Función cuadrática (forma vértice, discriminante), funciones polinomiales de grado n "
            "(ceros, multiplicidad, end behavior), división de polinomios (larga y sintética, teoremas "
            "del residuo y del factor, raíces racionales) y funciones racionales (asíntotas verticales, "
            "horizontales y oblicuas)."
        ),
        "order": 3,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_funcion_cuadratica,
        lesson_funciones_polinomiales,
        lesson_division_polinomios,
        lesson_funciones_racionales,
    ]
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
        f"✅ Capítulo 3 — Funciones Polinomiales y Racionales listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())

