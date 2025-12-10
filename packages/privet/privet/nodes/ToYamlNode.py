from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "toYaml",
    "title": "To YAML",
    "displayName": "To YAML",
    "data": {},
    "visual": {"width": 175},
    "uiData": {
        "infoBoxBody": "Turns the input object into YAML text.",
        "infoBoxTitle": "To YAML Node",
        "contextMenuTitle": "To YAML",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "object", "title": "Object", "dataType": "object", "required": True},
    ],
    "outputs": [
        {"id": "yaml", "title": "YAML", "dataType": "string"},
    ],
}

