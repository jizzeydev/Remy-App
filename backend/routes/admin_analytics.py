"""
Admin Dashboard Analytics Routes for Remy Platform
Provides real business metrics: revenue, subscriptions, users, simulations
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from jose import JWTError, jwt
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/analytics", tags=["admin-analytics"])

# Security
security = HTTPBearer()

# MongoDB connection
db = None


def set_db(database):
    """Set database instance from main app"""
    global db
    db = database


# Allowed admin emails
ALLOWED_ADMIN_EMAILS = [
    'seremonta.cl@gmail.com',
    'admin@seremonta.cl'
]


async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify admin JWT token"""
    try:
        token = credentials.credentials
        secret_key = os.environ.get('ADMIN_SECRET_KEY')
        admin_username = os.environ.get('ADMIN_USERNAME')
        
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        subject: str = payload.get("sub")
        token_type: str = payload.get("type", "")
        
        if subject is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
        
        if token_type == "admin_google":
            if subject.lower() not in [e.lower() for e in ALLOWED_ADMIN_EMAILS]:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
            return subject
        
        if subject != admin_username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
        return subject
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def parse_date(date_str: str) -> datetime:
    """Parse various date formats"""
    if isinstance(date_str, datetime):
        return date_str
    
    try:
        # Try ISO format with timezone
        if '+' in date_str or 'Z' in date_str:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        # Try ISO format without timezone
        return datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
    except:
        return datetime.now(timezone.utc)


# ==================== DASHBOARD SUMMARY ====================

@router.get("/dashboard")
async def get_dashboard_metrics(_: str = Depends(verify_admin_token)):
    """Get complete dashboard metrics"""
    now = datetime.now(timezone.utc)
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    
    # ===== USER METRICS =====
    total_users = await db.users.count_documents({})
    
    # New users this month
    new_users_this_month = await db.users.count_documents({
        "created_at": {"$gte": this_month_start.isoformat()}
    })
    
    # New users last month (for comparison)
    new_users_last_month = await db.users.count_documents({
        "created_at": {
            "$gte": last_month_start.isoformat(),
            "$lt": this_month_start.isoformat()
        }
    })
    
    # Users with active trial
    trial_users = await db.users.count_documents({"trial_active": True})
    
    # ===== SUBSCRIPTION METRICS =====
    active_subscriptions = await db.users.count_documents({"subscription_status": "active"})
    
    # Subscriptions by type
    mp_subscriptions = await db.users.count_documents({
        "subscription_status": "active",
        "subscription_type": "mercadopago"
    })
    manual_subscriptions = await db.users.count_documents({
        "subscription_status": "active",
        "subscription_type": "manual"
    })
    
    # ===== REVENUE METRICS =====
    # Calculate from payments collection
    payments_cursor = db.payments.find({"status": "paid"}, {"_id": 0, "amount": 1, "created_at": 1})
    payments = await payments_cursor.to_list(10000)
    
    total_revenue = sum(p.get("amount", 0) for p in payments)
    
    # Revenue this month
    revenue_this_month = 0
    revenue_last_month = 0
    
    for payment in payments:
        payment_date = payment.get("created_at")
        if payment_date:
            try:
                pd = parse_date(payment_date)
                if pd >= this_month_start:
                    revenue_this_month += payment.get("amount", 0)
                elif pd >= last_month_start:
                    revenue_last_month += payment.get("amount", 0)
            except:
                pass
    
    # MRR (Monthly Recurring Revenue) - based on active subscriptions
    # Assuming average of $9,990 per monthly and $4,998 per semestral (29,990/6)
    mrr = (mp_subscriptions * 9990)  # Simplified - could be more precise with actual plan data
    
    # ===== SIMULATION METRICS =====
    total_simulations = await db.quiz_attempts.count_documents({})
    
    # Simulations this month
    simulations_this_month = await db.quiz_attempts.count_documents({
        "created_at": {"$gte": this_month_start.isoformat()}
    })
    
    # ===== CONTENT METRICS =====
    total_courses = await db.courses.count_documents({})
    total_lessons = await db.lessons.count_documents({})
    total_questions = await db.questions.count_documents({})
    
    # ===== UNIVERSITY CONTENT =====
    total_universities = await db.universities.count_documents({})
    total_uni_questions = await db.evaluation_questions.count_documents({})
    
    return {
        "users": {
            "total": total_users,
            "new_this_month": new_users_this_month,
            "new_last_month": new_users_last_month,
            "trial_active": trial_users,
            "growth_percent": round(((new_users_this_month - new_users_last_month) / max(new_users_last_month, 1)) * 100, 1)
        },
        "subscriptions": {
            "active": active_subscriptions,
            "mercadopago": mp_subscriptions,
            "manual": manual_subscriptions,
            "conversion_rate": round((active_subscriptions / max(total_users, 1)) * 100, 1)
        },
        "revenue": {
            "total": total_revenue,
            "this_month": revenue_this_month,
            "last_month": revenue_last_month,
            "mrr": mrr,
            "growth_percent": round(((revenue_this_month - revenue_last_month) / max(revenue_last_month, 1)) * 100, 1)
        },
        "simulations": {
            "total": total_simulations,
            "this_month": simulations_this_month
        },
        "content": {
            "courses": total_courses,
            "lessons": total_lessons,
            "questions": total_questions,
            "universities": total_universities,
            "university_questions": total_uni_questions
        }
    }


