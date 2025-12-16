from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_extract_regex_node_basic(debugger_server_port: int):
    project_path = fixture_path("nodes/extract_regex_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {"input": {"type": "string", "value": "Hello Rivet!"}},
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["succeeded"]["value"] is True
    assert outputs["failed"]["value"] is False
    assert outputs["output1"] == {"type": "string", "value": "Rivet"}
    assert outputs["matches"]["value"] == ["Rivet"]
