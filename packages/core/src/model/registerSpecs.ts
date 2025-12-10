import type { NodeRegistration } from './NodeRegistration.js';
import { genericNodeDefinition, type GenericNodeSpec } from './nodes/GenericNode.js';

/**
 * Registers a list of GenericNodeSpec objects onto the provided registry by transforming
 * each spec into a node definition via genericNodeDefinition.
 */
export function registerSpecs(registry: NodeRegistration, specs: GenericNodeSpec<any>[]) {

  const existing = new Set<string>((registry.getNodeTypes() as unknown as string[]) ?? []);
  for (const spec of specs) {
    if (existing.has(spec.type)) {
      // Skip duplicates to avoid registry errors during transition
      continue;
    }
    const def = genericNodeDefinition(spec);
    registry.register(def);
    existing.add(spec.type);
  }
}
