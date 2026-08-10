import pytest
from server import fetch_customer_ticket, mcp


# ==========================================
# 1. Direct Unit Tests (Testing Python Logic)
# ==========================================

def test_fetch_customer_ticket_success():
    result = fetch_customer_ticket(101)
    assert "User: Caio" in result
    assert "Customer Tier: Enterprise" in result


def test_fetch_customer_ticket_not_found():
    result = fetch_customer_ticket(999)
    assert result == "Ticket #999 not found in database."


# ==========================================
# 2. FastMCP Tool Integration Tests (Async)
# Here we using the context to do assert based on answer.
# ==========================================

@pytest.mark.asyncio
async def test_mcp_registered_tool_call():
    # Unpack the list of content items from the result wrapper
    content_list, _ = await mcp.call_tool("fetch_customer_ticket", {"ticket_id": 101})

    first_item = content_list[0]
    assert "Caio" in first_item.text
    assert "Enterprise" in first_item.text


@pytest.mark.asyncio
async def test_mcp_tool_not_found_response():
    content_list, _ = await mcp.call_tool("fetch_customer_ticket", {"ticket_id": 999})

    first_item = content_list[0]
    assert first_item.text == "Ticket #999 not found in database."