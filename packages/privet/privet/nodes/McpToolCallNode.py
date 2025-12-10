from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "mcpToolCall",
    "title": "MCP Tool Call",
    "displayName": "MCP Tool Call",
    "data": {"name": "mcp-tool-call-client", "version": "1.0.0", "transportType": "stdio", "serverUrl": "http://localhost:8080/mcp", "serverId": "", "toolName": "", "toolArguments": '{\n  "key": "value"\n}', "toolCallId": "", "useNameInput": False, "useVersionInput": False, "useServerUrlInput": False, "useToolNameInput": True, "useToolArgumentsInput": True, "useToolCallIdInput": True},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Connects to an MCP server and performs a tool call.",
        "infoBoxTitle": "MCP Tool Call Node",
        "contextMenuTitle": "MCP Tool Call",
        "group": ["MCP"],
    },
    "inputs": [
        {"id": "name", "title": "Name", "dataType": "string", "showIf": {"dataKey": "useNameInput", "equals": True}},
        {"id": "version", "title": "Version", "dataType": "string", "showIf": {"dataKey": "useVersionInput", "equals": True}},
        {"id": "serverUrl", "title": "Server URL", "dataType": "string", "showIf": {"all": [ {"dataKey": "useServerUrlInput", "equals": True}, {"dataKey": "transportType", "equals": "http"} ]}},
        {"id": "toolName", "title": "Tool Name", "dataType": "string", "showIf": {"dataKey": "useToolNameInput", "equals": True}},
        {"id": "toolArguments", "title": "Tool Arguments", "dataType": "object", "showIf": {"dataKey": "useToolArgumentsInput", "equals": True}},
        {"id": "toolCallId", "title": "Tool ID", "dataType": "object", "showIf": {"dataKey": "useToolCallIdInput", "equals": True}},
    ],
    "outputs": [
        {"id": "response", "title": "Response", "dataType": "object"},
        {"id": "toolCallId", "title": "Tool ID", "dataType": "string"},
    ],
    "editors": [
        {"type": "string", "label": "Name", "dataKey": "name", "useInputToggleDataKey": "useNameInput"},
        {"type": "string", "label": "Version", "dataKey": "version", "useInputToggleDataKey": "useVersionInput"},
        {"type": "dropdown", "label": "Transport Type", "dataKey": "transportType", "options": [ {"label": "HTTP", "value": "http"}, {"label": "STDIO", "value": "stdio"} ]},
        {"type": "string", "label": "Server URL", "dataKey": "serverUrl", "useInputToggleDataKey": "useServerUrlInput"},
        {"type": "string", "label": "Server ID", "dataKey": "serverId"},
        {"type": "string", "label": "Tool Name", "dataKey": "toolName", "useInputToggleDataKey": "useToolNameInput"},
        {"type": "code", "label": "Tool Arguments", "dataKey": "toolArguments", "language": "json", "useInputToggleDataKey": "useToolArgumentsInput"},
        {"type": "string", "label": "Tool ID", "dataKey": "toolCallId", "useInputToggleDataKey": "useToolCallIdInput"},
    ],
}
