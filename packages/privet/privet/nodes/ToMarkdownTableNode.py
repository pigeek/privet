from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "toMarkdownTable",
    "title": "To Markdown Table",
    "displayName": "To Markdown Table",
    "data": {"includeHeaders": True, "alignPipes": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Converts an array of objects into a markdown table.",
        "infoBoxTitle": "To Markdown Table Node",
        "contextMenuTitle": "To Markdown Table",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "data", "title": "Data Array", "dataType": "any", "required": True},
    ],
    "outputs": [
        {"id": "markdown", "title": "Markdown Table", "dataType": "string"},
    ],
    "editors": [
        {"type": "toggle", "label": "Include Headers", "dataKey": "includeHeaders"},
        {"type": "toggle", "label": "Align Pipes", "dataKey": "alignPipes"},
    ],
    "body": "{{#if includeHeaders}}With Header Row{{/if}}{{#if alignPipes}}{{#if includeHeaders}}, {{/if}}Pipes Aligned{{/if}}",
}

