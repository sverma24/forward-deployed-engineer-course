"""Profile the client's raw exports before touching them (course chapter C5).

It changes nothing. It only reports what's wrong, so the findings can go back
to the client as questions.

Run:  uv run python -m outage_desk.audit > docs/data-quality-report.md
"""

import csv
import re
from collections import Counter

from .config import HANDOVER


def read(name):
    with (HANDOVER / "data" / name).open() as f:
        return list(csv.DictReader(f))


def main():
    accounts = read("accounts.csv")
    north = read("north_outages.csv")
    south = read("south_outages.csv")
    out = ["# Data-quality report: Larkfield Power exports", ""]

    out += ["## accounts.csv", f"- {len(accounts)} rows"]
    zeros = [a["account_no"] for a in accounts if a["account_no"].startswith("0")]
    out.append(f"- {len(zeros)} account numbers start with a leading zero: {', '.join(zeros)}")
    key = Counter(a["account_no"].lstrip("0") for a in accounts)
    dups = sorted(k for k, n in key.items() if n > 1)
    out.append(f"- {len(dups)} accounts appear more than once: {', '.join(dups)}")
    for k in dups:
        areas = {a["area_code"] for a in accounts if a["account_no"].lstrip("0") == k}
        if len(areas - {""}) > 1:
            out.append(f"  - **{k} is listed in different areas: {', '.join(sorted(areas))}. Ask the client which is right.**")
    blank = [a["account_no"] for a in accounts if not a["area_code"]]
    out.append(f"- {len(blank)} accounts have no area: {', '.join(blank)}")
    out.append("")

    out += ["## north_outages.csv vs south_outages.csv",
            f"- North: {len(north)} rows, columns {list(north[0])}",
            f"- South: {len(south)} rows, columns {list(south[0])}",
            f"- North dates look like `{north[0]['Start']}` (month first, 12-hour clock)",
            f"- South dates look like `{south[0]['began_at']}` (ISO, with time zone)",
            f"- North status words: {sorted({r['Status'] for r in north})}; "
            f"South status words: {sorted({r['state'] for r in south})}",
            f"- North keeps the area code and name in one column, e.g. `{north[0]['Area']}`"]
    tickets = Counter(r["ticket_no"] for r in south)
    twice = [t for t, n in tickets.items() if n > 1]
    out.append(f"- South tickets entered more than once: {', '.join(twice) or 'none'}")
    no_end = [r["ticket_no"] for r in south if r["state"] == "RESOLVED" and not r["restore_eta"]]
    no_end += [r["OutageID"] for r in north if r["Status"] == "Closed" and not r["Est_Restore"]]
    out.append(f"- Closed outages with no end time: {', '.join(no_end) or 'none'}")
    open_no_eta = [r["ticket_no"] for r in south if r["state"] == "ACTIVE" and not r["restore_eta"]]
    open_no_eta += [r["OutageID"] for r in north if r["Status"] == "Open" and not r["Est_Restore"]]
    out.append(f"- Open outages with no restore estimate yet: {', '.join(open_no_eta) or 'none'}")
    out.append("")

    complaints = read("complaints.csv")
    phones = sum(1 for c in complaints if re.search(r"\(\d{3}\) \d{3}-\d{4}", c["text"]))
    out += ["## complaints.csv",
            f"- {len(complaints)} complaints; {phones} have a phone number typed into the text (personal data)",
            "- At least one complaint contains instructions aimed at an AI system. Treat all complaint text as untrusted.",
            ""]
    out += ["## Questions for the client",
            "1. Account 4471 appears in two areas. Which one is current?",
            "2. Should accounts with no area be fixed at the source, or looked up by address?",
            "3. Is the grid status service or the outage log the source of truth for restore times?"]
    print("\n".join(out))


if __name__ == "__main__":
    main()
