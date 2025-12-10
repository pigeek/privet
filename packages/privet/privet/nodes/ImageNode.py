from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "image",
    "title": "Image",
    "displayName": "Image",
    "data": {"useDataInput": False, "mediaType": "image/png", "useMediaTypeInput": False},
    "visual": {"width": 250},
    "uiData": {
        "contextMenuTitle": "Image",
        "group": "Data",
        "infoBoxTitle": "Image Node",
        "infoBoxBody": "Defines a static image for use with other nodes. Can convert a binary type into an image type.",
    },
    "inputs": [
        {"id": "data", "title": "Data", "dataType": "binary", "showIf": {"dataKey": "useDataInput", "equals": True}},
        {"id": "mediaType", "title": "Media Type", "dataType": "string", "showIf": {"dataKey": "useMediaTypeInput", "equals": True}},
    ],
    "outputs": [
        {"id": "image", "title": "Image", "dataType": "image"},
    ],
    "editors": [
        {"type": "dropdown", "label": "Media Type", "dataKey": "mediaType", "useInputToggleDataKey": "useMediaTypeInput", "options": [
            {"value": "image/png", "label": "PNG"},
            {"value": "image/jpeg", "label": "JPEG"},
            {"value": "image/gif", "label": "GIF"}
        ]},
        {"type": "imageBrowser", "label": "Image", "dataKey": "data", "useInputToggleDataKey": "useDataInput", "mediaTypeDataKey": "mediaType"},
    ],
}

