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
        return await super().process(inputs)
