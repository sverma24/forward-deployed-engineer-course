"""Clean and join the client's exports into one SQLite database (chapter C6).

Every fix is a rule you can read, and every guess we couldn't make ourselves
comes from data/client_fixes.csv, which records who at the client confirmed it.

Run:  uv run python -m outage_desk.clean
"""

import csv
import sqlite3
from datetime import datetime

from .config import DATA_DIR, DB_PATH, EST, HANDOVER

SCHEMA = """
CREATE TABLE accounts (
    account_no   TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    phone        TEXT,
    address      TEXT,
    area_code    TEXT,            -- NULL when the client doesn't know
    priority     TEXT             -- 'MEDICAL' or NULL
);
CREATE TABLE outages (
    outage_id    TEXT PRIMARY KEY,
    division     TEXT NOT NULL,   -- North or South
    area_code    TEXT NOT NULL,
    started_at   TEXT NOT NULL,   -- ISO 8601, Eastern time
    restore_eta  TEXT,            -- ISO 8601, NULL if unknown
    cause        TEXT,
    status       TEXT NOT NULL,   -- open or closed
    crew_id      TEXT
);
CREATE TABLE areas (
    area_code    TEXT PRIMARY KEY,
    area_name    TEXT NOT NULL,
    division     TEXT NOT NULL
);
CREATE TABLE crews (
    crew_id      TEXT PRIMARY KEY,
    crew_lead    TEXT,
    division     TEXT,
    shift        TEXT
);
CREATE INDEX outages_area ON outages(area_code, status);
"""


def read(name):
    with (HANDOVER / "data" / name).open() as f:
        return list(csv.DictReader(f))


def client_fixes():
    path = DATA_DIR / "client_fixes.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        return {(r["account_no"], r["field"]): r["value"] for r in csv.DictReader(f)}


def north_time(text):
    """North uses US style: 11/03/2026 01:00 PM."""
    if not text:
        return None
    return datetime.strptime(text, "%m/%d/%Y %I:%M %p").replace(tzinfo=EST).isoformat()


def south_time(text):
    """South already uses ISO 8601 with a time zone."""
    return datetime.fromisoformat(text).isoformat() if text else None


def clean_accounts(rows, fixes):
    merged = {}
    for r in rows:
        acc = r["account_no"].strip().lstrip("0")          # 04471 and 4471 are one account
        name = r["customer_name"].strip().title()          # ASHA... and Asha... are one person
        rec = {"account_no": acc, "name": name, "phone": r["phone"] or None,
               "address": r["address"] or None, "area_code": r["area_code"] or None,
               "priority": r["priority"] or None}
        old = merged.get(acc)
        if old:
            # Keep whatever is filled in; a real conflict is settled by client_fixes.csv.
            for k, v in rec.items():
                if old[k] is None:
                    old[k] = v
        else:
            merged[acc] = rec
    for (acc, field), value in fixes.items():
        if acc in merged:
            merged[acc][field] = value or None
    return list(merged.values())


def clean_outages(north, south):
    out, areas = {}, {}
    for r in north:
        code, name = r["Area"].split(" ", 1)
        areas[code] = (name, "North")
        out[r["OutageID"]] = (r["OutageID"], "North", code, north_time(r["Start"]),
                              north_time(r["Est_Restore"]), r["Cause"],
                              "open" if r["Status"] == "Open" else "closed", r["Crew"] or None)
    for r in south:
        # The same ticket typed in twice collapses here, because the ID is the key.
        out[r["ticket_no"]] = (r["ticket_no"], "South", r["feeder_area"], south_time(r["began_at"]),
                               south_time(r["restore_eta"]), r["reason"].capitalize(),
                               "open" if r["state"] == "ACTIVE" else "closed", r["crew_id"] or None)
    return list(out.values()), areas


SOUTH_NAMES = {"S-02": "Station Hill", "S-05": "Depot Lane", "S-07": "Riverside",
               "S-09": "College Park", "S-12": "Harbor Industrial", "S-15": "Elm Valley"}


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)

    accounts = clean_accounts(read("accounts.csv"), client_fixes())
    db.executemany("INSERT INTO accounts VALUES (:account_no, :name, :phone, :address, :area_code, :priority)",
                   accounts)
    outages, areas = clean_outages(read("north_outages.csv"), read("south_outages.csv"))
    db.executemany("INSERT INTO outages VALUES (?, ?, ?, ?, ?, ?, ?, ?)", outages)
    # South's export only has codes, so the names come from the client's area list.
    for code, name in SOUTH_NAMES.items():
        areas[code] = (name, "South")
    db.executemany("INSERT INTO areas VALUES (?, ?, ?)", [(c, n, d) for c, (n, d) in areas.items()])
    db.executemany("INSERT INTO crews VALUES (:crew_id, :crew_lead, :division, :shift)", read("crew_roster.csv"))
    db.commit()

    for table in ("accounts", "outages", "areas", "crews"):
        n = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table:9} {n:4} rows")
    print(f"open outages: {db.execute('SELECT COUNT(*) FROM outages WHERE status = ?', ('open',)).fetchone()[0]}")
    db.close()


if __name__ == "__main__":
    main()
