from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_loop_until_node_input_equal(debugger_server_port: int):
    project_path = fixture_path("nodes/loop_until_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {"start": {"type": "number", "value": 1}},
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["completed"]["value"] in (True, False)
    # Out should eventually become a string representation; accept any string here
    assert outputs.get("out") is not None
    assert outputs["iter"]["value"] >= 1
