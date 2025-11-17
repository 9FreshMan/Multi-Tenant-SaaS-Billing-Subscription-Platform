# Deployment Guide

## Local Development

### Prerequisites
- Docker Desktop installed
- Git
- (Optional) Python 3.11+ and Node.js 18+ for local development without Docker

### Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd pet
```

2. **Copy environment file**
```bash
cp .env.example .env
```

3. **Edit `.env` file**
- Set your Stripe API keys (get from https://dashboard.stripe.com/test/apikeys)
- Update other configuration as needed

4. **Start all services**
```bash
docker-compose up -d
```

5. **Run database migrations**
```bash
docker-compose exec backend alembic upgrade head
```

6. **Create initial plans (optional)**
You can create subscription plans via the API or directly in the database:

```bash
docker-compose exec backend python -c "
from app.core.database import Base, engine
from app.models.plan import Plan, PlanTier, BillingInterval
from sqlalchemy.orm import Session
import uuid

with Session(engine) as session:
    plans = [
        Plan(
            id=uuid.uuid4(),
            name='Free',
            slug='free',
            tier=PlanTier.FREE,
            price=0,
            billing_interval=BillingInterval.MONTHLY,
            max_users=5,
            max_api_calls=1000,
            max_storage_gb=5,
            is_active=True,
            is_public=True,
            sort_order=1
        ),
        Plan(
            id=uuid.uuid4(),
            name='Pro',
            slug='pro',
            tier=PlanTier.PRO,
            price=29,
            billing_interval=BillingInterval.MONTHLY,
            max_users=25,
            max_api_calls=10000,
            max_storage_gb=50,
            is_active=True,
            is_public=True,
            sort_order=2
        ),
        Plan(
            id=uuid.uuid4(),
            name='Enterprise',
            slug='enterprise',
            tier=PlanTier.ENTERPRISE,
            price=99,
            billing_interval=BillingInterval.MONTHLY,
            max_users=999,
            max_api_calls=100000,
            max_storage_gb=500,
            is_active=True,
            is_public=True,
            sort_order=3
        ),
    ]
    session.add_all(plans)
    session.commit()
"
```

7. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Production Deployment (Kubernetes)

### Prerequisites
- Kubernetes cluster (1.24+)
- kubectl configured
- Helm (optional but recommended)
- Docker registry access
- Domain names configured

### Steps

1. **Build and push Docker images**

```bash
# Backend
cd backend
docker build -t your-registry/saas-billing-backend:latest -f ../docker/backend.Dockerfile .
docker push your-registry/saas-billing-backend:latest

# Frontend
cd ../frontend
docker build -t your-registry/saas-billing-frontend:latest -f ../docker/frontend.Dockerfile .
docker push your-registry/saas-billing-frontend:latest
```

2. **Update Kubernetes manifests**
- Edit `k8s/backend.yaml` and update image references
- Edit `k8s/config.yaml` with your production values
- Edit `k8s/ingress.yaml` with your domain names

3. **Create secrets**

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets (replace with actual values)
kubectl create secret generic backend-secret \
  --from-literal=SECRET_KEY=your-secret-key \
  --from-literal=STRIPE_SECRET_KEY=sk_live_xxx \
  --from-literal=STRIPE_PUBLISHABLE_KEY=pk_live_xxx \
  --from-literal=STRIPE_WEBHOOK_SECRET=whsec_xxx \
  -n saas-billing

kubectl create secret generic postgres-secret \
  --from-literal=password=your-postgres-password \
  -n saas-billing
```

4. **Deploy infrastructure**

```bash
# Deploy PostgreSQL
kubectl apply -f k8s/postgres.yaml

# Deploy Redis
kubectl apply -f k8s/redis.yaml

# Wait for databases to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n saas-billing --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n saas-billing --timeout=300s
```

5. **Run migrations**

