# Stack Técnico

## Frontend (`/frontend`)
- **React 19** + **React Router v7**
- **Tailwind CSS** + **Shadcn/UI** (componentes en `src/components/ui/`)
- **KaTeX** para renderizado de LaTeX matemático
- **Desmos** embebido para gráficas interactivas
- **Framer Motion** para animaciones
- **Sonner** para toasts
- **Recharts** (vía Shadcn Chart) para gráficos del admin
- **lucide-react** para iconografía
- **Axios** para HTTP
- Build: **CRACO** (override de Create React App)
- Package manager: **yarn**
- Fuentes: **Outfit** (headings), **Manrope** (body)

## Backend (`/backend`)
- **FastAPI** (Python)
- **MongoDB** vía **motor** (async driver)
- **JWT** + **bcrypt** para auth
- Estructura modularizada en `routes/`, `services/`, `models/`
- Punto de entrada: `server.py`
- Seed: `seed_data.py`
- Migración: `migration.py` (export/import a `migration_data/`)

## Integraciones externas
| Servicio | Uso |
|---|---|
| **Mercado Pago Chile** | Suscripciones recurrentes (PreApproval) + webhooks |
| **Google OAuth** | Login estudiantes y admin |
| **Resend** | Emails transaccionales (bienvenida, alertas admin) |
| **Cloudinary** | CDN de imágenes de preguntas (cloud `de7loz0sr`, folder `remy/questions/`) |

## Despliegue
- **Producción**: `https://remy.seremonta.store`
- **Webhook MP**: `https://remy.seremonta.store/api/payments/webhook/mercadopago`
- HTTPS configurado.
- Dev preview anterior: `https://remy-exam-prep.preview.emergentagent.com`

## Diseño / Branding
- Paleta: **Cyan #00BCD4** (primary), **#E0F7FA** (secondary), **#FFC107** (accent gamificación).
- Layout: sidebar en desktop, bottom nav en mobile.
- Modo claro y oscuro (toggle en sidebars, persiste en localStorage).
- Detalle completo en [`design_guidelines.json`](../design_guidelines.json).

## Convenciones
- `data-testid` en todos los elementos interactivos para testing.
- Touch targets ≥ 44px en mobile.
- Botones: `rounded-full` (pill) o `rounded-xl` (soft rect).
- Nunca negro puro: usar Slate-900 (`#0F172A`).
