# Remy - Plataforma Educativa de Se Remonta

## Problem Statement
App educativa para "Se Remonta" con las siguientes características:
- **BackOffice Admin**: Panel de administración para crear y gestionar contenido educativo usando GPT-5.2
- **Vista de Estudiantes**: Visualización de cursos, lecciones con LaTeX/KaTeX, Desmos interactivo, y simulacros de práctica

## User Personas
1. **Admin (Se Remonta)**: Crea contenido educativo, genera resúmenes y preguntas con AI
2. **Estudiantes**: Visualizan cursos, realizan simulacros, consultan progreso

## Tech Stack
- **Frontend**: React, React Router, Tailwind CSS, Shadcn/UI, KaTeX (LaTeX), Desmos
- **Backend**: FastAPI, MongoDB (motor), JWT Auth
- **AI**: GPT-5.2 (contenido), GPT Image 1 (imágenes) via emergentintegrations

## Core Requirements

### Implemented Features (P0) - COMPLETADO
- [x] Admin authentication with JWT
- [x] Admin BackOffice with CRUD for Courses, Chapters, Lessons, Questions
- [x] AI-assisted content generation (GPT-5.2) for lessons
- [x] Chat-based lesson editing ("Chat with Remy") for iterative refinement
- [x] Image generation (GPT Image 1) and manual upload
- [x] Image placeholder system (`**[INSERTAR IMAGEN: ...]**`) for static diagrams
- [x] Student course library (Biblioteca)
- [x] Course viewer with chapters and lessons hierarchy
- [x] Lesson viewer with Markdown + LaTeX/KaTeX + Desmos rendering
- [x] Simulacros (quizzes) with question bank - FUNCTIONAL
- [x] Student progress tracking page

### Removed Features
- [x] Fórmulas - Eliminado (no aporta valor diferenciador)

### Database Collections
- `courses`: {id, title, description, category, level, modules_count, instructor, rating, cover_image_url, summary}
- `chapters`: {id, course_id, title, description, order}
- `lessons`: {id, chapter_id, title, content (Markdown), order, duration_minutes}
- `questions`: {id, course_id, topic, subtopic, difficulty, question_text, options, correct_answer, explanation, latex_content}
- `quiz_attempts`: {id, user_id, course_id, topic, subtopic, questions, answers, score}
- `progress`: {id, user_id, course_id, completed_modules, total_modules, quizzes_completed, average_score, last_activity}

## API Endpoints

### Public (Student)
- `GET /api/courses` - List all courses
- `GET /api/courses/{course_id}` - Get course details
- `GET /api/courses/{course_id}/chapters` - Get course chapters
- `GET /api/chapters/{chapter_id}/lessons` - Get chapter lessons
- `GET /api/lessons/{lesson_id}` - Get lesson content
- `POST /api/quiz/start` - Start a quiz
- `POST /api/quiz/submit` - Submit quiz answers
- `GET /api/quiz/history/{user_id}` - Get quiz history
- `GET /api/progress/{user_id}` - Get user progress

### Admin (Protected)
- `POST /api/admin/login` - Admin login
- `GET /api/admin/verify` - Verify admin token
- CRUD: /api/admin/courses, chapters, lessons, questions
- `POST /api/admin/generate-lesson-content` - Generate lesson with GPT-5.2
- `POST /api/admin/edit-lesson-content` - Edit lesson with AI chat
- `POST /api/admin/generate-image` - Generate image with GPT Image 1
- `POST /api/admin/upload-image` - Upload manual image

## Credentials
- **Admin**: username=admin, password=#Alex060625

## Current Data State
- 1 Course (Cálculo Diferencial)
- 2 Chapters (Límites, Derivadas)
- 1 Lesson with rich content (KaTeX, images, Desmos)
- 5 Questions (2 Derivadas, 1 Integrales, 1 Vectores, 1 Cinemática)

## Visualization Strategy
- **Desmos**: For interactive graphs (functions, sliders)
- **[INSERTAR IMAGEN: ...]**: For static diagrams (discontinuities, annotations, open/closed circles)
- Both can coexist in the same lesson

## Testing Status (March 9, 2026)
- Feature Fórmulas eliminada: ✅
- Simulacros funcionales: ✅ (con 5 preguntas)
- Placeholder de imagen: ✅ verificado
- Admin Dashboard actualizado: ✅
- Error Select.Item en AdminQuestions: ✅ CORREGIDO
- Editor de contenido de cursos: ✅ FUNCIONAL

## Next Steps (Backlog P1)
- [ ] Add more questions to question bank for better quiz variety
- [ ] Implement real user authentication for students
- [ ] Connect progress tracking to actual student activity
- [ ] Refactor server.py into multiple routers

## Future Tasks (P2)
- [ ] PDF content extraction
- [ ] Multi-language support
