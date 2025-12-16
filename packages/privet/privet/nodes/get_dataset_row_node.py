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

class GetDatasetRowSchema(NodeSchema):
    NODE_TYPE = 'getDatasetRow'
    TITLE = 'Get Dataset Row'
    DISPLAY_NAME = 'Get Dataset Row'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Get Dataset Row Node'
    UI_INFOBOX_BODY = 'Gets a row from a dataset with the provided ID. If the dataset or row does not exist, it throws an error.'
    UI_CONTEXT_MENU_TITLE = 'Get Dataset Row'
    DATA = {'datasetId': '', 'useDatasetIdInput': False, 'rowId': '', 'useRowIdInput': False}
    EDITORS = [{'type': 'datasetSelector', 'label': 'Dataset', 'dataKey': 'datasetId', 'useInputToggleDataKey': 'useDatasetIdInput'}, {'type': 'string', 'label': 'Row ID', 'dataKey': 'rowId', 'useInputToggleDataKey': 'useRowIdInput'}]

    INPUTS = [
        Input(
            id='rowId',
            data_type='string',
            title='Row ID',
            show_if=Eq(data_key='useRowIdInput', equals=True),
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
            id='row',
            data_type='object',
            title='Row',
        ),
    ]



@bindschema(schema=GetDatasetRowSchema)
class GetDatasetRowNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        dataset_id = inputs.get("datasetId") if data.get("useDatasetIdInput") else data.get("datasetId")
        row_id = inputs.get("rowId") if data.get("useRowIdInput") else data.get("rowId")
        if isinstance(dataset_id, dict):
            candidate = dataset_id.get("value")
            if isinstance(candidate, dict) and "id" in candidate:
                dataset_id = candidate.get("id")
            elif candidate is not None:
                dataset_id = candidate
            elif "id" in dataset_id:
                dataset_id = dataset_id.get("id")
        dataset_id = str(dataset_id or "")
        if isinstance(row_id, dict):
            row_id = row_id.get("value")

        datasets = (self.context or {}).get("datasets") or {}
        ds = datasets.get(dataset_id)
        if ds is None:
            raise ValueError(f"Dataset not found: {dataset_id}")

        rows = ds.get("rows", [])
        match = next((r for r in rows if r.get("id") == row_id), None)
        if match is None:
            raise ValueError(f"Row {row_id} not found in dataset {dataset_id}")

        return {"row": {"type": "object", "value": match}}
