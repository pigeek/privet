from __future__ import annotations

from typing import Any, Dict, Optional

# Minimal DataValue helpers for Python executor parity. These mirror the most
# common behaviors of the TS utils without attempting to cover every Rivet type.


def is_array_data_type(data_type: str | None) -> bool:
    return bool(data_type) and str(data_type).endswith("[]")


def get_scalar_type(data_type: str | None) -> str:
    if not data_type:
        return "any"
    return data_type[:-2] if is_array_data_type(data_type) else data_type


def unwrap_data_value(value: Any) -> Any:
    if isinstance(value, dict) and "type" in value and "value" in value:
        return value.get("value")
    return value


def coerce_type_optional(value: Optional[Dict[str, Any]], data_type: str | None) -> Any:
    """Best-effort coercion that mirrors TS coerceTypeOptional for common cases."""
    if value is None:
        return None

    raw = unwrap_data_value(value)
    scalar_type = get_scalar_type(data_type)

    if is_array_data_type(data_type):
        # If already an array, coerce each element to the scalar type
        if isinstance(raw, list):
            return [coerce_type_optional({"type": scalar_type, "value": v}, scalar_type) for v in raw]
        coerced = coerce_type_optional({"type": scalar_type, "value": raw}, scalar_type)
        return [] if coerced is None else [coerced]

    if scalar_type == "string":
        if raw is None:
            return None
        return str(raw)

    if scalar_type == "number":
        try:
            return float(raw) if raw is not None else None
        except Exception:
            return None

    if scalar_type == "boolean":
        if isinstance(raw, bool):
            return raw
        if isinstance(raw, str):
            return raw.lower() in ("true", "1", "yes", "on")
        if raw is None:
            return None
        return bool(raw)

    if scalar_type == "object":
        # Accept any value; JSONPath can operate on dicts/lists/scalars
        return raw

    # Fallback: return unwrapped value
    return raw


def infer_type(value: Any) -> Dict[str, Any]:
    """Infer a DataValue from a Python value."""
    if value is None:
        return {"type": "any", "value": None}
    if isinstance(value, bool):
        return {"type": "boolean", "value": value}
    if isinstance(value, (int, float)):
        return {"type": "number", "value": value}
    if isinstance(value, str):
        return {"type": "string", "value": value}
    if isinstance(value, list):
        inferred = infer_type(value[0]) if value else {"type": "any", "value": None}
        return {"type": f"{inferred['type']}[]", "value": value}
    if isinstance(value, dict):
        return {"type": "object", "value": value}
    return {"type": "any", "value": value}


def get_default_value(data_type: str | None) -> Any:
    """Return a sensible default for the provided data type."""
    if is_array_data_type(data_type):
        return []
    scalar = get_scalar_type(data_type)
    if scalar == "string":
        return ""
    if scalar == "number":
        return 0
    if scalar == "boolean":
        return False
    if scalar == "object":
        return {}
    return None
