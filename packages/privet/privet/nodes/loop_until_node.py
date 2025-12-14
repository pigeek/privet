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

class LoopUntilSchema(NodeSchema):
    NODE_TYPE = 'loopUntil'
    TITLE = 'Loop Until'
    DISPLAY_NAME = 'Loop Until'
    VISUAL_WIDTH = 225
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'Loop Until Node'
    UI_INFOBOX_BODY = 'Executes a subgraph repeatedly until a condition is met. Outputs the final graph outputs, iteration count, and completion flag.'
    UI_CONTEXT_MENU_TITLE = 'Loop Until'
    DATA = {'targetGraph': None, 'useTargetGraphInput': False, 'conditionType': 'allOutputsSet', 'maxIterations': None, 'useMaxIterationsInput': False, 'inputToCheck': None, 'useInputToCheckInput': False, 'targetValue': None, 'useTargetValueInput': False}
    EDITORS = [{'type': 'graphSelector', 'label': 'Target Graph', 'dataKey': 'targetGraph'}, {'type': 'dropdown', 'label': 'Stop Condition', 'dataKey': 'conditionType', 'options': [{'label': 'All Outputs Set', 'value': 'allOutputsSet'}, {'label': 'Input Equals Value', 'value': 'inputEqual'}]}, {'type': 'number', 'label': 'Max Iterations', 'dataKey': 'maxIterations', 'allowEmpty': True}, {'type': 'string', 'label': 'Input to Check', 'dataKey': 'inputToCheck', 'showIf': {'dataKey': 'conditionType', 'equals': 'inputEqual'}}, {'type': 'string', 'label': 'Target Value', 'dataKey': 'targetValue', 'showIf': {'dataKey': 'conditionType', 'equals': 'inputEqual'}}]
    BODY = "{{#if targetGraph}}{{targetGraph}}{{#else}}(No target graph){{/if}}\nCondition: {{#if (conditionType == 'inputEqual')}}{{inputToCheck}} == {{targetValue}}{{#else}}All outputs set{{/if}}"

    INPUTS = [
        Input(
            id='targetGraph',
            data_type='string',
            title='Target Graph',
            show_if=Eq(data_key='useTargetGraphInput', equals=True),
        ),
        Input(
            id='maxIterations',
            data_type='number',
            title='Max Iterations',
            show_if=Eq(data_key='useMaxIterationsInput', equals=True),
        ),
        Input(
            id='inputToCheck',
            data_type='string',
            title='Input To Check',
            show_if=All(conditions=[Eq(data_key='useInputToCheckInput', equals=True), Eq(data_key='conditionType', equals='inputEqual')]),
        ),
        Input(
            id='targetValue',
            data_type='string',
            title='Target Value',
            show_if=All(conditions=[Eq(data_key='useTargetValueInput', equals=True), Eq(data_key='conditionType', equals='inputEqual')]),
        ),
    ]

    OUTPUTS = [
        Output(
            id='iteration',
            data_type='number',
            title='Iterations',
        ),
        Output(
            id='completed',
            data_type='boolean',
            title='Completed',
        ),
        Output(
            id='_subgraphOutputs',
            data_type='any',
            title='{{id}}',
            variadic={'type': 'subgraph', 'graphIdDataKey': 'targetGraph'},
        ),
    ]



@bindschema(schema=LoopUntilSchema)
class LoopUntilNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        project = (self.context or {}).get("project")
        create_subprocessor = (self.context or {}).get("create_subprocessor")
        context_values = (self.context or {}).get("context_values") or {}
        shared_globals = (self.context or {}).get("globals")

        if not project or not create_subprocessor:
            raise ValueError("LoopUntil requires project and subprocessor creator in context")
        target_graph = data.get("targetGraph")
        if not target_graph:
            raise ValueError("LoopUntil requires targetGraph")

        # Seed inputs with defaults from inputData when absent
        current_inputs = {**inputs}
        for key, val in (data.get("inputData") or {}).items():
            current_inputs.setdefault(key, val)

        max_iterations = data.get("maxIterations")
        if max_iterations is None:
            max_iterations = 100  # match TS default

        def should_break(outputs: Dict[str, Any]) -> bool:
            if data.get("conditionType") == "allOutputsSet":
                present = [v for v in outputs.values() if v is not None]
                return all(not (isinstance(v, dict) and v.get("type") == "control-flow-excluded") for v in present)
            if data.get("conditionType") == "inputEqual" and data.get("inputToCheck") and data.get("targetValue") is not None:
                val = outputs.get(data["inputToCheck"])
                sval = coerce_type_optional(val, "string")
                return sval == str(data.get("targetValue"))
            return False

        last_outputs: Dict[str, Any] = {}
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            subprocessor = create_subprocessor(target_graph, shared_globals)
            last_outputs = await subprocessor.process_graph(inputs=current_inputs, context_values=context_values)
            if should_break(last_outputs):
                break
            # Use outputs as inputs for next iteration
            current_inputs = last_outputs

        completed = should_break(last_outputs)
        last_outputs["iteration"] = {"type": "number", "value": iteration}
        last_outputs["completed"] = {"type": "boolean", "value": completed}
        return last_outputs
