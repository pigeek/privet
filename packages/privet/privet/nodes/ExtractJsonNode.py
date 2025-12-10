from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "extractJson",
    "title": "Extract JSON",
    "displayName": "Extract JSON",
    "data": {},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Finds and parses the first JSON object in the input text.",
        "infoBoxTitle": "Extract JSON Node",
        "contextMenuTitle": "Extract JSON",
        "group": ["Objects"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "string", "required": True},
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "object"},
        {"id": "noMatch", "title": "No Match", "dataType": "string"},
    ],
}

