# Part 2 exercises: the tech, from zero

Every exercise here was run for real while making the course. The solution files are in `exercises/solutions/part2/`, and the output shown is what came back.
Run the commands from the repo root unless a step says otherwise. The AI exercises use Claude Code on your own paid Claude plan (no API key), and F13 also uses Ollama.

---

## F1 How apps talk

**Your turn.** The F1 server answers `/hello`. Add a `/time` path that replies with the current time, and make sure any other address still gets a `404`.

**Hint.** The server looks at `self.path`. Add one more `if`, and keep the `404` as the last branch.

**Model answer.** `solutions/part2/f01/hello_server.py`
```
$ curl -i localhost:8081/time
HTTP/1.0 200 OK
The time here is 22:25.

$ curl -i localhost:8081/weather
HTTP/1.0 404 Not Found
Nothing lives at that address.
```

---

## F2 APIs, HTTP and JSON

**Your turn.** Add Toronto to the weather API, and add a `/stations` address that lists every station name.

**Hint.** The stations live in one dictionary. A new route can return `sorted(STATIONS)`.

**Model answer.** `solutions/part2/f02/status_api.py`
```
$ curl -s localhost:8091/stations
{"stations":["london","seattle","sydney","toronto"]}
$ curl -s localhost:8091/stations/toronto
{"city":"Toronto","temperature_c":4,"raining":false,"wind_kmh":18}
```

---

## F3 From spreadsheets to SQL

**Your turn.** Which customer spent the most money, and on how many orders?

**Hint.** `GROUP BY customer`, then `COUNT(*)` and `SUM(quantity * price_each)`, sorted biggest first.

**Model answer.** `solutions/part2/f03/answer.sql`. Zoe, 2 orders, $51.

---

## F4 SQL that FDEs use every day

**Your turn.** 1) List orders worth more than $20 with the customer's name. 2) Count orders per customer, counting the duplicated order only once.

**Hint.** For 2, use a `LEFT JOIN` so customers with no orders still show, and `COUNT(DISTINCT order_id)`.

**Model answer.** `solutions/part2/f04/answer.sql`
```
order_id  name  item        order_value
1003      Zoe   Backpack    45
1005      Ava   Calculator  25
```
Order 1006 has no customer, so a plain join drops it. That's exactly the kind of row you report to the client.

---

## F5 Just enough Python, part one

**Your turn.** The city report adds up money per city. Make it also count the orders per city.

**Model answer.** `solutions/part2/f05/city_report.py`
```
Boston   $88   from 4 orders
Denver   $73   from 3 orders
Austin   $20   from 1 order
```
Notice "1 order" vs "4 orders". Small touches like that are what clients notice.

---

## F6 Just enough Python, part two: reading errors

**Your turn.** Add a sale whose amount is `1O0` (the letter O, not a zero). Make the script log every bad row with the reason and skip it, instead of crashing.

**Hint.** Wrap `int(...)` in `try/except ValueError`, and use `logging.warning`.

**Model answer.** `solutions/part2/f06/sales_by_city.py`
```
WARNING sale 3 has amount '', which isn't a whole number; skipping it
WARNING sale 5 has amount '1O0', which isn't a whole number; skipping it
Total sales: 260
```

---

## F7 Tests

**Your turn.** Add a `SAVE20` coupon: 20% off orders of $100 or more. Write the tests first, at the boundary.

**Model answer.** `solutions/part2/f07/`. Four tests: exactly $100 gets the discount, $99 doesn't, $150 comes to $120, and `SAVE10` still works.
```
4 passed
```

---

## F8 The terminal for FDEs

**Your turn.** In `foundations/f08-terminal/app.log`: count the INFO lines, find the slow responses, and show every line that isn't INFO.

