"""
Cowork Server — FastAPI Application.

This module sets up the FastAPI application with middleware, routing,
and all necessary configurations for the Cowork service.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from cowork.api.v1.router import api_router as v1_router
from cowork.common.logger import setup_logging
from cowork.common.settings.app_settings import get_app_settings
from cowork.dev_setup import run_dev_setup
from cowork.scheduler import start_scheduler


# Set up logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_dev_setup()
    start_scheduler()
    await app.state.channel_adapters.refresh_all()
    from cowork.channels.ingress import sync_channel_ingress
    from cowork.channels.registry import get_registry

    for plugin in get_registry().all():
        await sync_channel_ingress(
            app.state.channel_ingress, app.state.channel_adapters, plugin.channel_type
        )
    try:
        yield
    finally:
        from cowork.channels.webhooks import drain_background_tasks
        from cowork.common.http_client import close_proxy_client
        from cowork.services.artifacts import shutdown_launched_backends
        from cowork.services.scratchpad_runtime import close_all as close_scratchpads

        await app.state.channel_ingress.stop_all()
        await drain_background_tasks()
        await app.state.channel_adapters.shutdown()
        shutdown_launched_backends()
        await close_scratchpads()
        await close_proxy_client()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """

    settings = get_app_settings()

    # Create FastAPI app
    app = FastAPI(
        title="Cowork API",
        description="Cowork server — OpenAI-compatible Responses API with pluggable harness backends",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Configure CORS middleware.
    #
    # This used to be allow_origins=["*"] with allow_credentials=True. Starlette
    # resolves that combination by echoing back whatever Origin the request
    # carried, so every website a user had open could call this API and read the
    # responses — and the API has no authentication of its own, so that meant
    # reading provider keys, stored connections and project files, and starting
    # agent runs. Restricted to an explicit list instead; note that both
    # supported setups serve the UI through a proxy and are therefore
    # same-origin, so they never exercise this path.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_app_settings().cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=3600,
    )

    _install_api_token_gate(app, settings.api_token)

    # Include v1 API routes
    app.include_router(v1_router)

    _install_channels(app)

    logger.info("Cowork application created successfully")
    return app


def _install_api_token_gate(app: FastAPI, token: str) -> None:
    """Require a shared secret on every request when COWORK_API_TOKEN is set.

    The API has no user accounts, so without this anything able to reach the
    port can read provider keys and stored connections and start agent runs.
    Off when the token is empty, which keeps existing setups working.

    Exempt:
      - the health route, so container healthchecks work;
      - CORS preflights, which browsers send without custom headers;
      - inbound channel webhooks, which external services call and which
        verify their own signatures (see cowork/channels/webhooks.py).

    The token is read from a header, a cookie or a query parameter: assets the
    browser loads itself (an <img> or <iframe> pointing at an artifact) cannot
    set headers. The reverse proxy serving the UI is expected to inject it, so
    the browser never has to hold it.
    """
    if not token:
        return

    import hmac

    from starlette.responses import JSONResponse

    @app.middleware("http")
    async def require_api_token(request: Request, call_next):
        path = request.scope.get("path", "")
        exempt = (
            request.method == "OPTIONS"
            or path.rstrip("/") == "/api/v1/health"
            or any(rx.match(path) for rx in getattr(app.state, "webhook_path_regexes", ()))
        )
        if not exempt:
            supplied = (
                request.headers.get("x-cowork-token")
                or request.cookies.get("cowork_token")
                or request.query_params.get("cowork_token")
                or ""
            )
            # compare_digest: keep the comparison time independent of how much
            # of the token a guess got right.
            if not hmac.compare_digest(supplied, token):
                return JSONResponse({"detail": "Not authenticated"}, status_code=401)
        return await call_next(request)


def _install_channels(app: FastAPI) -> None:
    """Discover channel plugins, mount their webhook routes, and build the
    Anton-only channel runtime + live-adapter registry.

    The registry/runtime are stashed on ``app.state`` so the lifespan can build
    adapters from stored credentials at startup and tear them down on shutdown.
    Webhook routes resolve the live adapter synchronously through the registry's
    cache, which the lifespan populates — so routes are mounted here but only
    serve once a channel is configured (otherwise the route ACK-ignores: 204).
    """
    from cowork.channels.ingress import IngressManager
    from cowork.channels.registry import get_registry, load_first_party_plugins
    from cowork.channels.runtime import AntonChannelRuntime, LiveAdapterRegistry
    from cowork.channels.webhooks import build_channel_webhook_router

    load_first_party_plugins()
    adapters = LiveAdapterRegistry()
    runtime = AntonChannelRuntime(adapters)
    # Remember which paths belong to webhooks so the API-token gate can let
    # them through: they are called by Slack/Telegram/etc., which cannot send
    # our header, and they authenticate callers by signature instead.
    webhook_path_regexes = []
    for plugin in get_registry().all():
        if not plugin.webhooks:
            continue
        before = len(app.routes)
        app.include_router(
            build_channel_webhook_router(plugin, resolver=adapters.get, sink=runtime.handle),
            prefix="/api/v1/channels",
        )
        for route in app.routes[before:]:
            regex = getattr(route, "path_regex", None)
            if regex is not None:
                webhook_path_regexes.append(regex)
    app.state.webhook_path_regexes = tuple(webhook_path_regexes)
    app.state.channel_adapters = adapters
    app.state.channel_runtime = runtime
    app.state.channel_ingress = IngressManager(sink=runtime.handle)


# Create the application instance
app = create_app()
