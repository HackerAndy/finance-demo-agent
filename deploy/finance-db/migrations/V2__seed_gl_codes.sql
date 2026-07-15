-- Seed GL master data, kept in sync with core/validators/gl_codes.py.
-- Update quarterly from ERP export (see CLAUDE.md).

INSERT INTO gl_codes (code, name, category, is_active) VALUES
    ('4000', 'Revenue - Product Sales',  'Revenue', TRUE),
    ('4010', 'Revenue - Services',       'Revenue', TRUE),
    ('5000', 'COGS - Materials',         'COGS',    TRUE),
    ('5010', 'COGS - Labor',             'COGS',    TRUE),
    ('6000', 'General Expense',          'OpEx',    TRUE),
    ('6100', 'Office Supplies',          'OpEx',    TRUE),
    ('6200', 'Software & SaaS',          'OpEx',    TRUE),
    ('6300', 'Professional Services',    'OpEx',    TRUE),
    ('6400', 'Travel & Entertainment',   'OpEx',    TRUE),
    ('6500', 'Rent & Utilities',         'OpEx',    TRUE),
    ('7000', 'Payroll',                  'OpEx',    TRUE),
    ('8000', 'Marketing',                'OpEx',    TRUE);
