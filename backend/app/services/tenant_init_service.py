"""
Helper service to create initial data for new tenants
"""
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.plan import Plan, PlanTier, BillingInterval
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.invoice import Invoice, InvoiceStatus
from app.models.tenant import Tenant


async def create_initial_tenant_data(db: AsyncSession, tenant: Tenant):
    """
    Create initial subscription and sample invoices for a new tenant
    
    Args:
        db: Database session
        tenant: The newly created tenant
    """
    # 1. Get or create Pro plan
    result = await db.execute(select(Plan).where(Plan.slug == "pro"))
    pro_plan = result.scalar_one_or_none()
    
    if not pro_plan:
        # Create Pro plan if it doesn't exist
        pro_plan = Plan(
            id=uuid.uuid4(),
            name="Pro",
            slug="pro",
            tier=PlanTier.PRO,
            description="Professional plan for growing businesses",
            price=Decimal("29.00"),
            billing_interval=BillingInterval.MONTHLY,
            max_users=25,
            max_api_calls=10000,
            max_storage_gb=50,
            features={
                "api_calls": 10000,
                "storage_gb": 50,
                "users": 25,
                "priority_support": True,
                "analytics": True
            },
            is_active=True,
            is_public=True,
            trial_days=14,
            sort_order=2
        )
        db.add(pro_plan)
        await db.flush()  # Flush to get the ID
    
    # 2. Create subscription for the tenant
    subscription = Subscription(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        plan_id=pro_plan.id,
        status=SubscriptionStatus.TRIALING if tenant.is_trial else SubscriptionStatus.ACTIVE,
        trial_start=datetime.utcnow() if tenant.is_trial else None,
        trial_end=tenant.trial_ends_at if tenant.is_trial else None,
        current_period_start=datetime.utcnow(),
        current_period_end=datetime.utcnow() + timedelta(days=30),
        cancel_at_period_end=False
    )
    db.add(subscription)
    await db.flush()
    
    # 3. Create 3 sample invoices (historical)
    invoices = []
    for i in range(3):
        invoice_date = datetime.utcnow() - timedelta(days=30 * (i + 1))
        
        invoice = Invoice(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            subscription_id=subscription.id,
            invoice_number=f"INV-{datetime.utcnow().year}-{tenant.slug.upper()}-{str(i + 1).zfill(3)}",
            status=InvoiceStatus.PAID,
            subtotal=Decimal("29.00"),
            tax=Decimal("0.00"),
            total=Decimal("29.00"),
            amount_paid=Decimal("29.00"),
            amount_due=Decimal("0.00"),
            currency="usd",
            line_items=[
                {
                    "description": f"{pro_plan.name} Plan - Monthly Subscription",
                    "amount": 2900,  # in cents
                    "quantity": 1
                }
            ],
            invoice_date=invoice_date,
            due_date=invoice_date + timedelta(days=14),
            paid_at=invoice_date + timedelta(days=1)
        )
        invoices.append(invoice)
    
    db.add_all(invoices)
    
    # Commit is handled by the caller (register endpoint)
    return {
        "subscription": subscription,
        "invoices": invoices
    }
