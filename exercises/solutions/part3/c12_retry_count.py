"""C12 your turn, solved: how much do retries help against a flaky grid service?

Start a flaky copy of the grid service first (half of all calls fail):
  FLAKY=0.5 LATENCY=0 uv run uvicorn server:app --app-dir client-handover/grid_api --port 8101
Then, from outage-desk/:
  PYTHONPATH=. uv run python ../exercises/solutions/part3/c12_retry_count.py
"""

import logging

from outage_desk.grid import GridClient, GridUnavailable

logging.disable(logging.WARNING)      # we only want the totals here

CALLS = 20
for attempts in (1, 2, 4):
    client = GridClient(base_url="http://localhost:8101", attempts=attempts, base_delay=0.1)
    failed = 0
    for _ in range(CALLS):
        try:
            client.area_status("S-07")
        except GridUnavailable:
            failed += 1
    print(f"attempts={attempts}: {failed} of {CALLS} calls failed")
