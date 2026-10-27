"""F17 your turn, solved: a second tool, list_stations, so the AI can find out which cities exist.

Try it with Claude Code (from the repo root):
  claude -p "Is it raining in London right now?" --mcp-config exercises/solutions/part2/f17/mcp.json --allowedTools mcp__weather__get_station
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


@server.tool()
def list_stations() -> list[str]:
    """The cities this weather service has stations for."""
    return sorted(s["city"] for s in STATIONS.values())


if __name__ == "__main__":
    server.run()
