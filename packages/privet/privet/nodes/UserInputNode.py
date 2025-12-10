from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "userInput",
    "title": "User Input",
    "displayName": "User Input",
    "data": {"prompt": "This is an example question?", "useInput": False, "renderingFormat": "markdown"},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Prompts the user for input during execution; response becomes output.",
        "infoBoxTitle": "User Input Node",
        "contextMenuTitle": "User Input",
        "group": ["Input/Output"],
    },
    "inputs": [
        {"id": "questions", "title": "Questions", "dataType": "string[]", "showIf": {"dataKey": "useInput", "equals": True}},
    ],
    "outputs": [
        {"id": "output", "title": "Answers Only", "dataType": "string[]"},
        {"id": "questionsAndAnswers", "title": "Q & A", "dataType": "string[]"},
    ],
    "editors": [
        {"type": "code", "label": "Prompt", "dataKey": "prompt", "useInputToggleDataKey": "useInput", "language": "plain-text"},
        {"type": "group", "label": "Rendering", "editors": [
            {"type": "dropdown", "dataKey": "renderingFormat", "label": "Format", "options": [
                {"label": "Preformatted", "value": "preformatted"},
                {"label": "Markdown", "value": "markdown"}
            ]}
        ]},
    ],
    "body": "{{#if useInput}}(Using input){{#else}}{{prompt}}{{/if}}",
}
