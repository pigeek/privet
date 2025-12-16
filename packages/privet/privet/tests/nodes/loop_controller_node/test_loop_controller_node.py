from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_loop_controller_outputs_break_when_continue_false(debugger_server_port: int):
    project_path = fixture_path("nodes/loop_controller_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {"val": {"type": "string", "value": "foo"}, "continue": {"type": "boolean", "value": False}},
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    # GraphOutput with control-flow-excluded input does not populate results; check break instead
    assert outputs["br"]["type"] == "any[]"
