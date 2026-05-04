"""
Seed del Capítulo 2 — Derivadas (curso Cálculo Diferencial).
11 lecciones que cubren todo el contenido de las guías oficiales:
  2.1 Definición y notación (ya existe, se preserva)
  2.2 Derivabilidad
  2.3 Reglas de derivación
  2.4 Derivadas trigonométricas
  2.5 Regla de la cadena
  2.6 Derivación implícita
  2.7 Derivación logarítmica
  2.8 Derivadas de funciones inversas
  2.9 Derivadas de funciones logarítmicas y exponenciales
  2.10 Regla de L'Hôpital
  2.11 Funciones hiperbólicas

Idempotente: borra y re-inserta las lecciones 2..11 (sin tocar la 2.1).
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


def now():
    return datetime.now(timezone.utc).isoformat()


# ============ helpers para ejercicios y figuras ============
STYLE = (
    "Estilo: diagrama educativo limpio, fondo blanco, lineas claras, etiquetas "
    "en espanol, notacion matematica renderizada con buena tipografia. Acentos "
    "de color suaves (teal #06b6d4 y ambar #f59e0b). Sin sombras dramaticas, "
    "sin texturas. Apto para libro universitario."
)


def ej(titulo, enunciado, pistas, solucion):
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def fig(prompt):
    return b("figura", image_url="", caption_md="", prompt_image_md=prompt)


# =====================================================================
# LECCIÓN 2.2 — Derivabilidad
# =====================================================================
def lesson_2_2():
    blocks = [
        b("texto", body_md=(
            "Una vez definida la derivada como un límite, surge la pregunta natural: **¿toda función tiene derivada en todo punto?** "
            "La respuesta es **no**. Esta lección explora cuándo una función es **derivable** y cuándo no.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar la **definición de derivada con $h$** para verificar si $f$ es derivable en un punto.\n"
            "- Comprender la relación **derivable $\\Rightarrow$ continua** (y por qué la recíproca falla).\n"
            "- Estudiar la derivabilidad de **funciones definidas por tramos** en los puntos de cambio.\n"
            "- Reconocer las tres fuentes típicas de **no derivabilidad**: discontinuidad, esquina y tangente vertical."
        )),

        b("intuicion",
          titulo="¿Qué significa que $f$ sea derivable en $a$?",
          body_md=(
              "Geométricamente, **$f$ es derivable en $a$** si la gráfica de $f$ admite una **recta tangente bien definida** en $(a, f(a))$. Eso requiere dos cosas:\n\n"
              "1. **La función está definida y es continua en $a$.** No tiene saltos ni huecos.\n"
              "2. **La curva es \"suave\" allí.** No tiene esquinas ni cambios bruscos de dirección.\n\n"
              "Cuando esto falla, el cociente incremental no se estabiliza en un único valor cuando $h \\to 0$, y el límite no existe."
          )),

        b("definicion",
          titulo="Derivada en un punto (con $h$)",
          body_md=(
              "Decimos que $f$ es **derivable en $a$** si el siguiente límite existe y es finito:\n\n"
              "$$f'(a) = \\lim_{h \\to 0} \\dfrac{f(a+h) - f(a)}{h}$$\n\n"
              "Si el límite no existe (no coinciden los laterales, da infinito, o uno de los términos no está definido), entonces $f$ **no es derivable** en $a$.\n\n"
              "Esta es la herramienta fundamental para verificar derivabilidad **punto a punto**, sobre todo en funciones definidas por tramos o con valor absoluto."
          )),

        b("ejemplo_resuelto",
          titulo="Estudiar la derivabilidad de $f(x) = x^2$ en $x = 3$",
          problema_md="Verificar si $f(x) = x^2$ es derivable en $x = 3$ y, en ese caso, calcular $f'(3)$.",
          pasos=[
              {"accion_md": "Aplicamos la definición con $h$:\n\n$$f'(3) = \\lim_{h \\to 0} \\dfrac{f(3+h) - f(3)}{h} = \\lim_{h \\to 0} \\dfrac{(3+h)^2 - 9}{h}$$",
               "justificacion_md": "Sustituimos $a = 3$ en la definición.",
               "es_resultado": False},
              {"accion_md": "Desarrollamos $(3+h)^2 = 9 + 6h + h^2$:\n\n$$\\lim_{h \\to 0} \\dfrac{9 + 6h + h^2 - 9}{h} = \\lim_{h \\to 0} \\dfrac{6h + h^2}{h} = \\lim_{h \\to 0}(6 + h)$$",
               "justificacion_md": "Cancelamos $h$ del numerador y del denominador. Esto es legítimo porque $h \\to 0$ pero $h \\neq 0$.",
               "es_resultado": False},
              {"accion_md": "$f'(3) = 6$.",
               "justificacion_md": "El límite existe y es finito, por lo tanto $f$ es derivable en $x = 3$ y la derivada vale $6$.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Derivabilidad implica continuidad",
          enunciado_md=(
              "Si $f$ es **derivable en $a$**, entonces $f$ es **continua en $a$**.\n\n"
              "Equivalentemente (contrapositiva): si $f$ **no es continua** en $a$, entonces $f$ **no es derivable** en $a$."
          ),
          demostracion_md=(
              "Queremos mostrar que $\\lim_{x \\to a} f(x) = f(a)$. Escribimos:\n\n"
              "$$f(x) - f(a) = \\dfrac{f(x) - f(a)}{x - a} \\cdot (x - a)$$\n\n"
              "El primer factor tiende a $f'(a)$ (existe por hipótesis), y el segundo factor tiende a $0$. Por tanto:\n\n"
              "$$\\lim_{x \\to a}[f(x) - f(a)] = f'(a) \\cdot 0 = 0$$\n\n"
              "Es decir, $\\lim_{x \\to a} f(x) = f(a)$, que es la definición de continuidad."
          )),

        b("intuicion",
          titulo="La recíproca es falsa",
          body_md=(
              "**Continuidad NO implica derivabilidad.** El ejemplo canónico es $f(x) = |x|$ en $x = 0$:\n\n"
              "- Es **continua** en $0$ (la gráfica no se corta).\n"
              "- **No es derivable** en $0$ (la gráfica forma una **esquina**).\n\n"
              "El cociente incremental $\\dfrac{|h|}{h}$ vale $+1$ por la derecha y $-1$ por la izquierda: los laterales del límite no coinciden, así que el límite no existe."
          )),

        b("ejemplo_resuelto",
          titulo="Función por tramos: $f(x) = \\begin{cases} x^2 & x \\le 1 \\\\ 2x - 1 & x > 1 \\end{cases}$ en $x = 1$",
          problema_md="Estudiar si $f$ es continua y derivable en $x = 1$.",
          pasos=[
              {"accion_md": "**Continuidad en $x = 1$.** Calculamos los laterales:\n\n- $\\lim_{x \\to 1^-} f(x) = 1^2 = 1$\n- $\\lim_{x \\to 1^+} f(x) = 2(1) - 1 = 1$\n- $f(1) = 1^2 = 1$\n\nLos tres valores coinciden: $f$ **es continua** en $x = 1$.",
               "justificacion_md": "Antes de mirar la derivabilidad, verificamos la continuidad: si fallara, ya sabríamos que no es derivable.",
               "es_resultado": False},
              {"accion_md": "**Derivabilidad en $x = 1$.** Calculamos los laterales del cociente incremental.\n\n**Lateral por la izquierda** ($h < 0$, entonces $1+h < 1$, usamos $x^2$):\n\n$$\\lim_{h \\to 0^-} \\dfrac{(1+h)^2 - 1}{h} = \\lim_{h \\to 0^-} \\dfrac{2h + h^2}{h} = \\lim_{h \\to 0^-}(2 + h) = 2$$",
               "justificacion_md": "Para $h$ negativo cercano a $0$, $1+h$ está aún en el primer tramo, así $f(1+h) = (1+h)^2$.",
               "es_resultado": False},
              {"accion_md": "**Lateral por la derecha** ($h > 0$, entonces $1+h > 1$, usamos $2x-1$):\n\n$$\\lim_{h \\to 0^+} \\dfrac{(2(1+h) - 1) - 1}{h} = \\lim_{h \\to 0^+} \\dfrac{2h}{h} = 2$$",
               "justificacion_md": "Para $h$ positivo cercano a $0$, $1+h$ está en el segundo tramo, así $f(1+h) = 2(1+h) - 1$.",
               "es_resultado": False},
              {"accion_md": "Como ambos laterales valen $2$, el límite existe y $f'(1) = 2$. **$f$ es derivable** en $x = 1$.",
               "justificacion_md": "Conclusión: pese a estar definida por tramos, en el punto de cambio la función es derivable porque los pendientes laterales coinciden.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Función con esquina: $f(x) = \\dfrac{x^2}{|x|}$ en $x = 0$",
          problema_md="Estudiar si $f(x) = \\dfrac{x^2}{|x|}$ admite una extensión continua y derivable en $x = 0$.",
          pasos=[
              {"accion_md": "Para $x \\neq 0$, $\\dfrac{x^2}{|x|} = \\dfrac{|x|^2}{|x|} = |x|$. Es decir, $f(x) = |x|$ en su dominio natural, y la extensión por continuidad da $f(0) = 0$.",
               "justificacion_md": "Simplificamos antes de estudiar el punto problemático.",
               "es_resultado": False},
              {"accion_md": "**Derivada en $0$.** El cociente incremental:\n\n$$\\lim_{h \\to 0} \\dfrac{|h| - 0}{h} = \\lim_{h \\to 0} \\dfrac{|h|}{h}$$\n\nLaterales:\n\n- Por la derecha: $\\dfrac{h}{h} = 1$\n- Por la izquierda: $\\dfrac{-h}{h} = -1$",
               "justificacion_md": "$|h| = h$ si $h > 0$ y $|h| = -h$ si $h < 0$.",
               "es_resultado": False},
              {"accion_md": "Los laterales son distintos ($1 \\neq -1$), así que el límite **no existe**. **$f$ NO es derivable** en $x = 0$.",
               "justificacion_md": "Geométricamente: la gráfica de $|x|$ tiene una **esquina** en el origen — pendientes distintas a izquierda y derecha. Es continua pero no derivable, justo el contraejemplo de la recíproca del teorema.",
               "es_resultado": True},
          ]),

        b("grafico_desmos",
          desmos_url="",
          expresiones=[
              "f(x) = |x|",
              "g(x) = x^2",
          ],
          guia_md=(
              "Compara $|x|$ (no derivable en $0$, esquina) con $x^2$ (derivable en todo $\\mathbb{R}$, suave). "
              "Ambas son continuas en $0$, pero solo la segunda admite una recta tangente bien definida en el origen."
          ),
          altura=380),

        b("definicion",
          titulo="Tres fuentes de no derivabilidad",
          body_md=(
              "Una función $f$ deja de ser derivable en $a$ por una (o más) de estas tres razones:\n\n"
              "1. **$f$ no es continua en $a$.** Salto, hueco, asíntota vertical. La derivabilidad requiere continuidad.\n\n"
              "2. **$f$ tiene una esquina en $a$.** Es continua, pero las pendientes laterales son distintas. Ej.: $|x|$ en $0$.\n\n"
              "3. **$f$ tiene tangente vertical en $a$.** El cociente incremental tiende a $\\pm \\infty$. Ej.: $f(x) = \\sqrt[3]{x}$ en $0$, o $f(x) = \\sqrt{x}$ en $0$ por la derecha.\n\n"
              "Si **ninguna** de estas situaciones ocurre, $f$ es derivable en $a$."
          )),

        b("verificacion",
          intro_md="Verifica que distingues continuidad y derivabilidad:",
          preguntas=[
              {
                  "enunciado_md": "Si $f$ es continua en $a$, ¿qué se puede afirmar sobre $f'(a)$?",
                  "opciones_md": [
                      "$f'(a)$ siempre existe.",
                      "$f'(a)$ existe solo si los laterales del cociente incremental coinciden.",
                      "$f'(a)$ nunca existe.",
                      "$f'(a)$ vale $0$.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "**Continuidad no implica derivabilidad** (la recíproca del teorema es falsa). $f$ puede ser continua y aún así tener una esquina o una tangente vertical en $a$. "
                      "La derivabilidad pide más: que el límite del cociente incremental exista, lo que requiere que los laterales coincidan."
                  ),
              },
              {
                  "enunciado_md": "Para $f(x) = \\begin{cases} 3x + 2 & x \\le 0 \\\\ x^2 + 2 & x > 0 \\end{cases}$, ¿qué ocurre en $x = 0$?",
                  "opciones_md": [
                      "$f$ no es continua, por tanto no es derivable.",
                      "$f$ es continua y derivable; $f'(0) = 3$.",
                      "$f$ es continua pero no derivable: pendientes laterales $3$ y $0$.",
                      "$f$ es continua y derivable; $f'(0) = 0$.",
                  ],
                  "correcta": "C",
                  "explicacion_md": (
                      "**Continuidad:** ambos tramos valen $2$ en $0$, y $f(0) = 2$. **Continua.** "
                      "**Derivabilidad:** la pendiente por izquierda es $3$ (de $3x+2$), por derecha es $2x|_{x=0} = 0$ (de $x^2+2$). "
                      "Como $3 \\neq 0$, hay una **esquina**: $f$ es continua pero no derivable."
                  ),
              },
          ]),

        ej(
            "Derivada por definición en un punto",
            "Calcula $f'(2)$ usando la definición $f'(a) = \\lim_{h \\to 0} \\dfrac{f(a+h) - f(a)}{h}$ para $f(x) = x^2 - 3x$.",
            [
                "Calcula $f(2+h)$ y $f(2)$ por separado y simplifica el cociente incremental.",
                "Cancela el factor $h$ del denominador antes de tomar el límite.",
            ],
            "**Paso 1 — Evaluar.** $f(2) = 4 - 6 = -2$ y $f(2+h) = (2+h)^2 - 3(2+h) = 4 + 4h + h^2 - 6 - 3h = -2 + h + h^2$.\n\n**Paso 2 — Cociente incremental.** $\\dfrac{f(2+h) - f(2)}{h} = \\dfrac{-2 + h + h^2 - (-2)}{h} = \\dfrac{h + h^2}{h} = 1 + h$ (con $h \\neq 0$).\n\n**Paso 3 — Tomar límite.** $f'(2) = \\lim_{h \\to 0}(1 + h) = 1$.\n\n**Verificación con regla:** $f'(x) = 2x - 3$, así $f'(2) = 1$. ✓",
        ),
        ej(
            "Continuidad y derivabilidad de una función con valor absoluto",
            "Sea $f(x) = x|x - 1|$. Estudia la continuidad y derivabilidad de $f$ en $x = 1$.",
            [
                "Reescribe $f$ por tramos abriendo el valor absoluto en $x = 1$.",
                "En el punto $x = 1$ usa los cocientes incrementales laterales para decidir derivabilidad.",
            ],
            "**Paso 1 — Función por tramos.** $f(x) = \\begin{cases} x(1 - x) = x - x^2 & x < 1 \\\\ x(x - 1) = x^2 - x & x \\geq 1 \\end{cases}$.\n\n**Paso 2 — Continuidad en 1.** $\\lim_{x \\to 1^-}(x - x^2) = 0$ y $\\lim_{x \\to 1^+}(x^2 - x) = 0$, y $f(1) = 0$. **Continua en $x = 1$**.\n\n**Paso 3 — Derivabilidad lateral.**\n- Por izquierda: derivada de $x - x^2$ en $1$ es $1 - 2(1) = -1$.\n- Por derecha: derivada de $x^2 - x$ en $1$ es $2(1) - 1 = 1$.\n\nComo $-1 \\neq 1$, los cocientes incrementales laterales no coinciden: **$f$ no es derivable en $x = 1$** (esquina).",
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir continuidad con derivabilidad.** Continuidad es necesaria pero no suficiente: $|x|$ es el contraejemplo clásico.",
              "**Olvidar verificar la continuidad antes de la derivabilidad** en una función por tramos. Si los tramos no \"pegan\", no hay derivabilidad — sin importar las pendientes.",
              "**Calcular las derivadas de cada tramo y compararlas en el punto de cambio en lugar de usar la definición.** El método correcto en el punto de cambio es **el cociente incremental por izquierda y por derecha** con la definición. Comparar derivadas tramo a tramo solo funciona si ya se sabe que $f$ es continua y suave dentro de cada tramo.",
              "**Asumir que una tangente vertical implica derivabilidad infinita.** En realidad, una tangente vertical en $a$ significa que el límite del cociente incremental es $\\pm \\infty$ — y por convención eso se considera **no derivable** (la derivada como número real no existe).",
          ]),

        b("resumen",
          puntos_md=[
              "**Derivable en $a$** $\\iff$ existe $f'(a) = \\lim_{h\\to 0} \\dfrac{f(a+h) - f(a)}{h}$ y es finito.",
              "**Derivable $\\Rightarrow$ continua**, pero **continua $\\not\\Rightarrow$ derivable** (ej.: $|x|$ en $0$).",
              "**Funciones por tramos en el punto de cambio:** primero verificar continuidad, luego comparar pendientes laterales del cociente incremental.",
              "**Tres fuentes de no derivabilidad:** discontinuidad, esquina, tangente vertical.",
              "**Próxima lección:** reglas algebraicas para calcular derivadas sin pasar por el límite cada vez.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-2-derivabilidad",
        "title": "Derivabilidad",
        "description": "Cuándo una función es derivable: relación con continuidad, funciones por tramos, esquinas y tangentes verticales.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 2,
    }


# =====================================================================
# LECCIÓN 2.3 — Reglas de derivación
# =====================================================================
def lesson_2_3():
    blocks = [
        b("texto", body_md=(
            "Calcular toda derivada por la definición ($\\lim_{h\\to 0}\\ldots$) sería impracticable. "
            "Esta lección presenta las **reglas algebraicas** que permiten derivar combinaciones de funciones rápidamente. "
            "Son la herramienta de uso diario en todo el resto del curso.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Memorizar y aplicar la regla de la **constante**, la **identidad**, la **potencia** y la **constante por función**.\n"
            "- Aplicar la regla de la **suma** y la **diferencia**.\n"
            "- Aplicar la regla del **producto** y la del **cociente**.\n"
            "- Combinar reglas para derivar polinomios y funciones racionales."
        )),

        b("definicion",
          titulo="Reglas básicas",
          body_md=(
              "Si $c$ es constante y $f, g$ son funciones derivables:\n\n"
              "**1. Constante:** $\\dfrac{d}{dx}[c] = 0$.\n\n"
              "**2. Identidad:** $\\dfrac{d}{dx}[x] = 1$.\n\n"
              "**3. Potencia:** $\\dfrac{d}{dx}[x^n] = n\\, x^{n-1}$ para todo $n \\in \\mathbb{R}$.\n\n"
              "**4. Constante por función:** $\\dfrac{d}{dx}[c \\cdot f(x)] = c \\cdot f'(x)$.\n\n"
              "**5. Suma y diferencia:** $\\dfrac{d}{dx}[f(x) \\pm g(x)] = f'(x) \\pm g'(x)$."
          )),

        b("intuicion",
          titulo="Por qué la regla de la potencia es tan central",
          body_md=(
              "La regla $\\dfrac{d}{dx}[x^n] = n x^{n-1}$ funciona para **cualquier exponente real**: enteros, fracciones, negativos.\n\n"
              "- $\\dfrac{d}{dx}[x^3] = 3x^2$ (entero).\n"
              "- $\\dfrac{d}{dx}[\\sqrt{x}] = \\dfrac{d}{dx}[x^{1/2}] = \\dfrac{1}{2}x^{-1/2} = \\dfrac{1}{2\\sqrt{x}}$ (raíz).\n"
              "- $\\dfrac{d}{dx}\\left[\\dfrac{1}{x}\\right] = \\dfrac{d}{dx}[x^{-1}] = -x^{-2} = -\\dfrac{1}{x^2}$ (negativo).\n\n"
              "La estrategia general: **reescribir** raíces y fracciones como potencias antes de derivar."
          )),

        b("ejemplo_resuelto",
          titulo="Derivar $f(x) = 4x^5 - 3x^2 + 7x - 9$",
          problema_md="Calcular $f'(x)$.",
          pasos=[
              {"accion_md": "**Aplicamos linealidad** (sumas/restas y constantes por función):\n\n$$f'(x) = 4 \\cdot \\dfrac{d}{dx}[x^5] - 3 \\cdot \\dfrac{d}{dx}[x^2] + 7 \\cdot \\dfrac{d}{dx}[x] - \\dfrac{d}{dx}[9]$$",
               "justificacion_md": "La derivada respeta sumas y constantes multiplicativas — eso es lo que permite trabajar término a término.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos potencia y constantes:**\n\n$$f'(x) = 4(5x^4) - 3(2x) + 7(1) - 0 = 20x^4 - 6x + 7$$",
               "justificacion_md": "$\\dfrac{d}{dx}[x^n] = n x^{n-1}$ y $\\dfrac{d}{dx}[c] = 0$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Regla del producto",
          body_md=(
              "Si $f$ y $g$ son derivables:\n\n"
              "$$\\dfrac{d}{dx}[f(x)\\, g(x)] = f'(x)\\, g(x) + f(x)\\, g'(x)$$\n\n"
              "**No es** $f' g'$. Cada factor mantiene la derivada del otro: derivamos uno y multiplicamos por el otro sin tocar; luego intercambiamos."
          )),

        b("ejemplo_resuelto",
          titulo="Derivar $h(x) = (x^2 + 1)(x^3 - 2x)$",
          problema_md="Calcular $h'(x)$ usando la regla del producto.",
          pasos=[
              {"accion_md": "Identificamos $f(x) = x^2 + 1$ y $g(x) = x^3 - 2x$. Calculamos sus derivadas:\n\n$$f'(x) = 2x, \\quad g'(x) = 3x^2 - 2$$",
               "justificacion_md": "Antes de aplicar la fórmula, derivamos cada factor por separado.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la regla del producto:**\n\n$$h'(x) = (2x)(x^3 - 2x) + (x^2+1)(3x^2 - 2)$$",
               "justificacion_md": "$f' g + f g'$.",
               "es_resultado": False},
              {"accion_md": "**Expandimos:**\n\n$$h'(x) = 2x^4 - 4x^2 + 3x^4 - 2x^2 + 3x^2 - 2 = 5x^4 - 3x^2 - 2$$",
               "justificacion_md": "Distribuimos y agrupamos términos semejantes. **Verificación:** podríamos haber expandido $(x^2+1)(x^3-2x) = x^5 - 2x^3 + x^3 - 2x = x^5 - x^3 - 2x$ y derivado: $5x^4 - 3x^2 - 2$. ¡Coincide!",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Regla del cociente",
          body_md=(
              "Si $f$ y $g$ son derivables y $g(x) \\neq 0$:\n\n"
              "$$\\dfrac{d}{dx}\\left[\\dfrac{f(x)}{g(x)}\\right] = \\dfrac{f'(x)\\, g(x) - f(x)\\, g'(x)}{[g(x)]^2}$$\n\n"
              "**Mnemotecnia:** \"baja por arriba menos arriba por baja, todo sobre baja al cuadrado\". El **orden** del numerador importa: $f' g - f g'$ (no $f g' - f' g$)."
          )),

        b("ejemplo_resuelto",
          titulo="Derivar $h(x) = \\dfrac{x^2 + 1}{x - 1}$",
          problema_md="Calcular $h'(x)$.",
          pasos=[
              {"accion_md": "$f(x) = x^2 + 1$ con $f'(x) = 2x$. $g(x) = x - 1$ con $g'(x) = 1$.",
               "justificacion_md": "Identificación de $f$ y $g$.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la regla del cociente:**\n\n$$h'(x) = \\dfrac{(2x)(x-1) - (x^2+1)(1)}{(x-1)^2}$$",
               "justificacion_md": "$\\dfrac{f' g - f g'}{g^2}$.",
               "es_resultado": False},
              {"accion_md": "**Expandimos el numerador:**\n\n$$h'(x) = \\dfrac{2x^2 - 2x - x^2 - 1}{(x-1)^2} = \\dfrac{x^2 - 2x - 1}{(x-1)^2}$$",
               "justificacion_md": "Generalmente conviene **dejar el denominador factorizado** en $(x-1)^2$ en vez de expandirlo: facilita futuras simplificaciones y análisis de signos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Combinar reglas: $f(x) = \\dfrac{\\sqrt{x}(x^2 + 3)}{x + 1}$",
          problema_md="Derivar combinando potencias, producto y cociente.",
          pasos=[
              {"accion_md": "Reescribimos $\\sqrt{x} = x^{1/2}$ y agrupamos el numerador como un producto: $u(x) = x^{1/2}(x^2 + 3)$. El denominador es $v(x) = x+1$.",
               "justificacion_md": "Vamos a aplicar **cociente** con $u$ y $v$, pero antes necesitamos $u'$ vía **producto**.",
               "es_resultado": False},
              {"accion_md": "**Calculamos $u'(x)$ con la regla del producto:**\n\n$$u'(x) = \\tfrac{1}{2}x^{-1/2}(x^2+3) + x^{1/2}(2x) = \\dfrac{x^2+3}{2\\sqrt{x}} + 2x\\sqrt{x}$$",
               "justificacion_md": "Las derivadas internas: $\\dfrac{d}{dx}[x^{1/2}] = \\tfrac{1}{2}x^{-1/2}$ y $\\dfrac{d}{dx}[x^2+3] = 2x$.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos el cociente** con $u$ y $v$, sabiendo que $v'(x) = 1$:\n\n$$f'(x) = \\dfrac{u'(x)(x+1) - x^{1/2}(x^2+3)(1)}{(x+1)^2}$$",
               "justificacion_md": "Sustituimos en la fórmula. Dejamos la expresión en términos de $u'$ para no perder claridad.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo de las reglas:",
          preguntas=[
              {
                  "enunciado_md": "$\\dfrac{d}{dx}\\left[\\dfrac{1}{x^3}\\right] = ?$",
                  "opciones_md": ["$3x^2$", "$-\\dfrac{3}{x^4}$", "$-\\dfrac{1}{3x^2}$", "$\\dfrac{3}{x^4}$"],
                  "correcta": "B",
                  "explicacion_md": (
                      "Reescribimos $\\dfrac{1}{x^3} = x^{-3}$. Por la regla de la potencia: $\\dfrac{d}{dx}[x^{-3}] = -3 x^{-4} = -\\dfrac{3}{x^4}$."
                  ),
              },
              {
                  "enunciado_md": "Si $h(x) = x^2 \\sin x$, entonces $h'(x) = ?$",
                  "opciones_md": [
                      "$2x \\cos x$",
                      "$2x \\sin x + x^2 \\cos x$",
                      "$2x \\sin x - x^2 \\cos x$",
                      "$x^2 \\cos x$",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Regla del producto: $(f g)' = f' g + f g'$. Con $f = x^2$ ($f' = 2x$) y $g = \\sin x$ ($g' = \\cos x$): $h' = 2x \\sin x + x^2 \\cos x$."
                  ),
              },
          ]),

        fig(
            "Tabla-resumen visual de las reglas basicas de derivacion en formato afiche educativo. "
            "Cinco filas con borde teal #06b6d4 a la izquierda mostrando: (1) Constante d/dx[c]=0, (2) "
            "Potencia d/dx[x^n]=n x^(n-1), (3) Suma d/dx[f+g]=f'+g', (4) Producto d/dx[f.g]=f'g+fg', "
            "(5) Cociente d/dx[f/g]=(f'g-fg')/g^2. Cada fila con la formula grande y un mini ejemplo en "
            "ambar #f59e0b a la derecha. Tipografia matematica clara, fondo blanco, sin sombras. "
            + STYLE
        ),
        ej(
            "Derivar combinando suma, producto y potencia",
            "Calcula $f'(x)$ para $f(x) = (3x^2 + 1)(x^3 - 2x)$. No expandas el producto antes de derivar.",
            [
                "Aplica la regla del producto: $(uv)' = u'v + uv'$ con $u = 3x^2 + 1$, $v = x^3 - 2x$.",
                "Calcula $u'$ y $v'$ por separado usando potencia y suma; al final puedes simplificar.",
            ],
            "**Identificar factores:** $u(x) = 3x^2 + 1$, $v(x) = x^3 - 2x$.\n\n**Derivadas individuales:** $u'(x) = 6x$, $v'(x) = 3x^2 - 2$.\n\n**Regla del producto:**\n\n$$f'(x) = u'v + uv' = 6x(x^3 - 2x) + (3x^2 + 1)(3x^2 - 2).$$\n\n**Expandir y simplificar:**\n\n$6x \\cdot x^3 - 6x \\cdot 2x = 6x^4 - 12x^2$.\n\n$(3x^2 + 1)(3x^2 - 2) = 9x^4 - 6x^2 + 3x^2 - 2 = 9x^4 - 3x^2 - 2$.\n\n$$f'(x) = 6x^4 - 12x^2 + 9x^4 - 3x^2 - 2 = 15x^4 - 15x^2 - 2.$$",
        ),
        ej(
            "Regla del cociente",
            "Calcula la derivada de $g(x) = \\dfrac{x^2 - 1}{x^2 + 1}$.",
            [
                "Aplica la regla del cociente $(f/h)' = (f'h - fh')/h^2$ con $f = x^2 - 1$ y $h = x^2 + 1$.",
                "Después de expandir el numerador, varios términos se cancelan.",
            ],
            "**Identificar:** $f(x) = x^2 - 1 \\Rightarrow f'(x) = 2x$; $h(x) = x^2 + 1 \\Rightarrow h'(x) = 2x$.\n\n**Regla del cociente:**\n\n$$g'(x) = \\dfrac{f'h - f h'}{h^2} = \\dfrac{2x(x^2 + 1) - (x^2 - 1)(2x)}{(x^2 + 1)^2}.$$\n\n**Numerador:** $2x[(x^2 + 1) - (x^2 - 1)] = 2x \\cdot 2 = 4x$.\n\n**Resultado:**\n\n$$g'(x) = \\dfrac{4x}{(x^2 + 1)^2}.$$",
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que $(fg)' = f'g'$.** Es el error más típico. La regla correcta es $f'g + fg'$.",
              "**Cambiar el signo del numerador del cociente:** $f g' - f' g$ en lugar de $f' g - f g'$. El orden importa.",
              "**Olvidar elevar al cuadrado el denominador en la regla del cociente.**",
              "**Aplicar la regla del producto cuando un factor es constante:** si $h(x) = 5 f(x)$, basta con $h' = 5 f'$. La regla del producto da lo mismo pero es un rodeo.",
              "**No simplificar antes de derivar.** Por ejemplo, $\\dfrac{x^2}{x}$ se simplifica a $x$ (para $x \\neq 0$), cuya derivada es $1$. Aplicar el cociente da el mismo resultado pero con más cuentas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Constante:** $(c)' = 0$. **Identidad:** $(x)' = 1$. **Potencia:** $(x^n)' = n x^{n-1}$ para $n \\in \\mathbb{R}$.",
              "**Linealidad:** $(c f \\pm d g)' = c f' \\pm d g'$.",
              "**Producto:** $(fg)' = f'g + fg'$.",
              "**Cociente:** $(f/g)' = (f'g - fg')/g^2$.",
              "**Estrategia:** reescribir raíces como $x^{1/n}$ y fracciones como $x^{-n}$ antes de derivar.",
              "**Próxima lección:** derivadas de funciones trigonométricas.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-3-reglas",
        "title": "Reglas de derivación",
        "description": "Reglas algebraicas: constante, potencia, suma, producto y cociente. Combinaciones.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 3,
    }


# =====================================================================
# LECCIÓN 2.4 — Derivadas trigonométricas
# =====================================================================
def lesson_2_4():
    blocks = [
        b("texto", body_md=(
            "Las funciones trigonométricas aparecen en todo modelo periódico: vibración, ondas, ciclos. "
            "Conocer sus derivadas es indispensable para el resto del cálculo. "
            "En esta lección las **deducimos desde la definición** (para $\\sin$ y $\\cos$) y luego derivamos las cuatro restantes con la regla del cociente.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Demostrar y memorizar $(\\sin x)' = \\cos x$ y $(\\cos x)' = -\\sin x$.\n"
            "- Derivar $\\tan, \\cot, \\sec, \\csc$ usando la regla del cociente.\n"
            "- Reconocer los **límites trigonométricos fundamentales** que se usan en la demostración."
        )),

        b("definicion",
          titulo="Límites trigonométricos fundamentales",
          body_md=(
              "Para deducir las derivadas, asumimos los siguientes límites (vistos en el capítulo de Límites):\n\n"
              "$$\\lim_{h \\to 0} \\dfrac{\\sin h}{h} = 1, \\qquad \\lim_{h \\to 0} \\dfrac{\\cos h - 1}{h} = 0$$"
          )),

        b("teorema",
          nombre="Derivada del seno",
          enunciado_md="$\\dfrac{d}{dx}[\\sin x] = \\cos x$.",
          demostracion_md=(
              "Aplicamos la definición y la identidad $\\sin(x+h) = \\sin x \\cos h + \\cos x \\sin h$:\n\n"
              "$$\\dfrac{\\sin(x+h) - \\sin x}{h} = \\dfrac{\\sin x \\cos h + \\cos x \\sin h - \\sin x}{h} = \\sin x \\cdot \\dfrac{\\cos h - 1}{h} + \\cos x \\cdot \\dfrac{\\sin h}{h}$$\n\n"
              "Tomando $h \\to 0$ y usando los dos límites fundamentales:\n\n"
              "$$\\sin x \\cdot 0 + \\cos x \\cdot 1 = \\cos x$$"
          )),

        b("teorema",
          nombre="Derivada del coseno",
          enunciado_md="$\\dfrac{d}{dx}[\\cos x] = -\\sin x$.",
          demostracion_md=(
              "Análogo, con $\\cos(x+h) = \\cos x \\cos h - \\sin x \\sin h$:\n\n"
              "$$\\dfrac{\\cos(x+h) - \\cos x}{h} = \\cos x \\cdot \\dfrac{\\cos h - 1}{h} - \\sin x \\cdot \\dfrac{\\sin h}{h}$$\n\n"
              "$$\\xrightarrow{h \\to 0} \\cos x \\cdot 0 - \\sin x \\cdot 1 = -\\sin x$$"
          )),

        b("definicion",
          titulo="Tabla de derivadas trigonométricas",
          body_md=(
              "Las seis derivadas, en una sola tabla:\n\n"
              "$$\\begin{array}{|c|c|}\\hline f(x) & f'(x) \\\\\\hline \\sin x & \\cos x \\\\ \\cos x & -\\sin x \\\\ \\tan x & \\sec^2 x \\\\ \\cot x & -\\csc^2 x \\\\ \\sec x & \\sec x \\tan x \\\\ \\csc x & -\\csc x \\cot x \\\\\\hline \\end{array}$$\n\n"
              "**Patrón mnemotécnico:** las derivadas de las funciones que empiezan con \"co-\" ($\\cos, \\cot, \\csc$) llevan **signo negativo**."
          )),

        b("ejemplo_resuelto",
          titulo="Deducir $(\\tan x)'$ desde la regla del cociente",
          problema_md="Demostrar que $\\dfrac{d}{dx}[\\tan x] = \\sec^2 x$.",
          pasos=[
              {"accion_md": "Escribimos $\\tan x = \\dfrac{\\sin x}{\\cos x}$ y aplicamos la regla del cociente con $f = \\sin x$, $g = \\cos x$, $f' = \\cos x$, $g' = -\\sin x$:\n\n$$\\dfrac{(\\cos x)(\\cos x) - (\\sin x)(-\\sin x)}{\\cos^2 x} = \\dfrac{\\cos^2 x + \\sin^2 x}{\\cos^2 x}$$",
               "justificacion_md": "Atención al signo: $g' = -\\sin x$ y al restarlo en el numerador queda $-(\\sin x)(-\\sin x) = +\\sin^2 x$.",
               "es_resultado": False},
              {"accion_md": "Por la identidad pitagórica $\\cos^2 x + \\sin^2 x = 1$:\n\n$$\\dfrac{1}{\\cos^2 x} = \\sec^2 x$$",
               "justificacion_md": "$\\sec x = 1/\\cos x$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $f(x) = x \\sin x$",
          problema_md="Calcular $f'(x)$.",
          pasos=[
              {"accion_md": "**Regla del producto** con $u = x$, $v = \\sin x$, $u' = 1$, $v' = \\cos x$:\n\n$$f'(x) = (1)(\\sin x) + (x)(\\cos x) = \\sin x + x \\cos x$$",
               "justificacion_md": "Aplicación directa de la regla del producto.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $g(x) = \\dfrac{\\sec x}{1 + \\tan x}$",
          problema_md="Calcular $g'(x)$.",
          pasos=[
              {"accion_md": "Identificamos $f = \\sec x$ con $f' = \\sec x \\tan x$, y $h = 1 + \\tan x$ con $h' = \\sec^2 x$.",
               "justificacion_md": "Derivadas individuales antes de aplicar la regla del cociente.",
               "es_resultado": False},
              {"accion_md": "**Regla del cociente:**\n\n$$g'(x) = \\dfrac{\\sec x \\tan x \\cdot (1 + \\tan x) - \\sec x \\cdot \\sec^2 x}{(1+\\tan x)^2}$$",
               "justificacion_md": "$f' h - f h'$ sobre $h^2$.",
               "es_resultado": False},
              {"accion_md": "Factorizamos $\\sec x$ del numerador:\n\n$$g'(x) = \\dfrac{\\sec x [\\tan x (1+\\tan x) - \\sec^2 x]}{(1+\\tan x)^2} = \\dfrac{\\sec x (\\tan x + \\tan^2 x - \\sec^2 x)}{(1+\\tan x)^2}$$",
               "justificacion_md": "Usando la identidad $\\sec^2 x = 1 + \\tan^2 x$, el numerador se simplifica: $\\tan x + \\tan^2 x - 1 - \\tan^2 x = \\tan x - 1$.",
               "es_resultado": False},
              {"accion_md": "$$g'(x) = \\dfrac{\\sec x (\\tan x - 1)}{(1+\\tan x)^2}$$",
               "justificacion_md": "**Lección general:** después de aplicar la regla del cociente, con frecuencia conviene usar identidades trigonométricas para simplificar.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el dominio de las derivadas trigonométricas:",
          preguntas=[
              {
                  "enunciado_md": "$\\dfrac{d}{dx}[\\sin x \\cos x] = ?$",
                  "opciones_md": [
                      "$\\cos^2 x - \\sin^2 x$",
                      "$\\cos^2 x + \\sin^2 x$",
                      "$-\\sin x \\cos x$",
                      "$\\cos x - \\sin x$",
                  ],
                  "correcta": "A",
                  "explicacion_md": (
                      "Regla del producto: $(\\sin x)' \\cos x + \\sin x (\\cos x)' = \\cos x \\cdot \\cos x + \\sin x \\cdot (-\\sin x) = \\cos^2 x - \\sin^2 x$. "
                      "(Equivale a $\\cos(2x)$ por la identidad de ángulo doble.)"
                  ),
              },
              {
                  "enunciado_md": "Si $f(x) = \\sec x$, entonces $f'(\\pi/4) = ?$",
                  "opciones_md": ["$\\sqrt{2}$", "$2$", "$2\\sqrt{2}$", "$\\sqrt{2}/2$"],
                  "correcta": "A",
                  "explicacion_md": (
                      "$f'(x) = \\sec x \\tan x$. En $\\pi/4$: $\\sec(\\pi/4) = \\sqrt{2}$ y $\\tan(\\pi/4) = 1$. Producto: $\\sqrt{2}$."
                  ),
              },
          ]),

        fig(
            "Tabla-resumen visual de las seis derivadas trigonometricas en formato tarjeta. Tres columnas "
            "y dos filas. Columna 1: (sen x)' = cos x | (cos x)' = -sen x. Columna 2: (tan x)' = sec^2 x "
            "| (cot x)' = -csc^2 x. Columna 3: (sec x)' = sec x tan x | (csc x)' = -csc x cot x. Las "
            "funciones 'co-' destacadas en ambar #f59e0b con flecha indicando 'signo negativo'. Las otras "
            "en teal #06b6d4. Tipografia matematica clara, fondo blanco. " + STYLE
        ),
        ej(
            "Derivar funciones trigonométricas combinadas",
            "Calcula la derivada de $f(x) = x \\sin x + \\cos x$.",
            [
                "Aplica suma y producto: $(x \\sin x)' = (x)' \\sin x + x (\\sin x)'$.",
                "Recuerda que $(\\cos x)' = -\\sin x$.",
            ],
            "**Primer término** (regla del producto): $(x \\sin x)' = 1 \\cdot \\sin x + x \\cdot \\cos x = \\sin x + x \\cos x$.\n\n**Segundo término:** $(\\cos x)' = -\\sin x$.\n\n**Suma:** $f'(x) = \\sin x + x \\cos x - \\sin x = x \\cos x$.\n\n**Resultado:** $f'(x) = x \\cos x$. (El término $\\sin x$ se cancela.)",
        ),
        ej(
            "Recta tangente a una curva trigonométrica",
            "Encuentra la ecuación de la recta tangente a $y = \\tan x$ en el punto $x_0 = \\pi/4$.",
            [
                "Calcula $y_0 = \\tan(\\pi/4) = 1$ y $y'(\\pi/4) = \\sec^2(\\pi/4)$.",
                "Recuerda que $\\sec(\\pi/4) = \\sqrt{2}$.",
            ],
            "**Punto de tangencia:** $y_0 = \\tan(\\pi/4) = 1$, así que el punto es $(\\pi/4,\\ 1)$.\n\n**Pendiente:** $y' = \\sec^2 x$. En $\\pi/4$: $\\sec(\\pi/4) = 1/\\cos(\\pi/4) = \\sqrt{2}$, luego $y'(\\pi/4) = (\\sqrt{2})^2 = 2$.\n\n**Ecuación punto-pendiente:**\n\n$$y - 1 = 2\\left(x - \\dfrac{\\pi}{4}\\right) \\quad\\Longleftrightarrow\\quad y = 2x - \\dfrac{\\pi}{2} + 1.$$",
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el signo negativo en $(\\cos x)'$, $(\\cot x)'$, $(\\csc x)'$.** Las funciones \"co-\" llevan signo negativo.",
              "**Confundir $(\\tan x)'$ con $\\tan^2 x$.** La derivada es $\\sec^2 x$, no $\\tan^2 x$ (aunque la identidad $\\sec^2 = 1 + \\tan^2$ las relaciona).",
              "**Aplicar la regla del producto donde basta el cociente o viceversa.** No es un error grave (el resultado es el mismo), pero el cociente es más natural cuando hay una fracción explícita.",
              "**No usar identidades trigonométricas para simplificar.** Después de derivar, casi siempre se puede simplificar el resultado con $\\sin^2 + \\cos^2 = 1$, $\\sec^2 = 1 + \\tan^2$, $\\csc^2 = 1 + \\cot^2$.",
          ]),

        b("resumen",
          puntos_md=[
              "$(\\sin x)' = \\cos x$, $(\\cos x)' = -\\sin x$.",
              "$(\\tan x)' = \\sec^2 x$, $(\\cot x)' = -\\csc^2 x$.",
              "$(\\sec x)' = \\sec x \\tan x$, $(\\csc x)' = -\\csc x \\cot x$.",
              "**Mnemotecnia:** las funciones \"co-\" ($\\cos, \\cot, \\csc$) tienen derivada con signo negativo.",
              "**Próxima lección:** la regla de la cadena, para derivar **composiciones** como $\\sin(2x)$, $\\cos(x^2)$, $\\sqrt{1+x^2}$, etc.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-4-trigonometricas",
        "title": "Derivadas trigonométricas",
        "description": "Derivadas de seno, coseno, tangente, cotangente, secante y cosecante. Demostraciones y ejemplos.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 4,
    }


# =====================================================================
# LECCIÓN 2.5 — Regla de la cadena
# =====================================================================
def lesson_2_5():
    blocks = [
        b("texto", body_md=(
            "Las reglas vistas hasta ahora cubren sumas, productos y cocientes — pero no **composiciones**. "
            "¿Cómo derivar $\\sin(x^2)$, $\\sqrt{1 + x^3}$, $(2x+1)^{10}$? "
            "Aquí entra la **regla de la cadena**, una de las más usadas del cálculo.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Reconocer una **composición** $f(g(x))$ y descomponerla en función exterior e interior.\n"
            "- Aplicar la fórmula $\\dfrac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)$.\n"
            "- Encadenar la regla **varias veces** cuando hay composiciones anidadas.\n"
            "- Combinar la regla de la cadena con producto y cociente."
        )),

        b("intuicion",
          titulo="Por qué hay que derivar también lo de adentro",
          body_md=(
              "Compara $\\sin(x)$ con $\\sin(2x)$. La segunda **oscila el doble de rápido**: completa un ciclo cuando la primera apenas ha avanzado medio. "
              "Esa velocidad mayor se traslada a su derivada: $(\\sin(2x))' = 2 \\cos(2x)$, no $\\cos(2x)$.\n\n"
              "El factor $2$ es exactamente la derivada de $g(x) = 2x$ — la **función interior**. "
              "La regla de la cadena formaliza esta intuición: derivar la función exterior **y multiplicar por la derivada de la interior**."
          )),

        b("teorema",
          nombre="Regla de la cadena",
          enunciado_md=(
              "Si $g$ es derivable en $x$ y $f$ es derivable en $g(x)$, entonces $(f \\circ g)$ es derivable en $x$ y:\n\n"
              "$$\\dfrac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)$$\n\n"
              "**Notación de Leibniz:** si $y = f(u)$ y $u = g(x)$, entonces $\\dfrac{dy}{dx} = \\dfrac{dy}{du} \\cdot \\dfrac{du}{dx}$."
          ),
          demostracion_md=(
              "Idea esquemática (la rigurosa requiere un argumento por casos):\n\n"
              "$$\\dfrac{f(g(x+h)) - f(g(x))}{h} = \\dfrac{f(g(x+h)) - f(g(x))}{g(x+h) - g(x)} \\cdot \\dfrac{g(x+h) - g(x)}{h}$$\n\n"
              "Cuando $h \\to 0$, el primer factor tiende a $f'(g(x))$ (porque $g(x+h) \\to g(x)$ por continuidad) y el segundo a $g'(x)$. Producto: $f'(g(x)) \\cdot g'(x)$."
          )),

        b("ejemplo_resuelto",
          titulo="Derivar $h(x) = \\sin(x^2)$",
          problema_md="Calcular $h'(x)$.",
          pasos=[
              {"accion_md": "**Identificamos exterior e interior:** la función exterior es $f(u) = \\sin u$, la interior $g(x) = x^2$. Sus derivadas: $f'(u) = \\cos u$ y $g'(x) = 2x$.",
               "justificacion_md": "Identificación clara de las dos capas antes de aplicar la regla.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la cadena:** $h'(x) = f'(g(x)) \\cdot g'(x) = \\cos(x^2) \\cdot 2x = 2x \\cos(x^2)$.",
               "justificacion_md": "$f'(g(x)) = \\cos(g(x)) = \\cos(x^2)$. Después multiplicamos por $g'(x) = 2x$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $h(x) = (3x^2 + 5)^{10}$",
          problema_md="Calcular $h'(x)$ usando la regla de la cadena.",
          pasos=[
              {"accion_md": "**Exterior:** $f(u) = u^{10}$ con $f'(u) = 10 u^9$. **Interior:** $g(x) = 3x^2 + 5$ con $g'(x) = 6x$.",
               "justificacion_md": "La regla de la potencia más la cadena.",
               "es_resultado": False},
              {"accion_md": "$$h'(x) = 10(3x^2+5)^9 \\cdot 6x = 60x(3x^2+5)^9$$",
               "justificacion_md": "**Sin la cadena**, derivar potencias de polinomios sería un trabajo enorme: expandir $(3x^2+5)^{10}$ es impensable.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $h(x) = \\sqrt{1 + x^3}$",
          problema_md="Calcular $h'(x)$.",
          pasos=[
              {"accion_md": "Reescribimos $h(x) = (1 + x^3)^{1/2}$. **Exterior:** $f(u) = u^{1/2}$ con $f'(u) = \\tfrac{1}{2} u^{-1/2}$. **Interior:** $g(x) = 1 + x^3$ con $g'(x) = 3x^2$.",
               "justificacion_md": "Reescribimos la raíz como potencia para usar la regla de la potencia.",
               "es_resultado": False},
              {"accion_md": "$$h'(x) = \\tfrac{1}{2}(1+x^3)^{-1/2} \\cdot 3x^2 = \\dfrac{3x^2}{2\\sqrt{1+x^3}}$$",
               "justificacion_md": "Volvemos a la notación de raíz para presentar el resultado.",
               "es_resultado": True},
          ]),

        b("intuicion",
          titulo="Cadena anidada",
          body_md=(
              "Cuando hay **tres o más capas**, la regla se aplica varias veces:\n\n"
              "$$\\dfrac{d}{dx}[f(g(h(x)))] = f'(g(h(x))) \\cdot g'(h(x)) \\cdot h'(x)$$\n\n"
              "Cada capa contribuye con la derivada de la siguiente, evaluada en lo que sigue dentro."
          )),

        b("ejemplo_resuelto",
          titulo="Cadena triple: $h(x) = \\sin^3(2x)$",
          problema_md="Calcular $h'(x)$.",
          pasos=[
              {"accion_md": "Reescribimos $h(x) = [\\sin(2x)]^3$. **Tres capas:** la más exterior es $u^3$, la del medio es $\\sin u$, y la más interior es $2x$.",
               "justificacion_md": "Identificar las capas en orden de aplicación.",
               "es_resultado": False},
              {"accion_md": "**Derivada exterior:** $\\dfrac{d}{du}[u^3] = 3u^2$, evaluada en $\\sin(2x)$: $3 \\sin^2(2x)$.",
               "justificacion_md": "Primera capa.",
               "es_resultado": False},
              {"accion_md": "**Derivada del medio:** $\\dfrac{d}{du}[\\sin u] = \\cos u$, evaluada en $2x$: $\\cos(2x)$.",
               "justificacion_md": "Segunda capa.",
               "es_resultado": False},
              {"accion_md": "**Derivada interna:** $\\dfrac{d}{dx}[2x] = 2$.",
               "justificacion_md": "Tercera capa.",
               "es_resultado": False},
              {"accion_md": "**Multiplicamos las tres:**\n\n$$h'(x) = 3 \\sin^2(2x) \\cdot \\cos(2x) \\cdot 2 = 6 \\sin^2(2x) \\cos(2x)$$",
               "justificacion_md": "La cadena se aplica de afuera hacia adentro, multiplicando todas las contribuciones.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Combinar con producto: $h(x) = x^2 \\sin(3x)$",
          problema_md="Derivar.",
          pasos=[
              {"accion_md": "**Regla del producto** con $u = x^2$ y $v = \\sin(3x)$:\n\n$$h'(x) = u' v + u v' = 2x \\sin(3x) + x^2 \\cdot \\dfrac{d}{dx}[\\sin(3x)]$$",
               "justificacion_md": "El factor $\\sin(3x)$ requiere a su vez la regla de la cadena.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la cadena en $\\sin(3x)$:** $\\dfrac{d}{dx}[\\sin(3x)] = \\cos(3x) \\cdot 3 = 3\\cos(3x)$.",
               "justificacion_md": "Exterior $\\sin u$, interior $3x$.",
               "es_resultado": False},
              {"accion_md": "$$h'(x) = 2x \\sin(3x) + 3x^2 \\cos(3x)$$",
               "justificacion_md": "Combinar producto y cadena es estándar: cada vez que un factor sea una composición, hay que aplicar la cadena dentro.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo de la cadena:",
          preguntas=[
              {
                  "enunciado_md": "$\\dfrac{d}{dx}[\\cos(x^2 + 1)] = ?$",
                  "opciones_md": [
                      "$-\\sin(x^2+1)$",
                      "$-2x\\sin(x^2+1)$",
                      "$2x\\cos(x^2+1)$",
                      "$\\sin(x^2+1) \\cdot 2x$",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Exterior $\\cos u$ con derivada $-\\sin u$; interior $x^2 + 1$ con derivada $2x$. Producto: $-\\sin(x^2+1) \\cdot 2x = -2x\\sin(x^2+1)$."
                  ),
              },
              {
                  "enunciado_md": "Si $h(x) = \\sqrt{\\tan x}$, entonces $h'(x) = ?$",
                  "opciones_md": [
                      "$\\dfrac{1}{2\\sqrt{\\tan x}}$",
                      "$\\dfrac{\\sec^2 x}{2\\sqrt{\\tan x}}$",
                      "$\\dfrac{\\sec^2 x}{\\sqrt{\\tan x}}$",
                      "$2\\sqrt{\\tan x} \\cdot \\sec^2 x$",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Reescribimos $h = (\\tan x)^{1/2}$. Exterior: $\\tfrac{1}{2}u^{-1/2}$. Interior: $(\\tan x)' = \\sec^2 x$. "
                      "Producto: $\\dfrac{1}{2\\sqrt{\\tan x}} \\cdot \\sec^2 x = \\dfrac{\\sec^2 x}{2\\sqrt{\\tan x}}$."
                  ),
              },
          ]),

        fig(
            "Diagrama esquematico de la regla de la cadena: tres engranajes interconectados representando "
            "una composicion f(g(x)). Engranaje exterior grande etiquetado 'derivada exterior f prima' en "
            "teal #06b6d4, engranaje interno mediano 'evaluado en g(x)', engranaje pequeno 'derivada "
            "interior g prima de x' en ambar #f59e0b. Flechas indicando multiplicacion. Texto al pie: "
            "'(f compuesto g)' = f'(g(x)) . g'(x)'. Estilo limpio, fondo blanco. " + STYLE
        ),
        ej(
            "Cadena con dos niveles",
            "Calcula $f'(x)$ para $f(x) = \\sin(3x^2 + 1)$.",
            [
                "Identifica función exterior $\\sin u$ con $u(x) = 3x^2 + 1$.",
                "Aplica $(f \\circ g)'(x) = f'(g(x)) \\cdot g'(x)$.",
            ],
            "**Identificación:** exterior $\\sin u$, interior $u(x) = 3x^2 + 1$.\n\n**Derivadas:** $(\\sin u)' = \\cos u$ y $u'(x) = 6x$.\n\n**Aplicar la cadena:**\n\n$$f'(x) = \\cos(3x^2 + 1) \\cdot 6x = 6x \\cos(3x^2 + 1).$$",
        ),
        ej(
            "Cadena con tres niveles anidados",
            "Calcula $g'(x)$ para $g(x) = \\sqrt{1 + \\sin^2 x}$.",
            [
                "Tienes tres funciones anidadas: raíz, cuadrado y seno. Aplica la cadena dos veces.",
                "Recuerda que $\\sin^2 x = (\\sin x)^2$.",
            ],
            "**Identificación:** $g(x) = (1 + \\sin^2 x)^{1/2}$. Capa exterior: $u^{1/2}$, intermedia $u(v) = 1 + v^2$ con $v = \\sin x$.\n\n**Capa exterior:** derivada de $u^{1/2}$ respecto a $u$ es $\\dfrac{1}{2}u^{-1/2} = \\dfrac{1}{2\\sqrt{1 + \\sin^2 x}}$.\n\n**Capa intermedia:** derivada de $1 + v^2$ respecto a $v$ es $2v = 2\\sin x$.\n\n**Capa interior:** $(\\sin x)' = \\cos x$.\n\n**Producto (regla de la cadena triple):**\n\n$$g'(x) = \\dfrac{1}{2\\sqrt{1 + \\sin^2 x}} \\cdot 2\\sin x \\cdot \\cos x = \\dfrac{\\sin x \\cos x}{\\sqrt{1 + \\sin^2 x}}.$$\n\nEquivalentemente, usando $2 \\sin x \\cos x = \\sin(2x)$: $g'(x) = \\dfrac{\\sin(2x)}{2\\sqrt{1 + \\sin^2 x}}$.",
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar multiplicar por la derivada de la función interior.** El error más común: escribir $(\\sin(2x))' = \\cos(2x)$ en lugar de $2\\cos(2x)$.",
              "**Confundir $f(g(x))$ con $f(x) \\cdot g(x)$.** La cadena se aplica a composiciones, no a productos.",
              "**Evaluar $f'$ en $x$ en vez de en $g(x)$.** En la fórmula $f'(g(x)) \\cdot g'(x)$, la derivada exterior se evalúa **en la función interior**, no en $x$.",
              "**Aplicar producto cuando hay composición.** $\\sqrt{x^2+1}$ es composición, no producto: la regla del producto no aplica aquí.",
              "**No anidar la cadena cuando hay tres o más capas.** Cada capa contribuye su propio factor en el producto final.",
          ]),

        b("resumen",
          puntos_md=[
              "**Regla de la cadena:** $\\dfrac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)$.",
              "**Notación de Leibniz:** $\\dfrac{dy}{dx} = \\dfrac{dy}{du} \\cdot \\dfrac{du}{dx}$.",
              "**Estrategia:** identificar la función exterior y la interior; derivar exterior **evaluada en la interior**; multiplicar por la derivada de la interior.",
              "**Cadenas anidadas:** aplicar la regla varias veces, una por cada capa.",
              "**Combinar con producto y cociente:** dentro de cualquier factor que sea una composición, usar cadena.",
              "**Próxima lección:** derivación implícita, para curvas dadas por ecuaciones $F(x, y) = 0$.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-5-cadena",
        "title": "Regla de la cadena",
        "description": "Derivada de composiciones $f(g(x))$. Cadenas anidadas y combinación con producto/cociente.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 5,
    }


# =====================================================================
# LECCIÓN 2.6 — Derivación implícita
# =====================================================================
def lesson_2_6():
    blocks = [
        b("texto", body_md=(
            "Hasta aquí, todas las funciones que derivamos tenían la forma **explícita** $y = f(x)$: una variable despejada en términos de la otra. "
            "Pero muchas curvas importantes están dadas por ecuaciones donde no es posible (o conveniente) despejar $y$ — por ejemplo, una circunferencia $x^2 + y^2 = 25$ o $e^{xy} = x + y$.\n\n"
            "La **derivación implícita** permite calcular $y'$ sin despejar $y$. Es una técnica imprescindible en geometría diferencial y en muchos problemas de razones relacionadas.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Diferenciar **ambos lados** de una ecuación tratando $y$ como función de $x$.\n"
            "- Despejar $\\dfrac{dy}{dx}$ algebraicamente.\n"
            "- Calcular pendientes de **rectas tangentes** a curvas implícitas.\n"
            "- Aplicar la técnica a curvas con $\\ln$, $e$, trigonométricas y combinaciones."
        )),

        b("intuicion",
          titulo="$y$ es función de $x$, aunque no esté despejada",
          body_md=(
              "Cuando una ecuación $F(x, y) = C$ define implícitamente a $y$ como función de $x$ — al menos en un trozo de la curva —, podemos pensar $y = y(x)$ y aplicar la **regla de la cadena** cada vez que una expresión incluya $y$.\n\n"
              "Por ejemplo, $\\dfrac{d}{dx}[y^2] = 2y \\cdot y'$ (no $2y$), porque $y^2$ es la composición de $u^2$ con $u = y(x)$.\n\n"
              "**Después de derivar ambos lados**, queda una ecuación en $x$, $y$ y $y'$ — y se despeja $y'$."
          )),

        b("definicion",
          titulo="Método de derivación implícita",
          body_md=(
              "Para encontrar $\\dfrac{dy}{dx}$ a partir de $F(x, y) = C$:\n\n"
              "1. **Derivar ambos lados** respecto de $x$, recordando que $y$ es función de $x$.\n"
              "2. Cada vez que aparezca un término en $y$, aplicar la **regla de la cadena**: $\\dfrac{d}{dx}[g(y)] = g'(y) \\cdot y'$.\n"
              "3. **Agrupar** los términos con $y'$ a un lado y los demás al otro.\n"
              "4. **Despejar $y'$** factorizando."
          )),

        b("ejemplo_resuelto",
          titulo="Circunferencia $x^2 + y^2 = 25$",
          problema_md="Calcular $\\dfrac{dy}{dx}$ y la pendiente de la recta tangente en $(3, 4)$.",
          pasos=[
              {"accion_md": "**Derivamos ambos lados respecto de $x$:**\n\n$$\\dfrac{d}{dx}[x^2] + \\dfrac{d}{dx}[y^2] = \\dfrac{d}{dx}[25]$$\n\n$$2x + 2y \\cdot y' = 0$$",
               "justificacion_md": "$\\dfrac{d}{dx}[y^2]$ requiere la cadena: $y^2$ es $u^2$ con $u = y(x)$, así su derivada es $2y \\cdot y'$. La derivada de la constante $25$ es $0$.",
               "es_resultado": False},
              {"accion_md": "**Despejamos $y'$:**\n\n$$2y \\cdot y' = -2x \\implies y' = -\\dfrac{x}{y}$$",
               "justificacion_md": "Aislamos el término con $y'$ y dividimos por su coeficiente.",
               "es_resultado": False},
              {"accion_md": "**Pendiente en $(3, 4)$:** $y'(3, 4) = -\\dfrac{3}{4}$.\n\n**Recta tangente:** $y - 4 = -\\dfrac{3}{4}(x - 3)$.",
               "justificacion_md": "Sustituimos las coordenadas del punto y usamos la forma punto-pendiente. Geométricamente, la tangente a la circunferencia es perpendicular al radio en ese punto: el radio tiene pendiente $4/3$, así la tangente tiene pendiente $-3/4$. ✓",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Curva $y^3 + xy = 10$",
          problema_md="Calcular $\\dfrac{dy}{dx}$.",
          pasos=[
              {"accion_md": "**Derivamos ambos lados:**\n\n$$\\dfrac{d}{dx}[y^3] + \\dfrac{d}{dx}[xy] = 0$$",
               "justificacion_md": "$\\dfrac{d}{dx}[y^3]$ por cadena: $3y^2 y'$. $\\dfrac{d}{dx}[xy]$ por **regla del producto**: $1 \\cdot y + x \\cdot y' = y + x y'$.",
               "es_resultado": False},
              {"accion_md": "$$3y^2 y' + y + x y' = 0$$\n\n**Agrupamos términos con $y'$:**\n\n$$y'(3y^2 + x) = -y$$",
               "justificacion_md": "Factorizamos $y'$ como factor común a la izquierda y movemos $y$ a la derecha.",
               "es_resultado": False},
              {"accion_md": "$$y' = -\\dfrac{y}{3y^2 + x}$$",
               "justificacion_md": "**Importante:** la derivada queda expresada en términos tanto de $x$ como de $y$. Eso es normal en derivación implícita — al no haber despejado $y$, la respuesta tampoco está despejada.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Curva $e^{xy} = x + y$",
          problema_md="Calcular $\\dfrac{dy}{dx}$.",
          pasos=[
              {"accion_md": "**Derivamos ambos lados.** El lado izquierdo requiere cadena con exterior $e^u$ e interior $u = xy$:\n\n$$\\dfrac{d}{dx}[e^{xy}] = e^{xy} \\cdot \\dfrac{d}{dx}[xy] = e^{xy}(y + x y')$$",
               "justificacion_md": "$(e^u)' = e^u \\cdot u'$. Y $\\dfrac{d}{dx}[xy] = y + xy'$ por la regla del producto.",
               "es_resultado": False},
              {"accion_md": "**Lado derecho:** $\\dfrac{d}{dx}[x + y] = 1 + y'$. Igualando:\n\n$$e^{xy}(y + xy') = 1 + y'$$",
               "justificacion_md": "Cada lado derivado por separado.",
               "es_resultado": False},
              {"accion_md": "**Distribuimos y agrupamos términos con $y'$:**\n\n$$y e^{xy} + x e^{xy} y' = 1 + y'$$\n\n$$y'(x e^{xy} - 1) = 1 - y e^{xy}$$",
               "justificacion_md": "Pasamos $y'$ a un lado, todo lo demás al otro, y factorizamos.",
               "es_resultado": False},
              {"accion_md": "$$y' = \\dfrac{1 - y e^{xy}}{x e^{xy} - 1}$$",
               "justificacion_md": "El resultado depende de $x$ y de $y$, como suele ser en derivación implícita con funciones exponenciales.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Tangente a la elipse $\\dfrac{x^2}{16} + \\dfrac{y^2}{9} = 1$ en $(2, \\tfrac{3\\sqrt{3}}{2})$",
          problema_md="Encontrar la ecuación de la recta tangente.",
          pasos=[
              {"accion_md": "**Derivamos implícitamente:**\n\n$$\\dfrac{2x}{16} + \\dfrac{2y \\cdot y'}{9} = 0 \\implies \\dfrac{x}{8} + \\dfrac{2 y y'}{9} = 0$$",
               "justificacion_md": "Cadena en $y^2$: $2y \\cdot y'$. Las constantes en denominador permanecen.",
               "es_resultado": False},
              {"accion_md": "**Despejamos $y'$:**\n\n$$\\dfrac{2 y y'}{9} = -\\dfrac{x}{8} \\implies y' = -\\dfrac{9x}{16 y}$$",
               "justificacion_md": "Aislamos $y'$ y simplificamos.",
               "es_resultado": False},
              {"accion_md": "**Evaluamos en $(2, \\tfrac{3\\sqrt{3}}{2})$:**\n\n$$y'(2, \\tfrac{3\\sqrt{3}}{2}) = -\\dfrac{9 \\cdot 2}{16 \\cdot \\tfrac{3\\sqrt{3}}{2}} = -\\dfrac{18}{24\\sqrt{3}} = -\\dfrac{3}{4\\sqrt{3}} = -\\dfrac{\\sqrt{3}}{4}$$",
               "justificacion_md": "Pendiente de la tangente.",
               "es_resultado": False},
              {"accion_md": "**Recta tangente:** $y - \\dfrac{3\\sqrt{3}}{2} = -\\dfrac{\\sqrt{3}}{4}(x - 2)$.",
               "justificacion_md": "Forma punto-pendiente con el punto y la pendiente recién calculados.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica la técnica:",
          preguntas=[
              {
                  "enunciado_md": "Para $x^2 + xy + y^2 = 7$, $\\dfrac{dy}{dx} = ?$",
                  "opciones_md": [
                      "$-\\dfrac{2x + y}{x + 2y}$",
                      "$-\\dfrac{2x + y}{2y}$",
                      "$\\dfrac{2x + y}{x + 2y}$",
                      "$\\dfrac{x}{y}$",
                  ],
                  "correcta": "A",
                  "explicacion_md": (
                      "Derivando: $2x + (y + xy') + 2y y' = 0$. Agrupando: $(x + 2y) y' = -(2x + y)$. Despejando: $y' = -\\dfrac{2x+y}{x+2y}$."
                  ),
              },
              {
                  "enunciado_md": "¿Por qué $\\dfrac{d}{dx}[y^2] = 2y \\cdot y'$ y no $2y$?",
                  "opciones_md": [
                      "Por la regla del producto.",
                      "Por la regla de la cadena: $y$ depende de $x$.",
                      "Por la regla del cociente.",
                      "No es así, sí es $2y$.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "$y$ es función de $x$, así $y^2$ es composición: exterior $u^2$, interior $y(x)$. La cadena da $2u \\cdot u' = 2y \\cdot y'$. "
                      "Olvidar el factor $y'$ es el error más típico de derivación implícita."
                  ),
              },
          ]),

        fig(
            "Diagrama de una elipse en el plano cartesiano (x^2/9 + y^2/4 = 1) en linea teal #06b6d4. "
            "Marca un punto P en el primer cuadrante con coordenadas (2, y0) y dibuja la recta tangente "
            "en ese punto en color ambar #f59e0b. Etiquetas: ecuacion de la elipse arriba, formula de la "
            "tangente abajo. Ejes con flechas y graduacion. Muestra como la derivacion implicita encuentra "
            "la pendiente sin despejar y. Estilo limpio educativo. " + STYLE
        ),
        ej(
            "Derivada implícita en una circunferencia",
            "Calcula $\\dfrac{dy}{dx}$ para la curva $x^2 + y^2 = 25$ y encuentra la pendiente de la tangente en el punto $(3, 4)$.",
            [
                "Deriva ambos lados respecto a $x$, recordando que $y$ depende de $x$ y por tanto $\\dfrac{d}{dx}[y^2] = 2y \\cdot y'$.",
                "Despeja $y'$ y evalúa en $(3, 4)$.",
            ],
            "**Paso 1 — Derivar implícitamente.** Aplicando $\\dfrac{d}{dx}$ a ambos lados:\n\n$$2x + 2y \\cdot y' = 0.$$\n\n**Paso 2 — Despejar.** $y' = -\\dfrac{x}{y}$.\n\n**Paso 3 — Evaluar.** En $(3, 4)$: $y' = -\\dfrac{3}{4}$.\n\n**Interpretación geométrica:** la pendiente de la tangente al círculo $x^2 + y^2 = 25$ en $(3, 4)$ es $-\\dfrac{3}{4}$. (Coincide con la pendiente perpendicular al radio $(0,0)$-$(3,4)$, que tiene pendiente $4/3$.)",
        ),
        ej(
            "Folium de Descartes",
            "Para la curva $x^3 + y^3 = 6xy$ (folium de Descartes), encuentra $\\dfrac{dy}{dx}$ y la ecuación de la recta tangente en el punto $(3, 3)$.",
            [
                "Aplica $\\dfrac{d}{dx}$ término a término. Para $6xy$ usa la regla del producto.",
                "Después de despejar $y'$, sustituye $(x, y) = (3, 3)$.",
            ],
            "**Paso 1 — Derivar implícitamente.**\n\n$\\dfrac{d}{dx}[x^3] = 3x^2$, $\\dfrac{d}{dx}[y^3] = 3y^2 \\cdot y'$, $\\dfrac{d}{dx}[6xy] = 6y + 6x\\,y'$ (producto).\n\n$$3x^2 + 3y^2 y' = 6y + 6x y'.$$\n\n**Paso 2 — Despejar $y'$.** Agrupar términos con $y'$:\n\n$$3y^2 y' - 6x y' = 6y - 3x^2 \\;\\Rightarrow\\; y'(3y^2 - 6x) = 6y - 3x^2 \\;\\Rightarrow\\; y' = \\dfrac{2y - x^2}{y^2 - 2x}.$$\n\n**Paso 3 — Evaluar en $(3, 3)$.** $y' = \\dfrac{2(3) - 9}{9 - 6} = \\dfrac{-3}{3} = -1$.\n\n**Recta tangente:** $y - 3 = -1(x - 3) \\Rightarrow y = -x + 6$.",
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar el factor $y'$ al derivar términos con $y$.** $\\dfrac{d}{dx}[y^n] = n y^{n-1} y'$, no $n y^{n-1}$.",
              "**Confundir derivación implícita con tratar $y$ como constante.** $y$ es **función de $x$**, no una constante.",
              "**No agrupar bien al despejar $y'$.** Hay que llevar todos los términos con $y'$ a un lado y factorizarlo. Es álgebra básica, pero con varios términos puede fallar.",
              "**Olvidar la regla del producto en términos como $xy$.** $\\dfrac{d}{dx}[xy] = y + xy'$, no $xy'$ ni $y'$.",
              "**Sustituir el punto antes de derivar.** Hay que derivar primero (en general) y luego evaluar el punto.",
          ]),

        b("resumen",
          puntos_md=[
              "**Derivación implícita:** se aplica cuando $y$ no está despejado en función de $x$.",
              "**Procedimiento:** derivar ambos lados respecto de $x$, tratando $y$ como función de $x$ (cada $g(y)$ aporta $g'(y) \\cdot y'$ por cadena), y despejar $y'$.",
              "**Resultado:** una expresión de $y'$ que depende típicamente de $x$ y de $y$.",
              "**Aplicación:** rectas tangentes a curvas implícitas, problemas de razones relacionadas.",
              "**Próxima lección:** derivación logarítmica — un caso especial de derivación implícita usando logaritmos.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-6-implicita",
        "title": "Derivación implícita",
        "description": "Calcular $y'$ desde $F(x,y)=C$ sin despejar $y$. Rectas tangentes a curvas implícitas.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 6,
    }


# =====================================================================
# LECCIÓN 2.7 — Derivación logarítmica
# =====================================================================
def lesson_2_7():
    blocks = [
        b("texto", body_md=(
            "Algunos productos y cocientes son tan complicados que aplicar las reglas estándar genera expresiones imposibles de simplificar. "
            "Otros, como $f(x)^{g(x)}$ con base y exponente variables, **no caen** en ninguna regla básica.\n\n"
            "La **derivación logarítmica** resuelve ambos casos: aplica $\\ln$ a ambos lados antes de derivar, lo que convierte productos en sumas y exponentes en multiplicadores.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar el método de **4 pasos**: tomar logaritmo, simplificar con propiedades de $\\ln$, derivar implícitamente, despejar.\n"
            "- Derivar productos y cocientes complicados con menos esfuerzo.\n"
            "- Derivar funciones de la forma $f(x)^{g(x)}$."
        )),

        b("definicion",
          titulo="Método de derivación logarítmica",
          body_md=(
              "Para derivar $y = f(x)$:\n\n"
              "1. **Tomar logaritmo natural** en ambos lados: $\\ln y = \\ln f(x)$.\n\n"
              "2. **Simplificar** usando las propiedades de los logaritmos:\n\n"
              "   - $\\ln(AB) = \\ln A + \\ln B$\n"
              "   - $\\ln(A/B) = \\ln A - \\ln B$\n"
              "   - $\\ln(A^k) = k \\ln A$\n\n"
              "3. **Derivar implícitamente**: la izquierda da $\\dfrac{y'}{y}$, la derecha se deriva normalmente.\n\n"
              "4. **Despejar $y'$** multiplicando por $y$ (y reescribiendo $y$ en términos de $x$ si conviene)."
          )),

        b("intuicion",
          titulo="¿Por qué simplifica?",
          body_md=(
              "El logaritmo es la función inversa del producto: convierte productos en sumas, cocientes en restas y potencias en factores. "
              "Esto reemplaza una derivada por **producto** o **cociente** complicada por una de **suma** — mucho más simple.\n\n"
              "**Ejemplo conceptual:** la derivada de $\\ln[(x^2)(x^3+1)] = 2\\ln x + \\ln(x^3+1)$ es trivial: $\\dfrac{2}{x} + \\dfrac{3x^2}{x^3+1}$. "
              "Calcular esa derivada **sin** logaritmo (con la regla del producto) hubiera sido más laborioso."
          )),

        b("ejemplo_resuelto",
          titulo="Producto difícil: $y = (x^2 + 1)^3 e^x \\sin x$",
          problema_md="Derivar usando derivación logarítmica.",
          pasos=[
              {"accion_md": "**Paso 1: tomar $\\ln$.** $\\ln y = \\ln[(x^2+1)^3 e^x \\sin x]$.\n\n**Paso 2: simplificar:**\n\n$$\\ln y = 3 \\ln(x^2+1) + x + \\ln(\\sin x)$$",
               "justificacion_md": "Aplicamos las propiedades: $\\ln$ de producto es suma, $\\ln$ de potencia es exponente por $\\ln$, y $\\ln(e^x) = x$.",
               "es_resultado": False},
              {"accion_md": "**Paso 3: derivar implícitamente:**\n\n$$\\dfrac{y'}{y} = \\dfrac{3 \\cdot 2x}{x^2+1} + 1 + \\dfrac{\\cos x}{\\sin x} = \\dfrac{6x}{x^2+1} + 1 + \\cot x$$",
               "justificacion_md": "Lado izquierdo: $(\\ln y)' = y'/y$. Lado derecho: $(\\ln u)' = u'/u$ aplicado a cada término.",
               "es_resultado": False},
              {"accion_md": "**Paso 4: despejar $y'$ multiplicando por $y$:**\n\n$$y' = (x^2+1)^3 e^x \\sin x \\cdot \\left[\\dfrac{6x}{x^2+1} + 1 + \\cot x\\right]$$",
               "justificacion_md": "Sustituimos $y$ por su forma original. **Comparación:** aplicar producto/cociente sin logaritmo hubiera requerido derivar tres factores con regla del producto extendida — más cuentas, más oportunidades de error.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Base y exponente variables: $y = (x^2 + 3x + 5)^{x+1}$",
          problema_md="Derivar.",
          pasos=[
              {"accion_md": "**Paso 1: $\\ln y = (x+1) \\ln(x^2+3x+5)$.**",
               "justificacion_md": "Aplicamos $\\ln$ y bajamos el exponente. **Importante:** sin logaritmo, esta derivada es directamente imposible — no es ni potencia (la base varía) ni exponencial (el exponente varía).",
               "es_resultado": False},
              {"accion_md": "**Paso 2: derivar el lado derecho con regla del producto:**\n\n$$\\dfrac{y'}{y} = (1) \\ln(x^2+3x+5) + (x+1) \\cdot \\dfrac{2x+3}{x^2+3x+5}$$",
               "justificacion_md": "Producto entre $(x+1)$ y $\\ln(x^2+3x+5)$: $u'v + uv'$. La derivada de $\\ln(x^2+3x+5)$ es $\\dfrac{2x+3}{x^2+3x+5}$ por cadena.",
               "es_resultado": False},
              {"accion_md": "**Paso 3: despejar $y'$:**\n\n$$y' = (x^2+3x+5)^{x+1} \\left[\\ln(x^2+3x+5) + \\dfrac{(x+1)(2x+3)}{x^2+3x+5}\\right]$$",
               "justificacion_md": "Multiplicamos por $y$ y reemplazamos por la expresión original. **Patrón general** para $f(x)^{g(x)}$: el resultado tiene dos términos — uno con $\\ln f$ (de derivar el exponente) y otro con $g \\cdot f'/f$ (de derivar la base).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="$y = x^x$",
          problema_md="Calcular $y'$.",
          pasos=[
              {"accion_md": "**$\\ln y = x \\ln x$.**",
               "justificacion_md": "Aplicamos $\\ln$ y propiedad de la potencia.",
               "es_resultado": False},
              {"accion_md": "**Derivamos** (regla del producto en la derecha):\n\n$$\\dfrac{y'}{y} = (1)\\ln x + x \\cdot \\dfrac{1}{x} = \\ln x + 1$$",
               "justificacion_md": "Producto entre $x$ y $\\ln x$.",
               "es_resultado": False},
              {"accion_md": "$$y' = x^x (\\ln x + 1)$$",
               "justificacion_md": "**Resultado clásico** que aparece en muchos contextos (probabilidad, optimización).",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el método:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuándo conviene usar derivación logarítmica?",
                  "opciones_md": [
                      "Para cualquier derivada, siempre simplifica.",
                      "Cuando hay productos/cocientes muy complicados o $f(x)^{g(x)}$ con $f, g$ no constantes.",
                      "Solo cuando aparece $\\ln x$ explícito.",
                      "Solo para derivadas de orden superior.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Para derivadas simples, las reglas estándar son más rápidas. La derivación logarítmica brilla en dos casos: productos/cocientes con muchos factores y $f(x)^{g(x)}$ — ese segundo caso ni siquiera se puede atacar con las reglas básicas."
                  ),
              },
              {
                  "enunciado_md": "Si $y = (\\sin x)^{\\cos x}$, ¿cuál es el primer paso?",
                  "opciones_md": [
                      "Aplicar la regla de la potencia: $\\cos x \\cdot (\\sin x)^{\\cos x - 1}$.",
                      "Aplicar $\\ln$ y obtener $\\ln y = \\cos x \\cdot \\ln(\\sin x)$.",
                      "Aplicar la regla del producto.",
                      "Derivar como $e^{x \\cos x}$.",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Como base ($\\sin x$) y exponente ($\\cos x$) son ambas variables, ninguna regla básica aplica. Se toma $\\ln$ y se baja el exponente: $\\ln y = \\cos x \\cdot \\ln(\\sin x)$, luego se deriva implícitamente."
                  ),
              },
          ]),

        fig(
            "Esquema procedimental en cuatro pasos para derivacion logaritmica, en formato infografia "
            "vertical. Paso 1 (teal #06b6d4): 'Aplicar ln a ambos lados: ln y = ln f(x)'. Paso 2: 'Usar "
            "propiedades del logaritmo: convertir productos en sumas, exponentes en multiplicaciones'. "
            "Paso 3 (ambar #f59e0b): 'Derivar implicitamente: (1/y) y' = (lado derecho)'. Paso 4: "
            "'Multiplicar por y para despejar y prima'. Numeros encerrados en circulos teal. " + STYLE
        ),
        ej(
            "Derivada logarítmica de un producto complicado",
            "Calcula $f'(x)$ usando derivación logarítmica para $f(x) = \\dfrac{(x+1)^3 \\sqrt{x-2}}{(x^2+5)^2}$ (asume $x > 2$).",
            [
                "Toma logaritmo natural y usa $\\ln(ab/c) = \\ln a + \\ln b - \\ln c$ y $\\ln(a^n) = n \\ln a$.",
                "Después de derivar implícitamente, multiplica por $f(x)$ para obtener $f'(x)$.",
            ],
            "**Paso 1 — Aplicar $\\ln$.**\n\n$$\\ln f(x) = 3\\ln(x+1) + \\tfrac{1}{2}\\ln(x-2) - 2\\ln(x^2 + 5).$$\n\n**Paso 2 — Derivar implícitamente.**\n\n$$\\dfrac{f'(x)}{f(x)} = \\dfrac{3}{x+1} + \\dfrac{1}{2(x-2)} - \\dfrac{4x}{x^2+5}.$$\n\n**Paso 3 — Despejar.**\n\n$$f'(x) = \\dfrac{(x+1)^3 \\sqrt{x-2}}{(x^2+5)^2}\\left[\\dfrac{3}{x+1} + \\dfrac{1}{2(x-2)} - \\dfrac{4x}{x^2+5}\\right].$$",
        ),
        ej(
            "Función de la forma $f(x)^{g(x)}$",
            "Calcula la derivada de $y = x^{\\ln x}$ con $x > 0$.",
            [
                "Toma $\\ln$: $\\ln y = \\ln x \\cdot \\ln x = (\\ln x)^2$.",
                "Deriva implícitamente: $y'/y = 2 \\ln x \\cdot (1/x)$.",
            ],
            "**Paso 1 — Aplicar $\\ln$.** $\\ln y = (\\ln x)(\\ln x) = (\\ln x)^2$.\n\n**Paso 2 — Derivar.** Lado izquierdo: $\\dfrac{y'}{y}$. Lado derecho (cadena): $2 \\ln x \\cdot \\dfrac{1}{x} = \\dfrac{2 \\ln x}{x}$.\n\n**Paso 3 — Despejar.**\n\n$$y' = y \\cdot \\dfrac{2 \\ln x}{x} = x^{\\ln x} \\cdot \\dfrac{2 \\ln x}{x} = \\dfrac{2 \\ln x \\cdot x^{\\ln x}}{x}.$$\n\nO equivalentemente $y' = 2 \\ln x \\cdot x^{\\ln x - 1}$.",
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar la regla de la potencia $(x^n)' = n x^{n-1}$ a $f(x)^{g(x)}$.** Esa regla solo vale cuando el exponente es **constante**.",
              "**Olvidar multiplicar por $y$ al final** y reportar como respuesta solo $\\dfrac{y'}{y}$.",
              "**No reescribir $y$ en términos de $x$** al final. La respuesta debe ser una función explícita de $x$.",
              "**Tomar $\\ln$ cuando $y$ puede ser negativo.** Para ser rigurosos, en ese caso se aplica $\\ln|y|$ y la derivada es la misma — pero el dominio donde se aplica el método debe ser revisado.",
              "**Confundirse con las propiedades de los logaritmos.** $\\ln(A+B) \\neq \\ln A + \\ln B$. La propiedad solo aplica a productos.",
          ]),

        b("resumen",
          puntos_md=[
              "**Método (4 pasos):** tomar $\\ln$ → simplificar con propiedades → derivar implícitamente → despejar $y'$ multiplicando por $y$.",
              "**Útil cuando:** hay productos/cocientes complicados, o cuando aparece $f(x)^{g(x)}$ con $f, g$ no constantes.",
              "**Resultado típico:** $y' = y \\cdot [\\text{lo que dio el lado derecho}]$.",
              "**Caso clásico** $y = x^x$: $y' = x^x(\\ln x + 1)$.",
              "**Próxima lección:** derivadas de funciones inversas — incluyendo arcseno, arccoseno y arctangente.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-7-logaritmica",
        "title": "Derivación logarítmica",
        "description": "Aplicar $\\ln$ antes de derivar para simplificar productos, cocientes y exponentes variables.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 7,
    }


# =====================================================================
# LECCIÓN 2.8 — Derivadas de funciones inversas
# =====================================================================
def lesson_2_8():
    blocks = [
        b("texto", body_md=(
            "Si $f$ es una función biyectiva en un intervalo, su **inversa** $f^{-1}$ existe y satisface $f(f^{-1}(x)) = x$. "
            "Esta lección deduce una **fórmula general** para la derivada de la inversa, y la aplica a las funciones trigonométricas inversas: $\\arcsin, \\arccos, \\arctan$.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar la fórmula $(f^{-1})'(x) = \\dfrac{1}{f'(f^{-1}(x))}$.\n"
            "- Conocer y manejar las derivadas de $\\arcsin, \\arccos, \\arctan$.\n"
            "- Comprender la geometría: pendientes recíprocas en puntos simétricos respecto a la recta $y = x$."
        )),

        b("teorema",
          nombre="Derivada de la inversa",
          enunciado_md=(
              "Si $f$ es derivable y biyectiva en un intervalo, con $f'(a) \\neq 0$ donde $a = f^{-1}(x)$, entonces $f^{-1}$ es derivable en $x$ y:\n\n"
              "$$\\dfrac{d}{dx}[f^{-1}(x)] = \\dfrac{1}{f'(f^{-1}(x))}$$"
          ),
          demostracion_md=(
              "Partimos de la identidad $f(f^{-1}(x)) = x$ y derivamos ambos lados respecto a $x$ (cadena en el lado izquierdo):\n\n"
              "$$f'(f^{-1}(x)) \\cdot (f^{-1})'(x) = 1$$\n\n"
              "Despejando, $\\dfrac{(f^{-1})'(x)}{1} = \\dfrac{1}{f'(f^{-1}(x))}$, siempre que el denominador no se anule."
          )),

        b("intuicion",
          titulo="Geometría: pendientes recíprocas",
          body_md=(
              "Las gráficas de $f$ y $f^{-1}$ son **reflejos respecto a la recta $y = x$**. "
              "En puntos simétricos, las pendientes son **recíprocas**: si $f$ pasa por $(a, b)$ con pendiente $m$, entonces $f^{-1}$ pasa por $(b, a)$ con pendiente $\\dfrac{1}{m}$.\n\n"
              "La fórmula del teorema captura exactamente eso."
          )),

        b("ejemplo_resuelto",
          titulo="Derivada de $f^{-1}$ donde $f(x) = x^3 + 2x + 1$",
          problema_md="Calcular $(f^{-1})'(1)$.",
          pasos=[
              {"accion_md": "**Necesitamos $f^{-1}(1)$**, es decir, el $a$ tal que $f(a) = 1$. Resolvemos: $a^3 + 2a + 1 = 1 \\implies a(a^2 + 2) = 0 \\implies a = 0$.",
               "justificacion_md": "$a^2 + 2 > 0$ siempre, así la única solución real es $a = 0$.",
               "es_resultado": False},
              {"accion_md": "**Derivamos $f$:** $f'(x) = 3x^2 + 2$. Evaluamos en $a = 0$: $f'(0) = 2$.",
               "justificacion_md": "Derivada estándar.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la fórmula:**\n\n$$(f^{-1})'(1) = \\dfrac{1}{f'(0)} = \\dfrac{1}{2}$$",
               "justificacion_md": "**Útil porque** despejar $f^{-1}$ explícitamente desde $y = x^3 + 2x + 1$ es difícil. La fórmula da la derivada sin necesidad de la inversa explícita.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Derivadas de las trigonométricas inversas",
          body_md=(
              "$$\\dfrac{d}{dx}[\\arcsin x] = \\dfrac{1}{\\sqrt{1 - x^2}}, \\quad |x| < 1$$\n\n"
              "$$\\dfrac{d}{dx}[\\arccos x] = -\\dfrac{1}{\\sqrt{1 - x^2}}, \\quad |x| < 1$$\n\n"
              "$$\\dfrac{d}{dx}[\\arctan x] = \\dfrac{1}{1 + x^2}, \\quad x \\in \\mathbb{R}$$"
          )),

        b("ejemplo_resuelto",
          titulo="Deducción de $(\\arcsin x)'$",
          problema_md="Demostrar que $(\\arcsin x)' = \\dfrac{1}{\\sqrt{1-x^2}}$.",
          pasos=[
              {"accion_md": "Sea $y = \\arcsin x$, equivalente a $\\sin y = x$ con $y \\in [-\\pi/2, \\pi/2]$.",
               "justificacion_md": "Definición de la inversa restringida al intervalo principal.",
               "es_resultado": False},
              {"accion_md": "**Derivación implícita** respecto a $x$: $\\cos y \\cdot y' = 1$, así $y' = \\dfrac{1}{\\cos y}$.",
               "justificacion_md": "$(\\sin y)' = \\cos y \\cdot y'$ por cadena.",
               "es_resultado": False},
              {"accion_md": "**Expresamos $\\cos y$ en términos de $x$.** Como $y \\in [-\\pi/2, \\pi/2]$, $\\cos y \\geq 0$. Por la identidad pitagórica:\n\n$$\\cos y = \\sqrt{1 - \\sin^2 y} = \\sqrt{1 - x^2}$$",
               "justificacion_md": "El signo positivo es por estar en el primer y cuarto cuadrante (donde $\\cos$ es no-negativo).",
               "es_resultado": False},
              {"accion_md": "$$y' = \\dfrac{1}{\\sqrt{1-x^2}}$$",
               "justificacion_md": "**Patrón general:** las derivadas de las inversas trigonométricas son **algebraicas** (raíces, fracciones racionales) — un resultado sorprendente y muy útil.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $h(x) = \\arctan(x^2)$",
          problema_md="Calcular $h'(x)$.",
          pasos=[
              {"accion_md": "**Cadena:** exterior $\\arctan u$ con derivada $\\dfrac{1}{1+u^2}$, interior $u = x^2$ con derivada $2x$.",
               "justificacion_md": "Composición simple.",
               "es_resultado": False},
              {"accion_md": "$$h'(x) = \\dfrac{1}{1+(x^2)^2} \\cdot 2x = \\dfrac{2x}{1 + x^4}$$",
               "justificacion_md": "Resultado totalmente algebraico.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo:",
          preguntas=[
              {
                  "enunciado_md": "$\\dfrac{d}{dx}[\\arcsin(2x)] = ?$",
                  "opciones_md": [
                      "$\\dfrac{1}{\\sqrt{1-4x^2}}$",
                      "$\\dfrac{2}{\\sqrt{1-4x^2}}$",
                      "$\\dfrac{2}{\\sqrt{1-x^2}}$",
                      "$\\dfrac{1}{\\sqrt{1-x^2}}$",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Cadena con $u = 2x$: $\\dfrac{1}{\\sqrt{1-u^2}} \\cdot 2 = \\dfrac{2}{\\sqrt{1-4x^2}}$."
                  ),
              },
              {
                  "enunciado_md": "Si $f(x) = x + e^x$, ¿cuál es $(f^{-1})'(1)$? (Note que $f(0) = 1$.)",
                  "opciones_md": ["$\\dfrac{1}{2}$", "$2$", "$1$", "$0$"],
                  "correcta": "A",
                  "explicacion_md": (
                      "$f'(x) = 1 + e^x$, así $f'(0) = 1 + 1 = 2$. Por la fórmula: $(f^{-1})'(1) = 1/f'(0) = 1/2$."
                  ),
              },
          ]),

        fig(
            "Esquema visual del teorema de la funcion inversa: dos curvas en el plano, y = f(x) en teal "
            "#06b6d4 y la inversa y = f-1(x) en ambar #f59e0b, simetricas respecto a la recta y = x "
            "(linea punteada gris). Marca dos puntos: P=(a, b) en f y Q=(b, a) en f-1. En cada punto "
            "dibuja la tangente con su pendiente: en P pendiente m, en Q pendiente 1/m. Anotacion: "
            "'(f-1)'(b) = 1/f'(a)'. Ejes etiquetados, fondo blanco. " + STYLE
        ),
        ej(
            "Aplicar la fórmula $(f^{-1})'(b) = 1/f'(a)$",
            "Sea $f(x) = x^3 + 2x + 1$. Sin calcular la inversa explícitamente, calcula $(f^{-1})'(4)$.",
            [
                "Encuentra $a$ tal que $f(a) = 4$ por inspección.",
                "Calcula $f'(a)$ y aplica la fórmula del teorema de la función inversa.",
            ],
            "**Paso 1 — Encontrar $a$ tal que $f(a) = 4$.** Probamos $a = 1$: $1 + 2 + 1 = 4$. ✓ Así que $f(1) = 4$, lo que implica $f^{-1}(4) = 1$.\n\n**Paso 2 — Verificar que $f$ es invertible localmente.** $f'(x) = 3x^2 + 2 > 0$ para todo $x$, así $f$ es estrictamente creciente — invertible.\n\n**Paso 3 — Calcular $f'(1)$.** $f'(1) = 3(1)^2 + 2 = 5$.\n\n**Paso 4 — Aplicar la fórmula.** $(f^{-1})'(4) = \\dfrac{1}{f'(1)} = \\dfrac{1}{5}$.",
        ),
        ej(
            "Recta tangente a la inversa",
            "Sea $f(x) = x + \\ln x$ (con $x > 0$). Sabiendo que $f(1) = 1$, encuentra la ecuación de la recta tangente a $y = f^{-1}(x)$ en el punto $(1, 1)$.",
            [
                "La pendiente buscada es $(f^{-1})'(1) = 1/f'(1)$.",
                "Calcula $f'(x) = 1 + 1/x$.",
            ],
            "**Paso 1 — Punto de tangencia.** $f(1) = 1 + \\ln 1 = 1$, así $f^{-1}(1) = 1$. El punto en la curva inversa es $(1, 1)$.\n\n**Paso 2 — Derivada.** $f'(x) = 1 + \\dfrac{1}{x}$. En $x = 1$: $f'(1) = 1 + 1 = 2$.\n\n**Paso 3 — Pendiente de la inversa.** $(f^{-1})'(1) = \\dfrac{1}{f'(1)} = \\dfrac{1}{2}$.\n\n**Paso 4 — Recta tangente.** $y - 1 = \\dfrac{1}{2}(x - 1) \\Rightarrow y = \\dfrac{x}{2} + \\dfrac{1}{2}$.",
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $f^{-1}(x)$ con $1/f(x)$.** $f^{-1}$ es la **inversa funcional**, no el recíproco.",
              "**Olvidar que $\\arcsin$ y $\\arccos$ tienen dominio $[-1, 1]$.** Las fórmulas $\\dfrac{1}{\\sqrt{1-x^2}}$ no aplican fuera de ese intervalo.",
              "**Olvidar el signo negativo en $(\\arccos x)'$.**",
              "**Aplicar la fórmula $(f^{-1})'(x) = 1/f'(x)$.** ¡Es $1/f'(f^{-1}(x))$! La derivada se evalúa en la inversa, no en $x$.",
          ]),

        b("resumen",
          puntos_md=[
              "**Fórmula:** $(f^{-1})'(x) = \\dfrac{1}{f'(f^{-1}(x))}$.",
              "**Geometría:** pendientes recíprocas en puntos simétricos respecto a $y = x$.",
              "$(\\arcsin x)' = \\dfrac{1}{\\sqrt{1-x^2}}$, $(\\arccos x)' = -\\dfrac{1}{\\sqrt{1-x^2}}$, $(\\arctan x)' = \\dfrac{1}{1+x^2}$.",
              "**Las inversas trigonométricas tienen derivadas algebraicas.** Esto las hace muy útiles en integración.",
              "**Próxima lección:** derivadas de exponenciales y logaritmos en cualquier base.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-8-inversas",
        "title": "Derivadas de funciones inversas",
        "description": "Fórmula general para $(f^{-1})'$ y derivadas de $\\arcsin, \\arccos, \\arctan$.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 8,
    }


# =====================================================================
# LECCIÓN 2.9 — Derivadas de funciones logarítmicas y exponenciales
# =====================================================================
def lesson_2_9():
    blocks = [
        b("texto", body_md=(
            "Las funciones exponenciales y logarítmicas aparecen en interés compuesto, crecimiento poblacional, decaimiento radiactivo, modelos epidemiológicos. Esta lección compila sus derivadas — algunas ya las usamos en lecciones anteriores, ahora las formalizamos.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Conocer y aplicar las derivadas de $e^x$, $a^x$, $\\ln x$, $\\log_a x$.\n"
            "- Combinarlas con la regla de la cadena.\n"
            "- Comprender por qué $e$ es la base \"natural\": $\\dfrac{d}{dx}[e^x] = e^x$."
        )),

        b("definicion",
          titulo="Derivadas fundamentales",
          body_md=(
              "$$\\dfrac{d}{dx}[e^x] = e^x$$\n\n"
              "$$\\dfrac{d}{dx}[a^x] = a^x \\ln a, \\quad a > 0$$\n\n"
              "$$\\dfrac{d}{dx}[\\ln x] = \\dfrac{1}{x}, \\quad x > 0$$\n\n"
              "$$\\dfrac{d}{dx}[\\log_a x] = \\dfrac{1}{x \\ln a}, \\quad x > 0, \\; a > 0, \\; a \\neq 1$$"
          )),

        b("intuicion",
          titulo="¿Por qué $e^x$ es \"el rey\" de las exponenciales?",
          body_md=(
              "$e^x$ es la **única función** (salvo constantes multiplicativas) cuya derivada es ella misma:\n\n"
              "$$\\dfrac{d}{dx}[e^x] = e^x$$\n\n"
              "Esto la hace fundamental en ecuaciones diferenciales: el crecimiento exponencial natural ($\\dot{y} = ky$) tiene a $e^{kx}$ como solución.\n\n"
              "Para otra base: $\\dfrac{d}{dx}[a^x] = a^x \\ln a$. El factor $\\ln a$ es el \"defecto\" de $a$ respecto a $e$: cuando $a = e$, $\\ln e = 1$ y desaparece."
          )),

        b("teorema",
          nombre="Derivada de $a^x$",
          enunciado_md="$\\dfrac{d}{dx}[a^x] = a^x \\ln a$.",
          demostracion_md=(
              "Reescribimos $a^x = e^{x \\ln a}$. Por cadena (exterior $e^u$, interior $x \\ln a$):\n\n"
              "$$\\dfrac{d}{dx}[e^{x \\ln a}] = e^{x \\ln a} \\cdot \\ln a = a^x \\ln a$$"
          )),

        b("teorema",
          nombre="Derivada de $\\ln x$",
          enunciado_md="$\\dfrac{d}{dx}[\\ln x] = \\dfrac{1}{x}$ para $x > 0$.",
          demostracion_md=(
              "Sea $y = \\ln x$, equivalente a $e^y = x$. Derivando implícitamente:\n\n"
              "$$e^y \\cdot y' = 1 \\implies y' = \\dfrac{1}{e^y} = \\dfrac{1}{x}$$"
          )),

        b("ejemplo_resuelto",
          titulo="Derivar $f(x) = 3^x$",
          problema_md="Calcular $f'(x)$.",
          pasos=[
              {"accion_md": "Aplicación directa de la fórmula con $a = 3$:\n\n$$f'(x) = 3^x \\ln 3$$",
               "justificacion_md": "$\\ln 3$ es un número fijo ($\\approx 1.0986$).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $g(x) = e^{2x}$",
          problema_md="Calcular $g'(x)$.",
          pasos=[
              {"accion_md": "**Cadena:** exterior $e^u$ con derivada $e^u$, interior $u = 2x$ con derivada $2$.\n\n$$g'(x) = e^{2x} \\cdot 2 = 2 e^{2x}$$",
               "justificacion_md": "Cuando el exponente es un múltiplo de $x$, aparece ese múltiplo como factor.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $h(x) = \\log_2 x$",
          problema_md="Calcular $h'(x)$.",
          pasos=[
              {"accion_md": "Aplicación directa: $h'(x) = \\dfrac{1}{x \\ln 2}$.",
               "justificacion_md": "$\\ln 2 \\approx 0.693$ es un número fijo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $k(x) = \\ln(3x + 1)$",
          problema_md="Calcular $k'(x)$.",
          pasos=[
              {"accion_md": "**Cadena:** exterior $\\ln u$ con derivada $1/u$, interior $u = 3x + 1$ con derivada $3$.\n\n$$k'(x) = \\dfrac{1}{3x+1} \\cdot 3 = \\dfrac{3}{3x+1}$$",
               "justificacion_md": "**Patrón:** $\\dfrac{d}{dx}[\\ln(g(x))] = \\dfrac{g'(x)}{g(x)}$, llamado **derivada logarítmica** de $g$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $f(x) = e^{x^2} \\sin x$",
          problema_md="Calcular $f'(x)$.",
          pasos=[
              {"accion_md": "**Producto** con $u = e^{x^2}$ y $v = \\sin x$. Derivada de $u$ por cadena: $u' = e^{x^2} \\cdot 2x$. Derivada de $v$: $v' = \\cos x$.",
               "justificacion_md": "Identificación y derivadas de cada factor.",
               "es_resultado": False},
              {"accion_md": "$$f'(x) = 2x e^{x^2} \\sin x + e^{x^2} \\cos x = e^{x^2}(2x \\sin x + \\cos x)$$",
               "justificacion_md": "Factorizamos $e^{x^2}$ común para presentar la respuesta más limpia.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo:",
          preguntas=[
              {
                  "enunciado_md": "$\\dfrac{d}{dx}[\\ln(\\cos x)] = ?$",
                  "opciones_md": [
                      "$\\dfrac{1}{\\cos x}$",
                      "$-\\tan x$",
                      "$\\tan x$",
                      "$\\dfrac{\\sin x}{\\cos x}$",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "Cadena: $(\\ln u)' = u'/u$ con $u = \\cos x$. Da $\\dfrac{-\\sin x}{\\cos x} = -\\tan x$."
                  ),
              },
              {
                  "enunciado_md": "$\\dfrac{d}{dx}[5^x] = ?$",
                  "opciones_md": ["$5^x$", "$x \\cdot 5^{x-1}$", "$5^x \\ln 5$", "$5 \\cdot \\ln x$"],
                  "correcta": "C",
                  "explicacion_md": (
                      "Para $a^x$ la derivada es $a^x \\ln a$. La opción A omite $\\ln a$ (sería incorrecto salvo $a = e$). La B confunde con la regla de la potencia."
                  ),
              },
          ]),

        fig(
            "Tabla-resumen visual con cuatro reglas de derivacion logaritmico-exponencial. Filas con "
            "borde teal #06b6d4 a la izquierda: (1) (e^x)' = e^x con nota 'caso especial', (2) (a^x)' = "
            "a^x ln a en ambar #f59e0b destacando 'ln a', (3) (ln x)' = 1/x para x>0, (4) (log_a x)' = "
            "1/(x ln a). Cada formula con un ejemplo numerico breve a la derecha. Tipografia matematica, "
            "fondo blanco, formato de tarjeta limpia. " + STYLE
        ),
        ej(
            "Derivar combinando exponencial y cadena",
            "Calcula $f'(x)$ para $f(x) = e^{2x} \\ln(x^2 + 1)$.",
            [
                "Aplica regla del producto y luego cadena en cada factor.",
                "Recuerda $(\\ln u)' = u'/u$ y $(e^{u})' = e^{u} \\cdot u'$.",
            ],
            "**Identificación:** producto de $u = e^{2x}$ y $v = \\ln(x^2 + 1)$.\n\n**Derivada de $u$:** cadena con interior $2x$ → $u' = e^{2x} \\cdot 2 = 2 e^{2x}$.\n\n**Derivada de $v$:** $v' = \\dfrac{(x^2 + 1)'}{x^2 + 1} = \\dfrac{2x}{x^2 + 1}$.\n\n**Regla del producto:**\n\n$$f'(x) = 2 e^{2x} \\ln(x^2 + 1) + e^{2x} \\cdot \\dfrac{2x}{x^2+1} = 2 e^{2x}\\!\\left[\\ln(x^2+1) + \\dfrac{x}{x^2+1}\\right].$$",
        ),
        ej(
            "Crecimiento exponencial — interpretación",
            "La población de una colonia de bacterias crece según $N(t) = 500 \\cdot e^{0{,}3 t}$ (con $t$ en horas). Calcula la **tasa de crecimiento instantánea** a las $t = 4$ horas e interpreta el resultado.",
            [
                "Calcula $N'(t)$ usando la cadena con $u = 0{,}3 t$.",
                "Evalúa $N'(4)$ y reporta unidades adecuadas (bacterias/hora).",
            ],
            "**Paso 1 — Derivada.** $N'(t) = 500 \\cdot e^{0{,}3 t} \\cdot 0{,}3 = 150\\, e^{0{,}3 t}$.\n\n**Paso 2 — Evaluar en $t = 4$.** $N'(4) = 150 \\cdot e^{1{,}2} \\approx 150 \\cdot 3{,}3201 \\approx 498$ bacterias/hora.\n\n**Interpretación:** a las $4$ horas, la colonia crece aproximadamente a $498$ bacterias por hora. Observa que $N'(t) = 0{,}3 \\cdot N(t)$, es decir, la tasa de crecimiento es proporcional a la población actual — característica del crecimiento exponencial.",
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $a^x$ con $x^a$.** $\\dfrac{d}{dx}[x^a] = a x^{a-1}$ (potencia), pero $\\dfrac{d}{dx}[a^x] = a^x \\ln a$ (exponencial). La variable está en distinta posición.",
              "**Olvidar el factor $\\ln a$ en $(a^x)'$.** Cuando la base es $e$, $\\ln e = 1$ y \"desaparece\"; en cualquier otra base, hay que escribirlo.",
              "**Pensar que $(\\ln x)' = \\ln$.** La derivada es $1/x$, una función completamente distinta.",
              "**Aplicar $(\\ln x)' = 1/x$ a $\\ln(g(x))$ olvidando la cadena.** La forma correcta es $\\dfrac{g'(x)}{g(x)}$.",
              "**Pensar que el dominio de $\\ln$ incluye $0$ o negativos.** $\\ln$ está definido solo para $x > 0$.",
          ]),

        b("resumen",
          puntos_md=[
              "$(e^x)' = e^x$, $(a^x)' = a^x \\ln a$.",
              "$(\\ln x)' = 1/x$, $(\\log_a x)' = 1/(x \\ln a)$.",
              "**$e$ es la base natural** porque su exponencial es su propia derivada.",
              "**Patrón con cadena:** $\\dfrac{d}{dx}[\\ln(g(x))] = \\dfrac{g'(x)}{g(x)}$ (derivada logarítmica).",
              "**Próxima lección:** regla de L'Hôpital, una aplicación poderosa de las derivadas para resolver límites indeterminados.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-9-log-exp",
        "title": "Derivadas de funciones logarítmicas y exponenciales",
        "description": "Derivadas de $e^x, a^x, \\ln x, \\log_a x$ y sus combinaciones.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 9,
    }


# =====================================================================
# LECCIÓN 2.10 — Regla de L'Hôpital
# =====================================================================
def lesson_2_10():
    blocks = [
        b("texto", body_md=(
            "En el capítulo de límites mencionamos la **regla de L'Hôpital** como una herramienta para resolver indeterminaciones, pero pospusimos su tratamiento porque requiere derivadas. Llegó el momento.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar L'Hôpital para indeterminaciones $\\dfrac{0}{0}$ y $\\dfrac{\\infty}{\\infty}$.\n"
            "- Reconocer y manipular **otras formas indeterminadas** ($0 \\cdot \\infty$, $\\infty - \\infty$, $1^\\infty$, $0^0$, $\\infty^0$) para reducirlas a una de las dos básicas.\n"
            "- Identificar las **hipótesis** del teorema y los casos donde no aplica."
        )),

        b("teorema",
          nombre="Regla de L'Hôpital",
          enunciado_md=(
              "Si $f$ y $g$ son derivables cerca de $a$ (excepto quizá en $a$ mismo), $g'(x) \\neq 0$ cerca de $a$, y se cumple **una** de:\n\n"
              "- $\\lim_{x \\to a} f(x) = 0$ y $\\lim_{x \\to a} g(x) = 0$ (caso $\\dfrac{0}{0}$), o\n"
              "- $\\lim_{x \\to a} |f(x)| = \\infty$ y $\\lim_{x \\to a} |g(x)| = \\infty$ (caso $\\dfrac{\\infty}{\\infty}$),\n\n"
              "entonces:\n\n"
              "$$\\lim_{x \\to a} \\dfrac{f(x)}{g(x)} = \\lim_{x \\to a} \\dfrac{f'(x)}{g'(x)}$$\n\n"
              "siempre que el límite del lado derecho exista (finito o infinito). El teorema vale también para $a = \\pm \\infty$ y para límites laterales."
          )),

        b("intuicion",
          titulo="Por qué funciona",
          body_md=(
              "Cerca de $a$, si ambas funciones se anulan, las podemos aproximar por sus rectas tangentes:\n\n"
              "$$f(x) \\approx f'(a)(x - a), \\quad g(x) \\approx g'(a)(x - a)$$\n\n"
              "Sustituyendo en el cociente, los factores $(x-a)$ se cancelan y queda $f'(a)/g'(a)$.\n\n"
              "**No es** una receta mágica: es la observación de que cerca del punto problemático, las funciones se comportan como sus derivadas. Para una demostración formal se usa el **teorema del valor medio de Cauchy**."
          )),

        b("ejemplo_resuelto",
          titulo="$\\lim_{x \\to 0} \\dfrac{\\sin x}{x}$",
          problema_md="Resolver con L'Hôpital.",
          pasos=[
              {"accion_md": "Sustitución directa: $\\dfrac{0}{0}$. Aplicamos L'Hôpital derivando numerador y denominador:\n\n$$\\lim_{x \\to 0} \\dfrac{\\cos x}{1} = \\cos(0) = 1$$",
               "justificacion_md": "**Caveat circular:** este límite ya lo conocíamos del capítulo de límites, y se usó en la **demostración** de $(\\sin x)' = \\cos x$. Por eso L'Hôpital aquí es \"trampa\" — pero el ejemplo ilustra el uso mecánico de la regla.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="$\\lim_{x \\to 0} \\dfrac{e^x - 1 - x}{x^2}$",
          problema_md="Aplicar L'Hôpital varias veces.",
          pasos=[
              {"accion_md": "Sustitución: $\\dfrac{0}{0}$. Derivamos: $\\lim_{x\\to 0} \\dfrac{e^x - 1}{2x}$. Volvemos a sustituir: $\\dfrac{0}{0}$.",
               "justificacion_md": "L'Hôpital se aplica **mientras la indeterminación persista**, siempre que se mantengan las hipótesis.",
               "es_resultado": False},
              {"accion_md": "Aplicamos L'Hôpital de nuevo: $\\lim_{x\\to 0} \\dfrac{e^x}{2} = \\dfrac{1}{2}$.",
               "justificacion_md": "Ya no hay indeterminación. Sustitución directa.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Otras formas indeterminadas",
          body_md=(
              "L'Hôpital exige $\\dfrac{0}{0}$ o $\\dfrac{\\infty}{\\infty}$. Pero hay otras indeterminaciones que se pueden **transformar** en una de esas:\n\n"
              "- **$0 \\cdot \\infty$:** reescribir como $\\dfrac{0}{1/\\infty} = \\dfrac{0}{0}$ o $\\dfrac{\\infty}{1/0} = \\dfrac{\\infty}{\\infty}$.\n"
              "- **$\\infty - \\infty$:** combinar en una sola fracción (denominador común).\n"
              "- **$1^\\infty, 0^0, \\infty^0$:** tomar logaritmo: si $L = \\lim f^g$, entonces $\\ln L = \\lim g \\ln f$, que cae en $0 \\cdot \\infty$.\n\n"
              "**Las indeterminaciones $\\dfrac{0}{\\infty}$, $\\dfrac{\\infty}{0}$, $0^\\infty$, $\\infty^\\infty$ NO existen** — esos cocientes/exponenciales tienen valor determinado ($0$ o $\\pm \\infty$)."
          )),

        b("ejemplo_resuelto",
          titulo="Forma $0 \\cdot \\infty$: $\\lim_{x \\to 0^+} x \\ln x$",
          problema_md="Resolver el límite.",
          pasos=[
              {"accion_md": "Sustitución directa: $0 \\cdot (-\\infty)$, indeterminación. **Reescribimos** como cociente:\n\n$$x \\ln x = \\dfrac{\\ln x}{1/x}$$",
               "justificacion_md": "Cuando $x \\to 0^+$, $\\ln x \\to -\\infty$ y $1/x \\to +\\infty$: indeterminación $\\dfrac{-\\infty}{+\\infty}$, donde aplica L'Hôpital.",
               "es_resultado": False},
              {"accion_md": "**L'Hôpital:**\n\n$$\\lim_{x \\to 0^+} \\dfrac{\\ln x}{1/x} = \\lim_{x \\to 0^+} \\dfrac{1/x}{-1/x^2} = \\lim_{x \\to 0^+}(-x) = 0$$",
               "justificacion_md": "$(\\ln x)' = 1/x$ y $(1/x)' = -1/x^2$. Simplificación: $\\dfrac{1/x}{-1/x^2} = -x$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Forma $1^\\infty$: $\\lim_{x \\to \\infty}\\left(1 + \\dfrac{1}{x}\\right)^x$",
          problema_md="Calcular el límite (debería dar $e$).",
          pasos=[
              {"accion_md": "Sea $L$ el límite. Aplicamos $\\ln$:\n\n$$\\ln L = \\lim_{x \\to \\infty} x \\ln\\left(1 + \\dfrac{1}{x}\\right)$$",
               "justificacion_md": "Bajamos el exponente con la propiedad $\\ln(A^B) = B \\ln A$. Es la técnica estándar para $1^\\infty$, $0^0$, $\\infty^0$.",
               "es_resultado": False},
              {"accion_md": "Forma $\\infty \\cdot 0$. Reescribimos como cociente:\n\n$$\\lim_{x\\to\\infty} \\dfrac{\\ln(1 + 1/x)}{1/x}$$\n\nForma $\\dfrac{0}{0}$. Aplicamos L'Hôpital.",
               "justificacion_md": "Cuando $x \\to \\infty$, $1/x \\to 0$ y $\\ln(1+1/x) \\to \\ln 1 = 0$.",
               "es_resultado": False},
              {"accion_md": "Derivamos: el numerador $\\ln(1 + 1/x)$ tiene derivada $\\dfrac{1}{1 + 1/x} \\cdot (-1/x^2) = \\dfrac{-1/x^2}{1 + 1/x}$. El denominador $1/x$ tiene derivada $-1/x^2$.\n\n$$\\dfrac{-1/x^2 / (1+1/x)}{-1/x^2} = \\dfrac{1}{1 + 1/x} \\to 1$$",
               "justificacion_md": "Cociente: las derivadas de los factores $-1/x^2$ se cancelan.",
               "es_resultado": False},
              {"accion_md": "$\\ln L = 1$, así $L = e$.",
               "justificacion_md": "**Resultado clásico:** este límite es **una de las definiciones** del número $e$. Aquí lo recuperamos vía L'Hôpital.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Forma $\\infty - \\infty$: $\\lim_{x \\to 0^+}\\left(\\dfrac{1}{\\sin x} - \\dfrac{1}{x}\\right)$",
          problema_md="Resolver.",
          pasos=[
              {"accion_md": "Forma $\\infty - \\infty$. **Combinamos en una fracción** con denominador común:\n\n$$\\lim_{x\\to 0^+} \\dfrac{x - \\sin x}{x \\sin x}$$\n\nForma $\\dfrac{0}{0}$.",
               "justificacion_md": "Estrategia clásica para $\\infty - \\infty$: convertir a un solo cociente.",
               "es_resultado": False},
              {"accion_md": "**L'Hôpital:** $\\dfrac{1 - \\cos x}{\\sin x + x \\cos x}$. Sustitución: $\\dfrac{0}{0}$, repetimos.",
               "justificacion_md": "Numerador: $(x - \\sin x)' = 1 - \\cos x$. Denominador: $(x \\sin x)' = \\sin x + x \\cos x$ por producto.",
               "es_resultado": False},
              {"accion_md": "**L'Hôpital de nuevo:** $\\dfrac{\\sin x}{2 \\cos x - x \\sin x}$. Sustitución: $\\dfrac{0}{2} = 0$.",
               "justificacion_md": "Numerador: $(1 - \\cos x)' = \\sin x$. Denominador: $(\\sin x + x \\cos x)' = \\cos x + \\cos x - x \\sin x = 2\\cos x - x \\sin x$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica las hipótesis y la aplicación:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuándo NO se puede aplicar L'Hôpital?",
                  "opciones_md": [
                      "Cuando la indeterminación es $0/0$.",
                      "Cuando la indeterminación es $\\infty/\\infty$.",
                      "Cuando no hay indeterminación, o cuando ya se resolvió.",
                      "Cuando aparecen funciones trigonométricas.",
                  ],
                  "correcta": "C",
                  "explicacion_md": (
                      "L'Hôpital **solo aplica** a $0/0$ o $\\infty/\\infty$. Aplicarla en $1/0$, por ejemplo, da resultados incorrectos (porque no es indeterminación: el límite ya está determinado)."
                  ),
              },
              {
                  "enunciado_md": "$\\lim_{x \\to \\infty} \\dfrac{\\ln x}{x}$ vale:",
                  "opciones_md": ["$0$", "$1$", "$\\infty$", "no existe"],
                  "correcta": "A",
                  "explicacion_md": (
                      "Forma $\\infty/\\infty$. L'Hôpital: $\\dfrac{1/x}{1} = \\dfrac{1}{x} \\to 0$. **Conclusión:** la función polinomial crece más rápido que el logaritmo en el infinito."
                  ),
              },
          ]),

        fig(
            "Diagrama de flujo en formato infografia para resolver limites con la regla de L Hopital. "
            "Caja inicial (teal #06b6d4): 'Sustitucion directa'. Decision: '?Es indeterminado?'. Si no, "
            "FIN. Si si, otra decision: '?Cual forma?'. Tres ramas en ambar #f59e0b: '0/0 o inf/inf' -> "
            "'Aplicar L Hopital: lim f'/g'', '0 . inf' -> 'Reescribir como cociente', '1^inf, 0^0, inf^0' "
            "-> 'Tomar logaritmo: y = lim, ln y = ...'. Cajas redondeadas, fondo blanco. " + STYLE
        ),
        ej(
            "L'Hôpital con forma $0/0$",
            "Calcula $\\displaystyle\\lim_{x \\to 0} \\dfrac{e^x - 1 - x}{x^2}$.",
            [
                "Verifica que el límite es $0/0$. Aplica L'Hôpital una vez y observa si sigue indeterminado.",
                "Si sigue $0/0$, aplica L'Hôpital nuevamente.",
            ],
            "**Sustitución directa:** numerador $= 1 - 1 - 0 = 0$; denominador $= 0$. Forma $0/0$.\n\n**L'Hôpital (1ª vez):** derivamos numerador y denominador por separado:\n\n$$\\lim_{x \\to 0} \\dfrac{(e^x - 1 - x)'}{(x^2)'} = \\lim_{x \\to 0} \\dfrac{e^x - 1}{2x}.$$\n\nSustituyendo: $\\dfrac{0}{0}$, sigue indeterminado.\n\n**L'Hôpital (2ª vez):**\n\n$$\\lim_{x \\to 0} \\dfrac{(e^x - 1)'}{(2x)'} = \\lim_{x \\to 0} \\dfrac{e^x}{2} = \\dfrac{1}{2}.$$\n\n**Resultado:** $\\boxed{\\dfrac{1}{2}}$.",
        ),
        ej(
            "Indeterminación $1^\\infty$ con logaritmo",
            "Calcula $\\displaystyle\\lim_{x \\to \\infty} \\left(1 + \\dfrac{3}{x}\\right)^{x}$.",
            [
                "La forma $1^\\infty$ es indeterminada. Llama $L$ al límite y toma logaritmo.",
                "Reescribe $\\ln L = \\lim x \\ln(1 + 3/x)$ y conviértelo en un cociente $0/0$.",
            ],
            "**Paso 1 — Tomar logaritmo.** Sea $L = \\lim_{x \\to \\infty}(1 + 3/x)^x$. Entonces $\\ln L = \\lim_{x \\to \\infty} x \\ln(1 + 3/x)$.\n\n**Paso 2 — Reescribir como cociente.**\n\n$$\\ln L = \\lim_{x \\to \\infty} \\dfrac{\\ln(1 + 3/x)}{1/x} \\quad (\\text{forma } 0/0).$$\n\n**Paso 3 — L'Hôpital.** Numerador derivado: $\\dfrac{1}{1 + 3/x} \\cdot \\left(-\\dfrac{3}{x^2}\\right) = -\\dfrac{3}{x^2 + 3x}$.\n\nDenominador derivado: $-\\dfrac{1}{x^2}$.\n\n$$\\ln L = \\lim_{x \\to \\infty} \\dfrac{-3/(x^2 + 3x)}{-1/x^2} = \\lim_{x \\to \\infty} \\dfrac{3 x^2}{x^2 + 3x} = 3.$$\n\n**Paso 4 — Despejar $L$.** $L = e^3$.\n\n**Resultado:** $\\boxed{e^3}$.",
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar L'Hôpital sin verificar la indeterminación.** La regla solo aplica si el cociente es $0/0$ o $\\infty/\\infty$. Si no, el resultado puede ser falso.",
              "**Derivar el cociente entero usando regla del cociente** en vez de derivar numerador y denominador por separado. L'Hôpital pide derivadas separadas.",
              "**Olvidar transformar las formas $0 \\cdot \\infty$, $\\infty - \\infty$, $1^\\infty$ a un cociente** antes de aplicar L'Hôpital.",
              "**No tomar logaritmo en formas $1^\\infty, 0^0, \\infty^0$.** Sin esa transformación, son intratables.",
              "**Aplicar L'Hôpital indefinidamente sin reflexión.** A veces la regla no termina (oscila o diverge); en ese caso hay que cambiar de estrategia.",
          ]),

        b("resumen",
          puntos_md=[
              "**L'Hôpital:** $\\lim \\dfrac{f}{g} = \\lim \\dfrac{f'}{g'}$ siempre que sea $\\dfrac{0}{0}$ o $\\dfrac{\\infty}{\\infty}$.",
              "**Otras formas indeterminadas:** $0 \\cdot \\infty$ (reescribir como cociente), $\\infty - \\infty$ (denominador común), $1^\\infty / 0^0 / \\infty^0$ (tomar $\\ln$).",
              "**Hay que verificar la hipótesis** ($0/0$ o $\\infty/\\infty$) **antes** de aplicar la regla.",
              "**Se puede aplicar repetidamente** mientras la indeterminación persista.",
              "**No es la única técnica:** factorización, racionalización, sándwich y series de Taylor son alternativas — y a veces más directas.",
              "**Próxima lección:** funciones hiperbólicas — análogas a las trigonométricas pero construidas con $e^x$.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-10-lhopital",
        "title": "Regla de L'Hôpital",
        "description": "Resolver indeterminaciones $0/0$ e $\\infty/\\infty$ usando derivadas. Otras formas: $0\\cdot\\infty$, $\\infty-\\infty$, $1^\\infty$, $0^0$, $\\infty^0$.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 10,
    }


# =====================================================================
# LECCIÓN 2.11 — Funciones hiperbólicas
# =====================================================================
def lesson_2_11():
    blocks = [
        b("texto", body_md=(
            "Las **funciones hiperbólicas** son los \"primos\" de las trigonométricas, pero construidos a partir de $e^x$ y $e^{-x}$. "
            "Aparecen en la forma de cables colgantes (catenaria), en relatividad especial, y en muchas integrales de aspecto inocente. "
            "Sus derivadas son sorprendentemente parecidas a las de las trigonométricas — con un detalle de signo.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Conocer las definiciones y las identidades fundamentales.\n"
            "- Calcular las derivadas de $\\sinh, \\cosh, \\tanh$ (y sus inversas).\n"
            "- Reconocer su utilidad en problemas de modelado e integración."
        )),

        b("definicion",
          titulo="Definiciones",
          body_md=(
              "$$\\sinh x = \\dfrac{e^x - e^{-x}}{2}, \\qquad \\cosh x = \\dfrac{e^x + e^{-x}}{2}$$\n\n"
              "$$\\tanh x = \\dfrac{\\sinh x}{\\cosh x} = \\dfrac{e^x - e^{-x}}{e^x + e^{-x}}$$\n\n"
              "Análogo: $\\coth, \\text{sech}, \\text{csch}$ como recíprocos. **Pronunciación:** \"sinh\" se lee \"shaine\" o \"seno hiperbólico\"; \"cosh\" se lee \"cosh\" o \"coseno hiperbólico\"."
          )),

        b("intuicion",
          titulo="¿Por qué \"hiperbólicas\"?",
          body_md=(
              "Las trigonométricas $(\\cos t, \\sin t)$ parametrizan la **circunferencia unitaria** $x^2 + y^2 = 1$. "
              "Las hiperbólicas $(\\cosh t, \\sinh t)$ parametrizan la **hipérbola** $x^2 - y^2 = 1$ (la rama derecha).\n\n"
              "De ahí el nombre: misma estructura, distinta geometría."
          )),

        b("definicion",
          titulo="Identidad fundamental",
          body_md=(
              "$$\\cosh^2 x - \\sinh^2 x = 1$$\n\n"
              "Comparable a $\\cos^2 + \\sin^2 = 1$, pero con un **signo cambiado**. Es la consecuencia de que parametrizan la hipérbola $x^2 - y^2 = 1$."
          )),

        b("teorema",
          nombre="Derivadas",
          enunciado_md=(
              "$$(\\sinh x)' = \\cosh x, \\qquad (\\cosh x)' = \\sinh x$$\n\n"
              "$$(\\tanh x)' = \\text{sech}^2 x = \\dfrac{1}{\\cosh^2 x}$$"
          ),
          demostracion_md=(
              "**Para $\\sinh$:**\n\n"
              "$$(\\sinh x)' = \\dfrac{(e^x)' - (e^{-x})'}{2} = \\dfrac{e^x - (-e^{-x})}{2} = \\dfrac{e^x + e^{-x}}{2} = \\cosh x$$\n\n"
              "**Para $\\cosh$:** análogo, $(\\cosh x)' = \\dfrac{e^x - e^{-x}}{2} = \\sinh x$.\n\n"
              "**Para $\\tanh$:** regla del cociente más identidad $\\cosh^2 - \\sinh^2 = 1$:\n\n"
              "$$(\\tanh x)' = \\dfrac{\\cosh^2 x - \\sinh^2 x}{\\cosh^2 x} = \\dfrac{1}{\\cosh^2 x} = \\text{sech}^2 x$$"
          )),

        b("intuicion",
          titulo="Diferencia con las trigonométricas",
          body_md=(
              "**Compara los signos:**\n\n"
              "- $(\\sin x)' = \\cos x$ vs. $(\\sinh x)' = \\cosh x$ ✓\n"
              "- $(\\cos x)' = -\\sin x$ vs. $(\\cosh x)' = \\sinh x$ ❗ (sin signo negativo)\n\n"
              "Las hiperbólicas \"perdieron\" el signo negativo porque la identidad pitagórica también lo perdió ($\\cosh^2 - \\sinh^2 = 1$, no $+$)."
          )),

        b("ejemplo_resuelto",
          titulo="Derivar $f(x) = \\cosh(x^2)$",
          problema_md="Calcular $f'(x)$.",
          pasos=[
              {"accion_md": "**Cadena:** exterior $\\cosh u$ con derivada $\\sinh u$, interior $u = x^2$ con derivada $2x$.\n\n$$f'(x) = \\sinh(x^2) \\cdot 2x = 2x \\sinh(x^2)$$",
               "justificacion_md": "Composición simple. **Sin signo negativo**, a diferencia de la trigonométrica $\\cos$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Derivar $g(x) = \\tanh(\\ln x)$",
          problema_md="Calcular $g'(x)$.",
          pasos=[
              {"accion_md": "**Cadena:** exterior $\\tanh u$ con derivada $\\text{sech}^2 u$, interior $u = \\ln x$ con derivada $1/x$.\n\n$$g'(x) = \\text{sech}^2(\\ln x) \\cdot \\dfrac{1}{x} = \\dfrac{1}{x \\cosh^2(\\ln x)}$$",
               "justificacion_md": "Forma equivalente con $\\cosh^2$ en lugar de $\\text{sech}^2$.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Inversas hiperbólicas y sus derivadas",
          body_md=(
              "$$\\text{arcsinh}\\, x = \\ln(x + \\sqrt{x^2 + 1}), \\qquad x \\in \\mathbb{R}$$\n\n"
              "$$\\text{arccosh}\\, x = \\ln(x + \\sqrt{x^2 - 1}), \\qquad x \\geq 1$$\n\n"
              "$$\\text{arctanh}\\, x = \\dfrac{1}{2} \\ln\\dfrac{1+x}{1-x}, \\qquad |x| < 1$$\n\n"
              "**Derivadas:**\n\n"
              "$$(\\text{arcsinh}\\, x)' = \\dfrac{1}{\\sqrt{x^2+1}}, \\quad (\\text{arccosh}\\, x)' = \\dfrac{1}{\\sqrt{x^2-1}}, \\quad (\\text{arctanh}\\, x)' = \\dfrac{1}{1-x^2}$$"
          )),

        b("ejemplo_resuelto",
          titulo="Verificar $(\\text{arctanh}\\, x)' = \\dfrac{1}{1-x^2}$",
          problema_md="Demostrar la fórmula directamente.",
          pasos=[
              {"accion_md": "Sea $y = \\text{arctanh}\\, x$, equivalente a $\\tanh y = x$ con $y \\in \\mathbb{R}$.",
               "justificacion_md": "Definición de la inversa.",
               "es_resultado": False},
              {"accion_md": "**Derivamos implícitamente:** $\\text{sech}^2 y \\cdot y' = 1 \\implies y' = \\dfrac{1}{\\text{sech}^2 y} = \\cosh^2 y$.",
               "justificacion_md": "$(\\tanh y)' = \\text{sech}^2 y$.",
               "es_resultado": False},
              {"accion_md": "**Expresamos $\\cosh^2 y$ en términos de $x$:** la identidad $\\cosh^2 - \\sinh^2 = 1$ y $\\tanh = \\sinh/\\cosh$ implican $\\cosh^2 y - x^2 \\cosh^2 y = 1$, es decir, $\\cosh^2 y = \\dfrac{1}{1-x^2}$.",
               "justificacion_md": "Manipulación algebraica con la identidad fundamental.",
               "es_resultado": False},
              {"accion_md": "$$y' = \\dfrac{1}{1-x^2}$$",
               "justificacion_md": "Como las inversas trigonométricas, las inversas hiperbólicas tienen derivadas algebraicas — útiles en integración.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo:",
          preguntas=[
              {
                  "enunciado_md": "$(\\sinh(2x))' = ?$",
                  "opciones_md": ["$2 \\cosh(2x)$", "$\\cosh(2x)$", "$-2\\cosh(2x)$", "$2\\sinh(2x)$"],
                  "correcta": "A",
                  "explicacion_md": (
                      "Cadena: $(\\sinh u)' = \\cosh u$ y $u = 2x$ con $u' = 2$. Producto: $\\cosh(2x) \\cdot 2$."
                  ),
              },
              {
                  "enunciado_md": "¿Qué identidad cumplen las hiperbólicas?",
                  "opciones_md": [
                      "$\\sinh^2 x + \\cosh^2 x = 1$",
                      "$\\cosh^2 x - \\sinh^2 x = 1$",
                      "$\\sinh^2 x - \\cosh^2 x = 1$",
                      "$\\sinh^2 x \\cdot \\cosh^2 x = 1$",
                  ],
                  "correcta": "B",
                  "explicacion_md": (
                      "$\\cosh^2 x - \\sinh^2 x = 1$ — análoga a la pitagórica pero con resta. Refleja que $(\\cosh t, \\sinh t)$ parametriza la hipérbola $x^2 - y^2 = 1$."
                  ),
              },
          ]),

        fig(
            "Grafica de las dos funciones hiperbolicas basicas en un mismo plano cartesiano: y = cosh(x) "
            "en teal #06b6d4 (curva tipo cadena, simetrica, con minimo en (0,1)) y y = sinh(x) en ambar "
            "#f59e0b (curva impar que pasa por el origen). Ejes con flechas, escala simetrica, etiquetas "
            "claras. Anotacion: 'cosh^2(x) - sinh^2(x) = 1 (identidad fundamental)'. Linea punteada "
            "horizontal y=1 marcando el minimo de cosh. Fondo blanco, estilo educativo. " + STYLE
        ),
        ej(
            "Derivar una función hiperbólica compuesta",
            "Calcula $f'(x)$ para $f(x) = \\sinh(x^2 + 1) + \\cosh^2 x$.",
            [
                "Aplica regla de la cadena: $(\\sinh u)' = \\cosh(u) \\cdot u'$ y $(\\cosh u)' = \\sinh(u) \\cdot u'$.",
                "Para $\\cosh^2 x = (\\cosh x)^2$, combina potencia y cadena.",
            ],
            "**Primer término:** $\\sinh(x^2 + 1)$. Cadena: $\\cosh(x^2 + 1) \\cdot 2x$.\n\n**Segundo término:** $\\cosh^2 x = (\\cosh x)^2$. Potencia + cadena: $2 \\cosh x \\cdot \\sinh x$.\n\n(Por identidad: $2 \\cosh x \\sinh x = \\sinh(2x)$.)\n\n**Resultado:**\n\n$$f'(x) = 2x \\cosh(x^2 + 1) + \\sinh(2x).$$",
        ),
        ej(
            "Verificar la identidad fundamental por derivación",
            "Demuestra usando derivadas que la función $g(x) = \\cosh^2 x - \\sinh^2 x$ es **constante** en $\\mathbb{R}$.",
            [
                "Calcula $g'(x)$ aplicando la regla de la cadena en cada término.",
                "Si $g'(x) = 0$ para todo $x$, $g$ es constante; evalúa en $x = 0$ para identificar el valor.",
            ],
            "**Paso 1 — Derivar.**\n\n$g'(x) = 2 \\cosh x \\cdot (\\cosh x)' - 2 \\sinh x \\cdot (\\sinh x)' = 2 \\cosh x \\sinh x - 2 \\sinh x \\cosh x = 0.$\n\n**Paso 2 — Conclusión.** Como $g'(x) = 0$ para todo $x \\in \\mathbb{R}$, $g$ es constante.\n\n**Paso 3 — Identificar la constante.** Evaluamos en $x = 0$: $g(0) = \\cosh^2(0) - \\sinh^2(0) = 1^2 - 0^2 = 1$.\n\n**Conclusión:** $\\cosh^2 x - \\sinh^2 x = 1$ para todo $x$, la identidad fundamental hiperbólica. $\\square$",
        ),

        b("errores_comunes",
          items_md=[
              "**Poner signo negativo en $(\\cosh x)'$.** A diferencia de $(\\cos x)' = -\\sin x$, $(\\cosh x)' = +\\sinh x$. Sin signo negativo.",
              "**Confundir $\\sinh^2 + \\cosh^2$ con $\\cosh^2 - \\sinh^2$.** La identidad correcta es la **diferencia**, no la suma.",
              "**Pensar que $\\text{sech} = 1/\\sin h$.** Es $\\text{sech} = 1/\\cosh$ (recíproco de coseno hiperbólico). Análogo a $\\sec = 1/\\cos$.",
              "**Olvidar el dominio de $\\text{arccosh}$.** Está definido solo para $x \\geq 1$. Las otras inversas tienen dominios distintos también.",
          ]),

        b("resumen",
          puntos_md=[
              "**Definiciones:** $\\sinh x = (e^x - e^{-x})/2$, $\\cosh x = (e^x + e^{-x})/2$, $\\tanh x = \\sinh x / \\cosh x$.",
              "**Identidad fundamental:** $\\cosh^2 x - \\sinh^2 x = 1$ (atención al signo).",
              "**Derivadas:** $(\\sinh)' = \\cosh$, $(\\cosh)' = \\sinh$ (sin signo negativo), $(\\tanh)' = \\text{sech}^2$.",
              "**Inversas:** $\\text{arcsinh}, \\text{arccosh}, \\text{arctanh}$ con derivadas algebraicas.",
              "**Aplicaciones:** catenaria (cable colgante), relatividad especial, integración (sustituciones hiperbólicas).",
              "**Capítulo siguiente:** aplicaciones de la derivada — razones relacionadas, optimización, gráficas, etc.",
          ]),
    ]
    return {
        "id": "lec-derivadas-2-11-hiperbolicas",
        "title": "Funciones hiperbólicas",
        "description": "Definición de $\\sinh, \\cosh, \\tanh$, identidades, derivadas y sus inversas.",
        "blocks": blocks,
        "duration_minutes": 40,
        "order": 11,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "calculo-diferencial"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Course {course_id} not found.")

    # ---- Asegurar el capítulo de Derivadas con la metadata correcta ----
    chapter_id = "ch-derivadas"
    chapter_data = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Derivadas",
        "description": "Definición, derivabilidad, reglas, regla de la cadena, derivación implícita y logarítmica, inversas, exponenciales/logaritmos, L'Hôpital y funciones hiperbólicas.",
        "order": 2,
    }
    existing = await db.chapters.find_one({"id": chapter_id})
    if existing:
        await db.chapters.update_one({"id": chapter_id}, {"$set": chapter_data})
        print(f"✓ Capítulo actualizado: {chapter_data['title']}")
    else:
        chapter_data["created_at"] = now()
        await db.chapters.insert_one(chapter_data)
        print(f"✓ Capítulo creado: {chapter_data['title']}")

    # ---- Verificar la lección 2.1 (preservar) ----
    lesson_2_1 = await db.lessons.find_one({"id": "lesson-definicion-y-notacion"})
    if lesson_2_1:
        # Asegurar que tenga el chapter_id y order=1 correctos
        await db.lessons.update_one(
            {"id": "lesson-definicion-y-notacion"},
            {"$set": {"chapter_id": chapter_id, "order": 1}}
        )
        print(f"✓ Lección 2.1 preservada: {lesson_2_1.get('title', '?')}")
    else:
        print("⚠ Lección 2.1 (lesson-definicion-y-notacion) NO encontrada — corre primero seed_lesson_definicion_derivada.py")

    # ---- Insertar/reemplazar lecciones 2.2..2.11 ----
    builders = [
        lesson_2_2, lesson_2_3, lesson_2_4, lesson_2_5, lesson_2_6,
        lesson_2_7, lesson_2_8, lesson_2_9, lesson_2_10, lesson_2_11,
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
    print(f"✅ Total nuevas: 10 lecciones, {total_blocks} bloques. Capítulo 2 listo.")
    print()
    print("Lecciones disponibles en:")
    print(f"  http://localhost:3007/lesson/lesson-definicion-y-notacion  (preservada)")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
