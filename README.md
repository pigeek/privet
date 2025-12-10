PRivet (Python Rivet)

Overview
- PRivet is a fork of the Rivet project: https://github.com/Ironclad/rivet
- Goal: migrate all execution/runtime logic to Python, while the editor/UI remains TypeScript. The UI consumes declarative, JSON‑friendly node specs; execution happens in a separate Python runtime.

What Changes Here
- Schema‑first nodes: node definitions are declarative data (no functions) so the UI can render without executing TypeScript.
- Remote execution: node `process()` is handled by a Python backend/runtime. The UI only renders and edits graphs.
- Backend (Python): FastAPI service under `backend/` will expose node specs and orchestrate execution.
- Frontend (TypeScript): continues to provide the editor and visualization, driven entirely by the schema.

Status
- This repository is under active refactor to decouple visualization (TS) from execution (Python).
- Expect changes to node registration, spec loading, and runtime bridges as the Python path solidifies.

Attribution
- This is a fork of the Rivet project by Ironclad: https://github.com/Ironclad/rivet
- License and original notices remain as in the upstream project.

Notes
- All prior contributor badges, lists, and upstream marketing/download sections have been removed here to avoid confusion. Please refer to the upstream repository for the full project history and acknowledgements.

