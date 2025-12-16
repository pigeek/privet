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

class DocumentSchema(NodeSchema):
    NODE_TYPE = 'document'
    TITLE = 'Document'
    DISPLAY_NAME = 'Document'
    VISUAL_WIDTH = 300
    UI_GROUP = 'Data'
    UI_INFOBOX_TITLE = 'Document Node'
    UI_INFOBOX_BODY = 'Defines a document for use with other nodes such as Assemble Message. Can accept text and PDF files.'
    UI_CONTEXT_MENU_TITLE = 'Document'
    DATA = {'useDataInput': False, 'useMediaTypeInput': False, 'title': '', 'useTitleInput': False, 'context': '', 'useContextInput': False, 'enableCitations': False, 'useEnableCitationsInput': False}
    EDITORS = [{'type': 'fileBrowser', 'label': 'Document File', 'dataKey': 'data', 'mediaTypeDataKey': 'mediaType', 'useInputToggleDataKey': 'useDataInput', 'accept': '*/*'}, {'type': 'string', 'label': 'Media Type', 'dataKey': 'mediaType', 'useInputToggleDataKey': 'useMediaTypeInput'}, {'type': 'string', 'label': 'Title', 'dataKey': 'title', 'useInputToggleDataKey': 'useTitleInput'}, {'type': 'string', 'label': 'Context', 'dataKey': 'context', 'useInputToggleDataKey': 'useContextInput'}, {'type': 'toggle', 'label': 'Enable Citations', 'dataKey': 'enableCitations', 'useInputToggleDataKey': 'useEnableCitationsInput'}]

    INPUTS = [
        Input(
            id='data',
            data_type=['string', 'binary'],
            title='Data',
            show_if=Eq(data_key='useDataInput', equals=True),
        ),
        Input(
            id='mediaType',
            data_type='string',
            title='Media Type',
            show_if=Eq(data_key='useMediaTypeInput', equals=True),
        ),
        Input(
            id='title',
            data_type='string',
            title='Title',
            show_if=Eq(data_key='useTitleInput', equals=True),
        ),
        Input(
            id='context',
            data_type='string',
            title='Context',
            show_if=Eq(data_key='useContextInput', equals=True),
        ),
        Input(
            id='enableCitations',
            data_type='boolean',
            title='Enable Citations',
            show_if=Eq(data_key='useEnableCitationsInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='data',
            data_type='document',
            title='Document Data',
        ),
    ]



@bindschema(schema=DocumentSchema)
class DocumentNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        from ..utils.data_values import coerce_type_optional

        inputs = inputs or {}
        data = self.node.data or {}

        media_type = data.get("mediaType") or "application/octet-stream"
        if data.get("useMediaTypeInput"):
            media_type = coerce_type_optional(inputs.get("mediaType"), "string") or media_type

        title = data.get("title") or ""
        if data.get("useTitleInput"):
            title = coerce_type_optional(inputs.get("title"), "string") or title

        context = data.get("context") or ""
        if data.get("useContextInput"):
            context = coerce_type_optional(inputs.get("context"), "string") or context

        enable_citations = bool(data.get("enableCitations"))
        if data.get("useEnableCitationsInput"):
            ec = coerce_type_optional(inputs.get("enableCitations"), "boolean")
            if ec is not None:
                enable_citations = ec

        doc_data = None
        if data.get("useDataInput"):
            val = inputs.get("data")
            doc_data = val.get("value") if isinstance(val, dict) else val
        else:
            doc_data = (data.get("data") or {}).get("value") or data.get("data")

        return {
            "data": {
                "type": "document",
                "value": {
                    "data": doc_data,
                    "mediaType": media_type,
                    "title": title,
                    "context": context,
                    "enableCitations": enable_citations,
                },
            }
        }
