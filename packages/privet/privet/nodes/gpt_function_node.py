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

class ToolSchema(NodeSchema):
    NODE_TYPE = 'gptFunction'
    TITLE = 'Tool'
    DISPLAY_NAME = 'Tool'
    VISUAL_WIDTH = 250
    UI_GROUP = ['AI']
    UI_INFOBOX_TITLE = 'Tool Node'
    UI_INFOBOX_BODY = 'Defines a tool (function) that the LLM can call in responses.'
    UI_CONTEXT_MENU_TITLE = 'Tool'
    DATA = {'name': 'newTool', 'description': 'No description provided', 'schema': '{\n  "type": "object",\n  "properties": {}\n}', 'useNameInput': False, 'useDescriptionInput': False, 'useSchemaInput': False, 'strict': False}
    EDITORS = [{'type': 'string', 'label': 'Name', 'dataKey': 'name', 'useInputToggleDataKey': 'useNameInput'}, {'type': 'toggle', 'label': 'Strict', 'dataKey': 'strict'}, {'type': 'code', 'label': 'Description', 'dataKey': 'description', 'useInputToggleDataKey': 'useDescriptionInput', 'language': 'markdown', 'height': 100}, {'type': 'custom', 'customEditorId': 'GptFunctionNodeJsonSchemaAiAssist', 'label': 'AI Assist'}, {'type': 'code', 'label': 'Schema', 'dataKey': 'schema', 'language': 'json', 'useInputToggleDataKey': 'useSchemaInput'}]
    BODY = '!markdown_{{name}}_: {{description}}'

    INPUTS = [
        Input(
            id='name',
            data_type='string',
            title='Name',
            show_if=Eq(data_key='useNameInput', equals=True),
        ),
        Input(
            id='description',
            data_type='string',
            title='Description',
            show_if=Eq(data_key='useDescriptionInput', equals=True),
        ),
        Input(
            id='schema',
            data_type='object',
            title='Schema',
            show_if=Eq(data_key='useSchemaInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='function',
            data_type='gpt-function',
            title='Function',
        ),
    ]



@bindschema(schema=ToolSchema)
class ToolNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
