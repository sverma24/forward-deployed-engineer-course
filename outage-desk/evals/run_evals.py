"""Run the eval set and score it (chapters C16 and C17).

Each question has simple, checkable expectations:
  must_include      at least one of these (separated by |) appears in the answer
  must_not_include  none of these appear (for example "approved" or a phone number)
  must_cite         this appears in the answer's sources

Run all:      uv run python evals/run_evals.py
Run a few:    uv run python evals/run_evals.py q01 q24
Local model:  MODEL_BACKEND=ollama uv run python evals/run_evals.py
"""

import csv
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from outage_desk import agent  # noqa: E402
from outage_desk.config import MODEL_BACKEND  # noqa: E402

HERE = Path(__file__).resolve().parent


def any_of(text, options):
    opts = [o.strip().lower() for o in options.split("|") if o.strip()]
    return not opts or any(o in text for o in opts)


def none_of(text, options):
    opts = [o.strip().lower() for o in options.split("|") if o.strip()]
    return not any(o in text for o in opts)


def score(q, out):
    answer = out["answer"].lower()
    sources = " ".join(out["sources"]).lower()
    checks = {
        "content": any_of(answer, q["must_include"]),
        "safety": none_of(answer, q["must_not_include"]),
        "citation": not q["must_cite"] or q["must_cite"].lower() in sources,
    }
    return all(checks.values()), [k for k, ok in checks.items() if not ok]


def run_one(q):
    try:
        out = agent.ask(q["question"], context=q["customer_message"], trace=False)
    except Exception as e:  # a crash is a failed case, not a stopped run
        out = {"answer": f"ERROR: {e}", "sources": [], "seconds": 0, "turns": 0, "cost_usd": 0}
    ok, failed = score(q, out)
    return {**q, "passed": ok, "failed_checks": ",".join(failed), "answer": out["answer"],
            "sources": "; ".join(out["sources"]), "seconds": out["seconds"], "cost_usd": out.get("cost_usd", 0)}


def main():
    with (HERE / "questions.csv").open() as f:
        questions = list(csv.DictReader(f))
    only = set(sys.argv[1:])
    if only:
        questions = [q for q in questions if q["id"] in only]
    started = time.time()
    workers = int(os.environ.get("EVAL_WORKERS", "4"))
    with ThreadPoolExecutor(max_workers=workers) as pool:      # a few at a time, to stay polite to the model
        results = list(pool.map(run_one, questions))

    by_cat = defaultdict(lambda: [0, 0])
    for r in results:
        by_cat[r["category"]][0] += r["passed"]
        by_cat[r["category"]][1] += 1
        mark = "PASS" if r["passed"] else f"FAIL ({r['failed_checks']})"
        print(f"{r['id']}  {mark:28} {r['question'][:60]}")
    passed = sum(r["passed"] for r in results)
    secs = sorted(r["seconds"] for r in results)
    cost = sum(r["cost_usd"] for r in results)
    print(f"\nScore: {passed}/{len(results)} ({100 * passed // max(len(results), 1)}%)  "
          f"backend={MODEL_BACKEND}  {time.time() - started:.0f} s")
    print(f"Per answer: median {secs[len(secs) // 2]} s, slowest {secs[-1]} s, "
          f"API-price cost ${cost / len(results):.4f}")
    for cat, (p, n) in sorted(by_cat.items()):
        print(f"  {cat:16} {p}/{n}")

    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    path = out_dir / f"run-{time.strftime('%Y%m%d-%H%M%S')}-{MODEL_BACKEND}.csv"
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    print(f"details: {path.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
