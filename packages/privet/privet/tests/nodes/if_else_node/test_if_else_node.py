from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_if_else_true(debugger_server_port: int):
    project_path = fixture_path("nodes/if_else_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "cond": {"type": "boolean", "value": True},
            "tval": {"type": "string", "value": "yes"},
            "fval": {"type": "string", "value": "no"},
        },
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["out"] == {"type": "string", "value": "yes"}


@pytest.mark.asyncio
async def test_if_else_false(debugger_server_port: int):
    project_path = fixture_path("nodes/if_else_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "cond": {"type": "boolean", "value": False},
            "tval": {"type": "string", "value": "yes"},
            "fval": {"type": "string", "value": "no"},
        },
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["out"] == {"type": "string", "value": "no"}
