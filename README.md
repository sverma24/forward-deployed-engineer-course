# Forward Deployed Engineer Course: Code and Project Files

Everything used in the free **Forward Deployed Engineer Full Course** on YouTube. It covers the small demos from the Foundations part, and the full client project from the first call to handover.

> **Larkfield Power is a fictional company.** All of its data is synthetic, made by `tools/make_client_data.py`. No real customer or company data is used anywhere.

## What's inside

| Folder | What it is | Course part |
|---|---|---|
| `foundations/` | small, separate demos: a web server, an API, SQL, Python, tests, a model in an app, tools, RAG, MCP, evals, Docker | Part 2 |
| `client-handover/` | what the client hands you on day one: messy exports, policy PDFs, a call transcript, and a stand-in for their grid status service | Part 3 |
| `outage-desk/` | the system we build for them: cleaning, a read-only database, an agent with tools, document search, an MCP server, guardrails, human sign-off, evals, Docker | Part 3 |
| `outage-desk/docs/` | the non-code deliverables: discovery note, scope, decisions, change request, runbook, postmortem, handover | Part 3 |
| `tools/` | scripts that generate the synthetic client data | |

## You need

- **Python 3.12+** and **uv** (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **SQLite** (`sqlite3`): already on Mac and most Linux machines. On Windows, download the "command-line tools" bundle from sqlite.org and put `sqlite3.exe` on your PATH.
- **Claude Code**, logged in with a paid Claude plan. The project calls it in headless mode (`claude -p`), so you don't need an API key.
- Optional, for the offline deploy chapter: **Docker** and **Ollama**

No accounts, keys or paid services beyond that.

## Quick start

```bash
uv sync
uv run python tools/make_client_data.py          # (re)create the client's files
cd outage-desk
uv run python -m outage_desk.audit               # what's wrong with the data
uv run python -m outage_desk.clean               # build data/outages.db
uv run python -m outage_desk.docs build          # index the policy PDFs
```

Start the client's grid service in a second terminal, from the repo root:

```bash
uv run uvicorn server:app --app-dir client-handover/grid_api --port 8100
```

Then ask a question, run the tests, or open the screen:

```bash
cd outage-desk
uv run python -m outage_desk.agent "When will power be back for account 4471?"
uv run pytest -q
uv run uvicorn outage_desk.service:app --port 8000     # open http://localhost:8000
```

## If something goes wrong

- **`claude: command not found`:** install Claude Code and run `claude` once to log in.
- **`Connection refused` on port 8100:** the grid service isn't running. Start it as shown above.
- **`no such table`:** run `python -m outage_desk.clean` and `python -m outage_desk.docs build` first.

## License

MIT. See `LICENSE`.
