from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "loopController",
    "title": "Loop Controller",
    "displayName": "Loop Controller",
    "data": {"maxIterations": 100, "atMaxIterationsAction": "error"},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": (
            "Defines the entry point for a loop. Values from inside the loop should be passed back "
            "through the Input ports; defaults can be set via the matching Default inputs.\n\n"
            "If the \"Continue\" input is falsey, the \"Break\" output runs."
        ),
        "infoBoxTitle": "Loop Controller Node",
        "contextMenuTitle": "Loop Controller",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "continue", "title": "Continue", "dataType": "any"},
        {"id": "input", "title": "Input {n}", "dataType": "any", "variadic": {"baseId": "input", "titlePattern": "Input {n}", "startAt": 1, "min": 1}},
        {"id": "inputDefault", "title": "Input {n} Default", "dataType": "any", "variadic": {"baseId": "input", "idPattern": "input{n}Default", "titlePattern": "Input {n} Default", "startAt": 1, "min": 1}},
    ],
    "outputs": [
        {"id": "break", "title": "Break", "dataType": "any"},
        {"id": "iteration", "title": "Iteration", "dataType": "number"},
        {"id": "output", "title": "Output {n}", "dataType": "any", "variadic": {"type": "mirror", "inputBaseId": "input", "baseId": "output", "titlePattern": "Output {n}", "startAt": 1, "excludeLast": True}},
    ],
    "editors": [
        {"type": "number", "label": "Max Iterations", "dataKey": "maxIterations", "min": 1, "step": 1, "defaultValue": 100},
        {"type": "dropdown", "label": "At Max Iterations", "dataKey": "atMaxIterationsAction", "defaultValue": "error", "options": [ {"label": "Break", "value": "break"}, {"label": "Error", "value": "error"} ]},
    ],
}
