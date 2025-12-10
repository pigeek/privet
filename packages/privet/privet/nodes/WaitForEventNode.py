from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "waitForEvent",
    "title": "Wait For Event",
    "displayName": "Wait For Event",
    "data": {"eventName": "continue", "useEventNameInput": False},
    "visual": {"width": 150},
    "uiData": {
        "infoBoxBody": "Waits for a specific event raised by 'Raise Event' or the host.",
        "infoBoxTitle": "Wait For Event Node",
        "contextMenuTitle": "Wait For Event",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "eventName", "title": "Event Name", "dataType": "string", "showIf": {"dataKey": "useEventNameInput", "equals": True}},
        {"id": "inputData", "title": "Data", "dataType": "any"},
    ],
    "outputs": [
        {"id": "outputData", "title": "Data", "dataType": "any"},
        {"id": "eventData", "title": "Event Data", "dataType": "any"},
    ],
    "editors": [
        {"type": "string", "label": "Event Name", "dataKey": "eventName", "useInputToggleDataKey": "useEventNameInput"},
    ],
    "body": "{{#if useEventNameInput}}(Using Input){{#else}}{{eventName}}{{/if}}",
}
