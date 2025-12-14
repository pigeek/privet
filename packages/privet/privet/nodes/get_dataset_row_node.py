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
        return await super().process(inputs)
