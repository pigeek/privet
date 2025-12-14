from __future__ import annotations

import asyncio
from typing import Any, Dict

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import Input, Output, NodeSchema


class DelaySchema(NodeSchema):
    NODE_TYPE = "delayNode"
    TITLE = "Delay"
    DISPLAY_NAME = "Delay"
    PRODUCES = ["any"]
    DESCRIPTION = "Delays the output by a specified duration."

    INPUTS = [
        Input(
            id="input",
            data_type="any",
            title="Input",
        )
    ]

    OUTPUTS = [
        Output(
            id="output",
            data_type="any",
            title="Output",
        )
    ]
    DATA = {"duration": 0.1}
    EDITORS = [
        {"type": "number", "label": "Duration (seconds)", "dataKey": "duration"},
    ]


@bindschema(schema=DelaySchema)
class DelayNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        duration = self.node.data.get("duration", 0.1)
        
        # Check for abort during delay
        try:
            await asyncio.sleep(duration)
        except asyncio.CancelledError:
            # If the task is cancelled (e.g., due to abort), re-raise the exception
            raise

        return {"output": inputs.get("input")}