from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "mcpGetPrompt",
    "title": "MCP Get Prompt",
    "displayName": "MCP Get Prompt",
    "data": {"name": "mcp-get-prompt-client", "version": "1.0.0", "transportType": "stdio", "serverUrl": "http://localhost:8080/mcp", "serverId": "", "promptName": "", "promptArguments": '{\n  "key": "value"\n}', "useNameInput": False, "useVersionInput": False, "useServerUrlInput": False, "usePromptNameInput": False, "usePromptArgumentsInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Connects to an MCP server and retrieves a prompt response.",
        "infoBoxTitle": "MCP Get Prompt Node",
        "contextMenuTitle": "MCP Get Prompt",
        "group": ["MCP"],
    },
    "inputs": [
        {"id": "name", "title": "Name", "dataType": "string", "showIf": {"dataKey": "useNameInput", "equals": True}},
        {"id": "version", "title": "Version", "dataType": "string", "showIf": {"dataKey": "useVersionInput", "equals": True}},
        {"id": "serverUrl", "title": "Server URL", "dataType": "string", "showIf": {"all": [ {"dataKey": "useServerUrlInput", "equals": True}, {"dataKey": "transportType", "equals": "http"} ]}},
        {"id": "promptName", "title": "Prompt Name", "dataType": "string", "showIf": {"dataKey": "usePromptNameInput", "equals": True}},
        {"id": "promptArguments", "title": "Prompt Arguments", "dataType": "object", "showIf": {"dataKey": "usePromptArgumentsInput", "equals": True}},
    ],
    "outputs": [
        {"id": "prompt", "title": "Prompt", "dataType": "object"},
    ],
    "editors": [
        {"type": "string", "label": "Name", "dataKey": "name", "useInputToggleDataKey": "useNameInput"},
        {"type": "string", "label": "Version", "dataKey": "version", "useInputToggleDataKey": "useVersionInput"},
        {"type": "dropdown", "label": "Transport Type", "dataKey": "transportType", "options": [ {"label": "HTTP", "value": "http"}, {"label": "STDIO", "value": "stdio"} ]},
        {"type": "string", "label": "Server URL", "dataKey": "serverUrl", "useInputToggleDataKey": "useServerUrlInput"},
        {"type": "string", "label": "Server ID", "dataKey": "serverId"},
        {"type": "string", "label": "Prompt Name", "dataKey": "promptName", "useInputToggleDataKey": "usePromptNameInput"},
        {"type": "code", "label": "Prompt Arguments", "dataKey": "promptArguments", "useInputToggleDataKey": "usePromptArgumentsInput", "language": "json"},
    ],
}

