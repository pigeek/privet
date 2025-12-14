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
from ..utils import get_default_value, is_array_data_type

class GetGlobalSchema(NodeSchema):
    NODE_TYPE = 'getGlobal'
    TITLE = 'Get Global'
    DISPLAY_NAME = 'Get Global'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Get Global Node'
    UI_INFOBOX_BODY = 'Retrieves a global value; can be on-demand or wait for availability.'
    UI_CONTEXT_MENU_TITLE = 'Get Global'
    DATA = {'id': 'variable-name', 'dataType': 'string', 'onDemand': True, 'useIdInput': False, 'wait': False}
    EDITORS = [{'type': 'string', 'label': 'Variable ID', 'dataKey': 'id', 'useInputToggleDataKey': 'useIdInput'}, {'type': 'dataTypeSelector', 'label': 'Data Type', 'dataKey': 'dataType'}, {'type': 'toggle', 'label': 'On Demand', 'dataKey': 'onDemand'}, {'type': 'toggle', 'label': 'Wait', 'dataKey': 'wait'}]
    BODY = '{{#if useIdInput}}(ID from input){{#else}}{{id}}{{/if}}\nType: {{dataType}}\n{{#if wait}}Waits for available data{{/if}}'

    INPUTS = [
        Input(
            id='id',
            data_type='string',
            title='Variable ID',
            show_if=Eq(data_key='useIdInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='value',
            data_type=['fn<string>', 'string'],
            title='Value',
            data_type_from={'dataKey': 'onDemand', 'map': {'true': 'fn<string>', 'false': 'string'}},
        ),
        Output(
            id='variable_id_out',
            data_type='string',
            title='Variable ID',
        ),
    ]



@bindschema(schema=GetGlobalSchema)
class GetGlobalNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        globals_store: Dict[str, Any] = (self.context or {}).get("globals", {})

        data_type = data.get("dataType") or "string"
        var_id = data.get("id")
        if data.get("useIdInput") and inputs.get("id") is not None:
            var_id = inputs["id"].get("value") if isinstance(inputs["id"], dict) else inputs["id"]

        def _default_value():
            value = get_default_value(data_type)
            if value is None and is_array_data_type(data_type):
                value = []
            return {"type": data_type, "value": value}

        def _get_current():
            val = globals_store.get(var_id)
            return val if val is not None else _default_value()

        if data.get("onDemand"):
            return {
                "value": {"type": f"fn<{data_type}>", "value": lambda: _get_current().get("value")},
                "variable_id_out": {"type": "string", "value": var_id},
            }

        value = _get_current()
        return {"value": value, "variable_id_out": {"type": "string", "value": var_id}}
