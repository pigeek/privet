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
from ..utils import coerce_type_optional, get_input_or_data, unwrap_data_value
import re

class PromptSchema(NodeSchema):
    NODE_TYPE = 'prompt'
    TITLE = 'Prompt'
    DISPLAY_NAME = 'Prompt'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'Prompt Node'
    UI_INFOBOX_BODY = 'Outputs a chat message (system/user/assistant/function) with interpolation like Text.'
    UI_CONTEXT_MENU_TITLE = 'Prompt'
    DATA = {'type': 'user', 'useTypeInput': False, 'promptText': '{{input}}', 'enableFunctionCall': False, 'computeTokenCount': False, 'isCacheBreakpoint': False, 'useIsCacheBreakpointInput': False, 'name': None, 'useNameInput': False}
    EDITORS = [{'type': 'custom', 'customEditorId': 'PromptNodeAiAssist', 'label': 'Generate Using AI'}, {'type': 'dropdown', 'label': 'Type', 'dataKey': 'type', 'useInputToggleDataKey': 'useTypeInput', 'options': [{'value': 'system', 'label': 'System'}, {'value': 'user', 'label': 'User'}, {'value': 'assistant', 'label': 'Assistant'}, {'value': 'function', 'label': 'Function'}]}, {'type': 'string', 'label': 'Name', 'dataKey': 'name', 'useInputToggleDataKey': 'useNameInput', 'showIf': {'dataKey': 'type', 'equals': 'function'}}, {'type': 'toggle', 'label': 'Enable Function Call', 'dataKey': 'enableFunctionCall', 'showIf': {'dataKey': 'type', 'equals': 'assistant'}}, {'type': 'toggle', 'label': 'Compute Token Count', 'dataKey': 'computeTokenCount'}, {'type': 'toggle', 'label': 'Is Cache Breakpoint', 'dataKey': 'isCacheBreakpoint', 'useInputToggleDataKey': 'useIsCacheBreakpointInput'}, {'type': 'code', 'label': 'Prompt Text', 'dataKey': 'promptText', 'language': 'prompt-interpolation-markdown', 'theme': 'prompt-interpolation'}]
    BODY = [{'type': 'markdown', 'text': '_{{type}}{{#if name}} ({{name}}){{/if}}{{#if isCacheBreakpoint}} (Cache Breakpoint){{/if}}_'}, {'type': 'colorized', 'text': '{{promptText}}', 'language': 'prompt-interpolation-markdown', 'theme': 'prompt-interpolation'}]

    INPUTS = [
        Input(
            id='function-call',
            data_type='object',
            title='Function Call',
            show_if=All(conditions=[Eq(data_key='enableFunctionCall', equals=True), Eq(data_key='type', equals='assistant')]),
        ),
        Input(
            id='type',
            data_type='string',
            title='Type',
            show_if=Eq(data_key='useTypeInput', equals=True),
        ),
        Input(
            id='name',
            data_type='string',
            title='Name/ID',
            show_if=Eq(data_key='useNameInput', equals=True),
        ),
        Input(
            id='isCacheBreakpoint',
            data_type='boolean',
            title='Is Cache Breakpoint',
            show_if=Eq(data_key='useIsCacheBreakpointInput', equals=True),
        ),
        VariadicInput(
            base_id='',
            id_value='input',
            data_type='string',
            title='Input {key}',
            title_pattern='{key}',
            start_at=0,
            min=0,
            variadic_extra={
                "type": "interpolation",
                "dataKey": "promptText",
                "baseId": "",
                "titlePattern": "{key}",
                "ignorePrefixes": ["@graphInputs.", "@context."],
            },
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='chat-message',
            title='Output',
        ),
        Output(
            id='tokenCount',
            data_type='number',
            title='Token Count',
            show_if=Eq(data_key='computeTokenCount', equals=True),
        ),
    ]



@bindschema(schema=PromptSchema)
class PromptNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        # Build string map from inputs
        str_inputs: Dict[str, str] = {}
        for key, val in inputs.items():
            coerced = coerce_type_optional(val, "string")
            str_inputs[key] = coerced if coerced is not None else ""

        graph_inputs = (self.context or {}).get("graph_input_node_values", {})
        context_values = (self.context or {}).get("context_values", {})

        def _resolve_key(key: str) -> str:
            key = key.strip()
            if key.startswith("@graphInputs."):
                raw = graph_inputs.get(key[len("@graphInputs.") :])
                return str(unwrap_data_value(raw) or "")
            if key.startswith("@context."):
                raw = context_values.get(key[len("@context.") :])
                return str(unwrap_data_value(raw) or "")
            return str_inputs.get(key, "")

        prompt_text = data.get("promptText", "")

        def _replace(match: re.Match[str]) -> str:
            return str(_resolve_key(match.group(1)))

        output_text = re.sub(r"\{\{([^}]+)\}\}", _replace, prompt_text)

        msg_type = get_input_or_data(data, inputs, "type", "string")
        is_cache_breakpoint = bool(get_input_or_data(data, inputs, "isCacheBreakpoint", "boolean"))

        if msg_type not in ("assistant", "system", "user", "function"):
            raise ValueError(f"Invalid chat-message type: {msg_type}")

        message: Dict[str, Any]
        if msg_type in ("system", "user"):
            message = {"type": msg_type, "message": output_text, "isCacheBreakpoint": is_cache_breakpoint}
        elif msg_type == "assistant":
            function_call = None
            if data.get("enableFunctionCall"):
                function_call = coerce_type_optional(inputs.get("function-call"), "object")
                if function_call and (not function_call.get("name") or not function_call.get("arguments")):
                    function_call = None
                if function_call and function_call.get("arguments") is not None and not isinstance(function_call.get("arguments"), str):
                    function_call["arguments"] = str(function_call.get("arguments"))
            message = {
                "type": msg_type,
                "message": output_text,
                "function_call": function_call,
                "function_calls": [function_call] if function_call else None,
                "isCacheBreakpoint": is_cache_breakpoint,
            }
        else:  # function
            name_val = get_input_or_data(data, inputs, "name", "string")
            message = {"type": msg_type, "message": output_text, "name": name_val, "isCacheBreakpoint": is_cache_breakpoint}

        outputs: Dict[str, Any] = {"output": {"type": "chat-message", "value": message}}

        if data.get("computeTokenCount"):
            # Placeholder count: length of text; real tokenization requires tokenizer integration
            outputs["tokenCount"] = {"type": "number", "value": len(output_text.split())}

        return outputs
