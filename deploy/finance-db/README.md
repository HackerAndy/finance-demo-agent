# finance-db — PostgreSQL on the k3s cluster

PostgreSQL 16 for the finance demo agent, deployed with plain Kubernetes
manifests via `k3s kubectl` (same style as the other cluster projects). The
schema lives entirely in versioned Flyway migrations (`migrations/`), so the
full history is in git and the database can be recreated from scratch with one
command.

## Layout

```
finance-db/
├── apply.sh               # one-command deploy + migrate (idempotent)
├── migrations/            # Flyway versioned SQL — the schema history
│   ├── V1__initial_schema.sql
│   └── V2__seed_gl_codes.sql
└── k8s/
    ├── 01-namespace.yaml      # finance namespace
    ├── 02-statefulset.yaml    # postgres:16-alpine + 2Gi PVC (local-path), pinned to pi-node-4
    ├── 03-service.yaml        # NodePort 30432
    ├── 04-flyway-job.yaml     # flyway migrate against the migrations ConfigMap
    └── 05-postgrest.yaml      # read-only JSON API for Excel, NodePort 30480
```

The DB credentials secret (`finance-db-auth`) is created by `apply.sh` on
first run and never committed to git. The migrations ConfigMap is regenerated
from `migrations/*.sql` on every run.

## Deploy

On a cluster node, from this directory:

```bash
./apply.sh
# or, if k3s kubectl needs root on this node:
KUBECTL="sudo k3s kubectl" ./apply.sh
```

The script applies the manifests, waits for the Flyway job, and prints its
log — expect `Successfully applied 2 migrations`. Check state anytime:

```bash
k3s kubectl get pods -n finance    # finance-db-0 Running, migrate job Completed
```

## Connect

Only pi-node-1 is visible from the LAN (pi-node-2/3/4 sit on a private
switch). NodePorts are open on every node, and kube-proxy on pi-node-1
forwards to the pod on pi-node-4 — so always connect via pi-node-1 (mDNS
name `pi-node-1.local`):

```bash
psql "postgresql://finance:<password>@pi-node-1.local:30432/finance"
```

Retrieve the generated password:

```bash
k3s kubectl -n finance get secret finance-db-auth \
  -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 -d
```

From inside the cluster: `finance-db.finance.svc:5432`.

## Excel / web API (PostgREST)

PostgREST exposes every table as a read-only JSON endpoint on NodePort
**30480** (anonymous requests run as the `web_anon` role from V3 — SELECT
only). One endpoint per table:

| Endpoint | Contents |
|---|---|
| `http://finance-api.klabsusa.com:30480/invoices` | Invoice headers (status, vendor, amounts, PO link) |
| `http://finance-api.klabsusa.com:30480/invoice_line_items` | Line items per invoice, with GL code |
| `http://finance-api.klabsusa.com:30480/purchase_orders` | PO headers |
| `http://finance-api.klabsusa.com:30480/po_line_items` | Line items per PO |
| `http://finance-api.klabsusa.com:30480/gl_codes` | GL master (12 seeded codes) |
| `http://finance-api.klabsusa.com:30480/audit_records` | Status-change audit trail per invoice |
| `http://finance-api.klabsusa.com:30480/erp_entries` | Posted ERP documents |
| `http://finance-api.klabsusa.com:30480/flyway_schema_history` | Applied-migration history |

Filters and sorting go in the URL, e.g.
`/invoices?status=eq.escalated&order=invoice_date.desc` or
`/gl_codes?category=eq.OpEx`.

### Connecting Excel for Mac (verified working)

Older Mac builds lack the "From Web" button, but Blank Query reaches the
same engine:

1. **Data → Get Data (Power Query) → Blank Query**
2. Open the **Advanced Editor** (toolbar, or right-click the query)
3. Paste, adjusting the table URL as needed:

   ```
   let
       Source = Json.Document(Web.Contents("http://finance-api.klabsusa.com:30480/gl_codes")),
       Result = Table.FromRecords(Source)
   in
       Result
   ```

4. **Done** → choose **Anonymous** if prompted → columns appear →
   **Close & Load**
5. **Data → Refresh All** re-pulls live data any time; duplicate the query
   and change the URL for additional tables

On current Microsoft 365 builds (16.76+), **Get Data → From Web** with the
table URL does the same thing (then **To Table** → expand the record
column).

## Adding schema changes

1. Add a new file: `migrations/V3__describe_change.sql` (never edit an
   applied migration — Flyway checksums them).
2. Re-run `./apply.sh` — it rebuilds the ConfigMap and re-runs Flyway, which
   applies only the new migration.

## Recreate from scratch

```bash
k3s kubectl delete namespace finance   # deletes DB, data PVC, and secret!
./apply.sh
```
