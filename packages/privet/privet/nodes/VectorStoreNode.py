from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "vectorStore",
    "title": "Vector Store",
    "displayName": "Vector Store",
    "data": {"integration": "pinecone", "collectionId": "", "useIntegrationInput": False, "useCollectionIdInput": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Stores vectors + data in the configured vector DB.",
        "infoBoxTitle": "Vector Store Node",
        "contextMenuTitle": "Vector Store",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "vector", "title": "Vector", "dataType": "vector", "required": True},
        {"id": "collectionId", "title": "Collection ID", "dataType": "string", "showIf": {"dataKey": "useCollectionIdInput", "equals": True}},
        {"id": "data", "title": "Data", "dataType": "any", "required": True},
        {"id": "integration", "title": "Integration", "dataType": "string", "showIf": {"dataKey": "useIntegrationInput", "equals": True}},
        {"id": "id", "title": "ID", "dataType": "string"},
    ],
    "outputs": [ {"id": "complete", "title": "Complete", "dataType": "boolean"} ],
    "editors": [
        {"type": "dropdown", "label": "Integration", "dataKey": "integration", "options": [ {"label": "Pinecone", "value": "pinecone"} ], "useInputToggleDataKey": "useIntegrationInput"},
        {"type": "string", "label": "Collection ID", "dataKey": "collectionId", "useInputToggleDataKey": "useCollectionIdInput"},
    ],
    "body": "Integration: {{#if useIntegrationInput}}(using input){{#else}}{{integration}}{{/if}}\nCollection Id: {{#if useCollectionIdInput}}(using input){{#else}}{{collectionId}}{{/if}}",
}
