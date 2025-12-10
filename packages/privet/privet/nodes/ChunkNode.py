from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "chunk",
    "title": "Chunk",
    "displayName": "Chunk",
    "data": {"model": "gpt-4o", "useModelInput": False, "numTokensPerChunk": 1024, "overlap": 0},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Splits input text into chunks based on approximate token count; optional overlap.",
        "infoBoxTitle": "Chunk Node",
        "contextMenuTitle": "Chunk",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "string"},
        {"id": "model", "title": "Model", "dataType": "string", "showIf": {"dataKey": "useModelInput", "equals": True}},
    ],
    "outputs": [
        {"id": "chunks", "title": "Chunks", "dataType": "string[]"},
        {"id": "first", "title": "First", "dataType": "string"},
        {"id": "last", "title": "Last", "dataType": "string"},
        {"id": "indexes", "title": "Indexes", "dataType": "number[]"},
        {"id": "count", "title": "Count", "dataType": "number"},
    ],
    "editors": [
        {"type": "dropdown", "label": "Model", "dataKey": "model", "options": [ {"label": "gpt-4o", "value": "gpt-4o"}, {"label": "gpt-4.1", "value": "gpt-4.1"} ], "useInputToggleDataKey": "useModelInput"},
        {"type": "number", "label": "Number of tokens per chunk", "dataKey": "numTokensPerChunk", "min": 1, "max": 32768, "step": 1},
        {"type": "number", "label": "Overlap (in %)", "dataKey": "overlap", "min": 0, "max": 100, "step": 1},
    ],
    "body": "Model: {{model}}\nToken Count: {{numTokensPerChunk}}\n{{#if overlap}}Overlap: {{overlap}}%{{/if}}",
}

