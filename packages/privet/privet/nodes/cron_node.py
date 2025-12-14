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

class CronSchema(NodeSchema):
    NODE_TYPE = 'cron'
    TITLE = 'Cron'
    DISPLAY_NAME = 'Cron'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Cron Node'
    UI_INFOBOX_BODY = 'Executes a subgraph on a schedule (cron or interval).'
    UI_CONTEXT_MENU_TITLE = 'Cron'
    DATA = {'targetGraph': None, 'scheduleType': 'interval', 'schedule': '5 minutes', 'executeImmediately': True, 'useTargetGraphInput': False}
    EDITORS = [{'type': 'toggle', 'dataKey': 'executeImmediately', 'label': 'Execute Immediately'}, {'type': 'graphSelector', 'dataKey': 'targetGraph', 'useInputToggleDataKey': 'useTargetGraphInput', 'label': 'Target Graph'}, {'type': 'dropdown', 'dataKey': 'scheduleType', 'label': 'Schedule Type', 'options': [{'label': 'Cron Expression', 'value': 'cron'}, {'label': 'Simple Interval', 'value': 'interval'}]}, {'type': 'string', 'dataKey': 'schedule', 'label': 'Schedule'}]

    INPUTS = [
        Input(
            id='trigger',
            data_type='boolean',
            title='Trigger',
        ),
        Input(
            id='targetGraph',
            data_type='string',
            title='Target Graph',
            show_if=Eq(data_key='useTargetGraphInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='any',
            title='Last Output',
        ),
        Output(
            id='iteration',
            data_type='number',
            title='Iteration',
        ),
        Output(
            id='completed',
            data_type='boolean',
            title='Completed',
        ),
        Output(
            id='nextRun',
            data_type='string',
            title='Next Run',
        ),
    ]



@bindschema(schema=CronSchema)
class CronNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
