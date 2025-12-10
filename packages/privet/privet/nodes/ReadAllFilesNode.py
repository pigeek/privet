from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "readAllFiles",
    "title": "Read All Files",
    "displayName": "Read All Files",
    "data": {"path": "", "usePathInput": False, "recursive": False, "useRecursiveInput": False, "filterGlobs": [], "useFilterGlobsInput": False, "ignores": [], "useIgnoresInput": False, "asBinary": False, "errorOnMissingFile": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Reads all files in a directory and outputs list of {path, content}.",
        "infoBoxTitle": "Read All Files Node",
        "contextMenuTitle": "Read All Files",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "path", "title": "Path", "dataType": "string", "showIf": {"dataKey": "usePathInput", "equals": True}},
        {"id": "recursive", "title": "Recursive", "dataType": "boolean", "showIf": {"dataKey": "useRecursiveInput", "equals": True}},
        {"id": "filterGlobs", "title": "Filter Globs", "dataType": "string[]", "showIf": {"dataKey": "useFilterGlobsInput", "equals": True}},
        {"id": "ignores", "title": "Ignores", "dataType": "string[]", "showIf": {"dataKey": "useIgnoresInput", "equals": True}},
    ],
    "outputs": [
        {"id": "files", "title": "Files", "dataType": "object[]"},
        {"id": "rootPath", "title": "Root Path", "dataType": "string"},
    ],
    "editors": [
        {"type": "directoryBrowser", "label": "Path", "dataKey": "path", "useInputToggleDataKey": "usePathInput"},
        {"type": "toggle", "label": "Recursive", "dataKey": "recursive", "useInputToggleDataKey": "useRecursiveInput"},
        {"type": "stringList", "label": "Filter Globs", "dataKey": "filterGlobs", "useInputToggleDataKey": "useFilterGlobsInput"},
        {"type": "stringList", "label": "Ignores", "dataKey": "ignores", "useInputToggleDataKey": "useIgnoresInput"},
        {"type": "toggle", "label": "Read as Binary", "dataKey": "asBinary"},
        {"type": "toggle", "label": "Error on Missing File", "dataKey": "errorOnMissingFile"},
    ],
    "body": (
        "{{#if asBinary}}Read as Binary{{#else}}Read as Text{{/if}}\n"
        "Path: {{#if usePathInput}}(Input){{#else}}{{path}}{{/if}}\n"
        "Recursive: {{#if useRecursiveInput}}(Input){{#else}}{{recursive}}{{/if}}\n"
        "Filters: {{#if useFilterGlobsInput}}(Input){{#else}}{{#if filterGlobs}}{{filterGlobs}}{{#else}}None{{/if}}{{/if}}"
    ),
}
