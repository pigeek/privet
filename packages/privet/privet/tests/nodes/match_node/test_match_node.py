from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_match_node_exclusive(debugger_server_port: int):
    project_path = fixture_path("nodes/match_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "text": {"type": "string", "value": "foo baz"},
            "val": {"type": "string", "value": "payload"},
        },
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["case1"] == {"type": "string", "value": "payload"}
    # case2 may be absent if the GraphOutput was excluded; either way it should not have a value
    case2 = outputs.get("case2")
    if case2 is not None:
        assert case2["type"] == "control-flow-excluded"
    unmatched = outputs.get("unmatched")
    if unmatched is not None:
        assert unmatched["type"] == "control-flow-excluded"