# ==================== REVENUE CHARTS ====================

@router.get("/revenue/chart")
async def get_revenue_chart(
    days: int = Query(default=30, ge=7, le=365),
    _: str = Depends(verify_admin_token)
):
    """Get revenue data for chart (last N days)"""
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)
    
    # Get all payments in range
    payments = await db.payments.find(
        {"status": "paid"},
        {"_id": 0, "amount": 1, "created_at": 1}
    ).to_list(10000)
    
    # Group by day
    daily_revenue = {}
    for i in range(days):
        day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        daily_revenue[day] = 0
    
    for payment in payments:
        try:
            pd = parse_date(payment.get("created_at", ""))
            if pd >= start_date:
                day = pd.strftime("%Y-%m-%d")
                if day in daily_revenue:
                    daily_revenue[day] += payment.get("amount", 0)
        except:
            pass
    
    # Convert to list format for charts
    chart_data = [
        {"date": day, "revenue": amount}
        for day, amount in sorted(daily_revenue.items())
    ]
    
    return {"data": chart_data, "period_days": days}


# ==================== USER GROWTH CHART ====================

@router.get("/users/chart")
async def get_users_chart(
    days: int = Query(default=30, ge=7, le=365),
    _: str = Depends(verify_admin_token)
):
    """Get user registration data for chart"""
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)
    
    # Get all users
    users = await db.users.find(
        {},
        {"_id": 0, "created_at": 1}
    ).to_list(100000)
    
    # Group by day
    daily_users = {}
    for i in range(days):
        day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        daily_users[day] = 0
    
    for user in users:
        try:
            created = user.get("created_at", "")
            if created:
                pd = parse_date(created)
                if pd >= start_date:
                    day = pd.strftime("%Y-%m-%d")
                    if day in daily_users:
                        daily_users[day] += 1
        except:
            pass
    
    # Calculate cumulative
    cumulative = 0
    # Count users before start_date
    for user in users:
        try:
            created = user.get("created_at", "")
            if created:
                pd = parse_date(created)
                if pd < start_date:
                    cumulative += 1
        except:
            pass
    
    chart_data = []
    for day, count in sorted(daily_users.items()):
        cumulative += count
        chart_data.append({
            "date": day,
            "new_users": count,
            "total_users": cumulative
        })
    
    return {"data": chart_data, "period_days": days}


# ==================== SIMULATIONS CHART ====================

@router.get("/simulations/chart")
async def get_simulations_chart(
    days: int = Query(default=30, ge=7, le=365),
    _: str = Depends(verify_admin_token)
):
    """Get simulations data for chart"""
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)
    
    # Get all quiz attempts
    quizzes = await db.quiz_attempts.find(
        {},
        {"_id": 0, "created_at": 1}
    ).to_list(100000)
    
    # Group by day
    daily_simulations = {}
    for i in range(days):
        day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        daily_simulations[day] = 0
    
    for quiz in quizzes:
        try:
            created = quiz.get("created_at", "")
            if created:
                pd = parse_date(created)
                if pd >= start_date:
                    day = pd.strftime("%Y-%m-%d")
                    if day in daily_simulations:
                        daily_simulations[day] += 1
        except:
            pass
    
    chart_data = [
        {"date": day, "simulations": count}
        for day, count in sorted(daily_simulations.items())
    ]
    
    return {"data": chart_data, "period_days": days}


# ==================== SUBSCRIPTION CHART ====================

@router.get("/subscriptions/chart")
async def get_subscriptions_chart(
    days: int = Query(default=30, ge=7, le=365),
    _: str = Depends(verify_admin_token)
):
    """Get subscription creation data for chart"""
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)
    
    # Get users with subscription_start
    users = await db.users.find(
        {"subscription_start": {"$exists": True, "$ne": None}},
        {"_id": 0, "subscription_start": 1, "subscription_type": 1}
    ).to_list(100000)
    
    # Group by day
    daily_subs = {}
    for i in range(days):
        day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        daily_subs[day] = {"mercadopago": 0, "manual": 0}
    
    for user in users:
        try:
            sub_start = user.get("subscription_start", "")
            if sub_start:
                pd = parse_date(sub_start)
                if pd >= start_date:
                    day = pd.strftime("%Y-%m-%d")
                    if day in daily_subs:
                        sub_type = user.get("subscription_type", "manual")
                        if sub_type in ["mercadopago", "manual"]:
                            daily_subs[day][sub_type] += 1
        except:
            pass
    
    chart_data = [
        {
            "date": day,
            "mercadopago": data["mercadopago"],
            "manual": data["manual"],
            "total": data["mercadopago"] + data["manual"]
        }
        for day, data in sorted(daily_subs.items())
    ]
    
    return {"data": chart_data, "period_days": days}


