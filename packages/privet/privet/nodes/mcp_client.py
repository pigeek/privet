from __future__ import annotations

import json
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Tuple

from mcp import types as mcp_types
from mcp.client import session as mcp_session
from mcp.client.streamable_http import streamable_http_client
from mcp.client.stdio import stdio_client, StdioServerParameters

# A minimal MCP client helper that keeps the dependency surface local to MCP nodes.


@asynccontextmanager
async def http_session(server_url: str, name: str, version: str) -> AsyncGenerator[mcp_session.ClientSession, None]:
    """
    Connect to an MCP HTTP server (SSE/WebSocket) and yield a ClientSession.
    """
    async with streamable_http_client(server_url) as (read_stream, write_stream, _get_session_id):
        client_info = mcp_types.Implementation(name=name or "mcp-client", version=version or "1.0.0")
        async with mcp_session.ClientSession(read_stream, write_stream, client_info=client_info) as sess:
            await sess.initialize()
            yield sess


@asynccontextmanager
async def stdio_session(
    server_cfg: Dict[str, Any],
    name: str,
    version: str,
) -> AsyncGenerator[mcp_session.ClientSession, None]:
    """
    Connect to an MCP stdio server using the provided config (command/args/env/cwd).
    """
    params = StdioServerParameters(
        command=server_cfg.get("command", ""),
        args=server_cfg.get("args") or [],
        env=server_cfg.get("env"),
        cwd=server_cfg.get("cwd"),
    )
    if not params.command:
        raise RuntimeError("MCP stdio server config missing command")

    async with stdio_client(params) as (read_stream, write_stream):
        client_info = mcp_types.Implementation(name=name or "mcp-client", version=version or "1.0.0")
        async with mcp_session.ClientSession(read_stream, write_stream, client_info=client_info) as sess:
            await sess.initialize()
            yield sess


def tool_to_dict(tool: mcp_types.Tool) -> Dict[str, Any]:
    data = tool.model_dump()
    # Align to the structure TS uses when converting to GPT functions
    return {
        "name": data.get("name"),
        "description": data.get("description"),
        "inputSchema": data.get("inputSchema"),
        "outputSchema": data.get("outputSchema"),
    }


def prompt_to_dict(prompt: mcp_types.Prompt) -> Dict[str, Any]:
    data = prompt.model_dump()
    return {
        "name": data.get("name"),
        "description": data.get("description"),
        "arguments": data.get("arugments") or data.get("arguments"),
    }


def call_result_to_dict(result: mcp_types.CallToolResult) -> Dict[str, Any]:
    data = result.model_dump()
    return {
        "content": data.get("content"),
        "structuredContent": data.get("structuredContent"),
        "isError": data.get("isError", False),
    }


def prompt_result_to_dict(result: mcp_types.GetPromptResult, prompt_name: str) -> Dict[str, Any]:
    data = result.model_dump()
    out = {
        "name": prompt_name,
        "description": data.get("description"),
        "messages": data.get("messages"),
    }
    return out


def parse_json_field(raw: Any) -> Any:
    if raw is None:
        return None
    if isinstance(raw, (dict, list)):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            return {"raw": raw}
    return raw
