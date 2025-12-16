from __future__ import annotations

from typing import Any, Dict
import asyncio

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
import json
import os
import requests

class ChatSchema(NodeSchema):
    NODE_TYPE = 'chat'
    TITLE = 'Chat'
    DISPLAY_NAME = 'Chat'
    VISUAL_WIDTH = 260
    UI_GROUP = ['AI']
    UI_INFOBOX_TITLE = 'Chat Node'
    UI_INFOBOX_BODY = 'Chats with an LLM; supports tools and multiple modalities (UI-only spec).'
    UI_CONTEXT_MENU_TITLE = 'Chat'
    DATA = {'model': 'gpt-4o', 'useModelInput': False, 'temperature': 0.5, 'useTemperatureInput': False, 'top_p': 1, 'useTopPInput': False, 'useTopP': False, 'useUseTopPInput': False, 'maxTokens': 1024, 'useMaxTokensInput': False, 'stop': '', 'useStopInput': False, 'presencePenalty': None, 'usePresencePenaltyInput': False, 'frequencyPenalty': None, 'useFrequencyPenaltyInput': False, 'numberOfChoices': 1, 'useNumberOfChoicesInput': False, 'outputUsage': False, 'enableFunctionUse': False, 'parallelFunctionCalling': True, 'toolChoice': '', 'useToolChoiceInput': False, 'toolChoiceFunction': '', 'useToolChoiceFunctionInput': False, 'responseFormat': '', 'useResponseFormatInput': False, 'responseSchemaName': 'response_schema', 'useResponseSchemaNameInput': False, 'seed': None, 'useSeedInput': False, 'user': None, 'useUserInput': False, 'modalitiesIncludeText': True, 'modalitiesIncludeAudio': False, 'audioVoice': '', 'useAudioVoiceInput': False, 'audioFormat': 'wav', 'useAudioFormatInput': False, 'usePredictedOutput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'GPT Model', 'dataKey': 'model', 'options': [{'label': 'gpt-4o', 'value': 'gpt-4o'}, {'label': 'gpt-4.1', 'value': 'gpt-4.1'}], 'useInputToggleDataKey': 'useModelInput'}, {'type': 'number', 'label': 'Temperature', 'dataKey': 'temperature', 'useInputToggleDataKey': 'useTemperatureInput'}, {'type': 'number', 'label': 'Top P', 'dataKey': 'top_p', 'useInputToggleDataKey': 'useTopPInput'}, {'type': 'toggle', 'label': 'Use Top P', 'dataKey': 'useTopP', 'useInputToggleDataKey': 'useUseTopPInput'}, {'type': 'number', 'label': 'Max Tokens', 'dataKey': 'maxTokens', 'useInputToggleDataKey': 'useMaxTokensInput'}, {'type': 'string', 'label': 'Stop', 'dataKey': 'stop', 'useInputToggleDataKey': 'useStopInput'}, {'type': 'number', 'label': 'Presence Penalty', 'dataKey': 'presencePenalty', 'useInputToggleDataKey': 'usePresencePenaltyInput'}, {'type': 'number', 'label': 'Frequency Penalty', 'dataKey': 'frequencyPenalty', 'useInputToggleDataKey': 'useFrequencyPenaltyInput'}, {'type': 'number', 'label': 'Number of Choices', 'dataKey': 'numberOfChoices', 'useInputToggleDataKey': 'useNumberOfChoicesInput'}, {'type': 'toggle', 'label': 'Enable Function Use', 'dataKey': 'enableFunctionUse'}, {'type': 'dropdown', 'label': 'Response Format', 'dataKey': 'responseFormat', 'useInputToggleDataKey': 'useResponseFormatInput', 'options': [{'label': 'Text', 'value': 'text'}, {'label': 'JSON', 'value': 'json'}, {'label': 'JSON Schema', 'value': 'json_schema'}]}, {'type': 'string', 'label': 'Response Schema Name', 'dataKey': 'responseSchemaName', 'useInputToggleDataKey': 'useResponseSchemaNameInput', 'showIf': {'dataKey': 'responseFormat', 'equals': 'json_schema'}}, {'type': 'dropdown', 'label': 'System Prompt Mode', 'dataKey': 'systemPromptMode', 'options': [{'value': '', 'label': 'Auto'}, {'value': 'developer', 'label': 'Developer Mode'}, {'value': 'system', 'label': 'System Mode'}]}, {'type': 'dropdown', 'label': 'Reasoning Mode', 'dataKey': 'reasoningMode', 'options': [{'value': '', 'label': 'Auto'}, {'value': 'non-reasoning', 'label': 'Non-Reasoning Mode'}, {'value': 'reasoning', 'label': 'Reasoning Mode'}]}, {'type': 'dropdown', 'label': 'Reasoning Effort', 'dataKey': 'reasoningEffort', 'useInputToggleDataKey': 'useReasoningEffortInput', 'options': [{'value': '', 'label': 'Unset'}, {'value': 'low', 'label': 'Low'}, {'value': 'medium', 'label': 'Medium'}, {'value': 'high', 'label': 'High'}]}, {'type': 'string', 'label': 'User', 'dataKey': 'user', 'useInputToggleDataKey': 'useUserInput'}, {'type': 'number', 'label': 'Seed', 'dataKey': 'seed', 'useInputToggleDataKey': 'useSeedInput'}, {'type': 'string', 'label': 'Endpoint', 'dataKey': 'endpoint', 'useInputToggleDataKey': 'useEndpointInput'}, {'type': 'string', 'label': 'Custom Model', 'dataKey': 'overrideModel'}, {'type': 'number', 'label': 'Custom Max Tokens', 'dataKey': 'overrideMaxTokens', 'allowEmpty': True}, {'type': 'keyValuePair', 'label': 'Headers', 'dataKey': 'headers', 'useInputToggleDataKey': 'useHeadersInput'}, {'type': 'keyValuePair', 'label': 'Additional Parameters', 'dataKey': 'additionalParameters', 'useInputToggleDataKey': 'useAdditionalParametersInput'}, {'type': 'toggle', 'label': 'Cache In Rivet', 'dataKey': 'cache'}, {'type': 'toggle', 'label': 'Use for subgraph partial output', 'dataKey': 'useAsGraphPartialOutput'}, {'type': 'toggle', 'label': 'Enable Predicted Output', 'dataKey': 'usePredictedOutput'}, {'type': 'toggle', 'label': 'Use Server Token Calculation', 'dataKey': 'useServerTokenCalculation'}, {'type': 'toggle', 'label': 'Output Usage Statistics', 'dataKey': 'outputUsage'}, {'type': 'toggle', 'label': 'Modalities: Text', 'dataKey': 'modalitiesIncludeText'}, {'type': 'toggle', 'label': 'Modalities: Audio', 'dataKey': 'modalitiesIncludeAudio'}, {'type': 'string', 'label': 'Audio Voice', 'dataKey': 'audioVoice', 'useInputToggleDataKey': 'useAudioVoiceInput', 'showIf': {'dataKey': 'modalitiesIncludeAudio', 'equals': True}}, {'type': 'dropdown', 'label': 'Audio Format', 'dataKey': 'audioFormat', 'useInputToggleDataKey': 'useAudioFormatInput', 'options': [{'label': 'wav', 'value': 'wav'}, {'label': 'mp3', 'value': 'mp3'}, {'label': 'flac', 'value': 'flac'}, {'label': 'opus', 'value': 'opus'}, {'label': 'pcm16', 'value': 'pcm16'}], 'showIf': {'dataKey': 'modalitiesIncludeAudio', 'equals': True}}]
    BODY = '{{#if useMaxTokensInput}}Max Tokens: (Using Input){{#else}}{{maxTokens}} tokens{{/if}}\n      Model: {{#if useModelInput}}(Using Input){{#else}}{{model}}{{/if}}\n      {{#if useTopP}}\n      Top P: {{#if useTopPInput}}(Using Input){{#else}}{{top_p}}{{/if}}\n      {{#else}}\n      Temperature: {{#if useTemperatureInput}}(Using Input){{#else}}{{temperature}}{{/if}}\n      {{/if}}\n      {{#if useStop}}Stop: {{#if useStopInput}}(Using Input){{#else}}{{stop}}{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='systemPrompt',
            data_type='string',
            title='System Prompt',
            required=False,
            coerced=True,
        ),
        Input(
            id='prompt',
            data_type=['chat-message', 'chat-message[]'],
            title='Prompt',
            coerced=True,
        ),
        Input(
            id='model',
            data_type='string',
            title='Model',
            show_if=Eq(data_key='useModelInput', equals=True),
        ),
        Input(
            id='temperature',
            data_type='number',
            title='Temperature',
            show_if=Eq(data_key='useTemperatureInput', equals=True),
        ),
        Input(
            id='top_p',
            data_type='number',
            title='Top P',
            show_if=Eq(data_key='useTopPInput', equals=True),
        ),
        Input(
            id='useTopP',
            data_type='boolean',
            title='Use Top P',
            show_if=Eq(data_key='useUseTopPInput', equals=True),
        ),
        Input(
            id='maxTokens',
            data_type='number',
            title='Max Tokens',
            show_if=Eq(data_key='useMaxTokensInput', equals=True),
        ),
        Input(
            id='stop',
            data_type='string',
            title='Stop',
            show_if=Eq(data_key='useStopInput', equals=True),
        ),
        Input(
            id='presencePenalty',
            data_type='number',
            title='Presence Penalty',
            show_if=Eq(data_key='usePresencePenaltyInput', equals=True),
        ),
        Input(
            id='frequencyPenalty',
            data_type='number',
            title='Frequency Penalty',
            show_if=Eq(data_key='useFrequencyPenaltyInput', equals=True),
        ),
        Input(
            id='numberOfChoices',
            data_type='number',
            title='Number Of Choices',
            show_if=Eq(data_key='useNumberOfChoicesInput', equals=True),
        ),
        Input(
            id='toolChoice',
            data_type='string',
            title='Tool Choice',
            show_if=Eq(data_key='useToolChoiceInput', equals=True),
        ),
        Input(
            id='toolChoiceFunction',
            data_type='string',
            title='Tool Choice Function',
            show_if=Eq(data_key='useToolChoiceFunctionInput', equals=True),
        ),
        Input(
            id='responseFormat',
            data_type='string',
            title='Response Format',
            show_if=Eq(data_key='useResponseFormatInput', equals=True),
        ),
        Input(
            id='responseSchemaName',
            data_type='string',
            title='Response Schema Name',
            show_if=Eq(data_key='useResponseSchemaNameInput', equals=True),
        ),
        Input(
            id='seed',
            data_type='number',
            title='Seed',
            show_if=Eq(data_key='useSeedInput', equals=True),
        ),
        Input(
            id='user',
            data_type='string',
            title='User',
            show_if=Eq(data_key='useUserInput', equals=True),
        ),
        Input(
            id='functions',
            data_type=['gpt-function', 'gpt-function[]'],
            title='Functions',
            show_if=Eq(data_key='enableFunctionUse', equals=True),
        ),
        Input(
            id='predictedOutput',
            data_type='string[]',
            title='Predicted Output',
            show_if=Eq(data_key='usePredictedOutput', equals=True),
            coerced=True,
        ),
        Input(
            id='audioVoice',
            data_type='string',
            title='Audio Voice',
            show_if=Eq(data_key='useAudioVoiceInput', equals=True),
        ),
        Input(
            id='audioFormat',
            data_type='string',
            title='Audio Format',
            show_if=Eq(data_key='useAudioFormatInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='response',
            data_type=['string', 'string[]'],
            title='Response',
            data_type_from={'dataKey': 'numberOfChoices', 'map': {'1': 'string'}},
        ),
        Output(
            id='in-messages',
            data_type='chat-message[]',
            title='In Messages',
        ),
        Output(
            id='all-messages',
            data_type='chat-message[]',
            title='All Messages',
        ),
        Output(
            id='function-call',
            data_type='object',
            title='Function Call',
            show_if=All(conditions=[Eq(data_key='enableFunctionUse', equals=True), Eq(data_key='parallelFunctionCalling', equals=False)]),
        ),
        Output(
            id='function-calls',
            data_type='object[]',
            title='Function Calls',
            show_if=All(conditions=[Eq(data_key='enableFunctionUse', equals=True), Eq(data_key='parallelFunctionCalling', equals=True)]),
        ),
        Output(
            id='usage',
            data_type='object',
            title='Usage',
            show_if=Eq(data_key='outputUsage', equals=True),
        ),
        Output(
            id='responseTokens',
            data_type='number',
            title='Response Tokens',
        ),
    ]



