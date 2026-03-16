# Changelog - Remy Platform

## [March 16, 2026] - Centralized Dynamic Pricing

### Added
- **`usePricing` Hook** (`/app/frontend/src/hooks/usePricing.js`)
  - Centralized pricing data management
  - Fetches prices from `/api/payments/plans` API
  - Provides `formatPrice()` utility function
  - Returns `monthly`, `semestral` plan objects with all metadata
  - Falls back to default values only if API fails

- **`PricingProvider` Context** - Wraps app to provide pricing data globally

### Changed
- **ALL pricing displays now use `usePricing` hook:**
  - `Landing.js` - Pricing section
  - `SubscriptionRequired.js` - Premium paywall
  - `Biblioteca.js` - Subscription banner
  - `MiSuscripcion.js` - Plan selection and details

### Removed
- All hardcoded price values (`$9.990`, `$29.990`, `$59.940`)
- Fallback price arrays in individual components

### Technical Notes
- Prices now update instantly when admin changes them
- No code deployment needed to change prices
- Discount badges show automatically when `discount_active: true`
- Original price crossed out when `original_amount` is set

---

## [March 16, 2026] - Admin Pricing Management

### Added
- **New Admin Page: `/admin/pricing`**
  - Edit monthly and semester plan prices
  - Configure discount percentages
  - Enable/disable discounts
  - Set promotion start and end dates (for CyberDay, CyberMonday, etc.)
  - Mark plans as "popular"
  - Manage features list for each plan
  - Live preview mode to see how prices will appear on landing page
  - Reset to default values button

- **New API Endpoints:**
  - `GET /api/payments/admin/pricing` - Get current pricing configuration
  - `PUT /api/payments/admin/pricing` - Update pricing configuration
  - `POST /api/payments/admin/pricing/reset` - Reset to default values

- **Database Storage:**
  - Pricing config stored in `pricing_config` collection
  - Supports promotional dates with automatic activation/deactivation
  - Falls back to default values if no config in database

### Changed
- **`GET /api/payments/plans` endpoint** now reads from database
  - Returns `original_amount` and `discount` when active
  - Automatic discount calculation based on percentage or fixed final price
  - Date-based promotion activation (promotion_start, promotion_end)

---

## [March 12, 2026] - Landing Page Redesign

### Changed
- **Complete Landing Page Refactor**
  - Removed all AI tutor references - Remy is now positioned as a "study platform"
  - New hero message: "Remonta tus ramos con la mejor plataforma de estudio para la universidad"
  - New subtitle focusing on: lecciones claras, simulacros personalizados, preguntas adaptadas

### Added
- **Problem Section**: "Estudiar matemáticas en la universidad no debería ser tan caótico"
  - Before/After comparison: PDFs desordenados vs Remy organizado
  - Highlight box explaining Remy's value proposition

- **Features Section** (4 features):
  1. Simulacros de Prueba
  2. Lecciones de Calidad
  3. Práctica tipo Examen
  4. Progreso y Correcciones Inteligentes

- **Simulation Section**: "Practica como si estuvieras en un examen real"
  - Benefits: práctica rápida, preguntas variadas, entrenamiento tipo examen

- **Final CTA Section**: "Empieza a estudiar matemáticas de forma más inteligente"

### Dynamic Content
- **Courses Section**: Loads dynamically from backend API (`/api/courses`)
- **Pricing Section**: Loads dynamically from backend API (`/api/payments/plans`)
  - Supports original/discounted prices
  - Shows discount percentage automatically
  - "MÁS POPULAR" badge for semestral plan

---

## [March 12, 2026] - AI Content Generation Fix (Background Tasks)

### Fixed
- **504 Gateway Timeout on AI Content Generation** 
  - The `/api/admin/generate-lesson-content` endpoint was timing out in production due to LLM response time exceeding proxy timeout limits
  - Implemented background task system with polling:
    - New endpoint `POST /api/admin/generate-lesson-content/start` - Starts async task, returns `task_id` immediately
    - New endpoint `GET /api/admin/generate-lesson-content/status/{task_id}` - Poll for completion status
  - Frontend updated to use polling mechanism (2-second intervals, max 2 minutes)
  - CORS errors eliminated since all requests now complete quickly
  - In-memory task storage (production recommendation: use Redis with TTL)

