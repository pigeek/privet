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

class ExtractJSONSchema(NodeSchema):
    NODE_TYPE = 'extractJson'
    TITLE = 'Extract JSON'
    DISPLAY_NAME = 'Extract JSON'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Objects']
    UI_INFOBOX_TITLE = 'Extract JSON Node'
    UI_INFOBOX_BODY = 'Finds and parses the first JSON object in the input text.'
    UI_CONTEXT_MENU_TITLE = 'Extract JSON'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Input',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='object',
            title='Output',
        ),
        Output(
            id='noMatch',
            data_type='string',
            title='No Match',
        ),
    ]



@bindschema(schema=ExtractJSONSchema)
class ExtractJSONNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import json
        from ..utils.data_values import expect_type

        input_string = expect_type(inputs.get('input'), 'string')

        # Try direct JSON parsing first
        try:
            parsed = json.loads(input_string)
            return {
                'output': {
                    'type': 'object',
                    'value': parsed,
                },
                'noMatch': {
                    'type': 'control-flow-excluded',
                    'value': None,
                },
            }
        except (json.JSONDecodeError, ValueError):
            # Fall back to manual parsing
            pass

        # Find the first { or [ and the last } or ], and try parsing everything in between
        first_bracket = input_string.find('{')
        last_bracket = input_string.rfind('}')
        first_square_bracket = input_string.find('[')
        last_square_bracket = input_string.rfind(']')

        if first_bracket >= 0 and first_square_bracket >= 0:
            first_index = min(first_bracket, first_square_bracket)
        elif first_bracket >= 0:
            first_index = first_bracket
        elif first_square_bracket >= 0:
            first_index = first_square_bracket
        else:
            first_index = -1

        if last_bracket >= 0 and last_square_bracket >= 0:
            last_index = max(last_bracket, last_square_bracket)
        elif last_bracket >= 0:
            last_index = last_bracket
        elif last_square_bracket >= 0:
            last_index = last_square_bracket
        else:
            last_index = -1

        if first_index < 0 or last_index < 0:
            return {
                'noMatch': {
                    'type': 'string',
                    'value': input_string,
                },
                'output': {
                    'type': 'control-flow-excluded',
                    'value': None,
                },
            }

        substring = input_string[first_index:last_index + 1]

        try:
            json_object = json.loads(substring)
            return {
                'output': {
                    'type': 'object',
                    'value': json_object,
                },
                'noMatch': {
                    'type': 'control-flow-excluded',
                    'value': None,
                },
            }
        except (json.JSONDecodeError, ValueError):
            return {
                'noMatch': {
                    'type': 'string',
                    'value': input_string,
                },
                'output': {
                    'type': 'control-flow-excluded',
                    'value': None,
                },
            }
