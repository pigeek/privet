from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "trimChatMessages",
    "title": "Trim Chat Messages",
    "displayName": "Trim Chat Messages",
    "data": {"maxTokenCount": 4096, "removeFromBeginning": True, "useMaxTokenCountInput": False, "useRemoveFromBeginningInput": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Slices messages from start or end until under token limit.",
        "infoBoxTitle": "Trim Chat Messages Node",
        "contextMenuTitle": "Trim Chat Messages",
        "group": ["AI"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "chat-message[]"},
        {"id": "maxTokenCount", "title": "Max Token Count", "dataType": "number", "showIf": {"dataKey": "useMaxTokenCountInput", "equals": True}},
        {"id": "removeFromBeginning", "title": "Remove From Beginning", "dataType": "boolean", "showIf": {"dataKey": "useRemoveFromBeginningInput", "equals": True}},
    ],
    "outputs": [ {"id": "trimmed", "title": "Trimmed", "dataType": "chat-message[]"} ],
    "editors": [
        {"type": "number", "label": "Max Token Count", "dataKey": "maxTokenCount", "useInputToggleDataKey": "useMaxTokenCountInput"},
        {"type": "toggle", "label": "Remove From Beginning", "dataKey": "removeFromBeginning", "useInputToggleDataKey": "useRemoveFromBeginningInput"},
    ],
    "body": "Max Token Count: {{#if useMaxTokenCountInput}}(From Input){{#else}}{{maxTokenCount}}{{/if}}\nRemove From Beginning: {{#if useRemoveFromBeginningInput}}(From Input){{#else}}{{#if removeFromBeginning}}Yes{{#else}}No{{/if}}{{/if}}",
}
