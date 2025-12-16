from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_call_graph_node(debugger_server_port: int):
    project_path = fixture_path("nodes/call_graph_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {"inputs": {"type": "object", "value": {"msg": {"type": "string", "value": "hi"}}}},
    )

    normalized = normalize_events(events)
    assert normalized[0:2] == [
        {"message": "start"},
        {"message": "graphStart", "graphId": "main"},
    ]
    assert normalized[-1]["message"] == "done"

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    out_val = outputs["out"]
    assert out_val["type"] == "object"
    assert out_val["value"]["out"] == {"type": "string", "value": "hi"}
