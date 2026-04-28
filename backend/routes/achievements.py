"""
Achievements router — exposes the gamification state to the frontend.

Endpoints:
  GET  /api/achievements/me         List all 50 with locked/unlocked + summary stats.
  POST /api/achievements/check      Force a re-check (idempotent). Returns newly unlocked.
  GET  /api/achievements/definitions Public catalog (no per-user state) — useful for the
                                     "all achievements" gallery on a marketing page.
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime, timezone

from services import achievements as ach_service

router = APIRouter()
security = HTTPBearer(auto_error=False)
db = None


def set_db(database):
    global db
    db = database


async def _current_user(
    request: Request,
    session_token: Optional[str] = Cookie(default=None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """Resolve user from session token (cookie or Bearer header).

    Mirrors the helper in routes/enrollments.py so we don't depend on it.
    """
    token = session_token
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
        elif credentials:
            token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")

    session = await db.user_sessions.find_one({"session_token": token}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")

    expires_at = session.get("expires_at")
    if expires_at:
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            await db.user_sessions.delete_one({"session_token": token})
            raise HTTPException(status_code=401, detail="Sesión expirada")

    user_id = session.get("user_id")
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    if not user:
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    if "id" not in user and "user_id" in user:
        user["id"] = user["user_id"]
    return user


@router.get("/achievements/me")
async def get_my_achievements(user: dict = Depends(_current_user)):
    user_id = user.get("user_id") or user.get("id")
    return await ach_service.list_for_user(user_id, db)


@router.post("/achievements/check")
async def force_check(user: dict = Depends(_current_user)):
    """Manually re-run the check. Useful after legacy data backfills."""
    user_id = user.get("user_id") or user.get("id")
    newly = await ach_service.check_and_grant(user_id, db)
    return {"newly_unlocked": newly}


@router.get("/achievements/definitions")
async def get_definitions():
    """Catalog (no auth, no per-user state)."""
    return {"achievements": ach_service.public_definitions()}
