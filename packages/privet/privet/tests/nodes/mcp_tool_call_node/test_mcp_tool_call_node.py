from __future__ import annotations

import pytest

from privet.tests.conftest import run_graph_via_ws
from privet.tests.nodes.utils import fixture_path, load_rivet_project


@pytest.mark.asyncio
async def test_mcp_tool_call(debugger_server_port: int):
    project = load_rivet_project(fixture_path("nodes/mcp_tool_call_node/graphs/basic.rivet-project"))
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "toolName": {"type": "string", "value": "compute"},
            "toolArguments": {"type": "object", "value": {"a": 1, "b": 2}},
            "toolCallId": {"type": "string", "value": "call-123"},
            "serverUrl": {"type": "string", "value": "http://localhost:9002/mcp"},
            "name": {"type": "string", "value": "tool-client"},
            "version": {"type": "string", "value": "2.0"},
        },
    )

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}

    response = outputs["response"]["value"]
    assert response["name"] == "compute"
    assert response["arguments"]["a"] == 1
    assert response["serverUrl"] == "http://localhost:9002/mcp"
    assert response["client"]["name"] == "tool-client"

    tool_call_id = outputs["toolCallIdOut"]["value"]
    assert tool_call_id == "call-123"
