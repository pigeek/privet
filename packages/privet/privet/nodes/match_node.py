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
import re

class MatchSchema(NodeSchema):
    NODE_TYPE = 'match'
    TITLE = 'Match'
    DISPLAY_NAME = 'Match'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Logic']
    UI_INFOBOX_TITLE = 'Match Node'
    UI_INFOBOX_BODY = 'Routes the value through the first matching regex case; can be exclusive.'
    UI_CONTEXT_MENU_TITLE = 'Match'
    DATA = {'cases': ['YES', 'NO'], 'exclusive': False}
    EDITORS = [{'type': 'toggle', 'dataKey': 'exclusive', 'label': 'Exclusive', 'helperMessage': 'Only the first matching branch runs.'}, {'type': 'stringList', 'dataKey': 'cases', 'label': 'Cases', 'placeholder': 'Case (regular expression)', 'helperMessage': '(Regular expressions)'}]
    BODY = '{{#if exclusive}}First Matching Case{{#else}}All Matching Cases{{/if}}\n{{cases.length}} Cases'

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Test',
            description='Value tested against each regex.',
            required=True,
        ),
        Input(
            id='value',
            data_type='any',
            title='Value',
            description='Passed through when a case matches.',
        ),
    ]

    OUTPUTS = [
        Output(
            id='case',
            data_type='string',
            title='{{item}}',
            variadic={'type': 'dataList', 'dataKey': 'cases', 'baseId': 'case', 'titleTemplate': '{{item}}', 'startAt': 1},
        ),
        Output(
            id='unmatched',
            data_type='string',
            title='Unmatched',
            description='Value when no regex matches.',
        ),
    ]



@bindschema(schema=MatchSchema)
class MatchNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        test_str = ""
        test_val = inputs.get("input")
        if isinstance(test_val, dict) and "value" in test_val:
            test_str = str(test_val.get("value") or "")
        elif test_val is not None:
            test_str = str(test_val)

        value = inputs.get("value")
        output_type = value.get("type") if isinstance(value, dict) else ("string" if value is None else "any")
        output_value = value.get("value") if isinstance(value, dict) else (test_str if value is None else value)

        cases = data.get("cases") or []
        exclusive = bool(data.get("exclusive"))
        matched_any = False
        outputs: Dict[str, Any] = {}

        for idx, pattern in enumerate(cases):
            try:
                reg = re.compile(pattern or "")
                match = bool(reg.search(test_str))
            except re.error:
                match = False

            can_match = not exclusive or not matched_any
            if match and can_match:
                matched_any = True
                outputs[f"case{idx+1}"] = {"type": output_type, "value": output_value}
            else:
                outputs[f"case{idx+1}"] = {"type": "control-flow-excluded", "value": None}

        if matched_any:
            outputs["unmatched"] = {"type": "control-flow-excluded", "value": None}
        else:
            outputs["unmatched"] = {"type": output_type, "value": output_value}

        return outputs
