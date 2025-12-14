from __future__ import annotations


def handle_escape_characters(value: str) -> str:
    """Translate escaped sequences like \\n and \\t into real characters."""
    if value is None:
        return ""
    # Process Windows newline first
    value = value.replace("\\r\\n", "\r\n")
    value = value.replace("\\n", "\n")
    value = value.replace("\\t", "\t")
    value = value.replace("\\r", "\r")
    return value
