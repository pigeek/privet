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

class RaceInputsSchema(NodeSchema):
    NODE_TYPE = 'raceInputs'
    TITLE = 'Race Inputs'
    DISPLAY_NAME = 'Race Inputs'
    VISUAL_WIDTH = 300
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'Race Inputs Node'
    UI_INFOBOX_BODY = 'Takes multiple inputs and outputs the first that finishes; others are cancelled.'
    UI_CONTEXT_MENU_TITLE = 'Race Inputs'
    DATA = {}
    EDITORS = []

    INPUTS = [
        VariadicInput(
            id_value='input',
            base_id='input',
            data_type='any',
            title='Input {n}',
            title_pattern='Input {n}',
            start_at=1,
            min=1,
        ),
    ]

    OUTPUTS = [
        Output(
            id='result',
            data_type='any',
            title='Result',
        ),
    ]



@bindschema(schema=RaceInputsSchema)
class RaceInputsNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
