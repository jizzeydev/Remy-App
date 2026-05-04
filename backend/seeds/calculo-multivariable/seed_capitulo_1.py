"""
Seed del curso Cálculo Multivariable — Capítulo 1: Series y Sucesiones.
8 lecciones reales:
  1.1 Sucesiones
  1.2 Series
  1.3 Pruebas de series
  1.4 Series alternantes
  1.5 Criterios de convergencia (razón y raíz)
  1.6 Series de potencias
  1.7 Representación de funciones
  1.8 Series de Taylor y Maclaurin

Crea el curso si no existe. Idempotente: borra y re-inserta el capítulo y sus lecciones.
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
    "#06b6d4 y ámbar #f59e0b. Sin sombras dramáticas, sin texturas. Apto para "
    "libro universitario."
)


# =====================================================================
# 1.1 Sucesiones
# =====================================================================
def lesson_1_1():
    blocks = [
        b("texto", body_md=(
            "Una **sucesión** es una lista ordenada de números: $a_1, a_2, a_3, \\ldots$. "
            "Más formalmente, es una función con dominio $\\mathbb{N}$. La pregunta central es: "
            "¿hacia dónde 'tiende' la sucesión cuando $n$ crece?\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir **convergencia** $\\lim_{n \\to \\infty} a_n = L$.\n"
            "- Aplicar las **reglas de límites** (linealidad, producto, cociente) a sucesiones.\n"
            "- Reconocer las **sucesiones clásicas** y sus límites.\n"
            "- Aplicar el **teorema del sándwich** y el de **convergencia monótona**."
        )),

        b("intuicion",
          titulo="Sucesión vs función",
          body_md=(
              "Una sucesión $(a_n)$ es como una función $f: \\mathbb{N} \\to \\mathbb{R}$ donde solo se evalúan los enteros positivos. "
              "Eso significa que **muchos resultados de límites de funciones siguen valiendo**, pero hay diferencias:\n\n"
              "- Sin la noción de \"$n$ se acerca a $a$\" — solo $n \\to \\infty$.\n"
              "- Sin continuidad ni derivabilidad estándar (no es función continua).\n\n"
              "**Atajo útil:** si existe una función $f$ continua con $f(n) = a_n$, entonces "
              "$\\lim_{n \\to \\infty} a_n = \\lim_{x \\to \\infty} f(x)$. Eso permite usar L'Hôpital y otras técnicas."
          )),

        b("definicion",
          titulo="Convergencia de una sucesión",
          body_md=(
              "$(a_n)$ **converge** a $L$ si para todo $\\epsilon > 0$ existe $N \\in \\mathbb{N}$ tal que\n\n"
              "$$|a_n - L| < \\epsilon \\quad \\text{para todo } n \\geq N$$\n\n"
              "Notación: $\\lim_{n \\to \\infty} a_n = L$ o $a_n \\to L$.\n\n"
              "Si no existe tal $L$, la sucesión **diverge**. Si $a_n \\to \\pm\\infty$, decimos que diverge a infinito."
          )),

        b("definicion",
          titulo="Reglas de límites de sucesiones",
          body_md=(
              "Si $a_n \\to A$ y $b_n \\to B$ (finitos):\n\n"
              "**Linealidad:** $\\lim(c \\, a_n + d \\, b_n) = cA + dB$.\n\n"
              "**Producto:** $\\lim(a_n b_n) = AB$.\n\n"
              "**Cociente:** $\\lim(a_n / b_n) = A/B$ (si $B \\neq 0$).\n\n"
              "**Función continua:** si $f$ es continua en $A$, $\\lim f(a_n) = f(A)$.\n\n"
              "**Atajo \"función real\":** si $a_n = f(n)$ con $f$ continua y $\\lim_{x \\to \\infty} f(x) = L$, entonces $a_n \\to L$. "
              "Permite usar L'Hôpital."
          )),

        formulas(
            titulo="Sucesiones clásicas y sus límites",
            body=(
                "| Sucesión | Límite |\n|---|---|\n"
                "| $\\dfrac{1}{n}$ | $0$ |\n"
                "| $\\dfrac{1}{n^p}$ ($p > 0$) | $0$ |\n"
                "| $r^n$ ($\\|r\\| < 1$) | $0$ |\n"
                "| $r^n$ ($r = 1$) | $1$ |\n"
                "| $r^n$ ($\\|r\\| > 1$) | diverge ($\\pm \\infty$ o sin límite) |\n"
                "| $\\sqrt[n]{n}$ | $1$ |\n"
                "| $\\sqrt[n]{c}$ ($c > 0$) | $1$ |\n"
                "| $\\dfrac{n^k}{r^n}$ ($r > 1$) | $0$ (exp gana a polinomial) |\n"
                "| $\\dfrac{r^n}{n!}$ | $0$ (factorial gana a exp) |\n"
                "| $\\left(1 + \\dfrac{1}{n}\\right)^n$ | $e$ |\n"
                "| $\\left(1 + \\dfrac{c}{n}\\right)^n$ | $e^c$ |\n\n"
                "**Jerarquía** (de más lento a más rápido en infinito): $\\ln n \\ll n^k \\ll r^n \\ll n! \\ll n^n$."
            ),
        ),

        b("teorema",
          nombre="Teorema del sándwich (squeeze)",
          enunciado_md=(
              "Si $a_n \\leq b_n \\leq c_n$ para $n$ grande y $\\lim a_n = \\lim c_n = L$, entonces $\\lim b_n = L$."
          ),
          demostracion_md=(
              "Dado $\\epsilon > 0$, existe $N$ tal que $|a_n - L| < \\epsilon$ y $|c_n - L| < \\epsilon$ para $n \\geq N$. "
              "Entonces $L - \\epsilon < a_n \\leq b_n \\leq c_n < L + \\epsilon$, así $|b_n - L| < \\epsilon$."
          )),

        b("ejemplo_resuelto",
          titulo="Sándwich con seno acotado",
          problema_md="Calcular $\\lim_{n \\to \\infty} \\dfrac{\\sin n}{n}$.",
          pasos=[
              {"accion_md": "**$\\sin n$ está acotado:** $-1 \\leq \\sin n \\leq 1$. Dividiendo por $n > 0$:\n\n"
                            "$$-\\dfrac{1}{n} \\leq \\dfrac{\\sin n}{n} \\leq \\dfrac{1}{n}$$",
               "justificacion_md": "El acotamiento permite plantear el sándwich.",
               "es_resultado": False},
              {"accion_md": "**Los extremos van a $0$:** $\\lim(-1/n) = \\lim(1/n) = 0$. Por el sándwich, $\\lim \\sin(n)/n = 0$.",
               "justificacion_md": "**Patrón clave:** factor acotado × factor que tiende a $0$ → toda la sucesión tiende a $0$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Convergencia monótona",
          enunciado_md=(
              "Toda sucesión **monótona y acotada** converge. En particular:\n\n"
              "- Si $(a_n)$ es **creciente y acotada superiormente**, converge al supremo de sus términos.\n"
              "- Si es **decreciente y acotada inferiormente**, converge al ínfimo.\n\n"
              "**Importancia:** permite probar convergencia sin saber el valor del límite."
          ),
          demostracion_md=(
              "Por la propiedad del supremo (axioma de los reales). Si $(a_n)$ es creciente y acotada, "
              "$L = \\sup_n a_n$ existe. Para todo $\\epsilon > 0$, $L - \\epsilon$ no es cota superior, así existe $N$ con $a_N > L - \\epsilon$. "
              "Por monotonía, $a_n \\geq a_N > L - \\epsilon$ para $n \\geq N$. Y como $L$ es cota, $a_n \\leq L$. "
              "Entonces $|a_n - L| < \\epsilon$."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicar el atajo \"función real\"",
          problema_md="Calcular $\\lim_{n \\to \\infty} \\dfrac{\\ln n}{n}$.",
          pasos=[
              {"accion_md": "Si $f(x) = \\dfrac{\\ln x}{x}$, entonces $a_n = f(n)$. Calculamos $\\lim_{x \\to \\infty} f(x)$.",
               "justificacion_md": "Convertimos a un límite de función para usar L'Hôpital.",
               "es_resultado": False},
              {"accion_md": "**L'Hôpital** ($\\infty/\\infty$): $\\lim_{x \\to \\infty} \\dfrac{\\ln x}{x} = \\lim_{x \\to \\infty} \\dfrac{1/x}{1} = 0$.",
               "justificacion_md": "Aplicación directa.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{n \\to \\infty} \\dfrac{\\ln n}{n} = 0$.",
               "justificacion_md": "**Confirmación de la jerarquía:** $\\ln n \\ll n$ — el polinomio gana al logaritmo.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "$\\lim_{n \\to \\infty} \\left(1 + \\dfrac{2}{n}\\right)^n = ?$",
                  "opciones_md": ["$1$", "$2$", "$e$", "$e^2$"],
                  "correcta": "D",
                  "pista_md": "Es la forma $(1 + c/n)^n \\to e^c$.",
                  "explicacion_md": (
                      "Patrón clásico: $(1 + c/n)^n \\to e^c$. Aquí $c = 2$, así el límite es $e^2$."
                  ),
              },
              {
                  "enunciado_md": "Una sucesión que es **creciente** y **acotada superiormente** por $5$:",
                  "opciones_md": [
                      "Diverge.",
                      "Converge a algún $L \\leq 5$.",
                      "Converge a $5$ exactamente.",
                      "No se puede saber.",
                  ],
                  "correcta": "B",
                  "pista_md": "Teorema de convergencia monótona.",
                  "explicacion_md": (
                      "Por convergencia monótona, **converge** al supremo de sus términos, que es $\\leq 5$. No tiene por qué alcanzar $5$ exactamente."
                  ),
              },
          ]),

        ej(
            titulo="Sucesión racional",
            enunciado="Calcula $\\lim_{n \\to \\infty} \\dfrac{2n^2 + 3n - 1}{5n^2 - n + 7}$.",
            pistas=[
                "Dividir numerador y denominador por la potencia más alta ($n^2$).",
                "Las potencias inversas tienden a $0$.",
            ],
            solucion=(
                "$$\\dfrac{2n^2 + 3n - 1}{5n^2 - n + 7} = \\dfrac{2 + 3/n - 1/n^2}{5 - 1/n + 7/n^2} \\xrightarrow{n \\to \\infty} \\dfrac{2}{5}$$"
            ),
        ),

        ej(
            titulo="Factorial vs exponencial",
            enunciado="Calcula $\\lim_{n \\to \\infty} \\dfrac{2^n}{n!}$.",
            pistas=[
                "Factorial crece más rápido que cualquier exponencial — anticipa el resultado.",
                "Argumento formal: para $n \\geq 4$, $\\dfrac{2^n}{n!} = \\dfrac{2 \\cdot 2 \\cdots 2}{1 \\cdot 2 \\cdots n}$. Acota cada factor.",
            ],
            solucion=(
                "Para $n \\geq 4$:\n\n"
                "$$\\dfrac{2^n}{n!} = \\dfrac{2}{1} \\cdot \\dfrac{2}{2} \\cdot \\dfrac{2}{3} \\cdot \\dfrac{2}{4} \\cdots \\dfrac{2}{n} \\leq 2 \\cdot 1 \\cdot \\dfrac{2}{3} \\cdot \\left(\\dfrac{2}{4}\\right)^{n-3}$$\n\n"
                "El último factor tiende a $0$ (es $r^{n-3}$ con $r = 1/2$). Por sándwich, $2^n/n! \\to 0$."
            ),
        ),

        fig(
            "Diagrama de dispersión con tres mini-paneles lado a lado, eje horizontal n (entero, "
            "1 a 12), eje vertical a_n. Panel 1 'Convergente': puntos en color teal #06b6d4 que "
            "se acercan a una recta horizontal teal punteada en y = L con etiqueta 'a_n → L'. "
            "Panel 2 'Divergente': puntos en color ámbar #f59e0b creciendo sin cota con flecha "
            "hacia arriba y etiqueta 'a_n → ∞'. Panel 3 'Oscilante': puntos en gris alternando "
            "entre dos niveles (+1 y -1) con etiqueta 'sin límite'. Cada panel con su título "
            "claro arriba. Ejes con marcas. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir 'sucesión acotada' con 'sucesión convergente'.** Acotada no implica convergente: $a_n = (-1)^n$ es acotada pero diverge.",
              "**Aplicar L'Hôpital directo a una sucesión.** Hay que pasar primero a la función continua $f(x)$ con $f(n) = a_n$.",
              "**Confundir $r^n$ con $n^r$.** $r^n$ es exponencial; $n^r$ es polinomial. Crecen muy distinto.",
              "**Olvidar la jerarquía** $\\ln n \\ll n^k \\ll r^n \\ll n!$. Identificar quién \"gana\" facilita muchos cálculos.",
              "**Pensar que $0.999\\ldots \\neq 1$.** Como $a_n = \\sum_{k=1}^n 9/10^k \\to 1$, los \"infinitos nueves\" igualan exactamente $1$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Convergencia** $\\epsilon$-$N$: $|a_n - L| < \\epsilon$ para $n \\geq N$.",
              "**Reglas de límites:** linealidad, producto, cociente, función continua.",
              "**Atajo:** si $a_n = f(n)$ con $f$ continua, usar L'Hôpital sobre $f$.",
              "**Sándwich:** si $a_n \\leq b_n \\leq c_n$ y los extremos convergen al mismo $L$, $b_n \\to L$.",
              "**Convergencia monótona:** monótona + acotada $\\Rightarrow$ converge.",
              "**Jerarquía:** $\\ln n \\ll n^k \\ll r^n \\ll n!$.",
              "**Próxima lección:** sumar infinitos términos — series.",
          ]),
    ]
    return {
        "id": "lec-mvar-1-1-sucesiones",
        "title": "Sucesiones",
        "description": "Convergencia de sucesiones, reglas de límites, sucesiones clásicas y teoremas del sándwich y monótona.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# 1.2 Series
# =====================================================================
def lesson_1_2():
    blocks = [
        b("texto", body_md=(
            "Una **serie** es la suma de los términos de una sucesión: $a_1 + a_2 + a_3 + \\cdots$. "
            "Sumar infinitos términos parece extraño, pero el truco es definir la suma como un **límite "
            "de sumas parciales**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir series mediante sumas parciales y convergencia.\n"
            "- Reconocer y sumar la **serie geométrica**.\n"
            "- Aplicar el criterio de la **serie $p$**.\n"
            "- Usar el **test del término $n$-ésimo** para divergencia.\n"
            "- Aplicar la **linealidad** de las series."
        )),

        b("intuicion",
          titulo="Suma infinita = límite de sumas finitas",
          body_md=(
              "Sumar infinitos números no se puede hacer \"de una vez\". Lo que sí podemos hacer es:\n\n"
              "1. Sumar los primeros $N$ términos: $s_N = a_1 + a_2 + \\cdots + a_N$ (suma parcial).\n"
              "2. Tomar el límite $\\lim_{N \\to \\infty} s_N$.\n\n"
              "Si ese límite existe y es finito, decimos que la serie **converge** y lo llamamos **suma de la serie**. "
              "Si no, **diverge**.\n\n"
              "**Idea clave:** la serie es una sucesión disfrazada — la sucesión de sus sumas parciales."
          )),

        b("definicion",
          titulo="Serie y convergencia",
          body_md=(
              "Sea $(a_n)$ una sucesión. La **serie** $\\sum_{n=1}^{\\infty} a_n$ es el límite de las **sumas parciales**:\n\n"
              "$$s_N = \\sum_{n=1}^{N} a_n = a_1 + a_2 + \\cdots + a_N$$\n\n"
              "Si $\\lim_{N \\to \\infty} s_N = S$ (finito), la serie **converge a $S$**:\n\n"
              "$$\\sum_{n=1}^{\\infty} a_n = S$$\n\n"
              "Si el límite no existe o es $\\pm\\infty$, la serie **diverge**."
          )),

        b("teorema",
          nombre="Serie geométrica",
          enunciado_md=(
              "Para $r$ real:\n\n"
              "$$\\sum_{n=0}^{\\infty} r^n = 1 + r + r^2 + r^3 + \\cdots$$\n\n"
              "**Converge** si $|r| < 1$, con suma $\\dfrac{1}{1-r}$. **Diverge** si $|r| \\geq 1$.\n\n"
              "**Forma con primer término $a$:**\n\n"
              "$$\\sum_{n=0}^{\\infty} a r^n = \\dfrac{a}{1 - r} \\quad \\text{(si } |r| < 1)$$"
          ),
          demostracion_md=(
              "**Suma parcial:** $s_N = 1 + r + \\cdots + r^N$. Multiplicando por $(1-r)$:\n\n"
              "$$(1-r) s_N = 1 - r^{N+1} \\implies s_N = \\dfrac{1 - r^{N+1}}{1 - r} \\quad (r \\neq 1)$$\n\n"
              "Si $|r| < 1$, $r^{N+1} \\to 0$, así $s_N \\to \\dfrac{1}{1-r}$. **Converge.**\n\n"
              "Si $|r| \\geq 1$ (y $r \\neq 1$), $r^{N+1}$ no tiende a $0$, así $s_N$ diverge. Si $r = 1$, $s_N = N+1 \\to \\infty$."
          )),

        b("ejemplo_resuelto",
          titulo="Suma de geométrica",
          problema_md="Calcular $\\sum_{n=0}^{\\infty} \\dfrac{1}{2^n}$.",
          pasos=[
              {"accion_md": "Es geométrica con $r = 1/2$ ($|r| < 1$, así converge) y primer término $a = 1$.\n\n"
                            "$$\\sum_{n=0}^{\\infty} \\dfrac{1}{2^n} = \\dfrac{1}{1 - 1/2} = 2$$",
               "justificacion_md": "**Visualización clásica:** $1 + 1/2 + 1/4 + 1/8 + \\cdots$ — cada término llena la mitad de lo que falta para llegar a $2$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Serie p (Riemann)",
          enunciado_md=(
              "Para $p > 0$:\n\n"
              "$$\\sum_{n=1}^{\\infty} \\dfrac{1}{n^p} \\quad \\text{converge si } p > 1, \\text{ diverge si } p \\leq 1$$\n\n"
              "**Casos especiales:**\n\n"
              "- $p = 1$: **serie armónica** $\\sum 1/n$, **diverge** (sorprendentemente).\n"
              "- $p = 2$: $\\sum 1/n^2 = \\pi^2/6$ (problema de Basilea).\n"
              "- $p = 3$: $\\sum 1/n^3$ converge (valor sin forma cerrada elemental)."
          ),
          demostracion_md=(
              "Por el test de la integral (lección 1.3): $\\int_1^\\infty 1/x^p \\, dx$ converge $\\iff p > 1$ (criterio $p$ de impropias). "
              "La conexión integral-serie traslada el resultado."
          )),

        b("teorema",
          nombre="Test de divergencia (término $n$-ésimo)",
          enunciado_md=(
              "Si $\\sum a_n$ converge, entonces $\\lim_{n \\to \\infty} a_n = 0$.\n\n"
              "**Contrapositiva (uso práctico):** si $\\lim a_n \\neq 0$ (o no existe), entonces $\\sum a_n$ **diverge**.\n\n"
              "**Cuidado:** $a_n \\to 0$ **NO** garantiza convergencia. La serie armónica $\\sum 1/n$ tiene $a_n = 1/n \\to 0$ y aún así diverge."
          ),
          demostracion_md=(
              "Si $\\sum a_n = S$, entonces $s_N \\to S$ y $s_{N-1} \\to S$. Pero $a_N = s_N - s_{N-1} \\to S - S = 0$."
          )),

        b("ejemplo_resuelto",
          titulo="Test de divergencia: $\\sum \\dfrac{n}{n+1}$",
          problema_md="Determinar si converge.",
          pasos=[
              {"accion_md": "$\\lim_{n \\to \\infty} \\dfrac{n}{n+1} = 1 \\neq 0$. Por el **test del término $n$-ésimo, diverge**.",
               "justificacion_md": "**Atajo útil:** mirar primero si el término general tiende a $0$. Si no, ya divergió y no hace falta más análisis.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Linealidad de series",
          body_md=(
              "Si $\\sum a_n = A$ y $\\sum b_n = B$ (ambas convergen):\n\n"
              "$$\\sum (c \\, a_n + d \\, b_n) = c A + d B$$\n\n"
              "para cualesquiera constantes $c, d$.\n\n"
              "**Atención:** si una de las dos diverge y la otra converge, la suma diverge. "
              "Si ambas divergen, no se puede afirmar nada con esta regla."
          )),

        b("ejemplo_resuelto",
          titulo="Combinar geométricas",
          problema_md="Calcular $\\sum_{n=0}^{\\infty} \\left(\\dfrac{2}{3^n} - \\dfrac{1}{4^n}\\right)$.",
          pasos=[
              {"accion_md": "**Por linealidad:**\n\n$$2 \\sum \\dfrac{1}{3^n} - \\sum \\dfrac{1}{4^n}$$",
               "justificacion_md": "Las dos series son geométricas y convergen.",
               "es_resultado": False},
              {"accion_md": "$\\sum_{n=0}^\\infty (1/3)^n = \\dfrac{1}{1 - 1/3} = \\dfrac{3}{2}$. $\\sum_{n=0}^\\infty (1/4)^n = \\dfrac{1}{1 - 1/4} = \\dfrac{4}{3}$.",
               "justificacion_md": "Aplicación de la fórmula geométrica.",
               "es_resultado": False},
              {"accion_md": "$$2 \\cdot \\dfrac{3}{2} - \\dfrac{4}{3} = 3 - \\dfrac{4}{3} = \\dfrac{5}{3}$$",
               "justificacion_md": "Combinación final.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Serie telescópica",
          problema_md="Calcular $\\sum_{n=1}^{\\infty} \\dfrac{1}{n(n+1)}$.",
          pasos=[
              {"accion_md": "**Fracciones parciales:** $\\dfrac{1}{n(n+1)} = \\dfrac{1}{n} - \\dfrac{1}{n+1}$.",
               "justificacion_md": "Descomposición clásica que produce telescopia.",
               "es_resultado": False},
              {"accion_md": "**Suma parcial:**\n\n$$s_N = \\sum_{n=1}^{N}\\left(\\dfrac{1}{n} - \\dfrac{1}{n+1}\\right) = 1 - \\dfrac{1}{N+1}$$",
               "justificacion_md": "Los términos intermedios se **cancelan en cascada** (telescópica): $1 - 1/2 + 1/2 - 1/3 + \\cdots = 1 - 1/(N+1)$.",
               "es_resultado": False},
              {"accion_md": "$\\lim_{N \\to \\infty} s_N = 1 - 0 = 1$. La serie **converge a $1$**.",
               "justificacion_md": "**Truco poderoso:** las series telescópicas se pueden sumar exactamente — una de las pocas técnicas que da una respuesta cerrada.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los criterios:",
          preguntas=[
              {
                  "enunciado_md": "¿La serie $\\sum_{n=1}^\\infty \\dfrac{1}{n}$ (armónica)?",
                  "opciones_md": [
                      "Converge porque $1/n \\to 0$.",
                      "Diverge a $\\infty$.",
                      "Converge a $\\ln 2$.",
                      "Converge a $1$.",
                  ],
                  "correcta": "B",
                  "pista_md": "Sí, $1/n \\to 0$, pero eso no es suficiente para convergencia. La serie $p$ con $p = 1$ diverge.",
                  "explicacion_md": (
                      "**La armónica es famosa:** los términos van a $0$, pero la suma diverge a infinito. Es el contraejemplo clásico al malentendido $a_n \\to 0 \\Rightarrow$ converge."
                  ),
              },
              {
                  "enunciado_md": "$\\sum_{n=1}^\\infty 0.7^n = ?$",
                  "opciones_md": [
                      "Diverge.",
                      "$\\dfrac{1}{0.3}$",
                      "$\\dfrac{0.7}{0.3} = \\dfrac{7}{3}$",
                      "$0$",
                  ],
                  "correcta": "C",
                  "pista_md": "Geométrica con $r = 0.7$, **empezando en $n = 1$**: primer término $a = 0.7$.",
                  "explicacion_md": (
                      "$\\sum_{n=1}^\\infty 0.7^n = 0.7 + 0.49 + \\ldots = \\dfrac{0.7}{1 - 0.7} = \\dfrac{0.7}{0.3} = 7/3$. **Cuidado con el índice inicial.**"
                  ),
              },
          ]),

        ej(
            titulo="Geométrica con índice no estándar",
            enunciado="Calcula $\\sum_{n=2}^{\\infty} \\dfrac{3}{4^n}$.",
            pistas=[
                "Reescribe extrayendo factores: $\\sum_{n=2}^\\infty \\dfrac{3}{4^n} = 3 \\sum_{n=2}^\\infty \\dfrac{1}{4^n}$.",
                "$\\sum_{n=2}^\\infty (1/4)^n = \\sum_{n=0}^\\infty (1/4)^n - 1 - 1/4$, o directamente: primer término $1/16$, razón $1/4$.",
            ],
            solucion=(
                "Geométrica con primer término $a = 1/16$ y razón $r = 1/4$:\n\n"
                "$$\\sum_{n=2}^\\infty (1/4)^n = \\dfrac{1/16}{1 - 1/4} = \\dfrac{1/16}{3/4} = \\dfrac{1}{12}$$\n\n"
                "Multiplicando por $3$: $\\dfrac{3}{12} = \\dfrac{1}{4}$."
            ),
        ),

        ej(
            titulo="Telescópica con logaritmos",
            enunciado="Determina si $\\sum_{n=1}^\\infty \\ln\\left(\\dfrac{n+1}{n}\\right)$ converge.",
            pistas=[
                "$\\ln\\left(\\dfrac{n+1}{n}\\right) = \\ln(n+1) - \\ln n$. Telescópica.",
                "Suma parcial: $\\ln(N+1) - \\ln 1 = \\ln(N+1)$.",
            ],
            solucion=(
                "$s_N = \\sum_{n=1}^N [\\ln(n+1) - \\ln n] = \\ln(N+1)$ (telescópica).\n\n"
                "$\\lim_{N \\to \\infty} \\ln(N+1) = +\\infty$. **Diverge.**"
            ),
        ),

        fig(
            "Dos paneles lado a lado. Panel izquierdo (a) 'Sumas parciales': eje horizontal n, "
            "eje vertical S_n. Puntos en color teal #06b6d4 que se acercan a una recta horizontal "
            "teal punteada en y = S, con etiqueta 'S_n → S'. Panel derecho (b) 'Serie geométrica "
            "como áreas': un cuadrado grande de lado 1 dividido en regiones; la mitad inferior "
            "sombreada en teal (área 1/2), arriba la mitad de esa mitad en ámbar #f59e0b (1/4), "
            "luego 1/8 en teal claro, 1/16 en ámbar claro, etc. Etiqueta '1/2 + 1/4 + 1/8 + ⋯ = 1'. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir 'serie' con 'sucesión'.** La sucesión es la lista de términos $(a_n)$; la serie es la suma $\\sum a_n$.",
              "**Aplicar el test del término $n$-ésimo al revés:** $a_n \\to 0$ **NO** implica convergencia. La armónica es el contraejemplo.",
              "**Olvidar el índice inicial** al sumar geométricas. La fórmula $a/(1-r)$ asume primer término $a$, no necesariamente $1$.",
              "**Sumar series divergentes 'por linealidad'.** La regla solo aplica si ambas convergen.",
              "**No reconocer telescópicas:** muchas series con denominador $n(n+1)$, $(n-1)(n+1)$, etc., admiten descomposición que produce cancelaciones.",
          ]),

        b("resumen",
          puntos_md=[
              "**Serie:** $\\sum a_n = \\lim_{N \\to \\infty} s_N$ donde $s_N = \\sum_{n=1}^N a_n$.",
              "**Geométrica** $\\sum r^n$: converge $\\iff |r| < 1$, suma $a/(1-r)$.",
              "**Serie $p$** $\\sum 1/n^p$: converge $\\iff p > 1$.",
              "**Test del término $n$-ésimo:** si $a_n \\not\\to 0$, diverge. Recíproca falsa.",
              "**Linealidad** y **telescópicas** son herramientas exactas cuando aplican.",
              "**Próxima lección:** pruebas de convergencia para series positivas (integral, comparación).",
          ]),
    ]
    return {
        "id": "lec-mvar-1-2-series",
        "title": "Series",
        "description": "Sumas parciales, convergencia, serie geométrica, serie p, test del término n-ésimo y linealidad.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# =====================================================================
# 1.3 Pruebas de series
# =====================================================================
def lesson_1_3():
    blocks = [
        b("texto", body_md=(
            "La mayoría de las series **no se pueden sumar exactamente**, pero todavía se puede determinar "
            "si **convergen o divergen**. Para series con términos no negativos, hay tres pruebas básicas: "
            "**integral**, **comparación directa** y **comparación de límites**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar el **test de la integral** para series cuya función asociada sea integrable.\n"
            "- Aplicar la **comparación directa** con series conocidas (geométricas, p).\n"
            "- Aplicar la **comparación de límites** cuando la directa es difícil."
        )),

        b("teorema",
          nombre="Test de la integral",
          enunciado_md=(
              "Sea $f$ una función **continua, positiva y decreciente** en $[N, \\infty)$, y $a_n = f(n)$. Entonces:\n\n"
              "$$\\sum_{n=N}^{\\infty} a_n \\quad \\text{converge} \\iff \\int_N^{\\infty} f(x) \\, dx \\quad \\text{converge}$$\n\n"
              "**Importante:** la suma de la serie y la integral **no son iguales** — solo comparten convergencia/divergencia."
          ),
          demostracion_md=(
              "Por monotonía de $f$, $a_{n+1} \\leq f(x) \\leq a_n$ en $[n, n+1]$. Integrando:\n\n"
              "$$a_{n+1} \\leq \\int_n^{n+1} f \\, dx \\leq a_n$$\n\n"
              "Sumando para $n = N, N+1, \\ldots$, las cotas inferior y superior comparan la serie con la integral. "
              "Si una converge, la otra también."
          )),

        b("ejemplo_resuelto",
          titulo="Test de la integral en $\\sum 1/(n \\ln n)$",
          problema_md="Determinar convergencia.",
          pasos=[
              {"accion_md": "$f(x) = \\dfrac{1}{x \\ln x}$ es continua, positiva y decreciente para $x \\geq 2$. Aplicamos el test.",
               "justificacion_md": "Verificamos las hipótesis primero.",
               "es_resultado": False},
              {"accion_md": "**Integral:** $\\int_2^\\infty \\dfrac{1}{x \\ln x} \\, dx$. Sustitución $u = \\ln x$, $du = dx/x$:\n\n"
                            "$$\\int_{\\ln 2}^\\infty \\dfrac{1}{u} \\, du = \\lim_{T \\to \\infty}[\\ln u]_{\\ln 2}^T = +\\infty$$",
               "justificacion_md": "Diverge.",
               "es_resultado": False},
              {"accion_md": "Por el test, $\\sum_{n=2}^\\infty \\dfrac{1}{n \\ln n}$ **diverge**.",
               "justificacion_md": "**Lección notable:** $1/(n \\ln n)$ va a $0$ más rápido que $1/n$, pero aún así suma divergencia. La armónica generalizada con factor logarítmico necesita más para converger.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Comparación directa",
          enunciado_md=(
              "Sean $a_n, b_n \\geq 0$ con $a_n \\leq b_n$ para todo $n$ grande.\n\n"
              "- Si $\\sum b_n$ **converge**, entonces $\\sum a_n$ **converge**.\n"
              "- Si $\\sum a_n$ **diverge**, entonces $\\sum b_n$ **diverge**.\n\n"
              "**En palabras:** si una serie con términos más grandes converge, las más chicas también. Si las más chicas divergen, las más grandes también."
          ),
          demostracion_md=(
              "Las sumas parciales de $\\sum a_n$ son crecientes (todos $a_n \\geq 0$) y acotadas por $\\sum b_n$ (finita). "
              "Por convergencia monótona, $\\sum a_n$ converge. La otra dirección es contrapositiva."
          )),

        b("ejemplo_resuelto",
          titulo="Comparación directa: $\\sum \\dfrac{1}{n^2 + n}$",
          problema_md="Determinar convergencia.",
          pasos=[
              {"accion_md": "**Comparar con $\\sum 1/n^2$** (converge, serie $p$ con $p = 2$):\n\n"
                            "$$\\dfrac{1}{n^2 + n} \\leq \\dfrac{1}{n^2}$$",
               "justificacion_md": "El denominador es más grande, así la fracción es más chica.",
               "es_resultado": False},
              {"accion_md": "Como $\\sum 1/n^2$ converge y $\\dfrac{1}{n^2 + n} \\leq \\dfrac{1}{n^2}$, por comparación directa **$\\sum 1/(n^2+n)$ converge**.",
               "justificacion_md": "Aplicación clásica.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Comparación de límites",
          enunciado_md=(
              "Sean $a_n, b_n > 0$ y $\\lim_{n \\to \\infty} \\dfrac{a_n}{b_n} = c$.\n\n"
              "- Si $0 < c < \\infty$, ambas series tienen el **mismo comportamiento** (ambas convergen o ambas divergen).\n"
              "- Si $c = 0$ y $\\sum b_n$ converge, $\\sum a_n$ converge.\n"
              "- Si $c = \\infty$ y $\\sum b_n$ diverge, $\\sum a_n$ diverge.\n\n"
              "**Idea:** si $a_n \\sim c \\, b_n$ asintóticamente, las series son \"equivalentes\" para convergencia."
          ),
          demostracion_md=(
              "Si $0 < c < \\infty$: para $n$ grande, $\\dfrac{c}{2} b_n \\leq a_n \\leq \\dfrac{3c}{2} b_n$. "
              "Aplicando comparación directa en ambas direcciones, las dos series tienen el mismo comportamiento."
          )),

        b("ejemplo_resuelto",
          titulo="Comparación de límites: $\\sum \\dfrac{2n+1}{n^3 + 5}$",
          problema_md="Determinar convergencia.",
          pasos=[
              {"accion_md": "**Comportamiento asintótico:** numerador $\\sim 2n$, denominador $\\sim n^3$, así $a_n \\sim 2n/n^3 = 2/n^2$.\n\n"
                            "Comparamos con $b_n = 1/n^2$ (serie $p$ con $p = 2$, converge).",
               "justificacion_md": "Identificar a qué se parece el término general en infinito.",
               "es_resultado": False},
              {"accion_md": "**Cociente:**\n\n$$\\lim_{n \\to \\infty} \\dfrac{(2n+1)/(n^3+5)}{1/n^2} = \\lim \\dfrac{n^2 (2n+1)}{n^3+5} = \\lim \\dfrac{2n^3 + n^2}{n^3 + 5} = 2$$",
               "justificacion_md": "Cociente de polinomios al infinito con grados iguales.",
               "es_resultado": False},
              {"accion_md": "$c = 2 \\in (0, \\infty)$ y $\\sum 1/n^2$ converge, así $\\sum (2n+1)/(n^3+5)$ **converge** también.",
               "justificacion_md": "**Lección general:** la comparación de límites es ideal para series racionales (cocientes de polinomios). Solo importa la \"parte dominante\".",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Cuál prueba usar",
          body_md=(
              "**Test de la integral:** cuando $a_n = f(n)$ con $f$ integrable. Útil con $1/n^p$, $1/(n \\ln n)$, etc.\n\n"
              "**Comparación directa:** cuando es fácil acotar arriba o abajo por algo conocido.\n\n"
              "**Comparación de límites:** cuando la asintótica es clara pero la cota directa requiere álgebra. **La más práctica para racionales.**\n\n"
              "**Pista común:** identifica los términos dominantes. $\\dfrac{P(n)}{Q(n)}$ se compara con $1/n^{q-p}$ donde $p, q$ son los grados."
          )),

        b("verificacion",
          intro_md="Verifica las pruebas:",
          preguntas=[
              {
                  "enunciado_md": "$\\sum_{n=1}^\\infty \\dfrac{n}{n^4 + 1}$:",
                  "opciones_md": [
                      "Diverge.",
                      "Converge (compara con $\\sum 1/n^3$).",
                      "Converge (compara con $\\sum 1/n$).",
                      "No se puede determinar.",
                  ],
                  "correcta": "B",
                  "pista_md": "Asintóticamente $n/n^4 = 1/n^3$. Serie $p$ con $p = 3$.",
                  "explicacion_md": (
                      "$\\dfrac{n}{n^4+1} \\sim \\dfrac{1}{n^3}$. Comparación de límites con $b_n = 1/n^3$ da $c = 1 > 0$, así ambas convergen ($p = 3 > 1$)."
                  ),
              },
              {
                  "enunciado_md": "Si $a_n \\leq 1/n^2$ para todo $n$ grande, entonces $\\sum a_n$:",
                  "opciones_md": [
                      "Converge.",
                      "Diverge.",
                      "No se puede determinar sin saber si $a_n \\geq 0$.",
                      "Es constante.",
                  ],
                  "correcta": "C",
                  "pista_md": "La comparación directa requiere $a_n \\geq 0$.",
                  "explicacion_md": (
                      "La hipótesis del test es **$a_n \\geq 0$**. Si $a_n$ pudiera ser negativo, el argumento falla. Hay que afirmar primero la no-negatividad."
                  ),
              },
          ]),

        ej(
            titulo="Test de la integral",
            enunciado="¿Converge $\\sum_{n=1}^\\infty \\dfrac{1}{n^2 + 1}$?",
            pistas=[
                "$f(x) = 1/(x^2+1)$ es continua, positiva, decreciente para $x \\geq 1$.",
                "$\\int 1/(x^2+1) \\, dx = \\arctan x$.",
            ],
            solucion=(
                "$\\int_1^\\infty \\dfrac{1}{x^2+1} \\, dx = [\\arctan x]_1^\\infty = \\dfrac{\\pi}{2} - \\dfrac{\\pi}{4} = \\dfrac{\\pi}{4}$ (finita).\n\n"
                "Por el test de la integral, **la serie converge**. (Aunque su suma exacta no es trivial — el test nos da convergencia, no el valor.)"
            ),
        ),

        ej(
            titulo="Comparación de límites con raíz",
            enunciado="¿Converge $\\sum_{n=1}^\\infty \\dfrac{1}{\\sqrt{n^3 + 2n}}$?",
            pistas=[
                "$\\sqrt{n^3 + 2n} \\sim \\sqrt{n^3} = n^{3/2}$.",
                "Compara con $b_n = 1/n^{3/2}$ (serie $p$, $p = 3/2 > 1$).",
            ],
            solucion=(
                "$$\\lim_{n \\to \\infty} \\dfrac{1/\\sqrt{n^3+2n}}{1/n^{3/2}} = \\lim \\dfrac{n^{3/2}}{\\sqrt{n^3 + 2n}} = \\lim \\dfrac{1}{\\sqrt{1 + 2/n^2}} = 1$$\n\n"
                "$c = 1 > 0$ y $\\sum 1/n^{3/2}$ converge ($p > 1$), así **la serie converge**."
            ),
        ),

        fig(
            "Árbol de decisión horizontal para elegir prueba de convergencia de series. Nodo "
            "raíz teal #06b6d4 con etiqueta '∑ a_n con a_n ≥ 0'. Cuatro ramas hacia la derecha "
            "etiquetadas: (1) 'Test de divergencia (a_n → 0?)' con mini-ejemplo '∑ n/(n+1) "
            "diverge'. (2) 'Test de la integral' en ámbar #f59e0b con mini-ejemplo '∑ 1/n ↔ "
            "∫ 1/x dx'. (3) 'Comparación directa' con '∑ 1/(n²+1) ≤ ∑ 1/n²'. (4) 'Comparación "
            "al límite' con '∑ 1/√(n³+2n) ~ ∑ 1/n^(3/2)'. Cada hoja en cajita redondeada. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar verificar las hipótesis del test de la integral** (continuidad, positividad, decrecimiento).",
              "**Aplicar comparación a series con términos negativos.** Las pruebas básicas asumen $a_n \\geq 0$.",
              "**Comparar con la serie equivocada.** Si $a_n \\sim 1/n$, comparar con $1/n^2$ da $c = 0$ y no se concluye.",
              "**Confundir $\\sum a_n$ con $\\int f$.** Comparten convergencia/divergencia, pero los valores son distintos.",
              "**No identificar el término dominante.** Para racionales, identificar los grados antes de plantear la comparación.",
          ]),

        b("resumen",
          puntos_md=[
              "**Test de la integral:** $\\sum f(n)$ converge $\\iff \\int f \\, dx$ converge (con hipótesis).",
              "**Comparación directa:** acotar arriba o abajo por una serie conocida.",
              "**Comparación de límites:** $\\lim a_n/b_n = c \\in (0, \\infty)$ → mismo comportamiento.",
              "**Series de referencia:** geométrica, $p$, telescópicas.",
              "**Para racionales:** comparar con $1/n^{q-p}$ donde $p, q$ son los grados de num y den.",
              "**Próxima lección:** series alternantes — los signos cambian, lo que abre nuevas técnicas.",
          ]),
    ]
    return {
        "id": "lec-mvar-1-3-pruebas-series",
        "title": "Pruebas de series",
        "description": "Tests de convergencia para series positivas: integral, comparación directa y comparación de límites.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 1.4 Series alternantes
# =====================================================================
def lesson_1_4():
    blocks = [
        b("texto", body_md=(
            "Una **serie alternante** tiene términos que cambian de signo en cada paso: "
            "$\\sum (-1)^n a_n$ con $a_n > 0$. La alternancia hace que las cancelaciones aceleren la "
            "convergencia, así muchas series alternantes convergen mientras que sus análogas positivas no.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar el **test de Leibniz** para series alternantes.\n"
            "- **Estimar el residuo** después de cortar la serie.\n"
            "- Distinguir convergencia **absoluta** de **condicional**."
        )),

        b("teorema",
          nombre="Test de Leibniz (series alternantes)",
          enunciado_md=(
              "Sea $\\sum_{n=1}^\\infty (-1)^{n-1} a_n$ con $a_n > 0$. Si:\n\n"
              "1. $a_n$ es **decreciente** ($a_{n+1} \\leq a_n$ para $n$ grande).\n"
              "2. $\\lim_{n \\to \\infty} a_n = 0$.\n\n"
              "Entonces la serie **converge**."
          ),
          demostracion_md=(
              "Las sumas parciales pares $s_{2N}$ son crecientes y acotadas (por $s_2$); las impares $s_{2N+1}$ son decrecientes y acotadas. "
              "Ambas convergen al mismo límite porque $|s_{N+1} - s_N| = a_{N+1} \\to 0$."
          )),

        b("ejemplo_resuelto",
          titulo="Serie armónica alternante",
          problema_md="Determinar si $\\sum_{n=1}^\\infty \\dfrac{(-1)^{n-1}}{n} = 1 - \\dfrac{1}{2} + \\dfrac{1}{3} - \\dfrac{1}{4} + \\cdots$ converge.",
          pasos=[
              {"accion_md": "$a_n = 1/n$. **Verificamos:**\n\n"
                            "(1) Decreciente: $1/(n+1) < 1/n$. ✓\n"
                            "(2) $\\lim 1/n = 0$. ✓",
               "justificacion_md": "Las dos hipótesis de Leibniz se cumplen.",
               "es_resultado": False},
              {"accion_md": "Por el test de Leibniz, **converge**. (De hecho, su suma es $\\ln 2 \\approx 0.693$.)",
               "justificacion_md": "**Contraste:** la armónica $\\sum 1/n$ diverge, pero la alternante converge. La alternancia permite cancelaciones que la salvan.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Estimación del residuo (Leibniz)",
          enunciado_md=(
              "Si $\\sum (-1)^{n-1} a_n$ satisface las hipótesis del test de Leibniz y $S$ es la suma exacta, "
              "entonces el **error** al truncar en la suma parcial $s_N$ está acotado por:\n\n"
              "$$|S - s_N| \\leq a_{N+1}$$\n\n"
              "Es decir, **el error es menor o igual al primer término que se omite**."
          ),
          demostracion_md=(
              "El residuo $R_N = S - s_N = \\sum_{n=N+1}^\\infty (-1)^{n-1} a_n$ es a su vez una serie alternante de Leibniz con primer término $a_{N+1}$. "
              "Por la propiedad de las sumas parciales acotadas entre dos consecutivas, $|R_N| \\leq a_{N+1}$."
          )),

        b("ejemplo_resuelto",
          titulo="Estimar la suma de la armónica alternante",
          problema_md=(
              "Aproximar $S = \\sum_{n=1}^\\infty \\dfrac{(-1)^{n-1}}{n}$ con error menor que $0.01$."
          ),
          pasos=[
              {"accion_md": "**Necesitamos** $a_{N+1} = 1/(N+1) < 0.01 \\implies N+1 > 100 \\implies N \\geq 100$.",
               "justificacion_md": "Aplicación directa del teorema de estimación.",
               "es_resultado": False},
              {"accion_md": "**Suma parcial $s_{100}$:**\n\n$$s_{100} = 1 - \\dfrac{1}{2} + \\dfrac{1}{3} - \\cdots - \\dfrac{1}{100} \\approx 0.6882$$\n\n"
                            "El verdadero valor es $\\ln 2 \\approx 0.6931$, así el error es $\\approx 0.005 < 0.01$. ✓",
               "justificacion_md": "**Lección:** las series alternantes convergen lentamente — necesitamos $100$ términos para 2 decimales. Por eso se usan principalmente para estimaciones, no cálculos exactos.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Convergencia absoluta vs condicional",
          body_md=(
              "Sea $\\sum a_n$ una serie cualquiera (no necesariamente alternante).\n\n"
              "**Converge absolutamente** si $\\sum |a_n|$ converge.\n\n"
              "**Converge condicionalmente** si $\\sum a_n$ converge pero $\\sum |a_n|$ diverge.\n\n"
              "**Hecho clave:** convergencia absoluta $\\Rightarrow$ convergencia. Pero la recíproca falla — la armónica alternante converge condicionalmente."
          )),

        b("teorema",
          nombre="Convergencia absoluta",
          enunciado_md=(
              "Si $\\sum |a_n|$ converge, entonces $\\sum a_n$ converge.\n\n"
              "**En palabras:** si la serie de valores absolutos converge, la serie original también."
          ),
          demostracion_md=(
              "Sea $a_n^+ = \\max(a_n, 0)$ y $a_n^- = \\max(-a_n, 0)$. Entonces $0 \\leq a_n^\\pm \\leq |a_n|$ y $a_n = a_n^+ - a_n^-$. "
              "Por comparación, $\\sum a_n^\\pm$ convergen. Por linealidad, $\\sum a_n = \\sum a_n^+ - \\sum a_n^-$ converge."
          )),

        b("ejemplo_resuelto",
          titulo="Distinguir absoluta vs condicional: $\\sum (-1)^{n-1}/n^2$",
          problema_md="Estudiar el tipo de convergencia.",
          pasos=[
              {"accion_md": "**Serie de valores absolutos:** $\\sum |(-1)^{n-1}/n^2| = \\sum 1/n^2$ converge (serie $p$ con $p = 2$).",
               "justificacion_md": "Reducimos al criterio absoluto.",
               "es_resultado": False},
              {"accion_md": "Como $\\sum 1/n^2$ converge, **$\\sum (-1)^{n-1}/n^2$ converge absolutamente.**",
               "justificacion_md": "**Comparación con la armónica alternante:** esa converge **condicionalmente** porque $\\sum 1/n$ diverge. La diferencia: aquí $1/n^2$ decae lo suficientemente rápido.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="¿Por qué importa la distinción?",
          body_md=(
              "Las series **absolutamente convergentes** se comportan como sumas finitas: se pueden **reordenar** sin cambiar la suma.\n\n"
              "Las **condicionalmente convergentes** son extrañas: el **teorema de Riemann** dice que reordenando los términos se puede obtener cualquier suma — incluso $+\\infty$ o $-\\infty$.\n\n"
              "**Ejemplo dramático:** la armónica alternante converge a $\\ln 2$. Pero reordenando $(1 - 1/2 - 1/4) + (1/3 - 1/6 - 1/8) + \\cdots$ se obtiene $\\dfrac{1}{2} \\ln 2$. **Misma suma de los mismos términos**, ordenados distinto, **dan resultados distintos**."
          )),

        b("verificacion",
          intro_md="Verifica los conceptos:",
          preguntas=[
              {
                  "enunciado_md": "$\\sum_{n=1}^\\infty \\dfrac{(-1)^n}{\\sqrt{n}}$:",
                  "opciones_md": [
                      "Diverge.",
                      "Converge absolutamente.",
                      "Converge condicionalmente.",
                      "No se puede determinar.",
                  ],
                  "correcta": "C",
                  "pista_md": "Por Leibniz converge. ¿Y la serie de valores absolutos?",
                  "explicacion_md": (
                      "Por Leibniz: $1/\\sqrt{n}$ decreciente, $\\to 0$ → **converge**. Pero $\\sum 1/\\sqrt{n} = \\sum 1/n^{1/2}$ diverge ($p = 1/2 \\leq 1$). Así, **converge condicionalmente**."
                  ),
              },
              {
                  "enunciado_md": "Si una serie converge absolutamente, ¿se puede reordenar?",
                  "opciones_md": [
                      "Sí, sin cambiar la suma.",
                      "No, nunca.",
                      "Sí, pero la suma puede cambiar.",
                      "Solo si los términos son positivos.",
                  ],
                  "correcta": "A",
                  "pista_md": "Las absolutamente convergentes se comportan como sumas finitas.",
                  "explicacion_md": (
                      "**Las absolutas son robustas a reordenamiento.** Las **condicionalmente convergentes** no — Riemann mostró que se puede manipular el orden para obtener cualquier suma."
                  ),
              },
          ]),

        ej(
            titulo="Estimación con error",
            enunciado=(
                "Aproxima $\\sum_{n=1}^\\infty \\dfrac{(-1)^{n-1}}{n^3}$ con error menor que $0.001$. "
                "¿Cuántos términos necesitas?"
            ),
            pistas=[
                "$|R_N| \\leq a_{N+1} = 1/(N+1)^3$.",
                "Resolver $1/(N+1)^3 < 0.001 \\implies (N+1)^3 > 1000$.",
            ],
            solucion=(
                "$1/(N+1)^3 < 0.001 \\implies (N+1)^3 > 1000 \\implies N+1 > 10 \\implies N \\geq 10$.\n\n"
                "**Bastan $10$ términos.** $s_{10} = 1 - 1/8 + 1/27 - 1/64 + \\cdots \\approx 0.9015$ (la suma exacta es $\\eta(3) \\approx 0.9016$). El error es del orden de $10^{-3}$ como prometido."
            ),
        ),

        ej(
            titulo="Convergencia absoluta o condicional",
            enunciado="Clasifica la convergencia de $\\sum_{n=1}^\\infty (-1)^n \\cdot \\dfrac{n}{n^2 + 1}$.",
            pistas=[
                "Por Leibniz: $a_n = n/(n^2+1)$ ¿es decreciente y → 0?",
                "Para $\\sum |a_n| = \\sum n/(n^2+1)$, comparar con $1/n$.",
            ],
            solucion=(
                "**Por Leibniz:** $a_n = n/(n^2+1) \\to 0$ (numerador grado 1, denominador grado 2). Decreciente para $n \\geq 1$ (verificar derivando $f(x) = x/(x^2+1)$: $f'(x) = (1-x^2)/(x^2+1)^2 < 0$ para $x > 1$). **Converge.**\n\n"
                "**Absoluta?** $\\sum n/(n^2+1) \\sim \\sum 1/n$, diverge por comparación de límites.\n\n"
                "**Conclusión: converge condicionalmente.**"
            ),
        ),

        fig(
            "Gráfico de las sumas parciales S_n de una serie alternante. Eje horizontal n (1 a "
            "10), eje vertical S_n. Recta horizontal punteada teal #06b6d4 en y = L marcando el "
            "límite. Los puntos S_n oscilan alrededor de L, con S_1 lejos arriba, S_2 abajo, "
            "S_3 más cerca arriba, etc., acercándose a L. Dos líneas horizontales tenues "
            "ámbar #f59e0b en y = L + a_(n+1) y y = L - a_(n+1) marcando la cota del error, "
            "con flecha doble vertical etiquetada '|S − S_n| ≤ a_(n+1)'. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Leibniz sin verificar que $a_n$ sea decreciente.** Si oscila, Leibniz no aplica.",
              "**Confundir el residuo con el término $N$-ésimo.** $|R_N| \\leq a_{N+1}$ — el **siguiente** después de cortar.",
              "**Asumir que toda alternante converge absolutamente.** Muchas convergen solo condicionalmente.",
              "**Reordenar series condicionalmente convergentes** sin avisar — cambia la suma.",
              "**Olvidar verificar $\\lim a_n = 0$** en Leibniz. Si $a_n \\not\\to 0$, ya diverge por el test del término $n$-ésimo.",
          ]),

        b("resumen",
          puntos_md=[
              "**Leibniz:** alternante con $a_n$ decreciente y $\\to 0$ → converge.",
              "**Estimación del residuo:** $|S - s_N| \\leq a_{N+1}$.",
              "**Convergencia absoluta:** $\\sum |a_n|$ converge → $\\sum a_n$ converge.",
              "**Condicional:** $\\sum a_n$ converge pero $\\sum |a_n|$ diverge.",
              "**Reordenamiento:** seguro en absolutas, peligroso en condicionales.",
              "**Próxima lección:** criterios de razón y raíz — para series con factoriales y exponenciales.",
          ]),
    ]
    return {
        "id": "lec-mvar-1-4-alternantes",
        "title": "Series alternantes",
        "description": "Test de Leibniz, estimación del residuo y distinción entre convergencia absoluta y condicional.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# 1.5 Criterios de convergencia (razón y raíz)
# =====================================================================
def lesson_1_5():
    blocks = [
        b("texto", body_md=(
            "Los **criterios de la razón y la raíz** son las dos herramientas más poderosas para series con "
            "**factoriales o exponenciales**. Ambos comparan implícitamente con una serie geométrica.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar el **criterio de la razón** (D'Alembert).\n"
            "- Aplicar el **criterio de la raíz** (Cauchy).\n"
            "- Reconocer cuándo cada uno es ventajoso.\n"
            "- Detectar el caso **inconcluso** ($L = 1$) y elegir otro método."
        )),

        b("teorema",
          nombre="Criterio de la razón (D'Alembert)",
          enunciado_md=(
              "Sea $\\sum a_n$ con $a_n \\neq 0$. Define\n\n"
              "$$L = \\lim_{n \\to \\infty} \\left|\\dfrac{a_{n+1}}{a_n}\\right|$$\n\n"
              "- Si $L < 1$: la serie **converge absolutamente**.\n"
              "- Si $L > 1$ (o $L = \\infty$): la serie **diverge**.\n"
              "- Si $L = 1$: el criterio **no decide** — usar otro método.\n\n"
              "**Idea:** la serie se comporta asintóticamente como geométrica con razón $L$."
          ),
          demostracion_md=(
              "Si $L < 1$, elegimos $r$ con $L < r < 1$. Para $n \\geq N$, $|a_{n+1}/a_n| < r$, así $|a_n| \\leq |a_N| \\cdot r^{n-N}$. "
              "Por comparación con la geométrica $\\sum r^n$ (converge porque $r < 1$), $\\sum |a_n|$ converge. "
              "Si $L > 1$, $|a_n|$ crece, así $a_n \\not\\to 0$ y la serie diverge por el test del término $n$-ésimo."
          )),

        b("ejemplo_resuelto",
          titulo="Razón con factorial: $\\sum n!/n^n$",
          problema_md="Determinar convergencia.",
          pasos=[
              {"accion_md": "**Razón:**\n\n$$\\dfrac{a_{n+1}}{a_n} = \\dfrac{(n+1)!/(n+1)^{n+1}}{n!/n^n} = \\dfrac{(n+1)! \\cdot n^n}{n! \\cdot (n+1)^{n+1}} = \\dfrac{(n+1) \\cdot n^n}{(n+1)^{n+1}} = \\dfrac{n^n}{(n+1)^n} = \\left(\\dfrac{n}{n+1}\\right)^n$$",
               "justificacion_md": "Simplificación clave: $(n+1)!/n! = n+1$ y $(n+1)^{n+1}/(n+1) = (n+1)^n$.",
               "es_resultado": False},
              {"accion_md": "**Límite:** $\\left(\\dfrac{n}{n+1}\\right)^n = \\left(1 - \\dfrac{1}{n+1}\\right)^n \\to e^{-1} = 1/e \\approx 0.368$.",
               "justificacion_md": "Aplicación de $(1 + c/n)^n \\to e^c$ con $c = -1$ (tras un pequeño ajuste).",
               "es_resultado": False},
              {"accion_md": "$L = 1/e < 1$ → **converge absolutamente**.",
               "justificacion_md": "**Patrón típico:** factoriales y potencias $n^n$ se manejan elegantemente con razón.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Criterio de la raíz (Cauchy)",
          enunciado_md=(
              "Sea $\\sum a_n$. Define\n\n"
              "$$L = \\lim_{n \\to \\infty} \\sqrt[n]{|a_n|}$$\n\n"
              "- Si $L < 1$: **converge absolutamente**.\n"
              "- Si $L > 1$: **diverge**.\n"
              "- Si $L = 1$: **inconcluso**.\n\n"
              "**Idea:** mismo principio que la razón, pero usando raíz $n$-ésima."
          ),
          demostracion_md=(
              "Si $L < 1$, elegimos $r \\in (L, 1)$. Para $n$ grande, $\\sqrt[n]{|a_n|} < r$, así $|a_n| < r^n$. "
              "Por comparación con $\\sum r^n$ (converge), $\\sum |a_n|$ converge."
          )),

        b("ejemplo_resuelto",
          titulo="Raíz: $\\sum (n/(2n+1))^n$",
          problema_md="Determinar convergencia.",
          pasos=[
              {"accion_md": "$|a_n|^{1/n} = \\dfrac{n}{2n+1}$. **Límite:**\n\n$$\\lim \\dfrac{n}{2n+1} = \\dfrac{1}{2}$$",
               "justificacion_md": "Cociente de polinomios al infinito.",
               "es_resultado": False},
              {"accion_md": "$L = 1/2 < 1$ → **converge**.",
               "justificacion_md": "**Patrón:** cuando $a_n$ es ya una potencia $n$-ésima, raíz simplifica al máximo. Razón daría algo más feo.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Cuándo razón vs raíz",
          body_md=(
              "**Razón** es ventajosa cuando hay:\n\n"
              "- **Factoriales** ($n!$, $(2n)!$, etc.) — la razón cancela elegantemente.\n"
              "- **Exponenciales con cocientes** que se simplifican: $r^n / s^n$.\n\n"
              "**Raíz** es ventajosa cuando hay:\n\n"
              "- **Potencia $n$-ésima global** del término: $a_n = (\\text{algo})^n$. Raíz lo destruye.\n"
              "- Combinaciones donde $\\sqrt[n]{n^k} = 1$ y $\\sqrt[n]{c} = 1$ permiten descartar mucho.\n\n"
              "**Hecho menor:** ambos criterios dan el **mismo límite** cuando los dos límites existen, pero raíz funciona en algunos casos donde razón no (por ejemplo, cuando la razón oscila)."
          )),

        b("ejemplo_resuelto",
          titulo="Caso inconcluso $L = 1$: $\\sum 1/n^p$",
          problema_md="Aplicar razón a $\\sum 1/n^p$.",
          pasos=[
              {"accion_md": "$\\dfrac{a_{n+1}}{a_n} = \\dfrac{n^p}{(n+1)^p} = \\left(\\dfrac{n}{n+1}\\right)^p \\to 1$.",
               "justificacion_md": "El límite es $1$, sin importar $p$.",
               "es_resultado": False},
              {"accion_md": "**$L = 1$** → razón no decide. **Pero sabemos** (serie $p$): converge $\\iff p > 1$.\n\n"
                            "**Lección:** razón y raíz fallan precisamente en las series $p$ — donde el término decae como potencia inversa, no exponencial.",
               "justificacion_md": "Para series $p$ y series racionales, usar **comparación** en su lugar.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los criterios:",
          preguntas=[
              {
                  "enunciado_md": "Para $\\sum \\dfrac{2^n}{n!}$, ¿qué criterio es más natural?",
                  "opciones_md": [
                      "Comparación directa.",
                      "Razón.",
                      "Raíz.",
                      "Test de la integral.",
                  ],
                  "correcta": "B",
                  "pista_md": "Hay factorial — la razón los cancela bien.",
                  "explicacion_md": (
                      "$a_{n+1}/a_n = \\dfrac{2^{n+1}/(n+1)!}{2^n/n!} = \\dfrac{2}{n+1} \\to 0$. $L = 0 < 1$ → converge. **(De hecho la suma es $e^2 - 1$.)**"
                  ),
              },
              {
                  "enunciado_md": "Si el criterio de la razón da $L = 1$, ¿qué hacer?",
                  "opciones_md": [
                      "Concluir que diverge.",
                      "Concluir que converge.",
                      "El criterio no decide; aplicar otro (comparación, integral).",
                      "Cambiar al criterio de la raíz, porque siempre da otro valor.",
                  ],
                  "correcta": "C",
                  "pista_md": "$L = 1$ es el caso ambiguo del criterio.",
                  "explicacion_md": (
                      "$L = 1$ es inconcluso. La raíz típicamente da el mismo $1$ (cuando ambos existen). Hay que **cambiar de método** — comparación con $1/n^p$, integral, etc."
                  ),
              },
          ]),

        ej(
            titulo="Razón clásica",
            enunciado="¿Converge $\\sum_{n=1}^\\infty \\dfrac{n^2}{3^n}$?",
            pistas=[
                "Razón: $\\dfrac{(n+1)^2/3^{n+1}}{n^2/3^n}$.",
                "Simplifica: $\\dfrac{(n+1)^2}{3 n^2} = \\dfrac{1}{3}\\left(1 + \\dfrac{1}{n}\\right)^2 \\to 1/3$.",
            ],
            solucion=(
                "$$\\dfrac{a_{n+1}}{a_n} = \\dfrac{(n+1)^2/3^{n+1}}{n^2/3^n} = \\dfrac{(n+1)^2}{3 n^2} \\to \\dfrac{1}{3}$$\n\n"
                "$L = 1/3 < 1$ → **converge**."
            ),
        ),

        ej(
            titulo="Raíz con potencia n-ésima",
            enunciado="¿Converge $\\sum_{n=1}^\\infty \\left(\\dfrac{n+1}{3n+2}\\right)^n$?",
            pistas=[
                "$|a_n|^{1/n} = \\dfrac{n+1}{3n+2}$.",
                "Toma el límite cuando $n \\to \\infty$.",
            ],
            solucion=(
                "$|a_n|^{1/n} = \\dfrac{n+1}{3n+2} \\to \\dfrac{1}{3}$. $L = 1/3 < 1$ → **converge**."
            ),
        ),

        fig(
            "Tabla visual con dos columnas: 'Criterio de la razón' (L = lim |a_(n+1)/a_n|) y "
            "'Criterio de la raíz n-ésima' (L = lim |a_n|^(1/n)). Bajo cada columna, tres filas "
            "horizontales por rangos de L: fila superior teal #06b6d4 'L < 1 → CONVERGE' con "
            "ejemplo '∑ 2^n/n!'; fila central gris 'L = 1 → NO CONCLUYE' con ejemplo '∑ 1/n²'; "
            "fila inferior ámbar #f59e0b 'L > 1 → DIVERGE' con ejemplo '∑ n!/2^n'. Encabezados "
            "claros, separadores de fila visibles, tipografía matemática. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar razón con $L = 1$ y concluir.** Es inconcluso — hay que cambiar de método.",
              "**Confundir $|a_{n+1}/a_n|$ con $a_{n+1} - a_n$.** El criterio usa cociente, no diferencia.",
              "**Olvidar el valor absoluto.** El criterio se aplica al cociente en valor absoluto, importante si $a_n$ tiene signos.",
              "**Aplicar a series racionales puras** ($1/n^p$): siempre dan $L = 1$ y no concluyen.",
              "**Aplicar raíz cuando razón es más simple** (factoriales): da el mismo resultado pero con cuentas más feas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Razón:** $L = \\lim |a_{n+1}/a_n|$. Converge si $L < 1$, diverge si $L > 1$.",
              "**Raíz:** $L = \\lim \\sqrt[n]{|a_n|}$. Mismo criterio.",
              "**Caso $L = 1$:** inconcluso — usar comparación o integral.",
              "**Razón** ideal con factoriales y exponenciales separadas.",
              "**Raíz** ideal con potencias $n$-ésimas globales.",
              "**Próxima lección:** series de potencias — series donde los términos dependen de $x$.",
          ]),
    ]
    return {
        "id": "lec-mvar-1-5-criterios",
        "title": "Criterios de convergencia",
        "description": "Criterio de la razón (D'Alembert) y de la raíz (Cauchy). Cuándo aplicar cada uno.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# 1.6 Series de potencias
# =====================================================================
def lesson_1_6():
    blocks = [
        b("texto", body_md=(
            "Una **serie de potencias** es como una serie con términos que dependen de una variable $x$. "
            "Esto las convierte en **funciones**: las series de potencias son la generalización natural de "
            "los polinomios a infinitos términos.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Definir series de potencias y su **radio de convergencia** $R$.\n"
            "- Calcular $R$ con el criterio de la razón.\n"
            "- Determinar el **intervalo de convergencia** verificando los bordes.\n"
            "- Aplicar las propiedades: **derivar e integrar** término a término."
        )),

        b("definicion",
          titulo="Serie de potencias",
          body_md=(
              "Una **serie de potencias centrada en $a$** es:\n\n"
              "$$\\sum_{n=0}^{\\infty} c_n (x - a)^n = c_0 + c_1(x-a) + c_2 (x-a)^2 + \\cdots$$\n\n"
              "donde $c_n$ son los **coeficientes** (constantes). Si $a = 0$, queda $\\sum c_n x^n$.\n\n"
              "Para cada $x$ fijo, es una serie numérica. La pregunta es: **¿para qué $x$ converge?**"
          )),

        b("teorema",
          nombre="Radio e intervalo de convergencia",
          enunciado_md=(
              "Para una serie de potencias $\\sum c_n (x-a)^n$, hay tres posibilidades:\n\n"
              "**1.** Converge solo en $x = a$ (radio $R = 0$).\n\n"
              "**2.** Converge para todo $x \\in \\mathbb{R}$ (radio $R = \\infty$).\n\n"
              "**3.** Existe $R \\in (0, \\infty)$ tal que:\n\n"
              "- Si $|x - a| < R$: **converge absolutamente**.\n"
              "- Si $|x - a| > R$: **diverge**.\n"
              "- Si $|x - a| = R$ (los bordes $x = a \\pm R$): hay que **chequear caso por caso**.\n\n"
              "$R$ se llama **radio de convergencia** y el conjunto donde converge es el **intervalo de convergencia**."
          ),
          demostracion_md=(
              "La idea: $R = 1/L$ donde $L = \\lim |c_{n+1}/c_n|$ (cuando existe), por el criterio de la razón aplicado a $|c_n (x-a)^n|$."
          )),

        b("definicion",
          titulo="Cómo encontrar $R$ (con razón)",
          body_md=(
              "Aplicamos el criterio de la razón a $\\sum |c_n (x - a)^n|$:\n\n"
              "$$\\lim_{n \\to \\infty} \\dfrac{|c_{n+1}(x-a)^{n+1}|}{|c_n (x-a)^n|} = |x - a| \\cdot \\lim \\dfrac{|c_{n+1}|}{|c_n|}$$\n\n"
              "Para convergencia se requiere este límite $< 1$, así:\n\n"
              "$$|x - a| < \\dfrac{1}{L} = R \\quad \\text{donde } L = \\lim \\dfrac{|c_{n+1}|}{|c_n|}$$\n\n"
              "Si $L = 0$, $R = \\infty$. Si $L = \\infty$, $R = 0$."
          )),

        b("ejemplo_resuelto",
          titulo="Encontrar $R$ y el intervalo",
          problema_md="Determinar el intervalo de convergencia de $\\sum_{n=1}^{\\infty} \\dfrac{(x-2)^n}{n \\cdot 3^n}$.",
          pasos=[
              {"accion_md": "**Coeficientes:** $c_n = \\dfrac{1}{n \\cdot 3^n}$. **Razón:**\n\n"
                            "$$\\dfrac{|c_{n+1}|}{|c_n|} = \\dfrac{n \\cdot 3^n}{(n+1) \\cdot 3^{n+1}} = \\dfrac{n}{3(n+1)} \\to \\dfrac{1}{3}$$",
               "justificacion_md": "Cancelaciones del cociente.",
               "es_resultado": False},
              {"accion_md": "$R = 1/(1/3) = 3$. **Centro $a = 2$**, así converge en $|x - 2| < 3$, es decir, $x \\in (-1, 5)$.",
               "justificacion_md": "El intervalo abierto sin verificar bordes.",
               "es_resultado": False},
              {"accion_md": "**Verificar bordes:**\n\n"
                            "- $x = 5$: $\\sum \\dfrac{3^n}{n \\cdot 3^n} = \\sum \\dfrac{1}{n}$. **Diverge** (armónica).\n"
                            "- $x = -1$: $\\sum \\dfrac{(-3)^n}{n \\cdot 3^n} = \\sum \\dfrac{(-1)^n}{n}$. **Converge** (Leibniz).",
               "justificacion_md": "Sustituimos cada borde y analizamos por separado.",
               "es_resultado": False},
              {"accion_md": "**Intervalo de convergencia:** $[-1, 5)$.",
               "justificacion_md": "**Lección:** los bordes pueden ir en uno, ambos o ninguno. Hay que verificar cada uno individualmente.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Derivación e integración término a término",
          enunciado_md=(
              "Si $f(x) = \\sum_{n=0}^\\infty c_n (x - a)^n$ tiene radio de convergencia $R > 0$, entonces $f$ es **derivable** e **integrable** en el intervalo abierto $(a - R, a + R)$, y:\n\n"
              "$$f'(x) = \\sum_{n=1}^\\infty n \\, c_n (x - a)^{n-1}$$\n\n"
              "$$\\int f(x) \\, dx = C + \\sum_{n=0}^\\infty \\dfrac{c_n}{n+1} (x - a)^{n+1}$$\n\n"
              "**Las nuevas series tienen el mismo radio $R$** (los bordes pueden cambiar)."
          ),
          demostracion_md=(
              "Resultado clásico de análisis real. La idea: la convergencia uniforme en intervalos compactos contenidos en $(a-R, a+R)$ permite intercambiar derivada/integral con la suma infinita."
          )),

        b("ejemplo_resuelto",
          titulo="Derivar la geométrica",
          problema_md="Sabiendo que $\\dfrac{1}{1-x} = \\sum_{n=0}^\\infty x^n$ para $|x| < 1$, encontrar una serie para $\\dfrac{1}{(1-x)^2}$.",
          pasos=[
              {"accion_md": "**Derivamos ambos lados:** $\\dfrac{d}{dx}\\dfrac{1}{1-x} = \\dfrac{1}{(1-x)^2}$.",
               "justificacion_md": "La derivada de $1/(1-x)$ se calcula directo con la cadena.",
               "es_resultado": False},
              {"accion_md": "**Derivamos la serie término a término:**\n\n$$\\dfrac{d}{dx} \\sum_{n=0}^\\infty x^n = \\sum_{n=1}^\\infty n x^{n-1}$$",
               "justificacion_md": "El término $n = 0$ es constante, derivada $0$.",
               "es_resultado": False},
              {"accion_md": "$$\\dfrac{1}{(1-x)^2} = \\sum_{n=1}^\\infty n x^{n-1} = 1 + 2x + 3x^2 + 4x^3 + \\cdots$$",
               "justificacion_md": "**Mismo radio $R = 1$.** Sirve para $|x| < 1$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El radio de convergencia de $\\sum n! \\, x^n$ es:",
                  "opciones_md": ["$0$", "$1$", "$\\infty$", "$1/e$"],
                  "correcta": "A",
                  "pista_md": "$|c_{n+1}/c_n| = (n+1)! / n! = n+1 \\to \\infty$.",
                  "explicacion_md": (
                      "$L = \\infty$ → $R = 0$. La serie **converge solo en $x = 0$**. Tiene sentido: el factorial crece tan rápido que cualquier $x \\neq 0$ hace divergir la serie."
                  ),
              },
              {
                  "enunciado_md": "Si una serie de potencias tiene $R = 5$ centrada en $a = 3$, el intervalo de convergencia ABIERTO es:",
                  "opciones_md": ["$(-5, 5)$", "$(0, 6)$", "$(-2, 8)$", "$(3, 8)$"],
                  "correcta": "C",
                  "pista_md": "$|x - a| < R$ con $a = 3$ y $R = 5$.",
                  "explicacion_md": (
                      "$|x - 3| < 5 \\iff -5 < x - 3 < 5 \\iff -2 < x < 8$. **Los bordes $x = -2, 8$ requieren chequeo aparte.**"
                  ),
              },
          ]),

        ej(
            titulo="Encontrar el intervalo completo",
            enunciado="Determina el intervalo de convergencia de $\\sum_{n=0}^\\infty \\dfrac{x^n}{n!}$.",
            pistas=[
                "$|c_{n+1}/c_n| = n!/(n+1)! = 1/(n+1) \\to 0$.",
                "$L = 0$ → $R = \\infty$.",
            ],
            solucion=(
                "$\\lim |c_{n+1}/c_n| = \\lim 1/(n+1) = 0$, así $R = \\infty$.\n\n"
                "**Intervalo: $(-\\infty, \\infty)$.** La serie converge para todo $x \\in \\mathbb{R}$. (De hecho representa $e^x$.)"
            ),
        ),

        ej(
            titulo="Integrar una serie",
            enunciado=(
                "Sabiendo $\\dfrac{1}{1+x^2} = \\sum_{n=0}^\\infty (-1)^n x^{2n}$ para $|x| < 1$, "
                "encuentra la serie de $\\arctan x$."
            ),
            pistas=[
                "$\\int \\dfrac{1}{1+x^2} \\, dx = \\arctan x$.",
                "Integra término a término. Recuerda la constante.",
            ],
            solucion=(
                "$\\arctan x = \\int_0^x \\dfrac{1}{1+t^2} \\, dt = \\int_0^x \\sum_{n=0}^\\infty (-1)^n t^{2n} \\, dt = \\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{2n+1}}{2n+1}$.\n\n"
                "$$\\arctan x = x - \\dfrac{x^3}{3} + \\dfrac{x^5}{5} - \\dfrac{x^7}{7} + \\cdots$$\n\n"
                "**Mismo radio $R = 1$.** En $x = 1$: $\\arctan 1 = \\pi/4 = 1 - 1/3 + 1/5 - \\cdots$ (serie de Leibniz para $\\pi/4$)."
            ),
        ),

        fig(
            "Recta numérica horizontal con un punto central marcado 'c' (centro de la serie de "
            "potencias). Dos segmentos teal #06b6d4 sólidos extendiéndose a ambos lados desde c "
            "hasta c−R y c+R, etiquetados como 'zona de convergencia, |x−c| < R'. Más allá de "
            "c−R y c+R, segmentos grises etiquetados 'diverge'. La distancia R marcada con doble "
            "flecha ámbar #f59e0b a cada lado, con etiqueta 'R = radio'. Marcadores '?' ámbar "
            "exactamente en x = c−R y x = c+R con etiqueta 'extremos: analizar caso a caso'. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar verificar los bordes.** El criterio de la razón da convergencia **estrictamente** dentro de $|x-a| < R$. Los bordes $x = a \\pm R$ requieren análisis aparte.",
              "**Confundir centro con $0$.** Si $a \\neq 0$, $|x - a| < R$ es un intervalo desplazado, no centrado en $0$.",
              "**Asumir que el radio cambia al derivar/integrar.** El radio se mantiene; **los bordes pueden cambiar.**",
              "**Aplicar derivada a una serie en su borde.** El teorema garantiza derivabilidad solo en el intervalo abierto.",
              "**Usar el criterio de raíz cuando razón es más natural** (con potencias polinomiales y exponenciales separadas).",
          ]),

        b("resumen",
          puntos_md=[
              "**Serie de potencias** centrada en $a$: $\\sum c_n (x-a)^n$.",
              "**Radio $R$:** $R = 1/L$ donde $L = \\lim |c_{n+1}/c_n|$.",
              "**Intervalo de convergencia:** $|x - a| < R$ → converge; $|x-a| > R$ → diverge; bordes: chequeo individual.",
              "**Derivar e integrar término a término** dentro del abierto $(a-R, a+R)$, mismo radio.",
              "**Series clásicas:** $1/(1-x), 1/(1+x^2), \\ln(1+x), \\arctan x$ derivan unas de otras.",
              "**Próxima lección:** representar funciones conocidas como series de potencias.",
          ]),
    ]
    return {
        "id": "lec-mvar-1-6-potencias",
        "title": "Series de potencias",
        "description": "Radio e intervalo de convergencia, derivación e integración término a término.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


# =====================================================================
# 1.7 Representación de funciones
# =====================================================================
def lesson_1_7():
    blocks = [
        b("texto", body_md=(
            "Muchas funciones \"cerradas\" se pueden expresar como series de potencias. Esto es útil porque "
            "**las series son fáciles de derivar, integrar y evaluar numéricamente**. La idea central es "
            "partir de la geométrica $\\dfrac{1}{1-x} = \\sum x^n$ y manipularla.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Manipular la serie geométrica para obtener nuevas representaciones.\n"
            "- Aplicar **derivación e integración** para encontrar series de funciones relacionadas.\n"
            "- Reconocer las **series clásicas** y de dónde vienen."
        )),

        b("definicion",
          titulo="La serie geométrica como punto de partida",
          body_md=(
              "$$\\dfrac{1}{1-x} = \\sum_{n=0}^\\infty x^n = 1 + x + x^2 + x^3 + \\cdots, \\quad |x| < 1$$\n\n"
              "**Familia inmediata** (sustituyendo $x \\to -x$, $x \\to x^2$, etc.):\n\n"
              "- $\\dfrac{1}{1+x} = \\sum_{n=0}^\\infty (-1)^n x^n$\n"
              "- $\\dfrac{1}{1+x^2} = \\sum_{n=0}^\\infty (-1)^n x^{2n}$\n"
              "- $\\dfrac{1}{1-x^3} = \\sum_{n=0}^\\infty x^{3n}$\n\n"
              "Cada una con su propio rango de convergencia (verificar que $|x|, |x^2|, |x^3| < 1$)."
          )),

        b("ejemplo_resuelto",
          titulo="Serie de $\\ln(1 + x)$",
          problema_md="Derivar una representación en serie a partir de $1/(1+x)$.",
          pasos=[
              {"accion_md": "$\\dfrac{d}{dx} \\ln(1+x) = \\dfrac{1}{1+x} = \\sum_{n=0}^\\infty (-1)^n x^n$ para $|x| < 1$.",
               "justificacion_md": "Conexión clave: $\\ln(1+x)$ es antiderivada de $1/(1+x)$.",
               "es_resultado": False},
              {"accion_md": "**Integrando término a término** con $\\ln(1+0) = 0$ como constante:\n\n"
                            "$$\\ln(1+x) = \\int_0^x \\sum_{n=0}^\\infty (-1)^n t^n \\, dt = \\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{n+1}}{n+1}$$",
               "justificacion_md": "Integramos cada potencia de $t$.",
               "es_resultado": False},
              {"accion_md": "Reescribiendo con $m = n + 1$:\n\n$$\\ln(1+x) = \\sum_{m=1}^\\infty (-1)^{m-1} \\dfrac{x^m}{m} = x - \\dfrac{x^2}{2} + \\dfrac{x^3}{3} - \\cdots$$",
               "justificacion_md": "**Validez:** $|x| < 1$. En $x = 1$ converge (Leibniz), en $x = -1$ diverge (armónica). Intervalo $(-1, 1]$.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Series clásicas",
            body=(
                "| Función | Serie | Convergencia |\n|---|---|---|\n"
                "| $\\dfrac{1}{1-x}$ | $\\sum_{n=0}^\\infty x^n$ | $\\|x\\| < 1$ |\n"
                "| $\\dfrac{1}{1+x}$ | $\\sum_{n=0}^\\infty (-1)^n x^n$ | $\\|x\\| < 1$ |\n"
                "| $\\dfrac{1}{1+x^2}$ | $\\sum_{n=0}^\\infty (-1)^n x^{2n}$ | $\\|x\\| < 1$ |\n"
                "| $\\ln(1+x)$ | $\\sum_{n=1}^\\infty (-1)^{n-1} \\dfrac{x^n}{n}$ | $-1 < x \\leq 1$ |\n"
                "| $\\arctan x$ | $\\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{2n+1}}{2n+1}$ | $\\|x\\| \\leq 1$ |\n"
                "| $e^x$ | $\\sum_{n=0}^\\infty \\dfrac{x^n}{n!}$ | $\\mathbb{R}$ |\n"
                "| $\\sin x$ | $\\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{2n+1}}{(2n+1)!}$ | $\\mathbb{R}$ |\n"
                "| $\\cos x$ | $\\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{2n}}{(2n)!}$ | $\\mathbb{R}$ |"
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Serie de $1/(2 - x)$",
          problema_md="Encontrar una representación en serie centrada en $0$.",
          pasos=[
              {"accion_md": "**Reescribimos** para que tenga forma $1/(1 - u)$:\n\n$$\\dfrac{1}{2 - x} = \\dfrac{1}{2(1 - x/2)} = \\dfrac{1}{2} \\cdot \\dfrac{1}{1 - x/2}$$",
               "justificacion_md": "Factorizamos un $2$ del denominador para llegar a la forma estándar.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la geométrica** con $u = x/2$:\n\n$$\\dfrac{1}{1 - x/2} = \\sum_{n=0}^\\infty \\left(\\dfrac{x}{2}\\right)^n = \\sum_{n=0}^\\infty \\dfrac{x^n}{2^n}$$",
               "justificacion_md": "Válido para $|x/2| < 1$, es decir, $|x| < 2$.",
               "es_resultado": False},
              {"accion_md": "$$\\dfrac{1}{2-x} = \\dfrac{1}{2} \\sum_{n=0}^\\infty \\dfrac{x^n}{2^n} = \\sum_{n=0}^\\infty \\dfrac{x^n}{2^{n+1}}, \\quad |x| < 2$$",
               "justificacion_md": "**Patrón general:** factorizar para llegar a la forma $1/(1-u)$ es la técnica más común.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Serie de $\\dfrac{x}{1 + x^4}$",
          problema_md="Encontrar la serie centrada en $0$.",
          pasos=[
              {"accion_md": "**Empezamos con** $\\dfrac{1}{1 + x^4} = \\sum_{n=0}^\\infty (-1)^n (x^4)^n = \\sum_{n=0}^\\infty (-1)^n x^{4n}$, válido para $|x^4| < 1 \\iff |x| < 1$.",
               "justificacion_md": "Sustituimos $x \\to x^4$ en $1/(1+u)$.",
               "es_resultado": False},
              {"accion_md": "**Multiplicamos por $x$:**\n\n$$\\dfrac{x}{1 + x^4} = \\sum_{n=0}^\\infty (-1)^n x^{4n+1}$$",
               "justificacion_md": "**Multiplicar una serie por $x^k$** simplemente sube los exponentes en $k$. Sin afectar el radio.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica las técnicas:",
          preguntas=[
              {
                  "enunciado_md": "Para encontrar la serie de $\\dfrac{1}{3 - 2x}$, ¿cómo factorizas?",
                  "opciones_md": [
                      "$\\dfrac{1}{3} \\cdot \\dfrac{1}{1 - 2x/3}$",
                      "$3 \\cdot \\dfrac{1}{1 - 2x}$",
                      "$\\dfrac{1}{3 \\cdot (1 - x/3)}$",
                      "$\\dfrac{1}{2 \\cdot (3/2 - x)}$",
                  ],
                  "correcta": "A",
                  "pista_md": "Factorizar el coeficiente del término constante: $3 - 2x = 3(1 - 2x/3)$.",
                  "explicacion_md": (
                      "$3 - 2x = 3(1 - 2x/3)$, así $\\dfrac{1}{3-2x} = \\dfrac{1}{3} \\cdot \\dfrac{1}{1 - 2x/3}$. Aplicando geométrica con $u = 2x/3$: válido para $|2x/3| < 1$, es decir, $|x| < 3/2$."
                  ),
              },
              {
                  "enunciado_md": "Si $f(x) = \\sum_{n=0}^\\infty x^n$ ($|x| < 1$), entonces $\\int_0^x f(t) \\, dt$ vale:",
                  "opciones_md": [
                      "$\\sum_{n=0}^\\infty x^n / n$",
                      "$\\sum_{n=0}^\\infty x^{n+1} / (n+1)$",
                      "$-\\ln(1 - x)$",
                      "Tanto B como C son correctas.",
                  ],
                  "correcta": "D",
                  "pista_md": "$\\int 1/(1-t) \\, dt = -\\ln(1-t)$. Y la serie integrada término a término.",
                  "explicacion_md": (
                      "$\\int_0^x \\sum t^n \\, dt = \\sum x^{n+1}/(n+1)$. Y como $f(t) = 1/(1-t)$, $\\int_0^x 1/(1-t) \\, dt = -\\ln(1-x)$. Así $-\\ln(1-x) = \\sum_{n=0}^\\infty x^{n+1}/(n+1)$."
                  ),
              },
          ]),

        ej(
            titulo="Serie por sustitución",
            enunciado="Encuentra la serie de $f(x) = \\dfrac{1}{1 + 4x^2}$ centrada en $0$.",
            pistas=[
                "Sustituye $x \\to 2x$ (entonces $x^2 \\to 4x^2$) en $1/(1+x^2)$.",
                "Es decir, usa $u = 2x$ en $1/(1+u^2) = \\sum (-1)^n u^{2n}$.",
            ],
            solucion=(
                "$\\dfrac{1}{1 + 4x^2} = \\dfrac{1}{1 + (2x)^2} = \\sum_{n=0}^\\infty (-1)^n (2x)^{2n} = \\sum_{n=0}^\\infty (-1)^n 4^n x^{2n}$.\n\n"
                "**Convergencia:** $|2x| < 1 \\iff |x| < 1/2$."
            ),
        ),

        ej(
            titulo="Serie por integración",
            enunciado=(
                "Usa la serie $\\dfrac{1}{1+x^2} = \\sum (-1)^n x^{2n}$ para encontrar una serie para $\\arctan(x^2)$."
            ),
            pistas=[
                "Sabes que $\\arctan x = \\sum (-1)^n x^{2n+1}/(2n+1)$.",
                "Sustituye $x \\to x^2$ en esa serie.",
            ],
            solucion=(
                "$\\arctan(x^2) = \\sum_{n=0}^\\infty (-1)^n \\dfrac{(x^2)^{2n+1}}{2n+1} = \\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{4n+2}}{2n+1}$.\n\n"
                "**Convergencia:** $|x^2| \\leq 1 \\iff |x| \\leq 1$."
            ),
        ),

        fig(
            "Gráfico cartesiano. Eje x desde -1.5 a 1.5, eje y desde -1 a 5. La función "
            "f(x) = 1/(1−x) trazada en azul oscuro grueso, con asíntota vertical punteada en "
            "x = 1. Las aproximaciones polinomiales sucesivas superpuestas en tonos teal "
            "#06b6d4 cada vez más oscuros: P_0(x) = 1 (recta horizontal), P_1(x) = 1 + x, "
            "P_2(x) = 1 + x + x², P_3(x) = 1 + x + x² + x³. Dentro del intervalo (−1, 1) las "
            "polinomiales se acercan a la curva azul; fuera (a la derecha de 1 o izquierda de "
            "−1) se alejan en ámbar #f59e0b. Líneas verticales punteadas ámbar en x = ±1. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar factorizar antes de aplicar la geométrica.** $\\dfrac{1}{a - x}$ requiere $\\dfrac{1}{a} \\cdot \\dfrac{1}{1 - x/a}$.",
              "**Olvidar el cambio de variable de convergencia.** Si sustituyes $x \\to x^2$, la condición $|x| < 1$ se vuelve $|x^2| < 1 \\iff |x| < 1$ — pero si fuera $x \\to 2x$, sería $|x| < 1/2$.",
              "**Confundir el radio al multiplicar por $x^k$.** Multiplicar por una potencia simple **no cambia el radio**, solo desplaza exponentes.",
              "**Integrar sin la constante de integración.** Aunque al evaluar entre $0$ y $x$ se cancela, hay que tenerla en cuenta para series indefinidas.",
              "**No verificar bordes** después de derivar/integrar. Pueden cambiar.",
          ]),

        b("resumen",
          puntos_md=[
              "**Punto de partida:** $1/(1-x) = \\sum x^n$ para $|x| < 1$.",
              "**Por sustitución:** $x \\to -x$, $x \\to x^2$, $x \\to x/a$, etc., genera familias de series.",
              "**Por derivación:** $1/(1-x)^2 = \\sum n x^{n-1}$, etc.",
              "**Por integración:** $\\ln(1+x) = \\sum (-1)^{n-1} x^n/n$, $\\arctan x = \\sum (-1)^n x^{2n+1}/(2n+1)$.",
              "**Series clásicas** ($e^x, \\sin x, \\cos x$) tienen radio $\\infty$.",
              "**Próxima lección:** Taylor y Maclaurin — la fórmula general para series de cualquier función suficientemente regular.",
          ]),
    ]
    return {
        "id": "lec-mvar-1-7-representacion",
        "title": "Representación de funciones",
        "description": "Manipular la serie geométrica para representar otras funciones por sustitución, derivación e integración.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 7,
    }


# =====================================================================
# 1.8 Series de Taylor y Maclaurin
# =====================================================================
def lesson_1_8():
    blocks = [
        b("texto", body_md=(
            "Las series de Taylor son la **fórmula universal** para representar una función como serie de "
            "potencias. Si $f$ es infinitamente derivable cerca de $a$, su serie de Taylor centrada en $a$ "
            "es una receta directa que usa los **valores de las derivadas** de $f$ en $a$.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Construir la **serie de Taylor** de cualquier $f$ infinitamente derivable.\n"
            "- Reconocer la **serie de Maclaurin** (caso $a = 0$).\n"
            "- Conocer las series clásicas: $e^x, \\sin x, \\cos x, \\ln(1+x), (1+x)^k$.\n"
            "- **Estimar el error** con el resto de Taylor."
        )),

        b("definicion",
          titulo="Serie de Taylor y Maclaurin",
          body_md=(
              "Si $f$ es infinitamente derivable cerca de $a$, su **serie de Taylor centrada en $a$** es:\n\n"
              "$$f(x) = \\sum_{n=0}^{\\infty} \\dfrac{f^{(n)}(a)}{n!} (x - a)^n = f(a) + f'(a)(x-a) + \\dfrac{f''(a)}{2!}(x-a)^2 + \\cdots$$\n\n"
              "**Caso $a = 0$:** se llama **serie de Maclaurin**.\n\n"
              "$$f(x) = \\sum_{n=0}^\\infty \\dfrac{f^{(n)}(0)}{n!} x^n$$"
          )),

        b("intuicion",
          titulo="Por qué la fórmula tiene esa forma",
          body_md=(
              "Si $f(x) = \\sum c_n (x-a)^n$, entonces:\n\n"
              "- $f(a) = c_0$.\n"
              "- Derivando: $f'(x) = \\sum n c_n (x-a)^{n-1}$, así $f'(a) = c_1$.\n"
              "- Derivando otra vez: $f''(x) = \\sum n(n-1) c_n (x-a)^{n-2}$, así $f''(a) = 2 c_2$, es decir $c_2 = f''(a)/2!$.\n"
              "- En general: $f^{(n)}(a) = n! \\cdot c_n$, así $c_n = f^{(n)}(a)/n!$.\n\n"
              "**Esa es la fórmula de Taylor.** No tiene magia: sale de imponer que la serie y sus derivadas coincidan con las de $f$ en $a$."
          )),

        b("ejemplo_resuelto",
          titulo="Serie de Maclaurin de $e^x$",
          problema_md="Construir la serie usando la definición.",
          pasos=[
              {"accion_md": "**$f(x) = e^x$.** Todas sus derivadas: $f^{(n)}(x) = e^x$. **Evaluadas en $0$:** $f^{(n)}(0) = 1$ para todo $n$.",
               "justificacion_md": "Propiedad única de $e^x$.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la fórmula de Maclaurin:**\n\n$$e^x = \\sum_{n=0}^\\infty \\dfrac{1}{n!} x^n = 1 + x + \\dfrac{x^2}{2!} + \\dfrac{x^3}{3!} + \\cdots$$",
               "justificacion_md": "**Convergencia:** por razón, $L = \\lim 1/(n+1) = 0$, así $R = \\infty$. Vale para todo $\\mathbb{R}$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Serie de Maclaurin de $\\sin x$",
          problema_md="Derivar las series de seno y coseno.",
          pasos=[
              {"accion_md": "$f(x) = \\sin x$. **Derivadas evaluadas en $0$:**\n\n"
                            "$f(0) = 0, f'(0) = \\cos 0 = 1, f''(0) = -\\sin 0 = 0, f'''(0) = -\\cos 0 = -1, f^{(4)}(0) = \\sin 0 = 0, \\ldots$\n\n"
                            "**Patrón:** $0, 1, 0, -1, 0, 1, 0, -1, \\ldots$ (período 4).",
               "justificacion_md": "Las derivadas de $\\sin$ rotan entre $\\sin, \\cos, -\\sin, -\\cos$.",
               "es_resultado": False},
              {"accion_md": "$$\\sin x = \\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{2n+1}}{(2n+1)!} = x - \\dfrac{x^3}{6} + \\dfrac{x^5}{120} - \\cdots$$",
               "justificacion_md": "Solo sobreviven los términos de exponente impar. **Análogo:** $\\cos x = \\sum (-1)^n x^{2n}/(2n)! = 1 - x^2/2 + x^4/24 - \\cdots$ (exponentes pares).",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Series de Maclaurin clásicas",
            body=(
                "| $f(x)$ | Serie | Radio |\n|---|---|---|\n"
                "| $e^x$ | $\\sum_{n=0}^\\infty \\dfrac{x^n}{n!}$ | $\\infty$ |\n"
                "| $\\sin x$ | $\\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{2n+1}}{(2n+1)!}$ | $\\infty$ |\n"
                "| $\\cos x$ | $\\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{2n}}{(2n)!}$ | $\\infty$ |\n"
                "| $\\sinh x$ | $\\sum_{n=0}^\\infty \\dfrac{x^{2n+1}}{(2n+1)!}$ | $\\infty$ |\n"
                "| $\\cosh x$ | $\\sum_{n=0}^\\infty \\dfrac{x^{2n}}{(2n)!}$ | $\\infty$ |\n"
                "| $\\ln(1+x)$ | $\\sum_{n=1}^\\infty (-1)^{n-1} \\dfrac{x^n}{n}$ | $1$ |\n"
                "| $\\arctan x$ | $\\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{2n+1}}{2n+1}$ | $1$ |\n"
                "| $\\dfrac{1}{1-x}$ | $\\sum_{n=0}^\\infty x^n$ | $1$ |\n"
                "| $(1+x)^k$ (binomial) | $\\sum_{n=0}^\\infty \\binom{k}{n} x^n$ | $1$ (si $k \\notin \\mathbb{N}_0$) |\n\n"
                "**Coeficiente binomial generalizado:** $\\binom{k}{n} = \\dfrac{k(k-1)(k-2)\\cdots(k-n+1)}{n!}$ (válido para $k$ real)."
            ),
        ),

        b("teorema",
          nombre="Resto de Taylor",
          enunciado_md=(
              "Si $f$ es derivable suficientes veces cerca de $a$, podemos escribir\n\n"
              "$$f(x) = T_N(x) + R_N(x)$$\n\n"
              "donde $T_N(x) = \\sum_{n=0}^N \\dfrac{f^{(n)}(a)}{n!}(x-a)^n$ es el **polinomio de Taylor** de orden $N$, "
              "y $R_N(x)$ es el **resto**.\n\n"
              "**Forma de Lagrange del resto:** existe $c$ entre $a$ y $x$ con\n\n"
              "$$R_N(x) = \\dfrac{f^{(N+1)}(c)}{(N+1)!} (x - a)^{N+1}$$\n\n"
              "**Cota práctica:** si $|f^{(N+1)}(t)| \\leq M$ para $t$ entre $a$ y $x$:\n\n"
              "$$|R_N(x)| \\leq \\dfrac{M \\cdot |x - a|^{N+1}}{(N+1)!}$$"
          ),
          demostracion_md=(
              "Generalización del Teorema del Valor Medio. Se prueba por inducción usando integración por partes. "
              "La forma de Lagrange es análoga a la del TVM aplicado al residuo."
          )),

        b("ejemplo_resuelto",
          titulo="Aproximar $e$ con error pequeño",
          problema_md="¿Cuántos términos de la serie de $e^x$ en $x = 1$ se necesitan para aproximar $e$ con error $< 10^{-5}$?",
          pasos=[
              {"accion_md": "**$|f^{(N+1)}(c)| = e^c \\leq e \\leq 3$** para $c \\in [0, 1]$. Cota del resto:\n\n"
                            "$$|R_N(1)| \\leq \\dfrac{3}{(N+1)!}$$",
               "justificacion_md": "$e \\approx 2.718 < 3$, así $M = 3$ es válido (estricto pero útil).",
               "es_resultado": False},
              {"accion_md": "**Necesitamos** $\\dfrac{3}{(N+1)!} < 10^{-5} \\iff (N+1)! > 3 \\times 10^5$.\n\n"
                            "$8! = 40\\,320$, $9! = 362\\,880 > 3 \\times 10^5$. Así $N + 1 \\geq 9$, $N \\geq 8$.",
               "justificacion_md": "Comparando factoriales con la cota requerida.",
               "es_resultado": False},
              {"accion_md": "**$T_8(1) = \\sum_{n=0}^8 1/n! \\approx 2.71828$**, error real $\\approx 3 \\times 10^{-6} < 10^{-5}$. ✓",
               "justificacion_md": "**Convergencia rapidísima:** factoriales en denominador hacen que $e^x$ se aproxime con muy pocos términos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Calcular un límite con Taylor",
          problema_md="Calcular $\\lim_{x \\to 0} \\dfrac{\\sin x - x}{x^3}$ usando series.",
          pasos=[
              {"accion_md": "**Serie de $\\sin x$:** $\\sin x = x - \\dfrac{x^3}{6} + \\dfrac{x^5}{120} - \\cdots$.\n\n"
                            "**Restando $x$:** $\\sin x - x = -\\dfrac{x^3}{6} + \\dfrac{x^5}{120} - \\cdots$.",
               "justificacion_md": "Truco: cancelar el término de menor grado para llegar a una potencia neta.",
               "es_resultado": False},
              {"accion_md": "**Dividiendo por $x^3$:**\n\n$$\\dfrac{\\sin x - x}{x^3} = -\\dfrac{1}{6} + \\dfrac{x^2}{120} - \\cdots \\xrightarrow{x \\to 0} -\\dfrac{1}{6}$$",
               "justificacion_md": "**Comparación:** L'Hôpital aplicado tres veces da el mismo $-1/6$, pero series es más directo y elegante.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El polinomio de Taylor de orden 2 de $f$ en $a$ es:",
                  "opciones_md": [
                      "$f(a) + f'(a)(x-a) + f''(a)(x-a)^2$",
                      "$f(a) + f'(a)(x-a) + \\dfrac{f''(a)}{2}(x-a)^2$",
                      "$f'(a) + f''(a)(x-a) + f'''(a)(x-a)^2$",
                      "$f(a) + 2 f'(a)(x-a)$",
                  ],
                  "correcta": "B",
                  "pista_md": "El coeficiente de $(x-a)^n$ es $f^{(n)}(a)/n!$. Para $n = 2$, es $f''(a)/2$.",
                  "explicacion_md": (
                      "Cada término lleva $1/n!$ al frente. El factor $1/2! = 1/2$ es el que separa la opción correcta de la incorrecta."
                  ),
              },
              {
                  "enunciado_md": "$\\sin(x) - \\tan(x) \\approx ?$ cerca de $x = 0$ a primer orden no trivial.",
                  "opciones_md": ["$0$", "$-x$", "$-x^3/2$", "$-x^3/3$"],
                  "correcta": "C",
                  "pista_md": "$\\sin x = x - x^3/6 + \\ldots$ y $\\tan x = x + x^3/3 + \\ldots$. Resta.",
                  "explicacion_md": (
                      "$\\sin x - \\tan x = (x - x^3/6) - (x + x^3/3) + O(x^5) = -x^3/6 - x^3/3 = -x^3/2 + O(x^5)$. "
                      "**Lección:** restar series para obtener orden de cancelación."
                  ),
              },
          ]),

        ej(
            titulo="Serie de Maclaurin de $\\cos(x^2)$",
            enunciado="Encuentra la serie de Maclaurin de $f(x) = \\cos(x^2)$.",
            pistas=[
                "Empieza con $\\cos u = \\sum (-1)^n u^{2n}/(2n)!$.",
                "Sustituye $u = x^2$.",
            ],
            solucion=(
                "$\\cos(x^2) = \\sum_{n=0}^\\infty (-1)^n \\dfrac{(x^2)^{2n}}{(2n)!} = \\sum_{n=0}^\\infty (-1)^n \\dfrac{x^{4n}}{(2n)!} = 1 - \\dfrac{x^4}{2} + \\dfrac{x^8}{24} - \\cdots$\n\n"
                "**Convergencia:** $\\mathbb{R}$ (igual que $\\cos$)."
            ),
        ),

        ej(
            titulo="Aproximar $\\sin(0.1)$",
            enunciado="Usando $\\sin x \\approx x - x^3/6$, aproxima $\\sin(0.1)$ y estima el error.",
            pistas=[
                "Calcula $0.1 - (0.1)^3/6$.",
                "El siguiente término omitido es $(0.1)^5/120$.",
            ],
            solucion=(
                "$0.1 - 0.001/6 = 0.1 - 0.000\\overline{16} \\approx 0.099833$.\n\n"
                "**Error** $\\leq |(0.1)^5/120| = 10^{-5}/120 \\approx 8 \\times 10^{-8}$.\n\n"
                "Valor real: $\\sin(0.1) \\approx 0.09983341\\ldots$. Diferencia $\\approx 7 \\times 10^{-8}$. ✓"
            ),
        ),

        fig(
            "Gráfico cartesiano. Eje x desde -2π a 2π, eje y desde -1.5 a 1.5. La función "
            "sin(x) trazada en negro grueso. Cuatro aproximaciones de Taylor centradas en 0, "
            "superpuestas en tonos teal degradados (de claro a oscuro): T_1(x) = x (teal muy "
            "claro), T_3(x) = x − x³/6 (teal claro), T_5(x) = x − x³/6 + x⁵/120 (teal medio), "
            "T_7(x) = x − x³/6 + x⁵/120 − x⁷/5040 (teal oscuro #06b6d4). Cada una se ajusta a "
            "sin(x) en un rango cada vez más amplio cerca del origen. Punto ámbar #f59e0b en "
            "x = 0 marcando el centro de Maclaurin. Leyenda con grados. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $1/n!$.** El coeficiente del $n$-ésimo término es $f^{(n)}(a)/n!$, no solo $f^{(n)}(a)$.",
              "**Confundir Taylor con Maclaurin.** Maclaurin = Taylor con $a = 0$.",
              "**No sustituir directamente las series clásicas** cuando aplica. Es más rápido que recalcular derivadas.",
              "**Asumir convergencia automática.** Aunque la serie de Taylor exista, su convergencia a $f(x)$ requiere $R_N(x) \\to 0$.",
              "**Olvidar que el radio de convergencia limita** dónde la serie representa fielmente la función original.",
          ]),

        b("resumen",
          puntos_md=[
              "**Serie de Taylor:** $f(x) = \\sum f^{(n)}(a)(x-a)^n / n!$.",
              "**Maclaurin:** caso $a = 0$.",
              "**Series clásicas** ($e^x, \\sin x, \\cos x$): radio $\\infty$.",
              "**Resto de Lagrange:** $|R_N| \\leq M |x-a|^{N+1} / (N+1)!$.",
              "**Aplicaciones:** aproximar valores, calcular límites, integrales no elementales (vía integración término a término).",
              "**Cierre del capítulo:** las series de Taylor son la herramienta universal — toda función analítica se puede manipular como una serie.",
          ]),
    ]
    return {
        "id": "lec-mvar-1-8-taylor",
        "title": "Series de Taylor y Maclaurin",
        "description": "Fórmula universal para representar funciones como series de potencias. Series clásicas, resto y aplicaciones.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 8,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "calculo-multivariable"

    # 1. Crear/asegurar el curso
    course_doc = {
        "id": course_id,
        "title": "Cálculo Multivariable",
        "description": "Series y sucesiones, geometría del espacio, funciones de varias variables, derivadas parciales, integrales múltiples y aplicaciones.",
        "category": "Matemáticas",
        "level": "Avanzado",
        "modules_count": 7,
        "rating": 4.8,
        "summary": "Curso completo de cálculo multivariable para alumnos universitarios chilenos.",
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

    # 2. Capítulo
    chapter_id = "ch-series-sucesiones"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Series y Sucesiones",
        "description": "Sucesiones, series, pruebas de convergencia, alternantes, series de potencias, Taylor y Maclaurin.",
        "order": 1,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    # 3. Lecciones
    builders = [
        lesson_1_1, lesson_1_2, lesson_1_3, lesson_1_4,
        lesson_1_5, lesson_1_6, lesson_1_7, lesson_1_8,
    ]
    total_blocks = 0
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
        print(f"  ✓ {data['title']} ({len(data['blocks'])} bloques, ~{data['duration_minutes']} min)")

    print()
    print(f"✅ Capítulo 1 — Series y Sucesiones listo: {len(builders)} lecciones, {total_blocks} bloques.")
    print()
    print("Lecciones disponibles en:")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
