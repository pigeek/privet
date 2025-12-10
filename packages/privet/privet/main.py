from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .nodes import load_all_specs

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

