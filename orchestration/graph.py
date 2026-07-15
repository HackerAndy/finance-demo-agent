"""
LangGraph orchestration - ONLY directory importing langgraph.
Thin glue layer: nodes call core tools, validate, return state.
"""
# from langgraph.graph import StateGraph, END
# from langgraph.checkpoint.postgres import PostgresSaver
# from typing import TypedDict, Annotated
# from core.models import Invoice, InvoiceStatus
# from core.tools import extract_invoice_fields, match_po, suggest_gl_code, create_erp_entry
# from core.validators import validate_gl_code
# from core.policies.thresholds import review_thresholds


# class AgentState(TypedDict):
#     invoice: Invoice
#     po_candidates: list
#     current_step: str
#     errors: list


# def extract_node(state: AgentState) -> AgentState:
#     """Extract invoice fields from PDF."""
#     invoice = state["invoice"]
#     # pdf_bytes = get_pdf_bytes(invoice.invoice_id)  # from interface
#     extracted = extract_invoice_fields(b"")  # placeholder
#     invoice.vendor_name = extracted.vendor_name
#     invoice.invoice_date = extracted.invoice_date
#     invoice.total_amount = extracted.total_amount
#     invoice.line_items = extracted.line_items
#     invoice.po_number = extracted.po_number
#     invoice.status = InvoiceStatus.EXTRACTED
#     return {"invoice": invoice, "current_step": "extracted"}


# def match_po_node(state: AgentState) -> AgentState:
#     """Match invoice to PO."""
#     invoice = state["invoice"]
#     matched_po = match_po(invoice, state["po_candidates"])
#     if matched_po:
#         invoice.po_number = matched_po.po_number
#         invoice.status = InvoiceStatus.PO_MATCHED
#     return {"invoice": invoice, "current_step": "po_matched"}


# def gl_code_node(state: AgentState) -> AgentState:
#     """Assign GL codes to line items."""
#     invoice = state["invoice"]
#     for item in invoice.line_items:
#         if not item.gl_code:
#             item.gl_code = suggest_gl_code(item, invoice.vendor_id)
#             # Validate
#             if not validate_gl_code(item.gl_code):
#                 item.gl_code = "6000"  # fallback
#     invoice.gl_codes = [item.gl_code for item in invoice.line_items]
#     invoice.status = InvoiceStatus.GL_CODED
#     return {"invoice": invoice, "current_step": "gl_coded"}


# def human_review_node(state: AgentState) -> AgentState:
#     """HITL interrupt at dollar thresholds."""
#     invoice = state["invoice"]
#     # Check thresholds from config
#     if invoice.total_amount >= review_thresholds["dual_approval"]:
#         # Interrupt - wait for dual approval
#         pass
#     elif invoice.total_amount >= review_thresholds["single_approver"]:
#         # Interrupt - wait for single approval
#         pass
#     else:
#         # Auto-approve
#         invoice.status = InvoiceStatus.APPROVED
#     return {"invoice": invoice, "current_step": "reviewed"}


# def submit_erp_node(state: AgentState) -> AgentState:
#     """Submit approved invoice to ERP."""
#     invoice = state["invoice"]
#     if invoice.status == InvoiceStatus.APPROVED:
#         erp_entry = create_erp_entry(invoice, get_erp_client())
#         invoice.status = InvoiceStatus.SUBMITTED
#     return {"invoice": invoice, "current_step": "submitted"}


# def build_graph():
#     """Build the LangGraph workflow."""
#     workflow = StateGraph(AgentState)
    
#     workflow.add_node("extract", extract_node)
#     workflow.add_node("match_po", match_po_node)
#     workflow.add_node("gl_code", gl_code_node)
#     workflow.add_node("human_review", human_review_node)
#     workflow.add_node("submit_erp", submit_erp_node)
    
#     workflow.set_entry_point("extract")
#     workflow.add_edge("extract", "match_po")
#     workflow.add_edge("match_po", "gl_code")
#     workflow.add_edge("gl_code", "human_review")
#     workflow.add_edge("human_review", "submit_erp")
#     workflow.add_edge("submit_erp", END)
    
#     return workflow.compile()