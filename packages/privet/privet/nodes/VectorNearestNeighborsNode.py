from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "vectorNearestNeighbors",
    "title": "Vector KNN",
    "displayName": "Vector KNN",
    "data": {"integration": "pinecone", "useIntegrationInput": False, "k": 10, "useKInput": False, "collectionId": "", "useCollectionIdInput": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "k-nearest neighbors search on stored vectors.",
        "infoBoxTitle": "Vector KNN Node",
        "contextMenuTitle": "Vector KNN",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "vector", "title": "Vector", "dataType": "vector", "required": True},
        {"id": "integration", "title": "Integration", "dataType": "string", "showIf": {"dataKey": "useIntegrationInput", "equals": True}},
        {"id": "collectionId", "title": "Collection ID", "dataType": "string", "showIf": {"dataKey": "useCollectionIdInput", "equals": True}},
        {"id": "k", "title": "K", "dataType": "number", "showIf": {"dataKey": "useKInput", "equals": True}},
    ],
    "outputs": [ {"id": "results", "title": "Results", "dataType": "any[]"} ],
    "editors": [
        {"type": "dropdown", "label": "Integration", "dataKey": "integration", "options": [ {"label": "Pinecone", "value": "pinecone"} ], "useInputToggleDataKey": "useIntegrationInput"},
        {"type": "number", "label": "K", "dataKey": "k", "min": 1, "max": 100, "step": 1, "defaultValue": 10, "useInputToggleDataKey": "useKInput"},
        {"type": "string", "label": "Collection ID", "dataKey": "collectionId", "useInputToggleDataKey": "useCollectionIdInput"},
    ],
    "body": "Integration: {{#if useIntegrationInput}}(using input){{#else}}{{integration}}{{/if}}\nK: {{#if useKInput}}(using input){{#else}}{{k}}{{/if}}\nCollection Id: {{#if useCollectionIdInput}}(using input){{#else}}{{collectionId}}{{/if}}",
}
