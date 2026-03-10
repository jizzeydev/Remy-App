"""Payment and subscription routes for Remy platform - Mercado Pago integration"""
from fastapi import APIRouter, HTTPException, status, Request, Depends
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from typing import Optional
import logging
import os
import asyncio

from services.mercadopago_service import MercadoPagoService, PLANS
from routes.auth import get_current_user_dependency

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/payments", tags=["payments"])

# MongoDB connection (will be set from main app)
db = None

# Email notification functions
notify_subscription_started = None
notify_subscription_cancelled = None

def set_db(database):
    """Set database instance from main app"""
    global db, notify_subscription_started, notify_subscription_cancelled
    db = database
    # Import email service
    from services.email_service import (
        notify_subscription_started as notify_start,
        notify_subscription_cancelled as notify_cancel
    )
    notify_subscription_started = notify_start
    notify_subscription_cancelled = notify_cancel


# Initialize Mercado Pago service
mp_service = MercadoPagoService()


# Request/Response models
class CreateSubscriptionRequest(BaseModel):
    plan_id: str  # "monthly" or "semestral"
    card_token: str


class SubscriptionResponse(BaseModel):
    subscription_id: str
    plan: str
    status: str
    amount: float
    currency: str
    start_date: str
    end_date: Optional[str] = None


# Helper functions
def calculate_end_date(plan_id: str) -> datetime:
    """Calculate subscription end date based on plan"""
    plan = PLANS.get(plan_id)
    if not plan:
        raise ValueError(f"Invalid plan: {plan_id}")
    
    months = plan["frequency"]
    return datetime.now(timezone.utc) + timedelta(days=30 * months)


async def update_user_subscription(
    user_id: str,
    plan_id: str,
    subscription_type: str,
    subscription_id: Optional[str] = None,
    status: str = "active"
) -> dict:
    """Update user's subscription status"""
    end_date = calculate_end_date(plan_id)
    
    update_data = {
        "subscription_status": status,
        "subscription_type": subscription_type,
        "subscription_plan": plan_id,
        "subscription_id": subscription_id,
        "subscription_start": datetime.now(timezone.utc).isoformat(),
        "subscription_end": end_date.isoformat()
    }
    
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": update_data}
    )
    
    return update_data


# ==================== SUBSCRIPTION ENDPOINTS ====================

@router.get("/plans")
async def get_available_plans():
    """Get all available subscription plans"""
    return {
        "plans": [
            {
                "id": "monthly",
                "name": "Plan Mensual",
                "description": "Acceso completo por 1 mes",
                "amount": 9990,
                "currency": "CLP",
                "frequency": "mensual",
                "features": [
                    "Acceso a todos los cursos",
                    "Simulacros ilimitados",
                    "Seguimiento de progreso",
                    "Soporte prioritario"
                ]
            },
            {
                "id": "semestral",
                "name": "Plan Semestral",
                "description": "Ahorra 50% - 6 meses de acceso",
                "amount": 29990,
                "original_amount": 59940,
                "currency": "CLP",
                "frequency": "semestral",
                "discount": "50%",
                "features": [
                    "Acceso a todos los cursos",
                    "Simulacros ilimitados",
                    "Seguimiento de progreso",
                    "Soporte prioritario",
                    "Contenido exclusivo",
                    "Acceso anticipado a nuevos cursos"
                ]
            }
        ],
        "mercadopago_public_key": os.environ.get("MERCADOPAGO_PUBLIC_KEY", "")
    }


