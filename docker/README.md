# Running with Docker

The whole stack — UI, API, agent, and the Bedrock model gateway — in one command.

```
browser ─► web (nginx :3000) ─► api (cowork-server) ─► model-gateway (LiteLLM) ─► AWS Bedrock
```

## Start

```bash
cp .env.example .env        # then fill in AWS credentials and LITELLM_MASTER_KEY
docker compose up -d --build
```

Open **http://localhost:3000**. The first build takes several minutes; later
starts take seconds.

## Everyday commands

| Task | Command |
|---|---|
| Start / rebuild after code changes | `docker compose up -d --build` |
| Stop | `docker compose down` |
| Follow logs | `docker compose logs -f api` (or `web`, `model-gateway`) |
| Status and health | `docker compose ps` |
| Apply a gateway routing change | `docker compose restart model-gateway` |

`docker compose down` keeps your data. `docker compose down -v` **deletes** it —
conversations, projects, and saved connector credentials.

## Configuration

Everything lives in `.env` (see `.env.example`):

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` — Bedrock access.
  Only the gateway container receives these.
- `LITELLM_MASTER_KEY` — shared secret between the api and the gateway. Any long
  random string.
- `WEB_PORT` — UI port, default `3000`.
- `COWORK_ENABLED_CONNECTORS` — connectors offered under *Connect Apps and Data*.
- `ANTON_VAULT_KEY` — optional; see below.

Which Bedrock model serves each request is decided by the gateway's routing
policy: `deploy/local/litellm-config.yaml`, explained in `deploy/local/ROUTING.md`.

## Data

All state lives in the `cowork-data` volume, mounted at `/home/cowork/.cowork`:
the database, projects, Hermes state, and the connector vault.

Connector credentials are encrypted at rest. The encryption key is generated
into the same volume (`.vault.key`) unless you set `ANTON_VAULT_KEY`. Setting it
keeps the key out of the volume, so a copied volume alone can't be decrypted.
**Lose the key and saved connections can't be read** — they have to be re-entered.

This state is separate from a `npm run dev:web` setup, which keeps its own under
`~/.cowork` on the host.

## Security

**This setup has no login.** The UI is published on localhost only, and the API
and gateway aren't published at all — keep it that way. The API has no
authentication of its own, so anyone who can reach it can use it, along with
every saved connector credential.

For a deployment other people can reach, use `deploy/aws/`, which puts an OIDC
login in front and gives the gateway an IAM role instead of static keys.

The web image is built with `VITE_AUTH_MODE=none`, which skips the upstream
MindsHub SSO login. That login is part of MindsHub's hosted product; in this
deployment it would redirect to an account you don't have.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `set AWS_ACCESS_KEY_ID in .env` on start | `.env` is missing or incomplete |
| `web` never starts | `api` isn't healthy yet — check `docker compose logs api` |
| Replies fail with a model error | Check `docker compose logs model-gateway`; confirm the model is enabled for your account in the Bedrock console |
| Port 3000 in use | Set `WEB_PORT` in `.env` |
