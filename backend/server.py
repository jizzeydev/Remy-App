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
import io
import json
from jose import JWTError, jwt
from passlib.context import CryptContext

# Import new routers
from routes import auth as auth_routes
from routes import payments as payments_routes
from routes import admin_users as admin_users_routes
from routes import admin_analytics as admin_analytics_routes
from routes import images as images_routes
from services.image_storage import init_image_storage

ROOT_DIR = Path(__file__).parent
UPLOADS_DIR = ROOT_DIR / 'uploads'
UPLOADS_DIR.mkdir(exist_ok=True)

load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize new routers with database connection
auth_routes.set_db(db)
payments_routes.set_db(db)
admin_users_routes.set_db(db)
admin_analytics_routes.set_db(db)

# Initialize image storage with GridFS
init_image_storage(db)

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
    university_id: Optional[str] = None  # None = "General", otherwise university ID
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
    # Template linking: if set, this chapter inherits content from the template chapter
    template_chapter_id: Optional[str] = None  # ID of the source chapter (from General courses)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Lesson(BaseModel):
    """A lesson is composed of an ordered list of typed content blocks.

    Block types (see frontend/src/lib/blockTypes.js for the full schema):
      texto, definicion, teorema, intuicion, ejemplo_resuelto,
      grafico_desmos, figura, verificacion, errores_comunes, resumen

    Each block is a dict with at minimum {id: str, type: str, ...type-specific fields}.
    The admin editor constructs blocks via typed forms; loose validation here is fine.
    """
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chapter_id: str
    title: str
    description: Optional[str] = None
    blocks: List[Dict[str, Any]] = Field(default_factory=list)
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
    chapter_id: Optional[str] = None  # Chapter classification (recommended)
    lesson_id: Optional[str] = None   # Optional lesson classification
    topic: Optional[str] = None  # Now optional, chapter_id is preferred
    subtopic: Optional[str] = None
    difficulty: str = "medio"
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
    course_title: Optional[str] = None
    topic: str  # Legacy field, will use chapter_ids now
    subtopic: Optional[str] = None
    chapter_ids: List[str] = []  # Chapters selected for this quiz
    lesson_ids: List[str] = []   # Specific lessons selected
    difficulty: str = "medio"
    time_limit_minutes: Optional[int] = None  # Time limit in minutes
    questions: List[Dict[str, Any]]
    answers: Dict[int, str] = {}
    score: Optional[float] = None
    grade: Optional[float] = None  # Chilean grade 1-7
    completed: bool = False
    time_spent_seconds: Optional[int] = None
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

class GoogleLoginRequest(BaseModel):
    credential: str  # Google ID token (JWT) from Google Identity Services

class Token(BaseModel):
    access_token: str
    token_type: str

class QuizStartRequest(BaseModel):
    user_id: str
    course_id: str
    chapter_ids: List[str] = []  # Chapters to include
    lesson_ids: List[str] = []   # Specific lessons to include (optional)
    difficulty: str = "medio"    # fácil, medio, difícil
    num_questions: int = 10
    time_limit_minutes: Optional[int] = None  # Optional time limit
    topic: Optional[str] = None  # Legacy field for backward compatibility

class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: Dict[str, str]  # Changed to str keys for JSON compatibility
    time_spent_seconds: Optional[int] = None

def calculate_chilean_grade(percentage: float) -> float:
    """
    Calculate Chilean grade (1-7) with 60% requirement for grade 4.
    Scale: 1 (0%) to 4 (60%) to 7 (100%)
    """
    if percentage < 0:
        percentage = 0
    if percentage > 100:
        percentage = 100
    
    if percentage < 60:
        # Linear scale from 1 (0%) to 4 (60%)
        grade = 1 + (percentage / 60) * 3
    else:
        # Linear scale from 4 (60%) to 7 (100%)
        grade = 4 + ((percentage - 60) / 40) * 3
    
    return round(grade, 1)

class FormulaSearchRequest(BaseModel):
    query: str
    course_id: Optional[str] = None

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
        subject: str = payload.get("sub")
        token_type: str = payload.get("type", "")
        
        if subject is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        # Check if it's a Google admin token
        if token_type == "admin_google":
            if subject.lower() not in [e.lower() for e in ALLOWED_ADMIN_EMAILS]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )
            return subject
        
        # Traditional username/password admin
        if subject != os.environ.get('ADMIN_USERNAME'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return subject
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


# Public endpoints
@api_router.get("/")
async def root():
    return {"message": "Bienvenido a Remy - Tu plataforma de estudio inteligente"}

# Serve uploaded images - supports both GridFS and filesystem
from fastapi.responses import FileResponse, Response

@api_router.get("/uploads/{filename}")
async def get_uploaded_image(filename: str):
    """Serve images - checks GridFS first, then filesystem for backward compatibility"""
    from services.image_storage import get_image
    
    # Try GridFS first (new persistent storage)
    image_id = filename.split('.')[0] if '.' in filename else filename
    image_data = await get_image(image_id)
    
    if image_data:
        return Response(
            content=image_data["content"],
            media_type=image_data["content_type"],
            headers={"Cache-Control": "public, max-age=31536000"}
        )
    
    # Fallback to filesystem (legacy)
    file_path = UPLOADS_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="Imagen no encontrada")

