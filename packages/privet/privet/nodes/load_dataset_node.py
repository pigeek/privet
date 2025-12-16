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

class LoadDatasetSchema(NodeSchema):
    NODE_TYPE = 'loadDataset'
    TITLE = 'Load Dataset'
    DISPLAY_NAME = 'Load Dataset'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Load Dataset Node'
    UI_INFOBOX_BODY = 'Loads a dataset with the provided ID. If the dataset does not exist, it throws an error.'
    UI_CONTEXT_MENU_TITLE = 'Load Dataset'
    DATA = {'datasetId': '', 'useDatasetIdInput': False}
    EDITORS = [{'type': 'datasetSelector', 'label': 'Dataset', 'dataKey': 'datasetId', 'useInputToggleDataKey': 'useDatasetIdInput'}]

    INPUTS = [
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
            data_type='object[]',
            title='Dataset',
        ),
        Output(
            id='datasetId_out',
            data_type='string',
            title='Dataset ID',
        ),
    ]



@bindschema(schema=LoadDatasetSchema)
class LoadDatasetNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}
        dataset_id = inputs.get("datasetId") if data.get("useDatasetIdInput") else data.get("datasetId")
        if isinstance(dataset_id, dict):
            dataset_id = dataset_id.get("value")
        dataset_id = str(dataset_id or "")

        datasets = (self.context or {}).get("datasets") or {}
        ds = datasets.get(dataset_id)
        if ds is None:
            raise ValueError(f"Dataset not found: {dataset_id}")

        rows = ds.get("rows", [])
        return {
            "dataset": {"type": "object[]", "value": rows},
            "datasetId_out": {"type": "string", "value": dataset_id},
        }
