# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal MCP (Model Context Protocol) tool-provider server built with `FastMCP`. It exposes one tool, `fetch_customer_ticket`, over SSE transport so LLM agent hosts (LangChain, LangGraph, Claude Desktop, etc.) can query customer support tickets. All state is an in-memory mock dict in `server.py` — there is no real database.

## Commands

Set up the environment (a `.venv` already exists in this repo):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-tests.txt
```

Run the server (binds to `0.0.0.0:8000`, SSE endpoint at `/sse`):
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

Verify the SSE endpoint manually while the server is running:
```bash
curl -i http://localhost:8000/sse
```

Docker build/run:
```bash
docker build -t simple-server-mcp .
docker run -p 8000:8000 simple-server-mcp
```

CI (`.github/workflows/test.yml`) runs `pytest` on every push/PR to `main`.

## Architecture

- `server.py` — the entire server. A `FastMCP` instance is configured with host/port, tools are registered with the `@mcp.tool()` decorator, and `mcp.run(transport="sse")` starts the SSE server when run as `__main__`. New tools follow the same pattern: a plain typed Python function decorated with `@mcp.tool()`, docstring/signature drives the MCP tool schema exposed to agents.
- `test_server.py` — two testing styles against the same tool, both worth keeping when adding tools:
  1. Direct unit tests calling the Python function itself (e.g. `fetch_customer_ticket(101)`).
  2. Integration tests going through the MCP layer via `await mcp.call_tool("tool_name", {...})`, which returns `(content_list, _)`; assert against `content_list[0].text`. These require `pytest-asyncio` and are marked `@pytest.mark.asyncio`.
- No persistence layer, no auth, no config file — everything is hardcoded in `server.py` (host, port, mock data). Treat these as the current scope of the project, not oversights, unless asked to extend them (see README roadmap: Docker hardening, persistent storage, mutation tools are explicitly unfinished/planned).
