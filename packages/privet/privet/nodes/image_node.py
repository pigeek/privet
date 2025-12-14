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
        return await super().process(inputs)
