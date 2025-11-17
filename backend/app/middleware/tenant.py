from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware для определения и установки контекста tenant'a
    
    Поддерживает несколько способов определения tenant:
    1. По поддомену (tenant.example.com)
    2. По заголовку X-Tenant-ID
    3. По заголовку X-Tenant-Slug
    """
    
    async def dispatch(self, request: Request, call_next):
        # Пропускаем системные эндпоинты и auth endpoints
        excluded_paths = [
            "/health", 
            "/docs", 
            "/redoc", 
            "/openapi.json",
            "/api/v1/auth/register",
            "/api/v1/auth/login",
            "/api/v1/auth/refresh",
            "/api/v1/plans/",
            "/api/v1/plans",
        ]
        
        # Также пропускаем если путь начинается с excluded path
        if request.url.path in excluded_paths or any(request.url.path.startswith(path) for path in ["/api/v1/plans"]):
            return await call_next(request)
        
        tenant_id = None
        tenant_slug = None
        
        # Попытка 1: Из заголовка X-Tenant-ID
        tenant_id = request.headers.get("X-Tenant-ID")
        
        # Попытка 2: Из заголовка X-Tenant-Slug
        if not tenant_id:
            tenant_slug = request.headers.get("X-Tenant-Slug")
        
        # Попытка 3: Из поддомена
        if not tenant_id and not tenant_slug:
            host = request.headers.get("host", "")
            parts = host.split(".")
            if len(parts) > 2:  # Есть поддомен
                tenant_slug = parts[0]
        
        # Сохраняем в state для использования в эндпоинтах
        request.state.tenant_id = tenant_id
        request.state.tenant_slug = tenant_slug
        
        logger.debug(f"Tenant context: id={tenant_id}, slug={tenant_slug}")
        
        response = await call_next(request)
        return response


async def get_current_tenant_id(request: Request) -> str:
    """Dependency для получения текущего tenant_id"""
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant ID not found in request context"
        )
    return tenant_id


async def get_current_tenant_slug(request: Request) -> str:
    """Dependency для получения текущего tenant_slug"""
    tenant_slug = getattr(request.state, "tenant_slug", None)
    if not tenant_slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant slug not found in request context"
        )
    return tenant_slug
