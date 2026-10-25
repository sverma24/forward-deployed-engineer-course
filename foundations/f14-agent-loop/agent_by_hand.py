"""F14: an agent loop you can read in one screen.

The model can't call anything itself. Each turn it replies with JSON: either
"run this tool" or "here's my answer". Our code runs the tool, adds the result
to the conversation, and asks again.

Start the F2 weather API first, then:
  uv run python foundations/f14-agent-loop/agent_by_hand.py "Should I take an umbrella in Seattle or London today?"
"""

import json
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claude_cli import ask_claude  # noqa: E402


def get_station(city):
    r = httpx.get(f"http://localhost:8090/stations/{city.lower()}")
    return r.json()


TOOLS = {"get_station": get_station}
SYSTEM = """You answer weather questions. You can't see live data yourself.
Tool available: get_station(city) returns the current temperature, rain and wind for one city.
Reply with JSON only. To use the tool: {"action": "call_tool", "tool": "get_station", "args": {"city": "..."}}
To finish: {"action": "answer", "answer": "..."}"""
SCHEMA = {"type": "object", "properties": {
    "action": {"type": "string", "enum": ["call_tool", "answer"]},
    "tool": {"type": "string"}, "args": {"type": "object"}, "answer": {"type": "string"}},
    "required": ["action"]}

question = " ".join(sys.argv[1:]) or "Should I take an umbrella in Seattle or London today?"
transcript = f"User: {question}"
for turn in range(1, 6):
    decision = ask_claude(transcript, system=SYSTEM, schema=SCHEMA)
    if decision["action"] == "answer":
        print(f"[turn {turn}] model answers: {decision['answer']}")
        break
    result = TOOLS[decision["tool"]](**decision["args"])
    print(f"[turn {turn}] model asks for {decision['tool']}({decision['args']}) -> our code returns {result}")
    transcript += f"\nTool call: {json.dumps(decision)}\nTool result: {json.dumps(result)}"
