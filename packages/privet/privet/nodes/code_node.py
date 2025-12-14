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

class CodeSchema(NodeSchema):
    NODE_TYPE = 'code'
    TITLE = 'Code'
    DISPLAY_NAME = 'Code'
    VISUAL_WIDTH = 420
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Code Node'
    UI_INFOBOX_BODY = 'Executes custom JavaScript remotely. Port names are configured via Inputs/Outputs lists for display; UI ports are generic and runtime maps values by position.'
    UI_CONTEXT_MENU_TITLE = 'Code'
    DATA = {'code': "// Write JavaScript here. Inputs available as inputs.input{n}\nreturn { output1: { type: 'any', value: inputs.input1?.value } };", 'inputNames': ['input1'], 'outputNames': ['output1'], 'allowFetch': False, 'allowRequire': False, 'allowRivet': False, 'allowProcess': False, 'allowConsole': False}
    EDITORS = [{'type': 'custom', 'customEditorId': 'CodeNodeAIAssist', 'label': 'AI Assist'}, {'type': 'code', 'label': 'Code', 'dataKey': 'code', 'language': 'javascript'}, {'type': 'stringList', 'label': 'Inputs', 'dataKey': 'inputNames'}, {'type': 'stringList', 'label': 'Outputs', 'dataKey': 'outputNames'}, {'type': 'toggle', 'label': 'Allow using `fetch`', 'dataKey': 'allowFetch'}, {'type': 'toggle', 'label': 'Allow using `require`', 'dataKey': 'allowRequire'}, {'type': 'toggle', 'label': 'Allow using `Rivet`', 'dataKey': 'allowRivet'}, {'type': 'toggle', 'label': 'Allow using `process`', 'dataKey': 'allowProcess'}, {'type': 'toggle', 'label': 'Allow using `console`', 'dataKey': 'allowConsole'}]
    BODY = [{'type': 'markdown', 'text': '**Inputs:** {{#if inputNames}}{{inputNames}}{{#else}}(none){{/if}}'}, {'type': 'markdown', 'text': '**Outputs:** {{#if outputNames}}{{outputNames}}{{#else}}(none){{/if}}'}, {'type': 'colorized', 'text': '{{code}}', 'language': 'javascript', 'fontSize': 12, 'fontFamily': 'monospace'}]

    INPUTS = [
        VariadicInput(
            id_value='input',
            base_id='input',
            data_type='string',
            title='Input {n}',
            title_pattern='Input {n}',
            start_at=1,
            min=0,
        ),
    ]

    OUTPUTS = [
        Output(
            id='output',
            data_type='any',
            title='{{item}}',
            variadic={'type': 'dataList', 'dataKey': 'outputNames', 'baseId': 'output', 'titleTemplate': '{{item}}', 'idTemplate': '{{item}}'},
        ),
    ]



@bindschema(schema=CodeSchema)
class CodeNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
