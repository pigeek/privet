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

class ReplaceDatasetSchema(NodeSchema):
    NODE_TYPE = 'replaceDataset'
    TITLE = 'Replace Dataset'
    DISPLAY_NAME = 'Replace Dataset'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Replace Dataset Node'
    UI_INFOBOX_BODY = 'Replaces the data in a dataset with the given data. If no data is given, the dataset will be cleared instead.'
    UI_CONTEXT_MENU_TITLE = 'Replace Dataset'
    DATA = {'datasetId': '', 'useDatasetIdInput': False}
    EDITORS = [{'type': 'datasetSelector', 'label': 'Dataset', 'dataKey': 'datasetId', 'useInputToggleDataKey': 'useDatasetIdInput'}]

    INPUTS = [
        Input(
            id='data',
            data_type='object[]',
            title='Data',
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
            data_type='object[]',
            title='Dataset',
            description='Array of rows ({ id, data }).',
        ),
    ]



@bindschema(schema=ReplaceDatasetSchema)
class ReplaceDatasetNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
