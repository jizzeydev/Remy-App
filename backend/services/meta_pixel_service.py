"""Meta Conversions API service (server-side tracking).

Pegamos a https://graph.facebook.com/v18.0/{PIXEL_ID}/events. Hasheamos PII
con SHA-256 antes de enviar (requerimiento de Meta para email/phone/name/etc).

Si META_PIXEL_ID o META_ACCESS_TOKEN no están configurados, todas las llamadas
quedan como no-op silencioso (devuelven None) — el resto del sistema no falla.

Refs:
- https://developers.facebook.com/docs/marketing-api/conversions-api
- https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/customer-information-parameters
"""
from __future__ import annotations

import hashlib
import logging
import os
import time
import uuid
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

META_API_VERSION = "v18.0"


def _hash(value: Optional[str]) -> Optional[str]:
    """SHA-256 lowercase trimmed. Meta requirement para datos del cliente."""
    if not value:
        return None
    normalized = str(value).strip().lower()
    if not normalized:
        return None
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class MetaPixelService:
    """Cliente delgado para la Conversions API de Meta."""

    def __init__(self):
        self.pixel_id = os.environ.get("META_PIXEL_ID", "").strip()
        self.access_token = os.environ.get("META_ACCESS_TOKEN", "").strip()
        # Code para sandbox / Events Manager → Test Events. Solo en QA.
        self.test_event_code = os.environ.get("META_TEST_EVENT_CODE", "").strip() or None
        self.enabled = bool(self.pixel_id and self.access_token)
        if not self.enabled:
            logger.info("Meta Conversions API deshabilitada (faltan META_PIXEL_ID / META_ACCESS_TOKEN)")

    def _endpoint(self) -> str:
        return f"https://graph.facebook.com/{META_API_VERSION}/{self.pixel_id}/events"

    def _build_user_data(
        self,
        *,
        email: Optional[str] = None,
        external_id: Optional[str] = None,
        client_ip: Optional[str] = None,
        client_user_agent: Optional[str] = None,
        fbp: Optional[str] = None,
        fbc: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> dict:
        user_data: dict = {}
        if email:
            user_data["em"] = [_hash(email)]
        if external_id:
            # external_id se puede mandar sin hashear, pero Meta recomienda hashear.
            user_data["external_id"] = [_hash(external_id)]
        if first_name:
            user_data["fn"] = [_hash(first_name)]
        if last_name:
            user_data["ln"] = [_hash(last_name)]
        if client_ip:
            user_data["client_ip_address"] = client_ip
        if client_user_agent:
            user_data["client_user_agent"] = client_user_agent
        if fbp:
            user_data["fbp"] = fbp
        if fbc:
            user_data["fbc"] = fbc
        return user_data

    async def send_event(
        self,
        *,
        event_name: str,
        event_id: Optional[str] = None,
        event_source_url: Optional[str] = None,
        action_source: str = "website",
        custom_data: Optional[dict] = None,
        # User data (sin hashear; el servicio se encarga).
        email: Optional[str] = None,
        external_id: Optional[str] = None,
        client_ip: Optional[str] = None,
        client_user_agent: Optional[str] = None,
        fbp: Optional[str] = None,
        fbc: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Optional[dict]:
        """Envía un evento a la Conversions API.

        Devuelve el response JSON de Meta, o None si la integración está
        deshabilitada o si la llamada falló (no propagamos la excepción para
        que el tracking nunca rompa el flujo del usuario).
        """
        if not self.enabled:
            return None

        event = {
            "event_name": event_name,
            "event_time": int(time.time()),
            "action_source": action_source,
            "event_id": event_id or str(uuid.uuid4()),
            "user_data": self._build_user_data(
                email=email,
                external_id=external_id,
                client_ip=client_ip,
                client_user_agent=client_user_agent,
                fbp=fbp,
                fbc=fbc,
                first_name=first_name,
                last_name=last_name,
            ),
        }
        if event_source_url:
            event["event_source_url"] = event_source_url
        if custom_data:
            event["custom_data"] = custom_data

        payload: dict = {
            "data": [event],
            "access_token": self.access_token,
        }
        if self.test_event_code:
            payload["test_event_code"] = self.test_event_code

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.post(self._endpoint(), json=payload)
            if resp.status_code >= 400:
                logger.warning(
                    "Meta CAPI %s rechazado (status=%s): %s",
                    event_name,
                    resp.status_code,
                    resp.text[:500],
                )
                return None
            return resp.json()
        except Exception as e:
            logger.warning("Meta CAPI %s falló: %s", event_name, e)
            return None


# Singleton.
meta_pixel_service = MetaPixelService()
