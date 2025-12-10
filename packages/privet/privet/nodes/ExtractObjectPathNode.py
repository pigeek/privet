from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "extractObjectPath",
    "title": "Extract Object Path",
    "displayName": "Extract Object Path",
    "data": {"path": "$", "usePathInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Extracts the value at the specified JSONPath from the input object.",
        "infoBoxTitle": "Extract Object Path Node",
        "contextMenuTitle": "Extract Object Path",
        "group": ["Objects"],
    },
    "inputs": [
        {"id": "object", "title": "Object", "dataType": "object", "required": True},
        {"id": "path", "title": "Path", "dataType": "string", "showIf": {"dataKey": "usePathInput", "equals": True}},
    ],
    "outputs": [
        {"id": "match", "title": "Match", "dataType": "any"},
        {"id": "all_matches", "title": "All Matches", "dataType": "any[]"},
    ],
    "editors": [
        {"type": "code", "label": "Path", "dataKey": "path", "language": "jsonpath", "useInputToggleDataKey": "usePathInput"},
    ],
    "body": "{{#if usePathInput}}(Using Input){{#else}}{{path}}{{/if}}",
}
