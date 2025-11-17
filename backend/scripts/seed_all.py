"""
Complete seed script: creates plans, subscriptions, and invoices
Run: docker-compose exec backend python scripts/seed_all.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import base  # Import all models
from app.core.database import get_db
from app.models.plan import Plan
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.invoice import Invoice, InvoiceStatus
from app.models.tenant import Tenant
from sqlalchemy import select
from datetime import datetime, timedelta
from decimal import Decimal
import uuid


async def seed_data():
    """Seed plans, subscriptions, and invoices"""
    async for db in get_db():
        try:
            # 1. Check/Create Plans
            print("📋 Checking plans...")
            result = await db.execute(select(Plan))
            plans = result.scalars().all()
            
            if not plans:
                print("  Creating plans...")
                free_plan = Plan(
                    id=uuid.uuid4(),
                    name="Free",
                    slug="free",
                    description="Basic plan for startups",
                    price_monthly=Decimal("0.00"),
                    price_yearly=Decimal("0.00"),
                    currency="usd",
                    features={"users": 5, "api_calls": 1000, "storage_gb": 5},
                    is_active=True
                )
                pro_plan = Plan(
                    id=uuid.uuid4(),
                    name="Pro",
                    slug="pro",
                    description="Professional plan",
                    price_monthly=Decimal("29.00"),
                    price_yearly=Decimal("290.00"),
                    currency="usd",
                    features={"users": 25, "api_calls": 10000, "storage_gb": 50},
                    is_active=True
                )
                db.add_all([free_plan, pro_plan])
                await db.commit()
                print(f"  ✓ Created 2 plans")
            else:
                print(f"  ✓ Found {len(plans)} existing plans")
            
            # Reload plans
            result = await db.execute(select(Plan))
            all_plans = result.scalars().all()
            pro_plan = next((p for p in all_plans if p.slug == "pro"), all_plans[0])
            
            # 2. Check tenants and create subscriptions
            print("\n👥 Checking tenants...")
            result = await db.execute(select(Tenant))
            tenants = result.scalars().all()
            
            if not tenants:
                print("  ❌ No tenants found. Register a user first!")
                return
            
            print(f"  ✓ Found {len(tenants)} tenants")
            
            # 3. Create subscriptions for tenants without one
            print("\n💳 Creating subscriptions...")
            sub_count = 0
            for tenant in tenants:
                result = await db.execute(
                    select(Subscription).where(Subscription.tenant_id == tenant.id)
                )
                existing_subs = result.scalars().all()
                
                if not existing_subs:
                    subscription = Subscription(
                        id=uuid.uuid4(),
                        tenant_id=tenant.id,
                        plan_id=pro_plan.id,
                        status=SubscriptionStatus.ACTIVE,
                        current_period_start=datetime.utcnow(),
                        current_period_end=datetime.utcnow() + timedelta(days=30),
                        cancel_at_period_end=False
                    )
                    db.add(subscription)
                    sub_count += 1
                    print(f"  ✓ Created Pro subscription for {tenant.name}")
            
            await db.commit()
            print(f"\n✅ Created {sub_count} subscriptions")
            
            # 4. Create invoices
            print("\n📄 Creating invoices...")
            invoice_count = 0
            
            result = await db.execute(select(Subscription))
            subscriptions = result.scalars().all()
            
            for subscription in subscriptions:
                # Create 3 past invoices
                for i in range(3):
                    invoice_date = datetime.utcnow() - timedelta(days=30 * (i + 1))
                    
                    invoice = Invoice(
                        id=uuid.uuid4(),
                        tenant_id=subscription.tenant_id,
                        subscription_id=subscription.id,
                        invoice_number=f"INV-{datetime.utcnow().year}-{str(invoice_count + 1).zfill(3)}",
                        status=InvoiceStatus.PAID,
                        subtotal=Decimal("29.00"),
                        tax=Decimal("0.00"),
                        total=Decimal("29.00"),
                        amount_paid=Decimal("29.00"),
                        amount_due=Decimal("0.00"),
                        currency="usd",
                        line_items=[
                            {
                                "description": "Pro Plan - Monthly Subscription",
                                "amount": 2900,
                                "quantity": 1
                            }
                        ],
                        invoice_date=invoice_date,
                        due_date=invoice_date + timedelta(days=14),
                        paid_at=invoice_date + timedelta(days=1)
                    )
                    
                    db.add(invoice)
                    invoice_count += 1
            
            await db.commit()
            print(f"\n✅ Created {invoice_count} invoices")
            
            # Show summary
            print("\n" + "="*50)
            print("📊 SEED SUMMARY")
            print("="*50)
            
            result = await db.execute(select(Invoice))
            all_invoices = result.scalars().all()
            print(f"\n📄 Invoice IDs (use these in frontend):")
            for inv in all_invoices[:5]:
                print(f"  • {inv.id}")
                print(f"    Number: {inv.invoice_number} | Status: {inv.status.value}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()
        finally:
            break


if __name__ == "__main__":
    print("🌱 SEEDING DATABASE...\n")
    asyncio.run(seed_data())
    print("\n✅ DONE!")
