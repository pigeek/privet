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

class DestructureSchema(NodeSchema):
    NODE_TYPE = 'destructure'
    TITLE = 'Destructure'
    DISPLAY_NAME = 'Destructure'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Objects']
    UI_INFOBOX_TITLE = 'Destructure Node'
    UI_INFOBOX_BODY = 'Destructures the input object by extracting values at configured JSONPath expressions.'
    UI_CONTEXT_MENU_TITLE = 'Destructure'
    DATA = {'paths': ['$.value']}
    EDITORS = [{'type': 'stringList', 'label': 'Paths', 'dataKey': 'paths', 'helperMessage': 'JSONPath expressions (one per line).'}]

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
            id='match_',
            data_type='any',
            title='{{item}}',
            variadic={'type': 'dataList', 'dataKey': 'paths', 'baseId': 'match_', 'titleTemplate': '{{item}}'},
        ),
    ]



@bindschema(schema=DestructureSchema)
class DestructureNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        from jsonpath_ng import parse as jsonpath_parse
        from ..utils.data_values import coerce_type_optional

        input_object = coerce_type_optional(inputs.get('object'), 'object')
        paths = self.data.get('paths', ['$.value'])

        output = {}

        for index, path in enumerate(paths):
            match = None
            try:
                jsonpath_expr = jsonpath_parse(path.strip())
                results = jsonpath_expr.find(input_object or {})
                # JSONPath with wrap=false behavior: return first match or undefined
                match = results[0].value if results else None
            except Exception:
                match = None

            output[f'match_{index}'] = {
                'type': 'any',
                'value': match,
            }

        return output
