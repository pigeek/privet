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

class GetEmbeddingSchema(NodeSchema):
    NODE_TYPE = 'getEmbedding'
    TITLE = 'Get Embedding'
    DISPLAY_NAME = 'Get Embedding'
    VISUAL_WIDTH = 250
    UI_GROUP = ['AI']
    UI_INFOBOX_TITLE = 'Get Embedding Node'
    UI_INFOBOX_BODY = 'Gets a vector embedding for input text.'
    UI_CONTEXT_MENU_TITLE = 'Get Embedding'
    DATA = {'integration': 'openai', 'useIntegrationInput': False, 'model': None, 'dimensions': None, 'useModelInput': False, 'useDimensionsInput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'Integration', 'dataKey': 'integration', 'options': [{'label': 'OpenAI', 'value': 'openai'}], 'useInputToggleDataKey': 'useIntegrationInput'}, {'type': 'string', 'label': 'Model', 'dataKey': 'model', 'useInputToggleDataKey': 'useModelInput'}, {'type': 'number', 'label': 'Dimensions', 'dataKey': 'dimensions', 'useInputToggleDataKey': 'useDimensionsInput'}]
    BODY = 'Using {{#if useIntegrationInput}}(input){{#else}}{{integration}}{{/if}}'

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Input',
            required=True,
        ),
        Input(
            id='integration',
            data_type='string',
            title='Integration',
            show_if=Eq(data_key='useIntegrationInput', equals=True),
        ),
        Input(
            id='model',
            data_type='string',
            title='Model',
            show_if=Eq(data_key='useModelInput', equals=True),
        ),
        Input(
            id='dimensions',
            data_type='number',
            title='Dimensions',
            show_if=Eq(data_key='useDimensionsInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='embedding',
            data_type='vector',
            title='Embedding',
        ),
    ]



@bindschema(schema=GetEmbeddingSchema)
class GetEmbeddingNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        text_val = inputs.get("input")
        text = text_val.get("value") if isinstance(text_val, dict) else text_val
        if text is None:
            text = ""
        text_str = str(text)

        # Deterministic toy embedding for testing: [len, char_sum/1000, word_count]
        char_sum = sum(ord(c) for c in text_str)
        word_count = len(text_str.split()) if text_str else 0
        embedding = [float(len(text_str)), float(char_sum % 1000) / 1000.0, float(word_count)]

        return {"embedding": {"type": "vector", "value": embedding}}
