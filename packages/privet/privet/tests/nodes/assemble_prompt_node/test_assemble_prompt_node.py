from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_assemble_prompt_node(debugger_server_port: int):
    project_path = fixture_path("nodes/assemble_prompt_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "m1": {"type": "chat-message", "value": {"type": "user", "message": "hi"}},
            "m2": {"type": "chat-message", "value": {"type": "assistant", "message": "yo"}},
            "m3": {"type": "chat-message", "value": {"type": "system", "message": "note"}},
        },
    )
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    prompt = outputs["prompt"]["value"]
    assert len(prompt) == 3
    assert prompt[-1].get("isCacheBreakpoint") is True
    assert outputs["tokenCount"]["value"] == 3
