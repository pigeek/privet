from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "extractRegex",
    "title": "Extract Regex",
    "displayName": "Extract Regex",
    "data": {"regex": "([a-zA-Z]+)", "useRegexInput": False, "errorOnFailed": False, "multilineMode": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Extracts data using a configured regular expression; capture groups become outputs.",
        "infoBoxTitle": "Extract With Regex Node",
        "contextMenuTitle": "Extract With Regex",
        "group": ["Text"],
    },
    "inputs": [
        {"id": "input", "title": "Input", "dataType": "string", "required": True, "coerced": False},
        {"id": "regex", "title": "Regex", "dataType": "string", "showIf": {"dataKey": "useRegexInput", "equals": True}, "coerced": False},
    ],
    "outputs": [
        {"id": "matches", "title": "Matches", "dataType": "string[]"},
        {"id": "succeeded", "title": "Succeeded", "dataType": "boolean"},
        {"id": "failed", "title": "Failed", "dataType": "boolean"},
        {"id": "output", "title": "Output {n}", "dataType": "string", "variadic": {"type": "regex", "baseId": "output", "titlePattern": "Output {n}", "startAt": 1, "regexDataKey": "regex", "multilineDataKey": "multilineMode"}},
    ],
    "editors": [
        {"type": "custom", "customEditorId": "ExtractRegexNodeAiAssist", "label": "AI Assist"},
        {"type": "toggle", "label": "Error on failed", "dataKey": "errorOnFailed"},
        {"type": "toggle", "label": "Multiline mode", "dataKey": "multilineMode"},
        {"type": "code", "label": "Regex", "dataKey": "regex", "useInputToggleDataKey": "useRegexInput", "language": "regex"},
    ],
    "body": "{{#if useRegexInput}}(Using regex input){{#else}}{{regex}}{{/if}}",
}
