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

class PopSchema(NodeSchema):
    NODE_TYPE = 'pop'
    TITLE = 'Pop'
    DISPLAY_NAME = 'Pop'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Lists']
    UI_INFOBOX_TITLE = 'Pop Node'
    UI_INFOBOX_BODY = 'Pops a value off the input array and outputs the remaining array and the popped value.'
    UI_CONTEXT_MENU_TITLE = 'Pop'
    DATA = {'fromFront': False}
    EDITORS = [{'type': 'toggle', 'label': 'Pop from front', 'dataKey': 'fromFront'}]
    BODY = '{{#if fromFront}}From front{{#else}}From back{{/if}}'

    INPUTS = [
        Input(
            id='array',
            data_type='any[]',
            title='Array',
        ),
    ]

    OUTPUTS = [
        Output(
            id='lastItem',
            data_type='any',
            title='Item',
        ),
        Output(
            id='restOfArray',
            data_type='any',
            title='Rest',
        ),
    ]



@bindschema(schema=PopSchema)
class PopNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
