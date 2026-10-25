# Architecture: Outage Desk

```
 call center agent
        │  question (+ customer's message, if any)
        ▼
 ┌──────────────────────────────┐
 │  Outage Desk service (FastAPI) │  ← one screen for agents, /health for IT
 └──────────────┬───────────────┘
                ▼
 ┌──────────────────────────────┐        ┌─────────────────────────┐
 │  Agent loop                    │◀──────▶│  Model                   │
 │  (our code runs every tool)    │        │  dev: Claude (claude -p)  │
 └──┬────────┬────────┬────────┬─┘        │  server: local (Ollama)   │
    │        │        │        │          └─────────────────────────┘
    ▼        ▼        ▼        ▼
 accounts  outage   policy   approvals
 + outages  status   search   queue
 (SQLite,  (grid     (FTS5    (the only thing
  read-only) service)  index)   we write to)
```

## Where each piece of data comes from
| Data | Source | How we use it |
|---|---|---|
| Customer → area | `accounts.csv`, cleaned into `outages.db` | read-only lookup |
| Open outages | North + South logs, merged into `outages.db` | read-only lookup |
| Latest restore time | grid status service (live) | preferred over the log; cached for 60 s |
| Policies | three PDFs, indexed page by page | answers cite document + page |
| Suggested actions | our approvals queue | a supervisor approves or rejects |

## Key decisions
See `decisions.md`.
