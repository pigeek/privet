from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "loopUntil",
    "title": "Loop Until",
    "displayName": "Loop Until",
    "data": {
        "targetGraph": None,
        "useTargetGraphInput": False,
        "conditionType": "allOutputsSet",
        "maxIterations": None,
        "useMaxIterationsInput": False,
        "inputToCheck": None,
        "useInputToCheckInput": False,
        "targetValue": None,
        "useTargetValueInput": False,
    },
    "visual": {"width": 225},
    "uiData": {
        "infoBoxBody": "Executes a subgraph repeatedly until a condition is met. Outputs the final graph outputs, iteration count, and completion flag.",
        "infoBoxTitle": "Loop Until Node",
        "contextMenuTitle": "Loop Until",
        "group": ["Logic"],
    },
    "inputs": [
        {"id": "targetGraph", "title": "Target Graph", "dataType": "string", "showIf": {"dataKey": "useTargetGraphInput", "equals": True}},
        {"id": "maxIterations", "title": "Max Iterations", "dataType": "number", "showIf": {"dataKey": "useMaxIterationsInput", "equals": True}},
        {"id": "inputToCheck", "title": "Input To Check", "dataType": "string", "showIf": {"all": [ {"dataKey": "useInputToCheckInput", "equals": True}, {"dataKey": "conditionType", "equals": "inputEqual"} ]}},
        {"id": "targetValue", "title": "Target Value", "dataType": "string", "showIf": {"all": [ {"dataKey": "useTargetValueInput", "equals": True}, {"dataKey": "conditionType", "equals": "inputEqual"} ]}},
    ],
    "outputs": [
        {"id": "iteration", "title": "Iterations", "dataType": "number"},
        {"id": "completed", "title": "Completed", "dataType": "boolean"},
        {"id": "_subgraphOutputs", "title": "{{id}}", "dataType": "any", "variadic": {"type": "subgraph", "graphIdDataKey": "targetGraph"}},
    ],
    "dynamicInputsFromSubgraph": {"graphIdDataKey": "targetGraph"},
    "editors": [
        {"type": "graphSelector", "label": "Target Graph", "dataKey": "targetGraph", "useInputToggleDataKey": "useTargetGraphInput"},
        {"type": "dropdown", "label": "Condition", "dataKey": "conditionType", "options": [ {"label": "All Outputs Set", "value": "allOutputsSet"}, {"label": "Input Equals", "value": "inputEqual"} ]},
        {"type": "number", "label": "Max Iterations", "dataKey": "maxIterations", "useInputToggleDataKey": "useMaxIterationsInput", "allowEmpty": True},
        {"type": "string", "label": "Input To Check", "dataKey": "inputToCheck", "useInputToggleDataKey": "useInputToCheckInput"},
        {"type": "string", "label": "Target Value", "dataKey": "targetValue", "useInputToggleDataKey": "useTargetValueInput"},
    ],
    "body": "{{#if targetGraph}}{{targetGraph}}{{#else}}(No target graph){{/if}}\nCondition: {{#if (conditionType == 'inputEqual')}}{{inputToCheck}} == {{targetValue}}{{#else}}All outputs set{{/if}}",
}
