from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "document",
    "title": "Document",
    "displayName": "Document",
    "data": {"useDataInput": False, "useMediaTypeInput": False, "title": "", "useTitleInput": False, "context": "", "useContextInput": False, "enableCitations": False, "useEnableCitationsInput": False},
    "visual": {"width": 300},
    "uiData": {
        "contextMenuTitle": "Document",
        "group": "Data",
        "infoBoxTitle": "Document Node",
        "infoBoxBody": "Defines a document for use with other nodes such as Assemble Message. Can accept text and PDF files.",
    },
    "inputs": [
        {"id": "data", "title": "Data", "dataType": ["string","binary"], "showIf": {"dataKey": "useDataInput", "equals": True}},
        {"id": "mediaType", "title": "Media Type", "dataType": "string", "showIf": {"dataKey": "useMediaTypeInput", "equals": True}},
        {"id": "title", "title": "Title", "dataType": "string", "showIf": {"dataKey": "useTitleInput", "equals": True}},
        {"id": "context", "title": "Context", "dataType": "string", "showIf": {"dataKey": "useContextInput", "equals": True}},
        {"id": "enableCitations", "title": "Enable Citations", "dataType": "boolean", "showIf": {"dataKey": "useEnableCitationsInput", "equals": True}},
    ],
    "outputs": [
        {"id": "data", "title": "Document Data", "dataType": "document"},
    ],
    "editors": [
        {"type": "fileBrowser", "label": "Document File", "dataKey": "data", "mediaTypeDataKey": "mediaType", "useInputToggleDataKey": "useDataInput", "accept": "*/*"},
        {"type": "string", "label": "Media Type", "dataKey": "mediaType", "useInputToggleDataKey": "useMediaTypeInput"},
        {"type": "string", "label": "Title", "dataKey": "title", "useInputToggleDataKey": "useTitleInput"},
        {"type": "string", "label": "Context", "dataKey": "context", "useInputToggleDataKey": "useContextInput"},
        {"type": "toggle", "label": "Enable Citations", "dataKey": "enableCitations", "useInputToggleDataKey": "useEnableCitationsInput"},
    ],
}

