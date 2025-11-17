from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base
from app.models.guid import GUID


class UserRole(str, enum.Enum):
    """User roles for RBAC"""
    OWNER = "owner"  # Tenant owner, full access
    ADMIN = "admin"  # Administrator, almost full access
    MANAGER = "manager"  # Can manage subscriptions and billing
    MEMBER = "member"  # Regular user, limited access
    VIEWER = "viewer"  # Read-only access


class User(Base):
    """
    User model - platform users belonging to tenants
    Implements role-based access control
    """
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID(), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Role & Permissions
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Session
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    
    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def has_permission(self, required_role: UserRole) -> bool:
        """Check if user has required permission level"""
        role_hierarchy = {
            UserRole.VIEWER: 1,
            UserRole.MEMBER: 2,
            UserRole.MANAGER: 3,
            UserRole.ADMIN: 4,
            UserRole.OWNER: 5,
        }
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)
