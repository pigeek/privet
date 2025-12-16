from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_comment_node_no_outputs(debugger_server_port: int):
    project_path = fixture_path("nodes/comment_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(debugger_server_port, project, {})

    # Graph has no outputs; just ensure it runs and finishes
    messages = [ev.get("message") for ev in events]
    assert "done" in messages
