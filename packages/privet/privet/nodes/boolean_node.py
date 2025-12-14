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

class BoolSchema(NodeSchema):
    NODE_TYPE = 'boolean'
    TITLE = 'Bool'
    DISPLAY_NAME = 'Boolean'
    VISUAL_WIDTH = 130
    UI_GROUP = ['Data']
    UI_INFOBOX_TITLE = 'Bool Node'
    UI_INFOBOX_BODY = 'Outputs a boolean constant, or converts an input value into a boolean.'
    UI_CONTEXT_MENU_TITLE = 'Bool'
    DATA = {'value': False, 'useValueInput': False}
    EDITORS = [{'type': 'toggle', 'label': 'Value', 'dataKey': 'value', 'useInputToggleDataKey': 'useValueInput'}]
    BODY = '{{#if useValueInput}}(Input to bool){{#else}}{{value}}{{/if}}'

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
            data_type='boolean',
            title='Value',
        ),
    ]



@bindschema(schema=BoolSchema)
class BoolNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        value = bool(data.get("value", False))
        if data.get("useValueInput") and inputs.get("input") is not None:
            raw = inputs["input"].get("value")
            if isinstance(raw, str):
                value = raw.lower() in ("true", "1", "yes", "on")
            else:
                value = bool(raw)

        return {"value": {"type": "boolean", "value": value}}
