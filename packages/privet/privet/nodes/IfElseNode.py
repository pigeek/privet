from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "ifElse",
    "title": "If/Else",
    "displayName": "If/Else",
    "data": {"unconnectedControlFlowExcluded": True},
    "visual": {"width": 175},
    "uiData": {
        "infoBoxBody": "Routes either the True or False input based on the If condition.",
        "infoBoxTitle": "If/Else Node",
        "contextMenuTitle": "If/Else",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "if", "title": "If", "dataType": "any"},
        {"id": "true", "title": "True", "dataType": "any"},
        {"id": "false", "title": "False", "dataType": "any"},
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "any"},
    ],
    "editors": [
        {"type": "toggle", "label": "Don't run unconnected ports", "dataKey": "unconnectedControlFlowExcluded"},
    ],
}

