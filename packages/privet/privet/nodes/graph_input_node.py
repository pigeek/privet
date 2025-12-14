from __future__ import annotations

from typing import Any, Dict

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import Input, Output, Eq, NodeSchema
from ..utils import coerce_type_optional, get_default_value, infer_type, is_array_data_type


class GraphInputSchema(NodeSchema):
    NODE_TYPE = "graphInput"
    EXPORT_TO_SPEC = False  # UI owns spec; executor only
    TITLE = "Graph Input"
    DISPLAY_NAME = "Graph Input"
    VISUAL_WIDTH = 300
    UI_GROUP = ["Input/Output"]
    UI_INFOBOX_TITLE = "Graph Input Node"
    UI_INFOBOX_BODY = (
        "Defines an input for the graph. The value passed into this node becomes available to downstream nodes."
    )
    UI_CONTEXT_MENU_TITLE = "Graph Input"
    DATA = {"id": "input", "dataType": "string", "defaultValue": None, "useDefaultValueInput": False}
    EDITORS = [
        {"type": "string", "label": "ID", "dataKey": "id"},
        {"type": "dataTypeSelector", "label": "Data Type", "dataKey": "dataType"},
        {"type": "anyData", "label": "Default Value", "dataKey": "defaultValue", "useInputToggleDataKey": "useDefaultValueInput"},
    ]
    BODY = "ID: {{id}} | Type: {{dataType}}"

    INPUTS = [
        Input(
            id="default",
            data_type="any",
            title="Default Value",
            show_if=Eq(data_key="useDefaultValueInput", equals=True),
        )
    ]

    OUTPUTS = [
        Output(
            id="data",
            data_type="any",
            title="Value",
        )
    ]


@bindschema(schema=GraphInputSchema)
class GraphInputNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        graph_inputs: Dict[str, Any] = (self.context or {}).get("graph_inputs", {})
        graph_input_values: Dict[str, Any] = (self.context or {}).get("graph_input_node_values", {})

        data_type = data.get("dataType") or "any"
        graph_id = data.get("id") or "input"

        # Prefer runtime graph input
        input_value = coerce_type_optional(graph_inputs.get(graph_id), data_type)

        # Fallback to default input port
        if input_value is None and data.get("useDefaultValueInput"):
            input_value = coerce_type_optional(inputs.get("default"), data_type)

        # Fallback to node's stored default
        if input_value is None:
            inferred = infer_type(data.get("defaultValue"))
            input_value = coerce_type_optional(inferred, data_type)

        if input_value is None:
            input_value = get_default_value(data_type)

        if input_value is None and is_array_data_type(data_type):
            input_value = []

        value = {"type": data_type, "value": input_value}

        graph_input_values[graph_id] = value
        return {"data": value}
