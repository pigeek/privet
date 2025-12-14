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

class URLReferenceSchema(NodeSchema):
    NODE_TYPE = 'urlReference'
    TITLE = 'URL Reference'
    DISPLAY_NAME = 'URL Reference'
    VISUAL_WIDTH = 225
    UI_GROUP = 'Data'
    UI_INFOBOX_TITLE = 'URL Reference Node'
    UI_INFOBOX_BODY = 'Defines a reference to a URL, or converts a string into a URL reference.'
    UI_CONTEXT_MENU_TITLE = 'URL Reference'
    DATA = {'url': '', 'useUrlInput': False}
    EDITORS = [{'type': 'string', 'label': 'URL', 'dataKey': 'url', 'useInputToggleDataKey': 'useUrlInput'}]
    BODY = '{{#if useUrlInput}}(URL Using Input){{#else}}{{url}}{{/if}}'

    INPUTS = [
        Input(
            id='url',
            data_type='string',
            title='URL',
            show_if=Eq(data_key='useUrlInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='urlReference',
            data_type='object',
            title='URL Reference',
        ),
    ]



@bindschema(schema=URLReferenceSchema)
class URLReferenceNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
