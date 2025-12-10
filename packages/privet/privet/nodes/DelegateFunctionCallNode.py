from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "delegateFunctionCall",
    "title": "Delegate Tool Call",
    "displayName": "Delegate Tool Call",
    "data": {
        "handlers": [],
        "unknownHandler": None,
        "autoDelegate": True,
        "fallBackToExternalCall": True,
        "passthroughErrors": True,
    },
    "visual": {"width": 325},
    "uiData": {
        "infoBoxBody": "Handles a tool call by delegating it to a different subgraph depending on the tool call.",
        "infoBoxTitle": "Delegate Tool Call Node",
        "contextMenuTitle": "Delegate Tool Call",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "function-call", "title": "Tool Call", "dataType": "object", "required": True, "coerced": True},
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "string"},
        {"id": "message", "title": "Message Output", "dataType": "object"},
    ],
    "editors": [
        {"type": "toggle", "label": "Auto Delegate", "dataKey": "autoDelegate"},
        {"type": "toggle", "label": "Fall Back To External Call", "dataKey": "fallBackToExternalCall", "showIf": {"dataKey": "autoDelegate", "equals": True}},
        {"type": "toggle", "label": "Passthrough Errors", "dataKey": "passthroughErrors", "showIf": {"all": [ {"dataKey": "autoDelegate", "equals": True}, {"dataKey": "fallBackToExternalCall", "equals": True} ]}},
        {"type": "custom", "customEditorId": "ToolCallHandlers", "label": "Handlers", "dataKey": "handlers", "showIf": {"dataKey": "autoDelegate", "equals": False}},
        {"type": "graphSelector", "dataKey": "unknownHandler", "label": "Unknown Handler"},
    ],
    "body": (
        "{{#if autoDelegate}}\n"
        "  Auto Delegate To Subgraphs{{#if fallBackToExternalCall}} (+ External Call Fallback{{#if passthroughErrors}}, Passthrough Errors{{/if}}){{/if}}\n"
        "{{#else}}\n"
        "  {{#if handlers.length}}\n"
        "    Handlers defined\n"
        "  {{#else}}\n"
        "    No handlers defined\n"
        "  {{/if}}\n"
        "{{/if}}\n"
    ),
}
