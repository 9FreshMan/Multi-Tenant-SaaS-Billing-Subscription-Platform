from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.MEMBER


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None


class UserUpdateRole(BaseModel):
    role: UserRole


class UserResponse(UserBase):
    id: UUID4
    tenant_id: UUID4
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    tenant_name: str = Field(..., min_length=1, max_length=255)
    tenant_slug: str = Field(..., min_length=3, max_length=100, pattern=r'^[a-z0-9-]+$')
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
