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


## Security

**Set `COWORK_AUTH_PASSWORD` (and optionally `COWORK_AUTH_EMAIL`) in `.env`.**
That is the sign-in page. There is no signup and no user list: one shared
credential, checked against the environment. Leave the password empty and the
app is open to anyone who can reach it.

```bash
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

Signing in sets an HttpOnly session cookie, so the password isn't stored in the
browser and page scripts can't read the session. Failed attempts are rate
limited. `COWORK_API_TOKEN` is separate, for scripts calling the API directly.

**Before exposing this beyond localhost**, serve it over HTTPS and set
`COWORK_COOKIE_SECURE=true` — otherwise the password and session travel in
clear text. One shared password also cannot be revoked per person or tell you
who did what; for that, use `deploy/aws/` with OIDC.

See [docs/SECURITY-AUDIT.md](../docs/SECURITY-AUDIT.md) for the full endpoint
review.

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
