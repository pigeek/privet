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

class RaiseEventSchema(NodeSchema):
    NODE_TYPE = 'raiseEvent'
    TITLE = 'Raise Event'
    DISPLAY_NAME = 'Raise Event'
    VISUAL_WIDTH = 150
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Raise Event Node'
    UI_INFOBOX_BODY = "Raises an event that the host project or a 'Wait For Event' node can listen for."
    UI_CONTEXT_MENU_TITLE = 'Raise Event'
    DATA = {'eventName': 'toast', 'useEventNameInput': False}
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
            id='data',
            data_type='any',
            title='Data',
        ),
    ]

    OUTPUTS = [
        Output(
            id='result',
            data_type='any',
            title='Result',
        ),
    ]



@bindschema(schema=RaiseEventSchema)
class RaiseEventNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
