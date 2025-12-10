import { nodeDefinition } from '../NodeDefinition.js';
import { NodeImpl, type NodeUIData , type NodeBody } from '../NodeImpl.js';
import type { ChartNode, NodeId, NodeInputDefinition, NodeOutputDefinition, PortId, ShowIfCondition, VisibilityCondition, VariadicOutputDescriptor } from '../NodeBase.js';
import { nanoid } from 'nanoid/non-secure';
import type { EditorDefinition } from '../EditorDefinition.js';
import type { NodeBodySpec } from '../NodeBodySpec.js';
import type { Inputs, Outputs } from '../GraphProcessor.js';
import type { InternalProcessContext } from '../ProcessContext.js';
import type { Project, ProjectId } from '../Project.js';
import { extractInterpolationVariables } from '../../utils/interpolation.js';
import { dedent } from '../../utils/misc.js';
import type { DataType } from '../DataValue.js';

// Runtime-friendly spec that can be pure JSON (e.g., loaded from backend)
export type GenericNodeSpec<Data = any> = {
  type: string;
  title: string;
  displayName: string;
  data: Data;
  visual?: {
    width?: number;
  };
  uiData: NodeUIData;
  // Use plain strings for ids; we will coerce internally to PortId
  inputs: (Omit<NodeInputDefinition, 'id'> & { id: string })[];
  outputs: (Omit<NodeOutputDefinition, 'id'> & { id: string; variadic?: VariadicOutputDescriptor })[];
  editors?: EditorDefinition<ChartNode<Data>>[];
  body?: string | NodeBodySpec | NodeBodySpec[];
  /** Optional: derive inputs declaratively from tokens within a data field (e.g., Text/Object). */
  interpolationInputs?: {
    dataKey: keyof Data & string;
    dataType?: DataType | Readonly<DataType[]>;
    required?: boolean;
    coerced?: boolean;
    /** Prefixes to ignore when extracting tokens. Defaults to ['@graphInputs.', '@context.'] */
    ignorePrefixes?: string[];
  };
  // Note: dynamic outputs should be expressed via per-output `variadic` descriptors
  /** Generate input ports by introspecting a selected subgraph's Graph Input nodes. */
  dynamicInputsFromSubgraph?: {
    graphIdDataKey: keyof Data & string;
    titleTemplate?: string; // defaults to id
  };
};

