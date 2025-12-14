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

class HashSchema(NodeSchema):
    NODE_TYPE = 'hash'
    TITLE = 'Hash'
    DISPLAY_NAME = 'Hash'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Data']
    UI_INFOBOX_TITLE = 'Hash Node'
    UI_INFOBOX_BODY = 'Computes a hash of the input using the selected algorithm.'
    UI_CONTEXT_MENU_TITLE = 'Hash'
    DATA = {'algorithm': 'sha256'}
    EDITORS = [{'type': 'dropdown', 'label': 'Algorithm', 'dataKey': 'algorithm', 'options': [{'value': 'md5', 'label': 'MD5'}, {'value': 'sha1', 'label': 'SHA1'}, {'value': 'sha256', 'label': 'SHA256'}, {'value': 'sha512', 'label': 'SHA512'}]}]
    BODY = '{{algorithm}}'

    INPUTS = [
        Input(
            id='input',
            data_type='string',
            title='Input',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='hash',
            data_type='string',
            title='Hash',
        ),
    ]



@bindschema(schema=HashSchema)
class HashNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import hashlib

        inputs = inputs or {}
        data = self.node.data or {}
        algorithm = (data.get("algorithm") or "sha256").lower()

        input_str = ""
        val = inputs.get("input")
        if isinstance(val, dict):
            raw = val.get("value")
        else:
            raw = val
        if raw is not None:
            input_str = str(raw)

        hasher = None
        if algorithm == "md5":
            hasher = hashlib.md5()
        elif algorithm == "sha1":
            hasher = hashlib.sha1()
        elif algorithm == "sha512":
            hasher = hashlib.sha512()
        else:
            hasher = hashlib.sha256()

        hasher.update(input_str.encode("utf-8"))
        digest = hasher.hexdigest()

        return {"hash": {"type": "string", "value": digest}}
