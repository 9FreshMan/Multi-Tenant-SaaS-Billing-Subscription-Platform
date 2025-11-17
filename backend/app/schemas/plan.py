from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal
from app.models.plan import PlanTier, BillingInterval


# Plan Schemas
class PlanBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    tier: PlanTier
    price: Decimal = Field(..., ge=0)
    billing_interval: BillingInterval = BillingInterval.MONTHLY
    max_users: int = Field(default=5, ge=1)
    max_api_calls: int = Field(default=1000, ge=0)
    max_storage_gb: int = Field(default=5, ge=0)
    trial_days: int = Field(default=14, ge=0)


class PlanCreate(PlanBase):
    slug: str = Field(..., min_length=3, max_length=100, pattern=r'^[a-z0-9-]+$')
    features: Optional[Dict[str, Any]] = None


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    max_users: Optional[int] = None
    max_api_calls: Optional[int] = None
    max_storage_gb: Optional[int] = None
    features: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    trial_days: Optional[int] = None


class PlanResponse(PlanBase):
    id: UUID4
    slug: str
    features: Optional[Dict[str, Any]]
    is_active: bool
    is_public: bool
    sort_order: int
    stripe_price_id: Optional[str]
    stripe_product_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
