"""Credentials must never leave the vault in the clear through the API."""
from __future__ import annotations

import pytest

from anton.core.datasources.data_vault import ANTON_VAULT_KEEP, LocalDataVault
from cowork.handlers.probe import _prepare_vault_payload
from cowork.services.connectors.connections import ConnectionsService, spec_secret_fields


@pytest.fixture()
def vault(tmp_path, monkeypatch):
    """A ConnectionsService and probe save path backed by a throwaway vault."""
    monkeypatch.delenv("ANTON_VAULT_KEY", raising=False)
    v = LocalDataVault(vault_dir=tmp_path / "data-vault")
    monkeypatch.setattr(ConnectionsService, "_vault", lambda self: v)
    monkeypatch.setattr("cowork.handlers.probe._vault", lambda: v)
    return v


def test_spec_marks_the_postgres_uri_secret():
    assert "connection_uri" in spec_secret_fields("postgres", "connection-string")


def test_record_without_secure_keys_is_still_masked(vault):
    # Exactly what the old save path wrote: no secure_keys at all. This is the
    # bug — GET returned the password in plaintext.
    vault.save("postgres", "prod", {
        "connection_uri": "postgresql://user:hunter2@db.internal:5432/app",
        "_connector_id": "postgres",
        "_method": "connection-string",
    })

    detail = ConnectionsService().get("postgres", "prod")

    assert detail.fields["connection_uri"] == ANTON_VAULT_KEEP
    assert "hunter2" not in str(detail.model_dump())


def test_unknown_connector_falls_back_to_the_name_heuristic(vault):
    # A handcrafted connector has no spec, so masking leans on field names.
    vault.save("bespoke", "thing", {"password": "hunter2", "host": "db.internal"})

    detail = ConnectionsService().get("bespoke", "thing")

    assert detail.fields["password"] == ANTON_VAULT_KEEP
    assert detail.fields["host"] == "db.internal"  # not a secret, stays visible


def test_save_records_secure_keys(vault):
    payload, secure_keys = _prepare_vault_payload(
        "postgres", "prod", "connection-string",
        {"connection_uri": "postgresql://user:hunter2@db.internal:5432/app"},
    )
    assert "connection_uri" in secure_keys
    assert payload["_connector_id"] == "postgres"


def test_editing_without_retyping_the_secret_keeps_it(vault):
    """The sentinel must resolve to the stored value, not overwrite it."""
    real = "postgresql://user:hunter2@db.internal:5432/app"
    payload, secure_keys = _prepare_vault_payload(
        "postgres", "prod", "connection-string", {"connection_uri": real})
    vault.save("postgres", "prod", payload, secure_keys=secure_keys)

    # Re-submitting the form with the masked field untouched.
    payload2, secure_keys2 = _prepare_vault_payload(
        "postgres", "prod", "connection-string", {"connection_uri": ANTON_VAULT_KEEP})
    vault.save("postgres", "prod", payload2, secure_keys=secure_keys2)

    assert vault.load("postgres", "prod")["connection_uri"] == real


def test_sentinel_is_the_real_constant_not_its_name():
    # The mask used to be the string "ANTON_VAULT_KEEP" (the constant's NAME),
    # which the save path did not recognise as "keep the stored value".
    assert ANTON_VAULT_KEEP == "__anton_vault_keep__"
