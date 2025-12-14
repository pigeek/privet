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

class ChatLoopSchema(NodeSchema):
    NODE_TYPE = 'chatLoop'
    TITLE = 'Chat Loop'
    DISPLAY_NAME = 'Chat Loop'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Convenience']
    UI_INFOBOX_TITLE = 'Chat Loop Node'
    UI_INFOBOX_BODY = 'Creates an interactive chat loop with an AI model. Outputs the conversation and last message.'
    UI_CONTEXT_MENU_TITLE = 'Chat Loop'
    DATA = {'userPrompt': 'Your response:', 'renderingFormat': 'markdown'}
    EDITORS = [{'type': 'dropdown', 'label': 'GPT Model', 'dataKey': 'model', 'useInputToggleDataKey': 'useModelInput', 'options': [{'label': 'gpt-4o', 'value': 'gpt-4o'}, {'label': 'gpt-4.1', 'value': 'gpt-4.1'}]}, {'type': 'number', 'label': 'Temperature', 'dataKey': 'temperature', 'useInputToggleDataKey': 'useTemperatureInput'}, {'type': 'number', 'label': 'Top P', 'dataKey': 'top_p', 'useInputToggleDataKey': 'useTopPInput'}, {'type': 'toggle', 'label': 'Use Top P', 'dataKey': 'useTopP', 'useInputToggleDataKey': 'useUseTopPInput'}, {'type': 'number', 'label': 'Max Tokens', 'dataKey': 'maxTokens', 'useInputToggleDataKey': 'useMaxTokensInput'}, {'type': 'string', 'label': 'Stop', 'dataKey': 'stop', 'useInputToggleDataKey': 'useStopInput'}, {'type': 'number', 'label': 'Presence Penalty', 'dataKey': 'presencePenalty', 'useInputToggleDataKey': 'usePresencePenaltyInput'}, {'type': 'number', 'label': 'Frequency Penalty', 'dataKey': 'frequencyPenalty', 'useInputToggleDataKey': 'useFrequencyPenaltyInput'}, {'type': 'number', 'label': 'Number of Choices', 'dataKey': 'numberOfChoices', 'useInputToggleDataKey': 'useNumberOfChoicesInput'}, {'type': 'toggle', 'label': 'Enable Function Use', 'dataKey': 'enableFunctionUse'}, {'type': 'dropdown', 'label': 'Response Format', 'dataKey': 'responseFormat', 'useInputToggleDataKey': 'useResponseFormatInput', 'options': [{'label': 'Text', 'value': 'text'}, {'label': 'JSON', 'value': 'json'}, {'label': 'JSON Schema', 'value': 'json_schema'}]}, {'type': 'string', 'label': 'Response Schema Name', 'dataKey': 'responseSchemaName', 'useInputToggleDataKey': 'useResponseSchemaNameInput', 'showIf': {'dataKey': 'responseFormat', 'equals': 'json_schema'}}, {'type': 'dropdown', 'label': 'System Prompt Mode', 'dataKey': 'systemPromptMode', 'options': [{'value': '', 'label': 'Auto'}, {'value': 'developer', 'label': 'Developer Mode'}, {'value': 'system', 'label': 'System Mode'}]}, {'type': 'dropdown', 'label': 'Reasoning Mode', 'dataKey': 'reasoningMode', 'options': [{'value': '', 'label': 'Auto'}, {'value': 'non-reasoning', 'label': 'Non-Reasoning Mode'}, {'value': 'reasoning', 'label': 'Reasoning Mode'}]}, {'type': 'dropdown', 'label': 'Reasoning Effort', 'dataKey': 'reasoningEffort', 'useInputToggleDataKey': 'useReasoningEffortInput', 'options': [{'value': '', 'label': 'Unset'}, {'value': 'low', 'label': 'Low'}, {'value': 'medium', 'label': 'Medium'}, {'value': 'high', 'label': 'High'}]}, {'type': 'string', 'label': 'User', 'dataKey': 'user', 'useInputToggleDataKey': 'useUserInput'}, {'type': 'number', 'label': 'Seed', 'dataKey': 'seed', 'useInputToggleDataKey': 'useSeedInput'}, {'type': 'string', 'label': 'Endpoint', 'dataKey': 'endpoint', 'useInputToggleDataKey': 'useEndpointInput'}, {'type': 'string', 'label': 'Custom Model', 'dataKey': 'overrideModel'}, {'type': 'number', 'label': 'Custom Max Tokens', 'dataKey': 'overrideMaxTokens', 'allowEmpty': True}, {'type': 'keyValuePair', 'label': 'Headers', 'dataKey': 'headers', 'useInputToggleDataKey': 'useHeadersInput'}, {'type': 'keyValuePair', 'label': 'Additional Parameters', 'dataKey': 'additionalParameters', 'useInputToggleDataKey': 'useAdditionalParametersInput'}, {'type': 'toggle', 'label': 'Cache In Rivet', 'dataKey': 'cache'}, {'type': 'toggle', 'label': 'Use for subgraph partial output', 'dataKey': 'useAsGraphPartialOutput'}, {'type': 'toggle', 'label': 'Enable Predicted Output', 'dataKey': 'usePredictedOutput'}, {'type': 'toggle', 'label': 'Use Server Token Calculation', 'dataKey': 'useServerTokenCalculation'}, {'type': 'toggle', 'label': 'Output Usage Statistics', 'dataKey': 'outputUsage'}, {'type': 'toggle', 'label': 'Modalities: Text', 'dataKey': 'modalitiesIncludeText'}, {'type': 'toggle', 'label': 'Modalities: Audio', 'dataKey': 'modalitiesIncludeAudio'}, {'type': 'code', 'label': 'User Prompt', 'dataKey': 'userPrompt', 'language': 'plain-text'}, {'type': 'group', 'label': 'Rendering', 'editors': [{'type': 'dropdown', 'dataKey': 'renderingFormat', 'label': 'Format', 'options': [{'label': 'Text', 'value': 'text'}, {'label': 'Markdown', 'value': 'markdown'}], 'defaultValue': 'markdown'}]}]

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
        ),
    ]

    OUTPUTS = [
        Output(
            id='conversation',
            data_type='string[]',
            title='Full Conversation',
        ),
        Output(
            id='lastMessage',
            data_type='string',
            title='Last Message',
        ),
    ]



@bindschema(schema=ChatLoopSchema)
class ChatLoopNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
