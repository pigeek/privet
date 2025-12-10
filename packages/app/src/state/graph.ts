import { atom } from 'jotai';
import { atomWithStorage, atomFamily } from 'jotai/utils';
import {
  type ChartNode,
  type NodeConnection,
  type NodeGraph,
  type NodeId,
  type NodeImpl,
  type NodeInputDefinition,
  type NodeOutputDefinition,
  type PortId,
  emptyNodeGraph,
  getError,
  globalRivetNodeRegistry,
} from '@ironclad/rivet-core';
import { mapValues } from 'lodash-es';
import { projectState, referencedProjectsState } from './savedGraphs';
import { pluginRefreshCounterState } from './plugins';
import { type CalculatedRevision } from '../utils/ProjectRevisionCalculator';
import { createHybridStorage } from './storage.js';

const { storage } = createHybridStorage('graph');

// Basic atoms
export const historicalGraphState = atom<CalculatedRevision | null>(null);
export const isReadOnlyGraphState = atom<boolean>(false);
export const historicalChangedNodesState = atom<Set<NodeId>>(new Set<NodeId>());

export const graphState = atomWithStorage<NodeGraph>('graphState', emptyNodeGraph(), storage);

// Derived atoms
export const graphMetadataState = atom(
  (get) => get(graphState).metadata,
  (get, set, newValue: NodeGraph['metadata']) => {
    const currentGraph = get(graphState);
    set(graphState, { ...currentGraph, metadata: newValue });
  },
);

export const nodesState = atom(
  (get) => get(graphState).nodes,
  (get, set, newValue: ChartNode[] | ((prev: ChartNode[]) => ChartNode[])) => {
    const currentGraph = get(graphState);
    const currentNodes = currentGraph.nodes;

    const nextNodes = typeof newValue === 'function' ? newValue(currentNodes) : newValue;

    set(graphState, { ...currentGraph, nodes: nextNodes });
  },
);

export const connectionsState = atom(
  (get) => get(graphState).connections,
  (get, set, newValue: NodeConnection[] | ((prev: NodeConnection[]) => NodeConnection[])) => {
    const currentGraph = get(graphState);
    const currentConnections = currentGraph.connections;

    const nextConnections = typeof newValue === 'function' ? newValue(currentConnections) : newValue;

    set(graphState, { ...currentGraph, connections: nextConnections });
  },
);

export const nodesByIdState = atom((get) =>
  get(nodesState).reduce(
    (acc, node) => {
      acc[node.id] = node;
      return acc;
    },
    {} as Record<NodeId, ChartNode>,
  ),
);

export const nodesForConnectionState = atom((get) => {
  const nodesById = get(nodesByIdState);
  return get(connectionsState).map((connection) => ({
    inputNode: nodesById[connection.inputNodeId],
    outputNode: nodesById[connection.outputNodeId],
  }));
});

export const connectionsForNodeState = atom((get) =>
  get(connectionsState).reduce(
    (acc, connection) => {
      acc[connection.inputNodeId] ??= [];
      acc[connection.inputNodeId]!.push(connection);

      acc[connection.outputNodeId] ??= [];
      acc[connection.outputNodeId]!.push(connection);
      return acc;
    },
    {} as Record<NodeId, NodeConnection[]>,
  ),
);

export const connectionsForSingleNodeState = atomFamily((nodeId: NodeId) =>
  atom((get) => get(connectionsForNodeState)[nodeId]),
);

export const nodeByIdState = atomFamily((nodeId: NodeId) => atom((get) => get(nodesByIdState)[nodeId]));

export const nodeInstancesState = atom((get) => {
  const nodesById = get(nodesByIdState);
  get(pluginRefreshCounterState); // Keep dependency

  return mapValues(nodesById, (node) => {
    try {
      return globalRivetNodeRegistry.createDynamicImpl(node);
    } catch (err) {
      return undefined;
    }
  });
});

export const nodeInstanceByIdState = atomFamily((nodeId: NodeId) => atom((get) => get(nodeInstancesState)?.[nodeId]));

