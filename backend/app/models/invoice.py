from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base
from app.models.guid import GUID


class InvoiceStatus(str, enum.Enum):
    """Invoice status"""
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    VOID = "void"
    UNCOLLECTIBLE = "uncollectible"


class Invoice(Base):
    """
    Invoice model - billing invoices for subscriptions
    """
    __tablename__ = "invoices"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID(), ForeignKey("tenants.id"), nullable=False, index=True)
    subscription_id = Column(GUID(), ForeignKey("subscriptions.id"), nullable=True, index=True)
    
    # Invoice details
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Stripe
    stripe_invoice_id = Column(String(255), unique=True, nullable=True)
    
    # Status
    status = Column(SQLEnum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False, index=True)
    
    # Amounts (in cents)
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), default=0, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    amount_paid = Column(Numeric(10, 2), default=0, nullable=False)
    amount_due = Column(Numeric(10, 2), nullable=False)
    
    # Currency
    currency = Column(String(3), default="usd", nullable=False)
    
    # Line items (JSON)
    line_items = Column(JSON, nullable=True)
    # Example: [{"description": "Pro Plan", "amount": 2900, "quantity": 1}]
    
    # Dates
    invoice_date = Column(DateTime(timezone=True), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    
    # PDF
    invoice_pdf_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="invoices")
    subscription = relationship("Subscription", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice")
    
    def __repr__(self):
        return f"<Invoice {self.invoice_number} - ${self.total} ({self.status})>"
