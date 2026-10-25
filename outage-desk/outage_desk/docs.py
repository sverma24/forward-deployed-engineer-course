"""Search over the client's policy PDFs (chapter C10).

No vector database: SQLite's built-in full-text search (FTS5) indexes one row
per PDF page, and every hit carries the file name and page number, so the
answer can cite exactly where it came from.

Build the index:  uv run python -m outage_desk.docs build
Try a search:     uv run python -m outage_desk.docs "compensation planned maintenance"
"""

import re
import sqlite3
import sys

from pypdf import PdfReader

from .config import DATA_DIR, DOCS_DB, HANDOVER


def build():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DOCS_DB.exists():
        DOCS_DB.unlink()
    db = sqlite3.connect(DOCS_DB)
    db.execute("CREATE VIRTUAL TABLE pages USING fts5(doc, page UNINDEXED, text, tokenize='porter')")
    n = 0
    for pdf in sorted((HANDOVER / "policies").glob("*.pdf")):
        for i, page in enumerate(PdfReader(pdf).pages, start=1):
            text = " ".join(page.extract_text().split())
            text = text.replace("Larkfield Power Co. (fictional)", "").strip()
            db.execute("INSERT INTO pages VALUES (?, ?, ?)", (pdf.name, i, text))
            n += 1
    db.commit()
    print(f"indexed {n} pages")


def search(query, limit=3):
    # Keep only plain words, so user text can't break the FTS query syntax.
    words = re.findall(r"[a-zA-Z0-9]+", query.lower())
    if not words:
        return []
    match = " OR ".join(words)
    with sqlite3.connect(DOCS_DB) as db:
        rows = db.execute("SELECT doc, page, text, bm25(pages) FROM pages WHERE pages MATCH ? "
                          "ORDER BY bm25(pages) LIMIT ?", (match, limit)).fetchall()
    return [{"doc": d, "page": p, "text": t, "score": round(-s, 2)} for d, p, t, s in rows]


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        build()
    else:
        for hit in search(" ".join(sys.argv[1:])):
            print(f"{hit['doc']} p.{hit['page']} (score {hit['score']}): {hit['text'][:160]}...")
