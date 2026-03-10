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

## Core Architecture
```
/app/
├── backend/
│   ├── server.py          # Main FastAPI app (monolito)
│   ├── routes/
│   │   ├── auth.py        # Student auth (Google + Email)
│   │   ├── payments.py    # Mercado Pago subscriptions
│   │   └── admin_users.py # Admin user management
│   ├── services/
│   │   └── mercadopago_service.py
│   └── models/
│       └── user.py
└── frontend/
    ├── src/
    │   ├── App.js         # Router with protected routes
    │   ├── contexts/
    │   │   └── AuthContext.js  # Auth state management
    │   ├── pages/
    │   │   ├── Landing.js      # Sales page
    │   │   ├── AuthPage.js     # Login/Register
    │   │   ├── AuthCallback.js # Google OAuth callback
    │   │   └── admin/
    │   │       └── AdminUsers.js # User management
    │   └── components/
    │       ├── Layout.js       # Student layout with auth
    │       └── AdminLayout.js  # Admin layout
```

## Implemented Features

### ✅ Authentication System (NEW - March 10, 2026)
- [x] Email/Password registration with bcrypt
- [x] Email/Password login with JWT sessions
- [x] Google OAuth via Emergent Auth redirect
- [x] Session management with httpOnly cookies
- [x] Protected routes for students (/biblioteca, /simulacros, etc.)
- [x] AuthContext for frontend state management
- [x] Logout functionality

### ✅ Admin User Management (NEW - March 10, 2026)
- [x] User list with pagination, search, and filter
- [x] User statistics dashboard (total, active, by type)
- [x] Grant manual access to private students (1-12 months)
- [x] Revoke manual access
- [x] Extend subscription duration
- [x] View user subscription history

### ✅ Payment Infrastructure (PARTIAL - March 10, 2026)
- [x] Mercado Pago SDK integration
- [x] Subscription plans endpoint (monthly $9.990, semestral $29.990)
- [x] PreApproval creation endpoint
- [x] Webhook handler for payment notifications
- [ ] Frontend card tokenization (requires Mercado Pago JS SDK)
- [ ] Subscription flow UI

### ✅ Landing Page
- [x] Hero section with CTA buttons (now linked to /auth)
- [x] Features showcase
- [x] Course preview with locked content
- [x] Pricing cards with subscription plans
- [x] Navigation bar with login/register buttons

### ✅ Admin BackOffice (Complete)
- [x] Admin JWT authentication
- [x] CRUD for Courses, Chapters, Lessons, Questions
- [x] AI-assisted content generation (GPT-5.2)
- [x] Chat with Remy for iterative editing
- [x] Image generation and upload
- [x] Question bank reorganized by course/chapter

### ✅ Student Application (Complete)
- [x] Course library (Biblioteca) with progress bars
- [x] Course/Chapter/Lesson viewer
- [x] Markdown + KaTeX + Desmos rendering
- [x] Simulacros with custom creation options
- [x] Chilean grading scale (1-7)
- [x] Quiz timer with countdown
- [x] Progress tracking per lesson

## Database Collections

### Users (NEW)
```javascript
{
  user_id: "user_xxx",
  email: "user@email.com",
  name: "Name",
  picture: "url",
  auth_provider: "google" | "email" | "manual",
  password_hash: "...",
  subscription_status: "active" | "inactive" | "cancelled" | "expired",
  subscription_type: "mercadopago" | "manual",
  subscription_plan: "monthly" | "semestral",
  subscription_id: "preapproval_xxx",
  subscription_start: ISODate,
  subscription_end: ISODate,
  created_at: ISODate
}
```

### User Sessions (NEW)
```javascript
{
  session_id: "session_xxx",
  user_id: "user_xxx",
  session_token: "sess_xxx",
  expires_at: ISODate,
  created_at: ISODate
}
```

