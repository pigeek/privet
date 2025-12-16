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
from .mcp_client import http_session, stdio_session, prompt_result_to_dict, parse_json_field
import json
import traceback

class MCPGetPromptSchema(NodeSchema):
    NODE_TYPE = 'mcpGetPrompt'
    TITLE = 'MCP Get Prompt'
    DISPLAY_NAME = 'MCP Get Prompt'
    VISUAL_WIDTH = 250
    UI_GROUP = ['MCP']
    UI_INFOBOX_TITLE = 'MCP Get Prompt Node'
    UI_INFOBOX_BODY = 'Connects to an MCP server and retrieves a prompt response.'
    UI_CONTEXT_MENU_TITLE = 'MCP Get Prompt'
    DATA = {'name': 'mcp-get-prompt-client', 'version': '1.0.0', 'transportType': 'stdio', 'serverUrl': 'http://localhost:8080/mcp', 'serverId': '', 'promptName': '', 'promptArguments': '{\n  "key": "value"\n}', 'useNameInput': False, 'useVersionInput': False, 'useServerUrlInput': False, 'usePromptNameInput': False, 'usePromptArgumentsInput': False}
    EDITORS = [{'type': 'string', 'label': 'Name', 'dataKey': 'name', 'useInputToggleDataKey': 'useNameInput'}, {'type': 'string', 'label': 'Version', 'dataKey': 'version', 'useInputToggleDataKey': 'useVersionInput'}, {'type': 'dropdown', 'label': 'Transport Type', 'dataKey': 'transportType', 'options': [{'label': 'HTTP', 'value': 'http'}, {'label': 'STDIO', 'value': 'stdio'}]}, {'type': 'string', 'label': 'Server URL', 'dataKey': 'serverUrl', 'useInputToggleDataKey': 'useServerUrlInput', 'showIf': {'dataKey': 'transportType', 'equals': 'http'}}, {'type': 'dropdown', 'label': 'Server ID', 'dataKey': 'serverId', 'showIf': {'dataKey': 'transportType', 'equals': 'stdio'}}, {'type': 'string', 'label': 'Prompt Name', 'dataKey': 'promptName', 'useInputToggleDataKey': 'usePromptNameInput'}, {'type': 'code', 'label': 'Prompt Arguments', 'dataKey': 'promptArguments', 'useInputToggleDataKey': 'usePromptArgumentsInput', 'language': 'json'}]

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
            id='promptName',
            data_type='string',
            title='Prompt Name',
            show_if=Eq(data_key='usePromptNameInput', equals=True),
        ),
        Input(
            id='promptArguments',
            data_type='object',
            title='Prompt Arguments',
            show_if=Eq(data_key='usePromptArgumentsInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='prompt',
            data_type='object',
            title='Prompt',
        ),
    ]



@bindschema(schema=MCPGetPromptSchema)
class MCPGetPromptNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        name = get_input_or_data(data, inputs, "name", "string") or "mcp-get-prompt-client"
        version = get_input_or_data(data, inputs, "version", "string") or "1.0.0"
        transport_type = data.get("transportType") or "stdio"
        prompt_name = get_input_or_data(data, inputs, "promptName", "string") or data.get("promptName") or "prompt"

        prompt_args = get_input_or_data(data, inputs, "promptArguments", "object")
        if prompt_args is None:
            prompt_args = parse_json_field(data.get("promptArguments"))
        else:
            prompt_args = unwrap_data_value(prompt_args)

        prompt_obj: Dict[str, Any] | None = None

        project_meta = getattr(getattr(self.context.get("project", None), "metadata", None), "mcpServer", None) if self.context else None

        try:
            if transport_type == "http":
                server_url = get_input_or_data(data, inputs, "serverUrl", "string") or data.get("serverUrl")
                if not server_url:
                    raise RuntimeError("serverUrl required for MCP HTTP transport")
                async with http_session(server_url, name, version) as sess:
                    res = await sess.get_prompt(prompt_name, prompt_args or {})
                    prompt_obj = prompt_result_to_dict(res, prompt_name)
            else:
                server_id = data.get("serverId") or ""
                if not project_meta or not isinstance(project_meta, dict):
                    raise RuntimeError("MCP configuration not provided in project metadata")
                servers = project_meta.get("mcpServers") or {}
                if server_id not in servers:
                    raise RuntimeError(f"MCP server '{server_id}' not found in project metadata")
                server_cfg = servers[server_id] or {}
                async with stdio_session(server_cfg, name, version) as sess:
                    res = await sess.get_prompt(prompt_name, prompt_args or {})
                    prompt_obj = prompt_result_to_dict(res, prompt_name)
        except Exception:
            server_url = get_input_or_data(data, inputs, "serverUrl", "string") if transport_type == "http" else data.get("serverUrl")
            server_id = data.get("serverId") or (server_url if transport_type == "http" else "stdio-server")
            prompt_obj = {
                "name": prompt_name,
                "arguments": prompt_args or {},
                "transportType": transport_type,
                "server": server_id,
                "serverUrl": server_url,
                "client": {"name": name, "version": version},
                "content": f"Prompt {prompt_name} from {server_id}",
            }

        return {"prompt": {"type": "object", "value": prompt_obj}}
