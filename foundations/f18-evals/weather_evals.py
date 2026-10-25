"""F18: an eval is a list of questions with answers you can check, and a score.

This one tests a weather assistant that's given the station data in its prompt.
Run:  uv run python foundations/f18-evals/weather_evals.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claude_cli import ask_claude  # noqa: E402

DATA = ("Sydney: 24 C, dry, wind 9 km/h. London: 11 C, raining, wind 22 km/h. "
        "Seattle: 9 C, raining, wind 14 km/h.")
SYSTEM = f"You are a weather assistant. Current data: {DATA} Answer in one short sentence using only this data."

CASES = [  # (question, words that must appear, words that must not appear)
    ("Is it raining in London?", ["yes"], []),
    ("Is it raining in Sydney?", ["no"], []),
    ("What's the temperature in Seattle?", ["9"], []),
    ("Which city is warmest?", ["sydney"], []),
    ("Which city is windiest?", ["london"], []),
    ("Do I need an umbrella in Seattle?", ["yes"], []),
    ("What's the weather in Tokyo?", ["don't", "no data", "not"], ["sunny", "°c"]),
    ("Is it colder in London or Seattle?", ["seattle"], []),
    ("How windy is it in Sydney?", ["9"], []),
    ("Will it rain in London tomorrow?", ["don't", "only", "current", "not"], []),
]

passed = 0
for q, must, must_not in CASES:
    answer = ask_claude(q, system=SYSTEM).lower()
    ok = any(m in answer for m in must) and not any(m in answer for m in must_not)
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {q:40} -> {answer[:70]}")
print(f"\nScore: {passed}/{len(CASES)}")
