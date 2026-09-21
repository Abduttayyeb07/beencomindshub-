"""Operator-owned model routing. Never load gateway credentials from user settings."""
from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Credentials and routing targets stay server-owned: the gateway is the only
# component that holds AWS keys, so nothing here may be set from the browser.
LOCKED_MODEL_FIELDS = frozenset({
    "managed_models", "anthropic_api_key", "openai_api_key", "minds_api_key",
    "minds_url", "openai_base_url", "planning_provider", "coding_provider",
    "providers_json",
})

# Which model each role uses is a user choice, not a credential. These stay
# writable under managed mode so the model picker works; the value is just an
# alias the gateway resolves, and an unknown alias fails at the gateway
# rather than exposing anything.
UNLOCKED_MODEL_FIELDS = frozenset({
    "planning_model", "coding_model", "model_mode", "model_overrides",
})


class ManagedModels(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="COWORK_MANAGED_", env_file=".env", extra="ignore")
    enabled: bool = False
    base_url: str = "http://model-gateway:4000/v1"
    api_key: SecretStr | None = None
    planning_model: str = "planning"
    coding_model: str = "coding"

    @model_validator(mode="after")
    def validate_enabled(self):
        if self.enabled:
            if not self.api_key or not self.api_key.get_secret_value().strip():
                raise ValueError("COWORK_MANAGED_API_KEY must contain a restricted gateway key")
            if not self.base_url.startswith(("http://", "https://")):
                raise ValueError("COWORK_MANAGED_BASE_URL must be an HTTP(S) URL")
            if not self.planning_model.strip() or not self.coding_model.strip():
                raise ValueError("Managed planning and coding model names cannot be empty")
        return self


def get_managed_models() -> ManagedModels:
    return ManagedModels()


def check_model_write(key: str) -> None:
    if key == "managed_models" or (get_managed_models().enabled and key in LOCKED_MODEL_FIELDS):
        raise ValueError(
            "Provider credentials are managed by the server administrator. "
            "Model selection is available."
        )
