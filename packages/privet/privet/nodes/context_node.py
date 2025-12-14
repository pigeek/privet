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

class ContextSchema(NodeSchema):
    NODE_TYPE = 'context'
    TITLE = 'Context'
    DISPLAY_NAME = 'Context'
    VISUAL_WIDTH = 300
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Context Node'
    UI_INFOBOX_BODY = 'Retrieves a value from the graph context using an id.'
    UI_CONTEXT_MENU_TITLE = 'Context'
    DATA = {'id': 'input', 'dataType': 'string', 'defaultValue': None, 'useDefaultValueInput': False}
    EDITORS = [{'type': 'string', 'label': 'ID', 'dataKey': 'id'}, {'type': 'dataTypeSelector', 'label': 'Data Type', 'dataKey': 'dataType'}, {'type': 'anyData', 'label': 'Default Value', 'dataKey': 'defaultValue', 'useInputToggleDataKey': 'useDefaultValueInput'}]
    BODY = '{{id}}\nType: {{dataType}}'

    INPUTS = [
        Input(
            id='default',
            data_type='any',
            title='Default Value',
            show_if=Eq(data_key='useDefaultValueInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='data',
            data_type=['any', 'string', 'number', 'boolean', 'object', 'chat-message', 'vector', 'image', 'binary', 'audio', 'document'],
            title='{{id}}',
            data_type_from={'dataKey': 'dataType'},
            extra={'titleTemplate': '{{id}}'},
        ),
    ]



@bindschema(schema=ContextSchema)
class ContextNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        context_values: Dict[str, Any] = (self.context or {}).get("context_values", {})

        key = data.get("id") or "input"
        ctx_val = context_values.get(key)
        if ctx_val is not None:
            return {"data": ctx_val}

        if data.get("useDefaultValueInput"):
            default_val = inputs.get("default")
        else:
            default_val = {"type": data.get("dataType") or "any", "value": data.get("defaultValue")}

        return {"data": default_val}
