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
    chapter_id: Optional[str] = None  # Optional chapter classification
    lesson_id: Optional[str] = None   # Optional lesson classification
    topic: str
    subtopic: Optional[str] = None
    difficulty: str
    question_text: str  # Supports Markdown + KaTeX
    options: List[str]  # Each option supports Markdown + KaTeX
    correct_answer: str  # A, B, C, or D - now randomized
    explanation: str     # Supports Markdown + KaTeX
    latex_content: Optional[str] = None  # Legacy field for main formula
    image_placeholder: Optional[str] = None  # Description for GPAI image generation
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
    pdf_content: Optional[str] = None
    topic_prompt: Optional[str] = None  # New: generate from topic
    lesson_title: str
    chapter_title: str
    course_title: str = ""

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
    """Extract text from PDF with improved handling for Spanish accents and LaTeX-generated PDFs"""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    
    import re
    
    # Fix common LaTeX accent encoding issues in Spanish PDFs
    # LaTeX uses special notation for accents that can get mangled in PDF extraction
    
    # Order matters! Process more specific patterns first
    latex_accent_fixes = [
        # Common Spanish word patterns where accent appears between letters
        # Pattern: consonant + ´ + space + vowel (the accent belongs to the vowel)
        (r"([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ])´\s*([aeiouAEIOU])", r"\1\2́"),
        
        # Pattern: vowel + ´ + space + vowel (accent belongs to second vowel)
        (r"([aeiouAEIOU])´\s+([aeiouAEIOU])", r"\1\2́"),
        
        # Pattern: ´ + space + vowel (standard pattern)
        (r"´\s*a", "á"), (r"´\s*e", "é"), (r"´\s*i", "í"), 
        (r"´\s*o", "ó"), (r"´\s*u", "ú"),
        (r"´\s*A", "Á"), (r"´\s*E", "É"), (r"´\s*I", "Í"), 
        (r"´\s*O", "Ó"), (r"´\s*U", "Ú"),
        
        # Pattern: vowel + space + ´ (accent after space)
        (r"a\s*´", "á"), (r"e\s*´", "é"), (r"i\s*´", "í"),
        (r"o\s*´", "ó"), (r"u\s*´", "ú"),
        (r"A\s*´", "Á"), (r"E\s*´", "É"), (r"I\s*´", "Í"),
        (r"O\s*´", "Ó"), (r"U\s*´", "Ú"),
        
        # Ñ (tilde)
        (r"[˜~]\s*n", "ñ"), (r"n\s*[˜~]", "ñ"),
        (r"[˜~]\s*N", "Ñ"), (r"N\s*[˜~]", "Ñ"),
        
        # Dieresis (ü)
        (r"¨\s*u", "ü"), (r"¨\s*U", "Ü"),
        
        # Dotless i with accent (common in LaTeX)
        (r"´\s*ı", "í"), (r"ı\s*´", "í"),
    ]
    
    for pattern, replacement in latex_accent_fixes:
        text = re.sub(pattern, replacement, text)
    
    # Clean up any remaining combining accents
    # Replace combining acute accent (́) with the proper accented character
    combining_fixes = [
        ("á́", "á"), ("é́", "é"), ("í́", "í"), ("ó́", "ó"), ("ú́", "ú"),
        ("a\u0301", "á"), ("e\u0301", "é"), ("i\u0301", "í"), 
        ("o\u0301", "ó"), ("u\u0301", "ú"),
        ("A\u0301", "Á"), ("E\u0301", "É"), ("I\u0301", "Í"),
        ("O\u0301", "Ó"), ("U\u0301", "Ú"),
    ]
    
    for pattern, replacement in combining_fixes:
        text = text.replace(pattern, replacement)
    
    # Fix hyphenated line breaks (word- \nrest -> wordrest)
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    
    # Fix multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()

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

@api_router.get("/progress/{student_id}/{course_id}")
async def get_course_progress(student_id: str, course_id: str):
    """Get progress for a specific student and course"""
    progress = await db.lesson_progress.find_one(
        {"student_id": student_id, "course_id": course_id},
        {"_id": 0}
    )
    if not progress:
        return {"student_id": student_id, "course_id": course_id, "completed_lessons": []}
    return progress

