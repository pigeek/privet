from typing import Any, Dict

# Pure-data spec mirroring packages/core/src/model/Nodes.ts joinNode
SPEC: Dict[str, Any] = {
    "type": "join",
    "title": "Join",
    "displayName": "Join",
    "data": {"flatten": True, "joinString": "\n", "useJoinStringInput": False},
    "visual": {"width": 150},
    "uiData": {
        "infoBoxBody": (
            "Takes an array of strings, and joins them using the configured delimiter.\n\n"
            "Defaults to a newline."
        ),
        "infoBoxTitle": "Join Node",
        "contextMenuTitle": "Join",
        "group": ["Text"],
    },
    "inputs": [
        {
            "dataType": "string",
            "id": "joinString",
            "title": "Join String",
            "showIf": {"dataKey": "useJoinStringInput", "equals": True},
        },
        {
            "dataType": "string",
            "id": "input",
            "title": "Input",
            "variadic": {"baseId": "input", "titlePattern": "Input {n}", "startAt": 1, "min": 1},
        },
    ],
    "outputs": [
        {"dataType": "string", "id": "output", "title": "Joined"},
    ],
    "editors": [
        {"type": "toggle", "label": "Flatten", "dataKey": "flatten"},
        {
            "type": "code",
            "label": "Join String",
            "dataKey": "joinString",
            "useInputToggleDataKey": "useJoinStringInput",
            "showIf": {"dataKey": "useJoinStringInput", "equals": True},
            "language": "plaintext",
        },
    ],
    "body": (
        "{{#if useJoinStringInput}}\n"
        "  (Join value is input)\n"
        "{{#elseif joinString == \"\\n\"}}\n"
        "  (New line)\n"
        "{{#elseif joinString == \"\\t\"}}\n"
        "  (Tab)\n"
        "{{#elseif joinString == \" \"}}\n"
        "  (Space)\n"
        "{{#else}}\n"
        "  {{joinString}}\n"
        "{{/if}}\n"
    ),
}
