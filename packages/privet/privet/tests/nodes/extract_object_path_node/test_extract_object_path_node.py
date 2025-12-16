from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_extract_object_path_node(debugger_server_port: int):
    project_path = fixture_path("nodes/extract_object_path_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    obj = {"items": [{"name": "first"}, {"name": "second"}]}
    events = await run_graph_via_ws(debugger_server_port, project, {"obj": {"type": "object", "value": obj}})
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["match"]["value"] == "first"
    assert outputs["all"]["value"] == ["first"]
