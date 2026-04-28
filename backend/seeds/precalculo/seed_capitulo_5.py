"""
Seed del curso Precálculo — Capítulo 5: Funciones Trigonométricas.

Crea el capítulo 'Funciones Trigonométricas' bajo el curso 'precalculo'
y siembra sus 7 lecciones:

  - Ángulos y medidas
  - Triángulos
  - Círculo unitario
  - Funciones trigonométricas
  - Gráficas trigonométricas
  - Funciones trigonométricas inversas
  - Leyes trigonométricas

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
# Ángulos y medidas
# =====================================================================
def lesson_angulos_medidas():
    blocks = [
        b("texto", body_md=(
            "Antes de hablar de funciones trigonométricas, hay que precisar qué entendemos por **ángulo** "
            "y cómo lo **medimos**.\n\n"
            "Un ángulo es la **rotación** desde un rayo inicial hasta uno final, alrededor de un vértice "
            "común. Lo medimos con dos sistemas:\n\n"
            "- **Grados:** el sistema escolar, una vuelta completa = $360^\\circ$.\n"
            "- **Radianes:** el sistema 'natural' de la matemática, una vuelta completa = $2\\pi$ rad.\n\n"
            "**¿Por qué dos sistemas?** Los grados son cómodos para uso cotidiano (mapas, ingeniería). Los "
            "radianes hacen las fórmulas del cálculo y la trigonometría **infinitamente más limpias**: "
            "$\\dfrac{d}{dx}\\sin x = \\cos x$ solo es cierto si $x$ está en radianes.\n\n"
            "**Al terminar:**\n\n"
            "- Convertís entre grados y radianes con fluidez.\n"
            "- Reconocés ángulos coterminales, complementarios y suplementarios.\n"
            "- Calculás **longitud de arco** y **área de sector** circular."
        )),

        b("definicion",
          titulo="Grados y radianes",
          body_md=(
              "**Grados.** Una vuelta completa = $360^\\circ$. Un ángulo recto = $90^\\circ$. Un ángulo llano = $180^\\circ$.\n\n"
              "**Radianes.** Un ángulo de **1 radián** es el ángulo central de una circunferencia que **subtiende un arco de longitud igual al radio**. Una vuelta completa = $2 \\pi$ rad (el perímetro de una circunferencia es $2 \\pi r$).\n\n"
              "**Relación fundamental:**\n\n"
              "$$180^\\circ = \\pi \\text{ rad}.$$\n\n"
              "**Conversiones:**\n\n"
              "- Grados $\\to$ radianes: multiplicar por $\\dfrac{\\pi}{180}$.\n"
              "- Radianes $\\to$ grados: multiplicar por $\\dfrac{180}{\\pi}$.\n\n"
              "**Aproximaciones útiles:** $1$ rad $\\approx 57{,}3^\\circ$. $1^\\circ \\approx 0{,}01745$ rad."
          )),

        formulas(
            titulo="Ángulos especiales",
            body=(
                "**Tabla de equivalencias** que conviene tener memorizada:\n\n"
                "| Grados | Radianes | Comentario |\n"
                "|---|---|---|\n"
                "| $30^\\circ$ | $\\pi/6$ | medio cateto $30$-$60$-$90$ |\n"
                "| $45^\\circ$ | $\\pi/4$ | diagonal del cuadrado |\n"
                "| $60^\\circ$ | $\\pi/3$ | triángulo equilátero |\n"
                "| $90^\\circ$ | $\\pi/2$ | recto |\n"
                "| $120^\\circ$ | $2\\pi/3$ | |\n"
                "| $135^\\circ$ | $3\\pi/4$ | |\n"
                "| $150^\\circ$ | $5\\pi/6$ | |\n"
                "| $180^\\circ$ | $\\pi$ | llano |\n"
                "| $270^\\circ$ | $3\\pi/2$ | |\n"
                "| $360^\\circ$ | $2\\pi$ | vuelta |\n\n"
                "**Truco visual:** una vuelta es $2 \\pi$. Dividirla en $4$ da los cuadrantes; en $6$ da los múltiplos de $30^\\circ$; en $8$ los múltiplos de $45^\\circ$."
            ),
        ),

        b("definicion",
          titulo="Tipos de ángulos relacionados",
          body_md=(
              "**Coterminales:** dos ángulos son **coterminales** si tienen el mismo lado terminal. Difieren en un múltiplo entero de $360^\\circ$ (o $2\\pi$ rad).\n\n"
              "Ejemplo: $30^\\circ, 390^\\circ, -330^\\circ$ son coterminales.\n\n"
              "**Complementarios:** dos ángulos cuya **suma es $90^\\circ$** ($\\pi/2$ rad). Ejemplo: $30^\\circ$ y $60^\\circ$.\n\n"
              "**Suplementarios:** dos ángulos cuya **suma es $180^\\circ$** ($\\pi$ rad). Ejemplo: $130^\\circ$ y $50^\\circ$.\n\n"
              "**Ángulo en posición estándar:** el vértice está en el origen y el lado inicial sobre el eje $x$ positivo. El **ángulo positivo** mide en sentido **antihorario**; el **negativo**, horario."
          )),

        b("ejemplo_resuelto",
          titulo="Conversiones",
          problema_md="Convertí: **(a)** $60^\\circ$ a radianes, **(b)** $5 \\pi / 6$ rad a grados, **(c)** $-225^\\circ$ a radianes.",
          pasos=[
              {"accion_md": "**(a)** $60^\\circ \\cdot \\dfrac{\\pi}{180} = \\dfrac{60 \\pi}{180} = \\dfrac{\\pi}{3}$ rad.",
               "justificacion_md": "Multiplicar por $\\pi/180$.",
               "es_resultado": False},
              {"accion_md": "**(b)** $\\dfrac{5 \\pi}{6} \\cdot \\dfrac{180}{\\pi} = \\dfrac{5 \\cdot 180}{6} = 150^\\circ$.",
               "justificacion_md": "Cancelar $\\pi$.",
               "es_resultado": False},
              {"accion_md": "**(c)** $-225^\\circ \\cdot \\dfrac{\\pi}{180} = -\\dfrac{225 \\pi}{180} = -\\dfrac{5 \\pi}{4}$ rad.",
               "justificacion_md": "Conservar el signo.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Longitud de arco y área de sector",
            body=(
                "Para una circunferencia de radio $r$ y un ángulo central $\\theta$ **en radianes**:\n\n"
                "**Longitud del arco subtendido:**\n\n"
                "$$\\boxed{\\,s = r \\theta.\\,}$$\n\n"
                "**Área del sector circular** (la 'porción de pizza'):\n\n"
                "$$\\boxed{\\,A = \\dfrac{1}{2} r^2 \\theta.\\,}$$\n\n"
                "**Importante.** Estas fórmulas **solo funcionan si $\\theta$ está en radianes**. Si te dan $\\theta$ en grados, **convertir primero**.\n\n"
                "**Origen de la simplicidad.** $s = r \\theta$ es la **definición** del radián: el ángulo de 1 rad subtiende un arco de longitud $r$. Por eso los radianes son el sistema natural — las fórmulas geométricas no llevan factor $\\pi/180$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Arco y sector",
          problema_md="En una circunferencia de radio $10$ m, calculá la longitud de arco y el área del sector que subtiende un ángulo central de $30^\\circ$.",
          pasos=[
              {"accion_md": (
                  "**Convertir $30^\\circ$ a radianes:** $30^\\circ \\cdot \\dfrac{\\pi}{180} = \\dfrac{\\pi}{6}$ rad."
              ),
               "justificacion_md": "Las fórmulas requieren radianes.",
               "es_resultado": False},
              {"accion_md": (
                  "**Arco:** $s = r \\theta = 10 \\cdot \\dfrac{\\pi}{6} = \\dfrac{5 \\pi}{3} \\approx 5{,}24$ m.\n\n"
                  "**Sector:** $A = \\dfrac{1}{2} r^2 \\theta = \\dfrac{1}{2} \\cdot 100 \\cdot \\dfrac{\\pi}{6} = \\dfrac{25 \\pi}{3} \\approx 26{,}18$ m²."
              ),
               "justificacion_md": "Sustitución directa.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué los radianes son 'naturales'.** El radián se define para que la fórmula $s = r \\theta$ "
            "sea exactamente cierta. En grados sería $s = r \\cdot \\theta \\cdot \\pi / 180$, agregando un "
            "factor incómodo. Lo mismo pasa con derivadas: $\\dfrac{d}{dx}\\sin x = \\cos x$ vale **solo** "
            "en radianes. En grados sería $\\dfrac{d}{dx}\\sin x^\\circ = \\dfrac{\\pi}{180} \\cos x^\\circ$ — un horror.\n\n"
            "**Visualizar 1 radián.** Tomá un trozo de cuerda igual al radio del círculo y curvalo sobre el "
            "borde. El ángulo central que cubre es 1 radián, aproximadamente $57^\\circ$ — un poco menos que un "
            "ángulo de $60^\\circ$ (que es $\\pi/3 \\approx 1{,}047$ rad).\n\n"
            "**Reconocer ángulos coterminales rápido.** $750^\\circ - 360^\\circ - 360^\\circ = 30^\\circ$, así "
            "$750^\\circ$ es coterminal con $30^\\circ$. Para mantener un ángulo en $[0^\\circ, 360^\\circ)$, "
            "restar (o sumar) $360^\\circ$ las veces necesarias."
        )),

        fig(
            "Circunferencia con centro en el origen y radio r. "
            "Un ángulo central θ marcado desde el eje x positivo en sentido antihorario (en color teal #06b6d4). "
            "Arco subtendido resaltado en color ámbar #f59e0b con la etiqueta 's = rθ'. "
            "Sector circular sombreado en gris claro con etiqueta 'A = (1/2) r² θ'. "
            "Etiqueta 'θ en radianes' destacada. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\pi/4$ rad equivale a:",
                  "opciones_md": [
                      "$30^\\circ$",
                      "**$45^\\circ$**",
                      "$60^\\circ$",
                      "$90^\\circ$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\pi$ rad = $180^\\circ$.",
                  "explicacion_md": "$\\pi/4 \\cdot 180/\\pi = 45^\\circ$.",
              },
              {
                  "enunciado_md": "$240^\\circ$ es coterminal con:",
                  "opciones_md": [
                      "$60^\\circ$",
                      "**$-120^\\circ$**",
                      "$-240^\\circ$",
                      "$120^\\circ$",
                  ],
                  "correcta": "B",
                  "pista_md": "Coterminales difieren en un múltiplo de $360^\\circ$.",
                  "explicacion_md": "$240^\\circ - 360^\\circ = -120^\\circ$.",
              },
              {
                  "enunciado_md": "Longitud del arco con $r = 6$ y $\\theta = \\pi/3$ rad:",
                  "opciones_md": [
                      "$\\pi$",
                      "**$2 \\pi$**",
                      "$6 \\pi$",
                      "$3 \\pi$",
                  ],
                  "correcta": "B",
                  "pista_md": "$s = r \\theta$.",
                  "explicacion_md": "$s = 6 \\cdot \\pi/3 = 2 \\pi$.",
              },
          ]),

        ej(
            "Conversión",
            "Convertí $135^\\circ$ a radianes y $7\\pi/6$ a grados.",
            ["Multiplicar por el factor adecuado."],
            (
                "$135^\\circ \\cdot \\pi/180 = 3\\pi/4$ rad. $7\\pi/6 \\cdot 180/\\pi = 210^\\circ$."
            ),
        ),

        ej(
            "Coterminal en $[0, 360^\\circ)$",
            "Halla el ángulo coterminal de $920^\\circ$ que esté en $[0^\\circ, 360^\\circ)$.",
            ["Restar $360^\\circ$ las veces necesarias."],
            (
                "$920 - 360 = 560$, $560 - 360 = 200$. **$200^\\circ$.**"
            ),
        ),

        ej(
            "Sector circular",
            "Una pizza de radio $20$ cm se corta en $8$ porciones iguales. Calcula el área de una porción.",
            ["Cada porción tiene ángulo $2\\pi/8 = \\pi/4$ rad."],
            (
                "$A = (1/2) \\cdot 20^2 \\cdot \\pi/4 = 200 \\cdot \\pi/4 = 50 \\pi \\approx 157$ cm²."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Usar grados en $s = r \\theta$ o $A = (1/2) r^2 \\theta$.** Las fórmulas requieren **radianes**.",
              "**Confundir arco con cuerda.** Arco es la parte curva; cuerda es el segmento recto.",
              "**Olvidar que ángulos negativos van en sentido horario.**",
              "**Convertir mal multiplicando por $180/\\pi$ cuando va $\\pi/180$.** Truco: si convertís de grados a radianes, deberías obtener un número con $\\pi$.",
              "**Pensar que coterminales son el mismo ángulo.** Tienen el mismo lado terminal pero medidas distintas.",
          ]),

        b("resumen",
          puntos_md=[
              "**Grados y radianes:** $180^\\circ = \\pi$ rad. Conversión multiplicando por $\\pi/180$ o $180/\\pi$.",
              "**Ángulos especiales:** memorizar $30^\\circ, 45^\\circ, 60^\\circ$ y sus equivalentes.",
              "**Coterminales:** difieren en múltiplo de $360^\\circ$. Complementarios suman $90^\\circ$. Suplementarios suman $180^\\circ$.",
              "**Longitud de arco:** $s = r \\theta$ (radianes). **Sector:** $A = (1/2) r^2 \\theta$.",
              "**Próxima lección:** triángulos rectángulos y razones trigonométricas básicas.",
          ]),
    ]
    return {
        "id": "lec-prec-5-1-angulos-medidas",
        "title": "Ángulos y medidas",
        "description": "Medida de ángulos en grados y radianes, conversión entre sistemas, ángulos coterminales, complementarios y suplementarios. Longitud de arco y área de sector circular.",
        "blocks": blocks,
        "duration_minutes": 45,
        "order": 1,
    }


# =====================================================================
# Triángulos
# =====================================================================
def lesson_triangulos():
    blocks = [
        b("texto", body_md=(
            "La trigonometría nació estudiando **triángulos rectángulos** — y ese caso simple permite "
            "introducir las **seis razones trigonométricas** básicas que después extenderemos a cualquier ángulo "
            "(con el círculo unitario).\n\n"
            "En un triángulo rectángulo, los **catetos** son los dos lados que forman el ángulo recto, y la "
            "**hipotenusa** es el lado opuesto al ángulo recto (siempre el más largo). Para cualquier ángulo "
            "agudo $\\alpha$ (uno de los no rectos), distinguimos:\n\n"
            "- **Cateto opuesto** (a $\\alpha$).\n"
            "- **Cateto adyacente** (al lado de $\\alpha$, que no es la hipotenusa).\n\n"
            "**Al terminar:**\n\n"
            "- Aplicás las razones $\\sin, \\cos, \\tan$ y sus recíprocas $\\csc, \\sec, \\cot$.\n"
            "- Resolvés un triángulo rectángulo a partir de dos elementos.\n"
            "- Usás la mnemotecnia **SOH-CAH-TOA**.\n"
            "- Conocés los valores exactos para $30^\\circ, 45^\\circ, 60^\\circ$."
        )),

        formulas(
            titulo="Las seis razones trigonométricas",
            body=(
                "Para un ángulo agudo $\\alpha$ en un triángulo rectángulo:\n\n"
                "**Tres principales (SOH-CAH-TOA):**\n\n"
                "$$\\sin \\alpha = \\dfrac{\\text{opuesto}}{\\text{hipotenusa}}, \\qquad \\cos \\alpha = \\dfrac{\\text{adyacente}}{\\text{hipotenusa}}, \\qquad \\tan \\alpha = \\dfrac{\\text{opuesto}}{\\text{adyacente}}.$$\n\n"
                "**Tres recíprocas:**\n\n"
                "$$\\csc \\alpha = \\dfrac{1}{\\sin \\alpha}, \\qquad \\sec \\alpha = \\dfrac{1}{\\cos \\alpha}, \\qquad \\cot \\alpha = \\dfrac{1}{\\tan \\alpha}.$$\n\n"
                "**Mnemotecnia SOH-CAH-TOA:**\n\n"
                "- **S**ine = **O**pposite/**H**ypotenuse.\n"
                "- **C**osine = **A**djacent/**H**ypotenuse.\n"
                "- **T**angent = **O**pposite/**A**djacent.\n\n"
                "**Cuidado.** Al cambiar de ángulo agudo (por ejemplo de $\\alpha$ a $\\beta$, el otro), los catetos 'opuesto' y 'adyacente' **se intercambian**. La hipotenusa siempre es la misma."
            ),
        ),

        formulas(
            titulo="Identidades complementarias",
            body=(
                "En un triángulo rectángulo $\\alpha + \\beta = 90^\\circ$, así $\\beta = 90^\\circ - \\alpha$. "
                "Las razones de $\\beta$ son las 'co-' de $\\alpha$:\n\n"
                "$$\\sin(90^\\circ - \\alpha) = \\cos \\alpha, \\qquad \\cos(90^\\circ - \\alpha) = \\sin \\alpha,$$\n"
                "$$\\tan(90^\\circ - \\alpha) = \\cot \\alpha, \\qquad \\cot(90^\\circ - \\alpha) = \\tan \\alpha,$$\n"
                "$$\\sec(90^\\circ - \\alpha) = \\csc \\alpha, \\qquad \\csc(90^\\circ - \\alpha) = \\sec \\alpha.$$\n\n"
                "**De ahí el prefijo 'co-':** **co**seno = **co**mplementario del seno. **co**tangente = complementaria de tangente, etc."
            ),
        ),

        formulas(
            titulo="Valores exactos en ángulos especiales",
            body=(
                "**Estos valores hay que tener memorizados** — aparecen una y otra vez:\n\n"
                "| $\\alpha$ | $\\sin \\alpha$ | $\\cos \\alpha$ | $\\tan \\alpha$ |\n"
                "|---|---|---|---|\n"
                "| $30^\\circ$ ($\\pi/6$) | $\\dfrac{1}{2}$ | $\\dfrac{\\sqrt{3}}{2}$ | $\\dfrac{\\sqrt{3}}{3} = \\dfrac{1}{\\sqrt{3}}$ |\n"
                "| $45^\\circ$ ($\\pi/4$) | $\\dfrac{\\sqrt{2}}{2}$ | $\\dfrac{\\sqrt{2}}{2}$ | $1$ |\n"
                "| $60^\\circ$ ($\\pi/3$) | $\\dfrac{\\sqrt{3}}{2}$ | $\\dfrac{1}{2}$ | $\\sqrt{3}$ |\n\n"
                "**De dónde salen.**\n\n"
                "- **45-45-90** (medio cuadrado): catetos iguales 1, hipotenusa $\\sqrt{2}$.\n"
                "- **30-60-90** (medio equilátero de lado 2): catetos $1$ (opuesto a $30^\\circ$) y $\\sqrt{3}$ (opuesto a $60^\\circ$), hipotenusa 2.\n\n"
                "**Truco mnemotécnico** para $\\sin$: $\\sin 0 = \\sqrt{0}/2, \\sin 30 = \\sqrt{1}/2, \\sin 45 = \\sqrt{2}/2, \\sin 60 = \\sqrt{3}/2, \\sin 90 = \\sqrt{4}/2$. Cosenos en orden inverso."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Resolver triángulo rectángulo",
          problema_md="En un triángulo rectángulo, el ángulo $\\alpha = 30^\\circ$ y la hipotenusa mide 12 m. Halla los catetos.",
          pasos=[
              {"accion_md": (
                  "**Cateto opuesto a $\\alpha$:** $a = c \\sin \\alpha = 12 \\sin 30^\\circ = 12 \\cdot 1/2 = 6$ m."
              ),
               "justificacion_md": "Despejar de $\\sin \\alpha = a/c$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cateto adyacente a $\\alpha$:** $b = c \\cos \\alpha = 12 \\cos 30^\\circ = 12 \\cdot \\sqrt{3}/2 = 6\\sqrt{3} \\approx 10{,}39$ m."
              ),
               "justificacion_md": "Análogo con coseno.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificación con Pitágoras:** $6^2 + (6\\sqrt{3})^2 = 36 + 108 = 144 = 12^2$ ✓."
              ),
               "justificacion_md": "Buena práctica de control.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Hallar ángulo desde lados",
          problema_md="Un triángulo rectángulo tiene catetos 3 y 4. Halla la hipotenusa, el seno, coseno y tangente del ángulo opuesto al cateto de 3.",
          pasos=[
              {"accion_md": (
                  "**Hipotenusa por Pitágoras:** $c = \\sqrt{3^2 + 4^2} = \\sqrt{25} = 5$. Es el famoso triángulo 3-4-5."
              ),
               "justificacion_md": "Triángulo pitagórico fundamental.",
               "es_resultado": False},
              {"accion_md": (
                  "**Razones para el ángulo $\\alpha$ opuesto al cateto 3:**\n\n"
                  "- $\\sin \\alpha = 3/5$ (opuesto/hipotenusa).\n"
                  "- $\\cos \\alpha = 4/5$ (adyacente/hipotenusa).\n"
                  "- $\\tan \\alpha = 3/4$ (opuesto/adyacente).\n\n"
                  "**Ángulo:** $\\alpha = \\arcsin(3/5) \\approx 36{,}87^\\circ$."
              ),
               "justificacion_md": "Los valores no son 'exactos' (no es uno de los ángulos especiales), pero las razones sí.",
               "es_resultado": True},
          ]),

        fig(
            "Triángulo rectángulo en el plano. Ángulo recto en el vértice inferior derecho. "
            "Ángulo agudo α en el vértice inferior izquierdo. "
            "Lados etiquetados: 'cateto opuesto a α' (el lado vertical, color teal #06b6d4), "
            "'cateto adyacente a α' (el lado horizontal inferior, color teal), "
            "'hipotenusa' (el lado inclinado, color ámbar #f59e0b). "
            "Texto a la derecha con las tres razones SOH-CAH-TOA. " + STYLE
        ),

        b("intuicion", body_md=(
            "**Por qué las razones dependen solo del ángulo.** Dos triángulos rectángulos con el mismo ángulo "
            "$\\alpha$ son **semejantes** (proporcionales). Las razones entre sus lados son **iguales** sin "
            "importar el tamaño. Por eso $\\sin 30^\\circ = 1/2$ vale para cualquier triángulo con ese ángulo: "
            "sea de juguete o de un edificio.\n\n"
            "**Por qué memorizar 30, 45, 60.** Aparecen continuamente y no se calculan con calculadora — son "
            "exactos. Saber que $\\cos 60^\\circ = 1/2$ exactamente (no $0{,}5$ aproximado) es esencial para "
            "trabajar con expresiones algebraicas trigonométricas.\n\n"
            "**Aplicaciones clásicas.** Altura de un edificio (medir su sombra y el ángulo del sol), "
            "navegación (rumbos), arquitectura (pendientes de techos), física (resolver fuerzas en "
            "componentes)."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\sin 30^\\circ = $",
                  "opciones_md": [
                      "$\\sqrt{2}/2$",
                      "**$1/2$**",
                      "$\\sqrt{3}/2$",
                      "$1$",
                  ],
                  "correcta": "B",
                  "pista_md": "Triángulo 30-60-90.",
                  "explicacion_md": "Mitad del cateto corto sobre la hipotenusa de un equilátero.",
              },
              {
                  "enunciado_md": "$\\cos 45^\\circ = $",
                  "opciones_md": [
                      "$1/2$",
                      "**$\\sqrt{2}/2$**",
                      "$\\sqrt{3}/2$",
                      "$1$",
                  ],
                  "correcta": "B",
                  "pista_md": "Triángulo 45-45-90.",
                  "explicacion_md": "Catetos iguales, hipotenusa $\\sqrt{2}$ veces el cateto.",
              },
              {
                  "enunciado_md": "Si $\\sin \\alpha = 3/5$, entonces $\\csc \\alpha = $",
                  "opciones_md": [
                      "$5/3$",
                      "**$5/3$**",
                      "$3/5$",
                      "$4/5$",
                  ],
                  "correcta": "A",
                  "pista_md": "$\\csc = 1/\\sin$.",
                  "explicacion_md": "Recíproco directo.",
              },
          ]),

        ej(
            "Resolver triángulo rectángulo",
            "Un triángulo rectángulo tiene un cateto de 5 m y un ángulo agudo opuesto a él de $40^\\circ$. Halla la hipotenusa.",
            ["$\\sin 40^\\circ = 5/c$."],
            (
                "$c = 5/\\sin 40^\\circ \\approx 5/0{,}643 \\approx 7{,}78$ m."
            ),
        ),

        ej(
            "Razones desde un punto",
            "Un punto $P(8, 6)$ está en el lado terminal de un ángulo $\\alpha$ en posición estándar. Calcula $\\sin \\alpha$ y $\\cos \\alpha$.",
            ["Distancia al origen $r = \\sqrt{x^2 + y^2}$. $\\sin = y/r$, $\\cos = x/r$."],
            (
                "$r = \\sqrt{64 + 36} = 10$. $\\sin \\alpha = 6/10 = 3/5$. $\\cos \\alpha = 8/10 = 4/5$."
            ),
        ),

        ej(
            "Aplicación práctica",
            "Una rampa forma un ángulo de $15^\\circ$ con el suelo y tiene 6 m de largo. ¿Cuánto sube?",
            ["$\\sin 15^\\circ = h/6$."],
            (
                "$h = 6 \\sin 15^\\circ \\approx 6 \\cdot 0{,}2588 \\approx 1{,}55$ m."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir 'opuesto' y 'adyacente'.** Opuesto está enfrente del ángulo; adyacente es el otro cateto.",
              "**Tomar la hipotenusa como cateto.** La hipotenusa siempre es el lado más largo, opuesto al ángulo recto.",
              "**Cambiar de ángulo sin actualizar opuesto/adyacente.** Si pasas de $\\alpha$ a $\\beta$, ambos catetos cambian de rol.",
              "**Aplicar SOH-CAH-TOA fuera del triángulo rectángulo.** Para triángulos generales hay leyes específicas (lección 7).",
              "**Confundir $\\csc$ con $\\sin^{-1}$.** $\\csc = 1/\\sin$ es la recíproca; $\\sin^{-1}$ es la **inversa funcional** (lección 6).",
          ]),

        b("resumen",
          puntos_md=[
              "**Triángulo rectángulo:** dos catetos y una hipotenusa.",
              "**SOH-CAH-TOA:** $\\sin = O/H, \\cos = A/H, \\tan = O/A$.",
              "**Recíprocas:** $\\csc, \\sec, \\cot$.",
              "**Identidades complementarias:** $\\sin(90 - \\alpha) = \\cos \\alpha$, etc.",
              "**Valores exactos** en $30, 45, 60$ se memorizan.",
              "**Próxima lección:** generalizar al círculo unitario para ángulos cualquiera.",
          ]),
    ]
    return {
        "id": "lec-prec-5-2-triangulos",
        "title": "Triángulos",
        "description": "Razones trigonométricas en triángulos rectángulos: seno, coseno, tangente y sus recíprocas (SOH-CAH-TOA). Identidades complementarias. Valores exactos para 30°, 45° y 60°. Resolución de triángulos rectángulos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 2,
    }


# =====================================================================
# Círculo unitario
# =====================================================================
def lesson_circulo_unitario():
    blocks = [
        b("texto", body_md=(
            "El triángulo rectángulo solo permite definir trigonometría para **ángulos agudos** ($0$ a $90^\\circ$). "
            "Para extender las funciones a **cualquier ángulo** (incluso negativos o mayores a $360^\\circ$), "
            "se usa el **círculo unitario**.\n\n"
            "**Definición clave.** El círculo unitario es la circunferencia $x^2 + y^2 = 1$ (centro en origen, radio 1). "
            "Para un ángulo $\\theta$ en posición estándar, su **lado terminal** corta al círculo en un punto "
            "$P(x, y)$. Entonces:\n\n"
            "$$\\boxed{\\,\\cos \\theta = x, \\qquad \\sin \\theta = y.\\,}$$\n\n"
            "Esto **generaliza** las razones trigonométricas: para cualquier $\\theta$ (incluso fuera de $[0, 90^\\circ]$), $\\sin$ y $\\cos$ están bien definidos como coordenadas de un punto en el círculo unitario.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces la **definición** de $\\sin, \\cos$ vía círculo unitario.\n"
            "- Aplicás los **signos por cuadrante** (Todos, Seno, Tangente, Coseno).\n"
            "- Calculás funciones trigonométricas en cualquier ángulo usando **ángulo de referencia**.\n"
            "- Conoces la **identidad pitagórica** fundamental."
        )),

        b("definicion",
          titulo="Definición vía círculo unitario",
          body_md=(
              "Sea $\\theta$ un ángulo en posición estándar (vértice en origen, lado inicial sobre eje $x$ positivo). "
              "Sea $P(x, y)$ el punto donde el **lado terminal** de $\\theta$ corta al círculo unitario.\n\n"
              "**Definimos:**\n\n"
              "$$\\sin \\theta = y, \\qquad \\cos \\theta = x.$$\n\n"
              "**Las otras cuatro:**\n\n"
              "$$\\tan \\theta = \\dfrac{\\sin \\theta}{\\cos \\theta} = \\dfrac{y}{x} \\quad (x \\neq 0),$$\n"
              "$$\\cot \\theta = \\dfrac{\\cos \\theta}{\\sin \\theta} = \\dfrac{x}{y} \\quad (y \\neq 0),$$\n"
              "$$\\sec \\theta = \\dfrac{1}{\\cos \\theta} = \\dfrac{1}{x}, \\qquad \\csc \\theta = \\dfrac{1}{\\sin \\theta} = \\dfrac{1}{y}.$$\n\n"
              "**Coherencia con el triángulo rectángulo.** Para $\\theta$ agudo, el triángulo rectángulo formado tiene hipotenusa 1, cateto opuesto $y$ y cateto adyacente $x$. Las razones coinciden con SOH-CAH-TOA."
          )),

        formulas(
            titulo="Identidad pitagórica",
            body=(
                "Como $P(x, y) = (\\cos \\theta, \\sin \\theta)$ está en el círculo unitario, satisface $x^2 + y^2 = 1$. Sustituyendo:\n\n"
                "$$\\boxed{\\,\\sin^2 \\theta + \\cos^2 \\theta = 1.\\,}$$\n\n"
                "Esta es la **identidad fundamental** de la trigonometría. **Vale para todo $\\theta$.**\n\n"
                "**Variantes (dividiendo por $\\cos^2 \\theta$ o $\\sin^2 \\theta$):**\n\n"
                "$$1 + \\tan^2 \\theta = \\sec^2 \\theta.$$\n\n"
                "$$1 + \\cot^2 \\theta = \\csc^2 \\theta.$$\n\n"
                "**Aplicación clave.** Si conocés una función trigonométrica de $\\theta$ y el cuadrante, "
                "podés calcular **todas las demás** usando estas identidades."
            ),
        ),

        formulas(
            titulo="Signos por cuadrante",
            body=(
                "El signo de $\\sin \\theta = y$ y $\\cos \\theta = x$ depende del **cuadrante** del lado terminal:\n\n"
                "| Cuadrante | $\\sin$ | $\\cos$ | $\\tan$ | Positivas |\n"
                "|---|---|---|---|---|\n"
                "| **I** | $+$ | $+$ | $+$ | **Todas** |\n"
                "| **II** | $+$ | $-$ | $-$ | **Seno** (y csc) |\n"
                "| **III** | $-$ | $-$ | $+$ | **Tangente** (y cot) |\n"
                "| **IV** | $-$ | $+$ | $-$ | **Coseno** (y sec) |\n\n"
                "**Mnemotecnia 'TASC':** **T**odas, **A** seno, **S** tangente, **C** oseno (en sentido antihorario desde el cuadrante I).\n\n"
                "Otra versión: **'All Students Take Calculus'** (en inglés), o **'Todos Sabemos Trigonometría con Coraje'**.\n\n"
                "**Las recíprocas tienen el mismo signo que su 'pareja':** $\\csc$ como $\\sin$, $\\sec$ como $\\cos$, $\\cot$ como $\\tan$."
            ),
        ),

        b("definicion",
          titulo="Ángulo de referencia",
          body_md=(
              "El **ángulo de referencia** $\\theta'$ es el ángulo agudo entre el lado terminal de $\\theta$ y el "
              "**eje $x$** (positivo o negativo, lo que esté más cerca).\n\n"
              "**Cómo calcular $\\theta'$ según cuadrante** (con $\\theta$ en $[0, 2\\pi)$):\n\n"
              "- **I:** $\\theta' = \\theta$.\n"
              "- **II:** $\\theta' = \\pi - \\theta$ (o $180^\\circ - \\theta$).\n"
              "- **III:** $\\theta' = \\theta - \\pi$ (o $\\theta - 180^\\circ$).\n"
              "- **IV:** $\\theta' = 2\\pi - \\theta$ (o $360^\\circ - \\theta$).\n\n"
              "**Propiedad clave.** Las funciones trigonométricas en $\\theta$ tienen el **mismo valor absoluto** que en $\\theta'$, solo cambia el signo según el cuadrante.\n\n"
              "**Procedimiento para evaluar $\\sin \\theta, \\cos \\theta, \\tan \\theta$ en cualquier $\\theta$:**\n\n"
              "1. Reducir $\\theta$ a $[0, 2\\pi)$ (sumar/restar $2\\pi$).\n"
              "2. Identificar cuadrante.\n"
              "3. Calcular ángulo de referencia $\\theta'$.\n"
              "4. Evaluar la función en $\\theta'$ (usar tabla de ángulos especiales si aplica).\n"
              "5. Asignar signo según cuadrante."
          )),

        b("ejemplo_resuelto",
          titulo="Evaluar usando ángulo de referencia",
          problema_md="Calcula $\\sin(7\\pi/6)$, $\\cos(5\\pi/4)$ y $\\tan(11\\pi/3)$.",
          pasos=[
              {"accion_md": (
                  "**$\\sin(7\\pi/6)$.** $7\\pi/6 \\in (\\pi, 3\\pi/2)$ → cuadrante III. Ángulo de referencia: $7\\pi/6 - \\pi = \\pi/6$.\n\n"
                  "$\\sin(\\pi/6) = 1/2$. En III seno es **negativo**. **$\\sin(7\\pi/6) = -1/2$.**"
              ),
               "justificacion_md": "III: solo tan/cot positivas.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\cos(5\\pi/4)$.** $5\\pi/4 \\in (\\pi, 3\\pi/2)$ → cuadrante III. Referencia: $5\\pi/4 - \\pi = \\pi/4$.\n\n"
                  "$\\cos(\\pi/4) = \\sqrt{2}/2$. En III coseno es **negativo**. **$\\cos(5\\pi/4) = -\\sqrt{2}/2$.**"
              ),
               "justificacion_md": "Mismo cuadrante, mismas reglas de signos.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\tan(11\\pi/3)$.** Reducir: $11\\pi/3 - 2\\pi = 11\\pi/3 - 6\\pi/3 = 5\\pi/3$. $5\\pi/3 \\in (3\\pi/2, 2\\pi)$ → cuadrante IV. Referencia: $2\\pi - 5\\pi/3 = \\pi/3$.\n\n"
                  "$\\tan(\\pi/3) = \\sqrt{3}$. En IV tangente es **negativa**. **$\\tan(11\\pi/3) = -\\sqrt{3}$.**"
              ),
               "justificacion_md": "Reducir primero al rango fundamental.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Hallar las restantes funciones",
          problema_md="Si $\\cos t = 3/5$ y $t$ está en cuadrante IV, halla $\\sin t$ y $\\tan t$.",
          pasos=[
              {"accion_md": (
                  "**Identidad pitagórica:** $\\sin^2 t = 1 - \\cos^2 t = 1 - 9/25 = 16/25$. $\\sin t = \\pm 4/5$."
              ),
               "justificacion_md": "Hasta acá hay dos posibilidades.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cuadrante IV → seno negativo.** $\\sin t = -4/5$.\n\n"
                  "$\\tan t = \\sin t / \\cos t = (-4/5)/(3/5) = -4/3$."
              ),
               "justificacion_md": "El cuadrante decide el signo.",
               "es_resultado": True},
          ]),

        fig(
            "Círculo unitario en el plano cartesiano. "
            "Marcado con los cuatro cuadrantes y sus signos: 'I: todas +', 'II: sin +', 'III: tan +', 'IV: cos +'. "
            "Puntos destacados sobre el círculo en ángulos especiales: (1, 0) en 0°, (√3/2, 1/2) en 30°, (√2/2, √2/2) en 45°, (1/2, √3/2) en 60°, (0, 1) en 90°. "
            "Eje x e y etiquetados. Acentos teal #06b6d4 para el círculo y ámbar #f59e0b para los puntos. " + STYLE
        ),

        b("intuicion", body_md=(
            "**Por qué el círculo unitario es la 'definición real'.** En el triángulo rectángulo, $\\sin$ y "
            "$\\cos$ solo tienen sentido para $0 < \\alpha < 90^\\circ$. El círculo unitario los extiende a "
            "**cualquier ángulo** real, manteniendo la coherencia con el triángulo cuando $\\alpha$ es agudo.\n\n"
            "**$\\sin$ y $\\cos$ siempre acotados.** Como $|x|, |y| \\leq 1$ en el círculo unitario:\n\n"
            "$$-1 \\leq \\sin \\theta \\leq 1, \\qquad -1 \\leq \\cos \\theta \\leq 1.$$\n\n"
            "$\\tan, \\cot, \\sec, \\csc$ **no** están acotadas (cuando el denominador se acerca a 0, divergen).\n\n"
            "**Periodicidad.** Sumar $2\\pi$ a $\\theta$ produce el **mismo punto** en el círculo. Por eso "
            "$\\sin(\\theta + 2\\pi) = \\sin \\theta$ y $\\cos(\\theta + 2\\pi) = \\cos \\theta$. Las "
            "funciones trigonométricas son **periódicas con período $2\\pi$** (la tangente con $\\pi$)."
        )),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Si $P(x, y)$ está en el círculo unitario en el ángulo $\\theta$, entonces:",
                  "opciones_md": [
                      "$\\sin \\theta = x$",
                      "**$\\sin \\theta = y$**",
                      "$\\sin \\theta = x + y$",
                      "$\\sin \\theta = x y$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\sin$ es la coordenada vertical.",
                  "explicacion_md": "$y$ = $\\sin$ por definición.",
              },
              {
                  "enunciado_md": "$\\sin^2 \\theta + \\cos^2 \\theta = $",
                  "opciones_md": [
                      "$0$",
                      "**$1$**",
                      "$\\theta$",
                      "$2$",
                  ],
                  "correcta": "B",
                  "pista_md": "Identidad pitagórica.",
                  "explicacion_md": "Por estar en el círculo unitario.",
              },
              {
                  "enunciado_md": "En el cuadrante III:",
                  "opciones_md": [
                      "$\\sin > 0$, $\\cos > 0$",
                      "$\\sin > 0$, $\\cos < 0$",
                      "**$\\sin < 0$, $\\cos < 0$**",
                      "$\\sin < 0$, $\\cos > 0$",
                  ],
                  "correcta": "C",
                  "pista_md": "Tercer cuadrante: $x < 0$ e $y < 0$.",
                  "explicacion_md": "Ambas coordenadas negativas.",
              },
          ]),

        ej(
            "Ángulo de referencia",
            "Halla el ángulo de referencia de $\\theta = 5\\pi/3$.",
            ["Cuadrante IV; restar de $2\\pi$."],
            (
                "$5\\pi/3 \\in $ IV. $\\theta' = 2\\pi - 5\\pi/3 = \\pi/3$."
            ),
        ),

        ej(
            "Identidad",
            "Si $\\sin \\theta = -3/5$ y $\\theta$ está en III, halla $\\cos \\theta$ y $\\tan \\theta$.",
            ["Pitagórica + signos del cuadrante."],
            (
                "$\\cos^2 \\theta = 1 - 9/25 = 16/25$, $\\cos \\theta = \\pm 4/5$. En III $\\cos < 0$: $\\cos \\theta = -4/5$. $\\tan \\theta = (-3/5)/(-4/5) = 3/4$."
            ),
        ),

        ej(
            "Evaluar exacto",
            "Calcula $\\cos(13\\pi/4)$.",
            ["Reducir y aplicar referencia."],
            (
                "$13\\pi/4 - 2\\pi = 13\\pi/4 - 8\\pi/4 = 5\\pi/4 \\in $ III. Referencia: $5\\pi/4 - \\pi = \\pi/4$. $\\cos(\\pi/4) = \\sqrt{2}/2$. En III negativo: $\\cos(13\\pi/4) = -\\sqrt{2}/2$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir coordenadas: $(x, y) = (\\cos \\theta, \\sin \\theta)$**, no al revés.",
              "**Olvidar el signo según cuadrante** al usar ángulo de referencia.",
              "**Pensar que $\\sin$ o $\\cos$ pueden valer más que 1.** Imposible — están acotados por la circunferencia.",
              "**Calcular ángulo de referencia restando del eje $y$.** Siempre se mide al eje $x$ (más cercano).",
              "**Olvidar reducir el ángulo a $[0, 2\\pi)$ antes de identificar cuadrante.**",
          ]),

        b("resumen",
          puntos_md=[
              "**Definición:** $\\sin \\theta = y, \\cos \\theta = x$ en el círculo unitario.",
              "**Identidad pitagórica:** $\\sin^2 + \\cos^2 = 1$. Variantes: $1 + \\tan^2 = \\sec^2$, $1 + \\cot^2 = \\csc^2$.",
              "**Signos:** TASC (Todas-Seno-Tangente-Coseno) por cuadrantes I a IV.",
              "**Ángulo de referencia:** ángulo agudo al eje $x$. Permite reducir cualquier $\\theta$ a un caso conocido.",
              "**Periodicidad:** $\\sin(\\theta + 2\\pi) = \\sin \\theta$, $\\cos(\\theta + 2\\pi) = \\cos \\theta$.",
              "**Próxima lección:** las funciones trigonométricas como funciones de $\\mathbb{R}$ y sus propiedades.",
          ]),
    ]
    return {
        "id": "lec-prec-5-3-circulo-unitario",
        "title": "Círculo unitario",
        "description": "Círculo unitario x² + y² = 1, definición de sin θ = y, cos θ = x, identidad pitagórica fundamental, signos por cuadrante (TASC) y ángulo de referencia para reducir cualquier ángulo a casos conocidos.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 3,
    }


# =====================================================================
# Funciones trigonométricas
# =====================================================================
def lesson_funciones_trigonometricas():
    blocks = [
        b("texto", body_md=(
            "Esta lección consolida las **seis funciones trigonométricas** como funciones reales con dominio "
            "y rango bien definidos, sus identidades fundamentales y sus simetrías (paridad).\n\n"
            "Las **seis funciones** son: $\\sin, \\cos, \\tan, \\cot, \\sec, \\csc$. Las dos primeras son las "
            "fundamentales (definidas para todo $\\theta$); las otras cuatro se construyen como cocientes y "
            "tienen restricciones de dominio donde sus denominadores se anulan.\n\n"
            "**Al terminar:**\n\n"
            "- Conoces el **dominio y rango** de cada función trigonométrica.\n"
            "- Aplicás las **identidades pitagóricas** y de cociente con fluidez.\n"
            "- Distinguís funciones **pares** ($\\cos, \\sec$) e **impares** ($\\sin, \\tan, \\cot, \\csc$).\n"
            "- Calculás las seis funciones a partir de una de ellas y el cuadrante."
        )),

        b("definicion",
          titulo="Las seis funciones trigonométricas",
          body_md=(
              "Para todo $\\theta \\in \\mathbb{R}$ donde estén definidas:\n\n"
              "$$\\sin \\theta, \\quad \\cos \\theta \\quad \\text{(definidas en todo } \\mathbb{R}\\text{)}.$$\n\n"
              "$$\\tan \\theta = \\dfrac{\\sin \\theta}{\\cos \\theta}, \\quad \\cot \\theta = \\dfrac{\\cos \\theta}{\\sin \\theta},$$\n\n"
              "$$\\sec \\theta = \\dfrac{1}{\\cos \\theta}, \\quad \\csc \\theta = \\dfrac{1}{\\sin \\theta}.$$\n\n"
              "**Dominios y rangos:**\n\n"
              "| Función | Dominio | Rango |\n"
              "|---|---|---|\n"
              "| $\\sin$ | $\\mathbb{R}$ | $[-1, 1]$ |\n"
              "| $\\cos$ | $\\mathbb{R}$ | $[-1, 1]$ |\n"
              "| $\\tan$ | $\\mathbb{R} \\setminus \\{\\pi/2 + n \\pi\\}$ | $\\mathbb{R}$ |\n"
              "| $\\cot$ | $\\mathbb{R} \\setminus \\{n \\pi\\}$ | $\\mathbb{R}$ |\n"
              "| $\\sec$ | $\\mathbb{R} \\setminus \\{\\pi/2 + n \\pi\\}$ | $(-\\infty, -1] \\cup [1, +\\infty)$ |\n"
              "| $\\csc$ | $\\mathbb{R} \\setminus \\{n \\pi\\}$ | $(-\\infty, -1] \\cup [1, +\\infty)$ |\n\n"
              "**Restricciones.** $\\tan$ y $\\sec$ se indefinen donde $\\cos = 0$ ($\\pi/2, 3\\pi/2, \\ldots$). "
              "$\\cot$ y $\\csc$, donde $\\sin = 0$ ($0, \\pi, 2\\pi, \\ldots$)."
          )),

        formulas(
            titulo="Identidades fundamentales",
            body=(
                "**Identidades de cociente:**\n\n"
                "$$\\tan \\theta = \\dfrac{\\sin \\theta}{\\cos \\theta}, \\qquad \\cot \\theta = \\dfrac{\\cos \\theta}{\\sin \\theta}.$$\n\n"
                "**Identidades recíprocas:**\n\n"
                "$$\\sin \\theta \\cdot \\csc \\theta = 1, \\qquad \\cos \\theta \\cdot \\sec \\theta = 1, \\qquad \\tan \\theta \\cdot \\cot \\theta = 1.$$\n\n"
                "**Identidades pitagóricas:**\n\n"
                "$$\\sin^2 \\theta + \\cos^2 \\theta = 1.$$\n\n"
                "$$1 + \\tan^2 \\theta = \\sec^2 \\theta.$$\n\n"
                "$$1 + \\cot^2 \\theta = \\csc^2 \\theta.$$\n\n"
                "**Paridad:**\n\n"
                "- **Pares:** $\\cos(-\\theta) = \\cos \\theta$, $\\sec(-\\theta) = \\sec \\theta$.\n"
                "- **Impares:** $\\sin(-\\theta) = -\\sin \\theta$, $\\tan(-\\theta) = -\\tan \\theta$, $\\cot(-\\theta) = -\\cot \\theta$, $\\csc(-\\theta) = -\\csc \\theta$.\n\n"
                "**Periodicidad.** $\\sin, \\cos, \\sec, \\csc$ tienen **período $2\\pi$**. $\\tan, \\cot$ tienen **período $\\pi$**."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="De una a las seis",
          problema_md="Si $\\sin t = 4/5$ y $t$ está en cuadrante II, halla $\\cos t, \\tan t, \\cot t, \\sec t, \\csc t$.",
          pasos=[
              {"accion_md": (
                  "**Pitagórica.** $\\cos^2 t = 1 - 16/25 = 9/25$, $\\cos t = \\pm 3/5$.\n\n"
                  "**Cuadrante II → coseno negativo:** $\\cos t = -3/5$."
              ),
               "justificacion_md": "Aplicar identidad y signo del cuadrante.",
               "es_resultado": False},
              {"accion_md": (
                  "**Cocientes:** $\\tan t = (4/5)/(-3/5) = -4/3$. $\\cot t = -3/4$."
              ),
               "justificacion_md": "Negativos: en II, $\\tan$ y $\\cot$ son negativos.",
               "es_resultado": False},
              {"accion_md": (
                  "**Recíprocas:** $\\sec t = 1/\\cos t = -5/3$. $\\csc t = 1/\\sin t = 5/4$."
              ),
               "justificacion_md": "Las recíprocas heredan signo.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Verificar identidad",
          problema_md="Demuestra que $\\dfrac{1 - \\cos^2 \\theta}{\\sin \\theta} = \\sin \\theta$ (donde esté definido).",
          pasos=[
              {"accion_md": (
                  "**Numerador.** $1 - \\cos^2 \\theta = \\sin^2 \\theta$ (pitagórica)."
              ),
               "justificacion_md": "Despejar $\\sin^2$ de la identidad.",
               "es_resultado": False},
              {"accion_md": (
                  "**Sustituir:** $\\dfrac{\\sin^2 \\theta}{\\sin \\theta} = \\sin \\theta$. ✓"
              ),
               "justificacion_md": "Cancelar.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué solo necesitás 2 funciones.** $\\sin$ y $\\cos$ son las **fundamentales**: las otras "
            "cuatro se construyen como cocientes o recíprocas. En la práctica del cálculo, casi todo el "
            "trabajo se hace con $\\sin$ y $\\cos$, y se traduce a las otras cuando es necesario.\n\n"
            "**Por qué $\\sin$ es impar y $\\cos$ es par.** Geométricamente: reflejar un punto $(x, y)$ del "
            "círculo unitario respecto al eje $x$ da $(x, -y)$. La coordenada $x = \\cos$ no cambia (par); "
            "la $y = \\sin$ cambia de signo (impar). Las gráficas reflejan esta simetría: $\\cos$ es simétrica "
            "respecto al eje $y$, $\\sin$ respecto al origen.\n\n"
            "**Por qué $\\tan$ tiene período $\\pi$ (no $2\\pi$).** $\\tan(\\theta + \\pi) = \\sin(\\theta + \\pi) / \\cos(\\theta + \\pi) = (-\\sin \\theta) / (-\\cos \\theta) = \\sin \\theta / \\cos \\theta = \\tan \\theta$. Los signos se cancelan."
        )),

        fig(
            "Las 6 funciones trigonométricas en el círculo unitario. "
            "Círculo unitario con un ángulo θ marcado. "
            "El punto P = (cos θ, sin θ) destacado en color teal #06b6d4. "
            "Segmentos auxiliares: el segmento horizontal de longitud cos θ (eje x), el vertical de longitud sin θ (perpendicular al eje x desde P). "
            "Las otras 4 funciones indicadas con sus interpretaciones geométricas: tan θ como segmento tangente al círculo en (1,0), sec θ como segmento desde el origen al punto donde la tangente corta al eje x, etc. "
            "Etiquetas claras de cada función. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\tan(-\\theta) = $",
                  "opciones_md": [
                      "$\\tan \\theta$",
                      "**$-\\tan \\theta$**",
                      "$\\cot \\theta$",
                      "$1 - \\tan \\theta$",
                  ],
                  "correcta": "B",
                  "pista_md": "Tangente es función impar.",
                  "explicacion_md": "$\\tan = \\sin/\\cos$, $\\sin$ impar y $\\cos$ par.",
              },
              {
                  "enunciado_md": "$1 + \\tan^2 \\theta = $",
                  "opciones_md": [
                      "$\\sin^2 \\theta$",
                      "$\\cos^2 \\theta$",
                      "**$\\sec^2 \\theta$**",
                      "$\\csc^2 \\theta$",
                  ],
                  "correcta": "C",
                  "pista_md": "Variante pitagórica.",
                  "explicacion_md": "Dividir $\\sin^2 + \\cos^2 = 1$ por $\\cos^2$.",
              },
              {
                  "enunciado_md": "El período de $\\tan$ es:",
                  "opciones_md": [
                      "$2 \\pi$",
                      "**$\\pi$**",
                      "$\\pi/2$",
                      "$4 \\pi$",
                  ],
                  "correcta": "B",
                  "pista_md": "Más corto que el de $\\sin/\\cos$.",
                  "explicacion_md": "$\\tan$ se repite cada $\\pi$ por la cancelación de signos.",
              },
          ]),

        ej(
            "Calcular las seis",
            "Si $\\cos t = -12/13$ y $t$ en cuadrante III, halla las seis funciones.",
            ["Pitagórica + signos del cuadrante."],
            (
                "$\\sin^2 t = 1 - 144/169 = 25/169$, $\\sin t = -5/13$ (III, negativo). "
                "$\\tan t = (-5/13)/(-12/13) = 5/12$. $\\cot t = 12/5$. $\\sec t = -13/12$. $\\csc t = -13/5$."
            ),
        ),

        ej(
            "Verificar identidad",
            "Demuestra que $\\sec^2 \\theta - \\tan^2 \\theta = 1$.",
            ["Variante pitagórica."],
            (
                "Por la pitagórica $1 + \\tan^2 \\theta = \\sec^2 \\theta$, despejando $\\sec^2 \\theta - \\tan^2 \\theta = 1$. ✓"
            ),
        ),

        ej(
            "Simplificar",
            "Simplifica $(\\sin \\theta + \\cos \\theta)^2 + (\\sin \\theta - \\cos \\theta)^2$.",
            ["Expandir y usar pitagórica."],
            (
                "$(\\sin^2 + 2 \\sin \\cos + \\cos^2) + (\\sin^2 - 2 \\sin \\cos + \\cos^2) = 2 \\sin^2 + 2 \\cos^2 = 2$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Pensar que $\\sin^2 \\theta$ significa $\\sin(\\theta^2)$.** Significa $(\\sin \\theta)^2$.",
              "**Confundir $\\csc$ con $\\sin^{-1}$.** $\\csc = 1/\\sin$ recíproco; $\\sin^{-1}$ inverso (lección 6).",
              "**Olvidar las restricciones del dominio** de tan, cot, sec, csc.",
              "**Pensar que toda función trig es impar.** $\\cos$ y $\\sec$ son **pares**.",
              "**Aplicar la pitagórica de memoria sin signo.** $\\cos = \\pm \\sqrt{1 - \\sin^2}$ — el signo lo decide el cuadrante.",
          ]),

        b("resumen",
          puntos_md=[
              "**6 funciones:** $\\sin, \\cos$ definidas en $\\mathbb{R}$ con rango $[-1, 1]$; las otras 4 con restricciones.",
              "**Identidades:** pitagóricas, cociente y recíprocas.",
              "**Paridad:** $\\cos, \\sec$ pares; $\\sin, \\tan, \\cot, \\csc$ impares.",
              "**Periodicidad:** $\\sin, \\cos, \\sec, \\csc$ con período $2\\pi$. $\\tan, \\cot$ con período $\\pi$.",
              "**De una se obtienen todas** combinando identidades y signos del cuadrante.",
              "**Próxima lección:** las gráficas de estas funciones y sus transformaciones.",
          ]),
    ]
    return {
        "id": "lec-prec-5-4-funciones-trigonometricas",
        "title": "Funciones trigonométricas",
        "description": "Las 6 funciones trigonométricas como funciones reales: dominios, rangos, identidades pitagóricas y de cociente, paridad y periodicidad. Cálculo de las 6 a partir de una.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 4,
    }


# =====================================================================
# Gráficas trigonométricas
# =====================================================================
def lesson_graficas_trigonometricas():
    blocks = [
        b("texto", body_md=(
            "Las funciones trigonométricas tienen gráficas características: **ondulantes y periódicas**. "
            "Saber cómo se ven a memoria y cómo se modifican con **transformaciones** (amplitud, período, "
            "desfase, desplazamiento vertical) es esencial para modelar fenómenos oscilatorios.\n\n"
            "**Aplicaciones:** sonido (ondas sinusoidales), corriente eléctrica alterna, mareas, ciclos "
            "estacionales, vibraciones mecánicas, péndulos, ondas electromagnéticas.\n\n"
            "**Al terminar:**\n\n"
            "- Identificás las gráficas básicas de $\\sin, \\cos, \\tan, \\cot, \\sec, \\csc$.\n"
            "- Calculás **amplitud, período, desfase y desplazamiento vertical** de $A \\sin(B(x - C)) + D$.\n"
            "- Esbozás la gráfica completa de funciones trigonométricas transformadas."
        )),

        b("definicion",
          titulo="Gráficas básicas de seno y coseno",
          body_md=(
              "**$y = \\sin x$:**\n\n"
              "- Dominio $\\mathbb{R}$, rango $[-1, 1]$.\n"
              "- Período $2\\pi$.\n"
              "- Pasa por el origen $(0, 0)$.\n"
              "- Máximos en $x = \\pi/2 + 2 k \\pi$ (valor 1).\n"
              "- Mínimos en $x = 3\\pi/2 + 2 k \\pi$ (valor $-1$).\n"
              "- Ceros en $x = k \\pi$.\n"
              "- **Función impar:** simétrica respecto al origen.\n\n"
              "**$y = \\cos x$:**\n\n"
              "- Mismo dominio, rango y período.\n"
              "- Pasa por $(0, 1)$.\n"
              "- Máximos en $x = 2 k \\pi$.\n"
              "- Mínimos en $x = \\pi + 2 k \\pi$.\n"
              "- Ceros en $x = \\pi/2 + k \\pi$.\n"
              "- **Función par:** simétrica respecto al eje $y$.\n\n"
              "**Relación clave:** $\\cos x = \\sin(x + \\pi/2)$ — el coseno es el seno desplazado $\\pi/2$ a la izquierda."
          )),

        formulas(
            titulo="Transformaciones de seno y coseno",
            body=(
                "Para una función de la forma\n\n"
                "$$y = A \\sin\\bigl(B (x - C)\\bigr) + D \\quad \\text{(o con } \\cos\\text{)},$$\n\n"
                "los parámetros tienen interpretación geométrica:\n\n"
                "- **Amplitud** $|A|$: la mitad de la diferencia entre máximo y mínimo. Estira/comprime verticalmente. Si $A < 0$, además **refleja** sobre el eje $x$.\n"
                "- **Período** $T = \\dfrac{2 \\pi}{|B|}$: distancia para completar un ciclo. $B > 1$ comprime horizontalmente; $B < 1$ estira.\n"
                "- **Desfase** $C$: desplazamiento horizontal. $C > 0$ a la **derecha**, $C < 0$ a la **izquierda**.\n"
                "- **Desplazamiento vertical** $D$: traslada toda la gráfica hacia arriba ($D > 0$) o abajo.\n\n"
                "**Rango resultante:** $[D - |A|, D + |A|]$.\n\n"
                "**Atención.** Si la fórmula es $y = A \\sin(B x - \\phi)$ (sin paréntesis con $C$), reescribir como $y = A \\sin(B(x - \\phi/B))$ para identificar el desfase como $C = \\phi/B$."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Identificar parámetros",
          problema_md="Identifica amplitud, período, desfase y desplazamiento vertical de $y = 3 \\cos(2 x - \\pi/2) + 1$.",
          pasos=[
              {"accion_md": (
                  "**Reescribir** para tener forma $A \\cos(B(x - C)) + D$:\n\n"
                  "$3 \\cos(2 x - \\pi/2) = 3 \\cos(2(x - \\pi/4))$. Así $C = \\pi/4$."
              ),
               "justificacion_md": "Factorizar el coeficiente de $x$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Identificar:** $A = 3$ (amplitud), $B = 2$ (período $T = 2\\pi/2 = \\pi$), $C = \\pi/4$ (desfase a la derecha), $D = 1$.\n\n"
                  "**Rango:** $[1 - 3, 1 + 3] = [-2, 4]$."
              ),
               "justificacion_md": "Lectura directa de la forma estándar.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Esbozar gráfica",
          problema_md="Grafica $y = 2 \\sin(3 x)$.",
          pasos=[
              {"accion_md": (
                  "**Parámetros:** $A = 2$, $B = 3$, $C = D = 0$. Amplitud 2, período $T = 2\\pi/3$, sin desfase, sin desplazamiento vertical."
              ),
               "justificacion_md": "Forma sencilla.",
               "es_resultado": False},
              {"accion_md": (
                  "**Puntos clave** en un período $[0, 2\\pi/3]$:\n\n"
                  "- Inicio $(0, 0)$.\n"
                  "- Máximo $(\\pi/6, 2)$ — a $T/4$.\n"
                  "- Cero $(\\pi/3, 0)$ — a $T/2$.\n"
                  "- Mínimo $(\\pi/2, -2)$ — a $3T/4$.\n"
                  "- Fin $(2\\pi/3, 0)$ — a $T$.\n\n"
                  "Repetir el patrón para más períodos."
              ),
               "justificacion_md": "Las cinco posiciones clave por período.",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Gráficas de tangente y cotangente",
          body_md=(
              "**$y = \\tan x$:**\n\n"
              "- Dominio: $\\mathbb{R} \\setminus \\{\\pi/2 + k \\pi\\}$.\n"
              "- Rango: $\\mathbb{R}$.\n"
              "- **Período $\\pi$** (no $2\\pi$).\n"
              "- **Asíntotas verticales** en $x = \\pi/2 + k \\pi$.\n"
              "- **Estrictamente creciente** en cada intervalo entre asíntotas.\n"
              "- Pasa por el origen, vale 1 en $\\pi/4$.\n\n"
              "**$y = \\cot x$:**\n\n"
              "- Dominio: $\\mathbb{R} \\setminus \\{k \\pi\\}$.\n"
              "- Asíntotas verticales en $x = k \\pi$.\n"
              "- **Estrictamente decreciente** en cada intervalo entre asíntotas.\n\n"
              "**Gráficas de secante y cosecante.** Son las recíprocas. $\\sec x = 1/\\cos x$ tiene asíntotas donde $\\cos = 0$. La gráfica consiste en 'U' alternadas (hacia arriba o abajo) con valor mínimo $|y| = 1$. Análogo para $\\csc$."
          )),

        b("intuicion", body_md=(
            "**Patrón mnemotécnico de seno y coseno.** Empezando en $\\sin 0 = 0$ y subiendo, el seno hace "
            "**'up-down-down-up'**: máximo en $\\pi/2$, cero en $\\pi$, mínimo en $3\\pi/2$, cero en $2\\pi$. "
            "El coseno empieza en $\\cos 0 = 1$ y hace **'down-down-up-up'**: cero en $\\pi/2$, mínimo en $\\pi$, "
            "cero en $3\\pi/2$, máximo en $2\\pi$.\n\n"
            "**Por qué horizontales 'al revés' en período.** $y = \\sin(2 x)$ **comprime** porque ahora un "
            "ciclo se completa cuando $2 x = 2\\pi$, es decir, cuando $x = \\pi$ (la mitad de $2\\pi$). "
            "Coeficiente más grande = ciclo más corto = comprimido.\n\n"
            "**Aplicación a vibraciones.** Un péndulo simple oscilando en pequeñas amplitudes sigue "
            "$x(t) = A \\cos(\\omega t)$ con $\\omega = \\sqrt{g/L}$ (frecuencia angular). Amplitud $A$ = "
            "máxima distancia del equilibrio; $\\omega$ controla la frecuencia. Período $T = 2\\pi/\\omega$ — "
            "el péndulo más corto oscila más rápido."
        )),

        fig(
            "Cuatro gráficas en una grilla 2x2: y = sin x, y = cos x, y = tan x, y = cot x. "
            "Panel superior izquierdo: y = sin x en color teal #06b6d4, mostrando dos períodos con valores marcados en 0, π/2, π, 3π/2, 2π. "
            "Panel superior derecho: y = cos x en color teal, también dos períodos. "
            "Panel inferior izquierdo: y = tan x en color ámbar #f59e0b, con asíntotas verticales en ±π/2 marcadas como líneas punteadas. "
            "Panel inferior derecho: y = cot x en color ámbar, asíntotas en 0 y π. "
            "Cada panel con eje x e y etiquetados, cuadrícula tenue. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "El período de $y = \\sin(4 x)$ es:",
                  "opciones_md": [
                      "$2 \\pi$",
                      "$4 \\pi$",
                      "**$\\pi/2$**",
                      "$8 \\pi$",
                  ],
                  "correcta": "C",
                  "pista_md": "$T = 2\\pi/B$.",
                  "explicacion_md": "$T = 2\\pi/4 = \\pi/2$.",
              },
              {
                  "enunciado_md": "Amplitud y rango de $y = -3 \\cos x + 2$:",
                  "opciones_md": [
                      "$|A| = 3$, rango $[-3, 3]$",
                      "**$|A| = 3$, rango $[-1, 5]$**",
                      "$|A| = -3$, rango $[2, 5]$",
                      "$|A| = 1$, rango $[-1, 1]$",
                  ],
                  "correcta": "B",
                  "pista_md": "Rango $= [D - |A|, D + |A|]$.",
                  "explicacion_md": "$D = 2, |A| = 3$, rango $[2 - 3, 2 + 3] = [-1, 5]$.",
              },
              {
                  "enunciado_md": "$y = \\tan x$ tiene asíntotas verticales en:",
                  "opciones_md": [
                      "$x = k \\pi$",
                      "**$x = \\pi/2 + k \\pi$**",
                      "$x = 0$ solamente",
                      "Ninguna",
                  ],
                  "correcta": "B",
                  "pista_md": "Donde $\\cos = 0$.",
                  "explicacion_md": "Coseno se anula en $\\pi/2 + k \\pi$.",
              },
          ]),

        ej(
            "Identificar parámetros",
            "Halla amplitud, período, desfase y desplazamiento vertical de $y = -2 \\sin(\\pi x - 2 \\pi) + 3$.",
            ["Reescribir factorizando $\\pi$."],
            (
                "$y = -2 \\sin(\\pi(x - 2)) + 3$. Amplitud 2 (con reflexión por el signo $-$), período $T = 2\\pi/\\pi = 2$, desfase $C = 2$ a la derecha, desplazamiento vertical $D = 3$. Rango $[1, 5]$."
            ),
        ),

        ej(
            "Esbozar gráfica",
            "Grafica $y = 4 \\cos(x - \\pi/2)$ en un período.",
            ["Empieza desplazada $\\pi/2$ a la derecha."],
            (
                "Coseno empieza en máximo en $x = 0$, ahora se mueve a $x = \\pi/2$. Máximos en $\\pi/2 + 2 k \\pi$, ceros en $0 + k \\pi$. Amplitud 4. Es equivalente a $y = 4 \\sin x$."
            ),
        ),

        ej(
            "Función con tangente",
            "¿En qué intervalos crece $y = \\tan(2 x)$?",
            ["Período $\\pi/2$, asíntotas en $\\pi/4 + k \\pi/2$."],
            (
                "En cada intervalo $(\\pi/4 + k \\pi/2 - \\pi/4, \\pi/4 + k \\pi/2 + \\pi/4) = (k \\pi/2, \\pi/2 + k\\pi/2)$ pero sin la asíntota: cada subintervalo entre dos asíntotas consecutivas, donde la función va de $-\\infty$ a $+\\infty$ creciendo."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir período con frecuencia.** Período $T = 2\\pi/B$, no $B$.",
              "**Olvidar el desplazamiento vertical $D$ en el rango.** Rango $[D - |A|, D + |A|]$.",
              "**Confundir desfase con la $C$ adentro de $\\sin(B x - C)$.** El verdadero desfase es $C/B$.",
              "**Pensar que tan tiene amplitud.** $\\tan$ no es acotada, no tiene amplitud.",
              "**Dibujar tan continua entre cuadrantes.** Hay asíntotas verticales que cortan la gráfica.",
          ]),

        b("resumen",
          puntos_md=[
              "**$\\sin, \\cos$:** rango $[-1, 1]$, período $2\\pi$. Sin/cos se diferencian en un desfase $\\pi/2$.",
              "**$\\tan, \\cot$:** rango $\\mathbb{R}$, período $\\pi$, asíntotas verticales.",
              "**$A \\sin(B(x - C)) + D$:** amplitud $|A|$, período $2\\pi/|B|$, desfase $C$, desplazamiento vertical $D$.",
              "**Esbozar:** identificar 5 puntos clave por período (inicio, máximo, cero, mínimo, fin).",
              "**Próxima lección:** funciones inversas — encontrar el ángulo a partir de la razón.",
          ]),
    ]
    return {
        "id": "lec-prec-5-5-graficas-trigonometricas",
        "title": "Gráficas trigonométricas",
        "description": "Gráficas de las 6 funciones trigonométricas. Transformaciones de y = A sin(B(x-C)) + D: amplitud, período, desfase y desplazamiento vertical. Esbozo de gráficas con 5 puntos clave por período.",
        "blocks": blocks,
        "duration_minutes": 55,
        "order": 5,
    }


# =====================================================================
# Funciones trigonométricas inversas
# =====================================================================
def lesson_funciones_inversas():
    blocks = [
        b("texto", body_md=(
            "Las funciones trigonométricas **no son inyectivas** en todo $\\mathbb{R}$ (oscilan): por "
            "ejemplo $\\sin 0 = \\sin \\pi = 0$. Por lo tanto **no tienen inversa global**. La solución es "
            "**restringir el dominio** a un intervalo donde sí lo sean, y definir la inversa allí.\n\n"
            "$$\\sin^{-1} x = \\arcsin x, \\qquad \\cos^{-1} x = \\arccos x, \\qquad \\tan^{-1} x = \\arctan x.$$\n\n"
            "**Pregunta operativa.** Dada una razón trigonométrica $r$, ¿cuál es el ángulo que la produce? "
            "$\\arcsin r, \\arccos r, \\arctan r$ devuelven **uno** de los infinitos posibles, según una "
            "convención.\n\n"
            "**Al terminar:**\n\n"
            "- Conocés los **dominios y rangos** restringidos de cada inversa.\n"
            "- Calculás $\\arcsin, \\arccos, \\arctan$ en valores notables.\n"
            "- Aplicás las **propiedades de cancelación** $\\sin(\\arcsin x) = x$, etc.\n"
            "- Resolvés composiciones tipo $\\cos(\\arctan x)$ usando triángulos auxiliares."
        )),

        formulas(
            titulo="Definición e intervalos restringidos",
            body=(
                "Para invertir cada función trigonométrica, restringimos el dominio al intervalo donde es **estrictamente monótona** y **alcanza todos los valores del rango**:\n\n"
                "**$\\arcsin$ (o $\\sin^{-1}$):** inversa de $\\sin$ restringido a $[-\\pi/2, \\pi/2]$ (creciente).\n\n"
                "$$\\arcsin : [-1, 1] \\to [-\\pi/2, \\pi/2].$$\n\n"
                "**$\\arccos$ (o $\\cos^{-1}$):** inversa de $\\cos$ restringido a $[0, \\pi]$ (decreciente).\n\n"
                "$$\\arccos : [-1, 1] \\to [0, \\pi].$$\n\n"
                "**$\\arctan$ (o $\\tan^{-1}$):** inversa de $\\tan$ restringido a $(-\\pi/2, \\pi/2)$ (creciente).\n\n"
                "$$\\arctan : \\mathbb{R} \\to (-\\pi/2, \\pi/2).$$\n\n"
                "**Notación.** $\\sin^{-1}$ es estándar pero **no significa $1/\\sin$** (eso es $\\csc$). Para evitar confusión, muchos prefieren $\\arcsin$.\n\n"
                "**Identidad útil.** $\\arcsin x + \\arccos x = \\pi/2$ para $x \\in [-1, 1]$."
            ),
        ),

        formulas(
            titulo="Propiedades de cancelación",
            body=(
                "**Cancelación funcionando 'en el rango':**\n\n"
                "$$\\sin(\\arcsin x) = x \\quad \\text{para } x \\in [-1, 1].$$\n"
                "$$\\cos(\\arccos x) = x \\quad \\text{para } x \\in [-1, 1].$$\n"
                "$$\\tan(\\arctan x) = x \\quad \\text{para todo } x \\in \\mathbb{R}.$$\n\n"
                "**Cancelación 'en el dominio restringido':**\n\n"
                "$$\\arcsin(\\sin y) = y \\quad \\text{para } y \\in [-\\pi/2, \\pi/2].$$\n"
                "$$\\arccos(\\cos y) = y \\quad \\text{para } y \\in [0, \\pi].$$\n"
                "$$\\arctan(\\tan y) = y \\quad \\text{para } y \\in (-\\pi/2, \\pi/2).$$\n\n"
                "**Atención.** Si $y$ está fuera del rango restringido, no se cancela directamente. Por ejemplo: $\\arcsin(\\sin(2\\pi)) = 0$, no $2\\pi$, porque $2\\pi \\notin [-\\pi/2, \\pi/2]$.\n\n"
                "**Paridad:** $\\arcsin(-x) = -\\arcsin x$, $\\arctan(-x) = -\\arctan x$ (impares). $\\arccos(-x) = \\pi - \\arccos x$ (no es impar)."
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Valores notables de inversas",
          problema_md="Calcula $\\arcsin(1/2)$, $\\arccos(0)$, $\\arctan(\\sqrt{3})$, $\\arccos(-\\sqrt{2}/2)$.",
          pasos=[
              {"accion_md": (
                  "**$\\arcsin(1/2)$:** ¿qué ángulo en $[-\\pi/2, \\pi/2]$ tiene seno $1/2$? **$\\pi/6$ ($30^\\circ$).**"
              ),
               "justificacion_md": "Recordar valor exacto en $\\pi/6$.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\arccos(0)$:** ¿qué ángulo en $[0, \\pi]$ tiene coseno $0$? **$\\pi/2$ ($90^\\circ$).**"
              ),
               "justificacion_md": "$\\cos(\\pi/2) = 0$.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\arctan(\\sqrt{3})$:** ¿qué ángulo en $(-\\pi/2, \\pi/2)$ tiene tangente $\\sqrt{3}$? **$\\pi/3$ ($60^\\circ$).**"
              ),
               "justificacion_md": "$\\tan(\\pi/3) = \\sqrt{3}$.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\arccos(-\\sqrt{2}/2)$:** $\\cos$ negativo en cuadrante II del rango $[0, \\pi]$. Referencia: $\\arccos(\\sqrt{2}/2) = \\pi/4$. Resultado: $\\pi - \\pi/4 = 3\\pi/4$."
              ),
               "justificacion_md": "Aplicar $\\arccos(-x) = \\pi - \\arccos x$.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Composición trig-inversa",
          problema_md="Calcula $\\cos(\\arctan 3)$ usando un triángulo auxiliar.",
          pasos=[
              {"accion_md": (
                  "**Sea $\\alpha = \\arctan 3$.** Entonces $\\tan \\alpha = 3$ y $\\alpha \\in (-\\pi/2, \\pi/2)$, así $\\alpha$ está en cuadrante I (porque $\\tan > 0$)."
              ),
               "justificacion_md": "Definir y ubicar.",
               "es_resultado": False},
              {"accion_md": (
                  "**Construir triángulo rectángulo** con $\\tan \\alpha = 3 = 3/1$: cateto opuesto $= 3$, adyacente $= 1$. Hipotenusa $= \\sqrt{1 + 9} = \\sqrt{10}$."
              ),
               "justificacion_md": "Auxilio geométrico para composiciones.",
               "es_resultado": False},
              {"accion_md": (
                  "**$\\cos \\alpha = $ adyacente/hipotenusa** $= 1/\\sqrt{10} = \\sqrt{10}/10$.\n\n"
                  "**$\\cos(\\arctan 3) = \\sqrt{10}/10$.**"
              ),
               "justificacion_md": "Truco general: convertir composiciones en cuestiones de triángulo.",
               "es_resultado": True},
          ]),

        b("intuicion", body_md=(
            "**Por qué hay que restringir el dominio.** $\\sin x = 1/2$ tiene infinitas soluciones: "
            "$\\pi/6, 5\\pi/6, \\pi/6 + 2\\pi, \\ldots$ Si quisiéramos definir $\\arcsin(1/2)$ sin "
            "restricción, **¿cuál de las infinitas soluciones devolvemos?** La convención: la del "
            "intervalo $[-\\pi/2, \\pi/2]$ — el más natural por simetría.\n\n"
            "**Diferencia entre 'inversa' y 'recíproca'.** $\\sin^{-1} x = \\arcsin x$ es la **inversa**: "
            "devuelve un ángulo. $1/\\sin x = \\csc x$ es la **recíproca**: un cociente.\n\n"
            "**Truco para composiciones.** Para evaluar $\\sin(\\arccos x)$, $\\tan(\\arcsin x)$ y "
            "similares: **dibujá un triángulo** con la razón especificada y leé la otra razón. Es la "
            "técnica más rápida y menos propensa a errores."
        )),

        fig(
            "Tres gráficas en una fila: y = arcsin(x), y = arccos(x), y = arctan(x). "
            "Panel izquierdo: arcsin de [-1, 1] a [-π/2, π/2], curva creciente en color teal #06b6d4. "
            "Panel central: arccos de [-1, 1] a [0, π], curva decreciente en color ámbar #f59e0b. "
            "Panel derecho: arctan en todo R con asíntotas horizontales y = ±π/2 (en gris punteado), curva creciente en color púrpura. "
            "Cada panel con eje x e y etiquetados y los rangos marcados. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "$\\arcsin(\\sqrt{2}/2) = $",
                  "opciones_md": [
                      "$\\pi/6$",
                      "**$\\pi/4$**",
                      "$\\pi/3$",
                      "$\\pi/2$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\sin(\\pi/4) = \\sqrt{2}/2$.",
                  "explicacion_md": "Y $\\pi/4 \\in [-\\pi/2, \\pi/2]$ ✓.",
              },
              {
                  "enunciado_md": "Rango de $\\arccos$:",
                  "opciones_md": [
                      "$[-\\pi/2, \\pi/2]$",
                      "**$[0, \\pi]$**",
                      "$(-\\pi/2, \\pi/2)$",
                      "$[-1, 1]$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\cos$ es decreciente en $[0, \\pi]$.",
                  "explicacion_md": "Convención estándar.",
              },
              {
                  "enunciado_md": "$\\arctan(\\tan(3\\pi/4)) = $",
                  "opciones_md": [
                      "$3\\pi/4$",
                      "**$-\\pi/4$**",
                      "$\\pi/4$",
                      "$0$",
                  ],
                  "correcta": "B",
                  "pista_md": "$3\\pi/4 \\notin (-\\pi/2, \\pi/2)$, hay que ajustar.",
                  "explicacion_md": "$\\tan(3\\pi/4) = -1$ y $\\arctan(-1) = -\\pi/4$.",
              },
          ]),

        ej(
            "Cancelación directa",
            "Calcula $\\sin(\\arcsin(0{,}3))$ y $\\arccos(\\cos(\\pi/3))$.",
            ["Verificar que estén en el rango/dominio adecuados."],
            (
                "$\\sin(\\arcsin 0{,}3) = 0{,}3$ (porque $0{,}3 \\in [-1, 1]$). $\\arccos(\\cos(\\pi/3)) = \\pi/3$ (porque $\\pi/3 \\in [0, \\pi]$)."
            ),
        ),

        ej(
            "Composición con triángulo",
            "Calcula $\\sin(\\arccos(2/3))$.",
            ["Triángulo: $\\cos = 2/3$, hallar $\\sin$."],
            (
                "$\\arccos(2/3)$ está en $[0, \\pi]$. Cateto adyacente 2, hipotenusa 3, cateto opuesto $\\sqrt{9 - 4} = \\sqrt{5}$. $\\sin = \\sqrt{5}/3$."
            ),
        ),

        ej(
            "Resolver ecuación con inversa",
            "Resuelve $\\sin x = 0{,}5$ para $x \\in [0, 2\\pi)$.",
            ["Una solución por $\\arcsin$, otra por simetría."],
            (
                "$x = \\arcsin(0{,}5) = \\pi/6$. Por simetría del seno respecto a $\\pi/2$: $x = \\pi - \\pi/6 = 5\\pi/6$. **Soluciones:** $\\pi/6$ y $5\\pi/6$."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Confundir $\\sin^{-1} x$ con $1/\\sin x$.** Inversa vs recíproca.",
              "**Olvidar restringir el dominio:** la inversa de $\\sin$ no está definida fuera de $[-1, 1]$.",
              "**Aplicar cancelación sin verificar el rango/dominio.** $\\arcsin(\\sin x) \\neq x$ en general.",
              "**Pensar que $\\arccos(-x) = -\\arccos(x)$.** **Falso.** $\\arccos$ no es impar; la fórmula correcta es $\\pi - \\arccos x$.",
              "**Dar dos soluciones de $\\arcsin$.** La función inversa devuelve **una** solución (la del rango restringido). Para todas las soluciones de una ecuación, hay que considerar simetría y periodicidad.",
          ]),

        b("resumen",
          puntos_md=[
              "**Restricciones para invertibilidad:** $\\sin$ a $[-\\pi/2, \\pi/2]$, $\\cos$ a $[0, \\pi]$, $\\tan$ a $(-\\pi/2, \\pi/2)$.",
              "**Dominios de inversas:** $\\arcsin, \\arccos$ tienen dominio $[-1, 1]$; $\\arctan$ tiene dominio $\\mathbb{R}$.",
              "**Cancelación** vale solo si el argumento está en el rango/dominio adecuado.",
              "**Composiciones** se evalúan con triángulos auxiliares.",
              "**Próxima lección:** las leyes de senos y cosenos para resolver triángulos no rectángulos.",
          ]),
    ]
    return {
        "id": "lec-prec-5-6-funciones-trigonometricas-inversas",
        "title": "Funciones trigonométricas inversas",
        "description": "Funciones inversas arcsin, arccos, arctan: dominios restringidos y rangos. Propiedades de cancelación con sus restricciones. Evaluación de composiciones trig-inversa usando triángulos auxiliares.",
        "blocks": blocks,
        "duration_minutes": 50,
        "order": 6,
    }


# =====================================================================
# Leyes trigonométricas
# =====================================================================
def lesson_leyes_trigonometricas():
    blocks = [
        b("texto", body_md=(
            "Hasta acá aprendimos a resolver **triángulos rectángulos** (lección 2) usando SOH-CAH-TOA. "
            "Para **triángulos no rectángulos** (oblicuángulos), las razones trigonométricas no se aplican "
            "directamente — pero hay dos generalizaciones poderosas:\n\n"
            "- **Ley de senos:** relaciona los lados con los senos de sus ángulos opuestos.\n"
            "- **Ley de cosenos:** generaliza el teorema de Pitágoras a cualquier triángulo.\n\n"
            "Con estas dos leyes, podemos **resolver cualquier triángulo** (encontrar lados o ángulos faltantes) "
            "dadas tres piezas de información apropiadas.\n\n"
            "**Aplicaciones clásicas:** topografía, navegación, astronomía, balística, diseño arquitectónico.\n\n"
            "**Al terminar:**\n\n"
            "- Aplicás la **ley de senos** en casos ALA, LAA, LLA.\n"
            "- Aplicás la **ley de cosenos** en casos LAL y LLL.\n"
            "- Reconocés y manejás el **caso ambiguo** (LLA), donde puede haber 0, 1 o 2 triángulos.\n"
            "- Calculás el **área** de un triángulo con la fórmula del ángulo y dos lados, o con Herón."
        )),

        formulas(
            titulo="Notación estándar y casos",
            body=(
                "En un triángulo $ABC$, denotamos los lados con la **letra minúscula del vértice opuesto**: lado $a$ opuesto al ángulo $A$, lado $b$ opuesto a $B$, lado $c$ opuesto a $C$.\n\n"
                "**Casos de información dada:**\n\n"
                "| Caso | Datos | Ley a usar |\n"
                "|---|---|---|\n"
                "| **ALA** | dos ángulos y el lado entre ellos | senos |\n"
                "| **LAA** | dos ángulos y un lado no contiguo | senos |\n"
                "| **LLA** | dos lados y un ángulo no contenido | senos (caso ambiguo) |\n"
                "| **LAL** | dos lados y el ángulo entre ellos | cosenos |\n"
                "| **LLL** | tres lados | cosenos |\n\n"
                "**Recordar:** la suma de los ángulos siempre es $180^\\circ$ ($\\pi$ rad), así que con dos ángulos sale el tercero."
            ),
        ),

        formulas(
            titulo="Ley de senos",
            body=(
                "En cualquier triángulo $ABC$:\n\n"
                "$$\\boxed{\\,\\dfrac{a}{\\sin A} = \\dfrac{b}{\\sin B} = \\dfrac{c}{\\sin C}.\\,}$$\n\n"
                "Equivalentemente: $\\dfrac{\\sin A}{a} = \\dfrac{\\sin B}{b} = \\dfrac{\\sin C}{c}$.\n\n"
                "**Interpretación geométrica.** El cociente $a / \\sin A$ es el mismo para los tres pares — y coincide con el **diámetro** de la circunferencia circunscrita al triángulo. Pero para uso operativo, basta saber que los tres cocientes son iguales.\n\n"
                "**Aplicación.** Conociendo dos pares (ángulo, lado opuesto) y otro elemento (ángulo o lado), se despeja el cuarto."
            ),
        ),

        formulas(
            titulo="Ley de cosenos",
            body=(
                "En cualquier triángulo $ABC$:\n\n"
                "$$\\boxed{\\,a^2 = b^2 + c^2 - 2 b c \\cos A.\\,}$$\n\n"
                "Y simétricamente:\n\n"
                "$$b^2 = a^2 + c^2 - 2 a c \\cos B,$$\n\n"
                "$$c^2 = a^2 + b^2 - 2 a b \\cos C.$$\n\n"
                "**Generalización del teorema de Pitágoras:** si $A = 90^\\circ$, $\\cos A = 0$ y queda $a^2 = b^2 + c^2$ (Pitágoras).\n\n"
                "**Para hallar un ángulo dado los tres lados** (caso LLL), despejar:\n\n"
                "$$\\cos A = \\dfrac{b^2 + c^2 - a^2}{2 b c}.$$"
            ),
        ),

        b("ejemplo_resuelto",
          titulo="Ley de senos (ALA)",
          problema_md="En un triángulo $A = 40^\\circ$, $B = 65^\\circ$, $a = 10$. Halla $b$.",
          pasos=[
              {"accion_md": (
                  "**Ley de senos:** $\\dfrac{a}{\\sin A} = \\dfrac{b}{\\sin B} \\Rightarrow \\dfrac{10}{\\sin 40^\\circ} = \\dfrac{b}{\\sin 65^\\circ}$."
              ),
               "justificacion_md": "Conocemos $a, A, B$; queremos $b$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Despejar:** $b = \\dfrac{10 \\sin 65^\\circ}{\\sin 40^\\circ} \\approx \\dfrac{10 \\cdot 0{,}906}{0{,}643} \\approx 14{,}09$."
              ),
               "justificacion_md": "Calcular con sin de los ángulos.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Ley de cosenos (LAL)",
          problema_md="En un triángulo $b = 10$, $c = 7$, $A = 40^\\circ$. Halla $a$.",
          pasos=[
              {"accion_md": (
                  "**Ley de cosenos:** $a^2 = b^2 + c^2 - 2 b c \\cos A = 100 + 49 - 140 \\cos 40^\\circ$."
              ),
               "justificacion_md": "$A$ es el ángulo entre los lados $b$ y $c$; el lado opuesto es $a$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Calcular:** $\\cos 40^\\circ \\approx 0{,}766$. $a^2 = 149 - 140 \\cdot 0{,}766 \\approx 149 - 107{,}3 = 41{,}7$. $a \\approx 6{,}46$."
              ),
               "justificacion_md": "Tomar raíz cuadrada al final.",
               "es_resultado": True},
          ]),

        b("ejemplo_resuelto",
          titulo="Ley de cosenos (LLL)",
          problema_md="En un triángulo $a = 5$, $b = 8$, $c = 12$. Halla $A$.",
          pasos=[
              {"accion_md": (
                  "**Despejar coseno:** $\\cos A = \\dfrac{b^2 + c^2 - a^2}{2 b c} = \\dfrac{64 + 144 - 25}{2 \\cdot 8 \\cdot 12} = \\dfrac{183}{192} \\approx 0{,}953$."
              ),
               "justificacion_md": "Aislar $\\cos A$ de la ley.",
               "es_resultado": False},
              {"accion_md": (
                  "**Aplicar arccos:** $A = \\arccos(0{,}953) \\approx 17{,}6^\\circ$."
              ),
               "justificacion_md": "$A$ resultante es agudo (esperable: $a$ es el lado más corto).",
               "es_resultado": True},
          ]),

        b("definicion",
          titulo="Caso ambiguo (LLA)",
          body_md=(
              "Cuando se conocen dos lados y un ángulo **no contenido entre ellos** (LLA), pueden ocurrir tres escenarios:\n\n"
              "Sea conocido $a, b, A$. Por ley de senos: $\\sin B = \\dfrac{b \\sin A}{a}$.\n\n"
              "**Caso 1 — sin solución:** $\\dfrac{b \\sin A}{a} > 1$ (no existe ángulo con tal seno).\n\n"
              "**Caso 2 — una solución:** $\\dfrac{b \\sin A}{a} = 1$ (ángulo recto $B = 90^\\circ$, único triángulo).\n\n"
              "**Caso 3 — posiblemente dos:** $0 < \\dfrac{b \\sin A}{a} < 1$. Hay dos ángulos posibles:\n\n"
              "- $B_1 = \\arcsin\\left(\\dfrac{b \\sin A}{a}\\right)$ (agudo).\n"
              "- $B_2 = 180^\\circ - B_1$ (obtuso).\n\n"
              "**Ambos son válidos solo si $A + B < 180^\\circ$.** Verificar caso por caso."
          )),

        b("ejemplo_resuelto",
          titulo="Caso ambiguo",
          problema_md="$a = 8, b = 10, A = 30^\\circ$. Resuelve el(los) triángulo(s).",
          pasos=[
              {"accion_md": (
                  "**Ley de senos para $B$:** $\\sin B = \\dfrac{b \\sin A}{a} = \\dfrac{10 \\sin 30^\\circ}{8} = \\dfrac{5}{8} = 0{,}625$."
              ),
               "justificacion_md": "Plantear desde el dato conocido.",
               "es_resultado": False},
              {"accion_md": (
                  "**Dos posibles ángulos:** $B_1 = \\arcsin(0{,}625) \\approx 38{,}68^\\circ$, $B_2 = 180^\\circ - 38{,}68^\\circ = 141{,}32^\\circ$."
              ),
               "justificacion_md": "El seno tiene dos preimágenes en $[0, \\pi]$.",
               "es_resultado": False},
              {"accion_md": (
                  "**Verificar:**\n\n"
                  "- $A + B_1 = 30^\\circ + 38{,}68^\\circ = 68{,}68^\\circ < 180^\\circ$ ✓. $C_1 = 180 - 68{,}68 = 111{,}32^\\circ$.\n"
                  "- $A + B_2 = 30^\\circ + 141{,}32^\\circ = 171{,}32^\\circ < 180^\\circ$ ✓. $C_2 = 180 - 171{,}32 = 8{,}68^\\circ$.\n\n"
                  "**Ambos válidos → dos triángulos.** Los lados $c_1, c_2$ se calculan por ley de senos para cada uno."
              ),
               "justificacion_md": "Caso ambiguo plenamente: dos soluciones distintas.",
               "es_resultado": True},
          ]),

        formulas(
            titulo="Área del triángulo",
            body=(
                "**Dos lados y el ángulo entre ellos:**\n\n"
                "$$\\text{Área} = \\dfrac{1}{2} b c \\sin A = \\dfrac{1}{2} a c \\sin B = \\dfrac{1}{2} a b \\sin C.$$\n\n"
                "**Fórmula de Herón** (los tres lados):\n\n"
                "$$\\text{Área} = \\sqrt{s (s - a)(s - b)(s - c)}, \\quad s = \\dfrac{a + b + c}{2} \\text{ (semiperímetro)}.$$\n\n"
                "Útil cuando se conocen los 3 lados y se quiere área **sin calcular ángulos**."
            ),
        ),

        b("intuicion", body_md=(
            "**Por qué la ley de cosenos es el 'Pitágoras generalizado'.** Tomando un triángulo y bajando "
            "una altura desde un vértice, queda dividido en dos triángulos rectángulos; el teorema de "
            "Pitágoras aplicado a uno de ellos, junto con la definición de coseno en el otro, lleva "
            "directamente a $a^2 = b^2 + c^2 - 2 b c \\cos A$. Cuando $A = 90^\\circ$, $\\cos A = 0$ y "
            "se recupera Pitágoras puro.\n\n"
            "**Cuándo usar cada ley.** Como regla general:\n\n"
            "- Si conoces un par (ángulo, lado opuesto) → **ley de senos**.\n"
            "- Si conoces un ángulo y los dos lados que lo contienen, o los tres lados → **ley de cosenos**.\n\n"
            "**Sobre el caso ambiguo.** Aparece **siempre** que se conocen dos lados y un ángulo no contenido. "
            "Hay que **verificar** si las dos posibles soluciones son geométricamente válidas."
        )),

        fig(
            "Dos triángulos no rectángulos lado a lado, ambos con vértices A, B, C y lados a, b, c. "
            "Triángulo izquierdo etiquetado 'Ley de senos: a/sin A = b/sin B = c/sin C' en color teal #06b6d4. "
            "Triángulo derecho etiquetado 'Ley de cosenos: a² = b² + c² - 2bc cos A' en color ámbar #f59e0b. "
            "En cada uno, marcar uno o dos ángulos y los lados opuestos correspondientes con flechas o subrayado. " + STYLE
        ),

        b("verificacion",
          intro_md="Verifica:",
          preguntas=[
              {
                  "enunciado_md": "Dado el caso LAL, conviene usar:",
                  "opciones_md": [
                      "Ley de senos",
                      "**Ley de cosenos**",
                      "Cualquiera",
                      "Ninguna",
                  ],
                  "correcta": "B",
                  "pista_md": "Tenés un ángulo y los dos lados a su alrededor.",
                  "explicacion_md": "Cosenos: $a^2 = b^2 + c^2 - 2 b c \\cos A$.",
              },
              {
                  "enunciado_md": "El caso ambiguo aparece en:",
                  "opciones_md": [
                      "ALA",
                      "LAL",
                      "**LLA**",
                      "LLL",
                  ],
                  "correcta": "C",
                  "pista_md": "Dos lados y un ángulo no contenido.",
                  "explicacion_md": "Puede haber 0, 1 o 2 triángulos.",
              },
              {
                  "enunciado_md": "Área de un triángulo con $a = 5$, $b = 7$, $C = 30^\\circ$:",
                  "opciones_md": [
                      "$5{,}25$",
                      "**$8{,}75$**",
                      "$17{,}5$",
                      "$35$",
                  ],
                  "correcta": "B",
                  "pista_md": "$\\text{Área} = (1/2) a b \\sin C$.",
                  "explicacion_md": "$(1/2)(5)(7)(0{,}5) = 8{,}75$.",
              },
          ]),

        ej(
            "Senos (LAA)",
            "$A = 50^\\circ, B = 70^\\circ, b = 12$. Halla $a$.",
            ["Aplicar ley de senos."],
            (
                "$a/\\sin 50^\\circ = 12/\\sin 70^\\circ \\Rightarrow a = 12 \\sin 50^\\circ / \\sin 70^\\circ \\approx 12 \\cdot 0{,}766 / 0{,}940 \\approx 9{,}78$."
            ),
        ),

        ej(
            "Cosenos para hallar ángulo",
            "Triángulo con $a = 4, b = 6, c = 8$. Halla $C$.",
            ["Despejar $\\cos C$."],
            (
                "$\\cos C = (16 + 36 - 64)/(2 \\cdot 4 \\cdot 6) = -12/48 = -1/4$. $C = \\arccos(-1/4) \\approx 104{,}48^\\circ$."
            ),
        ),

        ej(
            "Aplicación a navegación",
            "Un barco recorre 150 km en dirección N $25^\\circ$ E, después 80 km en dirección N $60^\\circ$ E. ¿A qué distancia del punto de partida está?",
            ["Triángulo con dos lados y el ángulo intermedio (180° - 35° = 145° entre los dos rumbos)."],
            (
                "Ángulo entre los dos tramos: $180^\\circ - (60^\\circ - 25^\\circ) = 145^\\circ$. Por cosenos: $d^2 = 150^2 + 80^2 - 2 \\cdot 150 \\cdot 80 \\cos 145^\\circ \\approx 22500 + 6400 + 19660 \\approx 48560$. $d \\approx 220{,}4$ km."
            ),
        ),

        b("errores_comunes",
          items_md=[
              "**Aplicar ley de senos al caso LAL** o **ley de cosenos al caso ALA** sin necesidad. Cada caso tiene su ley óptima.",
              "**Olvidar el caso ambiguo en LLA.** Verificar siempre si hay 0, 1 o 2 triángulos.",
              "**Confundir el ángulo opuesto al lado en la fórmula.** $a$ va con $A$, $b$ con $B$, $c$ con $C$.",
              "**Aplicar Pitágoras a un triángulo no rectángulo.** Solo vale cuando hay ángulo recto.",
              "**No verificar la suma de ángulos < 180° en el caso ambiguo.**",
          ]),

        b("resumen",
          puntos_md=[
              "**Ley de senos:** $a/\\sin A = b/\\sin B = c/\\sin C$. Casos ALA, LAA, LLA.",
              "**Ley de cosenos:** $a^2 = b^2 + c^2 - 2 b c \\cos A$. Casos LAL, LLL.",
              "**Caso ambiguo (LLA):** 0, 1 o 2 triángulos; verificar suma de ángulos < 180°.",
              "**Área:** $(1/2) a b \\sin C$ o Herón con los 3 lados.",
              "**Cierre del capítulo:** dominamos toda la trigonometría — ángulos, triángulos rectángulos y oblicuángulos, círculo unitario, las 6 funciones, sus gráficas e inversas.",
              "**Próximo capítulo:** identidades trigonométricas avanzadas y ecuaciones — el lado **algebraico** de la trigonometría.",
          ]),
    ]
    return {
        "id": "lec-prec-5-7-leyes-trigonometricas",
        "title": "Leyes trigonométricas",
        "description": "Resolución de triángulos no rectángulos: ley de senos (casos ALA, LAA, LLA con caso ambiguo) y ley de cosenos (casos LAL, LLL). Fórmulas de área. Aplicaciones a navegación.",
        "blocks": blocks,
        "duration_minutes": 60,
        "order": 7,
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

    chapter_id = "ch-prec-trigonometria"
    await db.chapters.delete_one({"id": chapter_id})
    chapter = {
        "id": chapter_id,
        "course_id": course_id,
        "title": "Funciones Trigonométricas",
        "description": (
            "Trigonometría completa: ángulos y sistemas de medida (grados/radianes), razones trigonométricas "
            "en triángulos rectángulos (SOH-CAH-TOA), círculo unitario y extensión a cualquier ángulo, "
            "las 6 funciones trigonométricas con sus identidades, gráficas y transformaciones, funciones "
            "inversas y leyes de senos y cosenos para triángulos oblicuángulos."
        ),
        "order": 5,
        "created_at": now(),
    }
    await db.chapters.insert_one(chapter)
    print(f"✓ Capítulo creado: {chapter['title']}")

    builders = [
        lesson_angulos_medidas,
        lesson_triangulos,
        lesson_circulo_unitario,
        lesson_funciones_trigonometricas,
        lesson_graficas_trigonometricas,
        lesson_funciones_inversas,
        lesson_leyes_trigonometricas,
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
        f"✅ Capítulo 5 — Funciones Trigonométricas listo: "
        f"{len(builders)} lecciones, {total_blocks} bloques, {total_figs} figuras pendientes."
    )
    print()
    for build in builders:
        data = build()
        print(f"  http://localhost:3007/lesson/{data['id']}")


if __name__ == "__main__":
    asyncio.run(main())


