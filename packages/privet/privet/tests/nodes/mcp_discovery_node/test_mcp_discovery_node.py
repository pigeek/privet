from __future__ import annotations

import pytest

from privet.tests.conftest import run_graph_via_ws
from privet.tests.nodes.utils import fixture_path, load_rivet_project


@pytest.mark.asyncio
async def test_mcp_discovery_outputs(debugger_server_port: int):
    project = load_rivet_project(fixture_path("nodes/mcp_discovery_node/graphs/basic.rivet-project"))
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "name": {"type": "string", "value": "tester"},
            "version": {"type": "string", "value": "0.1.0"},
            "serverUrl": {"type": "string", "value": "http://localhost:9000/mcp"},
        },
    )

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}

    tools = outputs["tools"]["value"]
    prompts = outputs["prompts"]["value"]

    assert tools[0]["serverUrl"] == "http://localhost:9000/mcp"
    assert prompts[0]["transportType"] == "http"
    assert tools[0]["client"]["name"] == "tester"
