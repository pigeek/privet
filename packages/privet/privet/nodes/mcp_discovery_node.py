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
        return await super().process(inputs)
