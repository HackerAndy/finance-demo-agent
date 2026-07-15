"""
GL code master list and validation - deterministic, no ML.
"""
from typing import Dict, Optional
from ..models import GLCode


# Static GL master - in production, load from ERP or CSV
GL_MASTER: Dict[str, GLCode] = {
    "4000": GLCode(code="4000", name="Revenue - Product Sales", category="Revenue", is_active=True),
    "4010": GLCode(code="4010", name="Revenue - Services", category="Revenue", is_active=True),
    "5000": GLCode(code="5000", name="COGS - Materials", category="COGS", is_active=True),
    "5010": GLCode(code="5010", name="COGS - Labor", category="COGS", is_active=True),
    "6000": GLCode(code="6000", name="General Expense", category="OpEx", is_active=True),
    "6100": GLCode(code="6100", name="Office Supplies", category="OpEx", is_active=True),
    "6200": GLCode(code="6200", name="Software & SaaS", category="OpEx", is_active=True),
    "6300": GLCode(code="6300", name="Professional Services", category="OpEx", is_active=True),
    "6400": GLCode(code="6400", name="Travel & Entertainment", category="OpEx", is_active=True),
    "6500": GLCode(code="6500", name="Rent & Utilities", category="OpEx", is_active=True),
    "7000": GLCode(code="7000", name="Payroll", category="OpEx", is_active=True),
    "8000": GLCode(code="8000", name="Marketing", category="OpEx", is_active=True),
}


# Vendor-specific GL mappings (vendor_id -> {keyword: gl_code})
VENDOR_GL_RULES: Dict[str, Dict[str, str]] = {
    "VENDOR_AWS": {
        "aws": "6200",
        "amazon web services": "6200",
    },
    "VENDOR_GOOGLE": {
        "google cloud": "6200",
        "gcp": "6200",
    },
    "VENDOR_OFFICE": {
        "staples": "6100",
        "office depot": "6100",
    },
}


def validate_gl_code(code: str) -> bool:
    """Check if GL code exists and is active in master."""
    return code in GL_MASTER and GL_MASTER[code].is_active


def get_gl_code(code: str) -> Optional[GLCode]:
    """Get GLCode object by code."""
    return GL_MASTER.get(code)


def load_gl_master() -> Dict[str, GLCode]:
    """Return full GL master for UI dropdowns, etc."""
    return {k: v for k, v in GL_MASTER.items() if v.is_active}


def get_vendor_gl_code(vendor_id: str, description: str) -> Optional[str]:
    """Look up vendor-specific GL code from description keywords."""
    rules = VENDOR_GL_RULES.get(vendor_id.upper(), {})
    desc_lower = description.lower()
    for keyword, gl_code in rules.items():
        if keyword in desc_lower:
            return gl_code
    return None