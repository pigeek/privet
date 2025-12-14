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
        return await super().process(inputs)
