import { NodeRegistration } from './NodeRegistration.js';

// During migration, all UI specs come from the backend.
// Keep only Graph I/O and SubGraph locally for editor/runtime compatibility.

// Re-export legacy classes for tooling that still imports them
export * from './nodes/GraphInputNode.js';
export * from './nodes/GraphOutputNode.js';
export * from './nodes/ChatNode.js';

import { graphInputNode } from './nodes/GraphInputNode.js';
import { graphOutputNode } from './nodes/GraphOutputNode.js';
import { subGraphNode } from './nodes/SubGraphNode.js';

export const registerBuiltInNodes = (registry: NodeRegistration) => {
  return registry
    .register(graphInputNode)
    .register(graphOutputNode)
    .register(subGraphNode);
};

let globalRivetNodeRegistry = registerBuiltInNodes(new NodeRegistration());
export { globalRivetNodeRegistry };

export type BuiltInNodes = typeof globalRivetNodeRegistry.NodesType;
export type BuiltInNodeType = typeof globalRivetNodeRegistry.NodeTypesType;
export type NodeOfType<T extends BuiltInNodeType> = Extract<BuiltInNodes, { type: T }>;

export function resetGlobalRivetNodeRegistry() {
  globalRivetNodeRegistry = registerBuiltInNodes(new NodeRegistration());
}

