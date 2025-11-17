"""
Seed script to create sample invoices for testing PDF generation
Run: docker-compose exec backend python scripts/seed_invoices.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all models first to ensure relationships are loaded
from app.models import base  # This imports all models
from app.core.database import get_db
from app.models.invoice import Invoice, InvoiceStatus
from app.models.subscription import Subscription
from app.models.user import User
from app.models.tenant import Tenant
from sqlalchemy import select
from datetime import datetime, timedelta
from decimal import Decimal
import uuid


async def create_sample_invoices():
    """Create sample invoices for existing tenants"""
    async for db in get_db():
        try:
            # Find existing tenants and users
            result = await db.execute(select(Tenant).limit(5))
            tenants = result.scalars().all()
            
            if not tenants:
                print("❌ No tenants found. Please create a tenant first (register a user).")
                return
            
            print(f"✓ Found {len(tenants)} tenants")
            
            invoice_count = 0
            for tenant in tenants:
                # Find subscriptions for this tenant
                sub_result = await db.execute(
                    select(Subscription).where(Subscription.tenant_id == tenant.id)
                )
                subscriptions = sub_result.scalars().all()
                
                if not subscriptions:
                    print(f"  ⚠ Tenant {tenant.name} has no subscriptions, skipping")
                    continue
                
                subscription = subscriptions[0]
                
                # Create 3 invoices for this tenant
                for i in range(3):
                    invoice_date = datetime.utcnow() - timedelta(days=30 * i)
                    
                    invoice = Invoice(
                        id=uuid.uuid4(),
                        tenant_id=tenant.id,
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
                                "amount": 2900,  # in cents
                                "quantity": 1
                            }
                        ],
                        invoice_date=invoice_date,
                        due_date=invoice_date + timedelta(days=14),
                        paid_at=invoice_date + timedelta(days=1)
                    )
                    
                    db.add(invoice)
                    invoice_count += 1
                    print(f"  ✓ Created invoice {invoice.invoice_number} for {tenant.name}")
            
            await db.commit()
            print(f"\n✅ Successfully created {invoice_count} sample invoices!")
            
            # Show invoice IDs for testing
            result = await db.execute(select(Invoice).limit(5))
            invoices = result.scalars().all()
            print("\n📄 Sample Invoice IDs for testing:")
            for inv in invoices:
                print(f"  - {inv.id} | {inv.invoice_number} | Status: {inv.status}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await db.rollback()
            raise
        finally:
            break  # Exit after first db session


if __name__ == "__main__":
    print("🌱 Seeding sample invoices...\n")
    asyncio.run(create_sample_invoices())
