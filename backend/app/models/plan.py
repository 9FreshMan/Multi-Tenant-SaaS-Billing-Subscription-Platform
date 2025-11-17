from sqlalchemy import Column, String, Boolean, DateTime, Integer, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base
from app.models.guid import GUID


class PlanTier(str, enum.Enum):
    """Subscription plan tiers"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class BillingInterval(str, enum.Enum):
    """Billing intervals"""
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Plan(Base):
    """
    Subscription plan model
    Defines available subscription tiers and pricing
    """
    __tablename__ = "plans"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    
    # Plan details
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    tier = Column(SQLEnum(PlanTier), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    
    # Pricing
    price = Column(Numeric(10, 2), nullable=False)  # Price in USD
    billing_interval = Column(SQLEnum(BillingInterval), default=BillingInterval.MONTHLY, nullable=False)
    
    # Stripe
    stripe_price_id = Column(String(255), unique=True, nullable=True)
    stripe_product_id = Column(String(255), unique=True, nullable=True)
    
    # Features & Limits
    max_users = Column(Integer, default=5, nullable=False)
    max_api_calls = Column(Integer, default=1000, nullable=False)  # Per month
    max_storage_gb = Column(Integer, default=5, nullable=False)
    
    # Feature flags (JSON)
    features = Column(JSON, nullable=True)
    # Example: {"custom_domain": true, "priority_support": true, "advanced_analytics": false}
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)  # Visible to customers
    
    # Trial
    trial_days = Column(Integer, default=14, nullable=False)
    
    # Display order
    sort_order = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")
    
    def __repr__(self):
        return f"<Plan {self.name} (${self.price}/{self.billing_interval})>"
    
    @property
    def monthly_price(self) -> float:
        """Calculate monthly equivalent price"""
        if self.billing_interval == BillingInterval.YEARLY:
            return float(self.price) / 12
        return float(self.price)
