from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_tenant
from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.tenant import TenantResponse
from app.schemas.tenant import TenantUpdate

from sqlalchemy import select, update

from fastapi import HTTPException, status

router = APIRouter()


@router.get("/me", response_model=TenantResponse)
async def get_current_tenant_info(
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    """
    Get current tenant information
    """
    return current_tenant


@router.put("/me", response_model=TenantResponse)
async def update_current_tenant(
    payload: TenantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    """
    Update current tenant settings
    """
    # Build update dict from payload
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    # Perform update
    stmt = (
        update(Tenant)
        .where(Tenant.id == current_tenant.id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()

    # Return updated tenant
    result = await db.execute(select(Tenant).where(Tenant.id == current_tenant.id))
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found after update")

    return tenant
