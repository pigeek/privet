from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "split",
    "title": "Split Text",
    "displayName": "Split String",
    "data": {"delimiter": ",", "useDelimiterInput": False, "regex": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Splits a string by the provided delimiter.",
        "infoBoxTitle": "Split Text Node",
        "contextMenuTitle": "Split Text",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "string", "title": "String", "dataType": "string"},
        {"id": "delimiter", "title": "Delimiter", "dataType": "string", "showIf": {"dataKey": "useDelimiterInput", "equals": True}},
    ],
    "outputs": [
        {"id": "splitString", "title": "Split", "dataType": "string[]"},
    ],
    "editors": [
        {"type": "toggle", "label": "Regex", "dataKey": "regex"},
        {"type": "code", "label": "Delimiter", "language": "plaintext", "dataKey": "delimiter", "useInputToggleDataKey": "useDelimiterInput"},
    ],
    "body": "{{#if useDelimiterInput}}(Delimiter from input){{#else}}{{delimiter}}{{/if}}",
}
