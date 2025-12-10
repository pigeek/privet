from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "listGraphs",
    "title": "List Graphs",
    "displayName": "List Graphs",
    "data": {},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Lists all graphs in the project.",
        "infoBoxTitle": "List Graphs Node",
        "contextMenuTitle": "List Graphs",
        "group": ["Input/Output"],
    },
    "inputs": [],
    "outputs": [
        {"id": "graphs", "title": "Graphs", "dataType": "graph-reference[]"},
        {"id": "graph-names", "title": "Graph Names", "dataType": "string[]"},
    ],
}

