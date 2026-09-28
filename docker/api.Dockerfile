# cowork-server (FastAPI) + the Anton agent it embeds.
#
# Built from the repo root:   docker build -f docker/api.Dockerfile .

# uv comes from PyPI rather than its GHCR image: PyPI is already required to
# build this image, and some hosts cannot reach ghcr.io at all (it refuses even
# `docker login`), which failed the build here.
ARG UV_VERSION=0.12.14

# ─── builder ──────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder
ARG UV_VERSION

# git: hermes-agent is a git dependency in backend/core_api/pyproject.toml.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "uv==${UV_VERSION}"

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Third-party dependencies first, from the manifests alone. Editing any source
# file leaves this layer cached, so a rebuild reinstalls nothing — previously a
# one-character change re-ran the whole two-minute install. The two local
# packages are excluded here because their sources are not copied yet.
WORKDIR /src
COPY backend/core_api/pyproject.toml backend/core_api/uv.lock ./core_api/
COPY backend/core_agent/pyproject.toml ./core_agent/
WORKDIR /src/core_api
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable \
        --no-install-project --no-install-package anton-agent

# Now the sources, and the two local packages on top of the cached deps.
# --no-editable copies anton (a path dependency on ../core_agent) into the venv
# instead of linking to /src, so the runtime stage needs only /opt/venv.
WORKDIR /src
COPY backend/core_agent/ ./core_agent/
COPY backend/core_api/ ./core_api/
WORKDIR /src/core_api
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# ─── runtime ──────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime
ARG UV_VERSION

LABEL org.opencontainers.image.title="cowork-api"

# gcc + libpq-dev: the agent's scratchpad installs packages at runtime, and a
# Postgres connector probe may `pip install psycopg2`, which builds from source.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 -s /bin/bash cowork

# uv on PATH: the scratchpad provisions its per-session venvs with it
# (anton/core/backends/local.py falls back to a slower stdlib venv without it).
# Copied from the builder rather than installed again — same binary, and it
# saves repeating the download in this stage.
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

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
