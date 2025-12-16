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
        from ..utils.data_values import coerce_type

        input_text = coerce_type(inputs.get('input'), 'string')
        num_tokens_per_chunk = self.data.get('numTokensPerChunk', 1024)
        overlap_percent = self.data.get('overlap', 0) / 100.0

        # Clamp overlap between 0 and 1
        overlap_percent = max(0.0, min(1.0, overlap_percent))

        # Chunk the text
        chunks = self._chunk_by_token_estimate(input_text, num_tokens_per_chunk, overlap_percent)

        # Generate indexes (1-based)
        indexes = list(range(1, len(chunks) + 1))

        return {
            'chunks': {
                'type': 'string[]',
                'value': chunks,
            },
            'first': {
                'type': 'string',
                'value': chunks[0] if chunks else '',
            },
            'last': {
                'type': 'string',
                'value': chunks[-1] if chunks else '',
            },
            'indexes': {
                'type': 'number[]',
                'value': indexes,
            },
            'count': {
                'type': 'number',
                'value': len(chunks),
            },
        }

    def _chunk_by_token_estimate(self, text: str, target_tokens: int, overlap_percent: float) -> list[str]:
        """
        Chunks text by estimating token count using character-to-token ratio.
        This is a simplified version that estimates ~4 characters per token (GPT average).
        """
        if not text:
            return []

        # Estimate characters per token (GPT models average ~4 chars per token)
        chars_per_token = 4
        target_chars = target_tokens * chars_per_token

        chunks = []
        remaining = text

        while remaining:
            # Take a chunk of approximately target_chars
            chunk_end = min(len(remaining), target_chars)
            chunk = remaining[:chunk_end]
            chunks.append(chunk)

            # Calculate overlap
            overlap_chars = int(chunk_end * overlap_percent)
            remaining = remaining[chunk_end - overlap_chars:]

            # Prevent infinite loop if we're not making progress
            if chunk_end == 0:
                break

        return chunks
