from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
import base64
import aiofiles
from datetime import datetime, timezone, timedelta
from emergentintegrations.llm.chat import LlmChat, UserMessage
from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration
import PyPDF2
import io
import json
from jose import JWTError, jwt
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
UPLOADS_DIR = ROOT_DIR / 'uploads'
UPLOADS_DIR.mkdir(exist_ok=True)

load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")
admin_router = APIRouter(prefix="/api/admin")

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

# Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Course(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str
    level: str
    modules_count: int
    instructor: str
    rating: float = 4.8
    cover_image_url: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Chapter(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    course_id: str
    title: str
    description: str
    order: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Lesson(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chapter_id: str
    title: str
    content: str
    order: int
    duration_minutes: int = 30
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Material(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    course_id: str
    title: str
    type: str
    content: Optional[str] = None
    file_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Question(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    course_id: str
    topic: str
    subtopic: Optional[str] = None
    difficulty: str
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: str
    latex_content: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuizAttempt(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    course_id: str
    topic: str
    subtopic: Optional[str] = None
    questions: List[Dict[str, Any]]
    answers: Dict[int, str]
    score: Optional[float] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Progress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    course_id: str
    completed_modules: int = 0
    total_modules: int
    quizzes_completed: int = 0
    average_score: float = 0.0
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Formula(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    course_id: str
    topic: str
    name: str
    latex: str
    description: str
    example: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class QuizStartRequest(BaseModel):
    user_id: str
    course_id: str
    topic: str
    subtopic: Optional[str] = None
    difficulty: Optional[str] = None
    num_questions: int = 10

class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: Dict[int, str]

class GenerateSummaryRequest(BaseModel):
    pdf_content: str
    course_title: str

class GenerateQuestionsRequest(BaseModel):
    pdf_content: str
    course_id: str
    topic: str
    num_questions: int = 10

class GenerateLessonContentRequest(BaseModel):
    pdf_content: str
    lesson_title: str
    chapter_title: str

class FormulaSearchRequest(BaseModel):
    query: str
    course_id: Optional[str] = None

# Helper functions
def get_gpt_chat(system_message: str):
    """Get GPT 5.2 chat instance for high-quality educational content generation"""
    api_key = os.environ.get('EMERGENT_LLM_KEY')
    session_id = str(uuid.uuid4())
    chat = LlmChat(
        api_key=api_key,
        session_id=session_id,
        system_message=system_message
    ).with_model("openai", "gpt-5.2")
    return chat

def get_gemini_chat(system_message: str):
    """Legacy Gemini chat - kept for backwards compatibility"""
    api_key = os.environ.get('GEMINI_API_KEY')
    session_id = str(uuid.uuid4())
    chat = LlmChat(
        api_key=api_key,
        session_id=session_id,
        system_message=system_message
    ).with_model("gemini", "gemini-2.5-flash")
    return chat

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username != os.environ.get('ADMIN_USERNAME'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

def extract_text_from_pdf(pdf_file: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Public endpoints
@api_router.get("/")
async def root():
    return {"message": "Bienvenido a Remy - Tu plataforma de estudio inteligente"}

# Serve uploaded images
from fastapi.responses import FileResponse

@api_router.get("/uploads/{filename}")
async def get_uploaded_image(filename: str):
    file_path = UPLOADS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return FileResponse(file_path)

@api_router.get("/courses", response_model=List[Course])
async def get_courses():
    courses = await db.courses.find({}, {"_id": 0}).to_list(100)
    for course in courses:
        if isinstance(course.get('created_at'), str):
            course['created_at'] = datetime.fromisoformat(course['created_at'])
    return courses

@api_router.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: str):
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    if isinstance(course.get('created_at'), str):
        course['created_at'] = datetime.fromisoformat(course['created_at'])
    return course

@api_router.get("/materials/{course_id}", response_model=List[Material])
async def get_materials(course_id: str):
    materials = await db.materials.find({"course_id": course_id}, {"_id": 0}).to_list(100)
    for material in materials:
        if isinstance(material.get('created_at'), str):
            material['created_at'] = datetime.fromisoformat(material['created_at'])
    return materials

@api_router.post("/formulas/search")
async def search_formulas(request: FormulaSearchRequest):
    query_filter = {}
    if request.course_id:
        query_filter["course_id"] = request.course_id
    
    formulas = await db.formulas.find(query_filter, {"_id": 0}).to_list(100)
    
    if request.query:
        query_lower = request.query.lower()
        formulas = [
            f for f in formulas 
            if query_lower in f.get('name', '').lower() or 
               query_lower in f.get('topic', '').lower() or
               query_lower in f.get('description', '').lower()
        ]
    
    return formulas

@api_router.post("/quiz/start")
async def start_quiz(request: QuizStartRequest):
    query = {"course_id": request.course_id, "topic": request.topic}
    if request.subtopic:
        query["subtopic"] = request.subtopic
    if request.difficulty:
        query["difficulty"] = request.difficulty
    
    all_questions = await db.questions.find(query, {"_id": 0}).to_list(1000)
    
    if len(all_questions) < request.num_questions:
        raise HTTPException(
            status_code=400, 
            detail=f"Solo hay {len(all_questions)} preguntas disponibles para este tema"
        )
    
    import random
    selected_questions = random.sample(all_questions, request.num_questions)
    
    quiz_attempt = QuizAttempt(
        user_id=request.user_id,
        course_id=request.course_id,
        topic=request.topic,
        subtopic=request.subtopic,
        questions=selected_questions,
        answers={}
    )
    
    doc = quiz_attempt.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.quiz_attempts.insert_one(doc)
    
    questions_without_answers = [
        {k: v for k, v in q.items() if k != 'correct_answer' and k != 'explanation'}
        for q in selected_questions
    ]
    
    return {
        "quiz_id": quiz_attempt.id,
        "questions": questions_without_answers
    }

@api_router.post("/quiz/submit")
async def submit_quiz(request: QuizSubmitRequest):
    quiz = await db.quiz_attempts.find_one({"id": request.quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")
    
    correct_count = 0
    results = []
    
    for idx, question in enumerate(quiz['questions']):
        user_answer = request.answers.get(str(idx))
        is_correct = user_answer == question['correct_answer']
        if is_correct:
            correct_count += 1
        
        results.append({
            "question_index": idx,
            "question_text": question['question_text'],
            "user_answer": user_answer,
            "correct_answer": question['correct_answer'],
            "is_correct": is_correct,
            "explanation": question['explanation']
        })
    
    score = (correct_count / len(quiz['questions'])) * 100
    
    await db.quiz_attempts.update_one(
        {"id": request.quiz_id},
        {"$set": {"answers": request.answers, "score": score}}
    )
    
    progress = await db.progress.find_one(
        {"user_id": quiz['user_id'], "course_id": quiz['course_id']},
        {"_id": 0}
    )
    
    if progress:
        new_quizzes_count = progress['quizzes_completed'] + 1
        new_avg_score = ((progress['average_score'] * progress['quizzes_completed']) + score) / new_quizzes_count
        
        await db.progress.update_one(
            {"id": progress['id']},
            {"$set": {
                "quizzes_completed": new_quizzes_count,
                "average_score": new_avg_score,
                "last_activity": datetime.now(timezone.utc).isoformat()
            }}
        )
    
    return {
        "score": score,
        "correct_count": correct_count,
        "total_questions": len(quiz['questions']),
        "results": results
    }

@api_router.get("/progress/{user_id}")
async def get_user_progress(user_id: str):
    progress_list = await db.progress.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    for progress in progress_list:
        if isinstance(progress.get('last_activity'), str):
            progress['last_activity'] = datetime.fromisoformat(progress['last_activity'])
    return progress_list

@api_router.get("/quiz/history/{user_id}")
async def get_quiz_history(user_id: str, limit: int = 20):
    quizzes = await db.quiz_attempts.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("created_at", -1).limit(limit).to_list(limit)
    
    for quiz in quizzes:
        if isinstance(quiz.get('created_at'), str):
            quiz['created_at'] = datetime.fromisoformat(quiz['created_at'])
    
    return quizzes

# Admin endpoints
@admin_router.post("/login", response_model=Token)
async def admin_login(request: LoginRequest):
    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH')
    
    if request.username != admin_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not pwd_context.verify(request.password, admin_password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@admin_router.get("/verify")
async def verify_admin(username: str = Depends(verify_admin_token)):
    return {"username": username, "verified": True}

@admin_router.post("/courses", response_model=Course)
async def create_course(course: Course, _: str = Depends(verify_admin_token)):
    doc = course.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.courses.insert_one(doc)
    return course

@admin_router.put("/courses/{course_id}", response_model=Course)
async def update_course(course_id: str, course: Course, _: str = Depends(verify_admin_token)):
    doc = course.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    result = await db.courses.update_one({"id": course_id}, {"$set": doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course

@admin_router.delete("/courses/{course_id}")
async def delete_course(course_id: str, _: str = Depends(verify_admin_token)):
    result = await db.courses.delete_one({"id": course_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"message": "Curso eliminado exitosamente"}

@admin_router.post("/formulas", response_model=Formula)
async def create_formula(formula: Formula, _: str = Depends(verify_admin_token)):
    doc = formula.model_dump()
    await db.formulas.insert_one(doc)
    return formula

@admin_router.put("/formulas/{formula_id}", response_model=Formula)
async def update_formula(formula_id: str, formula: Formula, _: str = Depends(verify_admin_token)):
    result = await db.formulas.update_one({"id": formula_id}, {"$set": formula.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Fórmula no encontrada")
    return formula

@admin_router.delete("/formulas/{formula_id}")
async def delete_formula(formula_id: str, _: str = Depends(verify_admin_token)):
    result = await db.formulas.delete_one({"id": formula_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Fórmula no encontrada")
    return {"message": "Fórmula eliminada exitosamente"}

@admin_router.post("/questions", response_model=Question)
async def create_question(question: Question, _: str = Depends(verify_admin_token)):
    doc = question.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.questions.insert_one(doc)
    return question

@admin_router.get("/questions")
async def get_all_questions(
    course_id: Optional[str] = None,
    topic: Optional[str] = None,
    _: str = Depends(verify_admin_token)
):
    query = {}
    if course_id:
        query["course_id"] = course_id
    if topic:
        query["topic"] = topic
    
    questions = await db.questions.find(query, {"_id": 0}).to_list(1000)
    return questions

@admin_router.put("/questions/{question_id}", response_model=Question)
async def update_question(question_id: str, question: Question, _: str = Depends(verify_admin_token)):
    doc = question.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    result = await db.questions.update_one({"id": question_id}, {"$set": doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return question

@admin_router.delete("/questions/{question_id}")
async def delete_question(question_id: str, _: str = Depends(verify_admin_token)):
    result = await db.questions.delete_one({"id": question_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return {"message": "Pregunta eliminada exitosamente"}

@admin_router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    pdf_content = await file.read()
    text = extract_text_from_pdf(pdf_content)
    
    return {
        "filename": file.filename,
        "text_length": len(text),
        "text_preview": text[:500] + "..."
    }

@admin_router.post("/generate-summary")
async def generate_summary(request: GenerateSummaryRequest, _: str = Depends(verify_admin_token)):
    try:
        system_message = f"""Eres un profesor experto de Se Remonta creando resúmenes educativos para el curso: {request.course_title}.

Crea un resumen ESTRUCTURADO y COMPLETO que incluya:

1. **Visión General** - Contexto y relevancia del tema
2. **Conceptos Fundamentales** - Ideas principales explicadas claramente
3. **Fórmulas Clave** - En formato LaTeX ($$formula$$)
4. **Relaciones Importantes** - Cómo se conectan los conceptos
5. **Aplicaciones Prácticas** - Ejemplos del mundo real
6. **Puntos para Recordar** - Lista de lo más importante

FORMATO:
- Usa Markdown con ## para secciones
- Fórmulas en bloque: $$formula$$
- Fórmulas en línea: $formula$
- Listas con viñetas para puntos clave
"""
        
        chat = get_gpt_chat(system_message)
        user_message = UserMessage(text=f"Resume el siguiente material educativo de forma completa y estructurada:\n\n{request.pdf_content[:12000]}")
        response = await chat.send_message(user_message)
        
        return {"summary": response}
    except Exception as e:
        logging.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/generate-questions")
async def generate_questions(request: GenerateQuestionsRequest, _: str = Depends(verify_admin_token)):
    try:
        system_message = """Eres un experto en evaluación educativa de Se Remonta, especializado en crear preguntas de examen de opción múltiple para estudiantes universitarios.

REGLAS ESTRICTAS:

1. Genera preguntas que evalúen COMPRENSIÓN, no solo memorización
2. Cada pregunta debe tener exactamente 4 opciones (A, B, C, D)
3. Los distractores (opciones incorrectas) deben ser plausibles
4. La explicación debe ser educativa y detallada

FORMATO DE SALIDA - JSON ESTRICTO:
```json
{
  "questions": [
    {
      "question_text": "Enunciado claro de la pregunta. Si incluye fórmulas usar $formula$ o $$formula$$",
      "options": [
        "A) Primera opción",
        "B) Segunda opción", 
        "C) Tercera opción",
        "D) Cuarta opción"
      ],
      "correct_answer": "A",
      "explanation": "Explicación detallada de por qué A es correcta y por qué las otras son incorrectas",
      "difficulty": "fácil|medio|difícil",
      "latex_content": "Fórmula principal si aplica, ej: \\\\frac{d}{dx}[x^n] = nx^{n-1}"
    }
  ]
}
```

IMPORTANTE: Responde SOLO con el JSON, sin texto adicional antes o después."""

        user_prompt = f"""Genera exactamente {request.num_questions} preguntas de opción múltiple sobre el tema "{request.topic}".

Material de referencia:
{request.pdf_content[:12000]}

Distribución de dificultad sugerida:
- 30% fácil (conceptos básicos)
- 50% medio (aplicación de conceptos)
- 20% difícil (análisis y síntesis)

Responde SOLO con el JSON válido."""
        
        chat = get_gpt_chat(system_message)
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        # Clean and parse JSON response
        try:
            # Remove markdown code blocks if present
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            clean_response = clean_response.strip()
            
            questions_data = json.loads(clean_response)
            questions = questions_data.get("questions", [])
        except json.JSONDecodeError as je:
            logging.error(f"JSON parse error: {je}, response: {response[:500]}")
            questions = []
        
        return {"questions": questions}
    except Exception as e:
        logging.error(f"Error generating questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Chapters endpoints
@admin_router.get("/courses/{course_id}/chapters")
async def get_course_chapters(course_id: str, _: str = Depends(verify_admin_token)):
    chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0}).sort("order", 1).to_list(100)
    for chapter in chapters:
        if isinstance(chapter.get('created_at'), str):
            chapter['created_at'] = datetime.fromisoformat(chapter['created_at'])
    return chapters

@admin_router.post("/chapters", response_model=Chapter)
async def create_chapter(chapter: Chapter, _: str = Depends(verify_admin_token)):
    doc = chapter.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.chapters.insert_one(doc)
    return chapter

@admin_router.put("/chapters/{chapter_id}", response_model=Chapter)
async def update_chapter(chapter_id: str, chapter: Chapter, _: str = Depends(verify_admin_token)):
    doc = chapter.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    result = await db.chapters.update_one({"id": chapter_id}, {"$set": doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Capítulo no encontrado")
    return chapter

@admin_router.delete("/chapters/{chapter_id}")
async def delete_chapter(chapter_id: str, _: str = Depends(verify_admin_token)):
    await db.lessons.delete_many({"chapter_id": chapter_id})
    result = await db.chapters.delete_one({"id": chapter_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Capítulo no encontrado")
    return {"message": "Capítulo y sus lecciones eliminadas exitosamente"}

# Lessons endpoints
@admin_router.get("/chapters/{chapter_id}/lessons")
async def get_chapter_lessons(chapter_id: str, _: str = Depends(verify_admin_token)):
    lessons = await db.lessons.find({"chapter_id": chapter_id}, {"_id": 0}).sort("order", 1).to_list(100)
    for lesson in lessons:
        if isinstance(lesson.get('created_at'), str):
            lesson['created_at'] = datetime.fromisoformat(lesson['created_at'])
    return lessons

@admin_router.post("/lessons", response_model=Lesson)
async def create_lesson(lesson: Lesson, _: str = Depends(verify_admin_token)):
    doc = lesson.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.lessons.insert_one(doc)
    return lesson

@admin_router.put("/lessons/{lesson_id}", response_model=Lesson)
async def update_lesson(lesson_id: str, lesson: Lesson, _: str = Depends(verify_admin_token)):
    doc = lesson.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    result = await db.lessons.update_one({"id": lesson_id}, {"$set": doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    return lesson

@admin_router.delete("/lessons/{lesson_id}")
async def delete_lesson(lesson_id: str, _: str = Depends(verify_admin_token)):
    result = await db.lessons.delete_one({"id": lesson_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    return {"message": "Lección eliminada exitosamente"}

@admin_router.post("/generate-lesson-content")
async def generate_lesson_content(request: GenerateLessonContentRequest, _: str = Depends(verify_admin_token)):
    try:
        system_message = """Eres REMY, el profesor virtual de Se Remonta. Tu misión es que cada estudiante ENTIENDA, APRENDA y APRUEBE.

🎯 TU FILOSOFÍA DE ENSEÑANZA:
- Explica como si fueras un amigo que domina el tema
- Usa ejemplos de la VIDA COTIDIANA (Netflix, deportes, cocina, videojuegos, redes sociales)
- Haz que los conceptos abstractos sean TANGIBLES y VISUALES
- Si algo puede verse, MUÉSTRALO con un gráfico interactivo
- Celebra los pequeños logros del estudiante
- Anticipa las dudas comunes y respóndelas proactivamente

📝 FORMATO MARKDOWN:
- Títulos: # para H1, ## para H2, ### para H3
- Listas: * o - para viñetas
- Negrita: **concepto importante**
- Cursiva: *énfasis suave*

📐 FÓRMULAS LATEX (KaTeX):
- En línea: $formula$ 
- En bloque: $$formula$$
- Ejemplos: $f(x) = x^2$, $$\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$$

📊 VISUALIZACIONES - CUÁNDO USAR CADA TIPO:

**DESMOS (Interactivo)** - Usa SOLO cuando el estudiante DEBE explorar:
✅ USAR Desmos cuando:
- El estudiante necesita mover un slider para entender (ej: ver cómo cambia la pendiente)
- Comparar múltiples funciones superpuestas
- Explorar qué pasa cuando un valor cambia (límites, parámetros)
- Ver animaciones de conceptos (secante → tangente)

❌ NO usar Desmos cuando:
- Necesitas mostrar círculos ABIERTOS (○) o CERRADOS (●) en puntos específicos
- Es un diagrama de discontinuidad con saltos visuales
- Necesitas anotaciones, flechas o líneas punteadas
- Es una ilustración conceptual, no exploratoria

Formato Desmos (UN SOLO tag con punto y coma):
[DESMOS:y = x^2; a=1; h=0.5; m=((a+h)^2-a^2)/h; y=m*(x-a)+a^2]

**IMAGEN_GPAI (Para ilustraciones estáticas)** - Usa para gráficas con detalles precisos:
⚠️ OBLIGATORIO usar IMAGEN_GPAI cuando:
- Hay discontinuidades de salto (necesitas mostrar círculos abiertos/cerrados)
- Hay huecos en la gráfica (puntos donde la función no existe)
- Necesitas mostrar límites laterales diferentes
- Requieres anotaciones con flechas o líneas punteadas

Formato:
[IMAGEN_GPAI:
**Título descriptivo**
- Eje X: de ___ a ___
- Eje Y: de ___ a ___
- Elemento 1: descripción con coordenadas
- Elemento 2: descripción (usar ○ para abierto, ● para cerrado)
- Líneas punteadas: desde ___ hasta ___
- Visual clave: qué debe notar el estudiante
]

EJEMPLO OBLIGATORIO para discontinuidad de salto:
[IMAGEN_GPAI:
**Discontinuidad de Salto en x=1**
- Eje X: de 0 a 3
- Eje Y: de 0 a 5
- Rama izquierda (x<1): línea desde (0,1) hasta punto (1,2) con círculo ABIERTO ○
- Rama derecha (x≥1): línea desde punto (1,4) con círculo CERRADO ● hasta (3,2)
- Visual clave: Salto vertical de 2 unidades entre y=2 y y=4 en x=1
- El límite por izquierda (2) ≠ límite por derecha (4)
]

📋 TABLAS - Para comparaciones y resúmenes:
| Concepto | Fórmula | Ejemplo |
|----------|---------|---------|
| dato     | dato    | dato    |

🏗️ ESTRUCTURA OBLIGATORIA DE LA LECCIÓN:

## 🎯 ¿Qué vas a aprender?
(Objetivos claros y motivadores)

## 🤔 ¿Por qué es importante?
(Conexión con la vida real, por qué debería importarle al estudiante)

## 📚 Desarrollo del Tema
(Explicación paso a paso, de lo simple a lo complejo)

## 🔢 Fórmulas Clave
(Con explicación de cada símbolo y cuándo usarlas)

## 👀 Visualízalo
(Usa Desmos para exploración interactiva O [IMAGEN_GPAI:...] para ilustraciones estáticas detalladas)
- Si el concepto requiere EXPLORAR con sliders → Desmos
- Si el concepto requiere ver puntos específicos, discontinuidades, anotaciones → IMAGEN_GPAI

## ✍️ Ejemplos Resueltos
(Mínimo 3 ejemplos, del más fácil al más difícil, paso a paso)

## 🎮 Ahora Practícalo Tú
(Ejercicios con pistas, no solo enunciados)

## 📌 Resumen Express
(Los puntos clave en bullets, como "cheat sheet")

## 💡 Tips para el Examen
(Errores comunes, trucos, qué suele preguntarse)

IMPORTANTE: El estudiante debe sentir que PUEDE aprender esto. Sé motivador pero honesto."""

        user_prompt = f"""Crea una lección COMPLETA, INTERACTIVA y MOTIVADORA para:

📖 Título: "{request.lesson_title}"
📂 Capítulo: "{request.chapter_title}"

Material de referencia:
{request.pdf_content[:10000]}

REQUISITOS OBLIGATORIOS:
✅ En la sección "Visualízalo": decide inteligentemente entre Desmos (interactivo) o IMAGEN_GPAI (descripción para generar imagen)
✅ Mínimo 3 ejemplos resueltos paso a paso
✅ Ejemplos de la vida cotidiana
✅ Una tabla comparativa o de resumen
✅ Tips específicos para aprobar el examen
✅ Tono amigable pero profesional

RECUERDA:
- Desmos = cuando el estudiante debe MOVER/EXPLORAR algo
- IMAGEN_GPAI = cuando necesitas mostrar algo estático con detalles precisos (discontinuidades, puntos específicos, anotaciones)

¡Haz que el estudiante disfrute aprendiendo!"""
        
        chat = get_gpt_chat(system_message)
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        return {"content": response}
    except Exception as e:
        logging.error(f"Error generating lesson content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# New: Edit lesson content with AI chat
class EditLessonContentRequest(BaseModel):
    current_content: str
    user_instruction: str
    lesson_title: str = ""
    chapter_title: str = ""

@admin_router.post("/edit-lesson-content")
async def edit_lesson_content(request: EditLessonContentRequest, _: str = Depends(verify_admin_token)):
    try:
        system_message = """Eres REMY, el asistente educativo de Se Remonta. Tu trabajo es MEJORAR el contenido de lecciones para que los estudiantes ENTIENDAN y APRUEBEN.

🎯 TU MISIÓN AL EDITAR:
- Cada cambio debe hacer el contenido MÁS CLARO y MÁS ÚTIL para el estudiante
- Si el usuario pide agregar algo, hazlo COMPLETO y DIDÁCTICO (no una línea genérica)
- Si pide quitar algo, elimínalo limpiamente sin dejar huecos
- Si pide cambiar algo, mejóralo significativamente

📐 REGLAS DE FORMATO (MANTENER SIEMPRE):

1. FÓRMULAS LATEX:
   - En línea: $formula$ (ej: $f(x) = x^2$)
   - En bloque: $$formula$$ (ej: $$\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$$)

2. DESMOS - GRÁFICOS INTERACTIVOS (MUY IMPORTANTE):
   - SIEMPRE en UN SOLO tag con punto y coma entre ecuaciones
   - SIEMPRE incluir sliders cuando el concepto lo permita
   - El estudiante debe poder EXPLORAR moviendo valores
   
   EJEMPLOS CORRECTOS:
   [DESMOS:y = x^2]
   [DESMOS:a=2; y = a*x^2]  <- Con slider para explorar
   [DESMOS:y=x^2; a=1; h=0.5; y=((a+h)^2-a^2)/h*(x-a)+a^2]  <- Secante interactiva
   [DESMOS:f(x)=x^3-3x; f'(x)=3x^2-3]  <- Función y derivada juntas
   
   NUNCA hagas esto:
   [DESMOS:y=x^2]
   [DESMOS:a=1]  <- MAL: separados no funcionan juntos

3. TABLAS MARKDOWN:
   | Columna 1 | Columna 2 |
   |-----------|-----------|
   | dato      | dato      |

4. ESTRUCTURA - Usa emojis para secciones:
   ## 🎯 Objetivo
   ## 📚 Explicación  
   ## 👀 Visualízalo (aquí va Desmos)
   ## ✍️ Ejemplo Resuelto
   ## 💡 Tip

🧠 FILOSOFÍA EDUCATIVA:
- Explica el POR QUÉ, no solo el QUÉ
- Usa analogías de la vida real (Netflix, deportes, cocina, videojuegos)
- Si agregas un ejemplo, hazlo PASO A PASO con explicación de cada paso
- Si agregas un gráfico Desmos, explica QUÉ debe observar el estudiante al moverlo
- Anticipa errores comunes y advierte sobre ellos

⚠️ IMPORTANTE:
- Responde SOLO con el contenido modificado
- NO incluyas explicaciones de qué cambiaste
- Mantén TODO lo que no se pidió cambiar
- El resultado debe ser contenido listo para mostrar al estudiante"""

        user_prompt = f"""📄 LECCIÓN: "{request.lesson_title}" (Capítulo: {request.chapter_title})

═══════════════════════════════════════
CONTENIDO ACTUAL:
═══════════════════════════════════════
{request.current_content}
═══════════════════════════════════════

📝 INSTRUCCIÓN DEL ADMINISTRADOR:
"{request.user_instruction}"

═══════════════════════════════════════

Genera el contenido COMPLETO de la lección con la modificación solicitada.
Recuerda: Si agregas un gráfico Desmos, incluye sliders para hacerlo interactivo y explica qué debe observar el estudiante."""
        
        chat = get_gpt_chat(system_message)
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        return {"content": response}
    except Exception as e:
        logging.error(f"Error editing lesson content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Image generation with AI
class GenerateImageRequest(BaseModel):
    prompt: str
    style: str = "educativo"  # educativo, diagrama, ilustracion

@admin_router.post("/generate-image")
async def generate_image(request: GenerateImageRequest, _: str = Depends(verify_admin_token)):
    try:
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="API key no configurada")
        
        # Enhance prompt for educational context
        enhanced_prompt = f"""Create an educational illustration for a math/science course.
Style: {request.style}, clean, professional, suitable for university students.
Content: {request.prompt}
Requirements: Clear labels if needed, high contrast, easy to understand, no text unless necessary."""
        
        image_gen = OpenAIImageGeneration(api_key=api_key)
        images = await image_gen.generate_images(
            prompt=enhanced_prompt,
            model="gpt-image-1",
            number_of_images=1
        )
        
        if images and len(images) > 0:
            # Save image to file with unique name
            image_id = str(uuid.uuid4())
            image_filename = f"{image_id}.png"
            image_path = UPLOADS_DIR / image_filename
            
            async with aiofiles.open(image_path, 'wb') as f:
                await f.write(images[0])
            
            # Return URL path
            image_url = f"/api/uploads/{image_filename}"
            return {"image_url": image_url}
        else:
            raise HTTPException(status_code=500, detail="No se pudo generar la imagen")
    except Exception as e:
        logging.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Upload image from file
@admin_router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")
        
        # Generate unique filename
        ext = file.filename.split('.')[-1] if '.' in file.filename else 'png'
        image_id = str(uuid.uuid4())
        image_filename = f"{image_id}.{ext}"
        image_path = UPLOADS_DIR / image_filename
        
        # Save file
        image_data = await file.read()
        async with aiofiles.open(image_path, 'wb') as f:
            await f.write(image_data)
        
        # Return URL path
        image_url = f"/api/uploads/{image_filename}"
        return {"image_url": image_url}
    except Exception as e:
        logging.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/upload-course-image")
async def upload_course_image(
    file: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")
    
    image_data = await file.read()
    import base64
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    image_url = f"data:{file.content_type};base64,{image_base64}"
    
    return {"image_url": image_url}

# Public endpoints for students to view course content
@api_router.get("/courses/{course_id}/chapters")
async def get_public_course_chapters(course_id: str):
    chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0}).sort("order", 1).to_list(100)
    for chapter in chapters:
        if isinstance(chapter.get('created_at'), str):
            chapter['created_at'] = datetime.fromisoformat(chapter['created_at'])
    return chapters

@api_router.get("/chapters/{chapter_id}/lessons")
async def get_public_chapter_lessons(chapter_id: str):
    lessons = await db.lessons.find({"chapter_id": chapter_id}, {"_id": 0}).sort("order", 1).to_list(100)
    for lesson in lessons:
        if isinstance(lesson.get('created_at'), str):
            lesson['created_at'] = datetime.fromisoformat(lesson['created_at'])
    return lessons

@api_router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str):
    lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    if isinstance(lesson.get('created_at'), str):
        lesson['created_at'] = datetime.fromisoformat(lesson['created_at'])
    return lesson

app.include_router(api_router)
app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
