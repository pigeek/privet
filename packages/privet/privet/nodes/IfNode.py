from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "if",
    "title": "If",
    "displayName": "If",
    "data": {"unconnectedControlFlowExcluded": True},
    "visual": {"width": 125},
    "uiData": {
        "infoBoxBody": "Routes a value to True or False outputs based on a condition.",
        "infoBoxTitle": "If Node",
        "contextMenuTitle": "If",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "if", "title": "If", "dataType": "any", "description": "Condition to test"},
        {"id": "value", "title": "Value", "dataType": "any", "description": "Value to pass through"},
    ],
    "outputs": [
        {"id": "output", "title": "True", "dataType": "any"},
        {"id": "falseOutput", "title": "False", "dataType": "any"},
    ],
    "editors": [
        {"type": "toggle", "label": "Don't run unconnected value", "dataKey": "unconnectedControlFlowExcluded"},
    ],
}

