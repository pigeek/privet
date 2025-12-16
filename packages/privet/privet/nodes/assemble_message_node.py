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

class AssembleMessageSchema(NodeSchema):
    NODE_TYPE = 'assembleMessage'
    TITLE = 'Assemble Message'
    DISPLAY_NAME = 'Assemble Message'
    VISUAL_WIDTH = 250
    UI_GROUP = 'AI'
    UI_INFOBOX_TITLE = 'Assemble Message Node'
    UI_INFOBOX_BODY = 'Assembles a single chat message from multiple parts (text, images, documents, URLs).'
    UI_CONTEXT_MENU_TITLE = 'Assemble Message'
    DATA = {'type': 'user', 'useTypeInput': False, 'toolCallId': '', 'useToolCallIdInput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'Type', 'dataKey': 'type', 'useInputToggleDataKey': 'useTypeInput', 'options': [{'value': 'system', 'label': 'System'}, {'value': 'user', 'label': 'User'}, {'value': 'assistant', 'label': 'Assistant'}, {'value': 'function', 'label': 'Function'}]}, {'type': 'string', 'label': 'Tool Call ID', 'dataKey': 'toolCallId', 'useInputToggleDataKey': 'useToolCallIdInput', 'showIf': {'dataKey': 'type', 'equals': 'function'}}]
    BODY = '{{#if useTypeInput}}(Type From Input){{#else}}{{type}}{{/if}}\n{{#if useToolCallIdInput}}Tool Call ID: (From Input){{#else}}{{#if toolCallId}}Tool Call ID: {{toolCallId}}{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='type',
            data_type='string',
            title='Type',
            show_if=Eq(data_key='useTypeInput', equals=True),
        ),
        Input(
            id='toolCallId',
            data_type='string',
            title='Tool Call ID',
            show_if=Eq(data_key='useToolCallIdInput', equals=True),
        ),
        VariadicInput(
            id_value='part',
            base_id='part',
            data_type=['string', 'image', 'string[]', 'image[]', 'object', 'object[]', 'document', 'document[]'],
            title='Part {n}',
            title_pattern='Part {n}',
            start_at=1,
            min=1,
        ),
    ]

    OUTPUTS = [
        Output(
            id='message',
            data_type='chat-message',
            title='Message',
        ),
    ]



@bindschema(schema=AssembleMessageSchema)
class AssembleMessageNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        from ..utils.inputs import get_input_or_data
        from ..utils.data_values import coerce_type_optional

        # Get message type from input or data
        msg_type = get_input_or_data(self.node.data, inputs, 'type', 'string', 'useTypeInput')
        if not msg_type:
            msg_type = 'user'

        # Build the message based on type
        if msg_type == 'system':
            out_message = {'type': 'system', 'message': []}
        elif msg_type == 'user':
            out_message = {'type': 'user', 'message': []}
        elif msg_type == 'assistant':
            out_message = {'type': 'assistant', 'message': [], 'function_call': None, 'function_calls': None}
        elif msg_type == 'function':
            tool_call_id = get_input_or_data(self.node.data, inputs, 'toolCallId', 'string', 'useToolCallIdInput')
            out_message = {'type': 'function', 'message': [], 'name': tool_call_id}
        else:
            raise ValueError(f"Invalid message type: {msg_type}")

        # Collect all parts (part1, part2, etc.) in order
        part_keys = sorted([k for k in (inputs or {}).keys() if k.startswith('part')],
                          key=lambda x: int(x.replace('part', '')))

        for key in part_keys:
            input_part = inputs[key]

            # Skip excluded or None values
            if not input_part or input_part.get('type') == 'control-flow-excluded' or not input_part.get('value'):
                continue

            # Handle arrays of parts
            part_value = input_part.get('value')
            part_type = input_part.get('type', '')

            # Convert to list if not already
            if part_type.endswith('[]'):
                parts_list = part_value if isinstance(part_value, list) else [part_value]
            else:
                parts_list = [part_value]

            for part in parts_list:
                if isinstance(part, str):
                    # Text part
                    out_message['message'].append(part)
                elif isinstance(part, dict):
                    if part.get('type') == 'image':
                        # Image part
                        out_message['message'].append({
                            'type': 'image',
                            'data': part.get('data'),
                            'mediaType': part.get('mediaType'),
                        })
                    elif part.get('type') == 'document':
                        # Document part
                        out_message['message'].append({
                            'type': 'document',
                            'data': part.get('data'),
                            'mediaType': part.get('mediaType'),
                            'context': part.get('context'),
                            'title': part.get('title'),
                            'enableCitations': part.get('enableCitations'),
                        })
                    elif part.get('type') == 'url_reference':
                        # URL reference
                        out_message['message'].append({
                            'type': 'url',
                            'url': part.get('url'),
                        })
                    else:
                        # Try to coerce to string
                        coerced = str(part)
                        if coerced:
                            out_message['message'].append(coerced)
                else:
                    # Coerce other types to string
                    out_message['message'].append(str(part))

        return {
            'message': {
                'type': 'chat-message',
                'value': out_message,
            }
        }
