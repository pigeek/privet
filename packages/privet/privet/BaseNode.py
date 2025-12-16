from __future__ import annotations

from typing import Dict, Any, Type, ClassVar, Callable

from .graph.types import ChartNode


class BaseNode:
    """
    Base class for Python-side nodes.

    Default process() prints the class name and node id so that running a graph
    provides a visible traversal without performing real execution.
    """

    # Global registry mapping node type -> implementation class
    registry: ClassVar[Dict[str, Type["BaseNode"]]] = {}
    NODE_TYPE: ClassVar[str | None] = None  # Deprecated: type comes from SCHEMA when available
    SCHEMA: ClassVar[Any | None] = None

    def __init_subclass__(cls, **kwargs):  # type: ignore[override]
        super().__init_subclass__(**kwargs)
        # Prefer schema as the authority for type
        schema = getattr(cls, "SCHEMA", None)
        schema_type = getattr(schema, "NODE_TYPE", None) if schema is not None else None
        class_type = getattr(cls, "NODE_TYPE", None)

        node_type = schema_type or class_type

        # Dev-time guard for mismatches if both are set
        if schema_type and class_type and schema_type != class_type:
            print(
                f"[BaseNode] Warning: NODE_TYPE mismatch between schema ({schema_type}) and class ({class_type}) for {cls.__name__}. Using schema type."
            )

        if node_type:
            BaseNode.registry[str(node_type).lower()] = cls  # type: ignore[index]

    def __init__(self, node: ChartNode, context: Dict[str, Any] | None = None) -> None:
        self.node = node
        self.context = context or {}
        # Common helper so nodes can read configuration without repeatedly reaching into self.node
        self.data = node.data or {}

    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        print(f"Processing {self.__class__.__name__} id={self.node.id} title='{self.node.title}' type={self.node.type}")
        # No real outputs yet — return empty mapping
        return {}

    @classmethod
    def for_type(cls, type_name: str) -> Type["BaseNode"]:
        return cls.registry.get((type_name or "").lower(), cls)


def bindschema(schema: Any) -> Callable[[Type["BaseNode"]], Type["BaseNode"]]:
    """Class decorator to bind a BaseNode subclass to a schema class.

    Ensures SCHEMA is set and registers the executor in BaseNode.registry using
    the schema's NODE_TYPE, avoiding reliance on class-level NODE_TYPE and
    timing of __init_subclass__.
    """

    def _decorator(cls: Type["BaseNode"]) -> Type["BaseNode"]:
        cls.SCHEMA = schema
        node_type = getattr(schema, "NODE_TYPE", None)
        if node_type:
            BaseNode.registry[str(node_type).lower()] = cls
        return cls

    return _decorator
