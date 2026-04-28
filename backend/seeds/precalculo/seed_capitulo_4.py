"""
Seed del curso Precálculo — Capítulo 4: Funciones Exponenciales y Logarítmicas.

Crea el capítulo 'Funciones Exponenciales y Logarítmicas' bajo el curso 'precalculo'
y siembra sus 3 lecciones:

  - Funciones exponenciales
  - Funciones logarítmicas
  - Ecuaciones exponenciales y logarítmicas

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
# Funciones exponenciales
# =====================================================================
def lesson_funciones_exponenciales():
    blocks = [
        b("texto", body_md=(
            "Las **funciones exponenciales** son la primera familia 'no algebraica' que aparece en "
            "precálculo. Su forma es\n\n"
            "$$f(x) = a^x, \\qquad a > 0, \\quad a \\neq 1.$$\n\n"
            "A diferencia de los polinomios, donde la variable está en la **base** y el exponente es fijo, "
            "aquí es al revés: la variable está **en el exponente**. Esto produce un comportamiento "
            "completamente nuevo: **crecimiento (o decrecimiento) explosivamente rápido**.\n\n"
            "**Aplicaciones omnipresentes:**\n\n"
            "- **Interés compuesto** y modelos financieros.\n"
            "- **Crecimiento poblacional** (bacterias, virus, especies).\n"
            "- **Decaimiento radiactivo** (fechado por carbono).\n"
            "- **Enfriamiento de Newton** (temperatura).\n"
            "- **Capacitor descargándose** en electrónica.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces la **forma general** $f(x) = a^x$ y sus propiedades.\n"
            "- Distinguís el comportamiento de $a > 1$ vs $0 < a < 1$.\n"
            "- Manejas el **número $e$** y la **función exponencial natural** $e^x$.\n"
            "- Aplicás el modelo a **interés compuesto** (capitalización discreta y continua)."
        )),

        b("definicion",
          titulo="Función exponencial",
          body_md=(
              "La **función exponencial de base $a$** se define como\n\n"
              "$$f(x) = a^x, \\qquad a > 0, \\quad a \\neq 1.$$\n\n"
              "**Restricciones de la base:**\n\n"
              "- $a > 0$: para que $a^x$ esté bien definido para **todos** los reales (incluidos los irracionales). "
              "Si $a < 0$, expresiones como $a^{1/2} = \\sqrt{a}$ no existen en $\\mathbb{R}$.\n"
              "- $a \\neq 1$: porque $1^x = 1$ es constante, no aporta nada nuevo.\n\n"
              "**Propiedades inmediatas:**\n\n"
              "- $\\operatorname{Dom}(f) = \\mathbb{R}$.\n"
              "- $\\operatorname{Ran}(f) = (0, +\\infty)$ — **siempre estrictamente positiva**.\n"
              "- $f(0) = a^0 = 1$ — **siempre pasa por $(0, 1)$**.\n"
              "- **Asíntota horizontal** $y = 0$ (eje $x$).\n"
              "- $f$ es **inyectiva**, así tiene inversa (el logaritmo, próxima lección).\n\n"
              "**Cuando $a$ es irracional**, $a^x$ se define por **continuidad** (límite de potencias racionales)."
          )),

        formulas(
            titulo="Comportamiento según la base",
            body=(
                "El signo de $\\log a$ (positivo si $a > 1$, negativo si $0 < a < 1$) controla el comportamiento:\n\n"
                "**Caso $a > 1$ (crecimiento exponencial):**\n\n"
                "- Función **estrictamente creciente**.\n"
                "- $f(x) \\to +\\infty$ cuando $x \\to +\\infty$.\n"
                "- $f(x) \\to 0^+$ cuando $x \\to -\\infty$.\n"
                "- Ejemplos: $2^x, 10^x, e^x, 3^x$.\n\n"
                "**Caso $0 < a < 1$ (decrecimiento exponencial):**\n\n"
                "- Función **estrictamente decreciente**.\n"
                "- $f(x) \\to 0^+$ cuando $x \\to +\\infty$.\n"
                "- $f(x) \\to +\\infty$ cuando $x \\to -\\infty$.\n"
                "- Ejemplos: $(1/2)^x, (0{,}9)^x, e^{-x}$.\n\n"
                "**Identidad útil.** $(1/a)^x = a^{-x}$. La gráfica de $(1/2)^x$ es la **reflexión** de $2^x$ "
                "respecto al eje $y$. Por eso 'crecimiento' y 'decrecimiento' son dos caras de la misma moneda."
            ),
        ),

        b("definicion",
          titulo="El número $e$ y la función natural",
          body_md=(
              "El **número $e$** se define por el límite\n\n"
              "$$e = \\lim_{n \\to \\infty} \\left(1 + \\dfrac{1}{n}\\right)^n \\approx 2{,}71828\\ldots$$\n\n"
              "Es **irracional** y **trascendente** (no es raíz de ningún polinomio con coeficientes enteros).\n\n"
              "Aparece **naturalmente** en problemas de **crecimiento continuo**: si una población crece "
              "instantáneamente a una tasa proporcional a su tamaño, su evolución se describe con $e^{r t}$.\n\n"
              "**Función exponencial natural:**\n\n"
              "$$f(x) = e^x.$$\n\n"
              "Es **la** función exponencial preferida en cálculo por su propiedad mágica: $\\dfrac{d}{dx} e^x = e^x$ "
              "(la derivada de $e^x$ es ella misma). Eso la convierte en el caballo de batalla del cálculo y de las ecuaciones diferenciales.\n\n"
              "**$e$ es la 'base canónica'.** Cualquier exponencial $a^x$ se puede reescribir como $e^{(\\ln a) x}$. "
              "Por eso, todo lo que se dice de $e^x$ se aplica con un cambio simple a cualquier base."
          )),

        b("ejemplo_resuelto",
          titulo="Identificar y graficar",
          problema_md="Compara las gráficas de $f(x) = 2^x$ y $g(x) = (1/2)^x$.",
          pasos=[
              {"accion_md": (
                  "**$f(x) = 2^x$:** $a = 2 > 1$ → creciente. Tabla:\n\n"
                  "| $x$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |\n"
                  "|---|---|---|---|---|---|\n"
                  "| $f(x)$ | $1/4$ | $1/2$ | $1$ | $2$ | $4$ |"
              ),
               "justificacion_md": "Crecimiento explosivo a la derecha, asintótico al eje a la izquierda.",
               "es_resultado": False},
              {"accion_md": (
                  "**$g(x) = (1/2)^x = 2^{-x}$:** $0 < a < 1$ → decreciente. Tabla:\n\n"
                  "| $x$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |\n"
                  "|---|---|---|---|---|---|\n"
                  "| $g(x)$ | $4$ | $2$ | $1$ | $1/2$ | $1/4$ |"
              ),
               "justificacion_md": "Valores 'al revés' que $f$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión:** las dos gráficas son **espejos** una de la otra respecto al eje $y$. Ambas pasan por $(0, 1)$ y tienen asíntota $y = 0$."
              ),
               "justificacion_md": "$g(x) = f(-x)$ por construcción.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Interés compuesto",
            body=(
                "Capital $P$ invertido a tasa anual $r$ (decimal), capitalizado $n$ veces por año, durante $t$ años produce:\n\n"
                "$$\\boxed{\\,A(t) = P \\left(1 + \\dfrac{r}{n}\\right)^{n t}.\\,}$$\n\n"
                "**Casos especiales:**\n\n"
                "- $n = 1$: anual.\n"
                "- $n = 2$: semestral.\n"
                "- $n = 4$: trimestral.\n"
                "- $n = 12$: mensual.\n"
                "- $n = 365$: diaria.\n\n"
                "**Capitalización continua** ($n \\to \\infty$):\n\n"
                "$$\\boxed{\\,A(t) = P\\, e^{r t}.\\,}$$\n\n"
                "**Mismo modelo** sirve para crecimiento poblacional ($P_0$ inicial, tasa $r$ por unidad de tiempo) y para muchos otros procesos exponenciales naturales."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Interés compuesto",
          problema_md="Inviertes \\$1000 a 12% anual, capitalizado trimestralmente, durante 3 años. ¿Cuánto tienes al final?",
          pasos=[
              {"accion_md": (
                  "**Identificar.** $P = 1000$, $r = 0{,}12$, $n = 4$ (trimestral), $t = 3$."
              ),
               "justificacion_md": "Trimestral = 4 veces por año.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar fórmula.** $A = 1000 (1 + 0{,}12/4)^{4 \\cdot 3} = 1000 (1{,}03)^{12}$.\n\n"
                  "$(1{,}03)^{12} \\approx 1{,}4258$.\n\n"
                  "**$A \\approx \\$1425{,}76$.**"
              ),
               "justificacion_md": "Casi 43% de ganancia en 3 años por la capitalización.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué el crecimiento exponencial es 'explosivo'.** $2^x$ duplica su valor cada vez que $x$ "
            "aumenta en 1. En $x = 30$, vale $\\approx 10^9$ (mil millones). Compará con $x^2$: en $x = 30$ "
            "vale $900$. Lo polinomial **no compite** con lo exponencial en escalas grandes.\n\n"
            "**Anécdota del ajedrez.** Cuento clásico: el inventor del ajedrez pidió como premio 1 grano de "
            "trigo en la primera casilla, 2 en la segunda, 4 en la tercera, ... Total: $2^{64} - 1 \\approx 1{,}8 \\cdot 10^{19}$ "
            "granos. **Más trigo del que ha producido la humanidad en toda su historia.** Eso es crecimiento exponencial.\n\n"
            "**$e$ y la capitalización continua.** Si invertís $\\$1$ a una tasa del 100% anual ($r = 1$) "
            "capitalizada $n$ veces, al cabo del año tenés $(1 + 1/n)^n$. Para $n \\to \\infty$, ese límite "
            "es $e \\approx 2{,}72$. Es decir: **capitalizando continuamente al 100%, multiplicás por $e$**."
        )),

        fig(
            "Dos exponenciales en un mismo plano: y = 2^x en color teal #06b6d4 (creciente) y y = (1/2)^x en ámbar #f59e0b (decreciente). "
            "Ambas pasan por (0, 1). Asíntota horizontal y = 0 marcada con línea punteada. "
            "Las curvas son simétricas respecto al eje y. "
            "Eje x de -3 a 3, eje y de 0 a 8 (con marcas en valores enteros). " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Toda exponencial $f(x) = a^x$ pasa por:",
                  "opciones_md": [
                      "$(1, a)$",
                      "**$(0, 1)$**",
                      "$(0, 0)$",
                      "$(a, 1)$",
                  ],
                  "correcta": "B",
                  "pista_md": "$a^0 = 1$ siempre.",
                  "explicacion_md": "Porque $f(0) = a^0 = 1$ para cualquier base válida.",
              },
              {
                  "enunciado_md": "$f(x) = (0{,}3)^x$ es:",
                  "opciones_md": [
                      "Creciente",
                      "**Decreciente**",
                      "Constante",
                      "Lineal",
                  ],
                  "correcta": "B",
                  "pista_md": "$0 < a < 1$.",
                  "explicacion_md": "Base entre 0 y 1 → decrecimiento.",
              },
              {
                  "enunciado_md": "El número $e$ vale aproximadamente:",
                  "opciones_md": [
                      "$2{,}5$",
                      "**$2{,}72$**",
                      "$3{,}14$",
                      "$1{,}41$",
                  ],
                  "correcta": "B",
                  "pista_md": "$e \\approx 2{,}71828$.",
                  "explicacion_md": "$\\pi \\approx 3{,}14$, $\\sqrt{2} \\approx 1{,}41$.",
              },
          ]),

        ej(
            "Determinar la base",
            "Halla $f(x) = a^x$ que pasa por $(2, 9)$.",
            ["$a^2 = 9$, con $a > 0$."],
            (
                "$a = 3$ (positivo). $f(x) = 3^x$."
            ),
        ),

        ej(
            "Decaimiento radiactivo",
            "Una sustancia tiene vida media de 10 años. Si comienzas con 100 g, ¿cuánto queda después de 30 años?",
            ["Cada 10 años se reduce a la mitad."],
            (
                "Modelo: $m(t) = 100 (1/2)^{t/10}$. Después de 30 años: $m(30) = 100 (1/2)^3 = 12{,}5$ g."
            ),
        ),

        ej(
            "Capitalización continua",
            "\\$5000 invertidos a 6% anual continuo durante 8 años. ¿Cuánto se obtiene?",
            ["$A = P e^{r t}$."],
            (
                "$A = 5000 \\cdot e^{0{,}06 \\cdot 8} = 5000 \\cdot e^{0{,}48} \\approx 5000 \\cdot 1{,}616 \\approx \\$8081$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**$a^x \\cdot a^y = a^{x \\cdot y}$.** Falso: es $a^{x + y}$.",
              "**$(a + b)^x = a^x + b^x$.** Falso. Solo $(a \\cdot b)^x = a^x b^x$.",
              "**Pensar que $a^x = 0$ para algún $x$.** Nunca: $a^x > 0$ para todo $x$.",
              "**Confundir $-3^x$ con $(-3)^x$.** Sin paréntesis: $-(3^x)$. Con paréntesis (que es problemático): $(-3)^x$ no está bien definido para $x$ irracional.",
              "**Olvidar que $a > 0$ es indispensable.** Sin esa condición, $a^{1/2}$ no existe.",
          ]),

        b("resumen",
          puntos_md=[
              "**$f(x) = a^x$** con $a > 0$, $a \\neq 1$. Dominio $\\mathbb{R}$, rango $(0, +\\infty)$.",
              "**$a > 1$ creciente; $0 < a < 1$ decreciente.** Asíntota $y = 0$.",
              "**Pasa por $(0, 1)$ siempre.** Es inyectiva (tiene inversa).",
              "**Número $e \\approx 2{,}72$.** Función natural $e^x$ es la base preferida en cálculo.",
              "**Interés compuesto:** $A = P(1 + r/n)^{n t}$ discreta, $A = P e^{r t}$ continua.",
              "**Próxima lección:** la **inversa** de la exponencial — el logaritmo.",
          ]),
    ]
    return {
        "id": "lec-prec-4-1-funciones-exponenciales",
        "title": "Funciones exponenciales",
        "description": "Función exponencial f(x) = a^x con a > 0 y a ≠ 1. Comportamiento según la base, número e y función exponencial natural e^x. Aplicaciones a interés compuesto (discreto y continuo) y crecimiento/decaimiento.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# Funciones logarítmicas
# =====================================================================
def lesson_funciones_logaritmicas():
    blocks = [
        b("texto", body_md=(
            "El **logaritmo** es **la función inversa** de la exponencial. Si la exponencial $a^x$ "
            "responde '¿qué pasa al elevar $a$ al exponente $x$?', el logaritmo responde la pregunta "
            "**inversa**: '¿a qué exponente hay que elevar $a$ para obtener un número dado?'.\n\n"
            "$$\\log_a x = y \\;\\Longleftrightarrow\\; a^y = x.$$\n\n"
            "Por ejemplo: $\\log_2 8 = 3$ porque $2^3 = 8$. $\\log_{10} 1000 = 3$ porque $10^3 = 1000$.\n\n"
            "**Aplicaciones:**\n\n"
            "- **Escala Richter** (terremotos): magnitud logarítmica.\n"
            "- **pH** (química): negativo del log de la concentración.\n"
            "- **Decibeles** (acústica).\n"
            "- **Resolver ecuaciones** donde la incógnita está en el exponente.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces la **definición** $\\log_a x$ y la conversión a forma exponencial.\n"
            "- Distinguís **log natural** $\\ln$ (base $e$) y **log decimal** $\\log$ (base 10).\n"
            "- Aplicás las **leyes de logaritmos** (producto, cociente, potencia, cambio de base).\n"
            "- Calculás el **dominio** de funciones con logaritmos."
        )),

        b("definicion",
          titulo="Definición del logaritmo",
          body_md=(
              "Sea $a > 0$, $a \\neq 1$. El **logaritmo de base $a$ de $x$** se define como\n\n"
              "$$\\boxed{\\,\\log_a x = y \\;\\Longleftrightarrow\\; a^y = x.\\,}$$\n\n"
              "Es decir: $\\log_a x$ es **el exponente al que hay que elevar $a$ para obtener $x$**.\n\n"
              "**Como inversa de la exponencial:**\n\n"
              "$$\\log_a(a^x) = x \\quad \\text{(para todo } x \\in \\mathbb{R}\\text{)},$$\n\n"
              "$$a^{\\log_a x} = x \\quad \\text{(para todo } x > 0\\text{)}.$$\n\n"
              "**Dominio y rango:**\n\n"
              "- $\\operatorname{Dom}(\\log_a) = (0, +\\infty)$ — solo positivos (porque $a^y$ es siempre positivo).\n"
              "- $\\operatorname{Ran}(\\log_a) = \\mathbb{R}$.\n\n"
              "**Logaritmos especiales:**\n\n"
              "- **Logaritmo natural** $\\ln x = \\log_e x$ (base $e \\approx 2{,}72$).\n"
              "- **Logaritmo decimal** $\\log x = \\log_{10} x$ (base 10).\n\n"
              "**Cuidado.** En distintos textos $\\log$ puede referirse a base $10$ o base $e$. En precálculo "
              "chileno, $\\log$ suele ser base 10 y $\\ln$ es base $e$."
          )),

        formulas(
            titulo="Propiedades fundamentales",
            body=(
                "Para $a > 0$, $a \\neq 1$ y $x, y > 0$:\n\n"
                "**Valores de referencia:**\n\n"
                "- $\\log_a 1 = 0$ (porque $a^0 = 1$).\n"
                "- $\\log_a a = 1$ (porque $a^1 = a$).\n"
                "- $\\log_a(a^x) = x$ y $a^{\\log_a x} = x$ (relaciones inversas).\n\n"
                "**Leyes de logaritmos:**\n\n"
                "$$\\log_a(x y) = \\log_a x + \\log_a y \\quad (\\textbf{producto}).$$\n\n"
                "$$\\log_a(x / y) = \\log_a x - \\log_a y \\quad (\\textbf{cociente}).$$\n\n"
                "$$\\log_a(x^k) = k \\log_a x \\quad (\\textbf{potencia}).$$\n\n"
                "**Cambio de base:**\n\n"
                "$$\\log_a x = \\dfrac{\\log_b x}{\\log_b a} \\quad (\\textbf{cualquier base } b > 0, b \\neq 1).$$\n\n"
                "Aplicación típica: $\\log_2 7 = \\dfrac{\\ln 7}{\\ln 2}$ o $\\dfrac{\\log 7}{\\log 2}$ — calculadora **siempre** tiene $\\ln$ o $\\log$."
            ),
        ),

        b("definicion",
          titulo="Gráfica del logaritmo",
          body_md=(
              "La gráfica de $y = \\log_a x$ es la **reflexión** de $y = a^x$ respecto a la recta $y = x$ (porque son inversas).\n\n"
              "**Caso $a > 1$ (logaritmo creciente):**\n\n"
              "- Estrictamente creciente.\n"
              "- Pasa por $(1, 0)$.\n"
              "- $\\log_a x \\to -\\infty$ cuando $x \\to 0^+$ (asíntota vertical $x = 0$).\n"
              "- $\\log_a x \\to +\\infty$ cuando $x \\to +\\infty$, pero **muy lentamente** (más despacio que cualquier polinomio).\n\n"
              "**Caso $0 < a < 1$ (logaritmo decreciente):**\n\n"
              "- Estrictamente decreciente.\n"
              "- Pasa por $(1, 0)$.\n"
              "- Asíntota vertical $x = 0$ (pero $\\to +\\infty$ ahí).\n"
              "- $\\to -\\infty$ cuando $x \\to +\\infty$.\n\n"
              "En la práctica casi siempre trabajamos con $a > 1$ (especialmente $\\ln$ y $\\log_{10}$)."
          )),

        b("ejemplo_resuelto",
          titulo="Aplicar leyes de logaritmos",
          problema_md="Expande $\\log\\dfrac{x^3 \\sqrt{y}}{z^2}$ usando las leyes.",
          pasos=[
              {"accion_md": (
                  "**Cociente:** $\\log\\dfrac{x^3 \\sqrt{y}}{z^2} = \\log(x^3 \\sqrt{y}) - \\log(z^2)$."
              ),
               "justificacion_md": "Ley del cociente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Producto en el primer término:** $\\log(x^3 \\sqrt{y}) = \\log(x^3) + \\log(\\sqrt{y}) = \\log(x^3) + \\log(y^{1/2})$."
              ),
               "justificacion_md": "Reescribir $\\sqrt{y}$ como exponente fraccionario.",
               "es_resultado": False},
              {"accion_md": (
                  "**Potencia en cada uno:** $3 \\log x + \\dfrac{1}{2} \\log y - 2 \\log z$.\n\n"
                  "**Resultado:** $\\log\\dfrac{x^3 \\sqrt{y}}{z^2} = 3 \\log x + \\dfrac{1}{2} \\log y - 2 \\log z$."
              ),
               "justificacion_md": "Ley de la potencia baja los exponentes.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cambio de base",
          problema_md="Calcula $\\log_5 30$ usando logaritmo natural.",
          pasos=[
              {"accion_md": (
                  "**Cambio de base:** $\\log_5 30 = \\dfrac{\\ln 30}{\\ln 5}$."
              ),
               "justificacion_md": "Cualquier base sirve; usar la que la calculadora tenga.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular.** $\\ln 30 \\approx 3{,}4012$, $\\ln 5 \\approx 1{,}6094$. $\\log_5 30 \\approx 3{,}4012/1{,}6094 \\approx 2{,}113$.\n\n"
                  "**Verificar.** $5^{2{,}113} \\approx 30$ ✓."
              ),
               "justificacion_md": "Sentido común: $5^2 = 25, 5^3 = 125$, así $\\log_5 30$ está entre 2 y 3, más cerca de 2.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Dominio con logaritmo",
          problema_md="Halla el dominio de $g(x) = \\log_3(x^2 - 1)$.",
          pasos=[
              {"accion_md": (
                  "**Restricción:** argumento $> 0$. $x^2 - 1 > 0 \\Rightarrow (x - 1)(x + 1) > 0$."
              ),
               "justificacion_md": "Logaritmo solo de positivos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Tabla de signos.** $(x - 1)(x + 1) > 0$ cuando ambos del mismo signo: $x < -1$ o $x > 1$.\n\n"
                  "**Dominio:** $(-\\infty, -1) \\cup (1, +\\infty)$."
              ),
               "justificacion_md": "Intervalos donde el producto es positivo.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué los logaritmos 'aplastan' magnitudes.** El logaritmo convierte **multiplicación en "
            "suma**: $\\log(ab) = \\log a + \\log b$. Eso significa que pasar de $10$ a $100$ (multiplicar "
            "por 10) corresponde a pasar de $\\log 10 = 1$ a $\\log 100 = 2$ (sumar 1). Por eso la **escala "
            "logarítmica** es ideal para representar fenómenos con rango enorme: terremotos, sonidos, etc.\n\n"
            "**Crecimiento muy lento.** $\\log x$ crece más despacio que **cualquier** polinomio. $\\log(10^{100}) = 100$. "
            "Ese 'rango enorme' aplastado a un número manejable.\n\n"
            "**Aplicaciones de escala logarítmica:**\n\n"
            "- **Richter:** magnitud $9$ es **10 veces** más fuerte que $8$, **100 veces** más que $7$.\n"
            "- **pH:** pH 4 es **10 veces** más ácido que pH 5.\n"
            "- **Decibeles:** sumar 10 dB = multiplicar la intensidad por 10.\n\n"
            "**Truco.** Antes de las calculadoras, los logaritmos eran la herramienta principal para multiplicar "
            "grandes números: convertir a sumas, sumar, antilogaritmar. Las **reglas de cálculo** funcionaban así."
        )),

        fig(
            "Función logaritmo y = log_2(x) en color teal #06b6d4 dibujada para x en (0, 8). "
            "Asíntota vertical x = 0 marcada como línea punteada. "
            "Pasa por (1, 0), (2, 1), (4, 2), (8, 3) — puntos marcados. "
            "En el mismo plano, la exponencial y = 2^x en color ámbar #f59e0b (creciente, asíntota y = 0). "
            "Recta y = x dibujada en gris punteada como referencia para mostrar que las curvas son simétricas respecto a ella. "
            "Eje x e y de -2 a 8. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\log_3 27 = $",
                  "opciones_md": ["$9$", "**$3$**", "$1$", "$27$"],
                  "correcta": "B",
                  "pista_md": "$3^? = 27$.",
                  "explicacion_md": "$3^3 = 27$, así $\\log_3 27 = 3$.",
              },
              {
                  "enunciado_md": "$\\log(x y) = $",
                  "opciones_md": [
                      "$\\log x \\cdot \\log y$",
                      "**$\\log x + \\log y$**",
                      "$\\log x - \\log y$",
                      "$\\log(x + y)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Producto adentro = suma afuera.",
                  "explicacion_md": "Ley del producto.",
              },
              {
                  "enunciado_md": "El dominio de $f(x) = \\ln(x - 5)$ es:",
                  "opciones_md": [
                      "$\\mathbb{R}$",
                      "$[5, +\\infty)$",
                      "**$(5, +\\infty)$**",
                      "$\\mathbb{R} \\setminus \\{5\\}$",
                  ],
                  "correcta": "C",
                  "pista_md": "Argumento estrictamente positivo.",
                  "explicacion_md": "$x - 5 > 0 \\Rightarrow x > 5$. Estricto, no incluye 5.",
              },
          ]),

        ej(
            "Calcular log",
            "Calcula sin calculadora: $\\log_4 64$, $\\log_{1/2} 8$, $\\ln(e^5)$.",
            ["Aplicar definición."],
            (
                "$\\log_4 64 = 3$ (porque $4^3 = 64$). $\\log_{1/2} 8 = -3$ (porque $(1/2)^{-3} = 8$). $\\ln(e^5) = 5$ (relación inversa)."
            ),
        ),

        ej(
            "Condensar logs",
            "Escribe como un solo logaritmo: $2 \\log x + 3 \\log y - \\log z$.",
            ["Usar potencia, después producto y cociente."],
            (
                "$\\log x^2 + \\log y^3 - \\log z = \\log(x^2 y^3) - \\log z = \\log\\dfrac{x^2 y^3}{z}$."
            ),
        ),

        ej(
            "Dominio compuesto",
            "Halla el dominio de $g(x) = \\ln(x - x^2)$.",
            ["$x - x^2 > 0$."],
            (
                "$x(1 - x) > 0$. Tabla de signos: positivo para $0 < x < 1$. **Dominio:** $(0, 1)$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**$\\log(a + b) = \\log a + \\log b$.** **Falso.** La ley del producto es $\\log(a \\cdot b)$.",
              "**$\\log(x - y) = \\log x - \\log y$.** **Falso.** La ley del cociente es $\\log(x / y)$.",
              "**Aplicar logaritmo a un argumento negativo o cero.** No está definido en $\\mathbb{R}$.",
              "**Confundir $\\ln^{-1}$ con $1/\\ln$.** $\\ln^{-1}$ = inversa = exponencial $e^x$. $1/\\ln$ = recíproca aritmética.",
              "**Calcular $\\log_a 1$ y dar algo que no sea $0$.** Siempre es $0$ porque $a^0 = 1$.",
          ]),

        b("resumen",
          puntos_md=[
              "**$\\log_a x = y \\Leftrightarrow a^y = x$.** Inversa de la exponencial.",
              "**Logs especiales:** $\\ln$ (base $e$), $\\log$ (base 10).",
              "**Dominio:** $(0, +\\infty)$. **Asíntota vertical** $x = 0$.",
              "**Leyes:** $\\log(x y) = \\log x + \\log y$; $\\log(x/y) = \\log x - \\log y$; $\\log(x^k) = k \\log x$.",
              "**Cambio de base:** $\\log_a x = \\dfrac{\\log_b x}{\\log_b a}$.",
              "**Próxima lección:** resolver ecuaciones donde aparece $a^x$ o $\\log x$.",
          ]),
    ]
    return {
        "id": "lec-prec-4-2-funciones-logaritmicas",
        "title": "Funciones logarítmicas",
        "description": "Logaritmo log_a x como inversa de la exponencial. Logaritmo natural ln y decimal log. Propiedades: producto, cociente, potencia, cambio de base. Gráficas y dominio de funciones con logaritmos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# Ecuaciones exponenciales y logarítmicas
# =====================================================================
def lesson_ecuaciones_exp_log():
    blocks = [
        b("texto", body_md=(
            "Una **ecuación exponencial** es aquella en que la incógnita aparece en el **exponente**. "
            "Una **ecuación logarítmica** es aquella en que la incógnita aparece dentro de un **logaritmo**.\n\n"
            "$$3^{x + 2} = 7 \\quad \\text{(exponencial)}, \\qquad \\log(x + 2) + \\log(x - 1) = 1 \\quad \\text{(logarítmica)}.$$\n\n"
            "Ambas se resuelven aprovechando que **exponencial y logaritmo son inversas mutuas**:\n\n"
            "- Para 'sacar' una incógnita de un exponente, **aplicar logaritmo** a ambos lados.\n"
            "- Para 'sacar' una incógnita de adentro de un log, **aplicar exponencial** (forma exponencial).\n\n"
            "**Al terminar:**\n\n"
            "- Resolvés ecuaciones exponenciales aislando la exponencial y aplicando $\\log$.\n"
            "- Resolvés ecuaciones logarítmicas pasando a forma exponencial.\n"
            "- **Verificás siempre el dominio** en ecuaciones logarítmicas.\n"
            "- Aplicás sustituciones para ecuaciones cuadráticas en $e^x$."
        )),

        formulas(
            titulo="Ecuaciones exponenciales — método",
            body=(
                "**Procedimiento general:**\n\n"
                "1. **Aislar la expresión exponencial** en un lado.\n"
                "2. **Aplicar logaritmo** (cualquier base, pero $\\ln$ o $\\log$ son los más cómodos) a ambos lados.\n"
                "3. **Bajar el exponente** usando $\\log(a^x) = x \\log a$.\n"
                "4. **Despejar la variable.**\n\n"
                "**Caso especial — bases iguales:** si la ecuación es $a^{f(x)} = a^{g(x)}$, por inyectividad de la exponencial, basta con $f(x) = g(x)$. No hace falta logaritmo.\n\n"
                "**Caso cuadrática en exponencial:** $e^{2 x} - 3 e^x + 2 = 0$. **Sustitución** $u = e^x$ → $u^2 - 3 u + 2 = 0$, cuadrática en $u$. Resolver y volver a $x$ con $x = \\ln u$ (recordando $u > 0$)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Exponencial básica",
          problema_md="Resuelve $3^{x + 2} = 7$.",
          pasos=[
              {"accion_md": (
                  "**Aplicar $\\log$ a ambos lados:** $\\log(3^{x + 2}) = \\log 7$."
              ),
               "justificacion_md": "Logaritmo de cualquier base. Usar $\\log_{10}$ o $\\ln$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Bajar el exponente:** $(x + 2) \\log 3 = \\log 7$."
              ),
               "justificacion_md": "Ley de la potencia.",
               "es_resultado": False},
              {"accion_md": (
                  "**Despejar:** $x + 2 = \\dfrac{\\log 7}{\\log 3}$, $x = \\dfrac{\\log 7}{\\log 3} - 2 \\approx 1{,}771 - 2 = -0{,}229$."
              ),
               "justificacion_md": "Verificar: $3^{-0{,}229 + 2} = 3^{1{,}771} \\approx 7$ ✓.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cuadrática en exponencial",
          problema_md="Resuelve $e^{2 x} - 3 e^x + 2 = 0$.",
          pasos=[
              {"accion_md": (
                  "**Sustituir** $u = e^x$. Como $e^{2 x} = (e^x)^2 = u^2$:\n\n"
                  "$u^2 - 3 u + 2 = 0$."
              ),
               "justificacion_md": "Reducir a cuadrática estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Factorizar:** $(u - 1)(u - 2) = 0 \\Rightarrow u = 1$ o $u = 2$."
              ),
               "justificacion_md": "Buscar dos números con suma 3 y producto 2.",
               "es_resultado": False},
              {"accion_md": (
                  "**Volver a $x$:** $u = e^x$, así $e^x = 1 \\Rightarrow x = 0$, o $e^x = 2 \\Rightarrow x = \\ln 2 \\approx 0{,}693$.\n\n"
                  "**Soluciones:** $x = 0$ y $x = \\ln 2$. Ambas válidas (no hay restricciones)."
              ),
               "justificacion_md": "Como $u > 0$ por ser exponencial, ambas raíces $u$ son aceptables.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Ecuaciones logarítmicas — método",
            body=(
                "**Procedimiento general:**\n\n"
                "1. **Aislar el término logarítmico** (combinarlo si hay varios usando las leyes).\n"
                "2. **Pasar a forma exponencial:** $\\log_a x = y \\Rightarrow x = a^y$.\n"
                "3. **Resolver** la ecuación algebraica resultante.\n"
                "4. **VERIFICAR** que las soluciones cumplen el dominio (todos los argumentos de log deben ser positivos).\n\n"
                "**Por qué verificar.** Las leyes de logaritmos pueden 'agrandar' el dominio. Por ejemplo, "
                "$\\log x + \\log(x - 1) = \\log[x(x - 1)]$, pero el original requiere $x > 0$ y $x > 1$, "
                "mientras que el combinado solo requiere $x(x - 1) > 0$. Una solución que cumpla la combinada "
                "puede no cumplir la original."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Logarítmica simple",
          problema_md="Resuelve $\\log(3 x + 5) = 2$.",
          pasos=[
              {"accion_md": (
                  "**Forma exponencial.** $\\log_{10}(3 x + 5) = 2 \\Rightarrow 3 x + 5 = 10^2 = 100$."
              ),
               "justificacion_md": "$\\log = 2$ significa $10^2 = $ argumento.",
               "es_resultado": False},
              {"accion_md": (
                  "**Despejar:** $3 x = 95 \\Rightarrow x = 95/3$.\n\n"
                  "**Verificar dominio:** $3(95/3) + 5 = 100 > 0$ ✓."
              ),
               "justificacion_md": "Solución única.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Logarítmica con varios términos",
          problema_md="Resuelve $\\log(x + 2) + \\log(x - 1) = 1$.",
          pasos=[
              {"accion_md": (
                  "**Combinar logs:** $\\log[(x + 2)(x - 1)] = 1$."
              ),
               "justificacion_md": "Ley del producto.",
               "es_resultado": False},
              {"accion_md": (
                  "**Forma exponencial:** $(x + 2)(x - 1) = 10^1 = 10$."
              ),
               "justificacion_md": "Pasar a forma exponencial.",
               "es_resultado": False},
              {"accion_md": (
                  "**Resolver cuadrática:** $x^2 + x - 2 = 10 \\Rightarrow x^2 + x - 12 = 0 \\Rightarrow (x + 4)(x - 3) = 0$.\n\n"
                  "$x = -4$ o $x = 3$."
              ),
               "justificacion_md": "Factorización por inspección.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificar dominio.** Original requiere $x + 2 > 0$ y $x - 1 > 0$, así $x > 1$.\n\n"
                  "$x = -4$: **descartar** (no cumple $x > 1$).\n\n"
                  "$x = 3$: $\\log 5 + \\log 2 = \\log 10 = 1$ ✓.\n\n"
                  "**Solución única:** $x = 3$."
              ),
               "justificacion_md": "**Crítico:** verificar siempre. Sin verificar, se reportarían dos soluciones erróneamente.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Aplicación a interés",
          problema_md="¿En cuánto tiempo se duplica una inversión a 5% anual capitalizado semestralmente?",
          pasos=[
              {"accion_md": (
                  "**Plantear.** Que se duplique: $A = 2 P$. $2 P = P(1 + 0{,}05/2)^{2 t} \\Rightarrow (1{,}025)^{2 t} = 2$."
              ),
               "justificacion_md": "Despejar para que el modelo sea $\\text{base}^{\\text{exp}} = 2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar log:** $2 t \\log(1{,}025) = \\log 2$.\n\n"
                  "$t = \\dfrac{\\log 2}{2 \\log 1{,}025} \\approx \\dfrac{0{,}301}{2 \\cdot 0{,}01072} \\approx 14{,}04$ años."
              ),
               "justificacion_md": "Despejar y calcular.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué verificar el dominio en log y no tanto en exp.** La función $a^x$ está definida para "
            "**todo** $x$ real, así nunca hay restricciones. Pero el log requiere argumento $> 0$ — y al "
            "combinar logs, esa restricción se puede perder.\n\n"
            "**Por qué $u = e^x$ siempre es positivo.** En la sustitución $u = e^x$, descartamos las raíces "
            "negativas de la cuadrática en $u$ porque la exponencial nunca es negativa. Olvidar esto produce "
            "soluciones espurias.\n\n"
            "**Regla del 70 (interés compuesto rápido).** Una aproximación útil: la duplicación de capital "
            "ocurre en aproximadamente $70 / r\\%$ años. A 5%: $70/5 = 14$ años (coincide con el cálculo "
            "de arriba). A 7%: 10 años. Sale del cálculo $\\ln 2 \\approx 0{,}693 \\approx 70/100$."
        )),

        fig(
            "Resolución gráfica de e^x = 5: dos curvas en un plano. "
            "Curva y = e^x en color teal #06b6d4 (creciente). "
            "Recta horizontal y = 5 en color ámbar #f59e0b. "
            "Punto de intersección marcado con un círculo lleno y etiquetado x = ln(5) ≈ 1.609. "
            "Línea vertical punteada desde el punto de intersección al eje x marcando la solución. "
            "Eje x de -1 a 3, eje y de 0 a 8. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para resolver $5^x = 13$, aplicamos:",
                  "opciones_md": [
                      "Raíz cuadrada",
                      "**Logaritmo a ambos lados**",
                      "Multiplicación cruzada",
                      "Igualar exponentes",
                  ],
                  "correcta": "B",
                  "pista_md": "Bajar el exponente.",
                  "explicacion_md": "$\\log(5^x) = \\log 13 \\Rightarrow x \\log 5 = \\log 13 \\Rightarrow x = \\log 13 / \\log 5$.",
              },
              {
                  "enunciado_md": "$\\ln x = 3$ tiene como solución:",
                  "opciones_md": [
                      "$x = 3$",
                      "**$x = e^3$**",
                      "$x = \\ln 3$",
                      "$x = 1/3$",
                  ],
                  "correcta": "B",
                  "pista_md": "Forma exponencial: $x = e^3$.",
                  "explicacion_md": "$\\ln x = 3 \\Leftrightarrow x = e^3 \\approx 20{,}09$.",
              },
              {
                  "enunciado_md": "Al resolver $\\log x + \\log(x - 3) = 1$ obtienes $x = -2$ y $x = 5$. Las soluciones válidas son:",
                  "opciones_md": [
                      "Ambas",
                      "**Solo $x = 5$**",
                      "Solo $x = -2$",
                      "Ninguna",
                  ],
                  "correcta": "B",
                  "pista_md": "Verificar dominio: $x > 0$ y $x > 3$.",
                  "explicacion_md": "$x = -2$ no cumple $x > 0$, descartar. Solo $x = 5$.",
              },
          ]),

        ej(
            "Exponencial",
            "Resuelve $2^{3 x + 1} = 3^{x - 2}$.",
            ["Aplicar $\\ln$ a ambos lados."],
            (
                "$(3 x + 1) \\ln 2 = (x - 2) \\ln 3 \\Rightarrow 3 x \\ln 2 + \\ln 2 = x \\ln 3 - 2 \\ln 3$. "
                "$x(3 \\ln 2 - \\ln 3) = -2 \\ln 3 - \\ln 2 \\Rightarrow x = \\dfrac{-2 \\ln 3 - \\ln 2}{3 \\ln 2 - \\ln 3} \\approx -3{,}08$."
            ),
        ),

        ej(
            "Logarítmica con cociente",
            "Resuelve $\\log_5(x + 1) - \\log_5(x - 1) = 2$.",
            ["Combinar como cociente y forma exponencial."],
            (
                "$\\log_5\\dfrac{x + 1}{x - 1} = 2 \\Rightarrow \\dfrac{x + 1}{x - 1} = 25 \\Rightarrow x + 1 = 25 x - 25 \\Rightarrow 24 x = 26 \\Rightarrow x = 13/12$. "
                "Verificar: $x > 1$ ✓ (porque $13/12 > 1$). **Solución única:** $x = 13/12$."
            ),
        ),

        ej(
            "Cuadrática en exponencial",
            "Resuelve $e^x - 12 e^{-x} - 1 = 0$.",
            ["Multiplicar por $e^x$."],
            (
                "Multiplicando por $e^x$: $e^{2 x} - 12 - e^x = 0 \\Rightarrow e^{2 x} - e^x - 12 = 0$. "
                "Sustituir $u = e^x$: $u^2 - u - 12 = (u - 4)(u + 3) = 0$. "
                "$u = 4$ o $u = -3$ (descartar negativa). $x = \\ln 4 \\approx 1{,}386$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**No verificar dominio** en ecuaciones logarítmicas. Lleva a soluciones falsas.",
              "**No descartar raíces negativas** de la cuadrática $u = e^x$. La exponencial es siempre positiva.",
              "**Aplicar log a un lado solo.** Hay que aplicar a ambos lados.",
              "**Confundir $\\log x + \\log y$ con $\\log(x + y)$.** Solo $\\log(x \\cdot y)$.",
              "**Olvidar que $\\log a / \\log b = \\log_b a$, NO $\\log(a/b)$.** Son cosas distintas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Exponenciales:** aplicar log a ambos lados, bajar el exponente, despejar.",
              "**Logarítmicas:** combinar logs, pasar a forma exponencial, resolver y verificar dominio.",
              "**Sustitución $u = e^x$ (o $u = a^x$)** convierte cuadrática en exp en cuadrática algebraica. **Descartar $u \\leq 0$.**",
              "**Verificar** siempre las soluciones de logarítmicas: deben cumplir el dominio del original.",
              "**Cierre del capítulo:** dominamos exponenciales, logaritmos y ecuaciones que los involucran. Herramientas clave para todo lo que sigue.",
              "**Próximo capítulo:** funciones trigonométricas — la última gran familia de funciones del precálculo.",
          ]),
    ]
    return {
        "id": "lec-prec-4-3-ecuaciones-exp-log",
        "title": "Ecuaciones exponenciales y logarítmicas",
        "description": "Resolución de ecuaciones con incógnita en el exponente (aplicar logaritmo) y en el argumento del logaritmo (forma exponencial). Sustituciones para cuadráticas en exp. Verificación obligatoria del dominio.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
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

    chapter_id = "ch-prec-exp-log"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Funciones Exponenciales y Logarítmicas",
        "description": (
            "Función exponencial a^x y exponencial natural e^x, número e e interés compuesto. "
            "Logaritmos como inversa de la exponencial: log_a x, ln x, log x. Leyes de logaritmos "
            "y cambio de base. Resolución de ecuaciones exponenciales y logarítmicas."
        ),
        "order": 4,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_funciones_exponenciales,
        lesson_funciones_logaritmicas,
        lesson_ecuaciones_exp_log,
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
        f"✅ Capítulo 4 — Funciones Exponenciales y Logarítmicas listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
