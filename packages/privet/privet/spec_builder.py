from __future__ import annotations

from dataclasses import is_dataclass, fields as dc_fields, MISSING, field as dc_field
from typing import Any, Dict, List, Optional, Union, ClassVar, Type


# ----- ShowIf DSL -----
class Eq:
    def __init__(self, data_key: str, equals: Any):
        self.data_key = data_key
        self.equals = equals

    def to_spec(self) -> Dict[str, Any]:
        return {"dataKey": self.data_key, "equals": self.equals}


class All:
    def __init__(self, conditions: List[Union["Eq", "All", "Any"]]):
        self.conditions = conditions

    def to_spec(self) -> Dict[str, Any]:
        return {"all": [c.to_spec() for c in self.conditions]}


class Any_:
    def __init__(self, conditions: List[Union["Eq", "All", "Any_"]]):
        self.conditions = conditions

    def to_spec(self) -> Dict[str, Any]:
        return {"any": [c.to_spec() for c in self.conditions]}


class RawShowIf:
    """Passthrough showIf wrapper for shapes not yet modeled in the DSL."""

    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw

    def to_spec(self) -> Dict[str, Any]:
        return self.raw


ShowIf = Union[Eq, All, Any_, RawShowIf]


# ----- Port descriptors -----
class Input:
    def __init__(
        self,
        id: str,
        data_type: Union[str, List[str]],
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        data_type_from: Optional[Dict[str, Any]] = None,
        show_if: Optional[ShowIf] = None,
        required: Optional[bool] = None,
        coerced: Optional[bool] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.id = id
        self.data_type = data_type
        self.title = title
        self.description = description
        self.data_type_from = data_type_from
        self.show_if = show_if
        self.required = required
        self.coerced = coerced
        self.extra = extra or {}

    def to_spec(self) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"id": self.id, "dataType": self.data_type}
        if self.title is not None:
            spec["title"] = self.title
        if self.description is not None:
            spec["description"] = self.description
        if self.data_type_from is not None:
            spec["dataTypeFrom"] = self.data_type_from
        if self.show_if is not None:
            spec["showIf"] = self.show_if.to_spec()
        if self.required is not None:
            spec["required"] = self.required
        if self.coerced is not None:
            spec["coerced"] = self.coerced
        spec.update(self.extra)
        return spec


class VariadicInput:
    def __init__(
        self,
        base_id: str,
        data_type: Union[str, List[str]],
        *,
        title: str,
        title_pattern: str,
        start_at: int = 1,
        min: int = 1,
        id_pattern: Optional[str] = None,
        description: Optional[str] = None,
        id_value: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
        variadic_extra: Optional[Dict[str, Any]] = None,
    ):
        self.id_value = id_value
        self.base_id = base_id
        self.data_type = data_type
        self.title = title
        self.title_pattern = title_pattern
        self.start_at = start_at
        self.min = min
        self.id_pattern = id_pattern
        self.description = description
        self.extra = extra or {}
        self.variadic_extra = variadic_extra or {}

    def to_spec(self) -> Dict[str, Any]:
        variadic: Dict[str, Any] = {
            "baseId": self.base_id,
            "titlePattern": self.title_pattern,
            "startAt": self.start_at,
            "min": self.min,
        }
        if self.id_pattern:
            variadic["idPattern"] = self.id_pattern
        if self.variadic_extra:
            variadic.update(self.variadic_extra)
        spec: Dict[str, Any] = {
            "id": self.id_value or self.base_id,
            "title": self.title,
            "dataType": self.data_type,
            "variadic": variadic,
        }
        if self.description is not None:
            spec["description"] = self.description
        spec.update(self.extra)
        return spec


class Output:
    def __init__(
        self,
        id: str,
        data_type: Union[str, List[str]],
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        data_type_from: Optional[Dict[str, Any]] = None,
        show_if: Optional[ShowIf] = None,
        variadic: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.id = id
        self.data_type = data_type
        self.title = title
        self.description = description
        self.data_type_from = data_type_from
        self.show_if = show_if
        self.variadic = variadic
        self.extra = extra or {}

    def to_spec(self) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"id": self.id, "dataType": self.data_type}
        if self.title is not None:
            spec["title"] = self.title
        if self.description is not None:
            spec["description"] = self.description
        if self.data_type_from is not None:
            spec["dataTypeFrom"] = self.data_type_from
        if self.show_if is not None:
            spec["showIf"] = self.show_if.to_spec()
        if self.variadic is not None:
            spec["variadic"] = self.variadic
        spec.update(self.extra)
        return spec


# ----- Spec builder -----
class EditorBase:
    def __init__(self, label: str, *, show_if: Optional[ShowIf] = None) -> None:
        self.label = label
        self.show_if = show_if

    def to_spec(self, data_key: str) -> Dict[str, Any]:  # pragma: no cover - abstract-ish
        raise NotImplementedError


class Toggle(EditorBase):
    def to_spec(self, data_key: str) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"type": "toggle", "label": self.label, "dataKey": data_key}
        if self.show_if:
            spec["showIf"] = self.show_if.to_spec()
        return spec


class Code(EditorBase):
    def __init__(
        self,
        label: str,
        *,
        language: str = "plaintext",
        use_input_toggle: Optional[str] = None,
        show_if: Optional[ShowIf] = None,
    ) -> None:
        super().__init__(label, show_if=show_if)
        self.language = language
        self.use_input_toggle = use_input_toggle

    def to_spec(self, data_key: str) -> Dict[str, Any]:
        spec: Dict[str, Any] = {
            "type": "code",
            "label": self.label,
            "dataKey": data_key,
            "language": self.language,
        }
        if self.use_input_toggle:
            spec["useInputToggleDataKey"] = self.use_input_toggle
        if self.show_if:
            spec["showIf"] = self.show_if.to_spec()
        return spec


