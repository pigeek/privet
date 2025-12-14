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

class ReadAllFilesSchema(NodeSchema):
    NODE_TYPE = 'readAllFiles'
    TITLE = 'Read All Files'
    DISPLAY_NAME = 'Read All Files'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Read All Files Node'
    UI_INFOBOX_BODY = 'Reads all files in a directory and outputs list of {path, content}.'
    UI_CONTEXT_MENU_TITLE = 'Read All Files'
    DATA = {'path': '', 'usePathInput': False, 'recursive': False, 'useRecursiveInput': False, 'filterGlobs': [], 'useFilterGlobsInput': False, 'ignores': [], 'useIgnoresInput': False, 'asBinary': False, 'errorOnMissingFile': False}
    EDITORS = [{'type': 'directoryBrowser', 'label': 'Path', 'dataKey': 'path', 'useInputToggleDataKey': 'usePathInput'}, {'type': 'toggle', 'label': 'Recursive', 'dataKey': 'recursive', 'useInputToggleDataKey': 'useRecursiveInput'}, {'type': 'stringList', 'label': 'Filter Globs', 'dataKey': 'filterGlobs', 'useInputToggleDataKey': 'useFilterGlobsInput'}, {'type': 'stringList', 'label': 'Ignores', 'dataKey': 'ignores', 'useInputToggleDataKey': 'useIgnoresInput'}, {'type': 'toggle', 'label': 'Read as Binary', 'dataKey': 'asBinary'}, {'type': 'toggle', 'label': 'Error on Missing File', 'dataKey': 'errorOnMissingFile'}]
    BODY = '{{#if asBinary}}Read as Binary{{#else}}Read as Text{{/if}}\nPath: {{#if usePathInput}}(Input){{#else}}{{path}}{{/if}}\nRecursive: {{#if useRecursiveInput}}(Input){{#else}}{{recursive}}{{/if}}\nFilters: {{#if useFilterGlobsInput}}(Input){{#else}}{{#if filterGlobs}}{{filterGlobs}}{{#else}}None{{/if}}{{/if}}'

    INPUTS = [
        Input(
            id='path',
            data_type='string',
            title='Path',
            show_if=Eq(data_key='usePathInput', equals=True),
        ),
        Input(
            id='recursive',
            data_type='boolean',
            title='Recursive',
            show_if=Eq(data_key='useRecursiveInput', equals=True),
        ),
        Input(
            id='filterGlobs',
            data_type='string[]',
            title='Filter Globs',
            show_if=Eq(data_key='useFilterGlobsInput', equals=True),
        ),
        Input(
            id='ignores',
            data_type='string[]',
            title='Ignores',
            show_if=Eq(data_key='useIgnoresInput', equals=True),
        ),
    ]

    OUTPUTS = [
        Output(
            id='files',
            data_type='object[]',
            title='Files',
        ),
        Output(
            id='rootPath',
            data_type='string',
            title='Root Path',
        ),
    ]



@bindschema(schema=ReadAllFilesSchema)
class ReadAllFilesNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
