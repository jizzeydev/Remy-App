"""
Seed del curso Precálculo — Capítulo 1: Fundamentos.

Crea el curso 'precalculo' (si no existe) y siembra el Cap. 1
con sus 8 lecciones:

  - Números reales
  - Conjuntos e intervalos
  - Potencias y raíces
  - Expresiones algebraicas
  - Factorización
  - Expresiones racionales
  - Ecuaciones
  - Inecuaciones

Basado en los Apuntes/Clase de Se Remonta (preparación PAES y curso
universitario inicial). Idempotente.
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
# Números reales
# =====================================================================
def lesson_numeros_reales():
    blocks = [
        b("texto", body_md=(
            "El **conjunto de los números reales** $\\mathbb{R}$ es el universo donde vive todo el "
            "precálculo y el cálculo. Lo construimos por capas, partiendo de los más simples (los que "
            "usamos para contar) y agregando nuevos números cada vez que necesitamos resolver una operación "
            "que no podíamos resolver antes:\n\n"
            "- Para **contar** alcanzan los naturales.\n"
            "- Para tener **resta** sin restricciones, necesitamos los enteros (con los negativos).\n"
            "- Para tener **división** sin restricciones, necesitamos los racionales (las fracciones).\n"
            "- Para que toda **medida geométrica** sea posible (como la diagonal de un cuadrado de lado 1, "
            "que mide $\\sqrt{2}$), necesitamos los irracionales.\n\n"
            "Juntos, racionales e irracionales forman los **reales** $\\mathbb{R}$.\n\n"
            "**Al terminar:**\n\n"
            "- Reconoces los conjuntos $\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{Q} \\subset \\mathbb{R}$.\n"
            "- Distingues racionales e irracionales por su expansión decimal.\n"
            "- Aplicas las propiedades algebraicas básicas (conmutativa, asociativa, distributiva)."
        )),

        b("definicion",
          titulo="Los conjuntos numéricos",
          body_md=(
              "**Naturales** $\\mathbb{N} = \\{1, 2, 3, 4, \\ldots\\}$ — los números para contar.\n\n"
              "**Enteros** $\\mathbb{Z} = \\{\\ldots, -3, -2, -1, 0, 1, 2, 3, \\ldots\\}$ — agregan el cero y los negativos.\n\n"
              "**Racionales** $\\mathbb{Q} = \\left\\{\\dfrac{m}{n} : m \\in \\mathbb{Z},\\, n \\in \\mathbb{Z},\\, n \\neq 0\\right\\}$ — fracciones de enteros. "
              "Ejemplos: $\\dfrac{3}{2} = 1{,}5$, $\\dfrac{1}{3} = 0{,}333\\ldots$, $7 = \\dfrac{7}{1}$.\n\n"
              "**Irracionales** — los que **no** se pueden escribir como fracción. Tienen expansión decimal "
              "infinita y no periódica. Ejemplos: $\\sqrt{2} = 1{,}41421\\ldots$, $\\pi = 3{,}14159\\ldots$, $e \\approx 2{,}71828\\ldots$.\n\n"
              "**Reales** $\\mathbb{R} = \\mathbb{Q} \\cup \\{\\text{irracionales}\\}$ — todos los anteriores.\n\n"
              "**Inclusiones:** $\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{Q} \\subset \\mathbb{R}$. Cada nuevo conjunto **contiene** a los anteriores."
          )),

        formulas(
            titulo="Cómo distinguir racional de irracional",
            body=(
                "**Criterio de la expansión decimal.** Un número real tiene **una** de las tres formas:\n\n"
                "1. **Decimal finito** (p. ej. $0{,}25$, $1{,}5$). **Racional.**\n"
                "2. **Decimal infinito periódico** (p. ej. $0{,}333\\ldots = 1/3$, $0{,}\\overline{142857} = 1/7$). **Racional.**\n"
                "3. **Decimal infinito no periódico** (p. ej. $\\sqrt{2}, \\pi$). **Irracional.**\n\n"
                "**Reglas útiles:**\n\n"
                "- $\\sqrt{n}$ es racional **solo si** $n$ es un cuadrado perfecto. $\\sqrt{4} = 2$ ✓ racional. $\\sqrt{5}$ irracional.\n"
                "- La suma de un racional con un irracional es **irracional**.\n"
                "- El producto de un racional **no nulo** con un irracional es **irracional**.\n"
                "- Suma o producto de dos irracionales **puede** ser racional. Ej.: $\\sqrt{2} + (-\\sqrt{2}) = 0$, $\\sqrt{2} \\cdot \\sqrt{2} = 2$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Clasificar números",
          problema_md=(
              "Para cada uno indica el conjunto más restrictivo al que pertenece:\n\n"
              "**(a)** $-7$, **(b)** $0{,}666\\ldots$, **(c)** $\\sqrt{9}$, **(d)** $\\sqrt{7}$, **(e)** $0$, **(f)** $\\dfrac{22}{7}$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $-7$: entero negativo. **$\\mathbb{Z}$** (también $\\mathbb{Q}, \\mathbb{R}$)."
              ),
               "justificacion_md": "No es natural por ser negativo.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $0{,}666\\ldots = 2/3$: decimal periódico → racional. **$\\mathbb{Q}$**."
              ),
               "justificacion_md": "Periódico = racional.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** $\\sqrt{9} = 3$: natural. **$\\mathbb{N}$**.\n\n"
                  "**(d)** $\\sqrt{7}$: 7 no es cuadrado perfecto → irracional. **$\\mathbb{R} \\setminus \\mathbb{Q}$**.\n\n"
                  "**(e)** $0$: entero (no natural en la convención $\\mathbb{N}$ desde 1). **$\\mathbb{Z}$**.\n\n"
                  "**(f)** $22/7 \\approx 3{,}142857\\ldots$: aunque se usa como aproximación de $\\pi$, **es** racional. **$\\mathbb{Q}$**. ¡No confundir con $\\pi$!"
              ),
               "justificacion_md": "Trampa común: $22/7 \\neq \\pi$. Una es racional, la otra no.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Propiedades algebraicas básicas",
            body=(
                "Para todo $a, b, c \\in \\mathbb{R}$:\n\n"
                "**Conmutativa:** $a + b = b + a$, $a \\cdot b = b \\cdot a$.\n\n"
                "**Asociativa:** $(a + b) + c = a + (b + c)$, $(a \\cdot b) \\cdot c = a \\cdot (b \\cdot c)$.\n\n"
                "**Distributiva:** $a (b + c) = a b + a c$.\n\n"
                "**Elementos neutros:** $a + 0 = a$, $a \\cdot 1 = a$.\n\n"
                "**Inversos:** $a + (-a) = 0$. Si $a \\neq 0$, $a \\cdot \\dfrac{1}{a} = 1$.\n\n"
                "**Recta numérica.** Cada real corresponde a un punto único en una recta orientada. "
                "El **orden** $a < b$ significa que $a$ está a la izquierda de $b$ en la recta. "
                "Si $a < b$ y $b < c$, entonces $a < c$ (transitividad)."
            ),
        ),

        fig(
            "Recta numérica horizontal con marcas en -3, -2, -1, 0, 1, 2, 3. "
            "Puntos destacados: -7/2 (entre -4 y -3, etiquetado), 0 (en negro), √2 ≈ 1.41 (etiquetado), π ≈ 3.14 (etiquetado, fuera de la región principal o al borde derecho). "
            "Acentos teal #06b6d4 para racionales y ámbar #f59e0b para irracionales. "
            "Etiqueta superior 'Recta de los números reales ℝ'. " + STYLE
        ),

        b("intuicion", body_md=(
            "**¿Por qué necesitamos los irracionales?**\n\n"
            "El descubrimiento de los irracionales es uno de los grandes momentos de la historia de las "
            "matemáticas. Los pitagóricos (siglo VI a.C.) creían que **todo** se podía expresar como cociente "
            "de enteros — hasta que demostraron que la **diagonal de un cuadrado de lado 1** mide $\\sqrt{2}$, "
            "que **no** es racional.\n\n"
            "Sin los irracionales, la recta numérica tendría 'agujeros' en lugares como $\\sqrt{2}, \\pi, e$. "
            "Los reales **completan** la recta — entre dos números cualesquiera siempre hay otro. Esa "
            "**propiedad de completitud** es el cimiento de todo el cálculo."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál de estos números es **irracional**?",
                  "opciones_md": [
                      "$0{,}5$",
                      "$\\sqrt{16}$",
                      "**$\\sqrt{3}$**",
                      "$\\dfrac{22}{7}$",
                  ],
                  "correcta": "C",
                  "pista_md": "Buscar el que tenga decimal infinito no periódico.",
                  "explicacion_md": "$\\sqrt{3}$ no es cuadrado perfecto. Los demás son racionales: $0{,}5 = 1/2$, $\\sqrt{16} = 4$, $22/7$ es fracción.",
              },
              {
                  "enunciado_md": "$\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{Q} \\subset \\mathbb{R}$ significa:",
                  "opciones_md": [
                      "Son disjuntos",
                      "**Cada conjunto está incluido en el siguiente**",
                      "Son iguales",
                      "Es una intersección",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\subset$ es 'subconjunto'.",
                  "explicacion_md": "Cada natural es entero, cada entero es racional, cada racional es real.",
              },
              {
                  "enunciado_md": "$3 \\cdot (4 + 5) = 3 \\cdot 4 + 3 \\cdot 5$ es la propiedad:",
                  "opciones_md": [
                      "Conmutativa",
                      "Asociativa",
                      "**Distributiva**",
                      "De inversos",
                  ],
                  "correcta": "C",
                  "pista_md": "Repartir el factor entre los sumandos.",
                  "explicacion_md": "Distributiva: $a(b + c) = a b + a c$.",
              },
          ]),

        ej(
            "Clasificar números",
            "Indica el conjunto más restrictivo al que pertenece cada uno: $-\\dfrac{3}{4}$, $\\sqrt{25}$, $\\pi - \\pi$, $\\sqrt{8}$.",
            ["Simplificar antes de clasificar."],
            (
                "$-3/4$: **racional** ($\\mathbb{Q}$). $\\sqrt{25} = 5$: **natural** ($\\mathbb{N}$). $\\pi - \\pi = 0$: **entero** ($\\mathbb{Z}$). $\\sqrt{8} = 2\\sqrt{2}$: **irracional**."
            ),
        ),

        ej(
            "Suma de racional e irracional",
            "Demuestra que $1 + \\sqrt{2}$ es irracional.",
            ["Por contradicción: supongamos que sí es racional."],
            (
                "Si $1 + \\sqrt{2} = q \\in \\mathbb{Q}$, entonces $\\sqrt{2} = q - 1$. La diferencia de dos racionales es racional, así $\\sqrt{2} \\in \\mathbb{Q}$, pero esto contradice que $\\sqrt{2}$ es irracional. **Conclusión:** $1 + \\sqrt{2}$ es irracional."
            ),
        ),

        ej(
            "Aplicar propiedades",
            "Calcula $(7 \\cdot 25) \\cdot 4$ usando asociatividad y conmutatividad para hacerlo mental.",
            ["Reordenar factores."],
            (
                "$(7 \\cdot 25) \\cdot 4 = 7 \\cdot (25 \\cdot 4) = 7 \\cdot 100 = 700$. La asociatividad permite agrupar como convenga."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $22/7$ con $\\pi$.** $22/7$ es racional; $\\pi$ es irracional. Solo coinciden en las primeras cifras.",
              "**Pensar que todo decimal es irracional.** Decimales finitos o periódicos son racionales.",
              "**Suponer que $0$ es natural.** Convención del curso (chilena/estándar): $\\mathbb{N}$ empieza en $1$.",
              "**Decir que $\\sqrt{2} \\cdot \\sqrt{2}$ es irracional.** Es $2$, racional. La regla es 'racional × irracional', no irracional × irracional.",
              "**Olvidar paréntesis al usar distributiva.** $a(b + c) \\neq a b + c$: el factor multiplica a **toda** la suma.",
          ]),

        b("resumen",
          puntos_md=[
              "**$\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{Q} \\subset \\mathbb{R}$:** naturales, enteros, racionales, reales.",
              "**Racional:** decimal finito o periódico. **Irracional:** decimal infinito no periódico.",
              "**Propiedades:** conmutativa, asociativa, distributiva, neutros, inversos.",
              "**Recta numérica:** cada real ↔ un punto. Los reales 'completan' la recta sin huecos.",
              "**Próxima lección:** subconjuntos importantes — conjuntos e intervalos.",
          ]),
    ]
    return {
        "id": "lec-prec-1-1-numeros-reales",
        "title": "Números reales",
        "description": "Conjuntos numéricos N ⊂ Z ⊂ Q ⊂ R, distinción entre racionales e irracionales por su expansión decimal, propiedades algebraicas básicas y la recta numérica.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 1,
    }


# =====================================================================
# Conjuntos e intervalos
# =====================================================================
def lesson_conjuntos_intervalos():
    blocks = [
        b("texto", body_md=(
            "Para hablar con precisión de soluciones de ecuaciones, dominios de funciones o regiones del "
            "plano, necesitamos un lenguaje claro: el de los **conjuntos** y, en particular, los "
            "**intervalos** de números reales.\n\n"
            "Un **conjunto** es simplemente una colección bien definida de objetos llamados **elementos**. "
            "Un **intervalo** es un tipo especial de conjunto: un 'pedazo conexo' de la recta real.\n\n"
            "**Al terminar:**\n\n"
            "- Manejas la notación básica de conjuntos: $\\in, \\notin, \\subset, \\cup, \\cap, \\setminus$.\n"
            "- Distingues los cinco tipos de **intervalos** (abierto, cerrado, semiabierto, infinito).\n"
            "- Calculas **uniones e intersecciones** de intervalos en la recta real.\n"
            "- Conoces la noción de **complemento** respecto a un universal."
        )),

        b("definicion",
          titulo="Conjuntos: notación básica",
          body_md=(
              "Un **conjunto** se denota con llaves: $A = \\{a, b, c\\}$ es el conjunto cuyos elementos son $a, b, c$.\n\n"
              "**Pertenencia:** $a \\in A$ significa '$a$ es elemento de $A$'. $d \\notin A$ significa que **no** lo es.\n\n"
              "**Notación por comprensión:** $\\{x : P(x)\\}$ = 'el conjunto de todos los $x$ que cumplen la propiedad $P$'.\n\n"
              "Ejemplo: $\\{x \\in \\mathbb{R} : x > 0\\}$ es el conjunto de los reales positivos.\n\n"
              "**Conjunto vacío:** $\\emptyset$ o $\\{\\,\\}$. **No tiene elementos.**\n\n"
              "**Conjunto universal $U$:** el 'mundo' en que estamos trabajando. En precálculo $U = \\mathbb{R}$ casi siempre.\n\n"
              "**Subconjunto:** $A \\subset B$ significa que todo elemento de $A$ también lo es de $B$. Ejemplo: $\\mathbb{N} \\subset \\mathbb{Z}$."
          )),

        b("definicion",
          titulo="Operaciones entre conjuntos",
          body_md=(
              "Sean $A, B$ subconjuntos de un universal $U$.\n\n"
              "**Unión** $A \\cup B = \\{x : x \\in A \\text{ o } x \\in B\\}$ — los elementos de **alguno** de los dos.\n\n"
              "**Intersección** $A \\cap B = \\{x : x \\in A \\text{ y } x \\in B\\}$ — los elementos de **ambos**.\n\n"
              "**Diferencia** $A \\setminus B = \\{x : x \\in A \\text{ y } x \\notin B\\}$ — los de $A$ que no están en $B$.\n\n"
              "**Complemento** $A^c = U \\setminus A$ — todo lo que **no** está en $A$ (relativo al universal).\n\n"
              "**Conjuntos disjuntos:** $A \\cap B = \\emptyset$ — no comparten elementos."
          )),

        formulas(
            titulo="Los cinco tipos de intervalos",
            body=(
                "Sean $a, b \\in \\mathbb{R}$ con $a < b$.\n\n"
                "| Tipo | Notación | Descripción |\n"
                "|---|---|---|\n"
                "| **Abierto** | $(a, b)$ | $\\{x : a < x < b\\}$ — sin extremos |\n"
                "| **Cerrado** | $[a, b]$ | $\\{x : a \\leq x \\leq b\\}$ — con ambos extremos |\n"
                "| **Semiabierto izq.** | $(a, b]$ | $\\{x : a < x \\leq b\\}$ — sin $a$, con $b$ |\n"
                "| **Semiabierto der.** | $[a, b)$ | $\\{x : a \\leq x < b\\}$ — con $a$, sin $b$ |\n"
                "| **Infinito** | $(a, +\\infty)$, etc. | uno de los extremos es $\\pm \\infty$ |\n\n"
                "**Convención del infinito:** $\\infty$ **nunca** es elemento — siempre se usa con paréntesis abierto. "
                "$[a, +\\infty)$ tiene corchete cerrado en $a$ y paréntesis abierto en $+\\infty$.\n\n"
                "**Representación gráfica.** Punto **lleno** ● = elemento incluido. Punto **vacío** ○ = no incluido. "
                "La parte del intervalo se traza como una **línea continua** entre los puntos."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Traducir entre notaciones",
          problema_md=(
              "Escribe en notación de intervalo y conjunto por comprensión:\n\n"
              "**(a)** $-3 < x \\leq 2$. **(b)** $x \\geq 5$. **(c)** $0 \\leq x < 4$ o $x > 7$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Sin el $-3$ (estricto), con el $2$ (no estricto): **$(-3, 2]$**. Comprensión: $\\{x \\in \\mathbb{R} : -3 < x \\leq 2\\}$."
              ),
               "justificacion_md": "$<$ → paréntesis; $\\leq$ → corchete.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $x \\geq 5$: con el $5$, sin tope superior. **$[5, +\\infty)$**."
              ),
               "justificacion_md": "$\\infty$ siempre con paréntesis.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** Dos pedazos: $[0, 4)$ y $(7, +\\infty)$. Como están unidos por 'o', se usa la **unión**: **$[0, 4) \\cup (7, +\\infty)$**."
              ),
               "justificacion_md": "'o' = unión; los intervalos son disjuntos pero la notación es la misma.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Operaciones con intervalos",
          problema_md=(
              "Sean $A = (-2, 5]$ y $B = [3, 8)$. Calcula $A \\cup B$, $A \\cap B$, $A \\setminus B$ y $B \\setminus A$."
          ),
          pasos=[
              {"accion_md": (
                  "**Visualizar.** $A = (-2, 5]$ va de $-2$ (sin) a $5$ (con). $B = [3, 8)$ va de $3$ (con) a $8$ (sin). Se solapan en $[3, 5]$."
              ),
               "justificacion_md": "Dibujar mentalmente las dos rectas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Unión** $A \\cup B$ = todo lo cubierto por al menos uno: desde $-2$ (sin) hasta $8$ (sin) sin huecos.\n\n"
                  "$A \\cup B = (-2, 8)$."
              ),
               "justificacion_md": "Los extremos siguen las convenciones de los originales: $-2$ abierto (de $A$), $8$ abierto (de $B$).",
               "es_resultado": False},
              {"accion_md": (
                  "**Intersección** $A \\cap B$ = solo donde se solapan: desde $3$ (con, por $B$) hasta $5$ (con, por $A$).\n\n"
                  "$A \\cap B = [3, 5]$."
              ),
               "justificacion_md": "El extremo más restrictivo gana en cada lado.",
               "es_resultado": False},
              {"accion_md": (
                  "**Diferencias.** $A \\setminus B$ = la parte de $A$ que no está en $B$: $(-2, 3)$. "
                  "$B \\setminus A$ = la parte de $B$ que no está en $A$: $(5, 8)$."
              ),
               "justificacion_md": "Los extremos donde 'corta' la otra región se vuelven abiertos.",
               "es_resultado": True},
          ]),

        fig(
            "Diagrama de intervalos en la recta real para A = (-2, 5] y B = [3, 8). "
            "Tres rectas paralelas horizontales con marcas en -2, 3, 5, 8. "
            "Recta superior: A en color teal #06b6d4, círculo abierto en -2 y cerrado en 5, línea entre ambos. "
            "Recta media: B en ámbar #f59e0b, círculo cerrado en 3 y abierto en 8. "
            "Recta inferior: A ∩ B = [3, 5] resaltado, ambos extremos cerrados, en color púrpura. "
            "Etiquetas claras de los conjuntos a la izquierda. " + STYLE
        ),

        b("intuicion", body_md=(
            "**Por qué importa la diferencia abierto/cerrado.**\n\n"
            "En cálculo, **incluir o no un extremo** cambia totalmente las propiedades. Por ejemplo, una "
            "función continua sobre $[a, b]$ (intervalo **cerrado y acotado**) alcanza su máximo y mínimo "
            "absolutos. Sobre $(a, b)$ esto puede fallar.\n\n"
            "**Trampa frecuente.** Una desigualdad **estricta** $x < 5$ corresponde a un extremo **abierto** "
            "$(\\ldots, 5)$. Una desigualdad **no estricta** $x \\leq 5$ corresponde a un extremo **cerrado** "
            "$(\\ldots, 5]$. Confundirlas es uno de los errores más comunes al resolver inecuaciones."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\{x \\in \\mathbb{R} : 1 \\leq x < 4\\}$ se escribe como intervalo:",
                  "opciones_md": [
                      "$(1, 4)$",
                      "$(1, 4]$",
                      "**$[1, 4)$**",
                      "$[1, 4]$",
                  ],
                  "correcta": "C",
                  "pista_md": "$\\leq$ → corchete; $<$ → paréntesis.",
                  "explicacion_md": "Con el $1$ (corchete), sin el $4$ (paréntesis).",
              },
              {
                  "enunciado_md": "$(2, 7] \\cap [5, 9) = $",
                  "opciones_md": [
                      "$(2, 9)$",
                      "**$[5, 7]$**",
                      "$[5, 7)$",
                      "$\\emptyset$",
                  ],
                  "correcta": "B",
                  "pista_md": "Intersección = donde ambos coinciden.",
                  "explicacion_md": "Empieza en $5$ (cerrado por $[5, 9)$), termina en $7$ (cerrado por $(2, 7]$).",
              },
              {
                  "enunciado_md": "El complemento (en $\\mathbb{R}$) de $[3, 8]$ es:",
                  "opciones_md": [
                      "$(3, 8)$",
                      "$[8, 3]$",
                      "**$(-\\infty, 3) \\cup (8, +\\infty)$**",
                      "$(-\\infty, 3] \\cup [8, +\\infty)$",
                  ],
                  "correcta": "C",
                  "pista_md": "Complemento = todo lo que no está. Los extremos $3$ y $8$ **sí** están en el original, así no están en el complemento.",
                  "explicacion_md": "Por eso los extremos quedan abiertos en el complemento.",
              },
          ]),

        ej(
            "Notación de intervalo",
            "Escribe como intervalo: $-1 \\leq x \\leq 3$ o $x > 6$.",
            ["Unión de dos partes."],
            (
                "$[-1, 3] \\cup (6, +\\infty)$."
            ),
        ),

        ej(
            "Operaciones",
            "Sean $A = (-\\infty, 4]$ y $B = (-1, 7)$. Calcula $A \\cap B$ y $A \\cup B$.",
            ["Identificar los rangos y combinarlos."],
            (
                "$A \\cap B = (-1, 4]$ (donde se solapan). $A \\cup B = (-\\infty, 7)$ (todo lo cubierto por al menos uno)."
            ),
        ),

        ej(
            "Diferencia",
            "Sea $A = [0, 10]$, $B = [3, 6]$. Calcula $A \\setminus B$.",
            ["La parte de $A$ que no está en $B$ son dos pedazos."],
            (
                "$A \\setminus B = [0, 3) \\cup (6, 10]$. Los extremos $3$ y $6$ están en $B$, así se quitan; los extremos del 'pedazo restante' quedan abiertos."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Usar corchete con $\\infty$.** Siempre paréntesis: $(a, +\\infty)$, $(-\\infty, b]$.",
              "**Confundir 'o' con 'y'.** 'o' es unión $\\cup$; 'y' es intersección $\\cap$.",
              "**Escribir el intervalo al revés.** $[5, 3]$ no tiene sentido; siempre $[a, b]$ con $a < b$.",
              "**Olvidar que el complemento depende del universal.** En $U = \\mathbb{R}$, el complemento de $[3, 5]$ son **dos** intervalos. En $U = [0, 10]$ es solo $[0, 3) \\cup (5, 10]$.",
              "**Mantener cerrado un extremo en la diferencia cuando ya está incluido en lo restado.** $A \\setminus B$ excluye los puntos de $B$ que están en $A$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Conjunto:** colección de elementos. Notaciones: $\\in, \\notin, \\subset, \\emptyset, U$.",
              "**Operaciones:** $\\cup$ (unión), $\\cap$ (intersección), $\\setminus$ (diferencia), $A^c$ (complemento).",
              "**Intervalos:** $(a, b)$, $[a, b]$, $(a, b]$, $[a, b)$, $(a, +\\infty)$, etc.",
              "**Convención:** $\\infty$ siempre con paréntesis. Estricto $<$ → abierto; no estricto $\\leq$ → cerrado.",
              "**Próxima lección:** repaso fundamental de cálculo numérico — potencias y raíces.",
          ]),
    ]
    return {
        "id": "lec-prec-1-2-conjuntos-intervalos",
        "title": "Conjuntos e intervalos",
        "description": "Notación de conjuntos (pertenencia, subconjunto, vacío), operaciones (unión, intersección, diferencia, complemento), tipos de intervalos en la recta real y representación gráfica.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 2,
    }


# =====================================================================
# Potencias y raíces
# =====================================================================
def lesson_potencias_raices():
    blocks = [
        b("texto", body_md=(
            "Las **potencias** son una abreviación: $a^n$ significa multiplicar $a$ por sí mismo $n$ veces. "
            "Y las **raíces** son la operación inversa: $\\sqrt[n]{a}$ es el número que elevado a la $n$ "
            "da $a$.\n\n"
            "Aunque parezca elemental, dominar potencias y raíces es **crítico**: aparecen en casi cualquier "
            "fórmula del precálculo y del cálculo, y pequeños errores de signo o de manejo del exponente "
            "se propagan a todos los pasos siguientes.\n\n"
            "**Al terminar:**\n\n"
            "- Aplicas las **leyes de los exponentes** (producto, cociente, potencia de potencia, ...).\n"
            "- Manejas exponentes **enteros**, **negativos** y **fraccionarios** (que conectan con raíces).\n"
            "- Calculas y simplificas **raíces** y reconoces cuándo $\\sqrt{a^2} = |a|$ vs. $a$.\n"
            "- Evitas los errores típicos como confundir $-3^2$ con $(-3)^2$."
        )),

        b("definicion",
          titulo="Potencia con exponente entero",
          body_md=(
              "Para $a \\in \\mathbb{R}$ y $n \\in \\mathbb{N}$ ($n \\geq 1$):\n\n"
              "$$a^n = \\underbrace{a \\cdot a \\cdot a \\cdots a}_{n \\text{ factores}}.$$\n\n"
              "**Casos especiales:**\n\n"
              "- $a^1 = a$.\n"
              "- $a^0 = 1$ (para $a \\neq 0$). $0^0$ es **indefinido**.\n"
              "- **Exponente negativo:** $a^{-n} = \\dfrac{1}{a^n}$ (para $a \\neq 0$).\n\n"
              "**Reglas de signos:**\n\n"
              "- $(-a)^{\\text{par}}$ = positivo. Ej: $(-3)^2 = 9$.\n"
              "- $(-a)^{\\text{impar}}$ = negativo. Ej: $(-3)^3 = -27$.\n\n"
              "**Trampa fundamental:** $-3^2 \\neq (-3)^2$. Sin paréntesis, **el exponente solo afecta al $3$** "
              "y luego se aplica el menos: $-3^2 = -(3^2) = -9$. Con paréntesis: $(-3)^2 = 9$."
          )),

        formulas(
            titulo="Leyes de los exponentes",
            body=(
                "Para todo $a, b \\in \\mathbb{R}$ no nulos y $m, n \\in \\mathbb{Z}$:\n\n"
                "| Regla | Fórmula | Ejemplo |\n"
                "|---|---|---|\n"
                "| Producto, base igual | $a^m \\cdot a^n = a^{m + n}$ | $3^2 \\cdot 3^4 = 3^6$ |\n"
                "| Cociente, base igual | $\\dfrac{a^m}{a^n} = a^{m - n}$ | $\\dfrac{5^6}{5^2} = 5^4$ |\n"
                "| Potencia de potencia | $(a^m)^n = a^{m n}$ | $(2^3)^2 = 2^6$ |\n"
                "| Producto, exponente igual | $a^n \\cdot b^n = (a b)^n$ | $2^3 \\cdot 5^3 = 10^3$ |\n"
                "| Cociente, exponente igual | $\\dfrac{a^n}{b^n} = \\left(\\dfrac{a}{b}\\right)^n$ | $\\dfrac{10^2}{5^2} = 2^2$ |\n"
                "| Exponente negativo | $a^{-n} = \\dfrac{1}{a^n}$ | $2^{-3} = \\dfrac{1}{8}$ |\n"
                "| Inversión por exponente neg. | $\\left(\\dfrac{a}{b}\\right)^{-n} = \\left(\\dfrac{b}{a}\\right)^n$ | $\\left(\\dfrac{2}{3}\\right)^{-2} = \\left(\\dfrac{3}{2}\\right)^2 = \\dfrac{9}{4}$ |\n\n"
                "**Mnemotecnia.** Multiplicar potencias de **misma base** = sumar exponentes; dividir = restar. "
                "Multiplicar potencias de **mismo exponente** = multiplicar bases."
            ),
        ),

        b("definicion",
          titulo="Raíces y exponente fraccionario",
          body_md=(
              "**Raíz $n$-ésima.** $\\sqrt[n]{a}$ es el número $x$ tal que $x^n = a$.\n\n"
              "- **Si $n$ es impar:** existe para todo $a \\in \\mathbb{R}$ y es único. Ej.: $\\sqrt[3]{-8} = -2$.\n"
              "- **Si $n$ es par:** existe solo si $a \\geq 0$, y es **no negativa** por convención. Ej.: $\\sqrt{16} = 4$ (no $\\pm 4$).\n\n"
              "**Importante.** $\\sqrt{a^2} = |a|$ — el valor absoluto, **no** $a$. Esto es porque la raíz cuadrada nunca es negativa.\n\n"
              "Ejemplo: $\\sqrt{(-5)^2} = \\sqrt{25} = 5$, no $-5$.\n\n"
              "**Conexión con exponentes fraccionarios:**\n\n"
              "$$a^{1/n} = \\sqrt[n]{a}, \\qquad a^{m/n} = \\sqrt[n]{a^m} = \\bigl(\\sqrt[n]{a}\\bigr)^m.$$\n\n"
              "Esto extiende las leyes de exponentes a **exponentes racionales** (y por continuidad, a "
              "exponentes reales — tema de la función exponencial)."
          )),

        b("ejemplo_resuelto",
          titulo="Simplificar usando leyes",
          problema_md="Simplifica: **(a)** $\\dfrac{x^7 \\cdot x^{-3}}{x^2}$, **(b)** $(2 a^2 b)^3$, **(c)** $\\left(\\dfrac{x^4}{y^2}\\right)^{-2}$.",
          pasos=[
              {"accion_md": (
                  "**(a)** Numerador: $x^7 \\cdot x^{-3} = x^{7 - 3} = x^4$. Dividiendo: $\\dfrac{x^4}{x^2} = x^{4 - 2} = x^2$."
              ),
               "justificacion_md": "Aplicar producto y cociente con la misma base.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $(2 a^2 b)^3 = 2^3 \\cdot (a^2)^3 \\cdot b^3 = 8 a^6 b^3$."
              ),
               "justificacion_md": "Producto con exponente igual + potencia de potencia.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** Exponente negativo invierte: $\\left(\\dfrac{x^4}{y^2}\\right)^{-2} = \\left(\\dfrac{y^2}{x^4}\\right)^2 = \\dfrac{y^4}{x^8}$."
              ),
               "justificacion_md": "$(a/b)^{-n} = (b/a)^n$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Operar con raíces y fraccionarios",
          problema_md="Calcula: **(a)** $\\sqrt{50}$ simplificado, **(b)** $\\sqrt[3]{8 x^6}$, **(c)** $16^{3/4}$.",
          pasos=[
              {"accion_md": (
                  "**(a)** $\\sqrt{50} = \\sqrt{25 \\cdot 2} = \\sqrt{25} \\cdot \\sqrt{2} = 5 \\sqrt{2}$."
              ),
               "justificacion_md": "Sacar el cuadrado perfecto.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $\\sqrt[3]{8 x^6} = \\sqrt[3]{8} \\cdot \\sqrt[3]{x^6} = 2 \\cdot x^{6/3} = 2 x^2$."
              ),
               "justificacion_md": "Raíz cúbica de $8$ es $2$; exponente entre 3 da $x^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** $16^{3/4} = (16^{1/4})^3 = 2^3 = 8$. Equivalente: $\\sqrt[4]{16^3} = \\sqrt[4]{4096} = 8$."
              ),
               "justificacion_md": "Conviene **primero** sacar la raíz, después elevar — los números se mantienen pequeños.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué $a^0 = 1$.** Si las leyes de exponentes deben mantenerse coherentes, "
            "$a^n / a^n = a^{n - n} = a^0$. Pero también $a^n / a^n = 1$. Por lo tanto, $a^0 = 1$ — es la "
            "**única definición compatible** con las demás reglas.\n\n"
            "**Por qué $a^{-n} = 1/a^n$.** Por la misma lógica: $a^0 = a^{n + (-n)} = a^n \\cdot a^{-n}$. "
            "Como $a^0 = 1$, sale $a^{-n} = 1/a^n$.\n\n"
            "**Por qué $a^{1/n} = \\sqrt[n]{a}$.** $\\bigl(a^{1/n}\\bigr)^n = a^{(1/n) \\cdot n} = a^1 = a$. "
            "El número que elevado a la $n$ da $a$ es justamente la raíz $n$-ésima.\n\n"
            "**Lección general:** las definiciones 'raras' como $a^0 = 1$, $a^{-n} = 1/a^n$, $a^{1/n} = \\sqrt[n]{a}$ "
            "**no son arbitrarias** — son las únicas que mantienen las leyes de exponentes consistentes."
        )),

        fig(
            "Diagrama jerárquico de las leyes de exponentes. "
            "Caja central grande: 'a^n = a × a × ... × a (n veces)' en color teal #06b6d4. "
            "Cuatro flechas hacia ramas: arriba 'producto a^m·a^n=a^{m+n}', derecha 'cociente a^m/a^n=a^{m-n}', "
            "abajo 'potencia (a^m)^n=a^{mn}', izquierda 'exp negativo a^{-n}=1/a^n'. "
            "Una rama adicional inferior: 'fraccionario a^{1/n}=ⁿ√a' en ámbar #f59e0b conectada con flecha curva. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$2^3 \\cdot 2^4 = $",
                  "opciones_md": ["$2^7$", "$4^7$", "$2^{12}$", "$4^{12}$"],
                  "correcta": "A",
                  "pista_md": "Misma base → sumar exponentes.",
                  "explicacion_md": "$2^{3 + 4} = 2^7 = 128$.",
              },
              {
                  "enunciado_md": "$-5^2 = $",
                  "opciones_md": ["$25$", "**$-25$**", "$10$", "$-10$"],
                  "correcta": "B",
                  "pista_md": "Sin paréntesis: el exponente solo afecta al $5$.",
                  "explicacion_md": "$-5^2 = -(5^2) = -25$. Distinto de $(-5)^2 = 25$.",
              },
              {
                  "enunciado_md": "$\\sqrt{(-3)^2} = $",
                  "opciones_md": ["$-3$", "**$3$**", "$\\pm 3$", "$9$"],
                  "correcta": "B",
                  "pista_md": "$\\sqrt{x^2} = |x|$.",
                  "explicacion_md": "$\\sqrt{9} = 3$, siempre positivo.",
              },
          ]),

        ej(
            "Simplificar exponentes",
            "Simplifica $\\dfrac{(3 a^4)^2 \\cdot a^{-3}}{9 a^2}$.",
            ["Aplicar potencia de potencia primero."],
            (
                "$(3 a^4)^2 = 9 a^8$. Numerador: $9 a^8 \\cdot a^{-3} = 9 a^5$. Dividiendo: $\\dfrac{9 a^5}{9 a^2} = a^3$."
            ),
        ),

        ej(
            "Simplificar raíz",
            "Simplifica $\\sqrt{75 x^3 y^4}$ asumiendo $x, y \\geq 0$.",
            ["Factorizar para sacar cuadrados perfectos."],
            (
                "$75 = 25 \\cdot 3$, $x^3 = x^2 \\cdot x$, $y^4 = (y^2)^2$. Así $\\sqrt{75 x^3 y^4} = \\sqrt{25 x^2 y^4} \\cdot \\sqrt{3 x} = 5 x y^2 \\sqrt{3 x}$."
            ),
        ),

        ej(
            "Exponente fraccionario",
            "Calcula $\\left(\\dfrac{27}{8}\\right)^{2/3}$.",
            ["Primero la raíz cúbica, después al cuadrado."],
            (
                "$\\left(\\dfrac{27}{8}\\right)^{1/3} = \\dfrac{3}{2}$. Elevando al cuadrado: $\\left(\\dfrac{3}{2}\\right)^2 = \\dfrac{9}{4}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**$-a^2 \\neq (-a)^2$.** El paréntesis cambia todo. Sin paréntesis, el exponente actúa antes que el menos.",
              "**Multiplicar exponentes en $a^m + a^n$.** No hay regla para suma; solo para producto y cociente con base igual.",
              "**$\\sqrt{a^2} = a$ sin valor absoluto.** Solo es $a$ si $a \\geq 0$. En general $\\sqrt{a^2} = |a|$.",
              "**$a^0 = 0$.** No: es $1$ (para $a \\neq 0$).",
              "**$\\sqrt{a + b} = \\sqrt{a} + \\sqrt{b}$.** **Falso.** La raíz no es lineal. Ejemplo: $\\sqrt{9 + 16} = 5 \\neq 3 + 4 = 7$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición:** $a^n$ = producto de $n$ factores $a$. $a^0 = 1$, $a^{-n} = 1/a^n$.",
              "**Leyes de exponentes:** suma/resta de exponentes (misma base) y producto/cociente de bases (mismo exponente).",
              "**Raíces:** $\\sqrt[n]{a}$ es el inverso de elevar a la $n$. Para $n$ par, $a \\geq 0$.",
              "**Exponente fraccionario:** $a^{m/n} = \\sqrt[n]{a^m}$.",
              "**Cuidado:** signos en $-a^n$ vs $(-a)^n$, valor absoluto en $\\sqrt{a^2}$.",
              "**Próxima lección:** uso de potencias y operaciones para construir expresiones algebraicas.",
          ]),
    ]
    return {
        "id": "lec-prec-1-3-potencias-raices",
        "title": "Potencias y raíces",
        "description": "Potencias con exponente entero, negativo y fraccionario. Leyes de exponentes. Raíces, simplificación y conexión con exponentes fraccionarios. Errores típicos de signos y paréntesis.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# Expresiones algebraicas
# =====================================================================
def lesson_expresiones_algebraicas():
    blocks = [
        b("texto", body_md=(
            "Una **expresión algebraica** es una combinación de números, variables y operaciones "
            "(suma, resta, producto, cociente, potencia). El álgebra es el lenguaje que usamos para "
            "describir relaciones generales — fórmulas físicas, tasas, áreas, modelos económicos.\n\n"
            "Esta lección te da las herramientas básicas para **construir, leer y manipular** expresiones "
            "algebraicas: identificar términos, traducir frases del lenguaje cotidiano al simbólico, "
            "reducir términos semejantes y aplicar **productos notables**.\n\n"
            "**Al terminar:**\n\n"
            "- Identificas **término**, **coeficiente**, **parte literal**, **grado** y tipo de expresión (monomio, binomio, trinomio, polinomio).\n"
            "- Traduces frases verbales a expresiones algebraicas.\n"
            "- Sumas y restas **términos semejantes** correctamente.\n"
            "- Multiplicas polinomios y aplicas los **productos notables** principales."
        )),

        b("definicion",
          titulo="Anatomía de una expresión",
          body_md=(
              "Un **término** es una expresión formada por un número (**coeficiente**) multiplicado por "
              "una o más variables elevadas a exponentes (**parte literal**).\n\n"
              "Ejemplo: en $-7 x^3 y^2$:\n\n"
              "- **Coeficiente:** $-7$.\n"
              "- **Parte literal:** $x^3 y^2$.\n"
              "- **Grado:** suma de los exponentes de las variables, $3 + 2 = 5$.\n\n"
              "Una **expresión algebraica** es una suma (algebraica) de términos:\n\n"
              "$$3 x^2 + 5 x - 7.$$\n\n"
              "**Clasificación por número de términos:**\n\n"
              "- **Monomio:** un término ($5 x^3$).\n"
              "- **Binomio:** dos términos ($x + 1$).\n"
              "- **Trinomio:** tres términos ($x^2 + 2 x + 1$).\n"
              "- **Polinomio:** uno o más términos en general.\n\n"
              "**Grado de un polinomio:** el grado del término de mayor grado. $4 x^3 - x^2 + 7$ tiene grado 3."
          )),

        b("definicion",
          titulo="Lenguaje algebraico — traducción",
          body_md=(
              "Frases comunes del lenguaje cotidiano y su traducción al álgebra (sea $x$ el número):\n\n"
              "| Frase | Expresión |\n"
              "|---|---|\n"
              "| Triple de un número | $3 x$ |\n"
              "| Un número aumentado en 4 | $x + 4$ |\n"
              "| Un número disminuido en 7 | $x - 7$ |\n"
              "| El doble de un número, menos 5 | $2 x - 5$ |\n"
              "| La mitad de un número | $\\dfrac{x}{2}$ |\n"
              "| Cuadrado de un número | $x^2$ |\n"
              "| El cuadrado de la suma de un número y 1 | $(x + 1)^2$ |\n"
              "| Suma de los cuadrados de un número y otro | $x^2 + y^2$ |\n"
              "| Edad dentro de 5 años (siendo $x$ la edad actual) | $x + 5$ |\n"
              "| Dos números consecutivos | $x$ y $x + 1$ |\n"
              "| Dos números pares consecutivos | $2 n$ y $2 n + 2$ |\n\n"
              "**Atención al orden.** 'El cuadrado de la suma' $(x + y)^2$ es **distinto** de 'la suma de los cuadrados' $x^2 + y^2$."
          )),

        b("definicion",
          titulo="Términos semejantes",
          body_md=(
              "Dos términos son **semejantes** si tienen la **misma parte literal** (mismas variables con los mismos exponentes).\n\n"
              "- $3 x^2$ y $-7 x^2$ son semejantes.\n"
              "- $5 x y^2$ y $2 x y^2$ son semejantes.\n"
              "- $3 x^2$ y $3 x^3$ **no** son semejantes.\n"
              "- $5 x y$ y $5 x^2 y$ **no** son semejantes.\n\n"
              "**Reducir términos semejantes:** sumar o restar los **coeficientes**, manteniendo la parte literal.\n\n"
              "$$3 x^2 + 5 x - 2 x^2 + 7 - 4 x = (3 - 2) x^2 + (5 - 4) x + 7 = x^2 + x + 7.$$\n\n"
              "Términos no semejantes **no se pueden combinar** — quedan tal cual."
          )),

        formulas(
            titulo="Productos notables (memorizar)",
            body=(
                "Patrones de multiplicación que aparecen una y otra vez:\n\n"
                "**Cuadrado del binomio:**\n\n"
                "$$(a + b)^2 = a^2 + 2 a b + b^2.$$\n"
                "$$(a - b)^2 = a^2 - 2 a b + b^2.$$\n\n"
                "**Suma por diferencia (diferencia de cuadrados):**\n\n"
                "$$(a + b)(a - b) = a^2 - b^2.$$\n\n"
                "**Cubo del binomio:**\n\n"
                "$$(a + b)^3 = a^3 + 3 a^2 b + 3 a b^2 + b^3.$$\n"
                "$$(a - b)^3 = a^3 - 3 a^2 b + 3 a b^2 - b^3.$$\n\n"
                "**Binomios con término común:**\n\n"
                "$$(x + a)(x + b) = x^2 + (a + b) x + a b.$$\n\n"
                "**Suma y diferencia de cubos** (las usaremos en factorización):\n\n"
                "$$a^3 + b^3 = (a + b)(a^2 - a b + b^2).$$\n"
                "$$a^3 - b^3 = (a - b)(a^2 + a b + b^2).$$\n\n"
                "**¿Por qué importan?** Porque permiten **multiplicar** o **factorizar** rápidamente, sin desarrollar todo a mano."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Productos notables",
          problema_md="Desarrolla: **(a)** $(x + 5)^2$, **(b)** $(2 a - 3)^2$, **(c)** $(x + 4)(x - 4)$, **(d)** $(x + 2)(x + 7)$.",
          pasos=[
              {"accion_md": (
                  "**(a)** $(x + 5)^2 = x^2 + 2 \\cdot x \\cdot 5 + 5^2 = x^2 + 10 x + 25$."
              ),
               "justificacion_md": "Cuadrado de binomio.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** $(2 a - 3)^2 = (2 a)^2 - 2 \\cdot (2 a) \\cdot 3 + 3^2 = 4 a^2 - 12 a + 9$."
              ),
               "justificacion_md": "Cuidado con $(2 a)^2 = 4 a^2$, no $2 a^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** $(x + 4)(x - 4) = x^2 - 4^2 = x^2 - 16$."
              ),
               "justificacion_md": "Suma por diferencia da diferencia de cuadrados.",
               "es_resultado": False},
              {"accion_md": (
                  "**(d)** $(x + 2)(x + 7) = x^2 + (2 + 7) x + 2 \\cdot 7 = x^2 + 9 x + 14$."
              ),
               "justificacion_md": "Patrón de binomios con término común.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Reducir y simplificar",
          problema_md="Reduce: $5 a^2 b - 3 a b^2 + 2 a^2 b - a b^2 + a^2 b$.",
          pasos=[
              {"accion_md": (
                  "**Identificar términos semejantes:**\n\n"
                  "- Con $a^2 b$: $5 a^2 b$, $2 a^2 b$, $a^2 b$ — coeficientes $5, 2, 1$.\n"
                  "- Con $a b^2$: $-3 a b^2$, $-a b^2$ — coeficientes $-3, -1$."
              ),
               "justificacion_md": "Agrupar por parte literal.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sumar coeficientes:**\n\n"
                  "$(5 + 2 + 1) a^2 b + (-3 - 1) a b^2 = 8 a^2 b - 4 a b^2$."
              ),
               "justificacion_md": "Distributiva al revés.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué los productos notables 'se memorizan'.** Aunque uno los puede derivar siempre con "
            "distributiva, en la práctica se usan **al revés** (factorización): ver $x^2 - 9$ y reconocerlo "
            "como $(x - 3)(x + 3)$ instantáneamente. Sin esa habilidad, factorizar — y resolver ecuaciones "
            "cuadráticas — se vuelve mucho más tedioso.\n\n"
            "**Triángulo de Pascal.** Los coeficientes de $(a + b)^n$ son los de la $n$-ésima fila del "
            "triángulo de Pascal:\n\n"
            "- $n = 0$: $1$.\n"
            "- $n = 1$: $1, 1$.\n"
            "- $n = 2$: $1, 2, 1$ (= $a^2 + 2 a b + b^2$).\n"
            "- $n = 3$: $1, 3, 3, 1$ (= $a^3 + 3 a^2 b + 3 a b^2 + b^3$).\n"
            "- $n = 4$: $1, 4, 6, 4, 1$.\n\n"
            "Esto se generaliza al **teorema del binomio** (Cap. 8)."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El grado del polinomio $4 x^3 y^2 - 5 x y^4 + 7$ es:",
                  "opciones_md": ["$3$", "**$5$**", "$7$", "$2$"],
                  "correcta": "B",
                  "pista_md": "Sumar los exponentes en cada término y tomar el máximo.",
                  "explicacion_md": "Términos: grado $5, 5, 0$ → grado del polinomio: $5$.",
              },
              {
                  "enunciado_md": "$(a - b)^2 = $",
                  "opciones_md": [
                      "$a^2 - b^2$",
                      "$a^2 + 2 a b + b^2$",
                      "**$a^2 - 2 a b + b^2$**",
                      "$a^2 - 2 a b - b^2$",
                  ],
                  "correcta": "C",
                  "pista_md": "Cuadrado de binomio con resta.",
                  "explicacion_md": "El término medio es $-2 a b$, el último es $+b^2$ (cuadrado de $-b$).",
              },
              {
                  "enunciado_md": "Reducir $4 x - 7 + 2 x + 3$:",
                  "opciones_md": [
                      "$6 x - 4$",
                      "**$6 x - 4$**",
                      "$2 x + 4$",
                      "No se puede",
                  ],
                  "correcta": "B",
                  "pista_md": "Combinar términos semejantes.",
                  "explicacion_md": "Variables: $4 x + 2 x = 6 x$. Constantes: $-7 + 3 = -4$. Total: $6 x - 4$.",
              },
          ]),

        ej(
            "Traducir al álgebra",
            "Si Pedro tiene $x$ años, escribe en términos de $x$: (a) la edad de su hermano, que tiene 4 años más; (b) la edad de Pedro hace 10 años; (c) el triple de la edad actual de Pedro disminuido en 6.",
            ["Ojo con 'hace' (resta) vs 'dentro de' (suma)."],
            (
                "(a) $x + 4$. (b) $x - 10$. (c) $3 x - 6$."
            ),
        ),

        ej(
            "Producto de polinomios",
            "Multiplica $(2 x + 3)(x^2 - x + 5)$.",
            ["Cada término del primer factor por todos los del segundo."],
            (
                "$2 x \\cdot (x^2 - x + 5) + 3 \\cdot (x^2 - x + 5) = (2 x^3 - 2 x^2 + 10 x) + (3 x^2 - 3 x + 15) = 2 x^3 + x^2 + 7 x + 15$."
            ),
        ),

        ej(
            "Cubo de un binomio",
            "Desarrolla $(2 x - 1)^3$.",
            ["$(a - b)^3 = a^3 - 3 a^2 b + 3 a b^2 - b^3$, con $a = 2 x$, $b = 1$."],
            (
                "$(2 x)^3 - 3 (2 x)^2 (1) + 3 (2 x)(1)^2 - 1^3 = 8 x^3 - 12 x^2 + 6 x - 1$."
            ),
        ),

        fig(
            "Diagrama geométrico que ilustra el cuadrado de binomio $(a+b)^2 = a^2 + 2ab + b^2$. "
            "Un cuadrado grande de lado $a+b$ subdividido en cuatro regiones rectangulares: "
            "(arriba-izq) un cuadrado de área $a^2$ en color teal #06b6d4 con su etiqueta; "
            "(abajo-der) un cuadrado de área $b^2$ en color teal claro; "
            "(arriba-der y abajo-izq) dos rectángulos idénticos de área $ab$ en color ámbar #f59e0b — "
            "el doble producto que típicamente se olvida. Etiquetas $a$, $b$ en los lados, marcador "
            "de la suma total. Fondo blanco, líneas claras. " + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**$(a + b)^2 = a^2 + b^2$.** **Falso.** Falta el doble producto: $(a + b)^2 = a^2 + 2 a b + b^2$.",
              "**Reducir términos no semejantes:** $3 x + 2 x^2 \\neq 5 x^3$ (no se pueden sumar).",
              "**Olvidar elevar el coeficiente al desarrollar $(2 a)^2$.** Es $4 a^2$, no $2 a^2$.",
              "**Confundir $-x^2$ con $(-x)^2$.** Igual que en potencias y raíces: el paréntesis decide.",
              "**Olvidar el signo en $(a - b)^3$.** Los términos alternados son $a^3 - 3 a^2 b + 3 a b^2 - b^3$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Término:** coeficiente × parte literal. **Grado:** suma de exponentes.",
              "**Polinomios:** monomio (1), binomio (2), trinomio (3), polinomio (varios).",
              "**Términos semejantes:** misma parte literal, se combinan sumando coeficientes.",
              "**Productos notables clave:** $(a + b)^2$, $(a - b)^2$, $(a + b)(a - b)$, $(a + b)^3$, $(a - b)^3$.",
              "**Próxima lección:** la operación inversa — factorización.",
          ]),
    ]
    return {
        "id": "lec-prec-1-4-expresiones-algebraicas",
        "title": "Expresiones algebraicas",
        "description": "Términos, coeficientes, grado, clasificación de polinomios. Lenguaje algebraico para traducir frases. Reducción de términos semejantes. Multiplicación de polinomios y productos notables.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# Factorización
# =====================================================================
def lesson_factorizacion():
    blocks = [
        b("texto", body_md=(
            "**Factorizar** una expresión algebraica es **escribirla como producto** de factores más simples. "
            "Es la operación inversa a 'expandir' o 'desarrollar'.\n\n"
            "Ejemplo: expandir $(x + 2)(x + 3) = x^2 + 5 x + 6$. Factorizar es ir al revés: ver "
            "$x^2 + 5 x + 6$ y reconocer que es $(x + 2)(x + 3)$.\n\n"
            "**¿Por qué importa tanto?** Porque casi todo lo demás del precálculo se basa en esto:\n\n"
            "- **Resolver ecuaciones cuadráticas o polinomiales:** se factorizan y se aplica la propiedad del producto cero.\n"
            "- **Simplificar expresiones racionales:** se factoriza numerador y denominador para cancelar.\n"
            "- **Resolver inecuaciones:** se factoriza y se analiza el signo de cada factor.\n\n"
            "Esta lección presenta los **seis métodos** principales de factorización.\n\n"
            "**Al terminar:**\n\n"
            "- Reconoces y aplicas: factor común, agrupación, trinomio cuadrático, diferencia de cuadrados, trinomio cuadrado perfecto, suma/diferencia de cubos."
        )),

        formulas(
            titulo="Método 1 — Factor común",
            body=(
                "**Idea.** Si todos los términos comparten un factor (numérico, literal o ambos), se 'saca' usando distributiva al revés:\n\n"
                "$$a b + a c = a(b + c).$$\n\n"
                "**Ejemplos:**\n\n"
                "- $6 x^2 + 9 x = 3 x (2 x + 3)$ — factor común $3 x$.\n"
                "- $4 a^3 b - 2 a^2 b + 6 a b = 2 a b (2 a^2 - a + 3)$ — factor común $2 a b$.\n"
                "- $-x - y - z = -(x + y + z)$ — sacar el menos cuando todo es negativo.\n\n"
                "**Truco.** Cuando hay más de un término, identificar el **mayor común divisor** de los coeficientes "
                "y la **menor potencia común** de cada variable que aparezca en todos."
            ),
        ),

        formulas(
            titulo="Método 2 — Agrupación (4+ términos)",
            body=(
                "**Idea.** Cuando hay cuatro o más términos sin factor común global, **agruparlos** en pares (o tríos) que sí compartan factor.\n\n"
                "**Ejemplo:** $x^3 + 2 x^2 + 3 x + 6$.\n\n"
                "Agrupar: $(x^3 + 2 x^2) + (3 x + 6) = x^2 (x + 2) + 3 (x + 2)$.\n\n"
                "Ahora $(x + 2)$ es factor común de los dos grupos:\n\n"
                "$x^2 (x + 2) + 3 (x + 2) = (x + 2)(x^2 + 3)$.\n\n"
                "**La clave:** después de la primera factorización por grupo, ambos paréntesis deben coincidir."
            ),
        ),

        formulas(
            titulo="Método 3 — Trinomio $x^2 + b x + c$",
            body=(
                "**Idea.** Buscar dos números $p, q$ tales que $p + q = b$ y $p \\cdot q = c$. Entonces\n\n"
                "$$x^2 + b x + c = (x + p)(x + q).$$\n\n"
                "**Ejemplos:**\n\n"
                "- $x^2 + 5 x + 6$: buscar $p, q$ con suma $5$ y producto $6$. Salen $2$ y $3$. Factorización: $(x + 2)(x + 3)$.\n"
                "- $x^2 - x - 12$: suma $-1$, producto $-12$. Salen $-4$ y $3$. Factorización: $(x - 4)(x + 3)$.\n"
                "- $x^2 + 7 x + 12$: $3$ y $4$. $(x + 3)(x + 4)$.\n\n"
                "**Si no existen tales $p, q$ enteros**, el trinomio **no factoriza** sobre los enteros. Hay que recurrir a la fórmula cuadrática."
            ),
        ),

        formulas(
            titulo="Método 4 — Trinomio $a x^2 + b x + c$ (con $a \\neq 1$)",
            body=(
                "**Método del 'splitting' (descomposición del término medio).**\n\n"
                "1. Calcular $a \\cdot c$.\n"
                "2. Buscar dos números $p, q$ con suma $b$ y producto $a c$.\n"
                "3. Reescribir el término del medio: $b x = p x + q x$.\n"
                "4. Factorizar por agrupación.\n\n"
                "**Ejemplo:** $2 x^2 + 7 x + 3$.\n\n"
                "$a c = 2 \\cdot 3 = 6$. Suma $7$, producto $6$ → $p = 6$, $q = 1$.\n\n"
                "$2 x^2 + 7 x + 3 = 2 x^2 + 6 x + x + 3 = 2 x (x + 3) + (x + 3) = (x + 3)(2 x + 1)$.\n\n"
                "**Alternativa.** Aplicar la fórmula cuadrática para hallar las raíces $r_1, r_2$, y entonces $a x^2 + b x + c = a (x - r_1)(x - r_2)$."
            ),
        ),

        formulas(
            titulo="Método 5 — Productos notables al revés",
            body=(
                "**Diferencia de cuadrados:**\n\n"
                "$$a^2 - b^2 = (a + b)(a - b).$$\n\n"
                "Ej: $9 x^2 - 25 = (3 x)^2 - 5^2 = (3 x + 5)(3 x - 5)$.\n\n"
                "**Trinomio cuadrado perfecto:**\n\n"
                "$$a^2 + 2 a b + b^2 = (a + b)^2, \\qquad a^2 - 2 a b + b^2 = (a - b)^2.$$\n\n"
                "Ej: $4 y^2 - 12 y + 9 = (2 y)^2 - 2 \\cdot (2 y) \\cdot 3 + 3^2 = (2 y - 3)^2$.\n\n"
                "**Truco para reconocer el cuadrado perfecto:** los términos extremos son cuadrados ($a^2, b^2$) y el del medio es **el doble del producto** $\\pm 2 a b$.\n\n"
                "**Suma y diferencia de cubos:**\n\n"
                "$$a^3 + b^3 = (a + b)(a^2 - a b + b^2).$$\n"
                "$$a^3 - b^3 = (a - b)(a^2 + a b + b^2).$$\n\n"
                "Ej: $x^3 - 27 = x^3 - 3^3 = (x - 3)(x^2 + 3 x + 9)$.\n\n"
                "**Importante:** $a^2 + b^2$ **no factoriza** sobre los reales (no es diferencia, es suma de cuadrados)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Combinar varios métodos",
          problema_md="Factoriza completamente $3 x^4 - 12 x^2$.",
          pasos=[
              {"accion_md": (
                  "**Factor común primero.** $3 x^2$ es común a ambos términos:\n\n"
                  "$3 x^4 - 12 x^2 = 3 x^2 (x^2 - 4)$."
              ),
               "justificacion_md": "**Regla de oro:** siempre intentar primero factor común antes que cualquier otra cosa.",
               "es_resultado": False},
              {"accion_md": (
                  "**Diferencia de cuadrados** dentro del paréntesis:\n\n"
                  "$x^2 - 4 = (x + 2)(x - 2)$.\n\n"
                  "**Resultado completo:** $3 x^4 - 12 x^2 = 3 x^2 (x + 2)(x - 2)$."
              ),
               "justificacion_md": "Factorizar **completamente** = no se puede factorizar más sin salir de los enteros.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Trinomio con $a > 1$",
          problema_md="Factoriza $6 x^2 + 7 x - 5$.",
          pasos=[
              {"accion_md": (
                  "**Splitting.** $a c = 6 \\cdot (-5) = -30$. Buscar $p, q$ con suma $7$ y producto $-30$.\n\n"
                  "Pares de factores de $-30$: $(1, -30), (-1, 30), (2, -15), (-2, 15), (3, -10), (-3, 10), (5, -6), (-5, 6)$.\n\n"
                  "Suma $7$: $-3 + 10 = 7$. ✓"
              ),
               "justificacion_md": "Listar pares y revisar cuál suma da $b$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Reescribir y agrupar:**\n\n"
                  "$6 x^2 + 7 x - 5 = 6 x^2 - 3 x + 10 x - 5 = 3 x (2 x - 1) + 5 (2 x - 1) = (2 x - 1)(3 x + 5)$."
              ),
               "justificacion_md": "Verificar expandiendo: $(2 x - 1)(3 x + 5) = 6 x^2 + 10 x - 3 x - 5 = 6 x^2 + 7 x - 5$. ✓",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Estrategia general para factorizar.** Siempre seguir este orden:\n\n"
            "1. **¿Hay factor común?** Sacarlo primero.\n"
            "2. **¿Cuántos términos quedan?**\n"
            "  - Dos términos: ¿diferencia de cuadrados? ¿suma o diferencia de cubos?\n"
            "  - Tres términos: ¿trinomio cuadrado perfecto? ¿trinomio $x^2 + b x + c$? ¿trinomio $a x^2 + b x + c$?\n"
            "  - Cuatro o más: agrupación.\n"
            "3. **¿Cada factor se puede factorizar más?** Repetir el proceso recursivamente.\n\n"
            "**Cuando ningún método funciona** sobre los enteros, queda la opción de la fórmula cuadrática "
            "(o numérica) para encontrar las raíces y escribir el polinomio en forma factorizada con "
            "coeficientes irracionales o complejos. Eso lo veremos en la lección de ecuaciones."
        )),

        fig(
            "Diagrama de flujo para decidir qué método de factorización usar. "
            "Caja inicial 'Polinomio a factorizar' en gris. "
            "Primer rombo: '¿Factor común?' → SÍ baja a 'Sacar factor común y volver al inicio'; NO sigue. "
            "Segundo rombo: '¿Cuántos términos?' con tres ramas: "
            "Rama '2 términos' → '¿Diferencia de cuadrados o de cubos?' (caja teal). "
            "Rama '3 términos' → '¿Cuadrado perfecto / trinomio simple / trinomio con a≠1?' (caja ámbar). "
            "Rama '4+ términos' → 'Intentar agrupación' (caja púrpura). "
            "Caja final: '¿Cada factor se puede factorizar más? Si sí, repetir.' " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$x^2 - 9 = $",
                  "opciones_md": [
                      "$(x - 3)^2$",
                      "**$(x + 3)(x - 3)$**",
                      "$(x - 9)(x + 1)$",
                      "No factoriza",
                  ],
                  "correcta": "B",
                  "pista_md": "Diferencia de cuadrados.",
                  "explicacion_md": "$a^2 - b^2 = (a + b)(a - b)$ con $a = x, b = 3$.",
              },
              {
                  "enunciado_md": "$x^2 + 8 x + 16 = $",
                  "opciones_md": [
                      "$(x + 4)(x + 4) = (x + 4)^2$",
                      "$(x + 8)(x + 2)$",
                      "$(x + 16)(x + 1)$",
                      "No factoriza",
                  ],
                  "correcta": "A",
                  "pista_md": "$16 = 4^2$ y $8 = 2 \\cdot 4$.",
                  "explicacion_md": "Trinomio cuadrado perfecto: $(x + 4)^2$.",
              },
              {
                  "enunciado_md": "$x^3 - 8 = $",
                  "opciones_md": [
                      "$(x - 2)^3$",
                      "**$(x - 2)(x^2 + 2 x + 4)$**",
                      "$(x - 2)(x^2 - 2 x + 4)$",
                      "$(x + 2)(x^2 - 2 x + 4)$",
                  ],
                  "correcta": "B",
                  "pista_md": "Diferencia de cubos: $a^3 - b^3 = (a - b)(a^2 + a b + b^2)$.",
                  "explicacion_md": "Con $a = x, b = 2$: $(x - 2)(x^2 + 2 x + 4)$.",
              },
          ]),

        ej(
            "Factor común y diferencia de cuadrados",
            "Factoriza completamente $5 x^3 - 45 x$.",
            ["Factor común primero, diferencia de cuadrados después."],
            (
                "$5 x^3 - 45 x = 5 x (x^2 - 9) = 5 x (x + 3)(x - 3)$."
            ),
        ),

        ej(
            "Trinomio simple",
            "Factoriza $x^2 - 7 x + 12$.",
            ["Buscar dos números con suma $-7$ y producto $12$."],
            (
                "$-3 \\cdot -4 = 12$, $-3 + (-4) = -7$. Por lo tanto $x^2 - 7 x + 12 = (x - 3)(x - 4)$."
            ),
        ),

        ej(
            "Agrupación",
            "Factoriza $a^3 - a^2 + a - 1$.",
            ["Agrupar 'de a dos'."],
            (
                "$(a^3 - a^2) + (a - 1) = a^2 (a - 1) + 1 (a - 1) = (a - 1)(a^2 + 1)$. "
                "$(a^2 + 1)$ no factoriza sobre los reales."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar sacar el factor común al principio.** Es siempre el primer paso. Sin eso, los métodos siguientes pueden complicarse.",
              "**Factorizar $a^2 + b^2$ como $(a + b)^2$ o $(a - b)(a + b)$.** **Falso.** $a^2 + b^2$ **no factoriza** sobre los reales.",
              "**Confundir diferencia de cuadrados con diferencia de cubos.** $a^2 - b^2 = (a + b)(a - b)$ pero $a^3 - b^3$ tiene un trinomio adentro.",
              "**Olvidar verificar la factorización expandiendo.** Es el chequeo que evita errores de signo.",
              "**Detenerse antes de factorizar completamente.** Si algún factor se puede factorizar más, hay que seguir.",
          ]),

        b("resumen",
          puntos_md=[
              "**Factor común:** $a b + a c = a(b + c)$. Siempre primero.",
              "**Agrupación:** para 4+ términos, agrupar en pares con factor común.",
              "**Trinomios:** $x^2 + b x + c$ por inspección; $a x^2 + b x + c$ por splitting.",
              "**Productos notables al revés:** diferencia de cuadrados, cuadrado perfecto, suma/diferencia de cubos.",
              "**Estrategia:** factor común → contar términos → método según cantidad → repetir hasta no poder más.",
              "**Próxima lección:** aplicar factorización para simplificar fracciones algebraicas.",
          ]),
    ]
    return {
        "id": "lec-prec-1-5-factorizacion",
        "title": "Factorización",
        "description": "Métodos de factorización: factor común, agrupación, trinomio cuadrático (con a=1 y a≠1), diferencia de cuadrados, trinomio cuadrado perfecto, suma y diferencia de cubos. Estrategia general.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 5,
    }


# =====================================================================
# Expresiones racionales
# =====================================================================
def lesson_expresiones_racionales():
    blocks = [
        b("texto", body_md=(
            "Una **expresión racional** es un cociente de polinomios:\n\n"
            "$$\\dfrac{P(x)}{Q(x)}, \\qquad Q(x) \\neq 0.$$\n\n"
            "Son la versión algebraica de las fracciones numéricas, y se manipulan con las **mismas reglas** "
            "(simplificar factores comunes, sumar con denominador común, multiplicar 'cruzado', dividir invirtiendo).\n\n"
            "**Restricción fundamental:** el denominador **nunca puede ser cero**. Por eso siempre hay que "
            "identificar las **restricciones** sobre la variable.\n\n"
            "**Al terminar:**\n\n"
            "- Identificas restricciones (ceros del denominador).\n"
            "- **Simplificas** factorizando y cancelando.\n"
            "- Sumas, restas, multiplicas y divides expresiones racionales.\n"
            "- **Racionalizas** denominadores que contienen raíces."
        )),

        b("definicion",
          titulo="Restricciones",
          body_md=(
              "El **dominio** de una expresión racional es el conjunto de valores de $x$ para los que está "
              "definida — es decir, todos los reales **excepto** los que anulan el denominador.\n\n"
              "Para encontrar las restricciones:\n\n"
              "1. Igualar el denominador a cero.\n"
              "2. Resolver para $x$.\n"
              "3. Excluir esos valores.\n\n"
              "**Ejemplo.** $\\dfrac{x + 1}{x^2 - 4}$. Denominador $= 0$: $x^2 = 4 \\Rightarrow x = \\pm 2$. "
              "**Dominio:** $x \\neq \\pm 2$, o $\\mathbb{R} \\setminus \\{-2, 2\\}$.\n\n"
              "**Atención.** Al simplificar una expresión racional, las restricciones del **original** "
              "se mantienen — aunque después de cancelar 'desaparezcan'. Por ejemplo, $\\dfrac{x^2 - 4}{x - 2} = x + 2$ "
              "pero **solo si $x \\neq 2$**. En $x = 2$ el original no está definido."
          )),

        b("definicion",
          titulo="Simplificación",
          body_md=(
              "**Procedimiento:**\n\n"
              "1. Factorizar numerador y denominador completamente.\n"
              "2. Cancelar factores comunes.\n"
              "3. Indicar las restricciones del original.\n\n"
              "**Ejemplo.** $\\dfrac{x^2 - 9}{x^2 - 4 x + 3}$.\n\n"
              "Numerador: $x^2 - 9 = (x + 3)(x - 3)$.\n\n"
              "Denominador: $x^2 - 4 x + 3 = (x - 1)(x - 3)$.\n\n"
              "$\\dfrac{(x + 3)(x - 3)}{(x - 1)(x - 3)} = \\dfrac{x + 3}{x - 1}$, con $x \\neq 1, 3$.\n\n"
              "**Importante.** **Solo se cancelan factores**, no términos. $\\dfrac{x + 2}{x + 5}$ **no** es $\\dfrac{2}{5}$."
          )),

        formulas(
            titulo="Operaciones",
            body=(
                "**Multiplicación:**\n\n"
                "$$\\dfrac{a}{b} \\cdot \\dfrac{c}{d} = \\dfrac{a c}{b d}.$$\n\n"
                "**División:** invertir el segundo y multiplicar:\n\n"
                "$$\\dfrac{a}{b} \\div \\dfrac{c}{d} = \\dfrac{a}{b} \\cdot \\dfrac{d}{c} = \\dfrac{a d}{b c}.$$\n\n"
                "**Suma y resta** con denominadores **iguales:** sumar/restar numeradores.\n\n"
                "$$\\dfrac{a}{c} + \\dfrac{b}{c} = \\dfrac{a + b}{c}.$$\n\n"
                "**Suma y resta** con denominadores **distintos:** llevar a denominador común (el **mínimo común múltiplo**) y luego sumar.\n\n"
                "$$\\dfrac{a}{b} + \\dfrac{c}{d} = \\dfrac{a d + b c}{b d}.$$\n\n"
                "**Estrategia general:** factorizar primero, después operar — minimiza el cálculo."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Multiplicación",
          problema_md="Calcula $\\dfrac{x^2 - 4}{x + 1} \\cdot \\dfrac{x^2 + 2 x + 1}{x - 2}$.",
          pasos=[
              {"accion_md": (
                  "**Factorizar todo:** $x^2 - 4 = (x + 2)(x - 2)$, $x^2 + 2 x + 1 = (x + 1)^2$."
              ),
               "justificacion_md": "Buscar factores comunes para cancelar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Multiplicar y cancelar:**\n\n"
                  "$\\dfrac{(x + 2)(x - 2)}{x + 1} \\cdot \\dfrac{(x + 1)^2}{x - 2} = \\dfrac{(x + 2)(x - 2)(x + 1)^2}{(x + 1)(x - 2)} = (x + 2)(x + 1)$."
              ),
               "justificacion_md": "Cancelar $(x - 2)$ y un $(x + 1)$.",
               "es_resultado": False},
              {"accion_md": "**Restricciones:** $x \\neq -1, 2$ (ceros de los denominadores originales).",
               "justificacion_md": "No olvidar las restricciones aunque desaparezcan al simplificar.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Suma con denominadores distintos",
          problema_md="Calcula $\\dfrac{2}{x} + \\dfrac{3}{x - 1}$.",
          pasos=[
              {"accion_md": (
                  "**Denominador común:** $x \\cdot (x - 1)$ (mínimo común múltiplo).\n\n"
                  "Convertir cada fracción: $\\dfrac{2}{x} = \\dfrac{2(x - 1)}{x(x - 1)}$, $\\dfrac{3}{x - 1} = \\dfrac{3 x}{x(x - 1)}$."
              ),
               "justificacion_md": "Multiplicar arriba y abajo por lo que falta.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sumar:** $\\dfrac{2(x - 1) + 3 x}{x(x - 1)} = \\dfrac{2 x - 2 + 3 x}{x(x - 1)} = \\dfrac{5 x - 2}{x(x - 1)}$.\n\n"
                  "**Restricciones:** $x \\neq 0, 1$."
              ),
               "justificacion_md": "Combinar términos en el numerador.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Racionalización",
          body_md=(
              "**Racionalizar** un denominador es reescribir la expresión para que **no haya raíces en el denominador**. La técnica:\n\n"
              "**Caso 1 — denominador con una raíz cuadrada simple $\\sqrt{a}$:** multiplicar arriba y abajo por $\\sqrt{a}$.\n\n"
              "$$\\dfrac{1}{\\sqrt{2}} = \\dfrac{1}{\\sqrt{2}} \\cdot \\dfrac{\\sqrt{2}}{\\sqrt{2}} = \\dfrac{\\sqrt{2}}{2}.$$\n\n"
              "**Caso 2 — denominador con raíz $n$-ésima $\\sqrt[n]{a^k}$:** multiplicar por la potencia que **completa** el índice.\n\n"
              "$$\\dfrac{1}{\\sqrt[3]{x}} = \\dfrac{\\sqrt[3]{x^2}}{\\sqrt[3]{x} \\cdot \\sqrt[3]{x^2}} = \\dfrac{\\sqrt[3]{x^2}}{x}.$$\n\n"
              "**Caso 3 — denominador binomial con raíces $\\sqrt{a} \\pm \\sqrt{b}$:** multiplicar arriba y abajo por el **conjugado** $\\sqrt{a} \\mp \\sqrt{b}$, que produce diferencia de cuadrados.\n\n"
              "$$\\dfrac{1}{\\sqrt{5} - \\sqrt{2}} = \\dfrac{\\sqrt{5} + \\sqrt{2}}{(\\sqrt{5})^2 - (\\sqrt{2})^2} = \\dfrac{\\sqrt{5} + \\sqrt{2}}{3}.$$\n\n"
              "**¿Por qué?** Las expresiones con raíces en el denominador son menos cómodas de evaluar y comparar. La forma racionalizada es la **forma estándar**."
          )),

        b("intuicion", body_md=(
            "**Por qué siempre identificar restricciones.** En el cálculo, una función definida por una "
            "fórmula racional **no incluye** los puntos donde el denominador se anula. Esos puntos son "
            "**discontinuidades** — agujeros o asíntotas. Olvidar las restricciones lleva a:\n\n"
            "- 'Soluciones' de ecuaciones que en realidad no resuelven nada (porque el denominador se anula).\n"
            "- Gráficas mal dibujadas que ignoran agujeros.\n"
            "- Errores en límites y derivadas.\n\n"
            "**Por qué cancelar solo factores.** La cancelación es una división arriba y abajo por el mismo "
            "número. Solo funciona con **factores** (que se multiplican), no con **términos** (que se suman). "
            "$(x + 2) / (x + 5) \\neq 2/5$ porque el $x$ se está sumando, no multiplicando."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El dominio de $\\dfrac{x + 1}{x^2 - 9}$ es:",
                  "opciones_md": [
                      "$\\mathbb{R}$",
                      "$\\mathbb{R} \\setminus \\{0\\}$",
                      "**$\\mathbb{R} \\setminus \\{-3, 3\\}$**",
                      "$\\mathbb{R} \\setminus \\{-1\\}$",
                  ],
                  "correcta": "C",
                  "pista_md": "Anular el denominador.",
                  "explicacion_md": "$x^2 - 9 = 0 \\Rightarrow x = \\pm 3$. Esos valores se excluyen.",
              },
              {
                  "enunciado_md": "$\\dfrac{x^2 - 1}{x - 1} = $ (asumiendo $x \\neq 1$)",
                  "opciones_md": [
                      "$x - 1$",
                      "**$x + 1$**",
                      "$1$",
                      "$x$",
                  ],
                  "correcta": "B",
                  "pista_md": "$x^2 - 1 = (x - 1)(x + 1)$.",
                  "explicacion_md": "Cancelar el factor $(x - 1)$ deja $(x + 1)$.",
              },
              {
                  "enunciado_md": "$\\dfrac{1}{\\sqrt{3}}$ racionalizado es:",
                  "opciones_md": [
                      "$\\dfrac{1}{3}$",
                      "**$\\dfrac{\\sqrt{3}}{3}$**",
                      "$3$",
                      "$\\sqrt{3}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Multiplicar por $\\sqrt{3}/\\sqrt{3}$.",
                  "explicacion_md": "$\\dfrac{1}{\\sqrt{3}} \\cdot \\dfrac{\\sqrt{3}}{\\sqrt{3}} = \\dfrac{\\sqrt{3}}{3}$.",
              },
          ]),

        ej(
            "Simplificar",
            "Simplifica $\\dfrac{x^2 - 5 x + 6}{x^2 - 4}$ e indica las restricciones.",
            ["Factorizar arriba y abajo."],
            (
                "Numerador: $(x - 2)(x - 3)$. Denominador: $(x + 2)(x - 2)$. "
                "Cancelando: $\\dfrac{x - 3}{x + 2}$, con $x \\neq \\pm 2$."
            ),
        ),

        ej(
            "Resta de fracciones",
            "Calcula $\\dfrac{1}{x - 2} - \\dfrac{1}{x + 2}$.",
            ["Denominador común $(x - 2)(x + 2) = x^2 - 4$."],
            (
                "$\\dfrac{(x + 2) - (x - 2)}{x^2 - 4} = \\dfrac{4}{x^2 - 4}$. Restricciones: $x \\neq \\pm 2$."
            ),
        ),

        ej(
            "Racionalizar denominador binomial",
            "Racionaliza $\\dfrac{2}{1 + \\sqrt{3}}$.",
            ["Multiplicar por el conjugado $1 - \\sqrt{3}$."],
            (
                "$\\dfrac{2}{1 + \\sqrt{3}} \\cdot \\dfrac{1 - \\sqrt{3}}{1 - \\sqrt{3}} = \\dfrac{2(1 - \\sqrt{3})}{1 - 3} = \\dfrac{2(1 - \\sqrt{3})}{-2} = \\sqrt{3} - 1$."
            ),
        ),

        fig(
            "Pizarra dividida en dos columnas con encabezados grandes 'CORRECTO ✓' (color teal #06b6d4) "
            "y 'INCORRECTO ✗' (color ámbar #f59e0b). En la columna correcta: la simplificación "
            "$\\frac{(x-2)(x+3)}{(x-2)(x+1)} = \\frac{x+3}{x+1}$ con los factores $(x-2)$ tachados con una línea diagonal "
            "verde y la nota 'cancelo factor común', además del recordatorio 'restricción: $x \\neq 2$' destacado. "
            "En la columna incorrecta: el ejemplo prohibido $\\frac{x+2}{x+5} = \\frac{2}{5}$ con una gran X roja, "
            "y la nota 'NO se cancelan términos sumados, solo factores multiplicados'. Estilo pizarra educativa. "
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Cancelar términos en lugar de factores.** $\\dfrac{x + 2}{x + 5} \\neq \\dfrac{2}{5}$.",
              "**Olvidar identificar restricciones.** Aunque al simplificar 'desaparezcan', se mantienen del original.",
              "**Sumar fracciones cruzando.** $\\dfrac{a}{b} + \\dfrac{c}{d} \\neq \\dfrac{a + c}{b + d}$. Hay que llevar a denominador común.",
              "**Dividir multiplicando.** Al dividir fracciones se invierte y multiplica, no se multiplica directo.",
              "**No racionalizar cuando se pide.** En la mayoría de los cursos chilenos, la forma estándar tiene denominador racional.",
          ]),

        b("resumen",
          puntos_md=[
              "**Expresión racional:** cociente de polinomios. **Restricciones:** ceros del denominador.",
              "**Simplificar:** factorizar arriba y abajo, cancelar **factores** comunes, anotar restricciones.",
              "**Operaciones:** multiplicar directo; dividir invirtiendo y multiplicando; sumar/restar con denominador común.",
              "**Racionalizar:** eliminar raíces del denominador multiplicando por la expresión adecuada (conjugado para binomios).",
              "**Próxima lección:** aplicación a la resolución de **ecuaciones**.",
          ]),
    ]
    return {
        "id": "lec-prec-1-6-expresiones-racionales",
        "title": "Expresiones racionales",
        "description": "Cocientes de polinomios: dominio y restricciones, simplificación por factorización, suma/resta/multiplicación/división y racionalización de denominadores.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 6,
    }


# =====================================================================
# Ecuaciones
# =====================================================================
def lesson_ecuaciones():
    blocks = [
        b("texto", body_md=(
            "Una **ecuación** es una **igualdad** entre dos expresiones que contiene una o más **incógnitas**. "
            "**Resolver** una ecuación es encontrar todos los valores de las incógnitas que la satisfacen — "
            "es decir, la convierten en una identidad verdadera.\n\n"
            "$$2 x + 3 = 11 \\;\\Longleftrightarrow\\; x = 4 \\quad (\\text{porque } 2 \\cdot 4 + 3 = 11).$$\n\n"
            "Esta lección recorre los tres tipos básicos: **lineales**, **cuadráticas** y algunas **especiales** "
            "(con raíces, valor absoluto, fracciones).\n\n"
            "**Al terminar:**\n\n"
            "- Resuelves ecuaciones lineales con paso a paso claro.\n"
            "- Aplicas las **tres técnicas** para cuadráticas: factorización, fórmula general, completación de cuadrados.\n"
            "- Interpretas el **discriminante** $\\Delta = b^2 - 4 a c$.\n"
            "- Manejas ecuaciones con fracciones, raíces y valor absoluto, **verificando** las soluciones."
        )),

        b("definicion",
          titulo="Propiedades de la igualdad",
          body_md=(
              "Para 'mover' términos entre lados de una ecuación se usan estas propiedades. Si $a = b$, entonces:\n\n"
              "- **Suma/resta:** $a + c = b + c$, $a - c = b - c$.\n"
              "- **Multiplicación/división:** $a \\cdot c = b \\cdot c$ y, si $c \\neq 0$, $a / c = b / c$.\n"
              "- **Potencia:** $a^n = b^n$ (cuidado: puede introducir soluciones espurias si $n$ es par).\n"
              "- **Raíz:** $\\sqrt[n]{a} = \\sqrt[n]{b}$ (con las restricciones usuales).\n\n"
              "**Idea operativa.** Hacer la **misma cosa de los dos lados** preserva la igualdad. La estrategia "
              "es 'aislar' la incógnita haciendo y deshaciendo operaciones.\n\n"
              "**Cuidado al multiplicar por una expresión variable:** si esta puede ser cero, podemos perder o ganar soluciones."
          )),

        formulas(
            titulo="Ecuaciones lineales: $a x + b = 0$",
            body=(
                "Una ecuación lineal en $x$ tiene la forma $a x + b = 0$ con $a \\neq 0$. Su **única** solución es\n\n"
                "$$x = -\\dfrac{b}{a}.$$\n\n"
                "**Procedimiento general** (cualquier lineal, aunque no esté en forma estándar):\n\n"
                "1. Eliminar paréntesis y fracciones (multiplicar por el común múltiplo de los denominadores).\n"
                "2. Llevar todos los términos con $x$ a un lado, los demás al otro.\n"
                "3. Reducir términos semejantes.\n"
                "4. Dividir por el coeficiente de $x$.\n\n"
                "**Ejemplo.** $3 x - 7 = 5 \\Rightarrow 3 x = 12 \\Rightarrow x = 4$.\n\n"
                "**Casos degenerados.** Si llegás a $0 = 0$, la 'ecuación' es una **identidad** (todo $x$ es solución). "
                "Si llegás a $0 = c$ con $c \\neq 0$, **no hay solución**."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Lineal con fracciones",
          problema_md="Resuelve $\\dfrac{x}{2} - \\dfrac{x - 1}{3} = 1$.",
          pasos=[
              {"accion_md": (
                  "**Multiplicar por el común múltiplo $6$ para eliminar fracciones:**\n\n"
                  "$6 \\cdot \\dfrac{x}{2} - 6 \\cdot \\dfrac{x - 1}{3} = 6 \\cdot 1$\n\n"
                  "$3 x - 2(x - 1) = 6$."
              ),
               "justificacion_md": "MCM de 2 y 3 es 6.",
               "es_resultado": False},
              {"accion_md": (
                  "**Distribuir y reducir:** $3 x - 2 x + 2 = 6 \\Rightarrow x + 2 = 6 \\Rightarrow x = 4$."
              ),
               "justificacion_md": "Verificar: $4/2 - (4 - 1)/3 = 2 - 1 = 1$ ✓.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Ecuaciones cuadráticas: $a x^2 + b x + c = 0$",
            body=(
                "Tres métodos. **Probar siempre primero el más rápido aplicable.**\n\n"
                "**Método 1 — Factorización.** Si la cuadrática factoriza fácilmente, usar la **propiedad del producto cero**: "
                "si $A \\cdot B = 0$, entonces $A = 0$ o $B = 0$.\n\n"
                "Ejemplo: $x^2 + x - 12 = 0 \\Rightarrow (x + 4)(x - 3) = 0 \\Rightarrow x = -4$ o $x = 3$.\n\n"
                "**Método 2 — Fórmula general.** Siempre funciona:\n\n"
                "$$\\boxed{\\,x = \\dfrac{-b \\pm \\sqrt{b^2 - 4 a c}}{2 a}.\\,}$$\n\n"
                "**Método 3 — Completación de cuadrados.** Reescribir como $(x + p)^2 = q$ y despejar.\n\n"
                "Ejemplo: $x^2 + 6 x + 5 = 0 \\Rightarrow x^2 + 6 x = -5 \\Rightarrow x^2 + 6 x + 9 = 4 \\Rightarrow (x + 3)^2 = 4 \\Rightarrow x + 3 = \\pm 2 \\Rightarrow x = -1, -5$.\n\n"
                "**Discriminante** $\\Delta = b^2 - 4 a c$ clasifica las soluciones:\n\n"
                "- $\\Delta > 0$: **dos soluciones reales distintas**.\n"
                "- $\\Delta = 0$: **una solución real (doble)**.\n"
                "- $\\Delta < 0$: **dos soluciones complejas conjugadas** (no reales)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Cuadrática con fórmula general",
          problema_md="Resuelve $2 x^2 - 5 x - 3 = 0$.",
          pasos=[
              {"accion_md": (
                  "**Identificar coeficientes:** $a = 2$, $b = -5$, $c = -3$.\n\n"
                  "**Discriminante:** $\\Delta = (-5)^2 - 4 \\cdot 2 \\cdot (-3) = 25 + 24 = 49 > 0$. Dos soluciones reales."
              ),
               "justificacion_md": "Cuidar el signo de $-3$ al calcular $4 a c$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar fórmula:** $x = \\dfrac{5 \\pm \\sqrt{49}}{4} = \\dfrac{5 \\pm 7}{4}$.\n\n"
                  "$x_1 = \\dfrac{5 + 7}{4} = 3$, $x_2 = \\dfrac{5 - 7}{4} = -\\dfrac{1}{2}$.\n\n"
                  "**Verificar.** $x = 3$: $2 \\cdot 9 - 15 - 3 = 0$ ✓. $x = -1/2$: $2 \\cdot 1/4 + 5/2 - 3 = 1/2 + 5/2 - 3 = 0$ ✓."
              ),
               "justificacion_md": "Buena práctica: siempre verificar al menos una solución.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Completación de cuadrados",
          problema_md="Resuelve $x^2 + 2 x - 5 = 0$ por completación de cuadrados.",
          pasos=[
              {"accion_md": (
                  "**Aislar el término constante:** $x^2 + 2 x = 5$.\n\n"
                  "**Completar:** la mitad del coeficiente de $x$ es $1$; su cuadrado es $1$. Sumar a ambos lados:\n\n"
                  "$x^2 + 2 x + 1 = 6 \\Rightarrow (x + 1)^2 = 6$."
              ),
               "justificacion_md": "El truco: la **mitad** del coeficiente de $x$, **al cuadrado**.",
               "es_resultado": False},
              {"accion_md": (
                  "**Tomar raíz:** $x + 1 = \\pm \\sqrt{6} \\Rightarrow x = -1 \\pm \\sqrt{6}$."
              ),
               "justificacion_md": "Las dos soluciones (con $\\pm$). $x_1 \\approx 1{,}45$, $x_2 \\approx -3{,}45$.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Ecuaciones especiales",
            body=(
                "**Con fracciones:** multiplicar por el común múltiplo de los denominadores. **Verificar** que las soluciones no anulen ningún denominador (caso contrario, son **espurias** y se descartan).\n\n"
                "**Con raíces:** **aislar** la raíz y **elevar al cuadrado** (o al índice). Como elevar puede introducir soluciones espurias, **siempre verificar**.\n\n"
                "Ejemplo: $\\sqrt{2 x + 1} = x - 1 \\Rightarrow 2 x + 1 = (x - 1)^2 = x^2 - 2 x + 1 \\Rightarrow x^2 - 4 x = 0 \\Rightarrow x = 0$ o $x = 4$. "
                "Verificar: $x = 0$: $\\sqrt{1} = -1$ **falso** (espuria). $x = 4$: $\\sqrt{9} = 3$ ✓.\n\n"
                "**Con valor absoluto:** $|A| = c$ con $c \\geq 0$ se desdobla en $A = c$ o $A = -c$. Si $c < 0$, **no hay solución**.\n\n"
                "Ejemplo: $|3 x + 5| = 1 \\Rightarrow 3 x + 5 = 1$ o $3 x + 5 = -1 \\Rightarrow x = -4/3$ o $x = -2$.\n\n"
                "**Polinómicas de grado $\\geq 3$:** factorizar (factor común, agrupación, productos notables, regla de Ruffini para hallar raíces racionales)."
            ),
        ),

        b("intuicion", body_md=(
            "**Por qué siempre verificar.** Algunas operaciones que aplicamos **no son reversibles** y "
            "pueden introducir 'soluciones' espurias:\n\n"
            "- **Elevar al cuadrado:** $x = -1$ implica $x^2 = 1$, pero $x^2 = 1$ tiene también la solución $x = 1$.\n"
            "- **Multiplicar por una expresión variable:** si esta es cero para algún valor, ese valor 'aparece' como solución sin serlo.\n"
            "- **Eliminar denominadores:** si el valor anula un denominador del original, no es solución válida.\n\n"
            "**Discriminante geométricamente.** La parábola $y = a x^2 + b x + c$ corta al eje $x$:\n\n"
            "- **dos veces** si $\\Delta > 0$ (dos raíces reales distintas);\n"
            "- **una vez** (tangente) si $\\Delta = 0$ (raíz doble);\n"
            "- **no corta** si $\\Delta < 0$ (raíces complejas — la parábola está toda arriba o toda abajo del eje)."
        )),

        fig(
            "Tres parábolas en un mismo plano cartesiano mostrando los tres casos según el discriminante. "
            "Parábola izquierda Δ > 0 en teal #06b6d4: corta al eje x en dos puntos distintos (marcas en x = -1 y x = 3, por ejemplo). "
            "Parábola central Δ = 0 en ámbar #f59e0b: tangente al eje x en un solo punto (marca x = 2). "
            "Parábola derecha Δ < 0 en gris: completamente arriba del eje x sin tocarlo. "
            "Eje x horizontal con marcas, eje y vertical. Anotaciones de Δ debajo de cada parábola. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "La solución de $5 x - 4 = 21$ es:",
                  "opciones_md": ["$x = 4$", "**$x = 5$**", "$x = 21/5$", "$x = 17$"],
                  "correcta": "B",
                  "pista_md": "Sumar 4 y dividir por 5.",
                  "explicacion_md": "$5 x = 25 \\Rightarrow x = 5$. Verificar: $25 - 4 = 21$ ✓.",
              },
              {
                  "enunciado_md": "El discriminante de $x^2 + 3 x + 5$ es:",
                  "opciones_md": ["$29$", "**$-11$**", "$11$", "$9$"],
                  "correcta": "B",
                  "pista_md": "$\\Delta = b^2 - 4 a c = 9 - 20$.",
                  "explicacion_md": "$\\Delta = -11 < 0$: la cuadrática no tiene raíces reales.",
              },
              {
                  "enunciado_md": "Las soluciones de $|x - 3| = 4$ son:",
                  "opciones_md": [
                      "$x = 7$ solamente",
                      "$x = -7$ solamente",
                      "**$x = 7$ o $x = -1$**",
                      "$x = 4$ o $x = -4$",
                  ],
                  "correcta": "C",
                  "pista_md": "Desdoblar: $x - 3 = 4$ o $x - 3 = -4$.",
                  "explicacion_md": "$x = 7$ o $x = -1$.",
              },
          ]),

        ej(
            "Cuadrática por factorización",
            "Resuelve $x^2 - x - 12 = 0$.",
            ["Buscar dos números con suma $-1$ y producto $-12$."],
            (
                "$(x + 3)(x - 4) = 0 \\Rightarrow x = -3$ o $x = 4$."
            ),
        ),

        ej(
            "Con fracciones",
            "Resuelve $\\dfrac{1}{x - 1} + \\dfrac{1}{x + 2} = \\dfrac{5}{4}$.",
            ["Multiplicar todo por $4(x - 1)(x + 2)$ y reducir."],
            (
                "$4(x + 2) + 4(x - 1) = 5(x - 1)(x + 2)$. Expandir: $8 x + 4 = 5 x^2 + 5 x - 10$. Reducir: $5 x^2 - 3 x - 14 = 0$. Fórmula: $x = (3 \\pm \\sqrt{9 + 280})/10 = (3 \\pm 17)/10 \\Rightarrow x = 2$ o $x = -7/5$. "
                "Ninguna anula los denominadores ($x \\neq 1, -2$), así ambas son válidas."
            ),
        ),

        ej(
            "Con raíz",
            "Resuelve $\\sqrt{2 x + 1} + 1 = x$.",
            ["Aislar la raíz, elevar al cuadrado, verificar."],
            (
                "$\\sqrt{2 x + 1} = x - 1 \\Rightarrow 2 x + 1 = x^2 - 2 x + 1 \\Rightarrow x^2 - 4 x = 0 \\Rightarrow x(x - 4) = 0$. "
                "$x = 0$: $\\sqrt{1} = -1$ **falso** (espuria). $x = 4$: $\\sqrt{9} = 3 = 4 - 1$ ✓. **Solución única:** $x = 4$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**No verificar las soluciones** especialmente al elevar al cuadrado o multiplicar por una expresión variable. Pueden ser espurias.",
              "**Olvidar el ± al sacar raíz cuadrada.** $(x + 1)^2 = 4 \\Rightarrow x + 1 = \\pm 2$, no solo $+2$.",
              "**Equivocar el signo en la fórmula cuadrática.** $-b$, no $b$. Y $b^2$ es siempre positivo (aun si $b < 0$).",
              "**Dividir por una expresión que puede ser cero.** Por ejemplo, dividir por $(x - 2)$ pierde la posible solución $x = 2$.",
              "**Tratar $|A| = c$ con $c < 0$ como si tuviera solución.** El valor absoluto siempre $\\geq 0$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Lineales:** despejar usando propiedades de igualdad. Una solución única (si $a \\neq 0$).",
              "**Cuadráticas:** factorización (rápido), fórmula general (siempre), completación (técnica).",
              "**Discriminante** $\\Delta = b^2 - 4 a c$: $> 0$ dos reales, $= 0$ una doble, $< 0$ complejas.",
              "**Especiales:** fracciones (verificar denominadores), raíces (verificar), valor absoluto (desdoblar).",
              "**Próxima lección:** desigualdades — ecuaciones con $<, >, \\leq, \\geq$ en vez de $=$.",
          ]),
    ]
    return {
        "id": "lec-prec-1-7-ecuaciones",
        "title": "Ecuaciones",
        "description": "Resolución de ecuaciones lineales y cuadráticas (factorización, fórmula general, completación de cuadrados, discriminante). Ecuaciones con fracciones, raíces y valor absoluto, con verificación de soluciones espurias.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 7,
    }


# =====================================================================
# Inecuaciones
# =====================================================================
def lesson_inecuaciones():
    blocks = [
        b("texto", body_md=(
            "Una **inecuación** es una **desigualdad** entre expresiones que contiene una incógnita. Su "
            "solución no es uno o varios números aislados, sino **un intervalo** (o unión de intervalos) "
            "de la recta real.\n\n"
            "$$2 x + 3 < 11 \\;\\Longleftrightarrow\\; x < 4 \\;\\Longleftrightarrow\\; x \\in (-\\infty, 4).$$\n\n"
            "El procedimiento es similar al de ecuaciones, pero hay una **regla crítica nueva**: "
            "**multiplicar o dividir por un negativo invierte el sentido de la desigualdad**.\n\n"
            "**Al terminar:**\n\n"
            "- Resuelves inecuaciones lineales y compuestas, expresando soluciones como intervalos.\n"
            "- Resuelves inecuaciones cuadráticas usando **tabla de signos**.\n"
            "- Manejas inecuaciones racionales y con valor absoluto.\n"
            "- Recordás invertir el sentido al multiplicar/dividir por negativos."
        )),

        formulas(
            titulo="Propiedades de la desigualdad",
            body=(
                "Sean $a, b, c \\in \\mathbb{R}$.\n\n"
                "**Suma/resta:** Si $a < b$, entonces $a + c < b + c$ (no invierte).\n\n"
                "**Multiplicación por $c > 0$:** Si $a < b$, entonces $a c < b c$ (no invierte).\n\n"
                "**Multiplicación por $c < 0$:** Si $a < b$, entonces $a c > b c$ (**¡invierte!**).\n\n"
                "**Transitividad:** Si $a < b$ y $b < c$, entonces $a < c$.\n\n"
                "**Inversión:** si $a, b > 0$, entonces $a < b \\Leftrightarrow 1/a > 1/b$ (al invertir cambia el sentido).\n\n"
                "**Reglas análogas para $\\leq, >, \\geq$.**\n\n"
                "**La regla del negativo es la trampa principal.** Olvidarla cambia el resultado completamente."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Lineal con inversión",
          problema_md="Resuelve $5 - 3 x \\geq -16$.",
          pasos=[
              {"accion_md": (
                  "**Restar $5$ a ambos lados:** $-3 x \\geq -21$."
              ),
               "justificacion_md": "Suma/resta no invierte.",
               "es_resultado": False},
              {"accion_md": (
                  "**Dividir por $-3$ — ¡INVIERTE!** $x \\leq 7$.\n\n"
                  "**Solución:** $x \\in (-\\infty, 7]$."
              ),
               "justificacion_md": "Olvidar invertir es el error más común.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Inecuación compuesta",
          problema_md="Resuelve $1 < 2 x - 5 < 7$.",
          pasos=[
              {"accion_md": (
                  "**Aplicar la operación a los TRES miembros simultáneamente.**\n\n"
                  "Sumar $5$: $6 < 2 x < 12$.\n\n"
                  "Dividir por $2$: $3 < x < 6$."
              ),
               "justificacion_md": "Misma operación a los tres miembros mantiene los dos sentidos.",
               "es_resultado": False},
              {"accion_md": "**Solución:** $x \\in (3, 6)$.",
               "justificacion_md": "Estricta en ambos extremos → paréntesis.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Inecuaciones cuadráticas: tabla de signos",
            body=(
                "Procedimiento estándar para $a x^2 + b x + c \\lessgtr 0$:\n\n"
                "1. **Llevar todo a un lado** (= 0 al otro).\n"
                "2. **Factorizar** (o usar la fórmula cuadrática para hallar raíces).\n"
                "3. **Marcar las raíces** en la recta real — dividen $\\mathbb{R}$ en intervalos.\n"
                "4. **Estudiar el signo** del producto factorizado en cada intervalo.\n"
                "5. **Seleccionar** los intervalos donde se cumple la desigualdad.\n\n"
                "**Atención a los extremos.** Si la desigualdad es **estricta** ($<, >$), los puntos donde "
                "la expresión se anula **no** se incluyen. Si es **no estricta** ($\\leq, \\geq$), **sí** se incluyen."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Cuadrática con tabla de signos",
          problema_md="Resuelve $x^2 - 3 x - 18 \\geq 0$.",
          pasos=[
              {"accion_md": (
                  "**Factorizar.** $x^2 - 3 x - 18 = (x - 6)(x + 3)$. Raíces: $x = 6, -3$."
              ),
               "justificacion_md": "Buscar dos números con suma $-3$ y producto $-18$: $-6$ y $3$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Tabla de signos** en los intervalos $(-\\infty, -3), (-3, 6), (6, +\\infty)$:\n\n"
                  "| Intervalo | $x + 3$ | $x - 6$ | producto |\n"
                  "|---|---|---|---|\n"
                  "| $x < -3$ | − | − | **+** |\n"
                  "| $-3 < x < 6$ | + | − | **−** |\n"
                  "| $x > 6$ | + | + | **+** |"
              ),
               "justificacion_md": "Probar un punto de cada intervalo: ej. $x = -4, 0, 7$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Buscamos producto $\\geq 0$** (no estricta, así incluir los ceros): intervalos $(-\\infty, -3]$ y $[6, +\\infty)$.\n\n"
                  "**Solución:** $x \\in (-\\infty, -3] \\cup [6, +\\infty)$."
              ),
               "justificacion_md": "Los extremos $-3$ y $6$ se incluyen porque la desigualdad es $\\geq$.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Inecuaciones racionales y con valor absoluto",
            body=(
                "**Racionales** $\\dfrac{P(x)}{Q(x)} \\lessgtr 0$:\n\n"
                "1. Llevar todo a un lado y combinar en una sola fracción.\n"
                "2. Factorizar numerador y denominador.\n"
                "3. **Puntos críticos:** raíces del numerador (donde la fracción se anula) y del denominador (donde no está definida).\n"
                "4. Tabla de signos como en cuadráticas.\n"
                "5. **Los ceros del denominador NUNCA se incluyen** (aunque la desigualdad sea no estricta).\n\n"
                "Ejemplo: $\\dfrac{2 x + 6}{x - 2} < 0$. Puntos críticos: $-3$ (cero numerador), $2$ (cero denominador). Tabla → solución $(-3, 2)$.\n\n"
                "**Con valor absoluto.** Dos casos clave:\n\n"
                "- $|x| \\leq a$ (con $a \\geq 0$) $\\Leftrightarrow -a \\leq x \\leq a \\Leftrightarrow x \\in [-a, a]$.\n"
                "- $|x| \\geq a$ (con $a \\geq 0$) $\\Leftrightarrow x \\leq -a$ o $x \\geq a \\Leftrightarrow x \\in (-\\infty, -a] \\cup [a, +\\infty)$.\n\n"
                "Generalización: $|f(x)| \\leq a \\Leftrightarrow -a \\leq f(x) \\leq a$. Para $|x - 5| \\leq 3$: $-3 \\leq x - 5 \\leq 3 \\Leftrightarrow 2 \\leq x \\leq 8$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Racional",
          problema_md="Resuelve $\\dfrac{x + 1}{x - 3} \\leq 0$.",
          pasos=[
              {"accion_md": (
                  "**Puntos críticos.** Numerador cero: $x = -1$. Denominador cero: $x = 3$.\n\n"
                  "**Tabla:** intervalos $(-\\infty, -1), (-1, 3), (3, +\\infty)$.\n\n"
                  "| Intervalo | $x + 1$ | $x - 3$ | cociente |\n"
                  "|---|---|---|---|\n"
                  "| $x < -1$ | − | − | **+** |\n"
                  "| $-1 < x < 3$ | + | − | **−** |\n"
                  "| $x > 3$ | + | + | **+** |"
              ),
               "justificacion_md": "Mismo procedimiento que cuadráticas, pero ahora hay un punto donde está indefinido.",
               "es_resultado": False},
              {"accion_md": (
                  "**Buscamos cociente $\\leq 0$:** intervalo $[-1, 3)$. Incluir $-1$ (cociente vale 0), **excluir $3$** (denominador se anula).\n\n"
                  "**Solución:** $x \\in [-1, 3)$."
              ),
               "justificacion_md": "El extremo $3$ siempre queda abierto.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué se invierte el sentido al multiplicar por negativo.** Geométricamente: si dos números "
            "$a < b$ están en la recta real, multiplicar por $-1$ los **refleja** en el origen — "
            "$-a > -b$ porque el orden se da vuelta. Multiplicar por cualquier negativo es equivalente a "
            "multiplicar por su valor absoluto (no invierte) y por $-1$ (invierte).\n\n"
            "**Por qué la tabla de signos.** Una expresión polinomial cambia de signo **solo** en sus raíces. "
            "Entre dos raíces consecutivas, el signo es constante. Por eso basta probar un punto en cada "
            "intervalo para conocer el signo en todo el intervalo.\n\n"
            "**Para racionales:** además de cambiar de signo en los ceros del numerador, cambia en los del "
            "denominador (donde 'pasa por infinito'). Por eso ambos tipos de puntos van a la tabla."
        )),

        fig(
            "Tabla de signos visual para (x + 3)(x - 6) ≥ 0. "
            "Recta real horizontal con marcas en -3 y 6 (puntos llenos por ser ≥). "
            "Tres regiones marcadas con signos: '+' a la izquierda de -3, '−' entre -3 y 6, '+' a la derecha de 6. "
            "Las regiones positivas (a la izquierda de -3 y a la derecha de 6) sombreadas en color teal #06b6d4. "
            "Etiqueta arriba: 'Solución: (-∞, -3] ∪ [6, +∞)'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$-2 x > 6$ implica:",
                  "opciones_md": [
                      "$x > -3$",
                      "**$x < -3$**",
                      "$x > 3$",
                      "$x < 3$",
                  ],
                  "correcta": "B",
                  "pista_md": "Dividir por $-2$ invierte.",
                  "explicacion_md": "$x < -3$: el sentido cambia.",
              },
              {
                  "enunciado_md": "Solución de $|x| < 5$:",
                  "opciones_md": [
                      "$x < -5$ o $x > 5$",
                      "**$-5 < x < 5$**",
                      "$x = \\pm 5$",
                      "$x > 5$",
                  ],
                  "correcta": "B",
                  "pista_md": "$|x| < a$ ↔ $-a < x < a$.",
                  "explicacion_md": "Intervalo abierto centrado en cero.",
              },
              {
                  "enunciado_md": "Solución de $\\dfrac{x - 2}{x + 1} > 0$:",
                  "opciones_md": [
                      "$(-1, 2)$",
                      "**$(-\\infty, -1) \\cup (2, +\\infty)$**",
                      "$(-\\infty, -1) \\cup (2, +\\infty)$ y $x \\neq 0$",
                      "$\\mathbb{R}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Tabla de signos con puntos críticos $-1$ (denom) y $2$ (num).",
                  "explicacion_md": "Cociente positivo cuando ambos del mismo signo.",
              },
          ]),

        ej(
            "Lineal",
            "Resuelve $4 - 2 x \\leq 10$.",
            ["Restar 4 y dividir por $-2$ (invierte)."],
            (
                "$-2 x \\leq 6 \\Rightarrow x \\geq -3$. **Solución:** $[-3, +\\infty)$."
            ),
        ),

        ej(
            "Cuadrática",
            "Resuelve $x^2 < 4$.",
            ["Llevar a $x^2 - 4 < 0$ y factorizar."],
            (
                "$(x + 2)(x - 2) < 0$. Tabla de signos da producto negativo en $(-2, 2)$. **Solución:** $(-2, 2)$."
            ),
        ),

        ej(
            "Valor absoluto",
            "Resuelve $|2 x - 1| \\geq 5$.",
            ["Desdoblar: $2 x - 1 \\geq 5$ o $2 x - 1 \\leq -5$."],
            (
                "$2 x \\geq 6 \\Rightarrow x \\geq 3$, o $2 x \\leq -4 \\Rightarrow x \\leq -2$. **Solución:** $(-\\infty, -2] \\cup [3, +\\infty)$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar invertir** al multiplicar/dividir por un negativo. Es el error más común.",
              "**Multiplicar ambos lados por una expresión variable** sin saber su signo. La inecuación racional se debe llevar primero a 'algo $\\lessgtr 0$' y usar tabla de signos.",
              "**Incluir los ceros del denominador** en la solución de una racional. Nunca se incluyen.",
              "**Tratar $|A| > c$ como $A > c$ y $A > -c$.** Lo correcto es $A > c$ **o** $A < -c$ (con 'o', no 'y').",
              "**Aplicar la operación solo a un miembro de una compuesta** $a < b < c$. Hay que aplicarla a los tres.",
          ]),

        b("resumen",
          puntos_md=[
              "**Lineales:** despejar como ecuaciones, **invirtiendo** al usar negativos. Solución es un intervalo.",
              "**Compuestas $a < f(x) < c$:** operar simultáneamente sobre los tres miembros.",
              "**Cuadráticas y racionales:** llevar a 'algo $\\lessgtr 0$', factorizar, hacer **tabla de signos**.",
              "**Valor absoluto:** $|f| \\leq a$ ↔ $-a \\leq f \\leq a$; $|f| \\geq a$ ↔ $f \\leq -a$ o $f \\geq a$.",
              "**Cierre del capítulo:** con números reales, conjuntos, potencias, expresiones algebraicas, factorización, racionales, ecuaciones e inecuaciones tienes las **bases** del precálculo.",
              "**Próximo capítulo:** **Funciones** — el concepto central que une todo lo anterior con el cálculo.",
          ]),
    ]
    return {
        "id": "lec-prec-1-8-inecuaciones",
        "title": "Inecuaciones",
        "description": "Inecuaciones lineales (con la regla del negativo), compuestas, cuadráticas (tabla de signos), racionales (puntos críticos numerador y denominador) y con valor absoluto.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 8,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "precalculo"

    course_doc = {
        "id": course_id,
        "title": "Precálculo",
        "description": (
            "Curso de fundamentos matemáticos para entrar a la universidad: números, álgebra, funciones "
            "(polinomiales, racionales, exponenciales, logarítmicas, trigonométricas), trigonometría "
            "analítica, números complejos y sucesiones y series."
        ),
        "category": "Matemáticas",
        "level": "Inicial",
        "modules_count": 8,
        "rating": 4.8,
        "summary": "Curso completo de precálculo para alumnos universitarios y preparación PAES.",
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

    chapter_id = "ch-prec-fundamentos"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Fundamentos",
        "description": (
            "Números reales, conjuntos e intervalos, potencias y raíces, expresiones algebraicas, "
            "factorización, expresiones racionales, ecuaciones e inecuaciones."
        ),
        "order": 1,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_numeros_reales,
        lesson_conjuntos_intervalos,
        lesson_potencias_raices,
        lesson_expresiones_algebraicas,
        lesson_factorizacion,
        lesson_expresiones_racionales,
        lesson_ecuaciones,
        lesson_inecuaciones,
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
        f"✅ Capítulo 1 — Fundamentos listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())


