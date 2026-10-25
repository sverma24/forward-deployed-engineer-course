"""Read-only access to the cleaned client data (chapter C8).

The model never writes SQL. It can only call these few functions, every query
uses ? placeholders, and the connection itself is opened read-only, so even a
bug in our code can't change the client's data.
"""

import sqlite3

from .config import DB_PATH


def connect():
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)


def find_account(account_no):
    acc = str(account_no).strip().lstrip("0")
    with connect() as db:
        row = db.execute(
            "SELECT a.account_no, a.name, a.area_code, ar.area_name, a.priority "
            "FROM accounts a LEFT JOIN areas ar ON ar.area_code = a.area_code "
            "WHERE a.account_no = ?", (acc,)).fetchone()
    if not row:
        return None
    keys = ("account_no", "name", "area_code", "area_name", "priority")
    return dict(zip(keys, row))


def open_outage(area_code):
    with connect() as db:
        row = db.execute(
            "SELECT outage_id, started_at, restore_eta, cause, crew_id FROM outages "
            "WHERE area_code = ? AND status = 'open' ORDER BY started_at DESC LIMIT 1",
            (area_code,)).fetchone()
    if not row:
        return None
    return dict(zip(("outage_id", "started_at", "restore_eta", "cause", "crew_id"), row))


def recent_outages(area_code, limit=5):
    with connect() as db:
        rows = db.execute(
            "SELECT outage_id, started_at, restore_eta, cause, status FROM outages "
            "WHERE area_code = ? ORDER BY started_at DESC LIMIT ?", (area_code, limit)).fetchall()
    return [dict(zip(("outage_id", "started_at", "restore_eta", "cause", "status"), r)) for r in rows]
