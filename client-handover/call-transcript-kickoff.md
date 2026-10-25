# Kickoff call: Larkfield Power (fictional)

**Thursday, 45 minutes, video call.**
- **Rachel Morgan** (Head of Customer Operations)
- **Daniel Thomas** (IT Manager)
- **Maria Lopez** (Call Center Supervisor, joined at minute 12)
- **FDE** (you)

---

**Rachel:** Thanks for making time. As I said in the email, we want a chatbot on the website. Customers keep calling, and if they could just check the website we wouldn't drown every time there's a storm.

**FDE:** That makes sense. Before we talk about the chatbot, can you walk me through what happened last Tuesday evening?

**Rachel:** The storm hit around four. By six we had more than four hundred calls waiting at once, and about four thousand over the evening. People were on hold for forty minutes, and some gave up and called back three or four times.

**FDE:** When a customer does get through, what do they usually ask?

**Rachel:** Almost always the same thing. When will my power come back?

**FDE:** And how does the agent find that out?

**Rachel:** Maria's team would know better. Daniel?

**Daniel:** It's not one system, honestly. The agent takes the account number and looks up the area in the customer system. Then they check the outage log, which is two logs, because North and South still run separate tools from before the merger. And the restore time comes from the grid status service, or sometimes from calling the crew supervisor.

**FDE:** So three or four lookups for one question.

**Daniel:** On a good day.

*(Maria joins.)*

**Maria:** Sorry, we're short-staffed today. What did I miss?

**FDE:** We were talking about what happens on a call. How long does a typical "when will it come back" call take?

**Maria:** Six, seven minutes on a storm day. Most of that is the agent clicking between screens while the customer waits. And the worst part is that the time we give them is often old. The crew updates the estimate, but our screens don't show it for an hour, so the customer calls back, angry, and gets a different answer.

**FDE:** How many of the calls on Tuesday were people calling back?

**Maria:** I'd guess a third. Maybe more. We don't track it properly.

**FDE:** That's really useful. Can I play back what I'm hearing? The website chatbot is one idea. But the reason the lines jam is that every call takes six minutes of looking things up, and a lot of people call back because the time they were given went stale.

**Rachel:** ...Yes. That's fair.

**FDE:** So if the agents could get the right, current answer in a few seconds, calls would be shorter and fewer people would call back. A website bot could come later, using the same engine.

**Rachel:** I like that. But the board has heard "chatbot", so I'll need to explain the change.

**FDE:** I'll write it up in a one-page note you can share. What would success look like to you by the end of this project?

**Rachel:** Shorter calls, and fewer people calling back. If storm-day calls drop from seven minutes to three, I'd be very happy.

**FDE:** Daniel, any limits I should know about?

**Daniel:** Customer data doesn't leave our servers. That's a hard rule from our regulator and our security team. The grid status service has a rate limit, and it falls over under load. And nothing gets written back to our systems without a person approving it. No automatic compensation, no closing tickets.

**Maria:** One more thing. Some customers are on medical equipment. They get priority, and a supervisor calls them. Whatever you build must never miss those.

**FDE:** Noted, all of it. I'll send the discovery note tomorrow, with the questions I still have.
