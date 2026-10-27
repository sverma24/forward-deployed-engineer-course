"""Check the model's times against the data (chapter C21).

A smaller model sometimes writes a restore time that isn't in any tool result,
like "8:45 PM" when the data says 7:45. A wrong time is the one mistake this
system must never make, so code checks every clock time in the answer. If one
isn't in the data, the answer is replaced with one built from the data by code.
"""

import re
from datetime import datetime

CLOCK = re.compile(r"\b(\d{1,2}):(\d{2})\s*([ap])?\.?m?\.?", re.IGNORECASE)
ISO = re.compile(r"\d{4}-\d{2}-\d{2}T(\d{2}):(\d{2})")


def _hm(hour, minute):
    return f"{int(hour) % 12 or 12}:{minute}"


def times_in_answer(text):
    return {_hm(h, m) for h, m, _ in CLOCK.findall(text)}


def times_in_data(steps):
    found = set()
    for s in steps:
        for r in s.get("results", []):
            found |= {_hm(h, m) for h, m in ISO.findall(str(r["result"]))}
    return found


def _clock(iso):
    return datetime.fromisoformat(iso).strftime("%-I:%M %p")


def answer_from_data(steps):
    """The restore time, written by code from the last outage lookup."""
    for s in reversed(steps):
        for r in s.get("results", []):
            if r["tool"] != "get_outage_status" or not isinstance(r["result"], dict):
                continue
            out = r["result"]
            live, log = out.get("live_status"), out.get("outage_log")
            if live and live.get("restore_eta"):
                return (f"Area {out['area_code']}: power is expected back at {_clock(live['restore_eta'])} "
                        f"(live grid status, updated {_clock(live['updated_at'])}).")
            if live and live.get("state") == "normal" and not log:
                return f"Area {out['area_code']}: no outage on record, and the grid shows the area as normal."
            if log and log.get("restore_eta"):
                return (f"Area {out['area_code']}: last known estimate {_clock(log['restore_eta'])} "
                        f"from the outage log ({log['outage_id']}); live status unavailable.")
            if log:
                return f"Area {out['area_code']}: outage {log['outage_id']} is open, with no restore estimate yet."
    return None


def check(answer, steps, also_allowed=()):
    """Returns (answer to show, list of times that weren't in the data).
    also_allowed: other ISO times the answer may mention, like the current time."""
    known = times_in_data(steps) | {_hm(h, m) for t in also_allowed for h, m in ISO.findall(t)}
    unknown = sorted(times_in_answer(answer) - known)
    if not unknown:
        return answer, []
    replacement = answer_from_data(steps)
    if replacement:
        return replacement + " (Answer rebuilt from the data: the model's version had a time that isn't in any source.)", unknown
    return answer + f" WARNING: check this answer; {', '.join(unknown)} isn't in any source.", unknown
