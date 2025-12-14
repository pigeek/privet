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

class CommentSchema(NodeSchema):
    NODE_TYPE = 'comment'
    TITLE = 'Comment'
    DISPLAY_NAME = 'Comment'
    VISUAL_WIDTH = 600
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Comment Node'
    UI_INFOBOX_BODY = 'A comment node for adding notes to a graph.'
    UI_CONTEXT_MENU_TITLE = 'Comment'
    DATA = {'text': '', 'height': 600, 'color': 'rgba(255,255,255,1)', 'backgroundColor': 'rgba(0,0,0,0.05)'}
    EDITORS = [{'type': 'color', 'label': 'Color', 'dataKey': 'color'}, {'type': 'color', 'label': 'Background Color', 'dataKey': 'backgroundColor'}, {'type': 'code', 'label': 'Text', 'dataKey': 'text', 'language': 'markdown', 'theme': 'vs-dark'}]

    INPUTS = [

    ]

    OUTPUTS = [

    ]



@bindschema(schema=CommentSchema)
class CommentNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
