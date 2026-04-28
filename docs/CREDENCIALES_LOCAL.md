# Credenciales para ejecutar Remy en Local

Este documento contiene todas las credenciales necesarias para ejecutar Remy localmente desde Claude Code o cualquier entorno de desarrollo.

---

## ⚠️ IMPORTANTE
**NUNCA compartas este archivo públicamente ni lo subas a un repositorio público.**

---

## 1. Variables de Entorno del Backend (`/backend/.env`)

```env
# MongoDB
MONGO_URL="mongodb://localhost:27017"
DB_NAME="remy_database"

# CORS y URLs
CORS_ORIGINS=http://localhost:3000,http://localhost:8001
FRONTEND_URL=http://localhost:3000

# Admin Panel
ADMIN_SECRET_KEY=remy-admin-super-secret-key-2026
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=$2b$12$l8bLsw7ue3d4.pZq0.Ai/.XsUrSLg9QNPpO2q/l6.6mrv/JcaVasC
# Password: remy2026admin

# Cloudinary (almacenamiento de imágenes)
CLOUDINARY_CLOUD_NAME=de7loz0sr
CLOUDINARY_API_KEY=288493885439125
CLOUDINARY_API_SECRET=RK4lo2tyVuQYhWw_y-FyTbDowNs

# Mercado Pago (pagos)
MERCADOPAGO_ACCESS_TOKEN=APP_USR-1254600887824978-030919-9c123b34e86bbaab959830ad94a34d4b-820370254
MERCADOPAGO_PUBLIC_KEY=APP_USR-cdaa17ad-38aa-471a-afaf-e354a7b5007c
MERCADOPAGO_CLIENT_ID=1254600887824978
MERCADOPAGO_CLIENT_SECRET=QEca07i3nwgdu0QKWsBDrQi3hVvyWo9n
MERCADOPAGO_WEBHOOK_SECRET=8d34537a98f4b229b2ccf5b14e3cb3d886f23fc05297e594b9d7f17ec08d76ea

# Resend (emails transaccionales)
RESEND_API_KEY=re_hBr1HuHY_4RvoAf4xpssUc19ZV7uHtn2B
ADMIN_NOTIFICATION_EMAIL=seremonta.cl@gmail.com
SENDER_EMAIL=onboarding@resend.dev

# Google OAuth (Debes obtener las tuyas desde Google Cloud Console)
# GOOGLE_CLIENT_ID=tu_google_client_id
# GOOGLE_CLIENT_SECRET=tu_google_client_secret
```

---

## 2. Variables de Entorno del Frontend (`/frontend/.env`)

```env
# Backend URL (ajustar según tu entorno)
REACT_APP_BACKEND_URL=http://localhost:8001

# Para desarrollo local
WDS_SOCKET_PORT=3000
ENABLE_HEALTH_CHECK=false
```

---

## 3. Credenciales de Acceso

### Panel de Administración
- **URL**: `http://localhost:3000/admin/login`
- **Usuario**: `admin`
- **Contraseña**: `remy2026admin`

### Google OAuth (Admin)
- **Email autorizado**: `seremonta.cl@gmail.com`

---

## 4. Servicios Externos y cómo obtener credenciales

### MongoDB
- **Local**: Instalar MongoDB Community Server
- **Cloud**: Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/atlas)

### Google OAuth
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto
3. Habilita "Google+ API" y "Google Identity"
4. Ve a Credentials → Create OAuth 2.0 Client ID
5. Añade los URIs de redirección:
   - `http://localhost:3000/auth/callback`
   - `http://localhost:8001/api/auth/google/callback`

### Cloudinary (ya configurado)
- **URL**: [cloudinary.com](https://cloudinary.com)
- Cloud Name: `de7loz0sr`
- Las imágenes se almacenan permanentemente aquí

### Mercado Pago (ya configurado)
- **URL**: [mercadopago.com.cl/developers](https://www.mercadopago.com.cl/developers)
- Modo: Credenciales de PRUEBA (sandbox)

### Resend (ya configurado)
- **URL**: [resend.com](https://resend.com)
- Usado para enviar emails transaccionales

---

## 5. Comandos para ejecutar localmente

### Requisitos previos
- Node.js 18+
- Python 3.10+
- MongoDB (local o Atlas)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend
```bash
cd frontend
yarn install
yarn start
```

---

## 6. Estructura de URLs en Producción

Si despliegas en producción, actualiza las siguientes URLs:

- `FRONTEND_URL`: URL de tu dominio frontend (ej: `https://remy.tudominio.com`)
- `CORS_ORIGINS`: Incluir todas las URLs permitidas
- `REACT_APP_BACKEND_URL`: URL de tu API backend

---

## 7. Notas de Seguridad

1. **Genera nuevas claves** para producción:
   - `ADMIN_SECRET_KEY`: Usa un string aleatorio de 64+ caracteres
   - `ADMIN_PASSWORD_HASH`: Genera con `bcrypt.hashpw(password.encode(), bcrypt.gensalt())`
   - `MERCADOPAGO_*`: Usa credenciales de PRODUCCIÓN (no sandbox)

2. **Variables sensibles** que NUNCA deben estar en código:
   - API keys
   - Secrets
   - Contraseñas
   - Tokens de acceso

3. **Rota las credenciales** periódicamente, especialmente si sospechas que han sido expuestas.

---

Última actualización: Abril 2026
