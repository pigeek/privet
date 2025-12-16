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

class AudioSchema(NodeSchema):
    NODE_TYPE = 'audio'
    TITLE = 'Audio'
    DISPLAY_NAME = 'Audio'
    VISUAL_WIDTH = 300
    UI_GROUP = 'Data'
    UI_INFOBOX_TITLE = 'Audio Node'
    UI_INFOBOX_BODY = 'Defines an audio sample for use with other nodes.'
    UI_CONTEXT_MENU_TITLE = 'Audio'
    DATA = {'useDataInput': False, 'useMediaTypeInput': False}
    EDITORS = [{'type': 'fileBrowser', 'label': 'Audio File', 'dataKey': 'data', 'mediaTypeDataKey': 'mediaType', 'useInputToggleDataKey': 'useDataInput', 'accept': 'audio/*'}, {'type': 'string', 'label': 'Media Type', 'dataKey': 'mediaType', 'useInputToggleDataKey': 'useMediaTypeInput'}]

    INPUTS = [
        Input(
            id='data',
            data_type='binary',
            title='Data',
            show_if=Eq(data_key='useDataInput', equals=True),
        ),
        Input(
            id='mediaType',
            data_type='string',
            title='Media Type',
            show_if=Eq(data_key='useMediaTypeInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='data',
            data_type='audio',
            title='Audio Data',
        ),
    ]



@bindschema(schema=AudioSchema)
class AudioNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import base64
        from ..utils.data_values import expect_type, coerce_type_optional

        inputs = inputs or {}
        data = self.node.data or {}

        media_type = data.get("mediaType") or "audio/wav"
        if data.get("useMediaTypeInput"):
            media_type = coerce_type_optional(inputs.get("mediaType"), "string") or media_type

        audio_value: Any
        if data.get("useDataInput"):
            audio_value = expect_type(inputs.get("data"), "audio")
        else:
            data_ref = (data.get("data") or {}).get("refId")
            if not data_ref:
                raise ValueError("No audio data provided")
            project = (self.context or {}).get("project")
            encoded = getattr(project, "data", {}).get(data_ref) if project else None
            if encoded is None:
                raise ValueError(f"No data found for ref {data_ref}")
            try:
                audio_value = base64.b64decode(encoded)
            except Exception as exc:
                raise ValueError(f"Failed to decode audio data for ref {data_ref}") from exc

        return {
            "data": {
                "type": "audio",
                "value": {"data": audio_value, "mediaType": media_type},
            }
        }
