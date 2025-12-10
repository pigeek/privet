from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "loadDataset",
    "title": "Load Dataset",
    "displayName": "Load Dataset",
    "data": {"datasetId": "", "useDatasetIdInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Loads a dataset with the provided ID. If the dataset does not exist, it throws an error.",
        "infoBoxTitle": "Load Dataset Node",
        "contextMenuTitle": "Load Dataset",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "datasetId", "title": "Dataset ID", "dataType": "string", "showIf": {"dataKey": "useDatasetIdInput", "equals": True}},
    ],
    "outputs": [
        {"id": "dataset", "title": "Dataset", "dataType": "object[]"},
        {"id": "datasetId_out", "title": "Dataset ID", "dataType": "string"},
    ],
    "editors": [
        {"type": "datasetSelector", "label": "Dataset", "dataKey": "datasetId", "useInputToggleDataKey": "useDatasetIdInput"},
    ],
}

