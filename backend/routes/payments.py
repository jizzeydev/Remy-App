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


# ==================== DEFAULT PRICING CONFIG ====================
DEFAULT_PRICING_CONFIG = {
    "monthly": {
        "id": "monthly",
        "name": "Plan Mensual",
        "description": "Acceso completo por 1 mes",
        "base_price": 9990,
        "currency": "CLP",
        "frequency": "mensual",
        "frequency_months": 1,
        "features": [
            "Acceso a todos los cursos",
            "Simulacros ilimitados",
            "Seguimiento de progreso",
            "Correcciones detalladas"
        ],
        "discount_enabled": False,
        "discount_percentage": 0,
        "promotion_start": None,
        "promotion_end": None
    },
    "semestral": {
        "id": "semestral",
        "name": "Plan Semestral",
        "description": "El más popular - 6 meses de acceso",
        "base_price": 59940,  # Original price (6 months)
        "final_price": 29990,  # Discounted price
        "currency": "CLP",
        "frequency": "semestral",
        "frequency_months": 6,
        "features": [
            "Acceso a todos los cursos",
            "Simulacros ilimitados",
            "Seguimiento de progreso",
            "Correcciones detalladas",
            "Acceso anticipado a nuevos cursos"
        ],
        "discount_enabled": True,
        "discount_percentage": 50,
        "promotion_start": None,
        "promotion_end": None,
        "is_popular": True
    }
}


async def get_pricing_config():
    """Get pricing config from database or return defaults"""
    config = await db.pricing_config.find_one({"config_id": "main"}, {"_id": 0})
    if config:
        return config.get("plans", DEFAULT_PRICING_CONFIG)
    return DEFAULT_PRICING_CONFIG


def is_discount_active(plan_config: dict) -> bool:
    """Check if discount is currently active based on dates"""
    if not plan_config.get("discount_enabled"):
        return False
    
    now = datetime.now(timezone.utc)
    start = plan_config.get("promotion_start")
    end = plan_config.get("promotion_end")
    
    # If no dates set, discount is always active when enabled
    if not start and not end:
        return True
    
    # Parse dates if they're strings
    if start and isinstance(start, str):
        start = datetime.fromisoformat(start.replace('Z', '+00:00'))
    if end and isinstance(end, str):
        end = datetime.fromisoformat(end.replace('Z', '+00:00'))
    
    # Check date range
    if start and now < start:
        return False
    if end and now > end:
        return False
    
    return True


def calculate_final_price(plan_config: dict) -> dict:
    """Calculate final price considering discounts"""
    base_price = plan_config.get("base_price", 0)
    
    # Check if this plan has a fixed final_price (like semestral)
    if "final_price" in plan_config and is_discount_active(plan_config):
        return {
            "amount": plan_config["final_price"],
            "original_amount": base_price,
            "discount_percentage": plan_config.get("discount_percentage", 0),
            "discount_active": True
        }
    
    # Calculate based on percentage discount
    if is_discount_active(plan_config):
        discount_pct = plan_config.get("discount_percentage", 0)
        discounted_price = int(base_price * (100 - discount_pct) / 100)
        return {
            "amount": discounted_price,
            "original_amount": base_price,
            "discount_percentage": discount_pct,
            "discount_active": True
        }
    
    return {
        "amount": base_price,
        "original_amount": None,
        "discount_percentage": 0,
        "discount_active": False
    }


# ==================== SUBSCRIPTION ENDPOINTS ====================

