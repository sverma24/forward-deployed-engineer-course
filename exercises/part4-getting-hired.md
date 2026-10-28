# Part 4 exercises: getting hired

These are the exercises that get you the job, so do them for real: write them down, say the interview ones out loud, and time yourself.
The coding answers (J12, J13) are in `exercises/solutions/part4/`, with tests.

---

## J1 Your path in

**Your turn.** Write one line each: where you're starting, the stepping-stone role closest to FDE for you, and the first thing you'll build.

**Model answer (a support engineer).** "I'm in technical support. My stepping stone is solutions engineer or support engineer at an AI or data company, where I'd already be talking to customers about their systems. First build: the outage desk from this course, run on my own laptop."

---

## J2 A ninety-day plan

**Your turn.** Write your first week, day by day, in one line per day.

**Model answer.**
- Mon: install Python, uv, Git and Docker. Run F1 and F2.
- Tue: F3 and F4, and do both SQL exercises without looking.
- Wed: F5 to F7, and break a test on purpose, then fix it.
- Thu: F8 and F9. Push a repo with a `.env` that Git ignores.
- Fri: F10 to F12 with Claude Code.
- Sat: redo the hardest exercise of the week from memory.
- Sun: rest, and write three lines about what was hard.

---

## J3 A portfolio that reads like client work

**Your turn.** Write the first four lines of your project's README, the way a client report starts.

**Model answer.**
> **Outage Desk: restore times for a utility call center**
> **Problem:** on storm nights, agents checked three systems per call and customers called back because times were stale.
> **Result:** 30 of 30 real agent questions answered correctly with Claude; 23 of 30 with a small local model that keeps customer data on the client's server, guarded so it never invents a restore time.
> **What's here:** the code, the discovery note, the scope, decision records, the eval set and a postmortem.

---

## J4 Resume and LinkedIn

**Your turn.** Turn this duty into an impact bullet: *"Responsible for writing test cases for the billing module."*

**Model answer.** "Wrote 140 test cases for the billing module and caught a rounding bug that would have overcharged about 2% of invoices, before release." Use your own real numbers. If you don't have numbers, count something you did.

---

## J5 Finding roles, and getting replies

**Your turn.** Write a four-sentence message to an FDE at a company you like.

**Model answer.**
> Hi Sam, I read your post about deploying agents at hospitals, and the part about matching patient records across systems was exactly the problem I hit in my practice project.
> I built a small outage desk for a fictional utility: tools, evals, guardrails and an offline deploy (link).
> Would you be open to telling me, in a sentence or two, what your team looks for in a junior FDE?
> Thanks either way.

It's short, it's about them first, and it asks for something small.

---

## J6 Vet the role before you accept it

**Your turn.** Write three questions you'd ask the hiring manager, and what a worrying answer would sound like.

**Model answer.**
| Question | Worrying answer |
|---|---|
| "What did an FDE on this team ship in the last three months?" | "They supported a lot of deals." (Sounds like a sales role.) |
| "How much of the week is writing code?" | "Some, when there's time." |
| "How is an FDE's success measured?" | "Revenue closed." |

---

## J7 The interview loop

**Your turn.** List the rounds you expect, and next to each one, the one thing you'll practise this week.

**Model answer.** Recruiter screen: a two-minute story of why FDE. Coding: J12 and J13 again, timed. Decomposition: one mock out loud per day. System design: J14's order from memory. Customer and behavioral: two STAR stories. Values: why this company, in three sentences.

---

## J8 The decomposition round: a method

**Your turn.** Prompt: *"A city library wants more young people to use it."* Say your first three moves out loud, then write them down.

**Model answer.**
1. **Clarify:** "Which ages count as young, and what does 'use' mean: visits, loans, events, or the app? Is there a target, like 20% more visits by under-25s in a year?"
2. **People and numbers:** librarians, young people who don't come, schools and colleges nearby, and the budget owner. The measure is visits and loans by age, which the library system already records.
3. **Data and limits:** what the membership and loan data show by age, what privacy rules cover young members, and the budget.

---

## J9 Mock decomposition: a new prompt

**Your turn.** *"A bakery chain with 40 shops throws away too much bread every evening."* Write your clarifying questions and a thin first version.

