from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "mcpDiscovery",
    "title": "MCP Discovery",
    "displayName": "MCP Discovery",
    "data": {"name": "mcp-client", "version": "1.0.0", "transportType": "stdio", "serverUrl": "http://localhost:8080/mcp", "serverId": "", "useNameInput": False, "useVersionInput": False, "useServerUrlInput": False, "useToolsOutput": True, "usePromptsOutput": True},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Connects to an MCP server to discover capabilities like tools and prompts.",
        "infoBoxTitle": "MCP Discovery Node",
        "contextMenuTitle": "MCP Discovery",
        "group": ["MCP"],
    },
    "inputs": [
        {"id": "name", "title": "Name", "dataType": "string", "showIf": {"dataKey": "useNameInput", "equals": True}},
        {"id": "version", "title": "Version", "dataType": "string", "showIf": {"dataKey": "useVersionInput", "equals": True}},
        {"id": "serverUrl", "title": "Server URL", "dataType": "string", "showIf": {"all": [ {"dataKey": "useServerUrlInput", "equals": True}, {"dataKey": "transportType", "equals": "http"} ]}},
    ],
    "outputs": [
        {"id": "tools", "title": "Tools", "dataType": "object[]", "showIf": {"dataKey": "useToolsOutput", "equals": True}},
        {"id": "prompts", "title": "Prompts", "dataType": "object[]", "showIf": {"dataKey": "usePromptsOutput", "equals": True}},
    ],
    "editors": [
        {"type": "toggle", "label": "Output Tools", "dataKey": "useToolsOutput"},
        {"type": "toggle", "label": "Output Prompts", "dataKey": "usePromptsOutput"},
        {"type": "string", "label": "Name", "dataKey": "name", "useInputToggleDataKey": "useNameInput"},
        {"type": "string", "label": "Version", "dataKey": "version", "useInputToggleDataKey": "useVersionInput"},
        {"type": "dropdown", "label": "Transport Type", "dataKey": "transportType", "options": [ {"label": "HTTP", "value": "http"}, {"label": "STDIO", "value": "stdio"} ]},
        {"type": "string", "label": "Server URL", "dataKey": "serverUrl", "useInputToggleDataKey": "useServerUrlInput"},
        {"type": "string", "label": "Server ID", "dataKey": "serverId"},
    ],
}

