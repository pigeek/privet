from __future__ import annotations

from typing import Any, Dict, List
import re

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import (
    Input,
    VariadicInput,
    Output,
    Eq,
    All,
    Any_,
    RawShowIf,
    NodeSchema,
)
from ..utils import coerce_type_optional

class ToTreeSchema(NodeSchema):
    NODE_TYPE = 'toTree'
    TITLE = 'To Tree'
    DISPLAY_NAME = 'To Tree'
    VISUAL_WIDTH = 300
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'To Tree Node'
    UI_INFOBOX_BODY = 'Converts an array of objects into a tree and renders it as text.'
    UI_CONTEXT_MENU_TITLE = 'To Tree'
    DATA = {'format': '{{path}}', 'childrenProperty': 'children', 'useSortAlphabetically': True}
    EDITORS = [{'type': 'string', 'label': 'Children Property', 'dataKey': 'childrenProperty'}, {'type': 'code', 'label': 'Format', 'dataKey': 'format', 'language': 'prompt-interpolation-markdown', 'theme': 'prompt-interpolation'}, {'type': 'toggle', 'label': 'Sort Alphabetically', 'dataKey': 'useSortAlphabetically'}]
    BODY = 'Format: {{format}}\nChildren: {{childrenProperty}}\nSort: {{#if useSortAlphabetically}}Yes{{#else}}No{{/if}}'

    INPUTS = [
        Input(
            id='objects',
            data_type=['object[]', 'object'],
            title='Objects',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='tree',
            data_type='string',
            title='Tree',
        ),
    ]



@bindschema(schema=ToTreeSchema)
class ToTreeNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        objects_val = coerce_type_optional(inputs.get("objects"), "object[]")
        objects: List[Dict[str, Any]] = []
        if isinstance(objects_val, list):
            objects = objects_val  # type: ignore[assignment]
        elif isinstance(objects_val, dict):
            objects = [objects_val]  # type: ignore[list-item]

        fmt = data.get("format", "{{path}}")
        children_key = data.get("childrenProperty", "children")
        sort_alpha = bool(data.get("useSortAlphabetically", True))

        tokens = re.findall(r"\{\{([^}]+)\}\}", fmt)

        def get_path(obj: Dict[str, Any], path: str, default: Any = "") -> Any:
            current: Any = obj
            for part in path.split("."):
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return default
            return current

        def format_node(obj: Dict[str, Any]) -> str:
            def _replace(match: re.Match[str]) -> str:
                key = match.group(1).strip()
                return str(get_path(obj, key, ""))

            return re.sub(r"\{\{([^}]+)\}\}", _replace, fmt)

        def build_tree(objs: List[Dict[str, Any]], level: int = 0) -> str:
            if not objs:
                return ""
            local = sorted(objs, key=lambda o: str(get_path(o, "path", ""))) if sort_alpha else objs
            lines: List[str] = []
            for idx, obj in enumerate(local):
                is_last = idx == len(local) - 1
                prefix = "" if level == 0 else ("└── " if is_last else "├── ")
                indent = "" if level == 0 else ("    " * (level - 1) + ("    " if is_last else "│   "))
                label = format_node(obj)
                lines.append(f"{indent}{prefix}{label}")

                children = get_path(obj, children_key, [])
                if isinstance(children, list) and children:
                    child_str = build_tree(children, level + 1)
                    if child_str:
                        lines.append(child_str)
            return "\n".join(lines)

        tree_text = build_tree(objects)

        return {"tree": {"type": "string", "value": tree_text}}
