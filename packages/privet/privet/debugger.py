import asyncio
import json
import logging
import tempfile
from typing import Any, Dict

import websockets
from websockets.server import WebSocketServerProtocol
from .graph.types import project_from_json
from .graph.processor import GraphProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RemoteDebuggerServer:
    """
    Minimal remote debugger WebSocket server to accept commands from the Rivet UI.

    Notes:
    - Binds to ws://localhost:21888 and accepts a single client.
    - Immediately notifies the client that graph upload is allowed.
    - Accepts known command messages and responds with simple acknowledgements.
    - Sends synthetic run lifecycle events for 'run' to keep UI functional.
    """

    def __init__(self, host: str = "localhost", port: int = 21888) -> None:
        self.host = host
        self.port = port
        self._server: websockets.server.Serve | None = None
        self._clients: set[WebSocketServerProtocol] = set()
        self._processors: list[Any] = []

        # In-memory placeholders for uploaded project/static data
        self.dynamic_data: Dict[str, Any] = {}
        self.static_data: Dict[str, Any] = {}
        self._last_project_dump_path: str | None = None

    async def _on_connect(self, websocket: WebSocketServerProtocol) -> None:
        self._clients.add(websocket)
        logger.info("Client connected: %s", websocket.remote_address)
        # Inform client that uploads are allowed
        await websocket.send(json.dumps({"message": "graph-upload-allowed", "data": True}))

    async def _on_disconnect(self, websocket: WebSocketServerProtocol) -> None:
        if websocket in self._clients:
            self._clients.remove(websocket)
        logger.info("Client disconnected: %s", websocket.remote_address)

    async def _handle_message(self, websocket: WebSocketServerProtocol, raw: str) -> None:
        # Two formats are used by the UI: JSON {type,data} and a raw string 'set-static-data:<id>:<json>'
        try:
            msg = json.loads(raw)
            msg_type = msg.get("type")
            data = msg.get("data")
        except json.JSONDecodeError:
            # Handle raw data messages
            if raw.startswith("set-static-data:"):
                _, id_part, json_part = raw.split(":", 2)
                try:
                    self.static_data[id_part] = json.loads(json_part)
                except Exception:
                    self.static_data[id_part] = json_part
                logger.debug("Stored static data for %s", id_part)
            else:
                logger.warning("Unknown non-JSON message: %s", raw)
            return

        if msg_type == "set-dynamic-data":
            self.dynamic_data = data or {}
            settings = self.dynamic_data.get("settings") or {}
            has_key = bool(settings.get("openAiKey"))
            logger.info("Dynamic data updated: keys=%s settings.openAiKey=%s", list(self.dynamic_data.keys()), has_key)
            # Best-effort dump of the incoming project for inspection
            try:
                await self._dump_project_to_temp(websocket)
            except Exception as e:
                logger.exception("Failed to write project dump: %s", e)
        elif msg_type == "preload":
            # Accept and ignore for now
            logger.debug("Preload received: %s", list((data or {}).keys()))
        elif msg_type == "user-input":
            try:
                print(f"[RemoteDebugger] user-input received: {data}")
            except Exception:
                pass
            node_id = (data or {}).get("nodeId")
            answers = (data or {}).get("answers")
            logger.info("user-input received for node %s answers=%s", node_id, answers)
            if node_id and answers is not None:
                # Route to this client's processors plus their subgraphs
                processors: list[GraphProcessor] = []
                for root in list(self._processors):
                    processors.extend(root.all_descendants())
                for processor in processors:
                    try:
                        await processor.user_input(node_id, answers)
                    except Exception:
                        continue
            logger.debug("User input received: %s", data)
        elif msg_type == "abort":
            for processor in list(self._processors):
                try:
                    await processor.abort()
                except Exception:
                    continue
        elif msg_type == "pause":
            for processor in list(self._processors):
                try:
                    await processor.pause()
                except Exception:
                    continue
        elif msg_type == "resume":
            for processor in list(self._processors):
                try:
                    await processor.resume()
                except Exception:
                    continue
        elif msg_type == "run":
            # Execute via Python GraphProcessor (synthetic events for now)
            graph_id = (data or {}).get("graphId")
            inputs = (data or {}).get("inputs") or {}
            context_values = (data or {}).get("contextValues") or {}
            try:
                print(f"[RemoteDebugger] run received raw data={data}")
            except Exception:
                pass

            # Build project from last uploaded dynamic data
            project_json = self.dynamic_data.get("project") or {}
            try:
                project = project_from_json(project_json)
            except Exception as e:
                logger.exception("Invalid project payload: %s", e)
                await websocket.send(json.dumps({"message": "error", "data": {"error": str(e)}}))
                return

            # Resolve graph to run: prefer explicit graphId, then project mainGraphId, then first graph.
            chosen_graph_id = graph_id
            if not chosen_graph_id:
                chosen_graph_id = project.metadata.mainGraphId
            if not chosen_graph_id and project.graphs:
                chosen_graph_id = next(iter(project.graphs.keys()))

            try:
                print(f"[RemoteDebugger] run requested graphId={graph_id} resolved={chosen_graph_id}")
            except Exception:
                pass

            processor = GraphProcessor(project, chosen_graph_id, settings=self.dynamic_data.get("settings"))
            self._processors.append(processor)

            async def forward_events():
                async for ev_type, ev_data in processor.events():
                    # Shape events as the UI expects: message + data
                    # Convert dataclasses to dicts via json dumps/loads for simplicity
                    try:
                        payload = json.loads(json.dumps(ev_data, default=lambda o: getattr(o, "__dict__", str(o))))
                    except Exception:
                        payload = {"raw": str(ev_data)}

                    # Debug: Log all main graph events (not just nodeStart/nodeFinish)
                    if isinstance(ev_data, dict) and "subgraphNodeId" not in ev_data:
                        try:
                            with open("/tmp/main_graph_events.log", "a") as f:
                                f.write(f"[MainGraph] {ev_type}: {json.dumps(payload, indent=2)}\n")
                        except Exception:
                            pass

                    await websocket.send(json.dumps({"message": ev_type, "data": payload}))

            async def _run_and_forward():
                # Start event forwarding and graph execution together
                forward_task = asyncio.create_task(forward_events())

                try:
                    await processor.process_graph(
                        inputs=inputs,
                        context_values=context_values,
                        run_to_node_ids=data.get("runToNodeIds"),
                        run_from_node_id=data.get("runFromNodeId"),
                    )
                except Exception as e:
                    # Emit error event to UI
                    try:
                        await websocket.send(json.dumps({"message": "error", "data": {"error": str(e)}}))
                    except Exception:
                        pass
                finally:
                    if processor in self._processors:
                        self._processors.remove(processor)

                # Wait for all events to be forwarded
                await forward_task

            asyncio.create_task(_run_and_forward())
        elif isinstance(msg_type, str) and msg_type.startswith("datasets:"):
            # Respond with generic ack for dataset operations
            request_id = (data or {}).get("requestId")
            await websocket.send(
                json.dumps(
                    {
                        "type": "datasets:response",
                        "data": {"requestId": request_id, "payload": None},
                    }
                )
            )
        else:
            logger.info("Unhandled message type: %s", msg_type)

    async def _client_handler(self, websocket: WebSocketServerProtocol):
        await self._on_connect(websocket)
        try:
            async for message in websocket:
                await self._handle_message(websocket, message)
        except Exception as e:
            logger.exception("WebSocket client error: %s", e)
        finally:
            await self._on_disconnect(websocket)

    async def _dump_project_to_temp(self, websocket: WebSocketServerProtocol) -> None:
        project_json = self.dynamic_data.get("project") or {}
        if not project_json:
            return
        # Create a temporary file and write the project JSON for inspection
        with tempfile.NamedTemporaryFile(prefix="rivet_project_", suffix=".json", delete=False, mode="w") as f:
            json.dump(project_json, f, indent=2)
            path = f.name
        self._last_project_dump_path = path
        # Inform client via trace and log it
        msg = f"Project JSON dumped to: {path}"
        # Print to stdout in addition to logger for visibility when logging isn't configured
        print(msg)
        logger.info(msg)
        try:
            await websocket.send(json.dumps({"message": "trace", "data": msg}))
        except Exception:
            # If trace fails, ignore
            pass

    async def start(self):
        logger.info("Starting RemoteDebuggerServer on ws://%s:%d", self.host, self.port)
        self._server = await websockets.serve(self._client_handler, self.host, self.port)

    async def stop(self):
        if self._server is not None:
            logger.info("Stopping RemoteDebuggerServer")
            self._server.close()
            await self._server.wait_closed()


async def run_server_forever():
    server = RemoteDebuggerServer()
    await server.start()
    # Keep running
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        await server.stop()
