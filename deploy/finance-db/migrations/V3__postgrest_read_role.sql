-- Read-only role for PostgREST (Excel/web access).
-- web_anon cannot log in; PostgREST connects as 'finance' and switches to
-- web_anon for anonymous requests, so the API is read-only.

CREATE ROLE web_anon NOLOGIN;

GRANT USAGE ON SCHEMA public TO web_anon;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO web_anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO web_anon;

GRANT web_anon TO finance;
