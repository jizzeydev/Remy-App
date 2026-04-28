# Remy App — Visión del Proyecto

## Qué es Remy
Remy es una **plataforma web educativa** desarrollada por la PyME chilena **Se Remonta** (seremonta.cl / seremonta.store). Está pensada para que **estudiantes universitarios** preparen sus ramos más difíciles —principalmente Cálculo I y II, Álgebra Lineal, Física y matemáticas afines— mediante tres pilares:

1. **Estudio guiado** por curso, capítulo y lección, con contenido renderizado en LaTeX/KaTeX y gráficos interactivos (Desmos).
2. **Simulacros desde un banco de preguntas curado** por curso. Las preguntas se cargan al admin manualmente o vía importación CSV; Remy las selecciona aleatoriamente para armar quizzes.
3. **Seguimiento de progreso**: estadísticas, racha de estudio, lecciones completadas, promedio, métricas por curso.

> **Nota:** Remy no usa IA en producto. Jesús puede generar contenido offline con sus propias herramientas y luego subirlo vía CSV o crearlo manualmente en el admin.

## Propuesta de valor
- **Para el estudiante**: una sola herramienta para repasar teoría, practicar con simulacros realistas y ver cuánto avanza — accesible 24/7.
- **Para Se Remonta**: convierte el conocimiento de los profesores (clases particulares, Preu SR, cursos online) en un producto SaaS recurrente que escala sin requerir 1:1 humano para cada alumno.

## Modelo de negocio
Suscripción recurrente en Mercado Pago:
- **Mensual**: $9.990 CLP/mes
- **Semestral**: $29.990 CLP/6 meses (≈ 50% descuento)
- **Trial**: 7 días gratis con límite de 10 simulaciones
- Acceso manual otorgable por admin (1–12 meses) para casos especiales (alumnos de clases particulares, becas, etc.)

## Encaje con el ecosistema Se Remonta
Remy es **uno de los 4 servicios** de Se Remonta:
1. Clases particulares (1:1)
2. Cursos online (seremonta.store)
3. **Remy** (suscripción — este proyecto)
4. Preu SR (gratuito)

Remy es la apuesta de producto digital recurrente: monetiza el flujo de alumnos que ya están en el embudo de Se Remonta y captura nuevos por SEO/contenido sin depender de horas de profesor.

## Estado actual (resumen)
MVP comercial **completo y desplegado** en `https://remy.seremonta.store`. Auth con Google, pagos en producción, panel admin, sistema de universidades→cursos→evaluaciones→preguntas, importación CSV, modo oscuro, métricas. Para el detalle ver [05-estado-actual.md](05-estado-actual.md).