@router.get("/plans")
async def get_available_plans():
    """Get all available subscription plans with current pricing"""
    pricing_config = await get_pricing_config()
    
    plans = []
    for plan_id, config in pricing_config.items():
        price_info = calculate_final_price(config)
        
        plan_data = {
            "id": config.get("id", plan_id),
            "name": config.get("name"),
            "description": config.get("description"),
            "amount": price_info["amount"],
            "currency": config.get("currency", "CLP"),
            "frequency": config.get("frequency"),
            "features": config.get("features", [])
        }
        
        # Add discount info if active
        if price_info["discount_active"]:
            plan_data["original_amount"] = price_info["original_amount"]
            plan_data["discount"] = f"{price_info['discount_percentage']}%"
        
        # Add popular flag
        if config.get("is_popular"):
            plan_data["is_popular"] = True
        
        plans.append(plan_data)
    
    # Sort: monthly first, then semestral
    plans.sort(key=lambda x: 0 if x["id"] == "monthly" else 1)
    
    return {
        "plans": plans,
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
    logger.info(f"Creating subscription for {current_user['email']}: plan_id={request.plan_id}")
    
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
    logger.info(f"Selected plan: {plan['name']} - ${plan['amount']} CLP")
    
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
    has_access = False
    subscription_end = current_user.get("subscription_end")
    subscription_status = current_user.get("subscription_status")
    
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
            
            # User has access if subscription is active OR cancelled but still within paid period
            if subscription_status == "active":
                has_access = True
            elif subscription_status == "cancelled" and days_remaining > 0:
                has_access = True  # Cancelled but paid period not over
                
        except Exception as e:
            logger.warning(f"Error calculating days remaining: {e}")
    
    # Also check for active status without end date (manual subscriptions)
    if subscription_status == "active" and not has_access:
        has_access = True
    
    # Get plan details
    plan_id = current_user.get("subscription_plan")
    plan_info = PLANS.get(plan_id, {}) if plan_id else {}
    
    return {
        "has_subscription": has_access,
        "subscription_status": current_user.get("subscription_status", "inactive"),
        "subscription_type": current_user.get("subscription_type"),
        "subscription_plan": current_user.get("subscription_plan"),
        "subscription_start": current_user.get("subscription_start"),
        "subscription_end": current_user.get("subscription_end"),
        "days_remaining": days_remaining,
        "auto_renewal": current_user.get("subscription_type") == "mercadopago" and current_user.get("subscription_status") == "active",
        "is_cancelled": current_user.get("subscription_status") == "cancelled",
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
    """
    Cancel current subscription - user keeps access until end of paid period
    """
    if current_user.get("subscription_status") not in ["active", "cancelled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No tienes una suscripción activa"
        )
    
    # Already cancelled
    if current_user.get("subscription_status") == "cancelled":
        return {
            "success": True,
            "message": "Tu suscripción ya está cancelada. Mantendrás acceso hasta el final del período pagado."
        }
    
    subscription_id = current_user.get("subscription_id")
    subscription_type = current_user.get("subscription_type")
    subscription_end = current_user.get("subscription_end")
    
    try:
        # If Mercado Pago subscription, cancel auto-renewal (but keep access)
        if subscription_type == "mercadopago" and subscription_id:
            try:
                mp_service.cancel_preapproval(subscription_id)
                logger.info(f"MP preapproval cancelled: {subscription_id}")
            except Exception as e:
                logger.warning(f"Could not cancel MP subscription: {e}")
        
        # Update user status to 'cancelled' but KEEP subscription_end date
        # This allows continued access until the paid period ends
        await db.users.update_one(
            {"user_id": current_user["user_id"]},
            {"$set": {
                "subscription_status": "cancelled",
                "auto_renewal": False
                # Note: subscription_end is NOT modified - user keeps access until then
            }}
        )
        
        # Update subscription record
        await db.subscriptions.update_one(
            {"user_id": current_user["user_id"], "status": "active"},
            {"$set": {
                "status": "cancelled",
                "auto_renewal": False,
                "cancelled_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        logger.info(f"Subscription cancelled for {current_user['email']}, access until {subscription_end}")
        
        # Send cancellation notification
        if notify_subscription_cancelled:
            try:
                import asyncio
                asyncio.create_task(notify_subscription_cancelled(
                    current_user.get("email"),
                    current_user.get("name", "Usuario"),
                    "Cancelación por usuario"
                ))
            except Exception as e:
                logger.error(f"Failed to send cancellation email: {e}")
        
        return {
            "success": True,
            "message": "Suscripción cancelada. Tu acceso continuará hasta el final del período pagado.",
            "access_until": subscription_end
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


# ==================== ADMIN PRICING ENDPOINTS ====================
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

admin_security = HTTPBearer()

# Allowed admin emails for Google login
ALLOWED_ADMIN_EMAILS = [
    'seremonta.cl@gmail.com',
    'admin@seremonta.cl'
]


async def verify_admin_for_pricing(credentials: HTTPAuthorizationCredentials = Depends(admin_security)):
    """Verify admin JWT token for pricing management"""
    try:
        token = credentials.credentials
        secret_key = os.environ.get('ADMIN_SECRET_KEY')
        admin_username = os.environ.get('ADMIN_USERNAME')
        
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        subject: str = payload.get("sub")
        token_type: str = payload.get("type", "")
        
        if subject is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de administrador inválidas"
            )
        
        # Check if it's a Google admin token
        if token_type == "admin_google":
            if subject.lower() not in [e.lower() for e in ALLOWED_ADMIN_EMAILS]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales de administrador inválidas"
                )
            return subject
        
        # Traditional username/password admin
        if subject != admin_username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de administrador inválidas"
            )
        return subject
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de administrador inválidas"
        )


class PlanPricingUpdate(BaseModel):
    name: str
    description: str
    base_price: int
    final_price: Optional[int] = None  # For semestral with fixed discount
    features: list[str]
    discount_enabled: bool = False
    discount_percentage: int = 0
    promotion_start: Optional[str] = None
    promotion_end: Optional[str] = None
    is_popular: bool = False


class PricingConfigUpdate(BaseModel):
    monthly: PlanPricingUpdate
    semestral: PlanPricingUpdate


@router.get("/admin/pricing")
async def get_admin_pricing(_: str = Depends(verify_admin_for_pricing)):
    """Get current pricing configuration for admin"""
    pricing_config = await get_pricing_config()
    
    # Get last updated timestamp
    config_doc = await db.pricing_config.find_one({"config_id": "main"}, {"_id": 0, "updated_at": 1})
    last_updated = config_doc.get("updated_at") if config_doc else None
    
    return {
        "plans": pricing_config,
        "last_updated": last_updated
    }


@router.put("/admin/pricing")
async def update_pricing(config: PricingConfigUpdate, _: str = Depends(verify_admin_for_pricing)):
    """Update pricing configuration"""
    try:
        # Build config object
        pricing_data = {
            "monthly": {
                "id": "monthly",
                "name": config.monthly.name,
                "description": config.monthly.description,
                "base_price": config.monthly.base_price,
                "currency": "CLP",
                "frequency": "mensual",
                "frequency_months": 1,
                "features": config.monthly.features,
                "discount_enabled": config.monthly.discount_enabled,
                "discount_percentage": config.monthly.discount_percentage,
                "promotion_start": config.monthly.promotion_start,
                "promotion_end": config.monthly.promotion_end,
                "is_popular": config.monthly.is_popular
            },
            "semestral": {
                "id": "semestral",
                "name": config.semestral.name,
                "description": config.semestral.description,
                "base_price": config.semestral.base_price,
                "final_price": config.semestral.final_price or int(config.semestral.base_price * (100 - config.semestral.discount_percentage) / 100),
                "currency": "CLP",
                "frequency": "semestral",
                "frequency_months": 6,
                "features": config.semestral.features,
                "discount_enabled": config.semestral.discount_enabled,
                "discount_percentage": config.semestral.discount_percentage,
                "promotion_start": config.semestral.promotion_start,
                "promotion_end": config.semestral.promotion_end,
                "is_popular": config.semestral.is_popular
            }
        }
        
        # Upsert pricing config
        await db.pricing_config.update_one(
            {"config_id": "main"},
            {
                "$set": {
                    "plans": pricing_data,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "config_id": "main"
                }
            },
            upsert=True
        )
        
        logger.info("Pricing config updated successfully")
        return {"success": True, "message": "Precios actualizados correctamente"}
        
    except Exception as e:
        logger.error(f"Error updating pricing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/pricing/reset")
async def reset_pricing(_: str = Depends(verify_admin_for_pricing)):
    """Reset pricing to default values"""
    try:
        await db.pricing_config.delete_one({"config_id": "main"})
        logger.info("Pricing config reset to defaults")
        return {"success": True, "message": "Precios restaurados a valores por defecto"}
    except Exception as e:
        logger.error(f"Error resetting pricing: {e}")
        raise HTTPException(status_code=500, detail=str(e))