### Subscriptions (NEW)
```javascript
{
  id: "sub_xxx",
  user_id: "user_xxx",
  user_email: "...",
  plan: "monthly" | "semestral",
  subscription_type: "mercadopago" | "manual",
  mercadopago_id: "...",
  amount: 9990,
  currency: "CLP",
  status: "active" | "pending" | "cancelled",
  start_date: ISODate,
  end_date: ISODate,
  created_at: ISODate
}
```

### Existing Collections
- `courses`, `chapters`, `lessons`, `questions`, `quiz_attempts`, `progress`

## API Endpoints

### Authentication (NEW)
- `POST /api/auth/register` - Email registration
- `POST /api/auth/login` - Email login
- `POST /api/auth/google/session` - Process Google OAuth
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Payments (NEW)
- `GET /api/payments/plans` - Get subscription plans
- `POST /api/payments/subscribe` - Create subscription
- `GET /api/payments/subscription` - Get subscription status
- `POST /api/payments/cancel` - Cancel subscription
- `POST /api/payments/webhook/mercadopago` - Webhook handler

### Admin Users (NEW)
- `GET /api/admin/users` - List users (paginated, searchable)
- `GET /api/admin/users/stats` - User statistics
- `GET /api/admin/users/{id}` - User details
- `POST /api/admin/users/grant-access` - Grant manual access
- `POST /api/admin/users/{id}/revoke-access` - Revoke access
- `POST /api/admin/users/{id}/extend-access` - Extend subscription

### Student Routes (Protected)
- `GET /api/courses`, `/api/lessons/{id}`, etc.

### Admin Routes (Protected)
- CRUD endpoints for courses, chapters, lessons, questions

## Credentials
- **Admin**: username=admin, password=#Alex060625
- **Test User**: test@example.com / test123
- **Manual User**: estudiante.privado@test.com (active subscription)
- **Mercado Pago TEST**: 
  - Public Key: TEST-0aa3843b-15cc-4312-9f09-5309dcf07002
  - Access Token: TEST-1254600887824978-030919-2172d8bba8bf6f32aab73fbc82d3dee9-820370254

## Application Routes
- `/` - Landing page (public)
- `/auth` - Login/Register page (public)
- `/auth/callback` - Google OAuth callback
- `/biblioteca` - Student dashboard (protected)
- `/simulacros` - Quiz practice (protected)
- `/course/:id` - Course viewer (protected)
- `/lesson/:id` - Lesson viewer (protected)
- `/progreso` - Progress page (protected)
- `/admin/login` - Admin login
- `/admin/dashboard` - Admin dashboard
- `/admin/courses` - Course management
- `/admin/questions` - Question bank
- `/admin/users` - **NEW** User management

## Pricing
- Plan Mensual: $9.990 CLP/mes
- Plan Semestral: $29.990 CLP/6 meses (50% descuento)

## Testing Status (March 10, 2026)
- Email Registration/Login: ✅ PASS
- Session Management: ✅ PASS
- Protected Routes: ✅ PASS (redirects to /auth)
- Admin User List: ✅ PASS (with auth)
- Admin User Stats: ✅ PASS (with auth)
- Admin Grant Access: ✅ PASS
- Payment Plans API: ✅ PASS
- Auth Page UI: ✅ PASS
- Admin Users UI: ✅ PASS
- Security Fix: ✅ Admin endpoints now require authentication

## Next Steps (P0 - In Progress)
- [ ] Complete Mercado Pago frontend integration (card tokenization)
- [ ] Subscription UI flow in Landing/Auth pages
- [ ] Email verification for new users (optional)

## Backlog (P1)
- [ ] Refactor server.py into multiple routers
- [ ] Admin dashboard with revenue metrics
- [ ] Password reset functionality
- [ ] Email notifications for subscription events

## Future Tasks (P2)
- [ ] Tutor IA Remy 24/7
- [ ] Export content to PDF
- [ ] Push notifications
- [ ] Mobile app
