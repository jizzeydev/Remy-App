"""
University Management Routes for Remy Platform
Handles: Universities → Courses → Evaluations → Question Banks
"""
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from jose import JWTError, jwt
import logging
import uuid
import os
import base64

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/universities", tags=["admin-universities"])

# Security
security = HTTPBearer()

# MongoDB connection
db = None


def set_db(database):
    """Set database instance from main app"""
    global db
    db = database


# Allowed admin emails
ALLOWED_ADMIN_EMAILS = [
    'seremonta.cl@gmail.com',
    'admin@seremonta.cl'
]


async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify admin JWT token"""
    try:
        token = credentials.credentials
        secret_key = os.environ.get('ADMIN_SECRET_KEY')
        admin_username = os.environ.get('ADMIN_USERNAME')
        
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        subject: str = payload.get("sub")
        token_type: str = payload.get("type", "")
        
        if subject is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
        
        if token_type == "admin_google":
            if subject.lower() not in [e.lower() for e in ALLOWED_ADMIN_EMAILS]:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
            return subject
        
        if subject != admin_username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
        return subject
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


# ==================== PYDANTIC MODELS ====================

class UniversityCreate(BaseModel):
    name: str
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    city: Optional[str] = None
    active: bool = True


class UniversityUpdate(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    city: Optional[str] = None
    active: Optional[bool] = None


class UniversityCourseCreate(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None


class EvaluationCreate(BaseModel):
    name: str  # e.g., "I1", "I2", "Midterm", "Exam"
    description: Optional[str] = None
    year: Optional[int] = None
    semester: Optional[int] = None  # 1 or 2


class EvaluationQuestionCreate(BaseModel):
    question_text: str
    question_type: str = "multiple_choice"  # multiple_choice, open
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    solution: Optional[str] = None
    difficulty: str = "medio"  # facil, medio, dificil
    topic: Optional[str] = None
    tags: Optional[List[str]] = []
    source: Optional[str] = None  # "manual", "ai_generated", "pdf_extracted"


# ==================== UNIVERSITY ENDPOINTS ====================

@router.get("")
async def list_universities(_: str = Depends(verify_admin_token)):
    """List all universities"""
    universities = await db.universities.find({}, {"_id": 0}).sort("name", 1).to_list(100)
    
    # Add stats for each university
    for uni in universities:
        courses_count = await db.university_courses.count_documents({"university_id": uni["id"]})
        uni["courses_count"] = courses_count
    
    return universities


@router.post("")
async def create_university(data: UniversityCreate, _: str = Depends(verify_admin_token)):
    """Create a new university"""
    uni_id = str(uuid.uuid4())
    
    university = {
        "id": uni_id,
        "name": data.name,
        "short_name": data.short_name or data.name[:10],
        "logo_url": data.logo_url,
        "city": data.city,
        "active": data.active,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.universities.insert_one(university)
    logger.info(f"Created university: {data.name}")
    
    return {"id": uni_id, "message": "Universidad creada exitosamente"}


@router.get("/{university_id}")
async def get_university(university_id: str, _: str = Depends(verify_admin_token)):
    """Get university details with courses"""
    university = await db.universities.find_one({"id": university_id}, {"_id": 0})
    if not university:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    
    # Get courses
    courses = await db.university_courses.find(
        {"university_id": university_id}, 
        {"_id": 0}
    ).sort("name", 1).to_list(100)
    
    # Add evaluation counts for each course
    for course in courses:
        eval_count = await db.evaluations.count_documents({"course_id": course["id"]})
        course["evaluations_count"] = eval_count
    
    university["courses"] = courses
    return university


@router.put("/{university_id}")
async def update_university(
    university_id: str, 
    data: UniversityUpdate, 
    _: str = Depends(verify_admin_token)
):
    """Update university"""
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    result = await db.universities.update_one(
        {"id": university_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    
    return {"message": "Universidad actualizada"}


@router.delete("/{university_id}")
async def delete_university(university_id: str, _: str = Depends(verify_admin_token)):
    """Delete university and all related data"""
    # Get all courses for this university
    courses = await db.university_courses.find({"university_id": university_id}).to_list(100)
    course_ids = [c["id"] for c in courses]
    
    # Delete all evaluations for these courses
    await db.evaluations.delete_many({"course_id": {"$in": course_ids}})
    
    # Delete all questions for these evaluations
    await db.evaluation_questions.delete_many({"course_id": {"$in": course_ids}})
    
    # Delete courses
    await db.university_courses.delete_many({"university_id": university_id})
    
    # Delete university
    result = await db.universities.delete_one({"id": university_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    
    return {"message": "Universidad eliminada"}


# ==================== UNIVERSITY COURSE ENDPOINTS ====================

@router.get("/{university_id}/courses")
async def list_university_courses(university_id: str, _: str = Depends(verify_admin_token)):
    """List courses for a university"""
    courses = await db.university_courses.find(
        {"university_id": university_id}, 
        {"_id": 0}
    ).sort("name", 1).to_list(100)
    
    for course in courses:
        eval_count = await db.evaluations.count_documents({"course_id": course["id"]})
        questions_count = await db.evaluation_questions.count_documents({"course_id": course["id"]})
        course["evaluations_count"] = eval_count
        course["questions_count"] = questions_count
    
    return courses


@router.post("/{university_id}/courses")
async def create_university_course(
    university_id: str, 
    data: UniversityCourseCreate, 
    _: str = Depends(verify_admin_token)
):
    """Create a course for a university"""
    # Verify university exists
    university = await db.universities.find_one({"id": university_id})
    if not university:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    
    course_id = str(uuid.uuid4())
    
    course = {
        "id": course_id,
        "university_id": university_id,
        "name": data.name,
        "code": data.code,
        "description": data.description,
        "department": data.department,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.university_courses.insert_one(course)
    logger.info(f"Created university course: {data.name} for {university['name']}")
    
    return {"id": course_id, "message": "Curso creado exitosamente"}


@router.get("/{university_id}/courses/{course_id}")
async def get_university_course(
    university_id: str, 
    course_id: str, 
    _: str = Depends(verify_admin_token)
):
    """Get course details with evaluations"""
    course = await db.university_courses.find_one(
        {"id": course_id, "university_id": university_id}, 
        {"_id": 0}
    )
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Get evaluations
    evaluations = await db.evaluations.find(
        {"course_id": course_id}, 
        {"_id": 0}
    ).sort("name", 1).to_list(100)
    
    for eval in evaluations:
        questions_count = await db.evaluation_questions.count_documents({"evaluation_id": eval["id"]})
        eval["questions_count"] = questions_count
    
    course["evaluations"] = evaluations
    return course


@router.delete("/{university_id}/courses/{course_id}")
async def delete_university_course(
    university_id: str, 
    course_id: str, 
    _: str = Depends(verify_admin_token)
):
    """Delete course and all related evaluations/questions"""
    # Delete questions
    await db.evaluation_questions.delete_many({"course_id": course_id})
    
    # Delete evaluations
    await db.evaluations.delete_many({"course_id": course_id})
    
    # Delete course
    result = await db.university_courses.delete_one({"id": course_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    return {"message": "Curso eliminado"}


# ==================== EVALUATION ENDPOINTS ====================

@router.get("/{university_id}/courses/{course_id}/evaluations")
async def list_evaluations(
    university_id: str, 
    course_id: str, 
    _: str = Depends(verify_admin_token)
):
    """List evaluations for a course"""
    evaluations = await db.evaluations.find(
        {"course_id": course_id}, 
        {"_id": 0}
    ).sort("name", 1).to_list(100)
    
    for eval in evaluations:
        questions_count = await db.evaluation_questions.count_documents({"evaluation_id": eval["id"]})
        eval["questions_count"] = questions_count
    
    return evaluations


@router.post("/{university_id}/courses/{course_id}/evaluations")
async def create_evaluation(
    university_id: str, 
    course_id: str, 
    data: EvaluationCreate, 
    _: str = Depends(verify_admin_token)
):
    """Create an evaluation (I1, I2, Midterm, etc.)"""
    # Verify course exists
    course = await db.university_courses.find_one({"id": course_id, "university_id": university_id})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    eval_id = str(uuid.uuid4())
    
    evaluation = {
        "id": eval_id,
        "university_id": university_id,
        "course_id": course_id,
        "name": data.name,
        "description": data.description,
        "year": data.year,
        "semester": data.semester,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.evaluations.insert_one(evaluation)
    logger.info(f"Created evaluation: {data.name}")
    
    return {"id": eval_id, "message": "Evaluación creada exitosamente"}


@router.delete("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}")
async def delete_evaluation(
    university_id: str, 
    course_id: str, 
    evaluation_id: str, 
    _: str = Depends(verify_admin_token)
):
    """Delete evaluation and all questions"""
    # Delete questions
    await db.evaluation_questions.delete_many({"evaluation_id": evaluation_id})
    
    # Delete evaluation
    result = await db.evaluations.delete_one({"id": evaluation_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    return {"message": "Evaluación eliminada"}


# ==================== EVALUATION QUESTION ENDPOINTS ====================

@router.get("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}/questions")
async def list_evaluation_questions(
    university_id: str, 
    course_id: str, 
    evaluation_id: str, 
    _: str = Depends(verify_admin_token)
):
    """List questions for an evaluation"""
    questions = await db.evaluation_questions.find(
        {"evaluation_id": evaluation_id}, 
        {"_id": 0}
    ).to_list(500)
    
    return questions


@router.post("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}/questions")
async def create_evaluation_question(
    university_id: str, 
    course_id: str, 
    evaluation_id: str, 
    data: EvaluationQuestionCreate, 
    _: str = Depends(verify_admin_token)
):
    """Create a question for an evaluation"""
    # Verify evaluation exists
    evaluation = await db.evaluations.find_one({"id": evaluation_id})
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    question_id = str(uuid.uuid4())
    
    question = {
        "id": question_id,
        "university_id": university_id,
        "course_id": course_id,
        "evaluation_id": evaluation_id,
        "question_text": data.question_text,
        "question_type": data.question_type,
        "options": data.options or [],
        "correct_answer": data.correct_answer,
        "solution": data.solution,
        "difficulty": data.difficulty,
        "topic": data.topic,
        "tags": data.tags or [],
        "source": data.source or "manual",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.evaluation_questions.insert_one(question)
    logger.info(f"Created evaluation question")
    
    return {"id": question_id, "message": "Pregunta creada exitosamente"}


@router.post("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}/questions/bulk")
async def create_bulk_questions(
    university_id: str, 
    course_id: str, 
    evaluation_id: str, 
    questions: List[EvaluationQuestionCreate], 
    _: str = Depends(verify_admin_token)
):
    """Create multiple questions at once"""
    # Verify evaluation exists
    evaluation = await db.evaluations.find_one({"id": evaluation_id})
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    created_ids = []
    for data in questions:
        question_id = str(uuid.uuid4())
        
        question = {
            "id": question_id,
            "university_id": university_id,
            "course_id": course_id,
            "evaluation_id": evaluation_id,
            "question_text": data.question_text,
            "question_type": data.question_type,
            "options": data.options or [],
            "correct_answer": data.correct_answer,
            "solution": data.solution,
            "difficulty": data.difficulty,
            "topic": data.topic,
            "tags": data.tags or [],
            "source": data.source or "manual",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.evaluation_questions.insert_one(question)
        created_ids.append(question_id)
    
    logger.info(f"Created {len(created_ids)} evaluation questions")
    
    return {"created_count": len(created_ids), "ids": created_ids}


@router.delete("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}/questions/{question_id}")
async def delete_evaluation_question(
    university_id: str, 
    course_id: str, 
    evaluation_id: str, 
    question_id: str, 
    _: str = Depends(verify_admin_token)
):
    """Delete a question"""
    result = await db.evaluation_questions.delete_one({"id": question_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    return {"message": "Pregunta eliminada"}


# ==================== STATS ENDPOINTS ====================

@router.get("/stats/summary")
async def get_universities_stats(_: str = Depends(verify_admin_token)):
    """Get summary stats for universities"""
    total_universities = await db.universities.count_documents({})
    total_courses = await db.university_courses.count_documents({})
    total_evaluations = await db.evaluations.count_documents({})
    total_questions = await db.evaluation_questions.count_documents({})
    
    return {
        "total_universities": total_universities,
        "total_courses": total_courses,
        "total_evaluations": total_evaluations,
        "total_questions": total_questions
    }