@router.post("/subscribe")
async def create_subscription(
    request: CreateSubscriptionRequest,
    current_user: dict = Depends(get_current_user_dependency)
):
    """
    Create a new subscription via Mercado Pago
    
    Requires:
    - plan_id: "monthly" or "semestral"
    - card_token: Token from Mercado Pago JS SDK
    """
    if request.plan_id not in PLANS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan inválido. Planes disponibles: {list(PLANS.keys())}"
        )
    
    # Check if user already has active subscription
    if current_user.get("subscription_status") == "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya tienes una suscripción activa"
        )
    
    plan = PLANS[request.plan_id]
    
    try:
        # Get base URL from environment variable
        # In production, FRONTEND_URL should be set to https://remy.seremonta.store
        # In preview, it should be the preview URL
        base_url = os.environ.get("FRONTEND_URL")
        if not base_url:
            logger.warning("FRONTEND_URL not set, using fallback")
            base_url = "https://remy.seremonta.store"
        back_url = f"{base_url}/biblioteca?subscription=success"
        
        # Create subscription in Mercado Pago
        mp_response = mp_service.create_preapproval(
            plan_id=request.plan_id,
            payer_email=current_user["email"],
            card_token=request.card_token,
            back_url=back_url
        )
        
        mercadopago_id = mp_response.get("id")
        mp_status = mp_response.get("status", "pending")
        
        # Map Mercado Pago status to our status
        status_map = {
            "authorized": "active",
            "pending": "pending",
            "cancelled": "cancelled"
        }
        our_status = status_map.get(mp_status, "pending")
        
        # Update user subscription
        await update_user_subscription(
            user_id=current_user["user_id"],
            plan_id=request.plan_id,
            subscription_type="mercadopago",
            subscription_id=mercadopago_id,
            status=our_status
        )
        
        # Save subscription record
        subscription_record = {
            "id": f"sub_{mercadopago_id}",
            "user_id": current_user["user_id"],
            "user_email": current_user["email"],
            "plan": request.plan_id,
            "subscription_type": "mercadopago",
            "mercadopago_id": mercadopago_id,
            "amount": plan["amount"],
            "currency": plan["currency"],
            "status": our_status,
            "start_date": datetime.now(timezone.utc).isoformat(),
            "end_date": calculate_end_date(request.plan_id).isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.subscriptions.insert_one(subscription_record)
        
        logger.info(f"Subscription created for {current_user['email']}: {mercadopago_id}")
        
        return {
            "success": True,
            "subscription_id": mercadopago_id,
            "status": our_status,
            "plan": request.plan_id,
            "message": "Suscripción creada exitosamente" if our_status == "active" else "Suscripción pendiente de autorización",
            "init_point": mp_response.get("init_point")  # URL to complete payment if needed
        }
        
    except Exception as e:
        logger.error(f"Error creating subscription: {e}")
        logger.error(f"Full error details: {repr(e)}")
        # Return more detailed error message
        error_msg = str(e)
        if "card_token" in error_msg.lower():
            error_msg = "Token de tarjeta inválido o expirado. Por favor intenta de nuevo."
        elif "payer_email" in error_msg.lower():
            error_msg = "Error con el email del pagador"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el pago: {error_msg}"
        )


