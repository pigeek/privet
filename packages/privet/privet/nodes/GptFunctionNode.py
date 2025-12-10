from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "gptFunction",
    "title": "Tool",
    "displayName": "Tool",
    "data": {"name": "newTool", "description": "No description provided", "schema": '{\n  "type": "object",\n  "properties": {}\n}', "useNameInput": False, "useDescriptionInput": False, "useSchemaInput": False, "strict": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Defines a tool (function) that the LLM can call in responses.",
        "infoBoxTitle": "Tool Node",
        "contextMenuTitle": "Tool",
        "group": ["AI"],
    },
    "inputs": [
        {"id": "name", "title": "Name", "dataType": "string", "showIf": {"dataKey": "useNameInput", "equals": True}},
        {"id": "description", "title": "Description", "dataType": "string", "showIf": {"dataKey": "useDescriptionInput", "equals": True}},
        {"id": "schema", "title": "Schema", "dataType": "object", "showIf": {"dataKey": "useSchemaInput", "equals": True}},
    ],
    "outputs": [ {"id": "function", "title": "Function", "dataType": "gpt-function"} ],
    "editors": [
        {"type": "string", "label": "Name", "dataKey": "name", "useInputToggleDataKey": "useNameInput"},
        {"type": "toggle", "label": "Strict", "dataKey": "strict"},
        {"type": "code", "label": "Description", "dataKey": "description", "useInputToggleDataKey": "useDescriptionInput", "language": "markdown", "height": 100},
        {"type": "custom", "customEditorId": "GptFunctionNodeJsonSchemaAiAssist", "label": "AI Assist"},
        {"type": "code", "label": "Schema", "dataKey": "schema", "language": "json", "useInputToggleDataKey": "useSchemaInput"},
    ],
    "body": "!markdown_{{name}}_: {{description}}",
    "interpolationInputs": {"dataKey": "schema", "dataType": "string"},
}

