from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "boolean",
    "title": "Bool",
    "displayName": "Boolean",
    "data": {"value": False, "useValueInput": False},
    "visual": {"width": 130},
    "uiData": {
        "infoBoxBody": "Outputs a boolean constant, or converts an input value into a boolean.",
        "infoBoxTitle": "Bool Node",
        "contextMenuTitle": "Bool",
        "group": ["Data"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "any", "showIf": {"dataKey": "useValueInput", "equals": True}},
    ],
    "outputs": [
        {"id": "value", "title": "Value", "dataType": "boolean"},
    ],
    "editors": [
        {"type": "toggle", "label": "Value", "dataKey": "value", "useInputToggleDataKey": "useValueInput"},
    ],
    "body": "{{#if useValueInput}}(Input to bool){{#else}}{{value}}{{/if}}",
}
