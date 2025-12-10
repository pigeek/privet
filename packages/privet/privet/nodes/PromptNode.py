from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "prompt",
    "title": "Prompt",
    "displayName": "Prompt",
    "data": {
        "type": "user",
        "useTypeInput": False,
        "promptText": "{{input}}",
        "enableFunctionCall": False,
        "computeTokenCount": False,
        "isCacheBreakpoint": False,
        "useIsCacheBreakpointInput": False,
        "name": None,
        "useNameInput": False,
    },
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Outputs a chat message (system/user/assistant/function) with interpolation like Text.",
        "infoBoxTitle": "Prompt Node",
        "contextMenuTitle": "Prompt",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "function-call", "title": "Function Call", "dataType": "object", "showIf": {"all": [{"dataKey": "enableFunctionCall", "equals": True}, {"dataKey": "type", "equals": "assistant"}]}},
        {"id": "type", "title": "Type", "dataType": "string", "showIf": {"dataKey": "useTypeInput", "equals": True}},
        {"id": "name", "title": "Name/ID", "dataType": "string", "showIf": {"dataKey": "useNameInput", "equals": True}},
        {"id": "isCacheBreakpoint", "title": "Is Cache Breakpoint", "dataType": "boolean", "showIf": {"dataKey": "useIsCacheBreakpointInput", "equals": True}},
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "chat-message"},
        {"id": "tokenCount", "title": "Token Count", "dataType": "number", "showIf": {"dataKey": "computeTokenCount", "equals": True}},
    ],
    "editors": [
        {"type": "custom", "customEditorId": "PromptNodeAiAssist", "label": "Generate Using AI"},
        {"type": "dropdown", "label": "Type", "dataKey": "type", "useInputToggleDataKey": "useTypeInput", "options": [
            {"value": "system", "label": "System"},
            {"value": "user", "label": "User"},
            {"value": "assistant", "label": "Assistant"},
            {"value": "function", "label": "Function"}
        ]},
        {"type": "string", "label": "Name", "dataKey": "name", "useInputToggleDataKey": "useNameInput"},
        {"type": "toggle", "label": "Enable Function Call", "dataKey": "enableFunctionCall"},
        {"type": "toggle", "label": "Compute Token Count", "dataKey": "computeTokenCount"},
        {"type": "toggle", "label": "Is Cache Breakpoint", "dataKey": "isCacheBreakpoint", "useInputToggleDataKey": "useIsCacheBreakpointInput"},
        {"type": "code", "label": "Prompt Text", "dataKey": "promptText", "language": "prompt-interpolation-markdown", "theme": "prompt-interpolation"},
    ],
    "body": [
        {"type": "markdown", "text": "_{{type}}{{#if name}} ({{name}}){{/if}}{{#if isCacheBreakpoint}} (Cache Breakpoint){{/if}}_"},
        {"type": "colorized", "text": "{{promptText}}", "language": "prompt-interpolation-markdown", "theme": "prompt-interpolation"},
    ],
    "interpolationInputs": {"dataKey": "promptText", "dataType": "string", "ignorePrefixes": ["@graphInputs.", "@context."]},
}

