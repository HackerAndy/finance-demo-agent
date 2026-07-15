"""
Evaluation runner - standalone, runs against core/ not LangGraph.
"""
from core.tools import extract_invoice_fields, match_po, suggest_gl_code
from core.validators import validate_gl_code
from core.models import Invoice, LineItem


def run_golden_set_eval(golden_set_dir: str = "evals/golden_set") -> dict:
    """
    Run evaluation on golden set invoices.
    
    Returns: {accuracy, latency, cost, per_task_metrics}
    """
    # TODO: Load golden set from files
    # For each invoice:
    #   1. extract_invoice_fields(pdf)
    #   2. match_po(invoice, po_candidates)
    #   3. suggest_gl_code for each line item
    #   4. validate_gl_code on all suggested codes
    # Compare against expected outputs
    
    return {
        "extraction_accuracy": 0.0,
        "po_match_rate": 0.0,
        "gl_accuracy_top20": 0.0,
        "avg_latency_seconds": 0.0,
        "total_cost_usd": 0.0,
        "failed_cases": []
    }


if __name__ == "__main__":
    results = run_golden_set_eval()
    print(f"Evaluation Results: {results}")