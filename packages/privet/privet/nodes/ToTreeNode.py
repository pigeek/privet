from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "toTree",
    "title": "To Tree",
    "displayName": "To Tree",
    "data": {"format": "{{path}}", "childrenProperty": "children", "useSortAlphabetically": True},
    "visual": {"width": 300},
    "uiData": {
        "infoBoxBody": "Converts an array of objects into a tree and renders it as text.",
        "infoBoxTitle": "To Tree Node",
        "contextMenuTitle": "To Tree",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "objects", "title": "Objects", "dataType": ["object[]", "object"], "required": True},
    ],
    "outputs": [
        {"id": "tree", "title": "Tree", "dataType": "string"},
    ],
    "editors": [
        {"type": "string", "label": "Children Property", "dataKey": "childrenProperty"},
        {"type": "code", "label": "Format", "dataKey": "format", "language": "prompt-interpolation-markdown", "theme": "prompt-interpolation"},
        {"type": "toggle", "label": "Sort Alphabetically", "dataKey": "useSortAlphabetically"},
    ],
    "body": "Format: {{format}}\nChildren: {{childrenProperty}}\nSort: {{#if useSortAlphabetically}}Yes{{#else}}No{{/if}}",
}
