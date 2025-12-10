from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "readDirectory",
    "title": "Read Directory",
    "displayName": "Read Directory",
    "data": {"path": "examples", "usePathInput": False, "recursive": False, "useRecursiveInput": False, "includeDirectories": False, "useIncludeDirectoriesInput": False, "filterGlobs": [], "useFilterGlobsInput": False, "relative": False, "useRelativeInput": False, "ignores": [], "useIgnoresInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Reads a directory and outputs Paths, Root Path, and a Tree.",
        "infoBoxTitle": "Read Directory Node",
        "contextMenuTitle": "Read Directory",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "path", "title": "Path", "dataType": "string", "showIf": {"dataKey": "usePathInput", "equals": True}},
        {"id": "recursive", "title": "Recursive", "dataType": "boolean", "showIf": {"dataKey": "useRecursiveInput", "equals": True}},
        {"id": "includeDirectories", "title": "Include Directories", "dataType": "boolean", "showIf": {"dataKey": "useIncludeDirectoriesInput", "equals": True}},
        {"id": "filterGlobs", "title": "Filter Globs", "dataType": "string[]", "showIf": {"dataKey": "useFilterGlobsInput", "equals": True}},
        {"id": "relative", "title": "Relative", "dataType": "boolean", "showIf": {"dataKey": "useRelativeInput", "equals": True}},
        {"id": "ignores", "title": "Ignores", "dataType": "string[]", "showIf": {"dataKey": "useIgnoresInput", "equals": True}},
    ],
    "outputs": [
        {"id": "rootPath", "title": "Root Path", "dataType": "string"},
        {"id": "paths", "title": "Paths", "dataType": "string[]"},
        {"id": "tree", "title": "Tree", "dataType": "object"},
    ],
    "body": "Path: {{#if usePathInput}}(Input){{#else}}{{path}}{{/if}}\nRecursive: {{#if useRecursiveInput}}(Input){{#else}}{{recursive}}{{/if}}\nInclude Directories: {{#if useIncludeDirectoriesInput}}(Input){{#else}}{{includeDirectories}}{{/if}}\nRelative: {{#if useRelativeInput}}(Input){{#else}}{{relative}}{{/if}}\nFilters: {{#if useFilterGlobsInput}}(Input){{#else}}{{#if filterGlobs}}{{filterGlobs}}{{#else}}None{{/if}}{{/if}}",
}
