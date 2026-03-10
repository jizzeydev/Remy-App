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

## Credenciales

### Admin
- **Username:** admin
- **Password:** #Alex060625

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
- Backend API Tests: ✅ 100% (17/17)
- Frontend UI Tests: ✅ 100%
- Auth Flow: ✅ Completo
- Payment Flow: ✅ Completo (TEST mode)
- Admin Management: ✅ Completo

## Backlog (Post-MVP)

### P1 - Mejoras
- [ ] Refactorizar server.py en routers separados
- [ ] Dashboard admin con métricas de ingresos
- [ ] Password reset functionality
- [ ] Email de confirmación de suscripción

### P2 - Futuro
- [ ] Tutor IA Remy 24/7
- [ ] Exportar contenido a PDF
- [ ] Push notifications
- [ ] App móvil

## Notas para Producción

1. **Mercado Pago:** Cambiar de TEST a PRODUCTION credentials
2. **Webhooks:** Configurar URL de webhook en dashboard de MP
3. **Dominio:** Actualizar `FRONTEND_URL` en backend/.env
4. **SSL:** Asegurar HTTPS para pagos seguros
5. **Monitoreo:** Implementar logging de errores de pago
