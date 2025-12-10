from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "httpCall",
    "title": "Http Call",
    "displayName": "Http Call",
    "data": {"method": "GET", "url": "", "headers": "", "body": "", "errorOnNon200": True, "isBinaryOutput": False, "useMethodInput": False, "useUrlInput": False, "useHeadersInput": False, "useBodyInput": False},
    "visual": {"width": 250},
    "uiData": {
        "infoBoxBody": "Makes an HTTP call to the specified URL with the given method, headers, and body.",
        "infoBoxTitle": "HTTP Call Node",
        "contextMenuTitle": "HTTP Call",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "method", "title": "Method", "dataType": "string", "showIf": {"dataKey": "useMethodInput", "equals": True}},
        {"id": "url", "title": "URL", "dataType": "string", "showIf": {"dataKey": "useUrlInput", "equals": True}},
        {"id": "headers", "title": "Headers", "dataType": "object", "showIf": {"dataKey": "useHeadersInput", "equals": True}},
        {"id": "req_body", "title": "Body", "dataType": "string", "showIf": {"dataKey": "useBodyInput", "equals": True}},
    ],
    "outputs": [
        {"id": "binary", "title": "Binary", "dataType": "binary", "showIf": {"dataKey": "isBinaryOutput", "equals": True}},
        {"id": "res_body", "title": "Body", "dataType": "string", "showIf": {"dataKey": "isBinaryOutput", "equals": False}},
        {"id": "json", "title": "JSON", "dataType": "object", "showIf": {"dataKey": "isBinaryOutput", "equals": False}},
        {"id": "statusCode", "title": "Status Code", "dataType": "number"},
        {"id": "res_headers", "title": "Headers", "dataType": "object"},
    ],
    "editors": [
        {"type": "dropdown", "label": "Method", "dataKey": "method", "useInputToggleDataKey": "useMethodInput", "options": [
            {"label": "GET", "value": "GET"}, {"label": "POST", "value": "POST"}, {"label": "PUT", "value": "PUT"}, {"label": "DELETE", "value": "DELETE"}
        ]},
        {"type": "string", "label": "URL", "dataKey": "url", "useInputToggleDataKey": "useUrlInput"},
        {"type": "code", "label": "Headers", "dataKey": "headers", "useInputToggleDataKey": "useHeadersInput", "language": "json"},
        {"type": "code", "label": "Body", "dataKey": "body", "useInputToggleDataKey": "useBodyInput", "language": "json"},
        {"type": "toggle", "label": "Binary Output", "dataKey": "isBinaryOutput"},
        {"type": "toggle", "label": "Error on non-200 status code", "dataKey": "errorOnNon200"},
    ],
    "body": (
        "{{#if useMethodInput}}(Method Using Input){{#else}}{{method}}{{/if}} {{#if useUrlInput}}(URL Using Input){{#else}}{{url}}{{/if}}\n"
        "{{#if useHeadersInput}}Headers: (Using Input){{#else}}{{#if headers}}Headers: {{headers}}{{/if}}{{/if}}\n"
        "{{#if useBodyInput}}Body: (Using Input){{#else}}{{#if body}}Body: {{body}}{{/if}}{{/if}}\n"
        "{{#if errorOnNon200}}Error on non-200{{/if}}"
    ),
}
