# Cowork

An agent workspace for knowledge work and software development — chat with
agents that can run code, read documents, query your databases, build
artifacts, and run on a schedule. Every model call goes to **AWS Bedrock** in
your own account.

```
browser ─► web UI ─► api (cowork-server) ─► agent (Anton / Hermes) ─► model gateway (LiteLLM) ─► AWS Bedrock
```

## Quick start (Docker)

The whole stack in one command. Needs Docker and an AWS account with Bedrock
model access.

```bash
cp .env.example .env          # fill in AWS credentials and LITELLM_MASTER_KEY
docker compose up -d --build
```

Open **http://localhost:3000**. The first build takes a few minutes.

Day-to-day commands, configuration, data and troubleshooting:
[docker/README.md](docker/README.md).

## What's inside

- **Agents** — two interchangeable harnesses, Anton (default) and Hermes,
  switchable in Settings. Both run multi-step tool use, including a Python
  scratchpad for code, file and document work.
- **Model routing** — the agent asks for a role (`planning`, `coding`), and the
  gateway picks the Bedrock model by capability, cost and latency, with
  failover. Any single model can also be pinned in Settings. See
  [deploy/local/ROUTING.md](deploy/local/ROUTING.md).
- **Connectors** — Postgres, ClickHouse, Redis, Slack, Notion and ClickUp,
  added under *Connect Apps and Data*. Credentials are encrypted at rest and
  reach the agent only as environment variables, never in its prompt.
- **Documents** — attach PDFs and other files, including scanned documents,
  which are read through the model's vision.
- **Scheduling** — run a prompt once, hourly, daily or weekly, with a recorded
  history of every run.
- **Artifacts and memory** — agent output saved as documents, dashboards and
  apps, plus memory that carries across conversations.

## Repository layout

| Path | What it is |
|---|---|
| `frontend/` | Web UI and Electron desktop app (React, Vite) |
| `backend/core_api/` | `cowork-server` — the FastAPI backend: API, scheduler, connectors, harness integration |
| `backend/core_agent/` | `anton` — the agent: reasoning loop, tools, scratchpad, credential vault |
| `backend/data-vault/` | Data-integration engine used by connectors |
| `deploy/local/` | Bedrock model gateway for local use, and its routing policy |
| `deploy/aws/` | Production deployment on AWS (OIDC login, IAM role, budget limits) |
| `docker/` | Dockerfiles and nginx config for the one-command stack |

`backend/core_api` depends on `backend/core_agent` by local path, so changes to
the agent take effect without a release.

## Local development

For working on the code with hot reload. Needs Node 22,
[uv](https://docs.astral.sh/uv/), and Docker (for the model gateway).

**1. Start the model gateway**

```bash
cp deploy/local/.env.example deploy/local/.env     # AWS credentials + LITELLM_MASTER_KEY
docker compose -f deploy/local/docker-compose.yml up -d
```

**2. Point the backend at it**

```bash
cp backend/core_api/.env.example backend/core_api/.env
# set COWORK_MANAGED_API_KEY to the same value as LITELLM_MASTER_KEY
```

**3. Skip the upstream sign-in in the dev UI**

```bash
echo "VITE_AUTH_MODE=none" > frontend/src/renderer/.env.local
```

**4. Run**

```bash
cd frontend
npm install
npm run dev:web
```

Open **http://localhost:5173**. `dev:web` starts the backend itself and
reloads on changes. This keeps its state in `~/.cowork` on your machine,
separate from the Docker stack's volume.

### Tests

```bash
cd backend/core_api  && uv run --with pytest --with pytest-asyncio pytest tests
cd backend/core_agent && uv run --with pytest --with pytest-asyncio pytest tests
```

On Windows, add `--basetemp` pointing at a writable directory if pytest can't
write to the default temp folder. Two permission tests in `core_agent` check
POSIX file modes and fail on Windows only.

## Security

**The API has no user accounts.** Set `COWORK_API_TOKEN` in `.env`: every
request must then carry it, and the web container injects it for you, so the
browser never holds it. Without it, anything able to reach the port can use the
agents and read every saved connector credential.

The Docker stack publishes the UI on `localhost` only and doesn't publish the
API or gateway at all — keep it that way. A full review of all 119 endpoints is
in [docs/SECURITY-AUDIT.md](docs/SECURITY-AUDIT.md).

For a deployment other people can reach, use [deploy/aws/](deploy/aws/), which
puts an OIDC login in front and gives the gateway an IAM role instead of static
keys.

Never commit `.env` files: they hold live AWS credentials and the gateway key,
and are gitignored.

## License

This repository combines components under different licenses:

| Component | License |
|---|---|
| `frontend/` | AGPL-3.0 |
| `backend/core_api/` | Proprietary — see [backend/core_api/LICENSE](backend/core_api/LICENSE) |
| `backend/core_agent/` | MIT |
| `backend/data-vault/` | See [backend/data-vault/LICENSE](backend/data-vault/LICENSE) |
| Everything else | MIT — see [LICENSE](LICENSE) |

Based on the Cowork platform by MindsDB, Inc. Each component's license file is
authoritative.
