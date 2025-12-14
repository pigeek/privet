import importlib
import os
from types import ModuleType
from typing import Any, Dict, List

from ..spec_builder import NodeSchema

# Import all node modules to trigger registration via BaseNode.__init_subclass__
# Keep imports lazy to avoid side effects when unused; for registry/spec loading we
# import every file in this package.
def _iter_node_modules() -> List[ModuleType]:
    modules: List[ModuleType] = []
    pkg_dir = os.path.dirname(__file__)
    pkg_name = __name__
    for filename in os.listdir(pkg_dir):
        if not filename.endswith('.py'):
            continue
        if filename in ('__init__.py',):
            continue
        modname = filename[:-3]
        try:
            modules.append(importlib.import_module(f"{pkg_name}.{modname}"))
        except Exception:
            # Ignore modules that fail to import; continue loading others
            continue
    return modules


# Ensure registry is populated on import
_iter_node_modules()


def load_all_specs() -> List[Dict[str, Any]]:
    """Discover and collect generated node specs from all registered schema classes."""
    _iter_node_modules()  # ensure modules are imported and schemas registered
    specs: List[Dict[str, Any]] = []
    for node_type, schema_cls in sorted(NodeSchema.registry.items()):
        if not getattr(schema_cls, "EXPORT_TO_SPEC", True):
            continue
        try:
            specs.append(schema_cls.build_spec())
        except Exception:
            continue
    return specs
