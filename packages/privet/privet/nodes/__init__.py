import importlib
import pkgutil
from typing import Any, Dict, List

def load_all_specs() -> List[Dict[str, Any]]:
    specs: List[Dict[str, Any]] = []
    package = __name__
    for _, module_name, is_pkg in pkgutil.iter_modules(__path__):  # type: ignore[name-defined]
        if is_pkg:
            continue
        mod = importlib.import_module(f"{package}.{module_name}")
        if hasattr(mod, "SPEC"):
            spec = getattr(mod, "SPEC")
            if isinstance(spec, dict):
                specs.append(spec)
    return specs

