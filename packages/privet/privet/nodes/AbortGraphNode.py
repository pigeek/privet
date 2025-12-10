from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "abortGraph",
    "title": "Abort Graph",
    "displayName": "Abort Graph",
    "data": {"successfully": True, "errorMessage": "", "useSuccessfullyInput": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Aborts graph execution (success or error).",
        "infoBoxTitle": "Abort Graph Node",
        "contextMenuTitle": "Abort Graph",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "data", "title": "Data or Error", "dataType": "any", "description": "Message to abort with."},
        {"id": "successfully", "title": "Successfully", "dataType": "boolean", "showIf": {"dataKey": "useSuccessfullyInput", "equals": True}},
    ],
    "outputs": [],
    "editors": [
        {"type": "toggle", "label": "Successfully Abort", "dataKey": "successfully", "useInputToggleDataKey": "useSuccessfullyInput"},
        {"type": "string", "label": "Error Message (if not successfully aborting)", "dataKey": "errorMessage"},
    ],
    "body": "{{#if useSuccessfullyInput}}Success depends on input{{#else}}{{#if successfully}}Successfully Abort{{#else}}{{#if errorMessage}}Error Abort: {{errorMessage}}{{#else}}Error Abort{{/if}}{{/if}}{{/if}}",
}
