from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_document_node(debugger_server_port: int):
    project_path = fixture_path("nodes/document_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(debugger_server_port, project, {})

    normalized = normalize_events(events)
    assert normalized[-1]["message"] == "done"

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    doc = outputs["out"]
    assert doc["type"] == "document"
    assert doc["value"]["title"] == "Sample"
    assert doc["value"]["data"] in (
        {"type": "string", "value": "body text"},
        "body text",
    )
