from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_read_all_files_node(debugger_server_port: int):
    project_path = fixture_path("nodes/read_all_files_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    base_dir = fixture_path("nodes/read_all_files_node/fixtures")
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {"path": {"type": "string", "value": base_dir}},
    )

    normalized = normalize_events(events)
    assert normalized[0:2] == [
        {"message": "start"},
        {"message": "graphStart", "graphId": "main"},
    ]
    assert normalized[-1]["message"] == "done"

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    files = outputs["out"]["value"]
    assert sorted([f["path"] for f in files]) == sorted(["fileA.txt", "fileB.md"])
    assert any(f["content"].strip() == "file one" for f in files)
    assert any(f["content"].strip() == "more text" for f in files)
