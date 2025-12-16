from __future__ import annotations

import pytest

from privet.tests.nodes.utils import load_rivet_project, fixture_path
from privet.tests.conftest import run_graph_via_ws


@pytest.mark.asyncio
async def test_extract_markdown_code_blocks_node(debugger_server_port: int):
    project_path = fixture_path("nodes/extract_markdown_code_blocks_node/graphs/happy.rivet-project")
    project = load_rivet_project(project_path)
    md = """
Here is code:
```py
print('hi')
```
And more:
```js
console.log('ok')
```
"""
    events = await run_graph_via_ws(debugger_server_port, project, {"input": {"type": "string", "value": md}})
    done = next(ev for ev in events if ev.get("message") == "done")
    outputs = (done.get("data") or {}).get("results") or {}
    assert outputs["first"]["value"].strip() == "print('hi')"
    assert outputs["all"]["value"][0].strip().startswith("print")
    assert outputs["langs"]["value"] == ["py", "js"]
