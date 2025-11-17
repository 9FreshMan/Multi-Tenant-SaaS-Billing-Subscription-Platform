import stripe
from typing import Optional, Dict, Any
from decimal import Decimal

from app.core.config import settings
from app.models.tenant import Tenant

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Service for Stripe payment processing"""
    
    @staticmethod
    async def create_customer(
        tenant: Tenant,
        email: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> stripe.Customer:
        """Create a Stripe customer"""
        customer_data = {
            "email": email,
            "name": name,
            "metadata": metadata or {},
        }
        
        if tenant.address_line1:
            customer_data["address"] = {
                "line1": tenant.address_line1,
                "line2": tenant.address_line2,
                "city": tenant.city,
                "state": tenant.state,
                "postal_code": tenant.postal_code,
                "country": tenant.country,
            }
        
        customer = stripe.Customer.create(**customer_data)
        return customer
    
    @staticmethod
    async def create_product(
        name: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> stripe.Product:
        """Create a Stripe product"""
        product = stripe.Product.create(
            name=name,
            description=description,
            metadata=metadata or {},
        )
        return product
    
    @staticmethod
    async def create_price(
        product_id: str,
        amount: Decimal,
        currency: str = "usd",
        interval: str = "month",  # "month" or "year"
        metadata: Optional[Dict[str, Any]] = None,
    ) -> stripe.Price:
        """Create a Stripe price"""
        # Convert to cents
        amount_cents = int(amount * 100)
        
        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount_cents,
            currency=currency,
            recurring={"interval": interval},
            metadata=metadata or {},
        )
        return price
    
    @staticmethod
    async def create_subscription(
        customer_id: str,
        price_id: str,
        trial_days: Optional[int] = None,
        payment_method_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> stripe.Subscription:
        """Create a Stripe subscription"""
        subscription_data = {
            "customer": customer_id,
            "items": [{"price": price_id}],
            "metadata": metadata or {},
            "payment_behavior": "default_incomplete",
            "expand": ["latest_invoice.payment_intent"],
        }
        
        if trial_days and trial_days > 0:
            subscription_data["trial_period_days"] = trial_days
        
        if payment_method_id:
            subscription_data["default_payment_method"] = payment_method_id
        
        subscription = stripe.Subscription.create(**subscription_data)
        return subscription
    
    @staticmethod
    async def update_subscription(
        subscription_id: str,
        price_id: Optional[str] = None,
        cancel_at_period_end: Optional[bool] = None,
    ) -> stripe.Subscription:
        """Update a Stripe subscription"""
        update_data = {}
        
        if price_id:
            # Get current subscription to update items
            subscription = stripe.Subscription.retrieve(subscription_id)
            update_data["items"] = [
                {
                    "id": subscription["items"]["data"][0].id,
                    "price": price_id,
                }
            ]
        
        if cancel_at_period_end is not None:
            update_data["cancel_at_period_end"] = cancel_at_period_end
        
        subscription = stripe.Subscription.modify(subscription_id, **update_data)
        return subscription
    
    @staticmethod
    async def cancel_subscription(
        subscription_id: str,
        immediately: bool = False,
    ) -> stripe.Subscription:
        """Cancel a Stripe subscription"""
        if immediately:
            subscription = stripe.Subscription.delete(subscription_id)
        else:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True,
            )
        return subscription
    
    @staticmethod
    async def retrieve_subscription(subscription_id: str) -> stripe.Subscription:
        """Retrieve a Stripe subscription"""
        subscription = stripe.Subscription.retrieve(subscription_id)
        return subscription
    
    @staticmethod
    async def create_payment_intent(
        amount: Decimal,
        currency: str = "usd",
        customer_id: Optional[str] = None,
        payment_method_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> stripe.PaymentIntent:
        """Create a Stripe payment intent"""
        amount_cents = int(amount * 100)
        
        payment_intent_data = {
            "amount": amount_cents,
            "currency": currency,
            "metadata": metadata or {},
        }
        
        if customer_id:
            payment_intent_data["customer"] = customer_id
        
        if payment_method_id:
            payment_intent_data["payment_method"] = payment_method_id
            payment_intent_data["confirm"] = True
        
        payment_intent = stripe.PaymentIntent.create(**payment_intent_data)
        return payment_intent
    
    @staticmethod
    async def retrieve_invoice(invoice_id: str) -> stripe.Invoice:
        """Retrieve a Stripe invoice"""
        invoice = stripe.Invoice.retrieve(invoice_id)
        return invoice
    
    @staticmethod
    async def create_checkout_session(
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
        trial_days: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> stripe.checkout.Session:
        """Create a Stripe checkout session"""
        session_data = {
            "customer": customer_id,
            "mode": "subscription",
            "line_items": [{"price": price_id, "quantity": 1}],
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata": metadata or {},
        }
        
        if trial_days and trial_days > 0:
            session_data["subscription_data"] = {
                "trial_period_days": trial_days,
            }
        
        session = stripe.checkout.Session.create(**session_data)
        return session
    
    @staticmethod
    def verify_webhook_signature(
        payload: bytes,
        signature: str,
        secret: str,
    ) -> stripe.Event:
        """Verify Stripe webhook signature"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, secret
            )
            return event
        except ValueError:
            raise ValueError("Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise ValueError("Invalid signature")
