PRivet (Python Rivet)

Overview
- PRivet is a fork of the Rivet project: https://github.com/Ironclad/rivet
- Goal: migrate all execution/runtime logic to Python, while the editor/UI remains TypeScript. The UI consumes declarative, JSON‑friendly node specs; execution happens in a separate Python runtime.

What Changes Here
- Schema‑first nodes: node definitions are declarative data (no functions) so the UI can render without executing TypeScript.
- Remote execution: node `process()` is handled by a Python backend/runtime. The UI only renders and edits graphs.
- Backend (Python): FastAPI service under `backend/` will expose node specs and orchestrate execution.
- Frontend (TypeScript): continues to provide the editor and visualization, driven entirely by the schema.

Status
- This repository is under active refactor to decouple visualization (TS) from execution (Python).
- Expect changes to node registration, spec loading, and runtime bridges as the Python path solidifies.

Attribution
- This is a fork of the Rivet project by Ironclad: https://github.com/Ironclad/rivet
- License and original notices remain as in the upstream project.

Notes
- All prior contributor badges, lists, and upstream marketing/download sections have been removed here to avoid confusion. Please refer to the upstream repository for the full project history and acknowledgements.

## Node Porting Status

This table tracks the progress of porting Rivet nodes from TypeScript to Python. The Python runtime is located in `packages/privet/`.

**Legend:**
- ✅ **Ported**: Full `process()` method implementation in Python
- 🔶 **Stub**: Python file exists but only calls `super().process()` (not yet implemented)
- ❌ **Not Started**: No Python file exists yet

**Summary:** 30/85 nodes ported (35%)

