from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "extractYaml",
    "title": "Extract YAML",
    "displayName": "Extract YAML",
    "data": {"rootPropertyName": "yamlDocument", "useRootPropertyNameInput": False, "objectPath": None, "useObjectPathInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Finds and parses a YAML object in the input text with a configured root property name.",
        "infoBoxTitle": "Extract YAML Node",
        "contextMenuTitle": "Extract YAML",
        "group": ["Objects"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "string", "required": True},
        {"id": "rootPropertyName", "title": "Root Property Name", "dataType": "string", "showIf": {"dataKey": "useRootPropertyNameInput", "equals": True}},
        {"id": "objectPath", "title": "Object Path", "dataType": "string", "showIf": {"dataKey": "useObjectPathInput", "equals": True}},
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "object"},
        {"id": "matches", "title": "Matches", "dataType": "any[]"},
        {"id": "noMatch", "title": "No Match", "dataType": "string"},
    ],
    "editors": [
        {"type": "string", "label": "Root Property Name", "dataKey": "rootPropertyName", "useInputToggleDataKey": "useRootPropertyNameInput"},
        {"type": "code", "label": "Object Path", "dataKey": "objectPath", "language": "jsonpath", "useInputToggleDataKey": "useObjectPathInput"},
    ],
    "body": (
        "Root: {{#if useRootPropertyNameInput}}(Using Input){{#else}}{{rootPropertyName}}{{/if}}\n"
        "{{#if useObjectPathInput}}Path: (Using Input){{#else}}{{#if objectPath}}Path: {{objectPath}}{{/if}}{{/if}}"
    ),
}
