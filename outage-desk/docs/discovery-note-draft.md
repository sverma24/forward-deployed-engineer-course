# Discovery Note: Larkfield Power

## The problem as stated
Customers keep calling during storms. Rachel asked for a website chatbot so customers can check for themselves instead of phoning.

## The problem underneath
Almost every storm call asks "When will my power come back?" Answering takes three or four lookups: the customer system, two separate outage logs (North and South), and the grid status service or a call to the crew supervisor. A storm-day call takes 6–7 minutes, mostly spent switching screens. Restore estimates also reach agent screens about an hour late. Customers are given stale times and call back. Maria estimates a third of calls or more are callbacks, but this isn't tracked.

The jam comes from slow, inconsistent lookups, not from a lack of self-service. A website bot can follow later on the same engine.

## Who is affected
- Customers, who face 40-minute holds and repeat calls
- Call center agents and Maria's team
- Rachel, who needs to explain the change to the board

## What success looks like
- Storm-day calls drop from about 7 minutes to 3
- Fewer callbacks (no target set yet)
- For scale, Tuesday had 400+ calls waiting at once and about 4,000 over the evening

## Constraints
- Customer data stays on Larkfield servers (regulator and security rule)
- The grid status service is rate-limited and fails under load
- Nothing is written back without human approval (no automatic compensation, no closing tickets)
- Medical-equipment customers get priority and a supervisor call, and none can be missed

## Open questions
- What callback reduction counts as success? What is the real baseline?
- How are medical-equipment customers flagged today, and in which system?
- What is the grid status service's rate limit?
- Can the North and South logs be queried together?
- How can crew estimate updates reach us faster than the current hour?
- What timeline or board milestone should we plan around?
