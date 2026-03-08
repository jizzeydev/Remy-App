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
from datetime import datetime, timezone, timedelta
from emergentintegrations.llm.chat import LlmChat, UserMessage
import PyPDF2
import io
import json
from jose import JWTError, jwt
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
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
    thumbnail_url: Optional[str] = None
    summary: Optional[str] = None
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

class FormulaSearchRequest(BaseModel):
    query: str
    course_id: Optional[str] = None

# Helper functions
def get_gemini_chat(system_message: str):
    api_key = os.environ.get('GEMINI_API_KEY')
    session_id = str(uuid.uuid4())
    chat = LlmChat(
        api_key=api_key,
        session_id=session_id,
        system_message=system_message
    ).with_model("gemini", "gemini-3-pro-preview")
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
        system_message = f"""Eres un experto en educación creando resúmenes concisos para el curso: {request.course_title}.
        
Crea un resumen estructurado del material proporcionado que incluya:
- Conceptos clave
- Fórmulas importantes (en formato LaTeX cuando sea necesario)
- Puntos principales a recordar
- Aplicaciones prácticas

El resumen debe ser claro, conciso y enfocado en lo más importante para estudiantes universitarios.
        """
        
        chat = get_gemini_chat(system_message)
        user_message = UserMessage(text=f"Resume el siguiente material educativo:\n\n{request.pdf_content[:15000]}")
        response = await chat.send_message(user_message)
        
        return {"summary": response}
    except Exception as e:
        logging.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/generate-questions")
async def generate_questions(request: GenerateQuestionsRequest, _: str = Depends(verify_admin_token)):
    try:
        system_message = f"""Eres un experto en educación creando preguntas de examen de opción múltiple.
        
Genera {request.num_questions} preguntas basadas EXCLUSIVAMENTE en el material proporcionado.

Cada pregunta debe tener:
- Enunciado claro
- 4 opciones (A, B, C, D)
- Una respuesta correcta
- Explicación detallada de por qué es correcta
- Si es necesario, incluir LaTeX para fórmulas matemáticas

Formato JSON requerido:
{{
  "questions": [
    {{
      "question_text": "texto de la pregunta",
      "options": ["A) opción 1", "B) opción 2", "C) opción 3", "D) opción 4"],
      "correct_answer": "A",
      "explanation": "explicación detallada",
      "latex_content": "contenido LaTeX si aplica",
      "difficulty": "medio"
    }}
  ]
}}
        """
        
        chat = get_gemini_chat(system_message)
        user_message = UserMessage(
            text=f"Genera {request.num_questions} preguntas sobre el tema '{request.topic}' del siguiente material:\n\n{request.pdf_content[:15000]}"
        )
        response = await chat.send_message(user_message)
        
        try:
            questions_data = json.loads(response)
            questions = questions_data.get("questions", [])
        except:
            questions = []
        
        return {"questions": questions}
    except Exception as e:
        logging.error(f"Error generating questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
