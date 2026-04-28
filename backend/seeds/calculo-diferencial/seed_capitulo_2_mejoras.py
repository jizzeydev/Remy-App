"""
Mejoras al Capítulo 2 — Derivadas (curso Cálculo Diferencial).

Mismo patrón que seed_chapter_1_mejoras.py:
- Idempotente: bloques nuevos llevan `_mej: True`. Re-correr borra y re-inserta.
- Pistas en verificaciones por sobreescritura.
- No toca definiciones, teoremas ni ejemplos existentes.
"""
import asyncio
import os
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')


def b(type_, **fields):
    return {"id": str(uuid.uuid4()), "type": type_, "_mej": True, **fields}


def fig(prompt):
    return b("figura", image_url="", caption_md="", prompt_image_md=prompt)


def desmos(expressions, guide, height=400, url=""):
    return b("grafico_desmos", desmos_url=url, expresiones=expressions,
             guia_md=guide, altura=height)


def ej(titulo, enunciado, pistas, solucion):
    return b("ejercicio", titulo=titulo, enunciado_md=enunciado,
             pistas_md=pistas, solucion_md=solucion)


def formulas(titulo, body):
    return b("definicion", titulo=titulo, body_md=body)


STYLE = (
    "Estilo: diagrama educativo limpio, fondo blanco, líneas claras, etiquetas "
    "en español, notación matemática renderizada con buena tipografía. Acentos "
    "de color suaves (teal #06b6d4 y ámbar #f59e0b). Sin sombras dramáticas. "
    "Apto para libro universitario."
)


