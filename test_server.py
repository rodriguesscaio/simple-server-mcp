import copy

import pytest

import server as server_module
from server import create_ticket, fetch_customer_ticket, mcp, update_status

_SEED_DB = copy.deepcopy(server_module._ticket_db)


@pytest.fixture(autouse=True)
def reset_ticket_db():
    server_module._ticket_db.clear()
    server_module._ticket_db.update(copy.deepcopy(_SEED_DB))
    yield


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


def test_create_ticket_adds_new_entry():
    result = create_ticket(user="Ana", issue="Cannot reset password", tier="Free")
    assert "TICKET #103 Created" in result
    assert "User: Ana" in result
    assert "Status: open" in result
    assert "User: Ana" in fetch_customer_ticket(103)


def test_update_status_success():
    result = update_status(101, "resolved")
    assert "TICKET #101 Updated" in result
    assert "Status: resolved" in fetch_customer_ticket(101)


def test_update_status_invalid_status():
    result = update_status(101, "not_a_status")
    assert "Invalid status" in result


def test_update_status_ticket_not_found():
    result = update_status(999, "resolved")
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


@pytest.mark.asyncio
async def test_mcp_create_ticket_tool_call():
    content_list, _ = await mcp.call_tool(
        "create_ticket", {"user": "Ana", "issue": "Cannot reset password", "tier": "Free"}
    )

    first_item = content_list[0]
    assert "TICKET #103 Created" in first_item.text
    assert "User: Ana" in first_item.text


@pytest.mark.asyncio
async def test_mcp_update_status_tool_call():
    content_list, _ = await mcp.call_tool("update_status", {"ticket_id": 101, "status": "resolved"})

    first_item = content_list[0]
    assert "Status: resolved" in first_item.text
