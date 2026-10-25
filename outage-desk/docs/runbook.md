# Runbook: Outage Desk on Larkfield's server

## Start, stop, status
```bash
docker compose -f outage-desk/docker-compose.yml -p larkfield up -d      # start
docker compose -f outage-desk/docker-compose.yml -p larkfield ps         # status
docker compose -f outage-desk/docker-compose.yml -p larkfield logs desk  # logs
docker compose -f outage-desk/docker-compose.yml -p larkfield down       # stop
curl localhost:8000/health                                               # quick health check
```

## If something's wrong
| Symptom | Check | Fix |
|---|---|---|
| `/health` says `"database": false` | the image was built without data | rebuild: `... up --build -d` |
| Answers say "live status unavailable" | `curl` the grid service; `logs desk` for `grid WARNING` lines | grid service is down or slow: tell Daniel's team; answers keep working from the log |
| Answers slow (over 30 s) | `uv run python -m outage_desk.monitor` | Ollama overloaded: check `ollama ps` on the server; restart Ollama |
| An answer is wrong | find it in `data/traces.jsonl` | add it to `evals/questions.csv`, fix, re-run evals before redeploying |

## Daily (5 minutes)
- Run `python -m outage_desk.monitor` and read any alerts.
- Spot-check 20 answers from the trace log against the source systems.
