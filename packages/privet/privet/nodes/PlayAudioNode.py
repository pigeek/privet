from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "playAudio",
    "title": "Play Audio",
    "displayName": "Play Audio",
    "data": {},
    "visual": {"width": 200},
    "uiData": {
        "contextMenuTitle": "Play Audio",
        "group": "Input/Output",
        "infoBoxTitle": "Play Audio Node",
        "infoBoxBody": "Plays audio data to the speakers.",
    },
    "inputs": [
        {"id": "data", "title": "Data", "dataType": "audio"},
    ],
    "outputs": [
        {"id": "data", "title": "Audio Data", "dataType": "audio"},
    ],
}

