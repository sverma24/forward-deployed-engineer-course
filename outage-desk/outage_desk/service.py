"""The web service call center agents use (chapters C7, C9, C15, C20).

Run:  uv run uvicorn outage_desk.service:app --port 8000
Then open http://localhost:8000
"""

import time

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import agent, approvals, db
from .config import DB_PATH, MODEL_BACKEND, HERE

app = FastAPI(title="Larkfield outage desk")
STARTED = time.time()


class Question(BaseModel):
    question: str
    customer_message: str = ""


class Decision(BaseModel):
    approve: bool
    supervisor: str


@app.get("/")
def page():
    return FileResponse(HERE / "web" / "index.html")


@app.get("/health")
def health():
    """What the runbook checks first: is the data there, and which model is in use?"""
    ok = DB_PATH.exists()
    return {"status": "ok" if ok else "degraded", "database": ok, "model_backend": MODEL_BACKEND,
            "uptime_seconds": int(time.time() - STARTED)}


@app.get("/accounts/{account_no}")
def account(account_no: str):
    acc = db.find_account(account_no)
    if not acc:
        raise HTTPException(status_code=404, detail="account not found")
    return acc


@app.post("/ask")
def ask(q: Question):
    out = agent.ask(q.question, context=q.customer_message)
    return {k: out[k] for k in ("answer", "sources", "turns", "seconds")}


@app.get("/approvals")
def list_approvals():
    return approvals.pending()


@app.post("/approvals/{aid}")
def decide(aid: str, d: Decision):
    if not approvals.decide(aid, d.approve, d.supervisor):
        raise HTTPException(status_code=404, detail="no pending approval with that id")
    return {"id": aid, "status": "approved" if d.approve else "rejected"}
