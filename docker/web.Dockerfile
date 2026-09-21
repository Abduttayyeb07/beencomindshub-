# Web UI: the renderer built as a static SPA, served by nginx, which also
# reverse-proxies /api/ to the api service.
#
# Built from the repo root:   docker build -f docker/web.Dockerfile .

FROM node:22-slim AS builder

WORKDIR /build
COPY frontend/package.json frontend/package-lock.json ./
# --ignore-scripts: skips Electron's postinstall binary download, which the
# web build never uses.
RUN npm ci --ignore-scripts
COPY frontend/ ./

# How the SPA authenticates. "none" skips the MindsHub (Keycloak) SSO login —
# this deployment has no MindsHub account, and that login flow would write a
# MindsHub token into settings. Note the API itself has no authentication
# either way, so access control has to come from the network: compose binds the
# UI to localhost only. For anything network-reachable use deploy/aws/, which
# puts OIDC in front.
ARG VITE_AUTH_MODE=none
ENV VITE_AUTH_MODE=${VITE_AUTH_MODE}

RUN npm run build:web

# ─── runtime ──────────────────────────────────────────────────────────────────
FROM nginx:alpine AS runtime

LABEL org.opencontainers.image.title="cowork-web"

COPY --from=builder /build/dist/renderer-web/ /usr/share/nginx/html/
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
