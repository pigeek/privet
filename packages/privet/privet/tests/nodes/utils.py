from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

import yaml

# Ensure privet is importable regardless of cwd during pytest
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def load_rivet_project(path: str) -> Dict[str, Any]:
    """Load a .rivet-project YAML into a dict suitable for project_from_json.

    Translates the UI-friendly YAML structure (with node keys and outgoingConnections)
    into the backend JSON shape (graphs: {id: {metadata,nodes,connections}}).
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    data = raw.get("data") or {}

    def parse_node_key(key: str) -> tuple[str, str, str]:
        # Example: '[n1]:graphInput "Input"'
        node_id = key[key.find("[") + 1 : key.find("]")]
        rest = key[key.find("]:") + 2 :].strip()
        parts = rest.split(" ", 1)
        node_type = parts[0]
        title = ""
        if len(parts) > 1 and parts[1].startswith('"'):
            title = parts[1].strip('"')
        return node_id, node_type, title

    def parse_outgoing(node_id: str, outgoing: list[str]) -> list[Dict[str, Any]]:
        conns: list[Dict[str, Any]] = []
        for raw_conn in outgoing:
            # Format: outputId->"Target" targetNode/inputId
            try:
                lhs, rhs = raw_conn.split("->", 1)
                out_id = lhs.strip()
                rhs = rhs.strip()
                # After title, we have target info
                if '"' in rhs:
                    _, rest = rhs.split('"', 2)[1:]
                    rhs = rest.strip()
                target = rhs.split()
                target_node_and_port = target[-1]
                tgt_node, tgt_port = target_node_and_port.split("/")
                conns.append(
                    {
                        "outputNodeId": node_id,
                        "outputId": out_id,
                        "inputNodeId": tgt_node,
                        "inputId": tgt_port,
                    }
                )
            except Exception:
                continue
        return conns

    graphs_out: Dict[str, Any] = {}
    for gid, g in (data.get("graphs") or {}).items():
        metadata = g.get("metadata") or {}
        nodes_raw = g.get("nodes") or {}
        nodes_list: list[Dict[str, Any]] = []
        connections: list[Dict[str, Any]] = []
        for key, node_body in nodes_raw.items():
            node_id, node_type, title = parse_node_key(key)
            nodes_list.append(
                {
                    "id": node_id,
                    "type": node_type,
                    "title": title,
                    "data": node_body.get("data") or {},
                }
            )
            outgoing = node_body.get("outgoingConnections") or []
            connections.extend(parse_outgoing(node_id, outgoing))
        graphs_out[gid] = {"metadata": metadata, "nodes": nodes_list, "connections": connections}

    return {
        "metadata": data.get("metadata") or {},
        "graphs": graphs_out,
        "references": data.get("references"),
    }


def normalize_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for ev in events:
        msg = ev.get("message")
        data = ev.get("data") or {}
        if msg in ("start", "done", "abort", "error"):
            out.append({"message": msg})
        elif msg in ("graphStart", "graphFinish"):
            graph_meta = (data.get("graph") or {}).get("metadata") or {}
            out.append({"message": msg, "graphId": graph_meta.get("id", "")})
        elif msg in ("nodeStart", "nodeFinish"):
            node = data.get("node") or {}
            out.append({"message": msg, "node": {"id": node.get("id"), "type": node.get("type")}})
    return out


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def fixture_path(*parts: str) -> str:
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, *parts)
