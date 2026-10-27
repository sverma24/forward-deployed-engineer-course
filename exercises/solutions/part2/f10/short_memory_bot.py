"""F10 your turn, solved: send only the last two messages. Watch what gets forgotten."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "foundations"))
from claude_cli import ask_claude  # noqa: E402

SYSTEM = "You are a support assistant for an online shop. Reply in one short sentence."
messages = ["Hi, my order number is 58213 and it hasn't arrived.",
            "Also, do you sell gift cards?",
            "And what are your opening hours?",
            "Can you remind me what my order number was?"]

history = []
for m in messages:
    history.append(f"Customer: {m}")
    window = history[-2:]                       # only the last two lines go on the desk
    reply = ask_claude("\n".join(window) + "\nBot:", system=SYSTEM)
    history.append(f"Bot: {reply}")
    print("Customer:", m)
    print("Bot:     ", reply)
