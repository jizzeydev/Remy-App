# Deploy — Remy

Operativa de despliegue post-migración Emergent (abril 2026). Stack:

```
Cloudflare DNS (seremonta.store)
    │
    ├─→ remy.seremonta.store      → Vercel  (frontend React)
    └─→ api.remy.seremonta.store  → Render  (FastAPI backend)
                                       │
                                       ↓
                                  MongoDB Atlas (cluster remy-prod, M0)
```

Imágenes en Cloudinary (no en Atlas). Pagos en Mercado Pago Chile (PROD).
Auth con Google Identity Services (sin Emergent).

---

## Workflow de deploy

```
1. Cambios locales
2. git add … && git commit -m "…" && git push origin main
3. AUTOMÁTICO:
   - Render rebuilds backend si tocaste backend/ (~5–8 min)
   - Vercel rebuilds frontend si tocaste frontend/ (~2–3 min)
4. Live en remy.seremonta.store / api.remy.seremonta.store
```

Donde mirar status:

- Render: https://dashboard.render.com/ → `remy-backend` → tab **Events**
- Vercel: https://vercel.com/ → `remy-frontend` → tab **Deployments**

---

## Env vars

### Backend (Render → `remy-backend` → Environment)

Las **secrets** (`sync: false` en `render.yaml`) las pegás manualmente:

| Variable | Valor |
|---|---|
| `MONGO_URL` | `mongodb+srv://remy_app:<PASS>@remy-prod.hwmj0fn.mongodb.net/?appName=remy-prod` |
| `ADMIN_SECRET_KEY` | (string aleatorio) |
| `ADMIN_PASSWORD_HASH` | bcrypt hash de la pwd admin |
| `CLOUDINARY_API_KEY` / `_SECRET` | desde panel Cloudinary |
| `MERCADOPAGO_ACCESS_TOKEN` | `APP_USR-…` (PROD) |
| `MERCADOPAGO_CLIENT_SECRET` | desde panel MP |
| `MERCADOPAGO_WEBHOOK_SECRET` | desde panel MP |
| `RESEND_API_KEY` | desde panel Resend |

Las **no-secrets** ya están en `render.yaml` y se setean solas:
`PYTHON_VERSION`, `DB_NAME`, `CORS_ORIGINS`, `FRONTEND_URL`, `ADMIN_USERNAME`,
`GOOGLE_OAUTH_CLIENT_ID`, `CLOUDINARY_CLOUD_NAME`, `MERCADOPAGO_PUBLIC_KEY`,
`MERCADOPAGO_CLIENT_ID`, `ADMIN_NOTIFICATION_EMAIL`, `SENDER_EMAIL`.

Cambiar una env var en Render dispara redeploy automático (~30s, sin rebuild de pip).

### Frontend (Vercel → `remy-frontend` → Settings → Environment Variables)

| Variable | Valor | Environments |
|---|---|---|
| `REACT_APP_BACKEND_URL` | `https://api.remy.seremonta.store` | Production + Preview |
| `REACT_APP_GOOGLE_CLIENT_ID` | `143856720230-…apps.googleusercontent.com` | Production + Preview |

⚠️ Las `REACT_APP_*` se **inlinean en build-time**. Cambiar el valor NO afecta hasta que rebuildees:
- Push un commit nuevo (recomendado), o
- Tab **Deployments** → último deploy → menú `…` → **Redeploy** **con la checkbox "Use existing Build Cache" DESMARCADA**.

---

## Operaciones comunes

### Cambiar precio de un plan

Hay que tocar **2 lugares** (si tocás solo uno, el display y el cobro divergen):

1. **Backend** (lo que MP cobra realmente):
   `backend/services/mercadopago_service.py` → `PLANS["monthly"]["amount"]`
   Commit + push → Render redeploys.

2. **DB Atlas** (lo que el frontend muestra):
   `pricing_config.plans.monthly.base_price` (y `final_price` si tiene descuento).
   Snippet rápido (corré desde la raíz del repo):

   ```bash
   backend/venv/Scripts/python.exe -c "
   import asyncio
   from motor.motor_asyncio import AsyncIOMotorClient
   ATLAS = 'mongodb+srv://remy_app:<PASS>@remy-prod.hwmj0fn.mongodb.net/?appName=remy-prod'
   async def go():
       db = AsyncIOMotorClient(ATLAS)['remy_database']
       cur = await db.pricing_config.find_one({'config_id': 'main'}, {'_id': 0})
       cur['plans']['monthly']['base_price'] = 4990   # nuevo precio
       await db.pricing_config.update_one({'config_id': 'main'}, {'\$set': {'plans': cur['plans']}})
   asyncio.run(go())
   "
   ```

   O desde el admin UI: `https://remy.seremonta.store/admin/pricing`.

### Cambiar dominios o agregar subdominios

