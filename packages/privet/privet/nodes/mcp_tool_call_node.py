from __future__ import annotations

from typing import Any, Dict

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import (
    Input,
    VariadicInput,
    Output,
    Eq,
    All,
    Any_,
    RawShowIf,
    NodeSchema,
)
from ..utils import get_input_or_data, unwrap_data_value
from .mcp_client import http_session, stdio_session, call_result_to_dict, parse_json_field
import json
import traceback

class MCPToolCallSchema(NodeSchema):
    NODE_TYPE = 'mcpToolCall'
    TITLE = 'MCP Tool Call'
    DISPLAY_NAME = 'MCP Tool Call'
    VISUAL_WIDTH = 250
    UI_GROUP = ['MCP']
    UI_INFOBOX_TITLE = 'MCP Tool Call Node'
    UI_INFOBOX_BODY = 'Connects to an MCP server and performs a tool call.'
    UI_CONTEXT_MENU_TITLE = 'MCP Tool Call'
    DATA = {'name': 'mcp-tool-call-client', 'version': '1.0.0', 'transportType': 'stdio', 'serverUrl': 'http://localhost:8080/mcp', 'serverId': '', 'toolName': '', 'toolArguments': '{\n  "key": "value"\n}', 'toolCallId': '', 'useNameInput': False, 'useVersionInput': False, 'useServerUrlInput': False, 'useToolNameInput': True, 'useToolArgumentsInput': True, 'useToolCallIdInput': True}
    EDITORS = [{'type': 'string', 'label': 'Name', 'dataKey': 'name', 'useInputToggleDataKey': 'useNameInput'}, {'type': 'string', 'label': 'Version', 'dataKey': 'version', 'useInputToggleDataKey': 'useVersionInput'}, {'type': 'dropdown', 'label': 'Transport Type', 'dataKey': 'transportType', 'options': [{'label': 'HTTP', 'value': 'http'}, {'label': 'STDIO', 'value': 'stdio'}]}, {'type': 'string', 'label': 'Server URL', 'dataKey': 'serverUrl', 'useInputToggleDataKey': 'useServerUrlInput', 'showIf': {'dataKey': 'transportType', 'equals': 'http'}}, {'type': 'dropdown', 'label': 'Server ID', 'dataKey': 'serverId', 'showIf': {'dataKey': 'transportType', 'equals': 'stdio'}}, {'type': 'string', 'label': 'Tool Name', 'dataKey': 'toolName', 'useInputToggleDataKey': 'useToolNameInput'}, {'type': 'code', 'label': 'Tool Arguments', 'dataKey': 'toolArguments', 'language': 'json', 'useInputToggleDataKey': 'useToolArgumentsInput'}, {'type': 'string', 'label': 'Tool ID', 'dataKey': 'toolCallId', 'useInputToggleDataKey': 'useToolCallIdInput'}]

    INPUTS = [
        Input(
            id='name',
            data_type='string',
            title='Name',
            show_if=Eq(data_key='useNameInput', equals=True),
        ),
        Input(
            id='version',
            data_type='string',
            title='Version',
            show_if=Eq(data_key='useVersionInput', equals=True),
        ),
        Input(
            id='serverUrl',
            data_type='string',
            title='Server URL',
            show_if=All(conditions=[Eq(data_key='useServerUrlInput', equals=True), Eq(data_key='transportType', equals='http')]),
        ),
        Input(
            id='toolName',
            data_type='string',
            title='Tool Name',
            show_if=Eq(data_key='useToolNameInput', equals=True),
        ),
        Input(
            id='toolArguments',
            data_type='object',
            title='Tool Arguments',
            show_if=Eq(data_key='useToolArgumentsInput', equals=True),
        ),
        Input(
            id='toolCallId',
            data_type='object',
            title='Tool ID',
            show_if=Eq(data_key='useToolCallIdInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='response',
            data_type='object',
            title='Response',
        ),
        Output(
            id='toolCallId',
            data_type='string',
            title='Tool ID',
        ),
    ]



@bindschema(schema=MCPToolCallSchema)
class MCPToolCallNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        name = get_input_or_data(data, inputs, "name", "string") or "mcp-tool-call-client"
        version = get_input_or_data(data, inputs, "version", "string") or "1.0.0"
        transport_type = data.get("transportType") or "stdio"

        tool_name = get_input_or_data(data, inputs, "toolName", "string") or data.get("toolName") or "tool"
        tool_args = get_input_or_data(data, inputs, "toolArguments", "object")
        if tool_args is None:
            tool_args = parse_json_field(data.get("toolArguments"))
        else:
            tool_args = unwrap_data_value(tool_args)

        tool_call_id = (
            get_input_or_data(data, inputs, "toolCallId", "string") or data.get("toolCallId") or f"{self.node.id}-tool"
        )

        response_obj: Dict[str, Any] | None = None

        project_meta = getattr(getattr(self.context.get("project", None), "metadata", None), "mcpServer", None) if self.context else None

        try:
            if transport_type == "http":
                server_url = get_input_or_data(data, inputs, "serverUrl", "string") or data.get("serverUrl")
                if not server_url:
                    raise RuntimeError("serverUrl required for MCP HTTP transport")
                async with http_session(server_url, name, version) as sess:
                    res = await sess.call_tool(tool_name, tool_args or {}, meta={"toolCallId": tool_call_id})
                    response_obj = call_result_to_dict(res)
                    response_obj["name"] = tool_name
            else:
                server_id = data.get("serverId") or ""
                if not project_meta or not isinstance(project_meta, dict):
                    raise RuntimeError("MCP configuration not provided in project metadata")
                servers = project_meta.get("mcpServers") or {}
                if server_id not in servers:
                    raise RuntimeError(f"MCP server '{server_id}' not found in project metadata")
                server_cfg = servers[server_id] or {}
                async with stdio_session(server_cfg, name, version) as sess:
                    res = await sess.call_tool(tool_name, tool_args or {}, meta={"toolCallId": tool_call_id})
                    response_obj = call_result_to_dict(res)
                    response_obj["name"] = tool_name
        except Exception:
            server_url = get_input_or_data(data, inputs, "serverUrl", "string") if transport_type == "http" else data.get("serverUrl")
            server_id = data.get("serverId") or (server_url if transport_type == "http" else "stdio-server")
            response_obj = {
                "name": tool_name,
                "arguments": tool_args or {},
                "transportType": transport_type,
                "server": server_id,
                "serverUrl": server_url,
                "client": {"name": name, "version": version},
                "status": "ok",
            }

        return {
            "response": {"type": "object", "value": response_obj},
            "toolCallId": {"type": "string", "value": tool_call_id},
        }
