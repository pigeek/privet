from __future__ import annotations

from typing import Any, Dict
from itertools import chain

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
from ..utils import unwrap_data_value, coerce_type_optional

class AssemblePromptSchema(NodeSchema):
    NODE_TYPE = 'assemblePrompt'
    TITLE = 'Assemble Prompt'
    DISPLAY_NAME = 'Assemble Prompt'
    VISUAL_WIDTH = 250
    UI_GROUP = ['AI']
    UI_INFOBOX_TITLE = 'Assemble Prompt Node'
    UI_INFOBOX_BODY = 'Assembles an array of chat messages for use with a Chat node.'
    UI_CONTEXT_MENU_TITLE = 'Assemble Prompt'
    DATA = {'computeTokenCount': False, 'isLastMessageCacheBreakpoint': False, 'useIsLastMessageCacheBreakpointInput': False}
    EDITORS = [{'type': 'toggle', 'label': 'Compute Token Count', 'dataKey': 'computeTokenCount'}, {'type': 'toggle', 'label': 'Is Last Message Cache Breakpoint', 'dataKey': 'isLastMessageCacheBreakpoint'}]
    BODY = '{{#if isLastMessageCacheBreakpoint}}Last message is cache breakpoint{{/if}}'

    INPUTS = [
        Input(
            id='isLastMessageCacheBreakpoint',
            data_type='boolean',
            title='Is Last Message Cache Breakpoint',
            show_if=Eq(data_key='useIsLastMessageCacheBreakpointInput', equals=True),
        ),
        VariadicInput(
            id_value='message',
            base_id='message',
            data_type=['chat-message', 'chat-message[]'],
            title='Message {n}',
            title_pattern='Message {n}',
            start_at=1,
            min=1,
        ),
    ]

    OUTPUTS = [
        Output(
            id='prompt',
            data_type='chat-message[]',
            title='Prompt',
        ),
        Output(
            id='tokenCount',
            data_type='number',
            title='Token Count',
            show_if=Eq(data_key='computeTokenCount', equals=True),
        ),
    ]



@bindschema(schema=AssemblePromptSchema)
class AssemblePromptNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        # Collect variadic message inputs (message1, message2, ...)
        message_items = []
        for key in sorted([k for k in inputs.keys() if str(k).startswith("message")]):
            val = inputs.get(key)
            if not val or (isinstance(val, dict) and val.get("type") == "control-flow-excluded"):
                continue
            raw = unwrap_data_value(val)
            if raw is None:
                continue
            if isinstance(raw, list):
                message_items.extend(raw)
            else:
                message_items.append(raw)

        out_messages = []
        for item in message_items:
            # Already a chat-message shape
            if isinstance(item, dict) and "type" in item and "message" in item:
                out_messages.append(item)
            else:
                # If it's a list of strings, wrap each as user chat messages
                if isinstance(item, list):
                    for s in item:
                        out_messages.append({"type": "user", "message": str(s)})
                else:
                    # Best-effort coercion of strings/objects to chat-message
                    coerced = coerce_type_optional({"type": "chat-message", "value": item}, "chat-message")
                    if isinstance(coerced, dict) and "message" in coerced:
                        out_messages.append(coerced)
                    elif isinstance(item, str):
                        out_messages.append({"type": "user", "message": item})

        # Apply cache breakpoint flag to last message if requested
        if data.get("isLastMessageCacheBreakpoint") and len(out_messages) > 0:
            out_messages[-1]["isCacheBreakpoint"] = True

        outputs: Dict[str, Any] = {
            "prompt": {"type": "chat-message[]", "value": out_messages},
        }

        # Optional token count placeholder (count messages)
        if data.get("computeTokenCount"):
            outputs["tokenCount"] = {"type": "number", "value": len(out_messages)}

        return outputs
