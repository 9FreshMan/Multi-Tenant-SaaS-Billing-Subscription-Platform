from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime, timedelta
import uuid

from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_tenant
from app.models.user import User
from app.models.tenant import Tenant
from app.models.usage_metric import UsageMetric, MetricType
from app.schemas.usage_metric import (
    UsageMetricCreate,
    UsageMetricResponse,
    UsageSummary,
    TenantUsageStats,
)

router = APIRouter()


@router.post("", response_model=UsageMetricResponse, status_code=status.HTTP_201_CREATED)
async def record_usage(
    request: UsageMetricCreate,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Record a usage metric for the current tenant
    """
    metric = UsageMetric(
        id=uuid.uuid4(),
        tenant_id=current_tenant.id,
        metric_type=request.metric_type,
        metric_name=request.metric_name,
        value=request.value,
        unit=request.unit,
        period_start=request.period_start,
        period_end=request.period_end,
        metadata=request.metadata,
    )
    
    db.add(metric)
    await db.commit()
    await db.refresh(metric)
    
    return metric


@router.get("/metrics", response_model=List[UsageMetricResponse])
async def get_usage_metrics(
    metric_type: MetricType = None,
    start_date: datetime = None,
    end_date: datetime = None,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Get usage metrics for current tenant
    """
    query = select(UsageMetric).where(UsageMetric.tenant_id == current_tenant.id)
    
    if metric_type:
        query = query.where(UsageMetric.metric_type == metric_type)
    
    if start_date:
        query = query.where(UsageMetric.period_start >= start_date)
    
    if end_date:
        query = query.where(UsageMetric.period_end <= end_date)
    
    query = query.order_by(UsageMetric.recorded_at.desc())
    
    result = await db.execute(query)
    metrics = result.scalars().all()
    
    return metrics


@router.get("/summary", response_model=List[UsageSummary])
async def get_usage_summary(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Get usage summary for the last N days
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    end_date = datetime.utcnow()
    
    # Aggregate usage by metric type
    summaries = []
    
    for metric_type in MetricType:
        result = await db.execute(
            select(
                UsageMetric.metric_type,
                func.sum(UsageMetric.value).label("total_usage"),
                UsageMetric.unit,
            )
            .where(
                UsageMetric.tenant_id == current_tenant.id,
                UsageMetric.metric_type == metric_type,
                UsageMetric.period_start >= start_date,
            )
            .group_by(UsageMetric.metric_type, UsageMetric.unit)
        )
        
        row = result.first()
        if row and row.total_usage:
            summaries.append(
                UsageSummary(
                    metric_type=row.metric_type,
                    total_usage=int(row.total_usage),
                    unit=row.unit,
                    period_start=start_date,
                    period_end=end_date,
                )
            )
    
    return summaries


@router.get("/stats", response_model=TenantUsageStats)
async def get_usage_stats(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Get comprehensive usage statistics
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    end_date = datetime.utcnow()
    
    # Helper function to get metric sum
    async def get_metric_sum(metric_type: MetricType) -> int:
        result = await db.execute(
            select(func.sum(UsageMetric.value))
            .where(
                UsageMetric.tenant_id == current_tenant.id,
                UsageMetric.metric_type == metric_type,
                UsageMetric.period_start >= start_date,
            )
        )
        total = result.scalar()
        return int(total) if total else 0
    
    # Get totals for each metric type
    api_calls = await get_metric_sum(MetricType.API_CALLS)
    storage_gb = await get_metric_sum(MetricType.STORAGE)
    bandwidth_mb = await get_metric_sum(MetricType.BANDWIDTH)
    active_users = await get_metric_sum(MetricType.USERS)
    
    return TenantUsageStats(
        tenant_id=current_tenant.id,
        api_calls=api_calls,
        storage_gb=storage_gb,
        bandwidth_mb=bandwidth_mb,
        active_users=active_users,
        period_start=start_date,
        period_end=end_date,
    )
