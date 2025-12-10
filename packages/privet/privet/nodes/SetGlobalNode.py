from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "setGlobal",
    "title": "Set Global",
    "displayName": "Set Global",
    "data": {"id": "variable-name", "dataType": "string", "useIdInput": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Sets a global value shared across graphs and subgraphs.",
        "infoBoxTitle": "Set Global Node",
        "contextMenuTitle": "Set Global",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "value", "title": "Value", "dataType": "any", "dataTypeFrom": {"dataKey": "dataType"}},
        {"id": "id", "title": "Variable ID", "dataType": "string", "showIf": {"dataKey": "useIdInput", "equals": True}},
    ],
    "outputs": [
        {"id": "saved-value", "title": "Value", "dataType": "any", "dataTypeFrom": {"dataKey": "dataType"}},
        {"id": "previous-value", "title": "Previous Value", "dataType": "any", "dataTypeFrom": {"dataKey": "dataType"}},
        {"id": "variable_id_out", "title": "Variable ID", "dataType": "string"},
    ],
    "editors": [
        {"type": "string", "label": "ID", "dataKey": "id", "useInputToggleDataKey": "useIdInput"},
        {"type": "dataTypeSelector", "label": "Data Type", "dataKey": "dataType"},
    ],
    "body": "{{id}}\nType: {{dataType}}",
}

