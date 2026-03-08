# Remy - Plataforma Educativa de Se Remonta

## Problem Statement
App educativa para "Se Remonta" con las siguientes características:
- **BackOffice Admin**: Panel de administración para crear y gestionar contenido educativo usando Gemini AI
- **Vista de Estudiantes**: Visualización de cursos, lecciones con LaTeX/KaTeX, simulacros de práctica y formulario de fórmulas

## User Personas
1. **Admin (Se Remonta)**: Crea contenido educativo, genera resúmenes y preguntas con AI
2. **Estudiantes**: Visualizan cursos, realizan simulacros, consultan fórmulas matemáticas

## Tech Stack
- **Frontend**: React, React Router, Tailwind CSS, Shadcn/UI, KaTeX (LaTeX), Desmos
- **Backend**: FastAPI, MongoDB (motor), JWT Auth
- **AI**: Google Gemini 2.5 Flash (para generación de contenido en BackOffice)

## Core Requirements

### Implemented Features (P0)
- [x] Admin authentication with JWT
- [x] Admin BackOffice with CRUD for Courses, Chapters, Lessons, Questions, Formulas
- [x] AI-assisted content generation (Gemini) for lessons and questions
- [x] Student course library (Biblioteca)
- [x] Course viewer with chapters and lessons hierarchy
- [x] Lesson viewer with Markdown + LaTeX/KaTeX rendering
- [x] Desmos graph embedding support
- [x] Formulas page with KaTeX rendering and search/filter
- [x] Simulacros (quizzes) with question bank selection
- [x] Student progress tracking page

### Database Collections
- `courses`: {id, title, description, category, level, modules_count, instructor, rating, cover_image_url, summary}
- `chapters`: {id, course_id, title, description, order}
- `lessons`: {id, chapter_id, title, content (Markdown), order, duration_minutes}
- `questions`: {id, course_id, topic, subtopic, difficulty, question_text, options, correct_answer, explanation, latex_content}
- `formulas`: {id, course_id, topic, name, latex, description, example}
- `quiz_attempts`: {id, user_id, course_id, topic, subtopic, questions, answers, score}
- `progress`: {id, user_id, course_id, completed_modules, total_modules, quizzes_completed, average_score, last_activity}

## API Endpoints

### Public (Student)
- `GET /api/courses` - List all courses
- `GET /api/courses/{course_id}` - Get course details
- `GET /api/courses/{course_id}/chapters` - Get course chapters
- `GET /api/chapters/{chapter_id}/lessons` - Get chapter lessons
- `GET /api/lessons/{lesson_id}` - Get lesson content
- `POST /api/formulas/search` - Search formulas
- `POST /api/quiz/start` - Start a quiz
- `POST /api/quiz/submit` - Submit quiz answers
- `GET /api/quiz/history/{user_id}` - Get quiz history
- `GET /api/progress/{user_id}` - Get user progress

### Admin (Protected)
- `POST /api/admin/login` - Admin login
- `GET /api/admin/verify` - Verify admin token
- CRUD: /api/admin/courses, chapters, lessons, questions, formulas
- `POST /api/admin/generate-summary` - Generate course summary with Gemini
- `POST /api/admin/generate-questions` - Generate questions with Gemini
- `POST /api/admin/generate-lesson-content` - Generate lesson content with Gemini

## Credentials
- **Admin**: username=admin, password=#Alex060625

## Current Data State
- 1 Course (Cálculo Diferencial)
- 2 Chapters (Límites, Derivadas)
- 1 Lesson with LaTeX content
- 10 Formulas with LaTeX
- 5 Questions (2 Derivadas, 1 Integrales, 1 Vectores, 1 Cinemática)

## Testing Status
- Backend: 100% (19/19 tests passed)
- Frontend: 100% all pages functional
- Test file: /app/backend/tests/test_remy_api.py

## Next Steps (Backlog)
- [ ] Add more lessons to chapters
- [ ] Populate question bank with more questions per topic
- [ ] Implement real user authentication for students
- [ ] Add PDF upload and content extraction
- [ ] Refine Gemini prompts for better LaTeX output
- [ ] Desmos production API key (currently using trial)
