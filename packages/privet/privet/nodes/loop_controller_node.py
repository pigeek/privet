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
from ..utils import coerce_type_optional

class LoopControllerSchema(NodeSchema):
    NODE_TYPE = 'loopController'
    TITLE = 'Loop Controller'
    DISPLAY_NAME = 'Loop Controller'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'Loop Controller Node'
    UI_INFOBOX_BODY = 'Defines the entry point for a loop. Values from inside the loop should be passed back through the Input ports; defaults can be set via the matching Default inputs.\n\nIf the "Continue" input is falsey, the "Break" output runs.'
    UI_CONTEXT_MENU_TITLE = 'Loop Controller'
    DATA = {'maxIterations': 100, 'atMaxIterationsAction': 'error'}
    EDITORS = [{'type': 'number', 'label': 'Max Iterations', 'dataKey': 'maxIterations', 'min': 1, 'step': 1, 'defaultValue': 100}, {'type': 'dropdown', 'label': 'At Max Iterations', 'dataKey': 'atMaxIterationsAction', 'defaultValue': 'error', 'options': [{'label': 'Break', 'value': 'break'}, {'label': 'Error', 'value': 'error'}]}]

    INPUTS = [
        Input(
            id='continue',
            data_type='any',
            title='Continue',
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
        VariadicInput(
            id_value='inputDefault',
            base_id='input',
            data_type='any',
            title='Input {n} Default',
            title_pattern='Input {n} Default',
            start_at=1,
            min=1,
            id_pattern='input{n}Default',
        ),
    ]

    OUTPUTS = [
        Output(
            id='break',
            data_type='any',
            title='Break',
        ),
        Output(
            id='iteration',
            data_type='number',
            title='Iteration',
        ),
        Output(
            id='output',
            data_type='any',
            title='Output {n}',
            variadic={'type': 'mirror', 'inputBaseId': 'input', 'baseId': 'output', 'titlePattern': 'Output {n}', 'startAt': 1, 'excludeLast': True},
        ),
    ]



@bindschema(schema=LoopControllerSchema)
class LoopControllerNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        output: Dict[str, Any] = {}

        # Count inputs
        input_count = 0
        while inputs.get(f"input{input_count + 1}") is not None or inputs.get(f"input{input_count + 1}Default") is not None:
            input_count += 1

        default_inputs = [v for k, v in inputs.items() if k.endswith("Default")]
        if any(isinstance(v, dict) and v.get("type") == "control-flow-excluded" for v in default_inputs):
            for i in range(0, input_count + 1):
                output[f"output{i}"] = {"type": "control-flow-excluded", "value": None}
            output["break"] = {"type": "control-flow-excluded", "value": None}
            return output

        attached = (self.context or {}).get("attached_data", {})
        loop_info = attached.setdefault("loopInfo", {})
        iteration_count = loop_info.get(self.node.id, 0)
        loop_info[self.node.id] = iteration_count + 1
        output["iteration"] = {"type": "number", "value": iteration_count + 1}

        max_iters = data.get("maxIterations", 100)
        if iteration_count >= max_iters and data.get("atMaxIterationsAction") != "break":
            raise ValueError(f"Loop controller exceeded max iterations of {max_iters}")

        # Determine continue value
        cont_val = inputs.get("continue")
        if cont_val is None:
            continue_value = True
        elif isinstance(cont_val, dict) and cont_val.get("type") == "control-flow-excluded":
            continue_value = False
        else:
            continue_value = bool(coerce_type_optional(cont_val, "boolean"))

        if iteration_count >= max_iters and data.get("atMaxIterationsAction") == "break":
            continue_value = False

        if continue_value:
            output["break"] = {"type": "control-flow-excluded", "value": "loop-not-broken"}
        else:
            input_values = []
            for i in range(1, input_count + 1):
                val = inputs.get(f"input{i}")
                input_values.append(val.get("value") if isinstance(val, dict) else val)
            output["break"] = {"type": "any[]", "value": input_values}

        for i in range(1, input_count + 1):
            input_id = f"input{i}"
            output_id = f"output{i}"
            if continue_value:
                if inputs.get(input_id):
                    output[output_id] = inputs[input_id]
                else:
                    output[output_id] = inputs.get(f"{input_id}Default")
            else:
                output[output_id] = {"type": "control-flow-excluded", "value": None}

        return output
