from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "callGraph",
    "title": "Call Graph",
    "displayName": "Call Graph",
    "data": {"useErrorOutput": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Calls another graph and passes inputs to it. Use in combination with the Graph Reference node to call dynamic graphs.",
        "infoBoxTitle": "Call Graph Node",
        "contextMenuTitle": "Call Graph",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "graph", "title": "Graph", "dataType": "graph-reference", "required": True},
        {"id": "inputs", "title": "Inputs", "dataType": "object"},
    ],
    "outputs": [
        {"id": "outputs", "title": "Outputs", "dataType": "object"},
        {"id": "error", "title": "Error", "dataType": "string", "showIf": {"dataKey": "useErrorOutput", "equals": True}},
    ],
    "editors": [
        {"type": "toggle", "label": "Use Error Output", "dataKey": "useErrorOutput"},
    ],
}

