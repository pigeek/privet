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

class ReadFileSchema(NodeSchema):
    NODE_TYPE = 'readFile'
    TITLE = 'Read File'
    DISPLAY_NAME = 'Read File'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Read File Node'
    UI_INFOBOX_BODY = 'Reads the contents of the specified file and outputs it as string or binary.'
    UI_CONTEXT_MENU_TITLE = 'Read File'
    DATA = {'path': '', 'asBinary': False, 'usePathInput': True, 'errorOnMissingFile': False}
    EDITORS = [{'type': 'filePathBrowser', 'label': 'Path', 'dataKey': 'path', 'useInputToggleDataKey': 'usePathInput'}, {'type': 'toggle', 'label': 'Error on Missing File', 'dataKey': 'errorOnMissingFile'}, {'type': 'toggle', 'label': 'Read as Binary', 'dataKey': 'asBinary'}]
    BODY = '{{#if asBinary}}Read as Binary{{#else}}Read as Text{{/if}}\n{{#if usePathInput}}{{#else}}Path: {{path}}{{/if}}'

    INPUTS = [
        Input(
            id='path',
            data_type='string',
            title='Path',
            show_if=Eq(data_key='usePathInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='content',
            data_type='string',
            title='Content',
        ),
    ]



@bindschema(schema=ReadFileSchema)
class ReadFileNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
