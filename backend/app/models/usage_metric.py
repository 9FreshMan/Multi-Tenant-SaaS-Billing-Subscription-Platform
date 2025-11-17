from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base
from app.models.guid import GUID


class MetricType(str, enum.Enum):
    """Usage metric types"""
    API_CALLS = "api_calls"
    STORAGE = "storage"
    BANDWIDTH = "bandwidth"
    USERS = "users"
    CUSTOM = "custom"


class UsageMetric(Base):
    """
    Usage metric model - tracks resource consumption for usage-based billing
    """
    __tablename__ = "usage_metrics"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID(), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Metric details
    metric_type = Column(SQLEnum(MetricType), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    
    # Value
    value = Column(Integer, nullable=False)  # Actual usage amount
    unit = Column(String(20), nullable=False)  # e.g., "calls", "GB", "MB"
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Additional data
    metric_metadata = Column(String, nullable=True)  # JSON for additional context
    
    # Timestamps
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="usage_metrics")
    
    def __repr__(self):
        return f"<UsageMetric {self.metric_type}: {self.value} {self.unit}>"
