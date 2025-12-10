from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "passthrough",
    "title": "Passthrough",
    "displayName": "Passthrough",
    "data": {},
    "visual": {"width": 175},
    "uiData": {
        "infoBoxBody": "Simply passes input values to outputs without modification.",
        "infoBoxTitle": "Passthrough Node",
        "contextMenuTitle": "Passthrough",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "input", "title": "Input {n}", "dataType": "any", "variadic": {"baseId": "input", "titlePattern": "Input {n}", "startAt": 1, "min": 1}},
    ],
    "outputs": [
        {"id": "output", "title": "Output {n}", "dataType": "any", "variadic": {"type": "mirror", "baseId": "output", "inputBaseId": "input", "titlePattern": "Output {n}", "startAt": 1, "excludeLast": True}},
    ],
}

