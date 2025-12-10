from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "graphReference",
    "title": "Graph Reference",
    "displayName": "Graph Reference",
    "data": {"graphId": "", "useGraphIdOrNameInput": False},
    "visual": {"width": 275},
    "uiData": {
        "infoBoxBody": "Gets a reference to another graph, that can be used to pass around graphs to call using a Call Graph node.",
        "infoBoxTitle": "Graph Reference Node",
        "contextMenuTitle": "Graph Reference",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "graph-name-or-id", "title": "Graph Name Or ID", "dataType": "string", "required": True, "showIf": {"dataKey": "useGraphIdOrNameInput", "equals": True}},
    ],
    "outputs": [
        {"id": "graph", "title": "Graph", "dataType": "graph-reference"},
    ],
    "editors": [
        {"type": "graphSelector", "label": "Graph", "dataKey": "graphId", "useInputToggleDataKey": "useGraphIdOrNameInput"},
    ],
    "body": "{{#if useGraphIdOrNameInput}}(Graph from input){{#else}}{{#if graphId}}{{graphId}}{{#else}}(No graph selected){{/if}}{{/if}}",
}
