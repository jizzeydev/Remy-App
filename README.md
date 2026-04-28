# Remy — Plataforma de Estudio Universitario

![Status](https://img.shields.io/badge/Status-MVP-success?style=for-the-badge)

**Remy** es la webapp de estudio de **Se Remonta** para alumnos universitarios chilenos en ramos STEM duros (Cálculo I/II, Álgebra Lineal, Física, EDOs). Los alumnos repasan con lecciones, practican con simulacros y siguen su progreso. El contenido (preguntas, lecciones) se carga en el back-office vía CRUD manual o importación CSV.

## Funcionalidades

### Estudiante
- **Biblioteca de cursos**: capítulos y lecciones con LaTeX/KaTeX y gráficos Desmos.
- **Simulacros**: por curso o por universidad/evaluación, generados a partir del banco de preguntas.
- **"Tu Universidad"**: flujo Universidad → Curso → Evaluación → Quiz.
- **Progreso**: dashboard con KPIs, racha, lecciones completadas, promedio.
- **Formulario**: catálogo de fórmulas matemáticas buscable.
- **Suscripción**: trial 7 días, planes mensual y semestral vía Mercado Pago.

### Admin
- CRUD de Cursos, Capítulos, Lecciones, Universidades, Evaluaciones, Preguntas.
- **Importación CSV** de preguntas con plantilla descargable.
- Subida de imágenes a Cloudinary.
- Gestión de usuarios y accesos manuales (1–12 meses).
- Panel de métricas (ingresos, MRR, suscripciones).
- Precios dinámicos editables.

> El contenido educativo se genera offline (con tus propias herramientas) y se carga en Remy vía CRUD manual o CSV. Remy en sí no usa IA.

## Stack

### Backend (`/backend`)
- **FastAPI** + **MongoDB** (motor async)
- **JWT** + **bcrypt** para auth
- **Mercado Pago Chile** para suscripciones
- **Cloudinary** para imágenes
- **Resend** para emails transaccionales
- Punto de entrada: `server.py`

### Frontend (`/frontend`)
- **React 19** + **React Router v7**
- **Tailwind CSS** + **Shadcn/UI**
- **KaTeX** (LaTeX matemático), **Desmos** (gráficas interactivas)
- **Framer Motion**, **Sonner**, **Recharts**, **lucide-react**
- Build: **CRACO** sobre Create React App
- Package manager: **yarn**
- Fuentes: **Outfit** (headings), **Manrope** (body)

## Instalación local

### Requisitos
- Python 3.10+
- Node 18+
- MongoDB (local o Atlas)
- Yarn (`corepack enable` con Node 18+ lo habilita)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py         # poblar DB con cursos/fórmulas iniciales
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend
```bash
cd frontend
yarn install
yarn start
```

### Variables de entorno
Las plantillas y credenciales locales están en [`docs/CREDENCIALES_LOCAL.md`](docs/CREDENCIALES_LOCAL.md).

## Estructura

```
/
├── backend/
│   ├── server.py              # FastAPI app
│   ├── routes/                # auth, payments, admin_universities, etc.
│   ├── services/              # image_storage, etc.
│   ├── seed_data.py           # script de seeding
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── pages/             # Landing, Auth, Biblioteca, Simulacros, etc.
│   │   ├── pages/admin/       # AdminQuestions, UniversityDetail, CourseContentEditor, etc.
│   │   └── components/        # Layout, AdminLayout, ui/, course/
│   └── package.json
├── context/                   # docs de referencia del proyecto
├── memory/                    # PRD vivo + CHANGELOG histórico
└── docs/                      # credenciales locales
```

## Endpoints principales

### Estudiante (público / autenticado)
- `GET /api/courses`, `/api/courses/{id}`, `/api/materials/{course_id}`
- `POST /api/quiz/start`, `POST /api/quiz/submit`, `GET /api/quiz/history/{user_id}`
- `GET /api/progress/{user_id}`
- `POST /api/formulas/search`
- `POST /api/auth/google/session`, `GET /api/auth/me`, `POST /api/auth/logout`
- `GET /api/payments/plans`, `POST /api/payments/subscribe`, etc.

### Admin
- CRUD: `/api/admin/courses`, `/api/admin/chapters`, `/api/admin/lessons`, `/api/admin/questions`
- CSV: `POST /api/admin/questions/import-csv/{course_id}`, `GET /api/admin/questions/csv-template`
- Universidades: `/api/admin/universities/...` (CRUD + CSV import por evaluación)
- Imágenes: `POST /api/admin/upload-image`, `POST /api/admin/upload-course-image`
- Usuarios: `/api/admin/users/...`
- Métricas: `/api/admin/analytics/...`

## Despliegue

- **Producción**: `https://remy.seremonta.store`
- **Webhook MP**: `https://remy.seremonta.store/api/payments/webhook/mercadopago`
- HTTPS configurado.

## Versión

MVP — abril 2026.
