"""
Estandariza nombres de carpetas y archivos del curso Cálculo Diferencial.

Convención:
- Carpetas de capítulo: '01. Límites y Continuidad', '02. Derivadas', '03. Aplicaciones de las Derivadas'
- Carpetas de lección: 'NN. Tema en español sentence-case' (sólo primera palabra y nombres propios)
- Carpetas de ejercicios: 'NN. Tema' (sin sufijo 'E', numeración propia, no la de la lección)
- Archivos de clase: 'Clase.pdf', 'Apuntes.pdf'
- Archivos de ejercicios: 'Enunciados.pdf', 'Soluciones.pdf'
- CSVs de preguntas: 'Preguntas.csv', 'Preguntas curadas.csv'

Uso:
  python scripts/rename_calculo_diferencial.py             # dry-run
  python scripts/rename_calculo_diferencial.py --apply     # ejecuta con git mv
"""
import os
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = REPO_ROOT / "docs" / "cursos" / "generales" / "calculo-diferencial"


# ============================================================
# Mapeos: old_relative_path -> new_relative_path
# Todas las rutas son relativas a BASE.
# ============================================================

# --- ARCHIVOS dentro de las carpetas ORIGINALES (renombrar primero) ---
FILE_RENAMES = {
    # Cap 1 — Clases
    "1. Límites y Continuidad/Clases/1. Introducción intuitiva/Límites_y_Continuidad___Introducción_intuitiva.pdf": "1. Límites y Continuidad/Clases/1. Introducción intuitiva/Clase.pdf",
    "1. Límites y Continuidad/Clases/1. Introducción intuitiva/Límites_y_Continuidad___Introducción_intuitiva_Apuntes.pdf": "1. Límites y Continuidad/Clases/1. Introducción intuitiva/Apuntes.pdf",
    "1. Límites y Continuidad/Clases/2. Definición formal/Límites_y_Continuidad___Definición_formal.pdf": "1. Límites y Continuidad/Clases/2. Definición formal/Clase.pdf",
    "1. Límites y Continuidad/Clases/2. Definición formal/Límites_y_Continuidad___Definición_formal_Apuntes.pdf": "1. Límites y Continuidad/Clases/2. Definición formal/Apuntes.pdf",
    "1. Límites y Continuidad/Clases/3. Propiedades de los límites/Límites_y_Continuidad___Propiedades_de_los_límites.pdf": "1. Límites y Continuidad/Clases/3. Propiedades de los límites/Clase.pdf",
    "1. Límites y Continuidad/Clases/3. Propiedades de los límites/Límites_y_Continuidad___Propiedades_de_los_límites_Apuntes.pdf": "1. Límites y Continuidad/Clases/3. Propiedades de los límites/Apuntes.pdf",
    "1. Límites y Continuidad/Clases/4. Continuidad de funciones/Límites_y_Continuidad___Continuidad.pdf": "1. Límites y Continuidad/Clases/4. Continuidad de funciones/Clase.pdf",
    "1. Límites y Continuidad/Clases/4. Continuidad de funciones/Límites_y_Continuidad___Continuidad_Apuntes.pdf": "1. Límites y Continuidad/Clases/4. Continuidad de funciones/Apuntes.pdf",
    "1. Límites y Continuidad/Clases/5. Teorema del valor intermedio/Límites_y_Continuidad___Teorema_del_Valor_Intermedio.pdf": "1. Límites y Continuidad/Clases/5. Teorema del valor intermedio/Clase.pdf",
    "1. Límites y Continuidad/Clases/5. Teorema del valor intermedio/Límites_y_Continuidad___Teorema_del_Valor_Intermedio_Apuntes.pdf": "1. Límites y Continuidad/Clases/5. Teorema del valor intermedio/Apuntes.pdf",
    "1. Límites y Continuidad/Clases/6. Asíntotas/Límites_y_Continuidad___Asíntotas.pdf": "1. Límites y Continuidad/Clases/6. Asíntotas/Clase.pdf",
    "1. Límites y Continuidad/Clases/6. Asíntotas/Límites_y_Continuidad___Asíntotas_Apuntes.pdf": "1. Límites y Continuidad/Clases/6. Asíntotas/Apuntes.pdf",
    "1. Límites y Continuidad/Clases/7. Resolver límites/Límites_y_Continuidad___Resolver_Límites.pdf": "1. Límites y Continuidad/Clases/7. Resolver límites/Clase.pdf",
    "1. Límites y Continuidad/Clases/7. Resolver límites/Límites_y_Continuidad___Resolver_Límites_Apuntes.pdf": "1. Límites y Continuidad/Clases/7. Resolver límites/Apuntes.pdf",

    # Cap 1 — Ejercicios
    "1. Límites y Continuidad/Ejercicios/1E. Definición formal/Límites___Ejercicios__Definición_Precisa.pdf": "1. Límites y Continuidad/Ejercicios/1E. Definición formal/Enunciados.pdf",
    "1. Límites y Continuidad/Ejercicios/1E. Definición formal/Límites___Ejercicios__Definición_Precisa_Soluciones.pdf": "1. Límites y Continuidad/Ejercicios/1E. Definición formal/Soluciones.pdf",
    "1. Límites y Continuidad/Ejercicios/2E. Continuidad/Límites___Ejercicios__Continuidad.pdf": "1. Límites y Continuidad/Ejercicios/2E. Continuidad/Enunciados.pdf",
    "1. Límites y Continuidad/Ejercicios/2E. Continuidad/Límites___Ejercicios__Continuidad_Soluciones.pdf": "1. Límites y Continuidad/Ejercicios/2E. Continuidad/Soluciones.pdf",
    "1. Límites y Continuidad/Ejercicios/3E. Límites al Infinito/Límites___Ejercicios__Límites_al_Infinito.pdf": "1. Límites y Continuidad/Ejercicios/3E. Límites al Infinito/Enunciados.pdf",
    "1. Límites y Continuidad/Ejercicios/3E. Límites al Infinito/Límites___Ejercicios__Límites_al_Infinito_Soluciones.pdf": "1. Límites y Continuidad/Ejercicios/3E. Límites al Infinito/Soluciones.pdf",
    "1. Límites y Continuidad/Ejercicios/4E. Teorema del Valor Intermedio/Límites___Ejercicios__Teorema_del_Valor_Intermedio.pdf": "1. Límites y Continuidad/Ejercicios/4E. Teorema del Valor Intermedio/Enunciados.pdf",
    "1. Límites y Continuidad/Ejercicios/4E. Teorema del Valor Intermedio/Límites___Ejercicios__Teorema_del_Valor_Intermedio_Soluciones.pdf": "1. Límites y Continuidad/Ejercicios/4E. Teorema del Valor Intermedio/Soluciones.pdf",
    "1. Límites y Continuidad/Ejercicios/5E. Asíntotas/Límites___Ejercicios__Asíntotas.pdf": "1. Límites y Continuidad/Ejercicios/5E. Asíntotas/Enunciados.pdf",
    "1. Límites y Continuidad/Ejercicios/5E. Asíntotas/Límites___Ejercicios__Asíntotas_Soluciones.pdf": "1. Límites y Continuidad/Ejercicios/5E. Asíntotas/Soluciones.pdf",
    "1. Límites y Continuidad/Ejercicios/6E. Límites/Límites___Ejercicios__Límites.pdf": "1. Límites y Continuidad/Ejercicios/6E. Límites/Enunciados.pdf",
    "1. Límites y Continuidad/Ejercicios/6E. Límites/Límites___Ejercicios__Límites_Soluciones.pdf": "1. Límites y Continuidad/Ejercicios/6E. Límites/Soluciones.pdf",

    # Cap 1 — Preguntas
    "1. Límites y Continuidad/Preguntas/limites.csv": "1. Límites y Continuidad/Preguntas/Preguntas.csv",
    "1. Límites y Continuidad/Preguntas/limites_curado.csv": "1. Límites y Continuidad/Preguntas/Preguntas curadas.csv",

    # Cap 2 — Clases
    "2. Derivadas/Clases/1. Definición y notación/Derivadas___Definición_y_notación.pdf": "2. Derivadas/Clases/1. Definición y notación/Clase.pdf",
    "2. Derivadas/Clases/1. Definición y notación/Derivadas___Definición_y_notación_Apuntes.pdf": "2. Derivadas/Clases/1. Definición y notación/Apuntes.pdf",
    "2. Derivadas/Clases/2. Derivabilidad/Derivadas___Derivabilidad.pdf": "2. Derivadas/Clases/2. Derivabilidad/Clase.pdf",
    "2. Derivadas/Clases/2. Derivabilidad/Derivadas___Derivabilidad_Apuntes.pdf": "2. Derivadas/Clases/2. Derivabilidad/Apuntes.pdf",
    "2. Derivadas/Clases/3. Reglas de derivación/Derivadas___Reglas_de_Derivación.pdf": "2. Derivadas/Clases/3. Reglas de derivación/Clase.pdf",
    "2. Derivadas/Clases/3. Reglas de derivación/Derivadas___Reglas_de_Derivación_Apuntes.pdf": "2. Derivadas/Clases/3. Reglas de derivación/Apuntes.pdf",
    "2. Derivadas/Clases/4. Derivadas trigonométricas/Derivadas___Derivadas_Trigonométricas.pdf": "2. Derivadas/Clases/4. Derivadas trigonométricas/Clase.pdf",
    "2. Derivadas/Clases/4. Derivadas trigonométricas/Derivadas___Derivadas_Trigonométricas_Apuntes.pdf": "2. Derivadas/Clases/4. Derivadas trigonométricas/Apuntes.pdf",
    "2. Derivadas/Clases/5. Regla de la cadena/Derivadas___Regla_de_la_Cadena.pdf": "2. Derivadas/Clases/5. Regla de la cadena/Clase.pdf",
    "2. Derivadas/Clases/5. Regla de la cadena/Derivadas___Regla_de_la_Cadena_Apuntes.pdf": "2. Derivadas/Clases/5. Regla de la cadena/Apuntes.pdf",
    "2. Derivadas/Clases/6. Derivación implícita/Derivadas___Derivación_Implícita.pdf": "2. Derivadas/Clases/6. Derivación implícita/Clase.pdf",
    "2. Derivadas/Clases/6. Derivación implícita/Derivadas___Derivación_Implícita_Apuntes.pdf": "2. Derivadas/Clases/6. Derivación implícita/Apuntes.pdf",
    "2. Derivadas/Clases/7. Derivación logarítmica/Derivadas___Derivación_Logarítmica.pdf": "2. Derivadas/Clases/7. Derivación logarítmica/Clase.pdf",
    "2. Derivadas/Clases/7. Derivación logarítmica/Derivadas___Derivación_Logarítmica_Apuntes.pdf": "2. Derivadas/Clases/7. Derivación logarítmica/Apuntes.pdf",
    "2. Derivadas/Clases/8. Derivadas de funciones inversas/Derivadas___Derivadas_de_funciones_inversas.pdf": "2. Derivadas/Clases/8. Derivadas de funciones inversas/Clase.pdf",
    "2. Derivadas/Clases/8. Derivadas de funciones inversas/Derivadas___Derivadas_de_funciones_inversas_Apuntes.pdf": "2. Derivadas/Clases/8. Derivadas de funciones inversas/Apuntes.pdf",
    "2. Derivadas/Clases/9. Derivadas de funciones logarítmicas y exponenciales/Derivadas___Derivadas_de_funciones_logarítmicas_y_exponenciales.pdf": "2. Derivadas/Clases/9. Derivadas de funciones logarítmicas y exponenciales/Clase.pdf",
    "2. Derivadas/Clases/9. Derivadas de funciones logarítmicas y exponenciales/Derivadas___Derivadas_de_funciones_logarítmicas_y_exponenciales_Apuntes.pdf": "2. Derivadas/Clases/9. Derivadas de funciones logarítmicas y exponenciales/Apuntes.pdf",
    "2. Derivadas/Clases/10. Regla de L'Hopital/Derivadas___Regla_de_L_Hopital.pdf": "2. Derivadas/Clases/10. Regla de L'Hopital/Clase.pdf",
    "2. Derivadas/Clases/10. Regla de L'Hopital/Derivadas___Regla_de_L_Hopital_Apuntes.pdf": "2. Derivadas/Clases/10. Regla de L'Hopital/Apuntes.pdf",
    "2. Derivadas/Clases/11. Funciones Hiperbólicas/Derivadas___Funciones_Hiperbólicas.pdf": "2. Derivadas/Clases/11. Funciones Hiperbólicas/Clase.pdf",
    "2. Derivadas/Clases/11. Funciones Hiperbólicas/Derivadas___Funciones_Hiperbólicas_Apuntes.pdf": "2. Derivadas/Clases/11. Funciones Hiperbólicas/Apuntes.pdf",

    # Cap 2 — Ejercicios
    "2. Derivadas/Ejercicios/1E. Derivabilidad/Derivadas___Ejercicios__Derivabilidad.pdf": "2. Derivadas/Ejercicios/1E. Derivabilidad/Enunciados.pdf",
    "2. Derivadas/Ejercicios/1E. Derivabilidad/Derivadas___Ejercicios__Derivabilidad_Soluciones.pdf": "2. Derivadas/Ejercicios/1E. Derivabilidad/Soluciones.pdf",
    "2. Derivadas/Ejercicios/2E. Regla de L'Hopital/Derivadas___Ejercicios__Regla_de_L_Hopital.pdf": "2. Derivadas/Ejercicios/2E. Regla de L'Hopital/Enunciados.pdf",
    "2. Derivadas/Ejercicios/2E. Regla de L'Hopital/Derivadas___Ejercicios__Regla_de_L_Hopital_Soluciones.pdf": "2. Derivadas/Ejercicios/2E. Regla de L'Hopital/Soluciones.pdf",
    "2. Derivadas/Ejercicios/3E. Derivación/Derivadas___Ejercicios__Derivación.pdf": "2. Derivadas/Ejercicios/3E. Derivación/Enunciados.pdf",
    "2. Derivadas/Ejercicios/3E. Derivación/Derivadas___Ejercicios__Derivación_Soluciones.pdf": "2. Derivadas/Ejercicios/3E. Derivación/Soluciones.pdf",

    # Cap 2 — Preguntas
    "2. Derivadas/Preguntas/derivadas.csv": "2. Derivadas/Preguntas/Preguntas.csv",

    # Cap 3 — Clases
    "3. Aplicaciones de las Derivadas/Clases/1. Razones Relacionadas/Aplicaciones_de_la_Derivada___Razones_Relacionadas.pdf": "3. Aplicaciones de las Derivadas/Clases/1. Razones Relacionadas/Clase.pdf",
    "3. Aplicaciones de las Derivadas/Clases/1. Razones Relacionadas/Aplicaciones_de_la_Derivada___Razones_Relacionadas_Apuntes.pdf": "3. Aplicaciones de las Derivadas/Clases/1. Razones Relacionadas/Apuntes.pdf",
    "3. Aplicaciones de las Derivadas/Clases/2. Aproximaciones Lineales y Diferenciales/Aplicaciones_de_la_Derivada___Aproximaciones_Lineales_y_Diferenciales.pdf": "3. Aplicaciones de las Derivadas/Clases/2. Aproximaciones Lineales y Diferenciales/Clase.pdf",
    "3. Aplicaciones de las Derivadas/Clases/2. Aproximaciones Lineales y Diferenciales/Aplicaciones_de_la_Derivada___Aproximaciones_Lineales_y_Diferenciales_Apuntes.pdf": "3. Aplicaciones de las Derivadas/Clases/2. Aproximaciones Lineales y Diferenciales/Apuntes.pdf",
    "3. Aplicaciones de las Derivadas/Clases/3. Máximos y Mínimos/Aplicaciones_de_la_Derivada___Máximos_y_Mínimos.pdf": "3. Aplicaciones de las Derivadas/Clases/3. Máximos y Mínimos/Clase.pdf",
    "3. Aplicaciones de las Derivadas/Clases/3. Máximos y Mínimos/Aplicaciones_de_la_Derivada___Máximos_y_Mínimos_Apuntes.pdf": "3. Aplicaciones de las Derivadas/Clases/3. Máximos y Mínimos/Apuntes.pdf",
    "3. Aplicaciones de las Derivadas/Clases/4. Teorema del Valor Medio/Aplicaciones_de_la_Derivada___Teorema_del_Valor_Medio.pdf": "3. Aplicaciones de las Derivadas/Clases/4. Teorema del Valor Medio/Clase.pdf",
    "3. Aplicaciones de las Derivadas/Clases/4. Teorema del Valor Medio/Aplicaciones_de_la_Derivada___Teorema_del_Valor_Medio_Apuntes.pdf": "3. Aplicaciones de las Derivadas/Clases/4. Teorema del Valor Medio/Apuntes.pdf",
    "3. Aplicaciones de las Derivadas/Clases/5. Forma de la gráfica/Aplicaciones_de_la_Derivada___Forma_de_la_Gráfica.pdf": "3. Aplicaciones de las Derivadas/Clases/5. Forma de la gráfica/Clase.pdf",
    "3. Aplicaciones de las Derivadas/Clases/5. Forma de la gráfica/Aplicaciones_de_la_Derivada___Forma_de_la_Gráfica_Apuntes.pdf": "3. Aplicaciones de las Derivadas/Clases/5. Forma de la gráfica/Apuntes.pdf",
    "3. Aplicaciones de las Derivadas/Clases/6. Graficar curvas/Aplicaciones_de_la_Derivada___Graficar_curvas.pdf": "3. Aplicaciones de las Derivadas/Clases/6. Graficar curvas/Clase.pdf",
    "3. Aplicaciones de las Derivadas/Clases/6. Graficar curvas/Aplicaciones_de_la_Derivada___Graficar_curvas_Apuntes.pdf": "3. Aplicaciones de las Derivadas/Clases/6. Graficar curvas/Apuntes.pdf",
    "3. Aplicaciones de las Derivadas/Clases/7. Optimización/Aplicaciones_de_la_Derivada___Optimización.pdf": "3. Aplicaciones de las Derivadas/Clases/7. Optimización/Clase.pdf",
    "3. Aplicaciones de las Derivadas/Clases/7. Optimización/Aplicaciones_de_la_Derivada___Optimización_Apuntes.pdf": "3. Aplicaciones de las Derivadas/Clases/7. Optimización/Apuntes.pdf",

    # Cap 3 — Ejercicios
    "3. Aplicaciones de las Derivadas/Ejercicios/1E. Razones Relacionadas/Aplicaciones_de_la_Derivada___Ejercicios__Razones_Relacionadas.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/1E. Razones Relacionadas/Enunciados.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/1E. Razones Relacionadas/Aplicaciones_de_la_Derivada___Ejercicios__Razones_Relacionadas_Soluciones.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/1E. Razones Relacionadas/Soluciones.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/2E. Aproximaciones Lineales y Diferenciales/Aplicaciones_de_la_Derivada___Ejercicios__Aproximaciones_Lineales_y_Diferenciales.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/2E. Aproximaciones Lineales y Diferenciales/Enunciados.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/2E. Aproximaciones Lineales y Diferenciales/Aplicaciones_de_la_Derivada___Ejercicios__Aproximaciones_Lineales_y_Diferenciales_Soluciones.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/2E. Aproximaciones Lineales y Diferenciales/Soluciones.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/3E. Teorema del Valor Medio/Aplicaciones_de_la_Derivada___Ejercicios__Teorema_del_Valor_Medio.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/3E. Teorema del Valor Medio/Enunciados.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/3E. Teorema del Valor Medio/Aplicaciones_de_la_Derivada___Ejercicios__Teorema_del_Valor_Medio_Soluciones.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/3E. Teorema del Valor Medio/Soluciones.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/4E. Graficar Curvas/Aplicaciones_de_la_Derivada___Ejercicios__Graficar_Curvas.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/4E. Graficar Curvas/Enunciados.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/4E. Graficar Curvas/Aplicaciones_de_la_Derivada___Ejercicios__Graficar_Curvas_Soluciones.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/4E. Graficar Curvas/Soluciones.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/5E. Optimización/Aplicaciones_de_la_Derivada___Ejercicios__Optimización.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/5E. Optimización/Enunciados.pdf",
    "3. Aplicaciones de las Derivadas/Ejercicios/5E. Optimización/Aplicaciones_de_la_Derivada___Ejercicios__Optimización_Soluciones.pdf": "3. Aplicaciones de las Derivadas/Ejercicios/5E. Optimización/Soluciones.pdf",

    # Cap 3 — Preguntas
    "3. Aplicaciones de las Derivadas/Preguntas/aplicaciones_de_las_derivadas.csv": "3. Aplicaciones de las Derivadas/Preguntas/Preguntas.csv",
}

