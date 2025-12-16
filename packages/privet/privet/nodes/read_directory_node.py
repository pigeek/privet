from __future__ import annotations

from typing import Any, Dict
import os
import fnmatch
from pathlib import Path

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
        from ..utils.inputs import get_input_or_data

        # Get parameters
        path = get_input_or_data(self.node.data, inputs, 'path', 'string', 'usePathInput')
        if not path:
            path = '.'

        recursive = get_input_or_data(self.node.data, inputs, 'recursive', 'boolean', 'useRecursiveInput')
        if recursive is None:
            recursive = False

        include_directories = get_input_or_data(self.node.data, inputs, 'includeDirectories', 'boolean', 'useIncludeDirectoriesInput')
        if include_directories is None:
            include_directories = False

        filter_globs = get_input_or_data(self.node.data, inputs, 'filterGlobs', 'string[]', 'useFilterGlobsInput')
        if filter_globs is None:
            filter_globs = []

        relative = get_input_or_data(self.node.data, inputs, 'relative', 'boolean', 'useRelativeInput')
        if relative is None:
            relative = False

        ignores = get_input_or_data(self.node.data, inputs, 'ignores', 'string[]', 'useIgnoresInput')
        if ignores is None:
            ignores = []

        # Expand user home directory
        path = os.path.expanduser(path)

        files = []
        base_path = Path(path)

        if not base_path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")

        # Walk the directory
        if recursive:
            for root, dirs, filenames in os.walk(path):
                # Filter ignored directories
                dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignores)]

                # Add directories if requested
                if include_directories:
                    for dirname in dirs:
                        full_path = os.path.join(root, dirname)
                        files.append(full_path)

                # Add files
                for filename in filenames:
                    if not any(fnmatch.fnmatch(filename, pattern) for pattern in ignores):
                        full_path = os.path.join(root, filename)
                        files.append(full_path)
        else:
            # Non-recursive: only immediate children
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                is_dir = os.path.isdir(full_path)

                # Skip if ignored
                if any(fnmatch.fnmatch(entry, pattern) for pattern in ignores):
                    continue

                if is_dir:
                    if include_directories:
                        files.append(full_path)
                else:
                    files.append(full_path)

        # Apply filter globs
        if filter_globs:
            filtered_files = []
            for file_path in files:
                filename = os.path.basename(file_path)
                if any(fnmatch.fnmatch(filename, pattern) for pattern in filter_globs):
                    filtered_files.append(file_path)
            files = filtered_files

        # Make paths relative if requested
        if relative:
            files = [os.path.relpath(f, path) for f in files]

        # Create tree structure
        tree = self._create_tree_from_paths(files, path)

        return {
            'paths': {
                'type': 'string[]',
                'value': files,
            },
            'rootPath': {
                'type': 'string',
                'value': path,
            },
            'tree': {
                'type': 'object',
                'value': tree,
            }
        }

    def _create_tree_from_paths(self, paths: list[str], root_path: str) -> dict:
        """Create a tree structure from a list of file paths"""
        tree = {
            'path': root_path,
            'name': os.path.basename(root_path) or root_path,
            'isDirectory': True,
            'children': []
        }

        for path in paths:
            # For simplicity, just add paths as flat children
            # A more sophisticated implementation could create nested structure
            tree['children'].append({
                'path': path,
                'name': os.path.basename(path),
                'isDirectory': os.path.isdir(path) if os.path.exists(path) else False,
            })

        return tree
