from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "context",
    "title": "Context",
    "displayName": "Context",
    "data": {"id": "input", "dataType": "string", "defaultValue": None, "useDefaultValueInput": False},
    "visual": {"width": 300},
    "uiData": {
        "infoBoxBody": "Retrieves a value from the graph context using an id.",
        "infoBoxTitle": "Context Node",
        "contextMenuTitle": "Context",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "default", "title": "Default Value", "dataType": "any", "showIf": {"dataKey": "useDefaultValueInput", "equals": True}},
    ],
    "outputs": [
        {"id": "data", "title": "{{id}}", "titleTemplate": "{{id}}", "dataTypeFrom": {"dataKey": "dataType"}, "dataType": ["any","string","number","boolean","object","chat-message","vector","image","binary","audio","document"]},
    ],
    "editors": [
        {"type": "string", "label": "ID", "dataKey": "id"},
        {"type": "dataTypeSelector", "label": "Data Type", "dataKey": "dataType"},
        {"type": "anyData", "label": "Default Value", "dataKey": "defaultValue", "useInputToggleDataKey": "useDefaultValueInput"},
    ],
    "body": "{{id}}\nType: {{dataType}}",
}
