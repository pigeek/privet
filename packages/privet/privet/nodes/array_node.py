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

class ArraySchema(NodeSchema):
    NODE_TYPE = 'array'
    TITLE = 'Array'
    DISPLAY_NAME = 'Array'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Lists']
    UI_INFOBOX_TITLE = 'Array Node'
    UI_INFOBOX_BODY = 'Creates an array from the input values. By default, flattens any input arrays. Can be configured to keep arrays separate or deeply flatten.\n\nThe number of inputs is dynamic based on connections.'
    UI_CONTEXT_MENU_TITLE = 'Array'
    DATA = {'flatten': True, 'flattenDeep': False}
    EDITORS = [{'type': 'toggle', 'label': 'Flatten', 'dataKey': 'flatten'}, {'type': 'toggle', 'label': 'Deep', 'dataKey': 'flattenDeep'}]
    BODY = '{{#if flatten}}{{#if flattenDeep}}Flatten (Deep){{#else}}Flatten{{/if}}{{#else}}No Flatten{{/if}}'

    INPUTS = [
        VariadicInput(
            id_value='input',
            base_id='input',
            data_type='any',
            title='Input {n}',
            title_pattern='Input {n}',
            start_at=1,
            min=1,
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='any[]',
            title='Output',
            description='The array created from the inputs.',
        ),
        Output(
            id='indices',
            data_type='number[]',
            title='Indices',
            description='The indices of the output array.',
        ),
        Output(
            id='length',
            data_type='number',
            title='Length',
            description='The length of the output array.',
        ),
    ]



@bindschema(schema=ArraySchema)
class ArrayNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        output_array: list[Any] = []
        # Inputs named input{n}
        for key, val in inputs.items():
            if not key.startswith("input"):
                continue
            value = val.get("value") if isinstance(val, dict) else val
            if data.get("flatten"):
                if isinstance(value, list):
                    if data.get("flattenDeep"):
                        # Deep flatten
                        def _flatten(v):
                            for item in v:
                                if isinstance(item, list):
                                    yield from _flatten(item)
                                else:
                                    yield item

                        output_array.extend(list(_flatten(value)))
                    else:
                        output_array.extend(value)
                else:
                    output_array.append(value)
            else:
                output_array.append(value)

        indices = list(range(len(output_array)))

        return {
            "output": {"type": "any[]", "value": output_array},
            "indices": {"type": "number[]", "value": indices},
            "length": {"type": "number", "value": len(output_array)},
        }
