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

class ExtractYAMLSchema(NodeSchema):
    NODE_TYPE = 'extractYaml'
    TITLE = 'Extract YAML'
    DISPLAY_NAME = 'Extract YAML'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Objects']
    UI_INFOBOX_TITLE = 'Extract YAML Node'
    UI_INFOBOX_BODY = 'Finds and parses a YAML object in the input text with a configured root property name.'
    UI_CONTEXT_MENU_TITLE = 'Extract YAML'
    DATA = {'rootPropertyName': 'yamlDocument', 'useRootPropertyNameInput': False, 'objectPath': None, 'useObjectPathInput': False}
    EDITORS = [{'type': 'string', 'label': 'Root Property Name', 'dataKey': 'rootPropertyName', 'useInputToggleDataKey': 'useRootPropertyNameInput'}, {'type': 'code', 'label': 'Object Path', 'dataKey': 'objectPath', 'language': 'jsonpath', 'useInputToggleDataKey': 'useObjectPathInput'}]
    BODY = 'Root: {{#if useRootPropertyNameInput}}(Using Input){{#else}}{{rootPropertyName}}{{/if}}\n{{#if useObjectPathInput}}Path: (Using Input){{#else}}{{#if objectPath}}Path: {{objectPath}}{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Input',
            required=True,
        ),
        Input(
            id='rootPropertyName',
            data_type='string',
            title='Root Property Name',
            show_if=Eq(data_key='useRootPropertyNameInput', equals=True),
        ),
        Input(
            id='objectPath',
            data_type='string',
            title='Object Path',
            show_if=Eq(data_key='useObjectPathInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='object',
            title='Output',
        ),
        Output(
            id='matches',
            data_type='any[]',
            title='Matches',
        ),
        Output(
            id='noMatch',
            data_type='string',
            title='No Match',
        ),
    ]



@bindschema(schema=ExtractYAMLSchema)
class ExtractYAMLNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
