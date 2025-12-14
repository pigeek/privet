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

class WaitForEventSchema(NodeSchema):
    NODE_TYPE = 'waitForEvent'
    TITLE = 'Wait For Event'
    DISPLAY_NAME = 'Wait For Event'
    VISUAL_WIDTH = 150
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Wait For Event Node'
    UI_INFOBOX_BODY = "Waits for a specific event raised by 'Raise Event' or the host."
    UI_CONTEXT_MENU_TITLE = 'Wait For Event'
    DATA = {'eventName': 'continue', 'useEventNameInput': False}
    EDITORS = [{'type': 'string', 'label': 'Event Name', 'dataKey': 'eventName', 'useInputToggleDataKey': 'useEventNameInput'}]
    BODY = '{{#if useEventNameInput}}(Using Input){{#else}}{{eventName}}{{/if}}'

    INPUTS = [
        Input(
            id='eventName',
            data_type='string',
            title='Event Name',
            show_if=Eq(data_key='useEventNameInput', equals=True),
        ),
        Input(
            id='inputData',
            data_type='any',
            title='Data',
        ),
    ]

    OUTPUTS = [
        Output(
            id='outputData',
            data_type='any',
            title='Data',
        ),
        Output(
            id='eventData',
            data_type='any',
            title='Event Data',
        ),
    ]



@bindschema(schema=WaitForEventSchema)
class WaitForEventNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
