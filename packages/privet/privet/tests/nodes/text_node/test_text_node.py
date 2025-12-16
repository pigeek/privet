from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_text_node_interpolation(debugger_server_port: int):
    project_path = fixture_path("nodes/text_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(debugger_server_port, project, {"name": {"type": "string", "value": "Rivet"}})

    normalized = normalize_events(events)
    assert normalized[0]["message"] == "start"

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["out"] == {"type": "string", "value": "Hello Rivet"}