**Model answer.**
- **Clarify:** How much is thrown away now, in loaves or dollars? What's the goal (half the waste, without more empty shelves)? Who decides how much each shop bakes, and when?
- **Data:** daily bake quantity and sales per shop and product, weather, holidays, local events.
- **Thin first version, no AI:** a daily sheet per shop with "last 4 same-weekdays sold" for each product, used by 3 shops for 2 weeks. Measure waste and sell-outs against the other 37.
- **Then:** a forecast model only if the simple sheet leaves real waste on the table.

---

## J10 Pin down the vague word

**Your turn.** *"A university wants to cut the wait for hostel room allotment."* Which word do you pin down first, and how?

**Model answer.** "Wait." From what moment to what moment? From applying to getting an offer, or from the offer to moving in? For which students? Measured how, today? Often the biggest win is removing a step, like asking for documents the university already holds, not making a step faster.

---

## J11 When the prompt says "never wrong"

**Your turn.** *"A city water company wants an AI assistant that tells residents whether their tap water is safe to drink after a repair, and it must never be wrong."* How do you split the work by risk?

**Model answer.** Say honestly that no AI can promise "never wrong". Then: the safe or not-safe answer comes straight from the water company's own notice for that street, looked up by code, and the model never writes it. The model only helps with low-risk parts: understanding the question, finding the street, and explaining the official notice in plain words. When there's no notice for a street, the answer is "we don't know yet, here's who to call", never a guess.

---

## J12 Coding round one: clean a messy file

**Your turn.** Add a rule: a meter can't use negative energy, so reject negative readings with a reason. First add a test row to `meters.csv`: `M-006,2026-10-02,-15,Garage`.

**Model answer.** `solutions/part4/j12/`
```
REJECTED line 9: exact duplicate of an earlier row (first one kept): ...
REJECTED line 10: negative reading: {'meter_id': 'M-006', 'reading_date': '2026-10-02', 'kwh': '-15', ...}
test_solution.py::test_negative_reading_rejected PASSED
```

---

## J13 Coding round two: retries and rate limits

**Your turn.** Add an overall time budget: stop retrying when waiting again would go past it, even if tries are left. Test it with a fake clock.

**Model answer.** `solutions/part4/j13/`. `call_with_retry(..., budget=5.0)` checks `elapsed + next_wait > budget` before sleeping. With 10 tries and 1-second base waits, it waits about 1 second, then 2, sees that the next 4-second wait would pass the 5-second budget, and gives up. The fake clock means the test never really sleeps.
```
test_solution.py::test_gives_up_when_budget_runs_out PASSED
```

---

## J14 AI system design round

**Your turn.** Design, in the chapter's order, an assistant that answers a gym chain's members about bookings and membership rules. One line per step.

**Model answer.**
1. **Requirements:** members ask in the app; answers within 5 seconds; it can't change bookings in phase 1.
2. **Data and tools:** class timetable API (read), member account (read), membership rules PDF (search).
3. **Model:** a small, cheap model is enough for simple lookups; test it on real member questions.
4. **Guardrails and humans:** only the member's own account; cancellations and refunds go to staff.
5. **Evals:** 50 real questions from the help desk, checked for facts and for never booking anything.
6. **Deployment and monitoring:** a container behind the app's backend; trace every answer, and alert on "no source" answers.
7. **Trade-offs:** small model vs accuracy, and read-only vs convenience. Bookings are phase 2.

---

## J15 Customer scenarios and behavioral questions

**Your turn.** Scenario: the client's IT manager sends you the production database password in a chat message "to save time". What do you say?

**Model answer.** "Thanks, I know you're trying to help us move fast. I'd rather not have that password in chat, because it now lives in the chat history. Could we change it, and set up a read-only account for the desk through your usual process? I'll send you the exact access we need today, so it doesn't slow us down."

Own it, explain the risk plainly, and offer a safe way forward.

---

## J16 The offer

**Your turn.** Offer A: higher pay, the team has no senior FDE, mostly demos. Offer B: 10% less, you'd work beside two senior FDEs shipping to customers. Which do you pick for a first role, and what would you ask before deciding?

**Model answer.** For a first role, B, because the work and the mentors build the career, and a 10% difference is small at this stage. Before deciding, ask B: "Could you match part of the gap, or review my pay after six months?" Ask A: "What did the last person in this role ship?"
