from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "readFile",
    "title": "Read File",
    "displayName": "Read File",
    "data": {"path": "", "asBinary": False, "usePathInput": True, "errorOnMissingFile": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Reads the contents of the specified file and outputs it as string or binary.",
        "infoBoxTitle": "Read File Node",
        "contextMenuTitle": "Read File",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "path", "title": "Path", "dataType": "string", "showIf": {"dataKey": "usePathInput", "equals": True}},
    ],
    "outputs": [
        {"id": "content", "title": "Content", "dataType": "string"},
    ],
    "editors": [
        {"type": "filePathBrowser", "label": "Path", "dataKey": "path", "useInputToggleDataKey": "usePathInput"},
        {"type": "toggle", "label": "Error on Missing File", "dataKey": "errorOnMissingFile"},
        {"type": "toggle", "label": "Read as Binary", "dataKey": "asBinary"},
    ],
    "body": "{{#if asBinary}}Read as Binary{{#else}}Read as Text{{/if}}\n{{#if usePathInput}}{{#else}}Path: {{path}}{{/if}}",
}
