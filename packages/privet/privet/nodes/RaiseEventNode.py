from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "raiseEvent",
    "title": "Raise Event",
    "displayName": "Raise Event",
    "data": {"eventName": "toast", "useEventNameInput": False},
    "visual": {"width": 150},
    "uiData": {
        "infoBoxBody": "Raises an event that the host project or a 'Wait For Event' node can listen for.",
        "infoBoxTitle": "Raise Event Node",
        "contextMenuTitle": "Raise Event",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "eventName", "title": "Event Name", "dataType": "string", "showIf": {"dataKey": "useEventNameInput", "equals": True}},
        {"id": "data", "title": "Data", "dataType": "any"},
    ],
    "outputs": [
        {"id": "result", "title": "Result", "dataType": "any"},
    ],
    "editors": [
        {"type": "string", "label": "Event Name", "dataKey": "eventName", "useInputToggleDataKey": "useEventNameInput"},
    ],
    "body": "{{#if useEventNameInput}}(Using Input){{#else}}{{eventName}}{{/if}}",
}
