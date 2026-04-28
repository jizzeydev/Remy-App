"""
Seed del curso Precálculo — Capítulo 7: Números Complejos.

Crea el capítulo 'Números Complejos' bajo el curso 'precalculo'
y siembra sus 4 lecciones:

  - Definición y forma estándar
  - Operaciones con complejos
  - Forma polar y exponencial
  - Teorema de De Moivre y raíces

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
# Definición y forma estándar
# =====================================================================
def lesson_definicion_complejos():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora, ecuaciones como $x^2 + 1 = 0$ no tenían solución en los reales: $x^2 = -1$ "
            "**no tiene solución** en $\\mathbb{R}$ porque ningún real al cuadrado es negativo.\n\n"
            "Los **números complejos** $\\mathbb{C}$ extienden los reales **agregando una nueva 'unidad imaginaria' $i$** que cumple la propiedad esencial:\n\n"
            "$$\\boxed{\\,i^2 = -1.\\,}$$\n\n"
            "Con esta sola adición se vuelve posible resolver toda ecuación polinomial — ese es el contenido del **teorema fundamental del álgebra** que vimos en el Cap. 3. \n\n"
            "**Aplicaciones del mundo real:**\n\n"
            "- **Electricidad alterna:** voltajes y corrientes se representan con complejos (impedancia).\n"
            "- **Procesamiento de señales:** transformada de Fourier.\n"
            "- **Mecánica cuántica:** estados cuánticos son vectores complejos.\n"
            "- **Cálculo:** integración por residuos, soluciones de EDOs lineales.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces la **forma estándar** $z = a + bi$ y sus partes real e imaginaria.\n"
            "- Representás complejos como puntos en el **plano complejo** (de Gauss).\n"
            "- Identificás casos especiales: reales puros e imaginarios puros."
        )),

        b("definicion",
          titulo="Número complejo",
          body_md=(
              "Un **número complejo** es una expresión\n\n"
              "$$z = a + b i,$$\n\n"
              "donde $a, b \\in \\mathbb{R}$ y $i$ es la **unidad imaginaria** que satisface $i^2 = -1$.\n\n"
              "- $a = \\operatorname{Re}(z)$ se llama **parte real** de $z$.\n"
              "- $b = \\operatorname{Im}(z)$ se llama **parte imaginaria** de $z$.\n\n"
              "**Cuidado:** la parte imaginaria es el **número** $b$, no $b i$. Es un real.\n\n"
              "El conjunto de todos los complejos se denota $\\mathbb{C} = \\{a + b i : a, b \\in \\mathbb{R}\\}$.\n\n"
              "**Igualdad de complejos:** $z_1 = z_2$ si y solo si $\\operatorname{Re}(z_1) = \\operatorname{Re}(z_2)$ y $\\operatorname{Im}(z_1) = \\operatorname{Im}(z_2)$ (ambas componentes).\n\n"
              "**Casos especiales:**\n\n"
              "- Si $b = 0$: $z = a$ es un **real puro** (los reales son un subconjunto de los complejos).\n"
              "- Si $a = 0$: $z = b i$ es un **imaginario puro**.\n"
              "- Si $a = 0$ y $b = 0$: $z = 0$."
          )),

        formulas(
            titulo="Potencias de $i$",
            body=(
                "La unidad imaginaria tiene un patrón **periódico de período 4** en sus potencias:\n\n"
                "$$i^1 = i, \\quad i^2 = -1, \\quad i^3 = -i, \\quad i^4 = 1.$$\n\n"
                "Después se repite: $i^5 = i, i^6 = -1, \\ldots$\n\n"
                "**Para calcular $i^n$ con $n$ grande:**\n\n"
                "1. Dividir $n$ entre 4 y obtener el resto $r$.\n"
                "2. $i^n = i^r$.\n\n"
                "**Ejemplo.** $i^{27}$: $27 = 4 \\cdot 6 + 3$, así $i^{27} = i^3 = -i$."
            ),
        ),

        b("definicion",
          titulo="Plano complejo (de Gauss)",
          body_md=(
              "Como un complejo $z = a + b i$ está caracterizado por **dos números reales** $(a, b)$, "
              "podemos representarlo como un **punto en el plano cartesiano**:\n\n"
              "- **Eje horizontal** = eje real (donde van los reales puros).\n"
              "- **Eje vertical** = eje imaginario (donde van los imaginarios puros).\n\n"
              "Esta representación se llama **plano complejo** o **plano de Argand-Gauss**.\n\n"
              "**Ejemplos en el plano:**\n\n"
              "- $z = 3 + 4 i \\to (3, 4)$.\n"
              "- $z = -2 + i \\to (-2, 1)$.\n"
              "- $z = -3 i \\to (0, -3)$.\n"
              "- $z = 5 \\to (5, 0)$.\n\n"
              "**Beneficio.** Las operaciones con complejos tienen **interpretación geométrica clara** en este plano (lo veremos en las próximas lecciones)."
          )),

        b("ejemplo_resuelto",
          titulo="Identificar partes",
          problema_md="Para cada complejo, identifica $\\operatorname{Re}(z)$, $\\operatorname{Im}(z)$ y su ubicación en el plano: **(a)** $z = 3 + 4 i$, **(b)** $z = -2 + 2 i$, **(c)** $z = 5$, **(d)** $z = 3 i$.",
          pasos=[
              {"accion_md": (
                  "**(a)** $z = 3 + 4 i$: $\\operatorname{Re} = 3$, $\\operatorname{Im} = 4$, punto $(3, 4)$ en el plano. **Cuadrante I.**\n\n"
                  "**(b)** $z = -2 + 2 i$: $\\operatorname{Re} = -2$, $\\operatorname{Im} = 2$, punto $(-2, 2)$. **Cuadrante II.**"
              ),
               "justificacion_md": "Lectura directa del coeficiente.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** $z = 5$: $\\operatorname{Re} = 5$, $\\operatorname{Im} = 0$, punto $(5, 0)$. **Real puro** (sobre eje real).\n\n"
                  "**(d)** $z = 3 i$: $\\operatorname{Re} = 0$, $\\operatorname{Im} = 3$, punto $(0, 3)$. **Imaginario puro** (sobre eje imaginario)."
              ),
               "justificacion_md": "Casos especiales con una parte nula.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Resolver ecuación con complejos",
          problema_md="Resuelve $x^2 + 9 = 0$ en $\\mathbb{C}$.",
          pasos=[
              {"accion_md": (
                  "**Despejar:** $x^2 = -9$. Tomar raíz cuadrada: $x = \\pm \\sqrt{-9} = \\pm \\sqrt{9} \\sqrt{-1} = \\pm 3 i$."
              ),
               "justificacion_md": "$\\sqrt{-1} = i$ por definición.",
               "es_resultado": False},
              {"accion_md": (
                  "**Soluciones:** $x = 3 i$ y $x = -3 i$ (dos imaginarios puros conjugados).\n\n"
                  "**Verificación:** $(3 i)^2 = 9 i^2 = -9 \\Rightarrow x^2 + 9 = 0$ ✓."
              ),
               "justificacion_md": "Ahora la ecuación tiene solución que antes no tenía.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué se necesita $i$.** Sin $i$, ecuaciones tan simples como $x^2 + 1 = 0$ quedan sin "
            "solución. Con $i$ definido por $i^2 = -1$, **toda ecuación polinomial de grado $n$ tiene "
            "exactamente $n$ raíces complejas** (TFA). Es la 'completación' algebraica natural de los reales.\n\n"
            "**$i$ no es 'imaginario' en el sentido coloquial.** El nombre es histórico (Descartes lo "
            "llamó 'imaginario' como insulto). Hoy en día los complejos son **tan reales** como los reales, "
            "con aplicaciones físicas concretas. Por ejemplo, en mecánica cuántica los estados son **vectores complejos**, no reales.\n\n"
            "**Plano complejo y geometría.** Pensar un complejo como un **punto** en el plano hace que las "
            "operaciones tengan **sentido geométrico**: la suma es vectorial, la multiplicación es rotación + "
            "estiramiento (próxima lección)."
        )),

        fig(
            "Plano complejo (de Argand-Gauss). "
            "Eje horizontal etiquetado 'eje real (Re)', eje vertical 'eje imaginario (Im)'. "
            "Cuatro puntos destacados con sus coordenadas: (3, 4) en cuadrante I (color teal #06b6d4) etiquetado 'z = 3 + 4i'; "
            "(-2, 2) en cuadrante II (ámbar #f59e0b) etiquetado 'z = -2 + 2i'; "
            "(5, 0) sobre eje real etiquetado 'z = 5 (real puro)'; "
            "(0, 3) sobre eje imaginario etiquetado 'z = 3i (imaginario puro)'. "
            "Cuadrícula tenue, marcas en valores enteros de -3 a 5 en ambos ejes. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\operatorname{Im}(2 - 7 i) = $",
                  "opciones_md": [
                      "$2$",
                      "**$-7$**",
                      "$-7 i$",
                      "$7$",
                  ],
                  "correcta": "B",
                  "pista_md": "Parte imaginaria es el coeficiente de $i$, sin el $i$.",
                  "explicacion_md": "Es el real $-7$.",
              },
              {
                  "enunciado_md": "$i^2 = $",
                  "opciones_md": [
                      "$1$",
                      "**$-1$**",
                      "$i$",
                      "$0$",
                  ],
                  "correcta": "B",
                  "pista_md": "Definición fundamental.",
                  "explicacion_md": "Esa es la propiedad que define $i$.",
              },
              {
                  "enunciado_md": "$i^{10} = $",
                  "opciones_md": [
                      "$i$",
                      "**$-1$**",
                      "$-i$",
                      "$1$",
                  ],
                  "correcta": "B",
                  "pista_md": "$10 = 4 \\cdot 2 + 2$, así $i^{10} = i^2$.",
                  "explicacion_md": "Patrón cíclico de período 4.",
              },
          ]),

        ej(
            "Identificar partes",
            "Para $z = -1 + \\sqrt{3} i$, halla $\\operatorname{Re}(z)$, $\\operatorname{Im}(z)$ y ubicalo en el plano.",
            ["Lectura directa."],
            (
                "$\\operatorname{Re}(z) = -1$, $\\operatorname{Im}(z) = \\sqrt{3}$, punto $(-1, \\sqrt 3) \\approx (-1, 1{,}73)$ en cuadrante II."
            ),
        ),

        ej(
            "Potencia alta de $i$",
            "Calcula $i^{2027}$.",
            ["Dividir 2027 entre 4."],
            (
                "$2027 = 4 \\cdot 506 + 3$, así $i^{2027} = i^3 = -i$."
            ),
        ),

        ej(
            "Resolver ecuación",
            "Resuelve $x^2 + 25 = 0$ en $\\mathbb{C}$.",
            ["$x^2 = -25$."],
            (
                "$x = \\pm \\sqrt{-25} = \\pm 5 i$. Soluciones: $5 i$ y $-5 i$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir 'parte imaginaria' con $b i$.** La parte imaginaria es el **real $b$**, no la expresión $b i$.",
              "**Olvidar $i^2 = -1$** al elevar al cuadrado un imaginario.",
              "**Pensar que los reales no son complejos.** Todo real es complejo (con parte imaginaria 0).",
              "**Calcular $i^n$ sin el truco del módulo 4.** Hacerlo a mano es tedioso e propenso a errores.",
              "**Dividir mal una raíz de número negativo:** $\\sqrt{-9} \\neq -3$. Es $3 i$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Número complejo:** $z = a + b i$ con $a, b \\in \\mathbb{R}$ y $i^2 = -1$.",
              "**Parte real** $a$ y **parte imaginaria** $b$ (ambas son números reales).",
              "**Plano complejo:** $z \\to (a, b)$. Eje horizontal real, vertical imaginario.",
              "**Casos especiales:** real puro ($b = 0$), imaginario puro ($a = 0$).",
              "**Potencias de $i$:** $i, -1, -i, 1$ se repiten con período 4.",
              "**Próxima lección:** operaciones — suma, resta, producto y cociente.",
          ]),
    ]
    return {
        "id": "lec-prec-7-1-definicion-complejos",
        "title": "Definición y forma estándar",
        "description": "Número complejo z = a + bi: definición, parte real e imaginaria, unidad imaginaria con i² = -1. Potencias cíclicas de i. Plano complejo (de Argand-Gauss) y representación gráfica.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 1,
    }


# =====================================================================
# Operaciones con números complejos
# =====================================================================
def lesson_operaciones_complejos():
    blocks = [
        b("texto", body_md=(
            "Para que los complejos sean realmente útiles, hay que poder **operar** con ellos: sumar, "
            "restar, multiplicar y dividir. Las reglas son **naturales**: tratar $i$ como una variable "
            "ordinaria y aplicar $i^2 = -1$ cuando aparezca.\n\n"
            "Además aparecen dos conceptos nuevos importantes:\n\n"
            "- El **conjugado** $\\bar z$, que invierte el signo de la parte imaginaria.\n"
            "- El **módulo** $|z|$, que mide la distancia al origen del plano complejo.\n\n"
            "**Al terminar:**\n\n"
            "- Sumás, restás, multiplicás y dividís complejos en forma estándar.\n"
            "- Calculás el **conjugado** y el **módulo** y conoces sus propiedades.\n"
            "- Aplicás el **truco del conjugado** para racionalizar cocientes."
        )),

        b("definicion",
          titulo="Conjugado y módulo",
          body_md=(
              "Sea $z = a + b i$. Definimos:\n\n"
              "**Conjugado:**\n\n"
              "$$\\bar z = a - b i \\quad (\\text{cambiar signo de la parte imaginaria}).$$\n\n"
              "**Módulo:**\n\n"
              "$$|z| = \\sqrt{a^2 + b^2} \\quad (\\text{distancia al origen en el plano complejo}).$$\n\n"
              "**Propiedades clave:**\n\n"
              "- $\\bar{\\bar z} = z$ (involutivo).\n"
              "- $z + \\bar z = 2 a = 2 \\operatorname{Re}(z)$.\n"
              "- $z - \\bar z = 2 b i = 2 i \\operatorname{Im}(z)$.\n"
              "- $z \\cdot \\bar z = a^2 + b^2 = |z|^2$ (¡real positivo!).\n"
              "- $\\overline{z_1 + z_2} = \\bar{z_1} + \\bar{z_2}$.\n"
              "- $\\overline{z_1 \\cdot z_2} = \\bar{z_1} \\cdot \\bar{z_2}$.\n"
              "- $|z| = 0 \\Leftrightarrow z = 0$.\n"
              "- $|z_1 z_2| = |z_1| |z_2|$.\n\n"
              "**Geometría.** En el plano, $\\bar z$ es el **reflejo** de $z$ respecto al eje real. $|z|$ es la **longitud del segmento** desde el origen hasta $z$."
          )),

        formulas(
            titulo="Suma y resta",
            body=(
                "Operar componente a componente:\n\n"
                "$$\\boxed{(a_1 + b_1 i) + (a_2 + b_2 i) = (a_1 + a_2) + (b_1 + b_2) i.}$$\n\n"
                "$$(a_1 + b_1 i) - (a_2 + b_2 i) = (a_1 - a_2) + (b_1 - b_2) i.$$\n\n"
                "**Geometría.** Sumar complejos es **sumar vectores** en el plano (ley del paralelogramo)."
            ),
        ),

        formulas(
            titulo="Multiplicación",
            body=(
                "Aplicar distributividad y reemplazar $i^2 = -1$ cuando aparezca:\n\n"
                "$$(a_1 + b_1 i)(a_2 + b_2 i) = a_1 a_2 + a_1 b_2 i + b_1 a_2 i + b_1 b_2 i^2.$$\n\n"
                "Como $i^2 = -1$:\n\n"
                "$$\\boxed{(a_1 + b_1 i)(a_2 + b_2 i) = (a_1 a_2 - b_1 b_2) + (a_1 b_2 + b_1 a_2) i.}$$\n\n"
                "**No memorizar la fórmula final** — basta con aplicar distributiva con cuidado."
            ),
        ),

        formulas(
            titulo="División (truco del conjugado)",
            body=(
                "Para dividir $z_1 / z_2$, **multiplicar arriba y abajo por el conjugado del denominador**:\n\n"
                "$$\\dfrac{z_1}{z_2} = \\dfrac{z_1 \\cdot \\bar{z_2}}{z_2 \\cdot \\bar{z_2}} = \\dfrac{z_1 \\cdot \\bar{z_2}}{|z_2|^2}.$$\n\n"
                "El denominador se vuelve **real positivo** $|z_2|^2$, así la división se reduce a:\n\n"
                "1. Multiplicar el numerador por $\\bar{z_2}$ (operación entre complejos).\n"
                "2. Dividir cada componente por el real $|z_2|^2$.\n\n"
                "**Análogo a racionalizar** $\\dfrac{1}{a + b\\sqrt{c}}$ multiplicando por el conjugado $a - b\\sqrt{c}$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Operaciones básicas",
          problema_md="Sean $z_1 = 3 + 2 i$ y $z_2 = 1 - i$. Calcula $z_1 + z_2$, $z_1 - z_2$, $z_1 z_2$ y $z_1 / z_2$.",
          pasos=[
              {"accion_md": (
                  "**Suma:** $z_1 + z_2 = (3 + 1) + (2 - 1) i = 4 + i$.\n\n"
                  "**Resta:** $z_1 - z_2 = (3 - 1) + (2 - (-1)) i = 2 + 3 i$."
              ),
               "justificacion_md": "Componente a componente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Producto:** $(3 + 2 i)(1 - i) = 3 - 3 i + 2 i - 2 i^2 = 3 - i + 2 = 5 - i$."
              ),
               "justificacion_md": "Distributiva + $i^2 = -1$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cociente:** $\\dfrac{3 + 2 i}{1 - i} \\cdot \\dfrac{1 + i}{1 + i} = \\dfrac{(3 + 2 i)(1 + i)}{1^2 + 1^2} = \\dfrac{3 + 3 i + 2 i + 2 i^2}{2} = \\dfrac{1 + 5 i}{2} = \\dfrac{1}{2} + \\dfrac{5}{2} i$."
              ),
               "justificacion_md": "Multiplicar arriba y abajo por $\\bar{z_2} = 1 + i$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Conjugado y módulo",
          problema_md="Para $z = 4 - 3 i$, calcula $\\bar z$, $|z|$ y $z \\cdot \\bar z$.",
          pasos=[
              {"accion_md": (
                  "**Conjugado:** $\\bar z = 4 + 3 i$ (cambiar signo de la parte imaginaria)."
              ),
               "justificacion_md": "Reflejo respecto al eje real.",
               "es_resultado": False},
              {"accion_md": (
                  "**Módulo:** $|z| = \\sqrt{4^2 + (-3)^2} = \\sqrt{16 + 9} = \\sqrt{25} = 5$."
              ),
               "justificacion_md": "Distancia euclidiana al origen.",
               "es_resultado": False},
              {"accion_md": (
                  "**Producto $z \\bar z$:** $(4 - 3 i)(4 + 3 i) = 16 + 12 i - 12 i - 9 i^2 = 16 + 9 = 25 = |z|^2$. ✓"
              ),
               "justificacion_md": "Confirma la propiedad $z \\bar z = |z|^2$.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué $z \\bar z = |z|^2$ es tan útil.** Multiplicar un complejo por su conjugado "
            "**elimina la parte imaginaria** y devuelve el cuadrado de su módulo. Es la herramienta clave "
            "para racionalizar cocientes — exactamente como con conjugados de raíces cuadradas en álgebra real.\n\n"
            "**Suma como vectores.** En el plano complejo, $z_1 + z_2$ se obtiene con la ley del "
            "paralelogramo: dibujar los dos vectores y completar el paralelogramo; la diagonal es la suma. "
            "Eso da una intuición geométrica directa.\n\n"
            "**Multiplicación NO es componente a componente.** $z_1 z_2 \\neq (a_1 a_2) + (b_1 b_2) i$. "
            "El producto involucra una **mezcla** de componentes por la propiedad $i^2 = -1$. "
            "Geométricamente, multiplicar es **rotar y escalar** (próxima lección)."
        )),

        fig(
            "Suma de complejos en el plano como suma vectorial. "
            "Vectores z_1 = 3 + 2i (color teal #06b6d4) y z_2 = 1 + 3i (color ámbar #f59e0b) dibujados desde el origen. "
            "El paralelogramo formado por trazos punteados, con la diagonal mayor siendo z_1 + z_2 = 4 + 5i (color púrpura grueso). "
            "Eje real e imaginario marcados, cuadrícula tenue. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$(2 + 3 i) + (1 - 5 i) = $",
                  "opciones_md": [
                      "$3 - 2 i$",
                      "**$3 - 2 i$**",
                      "$1 - 8 i$",
                      "$3 + 2 i$",
                  ],
                  "correcta": "A",
                  "pista_md": "Sumar componente a componente.",
                  "explicacion_md": "$3 + (-2) i = 3 - 2 i$.",
              },
              {
                  "enunciado_md": "$(1 + i)(1 - i) = $",
                  "opciones_md": [
                      "$0$",
                      "**$2$**",
                      "$1$",
                      "$2 i$",
                  ],
                  "correcta": "B",
                  "pista_md": "Producto por conjugado = $|z|^2 = 1 + 1$.",
                  "explicacion_md": "Diferencia de cuadrados: $1 - i^2 = 1 + 1 = 2$.",
              },
              {
                  "enunciado_md": "Para dividir complejos:",
                  "opciones_md": [
                      "Restar arriba y abajo",
                      "**Multiplicar arriba y abajo por el conjugado del denominador**",
                      "Dividir parte real entre parte real",
                      "Tomar inversa del módulo",
                  ],
                  "correcta": "B",
                  "pista_md": "Truco del conjugado.",
                  "explicacion_md": "Vuelve real al denominador.",
              },
          ]),

        ej(
            "Multiplicar",
            "Calcula $(2 - i)(3 + 4 i)$.",
            ["Distributiva."],
            (
                "$(2 - i)(3 + 4 i) = 6 + 8 i - 3 i - 4 i^2 = 6 + 5 i + 4 = 10 + 5 i$."
            ),
        ),

        ej(
            "Dividir",
            "Calcula $\\dfrac{5 + 2 i}{3 - i}$.",
            ["Multiplicar por $\\bar{z_2} = 3 + i$."],
            (
                "$\\dfrac{(5 + 2 i)(3 + i)}{(3 - i)(3 + i)} = \\dfrac{15 + 5 i + 6 i + 2 i^2}{9 + 1} = \\dfrac{13 + 11 i}{10} = \\dfrac{13}{10} + \\dfrac{11}{10} i$."
            ),
        ),

        ej(
            "Módulo y conjugado",
            "Para $z = 1 + 2 i$, calcula $|z|$, $\\bar z$ y verifica que $z \\bar z = |z|^2$.",
            ["Aplicar definiciones."],
            (
                "$|z| = \\sqrt{1 + 4} = \\sqrt 5$. $\\bar z = 1 - 2 i$. $z \\bar z = (1 + 2 i)(1 - 2 i) = 1 - 4 i^2 = 5 = (\\sqrt 5)^2$. ✓"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar $i^2 = -1$** al multiplicar.",
              "**Multiplicar componente a componente:** $(a_1 + b_1 i)(a_2 + b_2 i) \\neq a_1 a_2 + b_1 b_2 i$.",
              "**Dividir multiplicando solo el denominador** por el conjugado. Hay que hacerlo **arriba y abajo**.",
              "**Tomar el módulo como suma de las componentes** en lugar de raíz de suma de cuadrados.",
              "**Olvidar el signo del conjugado:** $\\overline{a + b i} = a - b i$, **no** $-a - b i$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Suma/resta:** componente a componente.",
              "**Multiplicación:** distributiva + $i^2 = -1$.",
              "**División:** multiplicar arriba y abajo por el conjugado del denominador.",
              "**Conjugado** $\\bar z = a - b i$. **Módulo** $|z| = \\sqrt{a^2 + b^2}$.",
              "**Identidad clave:** $z \\bar z = |z|^2$ (real positivo).",
              "**Próxima lección:** otras formas de representar complejos — polar y exponencial.",
          ]),
    ]
    return {
        "id": "lec-prec-7-2-operaciones-complejos",
        "title": "Operaciones con complejos",
        "description": "Suma, resta, producto y cociente de números complejos en forma estándar. Conjugado y módulo. Truco del conjugado para racionalizar cocientes. Propiedades algebraicas y interpretación geométrica.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# Forma polar y exponencial
# =====================================================================
def lesson_forma_polar():
    blocks = [
        b("texto", body_md=(
            "La **forma estándar** $z = a + b i$ es cómoda para sumar y restar, pero **incómoda para "
            "multiplicar y elevar a potencias**. Existen dos representaciones alternativas — la **forma "
            "polar** y la **exponencial** — que **simplifican enormemente** esas operaciones.\n\n"
            "**Idea geométrica.** En el plano complejo, $z$ se puede describir con:\n\n"
            "- Su **distancia al origen** $r = |z|$.\n"
            "- El **ángulo** $\\theta$ que forma con el eje real positivo.\n\n"
            "$$\\boxed{\\,z = r(\\cos \\theta + i \\sin \\theta) = r\\, e^{i \\theta}.\\,}$$\n\n"
            "Esto es **trigonometría aplicada a complejos** — y conecta este capítulo con el Cap. 5 y 6.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces la **forma polar/trigonométrica** $z = r(\\cos \\theta + i \\sin \\theta)$.\n"
            "- Aplicás la **fórmula de Euler** $e^{i\\theta} = \\cos\\theta + i \\sin\\theta$.\n"
            "- Conviertes entre forma estándar y polar.\n"
            "- Multiplicás y dividís en forma polar (sumar/restar argumentos)."
        )),

        b("definicion",
          titulo="Forma polar y exponencial",
          body_md=(
              "Sea $z = a + b i \\neq 0$. Sea $r = |z| = \\sqrt{a^2 + b^2}$ y $\\theta$ el ángulo que el "
              "vector $z$ forma con el eje real positivo. Entonces:\n\n"
              "$$a = r \\cos \\theta, \\qquad b = r \\sin \\theta.$$\n\n"
              "Sustituyendo en $z = a + b i$:\n\n"
              "$$\\boxed{\\,z = r(\\cos \\theta + i \\sin \\theta).\\,}$$\n\n"
              "Esta es la **forma polar** (o trigonométrica) de $z$.\n\n"
              "**Argumento.** $\\theta$ se llama **argumento** de $z$ y se denota $\\arg(z)$. Como el seno y coseno son periódicos en $2\\pi$, el argumento está definido **módulo $2\\pi$**:\n\n"
              "$$\\arg(z) = \\theta + 2 k \\pi, \\quad k \\in \\mathbb{Z}.$$\n\n"
              "El **argumento principal** $\\operatorname{Arg}(z)$ se elige en $(-\\pi, \\pi]$ (o $[0, 2\\pi)$ según convención).\n\n"
              "**Forma exponencial (fórmula de Euler):**\n\n"
              "$$e^{i \\theta} = \\cos \\theta + i \\sin \\theta.$$\n\n"
              "Por lo tanto:\n\n"
              "$$\\boxed{\\,z = r\\, e^{i \\theta}.\\,}$$\n\n"
              "Es la forma **más compacta** y la preferida en aplicaciones."
          )),

        formulas(
            titulo="Conversiones",
            body=(
                "**De forma estándar $a + b i$ a polar $(r, \\theta)$:**\n\n"
                "$$r = \\sqrt{a^2 + b^2}, \\qquad \\theta = \\arctan\\dfrac{b}{a}, \\text{ ajustado por cuadrante.}$$\n\n"
                "El ajuste por cuadrante es el mismo que para coordenadas polares (Cap. 6): $\\arctan$ devuelve un valor en $(-\\pi/2, \\pi/2)$, hay que sumar $\\pi$ si $a < 0$ para llegar al cuadrante correcto.\n\n"
                "**De polar a estándar:**\n\n"
                "$$a = r \\cos \\theta, \\qquad b = r \\sin \\theta.$$\n\n"
                "Sustituir y simplificar."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Estándar a polar",
          problema_md="Convierte $z = -1 + i$ a forma polar y exponencial.",
          pasos=[
              {"accion_md": (
                  "**Módulo:** $r = \\sqrt{(-1)^2 + 1^2} = \\sqrt{2}$.\n\n"
                  "**Argumento:** $z$ está en cuadrante II ($a < 0, b > 0$). $\\arctan(1/(-1)) = \\arctan(-1) = -\\pi/4$. Sumar $\\pi$ por estar en II: $\\theta = \\pi - \\pi/4 = 3\\pi/4$."
              ),
               "justificacion_md": "Ajustar el ángulo según cuadrante.",
               "es_resultado": False},
              {"accion_md": (
                  "**Forma polar:** $z = \\sqrt{2}(\\cos(3\\pi/4) + i \\sin(3\\pi/4))$.\n\n"
                  "**Forma exponencial:** $z = \\sqrt{2}\\, e^{i \\cdot 3\\pi/4}$."
              ),
               "justificacion_md": "Las dos representaciones son equivalentes.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Multiplicación y división en forma polar",
            body=(
                "Sean $z_1 = r_1 e^{i \\theta_1}$ y $z_2 = r_2 e^{i \\theta_2}$.\n\n"
                "**Multiplicación:**\n\n"
                "$$\\boxed{\\,z_1 \\cdot z_2 = r_1 r_2\\, e^{i(\\theta_1 + \\theta_2)}.\\,}$$\n\n"
                "Es decir: **multiplicar módulos** y **sumar argumentos**.\n\n"
                "**División:**\n\n"
                "$$\\boxed{\\,\\dfrac{z_1}{z_2} = \\dfrac{r_1}{r_2}\\, e^{i(\\theta_1 - \\theta_2)}.\\,}$$\n\n"
                "**Dividir módulos** y **restar argumentos**.\n\n"
                "**Por qué funcionan.** Como $e^{i\\theta_1} \\cdot e^{i\\theta_2} = e^{i(\\theta_1 + \\theta_2)}$ por leyes de exponentes, "
                "y los módulos son escalares reales que se multiplican normalmente.\n\n"
                "**Geometría.** Multiplicar por $z = r e^{i\\theta}$ corresponde a una **rotación de $\\theta$ y un escalamiento por $r$** en el plano."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Multiplicar en forma polar",
          problema_md="Calcula $z_1 \\cdot z_2$ con $z_1 = 2 e^{i \\pi/4}$ y $z_2 = 3 e^{i \\pi/6}$.",
          pasos=[
              {"accion_md": (
                  "**Multiplicar módulos:** $2 \\cdot 3 = 6$.\n\n"
                  "**Sumar argumentos:** $\\pi/4 + \\pi/6 = 3\\pi/12 + 2\\pi/12 = 5\\pi/12$."
              ),
               "justificacion_md": "Sumar fracciones con denominador común.",
               "es_resultado": False},
              {"accion_md": (
                  "**Resultado:** $z_1 z_2 = 6\\, e^{i \\cdot 5\\pi/12}$."
              ),
               "justificacion_md": "Mucho más simple que en forma estándar.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Dividir en forma polar",
          problema_md="Calcula $z_1 / z_2$ con $z_1 = 6 e^{i \\pi/3}$ y $z_2 = 2 e^{i \\pi/4}$.",
          pasos=[
              {"accion_md": (
                  "**Dividir módulos:** $6/2 = 3$.\n\n"
                  "**Restar argumentos:** $\\pi/3 - \\pi/4 = 4\\pi/12 - 3\\pi/12 = \\pi/12$."
              ),
               "justificacion_md": "Cuidado al restar argumentos.",
               "es_resultado": False},
              {"accion_md": "**Resultado:** $z_1 / z_2 = 3\\, e^{i \\pi/12}$.",
               "justificacion_md": "División polar es directa.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué la fórmula de Euler $e^{i\\theta} = \\cos\\theta + i\\sin\\theta$ es 'mágica'.** "
            "Conecta tres áreas aparentemente distintas: **exponenciales**, **trigonometría** y **números "
            "complejos**. Es uno de los resultados más elegantes de la matemática. En particular, con "
            "$\\theta = \\pi$:\n\n"
            "$$e^{i \\pi} + 1 = 0,$$\n\n"
            "la **identidad de Euler** — que combina $e, i, \\pi, 1, 0$, las cinco constantes más importantes.\n\n"
            "**Multiplicar = rotar y escalar.** Multiplicar por $e^{i\\theta}$ rota un complejo en $\\theta$ "
            "sin cambiar su módulo. Multiplicar por un real positivo lo escala sin rotarlo. Combinando: "
            "multiplicar por $r e^{i\\theta}$ es **rotación + escalamiento**. Esa interpretación geométrica "
            "es clave en aplicaciones (procesamiento de señales, computación gráfica, etc.).\n\n"
            "**Cuándo usar cada forma.** **Estándar** para sumas y restas. **Polar/exponencial** para "
            "productos, cocientes y potencias."
        )),

        fig(
            "Plano complejo con un complejo z = a + bi marcado. "
            "Vector desde el origen al punto z, con r = |z| etiquetado como longitud del vector y θ etiquetado como ángulo desde el eje real positivo. "
            "Triángulo rectángulo formado por el vector, su proyección sobre el eje real (etiquetada a = r cos θ) y la perpendicular (etiquetada b = r sin θ). "
            "Acentos teal #06b6d4 para r y θ, ámbar #f59e0b para a y b. "
            "Etiqueta superior: 'z = r(cos θ + i sin θ) = r e^{iθ}'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$|3 + 4 i| = $",
                  "opciones_md": [
                      "$3$",
                      "$4$",
                      "**$5$**",
                      "$7$",
                  ],
                  "correcta": "C",
                  "pista_md": "$\\sqrt{9 + 16}$.",
                  "explicacion_md": "Pitágoras: $\\sqrt{9 + 16} = \\sqrt{25} = 5$.",
              },
              {
                  "enunciado_md": "$e^{i\\pi} = $",
                  "opciones_md": [
                      "$0$",
                      "**$-1$**",
                      "$1$",
                      "$i$",
                  ],
                  "correcta": "B",
                  "pista_md": "Euler con $\\theta = \\pi$.",
                  "explicacion_md": "$\\cos \\pi + i \\sin \\pi = -1 + 0 = -1$.",
              },
              {
                  "enunciado_md": "Multiplicar dos complejos en forma polar:",
                  "opciones_md": [
                      "Sumar módulos, multiplicar argumentos",
                      "**Multiplicar módulos, sumar argumentos**",
                      "Multiplicar todo",
                      "Restar argumentos",
                  ],
                  "correcta": "B",
                  "pista_md": "Recordá: $r_1 r_2 e^{i(\\theta_1 + \\theta_2)}$.",
                  "explicacion_md": "Productos en módulo, sumas en argumento.",
              },
          ]),

        ej(
            "Convertir a polar",
            "Convierte $z = 2 - 2 i$ a forma polar.",
            ["Cuadrante IV."],
            (
                "$r = \\sqrt{4 + 4} = 2\\sqrt 2$. Cuadrante IV: $\\theta = -\\pi/4$ (o $7\\pi/4$). $z = 2\\sqrt 2\\, e^{-i \\pi/4}$."
            ),
        ),

        ej(
            "Convertir a estándar",
            "Convierte $z = 4 e^{i \\cdot 5\\pi/6}$ a forma estándar.",
            ["$\\cos(5\\pi/6) = -\\sqrt 3/2, \\sin(5\\pi/6) = 1/2$."],
            (
                "$z = 4(-\\sqrt 3/2 + i \\cdot 1/2) = -2\\sqrt 3 + 2 i$."
            ),
        ),

        ej(
            "Operación polar",
            "Calcula $\\dfrac{z_1}{z_2}$ con $z_1 = 8 e^{i \\cdot 2\\pi/3}$ y $z_2 = 4 e^{i \\cdot \\pi/6}$.",
            ["Dividir módulos, restar argumentos."],
            (
                "$z_1/z_2 = 2 e^{i(2\\pi/3 - \\pi/6)} = 2 e^{i \\cdot \\pi/2} = 2 i$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar ajustar el cuadrante** al calcular $\\theta = \\arctan(b/a)$.",
              "**Confundir multiplicar módulos** ($r_1 r_2$) con sumar módulos.",
              "**Confundir sumar argumentos** ($\\theta_1 + \\theta_2$) con multiplicarlos.",
              "**Tomar argumento de complejo nulo:** $z = 0$ tiene argumento indefinido (todo lo demás es válido).",
              "**No simplificar el argumento final** módulo $2\\pi$ cuando excede el rango.",
          ]),

        b("resumen",
          puntos_md=[
              "**Forma polar:** $z = r(\\cos \\theta + i \\sin \\theta)$ con $r = |z|$ y $\\theta = \\arg(z)$.",
              "**Forma exponencial (Euler):** $z = r e^{i \\theta}$. La más compacta.",
              "**Conversión:** $r = \\sqrt{a^2 + b^2}$, $\\theta = \\arctan(b/a)$ ajustado por cuadrante.",
              "**Multiplicar:** $r_1 r_2 e^{i(\\theta_1 + \\theta_2)}$ — multiplicar módulos, sumar argumentos.",
              "**Dividir:** $(r_1/r_2) e^{i(\\theta_1 - \\theta_2)}$.",
              "**Próxima lección:** potencias y raíces — De Moivre y la magia de las raíces $n$-ésimas.",
          ]),
    ]
    return {
        "id": "lec-prec-7-3-forma-polar-exponencial",
        "title": "Forma polar y exponencial",
        "description": "Forma polar/trigonométrica z = r(cos θ + i sin θ), forma exponencial vía fórmula de Euler z = r e^{iθ}. Conversión entre forma estándar y polar. Multiplicación y división en forma polar (sumar/restar argumentos).",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# Teorema de De Moivre y raíces
# =====================================================================
def lesson_moivre_raices():
    blocks = [
        b("texto", body_md=(
            "Las dos aplicaciones más espectaculares de la forma polar/exponencial son:\n\n"
            "1. **Potencias enteras** mediante el **teorema de De Moivre**.\n"
            "2. **Raíces $n$-ésimas** que producen exactamente $n$ valores distribuidos uniformemente en una circunferencia.\n\n"
            "Ambas se vuelven **triviales** en forma polar y serían **muy laboriosas** en forma estándar.\n\n"
            "**Aplicaciones famosas:**\n\n"
            "- **Raíces $n$-ésimas de la unidad:** vértices de polígonos regulares.\n"
            "- **Resolución de ecuaciones polinomiales** con coeficientes complejos.\n"
            "- **Diseño de filtros digitales** (procesamiento de señales).\n\n"
            "**Al terminar:**\n\n"
            "- Aplicás el **teorema de De Moivre** para calcular $z^n$.\n"
            "- Calculás las **$n$ raíces $n$-ésimas** de cualquier complejo.\n"
            "- Conoces las **raíces de la unidad** y su distribución geométrica."
        )),

        b("definicion",
          titulo="Teorema de De Moivre",
          body_md=(
              "**Teorema (De Moivre).** Si $z = r(\\cos \\theta + i \\sin \\theta) = r e^{i \\theta}$ y $n \\in \\mathbb{Z}$:\n\n"
              "$$\\boxed{\\,z^n = r^n (\\cos n\\theta + i \\sin n\\theta) = r^n\\, e^{i n \\theta}.\\,}$$\n\n"
              "Es decir: para elevar a la $n$-ésima, **elevar el módulo a la $n$** y **multiplicar el argumento por $n$**.\n\n"
              "**Demostración (vía exponencial).** $z^n = (r e^{i \\theta})^n = r^n (e^{i \\theta})^n = r^n e^{i n \\theta}$ por leyes de exponentes. La forma trigonométrica sale aplicando Euler.\n\n"
              "**Aplicaciones notables:**\n\n"
              "- Calcular potencias altas que serían imposibles en forma estándar.\n"
              "- Derivar identidades trigonométricas como $\\cos(n \\theta)$ y $\\sin(n \\theta)$ en términos de $\\cos \\theta$ y $\\sin \\theta$.\n"
              "- Demostrar identidades de suma y resta de ángulos a partir de productos de exponenciales."
          )),

        b("ejemplo_resuelto",
          titulo="De Moivre en acción",
          problema_md="Calcula $(1 + i)^{10}$.",
          pasos=[
              {"accion_md": (
                  "**Convertir a polar.** $|1 + i| = \\sqrt{2}$. $\\arg(1 + i) = \\pi/4$ (cuadrante I).\n\n"
                  "$1 + i = \\sqrt{2}\\, e^{i \\pi/4}$."
              ),
               "justificacion_md": "Forma exponencial primero.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar De Moivre:** $(1 + i)^{10} = (\\sqrt{2})^{10} e^{i \\cdot 10 \\pi/4} = 2^5 e^{i \\cdot 5\\pi/2} = 32\\, e^{i \\pi/2}$.\n\n"
                  "(Reducir $5\\pi/2 = 2 \\pi + \\pi/2$, así $e^{i \\cdot 5\\pi/2} = e^{i \\pi/2}$.)"
              ),
               "justificacion_md": "Reducir el argumento módulo $2\\pi$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Convertir de vuelta:** $32\\, e^{i \\pi/2} = 32 (\\cos \\pi/2 + i \\sin \\pi/2) = 32 (0 + i) = 32 i$.\n\n"
                  "**$(1 + i)^{10} = 32 i$.**"
              ),
               "justificacion_md": "Mucho más rápido que multiplicar 10 veces.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Raíces $n$-ésimas de un complejo",
            body=(
                "Sea $z = r e^{i \\theta}$ y $n \\geq 1$. Las **raíces $n$-ésimas** de $z$ son los $n$ complejos:\n\n"
                "$$\\boxed{\\,z_k = r^{1/n}\\, e^{i (\\theta + 2 k \\pi)/n}, \\qquad k = 0, 1, 2, \\ldots, n - 1.\\,}$$\n\n"
                "Equivalentemente:\n\n"
                "$$z_k = r^{1/n}\\left(\\cos \\dfrac{\\theta + 2 k \\pi}{n} + i \\sin \\dfrac{\\theta + 2 k \\pi}{n}\\right).$$\n\n"
                "**Propiedades fundamentales:**\n\n"
                "- Hay **exactamente $n$ raíces distintas** (por TFA).\n"
                "- **Todas tienen el mismo módulo** $r^{1/n}$.\n"
                "- **Sus argumentos están equiespaciados** por $2\\pi/n$.\n"
                "- En el plano, **forman los vértices de un $n$-gono regular** centrado en el origen, inscrito en una circunferencia de radio $r^{1/n}$.\n\n"
                "**Por qué $n$ raíces.** $z^n = w$ es una ecuación polinomial de grado $n$, así por TFA tiene $n$ soluciones. La fórmula con $k = 0, \\ldots, n-1$ las enumera todas."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Raíces cuartas de la unidad",
          problema_md="Halla las **cuatro raíces cuartas de 1**.",
          pasos=[
              {"accion_md": (
                  "**Forma polar de 1:** $z = 1 = 1 \\cdot e^{i \\cdot 0}$. Así $r = 1, \\theta = 0$, $n = 4$."
              ),
               "justificacion_md": "$1$ es real puro positivo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar fórmula con $k = 0, 1, 2, 3$:**\n\n"
                  "$z_k = 1^{1/4}\\, e^{i (0 + 2 k \\pi)/4} = e^{i k \\pi/2}$.\n\n"
                  "$z_0 = e^{i \\cdot 0} = 1$.\n"
                  "$z_1 = e^{i \\pi/2} = i$.\n"
                  "$z_2 = e^{i \\pi} = -1$.\n"
                  "$z_3 = e^{i \\cdot 3\\pi/2} = -i$."
              ),
               "justificacion_md": "Las cuatro raíces son $1, i, -1, -i$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Geometría.** Los cuatro puntos están en la circunferencia unitaria, equiespaciados por $\\pi/2$ — son los **vértices de un cuadrado**.\n\n"
                  "**Verificación:** $i^4 = (i^2)^2 = (-1)^2 = 1$ ✓."
              ),
               "justificacion_md": "Las raíces cuartas de 1 son las potencias de $i$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Raíces cúbicas de un complejo",
          problema_md="Halla las raíces cúbicas de $z = -8$.",
          pasos=[
              {"accion_md": (
                  "**Forma polar.** $-8 = 8 e^{i \\pi}$ (real negativo, argumento $\\pi$). $r = 8, \\theta = \\pi, n = 3$."
              ),
               "justificacion_md": "Identificar $r$ y $\\theta$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Fórmula:** $z_k = 8^{1/3}\\, e^{i(\\pi + 2 k \\pi)/3} = 2\\, e^{i(\\pi + 2 k \\pi)/3}$ para $k = 0, 1, 2$.\n\n"
                  "$z_0 = 2 e^{i \\pi/3} = 2(\\cos \\pi/3 + i \\sin \\pi/3) = 2(1/2 + i \\sqrt 3/2) = 1 + i\\sqrt{3}$.\n\n"
                  "$z_1 = 2 e^{i \\pi} = -2$.\n\n"
                  "$z_2 = 2 e^{i \\cdot 5\\pi/3} = 2(\\cos 5\\pi/3 + i \\sin 5\\pi/3) = 2(1/2 - i \\sqrt 3/2) = 1 - i\\sqrt{3}$."
              ),
               "justificacion_md": "Las tres raíces cúbicas distribuidas en triángulo equilátero.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación.** $(-2)^3 = -8$ ✓. Las otras dos son las raíces cúbicas complejas: forman vértices de un triángulo equilátero centrado en el origen, radio 2."
              ),
               "justificacion_md": "Notar que solo una raíz es real; las otras dos vienen como par conjugado.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué las raíces forman polígonos regulares.** Las $n$ raíces tienen el mismo módulo "
            "$r^{1/n}$ — están en una circunferencia. Sus argumentos son $\\theta/n + 2\\pi k/n$ — equiespaciados por "
            "$2\\pi/n$. Eso es exactamente la receta de los vértices de un **$n$-gono regular**.\n\n"
            "**Raíces de la unidad.** Las $n$ raíces $n$-ésimas de 1 son $\\omega_k = e^{2\\pi i k/n}$ para "
            "$k = 0, 1, \\ldots, n - 1$. Forman un $n$-gono regular en la circunferencia unitaria, con un "
            "vértice en $1$. Estas raíces tienen propiedades aritméticas profundas (suman 0 cuando $n > 1$, "
            "su producto es $\\pm 1$, etc.).\n\n"
            "**Aplicación: factorizar $x^n - 1$.** Las raíces de la unidad son **exactamente** las raíces de "
            "$x^n - 1 = 0$. Por TFA, $x^n - 1 = (x - 1)(x - \\omega_1) \\cdots (x - \\omega_{n - 1})$."
        )),

        fig(
            "Las tres raíces cúbicas de -8 dibujadas en el plano complejo. "
            "Circunferencia de radio 2 centrada en el origen, en color gris claro. "
            "Tres puntos sobre la circunferencia, equiespaciados a 120° entre sí, conectados formando un triángulo equilátero. "
            "Coordenadas: z_0 = 1 + i√3 (etiquetado), z_1 = -2 (etiquetado), z_2 = 1 - i√3 (etiquetado). "
            "Acentos teal #06b6d4 para los puntos, ámbar #f59e0b para la circunferencia y el triángulo. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Por De Moivre, $(2 e^{i \\pi/6})^3 = $",
                  "opciones_md": [
                      "$6 e^{i \\pi/2}$",
                      "**$8 e^{i \\pi/2}$**",
                      "$2 e^{i \\pi/2}$",
                      "$8 e^{i \\pi/6}$",
                  ],
                  "correcta": "B",
                  "pista_md": "$r^n e^{i n \\theta}$.",
                  "explicacion_md": "$2^3 = 8$ y $3 \\cdot \\pi/6 = \\pi/2$.",
              },
              {
                  "enunciado_md": "Cuántas raíces cuartas tiene un complejo no nulo:",
                  "opciones_md": [
                      "$1$",
                      "$2$",
                      "**$4$**",
                      "Infinitas",
                  ],
                  "correcta": "C",
                  "pista_md": "Tantas como el orden de la raíz.",
                  "explicacion_md": "TFA: ecuación de grado 4 tiene 4 raíces.",
              },
              {
                  "enunciado_md": "Las raíces $n$-ésimas de la unidad están distribuidas:",
                  "opciones_md": [
                      "En el eje real",
                      "**En los vértices de un $n$-gono regular en la circunferencia unitaria**",
                      "Aleatoriamente",
                      "En el eje imaginario",
                  ],
                  "correcta": "B",
                  "pista_md": "Equiespaciados en una circunferencia de radio 1.",
                  "explicacion_md": "Vértices de polígono regular.",
              },
          ]),

        ej(
            "De Moivre",
            "Calcula $(\\sqrt{3} + i)^6$.",
            ["Convertir a polar primero."],
            (
                "$|\\sqrt 3 + i| = 2$, $\\arg = \\pi/6$. Así $\\sqrt 3 + i = 2 e^{i \\pi/6}$. "
                "$(2 e^{i \\pi/6})^6 = 64 e^{i \\pi} = -64$."
            ),
        ),

        ej(
            "Raíces sextas de 1",
            "Halla las 6 raíces sextas de 1.",
            ["Equiespaciadas en circunferencia unitaria."],
            (
                "$z_k = e^{i k \\pi/3}$ para $k = 0, 1, 2, 3, 4, 5$. "
                "Son: $1, e^{i \\pi/3}, e^{i \\cdot 2\\pi/3}, -1, e^{i \\cdot 4\\pi/3}, e^{i \\cdot 5\\pi/3}$. Forman un hexágono regular."
            ),
        ),

        ej(
            "Raíces de complejo",
            "Halla las raíces cuadradas de $z = i$.",
            ["$i = e^{i \\pi/2}$, así raíces son $e^{i \\pi/4}$ y $e^{i \\cdot 5\\pi/4}$."],
            (
                "$z_0 = e^{i \\pi/4} = (\\sqrt 2/2)(1 + i)$. $z_1 = e^{i \\cdot 5\\pi/4} = -(\\sqrt 2/2)(1 + i)$. "
                "Verificar: $z_0^2 = e^{i \\pi/2} = i$ ✓."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el $2 k \\pi$ en la fórmula de raíces.** Sin él, salen menos raíces de las debidas.",
              "**Pensar que solo hay una 'raíz principal'.** Hay **$n$** raíces $n$-ésimas, todas válidas.",
              "**No reducir el argumento final** módulo $2\\pi$. Resulta en argumentos no canónicos.",
              "**Aplicar De Moivre directamente a un complejo en forma estándar.** Hay que pasar primero a polar.",
              "**Calcular $r^{1/n}$ asumiendo que es la raíz real principal sin más.** Para $n$ par y $r$ negativo (que no ocurre porque $r > 0$), pero hay que manejar $r$ correctamente.",
          ]),

        b("resumen",
          puntos_md=[
              "**Teorema de De Moivre:** $z^n = r^n e^{i n \\theta}$.",
              "**Raíces $n$-ésimas:** $z_k = r^{1/n} e^{i(\\theta + 2 k \\pi)/n}$ para $k = 0, \\ldots, n - 1$.",
              "**Propiedades:** $n$ raíces distintas, mismo módulo $r^{1/n}$, equiespaciadas en argumento por $2\\pi/n$.",
              "**Geometría:** las raíces son los vértices de un $n$-gono regular centrado en el origen.",
              "**Raíces de la unidad:** vértices de un $n$-gono regular en la circunferencia unitaria.",
              "**Cierre del capítulo:** dominamos los complejos — definición, operaciones, formas polar/exponencial, potencias y raíces.",
              "**Próximo capítulo (último):** sucesiones y series — el último gran tema del precálculo.",
          ]),
    ]
    return {
        "id": "lec-prec-7-4-moivre-raices",
        "title": "Teorema de De Moivre y raíces",
        "description": "Teorema de De Moivre para potencias enteras de complejos. Cálculo de las n raíces n-ésimas de un complejo (n soluciones equiespaciadas formando un n-gono regular). Raíces de la unidad.",
        "blocks": blocks,
        "duration_minutes": 50,
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

    chapter_id = "ch-prec-numeros-complejos"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Números Complejos",
        "description": (
            "Números complejos z = a + bi con i² = -1: forma estándar, conjugado, módulo, operaciones "
            "aritméticas, plano de Gauss. Forma polar y exponencial vía fórmula de Euler. Teorema de "
            "De Moivre y cálculo de raíces n-ésimas con su distribución geométrica."
        ),
        "order": 7,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_definicion_complejos,
        lesson_operaciones_complejos,
        lesson_forma_polar,
        lesson_moivre_raices,
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
        f"✅ Capítulo 7 — Números Complejos listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
