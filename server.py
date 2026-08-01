from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    "Memory data Server",
    host="0.0.0.0",
    port=8000
)


@mcp.tool()
def fetch_customer_ticket(ticket_id: int) -> str:
    # Simulating a database lookup
    mock_db = {
        101: {"user": "Caio", "issue": "Database timeout error when saving profile", "tier": "Enterprise"},
        102: {"user": "Diego", "issue": "Billing dashboard shows 404 on invoices", "tier": "Free"}
    }

    ticket = mock_db.get(ticket_id)
    if ticket:
        return f"TICKET #{ticket_id} Found - User: {ticket['user']} | Issue: {ticket['issue']} | Customer Tier: {ticket['tier']}"
    return f"Ticket #{ticket_id} not found in database."


if __name__ == "__main__":
    mcp.run(transport="sse")