from datetime import datetime
import logging

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.tenant import Tenant
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.invoice import Invoice
from sqlalchemy import select

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.billing.check_trial_expiration")
def check_trial_expiration():
    """
    Check for expired trials and update tenant status
    """
    import asyncio
    asyncio.run(_check_trial_expiration_async())


async def _check_trial_expiration_async():
    async with AsyncSessionLocal() as db:
        try:
            # Find tenants with expired trials
            result = await db.execute(
                select(Tenant).where(
                    Tenant.is_trial,
                    Tenant.trial_ends_at <= datetime.utcnow(),
                )
            )
            tenants = result.scalars().all()
            
            logger.info(f"Found {len(tenants)} tenants with expired trials")
            
            for tenant in tenants:
                # Check if they have an active subscription
                result = await db.execute(
                    select(Subscription).where(
                        Subscription.tenant_id == tenant.id,
                        Subscription.status == SubscriptionStatus.ACTIVE,
                    )
                )
                subscription = result.scalar_one_or_none()
                
                if subscription:
                    # Has paid subscription, remove trial status
                    tenant.is_trial = False
                else:
                    # No paid subscription, deactivate
                    tenant.is_active = False
                    logger.info(f"Deactivated tenant {tenant.slug} - trial expired")
            
            await db.commit()
            logger.info("Trial expiration check completed")
            
        except Exception as e:
            logger.error(f"Error checking trial expiration: {e}", exc_info=True)
            await db.rollback()


@celery_app.task(name="app.tasks.billing.generate_monthly_invoices")
def generate_monthly_invoices():
    """
    Generate monthly invoices for active subscriptions
    """
    import asyncio
    asyncio.run(_generate_monthly_invoices_async())


async def _generate_monthly_invoices_async():
    async with AsyncSessionLocal() as db:
        try:
            # Find subscriptions due for billing
            
            result = await db.execute(
                select(Subscription).where(
                    Subscription.status == SubscriptionStatus.ACTIVE,
                    Subscription.current_period_end <= datetime.utcnow(),
                )
            )
            subscriptions = result.scalars().all()
            
            logger.info(f"Found {len(subscriptions)} subscriptions due for billing")
            
            for subscription in subscriptions:
                # Check if invoice already exists
                result = await db.execute(
                    select(Invoice).where(
                        Invoice.subscription_id == subscription.id,
                        Invoice.invoice_date >= subscription.current_period_start,
                    )
                )
                existing_invoice = result.scalar_one_or_none()
                
                if existing_invoice:
                    logger.info(f"Invoice already exists for subscription {subscription.id}")
                    continue
                
                # Invoice generation would be handled by Stripe webhooks
                # This is a placeholder for custom logic
                logger.info(f"Would generate invoice for subscription {subscription.id}")
            
            await db.commit()
            logger.info("Monthly invoice generation completed")
            
        except Exception as e:
            logger.error(f"Error generating monthly invoices: {e}", exc_info=True)
            await db.rollback()


@celery_app.task(name="app.tasks.billing.calculate_usage_metrics")
def calculate_usage_metrics():
    """
    Calculate and aggregate usage metrics for all tenants
    """
    import asyncio
    asyncio.run(_calculate_usage_metrics_async())


async def _calculate_usage_metrics_async():
    async with AsyncSessionLocal() as db:
        try:
            # Find active tenants
            result = await db.execute(
                select(Tenant).where(Tenant.is_active)
            )
            tenants = result.scalars().all()
            
            logger.info(f"Calculating usage metrics for {len(tenants)} tenants")
            
            for tenant in tenants:
                # Placeholder for actual usage calculation
                # This would integrate with your actual service metrics
                logger.debug(f"Calculating usage for tenant {tenant.slug}")
            
            await db.commit()
            logger.info("Usage metrics calculation completed")
            
        except Exception as e:
            logger.error(f"Error calculating usage metrics: {e}", exc_info=True)
            await db.rollback()


@celery_app.task(name="app.tasks.billing.process_failed_payments")
def process_failed_payments():
    """
    Retry failed payments and update subscription status
    """
    import asyncio
    asyncio.run(_process_failed_payments_async())


async def _process_failed_payments_async():
    async with AsyncSessionLocal() as db:
        try:
            # Find subscriptions with payment issues
            result = await db.execute(
                select(Subscription).where(
                    Subscription.status == SubscriptionStatus.PAST_DUE,
                )
            )
            subscriptions = result.scalars().all()
            
            logger.info(f"Found {len(subscriptions)} subscriptions with failed payments")
            
            for subscription in subscriptions:
                # Retry payment logic would go here
                # This is typically handled by Stripe
                logger.info(f"Processing failed payment for subscription {subscription.id}")
            
            await db.commit()
            logger.info("Failed payment processing completed")
            
        except Exception as e:
            logger.error(f"Error processing failed payments: {e}", exc_info=True)
            await db.rollback()
