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

class AbortGraphSchema(NodeSchema):
    NODE_TYPE = 'abortGraph'
    TITLE = 'Abort Graph'
    DISPLAY_NAME = 'Abort Graph'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'Abort Graph Node'
    UI_INFOBOX_BODY = 'Aborts graph execution (success or error).'
    UI_CONTEXT_MENU_TITLE = 'Abort Graph'
    DATA = {'successfully': True, 'errorMessage': '', 'useSuccessfullyInput': False}
    EDITORS = [{'type': 'toggle', 'label': 'Successfully Abort', 'dataKey': 'successfully', 'useInputToggleDataKey': 'useSuccessfullyInput'}, {'type': 'string', 'label': 'Error Message (if not successfully aborting)', 'dataKey': 'errorMessage'}]
    BODY = '{{#if useSuccessfullyInput}}Success depends on input{{#else}}{{#if successfully}}Successfully Abort{{#else}}{{#if errorMessage}}Error Abort: {{errorMessage}}{{#else}}Error Abort{{/if}}{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='data',
            data_type='any',
            title='Data or Error',
            description='Message to abort with.',
        ),
        Input(
            id='successfully',
            data_type='boolean',
            title='Successfully',
            show_if=Eq(data_key='useSuccessfullyInput', equals=True),
        ),
    ]

    OUTPUTS = [

    ]



@bindschema(schema=AbortGraphSchema)
class AbortGraphNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
