# Multi-Tenant SaaS Billing Platform

Enterprise-grade billing system with complete tenant isolation, Stripe payments, and real-time analytics.

## Features

### Multi-Tenancy
- Complete tenant data isolation
- Automatic tenant context resolution

### Payments & Billing
- Stripe payment integration
- Subscription management (Free/Pro/Enterprise)
- Automated invoice generation with PDF export
- Trial period support (14 days)

### Security & Authentication
- JWT authentication (access + refresh tokens)
- Role-based access control
- Argon2 password hashing
- Tenant isolation middleware

### Analytics
- Real-time usage metrics
- Interactive charts (API calls, storage, bandwidth)
- Revenue tracking


## Tech Stack

**Backend:**
- FastAPI 0.104.1 - Async web framework
- SQLAlchemy 2.0 - Async ORM with Alembic migrations
- PostgreSQL 15 - Primary database
- Redis 7 - Caching & message broker
- Celery 5.3 - Background task queue
- Stripe SDK - Payment processing
- ReportLab 4.4.4 - PDF invoice generation

**Frontend:**
- React 18.2 with TypeScript 5.2
- Vite 5.0 - Build tool
- TailwindCSS 3.3 - Styling
- Recharts 2.10 - Interactive charts
- Axios - HTTP client

**DevOps:**
- Docker & Docker Compose
- Nginx - Reverse proxy


## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/              # API routes & endpoints
│   │   ├── core/             # Configuration
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── middleware/       # Tenant isolation
│   ├── alembic/              # Database migrations
│   └── tests/                # Test suite
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   └── services/         # API services
│   └── package.json
└── docker-compose.yml        # Local development setup
```

## Quick Start

```bash
# Clone repository
git clone <your-repo-url>
cd pet

# Copy environment configuration
cp .env.example .env

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### First Steps

1. Register a new account at http://localhost:3000/register
2. Explore the dashboard
3. For testing payments, use Stripe test card: `4242 4242 4242 4242`


## Environment Variables

Create `.env` file with these key variables:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/saas_billing

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=30

# Stripe (get from https://dashboard.stripe.com)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# CORS
CORS_ORIGINS=http://localhost:3000
```

## Database Models

- **Tenant** - Organization/Company
- **User** - Platform users with role-based access
- **Plan** - Subscription plans (Free/Pro/Enterprise)
- **Subscription** - Active subscriptions
- **Invoice** - Billing invoices with PDF generation
- **Payment** - Payment records
- **UsageMetric** - Usage tracking (API calls, storage, bandwidth)

## API Documentation

Interactive API docs available at http://localhost:8000/docs

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register new tenant & user |
| `/api/v1/auth/login` | POST | User authentication |
| `/api/v1/auth/refresh` | POST | Refresh JWT token |
| `/api/v1/plans/` | GET | List subscription plans |
| `/api/v1/subscriptions/` | GET/POST | Manage subscriptions |
| `/api/v1/invoices/` | GET | List invoices |
| `/api/v1/invoices/{id}/pdf` | GET | Download invoice PDF |
| `/api/v1/tenants/me` | GET/PUT | Tenant settings |
| `/api/v1/users/me` | GET/PATCH | User profile |

## License

MIT License
