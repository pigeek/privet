from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_extract_json_node_parses_object(debugger_server_port: int):
    project_path = fixture_path("nodes/extract_json_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    text = "prefix {\"a\":1} suffix"
    events = await run_graph_via_ws(debugger_server_port, project, {"input": {"type": "string", "value": text}})
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["output"]["value"] == {"a": 1}
    no_match = outputs.get("noMatch")
    if no_match is not None:
        assert no_match["type"] == "control-flow-excluded"
