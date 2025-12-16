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

class TrimChatMessagesSchema(NodeSchema):
    NODE_TYPE = 'trimChatMessages'
    TITLE = 'Trim Chat Messages'
    DISPLAY_NAME = 'Trim Chat Messages'
    VISUAL_WIDTH = 200
    UI_GROUP = ['AI']
    UI_INFOBOX_TITLE = 'Trim Chat Messages Node'
    UI_INFOBOX_BODY = 'Slices messages from start or end until under token limit.'
    UI_CONTEXT_MENU_TITLE = 'Trim Chat Messages'
    DATA = {'maxTokenCount': 4096, 'removeFromBeginning': True, 'useMaxTokenCountInput': False, 'useRemoveFromBeginningInput': False}
    EDITORS = [{'type': 'number', 'label': 'Max Token Count', 'dataKey': 'maxTokenCount', 'useInputToggleDataKey': 'useMaxTokenCountInput'}, {'type': 'toggle', 'label': 'Remove From Beginning', 'dataKey': 'removeFromBeginning', 'useInputToggleDataKey': 'useRemoveFromBeginningInput'}]
    BODY = 'Max Token Count: {{#if useMaxTokenCountInput}}(From Input){{#else}}{{maxTokenCount}}{{/if}}\nRemove From Beginning: {{#if useRemoveFromBeginningInput}}(From Input){{#else}}{{#if removeFromBeginning}}Yes{{#else}}No{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='input',
            data_type='chat-message[]',
            title='Input',
        ),
        Input(
            id='maxTokenCount',
            data_type='number',
            title='Max Token Count',
            show_if=Eq(data_key='useMaxTokenCountInput', equals=True),
        ),
        Input(
            id='removeFromBeginning',
            data_type='boolean',
            title='Remove From Beginning',
            show_if=Eq(data_key='useRemoveFromBeginningInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='trimmed',
            data_type='chat-message[]',
            title='Trimmed',
        ),
    ]



@bindschema(schema=TrimChatMessagesSchema)
class TrimChatMessagesNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        from ..utils.data_values import coerce_type
        from ..utils.inputs import get_input_or_data

        # Get input messages
        input_messages = coerce_type(inputs.get('input'), 'chat-message[]')

        # Get parameters
        max_token_count = get_input_or_data(self.node.data, inputs, 'maxTokenCount', 'number', 'useMaxTokenCountInput')
        if max_token_count is None:
            max_token_count = 4096

        remove_from_beginning = get_input_or_data(self.node.data, inputs, 'removeFromBeginning', 'boolean', 'useRemoveFromBeginningInput')
        if remove_from_beginning is None:
            remove_from_beginning = True

        # Create a copy of messages to trim
        trimmed_messages = list(input_messages)

        # Count tokens and trim messages
        token_count = self._estimate_token_count(trimmed_messages)

        while token_count > max_token_count and len(trimmed_messages) > 0:
            if remove_from_beginning:
                trimmed_messages.pop(0)  # Remove from beginning
            else:
                trimmed_messages.pop()  # Remove from end

            token_count = self._estimate_token_count(trimmed_messages)

        return {
            'trimmed': {
                'type': 'chat-message[]',
                'value': trimmed_messages,
            }
        }

    def _estimate_token_count(self, messages: list) -> int:
        """
        Estimate token count for chat messages.
        Uses a simple character-based approximation (~4 chars per token).
        """
        total_chars = 0

        for msg in messages:
            if isinstance(msg, dict):
                # Handle message structure
                message_content = msg.get('message', [])

                if isinstance(message_content, list):
                    # Array of message parts
                    for part in message_content:
                        if isinstance(part, str):
                            total_chars += len(part)
                        elif isinstance(part, dict):
                            # Could be image, document, etc - estimate
                            total_chars += 100  # Rough estimate for non-text content
                elif isinstance(message_content, str):
                    total_chars += len(message_content)

                # Add overhead for message metadata
                total_chars += 50

        # Estimate tokens (~4 characters per token on average for GPT models)
        return total_chars // 4
