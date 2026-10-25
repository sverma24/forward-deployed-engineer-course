"""The grid status service as an MCP server (chapter C11).

Any MCP client, such as Claude Code, can now check live outage status and
raise crew tickets through the same careful client our app uses, with its
retries, backoff and idempotency built in.

Register it with Claude Code from the outage-desk folder:
  claude mcp add larkfield-grid -- uv run python -m outage_desk.mcp_server
"""

from mcp.server.mcpserver import MCPServer

from .grid import GridClient, GridUnavailable

server = MCPServer("larkfield-grid")
grid = GridClient()


@server.tool()
def area_status(area_code: str) -> dict:
    """Live outage status for one area code, such as S-07: state, crew,
    restore estimate and when it was last updated."""
    try:
        return grid.area_status(area_code.upper())
    except GridUnavailable as e:
        return {"error": str(e), "retryable": True}


@server.tool()
def create_crew_ticket(area_code: str, note: str, request_id: str) -> dict:
    """Ask for a field crew in an area. request_id must be unique per real
    request; sending the same request_id twice never creates two tickets."""
    try:
        return grid.create_crew_ticket(area_code.upper(), note, idempotency_key=request_id)
    except GridUnavailable as e:
        return {"error": str(e), "retryable": True}


if __name__ == "__main__":
    server.run()
