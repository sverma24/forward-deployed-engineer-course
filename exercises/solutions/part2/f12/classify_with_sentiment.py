"""F12 your turn, solved: add a sentiment field with fixed values to the schema."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "foundations"))
from claude_cli import ask_claude  # noqa: E402

SCHEMA = {"type": "object", "properties": {
    "category": {"type": "string", "enum": ["billing", "outage", "account", "other"]},
    "urgency": {"type": "string", "enum": ["low", "medium", "high"]},
    "sentiment": {"type": "string", "enum": ["calm", "frustrated", "angry"]}},
    "required": ["category", "urgency", "sentiment"]}

for c in ["I've been charged twice for my March bill and nobody answers the phone. Sort it out!",
          "Hi, could you tell me how to update my email address? Thanks.",
          "Power's been off for six hours and the website says nothing. Unacceptable."]:
    print(json.dumps(ask_claude(f"Classify this customer complaint.\n\nComplaint: {c}", schema=SCHEMA)), "<-", c[:45])
