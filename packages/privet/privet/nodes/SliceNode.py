from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "slice",
    "title": "Slice",
    "displayName": "Slice",
    "data": {"start": 0, "useStartInput": False, "count": None, "useCountInput": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Slices an array from the start index for the count number of elements.",
        "infoBoxTitle": "Slice Node",
        "contextMenuTitle": "Slice",
        "group": ["Lists"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "any[]"},
        {"id": "start", "title": "Start", "dataType": "number", "showIf": {"dataKey": "useStartInput", "equals": True}},
        {"id": "count", "title": "Count", "dataType": "number", "showIf": {"dataKey": "useCountInput", "equals": True}},
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "any[]"},
    ],
    "editors": [
        {"type": "number", "label": "Start", "dataKey": "start", "useInputToggleDataKey": "useStartInput", "allowEmpty": True},
        {"type": "number", "label": "Count", "dataKey": "count", "useInputToggleDataKey": "useCountInput", "allowEmpty": True},
    ],
    "body": (
        "Start: {{#if useStartInput}}(Using Input){{#else}}{{#if start}}{{start}}{{#else}}0{{/if}}{{/if}}\n"
        "Count: {{#if useCountInput}}(Using Input){{#else}}{{#if count}}{{count}}{{#else}}All{{/if}}{{/if}}"
    ),
}
