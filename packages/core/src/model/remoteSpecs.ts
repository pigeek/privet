import type { GenericNodeSpec } from './nodes/GenericNode.js';

// Lightweight in-memory registry for remote specs, keyed by type.
// Intended for UI-only lookups (e.g., NodeBody fallback) when impls are not yet available.
const registry = new Map<string, GenericNodeSpec<any>>();

export function upsertRemoteSpecs(specs: GenericNodeSpec<any>[]) {
  for (const spec of specs) {
    registry.set(spec.type, spec);
  }
}

export function getRemoteSpec(type: string): GenericNodeSpec<any> | undefined {
  return registry.get(type);
}

export function getAllRemoteSpecs(): GenericNodeSpec<any>[] {
  return Array.from(registry.values());
}