1. Cloudflare (zona `seremonta.store`) → DNS → Add record.
   - Para Vercel/Render: **CNAME** + **DNS only (gris)**. NO uses Proxied (naranja); rompe el SSL handshake.
2. Vercel: Settings → Domains → Add. Vercel emite cert automáticamente.
3. Render: Settings → Custom Domains → Add. Render emite cert automáticamente.

### Migrar / restaurar datos

`scripts/migrate_to_atlas.py` copia todas las collections del Mongo local a Atlas:

```bash
backend/venv/Scripts/python.exe scripts/migrate_to_atlas.py "mongodb+srv://USER:PASS@cluster.mongodb.net/?retryWrites=true&w=majority"
```

Lee `MONGO_URL` y `DB_NAME` desde `backend/.env` como source. Idempotente: dropea cada
collection en target antes de re-insertar.

### Sync de contenido (curso/lección/preguntas) sin perder imágenes

`scripts/sync_content_to_atlas.py` empuja solo las colecciones de **contenido**
(`courses`, `chapters`, `lessons`, `questions`, `library_universities`,
`formulas`, `pricing_config`, `app_settings`) a Atlas, preservando las
de **usuarios** (`users`, `subscriptions`, `quiz_attempts`,
`lesson_progress`, `payments`, etc.). Es el script que usás cada vez que
agregás o editás cursos en local.

⚠️ **Caveat clave**: hace `drop()` de la colección **entera** `lessons` en
Atlas y la repuebla con la copia local — no es un sync diferencial por curso.
Si subiste imágenes vía `/admin` en producción y después corrés
`sync_content_to_atlas.py --confirm` con un local que tiene `image_url=""`,
**borrás todas las imágenes**, también las de cursos que no tocaste.

Para evitarlo, el flujo correcto cada vez que vas a hacer un nuevo deploy
de contenido es:

```bash
# 1. Traer desde Atlas todos los image_url ya cargados → Mongo local
backend/venv/Scripts/python.exe scripts/pull_image_urls_from_atlas.py            # dry-run
backend/venv/Scripts/python.exe scripts/pull_image_urls_from_atlas.py --confirm  # aplica

# 2. Aplicar el seed nuevo (solo toca las lecciones de ese capítulo en local)
backend/venv/Scripts/python.exe scripts/run_seed.py "backend/seeds/<curso>/seed_capitulo_<N>.py"

# 3. Auditar estructura de las lecciones tocadas (opcional pero recomendado)
backend/venv/Scripts/python.exe scripts/audit_lesson_structure.py <curso>
# o auditar todos los cursos:
backend/venv/Scripts/python.exe scripts/audit_all_courses.py > test_reports/audit_all_courses.json

# 4. Dry-run del sync para ver qué se va a escribir
backend/venv/Scripts/python.exe scripts/sync_content_to_atlas.py

# 5. Push real a producción
backend/venv/Scripts/python.exe scripts/sync_content_to_atlas.py --confirm
```

El paso 1 lee Atlas, y por cada bloque `figura` con `image_url` no vacío
busca el bloque correspondiente en local (mismo `lesson.id` + mismo
`block.id`) y le copia la URL. Es idempotente y respeta cualquier URL que
local ya tenga distinta (no la pisa). Después del paso 5, Atlas queda con
exactamente las mismas imágenes que tenía + las modificaciones del nuevo seed.

**Recomendación de dónde generar imágenes**: directo en producción
(`/admin` en `remy.seremonta.store`). Las imágenes viven en Cloudinary,
solo el `image_url` se guarda en Atlas. Generar en local obliga a un
re-sync, que es un extra paso destructivo. Generar en prod escribe el URL
quirúrgicamente sin tocar otras colecciones.

### Auditar estructura pedagógica de los cursos

Estándar mínimo por lección:
**Contenido** (texto/definición/teorema/intuición) →
**Ejemplos** (`ejemplo_resuelto`) →
**Verificaciones** (`verificacion`: MCQ con pista + explicación) →
**Ejercicios de desarrollo** (`ejercicio` con `pistas_md` + `solucion_md`) →
**Figura o gráfico** (`figura` con `prompt_image_md` listo para ChatGPT
Images, o `grafico_desmos`).

```bash
# Un curso
backend/venv/Scripts/python.exe scripts/audit_lesson_structure.py <slug>

# Todos los cursos generales (JSON estructurado)
backend/venv/Scripts/python.exe scripts/audit_all_courses.py > test_reports/audit_all_courses.json
```

Ambos scripts importan los seeds y verifican bucket por bucket.
**No tocan Mongo** — son lectura pura del código fuente.

### Rotar password de Atlas

1. Atlas → Database Access → user `remy_app` → Edit Password → Autogenerate → Save.
2. Render → `remy-backend` → Environment → editar `MONGO_URL` con la pwd nueva → Save.
3. Render redeploya solo (~30s) y vuelve a conectar.

