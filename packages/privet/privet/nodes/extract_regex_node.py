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

class ExtractRegexSchema(NodeSchema):
    NODE_TYPE = 'extractRegex'
    TITLE = 'Extract Regex'
    DISPLAY_NAME = 'Extract Regex'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'Extract With Regex Node'
    UI_INFOBOX_BODY = 'Extracts data using a configured regular expression; capture groups become outputs.'
    UI_CONTEXT_MENU_TITLE = 'Extract With Regex'
    DATA = {'regex': '([a-zA-Z]+)', 'useRegexInput': False, 'errorOnFailed': False, 'multilineMode': False}
    EDITORS = [{'type': 'custom', 'customEditorId': 'ExtractRegexNodeAiAssist', 'label': 'AI Assist'}, {'type': 'toggle', 'label': 'Error on failed', 'dataKey': 'errorOnFailed'}, {'type': 'toggle', 'label': 'Multiline mode', 'dataKey': 'multilineMode'}, {'type': 'code', 'label': 'Regex', 'dataKey': 'regex', 'useInputToggleDataKey': 'useRegexInput', 'language': 'regex'}]
    BODY = '{{#if useRegexInput}}(Using regex input){{#else}}{{regex}}{{/if}}'

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Input',
            required=True,
            coerced=False,
        ),
        Input(
            id='regex',
            data_type='string',
            title='Regex',
            show_if=Eq(data_key='useRegexInput', equals=True),
            coerced=False,
        ),
    ]

    OUTPUTS = [
        Output(
            id='matches',
            data_type='string[]',
            title='Matches',
        ),
        Output(
            id='succeeded',
            data_type='boolean',
            title='Succeeded',
        ),
        Output(
            id='failed',
            data_type='boolean',
            title='Failed',
        ),
        Output(
            id='output',
            data_type='string',
            title='Output {n}',
            variadic={'type': 'regex', 'baseId': 'output', 'titlePattern': 'Output {n}', 'startAt': 1, 'regexDataKey': 'regex', 'multilineDataKey': 'multilineMode'},
        ),
    ]



@bindschema(schema=ExtractRegexSchema)
class ExtractRegexNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
