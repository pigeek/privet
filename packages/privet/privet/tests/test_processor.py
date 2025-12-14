
import unittest
import asyncio
from ..graph.processor import GraphProcessor
from ..graph.types import project_from_json, NodeId, DataValue

class TestGraphProcessor(unittest.TestCase):

    def test_smoke(self):
        self.assertTrue(True)

    def test_can_run_passthrough_graph(self):
        project_json = {
            "graphs": {
                "passthrough": {
                    "id": "passthrough",
                    "nodes": [
                        {
                            "id": "input",
                            "type": "graphInput",
                            "data": {
                                "id": "input",
                                "dataType": "string"
                            }
                        },
                        {
                            "id": "output",
                            "type": "graphOutput",
                            "data": {
                                "id": "output",
                                "dataType": "string"
                            }
                        }
                    ],
                    "connections": [
                        {
                            "outputNodeId": "input",
                            "outputId": "data",
                            "inputNodeId": "output",
                            "inputId": "value"
                        }
                    ]
                }
            },
            "metadata": {
                "mainGraphId": "passthrough"
            }
        }
        project = project_from_json(project_json)
        processor = GraphProcessor(project)

        async def run():
            return await processor.process_graph(inputs={"input": {"type": "string", "value": "input value"}})

        outputs = asyncio.run(run())
        self.assertEqual(outputs, {"output": {"type": "string", "value": "input value"}})

    def test_run_from_and_to_nodes(self):
        project_json = {
            "graphs": {
                "linear_graph": {
                    "id": "linear_graph",
                    "nodes": [
                        {"id": "node1", "type": "graphInput", "data": {"id": "input", "dataType": "string"}},
                        {"id": "node2", "type": "passthroughNode", "data": {}}, # Assuming a passthroughNode
                        {"id": "node3", "type": "graphOutput", "data": {"id": "output", "dataType": "string"}},
                    ],
                    "connections": [
                        {"outputNodeId": "node1", "outputId": "data", "inputNodeId": "node2", "inputId": "input"},
                        {"outputNodeId": "node2", "outputId": "output", "inputNodeId": "node3", "inputId": "value"},
                    ],
                }
            },
            "metadata": {"mainGraphId": "linear_graph"},
        }
        project = project_from_json(project_json)

        # Test case 1: Run from node2 to node3
        processor1 = GraphProcessor(project)
        async def run1():
            # For this test, passthroughNode needs to be properly implemented
            # Let's assume for now, it just passes the input to output
            # And graphInput is preloaded with value
            processor1.preload_node_data("node1", {"data": {"type": "string", "value": "preloaded value"}})
            return await processor1.process_graph(
                run_from_node_id="node2",
                run_to_node_ids=["node3"],
                inputs={"input": {"type": "string", "value": "should be ignored"}} # Should be ignored due to preload
            )
        outputs1 = asyncio.run(run1())
        # Expected output is from node3, which gets input from node2, which gets from preloaded node1
        self.assertEqual(outputs1, {"output": {"type": "string", "value": "preloaded value"}})

        # Test case 2: Run only to node2 (output should be empty or reflect only intermediate state)
        # This will be tricky without a proper way to get intermediate outputs,
        # but the 'done' event should show node2 as processed.
        processor2 = GraphProcessor(project)
        async def run2():
            processor2.preload_node_data("node1", {"data": {"type": "string", "value": "another value"}})
            events = []
            async def event_collector():
                async for event in processor2.events():
                    events.append(event)
            asyncio.create_task(event_collector())
            outputs = await processor2.process_graph(
                run_to_node_ids=["node2"]
            )
            return outputs, events
        
        outputs2, events2 = asyncio.run(run2())
        
        # graphOutput node (node3) should not have been run
        self.assertNotIn("output", outputs2)
        
        # Check that 'done' event indicates node2 was processed but node3 was not
        done_event = next((e_data for e_type, e_data in events2 if e_type == "done"), None)
        self.assertIsNotNone(done_event)
        self.assertIn("node2", done_event["runToNodeIds"])
        self.assertNotIn("node3", done_event["runToNodeIds"])

    def test_user_input_node(self):
        project_json = {
            "graphs": {
                "user_input_graph": {
                    "id": "user_input_graph",
                    "nodes": [
                        {"id": "start", "type": "graphInput", "data": {"id": "start", "dataType": "string"}},
                        {"id": "ask_user", "type": "userInput", "data": {}},
                        {"id": "end", "type": "graphOutput", "data": {"id": "final_output", "dataType": "string"}},
                    ],
                    "connections": [
                        {"outputNodeId": "start", "outputId": "data", "inputNodeId": "ask_user", "inputId": "irrelevant"}, # Input to user input node is often ignored
                        {"outputNodeId": "ask_user", "outputId": "response", "inputNodeId": "end", "inputId": "value"},
                    ],
                }
            },
            "metadata": {"mainGraphId": "user_input_graph"},
        }
        project = project_from_json(project_json)
        processor = GraphProcessor(project)

        async def run_and_provide_input():
            # Start the graph processing
            process_task = asyncio.create_task(
                processor.process_graph(inputs={"start": {"type": "string", "value": "hello"}})
            )

            # Wait for the userInput event to be emitted
            # We need to consume events until we see the userInput event
            user_input_node_id = None
            async for event_type, event_data in processor.events():
                if event_type == "userInput":
                    user_input_node_id = event_data["node"].id
                    break
            
            self.assertIsNotNone(user_input_node_id)
            self.assertEqual(user_input_node_id, "ask_user")

            # Provide the user input
            await processor.user_input(user_input_node_id, {"response": {"type": "string", "value": "user's response"}})

            # Wait for the graph to finish and return outputs
            outputs = await process_task
            return outputs

        outputs = asyncio.run(run_and_provide_input())
        self.assertEqual(outputs, {"final_output": {"type": "string", "value": "user's response"}})

    def test_abort_pause_resume_graph(self):
        project_json = {
            "graphs": {
                "long_running_graph": {
                    "id": "long_running_graph",
                    "nodes": [
                        {"id": "start", "type": "graphInput", "data": {"id": "start", "dataType": "string"}},
                        {"id": "delay1", "type": "delayNode", "data": {"duration": 0.05}},
                        {"id": "delay2", "type": "delayNode", "data": {"duration": 0.05}},
                        {"id": "end", "type": "graphOutput", "data": {"id": "final_output", "dataType": "string"}},
                    ],
                    "connections": [
                        {"outputNodeId": "start", "outputId": "data", "inputNodeId": "delay1", "inputId": "input"},
                        {"outputNodeId": "delay1", "outputId": "output", "inputNodeId": "delay2", "inputId": "input"},
                        {"outputNodeId": "delay2", "outputId": "output", "inputNodeId": "end", "inputId": "value"},
                    ],
                }
            },
            "metadata": {"mainGraphId": "long_running_graph"},
        }
        project = project_from_json(project_json)
        processor = GraphProcessor(project)

        async def run_and_control():
            process_task = asyncio.create_task(
                processor.process_graph(inputs={"start": {"type": "string", "value": "initial"}})
            )

            # Wait for the first delay node to start, then pause
            async for event_type, event_data in processor.events():
                if event_type == "nodeStart" and event_data["node"].id == "delay1":
                    break
            
            await processor.pause()
            
            # Ensure the graph is paused (we'll check for a pause event)
            events = []
            async for event_type, event_data in processor.events():
                events.append(event_type)
                if event_type == "pause":
                    break
            self.assertIn("pause", events)
            
            # Wait a bit, then resume
            await asyncio.sleep(0.1)
            await processor.resume()

            # Ensure the graph resumes (we'll check for a resume event)
            async for event_type, event_data in processor.events():
                events.append(event_type)
                if event_type == "resume":
                    break
            self.assertIn("resume", events)

            # Let the graph finish
            await process_task

            # Check that an abort event was NOT emitted and the graph finished
            all_events = []
            async for event_type, _ in processor.events():
                all_events.append(event_type)
                if event_type == "done":
                    break

            self.assertNotIn("abort", all_events)
            self.assertIn("done", all_events)
            self.assertFalse(processor._aborted)
            self.assertFalse(processor._paused)

        asyncio.run(run_and_control())

if __name__ == '__main__':
    unittest.main()
