"""
Invoice extraction from PDF - core tool, no framework imports.
"""
from typing import List
from ..models import Invoice, LineItem


def extract_invoice_fields(pdf_bytes: bytes) -> Invoice:
    """
    Extract structured invoice data from PDF bytes.
    
    Returns Invoice with RECEIVED status.
    Fields: vendor_name, invoice_date, total_amount, line_items, po_number
    """
    # TODO: Implement PDF parsing (pdfplumber, pymupdf, or LLM vision)
    # For now, return minimal structure
    return Invoice(
        invoice_id="inv_001",
        vendor_name="[EXTRACTED_VENDOR]",
        invoice_date=None,
        total_amount=0.0,
        line_items=[],
        status=__import__("finance_demo_agent.core.models", fromlist=["InvoiceStatus"]).InvoiceStatus.RECEIVED
    )