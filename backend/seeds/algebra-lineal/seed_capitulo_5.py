"""
Seed del curso Álgebra Lineal — Capítulo 5: Espacios y Subespacios Vectoriales.
6 lecciones:
  5.1 Espacios vectoriales (axiomas, ejemplos, subespacios, Gen)
  5.2 Espacios notables (Nul A, Col A, núcleo y rango de TL)
  5.3 Bases (definición, teorema del conjunto generador, bases para Nul/Col)
  5.4 Sistemas de coordenadas (representación única, [x]_B, mapa de coordenadas)
  5.5 Dimensión y rango (dim V, dim Nul/Col, teorema del rango, TMI extendido)
  5.6 Cambio de coordenadas (matriz P_{C←B} y algoritmo [c|b]→[I|P])

Basado en los Apuntes/Clase de Se Remonta para cada lección.

Requiere que el curso 'algebra-lineal' ya exista (ver
seed_algebra_lineal_chapter_1.py). Idempotente.
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
# 5.1 Espacios vectoriales
# =====================================================================
def lesson_5_1():
    blocks = [
        b("texto", body_md=(
            "Hasta este capítulo, hemos hecho álgebra lineal **dentro de $\\mathbb{R}^n$**: vectores como "
            "n-tuplas, matrices, sistemas. En este capítulo damos el **gran salto a la abstracción**: "
            "un **espacio vectorial** es **cualquier conjunto** donde las operaciones de suma y producto "
            "por escalar se comporten como en $\\mathbb{R}^n$.\n\n"
            "**¿Por qué importa?** Esta abstracción nos permite tratar como 'vectores' a:\n\n"
            "- **Polinomios** de grado $\\leq n$ ($\\mathcal{P}_n$).\n"
            "- **Matrices** $m \\times n$ ($\\mathbb{R}^{m\\times n}$).\n"
            "- **Funciones continuas**, **soluciones de EDOs**, **señales**, etc.\n\n"
            "Toda la maquinaria del álgebra lineal (combinaciones lineales, independencia, bases, dimensión) "
            "se aplica idénticamente a estos contextos.\n\n"
            "Al terminar:\n\n"
            "- Conoces los **10 axiomas** de espacio vectorial y sabes verificarlos.\n"
            "- Reconoces los ejemplos clásicos: $\\mathbb{R}^n$, $\\mathcal{P}_n$, $\\mathbb{R}^{m\\times n}$.\n"
            "- Defines **subespacio** y verificas las **3 condiciones**.\n"
            "- Construyes el **subespacio generado** $\\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$."
        )),

        b("definicion",
          titulo="Espacio vectorial (sobre $\\mathbb{R}$)",
          body_md=(
              "Un **espacio vectorial** sobre $\\mathbb{R}$ es un conjunto **no vacío** $V$ cuyos elementos llamamos **vectores**, dotado de dos operaciones:\n\n"
              "- **Suma:** $+ : V \\times V \\to V$, $(\\vec{u}, \\vec{v}) \\mapsto \\vec{u} + \\vec{v}$.\n"
              "- **Producto por escalar:** $\\cdot : \\mathbb{R} \\times V \\to V$, $(c, \\vec{u}) \\mapsto c\\vec{u}$.\n\n"
              "que satisfacen los siguientes **10 axiomas** para todos $\\vec{u}, \\vec{v}, \\vec{w} \\in V$ y $c, d \\in \\mathbb{R}$:\n\n"
              "1. **Cierre de la suma:** $\\vec{u} + \\vec{v} \\in V$.\n"
              "2. **Conmutativa:** $\\vec{u} + \\vec{v} = \\vec{v} + \\vec{u}$.\n"
              "3. **Asociativa:** $(\\vec{u} + \\vec{v}) + \\vec{w} = \\vec{u} + (\\vec{v} + \\vec{w})$.\n"
              "4. **Neutro aditivo:** existe $\\vec{0} \\in V$ tal que $\\vec{u} + \\vec{0} = \\vec{u}$.\n"
              "5. **Inverso aditivo:** para cada $\\vec{u} \\in V$ existe $-\\vec{u} \\in V$ con $\\vec{u} + (-\\vec{u}) = \\vec{0}$.\n"
              "6. **Cierre del producto por escalar:** $c\\vec{u} \\in V$.\n"
              "7. **Distributiva (escalar sobre vectores):** $c(\\vec{u} + \\vec{v}) = c\\vec{u} + c\\vec{v}$.\n"
              "8. **Distributiva (escalares):** $(c + d)\\vec{u} = c\\vec{u} + d\\vec{u}$.\n"
              "9. **Compatibilidad de escalares:** $c(d\\vec{u}) = (cd)\\vec{u}$.\n"
              "10. **Identidad escalar:** $1 \\cdot \\vec{u} = \\vec{u}$."
          )),

        formulas(
            titulo="Propiedades inmediatas",
            body=(
                "De los 10 axiomas se deducen, para todo $\\vec{u} \\in V$ y $c \\in \\mathbb{R}$:\n\n"
                "- **Unicidad** del vector cero $\\vec{0}$ y del inverso aditivo.\n"
                "- $0 \\cdot \\vec{u} = \\vec{0}$ y $c \\cdot \\vec{0} = \\vec{0}$.\n"
                "- $(-1)\\vec{u} = -\\vec{u}$.\n"
                "- **Cancelación:** si $\\vec{u} + \\vec{w} = \\vec{v} + \\vec{w}$, entonces $\\vec{u} = \\vec{v}$.\n"
                "- Si $c\\vec{u} = \\vec{0}$, entonces $c = 0$ o $\\vec{u} = \\vec{0}$.\n\n"
                "Estas propiedades son consecuencias formales — no axiomas adicionales."
            ),
        ),

        b("definicion",
          titulo="Tres ejemplos clásicos",
          body_md=(
              "**Ejemplo 1 — $\\mathbb{R}^n$.** Para $n \\geq 1$, las n-tuplas $(u_1, \\ldots, u_n)$ con suma y producto por escalar **entrada a entrada**:\n\n"
              "$(\\vec{u} + \\vec{v})_i = u_i + v_i, \\qquad (c\\vec{u})_i = c\\,u_i.$\n\n"
              "El **prototipo** de espacio vectorial — todos los axiomas se verifican entrada por entrada.\n\n"
              "**Ejemplo 2 — Polinomios $\\mathcal{P}_n$.** Para $n \\geq 0$:\n\n"
              "$\\mathcal{P}_n = \\{ p(t) = a_0 + a_1 t + \\cdots + a_n t^n : a_0, \\ldots, a_n \\in \\mathbb{R} \\}.$\n\n"
              "Operaciones: $(p + q)(t) = p(t) + q(t)$, $(c \\cdot p)(t) = c\\,p(t)$. El polinomio cero (todos los coeficientes $= 0$) es el neutro.\n\n"
              "**Ejemplo 3 — Matrices $\\mathbb{R}^{m\\times n}$.** Todas las matrices reales $m \\times n$ con suma y producto por escalar **entrada a entrada**:\n\n"
              "$(A + B)_{ij} = a_{ij} + b_{ij}, \\qquad (cA)_{ij} = c\\,a_{ij}.$\n\n"
              "El neutro es la matriz cero $\\mathbf{0}_{m\\times n}$."
          )),

        b("intuicion", body_md=(
            "**¿Qué tienen en común estos ejemplos?**\n\n"
            "Aunque los **objetos** (vectores, polinomios, matrices) son distintos, las **reglas algebraicas** son idénticas. Por eso, todo lo que aprendamos en abstracto ('combinación lineal', 'independencia', 'base', 'dimensión') vale **simultáneamente** para los tres.\n\n"
            "Resolver una ecuación diferencial lineal y resolver un sistema $A\\vec{x} = \\vec{b}$ son, en cierto sentido profundo, **el mismo problema**. La abstracción del espacio vectorial **unifica** esos contextos."
        )),

        b("definicion",
          titulo="Subespacio vectorial",
          body_md=(
              "Sea $V$ un espacio vectorial sobre $\\mathbb{R}$. Un **subespacio vectorial** de $V$ es un subconjunto $H \\subseteq V$ que cumple:\n\n"
              "**(a)** El vector cero de $V$ pertenece a $H$: $\\vec{0} \\in H$.\n\n"
              "**(b)** **Cerrado bajo la suma:** si $\\vec{u}, \\vec{v} \\in H$, entonces $\\vec{u} + \\vec{v} \\in H$.\n\n"
              "**(c)** **Cerrado bajo producto por escalar:** si $\\vec{u} \\in H$ y $c \\in \\mathbb{R}$, entonces $c\\vec{u} \\in H$.\n\n"
              "**Idea clave:** estas tres condiciones aseguran que $H$ es **en sí mismo un espacio vectorial** con las operaciones heredadas de $V$ — los otros 7 axiomas se cumplen automáticamente porque ya valen en $V$.\n\n"
              "**Para verificar que algo es subespacio, basta chequear (a), (b), (c).**"
          )),

        b("ejemplo_resuelto",
          titulo="Subespacio trivial y el plano $xy$ en $\\mathbb{R}^3$",
          problema_md=(
              "Verifica que (i) $\\{\\vec{0}\\}$ es subespacio de cualquier $V$, y (ii) $H = \\{(s, t, 0) : s, t \\in \\mathbb{R}\\}$ es subespacio de $\\mathbb{R}^3$."
          ),
          pasos=[
              {"accion_md": (
                  "**(i)** **Subespacio cero $\\{\\vec{0}\\}$.** (a) Contiene a $\\vec{0}$ por definición. (b) $\\vec{0} + \\vec{0} = \\vec{0} \\in \\{\\vec{0}\\}$. (c) $c\\vec{0} = \\vec{0} \\in \\{\\vec{0}\\}$. ✓"
              ),
               "justificacion_md": "**Trivialmente** es subespacio. Llamado el **subespacio trivial** o **cero**.",
               "es_resultado": False},
              {"accion_md": (
                  "**(ii)** **Plano $xy$ en $\\mathbb{R}^3$.** (a) $(0, 0, 0) \\in H$ tomando $s = t = 0$. (b) $(s_1, t_1, 0) + (s_2, t_2, 0) = (s_1 + s_2, t_1 + t_2, 0) \\in H$. (c) $c(s, t, 0) = (cs, ct, 0) \\in H$. ✓"
              ),
               "justificacion_md": "**$H$ es subespacio** — geométricamente, el plano $xy$ del espacio 3D.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Dos contraejemplos importantes.**\n\n"
            "**Contraejemplo 1 — $\\mathbb{R}^2 \\not\\subseteq \\mathbb{R}^3$.** Aunque podemos 'visualizar' a $\\mathbb{R}^2$ dentro de $\\mathbb{R}^3$, los vectores de $\\mathbb{R}^2$ son **pares ordenados** (2 componentes), no triples. Estrictamente, $\\mathbb{R}^2 \\not\\subseteq \\mathbb{R}^3$, así que no puede ser subespacio.\n\n"
            "**Contraejemplo 2 — Plano que NO pasa por el origen.** El conjunto\n\n"
            "$P = \\{(x, y, z) \\in \\mathbb{R}^3 : x + y + z = 1\\}$\n\n"
            "**no** es subespacio: el vector cero $(0,0,0)$ no satisface $0 + 0 + 0 = 1$, así que **falla la condición (a)**. Geométricamente es un plano, pero no contiene el origen, por lo que falla.\n\n"
            "**Regla mnemotécnica:** todo subespacio de $\\mathbb{R}^n$ **debe contener el origen**."
        )),

        b("definicion",
          titulo="Subespacio generado por un conjunto",
          body_md=(
              "Sea $V$ un espacio vectorial y $\\vec{v}_1, \\ldots, \\vec{v}_p \\in V$. El **subespacio generado** por $\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$ es\n\n"
              "$$\\boxed{\\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\} = \\{c_1 \\vec{v}_1 + c_2 \\vec{v}_2 + \\cdots + c_p \\vec{v}_p : c_1, \\ldots, c_p \\in \\mathbb{R}\\}.}$$\n\n"
              "Es decir, el conjunto de **todas las combinaciones lineales** de los $\\vec{v}_i$.\n\n"
              "**Teorema.** $\\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$ es siempre un **subespacio** de $V$. Más aún, es el **menor** subespacio de $V$ que contiene a todos los $\\vec{v}_i$.\n\n"
              "**Consecuencia operativa:** una manera muy común de construir subespacios es 'tomar el gen' de un conjunto."
          )),

        b("ejemplo_resuelto",
          titulo="$\\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\}$ es un subespacio",
          problema_md=(
              "Verifica que $H = \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\} = \\{s_1 \\vec{v}_1 + s_2 \\vec{v}_2 : s_1, s_2 \\in \\mathbb{R}\\}$ es subespacio de $V$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** $\\vec{0} = 0\\,\\vec{v}_1 + 0\\,\\vec{v}_2 \\in H$ ✓."
              ),
               "justificacion_md": "Tomamos los pesos nulos.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Si $\\vec{u} = s_1\\vec{v}_1 + s_2\\vec{v}_2 \\in H$ y $\\vec{w} = t_1\\vec{v}_1 + t_2\\vec{v}_2 \\in H$, entonces:\n\n"
                  "$\\vec{u} + \\vec{w} = (s_1 + t_1)\\vec{v}_1 + (s_2 + t_2)\\vec{v}_2 \\in H.$ ✓"
              ),
               "justificacion_md": "La suma queda como otra combinación lineal.",
               "es_resultado": False},
              {"accion_md": (
                  "**(c)** Si $c \\in \\mathbb{R}$ y $\\vec{u} = s_1\\vec{v}_1 + s_2\\vec{v}_2$, entonces:\n\n"
                  "$c\\vec{u} = (cs_1)\\vec{v}_1 + (cs_2)\\vec{v}_2 \\in H.$ ✓\n\n"
                  "**Conclusión: $H$ es subespacio de $V$.**"
              ),
               "justificacion_md": "**Lección general:** $\\text{Gen}\\{\\cdot\\}$ produce subespacios automáticamente — ahorra verificar las 3 condiciones cada vez.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Subespacio en $\\mathbb{R}^3$",
          problema_md=(
              "Sean $\\vec{v}_1 = (1, 0, 0)^T$ y $\\vec{v}_2 = (0, 1, 0)^T$. Describir $\\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\}$ geométricamente."
          ),
          pasos=[
              {"accion_md": (
                  "$\\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\} = \\{s(1, 0, 0) + t(0, 1, 0) : s, t \\in \\mathbb{R}\\} = \\{(s, t, 0) : s, t \\in \\mathbb{R}\\}.$"
              ),
               "justificacion_md": "Combinación lineal entrada por entrada.",
               "es_resultado": False},
              {"accion_md": (
                  "**Geométricamente:** el **plano $xy$** dentro de $\\mathbb{R}^3$ — todos los puntos con tercera coordenada $0$."
              ),
               "justificacion_md": "**Patrón:** $\\text{Gen}$ de dos vectores no paralelos en $\\mathbb{R}^3$ es un **plano por el origen**.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál de los siguientes NO es un espacio vectorial sobre $\\mathbb{R}$ con las operaciones usuales?",
                  "opciones_md": [
                      "$\\mathbb{R}^4$",
                      "$\\mathcal{P}_3$ (polinomios de grado $\\leq 3$)",
                      "$\\mathbb{R}^{2\\times 3}$",
                      "$\\{(x, y) \\in \\mathbb{R}^2 : x \\geq 0\\}$",
                  ],
                  "correcta": "D",
                  "pista_md": "¿La condición $x \\geq 0$ se preserva por escalar negativo?",
                  "explicacion_md": "**(D) no es espacio vectorial.** Falla cierre bajo escalar: si $\\vec{u} = (1, 0)$ y $c = -1$, entonces $c\\vec{u} = (-1, 0)$ tiene $x = -1 < 0$, fuera del conjunto.",
              },
              {
                  "enunciado_md": "Para que $H \\subseteq V$ sea subespacio, ¿qué se debe verificar?",
                  "opciones_md": [
                      "Solo que $H$ sea no vacío",
                      "Solo que $H$ contenga al $\\vec{0}$",
                      "Las **tres** condiciones: $\\vec{0} \\in H$, cerrado bajo suma, cerrado bajo escalar",
                      "Los 10 axiomas de espacio vectorial",
                  ],
                  "correcta": "C",
                  "pista_md": "Las 3 condiciones del subespacio.",
                  "explicacion_md": "**Las 3 condiciones (a), (b), (c).** Los otros 7 axiomas se heredan automáticamente de $V$.",
              },
              {
                  "enunciado_md": "¿$P = \\{(x, y) : x + y = 5\\}$ es subespacio de $\\mathbb{R}^2$?",
                  "opciones_md": [
                      "Sí, siempre",
                      "Sí, porque es una recta",
                      "No, porque no contiene a $(0, 0)$",
                      "No se puede decidir",
                  ],
                  "correcta": "C",
                  "pista_md": "Verifica si $\\vec{0} \\in P$.",
                  "explicacion_md": "**(C).** $0 + 0 = 0 \\neq 5 \\Rightarrow \\vec{0} \\notin P \\Rightarrow$ no es subespacio. Toda recta de $\\mathbb{R}^2$ que **no pase por el origen** falla la primera condición.",
              },
          ]),

        ej(
            "Verificar subespacio",
            "Decide si $H = \\{(a, b, c) \\in \\mathbb{R}^3 : a + b + c = 0\\}$ es subespacio de $\\mathbb{R}^3$.",
            [
                "Verifica las 3 condiciones: $\\vec{0} \\in H$, cerrado bajo suma, cerrado bajo escalar.",
            ],
            (
                "(a) $(0, 0, 0)$: $0 + 0 + 0 = 0$ ✓.\n\n"
                "(b) Si $(a_1, b_1, c_1), (a_2, b_2, c_2) \\in H$, su suma $(a_1+a_2, b_1+b_2, c_1+c_2)$ cumple $(a_1+a_2) + (b_1+b_2) + (c_1+c_2) = (a_1+b_1+c_1) + (a_2+b_2+c_2) = 0 + 0 = 0$ ✓.\n\n"
                "(c) Si $\\lambda \\in \\mathbb{R}$: $\\lambda a + \\lambda b + \\lambda c = \\lambda(a+b+c) = 0$ ✓.\n\n"
                "**$H$ es subespacio** — geométricamente es el plano $a + b + c = 0$ que pasa por el origen."
            ),
        ),

        ej(
            "Subespacio de polinomios",
            "Sea $P = \\{p \\in \\mathcal{P}_3 : p(2) = 0\\}$. ¿Es $P$ subespacio de $\\mathcal{P}_3$?",
            [
                "El polinomio cero (todos los coeficientes $0$) tiene $p(2) = 0$.",
                "Verifica suma y escalar.",
            ],
            (
                "(a) El polinomio cero $p(t) \\equiv 0$ cumple $p(2) = 0$ ✓.\n\n"
                "(b) Si $p, q \\in P$: $(p+q)(2) = p(2) + q(2) = 0 + 0 = 0$ ✓.\n\n"
                "(c) Si $c \\in \\mathbb{R}$: $(cp)(2) = c\\,p(2) = c\\cdot 0 = 0$ ✓.\n\n"
                "**$P$ es subespacio.** Estos son los polinomios de $\\mathcal{P}_3$ que tienen una raíz en $t = 2$."
            ),
        ),

        ej(
            "Contraejemplo: cuadrado del módulo $\\leq 1$",
            "¿Es $H = \\{\\vec{x} \\in \\mathbb{R}^2 : \\|\\vec{x}\\| \\leq 1\\}$ (el disco unitario) subespacio de $\\mathbb{R}^2$?",
            [
                "Verifica si está cerrado bajo escalar.",
                "Considera multiplicar un vector por $c = 2$.",
            ],
            (
                "$\\vec{0} \\in H$ ✓ (la condición se cumple).\n\n"
                "**Falla cierre bajo escalar:** si $\\vec{x} = (1, 0)$ entonces $\\|\\vec{x}\\| = 1 \\leq 1$, pero $2\\vec{x} = (2, 0)$ tiene $\\|2\\vec{x}\\| = 2 > 1 \\Rightarrow 2\\vec{x} \\notin H$.\n\n"
                "**Conclusión:** $H$ **no es subespacio** — los subespacios son objetos 'rectos' (rectas, planos, etc.), nunca regiones acotadas."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar verificar $\\vec{0} \\in H$.** Es la primera condición y la más fácil de chequear: si falla, ya sabemos que no es subespacio.",
              "**Confundir $\\mathbb{R}^2$ con un subespacio de $\\mathbb{R}^3$.** Estrictamente, los vectores tienen distinto número de componentes — para 'incluir' $\\mathbb{R}^2$ en $\\mathbb{R}^3$ habría que identificar $(x, y) \\leftrightarrow (x, y, 0)$.",
              "**Pensar que cualquier 'recta' o 'plano' es subespacio.** Solo si **pasan por el origen**.",
              "**Querer demostrar los 10 axiomas para verificar subespacio.** Solo las 3 condiciones (a), (b), (c) — los demás se heredan.",
              "**Confundir 'genera' con 'contiene'.** $\\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\}$ es **el conjunto de todas las combinaciones lineales** — usualmente mucho más grande que $\\{\\vec{v}_1, \\vec{v}_2\\}$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Espacio vectorial:** conjunto $V$ con suma y escalar que cumplen los **10 axiomas**.",
              "**Ejemplos clave:** $\\mathbb{R}^n$, $\\mathcal{P}_n$ (polinomios de grado $\\leq n$), $\\mathbb{R}^{m\\times n}$ (matrices).",
              "**Subespacio:** subconjunto $H \\subseteq V$ que cumple las **3 condiciones**: $\\vec{0} \\in H$, cerrado bajo suma, cerrado bajo escalar.",
              "**Regla:** todo subespacio de $\\mathbb{R}^n$ contiene al origen.",
              "**Subespacio generado:** $\\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$ = todas las combinaciones lineales — siempre es subespacio.",
              "**Próxima lección:** los dos subespacios más importantes asociados a una matriz: **espacio nulo** $\\text{Nul}\\,A$ y **espacio columna** $\\text{Col}\\,A$.",
          ]),
    ]
    return {
        "id": "lec-al-5-1-espacios-vectoriales",
        "title": "Espacios vectoriales",
        "description": "Los 10 axiomas, ejemplos ($\\mathbb{R}^n$, $\\mathcal{P}_n$, $\\mathbb{R}^{m\\times n}$), subespacios con las 3 condiciones, subespacio generado $\\text{Gen}\\{\\vec{v}_1,\\ldots,\\vec{v}_p\\}$.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 1,
    }


# =====================================================================
# 5.2 Espacios notables (Nul A, Col A, núcleo y rango)
# =====================================================================
def lesson_5_2():
    blocks = [
        b("texto", body_md=(
            "Toda matriz $A$ trae consigo dos **subespacios distinguidos** que codifican gran parte "
            "de su estructura: el **espacio nulo** $\\text{Nul}\\,A$ (las soluciones de $A\\vec{x} = \\vec{0}$) "
            "y el **espacio columna** $\\text{Col}\\,A$ (las combinaciones lineales de las columnas de $A$).\n\n"
            "Ya hemos trabajado con ambos sin nombrarlos así:\n\n"
            "- $\\text{Nul}\\,A = \\mathcal{N}(A)$: aparece en la lección 2.4 como núcleo del sistema homogéneo.\n"
            "- $\\text{Col}\\,A$: es la imagen $\\text{Im}(T)$ de la transformación $T(\\vec{x}) = A\\vec{x}$ (lección 2.5).\n\n"
            "**¿Por qué importan?**\n\n"
            "- $\\text{Nul}\\,A$ describe **todas las soluciones del sistema homogéneo** y, junto con una solución particular, el conjunto solución completo de $A\\vec{x} = \\vec{b}$.\n"
            "- $\\text{Col}\\,A$ describe **para qué $\\vec{b}$ el sistema $A\\vec{x} = \\vec{b}$ es consistente**.\n\n"
            "Generalizamos también a **transformaciones lineales abstractas** $T : V \\to W$, definiendo **núcleo** $\\ker T$ y **rango** $\\text{Im}\\,T$ — los análogos en el contexto general.\n\n"
            "Al terminar:\n\n"
            "- Defines y manejas $\\text{Nul}\\,A$ y $\\text{Col}\\,A$ como subespacios.\n"
            "- Reconoces en qué espacio ambiente vive cada uno.\n"
            "- Describes $\\text{Nul}\\,A$ explícitamente con conjunto generador.\n"
            "- Generalizas a $\\ker T$ e $\\text{Im}\\,T$ para TL abstractas."
        )),

        b("definicion",
          titulo="Espacio nulo $\\text{Nul}\\,A$",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{m \\times n}$. El **espacio nulo** de $A$, denotado $\\text{Nul}\\,A$, es:\n\n"
              "$$\\boxed{\\text{Nul}\\,A = \\{\\vec{x} \\in \\mathbb{R}^n : A\\vec{x} = \\vec{0}\\}.}$$\n\n"
              "Es el conjunto de **todas las soluciones** de la ecuación homogénea $A\\vec{x} = \\vec{0}$. Equivalentemente, es el conjunto de vectores de $\\mathbb{R}^n$ que la transformación $T(\\vec{x}) = A\\vec{x}$ envía al cero de $\\mathbb{R}^m$.\n\n"
              "**Espacio ambiente:** $\\text{Nul}\\,A \\subseteq \\mathbb{R}^n$ (el dominio de $T$).\n\n"
              "**Teorema.** $\\text{Nul}\\,A$ es siempre un **subespacio** de $\\mathbb{R}^n$:\n\n"
              "- (a) $A\\vec{0} = \\vec{0}$ $\\Rightarrow \\vec{0} \\in \\text{Nul}\\,A$.\n"
              "- (b) Si $A\\vec{u} = \\vec{0}$ y $A\\vec{v} = \\vec{0}$: $A(\\vec{u} + \\vec{v}) = \\vec{0} + \\vec{0} = \\vec{0}$.\n"
              "- (c) Si $A\\vec{u} = \\vec{0}$ y $c \\in \\mathbb{R}$: $A(c\\vec{u}) = c(A\\vec{u}) = \\vec{0}$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Verificación directa",
          problema_md=(
              "Sea $A = \\begin{bmatrix} 1 & -3 & -2 \\\\ -5 & 9 & 1 \\end{bmatrix}$ y $\\vec{u} = (5, 3, -2)^T$. ¿Está $\\vec{u} \\in \\text{Nul}\\,A$?"
          ),
          pasos=[
              {"accion_md": (
                  "Calculamos $A\\vec{u}$:\n\n"
                  "$A\\vec{u} = \\begin{bmatrix} 1\\cdot 5 + (-3)\\cdot 3 + (-2)(-2) \\\\ -5\\cdot 5 + 9\\cdot 3 + 1\\cdot(-2) \\end{bmatrix} = \\begin{bmatrix} 5 - 9 + 4 \\\\ -25 + 27 - 2 \\end{bmatrix} = \\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Producto matriz-vector estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "$A\\vec{u} = \\vec{0}$ $\\Rightarrow$ **$\\vec{u} \\in \\text{Nul}\\,A$.**"
              ),
               "justificacion_md": "Verificación de membresía: aplicar $A$ y comprobar que da $\\vec{0}$.",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Descripción explícita de $\\text{Nul}\\,A$ como conjunto generado.**\n\n"
              "Para describir $\\text{Nul}\\,A$ explícitamente, se resuelve $A\\vec{x} = \\vec{0}$ por reducción por filas. La solución general queda en términos de las **variables libres**, lo que permite escribir\n\n"
              "$$\\text{Nul}\\,A = \\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_k\\},$$\n\n"
              "donde $k = $ número de variables libres y los $\\vec{v}_i$ son los vectores dirección asociados a cada parámetro (lección 2.4).\n\n"
              "**Importante:** este conjunto generador es **automáticamente linealmente independiente**, pues cada vector corresponde a una variable libre distinta."
          )),

        b("ejemplo_resuelto",
          titulo="Conjunto generador de $\\text{Nul}\\,A$",
          problema_md=(
              "Encuentra un conjunto generador para $\\text{Nul}\\,A$ con $A = \\begin{bmatrix} -3 & 6 & -1 & 1 & -7 \\\\ 1 & -2 & 2 & 3 & -1 \\\\ 2 & -4 & 5 & 8 & -4 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Reducir $[A \\mid \\vec{0}]$ a RREF:\n\n"
                  "$\\begin{bmatrix} 1 & -2 & 0 & -1 & 3 \\mid 0 \\\\ 0 & 0 & 1 & 2 & -2 \\mid 0 \\\\ 0 & 0 & 0 & 0 & 0 \\mid 0 \\end{bmatrix}.$\n\n"
                  "Pivotes en columnas $1, 3$ $\\Rightarrow$ libres $x_2, x_4, x_5$. De aquí: $x_1 = 2x_2 + x_4 - 3x_5$, $x_3 = -2x_4 + 2x_5$."
              ),
               "justificacion_md": "Despejamos básicas en términos de libres.",
               "es_resultado": False},
              {"accion_md": (
                  "Solución general:\n\n"
                  "$\\vec{x} = x_2 \\begin{bmatrix} 2 \\\\ 1 \\\\ 0 \\\\ 0 \\\\ 0 \\end{bmatrix} + x_4 \\begin{bmatrix} 1 \\\\ 0 \\\\ -2 \\\\ 1 \\\\ 0 \\end{bmatrix} + x_5 \\begin{bmatrix} -3 \\\\ 0 \\\\ 2 \\\\ 0 \\\\ 1 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Forma vectorial paramétrica.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\boxed{\\text{Nul}\\,A = \\text{Gen}\\Bigl\\{(2,1,0,0,0)^T,\\ (1,0,-2,1,0)^T,\\ (-3,0,2,0,1)^T\\Bigr\\}.}$\n\n"
                  "Estos $3$ vectores son LI (cada uno tiene un $1$ en una posición distinta correspondiente a la variable libre)."
              ),
               "justificacion_md": "**Patrón:** el número de vectores en el conjunto generador de $\\text{Nul}\\,A$ es **el número de variables libres** de $A\\vec{x} = \\vec{0}$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Espacio columna $\\text{Col}\\,A$",
          body_md=(
              "Sea $A \\in \\mathbb{R}^{m \\times n}$ con columnas $\\vec{a}_1, \\ldots, \\vec{a}_n$. El **espacio columna** de $A$, denotado $\\text{Col}\\,A$, es\n\n"
              "$$\\boxed{\\text{Col}\\,A = \\text{Gen}\\{\\vec{a}_1, \\ldots, \\vec{a}_n\\} \\subseteq \\mathbb{R}^m.}$$\n\n"
              "Es decir, el conjunto de **todas las combinaciones lineales** de las columnas de $A$.\n\n"
              "**Teorema.** $\\text{Col}\\,A$ es siempre un **subespacio** de $\\mathbb{R}^m$ (es un gen).\n\n"
              "**Espacio ambiente:** $\\text{Col}\\,A \\subseteq \\mathbb{R}^m$ (el codominio de $T(\\vec{x}) = A\\vec{x}$).\n\n"
              "**Caracterización.** $\\vec{b} \\in \\text{Col}\\,A \\iff$ existe $\\vec{x} \\in \\mathbb{R}^n$ con $A\\vec{x} = \\vec{b}$ $\\iff$ el sistema $A\\vec{x} = \\vec{b}$ es **consistente**."
          )),

        b("ejemplo_resuelto",
          titulo="Encontrar una matriz a partir de un subespacio",
          problema_md=(
              "Sea $W = \\Bigl\\{\\begin{bmatrix} 6a - b \\\\ a + b \\\\ -7a \\end{bmatrix} : a, b \\in \\mathbb{R}\\Bigr\\} \\subseteq \\mathbb{R}^3$. Halla una matriz $A$ tal que $W = \\text{Col}\\,A$."
          ),
          pasos=[
              {"accion_md": (
                  "Separamos por parámetros: $\\begin{bmatrix} 6a - b \\\\ a + b \\\\ -7a \\end{bmatrix} = a \\begin{bmatrix} 6 \\\\ 1 \\\\ -7 \\end{bmatrix} + b \\begin{bmatrix} -1 \\\\ 1 \\\\ 0 \\end{bmatrix}.$\n\n"
                  "Es decir, $W = \\text{Gen}\\{(6, 1, -7)^T, (-1, 1, 0)^T\\}$."
              ),
               "justificacion_md": "**Idea:** todo subespacio descrito como 'parametrización lineal' es un gen.",
               "es_resultado": False},
              {"accion_md": (
                  "Tomamos esos vectores como **columnas** de $A$:\n\n"
                  "$A = \\begin{bmatrix} 6 & -1 \\\\ 1 & 1 \\\\ -7 & 0 \\end{bmatrix}.$\n\n"
                  "Por construcción, $W = \\text{Col}\\,A$. ✓"
              ),
               "justificacion_md": "**Convertir un subespacio paramétrico en $\\text{Col}\\,A$**: pone vectores generadores como columnas.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Contraste entre $\\text{Nul}\\,A$ y $\\text{Col}\\,A$.**\n\n"
            "| | $\\text{Nul}\\,A$ | $\\text{Col}\\,A$ |\n|---|---|---|\n"
            "| **Definición** | $\\{\\vec{x} : A\\vec{x} = \\vec{0}\\}$ | $\\text{Gen}\\{\\text{columnas de }A\\}$ |\n"
            "| **Vive en** | $\\mathbb{R}^n$ (dominio) | $\\mathbb{R}^m$ (codominio) |\n"
            "| **Descripción** | Implícita (relaciones que cumplen los $\\vec{x}$) | Explícita (generadores ya dados) |\n"
            "| **Conexión** | Conjunto solución de homogéneo | $\\vec{b}$ tales que $A\\vec{x} = \\vec{b}$ es consistente |\n\n"
            "**Cuando $A$ no es cuadrada, $\\text{Nul}\\,A$ y $\\text{Col}\\,A$ viven en espacios distintos** $\\Rightarrow$ ni siquiera tiene sentido compararlos como conjuntos. El único elemento que ambos tienen 'a la fuerza' es el vector cero (en su respectivo espacio)."
        )),

        b("ejemplo_resuelto",
          titulo="$\\text{Nul}\\,A$ y $\\text{Col}\\,A$ — distintos espacios ambientes",
          problema_md=(
              "Sea $A = \\begin{bmatrix} 2 & 4 & -2 & 1 \\\\ -2 & -5 & 7 & 3 \\\\ 3 & 7 & -8 & 6 \\end{bmatrix}$. (a) ¿En qué $\\mathbb{R}^k$ vive $\\text{Col}\\,A$? (b) ¿En qué $\\mathbb{R}^k$ vive $\\text{Nul}\\,A$?"
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Cada columna de $A$ tiene **$3$ entradas** $\\Rightarrow$ las columnas viven en $\\mathbb{R}^3$ $\\Rightarrow$ $\\text{Col}\\,A \\subseteq \\mathbb{R}^3$. Aquí $k = 3$."
              ),
               "justificacion_md": "$\\text{Col}\\,A \\subseteq \\mathbb{R}^m$ donde $m$ = número de filas.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Un vector $\\vec{x}$ con $A\\vec{x} = \\vec{0}$ debe tener $4$ entradas (una por cada columna de $A$) $\\Rightarrow$ $\\text{Nul}\\,A \\subseteq \\mathbb{R}^4$. Aquí $k = 4$."
              ),
               "justificacion_md": "$\\text{Nul}\\,A \\subseteq \\mathbb{R}^n$ donde $n$ = número de columnas.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Núcleo y rango (imagen) de una transformación lineal",
          body_md=(
              "Generalizamos a transformaciones lineales abstractas. Sea $T : V \\to W$ una **transformación lineal** entre espacios vectoriales, es decir, $T$ satisface $T(\\vec{u} + \\vec{v}) = T(\\vec{u}) + T(\\vec{v})$ y $T(c\\vec{u}) = c\\,T(\\vec{u})$.\n\n"
              "**Núcleo** (o **espacio nulo**) de $T$:\n\n"
              "$$\\ker(T) = \\{\\vec{u} \\in V : T(\\vec{u}) = \\vec{0}\\}.$$\n\n"
              "Vectores del **dominio** que se mapean al cero. **Es subespacio de $V$.**\n\n"
              "**Rango** (o **imagen**) de $T$:\n\n"
              "$$\\text{Im}(T) = \\{T(\\vec{x}) : \\vec{x} \\in V\\}.$$\n\n"
              "Vectores del **codominio** que son imagen de algún vector del dominio. **Es subespacio de $W$.**\n\n"
              "**Conexión con matrices.** Si $T(\\vec{x}) = A\\vec{x}$ es matricial, entonces:\n\n"
              "$$\\ker(T) = \\text{Nul}\\,A, \\qquad \\text{Im}(T) = \\text{Col}\\,A.$$"
          )),

        b("ejemplo_resuelto",
          titulo="Núcleo e imagen de una TL",
          problema_md=(
              "Sea $T : \\mathbb{R}^3 \\to \\mathbb{R}^2$ definida por $T(x, y, z) = (x + 2y, y - z)$. Halla $\\ker T$ e $\\text{Im}\\,T$."
          ),
          pasos=[
              {"accion_md": (
                  "**Núcleo:** $T(x, y, z) = (0, 0)$ $\\iff x + 2y = 0$ y $y - z = 0$ $\\iff x = -2y, z = y$.\n\n"
                  "$\\ker T = \\{(-2y, y, y) : y \\in \\mathbb{R}\\} = \\text{Gen}\\{(-2, 1, 1)\\}.$"
              ),
               "justificacion_md": "Una recta por el origen en $\\mathbb{R}^3$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Imagen:** matricialmente, $T(\\vec{x}) = A\\vec{x}$ con $A = \\begin{bmatrix} 1 & 2 & 0 \\\\ 0 & 1 & -1 \\end{bmatrix}$.\n\n"
                  "$\\text{Im}\\,T = \\text{Col}\\,A = \\text{Gen}\\{(1,0)^T, (2,1)^T, (0,-1)^T\\}$.\n\n"
                  "Como las dos primeras columnas son LI y generan $\\mathbb{R}^2$ (forman base), $\\text{Im}\\,T = \\mathbb{R}^2$."
              ),
               "justificacion_md": "**$T$ es sobreyectiva** (alcanza todo $\\mathbb{R}^2$), pero **no inyectiva** (núcleo no trivial).",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $A \\in \\mathbb{R}^{4 \\times 7}$, entonces $\\text{Nul}\\,A$ es subespacio de:",
                  "opciones_md": ["$\\mathbb{R}^4$", "$\\mathbb{R}^7$", "$\\mathbb{R}^{4\\times 7}$", "$\\mathbb{R}^{11}$"],
                  "correcta": "B",
                  "pista_md": "$\\text{Nul}\\,A \\subseteq \\mathbb{R}^n$ con $n =$ # columnas.",
                  "explicacion_md": "**$\\mathbb{R}^7$.** Los vectores $\\vec{x}$ que cumplen $A\\vec{x} = \\vec{0}$ tienen 7 entradas (una por columna de $A$).",
              },
              {
                  "enunciado_md": "$\\vec{b} \\in \\text{Col}\\,A \\iff$:",
                  "opciones_md": [
                      "$\\vec{b}$ es combinación lineal de las filas de $A$",
                      "$A\\vec{x} = \\vec{b}$ es consistente",
                      "$A\\vec{b} = \\vec{0}$",
                      "$\\vec{b} = A^T\\vec{x}$ para algún $\\vec{x}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Caracterización del espacio columna.",
                  "explicacion_md": "**$A\\vec{x} = \\vec{b}$ consistente.** $\\text{Col}\\,A$ es exactamente el conjunto de $\\vec{b}$ para los cuales el sistema tiene solución.",
              },
              {
                  "enunciado_md": "Para $T : V \\to W$ lineal, $\\ker T = \\{\\vec{0}_V\\}$ significa que:",
                  "opciones_md": [
                      "$T$ es sobreyectiva",
                      "$T$ es inyectiva (uno a uno)",
                      "$T$ es la transformación cero",
                      "$T$ es la identidad",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\ker$ trivial $\\iff$ inyectiva.",
                  "explicacion_md": "**$T$ es inyectiva.** Equivalente a 'columnas LI' en el caso matricial. Para que $T$ sea biyectiva ($V \\cong W$) hace falta además que sea sobreyectiva.",
              },
          ]),

        ej(
            "Conjunto generador de $\\text{Nul}\\,A$",
            "Halla un conjunto generador para $\\text{Nul}\\,A$ con $A = \\begin{bmatrix} 1 & -3 & 2 \\\\ 2 & -6 & 4 \\end{bmatrix}$.",
            [
                "Reduce $[A \\mid \\vec{0}]$ a RREF.",
                "Identifica variables libres.",
            ],
            (
                "$A \\sim \\begin{bmatrix} 1 & -3 & 2 \\\\ 0 & 0 & 0 \\end{bmatrix}$. Variables libres: $x_2 = s$, $x_3 = t$. $x_1 = 3s - 2t$.\n\n"
                "$\\vec{x} = s(3, 1, 0)^T + t(-2, 0, 1)^T$.\n\n"
                "$\\text{Nul}\\,A = \\text{Gen}\\{(3, 1, 0)^T, (-2, 0, 1)^T\\}$."
            ),
        ),

        ej(
            "¿Pertenece $\\vec{b}$ a $\\text{Col}\\,A$?",
            "Determina si $\\vec{b} = (3, -1, -4)^T$ pertenece a $\\text{Col}\\,A$ donde $A = \\begin{bmatrix} 1 & -1 \\\\ 2 & 1 \\\\ 3 & 0 \\end{bmatrix}$.",
            [
                "Estudia la consistencia del sistema $A\\vec{x} = \\vec{b}$.",
            ],
            (
                "Reducimos $[A\\mid\\vec{b}] = \\begin{bmatrix} 1 & -1 & 3 \\\\ 2 & 1 & -1 \\\\ 3 & 0 & -4 \\end{bmatrix} \\sim \\begin{bmatrix} 1 & -1 & 3 \\\\ 0 & 3 & -7 \\\\ 0 & 0 & 0 \\end{bmatrix}$.\n\n"
                "No hay fila $[0\\ 0 \\mid c]$ con $c \\neq 0$ $\\Rightarrow$ **consistente** $\\Rightarrow$ **$\\vec{b} \\in \\text{Col}\\,A$**.\n\n"
                "(Si quisiéramos los pesos: $x_2 = -7/3$, $x_1 = 3 + x_2 = 2/3$.)"
            ),
        ),

        ej(
            "Núcleo de TL en polinomios",
            "Sea $T : \\mathcal{P}_2 \\to \\mathbb{R}^2$ definida por $T(p) = (p(0), p(1))$. Halla $\\ker T$.",
            [
                "Escribe $p(t) = a_0 + a_1 t + a_2 t^2$ y plantea $T(p) = (0, 0)$.",
                "Resuelve para $a_0, a_1, a_2$.",
            ],
            (
                "$T(p) = (a_0, a_0 + a_1 + a_2) = (0, 0) \\Rightarrow a_0 = 0$ y $a_1 + a_2 = 0$.\n\n"
                "$a_2 = -a_1$, $a_0 = 0$ $\\Rightarrow p(t) = a_1 t - a_1 t^2 = a_1(t - t^2)$.\n\n"
                "$\\ker T = \\text{Gen}\\{t - t^2\\} \\subset \\mathcal{P}_2$ — una 'recta' en el espacio de polinomios."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir el espacio ambiente.** $\\text{Nul}\\,A \\subseteq \\mathbb{R}^n$, $\\text{Col}\\,A \\subseteq \\mathbb{R}^m$.",
              "**Pensar que $\\text{Nul}\\,A = \\{\\vec{0}\\}$ siempre.** Solo si $A$ tiene columnas LI (= sin variables libres).",
              "**Olvidar comprobar consistencia para $\\vec{b} \\in \\text{Col}\\,A$.** No basta verificar que $\\vec{b}$ tenga el tamaño correcto.",
              "**Confundir 'núcleo' con 'imagen' en TL abstractas.** $\\ker T$ vive en $V$ (dominio); $\\text{Im}\\,T$ vive en $W$ (codominio).",
              "**Asumir que el conjunto generador de $\\text{Nul}\\,A$ tiene un solo vector.** Tiene tantos como variables libres.",
          ]),

        b("resumen",
          puntos_md=[
              "**$\\text{Nul}\\,A$:** soluciones de $A\\vec{x} = \\vec{0}$. Subespacio de $\\mathbb{R}^n$.",
              "**$\\text{Col}\\,A$:** combinaciones lineales de las columnas. Subespacio de $\\mathbb{R}^m$.",
              "**Caracterización:** $\\vec{b} \\in \\text{Col}\\,A \\iff A\\vec{x} = \\vec{b}$ consistente.",
              "**$\\text{Nul}\\,A$ explícito:** se obtiene resolviendo $A\\vec{x} = \\vec{0}$ y leyendo los vectores dirección.",
              "**Para TL abstracta $T : V \\to W$:** $\\ker T \\subseteq V$ (núcleo), $\\text{Im}\\,T \\subseteq W$ (imagen).",
              "**Conexión:** si $T(\\vec{x}) = A\\vec{x}$, entonces $\\ker T = \\text{Nul}\\,A$ e $\\text{Im}\\,T = \\text{Col}\\,A$.",
              "**Próxima lección:** **bases** — conjuntos generadores mínimos que describen unívocamente cada vector.",
          ]),
    ]
    return {
        "id": "lec-al-5-2-espacios-notables",
        "title": "Espacios notables",
        "description": "Espacio nulo $\\text{Nul}\\,A$ y espacio columna $\\text{Col}\\,A$, núcleo $\\ker T$ y rango $\\text{Im}\\,T$ de transformaciones lineales abstractas.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 2,
    }


# =====================================================================
# 5.3 Bases
# =====================================================================
def lesson_5_3():
    blocks = [
        b("texto", body_md=(
            "Una **base** es un conjunto de vectores que permite **describir todo el espacio (o subespacio) "
            "de manera única**. Combina dos ideas que ya conocemos:\n\n"
            "- **Independencia lineal:** ningún vector es redundante.\n"
            "- **Capacidad de generar:** los vectores cubren todo el subespacio.\n\n"
            "Una base es entonces un conjunto **mínimo** que **alcanza** para describir el espacio.\n\n"
            "El **teorema del conjunto generador** garantiza que **siempre** se puede reducir un conjunto generador "
            "a una base eliminando vectores redundantes.\n\n"
            "Veremos cómo construir bases concretas para los subespacios más importantes:\n\n"
            "- **Base de $\\text{Nul}\\,A$:** los vectores dirección obtenidos de la solución de $A\\vec{x} = \\vec{0}$.\n"
            "- **Base de $\\text{Col}\\,A$:** las **columnas pivote** de $A$ (¡las originales, no las reducidas!).\n\n"
            "Al terminar:\n\n"
            "- Defines y reconoces una base.\n"
            "- Aplicas el teorema del conjunto generador.\n"
            "- Construyes bases para $\\text{Nul}\\,A$ y $\\text{Col}\\,A$."
        )),

        b("definicion",
          titulo="Base de un subespacio",
          body_md=(
              "Sea $H$ un subespacio de un espacio vectorial $V$. Un conjunto indexado de vectores\n\n"
              "$$\\mathcal{B} = \\{\\vec{b}_1, \\ldots, \\vec{b}_p\\} \\subseteq V$$\n\n"
              "es una **base** de $H$ si cumple las **dos** condiciones:\n\n"
              "**(I)** $\\mathcal{B}$ es **linealmente independiente**.\n\n"
              "**(II)** $\\mathcal{B}$ **genera** $H$, es decir, $H = \\text{Gen}\\{\\vec{b}_1, \\ldots, \\vec{b}_p\\}$.\n\n"
              "**Caso especial $H = V$:** una base de $V$ es un conjunto LI que **genera todo $V$**.\n\n"
              "**Bases estándar (ejemplos clave):**\n\n"
              "- **$\\mathbb{R}^n$:** $\\{\\vec{e}_1, \\ldots, \\vec{e}_n\\}$ — los vectores canónicos.\n"
              "- **$\\mathcal{P}_n$:** $\\{1, t, t^2, \\ldots, t^n\\}$ — los monomios.\n"
              "- **$\\mathbb{R}^{m\\times n}$:** las matrices $E_{ij}$ con un $1$ en posición $(i,j)$ y ceros en el resto."
          )),

        b("ejemplo_resuelto",
          titulo="Dependencia lineal en polinomios",
          problema_md=(
              "Sean $p_1(t) = 1$, $p_2(t) = t$, $p_3(t) = 4 - t$ en $\\mathcal{P}_2$. ¿Es $\\{p_1, p_2, p_3\\}$ una base?"
          ),
          pasos=[
              {"accion_md": (
                  "Verificamos LI: ¿es $p_3$ combinación lineal de los otros? Notamos que $p_3 = 4\\,p_1 - p_2$ (sustituye: $4(1) - t = 4 - t$ ✓).\n\n"
                  "$\\Rightarrow$ existe relación no trivial $4p_1 - p_2 - p_3 = 0$, luego $\\{p_1, p_2, p_3\\}$ es **LD**."
              ),
               "justificacion_md": "Detectamos directamente que $p_3$ es redundante.",
               "es_resultado": False},
              {"accion_md": (
                  "Como falla la LI, **no es base** de $\\mathcal{P}_2$. (Aunque $\\{p_1, p_2\\}$ sí es base de $\\mathcal{P}_1$.)"
              ),
               "justificacion_md": "Una base requiere ambas condiciones — LI **y** generar.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Una base de $\\mathbb{R}^3$",
          problema_md=(
              "¿Es $\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3\\}$ con $\\vec{v}_1 = (3, 0, -6)^T$, $\\vec{v}_2 = (-4, 1, 7)^T$, $\\vec{v}_3 = (-2, 1, 5)^T$ una base de $\\mathbb{R}^3$?"
          ),
          pasos=[
              {"accion_md": (
                  "Formamos $A = [\\vec{v}_1\\ \\vec{v}_2\\ \\vec{v}_3]$ y reducimos:\n\n"
                  "$A = \\begin{bmatrix} 3 & -4 & -2 \\\\ 0 & 1 & 1 \\\\ -6 & 7 & 5 \\end{bmatrix} \\sim \\begin{bmatrix} 3 & -4 & -2 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 2 \\end{bmatrix}.$\n\n"
                  "**$3$ pivotes en una matriz $3 \\times 3$ $\\Rightarrow A$ invertible.**"
              ),
               "justificacion_md": "Por TMI: invertible $\\iff$ columnas LI $\\iff$ columnas generan $\\mathbb{R}^3$.",
               "es_resultado": False},
              {"accion_md": (
                  "Como las columnas de $A$ son LI **y** generan $\\mathbb{R}^3$, **$\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3\\}$ es base de $\\mathbb{R}^3$**."
              ),
               "justificacion_md": "**Atajo $\\mathbb{R}^n$:** $n$ vectores son base $\\iff$ son LI $\\iff$ matriz $n\\times n$ invertible.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Teorema del conjunto generador",
          enunciado_md=(
              "Sea $S = \\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}$ un conjunto de vectores en $V$ y sea\n\n"
              "$H = \\text{Gen}\\{\\vec{v}_1, \\ldots, \\vec{v}_p\\}.$\n\n"
              "**(a)** Si uno de los $\\vec{v}_k$ es combinación lineal de los demás, entonces $S \\setminus \\{\\vec{v}_k\\}$ **aún genera** $H$.\n\n"
              "**(b)** Si $H \\neq \\{\\vec{0}\\}$, entonces algún subconjunto de $S$ es **base** de $H$.\n\n"
              "**Lectura:** podemos siempre 'depurar' un conjunto generador, eliminando vectores redundantes uno a uno hasta llegar a una **base**."
          ),
          demostracion_md=(
              "**(a)** Si $\\vec{v}_k = \\sum_{i \\neq k} c_i \\vec{v}_i$, entonces toda combinación lineal $\\sum_i a_i \\vec{v}_i$ se reescribe como combinación lineal **sin** $\\vec{v}_k$ sustituyendo. Así $\\text{Gen}(S \\setminus \\{\\vec{v}_k\\}) = \\text{Gen}(S) = H$.\n\n"
              "**(b)** Aplicamos (a) repetidamente hasta que el conjunto restante sea LI. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Eliminar redundancia",
          problema_md=(
              "Sean $\\vec{v}_1 = (0, 2, -1)^T$, $\\vec{v}_2 = (2, 2, 0)^T$, $\\vec{v}_3 = (6, 16, -5)^T$ y $H = \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3\\}$. Halla una base de $H$."
          ),
          pasos=[
              {"accion_md": (
                  "Verificamos si $\\vec{v}_3$ es combinación lineal de $\\vec{v}_1, \\vec{v}_2$. Probando $\\vec{v}_3 = 5\\vec{v}_1 + 3\\vec{v}_2$:\n\n"
                  "$5(0, 2, -1) + 3(2, 2, 0) = (6, 10 + 6, -5) = (6, 16, -5) = \\vec{v}_3$ ✓."
              ),
               "justificacion_md": "$\\vec{v}_3$ es **redundante**.",
               "es_resultado": False},
              {"accion_md": (
                  "Por el teorema, $\\text{Gen}\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3\\} = \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\}$. Como $\\vec{v}_1, \\vec{v}_2$ no son colineales, son LI.\n\n"
                  "**$\\{\\vec{v}_1, \\vec{v}_2\\}$ es base de $H$.**"
              ),
               "justificacion_md": "Conjunto LI que genera = base.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Base para $\\text{Col}\\,A$ vía columnas pivote",
          enunciado_md=(
              "**Las columnas pivote** de una matriz $A$ (es decir, las columnas de $A$ correspondientes a las posiciones pivote en su forma escalonada) **forman una base para $\\text{Col}\\,A$**.\n\n"
              "**Cuidado importante:** las columnas pivote de **$A$ original**, **no** de su forma escalonada. Las OEF cambian las columnas, así que $\\text{Col}\\,A \\neq \\text{Col}\\,U$ donde $U$ es la REF, pero las **posiciones** de las columnas pivote se preservan."
          ),
          demostracion_md=(
              "Las columnas no pivote son combinaciones lineales de las columnas pivote (por unicidad de la solución de $A\\vec{x} = \\vec{0}$ en cada caso). Por el teorema del conjunto generador, podemos descartarlas y quedarnos con las columnas pivote, que generan $\\text{Col}\\,A$. Como las columnas pivote son LI (por su rol como pivotes), forman base. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Base para $\\text{Col}\\,B$ — caso simple",
          problema_md=(
              "Halla una base para $\\text{Col}\\,B$ con $B = \\begin{bmatrix} 1 & 4 & 0 & 2 & 0 \\\\ 0 & 0 & 1 & -1 & 0 \\\\ 0 & 0 & 0 & 0 & 1 \\\\ 0 & 0 & 0 & 0 & 0 \\end{bmatrix}$ (ya en forma escalonada)."
          ),
          pasos=[
              {"accion_md": (
                  "Pivotes en columnas $1, 3, 5$ $\\Rightarrow$ columnas pivote de $B$: $\\vec{b}_1, \\vec{b}_3, \\vec{b}_5$.\n\n"
                  "Las columnas no pivote son redundantes: $\\vec{b}_2 = 4\\vec{b}_1$, $\\vec{b}_4 = 2\\vec{b}_1 - \\vec{b}_3$ (verificable)."
              ),
               "justificacion_md": "Cuando $B$ ya está en forma escalonada, las relaciones se leen directamente.",
               "es_resultado": False},
              {"accion_md": (
                  "**Base de $\\text{Col}\\,B$:** $\\{\\vec{b}_1, \\vec{b}_3, \\vec{b}_5\\} = \\Bigl\\{(1,0,0,0)^T,\\ (0,1,0,0)^T,\\ (0,0,1,0)^T\\Bigr\\}.$"
              ),
               "justificacion_md": "Tres vectores LI que generan $\\text{Col}\\,B$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Base para $\\text{Col}\\,A$ — caso general",
          problema_md=(
              "Halla una base para $\\text{Col}\\,A$ con $A = \\begin{bmatrix} 1 & 4 & 0 & 2 & -1 \\\\ 3 & 12 & 1 & 5 & 5 \\\\ 2 & 8 & 1 & 3 & 2 \\\\ 5 & 20 & 2 & 8 & 8 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Reduciendo $A$ por filas se obtiene una matriz con pivotes en las columnas $1, 3, 5$ (las relaciones $\\vec{a}_2 = 4\\vec{a}_1$ y $\\vec{a}_4 = 2\\vec{a}_1 - \\vec{a}_3$ se verifican)."
              ),
               "justificacion_md": "Las **posiciones** de los pivotes no cambian con OEF — y las relaciones de dependencia entre columnas tampoco.",
               "es_resultado": False},
              {"accion_md": (
                  "**Base de $\\text{Col}\\,A$:** $\\{\\vec{a}_1, \\vec{a}_3, \\vec{a}_5\\}$ — las **columnas originales** de $A$ correspondientes a las posiciones pivote:\n\n"
                  "$\\Bigl\\{(1,3,2,5)^T,\\ (0,1,1,2)^T,\\ (-1,5,2,8)^T\\Bigr\\}.$"
              ),
               "justificacion_md": "**¡Nunca tomes las columnas reducidas!** Estas no están en $\\text{Col}\\,A$ (las OEF cambian las columnas).",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**El método para una base de $\\text{Nul}\\,A$ ya lo conocemos.**\n\n"
            "Resolver $A\\vec{x} = \\vec{0}$ por reducción produce automáticamente vectores generadores $\\vec{v}_1, \\ldots, \\vec{v}_k$ de $\\text{Nul}\\,A$, donde $k$ = número de variables libres.\n\n"
            "**Estos vectores son siempre LI** (cada uno tiene un $1$ en una posición correspondiente a una variable libre distinta), así que **forman base de $\\text{Nul}\\,A$**.\n\n"
            "**Resumen:**\n\n"
            "| Subespacio | Cómo encontrar la base |\n|---|---|\n"
            "| $\\text{Nul}\\,A$ | Resuelve $A\\vec{x} = \\vec{0}$, lee vectores dirección |\n"
            "| $\\text{Col}\\,A$ | Identifica columnas pivote, **toma las originales de $A$** |"
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Para que $\\{\\vec{b}_1, \\ldots, \\vec{b}_p\\}$ sea base de $H$:",
                  "opciones_md": [
                      "Solo necesita ser LI",
                      "Solo necesita generar $H$",
                      "Debe ser LI **y** generar $H$",
                      "Debe ser ortogonal",
                  ],
                  "correcta": "C",
                  "pista_md": "Las dos condiciones de base.",
                  "explicacion_md": "**LI y generar.** Independencia sin generación deja huecos; generación sin independencia incluye redundancia.",
              },
              {
                  "enunciado_md": "Una base de $\\text{Col}\\,A$ se obtiene tomando:",
                  "opciones_md": [
                      "Las columnas pivote de la **forma reducida** de $A$",
                      "Las columnas pivote **originales** de $A$",
                      "Todas las columnas de $A$",
                      "Las filas pivote de $A$",
                  ],
                  "correcta": "B",
                  "pista_md": "Las OEF cambian las columnas, pero no las posiciones pivote.",
                  "explicacion_md": "**Las columnas originales correspondientes a las posiciones pivote.** Las columnas reducidas pertenecen a $\\text{Col}\\,U$, no a $\\text{Col}\\,A$.",
              },
              {
                  "enunciado_md": "Si $H = \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3\\}$ y $\\vec{v}_3 = 2\\vec{v}_1 + \\vec{v}_2$, una base de $H$ es:",
                  "opciones_md": [
                      "$\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3\\}$",
                      "$\\{\\vec{v}_1, \\vec{v}_2\\}$ (si son LI)",
                      "$\\{\\vec{v}_3\\}$",
                      "$\\{\\vec{0}\\}$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\vec{v}_3$ es redundante.",
                  "explicacion_md": "**$\\{\\vec{v}_1, \\vec{v}_2\\}$ si son LI.** Por el teorema del conjunto generador, descartamos $\\vec{v}_3$ y queda un conjunto LI que genera $H$.",
              },
          ]),

        ej(
            "Base de $\\mathbb{R}^3$",
            "¿Es $\\{(1, 0, 1), (0, 1, 1), (1, 1, 0)\\}$ una base de $\\mathbb{R}^3$?",
            [
                "Verifica si la matriz formada por estos vectores es invertible.",
                "Calcula el determinante o reduce a forma escalonada.",
            ],
            (
                "$A = \\begin{bmatrix} 1 & 0 & 1 \\\\ 0 & 1 & 1 \\\\ 1 & 1 & 0 \\end{bmatrix}$. $\\det A = 1(0-1) - 0 + 1(0-1) = -1 - 1 = -2 \\neq 0$.\n\n"
                "$A$ invertible $\\Rightarrow$ por TMI las columnas son LI y generan $\\mathbb{R}^3$ $\\Rightarrow$ **forman base**."
            ),
        ),

        ej(
            "Base para $\\text{Col}\\,A$",
            "Halla una base para $\\text{Col}\\,A$ con $A = \\begin{bmatrix} 1 & 2 & 3 & 1 \\\\ 2 & 4 & 7 & 3 \\\\ 1 & 2 & 4 & 2 \\end{bmatrix}$.",
            [
                "Reduce $A$ a forma escalonada.",
                "Identifica posiciones pivote y toma las columnas originales correspondientes.",
            ],
            (
                "Reduciendo: $A \\sim \\begin{bmatrix} 1 & 2 & 3 & 1 \\\\ 0 & 0 & 1 & 1 \\\\ 0 & 0 & 0 & 0 \\end{bmatrix}$.\n\n"
                "Pivotes en columnas $1, 3$ $\\Rightarrow$ **base de $\\text{Col}\\,A$:** $\\{(1, 2, 1)^T,\\ (3, 7, 4)^T\\}$ (columnas originales)."
            ),
        ),

        ej(
            "Base para $\\text{Nul}\\,A$",
            "Halla una base para $\\text{Nul}\\,A$ con $A = \\begin{bmatrix} 1 & 2 & 0 & -1 \\\\ 0 & 0 & 1 & 2 \\end{bmatrix}$ (ya en RREF).",
            [
                "Variables libres: $x_2, x_4$.",
                "Despeja $x_1, x_3$ y arma vectores dirección.",
            ],
            (
                "$x_1 = -2x_2 + x_4$, $x_3 = -2x_4$. $\\vec{x} = x_2(-2, 1, 0, 0)^T + x_4(1, 0, -2, 1)^T$.\n\n"
                "**Base de $\\text{Nul}\\,A$:** $\\{(-2, 1, 0, 0)^T,\\ (1, 0, -2, 1)^T\\}$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Tomar las columnas reducidas (de la REF) como base de $\\text{Col}\\,A$.** ¡Error! Tomar siempre las **columnas originales** de $A$ correspondientes a las posiciones pivote.",
              "**Decir 'es base' por solo verificar LI o solo generar.** Hay que verificar **ambas** condiciones.",
              "**Confundir $\\text{Col}\\,A$ con $\\text{Col}\\,U$ (forma escalonada).** Estos espacios son **distintos** en general — las OEF cambian las columnas.",
              "**Olvidar que las filas no nulas de la forma escalonada generan el espacio fila** (lección 5.5), no el espacio columna.",
              "**Pensar que toda colección LI es base.** Solo si además **genera** el espacio entero.",
          ]),

        b("resumen",
          puntos_md=[
              "**Base:** conjunto LI que genera el subespacio. Cumple **ambas** condiciones.",
              "**Bases estándar:** $\\{\\vec{e}_i\\}$ en $\\mathbb{R}^n$, $\\{1, t, \\ldots, t^n\\}$ en $\\mathcal{P}_n$, $\\{E_{ij}\\}$ en matrices.",
              "**Teorema del conjunto generador:** todo conjunto generador (no trivial) contiene una base — basta eliminar redundancia.",
              "**Base de $\\text{Nul}\\,A$:** vectores dirección obtenidos al resolver $A\\vec{x} = \\vec{0}$ (uno por variable libre).",
              "**Base de $\\text{Col}\\,A$:** **columnas pivote originales** de $A$ (¡no las reducidas!).",
              "**Próxima lección:** **sistemas de coordenadas** — todo vector se escribe de forma **única** en una base.",
          ]),
    ]
    return {
        "id": "lec-al-5-3-bases",
        "title": "Bases",
        "description": "Definición de base (LI + generar), teorema del conjunto generador, bases para $\\text{Nul}\\,A$ (vectores dirección) y $\\text{Col}\\,A$ (columnas pivote originales).",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 3,
    }


# =====================================================================
# 5.4 Sistemas de coordenadas
# =====================================================================
def lesson_5_4():
    blocks = [
        b("texto", body_md=(
            "Una vez fijada una **base** $\\mathcal{B}$ de un espacio vectorial $V$, **cada vector** $\\vec{x} \\in V$ "
            "se escribe de **manera única** como combinación lineal de los elementos de $\\mathcal{B}$. Los pesos "
            "de esa combinación son las **coordenadas** de $\\vec{x}$ respecto a $\\mathcal{B}$.\n\n"
            "Esto resuelve un problema profundo: **trabajar con espacios abstractos** (como $\\mathcal{P}_n$ o $\\mathbb{R}^{m\\times n}$) **como si fueran $\\mathbb{R}^n$**. La base nos da un 'diccionario' que traduce vectores abstractos a $\\mathbb{R}^n$ y viceversa.\n\n"
            "**Esta es la idea profunda detrás del álgebra lineal:**\n\n"
            "- En la base estándar de $\\mathcal{P}_3$, el polinomio $5 + 2t - t^3$ corresponde al vector $(5, 2, 0, -1)^T \\in \\mathbb{R}^4$.\n"
            "- Sumar polinomios = sumar vectores (entrada a entrada). Un problema en $\\mathcal{P}_3$ se vuelve un problema en $\\mathbb{R}^4$.\n\n"
            "Al terminar:\n\n"
            "- Conoces el **teorema de la representación única**.\n"
            "- Calculas el vector de coordenadas $[\\vec{x}]_{\\mathcal{B}}$ resolviendo un sistema.\n"
            "- Usas la **matriz de cambio de coordenadas** $P_{\\mathcal{B}} = [\\vec{b}_1\\ \\cdots\\ \\vec{b}_n]$.\n"
            "- Reconoces el **mapa de coordenadas** como un **isomorfismo lineal** $V \\cong \\mathbb{R}^n$."
        )),

        b("teorema",
          nombre="Teorema de la representación única",
          enunciado_md=(
              "Sea $\\mathcal{B} = \\{\\vec{b}_1, \\ldots, \\vec{b}_n\\}$ una base de un espacio vectorial $V$. Entonces para cada $\\vec{x} \\in V$ **existe un único** conjunto de escalares $c_1, \\ldots, c_n$ tales que\n\n"
              "$$\\boxed{\\vec{x} = c_1 \\vec{b}_1 + c_2 \\vec{b}_2 + \\cdots + c_n \\vec{b}_n.}$$"
          ),
          demostracion_md=(
              "**Existencia:** $\\mathcal{B}$ genera $V$, así que tales escalares existen.\n\n"
              "**Unicidad:** supongamos $\\vec{x} = \\sum c_i \\vec{b}_i = \\sum d_i \\vec{b}_i$. Restando: $\\vec{0} = \\sum (c_i - d_i)\\vec{b}_i$. Como $\\mathcal{B}$ es LI, todos los coeficientes son cero: $c_i = d_i$. $\\blacksquare$\n\n"
              "**La unicidad es la propiedad clave que distingue una base** de un mero conjunto generador."
          )),

        b("definicion",
          titulo="Coordenadas y vector de coordenadas",
          body_md=(
              "Sea $\\mathcal{B} = \\{\\vec{b}_1, \\ldots, \\vec{b}_n\\}$ una base de $V$ y $\\vec{x} \\in V$. Las **coordenadas de $\\vec{x}$ respecto a $\\mathcal{B}$** (o **$\\mathcal{B}$-coordenadas**) son los únicos escalares $c_1, \\ldots, c_n$ con\n\n"
              "$$\\vec{x} = c_1 \\vec{b}_1 + \\cdots + c_n \\vec{b}_n.$$\n\n"
              "El **vector de coordenadas** de $\\vec{x}$ respecto a $\\mathcal{B}$ es\n\n"
              "$$[\\vec{x}]_{\\mathcal{B}} = \\begin{bmatrix} c_1 \\\\ c_2 \\\\ \\vdots \\\\ c_n \\end{bmatrix} \\in \\mathbb{R}^n.$$\n\n"
              "El mapeo $\\vec{x} \\mapsto [\\vec{x}]_{\\mathcal{B}}$ se llama el **mapa de coordenadas** determinado por $\\mathcal{B}$.\n\n"
              "**Nota importante:** $[\\vec{x}]_{\\mathcal{B}}$ es siempre un vector de $\\mathbb{R}^n$ (con $n = $ dimensión de $V$), aunque $\\vec{x}$ viva en un espacio abstracto."
          )),

        b("ejemplo_resuelto",
          titulo="Recuperar $\\vec{x}$ desde $[\\vec{x}]_{\\mathcal{B}}$",
          problema_md=(
              "Considera la base $\\mathcal{B} = \\{\\vec{b}_1, \\vec{b}_2\\}$ de $\\mathbb{R}^2$ con $\\vec{b}_1 = (1, 0)^T$, $\\vec{b}_2 = (1, 2)^T$. Si $[\\vec{x}]_{\\mathcal{B}} = (-2, 3)^T$, encuentra $\\vec{x}$."
          ),
          pasos=[
              {"accion_md": (
                  "Aplicamos la definición: las coordenadas son los pesos para construir $\\vec{x}$ desde la base.\n\n"
                  "$\\vec{x} = (-2)\\vec{b}_1 + 3\\vec{b}_2 = (-2)\\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix} + 3\\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix} = \\begin{bmatrix} -2 + 3 \\\\ 0 + 6 \\end{bmatrix} = \\begin{bmatrix} 1 \\\\ 6 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Pasar de coordenadas al vector estándar es **directo**: aplicar la combinación lineal.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\vec{x} = (1, 6)^T$.**"
              ),
               "justificacion_md": "El **mismo vector** $\\vec{x}$ tiene distintas representaciones en distintas bases.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Coordenadas en la base estándar",
          problema_md=(
              "Sea $\\vec{x} = (1, 6)^T$ y $\\mathcal{E} = \\{\\vec{e}_1, \\vec{e}_2\\}$ la base estándar de $\\mathbb{R}^2$. Halla $[\\vec{x}]_{\\mathcal{E}}$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\vec{x} = \\begin{bmatrix} 1 \\\\ 6 \\end{bmatrix} = 1\\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix} + 6\\begin{bmatrix} 0 \\\\ 1 \\end{bmatrix} = 1\\,\\vec{e}_1 + 6\\,\\vec{e}_2.$\n\n"
                  "$[\\vec{x}]_{\\mathcal{E}} = (1, 6)^T = \\vec{x}.$"
              ),
               "justificacion_md": "**En la base estándar, $[\\vec{x}]_{\\mathcal{E}} = \\vec{x}$** — las coordenadas coinciden con las entradas usuales.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Matriz de cambio de coordenadas $P_{\\mathcal{B}}$",
          body_md=(
              "Sea $\\mathcal{B} = \\{\\vec{b}_1, \\ldots, \\vec{b}_n\\}$ una base de $\\mathbb{R}^n$. La **matriz de cambio de coordenadas** es\n\n"
              "$$P_{\\mathcal{B}} = [\\,\\vec{b}_1\\ \\vec{b}_2\\ \\cdots\\ \\vec{b}_n\\,] \\in \\mathbb{R}^{n \\times n}.$$\n\n"
              "Es decir, $P_{\\mathcal{B}}$ tiene como columnas los vectores de la base **escritos en sus coordenadas estándar**.\n\n"
              "**Relación fundamental.** Para todo $\\vec{x} \\in \\mathbb{R}^n$:\n\n"
              "$$\\boxed{\\vec{x} = P_{\\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}}, \\qquad [\\vec{x}]_{\\mathcal{B}} = P_{\\mathcal{B}}^{-1}\\,\\vec{x}.}$$\n\n"
              "$P_{\\mathcal{B}}$ siempre es **invertible** (sus columnas forman base $\\Rightarrow$ son LI por TMI)."
          )),

        b("ejemplo_resuelto",
          titulo="Calcular $[\\vec{x}]_{\\mathcal{B}}$ en $\\mathbb{R}^2$",
          problema_md=(
              "Sean $\\vec{b}_1 = (2, 1)^T$, $\\vec{b}_2 = (-1, 1)^T$ y $\\vec{x} = (4, 5)^T$. Halla $[\\vec{x}]_{\\mathcal{B}}$."
          ),
          pasos=[
              {"accion_md": (
                  "Buscamos $c_1, c_2$ con $\\vec{x} = c_1 \\vec{b}_1 + c_2 \\vec{b}_2$, es decir, $P_{\\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}} = \\vec{x}$:\n\n"
                  "$\\begin{bmatrix} 2 & -1 \\\\ 1 & 1 \\end{bmatrix} \\begin{bmatrix} c_1 \\\\ c_2 \\end{bmatrix} = \\begin{bmatrix} 4 \\\\ 5 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Sistema lineal estándar.",
               "es_resultado": False},
              {"accion_md": (
                  "Reduciendo: $\\left[\\begin{array}{rr|r} 2 & -1 & 4 \\\\ 1 & 1 & 5 \\end{array}\\right] \\sim \\left[\\begin{array}{rr|r} 1 & 0 & 3 \\\\ 0 & 1 & 2 \\end{array}\\right]$.\n\n"
                  "$c_1 = 3, c_2 = 2 \\Rightarrow [\\vec{x}]_{\\mathcal{B}} = (3, 2)^T.$\n\n"
                  "**Verificación:** $3\\vec{b}_1 + 2\\vec{b}_2 = 3(2,1) + 2(-1,1) = (6 - 2, 3 + 2) = (4, 5)$ ✓."
              ),
               "justificacion_md": "Resolver $P_{\\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}} = \\vec{x}$ por Gauss-Jordan.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Mapa de coordenadas como isomorfismo",
          enunciado_md=(
              "Sea $\\mathcal{B} = \\{\\vec{b}_1, \\ldots, \\vec{b}_n\\}$ una base de un espacio vectorial $V$. El mapa de coordenadas\n\n"
              "$$\\vec{x} \\longmapsto [\\vec{x}]_{\\mathcal{B}}$$\n\n"
              "es una **transformación lineal uno a uno** de $V$ sobre $\\mathbb{R}^n$. En particular, $V$ es **isomorfo** a $\\mathbb{R}^n$, denotado $V \\cong \\mathbb{R}^n$."
          ),
          demostracion_md=(
              "**Lineal:** sean $\\vec{u} = \\sum c_i \\vec{b}_i$ y $\\vec{w} = \\sum d_i \\vec{b}_i$. Entonces $\\vec{u} + \\vec{w} = \\sum(c_i + d_i)\\vec{b}_i$, así $[\\vec{u} + \\vec{w}]_{\\mathcal{B}} = (c_i + d_i) = [\\vec{u}]_{\\mathcal{B}} + [\\vec{w}]_{\\mathcal{B}}$. Análogo para escalar.\n\n"
              "**Inyectiva:** si $[\\vec{u}]_{\\mathcal{B}} = [\\vec{w}]_{\\mathcal{B}}$, los pesos coinciden y $\\vec{u} = \\vec{w}$.\n\n"
              "**Sobreyectiva:** dado $(c_1, \\ldots, c_n) \\in \\mathbb{R}^n$, el vector $\\vec{x} = \\sum c_i \\vec{b}_i$ tiene esas coordenadas. $\\blacksquare$\n\n"
              "**Isomorfismo** = correspondencia biyectiva que preserva las operaciones. Significa que $V$ y $\\mathbb{R}^n$ son **'el mismo espacio'** desde el punto de vista del álgebra lineal."
          )),

        b("ejemplo_resuelto",
          titulo="Polinomios y $\\mathbb{R}^4$",
          problema_md=(
              "Sea $\\mathcal{B} = \\{1, t, t^2, t^3\\}$ la base estándar de $\\mathcal{P}_3$. Halla $[p]_{\\mathcal{B}}$ para $p(t) = 5 - 2t + 4t^3$."
          ),
          pasos=[
              {"accion_md": (
                  "Identificamos $p(t) = 5\\cdot 1 + (-2)\\cdot t + 0 \\cdot t^2 + 4\\cdot t^3$. Los coeficientes son las coordenadas:\n\n"
                  "$[p]_{\\mathcal{B}} = (5, -2, 0, 4)^T \\in \\mathbb{R}^4.$"
              ),
               "justificacion_md": "**En la base estándar de polinomios**, las coordenadas son simplemente los coeficientes.",
               "es_resultado": False},
              {"accion_md": (
                  "**El isomorfismo $\\mathcal{P}_3 \\cong \\mathbb{R}^4$:** todo problema de polinomios (sumar, multiplicar por escalar, decidir LI) se reduce a un problema en $\\mathbb{R}^4$ vía coordenadas."
              ),
               "justificacion_md": "**Esta es la idea poderosa:** trabajar en cualquier espacio de dimensión $n$ es trabajar en $\\mathbb{R}^n$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Independencia lineal de polinomios vía coordenadas",
          problema_md=(
              "Verifica si los polinomios $1 + 2t^2$, $4 + t + 5t^2$, $3 + 2t$ son LI o LD en $\\mathcal{P}_2$."
          ),
          pasos=[
              {"accion_md": (
                  "Mapeamos a coordenadas en la base estándar $\\{1, t, t^2\\}$:\n\n"
                  "$1 + 2t^2 \\leftrightarrow (1, 0, 2)^T$, $\\quad 4 + t + 5t^2 \\leftrightarrow (4, 1, 5)^T$, $\\quad 3 + 2t \\leftrightarrow (3, 2, 0)^T$."
              ),
               "justificacion_md": "Convertir el problema abstracto a un problema en $\\mathbb{R}^3$.",
               "es_resultado": False},
              {"accion_md": (
                  "Formamos $A = \\begin{bmatrix} 1 & 4 & 3 \\\\ 0 & 1 & 2 \\\\ 2 & 5 & 0 \\end{bmatrix}$ y reducimos:\n\n"
                  "$A \\sim \\begin{bmatrix} 1 & 4 & 3 \\\\ 0 & 1 & 2 \\\\ 0 & 0 & 0 \\end{bmatrix}.$\n\n"
                  "Solo $2$ pivotes en $3$ columnas $\\Rightarrow$ columnas LD $\\Rightarrow$ los polinomios son **LD**."
              ),
               "justificacion_md": "**Lección clave:** problemas de polinomios resueltos con técnicas de matrices.",
               "es_resultado": False},
              {"accion_md": (
                  "Relación explícita: $3 + 2t = 2(4 + t + 5t^2) - 5(1 + 2t^2)$ (verificable por sustitución)."
              ),
               "justificacion_md": "Las relaciones de dependencia se trasladan del espacio de coordenadas al espacio original.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $\\mathcal{B} = \\{\\vec{b}_1, \\vec{b}_2, \\vec{b}_3\\}$ y $[\\vec{x}]_{\\mathcal{B}} = (1, -2, 4)^T$, entonces $\\vec{x}$ vale:",
                  "opciones_md": [
                      "$(1, -2, 4)^T$",
                      "$\\vec{b}_1 - 2\\vec{b}_2 + 4\\vec{b}_3$",
                      "$\\vec{b}_1 + \\vec{b}_2 + \\vec{b}_3$",
                      "$P_{\\mathcal{B}}^{-1}(1, -2, 4)^T$",
                  ],
                  "correcta": "B",
                  "pista_md": "Las coordenadas son los pesos de la combinación lineal.",
                  "explicacion_md": "**$\\vec{x} = 1\\vec{b}_1 + (-2)\\vec{b}_2 + 4\\vec{b}_3$.** Las coordenadas son los pesos de la combinación lineal en la base.",
              },
              {
                  "enunciado_md": "La matriz de cambio de coordenadas $P_{\\mathcal{B}}$ es:",
                  "opciones_md": [
                      "Diagonal",
                      "Simétrica",
                      "Tiene los vectores de $\\mathcal{B}$ como columnas",
                      "Tiene los vectores de $\\mathcal{B}$ como filas",
                  ],
                  "correcta": "C",
                  "pista_md": "Definición de $P_{\\mathcal{B}}$.",
                  "explicacion_md": "**Las columnas de $P_{\\mathcal{B}}$ son los vectores $\\vec{b}_i$.** Esto la hace siempre invertible (columnas LI por ser base).",
              },
              {
                  "enunciado_md": "El mapa de coordenadas $V \\to \\mathbb{R}^n$ es:",
                  "opciones_md": [
                      "Inyectivo pero no sobreyectivo",
                      "Sobreyectivo pero no inyectivo",
                      "Un isomorfismo (lineal y biyectivo)",
                      "No lineal en general",
                  ],
                  "correcta": "C",
                  "pista_md": "Lineal + biyectivo = isomorfismo.",
                  "explicacion_md": "**Isomorfismo.** Por eso $V \\cong \\mathbb{R}^n$ siempre que $V$ tenga dimensión $n$ — todos los espacios vectoriales reales de dimensión $n$ son 'el mismo'.",
              },
          ]),

        ej(
            "Coordenadas en $\\mathbb{R}^3$",
            "Sean $\\vec{b}_1 = (1, 0, 2)^T$, $\\vec{b}_2 = (0, 1, 1)^T$, $\\vec{b}_3 = (1, 1, 0)^T$ y $\\vec{x} = (2, 3, 1)^T$. Halla $[\\vec{x}]_{\\mathcal{B}}$.",
            [
                "Resuelve $P_{\\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}} = \\vec{x}$.",
                "Aplica Gauss-Jordan al sistema.",
            ],
            (
                "$P_{\\mathcal{B}} = \\begin{bmatrix} 1 & 0 & 1 \\\\ 0 & 1 & 1 \\\\ 2 & 1 & 0 \\end{bmatrix}$. Resolvemos $P_{\\mathcal{B}}\\vec{c} = (2, 3, 1)^T$.\n\n"
                "Reduciendo $[P_{\\mathcal{B}}\\mid\\vec{x}]$ se obtiene $c_1 = 0, c_2 = 1, c_3 = 2$. **$[\\vec{x}]_{\\mathcal{B}} = (0, 1, 2)^T$.**\n\n"
                "Verificación: $0\\vec{b}_1 + 1\\vec{b}_2 + 2\\vec{b}_3 = (0, 1, 1) + (2, 2, 0) = (2, 3, 1) = \\vec{x}$ ✓."
            ),
        ),

        ej(
            "Coordenadas en $\\mathcal{P}_2$",
            "Considera $\\mathcal{B} = \\{1, 1+t, 1+t+t^2\\}$ como base de $\\mathcal{P}_2$. Halla $[p]_{\\mathcal{B}}$ para $p(t) = 1 + 2t + 3t^2$.",
            [
                "Plantea $p = c_1 \\cdot 1 + c_2(1+t) + c_3(1+t+t^2)$ y compara coeficientes.",
            ],
            (
                "Expandimos: $c_1 + c_2(1+t) + c_3(1+t+t^2) = (c_1 + c_2 + c_3) + (c_2 + c_3)t + c_3 t^2$.\n\n"
                "Igualando con $1 + 2t + 3t^2$: $c_3 = 3$, $c_2 + c_3 = 2 \\Rightarrow c_2 = -1$, $c_1 + c_2 + c_3 = 1 \\Rightarrow c_1 = -1$.\n\n"
                "**$[p]_{\\mathcal{B}} = (-1, -1, 3)^T$.**"
            ),
        ),

        ej(
            "LI de matrices vía coordenadas",
            "Sean $A_1 = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}, A_2 = \\begin{bmatrix} 0 & 1 \\\\ 1 & 0 \\end{bmatrix}, A_3 = \\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix}$. ¿Son LI en $\\mathbb{R}^{2\\times 2}$?",
            [
                "Mapea cada matriz a $\\mathbb{R}^4$ vía la base estándar $\\{E_{11}, E_{12}, E_{21}, E_{22}\\}$.",
                "Estudia LI en $\\mathbb{R}^4$.",
            ],
            (
                "Coordenadas: $[A_1] = (1,0,0,1)^T$, $[A_2] = (0,1,1,0)^T$, $[A_3] = (1,1,1,1)^T$.\n\n"
                "Notamos que $A_3 = A_1 + A_2$, es decir $(1,1,1,1) = (1,0,0,1) + (0,1,1,0)$ ✓.\n\n"
                "**Por tanto son LD** — el conjunto $\\{A_1, A_2, A_3\\}$ no es base de $\\mathbb{R}^{2\\times 2}$ (que tiene dimensión $4$)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\vec{x}$ con $[\\vec{x}]_{\\mathcal{B}}$.** Son **objetos distintos**: $\\vec{x} \\in V$ (abstracto), $[\\vec{x}]_{\\mathcal{B}} \\in \\mathbb{R}^n$ (siempre).",
              "**Olvidar que el resultado depende de la base.** Distintas bases dan distintos vectores de coordenadas para **el mismo $\\vec{x}$**.",
              "**Multiplicar $\\vec{x}$ por $P_{\\mathcal{B}}$ esperando obtener las coordenadas.** Lo correcto: $[\\vec{x}]_{\\mathcal{B}} = P_{\\mathcal{B}}^{-1}\\vec{x}$. La inversa, no la directa.",
              "**Pensar que el isomorfismo $V \\cong \\mathbb{R}^n$ significa que son 'literalmente iguales'.** Significa que tienen la **misma estructura**, pero los objetos son distintos (polinomios vs n-tuplas).",
              "**Construir $P_{\\mathcal{B}}$ con las filas en lugar de las columnas.** Convención: vectores de la base como **columnas**.",
          ]),

        b("resumen",
          puntos_md=[
              "**Representación única:** dado $\\mathcal{B}$ base, todo $\\vec{x}$ se escribe **únicamente** como $\\sum c_i \\vec{b}_i$.",
              "**Vector de coordenadas:** $[\\vec{x}]_{\\mathcal{B}} = (c_1, \\ldots, c_n)^T \\in \\mathbb{R}^n$.",
              "**Matriz de cambio:** $P_{\\mathcal{B}} = [\\vec{b}_1\\ \\cdots\\ \\vec{b}_n]$ (vectores de base como columnas). Invertible.",
              "**Relación clave:** $\\vec{x} = P_{\\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}}$ y $[\\vec{x}]_{\\mathcal{B}} = P_{\\mathcal{B}}^{-1}\\vec{x}$.",
              "**Mapa de coordenadas $V \\to \\mathbb{R}^n$:** isomorfismo lineal. **$V \\cong \\mathbb{R}^n$**.",
              "**Práctica:** problemas en $\\mathcal{P}_n$, $\\mathbb{R}^{m\\times n}$ se reducen a problemas en $\\mathbb{R}^k$ vía coordenadas.",
              "**Próxima lección:** **dimensión y rango** — el invariante numérico que captura el 'tamaño' de un espacio vectorial.",
          ]),
    ]
    return {
        "id": "lec-al-5-4-coordenadas",
        "title": "Sistemas de coordenadas",
        "description": "Teorema de la representación única, vector de coordenadas $[\\vec{x}]_{\\mathcal{B}}$, matriz de cambio $P_{\\mathcal{B}}$, mapa de coordenadas como isomorfismo $V \\cong \\mathbb{R}^n$.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 4,
    }


# =====================================================================
# 5.5 Dimensión y rango
# =====================================================================
def lesson_5_5():
    blocks = [
        b("texto", body_md=(
            "La **dimensión** de un espacio vectorial es el número de vectores en cualquier base. "
            "Es una **propiedad intrínseca** del espacio: no depende de la base elegida.\n\n"
            "Esta lección establece los resultados centrales sobre dimensión y conecta el concepto con "
            "el **rango** de una matriz, que ya conocemos como número de pivotes.\n\n"
            "El resultado más importante es el **teorema del rango**:\n\n"
            "$$\\text{rango}(A) + \\dim(\\text{Nul}\\,A) = n,$$\n\n"
            "donde $n$ es el número de **columnas** de $A$. Conecta la geometría de los dos subespacios fundamentales asociados a una matriz.\n\n"
            "Al terminar:\n\n"
            "- Conoces la definición de **dimensión** y por qué está bien definida.\n"
            "- Calculas $\\dim(\\text{Nul}\\,A)$ y $\\dim(\\text{Col}\\,A)$ para cualquier $A$.\n"
            "- Aplicas el **teorema del rango** y el **TMI extendido** con dimensiones."
        )),

        b("teorema",
          enunciado_md=(
              "**Cualquier conjunto en $V$ con más vectores que la base es LD.**\n\n"
              "Si $V$ tiene una base $\\mathcal{B} = \\{\\vec{b}_1, \\ldots, \\vec{b}_n\\}$, entonces cualquier conjunto $\\{\\vec{u}_1, \\ldots, \\vec{u}_p\\}$ en $V$ con $p > n$ debe ser **linealmente dependiente**."
          ),
          demostracion_md=(
              "Pasamos a coordenadas: los vectores $[\\vec{u}_1]_{\\mathcal{B}}, \\ldots, [\\vec{u}_p]_{\\mathcal{B}}$ están en $\\mathbb{R}^n$. Como $p > n$, por T2 (más vectores que entradas) son LD en $\\mathbb{R}^n$. Como el mapa de coordenadas es lineal e inyectivo, los $\\vec{u}_i$ son LD en $V$. $\\blacksquare$"
          )),

        b("teorema",
          enunciado_md=(
              "**Toda base de $V$ tiene el mismo número de vectores.**\n\n"
              "Si $V$ tiene una base con $n$ vectores, entonces cualquier otra base de $V$ debe tener exactamente $n$ vectores."
          ),
          demostracion_md=(
              "Sean $\\mathcal{B}_1$ con $n$ vectores y $\\mathcal{B}_2$ otra base. Por el teorema previo, $\\mathcal{B}_2$ no puede tener más de $n$ vectores. Por simetría (intercambiando los roles), $\\mathcal{B}_1$ no puede tener más de $|\\mathcal{B}_2|$. Luego $|\\mathcal{B}_2| = n$. $\\blacksquare$"
          )),

        b("definicion",
          titulo="Dimensión",
          body_md=(
              "Si $V$ se genera por un conjunto finito, decimos que $V$ tiene **dimensión finita**. La **dimensión** de $V$, denotada $\\dim V$, es el **número de vectores en cualquier base** de $V$.\n\n"
              "**Casos especiales:**\n\n"
              "- $\\dim\\{\\vec{0}\\} = 0$ (subespacio trivial: dimensión cero).\n"
              "- Si $V$ no es generado por ningún conjunto finito, decimos que $V$ tiene **dimensión infinita** (ej. funciones continuas $C[0, 1]$).\n\n"
              "**Dimensiones de los espacios estándar:**\n\n"
              "| Espacio | Base estándar | Dimensión |\n|---|---|---|\n"
              "| $\\mathbb{R}^n$ | $\\{\\vec{e}_1, \\ldots, \\vec{e}_n\\}$ | $n$ |\n"
              "| $\\mathcal{P}_n$ | $\\{1, t, t^2, \\ldots, t^n\\}$ | $n + 1$ |\n"
              "| $\\mathbb{R}^{m\\times n}$ | $\\{E_{ij}\\}$ | $mn$ |"
          )),

        b("ejemplo_resuelto",
          titulo="Dimensión de un subespacio generado",
          problema_md=(
              "Sea $H = \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2\\}$ con $\\vec{v}_1 = (3, 6, 2)^T$, $\\vec{v}_2 = (-1, 0, 1)^T$. Calcula $\\dim H$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\vec{v}_1, \\vec{v}_2$ no son colineales (no son uno múltiplo del otro), así que son LI."
              ),
               "justificacion_md": "T1: dos vectores son LD $\\iff$ uno es múltiplo del otro.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\{\\vec{v}_1, \\vec{v}_2\\}$ es LI y genera $H$ $\\Rightarrow$ es base de $H$ $\\Rightarrow$ $\\dim H = 2$."
              ),
               "justificacion_md": "**Geométricamente:** $H$ es un plano por el origen en $\\mathbb{R}^3$ (dim 2).",
               "es_resultado": True},
          ]),

        b("teorema",
          enunciado_md=(
              "**Subespacios y dimensión.** Sea $H$ un subespacio de un espacio $V$ de dimensión finita. Entonces:\n\n"
              "**(a)** $H$ tiene dimensión finita y $\\dim H \\leq \\dim V$.\n\n"
              "**(b)** Cualquier conjunto LI en $H$ se puede **extender** a una base de $H$.\n\n"
              "**(c)** Si $\\dim V = n$ y $S$ es un conjunto de **exactamente $n$ vectores LI** en $V$, entonces $S$ es **automáticamente** base de $V$ (no hace falta verificar generación).\n\n"
              "**(d)** Análogamente, $n$ vectores que generen $V$ son automáticamente LI."
          )),

        formulas(
            titulo="Dimensiones de $\\text{Nul}\\,A$ y $\\text{Col}\\,A$",
            body=(
                "Sea $A \\in \\mathbb{R}^{m \\times n}$.\n\n"
                "$$\\boxed{\\dim(\\text{Nul}\\,A) = \\text{número de variables libres en } A\\vec{x} = \\vec{0}.}$$\n\n"
                "$$\\boxed{\\dim(\\text{Col}\\,A) = \\text{número de columnas pivote de } A.}$$\n\n"
                "**Para hallar ambas:** reducir $A$ a forma escalonada y contar pivotes (= dim Col $A$) y columnas sin pivote (= dim Nul $A$)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="$\\dim(\\text{Nul}\\,A)$ y $\\dim(\\text{Col}\\,A)$",
          problema_md=(
              "Halla $\\dim(\\text{Nul}\\,A)$ y $\\dim(\\text{Col}\\,A)$ para $A = \\begin{bmatrix} -3 & 6 & -1 & 1 & -7 \\\\ 1 & -2 & 2 & 3 & -1 \\\\ 2 & -4 & 5 & 8 & -4 \\end{bmatrix}$."
          ),
          pasos=[
              {"accion_md": (
                  "Reduciendo $A$ se obtienen pivotes en columnas $1$ y $3$ (lección 5.2 con esta misma matriz). Las variables libres son $x_2, x_4, x_5$ (3 variables libres)."
              ),
               "justificacion_md": "REF: $\\begin{bmatrix} 1 & -2 & 0 & -1 & 3 \\\\ 0 & 0 & 1 & 2 & -2 \\\\ 0 & 0 & 0 & 0 & 0 \\end{bmatrix}$.",
               "es_resultado": False},
              {"accion_md": (
                  "$\\dim(\\text{Col}\\,A) = 2$ (dos columnas pivote).\n\n"
                  "$\\dim(\\text{Nul}\\,A) = 3$ (tres variables libres)."
              ),
               "justificacion_md": "Verificamos: $\\dim(\\text{Col}\\,A) + \\dim(\\text{Nul}\\,A) = 2 + 3 = 5 = $ # columnas — consistente con el teorema del rango.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Espacio fila y rango",
          body_md=(
              "El **espacio fila** de $A$, denotado $\\text{Fila}\\,A$, es el subespacio de $\\mathbb{R}^n$ generado por las **filas** de $A$. Equivalentemente, $\\text{Fila}\\,A = \\text{Col}(A^T)$.\n\n"
              "**Rango de $A$:**\n\n"
              "$$\\text{rango}(A) = \\dim(\\text{Col}\\,A) = \\dim(\\text{Fila}\\,A) = \\text{número de pivotes de } A.$$\n\n"
              "(El hecho de que $\\dim(\\text{Col}\\,A) = \\dim(\\text{Fila}\\,A)$ es no trivial: ambas dimensiones coinciden con el número de pivotes.)\n\n"
              "**Atajo:** las filas no nulas de la REF de $A$ forman base del **espacio fila** (no del espacio columna)."
          )),

        b("teorema",
          nombre="Teorema del rango",
          enunciado_md=(
              "Sea $A \\in \\mathbb{R}^{m \\times n}$. Entonces\n\n"
              "$$\\boxed{\\text{rango}(A) + \\dim(\\text{Nul}\\,A) = n,}$$\n\n"
              "donde $n$ es el **número de columnas** de $A$.\n\n"
              "**Lectura:** las $n$ columnas de $A$ se 'reparten' entre las que aportan algo nuevo (rango = pivotes) y las redundantes (= variables libres = dim Nul $A$)."
          ),
          demostracion_md=(
              "Las columnas pivote son $\\text{rango}(A)$ y dan base de $\\text{Col}\\,A$. Las columnas sin pivote son $n - \\text{rango}(A)$ y corresponden a las variables libres en $A\\vec{x} = \\vec{0}$, es decir, $\\dim(\\text{Nul}\\,A) = n - \\text{rango}(A)$. Reordenando: $\\text{rango}(A) + \\dim(\\text{Nul}\\,A) = n$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Aplicación del teorema del rango",
          problema_md=(
              "**(a)** Si $A$ es $7 \\times 9$ con $\\dim(\\text{Nul}\\,A) = 2$, halla $\\text{rango}(A)$.\n\n"
              "**(b)** ¿Puede una matriz $6 \\times 9$ tener $\\dim(\\text{Nul}\\,A) = 2$?"
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Por el teorema del rango: $\\text{rango}(A) + 2 = 9 \\Rightarrow \\text{rango}(A) = 7$."
              ),
               "justificacion_md": "$n = $ número de columnas $= 9$.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Si $\\dim(\\text{Nul}\\,A) = 2$, entonces $\\text{rango}(A) = 9 - 2 = 7$. Pero $\\text{Col}\\,A \\subseteq \\mathbb{R}^6 \\Rightarrow \\dim(\\text{Col}\\,A) \\leq 6$. Como $\\text{rango}(A) = \\dim(\\text{Col}\\,A) \\leq 6 < 7$, **es imposible**.\n\n"
                  "**Una matriz $6 \\times 9$ NO puede tener $\\dim(\\text{Nul}\\,A) = 2$.** El máximo posible es $\\dim(\\text{Nul}\\,A) = 9 - 6 = 3$."
              ),
               "justificacion_md": "**Lección general:** $\\text{rango}(A) \\leq \\min(m, n)$ — hay un límite estructural.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="TMI extendido (con dimensiones)",
          enunciado_md=(
              "Para $A \\in \\mathbb{R}^{n \\times n}$, las siguientes son **equivalentes** a las del TMI clásico (lección 3.3) y constituyen su extensión natural:\n\n"
              "**(m)** Las columnas de $A$ forman una **base de $\\mathbb{R}^n$**.\n\n"
              "**(n)** $\\text{Col}\\,A = \\mathbb{R}^n$.\n\n"
              "**(ñ)** $\\dim(\\text{Col}\\,A) = n$.\n\n"
              "**(o)** $\\text{rango}(A) = n$.\n\n"
              "**(p)** $\\text{Nul}\\,A = \\{\\vec{0}\\}$.\n\n"
              "**(q)** $\\dim(\\text{Nul}\\,A) = 0$."
          )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $V$ tiene dimensión $5$ y tomamos $5$ vectores LI en $V$, entonces:",
                  "opciones_md": [
                      "Forman base automáticamente",
                      "Solo si además generan $V$",
                      "Necesariamente generan un subespacio propio",
                      "Necesariamente son redundantes",
                  ],
                  "correcta": "A",
                  "pista_md": "Teorema: $n$ vectores LI en un espacio de dim $n$ son base.",
                  "explicacion_md": "**Forman base automáticamente.** $n$ vectores LI en un espacio de dimensión $n$ generan automáticamente todo el espacio.",
              },
              {
                  "enunciado_md": "Si $A \\in \\mathbb{R}^{3\\times 5}$ tiene $\\text{rango}(A) = 3$, entonces $\\dim(\\text{Nul}\\,A)$ vale:",
                  "opciones_md": ["$0$", "$2$", "$3$", "$5$"],
                  "correcta": "B",
                  "pista_md": "Teorema del rango con $n = 5$.",
                  "explicacion_md": "**$\\dim(\\text{Nul}\\,A) = 5 - 3 = 2$.** Hay $2$ variables libres en $A\\vec{x} = \\vec{0}$.",
              },
              {
                  "enunciado_md": "Para una matriz cuadrada $A \\in \\mathbb{R}^{n\\times n}$, '$A$ invertible' equivale a:",
                  "opciones_md": [
                      "$\\text{rango}(A) = n$",
                      "$\\dim(\\text{Nul}\\,A) = 0$",
                      "Las columnas son base de $\\mathbb{R}^n$",
                      "**Todas las anteriores**",
                  ],
                  "correcta": "D",
                  "pista_md": "TMI extendido.",
                  "explicacion_md": "**Todas son equivalentes** por TMI. Cada una caracteriza la invertibilidad desde un ángulo distinto.",
              },
          ]),

        ej(
            "Calcular dimensión de subespacio",
            "Sea $H = \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_3, \\vec{v}_4\\}$ con $\\vec{v}_1 = (1, 5, 0, 0), \\vec{v}_2 = (-3, 0, 1, 0), \\vec{v}_3 = (6, 0, -2, 0), \\vec{v}_4 = (0, 4, -1, 5)$. Halla $\\dim H$.",
            [
                "Forma una matriz con los vectores como columnas y reduce.",
                "Cuenta pivotes.",
            ],
            (
                "Notamos que $\\vec{v}_3 = -2\\vec{v}_2$ (verificable). Lo descartamos: $H = \\text{Gen}\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_4\\}$.\n\n"
                "Verificamos LI de $\\{\\vec{v}_1, \\vec{v}_2, \\vec{v}_4\\}$ formando matriz y reduciendo: las 3 columnas son LI (cada una tiene un pivote distinto).\n\n"
                "**$\\dim H = 3$.**"
            ),
        ),

        ej(
            "Aplicar teorema del rango",
            "Una matriz $A$ tiene $4$ filas, $7$ columnas y $\\text{rango}(A) = 3$. Halla $\\dim(\\text{Nul}\\,A)$ y $\\dim(\\text{Col}\\,A)$. ¿Es $A\\vec{x} = \\vec{b}$ consistente para todo $\\vec{b}$?",
            [
                "Aplica $\\text{rango} + \\dim\\text{Nul} = n$.",
                "$\\text{Col}\\,A \\subseteq \\mathbb{R}^4$ con $\\dim = $ rango.",
            ],
            (
                "$\\dim(\\text{Col}\\,A) = \\text{rango}(A) = 3$.\n\n"
                "Por teorema del rango: $\\dim(\\text{Nul}\\,A) = 7 - 3 = 4$.\n\n"
                "**Consistencia para todo $\\vec{b}$:** requeriría $\\text{Col}\\,A = \\mathbb{R}^4$, pero $\\dim(\\text{Col}\\,A) = 3 < 4$. Por tanto **NO** — existen $\\vec{b}$ para los cuales el sistema es inconsistente."
            ),
        ),

        ej(
            "TMI con dimensiones",
            "Sea $A$ una matriz $5 \\times 5$ con $\\dim(\\text{Nul}\\,A) = 0$. ¿Es $A$ invertible? Justifica usando varias condiciones del TMI.",
            [
                "Aplica el teorema del rango.",
                "Aplica TMI extendido.",
            ],
            (
                "Por teorema del rango: $\\text{rango}(A) = 5 - 0 = 5$.\n\n"
                "Por TMI extendido (q): $\\dim(\\text{Nul}\\,A) = 0 \\iff A$ invertible.\n\n"
                "Equivalentemente: rango $= n = 5 \\Rightarrow$ pivote en cada columna $\\Rightarrow$ columnas LI $\\Rightarrow$ columnas base de $\\mathbb{R}^5$ $\\Rightarrow$ $\\text{Col}\\,A = \\mathbb{R}^5$ $\\Rightarrow$ $A$ invertible."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que la dimensión depende de la base.** No: por el teorema, **toda base tiene el mismo número de vectores**.",
              "**Confundir $\\dim V$ con cardinalidad de $V$.** $\\mathbb{R}^2$ tiene infinitos elementos, pero dimensión $2$.",
              "**Olvidar que $\\dim(\\text{Col}\\,A)$ y $\\dim(\\text{Fila}\\,A)$ coinciden.** Ambos son el rango.",
              "**Aplicar teorema del rango con $m$ (filas).** El teorema usa $n$ (**columnas**): $\\text{rango}(A) + \\dim(\\text{Nul}\\,A) = n$.",
              "**Pensar que $\\text{rango}(A) = \\min(m, n)$ siempre.** Es solo el **máximo** posible; el rango real puede ser menor.",
          ]),

        b("resumen",
          puntos_md=[
              "**Dimensión:** número de vectores en cualquier base. Independiente de la base elegida.",
              "**Casos clave:** $\\dim\\mathbb{R}^n = n$, $\\dim\\mathcal{P}_n = n+1$, $\\dim\\mathbb{R}^{m\\times n} = mn$.",
              "**Para subespacios:** $\\dim H \\leq \\dim V$, y $n$ vectores LI en un espacio de dim $n$ son base.",
              "**$\\dim(\\text{Nul}\\,A)$:** número de **variables libres** de $A\\vec{x} = \\vec{0}$.",
              "**$\\dim(\\text{Col}\\,A) = \\text{rango}(A)$:** número de **columnas pivote**.",
              "**Teorema del rango:** $\\text{rango}(A) + \\dim(\\text{Nul}\\,A) = n$.",
              "**TMI extendido:** $A \\in \\mathbb{R}^{n\\times n}$ invertible $\\iff \\text{rango} = n \\iff \\dim(\\text{Nul}\\,A) = 0 \\iff$ columnas son base de $\\mathbb{R}^n$.",
              "**Próxima lección:** **cambio de coordenadas** entre dos bases distintas.",
          ]),
    ]
    return {
        "id": "lec-al-5-5-dimension-rango",
        "title": "Dimensión y rango",
        "description": "Dimensión como número de vectores en una base, $\\dim(\\text{Nul}\\,A)$ y $\\dim(\\text{Col}\\,A)$, teorema del rango $\\text{rango}(A) + \\dim(\\text{Nul}\\,A) = n$, TMI extendido.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 5,
    }


# =====================================================================
# 5.6 Cambio de coordenadas
# =====================================================================
def lesson_5_6():
    blocks = [
        b("texto", body_md=(
            "Cuando elegimos una base $\\mathcal{B}$ de un espacio vectorial $V$ de dimensión $n$, "
            "el vector de coordenadas $[\\vec{x}]_{\\mathcal{B}}$ proporciona un sistema de referencia para $V$. "
            "**El mismo vector tiene distintas coordenadas en distintas bases.**\n\n"
            "En esta lección estudiamos cómo **traducir entre coordenadas** de dos bases distintas $\\mathcal{B}$ y $\\mathcal{C}$ "
            "del mismo espacio. Este proceso se llama **cambio de coordenadas** y está descrito por una matriz "
            "$P_{\\mathcal{C} \\leftarrow \\mathcal{B}}$ con la propiedad\n\n"
            "$$[\\vec{x}]_{\\mathcal{C}} = P_{\\mathcal{C} \\leftarrow \\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}}.$$\n\n"
            "Este cambio aparece en muchos contextos:\n\n"
            "- **Física e ingeniería:** cambiar de coordenadas cartesianas a coordenadas adaptadas al problema.\n"
            "- **Computación gráfica:** rotaciones y cambios de cámara.\n"
            "- **Análisis numérico:** elegir bases que faciliten cálculos (ortonormales, autovectores, etc.).\n\n"
            "Al terminar:\n\n"
            "- Construyes $P_{\\mathcal{C} \\leftarrow \\mathcal{B}}$ usando los $\\mathcal{C}$-coordenadas de los $\\vec{b}_i$.\n"
            "- Aplicas el algoritmo $[\\,\\mathcal{C} \\mid \\mathcal{B}\\,] \\to [\\,I \\mid P_{\\mathcal{C} \\leftarrow \\mathcal{B}}\\,]$.\n"
            "- Conoces la relación $P_{\\mathcal{C} \\leftarrow \\mathcal{B}} = (P_{\\mathcal{B} \\leftarrow \\mathcal{C}})^{-1}$."
        )),

        b("ejemplo_resuelto",
          titulo="Cambio de base — caso introductorio",
          problema_md=(
              "Sean $\\mathcal{B} = \\{\\vec{b}_1, \\vec{b}_2\\}$ y $\\mathcal{C} = \\{\\vec{c}_1, \\vec{c}_2\\}$ dos bases de un espacio $V$ tales que $\\vec{b}_1 = 4\\vec{c}_1 + \\vec{c}_2$ y $\\vec{b}_2 = -6\\vec{c}_1 + \\vec{c}_2$. Si $[\\vec{x}]_{\\mathcal{B}} = (3, 1)^T$, halla $[\\vec{x}]_{\\mathcal{C}}$."
          ),
          pasos=[
              {"accion_md": (
                  "$\\vec{x} = 3\\vec{b}_1 + 1\\vec{b}_2$. Aplicando linealidad del mapa $[\\cdot]_{\\mathcal{C}}$:\n\n"
                  "$[\\vec{x}]_{\\mathcal{C}} = 3[\\vec{b}_1]_{\\mathcal{C}} + [\\vec{b}_2]_{\\mathcal{C}}.$"
              ),
               "justificacion_md": "El mapa de coordenadas es **lineal**.",
               "es_resultado": False},
              {"accion_md": (
                  "Por hipótesis: $[\\vec{b}_1]_{\\mathcal{C}} = (4, 1)^T$ y $[\\vec{b}_2]_{\\mathcal{C}} = (-6, 1)^T$.\n\n"
                  "$[\\vec{x}]_{\\mathcal{C}} = 3(4, 1)^T + (-6, 1)^T = (12 - 6,\\ 3 + 1)^T = (6, 4)^T.$"
              ),
               "justificacion_md": "Combinación lineal componente a componente.",
               "es_resultado": False},
              {"accion_md": (
                  "Equivalentemente: $[\\vec{x}]_{\\mathcal{C}} = \\begin{bmatrix} 4 & -6 \\\\ 1 & 1 \\end{bmatrix}\\begin{bmatrix} 3 \\\\ 1 \\end{bmatrix} = \\begin{bmatrix} 6 \\\\ 4 \\end{bmatrix}.$\n\n"
                  "**$[\\vec{x}]_{\\mathcal{C}} = (6, 4)^T$.**"
              ),
               "justificacion_md": "Esta matriz es exactamente $P_{\\mathcal{C} \\leftarrow \\mathcal{B}}$ — su construcción se generaliza a continuación.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Matriz de cambio de coordenadas $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$",
          body_md=(
              "Sean $\\mathcal{B} = \\{\\vec{b}_1, \\ldots, \\vec{b}_n\\}$ y $\\mathcal{C} = \\{\\vec{c}_1, \\ldots, \\vec{c}_n\\}$ dos bases de un espacio vectorial $V$. **Existe una única matriz** $P_{\\mathcal{C}\\leftarrow\\mathcal{B}} \\in \\mathbb{R}^{n \\times n}$ tal que para todo $\\vec{x} \\in V$:\n\n"
              "$$\\boxed{[\\vec{x}]_{\\mathcal{C}} = P_{\\mathcal{C}\\leftarrow\\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}}.}$$\n\n"
              "**Construcción.** Las **columnas** de $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ son los **$\\mathcal{C}$-coordenadas de los vectores de $\\mathcal{B}$**:\n\n"
              "$$P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = \\bigl[\\,[\\vec{b}_1]_{\\mathcal{C}}\\ \\ [\\vec{b}_2]_{\\mathcal{C}}\\ \\cdots\\ [\\vec{b}_n]_{\\mathcal{C}}\\,\\bigr].$$\n\n"
              "**Mnemónico para la notación:** $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ 'lee la flecha al revés': transforma $\\mathcal{B}$-coordenadas en $\\mathcal{C}$-coordenadas."
          )),

        b("ejemplo_resuelto",
          titulo="Cambio de base en $\\mathbb{R}^2$",
          problema_md=(
              "Sean $\\vec{b}_1 = (-9, 1)^T$, $\\vec{b}_2 = (-5, -1)^T$, $\\vec{c}_1 = (1, -4)^T$, $\\vec{c}_2 = (3, -5)^T$. Halla $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$."
          ),
          pasos=[
              {"accion_md": (
                  "Necesitamos $[\\vec{b}_1]_{\\mathcal{C}}$ y $[\\vec{b}_2]_{\\mathcal{C}}$. Es decir, escribir $\\vec{b}_i = \\alpha \\vec{c}_1 + \\beta \\vec{c}_2$ y leer $(\\alpha, \\beta)$.\n\n"
                  "Para $\\vec{b}_1 = (-9, 1)$: planteamos $\\alpha(1, -4) + \\beta(3, -5) = (-9, 1)$. Resolviendo: $\\alpha = 6$, $\\beta = -5$. **$[\\vec{b}_1]_{\\mathcal{C}} = (6, -5)^T$.**"
              ),
               "justificacion_md": "Resolver un sistema $2 \\times 2$ por cada $\\vec{b}_i$.",
               "es_resultado": False},
              {"accion_md": (
                  "Para $\\vec{b}_2 = (-5, -1)$: similarmente $\\alpha = 4$, $\\beta = -3$. **$[\\vec{b}_2]_{\\mathcal{C}} = (4, -3)^T$.**\n\n"
                  "Por tanto: $P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = \\begin{bmatrix} 6 & 4 \\\\ -5 & -3 \\end{bmatrix}.$"
              ),
               "justificacion_md": "Yuxtaponemos los $\\mathcal{C}$-coordenadas como columnas.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Algoritmo para $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$",
          enunciado_md=(
              "Para calcular $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ entre dos bases de $\\mathbb{R}^n$:\n\n"
              "1. Forma la **matriz aumentada** $[\\,\\vec{c}_1\\ \\vec{c}_2\\ \\cdots\\ \\vec{c}_n \\mid \\vec{b}_1\\ \\vec{b}_2\\ \\cdots\\ \\vec{b}_n\\,]$.\n"
              "2. Reduce por filas hasta forma escalonada **reducida**.\n"
              "3. El bloque izquierdo se convierte en $I_n$ y el bloque derecho contiene $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$:\n\n"
              "$$[\\,\\mathcal{C} \\mid \\mathcal{B}\\,] \\quad \\xrightarrow{\\text{OEF}} \\quad [\\,I_n \\mid P_{\\mathcal{C}\\leftarrow\\mathcal{B}}\\,].$$"
          ),
          demostracion_md=(
              "Resolver simultáneamente los $n$ sistemas $\\vec{c}_1 c_{1j} + \\cdots + \\vec{c}_n c_{nj} = \\vec{b}_j$ para $j = 1, \\ldots, n$ se hace formando $[\\mathcal{C} \\mid \\mathcal{B}]$ y reduciendo. Cada columna del bloque derecho es la solución $[\\vec{b}_j]_{\\mathcal{C}}$. $\\blacksquare$"
          )),

        b("ejemplo_resuelto",
          titulo="Algoritmo $[\\mathcal{C} \\mid \\mathcal{B}]$ — caso $\\mathbb{R}^2$",
          problema_md=(
              "Sean $\\vec{b}_1 = (1, -3)^T$, $\\vec{b}_2 = (-2, 4)^T$, $\\vec{c}_1 = (-7, 9)^T$, $\\vec{c}_2 = (-5, 7)^T$. (a) Halla $P_{\\mathcal{B}\\leftarrow\\mathcal{C}}$. (b) Halla $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$."
          ),
          pasos=[
              {"accion_md": (
                  "**(a)** Para $P_{\\mathcal{B}\\leftarrow\\mathcal{C}}$, necesitamos $[\\vec{c}_j]_{\\mathcal{B}}$. Construimos $[\\mathcal{B} \\mid \\mathcal{C}]$ y reducimos:\n\n"
                  "$\\left[\\begin{array}{rr|rr} 1 & -2 & -7 & -5 \\\\ -3 & 4 & 9 & 7 \\end{array}\\right] \\sim \\left[\\begin{array}{rr|rr} 1 & 0 & 5 & 3 \\\\ 0 & 1 & 6 & 4 \\end{array}\\right].$"
              ),
               "justificacion_md": "Reducción estándar de Gauss-Jordan.",
               "es_resultado": False},
              {"accion_md": (
                  "$P_{\\mathcal{B}\\leftarrow\\mathcal{C}} = \\begin{bmatrix} 5 & 3 \\\\ 6 & 4 \\end{bmatrix}.$"
              ),
               "justificacion_md": "El bloque derecho final.",
               "es_resultado": False},
              {"accion_md": (
                  "**(b)** Por la propiedad $P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = (P_{\\mathcal{B}\\leftarrow\\mathcal{C}})^{-1}$:\n\n"
                  "$P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = \\dfrac{1}{20 - 18}\\begin{bmatrix} 4 & -3 \\\\ -6 & 5 \\end{bmatrix} = \\dfrac{1}{2}\\begin{bmatrix} 4 & -3 \\\\ -6 & 5 \\end{bmatrix} = \\begin{bmatrix} 2 & -3/2 \\\\ -3 & 5/2 \\end{bmatrix}.$"
              ),
               "justificacion_md": "**Truco computacional:** una vez calculada una de las dos matrices, la otra se obtiene invirtiendo.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Propiedades clave del cambio de coordenadas",
            body=(
                "Sean $\\mathcal{B}, \\mathcal{C}, \\mathcal{D}$ tres bases de $V$.\n\n"
                "| Propiedad | Fórmula |\n|---|---|\n"
                "| **Inversa** | $P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = (P_{\\mathcal{B}\\leftarrow\\mathcal{C}})^{-1}$ |\n"
                "| **Composición** | $P_{\\mathcal{D}\\leftarrow\\mathcal{B}} = P_{\\mathcal{D}\\leftarrow\\mathcal{C}}\\,P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ |\n"
                "| **Identidad** | $P_{\\mathcal{B}\\leftarrow\\mathcal{B}} = I_n$ |\n"
                "| **Caso $V = \\mathbb{R}^n$, $\\mathcal{C} = \\mathcal{E}$ (estándar)** | $P_{\\mathcal{E}\\leftarrow\\mathcal{B}} = P_{\\mathcal{B}}$ (definida en lección 5.4) |\n\n"
                "**Mnemónico de las flechas:** $P_{\\mathcal{D}\\leftarrow\\mathcal{B}} = P_{\\mathcal{D}\\leftarrow\\mathcal{C}}\\,P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ — las $\\mathcal{C}$ se 'cancelan' como un cambio de variable encadenado."
            ),
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Las columnas de $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ son:",
                  "opciones_md": [
                      "Los vectores $\\vec{b}_i$ en sus coordenadas estándar",
                      "Los vectores $\\vec{c}_i$ en sus coordenadas estándar",
                      "Los $\\mathcal{C}$-coordenadas de los $\\vec{b}_i$",
                      "Los $\\mathcal{B}$-coordenadas de los $\\vec{c}_i$",
                  ],
                  "correcta": "C",
                  "pista_md": "La matriz transforma $[\\vec{x}]_{\\mathcal{B}} \\to [\\vec{x}]_{\\mathcal{C}}$.",
                  "explicacion_md": "**$[\\vec{b}_i]_{\\mathcal{C}}$ como columnas.** Esto es lo que hace que $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}\\,[\\vec{b}_i]_{\\mathcal{B}} = [\\vec{b}_i]_{\\mathcal{C}}$ (con $[\\vec{b}_i]_{\\mathcal{B}} = \\vec{e}_i$).",
              },
              {
                  "enunciado_md": "$P_{\\mathcal{C}\\leftarrow\\mathcal{B}} \\cdot P_{\\mathcal{B}\\leftarrow\\mathcal{C}}$ vale:",
                  "opciones_md": [
                      "$P_{\\mathcal{B}\\leftarrow\\mathcal{B}} = I$",
                      "$P_{\\mathcal{C}\\leftarrow\\mathcal{C}} = I$",
                      "$\\mathbf{0}$",
                      "Depende de las bases",
                  ],
                  "correcta": "B",
                  "pista_md": "Componer cambios de coordenadas equivale a un cambio total.",
                  "explicacion_md": "**$P_{\\mathcal{C}\\leftarrow\\mathcal{C}} = I$.** Las flechas se componen: $\\mathcal{C}\\leftarrow\\mathcal{B}\\leftarrow\\mathcal{C}$ es lo mismo que $\\mathcal{C}\\leftarrow\\mathcal{C}$ (no cambia).",
              },
              {
                  "enunciado_md": "Para usar el algoritmo $[\\mathcal{C}\\mid\\mathcal{B}] \\to [I\\mid P_{\\mathcal{C}\\leftarrow\\mathcal{B}}]$, ¿qué bases ponemos a la izquierda?",
                  "opciones_md": [
                      "$\\mathcal{B}$",
                      "$\\mathcal{C}$ (la base destino)",
                      "Ambas mezcladas",
                      "La estándar siempre",
                  ],
                  "correcta": "B",
                  "pista_md": "La base destino debe quedar como identidad tras la reducción.",
                  "explicacion_md": "**$\\mathcal{C}$ a la izquierda.** Reducimos a $I$ porque al hacerlo, los vectores $\\vec{b}_i$ del lado derecho se convierten en sus $\\mathcal{C}$-coordenadas.",
              },
          ]),

        ej(
            "Cambio de base en $\\mathbb{R}^2$",
            "Sean $\\mathcal{B} = \\{(1, 0), (1, 1)\\}$ y $\\mathcal{C} = \\{(2, 1), (1, 2)\\}$ bases de $\\mathbb{R}^2$. Halla $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$.",
            [
                "Aplica el algoritmo $[\\mathcal{C}\\mid\\mathcal{B}] \\to [I \\mid P_{\\mathcal{C}\\leftarrow\\mathcal{B}}]$.",
            ],
            (
                "$\\left[\\begin{array}{rr|rr} 2 & 1 & 1 & 1 \\\\ 1 & 2 & 0 & 1 \\end{array}\\right] \\sim \\left[\\begin{array}{rr|rr} 1 & 0 & 2/3 & 1/3 \\\\ 0 & 1 & -1/3 & 1/3 \\end{array}\\right]$.\n\n"
                "$P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = \\dfrac{1}{3}\\begin{bmatrix} 2 & 1 \\\\ -1 & 1 \\end{bmatrix}.$"
            ),
        ),

        ej(
            "Aplicar matriz de cambio",
            "Con $P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = \\begin{bmatrix} 1 & 2 \\\\ -1 & 3 \\end{bmatrix}$ y $[\\vec{x}]_{\\mathcal{B}} = (4, -1)^T$, halla $[\\vec{x}]_{\\mathcal{C}}$ y $[\\vec{x}]_{\\mathcal{B}}$ a partir de $[\\vec{x}]_{\\mathcal{C}}$.",
            [
                "Multiplicación directa para $[\\vec{x}]_{\\mathcal{C}}$.",
                "Para invertir, calcula $P_{\\mathcal{B}\\leftarrow\\mathcal{C}} = (P_{\\mathcal{C}\\leftarrow\\mathcal{B}})^{-1}$.",
            ],
            (
                "$[\\vec{x}]_{\\mathcal{C}} = \\begin{bmatrix} 1 & 2 \\\\ -1 & 3 \\end{bmatrix}\\begin{bmatrix} 4 \\\\ -1 \\end{bmatrix} = \\begin{bmatrix} 2 \\\\ -7 \\end{bmatrix}.$\n\n"
                "$P_{\\mathcal{B}\\leftarrow\\mathcal{C}} = (P_{\\mathcal{C}\\leftarrow\\mathcal{B}})^{-1} = \\dfrac{1}{5}\\begin{bmatrix} 3 & -2 \\\\ 1 & 1 \\end{bmatrix}$.\n\n"
                "Verificación: $P_{\\mathcal{B}\\leftarrow\\mathcal{C}}\\,[\\vec{x}]_{\\mathcal{C}} = \\dfrac{1}{5}\\begin{bmatrix} 3 & -2 \\\\ 1 & 1 \\end{bmatrix}\\begin{bmatrix} 2 \\\\ -7 \\end{bmatrix} = \\dfrac{1}{5}\\begin{bmatrix} 20 \\\\ -5 \\end{bmatrix} = \\begin{bmatrix} 4 \\\\ -1 \\end{bmatrix} = [\\vec{x}]_{\\mathcal{B}}$ ✓."
            ),
        ),

        ej(
            "Cambio de base en $\\mathbb{R}^3$",
            "Sean $\\mathcal{B} = \\{(1,0,0), (1,1,0), (1,1,1)\\}$ y $\\mathcal{C} = $ base estándar de $\\mathbb{R}^3$. Halla $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ y $P_{\\mathcal{B}\\leftarrow\\mathcal{C}}$.",
            [
                "Cuando $\\mathcal{C}$ es la estándar, $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ tiene como columnas los vectores de $\\mathcal{B}$ directamente.",
            ],
            (
                "$P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = \\begin{bmatrix} 1 & 1 & 1 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 1 \\end{bmatrix}$ (los $\\vec{b}_i$ como columnas, ya están en coordenadas estándar).\n\n"
                "$P_{\\mathcal{B}\\leftarrow\\mathcal{C}} = (P_{\\mathcal{C}\\leftarrow\\mathcal{B}})^{-1} = \\begin{bmatrix} 1 & -1 & 0 \\\\ 0 & 1 & -1 \\\\ 0 & 0 & 1 \\end{bmatrix}$ (inversa de triangular superior unitaria, fácil de calcular)."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir las flechas: $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ vs. $P_{\\mathcal{B}\\leftarrow\\mathcal{C}}$.** Lectura: la base **destino** está a la izquierda.",
              "**Construir la matriz con los vectores de $\\mathcal{B}$ en lugar de sus $\\mathcal{C}$-coordenadas.** Las **columnas** son $[\\vec{b}_i]_{\\mathcal{C}}$, no $\\vec{b}_i$ directamente (salvo si $\\mathcal{C}$ = estándar).",
              "**Olvidar invertir cuando se quiere ir 'al revés'.** $P_{\\mathcal{B}\\leftarrow\\mathcal{C}} = (P_{\\mathcal{C}\\leftarrow\\mathcal{B}})^{-1}$.",
              "**Aplicar el algoritmo $[\\mathcal{B}\\mid\\mathcal{C}]$ esperando obtener $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$.** Lo correcto es **al revés**: $[\\mathcal{C}\\mid\\mathcal{B}]$ produce $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$.",
              "**Pensar que el cambio de coordenadas cambia el vector.** El **vector** $\\vec{x}$ es el mismo; solo cambia su **representación** $[\\vec{x}]$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Cambio de coordenadas:** matriz $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ tal que $[\\vec{x}]_{\\mathcal{C}} = P_{\\mathcal{C}\\leftarrow\\mathcal{B}}\\,[\\vec{x}]_{\\mathcal{B}}$.",
              "**Construcción:** las columnas de $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$ son $[\\vec{b}_i]_{\\mathcal{C}}$.",
              "**Algoritmo:** $[\\,\\mathcal{C} \\mid \\mathcal{B}\\,] \\xrightarrow{\\text{OEF}} [\\,I \\mid P_{\\mathcal{C}\\leftarrow\\mathcal{B}}\\,]$.",
              "**Inversa:** $P_{\\mathcal{C}\\leftarrow\\mathcal{B}} = (P_{\\mathcal{B}\\leftarrow\\mathcal{C}})^{-1}$.",
              "**Composición:** $P_{\\mathcal{D}\\leftarrow\\mathcal{B}} = P_{\\mathcal{D}\\leftarrow\\mathcal{C}}\\,P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$.",
              "**Caso especial $\\mathcal{C}$ = estándar:** $P_{\\mathcal{E}\\leftarrow\\mathcal{B}}$ tiene los $\\vec{b}_i$ como columnas directamente.",
              "**Cierre del capítulo:** ya tenemos todo el lenguaje (espacios, subespacios, bases, dimensión, coordenadas) para abordar los temas avanzados.",
              "**Próximo capítulo:** **valores y vectores propios** — los vectores 'preferidos' de una transformación lineal.",
          ]),
    ]
    return {
        "id": "lec-al-5-6-cambio-coordenadas",
        "title": "Cambio de coordenadas",
        "description": "Matriz de cambio de coordenadas $P_{\\mathcal{C}\\leftarrow\\mathcal{B}}$, algoritmo $[\\mathcal{C}\\mid\\mathcal{B}]\\to[I\\mid P_{\\mathcal{C}\\leftarrow\\mathcal{B}}]$, propiedades (inversa y composición).",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "algebra-lineal"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(
            f"Curso {course_id} no existe. Corre primero seed_algebra_lineal_chapter_1.py"
        )

    chapter_id = "ch-al-espacios-subespacios"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Espacios y Subespacios Vectoriales",
        "description": (
            "Espacio vectorial abstracto y axiomas; subespacios y subespacio generado; "
            "espacios notables ($\\text{Nul}\\,A$, $\\text{Col}\\,A$, núcleo y rango de TL); "
            "bases, sistemas de coordenadas, dimensión y rango (teorema del rango), y cambio de coordenadas."
        ),
        "order": 5,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [lesson_5_1, lesson_5_2, lesson_5_3, lesson_5_4, lesson_5_5, lesson_5_6]
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
        f"✅ Capítulo 5 — Espacios y Subespacios Vectoriales listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
