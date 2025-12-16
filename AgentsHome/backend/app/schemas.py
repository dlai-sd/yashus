from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Auth
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: Optional[str] = None
    provider: str = "email"

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class SSOCallbackRequest(BaseModel):
    provider: str  # 'google', 'github', etc
    code: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class AuthResponse(BaseModel):
    token: str
    user: UserResponse

# Subscription
class SubscriptionBase(BaseModel):
    agent_id: str
    plan_tier: str

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionResponse(SubscriptionBase):
    id: str
    user_id: str
    status: str
    api_quota: int
    api_used: int
    renewal_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

# API Key
class APIKeyCreate(BaseModel):
    agent_id: str
    name: str = "API Key"

class APIKeyResponse(BaseModel):
    id: str
    agent_id: str
    name: str
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True

class APIKeyCreateResponse(APIKeyResponse):
    key: str  # Only returned on creation
