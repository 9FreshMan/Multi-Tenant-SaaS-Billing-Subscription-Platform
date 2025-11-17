from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Registration Schemas
class UserRegister(BaseModel):
    """Schema for user registration"""
    # Tenant info
    tenant_name: str = Field(..., min_length=2, max_length=100, description="Company/organization name")
    tenant_slug: str = Field(..., min_length=2, max_length=50, pattern="^[a-z0-9-]+$", description="Unique tenant identifier")
    
    # User info
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str


class TokenResponse(BaseModel):
    """Schema for token refresh response"""
    access_token: str
    token_type: str = "bearer"


# Password Reset Schemas
class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class PasswordChange(BaseModel):
    """Schema for password change"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