# ==================== RECENT ACTIVITY ====================

@router.get("/activity/recent")
async def get_recent_activity(
    limit: int = Query(default=20, ge=1, le=100),
    _: str = Depends(verify_admin_token)
):
    """Get recent platform activity"""
    activities = []
    
    # Recent user registrations
    recent_users = await db.users.find(
        {},
        {"_id": 0, "email": 1, "name": 1, "created_at": 1, "subscription_status": 1}
    ).sort("created_at", -1).limit(10).to_list(10)
    
    for user in recent_users:
        activities.append({
            "type": "user_registration",
            "email": user.get("email"),
            "name": user.get("name"),
            "timestamp": user.get("created_at"),
            "icon": "user_plus"
        })
    
    # Recent subscriptions
    recent_subs = await db.users.find(
        {"subscription_start": {"$exists": True, "$ne": None}},
        {"_id": 0, "email": 1, "name": 1, "subscription_start": 1, "subscription_plan": 1}
    ).sort("subscription_start", -1).limit(10).to_list(10)
    
    for sub in recent_subs:
        activities.append({
            "type": "subscription",
            "email": sub.get("email"),
            "name": sub.get("name"),
            "plan": sub.get("subscription_plan"),
            "timestamp": sub.get("subscription_start"),
            "icon": "credit_card"
        })
    
    # Recent simulations
    recent_quizzes = await db.quiz_attempts.find(
        {},
        {"_id": 0, "user_id": 1, "course_title": 1, "created_at": 1, "grade": 1}
    ).sort("created_at", -1).limit(10).to_list(10)
    
    for quiz in recent_quizzes:
        activities.append({
            "type": "simulation",
            "user_id": quiz.get("user_id"),
            "course": quiz.get("course_title"),
            "grade": quiz.get("grade"),
            "timestamp": quiz.get("created_at"),
            "icon": "clipboard"
        })
    
    # Sort all by timestamp
    activities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return activities[:limit]


# ==================== TOP CONTENT ====================

@router.get("/content/top")
async def get_top_content(_: str = Depends(verify_admin_token)):
    """Get most popular content"""
    # Most attempted courses (from quiz_attempts)
    pipeline = [
        {"$group": {"_id": "$course_title", "attempts": {"$sum": 1}}},
        {"$sort": {"attempts": -1}},
        {"$limit": 5}
    ]
    
    top_courses = []
    try:
        cursor = db.quiz_attempts.aggregate(pipeline)
        async for doc in cursor:
            if doc.get("_id"):
                top_courses.append({
                    "name": doc["_id"],
                    "attempts": doc["attempts"]
                })
    except:
        pass
    
    # Get courses with their lesson counts
    courses = await db.courses.find({}, {"_id": 0, "id": 1, "title": 1}).to_list(100)
    course_lessons = []
    for course in courses:
        lesson_count = await db.lessons.count_documents({"course_id": course["id"]})
        course_lessons.append({
            "name": course["title"],
            "lessons": lesson_count
        })
    course_lessons.sort(key=lambda x: x["lessons"], reverse=True)
    
    return {
        "top_attempted_courses": top_courses[:5],
        "courses_by_lessons": course_lessons[:5]
    }



# ==================== PLATFORM SETTINGS ====================

@router.get("/settings/trial")
async def get_trial_settings(_: str = Depends(verify_admin_token)):
    """Get current free trial settings"""
    settings = await db.platform_settings.find_one({"key": "free_trial"}, {"_id": 0})
    
    if not settings:
        # Default settings
        return {
            "enabled": True,
            "trial_days": 7,
            "simulations_limit": 10,
            "university_simulations_limit": 1
        }
    
    return settings.get("value", {})


@router.put("/settings/trial")
async def update_trial_settings(
    enabled: bool,
    trial_days: int = 7,
    simulations_limit: int = 10,
    university_simulations_limit: int = 1,
    _: str = Depends(verify_admin_token)
):
    """Update free trial settings"""
    settings = {
        "enabled": enabled,
        "trial_days": trial_days,
        "simulations_limit": simulations_limit,
        "university_simulations_limit": university_simulations_limit,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.platform_settings.update_one(
        {"key": "free_trial"},
        {"$set": {"key": "free_trial", "value": settings}},
        upsert=True
    )
    
    logger.info(f"Updated trial settings: enabled={enabled}, days={trial_days}")
    
    return {"success": True, "settings": settings}


# Public endpoint (no auth) for landing page
@router.get("/public/trial-status")
async def get_public_trial_status():
    """Get trial status for landing page (public endpoint)"""
    settings = await db.platform_settings.find_one({"key": "free_trial"}, {"_id": 0})
    
    if not settings:
        return {"enabled": True, "trial_days": 7}
    
    value = settings.get("value", {})
    return {
        "enabled": value.get("enabled", True),
        "trial_days": value.get("trial_days", 7)
    }
