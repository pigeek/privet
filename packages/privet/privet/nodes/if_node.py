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

class IfSchema(NodeSchema):
    NODE_TYPE = 'if'
    TITLE = 'If'
    DISPLAY_NAME = 'If'
    VISUAL_WIDTH = 125
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'If Node'
    UI_INFOBOX_BODY = 'Routes a value to True or False outputs based on a condition.'
    UI_CONTEXT_MENU_TITLE = 'If'
    DATA = {'unconnectedControlFlowExcluded': True}
    EDITORS = [{'type': 'toggle', 'label': "Don't run unconnected value", 'dataKey': 'unconnectedControlFlowExcluded'}]

    INPUTS = [
        Input(
            id='if',
            data_type='any',
            title='If',
            description='Condition to test',
        ),
        Input(
            id='value',
            data_type='any',
            title='Value',
            description='Value to pass through',
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='any',
            title='True',
        ),
        Output(
            id='falseOutput',
            data_type='any',
            title='False',
        ),
    ]



@bindschema(schema=IfSchema)
class IfNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        unconnected = (
            {"type": "control-flow-excluded", "value": None}
            if data.get("unconnectedControlFlowExcluded", True)
            else {"type": "any", "value": None}
        )

        condition = inputs.get("if")
        value = inputs.get("value", unconnected)

        def _is_falsey(cond: Any) -> bool:
            if cond is None:
                return True
            if isinstance(cond, dict):
                if cond.get("type") == "control-flow-excluded":
                    return True
                ctype = cond.get("type")
                cval = cond.get("value")
                if ctype == "string":
                    return not bool(cval)
                if ctype == "boolean":
                    return not bool(cval)
                if isinstance(ctype, str) and ctype.endswith("[]"):
                    return not bool(cval)
                if ctype in ("object", "any"):
                    return not bool(cval)
                if ctype == "chat-message":
                    sval = coerce_type_optional(cond, "string")
                    return not bool(sval)
            return not bool(unwrap_data_value(cond))

        if _is_falsey(condition):
            return {
                "output": {"type": "control-flow-excluded", "value": None},
                "falseOutput": value,
            }

        return {
            "output": value,
            "falseOutput": {"type": "control-flow-excluded", "value": None},
        }