# --- LECCIÓN dirs (renombrar después de archivos) ---
# Padding 0, sentence-case en español, L'Hôpital con ô, "Funciones hiperbólicas" (lower h)
LESSON_DIR_RENAMES = {
    # Cap 1
    "1. Límites y Continuidad/Clases/1. Introducción intuitiva": "1. Límites y Continuidad/Clases/01. Introducción intuitiva",
    "1. Límites y Continuidad/Clases/2. Definición formal": "1. Límites y Continuidad/Clases/02. Definición formal",
    "1. Límites y Continuidad/Clases/3. Propiedades de los límites": "1. Límites y Continuidad/Clases/03. Propiedades de los límites",
    "1. Límites y Continuidad/Clases/4. Continuidad de funciones": "1. Límites y Continuidad/Clases/04. Continuidad de funciones",
    "1. Límites y Continuidad/Clases/5. Teorema del valor intermedio": "1. Límites y Continuidad/Clases/05. Teorema del valor intermedio",
    "1. Límites y Continuidad/Clases/6. Asíntotas": "1. Límites y Continuidad/Clases/06. Asíntotas",
    "1. Límites y Continuidad/Clases/7. Resolver límites": "1. Límites y Continuidad/Clases/07. Resolver límites",

    # Cap 2 (sentence-case: "Funciones hiperbólicas" no "Hiperbólicas")
    "2. Derivadas/Clases/1. Definición y notación": "2. Derivadas/Clases/01. Definición y notación",
    "2. Derivadas/Clases/2. Derivabilidad": "2. Derivadas/Clases/02. Derivabilidad",
    "2. Derivadas/Clases/3. Reglas de derivación": "2. Derivadas/Clases/03. Reglas de derivación",
    "2. Derivadas/Clases/4. Derivadas trigonométricas": "2. Derivadas/Clases/04. Derivadas trigonométricas",
    "2. Derivadas/Clases/5. Regla de la cadena": "2. Derivadas/Clases/05. Regla de la cadena",
    "2. Derivadas/Clases/6. Derivación implícita": "2. Derivadas/Clases/06. Derivación implícita",
    "2. Derivadas/Clases/7. Derivación logarítmica": "2. Derivadas/Clases/07. Derivación logarítmica",
    "2. Derivadas/Clases/8. Derivadas de funciones inversas": "2. Derivadas/Clases/08. Derivadas de funciones inversas",
    "2. Derivadas/Clases/9. Derivadas de funciones logarítmicas y exponenciales": "2. Derivadas/Clases/09. Derivadas de funciones logarítmicas y exponenciales",
    "2. Derivadas/Clases/10. Regla de L'Hopital": "2. Derivadas/Clases/10. Regla de L'Hôpital",
    "2. Derivadas/Clases/11. Funciones Hiperbólicas": "2. Derivadas/Clases/11. Funciones hiperbólicas",

    # Cap 3 (sentence-case: minúsculas en palabras secundarias)
    "3. Aplicaciones de las Derivadas/Clases/1. Razones Relacionadas": "3. Aplicaciones de las Derivadas/Clases/01. Razones relacionadas",
    "3. Aplicaciones de las Derivadas/Clases/2. Aproximaciones Lineales y Diferenciales": "3. Aplicaciones de las Derivadas/Clases/02. Aproximaciones lineales y diferenciales",
    "3. Aplicaciones de las Derivadas/Clases/3. Máximos y Mínimos": "3. Aplicaciones de las Derivadas/Clases/03. Máximos y mínimos",
    "3. Aplicaciones de las Derivadas/Clases/4. Teorema del Valor Medio": "3. Aplicaciones de las Derivadas/Clases/04. Teorema del valor medio",
    "3. Aplicaciones de las Derivadas/Clases/5. Forma de la gráfica": "3. Aplicaciones de las Derivadas/Clases/05. Forma de la gráfica",
    "3. Aplicaciones de las Derivadas/Clases/6. Graficar curvas": "3. Aplicaciones de las Derivadas/Clases/06. Graficar curvas",
    "3. Aplicaciones de las Derivadas/Clases/7. Optimización": "3. Aplicaciones de las Derivadas/Clases/07. Optimización",
}

