from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_raise_event_node_flow(debugger_server_port: int):
    project_path = fixture_path("nodes/raise_event_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(debugger_server_port, project, {"msg": {"type": "string", "value": "ping-msg"}})

    normalized = normalize_events(events)
    assert normalized == [
        {"message": "start"},
        {"message": "graphStart", "graphId": "main"},
        {"message": "nodeStart", "node": {"id": "n1", "type": "graphInput"}},
        {"message": "nodeFinish", "node": {"id": "n1", "type": "graphInput"}},
        {"message": "nodeStart", "node": {"id": "n2", "type": "raiseEvent"}},
        {"message": "nodeFinish", "node": {"id": "n2", "type": "raiseEvent"}},
        {"message": "nodeStart", "node": {"id": "n3", "type": "waitForEvent"}},
        {"message": "nodeFinish", "node": {"id": "n3", "type": "waitForEvent"}},
        {"message": "nodeStart", "node": {"id": "n4", "type": "graphOutput"}},
        {"message": "nodeFinish", "node": {"id": "n4", "type": "graphOutput"}},
        {"message": "nodeStart", "node": {"id": "n5", "type": "graphOutput"}},
        {"message": "nodeFinish", "node": {"id": "n5", "type": "graphOutput"}},
        {"message": "graphFinish", "graphId": "main"},
        {"message": "done"},
    ]

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["out"]["value"] == "ping-msg"
    assert outputs["event"]["value"] == "ping-msg"
