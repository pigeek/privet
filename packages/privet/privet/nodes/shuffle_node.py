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

class ShuffleSchema(NodeSchema):
    NODE_TYPE = 'shuffle'
    TITLE = 'Shuffle'
    DISPLAY_NAME = 'Shuffle'
    VISUAL_WIDTH = 175
    UI_GROUP = ['Lists']
    UI_INFOBOX_TITLE = 'Shuffle Node'
    UI_INFOBOX_BODY = 'Shuffles the input array. Outputs the shuffled array.'
    UI_CONTEXT_MENU_TITLE = 'Shuffle'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='array',
            data_type='any[]',
            title='Array',
        ),
    ]

    OUTPUTS = [
        Output(
            id='shuffled',
            data_type='any[]',
            title='Shuffled',
        ),
    ]



@bindschema(schema=ShuffleSchema)
class ShuffleNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import random

        input_value = inputs.get('array', {})

        # Check if it's an array DataValue
        if isinstance(input_value, dict) and input_value.get('type', '').endswith('[]'):
            items = input_value.get('value', [])
        elif isinstance(input_value, dict) and 'value' in input_value:
            # Single value, wrap in array
            items = [input_value.get('value')]
        else:
            items = []

        # Shuffle the items
        shuffled = items.copy()
        random.shuffle(shuffled)

        # Preserve original type
        original_type = inputs.get('array', {}).get('type', 'any[]')

        return {
            'shuffled': {
                'type': original_type,
                'value': shuffled,
            }
        }
