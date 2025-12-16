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

class PlayAudioSchema(NodeSchema):
    NODE_TYPE = 'playAudio'
    TITLE = 'Play Audio'
    DISPLAY_NAME = 'Play Audio'
    VISUAL_WIDTH = 200
    UI_GROUP = 'Input/Output'
    UI_INFOBOX_TITLE = 'Play Audio Node'
    UI_INFOBOX_BODY = 'Plays audio data to the speakers.'
    UI_CONTEXT_MENU_TITLE = 'Play Audio'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='data',
            data_type='audio',
            title='Data',
        ),
    ]

    OUTPUTS = [
        Output(
            id='data',
            data_type='audio',
            title='Audio Data',
        ),
    ]



@bindschema(schema=PlayAudioSchema)
class PlayAudioNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        from ..utils.data_values import expect_type

        inputs = inputs or {}

        audio_value = expect_type(inputs.get("data"), "audio")
        # In tests, just echo the audio back
        return {"data": {"type": "audio", "value": audio_value}}
