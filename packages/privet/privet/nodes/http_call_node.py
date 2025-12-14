from __future__ import annotations

from typing import Any, Dict

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
        return await super().process(inputs)
