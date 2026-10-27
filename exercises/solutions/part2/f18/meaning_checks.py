"""F18 your turn, solved: checks that test the meaning, not the wording.
A structured answer has a field we can compare exactly, and a sentence answer is judged by its first word."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "foundations"))
from claude_cli import ask_claude  # noqa: E402

DATA = ("Sydney: 24 C, dry, wind 9 km/h. London: 11 C, raining, wind 22 km/h. "
        "Seattle: 9 C, raining, wind 14 km/h.")
SYSTEM = f"You are a weather assistant. Current data: {DATA} Use only this data."
SCHEMA = {"type": "object", "properties": {
    "city": {"type": ["string", "null"]}, "yes_no": {"type": ["string", "null"], "enum": ["yes", "no", None]},
    "sentence": {"type": "string"}}, "required": ["city", "yes_no", "sentence"]}

CASES = [  # (question, field, expected)
    ("Which city is colder, London or Seattle?", "city", "Seattle"),
    ("Which city is windiest?", "city", "London"),
    ("Is it raining in Sydney?", "yes_no", "no"),
    ("Is it raining in Seattle?", "yes_no", "yes"),
    ("Which city should I visit if I want dry weather?", "city", "Sydney"),
]
passed = 0
for q, field, expected in CASES:
    out = ask_claude(q, system=SYSTEM, schema=SCHEMA)
    ok = (out.get(field) or "").lower() == expected.lower()
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {q:50} {field}={out.get(field)!r:10} | {out['sentence'][:60]}")
print(f"\nScore: {passed}/{len(CASES)}")
