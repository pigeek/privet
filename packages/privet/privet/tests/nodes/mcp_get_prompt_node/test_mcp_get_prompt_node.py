from __future__ import annotations

import pytest

from privet.tests.conftest import run_graph_via_ws
from privet.tests.nodes.utils import fixture_path, load_rivet_project


@pytest.mark.asyncio
async def test_mcp_get_prompt(debugger_server_port: int):
    project = load_rivet_project(fixture_path("nodes/mcp_get_prompt_node/graphs/basic.rivet-project"))
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "promptName": {"type": "string", "value": "greeting"},
            "promptArguments": {"type": "object", "value": {"user": "Rivet"}},
            "serverUrl": {"type": "string", "value": "http://localhost:9001/mcp"},
            "name": {"type": "string", "value": "client"},
            "version": {"type": "string", "value": "1.0"},
        },
    )

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}

    prompt = outputs["prompt"]["value"]
    assert prompt["name"] == "greeting"
    assert prompt["arguments"]["user"] == "Rivet"
    assert prompt["serverUrl"] == "http://localhost:9001/mcp"
    assert prompt["client"]["name"] == "client"
