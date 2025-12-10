from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "destructure",
    "title": "Destructure",
    "displayName": "Destructure",
    "data": {"paths": ["$.value"]},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Destructures the input object by extracting values at configured JSONPath expressions.",
        "infoBoxTitle": "Destructure Node",
        "contextMenuTitle": "Destructure",
        "group": ["Objects"],
    },
    "inputs": [
        {"id": "object", "title": "Object", "dataType": "object", "required": True},
    ],
    "outputs": [
        {"id": "match_", "title": "{{item}}", "dataType": "any", "variadic": {"type": "dataList", "dataKey": "paths", "baseId": "match_", "titleTemplate": "{{item}}"}},
    ],
    "editors": [
        {"type": "stringList", "label": "Paths", "dataKey": "paths", "helperMessage": "JSONPath expressions (one per line)."},
    ],
}

