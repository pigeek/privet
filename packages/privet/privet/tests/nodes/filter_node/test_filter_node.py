from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_filter_node(debugger_server_port: int):
    project_path = fixture_path("nodes/filter_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(debugger_server_port, project, {})

    normalized = normalize_events(events)
    assert normalized == [
        {"message": "start"},
        {"message": "graphStart", "graphId": "main"},
        {"message": "nodeStart", "node": {"id": "n1", "type": "graphInput"}},
        {"message": "nodeFinish", "node": {"id": "n1", "type": "graphInput"}},
        {"message": "nodeStart", "node": {"id": "n2", "type": "graphInput"}},
        {"message": "nodeFinish", "node": {"id": "n2", "type": "graphInput"}},
        {"message": "nodeStart", "node": {"id": "n3", "type": "filter"}},
        {"message": "nodeFinish", "node": {"id": "n3", "type": "filter"}},
        {"message": "nodeStart", "node": {"id": "n4", "type": "graphOutput"}},
        {"message": "nodeFinish", "node": {"id": "n4", "type": "graphOutput"}},
        {"message": "graphFinish", "graphId": "main"},
        {"message": "done"},
    ]

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["out"] == {"type": "any[]", "value": ["a", "c"]}
