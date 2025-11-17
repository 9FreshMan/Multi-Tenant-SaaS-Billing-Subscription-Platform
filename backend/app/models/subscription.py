from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base
from app.models.guid import GUID


class SubscriptionStatus(str, enum.Enum):
    """Subscription status"""
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"


class Subscription(Base):
    """
    Subscription model - links tenants to plans
    Tracks subscription lifecycle and billing
    """
    __tablename__ = "subscriptions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID(), ForeignKey("tenants.id"), nullable=False, index=True)
    plan_id = Column(GUID(), ForeignKey("plans.id"), nullable=False, index=True)
    
    # Stripe
    stripe_subscription_id = Column(String(255), unique=True, nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    
    # Status
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.TRIALING, nullable=False, index=True)
    
    # Trial
    trial_start = Column(DateTime(timezone=True), nullable=True)
    trial_end = Column(DateTime(timezone=True), nullable=True)
    
    # Billing period
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    
    # Cancellation
    cancel_at_period_end = Column(Boolean, default=False, nullable=False)
    canceled_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    invoices = relationship("Invoice", back_populates="subscription")
    
    def __repr__(self):
        return f"<Subscription {self.id} - {self.status}>"
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is active"""
        return self.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]
    
    @property
    def is_trial(self) -> bool:
        """Check if subscription is in trial"""
        return self.status == SubscriptionStatus.TRIALING
