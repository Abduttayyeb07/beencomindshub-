"""CLI entry points for cowork server and developer setup commands."""

import uvicorn

from cowork.common.settings.app_settings import get_app_settings
from cowork.dev_setup import run_dev_setup


def main() -> None:
    settings = get_app_settings()
    port = settings.port
    host = settings.host
    # proxy_headers: trust X-Forwarded-Proto/For from the reverse proxy in
    # front. Without it the app believes every request is plain HTTP, so its
    # trailing-slash redirects come back as http:// — which a browser on an
    # HTTPS page blocks as mixed content, making those endpoints look empty.
    # forwarded_allow_ips is safe here because the API is never published
    # directly; only the proxy can reach it.
    uvicorn.run(
        "cowork.server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


def dev_setup_main() -> None:
    """Run local dev setup (schema create + base seed data)."""
    run_dev_setup()


if __name__ == "__main__":
    main()
