from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.plan import Plan
from app.schemas.plan import PlanResponse

router = APIRouter()


@router.get("", response_model=List[PlanResponse])
async def get_plans(
    include_inactive: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all available subscription plans
    Public endpoint - no authentication required
    """
    query = select(Plan).where(Plan.is_public)
    
    if not include_inactive:
        query = query.where(Plan.is_active)
    
    query = query.order_by(Plan.sort_order)
    
    result = await db.execute(query)
    plans = result.scalars().all()
    
    return plans


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific plan by ID
    """
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )
    
    return plan
