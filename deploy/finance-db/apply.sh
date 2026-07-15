#!/usr/bin/env bash
# Deploy (or re-deploy) the finance database and run Flyway migrations.
# Idempotent: safe to re-run after adding a new migration file.
#
# Usage:
#   ./apply.sh                                # first run generates a password
#   FINANCE_DB_PASSWORD=... ./apply.sh        # or supply your own (first run only)
#   KUBECTL="sudo k3s kubectl" ./apply.sh     # if k3s needs sudo on this node
set -euo pipefail
cd "$(dirname "$0")"

KUBECTL=${KUBECTL:-"k3s kubectl"}
NS=finance

$KUBECTL apply -f k8s/01-namespace.yaml

# Create the auth secret on first run only — POSTGRES_PASSWORD is baked into
# the data volume at initdb, so never overwrite an existing secret.
if ! $KUBECTL -n $NS get secret finance-db-auth >/dev/null 2>&1; then
  PASSWORD=${FINANCE_DB_PASSWORD:-$(head -c 24 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 20)}
  $KUBECTL -n $NS create secret generic finance-db-auth \
    --from-literal=POSTGRES_DB=finance \
    --from-literal=POSTGRES_USER=finance \
    --from-literal=POSTGRES_PASSWORD="$PASSWORD"
  echo ">>> Created secret finance-db-auth (retrieve password with:"
  echo ">>>   $KUBECTL -n $NS get secret finance-db-auth -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 -d)"
fi

$KUBECTL apply -f k8s/02-statefulset.yaml -f k8s/03-service.yaml -f k8s/05-postgrest.yaml

# Bundle migrations/*.sql into the ConfigMap the Flyway job mounts
$KUBECTL -n $NS create configmap finance-db-migrations \
  --from-file=migrations/ --dry-run=client -o yaml | $KUBECTL apply -f -

# Jobs are immutable — remove the previous run, then apply and wait
$KUBECTL -n $NS delete job finance-db-migrate --ignore-not-found
$KUBECTL apply -f k8s/04-flyway-job.yaml
echo ">>> Waiting for migrations to complete..."
$KUBECTL -n $NS wait --for=condition=complete job/finance-db-migrate --timeout=300s
$KUBECTL -n $NS logs job/finance-db-migrate | tail -n 20
echo ">>> Done. Connect: psql postgresql://finance:<password>@<pi-ip>:30432/finance"
