from __future__ import annotations

import pytest
import sys
from types import ModuleType


def _enable(monkeypatch):
    monkeypatch.setenv("COWORK_MANAGED_ENABLED", "true")
    monkeypatch.setenv("COWORK_MANAGED_BASE_URL", "http://gateway.internal:4000/v1")
    monkeypatch.setenv("COWORK_MANAGED_API_KEY", "sk-internal-test")
    monkeypatch.setenv("COWORK_MANAGED_PLANNING_MODEL", "planning")
    monkeypatch.setenv("COWORK_MANAGED_CODING_MODEL", "coding")


def test_managed_mode_is_ready_without_user_api_keys(monkeypatch):
    _enable(monkeypatch)
    from cowork.api.v1.endpoints.settings import check_configured

    result = check_configured(None)
    assert result == {
        "configured": True,
        "provider": "managed-bedrock",
        "managedModels": True,
    }


def test_managed_mode_blocks_user_provider_changes(monkeypatch):
    _enable(monkeypatch)
    from cowork.common.settings.managed_models import check_model_write

    with pytest.raises(ValueError, match="managed by the server administrator"):
        check_model_write("openai_api_key")
    check_model_write("greeting")


def _fake_anton_llm(monkeypatch):
    client_module = ModuleType("anton.core.llm.client")
    anthropic_module = ModuleType("anton.core.llm.anthropic")
    openai_module = ModuleType("anton.core.llm.openai")

    class FakeProvider:
        def __init__(self, api_key=None, base_url=None):
            self._api_key = api_key
            self._base_url = base_url

    class FakeClient:
        def __init__(self, **kwargs):
            self.__dict__.update({f"_{key}": value for key, value in kwargs.items()})

        @property
        def planning_provider(self):
            return self._planning_provider

        @property
        def coding_provider(self):
            return self._coding_provider

    client_module.LLMClient = FakeClient
    anthropic_module.AnthropicProvider = FakeProvider
    openai_module.OpenAIProvider = FakeProvider
    monkeypatch.setitem(sys.modules, "anton.core.llm.client", client_module)
    monkeypatch.setitem(sys.modules, "anton.core.llm.anthropic", anthropic_module)
    monkeypatch.setitem(sys.modules, "anton.core.llm.openai", openai_module)


def test_managed_mode_builds_gateway_client(monkeypatch):
    _enable(monkeypatch)
    _fake_anton_llm(monkeypatch)
    from cowork.services.providers import build_llm_client

    client = build_llm_client()
    assert client._planning_model == "planning"
    assert client._coding_model == "coding"
    assert client.planning_provider._base_url == "http://gateway.internal:4000/v1"
    assert client.coding_provider is client.planning_provider


def test_managed_mode_honours_an_explicit_model_pick(monkeypatch):
    _enable(monkeypatch)
    _fake_anton_llm(monkeypatch)
    import cowork.common.settings.user_settings as user_settings_module
    from cowork.common.settings.user_settings import UserSettings
    from cowork.services.providers import build_llm_client

    picked = UserSettings(planning_model="claude-opus-4-5")
    monkeypatch.setattr(user_settings_module, "get_user_settings", lambda: picked)

    client = build_llm_client()
    assert client._planning_model == "claude-opus-4-5"
    # coding was never picked, so it must still go to the routing alias.
    assert client._coding_model == "coding"


def test_chosen_model_ignores_provider_defaults():
    from cowork.common.settings.user_settings import UserSettings

    defaulted = UserSettings()
    # A default IS filled in for display, but it is not a user choice.
    assert defaulted.planning_model
    assert defaulted.chosen_model("planning_model") is None

    assert UserSettings(coding_model="qwen3-32b").chosen_model("coding_model") == "qwen3-32b"
    assert UserSettings(planning_model="  ").chosen_model("planning_model") is None


def test_enabled_managed_mode_requires_internal_key(monkeypatch):
    monkeypatch.setenv("COWORK_MANAGED_ENABLED", "true")
    monkeypatch.delenv("COWORK_MANAGED_API_KEY", raising=False)
    from cowork.common.settings.managed_models import ManagedModels

    # _env_file=None: otherwise a developer's backend/core_api/.env supplies
    # the key the test just removed from the environment, and nothing raises.
    with pytest.raises(ValueError, match="COWORK_MANAGED_API_KEY"):
        ManagedModels(_env_file=None)
