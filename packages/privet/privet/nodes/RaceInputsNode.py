from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "raceInputs",
    "title": "Race Inputs",
    "displayName": "Race Inputs",
    "data": {},
    "visual": {"width": 300},
    "uiData": {
        "infoBoxBody": "Takes multiple inputs and outputs the first that finishes; others are cancelled.",
        "infoBoxTitle": "Race Inputs Node",
        "contextMenuTitle": "Race Inputs",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "input", "title": "Input {n}", "dataType": "any", "variadic": {"baseId": "input", "titlePattern": "Input {n}", "startAt": 1, "min": 1}},
    ],
    "outputs": [
        {"id": "result", "title": "Result", "dataType": "any"},
    ],
}

