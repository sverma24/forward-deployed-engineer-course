"""F15 your turn, solved: the refund limit comes from a setting, not the code.
Run with REFUND_LIMIT=500 and two messages, $350 and $640."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "foundations"))
from claude_cli import ask_claude  # noqa: E402

REFUND_LIMIT = float(os.environ.get("REFUND_LIMIT", "200"))
SCHEMA = {"type": "object", "properties": {"topic": {"type": "string", "enum": ["billing", "outage", "other"]},
                                           "amount": {"type": ["number", "null"]}}, "required": ["topic", "amount"]}

print(f"refund limit: ${REFUND_LIMIT:.0f}")
for msg in ["I was charged $350 twice this month. Refund one please.",
            "I was charged $640 twice this month. Refund one of them NOW please."]:
    facts = ask_claude(f"Extract the facts from this message.\n\n{msg}", schema=SCHEMA)
    route = "a human" if facts["topic"] == "billing" and (facts["amount"] or 0) > REFUND_LIMIT else "the auto-refund queue"
    print(f"{facts} -> {route}")
