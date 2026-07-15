"""
PO matching - core tool, no framework imports.
"""
from typing import Optional
from ..models import Invoice, PurchaseOrder


def match_po(invoice: Invoice, po_candidates: List[PurchaseOrder]) -> Optional[PurchaseOrder]:
    """
    Match invoice to PO using vendor_id, amount, and line item fuzzy matching.
    
    Returns matched PO or None if no match found.
    """
    # TODO: Implement matching logic
    # 1. Exact match on PO number if present on invoice
    # 2. Fuzzy match on vendor + amount + date window
    # 3. Line item description similarity
    return None