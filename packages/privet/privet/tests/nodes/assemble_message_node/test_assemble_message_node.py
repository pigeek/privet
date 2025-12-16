from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_assemble_message_node(debugger_server_port: int):
    project_path = fixture_path("nodes/assemble_message_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {"part1": {"type": "string", "value": "hello"}},
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    msg = outputs["out"]["value"]
    assert msg["type"] == "user"
    assert msg["message"] == ["hello"]
