import pytest

from solution import TemporaryError, call_with_retry


def test_gives_up_when_budget_runs_out():
    t = [0.0]

    def always_fails():
        raise TemporaryError()

    def fake_sleep(s):
        t[0] += s

    with pytest.raises(TemporaryError):
        call_with_retry(always_fails, attempts=10, base=1.0, sleep=fake_sleep, budget=5.0, clock=lambda: t[0])
    assert t[0] <= 5.0          # never slept past the budget
