import { globalRivetNodeRegistry, registerSpecs } from '@ironclad/rivet-core';

function getBackendBaseUrl(): string {
  // Prefer vite env var; fallback to local default
  const url = (import.meta as any)?.env?.VITE_RIVET_BACKEND_URL;
  return url || 'http://localhost:8000';
}

export async function loadAndRegisterRemoteNodes(): Promise<void> {
  const baseUrl = getBackendBaseUrl();
  const endpoint = `${baseUrl}/nodes/specs`;
  try {
    const res = await fetch(endpoint);
    if (!res.ok) {
      // Non-fatal: skip remote if unavailable
      console.warn(`Remote node specs fetch failed: ${res.status} ${res.statusText} (${endpoint})`);
      return;
    }
    const specs = await res.json();
    if (Array.isArray(specs)) {
      console.info(`Registering ${specs.length} remote node spec(s) from ${endpoint}:`, specs.map((s: any) => s?.type));
      registerSpecs(globalRivetNodeRegistry as any, specs);
    } else {
      console.warn('Remote node specs response is not an array; ignoring.', specs);
    }
  } catch (err) {
    console.warn('Failed to fetch remote node specs:', err, 'Endpoint:', endpoint);
  }
}
