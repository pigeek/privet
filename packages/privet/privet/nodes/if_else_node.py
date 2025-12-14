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
from ..utils import coerce_type_optional, unwrap_data_value

class IfElseSchema(NodeSchema):
    NODE_TYPE = 'ifElse'
    TITLE = 'If/Else'
    DISPLAY_NAME = 'If/Else'
    VISUAL_WIDTH = 175
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'If/Else Node'
    UI_INFOBOX_BODY = 'Routes either the True or False input based on the If condition.'
    UI_CONTEXT_MENU_TITLE = 'If/Else'
    DATA = {'unconnectedControlFlowExcluded': True}
    EDITORS = [{'type': 'toggle', 'label': "Don't run unconnected ports", 'dataKey': 'unconnectedControlFlowExcluded'}]

    INPUTS = [
        Input(
            id='if',
            data_type='any',
            title='If',
        ),
        Input(
            id='true',
            data_type='any',
            title='True',
        ),
        Input(
            id='false',
            data_type='any',
            title='False',
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='any',
            title='Output',
        ),
    ]



@bindschema(schema=IfElseSchema)
class IfElseNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        unconnected = (
            {"type": "control-flow-excluded", "value": None}
            if data.get("unconnectedControlFlowExcluded", True)
            else {"type": "any", "value": None}
        )

        cond = inputs.get("if")
        true_val = inputs.get("true", unconnected)
        false_val = inputs.get("false", unconnected)

        def _truthy(val: Any) -> bool:
            if val is None:
                return False
            if isinstance(val, dict):
                if val.get("type") == "control-flow-excluded":
                    return False
                ctype = val.get("type")
                cval = val.get("value")
                if ctype == "boolean":
                    return bool(cval)
                if ctype == "string":
                    return bool(cval)
                if isinstance(ctype, str) and ctype.endswith("[]"):
                    return bool(cval) and len(cval) > 0  # type: ignore[arg-type]
                if ctype in ("any", "object"):
                    return bool(cval)
                if ctype == "chat-message":
                    sval = coerce_type_optional(val, "string")
                    return bool(sval)
            return bool(unwrap_data_value(val))

        return {"output": true_val if _truthy(cond) else false_val}
