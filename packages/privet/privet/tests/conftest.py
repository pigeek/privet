from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import time
from typing import Any, Dict, List

import pytest
import pytest_asyncio
import websockets

# Ensure privet is importable regardless of cwd during pytest
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

WS_HOST = "127.0.0.1"
WS_PORT = 21888


async def run_graph_via_ws(port: int, project: Dict[str, Any], inputs: Dict[str, Any]) -> List[Dict[str, Any]]:
    uri = f"ws://{WS_HOST}:{port}"
    events: List[Dict[str, Any]] = []

    async with websockets.connect(uri) as ws:
        _ = await asyncio.wait_for(ws.recv(), timeout=5)

        await ws.send(json.dumps({"type": "set-dynamic-data", "data": {"project": project, "settings": {}}}))
        await ws.send(json.dumps({"type": "run", "data": {"graphId": "main", "inputs": inputs, "contextValues": {}}}))

        while True:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=5)
            except websockets.ConnectionClosed:
                break
            except asyncio.TimeoutError:
                break
            msg = json.loads(raw)
            events.append(msg)
            if msg.get("message") in ("done", "abort", "error"):
                break

    return events


@pytest_asyncio.fixture(scope="session")
async def debugger_server_port():
    """
    Use the same WS endpoint the UI talks to (ws://localhost:21888). If something is already
    listening there, reuse it; otherwise start uvicorn privet.main:app on port 8000 (WS on 21888).
    """
    try:
        async with websockets.connect(f"ws://{WS_HOST}:{WS_PORT}") as ws:
            await asyncio.wait_for(ws.recv(), timeout=2)
        yield WS_PORT
        return
    except Exception:
        pass

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "privet.main:app", "--reload", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    deadline = time.time() + 15
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            async with websockets.connect(f"ws://{WS_HOST}:{WS_PORT}") as ws:
                await asyncio.wait_for(ws.recv(), timeout=2)
            last_err = None
            break
        except Exception as exc:
            last_err = exc
            await asyncio.sleep(0.5)
    if last_err:
        proc.terminate()
        proc.wait(timeout=5)
        pytest.skip(f"Could not start backend/WS server: {last_err}")

    try:
        yield WS_PORT
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
