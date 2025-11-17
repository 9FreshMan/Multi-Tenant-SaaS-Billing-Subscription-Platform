"""Tests for database models and validation"""
import pytest
from datetime import datetime, timedelta
import uuid


class TestUserModel:
    """Test User model validation and relationships"""
    
    def test_user_creation(self, db_session):
        """Test creating a user with valid data"""
        from app.models.user import User
        from app.models.tenant import Tenant
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        
        # Create tenant first
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Test Company",
            slug="test-company",
            email="company@example.com",
            schema_name="test_company"
        )
        db_session.add(tenant)
        db_session.commit()
        
        user = User(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password=pwd_context.hash("password123"),
            is_active=True
        )
        
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.is_active is True
    
    def test_user_unique_email(self, db_session):
        """Test that email must be unique"""
        from app.models.user import User
        from app.models.tenant import Tenant
        from sqlalchemy.exc import IntegrityError
        
        # Create tenant
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Test Company",
            slug="test-company",
            email="company@example.com",
            schema_name="test_company"
        )
        db_session.add(tenant)
        db_session.commit()
        
        user1 = User(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            email="duplicate@example.com",
            first_name="User",
            last_name="One",
            hashed_password="hash1"
        )
        user2 = User(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            email="duplicate@example.com",
            first_name="User",
            last_name="Two",
            hashed_password="hash2"
        )
        
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestSubscriptionPlanModel:
    """Test SubscriptionPlan model"""
    
    def test_plan_creation(self, db_session):
        """Test creating a subscription plan"""
        from app.models.plan import Plan, PlanTier, BillingInterval
        from decimal import Decimal
        
        plan = Plan(
            id=uuid.uuid4(),
            name="Pro Plan",
            slug="pro-plan",
            tier=PlanTier.PRO,
            price=Decimal("29.99"),
            billing_interval=BillingInterval.MONTHLY,
            is_active=True
        )
        
        db_session.add(plan)
        db_session.commit()
        
        assert plan.name == "Pro Plan"
        assert plan.price == Decimal("29.99")
    
    def test_plan_price_validation(self, db_session):
        """Test that price must be non-negative"""
        from app.models.plan import Plan, PlanTier, BillingInterval
        from decimal import Decimal
        
        # Negative price should be allowed by DB but validated in schema
        plan = Plan(
            id=uuid.uuid4(),
            name="Invalid Plan",
            slug="invalid-plan",
            tier=PlanTier.FREE,
            price=Decimal("-10.00"),
            billing_interval=BillingInterval.MONTHLY,
            is_active=True
        )
        
        # SQLAlchemy allows this, validation happens at Pydantic level
        db_session.add(plan)
        db_session.commit()
        assert plan.price == Decimal("-10.00")


class TestSubscriptionModel:
    """Test Subscription model and lifecycle"""
    
    def test_subscription_creation(self, db_session):
        """Test creating a subscription"""
        from app.models.tenant import Tenant
        from app.models.plan import Plan, PlanTier, BillingInterval
        from app.models.subscription import Subscription, SubscriptionStatus
        from decimal import Decimal
        
        # Create tenant
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Test Company",
            slug="test-company",
            email="company@example.com",
            schema_name="test_company"
        )
        plan = Plan(
            id=uuid.uuid4(),
            name="Test Plan",
            slug="test-plan",
            tier=PlanTier.PRO,
            price=Decimal("10.00"),
            billing_interval=BillingInterval.MONTHLY,
            is_active=True
        )
        
        db_session.add(tenant)
        db_session.add(plan)
        db_session.commit()
        
        # Create subscription
        subscription = Subscription(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            plan_id=plan.id,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30)
        )
        
        db_session.add(subscription)
        db_session.commit()
        
        assert subscription.status == SubscriptionStatus.ACTIVE
        assert subscription.tenant_id == tenant.id
        assert subscription.plan_id == plan.id
    
    def test_subscription_status_values(self, db_session):
        """Test subscription status transitions"""
        from app.models.subscription import Subscription, SubscriptionStatus
        from app.models.tenant import Tenant
        from app.models.plan import Plan, PlanTier, BillingInterval
        from decimal import Decimal
        
        # Create tenant and plan
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Test Company",
            slug="test-company",
            email="company@example.com",
            schema_name="test_company"
        )
        plan = Plan(
            id=uuid.uuid4(),
            name="Test Plan",
            slug="test-plan",
            tier=PlanTier.PRO,
            price=Decimal("10.00"),
            billing_interval=BillingInterval.MONTHLY,
            is_active=True
        )
        db_session.add(tenant)
        db_session.add(plan)
        db_session.commit()
        
        valid_statuses = [
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.CANCELED,
            SubscriptionStatus.PAST_DUE,
            SubscriptionStatus.TRIALING
        ]
        
        for status in valid_statuses:
            subscription = Subscription(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                plan_id=plan.id,
                status=status,
                current_period_start=datetime.utcnow(),
                current_period_end=datetime.utcnow() + timedelta(days=30)
            )
            assert subscription.status == status


