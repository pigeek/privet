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

class VectorStoreSchema(NodeSchema):
    NODE_TYPE = 'vectorStore'
    TITLE = 'Vector Store'
    DISPLAY_NAME = 'Vector Store'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Vector Store Node'
    UI_INFOBOX_BODY = 'Stores vectors + data in the configured vector DB.'
    UI_CONTEXT_MENU_TITLE = 'Vector Store'
    DATA = {'integration': 'pinecone', 'collectionId': '', 'useIntegrationInput': False, 'useCollectionIdInput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'Integration', 'dataKey': 'integration', 'options': [{'label': 'Pinecone', 'value': 'pinecone'}], 'useInputToggleDataKey': 'useIntegrationInput'}, {'type': 'string', 'label': 'Collection ID', 'dataKey': 'collectionId', 'useInputToggleDataKey': 'useCollectionIdInput'}]
    BODY = 'Integration: {{#if useIntegrationInput}}(using input){{#else}}{{integration}}{{/if}}\nCollection Id: {{#if useCollectionIdInput}}(using input){{#else}}{{collectionId}}{{/if}}'

    INPUTS = [
        Input(
            id='vector',
            data_type='vector',
            title='Vector',
            required=True,
        ),
        Input(
            id='collectionId',
            data_type='string',
            title='Collection ID',
            show_if=Eq(data_key='useCollectionIdInput', equals=True),
        ),
        Input(
            id='data',
            data_type='any',
            title='Data',
            required=True,
        ),
        Input(
            id='integration',
            data_type='string',
            title='Integration',
            show_if=Eq(data_key='useIntegrationInput', equals=True),
        ),
        Input(
            id='id',
            data_type='string',
            title='ID',
        ),
    ]

    OUTPUTS = [
        Output(
            id='complete',
            data_type='boolean',
            title='Complete',
        ),
    ]



@bindschema(schema=VectorStoreSchema)
class VectorStoreNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
