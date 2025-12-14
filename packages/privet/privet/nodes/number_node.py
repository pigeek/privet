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

class NumberSchema(NodeSchema):
    NODE_TYPE = 'number'
    TITLE = 'Number'
    DISPLAY_NAME = 'Number'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Numbers']
    UI_INFOBOX_TITLE = 'Number Node'
    UI_INFOBOX_BODY = 'Outputs a number constant, or converts an input value into a number.\nCan round to a certain number of decimals.'
    UI_CONTEXT_MENU_TITLE = 'Number'
    DATA = {'value': 0, 'useValueInput': False, 'round': False, 'roundTo': 0}
    EDITORS = [{'type': 'number', 'label': 'Value', 'dataKey': 'value', 'useInputToggleDataKey': 'useValueInput'}, {'type': 'toggle', 'label': 'Round', 'dataKey': 'round'}, {'type': 'number', 'label': 'Round To', 'dataKey': 'roundTo'}]
    BODY = '{{#if useValueInput}}(Input to number){{#else}}{{value}}{{/if}}'

    INPUTS = [
        Input(
            id='input',
            data_type='any',
            title='Input',
            show_if=Eq(data_key='useValueInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='value',
            data_type='number',
            title='Value',
        ),
    ]



@bindschema(schema=NumberSchema)
class NumberNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        value = data.get("value", 0)
        if data.get("useValueInput") and inputs.get("input") is not None:
            try:
                value = float(inputs["input"].get("value"))
            except Exception:
                value = data.get("value", 0) or 0

        round_to = data.get("roundTo", 0) or 0
        if data.get("round"):
            factor = 10 ** round_to
            value = round(value * factor) / factor

        return {"value": {"type": "number", "value": value}}
