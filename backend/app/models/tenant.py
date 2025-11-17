from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base
from app.models.guid import GUID


class Tenant(Base):
    """
    Tenant model - represents a company/organization using the platform
    Each tenant has isolated data and billing
    """
    __tablename__ = "tenants"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    domain = Column(String(255), unique=True, nullable=True)  # Custom domain
    
    # Contact info
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    
    # Address
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_trial = Column(Boolean, default=True, nullable=False)
    trial_ends_at = Column(DateTime(timezone=True), nullable=True)
    
    # Stripe
    stripe_customer_id = Column(String(255), unique=True, nullable=True)
    
    # Database schema for multi-tenancy
    schema_name = Column(String(100), unique=True, nullable=False)
    
    # Metadata
    settings = Column(String, nullable=True)  # JSON field for tenant-specific settings
    max_users = Column(Integer, default=5, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="tenant", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="tenant", cascade="all, delete-orphan")
    usage_metrics = relationship("UsageMetric", back_populates="tenant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Tenant {self.name} ({self.slug})>"