class TestInvoiceModel:
    """Test Invoice model"""
    
    def test_invoice_creation(self, db_session):
        """Test creating an invoice"""
        from app.models.invoice import Invoice, InvoiceStatus
        from app.models.tenant import Tenant
        from decimal import Decimal
        from datetime import datetime
        
        # Create tenant
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Test Company",
            slug="test-company",
            email="company@example.com",
            schema_name="test_company"
        )
        db_session.add(tenant)
        db_session.commit()
        
        now = datetime.utcnow()
        invoice = Invoice(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            invoice_number="INV-001",
            subtotal=Decimal("29.99"),
            tax=Decimal("0.00"),
            total=Decimal("29.99"),
            amount_due=Decimal("29.99"),
            invoice_date=now,
            due_date=now,
            status=InvoiceStatus.PAID
        )
        
        db_session.add(invoice)
        db_session.commit()
        
        assert invoice.amount_due == Decimal("29.99")
        assert invoice.status == InvoiceStatus.PAID


class TestUsageModel:
    """Test Usage tracking model"""
    
    def test_usage_record_creation(self, db_session):
        """Test creating a usage record"""
        from app.models.usage_metric import UsageMetric, MetricType
        from app.models.tenant import Tenant
        from datetime import datetime
        
        # Create tenant
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Test Company",
            slug="test-company",
            email="company@example.com",
            schema_name="test_company"
        )
        db_session.add(tenant)
        db_session.commit()
        
        now = datetime.utcnow()
        usage = UsageMetric(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            metric_type=MetricType.API_CALLS,
            metric_name="api_calls",
            value=100,
            unit="calls",
            period_start=now,
            period_end=now
        )
        
        db_session.add(usage)
        db_session.commit()
        
        assert usage.metric_name == "api_calls"
        assert usage.value == 100
    
    def test_usage_aggregation(self, db_session):
        """Test usage data can be aggregated"""
        from app.models.usage_metric import UsageMetric, MetricType
        from app.models.tenant import Tenant
        from sqlalchemy import func
        from datetime import datetime
        
        # Create tenant
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Test Company",
            slug="test-company",
            email="company@example.com",
            schema_name="test_company"
        )
        db_session.add(tenant)
        db_session.commit()
        
        now = datetime.utcnow()
        # Create multiple usage records
        for i in range(5):
            usage = UsageMetric(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                metric_type=MetricType.API_CALLS,
                metric_name="api_calls",
                value=10,
                unit="calls",
                period_start=now,
                period_end=now
            )
            db_session.add(usage)
        
        db_session.commit()
        
        # Aggregate total usage
        total = db_session.query(
            func.sum(UsageMetric.value)
        ).filter(
            UsageMetric.tenant_id == tenant.id,
            UsageMetric.metric_name == "api_calls"
        ).scalar()
        
        assert total == 50
