"""
Seed del curso Cálculo Multivariable — Capítulo 3: Funciones de Varias Variables.
2 lecciones:
  3.1 Dominio y rango
  3.2 Límites y continuidad

Incluye figuras para visualizar curvas de nivel, gráficos 3D y caminos al límite.
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
# 3.1 Dominio y rango
# =====================================================================
def lesson_3_1():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora hemos trabajado con funciones $f: \\mathbb{R} \\to \\mathbb{R}$ — una entrada, una salida. "
            "Ahora damos el salto a funciones de **varias variables**: $f: D \\subset \\mathbb{R}^n \\to \\mathbb{R}$. "
            "El caso más importante (y visualizable) es $n = 2$: $f(x, y)$, cuya gráfica es una **superficie en $\\mathbb{R}^3$**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Identificar el **dominio** y el **rango** de funciones $f(x, y)$ y $f(x, y, z)$.\n"
            "- Visualizar funciones de dos variables como **superficies**.\n"
            "- Trazar **curvas de nivel** (mapa topográfico) y **superficies de nivel**.\n"
            "- Reconocer las gráficas clásicas (planos, paraboloides, esferas, conos)."
        )),

        b("definicion",
          titulo="Función de varias variables",
          body_md=(
              "Una **función de $n$ variables** es una regla $f: D \\subset \\mathbb{R}^n \\to \\mathbb{R}$ que asigna "
              "a cada punto $(x_1, \\ldots, x_n) \\in D$ un único número $f(x_1, \\ldots, x_n)$.\n\n"
              "**Caso clave $n = 2$:** $f(x, y)$. Su gráfica es el conjunto:\n\n"
              "$$\\{(x, y, z) : z = f(x, y), \\; (x, y) \\in D\\} \\subset \\mathbb{R}^3$$\n\n"
              "**Una superficie**.\n\n"
              "**Caso $n = 3$:** $f(x, y, z)$ no es visualizable directamente (la gráfica viviría en $\\mathbb{R}^4$), pero se estudia con **superficies de nivel**."
          )),

        b("definicion",
          titulo="Dominio y rango",
          body_md=(
              "**Dominio** de $f$: el conjunto $D \\subset \\mathbb{R}^n$ de entradas válidas. Si no se da explícitamente, "
              "se asume el **dominio natural**: el mayor subconjunto donde la fórmula tiene sentido.\n\n"
              "**Restricciones típicas para encontrar el dominio:**\n\n"
              "- **Denominadores no nulos:** $\\dfrac{1}{x - y}$ requiere $x \\neq y$.\n"
              "- **Argumentos de raíces pares no negativos:** $\\sqrt{x + y}$ requiere $x + y \\geq 0$.\n"
              "- **Argumentos de logaritmos positivos:** $\\ln(x^2 - y)$ requiere $x^2 > y$.\n"
              "- **Argumentos de $\\arcsin, \\arccos$ en $[-1, 1]$.**\n\n"
              "**Rango** de $f$: el conjunto $\\{f(x, y) : (x, y) \\in D\\} \\subset \\mathbb{R}$ — los valores que efectivamente toma la función."
          )),

        b("ejemplo_resuelto",
          titulo="Encontrar dominio y rango",
          problema_md="Hallar el dominio y rango de $f(x, y) = \\sqrt{9 - x^2 - y^2}$.",
          pasos=[
              {"accion_md": "**Dominio:** raíz par, así $9 - x^2 - y^2 \\geq 0 \\iff x^2 + y^2 \\leq 9$.\n\n"
                            "Es el **disco cerrado de radio $3$** centrado en el origen.",
               "justificacion_md": "Restricción típica de raíz cuadrada.",
               "es_resultado": False},
              {"accion_md": "**Rango:** $f(x, y) \\geq 0$ siempre (es una raíz). El máximo se alcanza en el origen: $f(0, 0) = 3$. El mínimo en el borde: $f(x, y) = 0$ cuando $x^2 + y^2 = 9$.\n\n"
                            "**Rango:** $[0, 3]$.",
               "justificacion_md": "Analizar los extremos de la raíz.",
               "es_resultado": False},
              {"accion_md": "**Geometría:** la gráfica es **el hemisferio superior** de la esfera $x^2 + y^2 + z^2 = 9$ (porque $z = \\sqrt{9 - x^2 - y^2} \\geq 0$ implica $z^2 = 9 - x^2 - y^2$, y solo la mitad de arriba).",
               "justificacion_md": "**Truco visual:** elevar al cuadrado a veces revela una superficie clásica.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Curvas de nivel",
          body_md=(
              "Una **curva de nivel** de $f(x, y)$ con valor $k$ es:\n\n"
              "$$\\{(x, y) : f(x, y) = k\\}$$\n\n"
              "Es decir, el conjunto de puntos del plano donde $f$ vale exactamente $k$. **Geométricamente:** "
              "la **proyección al plano $xy$** de la intersección de la superficie $z = f(x, y)$ con el plano horizontal $z = k$.\n\n"
              "**Analogía topográfica:** un mapa con curvas de nivel muestra alturas constantes. "
              "Caminar a lo largo de una curva de nivel = mantener altura constante. "
              "Curvas muy juntas = pendiente fuerte; curvas separadas = terreno suave."
          )),

        fig(
            "Comparación lado a lado de una superficie 3D y sus curvas de nivel. PANEL IZQUIERDO: "
            "vista 3D isométrica de la superficie z = x² + y² (paraboloide elíptico, cuenco abierto "
            "hacia arriba), color teal claro semi-translúcido. Marcar tres planos horizontales que "
            "cortan la superficie en z = 1, z = 4, z = 9 (en líneas punteadas). PANEL DERECHO: "
            "vista 2D del plano xy con tres curvas de nivel correspondientes — círculos "
            "concéntricos x²+y² = 1, x²+y² = 4, x²+y² = 9 (radios 1, 2, 3), cada uno etiquetado "
            "con su valor 'k = 1', 'k = 4', 'k = 9'. Etiquetas claras en ambos paneles. " + STYLE
        ),

        b("ejemplo_resuelto",
          titulo="Curvas de nivel de un paraboloide",
          problema_md="Trazar las curvas de nivel de $f(x, y) = x^2 + y^2$ para $k = 1, 4, 9$.",
          pasos=[
              {"accion_md": "**Plantear** $f(x, y) = k$: $x^2 + y^2 = k$.",
               "justificacion_md": "Igualar la función al valor de nivel.",
               "es_resultado": False},
              {"accion_md": "**Curvas para cada $k$:**\n\n"
                            "- $k = 1$: $x^2 + y^2 = 1$ — círculo de radio $1$.\n"
                            "- $k = 4$: $x^2 + y^2 = 4$ — círculo de radio $2$.\n"
                            "- $k = 9$: $x^2 + y^2 = 9$ — círculo de radio $3$.",
               "justificacion_md": "Círculos concéntricos crecientes — la firma del paraboloide visto desde arriba.",
               "es_resultado": False},
              {"accion_md": "**Caso degenerado:** $k = 0$ da $x^2 + y^2 = 0 \\iff (x, y) = (0, 0)$ — un solo punto. **Caso vacío:** $k < 0$ no tiene solución (suma de cuadrados no es negativa).",
               "justificacion_md": "**Lección general:** las curvas de nivel pueden ser un punto, vacío, o curvas — depende del valor.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Superficies de nivel (para $f(x, y, z)$)",
          body_md=(
              "Para una función de tres variables $f(x, y, z)$, una **superficie de nivel** con valor $k$ es:\n\n"
              "$$\\{(x, y, z) : f(x, y, z) = k\\}$$\n\n"
              "Como ahora la entrada es $\\mathbb{R}^3$ y el conjunto $f = k$ es **2-dimensional**, no son curvas sino **superficies**.\n\n"
              "**Ejemplo clásico:** $f(x, y, z) = x^2 + y^2 + z^2$. Sus superficies de nivel son **esferas concéntricas**.\n\n"
              "**Aplicación:** las **isobaras** (curvas de presión constante) de un mapa meteorológico son curvas de nivel; las **isotermas** son lo mismo. En 3D, las superficies de temperatura constante en una habitación son superficies de nivel."
          )),

        b("ejemplo_resuelto",
          titulo="Reconocer la gráfica",
          problema_md="Describir la gráfica de $f(x, y) = \\sqrt{x^2 + y^2}$.",
          pasos=[
              {"accion_md": "**Curvas de nivel:** $\\sqrt{x^2 + y^2} = k \\iff x^2 + y^2 = k^2$ (con $k \\geq 0$). Círculos de radio $k$.",
               "justificacion_md": "Equiparable al paraboloide... pero no del todo.",
               "es_resultado": False},
              {"accion_md": "**Comportamiento radial:** $f$ depende solo de $r = \\sqrt{x^2+y^2}$, así $z = r$. **Es la mitad superior de un cono** $z^2 = x^2+y^2$ (con $z \\geq 0$).",
               "justificacion_md": "**Diferencia clave con el paraboloide** $z = x^2 + y^2$: el paraboloide crece como $r^2$ (más rápido al alejarse); el cono crece linealmente como $r$. Curvas de nivel del cono: $r = k$ (radios proporcionales a $k$). Curvas del paraboloide: $r^2 = k$ (radios proporcionales a $\\sqrt{k}$, más juntas al alejarse).",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El dominio de $f(x, y) = \\ln(x - y)$ es:",
                  "opciones_md": [
                      "$\\{(x, y) : x \\geq y\\}$",
                      "$\\{(x, y) : x > y\\}$",
                      "$\\{(x, y) : x \\neq y\\}$",
                      "$\\mathbb{R}^2$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\ln$ requiere argumento **estrictamente positivo**.",
                  "explicacion_md": (
                      "$\\ln(x - y)$ exige $x - y > 0 \\iff x > y$. **Geometría:** la región del plano arriba de la recta $y = x$ — un semiplano abierto."
                  ),
              },
              {
                  "enunciado_md": "Las curvas de nivel de $f(x, y) = y - x^2$ son:",
                  "opciones_md": [
                      "Círculos",
                      "Rectas paralelas",
                      "Parábolas $y = x^2 + k$",
                      "Hipérbolas",
                  ],
                  "correcta": "C",
                  "pista_md": "$f(x, y) = k \\iff y - x^2 = k \\iff y = x^2 + k$.",
                  "explicacion_md": (
                      "$y = x^2 + k$ son **parábolas** desplazadas verticalmente. Cada $k$ da una parábola distinta. La gráfica de $f$ es un cilindro parabólico inclinado."
                  ),
              },
          ]),

        ej(
            titulo="Dominio con dos restricciones",
            enunciado="Halla el dominio de $f(x, y) = \\dfrac{\\sqrt{x - y}}{x^2 + y^2 - 4}$.",
            pistas=[
                "Dos restricciones: la raíz exige $x - y \\geq 0$, y el denominador exige $x^2 + y^2 \\neq 4$.",
                "Combina ambas: el dominio es la intersección.",
            ],
            solucion=(
                "**Restricción 1 (raíz):** $x \\geq y$ — semiplano debajo (o sobre) la recta $y = x$.\n\n"
                "**Restricción 2 (denominador):** $x^2 + y^2 \\neq 4$ — todo el plano excepto el círculo de radio $2$.\n\n"
                "**Dominio:** $\\{(x, y) : x \\geq y \\text{ y } x^2 + y^2 \\neq 4\\}$. Geométricamente: el semiplano $y \\leq x$ menos los puntos del círculo $x^2 + y^2 = 4$."
            ),
        ),

        ej(
            titulo="Curvas de nivel de un plano inclinado",
            enunciado="Describe las curvas de nivel de $f(x, y) = 2x + 3y$.",
            pistas=[
                "$f(x, y) = k \\iff 2x + 3y = k$. ¿Qué curva representa eso?",
            ],
            solucion=(
                "$2x + 3y = k$ es una **recta** con pendiente $-2/3$ (en cada $k$). Las curvas de nivel son **rectas paralelas** entre sí.\n\n"
                "**Geometría:** la gráfica $z = 2x + 3y$ es un **plano** inclinado pasando por el origen. Sus 'curvas de nivel' son las intersecciones con planos horizontales — rectas paralelas, todas con la misma pendiente en el plano $xy$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar que el dominio puede ser una región del plano**, no solo un intervalo. La diferencia con cálculo de una variable es geométricamente importante.",
              "**Confundir curva de nivel con gráfica.** La curva de nivel **vive en $\\mathbb{R}^2$** (el dominio); la gráfica vive en $\\mathbb{R}^3$.",
              "**Confundir paraboloide con cono.** Paraboloide: $z = x^2 + y^2$ (radios crecen como $\\sqrt{k}$). Cono: $z = \\sqrt{x^2+y^2}$ (radios crecen como $k$).",
              "**No verificar valores excluidos** del rango. Por ejemplo, $1/(x^2+y^2)$ nunca es $0$, así $0$ no está en el rango.",
              "**Olvidar que curvas de nivel se proyectan al plano $xy$**, no \"viven\" en altura $z = k$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Función de varias variables:** $f: D \\subset \\mathbb{R}^n \\to \\mathbb{R}$.",
              "**Caso $n = 2$:** gráfica es una superficie en $\\mathbb{R}^3$.",
              "**Dominio:** restricciones por denominadores, raíces, logaritmos, dominios trigonométricos.",
              "**Curvas de nivel** $f(x, y) = k$: proyecciones al plano $xy$ de cortes horizontales. Mapa topográfico.",
              "**Superficies de nivel** $f(x, y, z) = k$: análogas para 3 variables (no se grafica $f$ en sí).",
              "**Gráficas clásicas:** plano (lineal), paraboloide ($x^2+y^2$), cono ($\\sqrt{x^2+y^2}$), hemisferio ($\\sqrt{r^2 - x^2 - y^2}$).",
              "**Próxima lección:** límites y continuidad — ahora con infinitos caminos para acercarse a un punto.",
          ]),
    ]
    return {
        "id": "lec-mvar-3-1-dominio-rango",
        "title": "Dominio y rango",
        "description": "Funciones de varias variables, dominio natural, rango, gráficas como superficies y curvas/superficies de nivel.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 3.2 Límites y continuidad
# =====================================================================
def lesson_3_2():
    blocks = [
        b("texto", body_md=(
            "El concepto de **límite** se generaliza directamente a varias variables, pero con una "
            "diferencia crucial respecto al caso 1D: en $\\mathbb{R}^2$ hay **infinitos caminos** para "
            "acercarse a un punto $(a, b)$. Para que el límite exista, **todos** deben dar el mismo valor.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir $\\lim_{(x,y) \\to (a,b)} f(x, y)$ y comprender su sutileza.\n"
            "- Aplicar el **test de los caminos** para mostrar **no existencia**.\n"
            "- Usar **coordenadas polares** para evaluar límites en $(0, 0)$.\n"
            "- Caracterizar la **continuidad** de funciones de varias variables."
        )),

        b("definicion",
          titulo="Límite de una función de dos variables",
          body_md=(
              "$$\\lim_{(x, y) \\to (a, b)} f(x, y) = L$$\n\n"
              "significa que para todo $\\epsilon > 0$ existe $\\delta > 0$ tal que\n\n"
              "$$0 < \\sqrt{(x-a)^2 + (y-b)^2} < \\delta \\implies |f(x, y) - L| < \\epsilon$$\n\n"
              "**Idea:** $f(x, y)$ está cerca de $L$ siempre que $(x, y)$ esté cerca de $(a, b)$ — **sin importar desde qué dirección se acerque**.\n\n"
              "**Generalización a $\\mathbb{R}^n$:** la distancia $\\sqrt{\\sum (x_i - a_i)^2}$ reemplaza al $|x - a|$ del caso 1D."
          )),

        b("intuicion",
          titulo="Infinitos caminos cambian todo",
          body_md=(
              "En 1D, $x \\to a$ tiene **dos direcciones**: por izquierda y por derecha. El límite existe si los dos laterales coinciden.\n\n"
              "En $\\mathbb{R}^2$, $(x, y) \\to (a, b)$ tiene **infinitas direcciones**: por el eje $x$, por el eje $y$, por la diagonal, por una espiral, por una parábola, por una recta de pendiente $m$ cualquiera...\n\n"
              "**Para que el límite exista, todos esos caminos deben dar el mismo valor.** Si encuentras dos caminos con valores distintos, el límite no existe."
          )),

        fig(
            "Diagrama 2D ilustrando 'infinitos caminos al acercarse a un punto'. Plano cartesiano con "
            "el origen marcado como punto destacado. Varias curvas convergiendo hacia el origen "
            "desde distintas direcciones, en colores distintos: una recta horizontal (eje x) en "
            "rojo, una recta vertical (eje y) en azul, una recta diagonal y = x en verde, una "
            "parábola y = x² en violeta, una espiral aproximándose en naranja. Cada curva con una "
            "flecha apuntando hacia el origen. Etiqueta general 'infinitos caminos hacia (0, 0)'. " + STYLE
        ),

        b("teorema",
          nombre="Test de los caminos (no existencia)",
          enunciado_md=(
              "Si existen dos caminos $C_1, C_2$ que pasan por $(a, b)$ tales que el límite de $f$ a lo largo de cada uno es **distinto**, entonces:\n\n"
              "$$\\lim_{(x, y) \\to (a, b)} f(x, y) \\quad \\text{NO existe}$$\n\n"
              "**Caminos típicos para probar:**\n\n"
              "- Eje $x$: $y = 0$, hacer $x \\to a$.\n"
              "- Eje $y$: $x = 0$, hacer $y \\to b$.\n"
              "- Diagonal: $y = x$, hacer $x \\to a$ (con $b = a$).\n"
              "- Recta de pendiente $m$: $y = m x$ (con $(a, b) = (0, 0)$).\n"
              "- Parábola: $y = x^2$, etc."
          ),
          demostracion_md=(
              "Por contrapositiva: si el límite existe, **todos** los caminos dan el mismo valor (ese límite). "
              "Si dos caminos dan valores distintos, no puede existir un valor único $L$."
          )),

        b("ejemplo_resuelto",
          titulo="Caso clásico: $\\lim_{(x,y) \\to (0,0)} \\dfrac{xy}{x^2 + y^2}$",
          problema_md="Determinar si el límite existe.",
          pasos=[
              {"accion_md": "**Camino 1: eje $x$** ($y = 0$, $x \\to 0$):\n\n"
                            "$f(x, 0) = \\dfrac{x \\cdot 0}{x^2 + 0} = 0 \\to 0$.",
               "justificacion_md": "Por el eje $x$ el límite es $0$.",
               "es_resultado": False},
              {"accion_md": "**Camino 2: diagonal** ($y = x$, $x \\to 0$):\n\n"
                            "$f(x, x) = \\dfrac{x \\cdot x}{x^2 + x^2} = \\dfrac{x^2}{2x^2} = \\dfrac{1}{2} \\to \\dfrac{1}{2}$.",
               "justificacion_md": "Por la diagonal el límite es $1/2$.",
               "es_resultado": False},
              {"accion_md": "**Como $0 \\neq 1/2$, el límite NO existe.**",
               "justificacion_md": "**Contraejemplo clásico:** un cociente con cada componente individual yendo a $0$, pero la función global no tiene límite. **Lección:** acercarse por dos caminos no es suficiente — pero es suficiente para mostrar **no existencia**.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Cómo demostrar existencia, entonces?",
          body_md=(
              "El test de los caminos es **asimétrico**: solo sirve para mostrar **no existencia**.\n\n"
              "Para demostrar **existencia**, hay tres rutas comunes:\n\n"
              "1. **Sustitución directa** si $f$ es continua en $(a, b)$ (polinomial, racional sin denominador 0, exponencial, etc.).\n\n"
              "2. **Coordenadas polares** alrededor de $(0, 0)$: $x = r\\cos\\theta$, $y = r\\sin\\theta$. Si el límite cuando $r \\to 0$ existe **independiente de $\\theta$**, ese es el límite.\n\n"
              "3. **Sándwich** o cota superior: $|f(x, y) - L| \\leq g(r)$ con $g(r) \\to 0$.\n\n"
              "**Atención:** caminos arbitrarios no son suficientes — un límite puede ser igual por todos los caminos rectos pero distinto en una espiral. Las polares son seguras."
          )),

        b("ejemplo_resuelto",
          titulo="Existencia con polares",
          problema_md="Calcular $\\lim_{(x,y) \\to (0,0)} \\dfrac{x^2 y}{x^2 + y^2}$.",
          pasos=[
              {"accion_md": "**Coordenadas polares:** $x = r\\cos\\theta$, $y = r\\sin\\theta$. Sustituimos:\n\n"
                            "$\\dfrac{r^2 \\cos^2\\theta \\cdot r\\sin\\theta}{r^2(\\cos^2\\theta + \\sin^2\\theta)} = \\dfrac{r^3 \\cos^2\\theta \\sin\\theta}{r^2} = r \\cos^2\\theta \\sin\\theta$.",
               "justificacion_md": "Polares simplifican muchísimo cuando hay $x^2 + y^2$ en el denominador.",
               "es_resultado": False},
              {"accion_md": "**Cota:** $|r \\cos^2\\theta \\sin\\theta| \\leq r \\to 0$ cuando $r \\to 0$, **independiente de $\\theta$**.",
               "justificacion_md": "Por sándwich (o porque $|\\cos^2\\theta \\sin\\theta| \\leq 1$).",
               "es_resultado": False},
              {"accion_md": "$$\\lim_{(x,y) \\to (0,0)} \\dfrac{x^2 y}{x^2 + y^2} = 0$$",
               "justificacion_md": "**Comparación con el ejemplo anterior:** $xy/(x^2+y^2)$ no existía, pero $x^2 y/(x^2+y^2)$ sí — la diferencia: aquí el numerador es de grado 3, el denominador grado 2; en polares queda un factor $r$ que aniquila todo.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Continuidad",
          body_md=(
              "$f$ es **continua en $(a, b)$** si:\n\n"
              "1. $(a, b)$ está en el dominio de $f$.\n"
              "2. $\\lim_{(x, y) \\to (a, b)} f(x, y)$ existe.\n"
              "3. $\\lim_{(x, y) \\to (a, b)} f(x, y) = f(a, b)$.\n\n"
              "**$f$ es continua en una región $D$** si lo es en cada punto de $D$.\n\n"
              "**Funciones continuas \"de fábrica\":**\n\n"
              "- **Polinomios** en $x, y$: continuos en todo $\\mathbb{R}^2$.\n"
              "- **Racionales** $P(x,y)/Q(x,y)$: continuos donde $Q \\neq 0$.\n"
              "- **Trigonométricas, exponenciales, logaritmos** aplicados a continuas: continuos donde estén definidos.\n"
              "- **Composición de continuas** es continua: $f(g(x, y), h(x, y))$ es continua si $f, g, h$ lo son."
          )),

        b("ejemplo_resuelto",
          titulo="Continuidad por sustitución",
          problema_md="Calcular $\\lim_{(x,y) \\to (1, 2)} (x^2 + 3xy - y^2)$.",
          pasos=[
              {"accion_md": "$f(x, y) = x^2 + 3xy - y^2$ es **polinomio**, continuo en todo $\\mathbb{R}^2$.",
               "justificacion_md": "Identificación rápida.",
               "es_resultado": False},
              {"accion_md": "**Sustitución directa:** $f(1, 2) = 1 + 6 - 4 = 3$.",
               "justificacion_md": "Para continuas, el límite es solo el valor — sin necesidad de polares ni caminos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Función definida por tramos: continuidad en $(0, 0)$",
          problema_md="¿Es $f(x, y) = \\begin{cases} \\dfrac{x^2 y}{x^2 + y^2} & (x, y) \\neq (0, 0) \\\\ 0 & (x, y) = (0, 0) \\end{cases}$ continua en $(0, 0)$?",
          pasos=[
              {"accion_md": "**Necesitamos verificar:** $\\lim_{(x,y)\\to(0,0)} f(x,y) = f(0, 0) = 0$.",
               "justificacion_md": "El valor en el punto está dado; el límite debe coincidir.",
               "es_resultado": False},
              {"accion_md": "**Por el ejemplo anterior:** $\\lim_{(x,y) \\to (0,0)} \\dfrac{x^2 y}{x^2+y^2} = 0$ (en polares).",
               "justificacion_md": "Reuso del cálculo previo.",
               "es_resultado": False},
              {"accion_md": "$\\lim = 0 = f(0, 0)$. **Sí es continua en $(0, 0)$.**",
               "justificacion_md": "**Lección:** la función racional $x^2 y/(x^2+y^2)$ tiene una singularidad removible en $(0,0)$, y al definir $f(0,0) = 0$ se vuelve continua. Es el análogo 2D de remover una discontinuidad en 1D.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para mostrar que un límite **NO existe** en $(a, b)$, basta:",
                  "opciones_md": [
                      "Encontrar un camino con un valor distinto a $f(a, b)$.",
                      "Encontrar dos caminos con valores distintos.",
                      "Probar todos los caminos posibles.",
                      "Aplicar L'Hôpital.",
                  ],
                  "correcta": "B",
                  "pista_md": "Es asimétrico: probar con dos caminos basta para no existencia, pero no para existencia.",
                  "explicacion_md": (
                      "**Test de los caminos:** dos caminos con valores distintos → el límite no existe. Para existencia, necesitamos polares o cotas, no solo caminos."
                  ),
              },
              {
                  "enunciado_md": "$\\lim_{(x,y) \\to (0,0)} \\dfrac{x^2 - y^2}{x^2 + y^2}$:",
                  "opciones_md": [
                      "Es $0$",
                      "Es $1$",
                      "No existe",
                      "Es $-1$",
                  ],
                  "correcta": "C",
                  "pista_md": "Probar el eje $x$ y el eje $y$ — distintos.",
                  "explicacion_md": (
                      "Eje $x$ ($y = 0$): $x^2/x^2 = 1$. Eje $y$ ($x = 0$): $-y^2/y^2 = -1$. **$1 \\neq -1$, no existe.**"
                  ),
              },
          ]),

        ej(
            titulo="Mostrar no existencia",
            enunciado=(
                "Demuestra que $\\lim_{(x,y) \\to (0,0)} \\dfrac{xy^2}{x^2 + y^4}$ no existe."
            ),
            pistas=[
                "Probar primero ejes y diagonal — quizá te dan el mismo valor.",
                "Si las rectas funcionan, intenta una **parábola**: $x = y^2$.",
            ],
            solucion=(
                "**Eje $x$** ($y = 0$): $0/x^2 = 0$. **Eje $y$** ($x = 0$): $0/y^4 = 0$. **Diagonal** ($y = x$): $x \\cdot x^2/(x^2 + x^4) = x^3/(x^2(1+x^2)) = x/(1+x^2) \\to 0$.\n\n"
                "**Todas las rectas dan $0$, pero el límite igualmente puede no existir.** Probamos $x = y^2$:\n\n"
                "$\\dfrac{y^2 \\cdot y^2}{(y^2)^2 + y^4} = \\dfrac{y^4}{y^4 + y^4} = \\dfrac{1}{2}$.\n\n"
                "**Por la parábola $x = y^2$ el límite es $1/2$**, distinto de $0$ por las rectas. **No existe.**\n\n"
                "**Lección moral:** rectas no son suficientes — siempre considerar parábolas u otras curvas."
            ),
        ),

        ej(
            titulo="Existencia con polares",
            enunciado="Calcula $\\lim_{(x,y) \\to (0,0)} \\dfrac{x^3 + y^3}{x^2 + y^2}$.",
            pistas=[
                "Pasa a polares.",
                "El cociente tendrá un factor $r$ que va a $0$.",
            ],
            solucion=(
                "Polares: $\\dfrac{r^3\\cos^3\\theta + r^3\\sin^3\\theta}{r^2} = r(\\cos^3\\theta + \\sin^3\\theta)$.\n\n"
                "$|r(\\cos^3\\theta + \\sin^3\\theta)| \\leq r \\cdot 2 = 2r \\to 0$.\n\n"
                "**Límite: $0$.** (Existe e independiente de la dirección, gracias al factor $r$ extra.)"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Concluir existencia desde el test de caminos.** Probar $5$ caminos con el mismo valor **no demuestra** existencia. Solo polares + cota o un argumento riguroso lo hacen.",
              "**Olvidar parábolas u otros caminos curvos.** Algunos contraejemplos famosos requieren $y = x^2$, no rectas.",
              "**Aplicar polares sin verificar que el límite es independiente de $\\theta$.** Si depende de $\\theta$, el límite **no existe**.",
              "**Confundir 'continuo en $(a,b)$' con 'definido en $(a,b)$'.** Continua requiere las tres condiciones: definido, límite existe, coinciden.",
              "**Sustituir directamente cuando hay singularidad.** Si la sustitución da $0/0$, hay que analizar el límite con técnicas — no concluir que vale $0$ o que no existe.",
          ]),

        b("resumen",
          puntos_md=[
              "**Límite en varias variables:** definición $\\epsilon$-$\\delta$ con distancia euclidiana.",
              "**Para mostrar NO existencia:** dos caminos con valores distintos.",
              "**Para mostrar existencia:** sustitución directa (continuas), polares con cota, sándwich.",
              "**Test de los caminos** es asimétrico: solo sirve para no existencia.",
              "**Continuidad:** $\\lim f = f(a, b)$, las tres condiciones (definido, existe, coinciden).",
              "**Funciones de fábrica continuas:** polinomios, racionales (donde definidas), trigonométricas, exponenciales, sus composiciones.",
              "**Próximo capítulo:** derivadas parciales — el primer paso de derivación en varias variables.",
          ]),
    ]
    return {
        "id": "lec-mvar-3-2-limites-continuidad",
        "title": "Límites y continuidad",
        "description": "Límites en varias variables: caminos, polares y continuidad. Diferencias clave con el caso 1D.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
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

    chapter_id = "ch-funciones-varias-variables"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Funciones de Varias Variables",
        "description": "Funciones $f(x, y)$ y $f(x, y, z)$: dominio, rango, gráficas, curvas de nivel, límites y continuidad.",
        "order": 3,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_3_1, lesson_3_2]
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
    print(f"✅ Capítulo 3 — Funciones de Varias Variables listo: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
