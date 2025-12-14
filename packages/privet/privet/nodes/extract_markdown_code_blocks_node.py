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

class ExtractMarkdownCodeBlocksSchema(NodeSchema):
    NODE_TYPE = 'extractMarkdownCodeBlocks'
    TITLE = 'Extract Markdown Code Blocks'
    DISPLAY_NAME = 'Extract Markdown Code Blocks'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'Extract Markdown Code Blocks Node'
    UI_INFOBOX_BODY = 'Extracts fenced code blocks and their languages from markdown.'
    UI_CONTEXT_MENU_TITLE = 'Extract Markdown Code Blocks'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Input',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='firstBlock',
            data_type='string',
            title='First Block',
        ),
        Output(
            id='allBlocks',
            data_type='string[]',
            title='All Blocks',
        ),
        Output(
            id='languages',
            data_type='string[]',
            title='Languages',
        ),
    ]



@bindschema(schema=ExtractMarkdownCodeBlocksSchema)
class ExtractMarkdownCodeBlocksNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
