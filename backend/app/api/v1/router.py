from fastapi import APIRouter

from app.api.v1.endpoints import auth, tenants, users, plans, subscriptions, invoices, usage, webhooks

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(plans.router, prefix="/plans", tags=["Plans"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
api_router.include_router(usage.router, prefix="/usage", tags=["Usage & Analytics"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
