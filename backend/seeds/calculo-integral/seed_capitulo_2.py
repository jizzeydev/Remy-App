"""
Seed del curso Cálculo Integral — Capítulo 2: Métodos de Integración.
7 lecciones:
  2.1 Sustitución simple (u-substitution)
  2.2 Integración por partes
  2.3 Integrales trigonométricas
  2.4 Sustitución trigonométrica
  2.5 División polinomial
  2.6 Fracciones parciales
  2.7 Integrales impropias

Sin Desmos ni figuras (capítulo puramente algebraico).
Idempotente: borra y re-inserta el capítulo y sus lecciones.
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
    "Estilo: diagrama educativo limpio, fondo blanco, líneas claras, etiquetas en español, "
    "notación matemática con buena tipografía. Acentos teal #06b6d4 y ámbar #f59e0b. "
    "Sin sombras dramáticas, sin texturas. Apto para libro universitario."
)


# =====================================================================
# 2.1 Sustitución simple
# =====================================================================
def lesson_2_1():
    blocks = [
        b("texto", body_md=(
            "La **sustitución simple** (también llamada $u$-sustitución) es la primera técnica de integración "
            "más allá de la tabla básica. Es el **inverso de la regla de la cadena**: si la cadena dice "
            "que $\\dfrac{d}{dx}[F(g(x))] = F'(g(x)) g'(x)$, integrando volvemos atrás.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Reconocer cuándo aplicar sustitución simple (presencia de **función + su derivada** en el integrando).\n"
            "- Aplicar el método paso a paso: elegir $u$, calcular $du$, sustituir.\n"
            "- Manejar el caso de **integral definida**: cambiar también los límites."
        )),

        b("intuicion",
          titulo="¿Cuándo es sustitución?",
          body_md=(
              "Si en el integrando ves una función compuesta $F(g(x))$ multiplicada por algo proporcional a $g'(x)$, "
              "es candidato a sustitución. Ejemplos típicos:\n\n"
              "- $\\int 2x \\cos(x^2) \\, dx$: aparece $x^2$ y $2x$ (su derivada).\n"
              "- $\\int \\dfrac{x}{x^2 + 1} \\, dx$: aparece $x^2 + 1$ y $x$ (proporcional a su derivada $2x$).\n"
              "- $\\int \\sin x \\cos x \\, dx$: aparece $\\sin x$ y $\\cos x$ (su derivada).\n\n"
              "**Idea:** si elegimos $u = g(x)$, entonces $du = g'(x) \\, dx$ — y el integrando se convierte en algo en $u$."
          )),

        b("definicion",
          titulo="Método de sustitución",
          body_md=(
              "Para $\\int f(g(x)) g'(x) \\, dx$:\n\n"
              "**1. Elegir** $u = g(x)$.\n\n"
              "**2. Calcular** $du = g'(x) \\, dx$.\n\n"
              "**3. Sustituir**: la integral se reescribe como $\\int f(u) \\, du$.\n\n"
              "**4. Integrar** en $u$.\n\n"
              "**5. Volver a $x$** sustituyendo $u = g(x)$.\n\n"
              "**Justificación formal:** si $F$ es antiderivada de $f$, por la regla de la cadena "
              "$\\dfrac{d}{dx}[F(g(x))] = F'(g(x)) g'(x) = f(g(x)) g'(x)$. "
              "Entonces $\\int f(g(x)) g'(x) \\, dx = F(g(x)) + C$."
          )),

        b("ejemplo_resuelto",
          titulo="Caso clásico: $\\int 2x \\cos(x^2) \\, dx$",
          problema_md="Calcular la integral.",
          pasos=[
              {"accion_md": "**Elegir $u$:** $u = x^2$. **Calcular $du$:** $du = 2x \\, dx$.",
               "justificacion_md": "Vemos $x^2$ adentro de $\\cos$ y $2x$ multiplicando — exactamente $du$.",
               "es_resultado": False},
              {"accion_md": "**Sustituir:** la integral se vuelve $\\int \\cos u \\, du$.",
               "justificacion_md": "Reemplazamos $x^2 \\to u$ y $2x \\, dx \\to du$.",
               "es_resultado": False},
              {"accion_md": "**Integrar:** $\\int \\cos u \\, du = \\sin u + C$.",
               "justificacion_md": "Tabla básica.",
               "es_resultado": False},
              {"accion_md": "**Volver a $x$:** $\\sin(x^2) + C$.",
               "justificacion_md": "**Verificación:** $\\dfrac{d}{dx}[\\sin(x^2)] = \\cos(x^2) \\cdot 2x$. ✓",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Ajustando una constante: $\\int x \\, e^{x^2} \\, dx$",
          problema_md="Calcular la integral.",
          pasos=[
              {"accion_md": "**Elegir $u$:** $u = x^2$. $du = 2x \\, dx$, así $x \\, dx = \\dfrac{1}{2} du$.",
               "justificacion_md": "El integrando tiene $x \\, dx$ pero $du = 2x \\, dx$ — falta un factor $1/2$ que ajustamos.",
               "es_resultado": False},
              {"accion_md": "**Sustituir:** $\\int e^u \\cdot \\dfrac{1}{2} du = \\dfrac{1}{2} \\int e^u \\, du = \\dfrac{1}{2} e^u + C$.",
               "justificacion_md": "La constante $1/2$ se saca afuera.",
               "es_resultado": False},
              {"accion_md": "**Volver a $x$:** $\\dfrac{1}{2} e^{x^2} + C$.",
               "justificacion_md": "**Patrón general:** si falta una constante multiplicativa para que $du$ encaje, se compensa con la inversa adelante de la integral.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Sustitución en integral definida: $\\int_0^1 \\dfrac{x}{x^2 + 1} \\, dx$",
          problema_md="Calcular la integral, **cambiando también los límites**.",
          pasos=[
              {"accion_md": "**Elegir $u$:** $u = x^2 + 1$, $du = 2x \\, dx$, $x \\, dx = du/2$.",
               "justificacion_md": "El denominador es candidato natural a $u$.",
               "es_resultado": False},
              {"accion_md": "**Cambiar los límites:** cuando $x = 0$, $u = 1$. Cuando $x = 1$, $u = 2$.",
               "justificacion_md": "**Importante:** al sustituir en una definida, los límites también cambian. Así no hace falta volver a $x$ al final.",
               "es_resultado": False},
              {"accion_md": "**Integral en $u$:** $\\dfrac{1}{2} \\int_1^2 \\dfrac{1}{u} \\, du = \\dfrac{1}{2} [\\ln u]_1^2 = \\dfrac{1}{2}(\\ln 2 - \\ln 1) = \\dfrac{\\ln 2}{2}$.",
               "justificacion_md": "Tabla básica $\\int 1/u \\, du = \\ln|u|$. Como $u > 0$ en el intervalo, no necesitamos valor absoluto.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Sustituciones útiles para reconocer",
          body_md=(
              "| Forma del integrando | Sustitución | $du$ |\n|---|---|---|\n"
              "| $f(ax + b)$ | $u = ax + b$ | $du = a \\, dx$ |\n"
              "| $f(x^n) \\cdot x^{n-1}$ | $u = x^n$ | $du = n x^{n-1} dx$ |\n"
              "| $f(\\sin x) \\cos x$ | $u = \\sin x$ | $du = \\cos x \\, dx$ |\n"
              "| $f(\\ln x) / x$ | $u = \\ln x$ | $du = dx/x$ |\n"
              "| $f(e^x) \\cdot e^x$ | $u = e^x$ | $du = e^x \\, dx$ |\n"
              "| $f(\\arctan x) / (1+x^2)$ | $u = \\arctan x$ | $du = dx/(1+x^2)$ |\n\n"
              "**Patrón:** identifica una función \"de adentro\" cuya derivada (salvo constante) aparezca en el integrando."
          )),

        b("verificacion",
          intro_md="Verifica el método:",
          preguntas=[
              {
                  "enunciado_md": "Para $\\int (x^3 + 1)^5 \\cdot 3x^2 \\, dx$, la sustitución natural es:",
                  "opciones_md": [
                      "$u = x^3$",
                      "$u = x^3 + 1$",
                      "$u = 3x^2$",
                      "$u = x$",
                  ],
                  "correcta": "B",
                  "pista_md": "Busca la función \"de adentro\" cuya derivada esté multiplicando.",
                  "explicacion_md": (
                      "$u = x^3 + 1 \\implies du = 3x^2 \\, dx$, justo lo que aparece. La integral se vuelve $\\int u^5 \\, du = u^6/6 + C$."
                  ),
              },
              {
                  "enunciado_md": "Al hacer $u$-sustitución en una **integral definida**, ¿qué hay que recordar?",
                  "opciones_md": [
                      "Volver a la variable $x$ antes de evaluar.",
                      "Cambiar los límites a la nueva variable $u$.",
                      "Mantener los límites en $x$.",
                      "Es lo mismo que en la indefinida.",
                  ],
                  "correcta": "B",
                  "pista_md": "Si los límites están en $x$ pero la antiderivada está en $u$, hay un desajuste. ¿Cómo lo arreglas?",
                  "explicacion_md": (
                      "**Dos opciones equivalentes:** (a) cambiar los límites según $u = g(x)$ y evaluar la antiderivada en $u$, o (b) volver a $x$ al final y evaluar entre los límites originales. Cambiar límites suele ser más rápido."
                  ),
              },
          ]),

        ej(
            titulo="Sustitución con seno y coseno",
            enunciado="Calcula $\\int \\sin^4 x \\cos x \\, dx$.",
            pistas=[
                "$u = \\sin x$ es candidato natural — $du = \\cos x \\, dx$ está disponible.",
                "Después de sustituir, integra una potencia de $u$.",
            ],
            solucion=(
                "$u = \\sin x$, $du = \\cos x \\, dx$. La integral:\n\n"
                "$$\\int u^4 \\, du = \\dfrac{u^5}{5} + C = \\dfrac{\\sin^5 x}{5} + C$$"
            ),
        ),

        ej(
            titulo="Logaritmo escondido",
            enunciado="Calcula $\\int \\dfrac{\\ln x}{x} \\, dx$.",
            pistas=[
                "$u = \\ln x \\implies du = dx/x$.",
                "El factor $1/x$ ya está separado en el integrando.",
            ],
            solucion=(
                "$u = \\ln x$, $du = \\dfrac{dx}{x}$. La integral:\n\n"
                "$$\\int u \\, du = \\dfrac{u^2}{2} + C = \\dfrac{(\\ln x)^2}{2} + C$$"
            ),
        ),

        fig(
            "Diagrama dividido en dos paneles lado a lado conectados por una flecha curva. Panel izquierdo titulado 'En x': integral ∫ f(g(x)) g'(x) dx con la sub-expresión g(x) destacada con un recuadro ámbar #f59e0b. Panel derecho titulado 'En u': integral resultante ∫ f(u) du, más simple, encerrada en un recuadro teal #06b6d4. Entre ambos, flecha curva con la leyenda 'u = g(x), du = g'(x) dx'. Estilo de pizarrón didáctico con tipografía matemática clara."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar volver a $x$** al final de una indefinida. La respuesta debe estar en términos de la variable original.",
              "**No cambiar los límites** en una integral definida después de sustituir. Si dejas los límites en $x$ pero evalúas en $u$, el resultado está mal.",
              "**Sustituir cuando no aplica.** Si no aparece $g'(x)$ (o un múltiplo constante de él), la sustitución directa falla. Buscar otro método.",
              "**Confundir $du$ con $dx$.** $du$ tiene un factor $g'(x)$ que hay que respetar; no es solo un cambio de letra.",
              "**Olvidar la constante** al ajustar: si $du = 2x \\, dx$ y el integrando tiene $x \\, dx$, hay que multiplicar por $1/2$, no ignorar.",
          ]),

        b("resumen",
          puntos_md=[
              "**Sustitución simple = inverso de la regla de la cadena.**",
              "**Pasos:** elegir $u = g(x)$ → calcular $du = g'(x) dx$ → sustituir → integrar en $u$ → volver a $x$ (o cambiar límites en definida).",
              "**Cuándo aplicar:** integrando = función de $g(x)$ multiplicada por algo proporcional a $g'(x)$.",
              "**Definida:** cambiar también los límites $a \\to g(a)$, $b \\to g(b)$.",
              "**Próxima lección:** integración por partes — para productos donde la sustitución no alcanza.",
          ]),
    ]
    return {
        "id": "lec-metodos-2-1-sustitucion",
        "title": "Sustitución simple",
        "description": "Método de u-sustitución como inverso de la regla de la cadena. Caso indefinido y definido.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 1,
    }


# =====================================================================
# 2.2 Integración por partes
# =====================================================================
def lesson_2_2():
    blocks = [
        b("texto", body_md=(
            "Cuando el integrando es un **producto** de funciones que no encaja en sustitución, "
            "la herramienta es la **integración por partes**. Es el inverso de la regla del producto.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar la fórmula $\\int u \\, dv = uv - \\int v \\, du$.\n"
            "- Usar la **estrategia LIATE** para elegir $u$.\n"
            "- Resolver casos clásicos: $\\int \\ln x \\, dx$, $\\int x e^x \\, dx$, $\\int e^x \\sin x \\, dx$.\n"
            "- Aplicar partes **varias veces** y reconocer el caso recursivo."
        )),

        b("intuicion",
          titulo="De la regla del producto",
          body_md=(
              "La regla del producto dice $(uv)' = u'v + uv'$. Integrando ambos lados:\n\n"
              "$$uv = \\int u'v \\, dx + \\int u v' \\, dx$$\n\n"
              "Reordenando:\n\n"
              "$$\\int u v' \\, dx = uv - \\int u' v \\, dx$$\n\n"
              "Que en notación diferencial es $\\int u \\, dv = uv - \\int v \\, du$. Esa es la fórmula de **integración por partes**."
          )),

        b("teorema",
          nombre="Integración por partes",
          enunciado_md=(
              "Si $u$ y $v$ son funciones derivables:\n\n"
              "$$\\int u \\, dv = uv - \\int v \\, du$$\n\n"
              "**En la versión definida:**\n\n"
              "$$\\int_a^b u \\, dv = [uv]_a^b - \\int_a^b v \\, du$$"
          ),
          demostracion_md=(
              "Por la regla del producto $(uv)' = u'v + uv'$. Integrando:\n\n"
              "$$uv = \\int (uv)' \\, dx = \\int u'v \\, dx + \\int uv' \\, dx$$\n\n"
              "Despejando: $\\int uv' \\, dx = uv - \\int u'v \\, dx$, equivalente a $\\int u \\, dv = uv - \\int v \\, du$."
          )),

        b("definicion",
          titulo="Estrategia LIATE para elegir $u$",
          body_md=(
              "El éxito del método depende de **elegir $u$ y $dv$ acertadamente**. "
              "La regla mnemotécnica **LIATE** prioriza qué función llamar $u$ (en orden de preferencia):\n\n"
              "**L** — Logarítmicas ($\\ln x$, $\\log_a x$).\n\n"
              "**I** — Inversas trigonométricas ($\\arcsin x$, $\\arctan x$, ...).\n\n"
              "**A** — Algebraicas (polinomios, raíces).\n\n"
              "**T** — Trigonométricas ($\\sin x$, $\\cos x$, ...).\n\n"
              "**E** — Exponenciales ($e^x$, $a^x$).\n\n"
              "La función que aparezca **primera** en LIATE es buena candidata a $u$; la otra a $dv$.\n\n"
              "**Por qué:** queremos que $du$ (la derivada de $u$) sea **más simple** y que $v$ (antiderivada de $dv$) sea **manejable**."
          )),

        b("ejemplo_resuelto",
          titulo="Algebraico × Exponencial: $\\int x e^x \\, dx$",
          problema_md="Calcular usando partes.",
          pasos=[
              {"accion_md": "**LIATE:** Algebraico ($x$) gana sobre Exponencial ($e^x$). Elegimos $u = x$, $dv = e^x \\, dx$.",
               "justificacion_md": "$u$ se simplifica al derivar (quedará $1$); $dv$ se integra fácil.",
               "es_resultado": False},
              {"accion_md": "**Calculamos:** $du = dx$, $v = \\int e^x \\, dx = e^x$.",
               "justificacion_md": "Las cuatro piezas listas.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos la fórmula:**\n\n$$\\int x e^x \\, dx = uv - \\int v \\, du = x e^x - \\int e^x \\, dx = x e^x - e^x + C$$",
               "justificacion_md": "El segundo integral es trivial.",
               "es_resultado": False},
              {"accion_md": "$\\int x e^x \\, dx = e^x(x - 1) + C$.",
               "justificacion_md": "**Verificación:** $\\dfrac{d}{dx}[e^x(x-1)] = e^x(x-1) + e^x = e^x \\cdot x$. ✓",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Truco con $\\int \\ln x \\, dx$",
          problema_md="Calcular $\\int \\ln x \\, dx$.",
          pasos=[
              {"accion_md": "Solo hay un factor visible ($\\ln x$), pero podemos escribir $\\ln x = \\ln x \\cdot 1$ y aplicar partes con $u = \\ln x$, $dv = dx$.",
               "justificacion_md": "**LIATE:** Logaritmo es la primera prioridad. $dv = dx$ porque no queda otra cosa.",
               "es_resultado": False},
              {"accion_md": "**Calculamos:** $du = \\dfrac{1}{x} dx$, $v = x$.",
               "justificacion_md": "$\\int dx = x$.",
               "es_resultado": False},
              {"accion_md": "**Aplicamos:**\n\n$$\\int \\ln x \\, dx = x \\ln x - \\int x \\cdot \\dfrac{1}{x} \\, dx = x \\ln x - \\int 1 \\, dx = x \\ln x - x + C$$",
               "justificacion_md": "**Patrón clásico:** mismo truco funciona para $\\arcsin x$, $\\arctan x$, etc.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Aplicar partes varias veces: $\\int x^2 \\sin x \\, dx$",
          problema_md="Calcular.",
          pasos=[
              {"accion_md": "**Primera vez:** $u = x^2$ (algebraico), $dv = \\sin x \\, dx$. Entonces $du = 2x \\, dx$, $v = -\\cos x$.\n\n"
                            "$$\\int x^2 \\sin x \\, dx = -x^2 \\cos x + 2 \\int x \\cos x \\, dx$$",
               "justificacion_md": "Reduce el grado de $x^2$ a $x$. Buen progreso.",
               "es_resultado": False},
              {"accion_md": "**Segunda vez** sobre $\\int x \\cos x \\, dx$: $u = x$, $dv = \\cos x \\, dx$. $du = dx$, $v = \\sin x$.\n\n"
                            "$$\\int x \\cos x \\, dx = x \\sin x - \\int \\sin x \\, dx = x \\sin x + \\cos x + C$$",
               "justificacion_md": "Ahora $u$ se redujo a constante.",
               "es_resultado": False},
              {"accion_md": "**Sustituimos:**\n\n$$\\int x^2 \\sin x \\, dx = -x^2 \\cos x + 2(x \\sin x + \\cos x) + C = -x^2 \\cos x + 2x \\sin x + 2 \\cos x + C$$",
               "justificacion_md": "**Tabular:** cuando hay polinomio × (sin/cos/exp), aplicar partes tantas veces como el grado del polinomio.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caso recursivo: $\\int e^x \\sin x \\, dx$",
          problema_md="Calcular.",
          pasos=[
              {"accion_md": "**Primera partes:** $u = \\sin x$, $dv = e^x \\, dx$. $du = \\cos x \\, dx$, $v = e^x$.\n\n"
                            "$$I = \\int e^x \\sin x \\, dx = e^x \\sin x - \\int e^x \\cos x \\, dx$$",
               "justificacion_md": "Llamamos $I$ al integral original para referencia.",
               "es_resultado": False},
              {"accion_md": "**Segunda partes** sobre $\\int e^x \\cos x \\, dx$: $u = \\cos x$, $dv = e^x dx$. $du = -\\sin x \\, dx$, $v = e^x$.\n\n"
                            "$$\\int e^x \\cos x \\, dx = e^x \\cos x + \\int e^x \\sin x \\, dx = e^x \\cos x + I$$",
               "justificacion_md": "**¡Reaparece $I$!** Pero no es un loop sin salida: vamos a despejar.",
               "es_resultado": False},
              {"accion_md": "**Sustituimos en la primera ecuación:**\n\n$$I = e^x \\sin x - (e^x \\cos x + I) = e^x \\sin x - e^x \\cos x - I$$\n\n"
                            "$$2I = e^x(\\sin x - \\cos x) \\implies I = \\dfrac{e^x(\\sin x - \\cos x)}{2} + C$$",
               "justificacion_md": "**Truco clave:** cuando el integral original reaparece después de aplicar partes, **se despeja** algebraicamente.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el método:",
          preguntas=[
              {
                  "enunciado_md": "Para $\\int x \\arctan x \\, dx$, ¿qué eliges como $u$?",
                  "opciones_md": [
                      "$u = x$",
                      "$u = \\arctan x$",
                      "Cualquiera, da lo mismo.",
                      "Ninguna funciona.",
                  ],
                  "correcta": "B",
                  "pista_md": "LIATE: Inversa trigonométrica gana sobre Algebraica.",
                  "explicacion_md": (
                      "**LIATE:** I (Inversa trig) gana sobre A (Algebraica). $u = \\arctan x$ con $du = \\dfrac{dx}{1+x^2}$. "
                      "Si eligieras $u = x$, $v = -1/(1+x^2)\\cdot \\ldots$ — más complicado."
                  ),
              },
              {
                  "enunciado_md": "Si después de aplicar partes el integrando reaparece igual al original, ¿qué hacer?",
                  "opciones_md": [
                      "Aplicar partes una vez más, indefinidamente.",
                      "Despejar la integral algebraicamente: pasar al lado izquierdo.",
                      "Es señal de error: revisar.",
                      "Cambiar de método.",
                  ],
                  "correcta": "B",
                  "pista_md": "Es el caso recursivo de $\\int e^x \\sin x \\, dx$. Después del segundo partes aparece $I$ del lado derecho.",
                  "explicacion_md": (
                      "Es el caso clásico recursivo. Llamando $I$ al integral, después de partes obtienes $I = (\\text{algo}) + cI$. **Despejas $I$**."
                  ),
              },
          ]),

        ej(
            titulo="Logaritmo simple",
            enunciado="Calcula $\\int x \\ln x \\, dx$.",
            pistas=[
                "LIATE: L gana sobre A. $u = \\ln x$, $dv = x \\, dx$.",
                "Vas a obtener $v = x^2/2$.",
            ],
            solucion=(
                "$u = \\ln x$, $du = dx/x$. $dv = x \\, dx$, $v = x^2/2$.\n\n"
                "$$\\int x \\ln x \\, dx = \\dfrac{x^2}{2} \\ln x - \\int \\dfrac{x^2}{2} \\cdot \\dfrac{1}{x} \\, dx = \\dfrac{x^2 \\ln x}{2} - \\dfrac{1}{2} \\int x \\, dx = \\dfrac{x^2 \\ln x}{2} - \\dfrac{x^2}{4} + C$$"
            ),
        ),

        ej(
            titulo="Inversa trigonométrica",
            enunciado="Calcula $\\int \\arctan x \\, dx$.",
            pistas=[
                "Truco del 1: $\\arctan x = \\arctan x \\cdot 1$.",
                "$u = \\arctan x$, $dv = dx$. Después necesitarás $\\int \\dfrac{x}{1+x^2} \\, dx$ — sustitución.",
            ],
            solucion=(
                "$u = \\arctan x$, $du = \\dfrac{dx}{1+x^2}$. $v = x$.\n\n"
                "$$\\int \\arctan x \\, dx = x \\arctan x - \\int \\dfrac{x}{1+x^2} \\, dx$$\n\n"
                "**El segundo integral por sustitución** ($w = 1 + x^2$, $dw = 2x \\, dx$):\n\n"
                "$$\\int \\dfrac{x}{1+x^2} \\, dx = \\dfrac{1}{2} \\int \\dfrac{dw}{w} = \\dfrac{1}{2} \\ln(1+x^2)$$\n\n"
                "**Resultado final:** $\\int \\arctan x \\, dx = x \\arctan x - \\dfrac{1}{2} \\ln(1+x^2) + C$."
            ),
        ),

        fig(
            "Lámina con la fórmula grande y centrada ∫ u dv = uv − ∫ v du en color teal #06b6d4. A la izquierda, una tabla DI (Derivar / Integrar) con dos columnas: columna D con u, u', u'' y columna I con dv, v, ∫v. A la derecha un ejemplo aplicado al integrar ∫ x e^x dx mostrando u = x, dv = e^x dx. Flechas curvas ámbar #f59e0b conectan las celdas de la tabla con los términos correspondientes de la fórmula y del ejemplo."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Elegir $u$ y $dv$ al revés.** Si $du$ se vuelve más complicado que $u$, o si no sabes integrar $dv$, elegiste mal. LIATE ayuda.",
              "**Olvidar el signo en $\\int v \\, du$.** La fórmula es $uv - \\int v \\, du$, no $uv + \\int v \\, du$.",
              "**No reconocer el caso recursivo.** Si el integral reaparece, despeja — no apliques partes infinitamente.",
              "**Olvidar la constante** $+C$ al final de la indefinida.",
              "**Aplicar partes cuando sustitución es más simple.** Si en el integrando ves función + su derivada, prueba sustitución primero.",
          ]),

        b("resumen",
          puntos_md=[
              "**Fórmula:** $\\int u \\, dv = uv - \\int v \\, du$.",
              "**LIATE:** orden de prioridad para $u$ → Logarítmica, Inversa trig, Algebraica, Trigonométrica, Exponencial.",
              "**Truco del 1:** $\\int \\ln x \\, dx = \\int \\ln x \\cdot 1 \\, dx$ con $dv = dx$ — funciona también para $\\arctan, \\arcsin$, etc.",
              "**Aplicar varias veces:** polinomio de grado $n$ × (sin/cos/exp) requiere $n$ aplicaciones.",
              "**Caso recursivo:** si el integral original reaparece, **despejar algebraicamente**.",
              "**Próxima lección:** integrales trigonométricas — productos de potencias de seno, coseno, tangente, secante.",
          ]),
    ]
    return {
        "id": "lec-metodos-2-2-partes",
        "title": "Integración por partes",
        "description": "Fórmula $\\int u \\, dv = uv - \\int v \\, du$, estrategia LIATE, casos recursivos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# 2.3 Integrales trigonométricas
# =====================================================================
def lesson_2_3():
    blocks = [
        b("texto", body_md=(
            "Cuando el integrando es un **producto de potencias de funciones trigonométricas**, "
            "hay estrategias específicas según las paridades de los exponentes y las identidades disponibles.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Resolver $\\int \\sin^m x \\cos^n x \\, dx$ según las paridades.\n"
            "- Resolver $\\int \\tan^m x \\sec^n x \\, dx$ análogamente.\n"
            "- Manejar productos $\\sin(ax) \\cos(bx)$ con identidades de producto a suma."
        )),

        b("definicion",
          titulo="Identidades fundamentales",
          body_md=(
              "**Pitagóricas:**\n\n"
              "$$\\sin^2 x + \\cos^2 x = 1, \\quad 1 + \\tan^2 x = \\sec^2 x, \\quad 1 + \\cot^2 x = \\csc^2 x$$\n\n"
              "**Ángulo doble:**\n\n"
              "$$\\sin^2 x = \\dfrac{1 - \\cos(2x)}{2}, \\quad \\cos^2 x = \\dfrac{1 + \\cos(2x)}{2}$$\n\n"
              "$$\\sin(2x) = 2 \\sin x \\cos x$$\n\n"
              "**Producto a suma:**\n\n"
              "$$\\sin A \\cos B = \\dfrac{1}{2}[\\sin(A-B) + \\sin(A+B)]$$\n\n"
              "$$\\sin A \\sin B = \\dfrac{1}{2}[\\cos(A-B) - \\cos(A+B)]$$\n\n"
              "$$\\cos A \\cos B = \\dfrac{1}{2}[\\cos(A-B) + \\cos(A+B)]$$"
          )),

        b("definicion",
          titulo="Estrategia para $\\int \\sin^m x \\cos^n x \\, dx$",
          body_md=(
              "**Caso 1: $m$ impar.** Reservar un $\\sin x$, convertir el resto en $\\cos$ con $\\sin^2 = 1 - \\cos^2$, sustituir $u = \\cos x$.\n\n"
              "**Caso 2: $n$ impar.** Análogo — reservar un $\\cos x$, convertir el resto, $u = \\sin x$.\n\n"
              "**Caso 3: $m, n$ ambos pares.** Usar las identidades de ángulo doble para reducir el grado:\n\n"
              "$\\sin^2 x = (1 - \\cos 2x)/2$, $\\cos^2 x = (1 + \\cos 2x)/2$. Repetir si hace falta."
          )),

        b("ejemplo_resuelto",
          titulo="Caso impar: $\\int \\sin^3 x \\cos^2 x \\, dx$",
          problema_md="Calcular.",
          pasos=[
              {"accion_md": "$m = 3$ (impar). **Separamos un $\\sin x$:** $\\sin^3 x = \\sin^2 x \\cdot \\sin x = (1 - \\cos^2 x) \\sin x$.\n\n"
                            "$$\\int (1 - \\cos^2 x) \\cos^2 x \\sin x \\, dx$$",
               "justificacion_md": "Convertimos $\\sin^2$ en términos de $\\cos$ usando la pitagórica.",
               "es_resultado": False},
              {"accion_md": "**Sustitución:** $u = \\cos x$, $du = -\\sin x \\, dx$, así $\\sin x \\, dx = -du$.\n\n"
                            "$$\\int (1 - u^2) u^2 (-du) = -\\int (u^2 - u^4) \\, du = -\\dfrac{u^3}{3} + \\dfrac{u^5}{5} + C$$",
               "justificacion_md": "La integral queda polinomial en $u$.",
               "es_resultado": False},
              {"accion_md": "**Volver a $x$:**\n\n$$\\int \\sin^3 x \\cos^2 x \\, dx = -\\dfrac{\\cos^3 x}{3} + \\dfrac{\\cos^5 x}{5} + C$$",
               "justificacion_md": "**Patrón:** cuando hay potencia impar de seno o coseno, separar uno y aplicar la pitagórica para el resto.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caso ambos pares: $\\int \\sin^2 x \\cos^2 x \\, dx$",
          problema_md="Calcular.",
          pasos=[
              {"accion_md": "**Identidad de ángulo doble:** $\\sin x \\cos x = \\dfrac{1}{2}\\sin(2x)$, así $\\sin^2 x \\cos^2 x = \\dfrac{1}{4} \\sin^2(2x)$.",
               "justificacion_md": "Reduce un par a un solo término.",
               "es_resultado": False},
              {"accion_md": "**Reducir potencia de $\\sin^2$:** $\\sin^2(2x) = \\dfrac{1 - \\cos(4x)}{2}$.\n\n"
                            "$$\\dfrac{1}{4} \\int \\sin^2(2x) \\, dx = \\dfrac{1}{4} \\int \\dfrac{1 - \\cos(4x)}{2} \\, dx = \\dfrac{1}{8} \\int (1 - \\cos(4x)) \\, dx$$",
               "justificacion_md": "Aplicamos la identidad a $\\sin^2$ con argumento $2x$.",
               "es_resultado": False},
              {"accion_md": "**Integrar:**\n\n$$\\dfrac{1}{8}\\left(x - \\dfrac{\\sin(4x)}{4}\\right) + C = \\dfrac{x}{8} - \\dfrac{\\sin(4x)}{32} + C$$",
               "justificacion_md": "**Patrón:** ambos pares → identidades de ángulo doble, posiblemente repetidas.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Estrategia para $\\int \\tan^m x \\sec^n x \\, dx$",
          body_md=(
              "**Caso 1: $n$ par.** Reservar $\\sec^2 x$, convertir el resto $\\sec^{n-2}$ con $\\sec^2 = 1 + \\tan^2$, sustituir $u = \\tan x$.\n\n"
              "**Caso 2: $m$ impar.** Reservar $\\sec x \\tan x$, convertir el resto $\\tan^{m-1}$ con $\\tan^2 = \\sec^2 - 1$, sustituir $u = \\sec x$.\n\n"
              "**Caso 3: $m$ par, $n$ impar.** Convertir todo a $\\sec$ usando $\\tan^2 = \\sec^2 - 1$ y aplicar fórmulas de reducción o partes."
          )),

        b("ejemplo_resuelto",
          titulo="$\\int \\tan^3 x \\sec^4 x \\, dx$",
          problema_md="Calcular.",
          pasos=[
              {"accion_md": "$n = 4$ (par). **Reservar $\\sec^2 x$:** $\\sec^4 x = \\sec^2 x \\cdot \\sec^2 x = (1 + \\tan^2 x) \\sec^2 x$.\n\n"
                            "$$\\int \\tan^3 x (1 + \\tan^2 x) \\sec^2 x \\, dx$$",
               "justificacion_md": "Convertimos parte de $\\sec^4$ a tangente para preparar la sustitución.",
               "es_resultado": False},
              {"accion_md": "**Sustitución:** $u = \\tan x$, $du = \\sec^2 x \\, dx$.\n\n"
                            "$$\\int u^3 (1 + u^2) \\, du = \\int (u^3 + u^5) \\, du = \\dfrac{u^4}{4} + \\dfrac{u^6}{6} + C$$",
               "justificacion_md": "Polinomial trivial.",
               "es_resultado": False},
              {"accion_md": "$$\\int \\tan^3 x \\sec^4 x \\, dx = \\dfrac{\\tan^4 x}{4} + \\dfrac{\\tan^6 x}{6} + C$$",
               "justificacion_md": "Volver a $x$ y listo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Producto a suma: $\\int \\sin(3x) \\cos(5x) \\, dx$",
          problema_md="Calcular usando identidad producto-a-suma.",
          pasos=[
              {"accion_md": "**Identidad:** $\\sin A \\cos B = \\dfrac{1}{2}[\\sin(A-B) + \\sin(A+B)]$. Con $A = 3x$, $B = 5x$:\n\n"
                            "$$\\sin(3x) \\cos(5x) = \\dfrac{1}{2}[\\sin(-2x) + \\sin(8x)] = \\dfrac{1}{2}[-\\sin(2x) + \\sin(8x)]$$",
               "justificacion_md": "$\\sin(-x) = -\\sin x$.",
               "es_resultado": False},
              {"accion_md": "**Integrar término a término:**\n\n$$\\dfrac{1}{2}\\left[\\dfrac{\\cos(2x)}{2} - \\dfrac{\\cos(8x)}{8}\\right] + C = \\dfrac{\\cos(2x)}{4} - \\dfrac{\\cos(8x)}{16} + C$$",
               "justificacion_md": "$\\int \\sin(kx) \\, dx = -\\cos(kx)/k$. **Lección:** las identidades producto-a-suma convierten productos en sumas, mucho más fáciles de integrar.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica las estrategias:",
          preguntas=[
              {
                  "enunciado_md": "Para $\\int \\sin^4 x \\cos^3 x \\, dx$, la estrategia es:",
                  "opciones_md": [
                      "Reservar $\\sin x$ y sustituir $u = \\cos x$.",
                      "Reservar $\\cos x$ y sustituir $u = \\sin x$.",
                      "Usar $\\sin^2 = (1-\\cos 2x)/2$.",
                      "Integrar por partes.",
                  ],
                  "correcta": "B",
                  "pista_md": "$n = 3$ (impar) en $\\cos$. ¿Qué se reserva?",
                  "explicacion_md": (
                      "$n$ impar → reservar un $\\cos x$, convertir el resto $\\cos^2 = 1 - \\sin^2$, sustituir $u = \\sin x$."
                  ),
              },
              {
                  "enunciado_md": "Para $\\int \\sin^2 x \\, dx$, ¿qué identidad conviene?",
                  "opciones_md": [
                      "$\\sin^2 x = 1 - \\cos^2 x$",
                      "$\\sin^2 x = (1 - \\cos 2x)/2$",
                      "$\\sin^2 x = \\sin x \\cdot \\sin x$",
                      "Ninguna, integrar directo.",
                  ],
                  "correcta": "B",
                  "pista_md": "La pitagórica te deja con otro $\\cos^2$, sin avanzar. La de ángulo doble baja el grado.",
                  "explicacion_md": (
                      "$\\sin^2 x = (1 - \\cos 2x)/2$ permite integrar directamente: $\\int \\sin^2 x \\, dx = x/2 - \\sin(2x)/4 + C$."
                  ),
              },
          ]),

        ej(
            titulo="Caso impar simple",
            enunciado="Calcula $\\int \\cos^3 x \\, dx$.",
            pistas=[
                "$n = 3$ impar. Separa un $\\cos x$ y convierte el resto.",
                "$\\cos^2 x = 1 - \\sin^2 x$. Sustituye $u = \\sin x$.",
            ],
            solucion=(
                "$\\cos^3 x = \\cos^2 x \\cdot \\cos x = (1 - \\sin^2 x) \\cos x$.\n\n"
                "$u = \\sin x$, $du = \\cos x \\, dx$:\n\n"
                "$$\\int (1 - u^2) \\, du = u - \\dfrac{u^3}{3} + C = \\sin x - \\dfrac{\\sin^3 x}{3} + C$$"
            ),
        ),

        ej(
            titulo="Tangente al cuadrado",
            enunciado="Calcula $\\int \\tan^2 x \\, dx$.",
            pistas=[
                "$\\tan^2 x = \\sec^2 x - 1$ (pitagórica).",
                "$\\int \\sec^2 x \\, dx = \\tan x$.",
            ],
            solucion=(
                "$\\tan^2 x = \\sec^2 x - 1$, así\n\n"
                "$$\\int \\tan^2 x \\, dx = \\int \\sec^2 x \\, dx - \\int 1 \\, dx = \\tan x - x + C$$"
            ),
        ),

        fig(
            "Tabla mnemotécnica de tres columnas para ∫ sin^m x cos^n x dx según la paridad de m y n. Columna 1 'm impar': sustitución u = cos x, ejemplo ∫ sin^3 x cos^2 x dx. Columna 2 'n impar': sustitución u = sin x, ejemplo ∫ sin^2 x cos^5 x dx. Columna 3 'ambos pares': identidades de ángulo doble sin²=(1−cos2x)/2. Encabezados en teal #06b6d4 y las sustituciones u = … resaltadas en ámbar #f59e0b."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar la pitagórica cuando ambas potencias son pares.** No avanza: hay que usar ángulo doble.",
              "**Olvidar el signo** al sustituir $u = \\cos x$ ($du = -\\sin x \\, dx$): $\\sin x \\, dx = -du$.",
              "**Confundir las identidades:** $\\sin^2 = (1 - \\cos 2x)/2$ tiene **menos**, $\\cos^2 = (1 + \\cos 2x)/2$ tiene **más**.",
              "**No simplificar antes:** $\\int \\sin^2 x \\cos^2 x \\, dx$ se simplifica con $\\sin x \\cos x = \\sin(2x)/2$ antes de integrar.",
              "**Confundir reducción con sustitución directa.** Para $\\int \\sin x \\cos x \\, dx$, hay 3 caminos válidos: sustitución $u=\\sin x$ ($\\sin^2/2$), $u=\\cos x$ ($-\\cos^2/2$), o ángulo doble ($-\\cos 2x/4$). Difieren en una constante.",
          ]),

        b("resumen",
          puntos_md=[
              "**$\\sin^m \\cos^n$ con uno impar:** reservar uno, convertir el resto con pitagórica, sustituir.",
              "**$\\sin^m \\cos^n$ con ambos pares:** identidades de ángulo doble para bajar grado.",
              "**$\\tan^m \\sec^n$:** elegir entre reservar $\\sec^2$ ($n$ par, $u = \\tan$) o $\\sec \\tan$ ($m$ impar, $u = \\sec$).",
              "**Productos $\\sin(ax)\\cos(bx)$:** identidades producto-a-suma.",
              "**Identidades clave:** $\\sin^2 + \\cos^2 = 1$, $1 + \\tan^2 = \\sec^2$, ángulo doble, producto-a-suma.",
              "**Próxima lección:** sustitución trigonométrica para integrales con $\\sqrt{a^2 \\pm x^2}$ y $\\sqrt{x^2 - a^2}$.",
          ]),
    ]
    return {
        "id": "lec-metodos-2-3-trigonometricas",
        "title": "Integrales trigonométricas",
        "description": "Productos de potencias de funciones trigonométricas. Estrategias por paridad e identidades.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# 2.4 Sustitución trigonométrica
# =====================================================================
def lesson_2_4():
    blocks = [
        b("texto", body_md=(
            "Cuando el integrando contiene una raíz cuadrada de la forma $\\sqrt{a^2 - x^2}$, "
            "$\\sqrt{a^2 + x^2}$ o $\\sqrt{x^2 - a^2}$, la **sustitución trigonométrica** elimina la raíz "
            "usando una identidad pitagórica. Es uno de los trucos más elegantes del cálculo.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Reconocer las tres formas y elegir la sustitución correcta.\n"
            "- Aplicar el método paso a paso (sustitución → simplificar raíz → integrar → volver a $x$).\n"
            "- Manejar el triángulo auxiliar para volver a la variable original."
        )),

        b("definicion",
          titulo="Tabla de sustituciones",
          body_md=(
              "| Expresión en el integrando | Sustitución | Identidad usada | Resultado de la raíz |\n|---|---|---|---|\n"
              "| $\\sqrt{a^2 - x^2}$ | $x = a \\sin\\theta$ | $1 - \\sin^2 = \\cos^2$ | $a\\cos\\theta$ |\n"
              "| $\\sqrt{a^2 + x^2}$ | $x = a \\tan\\theta$ | $1 + \\tan^2 = \\sec^2$ | $a\\sec\\theta$ |\n"
              "| $\\sqrt{x^2 - a^2}$ | $x = a \\sec\\theta$ | $\\sec^2 - 1 = \\tan^2$ | $a\\tan\\theta$ |\n\n"
              "Después de la sustitución la raíz **desaparece** y queda una integral trigonométrica (lección 2.3).\n\n"
              "**Diferenciales asociadas:**\n\n"
              "- $x = a\\sin\\theta \\implies dx = a\\cos\\theta \\, d\\theta$\n"
              "- $x = a\\tan\\theta \\implies dx = a\\sec^2\\theta \\, d\\theta$\n"
              "- $x = a\\sec\\theta \\implies dx = a\\sec\\theta \\tan\\theta \\, d\\theta$"
          )),

        b("intuicion",
          titulo="Por qué funciona",
          body_md=(
              "La pitagórica $\\sin^2 + \\cos^2 = 1$ es una **identidad cuadrática** en una variable angular. "
              "Si tenemos $\\sqrt{a^2 - x^2}$ y sustituimos $x = a\\sin\\theta$:\n\n"
              "$$\\sqrt{a^2 - a^2 \\sin^2\\theta} = \\sqrt{a^2(1 - \\sin^2\\theta)} = \\sqrt{a^2 \\cos^2\\theta} = a|\\cos\\theta|$$\n\n"
              "Eligiendo $\\theta \\in [-\\pi/2, \\pi/2]$ (rango principal de $\\arcsin$), $\\cos\\theta \\geq 0$ y queda $a\\cos\\theta$. **Sin raíz.**"
          )),

        b("ejemplo_resuelto",
          titulo="Forma $\\sqrt{a^2 - x^2}$: $\\int \\sqrt{4 - x^2} \\, dx$",
          problema_md="Calcular usando sustitución trigonométrica.",
          pasos=[
              {"accion_md": "**Sustitución:** $a = 2$, así $x = 2\\sin\\theta$. $dx = 2\\cos\\theta \\, d\\theta$.\n\n"
                            "**Raíz:** $\\sqrt{4 - 4\\sin^2\\theta} = 2\\cos\\theta$ (con $\\theta \\in [-\\pi/2, \\pi/2]$).",
               "justificacion_md": "Aplicamos la sustitución de la primera fila de la tabla.",
               "es_resultado": False},
              {"accion_md": "**Sustituyendo:**\n\n$$\\int 2\\cos\\theta \\cdot 2\\cos\\theta \\, d\\theta = 4 \\int \\cos^2\\theta \\, d\\theta$$",
               "justificacion_md": "El integrando se vuelve trigonométrico puro.",
               "es_resultado": False},
              {"accion_md": "**Identidad ángulo doble:** $\\cos^2\\theta = (1 + \\cos 2\\theta)/2$.\n\n"
                            "$$4 \\int \\dfrac{1 + \\cos 2\\theta}{2} \\, d\\theta = 2\\theta + \\sin 2\\theta + C = 2\\theta + 2\\sin\\theta \\cos\\theta + C$$",
               "justificacion_md": "Usamos $\\sin 2\\theta = 2\\sin\\theta\\cos\\theta$ para preparar el regreso a $x$.",
               "es_resultado": False},
              {"accion_md": "**Volver a $x$:** $\\sin\\theta = x/2$, $\\cos\\theta = \\sqrt{4-x^2}/2$, $\\theta = \\arcsin(x/2)$.\n\n"
                            "$$\\int \\sqrt{4 - x^2} \\, dx = 2\\arcsin(x/2) + 2 \\cdot \\dfrac{x}{2} \\cdot \\dfrac{\\sqrt{4-x^2}}{2} + C = 2\\arcsin(x/2) + \\dfrac{x\\sqrt{4-x^2}}{2} + C$$",
               "justificacion_md": "**Triángulo auxiliar:** $\\sin\\theta = x/2$ → cateto opuesto $x$, hipotenusa $2$, cateto adyacente $\\sqrt{4-x^2}$. De ahí $\\cos\\theta$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Forma $\\sqrt{a^2 + x^2}$: $\\int \\dfrac{1}{\\sqrt{1 + x^2}} \\, dx$",
          problema_md="Calcular.",
          pasos=[
              {"accion_md": "**Sustitución:** $a = 1$, $x = \\tan\\theta$. $dx = \\sec^2\\theta \\, d\\theta$.\n\n"
                            "**Raíz:** $\\sqrt{1 + \\tan^2\\theta} = \\sec\\theta$.",
               "justificacion_md": "Segunda fila de la tabla.",
               "es_resultado": False},
              {"accion_md": "**Sustituyendo:**\n\n$$\\int \\dfrac{1}{\\sec\\theta} \\cdot \\sec^2\\theta \\, d\\theta = \\int \\sec\\theta \\, d\\theta = \\ln|\\sec\\theta + \\tan\\theta| + C$$",
               "justificacion_md": "$\\int \\sec\\theta \\, d\\theta$ es una fórmula clásica que conviene memorizar.",
               "es_resultado": False},
              {"accion_md": "**Volver a $x$:** $\\tan\\theta = x$, $\\sec\\theta = \\sqrt{1 + x^2}$.\n\n"
                            "$$\\int \\dfrac{1}{\\sqrt{1+x^2}} \\, dx = \\ln\\left|\\sqrt{1+x^2} + x\\right| + C$$",
               "justificacion_md": "**Equivalente** a $\\text{arcsinh}\\, x + C$ (la inversa hiperbólica).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Forma $\\sqrt{x^2 - a^2}$: $\\int \\dfrac{\\sqrt{x^2 - 9}}{x} \\, dx$",
          problema_md="Calcular.",
          pasos=[
              {"accion_md": "**Sustitución:** $a = 3$, $x = 3\\sec\\theta$. $dx = 3\\sec\\theta \\tan\\theta \\, d\\theta$.\n\n"
                            "**Raíz:** $\\sqrt{9\\sec^2\\theta - 9} = 3\\tan\\theta$.",
               "justificacion_md": "Tercera fila.",
               "es_resultado": False},
              {"accion_md": "**Sustituyendo:**\n\n$$\\int \\dfrac{3\\tan\\theta}{3\\sec\\theta} \\cdot 3\\sec\\theta\\tan\\theta \\, d\\theta = 3\\int \\tan^2\\theta \\, d\\theta$$",
               "justificacion_md": "$\\sec\\theta$ se cancela.",
               "es_resultado": False},
              {"accion_md": "**$\\tan^2 = \\sec^2 - 1$:**\n\n$$3\\int (\\sec^2\\theta - 1) \\, d\\theta = 3(\\tan\\theta - \\theta) + C$$",
               "justificacion_md": "Visto en lección 2.3.",
               "es_resultado": False},
              {"accion_md": "**Volver a $x$:** $\\sec\\theta = x/3$, $\\tan\\theta = \\sqrt{x^2-9}/3$, $\\theta = \\text{arcsec}(x/3)$.\n\n"
                            "$$\\int \\dfrac{\\sqrt{x^2-9}}{x} \\, dx = \\sqrt{x^2 - 9} - 3\\,\\text{arcsec}(x/3) + C$$",
               "justificacion_md": "**Triángulo:** $\\sec = x/3$ → hipotenusa $x$, adyacente $3$, opuesto $\\sqrt{x^2-9}$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica las elecciones:",
          preguntas=[
              {
                  "enunciado_md": "Para $\\int \\dfrac{1}{x^2 \\sqrt{16 - x^2}} \\, dx$, ¿qué sustitución?",
                  "opciones_md": [
                      "$x = 4\\sin\\theta$",
                      "$x = 4\\tan\\theta$",
                      "$x = 4\\sec\\theta$",
                      "$x = \\sin\\theta$",
                  ],
                  "correcta": "A",
                  "pista_md": "Forma $\\sqrt{a^2 - x^2}$ con $a = 4$.",
                  "explicacion_md": (
                      "Forma $\\sqrt{a^2 - x^2}$ → $x = a\\sin\\theta$. Aquí $a = 4$, así $x = 4\\sin\\theta$."
                  ),
              },
              {
                  "enunciado_md": "¿Qué se simplifica con $x = a\\tan\\theta$?",
                  "opciones_md": [
                      "$\\sqrt{a^2 - x^2}$",
                      "$\\sqrt{a^2 + x^2}$",
                      "$\\sqrt{x^2 - a^2}$",
                      "$\\sqrt{x \\cdot a}$",
                  ],
                  "correcta": "B",
                  "pista_md": "Identidad: $1 + \\tan^2 = \\sec^2$.",
                  "explicacion_md": (
                      "$\\sqrt{a^2 + x^2} = \\sqrt{a^2(1 + \\tan^2\\theta)} = a\\sec\\theta$ con $x = a\\tan\\theta$."
                  ),
              },
          ]),

        ej(
            titulo="Aplicar el método",
            enunciado="Calcula $\\int \\dfrac{1}{\\sqrt{9 - x^2}} \\, dx$.",
            pistas=[
                "Forma $\\sqrt{a^2 - x^2}$ con $a = 3$. Sustituye $x = 3\\sin\\theta$.",
                "La raíz se vuelve $3\\cos\\theta$ y $dx = 3\\cos\\theta \\, d\\theta$.",
                "Después de cancelar, queda $\\int 1 \\, d\\theta$.",
            ],
            solucion=(
                "$x = 3\\sin\\theta$, $dx = 3\\cos\\theta \\, d\\theta$, $\\sqrt{9-x^2} = 3\\cos\\theta$.\n\n"
                "$$\\int \\dfrac{3\\cos\\theta}{3\\cos\\theta} \\, d\\theta = \\int 1 \\, d\\theta = \\theta + C = \\arcsin(x/3) + C$$\n\n"
                "**Resultado clásico** (de la tabla básica de antiderivadas con argumento $x/a$)."
            ),
        ),

        fig(
            "Tres triángulos rectángulos lado a lado, uno por cada caso de sustitución trigonométrica. Triángulo 1: hipotenusa a, cateto opuesto x, cateto adyacente √(a²−x²); etiqueta 'x = a sin θ'. Triángulo 2: cateto opuesto x, cateto adyacente a, hipotenusa √(a²+x²); etiqueta 'x = a tan θ'. Triángulo 3: hipotenusa x, cateto adyacente a, cateto opuesto √(x²−a²); etiqueta 'x = a sec θ'. Lados etiquetados en teal #06b6d4, sustituciones en ámbar #f59e0b. Ángulo θ marcado en cada uno."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Elegir la sustitución equivocada.** Solo memorizar la tabla evita esto: $\\sqrt{a^2 - x^2}$ → seno, $\\sqrt{a^2 + x^2}$ → tangente, $\\sqrt{x^2 - a^2}$ → secante.",
              "**Olvidar el $|\\cos\\theta|$ y simplificarlo a $\\cos\\theta$ sin justificar.** Eligiendo el rango principal de $\\theta$, $\\cos\\theta \\geq 0$ y se justifica.",
              "**No volver a $x$** al final. La respuesta de una indefinida debe estar en términos de $x$, no de $\\theta$.",
              "**No usar el triángulo auxiliar.** Para volver a $x$, dibujar el triángulo rectángulo con la sustitución es la herramienta más rápida.",
              "**Confundirse en la diferencial:** $dx = a\\cos\\theta \\, d\\theta$ (no $a \\, d\\theta$).",
          ]),

        b("resumen",
          puntos_md=[
              "**Tres formas, tres sustituciones** (memorizar la tabla).",
              "**$\\sqrt{a^2 - x^2}$:** $x = a\\sin\\theta$, raíz $\\to a\\cos\\theta$, $dx = a\\cos\\theta \\, d\\theta$.",
              "**$\\sqrt{a^2 + x^2}$:** $x = a\\tan\\theta$, raíz $\\to a\\sec\\theta$, $dx = a\\sec^2\\theta \\, d\\theta$.",
              "**$\\sqrt{x^2 - a^2}$:** $x = a\\sec\\theta$, raíz $\\to a\\tan\\theta$, $dx = a\\sec\\theta\\tan\\theta \\, d\\theta$.",
              "**Volver a $x$ con triángulo auxiliar:** dibujar el triángulo rectángulo de la sustitución.",
              "**Próxima lección:** división polinomial — preparar fracciones racionales con grado de numerador alto.",
          ]),
    ]
    return {
        "id": "lec-metodos-2-4-sustitucion-trig",
        "title": "Sustitución trigonométrica",
        "description": "Eliminar raíces $\\sqrt{a^2 \\pm x^2}$ y $\\sqrt{x^2 - a^2}$ con identidades pitagóricas.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# 2.5 División polinomial
# =====================================================================
def lesson_2_5():
    blocks = [
        b("texto", body_md=(
            "Cuando el integrando es una **fracción racional** $\\dfrac{P(x)}{Q(x)}$ con $\\deg P \\geq \\deg Q$, "
            "la fracción es **impropia** y no se puede integrar directamente. "
            "El primer paso es la **división polinomial**: reescribir como cociente + resto/divisor.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Aplicar la división polinomial larga.\n"
            "- Reescribir una fracción impropia como **polinomio + fracción propia**.\n"
            "- Integrar el polinomio directo y dejar la fracción propia para fracciones parciales (próxima lección)."
        )),

        b("intuicion",
          titulo="Como en la aritmética",
          body_md=(
              "Igual que $7/3 = 2 + 1/3$ (cociente más resto sobre divisor), polinomios:\n\n"
              "$$\\dfrac{P(x)}{Q(x)} = C(x) + \\dfrac{R(x)}{Q(x)}$$\n\n"
              "donde $C(x)$ es el cociente y $R(x)$ es el resto, con $\\deg R < \\deg Q$.\n\n"
              "**Por qué importa:** $C(x)$ es polinomial → trivial integrar. La fracción $R(x)/Q(x)$ es **propia** y se ataca con fracciones parciales."
          )),

        b("definicion",
          titulo="División polinomial larga",
          body_md=(
              "Para dividir $P(x) \\div Q(x)$:\n\n"
              "**1.** Dividir el término principal de $P$ por el de $Q$ → primer término del cociente.\n\n"
              "**2.** Multiplicar ese término por $Q$ y restar de $P$.\n\n"
              "**3.** Repetir con el resto, hasta que el grado del resto sea menor que $\\deg Q$.\n\n"
              "**Resultado:** $P(x) = Q(x) \\cdot C(x) + R(x)$, equivalente a $\\dfrac{P}{Q} = C + \\dfrac{R}{Q}$."
          )),

        b("ejemplo_resuelto",
          titulo="$\\int \\dfrac{x^3 + 2x + 1}{x - 1} \\, dx$",
          problema_md="Calcular usando división polinomial.",
          pasos=[
              {"accion_md": "**División larga** $x^3 + 0x^2 + 2x + 1$ entre $x - 1$:\n\n"
                            "- $x^3 \\div x = x^2$. $x^2 \\cdot (x-1) = x^3 - x^2$. Resto parcial: $x^2 + 2x + 1$.\n"
                            "- $x^2 \\div x = x$. $x(x-1) = x^2 - x$. Resto: $3x + 1$.\n"
                            "- $3x \\div x = 3$. $3(x-1) = 3x - 3$. Resto: $4$.\n\n"
                            "**Cociente:** $x^2 + x + 3$. **Resto:** $4$.",
               "justificacion_md": "$\\deg(\\text{resto}) = 0 < \\deg(\\text{divisor}) = 1$, listo.",
               "es_resultado": False},
              {"accion_md": "**Reescribimos:**\n\n$$\\dfrac{x^3 + 2x + 1}{x - 1} = x^2 + x + 3 + \\dfrac{4}{x - 1}$$",
               "justificacion_md": "Cociente más resto sobre divisor.",
               "es_resultado": False},
              {"accion_md": "**Integramos:**\n\n$$\\int \\left(x^2 + x + 3 + \\dfrac{4}{x-1}\\right) dx = \\dfrac{x^3}{3} + \\dfrac{x^2}{2} + 3x + 4\\ln|x-1| + C$$",
               "justificacion_md": "Polinomio término a término. Para $4/(x-1)$, sustitución $u = x - 1$ da $4 \\ln|u|$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Cuando el cociente es solo constante: $\\int \\dfrac{x^2}{x^2 + 1} \\, dx$",
          problema_md="Calcular.",
          pasos=[
              {"accion_md": "**División:** $x^2 \\div (x^2 + 1)$. Cociente $1$ (porque $x^2 = 1 \\cdot (x^2 + 1) - 1$). Resto $-1$.\n\n"
                            "$$\\dfrac{x^2}{x^2 + 1} = 1 - \\dfrac{1}{x^2 + 1}$$",
               "justificacion_md": "Truco rápido: sumar y restar lo necesario en el numerador. $x^2 = (x^2 + 1) - 1$.",
               "es_resultado": False},
              {"accion_md": "**Integramos:**\n\n$$\\int \\left(1 - \\dfrac{1}{x^2 + 1}\\right) dx = x - \\arctan x + C$$",
               "justificacion_md": "Tabla básica para $\\arctan$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el manejo:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuándo aplicar división polinomial antes de integrar $P(x)/Q(x)$?",
                  "opciones_md": [
                      "Siempre.",
                      "Cuando $\\deg P \\geq \\deg Q$ (fracción impropia).",
                      "Cuando $\\deg P < \\deg Q$.",
                      "Nunca, si se puede usar fracciones parciales.",
                  ],
                  "correcta": "B",
                  "pista_md": "Si $\\deg P < \\deg Q$, ya es propia y se va directo a fracciones parciales.",
                  "explicacion_md": (
                      "**Fracción impropia** ($\\deg P \\geq \\deg Q$) requiere división primero. **Propia** ($\\deg P < \\deg Q$) va directo a fracciones parciales."
                  ),
              },
              {
                  "enunciado_md": "Después de dividir $P/Q$, $\\deg(\\text{resto})$ es:",
                  "opciones_md": [
                      "Igual a $\\deg Q$.",
                      "Estrictamente menor que $\\deg Q$.",
                      "Mayor que $\\deg Q$.",
                      "Cero siempre.",
                  ],
                  "correcta": "B",
                  "pista_md": "Si fuera mayor o igual, podríamos seguir dividiendo.",
                  "explicacion_md": (
                      "Por definición, la división se detiene cuando $\\deg(\\text{resto}) < \\deg(\\text{divisor})$. La fracción $R/Q$ resultante es propia."
                  ),
              },
          ]),

        ej(
            titulo="Práctica de división",
            enunciado="Calcula $\\int \\dfrac{x^2 + 5}{x + 2} \\, dx$.",
            pistas=[
                "Divide $x^2 + 5$ entre $x + 2$.",
                "Cociente $x - 2$, resto $9$. Verifica: $(x-2)(x+2) + 9 = x^2 - 4 + 9 = x^2 + 5$. ✓",
            ],
            solucion=(
                "$$\\dfrac{x^2 + 5}{x + 2} = x - 2 + \\dfrac{9}{x + 2}$$\n\n"
                "$$\\int \\left(x - 2 + \\dfrac{9}{x+2}\\right) dx = \\dfrac{x^2}{2} - 2x + 9\\ln|x+2| + C$$"
            ),
        ),

        fig(
            "Esquema de división polinomial larga al estilo de pizarrón didáctico. A la izquierda, dividendo P(x) = x² + 5 dentro del símbolo de división y divisor Q(x) = x + 2 fuera. Pasos sucesivos de cocientes parciales y restos alineados verticalmente, con flechas ámbar #f59e0b indicando cada resta. Cociente 'x − 2' arriba y resto '9' abajo. Debajo, en grande, la igualdad final: P(x)/Q(x) = (x − 2) + 9/(x+2). Cociente en teal #06b6d4 y resto en ámbar."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Olvidar términos faltantes** al dividir. Ejemplo: $x^3 + 2x + 1$ se debe escribir como $x^3 + 0x^2 + 2x + 1$ para alinear bien.",
              "**Detenerse antes** de que $\\deg(\\text{resto}) < \\deg Q$. Si quedan términos divisibles, hay que seguir.",
              "**No reconocer el truco rápido** $x^n = (x^n + a) - a$ que evita la división larga en fracciones simples.",
              "**Aplicar fracciones parciales antes de dividir** cuando la fracción es impropia. La descomposición no funciona directamente.",
          ]),

        b("resumen",
          puntos_md=[
              "**División polinomial:** $P/Q = C + R/Q$ con $\\deg R < \\deg Q$.",
              "**Cuándo aplicar:** $\\deg P \\geq \\deg Q$ (fracción impropia).",
              "**Resultado:** se integra $C$ directo (polinomio) y queda $R/Q$ como fracción propia.",
              "**Trucos rápidos:** sumar/restar en el numerador para evitar la división larga en casos simples.",
              "**Próxima lección:** fracciones parciales — descomponer la fracción propia $R/Q$ en sumandos integrables.",
          ]),
    ]
    return {
        "id": "lec-metodos-2-5-division",
        "title": "División polinomial",
        "description": "Reescribir una fracción racional impropia como polinomio + fracción propia antes de integrar.",
        "blocks": blocks,
        "duration_minutes": 35,
        "order": 5,
    }


# =====================================================================
# 2.6 Fracciones parciales
# =====================================================================
def lesson_2_6():
    blocks = [
        b("texto", body_md=(
            "Toda **fracción racional propia** $P(x)/Q(x)$ se puede descomponer en una suma de "
            "**fracciones más simples** que sí están en la tabla básica. Esta técnica — "
            "**descomposición en fracciones parciales** — es la herramienta más sistemática para "
            "integrar fracciones racionales arbitrarias.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Reconocer los **cuatro casos** de descomposición según el tipo de factores en $Q(x)$.\n"
            "- Plantear el sistema de coeficientes y resolverlo.\n"
            "- Integrar cada fracción parcial."
        )),

        b("definicion",
          titulo="Los cuatro casos",
          body_md=(
              "Sea $P(x)/Q(x)$ propia. Factorizamos $Q(x)$ en factores **lineales** $(ax+b)$ y **cuadráticos irreducibles** $(ax^2 + bx + c)$ con discriminante negativo. Por cada factor:\n\n"
              "**Caso 1 — Factor lineal $(ax + b)$ no repetido:**\n\n"
              "$$\\dfrac{A}{ax + b}$$\n\n"
              "**Caso 2 — Factor lineal $(ax + b)^k$ repetido $k$ veces:**\n\n"
              "$$\\dfrac{A_1}{ax+b} + \\dfrac{A_2}{(ax+b)^2} + \\cdots + \\dfrac{A_k}{(ax+b)^k}$$\n\n"
              "**Caso 3 — Factor cuadrático irreducible $(ax^2 + bx + c)$ no repetido:**\n\n"
              "$$\\dfrac{Ax + B}{ax^2 + bx + c}$$\n\n"
              "**Caso 4 — Factor cuadrático irreducible $(ax^2+bx+c)^k$ repetido:**\n\n"
              "$$\\dfrac{A_1 x + B_1}{ax^2+bx+c} + \\dfrac{A_2 x + B_2}{(ax^2+bx+c)^2} + \\cdots + \\dfrac{A_k x + B_k}{(ax^2+bx+c)^k}$$"
          )),

        b("ejemplo_resuelto",
          titulo="Caso 1: factores lineales distintos",
          problema_md="Calcular $\\int \\dfrac{x + 5}{(x-1)(x+2)} \\, dx$.",
          pasos=[
              {"accion_md": "**Plantear:**\n\n$$\\dfrac{x+5}{(x-1)(x+2)} = \\dfrac{A}{x-1} + \\dfrac{B}{x+2}$$",
               "justificacion_md": "Dos factores lineales distintos → dos constantes.",
               "es_resultado": False},
              {"accion_md": "**Multiplicar por $(x-1)(x+2)$:**\n\n$$x + 5 = A(x+2) + B(x-1)$$",
               "justificacion_md": "Eliminamos los denominadores.",
               "es_resultado": False},
              {"accion_md": "**Asignar valores estratégicos:**\n\n- $x = 1$: $1 + 5 = A(3) + B(0) \\implies A = 2$.\n- $x = -2$: $-2 + 5 = A(0) + B(-3) \\implies B = -1$.",
               "justificacion_md": "Cada raíz del denominador anula el otro término — método rápido.",
               "es_resultado": False},
              {"accion_md": "**Integrar:**\n\n$$\\int \\left(\\dfrac{2}{x-1} - \\dfrac{1}{x+2}\\right) dx = 2\\ln|x-1| - \\ln|x+2| + C$$",
               "justificacion_md": "Cada parcial es del tipo $A/(x-r)$ → logaritmo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caso 2: factor lineal repetido",
          problema_md="Calcular $\\int \\dfrac{x^2 + 1}{(x-1)^3} \\, dx$.",
          pasos=[
              {"accion_md": "**Plantear:**\n\n$$\\dfrac{x^2 + 1}{(x-1)^3} = \\dfrac{A}{x-1} + \\dfrac{B}{(x-1)^2} + \\dfrac{C}{(x-1)^3}$$",
               "justificacion_md": "Factor lineal repetido $k = 3$ veces → tres parciales con potencias crecientes.",
               "es_resultado": False},
              {"accion_md": "**Multiplicar por $(x-1)^3$:**\n\n$$x^2 + 1 = A(x-1)^2 + B(x-1) + C$$",
               "justificacion_md": "Despejamos.",
               "es_resultado": False},
              {"accion_md": "**Sustituir $x = 1$ directamente:** $1 + 1 = C \\implies C = 2$.\n\n"
                            "**Expandir** $A(x-1)^2 + B(x-1) + 2 = Ax^2 - 2Ax + A + Bx - B + 2$. **Comparar coeficientes** con $x^2 + 1$:\n\n"
                            "- $x^2$: $A = 1$.\n- $x$: $-2A + B = 0 \\implies B = 2$.\n- const: $A - B + 2 = 1 \\implies 1 - 2 + 2 = 1$. ✓",
               "justificacion_md": "Mezcla de sustitución y comparación de coeficientes.",
               "es_resultado": False},
              {"accion_md": "**Integrar:**\n\n$$\\int \\left(\\dfrac{1}{x-1} + \\dfrac{2}{(x-1)^2} + \\dfrac{2}{(x-1)^3}\\right) dx$$\n\n"
                            "$$= \\ln|x-1| - \\dfrac{2}{x-1} - \\dfrac{1}{(x-1)^2} + C$$",
               "justificacion_md": "$\\int (x-1)^{-n} \\, dx = \\dfrac{(x-1)^{-n+1}}{-n+1}$ para $n \\geq 2$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Caso 3: factor cuadrático irreducible",
          problema_md="Calcular $\\int \\dfrac{2x^2 + 1}{(x+1)(x^2 + 1)} \\, dx$.",
          pasos=[
              {"accion_md": "**Plantear:**\n\n$$\\dfrac{2x^2 + 1}{(x+1)(x^2+1)} = \\dfrac{A}{x+1} + \\dfrac{Bx + C}{x^2 + 1}$$",
               "justificacion_md": "$x^2 + 1$ es cuadrático irreducible (discriminante $-4 < 0$).",
               "es_resultado": False},
              {"accion_md": "**Multiplicar:** $2x^2 + 1 = A(x^2+1) + (Bx+C)(x+1)$.\n\n"
                            "**$x = -1$:** $2 + 1 = A(2) + 0 \\implies A = 3/2$.\n\n"
                            "**Expandir y comparar coeficientes:** $A x^2 + A + Bx^2 + Bx + Cx + C = (A+B)x^2 + (B+C)x + (A + C)$. Igualando con $2x^2 + 0x + 1$:\n\n"
                            "- $A + B = 2 \\implies B = 1/2$.\n- $B + C = 0 \\implies C = -1/2$.\n- $A + C = 1 \\implies 3/2 - 1/2 = 1$. ✓",
               "justificacion_md": "Sistema de 3 ecuaciones, 3 incógnitas.",
               "es_resultado": False},
              {"accion_md": "**Integrar:**\n\n$$\\int \\dfrac{3/2}{x+1} dx + \\int \\dfrac{(1/2)x - 1/2}{x^2 + 1} dx$$\n\n"
                            "Para la segunda, separamos: $\\dfrac{(1/2) x}{x^2 + 1} - \\dfrac{1/2}{x^2+1}$.\n\n"
                            "$$= \\dfrac{3}{2}\\ln|x+1| + \\dfrac{1}{4}\\ln(x^2+1) - \\dfrac{1}{2}\\arctan x + C$$",
               "justificacion_md": "Para $x/(x^2+1)$ — sustitución $u = x^2+1$. Para $1/(x^2+1)$ — $\\arctan$.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica los casos:",
          preguntas=[
              {
                  "enunciado_md": "¿Cuál es la descomposición de $\\dfrac{1}{x^2(x-1)}$?",
                  "opciones_md": [
                      "$\\dfrac{A}{x^2} + \\dfrac{B}{x-1}$",
                      "$\\dfrac{A}{x} + \\dfrac{B}{x^2} + \\dfrac{C}{x-1}$",
                      "$\\dfrac{A}{x} + \\dfrac{B}{x-1}$",
                      "$\\dfrac{Ax+B}{x^2} + \\dfrac{C}{x-1}$",
                  ],
                  "correcta": "B",
                  "pista_md": "$x^2 = x \\cdot x$ es factor lineal $x$ **repetido** dos veces.",
                  "explicacion_md": (
                      "$x^2 = (x)^2$ es factor lineal repetido $k=2$. Caso 2 de la tabla. Más el factor $(x-1)$ no repetido (caso 1)."
                  ),
              },
              {
                  "enunciado_md": "$\\int \\dfrac{1}{x-r} \\, dx$ es:",
                  "opciones_md": [
                      "$\\dfrac{1}{(x-r)^2}$",
                      "$\\ln|x-r| + C$",
                      "$\\arctan(x-r) + C$",
                      "$x \\ln|x-r| + C$",
                  ],
                  "correcta": "B",
                  "pista_md": "Sustitución $u = x - r$ da $\\int 1/u \\, du$.",
                  "explicacion_md": (
                      "Cada fracción parcial del tipo $A/(x-r)$ se integra como $A \\ln|x-r| + C$ — directamente del logaritmo natural."
                  ),
              },
          ]),

        ej(
            titulo="Caso 1 simple",
            enunciado="Calcula $\\int \\dfrac{1}{x^2 - 4} \\, dx$.",
            pistas=[
                "Factoriza: $x^2 - 4 = (x-2)(x+2)$.",
                "Descompón: $\\dfrac{1}{(x-2)(x+2)} = \\dfrac{A}{x-2} + \\dfrac{B}{x+2}$.",
                "Resuelve y obtén $A = 1/4$, $B = -1/4$.",
            ],
            solucion=(
                "$1 = A(x+2) + B(x-2)$. **$x = 2$:** $1 = 4A \\implies A = 1/4$. **$x = -2$:** $1 = -4B \\implies B = -1/4$.\n\n"
                "$$\\int \\left(\\dfrac{1/4}{x-2} - \\dfrac{1/4}{x+2}\\right) dx = \\dfrac{1}{4}\\ln\\left|\\dfrac{x-2}{x+2}\\right| + C$$"
            ),
        ),

        fig(
            "Diagrama tipo árbol jerárquico. En la raíz, una fracción racional genérica P(x)/Q(x) en teal #06b6d4. Tres ramas hacia abajo, cada una etiquetada con un caso de descomposición en fracciones parciales: rama 1 'Factores lineales simples' con término A/(x−a); rama 2 'Factores lineales repetidos' con términos A/(x−a) + B/(x−a)²; rama 3 'Factor cuadrático irreducible' con término (Cx+D)/(x²+1). Los numeradores A, B, C, D resaltados en ámbar #f59e0b."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**No verificar que la fracción es propia** antes de descomponer. Si es impropia, hacer división polinomial primero (lección 2.5).",
              "**Olvidar que un factor repetido aporta varios términos** ($k$ términos para multiplicidad $k$).",
              "**Plantear $A$ sobre un factor cuadrático irreducible.** El numerador en ese caso es $Ax + B$, no solo $A$.",
              "**Olvidar el valor absoluto** en $\\ln|x-r|$ — sin él, la antiderivada solo vale para $x > r$.",
              "**Mezclar los métodos** de coeficientes: sustituir raíces es rápido para factores lineales; comparar coeficientes es necesario cuando hay términos repetidos o cuadráticos.",
          ]),

        b("resumen",
          puntos_md=[
              "**Cuatro casos:** lineal simple, lineal repetido, cuadrático irreducible simple, cuadrático irreducible repetido.",
              "**Cada factor lineal $(ax+b)^k$:** aporta $k$ parciales $A_i/(ax+b)^i$.",
              "**Cada cuadrático irreducible $(ax^2+bx+c)^k$:** aporta $k$ parciales $(A_i x + B_i)/(ax^2+bx+c)^i$.",
              "**Métodos para coeficientes:** sustituir raíces (rápido para lineales) + comparar coeficientes (general).",
              "**Integrales resultantes:** $\\ln$, potencias inversas, $\\arctan$.",
              "**Próxima lección:** integrales impropias (límites infinitos o integrandos no acotados).",
          ]),
    ]
    return {
        "id": "lec-metodos-2-6-fracciones-parciales",
        "title": "Fracciones parciales",
        "description": "Descomposición de fracciones racionales propias en sumandos integrables. Cuatro casos.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 6,
    }


# =====================================================================
# 2.7 Integrales impropias
# =====================================================================
def lesson_2_7():
    blocks = [
        b("texto", body_md=(
            "Hasta ahora $\\int_a^b f \\, dx$ asumía $a, b$ finitos y $f$ acotada en $[a, b]$. "
            "Las **integrales impropias** relajan estas dos hipótesis: o el intervalo es **infinito**, "
            "o el integrando **no está acotado** (típicamente diverge cerca de un punto). "
            "En ambos casos hay que pasar por un **límite**.\n\n"
            "Al terminar, los objetivos son:\n\n"
            "- Distinguir los **dos tipos** de impropias.\n"
            "- Calcular impropias del tipo 1 (límites infinitos) vía límite de la integral propia.\n"
            "- Calcular impropias del tipo 2 (integrando no acotado) análogamente.\n"
            "- Determinar cuándo una impropia **converge** o **diverge**.\n"
            "- Aplicar el **criterio $p$**: $\\int_1^\\infty 1/x^p \\, dx$ converge si y solo si $p > 1$."
        )),

        b("definicion",
          titulo="Tipo 1 — Límites infinitos",
          body_md=(
              "**Caso $a$ a $\\infty$:**\n\n"
              "$$\\int_a^\\infty f(x) \\, dx = \\lim_{t \\to \\infty} \\int_a^t f(x) \\, dx$$\n\n"
              "**Caso $-\\infty$ a $b$:**\n\n"
              "$$\\int_{-\\infty}^b f(x) \\, dx = \\lim_{t \\to -\\infty} \\int_t^b f(x) \\, dx$$\n\n"
              "**Caso $-\\infty$ a $\\infty$:** se parte en dos en cualquier $c$:\n\n"
              "$$\\int_{-\\infty}^\\infty f \\, dx = \\int_{-\\infty}^c f \\, dx + \\int_c^\\infty f \\, dx$$\n\n"
              "y se requiere que **ambas** converjan.\n\n"
              "Si el límite existe y es finito, la integral **converge** a ese valor. Si no, **diverge**."
          )),

        b("definicion",
          titulo="Tipo 2 — Integrando no acotado",
          body_md=(
              "Si $f$ tiene una asíntota vertical en $c$:\n\n"
              "**Asíntota en $c = b$ (extremo derecho):**\n\n"
              "$$\\int_a^b f \\, dx = \\lim_{t \\to b^-} \\int_a^t f \\, dx$$\n\n"
              "**Asíntota en $c = a$ (extremo izquierdo):**\n\n"
              "$$\\int_a^b f \\, dx = \\lim_{t \\to a^+} \\int_t^b f \\, dx$$\n\n"
              "**Asíntota en $c \\in (a, b)$ (interior):** partir en dos:\n\n"
              "$$\\int_a^b f \\, dx = \\int_a^c f \\, dx + \\int_c^b f \\, dx$$\n\n"
              "y ambas (impropias en $c$) deben converger."
          )),

        b("ejemplo_resuelto",
          titulo="Tipo 1: $\\int_1^\\infty \\dfrac{1}{x^2} \\, dx$",
          problema_md="Determinar si converge y, si lo hace, calcular el valor.",
          pasos=[
              {"accion_md": "**Por definición:**\n\n$$\\int_1^\\infty \\dfrac{1}{x^2} \\, dx = \\lim_{t \\to \\infty} \\int_1^t \\dfrac{1}{x^2} \\, dx$$",
               "justificacion_md": "Convertimos en límite de una propia.",
               "es_resultado": False},
              {"accion_md": "**Calcular la propia:**\n\n$$\\int_1^t \\dfrac{1}{x^2} \\, dx = \\left[-\\dfrac{1}{x}\\right]_1^t = -\\dfrac{1}{t} - (-1) = 1 - \\dfrac{1}{t}$$",
               "justificacion_md": "Antiderivada $-1/x$.",
               "es_resultado": False},
              {"accion_md": "**Tomar el límite:**\n\n$$\\lim_{t \\to \\infty}\\left(1 - \\dfrac{1}{t}\\right) = 1$$",
               "justificacion_md": "El límite existe y es finito → **converge** a $1$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Tipo 1 divergente: $\\int_1^\\infty \\dfrac{1}{x} \\, dx$",
          problema_md="Determinar si converge.",
          pasos=[
              {"accion_md": "**Calcular:** $\\int_1^t \\dfrac{1}{x} \\, dx = \\ln t - \\ln 1 = \\ln t$.",
               "justificacion_md": "Antiderivada $\\ln|x|$.",
               "es_resultado": False},
              {"accion_md": "**Límite:** $\\lim_{t \\to \\infty} \\ln t = +\\infty$. **Diverge.**",
               "justificacion_md": "**Lección sorprendente:** $1/x$ y $1/x^2$ son ambos parecidos visualmente, pero solo el segundo tiene área finita. La diferencia es **cuán rápido decrecen al infinito**.",
               "es_resultado": True},
          ]),

        b("teorema",
          nombre="Criterio $p$",
          enunciado_md=(
              "$$\\int_1^\\infty \\dfrac{1}{x^p} \\, dx$$\n\n"
              "**converge** si $p > 1$, **diverge** si $p \\leq 1$.\n\n"
              "**Análogamente:** $\\int_0^1 \\dfrac{1}{x^p} \\, dx$ **converge** si $p < 1$, **diverge** si $p \\geq 1$."
          ),
          demostracion_md=(
              "**Para $p \\neq 1$:**\n\n"
              "$$\\int_1^t \\dfrac{1}{x^p} \\, dx = \\dfrac{x^{1-p}}{1-p}\\Big|_1^t = \\dfrac{t^{1-p} - 1}{1-p}$$\n\n"
              "Cuando $t \\to \\infty$: si $p > 1$, $1 - p < 0$ y $t^{1-p} \\to 0$, así el límite es $\\dfrac{-1}{1-p} = \\dfrac{1}{p-1}$ (finito, **converge**). Si $p < 1$, $t^{1-p} \\to \\infty$ (**diverge**).\n\n"
              "**Para $p = 1$:** $\\int 1/x = \\ln t \\to \\infty$ (**diverge**)."
          )),

        b("ejemplo_resuelto",
          titulo="Tipo 2: $\\int_0^1 \\dfrac{1}{\\sqrt{x}} \\, dx$",
          problema_md="$1/\\sqrt{x}$ es no acotada en $x = 0$. Determinar convergencia.",
          pasos=[
              {"accion_md": "**Por definición:** asíntota en $a = 0$, así\n\n$$\\int_0^1 \\dfrac{1}{\\sqrt{x}} \\, dx = \\lim_{t \\to 0^+} \\int_t^1 x^{-1/2} \\, dx$$",
               "justificacion_md": "Tipo 2 con asíntota en el extremo izquierdo.",
               "es_resultado": False},
              {"accion_md": "**Calcular:** $\\int_t^1 x^{-1/2} \\, dx = [2\\sqrt{x}]_t^1 = 2 - 2\\sqrt{t}$.",
               "justificacion_md": "Antiderivada $2 x^{1/2}$.",
               "es_resultado": False},
              {"accion_md": "**Límite:** $\\lim_{t \\to 0^+}(2 - 2\\sqrt{t}) = 2$. **Converge a $2$.**",
               "justificacion_md": "**Otro patrón sorprendente:** la función crece a infinito cerca de $0$, pero el área bajo ella es finita (porque crece 'lento': como $x^{-1/2}$, no como $x^{-1}$).",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Tipo 2 con asíntota interior: $\\int_{-1}^1 \\dfrac{1}{x^2} \\, dx$",
          problema_md="¿Converge? La función diverge en $x = 0$.",
          pasos=[
              {"accion_md": "**Partir en $0$:**\n\n$$\\int_{-1}^1 \\dfrac{1}{x^2} \\, dx = \\int_{-1}^0 \\dfrac{1}{x^2} \\, dx + \\int_0^1 \\dfrac{1}{x^2} \\, dx$$\n\n"
                            "Ambas son impropias en $0$.",
               "justificacion_md": "**No** se puede aplicar Barrow ingenuamente — daría $-1 - 1 = -2$, **incorrecto** porque ignora la asíntota interior.",
               "es_resultado": False},
              {"accion_md": "**Calcular $\\int_0^1 1/x^2 \\, dx$:** $\\lim_{t \\to 0^+} [-1/x]_t^1 = \\lim_{t \\to 0^+}(-1 + 1/t) = +\\infty$. **Diverge.**",
               "justificacion_md": "Por criterio $p$ con $p = 2 \\geq 1$ en intervalo cerca de $0$, diverge.",
               "es_resultado": False},
              {"accion_md": "**Como una de las dos diverge, la integral original DIVERGE.**",
               "justificacion_md": "**Trampa famosa:** aplicar Barrow a $\\int_{-1}^1 1/x^2$ daría un valor finito y negativo, lo que es absurdo (el integrando es positivo). Hay que verificar siempre la continuidad antes de aplicar el TFC.",
               "es_resultado": True},
          ]),

        b("verificacion",
          intro_md="Verifica el criterio:",
          preguntas=[
              {
                  "enunciado_md": "¿$\\int_1^\\infty \\dfrac{1}{x^{1/2}} \\, dx$ converge?",
                  "opciones_md": [
                      "Sí, por criterio $p$.",
                      "No, $p \\leq 1$.",
                      "Sí, vale $\\sqrt{1}$.",
                      "Depende del integrando.",
                  ],
                  "correcta": "B",
                  "pista_md": "$p = 1/2$. Criterio $p$ para $[1, \\infty)$: converge si $p > 1$.",
                  "explicacion_md": (
                      "$p = 1/2 \\leq 1$. **Diverge.** $\\int 1/\\sqrt{x} = 2\\sqrt{x} \\to \\infty$ cuando $x \\to \\infty$."
                  ),
              },
              {
                  "enunciado_md": "Si $f$ tiene una asíntota vertical en $c \\in (a, b)$, ¿se puede aplicar Barrow directamente a $\\int_a^b f$?",
                  "opciones_md": [
                      "Sí, siempre.",
                      "Solo si la antiderivada es continua.",
                      "No, hay que partir en $c$ y verificar convergencia de cada trozo.",
                      "Solo si $f$ es positiva.",
                  ],
                  "correcta": "C",
                  "pista_md": "Barrow requiere continuidad del integrando en el cerrado.",
                  "explicacion_md": (
                      "El TFC parte 2 exige $f$ continua en $[a, b]$. Si hay asíntota interior, hay que partir y tratar como impropia."
                  ),
              },
          ]),

        ej(
            titulo="Aplicar criterio $p$",
            enunciado="¿Converge $\\int_1^\\infty \\dfrac{1}{x^3} \\, dx$? Si sí, calcula su valor.",
            pistas=[
                "$p = 3 > 1$ → criterio $p$ dice converge.",
                "Calcula $\\lim_{t \\to \\infty} \\int_1^t x^{-3} \\, dx$.",
            ],
            solucion=(
                "Sí, **converge** ($p = 3 > 1$).\n\n"
                "$\\int_1^t x^{-3} \\, dx = \\left[\\dfrac{x^{-2}}{-2}\\right]_1^t = -\\dfrac{1}{2t^2} + \\dfrac{1}{2}$.\n\n"
                "$\\lim_{t \\to \\infty}\\left(\\dfrac{1}{2} - \\dfrac{1}{2t^2}\\right) = \\dfrac{1}{2}$."
            ),
        ),

        ej(
            titulo="Tipo 2 con asíntota en el borde",
            enunciado="¿Converge $\\int_0^1 \\dfrac{1}{x} \\, dx$?",
            pistas=[
                "$1/x$ diverge en $x = 0$. Es impropia tipo 2.",
                "Por criterio $p$ análogo en $[0, 1]$: $1/x^p$ converge si $p < 1$.",
            ],
            solucion=(
                "$p = 1 \\geq 1$ → **diverge** (criterio $p$ en $[0, 1]$).\n\n"
                "Verificación: $\\int_t^1 \\dfrac{1}{x} \\, dx = -\\ln t \\to +\\infty$ cuando $t \\to 0^+$."
            ),
        ),

        fig(
            "Dos paneles con ejes cartesianos. Panel izquierdo 'Intervalo infinito': curva y = 1/x² desde x = 1 extendiéndose a la derecha; el área bajo la curva entre x = 1 y un x = b grande está sombreada en teal #06b6d4, con flecha ámbar #f59e0b apuntando a la derecha y leyenda 'lim_{b→∞}'. Panel derecho 'Función no acotada': curva y = 1/√x cerca de x = 0 con asíntota vertical ámbar #f59e0b en x = 0; área entre x = t y x = 1 sombreada en teal y leyenda 'lim_{t→0+}'. Etiquetas claras."
            + STYLE
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar Barrow ingenuamente** cuando hay asíntota interior. Ejemplo trampa: $\\int_{-1}^1 1/x^2 \\, dx$.",
              "**Confundir 'integrando va a $0$ al infinito' con 'integral converge'.** $1/x \\to 0$ pero $\\int_1^\\infty 1/x$ diverge.",
              "**Pensar que el criterio $p$ es el mismo en $[0, 1]$ y $[1, \\infty)$.** Es **opuesto**: en infinito $p > 1$ converge; en $0$ $p < 1$ converge.",
              "**Olvidar partir en dos** una integral con asíntotas en ambos extremos o interior.",
              "**Concluir convergencia desde una sola integración por partes** sin verificar el límite final del término evaluado.",
          ]),

        b("resumen",
          puntos_md=[
              "**Tipo 1:** límites infinitos. $\\int_a^\\infty f = \\lim_{t \\to \\infty} \\int_a^t f$.",
              "**Tipo 2:** integrando no acotado. Reemplazar el extremo problemático por un límite.",
              "**Convergencia:** límite finito = converge. Infinito o no existe = diverge.",
              "**Criterio $p$:** $\\int_1^\\infty 1/x^p$ converge $\\iff p > 1$. $\\int_0^1 1/x^p$ converge $\\iff p < 1$.",
              "**Asíntotas interiores:** partir el intervalo y verificar convergencia de cada trozo.",
              "**Próximo capítulo:** aplicaciones de la integral — áreas entre curvas, volúmenes de sólidos, longitud de arco, etc.",
          ]),
    ]
    return {
        "id": "lec-metodos-2-7-impropias",
        "title": "Integrales impropias",
        "description": "Integrales con límites infinitos o integrandos no acotados. Convergencia, divergencia y criterio $p$.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 7,
    }


# =====================================================================
# MAIN
# =====================================================================
async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    course_id = "calculo-integral"

    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise SystemExit(f"Course {course_id} not found. Corre primero seed_calculo_integral_chapter_1.py")

    chapter_id = "ch-metodos-integracion"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Métodos de Integración",
        "description": "Sustitución, integración por partes, integrales trigonométricas, sustitución trigonométrica, división polinomial, fracciones parciales e impropias.",
        "order": 2,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_2_1, lesson_2_2, lesson_2_3, lesson_2_4,
        lesson_2_5, lesson_2_6, lesson_2_7,
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
    print(f"✅ Capítulo 2 — Métodos de Integración listo: {len(builders)} lecciones, {total_blocks} bloques.")
    print()
    print("Lecciones disponibles en:")
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())
