# API security audit

Covers all 119 operations across 82 paths exposed by `cowork-server`, taken
from the live OpenAPI schema. Date: 2026-09-24.

## Summary

| | |
|---|---|
| Operations reviewed | 119 |
| Vulnerabilities found and fixed | 4 |
| Weaknesses noted, not fixed | 3 |
| Endpoints requiring authentication before this audit | **0** |

The dominant finding was that the API had no authentication of any kind. Every
per-endpoint rating below is conditional on who can reach the port, which is why
the token gate matters more than any individual endpoint fix.

## Fixed

### 1. Stored connector credentials returned in plaintext — high

`GET /api/v1/connectors/connections/{engine}/{name}` returned the full stored
credential, including database passwords, to any caller.

Masking keys off each record's `secure_keys` list, but the save path
(`handlers/probe.py`, both save sites) never recorded one, so the list was
always empty and nothing was masked. Confirmed live against a real production
Postgres URI.

Fixed by recording `secure_keys` on save from the connector spec's
`secret: true` fields, and by making the read path fall back to the spec and
then to a field-name heuristic, so a record without the list can never read
back unmasked. Tests: `tests/test_connection_secrets.py`.

### 2. Any website could call the API — high

CORS was `allow_origins=["*"]` with `allow_credentials=True`. Starlette resolves
that by echoing back whatever `Origin` the request carried, so a page on any
site the user had open could call every endpoint and read the responses — with
no authentication in the way. Verified: the server returned
`access-control-allow-origin: https://evil.example`.

Fixed by restricting to an explicit origin list (`COWORK_CORS_ALLOW_ORIGINS`).
Both supported setups proxy the API under the UI's origin, so normal use is
same-origin and unaffected. Tests: `tests/test_cors.py`.

### 3. No authentication on any endpoint — high

Anything that could reach port 26866 could read provider keys, list and read
stored connections, read and write project files, and start agent runs (which
execute code).

Fixed by adding `COWORK_API_TOKEN`: when set, every request must carry it as an
`X-Cowork-Token` header, a `cowork_token` cookie, or a query parameter — the
last two because assets the browser loads itself (`<img>`, `<iframe>`) cannot
set headers. The reverse proxy injects it, so the browser never holds it.
Exempt: the health route, CORS preflights, and inbound channel webhooks, which
verify their own signatures. Empty disables the check, so existing setups keep
working. Tests: `tests/test_api_token.py`.

### 4. Editing a connection destroyed the stored secret — medium (data loss)

The read path masked secrets with the string `"ANTON_VAULT_KEEP"` — the *name*
of the sentinel constant rather than its value (`__anton_vault_keep__`) — and
nothing called `resolve_modify_merge()`, the function that turns the sentinel
back into the stored value on save. Re-submitting a connection form with a
masked field untouched would therefore overwrite the real credential with the
placeholder. Fixed alongside #1.

## Noted, not fixed

- **`GET /api/v1/settings/reveal-key/{name}`** returns a provider API key in
  plaintext by design (the UI's "reveal" button). Now behind the token gate,
  but it remains the single most valuable endpoint on the server.
- **`POST /api/v1/settings/raw`** overwrites `~/.anton/.env` with arbitrary
  content. Variables from that file are applied to the server process, though
  only where the name is not already set — so `PATH` cannot be hijacked, but a
  new variable such as an alternate provider base URL can be introduced.
- **Artifact preview/proxy tokens are `sha256(path)[:16]`**, derived
  deterministically from the directory path rather than randomly generated.
  Anyone who can guess the path can compute the token. They are not secrets and
  should not be treated as an access control.

## Verified sound

- **Path traversal** — `projects/{name}/files/{path}`, `files-raw/{path}`,
  `artifacts/serve/{project}/{path}` and `artifacts/preview-asset/{token}/{path}`
  all reject traversal (`../`, encoded, and doubled forms tested live; 400/404,
  nothing served). `preview_asset` resolves and then checks containment with
  `relative_to`.
- **Sensitive settings** are returned as `null` by `GET /api/v1/settings/`;
  only the explicit reveal endpoint exposes a value.
- **Channel configs** mask their secrets on read — the pattern the connector
  code should have followed.

## Per-endpoint ratings

Ratings assume the token gate is enabled. "Powerful" means the endpoint is
supposed to do something far-reaching, so it is only as safe as the gate.

| Group | Ops | Rating | Notes |
|---|---|---|---|
| settings | 12 | Powerful | `reveal-key` returns a key; `raw` read/write touches `.env` |
| connectors | 9 | Powerful | Credential storage; masking fixed (#1, #4); OAuth callback is externally reachable by design |
| channels | 15 | Powerful | Bot tokens; masked on read; webhooks exempt from the gate and verify signatures |
| responses / scratchpad | 6 | Powerful | Runs the agent, which executes code by design |
| projects | 13 | Sensitive | Arbitrary read/write inside project directories; traversal blocked |
| artifacts | 13 | Sensitive | Serves files; traversal blocked; tokens are not secrets |
| attachments / files | 11 | Sensitive | Upload and raw download of stored files |
| publish | 3 | Sensitive | Sends artifact content to an external service |
| schedules | 10 | Sensitive | Creates recurring unattended agent runs |
| skills / memory | 9 | Moderate | Content the agent later acts on |
| conversations | 7 | Moderate | Message history |
| integrations | 2 | Moderate | OAuth initiation |
| pins / search / browse / health | 7 | Low | Read-mostly local metadata |

## Residual risk

- The token is a single shared secret with no rotation, expiry, users or audit
  log. It stops an unauthenticated caller; it does not distinguish between them.
- A cross-origin page still cannot read responses (CORS) but can cause a
  request to be *sent* through the proxy. FastAPI's JSON endpoints require a
  preflight, which CORS blocks, so this is limited — but it is not a CSRF
  token.
- DNS rebinding against `localhost` is not specifically mitigated; the token
  gate is the effective defence.
- Anything running as your user on the machine can read
  `~/.cowork/.vault.key`, the database, and the `.env` files directly, without
  touching the API.
