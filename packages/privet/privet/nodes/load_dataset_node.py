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
        return await super().process(inputs)
