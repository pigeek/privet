from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "delay",
    "title": "Delay",
    "displayName": "Delay",
    "data": {"delay": 0, "useDelayInput": False},
    "visual": {"width": 175},
    "uiData": {
        "infoBoxBody": "Delays execution then passes input values through.",
        "infoBoxTitle": "Delay Node",
        "contextMenuTitle": "Delay",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "delay", "title": "Delay (ms)", "dataType": "number", "showIf": {"dataKey": "useDelayInput", "equals": True}},
        {"id": "input", "title": "Input {n}", "dataType": "any", "variadic": {"baseId": "input", "titlePattern": "Input {n}", "startAt": 1, "min": 1}},
    ],
    "outputs": [
        {"id": "output", "title": "Output {n}", "dataType": "any", "variadic": {"type": "mirror", "baseId": "output", "inputBaseId": "input", "titlePattern": "Output {n}", "startAt": 1, "excludeLast": True}},
    ],
    "editors": [
        {"type": "number", "label": "Delay (ms)", "dataKey": "delay", "useInputToggleDataKey": "useDelayInput", "defaultValue": 0},
    ],
    "body": "Delay {{#if useDelayInput}}(Input ms){{#else}}{{delay}}ms{{/if}}",
}
