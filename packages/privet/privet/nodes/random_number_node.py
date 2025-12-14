from __future__ import annotations

from typing import Any, Dict
import random

from ..utils import coerce_type_optional

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

class RNGSchema(NodeSchema):
    NODE_TYPE = 'randomNumber'
    TITLE = 'RNG'
    DISPLAY_NAME = 'Random Number'
    VISUAL_WIDTH = 150
    UI_GROUP = ['Numbers']
    UI_INFOBOX_TITLE = 'RNG Node'
    UI_INFOBOX_BODY = 'Outputs a random number between configured min and max values.'
    UI_CONTEXT_MENU_TITLE = 'RNG'
    DATA = {'min': 0, 'max': 1, 'integers': False, 'maxInclusive': False, 'useMinInput': False, 'useMaxInput': False}
    EDITORS = [{'type': 'number', 'label': 'Min', 'dataKey': 'min', 'useInputToggleDataKey': 'useMinInput'}, {'type': 'number', 'label': 'Max', 'dataKey': 'max', 'useInputToggleDataKey': 'useMaxInput'}, {'type': 'toggle', 'label': 'Integers', 'dataKey': 'integers'}, {'type': 'toggle', 'label': 'Max Inclusive', 'dataKey': 'maxInclusive'}]
    BODY = 'Min: {{#if useMinInput}}(Input){{#else}}{{min}}{{/if}}\nMax: {{#if useMaxInput}}(Input){{#else}}{{max}}{{/if}}\n{{#if integers}}Integers{{#else}}Floats{{/if}}\n{{#if maxInclusive}}Max Inclusive{{#else}}Max Exclusive{{/if}}'

    INPUTS = [
        Input(
            id='min',
            data_type='number',
            title='Min',
            show_if=Eq(data_key='useMinInput', equals=True),
        ),
        Input(
            id='max',
            data_type='number',
            title='Max',
            show_if=Eq(data_key='useMaxInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='value',
            data_type='number',
            title='Value',
        ),
    ]



@bindschema(schema=RNGSchema)
class RNGNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        min_val = coerce_type_optional(inputs.get("min"), "number") if data.get("useMinInput") else data.get("min", 0)
        max_val = coerce_type_optional(inputs.get("max"), "number") if data.get("useMaxInput") else data.get("max", 1)

        try:
            min_val = float(min_val if min_val is not None else 0)
        except Exception:
            min_val = 0.0
        try:
            max_val = float(max_val if max_val is not None else 1)
        except Exception:
            max_val = 1.0

        if data.get("integers") and data.get("maxInclusive"):
            max_val += 1

        value = random.random() * (max_val - min_val) + min_val
        if data.get("integers"):
            value = int(value)

        return {"value": {"type": "number", "value": value}}
