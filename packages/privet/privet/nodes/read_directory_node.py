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

class ReadDirectorySchema(NodeSchema):
    NODE_TYPE = 'readDirectory'
    TITLE = 'Read Directory'
    DISPLAY_NAME = 'Read Directory'
    VISUAL_WIDTH = 250
    UI_GROUP = ['Input/Output']
    UI_INFOBOX_TITLE = 'Read Directory Node'
    UI_INFOBOX_BODY = 'Reads a directory and outputs Paths, Root Path, and a Tree.'
    UI_CONTEXT_MENU_TITLE = 'Read Directory'
    DATA = {'path': 'examples', 'usePathInput': False, 'recursive': False, 'useRecursiveInput': False, 'includeDirectories': False, 'useIncludeDirectoriesInput': False, 'filterGlobs': [], 'useFilterGlobsInput': False, 'relative': False, 'useRelativeInput': False, 'ignores': [], 'useIgnoresInput': False}
    EDITORS = []
    BODY = 'Path: {{#if usePathInput}}(Input){{#else}}{{path}}{{/if}}\nRecursive: {{#if useRecursiveInput}}(Input){{#else}}{{recursive}}{{/if}}\nInclude Directories: {{#if useIncludeDirectoriesInput}}(Input){{#else}}{{includeDirectories}}{{/if}}\nRelative: {{#if useRelativeInput}}(Input){{#else}}{{relative}}{{/if}}\nFilters: {{#if useFilterGlobsInput}}(Input){{#else}}{{#if filterGlobs}}{{filterGlobs}}{{#else}}None{{/if}}{{/if}}'

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
            id='includeDirectories',
            data_type='boolean',
            title='Include Directories',
            show_if=Eq(data_key='useIncludeDirectoriesInput', equals=True),
        ),
        Input(
            id='filterGlobs',
            data_type='string[]',
            title='Filter Globs',
            show_if=Eq(data_key='useFilterGlobsInput', equals=True),
        ),
        Input(
            id='relative',
            data_type='boolean',
            title='Relative',
            show_if=Eq(data_key='useRelativeInput', equals=True),
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
            id='rootPath',
            data_type='string',
            title='Root Path',
        ),
        Output(
            id='paths',
            data_type='string[]',
            title='Paths',
        ),
        Output(
            id='tree',
            data_type='object',
            title='Tree',
        ),
    ]



@bindschema(schema=ReadDirectorySchema)
class ReadDirectoryNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return await super().process(inputs)