@router.get("/subscription")
async def get_subscription_status(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get current user's subscription status with detailed info"""
    subscription = await db.subscriptions.find_one(
        {"user_id": current_user["user_id"], "status": {"$in": ["active", "pending", "cancelled"]}},
        {"_id": 0},
        sort=[("created_at", -1)]  # Get most recent
    )
    
    # Calculate days remaining
    days_remaining = 0
    subscription_end = current_user.get("subscription_end")
    if subscription_end:
        try:
            if isinstance(subscription_end, str):
                end_date = datetime.fromisoformat(subscription_end.replace('Z', '+00:00'))
            else:
                end_date = subscription_end
            
            if end_date.tzinfo is None:
                end_date = end_date.replace(tzinfo=timezone.utc)
            
            diff = end_date - datetime.now(timezone.utc)
            days_remaining = max(0, diff.days)
        except Exception as e:
            logger.warning(f"Error calculating days remaining: {e}")
    
    # Get plan details
    plan_id = current_user.get("subscription_plan")
    plan_info = PLANS.get(plan_id, {}) if plan_id else {}
    
    return {
        "has_subscription": current_user.get("subscription_status") == "active",
        "subscription_status": current_user.get("subscription_status", "inactive"),
        "subscription_type": current_user.get("subscription_type"),
        "subscription_plan": current_user.get("subscription_plan"),
        "subscription_start": current_user.get("subscription_start"),
        "subscription_end": current_user.get("subscription_end"),
        "days_remaining": days_remaining,
        "auto_renewal": current_user.get("subscription_type") == "mercadopago",
        "plan_details": {
            "name": plan_info.get("name", ""),
            "amount": plan_info.get("amount", 0),
            "currency": plan_info.get("currency", "CLP"),
            "frequency": plan_info.get("frequency", 1),
            "frequency_type": plan_info.get("frequency_type", "months")
        } if plan_info else None,
        "subscription_details": subscription
    }


@router.post("/cancel")
async def cancel_subscription(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Cancel current subscription"""
    if current_user.get("subscription_status") != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No tienes una suscripción activa"
        )
    
    subscription_id = current_user.get("subscription_id")
    subscription_type = current_user.get("subscription_type")
    
    try:
        # If Mercado Pago subscription, cancel it there too
        if subscription_type == "mercadopago" and subscription_id:
            try:
                mp_service.cancel_preapproval(subscription_id)
            except Exception as e:
                logger.warning(f"Could not cancel MP subscription: {e}")
        
        # Update user status
        await db.users.update_one(
            {"user_id": current_user["user_id"]},
            {"$set": {
                "subscription_status": "cancelled",
                "subscription_id": None
            }}
        )
        
        # Update subscription record
        await db.subscriptions.update_one(
            {"user_id": current_user["user_id"], "status": "active"},
            {"$set": {
                "status": "cancelled",
                "cancelled_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        logger.info(f"Subscription cancelled for {current_user['email']}")
        
        return {
            "success": True,
            "message": "Suscripción cancelada. Tu acceso continuará hasta el final del período pagado."
        }
        
    except Exception as e:
        logger.error(f"Error cancelling subscription: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cancelar la suscripción"
        )


# ==================== WEBHOOK HANDLERS ====================

@router.post("/webhook/mercadopago")
async def mercadopago_webhook(request: Request):
    """
    Handle Mercado Pago webhook notifications
    
    Receives notifications for:
    - payment.created / payment.updated
    - subscription.authorized / subscription.cancelled
    """
    try:
        # Verify webhook signature if secret is configured
        webhook_secret = os.environ.get("MERCADOPAGO_WEBHOOK_SECRET")
        if webhook_secret:
            # Get signature from headers
            x_signature = request.headers.get("x-signature")
            x_request_id = request.headers.get("x-request-id")
            
            if x_signature:
                # Parse signature parts
                signature_parts = {}
                for part in x_signature.split(","):
                    if "=" in part:
                        key, value = part.split("=", 1)
                        signature_parts[key.strip()] = value.strip()
                
                # Get raw body for signature verification
                body = await request.body()
                
                # Log for debugging (remove in production if too verbose)
                logger.info(f"Webhook received - Request ID: {x_request_id}")
        
        payload = await request.json()
        
        action = payload.get("action", payload.get("type", ""))
        data = payload.get("data", {})
        
        logger.info(f"Mercado Pago webhook: {action}")
        
        # Handle payment notifications
        if "payment" in action:
            payment_id = data.get("id")
            payment_status = data.get("status")
            
            # Get subscription by payment external reference
            external_ref = data.get("external_reference", "")
            
            if payment_status == "approved":
                # Find subscription and activate
                subscription = await db.subscriptions.find_one(
                    {"mercadopago_id": {"$regex": external_ref}},
                    {"_id": 0}
                )
                
                if subscription:
                    # Activate user subscription
                    await db.users.update_one(
                        {"user_id": subscription["user_id"]},
                        {"$set": {"subscription_status": "active"}}
                    )
                    
                    await db.subscriptions.update_one(
                        {"id": subscription["id"]},
                        {"$set": {"status": "active"}}
                    )
                    
                    logger.info(f"Subscription activated via webhook: {subscription['user_email']}")
                    
                    # Send email notification
                    try:
                        user = await db.users.find_one(
                            {"user_id": subscription["user_id"]},
                            {"_id": 0, "email": 1, "name": 1}
                        )
                        if user and notify_subscription_started:
                            asyncio.create_task(notify_subscription_started(
                                user.get("email", subscription["user_email"]),
                                user.get("name", "Usuario"),
                                subscription.get("plan", "monthly"),
                                subscription.get("amount", 0)
                            ))
                    except Exception as e:
                        logger.error(f"Failed to send subscription email: {e}")
        
        # Handle subscription notifications
        elif "subscription" in action or "preapproval" in action:
            preapproval_id = data.get("id")
            status = data.get("status")
            
            if preapproval_id:
                # Find subscription by Mercado Pago ID
                subscription = await db.subscriptions.find_one(
                    {"mercadopago_id": preapproval_id},
                    {"_id": 0}
                )
                
                if subscription:
                    status_map = {
                        "authorized": "active",
                        "cancelled": "cancelled",
                        "pending": "pending"
                    }
                    our_status = status_map.get(status, subscription.get("status", "pending"))
                    
                    await db.users.update_one(
                        {"user_id": subscription["user_id"]},
                        {"$set": {"subscription_status": our_status}}
                    )
                    
                    await db.subscriptions.update_one(
                        {"id": subscription["id"]},
                        {"$set": {"status": our_status}}
                    )
                    
                    logger.info(f"Subscription updated via webhook: {preapproval_id} -> {our_status}")
                    
                    # Send cancellation notification
                    if our_status == "cancelled" and notify_subscription_cancelled:
                        try:
                            user = await db.users.find_one(
                                {"user_id": subscription["user_id"]},
                                {"_id": 0, "email": 1, "name": 1}
                            )
                            if user:
                                asyncio.create_task(notify_subscription_cancelled(
                                    user.get("email", subscription["user_email"]),
                                    user.get("name", "Usuario"),
                                    "Cancelación desde Mercado Pago"
                                ))
                        except Exception as e:
                            logger.error(f"Failed to send cancellation email: {e}")
        
        return {"status": "received"}
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        # Return 200 to prevent retries
        return {"status": "error", "detail": str(e)}