```bash
# Create a migration job
kubectl run migration-job --image=your-registry/saas-billing-backend:latest \
  --restart=Never -n saas-billing \
  --env="DATABASE_URL=postgresql://postgres:password@postgres:5432/saas_billing" \
  -- alembic upgrade head

# Check logs
kubectl logs migration-job -n saas-billing
```

6. **Deploy application**

```bash
# Deploy backend
kubectl apply -f k8s/backend.yaml

# Deploy Celery workers
kubectl apply -f k8s/celery.yaml

# Deploy config
kubectl apply -f k8s/config.yaml

# Deploy ingress
kubectl apply -f k8s/ingress.yaml
```

7. **Verify deployment**

```bash
kubectl get pods -n saas-billing
kubectl get services -n saas-billing
kubectl get ingress -n saas-billing
```

8. **Configure DNS**
Point your domain names to the ingress load balancer IP:
```bash
kubectl get ingress -n saas-billing
```

## Stripe Configuration

### Webhook Setup

1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Set endpoint URL: `https://api.your-domain.com/api/v1/webhooks/stripe`
4. Select events:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.created`
   - `invoice.paid`
   - `invoice.payment_failed`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Copy the webhook secret and add to your secrets

### Create Products in Stripe

For each plan, create a product and price in Stripe:

```python
import stripe
stripe.api_key = "your_secret_key"

# Create Free Plan
product = stripe.Product.create(name="Free Plan")
price = stripe.Price.create(
    product=product.id,
    unit_amount=0,
    currency="usd",
    recurring={"interval": "month"},
)

# Update Plan model with stripe_price_id and stripe_product_id
```

## Monitoring

### Health Checks

- Backend: `https://api.your-domain.com/health`
- Check all pods: `kubectl get pods -n saas-billing`

### Logs

```bash
# Backend logs
kubectl logs -f deployment/backend -n saas-billing

# Celery worker logs
kubectl logs -f deployment/celery-worker -n saas-billing

# PostgreSQL logs
kubectl logs -f deployment/postgres -n saas-billing
```

### Metrics (if Prometheus is installed)

```bash
kubectl port-forward svc/prometheus 9090:9090 -n monitoring
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend
kubectl scale deployment backend --replicas=5 -n saas-billing

# Scale celery workers
kubectl scale deployment celery-worker --replicas=3 -n saas-billing
```

### Vertical Scaling

Edit resource limits in deployment manifests and apply:
```bash
kubectl apply -f k8s/backend.yaml
```

## Backup & Recovery

### Database Backup

```bash
# Create backup
kubectl exec -n saas-billing deployment/postgres -- \
  pg_dump -U postgres saas_billing > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
kubectl exec -i -n saas-billing deployment/postgres -- \
  psql -U postgres saas_billing < backup.sql
```

### Automated Backups

Use a CronJob for regular backups:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: saas-billing
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15-alpine
            command:
            - sh
            - -c
            - pg_dump -U postgres -h postgres saas_billing > /backup/backup_$(date +%Y%m%d).sql
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check PostgreSQL pod status
   - Verify DATABASE_URL configuration
   - Check network policies

2. **Stripe webhook failures**
   - Verify webhook secret
   - Check endpoint URL is accessible
   - Review Stripe dashboard for error details

3. **Celery tasks not running**
   - Check Redis connection
   - Verify Celery worker logs
   - Ensure Celery beat is running

4. **Frontend can't reach backend**
   - Check CORS_ORIGINS configuration
   - Verify ingress rules
   - Check API URL in frontend config

### Debug Commands

```bash
# Get detailed pod information
kubectl describe pod <pod-name> -n saas-billing

# Enter pod shell
kubectl exec -it <pod-name> -n saas-billing -- /bin/sh

# Check environment variables
kubectl exec <pod-name> -n saas-billing -- env

# Test database connection
kubectl exec -it deployment/backend -n saas-billing -- \
  python -c "from app.core.database import engine; print(engine.execute('SELECT 1').scalar())"
```
