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

class DelegateToolCallSchema(NodeSchema):
    NODE_TYPE = 'delegateFunctionCall'
    TITLE = 'Delegate Tool Call'
    DISPLAY_NAME = 'Delegate Tool Call'
    VISUAL_WIDTH = 325
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Delegate Tool Call Node'
    UI_INFOBOX_BODY = 'Handles a tool call by delegating it to a different subgraph depending on the tool call.'
    UI_CONTEXT_MENU_TITLE = 'Delegate Tool Call'
    DATA = {'handlers': [], 'unknownHandler': None, 'autoDelegate': True, 'fallBackToExternalCall': True, 'passthroughErrors': True}
    EDITORS = [{'type': 'toggle', 'label': 'Auto Delegate', 'dataKey': 'autoDelegate'}, {'type': 'toggle', 'label': 'Fall Back To External Call', 'dataKey': 'fallBackToExternalCall', 'showIf': {'dataKey': 'autoDelegate', 'equals': True}}, {'type': 'toggle', 'label': 'Passthrough Errors', 'dataKey': 'passthroughErrors', 'showIf': {'all': [{'dataKey': 'autoDelegate', 'equals': True}, {'dataKey': 'fallBackToExternalCall', 'equals': True}]}}, {'type': 'custom', 'customEditorId': 'ToolCallHandlers', 'label': 'Handlers', 'dataKey': 'handlers', 'showIf': {'dataKey': 'autoDelegate', 'equals': False}}, {'type': 'graphSelector', 'dataKey': 'unknownHandler', 'label': 'Unknown Handler'}]
    BODY = '{{#if autoDelegate}}\n  Auto Delegate To Subgraphs{{#if fallBackToExternalCall}} (+ External Call Fallback{{#if passthroughErrors}}, Passthrough Errors{{/if}}){{/if}}\n{{#else}}\n  {{#if handlers.length}}\n    Handlers defined\n  {{#else}}\n    No handlers defined\n  {{/if}}\n{{/if}}\n'

    INPUTS = [
        Input(
            id='function-call',
            data_type='object',
            title='Tool Call',
            required=True,
            coerced=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='string',
            title='Output',
        ),
        Output(
            id='message',
            data_type='object',
            title='Message Output',
        ),
    ]



@bindschema(schema=DelegateToolCallSchema)
class DelegateToolCallNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
