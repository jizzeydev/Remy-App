# Generación de Preguntas con Claude para Remy

## Instrucciones Rápidas

1. Sube tu PDF a Claude
2. Copia el prompt de abajo
3. Personaliza: CURSO, CAPÍTULO, LECCIÓN, NÚMERO DE PREGUNTAS
4. Claude te dará el CSV listo para importar

---

## PROMPT PARA CLAUDE

```
Eres un experto creando preguntas de examen para matemáticas universitarias chilenas.

Necesito que generes preguntas de opción múltiple en formato CSV para el sistema Remy.

CONTEXTO DEL MATERIAL:
- Curso: [NOMBRE DEL CURSO - ej: Cálculo I]
- Capítulo: [NOMBRE DEL CAPÍTULO - ej: Derivadas]
- Lección: [NOMBRE DE LA LECCIÓN - ej: Regla de la Cadena]

FORMATO CSV REQUERIDO (columnas separadas por coma):
capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion

REGLAS:
1. Usa LaTeX con $ para fórmulas (ej: $\frac{x}{2}$, $\int x dx$)
2. Dificultad: fácil, medio o difícil (distribuye variedad)
3. Las 4 opciones deben ser plausibles pero solo una correcta
4. La explicación debe mostrar el procedimiento paso a paso
5. Genera EXACTAMENTE [NÚMERO] preguntas
6. Incluye la línea de encabezado al inicio
7. Si el contenido tiene varios subtemas, distribuye las preguntas entre ellos

GENERA [NÚMERO] PREGUNTAS AHORA:
```

---

## EJEMPLO DE USO

### Input a Claude:
```
CONTEXTO DEL MATERIAL:
- Curso: Cálculo I
- Capítulo: Derivadas
- Lección: Regla de la Cadena

GENERA 15 PREGUNTAS AHORA:
```

### Output esperado (copiar directamente a archivo .csv):
```csv
capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion
Derivadas,Regla de la Cadena,fácil,"Calcule la derivada de $f(x) = (2x+1)^3$",$6(2x+1)^2$,$3(2x+1)^2$,$(2x+1)^2$,$2(2x+1)^3$,A,"Aplicando regla de la cadena: $f'(x) = 3(2x+1)^2 \cdot 2 = 6(2x+1)^2$"
Derivadas,Regla de la Cadena,medio,"Si $g(x) = \sin(x^2)$, entonces $g'(x)$ es:",$2x\cos(x^2)$,$\cos(x^2)$,$2\sin(x)\cos(x)$,$x^2\cos(x^2)$,A,"Por regla de la cadena: $g'(x) = \cos(x^2) \cdot 2x = 2x\cos(x^2)$"
Derivadas,Regla de la Cadena,difícil,"Encuentre $\frac{d}{dx}[\ln(\sqrt{x^2+1})]$","$\frac{x}{x^2+1}$","$\frac{1}{2(x^2+1)}$","$\frac{2x}{\sqrt{x^2+1}}$","$\frac{1}{\sqrt{x^2+1}}$",A,"Simplificando: $\ln(\sqrt{x^2+1}) = \frac{1}{2}\ln(x^2+1)$. Derivando: $\frac{1}{2} \cdot \frac{2x}{x^2+1} = \frac{x}{x^2+1}$"
```

---

## FLUJO PARA GENERAR CONTENIDO MASIVO

Para generar 10-20 preguntas por cada lección de un curso:

### Paso 1: Estructura tu contenido
Organiza tu material por:
```
Curso: Cálculo I
├── Capítulo 1: Límites
│   ├── Lección 1.1: Concepto de Límite (15 preguntas)
│   ├── Lección 1.2: Límites Laterales (15 preguntas)
│   └── Lección 1.3: Límites al Infinito (15 preguntas)
├── Capítulo 2: Derivadas
│   ├── Lección 2.1: Definición de Derivada (15 preguntas)
│   ├── Lección 2.2: Reglas de Derivación (20 preguntas)
│   └── Lección 2.3: Regla de la Cadena (20 preguntas)
```

