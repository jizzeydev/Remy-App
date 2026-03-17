"""
Student-facing University Routes for Remy Platform
Public/authenticated endpoints for students to browse universities and generate simulations
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional, List
from jose import JWTError, jwt
import logging
import uuid
import os
import random

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/universities", tags=["student-universities"])

# Security (optional - for authenticated features)
security = HTTPBearer(auto_error=False)

# MongoDB connection
db = None

def set_db(database):
    """Set database instance from main app"""
    global db
    db = database


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        secret_key = os.environ.get('ADMIN_SECRET_KEY')
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id:
            user = await db.users.find_one({"id": user_id}, {"_id": 0})
            return user
        return None
    except JWTError:
        return None


# ==================== PUBLIC ENDPOINTS ====================

@router.get("")
async def list_universities_public():
    """List all active universities (public)"""
    universities = await db.universities.find(
        {"active": True}, 
        {"_id": 0, "id": 1, "name": 1, "short_name": 1}
    ).sort("name", 1).to_list(100)
    
    # Add courses count for each
    for uni in universities:
        courses_count = await db.university_courses.count_documents({"university_id": uni["id"]})
        uni["courses_count"] = courses_count
    
    return universities


@router.get("/{university_id}")
async def get_university_public(university_id: str):
    """Get university with its courses (public)"""
    university = await db.universities.find_one(
        {"id": university_id, "active": True}, 
        {"_id": 0, "id": 1, "name": 1, "short_name": 1}
    )
    
    if not university:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    
    # Get courses
    courses = await db.university_courses.find(
        {"university_id": university_id}, 
        {"_id": 0, "id": 1, "name": 1, "code": 1, "description": 1}
    ).sort("name", 1).to_list(100)
    
    # Add evaluation counts
    for course in courses:
        eval_count = await db.evaluations.count_documents({"course_id": course["id"]})
        course["evaluations_count"] = eval_count
    
    university["courses"] = courses
    return university


@router.get("/{university_id}/courses/{course_id}")
async def get_course_public(university_id: str, course_id: str):
    """Get course with its evaluations (public)"""
    course = await db.university_courses.find_one(
        {"id": course_id, "university_id": university_id}, 
        {"_id": 0, "id": 1, "name": 1, "code": 1, "description": 1}
    )
    
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Get evaluations with question counts
    evaluations = await db.evaluations.find(
        {"course_id": course_id}, 
        {"_id": 0, "id": 1, "name": 1, "description": 1}
    ).sort("name", 1).to_list(100)
    
    for eval in evaluations:
        questions_count = await db.evaluation_questions.count_documents({"evaluation_id": eval["id"]})
        eval["questions_count"] = questions_count
    
    course["evaluations"] = evaluations
    return course


# ==================== SIMULATION ENDPOINTS ====================

class SimulationRequest(BaseModel):
    evaluation_id: str
    num_questions: int = 10
    difficulty: Optional[str] = None  # facil, medio, dificil, or None for mixed


@router.post("/{university_id}/courses/{course_id}/simulation")
async def generate_simulation(
    university_id: str,
    course_id: str,
    request: SimulationRequest,
    user = Depends(get_current_user)
):
    """Generate a simulation from the evaluation's question bank"""
    
    # Verify evaluation exists
    evaluation = await db.evaluations.find_one({
        "id": request.evaluation_id,
        "course_id": course_id
    })
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Build query for questions
    query = {"evaluation_id": request.evaluation_id}
    if request.difficulty:
        query["difficulty"] = request.difficulty
    
    # Get all available questions
    all_questions = await db.evaluation_questions.find(
        query, 
        {"_id": 0}
    ).to_list(500)
    
    if len(all_questions) == 0:
        raise HTTPException(
            status_code=400, 
            detail="No hay preguntas disponibles para esta evaluación"
        )
    
    # Select random questions
    num_to_select = min(request.num_questions, len(all_questions))
    selected_questions = random.sample(all_questions, num_to_select)
    
    # Shuffle options for each question (to prevent memorization)
    for q in selected_questions:
        if q.get("options") and len(q["options"]) > 1:
            # Store original correct answer
            correct_idx = ord(q.get("correct_answer", "A")) - ord("A")
            if 0 <= correct_idx < len(q["options"]):
                correct_option = q["options"][correct_idx]
                # Shuffle
                random.shuffle(q["options"])
                # Find new index of correct answer
                try:
                    new_idx = q["options"].index(correct_option)
                    q["correct_answer"] = chr(ord("A") + new_idx)
                except ValueError:
                    pass
    
    # Get course and university info
    course = await db.university_courses.find_one({"id": course_id}, {"_id": 0, "name": 1, "code": 1})
    university = await db.universities.find_one({"id": university_id}, {"_id": 0, "name": 1, "short_name": 1})
    
    # Create simulation record
    simulation_id = str(uuid.uuid4())
    simulation = {
        "id": simulation_id,
        "user_id": user["id"] if user else None,
        "university_id": university_id,
        "university_name": university["name"] if university else None,
        "course_id": course_id,
        "course_name": course["name"] if course else None,
        "evaluation_id": request.evaluation_id,
        "evaluation_name": evaluation["name"],
        "questions": selected_questions,
        "total_questions": len(selected_questions),
        "difficulty": request.difficulty,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed": False,
        "score": None
    }
    
    # Save simulation to database
    await db.university_simulations.insert_one(simulation)
    
    # Prepare response (without correct answers for the quiz)
    quiz_questions = []
    for q in selected_questions:
        quiz_questions.append({
            "id": q["id"],
            "question_content": q.get("question_content", q.get("question_text", "")),
            "options": q.get("options", []),
            "difficulty": q.get("difficulty", "medio"),
            "topic": q.get("topic"),
            # Don't include correct_answer or solution in response
        })
    
    logger.info(f"Generated simulation {simulation_id} with {len(quiz_questions)} questions")
    
    return {
        "simulation_id": simulation_id,
        "university": university["name"] if university else None,
        "course": course["name"] if course else None,
        "evaluation": evaluation["name"],
        "total_questions": len(quiz_questions),
        "questions": quiz_questions
    }


