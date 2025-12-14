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

class SetGlobalSchema(NodeSchema):
    NODE_TYPE = 'setGlobal'
    TITLE = 'Set Global'
    DISPLAY_NAME = 'Set Global'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Set Global Node'
    UI_INFOBOX_BODY = 'Sets a global value shared across graphs and subgraphs.'
    UI_CONTEXT_MENU_TITLE = 'Set Global'
    DATA = {'id': 'variable-name', 'dataType': 'string', 'useIdInput': False}
    EDITORS = [{'type': 'string', 'label': 'ID', 'dataKey': 'id', 'useInputToggleDataKey': 'useIdInput'}, {'type': 'dataTypeSelector', 'label': 'Data Type', 'dataKey': 'dataType', 'useInputToggleDataKey': 'useIdInput'}]
    BODY = '{{id}}\nType: {{dataType}}'

    INPUTS = [
        Input(
            id='value',
            data_type='any',
            title='Value',
            data_type_from={'dataKey': 'dataType'},
        ),
        Input(
            id='id',
            data_type='string',
            title='Variable ID',
            show_if=Eq(data_key='useIdInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='saved-value',
            data_type='any',
            title='Value',
            data_type_from={'dataKey': 'dataType'},
        ),
        Output(
            id='previous-value',
            data_type='any',
            title='Previous Value',
            data_type_from={'dataKey': 'dataType'},
        ),
        Output(
            id='variable_id_out',
            data_type='string',
            title='Variable ID',
        ),
    ]



@bindschema(schema=SetGlobalSchema)
class SetGlobalNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        globals_store: Dict[str, Any] = (self.context or {}).get("globals", {})
        emitter = (self.context or {}).get("emit")

        value = inputs.get("value")
        if value is None:
            return {}

        var_id = data.get("id")
        if data.get("useIdInput") and inputs.get("id") is not None:
            var_id = inputs["id"].get("value") if isinstance(inputs["id"], dict) else inputs["id"]
        if not var_id:
            raise ValueError("Missing variable ID")

        previous = globals_store.get(var_id)

        globals_store[var_id] = value
        if callable(emitter):
            try:
                await emitter("globalSet", {"id": var_id, "value": value, "processId": "sim"})
            except Exception:
                pass

        return {
            "saved-value": value,
            "previous-value": previous,
            "variable_id_out": {"type": "string", "value": var_id},
        }
