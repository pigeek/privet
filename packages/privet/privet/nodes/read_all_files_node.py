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
        import os
        import fnmatch
        import base64
        from pathlib import Path
        from ..utils.inputs import get_input_or_data

        # Get parameters
        path = get_input_or_data(self.node.data, inputs, 'path', 'string', 'usePathInput')
        if not path:
            path = '.'

        recursive = get_input_or_data(self.node.data, inputs, 'recursive', 'boolean', 'useRecursiveInput')
        if recursive is None:
            recursive = False

        filter_globs = get_input_or_data(self.node.data, inputs, 'filterGlobs', 'string[]', 'useFilterGlobsInput')
        if filter_globs is None:
            filter_globs = []

        ignores = get_input_or_data(self.node.data, inputs, 'ignores', 'string[]', 'useIgnoresInput')
        if ignores is None:
            ignores = []

        as_binary = self.node.data.get('asBinary', False)
        error_on_missing = self.node.data.get('errorOnMissingFile', False)

        # Expand user home directory
        path = os.path.expanduser(path)

        try:
            # Get list of files
            file_paths = []
            base_path = Path(path)

            if not base_path.exists():
                raise FileNotFoundError(f"Path does not exist: {path}")

            # Walk the directory
            if recursive:
                for root, dirs, filenames in os.walk(path):
                    # Filter ignored directories
                    dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignores)]

                    # Add files
                    for filename in filenames:
                        if not any(fnmatch.fnmatch(filename, pattern) for pattern in ignores):
                            full_path = os.path.join(root, filename)
                            rel_path = os.path.relpath(full_path, path)
                            file_paths.append(rel_path)
            else:
                # Non-recursive: only immediate children
                for entry in os.listdir(path):
                    full_path = os.path.join(path, entry)
                    if os.path.isfile(full_path):
                        if not any(fnmatch.fnmatch(entry, pattern) for pattern in ignores):
                            file_paths.append(entry)

            # Apply filter globs
            if filter_globs:
                filtered_files = []
                for file_path in file_paths:
                    filename = os.path.basename(file_path)
                    if any(fnmatch.fnmatch(filename, pattern) for pattern in filter_globs):
                        filtered_files.append(file_path)
                file_paths = filtered_files

            # Read all files
            files = []
            for file_path in file_paths:
                full_path = os.path.join(path, file_path)
                try:
                    if as_binary:
                        # Read as binary and encode to base64
                        with open(full_path, 'rb') as f:
                            content_bytes = f.read()
                            content = base64.b64encode(content_bytes).decode('utf-8')
                    else:
                        # Read as text
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                    files.append({
                        'path': file_path,
                        'content': content,
                    })
                except Exception as err:
                    if error_on_missing:
                        raise
                    # Add empty content on error
                    files.append({
                        'path': file_path,
                        'content': '' if not as_binary else '',
                    })

            return {
                'files': {
                    'type': 'object[]',
                    'value': files,
                },
                'rootPath': {
                    'type': 'string',
                    'value': path,
                }
            }

        except Exception as err:
            if error_on_missing:
                raise
            return {
                'files': {
                    'type': 'object[]',
                    'value': [],
                },
                'rootPath': {
                    'type': 'string',
                    'value': path,
                }
            }
