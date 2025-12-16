from __future__ import annotations

from typing import Any, Dict
from dataclasses import dataclass, field

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import (
    Input,
    VariadicInput,
    Output,
    Eq,
    NodeSchema,
    Toggle,
    Code,
    Editor,
)


@dataclass
class JoinConfig:
    flatten: bool = Editor(
        editor=Toggle(
            label="Flatten",
        ),
        default=True,
    )
    joinString: str = Editor(
        editor=Code(
            label="Join String",
            language="plaintext",
            use_input_toggle="useJoinStringInput",
        ),
        default="\n",
    )
    useJoinStringInput: bool = field(default=False)


class JoinSchema(NodeSchema):
    NODE_TYPE = "join"

    # UI metadata
    TITLE = "Join"
    DISPLAY_NAME = "Join"
    VISUAL_WIDTH = 150
    UI_GROUP = ["Text"]
    UI_INFOBOX_TITLE = "Join Node"
    UI_INFOBOX_BODY = (
        "Takes an array of strings, and joins them using the configured delimiter.\n\n"
        "Defaults to a newline."
    )
    UI_CONTEXT_MENU_TITLE = "Join"

    # Body
    BODY = (
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
    )

    # Config dataclass
    Config = JoinConfig

    # Port descriptors
    INPUTS = [
        Input(
            id="joinString",
            data_type="string",
            title="Join String",
            show_if=Eq(
                data_key="useJoinStringInput",
                equals=True,
            ),
        ),
        VariadicInput(
            base_id="input",
            data_type="string",
            title="Input",
            title_pattern="Input {n}",
            start_at=1,
            min=1,
        ),
    ]
    OUTPUTS = [
        Output(
            id="output",
            data_type="string",
            title="Joined",
        )
    ]

@bindschema(schema=JoinSchema)
class JoinNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        from ..utils.data_values import coerce_type, coerce_type_optional

        # Get join string from input or data
        join_string = self.node.data.get('joinString', '\n')
        if self.node.data.get('useJoinStringInput'):
            input_join = coerce_type_optional(inputs.get('joinString'), 'string')
            if input_join is not None:
                join_string = input_join

        # Handle escape characters (\n, \t, etc.)
        join_string = join_string.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')

        # Collect all input values
        input_values = []
        flatten = self.node.data.get('flatten', True)

        # Get all inputs that start with 'input'
        input_keys = sorted([k for k in (inputs or {}).keys() if k.startswith('input')])

        for key in input_keys:
            input_value = inputs[key]

            # Check if it's an array and should be flattened
            if isinstance(input_value, dict) and input_value.get('type', '').endswith('[]') and flatten:
                # Flatten the array
                array_values = input_value.get('value', [])
                for val in array_values:
                    input_values.append(str(val))
            else:
                # Coerce to string
                str_value = coerce_type(input_value, 'string')
                input_values.append(str_value)

        # Join all values
        output_value = join_string.join(input_values)

        return {
            'output': {
                'type': 'string',
                'value': output_value,
            }
        }
