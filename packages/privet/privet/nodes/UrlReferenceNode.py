from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "urlReference",
    "title": "URL Reference",
    "displayName": "URL Reference",
    "data": {"url": "", "useUrlInput": False},
    "visual": {"width": 225},
    "uiData": {
        "contextMenuTitle": "URL Reference",
        "group": "Data",
        "infoBoxTitle": "URL Reference Node",
        "infoBoxBody": "Defines a reference to a URL, or converts a string into a URL reference.",
    },
    "inputs": [
        {"id": "url", "title": "URL", "dataType": "string", "showIf": {"dataKey": "useUrlInput", "equals": True}},
    ],
    "outputs": [
        {"id": "urlReference", "title": "URL Reference", "dataType": "object"},
    ],
    "editors": [
        {"type": "string", "label": "URL", "dataKey": "url", "useInputToggleDataKey": "useUrlInput"},
    ],
    "body": "{{#if useUrlInput}}(URL Using Input){{#else}}{{url}}{{/if}}",
}
