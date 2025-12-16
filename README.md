# PRivet (Python Rivet)

PRivet is a fork of Rivet focused on running the full graph executor in Python while keeping the TypeScript UI. The UI still consumes declarative specs; execution now happens in `packages/privet` via a WebSocket endpoint that mirrors the UI’s flow.

## Current Status
- All nodes ported to Python with WS-driven tests (85/85 passing under `packages/privet/privet/tests/nodes`). Tests load UI-format `.rivet-project` graphs and talk to the same backend WS endpoint as the UI.
- Chat nodes: real OpenAI-compatible chat calls when `OPENAI_API_KEY` is set; deterministic fallback (including tool-calls) when no key is present.
- MCP nodes: real MCP HTTP and stdio support. HTTP uses the provided `serverUrl`; stdio spawns the configured server from project metadata. Synthetic fallback remains for offline runs.
- Subgraph, loop, dataset/vector store, text/object/array transforms, control-flow, and utility nodes all execute in Python with parity-focused behavior.

## How to Run
- Backend: `cd packages/privet && uvicorn privet.main:app --reload --port 8000` (WS at `ws://localhost:21888`).
- Tests: `cd packages/privet && pytest privet/tests/nodes`.
- The UI (TypeScript) connects to the same WS endpoint; configure via Settings → Remote Debugger Server URL.

## MCP Configuration (stdio)
For stdio MCP, include server definitions in project metadata (mirrors TS):
```yaml
metadata:
  mcpServer:
    mcpServers:
      myServer:
        command: "path/to/server"
        args: ["--flag"]
        env: { KEY: "value" }
        cwd: "/path"
```
Set `transportType: stdio` and `serverId: myServer` on MCP nodes. HTTP transport uses `serverUrl`.

## Notes
- Repo is under active refactor; execution logic lives in `packages/privet`. Avoid editing generated node specs in the UI.
- Default behavior prefers real services (OpenAI/MCP) when credentials/servers exist; fallbacks keep tests runnable offline.
