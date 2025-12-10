from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "assemblePrompt",
    "title": "Assemble Prompt",
    "displayName": "Assemble Prompt",
    "data": {"computeTokenCount": False, "isLastMessageCacheBreakpoint": False, "useIsLastMessageCacheBreakpointInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Assembles an array of chat messages for use with a Chat node.",
        "infoBoxTitle": "Assemble Prompt Node",
        "contextMenuTitle": "Assemble Prompt",
        "group": ["AI"],
    },
    "inputs": [
        {"id": "isLastMessageCacheBreakpoint", "title": "Is Last Message Cache Breakpoint", "dataType": "boolean", "showIf": {"dataKey": "useIsLastMessageCacheBreakpointInput", "equals": True}},
        {"id": "message", "title": "Message {n}", "dataType": ["chat-message", "chat-message[]"], "variadic": {"baseId": "message", "titlePattern": "Message {n}", "startAt": 1, "min": 1}},
    ],
    "outputs": [
        {"id": "prompt", "title": "Prompt", "dataType": "chat-message[]"},
        {"id": "tokenCount", "title": "Token Count", "dataType": "number", "showIf": {"dataKey": "computeTokenCount", "equals": True}},
    ],
    "editors": [
        {"type": "toggle", "label": "Compute Token Count", "dataKey": "computeTokenCount"},
        {"type": "toggle", "label": "Is Last Message Cache Breakpoint", "dataKey": "isLastMessageCacheBreakpoint"},
    ],
    "body": "{{#if isLastMessageCacheBreakpoint}}Last message is cache breakpoint{{/if}}",
}

