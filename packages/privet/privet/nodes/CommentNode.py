from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "comment",
    "title": "Comment",
    "displayName": "Comment",
    "data": {"text": "", "height": 600, "color": "rgba(255,255,255,1)", "backgroundColor": "rgba(0,0,0,0.05)"},
    "visual": {"width": 600},
    "uiData": {
        "infoBoxBody": "A comment node for adding notes to a graph.",
        "infoBoxTitle": "Comment Node",
        "contextMenuTitle": "Comment",
        "group": ["Advanced"],
    },
    "inputs": [],
    "outputs": [],
    "editors": [
        {"type": "color", "label": "Color", "dataKey": "color"},
        {"type": "color", "label": "Background Color", "dataKey": "backgroundColor"},
        {"type": "code", "label": "Text", "dataKey": "text", "language": "markdown", "theme": "vs-dark"},
    ],
}

