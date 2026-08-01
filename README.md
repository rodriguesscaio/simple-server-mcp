# 🚀 Memory Data Server (MCP Tool Provider)

A lightweight Model Context Protocol (MCP) server built with Python and **FastMCP**. This service acts as a specialized tool provider that enables LLMs and Agentic AI systems (like LangChain or Claude Desktop) to securely inspect and retrieve customer support records from an in-memory datastore via Server-Sent Events (SSE).

---

## 📌 Features

- **Standardized MCP Interface:** Exposes backend capabilities via the open [Model Context Protocol](https://modelcontextprotocol.io/).
- **SSE Transport:** Listens on HTTP via Server-Sent Events for real-time remote procedure calls (RPC).
- **Structured Tool Capabilities:** Exposes deterministic data querying functions (`fetch_customer_ticket`) with typed parameters.

---

## 🏗 System Architecture

┌─────────────────────────┐          SSE (Port 8000)         ┌──────────────────────────────┐
│  AI Agent / LLM Host    │ ───────────────────────────────► │    FastMCP Server            │
│  (LangChain / Claude)   │ ◄─────────────────────────────── │  (Memory data Server)        │
└─────────────────────────┘                                  └──────────────┬───────────────┘
│
▼
┌────────────────────┐
│ In-Memory DB Lookup│
└────────────────────┘


---

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **Framework:** `mcp` (`FastMCP`)
- **Transport:** SSE (Server-Sent Events) over HTTP

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python installed and the required dependencies:

```bash
pip install mcp
```

### 2.Running the Server
Execute the script directly to start the FastMCP SSE server listening on 0.0.0.0:8000:

```Bash
python server.py
```

The server will start and wait for incoming SSE connections on port 8000.

🛠 Available Tools
fetch_customer_ticket
Performs an in-memory lookup for customer support tickets using a numeric ticket_id.

Parameters:

ticket_id (int, required): The unique integer identifier of the target ticket.

Returns:

str: Formatted string containing user details, reported issue, and customer tier (or a formatted error message if not found).

📄 License
MIT License. Free to use and modify for personal or commercial projects.