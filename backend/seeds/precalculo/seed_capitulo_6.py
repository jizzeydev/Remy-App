"""
Seed del curso Precálculo — Capítulo 6: Trigonometría Analítica.

Crea el capítulo 'Trigonometría Analítica' bajo el curso 'precalculo'
y siembra sus 5 lecciones:

  - Identidades trigonométricas
  - Fórmulas (suma, doble, mitad, producto-suma)
  - Ecuaciones trigonométricas
  - Coordenadas polares
  - Curvas en coordenadas polares

Basado en los Apuntes/Clase de Se Remonta. Idempotente.
Las dos últimas lecciones (Polares y Curvas) están escritas desde
conocimiento estándar — los PDFs originales no estaban disponibles.
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
# Identidades trigonométricas
# =====================================================================
def lesson_identidades():
    blocks = [
        b("texto", body_md=(
            "Una **identidad trigonométrica** es una igualdad entre expresiones trigonométricas que se "
            "cumple para **todos los valores** de la variable donde ambos lados están definidos. Es el "
            "lenguaje algebraico de la trigonometría: las identidades nos permiten **transformar** "
            "expresiones complicadas en formas más simples, **simplificar** ecuaciones y **demostrar** "
            "nuevos resultados.\n\n"
            "**Diferencia clave entre identidad y ecuación.**\n\n"
            "- Una **ecuación** ($\\sin x = 1/2$) es cierta solo para valores **específicos** de $x$.\n"
            "- Una **identidad** ($\\sin^2 x + \\cos^2 x = 1$) es cierta para **todo** $x$.\n\n"
            "En esta lección consolidamos las **identidades fundamentales** ya vistas en el Cap. 5 y "
            "aprendemos las **estrategias** para verificar identidades nuevas.\n\n"
            "**Al terminar:**\n\n"
            "- Reconoces las **identidades pitagóricas, recíprocas, de cociente y de paridad**.\n"
            "- Aplicás técnicas estándar para **verificar identidades**.\n"
            "- Simplificás expresiones trigonométricas combinando varias identidades."
        )),

        formulas(
            titulo="Identidades fundamentales",
            body=(
                "**Identidades recíprocas:**\n\n"
                "$$\\csc \\theta = \\dfrac{1}{\\sin \\theta}, \\qquad \\sec \\theta = \\dfrac{1}{\\cos \\theta}, \\qquad \\cot \\theta = \\dfrac{1}{\\tan \\theta}.$$\n\n"
                "**Identidades de cociente:**\n\n"
                "$$\\tan \\theta = \\dfrac{\\sin \\theta}{\\cos \\theta}, \\qquad \\cot \\theta = \\dfrac{\\cos \\theta}{\\sin \\theta}.$$\n\n"
                "**Identidades pitagóricas (las tres versiones):**\n\n"
                "$$\\sin^2 \\theta + \\cos^2 \\theta = 1.$$\n\n"
                "$$1 + \\tan^2 \\theta = \\sec^2 \\theta.$$\n\n"
                "$$1 + \\cot^2 \\theta = \\csc^2 \\theta.$$\n\n"
                "**Identidades de paridad:**\n\n"
                "$$\\sin(-\\theta) = -\\sin \\theta, \\qquad \\cos(-\\theta) = \\cos \\theta, \\qquad \\tan(-\\theta) = -\\tan \\theta.$$\n\n"
                "$$\\csc(-\\theta) = -\\csc \\theta, \\qquad \\sec(-\\theta) = \\sec \\theta, \\qquad \\cot(-\\theta) = -\\cot \\theta.$$\n\n"
                "**Identidades complementarias** ($90^\\circ - \\theta$):\n\n"
                "$$\\sin(\\pi/2 - \\theta) = \\cos \\theta, \\qquad \\cos(\\pi/2 - \\theta) = \\sin \\theta,$$\n"
                "$$\\tan(\\pi/2 - \\theta) = \\cot \\theta, \\qquad \\cot(\\pi/2 - \\theta) = \\tan \\theta.$$"
            ),
        ),

        formulas(
            titulo="Estrategias para verificar identidades",
            body=(
                "**Regla cardinal:** **trabajar un lado a la vez** y transformarlo hasta que sea igual al otro. "
                "**No** mover términos de un lado al otro — eso es álgebra de ecuaciones, no de identidades.\n\n"
                "**Estrategias en orden de prioridad:**\n\n"
                "1. **Empezar por el lado más complicado.** Más sentido transformar lo difícil en lo simple.\n"
                "2. **Reescribir todo en términos de $\\sin$ y $\\cos$** — la forma más reducida.\n"
                "3. **Aplicar identidades pitagóricas** para reemplazar $\\sin^2 + \\cos^2$ por $1$ (o al revés).\n"
                "4. **Combinar fracciones con denominador común.**\n"
                "5. **Factorizar** o **expandir** según convenga.\n"
                "6. **Multiplicar arriba y abajo** por una expresión adecuada (a veces el conjugado: $1 + \\sin$, $1 - \\cos$, etc.).\n"
                "7. **Probar reescribir el otro lado** si te quedas atascado.\n\n"
                "**Si todo falla**, transformá ambos lados independientemente a una forma común y comparalos."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Verificar una identidad básica",
          problema_md="Verifica que $\\dfrac{1 - \\cos^2 \\theta}{\\sin \\theta} = \\sin \\theta$.",
          pasos=[
              {"accion_md": (
                  "**Trabajar el lado izquierdo.** Por pitagórica, $1 - \\cos^2 \\theta = \\sin^2 \\theta$."
              ),
               "justificacion_md": "Reemplazar $1 - \\cos^2$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\dfrac{\\sin^2 \\theta}{\\sin \\theta} = \\sin \\theta$. ✓\n\n"
                  "**Coincide con el lado derecho.**"
              ),
               "justificacion_md": "Cancelación.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Reescribir todo en sin y cos",
          problema_md="Verifica que $\\tan \\theta + \\cot \\theta = \\sec \\theta \\csc \\theta$.",
          pasos=[
              {"accion_md": (
                  "**Lado izquierdo en sin y cos:**\n\n"
                  "$\\tan \\theta + \\cot \\theta = \\dfrac{\\sin \\theta}{\\cos \\theta} + \\dfrac{\\cos \\theta}{\\sin \\theta}$."
              ),
               "justificacion_md": "Convertir a la forma más simple.",
               "es_resultado": False},
              {"accion_md": (
                  "**Denominador común** $\\sin \\theta \\cos \\theta$:\n\n"
                  "$\\dfrac{\\sin^2 \\theta + \\cos^2 \\theta}{\\sin \\theta \\cos \\theta} = \\dfrac{1}{\\sin \\theta \\cos \\theta}$ (por pitagórica)."
              ),
               "justificacion_md": "Combinar y simplificar.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\dfrac{1}{\\sin \\theta \\cos \\theta} = \\dfrac{1}{\\sin \\theta} \\cdot \\dfrac{1}{\\cos \\theta} = \\csc \\theta \\sec \\theta = \\sec \\theta \\csc \\theta$. ✓"
              ),
               "justificacion_md": "Reescribir como producto de recíprocas.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Multiplicar por el conjugado",
          problema_md="Verifica que $\\dfrac{1}{1 - \\sin \\theta} + \\dfrac{1}{1 + \\sin \\theta} = 2 \\sec^2 \\theta$.",
          pasos=[
              {"accion_md": (
                  "**Sumar fracciones con denominador común** $(1 - \\sin \\theta)(1 + \\sin \\theta) = 1 - \\sin^2 \\theta = \\cos^2 \\theta$:\n\n"
                  "$\\dfrac{(1 + \\sin \\theta) + (1 - \\sin \\theta)}{\\cos^2 \\theta} = \\dfrac{2}{\\cos^2 \\theta} = 2 \\sec^2 \\theta$. ✓"
              ),
               "justificacion_md": "El producto $(1 - \\sin)(1 + \\sin)$ produce diferencia de cuadrados, que se simplifica con pitagórica.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué 'verificar' una identidad no es resolver una ecuación.** Si la identidad es cierta, "
            "podemos manipular **ambos lados** algebraicamente para mostrar que coinciden. Pero **mover** "
            "términos de un lado al otro asume que la igualdad ya es cierta, lo que es **circular**.\n\n"
            "**Por qué reescribir en $\\sin/\\cos$ funciona casi siempre.** $\\sin$ y $\\cos$ son las funciones "
            "fundamentales; las otras 4 son combinaciones de ellas. Bajar todo a esa 'base común' es como "
            "factorizar primos: revela la estructura.\n\n"
            "**El truco del conjugado.** Multiplicar por $\\dfrac{1 + \\sin}{1 + \\sin}$ (o similar) "
            "transforma diferencia en suma de cuadrados. Es el mismo truco que con $\\sqrt{a} - \\sqrt{b}$ "
            "en racionalizaciones."
        )),

        fig(
            "Diagrama esquemático de las identidades trigonométricas fundamentales. "
            "Caja central con 'sin θ y cos θ' destacado. "
            "Cuatro ramas saliendo: 'Recíprocas (csc, sec, cot)', 'Cocientes (tan, cot)', 'Pitagóricas (sin²+cos²=1)', 'Paridad (par/impar)'. "
            "Acento teal #06b6d4 para sin/cos, ámbar #f59e0b para las derivadas. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\sin^2 \\theta + \\cos^2 \\theta = $",
                  "opciones_md": [
                      "$0$",
                      "**$1$**",
                      "$\\theta$",
                      "$2$",
                  ],
                  "correcta": "B",
                  "pista_md": "Pitagórica fundamental.",
                  "explicacion_md": "Identidad central — vale para todo $\\theta$.",
              },
              {
                  "enunciado_md": "Estrategia recomendada para verificar identidades:",
                  "opciones_md": [
                      "Mover términos al otro lado",
                      "**Trabajar un lado y transformarlo hasta coincidir con el otro**",
                      "Multiplicar ambos lados por cero",
                      "Despejar una variable",
                  ],
                  "correcta": "B",
                  "pista_md": "No es como una ecuación.",
                  "explicacion_md": "Las identidades se verifican; no se 'resuelven'.",
              },
              {
                  "enunciado_md": "$\\sin(-\\theta) = $",
                  "opciones_md": [
                      "$\\sin \\theta$",
                      "**$-\\sin \\theta$**",
                      "$\\cos \\theta$",
                      "$-\\cos \\theta$",
                  ],
                  "correcta": "B",
                  "pista_md": "Seno es función impar.",
                  "explicacion_md": "Identidad de paridad.",
              },
          ]),

        ej(
            "Identidad básica",
            "Verifica que $\\sec \\theta - \\sin \\theta \\tan \\theta = \\cos \\theta$.",
            ["Reescribir en $\\sin$ y $\\cos$."],
            (
                "$\\sec \\theta - \\sin \\theta \\tan \\theta = \\dfrac{1}{\\cos \\theta} - \\sin \\theta \\cdot \\dfrac{\\sin \\theta}{\\cos \\theta} = \\dfrac{1 - \\sin^2 \\theta}{\\cos \\theta} = \\dfrac{\\cos^2 \\theta}{\\cos \\theta} = \\cos \\theta$. ✓"
            ),
        ),

        ej(
            "Con conjugado",
            "Verifica que $\\dfrac{\\cos \\theta}{1 - \\sin \\theta} = \\dfrac{1 + \\sin \\theta}{\\cos \\theta}$.",
            ["Multiplicar arriba y abajo del lado izquierdo por $1 + \\sin \\theta$."],
            (
                "$\\dfrac{\\cos \\theta}{1 - \\sin \\theta} \\cdot \\dfrac{1 + \\sin \\theta}{1 + \\sin \\theta} = \\dfrac{\\cos \\theta (1 + \\sin \\theta)}{1 - \\sin^2 \\theta} = \\dfrac{\\cos \\theta (1 + \\sin \\theta)}{\\cos^2 \\theta} = \\dfrac{1 + \\sin \\theta}{\\cos \\theta}$. ✓"
            ),
        ),

        ej(
            "Combinar varias",
            "Simplifica $(\\sin \\theta + \\cos \\theta)^2 + (\\sin \\theta - \\cos \\theta)^2$.",
            ["Expandir ambos cuadrados y usar pitagórica."],
            (
                "$(\\sin^2 + 2 \\sin \\cos + \\cos^2) + (\\sin^2 - 2 \\sin \\cos + \\cos^2) = 2 \\sin^2 + 2 \\cos^2 = 2 (\\sin^2 + \\cos^2) = 2$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Mover términos como en una ecuación.** Identidades se transforman lado por lado, no se 'resuelven'.",
              "**Asumir lo que se quiere demostrar.** Es circularidad.",
              "**Olvidar restricciones de dominio** donde funciones no están definidas.",
              "**Confundir $\\sin^2 \\theta$ con $\\sin(\\theta^2)$.** Significa $(\\sin \\theta)^2$.",
              "**No reducir todo a $\\sin$ y $\\cos$** cuando el camino se complica.",
          ]),

        b("resumen",
          puntos_md=[
              "**Identidad** vs **ecuación:** identidad cierta para todo $x$; ecuación, solo para algunos.",
              "**Cuatro familias fundamentales:** recíprocas, cocientes, pitagóricas, paridad.",
              "**Verificar:** trabajar un lado a la vez, transformar hasta igualar al otro.",
              "**Estrategia universal:** reescribir en $\\sin$ y $\\cos$, aplicar pitagórica, combinar fracciones.",
              "**Próxima lección:** identidades nuevas — suma/resta, ángulo doble y mitad.",
          ]),
    ]
    return {
        "id": "lec-prec-6-1-identidades",
        "title": "Identidades trigonométricas",
        "description": "Identidades fundamentales: recíprocas, cocientes, pitagóricas (las tres versiones), paridad y complementarias. Estrategias para verificar identidades trigonométricas paso a paso.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 1,
    }


# =====================================================================
# Fórmulas (suma, ángulo doble, mitad, producto-suma)
# =====================================================================
def lesson_formulas():
    blocks = [
        b("texto", body_md=(
            "En esta lección agregamos al repertorio las **fórmulas avanzadas** de la trigonometría. Son "
            "las herramientas que convierten productos de funciones trigonométricas en sumas (y al revés), "
            "que calculan funciones de **suma y resta de ángulos**, **ángulos dobles** y **mitades**.\n\n"
            "**¿Para qué sirven?**\n\n"
            "- Calcular valores **exactos** de ángulos no estándar ($15^\\circ = 45^\\circ - 30^\\circ$, etc.).\n"
            "- **Simplificar** expresiones complicadas que de otro modo serían intratables.\n"
            "- **Resolver ecuaciones** trigonométricas que requieren reducir productos a sumas.\n"
            "- En cálculo, **integrar** funciones que contienen $\\sin^2, \\cos^2, \\sin x \\cos x$.\n\n"
            "**Al terminar:**\n\n"
            "- Aplicás las **fórmulas de suma y resta** para $\\sin, \\cos, \\tan$.\n"
            "- Conocés las **identidades de ángulo doble y mitad**.\n"
            "- Manejás las **identidades producto-suma** (mucho menos famosas pero muy útiles)."
        )),

        formulas(
            titulo="Fórmulas de suma y resta",
            body=(
                "**Para el seno:**\n\n"
                "$$\\boxed{\\,\\sin(A + B) = \\sin A \\cos B + \\cos A \\sin B.\\,}$$\n\n"
                "$$\\sin(A - B) = \\sin A \\cos B - \\cos A \\sin B.$$\n\n"
                "**Para el coseno:**\n\n"
                "$$\\boxed{\\,\\cos(A + B) = \\cos A \\cos B - \\sin A \\sin B.\\,}$$\n\n"
                "$$\\cos(A - B) = \\cos A \\cos B + \\sin A \\sin B.$$\n\n"
                "**Para la tangente:**\n\n"
                "$$\\tan(A + B) = \\dfrac{\\tan A + \\tan B}{1 - \\tan A \\tan B}.$$\n\n"
                "$$\\tan(A - B) = \\dfrac{\\tan A - \\tan B}{1 + \\tan A \\tan B}.$$\n\n"
                "**Mnemotecnia.** **Seno** mantiene la **misma operación** ($+$ con $+$, $-$ con $-$); **coseno** la **invierte** ($+$ produce $-$ entre los productos, y $-$ produce $+$)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Calcular $\\sin 75^\\circ$ exacto",
          problema_md="Halla el valor exacto de $\\sin 75^\\circ$.",
          pasos=[
              {"accion_md": (
                  "**Descomponer:** $75^\\circ = 45^\\circ + 30^\\circ$. Aplicar suma:\n\n"
                  "$\\sin 75^\\circ = \\sin(45^\\circ + 30^\\circ) = \\sin 45^\\circ \\cos 30^\\circ + \\cos 45^\\circ \\sin 30^\\circ$."
              ),
               "justificacion_md": "Combinar dos ángulos especiales.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sustituir valores:**\n\n"
                  "$= \\dfrac{\\sqrt{2}}{2} \\cdot \\dfrac{\\sqrt{3}}{2} + \\dfrac{\\sqrt{2}}{2} \\cdot \\dfrac{1}{2} = \\dfrac{\\sqrt{6}}{4} + \\dfrac{\\sqrt{2}}{4} = \\dfrac{\\sqrt{6} + \\sqrt{2}}{4}$.\n\n"
                  "**Resultado:** $\\sin 75^\\circ = \\dfrac{\\sqrt{6} + \\sqrt{2}}{4} \\approx 0{,}966$."
              ),
               "justificacion_md": "Verificable con calculadora.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Fórmulas de ángulo doble",
            body=(
                "Caso particular de la suma con $A = B$:\n\n"
                "**Seno:**\n\n"
                "$$\\boxed{\\,\\sin 2 \\theta = 2 \\sin \\theta \\cos \\theta.\\,}$$\n\n"
                "**Coseno (tres formas equivalentes):**\n\n"
                "$$\\cos 2 \\theta = \\cos^2 \\theta - \\sin^2 \\theta = 2 \\cos^2 \\theta - 1 = 1 - 2 \\sin^2 \\theta.$$\n\n"
                "Las tres versiones son equivalentes (usando pitagórica). Se usan según conveniencia.\n\n"
                "**Tangente:**\n\n"
                "$$\\tan 2 \\theta = \\dfrac{2 \\tan \\theta}{1 - \\tan^2 \\theta}.$$\n\n"
                "**Aplicación operativa.** Las versiones $\\cos 2\\theta = 2 \\cos^2 \\theta - 1$ y $\\cos 2\\theta = 1 - 2 \\sin^2 \\theta$ permiten **despejar $\\cos^2$ o $\\sin^2$**:\n\n"
                "$$\\cos^2 \\theta = \\dfrac{1 + \\cos 2 \\theta}{2}, \\qquad \\sin^2 \\theta = \\dfrac{1 - \\cos 2 \\theta}{2}.$$\n\n"
                "Estas se llaman **fórmulas de reducción de potencia** y son cruciales en cálculo."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Aplicar ángulo doble",
          problema_md="Si $\\sin \\theta = 3/5$ y $\\theta$ está en cuadrante I, halla $\\sin 2\\theta$ y $\\cos 2\\theta$.",
          pasos=[
              {"accion_md": (
                  "**Hallar $\\cos \\theta$.** Por pitagórica $\\cos^2 \\theta = 1 - 9/25 = 16/25$, $\\cos \\theta = 4/5$ (cuadrante I, positivo)."
              ),
               "justificacion_md": "Necesitamos ambos para las fórmulas.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\sin 2\\theta = 2 \\sin \\theta \\cos \\theta = 2 \\cdot (3/5)(4/5) = 24/25$.**"
              ),
               "justificacion_md": "Aplicar fórmula directa.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\cos 2\\theta = \\cos^2 \\theta - \\sin^2 \\theta = 16/25 - 9/25 = 7/25$.**"
              ),
               "justificacion_md": "También se obtiene con $1 - 2 \\sin^2 \\theta = 1 - 18/25 = 7/25$ ✓.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Fórmulas de ángulo mitad",
            body=(
                "Despejando de $\\cos 2 \\theta = 1 - 2 \\sin^2 \\theta$ y $\\cos 2\\theta = 2 \\cos^2 \\theta - 1$, con $\\theta = u/2$:\n\n"
                "$$\\boxed{\\,\\sin \\dfrac{u}{2} = \\pm \\sqrt{\\dfrac{1 - \\cos u}{2}}.\\,}$$\n\n"
                "$$\\boxed{\\,\\cos \\dfrac{u}{2} = \\pm \\sqrt{\\dfrac{1 + \\cos u}{2}}.\\,}$$\n\n"
                "$$\\tan \\dfrac{u}{2} = \\pm \\sqrt{\\dfrac{1 - \\cos u}{1 + \\cos u}} = \\dfrac{1 - \\cos u}{\\sin u} = \\dfrac{\\sin u}{1 + \\cos u}.$$\n\n"
                "**Sobre los signos $\\pm$.** El signo se decide según el **cuadrante donde caiga $u/2$** (no $u$). Las dos últimas formas para $\\tan(u/2)$ no necesitan signo $\\pm$.\n\n"
                "**Aplicación.** Calcular valores exactos de ángulos como $22{,}5^\\circ$ ($= 45^\\circ/2$) o $15^\\circ$ ($= 30^\\circ/2$)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Calcular $\\cos 15^\\circ$",
          problema_md="Halla el valor exacto de $\\cos 15^\\circ$.",
          pasos=[
              {"accion_md": (
                  "**Como $15^\\circ = 30^\\circ / 2$**, aplicar ángulo mitad con $u = 30^\\circ$:\n\n"
                  "$\\cos 15^\\circ = +\\sqrt{\\dfrac{1 + \\cos 30^\\circ}{2}} = \\sqrt{\\dfrac{1 + \\sqrt{3}/2}{2}}$."
              ),
               "justificacion_md": "Signo $+$ porque $15^\\circ$ está en cuadrante I.",
               "es_resultado": False},
              {"accion_md": (
                  "**Simplificar:** $\\sqrt{\\dfrac{2 + \\sqrt{3}}{4}} = \\dfrac{\\sqrt{2 + \\sqrt{3}}}{2}$.\n\n"
                  "**Forma alternativa** racionalizada: $\\dfrac{\\sqrt{6} + \\sqrt{2}}{4} \\approx 0{,}966$."
              ),
               "justificacion_md": "Las dos formas son equivalentes; la segunda es más estándar.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Identidades producto-suma",
            body=(
                "Convierten productos de funciones trigonométricas en sumas (más fáciles de integrar):\n\n"
                "$$\\sin A \\cos B = \\dfrac{1}{2}[\\sin(A + B) + \\sin(A - B)].$$\n\n"
                "$$\\cos A \\sin B = \\dfrac{1}{2}[\\sin(A + B) - \\sin(A - B)].$$\n\n"
                "$$\\cos A \\cos B = \\dfrac{1}{2}[\\cos(A - B) + \\cos(A + B)].$$\n\n"
                "$$\\sin A \\sin B = \\dfrac{1}{2}[\\cos(A - B) - \\cos(A + B)].$$\n\n"
                "**Identidades suma-producto** (al revés):\n\n"
                "$$\\sin x + \\sin y = 2 \\sin\\dfrac{x + y}{2} \\cos\\dfrac{x - y}{2}.$$\n\n"
                "$$\\sin x - \\sin y = 2 \\cos\\dfrac{x + y}{2} \\sin\\dfrac{x - y}{2}.$$\n\n"
                "$$\\cos x + \\cos y = 2 \\cos\\dfrac{x + y}{2} \\cos\\dfrac{x - y}{2}.$$\n\n"
                "$$\\cos x - \\cos y = -2 \\sin\\dfrac{x + y}{2} \\sin\\dfrac{x - y}{2}.$$\n\n"
                "**Aplicaciones:** procesamiento de señales (interferencia, batidos acústicos), integración trigonométrica."
            ),
        ),

        b("intuicion", body_md=(
            "**De dónde salen estas fórmulas.** La fórmula $\\sin(A + B) = \\sin A \\cos B + \\cos A \\sin B$ "
            "se prueba geométricamente con el círculo unitario, o algebraicamente usando la fórmula de Euler "
            "$e^{i\\theta} = \\cos\\theta + i \\sin\\theta$ y multiplicando $e^{iA} e^{iB} = e^{i(A+B)}$.\n\n"
            "**Ángulo doble como caso especial.** $\\sin 2\\theta = \\sin(\\theta + \\theta) = \\sin\\theta\\cos\\theta + \\cos\\theta\\sin\\theta = 2\\sin\\theta\\cos\\theta$. Lo mismo para coseno.\n\n"
            "**Fórmulas de reducción de potencia.** $\\sin^2 \\theta = (1 - \\cos 2\\theta)/2$ es la herramienta "
            "clave para **integrar potencias pares** de seno o coseno en cálculo. Sin ella, $\\int \\sin^2 x\\, dx$ "
            "es difícil; con ella se reduce a $\\int (1 - \\cos 2x)/2\\, dx$, que es elemental."
        )),

        fig(
            "Diagrama del círculo unitario con dos ángulos A y B marcados, y el ángulo suma A + B también marcado. "
            "Triángulos auxiliares dibujados que ilustran la deducción geométrica de las fórmulas de suma. "
            "Etiquetas: 'sin(A+B) = sin A cos B + cos A sin B' destacada al lado. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\cos(A + B) = $",
                  "opciones_md": [
                      "$\\cos A + \\cos B$",
                      "$\\cos A \\cos B + \\sin A \\sin B$",
                      "**$\\cos A \\cos B - \\sin A \\sin B$**",
                      "$\\sin A \\cos B - \\cos A \\sin B$",
                  ],
                  "correcta": "C",
                  "pista_md": "Coseno 'invierte' la operación.",
                  "explicacion_md": "Suma de ángulos para coseno cambia signo entre los productos.",
              },
              {
                  "enunciado_md": "$\\sin 2 \\theta = $",
                  "opciones_md": [
                      "$2 \\sin \\theta$",
                      "$\\sin^2 \\theta$",
                      "**$2 \\sin \\theta \\cos \\theta$**",
                      "$1 - \\cos 2 \\theta$",
                  ],
                  "correcta": "C",
                  "pista_md": "Caso especial de suma con $A = B$.",
                  "explicacion_md": "Fórmula del ángulo doble del seno.",
              },
              {
                  "enunciado_md": "$\\cos^2 \\theta = $",
                  "opciones_md": [
                      "$1 - \\sin^2 \\theta$",
                      "**$(1 + \\cos 2\\theta)/2$**",
                      "Ambas",
                      "$\\cos 2\\theta$",
                  ],
                  "correcta": "C",
                  "pista_md": "Las dos son ciertas (las dos opciones).",
                  "explicacion_md": "Pitagórica y reducción de potencia, ambas válidas.",
              },
          ]),

        ej(
            "Calcular exacto",
            "Halla el valor exacto de $\\cos 75^\\circ$.",
            ["Usar $75 = 45 + 30$."],
            (
                "$\\cos 75^\\circ = \\cos(45 + 30) = \\cos 45 \\cos 30 - \\sin 45 \\sin 30 = (\\sqrt 2/2)(\\sqrt 3/2) - (\\sqrt 2/2)(1/2) = (\\sqrt 6 - \\sqrt 2)/4$."
            ),
        ),

        ej(
            "Ángulo doble desde una razón",
            "Si $\\cos \\theta = -1/3$ y $\\theta$ está en cuadrante II, halla $\\sin 2\\theta$.",
            ["Hallar $\\sin \\theta$ con pitagórica + signo del cuadrante."],
            (
                "$\\sin^2 \\theta = 1 - 1/9 = 8/9$, $\\sin \\theta = +\\sqrt{8}/3 = 2\\sqrt 2/3$ (II positivo). "
                "$\\sin 2\\theta = 2 \\cdot (2\\sqrt 2/3) \\cdot (-1/3) = -4\\sqrt 2/9$."
            ),
        ),

        ej(
            "Reducción de potencia",
            "Reescribí $\\sin^4 x$ usando solo $\\cos$ de ángulos múltiplos.",
            ["Aplicar reducción dos veces."],
            (
                "$\\sin^4 x = (\\sin^2 x)^2 = ((1 - \\cos 2x)/2)^2 = (1 - 2\\cos 2x + \\cos^2 2x)/4$. "
                "Reducir $\\cos^2 2x = (1 + \\cos 4x)/2$. Sustituyendo: $\\sin^4 x = (3 - 4\\cos 2x + \\cos 4x)/8$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir el signo en $\\cos(A + B)$.** Es $-$, no $+$.",
              "**Olvidar el signo $\\pm$ en ángulo mitad** y elegirlo según el cuadrante.",
              "**Aplicar fórmula de suma para multiplicación:** $\\sin(A B) \\neq$ ninguna fórmula simple — solo $\\sin(A + B)$ tiene fórmula.",
              "**Usar $\\cos 2\\theta = 2 \\cos \\theta - 1$.** **Falso.** La correcta es $2 \\cos^2 \\theta - 1$ (con cuadrado).",
              "**Confundir 'ángulo doble' ($2\\theta$) con 'el doble del seno' ($2 \\sin \\theta$).** Cosas distintas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Suma/resta:** $\\sin(A \\pm B), \\cos(A \\pm B), \\tan(A \\pm B)$ — claves para ángulos no estándar.",
              "**Ángulo doble:** $\\sin 2\\theta, \\cos 2\\theta$ (3 versiones), $\\tan 2\\theta$.",
              "**Reducción de potencia:** $\\sin^2 \\theta = (1 - \\cos 2\\theta)/2$, $\\cos^2 \\theta = (1 + \\cos 2\\theta)/2$.",
              "**Ángulo mitad:** $\\sin(u/2), \\cos(u/2), \\tan(u/2)$ con signo según cuadrante.",
              "**Producto-suma y suma-producto:** convierten productos en sumas y viceversa.",
              "**Próxima lección:** resolver ecuaciones trigonométricas usando estas herramientas.",
          ]),
    ]
    return {
        "id": "lec-prec-6-2-formulas",
        "title": "Fórmulas trigonométricas",
        "description": "Fórmulas de suma y resta de ángulos para sin, cos, tan. Identidades de ángulo doble y mitad. Fórmulas de reducción de potencia y producto-suma / suma-producto. Cálculo de valores exactos de ángulos no estándar.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# =====================================================================
# Ecuaciones trigonométricas
# =====================================================================
def lesson_ecuaciones_trig():
    blocks = [
        b("texto", body_md=(
            "Una **ecuación trigonométrica** es aquella en la que la incógnita aparece dentro de una "
            "función trigonométrica. La diferencia esencial respecto a las ecuaciones algebraicas: por la "
            "**periodicidad** de las funciones trigonométricas, una ecuación puede tener **infinitas "
            "soluciones**.\n\n"
            "$$\\sin x = 1/2 \\;\\Rightarrow\\; x = \\pi/6, 5\\pi/6, \\pi/6 + 2\\pi, 5\\pi/6 + 2\\pi, \\ldots$$\n\n"
            "Por eso siempre conviene distinguir:\n\n"
            "- **Soluciones en un período fundamental** (típicamente $[0, 2\\pi)$).\n"
            "- **Solución general** (todas, parametrizadas por un entero $n$).\n\n"
            "**Al terminar:**\n\n"
            "- Resolvés ecuaciones trigonométricas básicas usando inversas y simetrías.\n"
            "- Manejás ecuaciones **cuadráticas** y **factorizables** en $\\sin, \\cos, \\tan$.\n"
            "- Aplicás **identidades** para reducir ecuaciones complejas a casos básicos.\n"
            "- Distinguís **soluciones en un intervalo** vs **solución general**."
        )),

        formulas(
            titulo="Soluciones generales de ecuaciones básicas",
            body=(
                "**$\\sin x = c$** con $|c| \\leq 1$:\n\n"
                "$$x = \\arcsin c + 2\\pi n \\qquad \\text{o} \\qquad x = \\pi - \\arcsin c + 2\\pi n, \\quad n \\in \\mathbb{Z}.$$\n\n"
                "**$\\cos x = c$** con $|c| \\leq 1$:\n\n"
                "$$x = \\pm \\arccos c + 2\\pi n, \\quad n \\in \\mathbb{Z}.$$\n\n"
                "**$\\tan x = c$** (cualquier $c$):\n\n"
                "$$x = \\arctan c + \\pi n, \\quad n \\in \\mathbb{Z}.$$\n\n"
                "**Casos sin solución:**\n\n"
                "- $\\sin x = c$ o $\\cos x = c$ con $|c| > 1$: **sin soluciones**.\n"
                "- $\\sec x = c$ o $\\csc x = c$ con $|c| < 1$: sin soluciones (rango es $|y| \\geq 1$)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Ecuación básica",
          problema_md="Resuelve $\\sin x = \\dfrac{1}{2}$ en $[0, 2\\pi)$ y da la solución general.",
          pasos=[
              {"accion_md": (
                  "**Soluciones en $[0, 2\\pi)$.** $\\arcsin(1/2) = \\pi/6$. La otra solución del seno positivo está en cuadrante II: $\\pi - \\pi/6 = 5\\pi/6$.\n\n"
                  "**Soluciones en $[0, 2\\pi)$:** $x = \\pi/6$ y $x = 5\\pi/6$."
              ),
               "justificacion_md": "El seno tiene dos preimágenes en $[0, 2\\pi)$ (en I y II) por simetría.",
               "es_resultado": False},
              {"accion_md": (
                  "**Solución general:** $x = \\pi/6 + 2\\pi n$ o $x = 5\\pi/6 + 2\\pi n$, $n \\in \\mathbb{Z}$."
              ),
               "justificacion_md": "Sumar el período $2\\pi$ tantas veces como se quiera.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Tipos de ecuaciones y estrategias",
            body=(
                "**Tipo 1 — Lineal en una función trig:** $a \\sin x + b = 0$, $\\tan x = c$, etc. Aislar y aplicar inversa.\n\n"
                "**Tipo 2 — Cuadrática (sustituir $u = \\sin x$ etc.):** $a \\sin^2 x + b \\sin x + c = 0$. "
                "Sustituir, resolver cuadrática en $u$, descartar $|u| > 1$, volver a $x$.\n\n"
                "**Tipo 3 — Factorizable:** $a \\sin x \\cos x + b \\cos x = 0 \\Rightarrow \\cos x (a \\sin x + b) = 0$. "
                "Aplicar **propiedad del producto cero**.\n\n"
                "**Tipo 4 — Requiere identidad:** $\\sin 2x = \\cos x$, $1 + \\sin x = 2 \\cos^2 x$. Reducir todo a la misma función trig usando identidades, después aplicar tipo 1, 2 o 3.\n\n"
                "**Tipo 5 — Múltiplos de ángulo:** $\\sin 3x = 1$. Resolver para el múltiplo, luego dividir."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Cuadrática en cos",
          problema_md="Resuelve $2 \\cos^2 x - 7 \\cos x + 3 = 0$.",
          pasos=[
              {"accion_md": (
                  "**Sustituir $u = \\cos x$:** $2 u^2 - 7 u + 3 = 0$. **Factorizar:** $(2 u - 1)(u - 3) = 0$."
              ),
               "justificacion_md": "Buscar dos números con suma 7 y producto 6.",
               "es_resultado": False},
              {"accion_md": (
                  "**Soluciones:** $u = 1/2$ o $u = 3$. **Descartar $u = 3$** (porque $|\\cos x| \\leq 1$).\n\n"
                  "Volver: $\\cos x = 1/2$."
              ),
               "justificacion_md": "Filtrar soluciones extrañas.",
               "es_resultado": False},
              {"accion_md": (
                  "**Soluciones de $\\cos x = 1/2$:** $x = \\pm \\pi/3 + 2\\pi n$.\n\n"
                  "En $[0, 2\\pi)$: $x = \\pi/3$ y $x = 5\\pi/3$."
              ),
               "justificacion_md": "Coseno positivo en cuadrantes I y IV.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Factorizable",
          problema_md="Resuelve $5 \\sin x \\cos x + 4 \\cos x = 0$ en $[0, 2\\pi)$.",
          pasos=[
              {"accion_md": (
                  "**Factorizar $\\cos x$:** $\\cos x (5 \\sin x + 4) = 0$.\n\n"
                  "**Producto cero:** $\\cos x = 0$ o $5 \\sin x + 4 = 0$."
              ),
               "justificacion_md": "Sin factorizar, el método sería más complejo.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\cos x = 0$ en $[0, 2\\pi)$:** $x = \\pi/2$ y $x = 3\\pi/2$.\n\n"
                  "**$\\sin x = -4/5$:** $x = \\arcsin(-4/5) \\approx -0{,}927$ rad. Coterminal en $[0, 2\\pi)$: $\\approx 5{,}356$ rad. Otra solución (sen negativo en III): $\\pi + 0{,}927 \\approx 4{,}069$ rad.\n\n"
                  "**Soluciones:** $x \\in \\{\\pi/2, 3\\pi/2, 4{,}069, 5{,}356\\}$ aproximadamente."
              ),
               "justificacion_md": "Las dos primeras son exactas; las otras dos numéricas.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Con identidad",
          problema_md="Resuelve $\\sin 2x = \\cos x$ en $[0, 2\\pi)$.",
          pasos=[
              {"accion_md": (
                  "**Aplicar ángulo doble:** $\\sin 2x = 2 \\sin x \\cos x$. La ecuación queda $2 \\sin x \\cos x = \\cos x$."
              ),
               "justificacion_md": "Reducir a una sola función trig si es posible.",
               "es_resultado": False},
              {"accion_md": (
                  "**Llevar todo a un lado y factorizar:** $\\cos x (2 \\sin x - 1) = 0$.\n\n"
                  "**Producto cero:** $\\cos x = 0$ o $\\sin x = 1/2$."
              ),
               "justificacion_md": "**No** dividir por $\\cos x$ — perderías soluciones.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\cos x = 0$:** $x = \\pi/2, 3\\pi/2$.\n\n"
                  "**$\\sin x = 1/2$:** $x = \\pi/6, 5\\pi/6$.\n\n"
                  "**Soluciones:** $x \\in \\{\\pi/6, \\pi/2, 5\\pi/6, 3\\pi/2\\}$."
              ),
               "justificacion_md": "Cuatro soluciones en el intervalo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Múltiplo de ángulo",
          problema_md="Resuelve $2 \\sin 3x - 1 = 0$ en $[0, 2\\pi)$.",
          pasos=[
              {"accion_md": (
                  "**Aislar:** $\\sin 3x = 1/2$.\n\n"
                  "**Soluciones generales para $3x$:** $3x = \\pi/6 + 2\\pi n$ o $3x = 5\\pi/6 + 2\\pi n$."
              ),
               "justificacion_md": "Resolver primero para $3x$, después dividir.",
               "es_resultado": False},
              {"accion_md": (
                  "**Despejar $x$:** $x = \\pi/18 + 2\\pi n/3$ o $x = 5\\pi/18 + 2\\pi n/3$."
              ),
               "justificacion_md": "Dividir por 3 (por el coeficiente del ángulo).",
               "es_resultado": False},
              {"accion_md": (
                  "**Filtrar en $[0, 2\\pi)$.** Probar $n = 0, 1, 2$:\n\n"
                  "Primera familia: $\\pi/18, \\pi/18 + 2\\pi/3 = 13\\pi/18, \\pi/18 + 4\\pi/3 = 25\\pi/18$.\n"
                  "Segunda familia: $5\\pi/18, 5\\pi/18 + 2\\pi/3 = 17\\pi/18, 5\\pi/18 + 4\\pi/3 = 29\\pi/18$.\n\n"
                  "**Total: 6 soluciones.** Tiene sentido — multiplicar el ángulo por 3 da 3 veces más soluciones."
              ),
               "justificacion_md": "Con multiplicador $k$ del ángulo, hay $k$ veces más soluciones por período.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué hay infinitas soluciones.** $\\sin, \\cos$ tienen período $2\\pi$. Cualquier solución "
            "$x_0$ de $\\sin x = c$ produce **infinitas** soluciones $x_0 + 2\\pi n$. Por eso siempre hay que "
            "indicar **todas** (solución general) o **restringir** a un intervalo.\n\n"
            "**Por qué nunca dividir por $\\cos x$ (u otra función trig).** Al dividir, se asume que $\\cos x \\neq 0$ "
            "— pero $\\cos x = 0$ podría ser solución, y la perderíamos. Mejor: **mover todo a un lado y factorizar**.\n\n"
            "**Múltiplos de ángulo y cantidad de soluciones.** $\\sin(k x) = c$ tiene $2 k$ soluciones en "
            "$[0, 2\\pi)$ (cuando $|c| \\leq 1$ y $c \\neq \\pm 1$), porque al cambiar $x$ en $2\\pi$, "
            "$k x$ cambia en $2 \\pi k$, así hay $k$ veces más ciclos."
        )),

        fig(
            "Gráfica de y = sin x en color teal #06b6d4 sobre [0, 2π], con la recta horizontal y = 1/2 en color ámbar #f59e0b. "
            "Dos puntos de intersección destacados con círculos negros: (π/6, 1/2) y (5π/6, 1/2). "
            "Líneas verticales punteadas desde cada punto hasta el eje x con etiquetas de las coordenadas. "
            "Eje x con marcas en 0, π/6, π/2, 5π/6, π, 3π/2, 2π. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\sin x = -1$ tiene como soluciones generales:",
                  "opciones_md": [
                      "$x = -\\pi + 2\\pi n$",
                      "**$x = 3\\pi/2 + 2\\pi n$**",
                      "$x = \\pi + \\pi n$",
                      "Sin solución",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\sin = -1$ solo en un punto del período.",
                  "explicacion_md": "Mínimo del seno está en $3\\pi/2$. Sumar $2\\pi n$.",
              },
              {
                  "enunciado_md": "$2 \\cos^2 x = 1$ implica $\\cos x = $",
                  "opciones_md": [
                      "$\\pm 1/2$",
                      "**$\\pm \\sqrt{2}/2$**",
                      "$\\pm \\sqrt{3}/2$",
                      "Sin solución real",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\cos^2 x = 1/2 \\Rightarrow \\cos x = \\pm 1/\\sqrt{2}$.",
                  "explicacion_md": "Tomar raíz cuadrada con $\\pm$.",
              },
              {
                  "enunciado_md": "Al resolver $\\sin x \\cos x = 0$, hay que:",
                  "opciones_md": [
                      "Dividir por $\\cos x$",
                      "**Aplicar producto cero: $\\sin x = 0$ o $\\cos x = 0$**",
                      "Sumar a ambos lados",
                      "Aplicar pitagórica",
                  ],
                  "correcta": "B",
                  "pista_md": "No dividir cuando puede ser cero.",
                  "explicacion_md": "Producto cero da dos casos.",
              },
          ]),

        ej(
            "Lineal",
            "Resuelve $2 \\sin x + 1 = 0$ en $[0, 2\\pi)$.",
            ["$\\sin x = -1/2$, ángulos en III y IV."],
            (
                "$\\sin x = -1/2$. En III: $\\pi + \\pi/6 = 7\\pi/6$. En IV: $2\\pi - \\pi/6 = 11\\pi/6$. **Soluciones:** $7\\pi/6, 11\\pi/6$."
            ),
        ),

        ej(
            "Cuadrática con identidad",
            "Resuelve $1 + \\sin x = 2 \\cos^2 x$ en $[0, 2\\pi)$.",
            ["Reescribir $\\cos^2 = 1 - \\sin^2$ y obtener cuadrática en $\\sin$."],
            (
                "$1 + \\sin x = 2(1 - \\sin^2 x) = 2 - 2 \\sin^2 x \\Rightarrow 2 \\sin^2 x + \\sin x - 1 = 0$. "
                "Factorizar: $(2 \\sin x - 1)(\\sin x + 1) = 0 \\Rightarrow \\sin x = 1/2$ o $\\sin x = -1$.\n\n"
                "Soluciones: $x = \\pi/6, 5\\pi/6, 3\\pi/2$."
            ),
        ),

        ej(
            "Múltiplo de ángulo",
            "Resuelve $\\cos 2x = -1/2$ en $[0, 2\\pi)$.",
            ["Resolver para $2x$ primero, después dividir."],
            (
                "$\\cos 2x = -1/2 \\Rightarrow 2x = \\pm 2\\pi/3 + 2\\pi n$, así $x = \\pm \\pi/3 + \\pi n$. "
                "En $[0, 2\\pi)$: $x = \\pi/3, 2\\pi/3, 4\\pi/3, 5\\pi/3$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar la solución general** y dar solo una solución.",
              "**Dividir por una función trig que puede valer cero**, perdiendo soluciones.",
              "**Aceptar soluciones de la cuadrática que están fuera del rango.** Por ejemplo, $\\cos x = 3$ no tiene solución.",
              "**Confundir 'soluciones en $[0, 2\\pi)$' con 'solución general':** son dos cosas distintas.",
              "**Dividir por $k$ al final sin agregar el $2\\pi/k$ apropiado:** la familia de soluciones no es única.",
          ]),

        b("resumen",
          puntos_md=[
              "**Periodicidad:** las ecuaciones trigonométricas tienen infinitas soluciones.",
              "**Solución general** se escribe con $2\\pi n$ (o $\\pi n$ para tan).",
              "**Tipos de ecuaciones:** lineales, cuadráticas (sustituir), factorizables (producto cero), con identidades, con múltiplos de ángulo.",
              "**Estrategia universal:** llevar todo a un lado, factorizar, aplicar producto cero, resolver cada caso.",
              "**Próxima lección:** un sistema de coordenadas alternativo — coordenadas polares.",
          ]),
    ]
    return {
        "id": "lec-prec-6-3-ecuaciones-trigonometricas",
        "title": "Ecuaciones trigonométricas",
        "description": "Resolución de ecuaciones trigonométricas: lineales, cuadráticas (sustitución), factorizables (producto cero), con identidades y con múltiplos de ángulo. Distinción entre soluciones en un intervalo y solución general.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 3,
    }


# =====================================================================
# Coordenadas polares
# =====================================================================
def lesson_coordenadas_polares():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora hemos localizado puntos en el plano usando **coordenadas cartesianas** $(x, y)$ — "
            "distancias horizontal y vertical desde el origen. Pero hay otro sistema, más natural para "
            "muchas situaciones que involucran **rotaciones** o **simetrías circulares**: las "
            "**coordenadas polares**.\n\n"
            "En coordenadas polares un punto se identifica con un par $(r, \\theta)$:\n\n"
            "- $r$ es la **distancia** al origen (llamado **polo**).\n"
            "- $\\theta$ es el **ángulo** desde el eje polar (que coincide con el eje $x$ positivo) hasta el punto, en sentido antihorario.\n\n"
            "**Aplicaciones clásicas:** radar, satélites, ondas circulares, espirales, posicionamiento angular en máquinas.\n\n"
            "**Al terminar:**\n\n"
            "- Identificás un punto en coordenadas polares $(r, \\theta)$.\n"
            "- Convertís entre coordenadas polares y cartesianas.\n"
            "- Trabajás con la **no unicidad** de la representación polar (varias formas para el mismo punto).\n"
            "- Conviertes ecuaciones entre los dos sistemas."
        )),

        b("definicion",
          titulo="Sistema polar",
          body_md=(
              "En el sistema polar:\n\n"
              "- El **polo** es el origen del sistema (equivalente al $(0, 0)$ cartesiano).\n"
              "- El **eje polar** es una semirrecta horizontal que sale del polo hacia la derecha (equivale al semieje $x$ positivo).\n"
              "- Un punto $P$ se representa con el par **$(r, \\theta)$**:\n"
              "  - $r$ = distancia desde $P$ al polo.\n"
              "  - $\\theta$ = ángulo (en radianes o grados) entre el eje polar y la semirrecta $\\overrightarrow{O P}$, medido en sentido antihorario.\n\n"
              "**Convención de signos:**\n\n"
              "- $r > 0$: distancia normal.\n"
              "- $r < 0$: el punto está en la **dirección opuesta** del ángulo $\\theta$ (lo veremos en ejemplos).\n"
              "- $\\theta$ puede ser cualquier real (positivo, negativo, mayor a $2\\pi$).\n\n"
              "**No unicidad.** Un mismo punto tiene **infinitas representaciones polares**:\n\n"
              "- $(r, \\theta) = (r, \\theta + 2\\pi n)$ para todo $n \\in \\mathbb{Z}$.\n"
              "- $(r, \\theta) = (-r, \\theta + \\pi)$.\n\n"
              "**Caso especial:** el polo $(0, 0)$ se representa como $(0, \\theta)$ para **cualquier** $\\theta$."
          )),

        formulas(
            titulo="Conversión entre polar y cartesiano",
            body=(
                "**De polar a cartesiano:**\n\n"
                "$$\\boxed{\\,x = r \\cos \\theta, \\qquad y = r \\sin \\theta.\\,}$$\n\n"
                "Estas fórmulas se obtienen directamente del triángulo rectángulo formado por el punto, el polo y el pie de su perpendicular al eje polar.\n\n"
                "**De cartesiano a polar:**\n\n"
                "$$r = \\sqrt{x^2 + y^2}, \\qquad \\tan \\theta = \\dfrac{y}{x} \\quad (x \\neq 0).$$\n\n"
                "**Atención al cuadrante** al calcular $\\theta = \\arctan(y/x)$:\n\n"
                "- Cuadrante I ($x > 0, y \\geq 0$): $\\theta = \\arctan(y/x)$.\n"
                "- Cuadrante II ($x < 0, y > 0$): $\\theta = \\pi + \\arctan(y/x)$.\n"
                "- Cuadrante III ($x < 0, y < 0$): $\\theta = \\pi + \\arctan(y/x)$.\n"
                "- Cuadrante IV ($x > 0, y < 0$): $\\theta = 2\\pi + \\arctan(y/x)$ o $\\arctan(y/x)$ negativo.\n\n"
                "Muchas calculadoras y librerías ofrecen `atan2(y, x)` que da $\\theta$ correctamente en todos los cuadrantes."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Polar a cartesiano",
          problema_md="Convierte el punto polar $(r, \\theta) = (4, \\pi/3)$ a cartesiano.",
          pasos=[
              {"accion_md": (
                  "**Aplicar fórmulas:** $x = 4 \\cos(\\pi/3) = 4 \\cdot 1/2 = 2$. $y = 4 \\sin(\\pi/3) = 4 \\cdot \\sqrt{3}/2 = 2\\sqrt{3}$."
              ),
               "justificacion_md": "Valores exactos del seno/coseno.",
               "es_resultado": False},
              {"accion_md": "**Punto cartesiano:** $(2, 2\\sqrt{3})$.",
               "justificacion_md": "Está en cuadrante I ✓ (consistente con $\\pi/3$).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cartesiano a polar",
          problema_md="Convierte el punto $(-1, \\sqrt{3})$ a polar.",
          pasos=[
              {"accion_md": (
                  "**$r$:** $r = \\sqrt{(-1)^2 + (\\sqrt{3})^2} = \\sqrt{1 + 3} = 2$."
              ),
               "justificacion_md": "Distancia al origen.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\theta$:** punto en cuadrante II ($x < 0, y > 0$). $\\arctan(y/x) = \\arctan(\\sqrt{3}/(-1)) = \\arctan(-\\sqrt{3}) = -\\pi/3$. Sumar $\\pi$ (cuadrante II): $\\theta = 2\\pi/3$."
              ),
               "justificacion_md": "Ajustar por cuadrante.",
               "es_resultado": False},
              {"accion_md": "**Punto polar:** $(2, 2\\pi/3)$.",
               "justificacion_md": "Verificar: $2 \\cos(2\\pi/3) = -1$, $2 \\sin(2\\pi/3) = \\sqrt 3$. ✓",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Conversión de ecuaciones",
          body_md=(
              "Las ecuaciones de curvas se pueden expresar en cualquiera de los dos sistemas. Las "
              "**conversiones de ecuaciones** son útiles para reconocer formas conocidas:\n\n"
              "**Sustituciones útiles:**\n\n"
              "- $x = r \\cos \\theta$, $y = r \\sin \\theta$.\n"
              "- $x^2 + y^2 = r^2$.\n"
              "- $\\tan \\theta = y/x$.\n\n"
              "**Ejemplos famosos:**\n\n"
              "| Cartesiana | Polar | Forma |\n"
              "|---|---|---|\n"
              "| $x^2 + y^2 = a^2$ | $r = a$ | Circunferencia centrada en origen |\n"
              "| $y = m x$ | $\\theta = \\arctan m$ (constante) | Recta por origen |\n"
              "| $x = a$ | $r \\cos \\theta = a$ | Recta vertical |\n"
              "| $y = a$ | $r \\sin \\theta = a$ | Recta horizontal |\n"
              "| $x^2 + y^2 = 2 a x$ | $r = 2 a \\cos \\theta$ | Circunferencia tangente a eje y |\n\n"
              "**Truco general:** algunas curvas tienen ecuación **mucho más simple** en polar que en cartesiano (las espirales, rosas, cardioides — próxima lección)."
          )),

        b("ejemplo_resuelto",
          titulo="Convertir ecuación a polar",
          problema_md="Convierte la ecuación cartesiana $x^2 + y^2 = 4 x$ a polar.",
          pasos=[
              {"accion_md": (
                  "**Sustituir.** $x^2 + y^2 = r^2$, $x = r \\cos \\theta$. Quedando $r^2 = 4 r \\cos \\theta$."
              ),
               "justificacion_md": "Reemplazar las identidades.",
               "es_resultado": False},
              {"accion_md": (
                  "**Simplificar.** Dividir por $r$ (asumiendo $r \\neq 0$, que coincide con el polo): $r = 4 \\cos \\theta$."
              ),
               "justificacion_md": "El polo $r = 0$ ya satisface $r = 4 \\cos(\\pi/2) = 0$, no se pierde nada.",
               "es_resultado": False},
              {"accion_md": (
                  "**Reconocer.** $r = 4 \\cos \\theta$ es una **circunferencia** de diámetro 4 con centro en $(2, 0)$ (cartesiano), tangente al eje $y$ en el origen."
              ),
               "justificacion_md": "La forma $r = 2 a \\cos \\theta$ corresponde a esta familia.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Cuándo usar polares.** Cuando el problema tiene **simetría circular** (un círculo, una "
            "espiral, un radar): las polares simplifican enormemente. Cuando el problema tiene "
            "**simetría rectangular** (rectángulos, paralelos, ejes principales): cartesianas son mejores.\n\n"
            "**Ejemplo concreto.** La ecuación $x^2 + y^2 = 1$ (circunferencia unitaria) en polares es "
            "simplemente $r = 1$ — mucho más limpia.\n\n"
            "**Por qué $r$ puede ser negativo.** Es una convención que extiende el sistema. $(2, \\pi/3)$ y "
            "$(-2, 4\\pi/3)$ son el mismo punto. Útil para describir ciertas curvas (rosas, cardioides) "
            "donde $r$ cambia de signo a lo largo del recorrido."
        )),

        fig(
            "Sistema de coordenadas polares con polo (origen) marcado y eje polar (semirrecta horizontal hacia derecha). "
            "Un punto P en cuadrante I con dos representaciones simultáneas: en color teal #06b6d4 sus coordenadas polares (r, θ) con r marcado como segmento radial y θ marcado como arco de ángulo desde el eje polar; "
            "en color ámbar #f59e0b sus coordenadas cartesianas (x, y) con x e y marcados como proyecciones sobre los ejes. "
            "Etiquetas claras: 'x = r cos θ', 'y = r sin θ', 'r = √(x² + y²)'. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El punto polar $(r, \\theta) = (3, \\pi/2)$ en cartesiano es:",
                  "opciones_md": [
                      "$(3, 0)$",
                      "**$(0, 3)$**",
                      "$(\\pi/2, 3)$",
                      "$(0, \\pi/2)$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\pi/2$ apunta hacia arriba (eje $y$ positivo).",
                  "explicacion_md": "$x = 3 \\cos(\\pi/2) = 0, y = 3 \\sin(\\pi/2) = 3$.",
              },
              {
                  "enunciado_md": "La ecuación cartesiana $x^2 + y^2 = 9$ en polar es:",
                  "opciones_md": [
                      "$r = 9$",
                      "**$r = 3$**",
                      "$\\theta = 3$",
                      "$r = \\sqrt 9$",
                  ],
                  "correcta": "B",
                  "pista_md": "$r^2 = 9 \\Rightarrow r = 3$.",
                  "explicacion_md": "Circunferencia de radio 3 centrada en origen.",
              },
              {
                  "enunciado_md": "Un punto polar $(r, \\theta)$ es equivalente a:",
                  "opciones_md": [
                      "$(r, \\theta + \\pi)$",
                      "**$(-r, \\theta + \\pi)$**",
                      "$(-r, \\theta)$",
                      "$(r, -\\theta)$",
                  ],
                  "correcta": "B",
                  "pista_md": "$r$ negativo apunta en dirección opuesta.",
                  "explicacion_md": "Cambiar signo de $r$ y sumar $\\pi$ devuelve al mismo punto.",
              },
          ]),

        ej(
            "Convertir punto",
            "Convierte $(r, \\theta) = (2, 5\\pi/6)$ a cartesiano.",
            ["Aplicar fórmulas con valores exactos."],
            (
                "$x = 2 \\cos(5\\pi/6) = 2 \\cdot (-\\sqrt 3/2) = -\\sqrt 3$. $y = 2 \\sin(5\\pi/6) = 2 \\cdot 1/2 = 1$. **$(-\\sqrt 3, 1)$.**"
            ),
        ),

        ej(
            "Cartesiano a polar",
            "Convierte $(0, -4)$ a polar (forma con $r > 0$ y $\\theta \\in [0, 2\\pi)$).",
            ["Sobre el eje $y$ negativo."],
            (
                "$r = 4$. Apunta en dirección del eje $y$ negativo: $\\theta = 3\\pi/2$. **$(4, 3\\pi/2)$.**"
            ),
        ),

        ej(
            "Convertir ecuación",
            "Convierte $r = 6 \\sin \\theta$ a cartesiano e identifica.",
            ["Multiplicar por $r$ y sustituir."],
            (
                "Multiplicar por $r$: $r^2 = 6 r \\sin \\theta \\Rightarrow x^2 + y^2 = 6 y$. Reordenar: $x^2 + y^2 - 6 y = 0$. Completar cuadrados: $x^2 + (y - 3)^2 = 9$. **Circunferencia** de radio 3 centrada en $(0, 3)$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Asumir que un punto polar tiene representación única.** Hay infinitas.",
              "**Olvidar el cuadrante** al calcular $\\theta$ con arctan. Usar `atan2` o ajustar.",
              "**Confundir $r$ y $\\theta$ en el par $(r, \\theta)$.** $r$ va primero.",
              "**Pensar que $\\theta$ es un ángulo entre 0° y 360° solamente.** Puede ser cualquier real (con identificación módulo $2\\pi$).",
              "**Dividir por $r$ sin considerar $r = 0$.** A veces el polo es solución legítima.",
          ]),

        b("resumen",
          puntos_md=[
              "**Coordenadas polares** $(r, \\theta)$: distancia al polo y ángulo desde el eje polar.",
              "**Conversión:** $x = r \\cos \\theta, y = r \\sin \\theta$. Inversa con $r = \\sqrt{x^2 + y^2}$ y $\\theta$ ajustado por cuadrante.",
              "**No unicidad:** $(r, \\theta) \\equiv (r, \\theta + 2\\pi n) \\equiv (-r, \\theta + \\pi)$.",
              "**Aplicación:** ecuaciones más simples para curvas con simetría circular.",
              "**Próxima lección:** familias clásicas de **curvas en coordenadas polares**.",
          ]),
    ]
    return {
        "id": "lec-prec-6-4-coordenadas-polares",
        "title": "Coordenadas polares",
        "description": "Sistema de coordenadas polares (r, θ): polo, eje polar, distancia y ángulo. Conversiones entre polar y cartesiano. No unicidad de la representación. Conversión de ecuaciones entre sistemas.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# Curvas en coordenadas polares
# =====================================================================
def lesson_curvas_polares():
    blocks = [
        b("texto", body_md=(
            "Algunas curvas tienen una **forma muy simple en coordenadas polares** y muy complicada en "
            "cartesianas. Esta lección presenta las **familias clásicas** de curvas polares: rectas, "
            "circunferencias, cardioides, rosas, espirales, lemniscatas y limaçones.\n\n"
            "**¿Cómo se grafican?** Una curva polar $r = f(\\theta)$ se traza calculando $r$ para varios "
            "valores de $\\theta$ y marcando los puntos $(r, \\theta)$. Como $\\theta$ recorre $[0, 2\\pi)$ (o "
            "más), el lápiz traza la curva.\n\n"
            "**Aplicaciones:** patrones de antenas, microscopía polar, diseño industrial, modelado de "
            "fenómenos con simetría rotacional.\n\n"
            "**Al terminar:**\n\n"
            "- Reconocés las familias principales: circunferencias polares, cardioides, rosas, lemniscatas, espirales.\n"
            "- Determinás la **simetría** de una curva polar (respecto al eje polar, al eje vertical o al polo).\n"
            "- Esbozás una curva polar a partir de su ecuación."
        )),

        formulas(
            titulo="Familias clásicas (catálogo)",
            body=(
                "**Circunferencias:**\n\n"
                "- $r = a$ (constante): circunferencia de radio $a$ centrada en el polo.\n"
                "- $r = 2 a \\cos \\theta$: circunferencia de diámetro $2a$ con centro en $(a, 0)$ (cartesiano), pasando por el polo.\n"
                "- $r = 2 a \\sin \\theta$: análoga, pero centro en $(0, a)$.\n\n"
                "**Rectas:**\n\n"
                "- $\\theta = \\theta_0$ (constante): recta por el polo con ese ángulo.\n"
                "- $r = a \\sec \\theta$ (es decir, $r \\cos \\theta = a$): recta vertical $x = a$.\n"
                "- $r = a \\csc \\theta$ (o $r \\sin \\theta = a$): recta horizontal $y = a$.\n\n"
                "**Cardioides** $r = a (1 + \\cos \\theta)$ o $r = a (1 + \\sin \\theta)$:\n\n"
                "- Forma de **corazón**.\n"
                "- Pasa por el polo cuando el coseno (o seno) vale $-1$.\n"
                "- Diámetro máximo: $2a$.\n\n"
                "**Limaçones (caracoles)** $r = a + b \\cos \\theta$ (o $\\sin$), $a, b > 0$:\n\n"
                "- $a < b$: con **bucle interior**.\n"
                "- $a = b$: cardioide.\n"
                "- $a > b$ pero $a < 2 b$: con 'hoyuelo' (no convexa).\n"
                "- $a \\geq 2 b$: convexa (ovoide).\n\n"
                "**Rosas** $r = a \\cos(n \\theta)$ o $r = a \\sin(n \\theta)$:\n\n"
                "- $n$ **impar:** $n$ pétalos.\n"
                "- $n$ **par:** $2n$ pétalos.\n\n"
                "**Lemniscatas** $r^2 = a^2 \\cos(2 \\theta)$ o $r^2 = a^2 \\sin(2 \\theta)$:\n\n"
                "- Forma de **'8' acostado** (figura $\\infty$).\n\n"
                "**Espirales:**\n\n"
                "- **Arquimedes** $r = a \\theta$: sucesivas vueltas equidistantes.\n"
                "- **Logarítmica** $r = a e^{b \\theta}$: las vueltas se separan exponencialmente.\n"
                "- **Hiperbólica** $r \\theta = a$: tiende al polo asintóticamente."
            ),
        ),

        formulas(
            titulo="Pruebas de simetría",
            body=(
                "Tres tipos de simetría a chequear:\n\n"
                "**Simetría respecto al eje polar (eje $x$):** la ecuación no cambia al reemplazar $\\theta$ por $-\\theta$ (o equivalentemente, $(r, \\theta)$ por $(r, -\\theta)$).\n\n"
                "**Simetría respecto al eje vertical ($\\theta = \\pi/2$):** la ecuación no cambia al reemplazar $\\theta$ por $\\pi - \\theta$.\n\n"
                "**Simetría respecto al polo (origen):** la ecuación no cambia al reemplazar $r$ por $-r$ (o $\\theta$ por $\\theta + \\pi$).\n\n"
                "**Ejemplos:**\n\n"
                "- $r = 2 \\cos \\theta$: como $\\cos$ es par, simétrica al **eje polar**.\n"
                "- $r = 2 \\sin \\theta$: simétrica al **eje vertical** (eje $y$).\n"
                "- $r^2 = 4 \\cos 2\\theta$ (lemniscata): simétrica al eje polar **y** al polo.\n"
                "- $r = \\theta$ (espiral arquimediana): no tiene simetrías obvias."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Esbozar una cardioide",
          problema_md="Esboza $r = 2 (1 + \\cos \\theta)$.",
          pasos=[
              {"accion_md": (
                  "**Tabla de valores notables:**\n\n"
                  "| $\\theta$ | $\\cos \\theta$ | $r$ |\n"
                  "|---|---|---|\n"
                  "| $0$ | $1$ | $4$ |\n"
                  "| $\\pi/2$ | $0$ | $2$ |\n"
                  "| $\\pi$ | $-1$ | $0$ |\n"
                  "| $3\\pi/2$ | $0$ | $2$ |"
              ),
               "justificacion_md": "Cinco puntos clave para guiar la forma.",
               "es_resultado": False},
              {"accion_md": (
                  "**Simetría:** simétrica al eje polar (porque $\\cos$ es par).\n\n"
                  "**Forma.** Empieza en $(4, 0)$, baja por arriba a $(2, \\pi/2)$, llega al polo en $\\theta = \\pi$, y por abajo regresa: $(2, 3\\pi/2), (4, 2\\pi)$. Forma de **corazón** apuntando hacia la derecha."
              ),
               "justificacion_md": "Cardioide clásica.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Rosa de 4 pétalos",
          problema_md="Esboza $r = 3 \\cos 2 \\theta$.",
          pasos=[
              {"accion_md": (
                  "**Reconocer rosa.** $r = a \\cos(n \\theta)$ con $n = 2$ par → **$2 n = 4$ pétalos**.\n\n"
                  "**Tamaño.** Cada pétalo tiene longitud máxima $|a| = 3$."
              ),
               "justificacion_md": "Catálogo.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cuándo $r = 0$:** $\\cos 2\\theta = 0 \\Rightarrow 2\\theta = \\pi/2 + k\\pi \\Rightarrow \\theta = \\pi/4 + k\\pi/2$. Es decir, $\\pi/4, 3\\pi/4, 5\\pi/4, 7\\pi/4$ — los 'cortes' entre pétalos.\n\n"
                  "**Cuándo $|r| = 3$ máximo:** $\\cos 2\\theta = \\pm 1 \\Rightarrow \\theta = 0, \\pi/2, \\pi, 3\\pi/2$ — los **centros** de los 4 pétalos.\n\n"
                  "**Forma:** una rosa con un pétalo apuntando en cada dirección de los ejes."
              ),
               "justificacion_md": "Estructura geométrica clara.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Espiral",
          problema_md="Esboza la espiral arquimediana $r = \\theta$ para $\\theta \\in [0, 4\\pi]$.",
          pasos=[
              {"accion_md": (
                  "**Tabla:**\n\n"
                  "| $\\theta$ | $r$ |\n"
                  "|---|---|\n"
                  "| $0$ | $0$ |\n"
                  "| $\\pi/2$ | $1{,}57$ |\n"
                  "| $\\pi$ | $3{,}14$ |\n"
                  "| $2\\pi$ | $6{,}28$ |\n"
                  "| $4\\pi$ | $12{,}57$ |"
              ),
               "justificacion_md": "$r$ crece linealmente con $\\theta$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Forma.** Espiral que se aleja del polo a velocidad constante. Cada vuelta de $2\\pi$ aleja al punto en $2\\pi \\approx 6{,}28$ unidades. Las vueltas son **equidistantes** entre sí."
              ),
               "justificacion_md": "Característica de la arquimediana.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué las rosas tienen $n$ o $2n$ pétalos.** Para $r = \\cos(n\\theta)$:\n\n"
            "- $n$ par: la curva se cierra cuando $\\theta$ recorre $[0, 2\\pi)$ una vez. En ese recorrido, $r$ "
            "pasa por $2n$ máximos positivos (un máximo cada $\\pi/n$), creando $2n$ pétalos.\n"
            "- $n$ impar: la mitad de los 'pétalos' se superponen con la otra mitad (porque $r < 0$ los proyecta "
            "al lado opuesto), dando solo $n$ pétalos visibles.\n\n"
            "**Cardioide y caracol.** La familia $r = a + b \\cos\\theta$ es muy versátil. La cardioide ($a = b$) "
            "es la frontera entre 'caracoles con bucle' ($a < b$) y 'caracoles sin bucle' ($a > b$).\n\n"
            "**Espirales en la naturaleza.** Las arquimedianas aparecen en el enrollado de mangueras o cuerdas. "
            "Las logarítmicas aparecen en conchas de caracol marinos, brazos de galaxias, y huracanes."
        )),

        fig(
            "Galería de curvas polares en una grilla 2x3. "
            "Panel 1: cardioide r = 1 + cos θ (forma de corazón apuntando a la derecha) en color teal #06b6d4. "
            "Panel 2: rosa de 3 pétalos r = sin 3θ en color ámbar #f59e0b. "
            "Panel 3: rosa de 4 pétalos r = cos 2θ en color púrpura. "
            "Panel 4: lemniscata r² = cos 2θ (figura 8 acostada) en color verde. "
            "Panel 5: espiral arquimediana r = θ en color naranja. "
            "Panel 6: limacón con bucle r = 1 + 2 cos θ en color rosa. "
            "Cada panel con sus ejes polares y etiqueta de la ecuación. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$r = 5$ representa:",
                  "opciones_md": [
                      "Una recta",
                      "**Una circunferencia centrada en el polo**",
                      "Una espiral",
                      "Un punto",
                  ],
                  "correcta": "B",
                  "pista_md": "Distancia constante al polo.",
                  "explicacion_md": "Todos los puntos a distancia 5 del polo forman una circunferencia.",
              },
              {
                  "enunciado_md": "$r = 2 \\sin 5\\theta$ tiene cuántos pétalos:",
                  "opciones_md": [
                      "$2$",
                      "**$5$**",
                      "$10$",
                      "$25$",
                  ],
                  "correcta": "B",
                  "pista_md": "$n = 5$ impar.",
                  "explicacion_md": "$n$ impar → $n$ pétalos.",
              },
              {
                  "enunciado_md": "Una espiral arquimediana tiene ecuación:",
                  "opciones_md": [
                      "$r = a^\\theta$",
                      "**$r = a \\theta$**",
                      "$r = a \\cos \\theta$",
                      "$r = a / \\theta$",
                  ],
                  "correcta": "B",
                  "pista_md": "$r$ proporcional a $\\theta$.",
                  "explicacion_md": "Distancia al polo crece linealmente con el ángulo.",
              },
          ]),

        ej(
            "Identificar curva",
            "¿Qué curva representa $r = 4 \\cos \\theta$?",
            ["$r = 2 a \\cos \\theta$ es circunferencia."],
            (
                "Circunferencia de diámetro 4, centrada en $(2, 0)$ cartesiano, tangente al eje $y$ en el origen."
            ),
        ),

        ej(
            "Pétalos de rosa",
            "Para $r = 3 \\cos 4\\theta$, indica número de pétalos y orientación de uno de ellos.",
            ["$n = 4$ par."],
            (
                "$2 n = 8$ pétalos. El primer máximo ocurre en $\\theta = 0$ ($r = 3$), así un pétalo apunta hacia el eje polar (a la derecha)."
            ),
        ),

        ej(
            "Simetría",
            "¿Qué simetrías tiene la lemniscata $r^2 = 4 \\cos 2 \\theta$?",
            ["Probar las tres."],
            (
                "Reemplazar $\\theta \\to -\\theta$: $\\cos(-2\\theta) = \\cos 2\\theta$, ecuación no cambia → simétrica al eje polar. "
                "Reemplazar $r \\to -r$: $r^2$ no cambia → simétrica al polo. Por composición, también respecto al eje vertical. **Las tres simetrías.**"
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir el número de pétalos** según paridad de $n$. Impar: $n$, par: $2 n$.",
              "**Pensar que toda curva polar tiene simetría.** Hay que verificar.",
              "**Olvidar el rango de $\\theta$ necesario** para trazar la curva completa. Algunas requieren más de $2 \\pi$ (espirales).",
              "**Confundir $r = a \\cos \\theta$ con $r = a$:** la primera es circunferencia que **pasa por el polo**, la segunda **está centrada en él**.",
              "**Aplicar fórmulas cartesianas a curvas polares directamente.** A veces conviene convertir, otras no.",
          ]),

        b("resumen",
          puntos_md=[
              "**Curvas básicas:** circunferencias ($r = a$, $r = 2a \\cos \\theta$), rectas, cardioides, limaçones, rosas, lemniscatas, espirales.",
              "**Rosas:** $r = a \\cos(n\\theta)$ tiene $n$ pétalos si $n$ impar, $2n$ si $n$ par.",
              "**Simetrías:** al eje polar ($\\theta \\to -\\theta$), al eje vertical ($\\theta \\to \\pi - \\theta$), al polo ($r \\to -r$).",
              "**Esbozo:** tabla de valores notables + simetría + reconocimiento de familia.",
              "**Cierre del capítulo:** dominamos la trigonometría analítica — identidades, fórmulas, ecuaciones, polares y curvas.",
              "**Próximo capítulo:** **números complejos** — extensión natural de los reales que aprovecha mucho de lo que vimos.",
          ]),
    ]
    return {
        "id": "lec-prec-6-5-curvas-polares",
        "title": "Curvas en coordenadas polares",
        "description": "Galería de curvas polares clásicas: circunferencias, cardioides, limaçones, rosas (con número de pétalos según paridad de n), lemniscatas y espirales (arquimediana, logarítmica). Pruebas de simetría.",
        "blocks": blocks,
        "duration_minutes": 50,
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

    chapter_id = "ch-prec-trig-analitica"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Trigonometría Analítica",
        "description": (
            "Identidades trigonométricas y técnicas para verificarlas. Fórmulas de suma/resta, ángulo doble, "
            "ángulo mitad y producto-suma. Resolución de ecuaciones trigonométricas. Sistema de coordenadas "
            "polares y galería de curvas polares clásicas."
        ),
        "order": 6,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_identidades,
        lesson_formulas,
        lesson_ecuaciones_trig,
        lesson_coordenadas_polares,
        lesson_curvas_polares,
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
        f"✅ Capítulo 6 — Trigonometría Analítica listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())