# -------------------- 2.1 Definición y notación --------------------
LECCION_2_1 = {
    "new_blocks": [
        fig(
            "Diagrama de la interpretación geométrica de la derivada. Eje x e y. Una curva suave "
            "y = f(x). Un punto P = (a, f(a)) marcado. Un segundo punto Q = (a+h, f(a+h)) marcado. "
            "Una recta secante que pasa por P y Q. Una recta tangente en P (de pendiente igual al "
            "límite cuando h tiende a 0). Mostrar h horizontal y f(a+h) - f(a) vertical formando un "
            "triángulo. Etiquetas: 'a', 'a+h', 'f(a)', 'f(a+h)', 'recta secante', 'recta tangente'. "
            "Q debe verse cerca de P. Color teal para la secante, ámbar para la tangente. " + STYLE
        ),
        ej(
            titulo="Derivada por la definición",
            enunciado="Calcula $f'(2)$ para $f(x) = x^2 + 3x$ usando la definición con $h$.",
            pistas=[
                "Plantea $f'(2) = \\lim_{h \\to 0} \\dfrac{f(2+h) - f(2)}{h}$.",
                "Desarrolla $f(2+h) = (2+h)^2 + 3(2+h)$ y simplifica.",
            ],
            solucion=(
                "$f(2) = 4 + 6 = 10$. $f(2+h) = (2+h)^2 + 3(2+h) = 4 + 4h + h^2 + 6 + 3h = 10 + 7h + h^2$.\n\n"
                "$$f'(2) = \\lim_{h \\to 0} \\dfrac{10 + 7h + h^2 - 10}{h} = \\lim_{h \\to 0} \\dfrac{7h + h^2}{h} = \\lim_{h \\to 0}(7 + h) = 7$$"
            ),
        ),
        ej(
            titulo="Recta tangente",
            enunciado="Halla la ecuación de la recta tangente a $f(x) = \\sqrt{x}$ en el punto $(4, 2)$.",
            pistas=[
                "Necesitas $f'(4)$. Recuerda $f'(x) = \\dfrac{1}{2\\sqrt{x}}$.",
                "Usa la forma punto-pendiente: $y - y_0 = m(x - x_0)$.",
            ],
            solucion=(
                "$f'(x) = \\dfrac{1}{2\\sqrt{x}}$, así $f'(4) = \\dfrac{1}{2 \\cdot 2} = \\dfrac{1}{4}$.\n\n"
                "**Recta tangente:** $y - 2 = \\dfrac{1}{4}(x - 4)$, equivalente a $y = \\dfrac{x}{4} + 1$."
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 2.2 Derivabilidad --------------------
LECCION_2_2 = {
    "new_blocks": [
        fig(
            "Tres pequeñas gráficas en una fila ilustrando los tres tipos de no-derivabilidad. "
            "PANEL 1 'Discontinuidad': una función con un salto vertical (dos pedazos a alturas "
            "distintas). PANEL 2 'Esquina': la función |x| con una esquina aguda en el origen, "
            "con dos rectas tangentes potenciales en ángulos distintos. PANEL 3 'Tangente vertical': "
            "una curva como x^(1/3) que pasa por el origen con tangente vertical (pendiente "
            "infinita). Cada panel etiquetado claramente debajo. " + STYLE
        ),
        ej(
            titulo="Estudiar derivabilidad en un punto",
            enunciado=(
                "¿Es $f(x) = |x - 2|$ derivable en $x = 2$? Justifica calculando los laterales del "
                "cociente incremental."
            ),
            pistas=[
                "$|x - 2|$ vale $x - 2$ si $x \\geq 2$ y $-(x - 2)$ si $x < 2$.",
                "Calcula $\\lim_{h \\to 0^+} \\dfrac{f(2+h) - f(2)}{h}$ y $\\lim_{h \\to 0^-} \\dfrac{f(2+h) - f(2)}{h}$.",
            ],
            solucion=(
                "$f(2) = 0$. **Lateral derecho** ($h > 0$): $\\dfrac{|h| - 0}{h} = \\dfrac{h}{h} = 1$. "
                "**Lateral izquierdo** ($h < 0$): $\\dfrac{|h|}{h} = \\dfrac{-h}{h} = -1$.\n\n"
                "Los laterales son distintos ($1 \\neq -1$), así el límite no existe. **$f$ no es derivable** en $x = 2$. "
                "Geométricamente, la gráfica tiene una esquina allí."
            ),
        ),
        ej(
            titulo="Función por tramos",
            enunciado=(
                "Estudia continuidad y derivabilidad en $x = 0$ de "
                "$f(x) = \\begin{cases} x^2 & x \\leq 0 \\\\ x^2 + x & x > 0 \\end{cases}$."
            ),
            pistas=[
                "**Continuidad:** ambos tramos en $0$ valen $0$. Continua.",
                "**Derivabilidad:** la derivada del tramo izquierdo en $0$ es $2x = 0$. La del derecho es $2x + 1 = 1$.",
            ],
            solucion=(
                "**Continuidad:** $\\lim_{x \\to 0^-} x^2 = 0$, $\\lim_{x \\to 0^+}(x^2 + x) = 0$, $f(0) = 0$. **Continua.**\n\n"
                "**Derivabilidad:** las derivadas laterales son $2x|_{x=0} = 0$ (izquierda) y $2x + 1|_{x=0} = 1$ (derecha). "
                "Como $0 \\neq 1$, **$f$ no es derivable en $0$** — esquina."
            ),
        ),
    ],
    "verif_pistas": {
        0: "Continuidad es necesaria pero no suficiente para derivabilidad. ¿Recuerdas el contraejemplo de $|x|$?",
    },
}


# -------------------- 2.3 Reglas de derivación --------------------
LECCION_2_3 = {
    "new_blocks": [
        formulas(
            titulo="Fórmulas clave",
            body=(
                "| Función | Derivada |\n|---|---|\n"
                "| $c$ (constante) | $0$ |\n"
                "| $x$ | $1$ |\n"
                "| $x^n$ | $n x^{n-1}$ |\n"
                "| $cf(x)$ | $cf'(x)$ |\n"
                "| $f \\pm g$ | $f' \\pm g'$ |\n"
                "| $f \\cdot g$ | $f'g + fg'$ |\n"
                "| $f/g$ | $(f'g - fg')/g^2$ |"
            ),
        ),
        ej(
            titulo="Polinomio con varias técnicas",
            enunciado="Deriva $f(x) = (x^2 + 1)(x^3 - 2x + 5)$.",
            pistas=[
                "Es un producto. Aplica $(uv)' = u'v + uv'$.",
                "$u = x^2 + 1$, $u' = 2x$. $v = x^3 - 2x + 5$, $v' = 3x^2 - 2$.",
            ],
            solucion=(
                "$$f'(x) = (2x)(x^3 - 2x + 5) + (x^2 + 1)(3x^2 - 2)$$\n\n"
                "Expandiendo: $2x^4 - 4x^2 + 10x + 3x^4 + 3x^2 - 2x^2 - 2 = 5x^4 - 3x^2 + 10x - 2$."
            ),
        ),
        ej(
            titulo="Cociente con simplificación",
            enunciado="Deriva $g(x) = \\dfrac{x^2 - 1}{x + 1}$ por dos métodos: cociente directo y simplificación previa.",
            pistas=[
                "**Método 1:** regla del cociente.",
                "**Método 2:** factoriza $x^2 - 1 = (x-1)(x+1)$ y simplifica antes.",
            ],
            solucion=(
                "**Método 2 (más rápido):** $g(x) = \\dfrac{(x-1)(x+1)}{x+1} = x - 1$ para $x \\neq -1$. "
                "Así $g'(x) = 1$.\n\n"
                "**Método 1 (cociente):** $g'(x) = \\dfrac{(2x)(x+1) - (x^2-1)(1)}{(x+1)^2} = "
                "\\dfrac{2x^2 + 2x - x^2 + 1}{(x+1)^2} = \\dfrac{x^2 + 2x + 1}{(x+1)^2} = \\dfrac{(x+1)^2}{(x+1)^2} = 1$. ✓"
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 2.4 Trigonométricas --------------------
LECCION_2_4 = {
    "new_blocks": [
        formulas(
            titulo="Tabla de derivadas trigonométricas",
            body=(
                "| Función | Derivada |\n|---|---|\n"
                "| $\\sin x$ | $\\cos x$ |\n"
                "| $\\cos x$ | $-\\sin x$ |\n"
                "| $\\tan x$ | $\\sec^2 x$ |\n"
                "| $\\cot x$ | $-\\csc^2 x$ |\n"
                "| $\\sec x$ | $\\sec x \\tan x$ |\n"
                "| $\\csc x$ | $-\\csc x \\cot x$ |\n\n"
                "**Mnemotecnia:** las funciones que empiezan con 'co-' ($\\cos, \\cot, \\csc$) llevan signo **negativo**."
            ),
        ),
        desmos(
            expressions=["f(x) = \\sin(x)", "g(x) = \\cos(x)"],
            guide=(
                "Compara $\\sin x$ (en azul) con su derivada $\\cos x$ (en rojo). "
                "Observa que donde $\\sin$ tiene un máximo o mínimo, $\\cos$ vale $0$ — "
                "los puntos críticos de $\\sin$ son los ceros de $\\cos$."
            ),
            height=380,
        ),
        ej(
            titulo="Combinar reglas",
            enunciado="Deriva $h(x) = x^2 \\cos x$.",
            pistas=[
                "Regla del producto.",
                "$u = x^2$, $u' = 2x$. $v = \\cos x$, $v' = -\\sin x$.",
            ],
            solucion=(
                "$h'(x) = 2x \\cos x + x^2 (-\\sin x) = 2x\\cos x - x^2 \\sin x$. "
                "Factorizando: $h'(x) = x(2\\cos x - x \\sin x)$."
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 2.5 Cadena --------------------
LECCION_2_5 = {
    "new_blocks": [
        ej(
            titulo="Cadena con función exponencial",
            enunciado="Deriva $f(x) = \\sin(x^3 + 2x)$.",
            pistas=[
                "Exterior $\\sin u$ con derivada $\\cos u$, interior $u = x^3 + 2x$ con derivada $3x^2 + 2$.",
                "$f'(x) = \\cos(g(x)) \\cdot g'(x)$.",
            ],
            solucion="$f'(x) = \\cos(x^3 + 2x) \\cdot (3x^2 + 2) = (3x^2 + 2)\\cos(x^3 + 2x)$.",
        ),
        ej(
            titulo="Cadena anidada (3 capas)",
            enunciado="Deriva $f(x) = \\sqrt{\\tan(2x)}$.",
            pistas=[
                "Tres capas: raíz cuadrada (más exterior), tangente (intermedia), $2x$ (más interior).",
                "Reescribe como $(\\tan(2x))^{1/2}$ y aplica la cadena dos veces.",
            ],
            solucion=(
                "**Capa 1 (exterior $u^{1/2}$):** derivada $\\dfrac{1}{2\\sqrt{\\tan(2x)}}$.\n\n"
                "**Capa 2 ($\\tan u$):** derivada $\\sec^2(2x)$.\n\n"
                "**Capa 3 ($2x$):** derivada $2$.\n\n"
                "**Producto:** $f'(x) = \\dfrac{1}{2\\sqrt{\\tan(2x)}} \\cdot \\sec^2(2x) \\cdot 2 = \\dfrac{\\sec^2(2x)}{\\sqrt{\\tan(2x)}}$."
            ),
        ),
    ],
    "verif_pistas": {
        0: "El factor más fácil de olvidar es la derivada de la función **interior**.",
    },
}


# -------------------- 2.6 Implícita --------------------
LECCION_2_6 = {
    "new_blocks": [
        ej(
            titulo="Recta tangente a una curva implícita",
            enunciado="Halla la recta tangente a la curva $x^2 + xy + y^2 = 7$ en el punto $(1, 2)$.",
            pistas=[
                "Deriva implícitamente: cada término que tenga $y$ aporta un factor $y'$ por cadena.",
                "$\\dfrac{d}{dx}[xy] = y + xy'$ por la regla del producto.",
            ],
            solucion=(
                "Derivando: $2x + (y + xy') + 2y \\cdot y' = 0$. Agrupando $y'$: $(x + 2y)y' = -(2x + y)$.\n\n"
                "$y' = -\\dfrac{2x + y}{x + 2y}$. **En $(1, 2)$:** $y' = -\\dfrac{2 + 2}{1 + 4} = -\\dfrac{4}{5}$.\n\n"
                "**Recta tangente:** $y - 2 = -\\dfrac{4}{5}(x - 1)$."
            ),
        ),
        ej(
            titulo="Implícita con exponencial",
            enunciado="Calcula $\\dfrac{dy}{dx}$ para la curva $e^y = x^2 + y$.",
            pistas=[
                "El lado izquierdo necesita cadena: $\\dfrac{d}{dx}[e^y] = e^y \\cdot y'$.",
                "Agrupa todos los $y'$ en un lado.",
            ],
            solucion=(
                "Derivando: $e^y \\cdot y' = 2x + y'$, así $y'(e^y - 1) = 2x$, y "
                "$y' = \\dfrac{2x}{e^y - 1}$ (definida cuando $e^y \\neq 1$, es decir, $y \\neq 0$)."
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 2.7 Logarítmica --------------------
LECCION_2_7 = {
    "new_blocks": [
        ej(
            titulo="Producto complicado",
            enunciado="Deriva $y = \\dfrac{x^3 \\sqrt{x^2 + 1}}{(x - 1)^4}$.",
            pistas=[
                "Toma $\\ln$ en ambos lados y usa propiedades para separar todo en sumas y restas.",
                "$\\ln y = 3\\ln x + \\dfrac{1}{2}\\ln(x^2+1) - 4\\ln(x-1)$.",
            ],
            solucion=(
                "$\\ln y = 3\\ln x + \\dfrac{1}{2}\\ln(x^2+1) - 4\\ln(x-1)$.\n\n"
                "Derivando: $\\dfrac{y'}{y} = \\dfrac{3}{x} + \\dfrac{x}{x^2+1} - \\dfrac{4}{x-1}$.\n\n"
                "$$y' = \\dfrac{x^3 \\sqrt{x^2+1}}{(x-1)^4} \\left(\\dfrac{3}{x} + \\dfrac{x}{x^2+1} - \\dfrac{4}{x-1}\\right)$$"
            ),
        ),
        ej(
            titulo="Base y exponente variables",
            enunciado="Deriva $y = (\\sin x)^x$ para $x \\in (0, \\pi)$.",
            pistas=[
                "$\\ln y = x \\ln(\\sin x)$.",
                "Deriva el lado derecho con regla del producto: $1 \\cdot \\ln(\\sin x) + x \\cdot \\dfrac{\\cos x}{\\sin x}$.",
            ],
            solucion=(
                "$\\ln y = x \\ln(\\sin x)$. Derivando: $\\dfrac{y'}{y} = \\ln(\\sin x) + x \\cdot \\cot x$.\n\n"
                "$$y' = (\\sin x)^x \\left[\\ln(\\sin x) + x \\cot x\\right]$$"
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 2.8 Inversas --------------------
LECCION_2_8 = {
    "new_blocks": [
        formulas(
            titulo="Derivadas de las trigonométricas inversas",
            body=(
                "| Función | Derivada | Dominio |\n|---|---|---|\n"
                "| $\\arcsin x$ | $\\dfrac{1}{\\sqrt{1-x^2}}$ | $|x| < 1$ |\n"
                "| $\\arccos x$ | $-\\dfrac{1}{\\sqrt{1-x^2}}$ | $|x| < 1$ |\n"
                "| $\\arctan x$ | $\\dfrac{1}{1+x^2}$ | $\\mathbb{R}$ |\n"
                "| $\\text{arccot}\\, x$ | $-\\dfrac{1}{1+x^2}$ | $\\mathbb{R}$ |\n"
                "| $\\text{arcsec}\\, x$ | $\\dfrac{1}{|x|\\sqrt{x^2-1}}$ | $|x| > 1$ |\n"
                "| $\\text{arccsc}\\, x$ | $-\\dfrac{1}{|x|\\sqrt{x^2-1}}$ | $|x| > 1$ |"
            ),
        ),
        ej(
            titulo="Cadena con arctangente",
            enunciado="Deriva $f(x) = \\arctan(\\sqrt{x})$.",
            pistas=[
                "Exterior $\\arctan u$ con derivada $1/(1+u^2)$, interior $u = \\sqrt{x}$ con derivada $1/(2\\sqrt{x})$.",
            ],
            solucion=(
                "$$f'(x) = \\dfrac{1}{1 + (\\sqrt{x})^2} \\cdot \\dfrac{1}{2\\sqrt{x}} = \\dfrac{1}{(1+x) \\cdot 2\\sqrt{x}} = \\dfrac{1}{2\\sqrt{x}(1+x)}$$"
            ),
        ),
        ej(
            titulo="Inversa funcional concreta",
            enunciado="Sea $f(x) = x + e^x$. Calcula $(f^{-1})'(1)$ sabiendo que $f(0) = 1$.",
            pistas=[
                "Fórmula: $(f^{-1})'(y) = \\dfrac{1}{f'(f^{-1}(y))}$.",
                "$f^{-1}(1) = 0$ (dado), así $(f^{-1})'(1) = 1/f'(0)$.",
            ],
            solucion=(
                "$f'(x) = 1 + e^x$, así $f'(0) = 1 + 1 = 2$. Por la fórmula:\n\n"
                "$$(f^{-1})'(1) = \\dfrac{1}{f'(f^{-1}(1))} = \\dfrac{1}{f'(0)} = \\dfrac{1}{2}$$"
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 2.9 Log/exp --------------------
LECCION_2_9 = {
    "new_blocks": [
        formulas(
            titulo="Derivadas de exponenciales y logarítmicas",
            body=(
                "| Función | Derivada |\n|---|---|\n"
                "| $e^x$ | $e^x$ |\n"
                "| $a^x$ ($a > 0$) | $a^x \\ln a$ |\n"
                "| $\\ln x$ ($x > 0$) | $1/x$ |\n"
                "| $\\log_a x$ | $\\dfrac{1}{x \\ln a}$ |\n"
                "| $e^{g(x)}$ | $e^{g(x)} g'(x)$ |\n"
                "| $\\ln(g(x))$ | $g'(x)/g(x)$ |\n\n"
                "**Patrón derivada logarítmica:** $\\dfrac{d}{dx}\\ln(g(x)) = \\dfrac{g'(x)}{g(x)}$ — útil en integración."
            ),
        ),
        ej(
            titulo="Combinación log y polinomio",
            enunciado="Deriva $f(x) = x^2 \\ln(3x + 1)$.",
            pistas=[
                "Producto: $u = x^2$ y $v = \\ln(3x+1)$.",
                "$v'$ por cadena: $\\dfrac{3}{3x+1}$.",
            ],
            solucion=(
                "$f'(x) = 2x \\ln(3x+1) + x^2 \\cdot \\dfrac{3}{3x+1} = 2x\\ln(3x+1) + \\dfrac{3x^2}{3x+1}$."
            ),
        ),
        ej(
            titulo="Exponencial con cadena",
            enunciado="Deriva $g(x) = e^{x^2 \\sin x}$.",
            pistas=[
                "Exterior $e^u$ con derivada $e^u$, interior $u = x^2 \\sin x$ que requiere regla del producto.",
                "$u' = 2x \\sin x + x^2 \\cos x$.",
            ],
            solucion=(
                "$$g'(x) = e^{x^2 \\sin x} \\cdot (2x \\sin x + x^2 \\cos x) = (2x \\sin x + x^2 \\cos x) \\, e^{x^2 \\sin x}$$"
            ),
        ),
    ],
    "verif_pistas": {},
}


# -------------------- 2.10 L'Hôpital --------------------
LECCION_2_10 = {
    "new_blocks": [
        desmos(
            expressions=["f(x) = \\ln(x)/x", "y = 0"],
            guide=(
                "Visualización del límite $\\lim_{x \\to +\\infty} \\dfrac{\\ln x}{x} = 0$. "
                "Aleja la vista hacia $x$ grande y observa cómo la función se acerca a cero. "
                "Es decir: la función polinómica (aquí $x$) crece más rápido que el logaritmo."
            ),
            height=380,
        ),
        ej(
            titulo="L'Hôpital aplicado dos veces",
            enunciado="Calcula $\\lim_{x \\to 0} \\dfrac{1 - \\cos x}{x^2}$.",
            pistas=[
                "Sustitución directa: $0/0$. Aplica L'Hôpital.",
                "Después de derivar una vez vuelve a salir $0/0$ — aplica L'Hôpital de nuevo.",
            ],
            solucion=(
                "**Primer L'Hôpital:** $\\lim_{x \\to 0} \\dfrac{\\sin x}{2x}$. Vuelve a salir $0/0$.\n\n"
                "**Segundo L'Hôpital:** $\\lim_{x \\to 0} \\dfrac{\\cos x}{2} = \\dfrac{1}{2}$.\n\n"
                "**Resultado:** $\\dfrac{1}{2}$. (Conocido como uno de los límites trigonométricos fundamentales.)"
            ),
        ),
        ej(
            titulo="Forma indeterminada $0 \\cdot \\infty$",
            enunciado="Calcula $\\lim_{x \\to 0^+} x^2 \\ln x$.",
            pistas=[
                "Indeterminación $0 \\cdot (-\\infty)$. Reescribe como cociente: $\\dfrac{\\ln x}{1/x^2}$.",
                "Ahora es $-\\infty/+\\infty$. Aplica L'Hôpital.",
            ],
            solucion=(
                "$$\\lim_{x \\to 0^+} \\dfrac{\\ln x}{1/x^2} = \\lim_{x \\to 0^+} \\dfrac{1/x}{-2/x^3} = \\lim_{x \\to 0^+} \\dfrac{-x^2}{2} = 0$$\n\n"
                "**Conclusión:** $\\lim_{x \\to 0^+} x^2 \\ln x = 0$. Polinomio gana sobre $\\ln$ incluso cerca de $0$."
            ),
        ),
        ej(
            titulo="Forma $1^\\infty$",
            enunciado="Calcula $\\lim_{x \\to 0}(1 + 2x)^{1/x}$.",
            pistas=[
                "Indeterminación $1^\\infty$. Toma logaritmo: si $L$ es el límite, $\\ln L = \\lim \\dfrac{\\ln(1+2x)}{x}$.",
                "Aplica L'Hôpital al lado derecho.",
            ],
            solucion=(
                "Sea $L$ el límite. $\\ln L = \\lim_{x \\to 0} \\dfrac{\\ln(1 + 2x)}{x}$, forma $0/0$.\n\n"
                "L'Hôpital: $\\lim_{x \\to 0} \\dfrac{2/(1+2x)}{1} = 2$.\n\n"
                "$\\ln L = 2 \\implies L = e^2$."
            ),
        ),
    ],
    "verif_pistas": {
        0: "L'Hôpital sólo aplica con $0/0$ o $\\infty/\\infty$. ¿Es ese el caso aquí?",
    },
}


# -------------------- 2.11 Hiperbólicas --------------------
LECCION_2_11 = {
    "new_blocks": [
        formulas(
            titulo="Funciones hiperbólicas y sus derivadas",
            body=(
                "**Definiciones:**\n\n"
                "$$\\sinh x = \\dfrac{e^x - e^{-x}}{2}, \\quad \\cosh x = \\dfrac{e^x + e^{-x}}{2}, \\quad \\tanh x = \\dfrac{\\sinh x}{\\cosh x}$$\n\n"
                "**Identidad fundamental:** $\\cosh^2 x - \\sinh^2 x = 1$.\n\n"
                "**Derivadas:**\n\n"
                "| Función | Derivada |\n|---|---|\n"
                "| $\\sinh x$ | $\\cosh x$ |\n"
                "| $\\cosh x$ | $\\sinh x$ |\n"
                "| $\\tanh x$ | $\\text{sech}^2 x$ |\n"
                "| $\\text{coth}\\, x$ | $-\\text{csch}^2 x$ |\n"
                "| $\\text{sech}\\, x$ | $-\\text{sech}\\, x \\tanh x$ |\n"
                "| $\\text{csch}\\, x$ | $-\\text{csch}\\, x \\coth x$ |\n\n"
                "**Atención:** $(\\cosh x)' = +\\sinh x$ — sin signo negativo (a diferencia de $\\cos$)."
            ),
        ),
        ej(
            titulo="Cadena con seno hiperbólico",
            enunciado="Deriva $f(x) = \\sinh(3x^2 + 1)$.",
            pistas=[
                "Exterior $\\sinh u$ con derivada $\\cosh u$, interior $u = 3x^2 + 1$ con derivada $6x$.",
            ],
            solucion="$f'(x) = \\cosh(3x^2 + 1) \\cdot 6x = 6x \\cosh(3x^2 + 1)$.",
        ),
        ej(
            titulo="Verificar identidad con derivadas",
            enunciado=(
                "Sabiendo que $\\dfrac{d}{dx}[\\tanh x] = \\text{sech}^2 x$, deduce esta fórmula desde "
                "$\\tanh x = \\sinh x / \\cosh x$ usando la regla del cociente."
            ),
            pistas=[
                "Aplica $(f/g)' = (f'g - fg')/g^2$ con $f = \\sinh$ y $g = \\cosh$.",
                "Después usa $\\cosh^2 - \\sinh^2 = 1$ para simplificar.",
            ],
            solucion=(
                "$$\\dfrac{d}{dx}\\dfrac{\\sinh x}{\\cosh x} = \\dfrac{\\cosh x \\cdot \\cosh x - \\sinh x \\cdot \\sinh x}{\\cosh^2 x} = \\dfrac{\\cosh^2 x - \\sinh^2 x}{\\cosh^2 x} = \\dfrac{1}{\\cosh^2 x} = \\text{sech}^2 x$$"
            ),
        ),
    ],
    "verif_pistas": {},
}


IMPROVEMENTS = {
    "lesson-definicion-y-notacion": LECCION_2_1,
    "lec-derivadas-2-2-derivabilidad": LECCION_2_2,
    "lec-derivadas-2-3-reglas": LECCION_2_3,
    "lec-derivadas-2-4-trigonometricas": LECCION_2_4,
    "lec-derivadas-2-5-cadena": LECCION_2_5,
    "lec-derivadas-2-6-implicita": LECCION_2_6,
    "lec-derivadas-2-7-logaritmica": LECCION_2_7,
    "lec-derivadas-2-8-inversas": LECCION_2_8,
    "lec-derivadas-2-9-log-exp": LECCION_2_9,
    "lec-derivadas-2-10-lhopital": LECCION_2_10,
    "lec-derivadas-2-11-hiperbolicas": LECCION_2_11,
}


async def main():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]

    total_added = 0
    total_pistas = 0
    for lesson_id, imp in IMPROVEMENTS.items():
        lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
        if not lesson:
            print(f"  ⚠ Lección no encontrada: {lesson_id}")
            continue

        cleaned = [blk for blk in lesson.get("blocks", []) if not blk.get("_mej")]

        new_blocks = imp.get("new_blocks", [])
        ec_idx = next((i for i, blk in enumerate(cleaned) if blk.get("type") == "errores_comunes"), None)
        resumen_idx = next((i for i, blk in enumerate(cleaned) if blk.get("type") == "resumen"), len(cleaned))
        insert_at = ec_idx if ec_idx is not None else resumen_idx
        cleaned[insert_at:insert_at] = new_blocks

        pistas = imp.get("verif_pistas", {})
        pistas_set = 0
        if pistas:
            for blk in cleaned:
                if blk.get("type") == "verificacion" and blk.get("preguntas"):
                    for idx, pista in pistas.items():
                        if idx < len(blk["preguntas"]):
                            blk["preguntas"][idx]["pista_md"] = pista
                            pistas_set += 1
                    break

        await db.lessons.update_one({"id": lesson_id}, {"$set": {"blocks": cleaned}})
        total_added += len(new_blocks)
        total_pistas += pistas_set
        print(f"  ✓ {lesson['title']} (+{len(new_blocks)} bloques, +{pistas_set} pistas)")

    print()
    print(f"✅ Capítulo 2 mejorado: {total_added} bloques nuevos, {total_pistas} pistas en verificaciones.")


if __name__ == "__main__":
    asyncio.run(main())
