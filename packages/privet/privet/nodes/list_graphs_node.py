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

class ListGraphsSchema(NodeSchema):
    NODE_TYPE = 'listGraphs'
    TITLE = 'List Graphs'
    DISPLAY_NAME = 'List Graphs'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'List Graphs Node'
    UI_INFOBOX_BODY = 'Lists all graphs in the project.'
    UI_CONTEXT_MENU_TITLE = 'List Graphs'
    DATA = {}
    EDITORS = []

    INPUTS = [

    ]

    OUTPUTS = [
        Output(
            id='graphs',
            data_type='graph-reference[]',
            title='Graphs',
        ),
        Output(
            id='graph-names',
            data_type='string[]',
            title='Graph Names',
        ),
    ]



@bindschema(schema=ListGraphsSchema)
class ListGraphsNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        project = (self.context or {}).get("project")
        graphs = list(getattr(project, "graphs", {}).values()) if project else []

        graph_refs = []
        graph_names = []
        for graph in graphs:
            meta = getattr(graph, "metadata", {}) or {}
            graph_id = meta.get("id") if isinstance(meta, dict) else getattr(meta, "id", "")
            graph_name = meta.get("name") if isinstance(meta, dict) else getattr(meta, "name", "")
            graph_refs.append({"graphId": graph_id or "", "graphName": graph_name or ""})
            graph_names.append(graph_name or "")

        return {
            "graphs": {"type": "graph-reference[]", "value": graph_refs},
            "graph-names": {"type": "string[]", "value": graph_names},
        }
