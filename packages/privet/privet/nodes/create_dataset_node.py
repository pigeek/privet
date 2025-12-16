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

class CreateDatasetSchema(NodeSchema):
    NODE_TYPE = 'createDataset'
    TITLE = 'Create Dataset'
    DISPLAY_NAME = 'Create Dataset'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Create Dataset Node'
    UI_INFOBOX_BODY = 'Creates a new dataset with the provided ID and name. If the dataset already exists, it does nothing.'
    UI_CONTEXT_MENU_TITLE = 'Create Dataset'
    DATA = {}
    EDITORS = []

    INPUTS = [
        Input(
            id='datasetId',
            data_type='string',
            title='Dataset ID',
        ),
        Input(
            id='datasetName',
            data_type='string',
            title='Dataset Name',
        ),
    ]

    OUTPUTS = [
        Output(
            id='datasetId_out',
            data_type='string',
            title='Dataset ID',
        ),
    ]



@bindschema(schema=CreateDatasetSchema)
class CreateDatasetNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        dataset_id = inputs.get("datasetId") or data.get("datasetId")
        dataset_name = inputs.get("datasetName") or data.get("datasetName") or dataset_id

        if isinstance(dataset_id, dict):
            dataset_id = dataset_id.get("value")
        dataset_id = str(dataset_id or "")
        if isinstance(dataset_name, dict):
            dataset_name = dataset_name.get("value")

        datasets = (self.context or {}).setdefault("datasets", {})
        ds = datasets.get(dataset_id)
        if not ds:
            ds = {"id": dataset_id, "name": dataset_name, "rows": []}
            datasets[dataset_id] = ds
        else:
            ds.setdefault("name", dataset_name)

        return {"datasetId_out": {"type": "string", "value": dataset_id}}
