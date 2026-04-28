# Estado Actual y Roadmap

> Snapshot a abril 2026. Para detalle granular ver `memory/PRD.md` y `memory/CHANGELOG.md`.

## Cambio mayor reciente: eliminación completa de IA (2026-04-25)

Toda la integración con IA fue removida del producto en una sola pasada. Lo que se eliminó:

**Backend:**
- Endpoints `/api/admin/generate-summary`, `/generate-questions`, `/generate-lesson-content/*`, `/edit-lesson-content`, `/edit-question-content`, `/generate-image`, `/upload-pdf`.
- Endpoint `/api/admin/universities/.../generate` (generación IA por evaluación).
- Helpers `get_gpt_chat`, `get_gemini_chat`, `_generate_lesson_content_task`, `extract_text_from_pdf`, `get_openai_client`, `generate_questions_with_ai`.
- Dependencias: `emergentintegrations` y `PyPDF2` quitadas de `requirements.txt`.
- Variable de entorno `EMERGENT_LLM_KEY` eliminada.

**Frontend:**
- Página `Chat.js` (huérfana, no estaba en routing).
- Componente `RemyChat.js`.
- Botones "Generar con IA", "Generar Imagen con IA", diálogos de generación, polling de tareas async, flujo de revisión de preguntas IA.
- Copy de marketing en `Home.js` y `design_guidelines.json` que prometía IA / tutor 24/7.

**Por qué:** Jesús (dueño de Se Remonta) decidió que Remy debe ser una plataforma de estudio sin IA en cara visible. La IA se usa offline para generar contenido, que luego se carga al admin vía CRUD manual o importación CSV.

## Lo que ya está en producción ✅

### Comercial
- Auth solo Google (email/password fue eliminado por bugs).
- Mercado Pago en modo producción (mensual / semestral).
- Trial de 7 días con límite de 10 simulaciones.
- Precios dinámicos editables desde admin.
- Emails transaccionales con Resend (bienvenida, alertas admin de nuevo registro / suscripción / cancelación).

### Contenido
- Sistema completo Universidades → Cursos → Evaluaciones → Preguntas.
- Importación CSV de preguntas con plantilla descargable.
- Imágenes en Cloudinary (URLs permanentes, optimización automática).
- KaTeX en preguntas, opciones y soluciones.

### UX estudiante
- Página "Tu Universidad" con flujo Universidad → Curso → Evaluación → Quiz.
- Quiz interactivo con navegación.
- Pantalla de resultados con soluciones.
- Modo oscuro (toggle persistente).

### Admin
- Dashboard con KPIs, gráficos, métricas de conversión, MRR.
- Login admin con Google (verificado contra `seremonta.cl@gmail.com`).
- Gestión de usuarios y accesos manuales.

### Calidad
- Backend compila sin errores tras la limpieza de IA.
- Sesión persistente (30 días, localStorage + httpOnly cookie).

## Pendiente / Backlog

### P0 (próximo)
- Levantar la app en local desde Claude Code (MongoDB + venv + yarn — ver [docs/CREDENCIALES_LOCAL.md](../docs/CREDENCIALES_LOCAL.md)).
- Refactorizar `server.py` en módulos / routers separados.

### P1
- Historial de simulaciones del estudiante (UI).
- Mejorar workflow de carga masiva (preview antes de importar CSV).

### P2 (a futuro)
- Emails de recordatorio de suscripción (renovación, upsell).
- Testimonios en landing.
- Gamificación: badges, logros (la paleta ya tiene color accent reservado para esto).
- App móvil nativa.
- Modo offline.
- Foros / sesiones grupales.

## Decisiones / aprendizajes registrados

- **Cero IA en producto** (2026-04-25). Decisión de producto, no técnica. Ver sección "Cambio mayor reciente" arriba.
- **Email/password se eliminó** porque la implementación estaba rota y mantenerlo no aportaba conversión vs. Google OAuth.
- **Cloudinary reemplazó al storage previo** porque las URLs anteriores expiraban y se perdían imágenes de preguntas.
- **MP en modo producción** implica que cualquier prueba de pago real cobra. Para QA usar las tarjetas de prueba de MP solo en ambiente de test (credenciales separadas).
- **Webhook URL** está fijada en el dashboard de MP — si se mueve el dominio, hay que reconfigurarlo allá.

## Credenciales y referencias rápidas

- Producción: `https://remy.seremonta.store`
- Admin: login con Google `seremonta.cl@gmail.com`
- Cloudinary cloud: `de7loz0sr`
- Datos exportados: `backend/migration_data/`
- Credenciales locales detalladas: [`docs/CREDENCIALES_LOCAL.md`](../docs/CREDENCIALES_LOCAL.md)
