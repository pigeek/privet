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
        import re
        import yaml
        from jsonpath_ng import parse as jsonpath_parse
        from ..utils.data_values import expect_type, coerce_type_optional

        input_string = expect_type(inputs.get('input'), 'string')
        data = self.node.data or {}

        # Get root property name from input or data
        root_property_name = (
            coerce_type_optional(inputs.get('rootPropertyName'), 'string')
            if data.get('useRootPropertyNameInput')
            else data.get('rootPropertyName', 'yamlDocument')
        )

        # Get object path from input or data
        object_path = (
            coerce_type_optional(inputs.get('objectPath'), 'string')
            if data.get('useObjectPathInput')
            else data.get('objectPath')
        )

        # Find the root property in the text
        pattern = re.compile(f'^{re.escape(root_property_name)}:', re.MULTILINE)
        match = pattern.search(input_string)

        if not match:
            return {
                'noMatch': {'type': 'string', 'value': input_string},
                'output': {'type': 'control-flow-excluded', 'value': None},
                'matches': {'type': 'control-flow-excluded', 'value': None},
            }

        root_property_start = match.start()
        next_lines = input_string[root_property_start:].split('\n')
        yaml_lines = [next_lines.pop(0)]  # First line with root property

        # Collect indented lines
        while next_lines and (next_lines[0].startswith(' ') or next_lines[0].startswith('\t') or next_lines[0] == ''):
            yaml_lines.append(next_lines.pop(0))

        potential_yaml = '\n'.join(yaml_lines)

        # Parse YAML
        try:
            yaml_object = yaml.safe_load(potential_yaml)
        except yaml.YAMLError:
            return {
                'noMatch': {'type': 'string', 'value': potential_yaml},
                'output': {'type': 'control-flow-excluded', 'value': None},
                'matches': {'type': 'control-flow-excluded', 'value': None},
            }

        if not isinstance(yaml_object, dict) or root_property_name not in yaml_object:
            return {
                'noMatch': {'type': 'string', 'value': potential_yaml},
                'output': {'type': 'control-flow-excluded', 'value': None},
                'matches': {'type': 'control-flow-excluded', 'value': None},
            }

        matches = []
        result_object = yaml_object

        # Apply JSONPath if specified
        if object_path:
            try:
                jsonpath_expr = jsonpath_parse(object_path.strip())
                matched_values = [match.value for match in jsonpath_expr.find(yaml_object)]
                matches = matched_values
                result_object = matched_values[0] if matched_values else None
            except Exception:
                return {
                    'noMatch': {'type': 'string', 'value': potential_yaml},
                    'output': {'type': 'control-flow-excluded', 'value': None},
                    'matches': {'type': 'control-flow-excluded', 'value': None},
                }

        return {
            'output': {
                'type': 'control-flow-excluded' if result_object is None else ('any' if object_path else 'object'),
                'value': result_object,
            },
            'noMatch': {'type': 'control-flow-excluded', 'value': None},
            'matches': {'type': 'any[]', 'value': matches},
        }
