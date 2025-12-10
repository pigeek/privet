from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "randomNumber",
    "title": "RNG",
    "displayName": "Random Number",
    "data": {"min": 0, "max": 1, "integers": False, "maxInclusive": False, "useMinInput": False, "useMaxInput": False},
    "visual": {"width": 150},
    "uiData": {
        "infoBoxBody": "Outputs a random number between configured min and max values.",
        "infoBoxTitle": "RNG Node",
        "contextMenuTitle": "RNG",
        "group": ["Numbers"],
    },
    "inputs": [
        {"id": "min", "title": "Min", "dataType": "number", "showIf": {"dataKey": "useMinInput", "equals": True}},
        {"id": "max", "title": "Max", "dataType": "number", "showIf": {"dataKey": "useMaxInput", "equals": True}},
    ],
    "outputs": [
        {"id": "value", "title": "Value", "dataType": "number"},
    ],
    "editors": [
        {"type": "number", "label": "Min", "dataKey": "min", "useInputToggleDataKey": "useMinInput"},
        {"type": "number", "label": "Max", "dataKey": "max", "useInputToggleDataKey": "useMaxInput"},
        {"type": "toggle", "label": "Integers", "dataKey": "integers"},
        {"type": "toggle", "label": "Max Inclusive", "dataKey": "maxInclusive"},
    ],
    "body": (
        "Min: {{#if useMinInput}}(Input){{#else}}{{min}}{{/if}}\n"
        "Max: {{#if useMaxInput}}(Input){{#else}}{{max}}{{/if}}\n"
        "{{#if integers}}Integers{{#else}}Floats{{/if}}\n"
        "{{#if maxInclusive}}Max Inclusive{{#else}}Max Exclusive{{/if}}"
    ),
}
