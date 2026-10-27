# Handover pack: Outage Desk

**To:** Daniel Thomas (IT, owner from today) · Maria Lopez (call center, day-to-day lead)
**From:** FDE

## What you're getting
| Item | Where |
|---|---|
| The code, with tests and evals | this repo (`outage-desk/`) |
| How to run, check and fix it | `docs/runbook.md` |
| Why it's built this way | `docs/decisions.md`, `docs/architecture.md` |
| How to roll back | `docs/rollback-plan.md` |
| What it achieved | `docs/impact-report.md` |
| Open requests | `docs/change-request-001.md` (text-message bot) |

## Who does what from now on
| Task | Who | How often |
|---|---|---|
| Daily monitor + 20-answer spot check | Maria's team lead | daily, 5 min |
| Add any wrong answer to the eval set | Maria's team lead, with IT | as found |
| Update policies index when a PDF changes | IT | when policies change |
| Re-run evals before any change goes live | IT | every change |

## Training done
- 60-minute session for all agents: how to read the sources, what "live status unavailable" means, when to escalate
- 30-minute session for supervisors: the approvals queue
- 90-minute session for IT: runbook, evals, updating the policy index, and postmortem 001 (the week 3 incident)

## Known limits
- Restore times are only as good as crews' estimates.
- The local model is less accurate than the cloud model we developed with (see eval results), so answers always show sources.
- Area names must match the area list; new estates need adding to it.

## Fed back to our product team
- **Repeatable pattern:** "live system first, fall back to log, say which" is now a template (`templates/`).
- **Product gap:** the platform has no built-in approvals queue; every utility client will need one.
