# cowork-server (FastAPI) + the Anton agent it embeds.
#
# Built from the repo root:   docker build -f docker/api.Dockerfile .

ARG UV_VERSION=0.12.14

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

# ─── builder ──────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# git: hermes-agent is a git dependency in backend/core_api/pyproject.toml.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /src
COPY backend/core_agent/ ./core_agent/
COPY backend/core_api/ ./core_api/

# Install exactly what uv.lock pins. --no-editable copies anton (a path
# dependency on ../core_agent) into the venv instead of linking to /src, so the
# runtime stage needs only /opt/venv.
WORKDIR /src/core_api
RUN uv sync --frozen --no-dev --no-editable

# ─── runtime ──────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="cowork-api"

# gcc + libpq-dev: the agent's scratchpad installs packages at runtime, and a
# Postgres connector probe may `pip install psycopg2`, which builds from source.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 -s /bin/bash cowork

# uv on PATH: the scratchpad provisions its per-session venvs with it
# (anton/core/backends/local.py falls back to a slower stdlib venv without it).
COPY --from=uv /uv /usr/local/bin/uv
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    COWORK_SERVER_HOST=0.0.0.0 \
    COWORK_SERVER_PORT=26866

# Everything the app persists — database, data vault, vault key, projects,
# Hermes state — lives under ~/.cowork, which compose mounts as a volume.
RUN mkdir -p /home/cowork/.cowork && chown cowork:cowork /home/cowork/.cowork

USER cowork
WORKDIR /home/cowork

EXPOSE 26866

# The health route is mounted under the API prefix; a bare /health is a 404,
# which previously left this container permanently "unhealthy".
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request,sys; \
sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:26866/api/v1/health/',timeout=3).status==200 else 1)"

CMD ["cowork-server"]
