"""Invoice PDF API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.invoice import Invoice
from app.services.pdf_service import pdf_generator

router = APIRouter()


@router.get("/invoices/{invoice_id}/pdf")
async def download_invoice_pdf(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Download invoice as PDF
    
    Returns PDF file for specified invoice
    """
    # Get invoice
    result = await db.execute(
        select(Invoice).where(
            Invoice.id == invoice_id,
            Invoice.tenant_id == current_user.tenant_id
        )
    )
    invoice = result.scalar_one_or_none()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Get plan name safely without lazy loading
    plan_name = "Service"
    if invoice.subscription_id:
        from app.models.subscription import Subscription
        from app.models.plan import Plan
        sub_result = await db.execute(
            select(Subscription).where(Subscription.id == invoice.subscription_id)
        )
        subscription = sub_result.scalar_one_or_none()
        if subscription and subscription.plan_id:
            plan_result = await db.execute(
                select(Plan).where(Plan.id == subscription.plan_id)
            )
            plan = plan_result.scalar_one_or_none()
            if plan:
                plan_name = plan.name
    
    # Generate PDF
    items = [
        {
            "description": f"{plan_name} - Monthly Subscription",
            "amount": float(invoice.total or invoice.amount_due or 0)
        }
    ]
    
    pdf_buffer = pdf_generator.generate_invoice(
        invoice_number=invoice.invoice_number or f"INV-{invoice.id[:8]}",
        invoice_date=invoice.created_at.strftime("%B %d, %Y"),
        customer_name=current_user.full_name or current_user.email,
        customer_email=current_user.email,
        items=items,
        subtotal=float(invoice.total or invoice.amount_due or 0),
        tax=0.00,
        total=float(invoice.total or invoice.amount_due or 0),
        status=invoice.status.value.upper() if hasattr(invoice.status, 'value') else str(invoice.status).upper()
    )
    
    # Return PDF as streaming response
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=invoice-{invoice.invoice_number or invoice.id[:8]}.pdf"
        }
    )


@router.get("/invoices/{invoice_id}/pdf/view")
async def view_invoice_pdf(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    View invoice PDF in browser
    
    Returns PDF file for inline viewing
    """
    # Get invoice
    result = await db.execute(
        select(Invoice).where(
            Invoice.id == invoice_id,
            Invoice.tenant_id == current_user.tenant_id
        )
    )
    invoice = result.scalar_one_or_none()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Get plan name safely without lazy loading
    plan_name = "Service"
    if invoice.subscription_id:
        from app.models.subscription import Subscription
        from app.models.plan import Plan
        sub_result = await db.execute(
            select(Subscription).where(Subscription.id == invoice.subscription_id)
        )
        subscription = sub_result.scalar_one_or_none()
        if subscription and subscription.plan_id:
            plan_result = await db.execute(
                select(Plan).where(Plan.id == subscription.plan_id)
            )
            plan = plan_result.scalar_one_or_none()
            if plan:
                plan_name = plan.name
    
    # Generate PDF
    items = [
        {
            "description": f"{plan_name} - Monthly Subscription",
            "amount": float(invoice.total or invoice.amount_due or 0)
        }
    ]
    
    pdf_buffer = pdf_generator.generate_invoice(
        invoice_number=invoice.invoice_number or f"INV-{invoice.id[:8]}",
        invoice_date=invoice.created_at.strftime("%B %d, %Y"),
        customer_name=current_user.full_name or current_user.email,
        customer_email=current_user.email,
        items=items,
        subtotal=float(invoice.total or invoice.amount_due or 0),
        tax=0.00,
        total=float(invoice.total or invoice.amount_due or 0),
        status=invoice.status.value.upper() if hasattr(invoice.status, 'value') else str(invoice.status).upper()
    )
    
    # Return PDF for inline viewing
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=invoice-{invoice.invoice_number or invoice.id[:8]}.pdf"
        }
    )


@router.get("/invoices/sample/pdf")
async def download_sample_invoice(
    current_user: User = Depends(get_current_user)
):
    """
    Download a sample invoice PDF (for demo/testing)
    """
    from app.services.pdf_service import generate_sample_invoice
    
    pdf_buffer = generate_sample_invoice()
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=sample-invoice.pdf"
        }
    )
