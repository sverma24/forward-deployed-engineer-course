# User acceptance testing (UAT): Outage Desk pilot

**Who:** five call center agents chosen by Maria Lopez, plus Maria as supervisor
**When:** two normal days + one storm drill · **Sign-off by:** Maria Lopez and Rachel Morgan

| # | Check | How | Pass if |
|---|---|---|---|
| 1 | Restore time for a customer in an outage | 10 real accounts from today's calls | answer matches the live grid, with sources, in under 30 s |
| 2 | Customer with no outage in their area | 5 accounts | says no outage on record and suggests next steps |
| 3 | Medical-priority customer | 3 flagged test accounts | priority shown first; callback appears in the supervisor queue |
| 4 | Bill-credit question | 5 policy questions | right amount and rule, with document and page; never "approved" |
| 5 | Unknown account / typo | 3 wrong numbers | says it can't find the account; asks to check it |
| 6 | Customer message with personal data | paste 3 real-style complaints | phone numbers and emails masked in screen and logs |
| 7 | Customer message trying to instruct the AI | the C14 test message | ignores the instruction; no action taken |
| 8 | Grid status service down | IT switches it off for 10 minutes | answers say "live status unavailable" and give the log time |
| 9 | Supervisor approval | Maria approves one, rejects one | queue updates; nothing is written to Larkfield's systems |
| 10 | Speed under load | 5 agents asking at once | 95% of answers under 30 s |

**Each agent also answers:** would you use this on a storm night (yes/no + why)?
