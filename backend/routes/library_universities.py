"""
Library Universities Router - Universities for course categorization
Different from admin_universities (exam bank system)
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import uuid
import os
from jose import JWTError, jwt

router = APIRouter()
security = HTTPBearer()
db = None

SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY')
ALGORITHM = "HS256"

def set_db(database):
    global db
    db = database

# Models
class LibraryUniversity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    short_name: str  # Sigla (PUC, UChile, etc.)
    logo_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CreateUniversityRequest(BaseModel):
    name: str
    short_name: str
    logo_url: Optional[str] = None

class UpdateUniversityRequest(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = None

# Auth helper
async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type", "admin")
        
        if token_type == "google_admin":
            email = payload.get("email")
            if email == "seremonta.cl@gmail.com":
                return email
        
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# ==================== ADMIN ENDPOINTS ====================

@router.get("/admin/library-universities")
async def list_library_universities(_: str = Depends(verify_admin_token)):
    """Get all library universities (for course categorization)"""
    universities = await db.library_universities.find(
        {}, {"_id": 0}
    ).sort("name", 1).to_list(100)
    return universities

@router.post("/admin/library-universities")
async def create_library_university(
    request: CreateUniversityRequest,
    _: str = Depends(verify_admin_token)
):
    """Create a new library university"""
    # Check if short_name already exists
    existing = await db.library_universities.find_one(
        {"short_name": request.short_name.upper()},
        {"_id": 0}
    )
    if existing:
        raise HTTPException(status_code=400, detail=f"Ya existe una universidad con sigla {request.short_name}")
    
    university = LibraryUniversity(
        name=request.name,
        short_name=request.short_name.upper(),
        logo_url=request.logo_url
    )
    
    await db.library_universities.insert_one(university.model_dump())
    
    return {"success": True, "university": university.model_dump()}

@router.put("/admin/library-universities/{university_id}")
async def update_library_university(
    university_id: str,
    request: UpdateUniversityRequest,
    _: str = Depends(verify_admin_token)
):
    """Update a library university"""
    university = await db.library_universities.find_one(
        {"id": university_id},
        {"_id": 0}
    )
    if not university:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    
    update_data = {k: v for k, v in request.model_dump().items() if v is not None}
    
    if "short_name" in update_data:
        update_data["short_name"] = update_data["short_name"].upper()
        # Check if new short_name conflicts
        existing = await db.library_universities.find_one(
            {"short_name": update_data["short_name"], "id": {"$ne": university_id}},
            {"_id": 0}
        )
        if existing:
            raise HTTPException(status_code=400, detail=f"Ya existe una universidad con sigla {update_data['short_name']}")
    
    if update_data:
        await db.library_universities.update_one(
            {"id": university_id},
            {"$set": update_data}
        )
    
    updated = await db.library_universities.find_one({"id": university_id}, {"_id": 0})
    return {"success": True, "university": updated}

@router.delete("/admin/library-universities/{university_id}")
async def delete_library_university(
    university_id: str,
    _: str = Depends(verify_admin_token)
):
    """Delete a library university (only if no courses use it)"""
    # Check if any courses use this university
    course_count = await db.courses.count_documents({"university_id": university_id})
    if course_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"No se puede eliminar: {course_count} curso(s) usan esta universidad. Cambia los cursos primero."
        )
    
    result = await db.library_universities.delete_one({"id": university_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    
    return {"success": True, "message": "Universidad eliminada"}

# ==================== PUBLIC ENDPOINTS ====================

@router.get("/library-universities")
async def get_active_library_universities():
    """Get all active library universities (public endpoint for filters)"""
    universities = await db.library_universities.find(
        {"is_active": True}, 
        {"_id": 0}
    ).sort("name", 1).to_list(100)
    return universities
