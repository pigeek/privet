from __future__ import annotations

from typing import Any, Dict

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

class ExtractObjectPathSchema(NodeSchema):
    NODE_TYPE = 'extractObjectPath'
    TITLE = 'Extract Object Path'
    DISPLAY_NAME = 'Extract Object Path'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Objects']
    UI_INFOBOX_TITLE = 'Extract Object Path Node'
    UI_INFOBOX_BODY = 'Extracts the value at the specified JSONPath from the input object.'
    UI_CONTEXT_MENU_TITLE = 'Extract Object Path'
    DATA = {'path': '$', 'usePathInput': False}
    EDITORS = [{'type': 'code', 'label': 'Path', 'dataKey': 'path', 'language': 'jsonpath', 'useInputToggleDataKey': 'usePathInput'}]
    BODY = '{{#if usePathInput}}(Using Input){{#else}}{{path}}{{/if}}'

    INPUTS = [
        Input(
            id='object',
            data_type='object',
            title='Object',
            required=True,
        ),
        Input(
            id='path',
            data_type='string',
            title='Path',
            show_if=Eq(data_key='usePathInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='match',
            data_type='any',
            title='Match',
        ),
        Output(
            id='all_matches',
            data_type='any[]',
            title='All Matches',
        ),
    ]



@bindschema(schema=ExtractObjectPathSchema)
class ExtractObjectPathNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        input_object = coerce_type_optional(inputs.get("object"), "object")
        if input_object is None:
            input_object = {}
        input_path = data.get("path", "$")
        if data.get("usePathInput"):
            raw_path = inputs.get("path")
            input_path = coerce_type_optional(raw_path, "string") or input_path

        if not input_path:
            raise ValueError("Path input is not provided")

        matches = []
        try:
            try:
                from jsonpath_ng import parse  # type: ignore
            except Exception as e:
                raise RuntimeError("jsonpath_ng is required for ExtractObjectPath; install via pip install jsonpath-ng") from e

            try:
                expr = parse(str(input_path).strip())
                results = expr.find(input_object)
                matches = [r.value for r in results]
            except Exception:
                matches = []
        except Exception:
            matches = []

        print(f"[ExtractObjectPath] node={self.node.id} path={input_path} input={input_object} matches={matches}")

        if not matches:
            return {
                "match": {"type": "control-flow-excluded", "value": None},
                "all_matches": {"type": "any[]", "value": []},
            }

        return {
            "match": {"type": "any", "value": matches[0]},
            "all_matches": {"type": "any[]", "value": matches},
        }
