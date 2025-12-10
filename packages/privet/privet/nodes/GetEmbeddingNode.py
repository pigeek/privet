from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "getEmbedding",
    "title": "Get Embedding",
    "displayName": "Get Embedding",
    "data": {"integration": "openai", "useIntegrationInput": False, "model": None, "dimensions": None, "useModelInput": False, "useDimensionsInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Gets a vector embedding for input text.",
        "infoBoxTitle": "Get Embedding Node",
        "contextMenuTitle": "Get Embedding",
        "group": ["AI"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "string", "required": True},
        {"id": "integration", "title": "Integration", "dataType": "string", "showIf": {"dataKey": "useIntegrationInput", "equals": True}},
        {"id": "model", "title": "Model", "dataType": "string", "showIf": {"dataKey": "useModelInput", "equals": True}},
        {"id": "dimensions", "title": "Dimensions", "dataType": "number", "showIf": {"dataKey": "useDimensionsInput", "equals": True}},
    ],
    "outputs": [ {"id": "embedding", "title": "Embedding", "dataType": "vector"} ],
    "editors": [
        {"type": "dropdown", "label": "Integration", "dataKey": "integration", "options": [ {"label": "OpenAI", "value": "openai"} ], "useInputToggleDataKey": "useIntegrationInput"},
        {"type": "string", "label": "Model", "dataKey": "model", "useInputToggleDataKey": "useModelInput"},
        {"type": "number", "label": "Dimensions", "dataKey": "dimensions", "useInputToggleDataKey": "useDimensionsInput"},
    ],
    "body": "Using {{#if useIntegrationInput}}(input){{#else}}{{integration}}{{/if}}",
}
