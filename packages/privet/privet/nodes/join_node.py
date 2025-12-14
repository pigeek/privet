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
        # For now, just print (and optionally could concatenate strings later)
        return await super().process(inputs)
