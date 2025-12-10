Rivet Backend (FastAPI)

This is a minimal Python FastAPI backend that serves Rivet node specs to the frontend. The frontend fetches these specs at startup and registers them into the global node registry for UI rendering.

Run locally
- Python 3.10+
- Create a virtualenv (recommended), then install deps:
- `pip install -r requirements.txt`
- Start the server (default port 8000):
- `uvicorn privet.main:app --reload --port 8000`

API
- `GET /nodes/specs` → returns a JSON array of node specs. Each spec matches the `GenericNodeSpec` shape used by the frontend (`packages/core/src/model/nodes/GenericNode.ts`).

Node discovery
- Nodes live under `privet/nodes/` and expose a module-level `SPEC` dictionary (pure JSON-serializable data).
- At startup, the server enumerates `privet/nodes` and aggregates all `SPEC` values.

Adding nodes
- Add a file like `privet/nodes/MyNode.py` with a module-level `SPEC` variable.
- Restart the backend (or rely on `--reload`).

Notes
- Specs are purely declarative; no functions or closures.
- Execution remains remote/non-local; this backend only serves specs for the UI.
