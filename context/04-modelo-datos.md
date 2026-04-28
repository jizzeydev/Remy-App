# Modelo de Datos (alto nivel)

> Esquema flexible en MongoDB. Esto es el mapa mental, no el schema literal — el código es la fuente de verdad.

## Jerarquía de contenido

```
Universidad (nombre, sigla)
└── Curso (e.g. "Cálculo I PUC")
    └── Evaluación (e.g. "Control 1 - 2024")
        └── Pregunta
            ├── enunciado (LaTeX)
            ├── opciones (A, B, C, D)
            ├── respuesta correcta
            ├── solución paso a paso (LaTeX)
            ├── dificultad (fácil/medio/difícil)
            ├── tema
            ├── tags[]
            └── imagen (Cloudinary URL)
```

Paralelo a esto existe el contenido **propio de Remy** (no anclado a una universidad):

```
Curso Remy (e.g. "Cálculo I")
└── Capítulo
    └── Lección
        ├── contenido (LaTeX/KaTeX)
        ├── gráficos Desmos
        └── imágenes
```

## Entidades transversales

- **Usuario**: `id`, `email`, `name`, `google_id`, `created_at`, `trial_started_at`, `trial_ends_at`, `subscription_status`, `subscription_type` (mensual/semestral/manual), `subscription_ends_at`.
- **Suscripción**: registro de PreApproval de Mercado Pago, estados (active/paused/cancelled), historial.
- **Sesión**: token JWT, `expires_at` (30 días), almacenado en cookie httpOnly + localStorage (`remy_session_token`).
- **Quiz / Simulacro**: snapshot de preguntas seleccionadas + respuestas del usuario + score + timestamp.
- **Progreso**: por usuario × curso (lecciones completadas, simulacros, promedio, racha).
- **Fórmula**: catálogo independiente buscable.
- **Precios**: documento de configuración editable desde `/admin/pricing`.

## Endpoints clave (referencia rápida)

### Auth
- `POST /api/auth/google/session`
- `GET /api/auth/me`
- `POST /api/auth/logout`

### Pagos
- `GET /api/payments/plans`
- `POST /api/payments/subscribe`
- `GET /api/payments/subscription`
- `POST /api/payments/cancel`
- `POST /api/payments/webhook/mercadopago`

### Universidades (admin)
- `GET|POST|PUT|DELETE /api/admin/universities`
- `.../courses`, `.../evaluations`, `.../questions`
- `POST .../questions/import-csv` y `GET .../questions/template-csv`

### Usuarios (admin)
- `GET /api/admin/users` y `/stats`
- `POST /api/admin/users/grant-access`
- `POST /api/admin/users/{id}/revoke-access`
- `POST /api/admin/users/{id}/extend-access`

> Lista canónica: ver `memory/PRD.md` y código en `backend/routes/`.
