# Remy - Plataforma Educativa de Se Remonta

## Problem Statement
App educativa para "Se Remonta" con las siguientes características:
- **BackOffice Admin**: Panel de administración para crear y gestionar contenido educativo usando GPT-5.2
- **Vista de Estudiantes**: Visualización de cursos, lecciones con LaTeX/KaTeX, Desmos interactivo, y simulacros de práctica
- **Sistema de Suscripciones**: Pagos recurrentes con Mercado Pago + gestión manual de accesos

## User Personas
1. **Admin (Se Remonta)**: Crea contenido educativo, genera resúmenes y preguntas con AI, gestiona usuarios/suscripciones
2. **Estudiantes**: Visualizan cursos, realizan simulacros, consultan progreso, pagan suscripciones

## Tech Stack
- **Frontend**: React, React Router, Tailwind CSS, Shadcn/UI, KaTeX (LaTeX), Desmos
- **Backend**: FastAPI, MongoDB (motor), JWT Auth, bcrypt
- **AI**: GPT-5.2 (contenido), GPT Image 1 (imágenes) via emergentintegrations
- **Auth**: Google OAuth (Emergent Auth) + Email/Password con sesiones
- **Pagos**: Mercado Pago (Chile) - Suscripciones recurrentes

## MVP Comercial - COMPLETADO ✅

### ✅ Sistema de Pagos (Mercado Pago) - IMPLEMENTADO
- [x] SDK de Mercado Pago integrado en frontend
- [x] Página de checkout `/subscribe` con selección de planes
- [x] Formulario de pago con campos de tarjeta
- [x] Tokenización de tarjeta client-side
- [x] Backend para crear suscripciones (PreApproval)
- [x] Webhook handler para notificaciones de pago
- [x] Plans: Mensual $9.990, Semestral $29.990 CLP

### ✅ Sistema de Autenticación - IMPLEMENTADO
- [x] Email/Password registration con bcrypt
- [x] Email/Password login con sesiones JWT
- [x] Google OAuth via Emergent Auth
- [x] Cookies httpOnly seguras
- [x] Rutas protegidas con redirección
- [x] Parámetro redirect después de login

### ✅ Gestión de Usuarios Admin - IMPLEMENTADO
- [x] Panel `/admin/users` con lista paginada
- [x] Estadísticas de usuarios y suscripciones
- [x] Otorgar acceso manual (1-12 meses)
- [x] Revocar/Extender accesos

### ✅ Integración Landing-Auth-Payment - IMPLEMENTADO
- [x] Botones de pricing redirigen a auth con plan preseleccionado
- [x] Auth respeta parámetro redirect
- [x] Subscribe page carga plan desde URL
- [x] Biblioteca muestra banner de suscripción
- [x] Candados en cursos para no suscriptores

## Flujo de Usuario

