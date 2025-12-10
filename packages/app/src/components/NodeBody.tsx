import { type FC, Suspense, memo, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { type HeightCache, useNodeBodyHeight } from '../hooks/useNodeBodyHeight';
import { useUnknownNodeComponentDescriptorFor } from '../hooks/useNodeTypes.js';
import {
  type ChartNode,
  type ColorizedNodeBodySpec,
  type MarkdownNodeBodySpec,
  type NodeBodySpec,
  type PlainNodeBodySpec,
  globalRivetNodeRegistry,
  type NodeBody as RenderedNodeBody,
  getError,
  type NodeId,
} from '@ironclad/rivet-core';
// No remote-spec fallback: bodies must come from impls (AbstractNode or legacy)
import { useMarkdown } from '../hooks/useMarkdown';
import { match } from 'ts-pattern';
import styled from '@emotion/styled';
import { LazyColorizedPreformattedText } from './LazyComponents';
import { useDependsOnPlugins } from '../hooks/useDependsOnPlugins';
import { useGetRivetUIContext } from '../hooks/useGetRivetUIContext';
import { useAsyncEffect } from 'use-async-effect';
import { toast } from 'react-toastify';
import { useAtomValue } from 'jotai';
import { pluginRefreshCounterState, registryReadyState } from '../state/plugins';

export const NodeBody: FC<{ heightCache: HeightCache; node: ChartNode }> = memo(({ heightCache, node }) => {
  const { Body } = useUnknownNodeComponentDescriptorFor(node);
  useDependsOnPlugins();

  const body = Body ? <Body node={node} /> : <UnknownNodeBody heightCache={heightCache} node={node} />;

  return <div className="node-body">{body}</div>;
});

NodeBody.displayName = 'NodeBody';

const UnknownNodeBodyWrapper = styled.div<{
  fontSize: number;
  fontFamily: 'monospace' | 'sans-serif';
}>`
  overflow: hidden;
  font-size: ${(props) => props.fontSize}px;
  font-family: ${(props) => (props.fontFamily === 'monospace' ? "'Roboto Mono', monospace" : "'Roboto', sans-serif")};
`;

// Fixes flickering due to async rendering of node body by caching the last rendered body
const previousRenderedBodyMap = new Map<NodeId, RenderedNodeBody>();

const UnknownNodeBody: FC<{ heightCache: HeightCache; node: ChartNode }> = ({ heightCache, node }) => {
  const getUIContext = useGetRivetUIContext();
  const refreshCounter = useAtomValue(pluginRefreshCounterState);

  const [body, setBody] = useState<RenderedNodeBody | undefined>(previousRenderedBodyMap.get(node.id));
  const { ref, height } = useNodeBodyHeight(heightCache, node.id, !!body);
  const registryReady = useAtomValue(registryReadyState);

  useAsyncEffect(async () => {
    if (!registryReady) return;
    try {
      const impl = globalRivetNodeRegistry.createDynamicImpl(node);
      const renderedBody = await impl.getBody(await getUIContext({ node }));

      setBody(renderedBody);
      previousRenderedBodyMap.set(node.id, renderedBody);
    } catch (err) {
      // eslint-disable-next-line no-console
      console.warn(`Failed to load body for node ${node.id}: ${getError(err).message}`);
    }
  }, [node, getUIContext, refreshCounter, registryReady]);

  // Simple, text-only template engine for plain string bodies
  function evaluateTemplate(template: string, data: any): string {
    const evalCond = (expr: string): boolean => {
      const e = expr.trim();
      // Equality check: key == 'value' or key == "value"
      const eqMatch = e.match(/^([a-zA-Z0-9_\.]+)\s*==\s*['\"]([\s\S]*?)['\"]/);
      if (eqMatch) {
        const [, key, expected] = eqMatch;
        const value = key.split('.').reduce((acc: any, k: string) => (acc ? acc[k] : undefined), data);
        return String(value) === expected;
      }
      // Truthy check: key
      const value = e.split('.').reduce((acc: any, k: string) => (acc ? acc[k] : undefined), data);
      return !!value;
    };

    // Process {{#if}}..{{/if}} blocks iteratively, supporting nesting and elseif/else branches
    let output = template;
    while (true) {
      const ifStart = output.indexOf('{{#if');
      if (ifStart === -1) break;
      const ifStartClose = output.indexOf('}}', ifStart);
      if (ifStartClose === -1) break;

      const ifHeader = output.slice(ifStart, ifStartClose + 2);
      const ifCond = ifHeader.replace('{{#if', '').replace('}}', '').trim();

      // Scan forward to find matching {{/if}} accounting for nested blocks
      let pos = ifStartClose + 2;
      let depth = 1;
      const controls: Array<{ kind: 'elseif' | 'else' | 'endif'; start: number; end: number; cond?: string }> = [];
      while (pos < output.length && depth > 0) {
        const nextIf = output.indexOf('{{#if', pos);
        const nextElseIf = output.indexOf('{{#elseif', pos);
        const nextElse = output.indexOf('{{#else}}', pos);
        const nextEndIf = output.indexOf('{{/if}}', pos);

        // Find nearest control token
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
        // Otherwise skip token at deeper depth
        pos = (next === nextElseIf || next === nextElse) ? next + 1 : next + 1;
      }

      const endControl = controls.find((c) => c.kind === 'endif');
      if (!endControl) break;

      const innerStart = ifStartClose + 2;
      const innerEnd = endControl.start;
      const inner = output.slice(innerStart, innerEnd);

      // Build branches from controls at depth 1
      const branches: { cond?: string; content: string }[] = [];
      let cursor = 0;
      let elseContent: string | undefined;
      const topControls = controls.filter((c) => c.kind !== 'endif');
      // First IF branch
      const firstBoundary = topControls.length > 0 ? topControls[0]!.start - innerStart : inner.length;
      branches.push({ cond: ifCond, content: inner.slice(0, firstBoundary) });
      cursor = firstBoundary;

      for (let i = 0; i < topControls.length; i++) {
        const ctrl = topControls[i]!;
        const segStart = ctrl.end - innerStart;
        const segEnd = (topControls[i + 1]?.start ?? endControl.start) - innerStart;
        if (ctrl.kind === 'elseif') {
          branches.push({ cond: ctrl.cond, content: inner.slice(segStart, segEnd) });
        } else if (ctrl.kind === 'else') {
          elseContent = inner.slice(segStart, segEnd);
        }
      }

      // Choose branch and replace
      let chosen = '';
      for (const b of branches) {
        if (!b.cond || evalCond(b.cond)) { chosen = b.content; break; }
      }
      if (!chosen && elseContent) chosen = elseContent;

      output = output.slice(0, ifStart) + chosen + output.slice(endControl.end);
    }

    // Simple variable replacement: {{key}}
    output = output.replace(/{{\s*([a-zA-Z0-9_\.]+)\s*}}/g, (_, key: string) => {
      const value = key.split('.').reduce((acc: any, k: string) => (acc ? acc[k] : undefined), data);
      return value === undefined || value === null ? '' : String(value);
    });

    return output;
  }

  const bodySpec: NodeBodySpec | NodeBodySpec[] | undefined =
    typeof body === 'string' ? { type: 'plain', text: evaluateTemplate(body, (node as any).data) } : body;
  let allSpecs = bodySpec ? (Array.isArray(bodySpec) ? bodySpec : [bodySpec]) : [];

  allSpecs = allSpecs.map((spec) => {
    if (spec.type === 'plain' && spec.text.startsWith('!markdown')) {
      return { type: 'markdown', text: spec.text.replace(/^!markdown/, '') };
    }

    return spec;
  });

  const renderedSpecs = allSpecs.map((spec) => ({
    spec,
    rendered: match(spec)
      .with({ type: 'plain' }, (spec) => <PlainNodeBody {...spec} />)
      .with({ type: 'markdown' }, (spec) => <MarkdownNodeBody {...spec} />)
      .with({ type: 'colorized' }, (spec) => <ColorizedNodeBody {...spec} />)
      .exhaustive(),
  }));

  return (
    <div ref={ref} style={{ height }}>
      {renderedSpecs.map(({ spec, rendered }, i) => (
        <UnknownNodeBodyWrapper key={i} fontFamily={spec.fontFamily ?? 'sans-serif'} fontSize={spec.fontSize ?? 12}>
          {rendered}
        </UnknownNodeBodyWrapper>
      ))}
    </div>
  );
};

export const PlainNodeBody: FC<PlainNodeBodySpec> = memo(({ text }) => {
  return <pre className="pre-wrap">{text}</pre>;
});

PlainNodeBody.displayName = 'PlainNodeBody';

export const MarkdownNodeBody: FC<MarkdownNodeBodySpec> = memo(({ text }) => {
  const markdownBody = useMarkdown(text);

  return <div className="pre-wrap" dangerouslySetInnerHTML={markdownBody} />;
});

MarkdownNodeBody.displayName = 'MarkdownNodeBody';

export const ColorizedNodeBody: FC<ColorizedNodeBodySpec> = memo(({ text, language, theme }) => {
  return (
    <Suspense fallback={<div />}>
      <LazyColorizedPreformattedText text={text} language={language} theme={theme} />
    </Suspense>
  );
});

ColorizedNodeBody.displayName = 'ColorizedNodeBody';
