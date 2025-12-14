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
from ..utils import coerce_type_optional, unwrap_data_value

class TextSchema(NodeSchema):
    NODE_TYPE = 'text'
    TITLE = 'Text'
    DISPLAY_NAME = 'Text'
    VISUAL_WIDTH = 300
    UI_GROUP = ['Common', 'Text']
    UI_INFOBOX_TITLE = 'Text Node'
    UI_INFOBOX_BODY = 'Outputs a string of text. It can also interpolate values using {{tags}}.\n\nThe inputs are dynamic based on the interpolation tags.'
    UI_CONTEXT_MENU_TITLE = 'Text'
    DATA = {'text': '{{input}}', 'normalizeLineEndings': True}
    EDITORS = [{'type': 'custom', 'label': 'AI Assist', 'customEditorId': 'TextNodeAiAssist'}, {'type': 'code', 'label': 'Text', 'dataKey': 'text', 'language': 'prompt-interpolation-markdown', 'theme': 'prompt-interpolation'}, {'type': 'toggle', 'label': 'Normalize Line Endings', 'dataKey': 'normalizeLineEndings'}]
    BODY = {'type': 'colorized', 'language': 'prompt-interpolation-markdown', 'theme': 'prompt-interpolation', 'text': '{{text}}'}

    INPUTS = [
        VariadicInput(
            base_id='',
            id_value='input',
            data_type='string',
            title='Input {key}',
            title_pattern='{key}',
            start_at=0,
            min=0,
            variadic_extra={
                "type": "interpolation",
                "dataKey": "text",
                "baseId": "",
                "titlePattern": "{key}",
                "ignorePrefixes": ["@graphInputs.", "@context."],
            },
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='string',
            title='Output',
        ),
    ]



@bindschema(schema=TextSchema)
class TextNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import re

        inputs = inputs or {}
        data = self.node.data or {}

        # Map inputs to strings
        str_inputs: Dict[str, str] = {}
        for key, val in inputs.items():
            coerced = coerce_type_optional(val, "string")
            str_inputs[key] = coerced if coerced is not None else ""

        graph_inputs = (self.context or {}).get("graph_input_node_values", {})
        context_values = (self.context or {}).get("context_values", {})

        def _resolve_key(key: str) -> str:
            key = key.strip()
            if key.startswith("@graphInputs."):
                raw = graph_inputs.get(key[len("@graphInputs.") :])
                return str(unwrap_data_value(raw) or "")
            if key.startswith("@context."):
                raw = context_values.get(key[len("@context.") :])
                return str(unwrap_data_value(raw) or "")
            return str_inputs.get(key, "")

        text = data.get("text", "")

        def _replace(match: re.Match[str]) -> str:
            return str(_resolve_key(match.group(1)))

        output_text = re.sub(r"\{\{([^}]+)\}\}", _replace, text)

        if data.get("normalizeLineEndings", True):
            output_text = output_text.replace("\r\n", "\n").replace("\r", "\n")

        return {"output": {"type": "string", "value": output_text}}
