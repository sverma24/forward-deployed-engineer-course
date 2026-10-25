"""A careful client for Larkfield's grid status service (chapters C11 and C12).

The service is slow, rate limited and sometimes down, so this client:
- retries 429 and 5xx with exponential backoff plus jitter, honouring Retry-After
- gives up after a few tries and says so clearly, instead of hanging or guessing
- sends an Idempotency-Key on every write, so a retry can't create a second ticket
"""

import logging
import random
import time
import uuid

import httpx

from .config import GRID_API_KEY, GRID_URL

log = logging.getLogger("grid")


class GridUnavailable(Exception):
    """The grid service couldn't be reached after several tries."""


class GridClient:
    def __init__(self, base_url=GRID_URL, api_key=GRID_API_KEY, attempts=4, base_delay=0.5, timeout=5.0):
        self.http = httpx.Client(base_url=base_url, timeout=timeout,
                                 headers={"X-Api-Key": api_key})
        self.attempts = attempts
        self.base_delay = base_delay

    def _request(self, method, path, **kw):
        last = None
        for attempt in range(1, self.attempts + 1):
            try:
                r = self.http.request(method, path, **kw)
            except httpx.TransportError as e:
                last = f"network error: {e.__class__.__name__}"
            else:
                if r.status_code < 400:
                    return r.json()
                if r.status_code not in (429, 500, 502, 503, 504):
                    r.raise_for_status()          # 401, 404...: retrying won't help
                last = f"HTTP {r.status_code}"
                retry_after = r.headers.get("Retry-After")
                if retry_after:
                    log.warning("%s %s: %s, waiting %s s as the server asked", method, path, last, retry_after)
                    time.sleep(float(retry_after))
                    continue
            if attempt < self.attempts:
                # 0.5 s, 1 s, 2 s... plus a random bit, so many clients don't retry in lockstep.
                wait = self.base_delay * 2 ** (attempt - 1) + random.uniform(0, 0.3)
                log.warning("%s %s: %s on try %d, retrying in %.1f s", method, path, last, attempt, wait)
                time.sleep(wait)
        raise GridUnavailable(f"grid service unavailable after {self.attempts} tries ({last})")

    def area_status(self, area_code):
        data = self._request("GET", f"/v1/areas/{area_code}/status")
        return {**data, "restore_eta": parse_eta(data)}

    def create_crew_ticket(self, area, note, idempotency_key=None):
        key = idempotency_key or str(uuid.uuid4())
        return self._request("POST", "/v1/crew-tickets", json={"area": area, "note": note},
                             headers={"Idempotency-Key": key})

    def send_text_alert(self, account_no, message, idempotency_key=None):
        key = idempotency_key or str(uuid.uuid4())
        return self._request("POST", "/v1/text-alerts", json={"account_no": account_no, "message": message},
                             headers={"Idempotency-Key": key})


def parse_eta(data):
    return data.get("restore_eta")
