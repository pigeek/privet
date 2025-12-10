from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "extractMarkdownCodeBlocks",
    "title": "Extract Markdown Code Blocks",
    "displayName": "Extract Markdown Code Blocks",
    "data": {},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Extracts fenced code blocks and their languages from markdown.",
        "infoBoxTitle": "Extract Markdown Code Blocks Node",
        "contextMenuTitle": "Extract Markdown Code Blocks",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "string", "required": True},
    ],
    "outputs": [
        {"id": "firstBlock", "title": "First Block", "dataType": "string"},
        {"id": "allBlocks", "title": "All Blocks", "dataType": "string[]"},
        {"id": "languages", "title": "Languages", "dataType": "string[]"},
    ],
}
