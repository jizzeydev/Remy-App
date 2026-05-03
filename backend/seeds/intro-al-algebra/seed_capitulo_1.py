"""
Seed del curso Introducción al Álgebra — Capítulo 1: El Lenguaje Matemático.
6 lecciones (alineadas con MAT1207 PUC, "INTRODUCCIÓN AL ÁLGEBRA Y GEOMETRÍA"):
  1.1 Conectivos Lógicos
  1.2 Leyes de la Lógica
  1.3 Reglas de Inferencia
  1.4 Técnicas de Demostración
  1.5 Conjuntos y Operaciones
  1.6 Cuantificadores

ENFOQUE: este capítulo construye el lenguaje en el que se enuncian, demuestran y
discuten todas las ideas matemáticas posteriores. Es la base obligada para el resto
del curso (Números Naturales, Trigonometría, Polinomios, Geometría Analítica) y
para cualquier curso universitario de matemáticas que use linked-chapters sobre él.

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


def now():
    return datetime.now(timezone.utc).isoformat()


STYLE = (
    "Estilo: diagrama matemático educativo limpio, fondo blanco, líneas claras, "
    "etiquetas en español, notación matemática con buena tipografía. Acentos teal "
    "#06b6d4 y ámbar #f59e0b. Sin sombras dramáticas. Apto para libro universitario."
)


# ============================================================================
# Identificadores del curso y capítulo
# ============================================================================
COURSE_ID = "intro-al-algebra"
COURSE_TITLE = "Introducción al Álgebra"
COURSE_DESCRIPTION = (
    "Curso fundacional que construye el lenguaje matemático universitario. "
    "Cubre lógica proposicional, teoría de conjuntos, cuantificadores, inducción, "
    "sucesiones, trigonometría, polinomios complejos y geometría analítica de las "
    "cónicas. Es la base de los cursos universitarios de Álgebra, Cálculo y "
    "Geometría que se construyen sobre estos contenidos.\n\n"
    "Inspirado en el programa **MAT1207** de la Pontificia Universidad Católica "
    "de Chile (Texto guía: *Álgebra e introducción al cálculo*, Irene Mikenberg)."
)
COURSE_CATEGORY = "Matemáticas"
COURSE_LEVEL = "Intermedio"
COURSE_MODULES_COUNT = 5

CHAPTER_ID = "ch-ia-lenguaje"
CHAPTER_TITLE = "El Lenguaje Matemático"
CHAPTER_DESCRIPTION = (
    "El idioma en el que se escriben y demuestran todos los teoremas. Aquí se "
    "estudia la lógica proposicional, las leyes algebraicas que rigen las "
    "fórmulas lógicas, las reglas que permiten inferir conclusiones válidas, "
    "los métodos de demostración (directa, contrarrecíproca, absurdo), la "
    "teoría básica de conjuntos y los cuantificadores universal y existencial."
)
CHAPTER_ORDER = 1


# ============================================================================
# 1.1 Conectivos Lógicos
# ============================================================================
def lesson_1_1():
    blocks = [
        b("texto", body_md=(
            "La **lógica proposicional** constituye el lenguaje fundamental de las "
            "matemáticas. Cada vez que demostramos un teorema, resolvemos una ecuación "
            "o verificamos un algoritmo, estamos aplicando —de manera consciente o "
            "inconsciente— las reglas de los conectivos lógicos.\n\n"
            "En esta lección estudiaremos los bloques fundamentales del razonamiento "
            "lógico: desde la noción de **proposición** y **valor de verdad**, hasta "
            "las **tablas de verdad** de cada conectivo (negación, conjunción, "
            "disyunción, implicación y equivalencia), pasando por **tautologías** y "
            "**contradicciones**. Al terminar serás capaz de:\n\n"
            "- Identificar qué es una proposición y asignarle un valor de verdad.\n"
            "- Construir la tabla de verdad de cualquier proposición compuesta.\n"
            "- Reconocer tautologías y contradicciones."
        )),

        b("definicion",
          titulo="Proposición",
          body_md=(
              "Una **proposición** es una frase declarativa —no necesariamente "
              "matemática— que puede clasificarse sin ambigüedad como **verdadera** "
              "($V$) o **falsa** ($F$), pero nunca ambas simultáneamente.\n\n"
              "Las proposiciones se denotan con letras minúsculas: $p$, $q$, $r$, "
              "$s$, $\\ldots$\n\n"
              "**No son proposiciones** las preguntas, las órdenes, los deseos ni "
              "las exclamaciones, pues no tienen un valor de verdad definido."
          )),

        b("ejemplo_resuelto",
          titulo="¿Es proposición? ¿Cuál es su valor de verdad?",
          problema_md=(
              "Para cada una de las siguientes expresiones, indique si es una "
              "proposición y, en caso de serlo, asigne su valor de verdad.\n\n"
              "1. $p$: «La suma de los ángulos interiores de un triángulo es $180°$.»\n"
              "2. $q$: «$2 + 1 = 5$.»\n"
              "3. $r$: «$1 \\ge 0$.»\n"
              "4. $\\ell$: «Siéntate.»\n"
              "5. $m$: «¿Cuánto mide este ángulo?»"
          ),
          pasos=[
              {"accion_md": "$p$ es una **proposición** verdadera ($V$): es un teorema clásico de geometría euclidiana.",
               "justificacion_md": "Es declarativa y tiene valor de verdad bien definido.",
               "es_resultado": False},
              {"accion_md": "$q$ es una **proposición** falsa ($F$): $2+1 = 3 \\neq 5$.",
               "justificacion_md": "Es declarativa con un valor de verdad concreto.",
               "es_resultado": False},
              {"accion_md": "$r$ es una **proposición** verdadera ($V$).",
               "justificacion_md": "$1$ es mayor o igual que $0$.",
               "es_resultado": False},
              {"accion_md": "$\\ell$ **no es** una proposición: es una orden, no una declaración verdadera o falsa.",
               "justificacion_md": "No tiene valor de verdad asignable.",
               "es_resultado": False},
              {"accion_md": "$m$ **no es** una proposición: es una pregunta.",
               "justificacion_md": "Las preguntas no son ni verdaderas ni falsas.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Conectivos lógicos fundamentales",
          body_md=(
              "Dadas dos proposiciones $p$ y $q$, los **conectivos lógicos** "
              "construyen nuevas proposiciones cuyo valor de verdad queda "
              "totalmente determinado por los valores de $p$ y $q$:\n\n"
              "- **Negación** $\\bar{p}$ (o $\\lnot p$): verdadera cuando $p$ es falsa.\n"
              "- **Conjunción** $p \\wedge q$ («$p$ **y** $q$»): verdadera **solo** "
              "cuando ambas son verdaderas.\n"
              "- **Disyunción** $p \\vee q$ («$p$ **o** $q$»): falsa **únicamente** "
              "cuando ambas son falsas (es el «o» **inclusivo**).\n"
              "- **Implicación** $p \\Rightarrow q$ («si $p$, entonces $q$»): falsa "
              "**solo** cuando $p$ es verdadera y $q$ es falsa.\n"
              "- **Equivalencia** $p \\Leftrightarrow q$ («$p$ si y solo si $q$»): "
              "verdadera cuando $p$ y $q$ comparten el mismo valor de verdad."
          )),

        fig(
            "Cinco tablas de verdad pequeñas dispuestas en cuadrícula 3x2 (la sexta celda vacía o con título). "
            "Cada tabla tiene encabezado con los símbolos del conectivo correspondiente: "
            "(1) negación: columnas p, ¬p — filas (V,F), (F,V). "
            "(2) conjunción p∧q: columnas p, q, p∧q — filas (V,V,V), (V,F,F), (F,V,F), (F,F,F). "
            "(3) disyunción p∨q: columnas p, q, p∨q — filas (V,V,V), (V,F,V), (F,V,V), (F,F,F). "
            "(4) implicación p⇒q: columnas p, q, p⇒q — filas (V,V,V), (V,F,F), (F,V,V), (F,F,V). "
            "(5) equivalencia p⇔q: columnas p, q, p⇔q — filas (V,V,V), (V,F,F), (F,V,F), (F,F,V). "
            "Encabezados con fondo teal claro, V en verde oscuro, F en rojo apagado, bordes finos negros. " + STYLE
        ),

        b("intuicion", body_md=(
            "**¿Por qué la implicación es \"vacuamente verdadera\" cuando $p$ es falsa?** "
            "Pensá en la promesa: «Si llueve, entonces me mojo.» Si **no** llueve, la "
            "promesa no ha sido violada sin importar si me mojé o no. Por eso "
            "$F \\Rightarrow V$ y $F \\Rightarrow F$ se consideran ambas **verdaderas**.\n\n"
            "La única forma de violar la promesa es que efectivamente llueva ($p$ "
            "verdadera) y aun así no me moje ($q$ falsa). Eso es lo que vuelve "
            "$V \\Rightarrow F$ falsa."
        )),

        b("ejemplo_resuelto",
          titulo="Tabla de verdad compuesta",
          problema_md=(
              "Construya la tabla de verdad de $\\overline{p} \\vee (p \\wedge q)$ "
              "y verifique si es lógicamente equivalente a $p \\Rightarrow q$."
          ),
          pasos=[
              {"accion_md": (
                  "Como hay $2$ variables, la tabla tiene $2^2 = 4$ filas. "
                  "Calculamos las columnas auxiliares $\\overline{p}$, $p \\wedge q$ y "
                  "luego $\\overline{p} \\vee (p \\wedge q)$, comparándola con $p \\Rightarrow q$."
               ),
               "justificacion_md": "Procedimiento estándar: ir desde paréntesis internos hacia afuera.",
               "es_resultado": False},
              {"accion_md": (
                  "| $p$ | $q$ | $\\overline{p}$ | $p \\wedge q$ | $\\overline{p} \\vee (p \\wedge q)$ | $p \\Rightarrow q$ |\n"
                  "|---|---|---|---|---|---|\n"
                  "| V | V | F | V | **V** | **V** |\n"
                  "| V | F | F | F | **F** | **F** |\n"
                  "| F | V | V | F | **V** | **V** |\n"
                  "| F | F | V | F | **V** | **V** |"
               ),
               "justificacion_md": "Cada fila se evalúa aplicando las definiciones de los conectivos.",
               "es_resultado": False},
              {"accion_md": (
                  "Las dos últimas columnas coinciden en cada fila, por lo tanto: "
                  "$$\\overline{p} \\vee (p \\wedge q) \\;\\equiv\\; p \\Rightarrow q.$$"
               ),
               "justificacion_md": "Mismo valor de verdad para todas las asignaciones ⟹ equivalencia lógica.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Tautología y contradicción",
          body_md=(
              "Una proposición compuesta es una **tautología** si su valor de verdad "
              "es **siempre $V$**, sin importar la asignación de las proposiciones "
              "simples. Es una **contradicción** si su valor es **siempre $F$**.\n\n"
              "Las tautologías representan **verdades lógicas universales**; son la "
              "base de todas las leyes lógicas que estudiaremos en la próxima lección.\n\n"
              "Dos ejemplos clásicos:\n\n"
              "- **Principio del tercio excluso:** $p \\vee \\overline{p}$ es tautología.\n"
              "- **Principio de no contradicción:** $p \\wedge \\overline{p}$ es contradicción."
          )),

        ej(
            "Implicación inversa al lenguaje natural",
            ("Sean $p$: «Llueve» y $q$: «El suelo está mojado». Traduzca la "
             "proposición compuesta $p \\Rightarrow q$ al lenguaje natural y construya "
             "su tabla de verdad. ¿Se cumple necesariamente que $q \\Rightarrow p$?"),
            ["Recordá que $p \\Rightarrow q$ se lee «si $p$ entonces $q$».",
             "$q \\Rightarrow p$ se llama **recíproca**; no es lógicamente equivalente a $p \\Rightarrow q$.",
             "Pensá en un caso donde el suelo esté mojado pero no llueva (alguien echó agua, por ejemplo)."],
            ("**Traducción:** «Si llueve, entonces el suelo está mojado». La tabla "
             "de verdad de $p \\Rightarrow q$ es:\n\n"
             "| $p$ | $q$ | $p \\Rightarrow q$ |\n|---|---|---|\n| V | V | V |\n| V | F | F |\n| F | V | V |\n| F | F | V |\n\n"
             "**No** se cumple necesariamente que $q \\Rightarrow p$: si el suelo "
             "está mojado puede ser por otra causa (riego, derrame, etc.). Es un "
             "**contraejemplo** a la implicación recíproca: $q$ verdadera y $p$ "
             "falsa, lo que invalida $q \\Rightarrow p$.")
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $p \\Rightarrow q$ con $q \\Rightarrow p$.** Son distintas: la segunda se llama recíproca y no equivale a la primera.",
              "**Asumir que «$p$ falsa» hace falsa la implicación.** Una implicación con hipótesis falsa es **vacuamente verdadera**.",
              "**Leer el «o» como exclusivo.** En matemática, $p \\vee q$ es **inclusivo**: vale también cuando ambas son verdaderas.",
              "**Pensar que toda oración es proposición.** Preguntas, órdenes y exclamaciones no lo son.",
          ]),

        b("resumen",
          puntos_md=[
              "Una **proposición** es una oración declarativa con valor de verdad bien definido.",
              "Hay cinco conectivos: $\\lnot$, $\\wedge$, $\\vee$, $\\Rightarrow$, $\\Leftrightarrow$. Su tabla de verdad los define completamente.",
              "Una **tautología** es siempre verdadera; una **contradicción**, siempre falsa.",
              "Próxima lección: las leyes algebraicas de la lógica que permiten manipular fórmulas sin construir tablas de verdad.",
          ]),
    ]
    return {
        "id": "lec-ia-1-1-conectivos",
        "title": "Conectivos Lógicos",
        "description": "Proposiciones, tablas de verdad de los conectivos fundamentales y tautologías.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# ============================================================================
# 1.2 Leyes de la Lógica
# ============================================================================
def lesson_1_2():
    blocks = [
        b("texto", body_md=(
            "Al igual que el álgebra ordinaria dispone de leyes que permiten "
            "simplificar expresiones numéricas (distributiva, asociativa, etc.), "
            "la lógica posee un conjunto de **tautologías fundamentales** que "
            "permiten transformar y simplificar fórmulas proposicionales de manera "
            "**algebraica**, sin construir tablas de verdad.\n\n"
            "Dominar estas leyes es indispensable para redactar demostraciones "
            "correctas, diseñar circuitos digitales, verificar programas y "
            "comprender estructuras de datos. En esta lección verás:\n\n"
            "- Las leyes elementales (dominancia, identidad, idempotencia, doble "
            "negación, tercio excluso, consistencia, absorción, relajación).\n"
            "- Las leyes de **De Morgan** y las propiedades algebraicas "
            "(conmutatividad, asociatividad, distributividad).\n"
            "- Cómo demostrar tautologías **algebraicamente**, sin tablas."
        )),

        b("definicion",
          titulo="Equivalencia lógica",
          body_md=(
              "Dos fórmulas proposicionales $\\varphi$ y $\\psi$ son **lógicamente "
              "equivalentes** si $\\varphi \\Leftrightarrow \\psi$ es una "
              "tautología. En tal caso escribimos $\\varphi \\equiv \\psi$ y "
              "podemos sustituir una por la otra en cualquier contexto sin "
              "alterar el valor de verdad."
          )),

        b("teorema",
          enunciado_md=(
              "**Leyes elementales de la lógica.** Para cualesquiera proposiciones "
              "$p$ y $q$ son tautologías:\n\n"
              "| Ley | Equivalencia |\n|---|---|\n"
              "| Dominancia | $p \\vee \\mathbf{V} \\equiv \\mathbf{V}$, $\\;\\;p \\wedge \\mathbf{F} \\equiv \\mathbf{F}$ |\n"
              "| Identidad | $p \\vee \\mathbf{F} \\equiv p$, $\\;\\;p \\wedge \\mathbf{V} \\equiv p$ |\n"
              "| Idempotencia | $p \\vee p \\equiv p$, $\\;\\;p \\wedge p \\equiv p$ |\n"
              "| Doble negación | $\\overline{\\overline{p}} \\equiv p$ |\n"
              "| Tercio excluso | $p \\vee \\overline{p} \\equiv \\mathbf{V}$ |\n"
              "| Consistencia | $p \\wedge \\overline{p} \\equiv \\mathbf{F}$ |\n"
              "| Absorción | $p \\vee (p \\wedge q) \\equiv p$, $\\;\\;p \\wedge (p \\vee q) \\equiv p$ |\n"
              "| Relajación | $(p \\wedge q) \\Rightarrow p$, $\\;\\;p \\Rightarrow (p \\vee q)$ |\n"
              "| Caracterización de la implicación | $(p \\Rightarrow q) \\equiv (\\overline{p} \\vee q)$ |"
          )),

        b("intuicion", body_md=(
            "Las leyes son **instrucciones de manipulación**: te dicen que podés "
            "cambiar un trozo de fórmula por otro equivalente, paso a paso, sin "
            "perder valor de verdad.\n\n"
            "La **caracterización de la implicación** $p \\Rightarrow q \\equiv "
            "\\overline{p} \\vee q$ es especialmente importante: convierte cualquier "
            "implicación en disyunción, abriendo la puerta a usar todas las leyes "
            "algebraicas (que están escritas en términos de $\\wedge$ y $\\vee$)."
        )),

        b("teorema",
          enunciado_md=(
              "**Leyes algebraicas y de De Morgan.** Para proposiciones $p$, $q$, $r$:\n\n"
              "1. **De Morgan:**\n"
              "$$\\overline{p \\wedge q} \\equiv \\overline{p} \\vee \\overline{q}, "
              "\\qquad \\overline{p \\vee q} \\equiv \\overline{p} \\wedge \\overline{q}.$$\n"
              "2. **Conmutatividad:** $p \\vee q \\equiv q \\vee p$, $\\;\\;p \\wedge q \\equiv q \\wedge p$.\n\n"
              "3. **Asociatividad:** $p \\vee (q \\vee r) \\equiv (p \\vee q) \\vee r$, igual con $\\wedge$.\n\n"
              "4. **Distributividad:**\n"
              "$$p \\wedge (q \\vee r) \\equiv (p \\wedge q) \\vee (p \\wedge r),$$\n"
              "$$p \\vee (q \\wedge r) \\equiv (p \\vee q) \\wedge (p \\vee r).$$\n"
              "5. **Equivalencia dividida:** $(p \\Leftrightarrow q) \\equiv (p \\Rightarrow q) \\wedge (q \\Rightarrow p)$."
          )),

        b("intuicion", body_md=(
            "**De Morgan** es la regla más útil para **negar** proposiciones: la "
            "negación de una conjunción es la disyunción de las negaciones, y "
            "viceversa. En lenguaje natural: la negación de «llueve **y** hace "
            "frío» es «no llueve **o** no hace frío».\n\n"
            "**Distributividad** tiene una simetría que el álgebra de los reales "
            "no tiene: tanto $\\wedge$ distribuye sobre $\\vee$ como $\\vee$ "
            "distribuye sobre $\\wedge$ (en aritmética, solo el producto distribuye "
            "sobre la suma)."
        )),

        b("ejemplo_resuelto",
          titulo="Negar una proposición compuesta",
          problema_md=(
              "Exprese, usando las leyes de De Morgan, la negación de:\n\n"
              "(a) «$n$ es par **y** positivo».\n\n"
              "(b) «María estudia matemáticas **o** física»."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Sea $p$: «$n$ es par» y $q$: «$n$ es positivo». La proposición "
                  "es $p \\wedge q$. Por De Morgan: "
                  "$$\\overline{p \\wedge q} \\equiv \\overline{p} \\vee \\overline{q}.$$"
               ),
               "justificacion_md": "La negación de una conjunción es la disyunción de las negaciones.",
               "es_resultado": False},
              {"accion_md": (
                  "Traduciendo: «$n$ **no** es par **o** $n$ **no** es positivo». "
                  "Equivalentemente, «$n$ es impar o no positivo»."
               ),
               "justificacion_md": "Convertimos cada negación al lenguaje natural.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Sea $p$: «estudia matemáticas» y $q$: «estudia física». "
                  "La proposición es $p \\vee q$. Por De Morgan: "
                  "$$\\overline{p \\vee q} \\equiv \\overline{p} \\wedge \\overline{q}.$$"
               ),
               "justificacion_md": "La negación de una disyunción es la conjunción de las negaciones.",
               "es_resultado": False},
              {"accion_md": (
                  "Traduciendo: «María **no** estudia matemáticas **y no** estudia física»."
               ),
               "justificacion_md": "Conjunción explícita de las dos negaciones.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Demostración algebraica de tautología",
          problema_md=(
              "Demuestre **algebraicamente** que "
              "$$(\\overline{p} \\wedge \\overline{q}) \\vee (p \\wedge \\overline{q}) "
              "\\vee (\\overline{p} \\wedge q) \\vee (p \\wedge q) \\;\\equiv\\; \\mathbf{V}.$$"
          ),
          pasos=[
              {"accion_md": (
                  "**Paso 1.** Aplicamos distributividad ($\\wedge$ distribuye sobre $\\vee$) "
                  "agrupando los dos primeros y los dos últimos términos: "
                  "$$\\bigl[(\\overline{p} \\vee p) \\wedge \\overline{q}\\bigr] \\;\\vee\\; "
                  "\\bigl[(\\overline{p} \\vee p) \\wedge q\\bigr].$$"
               ),
               "justificacion_md": "Factorizamos $\\overline{q}$ y $q$ respectivamente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 2.** Por **tercio excluso**, $(\\overline{p} \\vee p) \\equiv \\mathbf{V}$:"
                  "$$= (\\mathbf{V} \\wedge \\overline{q}) \\;\\vee\\; (\\mathbf{V} \\wedge q).$$"
               ),
               "justificacion_md": "$\\overline{p} \\vee p$ es siempre verdadera.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 3.** Por **identidad**, $\\mathbf{V} \\wedge r \\equiv r$: "
                  "$$= \\overline{q} \\;\\vee\\; q.$$"
               ),
               "justificacion_md": "Quitamos las constantes $\\mathbf{V}$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Paso 4.** Por tercio excluso nuevamente, $\\overline{q} \\vee q \\equiv \\mathbf{V}$. "
                  "Por tanto la fórmula es una tautología. $\\blacksquare$"
               ),
               "justificacion_md": "Llegamos a $\\mathbf{V}$ sin construir ninguna tabla.",
               "es_resultado": True},
          ]),

        ej(
            "Caracterización algebraica de la equivalencia",
            ("Demuestre **algebraicamente** que "
             "$$(p \\Leftrightarrow q) \\;\\equiv\\; (\\overline{p} \\wedge \\overline{q}) \\vee (p \\wedge q).$$"),
            ["Empezá usando la equivalencia dividida: $(p \\Leftrightarrow q) \\equiv (p \\Rightarrow q) \\wedge (q \\Rightarrow p)$.",
             "Aplicá caracterización de la implicación a cada factor.",
             "Distribuí $\\wedge$ sobre $\\vee$ y simplificá usando consistencia $p \\wedge \\overline{p} \\equiv \\mathbf{F}$ e identidad $\\mathbf{F} \\vee r \\equiv r$."],
            ("Por equivalencia dividida: $(p \\Leftrightarrow q) \\equiv (p \\Rightarrow q) \\wedge (q \\Rightarrow p)$. "
             "Aplicando caracterización de la implicación a cada factor: "
             "$\\equiv (\\overline{p} \\vee q) \\wedge (\\overline{q} \\vee p)$. "
             "Por distributividad: $\\equiv (\\overline{p} \\wedge \\overline{q}) \\vee (\\overline{p} \\wedge p) "
             "\\vee (q \\wedge \\overline{q}) \\vee (q \\wedge p)$. "
             "Por consistencia los dos términos centrales son $\\mathbf{F}$, y por identidad "
             "$\\mathbf{F} \\vee r \\equiv r$, queda: $(\\overline{p} \\wedge \\overline{q}) \\vee (p \\wedge q)$. $\\blacksquare$")
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar paréntesis en De Morgan.** $\\overline{p \\wedge q} \\neq \\overline{p} \\wedge \\overline{q}$. La barra cubre todo.",
              "**Aplicar distributividad incorrectamente.** Verificá qué conectivo distribuye sobre cuál; ambos sentidos son válidos en lógica.",
              "**Saltar pasos sin justificar.** En una demostración algebraica, cada igualdad debe nombrar la ley aplicada.",
              "**Usar reglas no demostradas.** Solo las leyes del repertorio (o tautologías ya demostradas) pueden invocarse.",
          ]),

        b("resumen",
          puntos_md=[
              "Las leyes lógicas son tautologías que permiten manipular fórmulas algebraicamente.",
              "**De Morgan** permite negar conjunciones y disyunciones intercambiando $\\wedge$ y $\\vee$.",
              "La **caracterización de la implicación** $p \\Rightarrow q \\equiv \\overline{p} \\vee q$ conecta implicaciones con las leyes algebraicas.",
              "Próxima lección: cómo usar estas leyes para inferir conclusiones válidas (Modus Ponens, Modus Tollens, etc.).",
          ]),
    ]
    return {
        "id": "lec-ia-1-2-leyes-logica",
        "title": "Leyes de la Lógica",
        "description": "Tautologías fundamentales, leyes de De Morgan, distributividad y demostración algebraica.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 2,
    }


# ============================================================================
# 1.3 Reglas de Inferencia
# ============================================================================
def lesson_1_3():
    blocks = [
        b("texto", body_md=(
            "Las **reglas de inferencia** son los esquemas que nos permiten derivar "
            "conclusiones **necesariamente verdaderas** a partir de premisas "
            "conocidas. En matemáticas no basta intuir que una conclusión es "
            "verdadera: debemos poder justificar cada paso de nuestro argumento "
            "mediante una regla lógica precisa.\n\n"
            "Esta lección presenta el problema central de la inferencia y las "
            "cuatro reglas fundamentales del curso: **Modus Ponens**, **Implicación "
            "Lógica** (silogismo hipotético), **Modus Tollens** y **Método de "
            "Contradicción**."
        )),

        b("definicion",
          titulo="Inferencia",
          body_md=(
              "Sean $p_1, p_2, \\ldots, p_n$ y $q$ proposiciones. Decimos que $q$ es "
              "**consecuencia lógica** de $p_1, \\ldots, p_n$, o que "
              "$$p_1, p_2, \\ldots, p_n \\;\\Rightarrow\\; q$$\n"
              "es una **inferencia**, si la proposición\n"
              "$$(p_1 \\wedge p_2 \\wedge \\cdots \\wedge p_n) \\Longrightarrow q$$\n"
              "es una **tautología**.\n\n"
              "Es decir: cada vez que las premisas $p_1, \\ldots, p_n$ son "
              "simultáneamente verdaderas, la conclusión $q$ debe ser verdadera "
              "**sin excepción**."
          )),

        b("teorema",
          enunciado_md=(
              "**Modus Ponens.** Si $p$ y $q$ son proposiciones, entonces\n"
              "$$\\bigl[p \\wedge (p \\Rightarrow q)\\bigr] \\;\\Longrightarrow\\; q$$\n"
              "es una tautología.\n\n"
              "*Esquema:* $\\dfrac{p \\quad p \\Rightarrow q}{q}\\;.$"
          )),

        b("intuicion", body_md=(
            "**Modus Ponens** formaliza el razonamiento más básico: si sé que $p$ es "
            "verdadero, **y** además sé que $p$ implica $q$, puedo concluir que $q$ "
            "también es verdadero.\n\n"
            "**Ejemplo cotidiano:** «Si hago las tareas, me gusta la clase. Hoy hice "
            "las tareas». Por Modus Ponens: hoy me gusta la clase."
        )),

        b("teorema",
          enunciado_md=(
              "**Implicación Lógica (silogismo hipotético).** Si $p$, $q$, $r$ son "
              "proposiciones, entonces\n"
              "$$\\bigl[(p \\Rightarrow q) \\wedge (q \\Rightarrow r)\\bigr] "
              "\\;\\Longrightarrow\\; (p \\Rightarrow r)$$\n"
              "es una tautología.\n\n"
              "*Esquema:* $\\dfrac{p \\Rightarrow q \\quad q \\Rightarrow r}{p \\Rightarrow r}\\;.$"
          )),

        b("teorema",
          enunciado_md=(
              "**Modus Tollens.** Si $p$ y $q$ son proposiciones, entonces\n"
              "$$\\bigl[(p \\Rightarrow q) \\wedge \\overline{q}\\bigr] "
              "\\;\\Longrightarrow\\; \\overline{p}$$\n"
              "es una tautología.\n\n"
              "*Esquema:* $\\dfrac{p \\Rightarrow q \\quad \\overline{q}}{\\overline{p}}\\;.$"
          )),

        b("intuicion", body_md=(
            "**Modus Tollens** es la contraparte del Modus Ponens: en lugar de "
            "afirmar la hipótesis para concluir la tesis, **negamos la tesis** para "
            "concluir la negación de la hipótesis. Es la base de la **demostración "
            "por contraposición**: $p \\Rightarrow q$ equivale a "
            "$\\overline{q} \\Rightarrow \\overline{p}$."
        )),

        b("teorema",
          enunciado_md=(
              "**Método de Contradicción (reductio ad absurdum).** Si $p$ es una "
              "proposición y $C$ es una contradicción, entonces\n"
              "$$(\\overline{p} \\Longrightarrow C) \\;\\Longrightarrow\\; p$$\n"
              "es una tautología.\n\n"
              "*Idea:* para demostrar $p$, suponemos $\\overline{p}$ y derivamos un absurdo."
          )),

        b("ejemplo_resuelto",
          titulo="Encadenamiento de reglas de inferencia",
          problema_md=(
              "Pruebe que la siguiente proposición es una inferencia:\n\n"
              "$$\\bigl[(p \\Rightarrow r) \\wedge (\\overline{p} \\Rightarrow q) "
              "\\wedge (q \\Rightarrow s)\\bigr] \\;\\Longrightarrow\\; "
              "(\\overline{r} \\Rightarrow s).$$"
          ),
          pasos=[
              {"accion_md": (
                  "Suponemos que las tres premisas son verdaderas y queremos demostrar "
                  "$\\overline{r} \\Rightarrow s$. Para ello asumimos también $\\overline{r}$ "
                  "(antecedente de la conclusión) y razonamos."
               ),
               "justificacion_md": "Para probar una implicación, suponemos su antecedente.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $p \\Rightarrow r$ es verdadera y $\\overline{r}$ es verdadera, "
                  "por **Modus Tollens** se concluye $\\overline{p}$."
               ),
               "justificacion_md": "Aplicación directa del Modus Tollens a la primera premisa.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $\\overline{p} \\Rightarrow q$ es verdadera y $\\overline{p}$ "
                  "es verdadera, por **Modus Ponens** se concluye $q$."
               ),
               "justificacion_md": "Aplicación de Modus Ponens a la segunda premisa.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $q \\Rightarrow s$ es verdadera y $q$ es verdadera, por "
                  "**Modus Ponens** se concluye $s$.\n\n"
                  "Hemos demostrado $\\overline{r} \\Rightarrow s$ usando solo las tres "
                  "premisas. La proposición es una inferencia. $\\blacksquare$"
               ),
               "justificacion_md": "Aplicación de Modus Ponens a la tercera premisa cierra el argumento.",
               "es_resultado": True},
          ]),

        ej(
            "Silogismo disyuntivo",
            ("Una persona afirma: «Este chaleco es de nylon **o** de lana. **No** es "
             "de nylon». ¿Qué se puede concluir? Identifique la regla de inferencia "
             "(o combinación de reglas) que justifica la conclusión."),
            ["Sean $p$: «el chaleco es de nylon» y $q$: «el chaleco es de lana». Las hipótesis son $p \\vee q$ y $\\overline{p}$.",
             "La conclusión natural es $q$. La tautología asociada se llama **silogismo disyuntivo**.",
             "Para verificarlo, podés escribir $p \\vee q \\equiv \\overline{p} \\Rightarrow q$ (caracterización de la implicación)."],
            ("**Conclusión:** el chaleco es de lana. La regla aplicada es el "
             "**silogismo disyuntivo**: $\\bigl[(p \\vee q) \\wedge \\overline{p}\\bigr] "
             "\\Rightarrow q$. Para verlo como combinación de reglas conocidas: por "
             "caracterización de la implicación, $p \\vee q \\equiv \\overline{p} "
             "\\Rightarrow q$. Como $\\overline{p}$ es verdadera, por **Modus Ponens** "
             "se concluye $q$.")
        ),

        b("errores_comunes",
          items_md=[
              "**Afirmar el consecuente** (falacia): de $p \\Rightarrow q$ y $q$ no se sigue $p$.",
              "**Negar el antecedente** (falacia): de $p \\Rightarrow q$ y $\\overline{p}$ no se sigue $\\overline{q}$.",
              "**Confundir Modus Tollens con la recíproca:** Tollens niega la tesis para concluir la negación de la hipótesis; la recíproca cambia el sentido de la implicación y no es tautología.",
              "**Aplicar Modus Ponens sin tener las dos premisas.** Necesitás $p$ verdadera Y $p \\Rightarrow q$ verdadera.",
          ]),

        b("resumen",
          puntos_md=[
              "Una **inferencia** $p_1, \\ldots, p_n \\Rightarrow q$ es válida cuando $(p_1 \\wedge \\cdots \\wedge p_n) \\Rightarrow q$ es tautología.",
              "**Modus Ponens**, **Implicación Lógica**, **Modus Tollens** y **Método de Contradicción** son las cuatro reglas básicas.",
              "Cualquier demostración matemática es —en el fondo— un encadenamiento de reglas de inferencia.",
              "Próxima lección: cómo organizar estas reglas en métodos de demostración (directa, contrarrecíproca, absurdo, contraejemplo).",
          ]),
    ]
    return {
        "id": "lec-ia-1-3-inferencia",
        "title": "Reglas de Inferencia",
        "description": "Modus Ponens, Modus Tollens, silogismo hipotético y método de contradicción.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# ============================================================================
# 1.4 Técnicas de Demostración
# ============================================================================
def lesson_1_4():
    blocks = [
        b("texto", body_md=(
            "Las **técnicas de demostración** constituyen el núcleo del razonamiento "
            "matemático riguroso. No basta con verificar que algo parece verdadero "
            "en algunos casos: debemos **demostrar** que es verdadero en todos los "
            "casos posibles, o bien encontrar un ejemplo que lo refute.\n\n"
            "Las herramientas se basan en tres tautologías ya conocidas:\n\n"
            "1. **Transitividad:** $(p \\Rightarrow q) \\wedge (q \\Rightarrow r) \\Rightarrow (p \\Rightarrow r)$.\n"
            "2. **Contrarrecíproca:** $(p \\Rightarrow q) \\Leftrightarrow (\\overline{q} \\Rightarrow \\overline{p})$.\n"
            "3. **Reducción al absurdo:** $[(p \\Rightarrow q) \\Leftrightarrow \\mathbf{V}] \\Leftrightarrow [p \\wedge \\overline{q} \\Rightarrow \\mathbf{F}]$."
        )),

        b("definicion",
          titulo="Teorema",
          body_md=(
              "Un **Teorema** es una proposición verdadera —de cierta relevancia "
              "para una teoría— cuya verdad debe ser demostrada.\n\n"
              "Existen dos formas principales de enunciar un teorema:\n\n"
              "- **Tipo implicación:** «Si $p$, entonces $q$.» Aquí $p$ es la "
              "**hipótesis** y $q$ la **tesis**.\n"
              "- **Tipo equivalencia:** «$p$ si y solo si $q$.» Se demuestra "
              "probando ambas implicaciones $p \\Rightarrow q$ y $q \\Rightarrow p$ "
              "por separado."
          )),

        b("teorema",
          enunciado_md=(
              "**Métodos de demostración para $p \\Rightarrow q$:**\n\n"
              "1. **Directo:** Suponer $p$ verdadera y deducir $q$ paso a paso.\n\n"
              "2. **Contrarrecíproca:** Suponer $\\overline{q}$ y deducir $\\overline{p}$. "
              "Equivalente a la directa por la tautología "
              "$(p \\Rightarrow q) \\Leftrightarrow (\\overline{q} \\Rightarrow \\overline{p})$.\n\n"
              "3. **Reducción al absurdo:** Suponer $p \\wedge \\overline{q}$ y derivar "
              "una contradicción $F$. Por la tercera tautología, esto prueba "
              "$p \\Rightarrow q$.\n\n"
              "4. **Contraejemplo:** Para refutar $p \\Rightarrow q$, exhibir un caso "
              "concreto donde $p$ es verdadera y $q$ es falsa."
          )),

        b("ejemplo_resuelto",
          titulo="Demostración directa",
          problema_md=(
              "Pruebe que **si $n$ es par, entonces $n^2$ es par**."
          ),
          pasos=[
              {"accion_md": (
                  "**Hipótesis:** $n$ es par. Entonces existe $k \\in \\mathbb{Z}$ tal "
                  "que $n = 2k$ (definición de número par)."
               ),
               "justificacion_md": "Aplicamos directamente la definición.",
               "es_resultado": False},
              {"accion_md": (
                  "Elevando al cuadrado: "
                  "$$n^2 = (2k)^2 = 4k^2 = 2(2k^2).$$"
               ),
               "justificacion_md": "Manipulación algebraica con factor 2 explícito.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $2k^2 \\in \\mathbb{Z}$, concluimos que $n^2 = 2 \\cdot (\\text{entero})$, "
                  "es decir, $n^2$ es par. $\\blacksquare$"
               ),
               "justificacion_md": "Por definición de número par.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Demostración por contrarrecíproca",
          problema_md=(
              "Pruebe que **si $n^2$ es par, entonces $n$ es par**."
          ),
          pasos=[
              {"accion_md": (
                  "Probaremos la **contrarrecíproca**: si $n$ es impar, entonces "
                  "$n^2$ es impar."
               ),
               "justificacion_md": "Por la equivalencia $(p \\Rightarrow q) \\equiv (\\overline{q} \\Rightarrow \\overline{p})$.",
               "es_resultado": False},
              {"accion_md": (
                  "Si $n$ es impar, existe $k \\in \\mathbb{Z}$ con $n = 2k+1$. Entonces "
                  "$$n^2 = (2k+1)^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1 = 2\\ell + 1,$$\n"
                  "con $\\ell = 2k^2 + 2k \\in \\mathbb{Z}$."
               ),
               "justificacion_md": "Manejo algebraico hasta la forma $2\\ell + 1$.",
               "es_resultado": False},
              {"accion_md": (
                  "Por definición, $n^2$ es impar. Hemos demostrado la contrarrecíproca, "
                  "lo cual prueba la proposición original. $\\blacksquare$"
               ),
               "justificacion_md": "La contrarrecíproca y la implicación original son equivalentes.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Reducción al absurdo: $\\sqrt{2}$ es irracional",
          problema_md=(
              "Pruebe que $\\sqrt{2}$ no es un número racional."
          ),
          pasos=[
              {"accion_md": (
                  "Por contradicción, supongamos que $\\sqrt{2}$ **es** racional. "
                  "Entonces existen $n, m \\in \\mathbb{Z}$ con $m \\neq 0$ tales que "
                  "$\\sqrt{2} = \\frac{m}{n}$. Cancelando factores comunes podemos "
                  "suponer que $m$ y $n$ **no tienen divisores comunes** (salvo $1$)."
               ),
               "justificacion_md": "Negación de la tesis y reducción a la mínima expresión.",
               "es_resultado": False},
              {"accion_md": (
                  "Elevando al cuadrado: $2 = \\dfrac{m^2}{n^2} \\iff 2n^2 = m^2$. "
                  "Por tanto $m^2$ es par, y por el ejemplo anterior $m$ es par. "
                  "Existe entonces $k \\in \\mathbb{Z}$ tal que $m = 2k$."
               ),
               "justificacion_md": "Aplicamos el teorema previo: $n^2$ par implica $n$ par.",
               "es_resultado": False},
              {"accion_md": (
                  "Sustituyendo: $2n^2 = (2k)^2 = 4k^2 \\iff n^2 = 2k^2$. Luego $n^2$ "
                  "es par, así que $n$ también es par."
               ),
               "justificacion_md": "Mismo argumento aplicado a $n$.",
               "es_resultado": False},
              {"accion_md": (
                  "Pero entonces $m$ y $n$ son **ambos pares**, lo cual contradice "
                  "que no tenían divisores comunes (compartirían el factor $2$). "
                  "Esta contradicción prueba que $\\sqrt{2}$ no puede ser racional. $\\blacksquare$"
               ),
               "justificacion_md": "La contradicción refuta la suposición inicial.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Condición necesaria y condición suficiente",
          body_md=(
              "Dada una implicación $p \\Rightarrow q$:\n\n"
              "- $p$ es una **condición suficiente** para $q$ (basta $p$ para que ocurra $q$).\n"
              "- $q$ es una **condición necesaria** para $p$ (sin $q$ no hay $p$).\n\n"
              "Regla mnemotécnica: $$\\text{suficiente} \\;\\Rightarrow\\; \\text{necesario}.$$\n\n"
              "Por ejemplo, «Si $x \\le 1$ entonces $x^4 > 5x - 6$» puede leerse "
              "como «**es suficiente** que $x \\le 1$ para que $x^4 > 5x-6$» o «**es "
              "necesario** que $x^4 > 5x - 6$ para que $x \\le 1$»."
          )),

        b("ejemplo_resuelto",
          titulo="Uso del contraejemplo",
          problema_md=(
              "Determine si la siguiente proposición es verdadera o falsa: "
              "**Si $x^{1/x} = 2^{1/2}$, entonces $x = 2$.**"
          ),
          pasos=[
              {"accion_md": (
                  "La proposición es **falsa**. Para refutarla basta exhibir un "
                  "**contraejemplo**: un valor de $x$ que cumpla la hipótesis pero "
                  "no la conclusión."
               ),
               "justificacion_md": "Una sola excepción basta para refutar una implicación.",
               "es_resultado": False},
              {"accion_md": (
                  "Tomemos $x = 4$. Verificamos: "
                  "$$x^{1/x} = 4^{1/4} = (2^2)^{1/4} = 2^{2/4} = 2^{1/2}.$$\n"
                  "La hipótesis se cumple para $x = 4$, pero la conclusión $x = 2$ **no**."
               ),
               "justificacion_md": "Cálculo directo del contraejemplo.",
               "es_resultado": False},
              {"accion_md": (
                  "Por tanto, $x = 4$ es un contraejemplo y la proposición es **falsa**. $\\blacksquare$"
               ),
               "justificacion_md": "Un contraejemplo refuta cualquier implicación universal.",
               "es_resultado": True},
          ]),

        ej(
            "Demostración por contrarrecíproca con números naturales",
            ("Pruebe la siguiente proposición usando contrarrecíproca: «Si el "
             "producto de dos números naturales $a$ y $b$ es mayor que $36$, "
             "entonces al menos uno de ellos es mayor o igual a $7$.»"),
            ["Sea $p$: $ab > 36$ y $q$: $a \\ge 7 \\;\\lor\\; b \\ge 7$. La contrarrecíproca es $\\overline{q} \\Rightarrow \\overline{p}$.",
             "$\\overline{q}$ es: $a < 7 \\;\\land\\; b < 7$. En naturales esto significa $a \\le 6$ y $b \\le 6$.",
             "Multiplicá las dos desigualdades."],
            ("Probaremos la contrarrecíproca: si $a < 7$ y $b < 7$, entonces $ab \\le 36$. "
             "Como $a, b \\in \\mathbb{N}$, $a < 7 \\Rightarrow a \\le 6$ y análogamente "
             "$b \\le 6$. Entonces $ab \\le 6 \\cdot 6 = 36$, que es precisamente "
             "$\\overline{p}$. Como la contrarrecíproca es verdadera, la proposición "
             "original también lo es. $\\blacksquare$")
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir contrarrecíproca con recíproca.** Contrarrecíproca de $p \\Rightarrow q$ es $\\overline{q} \\Rightarrow \\overline{p}$ (equivalente). Recíproca es $q \\Rightarrow p$ (no equivalente).",
              "**Asumir que basta verificar algunos casos.** «Funciona para $n=1,2,3$» no demuestra para todo $n$.",
              "**Olvidar que un contraejemplo requiere $p$ verdadera y $q$ falsa simultáneamente.** Un caso donde $p$ es falsa no refuta nada.",
              "**Negar mal la tesis al iniciar absurdo.** Cuidado con leyes de De Morgan al negar conjunciones, disyunciones o cuantificadores.",
          ]),

        b("resumen",
          puntos_md=[
              "Las cuatro técnicas básicas son: **directa**, **contrarrecíproca**, **reducción al absurdo** y **contraejemplo**.",
              "Para equivalencias, demostrá las dos implicaciones por separado usando cualquiera de los métodos.",
              "**Suficiente** ⟹ **necesario**: $p$ suficiente para $q$ significa $p \\Rightarrow q$; $q$ necesaria para $p$ significa lo mismo.",
              "Próxima lección: el lenguaje de los **conjuntos**, indispensable para enunciar gran parte de los teoremas matemáticos.",
          ]),
    ]
    return {
        "id": "lec-ia-1-4-demostracion",
        "title": "Técnicas de Demostración",
        "description": "Demostración directa, contrarrecíproca, reducción al absurdo y contraejemplo.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# ============================================================================
# 1.5 Conjuntos y Operaciones
# ============================================================================
def lesson_1_5():
    blocks = [
        b("texto", body_md=(
            "La **teoría de conjuntos** constituye el lenguaje fundamental sobre el "
            "cual se construyen prácticamente todas las ramas de la matemática "
            "moderna. Comprender qué es un conjunto, cómo se describe y cómo se "
            "relaciona con otros conjuntos es el primer paso imprescindible en "
            "cualquier curso de álgebra y geometría.\n\n"
            "Esta lección cubre:\n\n"
            "- Las dos formas de describir un conjunto: por **extensión** y por **comprensión**.\n"
            "- Pertenencia, igualdad, conjunto vacío, conjunto universo y cardinalidad.\n"
            "- **Subconjuntos** e inclusión.\n"
            "- Las operaciones básicas: **unión**, **intersección**, **diferencia** y **complemento**.\n"
            "- Las propiedades algebraicas (conmutatividad, distributividad, De Morgan)."
        )),

        b("definicion",
          titulo="Conjunto, pertenencia y descripción",
          body_md=(
              "Un **conjunto** es una colección bien definida de objetos llamados "
              "**elementos**. Se denotan con mayúsculas $A, B, C, \\ldots$ y sus "
              "elementos con minúsculas.\n\n"
              "**Pertenencia.** Si $a$ es elemento de $A$ escribimos $a \\in A$; si "
              "no lo es, $b \\notin A$.\n\n"
              "**Descripción de conjuntos:**\n\n"
              "- **Por extensión:** se listan los elementos: $A = \\{1, 2, 3\\}$.\n"
              "- **Por comprensión:** se enuncia una propiedad $P(x)$ que cumplen "
              "los elementos: $A = \\{x \\mid P(x)\\}$. Por ejemplo, "
              "$A = \\{x \\in \\mathbb{N} \\mid x < 4\\}$ describe el mismo conjunto "
              "$\\{1, 2, 3\\}$."
          )),

        b("definicion",
          titulo="Igualdad, conjunto vacío, universo, cardinalidad",
          body_md=(
              "**Igualdad.** $A = B$ si y solo si tienen los mismos elementos: "
              "$$A = B \\iff (\\forall x,\\; x \\in A \\iff x \\in B).$$\n"
              "Ni el orden de los elementos ni su repetición afectan el conjunto: "
              "$\\{1, 2, 3\\} = \\{3, 2, 1\\} = \\{1, 1, 2, 3\\}$.\n\n"
              "**Conjunto vacío.** El conjunto sin elementos se denota $\\varnothing$. "
              "Es único y subconjunto de todo conjunto.\n\n"
              "**Conjunto universo $U$.** Conjunto referencial fijo dentro del cual "
              "se trabajan los demás conjuntos.\n\n"
              "**Cardinalidad.** $|A|$ es el número de elementos distintos de $A$ "
              "(cuando es finito)."
          )),

        b("ejemplo_resuelto",
          titulo="El conjunto universo cambia el resultado",
          problema_md=(
              "Considere el conjunto $A = \\{x \\in U \\mid x^2 + 3 = 7\\}$. "
              "Determine $A$ cuando (a) $U = \\mathbb{N}$ y (b) $U = \\mathbb{Z}$."
          ),
          pasos=[
              {"accion_md": (
                  "Resolvemos la ecuación: "
                  "$$x^2 + 3 = 7 \\iff x^2 = 4 \\iff (x-2)(x+2) = 0,$$\n"
                  "cuyas soluciones reales son $x = 2$ y $x = -2$."
               ),
               "justificacion_md": "Diferencia de cuadrados.",
               "es_resultado": False},
              {"accion_md": "**(a)** Si $U = \\mathbb{N}$, solo $x = 2$ pertenece a $U$. Por tanto $A = \\{2\\}$.",
               "justificacion_md": "$-2 \\notin \\mathbb{N}$.",
               "es_resultado": False},
              {"accion_md": "**(b)** Si $U = \\mathbb{Z}$, ambos pertenecen a $U$. Por tanto $A = \\{-2, 2\\}$.",
               "justificacion_md": "El universo determina qué soluciones se admiten.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Subconjunto e inclusión",
          body_md=(
              "$A$ es **subconjunto** de $B$, denotado $A \\subseteq B$, si todo "
              "elemento de $A$ también es elemento de $B$:\n"
              "$$A \\subseteq B \\iff (\\forall x,\\; x \\in A \\Rightarrow x \\in B).$$\n"
              "**Propiedades importantes:**\n\n"
              "1. $\\varnothing \\subseteq A \\subseteq U$ para todo conjunto $A$.\n"
              "2. $A \\subseteq A$ (reflexividad).\n"
              "3. $(A \\subseteq B) \\wedge (B \\subseteq C) \\Rightarrow A \\subseteq C$ (transitividad).\n"
              "4. $A = B \\iff (A \\subseteq B \\wedge B \\subseteq A)$ (técnica de **doble inclusión**).\n\n"
              "**Cuidado:** $\\in$ y $\\subseteq$ son distintos. Para cualquier $a \\in A$ se cumple $\\{a\\} \\subseteq A$."
          )),

        b("definicion",
          titulo="Operaciones entre conjuntos",
          body_md=(
              "Dados $A, B \\subseteq U$, definimos:\n\n"
              "$$A \\cup B = \\{x \\in U \\mid x \\in A \\;\\vee\\; x \\in B\\} \\quad\\text{(unión)}$$\n"
              "$$A \\cap B = \\{x \\in U \\mid x \\in A \\;\\wedge\\; x \\in B\\} \\quad\\text{(intersección)}$$\n"
              "$$A - B = \\{x \\in A \\mid x \\notin B\\} \\quad\\text{(diferencia)}$$\n"
              "$$A^c = \\{x \\in U \\mid x \\notin A\\} \\quad\\text{(complemento)}$$\n"
              "Se cumple además que $A^c = U - A$ y $A - B = A \\cap B^c$.\n\n"
              "Los conectivos $\\wedge$ y $\\vee$ aparecen aquí explícitamente: las "
              "operaciones de conjuntos son la traducción de los conectivos lógicos "
              "al lenguaje de pertenencia."
          )),

        fig(
            "Cuatro diagramas de Venn pequeños en una grilla 2x2, todos con un rectángulo exterior etiquetado U y dos óvalos A y B parcialmente solapados. "
            "(1) Unión A∪B: ambos óvalos completos sombreados en teal claro. "
            "(2) Intersección A∩B: solo la zona de solape en teal oscuro. "
            "(3) Diferencia A−B: solo el creciente de A que no toca B en ámbar. "
            "(4) Complemento A^c: el rectángulo U menos el óvalo A en gris claro. "
            "Etiquetas debajo de cada diagrama. " + STYLE
        ),

        b("teorema",
          enunciado_md=(
              "**Propiedades algebraicas.** Para conjuntos $A, B, C \\subseteq U$:\n\n"
              "1. **Idempotencia:** $A \\cap A = A$, $\\;\\;A \\cup A = A$.\n\n"
              "2. **Neutro y absorbente:** $A \\cup \\varnothing = A$, $\\;\\;A \\cap \\varnothing = \\varnothing$, $\\;\\;A \\cup U = U$, $\\;\\;A \\cap U = A$.\n\n"
              "3. **Conmutatividad y asociatividad** análogas a las de $\\wedge, \\vee$.\n\n"
              "4. **Distributividad:** $A \\cap (B \\cup C) = (A \\cap B) \\cup (A \\cap C)$ y simétrica.\n\n"
              "5. **Leyes de De Morgan:** $(A \\cup B)^c = A^c \\cap B^c$ y $(A \\cap B)^c = A^c \\cup B^c$.\n\n"
              "6. **Doble complemento:** $(A^c)^c = A$.\n\n"
              "7. **Complemento y universo:** $A \\cap A^c = \\varnothing$, $\\;\\;A \\cup A^c = U$."
          )),

        b("ejemplo_resuelto",
          titulo="Demostración por álgebra de conjuntos",
          problema_md=(
              "Demuestre que para conjuntos arbitrarios $A$ y $B$:\n"
              "$$A - B = (A \\cup B) - B.$$"
          ),
          pasos=[
              {"accion_md": (
                  "Partimos del lado derecho usando $X - Y = X \\cap Y^c$:\n"
                  "$$(A \\cup B) - B = (A \\cup B) \\cap B^c.$$"
               ),
               "justificacion_md": "Definición de diferencia en términos de complemento.",
               "es_resultado": False},
              {"accion_md": (
                  "Por distributividad de $\\cap$ sobre $\\cup$:\n"
                  "$$= (A \\cap B^c) \\cup (B \\cap B^c).$$"
               ),
               "justificacion_md": "Distributividad.",
               "es_resultado": False},
              {"accion_md": (
                  "Como $B \\cap B^c = \\varnothing$:\n"
                  "$$= (A \\cap B^c) \\cup \\varnothing = A \\cap B^c = A - B.$$\n"
                  "$\\blacksquare$"
               ),
               "justificacion_md": "Propiedad del complemento y del neutro de la unión.",
               "es_resultado": True},
          ]),

        ej(
            "Igualdad de conjuntos con álgebra",
            ("Demuestre, usando solo álgebra de conjuntos, que para conjuntos "
             "arbitrarios $A$ y $B$:\n\n"
             "$$(A \\cap B) \\cup (A - B) = A.$$"),
            ["Recordá que $A - B = A \\cap B^c$.",
             "Aplicá distributividad de $\\cap$ sobre $\\cup$ en sentido inverso para factorizar $A$.",
             "Usá $B \\cup B^c = U$ y $A \\cap U = A$."],
            ("$(A \\cap B) \\cup (A - B) = (A \\cap B) \\cup (A \\cap B^c)$ por definición "
             "de diferencia. Factorizamos $A$ por distributividad: "
             "$= A \\cap (B \\cup B^c) = A \\cap U = A$. $\\blacksquare$")
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\in$ y $\\subseteq$.** $a \\in A$ significa que $a$ es elemento; $\\{a\\} \\subseteq A$ significa que el conjunto $\\{a\\}$ está contenido.",
              "**Olvidar el conjunto universo al complementar.** $A^c$ depende del $U$ que se haya fijado.",
              "**Asumir que $A - B = B - A$.** La diferencia **no** es conmutativa.",
              "**Aplicar mal De Morgan.** $(A \\cup B)^c = A^c \\cap B^c$, no $A^c \\cup B^c$.",
          ]),

        b("resumen",
          puntos_md=[
              "Un conjunto se define por extensión o comprensión; la igualdad se demuestra por **doble inclusión** o por álgebra.",
              "Las cuatro operaciones $\\cup, \\cap, -, ^c$ corresponden a $\\vee, \\wedge, \\wedge\\overline{(\\cdot)}, \\overline{(\\cdot)}$.",
              "El **álgebra de conjuntos** comparte estructura con la lógica: distributividad, De Morgan y absorción.",
              "Próxima lección: cuantificadores $\\forall$ y $\\exists$ para hacer afirmaciones sobre todos o algunos elementos de un conjunto.",
          ]),
    ]
    return {
        "id": "lec-ia-1-5-conjuntos",
        "title": "Conjuntos y Operaciones",
        "description": "Pertenencia, inclusión, operaciones básicas y álgebra de conjuntos.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 5,
    }


# ============================================================================
# 1.6 Cuantificadores
# ============================================================================
def lesson_1_6():
    blocks = [
        b("texto", body_md=(
            "Los **cuantificadores** son herramientas fundamentales del lenguaje "
            "matemático que permiten expresar con precisión la **generalidad** o la "
            "**existencia** de elementos que satisfacen una propiedad. Gracias a "
            "ellos podemos distinguir afirmaciones tan distintas como «**todo** "
            "número real tiene inverso aditivo» y «**existe** algún número real "
            "que es su propio inverso aditivo».\n\n"
            "Esta lección cubre:\n\n"
            "- **Funciones proposicionales** (predicados con variables libres).\n"
            "- Cuantificador **universal** ($\\forall$), **existencial** ($\\exists$) y de **unicidad** ($\\exists !$).\n"
            "- Cómo el **orden** de los cuantificadores afecta el valor de verdad.\n"
            "- Cómo **negar** proposiciones cuantificadas, incluso anidadas."
        )),

        b("definicion",
          titulo="Función proposicional",
          body_md=(
              "Una **función proposicional** $p(x)$ es una expresión que depende de "
              "una variable $x$ que, al ser reemplazada por elementos de un conjunto "
              "**referencial** $U$, se transforma en una proposición (verdadera o "
              "falsa).\n\n"
              "Más generalmente, $p(x, y)$, $p(x, y, z)$, etc., dependen de varias "
              "variables y se evalúan sobre los respectivos conjuntos referenciales.\n\n"
              "**Ejemplo:** $p(x): x - 5 \\le 0$ sobre $\\mathbb{Z}$. Entonces "
              "$p(3) \\iff 3 - 5 \\le 0$ es verdadera, mientras que "
              "$p(7) \\iff 7 - 5 \\le 0$ es falsa."
          )),

        b("definicion",
          titulo="Cuantificadores lógicos",
          body_md=(
              "Dada $p(x)$ con dominio $U$ y el conjunto $A = \\{x \\in U \\mid p(x)\\}$ "
              "donde $p$ es verdadera, definimos:\n\n"
              "- **Universal** $(\\forall x \\in U)\\, p(x) \\iff (A = U)$. Se lee «**para "
              "todo** $x$ en $U$, $p(x)$».\n\n"
              "- **Existencial** $(\\exists x \\in U)\\, p(x) \\iff (A \\neq \\varnothing)$. Se "
              "lee «**existe** (al menos un) $x$ en $U$ tal que $p(x)$».\n\n"
              "- **Unicidad** $(\\exists ! x \\in U)\\, p(x) \\iff |A| = 1$. Se lee «**existe "
              "un único** $x$ en $U$ tal que $p(x)$»."
          )),

        b("intuicion", body_md=(
            "**Estrategia para demostrar/refutar:**\n\n"
            "- Para refutar $(\\forall x)\\, p(x)$ basta exhibir **un solo "
            "contraejemplo**: un $x$ donde $p(x)$ es falsa.\n"
            "- Para demostrar $(\\exists x)\\, p(x)$ basta exhibir **un solo testigo**: "
            "un $x$ concreto donde $p(x)$ es verdadera (demostración **constructiva**).\n"
            "- Para demostrar $(\\forall x)\\, p(x)$ se toma un $x$ **arbitrario** del "
            "dominio y se prueba $p(x)$ sin suponer nada adicional."
        )),

        b("ejemplo_resuelto",
          titulo="Evaluación de cuantificadores",
          problema_md=(
              "Determine el valor de verdad de cada proposición:\n\n"
              "1. $(\\exists x \\in \\mathbb{N})(x \\text{ es divisible por } 2)$\n"
              "2. $(\\forall x \\in \\mathbb{N})(x \\text{ es divisible por } 2)$\n"
              "3. $(\\forall x \\in \\mathbb{R})(x^2 + x = 0)$\n"
              "4. $(\\exists x \\in \\mathbb{R})(x^2 + x = 0)$\n"
              "5. $(\\exists ! x \\in \\mathbb{R})(x^2 + x = 0)$"
          ),
          pasos=[
              {"accion_md": "**(1)** Verdadera: $2 \\in \\mathbb{N}$ es divisible por $2$.",
               "justificacion_md": "Exhibimos un testigo.",
               "es_resultado": False},
              {"accion_md": "**(2)** Falsa: $1 \\in \\mathbb{N}$ no es divisible por $2$ (contraejemplo).",
               "justificacion_md": "Un contraejemplo refuta una afirmación universal.",
               "es_resultado": False},
              {"accion_md": "**(3)** Falsa: $x = 1$ da $1 + 1 = 2 \\neq 0$.",
               "justificacion_md": "Contraejemplo.",
               "es_resultado": False},
              {"accion_md": (
                  "**(4)** Verdadera: $x^2 + x = x(x+1) = 0$ tiene soluciones $x = 0$ y $x = -1$, "
                  "ambas en $\\mathbb{R}$."
               ),
               "justificacion_md": "Existen testigos.",
               "es_resultado": False},
              {"accion_md": "**(5)** Falsa: hay **dos** soluciones reales, no una sola.",
               "justificacion_md": "La unicidad falla cuando hay más de un elemento.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Orden de cuantificadores.** Sea $p(x, y)$ una función proposicional "
              "sobre $U$. Se cumple:\n\n"
              "1. $(\\forall x)(\\forall y)\\, p(x,y) \\iff (\\forall y)(\\forall x)\\, p(x,y)$.\n\n"
              "2. $(\\exists x)(\\exists y)\\, p(x,y) \\iff (\\exists y)(\\exists x)\\, p(x,y)$.\n\n"
              "3. $(\\exists x)(\\forall y)\\, p(x,y) \\;\\Longrightarrow\\; (\\forall y)(\\exists x)\\, p(x,y)$.\n\n"
              "**Cuantificadores del mismo tipo conmutan**; mezclados, no en general. "
              "El recíproco de (3) **falla**: la versión con $\\exists$ afuera es más fuerte."
          )),

        b("ejemplo_resuelto",
          titulo="El orden importa: inverso aditivo en $\\mathbb{R}$",
          problema_md=(
              "Determine el valor de verdad de:\n\n"
              "(a) $(\\forall x \\in \\mathbb{R})(\\exists y \\in \\mathbb{R})(x + y = 0)$.\n\n"
              "(b) $(\\exists y \\in \\mathbb{R})(\\forall x \\in \\mathbb{R})(x + y = 0)$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Es **verdadera**: para cada $x$ basta tomar $y = -x$, "
                  "que cumple $x + (-x) = 0$. Esta es la versión simbólica del "
                  "axioma de inverso aditivo en $\\mathbb{R}$."
               ),
               "justificacion_md": "Construcción explícita del testigo $y$ en función de $x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Es **falsa**: afirma que existe **un único** $y$ que "
                  "funciona como inverso aditivo para **todos** los reales. Si "
                  "existiera tal $y$, debería cumplir $0 + y = 0$ (tomando $x = 0$) "
                  "y también $1 + y = 0$ (tomando $x = 1$), forzando $y = 0$ y $y = -1$ "
                  "simultáneamente. Contradicción."
               ),
               "justificacion_md": "Mostramos que ningún $y$ puede cumplir todas las condiciones.",
               "es_resultado": False},
              {"accion_md": (
                  "**Moraleja:** intercambiar $\\forall$ y $\\exists$ cambia "
                  "radicalmente el significado. En (a), $y$ depende de $x$; en (b), "
                  "se pide un $y$ independiente de $x$."
               ),
               "justificacion_md": "El orden codifica la dependencia entre variables.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Negación de cuantificadores.** Sea $p(x)$ una función "
              "proposicional con dominio $U$. Se cumplen las equivalencias:\n\n"
              "$$\\overline{(\\forall x \\in U)\\, p(x)} \\;\\equiv\\; (\\exists x \\in U)\\, \\overline{p(x)},$$\n"
              "$$\\overline{(\\exists x \\in U)\\, p(x)} \\;\\equiv\\; (\\forall x \\in U)\\, \\overline{p(x)}.$$\n\n"
              "*Regla:* la negación «empuja hacia adentro» cambiando cada "
              "cuantificador por el opuesto y negando la función al final."
          )),

        b("ejemplo_resuelto",
          titulo="Negación de un enunciado con cuantificadores anidados",
          problema_md=(
              "Construya y simplifique la negación de:\n"
              "$$(\\forall x \\in \\mathbb{R})(\\forall y \\in \\mathbb{R})(\\exists z \\in \\mathbb{R})\\;(x < z < y).$$"
          ),
          pasos=[
              {"accion_md": (
                  "Aplicamos la regla de negación de afuera hacia adentro: "
                  "$$\\overline{(\\forall x)(\\forall y)(\\exists z)\\,(x<z<y)} "
                  "\\equiv (\\exists x)(\\exists y)(\\forall z)\\,\\overline{(x<z<y)}.$$"
               ),
               "justificacion_md": "Cada cuantificador cambia y al final se niega la función.",
               "es_resultado": False},
              {"accion_md": (
                  "Simplificamos $\\overline{(x < z < y)} \\equiv \\overline{(x<z) \\wedge (z<y)}$. "
                  "Por De Morgan: $\\equiv \\overline{(x<z)} \\vee \\overline{(z<y)} \\equiv (x \\ge z) \\vee (z \\ge y)$."
               ),
               "justificacion_md": "Negación de una conjunción más negación de cada desigualdad.",
               "es_resultado": False},
              {"accion_md": (
                  "La negación queda: "
                  "$$(\\exists x \\in \\mathbb{R})(\\exists y \\in \\mathbb{R})(\\forall z \\in \\mathbb{R})\\;\\bigl[(x \\ge z) \\vee (z \\ge y)\\bigr].$$\n"
                  "**Lectura:** existen reales $x$ e $y$ tales que para todo real $z$, "
                  "$z \\le x$ o $z \\ge y$. $\\blacksquare$"
               ),
               "justificacion_md": "Forma simplificada y traducción al lenguaje natural.",
               "es_resultado": True},
          ]),

        ej(
            "Demostración con cuantificador universal",
            ("Demuestre que **para todo** $x \\in \\mathbb{R} \\setminus \\{0\\}$ "
             "se cumple $x^2 > 0$."),
            ["Empezá: «sea $x \\in \\mathbb{R} \\setminus \\{0\\}$ arbitrario».",
             "Como $x \\neq 0$, separá en dos casos: $x > 0$ y $x < 0$.",
             "Recordá que producto de dos negativos es positivo."],
            ("Sea $x \\in \\mathbb{R} \\setminus \\{0\\}$ arbitrario. Como $x \\neq 0$, "
             "hay dos casos:\n\n"
             "**Caso 1:** $x > 0$. Entonces $x^2 = x \\cdot x > 0$ (producto de positivos).\n\n"
             "**Caso 2:** $x < 0$. Entonces $-x > 0$ y $x^2 = (-x)(-x) > 0$ (producto de positivos).\n\n"
             "En ambos casos $x^2 > 0$. Como $x$ era arbitrario, se cumple para "
             "todo $x \\in \\mathbb{R} \\setminus \\{0\\}$. $\\blacksquare$")
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el dominio del cuantificador.** $(\\forall x)\\, p(x)$ sin especificar $U$ es ambiguo.",
              "**Cambiar el orden de cuantificadores mixtos.** $(\\forall x)(\\exists y)$ ≠ $(\\exists y)(\\forall x)$.",
              "**Negar mal:** la negación de $(\\forall x)\\, p(x)$ es $(\\exists x)\\, \\overline{p(x)}$, no $(\\forall x)\\, \\overline{p(x)}$.",
              "**Suponer un valor particular al probar $\\forall$.** El elemento debe ser **arbitrario**: nada extra puede asumirse sobre él.",
          ]),

        b("resumen",
          puntos_md=[
              "Una **función proposicional** $p(x)$ se vuelve proposición al fijar $x$ o al cuantificarla.",
              "$\\forall$ exige todos los casos; $\\exists$ basta un caso; $\\exists !$ exige exactamente uno.",
              "**Negación:** $\\forall \\leftrightarrow \\exists$ y se niega la función al final.",
              "**Cierre del capítulo:** ya tenés todo el lenguaje matemático básico — proposiciones, leyes lógicas, inferencia, demostración, conjuntos y cuantificadores. Próximo capítulo: usar este lenguaje para demostrar propiedades sobre **números naturales** mediante **inducción**.",
          ]),
    ]
    return {
        "id": "lec-ia-1-6-cuantificadores",
        "title": "Cuantificadores",
        "description": "Universal, existencial y unicidad. Orden y negación de cuantificadores.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


# ============================================================================
# MAIN — patrón idempotente
# ============================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    course_doc = {
        "id": COURSE_ID,
        "title": COURSE_TITLE,
        "description": COURSE_DESCRIPTION,
        "category": COURSE_CATEGORY,
        "level": COURSE_LEVEL,
        "modules_count": COURSE_MODULES_COUNT,
        "rating": 4.8,
        "summary": COURSE_DESCRIPTION,
        "created_at": now(),
        "visible_to_students": True,
    }
    existing = await db.courses.find_one({"id": COURSE_ID})
    if existing:
        update_fields = {k: v for k, v in course_doc.items() if k != "created_at"}
        await db.courses.update_one({"id": COURSE_ID}, {"$set": update_fields})
        print(f"✓ Curso actualizado: {COURSE_TITLE}")
    else:
        await db.courses.insert_one(course_doc)
        print(f"✓ Curso creado: {COURSE_TITLE}")

    await db.chapters.delete_one({"id": CHAPTER_ID})
    chapter = {
        "id": CHAPTER_ID,
        "course_id": COURSE_ID,
        "title": CHAPTER_TITLE,
        "description": CHAPTER_DESCRIPTION,
        "order": CHAPTER_ORDER,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {CHAPTER_TITLE}")

    builders = [lesson_1_1, lesson_1_2, lesson_1_3, lesson_1_4, lesson_1_5, lesson_1_6]

    total_blocks = 0
    total_figs = 0
    for build in builders:
        data = build()
        await db.lessons.delete_one({"id": data["id"]})
        lesson = {
            "id": data["id"],
            "chapter_id": CHAPTER_ID,
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
    print(f"✅ {CHAPTER_TITLE}: {len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes.")
    print()
    print("URLs locales para verificar:")
    print(f"  http://localhost:3007/courses/{COURSE_ID}")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
