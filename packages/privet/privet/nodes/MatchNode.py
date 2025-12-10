from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "match",
    "title": "Match",
    "displayName": "Match",
    "data": {"cases": ["YES", "NO"], "exclusive": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Routes the value through the first matching regex case; can be exclusive.",
        "infoBoxTitle": "Match Node",
        "contextMenuTitle": "Match",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "input", "title": "Test", "dataType": "string", "required": True, "description": "Value tested against each regex."},
        {"id": "value", "title": "Value", "dataType": "any", "description": "Passed through when a case matches."},
    ],
    "outputs": [
        {"id": "case", "title": "{{item}}", "dataType": "string", "variadic": {"type": "dataList", "dataKey": "cases", "baseId": "case", "titleTemplate": "{{item}}", "startAt": 1}},
        {"id": "unmatched", "title": "Unmatched", "dataType": "string", "description": "Value when no regex matches."},
    ],
    "editors": [
        {"type": "toggle", "dataKey": "exclusive", "label": "Exclusive", "helperMessage": "Only the first matching branch runs."},
        {"type": "stringList", "dataKey": "cases", "label": "Cases", "placeholder": "Case (regular expression)", "helperMessage": "(Regular expressions)"},
    ],
    "body": "{{#if exclusive}}First Matching Case{{#else}}All Matching Cases{{/if}}\n{{cases.length}} Cases",
}
