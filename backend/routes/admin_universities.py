"""
University Management Routes for Remy Platform
Handles: Universities → Courses → Evaluations → Question Banks
Supports: File uploads, AI generation from prompt/PDF, Markdown/LaTeX
"""
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from jose import JWTError, jwt
import logging
import uuid
import os
import aiofiles
from pathlib import Path
import PyPDF2
import io

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/universities", tags=["admin-universities"])

# Security
security = HTTPBearer()

# MongoDB connection
db = None

# Upload directory for university logos
UPLOADS_DIR = Path(__file__).parent.parent / 'uploads' / 'universities'
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


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
    city: Optional[str] = None
    active: bool = True


class UniversityUpdate(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    city: Optional[str] = None
    active: Optional[bool] = None


class UniversityCourseCreate(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None


class UniversityCourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None


class EvaluationCreate(BaseModel):
    name: str  # e.g., "I1", "I2", "Midterm", "Exam"
    description: Optional[str] = None


class EvaluationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class EvaluationQuestionCreate(BaseModel):
    """Question with Markdown/LaTeX support"""
    question_content: str  # Supports Markdown and LaTeX
    solution_content: Optional[str] = None  # Supports Markdown and LaTeX
    question_type: str = "multiple_choice"  # multiple_choice, open
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    difficulty: str = "medio"  # facil, medio, dificil
    topic: Optional[str] = None
    tags: Optional[List[str]] = []
    image_url: Optional[str] = None  # Optional image
    source: Optional[str] = None  # "manual", "ai_generated", "pdf_extracted"


class AIGenerateRequest(BaseModel):
    """Request for AI question generation"""
    generation_type: str  # "prompt" or "pdf"
    prompt: Optional[str] = None  # For prompt-based generation
    pdf_content: Optional[str] = None  # Extracted PDF text
    num_questions: int = 5
    difficulty: str = "medio"
    topic: Optional[str] = None


# ==================== OPENAI INTEGRATION ====================

async def get_openai_client():
    """Get OpenAI client using environment variable"""
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        # Try to use Emergent LLM key as fallback
        emergent_key = os.environ.get('EMERGENT_LLM_KEY')
        if emergent_key:
            try:
                from emergentintegrations.llm.chat import LlmChat, UserMessage
                return {"type": "emergent", "key": emergent_key}
            except ImportError:
                pass
        raise HTTPException(
            status_code=500, 
            detail="OPENAI_API_KEY no configurada. Configure la variable de entorno."
        )
    
    return {"type": "openai", "key": api_key}


async def generate_questions_with_ai(
    prompt: str, 
    num_questions: int = 5, 
    difficulty: str = "medio",
    topic: Optional[str] = None
) -> List[dict]:
    """Generate questions using OpenAI or Emergent LLM"""
    
    try:
        # Try Emergent integration first (already configured)
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        
        system_message = """Eres un experto en crear preguntas de examen para matemáticas universitarias.

FORMATO DE RESPUESTA - Devuelve SOLO un JSON array con este formato exacto:
[
  {
    "question_content": "Pregunta en Markdown con LaTeX: $\\\\frac{d}{dx}(x^2) = ?$",
    "options": ["$2x$", "$x^2$", "$2$", "$x$"],
    "correct_answer": "A",
    "solution_content": "Explicación paso a paso con LaTeX...",
    "difficulty": "medio",
    "topic": "Derivadas"
  }
]

REGLAS:
- Usa LaTeX para fórmulas: $formula$ para inline, $$formula$$ para bloque
- Cada pregunta debe tener 4 opciones (A, B, C, D)
- La solución debe explicar el procedimiento completo
- Varía la dificultad según se indique
- NO incluyas texto antes o después del JSON"""

        user_prompt = f"""Genera {num_questions} preguntas de examen.

Dificultad: {difficulty}
{f'Tema: {topic}' if topic else ''}

Instrucciones/Contenido:
{prompt}

Recuerda: Devuelve SOLO el JSON array, sin texto adicional."""

        session_id = str(uuid.uuid4())
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=session_id,
            system_message=system_message
        )
        
        response = await chat.send_message(UserMessage(text=user_prompt))
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        # Parse JSON response
        import json
        # Clean response - find JSON array
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            questions = json.loads(json_str)
            return questions
        else:
            logger.error(f"Could not find JSON in response: {response_text[:200]}")
            return []
            
    except Exception as e:
        logger.error(f"Error generating questions with AI: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al generar preguntas: {str(e)}")


async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting PDF text: {str(e)}")
        raise HTTPException(status_code=400, detail="Error al procesar el PDF")


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
async def create_university(
    name: str = Form(...),
    short_name: str = Form(None),
    city: str = Form(None),
    logo: UploadFile = File(None),
    _: str = Depends(verify_admin_token)
):
    """Create a new university with optional logo upload"""
    uni_id = str(uuid.uuid4())
    logo_path = None
    
    # Handle logo upload
    if logo and logo.filename:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
        if logo.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Tipo de archivo no permitido. Use JPG, PNG, WebP o GIF.")
        
        # Save file
        ext = logo.filename.split('.')[-1] if '.' in logo.filename else 'png'
        filename = f"{uni_id}.{ext}"
        file_path = UPLOADS_DIR / filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await logo.read()
            await f.write(content)
        
        logo_path = f"/api/admin/universities/logo/{filename}"
    
    university = {
        "id": uni_id,
        "name": name,
        "short_name": short_name or name[:10],
        "logo_path": logo_path,
        "city": city,
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.universities.insert_one(university)
    logger.info(f"Created university: {name}")
    
    return {"id": uni_id, "message": "Universidad creada exitosamente", "logo_path": logo_path}


@router.get("/logo/{filename}")
async def get_university_logo(filename: str):
    """Serve university logo file"""
    file_path = UPLOADS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Logo no encontrado")
    return FileResponse(file_path)


@router.post("/{university_id}/upload-logo")
async def upload_university_logo(
    university_id: str,
    logo: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    """Upload or update university logo"""
    # Verify university exists
    university = await db.universities.find_one({"id": university_id})
    if not university:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if logo.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido. Use JPG, PNG, WebP o GIF.")
    
    # Delete old logo if exists
    if university.get("logo_path"):
        old_filename = university["logo_path"].split('/')[-1]
        old_path = UPLOADS_DIR / old_filename
        if old_path.exists():
            old_path.unlink()
    
    # Save new file
    ext = logo.filename.split('.')[-1] if '.' in logo.filename else 'png'
    filename = f"{university_id}.{ext}"
    file_path = UPLOADS_DIR / filename
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await logo.read()
        await f.write(content)
    
    logo_path = f"/api/admin/universities/logo/{filename}"
    
    # Update database
    await db.universities.update_one(
        {"id": university_id},
        {"$set": {"logo_path": logo_path, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Logo actualizado", "logo_path": logo_path}


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
        questions_count = await db.evaluation_questions.count_documents({"course_id": course["id"]})
        course["evaluations_count"] = eval_count
        course["questions_count"] = questions_count
    
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
    
    # Delete university logo if exists
    university = await db.universities.find_one({"id": university_id})
    if university and university.get("logo_path"):
        filename = university["logo_path"].split('/')[-1]
        file_path = UPLOADS_DIR / filename
        if file_path.exists():
            file_path.unlink()
    
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


@router.put("/{university_id}/courses/{course_id}")
async def update_university_course(
    university_id: str, 
    course_id: str, 
    data: UniversityCourseUpdate, 
    _: str = Depends(verify_admin_token)
):
    """Update a course"""
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    result = await db.university_courses.update_one(
        {"id": course_id, "university_id": university_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    return {"message": "Curso actualizado"}


@router.delete("/{university_id}/courses/{course_id}")
async def delete_university_course(
    university_id: str, 
    course_id: str, 
    _: str = Depends(verify_admin_token)
):
    """Delete course and all related evaluations/questions"""
    # Get all evaluations for this course
    evaluations = await db.evaluations.find({"course_id": course_id}).to_list(100)
    evaluation_ids = [e["id"] for e in evaluations]
    
    # Delete questions linked to these evaluations
    await db.evaluation_questions.delete_many({"evaluation_id": {"$in": evaluation_ids}})
    
    # Delete evaluations
    await db.evaluations.delete_many({"course_id": course_id})
    
    # Delete course
    result = await db.university_courses.delete_one({"id": course_id, "university_id": university_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    logger.info(f"Deleted course {course_id} with {len(evaluations)} evaluations")
    return {"message": "Curso eliminado junto con sus evaluaciones y preguntas"}


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
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.evaluations.insert_one(evaluation)
    logger.info(f"Created evaluation: {data.name}")
    
    return {"id": eval_id, "message": "Evaluación creada exitosamente"}


@router.put("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}")
async def update_evaluation(
    university_id: str, 
    course_id: str, 
    evaluation_id: str, 
    data: EvaluationUpdate, 
    _: str = Depends(verify_admin_token)
):
    """Update an evaluation"""
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    result = await db.evaluations.update_one(
        {"id": evaluation_id, "course_id": course_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    return {"message": "Evaluación actualizada"}


@router.delete("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}")
async def delete_evaluation(
    university_id: str, 
    course_id: str, 
    evaluation_id: str, 
    _: str = Depends(verify_admin_token)
):
    """Delete evaluation and all questions"""
    # Delete questions
    deleted_questions = await db.evaluation_questions.delete_many({"evaluation_id": evaluation_id})
    
    # Delete evaluation
    result = await db.evaluations.delete_one({"id": evaluation_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    logger.info(f"Deleted evaluation {evaluation_id} with {deleted_questions.deleted_count} questions")
    return {"message": f"Evaluación eliminada con {deleted_questions.deleted_count} preguntas"}


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
    """Create a question for an evaluation (supports Markdown/LaTeX)"""
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
        "question_content": data.question_content,  # Markdown/LaTeX
        "solution_content": data.solution_content,  # Markdown/LaTeX
        "question_type": data.question_type,
        "options": data.options or [],
        "correct_answer": data.correct_answer,
        "difficulty": data.difficulty,
        "topic": data.topic,
        "tags": data.tags or [],
        "image_url": data.image_url,
        "source": data.source or "manual",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.evaluation_questions.insert_one(question)
    logger.info(f"Created evaluation question")
    
    return {"id": question_id, "message": "Pregunta creada exitosamente"}


@router.put("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}/questions/{question_id}")
async def update_evaluation_question(
    university_id: str, 
    course_id: str, 
    evaluation_id: str,
    question_id: str,
    data: EvaluationQuestionCreate, 
    _: str = Depends(verify_admin_token)
):
    """Update a question"""
    update_data = data.model_dump()
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    result = await db.evaluation_questions.update_one(
        {"id": question_id, "evaluation_id": evaluation_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    return {"message": "Pregunta actualizada"}


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
            "question_content": data.question_content,
            "solution_content": data.solution_content,
            "question_type": data.question_type,
            "options": data.options or [],
            "correct_answer": data.correct_answer,
            "difficulty": data.difficulty,
            "topic": data.topic,
            "tags": data.tags or [],
            "image_url": data.image_url,
            "source": data.source or "ai_generated",
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


# ==================== AI GENERATION ENDPOINTS ====================

@router.post("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}/generate")
async def generate_questions_ai(
    university_id: str, 
    course_id: str, 
    evaluation_id: str,
    data: AIGenerateRequest,
    _: str = Depends(verify_admin_token)
):
    """Generate questions using AI from prompt or PDF content"""
    # Verify evaluation exists
    evaluation = await db.evaluations.find_one({"id": evaluation_id})
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Get course info for context
    course = await db.university_courses.find_one({"id": course_id})
    university = await db.universities.find_one({"id": university_id})
    
    # Build prompt based on generation type
    if data.generation_type == "prompt":
        if not data.prompt:
            raise HTTPException(status_code=400, detail="El prompt es requerido")
        generation_prompt = data.prompt
    elif data.generation_type == "pdf":
        if not data.pdf_content:
            raise HTTPException(status_code=400, detail="El contenido del PDF es requerido")
        generation_prompt = f"""Analiza este contenido de un examen anterior y genera {data.num_questions} preguntas similares:

CONTENIDO DEL EXAMEN:
{data.pdf_content}

Genera preguntas del mismo estilo, nivel de dificultad y temática."""
    else:
        raise HTTPException(status_code=400, detail="Tipo de generación inválido")
    
    # Add context
    context = f"""
Universidad: {university['name'] if university else 'N/A'}
Curso: {course['name'] if course else 'N/A'}
Evaluación: {evaluation['name']}
"""
    
    full_prompt = f"{context}\n{generation_prompt}"
    
    # Generate questions
    questions = await generate_questions_with_ai(
        prompt=full_prompt,
        num_questions=data.num_questions,
        difficulty=data.difficulty,
        topic=data.topic
    )
    
    if not questions:
        raise HTTPException(status_code=500, detail="No se pudieron generar preguntas")
    
    # Save questions to database
    created_ids = []
    for q in questions:
        question_id = str(uuid.uuid4())
        
        question = {
            "id": question_id,
            "university_id": university_id,
            "course_id": course_id,
            "evaluation_id": evaluation_id,
            "question_content": q.get("question_content", q.get("question_text", "")),
            "solution_content": q.get("solution_content", q.get("explanation", "")),
            "question_type": "multiple_choice",
            "options": q.get("options", []),
            "correct_answer": q.get("correct_answer"),
            "difficulty": q.get("difficulty", data.difficulty),
            "topic": q.get("topic", data.topic),
            "tags": q.get("tags", []),
            "image_url": None,
            "source": f"ai_generated_{data.generation_type}",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.evaluation_questions.insert_one(question)
        created_ids.append(question_id)
    
    logger.info(f"AI generated {len(created_ids)} questions for evaluation {evaluation_id}")
    
    return {
        "success": True,
        "created_count": len(created_ids),
        "questions": questions,
        "ids": created_ids
    }


@router.post("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}/upload-pdf")
async def upload_pdf_for_extraction(
    university_id: str, 
    course_id: str, 
    evaluation_id: str,
    pdf_file: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    """Upload a PDF and extract text for question generation"""
    # Validate file type
    if pdf_file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Read and extract text
    content = await pdf_file.read()
    text = await extract_text_from_pdf(content)
    
    if not text or len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF. Asegúrese de que el PDF tenga texto seleccionable.")
    
    return {
        "success": True,
        "filename": pdf_file.filename,
        "extracted_text": text,
        "text_length": len(text)
    }


# ==================== QUESTION IMAGE UPLOAD ====================

@router.post("/{university_id}/courses/{course_id}/evaluations/{evaluation_id}/questions/upload-image")
async def upload_question_image(
    university_id: str, 
    course_id: str, 
    evaluation_id: str,
    image: UploadFile = File(...),
    _: str = Depends(verify_admin_token)
):
    """Upload an image for a question"""
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if image.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo de imagen no permitido. Use JPG, PNG, WebP o GIF.")
    
    # Create questions images directory
    questions_dir = UPLOADS_DIR.parent / 'questions'
    questions_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    image_id = str(uuid.uuid4())
    ext = image.filename.split('.')[-1] if '.' in image.filename else 'png'
    filename = f"{image_id}.{ext}"
    file_path = questions_dir / filename
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await image.read()
        await f.write(content)
    
    image_url = f"/api/admin/universities/question-image/{filename}"
    
    return {"success": True, "image_url": image_url}


@router.get("/question-image/{filename}")
async def get_question_image(filename: str):
    """Serve question image file"""
    file_path = UPLOADS_DIR.parent / 'questions' / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return FileResponse(file_path)


# ==================== STATS ENDPOINTS ====================

@router.get("/stats/summary")
async def get_universities_stats(_: str = Depends(verify_admin_token)):
    """Get summary stats for universities"""
    total_universities = await db.universities.count_documents({})
    total_courses = await db.university_courses.count_documents({})
    total_evaluations = await db.evaluations.count_documents({})
    total_questions = await db.evaluation_questions.count_documents({})
    
    # Questions by source
    ai_questions = await db.evaluation_questions.count_documents({"source": {"$regex": "ai_generated"}})
    pdf_questions = await db.evaluation_questions.count_documents({"source": "ai_generated_pdf"})
    manual_questions = await db.evaluation_questions.count_documents({"source": "manual"})
    
    return {
        "total_universities": total_universities,
        "total_courses": total_courses,
        "total_evaluations": total_evaluations,
        "total_questions": total_questions,
        "questions_by_source": {
            "ai_generated": ai_questions,
            "pdf_extracted": pdf_questions,
            "manual": manual_questions
        }
    }
