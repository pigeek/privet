import unittest
import asyncio
from ..graph.processor import GraphProcessor
from ..graph.types import project_from_json

class TestComplexGraph(unittest.TestCase):

    def test_two_node_graph(self):
        project_json = {
            "graphs": {
                "two-node-graph": {
                    "id": "two-node-graph",
                    "nodes": [
                        {
                            "id": "input",
                            "type": "graphInput",
                            "data": {
                                "id": "input",
                                "type": "string"
                            }
                        },
                        {
                            "id": "output",
                            "type": "graphOutput",
                            "data": {
                                "id": "output",
                                "type": "string"
                            }
                        },
                        {
                            "id": "intermediate",
                            "type": "stringNode", # Assuming a stringNode exists or will be created
                            "data": {
                                "value": "hello"
                            }
                        }
                    ],
                    "connections": [
                        {
                            "outputNodeId": "input",
                            "outputId": "input",
                            "inputNodeId": "intermediate",
                            "inputId": "value"
                        },
                        {
                            "outputNodeId": "intermediate",
                            "outputId": "output",
                            "inputNodeId": "output",
                            "inputId": "output"
                        }
                    ]
                }
            },
            "metadata": {
                "mainGraphId": "two-node-graph"
            }
        }
        project = project_from_json(project_json)
        processor = GraphProcessor(project)

        async def run():
            return await processor.process_graph(inputs={"input": {"type": "string", "value": "initial input"}})

        outputs = asyncio.run(run())
        # The expected output would depend on the actual logic of 'stringNode'
        # For now, let's assume it passes through the "hello" from the intermediate node
        self.assertEqual(outputs, {"output": {"type": "string", "value": "hello"}})

if __name__ == '__main__':
    unittest.main()
