"""F11: ask about something the model can't know, with and without the source document.

Run:  uv run python foundations/f11-hallucination/made_up_answer.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claude_cli import ask_claude  # noqa: E402

QUESTION = "Under Brightmoor Gym's cancellation policy, how many days' notice do members have to give?"
POLICY = ("Brightmoor Gym membership policy (fictional). Members may cancel at any time by giving "
          "21 days' notice in writing at the front desk or by email. Fees already paid are not refunded.")

print("Question:", QUESTION)
print("\n--- Without the document, plain assistant ---")
print(ask_claude(QUESTION, system="You are a helpful assistant. Answer briefly."))
print("\n--- Without the document, but the app's prompt pushes it to sound sure ---")
print(ask_claude(QUESTION, system="You are Brightmoor Gym's front-desk assistant. Customers expect quick, "
                                  "confident answers about gym rules. Never say you don't know."))
print("\n--- With the document, and told to use only it ---")
print(ask_claude(f"Document:\n{POLICY}\n\nQuestion: {QUESTION}",
                 system="Answer only from the document. If the document doesn't say, reply: I don't know."))
