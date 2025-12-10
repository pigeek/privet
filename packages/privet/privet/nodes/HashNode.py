from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "hash",
    "title": "Hash",
    "displayName": "Hash",
    "data": {"algorithm": "sha256"},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Computes a hash of the input using the selected algorithm.",
        "infoBoxTitle": "Hash Node",
        "contextMenuTitle": "Hash",
        "group": ["Data"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "string", "required": True},
    ],
    "outputs": [
        {"id": "hash", "title": "Hash", "dataType": "string"},
    ],
    "editors": [
        {"type": "dropdown", "label": "Algorithm", "dataKey": "algorithm", "options": [
            {"value": "md5", "label": "MD5"},
            {"value": "sha1", "label": "SHA1"},
            {"value": "sha256", "label": "SHA256"},
            {"value": "sha512", "label": "SHA512"}
        ]},
    ],
    "body": "{{algorithm}}",
}

