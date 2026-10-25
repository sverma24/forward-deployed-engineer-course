"""F16: retrieval-augmented generation (RAG) in about forty lines.

1. Index: put each document into SQLite's full-text search.
2. Retrieve: find the documents that best match the question.
3. Generate: give only those documents to the model, and ask it to answer from them and cite them.

Run:  uv run python foundations/f16-rag/ask_handbook.py "How much can I spend on meals when travelling?"
"""

import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claude_cli import ask_claude  # noqa: E402

docs = {p.name: p.read_text() for p in sorted((Path(__file__).parent / "handbook").glob("*.txt"))}
db = sqlite3.connect(":memory:")
db.execute("CREATE VIRTUAL TABLE docs USING fts5(name, text, tokenize='porter')")
db.executemany("INSERT INTO docs VALUES (?, ?)", docs.items())

question = " ".join(sys.argv[1:]) or "How much can I spend on meals when travelling?"
words = " OR ".join(re.findall(r"[a-z0-9]+", question.lower()))
hits = db.execute("SELECT name FROM docs WHERE docs MATCH ? ORDER BY bm25(docs) LIMIT 2", (words,)).fetchall()
found = [h[0] for h in hits]
print("Question:", question)
print("Retrieved:", ", ".join(found))

context = "\n\n".join(f"[{name}]\n{docs[name]}" for name in found)
print("Answer:", ask_claude(f"{context}\n\nQuestion: {question}",
                            system="Answer only from the documents given, in one or two sentences, "
                                   "and name the document in square brackets. If they don't say, reply: I don't know."))
