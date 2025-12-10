from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "toJson",
    "title": "To JSON",
    "displayName": "To JSON",
    "data": {"indented": True},
    "visual": {"width": 175},
    "uiData": {
        "infoBoxBody": "Turns the input value into its JSON equivalent (stringifies the value).",
        "infoBoxTitle": "To JSON Node",
        "contextMenuTitle": "To JSON",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "data", "title": "Data", "dataType": "any", "required": True},
    ],
    "outputs": [
        {"id": "json", "title": "JSON", "dataType": "string"},
    ],
    "editors": [
        {"type": "toggle", "label": "Indented", "dataKey": "indented"},
    ],
    "body": "{{#if indented}}Indented{{#else}}Not indented{{/if}}",
}
