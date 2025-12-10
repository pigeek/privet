from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "filter",
    "title": "Filter",
    "displayName": "Filter",
    "data": {},
    "visual": {"width": 175},
    "uiData": {
        "infoBoxBody": "Takes in both an array of values and an array of booleans of the same length, and filters where the boolean is true.",
        "infoBoxTitle": "Filter Node",
        "contextMenuTitle": "Filter",
        "group": ["Lists"],
    },
    "inputs": [
        {"id": "array", "title": "Array", "dataType": "any[]", "required": True},
        {"id": "include", "title": "Include", "dataType": "boolean[]", "required": True},
    ],
    "outputs": [
        {"id": "filtered", "title": "Filtered", "dataType": "any[]"},
    ],
}

