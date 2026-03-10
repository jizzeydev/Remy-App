# Changelog - Remy Platform

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
