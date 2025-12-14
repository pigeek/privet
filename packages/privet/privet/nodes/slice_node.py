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

class SliceSchema(NodeSchema):
    NODE_TYPE = 'slice'
    TITLE = 'Slice'
    DISPLAY_NAME = 'Slice'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Lists']
    UI_INFOBOX_TITLE = 'Slice Node'
    UI_INFOBOX_BODY = 'Slices an array from the start index for the count number of elements.'
    UI_CONTEXT_MENU_TITLE = 'Slice'
    DATA = {'start': 0, 'useStartInput': False, 'count': None, 'useCountInput': False}
    EDITORS = [{'type': 'number', 'label': 'Start', 'dataKey': 'start', 'useInputToggleDataKey': 'useStartInput', 'allowEmpty': True}, {'type': 'number', 'label': 'Count', 'dataKey': 'count', 'useInputToggleDataKey': 'useCountInput', 'allowEmpty': True}]
    BODY = 'Start: {{#if useStartInput}}(Using Input){{#else}}{{#if start}}{{start}}{{#else}}0{{/if}}{{/if}}\nCount: {{#if useCountInput}}(Using Input){{#else}}{{#if count}}{{count}}{{#else}}All{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='input',
            data_type='any[]',
            title='Input',
        ),
        Input(
            id='start',
            data_type='number',
            title='Start',
            show_if=Eq(data_key='useStartInput', equals=True),
        ),
        Input(
            id='count',
            data_type='number',
            title='Count',
            show_if=Eq(data_key='useCountInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='any[]',
            title='Output',
        ),
    ]



@bindschema(schema=SliceSchema)
class SliceNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
