import pytest
import pytest_asyncio
import httpx
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.database import Base, get_db

# Test database setup - using synchronous SQLite for tests  
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Sync engine for table creation/cleanup
sync_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Async engine for actual test operations
async_engine = create_async_engine(
    f"sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
AsyncTestingSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
def db_session():
    """Create a fresh synchronous database for model tests"""
    Base.metadata.create_all(bind=sync_engine)
    db = TestingSessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        Base.metadata.drop_all(bind=sync_engine)


@pytest_asyncio.fixture
async def async_db_session():
    """Create a fresh async database for endpoint tests"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncTestingSessionLocal() as session:
        yield session
        await session.rollback()
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(async_db_session):
    """Create an async test client with overridden database dependency"""
    async def override_get_db():
        yield async_db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create default plans for tests
    from app.models.plan import Plan, PlanTier, BillingInterval
    from decimal import Decimal
    import uuid
    
    plans = [
        Plan(
            id=uuid.uuid4(),
            name="Free",
            slug="free",
            tier=PlanTier.FREE,
            description="Free plan",
            price=Decimal("0.00"),
            billing_interval=BillingInterval.MONTHLY,
            max_users=1,
            max_api_calls=100,
            max_storage_gb=1,
            features={},
            is_active=True,
            is_public=True,
            trial_days=0,
            sort_order=1
        ),
        Plan(
            id=uuid.uuid4(),
            name="Pro",
            slug="pro",
            tier=PlanTier.PRO,
            description="Professional plan",
            price=Decimal("29.00"),
            billing_interval=BillingInterval.MONTHLY,
            max_users=25,
            max_api_calls=10000,
            max_storage_gb=50,
            features={},
            is_active=True,
            is_public=True,
            trial_days=14,
            sort_order=2
        ),
        Plan(
            id=uuid.uuid4(),
            name="Enterprise",
            slug="enterprise",
            tier=PlanTier.ENTERPRISE,
            description="Enterprise plan",
            price=Decimal("99.00"),
            billing_interval=BillingInterval.MONTHLY,
            max_users=100,
            max_api_calls=100000,
            max_storage_gb=500,
            features={},
            is_active=True,
            is_public=True,
            trial_days=30,
            sort_order=3
        )
    ]
    
    for plan in plans:
        async_db_session.add(plan)
    await async_db_session.commit()
    
    async with httpx.AsyncClient(app=app, base_url="http://test", follow_redirects=True) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "tenant_name": "Test Company",
        "tenant_slug": "test-company",
        "email": "test@example.com",
        "password": "TestPass123!",
        "first_name": "John",
        "last_name": "Doe"
    }


@pytest.fixture
def mock_stripe(monkeypatch):
    """Mock Stripe API calls"""
    class MockStripeCustomer:
        id = "cus_mock123"
    
    class MockStripe:
        @staticmethod
        def create_customer(*args, **kwargs):
            return MockStripeCustomer()
    
    monkeypatch.setattr("app.services.stripe_service.StripeService", MockStripe)
    return MockStripe
