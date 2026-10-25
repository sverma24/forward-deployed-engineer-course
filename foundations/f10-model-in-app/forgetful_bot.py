"""F10: the model remembers nothing between calls. Watch what happens when the app
sends only the newest message, then when it sends the whole conversation.

Run:  uv run python foundations/f10-model-in-app/forgetful_bot.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claude_cli import ask_claude  # noqa: E402

SYSTEM = "You are a support assistant for an online shop. Reply in one short sentence."
messages = ["Hi, my order number is 58213 and it hasn't arrived.",
            "Can you remind me what my order number was?"]

print("=== Version 1: send only the newest message ===")
for m in messages:
    print("Customer:", m)
    print("Bot:     ", ask_claude(m, system=SYSTEM))

print("\n=== Version 2: send the whole conversation every time ===")
history = ""
for m in messages:
    history += f"Customer: {m}\n"
    reply = ask_claude(history + "Bot:", system=SYSTEM)
    history += f"Bot: {reply}\n"
    print("Customer:", m)
    print("Bot:     ", reply)
