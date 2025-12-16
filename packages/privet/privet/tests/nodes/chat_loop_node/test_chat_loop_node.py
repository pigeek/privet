from __future__ import annotations

import pytest

from privet.tests.conftest import run_graph_via_ws
from privet.tests.nodes.utils import fixture_path, load_rivet_project


@pytest.mark.asyncio
async def test_chat_loop_conversation(debugger_server_port: int):
    project = load_rivet_project(fixture_path("nodes/chat_loop_node/graphs/basic.rivet-project"))
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "prompt": {"type": "string", "value": "How are you?"},
            "systemPrompt": {"type": "string", "value": "Be brief"},
        },
    )

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}

    conversation = outputs["conversation"]["value"]
    assert conversation[0].startswith("system:")
    assert any("How are you?" in part for part in conversation)

    last = outputs["last"]["value"]
    assert "How are you?" in last
    assert last.startswith("Reply with:")
