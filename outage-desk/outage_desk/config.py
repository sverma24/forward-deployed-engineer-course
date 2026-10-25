"""Settings for the outage desk. Everything can be changed with an environment
variable, so the same code runs on a laptop, in Docker, and on the client's server."""

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent                      # outage-desk/
LABS = PROJECT.parent                      # the repo root
HANDOVER = Path(os.environ.get("HANDOVER_DIR", LABS / "client-handover"))

DATA_DIR = Path(os.environ.get("DATA_DIR", PROJECT / "data"))
DB_PATH = DATA_DIR / "outages.db"          # cleaned client data, read-only at runtime
DOCS_DB = DATA_DIR / "policies.db"         # search index over the policy PDFs
APPROVALS_DB = DATA_DIR / "approvals.db"   # the only thing our app writes to
TRACE_LOG = DATA_DIR / "traces.jsonl"

EST = timezone(timedelta(hours=-5))
# The course replays one storm evening, so "now" is pinned. Set DEMO_NOW=real to use the clock.
_now = os.environ.get("DEMO_NOW", "2026-11-03T18:00:00-05:00")


def now():
    return datetime.now(EST) if _now == "real" else datetime.fromisoformat(_now)


# Which model answers: "claude" (Claude Code on your subscription) or "ollama" (local).
MODEL_BACKEND = os.environ.get("MODEL_BACKEND", "claude")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "haiku")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:4b")

GRID_URL = os.environ.get("GRID_URL", "http://localhost:8100")
GRID_API_KEY = os.environ.get("GRID_API_KEY", "demo-key-123")
