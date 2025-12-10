from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "createDataset",
    "title": "Create Dataset",
    "displayName": "Create Dataset",
    "data": {},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Creates a new dataset with the provided ID and name. If the dataset already exists, it does nothing.",
        "infoBoxTitle": "Create Dataset Node",
        "contextMenuTitle": "Create Dataset",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "datasetId", "title": "Dataset ID", "dataType": "string"},
        {"id": "datasetName", "title": "Dataset Name", "dataType": "string"},
    ],
    "outputs": [
        {"id": "datasetId_out", "title": "Dataset ID", "dataType": "string"},
    ],
}

