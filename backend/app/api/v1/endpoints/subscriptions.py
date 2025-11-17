from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime
import uuid

from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_tenant
from app.models.user import User
from app.models.tenant import Tenant
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.plan import Plan
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionUpdate,
)
from app.services.stripe_service import StripeService

router = APIRouter()


@router.get("", response_model=List[SubscriptionResponse])
async def get_subscriptions(
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all subscriptions for current tenant
    """
    result = await db.execute(
        select(Subscription)
        .where(Subscription.tenant_id == current_tenant.id)
        .order_by(Subscription.created_at.desc())
    )
    subscriptions = result.scalars().all()
    return subscriptions


@router.get("/active", response_model=SubscriptionResponse)
async def get_active_subscription(
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Get active subscription for current tenant
    """
    result = await db.execute(
        select(Subscription)
        .where(
            Subscription.tenant_id == current_tenant.id,
            Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING])
        )
        .order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found",
        )
    
    return subscription


@router.post("", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    request: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new subscription for the current tenant
    """
    # Check if tenant already has an active subscription
    result = await db.execute(
        select(Subscription).where(
            Subscription.tenant_id == current_tenant.id,
            Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING])
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant already has an active subscription",
        )
    
    # Get plan
    result = await db.execute(select(Plan).where(Plan.id == request.plan_id))
    plan = result.scalar_one_or_none()
    
    if not plan or not plan.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found or inactive",
        )
    
    # Create subscription in database
    subscription = Subscription(
        id=uuid.uuid4(),
        tenant_id=current_tenant.id,
        plan_id=plan.id,
        status=SubscriptionStatus.TRIALING if plan.trial_days > 0 else SubscriptionStatus.ACTIVE,
        current_period_start=datetime.utcnow(),
        current_period_end=datetime.utcnow(),  # Will be updated by Stripe
    )
    
    # Create subscription in Stripe
    try:
        if not current_tenant.stripe_customer_id:
            # Create Stripe customer if doesn't exist
            stripe_customer = await StripeService.create_customer(
                tenant=current_tenant,
                email=current_tenant.email,
                name=current_tenant.name,
                metadata={"tenant_id": str(current_tenant.id)},
            )
            current_tenant.stripe_customer_id = stripe_customer.id
            await db.commit()
        
        # Create Stripe subscription
        stripe_subscription = await StripeService.create_subscription(
            customer_id=current_tenant.stripe_customer_id,
            price_id=plan.stripe_price_id,
            trial_days=plan.trial_days if plan.trial_days > 0 else None,
            payment_method_id=request.payment_method_id,
            metadata={
                "tenant_id": str(current_tenant.id),
                "subscription_id": str(subscription.id),
            },
        )
        
        subscription.stripe_subscription_id = stripe_subscription.id
        subscription.stripe_customer_id = current_tenant.stripe_customer_id
        subscription.current_period_start = datetime.fromtimestamp(
            stripe_subscription.current_period_start
        )
        subscription.current_period_end = datetime.fromtimestamp(
            stripe_subscription.current_period_end
        )
        
        if stripe_subscription.trial_start:
            subscription.trial_start = datetime.fromtimestamp(stripe_subscription.trial_start)
        if stripe_subscription.trial_end:
            subscription.trial_end = datetime.fromtimestamp(stripe_subscription.trial_end)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create subscription: {str(e)}",
        )
    
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    
    return subscription


@router.patch("/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: str,
    request: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a subscription (change plan, cancel, etc.)
    """
    result = await db.execute(
        select(Subscription).where(
            Subscription.id == subscription_id,
            Subscription.tenant_id == current_tenant.id,
        )
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found",
        )
    
    # Update in Stripe
    try:
        update_params = {}
        
        if request.plan_id:
            # Get new plan
            result = await db.execute(select(Plan).where(Plan.id == request.plan_id))
            new_plan = result.scalar_one_or_none()
            
            if not new_plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Plan not found",
                )
            
            update_params["price_id"] = new_plan.stripe_price_id
            subscription.plan_id = new_plan.id
        
        if request.cancel_at_period_end is not None:
            update_params["cancel_at_period_end"] = request.cancel_at_period_end
            subscription.cancel_at_period_end = request.cancel_at_period_end
        
        if subscription.stripe_subscription_id and update_params:
            await StripeService.update_subscription(
                subscription.stripe_subscription_id,
                **update_params,
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update subscription: {str(e)}",
        )
    
    await db.commit()
    await db.refresh(subscription)
    
    return subscription


@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_subscription(
    subscription_id: str,
    immediately: bool = False,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Cancel a subscription
    """
    result = await db.execute(
        select(Subscription).where(
            Subscription.id == subscription_id,
            Subscription.tenant_id == current_tenant.id,
        )
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found",
        )
    
    # Cancel in Stripe
    try:
        if subscription.stripe_subscription_id:
            await StripeService.cancel_subscription(
                subscription.stripe_subscription_id,
                immediately=immediately,
            )
        
        if immediately:
            subscription.status = SubscriptionStatus.CANCELED
            subscription.ended_at = datetime.utcnow()
        else:
            subscription.cancel_at_period_end = True
        
        subscription.canceled_at = datetime.utcnow()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel subscription: {str(e)}",
        )
    
    await db.commit()
