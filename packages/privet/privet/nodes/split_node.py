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
from ..utils import coerce_type_optional, get_input_or_data, handle_escape_characters

class SplitTextSchema(NodeSchema):
    NODE_TYPE = 'split'
    TITLE = 'Split Text'
    DISPLAY_NAME = 'Split String'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'Split Text Node'
    UI_INFOBOX_BODY = 'Splits a string by the provided delimiter.'
    UI_CONTEXT_MENU_TITLE = 'Split Text'
    DATA = {'delimiter': ',', 'useDelimiterInput': False, 'regex': False}
    EDITORS = [{'type': 'toggle', 'label': 'Regex', 'dataKey': 'regex'}, {'type': 'code', 'label': 'Delimiter', 'language': 'plaintext', 'dataKey': 'delimiter', 'useInputToggleDataKey': 'useDelimiterInput'}]
    BODY = '{{#if useDelimiterInput}}(Delimiter from input){{#else}}{{delimiter}}{{/if}}'

    INPUTS = [
        Input(
            id='string',
            data_type='string',
            title='String',
        ),
        Input(
            id='delimiter',
            data_type='string',
            title='Delimiter',
            show_if=Eq(data_key='useDelimiterInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='splitString',
            data_type='string[]',
            title='Split',
        ),
    ]



@bindschema(schema=SplitTextSchema)
class SplitTextNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        delimiter = get_input_or_data(data, inputs, "delimiter", "string")
        delimiter = "" if delimiter is None else str(delimiter)
        normalized_delimiter = delimiter
        if data.get("regex"):
            try:
                import re

                pattern = re.compile(delimiter)
            except Exception:
                pattern = None
        else:
            normalized_delimiter = handle_escape_characters(delimiter)
            pattern = None

        string_value = coerce_type_optional(inputs.get("string"), "string") or ""
        split_result = []
        try:
            if pattern is not None:
                split_result = pattern.split(string_value)
            else:
                split_result = string_value.split(normalized_delimiter)
        except Exception:
            split_result = [string_value]

        return {"splitString": {"type": "string[]", "value": split_result}}
