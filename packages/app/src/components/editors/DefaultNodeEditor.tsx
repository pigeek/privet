import { type FC, useEffect, useState } from 'react';
import { type ChartNode, type EditorDefinition, getError, globalRivetNodeRegistry } from '@ironclad/rivet-core';
import { css } from '@emotion/react';
import { toast } from 'react-toastify';
import { type SharedEditorProps } from './SharedEditorProps';
import { DefaultNodeEditorField } from './DefaultNodeEditorField';
import { useGetRivetUIContext } from '../../hooks/useGetRivetUIContext';
import { produce } from 'immer';

export const defaultEditorContainerStyles = css`
  display: flex;
  flex-direction: column;
  align-items: stretch;
  width: 100%;
  align-content: start;
  gap: 8px;
  flex: 1 1 auto;
  min-height: 0;

  .row {
    display: grid;
    grid-template-columns: 1fr auto;
    column-gap: 16px;
  }

  .use-input-toggle {
    align-self: top;
    margin-top: 36px;
  }

  .data-type-selector {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    column-gap: 16px;
  }

  .editor-wrapper-wrapper {
    min-height: 200px;
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    position: relative;
    /* height: 100%; */
  }

  .editor-wrapper {
    position: absolute;
    top: 24px;
    left: 0;
    right: 0;
    bottom: 0;
  }

  .editor-container {
    height: 100%;
  }

  .row.code {
    min-height: 500px;
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
  }

  .row.toggle > div {
    display: flex;
    align-items: center;
    gap: 8px;

    label:first-of-type {
      min-width: 75px;
    }

    label:nth-of-type(2) {
      min-width: 32px;
    }

    &.use-input-toggle label:first-of-type {
      min-width: unset;
    }

    div,
    label {
      margin: 0;
    }
  }

  .helper-message {
  }
`;

export const DefaultNodeEditor: FC<
  Omit<SharedEditorProps, 'isDisabled'> & {
    onClose?: () => void;
  }
> = ({ node, onChange, isReadonly, onClose }) => {
  const [editors, setEditors] = useState<EditorDefinition<ChartNode>[]>([]);

  const getUIContext = useGetRivetUIContext();

  useEffect(() => {
    (async () => {
      try {
        const dynamicImpl = globalRivetNodeRegistry.createDynamicImpl(node);

        let loadedEditors = await dynamicImpl.getEditors(await getUIContext({ node }));

        loadedEditors = produce(loadedEditors, (draft) => {
          const autoFocused = draft.find((e) => e.autoFocus);
          if (!autoFocused) {
            const firstStringOrCodeEditor = draft.find(
              (e) =>
                e.type === 'string' ||
                e.type === 'code' ||
                e.type === 'number' ||
                e.type === 'dropdown' ||
                e.type === 'anyData',
            );
            if (firstStringOrCodeEditor) {
              firstStringOrCodeEditor.autoFocus = true;
            }
          }
        });

        setEditors(loadedEditors);
      } catch (err) {
        toast.error(`Failed to load editors for node ${node.id}: ${getError(err).message}`);
      }
    })();
  }, [node, getUIContext]);

  const isVisible = (editor: EditorDefinition<ChartNode>) => {
    const cond = (editor as any).showIf as { dataKey: string; equals?: unknown } | undefined;
    if (!cond) return true;
    const value = (node as any).data?.[cond.dataKey];
    if (cond.equals !== undefined) return value === cond.equals;
    return !!value;
  };

  const visibleEditors = editors
    .map((e) => (e.type === 'group' ? { ...e, editors: e.editors.filter(isVisible) } : e))
    .filter((e) => (e.type === 'group' ? e.editors.length > 0 : isVisible(e)));

  return (
    <div css={defaultEditorContainerStyles}>
      {visibleEditors.map((editor, i) => {
        const isDisabled = editor.disableIf?.(node.data) ?? false;
        const key =
          editor.type === 'group'
            ? `group:${editor.label ?? i}`
            : (editor as any).dataKey ?? (editor as any).customEditorId ?? `${editor.type}:${i}`;
        return (
          <DefaultNodeEditorField
            key={key}
            node={node}
            onChange={onChange}
            editor={editor}
            isReadonly={isReadonly}
            isDisabled={isDisabled}
            onClose={onClose}
          />
        );
      })}
    </div>
  );
};
