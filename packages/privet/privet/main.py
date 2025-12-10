import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .nodes import load_all_specs
from .debugger import run_server_forever

app = FastAPI(title="Rivet Backend", version="0.1.0")

# Allow local dev frontends to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/nodes/specs")
def get_node_specs():
    """Return the list of all node specs available on the backend."""
    return load_all_specs()


# Start the remote debugger WS server (ws://localhost:21888) alongside FastAPI
ws_task: asyncio.Task | None = None


@app.on_event("startup")
async def _start_ws_server():
    global ws_task
    loop = asyncio.get_event_loop()
    ws_task = loop.create_task(run_server_forever())


@app.on_event("shutdown")
async def _stop_ws_server():
    global ws_task
    if ws_task is not None:
        ws_task.cancel()
        try:
            await ws_task
        except asyncio.CancelledError:
            pass
