from __future__ import annotations

import hashlib

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_hash_node_sha256(debugger_server_port: int):
    project_path = fixture_path("nodes/hash_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    input_value = "hello"
    events = await run_graph_via_ws(debugger_server_port, project, {"input": {"type": "string", "value": input_value}})

    normalized = normalize_events(events)
    assert normalized[0]["message"] == "start"

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    expected = hashlib.sha256(input_value.encode("utf-8")).hexdigest()
    assert outputs["out"] == {"type": "string", "value": expected}
