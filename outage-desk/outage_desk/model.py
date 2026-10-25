"""One small door to the model, with two backends behind it (chapters F13, C21).

- "claude": runs headless Claude Code (`claude -p`) on your Claude subscription.
  No API key, no extra cost. Good on your laptop.
- "ollama": a local model through Ollama. Nothing leaves the machine. This is
  what runs on the client's server, where there's no Claude login.

The rest of the app only ever calls decide(), so swapping is one setting.
"""

import json
import os
import subprocess
import tempfile

import httpx

from .config import CLAUDE_MODEL, MODEL_BACKEND, OLLAMA_MODEL, OLLAMA_URL

DECISION_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["call_tools", "answer"]},
        "calls": {"type": "array", "items": {
            "type": "object",
            "properties": {"tool": {"type": "string"}, "args": {"type": "object"}},
            "required": ["tool", "args"]}},
        "answer": {"type": "string"},
        "sources": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["action"],
}


class ModelError(Exception):
    pass


def decide(system, transcript, backend=None):
    backend = backend or MODEL_BACKEND
    if backend == "claude":
        return _claude(system, transcript)
    if backend == "ollama":
        return _ollama(system, transcript)
    raise ModelError(f"unknown MODEL_BACKEND {backend!r}")


def _claude(system, transcript):
    # A clean environment and an empty folder: no project settings, no tools, no MCP servers.
    env = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "SHELL", "PATH", "TERM") if k in os.environ}
    cmd = ["claude", "-p", "--model", CLAUDE_MODEL, "--tools", "", "--setting-sources", "",
           "--strict-mcp-config", "--no-session-persistence", "--system-prompt", system,
           "--output-format", "json", "--json-schema", json.dumps(DECISION_SCHEMA)]
    with tempfile.TemporaryDirectory() as empty:
        p = subprocess.run(cmd, input=transcript, capture_output=True, text=True, env=env,
                           cwd=empty, timeout=120)
    if p.returncode != 0:
        raise ModelError(f"claude -p failed: {p.stderr.strip()[:300]}")
    out = json.loads(p.stdout)
    if out.get("is_error") or not out.get("structured_output"):
        raise ModelError(f"no structured output: {out.get('result', '')[:300]}")
    return out["structured_output"]


def _ollama(system, transcript):
    r = httpx.post(f"{OLLAMA_URL}/api/chat", timeout=180, json={
        "model": OLLAMA_MODEL, "stream": False, "format": DECISION_SCHEMA,
        "options": {"temperature": 0},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": transcript}],
    })
    r.raise_for_status()
    try:
        return json.loads(r.json()["message"]["content"])
    except (KeyError, json.JSONDecodeError) as e:
        raise ModelError(f"ollama returned something that isn't the expected JSON: {e}") from e
