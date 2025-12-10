from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "getGlobal",
    "title": "Get Global",
    "displayName": "Get Global",
    "data": {"id": "variable-name", "dataType": "string", "onDemand": True, "useIdInput": False, "wait": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Retrieves a global value; can be on-demand or wait for availability.",
        "infoBoxTitle": "Get Global Node",
        "contextMenuTitle": "Get Global",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "id", "title": "Variable ID", "dataType": "string", "showIf": {"dataKey": "useIdInput", "equals": True}},
    ],
    "outputs": [
        {"id": "value", "title": "Value", "dataTypeFrom": {"dataKey": "onDemand", "map": {"true": "fn<string>", "false": "string"}}, "dataType": ["fn<string>", "string"]},
        {"id": "variable_id_out", "title": "Variable ID", "dataType": "string"},
    ],
    "editors": [
        {"type": "string", "label": "Variable ID", "dataKey": "id", "useInputToggleDataKey": "useIdInput"},
        {"type": "dataTypeSelector", "label": "Data Type", "dataKey": "dataType"},
        {"type": "toggle", "label": "On Demand", "dataKey": "onDemand"},
        {"type": "toggle", "label": "Wait", "dataKey": "wait"},
    ],
    "body": "{{#if useIdInput}}(ID from input){{#else}}{{id}}{{/if}}\nType: {{dataType}}\n{{#if wait}}Waits for available data{{/if}}",
}