class SubmitAnswerRequest(BaseModel):
    answers: dict  # {question_id: "A", "B", "C", or "D"}


@router.post("/simulation/{simulation_id}/submit")
async def submit_simulation(
    simulation_id: str,
    request: SubmitAnswerRequest,
    user = Depends(get_current_user)
):
    """Submit answers for a simulation and get results"""
    
    # Get simulation
    simulation = await db.university_simulations.find_one({"id": simulation_id}, {"_id": 0})
    
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    
    if simulation.get("completed"):
        raise HTTPException(status_code=400, detail="Esta simulación ya fue completada")
    
    # Calculate score
    correct_count = 0
    results = []
    
    for question in simulation["questions"]:
        q_id = question["id"]
        user_answer = request.answers.get(q_id, "")
        correct_answer = question.get("correct_answer", "")
        is_correct = user_answer.upper() == correct_answer.upper()
        
        if is_correct:
            correct_count += 1
        
        results.append({
            "question_id": q_id,
            "question_content": question.get("question_content", question.get("question_text", "")),
            "options": question.get("options", []),
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "solution_content": question.get("solution_content", question.get("solution", "")),
            "topic": question.get("topic")
        })
    
    total = len(simulation["questions"])
    score = round((correct_count / total) * 100, 1) if total > 0 else 0
    
    # Update simulation as completed
    await db.university_simulations.update_one(
        {"id": simulation_id},
        {
            "$set": {
                "completed": True,
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "answers": request.answers,
                "score": score,
                "correct_count": correct_count
            }
        }
    )
    
    # If user is authenticated, update their stats
    if user:
        await db.users.update_one(
            {"id": user["id"]},
            {
                "$inc": {"university_simulations_completed": 1},
                "$set": {"last_simulation_at": datetime.now(timezone.utc).isoformat()}
            }
        )
    
    logger.info(f"Simulation {simulation_id} completed: {correct_count}/{total} ({score}%)")
    
    return {
        "simulation_id": simulation_id,
        "score": score,
        "correct_count": correct_count,
        "total_questions": total,
        "results": results,
        "university": simulation.get("university_name"),
        "course": simulation.get("course_name"),
        "evaluation": simulation.get("evaluation_name")
    }


@router.get("/simulation/{simulation_id}")
async def get_simulation_result(simulation_id: str, user = Depends(get_current_user)):
    """Get simulation result (if completed)"""
    
    simulation = await db.university_simulations.find_one({"id": simulation_id}, {"_id": 0})
    
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    
    if not simulation.get("completed"):
        # Return only basic info if not completed
        return {
            "simulation_id": simulation_id,
            "completed": False,
            "total_questions": simulation.get("total_questions", 0)
        }
    
    # Return full results
    return {
        "simulation_id": simulation_id,
        "completed": True,
        "score": simulation.get("score"),
        "correct_count": simulation.get("correct_count"),
        "total_questions": simulation.get("total_questions"),
        "university": simulation.get("university_name"),
        "course": simulation.get("course_name"),
        "evaluation": simulation.get("evaluation_name"),
        "completed_at": simulation.get("completed_at")
    }
