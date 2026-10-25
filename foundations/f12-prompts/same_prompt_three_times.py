"""F12: the same prompt, three times. Then the same task with a strict output shape (a schema).

Run:  uv run python foundations/f12-prompts/same_prompt_three_times.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claude_cli import ask_claude  # noqa: E402

COMPLAINT = "I've been charged twice for my March bill and nobody answers the phone. Sort it out!"
PROMPT = f"Classify this customer complaint and say how urgent it is.\n\nComplaint: {COMPLAINT}"

print("=== Free text, three runs ===")
for i in range(1, 4):
    print(f"\nRun {i}:\n{ask_claude(PROMPT)}")

SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": ["billing", "outage", "account", "other"]},
        "urgency": {"type": "string", "enum": ["low", "medium", "high"]},
        "summary": {"type": "string"},
    },
    "required": ["category", "urgency", "summary"],
}
print("\n=== With a schema, three runs ===")
for i in range(1, 4):
    print(f"Run {i}:", json.dumps(ask_claude(PROMPT, schema=SCHEMA)))
