from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base
from app.models.guid import GUID


class PaymentStatus(str, enum.Enum):
    """Payment status"""
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELED = "canceled"


class PaymentMethod(str, enum.Enum):
    """Payment method"""
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    OTHER = "other"


class Payment(Base):
    """
    Payment model - tracks payment transactions
    """
    __tablename__ = "payments"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(GUID(), ForeignKey("invoices.id"), nullable=False, index=True)
    
    # Stripe
    stripe_payment_intent_id = Column(String(255), unique=True, nullable=True)
    stripe_charge_id = Column(String(255), unique=True, nullable=True)
    
    # Payment details
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="usd", nullable=False)
    
    # Status
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False, index=True)
    
    # Method
    payment_method = Column(SQLEnum(PaymentMethod), default=PaymentMethod.CARD, nullable=False)
    
    # Card details (if applicable)
    card_last4 = Column(String(4), nullable=True)
    card_brand = Column(String(20), nullable=True)
    
    # Additional data
    payment_metadata = Column(JSON, nullable=True)
    
    # Failure
    failure_code = Column(String(100), nullable=True)
    failure_message = Column(String(500), nullable=True)
    
    # Dates
    paid_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment ${self.amount} - {self.status}>"
