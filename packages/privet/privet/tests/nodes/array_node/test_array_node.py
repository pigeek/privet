from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_array_node_flatten(debugger_server_port: int):
    project_path = fixture_path("nodes/array_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "a": {"type": "string", "value": "x"},
            "b": {"type": "string[]", "value": ["y", "z"]},
            "c": {"type": "string", "value": "w"},
        },
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["out"] == {"type": "any[]", "value": ["x", "y", "z", "w"]}
