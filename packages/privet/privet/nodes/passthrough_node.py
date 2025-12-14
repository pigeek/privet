from __future__ import annotations

from typing import Any, Dict

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import Input, Output, NodeSchema


class PassthroughSchema(NodeSchema):
    NODE_TYPE = "passthroughNode"
    TITLE = "Passthrough"
    DISPLAY_NAME = "Passthrough"
    PRODUCES = ["string"]
    DESCRIPTION = "Passes the input directly to the output."

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


@bindschema(schema=PassthroughSchema)
class PassthroughNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        return {"output": inputs.get("input")}