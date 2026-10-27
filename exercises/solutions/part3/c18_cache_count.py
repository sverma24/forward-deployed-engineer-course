"""C18 your turn, solved: count how many times the grid service is really called.

Ten agents ask about Riverside (S-07) one after another. Run from outage-desk/:
  PYTHONPATH=. uv run python ../exercises/solutions/part3/c18_cache_count.py
"""

import logging

from outage_desk import tools

logging.disable(logging.WARNING)

calls = 0
real_area_status = tools.grid().area_status


def counting_area_status(area_code):
    global calls
    calls += 1
    return real_area_status(area_code)


tools.grid().area_status = counting_area_status

for seconds in (0, 60):
    tools.CACHE_SECONDS = seconds
    tools._cache.clear()
    calls = 0
    for _ in range(10):
        tools.get_outage_status("S-07")
    print(f"cache {seconds:>2} s: 10 questions, {calls} call{"" if calls == 1 else "s"} to the grid service")
