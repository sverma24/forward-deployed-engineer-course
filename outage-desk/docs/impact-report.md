# Impact report: Outage Desk pilot (template with example numbers)

> **Larkfield Power is fictional, so these numbers are examples** that show how to build the report.
> On a real project, every number comes from the client's phone system and the desk's trace log, and the
> report says where each one came from.

## What we promised (from scope.md)
Storm-day "when will my power come back?" calls take 3 minutes instead of 7, and fewer customers call back.

## Before and after (example)
| Measure | Baseline: last 3 storms, old screens | Pilot: 2 storms, 5 agents with the desk | Source |
|---|---|---|---|
| Average call length, restore-time calls | 6 min 40 s | 3 min 10 s | phone system call logs |
| Repeat calls (same account within 2 h) | 34% | 19% | phone system, matched by account |
| Answers with a live restore time | not measured | 92% (8% fell back to the log) | desk trace log |
| Wrong restore times found in spot checks | not measured | 1 in 200 | daily spot-check sheet |

## What that's worth (example arithmetic, shown so the client can check it)
- 4,000 restore-time calls on a storm evening × 3.5 minutes saved = **233 agent-hours** per storm evening
- 15 points fewer repeat calls on 4,000 calls = **600 fewer calls** per storm evening
- At the client's loaded agent cost (they supply it, say $32 an hour): 233 × $32 ≈ **$7,500 per storm evening**

## What we can't claim
- Whether customers are happier: we didn't survey them, and that should be the next measure.
- Results for all 60 agents: the pilot had 5, picked by Maria; we expect some drop as it rolls out.
