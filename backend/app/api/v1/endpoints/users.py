from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_tenant, require_role
from app.models.user import User, UserRole
from app.models.tenant import Tenant
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user information
    """
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update current user profile
    """
    if request.first_name:
        current_user.first_name = request.first_name
    if request.last_name:
        current_user.last_name = request.last_name
    if request.phone:
        current_user.phone = request.phone
    if request.avatar_url:
        current_user.avatar_url = request.avatar_url
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.get("", response_model=List[UserResponse])
async def get_users(
    current_user: User = Depends(require_role(UserRole.MANAGER)),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all users in the current tenant
    Requires MANAGER role or higher
    """
    result = await db.execute(
        select(User).where(User.tenant_id == current_tenant.id)
    )
    users = result.scalars().all()
    return users
