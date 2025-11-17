from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from typing import Optional


# Tenant Schemas
class TenantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class TenantCreate(TenantBase):
    slug: str = Field(..., min_length=3, max_length=100, pattern=r'^[a-z0-9-]+$')
    domain: Optional[str] = None


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = None


class TenantResponse(TenantBase):
    id: UUID4
    slug: str
    domain: Optional[str]
    is_active: bool
    is_trial: bool
    trial_ends_at: Optional[datetime]
    max_users: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
