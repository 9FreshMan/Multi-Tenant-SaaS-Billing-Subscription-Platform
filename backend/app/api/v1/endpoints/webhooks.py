from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.services.stripe_service import StripeService
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.invoice import Invoice, InvoiceStatus

router = APIRouter()


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Handle Stripe webhook events
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header",
        )
    
    try:
        event = StripeService.verify_webhook_signature(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
    # Handle different event types
    event_type = event["type"]
    event_data = event["data"]["object"]
    
    if event_type == "customer.subscription.created":
        await handle_subscription_created(event_data, db)
    
    elif event_type == "customer.subscription.updated":
        await handle_subscription_updated(event_data, db)
    
    elif event_type == "customer.subscription.deleted":
        await handle_subscription_deleted(event_data, db)
    
    elif event_type == "invoice.created":
        await handle_invoice_created(event_data, db)
    
    elif event_type == "invoice.paid":
        await handle_invoice_paid(event_data, db)
    
    elif event_type == "invoice.payment_failed":
        await handle_invoice_payment_failed(event_data, db)
    
    elif event_type == "payment_intent.succeeded":
        await handle_payment_succeeded(event_data, db)
    
    elif event_type == "payment_intent.payment_failed":
        await handle_payment_failed(event_data, db)
    
    return {"status": "success"}


async def handle_subscription_created(data: dict, db: AsyncSession):
    """Handle subscription.created event"""
    stripe_sub_id = data["id"]
    
    result = await db.execute(
        select(Subscription).where(Subscription.stripe_subscription_id == stripe_sub_id)
    )
    subscription = result.scalar_one_or_none()
    
    if subscription:
        subscription.status = SubscriptionStatus(data["status"])
        subscription.current_period_start = datetime.fromtimestamp(data["current_period_start"])
        subscription.current_period_end = datetime.fromtimestamp(data["current_period_end"])
        await db.commit()


async def handle_subscription_updated(data: dict, db: AsyncSession):
    """Handle subscription.updated event"""
    stripe_sub_id = data["id"]
    
    result = await db.execute(
        select(Subscription).where(Subscription.stripe_subscription_id == stripe_sub_id)
    )
    subscription = result.scalar_one_or_none()
    
    if subscription:
        subscription.status = SubscriptionStatus(data["status"])
        subscription.current_period_start = datetime.fromtimestamp(data["current_period_start"])
        subscription.current_period_end = datetime.fromtimestamp(data["current_period_end"])
        subscription.cancel_at_period_end = data.get("cancel_at_period_end", False)
        
        if data.get("canceled_at"):
            subscription.canceled_at = datetime.fromtimestamp(data["canceled_at"])
        
        await db.commit()


async def handle_subscription_deleted(data: dict, db: AsyncSession):
    """Handle subscription.deleted event"""
    stripe_sub_id = data["id"]
    
    result = await db.execute(
        select(Subscription).where(Subscription.stripe_subscription_id == stripe_sub_id)
    )
    subscription = result.scalar_one_or_none()
    
    if subscription:
        subscription.status = SubscriptionStatus.CANCELED
        subscription.ended_at = datetime.utcnow()
        await db.commit()


async def handle_invoice_created(data: dict, db: AsyncSession):
    """Handle invoice.created event"""
    # Invoice creation is typically handled by subscription creation
    pass


async def handle_invoice_paid(data: dict, db: AsyncSession):
    """Handle invoice.paid event"""
    stripe_invoice_id = data["id"]
    
    result = await db.execute(
        select(Invoice).where(Invoice.stripe_invoice_id == stripe_invoice_id)
    )
    invoice = result.scalar_one_or_none()
    
    if invoice:
        invoice.status = InvoiceStatus.PAID
        invoice.amount_paid = invoice.total
        invoice.paid_at = datetime.utcnow()
        await db.commit()


async def handle_invoice_payment_failed(data: dict, db: AsyncSession):
    """Handle invoice.payment_failed event"""
    stripe_invoice_id = data["id"]
    
    result = await db.execute(
        select(Invoice).where(Invoice.stripe_invoice_id == stripe_invoice_id)
    )
    invoice = result.scalar_one_or_none()
    
    if invoice:
        invoice.status = InvoiceStatus.UNCOLLECTIBLE
        await db.commit()


async def handle_payment_succeeded(data: dict, db: AsyncSession):
    """Handle payment_intent.succeeded event"""
    # Payment success tracking
    pass


async def handle_payment_failed(data: dict, db: AsyncSession):
    """Handle payment_intent.payment_failed event"""
    # Payment failure tracking
    pass
