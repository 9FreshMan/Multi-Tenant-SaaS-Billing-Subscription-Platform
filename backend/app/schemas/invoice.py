from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal
from app.models.invoice import InvoiceStatus


# Invoice Line Item Schema
class InvoiceLineItem(BaseModel):
    description: str
    amount: Decimal
    quantity: int = 1


# Invoice Schemas
class InvoiceBase(BaseModel):
    subscription_id: Optional[UUID4] = None
    invoice_date: datetime
    due_date: Optional[datetime] = None


class InvoiceCreate(InvoiceBase):
    line_items: List[InvoiceLineItem]
    tax: Decimal = Decimal("0")


class InvoiceResponse(InvoiceBase):
    id: UUID4
    tenant_id: UUID4
    invoice_number: str
    status: InvoiceStatus
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    amount_paid: Decimal
    amount_due: Decimal
    currency: str
    line_items: Optional[List[Dict[str, Any]]]
    stripe_invoice_id: Optional[str]
    invoice_pdf_url: Optional[str]
    paid_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
