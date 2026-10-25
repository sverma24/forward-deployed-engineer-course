"""A stand-in for Larkfield Power's live grid status service (fictional).

It behaves like the real kind of client system an FDE meets:
- it needs an API key
- it's rate limited (5 requests a second), and says so with HTTP 429
- it's slow, and sometimes it just fails with HTTP 503
- it knows fresher restore times than the outage logs do

Switches (environment variables):
  GRID_API_KEY   the key clients must send (default: demo-key-123)
  FLAKY          chance of a random 503, 0 to 1 (default: 0.15)
  GRID_DOWN=1    every request fails, for the outage drill
  SCHEMA_V2=1    the vendor's surprise change: restore_eta becomes eta_epoch_ms
  LATENCY=0      turn off the fake slowness

Run:  uv run uvicorn server:app --app-dir client-handover/grid_api --port 8100
"""

import os
import random
import time
import uuid
from collections import deque
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Larkfield Power grid status service (fictional)")

EST = timezone(timedelta(hours=-5))
NOW = datetime(2026, 11, 3, 18, 0, tzinfo=EST)

# What the field crews have reported most recently. Note that S-07's estimate
# is earlier than the 8:30 PM in the South outage log: the crew updated it,
# and the log hasn't caught up. That gap is the stale-time problem from the call.
LIVE = {
    "S-07": {"state": "outage", "restore_eta": NOW + timedelta(hours=1, minutes=45), "crew": "CRW-14",
             "note": "Crew on site, replacing a damaged pole"},
    "S-12": {"state": "outage", "restore_eta": NOW + timedelta(minutes=40), "crew": "CRW-11",
             "note": "Transformer swap in progress"},
    "S-02": {"state": "outage", "restore_eta": None, "crew": None,
             "note": "Fault being located, no crew assigned yet"},
    "N-07": {"state": "outage", "restore_eta": NOW + timedelta(hours=2), "crew": "CRW-02",
             "note": "Tree removal before repair can start"},
    "N-14": {"state": "outage", "restore_eta": None, "crew": None,
             "note": "Assessing storm damage"},
}

API_KEY = os.environ.get("GRID_API_KEY", "demo-key-123")
_calls = {}                 # api key -> recent request times
_tickets, _alerts = [], []
_seen_keys = {}             # idempotency key -> stored response


def _env(name, default=""):
    return os.environ.get(name, default)


@app.middleware("http")
async def chaos(request: Request, call_next):
    if request.url.path.startswith("/docs") or request.url.path == "/openapi.json":
        return await call_next(request)
    if _env("LATENCY", "1") != "0":
        time.sleep(random.uniform(0.2, 1.0))
    if _env("GRID_DOWN") == "1":
        return JSONResponse({"error": "service unavailable"}, status_code=503)
    key = request.headers.get("x-api-key", "")
    window = _calls.setdefault(key, deque())
    t = time.monotonic()
    while window and t - window[0] > 1.0:
        window.popleft()
    if len(window) >= 5:
        return JSONResponse({"error": "rate limit exceeded"}, status_code=429,
                            headers={"Retry-After": "1"})
    window.append(t)
    if random.random() < float(_env("FLAKY", "0.15")):
        return JSONResponse({"error": "upstream timeout"}, status_code=503)
    return await call_next(request)


def _check_key(x_api_key):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="missing or wrong API key")


@app.get("/v1/areas/{area_code}/status")
def area_status(area_code: str, x_api_key: str = Header(default="")):
    _check_key(x_api_key)
    code = area_code.upper()
    live = LIVE.get(code, {"state": "normal", "restore_eta": None, "crew": None, "note": ""})
    body = {"area": code, "state": live["state"], "crew": live["crew"], "note": live["note"],
            "updated_at": (NOW - timedelta(minutes=random.randint(2, 9))).isoformat()}
    eta = live["restore_eta"]
    if _env("SCHEMA_V2") == "1":
        body["eta_epoch_ms"] = int(eta.timestamp() * 1000) if eta else None
    else:
        body["restore_eta"] = eta.isoformat() if eta else None
    return body


class Ticket(BaseModel):
    area: str
    note: str


class Alert(BaseModel):
    account_no: str
    message: str


def _idempotent(key, store, payload):
    if key and key in _seen_keys:
        return _seen_keys[key]
    record = {"id": str(uuid.uuid4())[:8], **payload, "created_at": NOW.isoformat()}
    store.append(record)
    if key:
        _seen_keys[key] = record
    return record


@app.post("/v1/crew-tickets", status_code=201)
def create_ticket(t: Ticket, x_api_key: str = Header(default=""),
                  idempotency_key: str = Header(default="")):
    _check_key(x_api_key)
    return _idempotent(idempotency_key, _tickets, t.model_dump())


@app.get("/v1/crew-tickets")
def list_tickets(x_api_key: str = Header(default="")):
    _check_key(x_api_key)
    return _tickets


@app.post("/v1/text-alerts", status_code=201)
def send_alert(a: Alert, x_api_key: str = Header(default=""),
               idempotency_key: str = Header(default="")):
    _check_key(x_api_key)
    return _idempotent(idempotency_key, _alerts, a.model_dump())


@app.get("/v1/text-alerts")
def list_alerts(x_api_key: str = Header(default="")):
    _check_key(x_api_key)
    return _alerts
