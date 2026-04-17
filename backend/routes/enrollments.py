"""
Student Enrollments Router - Course enrollment system
Uses session-based authentication (same as auth routes)
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import uuid
import os

router = APIRouter()
security = HTTPBearer(auto_error=False)
db = None

def set_db(database):
    global db
    db = database

# Models
class Enrollment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    course_id: str
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EnrollRequest(BaseModel):
    course_id: str

# Auth helper - uses session tokens (same as auth routes)
async def get_current_user(
    request: Request,
    session_token: Optional[str] = Cookie(default=None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> dict:
    """Get current user from session token (cookie or Authorization header)"""
    # Try cookie first, then Authorization header
    token = session_token
    
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
        elif credentials:
            token = credentials.credentials
    
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    # Look up session in database
    session = await db.user_sessions.find_one(
        {"session_token": token},
        {"_id": 0}
    )
    
    if not session:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")
    
    # Check if session is expired
    expires_at = session.get("expires_at")
    if expires_at:
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        # Ensure expires_at is timezone-aware
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            await db.user_sessions.delete_one({"session_token": token})
            raise HTTPException(status_code=401, detail="Sesión expirada")
    
    # Get user by user_id from session
    user_id = session.get("user_id")
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    
    if not user:
        # Try with 'id' field as fallback
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    # Ensure user has 'id' field for enrollment operations
    if "id" not in user and "user_id" in user:
        user["id"] = user["user_id"]
    
    return user

async def check_trial_enrollment_limit(user_id: str) -> tuple[bool, str]:
    """
    Check if user can enroll in more courses.
    Returns (can_enroll, reason)
    """
    # Try both id and user_id fields
    user = await db.users.find_one({"id": user_id}, {"_id": 0})
    if not user:
        user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    if not user:
        return False, "Usuario no encontrado"
    
    # Check subscription status
    subscription = user.get("subscription", {})
    status = subscription.get("status")
    manual_access = subscription.get("manual_access", False)
    
    # DEBUG logging
    import logging
    logging.info(f"Enrollment check - user_id: {user_id}, status: {status}, manual_access: {manual_access}")
    
    # If active subscription OR manual access, no limit
    if status == "authorized" or manual_access == True:
        return True, "subscription_active"
    
    # Check if in trial
    trial_start = user.get("trial_start")
    if trial_start:
        from datetime import timedelta
        if isinstance(trial_start, str):
            trial_start = datetime.fromisoformat(trial_start.replace('Z', '+00:00'))
        # Ensure trial_start is timezone-aware
        if trial_start.tzinfo is None:
            trial_start = trial_start.replace(tzinfo=timezone.utc)
        
        trial_end = trial_start + timedelta(days=7)
        now = datetime.now(timezone.utc)
        
        if now < trial_end:
            # In trial - check enrollment count
            enrollment_count = await db.student_enrollments.count_documents({"student_id": user_id})
            if enrollment_count < 1:
                return True, "trial_active"
            else:
                return False, "trial_limit_reached"
    
    # No trial, no subscription - can't enroll
    return False, "no_subscription"

# ==================== ENDPOINTS ====================

@router.post("/enrollments")
async def enroll_in_course(
    request: EnrollRequest,
    user: dict = Depends(get_current_user)
):
    """Enroll current user in a course"""
    user_id = user.get("id")
    course_id = request.course_id
    
    # Check if course exists
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Check if already enrolled
    existing = await db.student_enrollments.find_one(
        {"student_id": user_id, "course_id": course_id},
        {"_id": 0}
    )
    if existing:
        raise HTTPException(status_code=400, detail="Ya estás inscrito en este curso")
    
    # Check subscription/trial limits
    subscription = user.get("subscription", {})
    has_active_subscription = (
        subscription.get("status") == "authorized" or 
        subscription.get("manual_access") == True
    )
    
    if not has_active_subscription:
        # Check trial using the helper function
        can_enroll, reason = await check_trial_enrollment_limit(user_id)
        if not can_enroll:
            if reason == "trial_limit_reached":
                raise HTTPException(
                    status_code=403, 
                    detail="Límite de inscripción alcanzado. Durante el periodo de prueba solo puedes inscribirte en 1 curso. Suscríbete para acceso ilimitado."
                )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Necesitas una suscripción activa para inscribirte en cursos."
                )
    
    # Create enrollment
    enrollment = Enrollment(
        student_id=user_id,
        course_id=course_id
    )
    
    await db.student_enrollments.insert_one(enrollment.model_dump())
    
    return {
        "success": True, 
        "message": f"Inscrito exitosamente en {course.get('title')}",
        "enrollment": enrollment.model_dump()
    }

@router.delete("/enrollments/{course_id}")
async def unenroll_from_course(
    course_id: str,
    user: dict = Depends(get_current_user)
):
    """Unenroll current user from a course"""
    user_id = user.get("id")
    
    result = await db.student_enrollments.delete_one(
        {"student_id": user_id, "course_id": course_id}
    )
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No estás inscrito en este curso")
    
    return {"success": True, "message": "Desinscrito del curso"}

@router.get("/enrollments")
async def get_my_enrollments(user: dict = Depends(get_current_user)):
    """Get all courses the current user is enrolled in"""
    user_id = user.get("id")
    
    # Get enrollments
    enrollments = await db.student_enrollments.find(
        {"student_id": user_id},
        {"_id": 0}
    ).sort("enrolled_at", -1).to_list(100)
    
    # Get course details
    course_ids = [e.get("course_id") for e in enrollments]
    courses = []
    
    if course_ids:
        courses_data = await db.courses.find(
            {"id": {"$in": course_ids}},
            {"_id": 0}
        ).to_list(100)
        
        # Add university info to courses
        for course in courses_data:
            uni_id = course.get("university_id")
            if uni_id:
                uni = await db.library_universities.find_one(
                    {"id": uni_id},
                    {"_id": 0, "name": 1, "short_name": 1, "logo_url": 1}
                )
                course["university"] = uni
            else:
                course["university"] = {"name": "General", "short_name": "GEN"}
            
            # Find enrollment date
            enrollment = next((e for e in enrollments if e.get("course_id") == course.get("id")), None)
            if enrollment:
                course["enrolled_at"] = enrollment.get("enrolled_at")
            
            courses.append(course)
    
    return courses

@router.get("/enrollments/check/{course_id}")
async def check_enrollment(
    course_id: str,
    user: dict = Depends(get_current_user)
):
    """Check if current user is enrolled in a specific course"""
    user_id = user.get("id")
    
    enrollment = await db.student_enrollments.find_one(
        {"student_id": user_id, "course_id": course_id},
        {"_id": 0}
    )
    
    return {
        "enrolled": enrollment is not None,
        "enrollment": enrollment
    }

@router.get("/enrollments/stats")
async def get_enrollment_stats(user: dict = Depends(get_current_user)):
    """Get enrollment stats for current user"""
    user_id = user.get("id")
    
    # Count enrollments
    enrollment_count = await db.student_enrollments.count_documents({"student_id": user_id})
    
    # Check subscription status
    subscription = user.get("subscription", {})
    has_active_subscription = (
        subscription.get("status") == "authorized" or 
        subscription.get("manual_access") == True
    )
    
    # Calculate limit
    if has_active_subscription:
        limit = None  # Unlimited
        can_enroll_more = True
    else:
        limit = 1  # Trial limit
        can_enroll_more = enrollment_count < 1
    
    return {
        "enrolled_count": enrollment_count,
        "limit": limit,
        "can_enroll_more": can_enroll_more,
        "has_subscription": has_active_subscription
    }
