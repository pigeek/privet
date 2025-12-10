from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "number",
    "title": "Number",
    "displayName": "Number",
    "data": {"value": 0, "useValueInput": False, "round": False, "roundTo": 0},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": (
            "Outputs a number constant, or converts an input value into a number.\n"
            "Can round to a certain number of decimals."
        ),
        "infoBoxTitle": "Number Node",
        "contextMenuTitle": "Number",
        "group": ["Numbers"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "any", "showIf": {"dataKey": "useValueInput", "equals": True}},
    ],
    "outputs": [
        {"id": "value", "title": "Value", "dataType": "number"},
    ],
    "editors": [
        {"type": "number", "label": "Value", "dataKey": "value", "useInputToggleDataKey": "useValueInput"},
        {"type": "toggle", "label": "Round", "dataKey": "round"},
        {"type": "number", "label": "Round To", "dataKey": "roundTo"},
    ],
    "body": "{{#if useValueInput}}(Input to number){{#else}}{{value}}{{/if}}",
}
