"""
GL code suggestion - core tool, no framework imports.
Uses vendor rules + ML fallback.
"""
from typing import List
from ..models import Invoice, LineItem


def suggest_gl_code(line_item: LineItem, vendor_id: str = None) -> str:
    """
    Suggest GL code for a line item.
    
    Priority:
    1. Vendor-specific mapping (from GL master)
    2. Description keyword matching
    3. ML model fallback (if available)
    4. Default "Uncategorized Expense" code
    """
    # TODO: Implement GL coding logic
    # - Load vendor rules from validators.gl_codes
    # - Keyword matching on line_item.description
    # - Return GL code string
    return "6000"  # Default: General Expense