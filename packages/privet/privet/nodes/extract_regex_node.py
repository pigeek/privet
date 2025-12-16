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
        import re
        from ..utils.data_values import expect_type, expect_type_optional

        input_string = expect_type(inputs.get('input'), 'string')
        data = self.node.data or {}
        regex_pattern = expect_type_optional(inputs.get('regex'), 'string') or data.get('regex', '([a-zA-Z]+)')

        # Determine flags
        flags = re.MULTILINE if data.get('multilineMode') else 0

        try:
            regex = re.compile(regex_pattern, flags)
        except re.error as e:
            if data.get('errorOnFailed'):
                raise ValueError(f"Invalid regex pattern: {regex_pattern}") from e
            return {
                'succeeded': {'type': 'boolean', 'value': False},
                'failed': {'type': 'boolean', 'value': True},
            }

        matches_list = []
        first_match = None

        for match in regex.finditer(input_string):
            if first_match is None:
                first_match = match
            # Collect all matches from first capture group
            if len(match.groups()) > 0 and match.group(1):
                matches_list.append(match.group(1))

        if not first_match:
            if data.get('errorOnFailed'):
                raise ValueError(f"No match found for regex {regex_pattern}")
            return {
                'succeeded': {'type': 'boolean', 'value': False},
                'failed': {'type': 'boolean', 'value': True},
            }

        # Build output with all capture groups from first match
        output = {}
        for i in range(1, len(first_match.groups()) + 1):
            output[f'output{i}'] = {
                'type': 'string',
                'value': first_match.group(i) or '',
            }

        output['matches'] = {
            'type': 'string[]',
            'value': matches_list,
        }
        output['succeeded'] = {'type': 'boolean', 'value': True}
        output['failed'] = {'type': 'boolean', 'value': False}

        return output
