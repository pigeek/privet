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
        return await super().process(inputs)
