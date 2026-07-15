"""
Pydantic models for all data crossing boundaries.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class InvoiceStatus(str, Enum):
    RECEIVED = "received"
    EXTRACTED = "extracted"
    PO_MATCHED = "po_matched"
    GL_CODED = "gl_coded"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    gl_code: Optional[str] = None


class Invoice(BaseModel):
    invoice_id: str
    vendor_name: str
    vendor_id: Optional[str] = None
    invoice_date: datetime
    due_date: Optional[datetime] = None
    total_amount: float
    currency: str = "USD"
    line_items: List[LineItem]
    po_number: Optional[str] = None
    gl_codes: List[str] = []
    status: InvoiceStatus = InvoiceStatus.RECEIVED
    audit_trail: List["AuditRecord"] = []


class PurchaseOrder(BaseModel):
    po_number: str
    vendor_id: str
    line_items: List[LineItem]
    total_amount: float
    status: str


class GLCode(BaseModel):
    code: str
    name: str
    category: str
    is_active: bool = True


class AuditRecord(BaseModel):
    timestamp: datetime
    actor: str  # "system", "human", "agent"
    action: str
    from_status: Optional[InvoiceStatus] = None
    to_status: Optional[InvoiceStatus] = None
    details: dict = {}


class ERPEntry(BaseModel):
    invoice_id: str
    erp_document_number: str
    posted_date: datetime
    status: str


# Forward reference resolution
Invoice.model_rebuild()