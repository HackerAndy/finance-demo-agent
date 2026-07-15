# finance-db on a Mac mini — Docker Compose + Cloudflare Tunnel

Same finance database as the k3s deployment (`../finance-db`), rehosted on a
Mac mini outside the home network. Docker Compose replaces Kubernetes; the
**migrations, images, API, and Cloudflare pattern are identical**. The
migration files are shared from `../finance-db/migrations/` — one schema
history for both hosts.

Security model: every container port binds to `127.0.0.1` only. Nothing on
the mini's network can reach Postgres or the API directly. The single public
entry is a Cloudflare Tunnel (outbound-only — no inbound ports opened on
whatever network the mini sits on) to the read-only PostgREST API, protected
by Cloudflare Access.

## Layout

```
finance-db-macmini/
├── docker-compose.yml   # postgres + flyway (one-shot) + postgrest
├── .env.example         # copy to .env, set the DB password
└── README.md
```

Migrations are NOT copied here — the compose file mounts
`../finance-db/migrations/`, so copy the whole `deploy/` folder (or the repo)
to the mini, not just this directory.

## One-time setup on the Mac mini

### 1. Install Docker + get the files

```bash
brew install orbstack          # or Docker Desktop; OrbStack is lighter
# copy the repo (or at least the deploy/ folder) onto the mini, then:
cd deploy/finance-db-macmini
cp .env.example .env           # edit: set a strong alphanumeric password
```

Set OrbStack/Docker Desktop to **start at login** (app settings) so the stack
survives reboots — the containers themselves have `restart: unless-stopped`.

### 2. Start the stack

```bash
docker compose up -d
docker compose logs flyway     # expect: Successfully applied 3 migrations
curl http://localhost:3000/gl_codes   # 12 GL codes as JSON
```

Startup order is handled by compose: postgres (waits for healthy) → flyway
(runs migrations, exits) → postgrest.

### 3. Cloudflare Tunnel

The mini is on a different network than the Pi cluster, so it gets its own
tunnel under the same Cloudflare account:

```bash
brew install cloudflared
cloudflared tunnel login                 # browser opens; pick klabsusa.com
cloudflared tunnel create mac-mini       # note the tunnel ID it prints
```

Create `~/.cloudflared/config.yml` (substitute the tunnel ID and your macOS
username):

```yaml
tunnel: <TUNNEL_ID>
credentials-file: /Users/<username>/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: finance-api2.klabsusa.com
    service: http://localhost:3000
  - service: http_status:404
```

Then create the DNS record and install cloudflared as a boot service:

```bash
cloudflared tunnel route dns mac-mini finance-api2.klabsusa.com
sudo cloudflared service install
```

Verify from any machine:

```bash
curl https://finance-api2.klabsusa.com/gl_codes
```

### 4. Cloudflare Access (mandatory — this host is public)

The API is anonymous read-only; without Access, anyone with the URL can read
every table. At [one.dash.cloudflare.com](https://one.dash.cloudflare.com):

1. **Access → Applications → Add an application → Self-hosted**
2. Application domain: `finance-api2.klabsusa.com`
3. Policy: Allow → Include → **Emails** → your email → Save

Browser requests now require a one-time PIN emailed to you. Note this also
blocks Excel's anonymous refresh through this hostname — for programmatic
access (Excel, the agent), create an Access **service token** and send its
two headers with each request (in Power Query: the `Headers` option of
`Web.Contents`).

## Endpoints

Same tables as the k3s deployment — see the endpoint list in
[../finance-db/README.md](../finance-db/README.md). Base URL here:
`https://finance-api2.klabsusa.com`.

## Day-2 operations

```bash
# apply a newly added ../finance-db/migrations/V4__*.sql
docker compose up flyway

# psql shell into the database
docker compose exec postgres psql -U finance finance

# status / logs
docker compose ps
docker compose logs -f postgrest

# recreate from scratch (deletes all data!)
docker compose down -v && docker compose up -d
```

Migration rule is unchanged: new `V*__*.sql` files only, never edit applied
ones — Flyway checksums them, and both this host and the Pi cluster replay
the same files.
