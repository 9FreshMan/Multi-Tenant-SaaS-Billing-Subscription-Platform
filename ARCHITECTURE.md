# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌─────────┬──────────┬──────────┬──────────┬─────────────┐ │
│  │Dashboard│Billing   │Analytics │Settings  │Auth         │ │
│  └─────────┴──────────┴──────────┴──────────┴─────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS/REST API
┌──────────────────────────▼──────────────────────────────────┐
│                    API Gateway (Nginx)                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Routes                               │   │
│  │  /auth  /tenants  /subscriptions  /invoices  /usage │   │
│  └────────┬──────────────────────────────────┬──────────┘   │
│           │                                  │              │
│  ┌────────▼─────────┐              ┌────────▼────────┐     │
│  │   Services       │              │  Middleware     │     │
│  │  - Stripe        │              │  - Tenant       │     │
│  │  - Auth          │              │  - Auth         │     │
│  │  - Billing       │              │  - CORS         │     │
│  └────────┬─────────┘              └─────────────────┘     │
└───────────┼──────────────────────────────────────────────────┘
            │
┌───────────▼───────────────────────┐
│     Database Layer (PostgreSQL)   │
│  ┌──────────────────────────────┐ │
│  │  Multi-Tenant Schemas        │ │
│  │  - tenant_acme              │ │
│  │  - tenant_company           │ │
│  │  - shared (tenants, users) │ │
│  └──────────────────────────────┘ │
└───────────────────────────────────┘

┌──────────────────────────────────┐
│   Background Jobs (Celery)       │
│  ┌────────────────────────────┐  │
│  │  Workers                   │  │
│  │  - Invoice generation      │  │
│  │  - Payment reminders       │  │
│  │  - Usage calculation       │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │  Beat Scheduler            │  │
│  │  - Cron jobs               │  │
│  └────────────────────────────┘  │
└────────────┬─────────────────────┘
             │
┌────────────▼─────────────────────┐
│       Redis (Message Broker)      │
└───────────────────────────────────┘

┌───────────────────────────────────┐
│    External Services              │
│  - Stripe (Payments)              │
│  - SendGrid (Emails - optional)   │
└───────────────────────────────────┘
```

## Multi-Tenancy Strategy

### Schema-per-Tenant Approach

Each tenant has its own PostgreSQL schema for data isolation:

```
Database: saas_billing
├── public (shared tables)
│   ├── tenants
│   ├── users
│   ├── plans
│   └── subscriptions
│
├── tenant_acme (tenant-specific data)
│   ├── invoices
│   ├── payments
│   ├── usage_metrics
│   └── custom_data
│
└── tenant_company (tenant-specific data)
    ├── invoices
    ├── payments
    ├── usage_metrics
    └── custom_data
```

**Benefits:**
- Strong data isolation
- Easy backup/restore per tenant
- Performance isolation
- Simpler compliance (GDPR, etc.)

**Implementation:**
- Middleware extracts tenant context from header/subdomain
- Database queries scoped to tenant schema
- Row-level security for shared tables

## Data Flow

### 1. User Registration Flow

```
User → Frontend → Backend /auth/register
                     ↓
              Create Tenant in DB
                     ↓
              Create Stripe Customer
                     ↓
              Create Owner User
                     ↓
              Return JWT Token
                     ↓
              Frontend stores token
```

### 2. Subscription Creation Flow

```
User → Select Plan → Frontend → Backend /subscriptions
                                    ↓
                            Check existing subscription
                                    ↓
                            Create Stripe Subscription
                                    ↓
                            Save to Database
                                    ↓
                            Return subscription data
```

### 3. Payment Processing Flow

```
Stripe → Webhook → Backend /webhooks/stripe
                      ↓
                Verify signature
                      ↓
                Process event
                      ↓
                Update database
                      ↓
                Trigger email (if needed)
```

### 4. Usage Tracking Flow

```
Application → Backend /usage (record metric)
                 ↓
         Save to usage_metrics table
                 ↓
    Celery task aggregates usage
                 ↓
    Compare against plan limits
                 ↓
    Alert if approaching limit
```

## Security Architecture

### Authentication & Authorization

1. **JWT-based Authentication**
   - Access token (30 min expiry)
   - Refresh token (7 days expiry)
   - Stored in localStorage (client-side)

2. **Role-Based Access Control (RBAC)**
   - Roles: Owner, Admin, Manager, Member, Viewer
   - Hierarchical permissions
   - Enforced at API endpoint level

3. **Tenant Isolation**
   - Middleware validates tenant context
   - All queries scoped to tenant
   - No cross-tenant data access

### API Security

- **Rate Limiting**: Per tenant/user (to be implemented)
- **CORS**: Configured origins only
- **HTTPS**: Required in production
- **Input Validation**: Pydantic schemas
- **SQL Injection**: Protected by SQLAlchemy ORM

## Scalability Considerations

### Horizontal Scaling

- **Backend**: Stateless, can scale to N replicas
- **Celery Workers**: Scale based on queue length
- **Database**: Use read replicas for queries

### Vertical Scaling

- **Database**: Increase instance size
- **Redis**: Increase memory allocation

### Caching Strategy

- **Application Cache**: Redis for session data
- **API Cache**: Cache plan listings, etc.
- **Database Cache**: PostgreSQL query cache

## Performance Optimization

### Database

- **Indexes**: On foreign keys, frequently queried columns
- **Connection Pooling**: SQLAlchemy pool
- **Query Optimization**: Eager loading, select_related

### API

- **Async Operations**: FastAPI async endpoints
- **Background Tasks**: Celery for long-running operations
- **Pagination**: For list endpoints

### Frontend

- **Code Splitting**: React lazy loading
- **Asset Optimization**: Minification, compression
- **CDN**: Static assets served from CDN

## Monitoring & Observability

### Metrics to Track

1. **Application Metrics**
   - API response times
   - Error rates
   - Request volume

2. **Business Metrics**
   - Active subscriptions
   - Monthly recurring revenue (MRR)
   - Churn rate
   - Usage per tenant

3. **Infrastructure Metrics**
   - CPU/Memory usage
   - Database connections
   - Celery queue length

### Logging Strategy

- **Structured Logging**: JSON format
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Centralized**: Aggregate logs from all services

### Alerting

- Database connection failures
- Stripe webhook failures
- High error rates
- Resource exhaustion

## Disaster Recovery

### Backup Strategy

- **Database**: Daily automated backups
- **Retention**: 30 days
- **Testing**: Monthly restore tests

### High Availability

- **Database**: PostgreSQL with replication
- **Redis**: Redis Sentinel or Cluster
- **Application**: Multiple replicas behind load balancer

## Technology Choices Rationale

| Technology | Why? |
|-----------|------|
| **FastAPI** | Modern, fast, async support, auto-generated docs |
| **React** | Component-based, large ecosystem, TypeScript support |
| **PostgreSQL** | ACID compliance, JSON support, schema-per-tenant |
| **Redis** | Fast in-memory cache, Celery broker |
| **Stripe** | Industry standard, comprehensive API, webhooks |
| **Celery** | Distributed task queue, scheduling, reliability |
| **Docker** | Consistent environments, easy deployment |
| **Kubernetes** | Orchestration, scaling, self-healing |

## Future Enhancements

- [ ] GraphQL API option
- [ ] Webhooks for customer events
- [ ] Advanced analytics with BI tools
- [ ] Mobile apps (React Native)
- [ ] SSO integration (OAuth2, SAML)
- [ ] Multi-currency support
- [ ] Usage-based pricing calculations
- [ ] Dunning management
- [ ] Customer portal
- [ ] API rate limiting per plan
