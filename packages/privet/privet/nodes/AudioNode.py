from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "audio",
    "title": "Audio",
    "displayName": "Audio",
    "data": {"useDataInput": False, "useMediaTypeInput": False},
    "visual": {"width": 300},
    "uiData": {
        "contextMenuTitle": "Audio",
        "group": "Data",
        "infoBoxTitle": "Audio Node",
        "infoBoxBody": "Defines an audio sample for use with other nodes.",
    },
    "inputs": [
        {"id": "data", "title": "Data", "dataType": "binary", "showIf": {"dataKey": "useDataInput", "equals": True}},
        {"id": "mediaType", "title": "Media Type", "dataType": "string", "showIf": {"dataKey": "useMediaTypeInput", "equals": True}},
    ],
    "outputs": [
        {"id": "data", "title": "Audio Data", "dataType": "audio"},
    ],
    "editors": [
        {"type": "fileBrowser", "label": "Audio File", "dataKey": "data", "mediaTypeDataKey": "mediaType", "useInputToggleDataKey": "useDataInput", "accept": "audio/*"},
        {"type": "string", "label": "Media Type", "dataKey": "mediaType", "useInputToggleDataKey": "useMediaTypeInput"},
    ],
}

