# Part 1 exercises: the job

Each chapter in the video ends with a "Your turn" task. Pause the video, do it yourself, then compare with the model answer here.
A model answer is one good answer, not the only one. If yours is different but you can explain why, it counts.

---

## 1.1 One week as a forward deployed engineer

**Your turn.** A city hospital buys a ready-made food-ordering app for its staff canteen. Write down three things an FDE would have to change or check so the app fits *this* hospital, not hospitals in general.

**Hint.** Think about the hospital's people, its rules and its existing systems. Who orders food, when, and how do they pay?

**Model answer.**
1. **Shifts.** Night-shift nurses need to order at 3 AM, so the canteen's opening hours and the menu for each shift have to come from the hospital's own rota, not a default.
2. **Payment.** Staff pay through payroll deduction, so the app has to connect to the hospital's payroll system instead of taking cards.
3. **Rules.** Patients' diet rules must never mix with staff orders, so the FDE checks that staff accounts can't see or touch patient meal data.

That's the tailor's job: the app works for everyone roughly, and the FDE makes it fit one customer properly.

---

## 1.2 FDE vs software engineer vs solutions engineer vs consultant

**Your turn.** Name the role for each description.
1. "Joins before the deal is signed, runs demos, and helps close the sale."
2. "Works on the core product, shipping features that every customer gets."
3. "Arrives after the sale, writes production code inside one customer's systems, and owns whether it works."
4. "Writes a report recommending what the client should build, then leaves."

**Hint.** Ask two questions every time: when do they arrive, and who owns the outcome?

**Model answer.** 1 is a solutions or sales engineer (before the sale, tied to a target). 2 is a software engineer (builds for everyone). 3 is a forward deployed engineer (after the sale, production code, owns the result). 4 is a consultant (advises, doesn't usually build or own it).

---

## 1.3 Where the job came from

**Your turn.** Explain to a friend in two sentences why AI companies are hiring FDEs right now.

**Model answer.** "AI models are powerful, but on their own they don't know a company's data, systems or rules, so most companies can't turn them into something that works. FDEs sit with the customer and do that fitting, and what they learn makes the product better for the next customer."

---

## 1.4 Three different jobs hiding under one title

**Your turn.** Read this made-up posting and decide which of the three jobs it really is: a builder, the sales engineer kind, or an internal tools builder.

> *Forward Deployed Engineer.* You'll partner with our account executives on strategic opportunities, deliver compelling product demonstrations, run proofs of concept, and help shape the technical win strategy. Some scripting is a plus.

Then find one real FDE post near you and underline its verbs.

**Hint.** Ignore the title. Look at the verbs, and at who the role sits next to.

**Model answer.** It's the sales-engineer kind. The verbs are *partner with account executives, deliver demonstrations, run proofs of concept, shape the technical win*. All of that happens before a sale, and "some scripting is a plus" tells you there's very little production code. A builder post would say things like *build, deploy, integrate, own in production*.

---

## 1.5 Where FDEs work, and what they earn

**Your turn.** Make a short target list: three *kinds* of company where FDE work is likely, and for each one, why it needs FDEs.

**Model answer.**
| Kind of company | Why it needs FDEs |
|---|---|
| An AI lab selling models to big companies | Every customer has different data and rules, and a model alone doesn't ship anything |
| A software startup selling to hospitals, banks or utilities | Those industries run old systems with strict rules, so every install is different |
| A data or analytics platform | Customers' data is messy and lives in many systems, so someone has to connect it |

Remember from the chapter that pay figures are estimates, and that entry-level roles are a small share. Apply widely.

---

## 1.6 The engagement map

**Your turn.** These eight moments from a project are shuffled. Put them in order, and name the step of the engagement map for each.

a) Five call-center agents try the system for two storms.
b) You learn that "a chatbot" really means "agents can't find the restore time".
c) You write a runbook and train the client's IT team.
d) You connect to the client's grid-status service.
e) You compare call length before and after.
f) You split the goal into pieces and write a definition of done.
g) You draw the architecture and write down the trade-offs.
h) You write the first endpoint and its tests.

**Model answer.** b Discover → f Decompose → g Design → h Build → d Integrate → a Ship → e Measure → c Hand off.

---

## 1.7 Is this job for you?

**Your turn.** Write a short, honest note to yourself: which downside of the job (travel, pressure, constant switching between clients, being the face when things break) would be hardest for you, and one thing you'd do about it.

**Model answer (one example).** "Being the person on the call when something breaks would scare me. To get used to it, I'll practise explaining a bug out loud to a friend in plain words, and I'll offer to take the questions when our team demos our college project."

There's no wrong answer. The point is to decide with your eyes open.

---

## 1.8 What you already have

**Your turn.** Write three lines in this form: *"I've done (blank), which is the FDE skill of (blank)."*

**Model answer (a QA tester).**
- I've written test cases from vague requirements, which is the FDE skill of **turning a fuzzy request into a clear definition of done**.
- I've reproduced bugs from customer reports, which is the FDE skill of **debugging in someone else's environment**.
- I've explained bugs to developers and managers, which is the FDE skill of **explaining technical problems to different audiences**.

**Model answer (a final-year student).**
- I've built a college project with a team, which is the FDE skill of **shipping something end to end**.
- I've presented my project to examiners, which is the FDE skill of **demoing to people who ask hard questions**.
- I've cleaned data for a class assignment, which is the FDE skill of **working with messy client data**.
