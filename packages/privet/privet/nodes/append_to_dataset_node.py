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

class AppendtoDatasetSchema(NodeSchema):
    NODE_TYPE = 'appendToDataset'
    TITLE = 'Append to Dataset'
    DISPLAY_NAME = 'Append to Dataset'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Append to Dataset Node'
    UI_INFOBOX_BODY = 'Appends a row of data to the specified dataset.'
    UI_CONTEXT_MENU_TITLE = 'Append to Dataset'
    DATA = {'datasetId': '', 'useDatasetIdInput': False}
    EDITORS = [{'type': 'datasetSelector', 'label': 'Dataset', 'dataKey': 'datasetId', 'useInputToggleDataKey': 'useDatasetIdInput'}]

    INPUTS = [
        Input(
            id='data',
            data_type='string[]',
            title='Data',
        ),
        Input(
            id='id',
            data_type='string',
            title='ID',
        ),
        Input(
            id='embedding',
            data_type='vector',
            title='Embedding',
        ),
        Input(
            id='datasetId',
            data_type='string',
            title='Dataset ID',
            show_if=Eq(data_key='useDatasetIdInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='dataset',
            data_type='object',
            title='Dataset',
        ),
        Output(
            id='id_out',
            data_type='string',
            title='ID',
        ),
    ]



@bindschema(schema=AppendtoDatasetSchema)
class AppendtoDatasetNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        dataset_id = inputs.get("datasetId") if data.get("useDatasetIdInput") else data.get("datasetId")
        if isinstance(dataset_id, dict):
            dataset_id = dataset_id.get("value")
        dataset_id = str(dataset_id or "")

        datasets = (self.context or {}).setdefault("datasets", {})
        ds = datasets.setdefault(dataset_id, {"id": dataset_id, "name": dataset_id, "rows": []})

        row_id_val = inputs.get("id")
        row_id = row_id_val.get("value") if isinstance(row_id_val, dict) else row_id_val
        if row_id is None:
            row_id = str(len(ds.get("rows", [])))

        row_data = inputs.get("data")
        embedding = inputs.get("embedding")
        row = {"id": row_id, "data": row_data, "embedding": embedding}
        ds.setdefault("rows", []).append(row)

        return {
            "dataset": {"type": "object", "value": ds},
            "id_out": {"type": "string", "value": row_id},
        }
