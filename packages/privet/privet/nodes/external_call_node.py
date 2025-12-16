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

class ExternalCallSchema(NodeSchema):
    NODE_TYPE = 'externalCall'
    TITLE = 'External Call'
    DISPLAY_NAME = 'External Call'
    VISUAL_WIDTH = 150
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'External Call Node'
    UI_INFOBOX_BODY = 'Calls a host-provided function from the graph.'
    UI_CONTEXT_MENU_TITLE = 'External Call'
    DATA = {'functionName': '', 'useFunctionNameInput': False, 'useErrorOutput': False}
    EDITORS = [{'type': 'string', 'label': 'Function Name', 'dataKey': 'functionName', 'useInputToggleDataKey': 'useFunctionNameInput'}, {'type': 'toggle', 'label': 'Use Error Output', 'dataKey': 'useErrorOutput'}]
    BODY = '{{#if useFunctionNameInput}}(Using Input){{#else}}{{functionName}}{{/if}}'

    INPUTS = [
        Input(
            id='functionName',
            data_type='string',
            title='Function Name',
            show_if=Eq(data_key='useFunctionNameInput', equals=True),
        ),
        Input(
            id='arguments',
            data_type='any[]',
            title='Arguments',
        ),
    ]

    OUTPUTS = [
        Output(
            id='result',
            data_type='any',
            title='Result',
        ),
        Output(
            id='error',
            data_type='string',
            title='Error',
            show_if=Eq(data_key='useErrorOutput', equals=True),
        ),
    ]



@bindschema(schema=ExternalCallSchema)
class ExternalCallNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        func_name = inputs.get("functionName") if data.get("useFunctionNameInput") else data.get("functionName")
        if isinstance(func_name, dict):
            func_name = func_name.get("value")

        args_val = inputs.get("arguments")
        args = args_val.get("value") if isinstance(args_val, dict) else args_val
        if not isinstance(args, list):
            args = []

        result = {"type": "any", "value": {"function": func_name, "args": args}}
        outputs = {"result": result}
        if data.get("useErrorOutput"):
            outputs["error"] = {"type": "control-flow-excluded", "value": None}
        return outputs
