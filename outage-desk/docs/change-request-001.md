# Change request 001: text-message bot for customers

**Asked by:** Rachel Morgan, Thursday of week 2 ("the board loved the demo, can customers get this by text message too, by Friday?")
**Status:** proposed for phase 2 · **Decision needed from:** Rachel Morgan

## What's being asked
Customers text a number and get the same answer the agents get: when their power will be back.

## What it would take
| Work | Estimate | Why |
|---|---|---|
| Choose and set up a text-message provider | 3–5 days | Larkfield's IT and legal must approve a new vendor, because customer phone numbers go to them |
| Confirm who is texting (account + postcode check) | 2 days | Without it, anyone can ask about anyone's account |
| Rewrite answers for customers, not agents | 1 day | Agents see sources and internal notes; customers must not |
| Rate limits and abuse protection | 1 day | A public number gets spam |
| Eval set for customer questions + a pilot | 3 days | Customer questions are worded differently; we can't assume the agent eval covers them |

**Total: about 2–3 weeks**, mostly approvals and safety, not code.

## Impact on phase 1 if we do it now
Phase 1's pilot with five agents moves back by about two weeks, and the storm season is already under way.

## Recommendation
Finish phase 1 first, since it already reduces call time. Start the text-message bot as phase 2 on the same engine, once the pilot numbers are in. **A version by Friday isn't safe:** there'd be no identity check and no customer eval.
