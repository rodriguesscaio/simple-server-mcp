# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal MCP (Model Context Protocol) tool-provider server built with `FastMCP`. It exposes three tools — `fetch_customer_ticket`, `create_ticket`, `update_status` — over Streamable HTTP transport so LLM agent hosts (LangChain, LangGraph, Claude Desktop, etc.) can query and mutate customer support tickets. All state lives in `_ticket_db`, a module-level dict in `server.py` — there is no real database, so state resets whenever the process restarts.

## Commands

Set up the environment (a `.venv` already exists in this repo):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-tests.txt
```

Run the server (binds to `0.0.0.0:8000`, MCP endpoint at `/mcp`):
```bash
python server.py
```

Run all tests (use `python -m pytest`, not a bare `pytest` — a global Homebrew `pytest` on `PATH` will shadow the venv's and fail with `ModuleNotFoundError: mcp.server.fastmcp`):
```bash
python -m pytest
```

Run a single test:
```bash
python -m pytest test_server.py::test_fetch_customer_ticket_success
```

Verify the MCP endpoint manually while the server is running (Streamable HTTP requires a proper `initialize` request, not a bare GET):
```bash
curl -i -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl-test","version":"1.0"}}}'
```

Docker build/run:
```bash
docker build -t simple-server-mcp .
docker run -p 8000:8000 simple-server-mcp
```

CI (`.github/workflows/test.yml`) runs `pytest` on every push/PR to `main`.

## Architecture

- `server.py` — the entire server. A `FastMCP` instance is configured with host/port, tools are registered with the `@mcp.tool()` decorator, and `mcp.run(transport="streamable-http")` starts the server when run as `__main__`. New tools follow the same pattern: a plain typed Python function decorated with `@mcp.tool()`, docstring/signature drives the MCP tool schema exposed to agents.
- `_ticket_db` (module-level dict in `server.py`) is the single shared mutable state for all three tools. `fetch_customer_ticket` reads it; `create_ticket` and `update_status` mutate it in place. `_format_ticket` is the shared string-formatting helper all three tools use for their return value.
- `test_server.py` — two testing styles against the same tools, both worth keeping when adding new ones:
  1. Direct unit tests calling the Python function itself (e.g. `fetch_customer_ticket(101)`).
  2. Integration tests going through the MCP layer via `await mcp.call_tool("tool_name", {...})`, which returns `(content_list, _)`; assert against `content_list[0].text`. These require `pytest-asyncio` and are marked `@pytest.mark.asyncio`.
  Because `_ticket_db` is shared mutable module state, an `autouse` fixture (`reset_ticket_db`) resets it to a deep-copied seed snapshot before every test — required so `create_ticket`/`update_status` tests don't leak state into each other or depend on run order. New tests that mutate `_ticket_db` rely on this fixture already resetting it; no per-test cleanup needed.
- No persistence layer, no auth, no config file — everything is hardcoded in `server.py` (host, port, mock data). Treat these as the current scope of the project, not oversights, unless asked to extend them (see README roadmap: persistent storage is still explicitly unfinished/planned).
