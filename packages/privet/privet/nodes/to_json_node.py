from __future__ import annotations

from typing import Any, Dict
import json

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

class ToJSONSchema(NodeSchema):
    NODE_TYPE = 'toJson'
    TITLE = 'To JSON'
    DISPLAY_NAME = 'To JSON'
    VISUAL_WIDTH = 175
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'To JSON Node'
    UI_INFOBOX_BODY = 'Turns the input value into its JSON equivalent (stringifies the value).'
    UI_CONTEXT_MENU_TITLE = 'To JSON'
    DATA = {'indented': True}
    EDITORS = [{'type': 'toggle', 'label': 'Indented', 'dataKey': 'indented'}]
    BODY = '{{#if indented}}Indented{{#else}}Not indented{{/if}}'

    INPUTS = [
        Input(
            id='data',
            data_type='any',
            title='Data',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='json',
            data_type='string',
            title='JSON',
        ),
    ]



@bindschema(schema=ToJSONSchema)
class ToJSONNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        value = inputs.get("data")
        raw = value.get("value") if isinstance(value, dict) else value
        try:
            json_str = json.dumps(raw, indent=2 if data.get("indented") else None)
        except Exception:
            try:
                json_str = str(raw)
            except Exception:
                json_str = ""

        return {"json": {"type": "string", "value": json_str}}
