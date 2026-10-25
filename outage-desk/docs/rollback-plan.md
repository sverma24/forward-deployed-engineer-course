# Rollback plan: Outage Desk

**Rollback means:** agents go back to the old screens (customer system + two outage logs + grid service), exactly as before the pilot. Nothing in Larkfield's systems changes, because the desk only reads data and suggests actions, so rolling back has no data to undo.

## When we roll back (any one is enough)
- More than 1 in 20 answers wrong in the daily spot-check of 20 answers
- A wrong restore time reaches a customer and causes a complaint we can trace to the desk
- 95% of answers take longer than 60 s for more than 30 minutes
- Any sign of customer data leaving Larkfield's servers

## How (under 5 minutes)
1. Maria tells agents by the call center chat: "use the old screens".
2. IT stops the desk: `docker compose -f outage-desk/docker-compose.yml -p larkfield down`.
3. FDE writes up what happened within 24 h (see `postmortem-template.md`).

## Who can decide
Maria Lopez (call center), Daniel Thomas (IT), or the FDE. Any one of them, without waiting for the others.