export const ioDefinitionsState = atom((get) => {
  const nodeInstances = get(nodeInstancesState);
  const connectionsForNode = get(connectionsForNodeState);
  const nodesById = get(nodesByIdState);
  const project = get(projectState);
  const referencedProjects = get(referencedProjectsState);

  return mapValues(nodesById, (node) => {
    const connections = connectionsForNode[node.id] ?? [];

    let inputDefinitions: NodeInputDefinition[] | undefined;
    let outputDefinitions: NodeOutputDefinition[] | undefined;

    try {
      inputDefinitions = nodeInstances[node.id]?.getInputDefinitionsIncludingBuiltIn(
        connections,
        nodesById,
        project,
        referencedProjects,
      );

      // Apply declarative filters and expand variadic inputs
      if (inputDefinitions) {
        const expanded: NodeInputDefinition[] = [];
        for (const def of inputDefinitions) {
          // Apply showIf condition, if present
          const show = (() => {
            if (!('showIf' in def) || !def.showIf) return true;
            const cond = def.showIf as any;
            const data: any = (nodesById[node.id] as any)?.data ?? {};
            const value = data?.[cond.dataKey];
            if ('equals' in cond && cond.equals !== undefined) {
              return value === cond.equals;
            }
            return !!value;
          })();

          if (!show) continue;

          // Expand variadic input group, if specified
          const variadic = (def as any).variadic as
            | { baseId: string; titlePattern?: string; startAt?: number; min?: number; max?: number }
            | undefined;
          if (variadic) {
            const baseId = variadic.baseId;
            const startAt = variadic.startAt ?? 1;
            const min = variadic.min ?? 1;
            const max = variadic.max;

            // Find highest connected index for this baseId
            let maxIndex = startAt - 1;
            for (const c of connections ?? []) {
              if (c.inputNodeId !== node.id) continue;
              const inputId = String(c.inputId);
              if (inputId.startsWith(baseId)) {
                const suffix = inputId.slice(baseId.length);
                const n = parseInt(suffix, 10);
                if (!Number.isNaN(n)) {
                  maxIndex = Math.max(maxIndex, n);
                }
              }
            }

            let count = Math.max(min, (maxIndex >= startAt ? maxIndex : startAt - 1) + 1);
            if (typeof max === 'number') count = Math.min(count, max);

            for (let i = startAt; i < startAt + count; i++) {
              const id = `${baseId}${i}` as PortId;
              const titleTemplate = variadic.titlePattern ?? `${def.title} {n}`;
              const title = String(titleTemplate).replace('{n}', String(i));
              expanded.push({
                id,
                title,
                dataType: def.dataType,
                required: def.required,
                data: def.data,
                defaultValue: def.defaultValue,
                description: def.description,
                coerced: def.coerced,
              });
            }
          } else {
            expanded.push(def);
          }
        }
        inputDefinitions = expanded;
      }
    } catch (err) {
      const error = getError(err);
      console.error('Error getting node input definitions', error);
      inputDefinitions = [];
    }

    try {
      outputDefinitions = nodeInstances[node.id]?.getOutputDefinitions(
        connections,
        nodesById,
        project,
        referencedProjects,
      );
    } catch (err) {
      const error = getError(err);
      console.error('Error getting node output definitions', error);
      outputDefinitions = [];
    }

    return inputDefinitions && outputDefinitions
      ? {
          inputDefinitions,
          outputDefinitions,
        }
      : { inputDefinitions: [], outputDefinitions: [] };
  });
});

export const ioDefinitionsForNodeState = atomFamily((nodeId: NodeId | undefined) =>
  atom((get) => (nodeId ? get(ioDefinitionsState)[nodeId]! : { inputDefinitions: [], outputDefinitions: [] })),
);

export const nodeConstructorsState = atom((get) => {
  get(pluginRefreshCounterState);
  return globalRivetNodeRegistry.getNodeConstructors();
});
