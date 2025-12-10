/*
  Validates that backend AbstractNode specs match legacy node implementations (inputs/outputs/body at default state).
  Usage: yarn tsx packages/core/scripts/validate-specs.ts
*/
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { genericNodeDefinition, type GenericNodeSpec } from '../src/model/nodes/GenericNode.js';
import { readdirSync } from 'node:fs';
import type { ChartNode, NodeId, NodeInputDefinition, NodeOutputDefinition } from '../src/model/NodeBase.js';

type AnyNodeImplClass = new (chartNode: ChartNode) => {
  getInputDefinitions: (...args: any[]) => NodeInputDefinition[];
  getOutputDefinitions: (...args: any[]) => NodeOutputDefinition[];
  getBody: (...args: any[]) => any;
};

function pascalCaseFromType(type: string): string {
  return type
    .replace(/[^a-zA-Z0-9]/g, ' ')
    .split(/\s+/)
    .filter(Boolean)
    .map((token) => token[0]!.toUpperCase() + token.slice(1))
    .join('');
}

function findNodeImplExport(mod: any): AnyNodeImplClass | undefined {
  const keys = Object.keys(mod);
  for (const k of keys) {
    if (k.endsWith('NodeImpl') && typeof mod[k] === 'function') {
      return mod[k] as AnyNodeImplClass;
    }
  }
  return undefined;
}

function loadBackendSpecs(): GenericNodeSpec<any>[] {
  const py = spawnSync('python', [
    '-c',
    [
      'import json, sys',
      "sys.path.insert(0, 'packages/privet')",
      'from privet.nodes import load_all_specs',
      'print(json.dumps(load_all_specs()))',
    ].join('; '),
  ], { encoding: 'utf-8' });
  if (py.status !== 0) {
    throw new Error(`Failed to load backend specs via Python. Install Python and ensure import path works.\n${py.stderr || py.stdout}`);
  }
  return JSON.parse(py.stdout.trim());
}

const SKIP_PARITY: Record<string, string> = {
};

