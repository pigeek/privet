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

class ToMarkdownTableSchema(NodeSchema):
    NODE_TYPE = 'toMarkdownTable'
    TITLE = 'To Markdown Table'
    DISPLAY_NAME = 'To Markdown Table'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Text']
    UI_INFOBOX_TITLE = 'To Markdown Table Node'
    UI_INFOBOX_BODY = 'Converts an array of objects into a markdown table.'
    UI_CONTEXT_MENU_TITLE = 'To Markdown Table'
    DATA = {'includeHeaders': True, 'alignPipes': False}
    EDITORS = [{'type': 'toggle', 'label': 'Include Headers', 'dataKey': 'includeHeaders'}, {'type': 'toggle', 'label': 'Align Pipes', 'dataKey': 'alignPipes'}]
    BODY = '{{#if includeHeaders}}With Header Row{{/if}}{{#if alignPipes}}{{#if includeHeaders}}, {{/if}}Pipes Aligned{{/if}}'

    INPUTS = [
        Input(
            id='data',
            data_type='any',
            title='Data Array',
            required=True,
        ),
    ]

    OUTPUTS = [
        Output(
            id='markdown',
            data_type='string',
            title='Markdown Table',
        ),
    ]



@bindschema(schema=ToMarkdownTableSchema)
class ToMarkdownTableNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        from ..utils.data_values import coerce_type

        data_array = coerce_type(inputs.get('data'), 'object[]')
        include_headers = self.data.get('includeHeaders', True)
        align_pipes = self.data.get('alignPipes', False)

        if not data_array:
            return {'markdown': {'type': 'string', 'value': ''}}

        # Extract keys from first object
        keys = list(data_array[0].keys()) if data_array else []

        # Build markdown table
        lines = []

        # Add header row if requested
        if include_headers:
            if align_pipes:
                # Calculate column widths for alignment
                col_widths = {key: len(key) for key in keys}
                for row in data_array:
                    for key in keys:
                        value_str = str(row.get(key, ''))
                        col_widths[key] = max(col_widths[key], len(value_str))

                # Header with aligned pipes
                header_cells = [key.ljust(col_widths[key]) for key in keys]
                lines.append('| ' + ' | '.join(header_cells) + ' |')

                # Separator row
                separator_cells = ['-' * col_widths[key] for key in keys]
                lines.append('| ' + ' | '.join(separator_cells) + ' |')

                # Data rows with aligned pipes
                for row in data_array:
                    cells = [str(row.get(key, '')).ljust(col_widths[key]) for key in keys]
                    lines.append('| ' + ' | '.join(cells) + ' |')
            else:
                # Header without alignment
                lines.append('| ' + ' | '.join(keys) + ' |')

                # Separator row
                lines.append('| ' + ' | '.join(['-' * len(key) for key in keys]) + ' |')

                # Data rows
                for row in data_array:
                    cells = [str(row.get(key, '')) for key in keys]
                    lines.append('| ' + ' | '.join(cells) + ' |')
        else:
            # No header, just data rows
            if align_pipes:
                # Calculate column widths
                col_widths = {key: 0 for key in keys}
                for row in data_array:
                    for key in keys:
                        value_str = str(row.get(key, ''))
                        col_widths[key] = max(col_widths[key], len(value_str))

                for row in data_array:
                    cells = [str(row.get(key, '')).ljust(col_widths[key]) for key in keys]
                    lines.append('| ' + ' | '.join(cells) + ' |')
            else:
                for row in data_array:
                    cells = [str(row.get(key, '')) for key in keys]
                    lines.append('| ' + ' | '.join(cells) + ' |')

        markdown_table = '\n'.join(lines)

        return {
            'markdown': {
                'type': 'string',
                'value': markdown_table,
            }
        }
