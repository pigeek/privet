from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "array",
    "title": "Array",
    "displayName": "Array",
    "data": {"flatten": True, "flattenDeep": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": (
            "Creates an array from the input values. By default, flattens any input arrays. Can be configured to keep arrays separate or deeply flatten.\n\n"
            "The number of inputs is dynamic based on connections."
        ),
        "infoBoxTitle": "Array Node",
        "contextMenuTitle": "Array",
        "group": ["Lists"],
    },
    "inputs": [
        {
            "id": "input",
            "title": "Input {n}",
            "dataType": "any",
            "variadic": {"baseId": "input", "titlePattern": "Input {n}", "startAt": 1, "min": 1},
        }
    ],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "any[]", "description": "The array created from the inputs."},
        {"id": "indices", "title": "Indices", "dataType": "number[]", "description": "The indices of the output array."},
        {"id": "length", "title": "Length", "dataType": "number", "description": "The length of the output array."},
    ],
    "editors": [
        {"type": "toggle", "label": "Flatten", "dataKey": "flatten"},
        {"type": "toggle", "label": "Deep", "dataKey": "flattenDeep"},
    ],
    "body": "{{#if flatten}}{{#if flattenDeep}}Flatten (Deep){{#else}}Flatten{{/if}}{{#else}}No Flatten{{/if}}",
}
