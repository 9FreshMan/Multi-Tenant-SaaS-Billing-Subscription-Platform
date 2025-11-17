"""
Script to seed initial subscription plans
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.plan import Plan, PlanTier, BillingInterval
# Import all models to resolve relationships
from app.models import base  # noqa


async def seed_plans():
    """Seed initial subscription plans"""
    
    async with AsyncSessionLocal() as session:
        # Check if plans already exist
        result = await session.execute(select(Plan))
        existing_plans = result.scalars().all()
        
        if existing_plans:
            print(f"Plans already exist ({len(existing_plans)} plans found). Skipping seed.")
            return
        
        # Create plans
        plans = [
            Plan(
                name="Free",
                slug="free",
                tier=PlanTier.FREE,
                description="Perfect for getting started",
                price=0,
                billing_interval=BillingInterval.MONTHLY,
                max_users=5,
                max_api_calls=1000,
                max_storage_gb=5,
                features={
                    "features": [
                        "Up to 5 users",
                        "1,000 API calls per month",
                        "5 GB storage",
                        "Basic analytics",
                        "Community support"
                    ]
                },
                is_active=True,
                is_public=True,
                sort_order=1
            ),
            Plan(
                name="Pro",
                slug="pro",
                tier=PlanTier.PRO,
                description="For growing businesses",
                price=29.00,
                billing_interval=BillingInterval.MONTHLY,
                max_users=25,
                max_api_calls=10000,
                max_storage_gb=50,
                features={
                    "features": [
                        "Up to 25 users",
                        "10,000 API calls per month",
                        "50 GB storage",
                        "Advanced analytics",
                        "Priority support",
                        "Custom integrations",
                        "API access"
                    ]
                },
                is_active=True,
                is_public=True,
                sort_order=2
            ),
            Plan(
                name="Enterprise",
                slug="enterprise",
                tier=PlanTier.ENTERPRISE,
                description="For large organizations",
                price=99.00,
                billing_interval=BillingInterval.MONTHLY,
                max_users=999,
                max_api_calls=100000,
                max_storage_gb=500,
                features={
                    "features": [
                        "Unlimited users",
                        "100,000+ API calls per month",
                        "500 GB storage",
                        "Enterprise analytics",
                        "Dedicated support",
                        "Custom integrations",
                        "API access",
                        "SLA guarantee",
                        "Advanced security",
                        "White-label options"
                    ]
                },
                is_active=True,
                is_public=True,
                sort_order=3
            )
        ]
        
        # Add all plans
        session.add_all(plans)
        await session.commit()
        
        print(f"Successfully seeded {len(plans)} plans:")
        for plan in plans:
            print(f"  - {plan.name} (${plan.price}/month)")


if __name__ == "__main__":
    print("Seeding subscription plans...")
    asyncio.run(seed_plans())
    print("Done!")
