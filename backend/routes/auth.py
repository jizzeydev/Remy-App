"""Authentication routes for Remy platform - Google OAuth Only"""
from fastapi import APIRouter, HTTPException, status, Response, Request, Cookie
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
from typing import Optional
import httpx
import uuid
import os
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Session configuration
SESSION_EXPIRE_DAYS = 30  # Extended to 30 days for better UX

# MongoDB connection (will be set from main app)
db = None

# Email service (will be imported after db is set)
email_service = None

def set_db(database):
    """Set database instance from main app"""
    global db, email_service
    db = database
    # Import email service here to avoid circular imports
    from services.email_service import (
        notify_new_user_registration, 
        send_welcome_email
    )
    global notify_new_user, send_welcome
    notify_new_user = notify_new_user_registration
    send_welcome = send_welcome_email


# Request/Response models
class GoogleSessionRequest(BaseModel):
    session_id: str


class UserResponse(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    subscription_status: str = "inactive"
    subscription_type: Optional[str] = None
    subscription_plan: Optional[str] = None
    subscription_end: Optional[str] = None


# Helper functions
def generate_user_id() -> str:
    return f"user_{uuid.uuid4().hex[:12]}"


def generate_session_token() -> str:
    return f"sess_{uuid.uuid4().hex}"


async def get_user_by_email(email: str) -> Optional[dict]:
    """Get user by email, excluding MongoDB _id"""
    return await db.users.find_one({"email": email.lower()}, {"_id": 0})


async def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get user by user_id, excluding MongoDB _id"""
    return await db.users.find_one({"user_id": user_id}, {"_id": 0})


async def create_session(user_id: str) -> tuple[str, datetime]:
    """Create a new session for user"""
    session_token = generate_session_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=SESSION_EXPIRE_DAYS)
    
    await db.user_sessions.insert_one({
        "session_id": f"session_{uuid.uuid4().hex[:12]}",
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires_at.isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    return session_token, expires_at


async def get_session(session_token: str) -> Optional[dict]:
    """Get session by token"""
    session = await db.user_sessions.find_one(
        {"session_token": session_token},
        {"_id": 0}
    )
    
    if not session:
        return None
    
    # Check expiry
    expires_at = session.get("expires_at")
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at < datetime.now(timezone.utc):
        # Session expired, delete it
        await db.user_sessions.delete_one({"session_token": session_token})
        return None
    
    return session


def set_session_cookie(response: Response, session_token: str, expires_at: datetime):
    """Set session cookie on response"""
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        expires=expires_at
    )


def user_to_response(user: dict) -> dict:
    """Convert user document to response format"""
    sub_end = user.get("subscription_end")
    if sub_end and isinstance(sub_end, datetime):
        sub_end = sub_end.isoformat()
    
    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "name": user["name"],
        "picture": user.get("picture"),
        "subscription_status": user.get("subscription_status", "inactive"),
        "subscription_type": user.get("subscription_type"),
        "subscription_plan": user.get("subscription_plan"),
        "subscription_end": sub_end
    }


# ==================== GOOGLE OAUTH (Emergent Auth) ====================

@router.post("/google/session")
async def process_google_session(request: Request, response: Response):
    """
    Process Google OAuth session_id from Emergent Auth
    Frontend sends session_id after redirect from auth.emergentagent.com
    """
    body = await request.json()
    session_id = body.get("session_id")
    
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id requerido"
        )
    
    # Exchange session_id for user data from Emergent Auth
    try:
        async with httpx.AsyncClient() as client:
            auth_response = await client.get(
                "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
                headers={"X-Session-ID": session_id},
                timeout=10.0
            )
            
            if auth_response.status_code != 200:
                logger.error(f"Emergent Auth error: {auth_response.text}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Error de autenticación con Google"
                )
            
            auth_data = auth_response.json()
    
    except httpx.RequestError as e:
        logger.error(f"Error connecting to Emergent Auth: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio de autenticación no disponible"
        )
    
    email = auth_data.get("email", "").lower()
    name = auth_data.get("name", "Usuario")
    picture = auth_data.get("picture")
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo obtener el email de Google"
        )
    
    # Check if user exists
    user = await get_user_by_email(email)
    
    if user:
        # Update existing user if needed
        update_data = {}
        if user.get("auth_provider") != "google":
            update_data["auth_provider"] = "google"
        if picture and user.get("picture") != picture:
            update_data["picture"] = picture
        if name and user.get("name") != name:
            update_data["name"] = name
        
        if update_data:
            await db.users.update_one(
                {"user_id": user["user_id"]},
                {"$set": update_data}
            )
            user.update(update_data)
        
        user_id = user["user_id"]
        logger.info(f"Google user logged in: {email}")
    else:
        # Create new user
        user_id = generate_user_id()
        user = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": picture,
            "auth_provider": "google",
            "password_hash": None,
            "subscription_status": "inactive",
            "subscription_type": None,
            "subscription_plan": None,
            "subscription_id": None,
            "subscription_start": None,
            "subscription_end": None,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(user)
        logger.info(f"New Google user registered: {email}")
        
        # Send email notifications (non-blocking)
        try:
            asyncio.create_task(notify_new_user(email, name))
            asyncio.create_task(send_welcome(email, name))
        except Exception as e:
            logger.error(f"Failed to send registration emails: {e}")
    
    # Create our own session
    session_token, expires_at = await create_session(user_id)
    set_session_cookie(response, session_token, expires_at)
    
    return {
        "session_token": session_token,
        "user": user_to_response(user)
    }


# ==================== SESSION MANAGEMENT ====================

@router.get("/me")
async def get_current_user(
    request: Request,
    session_token: Optional[str] = Cookie(default=None)
):
    """Get current authenticated user"""
    # Try cookie first, then Authorization header
    token = session_token
    
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
    
    session = await get_session(token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada"
        )
    
    user = await get_user_by_id(session["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user_to_response(user)


@router.post("/logout")
async def logout(
    response: Response,
    request: Request,
    session_token: Optional[str] = Cookie(default=None)
):
    """Logout current user"""
    token = session_token
    
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if token:
        await db.user_sessions.delete_one({"session_token": token})
    
    # Clear cookie
    response.delete_cookie(
        key="session_token",
        path="/",
        secure=True,
        samesite="none"
    )
    
    return {"message": "Sesión cerrada exitosamente"}


# ==================== AUTH DEPENDENCY ====================

async def get_current_user_dependency(
    request: Request,
    session_token: Optional[str] = Cookie(default=None)
) -> dict:
    """Dependency to get current authenticated user"""
    token = session_token
    
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
    
    session = await get_session(token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada"
        )
    
    user = await get_user_by_id(session["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user


async def require_active_subscription(user: dict) -> dict:
    """Check if user has active subscription"""
    if user.get("subscription_status") != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere suscripción activa para acceder"
        )
    
    # Check if subscription hasn't expired
    sub_end = user.get("subscription_end")
    if sub_end:
        if isinstance(sub_end, str):
            sub_end = datetime.fromisoformat(sub_end)
        if sub_end.tzinfo is None:
            sub_end = sub_end.replace(tzinfo=timezone.utc)
        
        if sub_end < datetime.now(timezone.utc):
            # Subscription expired
            await db.users.update_one(
                {"user_id": user["user_id"]},
                {"$set": {"subscription_status": "expired"}}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tu suscripción ha expirado"
            )
    
    return user