@bindschema(schema=ChatSchema)
class ChatNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        # Extract endpoint and API key similar to TS implementation
        settings = (self.context or {}).get("settings") or {}
        endpoint = (
            data.get("endpoint")
            or get_input_or_data(data, inputs, "endpoint", "string")
            or "https://api.openai.com/v1/chat/completions"
        )
        api_key = settings.get("openAiKey") or os.getenv("OPENAI_API_KEY") or ""
        if not isinstance(api_key, str):
            api_key = ""

        def _listify(value: Any) -> list[Any]:
            if value is None:
                return []
            if isinstance(value, list):
                return value
            return [value]

        system_prompt = coerce_type_optional(inputs.get("systemPrompt"), "string")
        prompt_val = unwrap_data_value(inputs.get("prompt"))
        prompt_messages = _listify(prompt_val)

        normalized_inputs: list[Dict[str, Any]] = []
        messages: list[Dict[str, Any]] = []
        prompt_text_parts: list[str] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            prompt_text_parts.append(f"system:{system_prompt}")

        for raw in prompt_messages:
            msg = unwrap_data_value(raw)
            if isinstance(msg, dict):
                role = msg.get("type") or msg.get("role") or "user"
                content = msg.get("message") or msg.get("content") or ""
                name = msg.get("name")
                entry: Dict[str, Any] = {"type": role, "message": content}
                out_msg: Dict[str, Any] = {"role": role, "content": content}
                if name:
                    entry["name"] = name
                    out_msg["name"] = name
                if msg.get("function_call"):
                    entry["function_call"] = msg["function_call"]
                    out_msg["function_call"] = msg["function_call"]
                normalized_inputs.append(entry)
                messages.append(out_msg)
                prompt_text_parts.append(f"{role}:{content}")
            elif msg is not None:
                text = str(msg)
                normalized_inputs.append({"type": "user", "message": text})
                messages.append({"role": "user", "content": text})
                prompt_text_parts.append(f"user:{text}")

        model = (
            data.get("overrideModel")
            or get_input_or_data(data, inputs, "model", "string")
            or data.get("model")
            or "gpt-4o"
        )
        number_of_choices = int(get_input_or_data(data, inputs, "numberOfChoices", "number") or data.get("numberOfChoices") or 1)
        if number_of_choices < 1:
            number_of_choices = 1

        temperature = get_input_or_data(data, inputs, "temperature", "number") if data.get("useTemperatureInput") else data.get("temperature")
        top_p = get_input_or_data(data, inputs, "top_p", "number") if data.get("useTopPInput") else data.get("top_p")
        use_top_p = get_input_or_data(data, inputs, "useTopP", "boolean") if data.get("useUseTopPInput") else data.get("useTopP")
        max_tokens = get_input_or_data(data, inputs, "maxTokens", "number") if data.get("useMaxTokensInput") else data.get("maxTokens")
        if data.get("overrideMaxTokens") is not None:
            max_tokens = data.get("overrideMaxTokens")
        stop = get_input_or_data(data, inputs, "stop", "string") if data.get("useStopInput") else data.get("stop")
        presence_penalty = get_input_or_data(data, inputs, "presencePenalty", "number") if data.get("usePresencePenaltyInput") else data.get("presencePenalty")
        frequency_penalty = get_input_or_data(data, inputs, "frequencyPenalty", "number") if data.get("useFrequencyPenaltyInput") else data.get("frequencyPenalty")
        seed = get_input_or_data(data, inputs, "seed", "number") if data.get("useSeedInput") else data.get("seed")
        user = get_input_or_data(data, inputs, "user", "string") if data.get("useUserInput") else data.get("user")

        predicted_outputs = coerce_type_optional(inputs.get("predictedOutput"), "string[]") if data.get("usePredictedOutput") else None
        functions_raw = inputs.get("functions") if data.get("enableFunctionUse") else None
        tool_choice = get_input_or_data(data, inputs, "toolChoice", "string") if data.get("useToolChoiceInput") else data.get("toolChoice")
        tool_choice_fn = get_input_or_data(data, inputs, "toolChoiceFunction", "string") if data.get("useToolChoiceFunctionInput") else data.get("toolChoiceFunction")
        parallel_calls = data.get("parallelFunctionCalling", True)

        func_defs: list[Dict[str, Any]] = []
        for fn in _listify(functions_raw):
            unwrapped = unwrap_data_value(fn)
            if isinstance(unwrapped, list):
                for item in unwrapped:
                    item_unwrapped = unwrap_data_value(item)
                    if isinstance(item_unwrapped, dict):
                        func_defs.append(item_unwrapped)
            elif isinstance(unwrapped, dict):
                func_defs.append(unwrapped)

        selected_funcs: list[Dict[str, Any]] = []
        if tool_choice == "none":
            selected_funcs = []
        elif tool_choice == "function" and tool_choice_fn:
            selected_funcs = [fn for fn in func_defs if fn.get("name") == tool_choice_fn] or (func_defs[:1] if func_defs else [])
        else:
            selected_funcs = list(func_defs)

        # Build payload for real API
        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "n": number_of_choices,
        }
        if temperature is not None and not use_top_p:
            payload["temperature"] = temperature
        if top_p is not None and (use_top_p or data.get("useTopP")):
            payload["top_p"] = top_p
        if max_tokens:
            payload["max_tokens"] = int(max_tokens)
        if stop:
            payload["stop"] = stop
        if presence_penalty is not None:
            payload["presence_penalty"] = presence_penalty
        if frequency_penalty is not None:
            payload["frequency_penalty"] = frequency_penalty
        if seed is not None:
            payload["seed"] = int(seed)
        if user:
            payload["user"] = user

        if data.get("enableFunctionUse") and func_defs:
            tools = [{"type": "function", "function": fn} for fn in func_defs]
            payload["tools"] = tools
            if tool_choice:
                if tool_choice == "function" and tool_choice_fn:
                    payload["tool_choice"] = {"type": "function", "function": {"name": tool_choice_fn}}
                else:
                    payload["tool_choice"] = tool_choice

        resp_format = get_input_or_data(data, inputs, "responseFormat", "string") if data.get("useResponseFormatInput") else data.get("responseFormat")
        if resp_format == "json":
            payload["response_format"] = {"type": "json_object"}
        elif resp_format == "json_schema":
            schema_name = get_input_or_data(data, inputs, "responseSchemaName", "string") if data.get("useResponseSchemaNameInput") else data.get("responseSchemaName")
            if schema_name:
                payload["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": schema_name, "schema": {}, "strict": True},
                }

        if data.get("modalitiesIncludeAudio"):
            payload["modalities"] = ["text", "audio"] if data.get("modalitiesIncludeText", True) else ["audio"]
            if data.get("audioVoice"):
                payload.setdefault("audio", {})["voice"] = data.get("audioVoice")
            if data.get("audioFormat"):
                payload.setdefault("audio", {})["format"] = data.get("audioFormat")

        if data.get("additionalParameters"):
            for kv in data["additionalParameters"]:
                k = kv.get("key")
                v = kv.get("value")
                if k:
                    payload[k] = v

        def build_outputs_from_response(body: Dict[str, Any]) -> Dict[str, Any]:
            choices = body.get("choices") or []

            responses: list[str] = []
            func_calls: list[Any] = []
            for ch in choices:
                msg = ch.get("message") or {}
                content = msg.get("content") or ""
                responses.append(content)
                if msg.get("tool_calls"):
                    func_calls.extend(msg["tool_calls"])
                if msg.get("function_call"):
                    func_calls.append(msg["function_call"])

            assistant_msg = {
                "type": "assistant",
                "message": responses[0] if responses else "",
            }
            if func_calls:
                if parallel_calls:
                    assistant_msg["function_calls"] = func_calls
                else:
                    assistant_msg["function_call"] = func_calls[0]

            in_messages = normalized_inputs
            all_messages = list(in_messages) + [assistant_msg]

            usage = body.get("usage") or {}
            response_value: Any = responses[0] if number_of_choices == 1 else responses[:number_of_choices]
            response_type = "string" if number_of_choices == 1 else "string[]"

            outputs: Dict[str, Any] = {
                "response": {"type": response_type, "value": response_value},
                "in-messages": {"type": "chat-message[]", "value": in_messages},
                "all-messages": {"type": "chat-message[]", "value": all_messages},
                "responseTokens": {"type": "number", "value": usage.get("completion_tokens", 0)},
            }

            if data.get("outputUsage"):
                outputs["usage"] = {"type": "object", "value": usage}

            if data.get("enableFunctionUse"):
                if parallel_calls:
                    outputs["function-calls"] = {"type": "object[]", "value": func_calls}
                else:
                    outputs["function-call"] = {"type": "object", "value": func_calls[0] if func_calls else None}

            return outputs

        # If no API key is available, fall back to deterministic stub so tests/offline runs still work.
        if not api_key and endpoint.startswith("https://api.openai.com"):
            base_response_text = " | ".join(prompt_text_parts) or "ok"
            responses = predicted_outputs if predicted_outputs else [
                f"[{model}] {base_response_text}".strip() + (f" #{i+1}" if number_of_choices > 1 else "")
                for i in range(number_of_choices)
            ]
            func_calls: list[Dict[str, Any]] = []
            if data.get("enableFunctionUse") and selected_funcs:
                for idx, fn in enumerate(selected_funcs):
                    func_calls.append(
                        {
                            "id": f"{self.node.id}-tool-{idx}",
                            "type": "function",
                            "function": {"name": fn.get("name"), "arguments": fn.get("parameters") or {}},
                        }
                    )
                    if not parallel_calls:
                        break

            choices = []
            for idx, r in enumerate(responses):
                calls_for_choice = func_calls if func_calls and idx == 0 else None
                choices.append({"message": {"content": r, "tool_calls": calls_for_choice}})
            stub_body = {
                "choices": choices,
                "usage": {"completion_tokens": len(responses[0]) if responses else 0},
            }
            return build_outputs_from_response(stub_body)

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        try:
            resp = await asyncio.to_thread(requests.post, endpoint, headers=headers, data=json.dumps(payload))
        except Exception as exc:
            raise RuntimeError(f"Chat API request failed: {exc}") from exc

        if resp.status_code >= 300:
            title = getattr(self.node, "title", None) or getattr(self.node, "id", "unknown")
            raise RuntimeError(f"Chat API error {resp.status_code} (model={model}, node={title}): {resp.text}")

        body = resp.json()
        return build_outputs_from_response(body)
