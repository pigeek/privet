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
        from ..utils.data_values import coerce_type

        inputs = inputs or {}
        data = self.node.data or {}

        if data.get("useEventNameInput"):
            event_name = coerce_type(inputs.get("eventName"), "string")
        else:
            event_name = str(data.get("eventName") or "")

        processor = (self.context or {}).get("processor")
        if not processor or not hasattr(processor, "wait_event"):
            raise RuntimeError("Processor event handling is unavailable.")

        event_data = await processor.wait_event(event_name)

        return {
            "outputData": inputs.get("inputData"),
            "eventData": event_data,
        }
