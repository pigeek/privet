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

class ObjectSchema(NodeSchema):
    NODE_TYPE = 'object'
    TITLE = 'Object'
    DISPLAY_NAME = 'Object'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Objects']
    UI_INFOBOX_TITLE = 'Object Node'
    UI_INFOBOX_BODY = 'Creates an object (or array) from input values and a JSON template, inserting values via interpolation.'
    UI_CONTEXT_MENU_TITLE = 'Object'
    DATA = {'jsonTemplate': '{\n  "key": "{{input}}"\n}'}
    EDITORS = [{'type': 'custom', 'customEditorId': 'ObjectNodeAiAssist', 'label': 'AI Assist'}, {'type': 'code', 'label': 'JSON Template', 'dataKey': 'jsonTemplate', 'language': 'json', 'theme': 'prompt-interpolation'}]
    BODY = '{{jsonTemplate}}'

    INPUTS = [

    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type=['object', 'object[]'],
            title='Output',
        ),
    ]



@bindschema(schema=ObjectSchema)
class ObjectNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
