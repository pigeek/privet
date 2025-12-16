from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_http_call_node(debugger_server_port: int):
    project_path = fixture_path("nodes/http_call_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(debugger_server_port, project, {})

    normalized = normalize_events(events)
    assert normalized[-1]["message"] == "done"

    http_finish = next(ev for ev in events if ev.get("message") == "nodeFinish")
    outputs = (http_finish.get("data") or {}).get("outputs") or {}
    status = outputs.get("statusCode", {}).get("value")

    assert status is not None
    if status == 0:
        # Network error path: explicit error message returned
        assert "HTTP request failed" in outputs["res_body"]["value"]
        assert "error" in outputs["json"]["value"]
    else:
        # Success path: got a response body
        assert outputs["res_body"]["type"] == "string"
