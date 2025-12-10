from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "getDatasetRow",
    "title": "Get Dataset Row",
    "displayName": "Get Dataset Row",
    "data": {"datasetId": "", "useDatasetIdInput": False, "rowId": "", "useRowIdInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Gets a row from a dataset with the provided ID. If the dataset or row does not exist, it throws an error.",
        "infoBoxTitle": "Get Dataset Row Node",
        "contextMenuTitle": "Get Dataset Row",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "rowId", "title": "Row ID", "dataType": "string", "showIf": {"dataKey": "useRowIdInput", "equals": True}},
        {"id": "datasetId", "title": "Dataset ID", "dataType": "string", "showIf": {"dataKey": "useDatasetIdInput", "equals": True}},
    ],
    "outputs": [ {"id": "row", "title": "Row", "dataType": "object"} ],
    "editors": [
        {"type": "datasetSelector", "label": "Dataset", "dataKey": "datasetId", "useInputToggleDataKey": "useDatasetIdInput"},
        {"type": "string", "label": "Row ID", "dataKey": "rowId", "useInputToggleDataKey": "useRowIdInput"},
    ],
}

