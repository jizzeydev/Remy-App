from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage
import PyPDF2
import io
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

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

class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    user_id: str
    message: str
    course_context: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    timestamp: datetime

class Quiz(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    course_id: str
    title: str
    questions: List[Dict[str, Any]]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuizGenerateRequest(BaseModel):
    user_id: str
    course_id: str
    topic: str
    num_questions: int = 5

class Summary(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    material_id: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SummaryGenerateRequest(BaseModel):
    user_id: str
    material_id: str
    content: str

class Progress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    course_id: str
    completed_modules: int = 0
    total_modules: int
    quizzes_completed: int = 0
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

class FormulaSearchRequest(BaseModel):
    query: str
    course_id: Optional[str] = None

def get_ai_chat(system_message: str):
    api_key = os.environ.get('EMERGENT_LLM_KEY')
    session_id = str(uuid.uuid4())
    chat = LlmChat(
        api_key=api_key,
        session_id=session_id,
        system_message=system_message
    ).with_model("openai", "gpt-5.2")
    return chat

@api_router.get("/")
async def root():
    return {"message": "Bienvenido a Remy - Tu tutor inteligente 24/7"}

@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_remy(request: ChatRequest):
    try:
        system_message = f"""Eres Remy, un tutor inteligente y amigable que ayuda a estudiantes universitarios y preuniversitarios con matemáticas, cálculo, álgebra y física.
        
Tu objetivo es:
- Explicar conceptos de forma clara y paso a paso
- Resolver dudas con ejemplos prácticos
- Ser motivador y positivo
- Adaptar tu lenguaje al nivel del estudiante

{f'Contexto del curso: {request.course_context}' if request.course_context else ''}
        """
        
        chat = get_ai_chat(system_message)
        user_message = UserMessage(text=request.message)
        response = await chat.send_message(user_message)
        
        chat_msg = ChatMessage(
            user_id=request.user_id,
            role="assistant",
            content=response,
            timestamp=datetime.now(timezone.utc)
        )
        
        doc = chat_msg.model_dump()
        doc['timestamp'] = doc['timestamp'].isoformat()
        await db.chat_history.insert_one(doc)
        
        return ChatResponse(
            message=response,
            timestamp=datetime.now(timezone.utc)
        )
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/quiz/generate")
async def generate_quiz(request: QuizGenerateRequest):
    try:
        course = await db.courses.find_one({"id": request.course_id}, {"_id": 0})
        if not course:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        
        system_message = f"""Eres un experto en crear cuestionarios educativos para {course['title']}.
Genera {request.num_questions} preguntas de opción múltiple sobre el tema: {request.topic}

Formato JSON requerido:
{{
  "questions": [
    {{
      "question": "texto de la pregunta",
      "options": ["A) opción 1", "B) opción 2", "C) opción 3", "D) opción 4"],
      "correct_answer": "A",
      "explanation": "explicación detallada"
    }}
  ]
}}
        """
        
        chat = get_ai_chat(system_message)
        user_message = UserMessage(text=f"Genera {request.num_questions} preguntas sobre {request.topic}")
        response = await chat.send_message(user_message)
        
        try:
            questions_data = json.loads(response)
            questions = questions_data.get("questions", [])
        except:
            questions = []
        
        quiz = Quiz(
            user_id=request.user_id,
            course_id=request.course_id,
            title=f"Simulacro: {request.topic}",
            questions=questions
        )
        
        doc = quiz.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.quizzes.insert_one(doc)
        
        return quiz
    except Exception as e:
        logging.error(f"Quiz generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/summary/generate")
async def generate_summary(request: SummaryGenerateRequest):
    try:
        system_message = """Eres un experto en crear resúmenes educativos concisos y claros.
Crea un resumen estructurado del material proporcionado, destacando:
- Conceptos clave
- Fórmulas importantes
- Puntos principales a recordar
        """
        
        chat = get_ai_chat(system_message)
        user_message = UserMessage(text=f"Resume el siguiente material:\n\n{request.content[:5000]}")
        response = await chat.send_message(user_message)
        
        summary = Summary(
            user_id=request.user_id,
            material_id=request.material_id,
            content=response
        )
        
        doc = summary.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.summaries.insert_one(doc)
        
        return summary
    except Exception as e:
        logging.error(f"Summary generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/courses", response_model=List[Course])
async def get_courses():
    courses = await db.courses.find({}, {"_id": 0}).to_list(100)
    for course in courses:
        if isinstance(course.get('created_at'), str):
            course['created_at'] = datetime.fromisoformat(course['created_at'])
    return courses

@api_router.post("/courses", response_model=Course)
async def create_course(course: Course):
    doc = course.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.courses.insert_one(doc)
    return course

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

@api_router.get("/progress/{user_id}")
async def get_user_progress(user_id: str):
    progress_list = await db.progress.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    for progress in progress_list:
        if isinstance(progress.get('last_activity'), str):
            progress['last_activity'] = datetime.fromisoformat(progress['last_activity'])
    return progress_list

@api_router.get("/quizzes/{user_id}", response_model=List[Quiz])
async def get_user_quizzes(user_id: str):
    quizzes = await db.quizzes.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    for quiz in quizzes:
        if isinstance(quiz.get('created_at'), str):
            quiz['created_at'] = datetime.fromisoformat(quiz['created_at'])
    return quizzes

@api_router.get("/summaries/{user_id}", response_model=List[Summary])
async def get_user_summaries(user_id: str):
    summaries = await db.summaries.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    for summary in summaries:
        if isinstance(summary.get('created_at'), str):
            summary['created_at'] = datetime.fromisoformat(summary['created_at'])
    return summaries

@api_router.get("/chat/history/{user_id}", response_model=List[ChatMessage])
async def get_chat_history(user_id: str, limit: int = 50):
    messages = await db.chat_history.find(
        {"user_id": user_id}, 
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit).to_list(limit)
    
    for msg in messages:
        if isinstance(msg.get('timestamp'), str):
            msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])
    
    return list(reversed(messages))

app.include_router(api_router)

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
