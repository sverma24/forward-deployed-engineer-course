"""F15: the same job done two ways.

Workflow: our code decides the steps. The model only does the one thing it's good at (reading text).
Agent: the model decides the steps itself.

Run:  uv run python foundations/f15-workflow-vs-agent/triage.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claude_cli import ask_claude  # noqa: E402

MESSAGE = "I was charged $640 twice this month. Refund one of them NOW please."
REFUND_LIMIT = 200   # a business rule: refunds above this always go to a human

print("=== Workflow: fixed steps in code ===")
step1 = ask_claude(f"Extract the facts from this message.\n\n{MESSAGE}", schema={
    "type": "object", "properties": {"topic": {"type": "string", "enum": ["billing", "outage", "other"]},
                                     "amount": {"type": ["number", "null"]}},
    "required": ["topic", "amount"]})
print("1. model reads the message ->", step1)
if step1["topic"] == "billing" and (step1["amount"] or 0) > REFUND_LIMIT:
    print(f"2. code applies the rule: ${step1['amount']} is over ${REFUND_LIMIT}, so it goes to a human. Always.")
else:
    print("2. code applies the rule: small amount, auto-refund queue")

print("\n=== Agent: the model decides ===")
plan = ask_claude(
    f"You can: refund_payment(amount), escalate_to_human(reason), reply(text). "
    f"Company rule: refunds above ${REFUND_LIMIT} need a human.\n"
    f"Decide what to do with this message and list the actions you'd take, in order.\n\n{MESSAGE}",
    schema={"type": "object", "properties": {"actions": {"type": "array", "items": {"type": "string"}}},
            "required": ["actions"]})
for i, a in enumerate(plan["actions"], 1):
    print(f"{i}. {a}")
print("\nThe agent probably followed the rule this time. The workflow follows it every time, because it's code.")
