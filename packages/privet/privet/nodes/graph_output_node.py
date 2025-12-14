from __future__ import annotations

from typing import Any, Dict

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import Input, Output, NodeSchema


class GraphOutputSchema(NodeSchema):
    NODE_TYPE = "graphOutput"
    EXPORT_TO_SPEC = False  # UI owns spec; executor only
    TITLE = "Graph Output"
    DISPLAY_NAME = "Graph Output"
    VISUAL_WIDTH = 300
    UI_GROUP = ["Input/Output"]
    UI_INFOBOX_TITLE = "Graph Output Node"
    UI_INFOBOX_BODY = "Captures a value as a named output of the graph."
    UI_CONTEXT_MENU_TITLE = "Graph Output"
    DATA = {"id": "output", "dataType": "string"}
    EDITORS = [
        {"type": "string", "label": "ID", "dataKey": "id"},
        {"type": "dataTypeSelector", "label": "Data Type", "dataKey": "dataType"},
    ]
    BODY = "ID: {{id}} | Type: {{dataType}}"

    INPUTS = [
        Input(
            id="value",
            data_type="any",
            title="Value",
        )
    ]

    OUTPUTS = [
        Output(
            id="valueOutput",
            data_type="any",
            title="Value",
        )
    ]


@bindschema(schema=GraphOutputSchema)
class GraphOutputNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        graph_outputs: Dict[str, Any] = (self.context or {}).get("graph_outputs", {})

        graph_output_id = data.get("id") or "output"
        value = inputs.get("value")

        # Control-flow exclusion: preserve if first seen
        if (value or {}).get("type") == "control-flow-excluded":
            if graph_outputs.get(graph_output_id) is None:
                graph_outputs[graph_output_id] = {"type": "control-flow-excluded", "value": None}
            return {"valueOutput": {"type": "control-flow-excluded", "value": None}}

        # Only set once if not excluded
        if graph_outputs.get(graph_output_id) is None or graph_outputs.get(graph_output_id, {}).get("type") == "control-flow-excluded":
            if value is not None:
                graph_outputs[graph_output_id] = value

        return {"valueOutput": graph_outputs.get(graph_output_id)}
