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

class ShuffleSchema(NodeSchema):
    NODE_TYPE = 'shuffle'
    TITLE = 'Shuffle'
    DISPLAY_NAME = 'Shuffle'
    VISUAL_WIDTH = 175
    UI_GROUP = ['Lists']
    UI_INFOBOX_TITLE = 'Shuffle Node'
    UI_INFOBOX_BODY = 'Shuffles the input array. Outputs the shuffled array.'
    UI_CONTEXT_MENU_TITLE = 'Shuffle'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='array',
            data_type='any[]',
            title='Array',
        ),
    ]

    OUTPUTS = [
        Output(
            id='shuffled',
            data_type='any[]',
            title='Shuffled',
        ),
    ]



@bindschema(schema=ShuffleSchema)
class ShuffleNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
