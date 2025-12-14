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

class AssembleMessageSchema(NodeSchema):
    NODE_TYPE = 'assembleMessage'
    TITLE = 'Assemble Message'
    DISPLAY_NAME = 'Assemble Message'
    VISUAL_WIDTH = 250
    UI_GROUP = 'AI'
    UI_INFOBOX_TITLE = 'Assemble Message Node'
    UI_INFOBOX_BODY = 'Assembles a single chat message from multiple parts (text, images, documents, URLs).'
    UI_CONTEXT_MENU_TITLE = 'Assemble Message'
    DATA = {'type': 'user', 'useTypeInput': False, 'toolCallId': '', 'useToolCallIdInput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'Type', 'dataKey': 'type', 'useInputToggleDataKey': 'useTypeInput', 'options': [{'value': 'system', 'label': 'System'}, {'value': 'user', 'label': 'User'}, {'value': 'assistant', 'label': 'Assistant'}, {'value': 'function', 'label': 'Function'}]}, {'type': 'string', 'label': 'Tool Call ID', 'dataKey': 'toolCallId', 'useInputToggleDataKey': 'useToolCallIdInput', 'showIf': {'dataKey': 'type', 'equals': 'function'}}]
    BODY = '{{#if useTypeInput}}(Type From Input){{#else}}{{type}}{{/if}}\n{{#if useToolCallIdInput}}Tool Call ID: (From Input){{#else}}{{#if toolCallId}}Tool Call ID: {{toolCallId}}{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='type',
            data_type='string',
            title='Type',
            show_if=Eq(data_key='useTypeInput', equals=True),
        ),
        Input(
            id='toolCallId',
            data_type='string',
            title='Tool Call ID',
            show_if=Eq(data_key='useToolCallIdInput', equals=True),
        ),
        VariadicInput(
            id_value='part',
            base_id='part',
            data_type=['string', 'image', 'string[]', 'image[]', 'object', 'object[]', 'document', 'document[]'],
            title='Part {n}',
            title_pattern='Part {n}',
            start_at=1,
            min=1,
        ),
    ]

    OUTPUTS = [
        Output(
            id='message',
            data_type='chat-message',
            title='Message',
        ),
    ]



@bindschema(schema=AssembleMessageSchema)
class AssembleMessageNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
