"""F14 your turn, solved: a second tool, celsius_to_fahrenheit. The model chains both tools."""

import json
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "foundations"))
from claude_cli import ask_claude  # noqa: E402


def get_station(city):
    return httpx.get(f"http://localhost:8090/stations/{city.lower()}").json()


def celsius_to_fahrenheit(celsius):
    return {"fahrenheit": round(float(celsius) * 9 / 5 + 32, 1)}


TOOLS = {"get_station": get_station, "celsius_to_fahrenheit": celsius_to_fahrenheit}
SYSTEM = """You answer weather questions. You can't see live data yourself.
Tools: get_station(city) returns temperature (C), rain and wind for one city.
celsius_to_fahrenheit(celsius) converts a temperature. Don't do the conversion yourself.
Reply with JSON only: {"action": "call_tool", "tool": ..., "args": {...}} or {"action": "answer", "answer": ...}"""
SCHEMA = {"type": "object", "properties": {
    "action": {"type": "string", "enum": ["call_tool", "answer"]},
    "tool": {"type": "string"}, "args": {"type": "object"}, "answer": {"type": "string"}},
    "required": ["action"]}

transcript = "User: What's the temperature in London in Fahrenheit?"
for turn in range(1, 6):
    d = ask_claude(transcript, system=SYSTEM, schema=SCHEMA)
    if d["action"] == "answer":
        print(f"[turn {turn}] answer: {d['answer']}")
        break
    result = TOOLS[d["tool"]](**d["args"])
    print(f"[turn {turn}] {d['tool']}({d['args']}) -> {result}")
    transcript += f"\nTool call: {json.dumps(d)}\nTool result: {json.dumps(result)}"
