from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TypedDict


class DataValue(TypedDict, total=False):
    # Minimal structure; passthrough for UI data
    type: str
    # Arbitrary payload depending on type
    # Using Any to keep flexibility with existing JSON
    value: Any


NodeId = str
PortId = str
GraphId = str


@dataclass
class NodeConnection:
    inputNodeId: NodeId
    inputId: PortId
    outputNodeId: NodeId
    outputId: PortId


@dataclass
class ChartNode:
    id: NodeId
    type: str
    title: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NodeGraph:
    metadata: Dict[str, Any]
    nodes: List[ChartNode]
    connections: List[NodeConnection]


@dataclass
class ProjectMetadata:
    id: str
    name: str
    mainGraphId: Optional[GraphId] = None


@dataclass
class Project:
    metadata: ProjectMetadata
    graphs: Dict[GraphId, NodeGraph]
    references: Optional[List[Dict[str, Any]]] = None


def project_from_json(payload: Dict[str, Any]) -> Project:
    meta = payload.get("metadata") or {}
    metadata = ProjectMetadata(
        id=meta.get("id") or "",
        name=meta.get("name") or "",
        mainGraphId=meta.get("mainGraphId"),
    )

    def _node_from_json(n: Dict[str, Any]) -> ChartNode:
        # Accept unknown keys by ignoring them
        return ChartNode(
            id=n.get("id", ""),
            type=n.get("type", ""),
            title=n.get("title", ""),
            data=n.get("data") or {},
        )

    def _conn_from_json(c: Dict[str, Any]) -> NodeConnection:
        return NodeConnection(
            inputNodeId=c.get("inputNodeId", ""),
            inputId=c.get("inputId", ""),
            outputNodeId=c.get("outputNodeId", ""),
            outputId=c.get("outputId", ""),
        )

    raw_graphs: Dict[str, Any] = payload.get("graphs") or {}
    graphs: Dict[GraphId, NodeGraph] = {}
    for gid, g in raw_graphs.items():
        nodes = [_node_from_json(n) for n in g.get("nodes", [])]
        connections = [_conn_from_json(c) for c in g.get("connections", [])]
        graphs[gid] = NodeGraph(metadata=g.get("metadata") or {}, nodes=nodes, connections=connections)

    return Project(metadata=metadata, graphs=graphs, references=payload.get("references"))
