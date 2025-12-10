from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "replaceDataset",
    "title": "Replace Dataset",
    "displayName": "Replace Dataset",
    "data": {"datasetId": "", "useDatasetIdInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Replaces the data in a dataset with the given data. If no data is given, the dataset will be cleared instead.",
        "infoBoxTitle": "Replace Dataset Node",
        "contextMenuTitle": "Replace Dataset",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "data", "title": "Data", "dataType": "object[]"},
        {"id": "datasetId", "title": "Dataset ID", "dataType": "string", "showIf": {"dataKey": "useDatasetIdInput", "equals": True}},
    ],
    "outputs": [ {"id": "dataset", "title": "Dataset", "dataType": "object[]", "description": "Array of rows ({ id, data })."} ],
    "editors": [
        {"type": "datasetSelector", "label": "Dataset", "dataKey": "datasetId", "useInputToggleDataKey": "useDatasetIdInput"},
    ],
}

