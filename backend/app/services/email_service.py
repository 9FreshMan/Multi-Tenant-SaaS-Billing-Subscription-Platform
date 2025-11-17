"""Email notification service (stub implementation)"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications"""
    
    def __init__(self):
        """Initialize email service (stub)"""
        self.enabled = False
        logger.info("Email service initialized (stub mode)")
    
    async def send_welcome_email(
        self,
        to_email: str,
        user_name: str,
        tenant_name: Optional[str] = None
    ) -> bool:
        """Send welcome email to new user"""
        logger.info(
            f"📧 [STUB] Welcome email to {to_email} "
            f"(User: {user_name}, Tenant: {tenant_name})"
        )
        return True
    
    async def send_subscription_created(
        self,
        to_email: str,
        plan_name: str,
        amount: float,
        trial_days: Optional[int] = None
    ) -> bool:
        """Send email when subscription is created"""
        trial_msg = f" with {trial_days}-day trial" if trial_days else ""
        logger.info(
            f"📧 [STUB] Subscription created email to {to_email} "
            f"(Plan: {plan_name}, Amount: ${amount}{trial_msg})"
        )
        return True
    
    async def send_payment_succeeded(
        self,
        to_email: str,
        amount: float,
        invoice_url: str,
        next_billing_date: str
    ) -> bool:
        """Send email when payment is successful"""
        logger.info(
            f"📧 [STUB] Payment succeeded email to {to_email} "
            f"(Amount: ${amount}, Invoice: {invoice_url})"
        )
        return True
    
    async def send_payment_failed(
        self,
        to_email: str,
        amount: float,
        retry_date: str,
        reason: Optional[str] = None
    ) -> bool:
        """Send email when payment fails"""
        logger.info(
            f"📧 [STUB] Payment failed email to {to_email} "
            f"(Amount: ${amount}, Retry: {retry_date}, Reason: {reason})"
        )
        return True
    
    async def send_trial_ending_soon(
        self,
        to_email: str,
        days_remaining: int,
        plan_name: str,
        upgrade_url: str
    ) -> bool:
        """Send reminder when trial is ending"""
        logger.info(
            f"📧 [STUB] Trial ending email to {to_email} "
            f"({days_remaining} days left, Plan: {plan_name})"
        )
        return True
    
    async def send_subscription_canceled(
        self,
        to_email: str,
        plan_name: str,
        access_until: str
    ) -> bool:
        """Send email when subscription is canceled"""
        logger.info(
            f"📧 [STUB] Subscription canceled email to {to_email} "
            f"(Plan: {plan_name}, Access until: {access_until})"
        )
        return True
    
    async def send_invoice_generated(
        self,
        to_email: str,
        invoice_number: str,
        amount: float,
        due_date: str,
        pdf_url: Optional[str] = None
    ) -> bool:
        """Send invoice to customer"""
        logger.info(
            f"📧 [STUB] Invoice email to {to_email} "
            f"(#{invoice_number}, Amount: ${amount}, Due: {due_date})"
        )
        return True


# Singleton instance
email_service = EmailService()


# Template examples for future implementation
EMAIL_TEMPLATES = {
    "welcome": """
    <h1>Welcome to {app_name}! 🎉</h1>
    <p>Hi {user_name},</p>
    <p>Thank you for signing up. Your account has been created successfully.</p>
    <p>Tenant: <strong>{tenant_name}</strong></p>
    <a href="{dashboard_url}">Go to Dashboard</a>
    """,
    
    "subscription_created": """
    <h1>Subscription Activated! 🚀</h1>
    <p>Your {plan_name} subscription is now active.</p>
    <p>Amount: <strong>${amount}/month</strong></p>
    {trial_message}
    <a href="{billing_url}">Manage Subscription</a>
    """,
    
    "payment_succeeded": """
    <h1>Payment Received ✅</h1>
    <p>We've successfully charged ${amount} for your subscription.</p>
    <p>Next billing date: {next_billing_date}</p>
    <a href="{invoice_url}">View Invoice</a>
    """,
    
    "payment_failed": """
    <h1>Payment Failed ❌</h1>
    <p>We couldn't process your payment of ${amount}.</p>
    <p>Reason: {reason}</p>
    <p>We'll retry on {retry_date}. Please update your payment method.</p>
    <a href="{payment_methods_url}">Update Payment Method</a>
    """,
    
    "trial_ending": """
    <h1>Your Trial Ends in {days_remaining} Days ⏰</h1>
    <p>Your {plan_name} trial will expire soon.</p>
    <p>Add a payment method to continue using all features.</p>
    <a href="{upgrade_url}">Add Payment Method</a>
    """,
}
