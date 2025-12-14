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

class CoalesceSchema(NodeSchema):
    NODE_TYPE = 'coalesce'
    TITLE = 'Coalesce'
    DISPLAY_NAME = 'Coalesce'
    VISUAL_WIDTH = 150
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'Coalesce Node'
    UI_INFOBOX_BODY = 'Takes in any number of inputs and outputs the first value that exists. Useful for consolidating branches after a Match node.'
    UI_CONTEXT_MENU_TITLE = 'Coalesce'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='conditional',
            data_type='boolean',
            title='Conditional',
        ),
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
            data_type='any',
            title='Output',
        ),
    ]



@bindschema(schema=CoalesceSchema)
class CoalesceNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        conditional = inputs.get("conditional")

        # Allow control-flow exclusion to propagate
        if isinstance(conditional, dict) and conditional.get("type") == "control-flow-excluded":
            return {"output": {"type": "control-flow-excluded", "value": None}}

        input_keys = [k for k in inputs.keys() if k.startswith("input")]
        ok_values = []
        for key in input_keys:
            val = inputs.get(key)
            if not isinstance(val, dict):
                continue
            if val.get("type") == "control-flow-excluded":
                continue
            if val.get("value") is None:
                continue
            ok_values.append(val)

        if not ok_values:
            return {"output": {"type": "control-flow-excluded", "value": None}}

        return {"output": ok_values[0]}
