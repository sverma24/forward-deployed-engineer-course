"""One clear solution to J13."""

import random
import threading
import time
from collections import deque


class TemporaryError(Exception):
    """Something that may work if we try again (a timeout, a 503, a 429)."""


def call_with_retry(fn, attempts=4, base=0.5, sleep=time.sleep):
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except TemporaryError:
            if attempt == attempts:
                raise
            # Jitter spreads retries out, so a thousand clients don't all hit the service at the same instant.
            sleep(base * 2 ** (attempt - 1) + random.uniform(0, base / 2))


class RateLimiter:
    """Sliding window: remember when the last calls happened, and wait if the window is full."""

    def __init__(self, per_second, clock=time.monotonic, sleep=time.sleep):
        self.per_second, self.clock, self.sleep = per_second, clock, sleep
        self.calls = deque()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            while True:
                now = self.clock()
                while self.calls and now - self.calls[0] >= 1.0:
                    self.calls.popleft()
                if len(self.calls) < self.per_second:
                    self.calls.append(now)
                    return
                self.sleep(1.0 - (now - self.calls[0]))
