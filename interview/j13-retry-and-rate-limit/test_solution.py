import pytest

from solution import RateLimiter, TemporaryError, call_with_retry


def test_retries_then_succeeds():
    tries = []

    def flaky():
        tries.append(1)
        if len(tries) < 3:
            raise TemporaryError()
        return "ok"

    waits = []
    assert call_with_retry(flaky, sleep=waits.append) == "ok"
    assert len(waits) == 2 and waits[1] > waits[0]          # the wait grows


def test_never_retries_a_permanent_error():
    tries = []

    def broken():
        tries.append(1)
        raise ValueError("bad input")

    with pytest.raises(ValueError):
        call_with_retry(broken, sleep=lambda s: None)
    assert len(tries) == 1


def test_rate_limiter_waits_when_window_is_full():
    t = [0.0]
    slept = []
    limiter = RateLimiter(3, clock=lambda: t[0], sleep=lambda s: (slept.append(s), t.__setitem__(0, t[0] + s)))
    for _ in range(4):
        limiter.acquire()
    assert slept == [1.0]                                       # the 4th call waited a full second
