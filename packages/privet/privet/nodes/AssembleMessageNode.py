from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "assembleMessage",
    "title": "Assemble Message",
    "displayName": "Assemble Message",
    "data": {"type": "user", "useTypeInput": False, "toolCallId": "", "useToolCallIdInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Assembles a single chat message from multiple parts (text, images, documents, URLs).",
        "infoBoxTitle": "Assemble Message Node",
        "contextMenuTitle": "Assemble Message",
        "group": "AI",
    },
    "inputs": [
        {"id": "type", "title": "Type", "dataType": "string", "showIf": {"dataKey": "useTypeInput", "equals": True}},
        {"id": "toolCallId", "title": "Tool Call ID", "dataType": "string", "showIf": {"dataKey": "useToolCallIdInput", "equals": True}},
        {"id": "part", "title": "Part {n}", "dataType": ["string", "image", "string[]", "image[]", "object", "object[]", "document", "document[]"], "variadic": {"baseId": "part", "titlePattern": "Part {n}", "startAt": 1, "min": 1}},
    ],
    "outputs": [ {"id": "message", "title": "Message", "dataType": "chat-message"} ],
    "editors": [
        {"type": "dropdown", "label": "Type", "dataKey": "type", "useInputToggleDataKey": "useTypeInput", "options": [
            {"value": "system", "label": "System"},
            {"value": "user", "label": "User"},
            {"value": "assistant", "label": "Assistant"},
            {"value": "function", "label": "Function"}
        ]},
        {"type": "string", "label": "Tool Call ID", "dataKey": "toolCallId", "useInputToggleDataKey": "useToolCallIdInput"},
    ],
    "body": "{{#if useTypeInput}}(Type From Input){{#else}}{{type}}{{/if}}\n{{#if useToolCallIdInput}}Tool Call ID: (From Input){{#else}}{{#if toolCallId}}Tool Call ID: {{toolCallId}}{{/if}}{{/if}}",
}