### Webhook de Mercado Pago

URL configurada en MP panel: `https://api.remy.seremonta.store/api/payments/webhook/mercadopago`.
Para testear localmente, MP no llega a `localhost`; usá ngrok o testeá con un cobro real
en producción y verificá el log de Render.

---

## Gotchas (errores que ya pisamos)

| Error | Causa | Fix |
|---|---|---|
| `SSL handshake failed: TLSV1_ALERT_INTERNAL_ERROR` al conectar a Atlas desde Render | Network Access en Atlas no incluye la IP de Render | Atlas → Network Access → agregar `0.0.0.0/0` (Render usa IPs dinámicas) |
| `pymongo.errors.ServerSelectionTimeoutError` con OpenSSL 3.x | pymongo < 4.6 no maneja bien OpenSSL 3.x del Linux de Render | `pymongo>=4.10`, `motor>=3.7` (ya pineado en `requirements.txt`) |
| `Card token service not found` al crear suscripción en TEST | MP Chile **no soporta `preapproval` en TEST** sin test buyer users | Usar credenciales PROD + tarjeta real (cobro mínimo $1.000) o crear test buyer |
| `Your payment cannot be processed because … not using a secure connection` (MP SDK) | MP PROD exige HTTPS para tokenizar | En local: `HTTPS=true` en `frontend/.env` (cert auto-firmado). En prod ya está. |
| `Invalid value for back_url, must be a valid URL` (MP) | `back_url` apuntaba a `http://localhost` | `FRONTEND_URL` en backend tiene que ser HTTPS público (`https://remy.seremonta.store`) |
| `origin_mismatch` en Google OAuth | El origen del browser no está en Authorized JavaScript origins | Cloud Console → OAuth Client → agregar el origen exacto (con/sin `https://`, con/sin port). Tarda 1-2 min en propagar. |
| Frontend bundle no toma el env var nuevo después de `Redeploy` | Vercel reusó el build cache | Redeploy → **DESMARCAR "Use existing Build Cache"**. O pushear un commit nuevo. |
| Vercel deployment URL devuelve `HTTP 401` | Deployment Protection activado para preview URLs | Settings → Deployment Protection → Vercel Authentication → **Disabled**. La alias estable (`remy-frontend.vercel.app`) sigue pública igual. |
| CRA build falla en Vercel con warnings de ESLint | `CI=true` (default Vercel) convierte warnings en errores | `frontend/vercel.json` ya fuerza `CI=false yarn build` |
| Pagos: precio mostrado en `/subscribe` no coincide con el cobrado por MP | El display viene de `pricing_config` (DB) y el charge viene de `PLANS` (código) | Sincronizar ambos lugares cuando cambiás precios (ver "Cambiar precio de un plan") |
| Texto blanco invisible en cards `bg-white` en dark mode | Cards forzaban `bg-white` pero los hijos heredaban `text-foreground` que en dark = blanco | Forzar `text-slate-900` (o equivalente) en cards con bg blanco fijo |

---

## URLs operativas

| Servicio | URL |
|---|---|
| App (público) | https://remy.seremonta.store |
| API (público) | https://api.remy.seremonta.store |
| Frontend Vercel (alias) | https://remy-frontend.vercel.app |
| Backend Render (alias) | https://remy-backend-8w94.onrender.com |
| Render dashboard | https://dashboard.render.com/ |
| Vercel dashboard | https://vercel.com/jesusalonsobravosilva-9980s-projects/remy-frontend |
| Atlas dashboard | https://cloud.mongodb.com/ |
| Cloudflare DNS | https://dash.cloudflare.com/ |
| Google OAuth (Cloud Console) | https://console.cloud.google.com/apis/credentials |
| Mercado Pago panel | https://www.mercadopago.cl/developers/panel/app |
| Cloudinary panel | https://cloudinary.com/console |
| Resend panel | https://resend.com/emails |

## Identidades / accesos

- **Admin emails permitidos** (Google OAuth): `seremonta.cl@gmail.com`, `admin@seremonta.cl`. Hardcoded en `backend/server.py` (`ALLOWED_ADMIN_EMAILS`) y `backend/routes/payments.py`.
- **Admin user/password fallback**: `admin` / (la pwd local — el hash bcrypt está en `ADMIN_PASSWORD_HASH`).

## Costos mensuales

- Render Starter: **$7/mes**
- Vercel Hobby: $0 (free tier alcanza)
- MongoDB Atlas M0: $0 (free tier — 512 MB; usamos ~5.5 MB)
- Cloudflare: $0
- Cloudinary: $0 (free tier)
- Resend: $0 hasta cierto volumen
- **Total: ~$7/mes**

Próximo upgrade probable: Atlas M10 cuando crezcan los datos (>512 MB) o necesites
backups automáticos. Render Standard si necesitás más RAM o concurrency.
