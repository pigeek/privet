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

class DestructureSchema(NodeSchema):
    NODE_TYPE = 'destructure'
    TITLE = 'Destructure'
    DISPLAY_NAME = 'Destructure'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Objects']
    UI_INFOBOX_TITLE = 'Destructure Node'
    UI_INFOBOX_BODY = 'Destructures the input object by extracting values at configured JSONPath expressions.'
    UI_CONTEXT_MENU_TITLE = 'Destructure'
    DATA = {'paths': ['$.value']}
    EDITORS = [{'type': 'stringList', 'label': 'Paths', 'dataKey': 'paths', 'helperMessage': 'JSONPath expressions (one per line).'}]

    INPUTS = [
        Input(
            id='object',
            data_type='object',
            title='Object',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='match_',
            data_type='any',
            title='{{item}}',
            variadic={'type': 'dataList', 'dataKey': 'paths', 'baseId': 'match_', 'titleTemplate': '{{item}}'},
        ),
    ]



@bindschema(schema=DestructureSchema)
class DestructureNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
