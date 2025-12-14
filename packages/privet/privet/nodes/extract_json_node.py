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

class ExtractJSONSchema(NodeSchema):
    NODE_TYPE = 'extractJson'
    TITLE = 'Extract JSON'
    DISPLAY_NAME = 'Extract JSON'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Objects']
    UI_INFOBOX_TITLE = 'Extract JSON Node'
    UI_INFOBOX_BODY = 'Finds and parses the first JSON object in the input text.'
    UI_CONTEXT_MENU_TITLE = 'Extract JSON'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Input',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='object',
            title='Output',
        ),
        Output(
            id='noMatch',
            data_type='string',
            title='No Match',
        ),
    ]



@bindschema(schema=ExtractJSONSchema)
class ExtractJSONNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
