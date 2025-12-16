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

class GetAllDatasetsSchema(NodeSchema):
    NODE_TYPE = 'getAllDatasets'
    TITLE = 'Get All Datasets'
    DISPLAY_NAME = 'Get All Datasets'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Get All Datasets Node'
    UI_INFOBOX_BODY = 'Retrieves all datasets. If no datasets exist, it returns an empty array.'
    UI_CONTEXT_MENU_TITLE = 'Get All Datasets'
    DATA = {}
    EDITORS = []

    INPUTS = [

    ]

    OUTPUTS = [
        Output(
            id='datasets',
            data_type='object[]',
            title='Datasets',
        ),
    ]



@bindschema(schema=GetAllDatasetsSchema)
class GetAllDatasetsNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        datasets = (self.context or {}).get("datasets") or {}
        listing = [{"id": did, "name": ds.get("name"), "rowCount": len(ds.get("rows", []))} for did, ds in datasets.items()]
        return {"datasets": {"type": "object[]", "value": listing}}
