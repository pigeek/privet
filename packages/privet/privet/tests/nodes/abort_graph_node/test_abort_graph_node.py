from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_abort_graph_node(debugger_server_port: int):
    project_path = fixture_path("nodes/abort_graph_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(debugger_server_port, project, {})

    # Backend may close the socket immediately after abort; ensure at least one event and no exception.
    assert len(events) >= 1
