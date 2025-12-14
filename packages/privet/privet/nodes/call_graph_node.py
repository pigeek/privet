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

class CallGraphSchema(NodeSchema):
    NODE_TYPE = 'callGraph'
    TITLE = 'Call Graph'
    DISPLAY_NAME = 'Call Graph'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Call Graph Node'
    UI_INFOBOX_BODY = 'Calls another graph and passes inputs to it. Use in combination with the Graph Reference node to call dynamic graphs.'
    UI_CONTEXT_MENU_TITLE = 'Call Graph'
    DATA = {'useErrorOutput': False}
    EDITORS = []

    INPUTS = [
        Input(
            id='graph',
            data_type='graph-reference',
            title='Graph',
            required=True,
        ),
        Input(
            id='inputs',
            data_type='object',
            title='Inputs',
        ),
    ]

    OUTPUTS = [
        Output(
            id='outputs',
            data_type='object',
            title='Outputs',
        ),
        Output(
            id='error',
            data_type='string',
            title='Error',
            show_if=Eq(data_key='useErrorOutput', equals=True),
        ),
    ]



@bindschema(schema=CallGraphSchema)
class CallGraphNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
