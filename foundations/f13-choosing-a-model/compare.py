"""F13: the same task on Claude (cloud) and on a small local model (Ollama, nothing leaves your laptop).

Needs Ollama running with:  ollama pull qwen3:4b
Run:  uv run python foundations/f13-choosing-a-model/compare.py
"""

import json
import sys
import time
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claude_cli import ask_claude  # noqa: E402

SCHEMA = {"type": "object", "properties": {
    "category": {"type": "string", "enum": ["billing", "outage", "account", "other"]},
    "urgency": {"type": "string", "enum": ["low", "medium", "high"]}},
    "required": ["category", "urgency"]}
COMPLAINTS = [
    "I've been charged twice for my March bill and nobody answers the phone.",
    "Power has been out on our whole street since 6 AM and my father uses an oxygen machine.",
    "How do I change the email address on my account?",
    "The website says my payment failed but my bank says it went through.",
    "There's a sparking wire hanging off the pole outside my house.",
]


def local(prompt):
    r = httpx.post("http://localhost:11434/api/chat", timeout=120, json={
        "model": "qwen3:4b", "stream": False, "format": SCHEMA, "think": False, "options": {"temperature": 0},
        "messages": [{"role": "user", "content": prompt}]})
    return json.loads(r.json()["message"]["content"])


for name, fn in [("Claude (haiku, cloud)", lambda p: ask_claude(p, schema=SCHEMA)), ("qwen3:4b (local)", local)]:
    print(f"\n=== {name} ===")
    start = time.time()
    for c in COMPLAINTS:
        out = fn(f"Classify this utility customer complaint.\n\nComplaint: {c}")
        print(f"{out['category']:8} {out['urgency']:6}  {c[:60]}")
    print(f"total time: {time.time() - start:.1f} s for {len(COMPLAINTS)} complaints")
