# Prompt y Plantilla para Generar Preguntas con Claude

## Prompt para Claude

Copia y pega este prompt en Claude para generar preguntas de examen:

---

```
Eres un experto en crear preguntas de examen para matemáticas universitarias chilenas.

Genera preguntas de opción múltiple en formato CSV con las siguientes columnas:
- question_content: Pregunta usando LaTeX con delimitadores $ (ej: $\frac{x}{2}$)
- options: 4 opciones separadas por | (ej: $2x$|$x^2$|$3x$|$x$)
- correct_answer: Letra de la respuesta correcta (A, B, C o D)
- solution_content: Explicación paso a paso de la solución (usando LaTeX)
- difficulty: facil, medio o dificil
- topic: Tema específico (ej: Derivadas, Integrales, Límites)
- tags: Etiquetas separadas por coma (ej: cálculo,derivadas,regla de la cadena)

REGLAS IMPORTANTES:
1. Usa LaTeX para todas las expresiones matemáticas
2. Las opciones deben ser plausibles pero solo una correcta
3. La solución debe explicar el procedimiento completo
4. Varía la dificultad entre las preguntas
5. NO incluyas la línea de encabezado del CSV, solo las filas de datos

TEMA: [ESPECIFICA EL TEMA AQUÍ]
NÚMERO DE PREGUNTAS: [NÚMERO]
DIFICULTAD PREDOMINANTE: [facil/medio/dificil]

Genera las preguntas ahora:
```

---

## Ejemplo de uso:

### Input a Claude:
```
TEMA: Derivadas usando la regla de la cadena
NÚMERO DE PREGUNTAS: 5
DIFICULTAD PREDOMINANTE: medio
```

### Output esperado de Claude (copiar a un archivo .csv):
```csv
question_content,options,correct_answer,solution_content,difficulty,topic,tags
"Calcule la derivada de $f(x) = (3x^2 + 1)^4$","$24x(3x^2 + 1)^3$|$12x(3x^2 + 1)^3$|$4(3x^2 + 1)^3$|$24x(3x^2 + 1)^4$",A,"Usando la regla de la cadena: $f'(x) = 4(3x^2 + 1)^3 \cdot 6x = 24x(3x^2 + 1)^3$",medio,Derivadas,"cálculo,derivadas,regla de la cadena"
"Si $g(x) = \sin(x^2)$, entonces $g'(x)$ es:","$2x\cos(x^2)$|$\cos(x^2)$|$2\sin(x)\cos(x)$|$x^2\cos(x^2)$",A,"Aplicando la regla de la cadena: $g'(x) = \cos(x^2) \cdot 2x = 2x\cos(x^2)$",medio,Derivadas,"cálculo,derivadas,trigonométricas"
```

---

## Plantilla CSV (con encabezado)

Guarda esto como `plantilla_preguntas.csv`:

```csv
question_content,options,correct_answer,solution_content,difficulty,topic,tags
"Calcule la derivada de $f(x) = x^3 + 2x$","$3x^2 + 2$|$3x^2$|$x^2 + 2$|$3x + 2$",A,"La derivada de $x^3$ es $3x^2$ y la derivada de $2x$ es $2$. Por lo tanto: $f'(x) = 3x^2 + 2$",medio,Derivadas,"cálculo,derivadas"
"Resuelva la integral $\int x^2 dx$","$\frac{x^3}{3} + C$|$x^3 + C$|$2x + C$|$\frac{x^2}{2} + C$",A,"Usando la regla de potencias: $\int x^n dx = \frac{x^{n+1}}{n+1} + C$",facil,Integrales,"cálculo,integrales"
"Si $\lim_{x \to 0} \frac{\sin(x)}{x} = L$, ¿cuál es el valor de $L$?","$0$|$1$|$\infty$|No existe",B,"Este es un límite notable. $\lim_{x \to 0} \frac{\sin(x)}{x} = 1$",medio,Límites,"cálculo,límites"
```

---

## Instrucciones de importación:

1. Genera las preguntas con Claude usando el prompt
2. Copia el output de Claude a un archivo `.csv`
3. **IMPORTANTE**: Añade la línea de encabezado si Claude no la incluyó:
   ```
   question_content,options,correct_answer,solution_content,difficulty,topic,tags
   ```
4. Ve al BackOffice de Remy → Universidades → Selecciona Universidad → Curso → Evaluación
5. Haz clic en el botón "CSV" en la sección de Preguntas
6. Sube el archivo y haz clic en "Importar"

---

## Notas sobre el formato LaTeX:

- Fracciones: `$\frac{a}{b}$`
- Raíces: `$\sqrt{x}$` o `$\sqrt[n]{x}$`
- Potencias: `$x^2$` o `$x^{n+1}$`
- Subíndices: `$x_1$` o `$x_{i+1}$`
- Integrales: `$\int x dx$` o `$\int_a^b f(x) dx$`
- Límites: `$\lim_{x \to a} f(x)$`
- Sumatorias: `$\sum_{i=1}^n i$`
- Seno/Coseno: `$\sin(x)$`, `$\cos(x)$`, `$\tan(x)$`
- Pi/Euler: `$\pi$`, `$e$`
- Infinito: `$\infty$`

---

## Temas sugeridos para generación:

### Cálculo I
- Límites y continuidad
- Derivadas (regla de la cadena, producto, cociente)
- Aplicaciones de derivadas (máximos, mínimos, puntos de inflexión)
- Integrales indefinidas
- Integrales definidas
- Área bajo la curva

### Cálculo II
- Técnicas de integración (sustitución, partes, fracciones parciales)
- Integrales impropias
- Series y sucesiones
- Series de Taylor y Maclaurin

### Álgebra Lineal
- Matrices y determinantes
- Sistemas de ecuaciones lineales
- Espacios vectoriales
- Transformaciones lineales
- Valores y vectores propios

### Ecuaciones Diferenciales
- EDO de primer orden
- EDO de segundo orden
- Sistemas de ecuaciones diferenciales
