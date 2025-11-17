from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from typing import Optional
from app.models.usage_metric import MetricType


# Usage Metric Schemas
class UsageMetricBase(BaseModel):
    metric_type: MetricType
    metric_name: str = Field(..., min_length=1, max_length=100)
    value: int = Field(..., ge=0)
    unit: str = Field(..., min_length=1, max_length=20)


class UsageMetricCreate(UsageMetricBase):
    period_start: datetime
    period_end: datetime
    metric_metadata: Optional[str] = None


class UsageMetricResponse(UsageMetricBase):
    id: UUID4
    tenant_id: UUID4
    period_start: datetime
    period_end: datetime
    metric_metadata: Optional[str]
    recorded_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# Usage Analytics Schemas
class UsageSummary(BaseModel):
    """Summary of usage for a tenant"""
    metric_type: MetricType
    total_usage: int
    unit: str
    period_start: datetime
    period_end: datetime


class TenantUsageStats(BaseModel):
    """Overall usage statistics for a tenant"""
    tenant_id: UUID4
    api_calls: int
    storage_gb: int
    bandwidth_mb: int
    active_users: int
    period_start: datetime
    period_end: datetime
