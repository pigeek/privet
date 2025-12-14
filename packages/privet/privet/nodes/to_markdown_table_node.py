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

class ToMarkdownTableSchema(NodeSchema):
    NODE_TYPE = 'toMarkdownTable'
    TITLE = 'To Markdown Table'
    DISPLAY_NAME = 'To Markdown Table'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'To Markdown Table Node'
    UI_INFOBOX_BODY = 'Converts an array of objects into a markdown table.'
    UI_CONTEXT_MENU_TITLE = 'To Markdown Table'
    DATA = {'includeHeaders': True, 'alignPipes': False}
    EDITORS = [{'type': 'toggle', 'label': 'Include Headers', 'dataKey': 'includeHeaders'}, {'type': 'toggle', 'label': 'Align Pipes', 'dataKey': 'alignPipes'}]
    BODY = '{{#if includeHeaders}}With Header Row{{/if}}{{#if alignPipes}}{{#if includeHeaders}}, {{/if}}Pipes Aligned{{/if}}'

    INPUTS = [
        Input(
            id='data',
            data_type='any',
            title='Data Array',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='markdown',
            data_type='string',
            title='Markdown Table',
        ),
    ]



@bindschema(schema=ToMarkdownTableSchema)
class ToMarkdownTableNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