class CompleteLessonRequest(BaseModel):
    student_id: str
    course_id: str
    lesson_id: str

@api_router.post("/progress/complete-lesson")
async def complete_lesson(request: CompleteLessonRequest):
    """Mark a lesson as completed for a student"""
    # Find existing progress or create new
    progress = await db.lesson_progress.find_one({
        "student_id": request.student_id,
        "course_id": request.course_id
    })
    
    if progress:
        # Add lesson to completed list if not already there
        completed = progress.get("completed_lessons", [])
        if request.lesson_id not in completed:
            completed.append(request.lesson_id)
            await db.lesson_progress.update_one(
                {"student_id": request.student_id, "course_id": request.course_id},
                {"$set": {
                    "completed_lessons": completed,
                    "last_activity": datetime.now(timezone.utc).isoformat()
                }}
            )
    else:
        # Create new progress record
        await db.lesson_progress.insert_one({
            "id": f"progress_{request.student_id}_{request.course_id}",
            "student_id": request.student_id,
            "course_id": request.course_id,
            "completed_lessons": [request.lesson_id],
            "last_activity": datetime.now(timezone.utc).isoformat()
        })
    
    return {"success": True, "message": "Lección completada"}

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
    chapter_id: Optional[str] = None,
    lesson_id: Optional[str] = None,
    topic: Optional[str] = None,
    _: str = Depends(verify_admin_token)
):
    query = {}
    if course_id:
        query["course_id"] = course_id
    if chapter_id:
        query["chapter_id"] = chapter_id
    if lesson_id:
        query["lesson_id"] = lesson_id
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
        "text": text,  # Full text for generation
        "text_preview": text[:500] + "..." if len(text) > 500 else text
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
        import random
        
        system_message = """Eres un experto en evaluación educativa de Se Remonta, especializado en crear preguntas de examen de opción múltiple para estudiantes universitarios de matemáticas y ciencias.

TU TAREA PRINCIPAL:
1. EXTRAE ejercicios del documento proporcionado y conviértelos en preguntas de opción múltiple
2. CREA variantes de los ejercicios (cambiando números, funciones, o contexto)
3. GENERA preguntas nuevas basadas en los conceptos del documento

REGLAS ESTRICTAS PARA LAS FÓRMULAS:
- USA LaTeX en línea con $...$ para fórmulas cortas: $f(x) = x^2$
- USA LaTeX en bloque con $$...$$ para fórmulas largas o importantes
- NUNCA uses \\( \\) ni \\[ \\] - solo $ y $$
- Para fracciones: $\\frac{a}{b}$
- Para derivadas: $\\frac{d}{dx}$, $f'(x)$
- Para raíces: $\\sqrt{x}$, $\\sqrt[n]{x}$
- Para integrales: $\\int f(x)dx$, $\\int_a^b$

IMPORTANTE - VARIACIÓN DE RESPUESTA CORRECTA:
- La respuesta correcta DEBE variar entre A, B, C, D
- NO todas las respuestas deben ser A
- Distribuye las respuestas correctas de forma aleatoria
- Ejemplo: si generas 5 preguntas, las respuestas podrían ser: B, D, A, C, A

FORMATO DE CADA OPCIÓN:
- Formato: "A) contenido con $fórmulas$ si aplica"
- Cada opción en su propia línea
- Los distractores deben ser errores comunes que cometen los estudiantes

FORMATO DE SALIDA - JSON ESTRICTO:
```json
{
  "questions": [
    {
      "question_text": "Enunciado claro. Usa $fórmulas$ para matemáticas.",
      "options": [
        "A) $\\\\frac{d}{dx}[x^3] = 3x^2$",
        "B) $\\\\frac{d}{dx}[x^3] = x^2$",
        "C) $\\\\frac{d}{dx}[x^3] = 3x^3$",
        "D) $\\\\frac{d}{dx}[x^3] = 2x^2$"
      ],
      "correct_answer": "A",
      "explanation": "Explicación paso a paso usando $fórmulas$. La regla de la potencia establece que $\\\\frac{d}{dx}[x^n] = nx^{n-1}$, por lo tanto $\\\\frac{d}{dx}[x^3] = 3x^{3-1} = 3x^2$.",
      "difficulty": "medio",
      "image_placeholder": "Gráfica de f(x)=x³ mostrando la tangente en x=1 con pendiente 3"
    }
  ]
}
```

CAMPO image_placeholder:
- Es OPCIONAL - solo inclúyelo si la pregunta realmente necesita un gráfico o diagrama
- Describe exactamente qué debe mostrar la imagen para que pueda ser generada con IA
- Ejemplos buenos: "Gráfica de la función f(x)=sin(x) con el área bajo la curva entre 0 y π sombreada"
- NO lo incluyas para preguntas puramente algebraicas

IMPORTANTE: Responde SOLO con el JSON, sin texto adicional."""

        # Determine random distribution of correct answers
        letters = ['A', 'B', 'C', 'D']
        answer_distribution = [random.choice(letters) for _ in range(request.num_questions)]
        
        user_prompt = f"""Genera exactamente {request.num_questions} preguntas de opción múltiple sobre el tema "{request.topic}".

DISTRIBUCIÓN SUGERIDA DE RESPUESTAS CORRECTAS (para variar):
{', '.join([f"Pregunta {i+1}: {l}" for i, l in enumerate(answer_distribution)])}

Material de referencia del documento:
---
{request.pdf_content[:15000]}
---

INSTRUCCIONES ESPECÍFICAS:
1. EXTRAE al menos 50% de las preguntas directamente del documento (adaptándolas a formato de opción múltiple)
2. CREA variantes cambiando valores numéricos o funciones similares
3. Las fórmulas DEBEN usar $ para inline y $$ para bloques
4. Cada pregunta debe tener 4 opciones (A, B, C, D) con distractores plausibles
5. La explicación debe mostrar el proceso paso a paso

Distribución de dificultad:
- 30% fácil (conceptos básicos, cálculos directos)
- 50% medio (aplicación de reglas, varios pasos)
- 20% difícil (combinación de conceptos, análisis)

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
            
            # Ensure correct_answer values are valid
            for q in questions:
                if q.get('correct_answer') not in ['A', 'B', 'C', 'D']:
                    q['correct_answer'] = 'A'
                    
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

**DESMOS (Interactivo)** - Usa cuando el estudiante DEBE explorar:
✅ USAR Desmos cuando:
- El estudiante necesita mover un slider para entender
- Comparar múltiples funciones superpuestas
- Ver animaciones (secante → tangente, parámetros cambiando)
- Explorar comportamiento dinámico

Formato: [DESMOS:ecuaciones separadas por punto y coma]
Ejemplo: [DESMOS:y=x^2; a=1; h=0.5; m=((a+h)^2-a^2)/h; y=m*(x-a)+a^2]

**INSERTAR IMAGEN** - Usa para ilustraciones estáticas que requieren precisión:
❌ NO usar Desmos cuando necesites:
- Círculos abiertos (○) o cerrados (●) en puntos específicos
- Discontinuidades de salto con visual del "hueco"
- Anotaciones, flechas, etiquetas específicas
- Líneas punteadas auxiliares

Formato: Inserta directamente en el flujo del texto así:
**[INSERTAR IMAGEN: descripción breve pero clara de qué debe mostrar la imagen]**

EJEMPLOS de cómo insertar imágenes en el texto:

"Al graficar la función, observamos el comportamiento cerca de x=1:

**[INSERTAR IMAGEN: Gráfica de f(x) = (x²-1)/(x-1) mostrando una línea recta y=x+1 con un círculo abierto ○ en el punto (1,2)]**

Como vemos en la imagen, aunque f(1) no existe, la función se acerca a 2."

⚠️ IMPORTANTE SOBRE VISUALIZACIONES:
- Puedes combinar Desmos + imágenes en la misma lección
- Usa Desmos para lo interactivo (explorar con sliders)
- Usa **[INSERTAR IMAGEN:]** para lo estático (discontinuidades, huecos, anotaciones)
- Las descripciones de imagen deben ser claras pero breves (1-2 líneas)

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
(Usa Desmos para exploración interactiva O **[INSERTAR IMAGEN:]** para ilustraciones estáticas detalladas)
- Si el concepto requiere EXPLORAR con sliders → Desmos
- Si el concepto requiere ver puntos específicos, discontinuidades, anotaciones → INSERTAR IMAGEN

## ✍️ Ejemplos Resueltos
(Mínimo 3 ejemplos, del más fácil al más difícil, paso a paso)

## 🎮 Ahora Practícalo Tú
(Ejercicios con pistas, no solo enunciados)

## 📌 Resumen Express
(Los puntos clave en bullets, como "cheat sheet")

## 💡 Tips para el Examen
(Errores comunes, trucos, qué suele preguntarse)

IMPORTANTE: El estudiante debe sentir que PUEDE aprender esto. Sé motivador pero honesto."""

        # Determine if generating from document or from topic prompt
        if request.pdf_content and request.pdf_content.strip():
            # Generate from PDF document - SPECIALIZED PROMPT
            user_prompt = f"""## TU MISIÓN: Transformar Material Académico en Aprendizaje Efectivo

Tienes un documento de referencia de una universidad/instituto. Tu trabajo es:
1. **EXTRAER** todos los conceptos clave, definiciones, teoremas y fórmulas
2. **TRANSFORMAR** ese contenido en una lección que un estudiante novato pueda entender
3. **MEJORAR** la presentación: más ejemplos, más visual, más conectado con la vida real

📖 **Título de la Lección:** "{request.lesson_title}"
📂 **Capítulo:** "{request.chapter_title}"
📚 **Curso:** "{request.course_title}"

---
### DOCUMENTO DE REFERENCIA (extraer conceptos de aquí):
---
{request.pdf_content[:15000]}
---

## INSTRUCCIONES ESPECÍFICAS:

### 1️⃣ ANÁLISIS DEL DOCUMENTO:
- Identifica TODOS los conceptos, definiciones y teoremas mencionados
- Lista las fórmulas matemáticas clave
- Detecta la secuencia lógica del contenido

### 2️⃣ TRANSFORMACIÓN DIDÁCTICA:
- **NO copies el texto tal cual** - reformula todo para que sea más claro
- **SÍ mantén** todos los conceptos, teoremas y fórmulas importantes
- Explica cada concepto como si el estudiante lo viera por primera vez
- Usa analogías de la vida real (streaming, redes sociales, videojuegos, deportes)

### 3️⃣ ENRIQUECIMIENTO:
- Añade ejemplos que NO estén en el documento (mínimo 3, de fácil a difícil)
- Incluye "errores típicos" que los estudiantes cometen
- Agrega conexiones con otros temas del curso
- Crea ejercicios de práctica con pistas

### 4️⃣ VISUALIZACIÓN INTELIGENTE:
Para cada concepto visual del documento, decide:
- **DESMOS** → Si el estudiante debe explorar/mover algo (gráficas de funciones, parámetros)
  Formato: [DESMOS:ecuacion1; ecuacion2; parametro=valor]
- **INSERTAR IMAGEN** → Si necesitas mostrar algo estático específico (discontinuidades con círculos abiertos/cerrados, diagramas anotados)
  Formato: **[INSERTAR IMAGEN: descripción detallada para generar con IA]**

### 5️⃣ ESTRUCTURA DE SALIDA:
Sigue EXACTAMENTE esta estructura con los emojis indicados:

## 🎯 ¿Qué vas a aprender?
(Lista los objetivos basados en el contenido del documento)

## 🤔 ¿Por qué es importante?
(Conexión con aplicaciones reales - NO copiar del documento, crear nuevas)

## 📚 Desarrollo del Tema
(Todos los conceptos del documento, pero explicados de forma más clara y accesible)

## 🔢 Fórmulas Clave
(TODAS las fórmulas del documento en LaTeX, con explicación de cada símbolo)

## 👀 Visualízalo
(Desmos para explorar o **[INSERTAR IMAGEN:]** para diagramas estáticos)

## ✍️ Ejemplos Resueltos
(Mínimo 3 ejemplos paso a paso - pueden incluir los del documento MÁS nuevos)

## 🎮 Ahora Practícalo Tú
(Ejercicios con pistas, incluyendo algunos basados en el documento)

## 📌 Resumen Express
(Los puntos clave del documento en bullets concisos)

## 💡 Tips para el Examen
(Qué suele preguntarse sobre estos temas + errores comunes)

---
⚠️ RECORDATORIO FINAL:
- El documento es tu FUENTE de conceptos, no tu plantilla de texto
- Un estudiante novato debe poder entender TODO sin haber visto el documento original
- Sé más completo y didáctico que el material original

¡Transforma este material en la mejor lección posible!"""

        elif request.topic_prompt and request.topic_prompt.strip():
            # Generate from topic/prompt (NEW)
            user_prompt = f"""Crea una lección COMPLETA, INTERACTIVA y MOTIVADORA desde cero para:

📖 Título de la Lección: "{request.lesson_title}"
📂 Capítulo: "{request.chapter_title}"
📚 Curso: "{request.course_title}"

🎯 TEMA/INSTRUCCIONES DEL USUARIO:
{request.topic_prompt}

REQUISITOS OBLIGATORIOS:
✅ Genera contenido original y completo sobre el tema especificado
✅ Adapta el nivel al curso ({request.course_title})
✅ En la sección "Visualízalo": decide inteligentemente entre Desmos (interactivo) o **[INSERTAR IMAGEN:]** (descripción para imagen estática)
✅ Mínimo 3 ejemplos resueltos paso a paso con diferentes niveles de dificultad
✅ Ejemplos de la vida cotidiana que conecten con el estudiante
✅ Una tabla comparativa o de resumen de los conceptos clave
✅ Tips específicos para aprobar el examen
✅ Tono amigable pero profesional

RECUERDA:
- Si el tema requiere gráficas que el estudiante pueda explorar → usa Desmos con sliders
- Si el tema requiere diagramas estáticos con detalles precisos → usa **[INSERTAR IMAGEN: descripción]**
- El contenido debe ser tan completo como si fuera de un documento de referencia

¡Crea el mejor material didáctico posible para este tema!"""

        else:
            raise HTTPException(status_code=400, detail="Debes proporcionar un documento PDF o un tema para generar contenido")
        
        chat = get_gpt_chat(system_message)
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        return {"content": response}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error generating lesson content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# New: Edit lesson content with AI chat
class EditLessonContentRequest(BaseModel):
    current_content: str
    user_instruction: str
    lesson_title: str = ""
    chapter_title: str = ""
    course_title: str = ""

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

