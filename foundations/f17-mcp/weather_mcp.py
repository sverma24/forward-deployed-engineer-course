"""F17: a tiny MCP server. Any MCP client, like Claude Code, can discover and use its tool.

Try it with Claude Code (from the repo root):
  claude -p "Is it raining in London right now?" --mcp-config foundations/f17-mcp/mcp.json --allowedTools mcp__weather__get_station
"""

from mcp.server.mcpserver import MCPServer

STATIONS = {
    "sydney": {"city": "Sydney", "temperature_c": 24, "raining": False, "wind_kmh": 9},
    "london": {"city": "London", "temperature_c": 11, "raining": True, "wind_kmh": 22},
    "seattle": {"city": "Seattle", "temperature_c": 9, "raining": True, "wind_kmh": 14},
}

server = MCPServer("weather")


@server.tool()
def get_station(city: str) -> dict:
    """Current temperature (Celsius), rain and wind for one city: Sydney, London or Seattle."""
    return STATIONS.get(city.lower(), {"error": f"no station called {city}"})


if __name__ == "__main__":
    server.run()