def Editor(editor: EditorBase, *, default: Any = MISSING):
    """Helper to declare a dataclass field with an attached Editor descriptor.

    Usage:
      name: str = Editor(Code('Name'), default='')
    """
    return dc_field(default=default, metadata={"editor": editor})

def _build_data_and_editors_from_config(config_cls: Any) -> (Dict[str, Any], List[Dict[str, Any]]):
    data: Dict[str, Any] = {}
    editors: List[Dict[str, Any]] = []
    if not config_cls or not is_dataclass(config_cls):
        return data, editors

    for f in dc_fields(config_cls):
        # default value
        default = f.default if f.default is not MISSING else None
        data_key = f.name
        data[data_key] = default
        meta = dict(f.metadata or {})
        editor_meta = meta.get("editor")
        if editor_meta:
            # New path: typed Editor instance
            if isinstance(editor_meta, EditorBase):
                editors.append(editor_meta.to_spec(data_key))
            else:
                # Legacy path: string-based with extras in metadata
                editor_type = editor_meta
                ed: Dict[str, Any] = {"type": editor_type, "label": meta.get("label", data_key), "dataKey": data_key}
                # Map extra hints
                if "use_input_toggle" in meta:
                    ed["useInputToggleDataKey"] = meta["use_input_toggle"]
                if "show_if" in meta:
                    show_if = meta["show_if"]
                    try:
                        ed["showIf"] = show_if.to_spec()  # type: ignore[attr-defined]
                    except Exception:
                        pass
                if "language" in meta:
                    ed["language"] = meta["language"]
                if "description" in meta:
                    ed["description"] = meta["description"]
                editors.append(ed)
    return data, editors


def build_spec_from_class(node_cls: Any) -> Dict[str, Any]:
    node_type = getattr(node_cls, "NODE_TYPE", None)
    title = getattr(node_cls, "TITLE", node_type)
    display_name = getattr(node_cls, "DISPLAY_NAME", title)
    visual_width = getattr(node_cls, "VISUAL_WIDTH", 150)
    ui_group = getattr(node_cls, "UI_GROUP", [])
    info_box_title = getattr(node_cls, "UI_INFOBOX_TITLE", title + " Node")
    info_box_body = getattr(node_cls, "UI_INFOBOX_BODY", "")
    context_menu_title = getattr(node_cls, "UI_CONTEXT_MENU_TITLE", title)
    body = getattr(node_cls, "BODY", None)

    inputs_desc: List[Any] = getattr(node_cls, "INPUTS", [])
    outputs_desc: List[Any] = getattr(node_cls, "OUTPUTS", [])

    inputs: List[Dict[str, Any]] = []
    for d in inputs_desc:
        inputs.append(d.to_spec())

    outputs: List[Dict[str, Any]] = []
    for d in outputs_desc:
        outputs.append(d.to_spec())

    config_cls = getattr(node_cls, "Config", None)
    data, editors = _build_data_and_editors_from_config(config_cls)

    if not data:
        data = dict(getattr(node_cls, "DATA", {}) or {})
    if not editors:
        editors = list(getattr(node_cls, "EDITORS", []) or [])

    spec: Dict[str, Any] = {
        "type": node_type,
        "title": title,
        "displayName": display_name,
        "data": data,
        "visual": {"width": visual_width},
        "uiData": {
            "infoBoxBody": info_box_body,
            "infoBoxTitle": info_box_title,
            "contextMenuTitle": context_menu_title,
            "group": ui_group,
        },
        "inputs": inputs,
        "outputs": outputs,
    }

    if editors:
        spec["editors"] = editors
    if body is not None:
        spec["body"] = body

    return spec


def diff_specs(a: Dict[str, Any], b: Dict[str, Any], path: str = "") -> List[str]:
    diffs: List[str] = []
    a_keys = set(a.keys())
    b_keys = set(b.keys())
    for key in sorted(a_keys | b_keys):
        p = f"{path}.{key}" if path else key
        if key not in a:
            diffs.append(f"Missing in A: {p}")
            continue
        if key not in b:
            diffs.append(f"Missing in B: {p}")
            continue
        va, vb = a[key], b[key]
        if isinstance(va, dict) and isinstance(vb, dict):
            diffs.extend(diff_specs(va, vb, p))
        elif isinstance(va, list) and isinstance(vb, list):
            if len(va) != len(vb):
                diffs.append(f"Len mismatch at {p}: {len(va)} != {len(vb)}")
            else:
                for i, (ia, ib) in enumerate(zip(va, vb)):
                    ip = f"{p}[{i}]"
                    if isinstance(ia, dict) and isinstance(ib, dict):
                        diffs.extend(diff_specs(ia, ib, ip))
                    elif ia != ib:
                        diffs.append(f"Value mismatch at {ip}: {ia!r} != {ib!r}")
        else:
            if va != vb:
                diffs.append(f"Value mismatch at {p}: {va!r} != {vb!r}")
    return diffs


# ----- Schema registry -----
class NodeSchema:
    """Base class for declarative node schemas (UI/spec only)."""

    registry: ClassVar[Dict[str, Type["NodeSchema"]]] = {}
    NODE_TYPE: ClassVar[str]
    EXPORT_TO_SPEC: ClassVar[bool] = True  # allow executor-only nodes to opt out of export

    def __init_subclass__(cls, **kwargs):  # type: ignore[override]
        super().__init_subclass__(**kwargs)
        node_type = getattr(cls, "NODE_TYPE", None)
        if node_type:
            NodeSchema.registry[node_type] = cls

    @classmethod
    def build_spec(cls) -> Dict[str, Any]:
        return build_spec_from_class(cls)
