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

class ImageSchema(NodeSchema):
    NODE_TYPE = 'image'
    TITLE = 'Image'
    DISPLAY_NAME = 'Image'
    VISUAL_WIDTH = 250
    UI_GROUP = 'Data'
    UI_INFOBOX_TITLE = 'Image Node'
    UI_INFOBOX_BODY = 'Defines a static image for use with other nodes. Can convert a binary type into an image type.'
    UI_CONTEXT_MENU_TITLE = 'Image'
    DATA = {'useDataInput': False, 'mediaType': 'image/png', 'useMediaTypeInput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'Media Type', 'dataKey': 'mediaType', 'useInputToggleDataKey': 'useMediaTypeInput', 'options': [{'value': 'image/png', 'label': 'PNG'}, {'value': 'image/jpeg', 'label': 'JPEG'}, {'value': 'image/gif', 'label': 'GIF'}]}, {'type': 'imageBrowser', 'label': 'Image', 'dataKey': 'data', 'useInputToggleDataKey': 'useDataInput', 'mediaTypeDataKey': 'mediaType'}]

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
            id='image',
            data_type='image',
            title='Image',
        ),
    ]



@bindschema(schema=ImageSchema)
class ImageNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import base64
        from ..utils.data_values import expect_type, coerce_type_optional

        inputs = inputs or {}
        data = self.node.data or {}

        media_type = data.get("mediaType") or "image/png"
        if data.get("useMediaTypeInput"):
            media_type = coerce_type_optional(inputs.get("mediaType"), "string") or media_type

        image_bytes: Any
        if data.get("useDataInput"):
            image_value = expect_type(inputs.get("data"), "binary")
            image_bytes = image_value
        else:
            data_ref = (data.get("data") or {}).get("refId")
            if not data_ref:
                raise ValueError("No image data provided")
            project = (self.context or {}).get("project")
            encoded = getattr(project, "data", {}).get(data_ref) if project else None
            if encoded is None:
                raise ValueError(f"No data found for ref {data_ref}")
            try:
                image_bytes = base64.b64decode(encoded)
            except Exception as exc:
                raise ValueError(f"Failed to decode image data for ref {data_ref}") from exc

        return {
            "image": {
                "type": "image",
                "value": {"mediaType": media_type, "data": image_bytes},
            }
        }
