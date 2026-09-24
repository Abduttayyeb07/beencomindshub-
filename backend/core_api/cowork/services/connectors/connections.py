from __future__ import annotations

from anton.core.datasources.data_vault import ANTON_VAULT_KEEP, is_secret_key
from cowork.common.settings.app_settings import ConnectorSettings
from cowork.schemas.connectors import ConnectionDetailResponse, ConnectionSummaryResponse
from cowork.services.connectors.specs._registry import registry

# The value the save path recognises as "keep the stored value". This used to be
# the literal string "ANTON_VAULT_KEEP" — the constant's NAME rather than its
# value — so a masked field submitted unchanged was written to the vault as that
# placeholder, overwriting the real credential.
_SENTINEL = ANTON_VAULT_KEEP


def spec_secret_fields(connector_id: str | None, method: str | None) -> set[str]:
    """Field names a connector's spec marks `secret: true`.

    The single source of truth for which fields are credentials: the read path
    masks them and the save path records them as the record's `secure_keys`.
    """
    if not connector_id:
        return set()
    spec = registry.get_connector(connector_id)
    if spec is None:
        return set()
    form = spec.form
    methods = form.methods or []
    if methods:
        chosen = next((m for m in methods if m.id == method), None)
        # No method given: be conservative and treat a field marked secret in
        # ANY method as secret, rather than masking nothing.
        fields = list(chosen.fields or []) if chosen else [
            f for m in methods for f in (m.fields or [])
        ]
    else:
        fields = list(form.fields or [])
    return {f.name for f in fields if f.secret}


class ConnectionsService:
    def _vault(self):
        from pathlib import Path
        from anton.core.datasources.data_vault import LocalDataVault
        return LocalDataVault(Path(ConnectorSettings().vault_dir))

    def list(self) -> list[ConnectionSummaryResponse]:
        items = self._vault().list_connections()
        result = []
        for item in items:
            spec = registry.get_connector(item.get("engine", ""))
            result.append(ConnectionSummaryResponse(
                engine=item.get("engine", ""),
                name=item.get("name", ""),
                created_at=item.get("created_at"),
                label=spec.label if spec else None,
                logo=spec.logo if spec else None,
                logo_color=spec.logo_color if spec else None,
            ))
        return result

    def get(self, engine: str, name: str) -> ConnectionDetailResponse | None:
        vault = self._vault()
        if hasattr(vault, "read_record"):
            record = vault.read_record(engine, name)
        else:
            raw = vault.load(engine, name)
            record = {"engine": engine, "name": name, "fields": raw} if raw is not None else None

        if record is None:
            return None

        fields: dict = dict(record.get("fields") or {})

        # Masking cannot rely on `secure_keys` alone: records written before the
        # save path recorded it have none, and returned raw credentials over the
        # API. Fall back to the connector's spec, then to the name heuristic, so
        # a missing list can never mean "nothing is secret".
        secure_keys = record.get("secure_keys")
        if secure_keys:
            secret = set(secure_keys)
        else:
            secret = spec_secret_fields(
                fields.get("_connector_id") or record.get("engine", engine),
                fields.get("_method"),
            )
            secret |= {k for k in fields if is_secret_key(k, secure_keys=None)}
        for key in secret:
            if key in fields:
                fields[key] = _SENTINEL

        return ConnectionDetailResponse(
            engine=record.get("engine", engine),
            name=record.get("name", name),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            connector_id=fields.pop("_connector_id", None),
            method=fields.pop("_method", None),
            fields=fields,
        )

    def delete(self, engine: str, name: str) -> bool:
        return self._vault().delete(engine, name)


service = ConnectionsService()
