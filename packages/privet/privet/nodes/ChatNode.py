from typing import Any, Dict

# Note: Execution is remote; the spec captures UI shape only.
SPEC: Dict[str, Any] = {
    "type": "chat",
    "title": "Chat",
    "displayName": "Chat",
    "data": {
        "model": "gpt-4o", "useModelInput": False,
        "temperature": 0.5, "useTemperatureInput": False,
        "top_p": 1, "useTopPInput": False,
        "useTopP": False, "useUseTopPInput": False,
        "maxTokens": 1024, "useMaxTokensInput": False,
        "stop": "", "useStopInput": False,
        "presencePenalty": None, "usePresencePenaltyInput": False,
        "frequencyPenalty": None, "useFrequencyPenaltyInput": False,
        "numberOfChoices": 1, "useNumberOfChoicesInput": False,
        "outputUsage": False,
        "enableFunctionUse": False,
        "parallelFunctionCalling": True,
        "toolChoice": "", "useToolChoiceInput": False,
        "toolChoiceFunction": "", "useToolChoiceFunctionInput": False,
        "responseFormat": "", "useResponseFormatInput": False,
        "responseSchemaName": "response_schema", "useResponseSchemaNameInput": False,
        "seed": None, "useSeedInput": False,
        "user": None, "useUserInput": False,
        "modalitiesIncludeText": True,
        "modalitiesIncludeAudio": False,
        "audioVoice": "", "useAudioVoiceInput": False,
        "audioFormat": "wav", "useAudioFormatInput": False,
        "usePredictedOutput": False,
    },
    "visual": {"width": 260},
    "uiData": {
        "infoBoxBody": "Chats with an LLM; supports tools and multiple modalities (UI-only spec).",
        "infoBoxTitle": "Chat Node",
        "contextMenuTitle": "Chat",
        "group": ["AI"],
    },
    "inputs": [
        # System Prompt is always available (matches legacy ChatNode behavior)
        {"id": "systemPrompt", "title": "System Prompt", "dataType": "string", "required": False, "coerced": True},
        {"id": "prompt", "title": "Prompt", "dataType": ["chat-message", "chat-message[]"], "coerced": True},
        # Back-compat: legacy port id used by older graphs
        {"id": "input", "title": "Prompt", "dataType": ["chat-message", "chat-message[]"], "coerced": True},
        {"id": "model", "title": "Model", "dataType": "string", "showIf": {"dataKey": "useModelInput", "equals": True}},
        {"id": "temperature", "title": "Temperature", "dataType": "number", "showIf": {"dataKey": "useTemperatureInput", "equals": True}},
        {"id": "top_p", "title": "Top P", "dataType": "number", "showIf": {"dataKey": "useTopPInput", "equals": True}},
        {"id": "useTopP", "title": "Use Top P", "dataType": "boolean", "showIf": {"dataKey": "useUseTopPInput", "equals": True}},
        {"id": "maxTokens", "title": "Max Tokens", "dataType": "number", "showIf": {"dataKey": "useMaxTokensInput", "equals": True}},
        {"id": "stop", "title": "Stop", "dataType": "string", "showIf": {"dataKey": "useStopInput", "equals": True}},
        {"id": "presencePenalty", "title": "Presence Penalty", "dataType": "number", "showIf": {"dataKey": "usePresencePenaltyInput", "equals": True}},
        {"id": "frequencyPenalty", "title": "Frequency Penalty", "dataType": "number", "showIf": {"dataKey": "useFrequencyPenaltyInput", "equals": True}},
        {"id": "numberOfChoices", "title": "Number Of Choices", "dataType": "number", "showIf": {"dataKey": "useNumberOfChoicesInput", "equals": True}},
        {"id": "toolChoice", "title": "Tool Choice", "dataType": "string", "showIf": {"dataKey": "useToolChoiceInput", "equals": True}},
        {"id": "toolChoiceFunction", "title": "Tool Choice Function", "dataType": "string", "showIf": {"dataKey": "useToolChoiceFunctionInput", "equals": True}},
        {"id": "responseFormat", "title": "Response Format", "dataType": "string", "showIf": {"dataKey": "useResponseFormatInput", "equals": True}},
        {"id": "responseSchemaName", "title": "Response Schema Name", "dataType": "string", "showIf": {"dataKey": "useResponseSchemaNameInput", "equals": True}},
        {"id": "seed", "title": "Seed", "dataType": "number", "showIf": {"dataKey": "useSeedInput", "equals": True}},
        {"id": "user", "title": "User", "dataType": "string", "showIf": {"dataKey": "useUserInput", "equals": True}},
        {"id": "functions", "title": "Functions", "dataType": ["gpt-function", "gpt-function[]"], "showIf": {"dataKey": "enableFunctionUse", "equals": True}},
        {"id": "predictedOutput", "title": "Predicted Output", "dataType": "string[]", "coerced": True, "showIf": {"dataKey": "usePredictedOutput", "equals": True}},
        {"id": "audioVoice", "title": "Audio Voice", "dataType": "string", "showIf": {"dataKey": "useAudioVoiceInput", "equals": True}},
        {"id": "audioFormat", "title": "Audio Format", "dataType": "string", "showIf": {"dataKey": "useAudioFormatInput", "equals": True}},
    ],
    "outputs": [
        {"id": "response", "title": "Response", "dataTypeFrom": {"dataKey": "numberOfChoices", "map": {"1": "string"}}, "dataType": ["string", "string[]"]},
        {"id": "in-messages", "title": "In Messages", "dataType": "chat-message[]"},
        {"id": "all-messages", "title": "All Messages", "dataType": "chat-message[]"},
        {"id": "function-call", "title": "Function Call", "dataType": "object", "showIf": {"all": [{"dataKey": "enableFunctionUse", "equals": True}, {"dataKey": "parallelFunctionCalling", "equals": False}]}},
        {"id": "function-calls", "title": "Function Calls", "dataType": "object[]", "showIf": {"all": [{"dataKey": "enableFunctionUse", "equals": True}, {"dataKey": "parallelFunctionCalling", "equals": True}]}},
        {"id": "usage", "title": "Usage", "dataType": "object", "showIf": {"dataKey": "outputUsage", "equals": True}},
        {"id": "responseTokens", "title": "Response Tokens", "dataType": "number"},
    ],
    "editors": [
        {"type": "dropdown", "label": "Model", "dataKey": "model", "options": [ {"label": "gpt-4o", "value": "gpt-4o"}, {"label": "gpt-4.1", "value": "gpt-4.1"} ], "useInputToggleDataKey": "useModelInput"},
        {"type": "number", "label": "Temperature", "dataKey": "temperature", "useInputToggleDataKey": "useTemperatureInput"},
        {"type": "toggle", "label": "Output Usage", "dataKey": "outputUsage"},
    ],
    "body": """
      {{#if useMaxTokensInput}}Max Tokens: (Using Input){{#else}}{{maxTokens}} tokens{{/if}}
      Model: {{#if useModelInput}}(Using Input){{#else}}{{model}}{{/if}}
      {{#if useTopP}}
      Top P: {{#if useTopPInput}}(Using Input){{#else}}{{top_p}}{{/if}}
      {{#else}}
      Temperature: {{#if useTemperatureInput}}(Using Input){{#else}}{{temperature}}{{/if}}
      {{/if}}
      {{#if useStop}}Stop: {{#if useStopInput}}(Using Input){{#else}}{{stop}}{{/if}}{{/if}}
    """.strip(),
}
