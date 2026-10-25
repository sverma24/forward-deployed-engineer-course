# Scope: Outage Desk, phase 1

**Client:** Larkfield Power (fictional) · **Owner:** FDE · **Approved by:** Rachel Morgan (Customer Operations)

## The goal, in one sentence
Storm-day "when will my power come back?" calls take three minutes instead of seven, and fewer customers call back with the same question.

## How we break it down
| # | Piece | Why it matters | Value | Risk | Order |
|---|---|---|---|---|---|
| 1 | Measure today's repeat calls and call length (baseline) | Without it we can't prove anything | High | Low | **First** |
| 2 | One clean, joined copy of accounts and both outage logs | Every answer depends on it | High | Medium: messy data | 2 |
| 3 | Live restore time from the grid status service | Fixes the stale-time problem that causes repeat calls | High | High: rate limits, outages | 3 |
| 4 | An assistant that answers "when will power be back for account X?" with sources | The thing agents actually use | High | Medium | 4 |
| 5 | Policy answers (bill credits, planned maintenance) with page citations | The second most common question | Medium | Low | 5 |
| 6 | Medical-priority customers flagged on every answer, with a callback suggested | Safety requirement from Maria | High | Low | with 4 |
| 7 | Website chatbot for customers | Rachel's original idea | Medium | High: public, needs everything above first | **Phase 2** |

## The walking skeleton (week 1)
A thin version where every piece exists and connects: one account number in, one answer out, with its sources. Pieces 2–4 at their simplest, end to end, on real client data.

## Definition of done for phase 1
- [ ] On 30 real call-center questions, the assistant answers at least 27 correctly, with sources (eval set)
- [ ] It never gives a restore time without saying where it came from and when it was updated
- [ ] It never approves a bill credit or closes an outage: it can only suggest, and a supervisor decides
- [ ] It keeps working, and says so honestly, when the grid status service is down
- [ ] Customer data never leaves Larkfield's servers in the deployed version
- [ ] Five agents have used it during a pilot and signed off the test checklist
- [ ] Call length and repeat calls measured for two weeks after launch, compared with the baseline

## Out of scope (phase 1)
- The public website chatbot (phase 2, same engine)
- Changing how field crews update estimates (a process change for Larkfield's ops team; we'll report how often estimates are wrong)
- Writing anything back to Larkfield's systems