### Paso 2: Genera por lección
Para cada lección, usa el prompt con el PDF correspondiente:

```
[Sube el PDF del capítulo/lección]

Eres un experto creando preguntas de examen para matemáticas universitarias chilenas.

CONTEXTO:
- Curso: Cálculo I
- Capítulo: Límites
- Lección: Concepto de Límite

Basándote en el material del PDF, genera 15 preguntas variadas:
- 5 fáciles (conceptos básicos, cálculos directos)
- 7 medias (aplicación de técnicas, 2 pasos)
- 3 difíciles (problemas complejos, múltiples conceptos)

FORMATO CSV:
capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion

GENERA 15 PREGUNTAS AHORA:
```

### Paso 3: Combina los CSVs
1. Copia cada output de Claude
2. Combina en un solo archivo .csv
3. Mantén solo UNA línea de encabezado al inicio
4. Importa en Remy: BackOffice → Cursos → [Curso] → Importar CSV

---

## PLANTILLA CSV

Guarda esto como `plantilla_preguntas.csv`:

```csv
capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion
```

### Columnas explicadas:
| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| capitulo | Nombre del capítulo (debe coincidir con Remy) | Derivadas |
| leccion | Nombre de la lección (debe coincidir con Remy) | Regla de la Cadena |
| dificultad | fácil, medio o difícil | medio |
| enunciado | Pregunta con LaTeX usando $ | Calcule $\frac{d}{dx}[x^2]$ |
| opcion_a | Primera alternativa | $2x$ |
| opcion_b | Segunda alternativa | $x$ |
| opcion_c | Tercera alternativa | $x^2$ |
| opcion_d | Cuarta alternativa | $2$ |
| respuesta_correcta | A, B, C o D | A |
| explicacion | Solución paso a paso | La derivada de $x^n$ es $nx^{n-1}$ |

---

## REFERENCIA LATEX

### Operaciones comunes:
```latex
Fracciones:     $\frac{a}{b}$
Raíces:         $\sqrt{x}$ o $\sqrt[n]{x}$
Potencias:      $x^2$ o $x^{n+1}$
Subíndices:     $x_1$ o $x_{i+1}$
Integrales:     $\int x dx$ o $\int_a^b f(x) dx$
Límites:        $\lim_{x \to a} f(x)$
Sumatorias:     $\sum_{i=1}^n i$
Derivadas:      $\frac{d}{dx}$ o $f'(x)$
Parciales:      $\frac{\partial f}{\partial x}$
```

### Funciones:
```latex
Trigonométricas: $\sin(x)$, $\cos(x)$, $\tan(x)$
Logaritmos:      $\ln(x)$, $\log(x)$, $\log_a(x)$
Exponenciales:   $e^x$, $a^x$
```

### Símbolos:
```latex
Pi:        $\pi$
Euler:     $e$
Infinito:  $\infty$
Aproxima:  $\approx$
Diferente: $\neq$
Mayor/Menor: $\geq$, $\leq$
Pertenece: $\in$
```

---

## TIPS PARA MEJOR CALIDAD

1. **Sé específico con el contexto**: Incluye el nombre exacto del curso, capítulo y lección como aparecen en Remy

2. **Distribuye dificultad**: Pide explícitamente la distribución (5 fáciles, 7 medias, 3 difíciles)

3. **Varía los tipos de pregunta**:
   - Cálculo directo
   - Identificar propiedad
   - Encontrar error
   - Aplicar teorema
   - Problema verbal

4. **Revisa antes de importar**: Abre el CSV en Excel/Google Sheets para verificar que no haya errores de formato

5. **Importa por lotes pequeños**: Si tienes muchas preguntas, importa 50-100 a la vez para detectar errores más fácilmente
