from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import uuid

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
from app.models.user import User, UserRole
from app.models.tenant import Tenant
from app.schemas.user import (
    LoginRequest,
    RegisterRequest,
    Token,
)
from app.services.stripe_service import StripeService
from app.services.tenant_init_service import create_initial_tenant_data

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new tenant and owner user
    Creates both tenant and first user (owner)
    """
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == request.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Check if tenant slug already exists
    result = await db.execute(select(Tenant).where(Tenant.slug == request.tenant_slug))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant slug already taken",
        )
    
    # Create tenant
    tenant = Tenant(
        id=uuid.uuid4(),
        name=request.tenant_name,
        slug=request.tenant_slug,
        email=request.email,
        schema_name=f"tenant_{request.tenant_slug}",
        is_trial=True,
        trial_ends_at=datetime.utcnow() + timedelta(days=14),
    )
    
    # Create Stripe customer for tenant
    try:
        stripe_customer = await StripeService.create_customer(
            tenant=tenant,
            email=request.email,
            name=request.tenant_name,
            metadata={"tenant_id": str(tenant.id), "tenant_slug": tenant.slug},
        )
        tenant.stripe_customer_id = stripe_customer.id
    except Exception as e:
        # Log error but continue (Stripe is optional for trial)
        print(f"Failed to create Stripe customer: {e}")
    
    db.add(tenant)
    
    # Create owner user
    user = User(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email=request.email,
        hashed_password=get_password_hash(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
        role=UserRole.OWNER,
        is_active=True,
        is_verified=False,
    )
    db.add(user)
    
    # Create initial subscription and invoices for the tenant
    try:
        await create_initial_tenant_data(db, tenant)
    except Exception as e:
        # Log error but continue (user can still use the platform)
        print(f"Failed to create initial tenant data: {e}")
    
    await db.commit()
    await db.refresh(user)
    
    # Create tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Login with email and password
    Returns access and refresh tokens
    """
    # Find user by email
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    await db.commit()
    
    # Create tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Refresh access token using refresh token
    """
    from app.core.security import decode_token
    
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # Create new tokens
    new_access_token = create_access_token({"sub": str(user.id)})
    new_refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )
