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

class ObjectSchema(NodeSchema):
    NODE_TYPE = 'object'
    TITLE = 'Object'
    DISPLAY_NAME = 'Object'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Objects']
    UI_INFOBOX_TITLE = 'Object Node'
    UI_INFOBOX_BODY = 'Creates an object (or array) from input values and a JSON template, inserting values via interpolation.'
    UI_CONTEXT_MENU_TITLE = 'Object'
    DATA = {'jsonTemplate': '{\n  "key": "{{input}}"\n}'}
    EDITORS = [{'type': 'custom', 'customEditorId': 'ObjectNodeAiAssist', 'label': 'AI Assist'}, {'type': 'code', 'label': 'JSON Template', 'dataKey': 'jsonTemplate', 'language': 'json', 'theme': 'prompt-interpolation'}]
    BODY = '{{jsonTemplate}}'

    INPUTS = [

    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type=['object', 'object[]'],
            title='Output',
        ),
    ]



@bindschema(schema=ObjectSchema)
class ObjectNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import json
        import re

        # Get the JSON template
        json_template = self.node.data.get('jsonTemplate', '{"key": "{{input}}"}')

        # Unwrap all input values
        input_map = {}
        for key, value in (inputs or {}).items():
            if isinstance(value, dict) and 'value' in value:
                input_map[key] = value['value']
            else:
                input_map[key] = value

        # Get graph inputs and context values from context
        graph_input_values = self.context.get('graph_input_node_values', {})
        context_values = self.context.get('context_values', {})

        # Interpolate the template
        interpolated_string = self._interpolate(
            json_template,
            input_map,
            graph_input_values,
            context_values
        )

        # Parse the JSON
        try:
            output_value = json.loads(interpolated_string)
        except json.JSONDecodeError as err:
            raise ValueError(f"Failed to parse JSON template: {str(err)}")

        # Determine output type
        output_type = 'object[]' if isinstance(output_value, list) else 'object'

        return {
            'output': {
                'type': output_type,
                'value': output_value,
            }
        }

    def _interpolate(
        self,
        base_string: str,
        values: dict,
        graph_input_values: dict,
        context_values: dict
    ) -> str:
        """
        Interpolate {{placeholders}} in the template string.
        Handles quoted and unquoted placeholders, @graphInputs., and @context. references.
        """
        import json
        import re

        def replacer(match):
            open_quote = match.group(1)
            key = match.group(2)
            close_quote = match.group(3)

            is_quoted = bool(open_quote)
            trimmed_key = key.strip()

            # Resolve value
            value = None
            if trimmed_key.startswith('@graphInputs.'):
                prop_path = trimmed_key[len('@graphInputs.'):]
                value = self._resolve_path(graph_input_values, prop_path)
            elif trimmed_key.startswith('@context.'):
                prop_path = trimmed_key[len('@context.'):]
                value = self._resolve_path(context_values, prop_path)
            else:
                value = values.get(trimmed_key)

            # Handle None
            if value is None:
                return 'null'

            # Handle quoted strings
            if is_quoted and isinstance(value, str):
                return json.dumps(value)

            # Handle quoted non-strings (double stringify)
            if is_quoted:
                return json.dumps(json.dumps(value))

            # Unquoted values
            return json.dumps(value)

        # Replace all {{placeholder}} patterns
        pattern = r'("?)\{\{([^}]+?)\}\}("?)'
        return re.sub(pattern, replacer, base_string)

    def _resolve_path(self, obj: dict, path: str) -> Any:
        """Resolve a dotted path in a dictionary"""
        parts = path.split('.')
        current = obj

        for part in parts:
            if isinstance(current, dict):
                # Unwrap DataValue if needed
                if part in current:
                    current = current[part]
                    if isinstance(current, dict) and 'value' in current:
                        current = current['value']
                else:
                    return None
            else:
                return None

        return current
