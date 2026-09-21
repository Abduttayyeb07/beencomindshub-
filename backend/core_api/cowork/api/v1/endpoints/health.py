from importlib.metadata import version, PackageNotFoundError

from fastapi import APIRouter

from cowork.common.settings.user_settings import get_user_settings
from cowork.common.settings.managed_models import get_managed_models

router = APIRouter()


def _pkg_version(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


# Health endpoint — the Electron app and dev-web.mjs probe this
# to know when the server is ready before mounting the renderer.
# The cowork frontend also reads config_ready / config_error from
# this response to gate the home view input box.
@router.get("/", response_model=dict)
def health() -> dict:
    settings = get_user_settings()
    managed = get_managed_models()
    model_status = settings.config_status
    if managed.enabled:
        model_status = {
            "config_ready": True,
            "config_error": None,
            "provider": "managed-bedrock",
            "provider_label": "AWS Bedrock (managed)",
            "model": managed.planning_model,
            "managed_models": True,
        }
    return {
        "status": "ok",
        "anton_available": True,
        "mode": "anton",
        "server_version": _pkg_version("cowork-server"),
        "anton_version": _pkg_version("anton-agent"),
        **model_status,
    }
