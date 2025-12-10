from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "text",
    "title": "Text",
    "displayName": "Text",
    "data": {"text": "{{input}}", "normalizeLineEndings": True},
    "visual": {"width": 300},
    "uiData": {
        "infoBoxBody": (
            "Outputs a string of text. It can also interpolate values using {{tags}}.\n\n"
            "The inputs are dynamic based on the interpolation tags."
        ),
        "contextMenuTitle": "Text",
        "infoBoxTitle": "Text Node",
        "group": ["Common", "Text"],
    },
    "inputs": [],
    "outputs": [
        {"id": "output", "title": "Output", "dataType": "string"},
    ],
    "editors": [
        {"type": "custom", "label": "AI Assist", "customEditorId": "TextNodeAiAssist"},
        {"type": "code", "label": "Text", "dataKey": "text", "language": "prompt-interpolation-markdown", "theme": "prompt-interpolation"},
        {"type": "toggle", "label": "Normalize Line Endings", "dataKey": "normalizeLineEndings"},
    ],
    "body": {"type": "colorized", "language": "prompt-interpolation-markdown", "theme": "prompt-interpolation", "text": "{{text}}"},
    "interpolationInputs": {"dataKey": "text", "dataType": "string", "ignorePrefixes": ["@graphInputs.", "@context."]},
}

