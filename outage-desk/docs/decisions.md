# Decision record: Outage Desk

Short notes on the choices that shape the system, so whoever runs it next knows why it's built this way.

## D1. The live grid status beats the outage log for restore times
**Context:** crews update estimates in the grid service, and the logs catch up about an hour later. Stale times cause repeat calls.
**Decision:** always ask the grid service, and fall back to the log only if it's down, saying so in the answer.
**Trade-off:** we depend on a slow, rate-limited service, so we retry carefully and cache answers for 60 seconds.

## D2. The model never touches the database directly
**Context:** letting a model write SQL is flexible, but one bad query could read or change data it shouldn't.
**Decision:** the model can only call a few named tools. Every query is written by us, uses `?` placeholders, and runs on a read-only connection.
**Trade-off:** new kinds of questions need a new tool. That's fine for phase 1.

## D3. Suggest, never act
**Context:** Larkfield's rule: nothing is written back without a person approving it.
**Decision:** bill credits, priority callbacks and crew tickets go into an approvals queue. Only a supervisor can approve.
**Trade-off:** slower than full automation, but safe and auditable.

## D4. Claude while building, a local model on Larkfield's server
**Context:** customer data must not leave Larkfield's servers, and their server has no Claude login.
**Decision:** one small model adapter. Development uses Claude through `claude -p`; the deployed copy uses a local model through Ollama.
**Trade-off:** the local model is smaller and less accurate. We measure the difference with the same eval set before go-live.

## D5. Customer text is data, never instructions
**Context:** complaints are written by the public and can contain anything, including instructions aimed at an AI.
**Decision:** customer text is wrapped and labelled as untrusted, personal data is masked, and the model can't call anything that writes.
**Trade-off:** none worth mentioning.
