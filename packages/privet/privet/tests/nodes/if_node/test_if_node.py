from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_if_node_true_branch(debugger_server_port: int):
    project_path = fixture_path("nodes/if_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "cond": {"type": "boolean", "value": True},
            "val": {"type": "string", "value": "go"},
        },
    )

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["true_out"] == {"type": "string", "value": "go"}
    assert outputs.get("false_out") is None or outputs["false_out"]["type"] == "control-flow-excluded"


@pytest.mark.asyncio
async def test_if_node_false_branch(debugger_server_port: int):
    project_path = fixture_path("nodes/if_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "cond": {"type": "boolean", "value": False},
            "val": {"type": "string", "value": "stop"},
        },
    )

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["false_out"] == {"type": "string", "value": "stop"}
    assert outputs.get("true_out") is None or outputs["true_out"]["type"] == "control-flow-excluded"
