from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "getAllDatasets",
    "title": "Get All Datasets",
    "displayName": "Get All Datasets",
    "data": {},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Retrieves all datasets. If no datasets exist, it returns an empty array.",
        "infoBoxTitle": "Get All Datasets Node",
        "contextMenuTitle": "Get All Datasets",
        "group": ["Input/Output"],
    },
    "inputs": [],
    "outputs": [ {"id": "datasets", "title": "Datasets", "dataType": "object[]"} ],
}