**Model answer.**
```
$ grep -c INFO app.log
12
$ grep "slow response" app.log
$ grep -v INFO app.log
... WARNING slow response: 2100 ms
... ERROR upstream timeout after 5000 ms
```
`grep -v` (show lines that *don't* match) is the fastest way to find trouble in a noisy log.

---

## F9 Git and GitHub

**Your turn.** In a tiny practice repo (one file, `app.py`, that prints "weather api", and one commit), make a branch called `fix-typo`, change "weather api" to "weather API", look at the diff, commit it, and view the history.

**Model answer.**
```
$ git switch -c fix-typo
$ git diff
-print("weather api")
+print("weather API")
$ git commit -am "Capitalise API in the banner"
$ git log --oneline --all --graph
```
Always read `git diff` before you commit. It's your last chance to spot a key or password.

---

## F10 What a model does inside an app

**Your turn.** Change the chat app so it only sends the last two messages to the model. Then ask it to remind you of your order number.

**Model answer.** `solutions/part2/f10/short_memory_bot.py`. The bot answered "I don't have access to your order history, so I can't see your order number", even though the customer said it three messages earlier. The model didn't forget. The app stopped putting it on the desk.

---

## F11 Why models make things up

**Your turn.** Give the model a short library rules document. Ask three questions: one it covers, one that needs a calculation, and one it doesn't cover at all.

**Model answer.** `solutions/part2/f11/library_rules.py`
- Borrowing limit: "up to 8 books" (from the document).
- 30 days late: "$5.00", because 25 cents × 30 days is $7.50 but the document caps fees at $5.
- Dogs: "I don't know. The document … doesn't say anything about bringing dogs."

The third answer is the important one. A grounded model says "I don't know" instead of guessing.

---

## F12 Prompts are probability

**Your turn.** Add a `sentiment` field to the complaint schema, allowing only `calm`, `frustrated` or `angry`.

**Model answer.** `solutions/part2/f12/classify_with_sentiment.py`
```
{"category": "billing", "urgency": "high", "sentiment": "angry"}
{"category": "account", "urgency": "low", "sentiment": "calm"}
```
A fixed list (an enum) means your code can act on the value without guessing what "kind of upset" means.

---

## F13 Choosing a model

**Your turn.** Add one tricky complaint ("my neighbour's lights are on but mine aren't, and I paid my bill") and run it on Claude and on the local model.

**Model answer.** `solutions/part2/f13/compare_plus.py`. Claude said `outage, high`. The local model said `billing, low` because it latched onto "paid my bill". It was about seven times faster (2.8 s vs 19.5 s for six complaints), but it got the hard case wrong. That's the trade-off, measured on your own data.

---

## F14 Tools and the agent loop

**Your turn.** Add a second tool, `celsius_to_fahrenheit`, and ask for London's temperature in Fahrenheit.

**Model answer.** `solutions/part2/f14/agent_two_tools.py`
```
[turn 1] get_station({'city': 'London'}) -> temperature_c 11
[turn 2] celsius_to_fahrenheit({'celsius': 11}) -> 51.8
[turn 3] answer: London is currently 51.8°F (11°C).
```
The model chained two tools by itself, but your code ran both of them.

---

## F15 Workflows vs agents

**Your turn.** Move the refund limit out of the code into a setting, `REFUND_LIMIT`, and test $350 and $640 with the limit at $500.

**Model answer.** `solutions/part2/f15/triage_config.py`
```
$ REFUND_LIMIT=500 uv run python exercises/solutions/part2/f15/triage_config.py
{'topic': 'billing', 'amount': 350} -> the auto-refund queue
{'topic': 'billing', 'amount': 640} -> a human
```
The business can change the limit without a code change, and the model never decides it.

---

## F16 Answering from documents (RAG)

**Your turn.** Add a fourth handbook file about remote work, and ask how much you can spend on a chair for working from home.

**Model answer.** `solutions/part2/f16/`. No code change needed:
```
Retrieved: remote-work.txt, equipment.txt
Answer: Home equipment such as a chair is reimbursed up to $300, once every 3 years [remote-work.txt].
```

---

## F17 MCP

**Your turn.** Add a `list_stations` tool to the weather MCP server, then ask Claude Code which cities it can check and which is warmest.

**Model answer.** `solutions/part2/f17/weather_mcp.py` and `mcp.json`. Claude Code called `list_stations` first, then `get_station` for Sydney, London and Seattle, and answered "Sydney is the warmest right now at 24°C". A clear tool description is what made it pick the right tool first.

---

## F18 Evals

**Your turn.** Rewrite the eval so the checks test the meaning, not the exact wording.

**Model answer.** `solutions/part2/f18/meaning_checks.py`. The model also returns one structured field (`city` or `yes_no`), and the check compares only that field. Score: 5/5, and a reworded answer no longer fails.

---

## F19 Docker

**Your turn.** Rebuild the image with your F2 changes (Toronto and `/stations`) as `weather-api:v2`, and run it.

**Model answer.** `solutions/part2/f19/`
```
$ docker build -t weather-api:v2 .
#7 CACHED                     <- the pip install layer was reused
$ curl -s localhost:8096/stations
{"stations":["london","seattle","sydney","toronto"]}
```
Only the changed file was copied again. That's why the code goes in the last layer.

---

## F20 Where client software lives

**Your turn.** A regional bank wants an assistant for its branch staff. Fill in four lines: where the systems live, how people log in, who can see what, and where data may go.

**Model answer.**
| Question | Answer to find out (and a likely one) |
|---|---|
| Where do the systems live? | Core banking on the bank's own servers (on-prem), email and documents in a cloud office suite |
| How do people log in? | Single sign-on (SSO) with the bank's staff accounts; programs use API keys or service accounts that IT issues |
| Who can see what? | Tellers see their branch's customers only; managers see the region. The assistant must respect the same roles |
| Where may data go? | Customer data must stay in the country and likely on the bank's servers, so a cloud model may need approval or a local one |

---

## F21 What client systems really look like

**Your turn.** The same person appears in three systems. Are they one customer, and which system do you trust for what?
- Billing: `ACC 04471, E. WALKER`
- Customer service: `Emma Walker, account 4471, 17 Riverside Dr, phone (788) 555-0199`
- Field crew sheet: `Walker, Riverside Dr, area S-07`

**Model answer.** Very likely one customer. The account number matches once you drop the leading zero, the surname agrees, and two systems give the same street. Trust billing for the account number, customer service for the phone number, and the crew or network system for the area. Write that down as a rule, and confirm it with the client before you merge anything.

---

## F22 Working with a coding agent

**Your turn.** Ask Claude Code to add a `/stations` endpoint with a test. Ask for a plan first, then let it make the change, and review the diff.

**Model answer.** `solutions/part2/f22-stations-endpoint.patch`. The plan said it would return a bare list and asked which format we wanted. Without answering, we ran the request again with edits allowed, and the change returned `{"stations": [...]}`, explaining why afterwards. Both are reasonable, but **the plan and the change didn't match**, and only reading the diff caught it. That's why you review every diff yourself.
