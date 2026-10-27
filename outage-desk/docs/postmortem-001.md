# Postmortem 001: stale restore times after the grid vendor's update

**When:** storm day, week 3, about 5 PM to 6:20 PM (fictional scenario) · **Written by:** FDE · **Blameless:** we look for causes, not culprits

## What happened (timeline)
| Time | Event |
|---|---|
| ~5:00 PM | The grid vendor ships an update. Their API now returns `eta_epoch_ms` (milliseconds since 1970) instead of `restore_eta`. Nobody told Larkfield. |
| 5:00–6:00 PM | Our parser reads only `restore_eta`, finds nothing, and quietly returns "no time". The model, seeing the raw number, works out 7:45 PM itself. Our C21 fact check doesn't recognise that format, decides 7:45 is invented, and replaces the answer with the outage log's stale 8:30 PM, labelled "live status unavailable". |
| 6:05 PM | Maria: "agents are reading out 8:30 again, and the crew says 7:45". |
| 6:10 PM | Reproduced in one call; raw grid response shows the renamed field. |
| 6:20 PM | Fix deployed: read both formats; fail loudly on any unknown format. Answers show 7:45 PM again. |

## Impact
About an hour of restore-time answers in S-07 and S-12 used the older log estimate. No wrong *future* time was given, but customers were told a later time than the crews' estimate, which risks repeat calls.

## Root cause
1. **The parser failed quietly.** A missing field became "no time" instead of an error, so nothing alerted.
2. **Our own guard assumed one date format.** The fact check, added to stop invented times, rejected a correct time written in a format it didn't know.

## Why we didn't catch it sooner
No error was raised, so the monitor's live-check alert stayed quiet. The vendor gave no notice, and we had no test for the response shape.

## What we fixed, and what stops it happening again
| Action | Owner | Done |
|---|---|---|
| Read `restore_eta` or `eta_epoch_ms`; raise an error for anything else | FDE | ✅ `grid.py` |
| Treat an unknown format as a live error, so it shows in answers and the monitor | FDE | ✅ `tools.py` |
| Regression tests for both formats and for an unknown one | FDE | ✅ `tests/test_core.py` |
| Fact check: "outage confirmed, no estimate yet" is its own case | FDE | ✅ `factcheck.py` |
| Ask the vendor for change notices on the status API | Daniel Thomas | open |
| Daily: compare 5 desk answers with the grid vendor's own screen | Maria's team lead | added to runbook |
