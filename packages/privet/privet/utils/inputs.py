from __future__ import annotations

from typing import Any, Dict

from .data_values import coerce_type_optional


def get_input_or_data(
    data: Dict[str, Any],
    inputs: Dict[str, Any],
    input_and_data_key: str,
    data_type: str | None = "string",
    use_input_toggle_data_key: str | None = None,
) -> Any:
    """Replicates the TS getInputOrData helper."""
    if not use_input_toggle_data_key:
        capitalized = input_and_data_key[0].upper() + input_and_data_key[1:]
        use_input_toggle_data_key = f"use{capitalized}Input"

    use_input = bool(data.get(use_input_toggle_data_key)) and inputs.get(input_and_data_key) is not None
    if use_input:
        coerced = coerce_type_optional(inputs.get(input_and_data_key), data_type)
        if coerced is not None:
            return coerced

    return data.get(input_and_data_key)
