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
from ..utils import coerce_type_optional

class GraphReferenceSchema(NodeSchema):
    NODE_TYPE = 'graphReference'
    TITLE = 'Graph Reference'
    DISPLAY_NAME = 'Graph Reference'
    VISUAL_WIDTH = 275
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Graph Reference Node'
    UI_INFOBOX_BODY = 'Gets a reference to another graph, that can be used to pass around graphs to call using a Call Graph node.'
    UI_CONTEXT_MENU_TITLE = 'Graph Reference'
    DATA = {'graphId': '', 'useGraphIdOrNameInput': False}
    EDITORS = [{'type': 'graphSelector', 'label': 'Graph', 'dataKey': 'graphId', 'useInputToggleDataKey': 'useGraphIdOrNameInput'}]
    BODY = '{{#if useGraphIdOrNameInput}}(Graph from input){{#else}}{{#if graphId}}{{graphId}}{{#else}}(No graph selected){{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='graph-name-or-id',
            data_type='string',
            title='Graph Name Or ID',
            show_if=Eq(data_key='useGraphIdOrNameInput', equals=True),
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='graph',
            data_type='graph-reference',
            title='Graph',
        ),
    ]



@bindschema(schema=GraphReferenceSchema)
class GraphReferenceNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        project = (self.context or {}).get("project")

        def _build_ref(graph_id: str, graph_name: str = "") -> Dict[str, Any]:
            return {"type": "graph-reference", "value": {"graphId": graph_id, "graphName": graph_name}}

        if data.get("useGraphIdOrNameInput"):
            graph_input = coerce_type_optional(inputs.get("graph-name-or-id"), "string")
            graph_input = graph_input or ""
            graph = None
            if project:
                graph = project.graphs.get(graph_input)
                if not graph:
                    graph = next((g for g in project.graphs.values() if (g.metadata or {}).get("name") == graph_input), None)
            if not graph:
                return {"graph": {"type": "control-flow-excluded", "value": None}}
            graph_id = (graph.metadata or {}).get("id") or ""
            graph_name = (graph.metadata or {}).get("name") or ""
            return {"graph": _build_ref(graph_id, graph_name)}

        graph_id = data.get("graphId") or ""
        if project:
            graph = project.graphs.get(graph_id)
            if graph:
                graph_name = (graph.metadata or {}).get("name") or ""
                graph_id = (graph.metadata or {}).get("id") or graph_id
                return {"graph": _build_ref(graph_id, graph_name)}

        if not graph_id:
            return {"graph": {"type": "control-flow-excluded", "value": None}}
        return {"graph": _build_ref(graph_id, "")}
