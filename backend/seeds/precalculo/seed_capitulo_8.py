"""
Seed del curso Precálculo — Capítulo 8: Sucesiones y Series.

Crea el capítulo 'Sucesiones y Series' bajo el curso 'precalculo'
y siembra sus 5 lecciones:

  - Sucesiones
  - Tipos de sucesiones (aritméticas y geométricas)
  - Series
  - Inducción matemática
  - Teorema del binomio

Basado en los Apuntes/Clase de Se Remonta. Idempotente.
Cierre del curso Precálculo.
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
# Sucesiones
# =====================================================================
def lesson_sucesiones():
    blocks = [
        b("texto", body_md=(
            "Una **sucesión** es una **lista ordenada de números** indexada por los naturales. Más "
            "formalmente, es una función $a : \\mathbb{N} \\to \\mathbb{R}$, donde el valor $a(n)$ se "
            "denota $a_n$ y se llama **término $n$-ésimo**.\n\n"
            "$$a_1, a_2, a_3, \\ldots, a_n, \\ldots$$\n\n"
            "Las sucesiones aparecen en innumerables contextos: la población anual de una especie, los pagos "
            "mensuales de una hipoteca, los errores sucesivos de un método numérico, los términos de una "
            "expansión polinomial.\n\n"
            "**Aplicaciones famosas:**\n\n"
            "- **Fibonacci:** $1, 1, 2, 3, 5, 8, 13, 21, \\ldots$ — aparece en biología, arte, finanzas.\n"
            "- **Crecimiento poblacional discreto:** modelos malthusianos, logísticos.\n"
            "- **Algoritmos:** complejidad computacional como sucesión.\n\n"
            "**Al terminar:**\n\n"
            "- Distinguís sucesión **explícita** (con fórmula para $a_n$) de **recursiva** (con relación de recurrencia).\n"
            "- Calculás términos específicos a partir de cualquier definición.\n"
            "- Manejás la **notación sigma** $\\sum$ para sumas.\n"
            "- Conocés la sucesión de **Fibonacci** y su construcción."
        )),

        b("definicion",
          titulo="Sucesión",
          body_md=(
              "Una **sucesión** es una función $a : \\mathbb{N} \\to \\mathbb{R}$. Se denota como\n\n"
              "$$\\{a_n\\}_{n = 1}^{\\infty} = a_1, a_2, a_3, \\ldots$$\n\n"
              "donde $a_n$ es el **término general** o el **$n$-ésimo término**.\n\n"
              "**Dos formas de definir una sucesión:**\n\n"
              "**1. Forma explícita.** Una fórmula que da $a_n$ directamente en función de $n$.\n\n"
              "Ejemplo: $a_n = 2 n - 1$ define la sucesión $1, 3, 5, 7, 9, \\ldots$ (impares).\n\n"
              "**2. Forma recursiva.** Uno o más **valores iniciales** y una **relación de recurrencia** que determina $a_n$ en términos de los anteriores.\n\n"
              "Ejemplo: $a_1 = 1$, $a_n = 3(a_{n-1} + 2)$ para $n \\geq 2$. Genera $1, 9, 33, 105, \\ldots$\n\n"
              "**Ventaja de explícita:** se puede calcular cualquier término sin pasar por los anteriores.\n\n"
              "**Ventaja de recursiva:** modela naturalmente procesos que dependen del paso anterior (interés compuesto, dinámica poblacional, etc.). El precio: para calcular $a_{1000}$ hay que pasar por todos los anteriores."
          )),

        b("definicion",
          titulo="Sucesión de Fibonacci",
          body_md=(
              "Caso especial famoso: $F_1 = F_2 = 1$, $F_n = F_{n-1} + F_{n-2}$ para $n \\geq 3$.\n\n"
              "Genera: $1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, \\ldots$\n\n"
              "**Propiedades sorprendentes:**\n\n"
              "- $F_n / F_{n-1} \\to \\phi$ (la **razón áurea**, $\\phi = (1 + \\sqrt 5)/2 \\approx 1{,}618$).\n"
              "- Aparece en la disposición de hojas en una rama, en las espiras de una piña o de un girasol, en las medidas del Partenón.\n"
              "- Tiene una **fórmula explícita** (Binet): $F_n = (\\phi^n - \\psi^n)/\\sqrt 5$ con $\\psi = (1 - \\sqrt 5)/2$. Pero la recursión es más natural."
          )),

        b("definicion",
          titulo="Notación sigma (sumatoria)",
          body_md=(
              "Para denotar sumas largas se usa la **notación sigma**:\n\n"
              "$$\\sum_{k = m}^{n} a_k = a_m + a_{m+1} + \\cdots + a_n.$$\n\n"
              "El símbolo $\\Sigma$ es la letra griega 'sigma' (S de 'suma'). El **índice de suma** $k$ recorre los enteros desde $m$ (límite inferior) hasta $n$ (límite superior).\n\n"
              "**Ejemplo:** $\\sum_{k = 1}^{5} k^2 = 1 + 4 + 9 + 16 + 25 = 55$.\n\n"
              "**Propiedades clave:**\n\n"
              "$$\\sum_{k = 1}^{n} (a_k + b_k) = \\sum_{k = 1}^{n} a_k + \\sum_{k = 1}^{n} b_k.$$\n\n"
              "$$\\sum_{k = 1}^{n} (c \\cdot a_k) = c \\sum_{k = 1}^{n} a_k \\quad \\text{(con } c \\text{ constante)}.$$\n\n"
              "$$\\sum_{k = 1}^{n} c = n c \\quad \\text{(suma de constantes)}.$$\n\n"
              "**El índice $k$ es 'mudo':** $\\sum_{k = 1}^{n} k = \\sum_{j = 1}^{n} j$. Solo importan los límites y la fórmula."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular términos",
          problema_md="Para $a_n = (-1)^n \\cdot n / (n + 1)$, calcula $a_1, a_2, a_3, a_4$ y $a_{100}$.",
          pasos=[
              {"accion_md": (
                  "**Sustituir $n$ en la fórmula:**\n\n"
                  "$a_1 = (-1)^1 \\cdot 1/2 = -1/2$.\n"
                  "$a_2 = (-1)^2 \\cdot 2/3 = 2/3$.\n"
                  "$a_3 = -3/4$. $a_4 = 4/5$.\n\n"
                  "Patrón: signo alterna, fracciones $n/(n + 1)$ se acercan a 1."
              ),
               "justificacion_md": "Cada cálculo es independiente.",
               "es_resultado": False},
              {"accion_md": (
                  "**$a_{100} = (-1)^{100} \\cdot 100/101 = 100/101 \\approx 0{,}99$.**"
              ),
               "justificacion_md": "Sin pasar por los 99 anteriores — esa es la ventaja de la forma explícita.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Recursiva",
          problema_md="Calcula los primeros 5 términos de la sucesión $a_1 = 2$, $a_n = 3 a_{n-1} - 1$ para $n \\geq 2$.",
          pasos=[
              {"accion_md": (
                  "**Iterar:** $a_1 = 2$. $a_2 = 3 \\cdot 2 - 1 = 5$. $a_3 = 3 \\cdot 5 - 1 = 14$. $a_4 = 3 \\cdot 14 - 1 = 41$. $a_5 = 3 \\cdot 41 - 1 = 122$.\n\n"
                  "**Sucesión:** $2, 5, 14, 41, 122, \\ldots$"
              ),
               "justificacion_md": "Cada término requiere el anterior.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Sigma",
          problema_md="Calcula $\\sum_{k = 1}^{4} (2k + 1)$.",
          pasos=[
              {"accion_md": (
                  "**Expandir:** $k = 1: 3$. $k = 2: 5$. $k = 3: 7$. $k = 4: 9$. Suma: $3 + 5 + 7 + 9 = 24$."
              ),
               "justificacion_md": "Aplicar la fórmula a cada $k$ y sumar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Alternativa (usando propiedades):** $\\sum (2k + 1) = 2 \\sum k + \\sum 1 = 2 \\cdot 10 + 4 = 24$."
              ),
               "justificacion_md": "$\\sum_{k=1}^{4} k = 10$ y $\\sum_{k=1}^{4} 1 = 4$.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Sucesión vs función real.** Una sucesión es una función con dominio discreto ($\\mathbb{N}$). "
            "Por eso los términos están 'aislados' — no hay 'valores intermedios' como en una función continua "
            "$f: \\mathbb{R} \\to \\mathbb{R}$.\n\n"
            "**Recursivo vs explícito.** A veces es **muy difícil** convertir una recursión a una fórmula "
            "explícita, y viceversa. Por ejemplo, Fibonacci tiene fórmula explícita (Binet) pero es complicada; "
            "la recursión es directa. Para muchas sucesiones de la vida real, la recursión es lo natural y "
            "se calcula iterativamente con computadora.\n\n"
            "**Notación sigma compacta.** $\\sum_{k=1}^{1000} k^3$ encapsula una suma de mil términos en un "
            "símbolo. Indispensable para escribir matemática avanzada."
        )),

        fig(
            "Visualización de los primeros 10 términos de la sucesión de Fibonacci en una espiral. "
            "Cuadrados con lados de tamaño 1, 1, 2, 3, 5, 8, 13, 21 anidados formando la espiral áurea. "
            "Cada cuadrado etiquetado con el término correspondiente F_n. "
            "Espiral curva continua dibujada por dentro en color teal #06b6d4. "
            "Color ámbar #f59e0b para los cuadrados, etiquetas claras. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para $a_n = n^2 - n$, $a_5 = $",
                  "opciones_md": [
                      "$10$",
                      "**$20$**",
                      "$25$",
                      "$30$",
                  ],
                  "correcta": "B",
                  "pista_md": "$25 - 5 = 20$.",
                  "explicacion_md": "Sustituir $n = 5$ directamente.",
              },
              {
                  "enunciado_md": "$\\sum_{k=1}^{4} 3 = $",
                  "opciones_md": [
                      "$3$",
                      "**$12$**",
                      "$10$",
                      "$0$",
                  ],
                  "correcta": "B",
                  "pista_md": "Suma de 4 constantes iguales a 3.",
                  "explicacion_md": "$3 + 3 + 3 + 3 = 12$.",
              },
              {
                  "enunciado_md": "El término 7 de Fibonacci ($F_7$) es:",
                  "opciones_md": [
                      "$8$",
                      "**$13$**",
                      "$21$",
                      "$5$",
                  ],
                  "correcta": "B",
                  "pista_md": "1, 1, 2, 3, 5, 8, 13, ...",
                  "explicacion_md": "Séptimo término de la sucesión.",
              },
          ]),

        ej(
            "Calcular término",
            "Para $a_n = (n - 1)/(n + 1)$, halla $a_{99}$.",
            ["Sustituir directamente."],
            (
                "$a_{99} = 98/100 = 49/50 = 0{,}98$."
            ),
        ),

        ej(
            "Recursiva",
            "Para $a_1 = 3$, $a_n = a_{n-1} + 2 n - 1$ para $n \\geq 2$, calcula $a_2, a_3, a_4$.",
            ["Aplicar la recursión paso a paso."],
            (
                "$a_2 = 3 + 3 = 6$. $a_3 = 6 + 5 = 11$. $a_4 = 11 + 7 = 18$."
            ),
        ),

        ej(
            "Sigma",
            "Calcula $\\sum_{k=2}^{5} (k^2 - 1)$.",
            ["Expandir o usar propiedades."],
            (
                "$k = 2: 3$. $k = 3: 8$. $k = 4: 15$. $k = 5: 24$. Suma: $3 + 8 + 15 + 24 = 50$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir el índice con un valor:** $\\sum_{k=1}^{n} k$ no significa 'suma de $k$ veces 1', sino sumar los enteros de 1 a $n$.",
              "**Olvidar valores iniciales en sucesiones recursivas.** Sin ellos, la sucesión no está determinada.",
              "**Empezar la sucesión en $n = 0$ cuando se definió desde $n = 1$.** Verificar dominio de la sucesión.",
              "**Tratar $a_n$ como función real continua** y aplicar derivadas o integrales de cálculo. Las sucesiones son discretas.",
              "**Pensar que toda recursión tiene fórmula explícita 'simple'.** Algunas no la tienen.",
          ]),

        b("resumen",
          puntos_md=[
              "**Sucesión:** función $a: \\mathbb{N} \\to \\mathbb{R}$. Notación $\\{a_n\\}$.",
              "**Forma explícita:** fórmula directa $a_n = f(n)$. **Recursiva:** valores iniciales + relación de recurrencia.",
              "**Fibonacci:** $F_n = F_{n-1} + F_{n-2}$ con $F_1 = F_2 = 1$.",
              "**Notación sigma:** $\\sum_{k=m}^{n} a_k$. Linealidad: suma y producto por constante se distribuyen.",
              "**Próxima lección:** dos familias clásicas — sucesiones aritméticas y geométricas.",
          ]),
    ]
    return {
        "id": "lec-prec-8-1-sucesiones",
        "title": "Sucesiones",
        "description": "Sucesión como función a: N → R. Forma explícita vs recursiva. Sucesión de Fibonacci. Notación sigma para sumas y sus propiedades de linealidad.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 1,
    }


# =====================================================================
# Tipos de sucesiones (aritméticas y geométricas)
# =====================================================================
def lesson_tipos_sucesiones():
    blocks = [
        b("texto", body_md=(
            "Dos familias de sucesiones son **especialmente importantes** porque tienen fórmulas explícitas "
            "muy simples y aparecen en infinidad de aplicaciones:\n\n"
            "- **Sucesiones aritméticas:** cada término se obtiene **sumando** una constante al anterior.\n"
            "- **Sucesiones geométricas:** cada término se obtiene **multiplicando** el anterior por una constante.\n\n"
            "Para ambas conocemos:\n\n"
            "- Una **fórmula del término general**.\n"
            "- Una **fórmula cerrada para la suma de los primeros $n$ términos**.\n\n"
            "**Aplicaciones de aritméticas:** salarios crecientes en cantidad fija, depreciación lineal, conteo "
            "de personas en una progresión.\n\n"
            "**Aplicaciones de geométricas:** interés compuesto, decaimiento radiactivo, crecimiento bacteriano, "
            "fractales (autosimilares).\n\n"
            "**Al terminar:**\n\n"
            "- Distinguís aritméticas de geométricas.\n"
            "- Aplicás las fórmulas del término general y la suma para cada tipo.\n"
            "- Resolvés problemas de aplicación con ambas familias."
        )),

        formulas(
            titulo="Sucesión aritmética",
            body=(
                "Una sucesión $\\{a_n\\}$ es **aritmética** si cada término se obtiene del anterior **sumando una constante** $d$ (la **diferencia común**):\n\n"
                "$$a_{n + 1} = a_n + d \\quad \\text{para todo } n \\geq 1.$$\n\n"
                "Equivalentemente: $d = a_{n + 1} - a_n$ es **constante** para todos los pares consecutivos.\n\n"
                "**Forma:** $a, a + d, a + 2 d, a + 3 d, \\ldots$\n\n"
                "**Término general (fórmula explícita):**\n\n"
                "$$\\boxed{\\,a_n = a_1 + (n - 1) d.\\,}$$\n\n"
                "**Suma de los primeros $n$ términos:**\n\n"
                "$$\\boxed{\\,S_n = \\dfrac{n (a_1 + a_n)}{2} = \\dfrac{n [2 a_1 + (n - 1) d]}{2}.\\,}$$\n\n"
                "Las dos formas son equivalentes (sustituir $a_n$ por la fórmula general en la primera).\n\n"
                "**Mnemotecnia.** La suma es '$n$ veces el promedio entre el primero y el último'. Geométricamente: la suma de una progresión aritmética es como el área de un trapecio."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Aritmética básica",
          problema_md="Halla $a_{50}$ y $S_{50}$ de la sucesión $2, 5, 8, 11, \\ldots$",
          pasos=[
              {"accion_md": (
                  "**Identificar.** $a_1 = 2$, $d = 5 - 2 = 3$."
              ),
               "justificacion_md": "Verificar: $8 - 5 = 3$ ✓.",
               "es_resultado": False},
              {"accion_md": (
                  "**$a_{50}$:** $a_{50} = 2 + 49 \\cdot 3 = 2 + 147 = 149$."
              ),
               "justificacion_md": "$n - 1 = 49$.",
               "es_resultado": False},
              {"accion_md": (
                  "**$S_{50}$:** $S_{50} = 50 (2 + 149)/2 = 50 \\cdot 151/2 = 3775$."
              ),
               "justificacion_md": "Suma directa con la primera fórmula.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Sucesión geométrica",
            body=(
                "Una sucesión $\\{a_n\\}$ es **geométrica** si cada término se obtiene del anterior **multiplicando por una constante** $r$ (la **razón común**):\n\n"
                "$$a_{n + 1} = r \\cdot a_n \\quad \\text{para todo } n \\geq 1.$$\n\n"
                "Equivalentemente: $r = a_{n + 1} / a_n$ es **constante** para todos los pares consecutivos (asumiendo $a_n \\neq 0$).\n\n"
                "**Forma:** $a, a r, a r^2, a r^3, \\ldots$\n\n"
                "**Término general:**\n\n"
                "$$\\boxed{\\,a_n = a_1 \\cdot r^{n - 1}.\\,}$$\n\n"
                "**Suma de los primeros $n$ términos** (para $r \\neq 1$):\n\n"
                "$$\\boxed{\\,S_n = \\dfrac{a_1 (1 - r^n)}{1 - r}.\\,}$$\n\n"
                "(Si $r = 1$, la sucesión es constante y $S_n = n a_1$.)\n\n"
                "**Crecimiento exponencial.** Si $|r| > 1$, la sucesión crece (o decrece en magnitud) "
                "**exponencialmente**. Si $|r| < 1$, los términos tienden a 0."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Geométrica básica",
          problema_md="Para $5, 15, 45, 135, \\ldots$, halla $a_8$ y $S_8$.",
          pasos=[
              {"accion_md": (
                  "**Identificar.** $a_1 = 5$, $r = 15/5 = 3$."
              ),
               "justificacion_md": "Verificar: $45/15 = 3$ ✓.",
               "es_resultado": False},
              {"accion_md": (
                  "**$a_8$:** $a_8 = 5 \\cdot 3^7 = 5 \\cdot 2187 = 10935$."
              ),
               "justificacion_md": "$n - 1 = 7$.",
               "es_resultado": False},
              {"accion_md": (
                  "**$S_8$:** $S_8 = 5 (1 - 3^8)/(1 - 3) = 5 (1 - 6561)/(-2) = 5 \\cdot (-6560)/(-2) = 16400$."
              ),
               "justificacion_md": "Para $r > 1$, conviene reescribir como $a_1 (r^n - 1)/(r - 1)$ para evitar negativos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Aplicación: depreciación",
          problema_md="Una máquina cuesta \\$80\\,000 nueva y se deprecia 15% por año. ¿Cuánto vale después de 5 años?",
          pasos=[
              {"accion_md": (
                  "**Modelar.** Cada año el valor se multiplica por $1 - 0{,}15 = 0{,}85$. Geométrica con $a_1 = 80\\,000$ (valor inicial) y $r = 0{,}85$.\n\n"
                  "Si $a_1$ es el valor en año 0, entonces el valor en año $n$ es $a_{n + 1} = 80000 \\cdot 0{,}85^n$."
              ),
               "justificacion_md": "Cuidar la indexación: 'después de 5 años' = $n = 5$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular:** $80000 \\cdot (0{,}85)^5 = 80000 \\cdot 0{,}4437 \\approx \\$35\\,496$."
              ),
               "justificacion_md": "El valor cae casi a la mitad en 5 años.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Aritmética = lineal, Geométrica = exponencial.** Si graficás los términos:\n\n"
            "- Aritmética: los puntos caen sobre una **recta** ($a_n$ es función lineal de $n$).\n"
            "- Geométrica: los puntos caen sobre una **curva exponencial** ($a_n$ es función exponencial de $n$).\n\n"
            "Esto refleja la diferencia fundamental entre **sumar** una cantidad fija (lineal) y "
            "**multiplicar** por un factor fijo (exponencial).\n\n"
            "**El crecimiento exponencial es asombroso.** Una geométrica con $r = 1{,}05$ (5% anual) **duplica** "
            "su valor en aproximadamente 14 años (regla del 70: tiempo de duplicación $\\approx 70/r\\%$). "
            "Después de 100 años, multiplica por $(1{,}05)^{100} \\approx 131{,}5$. Por eso el interés "
            "compuesto a largo plazo es tan poderoso.\n\n"
            "**Origen de la fórmula de suma geométrica.** Sea $S_n = a + a r + a r^2 + \\cdots + a r^{n - 1}$. "
            "Multiplicando por $r$: $r S_n = a r + a r^2 + \\cdots + a r^n$. Restando: $S_n - r S_n = a - a r^n$, "
            "así $S_n (1 - r) = a (1 - r^n)$, despejando $S_n$. **Truco elegante.**"
        )),

        fig(
            "Comparación visual: dos sucesiones con los primeros 10 términos. "
            "Eje horizontal: índice n de 1 a 10. Eje vertical: valor del término. "
            "Sucesión aritmética con a_1 = 1, d = 2: 1, 3, 5, 7, 9, ... (puntos azules teal #06b6d4 cayendo sobre una recta). "
            "Sucesión geométrica con a_1 = 1, r = 1.5: 1, 1.5, 2.25, 3.375, ... (puntos ámbar #f59e0b sobre una curva exponencial creciente). "
            "Etiqueta: 'aritmética crece linealmente' vs 'geométrica crece exponencialmente'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para la aritmética con $a_1 = 5$ y $d = 3$, $a_{20} = $",
                  "opciones_md": [
                      "$60$",
                      "**$62$**",
                      "$65$",
                      "$23$",
                  ],
                  "correcta": "B",
                  "pista_md": "$a_n = a_1 + (n-1)d$.",
                  "explicacion_md": "$5 + 19 \\cdot 3 = 5 + 57 = 62$.",
              },
              {
                  "enunciado_md": "Si $S_{10}$ de una aritmética es 100 y $a_1 = 1$, entonces $a_{10} = $",
                  "opciones_md": [
                      "$10$",
                      "**$19$**",
                      "$20$",
                      "$50$",
                  ],
                  "correcta": "B",
                  "pista_md": "$S_{10} = 10 (a_1 + a_{10})/2 = 100$.",
                  "explicacion_md": "$a_1 + a_{10} = 20 \\Rightarrow a_{10} = 19$.",
              },
              {
                  "enunciado_md": "Para la geométrica $4, 12, 36, \\ldots$, la razón es:",
                  "opciones_md": [
                      "$4$",
                      "**$3$**",
                      "$8$",
                      "$12$",
                  ],
                  "correcta": "B",
                  "pista_md": "$r = a_2/a_1$.",
                  "explicacion_md": "$12/4 = 3$.",
              },
          ]),

        ej(
            "Identificar tipo",
            "¿Es $3, 9, 27, 81, \\ldots$ aritmética, geométrica o ninguna?",
            ["Calcular diferencias y razones."],
            (
                "Diferencias: $6, 18, 54$ (no constantes). Razones: $9/3 = 3, 27/9 = 3, 81/27 = 3$ (constantes). **Geométrica con $r = 3$.**"
            ),
        ),

        ej(
            "Suma aritmética",
            "Halla la suma de los primeros 100 enteros positivos: $1 + 2 + 3 + \\cdots + 100$.",
            ["$a_1 = 1, d = 1, a_{100} = 100$."],
            (
                "$S_{100} = 100 (1 + 100)/2 = 5050$. **El famoso resultado de Gauss niño.**"
            ),
        ),

        ej(
            "Aplicación interés",
            "Inviertes \\$1000 a 5% anual capitalizado anualmente. ¿Cuánto tienes después de 20 años?",
            ["Geométrica con $a_1 = 1000$ y $r = 1{,}05$."],
            (
                "Valor después de $n$ años: $1000 \\cdot 1{,}05^n$. Después de 20 años: $1000 \\cdot 1{,}05^{20} \\approx 1000 \\cdot 2{,}653 \\approx \\$2653$. **Más que se duplica.**"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir diferencia con razón.** Aritmética se reconoce por **diferencia** constante; geométrica por **cociente** constante.",
              "**Olvidar el $-1$ en la fórmula** $a_n = a_1 + (n - 1) d$. No es $a_1 + n d$.",
              "**Aplicar suma geométrica a $r = 1$:** la fórmula falla (división por cero). Caso especial.",
              "**Indexar mal:** 'después de 5 años' puede ser $a_5$ o $a_6$ según si empezamos en $n = 0$ o $n = 1$. Verificar.",
              "**Suponer que toda sucesión es aritmética o geométrica.** Existen muchas otras (Fibonacci, polinomial, etc.).",
          ]),

        b("resumen",
          puntos_md=[
              "**Aritmética:** $a_n = a_1 + (n - 1) d$. **Suma:** $S_n = n (a_1 + a_n)/2$.",
              "**Geométrica:** $a_n = a_1 r^{n - 1}$. **Suma:** $S_n = a_1 (1 - r^n)/(1 - r)$.",
              "**Aritmética crece lineal**; **geométrica crece exponencial**.",
              "**Aplicaciones:** aritméticas en conteo lineal, geométricas en interés compuesto y decaimiento.",
              "**Próxima lección:** ¿qué pasa cuando sumamos infinitos términos? Series.",
          ]),
    ]
    return {
        "id": "lec-prec-8-2-tipos-sucesiones",
        "title": "Tipos de sucesiones",
        "description": "Sucesiones aritméticas (diferencia común d) y geométricas (razón común r). Fórmulas del término general y de la suma de los primeros n términos. Aplicaciones a interés compuesto y depreciación.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# Series
# =====================================================================
def lesson_series():
    blocks = [
        b("texto", body_md=(
            "Una **serie** es una **suma de términos de una sucesión** — finita (los primeros $n$) o "
            "infinita (todos). Las series infinitas plantean una pregunta fundamental: **¿se puede sumar "
            "infinitos números y obtener un valor finito?**\n\n"
            "Sorprendentemente, **a veces sí**. Por ejemplo:\n\n"
            "$$\\dfrac{1}{2} + \\dfrac{1}{4} + \\dfrac{1}{8} + \\dfrac{1}{16} + \\cdots = 1.$$\n\n"
            "Otras veces **no** — la serie 'crece sin parar':\n\n"
            "$$1 + \\dfrac{1}{2} + \\dfrac{1}{3} + \\dfrac{1}{4} + \\cdots = \\infty.$$\n\n"
            "Esta lección presenta las **series finitas con fórmulas cerradas** (sumas de potencias, "
            "telescópicas) y los **criterios básicos de convergencia** para series infinitas (geométrica, "
            "$p$-serie).\n\n"
            "**Al terminar:**\n\n"
            "- Calculás sumas finitas de potencias usando fórmulas cerradas.\n"
            "- Reconocés y resolvés **series telescópicas**.\n"
            "- Distinguís **convergencia** vs **divergencia** de una serie infinita.\n"
            "- Sumás **series geométricas infinitas convergentes**."
        )),

        formulas(
            titulo="Sumas finitas de potencias",
            body=(
                "Resultados clásicos para las primeras potencias:\n\n"
                "$$\\sum_{k = 1}^{n} 1 = n.$$\n\n"
                "$$\\sum_{k = 1}^{n} k = \\dfrac{n (n + 1)}{2}.$$\n\n"
                "$$\\sum_{k = 1}^{n} k^2 = \\dfrac{n (n + 1)(2 n + 1)}{6}.$$\n\n"
                "$$\\sum_{k = 1}^{n} k^3 = \\left(\\dfrac{n (n + 1)}{2}\\right)^2 = \\dfrac{n^2 (n + 1)^2}{4}.$$\n\n"
                "**Notable:** $\\sum k^3 = \\bigl(\\sum k\\bigr)^2$ — la suma de cubos es el cuadrado de la suma.\n\n"
                "**Aplicación.** Combinando con las propiedades de $\\sum$, podés calcular cualquier suma polinomial:\n\n"
                "$$\\sum_{k = 1}^{n} (3 k^2 - 2 k + 1) = 3 \\sum k^2 - 2 \\sum k + \\sum 1.$$"
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Suma polinomial",
          problema_md="Calcula $\\sum_{k = 1}^{20} (k^2 + 3 k)$.",
          pasos=[
              {"accion_md": (
                  "**Separar:** $\\sum_{k=1}^{20} k^2 + 3 \\sum_{k=1}^{20} k$."
              ),
               "justificacion_md": "Linealidad de $\\sum$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar fórmulas:** $\\sum_{k=1}^{20} k^2 = 20 \\cdot 21 \\cdot 41/6 = 2870$. $\\sum_{k=1}^{20} k = 20 \\cdot 21/2 = 210$.\n\n"
                  "**Total:** $2870 + 3 \\cdot 210 = 2870 + 630 = 3500$."
              ),
               "justificacion_md": "Cálculo directo con las cerradas.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Series telescópicas",
          body_md=(
              "Una **serie telescópica** tiene la forma\n\n"
              "$$\\sum_{k = 1}^{n} (b_k - b_{k + 1}).$$\n\n"
              "Al expandir, los términos intermedios se **cancelan en cadena** (como un telescopio plegándose), "
              "y la suma se reduce a:\n\n"
              "$$\\boxed{\\,\\sum_{k = 1}^{n} (b_k - b_{k + 1}) = b_1 - b_{n + 1}.\\,}$$\n\n"
              "**Aplicación clásica.** $\\dfrac{1}{k(k + 1)} = \\dfrac{1}{k} - \\dfrac{1}{k + 1}$ (descomposición en fracciones parciales). Entonces\n\n"
              "$$\\sum_{k = 1}^{n} \\dfrac{1}{k (k + 1)} = \\sum_{k = 1}^{n} \\left(\\dfrac{1}{k} - \\dfrac{1}{k + 1}\\right) = 1 - \\dfrac{1}{n + 1}.$$\n\n"
              "Cuando $n \\to \\infty$, la suma telescópica converge a $1$.\n\n"
              "**Generalización.** Si encontrás una expresión como $b_k - b_{k + 1}$ (o $b_k - b_{k + m}$), podés sumar telescópicamente: solo sobreviven los **primeros $m$ y los últimos $m$ términos**."
          )),

        b("ejemplo_resuelto",
          titulo="Telescópica",
          problema_md="Calcula $\\sum_{k = 1}^{99} \\dfrac{1}{k (k + 1)}$.",
          pasos=[
              {"accion_md": (
                  "**Descomponer:** $\\dfrac{1}{k(k+1)} = \\dfrac{1}{k} - \\dfrac{1}{k+1}$ (fracciones parciales)."
              ),
               "justificacion_md": "Truco clave para reconocer la forma telescópica.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar telescópica:** $\\sum_{k=1}^{99} (1/k - 1/(k+1)) = 1/1 - 1/100 = 99/100$."
              ),
               "justificacion_md": "Primer término menos el (n+1)-ésimo del segundo factor.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Series infinitas: convergencia",
          body_md=(
              "Una **serie infinita** es una suma de infinitos términos:\n\n"
              "$$\\sum_{k = 1}^{\\infty} a_k = a_1 + a_2 + a_3 + \\cdots$$\n\n"
              "Se define como el **límite de las sumas parciales**:\n\n"
              "$$\\sum_{k = 1}^{\\infty} a_k = \\lim_{n \\to \\infty} S_n, \\quad \\text{donde } S_n = \\sum_{k = 1}^{n} a_k.$$\n\n"
              "**Convergente:** si el límite existe y es finito.\n\n"
              "**Divergente:** si el límite es $\\pm \\infty$ o no existe.\n\n"
              "**Test esencial (necesario, no suficiente):** si $\\sum a_k$ converge, entonces $a_k \\to 0$. "
              "**Equivalentemente** (contrapositivo): si $a_k \\not\\to 0$, la serie **diverge**.\n\n"
              "**Atención.** $a_k \\to 0$ NO basta para garantizar convergencia. Contraejemplo famoso: la serie armónica $\\sum 1/k$ diverge aunque $1/k \\to 0$."
          )),

        formulas(
            titulo="Series clásicas",
            body=(
                "**Serie geométrica:** $\\sum_{k = 0}^{\\infty} a r^k = a + a r + a r^2 + \\cdots$\n\n"
                "- Si **$|r| < 1$**: converge y suma $\\boxed{\\,S_\\infty = \\dfrac{a}{1 - r}.\\,}$\n"
                "- Si **$|r| \\geq 1$**: diverge.\n\n"
                "**Serie armónica:** $\\sum_{k = 1}^{\\infty} \\dfrac{1}{k} = 1 + \\dfrac{1}{2} + \\dfrac{1}{3} + \\cdots$ **diverge** (resultado clásico).\n\n"
                "**$p$-serie:** $\\sum_{k = 1}^{\\infty} \\dfrac{1}{k^p}$.\n\n"
                "- Converge sii $p > 1$.\n"
                "- Diverge si $p \\leq 1$ (la armónica es el caso $p = 1$).\n\n"
                "**Telescópicas infinitas:** $\\sum (b_k - b_{k+1})$ converge sii $b_n$ tiene límite finito; el valor es $b_1 - \\lim b_n$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Geométrica infinita",
          problema_md="Calcula $\\sum_{n = 0}^{\\infty} (1/3)^n$.",
          pasos=[
              {"accion_md": (
                  "**Identificar.** Geométrica con $a = 1$, $r = 1/3$. $|r| = 1/3 < 1$ → converge."
              ),
               "justificacion_md": "El test de $|r| < 1$ garantiza convergencia.",
               "es_resultado": False},
              {"accion_md": (
                  "**Suma:** $S = a/(1 - r) = 1/(1 - 1/3) = 1/(2/3) = 3/2$.\n\n"
                  "**Resultado:** $\\sum (1/3)^n = 3/2$."
              ),
               "justificacion_md": "Aplicar fórmula directa.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Decimal periódico como serie",
          problema_md="Expresa $0{,}\\overline{37} = 0{,}373737\\ldots$ como fracción usando una serie geométrica.",
          pasos=[
              {"accion_md": (
                  "**Reescribir:** $0{,}373737\\ldots = 0{,}37 + 0{,}0037 + 0{,}000037 + \\cdots = \\sum_{n = 0}^{\\infty} 0{,}37 \\cdot (0{,}01)^n$."
              ),
               "justificacion_md": "Geométrica con $a = 0{,}37$, $r = 0{,}01$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar suma:** $S = 0{,}37/(1 - 0{,}01) = 0{,}37/0{,}99 = 37/99$."
              ),
               "justificacion_md": "Confirmación: 37/99 = 0,3737... ✓.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué la armónica diverge a pesar de $1/k \\to 0$.** Aunque cada término es pequeño, los "
            "términos no decrecen **lo suficientemente rápido**. Una agrupación clásica:\n\n"
            "$$1 + \\dfrac{1}{2} + \\bigl(\\dfrac{1}{3} + \\dfrac{1}{4}\\bigr) + \\bigl(\\dfrac{1}{5} + \\dfrac{1}{6} + \\dfrac{1}{7} + \\dfrac{1}{8}\\bigr) + \\cdots$$\n\n"
            "Cada grupo entre paréntesis suma **al menos $1/2$**. Como hay infinitos grupos, la suma diverge.\n\n"
            "**Por qué $\\sum 1/k^2$ converge.** $1/k^2$ decae mucho más rápido que $1/k$. De hecho, "
            "$\\sum 1/k^2 = \\pi^2/6$ — un resultado famoso de Euler.\n\n"
            "**Geométrica como modelo paradigmático.** La fórmula $a/(1 - r)$ se usa en finanzas (perpetuidades), "
            "física (suma de reflexiones múltiples), economía (multiplicador keynesiano)."
        )),

        fig(
            "Visualización del concepto de convergencia: dos series con sus sumas parciales graficadas. "
            "Eje horizontal n (de 1 a 30), eje vertical S_n. "
            "Curva ámbar #f59e0b: sumas parciales de Σ (1/2)^k convergiendo asintóticamente a 1. Línea horizontal punteada en y=1. "
            "Curva teal #06b6d4: sumas parciales de la serie armónica Σ 1/k creciendo lentamente sin tope, etiquetada 'diverge'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\sum_{k=1}^{50} k = $",
                  "opciones_md": [
                      "$1250$",
                      "**$1275$**",
                      "$2500$",
                      "$50$",
                  ],
                  "correcta": "B",
                  "pista_md": "$n(n+1)/2 = 50 \\cdot 51/2$.",
                  "explicacion_md": "Fórmula de Gauss.",
              },
              {
                  "enunciado_md": "$\\sum_{n=0}^{\\infty} (1/2)^n = $",
                  "opciones_md": [
                      "$1$",
                      "**$2$**",
                      "$1/2$",
                      "Diverge",
                  ],
                  "correcta": "B",
                  "pista_md": "Geométrica con $r = 1/2$.",
                  "explicacion_md": "$1/(1 - 1/2) = 2$.",
              },
              {
                  "enunciado_md": "La serie armónica:",
                  "opciones_md": [
                      "Converge a 0",
                      "Converge a $\\pi$",
                      "**Diverge**",
                      "No tiene suma definida",
                  ],
                  "correcta": "C",
                  "pista_md": "Caso $p = 1$ de la $p$-serie.",
                  "explicacion_md": "Diverge a $+\\infty$ aunque sus términos tiendan a 0.",
              },
          ]),

        ej(
            "Suma cuadrados",
            "Calcula $\\sum_{k=1}^{15} k^2$.",
            ["$n(n+1)(2n+1)/6$."],
            (
                "$15 \\cdot 16 \\cdot 31 / 6 = 7440/6 = 1240$."
            ),
        ),

        ej(
            "Geométrica infinita",
            "Halla la suma de $4 + 4(0{,}3) + 4(0{,}3)^2 + \\cdots$",
            ["$a = 4$, $r = 0{,}3$."],
            (
                "$|r| = 0{,}3 < 1$ → converge. $S = 4/(1 - 0{,}3) = 4/0{,}7 = 40/7 \\approx 5{,}71$."
            ),
        ),

        ej(
            "Telescópica",
            "Calcula $\\sum_{k=1}^{\\infty} \\dfrac{1}{k(k+2)}$.",
            ["$\\dfrac{1}{k(k+2)} = \\dfrac{1}{2}\\left(\\dfrac{1}{k} - \\dfrac{1}{k+2}\\right)$."],
            (
                "$\\dfrac{1}{2} \\sum \\bigl(1/k - 1/(k+2)\\bigr) = \\dfrac{1}{2}(1 + 1/2) = 3/4$ (sobreviven dos términos por el desfase 2)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que $a_k \\to 0$ implica convergencia.** Falso (armónica).",
              "**Aplicar la fórmula geométrica con $|r| \\geq 1$.** No converge.",
              "**Confundir series finitas con infinitas.** Las finitas siempre 'convergen' (es solo una suma); las infinitas requieren análisis.",
              "**No descomponer fracciones parciales** antes de buscar telescopio.",
              "**Equivocar índices del límite inferior** en sigma. Verificar siempre.",
          ]),

        b("resumen",
          puntos_md=[
              "**Sumas finitas de potencias:** fórmulas cerradas para $\\sum k, \\sum k^2, \\sum k^3$.",
              "**Telescópicas:** $\\sum (b_k - b_{k+1}) = b_1 - b_{n+1}$.",
              "**Convergencia:** $\\lim S_n$ existe finito.",
              "**Geométrica infinita:** converge a $a/(1-r)$ sii $|r| < 1$.",
              "**$p$-serie:** converge sii $p > 1$. **Armónica** ($p = 1$) **diverge.**",
              "**Próxima lección:** la herramienta de demostración rigurosa que valida muchas de estas fórmulas — inducción.",
          ]),
    ]
    return {
        "id": "lec-prec-8-3-series",
        "title": "Series",
        "description": "Series finitas con fórmulas cerradas (sumas de potencias, telescópicas) y series infinitas (convergencia y divergencia). Series geométricas infinitas, serie armónica y p-serie.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# Inducción matemática
# =====================================================================
def lesson_induccion():
    blocks = [
        b("texto", body_md=(
            "La **inducción matemática** es una técnica de demostración para enunciados de la forma 'la "
            "propiedad $P(n)$ se cumple para todo $n \\in \\mathbb{N}$'. Se basa en una analogía elegante: "
            "**las fichas de dominó**.\n\n"
            "Si demuestro:\n\n"
            "- Que la **primera ficha** cae (caso base).\n"
            "- Que **cuando una ficha cae, también cae la siguiente** (paso inductivo).\n\n"
            "Entonces **todas** las fichas caen — porque la primera cae, lo que hace caer la segunda, lo que "
            "hace caer la tercera, y así sucesivamente.\n\n"
            "Es la herramienta fundamental para **demostrar fórmulas** que dependen de un entero $n$, "
            "como $\\sum k = n(n+1)/2$ o las que aparecen en sucesiones aritméticas/geométricas.\n\n"
            "**Al terminar:**\n\n"
            "- Conocés el **principio de inducción matemática**.\n"
            "- Aplicás el **esquema de tres pasos**: caso base, hipótesis inductiva, paso inductivo.\n"
            "- Demostrás identidades sumatorias y desigualdades por inducción."
        )),

        b("definicion",
          titulo="Principio de inducción matemática",
          body_md=(
              "Sea $P(n)$ una proposición que depende de un entero $n$. Si:\n\n"
              "**1. Caso base:** $P(1)$ es verdadero (o $P(n_0)$ para el primer $n_0$ relevante).\n\n"
              "**2. Paso inductivo:** para todo $k \\geq 1$ (o $\\geq n_0$), si $P(k)$ es verdadero entonces $P(k + 1)$ es verdadero.\n\n"
              "Entonces $P(n)$ es verdadero para **todo** $n \\geq 1$ (o $\\geq n_0$).\n\n"
              "**Estructura de una demostración:**\n\n"
              "- **Caso base.** Verificar $P(1)$ explícitamente (sustituir $n = 1$ y comprobar).\n"
              "- **Hipótesis inductiva (HI).** Asumir que $P(k)$ es verdadero para algún $k$ arbitrario.\n"
              "- **Paso inductivo.** Demostrar que la HI implica $P(k + 1)$. Típicamente:\n"
              "  - Partir del lado izquierdo de $P(k + 1)$.\n"
              "  - Identificar el lado izquierdo de $P(k)$ adentro.\n"
              "  - Aplicar HI para reemplazar.\n"
              "  - Manipular algebraicamente hasta obtener el lado derecho de $P(k + 1)$.\n\n"
              "**Conclusión:** 'Por el principio de inducción, $P(n)$ es verdadero para todo $n \\geq 1$'."
          )),

        b("ejemplo_resuelto",
          titulo="Suma de impares",
          problema_md="Demuestra por inducción que $1 + 3 + 5 + \\cdots + (2 n - 1) = n^2$ para todo $n \\geq 1$.",
          pasos=[
              {"accion_md": (
                  "**Caso base ($n = 1$):** lado izquierdo = $1$. Lado derecho = $1^2 = 1$. ✓"
              ),
               "justificacion_md": "Verificación explícita.",
               "es_resultado": False},
              {"accion_md": (
                  "**Hipótesis inductiva.** Asumir que $1 + 3 + 5 + \\cdots + (2 k - 1) = k^2$."
              ),
               "justificacion_md": "Suponemos que la fórmula vale para algún $k$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso inductivo.** Hay que probar que $1 + 3 + \\cdots + (2 k - 1) + (2 (k + 1) - 1) = (k + 1)^2$.\n\n"
                  "Lado izquierdo: $\\underbrace{1 + 3 + \\cdots + (2 k - 1)}_{= k^2 \\text{ por HI}} + (2 k + 1) = k^2 + 2 k + 1 = (k + 1)^2$. ✓"
              ),
               "justificacion_md": "Aplicamos HI a la suma de los primeros $k$ términos y simplificamos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Conclusión.** Por el principio de inducción matemática, $1 + 3 + 5 + \\cdots + (2 n - 1) = n^2$ para todo $n \\geq 1$."
              ),
               "justificacion_md": "Cierre formal de la demostración.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Suma de los primeros $n$ enteros",
          problema_md="Demuestra que $1 + 2 + 3 + \\cdots + n = \\dfrac{n (n + 1)}{2}$ para todo $n \\geq 1$.",
          pasos=[
              {"accion_md": (
                  "**Caso base ($n = 1$):** $1 = \\dfrac{1 \\cdot 2}{2} = 1$. ✓"
              ),
               "justificacion_md": "OK.",
               "es_resultado": False},
              {"accion_md": (
                  "**HI.** $1 + 2 + \\cdots + k = \\dfrac{k(k+1)}{2}$.\n\n"
                  "**Paso inductivo.** Probar $1 + 2 + \\cdots + k + (k + 1) = \\dfrac{(k+1)(k+2)}{2}$.\n\n"
                  "Lado izquierdo: $\\dfrac{k(k+1)}{2} + (k + 1) = \\dfrac{k(k+1) + 2(k+1)}{2} = \\dfrac{(k+1)(k+2)}{2}$. ✓"
              ),
               "justificacion_md": "Sacar factor común $(k + 1)$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Desigualdad por inducción",
          problema_md="Demuestra que $4 n < 2^n$ para todo $n \\geq 5$.",
          pasos=[
              {"accion_md": (
                  "**Caso base ($n = 5$):** $4 \\cdot 5 = 20$ y $2^5 = 32$. $20 < 32$. ✓\n\n"
                  "**HI.** $4 k < 2^k$ para algún $k \\geq 5$."
              ),
               "justificacion_md": "El caso base es $n = 5$, no $n = 1$ — la desigualdad falla para $n < 5$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso inductivo.** Probar $4 (k + 1) < 2^{k + 1}$.\n\n"
                  "Lado izquierdo: $4 (k + 1) = 4 k + 4 < 2^k + 4$ (por HI).\n\n"
                  "Como $k \\geq 5$, $2^k \\geq 32 > 4$, así $4 < 2^k$. Por tanto:\n\n"
                  "$2^k + 4 < 2^k + 2^k = 2 \\cdot 2^k = 2^{k+1}$.\n\n"
                  "Combinando: $4(k+1) < 2^{k+1}$. ✓"
              ),
               "justificacion_md": "Acotar el $4$ en términos de $2^k$ aprovecha la base $n \\geq 5$.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué inducción 'funciona' (no es circular).** El paso inductivo no asume lo que se quiere "
            "probar para todo $n$; solo asume lo que vale para un $k$ específico (HI) y demuestra que vale "
            "para el siguiente. Combinado con el caso base, **se desencadena** la verdad para todos: $P(1)$ "
            "es cierto (base), entonces por paso inductivo $P(2)$, entonces $P(3)$, etc.\n\n"
            "**Por qué se necesita el caso base.** Sin él, el dominó podría no empezar. Por ejemplo, "
            "$P(n)$: '$n = n + 1$' satisface trivialmente el paso inductivo ('si $k = k+1$ entonces $k+1 = k+2$', "
            "lógicamente válido sumando 1) — pero falla el caso base, y la afirmación es falsa para todo $n$.\n\n"
            "**Versiones alternativas de inducción:**\n\n"
            "- **Inducción fuerte:** asumir $P(1), P(2), \\ldots, P(k)$ todas verdaderas. Útil cuando para "
            "probar $P(k+1)$ se necesita información de varios casos anteriores (Fibonacci, recursividades complejas).\n"
            "- **Inducción descendente:** parte de un caso fácil más alto y desciende — útil en algunas demostraciones específicas."
        )),

        fig(
            "Visualización del principio de inducción como fichas de dominó. "
            "Una fila de fichas de dominó numeradas 1, 2, 3, 4, 5, ... "
            "La primera ficha (n=1) representada cayendo (etiquetada 'caso base'). "
            "Una flecha curva de la ficha k a la k+1 etiquetada 'paso inductivo: si cae k, cae k+1'. "
            "Las fichas siguientes inclinadas mostrando la onda de caída en cadena. "
            "Acentos teal #06b6d4 para fichas en pie, ámbar #f59e0b para fichas cayendo. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El principio de inducción requiere demostrar:",
                  "opciones_md": [
                      "Solo el caso base",
                      "Solo el paso inductivo",
                      "**Caso base **y** paso inductivo**",
                      "Ningún caso particular",
                  ],
                  "correcta": "C",
                  "pista_md": "Ambos son necesarios.",
                  "explicacion_md": "Sin caso base no empieza la cadena; sin paso inductivo no se propaga.",
              },
              {
                  "enunciado_md": "En el paso inductivo se asume:",
                  "opciones_md": [
                      "$P(n)$ para todo $n$",
                      "**$P(k)$ para algún $k$ y se demuestra $P(k+1)$**",
                      "$P(1)$ solamente",
                      "$P(n+1)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Esa es la HI.",
                  "explicacion_md": "Hipótesis inductiva: asumir vale para $k$, demostrar para $k+1$.",
              },
              {
                  "enunciado_md": "Si demostrás $P(n)$ por inducción con caso base $n_0 = 5$, conocés:",
                  "opciones_md": [
                      "$P(n)$ para todo $n \\in \\mathbb{N}$",
                      "**$P(n)$ para todo $n \\geq 5$**",
                      "$P(n)$ para $n \\leq 5$",
                      "Solo $P(5)$",
                  ],
                  "correcta": "B",
                  "pista_md": "La inducción solo concluye desde el caso base hacia arriba.",
                  "explicacion_md": "Para $n < 5$, el resultado puede ser falso — hay que verificar caso por caso.",
              },
          ]),

        ej(
            "Suma de cuadrados",
            "Demuestra por inducción que $\\sum_{k=1}^{n} k^2 = n(n+1)(2n+1)/6$.",
            ["Caso base $n = 1$, después HI y paso."],
            (
                "**Base:** $n = 1$: LI = 1, LD = $1 \\cdot 2 \\cdot 3/6 = 1$. ✓\n\n"
                "**HI:** $\\sum_{k=1}^{m} k^2 = m(m+1)(2m+1)/6$.\n\n"
                "**Paso:** $\\sum_{k=1}^{m+1} k^2 = m(m+1)(2m+1)/6 + (m+1)^2 = (m+1)[m(2m+1) + 6(m+1)]/6 = (m+1)(2m^2 + 7m + 6)/6 = (m+1)(m+2)(2m+3)/6$, que es la fórmula con $n = m + 1$. ✓"
            ),
        ),

        ej(
            "Divisibilidad",
            "Demuestra que $7^n - 1$ es divisible por 6 para todo $n \\geq 1$.",
            ["HI: $7^k - 1 = 6 m$. Probar $7^{k+1} - 1$ múltiplo de 6."],
            (
                "**Base:** $7^1 - 1 = 6 = 6 \\cdot 1$ ✓.\n\n"
                "**HI:** $7^k - 1 = 6 m$ para algún $m \\in \\mathbb{Z}$, así $7^k = 6m + 1$.\n\n"
                "**Paso:** $7^{k+1} - 1 = 7 \\cdot 7^k - 1 = 7(6m + 1) - 1 = 42 m + 6 = 6 (7m + 1)$. **Divisible por 6.** ✓"
            ),
        ),

        ej(
            "Identidad",
            "Demuestra que $1 \\cdot 2 + 2 \\cdot 3 + \\cdots + n(n+1) = n(n+1)(n+2)/3$.",
            ["Inducción estándar."],
            (
                "Base: $n = 1$: $1 \\cdot 2 = 2 = 1 \\cdot 2 \\cdot 3/3$. ✓\n\n"
                "HI: $\\sum_{k=1}^{m} k(k+1) = m(m+1)(m+2)/3$.\n\n"
                "Paso: $\\sum_{k=1}^{m+1} = m(m+1)(m+2)/3 + (m+1)(m+2) = (m+1)(m+2)[m/3 + 1] = (m+1)(m+2)(m+3)/3$. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el caso base.** Sin él, todo el argumento es inválido.",
              "**Asumir lo que se quiere probar** en el paso inductivo (circularidad). HI es solo para $k$, no para $k+1$.",
              "**Probar solo el caso base sin paso inductivo.** Demuestra solo $P(1)$, no para todo $n$.",
              "**Plantear el paso inductivo al revés** (asumir $P(k+1)$ para probar $P(k)$).",
              "**Concluir 'por inducción' sin haber escrito explícitamente la HI** y el paso.",
          ]),

        b("resumen",
          puntos_md=[
              "**Principio:** $P(1)$ + 'si $P(k)$ entonces $P(k+1)$' $\\Rightarrow$ $P(n)$ para todo $n \\geq 1$.",
              "**Estructura de la demostración:** caso base, hipótesis inductiva, paso inductivo, conclusión.",
              "**Aplicaciones:** demostrar identidades sumatorias, desigualdades, divisibilidades, propiedades recursivas.",
              "**Analogía:** las fichas de dominó. Si la primera cae y cada una empuja a la siguiente, todas caen.",
              "**Próxima lección:** una aplicación concreta y elegante — el teorema del binomio de Newton.",
          ]),
    ]
    return {
        "id": "lec-prec-8-4-induccion",
        "title": "Inducción matemática",
        "description": "Principio de inducción matemática para demostrar enunciados que dependen de un natural n. Esquema en tres pasos: caso base, hipótesis inductiva y paso inductivo. Aplicaciones a identidades sumatorias, desigualdades y divisibilidades.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# Teorema del binomio
# =====================================================================
def lesson_binomio():
    blocks = [
        b("texto", body_md=(
            "El **teorema del binomio** (de Newton) da una fórmula explícita para expandir $(a + b)^n$ "
            "para cualquier $n \\in \\mathbb{N}$:\n\n"
            "$$\\boxed{\\,(a + b)^n = \\sum_{k = 0}^{n} \\binom{n}{k} a^{n - k} b^k.\\,}$$\n\n"
            "Es una de las herramientas más usadas en álgebra, combinatoria, probabilidad, cálculo de "
            "derivadas/integrales y series de potencias.\n\n"
            "Para usarlo necesitamos:\n\n"
            "- El **factorial** $n!$.\n"
            "- El **coeficiente binomial** $\\binom{n}{k}$.\n"
            "- La **propiedad de Pascal** que da el famoso **triángulo de Pascal**.\n\n"
            "**Aplicaciones famosas:**\n\n"
            "- Expandir potencias de binomios sin multiplicar manualmente.\n"
            "- **Combinatoria:** $\\binom{n}{k}$ cuenta combinaciones de $k$ elementos entre $n$.\n"
            "- **Probabilidad:** distribución binomial.\n\n"
            "**Al terminar:**\n\n"
            "- Calculás factoriales y coeficientes binomiales.\n"
            "- Aplicás la **propiedad de Pascal** y construís el triángulo.\n"
            "- Expandís $(a + b)^n$ usando el teorema del binomio.\n"
            "- Hallás un **término específico** sin expandir todo."
        )),

        b("definicion",
          titulo="Factorial",
          body_md=(
              "Para $n \\in \\mathbb{N}$, el **factorial** de $n$ es\n\n"
              "$$n! = n \\cdot (n - 1) \\cdot (n - 2) \\cdots 2 \\cdot 1.$$\n\n"
              "Por convención, $0! = 1$.\n\n"
              "**Recursividad:** $n! = n \\cdot (n - 1)!$ para $n \\geq 1$.\n\n"
              "**Valores pequeños:**\n\n"
              "$$0! = 1, \\quad 1! = 1, \\quad 2! = 2, \\quad 3! = 6, \\quad 4! = 24, \\quad 5! = 120, \\quad 6! = 720.$$\n\n"
              "**Crecimiento.** El factorial crece **muy rápido** — más rápido que cualquier exponencial polinomial. $10! = 3{,}6 \\cdot 10^6$ y $20! \\approx 2{,}4 \\cdot 10^{18}$.\n\n"
              "**Interpretación combinatoria.** $n!$ es el número de **permutaciones** (ordenamientos) de $n$ objetos distintos."
          )),

        b("definicion",
          titulo="Coeficiente binomial",
          body_md=(
              "Para $n, k$ enteros con $0 \\leq k \\leq n$, el **coeficiente binomial** $\\binom{n}{k}$ ('$n$ sobre $k$') es\n\n"
              "$$\\binom{n}{k} = \\dfrac{n!}{k! (n - k)!}.$$\n\n"
              "Se lee como **'combinaciones de $n$ tomadas de a $k$'**.\n\n"
              "**Interpretación combinatoria.** $\\binom{n}{k}$ cuenta el número de formas de **elegir $k$ objetos entre $n$ distintos**, sin importar el orden.\n\n"
              "**Propiedades clave:**\n\n"
              "- $\\binom{n}{0} = \\binom{n}{n} = 1$.\n"
              "- $\\binom{n}{1} = \\binom{n}{n - 1} = n$.\n"
              "- **Simetría:** $\\binom{n}{k} = \\binom{n}{n - k}$.\n"
              "- **Identidad de Pascal:** $\\binom{n}{k - 1} + \\binom{n}{k} = \\binom{n + 1}{k}$.\n\n"
              "**Ejemplo.** $\\binom{6}{2} = \\dfrac{6!}{2! \\cdot 4!} = \\dfrac{720}{2 \\cdot 24} = 15$. Significa: hay 15 formas de elegir 2 elementos entre 6."
          )),

        formulas(
            titulo="Triángulo de Pascal",
            body=(
                "Los coeficientes binomiales $\\binom{n}{k}$ se organizan en un arreglo triangular llamado **triángulo de Pascal**. Cada fila corresponde a un valor de $n$:\n\n"
                "```\n"
                "n=0:        1\n"
                "n=1:       1 1\n"
                "n=2:      1 2 1\n"
                "n=3:     1 3 3 1\n"
                "n=4:    1 4 6 4 1\n"
                "n=5:   1 5 10 10 5 1\n"
                "n=6:  1 6 15 20 15 6 1\n"
                "```\n\n"
                "**Construcción.** Cada entrada (excepto los bordes que valen 1) es la **suma de las dos entradas arriba** — esto es exactamente la identidad de Pascal $\\binom{n}{k - 1} + \\binom{n}{k} = \\binom{n + 1}{k}$.\n\n"
                "**Uso.** La fila $n$-ésima da los coeficientes de $(a + b)^n$. Ejemplo: $(a + b)^4 = 1 a^4 + 4 a^3 b + 6 a^2 b^2 + 4 a b^3 + 1 b^4$."
            ),
        ),

        formulas(
            titulo="Teorema del binomio",
            body=(
                "Para $n \\in \\mathbb{N}$:\n\n"
                "$$\\boxed{\\,(a + b)^n = \\sum_{k = 0}^{n} \\binom{n}{k} a^{n - k} b^k.\\,}$$\n\n"
                "Expandido:\n\n"
                "$$(a + b)^n = \\binom{n}{0} a^n + \\binom{n}{1} a^{n - 1} b + \\binom{n}{2} a^{n - 2} b^2 + \\cdots + \\binom{n}{n} b^n.$$\n\n"
                "**Patrón de cada término:**\n\n"
                "- Coeficiente: $\\binom{n}{k}$.\n"
                "- Potencia de $a$: $n - k$ (decrece de $n$ a $0$).\n"
                "- Potencia de $b$: $k$ (crece de $0$ a $n$).\n"
                "- **La suma de exponentes es siempre $n$.**\n\n"
                "**Hay $n + 1$ términos** en la expansión.\n\n"
                "**Término general** (el $(r + 1)$-ésimo, con $r = 0, 1, \\ldots, n$):\n\n"
                "$$T_{r + 1} = \\binom{n}{r} a^{n - r} b^r.$$"
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Expandir $(a + b)^5$",
          problema_md="Expande $(a + b)^5$ usando el teorema del binomio.",
          pasos=[
              {"accion_md": (
                  "**Coeficientes de la fila 5 del triángulo:** $1, 5, 10, 10, 5, 1$."
              ),
               "justificacion_md": "$\\binom{5}{0}, \\binom{5}{1}, \\ldots, \\binom{5}{5}$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Expandir:**\n\n"
                  "$(a + b)^5 = a^5 + 5 a^4 b + 10 a^3 b^2 + 10 a^2 b^3 + 5 a b^4 + b^5$.\n\n"
                  "**Verificar:** suma de exponentes en cada término es 5 ✓. Hay 6 términos ✓."
              ),
               "justificacion_md": "Patrón claro: potencias decrecen/crecen, coeficientes simétricos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Expandir con coeficientes",
          problema_md="Expande $(2 - 3 x)^4$.",
          pasos=[
              {"accion_md": (
                  "**Identificar.** $a = 2$, $b = -3 x$, $n = 4$. Coeficientes de la fila 4: $1, 4, 6, 4, 1$."
              ),
               "justificacion_md": "El signo negativo va en $b$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Expandir cuidando signos** (negativo de $b$ produce signo alternado):\n\n"
                  "$(2 - 3 x)^4 = 1 \\cdot 2^4 + 4 \\cdot 2^3 (-3 x) + 6 \\cdot 2^2 (-3 x)^2 + 4 \\cdot 2 (-3 x)^3 + 1 (-3 x)^4$.\n\n"
                  "$= 16 - 96 x + 6 \\cdot 4 \\cdot 9 x^2 - 4 \\cdot 2 \\cdot 27 x^3 + 81 x^4$.\n\n"
                  "$= 16 - 96 x + 216 x^2 - 216 x^3 + 81 x^4$."
              ),
               "justificacion_md": "Cuidar potencias y signos cuidadosamente.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Hallar un término específico",
          problema_md="¿Cuál es el coeficiente de $x^8$ en la expansión de $\\left(x^2 + \\dfrac{1}{x}\\right)^{10}$?",
          pasos=[
              {"accion_md": (
                  "**Término general** con $a = x^2$, $b = 1/x$, $n = 10$:\n\n"
                  "$T_{r + 1} = \\binom{10}{r} (x^2)^{10 - r} (1/x)^r = \\binom{10}{r} x^{20 - 2 r - r} = \\binom{10}{r} x^{20 - 3 r}$."
              ),
               "justificacion_md": "Combinar potencias de $x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Buscar exponente $8$:** $20 - 3 r = 8 \\Rightarrow r = 4$.\n\n"
                  "**Coeficiente:** $\\binom{10}{4} = \\dfrac{10!}{4! \\cdot 6!} = \\dfrac{10 \\cdot 9 \\cdot 8 \\cdot 7}{4 \\cdot 3 \\cdot 2 \\cdot 1} = 210$.\n\n"
                  "**Coeficiente de $x^8$ es $210$.**"
              ),
               "justificacion_md": "Sin expandir todo el binomio.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué los coeficientes son $\\binom{n}{k}$.** Al expandir $(a + b)^n = \\underbrace{(a + b)(a + b) \\cdots (a + b)}_{n \\text{ factores}}$, "
            "cada término del resultado es un producto donde de cada factor elegimos $a$ o $b$. Para obtener "
            "$a^{n - k} b^k$, hay que elegir $b$ de exactamente $k$ factores (y $a$ de los restantes). "
            "Esa cantidad de elecciones es $\\binom{n}{k}$.\n\n"
            "**Por qué Pascal funciona.** Cada coeficiente del triángulo de Pascal cuenta combinaciones; "
            "la regla 'suma de los dos arriba' es la identidad de Pascal traducida combinatoriamente: las "
            "combinaciones de $n+1$ tomadas de a $k$ se dividen en las que **incluyen** el último elemento "
            "(restantes $\\binom{n}{k-1}$) y las que **no** lo incluyen ($\\binom{n}{k}$).\n\n"
            "**Aplicaciones más allá del álgebra.** El teorema del binomio se generaliza al **teorema del "
            "binomio para exponentes reales** (serie de Taylor de $(1 + x)^\\alpha$), aparece en distribuciones "
            "de probabilidad, en mecánica cuántica (estados de espín), en análisis combinatorio, etc."
        )),

        fig(
            "Triángulo de Pascal hasta la fila 6 dibujado de forma estética. "
            "Cada número en un círculo o en posición simétrica, formando un triángulo equilátero. "
            "Filas (de arriba a abajo): 1; 1 1; 1 2 1; 1 3 3 1; 1 4 6 4 1; 1 5 10 10 5 1; 1 6 15 20 15 6 1. "
            "Flechas curvas mostrando que dos números adyacentes en una fila suman al de abajo entre ellos. "
            "Acento teal #06b6d4 para los bordes (todos 1), ámbar #f59e0b para los interiores. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\binom{8}{3} = $",
                  "opciones_md": [
                      "$24$",
                      "**$56$**",
                      "$120$",
                      "$336$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\binom{8}{3} = 8!/(3! \\cdot 5!) = (8 \\cdot 7 \\cdot 6)/(3 \\cdot 2)$.",
                  "explicacion_md": "$56$.",
              },
              {
                  "enunciado_md": "Cuántos términos tiene la expansión de $(a + b)^{12}$:",
                  "opciones_md": [
                      "$12$",
                      "**$13$**",
                      "$24$",
                      "$11$",
                  ],
                  "correcta": "B",
                  "pista_md": "$n + 1$ términos.",
                  "explicacion_md": "Desde $k = 0$ hasta $k = n = 12$, son 13 términos.",
              },
              {
                  "enunciado_md": "El término medio de $(a + b)^6$ es:",
                  "opciones_md": [
                      "$15 a^3 b^3$",
                      "**$20 a^3 b^3$**",
                      "$10 a^3 b^3$",
                      "$6 a^3 b^3$",
                  ],
                  "correcta": "B",
                  "pista_md": "Término del medio: $r = 3$, $\\binom{6}{3} = 20$.",
                  "explicacion_md": "El término del medio en una expansión de orden par tiene índice $n/2$.",
              },
          ]),

        ej(
            "Coeficiente binomial",
            "Calcula $\\binom{10}{3}$.",
            ["$10!/(3! \\cdot 7!)$."],
            (
                "$\\binom{10}{3} = (10 \\cdot 9 \\cdot 8)/(3 \\cdot 2 \\cdot 1) = 720/6 = 120$."
            ),
        ),

        ej(
            "Expansión",
            "Expandí $(x + 2)^4$.",
            ["Coeficientes 1, 4, 6, 4, 1."],
            (
                "$(x + 2)^4 = x^4 + 4 x^3 \\cdot 2 + 6 x^2 \\cdot 4 + 4 x \\cdot 8 + 16 = x^4 + 8 x^3 + 24 x^2 + 32 x + 16$."
            ),
        ),

        ej(
            "Término específico",
            "Halla el término que contiene $x^5$ en la expansión de $(2 x - 1)^7$.",
            ["Término general: $\\binom{7}{r}(2x)^{7-r}(-1)^r$."],
            (
                "Buscar $7 - r = 5$, así $r = 2$. Término: $\\binom{7}{2}(2x)^5(-1)^2 = 21 \\cdot 32 x^5 \\cdot 1 = 672 x^5$. **Coeficiente:** 672."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\binom{n}{k}$ con $n^k$.** Son cosas distintas: $\\binom{6}{2} = 15$ pero $6^2 = 36$.",
              "**Olvidar el factor de signo** cuando $b$ es negativo: $(a - b)^n = (a + (-b))^n$, los términos alternan en signo.",
              "**Calcular $\\binom{n}{k}$ con factoriales completos** cuando $k$ es pequeño. Mejor cancelar: $\\binom{n}{k} = n(n-1)\\cdots(n-k+1)/k!$.",
              "**Confundir el número de términos** ($n + 1$, no $n$).",
              "**Ignorar la simetría** $\\binom{n}{k} = \\binom{n}{n-k}$ cuando $k$ está cerca de $n$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Factorial:** $n! = n(n-1)\\cdots 1$. $0! = 1$.",
              "**Coeficiente binomial:** $\\binom{n}{k} = n!/(k!(n-k)!)$. Cuenta combinaciones.",
              "**Triángulo de Pascal:** filas son los $\\binom{n}{k}$. Cada interior es la suma de los dos de arriba.",
              "**Teorema del binomio:** $(a + b)^n = \\sum_{k=0}^{n} \\binom{n}{k} a^{n-k} b^k$.",
              "**Término general:** $T_{r+1} = \\binom{n}{r} a^{n-r} b^r$.",
              "**Cierre del capítulo y del curso.** Hemos completado los 8 capítulos: fundamentos, funciones, polinomiales/racionales, exponenciales/logarítmicas, trigonometría, trigonometría analítica, complejos, sucesiones y series. **¡Estás listo para el cálculo!**",
          ]),
    ]
    return {
        "id": "lec-prec-8-5-binomio",
        "title": "Teorema del binomio",
        "description": "Factorial n!, coeficiente binomial C(n,k) = n!/(k!(n-k)!), triángulo de Pascal e identidad de Pascal. Teorema del binomio (a+b)^n = Σ C(n,k) a^{n-k} b^k. Cálculo de términos específicos sin expandir.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 5,
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

    chapter_id = "ch-prec-sucesiones-series"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Sucesiones y Series",
        "description": (
            "Sucesiones (explícitas y recursivas), Fibonacci, sucesiones aritméticas y geométricas con sus "
            "fórmulas de término general y suma. Series finitas e infinitas, convergencia. Inducción "
            "matemática como técnica de demostración. Coeficientes binomiales, triángulo de Pascal y "
            "teorema del binomio."
        ),
        "order": 8,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_sucesiones,
        lesson_tipos_sucesiones,
        lesson_series,
        lesson_induccion,
        lesson_binomio,
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
        f"✅ Capítulo 8 — Sucesiones y Series listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
