# Discovery Note: Larkfield Power

## The problem as stated
Larkfield wants a website chatbot so customers can check outage information themselves and stop flooding the phone lines during storms.

## The problem underneath
The lines jam because each "when will my power come back?" call takes six to seven minutes on a storm day. Agents click between screens while the customer waits. Restore times are also often stale, because crew updates take about an hour to appear. Customers then call back and get a different answer.

## Who is affected
- **Customers:** On last Tuesday's storm, about 4,000 calls were waiting by 6pm. Hold times reached 40 minutes, and some people called back three or four times.
- **Call center agents:** Each question needs three or four lookups across the customer system, two outage logs (North and South) and the grid status service. Sometimes they also call a crew supervisor.
- **Customers on medical equipment:** They get priority and a supervisor call.

## What success looks like
- Storm-day "when will it come back" calls drop from about 7 minutes to 3.
- Fewer repeat callers. Maria estimates roughly a third or more of Tuesday's calls were callbacks, but this isn't tracked, so there is no target yet.
- Agents get a current answer in a few seconds.
- A website bot can follow later, built on the same engine.

## Constraints
- Customer data stays on Larkfield's servers (regulator and security requirement).
- The grid status service is rate-limited and fails under load.
- Nothing is written back to Larkfield systems without human approval. That means no automatic compensation and no ticket closing.
- Medical-equipment customers must never be missed.

## Open questions
- What is the target for callbacks, and how will we measure them?
- How do we identify medical-equipment customers, and where is that data held?
- What are the grid service's rate limits?
- Can the North and South logs be read together?
- How will the board be told that the project has moved from a "chatbot" to an agent-facing tool first?