export function genericNodeDefinition<Data>(spec: GenericNodeSpec<Data>) {
  type ThisNode = ChartNode<typeof spec.type, Data>;

  class GenericNodeImpl extends NodeImpl<ThisNode> {
    static create(): ThisNode {
      return {
        type: spec.type,
        title: spec.title,
        id: nanoid() as NodeId,
        data: spec.data,
        visualData: {
          x: 0,
          y: 0,
          width: spec.visual?.width ?? 150,
        },
      } as ThisNode;
    }

    #evalShowIf(cond: VisibilityCondition | undefined): boolean {
      if (!cond) return true;
      // Composite conditions
      if ((cond as any).all) {
        return ((cond as any).all as VisibilityCondition[]).every((c) => this.#evalShowIf(c));
      }
      if ((cond as any).any) {
        return ((cond as any).any as VisibilityCondition[]).some((c) => this.#evalShowIf(c));
      }
      const c = cond as ShowIfCondition;
      const value = (this.chartNode.data as any)?.[c.dataKey];
      if (c.equals !== undefined) return value === c.equals;
      if (c.notEquals !== undefined) return value !== c.notEquals;
      if (c.in) return c.in.includes(value);
      if (c.notIn) return !c.notIn.includes(value);
      // default truthy check
      return Boolean(value);
    }

    #applyTitleTemplate<T extends { title: string; titleTemplate?: string }>(
      def: T,
    ): T {
      const tpl = (def as any).titleTemplate as string | undefined;
      if (!tpl) return def;
      // Very light substitution: replace {{key}} with data[key]
      const replaced = tpl.replace(/\{\{\s*([^}]+?)\s*\}\}/g, (_m, key) => {
        const v = (this.chartNode.data as any)?.[key as string];
        return v == null ? '' : String(v);
      });
      return { ...(def as any), title: replaced };
    }

    getInputDefinitions(
      connections: any,
      _nodes: Record<NodeId, ChartNode>,
      project: Project,
      _referenced: Record<ProjectId, Project>,
    ) {
      // Ensure connected inputs are always visible so edges don't disappear
      const connected = ((connections as any[] | undefined)?.filter(
        (c) => c.inputNodeId === (this.chartNode.id as unknown as NodeId),
      ) ?? []) as Array<{ inputId: string | number }>;
      const connectedInputIds = new Set<string>(connected.map((c) => String(c.inputId)));

      const expandedInputs: NodeInputDefinition[] = [];
      for (const iSpec of spec.inputs) {
        const base = this.#applyDynamicDataType(this.#applyTitleTemplate({ ...iSpec, id: iSpec.id as PortId } as any)) as any;
        const visible = this.#evalShowIf((iSpec as any).showIf) || connectedInputIds.has(String(base.id));
        if (!visible) continue;

        const variadic: any = (iSpec as any).variadic;
        if (variadic) {
          // Simple numeric variadic expansion for inputs: baseId, titlePattern, startAt, min
          const baseId: string = variadic.baseId ?? String(base.id);
          const titlePattern: string = variadic.titlePattern ?? String(base.title ?? 'Input {n}');
          const startAt: number = Number.isFinite(variadic.startAt) ? variadic.startAt : 1;
          const min: number = Number.isFinite(variadic.min) ? variadic.min : 1;
          const idPattern: string | undefined = (variadic as any).idPattern;

          // Determine max index based on connected ports with this baseId prefix
          let maxIndex = 0;
          for (const c of connected) {
            const id = String(c.inputId);
            if (!id.startsWith(baseId)) continue;
            const idxStr = id.slice(baseId.length);
            const n = parseInt(idxStr || '0', 10);
            if (!Number.isNaN(n) && n > maxIndex) maxIndex = n;
          }
          const count = Math.max(min, maxIndex + 1);
          for (let i = startAt; i <= count; i++) {
            const idStr = idPattern ? idPattern.replace('{n}', String(i)) : `${baseId}${i}`;
            const id = idStr as PortId;
            const title = titlePattern.replace('{n}', String(i));
            expandedInputs.push({ id, title, dataType: base.dataType, required: base.required, coerced: base.coerced, description: base.description } as NodeInputDefinition);
          }
          continue;
        }

        expandedInputs.push({ id: base.id, title: base.title, dataType: base.dataType, required: base.required, coerced: base.coerced, description: base.description } as NodeInputDefinition);
      }

      // Interpolation-derived inputs
      let interpolationInputs: NodeInputDefinition[] = [];
      if (spec.interpolationInputs) {
        const { dataKey, dataType = 'string', required = false, coerced = false, ignorePrefixes } =
          spec.interpolationInputs;
        const raw = (this.chartNode.data as any)?.[dataKey];
        if (typeof raw === 'string') {
          let tokens = extractInterpolationVariables(raw);
          if (ignorePrefixes && ignorePrefixes.length > 0) {
            tokens = tokens.filter((t) => !ignorePrefixes.some((p) => t.startsWith(p)));
          }
          const uniq = Array.from(new Set(tokens));
          interpolationInputs = uniq.map((name) => ({
            id: name as unknown as PortId,
            title: name,
            dataType,
            required,
            coerced,
          }));
        }
      }

      // Subgraph-derived inputs
      const subgraphInputs: NodeInputDefinition[] = [];
      if (spec.dynamicInputsFromSubgraph) {
        const { graphIdDataKey, titleTemplate } = spec.dynamicInputsFromSubgraph as any;
        const graphId = (this.chartNode.data as any)?.[graphIdDataKey];
        const graph = graphId ? (project?.graphs?.[graphId as any] as any) : undefined;
        if (graph?.nodes) {
          const inputsSet = new Set<string>();
          for (const n of graph.nodes as any[]) {
            if (n?.type === 'graphInput' && n?.data?.id) {
              const id = String(n.data.id) as PortId;
              if (inputsSet.has(String(id))) continue;
              inputsSet.add(String(id));
              const title = titleTemplate ? String(titleTemplate).replace(/\{\{\s*id\s*\}\}/g, String(n.data.id)) : String(n.data.id);
              subgraphInputs.push({ id, title, dataType: n.data.dataType } as NodeInputDefinition);
            }
          }
        }
      }

      return [...expandedInputs, ...interpolationInputs, ...subgraphInputs];
    }

    getOutputDefinitions(
      connections: any,
      _nodes: Record<NodeId, ChartNode>,
      project: Project,
      _referenced: Record<ProjectId, Project>,
    ) {
      const outputs: NodeOutputDefinition[] = [];
      // Expand outputs, handling variadic descriptors encoded in each output
      for (const oSpec of spec.outputs) {
        const specWithId = { ...oSpec, id: oSpec.id as PortId } as any;
        if (!this.#evalShowIf(specWithId.showIf)) continue;
        const base = this.#applyDynamicDataType(this.#applyTitleTemplate(specWithId)) as any;
        const variadic: VariadicOutputDescriptor | undefined = (oSpec as any).variadic;
        if (!variadic) {
          outputs.push({ id: base.id, title: base.title, dataType: base.dataType, description: base.description } as NodeOutputDefinition);
          continue;
        }

        // Handle regex-derived variadic outputs
        if (variadic.type === 'regex') {
          const { baseId, titlePattern = 'Output {n}', startAt = 1, regexDataKey, multilineDataKey } = variadic;
          const pattern = String((this.chartNode.data as any)?.[regexDataKey] ?? '');
          const multiline = multilineDataKey ? Boolean((this.chartNode.data as any)?.[multilineDataKey]) : false;
          try {
            const flags = multiline ? 'gm' : 'g';
            const regExp = new RegExp(pattern, flags);
            const src = regExp.source;
            let count = 0;
            let inClass = false;
            for (let i = 0; i < src.length; i++) {
              const ch = src[i]!;
              const prev = i > 0 ? src[i - 1] : null;
              if (ch === '[' && prev !== '\\') inClass = true;
              else if (ch === ']' && prev !== '\\') inClass = false;
              else if (ch === '(' && prev !== '\\' && !inClass) {
                if (src[i + 1] !== '?' || src[i + 2] === ':') count++;
              }
            }
            for (let i = 0; i < count; i++) {
              const n = i + startAt;
              const id = `${baseId}${n}` as PortId;
              const title = (titlePattern || String(base.title ?? 'Output {n}')).replace('{n}', String(n));
              outputs.push({ id, title, dataType: base.dataType } as NodeOutputDefinition);
            }
          } catch (_err) {
            // Invalid regex; skip dynamic outputs
          }
          continue;
        }

        if (variadic.type === 'mirror') {
          const { inputBaseId, baseId, titlePattern = 'Output {n}', startAt = 1, excludeLast } = variadic as any;
          const inputNodeId = this.chartNode.id as unknown as NodeId;
          const inputConnections = (connections as any[] | undefined)?.filter(
            (c) => c.inputNodeId === inputNodeId && String(c.inputId).startsWith(inputBaseId),
          ) ?? [];
          let maxIndex = 0;
          for (const c of inputConnections) {
            const m = String(c.inputId).slice(inputBaseId.length);
            const i = parseInt(m || '0', 10);
            if (!Number.isNaN(i) && i > maxIndex) maxIndex = i;
          }
          let count = Math.max(startAt, maxIndex + 1);
          if (excludeLast && count > 0) count -= 1;
          for (let i = startAt; i <= count; i++) {
            const id = `${baseId}${i}` as PortId;
            const title = (titlePattern || String(base.title ?? 'Output {n}')).replace('{n}', String(i));
            outputs.push({ id, title, dataType: base.dataType } as NodeOutputDefinition);
          }
          continue;
        }

        // Handle data-list-derived variadic outputs
        if (variadic.type === 'dataList') {
          const { dataKey, baseId, titleTemplate, startAt = 0, idTemplate } = variadic as any;
          const arr = (this.chartNode.data as any)?.[dataKey];
          if (Array.isArray(arr)) {
            for (let i = 0; i < arr.length; i++) {
              const item = arr[i];
              const idStr = idTemplate
                ? String(idTemplate).replace(/\{\{\s*item\s*\}\}/g, String(item))
                : `${baseId}${i + startAt}`;
              const id = idStr as PortId;
              let title = String(base.title ?? String(item));
              if (titleTemplate) {
                title = titleTemplate.replace(/\{\{\s*item\s*\}\}/g, String(item));
              }
              outputs.push({ id, title, dataType: base.dataType } as NodeOutputDefinition);
            }
          }
          continue;
        }

        if (variadic.type === 'subgraph') {
          const { graphIdDataKey, titleTemplate } = variadic as any;
          const graphId = (this.chartNode.data as any)?.[graphIdDataKey];
          const graph = graphId ? (project?.graphs?.[graphId as any] as any) : undefined;
          if (graph?.nodes) {
            const seen = new Set<string>();
            for (const n of graph.nodes as any[]) {
              if (n?.type === 'graphOutput' && n?.data?.id) {
                const id = String(n.data.id) as PortId;
                if (seen.has(String(id))) continue;
                seen.add(String(id));
                const title = titleTemplate
                  ? String(titleTemplate).replace(/\{\{\s*id\s*\}\}/g, String(n.data.id))
                  : String(n.data.id);
                outputs.push({ id, title, dataType: n.data.dataType } as NodeOutputDefinition);
              }
            }
          }
          continue;
        }

        // Unknown variadic type: ignore and push base as-is
        outputs.push({ id: base.id, title: base.title, dataType: base.dataType } as NodeOutputDefinition);
      }

      return outputs;
    }

    #applyDynamicDataType<T extends { dataType?: DataType | Readonly<DataType[]>; dataTypeFrom?: { dataKey: string; map?: Record<string, DataType | Readonly<DataType[]>> } }>(
      def: T,
    ): T {
      const cfg = (def as any).dataTypeFrom as { dataKey: string; map?: Record<string, DataType | Readonly<DataType[]>> } | undefined;
      if (!cfg) return def;
      const raw = (this.chartNode.data as any)?.[cfg.dataKey];
      if (raw == null) return def;
      const mapped = cfg.map ? cfg.map[String(raw)] : (String(raw) as any);
      if (mapped) {
        return { ...(def as any), dataType: mapped };
      }
      return def;
    }

    async process(_inputs: Inputs, _context: InternalProcessContext): Promise<Outputs> {
      throw new Error('GenericNode is remote-only: no local process implementation');
    }

    getEditors(): EditorDefinition<ThisNode>[] {
      return (spec.editors ?? []) as EditorDefinition<ThisNode>[];
    }

    #evaluateTemplate(template: string, data: any): string {
      const evalCond = (expr: string): boolean => {
        const e = expr.trim();
        const eqMatch = e.match(/^([a-zA-Z0-9_\.]+)\s*==\s*['\"]([\s\S]*?)['\"]/);
        if (eqMatch) {
          const [, key, expected] = eqMatch;
          const value = key.split('.').reduce((acc: any, k: string) => (acc ? acc[k] : undefined), data);
          return String(value) === expected;
        }
        const value = e.split('.').reduce((acc: any, k: string) => (acc ? acc[k] : undefined), data);
        return !!value;
      };

      let output = template;
      while (true) {
        const ifStart = output.indexOf('{{#if');
        if (ifStart === -1) break;
        const ifStartClose = output.indexOf('}}', ifStart);
        if (ifStartClose === -1) break;

        const ifHeader = output.slice(ifStart, ifStartClose + 2);
        const ifCond = ifHeader.replace('{{#if', '').replace('}}', '').trim();

        let pos = ifStartClose + 2;
        let depth = 1;
        const controls: Array<{ kind: 'elseif' | 'else' | 'endif'; start: number; end: number; cond?: string }> = [];
        while (pos < output.length && depth > 0) {
          const nextIf = output.indexOf('{{#if', pos);
          const nextElseIf = output.indexOf('{{#elseif', pos);
          const nextElse = output.indexOf('{{#else}}', pos);
          const nextEndIf = output.indexOf('{{/if}}', pos);
          const candidates = [nextIf, nextElseIf, nextElse, nextEndIf].filter((i) => i !== -1) as number[];
          if (candidates.length === 0) break;
          const next = Math.min(...candidates);
          if (next === nextIf) {
            depth++;
            pos = output.indexOf('}}', next) + 2;
            continue;
          }
          if (next === nextEndIf) {
            depth--;
            if (depth === 0) {
              controls.push({ kind: 'endif', start: next, end: next + '{{/if}}'.length });
              break;
            }
            pos = next + '{{/if}}'.length;
            continue;
          }
          if (depth === 1) {
            if (next === nextElse) {
              controls.push({ kind: 'else', start: next, end: next + '{{#else}}'.length });
              pos = next + '{{#else}}'.length;
              continue;
            }
            if (next === nextElseIf) {
              const headClose = output.indexOf('}}', next);
              const elseifHeader = output.slice(next, headClose + 2);
              const elseifCond = elseifHeader.replace('{{#elseif', '').replace('}}', '').trim();
              controls.push({ kind: 'elseif', start: next, end: headClose + 2, cond: elseifCond });
              pos = headClose + 2;
              continue;
            }
          }
          pos = next + 1;
        }

        const endControl = controls.find((c) => c.kind === 'endif');
        if (!endControl) break;

        const innerStart = ifStartClose + 2;
        const innerEnd = endControl.start;
        const inner = output.slice(innerStart, innerEnd);

        const branches: { cond?: string; content: string }[] = [];
        let elseContent: string | undefined;
        const topControls = controls.filter((c) => c.kind !== 'endif');
        const firstBoundary = topControls.length > 0 ? topControls[0]!.start - innerStart : inner.length;
        branches.push({ cond: ifCond, content: inner.slice(0, firstBoundary) });
        for (let i = 0; i < topControls.length; i++) {
          const ctrl = topControls[i]!;
          const segStart = ctrl.end - innerStart;
          const segEnd = (topControls[i + 1]?.start ?? endControl.start) - innerStart;
          if (ctrl.kind === 'elseif') branches.push({ cond: ctrl.cond, content: inner.slice(segStart, segEnd) });
          else if (ctrl.kind === 'else') elseContent = inner.slice(segStart, segEnd);
        }

        let chosen = '';
        for (const b of branches) {
          if (!b.cond || evalCond(b.cond)) { chosen = b.content; break; }
        }
        if (!chosen && elseContent) chosen = elseContent;

        output = output.slice(0, ifStart) + chosen + output.slice(endControl.end);
      }

      output = output.replace(/{{\s*([a-zA-Z0-9_\.]+)\s*}}/g, (_m, key: string) => {
        const value = key.split('.').reduce((acc: any, k: string) => (acc ? acc[k] : undefined), data);
        return value === undefined || value === null ? '' : String(value);
      });

      return output;
    }

    getBody(): NodeBody {
      const data = (this.chartNode as any).data;
      const b = spec.body as NodeBody;
      if (typeof b === 'string') {
        return this.#evaluateTemplate(dedent(b).trim(), data);
      }
      if (Array.isArray(b)) {
        return b.map((s: any) =>
          s && typeof s.text === 'string'
            ? { ...s, text: this.#evaluateTemplate(dedent(s.text).trim(), data) }
            : s,
        ) as any;
      }
      if (b && typeof (b as any).text === 'string') {
        return { ...(b as any), text: this.#evaluateTemplate(dedent((b as any).text).trim(), data) } as any;
      }
      return b;
    }

    static getUIData(): NodeUIData {
      return spec.uiData;
    }
  }

  return nodeDefinition(GenericNodeImpl as any, spec.displayName);
}
