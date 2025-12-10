from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "coalesce",
    "title": "Coalesce",
    "displayName": "Coalesce",
    "data": {},
    "visual": {"width": 150},
    "uiData": {
        "infoBoxBody": "Takes in any number of inputs and outputs the first value that exists. Useful for consolidating branches after a Match node.",
        "infoBoxTitle": "Coalesce Node",
        "contextMenuTitle": "Coalesce",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "conditional", "title": "Conditional", "dataType": "boolean"},
        {"id": "input", "title": "Input {n}", "dataType": "any", "variadic": {"baseId": "input", "titlePattern": "Input {n}", "startAt": 1, "min": 1}},
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "any"},
    ],
}

