# Remy - Tutor Inteligente 24/7

![Remy](https://img.shields.io/badge/Remy-Tutor%20IA-00BCD4?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-MVP%20Complete-success?style=for-the-badge)

**Remy** es una plataforma educativa impulsada por IA para ayudar a estudiantes universitarios y preuniversitarios con matemáticas, cálculo, álgebra y física.

## 🎯 Funcionalidades Principales

### ✅ Implementadas

1. **🤖 Tutor IA 24/7**
   - Chat inteligente con GPT 5.2
   - Resuelve dudas al instante
   - Explicaciones paso a paso
   - Contexto por curso

2. **📝 Generador de Simulacros**
   - Crea exámenes personalizados con IA
   - Preguntas de opción múltiple
   - Explicaciones detalladas de respuestas
   - Feedback inmediato

3. **📚 Biblioteca de Cursos**
   - 6 cursos disponibles (Cálculo I, II, Álgebra Lineal, Física, etc.)
   - Organización por nivel y categoría
   - Tracking de progreso por curso

4. **🔢 Formulario Inteligente**
   - 10+ fórmulas matemáticas
   - Búsqueda por nombre o tema
   - Ejemplos prácticos
   - Filtrado por curso

5. **📊 Dashboard de Progreso**
   - Estadísticas de aprendizaje
   - Racha de estudio
   - Lecciones completadas
   - Promedio general

6. **📱 Diseño Responsive**
   - Desktop: Sidebar navigation
   - Mobile: Bottom navigation
   - Diseño moderno educativo
   - Paleta cyan/turquesa/azul

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: FastAPI
- **Base de datos**: MongoDB
- **IA**: OpenAI GPT 5.2 (via emergentintegrations)
- **Autenticación**: JWT (preparado para SSO con seremonta.store)

### Frontend
- **Framework**: React 19
- **Styling**: Tailwind CSS + Shadcn/UI
- **Routing**: React Router v7
- **Animaciones**: Framer Motion
- **Notificaciones**: Sonner
- **HTTP Client**: Axios
- **Fuentes**: Outfit (headings), Manrope (body)

## 🚀 Instalación y Uso

### Backend
```bash
cd /app/backend
pip install -r requirements.txt
python seed_data.py  # Poblar base de datos
```

### Frontend
```bash
cd /app/frontend
yarn install
```

### Variables de Entorno

**Backend (.env)**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
CORS_ORIGINS=*
EMERGENT_LLM_KEY=sk-emergent-39a5b126c034486Bc7
```

**Frontend (.env)**
```env
REACT_APP_BACKEND_URL=https://remy-exam-prep.preview.emergentagent.com
```

## 📡 API Endpoints

### Chat
- `POST /api/chat` - Chatear con Remy
- `GET /api/chat/history/{user_id}` - Historial de chat

### Simulacros
- `POST /api/quiz/generate` - Generar nuevo simulacro
- `GET /api/quizzes/{user_id}` - Obtener simulacros del usuario

### Cursos
- `GET /api/courses` - Listar todos los cursos
- `GET /api/courses/{course_id}` - Obtener curso específico
- `GET /api/materials/{course_id}` - Materiales de un curso

### Fórmulas
- `POST /api/formulas/search` - Buscar fórmulas

### Progreso
- `GET /api/progress/{user_id}` - Progreso del usuario

### Resúmenes
- `POST /api/summary/generate` - Generar resumen de material
- `GET /api/summaries/{user_id}` - Resúmenes del usuario

## 🎨 Paleta de Colores

- **Primary (Cyan)**: `#00BCD4` - Botones principales, elementos activos
- **Secondary**: `#E0F7FA` - Fondos de cards, highlights
- **Accent (Amarillo)**: `#FFC107` - Gamificación, logros
- **Background**: `#FFFFFF` - Fondo principal
- **Text Primary**: `#0F172A` - Texto principal
- **Text Secondary**: `#64748B` - Texto secundario

## 📊 Estructura del Proyecto

```
/app
├── backend/
│   ├── server.py           # FastAPI application
│   ├── seed_data.py        # Script para poblar DB
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Backend environment variables
│
├── frontend/
│   ├── src/
│   │   ├── App.js         # Main app component
│   │   ├── index.css      # Global styles with design tokens
│   │   ├── components/
│   │   │   ├── Layout.js  # Main layout with navigation
│   │   │   └── ui/        # Shadcn UI components
│   │   └── pages/
│   │       ├── Home.js           # Landing page
│   │       ├── Dashboard.js      # Main dashboard
│   │       ├── Chat.js           # Chat with Remy
│   │       ├── Simulacros.js     # Quiz generator
│   │       ├── Biblioteca.js     # Course library
│   │       ├── Formulas.js       # Formula finder
│   │       └── Progreso.js       # Progress tracker
│   │
│   ├── package.json       # Node dependencies
│   └── .env              # Frontend environment variables
│
└── README.md             # This file
```

## 🧪 Testing

El proyecto incluye testing completo con:
- Backend API testing
- Frontend UI testing
- Integration testing con GPT 5.2
- Responsive design validation

Test report: `/app/test_reports/iteration_1.json`

**Resultados:**
- Backend: ✅ 100% passed
- Frontend: ✅ 95% passed
- GPT 5.2 Integration: ✅ Working

## 🌐 Despliegue

La aplicación está desplegada en:
- **URL**: https://remy-exam-prep.preview.emergentagent.com
- **Backend API**: https://remy-exam-prep.preview.emergentagent.com/api

## 📈 Próximos Pasos

### Fase 2 (Pendiente)
- [ ] SSO con seremonta.store
- [ ] Procesamiento de PDFs para generar resúmenes automáticos
- [ ] Integración con videos de clases
- [ ] Sistema de gamificación completo
- [ ] Modo oscuro
- [ ] Notificaciones push
- [ ] Exportar simulacros a PDF

### Fase 3 (Futuro)
- [ ] App móvil nativa
- [ ] Modo offline
- [ ] Compartir progreso con instructores
- [ ] Foros de discusión
- [ ] Sesiones de estudio en grupo

## 👥 Créditos

- **Desarrollado para**: Se Remonta (seremonta.store)
- **IA Integration**: OpenAI GPT 5.2
- **Built by**: Emergent AI

## 📝 Notas de Desarrollo

### Usuario Demo
- **User ID**: `demo-user-001`
- Usado para testing y desarrollo inicial

### Base de Datos
- 6 cursos pre-cargados
- 10 fórmulas matemáticas
- Esquema flexible para expansión

### Integración GPT 5.2
- Usa `emergentintegrations` library
- Key universal de Emergent
- Contexto educativo optimizado

---

**Versión**: 1.0.0 (MVP)
**Última actualización**: Enero 2026