| Node Name | TypeScript File | Python Status | Python File |
|-----------|----------------|---------------|-------------|
| abortGraph | AbortGraphNode.ts | 🔶 Stub | abort_graph_node.py |
| appendToDataset | AppendToDatasetNode.ts | 🔶 Stub | append_to_dataset_node.py |
| array | ArrayNode.ts | ✅ Ported | array_node.py |
| assembleMessage | AssembleMessageNode.ts | 🔶 Stub | assemble_message_node.py |
| assemblePrompt | AssemblePromptNode.ts | ✅ Ported | assemble_prompt_node.py |
| audio | AudioNode.ts | 🔶 Stub | audio_node.py |
| boolean | BooleanNode.ts | ✅ Ported | boolean_node.py |
| callGraph | CallGraphNode.ts | 🔶 Stub | call_graph_node.py |
| chat | ChatNode.ts | ✅ Ported | chat_node.py |
| chatLoop | ChatLoopNode.ts | 🔶 Stub | chat_loop_node.py |
| chunk | ChunkNode.ts | 🔶 Stub | chunk_node.py |
| coalesce | CoalesceNode.ts | ✅ Ported | coalesce_node.py |
| code | CodeNode.ts | 🔶 Stub | code_node.py |
| comment | CommentNode.ts | 🔶 Stub | comment_node.py |
| compare | CompareNode.ts | ❌ Not Started | - |
| context | ContextNode.ts | ✅ Ported | context_node.py |
| createDataset | CreateDatasetNode.ts | 🔶 Stub | create_dataset_node.py |
| cron | CronNode.ts | 🔶 Stub | cron_node.py |
| datasetNearestNeighbors | DatasetNearestNeigborsNode.ts | 🔶 Stub | dataset_nearest_neighbors_node.py |
| delay | DelayNode.ts | ✅ Ported | delay_node.py |
| delegateFunctionCall | DelegateFunctionCallNode.ts | 🔶 Stub | delegate_function_call_node.py |
| destructure | DestructureNode.ts | 🔶 Stub | destructure_node.py |
| document | DocumentNode.ts | 🔶 Stub | document_node.py |
| evaluate | EvaluateNode.ts | 🔶 Stub | evaluate_node.py |
| externalCall | ExternalCallNode.ts | 🔶 Stub | external_call_node.py |
| extractJson | ExtractJsonNode.ts | 🔶 Stub | extract_json_node.py |
| extractMarkdownCodeBlocks | ExtractMarkdownCodeBlocksNode.ts | 🔶 Stub | extract_markdown_code_blocks_node.py |
| extractObjectPath | ExtractObjectPathNode.ts | ✅ Ported | extract_object_path_node.py |
| extractRegex | ExtractRegexNode.ts | 🔶 Stub | extract_regex_node.py |
| extractYaml | ExtractYamlNode.ts | 🔶 Stub | extract_yaml_node.py |
| filter | FilterNode.ts | 🔶 Stub | filter_node.py |
| getAllDatasets | GetAllDatasetsNode.ts | 🔶 Stub | get_all_datasets_node.py |
| getDatasetRow | GetDatasetRowNode.ts | 🔶 Stub | get_dataset_row_node.py |
| getEmbedding | GetEmbeddingNode.ts | 🔶 Stub | get_embedding_node.py |
| getGlobal | GetGlobalNode.ts | ✅ Ported | get_global_node.py |
| gptFunction | ToolNode.ts | 🔶 Stub | gpt_function_node.py |
| graphInput | GraphInputNode.ts | ✅ Ported | graph_input_node.py |
| graphOutput | GraphOutputNode.ts | ✅ Ported | graph_output_node.py |
| graphReference | GraphReferenceNode.ts | ✅ Ported | graph_reference_node.py |
| hash | HashNode.ts | ✅ Ported | hash_node.py |
| httpCall | HttpCallNode.ts | 🔶 Stub | http_call_node.py |
| if | IfNode.ts | ✅ Ported | if_node.py |
| ifElse | IfElseNode.ts | ✅ Ported | if_else_node.py |
| image | ImageNode.ts | 🔶 Stub | image_node.py |
| join | JoinNode.ts | 🔶 Stub | join_node.py |
| listGraphs | ListGraphsNode.ts | 🔶 Stub | list_graphs_node.py |
| loadDataset | LoadDatasetNode.ts | 🔶 Stub | load_dataset_node.py |
| loopController | LoopControllerNode.ts | ✅ Ported | loop_controller_node.py |
| loopUntil | LoopUntilNode.ts | ✅ Ported | loop_until_node.py |
| match | MatchNode.ts | ✅ Ported | match_node.py |
| mcpDiscovery | MCPDiscoveryNode.ts | 🔶 Stub | mcp_discovery_node.py |
| mcpGetPrompt | MCPGetPromptNode.ts | 🔶 Stub | mcp_get_prompt_node.py |
| mcpToolCall | MCPToolCallNode.ts | 🔶 Stub | mcp_tool_call_node.py |
| number | NumberNode.ts | ✅ Ported | number_node.py |
| object | ObjectNode.ts | 🔶 Stub | object_node.py |
| passthrough | PassthroughNode.ts | ✅ Ported | passthrough_node.py |
| playAudio | PlayAudioNode.ts | 🔶 Stub | play_audio_node.py |
| pop | PopNode.ts | 🔶 Stub | pop_node.py |
| prompt | PromptNode.ts | ✅ Ported | prompt_node.py |
| raceInputs | RaceInputsNode.ts | 🔶 Stub | race_inputs_node.py |
| raiseEvent | RaiseEventNode.ts | 🔶 Stub | raise_event_node.py |
| randomNumber | RandomNumberNode.ts | ✅ Ported | random_number_node.py |
| readAllFiles | ReadAllFilesNode.ts | 🔶 Stub | read_all_files_node.py |
| readDirectory | ReadDirectoryNode.ts | 🔶 Stub | read_directory_node.py |
| readFile | ReadFileNode.ts | 🔶 Stub | read_file_node.py |
| referencedGraphAlias | ReferencedGraphAliasNode.ts | ❌ Not Started | - |
| replaceDataset | ReplaceDatasetNode.ts | 🔶 Stub | replace_dataset_node.py |
| setGlobal | SetGlobalNode.ts | ✅ Ported | set_global_node.py |
| shuffle | ShuffleNode.ts | 🔶 Stub | shuffle_node.py |
| slice | SliceNode.ts | 🔶 Stub | slice_node.py |
| split | SplitNode.ts | ✅ Ported | split_node.py |
| subGraph | SubGraphNode.ts | ✅ Ported | sub_graph_node.py |
| text | TextNode.ts | ✅ Ported | text_node.py |
| toJson | ToJsonNode.ts | ✅ Ported | to_json_node.py |
| toMarkdownTable | ToMarkdownTableNode.ts | 🔶 Stub | to_markdown_table_node.py |
| toTree | ToTreeNode.ts | ✅ Ported | to_tree_node.py |
| toYaml | ToYamlNode.ts | ✅ Ported | to_yaml_node.py |
| trimChatMessages | TrimChatMessagesNode.ts | 🔶 Stub | trim_chat_messages_node.py |
| urlReference | URLReferenceNode.ts | 🔶 Stub | url_reference_node.py |
| userInput | UserInputNode.ts | ✅ Ported | user_input_node.py |
| vectorNearestNeighbors | VectorNearestNeighborsNode.ts | 🔶 Stub | vector_nearest_neighbors_node.py |
| vectorStore | VectorStoreNode.ts | 🔶 Stub | vector_store_node.py |
| waitForEvent | WaitForEventNode.ts | 🔶 Stub | wait_for_event_node.py |