# --- EJERCICIO dirs (sin sufijo 'E', padding 0, sentence-case) ---
EXERCISE_DIR_RENAMES = {
    # Cap 1
    "1. Límites y Continuidad/Ejercicios/1E. Definición formal": "1. Límites y Continuidad/Ejercicios/01. Definición formal",
    "1. Límites y Continuidad/Ejercicios/2E. Continuidad": "1. Límites y Continuidad/Ejercicios/02. Continuidad",
    "1. Límites y Continuidad/Ejercicios/3E. Límites al Infinito": "1. Límites y Continuidad/Ejercicios/03. Límites al infinito",
    "1. Límites y Continuidad/Ejercicios/4E. Teorema del Valor Intermedio": "1. Límites y Continuidad/Ejercicios/04. Teorema del valor intermedio",
    "1. Límites y Continuidad/Ejercicios/5E. Asíntotas": "1. Límites y Continuidad/Ejercicios/05. Asíntotas",
    "1. Límites y Continuidad/Ejercicios/6E. Límites": "1. Límites y Continuidad/Ejercicios/06. Límites",

    # Cap 2
    "2. Derivadas/Ejercicios/1E. Derivabilidad": "2. Derivadas/Ejercicios/01. Derivabilidad",
    "2. Derivadas/Ejercicios/2E. Regla de L'Hopital": "2. Derivadas/Ejercicios/02. Regla de L'Hôpital",
    "2. Derivadas/Ejercicios/3E. Derivación": "2. Derivadas/Ejercicios/03. Derivación",

    # Cap 3
    "3. Aplicaciones de las Derivadas/Ejercicios/1E. Razones Relacionadas": "3. Aplicaciones de las Derivadas/Ejercicios/01. Razones relacionadas",
    "3. Aplicaciones de las Derivadas/Ejercicios/2E. Aproximaciones Lineales y Diferenciales": "3. Aplicaciones de las Derivadas/Ejercicios/02. Aproximaciones lineales y diferenciales",
    "3. Aplicaciones de las Derivadas/Ejercicios/3E. Teorema del Valor Medio": "3. Aplicaciones de las Derivadas/Ejercicios/03. Teorema del valor medio",
    "3. Aplicaciones de las Derivadas/Ejercicios/4E. Graficar Curvas": "3. Aplicaciones de las Derivadas/Ejercicios/04. Graficar curvas",
    "3. Aplicaciones de las Derivadas/Ejercicios/5E. Optimización": "3. Aplicaciones de las Derivadas/Ejercicios/05. Optimización",
}