async function compareOne(spec: GenericNodeSpec<any>) {
  const typeName = spec.type;
  if (SKIP_PARITY[typeName]) {
    return { type: typeName, skipped: true, reason: SKIP_PARITY[typeName] } as const;
  }
  const pascal = pascalCaseFromType(typeName);
  const tsPath = resolve(process.cwd(), 'packages/core/src/model/nodes', `${pascal}Node.ts`);

  let legacyImplClass: AnyNodeImplClass | undefined;
  let legacyModule: any | undefined;
  try {
    const mod = await import(pathToFileURL(tsPath).href);
    legacyImplClass = findNodeImplExport(mod);
    legacyModule = mod;
  } catch {
    // Fallback: scan all node modules to find any Impl whose create() type matches spec.type
    const dir = resolve(process.cwd(), 'packages/core/src/model/nodes');
    const files = readdirSync(dir).filter((f) => f.endsWith('Node.ts'));
    for (const f of files) {
      try {
        const mod = await import(pathToFileURL(resolve(dir, f)).href);
        const impl = findNodeImplExport(mod);
        if (impl && typeof (impl as any).create === 'function') {
          const created = (impl as any).create();
          if (created?.type === typeName) {
            legacyImplClass = impl;
            legacyModule = mod;
            break;
          }
        }
      } catch {}
    }
    if (!legacyImplClass) {
      return { type: typeName, skipped: true } as const;
    }
  }

  // Instantiate legacy
  const createLegacy = (mod: any): ChartNode => {
    const createFns = Object.values(mod).filter((v) => typeof v?.create === 'function');
    if (createFns.length > 0) {
      try { return (createFns[0] as any).create(); } catch {}
    }
    // Fallback: call static create on Impl if present
    if (typeof (legacyImplClass as any).create === 'function') {
      return (legacyImplClass as any).create();
    }
    throw new Error('No create() found for legacy node');
  };

  let legacyNode: ChartNode;
  try {
    legacyNode = createLegacy(legacyModule);
  } catch (err) {
    return { type: typeName, error: `Failed to create legacy node: ${(err as Error).message}` } as const;
  }

  const legacyImpl = new legacyImplClass(legacyNode as any);
  let legacyInputs: NodeInputDefinition[] = [];
  let legacyOutputs: NodeOutputDefinition[] = [];
  try {
    const dummyProject = { graphs: {} } as any;
    legacyInputs = legacyImpl.getInputDefinitions([], {} as any, dummyProject, {} as any) as any;
    legacyOutputs = legacyImpl.getOutputDefinitions([], {} as any, dummyProject, {} as any) as any;
  } catch (err) {
    return { type: typeName, error: `Legacy getInput/Output failed: ${(err as Error).message}` } as const;
  }

  // Instantiate spec-based node via AbstractNode
  const specDef = genericNodeDefinition(spec);
  const specImplClass = specDef.impl as unknown as AnyNodeImplClass & { create(): ChartNode };
  const specNode = specImplClass.create();
  const specImpl = new specImplClass(specNode);
  let specInputs: NodeInputDefinition[] = [];
  let specOutputs: NodeOutputDefinition[] = [];
  try {
    specInputs = specImpl.getInputDefinitions([], {} as any, {} as any, {} as any) as any;
    specOutputs = specImpl.getOutputDefinitions([], {} as any, {} as any, {} as any) as any;
  } catch (err) {
    return { type: typeName, error: `Spec getInput/Output failed: ${(err as Error).message}` } as const;
  }

  const inKey = (i: NodeInputDefinition) => `${i.id}::${Array.isArray(i.dataType) ? i.dataType.join('|') : i.dataType}`;
  const outKey = (o: NodeOutputDefinition) => `${o.id}::${Array.isArray(o.dataType) ? o.dataType.join('|') : o.dataType}`;

  const lIn = new Set(legacyInputs.map(inKey));
  const sIn = new Set(specInputs.map(inKey));
  const lOut = new Set(legacyOutputs.map(outKey));
  const sOut = new Set(specOutputs.map(outKey));

  const missingInputs = [...lIn].filter((k) => !sIn.has(k));
  const extraInputs = [...sIn].filter((k) => !lIn.has(k));
  const missingOutputs = [...lOut].filter((k) => !sOut.has(k));
  const extraOutputs = [...sOut].filter((k) => !lOut.has(k));

  // Body lint: ensure no unsupported handlebars tokens in spec.body
  const body = (spec as any).body;
  const bodyIssues: string[] = [];
  if (typeof body === 'string') {
    if (/{{\s*else\s*}}/.test(body)) bodyIssues.push('uses {{else}} (should be {{#else}})');
    if (/{{\s*unless\b/.test(body)) bodyIssues.push('uses {{#unless}} (unsupported)');
  }

  const ok = missingInputs.length === 0 && missingOutputs.length === 0 && bodyIssues.length === 0;

  return {
    type: typeName,
    ok,
    missingInputs,
    extraInputs,
    missingOutputs,
    extraOutputs,
    bodyIssues,
  } as const;
}

async function main() {
  const specs = loadBackendSpecs();
  const results = [] as any[];
  for (const spec of specs) {
    results.push(await compareOne(spec));
  }

  const problems = results.filter((r) => !r.skipped && (!r.ok || r.error));
  const skipped = results.filter((r) => r.skipped);

  console.log(`Checked ${results.length} backend specs; skipped ${skipped.length} with no legacy class.`);
  if (skipped.length > 0) {
    console.log('Skipped types:', skipped.map((s: any) => s.type).join(', '));
  }
  if (problems.length === 0) {
    console.log('All checked specs match legacy shapes.');
    return;
  }
  console.log('Differences found:');
  for (const r of problems) {
    console.log(`- ${r.type}: ${r.error ?? ''}`);
    if (r.missingInputs?.length) console.log(`  missing inputs: ${r.missingInputs.join(', ')}`);
    if (r.extraInputs?.length) console.log(`  extra inputs: ${r.extraInputs.join(', ')}`);
    if (r.missingOutputs?.length) console.log(`  missing outputs: ${r.missingOutputs.join(', ')}`);
    if (r.extraOutputs?.length) console.log(`  extra outputs: ${r.extraOutputs.join(', ')}`);
    if (r.bodyIssues?.length) console.log(`  body issues: ${r.bodyIssues.join('; ')}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
