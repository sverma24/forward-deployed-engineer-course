"""F11 your turn, solved: ground answers in a document, and check the model says "I don't know"
when the document doesn't cover the question."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "foundations"))
from claude_cli import ask_claude  # noqa: E402

DOC = ("Elm Street Library rules (fictional). Members may borrow up to 8 books at a time for 21 days. "
       "Each book can be renewed twice online. Late returns cost 25 cents a day per book, up to 5 dollars.")
SYSTEM = "Answer only from the document. If the document doesn't say, reply: I don't know."

for q in ["How many books can I borrow at once?", "What's the late fee for a book that's 30 days late?",
          "Can I bring my dog into the library?"]:
    print(f"Q: {q}\nA: {ask_claude(f'Document:{chr(10)}{DOC}{chr(10)}{chr(10)}Question: {q}', system=SYSTEM)}\n")
