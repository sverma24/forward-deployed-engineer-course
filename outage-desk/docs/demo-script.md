# Demo day script: 15 minutes with Rachel, Daniel, Maria and the ops director

1. **The problem, in their words (1 min).** "On Tuesday's storm, a restore-time call took about seven minutes, and a third of callers called back."
2. **Live demo, the happy path (3 min).** Account 4471 → 7:45 PM, with sources. Point at "updated 5:54 PM" and say why that matters (the old screens showed 8:30).
3. **Live demo, the hard cases (4 min).** A medical-priority customer (callback queued, Maria approves on screen). A message that tries to instruct the AI (ignored). Grid service switched off (says so, gives the log time).
4. **The numbers (3 min).** Eval score on 30 real questions, and pilot results against the baseline. Say plainly what isn't proven yet.
5. **"Why isn't it 100%?" (2 min).** Prepared answer: "On our 30 test questions, the version on your server gets 23 right, and Claude gets 29 or 30, which is why we've recommended a larger model for full rollout. Code makes sure no restore time is ever invented, and every answer shows its sources, so an agent can check in seconds. When live data is missing, it says so instead of guessing. The remaining risk is a wrong estimate from the field, which no software can fix, so we're also reporting how often crews' estimates change."
6. **What's next, and what we need from you (2 min).** Phase 2 text-message bot; a decision on rollout to all 60 agents.