3. **INSERTAR IMAGEN** - Para diagramas estáticos:
   Usa cuando necesites mostrar algo que Desmos no puede hacer bien:
   - Círculos abiertos/cerrados en discontinuidades
   - Diagramas con anotaciones específicas
   - Flechas o marcas especiales
   
   Formato: **[INSERTAR IMAGEN: descripción detallada para generar con IA]**

4. TABLAS MARKDOWN:
   | Columna 1 | Columna 2 |
   |-----------|-----------|
   | dato      | dato      |

5. ESTRUCTURA - Usa emojis para secciones:
   ## 🎯 Objetivo
   ## 📚 Explicación  
   ## 👀 Visualízalo (aquí va Desmos o INSERTAR IMAGEN)
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

        user_prompt = f"""📚 CURSO: "{request.course_title}"
📂 CAPÍTULO: "{request.chapter_title}"
📄 LECCIÓN: "{request.lesson_title}"

═══════════════════════════════════════
CONTENIDO ACTUAL:
═══════════════════════════════════════
{request.current_content}
═══════════════════════════════════════

📝 INSTRUCCIÓN DEL ADMINISTRADOR:
"{request.user_instruction}"

═══════════════════════════════════════

Genera el contenido COMPLETO de la lección con la modificación solicitada.
Recuerda: Si agregas visualizaciones, usa Desmos para interactivo o **[INSERTAR IMAGEN:]** para estático."""
        
        chat = get_gpt_chat(system_message)
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        return {"content": response}
    except Exception as e:
        logging.error(f"Error editing lesson content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Edit question content with AI
class EditQuestionContentRequest(BaseModel):
    current_content: str  # JSON stringified question data or main content
    user_instruction: str
    question_data: Dict[str, Any] = {}  # Full question object for context
    topic: str = ""
    course_title: str = ""

@admin_router.post("/edit-question-content")
async def edit_question_content(request: EditQuestionContentRequest, _: str = Depends(verify_admin_token)):
    try:
        system_message = """Eres REMY, el asistente educativo de Se Remonta. Tu trabajo es MEJORAR preguntas de examen para que evalúen correctamente y ayuden a los estudiantes a aprender.

🎯 TU MISIÓN AL EDITAR PREGUNTAS:
- Mejorar la claridad del enunciado
- Crear distractores (opciones incorrectas) que sean PLAUSIBLES pero claramente distinguibles
- Hacer explicaciones paso a paso que enseñen
- Mantener el nivel de dificultad apropiado

📐 FORMATO DE RESPUESTA - JSON ESTRICTO:
Responde SIEMPRE con un JSON válido con esta estructura exacta:

```json
{
  "question_text": "Enunciado claro. Usa $fórmulas$ para matemáticas.",
  "options": [
    "A) Primera opción con $fórmula$ si aplica",
    "B) Segunda opción",
    "C) Tercera opción",
    "D) Cuarta opción"
  ],
  "correct_answer": "A",
  "explanation": "Explicación paso a paso...",
  "difficulty": "fácil|medio|difícil"
}
```

📝 REGLAS PARA FÓRMULAS:
- En línea: $formula$ (ej: $f(x) = x^2$)
- En bloque: $$formula$$ (para ecuaciones importantes)
- Usa \\frac{a}{b} para fracciones
- Usa \\sqrt{x} para raíces

🎓 REGLAS PARA OPCIONES:
- Cada opción debe empezar con letra y paréntesis: "A) ", "B) ", etc.
- Los distractores deben ser errores COMUNES que estudiantes realmente cometen
- Evita opciones obviamente incorrectas
- La respuesta correcta puede ser A, B, C o D (varía)

💡 REGLAS PARA EXPLICACIONES:
- Muestra el proceso paso a paso
- Explica POR QUÉ cada distractor es incorrecto
- Usa fórmulas LaTeX donde corresponda
- Sé didáctico pero conciso

⚠️ IMPORTANTE:
- Responde SOLO con el JSON
- NO incluyas texto adicional antes o después
- Si cambias la respuesta correcta, actualiza "correct_answer"
- Mantén coherencia entre pregunta, opciones y explicación"""

        # Build context from question data
        q_data = request.question_data
        current_question = f"""Tema: {request.topic}
Curso: {request.course_title}

Pregunta actual:
- Enunciado: {q_data.get('question_text', request.current_content)}
- Opciones: {json.dumps(q_data.get('options', []), ensure_ascii=False)}
- Respuesta correcta: {q_data.get('correct_answer', 'A')}
- Dificultad: {q_data.get('difficulty', 'medio')}
- Explicación: {q_data.get('explanation', '')}"""

        user_prompt = f"""📝 PREGUNTA A MODIFICAR:
═══════════════════════════════════════
{current_question}
═══════════════════════════════════════

✏️ INSTRUCCIÓN DEL ADMINISTRADOR:
"{request.user_instruction}"

═══════════════════════════════════════

Genera la pregunta COMPLETA modificada en formato JSON.
Recuerda: Los distractores deben ser errores plausibles, y la explicación debe enseñar."""
        
        chat = get_gpt_chat(system_message)
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        # Parse JSON response
        try:
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            clean_response = clean_response.strip()
            
            question_data = json.loads(clean_response)
            
            return {
                "content": json.dumps(question_data, ensure_ascii=False),
                "question_data": question_data,
                "message": "✅ ¡Pregunta actualizada! Revisa los cambios."
            }
        except json.JSONDecodeError as je:
            logging.error(f"JSON parse error in edit question: {je}")
            return {
                "content": response,
                "message": "⚠️ Respuesta generada pero puede necesitar ajustes manuales."
            }
            
    except Exception as e:
        logging.error(f"Error editing question content: {str(e)}")
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
