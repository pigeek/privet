from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "shuffle",
    "title": "Shuffle",
    "displayName": "Shuffle",
    "data": {},
    "visual": {"width": 175},
    "uiData": {
        "infoBoxBody": "Shuffles the input array. Outputs the shuffled array.",
        "infoBoxTitle": "Shuffle Node",
        "contextMenuTitle": "Shuffle",
        "group": ["Lists"],
    },
    "inputs": [
        {"id": "array", "title": "Array", "dataType": "any[]"},
    ],
    "outputs": [
        {"id": "shuffled", "title": "Shuffled", "dataType": "any[]"},
    ],
}

