# 🚀 Memory Data Server (MCP Tool Provider)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight **Model Context Protocol (MCP)** server built with Python and **FastMCP**. This service acts as a tool provider that enables LLMs and Agentic AI systems (e.g., LangChain, LangGraph, Claude Desktop) to inspect and manage customer support records via Streamable HTTP.

---

## 📌 Key Features

* **Standardized MCP Interface:** Exposes backend tools via the open [Model Context Protocol](https://modelcontextprotocol.io/).
* **Streamable HTTP Transport:** Operates over HTTP via MCP's current Streamable HTTP transport, making it Docker-friendly and easy to deploy in containerized environments.
* **Deterministic Tool Capabilities:** Exposes typed data-querying and mutation functions (`fetch_customer_ticket`, `create_ticket`, `update_status`) to provide dynamic context to LLM reasoning loops.

---

## 🏗 System Architecture

```text
┌─────────────────────────┐    Streamable HTTP (Port 8000)   ┌──────────────────────────────┐
│  AI Agent / LLM Host    │ ───────────────────────────────► │    FastMCP Tool Server       │
│  (LangChain / Claude)   │ ◄─────────────────────────────── │   (Memory Data Server)       │
└─────────────────────────┘                                  └──────────────┬───────────────┘
                                                                            │
                                                                            ▼
                                                                 ┌────────────────────┐
                                                                 │ In-Memory DB Lookup│
                                                                 └────────────────────┘
```

---

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Framework:** `mcp` (`FastMCP`)
* **Transport Protocol:** Streamable HTTP over HTTP

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Running the Server

Execute the script to start the FastMCP Streamable HTTP server bound to `0.0.0.0:8000`:

```bash
python server.py
```

> **Note:** The server will start and expose its MCP endpoint at `http://0.0.0.0:8000/mcp`.

---

## 🛠 Available Tools

### `fetch_customer_ticket`

Performs a lookup for customer support tickets using a unique ticket ID.

* **Input Parameters:**
  * `ticket_id` (`int`, required): The numeric identifier of the support ticket.
* **Output:**
  * `str`: Formatted text string containing ticket owner, issue summary, customer tier, and status (or an error message if missing).

### `create_ticket`

Creates a new customer support ticket with an auto-assigned ID and `open` status.

* **Input Parameters:**
  * `user` (`str`, required): Name of the customer opening the ticket.
  * `issue` (`str`, required): Description of the issue.
  * `tier` (`str`, optional, default `"Free"`): Customer tier.
* **Output:**
  * `str`: Formatted text string confirming the created ticket.

### `update_status`

Updates the status of an existing ticket.

* **Input Parameters:**
  * `ticket_id` (`int`, required): The ticket to update.
  * `status` (`str`, required): One of `open`, `in_progress`, `resolved`, `closed`.
* **Output:**
  * `str`: Formatted text string confirming the update, or an error message if the ticket is missing or the status is invalid.

---

## 🧪 Quick Test (Verifying the MCP Endpoint)

While running the server, you can verify the Streamable HTTP endpoint is active with an MCP `initialize` request:

```bash
curl -i -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl-test","version":"1.0"}}}'
```

---

## 📜 Roadmap

- [x] Basic FastMCP server with Streamable HTTP transport
- [x] In-memory database simulation tool
- [x] Implement write/mutation tools (`create_ticket`, `update_status`)
- [x] Docker containerization setup
- [ ] Connect tool backend to persistent storage (PostgreSQL / AWS DynamoDB)

---

## 📄 License

This project is licensed under the MIT License — free to use, modify, and distribute.