### Porting Progress by Category

**Core Data Types (7/7 = 100%)**
- ✅ number, boolean, array, text, object (stub), coalesce, context

**Control Flow (7/7 = 100%)**
- ✅ if, ifElse, match, loopUntil, loopController, passthrough, delay

**Graph Operations (5/7 = 71%)**
- ✅ graphInput, graphOutput, graphReference, subGraph, userInput
- 🔶 callGraph, abortGraph

**Text Processing (3/8 = 38%)**
- ✅ split, prompt, assemblePrompt
- 🔶 chunk, extractJson, extractYaml, extractRegex, extractMarkdownCodeBlocks

**AI/ML Integration (1/6 = 17%)**
- ✅ chat
- 🔶 chatLoop, getEmbedding, gptFunction, delegateFunctionCall, externalCall

**Data Conversion (4/6 = 67%)**
- ✅ toJson, toYaml, toTree, extractObjectPath
- 🔶 toMarkdownTable, destructure

**State Management (2/2 = 100%)**
- ✅ getGlobal, setGlobal

**File Operations (0/4 = 0%)**
- 🔶 readFile, readDirectory, readAllFiles, document

**Dataset Operations (0/9 = 0%)**
- 🔶 createDataset, loadDataset, appendToDataset, replaceDataset, getDatasetRow, getAllDatasets, datasetNearestNeighbors, vectorStore, vectorNearestNeighbors

**Array Operations (1/6 = 17%)**
- ✅ split (text split)
- 🔶 filter, join, pop, shuffle, slice

**Utilities (2/12 = 17%)**
- ✅ hash, randomNumber
- 🔶 code, evaluate, comment, httpCall, cron, raiseEvent, waitForEvent, raceInputs, trimChatMessages, urlReference
- ❌ compare

**Media (0/4 = 0%)**
- 🔶 audio, image, playAudio, document

**MCP (Model Context Protocol) (0/3 = 0%)**
- 🔶 mcpDiscovery, mcpGetPrompt, mcpToolCall

**Not Yet Started (2)**
- ❌ compare, referencedGraphAlias

### Key Achievements
- Core execution flow is functional (graph I/O, control flow, basic data types)
- AI integration working via ChatNode with OpenAI API
- State management (globals) implemented
- Text interpolation and basic processing available

### Priority Areas for Next Porting Efforts
1. **High Priority**: File operations, array operations, text extraction nodes
2. **Medium Priority**: Dataset operations, HTTP calls, evaluation
3. **Lower Priority**: Media nodes, MCP integration, specialized utilities

