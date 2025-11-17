from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional
from app.models.subscription import SubscriptionStatus


# Subscription Schemas
class SubscriptionBase(BaseModel):
    plan_id: UUID4


class SubscriptionCreate(SubscriptionBase):
    payment_method_id: Optional[str] = None  # Stripe payment method ID


class SubscriptionUpdate(BaseModel):
    plan_id: Optional[UUID4] = None
    cancel_at_period_end: Optional[bool] = None


class SubscriptionResponse(SubscriptionBase):
    id: UUID4
    tenant_id: UUID4
    status: SubscriptionStatus
    stripe_subscription_id: Optional[str]
    trial_start: Optional[datetime]
    trial_end: Optional[datetime]
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    canceled_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class SubscriptionWithPlan(SubscriptionResponse):
    """Subscription response with nested plan details"""
    plan: dict  # PlanResponse
