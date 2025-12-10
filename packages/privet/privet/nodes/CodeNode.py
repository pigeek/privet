from typing import Any, Dict

# UI-only code node. Execution is remote; outputs are driven by a data list.
SPEC: Dict[str, Any] = {
    "type": "code",
    "title": "Code",
    "displayName": "Code",
    "data": {
        "code": "// Write JavaScript here. Inputs available as inputs.input{n}\nreturn { output1: { type: 'any', value: inputs.input1?.value } };",
        "inputNames": ["input1"],
        "outputNames": ["output1"],
        "allowFetch": False,
        "allowRequire": False,
        "allowRivet": False,
        "allowProcess": False,
        "allowConsole": False,
    },
    "visual": {"width": 420},
    "uiData": {
        "infoBoxBody": "Executes custom JavaScript remotely. Port names are configured via Inputs/Outputs lists for display; UI ports are generic and runtime maps values by position.",
        "infoBoxTitle": "Code Node",
        "contextMenuTitle": "Code",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "input", "title": "Input {n}", "dataType": "string", "variadic": {"baseId": "input", "titlePattern": "Input {n}", "startAt": 1, "min": 0}},
    ],
    "outputs": [
        {"id": "output", "title": "{{item}}", "dataType": "any", "variadic": {"type": "dataList", "dataKey": "outputNames", "baseId": "output", "titleTemplate": "{{item}}", "idTemplate": "{{item}}"}},
    ],
    "editors": [
        {"type": "custom", "customEditorId": "CodeNodeAIAssist", "label": "AI Assist"},
        {"type": "code", "label": "Code", "dataKey": "code", "language": "javascript"},
        {"type": "stringList", "label": "Inputs", "dataKey": "inputNames"},
        {"type": "stringList", "label": "Outputs", "dataKey": "outputNames"},
        {"type": "toggle", "label": "Allow using `fetch`", "dataKey": "allowFetch"},
        {"type": "toggle", "label": "Allow using `require`", "dataKey": "allowRequire"},
        {"type": "toggle", "label": "Allow using `Rivet`", "dataKey": "allowRivet"},
        {"type": "toggle", "label": "Allow using `process`", "dataKey": "allowProcess"},
        {"type": "toggle", "label": "Allow using `console`", "dataKey": "allowConsole"},
    ],
    "body": [
        {"type": "markdown", "text": "**Inputs:** {{#if inputNames}}{{inputNames}}{{#else}}(none){{/if}}"},
        {"type": "markdown", "text": "**Outputs:** {{#if outputNames}}{{outputNames}}{{#else}}(none){{/if}}"},
        {"type": "colorized", "text": "{{code}}", "language": "javascript", "fontSize": 12, "fontFamily": "monospace"},
    ],
}
