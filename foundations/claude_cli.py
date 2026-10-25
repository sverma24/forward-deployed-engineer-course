"""A tiny helper the AI demos share: ask Claude a question through headless Claude Code.

It runs `claude -p` on your Claude plan, so there's no API key and no extra cost.
Every call starts fresh: the model remembers nothing between calls.
"""

import json
import os
import subprocess
import tempfile


def ask_claude(prompt, system="You are a helpful assistant. Answer briefly.", schema=None, model="haiku"):
    env = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "SHELL", "PATH", "TERM") if k in os.environ}
    env["ENABLE_TOOL_SEARCH"] = "false"
    cmd = ["claude", "-p", "--model", model, "--tools", "", "--setting-sources", "",
           "--strict-mcp-config", "--no-session-persistence", "--system-prompt", system,
           "--output-format", "json"]
    if schema:
        cmd += ["--json-schema", json.dumps(schema)]
    with tempfile.TemporaryDirectory() as empty:
        out = subprocess.run(cmd, input=prompt, capture_output=True, text=True, env=env, cwd=empty, timeout=120)
    data = json.loads(out.stdout)
    return data["structured_output"] if schema else data["result"]
