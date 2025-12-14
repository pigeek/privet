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
        return await super().process(inputs)
