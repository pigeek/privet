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

class CallGraphSchema(NodeSchema):
    NODE_TYPE = 'callGraph'
    TITLE = 'Call Graph'
    DISPLAY_NAME = 'Call Graph'
    VISUAL_WIDTH = 200
    UI_GROUP = ['Advanced']
    UI_INFOBOX_TITLE = 'Call Graph Node'
    UI_INFOBOX_BODY = 'Calls another graph and passes inputs to it. Use in combination with the Graph Reference node to call dynamic graphs.'
    UI_CONTEXT_MENU_TITLE = 'Call Graph'
    DATA = {'useErrorOutput': False}
    EDITORS = []

    INPUTS = [
        Input(
            id='graph',
            data_type='graph-reference',
            title='Graph',
            required=True,
        ),
        Input(
            id='inputs',
            data_type='object',
            title='Inputs',
        ),
    ]

    OUTPUTS = [
        Output(
            id='outputs',
            data_type='object',
            title='Outputs',
        ),
        Output(
            id='error',
            data_type='string',
            title='Error',
            show_if=Eq(data_key='useErrorOutput', equals=True),
        ),
    ]



@bindschema(schema=CallGraphSchema)
class CallGraphNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        import time
        from ..utils.data_values import coerce_type_optional

        # Get the graph reference from inputs
        graph_ref = coerce_type_optional(inputs.get('graph'), 'graph-reference')
        graph_inputs = coerce_type_optional(inputs.get('inputs'), 'object') or {}

        # If no graph reference, return control-flow-excluded
        if not graph_ref:
            return {
                'outputs': {
                    'type': 'control-flow-excluded',
                    'value': None,
                }
            }

        # Get the graph from the project
        graph_id = graph_ref.get('graphId') if isinstance(graph_ref, dict) else None
        if not graph_id:
            return {
                'outputs': {
                    'type': 'control-flow-excluded',
                    'value': None,
                }
            }

        project = self.context.get('project')
        if not project or graph_id not in project.graphs:
            return {
                'outputs': {
                    'type': 'control-flow-excluded',
                    'value': None,
                }
            }

        # Create a subprocessor for the called graph
        create_subprocessor = self.context.get('create_subprocessor')
        if not create_subprocessor:
            raise RuntimeError("create_subprocessor not available in context")

        subprocessor = create_subprocessor(graph_id)

        # Register the subprocessor as a child
        parent_processor = self.context.get('processor')
        if parent_processor:
            parent_processor.register_child(subprocessor)

        try:
            start_time = time.time()

            # Convert graph_inputs to DataValue format
            input_data_values = {}
            for key, value in graph_inputs.items():
                if isinstance(value, dict) and 'type' in value and 'value' in value:
                    input_data_values[key] = value
                else:
                    # Infer type if not already a DataValue
                    input_data_values[key] = {'type': 'any', 'value': value}

            # Process the subgraph
            graph_outputs = await subprocessor.process_graph(
                inputs=input_data_values,
                context_values=self.context.get('context_values', {})
            )

            duration = (time.time() - start_time) * 1000  # Convert to milliseconds

            outputs = {
                'outputs': {
                    'type': 'object',
                    'value': graph_outputs,
                },
                'duration': {
                    'type': 'number',
                    'value': duration,
                }
            }

            if self.node.data.get('useErrorOutput'):
                outputs['error'] = {
                    'type': 'control-flow-excluded',
                    'value': None,
                }

            return outputs

        except Exception as err:
            # If useErrorOutput is enabled, return error in output
            if self.node.data.get('useErrorOutput'):
                return {
                    'outputs': {
                        'type': 'control-flow-excluded',
                        'value': None,
                    },
                    'error': {
                        'type': 'string',
                        'value': str(err),
                    }
                }
            else:
                # Re-raise the error
                raise
