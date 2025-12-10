from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "chatLoop",
    "title": "Chat Loop",
    "displayName": "Chat Loop",
    "data": {"userPrompt": "Your response:", "renderingFormat": "markdown"},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Creates an interactive chat loop with an AI model. Outputs the conversation and last message.",
        "infoBoxTitle": "Chat Loop Node",
        "contextMenuTitle": "Chat Loop",
        "group": ["Convenience"],
    },
    "inputs": [
        {"id": "systemPrompt", "title": "System Prompt", "dataType": "string", "required": False, "coerced": True},
        {"id": "prompt", "title": "Prompt", "dataType": ["chat-message", "chat-message[]"]},
    ],
    "outputs": [
        {"id": "conversation", "title": "Full Conversation", "dataType": "string[]"},
        {"id": "lastMessage", "title": "Last Message", "dataType": "string"},
    ],
    "editors": [
        {"type": "code", "label": "User Prompt", "dataKey": "userPrompt", "language": "plain-text"},
        {"type": "group", "label": "Rendering", "editors": [ {"type": "dropdown", "dataKey": "renderingFormat", "label": "Format", "options": [ {"label": "Text", "value": "text"}, {"label": "Markdown", "value": "markdown"} ], "defaultValue": "markdown" } ]},
    ],
}
