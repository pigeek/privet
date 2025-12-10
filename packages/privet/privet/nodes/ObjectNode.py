from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "object",
    "title": "Object",
    "displayName": "Object",
    "data": {"jsonTemplate": '{\n  "key": "{{input}}"\n}'},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Creates an object (or array) from input values and a JSON template, inserting values via interpolation.",
        "infoBoxTitle": "Object Node",
        "contextMenuTitle": "Object",
        "group": ["Objects"],
    },
    "inputs": [],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": ["object", "object[]"]},
    ],
    "editors": [
        {"type": "custom", "customEditorId": "ObjectNodeAiAssist", "label": "AI Assist"},
        {"type": "code", "label": "JSON Template", "dataKey": "jsonTemplate", "language": "json", "theme": "prompt-interpolation"},
    ],
    "body": "{{jsonTemplate}}",
    "interpolationInputs": {"dataKey": "jsonTemplate", "dataType": "any", "ignorePrefixes": ["@graphInputs.", "@context."]},
}

