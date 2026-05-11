"""Meta Pixel / Conversions API forwarder.

Endpoint público: el frontend dispara fbq browser-side y POSTea acá el mismo
evento (con el mismo event_id) para que Meta deduplique. Esto mejora el match
rate cuando el navegador del usuario bloquea Pixel (ad-blockers, iOS ITP, etc).
"""
from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Cookie, Request
from pydantic import BaseModel, Field

from services.meta_pixel_service import meta_pixel_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/meta", tags=["meta-pixel"])

# DB se setea desde server.py si se necesita.
db = None


def set_db(database):
    global db
    db = database


class MetaUserData(BaseModel):
    email: Optional[str] = None
    external_id: Optional[str] = None
    fbp: Optional[str] = None
    fbc: Optional[str] = None


class MetaTrackRequest(BaseModel):
    event_name: str
    event_id: Optional[str] = None
    event_source_url: Optional[str] = None
    custom_data: dict = Field(default_factory=dict)
    user_data: MetaUserData = Field(default_factory=MetaUserData)


def _client_ip(request: Request) -> Optional[str]:
    # Detrás de Render / Cloudflare, X-Forwarded-For trae la IP real.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


async def _resolve_user_email_from_session(session_token: Optional[str]) -> Optional[str]:
    """Si el browser está logueado pero no mandó email (case habitual: PageView
    de página interna), intentamos enriquecer desde la sesión para que el match
    rate sea mejor."""
    if not session_token or db is None:
        return None
    try:
        session = await db.user_sessions.find_one(
            {"session_token": session_token}, {"_id": 0, "user_id": 1}
        )
        if not session:
            return None
        user = await db.users.find_one(
            {"user_id": session["user_id"]}, {"_id": 0, "email": 1}
        )
        return user.get("email") if user else None
    except Exception as e:
        logger.debug("No pude resolver email desde sesión para CAPI: %s", e)
        return None


@router.post("/track")
async def track_meta_event(
    payload: MetaTrackRequest,
    request: Request,
    session_token: Optional[str] = Cookie(default=None),
):
    """Recibe un evento del frontend y lo reenvía a la Conversions API."""
    if not meta_pixel_service.enabled:
        return {"status": "disabled"}

    email = payload.user_data.email
    external_id = payload.user_data.external_id

    # Enriquecer con datos de sesión si el browser no los mandó (no rompemos
    # privacy: ya autenticamos al usuario contra nuestra propia DB).
    if not email:
        # Cookie de sesión o Authorization header.
        token = session_token
        if not token:
            auth_header = request.headers.get("authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]
        if token:
            email = await _resolve_user_email_from_session(token)

    await meta_pixel_service.send_event(
        event_name=payload.event_name,
        event_id=payload.event_id,
        event_source_url=payload.event_source_url,
        custom_data=payload.custom_data or None,
        email=email,
        external_id=external_id,
        client_ip=_client_ip(request),
        client_user_agent=request.headers.get("user-agent"),
        fbp=payload.user_data.fbp,
        fbc=payload.user_data.fbc,
    )

    return {"status": "received"}