### Technical Details
- `asyncio.create_task()` for non-blocking LLM calls
- Task states: `pending` → `processing` → `completed|error`
- Auto-cleanup of completed/failed tasks after status retrieval
- Backward-compatible: legacy endpoint still exists

---

## [March 10, 2026] - Admin Google Login & Data Migration

### Added
- **Admin Google Authentication**
  - New endpoint `POST /api/admin/google-login` for admin Google OAuth
  - Validates email against whitelist (`seremonta.cl@gmail.com`, `admin@seremonta.cl`)
  - Generates JWT token with `type: admin_google` claim
  - Updated `verify_admin_token()` to accept both traditional and Google tokens
  - Google login button added to Admin Login UI

- **Data Migration Script** (`/app/backend/migration.py`)
  - `export` command: Exports courses, chapters, lessons, questions, formulas to JSON
  - `import` command: Upserts data with duplicate handling
  - `stats` command: Shows current database statistics
  - Exported data stored in `/app/backend/migration_data/`

### Production Readiness
- All Mercado Pago credentials configured for PRODUCTION
- Webhook URL: `https://remy.seremonta.store/api/payments/webhook/mercadopago`
- Admin can now login via Google with authorized email

### Data Exported (Preview Environment)
- 2 courses, 2 chapters, 5 lessons, 9 questions, 10 formulas

---

## [March 10, 2026] - Authentication & User Management Release

### Added
- **Student Authentication System**
  - Email/Password registration with bcrypt hashing
  - Email/Password login with JWT session tokens
  - Google OAuth integration via Emergent Auth redirect flow
  - Session management with httpOnly secure cookies (7-day expiry)
  - Protected routes that redirect to /auth when not authenticated
  - AuthContext for frontend state management
  - Logout functionality with session cleanup

- **Admin User Management Panel (`/admin/users`)**
  - User list with pagination, search, and status filter
  - Statistics dashboard showing:
    - Total users, active subscriptions
    - Breakdown by subscription type (Mercado Pago vs Manual)
    - Breakdown by auth provider (Google vs Email)
    - Recent registrations (7 days)
  - Grant manual access to students (1-12 months duration)
  - Revoke manual access
  - Extend subscription duration
  - View user details and subscription history

- **Mercado Pago Integration (Backend)**
  - SDK integration with TEST credentials
  - Subscription plans endpoint
  - PreApproval creation endpoint
  - Webhook handler for payment notifications
  - Cancel subscription endpoint

- **New Backend Routes**
  - `/app/backend/routes/auth.py` - Student authentication
  - `/app/backend/routes/payments.py` - Payment processing
  - `/app/backend/routes/admin_users.py` - User management
  - `/app/backend/services/mercadopago_service.py` - MP service layer

- **New Frontend Pages**
  - `/app/frontend/src/pages/AuthPage.js` - Login/Register form
  - `/app/frontend/src/pages/AuthCallback.js` - Google OAuth callback handler
  - `/app/frontend/src/pages/admin/AdminUsers.js` - User management UI
  - `/app/frontend/src/contexts/AuthContext.js` - Auth state provider

### Changed
- `App.js` - Added protected route components for student and admin areas
- `Layout.js` - Added user menu with logout and subscription status
- `AdminLayout.js` - Added "Usuarios" nav item
- `Landing.js` - Connected CTA buttons to /auth route, added navbar with login buttons

### Fixed
- **SECURITY:** Fixed admin user endpoints that were accessible without authentication
  - Changed from `Depends(lambda: verify_admin_token)` to proper direct dependency
- Badge "Made with Emergent" removed from index.html

### Database Collections Added
- `users` - Student user accounts
- `user_sessions` - Active sessions
- `subscriptions` - Subscription records

## [March 9, 2026] - Landing Page & Quiz System

### Added
- Sales landing page at root URL (/)
- Advanced quiz system (Simulacros) with:
  - Custom quiz creation by course/chapter/lesson
  - Configurable question count and difficulty
  - Timer with countdown
  - Chilean grading scale (1-7)
- Student progress tracking per lesson
- "Chat with Remy" iterative content editing

### Changed
- Question bank reorganized by course/chapter
- Course viewer shows progress bars

---

## Test Credentials
- **Admin:** admin / #Alex060625
- **Test User:** test@example.com / test123
- **Mercado Pago TEST Keys:** Configured in backend/.env
