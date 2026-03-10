"""User and subscription models for Remy platform"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum
import uuid


class SubscriptionStatus(str, Enum):
    """Subscription status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PENDING = "pending"


class SubscriptionType(str, Enum):
    """Types of subscription"""
    MERCADOPAGO = "mercadopago"
    MANUAL = "manual"  # Granted by admin


class SubscriptionPlan(str, Enum):
    """Available subscription plans"""
    MONTHLY = "monthly"
    SEMESTRAL = "semestral"


class User(BaseModel):
    """Student user model"""
    model_config = ConfigDict(extra="ignore")
    
    user_id: str = Field(default_factory=lambda: f"user_{uuid.uuid4().hex[:12]}")
    email: str
    name: str
    picture: Optional[str] = None
    auth_provider: str = "email"  # "google" or "email"
    password_hash: Optional[str] = None  # Only for email auth
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Subscription info
    subscription_status: SubscriptionStatus = SubscriptionStatus.INACTIVE
    subscription_type: Optional[SubscriptionType] = None
    subscription_plan: Optional[SubscriptionPlan] = None
    subscription_id: Optional[str] = None  # Mercado Pago preapproval ID
    subscription_start: Optional[datetime] = None
    subscription_end: Optional[datetime] = None


class UserSession(BaseModel):
    """User session for authentication"""
    model_config = ConfigDict(extra="ignore")
    
    session_id: str = Field(default_factory=lambda: f"session_{uuid.uuid4().hex}")
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Subscription(BaseModel):
    """Subscription record"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: f"sub_{uuid.uuid4().hex[:12]}")
    user_id: str
    user_email: str
    plan: SubscriptionPlan
    subscription_type: SubscriptionType
    mercadopago_id: Optional[str] = None  # PreApproval ID from Mercado Pago
    amount: float
    currency: str = "CLP"
    status: SubscriptionStatus = SubscriptionStatus.PENDING
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_date: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Request/Response schemas
class RegisterRequest(BaseModel):
    """Email registration request"""
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=2)


class LoginRequest(BaseModel):
    """Email login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Authentication token response"""
    session_token: str
    user: dict


class UserResponse(BaseModel):
    """Public user response"""
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    subscription_status: SubscriptionStatus
    subscription_type: Optional[SubscriptionType] = None
    subscription_plan: Optional[SubscriptionPlan] = None
    subscription_end: Optional[datetime] = None


class GrantAccessRequest(BaseModel):
    """Admin request to grant manual access"""
    user_email: EmailStr
    user_name: Optional[str] = None
    duration_months: int = 1  # Default 1 month


class CreateSubscriptionRequest(BaseModel):
    """Request to create a subscription via Mercado Pago"""
    plan: SubscriptionPlan
    card_token: str
