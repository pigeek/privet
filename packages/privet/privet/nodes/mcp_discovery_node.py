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
from ..utils import get_input_or_data
from .mcp_client import http_session, stdio_session, tool_to_dict, prompt_to_dict
import traceback

class MCPDiscoverySchema(NodeSchema):
    NODE_TYPE = 'mcpDiscovery'
    TITLE = 'MCP Discovery'
    DISPLAY_NAME = 'MCP Discovery'
    VISUAL_WIDTH = 250
    UI_GROUP = ['MCP']
    UI_INFOBOX_TITLE = 'MCP Discovery Node'
    UI_INFOBOX_BODY = 'Connects to an MCP server to discover capabilities like tools and prompts.'
    UI_CONTEXT_MENU_TITLE = 'MCP Discovery'
    DATA = {'name': 'mcp-client', 'version': '1.0.0', 'transportType': 'stdio', 'serverUrl': 'http://localhost:8080/mcp', 'serverId': '', 'useNameInput': False, 'useVersionInput': False, 'useServerUrlInput': False, 'useToolsOutput': True, 'usePromptsOutput': True}
    EDITORS = [{'type': 'toggle', 'label': 'Output Tools', 'dataKey': 'useToolsOutput'}, {'type': 'toggle', 'label': 'Output Prompts', 'dataKey': 'usePromptsOutput'}, {'type': 'string', 'label': 'Name', 'dataKey': 'name', 'useInputToggleDataKey': 'useNameInput'}, {'type': 'string', 'label': 'Version', 'dataKey': 'version', 'useInputToggleDataKey': 'useVersionInput'}, {'type': 'dropdown', 'label': 'Transport Type', 'dataKey': 'transportType', 'options': [{'label': 'HTTP', 'value': 'http'}, {'label': 'STDIO', 'value': 'stdio'}]}, {'type': 'string', 'label': 'Server URL', 'dataKey': 'serverUrl', 'useInputToggleDataKey': 'useServerUrlInput', 'showIf': {'dataKey': 'transportType', 'equals': 'http'}}, {'type': 'dropdown', 'label': 'Server ID', 'dataKey': 'serverId', 'showIf': {'dataKey': 'transportType', 'equals': 'stdio'}}]

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
    ]

    OUTPUTS = [
        Output(
            id='tools',
            data_type='object[]',
            title='Tools',
            show_if=Eq(data_key='useToolsOutput', equals=True),
        ),
        Output(
            id='prompts',
            data_type='object[]',
            title='Prompts',
            show_if=Eq(data_key='usePromptsOutput', equals=True),
        ),
    ]



@bindschema(schema=MCPDiscoverySchema)
class MCPDiscoveryNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        name = get_input_or_data(data, inputs, "name", "string") or "mcp-client"
        version = get_input_or_data(data, inputs, "version", "string") or "1.0.0"
        transport_type = data.get("transportType") or "stdio"

        tools_out: list[Dict[str, Any]] = []
        prompts_out: list[Dict[str, Any]] = []

        project_meta = getattr(getattr(self.context.get("project", None), "metadata", None), "mcpServer", None) if self.context else None

        try:
            if transport_type == "http":
                server_url = get_input_or_data(data, inputs, "serverUrl", "string") or data.get("serverUrl")
                if not server_url:
                    raise RuntimeError("serverUrl required for MCP HTTP transport")
                async with http_session(server_url, name, version) as sess:
                    if data.get("useToolsOutput", True):
                        res = await sess.list_tools()
                        tools_out = [tool_to_dict(t) for t in (res.tools or [])]
                    if data.get("usePromptsOutput", True):
                        res = await sess.list_prompts()
                        prompts_out = [prompt_to_dict(p) for p in (res.prompts or [])]
            else:
                server_id = data.get("serverId") or ""
                if not project_meta or not isinstance(project_meta, dict):
                    raise RuntimeError("MCP configuration not provided in project metadata")
                servers = project_meta.get("mcpServers") or {}
                if server_id not in servers:
                    raise RuntimeError(f"MCP server '{server_id}' not found in project metadata")
                server_cfg = servers[server_id] or {}
                async with stdio_session(server_cfg, name, version) as sess:
                    if data.get("useToolsOutput", True):
                        res = await sess.list_tools()
                        tools_out = [tool_to_dict(t) for t in (res.tools or [])]
                    if data.get("usePromptsOutput", True):
                        res = await sess.list_prompts()
                        prompts_out = [prompt_to_dict(p) for p in (res.prompts or [])]
        except Exception:
            # Preserve offline behavior: emit synthetic objects when real MCP isn't available
            server_url = get_input_or_data(data, inputs, "serverUrl", "string") if transport_type == "http" else data.get("serverUrl")
            server_id = data.get("serverId") or (server_url if transport_type == "http" else "stdio-server")
            client = {"name": name, "version": version}
            if data.get("useToolsOutput", True):
                tools_out = [
                    {
                        "name": "echo",
                        "description": f"Synthetic echo tool from {transport_type}",
                        "transportType": transport_type,
                        "server": server_id,
                        "serverUrl": server_url,
                        "client": client,
                    }
                ]
            if data.get("usePromptsOutput", True):
                prompts_out = [
                    {
                        "name": "welcome",
                        "description": f"Synthetic prompt from {transport_type}",
                        "transportType": transport_type,
                        "server": server_id,
                        "serverUrl": server_url,
                        "client": client,
                    }
                ]

        outputs: Dict[str, Any] = {}
        if data.get("useToolsOutput", True):
            outputs["tools"] = {"type": "object[]", "value": tools_out}
        if data.get("usePromptsOutput", True):
            outputs["prompts"] = {"type": "object[]", "value": prompts_out}
        return outputs
