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
        from ..utils.data_values import coerce_type, coerce_type_optional

        # Get operation
        operation = self.node.data.get('operation', '+')
        if self.node.data.get('useOperationInput'):
            op_input = inputs.get('operation')
            if op_input:
                operation = coerce_type(op_input, 'string')

        # Get input values
        input_a = coerce_type_optional(inputs.get('a'), 'number')

        # Handle unary operations
        unary_operations = ['abs', 'negate']
        if operation in unary_operations:
            if input_a is None:
                raise ValueError("Missing input A")

            if operation == 'abs':
                result = abs(input_a)
            elif operation == 'negate':
                result = -input_a
            else:
                result = 0

            return {
                'output': {
                    'type': 'number',
                    'value': result,
                }
            }

        # Handle binary operations
        input_b = coerce_type_optional(inputs.get('b'), 'number')

        if input_a is None or input_b is None:
            raise ValueError("Missing inputs")

        if operation == '+':
            result = input_a + input_b
        elif operation == '-':
            result = input_a - input_b
        elif operation == '*':
            result = input_a * input_b
        elif operation == '/':
            result = input_a / input_b
        elif operation == '^':
            result = input_a ** input_b
        elif operation == '%':
            result = input_a % input_b
        else:
            result = 0

        return {
            'output': {
                'type': 'number',
                'value': result,
            }
        }
