from __future__ import annotations

from typing import Any, Dict
import json

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None

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

class ToYAMLSchema(NodeSchema):
    NODE_TYPE = 'toYaml'
    TITLE = 'To YAML'
    DISPLAY_NAME = 'To YAML'
    VISUAL_WIDTH = 175
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'To YAML Node'
    UI_INFOBOX_BODY = 'Turns the input object into YAML text.'
    UI_CONTEXT_MENU_TITLE = 'To YAML'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='object',
            data_type='object',
            title='Object',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='yaml',
            data_type='string',
            title='YAML',
        ),
    ]



@bindschema(schema=ToYAMLSchema)
class ToYAMLNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        obj = inputs.get("object")
        raw = obj.get("value") if isinstance(obj, dict) else obj

        if yaml:
            try:
                yaml_str = yaml.dump(raw, allow_unicode=False, default_flow_style=False, sort_keys=False)
            except Exception:
                yaml_str = json.dumps(raw, indent=2)
        else:
            yaml_str = json.dumps(raw, indent=2)

        return {"yaml": {"type": "string", "value": yaml_str}}