# --- CAPÍTULO dirs (al final, ya con todo dentro renombrado) ---
CHAPTER_DIR_RENAMES = {
    "1. Límites y Continuidad": "01. Límites y Continuidad",
    "2. Derivadas": "02. Derivadas",
    "3. Aplicaciones de las Derivadas": "03. Aplicaciones de las Derivadas",
}


# ============================================================
# Ejecución
# ============================================================
def _nfd(s):
    return unicodedata.normalize("NFD", s)


def _resolve_actual_path(target_abs):
    """Encuentra el path real en disco para target_abs, tolerando NFC vs NFD.
    Si existe directamente, devuelve target_abs. Si no, busca en el parent
    un hijo cuyo nombre NFD-normalizado coincida y devuelve ese path real.
    Devuelve None si no encuentra nada."""
    if target_abs.exists():
        return target_abs
    parent = target_abs.parent
    if not parent.exists():
        return None
    target_nfd = _nfd(target_abs.name)
    for child in parent.iterdir():
        if _nfd(child.name) == target_nfd:
            return child
    return None


def _is_case_only_diff(a, b):
    """True si a y b sólo difieren en mayúsculas/minúsculas."""
    return a != b and a.lower() == b.lower()


def git_mv(old_rel, new_rel, dry_run):
    old_abs = BASE / old_rel
    new_abs = BASE / new_rel
    if old_rel == new_rel:
        return ("skip", "ya tiene ese nombre")

    # Resolver el path real en disco (maneja NFC/NFD)
    actual_old = _resolve_actual_path(old_abs)
    if actual_old is None:
        return ("missing", f"{old_abs} no existe (ni en NFC ni NFD)")

    # Detectar si es un rename case-only — Windows no lo ve como conflicto
    case_only = _is_case_only_diff(old_abs.name, new_abs.name) and old_abs.parent == new_abs.parent
    if new_abs.exists() and not case_only:
        # Verificar también con NFD por si acaso
        actual_new = _resolve_actual_path(new_abs)
        if actual_new is not None and actual_new != actual_old:
            return ("conflict", f"{new_abs} ya existe")

    if dry_run:
        return ("dry", f"{old_rel}  →  {new_rel}{'  [case-only]' if case_only else ''}")

    # Los PDFs no están trackeados por git, así que usamos os.rename directo.
    # Para case-only en Windows: rename a un nombre temporal primero, luego al final.
    try:
        if case_only:
            tmp = new_abs.parent / (actual_old.name + ".__tmp__")
            os.rename(str(actual_old), str(tmp))
            os.rename(str(tmp), str(new_abs))
        else:
            os.rename(str(actual_old), str(new_abs))
    except OSError as e:
        return ("error", f"{e}")
    return ("ok", f"{old_rel}  →  {new_rel}")