@api_router.get("/courses", response_model=List[Course])
async def get_courses(
    university_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Get visible courses with optional filters"""
    query = {"$or": [{"visible_to_students": True}, {"visible_to_students": {"$exists": False}}]}
    
    # Filter by university
    if university_id:
        if university_id == "general":
            query["$and"] = [
                query.pop("$or"),
                {"$or": [{"university_id": None}, {"university_id": {"$exists": False}}]}
            ]
            query["$or"] = query["$and"][0]
            query["$and"] = [{"$or": query.pop("$or")}, query["$and"][1]]
        else:
            query["university_id"] = university_id
    
    # Search by title
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
    
    courses = await db.courses.find(query, {"_id": 0}).to_list(500)
    
    for course in courses:
        if isinstance(course.get('created_at'), str):
            course['created_at'] = datetime.fromisoformat(course['created_at'])
        
        # Add university info
        uni_id = course.get('university_id')
        if uni_id:
            uni = await db.library_universities.find_one(
                {"id": uni_id},
                {"_id": 0, "name": 1, "short_name": 1, "logo_url": 1}
            )
            course['university'] = uni
        else:
            course['university'] = {"name": "General", "short_name": "GEN"}
    
    return courses

@api_router.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: str):
    course = await db.courses.find_one(
        {"id": course_id, "$or": [{"visible_to_students": True}, {"visible_to_students": {"$exists": False}}]}, 
        {"_id": 0}
    )
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
    import random
    
    # Check trial limits for users without active subscription
    user = await db.users.find_one({"user_id": request.user_id}, {"_id": 0})
    
    if user:
        has_subscription = user.get("subscription_status") == "active"
        
        if not has_subscription:
            # Check trial status
            trial_active = user.get("trial_active", False)
            trial_end = user.get("trial_end_date")
            
            # Check if trial has expired
            if trial_end:
                if isinstance(trial_end, str):
                    trial_end_dt = datetime.fromisoformat(trial_end.replace('Z', '+00:00'))
                else:
                    trial_end_dt = trial_end
                
                if datetime.now(timezone.utc) > trial_end_dt:
                    trial_active = False
                    # Update in database
                    await db.users.update_one(
                        {"user_id": request.user_id},
                        {"$set": {"trial_active": False}}
                    )
            
            if trial_active:
                # Check simulation limit
                trial_simulations_used = user.get("trial_simulations_used", 0)
                if trial_simulations_used >= 10:
                    raise HTTPException(
                        status_code=403,
                        detail="Has alcanzado el límite de 10 simulacros de la prueba gratuita. Suscríbete para seguir generando simulacros ilimitados."
                    )
            else:
                # Trial expired or not active and no subscription
                raise HTTPException(
                    status_code=403,
                    detail="Tu prueba gratuita ha terminado. Suscríbete para acceder a los simulacros."
                )
    
    # Build query based on chapter_ids and lesson_ids
    query = {"course_id": request.course_id}
    
    # If specific chapters or lessons are provided, use them
    if request.chapter_ids or request.lesson_ids:
        or_conditions = []
        if request.chapter_ids:
            or_conditions.append({"chapter_id": {"$in": request.chapter_ids}})
        if request.lesson_ids:
            or_conditions.append({"lesson_id": {"$in": request.lesson_ids}})
        if or_conditions:
            query["$or"] = or_conditions
    
    # Filter by difficulty if not "todos"
    if request.difficulty and request.difficulty != "todos":
        query["difficulty"] = request.difficulty
    
    all_questions = await db.questions.find(query, {"_id": 0}).to_list(1000)
    
    # If using legacy topic field
    if not all_questions and request.topic:
        legacy_query = {"course_id": request.course_id, "topic": request.topic}
        if request.difficulty and request.difficulty != "todos":
            legacy_query["difficulty"] = request.difficulty
        all_questions = await db.questions.find(legacy_query, {"_id": 0}).to_list(1000)
    
    if len(all_questions) == 0:
        raise HTTPException(
            status_code=400, 
            detail="No hay preguntas disponibles para los filtros seleccionados"
        )
    
    # Limit to available questions if fewer than requested
    num_to_select = min(request.num_questions, len(all_questions))
    selected_questions = random.sample(all_questions, num_to_select)
    
    # Get course title for display
    course = await db.courses.find_one({"id": request.course_id}, {"_id": 0})
    course_title = course.get("title", "") if course else ""
    
    # Build topic string from chapters for display
    topic = request.topic or "Simulacro personalizado"
    if request.chapter_ids:
        chapters = await db.chapters.find(
            {"id": {"$in": request.chapter_ids}}, 
            {"_id": 0, "title": 1}
        ).to_list(10)
        if chapters:
            topic = ", ".join([c.get("title", "") for c in chapters])
    
    quiz_attempt = QuizAttempt(
        user_id=request.user_id,
        course_id=request.course_id,
        course_title=course_title,
        topic=topic,
        chapter_ids=request.chapter_ids,
        lesson_ids=request.lesson_ids,
        difficulty=request.difficulty,
        time_limit_minutes=request.time_limit_minutes,
        questions=selected_questions,
        answers={},
        completed=False
    )
    
    doc = quiz_attempt.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.quiz_attempts.insert_one(doc)
    
    # Increment trial simulation counter if user is on trial
    if user and user.get("trial_active") and user.get("subscription_status") != "active":
        await db.users.update_one(
            {"user_id": request.user_id},
            {"$inc": {"trial_simulations_used": 1}}
        )
    
    # Return questions without answers for the quiz
    questions_for_quiz = [
        {k: v for k, v in q.items() if k not in ['correct_answer', 'explanation']}
        for q in selected_questions
    ]
    
    return {
        "quiz_id": quiz_attempt.id,
        "questions": questions_for_quiz,
        "time_limit_minutes": request.time_limit_minutes,
        "total_questions": len(selected_questions)
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
        correct_answer = question.get('correct_answer', '')
        is_correct = user_answer == correct_answer
        if is_correct:
            correct_count += 1
        
        results.append({
            "question_index": idx,
            "question_text": question.get('question_text', ''),
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.get('explanation', '')
        })
    
    total_questions = len(quiz['questions'])
    score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    grade = calculate_chilean_grade(score)
    
    # Update quiz with results
    update_data = {
        "answers": request.answers, 
        "score": score,
        "grade": grade,
        "completed": True
    }
    if request.time_spent_seconds:
        update_data["time_spent_seconds"] = request.time_spent_seconds
    
    await db.quiz_attempts.update_one(
        {"id": request.quiz_id},
        {"$set": update_data}
    )
    
    # Update user progress
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
        "grade": grade,
        "correct_count": correct_count,
        "total_questions": total_questions,
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

@api_router.delete("/quiz/{quiz_id}")
async def delete_quiz(quiz_id: str, user_id: str):
    """Delete a quiz attempt"""
    result = await db.quiz_attempts.delete_one({"id": quiz_id, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Simulacro no encontrado")
    return {"success": True, "message": "Simulacro eliminado"}

@api_router.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str):
    """Get a specific quiz by ID"""
    quiz = await db.quiz_attempts.find_one({"id": quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Simulacro no encontrado")
    return quiz

# Migration endpoint to assign chapter_id to existing questions
@api_router.post("/migrate/questions-chapter-id")
async def migrate_questions_chapter_id():
    """Migrate existing questions to assign chapter_id based on topic field"""
    # Get all courses and their chapters
    courses = await db.courses.find({}, {"_id": 0}).to_list(100)
    
    migrated_count = 0
    for course in courses:
        chapters = await db.chapters.find({"course_id": course["id"]}, {"_id": 0}).to_list(100)
        
        # Create mapping of topic name to chapter_id
        for chapter in chapters:
            chapter_title = chapter.get("title", "")
            
            # Update questions where topic matches chapter title and chapter_id is null
            result = await db.questions.update_many(
                {
                    "course_id": course["id"],
                    "topic": chapter_title,
                    "$or": [{"chapter_id": None}, {"chapter_id": {"$exists": False}}]
                },
                {"$set": {"chapter_id": chapter["id"]}}
            )
            migrated_count += result.modified_count
            
            # Also try with lowercase match
            result2 = await db.questions.update_many(
                {
                    "course_id": course["id"],
                    "topic": {"$regex": f"^{chapter_title}$", "$options": "i"},
                    "$or": [{"chapter_id": None}, {"chapter_id": {"$exists": False}}]
                },
                {"$set": {"chapter_id": chapter["id"]}}
            )
            migrated_count += result2.modified_count
    
    return {"success": True, "migrated_questions": migrated_count}

# Admin endpoints
# Allowed admin emails for Google login
ALLOWED_ADMIN_EMAILS = [
    'seremonta.cl@gmail.com',
    'admin@seremonta.cl'
]

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

@admin_router.post("/google-login", response_model=Token)
async def admin_google_login(request: GoogleLoginRequest):
    """
    Authenticate admin via Google ID token (Google Identity Services).
    Only allows emails listed in ALLOWED_ADMIN_EMAILS.
    """
    from routes.auth import verify_google_id_token

    if not request.credential:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="credential requerido"
        )

    auth_data = verify_google_id_token(request.credential)

    email = (auth_data.get("email") or "").lower()
    name = auth_data.get("name") or auth_data.get("given_name") or "Admin"

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo obtener el email de Google"
        )
    
    # Check if email is in allowed admin list
    if email not in [e.lower() for e in ALLOWED_ADMIN_EMAILS]:
        logger.warning(f"Unauthorized admin login attempt: {email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"El email {email} no está autorizado como administrador"
        )
    
    logger.info(f"Admin Google login successful: {email}")
    
    # Create JWT token for admin
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email, "type": "admin_google"},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@admin_router.get("/verify")
async def verify_admin(username: str = Depends(verify_admin_token)):
    return {"username": username, "verified": True}

# Get all courses for admin (including hidden ones)
@admin_router.get("/courses")
async def admin_get_courses(
    university_id: Optional[str] = None,
    search: Optional[str] = None,
    _: str = Depends(verify_admin_token)
):
    """Get all courses including hidden ones, with optional filters"""
    query = {}
    
    # Filter by university
    if university_id:
        if university_id == "general":
            query["$or"] = [{"university_id": None}, {"university_id": {"$exists": False}}]
        else:
            query["university_id"] = university_id
    
    # Search by title
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
    
    courses = await db.courses.find(query, {"_id": 0}).to_list(500)
    
    # Add university info to each course
    for course in courses:
        if isinstance(course.get('created_at'), str):
            course['created_at'] = course['created_at']
        # Add visibility field if not present
        if 'visible_to_students' not in course:
            course['visible_to_students'] = True
        
        # Add university info
        uni_id = course.get('university_id')
        if uni_id:
            uni = await db.library_universities.find_one(
                {"id": uni_id},
                {"_id": 0, "name": 1, "short_name": 1, "logo_url": 1}
            )
            course['university'] = uni
        else:
            course['university'] = {"name": "General", "short_name": "GEN"}
    
    return courses

@admin_router.post("/courses", response_model=Course)
async def create_course(course: Course, _: str = Depends(verify_admin_token)):
    doc = course.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['visible_to_students'] = True  # Default to visible
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

# Toggle course visibility
@admin_router.patch("/courses/{course_id}/visibility")
async def toggle_course_visibility(course_id: str, visible: bool, _: str = Depends(verify_admin_token)):
    """Toggle course visibility for students"""
    result = await db.courses.update_one(
        {"id": course_id}, 
        {"$set": {"visible_to_students": visible}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"message": f"Curso {'visible' if visible else 'oculto'} para estudiantes", "visible_to_students": visible}

@admin_router.delete("/courses/{course_id}")
async def delete_course(course_id: str, admin: str = Depends(verify_admin_token)):
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0}).to_list(1000)
    chapter_ids = [c["id"] for c in chapters]
    lessons = await db.lessons.find({"chapter_id": {"$in": chapter_ids}}, {"_id": 0}).to_list(5000) if chapter_ids else []
    await _trash_put("course", course["id"], course.get("title", "(sin título)"),
                     payload=course, children={"chapters": chapters, "lessons": lessons},
                     deleted_by=admin, course_id=course_id)
    if chapter_ids:
        await db.lessons.delete_many({"chapter_id": {"$in": chapter_ids}})
        await db.chapters.delete_many({"course_id": course_id})
    await db.courses.delete_one({"id": course_id})
    return {"message": "Curso movido a la papelera"}

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
    
    # Handle chapter_id - check if it's a linked chapter
    actual_chapter_id = chapter_id
    if chapter_id:
        chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
        if chapter and chapter.get("template_chapter_id"):
            actual_chapter_id = chapter["template_chapter_id"]
        query["chapter_id"] = actual_chapter_id
    
    if lesson_id:
        query["lesson_id"] = lesson_id
    if topic:
        query["topic"] = topic
    
    questions = await db.questions.find(query, {"_id": 0}).to_list(1000)
    
    # Mark questions as inherited if from template
    if chapter_id and actual_chapter_id != chapter_id:
        for q in questions:
            q['inherited_from_template'] = True
            q['read_only'] = True
    
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
async def delete_question(question_id: str, admin: str = Depends(verify_admin_token)):
    question = await db.questions.find_one({"id": question_id}, {"_id": 0})
    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    title = (question.get("text") or question.get("question") or "")[:80] or "(sin enunciado)"
    await _trash_put("question", question["id"], title, payload=question,
                     deleted_by=admin,
                     course_id=question.get("course_id"),
                     chapter_id=question.get("chapter_id"),
                     lesson_id=question.get("lesson_id"))
    await db.questions.delete_one({"id": question_id})
    return {"message": "Pregunta movida a la papelera"}


# ==================== CSV IMPORT FOR QUESTIONS ====================
@admin_router.post("/questions/import-csv/{course_id}")
async def import_questions_csv(
    course_id: str,
    csv_file: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    """
    Import questions from CSV file for a specific course.
    
    CSV format (columnas separadas - más fácil de usar):
    capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion
    
    - capitulo: Nombre del capítulo (buscará por título, si no existe se ignora)
    - leccion: Nombre de la lección (buscará por título, si no existe se ignora)
    - dificultad: fácil, medio o difícil
    - enunciado: Pregunta (soporta Markdown + LaTeX con $)
    - opcion_a, opcion_b, opcion_c, opcion_d: Las 4 alternativas
    - respuesta_correcta: A, B, C o D
    - explicacion: Explicación de la solución
    
    También acepta formato legacy con pipe-separated options.
    """
    import csv as csv_module
    
    # Validate file type
    if not csv_file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser CSV")
    
    # Verify course exists
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Get chapters and lessons for this course (for name lookup)
    chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0}).to_list(100)
    chapter_map = {ch.get('title', '').lower().strip(): ch.get('id') for ch in chapters}
    
    # Build lesson map (lesson name -> lesson id, grouped by chapter)
    lesson_map = {}
    for ch in chapters:
        lessons = await db.lessons.find({"chapter_id": ch.get('id')}, {"_id": 0}).to_list(100)
        for lesson in lessons:
            lesson_key = f"{ch.get('title', '').lower().strip()}|{lesson.get('title', '').lower().strip()}"
            lesson_map[lesson_key] = lesson.get('id')
            # Also map just lesson name (in case chapter not provided)
            lesson_map[lesson.get('title', '').lower().strip()] = lesson.get('id')
    
    # Read CSV content
    content = await csv_file.read()
    
    # Try different encodings
    text_content = None
    for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
        try:
            text_content = content.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    
    if not text_content:
        raise HTTPException(status_code=400, detail="No se pudo decodificar el archivo CSV. Use UTF-8.")
    
    # Parse CSV
    csv_reader = csv_module.DictReader(io.StringIO(text_content))
    
    created_questions = []
    errors = []
    row_num = 1
    
    for row in csv_reader:
        row_num += 1
        try:
            # Check if using new format (with capitulo, enunciado, opcion_a) or legacy format
            is_new_format = 'enunciado' in row or 'opcion_a' in row
            
            if is_new_format:
                # NEW FORMAT: capitulo, leccion, dificultad, enunciado, opcion_a-d, respuesta_correcta, explicacion
                question_text = row.get('enunciado', '').strip()
                if not question_text:
                    errors.append(f"Fila {row_num}: enunciado es requerido")
                    continue
                
                # Get options from separate columns
                opcion_a = row.get('opcion_a', '').strip()
                opcion_b = row.get('opcion_b', '').strip()
                opcion_c = row.get('opcion_c', '').strip()
                opcion_d = row.get('opcion_d', '').strip()
                
                if not opcion_a or not opcion_b:
                    errors.append(f"Fila {row_num}: Se necesitan al menos opciones A y B")
                    continue
                
                options = [f"A) {opcion_a}", f"B) {opcion_b}"]
                if opcion_c:
                    options.append(f"C) {opcion_c}")
                if opcion_d:
                    options.append(f"D) {opcion_d}")
                
                correct_answer = row.get('respuesta_correcta', '').strip().upper()
                explanation = row.get('explicacion', '').strip() or None
                
                # Lookup chapter by name
                capitulo = row.get('capitulo', '').strip().lower()
                chapter_id = chapter_map.get(capitulo) if capitulo else None
                
                # Lookup lesson by name (with chapter context if available)
                leccion = row.get('leccion', '').strip().lower()
                lesson_id = None
                if leccion:
                    if capitulo:
                        lesson_key = f"{capitulo}|{leccion}"
                        lesson_id = lesson_map.get(lesson_key) or lesson_map.get(leccion)
                    else:
                        lesson_id = lesson_map.get(leccion)
                
                difficulty = row.get('dificultad', '').strip().lower() or 'medio'
            else:
                # LEGACY FORMAT: chapter_id, lesson_id, question_text, options (pipe-separated), correct_answer, explanation, difficulty
                question_text = row.get('question_text', '').strip()
                if not question_text:
                    errors.append(f"Fila {row_num}: question_text es requerido")
                    continue
                
                # Parse options (pipe-separated)
                options_str = row.get('options', '').strip()
                if not options_str:
                    errors.append(f"Fila {row_num}: options es requerido")
                    continue
                
                options = [opt.strip() for opt in options_str.split('|') if opt.strip()]
                if len(options) < 2:
                    errors.append(f"Fila {row_num}: Se necesitan al menos 2 opciones separadas por |")
                    continue
                
                correct_answer = row.get('correct_answer', '').strip().upper()
                chapter_id = row.get('chapter_id', '').strip() or None
                lesson_id = row.get('lesson_id', '').strip() or None
                explanation = row.get('explanation', '').strip() or None
                difficulty = row.get('difficulty', '').strip().lower() or 'medio'
            
            if not correct_answer:
                errors.append(f"Fila {row_num}: respuesta_correcta es requerido")
                continue
            
            # Normalize difficulty
            difficulty_map = {'fácil': 'fácil', 'facil': 'fácil', 'medio': 'medio', 'difícil': 'difícil', 'dificil': 'difícil', 'easy': 'fácil', 'medium': 'medio', 'hard': 'difícil'}
            difficulty = difficulty_map.get(difficulty, 'medio')
            
            # Create question
            question_id = str(uuid.uuid4())
            question = {
                "id": question_id,
                "course_id": course_id,
                "chapter_id": chapter_id,
                "lesson_id": lesson_id,
                "question_text": question_text,
                "question_type": "multiple_choice",
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "difficulty": difficulty,
                "image_url": None,
                "source": "csv_import",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            await db.questions.insert_one(question)
            created_questions.append(question_id)
            
        except Exception as e:
            errors.append(f"Fila {row_num}: {str(e)}")
    
    logging.info(f"CSV Import: Created {len(created_questions)} questions for course {course_id}")
    
    return {
        "success": True,
        "created_count": len(created_questions),
        "errors_count": len(errors),
        "errors": errors[:10],  # Return first 10 errors
        "question_ids": created_questions
    }


@admin_router.get("/questions/csv-template")
async def get_questions_csv_template(_: str = Depends(verify_admin_token)):
    """Get CSV template for importing questions - NEW FORMAT with separate columns"""
    from fastapi.responses import Response
    
    csv_content = """capitulo,leccion,dificultad,enunciado,opcion_a,opcion_b,opcion_c,opcion_d,respuesta_correcta,explicacion
Derivadas,Regla de la Cadena,medio,"Calcule la derivada de $f(x) = (3x^2 + 1)^4$",$24x(3x^2 + 1)^3$,$12x(3x^2 + 1)^3$,$4(3x^2 + 1)^3$,$24x(3x^2 + 1)^4$,A,"Usando la regla de la cadena: $f'(x) = 4(3x^2 + 1)^3 \\cdot 6x = 24x(3x^2 + 1)^3$"
Derivadas,Derivadas Básicas,fácil,"Calcule la derivada de $f(x) = x^3 + 2x$",$3x^2 + 2$,$3x^2$,$x^2 + 2$,$3x + 2$,A,"La derivada de $x^3$ es $3x^2$ y la derivada de $2x$ es $2$"
Integrales,Integrales Indefinidas,fácil,"Resuelva la integral $\\int x^2 dx$","$\\frac{x^3}{3} + C$","$x^3 + C$","$2x + C$","$\\frac{x^2}{2} + C$",A,"Usando la regla de potencias: $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$"
Límites,Límites Notables,medio,"Si $\\lim_{x \\to 0} \\frac{\\sin(x)}{x} = L$, ¿cuál es el valor de $L$?",$0$,$1$,$\\infty$,No existe,B,"Este es un límite notable. $\\lim_{x \\to 0} \\frac{\\sin(x)}{x} = 1$"
"""
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=plantilla_preguntas_remy.csv"
        }
    )


# Chapters endpoints
@admin_router.get("/courses/{course_id}/chapters")
async def get_course_chapters(course_id: str, _: str = Depends(verify_admin_token)):
    chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0}).sort("order", 1).to_list(100)
    
    for chapter in chapters:
        if isinstance(chapter.get('created_at'), str):
            chapter['created_at'] = datetime.fromisoformat(chapter['created_at'])
        
        # If linked to a template, get template info
        template_id = chapter.get('template_chapter_id')
        if template_id:
            template = await db.chapters.find_one({"id": template_id}, {"_id": 0})
            if template:
                # Get template's course info
                template_course = await db.courses.find_one({"id": template.get('course_id')}, {"_id": 0, "title": 1, "university_id": 1})
                chapter['template_info'] = {
                    "chapter_title": template.get('title'),
                    "course_title": template_course.get('title') if template_course else None,
                    "is_general": template_course.get('university_id') is None if template_course else True
                }
                chapter['is_linked'] = True
        else:
            chapter['is_linked'] = False
    
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
async def delete_chapter(chapter_id: str, admin: str = Depends(verify_admin_token)):
    # Check if this is a template chapter being used by other courses
    linked_chapters = await db.chapters.count_documents({"template_chapter_id": chapter_id})
    if linked_chapters > 0:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar: {linked_chapters} capítulo(s) en otros cursos están vinculados a esta plantilla."
        )

    chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
    if not chapter:
        raise HTTPException(status_code=404, detail="Capítulo no encontrado")
    lessons = await db.lessons.find({"chapter_id": chapter_id}, {"_id": 0}).to_list(1000)
    await _trash_put("chapter", chapter["id"], chapter.get("title", "(sin título)"),
                     payload=chapter, children={"lessons": lessons},
                     deleted_by=admin, course_id=chapter.get("course_id"))
    await db.lessons.delete_many({"chapter_id": chapter_id})
    await db.chapters.delete_one({"id": chapter_id})
    return {"message": "Capítulo movido a la papelera"}

# Link chapters from template courses (General courses)
class LinkChaptersRequest(BaseModel):
    template_chapter_ids: List[str]  # IDs of chapters to link from General courses

@admin_router.post("/courses/{course_id}/link-chapters")
async def link_chapters(
    course_id: str,
    request: LinkChaptersRequest,
    _: str = Depends(verify_admin_token)
):
    """
    Link chapters from General courses to this course.
    Creates reference chapters that inherit content from templates.
    """
    # Verify target course exists
    target_course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not target_course:
        raise HTTPException(status_code=404, detail="Curso destino no encontrado")
    
    # Get max order in target course
    max_order_result = await db.chapters.find_one(
        {"course_id": course_id},
        {"order": 1},
        sort=[("order", -1)]
    )
    current_max_order = max_order_result.get("order", 0) if max_order_result else 0
    
    linked_chapters = []
    errors = []
    
    for template_id in request.template_chapter_ids:
        # Get template chapter
        template_chapter = await db.chapters.find_one({"id": template_id}, {"_id": 0})
        if not template_chapter:
            errors.append(f"Capítulo plantilla {template_id} no encontrado")
            continue
        
        # Check if already linked
        existing = await db.chapters.find_one({
            "course_id": course_id,
            "template_chapter_id": template_id
        }, {"_id": 0})
        if existing:
            errors.append(f"Capítulo '{template_chapter.get('title')}' ya está vinculado")
            continue
        
        # Create linked chapter
        current_max_order += 1
        new_chapter = {
            "id": str(uuid.uuid4()),
            "course_id": course_id,
            "title": template_chapter.get("title"),  # Use same title
            "description": template_chapter.get("description", ""),
            "order": current_max_order,
            "template_chapter_id": template_id,  # Link to template
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.chapters.insert_one(new_chapter)
        linked_chapters.append({
            "id": new_chapter["id"],
            "title": new_chapter["title"],
            "template_id": template_id
        })
    
    return {
        "success": True,
        "message": f"Vinculados {len(linked_chapters)} capítulo(s)",
        "linked_chapters": linked_chapters,
        "errors": errors if errors else None
    }

@admin_router.post("/chapters/{chapter_id}/unlink")
async def unlink_chapter(
    chapter_id: str,
    _: str = Depends(verify_admin_token)
):
    """
    Convert a linked chapter to an independent chapter by copying the template content.
    """
    chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
    if not chapter:
        raise HTTPException(status_code=404, detail="Capítulo no encontrado")
    
    template_id = chapter.get("template_chapter_id")
    if not template_id:
        raise HTTPException(status_code=400, detail="Este capítulo no está vinculado a una plantilla")
    
    # Copy lessons from template
    template_lessons = await db.lessons.find({"chapter_id": template_id}, {"_id": 0}).to_list(100)
    
    for lesson in template_lessons:
        old_lesson_id = lesson.get("id")
        new_lesson_id = str(uuid.uuid4())
        lesson["id"] = new_lesson_id
        lesson["chapter_id"] = chapter_id
        lesson["created_at"] = datetime.now(timezone.utc).isoformat()
        await db.lessons.insert_one(lesson)
        
        # Copy questions linked to this lesson
        lesson_questions = await db.questions.find({"lesson_id": old_lesson_id}, {"_id": 0}).to_list(500)
        for q in lesson_questions:
            q["id"] = str(uuid.uuid4())
            q["lesson_id"] = new_lesson_id
            q["chapter_id"] = chapter_id
            q["course_id"] = chapter.get("course_id")
            q["created_at"] = datetime.now(timezone.utc).isoformat()
            await db.questions.insert_one(q)
    
    # Copy questions linked to chapter (not specific lesson)
    chapter_questions = await db.questions.find({
        "chapter_id": template_id,
        "$or": [{"lesson_id": None}, {"lesson_id": {"$exists": False}}]
    }, {"_id": 0}).to_list(500)
    
    for q in chapter_questions:
        q["id"] = str(uuid.uuid4())
        q["chapter_id"] = chapter_id
        q["course_id"] = chapter.get("course_id")
        q["created_at"] = datetime.now(timezone.utc).isoformat()
        await db.questions.insert_one(q)
    
    # Remove template link
    await db.chapters.update_one(
        {"id": chapter_id},
        {"$unset": {"template_chapter_id": ""}}
    )
    
    return {
        "success": True,
        "message": "Capítulo desvinculado. El contenido ha sido copiado y ahora es independiente."
    }

# Get available template chapters (from General courses)
@admin_router.get("/template-chapters")
async def get_template_chapters(_: str = Depends(verify_admin_token)):
    """Get all chapters from General courses (available as templates)"""
    # Get General courses (no university_id)
    general_courses = await db.courses.find(
        {"$or": [{"university_id": None}, {"university_id": {"$exists": False}}]},
        {"_id": 0}
    ).to_list(100)
    
    result = []
    for course in general_courses:
        chapters = await db.chapters.find(
            {"course_id": course["id"]},
            {"_id": 0}
        ).sort("order", 1).to_list(100)
        
        # Get lesson count for each chapter
        for chapter in chapters:
            lesson_count = await db.lessons.count_documents({"chapter_id": chapter["id"]})
            question_count = await db.questions.count_documents({"chapter_id": chapter["id"]})
            chapter["lesson_count"] = lesson_count
            chapter["question_count"] = question_count
        
        result.append({
            "course": {
                "id": course["id"],
                "title": course["title"],
                "category": course.get("category")
            },
            "chapters": chapters
        })
    
    return result

# Import chapters from another course (for content splitting/reuse)
class ImportChaptersRequest(BaseModel):
    source_course_id: str
    chapter_ids: List[str]  # Chapters to import
    include_lessons: bool = True
    include_questions: bool = True

@admin_router.post("/courses/{target_course_id}/import-chapters")
async def import_chapters(
    target_course_id: str,
    request: ImportChaptersRequest,
    _: str = Depends(verify_admin_token)
):
    """
    Import chapters (with lessons and questions) from another course.
    Creates copies with new IDs, linked to the target course.
    """
    # Verify target course exists
    target_course = await db.courses.find_one({"id": target_course_id}, {"_id": 0})
    if not target_course:
        raise HTTPException(status_code=404, detail="Curso destino no encontrado")
    
    # Verify source course exists
    source_course = await db.courses.find_one({"id": request.source_course_id}, {"_id": 0})
    if not source_course:
        raise HTTPException(status_code=404, detail="Curso origen no encontrado")
    
    # Get max order in target course
    max_order_result = await db.chapters.find_one(
        {"course_id": target_course_id},
        {"order": 1},
        sort=[("order", -1)]
    )
    current_max_order = max_order_result.get("order", 0) if max_order_result else 0
    
    imported_chapters = []
    imported_lessons = []
    imported_questions = []
    
    for chapter_id in request.chapter_ids:
        # Get source chapter
        source_chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
        if not source_chapter:
            continue
        
        # Create new chapter with new ID
        current_max_order += 1
        new_chapter_id = str(uuid.uuid4())
        new_chapter = {
            "id": new_chapter_id,
            "course_id": target_course_id,
            "title": source_chapter.get("title"),
            "description": source_chapter.get("description", ""),
            "order": current_max_order,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "imported_from": {
                "course_id": request.source_course_id,
                "course_title": source_course.get("title"),
                "chapter_id": chapter_id
            }
        }
        await db.chapters.insert_one(new_chapter)
        imported_chapters.append(new_chapter_id)
        
        if request.include_lessons:
            # Get lessons from source chapter
            source_lessons = await db.lessons.find(
                {"chapter_id": chapter_id},
                {"_id": 0}
            ).sort("order", 1).to_list(100)
            
            for source_lesson in source_lessons:
                old_lesson_id = source_lesson.get("id")
                new_lesson_id = str(uuid.uuid4())
                new_lesson = {
                    "id": new_lesson_id,
                    "chapter_id": new_chapter_id,  # Link to new chapter
                    "title": source_lesson.get("title"),
                    "content": source_lesson.get("content", ""),
                    "order": source_lesson.get("order", 0),
                    "duration_minutes": source_lesson.get("duration_minutes", 30),
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                await db.lessons.insert_one(new_lesson)
                imported_lessons.append(new_lesson_id)
                
                if request.include_questions:
                    # Get questions linked to this lesson
                    source_questions = await db.questions.find(
                        {"lesson_id": old_lesson_id},
                        {"_id": 0}
                    ).to_list(500)
                    
                    for source_q in source_questions:
                        new_q_id = str(uuid.uuid4())
                        new_question = {
                            "id": new_q_id,
                            "course_id": target_course_id,
                            "chapter_id": new_chapter_id,
                            "lesson_id": new_lesson_id,
                            "topic": source_q.get("topic"),
                            "subtopic": source_q.get("subtopic"),
                            "difficulty": source_q.get("difficulty", "medio"),
                            "question_text": source_q.get("question_text"),
                            "question_type": source_q.get("question_type", "multiple_choice"),
                            "options": source_q.get("options", []),
                            "correct_answer": source_q.get("correct_answer"),
                            "explanation": source_q.get("explanation"),
                            "image_url": source_q.get("image_url"),
                            "created_at": datetime.now(timezone.utc).isoformat(),
                            "source": "imported"
                        }
                        await db.questions.insert_one(new_question)
                        imported_questions.append(new_q_id)
            
            if request.include_questions:
                # Also import questions linked to chapter (not specific lesson)
                chapter_questions = await db.questions.find(
                    {"chapter_id": chapter_id, "lesson_id": None},
                    {"_id": 0}
                ).to_list(500)
                
                for source_q in chapter_questions:
                    new_q_id = str(uuid.uuid4())
                    new_question = {
                        "id": new_q_id,
                        "course_id": target_course_id,
                        "chapter_id": new_chapter_id,
                        "lesson_id": None,
                        "topic": source_q.get("topic"),
                        "subtopic": source_q.get("subtopic"),
                        "difficulty": source_q.get("difficulty", "medio"),
                        "question_text": source_q.get("question_text"),
                        "question_type": source_q.get("question_type", "multiple_choice"),
                        "options": source_q.get("options", []),
                        "correct_answer": source_q.get("correct_answer"),
                        "explanation": source_q.get("explanation"),
                        "image_url": source_q.get("image_url"),
                        "created_at": datetime.now(timezone.utc).isoformat(),
                        "source": "imported"
                    }
                    await db.questions.insert_one(new_question)
                    imported_questions.append(new_q_id)
    
    logging.info(f"Imported {len(imported_chapters)} chapters, {len(imported_lessons)} lessons, {len(imported_questions)} questions to course {target_course_id}")
    
    return {
        "success": True,
        "message": f"Importación completada",
        "imported": {
            "chapters": len(imported_chapters),
            "lessons": len(imported_lessons),
            "questions": len(imported_questions)
        },
        "chapter_ids": imported_chapters
    }

# Lessons endpoints
@admin_router.get("/chapters/{chapter_id}/lessons")
async def get_chapter_lessons(chapter_id: str, _: str = Depends(verify_admin_token)):
    # Check if this chapter has a template (is linked)
    chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
    
    # Determine source chapter for lessons
    source_chapter_id = chapter_id
    is_linked = False
    if chapter and chapter.get("template_chapter_id"):
        source_chapter_id = chapter["template_chapter_id"]
        is_linked = True
    
    lessons = await db.lessons.find({"chapter_id": source_chapter_id}, {"_id": 0}).sort("order", 1).to_list(100)
    for lesson in lessons:
        if isinstance(lesson.get('created_at'), str):
            lesson['created_at'] = datetime.fromisoformat(lesson['created_at'])
        if is_linked:
            lesson['inherited_from_template'] = True
            lesson['read_only'] = True  # Can't edit inherited lessons
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
async def delete_lesson(lesson_id: str, admin: str = Depends(verify_admin_token)):
    lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    await _trash_put("lesson", lesson["id"], lesson.get("title", "(sin título)"),
                     payload=lesson, deleted_by=admin,
                     chapter_id=lesson.get("chapter_id"))
    await db.lessons.delete_one({"id": lesson_id})
    return {"message": "Lección movida a la papelera"}


# Upload image from file - now uses GridFS for persistent storage
@admin_router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    """Upload image to MongoDB GridFS for permanent storage"""
    from services.image_storage import save_image, get_image_url
    
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")
        
        # Read file content
        image_data = await file.read()
        
        # Validate size (max 5MB)
        if len(image_data) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Archivo muy grande. Máximo 5MB.")
        
        # Save to GridFS (persistent storage)
        image_id = await save_image(
            image_data,
            file.filename,
            file.content_type,
            metadata={"source": "admin_upload"}
        )
        
        # Return URL using the images API
        image_url = get_image_url(image_id)
        
        logging.info(f"Uploaded image {image_id} to GridFS ({len(image_data)} bytes)")
        return {"image_url": image_url, "image_id": image_id}
    except Exception as e:
        logging.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/upload-course-image")
async def upload_course_image(
    file: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    """Upload course image to MongoDB GridFS"""
    from services.image_storage import save_image, get_image_url
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")
    
    image_data = await file.read()
    
    # Validate size
    if len(image_data) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo muy grande. Máximo 5MB.")
    
    # Save to GridFS
    image_id = await save_image(
        image_data,
        file.filename,
        file.content_type,
        metadata={"source": "course_image"}
    )
    
    return {"image_url": get_image_url(image_id), "image_id": image_id}

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
    # First, check if this chapter has a template (is linked)
    chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
    
    # Use template chapter's lessons if linked
    source_chapter_id = chapter_id
    if chapter and chapter.get("template_chapter_id"):
        source_chapter_id = chapter["template_chapter_id"]
    
    lessons = await db.lessons.find({"chapter_id": source_chapter_id}, {"_id": 0}).sort("order", 1).to_list(100)
    for lesson in lessons:
        if isinstance(lesson.get('created_at'), str):
            lesson['created_at'] = datetime.fromisoformat(lesson['created_at'])
        # Mark lessons as inherited if from template
        if source_chapter_id != chapter_id:
            lesson['inherited_from_template'] = True
    return lessons

@api_router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str):
    lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    if isinstance(lesson.get('created_at'), str):
        lesson['created_at'] = datetime.fromisoformat(lesson['created_at'])
    return lesson

# ==================== APP SETTINGS ====================

@api_router.get("/settings")
async def get_app_settings():
    """Get public app settings"""
    settings = await db.app_settings.find_one({"id": "main"}, {"_id": 0})
    if not settings:
        settings = {
            "id": "main",
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    return settings

@admin_router.get("/settings")
async def get_admin_settings(_: str = Depends(verify_admin_token)):
    """Get all app settings (admin)"""
    settings = await db.app_settings.find_one({"id": "main"}, {"_id": 0})
    if not settings:
        settings = {
            "id": "main",
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.app_settings.insert_one(settings)
    return settings

class UpdateSettingsRequest(BaseModel):
    pass

@admin_router.put("/settings")
async def update_admin_settings(
    request: UpdateSettingsRequest,
    _: str = Depends(verify_admin_token)
):
    """Update app settings"""
    update_data = {k: v for k, v in request.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    await db.app_settings.update_one(
        {"id": "main"},
        {"$set": update_data},
        upsert=True
    )

    settings = await db.app_settings.find_one({"id": "main"}, {"_id": 0})
    return {"success": True, "settings": settings}

# =====================================================================
# PAPELERA (TRASH) — soft-delete con restauración
# =====================================================================
TRASH_TYPES = {"course", "chapter", "lesson", "question"}


async def _trash_put(type_: str, original_id: str, title: str, payload: Dict[str, Any],
                     deleted_by: str, children: Optional[Dict[str, List[Dict[str, Any]]]] = None,
                     course_id: Optional[str] = None, chapter_id: Optional[str] = None,
                     lesson_id: Optional[str] = None):
    children = children or {}
    children_summary = {k: len(v) for k, v in children.items()}
    doc = {
        "id": str(uuid.uuid4()),
        "type": type_,
        "original_id": original_id,
        "title": title,
        "course_id": course_id,
        "chapter_id": chapter_id,
        "lesson_id": lesson_id,
        "payload": payload,
        "children": children,
        "children_summary": children_summary,
        "deleted_at": datetime.now(timezone.utc).isoformat(),
        "deleted_by": deleted_by,
    }
    await db.trash.insert_one(doc)
    return doc


@admin_router.get("/trash")
async def list_trash(type: Optional[str] = None, _: str = Depends(verify_admin_token)):
    query: Dict[str, Any] = {}
    if type:
        if type not in TRASH_TYPES:
            raise HTTPException(status_code=400, detail=f"Tipo inválido. Permitidos: {sorted(TRASH_TYPES)}")
        query["type"] = type
    items = await db.trash.find(query, {"_id": 0, "payload": 0, "children": 0}).sort("deleted_at", -1).to_list(2000)
    return items


@admin_router.get("/trash/{trash_id}")
async def get_trash_item(trash_id: str, _: str = Depends(verify_admin_token)):
    item = await db.trash.find_one({"id": trash_id}, {"_id": 0})
    if not item:
        raise HTTPException(status_code=404, detail="Elemento no encontrado en la papelera")
    return item


@admin_router.post("/trash/{trash_id}/restore")
async def restore_trash_item(trash_id: str, _: str = Depends(verify_admin_token)):
    item = await db.trash.find_one({"id": trash_id}, {"_id": 0})
    if not item:
        raise HTTPException(status_code=404, detail="Elemento no encontrado en la papelera")

    type_ = item["type"]
    payload = item["payload"]
    children = item.get("children", {}) or {}

    if type_ == "course":
        if await db.courses.find_one({"id": payload["id"]}):
            raise HTTPException(status_code=409, detail="Ya existe un curso con ese id. Renombra o elimina el actual primero.")
        await db.courses.insert_one(payload)
        for ch in children.get("chapters", []):
            await db.chapters.delete_one({"id": ch["id"]})
            await db.chapters.insert_one(ch)
        for ls in children.get("lessons", []):
            await db.lessons.delete_one({"id": ls["id"]})
            await db.lessons.insert_one(ls)

    elif type_ == "chapter":
        course_id = payload.get("course_id")
        if course_id and not await db.courses.find_one({"id": course_id}):
            raise HTTPException(status_code=409, detail="El curso de este capítulo ya no existe. Restaura el curso primero.")
        if await db.chapters.find_one({"id": payload["id"]}):
            raise HTTPException(status_code=409, detail="Ya existe un capítulo con ese id.")
        await db.chapters.insert_one(payload)
        for ls in children.get("lessons", []):
            await db.lessons.delete_one({"id": ls["id"]})
            await db.lessons.insert_one(ls)

    elif type_ == "lesson":
        chapter_id = payload.get("chapter_id")
        if chapter_id and not await db.chapters.find_one({"id": chapter_id}):
            raise HTTPException(status_code=409, detail="El capítulo de esta lección ya no existe. Restaúralo primero.")
        if await db.lessons.find_one({"id": payload["id"]}):
            raise HTTPException(status_code=409, detail="Ya existe una lección con ese id.")
        await db.lessons.insert_one(payload)

    elif type_ == "question":
        if await db.questions.find_one({"id": payload["id"]}):
            raise HTTPException(status_code=409, detail="Ya existe una pregunta con ese id.")
        await db.questions.insert_one(payload)

    else:
        raise HTTPException(status_code=400, detail=f"Tipo desconocido: {type_}")

    await db.trash.delete_one({"id": trash_id})
    return {"message": f"{type_} restaurado exitosamente", "type": type_, "id": payload.get("id")}


@admin_router.delete("/trash/{trash_id}")
async def delete_trash_item(trash_id: str, _: str = Depends(verify_admin_token)):
    result = await db.trash.delete_one({"id": trash_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Elemento no encontrado en la papelera")
    return {"message": "Elemento eliminado definitivamente"}


@admin_router.delete("/trash")
async def empty_trash(_: str = Depends(verify_admin_token)):
    result = await db.trash.delete_many({})
    return {"message": f"Papelera vaciada", "deleted": result.deleted_count}


app.include_router(api_router)
app.include_router(admin_router)

# Include new routers for auth, payments, and user management
app.include_router(auth_routes.router)
app.include_router(payments_routes.router)
app.include_router(admin_users_routes.router)
app.include_router(admin_analytics_routes.router)
app.include_router(images_routes.router)

# Import and include new routers
from routes import library_universities as library_universities_routes
from routes import enrollments as enrollments_routes
library_universities_routes.set_db(db)
enrollments_routes.set_db(db)
app.include_router(library_universities_routes.router, prefix="/api")
app.include_router(enrollments_routes.router, prefix="/api")

# CORS configuration - allow all origins since we use Bearer tokens (not cookies)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
