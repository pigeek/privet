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
        return await super().process(inputs)
