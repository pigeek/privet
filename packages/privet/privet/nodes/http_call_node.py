from __future__ import annotations

from typing import Any, Dict, Optional
import json

import httpx

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import (
    Input,
    VariadicInput,
    Output,
    Eq,
    All,
    Any_,
    RawShowIf,
    NodeSchema,
)
from ..utils import get_input_or_data

class HttpCallSchema(NodeSchema):
    NODE_TYPE = 'httpCall'
    TITLE = 'Http Call'
    DISPLAY_NAME = 'Http Call'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'HTTP Call Node'
    UI_INFOBOX_BODY = 'Makes an HTTP call to the specified URL with the given method, headers, and body.'
    UI_CONTEXT_MENU_TITLE = 'HTTP Call'
    DATA = {'method': 'GET', 'url': '', 'headers': '', 'body': '', 'errorOnNon200': True, 'isBinaryOutput': False, 'useMethodInput': False, 'useUrlInput': False, 'useHeadersInput': False, 'useBodyInput': False}
    EDITORS = [{'type': 'dropdown', 'label': 'Method', 'dataKey': 'method', 'useInputToggleDataKey': 'useMethodInput', 'options': [{'label': 'GET', 'value': 'GET'}, {'label': 'POST', 'value': 'POST'}, {'label': 'PUT', 'value': 'PUT'}, {'label': 'DELETE', 'value': 'DELETE'}]}, {'type': 'string', 'label': 'URL', 'dataKey': 'url', 'useInputToggleDataKey': 'useUrlInput'}, {'type': 'code', 'label': 'Headers', 'dataKey': 'headers', 'useInputToggleDataKey': 'useHeadersInput', 'language': 'json'}, {'type': 'code', 'label': 'Body', 'dataKey': 'body', 'useInputToggleDataKey': 'useBodyInput', 'language': 'json'}, {'type': 'toggle', 'label': 'Binary Output', 'dataKey': 'isBinaryOutput'}, {'type': 'toggle', 'label': 'Error on non-200 status code', 'dataKey': 'errorOnNon200'}]
    BODY = '{{#if useMethodInput}}(Method Using Input){{#else}}{{method}}{{/if}} {{#if useUrlInput}}(URL Using Input){{#else}}{{url}}{{/if}}\n{{#if useHeadersInput}}Headers: (Using Input){{#else}}{{#if headers}}Headers: {{headers}}{{/if}}{{/if}}\n{{#if useBodyInput}}Body: (Using Input){{#else}}{{#if body}}Body: {{body}}{{/if}}{{/if}}\n{{#if errorOnNon200}}Error on non-200{{/if}}'

    INPUTS = [
        Input(
            id='method',
            data_type='string',
            title='Method',
            show_if=Eq(data_key='useMethodInput', equals=True),
        ),
        Input(
            id='url',
            data_type='string',
            title='URL',
            show_if=Eq(data_key='useUrlInput', equals=True),
        ),
        Input(
            id='headers',
            data_type='object',
            title='Headers',
            show_if=Eq(data_key='useHeadersInput', equals=True),
        ),
        Input(
            id='req_body',
            data_type='string',
            title='Body',
            show_if=Eq(data_key='useBodyInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='binary',
            data_type='binary',
            title='Binary',
            show_if=Eq(data_key='isBinaryOutput', equals=True),
        ),
        Output(
            id='res_body',
            data_type='string',
            title='Body',
            show_if=Eq(data_key='isBinaryOutput', equals=False),
        ),
        Output(
            id='json',
            data_type='object',
            title='JSON',
            show_if=Eq(data_key='isBinaryOutput', equals=False),
        ),
        Output(
            id='statusCode',
            data_type='number',
            title='Status Code',
        ),
        Output(
            id='res_headers',
            data_type='object',
            title='Headers',
        ),
    ]



@bindschema(schema=HttpCallSchema)
class HttpCallNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        data = self.node.data or {}

        # Resolve configured vs. input-driven values
        method = (get_input_or_data(data, inputs, "method", "string", "useMethodInput") or "GET").upper()
        url = get_input_or_data(data, inputs, "url", "string", "useUrlInput") or ""

        raw_headers: Optional[Any] = get_input_or_data(data, inputs, "headers", None, "useHeadersInput")
        headers: Dict[str, str] = {}
        if isinstance(raw_headers, str) and raw_headers.strip():
            try:
                headers = json.loads(raw_headers)
            except Exception:
                headers = {}
        elif isinstance(raw_headers, dict):
            headers = {str(k): str(v) for k, v in raw_headers.items()}
        elif raw_headers is None and isinstance(data.get("headers"), str) and data.get("headers").strip():
            try:
                headers = json.loads(data["headers"])
            except Exception:
                headers = {}

        body_value: Optional[Any]
        if data.get("useBodyInput"):
            body_value = inputs.get("req_body")
            if isinstance(body_value, dict) and "type" in body_value:
                # Coerce DataValue wrapper
                body_value = body_value.get("value")
        else:
            body_value = data.get("body")

        content: Optional[bytes | str] = None
        if body_value is None or body_value == "":
            content = None
        elif isinstance(body_value, (dict, list)):
            content = json.dumps(body_value)
            headers.setdefault("content-type", "application/json")
        else:
            content = str(body_value)

        timeout = httpx.Timeout(30.0, connect=10.0)

        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
                response = await client.request(method, url, headers=headers or None, content=content)

            status_code = response.status_code
            if data.get("errorOnNon200", True) and not (200 <= status_code < 300):
                response.raise_for_status()

            out: Dict[str, Any] = {
                "statusCode": {"type": "number", "value": status_code},
                "res_headers": {
                    "type": "object",
                    "value": {k.lower(): v for k, v in response.headers.items()},
                },
            }

            if data.get("isBinaryOutput"):
                out["binary"] = {"type": "binary", "value": response.content}
            else:
                text = response.text
                out["res_body"] = {"type": "string", "value": text}

                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type.lower():
                    try:
                        out["json"] = {"type": "object", "value": response.json()}
                    except Exception:
                        out["json"] = {"type": "control-flow-excluded", "value": None}
                else:
                    out["json"] = {"type": "control-flow-excluded", "value": None}

            return out
        except httpx.HTTPError as exc:
            # Return explicit error details without crashing the graph
            error_message = f"HTTP request failed: {exc}"
            return {
                "statusCode": {"type": "number", "value": 0},
                "res_headers": {"type": "object", "value": headers or {}},
                "res_body": {"type": "string", "value": error_message},
                "json": {"type": "object", "value": {"error": error_message}},
            }
