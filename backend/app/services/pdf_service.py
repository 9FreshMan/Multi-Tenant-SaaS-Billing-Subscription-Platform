"""PDF Invoice Generation Service"""
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


class InvoicePDFGenerator:
    """Generate PDF invoices"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='InvoiceHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='InvoiceAmount',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#059669'),
            alignment=TA_RIGHT
        ))
    
    def generate_invoice(
        self,
        invoice_number: str,
        invoice_date: str,
        customer_name: str,
        customer_email: str,
        items: list,
        subtotal: float,
        tax: float = 0.0,
        total: float = None,
        status: str = "PAID"
    ) -> BytesIO:
        """
        Generate PDF invoice
        
        Args:
            invoice_number: Invoice number (e.g., INV-2024-001)
            invoice_date: Invoice date
            customer_name: Customer/Company name
            customer_email: Customer email
            items: List of items [{"description": "...", "amount": 29.00}]
            subtotal: Subtotal amount
            tax: Tax amount
            total: Total amount (if None, calculated as subtotal + tax)
            status: Invoice status (PAID, PENDING, etc.)
        
        Returns:
            BytesIO: PDF file buffer
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        elements = []
        
        # Title
        title = Paragraph("INVOICE", self.styles['InvoiceTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Invoice Info Table
        invoice_info_data = [
            ['Invoice Number:', invoice_number],
            ['Invoice Date:', invoice_date],
            ['Status:', status],
            ['', '']
        ]
        
        invoice_info_table = Table(invoice_info_data, colWidths=[2 * inch, 2.5 * inch])
        invoice_info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6b7280')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1f2937')),
        ]))
        
        elements.append(invoice_info_table)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Billing Information
        billing_header = Paragraph("<b>BILL TO:</b>", self.styles['InvoiceHeader'])
        elements.append(billing_header)
        elements.append(Spacer(1, 0.1 * inch))
        
        customer_info = Paragraph(
            f"<b>{customer_name}</b><br/>{customer_email}",
            self.styles['Normal']
        )
        elements.append(customer_info)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Items Table
        items_data = [['Description', 'Amount']]
        for item in items:
            items_data.append([
                item.get('description', 'Service'),
                f"${item.get('amount', 0.0):.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[4.5 * inch, 2 * inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(items_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Totals
        total_amount = total if total is not None else (subtotal + tax)
        
        totals_data = [
            ['Subtotal:', f'${subtotal:.2f}'],
            ['Tax:', f'${tax:.2f}'],
            ['', ''],
            ['TOTAL:', f'${total_amount:.2f}']
        ]
        
        totals_table = Table(totals_data, colWidths=[4.5 * inch, 2 * inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 2), 'Helvetica'),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 2), 10),
            ('FONTSIZE', (0, 3), (-1, 3), 14),
            ('TEXTCOLOR', (0, 0), (-1, 2), colors.HexColor('#6b7280')),
            ('TEXTCOLOR', (0, 3), (-1, 3), colors.HexColor('#059669')),
            ('LINEABOVE', (0, 3), (-1, 3), 2, colors.HexColor('#059669')),
            ('TOPPADDING', (0, 3), (-1, 3), 12),
        ]))
        
        elements.append(totals_table)
        elements.append(Spacer(1, 1 * inch))
        
        # Footer
        footer_text = Paragraph(
            "<i>Thank you for your business!</i><br/>"
            "For questions about this invoice, please contact billing@saas.com",
            self.styles['Normal']
        )
        elements.append(footer_text)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer


# Singleton instance
pdf_generator = InvoicePDFGenerator()


def generate_sample_invoice() -> BytesIO:
    """Generate a sample invoice for testing"""
    return pdf_generator.generate_invoice(
        invoice_number="INV-2024-001",
        invoice_date="January 15, 2024",
        customer_name="Acme Inc",
        customer_email="billing@acme.com",
        items=[
            {
                "description": "Pro Plan - Monthly Subscription",
                "amount": 29.00
            }
        ],
        subtotal=29.00,
        tax=0.00,
        total=29.00,
        status="PAID"
    )