```
Usuario Nuevo:
1. Landing page (/) → Ver pricing
2. Click "Suscribirse" → /auth?redirect=/subscribe?plan=monthly
3. Crear cuenta o Google OAuth
4. Redirect a /subscribe?plan=monthly (preseleccionado)
5. Ingresar datos de tarjeta → Crear suscripción
6. Redirect a /biblioteca?subscription=success
7. Acceso completo a cursos y simulacros

Usuario sin Suscripción:
- Ve banner "Desbloquea todo el contenido"
- Cursos con candado
- Botón "Suscribirse para acceder"

Usuario con Suscripción Activa:
- Badge "Suscripción activa - Acceso completo"
- Sin candados
- Botón "Comenzar/Continuar"
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Registro con email
- `POST /api/auth/login` - Login con email
- `POST /api/auth/google/session` - OAuth de Google
- `GET /api/auth/me` - Usuario actual
- `POST /api/auth/logout` - Cerrar sesión

### Payments
- `GET /api/payments/plans` - Planes disponibles
- `POST /api/payments/subscribe` - Crear suscripción
- `GET /api/payments/subscription` - Estado de suscripción
- `POST /api/payments/cancel` - Cancelar suscripción
- `POST /api/payments/webhook/mercadopago` - Webhooks

### Admin Users
- `GET /api/admin/users` - Lista de usuarios
- `GET /api/admin/users/stats` - Estadísticas
- `POST /api/admin/users/grant-access` - Otorgar acceso manual
- `POST /api/admin/users/{id}/revoke-access` - Revocar acceso
- `POST /api/admin/users/{id}/extend-access` - Extender acceso

### Admin AI Content Generation (Async)
- `POST /api/admin/generate-lesson-content/start` - Inicia generación asíncrona (retorna task_id)
- `GET /api/admin/generate-lesson-content/status/{task_id}` - Polling de estado (pending|processing|completed|error)

## Credenciales

### Admin
- **Username:** admin
- **Password:** #Alex060625
- **Google Login:** seremonta.cl@gmail.com (authorized)

### Test User
- **Email:** test@example.com
- **Password:** test123
- **Status:** Sin suscripción activa

### Mercado Pago (TEST)
- **Public Key:** TEST-0aa3843b-15cc-4312-9f09-5309dcf07002
- **Access Token:** (en backend/.env)
- **Test Cards:** https://www.mercadopago.cl/developers/es/docs/checkout-api/integration-test/test-cards

## Pricing
- **Plan Mensual:** $9.990 CLP/mes
- **Plan Semestral:** $29.990 CLP/6 meses (50% descuento)

## Testing Status (March 10, 2026)
- Backend API Tests: ✅ 100%
- Frontend UI Tests: ✅ 100%
- Auth Flow: ✅ Google Only (email/password eliminado)
- Payment Flow: ✅ Completo (Production mode)
- Admin Management: ✅ Completo
- Email Notifications: ✅ Implementado (Resend)

## Production Deployment

### ✅ Email Notifications - IMPLEMENTADO (March 10, 2026)
- [x] Integración con Resend API
- [x] Notificación admin: nuevo usuario registrado
- [x] Notificación admin: suscripción iniciada (Mercado Pago)
- [x] Notificación admin: suscripción cancelada
- [x] Email bienvenida al usuario nuevo
- [x] Templates HTML profesionales

### ✅ Solo Google Auth - IMPLEMENTADO (March 10, 2026)
- [x] Eliminado registro email/password (roto)
- [x] Simplificada página /auth solo con Google
- [x] Sesiones extendidas a 30 días

### ✅ Admin Dashboard Metrics - IMPLEMENTADO (March 10, 2026)
- [x] Métricas de ingresos del período seleccionado
- [x] Contador de suscripciones activas
- [x] Selector de rango de fechas (hoy, semana, mes, mes anterior, 3/6 meses, año)
- [x] Gráfico de ingresos mensuales (últimos 6 meses)
- [x] Desglose por estado de suscripción y tipo (Mercado Pago vs Manual)
- [x] Fix: verify_admin_token acepta tokens de Google admin

### ✅ Session Persistence - IMPLEMENTADO (March 10, 2026)
- [x] Token almacenado en localStorage (`remy_session_token`)
- [x] Backend acepta Bearer token en header Authorization
- [x] Sesión persiste al recargar página
- [x] Landing y Auth redirigen usuarios autenticados a /dashboard

### ✅ Admin Google Login - IMPLEMENTADO (March 10, 2026)
- [x] Endpoint `/api/admin/google-login` creado
- [x] Verifica que email sea `seremonta.cl@gmail.com`
- [x] Genera JWT token para sesión de admin
- [x] `verify_admin_token` actualizado para aceptar tokens Google
- [x] Botón "Continuar con Google" en UI de admin login

### ✅ Script de Migración - CREADO (March 10, 2026)
- [x] `/app/backend/migration.py` para exportar/importar datos
- [x] Exporta: courses, chapters, lessons, questions, formulas
- [x] Datos exportados a `/app/backend/migration_data/`
- [x] Instrucciones claras para importar en producción

### Credenciales de Producción (CONFIGURADAS)
- **Mercado Pago:** Credenciales de producción en backend/.env
- **Webhook URL:** `https://remy.seremonta.store/api/payments/webhook/mercadopago`
- **Admin Google Email:** seremonta.cl@gmail.com

## ✅ Sistema de Trial Gratuito - IMPLEMENTADO (March 16, 2026)
- [x] 7 días de trial para usuarios nuevos
- [x] Límite de 10 simulaciones durante trial
- [x] Banners de trial en dashboard
- [x] Conversión automática a no-suscrito al expirar

## ✅ Sistema de Precios Dinámicos - IMPLEMENTADO (March 16, 2026)
- [x] Panel admin `/admin/pricing` para gestionar precios
- [x] Hook `usePricing` centralizado en frontend
- [x] Precios dinámicos en landing y suscripción
- [x] Eliminados hardcodes de precios

## ✅ Sistema de Universidades (Backend) - IMPLEMENTADO (March 16, 2026)
- [x] CRUD completo: Universidades → Cursos → Evaluaciones → Preguntas
- [x] Upload de logos de universidades
- [x] Generación de preguntas con IA (Emergent LLM)
- [x] Extracción de texto de PDFs
- [x] Estadísticas de contenido
- [x] Tests 100% pasando

## Backlog (Post-MVP)

### P0 - En Progreso
- [ ] Frontend Admin para gestionar Universidades (UI)
- [ ] Dashboard de métricas con gráficos (conectar backend analytics)

### P1 - Próximo
- [ ] Sección "Tu Universidad" para estudiantes
- [ ] Editor de texto enriquecido (LaTeX/Markdown) para preguntas
- [ ] Configuración de OPENAI_API_KEY desde admin

### P2 - Futuro
- [ ] Refactorizar server.py en routers separados
- [ ] Tutor IA Remy 24/7
- [ ] Emails de recordatorio de suscripción
- [ ] Testimonios en landing page
- [ ] Modo oscuro
- [ ] Gamificación (badges, logros)

## Notas para Producción

1. **Admin Login:** Usar Google con email seremonta.cl@gmail.com
2. **Migración de Datos:**
   - Los datos están exportados en `/app/backend/migration_data/`
   - Para importar en producción: `python migration.py import`
3. **Webhooks:** Configurar URL `https://remy.seremonta.store/api/payments/webhook/mercadopago` en dashboard de Mercado Pago
4. **SSL:** HTTPS ya configurado en producción
5. **Monitoreo:** Implementar logging de errores de pago
