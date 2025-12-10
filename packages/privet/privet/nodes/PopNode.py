from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "pop",
    "title": "Pop",
    "displayName": "Pop",
    "data": {"fromFront": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Pops a value off the input array and outputs the remaining array and the popped value.",
        "infoBoxTitle": "Pop Node",
        "contextMenuTitle": "Pop",
        "group": ["Lists"],
    },
    "inputs": [
        {"id": "array", "title": "Array", "dataType": "any[]"},
    ],
    "outputs": [
        {"id": "lastItem", "title": "Item", "dataType": "any"},
        {"id": "restOfArray", "title": "Rest", "dataType": "any"},
    ],
    "editors": [
        {"type": "toggle", "label": "Pop from front", "dataKey": "fromFront"},
    ],
    "body": "{{#if fromFront}}From front{{#else}}From back{{/if}}",
}
