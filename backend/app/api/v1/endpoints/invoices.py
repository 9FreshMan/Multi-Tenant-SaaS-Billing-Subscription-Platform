from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_tenant
from app.models.user import User
from app.models.tenant import Tenant
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceResponse

router = APIRouter()


@router.get("", response_model=List[InvoiceResponse])
async def get_invoices(
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all invoices for current tenant
    """
    result = await db.execute(
        select(Invoice)
        .where(Invoice.tenant_id == current_tenant.id)
        .order_by(Invoice.created_at.desc())
    )
    invoices = result.scalars().all()
    return invoices


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific invoice
    """
    from fastapi import HTTPException, status
    
    result = await db.execute(
        select(Invoice).where(
            Invoice.id == invoice_id,
            Invoice.tenant_id == current_tenant.id,
        )
    )
    invoice = result.scalar_one_or_none()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    
    return invoice
