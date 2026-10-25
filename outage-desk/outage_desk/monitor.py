"""After launch: what the trace log says about the last N answers (chapter C23).

Every answer the agent gives is written to data/traces.jsonl. This turns that file
into the handful of numbers an ops team actually watches, plus simple alerts.

Run:  uv run python -m outage_desk.monitor
"""

import json
from collections import Counter

from .config import TRACE_LOG

# Alert when these are crossed. Agree the numbers with the client in the runbook.
SLOW_SECONDS = 30          # an agent waiting longer than this will give up and click through screens
FALLBACK_RATE = 0.2        # more than 1 in 5 answers without live grid data means the grid service is in trouble


def load():
    if not TRACE_LOG.exists():
        return []
    return [json.loads(line) for line in TRACE_LOG.read_text().splitlines() if line.strip()]


def pct(values, p):
    values = sorted(values)
    return values[min(len(values) - 1, int(len(values) * p))] if values else 0


def main():
    traces = load()
    if not traces:
        print("No traces yet.")
        return
    secs = [t["seconds"] for t in traces]
    fallbacks = sum(1 for t in traces if t.get("live_errors"))
    unanswered = sum(1 for t in traces if not t.get("sources"))
    tools = Counter(tool for t in traces for tool in t.get("tools", []))

    print(f"Answers:            {len(traces)}")
    print(f"Time per answer:    median {pct(secs, .5):.1f} s · 95th percentile {pct(secs, .95):.1f} s · slowest {max(secs):.1f} s")
    print(f"Live grid missing:  {fallbacks} ({fallbacks / len(traces):.0%}) answers fell back to the outage log")
    print(f"No sources:         {unanswered} answers had no source at all")
    print(f"Tools used:         " + ", ".join(f"{k} {v}" for k, v in tools.most_common()))

    alerts = []
    if pct(secs, .95) > SLOW_SECONDS:
        alerts.append(f"SLOW: 1 in 20 answers takes over {pct(secs, .95):.0f} s (limit {SLOW_SECONDS} s)")
    if fallbacks / len(traces) > FALLBACK_RATE:
        alerts.append(f"GRID: {fallbacks / len(traces):.0%} of answers had no live data (limit {FALLBACK_RATE:.0%})")
    if unanswered:
        alerts.append(f"QUALITY: {unanswered} answers with no source; read them")
    print("\n" + ("\n".join("ALERT " + a for a in alerts) if alerts else "No alerts."))


if __name__ == "__main__":
    main()
