-- Initial schema for the finance demo agent.
-- Tables mirror the Pydantic models in core/models.py.

CREATE TYPE invoice_status AS ENUM (
    'received',
    'extracted',
    'po_matched',
    'gl_coded',
    'submitted',
    'approved',
    'rejected',
    'escalated'
);

CREATE TABLE gl_codes (
    code       TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT NOT NULL,
    is_active  BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE purchase_orders (
    po_number     TEXT PRIMARY KEY,
    vendor_id     TEXT NOT NULL,
    total_amount  NUMERIC(14, 2) NOT NULL,
    status        TEXT NOT NULL
);

CREATE TABLE po_line_items (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    po_number   TEXT NOT NULL REFERENCES purchase_orders (po_number) ON DELETE CASCADE,
    description TEXT NOT NULL,
    quantity    NUMERIC(12, 3) NOT NULL,
    unit_price  NUMERIC(14, 4) NOT NULL,
    gl_code     TEXT REFERENCES gl_codes (code)
);

CREATE TABLE invoices (
    invoice_id    TEXT PRIMARY KEY,
    vendor_name   TEXT NOT NULL,
    vendor_id     TEXT,
    invoice_date  TIMESTAMPTZ NOT NULL,
    due_date      TIMESTAMPTZ,
    total_amount  NUMERIC(14, 2) NOT NULL,
    currency      CHAR(3) NOT NULL DEFAULT 'USD',
    po_number     TEXT REFERENCES purchase_orders (po_number),
    status        invoice_status NOT NULL DEFAULT 'received',
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE invoice_line_items (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    invoice_id  TEXT NOT NULL REFERENCES invoices (invoice_id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    quantity    NUMERIC(12, 3) NOT NULL,
    unit_price  NUMERIC(14, 4) NOT NULL,
    gl_code     TEXT REFERENCES gl_codes (code)
);

CREATE TABLE audit_records (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    invoice_id   TEXT NOT NULL REFERENCES invoices (invoice_id) ON DELETE CASCADE,
    occurred_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    actor        TEXT NOT NULL,  -- 'system', 'human', 'agent'
    action       TEXT NOT NULL,
    from_status  invoice_status,
    to_status    invoice_status,
    details      JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE erp_entries (
    invoice_id           TEXT PRIMARY KEY REFERENCES invoices (invoice_id),
    erp_document_number  TEXT NOT NULL,
    posted_date          TIMESTAMPTZ NOT NULL,
    status               TEXT NOT NULL
);

CREATE INDEX idx_invoices_status ON invoices (status);
CREATE INDEX idx_invoices_po_number ON invoices (po_number);
CREATE INDEX idx_audit_records_invoice ON audit_records (invoice_id, occurred_at);
