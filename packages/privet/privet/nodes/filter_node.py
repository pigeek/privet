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

class FilterSchema(NodeSchema):
    NODE_TYPE = 'filter'
    TITLE = 'Filter'
    DISPLAY_NAME = 'Filter'
    VISUAL_WIDTH = 175
    UI_GROUP = ['Lists']
    UI_INFOBOX_TITLE = 'Filter Node'
    UI_INFOBOX_BODY = 'Takes in both an array of values and an array of booleans of the same length, and filters where the boolean is true.'
    UI_CONTEXT_MENU_TITLE = 'Filter'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='array',
            data_type='any[]',
            title='Array',
            required=True,
        ),
        Input(
            id='include',
            data_type='boolean[]',
            title='Include',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='filtered',
            data_type='any[]',
            title='Filtered',
        ),
    ]



@bindschema(schema=FilterSchema)
class FilterNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
