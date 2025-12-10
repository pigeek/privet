import asyncio
import json
import logging
from typing import Any, Dict

import websockets
from websockets.server import WebSocketServerProtocol


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

        # In-memory placeholders for uploaded project/static data
        self.dynamic_data: Dict[str, Any] = {}
        self.static_data: Dict[str, Any] = {}

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
            logger.debug("Dynamic data updated: keys=%s", list(self.dynamic_data.keys()))
        elif msg_type == "preload":
            # Accept and ignore for now
            logger.debug("Preload received: %s", list((data or {}).keys()))
        elif msg_type == "user-input":
            logger.debug("User input received: %s", data)
        elif msg_type == "abort":
            await websocket.send(json.dumps({"message": "abort", "data": {}}))
        elif msg_type == "pause":
            await websocket.send(json.dumps({"message": "pause", "data": {}}))
        elif msg_type == "resume":
            await websocket.send(json.dumps({"message": "resume", "data": {}}))
        elif msg_type == "run":
            # Send minimal lifecycle so UI doesn’t error. No real execution here.
            graph_id = (data or {}).get("graphId")
            await websocket.send(json.dumps({"message": "start", "data": {"graphId": graph_id}}))
            await websocket.send(
                json.dumps(
                    {
                        "message": "done",
                        "data": {"results": {}},  # empty results
                    }
                )
            )
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

