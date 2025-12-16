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

class VectorKNNSchema(NodeSchema):
    NODE_TYPE = 'vectorNearestNeighbors'
    TITLE = 'Vector KNN'
    DISPLAY_NAME = 'Vector KNN'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Vector KNN Node'
    UI_INFOBOX_BODY = 'k-nearest neighbors search on stored vectors.'
    UI_CONTEXT_MENU_TITLE = 'Vector KNN'
    DATA = {'integration': 'pinecone', 'useIntegrationInput': False, 'k': 10, 'useKInput': False, 'collectionId': '', 'useCollectionIdInput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'Integration', 'dataKey': 'integration', 'options': [{'label': 'Pinecone', 'value': 'pinecone'}], 'useInputToggleDataKey': 'useIntegrationInput'}, {'type': 'number', 'label': 'K', 'dataKey': 'k', 'min': 1, 'max': 100, 'step': 1, 'defaultValue': 10, 'useInputToggleDataKey': 'useKInput'}, {'type': 'string', 'label': 'Collection ID', 'dataKey': 'collectionId', 'useInputToggleDataKey': 'useCollectionIdInput'}]
    BODY = 'Integration: {{#if useIntegrationInput}}(using input){{#else}}{{integration}}{{/if}}\nK: {{#if useKInput}}(using input){{#else}}{{k}}{{/if}}\nCollection Id: {{#if useCollectionIdInput}}(using input){{#else}}{{collectionId}}{{/if}}'

    INPUTS = [
        Input(
            id='vector',
            data_type='vector',
            title='Vector',
            required=True,
        ),
        Input(
            id='integration',
            data_type='string',
            title='Integration',
            show_if=Eq(data_key='useIntegrationInput', equals=True),
        ),
        Input(
            id='collectionId',
            data_type='string',
            title='Collection ID',
            show_if=Eq(data_key='useCollectionIdInput', equals=True),
        ),
        Input(
            id='k',
            data_type='number',
            title='K',
            show_if=Eq(data_key='useKInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='results',
            data_type='any[]',
            title='Results',
        ),
    ]



@bindschema(schema=VectorKNNSchema)
class VectorKNNNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import math

        inputs = inputs or {}
        data = self.node.data or {}

        vector_val = inputs.get("vector")
        query = vector_val.get("value") if isinstance(vector_val, dict) else vector_val or []

        collection_id = inputs.get("collectionId") if data.get("useCollectionIdInput") else data.get("collectionId")
        if isinstance(collection_id, dict):
            collection_id = collection_id.get("value")
        collection_id = collection_id or "default"

        k = inputs.get("k") if data.get("useKInput") else data.get("k", 10)
        if isinstance(k, dict):
            k = k.get("value")
        k = int(k or 10)

        store = (self.context or {}).get("vector_store") or {}
        collection = store.get(collection_id) or []

        def l2(a, b):
            try:
                return math.sqrt(sum((float(x) - float(y)) ** 2 for x, y in zip(a, b)))
            except Exception:
                return math.inf

        scored = []
        for entry in collection:
            dist = l2(query, entry.get("vector") or [])
            scored.append({"id": entry.get("id"), "data": entry.get("data"), "distance": dist})
        scored.sort(key=lambda x: x["distance"])
        return {"results": {"type": "any[]", "value": scored[:k]}}
