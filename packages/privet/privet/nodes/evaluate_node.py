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

class EvaluateSchema(NodeSchema):
    NODE_TYPE = 'evaluate'
    TITLE = 'Evaluate'
    DISPLAY_NAME = 'Evaluate'
    VISUAL_WIDTH = 175
    UI_GROUP = ['Numbers']
    UI_INFOBOX_TITLE = 'Evaluate Node'
    UI_INFOBOX_BODY = 'Evaluates a mathematical operation on inputs.'
    UI_CONTEXT_MENU_TITLE = 'Evaluate'
    DATA = {'operation': '+', 'useOperationInput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'Operation', 'dataKey': 'operation', 'options': [{'label': '+', 'value': '+'}, {'label': '-', 'value': '-'}, {'label': '*', 'value': '*'}, {'label': '/', 'value': '/'}, {'label': '^', 'value': '^'}, {'label': '%', 'value': '%'}, {'label': 'abs', 'value': 'abs'}, {'label': 'negate', 'value': 'negate'}], 'useInputToggleDataKey': 'useOperationInput'}]
    BODY = '{{#if useOperationInput}}A (Operation) B{{#else}}A {{operation}} B{{/if}}'

    INPUTS = [
        Input(
            id='a',
            data_type='number',
            title='A',
        ),
        Input(
            id='b',
            data_type='number',
            title='B',
            show_if=RawShowIf(raw={'dataKey': 'operation', 'notIn': ['abs', 'negate']}),
        ),
        Input(
            id='operation',
            data_type='string',
            title='Operation',
            show_if=Eq(data_key='useOperationInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='number',
            title='Output',
        ),
    ]



@bindschema(schema=EvaluateSchema)
class EvaluateNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