def run_phase(name, mapping, dry_run):
    print(f"\n=== {name} ({len(mapping)} renames) ===")
    counts = {"ok": 0, "dry": 0, "skip": 0, "missing": 0, "conflict": 0, "error": 0}
    for old, new in mapping.items():
        status, msg = git_mv(old, new, dry_run)
        counts[status] += 1
        prefix = {
            "ok": "✓",
            "dry": " ",
            "skip": "·",
            "missing": "✗",
            "conflict": "!",
            "error": "✗",
        }[status]
        print(f"  {prefix} {msg}")
    return counts


def main():
    apply_mode = "--apply" in sys.argv

    if not BASE.exists():
        print(f"ERROR: no existe {BASE}")
        sys.exit(1)

    mode_label = "APPLY (git mv real)" if apply_mode else "DRY-RUN"
    print(f"Modo: {mode_label}")
    print(f"Base: {BASE}")

    # Orden importa: archivos dentro de carpetas viejas → leccion/ejercicio dirs → capítulo dirs
    all_counts = {"ok": 0, "dry": 0, "skip": 0, "missing": 0, "conflict": 0, "error": 0}
    for name, mapping in [
        ("FASE 1 — archivos (dentro de dirs originales)", FILE_RENAMES),
        ("FASE 2 — carpetas de lección", LESSON_DIR_RENAMES),
        ("FASE 3 — carpetas de ejercicios", EXERCISE_DIR_RENAMES),
        ("FASE 4 — carpetas de capítulo", CHAPTER_DIR_RENAMES),
    ]:
        c = run_phase(name, mapping, dry_run=not apply_mode)
        for k, v in c.items():
            all_counts[k] += v

    print()
    print("=" * 60)
    print(f"Resumen: {all_counts}")
    if not apply_mode:
        print()
        print("Para ejecutar de verdad:  python scripts/rename_calculo_diferencial.py --apply")


if __name__ == "__main__":
    main()
