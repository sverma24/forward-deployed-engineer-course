"""Human sign-off (chapter C15).

The agent can suggest a bill credit, a medical-priority callback or a crew
ticket, but only a supervisor can approve one. Suggestions wait here.
"""

import json
import sqlite3
import uuid

from .config import APPROVALS_DB, DATA_DIR, now

KINDS = {"bill_credit", "priority_callback", "crew_ticket"}


def _db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(APPROVALS_DB)
    db.execute("CREATE TABLE IF NOT EXISTS approvals (id TEXT PRIMARY KEY, kind TEXT, account_no TEXT, "
               "reason TEXT, details TEXT, status TEXT, created_at TEXT, decided_by TEXT, decided_at TEXT)")
    return db


def propose(kind, account_no, reason, details=None):
    if kind not in KINDS:
        raise ValueError(f"unknown action kind: {kind}")
    with _db() as db:
        # One open suggestion per account and kind, however many times the agent asks.
        row = db.execute("SELECT id FROM approvals WHERE kind = ? AND account_no = ? AND status = 'pending'",
                         (kind, account_no)).fetchone()
        if row:
            return {"id": row[0], "status": "pending", "note": "already waiting for a supervisor"}
        aid = uuid.uuid4().hex[:8]
        db.execute("INSERT INTO approvals VALUES (?, ?, ?, ?, ?, 'pending', ?, NULL, NULL)",
                   (aid, kind, account_no, reason, json.dumps(details or {}), now().isoformat()))
    return {"id": aid, "status": "pending", "note": "a supervisor must approve this"}


def pending():
    with _db() as db:
        rows = db.execute("SELECT id, kind, account_no, reason, created_at FROM approvals "
                          "WHERE status = 'pending' ORDER BY created_at").fetchall()
    return [dict(zip(("id", "kind", "account_no", "reason", "created_at"), r)) for r in rows]


def decide(aid, approve, supervisor):
    with _db() as db:
        n = db.execute("UPDATE approvals SET status = ?, decided_by = ?, decided_at = ? "
                       "WHERE id = ? AND status = 'pending'",
                       ("approved" if approve else "rejected", supervisor, now().isoformat(), aid)).rowcount
    return n == 1
