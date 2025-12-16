from __future__ import annotations

import os
import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_read_file_node(debugger_server_port: int):
    project_path = fixture_path("nodes/read_file_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    path = fixture_path("nodes/read_file_node/fixtures/sample.txt")
    events = await run_graph_via_ws(debugger_server_port, project, {"path": {"type": "string", "value": path}})

    normalized = normalize_events(events)
    assert normalized[0:2] == [
        {"message": "start"},
        {"message": "graphStart", "graphId": "main"},
    ]
    assert normalized[-1]["message"] == "done"

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["out"] == {"type": "string", "value": "sample content for read file\n"}
