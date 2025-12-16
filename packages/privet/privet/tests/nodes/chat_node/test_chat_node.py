from __future__ import annotations

import pytest

from privet.tests.conftest import run_graph_via_ws
from privet.tests.nodes.utils import fixture_path, load_rivet_project


@pytest.mark.asyncio
async def test_chat_node_basic(debugger_server_port: int):
    project = load_rivet_project(fixture_path("nodes/chat_node/graphs/basic.rivet-project"))
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {"prompt": {"type": "string", "value": "Hello Rivet"}},
    )

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}

    resp = outputs["resp"]
    assert resp["type"] == "string"
    assert "Hello Rivet" in resp["value"]

    messages = outputs["messages"]["value"]
    assert messages[0]["message"] == "Hello Rivet"
    assert messages[-1]["type"] == "assistant"


@pytest.mark.asyncio
async def test_chat_node_function_calls(debugger_server_port: int):
    project = load_rivet_project(fixture_path("nodes/chat_node/graphs/function_calls.rivet-project"))
    funcs = [
        {"name": "do_a", "description": "A"},
        {"name": "do_b", "description": "B"},
    ]
    events = await run_graph_via_ws(
        debugger_server_port,
        project,
        {
            "prompt": {"type": "string", "value": "use tools"},
            "functions": {"type": "object[]", "value": funcs},
        },
    )

    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}

    resp = outputs["resp"]
    assert resp["type"] == "string[]"
    assert len(resp["value"]) == 2

    calls = outputs["calls"]["value"]
    assert len(calls) == 2
    assert {c["function"]["name"] for c in calls} == {"do_a", "do_b"}
