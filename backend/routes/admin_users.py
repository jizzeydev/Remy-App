"""Admin user management routes for Remy platform"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from jose import JWTError, jwt
import logging
import uuid
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/users", tags=["admin-users"])

# Security
security = HTTPBearer()

# MongoDB connection (will be set from main app)
db = None


def set_db(database):
    """Set database instance from main app"""
    global db
    db = database


# Allowed admin emails for Google login
ALLOWED_ADMIN_EMAILS = [
    'seremonta.cl@gmail.com',
    'admin@seremonta.cl'
]

# Admin authentication - supports both traditional and Google login
async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify admin JWT token (traditional or Google)"""
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
                    detail="Email no autorizado como administrador"
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
            detail="Token de administrador inválido o expirado"
        )


# Request/Response models
class GrantAccessRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    duration_months: int = 1  # Default 1 month


class UserListResponse(BaseModel):
    users: List[dict]
    total: int


# Helper functions
def generate_user_id() -> str:
    return f"user_{uuid.uuid4().hex[:12]}"


def calculate_end_date(months: int) -> datetime:
    """Calculate subscription end date"""
    return datetime.now(timezone.utc) + timedelta(days=30 * months)


# ==================== ADMIN USER MANAGEMENT ====================

@router.get("")
async def list_users(
    page: int = 1,
    limit: int = 50,
    status_filter: Optional[str] = None,
    search: Optional[str] = None,
    _: str = Depends(verify_admin_token)
):
    """
    List all registered users with their subscription status
    
    Query params:
    - page: Page number (default 1)
    - limit: Items per page (default 50)
    - status_filter: Filter by subscription_status (active, inactive, cancelled, expired)
    - search: Search by email or name
    """
    # Build query
    query = {}
    
    if status_filter:
        query["subscription_status"] = status_filter
    
    if search:
        query["$or"] = [
            {"email": {"$regex": search, "$options": "i"}},
            {"name": {"$regex": search, "$options": "i"}}
        ]
    
    # Get total count
    total = await db.users.count_documents(query)
    
    # Get paginated users
    skip = (page - 1) * limit
    users = await db.users.find(
        query,
        {"_id": 0, "password_hash": 0}  # Exclude sensitive data
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    # Format dates
    for user in users:
        for date_field in ["created_at", "subscription_start", "subscription_end"]:
            if date_field in user and isinstance(user[date_field], str):
                try:
                    user[date_field] = datetime.fromisoformat(user[date_field]).isoformat()
                except:
                    pass
    
    return {
        "users": users,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/stats")
async def get_user_stats(_: str = Depends(verify_admin_token)):
    """Get user and subscription statistics"""
    
    # Total users
    total_users = await db.users.count_documents({})
    
    # Users by subscription status
    active_subs = await db.users.count_documents({"subscription_status": "active"})
    inactive_users = await db.users.count_documents({"subscription_status": "inactive"})
    cancelled_subs = await db.users.count_documents({"subscription_status": "cancelled"})
    expired_subs = await db.users.count_documents({"subscription_status": "expired"})
    
    # Users by subscription type
    mercadopago_users = await db.users.count_documents({
        "subscription_status": "active",
        "subscription_type": "mercadopago"
    })
    manual_users = await db.users.count_documents({
        "subscription_status": "active",
        "subscription_type": "manual"
    })
    
    # Users by auth provider
    google_users = await db.users.count_documents({"auth_provider": "google"})
    email_users = await db.users.count_documents({"auth_provider": "email"})
    
    # Recent registrations (last 7 days)
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    recent_users = await db.users.count_documents({
        "created_at": {"$gte": week_ago.isoformat()}
    })
    
    return {
        "total_users": total_users,
        "subscription_stats": {
            "active": active_subs,
            "inactive": inactive_users,
            "cancelled": cancelled_subs,
            "expired": expired_subs
        },
        "subscription_types": {
            "mercadopago": mercadopago_users,
            "manual": manual_users
        },
        "auth_providers": {
            "google": google_users,
            "email": email_users
        },
        "recent_registrations": recent_users
    }


@router.get("/revenue/summary")
async def get_revenue_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    _: str = Depends(verify_admin_token)
):
    """
    Get revenue summary for a date range
    
    Query params:
    - start_date: ISO date string (default: first day of current month)
    - end_date: ISO date string (default: today)
    
    Returns:
    - Total revenue in the period
    - Number of paid subscriptions
    - Revenue breakdown by plan
    - Daily revenue data for chart
    """
    now = datetime.now(timezone.utc)
    
    # Default to current month
    if not start_date:
        start_dt = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            if start_dt.tzinfo is None:
                start_dt = start_dt.replace(tzinfo=timezone.utc)
        except:
            start_dt = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    if not end_date:
        end_dt = now
    else:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            if end_dt.tzinfo is None:
                end_dt = end_dt.replace(tzinfo=timezone.utc)
        except:
            end_dt = now
    
    # Query payments in date range
    query = {
        "status": {"$in": ["active", "authorized", "completed"]},
        "created_at": {
            "$gte": start_dt.isoformat(),
            "$lte": end_dt.isoformat()
        },
        "subscription_type": {"$ne": "manual"}  # Exclude manual (free) subscriptions
    }
    
    subscriptions = await db.subscriptions.find(query, {"_id": 0}).to_list(1000)
    
    # Calculate totals
    total_revenue = sum(sub.get("amount", 0) for sub in subscriptions)
    total_subscriptions = len(subscriptions)
    
    # Revenue by plan
    revenue_by_plan = {}
    for sub in subscriptions:
        plan = sub.get("plan", "unknown")
        revenue_by_plan[plan] = revenue_by_plan.get(plan, 0) + sub.get("amount", 0)
    
    # Daily breakdown for chart
    daily_revenue = {}
    for sub in subscriptions:
        created_at = sub.get("created_at", "")
        if created_at:
            try:
                day = created_at[:10]  # Extract YYYY-MM-DD
                daily_revenue[day] = daily_revenue.get(day, 0) + sub.get("amount", 0)
            except:
                pass
    
    # Sort daily data
    sorted_daily = sorted(daily_revenue.items())
    
    return {
        "period": {
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        },
        "total_revenue": total_revenue,
        "currency": "CLP",
        "total_subscriptions": total_subscriptions,
        "revenue_by_plan": revenue_by_plan,
        "daily_revenue": [
            {"date": day, "amount": amount} 
            for day, amount in sorted_daily
        ],
        "average_per_subscription": total_revenue / total_subscriptions if total_subscriptions > 0 else 0
    }


@router.get("/revenue/monthly")
async def get_monthly_revenue(
    months: int = 6,
    _: str = Depends(verify_admin_token)
):
    """
    Get revenue data for the last N months
    
    Returns monthly totals for comparison
    """
    now = datetime.now(timezone.utc)
    monthly_data = []
    
    for i in range(months):
        # Calculate month boundaries
        if i == 0:
            month_end = now
        else:
            month_end = now.replace(day=1) - timedelta(days=1)
            for _ in range(i - 1):
                month_end = month_end.replace(day=1) - timedelta(days=1)
        
        month_start = month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Calculate the actual month we're querying
        target_month = now.month - i
        target_year = now.year
        while target_month <= 0:
            target_month += 12
            target_year -= 1
        
        month_start = datetime(target_year, target_month, 1, tzinfo=timezone.utc)
        if target_month == 12:
            month_end = datetime(target_year + 1, 1, 1, tzinfo=timezone.utc) - timedelta(seconds=1)
        else:
            month_end = datetime(target_year, target_month + 1, 1, tzinfo=timezone.utc) - timedelta(seconds=1)
        
        # Query subscriptions for this month
        query = {
            "status": {"$in": ["active", "authorized", "completed"]},
            "created_at": {
                "$gte": month_start.isoformat(),
                "$lte": month_end.isoformat()
            },
            "subscription_type": {"$ne": "manual"}
        }
        
        subs = await db.subscriptions.find(query, {"_id": 0, "amount": 1}).to_list(1000)
        revenue = sum(sub.get("amount", 0) for sub in subs)
        
        monthly_data.append({
            "month": month_start.strftime("%Y-%m"),
            "month_name": month_start.strftime("%B %Y"),
            "revenue": revenue,
            "subscriptions": len(subs)
        })
    
    return {
        "monthly_data": list(reversed(monthly_data)),  # Oldest to newest
        "currency": "CLP"
    }


@router.get("/{user_id}")
async def get_user_details(
    user_id: str,
    _: str = Depends(verify_admin_token)
):
    """Get detailed information about a specific user"""
    user = await db.users.find_one(
        {"user_id": user_id},
        {"_id": 0, "password_hash": 0}
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Get user's subscription history
    subscriptions = await db.subscriptions.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("created_at", -1).to_list(10)
    
    # Get user's quiz history
    quizzes = await db.quiz_attempts.find(
        {"user_id": user_id},
        {"_id": 0, "questions": 0}  # Exclude large questions array
    ).sort("created_at", -1).to_list(10)
    
    # Get user's progress
    progress = await db.lesson_progress.find(
        {"student_id": user_id},
        {"_id": 0}
    ).to_list(100)
    
    return {
        "user": user,
        "subscriptions": subscriptions,
        "recent_quizzes": quizzes,
        "progress": progress
    }


@router.post("/grant-access")
async def grant_manual_access(
    request: GrantAccessRequest,
    _: str = Depends(verify_admin_token)
):
    """
    Grant manual access to a user
    
    Creates user if doesn't exist, or updates existing user's subscription
    """
    email = request.email.lower()
    
    # Check if user exists
    user = await db.users.find_one({"email": email}, {"_id": 0})
    
    end_date = calculate_end_date(request.duration_months)
    
    if user:
        # Update existing user
        await db.users.update_one(
            {"email": email},
            {"$set": {
                "subscription_status": "active",
                "subscription_type": "manual",
                "subscription_plan": "monthly" if request.duration_months <= 1 else "semestral",
                "subscription_start": datetime.now(timezone.utc).isoformat(),
                "subscription_end": end_date.isoformat()
            }}
        )
        
        user_id = user["user_id"]
        action = "updated"
        logger.info(f"Manual access granted to existing user: {email}")
    else:
        # Create new user with manual access
        user_id = generate_user_id()
        name = request.name or email.split("@")[0]
        
        new_user = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": None,
            "auth_provider": "manual",  # Special provider for admin-created users
            "password_hash": None,
            "subscription_status": "active",
            "subscription_type": "manual",
            "subscription_plan": "monthly" if request.duration_months <= 1 else "semestral",
            "subscription_id": None,
            "subscription_start": datetime.now(timezone.utc).isoformat(),
            "subscription_end": end_date.isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.users.insert_one(new_user)
        action = "created"
        logger.info(f"Manual access granted to new user: {email}")
    
    # Create subscription record
    subscription_record = {
        "id": f"sub_manual_{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "user_email": email,
        "plan": "monthly" if request.duration_months <= 1 else "semestral",
        "subscription_type": "manual",
        "mercadopago_id": None,
        "amount": 0,  # Manual = free
        "currency": "CLP",
        "status": "active",
        "start_date": datetime.now(timezone.utc).isoformat(),
        "end_date": end_date.isoformat(),
        "granted_by": "admin",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.subscriptions.insert_one(subscription_record)
    
    return {
        "success": True,
        "action": action,
        "user_id": user_id,
        "email": email,
        "subscription_end": end_date.isoformat(),
        "message": f"Acceso otorgado por {request.duration_months} mes(es) hasta {end_date.strftime('%d/%m/%Y')}"
    }


@router.post("/{user_id}/revoke-access")
async def revoke_user_access(
    user_id: str,
    _: str = Depends(verify_admin_token)
):
    """Revoke a user's manual access"""
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Only allow revoking manual subscriptions
    if user.get("subscription_type") != "manual":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se puede revocar acceso manual. Para suscripciones de Mercado Pago, el usuario debe cancelar."
        )
    
    # Update user
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {
            "subscription_status": "cancelled",
            "subscription_end": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    # Update subscription record
    await db.subscriptions.update_one(
        {"user_id": user_id, "subscription_type": "manual", "status": "active"},
        {"$set": {
            "status": "cancelled",
            "cancelled_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    logger.info(f"Manual access revoked for user: {user['email']}")
    
    return {
        "success": True,
        "message": f"Acceso revocado para {user['email']}"
    }


@router.post("/{user_id}/extend-access")
async def extend_user_access(
    user_id: str,
    months: int = 1,
    _: str = Depends(verify_admin_token)
):
    """Extend a user's subscription by X months"""
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Calculate new end date
    current_end = user.get("subscription_end")
    if current_end:
        if isinstance(current_end, str):
            current_end = datetime.fromisoformat(current_end)
        if current_end.tzinfo is None:
            current_end = current_end.replace(tzinfo=timezone.utc)
        
        # If subscription hasn't expired, extend from current end
        if current_end > datetime.now(timezone.utc):
            new_end = current_end + timedelta(days=30 * months)
        else:
            new_end = calculate_end_date(months)
    else:
        new_end = calculate_end_date(months)
    
    # Update user
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {
            "subscription_status": "active",
            "subscription_end": new_end.isoformat()
        }}
    )
    
    logger.info(f"Access extended for user: {user['email']} until {new_end}")
    
    return {
        "success": True,
        "new_end_date": new_end.isoformat(),
        "message": f"Acceso extendido hasta {new_end.strftime('%d/%m/%Y')}"
    }
