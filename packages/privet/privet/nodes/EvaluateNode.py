from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "evaluate",
    "title": "Evaluate",
    "displayName": "Evaluate",
    "data": {"operation": "+", "useOperationInput": False},
    "visual": {"width": 175},
    "uiData": {
        "infoBoxBody": "Evaluates a mathematical operation on inputs.",
        "infoBoxTitle": "Evaluate Node",
        "contextMenuTitle": "Evaluate",
        "group": ["Numbers"],
    },
    "inputs": [
        {"id": "a", "title": "A", "dataType": "number"},
        {"id": "b", "title": "B", "dataType": "number", "showIf": {"dataKey": "operation", "notIn": ["abs", "negate"]}},
        {"id": "operation", "title": "Operation", "dataType": "string", "showIf": {"dataKey": "useOperationInput", "equals": True}},
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "number"},
    ],
    "editors": [
        {"type": "dropdown", "label": "Operation", "dataKey": "operation", "options": [
            {"label": "+", "value": "+"},
            {"label": "-", "value": "-"},
            {"label": "*", "value": "*"},
            {"label": "/", "value": "/"},
            {"label": "^", "value": "^"},
            {"label": "%", "value": "%"},
            {"label": "abs", "value": "abs"},
            {"label": "negate", "value": "negate"}
        ], "useInputToggleDataKey": "useOperationInput"},
    ],
    "body": "{{#if useOperationInput}}A (Operation) B{{#else}}A {{operation}} B{{/if}}",
}
