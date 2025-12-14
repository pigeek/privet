from __future__ import annotations

import time
import asyncio
from typing import Any, Dict

from ..BaseNode import BaseNode, bindschema
from ..graph.processor import GraphProcessor
from ..spec_builder import Input, Output, Eq, NodeSchema, VariadicInput
from ..utils import coerce_type_optional


class SubGraphSchema(NodeSchema):
    NODE_TYPE = "subGraph"
    EXPORT_TO_SPEC = False  # UI owns spec; executor only
    TITLE = "Subgraph"
    DISPLAY_NAME = "Subgraph"
    VISUAL_WIDTH = 300
    UI_GROUP = ["Advanced"]
    UI_INFOBOX_TITLE = "Subgraph Node"
    UI_INFOBOX_BODY = "Executes another graph. Inputs/outputs mirror the target graph's Graph Input/Output nodes."
    UI_CONTEXT_MENU_TITLE = "Subgraph"
    DATA = {"graphId": None, "useErrorOutput": False, "useAsGraphPartialOutput": False, "inputData": {}}
    EDITORS = [
        {"type": "graphSelector", "label": "Graph", "dataKey": "graphId"},
        {"type": "toggle", "label": "Use Error Output", "dataKey": "useErrorOutput"},
    ]
    BODY = "Runs graph {{graphId}}"

    INPUTS = [
        VariadicInput(
            base_id="input",
            id_value="input",
            data_type="any",
            title="Input {n}",
            title_pattern="Input {n}",
            start_at=1,
            min=0,
        ),
    ]

    OUTPUTS = [
        Output(
            id="output",
            data_type="any",
            title="Output {n}",
            variadic={"type": "dynamic", "baseId": "output", "titlePattern": "Output {n}", "startAt": 1},
        ),
        Output(id="duration", data_type="number", title="Duration (ms)"),
        Output(id="error", data_type="string", title="Error", show_if=Eq(data_key="useErrorOutput", equals=True)),
    ]


@bindschema(schema=SubGraphSchema)
class SubGraphNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        project = (self.context or {}).get("project")
        context_values = (self.context or {}).get("context_values") or {}
        shared_globals = (self.context or {}).get("globals")
        emit = (self.context or {}).get("emit")
        settings = (self.context or {}).get("settings")

        graph_id = data.get("graphId")

        if not project:
            raise ValueError("SubGraphNode requires project context")
        graph = project.graphs.get(graph_id)
        if not graph:
            raise ValueError(f"SubGraphNode requires graph id {graph_id}")

        # Collect graph input defaults from node data
        input_data_defaults = data.get("inputData") or {}
        graph_inputs: Dict[str, Any] = {}
        graph_input_nodes = [n for n in graph.nodes if n.type == "graphInput"]
        sorted_input_ids = sorted({n.data.get("id") for n in graph_input_nodes if n.data.get("id")})

        for idx, input_id in enumerate(sorted_input_ids, start=1):
            if input_id in inputs:
                graph_inputs[input_id] = inputs[input_id]
            elif f"input{idx}" in inputs:
                graph_inputs[input_id] = inputs[f"input{idx}"]
            elif input_id in input_data_defaults:
                graph_inputs[input_id] = input_data_defaults[input_id]

        subprocessor = GraphProcessor(project, graph_id, shared_globals=shared_globals, settings=settings)
        parent_processor = self.context.get("processor")
        if isinstance(parent_processor, GraphProcessor):
            parent_processor.register_child(subprocessor)

        async def _forward_events():
            if not callable(emit):
                return
            async for ev_type, ev_data in subprocessor.events():
                # Don't forward graph-level events from subgraphs, only node-level events
                if ev_type in ("start", "graphStart", "graphFinish", "done", "abort", "error"):
                    continue

                try:
                    if isinstance(ev_data, dict):
                        payload = {**ev_data, "subgraphNodeId": self.node.id}
                    else:
                        payload = {"subgraphNodeId": self.node.id, "raw": str(ev_data)}
                except Exception:
                    payload = {"subgraphNodeId": self.node.id, "raw": str(ev_data)}
                await emit(ev_type, payload)

        forward_task = asyncio.create_task(_forward_events())
        start = time.time()
        try:
            outputs = await subprocessor.process_graph(inputs=graph_inputs, context_values=context_values)
            await forward_task
        except Exception as exc:
            await forward_task
            if not data.get("useErrorOutput"):
                raise
            # Return control-flow-excluded for expected outputs, string error otherwise
            out: Dict[str, Any] = {}
            out_index = 1
            for node in graph.nodes:
                if node.type != "graphOutput":
                    continue
                output_id = node.data.get("id")
                if output_id is None:
                    continue
                out[output_id] = {"type": "control-flow-excluded", "value": None}
                out[f"output{out_index}"] = {"type": "control-flow-excluded", "value": None}
                out_index += 1
            out["error"] = {"type": "string", "value": str(exc)}
            return out

        duration_ms = int((time.time() - start) * 1000)

        # Ensure duration output if absent
        if "duration" not in outputs:
            outputs["duration"] = {"type": "number", "value": duration_ms}

        if data.get("useErrorOutput"):
            outputs.setdefault("error", {"type": "control-flow-excluded", "value": None})

        # Also expose positional outputs for generic wiring if spec uses output{n}
        out_index = 1
        graph_output_nodes = [n for n in graph.nodes if n.type == "graphOutput"]
        sorted_output_ids = sorted({n.data.get("id") for n in graph_output_nodes if n.data.get("id")})
        for oid in sorted_output_ids:
            if oid in outputs:
                outputs[f"output{out_index}"] = outputs[oid]
                out_index += 1

        return outputs
