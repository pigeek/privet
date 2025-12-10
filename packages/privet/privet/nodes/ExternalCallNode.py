from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "externalCall",
    "title": "External Call",
    "displayName": "External Call",
    "data": {"functionName": "", "useFunctionNameInput": False, "useErrorOutput": False},
    "visual": {"width": 150},
    "uiData": {
        "infoBoxBody": "Calls a host-provided function from the graph.",
        "infoBoxTitle": "External Call Node",
        "contextMenuTitle": "External Call",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "functionName", "title": "Function Name", "dataType": "string", "showIf": {"dataKey": "useFunctionNameInput", "equals": True}},
        {"id": "arguments", "title": "Arguments", "dataType": "any[]"},
    ],
    "outputs": [
        {"id": "result", "title": "Result", "dataType": "any"},
        {"id": "error", "title": "Error", "dataType": "string", "showIf": {"dataKey": "useErrorOutput", "equals": True}},
    ],
    "editors": [
        {"type": "string", "label": "Function Name", "dataKey": "functionName", "useInputToggleDataKey": "useFunctionNameInput"},
        {"type": "toggle", "label": "Use Error Output", "dataKey": "useErrorOutput"},
    ],
    "body": "{{#if useFunctionNameInput}}(Using Input){{#else}}{{functionName}}{{/if}}",
}
