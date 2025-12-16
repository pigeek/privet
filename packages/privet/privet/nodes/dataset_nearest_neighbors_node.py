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

class KNNDatasetSchema(NodeSchema):
    NODE_TYPE = 'datasetNearestNeighbors'
    TITLE = 'KNN Dataset'
    DISPLAY_NAME = 'KNN Dataset'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'KNN Dataset Node'
    UI_INFOBOX_BODY = 'Finds the k nearest neighbors in the dataset with the provided ID, given an embedding.'
    UI_CONTEXT_MENU_TITLE = 'KNN Dataset'
    DATA = {'datasetId': '', 'useDatasetIdInput': False, 'k': 5, 'useKInput': False}
    EDITORS = [{'type': 'datasetSelector', 'label': 'Dataset', 'dataKey': 'datasetId', 'useInputToggleDataKey': 'useDatasetIdInput'}, {'type': 'number', 'label': 'K', 'dataKey': 'k', 'useInputToggleDataKey': 'useKInput'}]

    INPUTS = [
        Input(
            id='embedding',
            data_type='object',
            title='Embedding',
        ),
        Input(
            id='datasetId',
            data_type='string',
            title='Dataset ID',
            show_if=Eq(data_key='useDatasetIdInput', equals=True),
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
            id='nearestNeighbors',
            data_type='object[]',
            title='Nearest Neighbors',
        ),
    ]



@bindschema(schema=KNNDatasetSchema)
class KNNDatasetNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import math

        inputs = inputs or {}
        data = self.node.data or {}

        dataset_id = inputs.get("datasetId") if data.get("useDatasetIdInput") else data.get("datasetId")
        if isinstance(dataset_id, dict):
            candidate = dataset_id.get("value")
            if isinstance(candidate, dict) and "id" in candidate:
                dataset_id = candidate.get("id")
            elif candidate is not None:
                dataset_id = candidate
            elif "id" in dataset_id:
                dataset_id = dataset_id.get("id")
        dataset_id = str(dataset_id or "")

        k = inputs.get("k") if data.get("useKInput") else data.get("k", 5)
        if isinstance(k, dict):
            k = k.get("value")
        k = int(k or 5)

        query_val = inputs.get("embedding")
        query = query_val.get("value") if isinstance(query_val, dict) else query_val or []

        datasets = (self.context or {}).get("datasets") or {}
        ds = datasets.get(dataset_id)
        if ds is None:
            raise ValueError(f"Dataset not found: {dataset_id}")

        rows = ds.get("rows", [])

        def l2(a, b):
            try:
                return math.sqrt(sum((float(x) - float(y)) ** 2 for x, y in zip(a, b)))
            except Exception:
                return math.inf

        scored = []
        for row in rows:
            emb = row.get("embedding")
            if isinstance(emb, dict):
                emb = emb.get("value")
            dist = l2(query, emb or [])
            scored.append({"row": row, "distance": dist})
        scored.sort(key=lambda x: x["distance"])

        return {"nearestNeighbors": {"type": "object[]", "value": scored[:k]}}
