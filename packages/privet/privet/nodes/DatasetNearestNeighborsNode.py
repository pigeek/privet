from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "datasetNearestNeighbors",
    "title": "KNN Dataset",
    "displayName": "KNN Dataset",
    "data": {"datasetId": "", "useDatasetIdInput": False, "k": 5, "useKInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Finds the k nearest neighbors in the dataset with the provided ID, given an embedding.",
        "infoBoxTitle": "KNN Dataset Node",
        "contextMenuTitle": "KNN Dataset",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "embedding", "title": "Embedding", "dataType": "object"},
        {"id": "datasetId", "title": "Dataset ID", "dataType": "string", "showIf": {"dataKey": "useDatasetIdInput", "equals": True}},
        {"id": "k", "title": "K", "dataType": "number", "showIf": {"dataKey": "useKInput", "equals": True}},
    ],
    "outputs": [ {"id": "nearestNeighbors", "title": "Nearest Neighbors", "dataType": "object[]"} ],
    "editors": [
        {"type": "datasetSelector", "label": "Dataset", "dataKey": "datasetId", "useInputToggleDataKey": "useDatasetIdInput"},
        {"type": "number", "label": "K", "dataKey": "k", "useInputToggleDataKey": "useKInput"},
    ],
}
