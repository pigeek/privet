from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "appendToDataset",
    "title": "Append to Dataset",
    "displayName": "Append to Dataset",
    "data": {"datasetId": "", "useDatasetIdInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Appends a row of data to the specified dataset.",
        "infoBoxTitle": "Append to Dataset Node",
        "contextMenuTitle": "Append to Dataset",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "data", "title": "Data", "dataType": "string[]"},
        {"id": "id", "title": "ID", "dataType": "string"},
        {"id": "embedding", "title": "Embedding", "dataType": "vector"},
        {"id": "datasetId", "title": "Dataset ID", "dataType": "string", "showIf": {"dataKey": "useDatasetIdInput", "equals": True}},
    ],
    "outputs": [
        {"id": "dataset", "title": "Dataset", "dataType": "object"},
        {"id": "id_out", "title": "ID", "dataType": "string"},
    ],
    "editors": [
        {"type": "datasetSelector", "label": "Dataset", "dataKey": "datasetId", "useInputToggleDataKey": "useDatasetIdInput"},
    ],
}
