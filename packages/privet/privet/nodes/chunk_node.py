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

class ChunkSchema(NodeSchema):
    NODE_TYPE = 'chunk'
    TITLE = 'Chunk'
    DISPLAY_NAME = 'Chunk'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'Chunk Node'
    UI_INFOBOX_BODY = 'Splits input text into chunks based on approximate token count; optional overlap.'
    UI_CONTEXT_MENU_TITLE = 'Chunk'
    DATA = {'model': 'gpt-4o', 'useModelInput': False, 'numTokensPerChunk': 1024, 'overlap': 0}
    EDITORS = [{'type': 'dropdown', 'label': 'Model', 'dataKey': 'model', 'options': [{'label': 'gpt-4o', 'value': 'gpt-4o'}, {'label': 'gpt-4.1', 'value': 'gpt-4.1'}], 'useInputToggleDataKey': 'useModelInput'}, {'type': 'number', 'label': 'Number of tokens per chunk', 'dataKey': 'numTokensPerChunk', 'min': 1, 'max': 32768, 'step': 1}, {'type': 'number', 'label': 'Overlap (in %)', 'dataKey': 'overlap', 'min': 0, 'max': 100, 'step': 1}]
    BODY = 'Model: {{model}}\nToken Count: {{numTokensPerChunk}}\n{{#if overlap}}Overlap: {{overlap}}%{{/if}}'

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Input',
        ),
        Input(
            id='model',
            data_type='string',
            title='Model',
            show_if=Eq(data_key='useModelInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='chunks',
            data_type='string[]',
            title='Chunks',
        ),
        Output(
            id='first',
            data_type='string',
            title='First',
        ),
        Output(
            id='last',
            data_type='string',
            title='Last',
        ),
        Output(
            id='indexes',
            data_type='number[]',
            title='Indexes',
        ),
        Output(
            id='count',
            data_type='number',
            title='Count',
        ),
    ]



@bindschema(schema=ChunkSchema)
class ChunkNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
