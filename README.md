# 🚀 Memory Data Server (MCP Tool Provider)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight **Model Context Protocol (MCP)** server built with Python and **FastMCP**. This service acts as a tool provider that enables LLMs and Agentic AI systems (e.g., LangChain, LangGraph, Claude Desktop) to inspect and retrieve customer support records via Server-Sent Events (SSE).

---

## 📌 Key Features

* **Standardized MCP Interface:** Exposes backend tools via the open [Model Context Protocol](https://modelcontextprotocol.io/).
* **SSE Transport Layer:** Operates over HTTP via Server-Sent Events (SSE), making it Docker-friendly and easy to deploy in containerized environments.
* **Deterministic Tool Capabilities:** Exposes typed data-querying functions (`fetch_customer_ticket`) to provide dynamic context to LLM reasoning loops.

---

## 🏗 System Architecture

```text
┌─────────────────────────┐          SSE (Port 8000)         ┌──────────────────────────────┐
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
* **Transport Protocol:** SSE (Server-Sent Events) over HTTP

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python installed, then install the dependencies:

```bash
pip install mcp
```

### 2. Running the Server

Execute the script to start the FastMCP SSE server bound to `0.0.0.0:8000`:

```bash
python server.py
```

> **Note:** The server will start and wait for incoming SSE client connections on `[http://0.0.0.0:8000/sse](http://0.0.0.0:8000/sse)`.

---

## 🛠 Available Tools

### `fetch_customer_ticket`

Performs a simulated lookup for customer support tickets using a unique ticket ID.

* **Input Parameters:**
  * `ticket_id` (`int`, required): The numeric identifier of the support ticket.
* **Output:**
  * `str`: Formatted text string containing ticket owner, issue summary, and user tier (or an error message if missing).

---

## 🧪 Quick Test (Verifying SSE Endpoint)

While running the server, you can verify that the SSE endpoint is active by executing a simple GET request:

```bash
curl -i http://localhost:8000/sse
```

---

## 📜 Roadmap

- [x] Basic FastMCP server with SSE transport
- [x] In-memory database simulation tool
- [ ] Docker containerization setup
- [ ] Connect tool backend to persistent storage (PostgreSQL / AWS DynamoDB)
- [ ] Implement write/mutation tools (`create_ticket`, `update_status`)

---

## 📄 License

This project is licensed under the MIT License — free to use, modify, and distribute.