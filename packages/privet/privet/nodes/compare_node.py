from __future__ import annotations

from typing import Any, Dict

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import (
    Input,
    Output,
    Eq,
    NodeSchema,
)

class CompareSchema(NodeSchema):
    NODE_TYPE = 'compare'
    TITLE = 'Compare'
    DISPLAY_NAME = 'Compare'
    VISUAL_WIDTH = 160
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'Compare Node'
    UI_INFOBOX_BODY = 'Compares two values using the configured operator and outputs the result.\n\nIf the data types of the values do not match, then the B value is converted to the type of the A value.'
    UI_CONTEXT_MENU_TITLE = 'Compare'
    DATA = {'comparisonFunction': '==', 'useComparisonFunctionInput': False}
    EDITORS = [
        {
            'type': 'dropdown',
            'label': 'Comparison Function',
            'dataKey': 'comparisonFunction',
            'useInputToggleDataKey': 'useComparisonFunctionInput',
            'options': [
                {'label': '==', 'value': '=='},
                {'label': '!=', 'value': '!='},
                {'label': '<', 'value': '<'},
                {'label': '<=', 'value': '<='},
                {'label': '>', 'value': '>'},
                {'label': '>=', 'value': '>='},
                {'label': 'and', 'value': 'and'},
                {'label': 'or', 'value': 'or'},
                {'label': 'xor', 'value': 'xor'},
                {'label': 'nand', 'value': 'nand'},
                {'label': 'nor', 'value': 'nor'},
                {'label': 'xnor', 'value': 'xnor'},
            ]
        }
    ]
    BODY = '{{#if useComparisonFunctionInput}}A (Comparison Function) B{{#else}}A {{comparisonFunction}} B{{/if}}'

    INPUTS = [
        Input(
            id='a',
            data_type='any',
            title='A',
        ),
        Input(
            id='b',
            data_type='any',
            title='B',
        ),
        Input(
            id='comparisonFunction',
            data_type='string',
            title='Comparison Function',
            show_if=Eq(data_key='useComparisonFunctionInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='boolean',
            title='Output',
        ),
    ]



@bindschema(schema=CompareSchema)
class CompareNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        from ..utils.data_values import coerce_type, coerce_type_optional

        # Get comparison function
        comparison_function = self.node.data.get('comparisonFunction', '==')
        if self.node.data.get('useComparisonFunctionInput'):
            func_input = inputs.get('comparisonFunction')
            if func_input:
                comparison_function = coerce_type(func_input, 'string')

        input_a = inputs.get('a')
        input_b = inputs.get('b')

        # Handle case where A is None
        if not input_a:
            if comparison_function == '==':
                result = not input_b
            elif comparison_function == '!=':
                result = bool(input_b)
            else:
                result = False

            return {
                'output': {
                    'type': 'boolean',
                    'value': result,
                }
            }

        value1 = input_a.get('value')
        type_a = input_a.get('type')

        # Coerce B to match A's type if different
        if input_b and input_b.get('type') != type_a:
            value2 = coerce_type_optional(input_b, type_a)
        else:
            value2 = input_b.get('value') if input_b else None

        # Perform comparison
        if comparison_function == '==':
            result = value1 == value2
        elif comparison_function == '!=':
            result = value1 != value2
        elif comparison_function == '<':
            result = value1 < value2
        elif comparison_function == '>':
            result = value1 > value2
        elif comparison_function == '<=':
            result = value1 <= value2
        elif comparison_function == '>=':
            result = value1 >= value2
        elif comparison_function == 'and':
            result = bool(value1 and value2)
        elif comparison_function == 'or':
            result = bool(value1 or value2)
        elif comparison_function == 'xor':
            result = bool(value1) != bool(value2)
        elif comparison_function == 'nand':
            result = not (value1 and value2)
        elif comparison_function == 'nor':
            result = not (value1 or value2)
        elif comparison_function == 'xnor':
            result = bool(value1) == bool(value2)
        else:
            result = False

        return {
            'output': {
                'type': 'boolean',
                'value': result,
            }
        }
