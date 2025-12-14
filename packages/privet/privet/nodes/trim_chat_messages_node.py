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

class TrimChatMessagesSchema(NodeSchema):
    NODE_TYPE = 'trimChatMessages'
    TITLE = 'Trim Chat Messages'
    DISPLAY_NAME = 'Trim Chat Messages'
    VISUAL_WIDTH = 200
    UI_GROUP = ['AI']
    UI_INFOBOX_TITLE = 'Trim Chat Messages Node'
    UI_INFOBOX_BODY = 'Slices messages from start or end until under token limit.'
    UI_CONTEXT_MENU_TITLE = 'Trim Chat Messages'
    DATA = {'maxTokenCount': 4096, 'removeFromBeginning': True, 'useMaxTokenCountInput': False, 'useRemoveFromBeginningInput': False}
    EDITORS = [{'type': 'number', 'label': 'Max Token Count', 'dataKey': 'maxTokenCount', 'useInputToggleDataKey': 'useMaxTokenCountInput'}, {'type': 'toggle', 'label': 'Remove From Beginning', 'dataKey': 'removeFromBeginning', 'useInputToggleDataKey': 'useRemoveFromBeginningInput'}]
    BODY = 'Max Token Count: {{#if useMaxTokenCountInput}}(From Input){{#else}}{{maxTokenCount}}{{/if}}\nRemove From Beginning: {{#if useRemoveFromBeginningInput}}(From Input){{#else}}{{#if removeFromBeginning}}Yes{{#else}}No{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='input',
            data_type='chat-message[]',
            title='Input',
        ),
        Input(
            id='maxTokenCount',
            data_type='number',
            title='Max Token Count',
            show_if=Eq(data_key='useMaxTokenCountInput', equals=True),
        ),
        Input(
            id='removeFromBeginning',
            data_type='boolean',
            title='Remove From Beginning',
            show_if=Eq(data_key='useRemoveFromBeginningInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='trimmed',
            data_type='chat-message[]',
            title='Trimmed',
        ),
    ]



@bindschema(schema=TrimChatMessagesSchema)
class TrimChatMessagesNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
