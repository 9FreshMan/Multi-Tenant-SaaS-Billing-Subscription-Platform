from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal
from app.models.payment import PaymentStatus, PaymentMethod


# Payment Schemas
class PaymentResponse(BaseModel):
    id: UUID4
    invoice_id: UUID4
    amount: Decimal
    currency: str
    status: PaymentStatus
    payment_method: PaymentMethod
    card_last4: Optional[str]
    card_brand: Optional[str]
    stripe_payment_intent_id: Optional[str]
    stripe_charge_id: Optional[str]
    payment_metadata: Optional[Dict[str, Any]]
    failure_code: Optional[str]
    failure_message: Optional[str]
    paid_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
