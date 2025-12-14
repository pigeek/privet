from __future__ import annotations

import asyncio
from typing import Any, Dict

from ..BaseNode import BaseNode, bindschema
from ..spec_builder import Input, Output, NodeSchema, Toggle, Code, Eq
from ..graph.types import DataValue, NodeId


class UserInputSchema(NodeSchema):
    NODE_TYPE = "userInput"
    TITLE = "User Input"
    DISPLAY_NAME = "User Input"
    PRODUCES = ["string"]
    DESCRIPTION = "Waits for input from the user (e.g., from the UI)."

    DATA = {"prompt": "This is an example question?", "useInput": False, "renderingFormat": "markdown"}

    EDITORS = [
        Code(label="Prompt", language="plain-text", show_if=None).to_spec("prompt") | {"useInputToggleDataKey": "useInput"},
        {
            "type": "group",
            "label": "Rendering",
            "editors": [
                {
                    "type": "dropdown",
                    "dataKey": "renderingFormat",
                    "label": "Format",
                    "options": [
                        {"label": "Preformatted", "value": "preformatted"},
                        {"label": "Markdown", "value": "markdown"},
                    ],
                    "defaultValue": "markdown",
                }
            ],
        },
    ]

    INPUTS = [
        Input(
            id="questions",
            data_type="string[]",
            title="Questions",
            show_if=Eq(data_key="useInput", equals=True),
        )
    ]

    OUTPUTS = [
        Output(
            id="output",
            data_type="string[]",
            title="Answers Only",
        ),
        Output(
            id="questionsAndAnswers",
            data_type="string[]",
            title="Q & A",
        )
    ]


@bindschema(schema=UserInputSchema)
class UserInputNode(BaseNode):
    async def process(self, inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        inputs = inputs or {}
        node_id: NodeId = self.node.id

        data = self.node.data or {}
        process_id = "sim"

        # Determine questions list
        if data.get("useInput"):
            questions_val = inputs.get("questions", {})
            raw = questions_val.get("value") if isinstance(questions_val, dict) else questions_val
            if isinstance(raw, list):
                questions = raw
            elif isinstance(raw, str):
                questions = [raw]
            else:
                questions = []
        else:
            questions = [data.get("prompt") or ""]

        # Ensure strings
        questions = [str(q) for q in questions]

        rendering_format = "text" if data.get("renderingFormat") == "preformatted" else "markdown"

        # Emit a userInput event to signal that this node is waiting for input
        print(f"[UserInputNode] Emitting userInput for node={node_id} questions={questions} rendering={rendering_format}")
        await self.context["emit"](
            "userInput",
            {
                "node": self.node,
                "inputs": inputs,
                "processId": process_id,
                "inputStrings": questions,
                "renderingFormat": rendering_format,
                "nodeId": node_id,
            },
        )

        # Wait for user input from the GraphProcessor. This mirrors the TS implementation by
        # registering a pending future per node id, then resolving it when the processor receives
        # a matching user-input event.
        processor = self.context["processor"]
        future: asyncio.Future = asyncio.get_event_loop().create_future()
        processor._pending_user_inputs[node_id] = future
        try:
            await self.context["emit"]("trace", {"message": f"[UserInputNode] Waiting for input node={node_id} graph={getattr(self.context.get('project'), 'metadata', {}).get('id', None)}"})
        except Exception:
            pass

        try:
            # Consume any queued answers that arrived before we registered the pending future.
            leftovers: list[tuple[NodeId, Dict[str, Any]]] = []
            match: Dict[str, Any] | None = None
            while not processor._user_input_queue.empty():
                input_node_id, answers = processor._user_input_queue.get_nowait()
                print(f"[UserInputNode] Pre-queued user input for node={input_node_id} ours={node_id} answers={answers}")
                if input_node_id == node_id and match is None:
                    match = answers
                else:
                    leftovers.append((input_node_id, answers))
            for item in leftovers:
                processor._user_input_queue.put_nowait(item)
            if match is not None and not future.done():
                future.set_result(match)

            answers = await future
        finally:
            processor._pending_user_inputs.pop(node_id, None)
            if processor._user_input_queue.empty():
                processor._user_input_event.clear()
            try:
                await self.context["emit"]("trace", {"message": f"[UserInputNode] Finished waiting node={node_id}"})
            except Exception:
                pass

        answer_val = answers.get("value") if isinstance(answers, dict) else None
        if not isinstance(answer_val, list):
            answer_val = []
        q_and_a = [f"{q}\n{a}" for q, a in zip(questions, answer_val)]
        return {
            "output": {"type": "string[]", "value": answer_val},
            "questionsAndAnswers": {"type": "string[]", "value": q_and_a},
        }
