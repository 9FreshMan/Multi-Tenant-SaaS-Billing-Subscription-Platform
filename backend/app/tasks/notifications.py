from datetime import datetime, timedelta
import logging

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.tenant import Tenant
from app.models.invoice import Invoice, InvoiceStatus
from app.services.email_service import email_service
from sqlalchemy import select

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.notifications.send_welcome_email")
def send_welcome_email(email: str, user_name: str, tenant_name: str = None):
    """Send welcome email to new user"""
    import asyncio
    asyncio.run(email_service.send_welcome_email(email, user_name, tenant_name))


@celery_app.task(name="app.tasks.notifications.send_subscription_email")
def send_subscription_email(email: str, plan_name: str, amount: float, trial_days: int = None):
    """Send subscription created email"""
    import asyncio
    asyncio.run(email_service.send_subscription_created(email, plan_name, amount, trial_days))


@celery_app.task(name="app.tasks.notifications.send_payment_success_email")
def send_payment_success_email(email: str, amount: float, invoice_url: str, next_billing: str):
    """Send payment success email"""
    import asyncio
    asyncio.run(email_service.send_payment_succeeded(email, amount, invoice_url, next_billing))


@celery_app.task(name="app.tasks.notifications.send_payment_failure_email")
def send_payment_failure_email(email: str, amount: float, retry_date: str, reason: str = None):
    """Send payment failure email"""
    import asyncio
    asyncio.run(email_service.send_payment_failed(email, amount, retry_date, reason))


@celery_app.task(name="app.tasks.notifications.send_payment_reminders")
def send_payment_reminders():
    """
    Send payment reminder emails for overdue invoices
    """
    import asyncio
    asyncio.run(_send_payment_reminders_async())


async def _send_payment_reminders_async():
    async with AsyncSessionLocal() as db:
        try:
            # Find overdue invoices
            result = await db.execute(
                select(Invoice).where(
                    Invoice.status == InvoiceStatus.OPEN,
                    Invoice.due_date <= datetime.utcnow(),
                )
            )
            invoices = result.scalars().all()
            
            logger.info(f"Found {len(invoices)} overdue invoices")
            
            for invoice in invoices:
                # Get tenant
                result = await db.execute(
                    select(Tenant).where(Tenant.id == invoice.tenant_id)
                )
                tenant = result.scalar_one_or_none()
                
                if tenant:
                    # Send email reminder
                    await send_email_reminder(tenant, invoice)
                    logger.info(f"Sent payment reminder to {tenant.email} for invoice {invoice.invoice_number}")
            
            logger.info("Payment reminders sent successfully")
            
        except Exception as e:
            logger.error(f"Error sending payment reminders: {e}", exc_info=True)


@celery_app.task(name="app.tasks.notifications.send_trial_expiry_warning")
def send_trial_expiry_warning():
    """
    Send warning emails to tenants with trials expiring soon
    """
    import asyncio
    asyncio.run(_send_trial_expiry_warning_async())


async def _send_trial_expiry_warning_async():
    async with AsyncSessionLocal() as db:
        try:
            # Find trials expiring in 3 days
            expiry_date = datetime.utcnow() + timedelta(days=3)
            
            result = await db.execute(
                select(Tenant).where(
                    Tenant.is_trial,
                    Tenant.trial_ends_at <= expiry_date,
                    Tenant.trial_ends_at > datetime.utcnow(),
                )
            )
            tenants = result.scalars().all()
            
            logger.info(f"Found {len(tenants)} tenants with trials expiring soon")
            
            for tenant in tenants:
                # Send trial expiry warning email
                await send_trial_warning_email(tenant)
                logger.info(f"Sent trial expiry warning to {tenant.email}")
            
            logger.info("Trial expiry warnings sent successfully")
            
        except Exception as e:
            logger.error(f"Error sending trial expiry warnings: {e}", exc_info=True)


@celery_app.task(name="app.tasks.notifications.send_invoice_email")
def send_invoice_email(invoice_id: str):
    """
    Send invoice email to tenant
    """
    import asyncio
    asyncio.run(_send_invoice_email_async(invoice_id))


async def _send_invoice_email_async(invoice_id: str):
    async with AsyncSessionLocal() as db:
        try:
            # Get invoice
            result = await db.execute(
                select(Invoice).where(Invoice.id == invoice_id)
            )
            invoice = result.scalar_one_or_none()
            
            if not invoice:
                logger.error(f"Invoice {invoice_id} not found")
                return
            
            # Get tenant
            result = await db.execute(
                select(Tenant).where(Tenant.id == invoice.tenant_id)
            )
            tenant = result.scalar_one_or_none()
            
            if tenant:
                # Send invoice email
                await send_invoice_notification(tenant, invoice)
                logger.info(f"Sent invoice email to {tenant.email}")
            
        except Exception as e:
            logger.error(f"Error sending invoice email: {e}", exc_info=True)


async def send_email_reminder(tenant: Tenant, invoice: Invoice):
    """
    Send payment reminder email
    """
    # Placeholder for email sending logic
    # Would integrate with SendGrid, AWS SES, etc.
    logger.info(f"Sending payment reminder to {tenant.email} for ${invoice.total}")


async def send_trial_warning_email(tenant: Tenant):
    """
    Send trial expiry warning email
    """
    # Placeholder for email sending logic
    logger.info(f"Sending trial warning to {tenant.email}")


async def send_invoice_notification(tenant: Tenant, invoice: Invoice):
    """
    Send new invoice notification email
    """
    # Placeholder for email sending logic
    logger.info(f"Sending invoice notification to {tenant.email}")
