from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, normalize_events, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_dataset_nearest_neighbors_node(debugger_server_port: int):
    project_path = fixture_path("nodes/dataset_nearest_neighbors_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "vector": {"type": "vector", "value": [1, 0, 0]},
            "vector1": {"type": "vector", "value": [5, 0, 0]},
            "embedding": {"type": "vector", "value": [0, 0, 0]},
            "data": {"type": "string[]", "value": ["rowA"]},
            "data1": {"type": "string[]", "value": ["rowB"]},
        },
    )

    normalized = normalize_events(events)
    assert normalized[-1]["message"] == "done"

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    nn = outputs["out"]["value"]
    assert nn and nn[0]["row"]["id"] == "0"
