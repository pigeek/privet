from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, List, Optional, Set, Tuple, ClassVar
import json

from .types import ChartNode, DataValue, GraphId, NodeGraph, NodeId, Project
from ..BaseNode import BaseNode
# Ensure node implementations are imported for registration side-effects
from .. import nodes as _nodes  # noqa: F401


ProcessEvent = Tuple[str, Dict[str, Any]]


@dataclass(eq=False)
class GraphProcessor:
    _active_processors: ClassVar[Set["GraphProcessor"]] = set()

    project: Project
    graph_id: Optional[GraphId] = None
    shared_globals: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None
    run_to_node_ids: Optional[List[NodeId]] = None
    run_from_node_id: Optional[NodeId] = None

    def __post_init__(self) -> None:
        graph = (
            self.project.graphs.get(self.graph_id) if self.graph_id else self.project.graphs.get(self.project.metadata.mainGraphId or "")
        )
        if not graph:
            raise ValueError(f"Graph {self.graph_id} not found in project")
        self.graph: NodeGraph = graph
        self._nodes_by_id: Dict[NodeId, ChartNode] = {n.id: n for n in self.graph.nodes}
        self._connections_by_node: Dict[NodeId, List[Any]] = {}
        for conn in self.graph.connections:
            self._connections_by_node.setdefault(conn.inputNodeId, []).append(conn)
            self._connections_by_node.setdefault(conn.outputNodeId, []).append(conn)

        # Shared global storage across a processor run (can be shared with subgraphs)
        self._globals: Dict[str, Any] = self.shared_globals if self.shared_globals is not None else {}

        self._running: bool = False
        self._paused: bool = False
        self._aborted: bool = False
        self._process_graph_task: Optional[asyncio.Task] = None
        self._preloaded: Dict[NodeId, Dict[str, DataValue]] = {}
        self._events: asyncio.Queue[ProcessEvent] = asyncio.Queue()
        self._node_outputs: Dict[NodeId, Dict[str, DataValue]] = {}
        self._node_inputs: Dict[NodeId, Dict[str, DataValue]] = {}
        self._user_input_queue: asyncio.Queue[Tuple[NodeId, Dict[str, DataValue]]] = asyncio.Queue()
        self._user_input_event: asyncio.Event = asyncio.Event()
        self._pending_user_inputs: Dict[NodeId, asyncio.Future] = {}
        self._log_path = "/tmp/privet_run.log"
        self._log_initialized = False
        GraphProcessor._active_processors.add(self)
        self._children: Set["GraphProcessor"] = set()
        self._parent: Optional["GraphProcessor"] = None
        self._visited_nodes: Set[NodeId] = set()  # Track processed nodes like TypeScript
        self._event_waiters: Dict[str, List[asyncio.Future]] = {}
        self._event_queue: Dict[str, List[Any]] = {}  # Deliver events raised before waiters subscribe

    __hash__ = object.__hash__

    async def emit(self, type_: str, data: Dict[str, Any]) -> None:
        # Debug visibility for core lifecycle events
        if type_ in ("start", "graphStart", "graphFinish", "nodeStart", "nodeFinish", "nodeExcluded", "error"):
            try:
                print(f"[GraphProcessor] {type_}: {data}")
            except Exception:
                pass
        try:
            # Overwrite log at beginning of a run
            mode = "a"
            if not self._log_initialized and type_ == "start":
                mode = "w"
                self._log_initialized = True
            with open(self._log_path, mode) as f:
                f.write(f"{type_}: {data}\n")
        except Exception:
            pass
        await self._events.put((type_, data))

    async def events(self) -> AsyncGenerator[ProcessEvent, None]:
        while True:
            type_, data = await self._events.get()
            yield (type_, data)
            # Only break on main graph completion (done/abort/error without subgraphNodeId)
            if type_ in ("done", "abort", "error"):
                # Check if this is a subgraph event (has subgraphNodeId)
                if isinstance(data, dict) and "subgraphNodeId" in data:
                    continue  # Keep listening for more events
                else:
                    break  # Main graph is done

    def preload_node_data(self, node_id: NodeId, outputs: Dict[str, DataValue]) -> None:
        self._preloaded[node_id] = outputs

    def get_dependency_nodes_deep(self, node_id: NodeId) -> List[NodeId]:
        node = self._nodes_by_id.get(node_id)
        if not node:
            return []
        conns = self._connections_by_node.get(node_id) or []
        deps: List[NodeId] = []
        for c in conns:
            if c.inputNodeId == node_id:
                deps.extend(self.get_dependency_nodes_deep(c.outputNodeId))
        # dedupe and include self
        out = list(dict.fromkeys([node_id, *deps]).keys())
        return out

    def _incoming(self) -> Dict[NodeId, Set[NodeId]]:
        incoming: Dict[NodeId, Set[NodeId]] = {n.id: set() for n in self.graph.nodes}
        for c in self.graph.connections:
            incoming[c.inputNodeId].add(c.outputNodeId)
        return incoming

    async def pause(self) -> None:
        self._paused = True
        await self.emit("pause", {})

    async def resume(self) -> None:
        self._paused = False
        await self.emit("resume", {})

    async def user_input(self, node_id: NodeId, answers: Dict[str, DataValue]) -> None:
        """Called by the debugger to provide user input to a waiting node."""
        # If a node is actively waiting, resolve its future immediately; otherwise queue it.
        pending = self._pending_user_inputs.get(node_id)
        if pending and not pending.done():
            pending.set_result(answers)
            status = "resolved-pending"
        else:
            await self._user_input_queue.put((node_id, answers))
            status = "queued"
        self._user_input_event.set() # Signal that input is available
        print(f"[GraphProcessor] user_input received for node {node_id} ({status}): {answers}")
        graph_id = getattr(self.graph.metadata, "id", None)
        await self.emit("trace", {"message": f"User input received for node {node_id} (graph={graph_id}, {status})"})
        
    async def abort(self, successful: bool = False, error: Optional[str] = None) -> None:
        self._aborted = True
        if self._process_graph_task:
            self._process_graph_task.cancel()
            self._process_graph_task = None
        await self.emit("graphAbort", {"successful": successful, "graph": self.graph, "error": error})
        await self.emit("abort", {"successful": successful, "error": error})

    def _get_root_processor(self) -> "GraphProcessor":
        """Walk up parent pointers to find the root processor."""
        processor: "GraphProcessor" = self
        while processor._parent:
            processor = processor._parent
        return processor

    def raise_event(self, event_name: str, data: Any) -> None:
        """Raise a user event on the root processor and propagate to children."""
        root = self._get_root_processor()
        root._dispatch_event(event_name, data)

    def _dispatch_event(self, event_name: str, data: Any) -> None:
        """Resolve any waiters for this event and propagate to children."""
        waiters = list(self._event_waiters.get(event_name, []))
        delivered = False
        for fut in waiters:
            if fut.done():
                continue
            try:
                fut.set_result(data)
                delivered = True
            except Exception:
                continue
        # If no one was waiting, queue it for the next wait_event call
        if not delivered:
            self._event_queue.setdefault(event_name, []).append(data)

        # Propagate to child processors (e.g., subgraphs)
        for child in list(self._children):
            child._dispatch_event(event_name, data)

    async def wait_event(self, event_name: str) -> Any:
        """Wait for a user event raised via RaiseEventNode or host."""
        loop = asyncio.get_running_loop()
        # First, consume any queued events for this name
        queued = self._event_queue.get(event_name)
        if queued:
            return queued.pop(0)

        future: asyncio.Future = loop.create_future()
        self._event_waiters.setdefault(event_name, []).append(future)

        try:
            if self._aborted:
                raise asyncio.CancelledError("Processor aborted")
            return await future
        finally:
            waiters = self._event_waiters.get(event_name)
            if waiters and future in waiters:
                waiters.remove(future)
                if not waiters:
                    self._event_waiters.pop(event_name, None)

    async def _wait_until_unpaused(self) -> None:
        while self._paused and not self._aborted:
            await asyncio.sleep(0.05)

    def _outgoing_ports(self, node_id: NodeId) -> List[str]:
        ports: List[str] = []
        for c in self.graph.connections:
            if c.outputNodeId == node_id and c.outputId not in ports:
                ports.append(c.outputId)
        return ports

    def _get_downstream_nodes(self, node_id: NodeId) -> Set[NodeId]:
        """Get all nodes that are downstream from the given node (can be reached via connections)."""
        visited = set()
        to_visit = [node_id]

        while to_visit:
            current = to_visit.pop()
            if current in visited:
                continue
            visited.add(current)

            # Find all nodes this node connects to
            for conn in self.graph.connections:
                if conn.outputNodeId == current and conn.inputNodeId not in visited:
                    to_visit.append(conn.inputNodeId)

        # Remove the starting node itself from the result
        visited.discard(node_id)
        return visited

    def _connected_inputs_ready(self, node: ChartNode, node_inputs: Dict[str, DataValue]) -> bool:
        """Ensure all inputs that have connections into this node have values."""
        for conn in self.graph.connections:
            if conn.inputNodeId != node.id:
                continue
            if conn.inputId not in node_inputs:
                # Allow loopController to start when an input has a matching Default value
                if (
                    node.type == "loopController"
                    and conn.inputId.startswith("input")
                    and node_inputs.get(f"{conn.inputId}Default") is not None
                ):
                    continue
                # Missing input that has a connection; not ready yet
                try:
                    with open("/tmp/privet_run.log", "a") as f:
                        f.write(f"nodeWait: {{'node': '{node.id}', 'type': '{node.type}', 'missing': '{conn.inputId}', 'inputs': {list(node_inputs.keys())}}}\n")
                except Exception:
                    pass
                return False
        return True

    async def process_graph(
        self,
        inputs: Dict[str, DataValue] | None = None,
        context_values: Dict[str, DataValue] | None = None,
        run_to_node_ids: Optional[List[NodeId]] = None,
        run_from_node_id: Optional[NodeId] = None,
    ) -> Dict[str, DataValue]:
        if self._running:
            raise RuntimeError("Graph is already running")
        self._running = True
        self._process_graph_task = asyncio.current_task() # Store the current task

        

        inputs = inputs or {}

        context_values = context_values or {}

        run_to_node_ids = run_to_node_ids or []



        # Shared context passed to node implementations. Keep minimal and expand as nodes are ported.

        context: Dict[str, Any] = {

            "graph_inputs": inputs,

            "graph_input_node_values": {},

            "graph_outputs": {}, # This will be the main output collection

            "context_values": context_values,

            "emit": self.emit,

            "globals": self._globals,

            "project": self.project,

            "attached_data": {},

            "processor": self, # Allow nodes to access the processor directly
            "settings": self.settings or {},
            "raise_event": self.raise_event,
            "wait_event": self.wait_event,

            "create_subprocessor": lambda gid, shared=None: GraphProcessor(

                self.project,
                gid,
                shared_globals=self._globals if shared is None else shared,
                settings=self.settings,

            ),

        }

        

        # Clear previous graph outputs if this is a targeted run

        if run_to_node_ids:

            context["graph_outputs"] = {}



        await self.emit("start", {"project": self.project, "startGraph": self.graph, "inputs": inputs, "contextValues": context_values})

        await self.emit("graphStart", {"graph": self.graph, "inputs": inputs})



        # Preloaded data becomes synthetic nodeStart/nodeFinish

        for node_id, outputs in self._preloaded.items():

            node = self._nodes_by_id.get(node_id)

            if not node:

                continue

            await self.emit("nodeStart", {"node": node, "inputs": {}, "processId": "preload"})

            await self.emit("nodeFinish", {"node": node, "outputs": outputs, "processId": "preload"})

            self._node_outputs[node_id] = outputs



        # Iterative scheduler that allows cycles by re-running nodes when inputs change

        last_input_signatures: Dict[NodeId, str] = {}

        run_counts: Dict[NodeId, int] = {}

        max_runs = max(10, len(self.graph.nodes) * 10)

        

        # New logic for runFromNodeId and runToNodeIds

        should_run = False

        if run_from_node_id is None:

            should_run = True

        

        processed_run_to_nodes: Set[NodeId] = set()



        

        should_break_outer_loop = False



        try:
            for _ in range(max_runs):
                if self._aborted:
                    break
                progress = False
                for node in self.graph.nodes:
                    if should_break_outer_loop:
                        break

                    if not should_run and node.id == run_from_node_id:
                        should_run = True

                    if not should_run:
                        continue

                    # Skip nodes that have already been processed (like TypeScript line 1042)
                    # Exception: loopController can run multiple times
                    if node.id in self._visited_nodes and node.type != "loopController":
                        continue

                    await self._wait_until_unpaused()
                    # Gather inputs from upstream outputs
                    node_inputs: Dict[str, DataValue] = {}
                    for conn in self.graph.connections:
                        if conn.inputNodeId != node.id:
                            continue
                        src_outputs = self._node_outputs.get(conn.outputNodeId) or {}
                        if conn.outputId in src_outputs:
                            node_inputs[conn.inputId] = src_outputs[conn.outputId]

                    # Include any preloaded inputs saved earlier
                    if node.id in self._node_inputs:
                        node_inputs.update(self._node_inputs[node.id])

                    # If this node has incoming connections but some are not yet provided, defer until upstream runs
                    if not self._connected_inputs_ready(node, node_inputs):
                        continue

                    input_sig = json.dumps(node_inputs, sort_keys=True, default=str)
                    if run_counts.get(node.id, 0) > 0 and input_sig == last_input_signatures.get(node.id):
                        continue

                    last_input_signatures[node.id] = input_sig
                    run_counts[node.id] = run_counts.get(node.id, 0) + 1

                    # Control-flow exclusion handling: skip processing if every input is excluded
                    if node_inputs and all(isinstance(v, dict) and v.get("type") == "control-flow-excluded" for v in node_inputs.values()):
                        outputs: Dict[str, DataValue] = {}
                        for out_id in self._outgoing_ports(node.id):
                            outputs[out_id] = {"type": "control-flow-excluded", "value": None}
                        self._node_outputs[node.id] = outputs
                        await self.emit(
                            "nodeExcluded",
                            {"node": node, "inputs": node_inputs, "outputs": outputs, "processId": "sim", "reason": "control-flow-excluded"},
                        )
                        self._visited_nodes.add(node.id)  # Mark as visited
                        progress = True
                        continue

                    # Clear prior outputs when re-running with new inputs
                    if run_counts[node.id] > 1:
                        await self.emit("nodeOutputsCleared", {"node": node, "processId": "sim"})

                    await self.emit("nodeStart", {"node": node, "inputs": node_inputs, "processId": "sim"})

                    impl = self._create_node_impl(node, context)
                    try:
                        outputs: Dict[str, DataValue] = await impl.process(node_inputs)  # type: ignore[assignment]
                    except Exception as exc:
                        await self.emit(
                            "nodeError",
                            {
                                "node": node,
                                "inputs": node_inputs,
                                "processId": "sim",
                                "error": str(exc),
                            },
                        )
                        await self.emit(
                            "error",
                            {
                                "node": node,
                                "inputs": node_inputs,
                                "processId": "sim",
                                "error": str(exc),
                            },
                        )
                        raise

                    self._node_outputs[node.id] = outputs or {}
                    await self.emit("nodeFinish", {"node": node, "outputs": outputs or {}, "processId": "sim"})

                    # Handle loop controller clearing logic like TypeScript
                    if node.type == "loopController":
                        # Check if loop should continue (break output is control-flow-excluded)
                        break_output = outputs.get("break")
                        if isinstance(break_output, dict) and break_output.get("type") == "control-flow-excluded":
                            # Loop continues - clear all nodes that could be part of the loop cycle
                            # For simplicity, clear all nodes downstream from this loop controller
                            downstream_nodes = self._get_downstream_nodes(node.id)
                            for downstream_id in downstream_nodes:
                                self._visited_nodes.discard(downstream_id)

                    self._visited_nodes.add(node.id)  # Mark as visited after successful processing
                    progress = True

                    if node.id in run_to_node_ids:
                        processed_run_to_nodes.add(node.id)
                    
                    if len(run_to_node_ids) > 0 and len(processed_run_to_nodes) == len(run_to_node_ids):
                        await self.emit("trace", {"message": f"All runToNodeIds ({run_to_node_ids}) processed. Setting flag to stop graph."})
                        should_break_outer_loop = True
                        break # Break from inner loop
                
                if should_break_outer_loop:
                    break # Break from outer loop

                if not progress:
                    break

            outputs: Dict[str, DataValue] = context.get("graph_outputs", {})
            await self.emit("graphFinish", {"graph": self.graph, "outputs": outputs})
            await self.emit("done", {"results": outputs, "runToNodeIds": list(processed_run_to_nodes), "runFromNodeId": run_from_node_id})
            return outputs
        finally:
            self._running = False
            self._process_graph_task = None
            GraphProcessor._active_processors.discard(self)
            if self._parent:
                self._parent._children.discard(self)

    @classmethod
    def all_active(cls) -> List["GraphProcessor"]:
        return list(cls._active_processors)

    def register_child(self, child: "GraphProcessor") -> None:
        child._parent = self
        # Share the log file with the parent but avoid truncating it when the child starts.
        child._log_path = self._log_path
        child._log_initialized = True
        self._children.add(child)

    def all_descendants(self) -> List["GraphProcessor"]:
        out: List["GraphProcessor"] = [self]
        for c in list(self._children):
            out.extend(c.all_descendants())
        return out
    def _create_node_impl(self, node: ChartNode, context: Dict[str, Any]) -> BaseNode:
        impl_cls = BaseNode.for_type(node.type)
        return impl_cls(node, context)
