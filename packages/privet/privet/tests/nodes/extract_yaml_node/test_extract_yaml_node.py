from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_extract_yaml_node_with_jsonpath(debugger_server_port: int):
    project_path = fixture_path("nodes/extract_yaml_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    text = """some text
yamlDocument:
  settings:
    name: Rivet
    version: 1
"""
    events = await run_graph_via_ws(debugger_server_port, project, {"input": {"type": "string", "value": text}})
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    # Output is the first jsonpath match (with root property applied)
    assert outputs["output"]["value"] == "Rivet"
    assert outputs["matches"]["value"] == ["Rivet"]
    no_match = outputs.get("noMatch")
    if no_match is not None:
        assert no_match["type"] == "control-flow-excluded"
