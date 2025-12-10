import { useEffect } from 'react';
import { useAtomValue } from 'jotai';
import { useExecutorSidecar } from './useExecutorSidecar';
import { useRemoteExecutor } from './useRemoteExecutor';
import { debuggerDefaultUrlState } from '../state/settings';

/**
 * Caution: only use this hook on components that will not dismount. The `useEffect` cleanup function
 * can result in a subtle bug where the remote debugger will mysteriously disconnect when the
 * component dismounts.
 * TODO Refactor so that this doesn't happen.
 * @returns
 */
export function useGraphExecutor() {
  const defaultDebuggerUrl = useAtomValue(debuggerDefaultUrlState);
  const remoteExecutor = useRemoteExecutor();

  // Always prefer remote executor and auto-connect to default debugger URL
  useExecutorSidecar({ enabled: false });

  const executor = remoteExecutor;

  useEffect(() => {
    // Connect to configured remote debugger URL (falls back internally if blank)
    remoteExecutor.remoteDebugger.connect(defaultDebuggerUrl);
    // Do not auto-disconnect; keep persistent remote debugging
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [defaultDebuggerUrl]);

  return {
    tryRunGraph: executor.tryRunGraph,
    tryAbortGraph: executor.tryAbortGraph,
    tryPauseGraph: executor.tryPauseGraph,
    tryResumeGraph: executor.tryResumeGraph,
    tryRunTests: executor.tryRunTests,
  };
}
