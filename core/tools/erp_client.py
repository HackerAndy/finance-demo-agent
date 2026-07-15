"""
ERP client adapter - core tool, no framework imports.
Interface + production adapter pattern for testability.
"""
from abc import ABC, abstractmethod
from typing import Optional
from ..models import Invoice, ERPEntry


class ERPClient(ABC):
    """Abstract interface for ERP systems."""
    
    @abstractmethod
    def create_entry(self, invoice: Invoice) -> ERPEntry:
        """Create ERP entry from coded invoice. Returns ERP document number."""
        pass
    
    @abstractmethod
    def validate_connection(self) -> bool:
        """Test ERP connectivity."""
        pass


class MockERPClient(ERPClient):
    """Test adapter - records calls, returns fake document numbers."""
    
    def __init__(self):
        self.calls = []
    
    def create_entry(self, invoice: Invoice) -> ERPEntry:
        self.calls.append(invoice)
        return ERPEntry(
            invoice_id=invoice.invoice_id,
            erp_document_number=f"TEST-{invoice.invoice_id}",
            posted_date=__import__("datetime").datetime.now(),
            status="posted"
        )
    
    def validate_connection(self) -> bool:
        return True


class ProductionERPClient(ERPClient):
    """Production adapter - calls real ERP API."""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    def create_entry(self, invoice: Invoice) -> ERPEntry:
        # TODO: Implement real ERP API call
        raise NotImplementedError("Production ERP client not implemented")
    
    def validate_connection(self) -> bool:
        # TODO: Implement real connectivity check
        raise NotImplementedError("Production ERP client not implemented")


def create_erp_entry(invoice: Invoice, client: ERPClient) -> ERPEntry:
    """
    Factory function to create ERP entry using injected client.
    
    This is the tool entry point - takes Pydantic models, returns Pydantic models.
    """
    return client.create_entry(invoice)