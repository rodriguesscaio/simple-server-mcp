from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    "Memory data Server",
    host="0.0.0.0",
    port=8000
)

VALID_STATUSES = {"open", "in_progress", "resolved", "closed"}

# Simulating a database
_ticket_db = {
    101: {"user": "Caio", "issue": "Database timeout error when saving profile", "tier": "Enterprise", "status": "open"},
    102: {"user": "Diego", "issue": "Billing dashboard shows 404 on invoices", "tier": "Free", "status": "open"},
}


def _format_ticket(ticket_id: int, ticket: dict, verb: str = "Found") -> str:
    return (
        f"TICKET #{ticket_id} {verb} - User: {ticket['user']} | Issue: {ticket['issue']} | "
        f"Customer Tier: {ticket['tier']} | Status: {ticket['status']}"
    )


@mcp.tool()
def fetch_customer_ticket(ticket_id: int) -> str:
    ticket = _ticket_db.get(ticket_id)
    if ticket:
        return _format_ticket(ticket_id, ticket)
    return f"Ticket #{ticket_id} not found in database."


@mcp.tool()
def create_ticket(user: str, issue: str, tier: str = "Free") -> str:
    ticket_id = max(_ticket_db) + 1 if _ticket_db else 101
    _ticket_db[ticket_id] = {"user": user, "issue": issue, "tier": tier, "status": "open"}
    return _format_ticket(ticket_id, _ticket_db[ticket_id], verb="Created")


@mcp.tool()
def update_status(ticket_id: int, status: str) -> str:
    if status not in VALID_STATUSES:
        return f"Invalid status '{status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}."

    ticket = _ticket_db.get(ticket_id)
    if not ticket:
        return f"Ticket #{ticket_id} not found in database."

    ticket["status"] = status
    return _format_ticket(ticket_id, ticket, verb="Updated")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
