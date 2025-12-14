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

        settings = (self.context or {}).get("settings") or {}
        endpoint = data.get("endpoint") or get_input_or_data(data, inputs, "endpoint", "string") or "https://api.openai.com/v1/chat/completions"
        api_key = settings.get("openAiKey") or os.getenv("OPENAI_API_KEY")
        if api_key is None:
            api_key = ""
        if not isinstance(api_key, str):
            api_key = ""
        try:
            def _append_log(message: str) -> None:
                try:
                    with open("/tmp/privet_run.log", "a") as f:
                        f.write(message + "\n")
                except Exception:
                    pass

            key_repr: str
            if isinstance(api_key, str) and api_key:
                key_repr = f"len={len(api_key)} prefix={api_key[:4]} suffix={api_key[-4:]}"
            else:
                key_repr = f"type={type(api_key).__name__} truthy={bool(api_key)}"
            msg = f"[ChatNode] endpoint={endpoint} api_key_info={key_repr}"
            print(msg)
            _append_log(msg)
        except Exception:
            pass

        # Build messages
        system_prompt = coerce_type_optional(inputs.get("systemPrompt"), "string")
        prompt_messages = coerce_type_optional(inputs.get("prompt"), "chat-message[]") or []
        if not isinstance(prompt_messages, list) and prompt_messages is not None:
            prompt_messages = [prompt_messages]

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        for m in prompt_messages:
            if not isinstance(m, dict):
                continue
            role = m.get("type") or "user"
            content = m.get("message") or ""
            name = m.get("name")
            msg = {"role": role, "content": content}
            if name:
                msg["name"] = name
            if m.get("function_call"):
                msg["function_call"] = m["function_call"]
            messages.append(msg)

        # Model and params
        model = get_input_or_data(data, inputs, "model", "string") or data.get("model") or "gpt-4o"
        # Map legacy/expired model ids to current defaults so old projects still run.
        effective_model = data.get("overrideModel") or model
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
        number_of_choices = int(get_input_or_data(data, inputs, "numberOfChoices", "number") or data.get("numberOfChoices") or 1)

        functions = inputs.get("functions") if data.get("enableFunctionUse") else None
        tool_choice = get_input_or_data(data, inputs, "toolChoice", "string") if data.get("useToolChoiceInput") else data.get("toolChoice")
        tool_choice_fn = get_input_or_data(data, inputs, "toolChoiceFunction", "string") if data.get("useToolChoiceFunctionInput") else data.get("toolChoiceFunction")

        headers = {"Authorization": f"Bearer {api_key or ''}", "Content-Type": "application/json"}
        if data.get("headers"):
            for kv in data["headers"]:
                k = kv.get("key")
                v = kv.get("value")
                if k:
                    headers[k] = v
        try:
            header_msg = f"[ChatNode] Headers keys={list(headers.keys())} has_auth={bool(headers.get('Authorization'))} auth_len={len(headers.get('Authorization') or '')}"
            print(header_msg)
            _append_log(header_msg)
        except Exception:
            pass

        payload: Dict[str, Any] = {
            "model": effective_model,
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

        # Tools/functions
        if data.get("enableFunctionUse") and functions:
            funcs = functions if isinstance(functions, list) else [functions]
            tools = []
            for fn in funcs:
                if isinstance(fn, dict):
                    tools.append({"type": "function", "function": fn})
            if tools:
                payload["tools"] = tools
                if tool_choice:
                    if tool_choice == "function" and tool_choice_fn:
                        payload["tool_choice"] = {"type": "function", "function": {"name": tool_choice_fn}}
                    else:
                        payload["tool_choice"] = tool_choice

        # Response format
        resp_format = get_input_or_data(data, inputs, "responseFormat", "string") if data.get("useResponseFormatInput") else data.get("responseFormat")
        if resp_format == "json":
            payload["response_format"] = {"type": "json_object"}
        elif resp_format == "json_schema":
            schema_name = get_input_or_data(data, inputs, "responseSchemaName", "string") if data.get("useResponseSchemaNameInput") else data.get("responseSchemaName")
            if schema_name:
                payload["response_format"] = {"type": "json_schema", "json_schema": {"name": schema_name, "schema": {}, "strict": True}}

        # Audio modalities
        if data.get("modalitiesIncludeAudio"):
            payload["modalities"] = ["text", "audio"] if data.get("modalitiesIncludeText", True) else ["audio"]
            if data.get("audioVoice"):
                payload.setdefault("audio", {})["voice"] = data.get("audioVoice")
            if data.get("audioFormat"):
                payload.setdefault("audio", {})["format"] = data.get("audioFormat")

        # Additional parameters passthrough (key/value pairs)
        if data.get("additionalParameters"):
            for kv in data["additionalParameters"]:
                k = kv.get("key")
                v = kv.get("value")
                if k:
                    payload[k] = v

        resp = await asyncio.to_thread(requests.post, endpoint, headers=headers, data=json.dumps(payload))
        if resp.status_code >= 300:
            title = getattr(self.node, "title", None) or getattr(self.node, "id", "unknown")
            raise RuntimeError(f"Chat API error {resp.status_code} (model={effective_model}, node={title}): {resp.text}")
        body = resp.json()
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
            assistant_msg["function_call"] = func_calls[0] if func_calls else None
            assistant_msg["function_calls"] = func_calls

        in_messages = prompt_messages if isinstance(prompt_messages, list) else []
        all_messages = list(in_messages) + [assistant_msg]

        usage = body.get("usage") or {}
        outputs: Dict[str, Any] = {
            "response": {"type": "string" if number_of_choices == 1 else "string[]", "value": responses[0] if number_of_choices == 1 and responses else (responses or "")},
            "in-messages": {"type": "chat-message[]", "value": in_messages},
            "all-messages": {"type": "chat-message[]", "value": all_messages},
            "responseTokens": {"type": "number", "value": usage.get("completion_tokens", 0)},
        }

        if data.get("outputUsage"):
            outputs["usage"] = {"type": "object", "value": usage}

        if data.get("enableFunctionUse"):
            if data.get("parallelFunctionCalling", True):
                outputs["function-calls"] = {"type": "object[]", "value": func_calls}
            else:
                outputs["function-call"] = {"type": "object", "value": func_calls[0] if func_calls else None}

        return outputs
