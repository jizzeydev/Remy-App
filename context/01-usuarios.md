# Usuarios y Personas

## 1. Estudiante universitario (usuario principal)
**Quién es:** Alumno de primeros años de carreras STEM en Chile (ingeniería, ciencias, comercial con cálculo). Cursando ramos como Cálculo I/II, Álgebra Lineal, Física, Ecuaciones Diferenciales.

**Pain points:**
- Llega mal preparado del colegio a ramos exigentes.
- Profesores universitarios no siempre explican bien o el ritmo es muy rápido.
- Pocos materiales de práctica reales (controles/exámenes de su universidad).
- Estudiar solo es difícil; no sabe en qué está fallando.

**Lo que busca en Remy:**
- Practicar con preguntas tipo evaluación real, no ejercicios genéricos.
- Ver soluciones paso a paso con notación matemática correcta (LaTeX).
- Saber cuánto está avanzando y qué temas tiene flojos.
- Acceso 24/7, sin agendar hora con un profe.

**Flujo típico:**
Landing → Auth (Google) → Trial 7 días → Elegir universidad/curso → Hacer simulacro → Ver resultados → Suscribirse → Estudiar capítulos → Repetir.

## 2. Admin (Se Remonta)
**Quién es:** Equipo de Se Remonta (Jesús + profesores). Login con `seremonta.cl@gmail.com`.

**Responsabilidades:**
- Crear y mantener contenido: universidades, cursos, capítulos, lecciones, evaluaciones, preguntas.
- Cargar preguntas masivamente vía importación CSV (las genera offline con sus propias herramientas).
- Gestionar usuarios: otorgar/revocar/extender accesos manuales.
- Monitorear métricas: ingresos, suscripciones activas, MRR, simulacros realizados.
- Ajustar precios desde el panel (`/admin/pricing`) sin tocar código.

**Herramientas en el panel admin:**
- `/admin/users` — gestión de usuarios y accesos
- `/admin/universities` — CRUD de universidades, cursos, evaluaciones, preguntas
- `/admin/pricing` — precios dinámicos
- Dashboard con KPIs y gráficos

## 3. Usuario sin suscripción (lead)
- Llega por landing, ve pricing, puede registrarse y obtiene 7 días de trial.
- Si no paga, queda con cuentas con candados visuales en cursos y banner "Suscribirse para acceder".
- Sigue siendo addressable para emails de remarketing (Resend) y para conversión posterior.
